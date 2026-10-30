# Förregistrering: memory-fidelity-bench

**Daterad:** 2026-10-30. Låst före all körning. Ändringar efter detta datum
loggas i en ändringslogg sist, aldrig genom tyst redigering (samma regel som
benchmark/PROTOKOLL.md i selvra-analysis).

## Frågan

Sparar ett agentminneslager det användaren **faktiskt sa** — ordagrant, med
rätt polaritet, rätt talare, rätt modalitet och rätt tid — och avstår det som
inte borde sparas?

Detta är en trohets-benchmark (fidelity), inte en återkallnings-benchmark
(recall). LongMemEval och LoCoMo mäter om systemet kan *hämta* rätt svar efter
tusentals meddelanden. Vi mäter något före det: om det som lades i minnet över
huvud taget stämmer med vad som sades. Ett system kan ha perfekt recall på en
förvanskad minnespost.

## System och versioner

Fyra självhostade, öppna minneslager. Ingen molntjänst. Licens kontrolleras och
skrivs i README innan adaptern byggs.

| system | licens (verifieras) | version |
|---|---|---|
| Mem0 (OSS) | Apache-2.0 (verifieras) | **pinnas i FAS 3, loggas per körning** |
| Hindsight | MIT (verifieras) | pinnas i FAS 3 |
| Graphiti | verifieras | pinnas i FAS 3 |
| Letta | verifieras | pinnas i FAS 3 |

Versionerna kan inte pinnas i dag utan att installera systemen. Därför: exakt
version, commit-hash och konfiguration **fryses och committas i FAS 3 innan den
dolda uppsättningen körs** — det är den bindande punkten, speglad från
PROTOKOLL:s "fruset facit före resultat". Förregistreringen binder *metoden*;
FAS 3 binder *versionerna*.

## Modellen

Samma språkmodell och samma inställningar för ALLA system — vi mäter minnet,
inte modellen. Modell, temperatur och alla parametrar loggas per körning.
Modellen pinnas i FAS 3 tillsammans med systemversionerna.

## Måtten (per sparad minnespost)

1. **citat** — finns innehållet ordagrant som delsträng i samtalet?
   (deterministisk kontroll, 100 % mekanisk)
2. **polaritet** — är negation bevarad? ("jag dricker inte kaffe" får aldrig
   bli "dricker kaffe")
3. **talare** — tillskrivs posten rätt röst? (användaren / assistenten / tredje
   part)
4. **modalitet** — faktisk / avsedd / hypotetisk, rätt klassad?
5. **tid** — är tidsuttrycket rätt upplöst till datum?
6. **avstående** — sparades något som INTE borde sparas? (falsk post)
7. **motsägelse** — vid ny info som motsäger gammal: raderas det gamla, skrivs
   det över, eller sparas båda? (registreras, inte poängsätts som fel i sig —
   vi rapporterar beteendet)

## Allvarliga fel (de tre som gör ett minne farligt)

- **Negation vänd:** polariteten omkastad mot facit.
- **Annans ord som användarens:** talare fel på ett sätt som tillskriver
  användaren något hen inte sa.
- **Påhittat innehåll:** en sparad post vars citat inte är en delsträng av
  samtalet (konfabulation).

Lätta fel (modalitet- eller tidsnyans) rapporteras separat och räknas aldrig
som allvarliga.

## Måttens poängsättning

- Citat och avstående: deterministiskt (exakt delsträng, mängdjämförelse mot
  facit).
- Polaritet, talare, modalitet, tid: deterministiskt där facit är entydigt;
  **LLM-domare endast där det måste**, och då med en kontroll mot handmärkta
  fall (domaren får aldrig vara samma modell som minneslagret använder, och
  dess träffsäkerhet mot handmärkningen rapporteras).

## Trösklar och nedläggningskriterium (låsta 2026-10-30)

- **Nedläggning:** om ALLA fyra system har **under 1 % allvarliga fel** på den
  dolda uppsättningen finns ingen historia — projektet läggs ner och det
  rapporteras som ett nollresultat. Skrivet i förväg.
- Ett system räknas som "har ett troshetsproblem" vid ≥ 1 % allvarliga fel.
- Lätta fel har ingen tröskel; de beskrivs, döms inte.

## Testdata (FAS 2)

150 syntetiska samtal, svenska och engelska, 17 kategorier (se
`facit/KATEGORIER.md`). Varje samtal har facit i JSON: exakt vad som ska
sparas och vad som inte ska sparas.

- **Utveckling:** 100 samtal (`facit/utveckling/`), öppna, används för att
  bygga och felsöka riggen.
- **Dold:** 50 samtal (`facit/dold/`), **frysta med SHA-256-manifest, körs en
  enda gång i slutet.** Rättningar av riggen efter att dolda setet körts
  ogiltigförklarar det — en ny dold uppsättning krävs. (PROTOKOLL-regeln.)

**Beroende, ärligt noterat:** de 17 kategorierna är i denna version härledda ur
måtten och de kända dialoglager-kategorierna (negation, hypotetiskt, annans
röst, ironi, tid över månads-/årsskifte, flera fakta per rad, inget att
extrahera, injektion m.fl.). De synkas mot `reports/Dialoglager för Selvra.md`
när den filen finns; avviker den justeras `KATEGORIER.md` *före* FAS 3, aldrig
efter att dolda setet körts.

## Testrigg (FAS 3)

Mata in varje samtal, dumpa allt systemet sparat, jämför mekaniskt med facit.
Logga version, modell, datum och kostnad per körning. Determinism där det går,
LLM-domare bara där det måste (med handmärknings-kontroll).

## Kalibrering (FAS 4)

Reproducera en liten del av LongMemEval eller LoCoMo med varje system och
jämför med deras publicerade siffror. Stor avvikelse → felsök riggen innan
något troshets-resultat tas på allvar. Riggen måste först visa att den kan
återskapa kända tal.

## Regler

- Inga resultat publiceras före en kommentarsvecka för Mem0 och Vectorize
  (systemens upphovspersoner får svara innan publicering — ansvarsfull
  disclosure).
- Ton: torr och saklig. Fynd, inte omdömen. Inga superlativ, inga rankningar
  utan konfidensintervall.
- Allt syntetiskt. Ingen hälsodata, ingen Selvra-historik, inget privat.

## Ändringslogg

- 2026-10-30: Första versionen, låst.
