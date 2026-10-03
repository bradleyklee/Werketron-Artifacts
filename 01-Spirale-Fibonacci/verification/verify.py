#!/usr/bin/env python3
"""Run common public checks against both exported candidates."""

from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
CANDIDATES = {
    "Luna": ROOT / "candidates/luna/spirale_fibonacci.py",
    "Sol": ROOT / "candidates/sol/spirale_fibonacci.py",
}

for name, program in CANDIDATES.items():
    for n in range(2, 12):
        for option in ("--verifica", "--griglia", ""):
            command = [sys.executable, str(program), str(n)]
            if option:
                command.append(option)
            result = subprocess.run(command, capture_output=True, check=True)
            if not result.stdout or result.stderr:
                raise SystemExit(f"{name} N={n} {option or 'Braille'} failed")
        print(f"{name} N={n}: PASS")

print("All common candidate checks passed.")
