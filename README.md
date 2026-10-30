# memory-fidelity-bench

> **A serrier benchmark.** serrier and Selvra share the same founder. Selvra's
> own memory layer will be tested under exactly these rules once it exists.
> This is an **open, pre-registered** benchmark — not a claim of neutrality.

An open, pre-registered benchmark for **memory fidelity** in agent memory: does the
memory layer store what the user **actually said** — verbatim, with the right
polarity, speaker, modality and time — and abstain from storing what it
shouldn't?

Fidelity, not recall. LongMemEval and LoCoMo ask whether a system can *retrieve*
the right answer after thousands of messages. This asks something upstream:
whether what was put into memory matches what was said at all. A system can have
perfect recall of a corrupted memory.

**Status:** pre-registration (see `PREREGISTRERING.md`, locked 2026-10-30). No
code run, no results, no systems installed yet. Everything is synthetic.

## Why the test data is bilingual (by design, not an oversight)

The conversations are Swedish and English on purpose. Most memory layers are
trained predominantly on English, and Swedish negation and time expressions
("i julas", "sista augusti") are a harder test of fidelity. A system that
preserves negation and resolves dates correctly in English but not in Swedish
has a fidelity gap worth measuring. The **framing documents and code are in
English**; the **conversation utterances stay in their original language**
because translating them would destroy the cross-lingual test. Facit
annotation fields (`skal`, `amne`) are kept in Swedish internally and are
explained by these English docs; the hidden set's annotations are frozen in
the SHA-256 manifest and must not be edited.

## Layout

- `PREREGISTRERING.md` — the question, measures, thresholds, shutdown criterion; locked.
- `facit/KATEGORIER.md` + `facit/SCHEMA.md` — the 17 traps and the facit format.
- `facit/utveckling/` — open development conversations (build and debug the rig here).
- `DOLD_MANIFEST_V2.sha256` — SHA-256 of every hidden-set-v2 file. The files
  themselves live in a private path outside the repo and are published only
  after the single run. (Hidden set v1 was committed here and is spent; see the
  changelog in PREREGISTRERING.md.)
- `adaptrar/` — one per memory layer (Mem0, Hindsight, Graphiti, Letta). Built in
  Phase 3; licences verified and recorded here first.
- `rigg/` — feeding, dumping, mechanical comparison against facit.

Swedish directory and field names (`facit` = ground truth, `utveckling` =
development, `dold` = hidden, `rigg` = rig, `skal` = reason) are kept as stable
identifiers; this README is the key.

## Rules

- No results published before a comment week for Mem0 and Vectorize.
- Tone: findings, not judgements. No rankings without confidence intervals.
- The method was locked before the code; versions are locked in Phase 3 before
  the hidden set runs.
