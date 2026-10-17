"""Audit June 2026 public LOVAC CSV: twenty Paris arrondissements, no dwelling records.

Offline, source-pinned, and refusal on suppression ('s') or mismatched departments.
"""
import argparse,csv,hashlib,io,json,re
from pathlib import Path

CHECKS={
 "lovac-opendata-communes26.csv":"b856568d4b69784d32f9fafaf7e1376047e45eed245fb114dd737d2d43826245",
 "lovac-opendata-departements26.csv":"b6c3d2304dd4d35d07f6153720874650ea1f55583ffe58e459632b2f3e01a2ff",
 "lovac-opendata-metadonnees26.csv":"d8698c32631201ab295268aa2e8679cd715abcc7c3550379c53c41076174bd81"
}
COLS={y:{"vacant":f"pp_vacant_{y%100:02d}",
 "long":f"pp_vacant_plus_2ans_{y%100:02d}",
 "stock":f"ff_pp_total_{y%100:02d}" if y<2026 else None}
 for y in range(2020,2027)}
DATES=re.compile(r"au (0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[012])/(20\d\d)")
CODES=[f"751{i:02d}" for i in range(1,21)]
def source(path):
 if path.name not in CHECKS or path.is_symlink():raise ValueError("Unexpected source")
 raw=path.read_bytes()
 if hashlib.sha256(raw).hexdigest()!=CHECKS[path.name]:raise ValueError("Source SHA256 mismatch")
 return raw.decode("cp1252")
def rows(text):
 return list(csv.DictReader(io.StringIO(text),delimiter=";"))
def number(v):
 if not isinstance(v,str) or not re.fullmatch(r"\d+",v):
  raise ValueError("Missing, suppressed, or invalid public aggregate")
 return int(v)
def dates(dictionary):
 content=list(csv.reader(io.StringIO(dictionary),delimiter=";"))
 needed={col for v in COLS.values() for col in v.values() if col}
 found={}
 for row in content:
  if row and row[0] in needed:
   m=DATES.search(row[1])
   if not m:raise ValueError("Missing official reference date "+row[0])
   found[row[0]]=f"{m[3]}-{m[2]}-{m[1]}"
 if set(found)!=needed or found["pp_vacant_26"]!="2025-01-01" or found["pp_vacant_plus_2ans_23"]!="2022-01-01":
  raise ValueError("Unexpected dictionary year mapping")
 return found
def build(commune,department,dictionary):
 ds=dates(dictionary)
 paris=[r for r in rows(commune) if r.get("CODGEO_26") in CODES]
 if sorted(r["CODGEO_26"] for r in paris)!=CODES or len(paris)!=20:
  raise ValueError("Missing/duplicate arrondissement")
 if any(r.get("DEP")!="75" or not r.get("LIBGEO_26","").startswith("Paris ") for r in paris):
  raise ValueError("Wrong geography")
 dept=[{k.strip():v.strip() for k,v in r.items()} for r in rows(department)]
 dept=[r for r in dept if r.get("DEP")=="75"]
 if len(dept)!=1:raise ValueError("Department check absent")
 out=[];aggregate={}
 for y,cols in COLS.items():
  total={}
  for kind,col in cols.items():
   if col is None:continue
   val=sum(number(r[col]) for r in paris)
   if val!=number(dept[0][col].replace("\u00a0","").replace(" ","")):
    raise ValueError("Paris district/department mismatch")
   total[kind]=val
  if total["long"]>total["vacant"]:raise ValueError("Invalid long-term count")
  aggregate[y]=total
 for r in sorted(paris,key=lambda x:x["CODGEO_26"]):
  series={str(y):{kind:number(r[col]) for kind,col in cols.items() if col}
    for y,cols in COLS.items()}
  if any(s["long"]>s["vacant"] for s in series.values()):raise ValueError("Invalid arrondissement data")
  out.append({"arrondissement":int(r["CODGEO_26"][-2:]),"code":r["CODGEO_26"],"series":series})
 return {"kind":"lovac_public_private_housing_aggregates","license":"Licence Ouverte 2.0",
  "source":"https://www.data.gouv.fr/datasets/61816c6e23197bb34835228e",
  "source_sha256":CHECKS,"years":[{"production_year":y,
   "date_by_variable":{k:ds[v] for k,v in cols.items() if v},
   "phase":"legacy" if y<2024 else "GMBI-transition" if y==2024 else
           "GMBI-declarations" if y==2025 else "GMBI-stabilizing",
   "paris":aggregate[y]} for y,cols in COLS.items()],
  "arrondissements":out,
  "warnings":["GMBI rupture 2024–2025; not a homogeneous time series",
   "Insee RP counts all housing; LOVAC covers fiscal private housing only",
   "Production year differs from observation date",
   "No denominator 2026 provided; do not calculate a 2026 vacancy rate",
   "LOVAC 2023 long-term count has a different reference date than all-vacant count"]}
def main():
 p=argparse.ArgumentParser()
 p.add_argument("--input-dir",required=True,type=Path)
 p.add_argument("--output",required=True,type=Path)
 a=p.parse_args()
 if not a.output.is_absolute() or a.output.exists() or a.output.is_symlink():
  raise SystemExit("Refusing destination")
 paths={k:source(a.input_dir/k) for k in CHECKS}
 result=build(paths["lovac-opendata-communes26.csv"],paths["lovac-opendata-departements26.csv"],
  paths["lovac-opendata-metadonnees26.csv"])
 with a.output.open("x",encoding="utf8") as f:json.dump(result,f,ensure_ascii=False,indent=2);f.write("\n")
 a.output.chmod(0o600)
 print(json.dumps({"output":str(a.output),"Paris":[{"year":x["production_year"],**x["paris"]} for x in result["years"]]},ensure_ascii=False))
if __name__=="__main__":main()
