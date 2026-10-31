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

This is a fidelity benchmark. Most memory benchmarks (LongMemEval, LoCoMo,
MemBench, MemoryAgentBench, STALE) score the final *answer*. **HaluMem is prior
art that already scores the stored layer** — so this benchmark is not first to
measure storage. Its contribution is narrower and specific: scoring each
dimension separately (verbatimness, polarity, speaker, modality, time, recall),
in Swedish and health-adjacent cases, with the vendor disclosed, and with test
cases adapted from real user issues. We also report recall, because a system
can be faithful about the little it stores and still omit most of what was said.

**Conflict of interest (disclosed):** the author of this benchmark builds
Selvra, an adjacent memory layer. Selvra's own memory layer will be tested under
exactly these rules once it exists. This is an open, pre-registered benchmark —
not a claim of neutrality. (We hold HaluMem, DolphinBench and vendor benchmarks
to the same disclosure standard.)

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

## Verbatimness is a property, not an error (revised 2026-10-30, see changelog)

Several memory layers paraphrase the user's words into "facts" by design. A
measure that counted paraphrase as fabrication would score those systems ~100%
wrong regardless of whether the content is faithful — the benchmark would then
rank design choices, not fidelity, and the shutdown criterion below could never
trigger. So:

- **Verbatimness** (is the stored text an exact substring of a user message?) is
  reported as a **descriptive per-system property**, never counted as an error.
  A system that stores raw text and one that paraphrases are simply described as
  such.
- **Confabulation** (a serious error) is redefined: a stored entry whose content
  is **not supported by any user message** in the ground truth. Checked
  deterministically by substring first; where the text is a faithful paraphrase
  (no verbatim match) an **entailment judge** decides, validated against
  hand-labelled cases. This is the HaluMem approach, but scored per dimension.

## Serious errors (the ones that make a memory dangerous)

- **Negation flipped:** polarity inverted against the ground truth.
- **Someone else's words as the user's:** speaker wrong in a way that attributes
  to the user something they did not say.
- **Confabulation:** stored content not supported by any user message (per the
  entailment-aware definition above — not mere paraphrase).
- **Wrong medication, dose or allergy:** in a health context, a stored entry
  that names the wrong drug, the wrong dose, or inverts an allergy
  ("allergic to penicillin" stored as tolerated, or vice versa). A fidelity
  error here can harm, so it is serious regardless of category.

Minor errors (modality or time nuance) are reported separately and never counted
as serious.

## Superseded values: a serious error only if stored as current (revised 2026-10-31, see changelog)

When a later message supersedes or corrects an earlier one (categories
`motsagelse` and `korrigering`), the `ska_ej_sparas` entry names the OLD value.
It is a **serious error only if the system presents it as current/active**. A
system that keeps the old value but marks it superseded and linked — dumped with
`aktiv: false` and `ersatt_av` — is **recorded in the contradiction taxonomy
("keeps both, linked"), not scored as a serious error.** This is the behaviour of
Graphiti (edge invalidation) and Mem0's graph variant (linked memories), not only
Selvra; the rule is general, stated so no single system is advantaged by it.

Consequently: to be scored on the **active view**, an adapter MUST dump each
entry with `aktiv` and `ersatt_av`. A system that cannot express "superseded" is
scored on everything it returns as current — keeping a replaced value visible as
current is then exactly the serious error that matters (see Mem0 issue reports of
replaced values still retrieved as current).

## Scoring

- Verbatimness and abstention: deterministic (substring check; set comparison
  against ground truth).
- Confabulation, polarity, speaker, modality, time: deterministic where the
  ground truth is unambiguous; **an LLM judge only where it must be used**
  (paraphrase/entailment), and then checked against hand-labelled cases (the
  judge is never the same model the memory layer uses, and its agreement with
  the hand labels is reported).
- **Omission / recall:** for every item the ground truth says should be stored,
  did the system store something that entails it? Reported as recall. A system
  that stores little scores low here even if what it stores is faithful.
- **Matching (entry → ground-truth item):** an entry matches a `ska_sparas` item
  if it **contains or entails** it — never by exact-string equality. The ground
  truth may quote a short span ("tre gånger") while a faithful system stores the
  whole clause ("Jag tar tabletten tre gånger"); one ground-truth item may be
  satisfied by one entry (one-to-many). Containment is checked first, the
  entailment judge only where there is no verbatim overlap.
- **Role `third`:** a message spoken by a third party (`roll: "third"`) can never
  yield a `sagt`/user entry. Storing a `third` message as the user's own is the
  speaker serious error, the same as assistant content phrased as the user's.
- **Every measure is also reported per domain** (health vs everyday) and, where
  it matters, per category.

## Thresholds and shutdown criterion (revised 2026-10-30, see changelog)

Two failure modes, both reported:

- **Serious-error rate** per system (negation flip, speaker-as-user,
  confabulation, wrong med/dose/allergy) — paraphrase is NOT in this set.
- **Recall** per system against `ska_sparas`.

Denominators are stated explicitly and reported side by side: serious-error rate
is **per stored entry** and **per ground-truth item** (a system is matched
one-to-many where it splits an utterance into several entries); recall is **per
ground-truth item**.

- A system "has a fidelity problem" at **≥ 1% serious errors** OR materially low
  recall (threshold fixed in Phase 3 against the no-op and raw-store baselines).
- **Shutdown / null result:** declared only if ALL systems are clean on serious
  errors **and** none shows a recall problem — so a system that stores nothing
  cannot produce a null result, because it fails on recall. Written in advance.
- **A clean run is an upper bound, never a guarantee (added 2026-10-31).** With
  the hidden set's size (50 conversations, a few ground-truth items each), zero
  observed serious errors is reported as *"none observed; upper 95% bound X%"*
  (Wilson, or the rule of three: ≈3/n), **never** as "< 1%". Showing a serious-
  error rate below 1% at 95% confidence needs roughly **300 error-free items**.
  The hidden set can therefore *fail* a system (one error among ~100 entries is
  already ≥1%) but cannot statistically *acquit* one. Result text says "none
  observed" with the bound, not a point claim.

## Test data (Phase 2)

151 synthetic conversations, Swedish and English, 17 categories (see
`facit/KATEGORIER.md`). Each conversation has ground truth in JSON: exactly what
should be stored and what should not.

- **Development:** 101 conversations (`facit/utveckling/`), open, used to build
  and debug the rig. (Was 100; one `third`-role case added 2026-10-31, see
  changelog.)
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

- No results are published before a comment week for ALL evaluated systems'
  authors — Mem0, Vectorize (Hindsight), Zep (Graphiti) and Letta — not only the
  two originally named. They respond before publication (responsible disclosure).
- Tone: dry and factual. Findings, not judgements. No superlatives, no rankings
  without confidence intervals.
- Everything synthetic. No REAL health data, no real-person data, no Selvra
  history. Synthetic health-adjacent cases ("the doctor said…") are part of the
  contribution. The only private artefact is hidden set v2 before its single
  run; its manifest is public.

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
  from the private path. The external author follows AUTHORING-HIDDEN-V2.md.
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
- 2026-10-30: **External review acted on (validity fixes).** (a) Verbatimness is
  now a descriptive property, never an error; confabulation redefined as content
  not supported by any user message (substring, then entailment judge) — so the
  bench measures fidelity, not design choice. (b) Added a recall/omission
  measure against `ska_sparas` with explicit denominators. (c) Shutdown
  criterion rewritten so it can trigger and a store-nothing system cannot pass
  (it fails on recall). (d) Novelty stated against HaluMem, not as "first".
  (e) Comment week extended to all four systems' authors. (f) Conflict of
  interest (Selvra) disclosed in the preregistration. (g) "No health data" →
  "no REAL health data".
- 2026-10-30: **Deferred to before Phase 3 (planned, not yet built), logged so
  they are not silent):** multi-session schema with per-message time and a
  per-session expected-state (for contradiction/supersede cases); backdated and
  varied `samtalsdatum` injected via each system's own time API; locked
  per-system modes and baselines (Mem0 infer=True/False, Hindsight
  standard/verbatim, a raw-store no-op baseline, a Letta variant with a fixed
  agent prompt, possibly LangMem); a speaker rule (assistant content correctly
  attributed is not a serious error; assistant content phrased as the user's own
  claim is); and a SEPARATE frozen set (dold-B, own manifest) for test cases
  adapted from real public issues — the existing 50 hidden files stay untouched.
  NOTE: claims in the external review about other systems' internals (commits,
  issue numbers, line references) are NOT encoded here as fact; they are the
  reviewer's, unverified by this project, and are only used to motivate case
  *shapes* — never asserted as another system's behaviour in public output.
- 2026-10-31: **Superseded-value scoring made explicit, matching stated, clean
  run reported as a bound.** (a) A `ska_ej_sparas` entry in `motsagelse` and
  `korrigering` is a serious error **only if stored as current/active**; a value
  kept superseded and linked (`aktiv=false`, `ersatt_av`) is logged in the
  contradiction taxonomy, not scored as a serious error. u037 and u040 reworded
  to this conditional form (generator + regenerated facit). (b) Entry→ground-
  truth matching is **contains/entails**, not exact equality. (c) Role `third`
  can never become a `sagt`/user entry; a `third`-role development case added
  (set 100 → 101, within u001–u101). (d) A clean hidden-set run is reported as
  an upper 95% bound ("none observed"), never "< 1%": the set can fail but not
  acquit. This change **advantages every link/invalidate system (Graphiti,
  Mem0's graph variant), not only Selvra** — motivated generally and stated with
  the conflict of interest. **Locked 2026-10-31, before any system is run.**
  **Status: awaiting external read before it is treated as binding** (the author
  builds Selvra and benefits from this change; an outside reader checks it first).
