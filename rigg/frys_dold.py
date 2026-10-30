"""Freeze hidden set v2: a SHA-256 manifest over every ground-truth file.

The hidden set lives in a PRIVATE path outside this repo (default
~/memory-fidelity-bench-private/dold-v2, override with MFBENCH_DOLD). Only the
manifest is committed publicly, in advance. The conversation files are published
only after the single run — the manifest proves the set was fixed beforehand,
publication proves it was not altered.

After freezing, the PROTOKOLL rule applies: the hidden set is run ONCE. If any
file changes afterwards the manifest breaks and the set is spent — a new hidden
set is required. The freezer (whoever runs this) is not the author and not the
one who fixes the rig; the roles are kept apart so no one can teach to the test.

Hidden set v1 is spent: it was committed to the public repo and is therefore
known (see PREREGISTRERING.md changelog).

    python rigg/frys_dold.py           # create DOLD_MANIFEST_V2.sha256 (once)
    python rigg/frys_dold.py --verify  # check that nothing changed
"""
from __future__ import annotations

import hashlib
import os
import sys
from pathlib import Path

DOLD = Path(os.environ.get("MFBENCH_DOLD",
                           Path.home() / "memory-fidelity-bench-private" / "dold-v2"))
MANIFEST = Path(__file__).resolve().parent.parent / "DOLD_MANIFEST_V2.sha256"


def _hashar() -> list[str]:
    rader = []
    for f in sorted(DOLD.glob("*.json")):
        h = hashlib.sha256(f.read_bytes()).hexdigest()
        rader.append(f"{h}  {f.name}")   # bara filnamn — sökvägen är privat
    return rader


def frys() -> int:
    if MANIFEST.exists():
        print("DOLD_MANIFEST_V2.sha256 already exists — hidden set v2 is already "
              "frozen. A new set is required to re-freeze.", file=sys.stderr)
        return 1
    if not DOLD.exists():
        print(f"private hidden-set path not found: {DOLD}\n"
              "set MFBENCH_DOLD or place the externally-authored files there.",
              file=sys.stderr)
        return 1
    rader = _hashar()
    if not rader:
        print(f"{DOLD} is empty — nothing to freeze.", file=sys.stderr)
        return 1
    MANIFEST.write_text("\n".join(rader) + "\n")
    print(f"Froze {len(rader)} hidden (v2) files into {MANIFEST.name} from a "
          "private path. The set runs ONCE; if any file changes the manifest breaks.")
    return 0


def verify() -> int:
    if not MANIFEST.exists():
        print("no manifest — hidden set v2 is not frozen yet", file=sys.stderr)
        return 1
    if not DOLD.exists():
        print(f"cannot verify: private path {DOLD} not present on this machine",
              file=sys.stderr)
        return 1
    if MANIFEST.read_text().strip().splitlines() == _hashar():
        print(f"OK — all hidden (v2) files unchanged since freezing.")
        return 0
    print("BROKEN MANIFEST — hidden set v2 has changed and is spent. "
          "A new hidden set is required.", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(verify() if "--verify" in sys.argv else frys())
