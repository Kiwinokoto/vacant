import importlib.util
import hashlib
from pathlib import Path
import tempfile
import unittest
import json

path=Path(__file__).resolve().parents[1]/"scripts"/"build_apur_lab_heights.py"
spec=importlib.util.spec_from_file_location("apur_heights",path)
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class HeightsTests(unittest.TestCase):
    def test_median_height_keeps_meters(self):
        self.assertEqual(module.normal_height({"h_med":12.345,"h_min":4,"h_max":20}),12.35)
    def test_height_zero_means_unavailable_not_ground_floor(self):
        self.assertIsNone(module.normal_height({"h_med":0,"h_min":0,"h_max":5}))
    def test_null_height_not_forced_to_zero(self):
        self.assertIsNone(module.normal_height({"h_med":None,"h_min":None,"h_max":None}))
    def test_inconsistent_minimum_excluded_not_clipped(self):
        self.assertIsNone(module.normal_height({"h_med":1.3,"h_min":3.8,"h_max":14}))
    def test_inconsistent_maximum_excluded_not_clipped(self):
        self.assertIsNone(module.normal_height({"h_med":22,"h_min":3,"h_max":18}))
    def test_high_architectural_height_preserved(self):
        self.assertEqual(module.normal_height({"h_med":300,"h_min":None,"h_max":None}),300)
    def test_sha_helper(self):
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder)/"f"
            p.write_bytes(b"frozen")
            self.assertEqual(module.sha_file(p),hashlib.sha256(b"frozen").hexdigest())
    def test_wrong_original_snapshot_fails_closed(self):
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder)/"fake.zip";p.write_bytes(b"test")
            m=Path(folder)/"manifest.json"
            m.write_text(json.dumps({"files":{"fake.zip":{"size_bytes":4,"sha256":"0"*64}}}))
            candidate=Path(folder)/"candidate.geojson";candidate.write_text("{}")
            with self.assertRaisesRegex(ValueError,"SHA-256"):
                module.build(p,m,candidate,"0"*64,Path(folder)/"out.geojson")

if __name__=="__main__":
    unittest.main()
