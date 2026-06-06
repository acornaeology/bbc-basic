#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# ///
r"""Correlate J.G. Harston's BBC BASIC source with our disassembly.

JGH's `Basic2.src` assembles (with the BBC BASIC assembler) to a
byte-identical BASIC II ROM, and its code labels are address-based
(`.L9857` lives at &9857). That gives us two independent anchors for
lining his commentary up against our disassembly:

  1. every `.Lxxxx` / `.Xxxxx` label is a hard address anchor, and
  2. between anchors, his instruction stream must match ours opcode
     for opcode.

This tool walks his source for the BBC version-2 build (evaluating the
`OPT FNif(...)` conditionals so only the bytes that actually assemble
into our ROM are considered), tracks the current address from the label
anchors, and validates each instruction against our disassembly by
comparing mnemonics. Where they line up it harvests his inline `\`
comment and the `\ ===` banner block that precedes each label.

Output (under tools/):
  jgh_correlation.tsv  — addr <TAB> our_mnemonic <TAB> jgh_comment
  jgh_banners.tsv      — addr <TAB> banner text (label header blocks)

Run:  uv run tools/correlate_jgh.py
It prints alignment statistics; a high match rate means the address
mapping is trustworthy.
"""
import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
JGH_SRC = REPO_ROOT / "docs/disasm/MDFS/Basic2/Basic2.src"
OUR_JSON = REPO_ROOT / "versions/basic-2/output/basic-2.json"
OUT_CORR = REPO_ROOT / "tools/jgh_correlation.tsv"
OUT_BANNERS = REPO_ROOT / "tools/jgh_banners.tsv"

# The build we are matching: BBC BASIC II.
BUILD_VARS = {
    "mos$": "bbc", "target$": "bbc",
    "VALversion$": 2, "INTVALversion$": 2,
    "drop%": 0, "foldup": False, "split%": False,
    "memtop": 0, "membot": 0,
}

LABEL_RE = re.compile(r"^\.([LX][0-9A-Fa-f]{4})\b")
# Mnemonics we treat as code (for opcode matching). Data directives
# (EQU*) and BRK are handled separately.
MNEMONICS = {
    "adc", "and", "asl", "bcc", "bcs", "beq", "bit", "bmi", "bne", "bpl",
    "brk", "bvc", "bvs", "clc", "cld", "cli", "clv", "cmp", "cpx", "cpy",
    "dec", "dex", "dey", "eor", "inc", "inx", "iny", "jmp", "jsr", "lda",
    "ldx", "ldy", "lsr", "nop", "ora", "pha", "php", "pla", "plp", "rol",
    "ror", "rti", "rts", "sbc", "sec", "sed", "sei", "sta", "stx", "sty",
    "tax", "tay", "tsx", "txa", "txs", "tya",
}


def eval_cond(expr: str) -> bool:
    """Evaluate a BBC BASIC OPT FNif() condition for our build."""
    py = expr
    for name, value in BUILD_VARS.items():
        py = py.replace(name, repr(value))
    py = py.replace("<>", "!=").replace("=", "==").replace("!==", "!=")
    py = re.sub(r"\bAND\b", " and ", py)
    py = re.sub(r"\bOR\b", " or ", py)
    py = re.sub(r"\bNOT\b", " not ", py)
    try:
        return bool(eval(py, {"__builtins__": {}}, {}))
    except Exception:
        # Unknown condition: assume included (conservative).
        return True


def split_statements(line: str):
    """Split a source line into (statements, comment).

    Statements are separated by ':' outside string literals. The
    comment is everything from the first unquoted '\\'.
    """
    stmts, cur, comment = [], "", None
    in_str = False
    i = 0
    while i < len(line):
        ch = line[i]
        if ch == '"':
            in_str = not in_str
            cur += ch
        elif not in_str and ch == "\\":
            comment = line[i + 1:].strip()
            break
        elif not in_str and ch == ":":
            stmts.append(cur)
            cur = ""
        else:
            cur += ch
        i += 1
    if cur.strip():
        stmts.append(cur)
    return [s.strip() for s in stmts if s.strip()], comment


def load_our_disassembly():
    """Return (addr -> item) and a sorted list of code addresses."""
    data = json.loads(OUR_JSON.read_text())
    by_addr = {it["addr"]: it for it in data["items"]}
    return by_addr


def main():
    by_addr = load_our_disassembly()

    corr = {}        # addr -> jgh comment (instruction-level)
    banners = {}     # addr -> banner text (label header block)
    pending_banner = []   # accumulating '\ ...' lines before a label

    addr = None      # current assembly address
    matched = mismatched = anchored = 0
    cond_stack = []  # OPT FNif include flags

    for raw in JGH_SRC.read_text(errors="replace").splitlines():
        line = raw.rstrip()
        stripped = line.strip()

        # Banner accumulation: lines that are pure '\' comments and not
        # rule lines (==== / ----) feed the next label's banner.
        if stripped.startswith("\\"):
            text = stripped.lstrip("\\").strip()
            if text and not set(text) <= set("=-"):
                pending_banner.append(text)
            continue

        # Walk tokens, honouring inline OPT FNif/FNelse/FNendif.
        stmts, comment = split_statements(line)
        included = all(cond_stack)
        for stmt in stmts:
            low = stmt.lower()

            if stmt.startswith("OPT FNif"):
                m = re.search(r"FNif\((.*)\)", stmt)
                cond_stack.append(eval_cond(m.group(1)) if m else True)
                included = all(cond_stack)
                continue
            if stmt.startswith("OPT FNelse"):
                if cond_stack:
                    cond_stack[-1] = not cond_stack[-1]
                included = all(cond_stack)
                continue
            if stmt.startswith("OPT FNendif"):
                if cond_stack:
                    cond_stack.pop()
                included = all(cond_stack)
                continue

            lm = LABEL_RE.match(stmt)
            if lm:
                # Label anchor: address is encoded in the name.
                addr = int(lm.group(1)[1:], 16)
                anchored += 1
                if pending_banner:
                    banners[addr] = " ".join(pending_banner)
                pending_banner = []
                continue

            # Any non-label statement ends the banner-accumulation run.
            pending_banner = []
            if not included or addr is None:
                continue

            mnem = low.split()[0] if low.split() else ""
            if mnem in MNEMONICS:
                ours = by_addr.get(addr)
                if ours and ours.get("type") == "code":
                    if ours["mnemonic"] == mnem:
                        matched += 1
                        # Drop JGH's auto "ADDR= bytes" listing
                        # annotations; keep only semantic comments.
                        if comment and not re.match(
                            r"^[0-9A-Fa-f]{4}=", comment
                        ):
                            corr[addr] = comment
                        addr += len(ours["bytes"])
                    else:
                        mismatched += 1
                        addr = None  # lost alignment; wait for a label
                else:
                    mismatched += 1
                    addr = None
            else:
                # Data directive or macro: drop alignment, resync at the
                # next label. (Comments on data lines are recovered via
                # the label banner instead.)
                addr = None

    OUT_CORR.write_text(
        "".join(
            f"{a:04X}\t{by_addr[a]['mnemonic']}\t{corr[a]}\n"
            for a in sorted(corr)
        ),
        encoding="utf-8",
    )
    OUT_BANNERS.write_text(
        "".join(f"{a:04X}\t{banners[a]}\n" for a in sorted(banners)),
        encoding="utf-8",
    )

    total = matched + mismatched
    rate = (100 * matched / total) if total else 0.0
    print(f"label anchors:        {anchored}")
    print(f"instructions matched: {matched}")
    print(f"instructions missed:  {mismatched}  ({rate:.1f}% matched)")
    print(f"inline comments:      {len(corr)} -> {OUT_CORR.name}")
    print(f"label banners:        {len(banners)} -> {OUT_BANNERS.name}")


if __name__ == "__main__":
    main()
