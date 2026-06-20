# Indirection lvalues as PROC/FN parameters in BBC BASIC II

> **Scope.** This article is about **BBC BASIC II** — the 16 KB language ROM of the BBC Micro. It documents a little-known capability: that a formal parameter of a `DEF FN`/`DEF PROC` may be *any assignable location*, including a byte (`?`), word (`!`) or string (`$`) indirection onto raw memory, not just a named variable. Every address and value below was read from the disassembly (which reassembles byte-identically to the ROM). The *shape* of the behaviour carries forward to later BASICs; the *addresses* are version II only.

Most people learn `DEF FNarea(w, h) = w*h` and stop there: a parameter is a name, and the name becomes a `LOCAL` variable that holds the argument. That is the common case, but it is not the rule the ROM actually implements. The real rule is stranger and more powerful:

> A formal parameter is parsed by exactly the same routine that parses the left-hand side of `LET`. So **anything you can assign to, you can use as a parameter** — including a `?`, `!` or `$` indirection onto an arbitrary address. The call then *assigns* the argument into that location, runs the body, and restores the location's previous contents on return.

So this is legal, and does what the comment says:

```basic
   10 DIM buf% 32
   20 $buf% = "before"
   30 dummy = FNstore("hello")
   40 PRINT "after the call: ";$buf%
   50 END
   60 DEF FNstore($buf%)            : REM $buf% is the parameter!
   70 PRINT "the body sees:  ";$buf%
   80 = LEN $buf%
```
```
the body sees:  hello
after the call: before
```

The formal is not a variable name at all — it is the *string stored at the address in `buf%`*. Calling `FNstore("hello")` writes `"hello"` (plus a carriage-return terminator) into that buffer **for the duration of the call**, where the body reads it back through the same `$buf%`. On return the buffer's previous contents (`"before"`) are restored — a `$addr` parameter is saved and restored exactly like a `LOCAL`, which is why line 40 prints `before`, not `hello`. (Had we not initialised `buf%` on line 20, "the previous contents" would be whatever uninitialised bytes `DIM` happened to reserve, up to the first carriage return — so always set a buffer before relying on what comes back.) This is not a trick that slips past the parser; it is the parser working exactly as designed — the save/restore mechanics are spelt out [below](#what-binding-to-an-lvalue-parameter-actually-does).


## Why it works: one lvalue parser, used everywhere

BBC BASIC has a single routine for "parse a thing that can be assigned to": [`parse_lvalue`](address:9582@2?hex) (`&9582`), whose own banner describes it as *"Shared by LET and FOR."* It is, in fact, shared by four callers:

| Caller | Site | What it parses |
|---|---|---|
| `LET` / implied `LET` | [`stmt_let`](address:8BE4@2?hex) | the target of `var = expr` |
| `FOR` | [`stmt_for`](address:B7C4@2?hex) | the loop control variable |
| `LOCAL` | [`stmt_local`](address:9323@2?hex) (`jsr` at `&9328`) | each localised variable |
| **`PROC`/`FN` binding** | [`call_proc_fn`](address:B197@2?hex) (`jsr` at `&B256`) | **each formal parameter** |

Because the same routine resolves all four, they accept the same grammar. `parse_lvalue` (via [`parse_var_ref`](address:95C9@2?hex), `&95C9`) recognises:

- a named scalar — `A`, `count%`, `name$`;
- an array element — `a(3)`, `n$(i,j)`;
- a leading indirection — `?addr` (byte), `!addr` (word), `$addr` (string);
- a trailing indirection — `base?n`, `base!n`.

For each it returns the storage address in [`zp_iwa`](address:002a@2?hex) (`&2A/&2B`) and a **type byte** in [`zp_iwa_2`](address:002c@2?hex) (`&2C`):

| Type | Meaning | Width / form |
|---|---|---|
| `&00` | `?` byte indirection | 1 byte |
| `&04` | integer variable, or `!` word indirection | 4 bytes |
| `&05` | real variable | 5-byte float |
| `&80` | `$` indirection (string at a raw address) | bytes + `&0D` terminator |
| `&81` | string variable / string array element | heap descriptor |

That table is the whole story. The parameter binder does not know or care which of these it is holding until it is time to store the argument — at which point it branches on bit 7 (string vs numeric) and on the width.


## What "binding to an lvalue parameter" actually does

The parameter binder lives inside [`call_proc_fn`](address:B197@2?hex) at `&B24D`. For each formal it performs three steps, in this order:

1. **Parse the formal as an lvalue** — `jsr parse_lvalue` (`&B256`). This yields the address and type byte above.
2. **Save the location's current contents** — `jsr` [`stack_local`](address:B30D@2?hex) (`&B276`), pushing a *(address, type, old value)* record onto the BASIC value stack. This is the *identical* call `LOCAL` makes; a parameter is a `LOCAL` that is about to be assigned. The "old value" is captured by type: 1 byte for `?`, 4 bytes for `!`, and — for a `$addr` target — the string currently at the address, read **up to and including the first `&0D`** (the `lsv_dollar` loop at `&B3A7`). A `$addr` save therefore depends on a terminator already being present; an uninitialised buffer is saved as whatever bytes precede the first stray `&0D`.
3. **Assign the actual argument into the location** — after a parameter/argument count check, the binder dispatches on the type byte:
   - bit 7 set (`&80`/`&81`, a string target) → [`assign_string_to`](address:8C21@2?hex) (`&B300`). For `$addr` (`&80`) this writes the string's bytes to the raw address followed by a `&0D` carriage-return terminator.
   - bit 7 clear (numeric) → [`assign_num_by_type`](address:B4B7@2?hex) (`&B2F3`), storing 1 byte for `?`, 4 bytes for `!`, or the value coerced to the variable's own type.

On `=expr` (for `FN`) or `ENDPROC` (for `PROC`), the frame unwinds back through `call_proc_fn` at `&B20E`, which replays the saved records — each *(address, old value)* pair restored via [`unstack_value_to_var`](address:8CC1@2?hex) (`&B21C`/`&B21F`). The location is returned to exactly what it held before the call.

The crucial consequence for anyone modelling this:

> An indirection parameter is **not** call-by-reference and **not** a named variable. It is a *scoped assignment to a fixed memory location*. `DEF FNf(?buf%)` called with value `V` behaves precisely like `LOCAL ?buf% : ?buf% = V` at entry and a restore of `?buf%` at exit. The address (`buf%` here) is named in the `DEF` line and evaluated afresh on each call; the body refers to the parameter not by a name but by *repeating the indirection*.

There is one guard worth knowing: the `$` lvalue path rejects an address whose high byte is zero (`address in zero page? → $ range error`, [`&95BF`](address:95BF@2?hex)), so `$0`–`$255` will not bind.


## A catalogue, with the smallest programs that show each

Each program is deliberately minimal. The pattern throughout: set a location to a "before" value, call a function whose *formal parameter is that location*, observe the argument inside the body, then observe the location restored after the call.

### 1. The ordinary case — a named scalar (for contrast)

```basic
   10 PRINT FNsquare(7)
   20 END
   30 DEF FNsquare(x) = x*x
```
```
49
```
`x` is type `&04` (it is created as a new integer `LOCAL`); the argument `7` is assigned to it. Nothing surprising — but it is the *same* machinery as everything below.

### 2. An array element — `a(i)` (the most familiar lvalue)

You do not need pointers to meet this feature. An array element is an assignable location like any other, so it too can be a formal parameter. This is the gentlest example: a three-element array, printed in full before, during, and after a call whose parameter *is* one of its elements.

```basic
   10 DIM a(2)
   20 FOR i%=0 TO 2 : a(i%)=10*(i%+1) : NEXT
   30 PRINT "before:";
   40 FOR i%=0 TO 2 : PRINT " ";STR$(a(i%)); : NEXT : PRINT
   50 dummy = FNpoke(99)
   60 PRINT "after: ";
   70 FOR i%=0 TO 2 : PRINT " ";STR$(a(i%)); : NEXT : PRINT
   80 END
   90 DEF FNpoke(a(1))
  100 PRINT "inside:";
  110 FOR i%=0 TO 2 : PRINT " ";STR$(a(i%)); : NEXT : PRINT
  120 = 0
```
```
before: 10 20 30
inside: 10 99 30
after:  10 20 30
```

The function's only formal parameter is `a(1)` — element one of the array. On the call the binder evaluates that subscript, stacks the element's current value (`20`), and assigns the argument `99` into it. The body's own `FOR` loop then walks the whole array and sees `10 99 30`: only the one element changed. On `=` the saved `20` is written back, so after the call the array reads `10 20 30` again. The element behaved exactly like a `LOCAL` for the duration of the call — which is the whole point, and needs no understanding of addresses at all.

A multidimensional element works just as well — `DEF FNpoke(m(1,1))` is a legal formal list. [`index_array`](address:96DF@2?hex) evaluates every comma-separated subscript and folds them (by Horner's method) into one flattened element address before the binder sees it, so a `2`-D element is indistinguishable from a `1`-D one at bind time. The usual rules apply at the call: the subscript count must match the array's declared rank (else *Array*) and each index must be in range (else *Subscript*).

### 3. A byte indirection — `?addr`

```basic
   10 DIM buf% 8
   20 ?buf% = 99
   30 dummy = FNbyte(65)
   40 PRINT "after  ?buf% = ";?buf%
   50 END
   60 DEF FNbyte(?buf%)
   70 PRINT "inside ?buf% = ";?buf%
   80 = ?buf%
```
```
inside ?buf% = 65
after  ?buf% = 99
```
The formal `?buf%` (type `&00`, width 1) names the single byte at `buf%`. On the call its old contents (`99`) are stacked, the argument `65` is poked in, the body reads it back through the same `?buf%`, and on `=` the byte is restored to `99`.

### 4. A word indirection — `!addr`

```basic
   10 DIM buf% 8
   20 !buf% = &12345678
   30 dummy = FNword(&AABBCCDD)
   40 PRINT "after  !buf% = ";~!buf%
   50 END
   60 DEF FNword(!buf%)
   70 PRINT "inside !buf% = ";~!buf%
   80 = 0
```
```
inside !buf% = AABBCCDD
after  !buf% = 12345678
```
Identical in spirit to the byte case, but the formal is type `&04` and four bytes are written and restored.

### 5. A string indirection — `$addr`

```basic
   10 DIM buf% 32
   20 $buf% = "hello"
   30 dummy = FNstr("WORLD")
   40 PRINT "after  = ";$buf%
   50 END
   60 DEF FNstr($buf%)
   70 PRINT "inside = ";$buf%
   80 PRINT "length = ";LEN $buf%
   90 = 0
```
```
inside = WORLD
length = 5
after  = hello
```
Here the formal `$buf%` is type `&80`. The argument string `"WORLD"` is written to the bytes at `buf%` with a trailing `&0D`; inside the body `$buf%` and `LEN $buf%` read those raw bytes; on return the original `"hello"` (and its terminator) are restored.

The array element of example 2 and the three indirections here are resolved by different helpers — [`index_array`](address:96DF@2?hex) for the subscript, the indirection dispatch in [`parse_lvalue`](address:9582@2?hex) for `?`/`!`/`$` — but they converge on the same `(address, type)` pair and travel through the identical save/assign/restore path. The rule really is general: it is not a special case bolted on for any one form.


## Is it a feature, or an artifact?

It is a **feature**, in the precise sense that it falls directly out of the interpreter's design rather than from a coincidence two routines happen to permit:

- The `DEF` line is never parsed at definition time — `DEF` shares the skip-to-end-of-line handler with `DATA`/`REM`/`ELSE`. The formal list is parsed lazily, at *call* time, by the binder.
- That binder reuses [`parse_lvalue`](address:9582@2?hex) verbatim. There is no separate, weaker "parameter parser" that an indirection sneaks through — it is the full assignment-target grammar.
- The binding (`stack_local` → assign → restore) is the same `LOCAL` machinery the language documents for ordinary locals.

So the capability is intentional in the way a great deal of BBC BASIC is intentional: by composing one general mechanism (lvalues) into several places (`LET`, `FOR`, `LOCAL`, parameters) rather than special-casing each. It was almost certainly never *documented* — no user-guide example passes a `$addr` as a parameter — but it is not a bug, and it is stable across the ROM's logic.

What makes it feel like a trick is the *use*, not the *mechanism*: passing a value into a fixed memory cell under cover of a parameter, then reading it back through indirection inside the body, is a way to smuggle data into a known buffer for the duration of a call. That is creative exploitation of an honest feature.


## Notes for a compiler (OWL and friends)

If byte-exact fidelity with corpus/Bot one-liners matters:

- **Accept the full lvalue grammar in formal lists** — named scalars, array elements, `?e`, `!e`, `$e`, and the trailing `e?n` / `e!n` forms — wherever you parse `DEF FN`/`DEF PROC` parameters.
- **Model an indirection formal as a scoped assignment, not a binding to a name.** `DEF FNf(?e)` ≡ "evaluate `e`, save the byte there, store the argument, run the body, restore the byte." There is no parameter *name*; the body reaches the value by re-evaluating the same indirection. The address `e` is taken from the `DEF` text and re-evaluated per call.
- **Respect the type/width split:** `?` → 1 byte, `!` → 4 bytes, `$` → bytes plus a `&0D` terminator; numeric formals reject string arguments and vice-versa (the ROM raises *Arguments* at [`&B2BE`](address:B2BE@2?hex)).
- **Restore on return** — the previous contents must come back on `=`/`ENDPROC`, including the original string's bytes and terminator for the `$` case. The save/restore is the same list `LOCAL` uses, replayed in `call_proc_fn`.
- You may reasonably *decline* the zero-page guard subtlety (`$` with a high address byte of `0` errors) only if you never need that exact error; otherwise it is part of the semantics.

The honest summary: this is a language feature a faithful compiler should support, not an interpreter-specific quirk it can wave away — but it is a feature you implement *for free* if your front end already treats parameters as lvalues the way the ROM does.


## Provenance

This analysis was prompted by a [rheolism](https://bbcmic.ro/) BBC Micro Bot one-liner whose function header reads `DEF FNd(X, $@%)` — a string-indirection parameter onto `@%`, the resident print-format integer at [`&0400`](address:0400@2?hex), used here purely as a pointer. The body then writes its string argument over whatever address `@%` holds and reads it back with `LEN $@%` and `@%?i`. It looked at first like an interpreter quirk worth distrusting; the disassembly shows it is the ordinary lvalue machinery above, with `@%` chosen as the buffer address. The mechanism is the same as the tame `$buf%` demos; only the choice of address is audacious.


## Cross-references

- [`parse_lvalue`](address:9582@2?hex) (`&9582`) — the shared assignment-target parser; the leading `!`/`$`/`?` dispatch lives at `&9595`–`&95BE`, with the `$ range` guard at [`&95BF`](address:95BF@2?hex).
- [`parse_var_ref`](address:95C9@2?hex) (`&95C9`) — scans names, arrays and indirections; sets the type byte (`&00`/`&04`/`&05`/`&80`/`&81`) in [`zp_iwa_2`](address:002c@2?hex).
- [`call_proc_fn`](address:B197@2?hex) (`&B197`) — the call mechanism; parameter binding at `&B24D`, the per-formal `parse_lvalue` at `&B256`, the string/numeric assign at `&B2F3`/`&B300`, and the restore replay at `&B21C`.
- [`stack_local`](address:B30D@2?hex) (`&B30D`) — stacks a location's old value for restore; shared by `LOCAL` and by each parameter.
- [`assign_string`](address:8C1E@2?hex) (`&8C1E`) / `assign_string_to` (`&8C21`) — the `$addr` CR-terminated write; [`iwa_store_var`](address:B4C6@2?hex) (`&B4C6`) — the `?`/`!`/integer write, width from the size byte.
- [`stmt_local`](address:9323@2?hex) (`&9323`) — confirms `LOCAL` uses the same `parse_lvalue`, so `LOCAL ?buf%` / `LOCAL $buf%` are equally legal.
- Related reading: [Control flow on five stacks](control-flow-stacks.md) for the call frame and the `LOCAL`/parameter restore list that this feature rides on.
