"""Run from the installed drumtool directory. Explicit slot numbers prevent accidental remapping."""
import argparse
import subprocess
import wave
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("folder", type=Path)
parser.add_argument("--write", action="store_true")
args = parser.parse_args()
files = sorted(args.folder.glob("*/*.wav"))
if not Path("drumtool.js").is_file():
    parser.error("Run from the upstream tools/drumtool directory.")
slots = {}
for file in files:
    slot = int(file.name.split("_", 1)[0])
    if slot in slots:
        parser.error(f"Duplicate slot {slot}")
    with wave.open(str(file), "rb") as wav:
        if (wav.getframerate(), wav.getnchannels(), wav.getsampwidth()) != (44100, 1, 2) or not 0 < wav.getnframes() <= 39690:
            parser.error(f"Unexpected WAV format or duration: {file}")
    slots[slot] = file.resolve()
if sorted(slots) != list(range(30, 94)):
    parser.error("Expected exactly slots 30 through 93 across the two bank folders.")
for slot, file in sorted(slots.items()):
    print(f"{slot} <- {file.name}", flush=True)
    if args.write:
        subprocess.run(["node", "drumtool.js", "send", f"{file}:{slot}", "44100"], check=True)
