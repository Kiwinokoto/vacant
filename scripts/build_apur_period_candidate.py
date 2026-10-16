#!/usr/bin/env python3
"""Build a PRIVATE Apur construction-period GeoJSON from a SHA-256 checked SHP ZIP.

Research only: no API, no vacancy join, no silent repair, no public output.
"""
from __future__ import annotations
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import stat
import tempfile
import zipfile

PERIODS = frozenset((1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 99))
EXPECTED_MEMBERS = frozenset({
    "EMPRISE_BATIE_PARIS.shp", "EMPRISE_BATIE_PARIS.shx",
    "EMPRISE_BATIE_PARIS.dbf", "EMPRISE_BATIE_PARIS.prj",
    "EMPRISE_BATIE_PARIS.cpg",
})
MAX_FEATURES = 200


def verify_snapshot(archive: Path, manifest: Path) -> str:
    """Fail closed when source no longer matches original private export."""
    if archive.stat().st_size > 250_000_000:
        raise ValueError("Archive exceeds bounded size")
    record = json.loads(manifest.read_text(encoding="utf-8"))
    entry = record["files"][archive.name]
    sha = hashlib.sha256()
    with archive.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            sha.update(chunk)
    if archive.stat().st_size != entry["size_bytes"] or sha.hexdigest() != entry["sha256"]:
        raise ValueError("Snapshot SHA-256/size mismatch")
    return sha.hexdigest()


def projected_selection(west: float, south: float, east: float, north: float):
    """Densify and project a small WGS84 bounding rectangle, not its L93 envelope."""
    from pyproj import Transformer
    from shapely.geometry import Polygon

    if not (2.15 < west < east < 2.51 and 48.75 < south < north < 49.0
            and east - west <= 0.006 and north - south <= 0.004):
        raise ValueError("Selection must be a small, valid area inside Paris")
    corners = ((west, south), (east, south), (east, north), (west, north))
    geographic_ring = []
    for idx, (ax, ay) in enumerate(corners):
        bx, by = corners[(idx + 1) % 4]
        for part in range(8):
            fraction = part / 8
            geographic_ring.append((ax + (bx-ax)*fraction, ay + (by-ay)*fraction))
    to_m = Transformer.from_crs(4326, 2154, always_xy=True).transform
    return Polygon([to_m(x, y) for x, y in geographic_ring])


def private_target(output: Path):
    """Fail closed on public, shared, source, symlink and existing output paths."""
    parent = output.parent.resolve(strict=True)
    if parent.stat().st_mode & (stat.S_IRWXG | stat.S_IRWXO):
        raise ValueError("Destination directory must be private (0700)")
    if output.suffix.lower() != ".geojson" or output.exists() or output.is_symlink():
        raise ValueError("Unsafe or existing output file")
    if any(piece in ("site", ".git", "releases", "raw") for piece in parent.parts):
        raise ValueError("Refusing source or publicly deployed destination")
    return parent


def build(archive: Path, manifest: Path, output: Path, bbox, max_features=MAX_FEATURES,
          expected_records=128206):
    import shapefile
    from pyproj import CRS, Transformer
    from shapely.geometry import shape, mapping
    from shapely.ops import transform

    if not 1 <= max_features <= MAX_FEATURES:
        raise ValueError("Max features must be 1–200")
    parent = private_target(output)
    digest = verify_snapshot(archive, manifest)
    footprint = projected_selection(*bbox)
    to_geo = Transformer.from_crs(2154, 4326, always_xy=True).transform
    matched, excluded, selected, object_ids = 0, Counter(), [], set()

    with zipfile.ZipFile(archive) as archive_zip:
        if (set(archive_zip.namelist()) != EXPECTED_MEMBERS or
                sum(f.file_size for f in archive_zip.infolist()) > 200_000_000):
            raise ValueError("Unexpected ZIP structure or expanded size")
        if archive_zip.testzip() is not None:
            raise ValueError("Corrupted ZIP")
        crs = CRS.from_wkt(archive_zip.read("EMPRISE_BATIE_PARIS.prj").decode("utf-8"))
        if crs.to_epsg() != 2154:
            raise ValueError("Apur source must be EPSG:2154")
        with (archive_zip.open("EMPRISE_BATIE_PARIS.shp") as shp,
              archive_zip.open("EMPRISE_BATIE_PARIS.shx") as shx,
              archive_zip.open("EMPRISE_BATIE_PARIS.dbf") as dbf):
            reader = shapefile.Reader(shp=shp, shx=shx, dbf=dbf, encoding="utf-8")
            if len(reader) != expected_records:
                raise ValueError("Unexpected source record count")
            for item in reader.iterShapeRecords():
                geom = shape(item.shape.__geo_interface__)
                if not geom.intersects(footprint):
                    continue
                matched += 1
                if matched > max_features:
                    raise ValueError("Selection exceeds cap; no output written")
                attrs = item.record.as_dict()
                oid, key, period = (attrs.get(k) for k in
                                    ("OBJECTID", "n_sq_eb", "c_perconst"))
                if not isinstance(oid, int) or oid in object_ids:
                    raise ValueError("Missing or duplicated OBJECTID")
                object_ids.add(oid)
                if (geom.is_empty or not geom.is_valid or geom.area <= 0 or
                        geom.geom_type not in ("Polygon", "MultiPolygon")):
                    excluded["invalid_geometry"] += 1
                    continue
                if key is None:
                    excluded["missing_business_id"] += 1
                    continue
                if period is not None and period not in PERIODS:
                    raise ValueError("Unknown construction period")
                # Do not clip, repair or simplify. No vacancy information is read.
                selected.append({
                    "type": "Feature",
                    "properties": {"object_id": oid, "period_code": period},
                    "geometry": mapping(transform(to_geo, geom)),
                })

    payload = {
        "type": "FeatureCollection",
        "metadata": {
            "research_only": True, "public_release_allowed": False,
            "not_vacancy_data": True,
            "source": "Atelier parisien d'urbanisme — EMPRISE_BATIE_PARIS",
            "license": "ODbL-1.0",
            "source_archive_sha256": digest,
            "scientific_vintage": "not confirmed by Apur",
            "extracted_at_utc": datetime.now(timezone.utc).isoformat(),
            "source_crs": "EPSG:2154", "output_crs": "EPSG:4326",
            "bbox_wgs84": list(bbox),
            "selection_rule": "intersects densified WGS84 rectangle reprojected to EPSG:2154",
            "geometry_policy": "GEOS valid only; no silent correction, clipping or simplification",
            "matched_source_features": matched,
            "excluded": dict(sorted(excluded.items())),
            "included_features": len(selected),
            "scope": "current Apur footprints, NOT historical inventory or vacant buildings",
        },
        "features": selected,
    }
    # Private temp + atomic no-overwrite hard link: no competing output can be replaced.
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", prefix=".apur-period-",
            suffix=".part", dir=parent, delete=False
        ) as fh:
            temporary = Path(fh.name)
            os.chmod(temporary, 0o600)
            json.dump(payload, fh, ensure_ascii=False, separators=(",", ":"))
        os.link(temporary, output)
        temporary.unlink()
        temporary = None
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    return payload["metadata"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--bbox", nargs=4, required=True, type=float,
                        metavar=("WEST", "SOUTH", "EAST", "NORTH"))
    parser.add_argument("--max-features", type=int, default=MAX_FEATURES)
    args = parser.parse_args()
    print(json.dumps(build(args.archive, args.manifest, args.output, args.bbox,
                           args.max_features), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
