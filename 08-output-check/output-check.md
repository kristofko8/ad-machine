# 08 — Output Check

Vizuálna kontrola vygenerovaných obrázkov pred finalizáciou. Spúšťa sa po každom generovaní (krok 07). Výstup: PASS alebo REGENERATE pre každý obrázok.

## Čo kontrolovať

### 1. Text rendering
- Headline je čitateľný, plný, neorezaný
- Subhead je čitateľný, žiadne garbled/corrupted znaky
- CTA je čitateľný a úplný
- Žiadny text nechýba oproti copy briefa

### 2. Copy presnosť
- Text v obraze zodpovedá copy poliam z JSON (verbatim)
- Žiadne substitúcie, skrátenia ani vynechané slová

### 3. Kompozícia
- Produkt je viditeľný a nepoškodený (label, farba, tvar zodpovedajú reference image)
- Text nespadá do safe zone (top 270px, bottom 340px pre 9:16)
- Headline a produkt sú v rovnováhe — jeden neprehlušuje druhý

### 4. Brand
- Farby zodpovedajú brand spec card
- Typografia zodpovedá brand spec card
- Logo prítomné ak template vyžaduje

### 5. Technická kvalita
- Obrázok nie je rozmazaný ani artefaktovaný
- Bez viditeľných AI hallucinations (deformované objekty, nečitateľné pseudo-znaky)

---

## Output formát

```
OUTPUT CHECK — [brand] / [produkt] / [dátum]

[template ID] — [názov formátu]
  Text rendering:  PASS / FAIL — [poznámka]
  Copy presnosť:   PASS / FAIL — [poznámka]
  Kompozícia:      PASS / FAIL — [poznámka]
  Brand:           PASS / FAIL — [poznámka]
  Tech kvalita:    PASS / FAIL — [poznámka]
  Verdict:         PASS / REGENERATE
  Dôvod (ak REGENERATE): [čo konkrétne nefunguje]

[opakovať pre každý obrázok]

SÚHRN:
  PASS:        [počet]
  REGENERATE:  [počet]
  Zoznam na regeneráciu: [template ID zoznam]
```

---

## Postup po kontrole

**PASS** → obrázok postupuje do `brands/{brand}/brand-dna/ads/{date}-{format}/output.png`

**REGENERATE** → uprav prompt (ak bol problém v kompozícii/brand) alebo over copy JSON (ak bol problém v texte), spusti generovanie znova len pre dané templaty

---

## Časté príčiny zlyhania a riešenia

| Problém | Príčina | Riešenie |
|---|---|---|
| Orezaný headline | Príliš dlhý text pre danú pozíciu | Skráť headline alebo uprav pozíciu v prompt stringu |
| Garbled subhead | Model nečítal copy pole správne | Over placeholder substitúciu, skontroluj špeciálne znaky |
| Deformovaný produkt | Slabá reference image alebo konflikt v prompte | Nahraj kvalitnejší product shot, zjednodušь prompt |
| Zlé farby | Brand spec card nebola uploadnutá | Skontroluj reference images pri generovaní |
| Text v safe zone | Chýbajúca safe zone inštrukcia v prompte | Doplň safe zone do prompt stringu |
