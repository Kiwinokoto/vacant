"""No-network tests for Apur private grid policy and synthetic SHP input."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest
import zipfile

import shapefile
from pyproj import CRS, Transformer
from shapely.geometry import box

script = Path(__file__).resolve().parents[1] / "scripts" / "build_apur_private_grid.py"
spec = importlib.util.spec_from_file_location("apur_grid", script)
grid = importlib.util.module_from_spec(spec)
spec.loader.exec_module(grid)


def synthetic_source(folder: Path):
    prefix = folder / "EMPRISE_BATIE_PARIS"
    to_m = Transformer.from_crs(4326, 2154, always_xy=True)
    with shapefile.Writer(str(prefix), shapeType=shapefile.POLYGON) as writer:
        for key in ("OBJECTID", "n_sq_eb", "c_perconst"):
            writer.field(key, "N", size=10)
        for key in ("h_med", "h_min", "h_max"):
            writer.field(key, "F", size=12, decimal=2)

        def add(index, business, code, median, coordinates):
            points = [list(to_m.transform(x, y)) for x, y in coordinates]
            writer.poly([points])
            writer.record(index, business, code, median, 2, 40)

        add(1, 1001, 3, 24,
            [(2.373, 48.854), (2.373, 48.8545),
             (2.3735, 48.8545), (2.3735, 48.854), (2.373, 48.854)])
        # Intentional invalid bow-tie.
        add(2, 1002, 11, 20,
            [(2.374, 48.855), (2.3745, 48.8555),
             (2.374, 48.8555), (2.3745, 48.855), (2.374, 48.855)])
        add(3, None, 99, 9,
            [(2.375, 48.855), (2.375, 48.8555),
             (2.3755, 48.8555), (2.3755, 48.855), (2.375, 48.855)])
        add(4, 1004, 12, 18,
            [(2.376, 48.855), (2.376, 48.8555),
             (2.3765, 48.8555), (2.3765, 48.855), (2.376, 48.855)])

    (folder / "EMPRISE_BATIE_PARIS.prj").write_text(CRS.from_epsg(2154).to_wkt())
    (folder / "EMPRISE_BATIE_PARIS.cpg").write_text("UTF-8")
    archive = folder / "source.zip"
    with zipfile.ZipFile(archive, "w") as z:
        for name in grid.EXPECTED_MEMBERS:
            z.write(folder / name, arcname=name)
    manifest = folder / "source-manifest.json"
    manifest.write_text(json.dumps({"files": {archive.name: {
        "size_bytes": archive.stat().st_size,
        "sha256": hashlib.sha256(archive.read_bytes()).hexdigest()
    }}}))
    target_root = folder / "private"
    target_root.mkdir(mode=0o700)
    os.chmod(target_root, 0o700)
    return archive, manifest, target_root


class ApurGridTests(unittest.TestCase):
    def test_height_is_metric_and_missing_is_not_zero(self):
        self.assertEqual(grid.normal_height({"h_med": 300, "h_min": None, "h_max": None}), 300)
        self.assertIsNone(grid.normal_height({"h_med": 0, "h_min": 0, "h_max": 10}))
        self.assertIsNone(grid.normal_height({"h_med": 3, "h_min": 5, "h_max": 20}))

    def test_positive_area_grid_intersection_excludes_touch_only(self):
        polygon = box(650000, 6860000, 650500, 6860500)
        self.assertEqual(grid.candidate_cells(polygon, 500), [(1300, 13720)])

    def test_crossing_cells_duplicates_feature_by_design(self):
        polygon = box(650400, 6860400, 650600, 6860600)
        self.assertEqual(set(grid.candidate_cells(polygon, 500)),
                         {(1300,13720),(1300,13721),(1301,13720),(1301,13721)})

    def test_too_many_cells_rejected(self):
        with self.assertRaisesRegex(ValueError, "large polygon"):
            grid.candidate_cells(box(640000, 6850000, 650000, 6860000), 500)

    def test_private_folder_required(self):
        with tempfile.TemporaryDirectory() as dirname:
            root = Path(dirname)
            folder = root / "public"
            folder.mkdir(mode=0o755)
            os.chmod(folder, 0o755)
            with self.assertRaisesRegex(ValueError, "private"):
                grid.safe_private_destination(folder / "out")

    def test_densified_wgs84_bbox_covers_projected_cell(self):
        to_geo = Transformer.from_crs(2154, 4326, always_xy=True)
        bounds = grid.geographic_bbox(1300,13720,500,to_geo)
        x, y = to_geo.transform(650250,6860250)
        self.assertLessEqual(bounds[0],x)
        self.assertLessEqual(bounds[1],y)
        self.assertGreaterEqual(bounds[2],x)
        self.assertGreaterEqual(bounds[3],y)

    def test_archive_build_exclusions_and_tile_integrity(self):
        with tempfile.TemporaryDirectory() as name:
            archive, manifest, folder = synthetic_source(Path(name))
            output = folder / "grid"
            result = grid.build(archive, manifest, output, expected_records=4)
            self.assertEqual(result["source_count"], 4)
            self.assertEqual(result["unique_features"], 2)
            self.assertEqual(result["skipped_by_exclusive_reason"],
                             {"invalid_geometry": 1, "missing_business_id": 1})
            self.assertFalse(result["public_release_allowed"])
            self.assertEqual((output.stat().st_mode & 0o077), 0)
            data = json.loads((output / "manifest.json").read_text())
            ids = set()
            for cell in data["cells"].values():
                path = output / cell["file"]
                self.assertEqual(grid.sha256_file(path), cell["sha256"])
                self.assertEqual(path.stat().st_mode & 0o077, 0)
                payload = json.loads(path.read_text())
                for feature in payload["features"]:
                    self.assertEqual(set(feature["properties"]),
                                     {"object_id","period_code","height_m"})
                    ids.add(feature["properties"]["object_id"])
            self.assertEqual(ids, {1,4})
            self.assertGreaterEqual(result["placements"], 2)
            with self.assertRaises(ValueError):
                grid.build(archive, manifest, output, expected_records=4)

    def test_source_tampering_does_not_create_output(self):
        with tempfile.TemporaryDirectory() as name:
            archive, manifest, folder = synthetic_source(Path(name))
            archive.write_bytes(archive.read_bytes()+b"tamper")
            with self.assertRaisesRegex(ValueError, "SHA-256"):
                grid.build(archive, manifest, folder / "not-created",
                           expected_records=4)
            self.assertFalse((folder / "not-created").exists())


if __name__ == "__main__":
    unittest.main()
