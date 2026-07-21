"""Read Noita's uncompressed ``data.wak`` archive directory."""

from __future__ import annotations

import mmap
import re
import struct
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class WakEntry:
    path: str
    offset: int
    size: int


@dataclass(frozen=True)
class WakArchive:
    path: Path
    version: int
    directory_end: int
    entries: tuple[WakEntry, ...]

    @classmethod
    def open(cls, path: Path) -> "WakArchive":
        archive_size = path.stat().st_size
        with path.open("rb") as source:
            header = source.read(16)
            if len(header) != 16:
                raise ValueError("truncated WAK header")
            version, count, directory_end, reserved = struct.unpack("<IIII", header)
            if reserved != 0:
                raise ValueError(f"unexpected WAK reserved word 0x{reserved:x}")
            entries = []
            for index in range(count):
                metadata = source.read(12)
                if len(metadata) != 12:
                    raise ValueError("truncated WAK directory entry")
                offset, size, path_length = struct.unpack("<III", metadata)
                raw_path = source.read(path_length)
                if len(raw_path) != path_length:
                    raise ValueError("truncated WAK path")
                try:
                    entry_path = raw_path.decode("utf-8")
                except UnicodeDecodeError as error:
                    raise ValueError(
                        f"invalid UTF-8 WAK path at entry {index}: {raw_path.hex()}"
                    ) from error
                if offset < directory_end or offset + size > archive_size:
                    raise ValueError(f"invalid data extent for {entry_path!r}")
                entries.append(WakEntry(entry_path, offset, size))
            if source.tell() != directory_end:
                raise ValueError(
                    f"directory ends at {source.tell()}, header says {directory_end}"
                )
        return cls(path, version, directory_end, tuple(entries))

    def read(self, entry: WakEntry) -> bytes:
        with self.path.open("rb") as source:
            source.seek(entry.offset)
            contents = source.read(entry.size)
        if len(contents) != entry.size:
            raise ValueError(f"truncated data for {entry.path!r}")
        return contents

    def matching_contents(
        self, pattern: bytes, *, flags: int = 0
    ) -> Iterator[tuple[WakEntry, int]]:
        expression = re.compile(pattern, flags)
        with self.path.open("rb") as source:
            with mmap.mmap(source.fileno(), 0, access=mmap.ACCESS_READ) as data:
                for entry in self.entries:
                    match = expression.search(data, entry.offset, entry.offset + entry.size)
                    if match is not None:
                        yield entry, match.start() - entry.offset
