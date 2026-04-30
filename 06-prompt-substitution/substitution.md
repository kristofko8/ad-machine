# 06 — Prompt Substitution

Nahradenie `{{placeholderov}}` v prompt stringu hodnotami z copy polí. Spúšťa sa po PASS všetkých 7 agentov, pred odoslaním do generátora.

## Vstup

`prompt.json` z kroku 5 — schválený copy brief po PASS všetkých 7 agentov

## Proces

1. Otvor `prompt.json`
2. Pre každý placeholder v `prompt` stringu:
   - `{{headline}}` → hodnota poľa `headline`
   - `{{subhead}}` → hodnota poľa `subhead`
   - `{{cta}}` → hodnota poľa `cta`
   - `{{body}}` → hodnota poľa `body` (ak existuje)
   - `{{review_1}}` → hodnota poľa `review_1` (ak existuje)
   - `{{review_2}}` → hodnota poľa `review_2` (ak existuje)
3. Skontroluj že v prompt stringu nezostal žiadny nenahradzený `{{placeholder}}`
4. Výstup = finálny prompt string pripravený na generátor

## Kontrola pred odoslaním

- [ ] Žiadny `{{placeholder}}` v prompt stringu
- [ ] Text v prompte zodpovedá copy poliam (žiadny drift)
- [ ] `aspect_ratio` je nastavený
- [ ] `needs_product_images` je nastavený
- [ ] Reference images pripravené: `brand-spec-card.png`, `visual-style-card.png`, product image

## Výstup

Finálny prompt string ide do kroku 7 (Image Generation).
