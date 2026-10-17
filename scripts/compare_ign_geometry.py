#!/usr/bin/env python3
"""Compare two VERIFIED historic Paris BD TOPO editions, privately.

This measures mapping consistency, NOT construction, demolition, or vacancy.
Outputs aggregate statistics only; no feature IDs/individual polygons.
"""
from __future__ import annotations
import argparse
from hashlib import blake2b
import json
from pathlib import Path
import statistics
import struct

import shapefile
from shapely.geometry import shape
from audit_ign_historic_snapshots import EDITIONS, TYPES, verify_source, validate_footprints

YEARS=("2011-04-12","2018-03-29")

def vertex_fingerprint(feature):
    h=blake2b(digest_size=16)
    h.update(struct.pack("<I",feature.shapeType))
    for part in feature.parts:h.update(struct.pack("<I",part))
    for x,y in feature.points:h.update(struct.pack("<dd",x,y))
    return h.digest()

def compare_metadata(a,b):
    """Never infer a building event from a document's features."""
    common=a.keys() & b.keys()
    changed=[fid for fid in common if a[fid][0]!=b[fid][0]]
    return {
        "edition_2011":len(a),"edition_2018":len(b),"shared_ids":len(common),
        "only_in_2011_reference":len(a)-len(common),
        "only_in_2018_reference":len(b)-len(common),
        "exact_same_vertex_lists":len(common)-len(changed),
        "different_vertex_lists":len(changed),
        "changed_feature_class":sum(a[fid][1]!=b[fid][1] for fid in common),
        "changed_height_attribute":sum(a[fid][2]!=b[fid][2] for fid in common)
    }, changed

def edition_rows(folder:Path):
    rows={};readers={}
    for kind in TYPES:
        files=list(folder.rglob("BATI_"+kind+".SHP"))
        if len(files)!=1:raise ValueError("Missing or duplicated audited SHP")
        reader=shapefile.Reader(str(files[0]),encoding="utf8")
        readers[kind]=reader
        names=[x[0] for x in reader.fields[1:]]
        h_index=names.index("HAUTEUR")
        for i,feature in enumerate(reader.iterShapeRecords()):
            fid=feature.record[0]
            if fid in rows:raise ValueError("Duplicate ID across classes")
            rows[fid]=(vertex_fingerprint(feature.shape),kind,feature.record[h_index],i)
    return rows,readers

def overlap_iou(shape2011,shape2018):
    a=shape(shape2011.__geo_interface__)
    b=shape(shape2018.__geo_interface__)
    if a.is_empty or b.is_empty or not a.is_valid or not b.is_valid:
        raise ValueError("Invalid geometry in spatial comparison")
    total=a.union(b).area
    if total<=0:raise ValueError("Empty union")
    result=a.intersection(b).area/total
    if result<0 or result>1.0000001:raise ValueError("Invalid overlap ratio")
    return min(1.,result)

def compare(archive_dir:Path,unpacked_dir:Path):
    # Independent source and SHP schema checks, not just a cached report.
    for year in YEARS:
        verify_source(archive_dir/EDITIONS[year]["filename"],EDITIONS[year])
        validate_footprints(year,unpacked_dir/year)
    a,r1=edition_rows(unpacked_dir/YEARS[0])
    b,r2=edition_rows(unpacked_dir/YEARS[1])
    try:
        summary,changed=compare_metadata(a,b)
        if summary["shared_ids"]<110000 or len(changed)>5000:
            raise ValueError("Unexpected coverage or mutation rate: audit suspended")
        ratios=[]
        for fid in changed:
            left,right=a[fid],b[fid]
            ratios.append(overlap_iou(r1[left[1]].shape(left[3]),r2[right[1]].shape(right[3])))
        summary["changed_geometry_overlap"]={
            "count":len(ratios),
            "minimum":round(min(ratios),6) if ratios else None,
            "median":round(statistics.median(ratios),6) if ratios else None,
            "maximum":round(max(ratios),6) if ratios else None,
            "iou_at_least_0_99":sum(x>=.99 for x in ratios),
            "iou_below_0_50":sum(x<.5 for x in ratios)
        }
        summary["method"]={
            "geometry_fingerprint":"BLAKE2b(ShapeType + exact Lambert-93 part indexes and XY doubles)",
            "overlap":"GEOS area(intersection) / area(union), only for shared IDs with nonidentical vertices",
            "unit":"IGN building reference features, NOT physical building events",
            "limitations":"ID changes, class changes and topology updates are not proof of new/demolished buildings; no vacancy data"
        }
        summary["sources"]={year:{
            "sha256":EDITIONS[year]["sha256"],
            "mirror_url":EDITIONS[year]["url"],
            "metadata_extraction":EDITIONS[year]["metadata_extraction"]
        } for year in YEARS}
        return summary
    finally:
        for reader in (*r1.values(),*r2.values()):reader.close()

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--archive-dir",required=True,type=Path)
    p.add_argument("--unpacked-dir",required=True,type=Path)
    p.add_argument("--output",required=True,type=Path)
    args=p.parse_args()
    target=args.output
    if not target.is_absolute() or target.exists() or target.is_symlink() or \
       "processed" not in target.parts or not target.parent.is_dir():
        raise SystemExit("Must use a NEW absolute private processed output path")
    result=compare(args.archive_dir,args.unpacked_dir)
    with target.open("x",encoding="utf8") as f:
        json.dump(result,f,indent=2,ensure_ascii=False);f.write("\n")
    target.chmod(0o600)
    print(json.dumps(result,indent=2,ensure_ascii=False))

if __name__=="__main__":
    main()
