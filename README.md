# Ad Static Generator (by Motion Foundations)

8-krokový systém (+ bonus) na produkciu AI static ads podľa metodiky Motion Foundations.

## Getting Started

### Čo potrebuješ

1. **Claude Code** — celý workflow prebieha cez neho ([inštalácia](https://claude.ai/code))
2. **Python 3** — pre image generation script (krok 7)
3. **API kľúč** — Google Gemini alebo FAL AI (vyber jedno):
   - Google Gemini: [aistudio.google.com](https://aistudio.google.com) → Get API key
   - FAL AI: [fal.ai](https://fal.ai) → Dashboard → API Keys

### Inštalácia Python závislostí

```bash
pip install requests Pillow
```

### Nastavenie API kľúča

Vytvor súbor `.env` v priečinku `07-image-generation/`:

```env
GEMINI_API_KEY=tvoj_kluč_sem
# alebo
FAL_KEY=tvoj_kluč_sem
```

### Spustenie

Otvor tento priečinok v Claude Code a postupuj krok po kroku podľa sekcie Workflow nižšie.

---

## Workflow

0. **Inicializácia** — brand, produkt, úloha; načítaj brand DNA súbory
1. **Research Prompt** (`01-brand-research-prompt/`) — brand intelligence extrakcia (raz na brand), výstup JSON do `brands/{brand}/brand-dna/`
2. **Brand Reference Cards** (`02-brand-cards/`) — HTML → PNG (Brand Spec Card + Visual Style Card)
3. **Product Research Check** (`03-product-research/`) — overenie že marketing research pre produkt existuje, inak presmeruj na `/marketing-research`
4. **Format Templates + Copy** (`04-format-templates-copy-prompt/`) — výber template, písanie copy, zostav `prompt.json` s placeholdermi
5. **Scoring Agents** (`05-scoring-agents/`) — 7 agentov, každý 1-100, threshold 90
6. **Prompt Substitution** (`06-prompt-substitution/`) — nahradenie `{{placeholderov}}` hodnotami z copy polí
7. **Image Generation** (`07-image-generation/`) — Nano Banana 2 / fal.ai prompty (1080x1920, safe zones)
8. **Output Check** (`08-output-check/`) — vizuálna kontrola každého výstupu pred finalizáciou

## Bonus

- **Multiply** (`BONUS/01-multiply/`) — validovaný winner → variácie naprieč formátmi (podmienka: reálny CTR/ROAS)
- **Animate** (`BONUS/02-animate/`) — winner static → 3-4s video cez Nano Banana 2 + Veo 3.1
- **Image Translator** (`BONUS/03-image-translator/`) — hotový ad → preklad textov do zadaných jazykov, produktové texty zachované

## Kľúčové pravidlá

- **Safe zone:** top 270px + bottom 340px bez textu (kvôli platform UI)
- **Formát:** 1080x1920, 9:16 vertikál
- **Image:** jedna súvislá fotka po okraje, žiadne rámčeky/panely
- **Copy:** JSON s placeholdermi — copy polia sú single source of truth, prompt string používa `{{headline}}`, `{{subhead}}`, `{{cta}}`
- **Threshold:** nič neide do generácie pod 90 bodov vo všetkých 7 agentoch
- **Product research:** bez kompletného researchu (deep-research, avatar-sheet, necessary-beliefs) nepokračuj do copy

## Status obsahu

- [x] 01 — brand research prompt
- [x] 02 — brand spec card + visual style card HTML templates
- [x] 03 — product research check protokol
- [x] 04 — 40 Motion recipe cards + 40 generických templates + ad-swipe + copy-prompt.md
- [x] 05 — 7 scoring agentov
- [x] 06 — prompt substitution protokol
- [x] 07 — generation prompt template
- [x] 08 — output check protokol
- [x] BONUS/01 — multiply winner prompt
- [x] BONUS/02 — animation workflow
- [x] BONUS/03 — image translator
