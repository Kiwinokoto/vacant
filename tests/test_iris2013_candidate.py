"""Synthetic tests; no real IRIS geometry exported or downloaded."""
import importlib.util
from pathlib import Path
import tempfile
import unittest
from zipfile import ZipFile

from shapely.geometry import Polygon
from shapely.affinity import translate

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/audit_iris2013_candidate.py"
spec = importlib.util.spec_from_file_location("iris2013candidate", SCRIPT)
# import the other standalone repo scripts normally when run inside project
import sys
sys.path.insert(0, str(SCRIPT.parent))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class CandidateGeometryTests(unittest.TestCase):
    def setUp(self):
        self.g = Polygon([(0, 0), (10, 0), (10, 10), (0, 10)])

    def test_near_identical_duplicate_geometry(self):
        diff = module.variants_equivalent([self.g, self.g, translate(self.g, xoff=0.00000001)])
        self.assertLess(diff, 0.001)

    def test_reject_geometrically_changed_duplicate(self):
        with self.assertRaisesRegex(ValueError, "Conflicting"):
            module.variants_equivalent([self.g, translate(self.g, xoff=1)])

    def test_invalid_geometry_rejected(self):
        invalid = Polygon([(0, 0), (1, 1), (0, 1), (1, 0)])
        with self.assertRaisesRegex(ValueError, "Invalid"):
            module.variants_equivalent([self.g, invalid])

    def test_untrusted_archive_paths_and_names_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            archive = Path(temp) / "bad.zip"
            with ZipFile(archive, "w") as z:
                z.writestr("../surprise.shp", "unsafe")
            with self.assertRaisesRegex(ValueError, "Unexpected"):
                with module.isolated_shapefile(archive):
                    pass
            self.assertFalse((Path(temp) / "surprise.shp").exists())

    def test_source_is_pinned_and_candidate_not_public(self):
        self.assertEqual(len(module.SOURCE_SHA), 64)
        self.assertIn("data.gouv.fr", module.SOURCE_URL)
        self.assertIn("not_approved", module.PRIVATE_STATUS)


if __name__ == "__main__":
    unittest.main()
