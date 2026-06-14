# BBC BASIC II annotation — label-naming pass

**STATUS: COMPLETE — all 864 dasmos auto-generated code labels named,
plus the ~50 auto-generated zero-page/RAM workspace labels. Every label
in the disassembly now has a semantically meaningful, globally unique
name. Verification byte-identical; `labels classify 2` reports 0;
`driver sort --check` clean.**

This is the follow-on to the inline-comment pass and the banner pass
(both COMPLETE — see ANNOTATION_PROGRESS.md / BANNER_PROGRESS.md). All
routines now carry rich descriptions and contracts, so the semantics of
each label are already documented; this pass just names the labels.

## The goal & policy

Every label must have a meaningful name. dasmos auto-generates names like
`c8b41`, `loop_ca8b5`, `sub_c8c21`, `l82df` for branch/loop/call/data
targets that have no declared label. Replace them all.

- **Subroutine-category labels** (JSR targets) get **globally meaningful**
  names — a reader should understand them anywhere (e.g. `asm_enter`,
  `skip_to_statement_end`).
- **Local labels** (branch targets, loop heads, shared rts tails within a
  routine) may be **terser/abbreviated** but must stay **globally unique**.
  Convention: prefix with the routine name (or a clear abbreviation of
  it) + purpose, e.g. `eval_power_int_loop`, `iwa_add_done`,
  `parse_var_ref_array`. The prefix guarantees global uniqueness.
- Loop heads → `…_loop` (or `…_loop2` etc.). Shared rts → `…_done` /
  `…_rts`. Error/exit branches → `…_error` / `…_fail` / a named outcome.
- Names are 6502-assembler identifiers: `[a-z0-9_]`, start with a letter.

Global uniqueness is enforced by `verify` (beebasm errors on a duplicate
label), so a clash is caught immediately.

## Categories (from `fantasm labels classify 2`)

| Category | Count | Notes |
|----------|-------|-------|
| internal_conditional | 480 | branch targets (`cXXXX`) |
| internal_loop | 185 | loop heads (`loop_cXXXX`) |
| subroutine | 126 | JSR targets (`sub_cXXXX` / `cXXXX`) |
| shared_tail | 66 | shared rts / fall-through tails |
| data | 7 | data-table labels (`lXXXX`) |

## Workflow per batch (a few routines at a time, address-ascending)

1. For each routine, `uv run fantasm asm extract 2 <routine>` — read the
   **whole body and its control flow**, not just the one inline comment
   at a label's address. A label's *role* (why control arrives there,
   what the block represents, where it exits) often needs the branch
   condition that targets it and the surrounding structure — the
   `; &XXXX referenced N times by &YYYY` lines in the .asm and
   `fantasm labels refs 2 <label>` show the inbound sites. Shared tails,
   error exits, and mode-dispatch targets especially need this.
2. Decide names. Append `d.label(0xXXXX, 'name')` lines for the batch
   just before the `ir = d.disassemble()` render block (any order — they
   get sorted next).
3. `uv run fantasm driver sort versions/basic-2/disassemble/disasm_basic_2.py -i`
   — distributes each d.label to its address position next to its routine.
4. If a renamed label's old auto-name appears in a `d.comment(...)` /
   `description=` prose string, update that text by hand (there are only
   ~18 such references in the whole driver).
5. `uv run fantasm disassemble 2`, then `verify 2` (must say
   "Verification PASSED: 16384 bytes match"), `lint 2 <driver>`, and
   `comments check 2` — all clean before committing.
6. Commit per coherent batch; update the batch log + status + resume
   pointer here.

## Tooling notes

- `fantasm labels classify 2` — the worklist (label, addr, category,
  refs, parent routine). `--category X` to filter.
- `fantasm labels list 2 --match <re>` — inventory / find labels.
- `fantasm labels refs 2 <label>` — inbound references for one label.
- `fantasm labels apply` exists (renames TOML) but its inline mode needs
  pre-existing declarations and its `--section` mode clusters renames in
  a block that `driver sort` would then scatter — so we use the simpler
  "append `d.label` + `driver sort`" recipe above, which yields the
  canonical inline `d.label` style next to each routine.
- Driver stays address-sorted; `driver sort --check` clean before each
  commit.

## Batch log

| Date | Routines (addr range) | Labels named | Remaining | Commit |
|------|-----------------------|--------------|-----------|--------|
| 2026-06-14 | setup + assembler_exit + language_startup | 19 | 845 | 5f2a08b |
| 2026-06-14 | keyword/action + asm decode tables | 7 | 838 | 3a522de |
| 2026-06-14 | asm_parse_mnemonic (full assembler) | 51 | 787 | 6ea288a |
| 2026-06-14 | parse_decimal_u16 + name-char helpers | 8 | 779 | ce7b6f7 |
| 2026-06-14 | tokenise_line | 35 | 744 | 75b0d75 |
| 2026-06-14 | line exec + LET | 16 | 728 | 935168b |
| 2026-06-14 | string assign + LOCAL + PRINT# | 27 | 701 | 928d13d |
| 2026-06-14 | stmt_print + special items | 22 | 679 | 5e0b606 |
| 2026-06-14 | CLS/CALL/DELETE/RENUMBER/AUTO/DIM | 40 | 639 | ecb899b |
| 2026-06-14 | imul/TRACE/PROC/LOCAL/MODE/PLOT/VDU | 25 | 614 | a6b1165 |
| 2026-06-14 | find/create var + lvalue | 29 | 585 | 1365841 |
| 2026-06-14 | parse_var_ref + index_array | 31 | 554 | 23e4916 |
| 2026-06-14 | line-number/stmt-end/IF | 27 | 527 | a937781 |
| 2026-06-14 | decimal print/find/divide/compare | 32 | 495 | 8768244 |
| 2026-06-14 | bitwise/relational/add-sub eval | 23 | 472 | ac2e15d |
| 2026-06-14 | integer +/-/*/DIV operators | 29 | 443 | 0ff433b |
| 2026-06-14 | eval_power + hex convert | 14 | 429 | 8e99038 |
| 2026-06-14 | number_to_ascii | 32 | 397 | 425c2cb |
| 2026-06-14 | parse_number/exponent/output | 21 | 376 | 95cb707 |
| 2026-06-14 | FP normalise/int-float/split | 22 | 354 | 6b8cd0e |
| 2026-06-14 | FP add/multiply/round | 27 | 327 | 3504126 |
| 2026-06-14 | fp_divide | 12 | 315 | 65eaece |
| 2026-06-14 | SQR/LN/ASN/ATN/SIN/EXP | 32 | 283 | 676f917 |
| 2026-06-14 | SGN/VAL/INT/INSTR + misc fns | 28 | 255 | c955272 |
| 2026-06-14 | eval_factor/negate/string-literal | 29 | 226 | b66c509 |
| 2026-06-14 | string functions + RND loops | 23 | 203 | 21413f2 |
| 2026-06-14 | find_def + call_proc_fn | 24 | 179 | f3ff960 |
| 2026-06-14 | LOCAL/load/SOUND/WIDTH/print | 30 | 149 | 4dc23a7 |
| 2026-06-14 | LIST/NEXT/FOR | 35 | 114 | 9a9afe3 |
| 2026-06-14 | GOTO/ON/find_line/INPUT# | 29 | 85 | dcf2907 |
| 2026-06-14 | INPUT/READ/DATA/edit/file (final code) | 85 | 0 | (4dc23a7..) |
| 2026-06-14 | workspace/zero-page/frame-field labels | 50 | 0 | 3aeb5f2 |

## Resume here

**COMPLETE — nothing remains.** All auto-generated labels (cXXXX,
loop_cXXXX, sub_cXXXX, lXXXX) have been replaced with meaningful,
globally unique names, working address-ascending routine by routine.
`uv run fantasm labels classify 2` reports 0; the driver is
address-sorted and reassembles byte-identical.

Naming conventions used: subroutine-category labels got standalone
descriptive names; local branch/loop/tail labels were prefixed by their
routine (tok_*, asm_*, pvr_*, nta_*, callpf_*, etc.) for global
uniqueness; shared error/return points got domain names (syntax_error,
no_for_error, mistake_error, …); zero-page extensions followed the
existing zp_* scheme.
