# Copy Generation — Motion Templates

Návod na písanie copy pre Motion Foundations recipe cards (krok 4 workflow).

## Vstup

**Copy polia** (headline, subhead, cta):
- `brands/{brand}/products/{product}/marketing-research/avatar-sheet.md` — jazyk zákazníka, pain points, citáty
- `brands/{brand}/products/{product}/marketing-research/necessary-beliefs.md` — North Star pre každý kus copy
- `brands/{brand}/products/{product}/marketing-research/deep-research.md` — overené claims, specs, diferenciátory

**Image direction** (background, lighting, farby, typografia, product position):
- `brands/{brand}/brand-dna/brand-research-brief.json` — visual_system, primary_color_hex, brand colors
- `brands/{brand}/brand-dna/brand-spec-card.html` — typografia, logo, CTA štýl
- `brands/{brand}/brand-dna/visual-style-card.html` — photography direction, mood, always/never rules

**Template:**
- Vybraný recipe card (napr. `01-headline-template.md`) — variation vectors pre image direction

## Proces

### 1. Načítaj template

Otvor vybraný recipe card. Identifikuj:
- Ktorý štýl (A / B / C) sa použije
- Copy template pre daný štýl (headline / subhead / CTA)
- Word counts pre každý element
- Image direction a variation vectors

### 2. Napíš copy

Pre každý copy element dodržuj word count z template:
- **Headline** — presný počet slov, jedna myšlienka, musí fungovať aj bez vizuálu
- **Subhead** — pridáva novú dimenziu (dôkaz, špecifikum, urgencia) — neopakuje headline
- **CTA** — 2–5 slov

**Pravidlá:**
- Použi jazyk zákazníka z `avatar-sheet.md` (Direct Client Quotes sekcia) — nie marketingový žargón
- Claims musia byť overené z `deep-research.md` alebo `brand-research-brief.json` — nikdy vymyslené
- Beliefs z `necessary-beliefs.md` sú North Star — copy musí viesť k nim
- Žiadne em dash (—), en dash (–), bodkočiarky v renderovanom texte

### 3. Vyber variation

Z variation vectors v template vyber konkrétne hodnoty. Dáta ber z:

| Hodnota | Zdroj |
|---------|-------|
| Background | `brand-research-brief.json` → visual_system + variation vectors z template |
| Lighting | `visual-style-card.html` → photography direction |
| Product position | variation vectors z template |
| Farby | `brand-research-brief.json` → primary_color_hex, secondary_color_hex |
| Typografia | `brand-spec-card.html` → headline font, weights, colors |
| Focal length | variation vectors z template |
| Energy / mood | `visual-style-card.html` → mood + variation vectors z template |

### 4. Zostav JSON output

Výstup musí byť vždy platný JSON. Copy polia sú **single source of truth** — prompt string odkazuje na ne cez `{{placeholder}}`, nikdy neobsahuje text natvrdo.

```json
{
  "template": "[číslo + názov] — Style [A/B/C]",
  "aspect_ratio": "[napr. 9:16]",
  "needs_product_images": true,
  "headline": "[text]",
  "subhead": "[text alebo null]",
  "cta": "[text alebo null]",
  "image_direction": {
    "background": "[voľba z variation vectors]",
    "product_position": "[voľba]",
    "lighting": "[voľba]",
    "focal_length": "[voľba]",
    "energy": "[voľba]"
  },
  "prompt": "[kompletný image generation prompt z recipe card s {{headline}}, {{subhead}}, {{cta}} namiesto hardcoded textu]"
}
```

**Pravidlo pre prompt string:** Vezmi image generation prompt z recipe card pre daný štýl. Všade kde template hovorí `"[HEADLINE]"` daj `{{headline}}`, kde `"[SUBHEAD]"` daj `{{subhead}}`, kde `"[CTA]"` daj `{{cta}}`. Ostatné `[BRACKETED]` hodnoty (brand name, product name, aspect ratio, safe zones, variation values) vyplň priamo.

JSON ide priamo do kroku 5 (Scoring) — Agent 07 číta len copy polia, prompt string neotvára.
