"""Small deterministic contracts for historical Iris reference audit."""
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest import mock

path = Path(__file__).resolve().parents[1] / "scripts" / "audit_iris_references.py"
spec = importlib.util.spec_from_file_location("iris_history_audit", path)
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


class AuditContracts(unittest.TestCase):
    def test_identity_and_renaming_are_distinct(self):
        a = {"751010101": ("Centre", "H"), "751010102": ("Nord", "A")}
        b = {"751010101": ("Centre nouveau", "H"), "751010103": ("Sud", "H")}
        self.assertEqual(audit.compare(a, b), {
            "removed_count": 1, "added_count": 1,
            "renamed_count": 1, "type_changed_count": 0
        })

    def test_code_identity_does_not_claim_geographic_identity(self):
        a = {"751010101": ("Centre", "H")}
        self.assertEqual(audit.compare(a, a)["removed_count"], 0)
        self.assertEqual(audit.compare(a, a)["added_count"], 0)
        self.assertEqual(audit.PARIS, "751")

    def test_bad_or_duplicate_iris_is_rejected(self):
        fake = mock.Mock()
        fake.nrows = 8
        rows = [
            ["géographie 2008"], ["autre"], ["référence"], ["insee"],
            ["libellés"], ["CODE_IRIS", "LIB_IRIS", "TYP_IRIS"],
            ["751010101", "A", "H"], ["751010101", "B", "H"],
        ]
        fake.row_values.side_effect = lambda index: rows[index]
        with self.assertRaises(ValueError):
            audit.read_paris(fake, "xls", 2008, strict_reference=True)

    def test_missing_official_manifest_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            with self.assertRaises(ValueError):
                audit.audited_file(root, root, "iris-ref2008", "missing.zip")


if __name__ == "__main__":
    unittest.main()
