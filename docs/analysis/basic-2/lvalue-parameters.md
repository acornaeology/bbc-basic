# Arbitrary lvalues as formal PROC/FN parameters in BBC BASIC

> **Scope.** This article documents a little-known capability of BBC BASIC: that a formal parameter of a `DEF FN`/`DEF PROC` may be *any assignable location* – not just a named variable. The capability is present across the family: BASIC I, II and IV on the BBC Micro, and BASIC V on RISC OS. The code addresses, routine names and values below are read from our annotated disassembly of the **BASIC II** ROM. The *shape* of the behaviour is common to all these versions, but the *addresses* referred to here are for BASIC II only.

## Prelude: A review of formal parameters

In the common case, a formal procedure or function parameter is a just the name. Most BBC BASIC programmers have a clear mental model of what that means: the name introduces a **new variable, local to the PROC or FN**. It may share its name with a global, but the two behave as different variables. To the rest of the program the global keeps whatever value it had. The BBC Microcomputer User Guide states it plainly: *"All formal parameters are local to the procedure … their value is not known to the rest of the program."* This is ordinary pass-by-value:

```basic
   10 count = 10
   20 PROCshow(99)
   30 PRINT "after:  ";count
   40 END
   50 :
   60 DEF PROCshow(count)
   70   PRINT "inside: ";count
   80 ENDPROC
```
```
inside: 99
after:  10
```

So far as the programmer is concerned there are two separate variables named `count`: the global holding `10`, and a procedure-local one that `PROCshow` receives as `99`. The body sees the local; the global keeps its `10`, so line 30 prints `10`. Nothing here would surprise anyone who has written BBC BASIC programs.

However, a surprise lies in wait.

## A formal parameter can be *any* lvalue

First, what is an *lvalue*?

The simplest place an *lvalue* shows up is the value that occurs on the left-hand side (hence the 'L' in *lvalue*) of an assignment:

```basic
LET x = 123.4
```

or, in BBC BASIC, where we're allowed to drop the `LET`, simply,

```basic
x = 123.4
```

which is equivalent.

In these two examples, the variable `x` is the *lvalue*. In BASIC variables are created on first use, but in general assignment modifies the content of the *lvalue*. We can see this more generally, by using an array element, which can also serve as an *lvalue*,

```basic
DIM A$(3)
A$(0) = "Acorn"
```

where the zeroth element of the `A$()` array is the *lvalue*.

There are other expressions which can be used as *lvalues*, including those that involve the unary indirection operators:

```basic
M = &2000
?M = 42
!M = &12345678
$M = "ABCDEF"
```

There are four *lvalues* here. `M` is an ordinary variable, but `?M`, `!M` and `$M` are unary indirection values which cause writes of a byte, word and string respectively to the memory at address &2000.

Similarly, the two dyadic indirection operators can also be used as *lvalues*:

```basic
DIM buffer% 1024
buffer%?0 = 42
buffer%!1 = &87654321
```

where `buffer%?0` and `buffer%!1` are the *lvalues*.

Such *lvalues* show up in a few other places in BBC BASIC, notably in FOR-loop counter variables:

```basic
FOR i% = 0 TO 3
  PRINT i%
NEXT i%
```

where the first occurrence of i% here is an *lvalue*.

This *lvalue* placement shows similar flexibility, so array elements can be used as loop counters,

```basic
DIM counters%(3)
FOR counters%(0) = 0 TO 2
  FOR counters%(1) = 0 TO 2
    FOR counters%(2) = 0 TO 2
      PRINT counters%(0), counters%(1), counters%(2)
    NEXT counters%(2)
  NEXT counters%(1)
NEXT counters%(0)
```

and a little experimentation will demonstrate that the various forms of indirection operator *lvalues* can also be used as for-loop counters.

So much for *lvalues*. How do they relate to procedures and functions? A procedure's formal parameters are *lvalues* too. Take a definition like:

```basic
DEF PROCreticulate_splines(a, b, c, d)
   ...
ENDPROC
```

Here `a`, `b`, `c` and `d` are the *formal parameters*. Because they are *lvalues*, they are the targets of assignment: on entry, each *actual parameter* is assigned to the formal parameter in the corresponding position, as in:

```basic
PROCreticulate_splines(32.2, 67.1, 12.6, 55.82)
```

This effectively performs `a = 32.2`, `b = 67.1`, `c = 12.6` and `d = 55.82` where `a`, `b`, `c` and `d` are new variables local to the procedure.

What *is* surprising is as the formal parameters in BBC BASIC are *lvalues*, they can be *any* legitimate *lvalue*! Consider:

```basic
DEF PROCfrobnicate(a(3))
   ...
ENDPROC
```

What does this odd-looking syntax mean?! Remarkably, this legal construct means, "Use the named location as the storage for the procedure parameter, stack its value on entry, and restore its value on exit."

In fact, it's not a special syntax at all - it's just `lvalue` syntax - and a quirk of using the very same code to process the formal parameters of procedures as is used for assignment statements and FOR-loop counters.

So this is entirely legal:

```basic
   10 DIM words$(3)
   20 words$(0) = "The"
   30 words$(1) = "North"
   40 words$(2) = "Pole"
   50 PROCprint_words("Before")
   60 PROCscoped_edit("South")
   70 PROCprint_words("After")
   80 END
   90 :
  100 DEF PROCscoped_edit(words$(1))   : REM formal parameter is an array element!
  110   PROCprint_words("During")
  120 ENDPROC
  130 :
  140 DEF PROCprint_words(prefix$)
  150   PRINT prefix$,":";
  160   FOR i% = 0 TO 2
  170     PRINT " ";words$(i%);
  180   NEXT i%
  190   PRINT
  200 ENDPROC
```
```
Before    : The North Pole
During    : The South Pole
After     : The North Pole
```

The formal parameter of `PROCscoped_edit` is not a new variable; it is `words$(1)`, element one of an array that already exists. Calling `PROCscoped_edit("South")` assigns `"South"` into that element **for the duration of the call**. Then `PROCprint_words` walks the whole array and prints `The South Pole` with only the middle element changed. Once the call returns, the array element is restored to its original `"North"` again, so the final line prints `The North Pole`. The element behaves just as a local variable would — it carries the argument for the length of the call and is left as it was before — even though nothing here is a *name*, only an existing location.

This is not a trick; it is just how BBC BASIC works. The mechanics are spelt out [below](#what-binding-to-an-lvalue-parameter-actually-does).


## Why it works: one lvalue parser, used everywhere

BBC BASIC has a single routine for "parse a thing that can be assigned to": [`parse_lvalue`](address:9582@2?hex). It is, in fact, shared by four callers:

| Caller                  | Site                                                    | What it parses             |
|-------------------------|---------------------------------------------------------|----------------------------|
| `LET` / implied `LET`   | [`stmt_let`](address:8BE4@2?hex)                        | the target of `var = expr` |
| `FOR`                   | [`stmt_for`](address:B7C4@2?hex)                        | the loop control variable  |
| `LOCAL`                 | [`stmt_local`](address:9323@2?hex) (`jsr` at `&9328`)   | each localised variable    |
| **`PROC`/`FN` binding** | [`call_proc_fn`](address:B197@2?hex) (`jsr` at `&B256`) | **each formal parameter**  |

Because the same routine resolves all four, they accept the same grammar. `parse_lvalue` (via [`parse_var_ref`](address:95C9@2?hex), `&95C9`) recognises:

- a named scalar — `A`, `count%`, `name$`;
- an array element — `a(3)`, `n$(i,j)`;
- a unary indirection — `?addr` (byte), `!addr` (word), `$addr` (string);
- a dyadic indirection — `base?n`, `base!n`.

For each it returns the storage address in [`zp_iwa`](address:002a@2) (`&2A/&2B`) and a **type code byte** in [`zp_iwa_2`](address:002c@2?hex):

| Type  | Meaning                                   | Width / form             |
|-------|-------------------------------------------|--------------------------|
| `&00` | `?` byte indirection                      | 1 byte                   |
| `&04` | integer variable, or `!` word indirection | 4 bytes                  |
| `&05` | real variable                             | 5-byte float             |
| `&80` | `$` indirection (string at a raw address) | bytes + `&0D` terminator |
| `&81` | string variable / string array element    | heap descriptor          |

The parameter binder does not know or care which of these it is holding until it is time to store the argument, at which point it branches on bit 7 (string vs numeric) and on the width.


## What "binding to an lvalue parameter" actually does

The parameter binder lives inside [`call_proc_fn`](address:B197@2?hex) at `&B24D`. For each formal parameter it performs three steps, in this order:

1. **Parse the formal as an lvalue** — `jsr parse_lvalue` (`&B256`). This yields the address and type byte above. Nothing has looked at the formal parameter list before this moment: `DEF` is never parsed at definition time, sharing the skip-to-end-of-line handler with `DATA`/`REM`/`ELSE`, so the list is parsed lazily, at *call* time, by the binder.
2. **Save the location's current contents** — `jsr` [`stack_local`](address:B30D@2?hex) (at `&B276`), pushing a *(address, type, old value)* record onto the BASIC value stack. The "old value" is captured by type: 1 byte for `?`, 4 bytes for `!`, and — for a `$addr` target — the string currently at the address, scanned for a terminating `&0D` (the `lsv_dollar` loop at `&B3A7`). That scan is bounded by the 8-bit index it uses: at most 256 bytes are copied from the address into the string work area at `&0600`, and if no `&0D` turns up within them the recorded length is `0` and the saved string is simply empty (`&B3B9`). The bound is on the count, not on the address, so the scan crosses page boundaries freely. The terminator is not counted in the length; the restore path appends a fresh `&0D` of its own ([`unstack_value_to_var`](address:8CC1@2?hex), `&8CFF`). A `$addr` save therefore depends on a terminator already being present within 256 bytes; an uninitialised buffer is saved as whatever bytes precede the first stray `&0D`, and a buffer with no `&0D` at all is saved as nothing.
3. **Assign the actual argument into the location** — after a parameter/argument count and type check (a numeric formal given a string argument, or the reverse, raises *Arguments* at `&B2BE`), the binder dispatches on the type byte:
   - bit 7 set (`&80`/`&81`, a string target) → [`assign_string_to`](address:8C21@2?hex) (`jsr` at `&B300`). For `$addr` (`&80`) this writes the string's bytes to the raw address followed by a `&0D` carriage-return terminator.
   - bit 7 clear (numeric) → [`assign_num_by_type`](address:B4B7@2?hex) (`jsr` at `&B2F3`), storing 1 byte for `?`, 4 bytes for `!`, or the value coerced to the variable's own type.

On `ENDPROC` (or `=expr` for `FN`), the frame unwinds back through `call_proc_fn` at `&B20E`, which replays the saved records — each *(address, old value)* pair restored via [`unstack_value_to_var`](address:8CC1@2?hex) (`&B21C`/`&B21F`). The location is returned to exactly what it held before the call.

There is one guard worth knowing about: the `$` lvalue path rejects an address whose high byte is zero, so the zero-page addresses `$0`–`$255` will not bind and give `$ range error` if an attempt is made to use them.


## "Local" means saved and restored, not created and destroyed

Reading those three steps again — save the location's value, overwrite it, write the saved value back — and the widely held conception of a local variable or parameter as a new location separate from any existing global with the same name falls apart. BBC BASIC does not make a fresh variable that lives for the call and is destroyed at `ENDPROC`. It takes a location that already exists, remembers what it holds, lends it to the call, and puts the remembered value back on return. Whether the formal parameter is a variable name or an indirection expression doesn't make any difference. The familiar idea of a parameter as a "new local variable" is at variance with what the code actually does. Two cases show how far apart they are.

**A formal parameter whose name is already in use as a global reuses that variable's own storage.** What looks like a separate local was the global location itself, with its value saved and restored back after the call.

**A formal parameter whose name *is* new creates a variable that then outlives the call.** When the parameter name has never been seen, `parse_lvalue` creates it — a permanent entry in BASIC's variable chain, linked in by [`create_variable`](address:94FC@2?hex), and clears it to zero *before* the binder runs. The saved "previous value" is therefore that zero; the argument is assigned; and on `ENDPROC` the zero is written back. BBC BASIC has no routine to unlink a single variable, so the entry stays. The parameter survives the call, holding `0`:

```basic
   10 PROCdo(5)
   20 PRINT "After  : ";x
   30 END
   40 :
   50 DEF PROCdo(x)
   60  PRINT "During : ";x
   70 ENDPROC
```
```
During : 5
After  : 0
```

`x` did not exist before line 10. Inside `PROCdo` it holds the argument `5`. After `ENDPROC` it is still a variable named `x` — now holding the `0` it was cleared to at creation, not the *No such variable* error an unknown variable would cause. The parameter was not destroyed at the end of the call; it was restored to zero.

Binding a parameter is *save, assign, restore* on whatever location the formal names; the location's nature does not matter: a variable's slot, an array element, or a raw byte, word or string behind `?`, `!` or `$` all travel the same path. The everyday case of a named parameter variable is not the simple one with the exotic forms bolted on - it's the same save-and-restore, applied to a variable's storage rather than to memory addressed directly. Where a name would identify the parameter, an indirection or array element has none, so inside the body it is reached only by repeating the same *lvalue* — `?buf%`, `words$(1)` — again. The programmer's conception of a "new local variable" is a convenient story, but is at odds with the implementation.


## Some small programs which show various forms

Each program is deliberately minimal. The pattern throughout: set a location to a "before" value, call a procedure whose *formal parameter is that location*, observe the argument inside the body, then observe the location restored after the call.

### 1. The ordinary case — a named scalar (for contrast)

```basic
   10 PROCsquare(7)
   20 END
   30 :
   40 DEF PROCsquare(x)
   50 PRINT "x*x = ";x*x
   60 ENDPROC
```
```
x*x = 49
```
`x` is type `&05` — a real variable created fresh and cleared to zero before the argument `7` is assigned to it. Nothing surprising — but it is the *same* machinery as everything below, and as we showed above `x` will persist beyond the call.

### 2. A multidimensional array element — `m(i,j)`

The array element in the opening example was one-dimensional. A multidimensional element works just as well:

```basic
   10 DIM m(2,2)
   20 m(1,1) = 55
   30 PRINT "Before : ";m(1,1)
   40 PROCcentre(99)
   50 PRINT "After  : ";m(1,1)
   60 END
   70 :
   80 DEF PROCcentre(m(1,1))
   90 PRINT "During : ";m(1,1)
  100 ENDPROC
```
```
Before : 55
During : 99
After  : 55
```
[`index_array`](address:96DF@2?hex) evaluates every comma-separated subscript and folds them into one flattened element address before the binder sees it, so a `2`-D element is indistinguishable from a `1`-D one at bind time. The usual rules apply at the call: the subscript count must match the array's declared rank (else *Array*) and each index must be in range (else *Subscript*).

### 3. A unary byte indirection — `?addr`

```basic
   10 DIM buf% 8
   20 ?buf% = 99
   30 PRINT "Before : ";?buf%
   40 PROCbyte(65)
   50 PRINT "After  : ";?buf%
   60 END
   70 :
   80 DEF PROCbyte(?buf%)
   90 PRINT "During : ";?buf%
  100 ENDPROC
```
```
Before : 99
During : 65
After  : 99
```
The formal parameter `?buf%` (type `&00`, width 1) names the single byte at `buf%`. On the call its old contents (`99`) are stacked and the argument `65` is poked in, so the body reads `65` back through the same `?buf%`; on `ENDPROC` the byte is restored to `99`.

### 4. A dyadic word indirection — `base!n`

```basic
   10 DIM buf% 8
   20 buf%!4 = &12345678
   30 PRINT "Before : ";~buf%!4
   40 PROCword(&AABBCCDD)
   50 PRINT "After  : ";~buf%!4
   60 END
   70 :
   80 DEF PROCword(buf%!4)
   90 PRINT "During : ";~buf%!4
  100 ENDPROC
```
```
Before : 12345678
During : AABBCCDD
After  : 12345678
```
The formal `buf%!4` is the *dyadic* form — base `buf%` plus offset `4` — naming the four bytes at `buf%+4`. It is type `&04`, so four bytes are stacked, overwritten and restored. To the binder this is no different from a unary indirection: `parse_lvalue` reduces both forms to the same `(address, type)` pair, and everything downstream sees only that.

### 5. A unary string indirection — `$addr`

```basic
   10 DIM slogan% 26
   20 $slogan% = "To be this good takes AGES"
   30 PRINT "Before : ";$slogan%
   40 PROCedit("SEGA")
   50 PRINT "After  : ";$slogan%
   60 END
   70 :
   80 DEF PROCedit($(slogan%+22))
   90 PRINT "During : ";$slogan%
  100 ENDPROC
```
```
Before : To be this good takes AGES
During : To be this good takes SEGA
After  : To be this good takes AGES
```
The formal `$(slogan%+22)` is type `&80`: the string at address `slogan%+22`, which is the `"AGES"` at the tail of the buffer — offset 22 is the byte just past `"To be this good takes "`. On the call the binder saves that string (the bytes from `slogan%+22` up to the first `&0D`), then writes the argument `"SEGA"` there with its own `&0D` terminator. The body, reading the whole buffer through `$slogan%`, sees `"To be this good takes SEGA"`; on `ENDPROC` the saved `"AGES"` is written back. The address is an ordinary expression evaluated afresh at call time, so a `$` parameter can name any string in memory, not only the start of a buffer. The `"AGES"` here is safely terminated; a buffer with no `&0D` in its first 256 bytes saves as empty, and the restore then leaves only a bare terminator where the old contents were.

The array element of example 2 and the three indirections here are resolved by different helpers — [`index_array`](address:96DF@2?hex) for the subscript, the indirection dispatch in [`parse_lvalue`](address:9582@2?hex) for `?`/`!`/`$` — but they converge on the same `(address, type)` pair and travel through the identical save/assign/restore path. The rule really is general: it is not a special case bolted on for any one form.


## `LOCAL` uses the same mechanism

Though there's no mention of it in the BBC Microcomputer User Guide, the `LOCAL` statement behaves the same way. The guide says,

> This informs the computer that the named variables are “local”
> to the procedure or function in which they occur; their use in
> this procedure or function in no way affects their value outside
> it.
>
> LOCAL saves the values of the external
> variables named and restores these original values when the
> function or procedure is completed.

and moreover, the grammar presented in the manual gives the impression that the list introduced by the `LOCAL` keyword is for variables only:

> Syntax
> `LOCAL <string-var>|<num-var>{,<string-var>|<num-var>}`

This undersells the capabilities of `LOCAL`. In fact, it can be used to stack *any lvalue*. For example, let's use it to stack and restore a byte in a global byte-array:

```basic
10 DIM data% 10
20 data%?3 = 19
30 PRINT "Before PROC   : ";data%?3
40 PROCfoo
50 PRINT "After PROC    : ";data%?3
60 END
70 :
80 DEF PROCfoo
90 PRINT "Inside PROC   : ";data%?3
100 LOCAL data%?3
110 PRINT "After LOCAL   : ";data%?3
120 data%?3 = 77
130 PRINT "After assign  : ";data%?3
140 ENDPROC
```

when RUN,

```
Before PROC   : 19
Inside PROC   : 19
After LOCAL   : 0
After assign  : 77
After PROC    : 19
```

We see that `LOCAL` sets the existing value to zero, though it has also stacked the previous value, 19. Then we reassign inside the procedure to the value 77. On exit, the value of the byte is restored to 19.

In detail, the `LOCAL` statement ([`stmt_local`](address:9323@2?hex)) parses its variable with the same `parse_lvalue` and saves it with the same `stack_local`; it then assigns zero (`&933E`) where the parameter binder assigns the argument. A formal parameter is precisely a `LOCAL` whose initial value is the argument instead of `0`. Everything shown here therefore holds for `LOCAL` too: `LOCAL` on an existing name saves and restores that variable's own cell, and `LOCAL fresh` on an unused name leaves `fresh` defined and zero after the procedure returns — for the same reason `PROCdo`'s `x` did. The same assignment-target grammar is open to it, so an indirection or array element is as valid after `LOCAL` as it is in a parameter list.

So, in mild contradiction to the user guide's claim that,

> "...the named variables are “local”
> to the procedure or function in which they occur; their use in
> this procedure or function in no way affects their value outside
> it."

the `LOCAL` statement is quite capable of creating a global variable that otherwise would not exist:

```basic
10 PROCmake_global
20 PRINT x
30 END
40 :
50 DEF PROCmake_global
60 LOCAL x
70 ENDPROC
```

which duly creates the global variable `x` and initialises it to zero:

```
>RUN
         0
>
```


## Examples in the wild

This unusual feature isn't completely unknown or indeed completely unused, but across nearly 5000 BBC BASIC programs collected from *The Micro User*, *Acorn User* and *A & B Computing* at [8bs.com](https://8bs.com), a single idiom dominates: an `OSCLI` implementation portable across BASIC I and BASIC II. Here it is written out in long form as most corpus examples are somewhat more condensed:

```basic
   10 PROCoscli("SAVE SCREEN 3000 +5000")
   20 END
   30 :
   40 DEF PROCoscli($&700)
   50   LOCAL X%, Y%
   60   X% = &700 MOD 256
   70   Y% = &700 DIV 256
   80   CALL &FFF7
   90 ENDPROC
```

What each part does:

- Line 40 — the formal parameter is `$&700`, the string at address `&700`. Binding the argument to it writes the command text into BASIC's line input buffer and appends the `&0D` terminator that `OSCLI` requires. There is no assignment statement anywhere; the parameter binding is the copy.
- Line 50 — `X%` and `Y%` are resident integers at `&0460`/`&0464`, shared with the rest of the program. `LOCAL` saves and restores them, so the wrapper doesn't trample a caller's loop counter.
- Lines 60–70 — `OSCLI` wants the buffer address split across two registers, low byte in X and high byte in Y. `&700 MOD 256` is 0 and `&700 DIV 256` is 7.
- Line 80 — `CALL` loads the 6502 registers from `A%`, `X%` and `Y%` before entering the routine, so `CALL &FFF7` arrives at `OSCLI` with the pointer already in place.

On `ENDPROC` the binder writes the buffer's previous contents back to `&700`, and `LOCAL` restores `X%` and `Y%`.

Two things worth writing out explicitly, since the compressed one-liners in the corpus hide them:

The corpus versions almost all write `LOCAL X%, Y%` and then set only `Y% = 7`, never `X%`. That works because `LOCAL` zeroes what it localises, and `&700 MOD 256` happens to be zero — the low byte arrives correctly by way of `LOCAL`'s initialisation rather than by assignment. Lines 60–70 above say it out loud instead of relying on the coincidence.

And this is BASIC I-era code. BASIC II has an `OSCLI` keyword, so the whole procedure collapses to:

```basic
   10 OSCLI "SAVE SCREEN 3000 +5000"
```

which passes the string through `&0600`, the string work area, and never touches `&700`. The wrapper survived in listings for another decade regardless.

Evidently, this wrapper and minor variants of it became routinely copied into new programs when the capability of calling OS CLI commands was required, probably without most program authors pausing to consider how the code worked.

Setting aside that widely propagated wrapper, 58 distinct listings across 4995 programs (1.2%) exercise the capability for something else, and about 22 of those are unique one-offs. The rest are house routines from *Acorn User*, or from frequent authors, such as `DEFPROCprop($ms%)`, a proportional-text printing routine.


### `LOCAL` for stacking lvalues

BBC BASIC programmers evidently took the User Guide at its word, because across the nearly 5000 program corpus there are zero examples of using `LOCAL` to stack and restore anything other than a regular variable.


## Is it a deliberate feature, or an emergent consequence of the implementation?

It seems unlikely that every program behaviour afforded by the implementation was a deliberate goal of it, but equally unlikely that the implementers remained unaware of the capabilities of what they had made. Either way, those capabilities were never publicised in official documentation, and consequently very few programs make use of them.

One imagines that Wilson made the implementation work this way to prioritise concision, efficiency and code-sharing, rather than to deliberately allow these somewhat exotic and unconventional constructs.