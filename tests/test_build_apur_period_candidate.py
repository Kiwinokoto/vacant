"""Synthetic no-network checks for bounded, private Apur period derivation."""
import importlib.util
import hashlib
import json
import os
from pathlib import Path
import tempfile
import unittest
import zipfile

import shapefile
from pyproj import CRS, Transformer

SOURCE = Path(__file__).resolve().parents[1] / "scripts/build_apur_period_candidate.py"
spec = importlib.util.spec_from_file_location("candidate", SOURCE)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def synthetic_archive(base, *, invalid=False, with_null=False):
    to_m = Transformer.from_crs(4326, 2154, always_xy=True).transform
    basename = str(base / "EMPRISE_BATIE_PARIS")
    with shapefile.Writer(basename, shapeType=shapefile.POLYGON) as shp:
        shp.field("OBJECTID", "N", size=12)
        shp.field("n_sq_eb", "N", size=12)
        shp.field("c_perconst", "N", size=3)
        def ring(coords):
            return [list(to_m(x, y)) for x, y in coords]
        shp.poly([ring([(2.373, 48.854), (2.373, 48.8545),
                        (2.3735, 48.8545), (2.3735, 48.854), (2.373, 48.854)])])
        shp.record(1, None if with_null else 123, 3)
        if invalid:
            shp.poly([list(reversed(ring([(2.374, 48.854), (2.3745, 48.8545),
                            (2.3745, 48.854), (2.374, 48.8545), (2.374, 48.854)])))])
            shp.record(2, 456, 99)
    (base / "EMPRISE_BATIE_PARIS.prj").write_text(CRS.from_epsg(2154).to_wkt())
    (base / "EMPRISE_BATIE_PARIS.cpg").write_text("UTF-8")
    archive = base / "frozen.zip"
    with zipfile.ZipFile(archive, "w") as z:
        for name in module.EXPECTED_MEMBERS:
            z.write(base / name, arcname=name)
    manifest = base / "manifest.json"
    manifest.write_text(json.dumps({"files": {"frozen.zip": {
        "size_bytes": archive.stat().st_size,
        "sha256": hashlib.sha256(archive.read_bytes()).hexdigest()}}}))
    private = base / "private"
    private.mkdir(mode=0o700)
    os.chmod(private, 0o700)
    return archive, manifest, private


class CandidateTests(unittest.TestCase):
    BBOX = [2.373, 48.854, 2.376, 48.856]

    def test_projected_polygon_not_loose_envelope(self):
        polygon = module.projected_selection(*self.BBOX)
        self.assertTrue(polygon.is_valid)
        self.assertGreater(polygon.area, 0)
        self.assertFalse(polygon.equals(polygon.envelope))
        self.assertGreater(len(polygon.exterior.coords), 16)

    def test_reject_large_selection(self):
        with self.assertRaises(ValueError):
            module.projected_selection(2.2, 48.80, 2.4, 48.89)

    def test_private_output_and_allowlisted_attributes(self):
        with tempfile.TemporaryDirectory() as tmp:
            archive, manifest, folder = synthetic_archive(Path(tmp))
            output = folder / "periods.geojson"
            metadata = module.build(archive, manifest, output, self.BBOX, expected_records=1)
            payload = json.loads(output.read_text())
            self.assertEqual(output.stat().st_mode & 0o077, 0)
            self.assertEqual(metadata["matched_source_features"], 1)
            self.assertFalse(payload["metadata"]["public_release_allowed"])
            self.assertEqual(set(payload["features"][0]["properties"]),
                             {"object_id", "period_code"})
            with self.assertRaises(ValueError):
                module.build(archive, manifest, output, self.BBOX, expected_records=1)

    def test_invalid_shape_is_excluded(self):
        with tempfile.TemporaryDirectory() as tmp:
            archive, manifest, folder = synthetic_archive(Path(tmp), invalid=True)
            metadata = module.build(archive, manifest, folder / "out.geojson",
                                    self.BBOX, expected_records=2)
            self.assertEqual(metadata["matched_source_features"], 2)
            self.assertEqual(metadata["included_features"], 1)
            self.assertEqual(metadata["excluded"]["invalid_geometry"], 1)

    def test_null_business_id_excluded(self):
        with tempfile.TemporaryDirectory() as tmp:
            archive, manifest, folder = synthetic_archive(Path(tmp), with_null=True)
            metadata = module.build(archive, manifest, folder / "out.geojson",
                                    self.BBOX, expected_records=1)
            self.assertEqual(metadata["excluded"]["missing_business_id"], 1)
            self.assertEqual(metadata["included_features"], 0)

    def test_cap_refuses_without_creating_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            archive, manifest, folder = synthetic_archive(Path(tmp), invalid=True)
            output = folder / "none.geojson"
            with self.assertRaisesRegex(ValueError, "cap"):
                module.build(archive, manifest, output, self.BBOX,
                             max_features=1, expected_records=2)
            self.assertFalse(output.exists())

    def test_checksum_tampering_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            archive, manifest, folder = synthetic_archive(Path(tmp))
            archive.write_bytes(archive.read_bytes() + b"altered")
            with self.assertRaisesRegex(ValueError, "SHA-256"):
                module.build(archive, manifest, folder / "none.geojson",
                             self.BBOX, expected_records=1)

    def test_dangling_output_symlink_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            archive, manifest, folder = synthetic_archive(Path(tmp))
            target = folder / "link.geojson"
            target.symlink_to(folder / "absent")
            with self.assertRaises(ValueError):
                module.build(archive, manifest, target, self.BBOX, expected_records=1)


if __name__ == "__main__":
    unittest.main()
