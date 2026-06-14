# BBC BASIC II annotation — subroutine banner pass

**STATUS: COMPLETE — 285 ROM subroutine banners, 284 fully documented
(desc + calling contract), 99 %. The one undocumented banner is
fwa_compare_var (&A5FF), a FALL_THROUGH_ENTRY with no callers — a
mid-instruction continuation, not a callable routine, so a contract
would be meaningless. Inline-comment pass is COMPLETE (see
ANNOTATION_PROGRESS.md); this follow-on banner pass is now COMPLETE.**

Every banner's description was reviewed for accuracy and every callable
ROM routine now carries a structured on_entry/on_exit contract naming
its zero-page and register usage. The driver remains address-sorted
(`fantasm driver sort --check` is clean) and reassembles byte-identical.

Stale banners corrected along the way: iwa_from_ya ("sign-extended" →
zero-extended), fn_to (TO P reads TOP), unstack_integer ("caller drops"
→ falls through and drops), find_program_line (carry sense reversed),
iwa_divide (operand roles; its inline comments still swap dividend/
divisor — an inline-pass follow-up), fp_eval_cont_frac (A/Y not X/Y).

## The goal

The inline pass made every *instruction* carry an intention-revealing
comment. This pass reviews and enriches every *subroutine banner* — the
block comment dasmos renders above a routine from its `d.subroutine(...)`
annotation. A banner sits one level of abstraction above the inline
comments: it says **what the routine does** and, crucially, **how to
call it** — its register and zero-page contract.

Two things to deliver per routine:

1. **Review the title + description for accuracy** now that the inline
   comments document the real behaviour. Fix anything stale or vague;
   enrich thin ones. Keep the description at banner altitude (what +
   how), not a paraphrase of the inline comments.
2. **Document the calling contract** with the structured `on_entry` /
   `on_exit` dicts. This is the headline gap: only 20 of 285 routines
   have one. BBC BASIC threads almost everything through zero page, so
   naming the ZP locations a routine reads and writes is the single most
   useful thing this pass adds.

## The model banner (the bar)

```
; ***************************************************************************************
; Load an integer variable into the accumulator
;
; Copy the 4-byte integer addressed by zp_iwa into IWA.
;
; On Entry:
;     ZP_IWA (&2A/&2B): a pointer to the 4-byte integer variable
;
; On Exit:
;     ZP_IWA: the loaded integer
;     X: preserved
.iwa_load_var
```

Produced by:

```python
d.subroutine(
    0xb336, 'iwa_load_var',
    title='Load an integer variable into the accumulator',
    description='Copy the 4-byte integer addressed by zp_iwa into IWA.',
    on_entry={'zp_iwa (&2A/&2B)': 'a pointer to the 4-byte integer variable'},
    on_exit={'zp_iwa': 'the loaded integer', 'X': 'preserved'},
)
```

### The `d.subroutine()` API (dasmos)

`d.subroutine(addr, name, *, title='', description='', on_entry=None,
on_exit=None, is_entry_point=True, move=None)`

- `title` — one line, the banner's first line. Imperative, concrete
  ("Store the accumulator into an integer variable", not "Integer store").
- `description` — the body. May be multi-line (use a `"""..."""`
  string). State the algorithm/effect at a high level; mention error
  paths it can raise.
- `on_entry` / `on_exit` — **dicts** `{thing: meaning}`. There is no
  separate "clobbers"/"preserves" field: put preservation in `on_exit`
  (`'X': 'preserved'`) and clobbering implicitly (anything not mentioned
  may be corrupted; call it out if a caller would be surprised).

Conventions for the dict keys, matching the existing 20:
- Registers: `'A'`, `'X'`, `'Y'`, `'C'` (carry), `'N'`/`'Z'` (flags).
- Zero page: name **and** address, e.g. `'zp_iwa (&2A)'`,
  `'(zp_general) (&37/&38)'` (parentheses around the label = "the
  address pointed to by"). Use the label names already in the driver
  (`zp_iwa`, `zp_general`, `zp_text_ptr`, `zp_fwa_*`, `zp_fwb_*`, …) so
  lint stays happy and readers can cross-reference.
- Span multi-byte values as `(&2A/&2B)` or `(&2A-&2D)`.

Acorn `&XXXX` notation in the rendered text; Python `0xXXXX` in the
driver source. Keep keys/values tight — these render in the banner.

## Where banners come from (two sources)

Most edits are to literal `d.subroutine(...)` calls, but ~112 of the 285
are **table-generated**, so know which you're editing:

1. **Hand-written `d.subroutine(...)` calls** — ~173, scattered through
   the driver (IWA/FWA arithmetic primitives, the line editor, parsers,
   helpers). Edit these in place. The 20 already-documented routines are
   all here — copy their style.

2. **The `HANDLER_INFO` table** (driver ~line 425) — a dict
   `name -> (title, description)` consumed by the keyword-dispatch loop
   (~line 654) that declares every `stmt_*` / `fn_*` keyword handler via
   `d.subroutine(target, name, title=info[0], description=info[1])`.
   These currently get **title + description only — no contract.** To add
   contracts you must either:
   - **(preferred)** widen the loop + table so an entry may carry
     `on_entry`/`on_exit` (e.g. make the value a dataclass or a 4-tuple
     `(title, desc, on_entry, on_exit)` with the loop passing them
     through), **or**
   - apply a shared default contract in the loop for the two families
     (see below) with per-entry overrides.

   Decide this early and write it in the batch log; it shapes the rest.

### Shared calling conventions to establish first

`stmt_*` and `fn_*` handlers are dispatched, so they share a contract —
establish each ONCE (read the dispatcher and a few handlers; verify with
`fantasm cfg sub-context`/`cfg sub`) and reuse it:

- **`stmt_*` handlers** are entered from the statement dispatcher in
  `execute_line` (&8B0B) after the keyword token is consumed. The
  program pointer is `zp_text_ptr` (&0B/&0C) + offset `zp_text_ptr_off`
  (&0A). They run to the next statement (`jmp statement_loop` etc.) and
  return no value. *Verify the exact register state on entry before
  asserting it.*
- **`fn_*` handlers** are entered from `eval_factor` while evaluating an
  expression; the working text pointer is PtrB (`zp_text_ptr2` &19/&1A,
  offset &1B). They consume their argument(s) and return the result in
  IWA / FWA / the &0600 string buffer with the type in `A` /
  `zp_var_type` (&27). *Verify against the evaluator before asserting.*

Don't guess these — confirm them, because every handler banner inherits
them.

## Tooling (use it, don't hand-grep)

- **Worklist:** `uv run tools/banner_status.py` — counts and the
  remaining-work list, leaves-first (call-graph depth ascending) when
  `/tmp/cfg_depth.tsv` exists. Generate that once:
  `uv run fantasm cfg depth 2 --no-header > /tmp/cfg_depth.tsv`.
  `--all` lists everything; `--name N` dumps one routine's current
  banner fields. A routine is "done" when it has a description AND a
  contract (driver is the single source of truth → resumable).
- **`fantasm audit summary 2`** — every subroutine with flags
  (`--flag no_description`, end type, code/data). `audit detail 2 <name>`
  — extent, end type, callers, escaping branches. `audit undeclared 2` —
  93 JSR targets with no `d.subroutine()` (promotion candidates, see
  Scope).
- **`fantasm cfg sub-context 2 <name>`** — the routine's body + its call
  sites + exit points. The best single view for deriving a contract:
  exit points show what's set on return; call sites show what callers
  set up.
- **`fantasm cfg sub 2 <name>`** — callers/callees. **`cfg depth 2`** —
  leaves-first ordering. **`cfg leaves 2`** / **`cfg roots 2`**.
- **`fantasm asm extract 2 <name>`** — read the routine in context (its
  inline comments are now rich — lean on them to derive the contract).
- **`fantasm sub insert <driver> <addr>`** — where a *new*
  `d.subroutine()` belongs in address order (for promotions).
- **`fantasm driver sort <driver> -i`** — sort the whole driver into
  canonical address order (see "Driver layout" below).

## Workflow per routine

1. `uv run tools/banner_status.py` → pick the next leaf without a
   contract.
2. `uv run fantasm cfg sub-context 2 <name>` and/or
   `fantasm asm extract 2 <name>` — derive the contract from the body,
   exit points and callers. The inline comments already name the ZP
   locations; the entry instructions show what's read, the exit
   instructions what's set, and stable registers (e.g. an untouched X)
   are "preserved".
3. Review the title/description for accuracy; rewrite if stale/thin.
4. Edit the driver: the literal `d.subroutine(...)` call, or the
   `HANDLER_INFO` entry + loop. Add `on_entry`/`on_exit`.
5. `uv run fantasm disassemble 2`, then `verify 2` (must say
   "Verification PASSED: 16384 bytes match"), `lint 2 <driver>`,
   `comments check 2` — all clean before committing.
6. Commit per coherent batch; update the batch-log table + status header
   + resume pointer here; re-run the worklist tool.

## Applying edits

Banners are larger and more varied than the inline one-liners, so the
single-line regex trick from the inline pass mostly doesn't apply. Edit
the driver with the normal file-editing tools: locate the
`d.subroutine(...)` call (or `HANDLER_INFO` entry) by name, and add the
`on_entry=`/`on_exit=` kwargs / rewrite the description. Re-run
`disassemble` + `verify` after every batch — banners don't emit bytes,
so a passing verify just confirms you didn't corrupt the driver, but it
also catches typos that break the Python.

Do NOT hand-edit the generated `.asm`/`.json`; they are rebuilt by
`fantasm disassemble`.

## Driver layout (address order)

The driver is **not** currently in canonical address order (71
out-of-order `d.subroutine` steps; `fantasm driver sort ... --check`
reports a large diff). Goal: leave it address-ordered.

- `fantasm driver sort <driver> -i` rewrites it in place (imports/create
  /load pinned top, render block pinned bottom, address-keyed
  annotations sorted by first-arg address; for/while blocks like the
  HANDLER_INFO loop anchor at their first iteration's literal).
- **Recommended first batch:** run the sort, `verify 2` (must stay
  byte-identical — sorting only moves statements, emits no bytes),
  eyeball the diff (it relocates the module docstring, which is benign),
  and commit it on its own. Starting from a sorted file makes every
  subsequent banner edit land in an obvious place, and
  `fantasm sub insert` keeps new declarations ordered.
- Re-run `driver sort --check` before the final commit so it stays
  sorted.

## Scope

Primary: the 285 ROM banners (`&8000-&BFFF`) — review description +
add contract. Out of scope: OS vectors (osbyte/osword/… at &FFxx,
declared by the `acorn_mos` environment) and pure data tables
(`keyword_table`).

Secondary / optional (judge as you go): `fantasm audit undeclared 2`
lists 93 JSR targets that are real routines but have no
`d.subroutine()` banner (currently auto-named `cXXXX`/`sub_cXXXX`). The
genuinely reusable ones deserve promotion to named subroutines with
banners (use `fantasm sub insert`); the one-off internal jump targets do
not. Don't bulk-promote — promote only where it improves the call graph
and the reader's understanding, and note each in the batch log.

## Quality bar recap

- A banner says *what + how to call*, above the inline altitude.
- Name the **domain effect** and the **ZP/register contract**; use the
  driver's existing ZP label names.
- Verify contracts against the code (`cfg sub-context`, exit points,
  callers) — never assert a register state you haven't checked.
- 62-char-ish lines render best; Acorn `&XXXX` in text, `0xXXXX` in
  driver source.
- Establish the `stmt_*` / `fn_*` shared conventions once, up front.

## Reference works

- **dasmos driver API:** <https://acornaeology.github.io/dasmos/driver_api.html>
  (local source: `/Users/rjs/Code/acornaeology/dasmos/src/dasmos/` —
  `disassembler.py` `subroutine()` is the authority for the kwargs).
- **fantasm guide:** <https://acornaeology.github.io/fantasm/> (audit,
  cfg, driver, sub subcommands and the `fantasm.toml` schema).
- **`tools/jgh_correlation.tsv`** (J.G. Harston) and the **Advanced
  BASIC ROM User Guide** (Colin Pharo): zero-page map, calling
  conventions, FP accumulator layout — the authority for what the ZP
  locations *mean*.
- **`ANNOTATION_PROGRESS.md`** — the completed inline pass; its glossary
  of ZP labels (`zp_iwa` = integer work accumulator, `fwa`/`fwb` = FP
  accumulators A/B, `string_work` = &0600 buffer, etc.) is the
  vocabulary to reuse.
- The **20 already-documented routines** (run `banner_status.py --all`,
  pick the `D E X` rows) are worked examples — match their style.

## Constraints

Never mention Claude/Anthropic/the model in comments or commit messages;
no emojis in commit messages; never `git push`; prefer
`_filepath`/`_dirpath`/`_filename` suffixes. End commit messages with the
`Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>` trailer.

## Batch log

| Date | Batch | Routines | Contracts added | Remaining | Commit |
|------|-------|----------|-----------------|-----------|--------|
| 2026-06-14 | setup | banner_status.py tool + this tracker | — | 265 | — |
| 2026-06-14 | driver sort | (whole driver) address-ordered | — | 265 | b8a29c5 |
| 2026-06-14 | shared contracts | ~112 table-generated stmt_*/fn_* handlers | 111 | 154 | 8ed2ace |
| 2026-06-14 | FP primitives | 17 FWA/FWB pack/unpack/move/mantissa routines | 17 | 137 | ad91f78 |
| 2026-06-14 | FP ptrs + helpers | 7 point_* setters, byte/print/int-result helpers; fixed iwa_from_ya + fn_to | 15 | 122 | eccee24 |
| 2026-06-14 | value stack + loaders | stack/unstack/drop + load_real_var/load_string_var; fixed unstack_integer | 8 | 114 | 8afd278 |
| 2026-06-14 | line/program helpers | check/decode_line_number, parse_decimal_u16, advance_to_next_line, check_subscript_bound, clear_value_bytes; fixed find_program_line | 7 | 107 | e46362b |
| 2026-06-14 | variable management | find_variable, find_proc_fn, create_variable, validate_var_name | 4 | 103 | 3e6bd5e |
| 2026-06-14 | number<->FP conversion | int_to_fwa, small_int_to_fwa, fwa_mul10/div10, output_* digit helpers, parse_exponent | 9 | 94 | ac0bf3c |
| 2026-06-14 | integer/RND/USR | iwa_inc, imul16, iwa_store_zp, unstack_int_to_zp, rnd_step, rnd_repeat, read_key_timed, usr_call | 8 | 86 | 48d054e |
| 2026-06-14 | FP operators | add/sub/mul/div var + fwb, compare, round, negate, set_one, swap, to_int/to_int2, split_int_frac | 16 | 70 | d469dd8 |
| 2026-06-14 | RND/stack/helpers | rnd_seed/integer/fraction/range, fwa_reciprocal, fwa_sub_var, stack_real/string, print_hex_byte, load_byte_var, encode_line_number | 11 | 59 | c4b3f45 |
| 2026-06-14 | evaluator chain | eval_factor + levels 2-7 (shared contract via table) + eval_and_compare, eval_real, ensure_real | 10 | 49 | cb17bf0 |
| 2026-06-14 | parsers + int divide | check_end_of_statement, expect_eq, skip_spaces_expect_comma, check_eq_star_bracket, eval_after_eq, eval_channel, iwa_divide, iwa_test_var; fixed iwa_divide operand roles | 8 | 41 | f1c5dc7 |
| 2026-06-14 | inline assembler | asm_parse_mnemonic, asm_opcode_add4/8/16, assembler_exit | 5 | 36 | a48534d |
| 2026-06-14 | assignment | parse_var_ref, parse_lvalue, assign_string, assign_number, unstack_value_to_var, try_variable_assignment | 6 | 30 | 85c1085 |
| 2026-06-14 | program/loops | statement_loop, execute_line, immediate_loop, clear_vars_heap_stack, load_program, start_new_program, check_program, delete_program_line, find_line_target | 9 | 21 | e915886 |
| 2026-06-14 | transcendental/print | parse_number, fp_eval_cont_frac, fwa_complement_half_pi, sin_cos_reduce, fwa_int_power, print_special_item, print_line_number, print_token, print_listo_indent | 9 | 12 | 254bb1c |
| 2026-06-14 | final helpers | tokenise_line, read_string_literal, find_def, find_error_line, next_data_item, language_startup, stack_local, read_input_line, index_array, trace_line, stmt_listo | 11 | 1 | 781d56c |
| 2026-06-14 | re-sort | driver back to canonical order | — | 1 | 2008518 |

## Resume here

**The banner pass is COMPLETE** — 284/285 documented. Nothing remains in
this pass. The shared-contract dicts live in the top constants block:
`STMT_ON_ENTRY`/`STMT_ON_EXIT` and `FN_ON_ENTRY`/`FN_ON_EXIT` (above
`HANDLER_INFO`) for the dispatched keyword handlers, and
`EVAL_LEVEL_ON_ENTRY`/`EVAL_LEVEL_ON_EXIT` for the precedence-climbing
evaluator levels. A HANDLER_INFO entry may override either family default
with an optional 3rd/4th tuple element (None = use the default).

Possible follow-ups, all out of this pass's scope:

1. **Inline-comment fix:** iwa_divide (&99BE) has ~5 inline comments that
   swap "dividend"/"divisor"; the banner is correct, the inline labels
   are not. A small inline-pass correction.
2. **Optional promotions:** `fantasm audit undeclared 2` still lists
   JSR'd routines with no banner (auto-named cXXXX). Promote only the
   genuinely reusable ones, leaves-first, noting each in the batch log.
3. **Consider** demoting fwa_compare_var (&A5FF) from `d.subroutine` to a
   plain `d.label` — it is a fall-through point with no callers, not a
   routine. Would make the count 284/284. Verify it stays byte-identical.
