import importlib.util
from pathlib import Path
import unittest

p=Path(__file__).resolve().parents[1]/"scripts"/"sample_apur_geometry.py"
spec=importlib.util.spec_from_file_location("sample_apur_geometry",p)
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class GeometrySampleTests(unittest.TestCase):
    def test_params_bounded(self):
        self.assertEqual(mod.params("1=1",0,8)["outSR"],4326)
        with self.assertRaises(ValueError): mod.params("1=1",0,100)
        with self.assertRaises(ValueError): mod.params("1=0",0,8)
    def test_valid_polygon_and_inconsistent_height(self):
        feature={"properties":{"OBJECTID":1,"h_med":1.3,"h_min":3.8,"h_max":14},
            "geometry":{"type":"Polygon","coordinates":[[[2.3,48.85],[2.301,48.85],[2.301,48.851],[2.3,48.851],[2.3,48.85]]]}}
        result=mod.inspect([feature],lambda x,y:(x,y))
        self.assertEqual(result["valid"],1)
        self.assertEqual(result["inconsistent_h_med"],1)
    def test_duplicate_id_rejected(self):
        f={"properties":{"OBJECTID":1},"geometry":None}
        with self.assertRaises(ValueError): mod.inspect([f,f],lambda x,y:(x,y))
    def test_geometry_absent_is_invalid(self):
        r=mod.inspect([{"properties":{"OBJECTID":9},"geometry":None}],lambda x,y:(x,y))
        self.assertEqual(r["invalid"],1)

if __name__=="__main__": unittest.main()
