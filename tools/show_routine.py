#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# ///
"""Show one routine's instructions for the inline-comment grind.

For each item in a routine (from its label or start address up to the
next declared subroutine / named region), prints the address, the
disassembled instruction, whether it already has an inline comment, and
J.G. Harston's comment for that address as a cross-reference. Lines
lacking a comment are flagged so nothing is missed on the way to full
coverage.

Usage:
  uv run tools/show_routine.py skip_spaces
  uv run tools/show_routine.py 0x8a97
  uv run tools/show_routine.py 0x8a97 0x8ab0     # explicit address range
"""
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JSON = ROOT / "versions/basic-2/output/basic-2.json"
JGH = ROOT / "tools/jgh_correlation.tsv"


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    data = json.loads(JSON.read_text())
    items = sorted(data["items"], key=lambda x: x["addr"])
    labels = {l: it["addr"] for it in items for l in it.get("labels", [])}

    jgh = {}
    if JGH.exists():
        for line in JGH.read_text().splitlines():
            a, _mn, c = line.split("\t", 2)
            jgh[int(a, 16)] = c

    target = sys.argv[1]
    start = labels[target] if target in labels else int(target, 16)
    if len(sys.argv) >= 3:
        end = int(sys.argv[2], 16)
    else:
        # up to the next item carrying a non-auto label (next routine)
        end = 0x10000
        for it in items:
            if it["addr"] > start and any(
                not (l[0] in "cl" and l[1:].isalnum() and
                     l.lstrip("cl").rstrip("0123456789abcdef") == "")
                for l in it.get("labels", [])
            ):
                end = it["addr"] - 1
                break

    n_code = n_done = 0
    for it in items:
        a = it["addr"]
        if a < start or a > end:
            continue
        labs = " ".join("." + l for l in it.get("labels", []))
        if it["type"] != "code":
            print(f"  {a:04X}  [{it['type']}] {labs}")
            continue
        n_code += 1
        op = it["mnemonic"] + (" " + it["operand"] if it.get("operand") else "")
        has = it.get("comment_inline")
        if has:
            n_done += 1
        flag = "  " if has else ">>"
        cur = f"  ;= {has}" if has else ""
        hint = f"   [jgh: {jgh[a]}]" if a in jgh and not has else ""
        print(f"{flag}{a:04X}  {op:22s}{labs}{cur}{hint}")
    print(f"\n  {n_done}/{n_code} instructions commented"
          f"{' — COMPLETE' if n_done == n_code and n_code else ''}")


if __name__ == "__main__":
    main()
