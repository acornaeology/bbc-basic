# The inline 6502 assembler in BBC BASIC II

> **Scope.** This article describes the **BBC BASIC II** inline 6502 assembler — the `[ ... ]` feature that lets machine code be written and assembled directly from a BASIC program. Every routine, workspace address and opcode-table detail is specific to this version and was read from the disassembly (which reassembles byte-identically to the ROM). The assembler shares the interpreter's expression evaluator and variable storage; the [parsers and evaluators](parsers-and-evaluators.md) and [program lifecycle](program-lifecycle.md) articles cover the machinery it leans on.

BBC BASIC's inline assembler is unusually well integrated: it is not a bolted-on macro layer but a thin front end over the *same* expression evaluator, variable table and tokeniser the interpreter already has. Three facts follow from that integration and explain almost everything about how the assembler behaves:

> 1. **Labels are ordinary BASIC variables.** `.loop` assigns the current program counter to a variable called `loop`.
> 2. **`P%` and `O%` are resident integers.** The program counter and the offset-assembly address are just two of the `A%`–`Z%` slots, readable and writable from BASIC.
> 3. **Assembly is single-pass per `[ ... ]`.** Two-pass assembly is a *BASIC-level idiom* (`FOR…[OPT…]…NEXT`), enabled by one bit of `OPT` that decides whether an undefined label is an error or evaluates to `P%`.

## Entering and leaving: `[` and `]`

`[` at the start of a statement is recognised by [`check_eq_star_bracket`](address:8B60@2?hex) (`&8B60`) and jumps to [`asm_enter`](address:8504@2?hex) (`&8504`), which sets the default **`OPT 3`** and falls into the main loop [`asm_loop`](address:8508@2?hex):

```
.asm_enter
    lda #3                  ; default OPT 3 (listing + error reporting, assemble to P%)
    sta zp_opt_flag
.asm_loop
    jsr skip_spaces
    cmp #ASC("]")           ; &850B — ']' only here ends the assembler
    beq assembler_exit
    ...                     ; assemble one statement, optionally list it, advance
```

The terminator `]` is only ever tested **at the start of a statement** (the first non-space character). [`assembler_exit`](address:84FD@2?hex) (`&84FD`) sets the `OPT` flag [`zp_opt_flag`](address:0028@2?hex) (`&28`) to `&FF` and returns to the interpreter. That `&FF` is doing double duty: it is the *"not currently assembling"* sentinel that the rest of the ROM checks (see *Forward references* below).

Because `]` is only the terminator at statement-start, it is safe **inside an `EQUS` string** — `EQUS "Contains]"` assembles the nine bytes verbatim, since the `]` is read as string data by the `EQUS` operand evaluator and never reaches the statement-start test.

## `P%`, `O%` and offset assembly

The program counter `P%` lives at [`resint_p`](address:0440@2?hex) (`&0440`) and the offset address `O%` at [`resint_o`](address:043C@2?hex) (`&043C`) — the `'P'` and `'O'` slots of the resident integers `A%`–`Z%`. So they are plain BASIC variables: set `P% = &2000` before a block, read `P%` after it to find the end.

Assembled bytes are written by [`asm_emit`](address:862B@2?hex) (`&862B`), which picks the destination from **`OPT` bit 2**:

- bit 2 clear → store at `P%` (the normal case);
- bit 2 set (`OPT >= 4`) → store at `O%` instead, while still advancing `P%`.

This is **offset assembly**: the code is laid down at `O%` but assembled *as if* it will run at `P%` (so all address calculations use `P%`). It is how you build code in a spare buffer that will later be copied to, or paged into, its real run address. `P%` always advances; `O%` advances too only while bit 2 is set.

## `OPT`: four bits, two of which matter a lot

[`asm_opt_directive`](address:8813@2?hex) (`&8813`) evaluates `OPT n` and stores `n` into the flag. The bits ([`zp_opt_flag`](address:0028@2?hex)):

| Bit | Value | Meaning |
|---|---|---|
| 0 | 1 | **Listing** — print each assembled line |
| 1 | 2 | **Error reporting** — report undefined labels and out-of-range branches (rather than tolerating them) |
| 2 | 4 | **Offset assembly** — store at `O%`, assemble for `P%` |
| — | `&FF` | not inside `[ ]` (set on exit) |

Default on entry is `OPT 3` (listing + errors, assemble to `P%`). Bit 1 is the one that makes two-pass assembly work.

## Mnemonics: a 58-entry packed table

[`asm_parse_mnemonic`](address:85BA@2?hex) (`&85BA`) packs a three-letter mnemonic **5 bits per letter** into a 15-bit key and searches three parallel 58-entry tables — [`asm_mnemonic_lo`](address:8450@2?hex) / `asm_mnemonic_hi` (`&8450`/`&848A`) for the key, [`asm_base_opcode`](address:84C4@2?hex) (`&84C4`) for the base opcode. The set is the **NMOS 6502** instruction set (BASIC II predates the 65C02 — there are no `&C02` mnemonics). Before the table search, the statement dispatcher handles the non-mnemonic cases:

- `:` or carriage return → empty statement;
- `\` → a comment to end of statement;
- `.` → a **label definition** (below);
- tokenised `AND` / `EOR` / `OR` → handled specially (`asm_logic_mnemonic`), because these mnemonics collide with BASIC keywords and are stored as single tokens, not letters.

Addressing modes are selected by the mnemonic's table-index range and the operand syntax (`#`, `(`, `,X`, `,Y`, `A`, `)`), with the opcode stepped between the 6502's regular four-column mode layout by `+4`/`+8`/`+16` helpers. Zero-page versus absolute is **auto-selected by the operand's high byte**: high byte zero → 2-byte zero-page form, otherwise 3-byte absolute (`asm_zp_or_abs`, `&8738`). Remember that detail — it interacts with forward references.

## Labels are BASIC variables

A leading `.` runs [`asm_define_label`](address:85A5@2?hex) (`&85A5`):

```
.asm_define_label
    jsr parse_lvalue        ; parse the name as an assignment target
    ...
    jsr factor_pcounter     ; value = P%
    jsr assign_number       ; label_variable = P%
```

So `.loop` is literally `loop = P%` — the label is an ordinary integer variable holding the address. Consequences a compiler must mirror: labels live in the same namespace as program variables, persist after the block, can be read or even reassigned from BASIC, and an indirection or empty name where a label is expected raises *Mistake*.

## Forward references and the two-pass idiom

This is the heart of how the assembler is used. When the expression evaluator meets a reference to an **undefined** variable, it reaches [`factor_undefined`](address:AE30@2?hex) (`&AE30`):

```
.factor_undefined
    lda zp_opt_flag
    and #2                  ; OPT bit 1 (error reporting) set?
    bne no_such_variable    ; yes: raise "No such variable"
    bcs no_such_variable    ; (a malformed name still errors)
    stx zp_text_ptr2_off    ; otherwise accept it...
    ...                     ; ...falls into factor_pcounter → value = P%
```

So an undefined label evaluates to **`P%`** (the current program counter) when `OPT` bit 1 is clear, and is an error when it is set. The same path serves normal BASIC: outside `[ ]` the flag is `&FF`, so bit 1 is always set and an undefined variable always errors — it is *only* inside the assembler, with error reporting turned off, that an undefined name is tolerated.

That is exactly what the classic two-pass loop exploits:

```basic
   10 DIM code% 256
   20 FOR pass% = 0 TO 3 STEP 3      : REM OPT 0 then OPT 3
   30   P% = code%
   40   [ OPT pass%
   50     .start LDA #0
   60            BNE start
   70     .end ]
   80 NEXT
```

- **Pass 1 (`OPT 0`, bit 1 clear):** forward references to not-yet-defined labels evaluate to `P%`; no errors; the `.label` assignments create the variables as they are reached.
- **Pass 2 (`OPT 3`, bit 1 set):** every label now exists, references resolve to real addresses, and any genuinely undefined name (or out-of-range branch) is reported.

The choice to return **`P%` rather than `0`** for an unknown forward reference is deliberate and load-bearing: `P%` is a real 16-bit address with (usually) a non-zero high byte, so `LDA forwardlabel` auto-sizes to **absolute (3 bytes)** on pass 1 — matching the 3-byte absolute it will be on pass 2 once the label resolves to another address. Instruction sizes therefore stay consistent between passes and `P%` doesn't drift. (The known failure case is a forward reference that ultimately resolves to a **zero-page** address: pass 1 sizes it absolute, pass 2 zero-page, and everything after it shifts — which is why zero-page labels must be defined before use or forced.)

## The `EQU` directives

[`equb_directive`](address:883A@2?hex) (`&883A`) dispatches on the letter after `EQU`:

- **`EQUB` / `EQUW` / `EQUD`** evaluate a **numeric** expression (`eval_expr_to_integer`) and emit 1 / 2 / 4 bytes.
- **`EQUS`** evaluates a **string** expression and emits its bytes; a non-string operand raises *Type mismatch*.

So `EQUS "AB]"` is the way to embed text (including a `]`), while `EQUB` wants a number — `EQUB ASC("]")`, `EQUB &5D` or `EQUB 93` for a single byte. Passing a string to `EQUB` is a *Type mismatch*.

## The listing (`OPT` bit 0)

With bit 0 set, each assembled line prints as: `P%` as four hex digits, then the assembled bytes in hex (wrapping with an indent when an `EQUS` runs long), then the **de-tokenised source** line (via `print_token`, so keywords reappear as text). This is the familiar two-column assembler listing.

## Errors the assembler raises

| Error | BRK code | Cause |
|---|---|---|
| *Mistake* | (syntax) | unknown mnemonic, bad label name, unrecognised `EQU` suffix |
| *Out of range* | `&01` | branch target outside −128…+127 — **only reported when `OPT` bit 1 is set**; otherwise the bad offset is silently assembled |
| *Byte* | `&02` | an immediate / zero-page value > 255 |
| *Index* | `&03` | malformed indexed/indirect operand, or an index-register mismatch |
| *Type mismatch* | — | `EQUS` given a non-string |
| *No such variable* | — | undefined label with `OPT` bit 1 set (i.e. on the checked pass) |

Note the same OPT-bit-1 gate on *Out of range* as on *No such variable*: pass 1 tolerates both a missing label and a not-yet-valid branch distance; pass 2 enforces them.

## For a compiler

To reproduce BASIC II's assembler faithfully: model labels as entries in the ordinary variable namespace assigned `P%`; expose `P%`/`O%` as the live program counter and offset address; implement `OPT` as the four-bit flag with bit 1 gating both undefined-label tolerance (returning `P%`) and branch-range/`No such variable` reporting; assemble one pass per `[ ... ]` and leave multi-pass to the caller's `FOR` loop; and auto-size zero-page vs absolute by the operand's high byte. The `]`-only-at-statement-start rule and the `P%`-for-unknown-forward-reference rule are both observable behaviours real programs depend on.

## Cross-references

- Entry/loop/exit: [`check_eq_star_bracket`](address:8B60@2?hex) (`&8B60`), [`asm_enter`](address:8504@2?hex) (`&8504`), [`asm_loop`](address:8508@2?hex) (`&8508`), [`assembler_exit`](address:84FD@2?hex) (`&84FD`).
- Mnemonics/operands: [`asm_parse_mnemonic`](address:85BA@2?hex) (`&85BA`), [`asm_mnemonic_lo`](address:8450@2?hex) (`&8450`), [`asm_base_opcode`](address:84C4@2?hex) (`&84C4`), [`asm_emit`](address:862B@2?hex) (`&862B`).
- Labels & forward refs: [`asm_define_label`](address:85A5@2?hex) (`&85A5`), [`factor_undefined`](address:AE30@2?hex) (`&AE30`), [`factor_pcounter`](address:AE3A@2?hex) (`&AE3A`).
- Directives & `OPT`: [`equb_directive`](address:883A@2?hex) (`&883A`), [`asm_opt_directive`](address:8813@2?hex) (`&8813`).
- Workspace: [`zp_opt_flag`](address:0028@2?hex) (`&28`), [`zp_asm_opcode`](address:0029@2?hex) (`&29`), [`resint_p`](address:0440@2?hex) (`P%`), [`resint_o`](address:043C@2?hex) (`O%`).
