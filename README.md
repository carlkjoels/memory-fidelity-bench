# memory-fidelity-bench

En oberoende benchmark för **minnets trohet** i agentminne: sparar minneslagret
det användaren faktiskt sa — ordagrant, med rätt polaritet, talare, modalitet
och tid — och avstår det som inte borde sparas?

Trohet, inte återkallning. LongMemEval och LoCoMo frågar om systemet kan hämta
rätt svar. Den här frågar något före det: om det som lades i minnet stämmer med
vad som sades. Ett system kan ha perfekt recall på en förvanskad post.

**Status:** förregistrering (se `PREREGISTRERING.md`, låst 2026-10-30). Ingen
kod körd, inga resultat, inga system installerade än. Allt syntetiskt.

## Struktur

- `PREREGISTRERING.md` — frågan, måtten, trösklarna, nedläggningskriteriet, låst.
- `facit/KATEGORIER.md` + `facit/SCHEMA.md` — de 17 fällorna och facit-formatet.
- `facit/utveckling/` — öppna testsamtal (bygg och felsök riggen här).
- `facit/dold/` — frysta, körs en gång i slutet (FAS 3).
- `adaptrar/` — en per minneslager (Mem0, Hindsight, Graphiti, Letta). Byggs i
  FAS 3; licenser verifieras och skrivs här innan dess.
- `rigg/` — matning, dumpning, mekanisk jämförelse mot facit.

## Regler

- Inga resultat publiceras före kommentarsvecka för Mem0 och Vectorize.
- Ton: fynd, inte omdömen. Inga rankningar utan konfidensintervall.
- Metoden låstes före koden; versionerna låses i FAS 3 före den dolda uppsättningen.
