"""Synthetic contract tests; never includes real IGN geometry."""
import io
import hashlib
from pathlib import Path
import sys
import tempfile
import unittest
from email.message import Message

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from collect_ign import allowed_url, archive_ign

class FakeResponse:
    def __init__(self, body, url="https://data.geopf.fr/official", media="application/octet-stream"):
        self.input=io.BytesIO(body)
        self.url=url
        self.headers=Message()
        self.headers["Content-Type"]=media
        self.headers["Content-Length"]=str(len(body))
    def __enter__(self):return self
    def __exit__(self,*args):self.input.close()
    def read(self,n):return self.input.read(n)
    def geturl(self):return self.url

class Opener:
    def __init__(self,data):self.data=data
    def open(self,*args,**kwargs):return self.data

class IGNCollectorTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.root=Path(self.temp.name)
    def tearDown(self):self.temp.cleanup()
    def test_domains(self):
        self.assertTrue(allowed_url("https://data.geopf.fr/telechargement/file"))
        self.assertFalse(allowed_url("http://data.geopf.fr/file"))
        self.assertFalse(allowed_url("https://data.geopf.fr.evil.org/file"))
    def test_archives_immutable(self):
        example=b"PAR1"+b"\0"*12+b"PAR1"  # magic fixture only; not a valid GeoParquet file
        report=archive_ign(self.root,Opener(FakeResponse(example)))
        self.assertEqual(report["sha256"],hashlib.sha256(example).hexdigest())
        self.assertEqual(report["status"],"raw_unvalidated")
        with self.assertRaises(FileExistsError):
            archive_ign(self.root,Opener(FakeResponse(example)))
        self.assertTrue((self.root/report["filename"]).exists())
    def test_rejects_bad_source_and_html(self):
        with self.assertRaises(ValueError):
            archive_ign(self.root,Opener(FakeResponse(b"<html></html>",media="text/html")))
        with self.assertRaises(ValueError):
            archive_ign(self.root,Opener(FakeResponse(b"PAR1\0\0PAR1",url="https://wrong.example.com/")))
        with self.assertRaises(ValueError):
            archive_ign(self.root,Opener(FakeResponse(b"not-parquet")))
if __name__=="__main__":
    unittest.main()
