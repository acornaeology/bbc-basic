#!/usr/bin/env python3
"""Report annotation quality per subroutine for the BASIC II disassembly.

The headline density metric is misleading: a comment of "..." counts as
"commented" but conveys nothing. This tool measures the *real* state by
mapping every code item to its containing subroutine and counting how
many carry a placeholder comment (literally "...") versus a substantive
one.

A subroutine is considered DONE when it has zero placeholder comments,
so re-running this tool after each batch shows exactly what remains —
the driver script is the single source of truth, which makes the
re-annotation pass interruptible and resumable.

Usage:
    uv run tools/annotation_status.py            # summary + remaining work
    uv run tools/annotation_status.py --all      # every subroutine
    uv run tools/annotation_status.py --table    # emit the tracker table
"""

from __future__ import annotations

import argparse
import bisect
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JSON_FILEPATH = ROOT / "versions/basic-2/output/basic-2.json"
DEPTH_TSV_FILEPATH = Path("/tmp/cfg_depth.tsv")  # optional; from `fantasm cfg depth`

PLACEHOLDER = "..."


def load_depths() -> dict[int, int]:
    """addr -> call-graph depth (leaves = 0), if the TSV is present."""
    depths: dict[int, int] = {}
    if DEPTH_TSV_FILEPATH.exists():
        for line in DEPTH_TSV_FILEPATH.read_text().splitlines():
            parts = line.split("\t")
            if len(parts) >= 3:
                depth = int(parts[0])
                addr = int(parts[1], 16)
                depths[addr] = depth
    return depths


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true", help="show subroutines with no placeholders too")
    ap.add_argument("--table", action="store_true", help="emit a markdown tracker table")
    args = ap.parse_args()

    data = json.loads(JSON_FILEPATH.read_text())
    subs = sorted(data["subroutines"], key=lambda s: s["addr"])
    sub_addrs = [s["addr"] for s in subs]
    sub_names = {s["addr"]: s["name"] for s in subs}
    depths = load_depths()

    # Per-subroutine tallies.
    total = {a: 0 for a in sub_addrs}
    placeholder = {a: 0 for a in sub_addrs}

    for it in data["items"]:
        if it.get("type") != "code":
            continue
        addr = it["addr"]
        idx = bisect.bisect_right(sub_addrs, addr) - 1
        if idx < 0:
            continue
        owner = sub_addrs[idx]
        total[owner] += 1
        if (it.get("comment_inline") or "").strip() == PLACEHOLDER:
            placeholder[owner] += 1

    rows = []
    for a in sub_addrs:
        rows.append(
            {
                "addr": a,
                "name": sub_names[a],
                "code": total[a],
                "ph": placeholder[a],
                "depth": depths.get(a, -1),
            }
        )

    # Order leaves-first (depth asc; unknown depth last), then most
    # placeholders first within a depth so the worst offenders surface.
    def sort_key(r):
        d = r["depth"] if r["depth"] >= 0 else 999
        return (d, -r["ph"], r["addr"])

    rows.sort(key=sort_key)

    remaining = [r for r in rows if r["ph"] > 0]
    total_ph = sum(r["ph"] for r in rows)
    total_code = sum(r["code"] for r in rows)
    done_subs = sum(1 for r in rows if r["ph"] == 0)

    if args.table:
        print("| Status | Depth | Addr | Name | Instrs | Placeholders |")
        print("|--------|-------|------|------|--------|--------------|")
        for r in rows:
            status = "done" if r["ph"] == 0 else "todo"
            depth = r["depth"] if r["depth"] >= 0 else "?"
            print(
                f"| {status} | {depth} | &{r['addr']:04X} | {r['name']} | "
                f"{r['code']} | {r['ph']} |"
            )
        return

    print(f"Subroutines:         {len(rows)}")
    print(f"  fully substantive: {done_subs}")
    print(f"  with placeholders: {len(remaining)}")
    print(f"Code instructions:   {total_code}")
    print(f"  placeholder '...':  {total_ph}  ({100*total_ph/total_code:.1f}%)")
    print()
    show = rows if args.all else remaining
    print(f"{'depth':>5}  {'addr':>5}  {'instrs':>6}  {'ph':>4}  name")
    for r in show:
        depth = r["depth"] if r["depth"] >= 0 else "?"
        print(f"{str(depth):>5}  &{r['addr']:04X}  {r['code']:>6}  {r['ph']:>4}  {r['name']}")


if __name__ == "__main__":
    main()
