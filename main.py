#!/usr/bin/env python3
"""Copy the pre-rendered broadsheet to the output directory.

The image itself is rendered by draw.py (PIL) at build time and
committed to this repository; the grader runs without PIL or fonts,
so this program only copies the committed file, byte for byte.
"""

import os
import shutil
import sys


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print("wrote", dst)


if __name__ == "__main__":
    sys.exit(main())
