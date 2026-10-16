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
    def test_reject_outside_paris(self):
        ring=[{"x":3.35,"y":48.85},{"x":3.36,"y":48.85},{"x":3.36,"y":48.86},{"x":3.35,"y":48.85}]
        with self.assertRaises(ValueError):prepare_geometry([[ring]])

if __name__=="__main__":unittest.main()
