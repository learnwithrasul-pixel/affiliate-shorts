"""Turn each scene's `voice` text into a local Piper TTS clip and fit scene length to it.

Usage: python scripts/make_voice.py public/projects/<name>/video.json

Writes <scene>.wav next to video.json, then updates each scene's `audio` and
`seconds` in place. Free and offline after the first voice download.
"""

import json
import subprocess
import sys
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"
VOICES = ROOT / "voices"
PADDING = 0.5  # seconds of silence after each line


def ensure_voice(model: str) -> None:
    if (VOICES / f"{model}.onnx").exists():
        return
    VOICES.mkdir(exist_ok=True)
    subprocess.run(
        [sys.executable, "-m", "piper.download_voices", "--download-dir", str(VOICES), model],
        check=True,
    )


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    video_path = Path(sys.argv[1]).resolve()
    video = json.loads(video_path.read_text(encoding="utf-8"))
    model = video.get("voiceModel", "de_DE-thorsten-medium")
    speed = float(video.get("voiceSpeed", 0.92))  # piper length_scale: <1 = faster
    ensure_voice(model)

    for i, scene in enumerate(video["scenes"], start=1):
        text = scene.get("voice")
        if not text:
            continue
        wav = video_path.parent / f"vo{i}.wav"
        subprocess.run(
            [sys.executable, "-m", "piper", "--data-dir", str(VOICES), "-m", model,
             "--length-scale", str(speed), "-f", str(wav)],
            input=text.encode("utf-8"),
            check=True,
            capture_output=True,
        )
        with wave.open(str(wav)) as w:
            length = w.getnframes() / w.getframerate()
        scene["audio"] = wav.relative_to(PUBLIC).as_posix()
        scene["seconds"] = round(max(scene.get("minSeconds", 2.0), length + PADDING), 2)
        print(f"scene {i}: {length:.2f}s  {text}")

    video_path.write_text(json.dumps(video, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    total = sum(s["seconds"] for s in video["scenes"])
    print(f"total: {total:.1f}s -> {video_path}")


if __name__ == "__main__":
    main()
