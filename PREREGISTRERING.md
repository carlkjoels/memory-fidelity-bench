# Pre-registration: memory-fidelity-bench

**Dated:** 2026-10-30. Locked before any run. Changes after this date are
recorded in a changelog at the end, never by silent edit (the same rule as
`benchmark/PROTOKOLL.md` in the selvra-analysis project).

## The question

Does an agent memory layer store what the user **actually said** — verbatim,
with the right polarity (negation preserved), the right speaker, the right
modality (factual / intended / hypothetical) and the right time — and abstain
from storing what it shouldn't?

This is a fidelity benchmark, not a recall benchmark. LongMemEval and LoCoMo
measure whether a system can *retrieve* the right answer after thousands of
messages. We measure something upstream: whether what was placed in memory
matches what was said at all. A system can have perfect recall of a corrupted
memory entry.

## Systems and versions

Four self-hosted, open memory layers. No cloud service. Licence is verified and
recorded in the README before the adapter is built.

| system | licence (to verify) | version |
|---|---|---|
| Mem0 (OSS) | Apache-2.0 (verify) | **pinned in Phase 3, logged per run** |
| Hindsight | MIT (verify) | pinned in Phase 3 |
| Graphiti | verify | pinned in Phase 3 |
| Letta | verify | pinned in Phase 3 |

Versions cannot be pinned today without installing the systems. Therefore: the
exact version, commit hash and configuration are **frozen and committed in
Phase 3 before the hidden set runs** — that is the binding point, mirrored from
PROTOKOLL's "frozen ground truth before results". The pre-registration binds the
*method*; Phase 3 binds the *versions*.

## The model

The same language model and the same settings for ALL systems — we measure the
memory, not the model. Model, temperature and every parameter are logged per
run. The model is pinned in Phase 3 together with the system versions.

## Measures (per stored memory entry)

1. **citat (quote)** — does the content appear verbatim as a substring of the
   conversation? (deterministic check, 100% mechanical)
2. **polaritet (polarity)** — is negation preserved? ("I don't drink coffee"
   must never become "drinks coffee")
3. **talare (speaker)** — is the entry attributed to the right voice? (user /
   assistant / third party)
4. **modalitet (modality)** — factual / intended / hypothetical, classified right?
5. **tid (time)** — is the time expression resolved to the right date?
6. **avstående (abstention)** — was something stored that should NOT have been?
   (false entry)
7. **motsägelse (contradiction)** — when new info contradicts old: is the old
   deleted, overwritten, or are both kept? (recorded, not scored as an error in
   itself — we report the behaviour)

## Serious errors (the three that make a memory dangerous)

- **Negation flipped:** polarity inverted against the ground truth.
- **Someone else's words as the user's:** speaker wrong in a way that attributes
  to the user something they did not say.
- **Fabricated content:** a stored entry whose quote is not a substring of the
  conversation (confabulation).

Minor errors (modality or time nuance) are reported separately and never counted
as serious.

## Scoring

- Quote and abstention: deterministic (exact substring, set comparison against
  ground truth).
- Polarity, speaker, modality, time: deterministic where the ground truth is
  unambiguous; **an LLM judge only where it must be used**, and then checked
  against hand-labelled cases (the judge is never the same model the memory
  layer uses, and its agreement with the hand labels is reported).

## Thresholds and shutdown criterion (locked 2026-10-30)

- **Shutdown:** if ALL four systems have **under 1% serious errors** on the
  hidden set, there is no story — the project is shut down and reported as a
  null result. Written in advance.
- A system is deemed to "have a fidelity problem" at ≥ 1% serious errors.
- Minor errors have no threshold; they are described, not judged.

## Test data (Phase 2)

150 synthetic conversations, Swedish and English, 17 categories (see
`facit/KATEGORIER.md`). Each conversation has ground truth in JSON: exactly what
should be stored and what should not.

- **Development:** 100 conversations (`facit/utveckling/`), open, used to build
  and debug the rig.
- **Hidden:** 50 conversations (`facit/dold/`), **frozen with a SHA-256
  manifest, run exactly once at the end.** Fixing the rig after the hidden set
  has run invalidates it — a new hidden set is required. (The PROTOKOLL rule.)

**Dependency, noted honestly:** the 17 categories in this version are derived
from the measures and the known dialogue-layer categories (negation,
hypothetical, third-party voice, irony, time across month/year boundaries,
multiple facts per line, nothing to extract, injection, etc.). They are
reconciled against `reports/Dialoglager för Selvra.md` when that file exists; if
it differs, `KATEGORIER.md` is adjusted *before* Phase 3, never after the hidden
set has run.

## Test rig (Phase 3)

Feed each conversation, dump everything the system stored, compare mechanically
against the ground truth. Log version, model, date and cost per run. Determinism
where possible, LLM judge only where it must be used (with a hand-label check).

## Calibration (Phase 4)

Reproduce a small part of LongMemEval or LoCoMo with each system and compare to
their published numbers. A large discrepancy → debug the rig before any fidelity
result is taken seriously. The rig must first show it can reproduce known
numbers.

## Rules

- No results are published before a comment week for Mem0 and Vectorize (the
  system authors get to respond before publication — responsible disclosure).
- Tone: dry and factual. Findings, not judgements. No superlatives, no rankings
  without confidence intervals.
- Everything synthetic. No health data, no Selvra history, nothing private.

## Changelog

- 2026-10-30: First version, locked.
- 2026-10-30: Framing documents and code translated to English; identifiers,
  conversation utterances (bilingual by design) and the frozen hidden set left
  unchanged.
