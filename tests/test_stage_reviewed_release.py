"""Regression tests for the reviewed VACANT static-release staging gate."""
from hashlib import sha256
from pathlib import Path
import importlib.util
import os
import subprocess
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "stage_reviewed_release.py"
spec = importlib.util.spec_from_file_location("release_gate", SCRIPT)
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)


def git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], check=True,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          text=True).stdout.strip()


class ReleaseGateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        base = Path(self.temp.name)
        self.repo = base / "repo"
        self.repo.mkdir()
        git(self.repo, "init", "--quiet")
        git(self.repo, "config", "user.email", "vacant-test@example.invalid")
        git(self.repo, "config", "user.name", "VACANT tests")
        (self.repo/"site/data/apur-grid").mkdir(parents=True)
        (self.repo/"site/index.html").write_text("<!doctype html><title>VACANT</title>")
        (self.repo/"site/app.mjs").write_text("console.log('VACANT');")
        (self.repo/"site/data/.gitignore").write_text("*.geojson\n")
        (self.repo/"site/data/apur-grid/.gitignore").write_text("*\n!.gitignore\n")
        git(self.repo, "add", "site")
        git(self.repo, "commit", "-qm", "test fixture")
        self.sha = git(self.repo, "rev-parse", "HEAD")
        self.destroot = base / "releases"
        self.destroot.mkdir()
        self.dest = self.destroot/self.sha
        self.public = base / "public"
        self.public.mkdir()
        self.datasets = {}
        for filename in gate.ALLOWED_DATASETS:
            file = self.public/filename
            file.write_text('{"type":"FeatureCollection","features":[]}', encoding="utf-8")
            self.datasets[filename] = (file, gate.digest(file))
        # Contents ignored by Git on purpose; must never appear in a release.
        (self.repo/"site/data/apur-grid/manifest.json").write_text("PRIVATE APUR")
        (self.repo/"site/data/apur-grid/cell_000.geojson").write_text("PRIVATE GEOMETRY")

    def build(self):
        return gate.stage_public_release(self.repo, self.sha, self.dest, self.datasets)

    def test_stage_from_git_only_leaves_ignored_apur_private(self):
        result = self.build()
        self.assertTrue((result/"site/index.html").is_file())
        self.assertEqual(result.stat().st_mode & 0o777, 0o755)
        self.assertEqual((result/"site").stat().st_mode & 0o777, 0o755)
        self.assertEqual((result/"site/index.html").stat().st_mode & 0o777, 0o644)
        self.assertFalse((result/"site/data/apur-grid").exists())
        self.assertFalse((result/"site/data/apur-lab.geojson").exists())
        for filename in gate.ALLOWED_DATASETS:
            self.assertTrue((result/"site/data"/filename).is_file())
        self.assertFalse((self.repo/"site/data/apur-grid/manifest.json").stat().st_size == 0)

    def test_refuses_second_stage_without_overwrite(self):
        self.build()
        with self.assertRaisesRegex(ValueError, "new"):
            self.build()

    def test_refuses_wrong_checkout_sha(self):
        with self.assertRaisesRegex(ValueError, "HEAD"):
            gate.stage_public_release(self.repo, "0"*40, self.destroot/("0"*40), self.datasets)
        self.assertFalse((self.destroot/("0"*40)).exists())

    def test_missing_or_bad_sha_public_data_is_rejected(self):
        src, _ = self.datasets["iris-2023.geojson"]
        self.datasets["iris-2023.geojson"] = (src, "1"*64)
        with self.assertRaisesRegex(ValueError, "SHA-256"):
            self.build()
        self.assertFalse(self.dest.exists())

    def test_symlinked_public_source_rejected(self):
        target, hash = self.datasets["iris-2023.geojson"]
        link = self.public/"iris-link.geojson"
        link.symlink_to(target)
        self.datasets["iris-2023.geojson"] = (link, hash)
        with self.assertRaisesRegex(ValueError, "Missing or oversized"):
            self.build()

    def test_tracked_apur_geometry_blocks_stage_entirely(self):
        bad = self.repo/"site/data/apur-grid/private.geojson"
        bad.write_text("PRIVATE TEST FIXTURE")
        # Git's ignore is intentionally overridden here to simulate a mistake.
        git(self.repo, "add", "-f", str(bad))
        git(self.repo, "commit", "-qm", "accidentally tracked private data")
        head = git(self.repo, "rev-parse", "HEAD")
        with self.assertRaisesRegex(ValueError, "private data"):
            gate.stage_public_release(self.repo, head, self.destroot/head, self.datasets)
        self.assertFalse((self.destroot/head).exists())

    def test_only_three_reviewed_tracked_aggregates_are_staged(self):
        for relative in gate.TRACKED_PUBLIC_AGGREGATES:
            file = self.repo / relative
            file.write_text('{"kind":"reviewed_synthetic_fixture"}', encoding="utf-8")
        git(self.repo, "add", "site/data")
        git(self.repo, "commit", "-qm", "three reviewed public aggregates")
        head = git(self.repo, "rev-parse", "HEAD")
        result = gate.stage_public_release(
            self.repo, head, self.destroot / head, self.datasets)
        for relative in gate.TRACKED_PUBLIC_AGGREGATES:
            self.assertEqual((result / relative).read_text(),
                             '{"kind":"reviewed_synthetic_fixture"}')
        self.assertFalse((result / "site/data/apur-grid").exists())

    def test_arbitrary_tracked_json_still_refused(self):
        file = self.repo / "site/data/other-data.json"
        file.write_text('{"address":"private test value"}', encoding="utf-8")
        git(self.repo, "add", "site/data/other-data.json")
        git(self.repo, "commit", "-qm", "unreviewed json test")
        head = git(self.repo, "rev-parse", "HEAD")
        with self.assertRaisesRegex(ValueError, "Unreviewed"):
            gate.stage_public_release(
                self.repo, head, self.destroot / head, self.datasets)

    def test_allowlisted_name_outside_data_directory_is_rejected(self):
        file = self.repo / "site/lovac-paris-open-2026.json"
        file.write_text('{"kind":"wrong_location"}', encoding="utf-8")
        git(self.repo, "add", "site/lovac-paris-open-2026.json")
        git(self.repo, "commit", "-qm", "misplaced public aggregate")
        head = git(self.repo, "rev-parse", "HEAD")
        with self.assertRaisesRegex(ValueError, "Unreviewed"):
            gate.stage_public_release(
                self.repo, head, self.destroot / head, self.datasets)

    def test_tracked_unreviewed_dataset_blocks_stage(self):
        bad = self.repo/"site/footprints.geojson"
        bad.write_text("PRIVATE")
        git(self.repo, "add", "site/footprints.geojson")
        git(self.repo, "commit", "-qm", "accidentally tracked dataset")
        head = git(self.repo, "rev-parse", "HEAD")
        with self.assertRaisesRegex(ValueError, "Unreviewed"):
            gate.stage_public_release(self.repo, head, self.destroot/head, self.datasets)
        self.assertFalse((self.destroot/head).exists())


if __name__ == "__main__":
    unittest.main()
