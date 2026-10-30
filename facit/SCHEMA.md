# Facit-schema

Ett samtal = en JSON-fil i facit/utveckling/ eller facit/dold/.

```
{
  "id": "u001",                         # u = utveckling, d = dold
  "sprak": "sv" | "en",
  "kategori": "<en av de 17>",
  "samtalsdatum": "2026-10-30",         # "idag" för relativa tidsuttryck
  "meddelanden": [
    {"roll": "user" | "assistant" | "third", "text": "..."}
  ],
  "ska_sparas": [
    {
      "citat": "<exakt delsträng av något user-meddelande>",
      "typ": "intention" | "handelse" | "sjalvbild",
      "polaritet": "bekraftad" | "negerad",
      "modalitet": "faktisk" | "avsedd" | "hypotetisk" | "annans_rost",
      "tid": "2026-08-31" | null,
      "talare": "user"
    }
  ],
  "ska_ej_sparas": [
    {"amne": "<kort beskrivning>", "skal": "<varför det inte får sparas>"}
  ]
}
```

citat är ALLTID en exakt delsträng — en post vars citat inte finns ordagrant
i samtalet är per definition konfabulation (allvarligt fel).
