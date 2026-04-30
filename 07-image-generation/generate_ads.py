#!/usr/bin/env python3
"""
Static Ad Generator — Phase 3: Image Generation via Nano Banana 2

Supports FAL AI and Google Gemini API as providers.
At startup, prompts the user to select a provider interactively.

Usage:
    python generate_ads.py                          # Interactive provider selection
    python generate_ads.py --provider fal           # Use FAL AI directly
    python generate_ads.py --provider google        # Use Google Gemini API
    python generate_ads.py --templates 1,7,13,15    # Generate specific templates
    python generate_ads.py --resolution 2K          # Use 2K resolution
    python generate_ads.py --variations 3           # Generate 3 variations per template
    python generate_ads.py --dry-run                # Show what would be generated without calling API
    python generate_ads.py --prompts-file prompts/essentials-vitapack-prompts.json
    python generate_ads.py --images-dir product-images/essentials-vitapack
    python generate_ads.py --output-dir product-images/essentials-vitapack/outputs/sk

Required env vars:
    FAL_KEY         — FAL AI API key
    GEMINI_API_KEY  — Google Gemini API key (only if using google/google-batch provider)
"""

import argparse
import json
import os
import sys
import time
import base64
import mimetypes
from pathlib import Path

try:
    import requests
except ImportError:
    print("Error: 'requests' package required. Install with: pip install requests")
    sys.exit(1)

try:
    from PIL import Image
    import io as _io
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

FAL_KEY = os.environ.get("FAL_KEY", "")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

FAL_DIRECT_URL = "https://fal.run"
T2I_ENDPOINT = "fal-ai/nano-banana-2"
EDIT_ENDPOINT = "fal-ai/nano-banana-2/edit"
GEMINI_MODEL_ID = "gemini-3.1-flash-image-preview"
FAL_MAX_IMAGES = 4

MAX_POLL_TIME = 180
DEFAULT_RESOLUTION = "1K"
DEFAULT_OUTPUT_FORMAT = "png"

RESOLUTION_MAP_GOOGLE = {
    "0.5K": "512x512",
    "1K":   "1024x1024",
    "2K":   "2048x2048",
    "4K":   "4096x4096",
}


# ---------------------------------------------------------------------------
# Provider selection
# ---------------------------------------------------------------------------

def select_provider():
    print("\n╔════════════════════════════════════════════════════════╗")
    print("║         Static Ad Generator — Provider               ║")
    print("╠════════════════════════════════════════════════════════╣")
    print("║  1. FAL AI                  (~$0.06/obr 1K, okamžite) ║")
    print("║  2. Google — Nano Banana 2  (~$0.067/obr 1K, okamžite)║")
    print("║  3. Google Batch — NB2      (~$0.034/obr 1K, do 24h) ║")
    print("╚════════════════════════════════════════════════════════╝")
    while True:
        choice = input("\nVyber provider [1/2/3]: ").strip()
        if choice == "1":
            return "fal"
        elif choice == "2":
            return "google"
        elif choice == "3":
            return "google-batch"
        else:
            print("Zadaj 1, 2 alebo 3.")


# ---------------------------------------------------------------------------
# FAL API helpers
# ---------------------------------------------------------------------------

def fal_headers():
    return {
        "Authorization": f"Key {FAL_KEY}",
        "Content-Type": "application/json",
    }


def upload_image_to_fal(image_path: str) -> str:
    mime_type = mimetypes.guess_type(image_path)[0] or "image/png"
    with open(image_path, "rb") as f:
        image_data = f.read()
    resp = requests.post(
        "https://fal.run/fal-ai/file-storage/upload",
        headers={"Authorization": f"Key {FAL_KEY}"},
        files={"file": (os.path.basename(image_path), image_data, mime_type)},
    )
    if resp.status_code != 200:
        b64 = base64.b64encode(image_data).decode("utf-8")
        return f"data:{mime_type};base64,{b64}"
    data = resp.json()
    return data.get("url", data.get("file_url", ""))


def run_generation_fal(endpoint: str, payload: dict) -> dict:
    url = f"{FAL_DIRECT_URL}/{endpoint}"
    resp = requests.post(url, headers=fal_headers(), json=payload, timeout=MAX_POLL_TIME)
    resp.raise_for_status()
    return resp.json()


def download_image(image_url: str, save_path: str):
    resp = requests.get(image_url, stream=True)
    resp.raise_for_status()
    with open(save_path, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)


def composite_product(image_source, product_png_path: str, placement: dict, save_path: str):
    if not PILLOW_AVAILABLE:
        print("     ⚠ Pillow not available — skipping product composite")
        return

    if isinstance(image_source, (str, Path)):
        base = Image.open(image_source).convert("RGBA")
    else:
        base = Image.open(_io.BytesIO(image_source)).convert("RGBA")

    product = Image.open(product_png_path).convert("RGBA")

    img_w, img_h = base.size
    area_x = int(placement["x"] * img_w)
    area_y = int(placement["y"] * img_h)
    area_w = int(placement["w"] * img_w)
    area_h = int(placement["h"] * img_h)

    product.thumbnail((area_w, area_h), Image.LANCZOS)

    offset_x = area_x + (area_w - product.width) // 2
    offset_y = area_y + (area_h - product.height) // 2

    base.paste(product, (offset_x, offset_y), product)
    base.convert("RGB").save(save_path, "PNG")
    print(f"     ✓ Product composited onto image")


# ---------------------------------------------------------------------------
# Google Gemini API helpers
# ---------------------------------------------------------------------------

def load_image_part_google(image_path: str):
    try:
        from google.genai import types
    except ImportError:
        print("Error: 'google-genai' package required. Install with: pip install google-genai")
        sys.exit(1)
    mime_type = mimetypes.guess_type(image_path)[0] or "image/png"
    with open(image_path, "rb") as f:
        data = f.read()
    return types.Part.from_bytes(data=data, mime_type=mime_type)


def run_generation_google(prompt_text: str, image_parts: list, aspect_ratio: str) -> bytes:
    try:
        from google import genai
        from google.genai import types
    except ImportError:
        print("Error: 'google-genai' package required. Install with: pip install google-genai")
        sys.exit(1)
    client = genai.Client(api_key=GEMINI_API_KEY)
    contents = image_parts + [types.Part.from_text(text=prompt_text)]
    response = client.models.generate_content(
        model=GEMINI_MODEL_ID,
        contents=contents,
        config=types.GenerateContentConfig(
            response_modalities=["IMAGE"],
            image_config=types.ImageConfig(
                aspect_ratio=aspect_ratio,
            ),
        ),
    )
    for part in response.candidates[0].content.parts:
        if part.inline_data:
            return part.inline_data.data
    raise ValueError("No image returned in response")


# ---------------------------------------------------------------------------
# Template name mapping
# ---------------------------------------------------------------------------

TEMPLATE_NAMES = {
    1: "headline",
    2: "offer-promotion",
    3: "testimonials",
    4: "features-benefits",
    5: "bullet-points",
    6: "social-proof",
    7: "us-vs-them",
    8: "before-after-ugc",
    9: "negative-marketing",
    10: "press-editorial",
    11: "pull-quote-review",
    12: "lifestyle-colorway",
    13: "stat-surround-hero",
    14: "bundle-showcase",
    15: "social-comment-screenshot",
    16: "curiosity-gap-testimonial",
    17: "verified-review-card",
    18: "stat-surround-flatlay",
    19: "highlighted-testimonial",
    20: "advertorial-editorial",
    21: "bold-statement",
    22: "flavor-story",
    23: "long-form-manifesto",
    24: "product-comment-callout",
    25: "us-vs-them-color-split",
    26: "stat-callout-lifestyle",
    27: "benefit-checklist",
    28: "feature-arrow-callout",
    29: "ugc-viral-post",
    30: "hero-statement-icon-bar",
    31: "comparison-grid",
    32: "ugc-story-callout",
    33: "faux-press-screenshot",
    34: "faux-iphone-notes",
    35: "hero-product-stat-bar",
    36: "whiteboard-before-after",
    37: "hero-statement-promo",
    38: "ugc-lifestyle-review-split",
    39: "curiosity-gap-scroll-stopper",
    40: "post-it-note-style",
}


# ---------------------------------------------------------------------------
# Pre-generation prompt validation
# ---------------------------------------------------------------------------

REFERENCE_PHRASES = ["reference image", "shown in the reference", "reproduce it exactly", "reproduce the product exactly"]
INVENTION_PATTERNS = ["white/cream bottle", "white/cream shampoo", "matte black box", "amber/white cosmetic",
                      "blue bottle", "green bottle", "red bottle", "plastic bottle", "glass jar", "metal tube"]


def validate_prompts_quick(prompts, templates_filter, images_dir):
    issues = []
    filtered = [p for p in prompts if templates_filter is None or p["template_number"] in templates_filter]

    missing_ref = []
    invented = []
    for p in filtered:
        prompt = p.get("prompt", p.get("ai_prompt", "")).lower()
        needs_images = p.get("needs_product_images", True)
        num = p["template_number"]
        if needs_images:
            if not any(ph in prompt for ph in REFERENCE_PHRASES):
                missing_ref.append(num)
            for pat in INVENTION_PATTERNS:
                if pat.lower() in prompt:
                    invented.append((num, pat))

    if missing_ref:
        issues.append(f"✗ Chýba 'reference image' v {len(missing_ref)} template(och): {missing_ref}")
    if invented:
        for num, pat in invented:
            issues.append(f"✗ T{num:02d}: podozrivý popis produktu '{pat}'")

    if images_dir and images_dir.exists():
        img_files = [f for f in images_dir.iterdir()
                     if f.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp") and not f.name.startswith(".")]
        if not img_files:
            issues.append(f"✗ Žiadne produktové obrázky v {images_dir}")
        else:
            needs_images_templates = [p["template_number"] for p in filtered if p.get("needs_product_images", True)]
            if needs_images_templates and not issues:
                issues_info = f"✓ {len(img_files)} obrázok(ov) nájdených pre {len(needs_images_templates)} template(ov) s needs_product_images=true"
                print(f"  {issues_info}")

    return issues


# ---------------------------------------------------------------------------
# Main generation logic
# ---------------------------------------------------------------------------

def generate_ads(
    provider,
    brand_dir,
    prompts_file=None,
    images_dir=None,
    output_dir=None,
    templates_filter=None,
    resolution=DEFAULT_RESOLUTION,
    num_variations=1,
    dry_run=False,
):
    brand_path = Path(brand_dir)

    if prompts_file:
        prompts_path = Path(prompts_file) if Path(prompts_file).is_absolute() else brand_path / prompts_file
    else:
        prompts_path = brand_path / "prompts.json"

    if images_dir:
        product_images_dir = Path(images_dir) if Path(images_dir).is_absolute() else brand_path / images_dir
    else:
        product_images_dir = brand_path / "product-images"

    if output_dir:
        outputs_dir = Path(output_dir) if Path(output_dir).is_absolute() else brand_path / output_dir
    else:
        outputs_dir = brand_path / "outputs"

    if not prompts_path.exists():
        print(f"Error: {prompts_path} not found. Run Phase 2 first.")
        sys.exit(1)

    if not dry_run:
        if provider == "fal" and not FAL_KEY:
            print("Error: FAL_KEY not set. Set with: export FAL_KEY='your-key'")
            sys.exit(1)
        if provider in ("google", "google-batch") and not GEMINI_API_KEY:
            print("Error: GEMINI_API_KEY not set. Set with: export GEMINI_API_KEY='your-key'")
            sys.exit(1)

    with open(prompts_path) as f:
        prompts_data = json.load(f)

    brand_name = prompts_data.get("brand", "unknown")
    prompts = prompts_data.get("prompts", [])

    if not dry_run:
        issues = validate_prompts_quick(prompts, templates_filter, product_images_dir)
        if issues:
            print("\n⚠  UPOZORNENIE pred generovaním:")
            for issue in issues:
                print(f"   {issue}")
            answer = input("\nPokračovať napriek upozorneniam? [a/N]: ").strip().lower()
            if answer not in ("a", "ano", "y", "yes"):
                print("Generovanie zrušené.")
                sys.exit(0)
        print()

    if templates_filter:
        prompts = [p for p in prompts if p["template_number"] in templates_filter]

    print(f"\n{'='*60}")
    print(f"  Static Ad Generator — {brand_name}")
    print(f"  Provider: {provider.upper()}")
    print(f"  Prompts file: {prompts_path}")
    print(f"  Images dir:   {product_images_dir}")
    print(f"  Templates: {len(prompts)} | Resolution: {resolution} | Variations: {num_variations}")
    print(f"{'='*60}\n")

    product_image_urls = []
    product_image_parts = []
    image_files = []

    if product_images_dir.exists() and not dry_run:
        image_files = sorted([
            f for f in product_images_dir.iterdir()
            if f.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp")
        ])
        if image_files:
            if provider == "fal":
                print(f"Uploading {len(image_files)} product image(s) to FAL storage...")
                for img_file in image_files:
                    try:
                        url = upload_image_to_fal(str(img_file))
                        product_image_urls.append(url)
                        print(f"  ✓ {img_file.name}")
                    except Exception as e:
                        print(f"  ✗ {img_file.name}: {e}")
            else:
                print(f"Loading {len(image_files)} product image(s)...")
                for img_file in image_files:
                    try:
                        part = load_image_part_google(str(img_file))
                        product_image_parts.append(part)
                        print(f"  ✓ {img_file.name}")
                    except Exception as e:
                        print(f"  ✗ {img_file.name}: {e}")
            print()
        else:
            print("Warning: No product images found in images dir.\n")

    results = []
    total = len(prompts) * num_variations
    completed = 0
    failed = 0

    if provider == "google-batch" and not dry_run:
        from google import genai
        client = genai.Client(api_key=GEMINI_API_KEY)
        results, completed, failed = run_generation_google_batch(
            client, prompts, product_image_parts, resolution, outputs_dir, brand_name, num_variations
        )
    else:
        for prompt_entry in prompts:
            tpl_num = prompt_entry["template_number"]
            tpl_name = prompt_entry.get("template_name", TEMPLATE_NAMES.get(tpl_num, f"template-{tpl_num}"))
            is_hybrid = "ai_prompt" in prompt_entry
            prompt_text = prompt_entry["ai_prompt"] if is_hybrid else prompt_entry["prompt"]
            product_placement = prompt_entry.get("product_placement") if is_hybrid else None
            aspect_ratio = prompt_entry.get("aspect_ratio", "1:1")
            needs_images = prompt_entry.get("needs_product_images", True)

            folder_name = f"{tpl_num:02d}-{tpl_name}"
            output_folder = outputs_dir / folder_name
            output_folder.mkdir(parents=True, exist_ok=True)

            with open(output_folder / "prompt.txt", "w") as f:
                f.write(prompt_text)

            print(f"[{tpl_num:02d}] {tpl_name}")

            if dry_run:
                print(f"     → DRY RUN: {num_variations} variation(s) | Aspect: {aspect_ratio} | Provider: {provider}")
                print()
                continue

            for var_idx in range(num_variations):
                var_label = f"v{var_idx + 1}" if num_variations > 1 else "v1"

                try:
                    print(f"     → Generating ({var_label}) via {provider}...")

                    if provider == "fal":
                        num_images = 1
                        if needs_images and product_image_urls:
                            endpoint = EDIT_ENDPOINT
                            payload = {
                                "prompt": prompt_text,
                                "image_urls": product_image_urls[:FAL_MAX_IMAGES],
                                "aspect_ratio": aspect_ratio,
                                "num_images": num_images,
                                "output_format": DEFAULT_OUTPUT_FORMAT,
                                "resolution": resolution,
                                "safety_tolerance": "5",
                                "limit_generations": False,
                            }
                        else:
                            endpoint = T2I_ENDPOINT
                            payload = {
                                "prompt": prompt_text,
                                "aspect_ratio": aspect_ratio,
                                "num_images": num_images,
                                "output_format": DEFAULT_OUTPUT_FORMAT,
                                "resolution": resolution,
                                "safety_tolerance": "5",
                                "limit_generations": False,
                            }
                        result = run_generation_fal(endpoint, payload)
                        images = result.get("images", [])
                        if not images:
                            print(f"     ✗ No images returned")
                            failed += 1
                            continue
                        img_url = images[0].get("url", "")
                        if not img_url:
                            print(f"     ✗ No image URL in response")
                            failed += 1
                            continue
                        save_name = f"{tpl_name}_{var_label}_img1.{DEFAULT_OUTPUT_FORMAT}"
                        save_path = output_folder / save_name
                        download_image(img_url, str(save_path))
                        if product_placement and product_image_urls:
                            product_local = image_files[0] if image_files else None
                            if product_local:
                                composite_product(save_path, str(product_local), product_placement, str(save_path))

                    else:
                        image_parts = product_image_parts if (needs_images and product_image_parts) else []
                        img_bytes = run_generation_google(prompt_text, image_parts, aspect_ratio)
                        save_name = f"{tpl_name}_{var_label}_img1.{DEFAULT_OUTPUT_FORMAT}"
                        save_path = output_folder / save_name
                        if product_placement and image_files:
                            composite_product(img_bytes, str(image_files[0]), product_placement, str(save_path))
                        else:
                            with open(save_path, "wb") as f:
                                f.write(img_bytes)

                    print(f"     ✓ Saved: {save_name}")
                    completed += 1
                    results.append({
                        "template": tpl_num,
                        "name": tpl_name,
                        "variation": f"{var_label}_img1",
                        "file": str(save_path),
                    })

                except Exception as e:
                    print(f"     ✗ Error: {e}")
                    failed += 1

            print()

    if not dry_run:
        print(f"\n{'='*60}")
        print(f"  Generation Complete")
        print(f"  ✓ Completed: {completed}/{total}")
        if failed:
            print(f"  ✗ Failed: {failed}/{total}")
        print(f"  Output: {outputs_dir}/")
        print(f"{'='*60}\n")

        manifest = {
            "brand": brand_name,
            "provider": provider,
            "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "resolution": resolution,
            "total_generated": completed,
            "total_failed": failed,
            "results": results,
        }
        manifest_path = outputs_dir / "manifest.json"
        with open(manifest_path, "w") as f:
            json.dump(manifest, f, indent=2)
        print(f"Manifest saved: {manifest_path}")

        generate_gallery(outputs_dir, brand_name, results)


def run_generation_google_batch(client, prompts, product_image_parts, resolution, outputs_dir, brand_name, num_variations):
    try:
        from google.genai import types
        import tempfile
    except ImportError:
        print("Error: 'google-genai' package required. Install with: pip install google-genai")
        sys.exit(1)

    image_size = RESOLUTION_MAP_GOOGLE.get(resolution, "2048x2048")

    request_map = {}
    jsonl_lines = []

    for prompt_entry in prompts:
        tpl_num = prompt_entry["template_number"]
        tpl_name = prompt_entry.get("template_name", TEMPLATE_NAMES.get(tpl_num, f"template-{tpl_num}"))
        prompt_text = prompt_entry["prompt"]
        aspect_ratio = prompt_entry.get("aspect_ratio", "1:1")
        needs_images = prompt_entry.get("needs_product_images", True)

        folder_name = f"{tpl_num:02d}-{tpl_name}"
        output_folder = outputs_dir / folder_name
        output_folder.mkdir(parents=True, exist_ok=True)

        with open(output_folder / "prompt.txt", "w") as f:
            f.write(prompt_text)

        for var_idx in range(num_variations):
            var_label = f"v{var_idx + 1}" if num_variations > 1 else "v1"
            key = f"tpl{tpl_num:02d}_{var_label}"
            request_map[key] = (tpl_num, tpl_name, var_label, output_folder, aspect_ratio)

            parts = []
            if needs_images and product_image_parts:
                for img_part in product_image_parts:
                    parts.append({
                        "inlineData": {
                            "mimeType": img_part.inline_data.mime_type,
                            "data": base64.b64encode(img_part.inline_data.data).decode("utf-8")
                        }
                    })
            parts.append({"text": prompt_text})

            jsonl_lines.append(json.dumps({
                "key": key,
                "request": {
                    "contents": [{"parts": parts}],
                    "generation_config": {
                        "responseModalities": ["IMAGE"],
                        "imageConfig": {"aspectRatio": aspect_ratio, "imageSize": image_size}
                    }
                }
            }))

    with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False) as f:
        f.write("\n".join(jsonl_lines))
        jsonl_path = f.name

    print(f"Uploading batch file ({len(jsonl_lines)} requests)...")
    uploaded_file = client.files.upload(
        file=jsonl_path,
        config=types.UploadFileConfig(display_name=f'{brand_name}-batch', mime_type='jsonl')
    )

    print(f"Submitting batch job...")
    batch_job = client.batches.create(
        model=GEMINI_MODEL_ID,
        src=uploaded_file.name,
        config={"display_name": f"{brand_name}-ads-batch"}
    )
    print(f"Batch job created: {batch_job.name}")
    print(f"Waiting for results (up to 24h, checking every 30s)...\n")

    completed_states = {"JOB_STATE_SUCCEEDED", "JOB_STATE_FAILED", "JOB_STATE_CANCELLED", "JOB_STATE_EXPIRED"}
    while True:
        batch_job = client.batches.get(name=batch_job.name)
        state = batch_job.state.name
        print(f"  Status: {state} ({time.strftime('%H:%M:%S')})")
        if state in completed_states:
            break
        time.sleep(30)

    if batch_job.state.name != "JOB_STATE_SUCCEEDED":
        print(f"  ✗ Batch job failed: {batch_job.state.name}")
        return [], 0, len(request_map)

    result_file = batch_job.dest.file_name
    file_content = client.files.download(file=result_file)
    results = []
    completed = 0
    failed = 0

    for line in file_content.decode("utf-8").splitlines():
        if not line:
            continue
        resp = json.loads(line)
        key = resp.get("key", "")
        if key not in request_map:
            continue
        tpl_num, tpl_name, var_label, output_folder, _ = request_map[key]
        try:
            parts = resp["response"]["candidates"][0]["content"]["parts"]
            img_bytes = None
            for part in parts:
                if "inlineData" in part:
                    img_bytes = base64.b64decode(part["inlineData"]["data"])
                    break
            if not img_bytes:
                print(f"  ✗ [{tpl_num:02d}] {tpl_name}: no image in response")
                failed += 1
                continue
            save_name = f"{tpl_name}_{var_label}_img1.{DEFAULT_OUTPUT_FORMAT}"
            save_path = output_folder / save_name
            with open(save_path, "wb") as f:
                f.write(img_bytes)
            print(f"  ✓ [{tpl_num:02d}] {tpl_name}: {save_name}")
            completed += 1
            results.append({
                "template": tpl_num,
                "name": tpl_name,
                "variation": f"{var_label}_img1",
                "file": str(save_path),
            })
        except Exception as e:
            print(f"  ✗ [{tpl_num:02d}] {tpl_name}: {e}")
            failed += 1

    os.unlink(jsonl_path)
    return results, completed, failed


def generate_gallery(outputs_dir: Path, brand_name: str, results: list):
    html_parts = [f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{brand_name} — Static Ad Gallery</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #0a0a0a; color: #fff; padding: 2rem; }}
  h1 {{ font-size: 1.8rem; margin-bottom: 0.5rem; }}
  .meta {{ color: #888; margin-bottom: 2rem; font-size: 0.9rem; }}
  .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 1.5rem; }}
  .card {{ background: #1a1a1a; border-radius: 12px; overflow: hidden; }}
  .card img {{ width: 100%; display: block; }}
  .card .info {{ padding: 1rem; }}
  .card .info h3 {{ font-size: 0.95rem; margin-bottom: 0.3rem; }}
  .card .info p {{ font-size: 0.8rem; color: #888; }}
</style>
</head>
<body>
<h1>{brand_name} — Static Ad Gallery</h1>
<p class="meta">Generated {time.strftime("%B %d, %Y")} · {len(results)} ads</p>
<div class="grid">
"""]

    for r in results:
        file_path = Path(r["file"])
        rel_path = file_path.relative_to(outputs_dir)
        tpl_num = r["template"]
        tpl_name = r["name"].replace("-", " ").title()
        html_parts.append(f"""  <div class="card">
    <img src="{rel_path}" alt="Template {tpl_num}: {tpl_name}" loading="lazy">
    <div class="info">
      <h3>#{tpl_num:02d} — {tpl_name}</h3>
      <p>{r['variation']}</p>
    </div>
  </div>
""")

    html_parts.append("</div>\n</body>\n</html>")

    gallery_path = outputs_dir / "gallery.html"
    with open(gallery_path, "w") as f:
        f.write("".join(html_parts))
    print(f"Gallery saved: {gallery_path}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Generate static ads via Nano Banana 2")
    parser.add_argument("--provider", type=str, default=None, choices=["fal", "google", "google-batch"],
        help="Image generation provider: fal or google (default: interactive selection)")
    parser.add_argument("--templates", type=str, default=None,
        help="Comma-separated template numbers to generate (e.g., 1,7,13,15)")
    parser.add_argument("--resolution", type=str, default=DEFAULT_RESOLUTION,
        choices=["0.5K", "1K", "2K", "4K"], help="Image resolution (default: 2K)")
    parser.add_argument("--variations", type=int, default=1,
        help="Number of variations per template (default: 1)")
    parser.add_argument("--dry-run", action="store_true",
        help="Show what would be generated without calling the API")
    parser.add_argument("--brand-dir", type=str, default=".",
        help="Path to the brand folder (default: current directory)")
    parser.add_argument("--prompts-file", type=str, default=None,
        help="Path to prompts JSON file, relative to brand-dir or absolute")
    parser.add_argument("--images-dir", type=str, default=None,
        help="Path to product images folder, relative to brand-dir or absolute")
    parser.add_argument("--output-dir", type=str, default=None,
        help="Path to output folder, relative to brand-dir or absolute")
    parser.add_argument("--lang", type=str, default="sk",
        help="Language/country code for auto-generated output folder name (default: sk)")

    args = parser.parse_args()

    provider = args.provider if args.provider else select_provider()

    templates_filter = None
    if args.templates:
        templates_filter = [int(t.strip()) for t in args.templates.split(",")]

    output_dir = args.output_dir
    if output_dir is None and args.images_dir:
        date_suffix = time.strftime("%y%m%d")
        images_path = Path(args.images_dir)
        product_name = images_path.name
        output_dir = str(images_path / f"{product_name}-outputs" / f"{args.lang}-{date_suffix}")

    generate_ads(
        provider=provider,
        brand_dir=args.brand_dir,
        prompts_file=args.prompts_file,
        images_dir=args.images_dir,
        output_dir=output_dir,
        templates_filter=templates_filter,
        resolution=args.resolution,
        num_variations=args.variations,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    main()
