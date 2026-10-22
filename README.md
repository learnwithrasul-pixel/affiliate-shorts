# Affiliate Shorts 🎬

**Product link → 20-second vertical video with voice-over, ready for TikTok / Reels / Shorts.
Free, local, and with German/EU ad rules checked before you post.**

Built by an eBay seller in Germany who wanted to make one product video a day without paying for video tools, and without getting fined for a missing „Werbung" label.

| | |
|---|---|
| 💸 **Free** | Local text-to-speech ([Piper](https://github.com/rhasspy/piper)) + [Remotion](https://www.remotion.dev). No API keys, no subscriptions. |
| ⚖️ **Compliance built in** | Checks ad labels, fake-discount claims (§ 11 PAngV, 30-day lowest price), undated prices and the Amazon Associates sentence. |
| 🤖 **Claude Code skill** | Give Claude a product link; it collects facts, writes the script, checks, voices and renders. |
| 🗣️ **Any language** | German by default; swap in any Piper voice. |

## Quick start

Requirements: Node.js 18+, Python 3.10+.

```bash
git clone https://github.com/learnwithrasul-pixel/affiliate-shorts.git
cd affiliate-shorts
npm install
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

Render the demo:

```bash
python scripts/check_compliance.py public/projects/demo/video.json
python scripts/make_voice.py public/projects/demo/video.json
npx remotion render src/index.tsx ProductShort out/demo.mp4 --props=public/projects/demo/video.json
```

The first voice run downloads the Piper voice (~60 MB) into `voices/`.

## Use it with Claude Code

```bash
mkdir -p ~/.claude/skills && cp -r skill/affiliate-shorts ~/.claude/skills/
```

Then, inside this folder, ask Claude: *"Make an affiliate short for <product link>."*
Claude never posts for you; you get the `.mp4` and a caption.

## Make your own video

1. Create `public/projects/<name>/` with your product image.
2. Write `video.json` (copy the demo): each scene has an `image`, a `headline`, an optional `sub` line and the `voice` text.
3. Run the three commands above with your folder name.

## What the checker catches

```
FAIL  Discount wording ("50%") without the lowest price of the last 30 days.
FAIL  Amazon link found: add "Als Amazon-Partner verdiene ich an qualifizierten Verkäufen."
WARN  Add a date to the price, e.g. "Stand 22.10.2026".
WARN  Synthetic voice: turn on the platform's AI-generated content label when posting.
```

## Good to know

- **Not legal advice.** The checker covers common German rules (Leitfaden der Medienanstalten, § 11 PAngV). Ask a lawyer for your specific case.
- **Images:** use your own photos or images the brand or affiliate network lets you use.
- **Remotion license:** Remotion is free for individuals and companies with up to 3 employees; larger companies need a [company license](https://www.remotion.dev/license).
- **Piper voices** have their own licenses; check the voice's model card.
- **Voice error `phontab: No such file or directory`?** Piper's bundled espeak can't handle very long folder paths. Clone the repo to a short path such as `~/affiliate-shorts`.

## Kurz auf Deutsch

Produktlink rein, 20-Sekunden-Hochkantvideo raus, mit deutscher Stimme, kostenlos und lokal. Vor dem Rendern prüft ein Skript Werbekennzeichnung, Fake-Rabatte (30-Tage-Bestpreis) und Preisdatum. Keine Rechtsberatung.

## License

MIT. See [LICENSE](LICENSE).
