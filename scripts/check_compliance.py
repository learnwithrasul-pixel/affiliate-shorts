"""Pre-publish check for German/EU ad rules on a short video and its caption.

Usage: python scripts/check_compliance.py public/projects/<name>/video.json [caption.txt]

Not legal advice. It catches the common mistakes creators get fined for:
  - missing ad label ("Werbung" / "Anzeige") on video and caption
  - discount claims without the lowest price of the last 30 days (§ 11 PAngV)
  - prices without a date
  - Amazon links without the required Amazon Associates sentence
Exit code 1 if any check FAILS, so it can gate a render.
"""

import json
import re
import sys
from pathlib import Path

AD_LABEL = re.compile(r"\b(werbung|anzeige|eigenes angebot)\b", re.I)
DISCOUNT = re.compile(r"(\d+\s?%|rabatt|reduziert|statt\s+\d|spare|sparen|sale\b|deal\b|uvp)", re.I)
LOWEST_30 = re.compile(r"(niedrigste[rn]? (gesamt)?preis.{0,40}30 tage|30.?tage.?(best|tiefst)preis)", re.I)
PRICE = re.compile(r"\d[\d.,]*\s?(€|eur\b|euro)", re.I)
DATE = re.compile(r"(stand|preis am|abgerufen)\s*:?\s*\d{1,2}\.\d{1,2}\.\d{2,4}", re.I)
AMAZON = re.compile(r"(amazon\.|amzn\.)", re.I)
AMAZON_SENTENCE = re.compile(r"als amazon-partner verdiene ich an qualifizierten verkäufen", re.I)
AFFILIATE_MARK = re.compile(r"\*\s?(affiliate|werbe)", re.I)

FAIL, WARN, OK = "FAIL", "WARN", "OK"


def video_text(video: dict) -> str:
    parts = [video.get("label", ""), video.get("footer", "")]
    for s in video.get("scenes", []):
        parts += [s.get("headline", ""), s.get("sub", ""), s.get("voice", "")]
    return "\n".join(p for p in parts if p)


def check(video: dict, caption: str) -> list[tuple[str, str]]:
    results = []
    on_screen = video_text(video)
    everything = on_screen + "\n" + caption

    # 1. Ad label must be on screen for the whole video; the composition shows `label` throughout.
    if AD_LABEL.search(video.get("label", "")):
        results.append((OK, f"On-screen ad label: \"{video['label']}\""))
    else:
        results.append((FAIL, "Set \"label\" to \"Werbung\" or \"Anzeige\" (shown for the whole video)."))

    if caption:
        if AD_LABEL.search(caption):
            results.append((OK, "Caption contains an ad label."))
        else:
            results.append((FAIL, "Caption needs \"Werbung\" or \"Anzeige\"."))
        if AFFILIATE_MARK.search(caption):
            results.append((OK, "Affiliate link is marked with * and an explanation."))
        else:
            results.append((WARN, "Mark affiliate links with * plus a short explanation, e.g. \"*Affiliate-Link\"."))

    # 2. Discount claims need the lowest price of the last 30 days (§ 11 PAngV).
    if DISCOUNT.search(everything):
        if LOWEST_30.search(everything):
            results.append((OK, "Discount claim comes with the 30-day lowest price."))
        else:
            hit = DISCOUNT.search(everything).group(0)
            results.append((FAIL, f"Discount wording (\"{hit}\") without the lowest price of the last 30 days. "
                                  "Show it clearly or drop the discount claim."))

    # 3. Prices change: date every price.
    if PRICE.search(everything):
        if DATE.search(everything):
            results.append((OK, "Price is dated."))
        else:
            results.append((WARN, "Add a date to the price, e.g. \"Stand 22.10.2026\"."))

    # 4. Amazon Associates disclosure.
    if AMAZON.search(everything):
        if AMAZON_SENTENCE.search(everything):
            results.append((OK, "Amazon Associates sentence present."))
        else:
            results.append((FAIL, "Amazon link found: add \"Als Amazon-Partner verdiene ich an qualifizierten "
                                  "Verkäufen.\" to the caption or your bio."))

    # 5. Reminders the script cannot verify.
    if any(s.get("voice") for s in video.get("scenes", [])):
        results.append((WARN, "Synthetic voice: turn on the platform's AI-generated content label when posting."))
    results.append((WARN, "Use only images you own or the brand/affiliate network allows you to use."))
    return results


def main() -> None:
    if len(sys.argv) not in (2, 3):
        sys.exit(__doc__)
    video_path = Path(sys.argv[1])
    video = json.loads(video_path.read_text(encoding="utf-8"))
    caption_path = Path(sys.argv[2]) if len(sys.argv) == 3 else video_path.parent / "caption.txt"
    caption = caption_path.read_text(encoding="utf-8") if caption_path.exists() else ""
    if not caption:
        print("WARN  No caption.txt found; only the video text was checked.")

    results = check(video, caption)
    for level, msg in results:
        print(f"{level:<5} {msg}")
    print("\nNot legal advice. Rules: Leitfaden der Medienanstalten, § 11 PAngV.")
    sys.exit(1 if any(level == FAIL for level, _ in results) else 0)


if __name__ == "__main__":
    main()
