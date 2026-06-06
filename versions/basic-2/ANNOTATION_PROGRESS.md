# BBC BASIC II annotation progress

Tracks the bottom-up annotation of the disassembly. Verify must stay
byte-identical and lint clean after every batch
(`uv run fantasm disassemble 2 && uv run fantasm verify 2 &&
uv run fantasm lint 2 versions/basic-2/disassemble/disasm_basic_2.py`).

## Foundations (done)

- [x] Bootstrap: round-trip byte-identical, CI, docs.
- [x] Zero-page / RAM map imported from Pharo ch. 7 (`zp_*`, resident
      integer variables, FP temporaries, variable table, stacks/buffers).
- [x] Keyword table bannered at `&8071`; tokeniser flag bits documented.
- [x] Statement/function dispatch decoded: action-address tables at
      `&836D`/`&83DF` seeded with `code_ptr`; all 114 handlers traced and
      declared as subroutines (`fn_*` / `stmt_*`).
- [x] Header noted; `language_startup` (`&8023`) annotated;
      `immediate_loop` (`&8ADD`), `brk_handler` (`&B402`) named.

## Core leaf utilities

- [x] `skip_spaces` (`&8A97`) — skip spaces at the primary text pointer.
- [x] `skip_spaces_ptr2` (`&8A8C`) — same, secondary pointer.
- [x] `skip_spaces_expect_comma` (`&8AAE`).
- [x] `read_via_ptr_general` (`&8942`), `inc_ptr_general` (`&8944`).
- [ ] Remaining high-call utilities from `fantasm audit undeclared 2`
      (e.g. `&8821`, `&8C1E`, `&8821`, the `&882C`/`&882F`/`&8832` group).

## Tooling

- [x] `tools/correlate_jgh.py` — aligns JGH's `Basic2.src` against our
      disassembly (label anchors + 98.6% opcode match) and harvests his
      inline comments and routine banners keyed by our addresses. Outputs
      gitignored; used as a research aid (we write our own annotations).

## Pharo reference sweep (build foundational routine declarations)

- [x] Ch. 7 memory map (zero page, RAM, tables).
- [x] Ch. 2 integer routines (IWA): `iwa_negate/abs/add/rsub/mul/div/mod/
      test_var/from_ya/load_var/store_var/load_zp/store_zp`.
- [x] Ch. 3 floating-point routines (FWA/FWB): clear/set_one/negate/
      normalise/round/reciprocal/copy/swap/compare, add/sub/mul/div
      variants, pack/unpack to temps and variables.
- [x] Ch. 4 conversions: ascii_to_number, number_to_ascii (the shared
      &9EDF int/FP -> decimal/hex routine), fwa_to_int/fwa_to_int2,
      int_to_fwa.
- [x] Ch. 5 mathematical functions: descriptions attached to the fn_*
      handlers (SIN/COS/TAN/ASN/ACS/ATN/LN/LOG/EXP/SQR/DEG/RAD/PI), each
      noting the pure FWA-in routine a few bytes on.
- [x] Ch. 6 random numbers: rnd_integer/fraction/repeat/range/seed.
- [x] Entry/exit detail for the highest-value conventions: integer
      routines (Pharo ch. 2.4) — including the insight that the binary
      ops take their second operand via the BASIC stack pointer
      (&04/&05) — and the conversions (ch. 4.3: SWA / &36 / &15 / @%).
      The FP-operand convention (&4B/&4C) is documented in the FP
      section header. Remaining per-routine register-kill detail for FP
      / maths / random (uniform: arg in FWA, result in FWA, registers
      destroyed) can be folded in on demand from ch. 3.6 / 5.2 / 6.3.

## Statement / function handlers

- [x] All `stmt_*` statement handlers (AUTO..WIDTH) carry a behaviour +
      syntax description, attached via HANDLER_INFO in the dispatch loop.
      Syntax forms cross-checked against JGH banners and the User Guide.
- [x] Maths `fn_*` handlers described (Pharo ch. 5).
- [ ] Remaining `fn_*` handlers (non-maths: OPENIN/PTR/PAGE reads,
      ASC/CHR$/LEN/VAL/INSTR/GET/INKEY, EOF/EXT/COUNT, etc.).
- [ ] Per-statement inline comments (next density pass).

## Next (bottom-up, by subsystem)

Use `fantasm cfg leaves 2` and `fantasm audit undeclared 2` to pick
self-contained routines first, then climb.

- [ ] Tokeniser / line-entry path (`&8451` data table + the code that
      consumes it; the immediate loop at `&8ADD`).
- [ ] Expression evaluator and the integer/FP accumulator primitives
      (`zp_iwa` `&2A`, `zp_fwa` `&2E`, `zp_fwb` `&3B`) — needed before
      the maths functions read cleanly.
- [ ] Floating-point pack/unpack and arithmetic (Pharo ch. 3).
- [ ] Maths functions: `fn_abs`, `fn_sqr`, `fn_sin`/`fn_cos`, … (Pharo
      ch. 5 documents the algorithms and entry/exit conventions).
- [ ] Variable storage and lookup (`var_ptr_table` `&0480`; Pharo ch. 7.5).
- [ ] Simple statement handlers: `stmt_end`, `stmt_stop`, `stmt_clear`, …
- [ ] Print / number formatting (`@%`, `zp_print_flag`, `zp_count`).

## Notes

- The `keyword_table` banner currently shows as the container for the
  interpreter core above the lowest handler (`&8AB6`); this resolves as
  the core routines between `&8451` and `&8AB6` get declared.
- There is a further data table at `&8451` (after the action tables) —
  identify and banner it.
- References: Pharo's *Advanced BASIC ROM User Guide* (internals),
  J.G. Harston's `Basic2.src` (labels/structure; local under
  `docs/disasm/MDFS/`), Toby Nelson's OS 1.20 (`/Users/rjs/Code/os120`)
  for MOS call semantics.
