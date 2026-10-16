#!/usr/bin/env python3
"""Audit the institutionally distributed Atlasanté 'IGN Métropole IRIS 2014'.

Read the pinned SQL dump as *data*, never execute it. Compare Paris geometries
with the privately audited third-party candidate claiming geometry 2013.
No redistribution, no public geometry export, no database operation.
"""
import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import re
from zipfile import ZipFile

from audit_iris2013_candidate import (
    SOURCE_SHA as CANDIDATE_SHA, audit as check_candidate, isolated_shapefile,
)

ARCHIVE_SHA = "5cefdde58d228b3f8643d01ef61c80c10bf4ce30a30e78b61e2dc48fdf9acf27"
MANIFEST_NAME = "iris-2014-atlasante-20261016.json"
STATUS = "institutional_crosscheck_verified_geometry_not_licensed_for_publication"

# Limit the SQL grammar to the exact INSERT row structure. No SQL is executed.
INSERT_PREFIX = (
    b'INSERT INTO "public"."ign_metropole_contours_iris2014_z" '
    b'("the_geom" , "depcom", "nom_com", "iris", "dcomiris", "nom_iris", '
    b'"typ_iris", "origine") VALUES ('
)
ATTRIBUTES = re.compile(
    rb"^([0-9]{5})', '((?:[^']|'')*)', '([0-9]{4})', "
    rb"'([0-9]{9})', '((?:[^']|'')*)', '([HADZ])', "
    rb"(?:NULL|'(?:[^']|'')*')\);$"
)
MAX_ARCHIVE_BYTES = 25_000_000
MAX_SQL_BYTES = 130_000_000


def file_sha(path):
    h = sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def parse_paris_insert(line):
    """Return (code, EWKB bytes) only for Paris, None for another commune."""
    if not line.startswith(INSERT_PREFIX):
        raise ValueError("Unexpected INSERT schema")
    contents = line[len(INSERT_PREFIX):].rstrip(b"\r\n")
    if not contents.startswith(b"'"):
        raise ValueError("Missing WKB quoted literal")
    blob, delimiter, tail = contents[1:].partition(b"', '")
    if not delimiter or not re.fullmatch(rb"[0-9A-Fa-f]+", blob):
        raise ValueError("Malformed SQL geometry")
    if not tail.startswith(b"751"):
        return None
    match = ATTRIBUTES.fullmatch(tail)
    if not match:
        raise ValueError("Unexpected Paris attributes")
    dep, _, iris, code, _, _, = match.groups()
    if code != dep + iris or len(code) != 9:
        raise ValueError("Inconsistent Paris IRIS identifier")
    ewkb = bytes.fromhex(blob.decode("ascii"))
    if len(ewkb) < 9 or ewkb[0] != 1 or int.from_bytes(ewkb[5:9], "little") != 2154:
        raise ValueError("Unexpected EWKB SRID (expect 2154)")
    return code.decode("ascii"), ewkb


def load_atlasante(root):
    from shapely.wkb import loads
    path = root / "raw/secondary/iris-2014-atlasante/source.zip"
    manifest = root / "manifests" / MANIFEST_NAME
    if not path.is_file() or not manifest.is_file() or path.stat().st_size > MAX_ARCHIVE_BYTES:
        raise ValueError("Institutional archive not present")
    if file_sha(path) != ARCHIVE_SHA:
        raise ValueError("Institutional source checksum mismatch")
    info = json.loads(manifest.read_text(encoding="utf-8"))
    if info.get("dataset_id") != "iris-2014-atlasante" or info.get("sha256") != ARCHIVE_SHA:
        raise ValueError("Manifest mismatch")
    if "institutional_secondary_source_private" not in info.get("status", ""):
        raise ValueError("Manifest incorrectly permits publication")
    result = {}
    with ZipFile(path) as z:
        members = [x for x in z.infolist() if not x.is_dir()]
        sql = [x for x in members if x.filename.endswith(".sql")]
        metadata = [x for x in members if x.filename.endswith(".xml")]
        if len(members) != 3 or len(sql) != 1 or len(metadata) != 1:
            raise ValueError("Unexpected ZIP member structure")
        if any(x.flag_bits & 1 or x.file_size > MAX_SQL_BYTES for x in members):
            raise ValueError("Encrypted or oversized archive")
        description = z.read(metadata[0]).decode("utf-8")
        if ("IGN - Métropole - IRIS 2014" not in description or
            "conditions générales d'utilisation des fichiers IGN /INSEE" not in description):
            raise ValueError("Incorrect institutional metadata or licensing note")
        with z.open(sql[0]) as lines:
            for line in lines:
                if not line.startswith(b"INSERT INTO"):
                    continue
                parsed = parse_paris_insert(line)
                if parsed is None:
                    continue
                code, blob = parsed
                if code in result:
                    raise ValueError("Duplicate Paris IRIS in 2014 institutional distribution")
                geometry = loads(blob)
                if not geometry.is_valid or geometry.is_empty or geometry.area <= 0:
                    raise ValueError("Invalid institutional geometry: " + code)
                xmin, ymin, xmax, ymax = geometry.bounds
                if not (640000 < xmin < 670000 and 6850000 < ymin < 6870000 and
                        640000 < xmax < 670000 and 6850000 < ymax < 6870000):
                    raise ValueError("Unexpected geometry coordinates, not Lambert-93 Paris")
                result[code] = geometry
    if len(result) != 992:
        raise ValueError(f"Incomplete Paris coverage in Atlasanté: {len(result)}")
    return result


def audit(root):
    import shapefile
    from shapely.geometry import shape
    from shapely.ops import transform
    from pyproj import Transformer

    atlas = load_atlasante(root)
    # Existing auditor rechecks original SHA, census/ref correspondence,
    # 10x duplicate equivalence, geometry validity and topology.
    prior = check_candidate(root)
    if prior.get("quality", {}).get("paris_unique_iris") != 992:
        raise ValueError("Prior candidate verification changed")
    path = root / "raw/secondary/iris-2013-candidate/iris-2013-01-01.zip"
    if file_sha(path) != CANDIDATE_SHA:
        raise ValueError("Candidate archive SHA mismatch")
    projector = Transformer.from_crs(4326, 2154, always_xy=True).transform
    shapes = {}
    counts = Counter()
    with isolated_shapefile(path) as name:
        with shapefile.Reader(name, encoding="latin1") as reader:
            for i,row in enumerate(reader.iterRecords()):
                code = str(row["DCOMIRIS"]).strip()
                if code.startswith("751"):
                    counts[code] += 1
                    if code not in shapes:
                        shapes[code] = transform(projector, shape(reader.shape(i).__geo_interface__))
    if set(shapes) != set(atlas) or set(counts.values()) != {10}:
        raise ValueError("Atlasanté/candidate IRIS mismatch")
    differences, ious = [], []
    for code,g in atlas.items():
        other = shapes[code]
        diff = g.symmetric_difference(other).area
        union = g.union(other).area
        differences.append((diff,code))
        ious.append(g.intersection(other).area/union)
    maximum, code = max(differences)
    if maximum >= 0.001 or min(ious) < 0.999999:
        raise ValueError("Institutional and 2013 candidate outlines differ")
    return {
        "status": STATUS,
        "2014_atlasante_sha256": ARCHIVE_SHA,
        "2013_candidate_sha256": CANDIDATE_SHA,
        "paris_unique_iris":len(atlas),
        "invalid_2014_geometries":0,
        "max_symmetric_difference_sq_m":round(maximum,9),
        "min_iou":round(min(ious),10),
        "median_iou":round(sorted(ious)[len(ious)//2],10),
        "note": "Geometry equivalence corroborated by institutional archive labelled 2014. Not direct proof of 2013 official edition or public redistribution rights.",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-root", type=Path, default=Path("/srv/vacant/data"))
    args = parser.parse_args()
    print(json.dumps(audit(args.data_root),ensure_ascii=False,indent=2))


if __name__ == "__main__":
    main()
