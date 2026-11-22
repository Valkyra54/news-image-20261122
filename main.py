#!/usr/bin/env python3
"""news-image-20261122 — THE SUNDAY GAZETTE.

Writes one image summing up Sunday 22 November 2026 to the output directory.

The image is pre-rendered at build time (entry.png, next to this file).
This entrypoint is stdlib-only: it validates the PNG and copies it to
$MAKEFUN_OUTPUT_DIR (default /output). It never deletes the output
directory itself.
"""

import os
import shutil
import struct
import sys

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MAX_DIM = 1024
MAX_SIZE = 1024 * 1024


def fail(message):
    sys.stderr.write("error: %s\n" % message)
    sys.exit(1)


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    dst = os.path.join(out_dir, "entry.png")

    if not os.path.isfile(src):
        fail("entry.png not found next to main.py")

    with open(src, "rb") as fh:
        data = fh.read()

    if len(data) > MAX_SIZE:
        fail("entry.png is %d bytes, over the 1 MiB limit" % len(data))
    if data[:8] != PNG_SIGNATURE:
        fail("entry.png does not start with the PNG signature")
    if len(data) < 33:
        fail("entry.png is too short to hold an IHDR chunk")
    ihdr_len, ihdr_type = struct.unpack(">I4s", data[8:16])
    if ihdr_type != b"IHDR" or ihdr_len != 13:
        fail("entry.png has no valid IHDR chunk")
    width, height = struct.unpack(">II", data[16:24])
    if width > MAX_DIM or height > MAX_DIM:
        fail("entry.png is %dx%d, over the 1024x1024 limit" % (width, height))
    if data[-8:-4] != b"IEND":
        fail("entry.png has no IEND tail chunk")

    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, dst)
    sys.stdout.write("wrote %s (%dx%d, %d bytes)\n" % (dst, width, height, len(data)))


if __name__ == "__main__":
    main()
