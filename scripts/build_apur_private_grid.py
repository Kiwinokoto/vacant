#!/usr/bin/env python3
"""Build a private, auditable Paris-wide Apur tile grid (not a public release).

Input: unchanged official Apur SHP ZIP and private acquisition manifest.
Output: immutable-by-policy directory of GeoJSON cells + provenance manifest.
Tile geometries are NOT clipped or simplified. Features crossing cell boundaries
are repeated; consumers MUST deduplicate by OBJECTID across visible cells.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import shutil
import stat
import tempfile
import zipfile

EXPECTED_COUNT = 128206
EXPECTED_MEMBERS = frozenset({
    "EMPRISE_BATIE_PARIS.shp", "EMPRISE_BATIE_PARIS.shx",
    "EMPRISE_BATIE_PARIS.dbf", "EMPRISE_BATIE_PARIS.prj",
    "EMPRISE_BATIE_PARIS.cpg",
})
PERIOD_CODES = frozenset({1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 99})
MAX_SOURCE_BYTES = 250_000_000
MAX_EXPANDED_BYTES = 200_000_000
MAX_CELL_COPIES_PER_FEATURE = 100
ALLOWED_CELL_SIZES = (250, 500, 1000)


def sha256_file(filename: Path) -> str:
    digest = hashlib.sha256()
    with filename.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def verify_snapshot(archive: Path, manifest: Path) -> str:
    if not archive.is_file() or archive.stat().st_size > MAX_SOURCE_BYTES:
        raise ValueError("Missing or oversized Apur source archive")
    recorded = json.loads(manifest.read_text(encoding="utf-8"))
    info = recorded["files"][archive.name]
    actual = sha256_file(archive)
    if (archive.stat().st_size != info["size_bytes"] or
            actual != info["sha256"] or len(actual) != 64):
        raise ValueError("Source ZIP SHA-256 or byte size differs from frozen manifest")
    return actual


def safe_private_destination(destination: Path) -> Path:
    # Staging and final directory MUST remain outside any served/site paths.
    parent = destination.parent.resolve(strict=True)
    if (parent.stat().st_mode & (stat.S_IRWXG | stat.S_IRWXO) or
            any(p in {"site", ".git", "releases", "raw"} for p in parent.parts) or
            destination.exists() or destination.is_symlink()):
        raise ValueError("Expected fresh destination under private mode-0700 directory")
    return parent


def normal_height(row: dict) -> float | None:
    mid, lo, hi = (row.get(k) for k in ("h_med", "h_min", "h_max"))
    if not isinstance(mid, (int, float)) or not math.isfinite(mid) or mid <= 0:
        return None
    if ((isinstance(lo, (int, float)) and mid < lo) or
            (isinstance(hi, (int, float)) and mid > hi)):
        return None
    return round(float(mid), 2)


def candidate_cells(geometry, cell_size: int):
    """Only grid cells with a *positive area* overlap; no edge-only duplicates."""
    from shapely.geometry import box
    xmin, ymin, xmax, ymax = geometry.bounds
    x0, x1 = math.floor(xmin / cell_size), math.floor(xmax / cell_size)
    y0, y1 = math.floor(ymin / cell_size), math.floor(ymax / cell_size)
    count = (x1 - x0 + 1) * (y1 - y0 + 1)
    if count > MAX_CELL_COPIES_PER_FEATURE:
        raise ValueError("Extremely large polygon bounding box; manual review required")
    cells = []
    for cx in range(x0, x1 + 1):
        for cy in range(y0, y1 + 1):
            tile = box(cx * cell_size, cy * cell_size,
                       (cx + 1) * cell_size, (cy + 1) * cell_size)
            if geometry.intersects(tile) and geometry.intersection(tile).area > 0:
                cells.append((cx, cy))
    if not cells:
        raise ValueError("Polygon did not intersect a positive-area grid cell")
    return cells


def geographic_bbox(ix: int, iy: int, cell_size: int, transformer):
    """Approximate safe WGS84 envelope of a projected square, densified edges."""
    bounds = []
    xmin, ymin = ix * cell_size, iy * cell_size
    for k in range(9):
        offset = k * cell_size / 8
        bounds.extend(((xmin + offset, ymin), (xmin + offset, ymin + cell_size),
                       (xmin, ymin + offset), (xmin + cell_size, ymin + offset)))
    points = [transformer.transform(x, y) for x, y in bounds]
    return [min(x for x, _ in points), min(y for _, y in points),
            max(x for x, _ in points), max(y for _, y in points)]


def build(archive: Path, manifest: Path, destination: Path, *,
          cell_size: int = 500, expected_records: int = EXPECTED_COUNT):
    import shapefile
    from pyproj import CRS, Transformer
    from shapely.geometry import shape, mapping
    from shapely.ops import transform

    if cell_size not in ALLOWED_CELL_SIZES:
        raise ValueError("Unsupported grid cell size")
    archive, manifest, destination = map(Path, (archive, manifest, destination))
    parent = safe_private_destination(destination)
    frozen_hash = verify_snapshot(archive, manifest)
    to_geo = Transformer.from_crs(2154, 4326, always_xy=True)
    features_by_cell = defaultdict(list)
    skipped = Counter()
    counts = Counter()
    periods = Counter()
    heights = Counter()
    seen_ids = set()
    seen_nonnull_business_ids = set()
    stage = Path(tempfile.mkdtemp(prefix=".apur-grid-staging-", dir=parent))
    os.chmod(stage, 0o700)
    try:
        with zipfile.ZipFile(archive) as z:
            if set(z.namelist()) != EXPECTED_MEMBERS:
                raise ValueError("Unexpected source SHP ZIP members")
            if sum(x.file_size for x in z.infolist()) > MAX_EXPANDED_BYTES or z.testzip() is not None:
                raise ValueError("Source ZIP expansion/CRC validation failed")
            if CRS.from_wkt(z.read("EMPRISE_BATIE_PARIS.prj").decode()).to_epsg() != 2154:
                raise ValueError("Expected Apur source CRS EPSG:2154")
            with (z.open("EMPRISE_BATIE_PARIS.shp") as shp,
                  z.open("EMPRISE_BATIE_PARIS.shx") as shx,
                  z.open("EMPRISE_BATIE_PARIS.dbf") as dbf):
                reader = shapefile.Reader(shp=shp, shx=shx, dbf=dbf, encoding="utf-8")
                if len(reader) != expected_records:
                    raise ValueError("Frozen source record count differs")
                required = {"OBJECTID", "n_sq_eb", "c_perconst", "h_med", "h_min", "h_max"}
                if not required.issubset({x[0] for x in reader.fields[1:]}):
                    raise ValueError("Unexpected Apur DBF field schema")
                for record in reader.iterShapeRecords():
                    counts["read"] += 1
                    values = record.record.as_dict()
                    oid, bid, code = (values.get(k) for k in
                                      ("OBJECTID", "n_sq_eb", "c_perconst"))
                    if not isinstance(oid, int) or oid in seen_ids:
                        raise ValueError("Unexpected or duplicate OBJECTID")
                    seen_ids.add(oid)
                    polygon = shape(record.shape.__geo_interface__)
                    if polygon.is_empty or not polygon.is_valid or polygon.area <= 0 or (
                            polygon.geom_type not in ("Polygon", "MultiPolygon")):
                        skipped["invalid_geometry"] += 1
                        continue
                    if bid is None:
                        skipped["missing_business_id"] += 1
                        continue
                    if bid in seen_nonnull_business_ids:
                        raise ValueError("Duplicate nonempty business identifier")
                    seen_nonnull_business_ids.add(bid)
                    if code is not None and code not in PERIOD_CODES:
                        raise ValueError("Unexpected construction-period code")
                    period = 99 if code is None else int(code)
                    height = normal_height(values)
                    counts["kept"] += 1
                    periods[str(period)] += 1
                    if height is None:
                        heights["missing_zero_or_inconsistent"] += 1
                    else:
                        heights["valid"] += 1
                        if height > 200:
                            heights["over_200_m"] += 1
                    projected = transform(to_geo.transform, polygon)
                    feature = {"type": "Feature", "properties": {
                        "object_id": oid, "period_code": period, "height_m": height,
                    }, "geometry": mapping(projected)}
                    cells = candidate_cells(polygon, cell_size)
                    counts["placements"] += len(cells)
                    counts["multi_cell_features"] += len(cells) > 1
                    for cell in cells:
                        features_by_cell[cell].append(feature)
        if counts["read"] != expected_records:
            raise ValueError("Incomplete source iteration")
        cells = {}
        total_bytes = 0
        for (ix, iy), features in sorted(features_by_cell.items()):
            # No clipping: repeat the same full footprint across its overlapping cells.
            filename = f"cell_{ix}_{iy}.geojson"
            payload = {"type": "FeatureCollection", "features": features}
            encoded = json.dumps(payload, ensure_ascii=False,
                                 separators=(",", ":")).encode("utf-8")
            target = stage / filename
            with target.open("xb") as out:
                os.chmod(target, 0o600)
                out.write(encoded)
            total_bytes += len(encoded)
            cells[f"{ix},{iy}"] = {
                "file": filename, "count": len(features),
                "bytes": len(encoded), "sha256": hashlib.sha256(encoded).hexdigest(),
                "bbox_wgs84": geographic_bbox(ix, iy, cell_size, to_geo),
            }
        result = {
            "research_only": True, "public_release_allowed": False,
            "contains_vacancy_data": False, "source": "Apur EMPRISE_BATIE_PARIS",
            "license": "ODbL-1.0", "scientific_vintage": "not confirmed by Apur",
            "source_archive_sha256": frozen_hash,
            "data_extracted_at_utc": datetime.now(timezone.utc).isoformat(),
            "source_crs": "EPSG:2154", "output_crs": "EPSG:4326",
            "source_geometry_policy": "keep original polygons, never repair or simplify",
            "grid_policy": "positive-area cell intersection, full-shape repeats, client dedup by object_id",
            "grid_cell_m": cell_size, "source_count": counts["read"],
            "unique_features": counts["kept"], "placements": counts["placements"],
            "multi_cell_features": counts["multi_cell_features"],
            "skipped_by_exclusive_reason": dict(skipped), "period_counts": dict(periods),
            "height_counts": dict(heights), "total_geojson_bytes": total_bytes,
            "cell_count": len(cells), "max_cell_bytes": max((v["bytes"] for v in cells.values()), default=0),
            "max_cell_features": max((v["count"] for v in cells.values()), default=0),
            "cells": cells,
        }
        with (stage / "manifest.json").open("x", encoding="utf-8") as f:
            os.chmod(stage / "manifest.json", 0o600)
            json.dump(result, f, ensure_ascii=False, indent=2)
        # The destination must be new. Never modify an earlier snapshot.
        if destination.exists() or destination.is_symlink():
            raise ValueError("Output appeared while building")
        stage.rename(destination)
        stage = None
        return {key: value for key, value in result.items() if key != "cells"}
    finally:
        if stage is not None:
            shutil.rmtree(stage)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("destination", type=Path)
    parser.add_argument("--cell-m", type=int, choices=ALLOWED_CELL_SIZES, default=500)
    args = parser.parse_args()
    print(json.dumps(build(args.archive, args.manifest, args.destination,
                           cell_size=args.cell_m), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
