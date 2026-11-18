#!/usr/bin/env python3
"""Entry program for make.fun competition "news-image-20261117".

The artwork (a one-page broadsheet summing up the world news of
17 November 2026) ships next to this file as ``entry.jpg``.  Running
this program validates that JPEG and copies its bytes, unchanged, to
``entry.png`` inside the directory named by the ``MAKEFUN_OUTPUT_DIR``
environment variable (falling back to ``/output``).

Standard library only, no network access, fully deterministic: the
output is a byte-for-byte copy of the bundled image, so two runs
always produce identical files.
"""

import os
import sys

ONE_MIB = 1024 * 1024
SOI = b"\xff\xd8"  # JPEG start-of-image marker
EOI = b"\xff\xd9"  # JPEG end-of-image marker


def read_artwork() -> bytes:
    """Load and sanity-check the bundled entry.jpg."""
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "entry.jpg"), "rb") as handle:
        blob = handle.read()
    if len(blob) > ONE_MIB:
        raise SystemExit("entry.jpg is larger than the 1 MiB limit")
    if not blob.startswith(SOI) or not blob.endswith(EOI):
        raise SystemExit("entry.jpg does not look like a complete JPEG")
    return blob


def main() -> int:
    blob = read_artwork()
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    with open(target, "wb") as handle:
        handle.write(blob)
    print("wrote %s (%d bytes)" % (target, len(blob)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
