"""Synthetic-only tests: the institutional SQL is never executed."""
import importlib.util
import sys
from pathlib import Path
import tempfile
import unittest
from unittest import mock

from shapely.geometry import Polygon
from shapely import wkb

source = Path(__file__).resolve().parents[1] / "scripts/audit_iris2014_atlasante.py"
sys.path.insert(0, str(source.parent))
spec=importlib.util.spec_from_file_location("atlasante_auditor", source)
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

def sample(srid=2154, code="751010101"):
    polygon=Polygon([(650000,6860000),(650020,6860000),(650020,6860020),(650000,6860020)])
    geom=wkb.dumps(polygon,hex=True,srid=srid).encode()
    return mod.INSERT_PREFIX+b"'"+geom+b"', '75101', 'PARIS 1E ARRONDISSEMENT', '0101', '"+code.encode()+b"', 'TEST', 'H', NULL);\n"

class Atlasante2014Contracts(unittest.TestCase):
    def test_parse_valid_paris_EWKB(self):
        code,binary=mod.parse_paris_insert(sample())
        self.assertEqual(code,"751010101")
        self.assertTrue(binary.startswith(b"\x01"))

    def test_mismatched_iris_code_rejected(self):
        with self.assertRaisesRegex(ValueError,"Inconsistent"):
            mod.parse_paris_insert(sample(code="751010102"))

    def test_wrong_crs_rejected(self):
        with self.assertRaisesRegex(ValueError,"SRID"):
            mod.parse_paris_insert(sample(srid=4326))

    def test_unexpected_sql_never_executed(self):
        with self.assertRaisesRegex(ValueError,"Unexpected"):
            mod.parse_paris_insert(b"DROP TABLE public.users;")

    def test_non_paris_skipped(self):
        line=sample().replace(b"'75101', 'PARIS",b"'75056', 'PARIS",1)
        self.assertIsNone(mod.parse_paris_insert(line))

    def test_untrusted_data_root_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaisesRegex(ValueError,"not present"):
                mod.load_atlasante(Path(temp))

    def test_audit_status_not_public(self):
        self.assertIn("not_licensed_for_publication", mod.STATUS)
        self.assertEqual(len(mod.ARCHIVE_SHA),64)

if __name__=="__main__":
    unittest.main()
