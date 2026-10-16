#!/usr/bin/env python3
"""Reproducible RP2023/IGN2025/INSEE2025 exact IRIS merge for Paris.

PREPARES data; doesn't publish or modify a web site. Fail closed on mismatches.
Requires Python 3.12 env with duckdb, openpyxl, shapely.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import io
import json
from math import isfinite
from pathlib import Path
import re
import zipfile

import duckdb
import openpyxl
from shapely.geometry import shape

EXPECTED_TOTAL = 1402024
EXPECTED_VACANT = 139075
GEO_YEAR = 2025
RP_YEAR = 2023
SOURCE_IDS = ("rp2023", "iris-ref2025", "contours-iris-2025")
CATEGORIES = ("_T", "DW_VAC")

def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

def read_original(root: Path, source_id: str):
    matches = sorted((root / "manifests").glob(source_id + "-*.json"))
    if len(matches) != 1:
        raise ValueError(f"Exactly one reviewed manifest expected for {source_id}, got {len(matches)}")
    info = json.loads(matches[0].read_text(encoding="utf-8"))
    if info.get("dataset_id") != source_id or info.get("status") != "raw_unvalidated":
        raise ValueError(f"Unrecognized raw source: {source_id}")
    path = (root / info["filename"]).resolve(strict=True)
    if root.resolve() not in path.parents:
        raise ValueError("Raw source escapes data root")
    if sha256_file(path) != info.get("sha256"):
        raise ValueError(f"SHA-256 mismatch for {source_id}")
    if info.get("geography_year") != GEO_YEAR:
        raise ValueError(f"Incorrect geography vintage in {source_id}")
    return path, info

def reference_codes(xlsx_zip: Path) -> set[str]:
    with zipfile.ZipFile(xlsx_zip) as archive:
        names = [x for x in archive.namelist() if x.endswith(".xlsx")]
        if len(names) != 1:
            raise ValueError("IRIS reference has unexpected files")
        workbook = openpyxl.load_workbook(io.BytesIO(archive.read(names[0])), read_only=True, data_only=True)
    sheet = workbook["Emboitements_IRIS"]
    # INSEE workbook has inaccurate worksheet dimension metadata (A1); reset it.
    sheet.reset_dimensions()
    found = []
    for row in sheet.values:
        code = row[0] if row else None
        if isinstance(code, str) and re.fullmatch(r"751(?:0[1-9]|1\d|20)\d{4}",code):
            found.append(code)
    workbook.close()
    if len(found) != len(set(found)) or not found:
        raise ValueError("Empty or duplicate Paris IRIS official reference")
    return set(found)

def prepare_geometry(raw):
    """IGN GeoParquet stores WGS84 multipolygons as arrays of x/y structs."""
    if not isinstance(raw,list) or not raw:
        raise ValueError("Missing multipolygon geometry")
    try:
        polygons = [
            [[[float(vertex["x"]), float(vertex["y"])] for vertex in ring]
             for ring in polygon]
            for polygon in raw
        ]
    except (KeyError,TypeError,ValueError,IndexError) as exc:
        raise ValueError("Malformed IGN geometry") from exc
    for poly in polygons:
        if not poly:raise ValueError("Empty polygon")
        for ring in poly:
            if len(ring)<4 or ring[0]!=ring[-1] or not all(
                isfinite(v) for point in ring for v in point):
                raise ValueError("Invalid/unclosed ring")
    geo={"type":"MultiPolygon","coordinates":polygons}
    polygon=shape(geo)
    if not polygon.is_valid or polygon.is_empty or polygon.area<=0:
        raise ValueError("Topologically invalid IGN multipolygon")
    if polygon.bounds[0]<2.19 or polygon.bounds[2]>2.50 or polygon.bounds[1]<48.78 or polygon.bounds[3]>48.93:
        raise ValueError("Coordinates outside broad Paris bounds")
    return geo

def extract_stats(conn, path: Path) -> dict[str,dict]:
    rows=conn.execute("""
        SELECT GEO, OCS, OBS_VALUE, OBS_STATUS
        FROM read_parquet(?)
        WHERE GEO_OBJECT='IRIS' AND LEFT(GEO,3)='751'
        AND TIME_PERIOD=DATE '2023-01-01' AND FREQ='A'
        AND RP_MEASURE='DWELLINGS' AND OCS IN ('_T','DW_VAC')
        AND TDW='_T' AND L_STAY='_T' AND NRG_SRC='_T'
        AND CARPARK='_T' AND NOR='_T' AND TSH='_T'
        AND CARS='_T' AND BUILD_END='_T' AND UFS='_T'
    """,[str(path)]).fetchall()
    result={}
    for code,category,value,status in rows:
        if not isinstance(code,str) or not re.fullmatch(r"751(?:0[1-9]|1\d|20)\d{4}",code):
            raise ValueError("Unexpected Paris IRIS code")
        if status!="A" or value is None or not isfinite(value) or value<0:
            raise ValueError("Unusable RP2023 observation")
        cell=result.setdefault(code,{})
        if category in cell:raise ValueError("Duplicate RP2023 category for "+code)
        cell[category]=float(value)
    for code,p in result.items():
        if set(p)!=set(CATEGORIES) or p["DW_VAC"]>p["_T"]:
            raise ValueError("Missing categories or vacants exceed housing: "+code)
    total=sum(x["_T"] for x in result.values())
    vacant=sum(x["DW_VAC"] for x in result.values())
    if abs(total-EXPECTED_TOTAL)>1 or abs(vacant-EXPECTED_VACANT)>1:
        raise ValueError(f"Paris aggregates differ from official reference: {total}, {vacant}")
    return result

def prepare(root:Path):
    originals=dict((key,read_original(root,key)) for key in SOURCE_IDS)
    reference=reference_codes(originals["iris-ref2025"][0])
    conn=duckdb.connect(database=":memory:")
    stats=extract_stats(conn, originals["rp2023"][0])
    georows=conn.execute("""
        SELECT code_iris, geometrie FROM read_parquet(?)
        WHERE LEFT(code_iris,3)='751' ORDER BY code_iris
    """,[str(originals["contours-iris-2025"][0])]).fetchall()
    if len(georows)!=len(reference) or len(stats)!=len(reference):
        raise ValueError("Count mismatch between three independent official sources")
    if set(stats)!=reference or set(code for code,_ in georows)!=reference:
        raise ValueError("IRIS code mismatch across Insee census, reference and IGN geometry")
    if len(set(code for code,_ in georows))!=len(georows):
        raise ValueError("Duplicate IGN geometric unit")
    features=[]
    for code,geom in georows:
        features.append({
            "type":"Feature",
            "id":code,
            "geometry":prepare_geometry(geom),
            "properties":{
                "iris_code":code,
                "housing_count":stats[code]["_T"],
                "vacant_count":stats[code]["DW_VAC"]
            }
        })
    stat_info=originals["rp2023"][1]
    ref_info=originals["iris-ref2025"][1]
    geo_info=originals["contours-iris-2025"][1]
    manifest={
        "census_year": RP_YEAR,
        "geography_year": GEO_YEAR,
        "zone":"Paris",
        "geography":"IRIS",
        "metric":"vacant_housing_rp",
        "extracted_at":datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "expected_iris_count":len(reference),
        "statistics":{"url":stat_info["response_url"],"sha256":stat_info["sha256"],"licence":"Licence Ouverte 2.0"},
        "contours":{"url":geo_info["response_url"],"sha256":geo_info["sha256"],"licence":"Licence Ouverte 2.0"},
        "independent_reference":{"url":ref_info["response_url"],"sha256":ref_info["sha256"],"iris_count":len(reference)},
        "method":"Insee RP2023 exploitation principale, OCS=_T and DW_VAC, TDW and other dimensions _T; IGN 2025 WGS84; strict 1:1 iris code; GEOS valid.",
        "quality":{"matched_iris":len(reference),"missing_codes":0,"invalid_geometries":0,
                    "housing_total":sum(p["_T"] for p in stats.values()),
                    "vacant_total":sum(p["DW_VAC"] for p in stats.values()),
                    "checked_against_insee_city_totals":True},
        "limitations":"Recensement estimates; no vacant apartment/building can be located; 2023 only."
    }
    return {"type":"FeatureCollection","features":features},manifest

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root",type=Path,default=Path("/srv/vacant/data"))
    parser.add_argument("--output-dir",type=Path,default=Path("/srv/vacant/data/processed/iris-2023"))
    parser.add_argument("--execute",action="store_true")
    args=parser.parse_args(argv)
    try:
        collection,manifest=prepare(args.root)
        print("VALIDATED",json.dumps(manifest["quality"],ensure_ascii=False))
        if not args.execute:
            print("PREVIEW ONLY: add --execute to write prepared GeoJSON and manifest.")
            return 0
        if args.output_dir.exists():
            raise FileExistsError("Output directory already exists: immutable result")
        args.output_dir.mkdir(parents=True,mode=0o700)
        try:
            (args.output_dir/"prepared-iris-2023.geojson").write_text(json.dumps(collection,separators=(",",":"),ensure_ascii=False)+"\n",encoding="utf-8")
            (args.output_dir/"manifest.json").write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
        except Exception:
            for name in ("prepared-iris-2023.geojson","manifest.json"):
                (args.output_dir/name).unlink(missing_ok=True)
            args.output_dir.rmdir()
            raise
        print("PREPARED",args.output_dir)
        return 0
    except (OSError,ValueError,KeyError) as e:
        print("IRIS_2023_REJECTED",type(e).__name__,str(e)[:400])
        return 1

if __name__=="__main__":
    raise SystemExit(main())
