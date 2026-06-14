#!/usr/bin/env python3
"""Report subroutine *banner* documentation quality for BASIC II.

The inline-comment pass is complete; this is the companion pass that
reviews and enriches each subroutine's banner (the block comment that
dasmos renders from ``d.subroutine(title=..., description=...,
on_entry=..., on_exit=...)``).

A banner should describe, at a higher level than the inline comments,
*what* the routine does and *how to call it* -- in particular its
register and zero-page contract via the structured ``on_entry`` /
``on_exit`` dicts.

A ROM routine is considered DONE here when it has BOTH a description and
at least one of on_entry/on_exit (its calling contract). The driver is
the single source of truth, so re-running this after each batch shows
what remains -- the pass is interruptible and resumable. (Description
*accuracy* is a human judgement the tool can't measure; review it as you
add the contract.)

Only ROM-image routines (&8000-&BFFF) with a name we gave are in scope;
the OS vectors (osbyte/osword/... at &FFxx) are declared by the
acorn_mos environment and are out of scope.

Ordering is leaves-first (call-graph depth ascending) when a depth TSV
is present -- document callees before callers so each contract can lean
on the contracts it calls. Generate the TSV once with:

    uv run fantasm cfg depth 2 --no-header > /tmp/cfg_depth.tsv

Usage:
    uv run tools/banner_status.py            # summary + remaining work
    uv run tools/banner_status.py --all      # every in-scope routine
    uv run tools/banner_status.py --name N   # show one routine's banner
"""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JSON_FILEPATH = ROOT / "versions/basic-2/output/basic-2.json"
DEPTH_TSV_FILEPATH = Path("/tmp/cfg_depth.tsv")

ROM_LO, ROM_HI = 0x8000, 0xC000

# Data tables that carry a banner but have no calling contract to state.
DATA_TABLES = {"keyword_table"}


def load_depths() -> dict[int, int]:
    """addr -> call-graph depth (leaves low). Empty if unavailable."""
    text = ""
    if DEPTH_TSV_FILEPATH.exists():
        text = DEPTH_TSV_FILEPATH.read_text()
    else:
        try:
            text = subprocess.run(
                ["uv", "run", "fantasm", "cfg", "depth", "2", "--no-header"],
                capture_output=True, text=True, cwd=ROOT, timeout=120,
            ).stdout
        except Exception:
            return {}
    depths: dict[int, int] = {}
    for line in text.splitlines():
        parts = line.split("\t")
        if len(parts) >= 2 and parts[0].lstrip("-").isdigit():
            try:
                depths[int(parts[1], 16)] = int(parts[0])
            except ValueError:
                pass
    return depths


def in_scope(s: dict) -> bool:
    addr = s["addr"]
    if not (ROM_LO <= addr < ROM_HI):
        return False
    if not s.get("title"):
        return False
    if s.get("name") in DATA_TABLES:
        return False
    return True


def classify(s: dict) -> tuple[bool, bool, bool]:
    has_desc = bool(s.get("description"))
    has_entry = bool(s.get("on_entry"))
    has_exit = bool(s.get("on_exit"))
    return has_desc, has_entry, has_exit


def is_done(s: dict) -> bool:
    has_desc, has_entry, has_exit = classify(s)
    return has_desc and (has_entry or has_exit)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true",
                    help="list every in-scope routine, done or not")
    ap.add_argument("--name", metavar="NAME",
                    help="dump one routine's current banner fields")
    args = ap.parse_args()

    data = json.loads(JSON_FILEPATH.read_text())
    subs = [s for s in data["subroutines"] if in_scope(s)]
    depths = load_depths()

    if args.name:
        for s in data["subroutines"]:
            if s.get("name") == args.name:
                for k in ("addr", "name", "title", "description",
                          "on_entry", "on_exit"):
                    v = s.get(k)
                    if k == "addr":
                        v = f"&{v:04X}"
                    print(f"{k}: {v!r}")
                return
        raise SystemExit(f"no subroutine named {args.name!r}")

    n = len(subs)
    n_desc = sum(1 for s in subs if classify(s)[0])
    n_entry = sum(1 for s in subs if classify(s)[1])
    n_exit = sum(1 for s in subs if classify(s)[2])
    n_done = sum(1 for s in subs if is_done(s))

    print(f"ROM subroutine banners: {n}")
    print(f"  with description:     {n_desc}")
    print(f"  with on_entry:        {n_entry}")
    print(f"  with on_exit:         {n_exit}")
    print(f"  documented (desc+IO): {n_done}  ({100*n_done//max(n,1)}%)")
    print(f"  REMAINING:            {n - n_done}")
    print()

    def sort_key(s: dict):
        return (depths.get(s["addr"], 99), s["addr"])

    rows = subs if args.all else [s for s in subs if not is_done(s)]
    rows.sort(key=sort_key)

    print("depth   addr  D E X  name")
    for s in rows:
        d, e, x = classify(s)
        flags = ("D" if d else "-") + ("E" if e else "-") + ("X" if x else "-")
        depth = depths.get(s["addr"], -1)
        dstr = f"{depth:>5}" if depth >= 0 else "    ?"
        print(f"{dstr}  &{s['addr']:04X}  {flags[0]} {flags[1]} {flags[2]}  {s['name']}")


if __name__ == "__main__":
    main()
