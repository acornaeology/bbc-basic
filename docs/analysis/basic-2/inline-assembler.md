# The inline 6502 assembler in BBC BASIC II

> **Scope.** This article describes the **BBC BASIC II** inline 6502 assembler — the `[ ... ]` feature that lets machine code be written and assembled directly from a BASIC program. Every routine, workspace address and opcode-table detail is specific to this version and was read from the disassembly (which reassembles byte-identically to the ROM). The assembler shares the interpreter's expression evaluator and variable storage; the [parsers and evaluators](parsers-and-evaluators.md) and [program lifecycle](program-lifecycle.md) articles cover the machinery on which it relies.

BBC BASIC's inline assembler is closely integrated with the interpreter: rather than a separate macro layer, it is a thin front end over the *same* expression evaluator, variable table and tokeniser the interpreter already provides. Three consequences of that integration account for most of the assembler's behaviour:

> 1. **Labels are ordinary BASIC variables.** `.loop` assigns the current program counter to a variable called `loop`.
> 2. **`P%` and `O%` are resident integers.** The program counter and the offset-assembly address are just two of the `A%`–`Z%` slots, readable and writable from BASIC.
> 3. **Assembly is single-pass per `[ ... ]`.** Two-pass assembly is a *BASIC-level idiom* (`FOR…[OPT…]…NEXT`), enabled by one bit of `OPT` that decides whether an undefined label is an error or evaluates to `P%`.

## Entering and leaving: `[` and `]`

`[` at the start of a statement is recognised by [`check_eq_star_bracket`](address:8B60@2?hex) and jumps to [`asm_enter`](address:8504@2?hex), which sets the default **`OPT 3`** and falls into the main loop [`asm_loop`](address:8508@2?hex):

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

The terminator `]` is only ever tested **at the start of a statement** (the first non-space character). [`assembler_exit`](address:84FD@2?hex) sets the `OPT` flag [`zp_opt_flag`](address:0028@2?hex) to `&FF` and returns to the interpreter. That `&FF` is doing double duty: it is the *"not currently assembling"* sentinel that the rest of the ROM checks (see *Forward references* below).

Because `]` is only the terminator at statement-start, it is safe **inside an `EQUS` string** — `EQUS "Contains]"` assembles the nine bytes verbatim, since the `]` is read as string data by the `EQUS` operand evaluator and never reaches the statement-start test.

## `P%`, `O%` and offset assembly

The program counter `P%` lives at [`resint_p`](address:0440@2?hex) and the offset address `O%` at [`resint_o`](address:043C@2?hex) — the `'P'` and `'O'` slots of the resident integers `A%`–`Z%`. They are therefore plain BASIC variables: one may set `P% = &2000` before a block and read `P%` afterwards to find its end.

Assembled bytes are written by [`asm_emit`](address:862B@2?hex), which picks the destination from **`OPT` bit 2**:

- bit 2 clear → store at `P%` (the normal case);
- bit 2 set (`OPT >= 4`) → store at `O%` instead, while still advancing `P%`.

This is **offset assembly**: the code is laid down at `O%` but assembled *as if* it will run at `P%` (so that all address calculations use `P%`). It is the means of building code in a spare buffer that will later be copied to, or paged into, its true run address. `P%` always advances; `O%` advances only while bit 2 is set.

## The `OPT` directive

`OPT` is the assembler's options directive: `OPT n` sets a flag whose individual bits govern listing, error reporting and offset assembly. [`asm_opt_directive`](address:8813@2?hex) evaluates the expression `n` and stores the result in [`zp_opt_flag`](address:0028@2?hex). The bits are:

| Bit | Value | Meaning |
|---|---|---|
| 0 | 1 | **Listing** — print each assembled line |
| 1 | 2 | **Error reporting** — report undefined labels and out-of-range branches (rather than tolerating them) |
| 2 | 4 | **Offset assembly** — store at `O%`, assemble for `P%` |
| — | `&FF` | not inside `[ ]` (set on exit) |

The default on entry is `OPT 3` (listing and error reporting, assembling to `P%`). Bit 1 is the flag on which two-pass assembly depends, as the sections below describe.

## The packed mnemonic table (and the `OPT`/`EQU` directives)

[`asm_parse_mnemonic`](address:85BA@2?hex) reads the three-letter mnemonic, takes the **low 5 bits of each letter** (so `A`=1 … `Z`=26) and packs them **most-significant letter first** into a 15-bit key held in `&3D` (low) / `&3E` (high). [`asm_mn_search`](address:85F1@2?hex) then walks one index register **from `&3A` down to `1`** — a **one-based** scan — comparing the low half against [`asm_mnemonic_lo`](address:8451@2?hex)`-1,X` and, on a hit, the high half against `asm_mnemonic_hi-1,X`. A match yields an **index** that does two jobs at once: it selects the base opcode from [`asm_base_opcode`](address:84C5@2?hex)`-1,X`, and its numeric *value* routes the operand parser to the right addressing-mode handler. (Those `-1` bases are what let each table start at index `&01` with no wasted zeroth entry — see below.)

Before the search, the statement dispatcher peels off the non-mnemonic cases:

- `:` or carriage return → empty statement;
- `\` → a comment to end of statement;
- `.` → a **label definition** (below);
- tokenised `AND` / `EOR` / `OR` → [`asm_logic_mnemonic`](address:8607@2?hex), because these collide with BASIC keywords and are stored as single tokens, not letters (they rejoin the opcode path at indices `&22`–`&24`).

Everything else — **including the `OPT` and `EQU` directives** — goes through the packed table. There are 58 index slots, `&01`–`&3A`:

| Index | Entries | Operand handling |
|---|---|---|
| `&01`–`&19` | `BRK`…`TYA` | implied (opcode only) |
| `&1A`–`&21` | `BCC`…`BVS` | relative branch |
| `&22`–`&28` | `AND`…`SBC` | full modes: `#`/zp/abs/`(zp,X)`/`(zp),Y`/`,X`/`,Y` |
| `&29`–`&2C` | `ASL`…`ROR` | accumulator (`A`) or memory |
| `&2D`–`&2E` | `DEC`, `INC` | memory only |
| `&2F`–`&30` | `CPX`, `CPY` | `#`/zp/abs |
| `&31` | `BIT` | abs/zp |
| `&32`–`&33` | `JMP`, `JSR` | abs; `JMP` also `(abs)` |
| `&34`–`&36` | `LDX`, `LDY`, `STA` | with index register |
| `&37`–`&38` | `STX`, `STY` | two-register form |
| `&39` | `OPT` | directive → [`asm_opt_directive`](address:8813@2?hex) |
| `&3A` | `EQU` | directive → [`equb_directive`](address:883A@2?hex) (`EQUB`/`W`/`D`/`S`) |

Indices `&01`–`&38` are exactly the **56 NMOS 6502 mnemonics** (BASIC II predates the 65C02 — there are no `&C02` mnemonics); `&39`/`&3A` are the two directives, recognised by the *same* packed hash rather than a separate keyword test. `OPT` and `EQU` therefore have no `asm_base_opcode` entry — the operand parser branches to their handlers on the index before it would ever read one.

The **base opcodes are the addressing-mode "column 0" value** of each instruction group; the operand parser steps between the 6502's regular four-column mode layout with the `+4`/`+8`/`+16` helpers ([`asm_opcode_add4`](address:8832@2?hex)/[`asm_opcode_add8`](address:882F@2?hex)/[`asm_opcode_add16`](address:882C@2?hex)). A few base bytes are slot values rather than legal standalone opcodes (e.g. `BIT` base `&20`, `LDX`/`LDY`-immediate `&A2`/`&A0`). Zero-page versus absolute is **selected automatically from the operand's high byte**: a zero high byte gives the 2-byte zero-page form, otherwise the 3-byte absolute form ([`asm_zp_or_abs`](address:8738@2?hex)). This behaviour interacts with forward references, as discussed below.

The index register counts from `&3A` down to `1` and never reaches `0`, so the tables carry no zeroth entry: each begins at index `&01`. The lookups accommodate this by naming the base address *minus one* — `asm_mnemonic_lo-1,X`, `asm_mnemonic_hi-1,X`, `asm_base_opcode-1,X` — the conventional 6502 idiom for a one-based table. With `X` in the range `1`–`&3A` the effective address spans exactly entries `&01`–`&3A`. The three arrays are consequently packed contiguously, with neither padding nor overlap: [`asm_mnemonic_lo`](address:8451@2?hex) occupies `&8451`–`&848A`, [`asm_mnemonic_hi`](address:848B@2?hex) `&848B`–`&84C4`, and [`asm_base_opcode`](address:84C5@2?hex) begins at `&84C5`.

## Labels as BASIC variables

A leading `.` runs [`asm_define_label`](address:85A5@2?hex):

```
.asm_define_label
    jsr parse_lvalue        ; parse the name as an assignment target
    ...
    jsr factor_pcounter     ; value = P%
    jsr assign_number       ; label_variable = P%
```

So `.loop` is literally `loop = P%` — the label is an ordinary **floating-point variable** holding the address. A BASIC variable name is integer only when it carries a `%` suffix, so a bare label defines a floating-point variable, presumably so that the same plain name denotes the label at its definition (`.loop`) and at every reference (`loop`); an integer label would have to be spelled `.loop%` and referenced as `loop%`. It follows that labels live in the same namespace as program variables, persist after the block, and can be read or even reassigned from BASIC; an indirection or empty name where a label is expected raises *Mistake*.

## Forward references and the two-pass idiom

The handling of forward references is what makes the two-pass idiom possible. When the expression evaluator meets a reference to an **undefined** variable, it reaches [`factor_undefined`](address:AE30@2?hex):

```
.factor_undefined
    lda zp_opt_flag
    and #2                  ; OPT bit 1 (error reporting) set?
    bne no_such_variable    ; yes: raise "No such variable"
    bcs no_such_variable    ; (a malformed name still errors)
    stx zp_text_ptr2_off    ; otherwise accept it...
    ...                     ; ...falls into factor_pcounter → value = P%
```

So an undefined label evaluates to **`P%`** (the current program counter, supplied by [`factor_pcounter`](address:AE3A@2?hex)) when `OPT` bit 1 is clear, and raises an error when it is set. The same path serves ordinary BASIC: outside `[ ]` the flag is `&FF`, so bit 1 is always set and an undefined variable always errors. It is *only* inside the assembler, with error reporting disabled, that an undefined name is tolerated.

The classic two-pass loop relies on exactly this behaviour:

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

The choice to return **`P%` rather than `0`** for an unknown forward reference is deliberate and consequential, in two complementary ways. First, **sizing**: `P%` is a genuine 16-bit address with (usually) a non-zero high byte, so `LDA forwardlabel` sizes to **absolute (3 bytes)** on pass 1 — matching the 3-byte absolute it will be on pass 2 once the label resolves to a real address. Had an undefined reference evaluated to `0`, pass 1 would size it *zero-page (2 bytes)* and pass 2 *absolute (3 bytes)*, growing the instruction and shifting everything after it. Second, **branch range**: a forward branch such as `BNE fwd` evaluates its not-yet-defined target as `P%`, giving an offset of about −2 rather than a wild displacement measured from `0`, so the branch is trivially in range on pass 1 even though its target does not yet exist. Between them, instruction sizes and label addresses stay consistent across the two passes.

The residual failure case is a forward reference that ultimately resolves to a **zero-page** address: pass 1 sizes it absolute (operand `P%`, non-zero high byte), pass 2 zero-page, and the instruction shrinks — shifting every address after it. BBC BASIC II offers no directive to force an addressing mode — the mode is chosen solely from the operand's high byte, and the pass-1 value is `P%`, which cannot be coerced to zero page — so the only remedy is to **define zero-page labels before they are used**, giving both passes the same small value:

```basic
   10 DIM code% 256
   20 zpwork = &70                 : REM define the zero-page label up front
   30 FOR pass% = 0 TO 3 STEP 3
   40   P% = code%
   50   [ OPT pass%
   60     LDA zpwork               \ zero-page (2 bytes) on both passes
   70   ]
   80 NEXT
```

Assign `zpwork` *after* the block instead and pass 1 would size the `LDA` absolute, pass 2 zero-page, and every label following it would take a different value on each pass.

## The `EQU` directives

[`equb_directive`](address:883A@2?hex) dispatches on the letter after `EQU`:

- **`EQUB` / `EQUW` / `EQUD`** evaluate a **numeric** expression (`eval_expr_to_integer`) and emit 1 / 2 / 4 bytes.
- **`EQUS`** evaluates a **string** expression and emits its bytes; a non-string operand raises *Type mismatch*.

Thus `EQUS "AB]"` embeds text (including a `]`), whereas `EQUB` requires a number — `EQUB ASC("]")`, `EQUB &5D` or `EQUB 93` for a single byte. Passing a string to `EQUB` raises *Type mismatch*.

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
