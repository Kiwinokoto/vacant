#!/usr/bin/env python3
"""Compare three *secondary* historical Paris IRIS geometry sources.

Strictly private diagnostic. Neither the 2013 OSM adaptation nor the 2016
reprojection qualifies as an authenticated IGN original or 2018 geometry.
"""
import argparse
from collections import Counter
from contextlib import contextmanager
from hashlib import sha256
import json
from pathlib import Path
import statistics
import tempfile
from zipfile import ZipFile

from audit_iris2013_candidate import isolated_shapefile

SOURCES = {
    "iris-2013-osm-secondary": {
        "sha": "deb1b378aefa823ad3f2b22700c5c12b8133f782ddb87f059b1dc7518207a2c2",
        "members": {f"Mix_Contours_IRIS_Communes_OSM.{ext}" for ext in ("shp","shx","dbf","prj","qpj","cpg")},
        "basename": "Mix_Contours_IRIS_Communes_OSM",
        "field": "dcomiris",
        "crs": "EPSG:2154",
    },
    "iris-2016-secondary": {
        "sha": "843049e9af98c25bb74f9c8d8fe84348429596a3bf69fb6406b77fa8951436cd",
        "members": {f"contours_iris_2016/contours_iris_2016.{ext}" for ext in ("shp","shx","dbf","cpg")},
        "basename": "contours_iris_2016",
        "field": "CODE_IRIS",
        # Only claimed in the publisher's 2017 description; no PRJ in archive.
        "crs": "EPSG:4326",
    },
}
ORIGINAL2013_SHA = "c6afee56f81b3a9d08316034f0f48259162276a3d7a0d11388c2472f2fd5d3a7"
REPORT_STATUS = "research_only_not_approved_for_publication"


def digest(path):
    h = sha256()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(1024 * 1024), b""):
            h.update(b)
    return h.hexdigest()


def verify_manifest(root, name, expected):
    path = root / "raw/secondary" / name / "source.zip"
    manifest = root / "manifests" / f"{name}-20261016.json"
    if not path.is_file() or not manifest.is_file() or digest(path) != expected:
        raise ValueError(f"Missing/mismatching private archive: {name}")
    info = json.loads(manifest.read_text(encoding="utf-8"))
    if info.get("sha256") != expected or info.get("dataset_id") != name:
        raise ValueError(f"Bad source manifest: {name}")
    if info.get("status") != "secondary_candidate_private_not_approved_for_publishing":
        raise ValueError("Secondary data publication status unexpectedly changed")
    return path


@contextmanager
def safe_shapefile(zip_path, spec):
    """Extract whitelisted shapefile components; no path traversal or writable ZIP paths."""
    with tempfile.TemporaryDirectory(prefix="vacant-historic-crosscheck-") as temp:
        root = Path(temp)
        with ZipFile(zip_path) as z:
            inf = [v for v in z.infolist() if not v.is_dir()]
            if {v.filename for v in inf} != spec["members"]:
                raise ValueError("Archive has unexpected/missing members")
            if any(v.flag_bits & 1 or v.file_size > 150_000_000 for v in inf):
                raise ValueError("Encrypted or oversized archive member")
            for v in inf:
                name = Path(v.filename).name
                if name != spec["basename"] + Path(name).suffix:
                    raise ValueError("Archive entry basename mismatch")
                with z.open(v) as source, (root / name).open("xb") as target:
                    import shutil
                    shutil.copyfileobj(source, target, 1024 * 1024)
        prj = root / (spec["basename"] + ".prj")
        if prj.is_file():
            data = prj.read_text(encoding="utf-8")
            if "Lambert" not in data and "LAMBERT" not in data and "RGF_1993" not in data:
                raise ValueError("Expected metric projected Lambert-93 CRS in OSM archive")
        yield root / spec["basename"]


def load_paris(reader, field, project):
    from shapely.geometry import shape
    from shapely.ops import transform
    by_code, counts = {}, Counter()
    for index, row in enumerate(reader.iterRecords()):
        code = str(row[field]).strip()
        if code.startswith("751"):
            if len(code) != 9 or not code.isdigit():
                raise ValueError("Invalid Paris IRIS code")
            counts[code] += 1
            if code in by_code:
                continue
            geom = shape(reader.shape(index).__geo_interface__)
            if not geom.is_valid or geom.is_empty:
                raise ValueError(f"Invalid geometry for {code}")
            geom = transform(project, geom) if project is not None else geom
            if geom.area <= 0:
                raise ValueError(f"Non-positive geometry area for {code}")
            by_code[code] = geom
    if len(by_code) != 992:
        raise ValueError(f"Expected 992 Paris IRIS; got {len(by_code)}")
    return by_code, counts


def metrics(left, right):
    if set(left) != set(right):
        raise ValueError("Cannot compare different Paris IRIS code sets")
    measures = []
    for code in sorted(left):
        a, b = left[code], right[code]
        union = a.union(b).area
        if union <= 0:
            raise ValueError("Bad/zero geographic union")
        measures.append((a.intersection(b).area / union, code))
    measures.sort()
    scores = [x[0] for x in measures]
    return {
        "matched_codes": len(measures),
        "min_iou": round(scores[0], 5),
        "min_iou_code": measures[0][1],
        "median_iou": round(statistics.median(scores), 5),
        "p10_iou": round(scores[len(scores)//10], 5),
        "p90_iou": round(scores[len(scores)*9//10], 5),
        "below_iou_0_99": sum(x < .99 for x in scores),
        "below_iou_0_95": sum(x < .95 for x in scores),
    }


def audit(root):
    import shapefile
    from pyproj import Transformer

    original = root / "raw/secondary/iris-2013-candidate/iris-2013-01-01.zip"
    if digest(original) != ORIGINAL2013_SHA:
        raise ValueError("2013 original third-party archive changed")
    projector = Transformer.from_crs("EPSG:4326", "EPSG:2154", always_xy=True).transform
    with isolated_shapefile(original) as basename:
        old, old_count = load_paris(shapefile.Reader(basename, encoding="latin1"), "DCOMIRIS", projector)
    if set(old_count.values()) != {10}:
        raise ValueError("2013 original duplicate pattern changed")

    compared = {}
    for name,spec in SOURCES.items():
        zip_path = verify_manifest(root, name, spec["sha"])
        with safe_shapefile(zip_path, spec) as basename:
            current, counts = load_paris(
                shapefile.Reader(str(basename), encoding="latin1"), spec["field"],
                projector if spec["crs"] == "EPSG:4326" else None
            )
        if set(counts.values()) != {1}:
            raise ValueError(f"Unexpected duplicates in independent source: {name}")
        compared[name] = current

    census2025 = root / "processed/iris-2023/iris-2023.geojson"
    from audit_iris2013_candidate import digest as digest2025
    from audit_iris2013_candidate import SOURCE_SHA as old_source_sha
    if old_source_sha != ORIGINAL2013_SHA:
        raise ValueError("Pinned 2013 hash inconsistent across auditors")
    from build_arrondissement_history import GEOMETRY_SHA
    if digest2025(census2025) != GEOMETRY_SHA:
        raise ValueError("Reference 2025 changed")
    from shapely.geometry import shape
    from shapely.ops import transform
    features = json.loads(census2025.read_text(encoding="utf-8"))["features"]
    new2025 = {f["properties"]["iris_code"]:transform(projector,shape(f["geometry"])) for f in features}
    return {
        "status": REPORT_STATUS,
        "2013_candidate_vs_2013_OSM_modified": metrics(old, compared["iris-2013-osm-secondary"]),
        "2013_candidate_vs_2016_secondary": metrics(old, compared["iris-2016-secondary"]),
        "2016_secondary_vs_2025_IGN": metrics(compared["iris-2016-secondary"], new2025),
        "sources": {x: v["sha"] for x,v in SOURCES.items()},
        "qualification": [
            "2013 OSM modifies municipal outlines and is ODbL; not an original IGN file",
            "2016 geometry is not 2018 geography used by RP2016; do not join automatically",
            "no secondary geometry accepted for publication or used to localize dwellings",
        ],
    }


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--data-root",type=Path,default=Path("/srv/vacant/data"))
    a=parser.parse_args()
    print(json.dumps(audit(a.data_root),indent=2,ensure_ascii=False))


if __name__=="__main__":
    main()
