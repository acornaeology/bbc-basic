# BBC BASIC II annotation — semantic quality pass

**STATUS: in progress.** Inline-comment *density* is 100 %, but that
number is hollow: a first pass met the coverage target by emitting a
literal `...` placeholder wherever it had nothing to say. At the start
of this pass **1,806 of 7,129 code instructions (25.3 %)** carried a
`...` comment — coverage theatre, not annotation.

This pass replaces every placeholder with an intention-revealing comment
in the language of the domain (BASIC interpretation: tokeniser, line
editor, statement dispatch, expression evaluator, variable storage,
40-bit floating point), to the standard of the sibling NFS / ADFS /
Econet disassemblies.

## The quality bar

A comment must say *why*, in domain terms — never restate the opcode.

Bad (the first pass):
```
    lda string_work,x     ; ...
    sta string_work,y     ; ...
    inx                   ; ...
    dec zp_iwa            ; ...
    bne loop_cb017        ; loop
```

Good (this pass — RIGHT$ shifting the tail to the front):
```
    lda string_work,x     ; Read a kept char from the tail (offset X)
    sta string_work,y     ; Pack it down to the front of the buffer
    inx                   ; Advance the read cursor
    dec zp_iwa            ; One fewer char to move
    bne loop_cb017        ; Until all `count` chars are shifted down
```

Rules of thumb:
- Name the **domain value**, not the register (`new string length`, not
  `A`). State register identity only when it is the point (`A = &82:
  TX in reset`).
- A branch comment says what the *taken* branch means
  (`count == length: keep it`), not "branch if equal".
- Lean on the routine's purpose: a line is allowed to be terse when an
  adjacent line already gives the context.
- 62-character limit on the rendered comment (py8dis formatting).
- Acorn notation (`&XXXX`) in comments; Python (`0xXXXX`) in the driver.

### Continuation lines (multi-instruction operations)

Two sanctioned idioms — never leave a continuation as `...`:

- **Repeated identical instructions doing one thing** (e.g. three `iny`
  to skip a 4-byte header): the first line carries the description, the
  rest are `(continued)`. `fantasm comments check` enforces this
  (`chain_comment` finding); ~13 already exist.
- **A chain over distinct named bytes** (e.g. `rol m4 / rol m3 / rol m2`
  shifting the 40-bit mantissa, or `adc m4 / adc m3 …` summing it): the
  lead states the operation and the result; each continuation **names
  its byte** so the line reads as a sentence across the chain —
  `carrying up through m4, / m3, / m2, / m1 (mantissa now x2)`. Mirrors
  the existing `fwa_sign` style (`(mantissa byte 2)`).
  **Decided 2026-06-14: use the sentence style for these chains** (not a
  bare byte name and not `(continued)`) — the richest reading.

## Reference works (consult before guessing)

- **J.G. Harston's source reconstruction** — harvested into
  `tools/jgh_correlation.tsv` (addr → his inline comment) and
  `tools/jgh_banners.tsv`. The primary external anchor; sparse in
  places, authoritative where present.
- **The Advanced BASIC ROM User Guide (Colin Pharo)** — zero-page map,
  keyword table, interpreter loop, variable storage, FP routines. Linked
  in `acornaeology.json`.
- **hoglet's BBC BASIC 4r32 disassembly** — a later, reorganised cousin;
  useful for cross-checking structure and names.
- Existing **substantive** comments already in the driver — match their
  vocabulary (e.g. `zp_iwa` = integer work accumulator, `fwa`/`fwb` =
  floating-point work accumulators A/B, `string_work` = &0600 string
  buffer).

## Workflow per routine

1. `uv run tools/annotation_status.py` — live worklist. A routine is
   **done** when its placeholder count hits 0; the driver is the single
   source of truth, so this is fully resumable. Worst offenders surface
   first within each call-graph depth (leaves first).
2. `uv run fantasm asm extract 2 <name>` — read it in context (callers
   and callees shown).
3. `uv run tools/show_routine.py <name>` — per-line view with JGH
   cross-reference.
4. Understand the whole routine, then replace each `...` with intent.
   Rename `loop_cXXXX` / `cXXXX` / `return_N` auto-labels to semantic
   names as understanding firms up.
5. `uv run fantasm verify 2` (byte-identical), `lint 2 <driver>`,
   `comments check 2` — all clean before commit.
6. Commit per batch (a coherent cluster of routines), then re-run the
   status tool and log below.

## Ordering

Leaves first (call-graph depth 0 upward): a leaf can be understood in
isolation, and doing it first establishes the vocabulary that the
callers above it reuse. Within a depth, the routine with the most
placeholders goes first.

## Batch log

| Date | Batch | Routines | Placeholders fixed | Remaining | Commit |
|------|-------|----------|--------------------|-----------|--------|
| 2026-06-14 | start | — | — | 1806 | — |
| 2026-06-14 | pilot | mant_mul10, fn_rights (RIGHT$), +2 chain fixes | 32 | 1774 | — |
| 2026-06-14 | leaves: number parsing | parse_decimal_u16, decode_line_number, parse_exponent | 29 | 1745 | — |
| 2026-06-14 | leaves: FP load/unpack | fwa_acc_fwb, fwb_unpack_var, fwb_clear/negate, load_real_var, clear_value_bytes | 28 | 1717 | — |
| 2026-06-14 | leaves: string load, subscript, imul16 | load_string_var, check_subscript_bound, imul16 | 18 | 1699 | — |
| 2026-06-14 | depth 0 complete | find_program_line, pointer helpers, find/create_variable, unstack_string, iwa_load_var, rnd_step, +singletons & trailing blocks | 50 | 1649 | — |
| 2026-06-14 | depth 1: encode/FP-to-int | encode_line_number (+2 high/low fixes), fwa_to_int2 | 43 | 1606 | — |
| 2026-06-14 | depth 1: FP add/align | fwa_add_fwb_raw (+1 smaller/larger fix) | 23 | 1583 | — |
| 2026-06-14 | depth 1: find_def | find_def (PROC/FN definition search + cache) | 30 | 1553 | — |
| 2026-06-14 | depth 1: FP divide | fp_divide (restoring long division, 32-bit + 7 guard bits) | 70 | 1483 | — |
| 2026-06-14 | depth 1: assign_string | assign_string (string store: reuse/extend/grow allocation) | 47 | 1436 | — |
| 2026-06-14 | depth 1: FP arithmetic cluster | fwa_mul_var_raw, fp_compare, int_to_fwa, fwa_mul10, fwa_div10, small_int_to_fwa, fwa_round, fwa_negate, iwa_inc | 33 | 1403 | — |
| 2026-06-14 | depth 1: tokenise_line | tokenise_line (keyword match, abbreviations, token emit, state flags) | 19 | 1384 | — |
| 2026-06-14 | depth 1: error/DATA walkers | find_error_line (set ERL, ON ERROR handler dispatch), next_data_item | 30 | 1354 | — |
| 2026-06-14 | depth 1: output helpers | output_top_digit, output_char, output_byte_decimal, print_hex_byte, fn_usr, encode_line_number tail | 17 | 1337 | — |
