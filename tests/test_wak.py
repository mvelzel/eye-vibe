import struct
import tempfile
import unittest
from pathlib import Path

from eye_mystery.wak import WakArchive


class WakTests(unittest.TestCase):
    def test_reads_directory_and_searches_bounded_file_contents(self):
        files = (("data/a.txt", b"an eye"), ("data/b.bin", b"eyeless"))
        directory_end = 16 + sum(12 + len(path) for path, _ in files)
        offset = directory_end
        directory = bytearray(struct.pack("<IIII", 0, len(files), directory_end, 0))
        body = bytearray()
        for path, contents in files:
            encoded_path = path.encode()
            directory.extend(struct.pack("<III", offset, len(contents), len(encoded_path)))
            directory.extend(encoded_path)
            body.extend(contents)
            offset += len(contents)
        with tempfile.TemporaryDirectory() as temporary:
            archive_path = Path(temporary) / "data.wak"
            archive_path.write_bytes(directory + body)
            archive = WakArchive.open(archive_path)
            self.assertEqual(archive.version, 0)
            self.assertEqual([entry.path for entry in archive.entries], ["data/a.txt", "data/b.bin"])
            self.assertEqual(archive.read(archive.entries[0]), b"an eye")
            self.assertEqual(
                [(entry.path, found) for entry, found in archive.matching_contents(b"eye")],
                [("data/a.txt", 3), ("data/b.bin", 0)],
            )


if __name__ == "__main__":
    unittest.main()
