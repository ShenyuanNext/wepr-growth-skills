import argparse
import hashlib
import json
import tempfile
import unittest
import zipfile
from pathlib import Path

from install_viewer import MARKER, VERSION, install


class ViewerInstallationTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.archive = self.root / "viewer.zip"
        self.checksum = self.root / "viewer.sha256"
        self.destination = self.root / "installed"

    def tearDown(self):
        self.temp.cleanup()

    def fixture(self, unsafe=False):
        files = {name: b"test notice" for name in
                 ["LICENSE", "LICENSE-CODE", "LICENSE-CONTENT", "THIRD_PARTY_NOTICES.md"]}
        files["index.html"] = b"original research index"
        files["geo-citation-lab-manifest.json"] = json.dumps(
            {"distribution_version": VERSION}).encode()
        if unsafe:
            files["../outside.txt"] = b"unsafe"
        lines = [hashlib.sha256(body).hexdigest() + "  " + name
                 for name, body in files.items()]
        files["geo-citation-lab-files.sha256"] = "\n".join(lines).encode()
        with zipfile.ZipFile(self.archive, "w") as package:
            for name, body in files.items():
                package.writestr(name, body)
        self.checksum.write_text(hashlib.sha256(self.archive.read_bytes()).hexdigest())

    def args(self):
        return argparse.Namespace(dir=self.destination, archive=self.archive, checksum=self.checksum)

    def test_installs_and_preserves_originals_on_upgrade(self):
        self.fixture()
        first = install(self.args())
        self.assertIsNone(first["backup_path"])
        self.assertIn("WEPR", (self.destination / "index.html").read_text())
        self.assertEqual((self.destination / "research-index.html").read_text(), "original research index")
        self.assertEqual((self.destination / "LICENSE").read_bytes(), b"test notice")
        second = install(self.args())
        self.assertTrue((Path(second["backup_path"]) / MARKER).exists())

    def test_corruption_does_not_replace_existing_install(self):
        self.fixture()
        install(self.args())
        previous = (self.destination / MARKER).read_bytes()
        self.archive.write_bytes(self.archive.read_bytes() + b"corruption")
        with self.assertRaisesRegex(ValueError, "SHA-256 mismatch"):
            install(self.args())
        self.assertEqual((self.destination / MARKER).read_bytes(), previous)

    def test_unmanaged_folder_is_preserved(self):
        self.fixture()
        self.destination.mkdir()
        with self.assertRaisesRegex(ValueError, "not managed"):
            install(self.args())
        self.assertEqual(list(self.destination.iterdir()), [])

    def test_path_traversal_is_rejected(self):
        self.fixture(unsafe=True)
        with self.assertRaisesRegex(ValueError, "Unsafe ZIP path"):
            install(self.args())
        self.assertFalse((self.root / "outside.txt").exists())
        self.assertFalse(self.destination.exists())


if __name__ == "__main__":
    unittest.main()
