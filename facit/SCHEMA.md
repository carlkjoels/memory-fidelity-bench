# Facit (ground-truth) schema

One conversation = one JSON file in `facit/utveckling/` or `facit/dold/`.
Field names are Swedish identifiers (facit = ground truth, ska_sparas = should
be stored, ska_ej_sparas = should not be stored, citat = quote, skal = reason).

```
{
  "id": "u001",                         # u = development (utveckling), d = hidden (dold)
  "sprak": "sv" | "en",                 # language of the conversation
  "doman": "halsa" | "vardag",         # domain: health (focus) | everyday (control)
  "kategori": "<one of the 17>",
  "samtalsdatum": "2026-10-30",         # "today" for relative time expressions
  "meddelanden": [                      # messages
    {"roll": "user" | "assistant" | "third", "text": "..."}
  ],
  "ska_sparas": [                       # what SHOULD be stored
    {
      "citat": "<exact substring of some user message>",
      "typ": "intention" | "handelse" | "sjalvbild",   # intent | event | self-image
      "polaritet": "bekraftad" | "negerad",            # confirmed | negated
      "modalitet": "faktisk" | "avsedd" | "hypotetisk" | "annans_rost",
      "tid": "2026-08-31" | null,       # resolved date, or null
      "talare": "user"
    }
  ],
  "ska_ej_sparas": [                    # what should NOT be stored
    {"amne": "<short topic>", "skal": "<why it must not be stored>"}
  ]
}
```

`citat` in the ground truth is ALWAYS an exact substring (otherwise the ground
truth itself would be fabrication). Note for scoring: a *system's* stored entry
is NOT penalised merely for paraphrasing — verbatimness is reported descriptively.
Confabulation (a serious error) means stored content not supported by any user
message (substring check first, entailment judge otherwise). See PREREGISTRERING.md.

**Matching** a system entry to a `ska_sparas` item is by *contains/entails*,
never exact equality: the ground-truth `citat` may be a short span ("tre gånger")
while a faithful system stores the whole clause.

**Superseded values.** For `motsagelse` and `korrigering`, the `ska_ej_sparas`
entry is the OLD value. It is a serious error **only if stored as current**. To
be scored on the active view, an adapter dumps each entry with `aktiv:
true|false` and `ersatt_av: <id|null>`; a value kept superseded and linked is
contradiction behaviour, not a serious error. See PREREGISTRERING.md.

**Role `third`.** A message with `"roll": "third"` is a third party speaking in
the transcript. Its content must never be stored as the user's own (`talare:
user`); doing so is the speaker serious error.
