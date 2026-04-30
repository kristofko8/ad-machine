# Colla Pink SK — Hero Product Showcase Ad Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Vytvoriť jeden hotový statický ad pre Colla Pink (BeastPink) na SK trh — template #35 Hero Product Showcase + Stat Bar — vrátane product researchu, copy, scoringu a finálneho image promptu.

**Architecture:** Product research → copy → scoring (7 agentov, threshold 90) → prompt.json → finálny image prompt. Žiadna image generácia (chýba API kľúč).

**Tech Stack:** Markdown súbory, JSON, ad-static-generator-by-motion workflow

---

## Súbory

- Create: `brands/beastpink/product-research/colla-pink-sk-avatar.md`
- Create: `brands/beastpink/product-research/colla-pink-sk-offer-brief.md`
- Create: `brands/beastpink/ads/colla-pink-sk-hero-01/prompt.json`
- Create: `brands/beastpink/ads/colla-pink-sk-hero-01/image-prompt.md`

---

## Task 1: Avatar Sheet — Colla Pink SK

**Súbory:**
- Create: `brands/beastpink/product-research/colla-pink-sk-avatar.md`

- [ ] **Krok 1: Vytvor avatar sheet**

Obsah súboru `brands/beastpink/product-research/colla-pink-sk-avatar.md`:

```markdown
# Avatar Sheet — Colla Pink SK

## Demographic & General Information
- **Age Range:** 25–40
- **Gender:** Žena
- **Location:** Slovensko
- **Monthly Revenue:** 1 000–2 500 €
- **Professional Backgrounds:** Administratíva, marketing, HR, zdravotníctvo, SZČO
- **Typical Identities:** Aktívna žena, ktorá dbá na seba — cvičí 2–4x týždenne, sleduje beauty/wellness obsah, nakupuje online, číta zloženie produktov

## Key Challenges & Pain Points

1. Vlasy a nechty nie sú v stave, v akom by chcela:
   - Lámavé nechty, ktoré nevydržia
   - Vlasy, ktoré vypadávajú viac ako pred rokom
   - Pokožka, ktorá nestráca únavu ani po spánku

2. Nechce komplikovaný rituál:
   - Nemá čas na 5 rôznych doplnkov ráno
   - Kapsuly ju nudia, chce niečo čo si „vychutná"
   - Skúšala kolagény, ktoré nefungovali alebo chutnali zle

3. Nedôvera k doplnkom:
   - Nevie či kolagén skutočne funguje
   - Bojí sa cukru a zbytočných prísad
   - Chce vedieť, čo presne pije

## Goals & Aspirations

### Short-Term Goals
- Zdravšie nechty do 4–6 týždňov
- Jednoduchý ranný rituál, ktorý zvládne každý deň
- Doplnok, ktorý jej nestojí 60 € mesačne

### Long-Term Aspirations
- Cítiť sa sebaisto v koži — bez filtrov
- Udržať si zdravý vzhľad aj s vekom
- Vedieť, že sa stará o seba zvnútra, nielen zvonka

## Emotional Drivers & Psychological Insights
- Chce výsledky, nie sľuby — je skeptická, lebo skúšala veľa produktov
- Identifikuje sa ako „zdravo žijúca" — clean label je signál dôvery
- Social proof pre ňu nie je influencer — sú to skutočné recenzie reálnych žien

## Direct Client Quotes (z recenzií Colla Pink na GymBeam)

### General
- „Nechty konečne nevylamujú, po mesiaci vidím rozdiel."
- „Príjemná chuť, ľahko sa pridá do vody alebo smoothie."
- „Konečne kolagén bez cukru, ktorý mi nezničí makrá."

### Pain Points & Frustrations
- „Skúšala som drahé krémy, ale problém je zvnútra."
- „Ostatné kolagény mi nechutili, táto príchuť hrozna je fajn."
- „Nemám čas na veľa doplnkov, potrebujem jedno riešenie."

### Mindset
- „Chcem sa o seba starať, ale zmysluplne."
- „Ak niečo beriem každý deň, musí byť dobré a účinné."

## Key Emotional Fears & Deep Frustrations
- Strach: míňam peniaze na niečo, čo nefunguje
- Frustrácia: vidím iné ženy s krásnymi nechtami/vlasmi a neviem prečo u mňa to nefunguje
- Hlboký strach: starnem rýchlejšie ako chcem

## Typical Emotional Journey
- **Awareness:** Vidí obsah o kolagéne na Instagrame / TikToku, recenzia od kamarátky
- **Frustration:** Skúšala lacný kolagén — bez efektu. Drahý krém — dočasný efekt.
- **Seeking Solutions:** Hľadá kolagén bez cukru, s dobrými recenziami, od known brandy
- **Relief & Commitment:** 1265 recenzií + 4.5★ + bez cukru = dôvera. Kúpi.
```

- [ ] **Krok 2: Overiť že súbor existuje a je kompletný** — skontroluj sekcie Demographics, Pain Points, Goals, Quotes

---

## Task 2: Offer Brief — Colla Pink SK

**Súbory:**
- Create: `brands/beastpink/product-research/colla-pink-sk-offer-brief.md`

- [ ] **Krok 1: Vytvor offer brief**

Obsah súboru `brands/beastpink/product-research/colla-pink-sk-offer-brief.md`:

```markdown
# Offer Brief — Colla Pink SK

## Level of Awareness
- Solution Aware — vie o kolagéne, hľadá ten správny produkt

## Stage of Sophistication
- Level 3 — trh je nasýtený kolagénmi, treba mechanizmus: prečo práve tento

## Big Idea
- Beauty sa buduje zvnútra — jeden denný nápoj stačí

## Potential UMP (Unique Mechanism of the Problem)
- Lámavé nechty a vypadávanie vlasov nie je problém starostlivosti zvonka — je to nedostatok kolagénu a zinku, ktorý zvonka nedoplníš

## Potential UMS (Unique Mechanism of the Solution)
- Colla Pink kombinuje kolagén + zinok + selén v jednej porcii bez cukru — 3 kľúčové živiny pre vlasy, nechty a imunitu v jednom čistom nápoji

## Product
- Colla Pink by BeastPink — prášková forma, príchuť hrozna, 20 porcií/balenie
- Bez cukru, bez lepku, bez laktózy, bez GMO
- Obsah: kolagén + zinok (zdravé vlasy/nechty) + selén (imunita)
- Cena: ~7–9 € / balenie (189 CZK)

## Potential Headline Ideas
- „VLASY. NECHTY. HOTOVO." — jednoduchý declaratív
- „KOLAGÉN BEZ KOMPROMISOV" — mechanism + clean claim
- „1 NÁPOJ. 3 VÝSLEDKY." — stat-forward

## List All Objections
- „Kolagén nefunguje" → 1265 recenzií, 4.5★ je sociálny dôkaz
- „Je tam cukor?" → bez cukru — treba povedať explicitne
- „Je to drahé" → 20 porcií za ~9 € = menej ako káva denne
- „Nechutí to dobre" → príchuť hrozna, ľahko sa rozpustí

## Belief Chains
1. Musí veriť, že kolagén funguje → social proof (1265 recenzií)
2. Musí veriť, že tento je čistý → „bez cukru, bez lepku, bez GMO"
3. Musí veriť, že výsledky uvidí → konkrétny benefit: vlasy + nechty + imunita

## Stats pre Stat Bar (z reálneho produktu)
- „1 265 RECENZIÍ" — social proof
- „BEZ CUKRU" — clean label objection handler
- „3 V 1" — kolagén + zinok + selén

## Other Notes
- Template #35 nepotrebuje subhead — produkt + štatistiky robia argument samy
- Headline musí byť superlative alebo strong declarative (max 6 slov, uppercase)
- CTA: krátky, akčný, 2–4 slová
```

- [ ] **Krok 2: Skontrolovať belief chains a stats** — overiť že stats sú z reálneho produktu (nie vymyslené)

---

## Task 3: Copy + Scoring (7 agentov)

**Súbory:**
- Create: `brands/beastpink/ads/colla-pink-sk-hero-01/prompt.json` (draft, pred scoringom)

- [ ] **Krok 1: Napíš draft copy**

```json
{
  "template": "35-hero-product-showcase-stat-bar",
  "brand": "BeastPink",
  "product": "Colla Pink",
  "market": "SK",
  "language": "sk",
  "copy": {
    "headline": "VLASY. NECHTY. HOTOVO.",
    "cta": "VYSKÚŠAJ TERAZ",
    "stat_1": "1 265 RECENZIÍ",
    "stat_2": "BEZ CUKRU",
    "stat_3": "3 V 1"
  }
}
```

- [ ] **Krok 2: Spusti Agent 1 — Persona Fit**

Vyhodnoť copy voči avatar sheet. Skontroluj:
- Hovorí copy jazykom avatara (nie marketingovým)?
- Pomenúva skutočný pain (vlasy/nechty, nie abstraktný wellness)?
- Má identity signal (pre túto konkrétnu ženu)?
- Rieši hlavnú námietku (funguje to / je čistý)?
- Je kultúrne špecifický pre SK ženu 25–40?

Prah: 90/100. Ak <90 → oprav copy, opakuj.

- [ ] **Krok 3: Spusti Agent 2 — Angle**

Skontroluj: je uhol reklamy (benefit-first declarative) správny pre túto fázu awareness (Solution Aware, Sophistication Level 3)?

- [ ] **Krok 4: Spusti Agent 3 — Emotion**

Skontroluj: vyvoláva copy správnu emóciu? Pre tento produkt: sebavedomie + dôvera, nie strach alebo urgentnosť.

- [ ] **Krok 5: Spusti Agent 4 — Brand**

Skontroluj: „VLASY. NECHTY. HOTOVO." — je superlative alebo strong declarative? Je obhájiteľné (nie „najlepší na svete")? Áno — je to declarative, obhájiteľné.

- [ ] **Krok 6: Spusti Agent 5 — Copy Excellence**

Skontroluj: je každé slovo nutné? Headline je 3 slová + bodky — efektívny. CTA je akčný. Stats sú konkrétne a reálne.

- [ ] **Krok 7: Spusti Agent 6 — Format**

Skontroluj: sedí copy na template #35? Headline max 6 slov ✓, CTA 2–4 slová ✓, 3 stats ✓, žiadny body copy ✓.

- [ ] **Krok 8: Spusti Agent 7 — Grammar (SK)**

Skontroluj: gramatika, diakritika, interpunkcia v slovenčine. „VYSKÚŠAJ TERAZ" — správne. „BEZ CUKRU" — správne.

- [ ] **Krok 9: Ak všetky agenty PASS → pokračuj. Ak nie → oprav copy a opakuj od Kroku 2.**

---

## Task 4: Finálny prompt.json + Image Prompt

**Súbory:**
- Modify: `brands/beastpink/ads/colla-pink-sk-hero-01/prompt.json` (pridaj prompt string)
- Create: `brands/beastpink/ads/colla-pink-sk-hero-01/image-prompt.md`

- [ ] **Krok 1: Doplň prompt.json o finálny prompt string so substitúciou**

```json
{
  "template": "35-hero-product-showcase-stat-bar",
  "brand": "BeastPink",
  "product": "Colla Pink",
  "market": "SK",
  "language": "sk",
  "aspect_ratio": "1:1",
  "needs_product_images": true,
  "reference_uploads": [
    "brand-spec-card.png",
    "visual-style-card.png",
    "colla-pink-product.jpg"
  ],
  "copy": {
    "headline": "VLASY. NECHTY. HOTOVO.",
    "cta": "VYSKÚŠAJ TERAZ",
    "stat_1": "1 265 RECENZIÍ",
    "stat_2": "BEZ CUKRU",
    "stat_3": "3 V 1"
  },
  "prompt": "Use the attached product image as the primary reference — reproduce the product EXACTLY as it appears in the photo, do not invent or alter shape, color, labels, or design. Reference the attached brand spec card and visual style card for all typography, colors, and photography direction.\n\nCreate a hero product showcase + stat bar ad for BeastPink's Colla Pink. 1080x1080.\n\nCOMPOSITION:\nOne continuous image filling the entire frame. Background: soft pastel pink-to-white gradient, clean and airy.\n\nTop: large bold pink uppercase sans-serif headline \"VLASY. NECHTY. HOTOVO.\" at maximum scale. 2 lines max.\n\nBelow headline: white rounded-rectangle pill CTA button with pink uppercase bold text \"VYSKÚŠAJ TERAZ\".\n\nCenter: the Colla Pink product (reproduced exactly from reference) in full packaging, angled slightly, hero-lit with soft studio lighting. Product fills the vertical center zone.\n\nSurrounding the product: fine pink powder dust, small collagen granule particles, delicate botanical elements (small grape blossoms or dried grape slices) arranged in a soft radial scatter around the product. Debris looks natural — not machine-placed. Light, airy, beauty-forward.\n\nBottom: a white rounded-pill stat bar spanning most of the width with three metrics separated by thin vertical pink hairlines:\n- \"1 265 RECENZIÍ\"  |  \"BEZ CUKRU\"  |  \"3 V 1\"\n\nNumbers/labels large and bold in pink. Short labels smaller below in bold.\n\nTYPOGRAPHY:\nHeadline at max scale, all caps, pink or deep rose. CTA pill uppercase bold. Stat labels bold, pink.\n\nSAFE ZONES:\nTop 270px and bottom 340px clear of all text and key elements.\n\nCOLOR AND TREATMENT:\nSoft pastel pink background. Brand-color (pink/rose) typography. Product hero-lit with realistic powder shadows.\n\nMOOD:\nPremium feminine beauty — confident, clean, results-driven. Not clinical. Not girly-overload. Aspirational but real."
}
```

- [ ] **Krok 2: Vytvor `image-prompt.md`** — čitateľná verzia finálneho promptu pre manuálne vloženie do generátora

Obsah súboru `brands/beastpink/ads/colla-pink-sk-hero-01/image-prompt.md`:

```markdown
# Image Prompt — Colla Pink SK Hero 01

**Template:** 35 — Hero Product Showcase + Stat Bar
**Aspect ratio:** 1:1 (1080x1080)
**Reference uploads potrebné:** brand-spec-card.png + visual-style-card.png + colla-pink-product.jpg

---

## Finálny prompt

Use the attached product image as the primary reference — reproduce the product EXACTLY as it appears in the photo, do not invent or alter shape, color, labels, or design. Reference the attached brand spec card and visual style card for all typography, colors, and photography direction.

Create a hero product showcase + stat bar ad for BeastPink's Colla Pink. 1080x1080.

COMPOSITION:
One continuous image filling the entire frame. Background: soft pastel pink-to-white gradient, clean and airy.

Top: large bold pink uppercase sans-serif headline "VLASY. NECHTY. HOTOVO." at maximum scale. 2 lines max.

Below headline: white rounded-rectangle pill CTA button with pink uppercase bold text "VYSKÚŠAJ TERAZ".

Center: the Colla Pink product (reproduced exactly from reference) in full packaging, angled slightly, hero-lit with soft studio lighting. Product fills the vertical center zone.

Surrounding the product: fine pink powder dust, small collagen granule particles, delicate botanical elements (small grape blossoms or dried grape slices) arranged in a soft radial scatter around the product. Debris looks natural — not machine-placed. Light, airy, beauty-forward.

Bottom: a white rounded-pill stat bar spanning most of the width with three metrics separated by thin vertical pink hairlines:
- "1 265 RECENZIÍ"  |  "BEZ CUKRU"  |  "3 V 1"

Numbers/labels large and bold in pink. Short labels smaller below in bold.

TYPOGRAPHY:
Headline at max scale, all caps, pink or deep rose. CTA pill uppercase bold. Stat labels bold, pink.

SAFE ZONES:
Top 270px and bottom 340px clear of all text and key elements.

COLOR AND TREATMENT:
Soft pastel pink background. Brand-color (pink/rose) typography. Product hero-lit with realistic powder shadows.

MOOD:
Premium feminine beauty — confident, clean, results-driven. Not clinical. Not girly-overload. Aspirational but real.

---

## Copy summary

| Pole | Text |
|------|------|
| Headline | VLASY. NECHTY. HOTOVO. |
| CTA | VYSKÚŠAJ TERAZ |
| Stat 1 | 1 265 RECENZIÍ |
| Stat 2 | BEZ CUKRU |
| Stat 3 | 3 V 1 |

## Checklist pred generovaním

- [ ] Žiadny `{{placeholder}}` v prompte
- [ ] brand-spec-card.png pripravená
- [ ] visual-style-card.png pripravená
- [ ] colla-pink-product.jpg stiahnutá z gymbeam.cz
- [ ] aspect_ratio nastavený: 1:1
- [ ] needs_product_images: true
```

- [ ] **Krok 3: Záverečná kontrola** — overiť že v `image-prompt.md` nie je žiadny `{{placeholder}}`, copy sedí s prompt stringom, safe zones sú v prompte uvedené

---

## Hotovo

Po dokončení všetkých taskov:
- `brands/beastpink/product-research/colla-pink-sk-avatar.md` ✓
- `brands/beastpink/product-research/colla-pink-sk-offer-brief.md` ✓
- `brands/beastpink/ads/colla-pink-sk-hero-01/prompt.json` ✓
- `brands/beastpink/ads/colla-pink-sk-hero-01/image-prompt.md` ✓

Nasledujúci krok (keď bude API kľúč): spusti `07-image-generation/generate_ads.py` s týmito súbormi.
