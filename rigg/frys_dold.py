"""Frys den dolda uppsättningen: SHA-256-manifest över varje facit-fil.

Efter frysning gäller PROTOKOLL-regeln: den dolda uppsättningen körs EN gång.
Ändras någon fil efteråt bryts manifestet och uppsättningen är förbrukad — en
ny dold uppsättning krävs. Frysaren (den som kör detta) är inte författaren och
inte den som rättar riggen; rollerna hålls isär så att ingen kan teacha mot
testet.

    python rigg/frys_dold.py           # skapar DOLD_MANIFEST.sha256 (en gång)
    python rigg/frys_dold.py --verify  # kontrollerar att inget ändrats
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
        print("DOLD_MANIFEST.sha256 finns redan — den dolda uppsättningen är "
              "redan fryst. En ny uppsättning krävs för att frysa om.", file=sys.stderr)
        return 1
    rader = _hashar()
    if not rader:
        print("facit/dold/ är tom — inget att frysa.", file=sys.stderr)
        return 1
    MANIFEST.write_text("\n".join(rader) + "\n")
    print(f"Fryst {len(rader)} dolda facit-filer i {MANIFEST.name}. "
          "Uppsättningen körs nu EN gång; ändras någon fil bryts manifestet.")
    return 0


def verify() -> int:
    if not MANIFEST.exists():
        print("inget manifest — uppsättningen är inte fryst än", file=sys.stderr)
        return 1
    forvantat = MANIFEST.read_text().strip().splitlines()
    nu = _hashar()
    if forvantat == nu:
        print(f"OK — alla {len(nu)} dolda filer oförändrade sedan frysning.")
        return 0
    print("BRUTET MANIFEST — den dolda uppsättningen har ändrats och är förbrukad. "
          "En ny dold uppsättning krävs.", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(verify() if "--verify" in sys.argv else frys())
