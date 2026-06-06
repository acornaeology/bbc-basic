# Inline-comment pass progress

Annotating per-instruction comments **bottom-up**: leaf routines first
(no internal callees, from `fantasm cfg leaves 2`), then reverse
breadth-first up the call graph, so understanding accumulates.

Goal: comment intent, not opcodes — what the values represent, what
structures are manipulated, why the code is shaped this way. Rename
code/data labels once a routine's purpose is clear. Verify + lint after
each batch; verify must stay byte-identical.

Cross-references: `tools/jgh_correlation.tsv` (regenerate with
`uv run tools/correlate_jgh.py`), Pharo chapters, the JGH banners.

## Key structures (reference for the comments)

- **Packed float (5 bytes)**: exponent (excess-128; &00 => value is 0),
  then mantissa-1..4. Mantissa is normalised (implied leading 1).
  Sign lives in bit 7 of mantissa-1: 0 = positive (implied 1 cleared),
  1 = negative (implied 1 left set). Negate = toggle that bit.
- **Unpacked float**: FWA = &2E sign, &2F overflow, &30 exponent,
  &31-&34 mantissa-1..4, &35 rounding. FWB = &3B..&42 likewise.
  Unpack restores the implied 1 into mantissa-1 bit 7 and lifts the
  sign into the sign byte; clears overflow and rounding.
- **IWA** (integer work area, &2A-&2D): 32-bit signed, little-endian.
- **BASIC value stack**: grows down from HIMEM; top in zp_stack_ptr
  (&04/&05). Integers pushed as 4 bytes, reals as 5, strings as text
  + length.

## Data-label renames (foundational)

- [x] FWA / FWB byte fields (zp_fwa_sign/ovf/exp/m1-m4/rnd and the FWB
      twins) and IWA bytes (zp_iwa, zp_iwa_1-3) — makes every numeric
      routine self-documenting.
- [x] zp_fp_ptr (&4B/&4C) — the packed-fp-variable pointer used by the
      FP routines.

## Leaf batch 1 (numeric primitives)

- [x] fwa_clear (&A686) — self-documenting via the field labels.
- [x] fwa_sign (&A1DA) — returns +1/0/-1; zero iff mantissa all zero.
- [x] iwa_from_ya (&AEEA) — unsigned 0-65535 into IWA.
- [x] fwa_unpack_var (&A3B5) — packed 5-byte -> unpacked 8-byte FWA.
- [x] fwa_pack_var (&A38D) — sign-fold into mantissa bit 7.
- [x] fwa_normalise (&A303) — byte then bit shift to set mantissa MSB.
- [x] fwa_round (&A65C) + fwa_round_carry (&A2A4, renamed).
- [x] stack/unstack: stack_integer/real/string, unstack_integer; the
      shared reserve_stack (&BE2E, renamed) heap-collision check.
- [ ] skip_spaces (&8A97), skip_spaces_ptr2 (&8A8C) — enrich
- [ ] Move up: fwa arithmetic (add/mul/div), then evaluator.

## Done

- Batch 1: FWA/FWB/IWA field labels; fwa_clear, fwa_sign, iwa_from_ya,
  fwa_unpack/pack_var, fwa_normalise, fwa_round, the stack push/pop
  primitives and reserve_stack. Renames: fwa_round_carry, reserve_stack,
  err_too_big, err_no_room; labelled zp_fp_ptr, zp_stack_ptr_1,
  zp_vartop_1.
