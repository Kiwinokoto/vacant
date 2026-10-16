#!/usr/bin/env python3
"""Smoke-test the repository's Nginx gzip configuration on 127.0.0.1 only.

Uses SYNTHETIC files, an ephemeral port, and a separate isolated Nginx process.
Never uses the active VACANT Docker container or real private Apur geometries.
"""
from __future__ import annotations

import argparse
import gzip
import json
from pathlib import Path
import re
import shutil
import socket
import subprocess
import tempfile
import time
import urllib.error
import urllib.request


def request(url, encoding="identity"):
    rq = urllib.request.Request(url, headers={"Accept-Encoding": encoding})
    try:
        with urllib.request.urlopen(rq, timeout=4) as resp:
            return resp.status, resp.headers, resp.read()
    except urllib.error.HTTPError as e:
        return e.code, e.headers, e.read()


def run(config: Path):
    nginx = shutil.which("nginx") or "/usr/sbin/nginx"
    if not Path(nginx).is_file():
        raise RuntimeError("Native Nginx executable not found")
    original = Path(config).read_text(encoding="utf-8")
    if original.count("listen 80;") != 1 or original.count(
            "root /usr/share/nginx/html;") != 1:
        raise ValueError("Unexpected source Nginx server structure")
    if "gzip_types application/geo+json application/json;" not in original:
        raise ValueError("Expected GeoJSON and JSON gzip content types missing")
    with tempfile.TemporaryDirectory(prefix="vacant-nginx-gzip-") as tmp:
        base = Path(tmp)
        base.chmod(0o755)  # Synthetic fixtures only, Nginx worker access.
        docroot = base / "www"
        docroot.mkdir(mode=0o755)
        # Single synthetic gzip-friendly payload. No Apur, LOVAC or private data.
        geojson = json.dumps({"type": "FeatureCollection", "features": [
            {"type": "Feature", "geometry": {"type": "Polygon", "coordinates":
                [[[2.3, 48.8], [2.31, 48.8], [2.31, 48.81],
                  [2.3, 48.81], [2.3, 48.8]]]},
             "properties": {"object_id": i, "period_code": 3}}
            for i in range(300)]}, separators=(",", ":")).encode()
        manifest = json.dumps({"test_only": True, "fake_sha256": "f"*64,
                               "cells": [i for i in range(300)]}).encode()
        fixtures = {"cell_test.geojson": geojson,
                    "manifest.json": manifest,
                    "tiny.geojson": b'{"ok":true}',
                    "module.mjs": b'export const smoke = true;'}
        for name, payload in fixtures.items():
            f = docroot / name
            f.write_bytes(payload)
            f.chmod(0o644)
        (docroot / ".test-hidden").write_text("do not expose")
        with socket.socket() as s:
            s.bind(("127.0.0.1", 0))
            port = s.getsockname()[1]
        test_server = original.replace("listen 80;", f"listen 127.0.0.1:{port};").replace(
            "root /usr/share/nginx/html;", f"root {docroot};")
        conf = (f"worker_processes 1;\n"
                f"pid {base/'nginx.pid'};\n"
                f"error_log {base/'error.log'} warn;\n"
                "events { worker_connections 64; }\n"
                "http { include /etc/nginx/mime.types;\n"
                "access_log off;\n" + test_server + "\n}\n")
        conf_file = base / "isolated.conf"
        conf_file.write_text(conf, encoding="utf-8")
        subprocess.run([nginx, "-t", "-p", str(base), "-c", str(conf_file)],
                       check=True, capture_output=True)
        proc = subprocess.Popen(
            [nginx, "-p", str(base), "-c", str(conf_file), "-g", "daemon off;"],
            stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        try:
            root = f"http://127.0.0.1:{port}"
            for retry in range(60):
                if proc.poll() is not None:
                    raise RuntimeError("Isolated Nginx exited unexpectedly")
                try:
                    status, _, _ = request(root + "/tiny.geojson")
                    if status == 200:
                        break
                except urllib.error.URLError:
                    time.sleep(.05)
            else:
                raise RuntimeError("Isolated Nginx did not start in time")
            results = {}
            for filename in ("cell_test.geojson", "manifest.json"):
                raw = fixtures[filename]
                s, h, compressed = request(root + "/" + filename, "gzip")
                if (s != 200 or h.get("Content-Encoding") != "gzip" or
                        h.get("Vary") != "Accept-Encoding" or
                        gzip.decompress(compressed) != raw):
                    raise AssertionError(f"gzip response broken for {filename}: {s}, {dict(h)}")
                mime = "application/geo+json" if filename.endswith(".geojson") else "application/json"
                if h.get("Content-Type", "").split(";")[0] != mime:
                    raise AssertionError("Unexpected MIME for " + filename)
                s2, h2, plain = request(root + "/" + filename, "identity")
                if s2 != 200 or h2.get("Content-Encoding") or plain != raw:
                    raise AssertionError("Identity byte stream changed")
                results[filename] = {"raw_bytes": len(raw), "gzip_bytes": len(compressed),
                                     "ratio": round(len(compressed)/len(raw), 4),
                                     "mime": mime, "vary": h.get("Vary")}
            small_s, small_h, _ = request(root + "/tiny.geojson", "gzip")
            js_s, js_h, _ = request(root + "/module.mjs", "identity")
            denied_s, _, _ = request(root + "/.test-hidden")
            missing_s, _, _ = request(root + "/nonexistent.geojson")
            if (small_s != 200 or small_h.get("Content-Encoding") or
                    js_s != 200 or "javascript" not in js_h.get("Content-Type","") or
                    denied_s != 403 or missing_s != 404):
                raise AssertionError("Nginx MIME, min_size or access rules regressed")
            print(json.dumps({"isolated_loopback": True, "real_apur_data": False,
                              "tests": results, "tiny_not_gzipped": True,
                              "mjs_mime_ok": True, "dotfiles_denied": True,
                              "unknown_404": True}, indent=2))
        finally:
            proc.terminate()
            try:
                proc.wait(timeout=3)
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.wait(timeout=3)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--config", type=Path, default=Path("deploy/nginx.conf"))
    args = p.parse_args()
    run(args.config)
