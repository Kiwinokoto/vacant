#!/usr/bin/env python3
"""Build independently audited Paris arrondissement vacancy series, 2006-2023.

Historical IRIS boundaries change. Aggregate the vintage IRIS estimates to stable
Paris arrondissements; DO NOT assign historic estimates to 2025 IRIS polygons.
Geometry for arrondissement display is a union of official IGN 2025 IRIS.
"""
import argparse
import hashlib
import io
import json
import math
from collections import defaultdict
from pathlib import Path
from zipfile import ZipFile

SOURCE = {
    2006: ("rp2006/BTX_IC_LOG_2006.xls", "20d81952ac0e8032bbd9ab38e5d8d1b86c708fb6090ce3809cd7a44566f2ee88", 2008, "https://www.insee.fr/fr/statistiques/fichier/2028562/BTX_IC_LOG_2006.xls"),
    2011: ("rp2011/infra-logement-2011.zip", "c05249a8512e0f237347b889fdc6462e471ab189ebb1a09549a8be67bfa35e50", 2013, "https://www.insee.fr/fr/statistiques/fichier/2028269/infra-logement-2011.zip"),
    2016: ("rp2016/base-ic-logement-2016.zip", "ca1f44bac285f7cebbb1a223d821877381e123db80e0bc1269848348f6dda40c", 2018, "https://www.insee.fr/fr/statistiques/fichier/4228432/base-ic-logement-2016.zip"),
}
EXPECTED = {2006: (1334814, 122667), 2011: (1356074, 98698), 2016: (1374377, 114306), 2023: (1402024, 139075)}
GEOMETRY_SHA = "0b79e30afb5055448d4561960f55db3cc92a84feb2a498adb2588c00b6499a6f"
ARRONDS = {f"751{i:02}": i for i in range(1, 21)}


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def assert_stat(code, housing, vacant, primary=None, secondary=None):
    if not (isinstance(code, str) and len(code) == 9 and code[:5] in ARRONDS and code.isdigit()):
        raise ValueError(f"Not a Paris IRIS code: {code!r}")
    if not all(isinstance(n, (int, float)) and not isinstance(n, bool) and math.isfinite(n) and n >= 0 for n in (housing, vacant)):
        raise ValueError(f"Non-finite/negative census observation: {code}")
    if vacant > housing + 1e-6:
        raise ValueError(f"Vacants exceed dwellings: {code}")
    if primary is not None or secondary is not None:
        if not all(isinstance(n, (float, int)) and math.isfinite(n) and n >= 0 for n in (primary, secondary)):
            raise ValueError(f"Missing housing category: {code}")
        if abs(housing - (vacant + primary + secondary)) > 0.02:
            raise ValueError(f"Nonreconciling dwelling categories: {code}")


def totals_check(year, rows):
    if len(rows) != 992 or len({r[0] for r in rows}) != 992:
        raise ValueError(f"Unexpected IRIS cardinality/duplicates in {year}: {len(rows)}")
    if set(code[:5] for code, _, _ in rows) != set(ARRONDS):
        raise ValueError(f"Missing arrondissement in {year}")
    got_h = sum(h for _, h, _ in rows)
    got_v = sum(v for _, _, v in rows)
    exp_h, exp_v = EXPECTED[year]
    if abs(got_h - exp_h) > 1.1 or abs(got_v - exp_v) > 1.1:
        raise ValueError(f"Paris totals do not match published Insee {year}: {(got_h, got_v)}")
    return got_h, got_v


def read_legacy_year(year, path):
    import xlrd
    spec = SOURCE[year]
    if sha256(path) != spec[1]:
        raise ValueError(f"Source checksum changed: {path}")
    if path.suffix == ".zip":
        with ZipFile(path) as archive:
            items = [e for e in archive.infolist() if not e.is_dir()]
            if len(items) != 1 or items[0].file_size > 200_000_000 or not items[0].filename.endswith(".xls"):
                raise ValueError("Unexpected ZIP contents")
            data = archive.read(items[0])
    else:
        data = path.read_bytes()
    sheet = xlrd.open_workbook(file_contents=data, on_demand=True).sheet_by_name("IRIS")
    if str(spec[2]) not in str(sheet.cell_value(2, 0)):
        raise ValueError(f"Wrong geography for {year}")
    headers = [sheet.cell_value(5, c) for c in range(sheet.ncols)]
    prefix = f"P{str(year)[-2:]}"
    keys = ["IRIS", prefix + "_LOG", prefix + "_LOGVAC", prefix + "_RP", prefix + "_RSECOCC"]
    if any(headers.count(k) != 1 for k in keys):
        raise ValueError(f"Missing or duplicated source fields for {year}")
    cols = [headers.index(k) for k in keys]
    rows = []
    for i in range(6, sheet.nrows):
        code = str(sheet.cell_value(i, cols[0]))
        if not code.startswith("751"):
            continue
        h, v, p, s = (sheet.cell_value(i, c) for c in cols[1:])
        assert_stat(code, h, v, p, s)
        rows.append((code, h, v))
    totals_check(year, rows)
    return rows


def read_2023(geojson):
    if sha256(geojson) != GEOMETRY_SHA:
        raise ValueError("2023 geometry checksum changed")
    payload = json.loads(geojson.read_text(encoding="utf-8"))
    meta = payload.get("metadata", {})
    if meta.get("census_year") != 2023 or meta.get("geography_year") != 2025:
        raise ValueError("Unexpected 2023 geography/census year")
    rows = []
    geoms = defaultdict(list)
    from shapely.geometry import shape
    for f in payload["features"]:
        p = f["properties"]
        code, h, v = p["iris_code"], p["housing_count"], p["vacant_count"]
        assert_stat(code, h, v)
        rows.append((code, h, v))
        geom = shape(f["geometry"])
        if geom.is_empty or not geom.is_valid:
            raise ValueError(f"Invalid source geometry: {code}")
        geoms[code[:5]].append(geom)
    totals_check(2023, rows)
    return rows, geoms


def build(raw_root, geojson):
    from shapely.geometry import mapping
    from shapely.ops import unary_union
    series, geoms = {}, None
    for year, (name, _, _, _) in SOURCE.items():
        series[year] = read_legacy_year(year, raw_root / name)
    series[2023], geoms = read_2023(geojson)
    aggregates = {code: {} for code in ARRONDS}
    for year, rows in series.items():
        buckets = defaultdict(lambda: [0.0, 0.0])
        for code, h, v in rows:
            bucket = buckets[code[:5]]
            bucket[0] += h
            bucket[1] += v
        for code, (h, v) in buckets.items():
            aggregates[code][str(year)] = {
                "housing_count": round(h, 3),
                "vacant_count": round(v, 3),
                "vacancy_percent": round(100 * v / h, 1) if h >= 50 else None,
            }
    features = []
    for code, i in ARRONDS.items():
        g = unary_union(geoms[code])
        if g.is_empty or not g.is_valid:
            raise ValueError(f"Invalid dissolved arrondissement geometry: {code}")
        features.append({
            "type": "Feature", "id": code, "geometry": mapping(g),
            "properties": {"arrondissement_code": code, "arrondissement": i, "series": aggregates[code]},
        })
    return {
        "type": "FeatureCollection", "features": features,
        "metadata": {
            "kind": "vacant_housing_arrondissement_estimate",
            "years": [2006, 2011, 2016, 2023],
            "geography_years": {"2006": 2008, "2011": 2013, "2016": 2018, "2023": 2025},
            "geometry": "2025 arrondissement display boundary formed by union of IGN 2025 IRIS; NO historical IRIS boundary reconstruction",
            "statistical_method": "Sum all 992 vintage Insee IRIS estimated dwelling and vacancy counts by 20 stable municipal arrondissement codes, never map old IRIS counts to 2025 polygons",
            "source_files": {str(y): {"url": s[3], "sha256": s[1], "extracted_at": "2026-10-16", "geography_year": s[2]} for y, s in SOURCE.items()},
            "geometry_2023_sha256": GEOMETRY_SHA,
            "licence": "Licence Ouverte 2.0",
            "limitations": "Insee census estimates, not individual buildings. Arrondissement rates are geographic aggregates; do not infer vacancies at any address.",
        },
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw-root", type=Path, required=True)
    ap.add_argument("--iris-geojson", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    if args.output.exists():
        ap.error("refusing to overwrite existing output")
    obj = build(args.raw_root, args.iris_geojson)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    print(f"BUILT {args.output}: {len(obj['features'])} arrondissements, years={obj['metadata']['years']}, sha256={sha256(args.output)}")


if __name__ == "__main__":
    main()
