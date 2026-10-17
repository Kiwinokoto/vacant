#!/usr/bin/env python3
"""Audit frozen historical IGN BD TOPO building editions, without public export.

Requires pyshp. 7z extraction happens separately in a guarded PRIVATE folder.
Do not infer that non-matching IDs represent construction/demolition.
"""
from __future__ import annotations
import argparse
from datetime import datetime,timezone
from hashlib import sha256
import json
from pathlib import Path
import shapefile
import zlib

EDITIONS = {
 "2008-09-14": {
  "filename": "BDTOPO_2-0_TOUSTHEMES_SHP_LAMB93_D075_2008-09-14.7z",
  "size": 8547169,
  "sha256": "64f4588c9ec8dbcce2c72ec7e7e24a142477996910fde80f24e81e2b13252d65",
  "url": "https://data.cquest.org/ign/bdtopo/BDTOPO_2-0_2008-09/BDTOPO_2-0_TOUSTHEMES_SHP_LAMB93_D075_2008-09-14.7z",
  "metadata_extraction": "2019-05-23",
 },
 "2011-04-12": {
  "filename": "BDTOPO_2-0_TOUSTHEMES_SHP_LAMB93_D075_2011-04-12.7z",
  "size": 15647070,
  "sha256": "5926330d42fd290b1008f266b5082a95e73c765ec06027fcc45b7721ea00a3ad",
  "url": "https://data.cquest.org/ign/bdtopo/BDTOPO_2-0_2011-04/BDTOPO_2-0_TOUSTHEMES_SHP_LAMB93_D075_2011-04-12.7z",
  "metadata_extraction": "2021-10-05",
 },
 "2018-03-29": {
  "filename": "BDTOPO_2-2_TOUSTHEMES_SHP_LAMB93_D075_2018-03-29.7z",
  "size": 15442618,
  "sha256": "0bf421c0e7092c8dfe343e6506ec605c92d88a1f78d19a0b075bafca641d88b9",
  "url": "https://data.cquest.org/ign/bdtopo/BDTOPO_2-2_2018-03-29/BDTOPO_2-2_TOUSTHEMES_SHP_LAMB93_D075_2018-03-29.7z",
  "metadata_extraction": "2018-04-14",
 },
}
TYPES=("INDIFFERENCIE","INDUSTRIEL","REMARQUABLE")
PARIS_L93_LIMITS=(640000,6850000,665000,6875000)

def digest(path):
 h=sha256()
 with path.open("rb") as inp:
  for data in iter(lambda:inp.read(1024*1024),b""):h.update(data)
 return h.hexdigest()

def verify_source(path,metadata):
 if path.is_symlink() or not path.is_file() or path.stat().st_size!=metadata["size"]:
  raise ValueError("Missing/untrusted original archive")
 if digest(path)!=metadata["sha256"]:
  raise ValueError("Historical archive SHA-256 mismatch")

def validate_footprints(label,folder):
 if not folder.is_dir() or folder.is_symlink():
  raise ValueError("Unpacked edition missing or symlinked")
 xmls=list(folder.rglob("*.xml"))
 if len(xmls)!=1 or xmls[0].is_symlink():
  raise ValueError("Exactly one historic metadata XML required")
 xml=xmls[0].read_text(encoding="utf8")
 for anchor in (label,EDITIONS[label]["metadata_extraction"],"LAMB93","D075"):
  if anchor not in xml:raise ValueError("Historical date / edition metadata mismatch: "+anchor)
 unique=set();counts={};shapes={}
 for kind in TYPES:
  f=list(folder.rglob("BATI_"+kind+".SHP"))
  if len(f)!=1:raise ValueError("One and only one "+kind+" SHP expected")
  shp=f[0]
  if shp.is_symlink():raise ValueError("SHP symlink forbidden")
  for ext in (".DBF",".SHX",".PRJ",".CPG"):
   sibling=shp.with_suffix(ext)
   if not sibling.is_file() or sibling.is_symlink():
    raise ValueError("Missing SHP component "+str(sibling))
  prj=shp.with_suffix(".PRJ").read_text(encoding="utf8",errors="replace")
  if "Lambert" not in prj and "LAMBERT" not in prj:raise ValueError("Unknown CRS")
  reader=shapefile.Reader(str(shp),encoding="utf8")
  fields=[x[0] for x in reader.fields[1:]]
  if fields[0]!="ID" or "HAUTEUR" not in fields or not 0<len(reader)<200000:
   raise ValueError("Unknown historic building schema")
  bounds=reader.bbox
  if (not PARIS_L93_LIMITS[0]<bounds[0]<bounds[2]<PARIS_L93_LIMITS[2] or
      not PARIS_L93_LIMITS[1]<bounds[1]<bounds[3]<PARIS_L93_LIMITS[3]):
   raise ValueError("Outside Paris Lambert93 study envelope")
  ids={r[0] for r in reader.iterRecords()}
  if len(ids)!=len(reader) or any(not str(x).startswith("BATIMENT") for x in ids):
   raise ValueError("Duplicate or invalid building ID in "+kind)
  if unique & ids:raise ValueError("Multiple types with duplicate building ID")
  unique.update(ids)
  counts[kind]=len(ids);shapes[kind]={"bbox_lambert93":[float(x) for x in bounds],"features":len(ids)}
  reader.close()
 return unique,{"counts":counts,"classes":shapes,"total":sum(counts.values()),
                "metadata_label":label,"metadata_extraction":EDITIONS[label]["metadata_extraction"]}

def overlap_stats(a,b):
 common=len(a&b)
 return {"shared_ids":common,"first_fraction":round(common/len(a),5),
         "second_fraction":round(common/len(b),5)}

def sampled_shapes(folder):
 """Stable 1% systematic hash sample for document/version continuity, NOT change detection."""
 result={}
 for kind in TYPES:
  shp=next(folder.rglob("BATI_"+kind+".SHP"))
  reader=shapefile.Reader(str(shp),encoding="utf8")
  names=[x[0] for x in reader.fields[1:]]
  for feat in reader.iterShapeRecords():
   fid=feat.record[0]
   if zlib.crc32(fid.encode("utf8"))%100:continue
   raw=json.dumps([list(feat.shape.parts),list(feat.shape.points)],separators=(",",":"))
   result[fid]=(kind,sha256(raw.encode()).hexdigest(),
                feat.record[names.index("HAUTEUR")])
  reader.close()
 return result

def geometry_sample_stats(a,b):
 shared=a.keys() & b.keys()
 return {
  "sample_selection":"crc32(feature_id) % 100 == 0",
  "sample_a":len(a),"sample_b":len(b),"shared":len(shared),
  "same_exact_vertex_lists":sum(a[k][1]==b[k][1] for k in shared),
  "different_exact_vertex_lists":sum(a[k][1]!=b[k][1] for k in shared),
  "changed_type":sum(a[k][0]!=b[k][0] for k in shared),
  "changed_height_value":sum(a[k][2]!=b[k][2] for k in shared),
  "interpretation":"Non-equal vertices/attributes may be revisions, not construction/demolition",
 }

def build_report(archives:Path,unpacked:Path):
 ids={};report={"dataset":"IGN BD TOPO historic Paris D075 — documentary snapshots",
     "license_reference":"Licence Ouverte v2.0 — verify conditions for each edition",
     "mirror":"data.cquest.org — independent archive mirror, not official server",
     "does_not_prove_building_appearance_or_demolition":True,
     "year_2008_comparability":"blocked: sparse coverage and low stable ID overlap",
     "editions":{},"comparisons":{}}
 for label,metadata in EDITIONS.items():
  verify_source(archives/metadata["filename"],metadata)
  obj,detail=validate_footprints(label,unpacked/label)
  ids[label]=obj
  detail.update({"download_url":metadata["url"],"archive_bytes":metadata["size"],
                 "archive_sha256":metadata["sha256"]})
  report["editions"][label]=detail
 for a,b in (("2008-09-14","2011-04-12"),("2011-04-12","2018-03-29"),
             ("2008-09-14","2018-03-29")):
  report["comparisons"][a+" vs "+b]=overlap_stats(ids[a],ids[b])
 report["2011_2018_sample_1pct"]=geometry_sample_stats(
  sampled_shapes(unpacked/"2011-04-12"),
  sampled_shapes(unpacked/"2018-03-29"))
 if report["comparisons"]["2008-09-14 vs 2011-04-12"]["first_fraction"]>=0.5:
  raise ValueError("2008 compatibility status must be reviewed anew")
 if report["comparisons"]["2011-04-12 vs 2018-03-29"]["first_fraction"]<=0.90:
  raise ValueError("2011↔2018 ID continuity is unexpectedly low")
 return report

def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument("--archive-dir",type=Path,required=True)
 p.add_argument("--unpacked-dir",type=Path,required=True)
 p.add_argument("--output",type=Path,required=True)
 args=p.parse_args()
 dest=args.output
 if not dest.is_absolute() or dest.exists() or dest.is_symlink():
  raise SystemExit("Output must be an unused absolute path")
 if not dest.parent.is_dir() or "processed" not in dest.parts:
  raise SystemExit("Output must be in the controlled processed directory")
 obj=build_report(args.archive_dir,args.unpacked_dir)
 obj["audit_date_utc"]=datetime.now(timezone.utc).isoformat()
 with dest.open("x",encoding="utf8") as out:json.dump(obj,out,ensure_ascii=False,indent=2);out.write("\n")
 dest.chmod(0o600)
 print(json.dumps({k:v["total"] for k,v in obj["editions"].items()},indent=2))
 print(json.dumps(obj["comparisons"],indent=2))
 print("PRIVATE_REPORT_PATH",dest)

if __name__=="__main__":main()
