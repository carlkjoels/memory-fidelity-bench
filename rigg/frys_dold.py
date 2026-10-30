"""Freeze the hidden set: a SHA-256 manifest over every ground-truth file.

After freezing, the PROTOKOLL rule applies: the hidden set is run ONCE. If any
file changes afterwards the manifest breaks and the set is spent — a new hidden
set is required. The freezer (whoever runs this) is not the author and not the
one who fixes the rig; the roles are kept apart so no one can teach to the test.

    python rigg/frys_dold.py           # create DOLD_MANIFEST.sha256 (once)
    python rigg/frys_dold.py --verify  # check that nothing changed
"""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

DOLD = Path(__file__).resolve().parent.parent / "facit" / "dold"
MANIFEST = Path(__file__).resolve().parent.parent / "DOLD_MANIFEST.sha256"


def _hashar() -> list[str]:
    rader = []
    for f in sorted(DOLD.glob("*.json")):
        h = hashlib.sha256(f.read_bytes()).hexdigest()
        rader.append(f"{h}  facit/dold/{f.name}")
    return rader


def frys() -> int:
    if MANIFEST.exists():
        print("DOLD_MANIFEST.sha256 already exists — the hidden set is already "
              "frozen. A new set is required to re-freeze.", file=sys.stderr)
        return 1
    rader = _hashar()
    if not rader:
        print("facit/dold/ is empty — nothing to freeze.", file=sys.stderr)
        return 1
    MANIFEST.write_text("\n".join(rader) + "\n")
    print(f"Froze {len(rader)} hidden ground-truth files in {MANIFEST.name}. "
          "The set now runs ONCE; if any file changes the manifest breaks.")
    return 0


def verify() -> int:
    if not MANIFEST.exists():
        print("no manifest — the set is not frozen yet", file=sys.stderr)
        return 1
    forvantat = MANIFEST.read_text().strip().splitlines()
    nu = _hashar()
    if forvantat == nu:
        print(f"OK — all {len(nu)} hidden files unchanged since freezing.")
        return 0
    print("BROKEN MANIFEST — the hidden set has changed and is spent. "
          "A new hidden set is required.", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(verify() if "--verify" in sys.argv else frys())
