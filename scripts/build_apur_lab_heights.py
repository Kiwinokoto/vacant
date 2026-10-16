#!/usr/bin/env python3
"""Build a private period/height candidate from immutable Apur SHP and validated period GeoJSON.

No public output, no joins to Insee/LOVAC/Paris Data, no network calls.
"""
import argparse
from collections import Counter
from hashlib import sha256
import json
import os
from pathlib import Path
import stat
import tempfile
import zipfile


def sha_file(path):
    digest = sha256()
    with open(path, "rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normal_height(row):
    med, low, high = (row.get(k) for k in ("h_med", "h_min", "h_max"))
    if not isinstance(med, (int, float)) or med <= 0:
        return None
    if ((isinstance(low, (int, float)) and med < low) or
            (isinstance(high, (int, float)) and med > high)):
        return None
    # A large, plausible emprise (Tour Eiffel) should not be silently clipped.
    return round(float(med), 2)


def build(source, manifest, candidate, candidate_sha, target):
    import shapefile
    from pyproj import CRS
    source, manifest, candidate, target = map(Path, (source, manifest, candidate, target))
    if not source.is_file() or source.stat().st_size > 250_000_000:
        raise ValueError("Missing or oversized frozen Apur archive")
    manifest_data = json.loads(manifest.read_text())
    entry = manifest_data["files"][source.name]
    if source.stat().st_size != entry["size_bytes"] or sha_file(source) != entry["sha256"]:
        raise ValueError("Frozen Apur ZIP SHA-256 mismatch")
    if sha_file(candidate) != candidate_sha:
        raise ValueError("Period candidate SHA-256 mismatch")
    old = json.loads(candidate.read_text())
    if old.get("type") != "FeatureCollection" or len(old.get("features", [])) != 150:
        raise ValueError("Unexpected period candidate cardinality")
    meta = old.get("metadata", {})
    if (meta.get("source_archive_sha256") != entry["sha256"] or
            meta.get("included_features") != 150 or
            meta.get("public_release_allowed") is not False):
        raise ValueError("Invalid private period candidate provenance")
    folder = target.parent.resolve(strict=True)
    if (folder.stat().st_mode & (stat.S_IRWXG | stat.S_IRWXO) or
            target.exists() or target.is_symlink() or
            target.suffix != ".geojson" or
            any(part in ("site", "releases", "raw", ".git") for part in folder.parts)):
        raise ValueError("Output must be new and strictly private")
    ids = set()
    for f in old["features"]:
        k = f.get("properties", {}).get("object_id")
        if not isinstance(k, int) or k in ids or set(f["properties"]) != {"object_id", "period_code"}:
            raise ValueError("Malformed period candidate identifiers")
        ids.add(k)
    values = {}
    with zipfile.ZipFile(source) as z:
        if z.testzip() is not None:
            raise ValueError("ZIP CRC mismatch")
        if CRS.from_wkt(z.read("EMPRISE_BATIE_PARIS.prj").decode()).to_epsg() != 2154:
            raise ValueError("Unexpected EPSG")
        with (z.open("EMPRISE_BATIE_PARIS.shp") as shp,
              z.open("EMPRISE_BATIE_PARIS.shx") as shx,
              z.open("EMPRISE_BATIE_PARIS.dbf") as dbf):
            reader = shapefile.Reader(shp=shp, shx=shx, dbf=dbf, encoding="utf-8")
            if len(reader) != 128206:
                raise ValueError("Source cardinality changed")
            for record in reader.iterRecords():
                attrs = record.as_dict()
                oid = attrs["OBJECTID"]
                if oid in ids:
                    if oid in values:
                        raise ValueError("Duplicate source OBJECTID")
                    values[oid] = normal_height(attrs)
    if len(values) != 150:
        raise ValueError("Source OBJECTID mismatch")
    features = []
    flags = Counter()
    for f in old["features"]:
        oid = f["properties"]["object_id"]
        height = values[oid]
        if height is None:
            flags["height_unavailable_or_inconsistent"] += 1
        features.append({"type": "Feature", "geometry": f["geometry"], "properties": {
            "object_id": oid, "period_code": f["properties"]["period_code"], "height_m": height
        }})
    result = {"type": "FeatureCollection", "metadata": {
        "research_only": True, "public_release_allowed": False,
        "not_vacancy_data": True, "license": "ODbL-1.0",
        "source_archive_sha256": entry["sha256"],
        "source_period_candidate_sha256": candidate_sha,
        "scientific_vintage": "not confirmed by Apur",
        "source_crs": "EPSG:2154", "output_crs": "EPSG:4326",
        "expected_features": 150, "included_features": len(features),
        "height_unit": "m", "height_field": "h_med",
        "height_invalid_policy": "null if missing, zero, or outside min/max",
        "height_quality_flags": dict(flags),
        "scope": "current Apur footprints only; no building vacancy",
    }, "features": features}
    pending = None
    try:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=folder,
                                         prefix=".apur-heights-", suffix=".tmp", delete=False) as output:
            pending = Path(output.name)
            os.chmod(pending, 0o600)
            json.dump(result, output, ensure_ascii=False, separators=(",", ":"))
        os.link(pending, target)  # No overwrite, even if another process created the target.
    finally:
        if pending is not None:
            pending.unlink(missing_ok=True)
    return {"sha256": sha_file(target), "size_bytes": target.stat().st_size,
            "included_features": len(features), "quality": dict(flags)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("period_candidate", type=Path)
    parser.add_argument("period_candidate_sha256")
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    print(json.dumps(build(args.source, args.manifest, args.period_candidate,
                           args.period_candidate_sha256, args.output), indent=2))
