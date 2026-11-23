#!/usr/bin/env python3
"""news-image-20261122 v2 — THE SUNDAY GAZETTE (Monday refresh).

Stdlib-only entry program (the make.fun grader has no Pillow): validates the
pre-rendered entry.png and copies it to $MAKEFUN_OUTPUT_DIR.
The image itself is rendered at build time by render.py (PIL, build machine
only) from the verified stories in the lab research notes.
"""
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
MAX_BYTES = 1024 * 1024
PNG_SIG = b"\x89PNG\r\n\x1a\n"


def fail(msg):
    print("error: " + msg, file=sys.stderr)
    return 1


def main():
    if not os.path.isfile(SRC):
        return fail("entry.png not found next to main.py")
    size = os.path.getsize(SRC)
    if size >= MAX_BYTES:
        return fail("entry.png is %d bytes, must be < 1 MiB" % size)
    with open(SRC, "rb") as f:
        data = f.read()
    if data[:8] != PNG_SIG:
        return fail("entry.png is not a PNG file")
    if len(data) < 33 or data[12:16] != b"IHDR":
        return fail("entry.png has no IHDR chunk")
    width, height = struct.unpack(">II", data[16:24])
    if (width, height) != (1024, 1024):
        return fail("entry.png is %dx%d, expected 1024x1024" % (width, height))
    if data[-12:] != b"\x00\x00\x00\x00IEND\xaeB`\x82":
        return fail("entry.png has no valid IEND tail")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, out_path)
    print("copied entry.png (%dx%d, %d bytes) -> %s" % (width, height, size, out_path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
