"""Unit safety tests for historical IGN building edition audit (synthetic only)."""
import importlib.util
from hashlib import sha256
from pathlib import Path
import tempfile
import unittest
import shapefile

SCRIPT=Path(__file__).resolve().parents[1]/"scripts"/"audit_ign_historic_snapshots.py"
spec=importlib.util.spec_from_file_location("ign_historical",SCRIPT)
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
class HistoricAuditTests(unittest.TestCase):
 def test_version_id_overlap_not_demolition(self):
  x=mod.overlap_stats({"a","b","c"},{"b","c","d"})
  self.assertEqual(x["shared_ids"],2)
  self.assertAlmostEqual(x["first_fraction"],.66667,places=5)
  self.assertTrue("does_not_prove_building" in SCRIPT.read_text())
 def test_bad_sha_or_size_rejected(self):
  with tempfile.TemporaryDirectory() as tmp:
   p=Path(tmp)/"archive.7z";p.write_bytes(b"not a real archive")
   with self.assertRaisesRegex(ValueError,"original archive"):
    mod.verify_source(p,{"size":999,"sha256":"0"*64})
   with self.assertRaisesRegex(ValueError,"SHA-256"):
    mod.verify_source(p,{"size":18,"sha256":"0"*64})
 def _sample(self,root,label):
  d=root/label;d.mkdir()
  (d/"test.xml").write_text(f"{label} {mod.EDITIONS[label]['metadata_extraction']} LAMB93 D075",encoding="utf8")
  for i,kind in enumerate(mod.TYPES):
   name=d/("BATI_"+kind)
   w=shapefile.Writer(str(name),shapeType=shapefile.POLYGON)
   w.field("ID","C",size=30);w.field("HAUTEUR","N",size=5)
   x=650000+i*25;y=6860000+i*25
   w.poly([[[x,y],[x+10,y],[x+10,y+10],[x,y+10],[x,y]]])
   w.record(f"BATIMENT{i:017d}",10+i);w.close()
   # pyshp writes lower-case components, historical IGN packages upper-case.
   for ext in (".shp",".shx",".dbf"):
    name.with_suffix(ext).rename(name.with_suffix(ext.upper()))
   name.with_suffix(".PRJ").write_text("Lambert 93")
   name.with_suffix(".CPG").write_text("UTF-8")
  return d
 def test_synthetic_shapes_and_date_provenance(self):
  with tempfile.TemporaryDirectory() as t:
   root=Path(t);d=self._sample(root,"2011-04-12")
   ids,result=mod.validate_footprints("2011-04-12",d)
   self.assertEqual(len(ids),3)
   self.assertEqual(result["total"],3)
   self.assertEqual(result["metadata_extraction"],"2021-10-05")
 def test_nonconforming_metadata_blocks(self):
  with tempfile.TemporaryDirectory() as t:
   root=Path(t);d=self._sample(root,"2018-03-29")
   (d/"test.xml").write_text("2018-03-29 LAMB93 D075")
   with self.assertRaisesRegex(ValueError,"Historical date"):
    mod.validate_footprints("2018-03-29",d)
 def test_duplicate_id_fails(self):
  with tempfile.TemporaryDirectory() as t:
   root=Path(t);d=self._sample(root,"2018-03-29")
   p=next(d.glob("*INDUSTRIEL.DBF"))
   # Overwrite only the first record's fixed-width ID field.
   data=bytearray(p.read_bytes())
   start=32+32*2+1
   data[start:start+30]=b"BATIMENT00000000000000000".ljust(30,b" ")
   p.write_bytes(data)
   with self.assertRaisesRegex(ValueError,"Duplicate"):
    mod.validate_footprints("2018-03-29",d)
if __name__=="__main__":unittest.main()
