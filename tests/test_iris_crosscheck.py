"""Synthetic tests only; original geographic data are never embedded."""
import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest
from zipfile import ZipFile

from shapely.geometry import Polygon
from shapely.affinity import translate

path=Path(__file__).resolve().parents[1]/"scripts"/"audit_iris_crosscheck.py"
sys.path.insert(0,str(path.parent))
spec=importlib.util.spec_from_file_location("iris_crosscheck",path)
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class IndependentCrosscheckTests(unittest.TestCase):
    def setUp(self):
        self.a=Polygon([(0,0),(10,0),(10,10),(0,10)])

    def test_identical_polygons_have_100_percent_overlap(self):
        m=mod.metrics({"751010101":self.a},{"751010101":self.a})
        self.assertEqual(m["median_iou"],1.0)
        self.assertEqual(m["below_iou_0_99"],0)

    def test_different_outlines_have_lower_overlap(self):
        b=translate(self.a,xoff=1)
        m=mod.metrics({"751010101":self.a},{"751010101":b})
        self.assertLess(m["median_iou"],0.9)

    def test_different_code_sets_are_rejected(self):
        with self.assertRaisesRegex(ValueError,"different"):
            mod.metrics({"751010101":self.a},{"751010102":self.a})

    def test_missing_or_modified_manifest_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaisesRegex(ValueError,"mismatching"):
                mod.verify_manifest(Path(td),"iris-2013-osm-secondary",mod.SOURCES["iris-2013-osm-secondary"]["sha"])

    def test_untrusted_archive_paths_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            archive=Path(td)/"invalid.zip"
            with ZipFile(archive,"w") as z:
                z.writestr("../bad.shp","unsafe")
            with self.assertRaisesRegex(ValueError,"unexpected"):
                with mod.safe_shapefile(archive,mod.SOURCES["iris-2013-osm-secondary"]):
                    pass
            self.assertFalse((Path(td)/"bad.shp").exists())

    def test_2016_not_mistaken_for_2018(self):
        self.assertEqual(mod.SOURCES["iris-2016-secondary"]["crs"],"EPSG:4326")
        self.assertIn("not_approved",mod.REPORT_STATUS)
        self.assertNotIn("2018",mod.SOURCES["iris-2016-secondary"]["basename"])


if __name__=="__main__":
    unittest.main()
