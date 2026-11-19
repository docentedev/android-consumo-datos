#!/usr/bin/env python3
"""Genera la narración en español con Kokoro (modelo local) y la ajusta a cada escena."""
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VOICE_DIR = ROOT / "assets" / "voice"
VOICE_DIR.mkdir(parents=True, exist_ok=True)
CONFIG = json.loads((ROOT / "narration.json").read_text(encoding="utf-8"))
ENV = dict(os.environ)
ENV["HYPERFRAMES_PYTHON"] = os.environ.get(
    "HYPERFRAMES_PYTHON",
    "/private/var/folders/zd/1m_06bd13ys71kc1rvpz_gv00000gn/T/opencode/kokoro-venv/bin/python3",
)


def synthesize(text, voice, lang, speed, out):
    txt = VOICE_DIR / "_line.txt"
    txt.write_text(text, encoding="utf-8")
    proc = subprocess.run(
        ["npx", "hyperframes", "tts", "--text-file", str(txt),
         "--voice", voice, "--lang", lang, "--speed", f"{speed:.3f}",
         "-o", str(out), "--json"],
        cwd=ROOT, env=ENV, capture_output=True, text=True,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"TTS falló: {proc.stdout}\n{proc.stderr}")
    payload = json.loads(proc.stdout.strip().splitlines()[-1])
    if not payload.get("ok"):
        raise RuntimeError(f"TTS devolvió error: {payload}")
    return float(payload["durationSeconds"])


meta = {"voice": CONFIG["voice"], "lang": CONFIG["lang"], "scenes": []}
for sc in CONFIG["scenes"]:
    target = sc["duration"] - 0.7
    speed = float(sc.get("speed", CONFIG["speed"]))
    out = VOICE_DIR / f"{sc['id']}.wav"
    measured = synthesize(sc["text"], CONFIG["voice"], CONFIG["lang"], speed, out)
    if "speed" not in sc:
        # Ajuste iterativo: que la voz termine justo antes del corte de escena.
        for _ in range(5):
            error = measured - target
            if abs(error) < 0.6:
                break
            factor = 0.995 if error > 0 else 1.005
            candidate = round(speed * measured / target * factor, 3)
            if not (0.6 <= candidate <= 1.4):
                break
            speed = candidate
            measured = synthesize(sc["text"], CONFIG["voice"], CONFIG["lang"], speed, out)
    meta["scenes"].append({
        "id": sc["id"],
        "start": sc["start"],
        "window": sc["duration"],
        "duration": round(measured, 3),
        "speed": speed,
        "file": f"assets/voice/{sc['id']}.wav",
    })
    print(f"{sc['id']:18s} {measured:6.2f}s / {target:5.2f}s  speed={speed:.3f}", flush=True)

(VOICE_DIR / "meta.json").write_text(
    json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print(f"Narración total: {sum(s['duration'] for s in meta['scenes']):.1f}s")
