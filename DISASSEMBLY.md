# Disassembly Guide

How to produce and maintain an annotated, verified disassembly of the Acorn BBC BASIC ROM.

For project overview and build instructions, see [README.md](README.md). For architecture details, see [CLAUDE.md](CLAUDE.md). For BBC BASIC terminology, see [GLOSSARY.md](GLOSSARY.md).


## Prerequisites

- [uv](https://docs.astral.sh/uv/) for Python dependency management
- [beebasm](https://github.com/stardot/beebasm) (v1.10+) for assembly verification
- The ROM binary (16384 bytes for a 16 kB sideways ROM)
- MD5 and SHA-256 hashes of the ROM (`md5 <rom>`, `shasum -a 256 <rom>`)
- Reference materials: the BBC Micro User Guide, Colin Pharo's *Advanced BASIC ROM User Guide*, and existing disassemblies (tobylobster, J.G. Harston)

### One-time setup

After cloning, install dependencies and wire up the git hooks:

```sh
uv sync                    # Install dependencies (fantasm, dasmos)
uv run pre-commit install  # Activate the pre-commit hook (regenerates README.md)
```

`pre-commit install` is per-clone and easily forgotten: without it the `readme-update` hook never fires, so a change to `README.md.j2`, `acornaeology.json`, or `rom.json` can be committed without regenerating `README.md`. The CI `check-readme` job is the non-bypassable backstop that catches such drift.


## Quick reference: CLI tools

The disassembly tooling is provided by [fantasm](https://acornaeology.github.io/fantasm/), invoked as `uv run fantasm <command>`. The full command-by-command reference is at <https://acornaeology.github.io/fantasm/cli.html> and the workflow guide at <https://acornaeology.github.io/fantasm/workflows.html>; the most-used commands here are:

| Command | Description | Example |
|---------|-------------|---------|
| `disassemble` | Run the dasmos driver to generate `.asm` and `.json` from ROM | `fantasm disassemble 2` |
| `verify` | Reassemble and byte-compare against original ROM | `fantasm verify 2` |
| `lint` | Validate annotation addresses against the disassembly | `fantasm lint 2 versions/basic-2/disassemble/disasm_basic_2.py` |
| `asm extract` | Extract assembly section by address range or label | `fantasm asm extract 2 &8000 &8040` |
| `audit summary/detail/undeclared` | Subroutine annotation audit | `fantasm audit summary 2` |
| `cfg leaves/roots/depth/sub/blocks/sub-context` | Inter-procedural call graph queries | `fantasm cfg depth 2` |
| `context uncommented` | Find subroutines with low comment density | `fantasm context uncommented 2` |
| `comments suggest/check` | Comment suggestions and consistency checks | `fantasm comments check 2` |
| `labels classify/apply` | Auto-label classification + rename application | `fantasm labels classify 2` |
| `sub insert` | Find insertion point for a new `subroutine()` | `fantasm sub insert <driver> &8071` |

`fantasm` accepts hex addresses in multiple formats (`&80EA`, `$80EA`, `0x80EA`) as well as label names where appropriate.


## Producing the disassembly

### Step 1: Directory structure

```
versions/basic-2/
  rom/
    basic-2.rom            # The ROM binary
    rom.json               # Metadata: title, size, md5, sha256, links, docs
  disassemble/
    __init__.py            # Empty
    disasm_basic_2.py      # Driver script
  output/                  # Generated .asm and .json go here
```

### Step 2: Bootstrap the driver script

Create a minimal driver following the pattern in `disasm_basic_2.py`:

```python
import os, sys
from pathlib import Path
import dasmos

_rom_filepath = os.environ["FANTASM_ROM"]
_output_dirpath = Path(os.environ["FANTASM_OUTPUT_DIR"])

d = dasmos.Disassembler.create(cpu="6502")
d.load(_rom_filepath, 0x8000)

# Standard environments for an Acorn sideways language ROM
d.use_environment("acorn_mos")
d.use_environment("acorn_model_b_hardware")
d.use_environment("acorn_sideways_rom")

# Seed the trace from the language and service entry points. BASIC's
# language entry is inline code (CMP #1 / BEQ ...), not a JMP, so the
# sideways-ROM environment cannot auto-seed it.
d.entry(0x8000)
d.entry(0x8003)

# ... labels, constants, hooks, subroutines ...

ir = d.disassemble()
(_output_dirpath / "basic-2.asm").write_text(str(ir.render("beebasm")), encoding="utf-8")
(_output_dirpath / "basic-2.json").write_text(str(ir.render("json")), encoding="utf-8")
```

### Step 3: Verify the round-trip immediately

Before any annotation, prove the round-trip:

```sh
uv run fantasm disassemble 2
uv run fantasm verify 2
uv run fantasm lint 2 versions/basic-2/disassemble/disasm_basic_2.py
```

Verification must report byte-identical with zero annotation, and must stay byte-identical after every subsequent change. dasmos is a byte-faithful round-trip oracle: anything it cannot prove is code is emitted as data, which still reassembles identically.


## The BBC BASIC ROM structure

### Sideways-ROM header (&8000-&8018)

Decode this precisely as the first hand-annotated region:

| Address | Contents |
|---------|----------|
| &8000 | Language entry point (`CMP #1 : BEQ ...` — entered by the MOS) |
| &8003 | Service entry point |
| &8006 | ROM type byte |
| &8007 | Copyright-offset pointer (offset to the `(C)` string) |
| &8008 | Binary version byte |
| &8009 | Title string "BASIC" (NUL-terminated) |
| &800F+ | "(C)1982 Acorn" copyright string |

The `acorn_sideways_rom` environment recognises this layout and synthesises per-field annotations from the ROM bytes.

### Keyword / tokeniser table (from ~&8071)

The single most distinctive data structure in the ROM. Each entry is keyword text followed by a token byte and a flag byte (e.g. `AND` &80, `ABS` &94, `ACS` &95). The interpreter scans this table to tokenise keywords on entry and to de-tokenise them when listing. Give the table a `subroutine()`-style data banner and lay it out with explicit `EQUS`/`EQUB` (or a hook) so it round-trips. Per-entry detail goes in inline `comment()` calls.

### Interpreter and arithmetic

The bulk of the ROM:
- the statement dispatch / interpreter loop
- the expression evaluator (with operator precedence)
- variable storage and lookup
- line tokenise / de-tokenise and the line editor
- the 40-bit floating-point pack/unpack and arithmetic routines

These make heavy use of zero page. Declare ZP locations with `d.label()` generously — the floating-point accumulators (FPA/FPB), the program/text pointers, `LOMEM`/`HIMEM`/`TOP`/`PAGE`, and the expression stack pointers are the highest-value labels.

### Inline-data idioms

Where a `JSR` is followed by inline data (an embedded string or an error block: error-number byte + message + `&00`), hook the called routine with `d.hook_subroutine()` so the post-call bytes are classified as data rather than mis-disassembled as code.


## Annotation workflow

### Recommended approach: bottom-up call graph

Annotate routines bottom-up through the call graph, starting with leaf routines (no outgoing calls) and working up to the complex handlers that call them.

1. Import reference labels first (header, ZP map, keyword table, FP routines) — biggest understanding-per-effort.
2. Decode the header and the keyword table as the first hand-annotated regions.
3. Get the call-graph depth ordering: `uv run fantasm cfg depth 2`.
4. Work through each routine: use `audit detail` to see code, callers, callees, and flags; read the relevant User Guide / Pharo section; add inline `comment()` for each instruction and a `subroutine()` with title, description, and calling convention.
5. Run `disassemble`, `verify`, `lint` after each batch.

### Importing labels from reference disassemblies

Use the same pattern the sibling projects used for external symbols: build the byte-identical ROM from a reference source, extract its symbol names, generate `d.label()` calls, then verify the round-trip still holds. Keep such importers as small throwaway scripts under `tools/`.

Check each reference's licence before copying prose. Importing label *names* and re-deriving the comments yourself is the safe pattern.


## Annotation guidelines

### Comment style

All per-instruction comments use `inline=True` (or `align=Align.INLINE`), placing the comment at the end of the instruction line. Comments are formatted to fit within 62 characters.

### Hex notation

- Use **Acorn notation** (`&XXXX`) in documentation, Markdown files, and human-readable comments
- Use **Python notation** (`0xXXXX`) in Python scripts (driver scripts, tools)

### Naming conventions

- Labels and subroutine names: descriptive `snake_case` (e.g. `tokenise_line`, `expr_eval`, `fp_add`, `var_lookup`)
- Keep cross-project / cross-version comparisons out of the driver — they belong in progress / notes markdown, not in `disasm_basic_2.py`

### Variable / function naming in driver and tools

Use the suffixes `_filepath`, `_dirpath`, `_dirname`, `_filename` (never the ambiguous `_dir` / `_file`).


## Reference materials

### The BBC Micro User Guide

Documents the BBC BASIC language from the user's side: every statement and function, operator precedence, the assembler. Useful for understanding what each handler implements.

### Colin Pharo — Advanced BASIC ROM User Guide

The best reference to the ROM internals: zero-page maps, the keyword table format, the interpreter loop, variable storage, and the floating-point routines. Read the relevant section before annotating each subsystem.

### J.G. Harston's source reconstruction

A multi-target reconstruction (`Basic2/Basic2.src`) that reassembles with the BBC BASIC assembler to byte-identical ROMs, with informative block comments and zero-page maps. A local copy is under `docs/disasm/MDFS/`. This is the primary external source of BBC BASIC II label names.

### tobylobster's BBC BASIC tokeniser

The [`basic_tokens`](https://github.com/TobyLobster/basic_tokens) Python tokeniser/detokeniser is a clean cross-reference for the keyword/token table and the tokenising rules (a local checkout is at `/Users/rjs/Code/basic_tokens`).

### Toby Nelson's OS 1.20 reassembly

A fully-annotated reassembly of the BBC Micro MOS (ACME syntax), local at `/Users/rjs/Code/os120`. Invaluable for the OS zero-page / workspace names and the exact semantics of the OSBYTE / OSWORD / vector calls BASIC makes.

### hoglet's BBC BASIC 4r32 disassembly

A byte-identical disassembly of [BBC BASIC 4r32](https://github.com/hoglet67/BBCBasic4r32) — a later, reorganised cousin of BASIC II. Addresses differ, but the structure and label names are useful for cross-referencing when BASIC II code is unclear.


## Lint checks

The lint tool validates:

1. Every `comment()`, `subroutine()`, and `label()` address corresponds to a valid address in the dasmos JSON output
2. No duplicate `subroutine()` or `label()` declarations at the same address
3. No double-comment lines (`"; ;"`) in the assembly output (indicates a subroutine description placed at a data address)
