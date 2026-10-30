# Pre-registration: memory-fidelity-bench

> **A serrier benchmark.** serrier and Selvra share the same founder. Selvra's
> own memory layer will be tested under exactly these rules once it exists.
> This is an **open, pre-registered** benchmark — not a claim of neutrality.


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

## Serious errors (the ones that make a memory dangerous)

- **Negation flipped:** polarity inverted against the ground truth.
- **Someone else's words as the user's:** speaker wrong in a way that attributes
  to the user something they did not say.
- **Fabricated content:** a stored entry whose quote is not a substring of the
  conversation (confabulation).

- **Wrong medication, dose or allergy:** in a health context, a stored entry
  that names the wrong drug, the wrong dose, or inverts an allergy
  ("allergic to penicillin" stored as tolerated, or vice versa). A fidelity
  error here can harm, so it is serious regardless of category.

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
- **Hidden (v2):** 50 conversations authored by an external person, kept in a
  **private path outside this repo**. Only the SHA-256 manifest
  (`DOLD_MANIFEST_V2.sha256`) is committed publicly, in advance; the
  conversation files are published only AFTER the single run. The manifest
  proves the set was fixed before results; publication proves it was unaltered.
  Fixing the rig after the hidden set has run invalidates it — a new hidden set
  is required. (The PROTOKOLL rule.) Hidden set v1 is spent (see changelog).

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
- Everything synthetic. No real-person data, no Selvra history. The only
  private artefact is hidden set v2 before its single run; its manifest is public.

## Changelog

- 2026-10-30: First version, locked.
- 2026-10-30: Framing documents and code translated to English; identifiers,
  conversation utterances (bilingual by design) and the frozen hidden set left
  unchanged.
- 2026-10-30: **Hidden set v1 is SPENT.** It was committed to this public repo
  (`facit/dold/`, 50 files, manifest `DOLD_MANIFEST.sha256`) and is therefore
  known — a published hidden set can never be a blind test again (the PROTOKOLL
  rule: a hidden set the system-under-test or its authors could have seen is no
  longer hidden). `facit/dold/` is removed from the repo. The v1 manifest is
  kept in git history as the honest record that it existed and was retired.
- 2026-10-30: **Hidden set v2 protocol.** v2 is authored by an external person,
  kept in a private path OUTSIDE this repo, and only its SHA-256 manifest is
  committed publicly (`DOLD_MANIFEST_V2.sha256`). The conversation files are
  published only AFTER the single run — so the manifest proves the set was fixed
  in advance, and publication proves it was not altered. `frys_dold.py` reads
  from the private path.
- 2026-10-30: Health niche added via this changelog — test conversations cover
  allergies, medications, doses, symptoms, what the doctor said and what the
  patient believes. A fourth serious error is added: **wrong medication, dose or
  allergy** (a fidelity error here can harm).
- 2026-10-30: Filenames restricted to `a-z 0-9 - _`; one spelling per category.
- 2026-10-30: At least a third of the development cases are 6–12 messages long,
  with the important statement in the middle of the conversation.
- 2026-10-30: **Two domains, reported separately.** Conversations are ~2/3
  health (allergies, medications, doses, symptoms, what the doctor said vs what
  the patient believes) and ~1/3 everyday (the control). Every measure is
  reported per domain, so "are fidelity errors more common in health
  conversations than everyday ones?" is a finding in its own right. Each
  conversation carries a `doman` field ("halsa" | "vardag"). The same 2/3–1/3
  split applies to hidden set v2. All 17 categories appear in BOTH domains.
- 2026-10-30: Development set reworked in place within u001–u100 (open set,
  rework permitted and logged): ~35 short cases converted to 6–12-message
  conversations with the key statement mid-conversation; health woven in to the
  2/3 ratio; the generator remains the single reproducible source.
