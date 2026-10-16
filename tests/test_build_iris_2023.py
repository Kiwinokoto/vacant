"""Contract-only geometry tests; no invented vacancies ever published."""
import sys
from pathlib import Path
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from build_iris_2023 import prepare_geometry

class ShapeTests(unittest.TestCase):
    def test_valid_multipolygon_structs(self):
        ring=[{"x":2.35,"y":48.85},{"x":2.36,"y":48.85},{"x":2.36,"y":48.86},{"x":2.35,"y":48.85}]
        geo=prepare_geometry([[[*ring]]])
        self.assertEqual(geo["type"],"MultiPolygon")
        self.assertEqual(geo["coordinates"][0][0][0],[2.35,48.85])
    def test_reject_invalid_or_unclosed(self):
        ring=[{"x":2.35,"y":48.85},{"x":2.36,"y":48.85},{"x":2.36,"y":48.86},{"x":2.35,"y":48.86}]
        with self.assertRaises(ValueError):prepare_geometry([[ring]])
    def test_manifest_prefix_collision_is_not_a_collision(self):
        import tempfile, json, hashlib
        from build_iris_2023 import read_original
        with tempfile.TemporaryDirectory() as root_dir:
            root=Path(root_dir)
            (root/"manifests").mkdir()
            raw=root/"raw"/"insee"/"rp2023"
            raw.mkdir(parents=True)
            p=raw/"test.parquet";p.write_bytes(b"synthetic test file")
            manifest={"dataset_id":"rp2023","status":"raw_unvalidated",
                      "filename":str(p.relative_to(root)),"geography_year":2025,
                      "sha256":hashlib.sha256(p.read_bytes()).hexdigest()}
            (root/"manifests"/"rp2023-a.json").write_text(json.dumps(manifest))
            (root/"manifests"/"rp2023-passage-b.json").write_text(json.dumps({"dataset_id":"rp2023-passage"}))
            selected,_=read_original(root,"rp2023")
            self.assertEqual(selected,p)
    def test_reject_outside_paris(self):
        ring=[{"x":3.35,"y":48.85},{"x":3.36,"y":48.85},{"x":3.36,"y":48.86},{"x":3.35,"y":48.85}]
        with self.assertRaises(ValueError):prepare_geometry([[ring]])

if __name__=="__main__":unittest.main()
