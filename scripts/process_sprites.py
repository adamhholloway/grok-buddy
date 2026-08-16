#!/usr/bin/env python3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from buddy.sprites import process_all, process_character


def main():
    if len(sys.argv) > 1:
        written = process_character(sys.argv[1])
    else:
        written = process_all()
    if not written:
        print("no sprites written", file=sys.stderr)
        return 1
    for path in written:
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
