"""Publish the 17 November 2026 world-news front page as the entry image.

The artwork staged beside this script (entry.jpg) already is the finished
entry: a one-page newspaper that sums up Tuesday 17 November 2026. This
program's single job is to deliver those exact bytes to the folder the
harness reads, under the name it expects, and to prove on the way that
nothing was altered, truncated or swapped.

Run it twice and the output is identical both times: the bytes written
are the bytes staged, with a digest check before the program exits.
"""

from __future__ import annotations

import hashlib
import os
import sys
from pathlib import Path

STAGED_NAME = "entry.jpg"
OUTPUT_NAME = "entry.png"
BYTE_LIMIT = 1_048_576  # the competition's 1 MiB ceiling
JPEG_SOI = b"\xff\xd8\xff"
JPEG_EOI = b"\xff\xd9"


def staged_picture() -> Path:
    """Locate the artwork that ships with this repository."""
    path = Path(__file__).resolve().parent / STAGED_NAME
    if not path.is_file():
        raise SystemExit(f"staged artwork not found: {path}")
    return path


def checked_bytes(path: Path) -> bytes:
    """Read the artwork and refuse anything that is not a whole JPEG."""
    blob = path.read_bytes()
    if not blob.startswith(JPEG_SOI):
        raise SystemExit("staged artwork is not a JPEG (missing SOI marker)")
    if not blob.endswith(JPEG_EOI):
        raise SystemExit("staged artwork looks truncated (missing EOI marker)")
    if len(blob) > BYTE_LIMIT:
        raise SystemExit(f"artwork is {len(blob)} bytes, over the {BYTE_LIMIT} limit")
    if len(blob) < 10_000:
        raise SystemExit(f"artwork is only {len(blob)} bytes, too small to be the front page")
    return blob


def output_folder() -> Path:
    """Resolve where the harness collects finished entries."""
    folder = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def main() -> int:
    source = staged_picture()
    blob = checked_bytes(source)

    target = output_folder() / OUTPUT_NAME
    target.write_bytes(blob)

    written = target.read_bytes()
    if written != blob:
        raise SystemExit("verification failed: written bytes differ from staged artwork")

    digest = hashlib.sha256(written).hexdigest()
    print(f"entry written: {target} ({len(written)} bytes, sha256 {digest})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
