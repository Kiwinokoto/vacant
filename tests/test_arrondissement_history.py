"""Safety tests for historical arrondissement-only mapping."""
import importlib.util
from pathlib import Path
import unittest

module_path = Path(__file__).resolve().parents[1] / "scripts" / "build_arrondissement_history.py"
spec = importlib.util.spec_from_file_location("history_build", module_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class HistoryTests(unittest.TestCase):
    def test_codes_and_values(self):
        module.assert_stat("751010101", 100.2, 9.2, 80, 11)
        for code, total, vacant in [
            ("750560101", 100, 10), ("7510101", 100, 10),
            ("751010101", 10, 11), ("751010101", 10, -1),
            ("751010101", float("nan"), 1),
        ]:
            with self.subTest(code=code, total=total, vacant=vacant), self.assertRaises(ValueError):
                module.assert_stat(code, total, vacant)

    def test_rejects_categories_that_do_not_sum(self):
        with self.assertRaises(ValueError):
            module.assert_stat("751010101", 100, 10, 50, 20)

    def test_rejects_missing_iris_and_forged_totals(self):
        with self.assertRaises(ValueError):
            module.totals_check(2006, [("751010101", 100, 10)] * 992)

    def test_source_versions_are_explicit(self):
        self.assertEqual([module.SOURCE[y][2] for y in (2006, 2011, 2016)], [2008, 2013, 2018])
        self.assertEqual(len(module.ARRONDS), 20)
        self.assertEqual(len(set(module.ARRONDS)), 20)


if __name__ == "__main__":
    unittest.main()
