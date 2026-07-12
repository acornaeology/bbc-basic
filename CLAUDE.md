# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

Annotated disassembly of Acorn BBC BASIC, the BASIC interpreter ROM for the BBC Micro. Python scripts drive [dasmos](https://github.com/acornaeology/dasmos) (a programmable 6502 disassembler) to produce readable, verified assembly output from the original ROM binary. The version covered is BASIC II — the 16 kB language ROM at `&8000`.

Unlike the filing-system ROMs in the sibling projects (NFS, ADFS), BBC BASIC is a *language* ROM: a line editor, keyword tokeniser/de-tokeniser, statement interpreter, expression evaluator, variable storage, and floating-point arithmetic. There is no filing-system or FDC code, and the hardware footprint is small.

## Build commands

Requires [uv](https://docs.astral.sh/uv/) and [beebasm](https://github.com/stardot/beebasm) (v1.10+).

```sh
uv sync                                                                       # Install dependencies (fantasm, dasmos)
uv run pre-commit install                                                     # One-time: activate the pre-commit hook (regenerates README.md)
uv run fantasm disassemble 2                                                  # Run the dasmos driver via fantasm (sets FANTASM_ROM / FANTASM_OUTPUT_DIR)
uv run fantasm lint 2 versions/basic-2/disassemble/disasm_basic_2.py          # Validate annotation addresses
uv run fantasm verify 2                                                       # Reassemble and byte-compare against original ROM
```

Verification is the primary correctness check: the generated assembly must reassemble to a byte-identical copy of the original ROM. Lint validates that all annotation addresses (comments, subroutines, labels) reference valid item addresses in the dasmos output. CI (`.github/workflows/verify.yml`) runs disassemble, lint, then verify on every push.

After editing the driver, keep it address-sorted — `uv run fantasm driver sort` reorders the annotation calls; `fantasm driver sort --check` (clean tree expected) and `fantasm labels classify 2` (expect 0 unclassified auto-labels) are the housekeeping gates the progress docs treat as part of "done".

`README.md` is **generated** — do not edit it directly. It is rendered from `README.md.j2` + `acornaeology.json` (+ `rom.json`) by `generate_readme.py`, wired up as a pre-commit hook (`.pre-commit-config.yaml`). Edit the template or the JSON, then run `uv run generate_readme.py` (or let pre-commit do it).

## Architecture

### Tooling: fantasm + dasmos

The orchestration layer is provided by [fantasm](https://github.com/acornaeology/fantasm) — installed as a regular project dependency. fantasm exposes a `fantasm` CLI (subcommands: `verify`, `lint`, `compare`, `audit`, `cfg`, `comments`, `coverage`, `context`, `data`, `driver`, `hooks`, `labels`, `bytes`, `asm`, `sub`, `addresses`, `annotations`, `backfill`, `promote`, `fingerprint`, `shared`, `info`, `project`, `disassemble`) and a `fantasm.api` package for programmatic use. Project layout, prefixes, and per-version metadata live in `fantasm.toml`. fantasm is library-agnostic: it runs the per-version driver as a subprocess and consumes the JSON / `.asm` artefacts the driver emits.

**Full fantasm reference: <https://acornaeology.github.io/fantasm/>** — the user guide covers every subcommand, the `fantasm.toml` schema, the version-graph workflows, and the importable `fantasm.api`. Reach for it before guessing.

[dasmos](https://github.com/acornaeology/dasmos) (a programmable 6502 disassembler with a stable 1.0 API, byte-faithful round-trip oracle, and Stevedore-managed CPU / renderer / environment plug-ins) is invoked directly via the per-version driver script under `versions/basic-2/disassemble/`. The driver builds a `dasmos.Disassembler` with `Disassembler.create(cpu="6502", ...)`, calls `d.load()`, registers labels/comments/subroutines/hooks, then renders both `beebasm` and `json` outputs from a single `ir = d.disassemble()` step. Reference: <https://acornaeology.github.io/dasmos/driver_api.html>. Local source of truth: `/Users/rjs/Code/acornaeology/dasmos/` (sibling checkout — read `src/dasmos/` directly when investigating behaviour).

### Disassembly driver

`versions/basic-2/disassemble/disasm_basic_2.py` — the main annotation file. Configures dasmos with entry points, labels, constants, subroutine descriptions, comments, and hooks using the dasmos driver API (`d.entry()`, `d.label()`, `d.constant()`, `d.comment()`, `d.subroutine()`, `d.hook_subroutine()`, `d.byte()`, `d.stringz()`, `d.format_hint()`). This is where most development work happens.

`d.subroutine()` takes structured `description`, `on_entry`, and `on_exit` kwargs — the on_entry/on_exit dicts document a routine's register and zero-page calling contract and render as the subroutine banner. A `d.label()` for a sub-&8000 location that also carries `description=`, `length=`, `group=`, and `access=` kwargs is emitted into the JSON's `memory_map` array (grouped per `rom.json`'s `memory_map_groups`) and becomes a row on the rendered memory-map page, with `[name](address:XXXX)` links resolving to it.

### Indexing bases (`d.index_base` / `d.index_region`)

**Version floor: dasmos ≥ 4.0.0, fantasm ≥ 0.18.0.** The disassembly JSON is `schema_version: 4`. dasmos 2.0 introduced classifying every cross-reference to an address as either a **direct** access (`lda addr` / `sta addr`) or an **indexing base** (`lda addr,X` / `sta addr,Y`, where the byte touched is `addr+reg` and the base byte itself is never read or written), with `references[]` entries as `{addr, kind, move_id?}` objects (not bare ints). dasmos 3.0 reshaped `expressions[]` to `{text, tree}` objects and added a top-level `macros` section (see the `pack_mnemonic_*` macros and the assembler-neutral `d.expr(...)` DSL in the driver). dasmos 4.0 (schema v4) made memory **access orthogonal**: each `memory_map` entry carries `access` as an ordered flag array over `["r","w","b"]` — read / write / indexing-base — **derived from the references**, and the former top-level `index_bases` array is folded into `memory_map`. A pure base is a bare `["b"]` entry; an address both touched and based (e.g. `hw_stack`, block-copied via `,X` during PROC/FN save) comes out `["r","w","b"]`. Older fantasm misreads these schemas — do not drop the floor. (Local tooling in `tools/` and `generate_readme.py` only reads `items`/`subroutines`/the project manifest, not the disassembly `references`, so it is unaffected.)

`d.index_base(addr, name, group=, description=, length=)` is the intention-revealing label for an address used as an indexing base; it tags the `b` access flag while the name still resolves the `,X`/`,Y` operand. Under schema v4 an index base is an ordinary `memory_map` entry carrying `b` — alone (`["b"]`) for a pure base, or alongside `r`/`w` when the same address is also touched directly, since access is a set. There is **no** longer a separate `index_bases` section and **no** `access=` either/or: a region and a base coexist at one address, and dasmos derives the flags from the references. **Always pass `group=`** so the base sits within the surrounding ZP/page layout on the memory-map page — dasmos 4.0.0 warns for every ungrouped `memory_map` entry (dasmos#43), and this ROM still has 33 (the FOR/REPEAT/GOSUB frame-field bases, `var_table_base`, `strbuf_base`, …) awaiting a grouping pass. An in-image ROM data table (≥&8000) tagged as a base stays a label on its data item and does not appear in `memory_map` (a sub-&8000 view).

**Workflow.** `fantasm labels list <VER> --index-base-only` lists labels used exclusively as indexing bases (with `Direct`/`Idx`/`Code` columns). Treat it as a lead, not an oracle, and **read each label and its `.asm` usage before converting** — the tool finds candidates; only the code says what a label is. Two blind spots to compensate for by hand:
- It can **under-report low-page (page 0–2) bases** (fantasm excludes them conservatively when the reference kind isn't surfaced for that page). The dasmos `.asm` xref comment (`used as index base N times`) IS authoritative there — grep the `.asm` for it and cross-check against your driver labels.
- The `Code` flag **misses relocated-code entries** (a block copied to RAM via `add_move` and executed there). This ROM has no moves, but the rule stands: also exclude any `d.entry()` target — converting a live entry point off the map is the cardinal error. Assert no `d.entry()` address is a `d.index_base` after converting.

**Classify by reading**, per label: **CONVERT** genuine data index-bases — ROM lookup/dispatch/message tables and RAM scratch/field-base offsets (e.g. the FOR/REPEAT/GOSUB stack frame-field bases in `disasm_basic_2.py`, and `−1` base-adjustment tricks like `var_table_base`/`strbuf_base`). **LEAVE** anything that labels executable code (any `type=='code'` item or `d.entry()` target), `d.subroutine()`-style data banners, auto-labels (`l####`), and environment-provided labels. Under v4 a fundamental fixed region that is incidentally indexed needs no choice: **keep it a memory-map region** (its `r`/`w` banner) and dasmos adds the `b` flag automatically from the references (here `hw_stack`, the 6502 hardware stack block-copied via `,X` during PROC/FN save, comes out `["r","w","b"]`; the `fp_temp*` scratch keeps its region banner). `verify` passing does **not** prove a classification is right — the access model is annotation-only; correctness comes from the reading.

**`d.index_region(anchor, name, window=(lo,hi))`** renders in-window neighbours as `anchor±k,X`. Use it **only** to eliminate many interchangeable notional slots around one real anchor. Do **not** force it onto `*_lo`/`*_hi` pairs, distinct adjacent tables, N-byte-spaced parallel arrays, or single base-adjustment tricks — those keep their distinct names as separate `index_base`s. This ROM has no case that pays off; all clusters here are anti-patterns.

### Lint

`fantasm lint <VER> <DRIVER_PATH>` validates that every `comment()`, `subroutine()`, and `label()` address in a driver script corresponds to a valid address in the dasmos JSON output (or the workspace / external regions declared in `fantasm.toml`).

### Verification

`fantasm verify <VER>` assembles the generated `.asm` with beebasm and does a byte-for-byte comparison against the original ROM.

### Version layout

The ROM version lives under `versions/basic-2/`. Subdirectories:
- `rom/` — original ROM binary and metadata (`rom.json` with hashes)
- `disassemble/` — dasmos driver script
- `output/` — generated assembly (`.asm` beebasm, `.s` 64tass) and structured data (`.json`)

The version ID in `acornaeology.json` and CLI arguments is the bare number `2`. The directory layout is governed by `[versions] prefixes` in `fantasm.toml`; fantasm's `resolve_version_files()` maps a version ID to the matching `versions/basic-{version_id}/` directory and the driver `disasm_basic_{version_id}.py`.

### Helper tools (`tools/`)

Project-local scripts that support the annotation grind; the driver is always the single source of truth, so they only read the generated JSON and report. Run with `uv run tools/<script>.py`.

- `annotation_status.py` — per-subroutine inline-comment quality; flags placeholder (`...`) comments and reports what remains. `--all`, `--table`.
- `banner_status.py` — per-subroutine *banner* quality (description + on_entry/on_exit contract).
- `show_routine.py <name|addr> [end]` — dump one routine's instructions with comment/JGH cross-reference for the grind.
- `gaps.py <lo> <hi>` — uncommented instructions in an address range, with JGH cross-ref.
- `correlate_jgh.py` — correlate [J.G. Harston's](https://mdfs.net/Software/BBCBasic/BBC/) byte-identical BASIC II source against our disassembly via address anchors; harvests his inline comments into `tools/jgh_correlation.tsv`. JGH is the primary external label/commentary source.

### Documentation and progress tracking

- `DISASSEMBLY.md` — how to produce and maintain the disassembly (prerequisites, CLI reference, workflow).
- `versions/basic-2/*_PROGRESS.md` — narrative trackers for the annotation passes (inline comments, subroutine banners, label naming, memory map). All currently marked **COMPLETE**; read the top of the relevant one before re-touching that surface — they record the conventions used and the subtle mislabels already corrected (e.g. array descriptor byte 0 is a data offset, not a dimension count).
- `docs/` — bundled reference PDFs/Markdown (BBC User Guide, Advanced BASIC ROM User Guide) and `docs/analysis/basic-2/` deep-dive notes (control-flow stacks, floating-point precision).

### Glossary

`GLOSSARY.md` — project-level glossary of BBC BASIC and Acorn terms, registered in `acornaeology.json` as `"glossary": "GLOSSARY.md"`. Uses Markdown definition-list syntax with a brief/extended split:

```markdown
**TERM** (Expansion)
: Brief definition — one or two sentences. What the term IS.

  Extended detail — how BASIC uses it, implementation specifics,
  or additional context. Shown only on the glossary page.
```

First paragraph = brief (tooltip text). Subsequent indented paragraphs after a blank line = extended (glossary page only).

## Key technical context

- BBC BASIC II ROM base address: 0x8000, size: 16384 bytes (16 kB sideways ROM)
- NMOS 6502 processor (BASIC II predates the 65C02)
- Sideways-ROM header at &8000: language entry (&8000), service entry (&8003), ROM type byte (&8006), copyright-offset pointer (&8007), binary version (&8008), title "BASIC" (&8009), then the "(C)1982 Acorn" copyright string
- Keyword/tokeniser table begins around &8071: each entry is keyword text + token byte + flag byte
- Heavy zero-page usage for the interpreter, expression stack, variable pointers, and the 40-bit floating-point accumulators — declare ZP locations with `d.label()` generously
- Environments: `acorn_mos`, `acorn_model_b_hardware`, `acorn_sideways_rom`. Do NOT pull in filing-system / FDC environments
- Assembly output targets beebasm syntax (`ir.render("beebasm", ...)`); structured output is `ir.render("json")`
- Assembly comments are formatted to fit within 62 characters
- Use Acorn notation (`&XXXX`) in prose and comments; Python notation (`0xXXXX`) in driver code
