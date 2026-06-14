# BBC BASIC II annotation — label-naming pass

**STATUS: in progress — 787 auto-generated labels remaining (of 864).
Goal: give every dasmos auto-named label (`cXXXX`, `loop_cXXXX`,
`sub_cXXXX`, `lXXXX`) a semantically meaningful, globally unique name.**

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

## Resume here

Done through the inline assembler (&8063-&8831). The append +
`driver sort -i` recipe is confirmed (byte-identical each batch).

Next routine in address order: **parse_decimal_u16 (&889D)**, then
encode_line_number, is_alphanumeric, inc_ptr_general, tokenise_line
(&8955, 35 labels), … Work address-ascending; regenerate the live,
comment-enriched worklist with:

```
uv run fantasm labels classify 2 --no-header --as tsv > /tmp/labels_classify.tsv
# then the python snippet in the conversation builds /tmp/labels_enriched.tsv
```

`/tmp/labels_enriched.tsv` columns: routine, addr, auto-name, category,
refs, inline-comment — a starting hint only; read the full routine body
before naming (see step 1).
