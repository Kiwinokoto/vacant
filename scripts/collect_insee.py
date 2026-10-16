#!/usr/bin/env python3
"""Archive verified official INSEE files; does NOT process or publish them.

Offline preview by default. Run on an authorized private Linux host only after
checking host identity, free disk space, AgentCTL leases and existing work.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import os
from pathlib import Path
import tempfile
from urllib.parse import urlparse
from urllib.request import HTTPRedirectHandler, Request, build_opener
import uuid
import zipfile

MAX_BYTES = 750 * 1024 * 1024
SOURCES = {
    "rp2006": dict(url="https://www.insee.fr/fr/statistiques/fichier/2028562/BTX_IC_LOG_2006.xls",
                   filename="BTX_IC_LOG_2006.xls", year=2006, geography_year=2008,
                   page="https://www.insee.fr/fr/statistiques/2028562", fmt="xls"),
    "rp2011": dict(url="https://www.insee.fr/fr/statistiques/fichier/2028269/infra-logement-2011.zip",
                   filename="infra-logement-2011.zip", year=2011, geography_year=2013,
                   page="https://www.insee.fr/fr/statistiques/2028269", fmt="zip"),
    "rp2016": dict(url="https://www.insee.fr/fr/statistiques/fichier/4228432/base-ic-logement-2016.zip",
                   filename="base-ic-logement-2016.zip", year=2016, geography_year=2018,
                   page="https://www.insee.fr/fr/statistiques/4228432", fmt="zip"),
    "rp2023": dict(url="https://api.insee.fr/melodi/file/DS_RP_LOGEMENT_PRINC_IRIS_2023/PARQUET",
                   filename="DS_RP_LOGEMENT_PRINC_IRIS_2023.parquet", year=2023, geography_year=2025,
                   page="https://www.insee.fr/fr/statistiques/9061333", fmt="parquet"),
    "rp2023-passage": dict(url="https://www.insee.fr/fr/statistiques/fichier/9061333/table_passage_logement.xlsx",
                   filename="table_passage_logement_2023.xlsx", year=2023, geography_year=2025,
                   page="https://www.insee.fr/fr/statistiques/9061333", fmt="xlsx"),
}

def allowed_url(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.scheme == "https" and parsed.hostname in {"www.insee.fr", "api.insee.fr"} and not parsed.username and not parsed.password

class OfficialOnlyRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if not allowed_url(newurl):
            raise ValueError("Redirect outside official HTTPS INSEE hosts refused")
        return super().redirect_request(req, fp, code, msg, headers, newurl)

def valid_magic(path: Path, fmt: str) -> bool:
    with path.open("rb") as file:
        start = file.read(8)
        if fmt == "parquet":
            file.seek(-4, os.SEEK_END)
            return start.startswith(b"PAR1") and file.read(4) == b"PAR1"
        if fmt == "xls":
            return start == bytes.fromhex("D0CF11E0A1B11AE1")
        if fmt in ("xlsx", "zip"):
            return start.startswith(b"PK\x03\x04") and zipfile.is_zipfile(path)
    return False

@contextmanager
def exclusive_root_lock(root: Path):
    root.mkdir(parents=True, exist_ok=True)
    with (root / ".collect-insee.lock").open("a+b") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise RuntimeError("Another VACANT collector is active") from exc
        try:
            yield
        finally:
            fcntl.flock(lock, fcntl.LOCK_UN)

def record_source(source_id: str, root: Path, opener=None) -> dict:
    source = SOURCES[source_id]
    if not allowed_url(source["url"]):
        raise ValueError("Disallowed source URL")
    directory = root / "raw" / "insee" / source_id
    directory.mkdir(parents=True, exist_ok=True)
    target = directory / source["filename"]
    if target.exists():
        raise FileExistsError(f"Immutable original already exists: {target}")
    opener = opener or build_opener(OfficialOnlyRedirect())
    temporary = None
    count = 0
    digest = hashlib.sha256()
    try:
        fd, name = tempfile.mkstemp(prefix=".download-", dir=directory)
        temporary = Path(name)
        with os.fdopen(fd, "wb") as output:
            request = Request(source["url"], headers={"User-Agent": "VACANT-research/0.1 (https://github.com/Kiwinokoto/vacant)", "Accept": "application/octet-stream,*/*"})
            with opener.open(request, timeout=45) as response:
                final_url = response.geturl()
                if not allowed_url(final_url):
                    raise ValueError("Final URL is not approved")
                media_type = (response.headers.get("Content-Type") or "").lower()
                content_length = response.headers.get("Content-Length")
                if "text/html" in media_type or (content_length and int(content_length) > MAX_BYTES):
                    raise ValueError("HTML response or unexpectedly large payload")
                while True:
                    block = response.read(256 * 1024)
                    if not block:
                        break
                    count += len(block)
                    if count > MAX_BYTES:
                        raise ValueError("Size cap exceeded")
                    output.write(block)
                    digest.update(block)
                etag = response.headers.get("ETag")
                last_modified = response.headers.get("Last-Modified")
            output.flush()
            os.fsync(output.fileno())
        if count == 0 or not valid_magic(temporary, source["fmt"]):
            raise ValueError("Empty or invalid file format")
        os.link(temporary, target)  # atomic no-clobber, including racing writers
        try:
            record = {
                "dataset_id": source_id,
                "organisme": "Insee",
                "recensement_year": source["year"],
                "geography_year": source["geography_year"],
                "landing_page": source["page"],
                "request_url": source["url"],
                "response_url": final_url,
                "licence_claim": "Licence Ouverte 2.0 (verify on the original dataset page)",
                "extracted_at": datetime.now(timezone.utc).isoformat(),
                "filename": str(target.relative_to(root)),
                "content_type": media_type,
                "etag": etag,
                "last_modified": last_modified,
                "size_bytes": count,
                "sha256": digest.hexdigest(),
                "status": "raw_unvalidated",
                "comment": "Not yet audited for IRIS geography, statistical meaning or republication",
            }
            manifests = root / "manifests"
            manifests.mkdir(parents=True, exist_ok=True)
            with (manifests / (source_id + "-" + uuid.uuid4().hex + ".json")).open("x", encoding="utf-8") as manifest:
                json.dump(record, manifest, indent=2, ensure_ascii=False)
                manifest.write("\n")
            return record
        except BaseException:
            target.unlink(missing_ok=True)  # never retain an untracked raw original
            raise
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("/srv/vacant/data"))
    parser.add_argument("--fetch", nargs="+", choices=sorted(SOURCES), metavar="ID")
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args(argv)
    requested = args.fetch or list(SOURCES)
    for key in requested:
        source = SOURCES[key]
        print(f"{key} · RP{source['year']} / IRIS geo{source['geography_year']} · {source['url']}")
    if not args.execute:
        print("PREVIEW ONLY. No data written. --execute explicitly required.")
        return 0
    try:
        with exclusive_root_lock(args.root):
            for key in requested:
                record = record_source(key, args.root)
                print(f"ARCHIVED {key}: {record['size_bytes']} bytes / SHA-256 {record['sha256']}")
        return 0
    except (OSError, RuntimeError, ValueError) as err:
        print("STOPPED without overwriting originals:", err)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
