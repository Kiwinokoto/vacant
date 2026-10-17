"""LOVAC-only public aggregate audit unit tests, synthetic data."""
import csv,importlib.util,io
from pathlib import Path
import unittest

modpath=Path(__file__).resolve().parents[1]/"scripts/audit_lovac_open_paris.py"
spec=importlib.util.spec_from_file_location("lovac_open",modpath)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def csvtext(fields,records):
 s=io.StringIO();w=csv.DictWriter(s,fieldnames=fields,delimiter=";")
 w.writeheader();w.writerows(records);return s.getvalue()
def sample():
 fields=["CODGEO_26","LIBGEO_26","DEP"]+[
  name for info in m.COLS.values() for name in info.values() if name]
 fields=list(dict.fromkeys(fields))
 district=[{**{key:"20" if key.startswith("pp_vacant_") else
                       "10" if key.startswith("pp_vacant_plus") else "100"
             for key in fields if key not in ["CODGEO_26","LIBGEO_26","DEP"]},
            "CODGEO_26":code,"LIBGEO_26":f"Paris {i}e Arrondissement","DEP":"75"}
     for i,code in enumerate(m.CODES,1)]
 department={"DEP":"75","LIB_DEP":"Paris"}
 department.update({k:"400" if k.startswith("pp_vacant_") else
      "200" if k.startswith("pp_vacant_plus") else "2\u00a0000"
     for k in fields if k not in ["CODGEO_26","LIBGEO_26","DEP"]})
 # correct ordering: long field starts with 'pp_vacant_plus_', not 'pp_vacant_'
 for row in district:
  for k in row:
   if k.startswith("pp_vacant_plus_"):row[k]="10"
 for k in department:
  if k.startswith("pp_vacant_plus_"):department[k]="200"
 meta=[]
 for y,cs in m.COLS.items():
  for kind,col in cs.items():
   if not col:continue
   obs=2022 if y==2023 and kind=="long" else 2023 if y==2023 else y-1
   meta.append([col,f"Nombre de logements au 01/01/{obs}","LOVAC Cerema"])
 metadata=io.StringIO();csv.writer(metadata,delimiter=";").writerows(meta)
 return csvtext(fields,district),csvtext(list(department),[department]),metadata.getvalue()
class PublicLovacTests(unittest.TestCase):
 def test_twenty_arrondissements_and_department_crosscheck(self):
  src=sample();x=m.build(*src)
  self.assertEqual(len(x["arrondissements"]),20)
  self.assertEqual(x["years"][-1]["date_by_variable"]["vacant"],"2025-01-01")
  self.assertEqual(x["years"][3]["date_by_variable"]["long"],"2022-01-01")
  self.assertNotIn("owner",str(x))
  self.assertEqual(x["years"][0]["paris"]["vacant"],400)
 def test_secreted_value_is_never_zero(self):
  a,b,c=sample()
  a=a.replace(";\"20\"",";\"s\"",1) if ';"20"' in a else a.replace(";20",";s",1)
  with self.assertRaises(ValueError):m.build(a,b,c)
 def test_missing_district_rejected(self):
  a,b,c=sample();a="\n".join(a.splitlines()[:-1])+"\n"
  with self.assertRaisesRegex(ValueError,"arrondissement"):m.build(a,b,c)
 def test_wrong_department_rejected(self):
  a,b,c=sample();b=b.replace("400","401",1)
  with self.assertRaisesRegex(ValueError,"mismatch"):m.build(a,b,c)
 def test_reference_year_guard(self):
  a,b,c=sample();c=c.replace("01/01/2025","01/01/2026")
  with self.assertRaisesRegex(ValueError,"year mapping"):m.build(a,b,c)
 def test_bad_bytes_are_rejected_before_parsing(self):
  import tempfile
  with tempfile.TemporaryDirectory() as tmp:
   p=Path(tmp)/"lovac-opendata-communes26.csv";p.write_text("not the official data")
   with self.assertRaisesRegex(ValueError,"SHA256"):m.source(p)
if __name__=="__main__":unittest.main()
