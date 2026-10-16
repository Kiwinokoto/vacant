#!/usr/bin/env python3
"""Audit third-party 2013 IRIS geometries against Insee RP2011 and IGN 2025.

Produces only an explicitly *unpublished* private candidate derivative. This
secondary upload is not an authoritative archived IGN original.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from contextlib import contextmanager
from hashlib import sha256
import json
from pathlib import Path
import statistics
import tempfile
from zipfile import ZipFile

from audit_iris_references import audited_file, one_workbook, read_paris
from build_arrondissement_history import read_legacy_year, GEOMETRY_SHA

SOURCE_SHA = "c6afee56f81b3a9d08316034f0f48259162276a3d7a0d11388c2472f2fd5d3a7"
SOURCE_URL = "https://www.data.gouv.fr/s/resources/contour-des-iris-insee-tout-en-un/20150428-161348/iris-2013-01-01.zip"
MEMBERS = {"iris-2013-01-01." + ext for ext in ("shp", "shx", "dbf", "prj")}
PRIVATE_STATUS = "candidate_secondary_2013_not_approved_for_publication"


def digest(path):
    h = sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def variants_equivalent(geometries, threshold_sq_m=0.001):
    """A duplicate is acceptable only if its geometry is nearly identical."""
    if not geometries or any(g.is_empty or not g.is_valid for g in geometries):
        raise ValueError("Invalid/empty geometric variant")
    base = geometries[0]
    max_area = 0.0
    for other in geometries[1:]:
        difference = base.symmetric_difference(other).area
        max_area = max(max_area, difference)
        if difference > threshold_sq_m:
            raise ValueError(f"Conflicting polygons for one code: {difference:.6f} m2")
    return max_area


@contextmanager
def isolated_shapefile(archive):
    """Whitelisted uncompressed files only, never extract arbitrary ZIP paths."""
    with tempfile.TemporaryDirectory(prefix="vacant-iris2013-") as tmp:
        with ZipFile(archive) as z:
            infos = [i for i in z.infolist() if not i.is_dir()]
            if {x.filename for x in infos} != MEMBERS:
                raise ValueError("Unexpected ZIP members")
            if any(i.flag_bits & 1 or i.file_size > 650_000_000 for i in infos):
                raise ValueError("Encrypted or oversized ZIP member")
            for info in infos:
                out = Path(tmp) / info.filename
                with z.open(info) as source, out.open("xb") as dest:
                    import shutil
                    shutil.copyfileobj(source, dest, 1024 * 1024)
        projection = (Path(tmp) / "iris-2013-01-01.prj").read_text(encoding="ascii")
        if "WGS_1984" not in projection or "Degree" not in projection:
            raise ValueError("Unexpected coordinate system")
        yield str(Path(tmp) / "iris-2013-01-01")


def audit(data_root, output=None):
    import shapefile
    from shapely.geometry import shape, mapping
    from shapely.ops import transform, unary_union
    from pyproj import Transformer

    original = data_root / "raw/secondary/iris-2013-candidate/iris-2013-01-01.zip"
    manifest = data_root / "manifests/secondary-iris2013-reprojected-20261016.json"
    if digest(original) != SOURCE_SHA:
        raise ValueError("Secondary original changed")
    record = json.loads(manifest.read_text(encoding="utf-8"))
    if record.get("sha256") != SOURCE_SHA or record.get("request_url") != SOURCE_URL:
        raise ValueError("Source metadata does not match immutable candidate")
    ref, _ = audited_file(data_root / "raw/insee", data_root / "manifests",
                          "iris-ref2013", "IRIS_table_geo2013.zip")
    book, fmt = one_workbook(ref, ".xls")
    codes2013 = read_paris(book, fmt, 2013, strict_reference=True)
    rp2011 = read_legacy_year(2011, data_root / "raw/insee/rp2011/infra-logement-2011.zip")
    census = {c: (h, v) for c, h, v in rp2011}
    if set(census) != set(codes2013):
        raise ValueError("2011 census mismatches Insee geography 2013")

    polygon2025 = data_root / "processed/iris-2023/iris-2023.geojson"
    if digest(polygon2025) != GEOMETRY_SHA:
        raise ValueError("IGN 2025 validated derivative changed")
    features2025 = json.loads(polygon2025.read_text(encoding="utf-8"))["features"]
    shapes2025 = {f["properties"]["iris_code"]: shape(f["geometry"]) for f in features2025}
    if set(shapes2025) != set(codes2013):
        raise ValueError("2025 reference code count mismatches 2013")

    to_metric = Transformer.from_crs("EPSG:4326", "EPSG:2154", always_xy=True).transform
    by_code = defaultdict(list)
    selected = {}
    max_noise = 0.0
    with isolated_shapefile(original) as shp_file:
        with shapefile.Reader(shp_file, encoding="latin1") as reader:
            for idx, row in enumerate(reader.iterRecords()):
                code = str(row["DCOMIRIS"]).strip()
                if code.startswith("751"):
                    if code not in codes2013:
                        raise ValueError("Unknown Paris IRIS in secondary map: " + code)
                    if str(row["TYP_IRIS"]).strip() != codes2013[code][1]:
                        raise ValueError("Type mismatch for " + code)
                    by_code[code].append(idx)
            if set(by_code) != set(codes2013):
                raise ValueError("Secondary coverage incomplete")
            if any(len(indices) != 10 for indices in by_code.values()):
                raise ValueError("Source duplication pattern changed unexpectedly")
            ious = []
            for code, indices in by_code.items():
                geom_variants = [shape(reader.shape(i).__geo_interface__) for i in indices]
                metric_variants = [transform(to_metric, g) for g in geom_variants]
                max_noise = max(max_noise, variants_equivalent(metric_variants))
                selected[code] = geom_variants[0]
                reference = transform(to_metric, shapes2025[code])
                a = metric_variants[0]
                ious.append(a.intersection(reference).area / a.union(reference).area)
    if len(selected) != 992:
        raise ValueError("Unexpected Paris cardinality")
    metric_polygons = [transform(to_metric, g) for g in selected.values()]
    combined = unary_union(metric_polygons)
    overlap = sum(g.area for g in metric_polygons) - combined.area
    if not combined.is_valid or overlap > 1.0 or overlap < -1.0:
        raise ValueError(f"Overlapping or invalid Paris partition: {overlap}")
    if max_noise > 0.001:
        raise ValueError("Geometric duplicate noise too large")
    quality = {
        "paris_unique_iris": len(selected),
        "secondary_records_paris": sum(len(v) for v in by_code.values()),
        "versions_per_iris": 10,
        "max_duplicate_symmetric_difference_sq_m": round(max_noise, 6),
        "invalid_iris_count": 0,
        "partition_overlap_sq_m": round(overlap, 6),
        "comparison_to_2025_median_iou": round(statistics.median(ious), 4),
        "comparison_to_2025_min_iou": round(min(ious), 4),
        "comparison_to_2025_iou_below_0_90": sum(x < 0.9 for x in ious)
    }
    result = {
        "status": PRIVATE_STATUS,
        "source": SOURCE_URL,
        "sha256": SOURCE_SHA,
        "census_year": 2011,
        "geography_year_claim": 2013,
        "geometry_origin": "third_party_2015_reprojection_claiming_IGN_2013",
        "licence_claim": "Licence Ouverte on the third-party data.gouv.fr page",
        "quality": quality
    }
    if output:
        allowed = (data_root / "processed").resolve()
        target = output.resolve()
        if not target.is_relative_to(allowed) or target.exists():
            raise ValueError("Output must be a new file in private processed data directory")
        geo = {
            "type": "FeatureCollection",
            "features": [],
            "metadata": result,
        }
        for code in sorted(selected):
            h, v = census[code]
            geo["features"].append({
                "type": "Feature", "id": code, "geometry": mapping(selected[code]),
                "properties": {
                    "iris_code": code, "census_year": 2011, "geography_year": 2013,
                    "housing_count": round(h, 5), "vacant_count": round(v, 5),
                    "vacancy_percent": round(100 * v / h, 1) if h >= 50 else None,
                    "status": "statistique_agregee"
                }
            })
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("x", encoding="utf-8") as out:
            json.dump(geo, out, ensure_ascii=False, separators=(",", ":"))
            out.write("\n")
        result["derived_sha256"] = digest(target)
        result["derived_bytes"] = target.stat().st_size
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-root", type=Path, default=Path("/srv/vacant/data"))
    parser.add_argument("--private-output", type=Path,
                        help="Create a GeoJSON candidate in processed/, not inside the public site")
    args = parser.parse_args()
    print(json.dumps(audit(args.data_root, args.private_output),
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
