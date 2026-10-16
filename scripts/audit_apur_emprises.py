#!/usr/bin/env python3
"""Read-only, aggregate-only audit of the Apur Paris built-footprint service.

No individual features, geometry, addresses, building identifiers or complete
datasets are requested or stored. Not a publication-ready map data builder.
"""
import argparse
from datetime import datetime, timezone
import json
from urllib.parse import urlencode
from urllib.request import Request, urlopen

BASE = "https://carto2.apur.org/apur/rest/services/OPENDATA/EMPRISE_BATIE_PARIS/MapServer"
LAYER_URL = BASE + "/0"
REQUIRED_FIELDS = frozenset({
    "OBJECTID", "n_sq_eb", "an_const", "c_perconst",
    "h_med", "h_moy", "h_min", "h_max",
})
COUNT_WHERE = {
    "total": "1=1",
    "median_height_null": "h_med IS NULL",
    "median_height_zero": "h_med = 0",
    "median_height_negative": "h_med < 0",
    "median_height_over_200": "h_med > 200",
    "year_of_construction_null": "an_const IS NULL",
    "period_of_construction_null": "c_perconst IS NULL",
    "period_undated": "c_perconst = 99",
}
PERIOD_STAT = json.dumps(
    [{"statisticType":"count","onStatisticField":"OBJECTID","outStatisticFieldName":"n"}],
    separators=(",", ":"),
)
HEIGHT_STATS = json.dumps([
    {"statisticType":"min","onStatisticField":"h_med","outStatisticFieldName":"min_h_med"},
    {"statisticType":"max","onStatisticField":"h_med","outStatisticFieldName":"max_h_med"},
], separators=(",", ":"))


def fetch_json(url, params=None):
    if not url.startswith(BASE):
        raise ValueError("Unapproved endpoint")
    target = url + ("?" + urlencode(params) if params else "?f=json")
    with urlopen(Request(target, headers={"User-Agent": "VACANT-readonly-public-aggregate-audit/1.0"}),
                 timeout=25) as response:
        if response.status != 200:
            raise ValueError("External service non-200")
        data = response.read(450_000)
    result = json.loads(data)
    if not isinstance(result, dict) or "error" in result:
        raise ValueError("Invalid ArcGIS service response")
    return result


def validate_layer(layer):
    names = {f.get("name") for f in layer.get("fields", [])}
    if not REQUIRED_FIELDS.issubset(names):
        raise ValueError("Apur attribute schema changed")
    if layer.get("geometryType") != "esriGeometryPolygon":
        raise ValueError("Unexpected geometry type")
    if layer.get("extent", {}).get("spatialReference", {}).get("latestWkid") != 2154:
        raise ValueError("Expected EPSG:2154")
    if "Query" not in layer.get("capabilities", "") or not layer.get("advancedQueryCapabilities", {}).get("supportsStatistics", False):
        raise ValueError("Aggregate statistics not available")
    return True


def validate_counts(counts, categories, height):
    total = counts.get("total")
    if type(total) is not int or total < 1:
        raise ValueError("Invalid Apur total")
    for name, value in counts.items():
        if type(value) is not int or value < 0 or value > total:
            raise ValueError("Invalid count: " + name)
    if counts["median_height_null"] + counts["median_height_zero"] > total:
        raise ValueError("Impossible height missing/zero counts")
    if counts["period_of_construction_null"] + counts["period_undated"] > total:
        raise ValueError("Impossible period missing/undated counts")
    if not isinstance(categories, dict) or sum(categories.values()) != total:
        raise ValueError("Construction period group counts mismatch")
    if categories.get(None) != counts["period_of_construction_null"] or categories.get(99) != counts["period_undated"]:
        raise ValueError("Construction period categories inconsistent")
    if any(type(n) is not int or n < 0 for n in categories.values()):
        raise ValueError("Invalid category frequency")
    if not all(isinstance(height.get(k), (int,float)) for k in ("min_h_med","max_h_med")):
        raise ValueError("Missing height bounds")
    if height["min_h_med"] < 0 or height["max_h_med"] < height["min_h_med"]:
        raise ValueError("Impossible height distribution")
    return True


def audit(query=fetch_json):
    layer = query(LAYER_URL, {"f":"json"})
    validate_layer(layer)
    endpoint = LAYER_URL + "/query"
    counts = {}
    for name, where in COUNT_WHERE.items():
        payload = query(endpoint, {"f":"json","where":where,"returnCountOnly":"true"})
        counts[name] = payload.get("count")
    series = query(endpoint, {
        "f":"json", "where":"1=1", "outStatistics":PERIOD_STAT,
        "groupByFieldsForStatistics":"c_perconst", "returnGeometry":"false", "orderByFields":"c_perconst",
    })
    categories = {}
    for row in series.get("features", []):
        p = row.get("attributes", {})
        code, count = p.get("c_perconst"), p.get("n")
        if code in categories:
            raise ValueError("Duplicate period code")
        categories[code] = count
    bounds = query(endpoint, {
        "f":"json", "where":"1=1", "outStatistics":HEIGHT_STATS, "returnGeometry":"false"
    })
    if len(bounds.get("features",[])) != 1:
        raise ValueError("Unexpected height statistic result")
    height = bounds["features"][0]["attributes"]
    validate_counts(counts, categories, height)
    total = counts["total"]
    return {
        "status": "schema_and_aggregate_audit_only_not_released_as_layer",
        "observed_at_utc": datetime.now(timezone.utc).isoformat(),
        "source": LAYER_URL,
        "reported_layer_name": layer["name"],
        "crs": "EPSG:2154",
        "objects": total,
        "counts": counts,
        "height_median_m": {"minimum":height["min_h_med"],"maximum":height["max_h_med"]},
        "period_counts": {str(k):v for k,v in sorted(categories.items(),key=lambda x:(x[0] is not None, x[0] if x[0] is not None else -1))},
        "eligible_positive_median_height_count": total - counts["median_height_null"] - counts["median_height_zero"],
        "dated_period_count": total - counts["period_of_construction_null"] - counts["period_undated"],
        "warnings": [
            "Apur emprise may represent one or several buildings, not a dwelling or an address-level vacancy observation",
            "h_med is median building footprint height in metres; do not confuse with Paris Data H_ET_MAX storeys",
            "an_const (year) and c_perconst (period) have different coverage; do not infer precise year from a period",
            "Layer schema provides no independently validated per-object accuracy or current update vintage",
            "ODbL attribution and redistribution conditions require review before publishing modified spatial database",
            "No geometry or object-level dataset was retrieved in this audit",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true",
                        help="Send a bounded series of read-only aggregate/statistics requests")
    args = parser.parse_args()
    if not args.live:
        print("Preview only. Use --live for read-only Apur metadata and aggregate counts.")
        return
    print(json.dumps(audit(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
