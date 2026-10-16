#!/usr/bin/env python3
"""Archive the exact official IGN Contours... IRIS edition 2025 GeoParquet.
No download unless --execute. This is a statistical geographic boundary,
not an observation of empty apartments or an annual historical map.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import tempfile
from urllib.parse import urlparse
from urllib.request import HTTPRedirectHandler, Request, build_opener
import uuid

from collect_insee import exclusive_root_lock, valid_magic, MAX_BYTES

SOURCE_ID = "contours-iris-2025"
SOURCE_PAGE = "https://www.data.gouv.fr/datasets/contours-iris-r-2"
CATALOG_URL = "https://data.geopf.fr/telechargement/resource/CONTOURS-IRIS/CONTOURS-IRIS_3-0__GEOPARQUET_WGS84G_FRA_2025-01-01"
URL = "https://data.geopf.fr/telechargement/download/CONTOURS-IRIS/CONTOURS-IRIS_3-0__GEOPARQUET_WGS84G_FRA_2025-01-01/contours_iris.parquet"
FILENAME = "contours_iris_2025.parquet"

def allowed_url(url: str) -> bool:
    p = urlparse(url)
    return p.scheme == "https" and p.hostname == "data.geopf.fr" and p.username is None and p.password is None

class GeoportalOnlyRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if not allowed_url(newurl):
            raise ValueError("IGN request redirected outside trusted Geoportal host")
        return super().redirect_request(req, fp, code, msg, headers, newurl)

def archive_ign(root: Path, opener=None) -> dict:
    if not allowed_url(URL):
        raise ValueError("Invalid configured IGN source URL")
    target_dir = root / "raw" / "ign" / SOURCE_ID
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / FILENAME
    if target.exists():
        raise FileExistsError(f"Immutable original already exists: {target}")
    opener = opener or build_opener(GeoportalOnlyRedirect())
    temporary = None
    digest = hashlib.sha256()
    total = 0
    try:
        fd, name = tempfile.mkstemp(dir=target_dir, prefix=".download-")
        temporary = Path(name)
        with os.fdopen(fd, "wb") as output:
            request = Request(URL, headers={
                "Accept": "application/octet-stream,*/*",
                "User-Agent": "VACANT-research/0.1 (https://github.com/Kiwinokoto/vacant)"
            })
            with opener.open(request, timeout=45) as response:
                final_url = response.geturl()
                if not allowed_url(final_url):
                    raise ValueError("Untrusted final download URL")
                media = (response.headers.get("Content-Type") or "").lower()
                declared_length = response.headers.get("Content-Length")
                if "text/html" in media or (declared_length and int(declared_length) > MAX_BYTES):
                    raise ValueError("Invalid media type or declared size")
                while True:
                    block = response.read(256 * 1024)
                    if not block:
                        break
                    total += len(block)
                    if total > MAX_BYTES:
                        raise ValueError("Archive exceeds size cap")
                    output.write(block)
                    digest.update(block)
                etag = response.headers.get("ETag")
            output.flush()
            os.fsync(output.fileno())
        if total == 0 or not valid_magic(temporary, "parquet"):
            raise ValueError("IGN expected valid Parquet with PAR1 signature")
        os.link(temporary, target)  # immutable original, no clobber
        try:
            record = {
                "dataset_id": SOURCE_ID,
                "organisme": "IGN / Insee",
                "title": "Contours... IRIS, édition 2025 (Géoparquet WGS84G)",
                "geography_year": 2025,
                "catalog_url": CATALOG_URL,
                "landing_page": SOURCE_PAGE,
                "request_url": URL,
                "response_url": final_url,
                "licence_claim": "Licence Ouverte 2.0 (according to official product listing)",
                "extracted_at": datetime.now(timezone.utc).isoformat(),
                "filename": str(target.relative_to(root)),
                "format": "GeoParquet",
                "size_bytes": total,
                "sha256": digest.hexdigest(),
                "etag": etag,
                "status": "raw_unvalidated",
                "comment": "Original archive only; geographical coverage and IRIS codes remain to audit",
            }
            dest = root / "manifests"
            dest.mkdir(parents=True, exist_ok=True)
            with (dest / (SOURCE_ID + "-" + uuid.uuid4().hex + ".json")).open("x", encoding="utf-8") as f:
                json.dump(record, f, indent=2, ensure_ascii=False)
                f.write("\n")
            return record
        except BaseException:
            target.unlink(missing_ok=True)
            raise
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("/srv/vacant/data"))
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args(argv)
    print("IGN", SOURCE_ID, "source:", URL)
    if not args.execute:
        print("PREVIEW ONLY; no writes until --execute.")
        return 0
    try:
        with exclusive_root_lock(args.root):
            report = archive_ign(args.root)
            print("ARCHIVED", report["filename"], report["size_bytes"], report["sha256"])
        return 0
    except (OSError, RuntimeError, ValueError) as error:
        print("STOPPED:", error)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
