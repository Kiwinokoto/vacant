#!/usr/bin/env python3
"""Stage a reviewed VACANT static release from Git-tracked files ONLY.

Safety rules:
- The Git commit must be specified as a full SHA, never an unpinned branch.
- No ignored, untracked, or private Apur files in any release.
- Public datasets are copied only by explicit, SHA-256-verified whitelisting.
- Output is a NEW destination; never overwrite or deploy automatically.
"""
from __future__ import annotations

import argparse
from hashlib import sha256
import io
import os
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import tarfile
import tempfile

ALLOWED_DATASETS = frozenset({"iris-2023.geojson", "arrond-history.geojson"})
FORBIDDEN_PARTS = frozenset({"apur-grid", "_local", "raw", "processed", "private"})
MAX_ARCHIVE = 20_000_000
MAX_PUBLIC_DATASET = 40_000_000


def digest(path: Path) -> str:
    h = sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def assert_sha(value: str):
    if len(value) != 64 or any(c not in "0123456789abcdef" for c in value):
        raise ValueError("A full lower-case SHA-256 is required")


def tracked_site(archive: bytes, site_dir: Path):
    """Extract a tracked Git site archive without accepting symlinks/other paths."""
    with tarfile.open(fileobj=io.BytesIO(archive), mode="r:") as tar:
        members = tar.getmembers()
        if not members:
            raise ValueError("Empty tracked site")
        for m in members:
            p = PurePosixPath(m.name)
            if (not p.parts or p.parts[0] != "site" or
                    any(x in ("", ".", "..") for x in p.parts) or
                    not (m.isfile() or m.isdir())):
                raise ValueError("Unexpected path or special file in Git archive")
            private_marker = "apur-grid" in p.parts and (m.isdir() or p.name == ".gitignore")
            if any(x in FORBIDDEN_PARTS for x in p.parts) and not private_marker:
                raise ValueError("Unexpected private data tracked in Git archive")
            if m.isfile() and not private_marker:
                if len(p.parts) < 2:
                    raise ValueError("Unexpected top-level tracked file")
                name = p.name
                if (name.endswith((".geojson", ".json")) and
                        name not in ALLOWED_DATASETS):
                    raise ValueError("Unreviewed tracked dataset in site/")
                if (p.parts[1] == "data" and len(p.parts) > 2 and
                        name not in ALLOWED_DATASETS and name != ".gitignore"):
                    raise ValueError("Unexpected tracked data in site/data/")
        for m in members:
            p = PurePosixPath(m.name)
            relative = p.parts[1:]
            if not relative or "apur-grid" in p.parts:
                continue
            target = site_dir.joinpath(*relative)
            if m.isdir():
                target.mkdir(parents=True, exist_ok=True)
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                with tar.extractfile(m) as f, target.open("xb") as output:
                    shutil.copyfileobj(f, output)


def stage_public_release(repo: Path, commit: str, dest: Path,
                         datasets: dict[str, tuple[Path, str]],
                         apur: tuple[Path, str, str, str] | None = None):
    if len(commit) != 40 or any(c not in "0123456789abcdef" for c in commit):
        raise ValueError("An immutable full Git commit SHA is mandatory")
    if set(datasets) != set(ALLOWED_DATASETS):
        raise ValueError("Both audited public datasets must be explicitly provided")
    dest = Path(dest)
    if not dest.is_absolute() or not Path(repo).is_absolute():
        raise ValueError("Repository and release path must be absolute")
    if dest.exists() or dest.is_symlink() or dest.name != commit:
        raise ValueError("Release destination must be new and named after the commit")
    parent = dest.parent.resolve(strict=True)
    if parent in (Path("/"), Path.home()) or any(x in FORBIDDEN_PARTS for x in parent.parts):
        raise ValueError("Release directory is not allowed")
    expected = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "--verify", "HEAD^{commit}"],
        check=True, capture_output=True, text=True).stdout.strip()
    if expected != commit:
        raise ValueError("Checkout HEAD does not match pinned release commit")
    for name, (path, sha) in datasets.items():
        if name not in ALLOWED_DATASETS:
            raise ValueError("Unexpected public dataset name")
        assert_sha(sha)
        if not path.is_file() or path.is_symlink() or path.stat().st_size > MAX_PUBLIC_DATASET:
            raise ValueError("Missing or oversized public dataset")
        if digest(path) != sha:
            raise ValueError("Public dataset SHA-256 mismatch")
    raw = subprocess.run(
        ["git", "-C", str(repo), "archive", "--format=tar", commit, "site"],
        check=True, capture_output=True).stdout
    if len(raw) > MAX_ARCHIVE:
        raise ValueError("Unexpected tracked site archive size")
    stage = Path(tempfile.mkdtemp(dir=parent, prefix=".vacant-reviewed-"))
    os.chmod(stage, 0o700)
    try:
        site = stage / "site"
        site.mkdir()
        tracked_site(raw, site)
        public = site / "data"
        public.mkdir(exist_ok=True)
        for name, (src, expected_sha) in datasets.items():
            output = public / name
            if output.exists() or output.is_symlink():
                raise ValueError("Tracked data file would be overwritten")
            shutil.copyfile(src, output, follow_symlinks=False)
            if digest(output) != expected_sha:
                raise ValueError("Copied dataset SHA-256 mismatch")
            os.chmod(output, 0o644)
        if apur is not None:
            from scripts.package_apur_public import (
                package_grid, PRIVATE_MANIFEST_SHA, PUBLIC_DATASET_NAME)
            src, input_sha, published_sha, zip_sha = apur
            for value in (input_sha, published_sha, zip_sha):
                assert_sha(value)
            if input_sha != PRIVATE_MANIFEST_SHA:
                raise ValueError("Apur source manifest not pinned to reviewed frozen extract")
            apur_dir = public / "apur-grid"
            if apur_dir.exists() or apur_dir.is_symlink():
                raise ValueError("Apur public distribution path already populated")
            apur_dir.mkdir(mode=0o700)
            receipt = package_grid(src, apur_dir)
            if (receipt["source_manifest_sha256"] != input_sha or
                    receipt["public_manifest_sha256"] != published_sha or
                    receipt["zip_sha256"] != zip_sha or
                    not (apur_dir / PUBLIC_DATASET_NAME).is_file()):
                raise ValueError("Public ODbL derivative hash differs from approved release")
        if not (site / "index.html").is_file():
            raise ValueError("Missing main VACANT page")
        # Fail closed even if someone tracks a file with another extension below
        # a forbidden Apur path in the future.
        if any("_local" in p.parts or
               ("apur-grid" in p.parts and apur is None)
               for p in site.rglob("*")):
            raise ValueError("Apur private data directory accidentally staged")
        # Nginx needs to traverse the immutable read-only release.
        # Keep staging private until every check above has succeeded.
        for p in site.rglob("*"):
            if p.is_dir():
                os.chmod(p, 0o755)
            elif p.is_file():
                os.chmod(p, 0o644)
        os.chmod(site, 0o755)
        os.chmod(stage, 0o755)
        if dest.exists():
            raise ValueError("Destination appeared during release preparation")
        stage.rename(dest)
        stage = None
        return dest
    finally:
        if stage is not None:
            shutil.rmtree(stage)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--commit", required=True)
    parser.add_argument("--destination", type=Path, required=True)
    parser.add_argument("--iris", type=Path, required=True)
    parser.add_argument("--iris-sha256", required=True)
    parser.add_argument("--arrond", type=Path, required=True)
    parser.add_argument("--arrond-sha256", required=True)
    parser.add_argument("--publish-apur", action="store_true",
                        help="Explicit opt-in to distribute the audited ODbL base")
    parser.add_argument("--apur-private-dir", type=Path)
    parser.add_argument("--apur-private-manifest-sha256")
    parser.add_argument("--apur-public-manifest-sha256")
    parser.add_argument("--apur-public-zip-sha256")
    parser.add_argument("--execute", action="store_true",
                        help="Required: writing a new staged release, never deploying")
    args = parser.parse_args()
    if not args.execute:
        parser.error("No files created; use --execute after reviewing hashes/paths")
    supplied = (args.apur_private_dir, args.apur_private_manifest_sha256,
                args.apur_public_manifest_sha256, args.apur_public_zip_sha256)
    if args.publish_apur != all(x is not None for x in supplied):
        parser.error("Publishing Apur requires --publish-apur AND all four pinned arguments")
    apur = supplied if args.publish_apur else None
    result = stage_public_release(args.repo, args.commit, args.destination,
                                  {"iris-2023.geojson": (args.iris, args.iris_sha256),
                                   "arrond-history.geojson": (args.arrond, args.arrond_sha256)},
                                  apur=apur)
    print(f"Prepared immutable static tree: {result} (not deployed)")


if __name__ == "__main__":
    main()
