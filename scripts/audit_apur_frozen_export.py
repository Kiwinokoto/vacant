#!/usr/bin/env python3
"""Read-only SIG audit of a private Apur SHP snapshot. Aggregates only, no export."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import zipfile

PERIODS = {1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 99}
MEMBERS = {"EMPRISE_BATIE_PARIS.shp", "EMPRISE_BATIE_PARIS.shx",
           "EMPRISE_BATIE_PARIS.dbf", "EMPRISE_BATIE_PARIS.prj",
           "EMPRISE_BATIE_PARIS.cpg"}

def check_hash(path, manifest):
    record = json.loads(Path(manifest).read_text(encoding="utf-8"))
    meta = record["files"][Path(path).name]
    digest = hashlib.sha256()
    with Path(path).open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    if digest.hexdigest() != meta["sha256"] or Path(path).stat().st_size != meta["size_bytes"]:
        raise ValueError("Frozen archive hash or size differs from manifest")
    return digest.hexdigest()

def should_check_geometry(oid, code, height):
    if type(oid) is not int:
        raise ValueError("Invalid OBJECTID")
    return oid % 17 == 0 or code in (None, 99) or (height is not None and height > 200)

def height_flags(row):
    median, low, high = (row.get(x) for x in ("h_med", "h_min", "h_max"))
    return ([ "missing" ] if median is None else
            ["zero"] if median == 0 else []) + (
            ["below_min"] if median is not None and low is not None and median < low else []) + (
            ["above_max"] if median is not None and high is not None and median > high else []) + (
            ["above_200"] if median is not None and median > 200 else [])

def audit(path, manifest, *, full_geometries=False):
    import shapefile
    from shapely.geometry import shape
    from shapely.validation import explain_validity
    from pyproj import Transformer
    path = Path(path)
    if path.stat().st_size > 250_000_000:
        raise ValueError("Archive exceeds limit")
    checksum = check_hash(path, manifest)
    counts, periods, heights = Counter(), Counter(), Counter()
    kinds, invalid, grid = Counter(), Counter(), Counter()
    keys, object_ids = set(), set()
    max_edit = ""
    converter = Transformer.from_crs(2154, 4326, always_xy=True)
    with zipfile.ZipFile(path) as archive:
        if set(archive.namelist()) != MEMBERS or sum(x.file_size for x in archive.infolist()) > 200_000_000:
            raise ValueError("Unexpected archive members or expansion")
        if archive.testzip():
            raise ValueError("ZIP CRC failure")
        with archive.open("EMPRISE_BATIE_PARIS.shp") as shp, archive.open("EMPRISE_BATIE_PARIS.shx") as shx, archive.open("EMPRISE_BATIE_PARIS.dbf") as dbf:
            reader = shapefile.Reader(shp=shp, shx=shx, dbf=dbf, encoding="utf-8")
            for feature in reader.iterShapeRecords():
                a = feature.record.as_dict()
                counts["total"] += 1
                oid, key, code, h = (a.get(x) for x in ("OBJECTID", "n_sq_eb", "c_perconst", "h_med"))
                if oid in object_ids:
                    counts["duplicate_objectid"] += 1
                object_ids.add(oid)
                if key is None:
                    counts["business_id_null"] += 1
                elif key in keys:
                    counts["business_id_duplicate_nonnull"] += 1
                else:
                    keys.add(key)
                periods[str(code)] += 1
                if code not in PERIODS and code is not None:
                    counts["unknown_period_code"] += 1
                if a.get("an_const") is None:
                    counts["year_null"] += 1
                for flag in height_flags(a):
                    heights[flag] += 1
                edited = str(a.get("last_edi_1") or "")[:10]
                max_edit = max(max_edit, edited)
                if not full_geometries and not should_check_geometry(oid, code, h):
                    continue
                geom = shape(feature.shape.__geo_interface__)
                kinds[geom.geom_type] += 1
                if not geom.is_valid:
                    invalid[explain_validity(geom).split("[", 1)[0]] += 1
                if not geom.is_empty:
                    x, y = converter.transform(geom.centroid.x, geom.centroid.y)
                    if not (2.15 < x < 2.51 and 48.75 < y < 49):
                        invalid["outside_paris_envelope"] += 1
                    ix = min(4, max(0, int((x - 2.22) / .05)))
                    iy = min(4, max(0, int((y - 48.815) / .017)))
                    grid[f"{ix}-{iy}"] += 1
    if counts["total"] != 128206:
        raise ValueError("Unexpected source record count")
    return {"status": "research_only_not_for_publication", "sha256": checksum,
            "counts": dict(counts), "period_counts": dict(periods),
            "height_flags_nonexclusive": dict(heights), "last_object_edit": max_edit,
            "sample_policy": "OBJECTID mod 17 == 0 or undated or h_med > 200",
            "sampled_geometries": sum(kinds.values()), "full_geometries": full_geometries, "geometry_types": dict(kinds),
            "topological_anomalies": dict(invalid), "occupied_grid_cells_5x5": len(grid)}

if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("archive", type=Path)
    p.add_argument("manifest", type=Path)
    p.add_argument("--full-geometries", action="store_true", help="Run GEOS on every source shape")
    args = p.parse_args()
    print(json.dumps(audit(args.archive, args.manifest, full_geometries=args.full_geometries), indent=2, ensure_ascii=False))
