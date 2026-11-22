#!/usr/bin/env python3
"""Write the front-page image to the grader's output directory.

The image itself is drawn by render.py and shipped in this repository
as entry.png. This program only validates it (PNG magic bytes and the
1 MiB size limit) and copies it to $MAKEFUN_OUTPUT_DIR, defaulting to
/output. Standard library only, no network, deterministic: two runs
write the same bytes.
"""

import os
import shutil
import sys
from pathlib import Path

IMAGE_NAME = "entry.png"
SIZE_LIMIT = 1048576
MAGIC = b"\x89PNG\r\n\x1a\n"


def fail(message):
    print(f"main.py: {message}", file=sys.stderr)
    return 1


def main():
    here = Path(__file__).resolve().parent
    source = here / IMAGE_NAME
    try:
        with source.open("rb") as handle:
            if handle.read(len(MAGIC)) != MAGIC:
                return fail(f"{IMAGE_NAME} does not start with PNG magic bytes")
    except OSError as exc:
        return fail(f"cannot read {IMAGE_NAME}: {exc}")
    size = source.stat().st_size
    if size > SIZE_LIMIT:
        return fail(f"{IMAGE_NAME} is {size} bytes, over the 1 MiB limit")
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / IMAGE_NAME
    shutil.copyfile(source, target)
    print(f"wrote {target} ({size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
