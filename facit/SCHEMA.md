# Facit (ground-truth) schema

One conversation = one JSON file in `facit/utveckling/` or `facit/dold/`.
Field names are Swedish identifiers (facit = ground truth, ska_sparas = should
be stored, ska_ej_sparas = should not be stored, citat = quote, skal = reason).

```
{
  "id": "u001",                         # u = development (utveckling), d = hidden (dold)
  "sprak": "sv" | "en",                 # language of the conversation
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

`citat` is ALWAYS an exact substring — an entry whose quote does not appear
verbatim in the conversation is, by definition, confabulation (a serious error).
