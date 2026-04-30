#!/bin/bash
# Generovanie Crea7in SK awareness ads
# Použitie: ./run-crea7in-sk.sh
# Pred spustením vlož foto produktu do: brands/gymbeam/crea7in-sk/product-images/

BASE="$(cd "$(dirname "$0")" && pwd)"
BRAND_DIR="$BASE/brands/gymbeam/crea7in-sk"

cd "$BASE/07-image-generation"

python3 generate_ads.py \
  --provider google \
  --brand-dir "$BRAND_DIR" \
  --prompts-file "$BRAND_DIR/prompts.json" \
  --images-dir "$BRAND_DIR/product-images" \
  --output-dir "$BRAND_DIR/outputs"
