# Ad Swipe: Competitor Ad Reverse-Engineering

## What this does

Takes a competitor's ad image, deconstructs every creative decision, and rebuilds it as a ready-to-generate prompt for YOUR brand with the correct copy for your persona, angle, and emotion. The output is a complete Nano Banana prompt you can paste directly into an image generator.

## How to use

1. Upload a competitor ad image
2. Provide: your brand name, product, persona, angle, emotion
3. Reference your brand spec sheet and product images
4. This system will deconstruct the competitor ad and output a finished prompt

---

## Stage 1: Deconstruct the competitor ad

When a competitor ad image is uploaded, analyze and extract the following:

### Layout analysis
```
{
  "aspect_ratio": "",
  "format_type": "headline | before-after | testimonial | social-proof | us-vs-them | statistics | features-benefits | bullet-points | press | news | ugc | founder-story | carousel | handwriting | negative-marketing | other",
  "style_match": "Which style (A/B/C/D) from the matched format spec best describes this ad",
  "composition": {
    "text_position": "top-third | center | bottom-third | left-aligned | right-aligned | overlaid",
    "product_position": "center | left | right | top | bottom | absent | background",
    "product_frame_percentage": "estimated % of frame the product occupies",
    "negative_space": "minimal | moderate | generous",
    "visual_hierarchy": "What the eye reads first, second, third"
  }
}
```

### Typography extraction
```
{
  "headline_treatment": {
    "case": "uppercase | lowercase | title case | sentence case",
    "estimated_font_category": "sans-serif geometric | sans-serif humanist | serif modern | serif traditional | slab serif | display | handwritten | monospace",
    "weight": "light | regular | medium | bold | black",
    "alignment": "left | center | right",
    "letter_spacing": "tight | normal | wide | very wide",
    "line_count": "",
    "color": "describe the color"
  },
  "subhead_treatment": "same structure as above, or 'none'",
  "body_treatment": "same structure as above, or 'none'",
  "cta_treatment": {
    "shape": "rounded | pill | sharp corners | no button (text only)",
    "fill": "solid color | outline | ghost",
    "text_case": "uppercase | sentence case",
    "color": "describe fill and text colors"
  }
}
```

### Color and mood extraction
```
{
  "background": {
    "type": "solid color | gradient | photograph | texture | pattern",
    "dominant_color": "",
    "secondary_color": ""
  },
  "color_palette": ["list all visible colors"],
  "lighting": "flat | soft natural | dramatic side | overhead | backlit | warm golden | cool blue",
  "mood": "1-3 adjectives describing the emotional feel",
  "energy_level": "quiet and restrained | confident and direct | bold and loud | playful and energetic | premium and elevated | urgent and high-pressure"
}
```

### Copy extraction
```
{
  "text_elements": [
    {
      "role": "headline | subhead | body | label | cta | proof | offer | badge",
      "text": "exact text as rendered",
      "word_count": "",
      "position_in_frame": ""
    }
  ],
  "total_text_elements": "",
  "copy_strategy": "What is the ad actually arguing? What is the single message?",
  "emotional_register": "What emotion is it trying to trigger?",
  "proof_mechanism": "How does it prove its claim? (social proof, statistic, authority, demonstration, testimonial, none)"
}
```

### What makes this ad work (or not)
```
{
  "strongest_element": "The single best creative decision in this ad",
  "weakest_element": "The single worst creative decision",
  "visual_copy_coherence": "Does the image reinforce the copy's concept? Yes/No and why",
  "scroll_stop_factor": "What would make someone stop scrolling? Rate 1-10",
  "steal_worthy": ["List 1-3 specific techniques worth borrowing"]
}
```

---

## Stage 2: Rebuild for your brand

Using the deconstruction above, generate a complete ad prompt that:
1. Keeps the structural techniques that work (layout, composition, visual hierarchy)
2. Replaces all copy with YOUR brand's copy matched to the specified persona/angle/emotion
3. Applies YOUR brand's visual system (fonts, colors, imagery style) from the uploaded spec sheet
4. Maintains YOUR brand's text element limits from the matched format spec
5. Passes Agent 7 (Copy Editor) checklist before output

### Rebuild template

```
You are generating a social media ad creative. The output must be a finished, publication-ready image at [ASPECT RATIO] with all copy rendered directly in the image using the brand's fonts from the uploaded spec sheet.

CREATIVE ORIGIN:
This ad is inspired by a competitor's creative approach. We are borrowing the STRUCTURE and COMPOSITION techniques, not the copy, colors, or brand identity. The structural techniques being borrowed are: [LIST STEAL-WORTHY TECHNIQUES FROM DECONSTRUCTION].

BRAND CONTEXT:
This is [BRAND NAME]. Reference the uploaded brand spec sheet for all visual identity decisions.
- Fonts: [FROM SPEC SHEET]
- Colors: [FROM SPEC SHEET]
- Voice: [FROM BRAND BRIEF]

PERSONA: [PERSONA NAME AND DESCRIPTION]
ANGLE: [ANGLE]
EMOTION: [EMOTION]
PRODUCT: [PRODUCT NAME AND KEY DETAILS]

COMPOSITION:
One continuous image filling the entire frame at [ASPECT RATIO].

[MAP THE COMPETITOR'S LAYOUT TO YOUR BRAND]:
- Product position: [MATCH COMPETITOR'S PRODUCT POSITION, USING YOUR PRODUCT]
- Text position: [MATCH COMPETITOR'S TEXT POSITION]
- Visual hierarchy: [MATCH COMPETITOR'S READING ORDER]
- Negative space: [MATCH COMPETITOR'S SPACING APPROACH]

COPY ELEMENTS:
This ad has exactly [N] text elements. No more.

[For each text element, mapped from the competitor's structure]:
1. [ROLE]: "[YOUR COPY]"
   - Font: [FROM SPEC SHEET]
   - Color: [FROM SPEC SHEET]
   - Treatment: [MATCH COMPETITOR'S TREATMENT - case, weight, spacing]

[Continue for each element]

SAFE ZONES:
Top 270px and bottom 340px of the frame kept clear of critical content. Left margin 40px. Right margin 120px from y=600 downward.

PRIMARY CONTENT ZONE: All critical content within x=40-960, y=270-1580.

COLOR AND TREATMENT:
Background: [YOUR BRAND'S BACKGROUND, NOT THE COMPETITOR'S]
Lighting: [MATCH COMPETITOR'S LIGHTING APPROACH, ADAPTED TO YOUR BRAND PALETTE]
The overall color treatment should feel like YOUR brand, even though the layout borrows from the competitor's structure.

BRAND IDENTITY:
Logo placed per brand spec sheet rules.

PHOTOGRAPHY DIRECTION:
[YOUR BRAND'S PHOTOGRAPHY STYLE]. The product must be accurately represented per the uploaded product image.

MOOD:
[MATCH THE COMPETITOR'S ENERGY LEVEL, FILTERED THROUGH YOUR BRAND'S VOICE].
The ad should feel like it was conceived natively for your brand, not like a reskin of someone else's creative.

RULES:
1. Exactly [N] text elements. No more. No offer bars, financing lines, or extra proof unless defined in the format spec.
2. Reference the uploaded brand spec sheet for ALL visual identity decisions.
3. The product must be accurately represented per the uploaded product image.
4. All critical content within the primary content zone.
5. No text smaller than 24px at 1080px width.
6. One continuous image. No panels, borders, or grid lines.
7. No em dashes anywhere in rendered copy.
8. Every data point (price, stat, claim) appears exactly once.
9. This must look like YOUR brand's ad, not a copy of the competitor's.
```

---

## Stage 3: Copy generation for the rebuild

Before inserting copy into the prompt, generate it using this framework:

### Copy generation inputs
- **Format**: [Matched format from deconstruction]
- **Style**: [Matched style from deconstruction]
- **Persona**: [User-provided]
- **Angle**: [User-provided]
- **Emotion**: [User-provided]
- **Product**: [User-provided]
- **Word count constraints**: [From the matched format spec's copy template]

### Copy generation process
1. Load the matched format spec (.md file)
2. Use the copy template from the matched style
3. Write copy that fits the persona/angle/emotion
4. Verify against word count limits from the template
5. Run Agent 7 checklist:
   - Grammar check (subject-verb agreement, tense)
   - Spelling check (including brand name capitalization)
   - Punctuation check
   - Banned characters (no em dashes, no en dashes, no semicolons in headlines)
   - Number consistency
   - Duplicate content check (no data point appears twice)
   - Word count compliance (every element within spec)
6. Output the copy mapped to each text element slot

---

## Example workflow

**Input**: User uploads a Caraway cookware ad showing a pink pan on a marble counter with the headline "Cook Without Compromise" and subline "Non-toxic ceramic coating. Naturally nonstick."

**Stage 1 output**: Format = Headline, Style A. Product center, headline top-third, clean background, warm lighting. 3 text elements (headline, subhead, logo). Steal-worthy: the generous negative space and warm domestic lighting.

**Stage 2 output**: Rebuild prompt using YOUR brand's spec sheet, YOUR product image, YOUR copy. Same layout structure (product center, headline top-third, 3 elements) but with your brand's fonts, colors, and voice.

**Stage 3 output**: Copy generated for your persona/angle/emotion, verified against headline format spec word counts, passed Agent 7.

**Final output**: A complete Nano Banana prompt ready to paste.

---

## Rules

1. Never copy a competitor's actual copy, tagline, or brand-specific language
2. The structural techniques are what we borrow, not the creative content
3. The output must pass YOUR brand's format spec constraints, not the competitor's
4. Agent 7 must sign off on all copy before it enters the prompt
5. The final ad must look like it was conceived for your brand from scratch
6. If the competitor ad uses a format/style not in our spec library, flag it and suggest the closest match
7. Always specify which format .md file the rebuild maps to
