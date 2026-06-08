#!/usr/bin/env python3
"""Show uncommented code instructions in an address range, with JGH cross-ref.
Usage: uv run tools/gaps.py 0x937a 0x9432
"""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
d = json.loads((ROOT/"versions/basic-2/output/basic-2.json").read_text())
jgh = {}
jf = ROOT/"tools/jgh_correlation.tsv"
if jf.exists():
    for line in jf.read_text().splitlines():
        a,_mn,c = line.split("\t",2); jgh[int(a,16)] = c
lo, hi = int(sys.argv[1],16), int(sys.argv[2],16)
for it in sorted(d["items"], key=lambda x:x["addr"]):
    a = it["addr"]
    if not (lo <= a < hi): continue
    labs = " ".join("."+l for l in it.get("labels",[]))
    if it["type"]!="code":
        print(f"  {a:04x} [{it['type']}] {labs}"); continue
    op = it["mnemonic"]+(" "+it.get("operand","") if it.get("operand") else "")
    if it.get("comment_inline"):
        print(f"     {a:04x} {op:24s} {labs}  ;= {it['comment_inline'][:40]}")
    else:
        h = f"   [jgh: {jgh[a]}]" if a in jgh else ""
        print(f">>>  {a:04x} {op:24s} {labs}{h}")
