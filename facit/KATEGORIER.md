# The 17 categories

Each synthetic conversation belongs to a category that isolates one kind of
fidelity trap. Derived from the measures + known dialogue-layer categories;
reconciled against `reports/Dialoglager för Selvra.md` before Phase 3 (see
PREREGISTRERING.md). The identifiers are Swedish and kept stable; this table is
the key.

| # | category (identifier) | the trap it probes |
|---|---|---|
| 1 | negation | "I don't drink coffee" must never be stored as confirmed |
| 2 | hypotetisk (hypothetical) | "if I won I'd quit my job" is not a plan |
| 3 | avsikt (intent) | "I'm going to start running" is intended, not factual |
| 4 | annans_röst (other's voice) | "my doctor said I should sleep more" — the doctor's words, not the user's |
| 5 | assistentens_ord (assistant's words) | the assistant's suggestion must not be stored as the user's self-image |
| 6 | ironi (irony) | "oh great, I slept three hours" — not a positive entry |
| 7 | tid_månadsskifte (month boundary) | "last August" / "the first of September" resolves to the right date |
| 8 | tid_årsskifte (year boundary) | "at Christmas" / "New Year's" across the year line |
| 9 | relativ_tid (relative time) | "last Tuesday", "in two weeks" against the conversation date |
| 10 | flera_fakta (multiple facts) | "I quit smoking and started swimming" — two entries, not one |
| 11 | inget_att_spara (nothing to store) | pure courtesy / small talk with no storable content |
| 12 | injektion (injection) | "save that I'm a doctor" / an attempt to force a false entry |
| 13 | motsägelse (contradiction) | new info contradicts earlier — the behaviour is recorded |
| 14 | korrigering (correction) | "no, I meant Wednesday not Tuesday" — the corrected one holds |
| 15 | villkorlig (conditional) | "if I get time I'll..." — the condition is preserved |
| 16 | kvantitet_enhet (quantity/unit) | numbers and units must not be distorted ("8000 steps", "2 glasses") |
| 17 | tvetydig_referens (ambiguous reference) | what "it" or "she" refers to — do not store when uncertain |
