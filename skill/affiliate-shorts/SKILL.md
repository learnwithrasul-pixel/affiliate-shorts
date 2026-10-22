---
name: affiliate-shorts
description: Turn a product link into a 9:16 short video (TikTok, Reels, Shorts) with free local voice-over and German/EU ad-labelling checks. Use when the user wants a product video, affiliate short, deal video, or "Video aus Produktlink".
---

# Affiliate Shorts

Product link → script → local voice-over → 1080×1920 video → compliance check.
Runs entirely on the user's machine. No API keys.

Repository root: the folder that contains `package.json` and `scripts/` (ask the user if unsure).

## 1. Collect facts (never invent them)
1. Read the product page the user gives you. Note: exact product name, current price, the page's date, and 2–3 key specs **as written on the page**.
2. If the page shows a crossed-out price, look for the lowest price of the last 30 days. If the page doesn't state it, **do not** make any discount claim ("-50 %", "statt", "Rabatt").
3. Ask the user which image to use. Prefer their own photo or images the brand / affiliate network allows. Copy it to `public/projects/<slug>/`.
4. Ask whether the link is an affiliate link, the user's own product, or neither. This sets `label`: `Werbung` (affiliate/sponsored) or `Eigenes Angebot` (own shop).

## 2. Write `public/projects/<slug>/video.json`
4–5 scenes, 15–25 seconds total. Scene 1 is the hook (max ~6 words on screen). Last scene asks a question to drive comments.

```json
{
  "label": "Werbung",
  "footer": "Preis kann sich ändern · Link in Bio",
  "accent": "#E8382F",
  "voiceModel": "de_DE-thorsten-medium",
  "scenes": [
    { "image": "projects/<slug>/product.png", "headline": "Hook", "voice": "Spoken line", "seconds": 3 },
    { "image": "projects/<slug>/product.png", "headline": "719 €", "sub": "Stand 22.10.2026", "voice": "…", "seconds": 3, "highlight": true }
  ]
}
```

- Write numbers in `voice` as words so the TTS reads them right ("siebenhundertneunzehn Euro").
- Every price on screen carries a date (`Stand DD.MM.YYYY`).
- Other voices: any Piper model name, e.g. `en_US-lessac-medium`, `fr_FR-siwis-medium`.

Also write `public/projects/<slug>/caption.txt`: 1–2 sentences, the dated price, `#Werbung *Affiliate-Link in Bio` (or the own-shop equivalent), 4–6 hashtags. If any link goes to Amazon, add: „Als Amazon-Partner verdiene ich an qualifizierten Verkäufen."

## 3. Check, voice, render
```bash
python scripts/check_compliance.py public/projects/<slug>/video.json
python scripts/make_voice.py public/projects/<slug>/video.json
npx remotion render src/index.tsx ProductShort out/<slug>.mp4 --props=public/projects/<slug>/video.json
```
If the check reports `FAIL`, fix the text before rendering. Show the user every `WARN`.

## 4. Hand over
Give the user the path to `out/<slug>.mp4` and the caption. **Do not post anything yourself.** Remind them to switch on the platform's AI-generated content label (synthetic voice).

## Rules
- No fake discounts, no invented specs, no invented reviews or "I tested it" claims unless the user did.
- Not legal advice; the checker covers common German rules (Medienanstalten guideline, § 11 PAngV) only.
