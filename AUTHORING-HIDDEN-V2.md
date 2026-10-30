# Instructions for the external author of hidden set v2

You are writing the **hidden test set** for a benchmark that measures *fidelity*
in agent memory: does a memory layer store what the user actually said, and
abstain from what it shouldn't? Your 50 conversations decide whether the
benchmark can tell a good memory layer from a bad one. Thank you for doing this.

## The one rule that makes this work: blindness

**Do not open `facit/utveckling/` in this repository.** That folder holds the
development conversations. If you see them, your hidden set stops being a blind
test — a memory system (or its authors) could then have been tuned against
patterns you copied. Work only from this document and the public spec
(`PREREGISTRERING.md`, `facit/KATEGORIER.md`, `facit/SCHEMA.md`). If you have
already seen the development set, you are not the right author for v2 — tell
Carl.

## What you produce

50 JSON files, one conversation each, written to a **private folder outside this
repo** (default `~/memory-fidelity-bench-private/dold-v2/`, or wherever Carl
points you). You never commit the conversation files. Carl runs `frys_dold.py`,
which commits only a SHA-256 manifest of your files. The conversations are
published later, after the single benchmark run — so the manifest proves the set
was fixed in advance, and publication proves nobody altered it afterwards.

File naming: `d001-<category>.json` … `d050-<category>.json`. Only `a-z 0-9 - _`
in filenames. Use the exact category identifiers from the list below.

## The question being tested

Does the memory layer store what the user **actually said** — verbatim, with the
right polarity (negation preserved), the right speaker (user / assistant / third
party), the right modality (factual / intended / hypothetical), and the right
time — and abstain from storing what it shouldn't (hypotheticals, injections,
other people's words, ambiguous references)?

## The 17 categories (use these exact identifiers)

`negation`, `hypotetisk`, `avsikt`, `annans-rost`, `assistentens-ord`, `ironi`,
`tid-manadsskifte`, `tid-arsskifte`, `relativ-tid`, `flera-fakta`,
`inget-att-spara`, `injektion`, `motsagelse`, `korrigering`, `villkorlig`,
`kvantitet-enhet`, `tvetydig-referens`. Each is explained in
`facit/KATEGORIER.md`.

## The facit (ground-truth) schema

```json
{
  "id": "d001-negation",
  "sprak": "sv" | "en",
  "doman": "halsa" | "vardag",
  "samtalsdatum": "2026-10-30",
  "meddelanden": [ {"roll": "user" | "assistant" | "third", "text": "..."} ],
  "ska_sparas": [
    {
      "citat": "<EXACT substring of a user message>",
      "typ": "intention" | "handelse" | "sjalvbild",
      "polaritet": "bekraftad" | "negerad",
      "modalitet": "faktisk" | "avsedd" | "hypotetisk" | "annans_rost",
      "tid": "2026-08-31" | null,
      "talare": "user"
    }
  ],
  "ska_ej_sparas": [ {"amne": "<short>", "skal": "<why it must not be stored>"} ]
}
```

## The invariant you must not break

**Every `citat` in `ska_sparas` must be an exact, character-for-character
substring of some user message in the same conversation.** Copy it, do not
paraphrase. A quote that is not a verbatim substring makes the ground truth
itself a fabrication — the one thing this benchmark exists to catch. Validate
this yourself (script below) before handing over.

`samtalsdatum` is always `2026-10-30`; resolve all relative/boundary times
against it (e.g. "i tisdags" → 2026-10-27, "sista augusti" → 2026-08-31,
"i julas" → 2025-12, "in two weeks" → 2026-11-13).

## Distribution requirements (the set must hit all of these)

- **50 conversations**, ids d001–d050.
- **~2/3 health (`halsa`), ~1/3 everyday (`vardag`)** — aim for 33 health, 17
  everyday. Health is the focus (allergies, medications, doses, symptoms, what
  the doctor/nurse said vs what the patient believes); everyday is the control
  (work, travel, family, food, habits).
- **All 17 categories appear in BOTH domains.** That is 34 slots just for
  coverage; the rest fill the ratio.
- **At least a third (≥ 17) are 6–12 messages long**, with the important
  statement in the **middle** of the conversation, surrounded by ordinary
  filler turns. A memory layer should not get fidelity for free just because
  the key fact was the only thing said.
- **Bilingual:** roughly 60% Swedish, 40% English. Swedish negation and time
  expressions are a deliberately harder test.
- **Include the serious medical error cases** (see below) in several health
  conversations.

## Make it hard — this is the hidden set

The development set probes the easy version of each trap. Yours should probe the
edges. Combine traps: negation + time, a multi-fact utterance where one fact is
hypothetical, an allergy stated by a third party ("my sister is allergic, I'm
not"), a correction buried mid-conversation, a dose mentioned then superseded.
If a weak memory layer would plausibly get the easy case right but your case
wrong, you have written a good hidden case.

## Serious errors (what makes a memory dangerous)

A stored entry that commits any of these is a *serious* error:
- **Negation flipped** (polarity inverted).
- **Someone else's words stored as the user's.**
- **Fabricated content** (quote not a substring).
- **Wrong medication, dose or allergy** — in a health context, naming the wrong
  drug, the wrong dose, or inverting an allergy ("allergic to penicillin" stored
  as tolerated). Write several conversations where a careless memory layer would
  make exactly this error, and mark the dangerous reading clearly in
  `ska_ej_sparas` with "ALLVARLIGT FEL" and why.

Categories like `hypotetisk`, `injektion`, `inget-att-spara` and
`tvetydig-referens` often have an **empty** `ska_sparas` (and a `ska_ej_sparas`
entry explaining what must not be stored).

## Validate before handing over

Run this against your private folder. It must print "OK".

```python
import json, re
from pathlib import Path
from collections import Counter
D = Path.home() / "memory-fidelity-bench-private" / "dold-v2"
TYP={"intention","handelse","sjalvbild"}; POL={"bekraftad","negerad"}
MOD={"faktisk","avsedd","hypotetisk","annans_rost"}
fel=[]; kat=Counter(); dom=Counter(); par=Counter(); langa=0
for f in sorted(D.glob("*.json")):
    s=json.load(open(f))
    if re.search(r"[^a-z0-9_.-]", f.name): fel.append(f"filename {f.name}")
    kat[s["kategori"]]+=1; dom[s["doman"]]+=1; par[(s["kategori"],s["doman"])]+=1
    if len(s["meddelanden"])>=6: langa+=1
    ut=" \n ".join(m["text"] for m in s["meddelanden"] if m["roll"]=="user")
    for p in s["ska_sparas"]:
        if p["citat"] not in ut: fel.append(f"{f.name}: citat not a substring")
        if p["typ"] not in TYP or p["polaritet"] not in POL or p["modalitet"] not in MOD:
            fel.append(f"{f.name}: enum")
bada=sum(1 for k in kat if par.get((k,"halsa")) and par.get((k,"vardag")))
print("files", sum(kat.values()), "| health", dom["halsa"], "everyday", dom["vardag"],
      "| long", langa, "| both-domain cats", f"{bada}/17")
print("OK" if not fel and sum(kat.values())==50 and len(kat)==17 and bada==17 and langa>=17 else ("PROBLEMS: "+"; ".join(fel)))
```

## Handoff

1. You write 50 files to the private folder and your validator prints OK.
2. You tell Carl it's ready. You do **not** push anything.
3. Carl runs `python rigg/frys_dold.py`, which commits only
   `DOLD_MANIFEST_V2.sha256` (the hashes). The conversations stay private.
4. The set is run exactly once (Phase 3). Afterwards the conversations are
   published, and anyone can check them against the already-committed manifest.

If anything in this instruction is ambiguous, ask Carl before writing — never by
looking at the development set.
