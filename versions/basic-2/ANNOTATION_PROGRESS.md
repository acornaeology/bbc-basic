# BBC BASIC II annotation — semantic quality pass

**STATUS: in progress — 934 of 7,129 placeholders left (13.1 %);
depths 0–4 complete.**

**Stray partial placeholders:** the status tool counts an instruction
as a placeholder only when its *whole* rendered comment is `...`. A few
instructions carry a sub-instruction `'...'` d.comment concatenated with
real text (an artefact of the first pass placing comments at mid-
instruction byte addresses), so they render as e.g. `...  Recover x` and
are NOT counted. As of depth 4 there are ~12 such strays (source `...`
count 946 vs counted 934). Find them by diffing `grep -c ",'\.\.\.'"`
against the tool count; clean by deleting the redundant d.comment line
(as done for fn_point &AB56/&AB5B). Worth a final sweep once the counted
placeholders are gone.

**Note for `stmt_dim` (depth 5):** its descriptor byte 0 leads are
mislabelled the same way index_array's was — &91C4 "Store the dimension
count" actually stores the *data offset* (1 + 2*dims), and &91B7
"Recover the element size" actually recovers that *offset* (the element
size is the following pla at &91BA). Fix when annotating stmt_dim. Inline-comment *density* is 100 %, but that
number is hollow: a first pass met the coverage target by emitting a
literal `...` placeholder wherever it had nothing to say. At the start
of this pass **1,806 of 7,129 code instructions (25.3 %)** carried a
`...` comment — coverage theatre, not annotation.

**Resume here:** run `uv run tools/annotation_status.py` for the live
worklist (leaves-first, worst offenders first). Depth 5 next:
`stmt_dim` (58 — see the byte-0 lead note above), then
`parse_var_ref` (51), `unstack_value_to_var` (42), `iwa_divide` (38),
and the rest of depths 5–8. Per routine:
`uv run tools/annotation_status.py --addrs <name>` for placeholder
addresses + leads, then `uv run fantasm asm extract 2 <name>` to read it.
Verify byte-identical + lint + comments-check before each commit.

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
2. `uv run tools/annotation_status.py --addrs <name>` — the placeholder
   addresses in that routine's **owned range** (up to the next
   subroutine, so trailing un-named blocks are included), each with the
   nearest preceding lead comment. This is the token-efficient way to
   locate work.
3. `uv run fantasm asm extract 2 <name>` (or an address range) — read it
   in context. Pull only the windows you need. (Note: `show_routine.py`
   and the density metric count `...` as "commented" — don't trust them
   for what's left; `annotation_status.py` is the honest measure.)
4. Understand the whole routine, then replace each `...` with intent
   (see *Applying edits* below). Rename `loop_cXXXX` / `cXXXX` /
   `return_N` auto-labels to semantic names as understanding firms up.
   If an existing (non-placeholder) lead is wrong, fix it — verify
   against the branch logic first.
5. `uv run fantasm disassemble 2`, then `verify 2` (byte-identical),
   `lint 2 <driver>`, `comments check 2` — all clean before commit.
6. Commit per batch (a coherent cluster of routines), then re-run the
   status tool and log below.

## Applying edits

Edit the driver `versions/basic-2/disassemble/disasm_basic_2.py` by
rewriting the placeholder comment strings. Each placeholder is a single
line `d.comment(0xADDR, '...', align=Align.INLINE)`. The reliable way is
a Python script that regex-replaces by address, asserting exactly one
match per address (catches typos and addresses that aren't actually
placeholders):

```python
import re
from pathlib import Path
drv = Path("versions/basic-2/disassemble/disasm_basic_2.py")
src = drv.read_text()

# addr -> new comment text (only addresses that currently hold '...')
edits = {
    0xb017: 'Read a kept char from the tail (at X)',
    0xb01a: 'Pack it down to the front (at Y)',
    # ...
}
for addr, new in edits.items():
    pat = re.compile(r"(d\.comment\(0x%x,\s*)'\.\.\.'" % addr)
    if len(pat.findall(src)) != 1:
        raise SystemExit(f"expected 1 placeholder at 0x{addr:x}, found {len(pat.findall(src))}")
    src = pat.sub(lambda m: m.group(1) + repr(new), src, count=1)

drv.write_text(src)
print(f"applied {len(edits)} edits")
```

To **correct an existing (non-placeholder) lead** — e.g. a swapped
high/low label — match its current text instead of `'...'`:

```python
corrections = {
    0x88f5: ('Byte 2 = low | &40', 'Byte 2 = line-number high | &40'),
}
for addr, (old, new) in corrections.items():
    pat = re.compile(r"(d\.comment\(0x%x,\s*)'%s'" % (addr, re.escape(old)))
    if len(pat.findall(src)) != 1:
        raise SystemExit(f"correction miss 0x{addr:x}")
    src = pat.sub(lambda m: m.group(1) + repr(new), src, count=1)
```

`repr(new)` handles quoting, so comment text may contain `"`, `&`, etc.
freely. Run via `uv run python - <<'PY' ... PY`. Don't hand-edit the
generated `.asm`/`.json`; they are rebuilt by `fantasm disassemble`.

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
| 2026-06-14 | depth 1 complete | read_string_literal, stmt_until, stmt_oscli, stmt_close, validate_var_name, stack_real/integer/string, stmt_ptr | 18 | 1319 | — |
| 2026-06-14 | depth 2: number_to_ascii | number_to_ascii (PRINT number formatter: round, format-select, trim, exponent) | 49 | 1270 | — |
| 2026-06-14 | depth 2: parse_number | parse_number (decimal/real parse: digit accumulate, decimal point/exponent, real-vs-integer result) | 30 | 1240 | — |
| 2026-06-14 | depth 2: iwa_store_var | iwa_store_var (store IWA to integer var; trailing real-store path: exponent + sign-packed mantissa) | 22 | 1218 | — |
| 2026-06-14 | depth 2: iwa_mul | iwa_mul (shift-and-add integer multiply: 32-bit running product, multiplier/multiplicand shifts, sign) | 21 | 1197 | — |
| 2026-06-14 | depth 2: fp_split_int_frac | fp_split_int_frac (round-to-nearest integer/fraction split; +1 swapped round up/down branch fix) | 13 | 1184 | — |
| 2026-06-14 | depth 2: fp_eval_cont_frac | fp_eval_cont_frac (continued-fraction eval: count byte, 5-byte coefficient pointer walk, arg/FWA + coeff fold) | 13 | 1171 | — |
| 2026-06-14 | depth 2: stmt_call | stmt_call (CALL: build &0600 parameter block, addr-low/high/type per param) | 9 | 1162 | — |
| 2026-06-14 | depth 2 complete | fwa_to_int (mantissa->IWA copy), fn_strings (No such FN/PROC error tail), stack_local (LOCAL save) | 10 | 1152 | — |
| 2026-06-14 | depth 3: print_line_number | print_line_number (decimal via repeated subtraction of powers of ten, zero-suppress, field pad) | 17 | 1135 | — |
| 2026-06-14 | depth 3: sin_cos_reduce | sin_cos_reduce (SIN/COS range reduction: quadrant via /(pi/2), Cody-Waite two-part subtract) | 10 | 1125 | — |
| 2026-06-14 | depth 3: ascii_to_number | ascii_to_number (VAL/tokenise: NUL-terminate SWA, save/repoint PtrB at &0600) | 10 | 1115 | — |
| 2026-06-14 | depth 3: print_token | print_token (de-tokenise: scan keyword table at &8071, match token byte, advance entry) | 10 | 1105 | — |
| 2026-06-14 | depth 3: fwa_complement_half_pi | fwa_complement_half_pi (pi/2 - FWA two-part; ATN core: FWB build, arctan continued fraction) | 9 | 1096 | — |
| 2026-06-14 | depth 3: read_input_line | read_input_line (prompt + OSWORD 0 read line: build the param block at &37) | 9 | 1087 | — |
| 2026-06-14 | depth 3 complete | print_special_item (PRINT ' TAB SPC + inline string), stmt_if (IF condition test/THEN/ELSE), fwa_int_power (FWA^n) | 14 | 1073 | — |
| 2026-06-14 | depth 4: index_array | index_array (array element address: row-major Horner over extents, x4/x5 element scale; +1 byte-0 = data-offset lead fix) | 62 | 1011 | — |
| 2026-06-14 | depth 4: eval_power | eval_power (^ operator: int/frac/large-exponent paths; owned hex-output nibble expansion and real-print sign) | 23 | 988 | — |
| 2026-06-14 | depth 4: eval_relational | eval_relational (< <= = >= > <> -> TRUE/FALSE; owned string-concat tail: new length, prepend) | 16 | 972 | — |
| 2026-06-14 | depth 4: eval_factor | eval_factor (level-1 factor: token classify; hex-number parse - clear IWA, nibble shift, bit roll) | 14 | 958 | — |
| 2026-06-14 | depth 4 complete | fn_point (POINT->OSWORD 9), eval_or_eor, trace_line ([line] TRACE), eval_and, eval_mul_div, eval_expr_to_integer; +2 stray concat-placeholder lines removed | 24 | 934 | — |
