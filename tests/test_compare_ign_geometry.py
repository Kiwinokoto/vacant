"""Synthetic invariants for full historic BD TOPO geometry audit."""
import importlib.util
from pathlib import Path
import sys
import unittest
import shapefile

SCRIPT=Path(__file__).resolve().parents[1]/"scripts"/"compare_ign_geometry.py"
sys.path.insert(0,str(SCRIPT.parent))
spec=importlib.util.spec_from_file_location("compare_ign_geometry",SCRIPT)
geo=importlib.util.module_from_spec(spec);spec.loader.exec_module(geo)

def rectangle(x0,y0,x1,y1):
    # Shapefile polygon exterior ring clockwise.
    s=shapefile.Shape(shapefile.POLYGON)
    s.points=[(x0,y0),(x0,y1),(x1,y1),(x1,y0),(x0,y0)]
    s.parts=[0]
    return s

class GeometryAuditTests(unittest.TestCase):
    def test_exact_fingerprint_is_stable_and_coordinate_sensitive(self):
        a=rectangle(0,0,1,1);b=rectangle(0,0,1,1);c=rectangle(0,0,1.001,1)
        self.assertEqual(geo.vertex_fingerprint(a),geo.vertex_fingerprint(b))
        self.assertNotEqual(geo.vertex_fingerprint(a),geo.vertex_fingerprint(c))
    def test_counts_are_reference_edits_not_building_events(self):
        a={"same":(b"a","INDIFFERENCIE",10,0),
           "changed":(b"a","INDIFFERENCIE",10,1),
           "absent":(b"z","INDUSTRIEL",5,2)}
        b={"same":(b"a","INDIFFERENCIE",10,0),
           "changed":(b"b","REMARQUABLE",12,1),
           "new_id":(b"n","INDUSTRIEL",5,2)}
        stats,changed=geo.compare_metadata(a,b)
        self.assertEqual(stats["shared_ids"],2)
        self.assertEqual(stats["only_in_2011_reference"],1)
        self.assertEqual(stats["only_in_2018_reference"],1)
        self.assertEqual(stats["exact_same_vertex_lists"],1)
        self.assertEqual(stats["changed_feature_class"],1)
        self.assertEqual(stats["changed_height_attribute"],1)
        self.assertEqual(changed,["changed"])
    def test_geos_iou_is_spatial_ratio_not_building_count(self):
        self.assertAlmostEqual(geo.overlap_iou(rectangle(0,0,2,2),rectangle(1,0,3,2)),1/3)
        self.assertEqual(geo.overlap_iou(rectangle(0,0,2,2),rectangle(0,0,2,2)),1)
        self.assertEqual(geo.overlap_iou(rectangle(0,0,2,2),rectangle(4,4,6,6)),0)

if __name__=="__main__":
    unittest.main()
