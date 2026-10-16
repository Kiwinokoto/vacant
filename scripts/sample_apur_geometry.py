#!/usr/bin/env python3
"""Bounded geometry quality audit of public Apur footprints. No geometry persisted."""
import argparse, json
from urllib.parse import urlencode
from urllib.request import Request, urlopen

URL = "https://carto2.apur.org/apur/rest/services/OPENDATA/EMPRISE_BATIE_PARIS/MapServer/0/query"
FIELDS = "OBJECTID,n_sq_eb,h_med,h_moy,h_min,h_max,c_perconst,an_const"
STRATA = (
    ("head", "1=1", 0, 8),
    ("middle_a", "1=1", 40000, 8),
    ("middle_b", "1=1", 80000, 8),
    ("tail", "1=1", 120000, 8),
    ("missing_year", "an_const IS NULL", 0, 8),
    ("undated", "c_perconst = 99", 0, 8),
    ("missing_height", "h_med IS NULL OR h_med = 0", 0, 8),
    ("over_200", "h_med > 200", 0, 10),
)
def params(where, offset, limit):
    if where not in {s[1] for s in STRATA} or offset not in {0,40000,80000,120000} or not 1 <= limit <= 10:
        raise ValueError("Unbounded query refused")
    return dict(f="geojson",where=where,outFields=FIELDS,returnGeometry="true",
                outSR=4326,orderByFields="OBJECTID",resultOffset=offset,resultRecordCount=limit)
def fetch(p):
    req=Request(URL+"?"+urlencode(p),headers={"User-Agent":"VACANT-readonly-bounded-audit/1.0"})
    with urlopen(req,timeout=35) as response: data=response.read(2000001)
    if len(data)>2000000: raise ValueError("Response too large")
    result=json.loads(data)
    if not isinstance(result,dict) or "error" in result: raise ValueError("ArcGIS error")
    return result,len(data)
def inspect(features, projection):
    from shapely.geometry import shape
    from shapely.ops import transform
    if not isinstance(features,list) or len(features)>10: raise ValueError("Unexpected batch size")
    result={"count":len(features),"valid":0,"invalid":0,"inconsistent_h_med":0,"outliers":[]}
    seen=set()
    for feat in features:
        a=feat.get("properties") or {}
        object_id=a.get("OBJECTID")
        if type(object_id) is not int or object_id in seen: raise ValueError("Duplicate/missing OBJECTID")
        seen.add(object_id)
        geom=shape(feat["geometry"]) if feat.get("geometry") else None
        good=bool(geom and geom.is_valid and not geom.is_empty and geom.geom_type in ("Polygon","MultiPolygon"))
        if good:
            w,s,e,n=geom.bounds
            good=2.15<w<e<2.5 and 48.75<s<n<49.0
        area=round(transform(projection,geom).area,1) if good else None
        result["valid" if good else "invalid"]+=1
        med,lo,hi=(a.get(k) for k in ("h_med","h_min","h_max"))
        if isinstance(med,(float,int)) and ((isinstance(lo,(float,int)) and med<lo) or (isinstance(hi,(float,int)) and med>hi)):
            result["inconsistent_h_med"]+=1
        if isinstance(med,(float,int)) and med>200:
            result["outliers"].append({"OBJECTID":object_id,"h_med_m":med,
                "h_min_m":lo,"h_max_m":hi,"h_moy_m":a.get("h_moy"),
                "period":a.get("c_perconst"),"year":a.get("an_const"),
                "area_m2":area,"valid":good})
    return result
def audit():
    from pyproj import Transformer
    projection=Transformer.from_crs(4326,2154,always_xy=True).transform
    count_response,_=fetch({"f":"json","where":"h_med > 200","returnCountOnly":"true"})
    n=count_response.get("count")
    if type(n) is not int or not 0<=n<=10: raise ValueError("Outlier count exceeds cap")
    output={"source":URL,"status":"research_only_not_for_publication","strata":{},"distinct_ids":0}
    seen=set()
    for name,where,offset,limit in STRATA:
        response,size=fetch(params(where,offset,limit))
        if response.get("type")!="FeatureCollection": raise ValueError("Not GeoJSON")
        batch=response.get("features")
        r=inspect(batch,projection)
        if name=="over_200" and len(batch)!=n: raise ValueError("Partial outlier batch")
        ids={f["properties"]["OBJECTID"] for f in batch}
        r["overlap_between_strata"]=len(seen & ids)
        r["response_bytes"]=size
        seen.update(ids)
        output["strata"][name]=r
    output["distinct_ids"]=len(seen)
    return output
if __name__=="__main__":
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--live",action="store_true")
    args=ap.parse_args()
    print(json.dumps(audit(),indent=2) if args.live else "Preview only. Use --live for eight tiny spatial samples.")
