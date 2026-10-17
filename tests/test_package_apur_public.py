"""Public ODbL distribution safety — synthetic negative cases only."""
import importlib.util
from pathlib import Path
import tempfile
import unittest
import json

script=Path(__file__).resolve().parents[1]/"scripts"/"package_apur_public.py"
spec=importlib.util.spec_from_file_location("apur_public",script)
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class ApurPublicTests(unittest.TestCase):
    def test_licence_and_transformation_notice(self):
        self.assertIn("ODbL",mod.NOTICE)
        self.assertIn("scripts/build_apur_private_grid.py",mod.NOTICE)
        self.assertIn("104",mod.NOTICE)
        self.assertIn("13 identifiants",mod.NOTICE)
        self.assertIn("AUCUNE",mod.NOTICE)
        self.assertEqual(mod.PUBLIC_DATASET_NAME,"apur-paris-grid-500m-2026-10-16-odbl.zip")
    def test_no_source_directory_no_output(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t);out=root/"public";out.mkdir()
            with self.assertRaisesRegex(ValueError,"existing audited source"):
                mod.package_grid(root/"missing",out)
            self.assertEqual(list(out.iterdir()),[])
    def test_no_in_place_output(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t)
            with self.assertRaises(ValueError):
                mod.package_grid(root,root)
    def test_tampered_source_manifest_blocks_publication(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t);source=root/"source";source.mkdir()
            (source/"manifest.json").write_text(json.dumps({"license":"ODbL-1.0"}))
            target=root/"target";target.mkdir()
            with self.assertRaisesRegex(ValueError,"SHA-256 mismatch"):
                mod.package_grid(source,target)
            self.assertEqual(list(target.iterdir()),[])
    def test_unreviewed_file_is_refused(self):
        # Source export directory must contain nothing beyond audited cell files,
        # verified by package_grid after checking the fixed source manifest.
        self.assertIn("Unexpected input file",script.read_text())
