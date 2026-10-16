"""Purely synthetic tests; no Internet access or real observations involved."""
from pathlib import Path
from importlib.util import module_from_spec, spec_from_file_location
import hashlib
import io
import tempfile
import unittest
import zipfile
from email.message import Message

script = Path(__file__).resolve().parents[1] / "scripts" / "collect_insee.py"
spec = spec_from_file_location("collect_insee", script)
module = module_from_spec(spec)
spec.loader.exec_module(module)

class Response:
    def __init__(self, data, url="https://www.insee.fr/fixture", media="application/zip"):
        self.body = io.BytesIO(data)
        self.url = url
        self.headers = Message()
        self.headers["Content-Type"] = media
        self.headers["Content-Length"] = str(len(data))
    def __enter__(self): return self
    def __exit__(self, *_): self.body.close()
    def read(self, count): return self.body.read(count)
    def geturl(self): return self.url

class Opener:
    def __init__(self, response): self.response = response
    def open(self, *args, **kwargs): return self.response

class CollectorTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
    def tearDown(self): self.tmp.cleanup()

    def test_url_allowlist(self):
        self.assertTrue(module.allowed_url("https://api.insee.fr/file"))
        self.assertFalse(module.allowed_url("http://www.insee.fr/file"))
        self.assertFalse(module.allowed_url("https://insee.fr.evil.example/file"))

    def test_preview_creates_nothing(self):
        self.assertEqual(module.main(["--fetch","rp2023","--root",str(self.root)]),0)
        self.assertEqual(list(self.root.iterdir()),[])

    def test_immutable_original_and_checksum(self):
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w") as z:
            z.writestr("test.txt", "synthetic, not published")
        data = buf.getvalue()
        with module.exclusive_root_lock(self.root):
            info = module.record_source("rp2011", self.root, Opener(Response(data)))
        self.assertEqual(info["sha256"], hashlib.sha256(data).hexdigest())
        self.assertEqual(info["status"], "raw_unvalidated")
        self.assertTrue((self.root / info["filename"]).is_file())
        self.assertEqual(len(list((self.root / "manifests").glob("*.json"))),1)
        with self.assertRaises(FileExistsError):
            module.record_source("rp2011", self.root, Opener(Response(data)))

    def test_html_rejected(self):
        with self.assertRaises(ValueError):
            module.record_source("rp2011", self.root, Opener(Response(b"<html>bad</html>", media="text/html")))
        self.assertEqual(list((self.root / "raw" / "insee" / "rp2011").iterdir()),[])

    def test_bad_signature_and_redirect(self):
        with self.assertRaises(ValueError):
            module.record_source("rp2011", self.root, Opener(Response(b"not a ZIP")))
        with self.assertRaises(ValueError):
            module.record_source("rp2011", self.root, Opener(Response(b"PK\x03\x04bad", url="https://example.org/data")))

    def test_exclusive_lock(self):
        with module.exclusive_root_lock(self.root):
            with self.assertRaises(RuntimeError):
                with module.exclusive_root_lock(self.root):
                    pass

if __name__ == "__main__":
    unittest.main()
