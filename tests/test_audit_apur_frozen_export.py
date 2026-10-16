"""Synthetic, no-network tests for the Apur frozen archive audit."""
import importlib.util
import json
from pathlib import Path
import hashlib
import tempfile
import unittest

path = Path(__file__).resolve().parents[1] / "scripts/audit_apur_frozen_export.py"
spec = importlib.util.spec_from_file_location("apur_frozen", path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class FrozenExportTests(unittest.TestCase):
    def test_codes(self):
        self.assertNotIn(4, mod.PERIODS)
        self.assertIn(11, mod.PERIODS)
        self.assertIn(12, mod.PERIODS)
        self.assertIn(99, mod.PERIODS)

    def test_geos_sampling(self):
        self.assertTrue(mod.should_check_geometry(17, 3, 17))
        self.assertTrue(mod.should_check_geometry(1, 99, 17))
        self.assertTrue(mod.should_check_geometry(1, None, 17))
        self.assertTrue(mod.should_check_geometry(1, 3, 300))
        self.assertFalse(mod.should_check_geometry(1, 3, 17))
        with self.assertRaises(ValueError):
            mod.should_check_geometry(None, 3, 17)

    def test_height_missing_and_zero_are_distinct(self):
        self.assertEqual(mod.height_flags({"h_med": None}), ["missing"])
        self.assertEqual(mod.height_flags({"h_med": 0}), ["zero"])

    def test_height_outlier_retained_not_clipped(self):
        self.assertEqual(mod.height_flags({"h_med": 300, "h_min": None, "h_max": None}), ["above_200"])
        self.assertEqual(mod.height_flags({"h_med": 1.3, "h_min": 3.8, "h_max": 14}), ["below_min"])

    def test_original_sha256_validated(self):
        with tempfile.TemporaryDirectory() as tmp:
            archive = Path(tmp) / "sample.zip"
            archive.write_bytes(b"synthetic only")
            manifest = Path(tmp) / "manifest.json"
            manifest.write_text(json.dumps({"files": {archive.name: {
                "sha256": hashlib.sha256(archive.read_bytes()).hexdigest(),
                "size_bytes": archive.stat().st_size}}}))
            self.assertEqual(mod.check_hash(archive, manifest),
                             hashlib.sha256(archive.read_bytes()).hexdigest())
            archive.write_bytes(b"tampered")
            with self.assertRaisesRegex(ValueError, "hash or size"):
                mod.check_hash(archive, manifest)

if __name__ == "__main__":
    unittest.main()
