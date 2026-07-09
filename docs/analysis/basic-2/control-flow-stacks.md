# Control flow on five stacks: loops, procedures, and early exits in BBC BASIC II

> **Scope.** This article describes **BBC BASIC II** — the 16 KB language ROM of the BBC Micro. The mechanism, the workspace addresses, and the ROM entry points are all specific to this version. BASIC IV (the BBC Master) keeps the same architecture but relocates the addresses; BASIC V (Acorn Archimedes) is a 32-bit ARM interpreter and works differently again. Treat the *shape* of the argument as portable and the *addresses* as version II only.

BBC BASIC is justly admired for its structured-programming constructs — named `PROC`s and `FN`s with `LOCAL` variables, `REPEAT…UNTIL`, `FOR…NEXT`, and `GOSUB…RETURN`. Underneath, every one of these rests on a stack. But not the *same* stack: the interpreter maintains **five** distinct ones, and which construct uses which is the key to understanding why some control-flow tricks are clean and others quietly corrupt the interpreter's state.

The single most useful fact, derived directly from the ROM, is this:

> A `PROC`/`FN` call saves and restores the 6502 hardware stack and the BASIC value stack. It does **not** save the `FOR`, `REPEAT` or `GOSUB` stacks. So leaving a loop early — whether by `GOTO` or by `ENDPROC` from inside it — leaks that loop's frame.


## The five stacks

| Stack | Where | Frame | Counter | Capacity | Used by |
|---|---|---|---|---|---|
| 6502 hardware stack | page 1, `&0100–01FF` | 2 bytes (return addr) | the 6502 `S` register | 256 bytes | interpreter `JSR` nesting; nested `PROC`/`FN` call context |
| BASIC value stack | descends from `HIMEM`, ptr at [`zp_stack_ptr`](address:0004@2) (`&04/05`) | varies | the pointer itself | down to the top of variables | expression temporaries, stacked strings, the saved copy of the 6502 stack during a call, and the per-call `LOCAL`/parameter restore list |
| `FOR` stack | [`for_stack`](address:0500@2?hex) | 15 bytes | [`zp_for_level`](address:0026@2?hex) | 10 nested | `FOR`/`NEXT` |
| `REPEAT` stack | [`repeat_stack`](address:05A4@2) (`&05A4`/`&05B8`) | 2 bytes | [`zp_repeat_level`](address:0024@2?hex) | 20 nested | `REPEAT`/`UNTIL` |
| `GOSUB` stack | [`gosub_stack`](address:05CC@2) (`&05CC`/`&05E6`) | 2 bytes | [`zp_gosub_level`](address:0025@2?hex) | 26 nested | `GOSUB`/`RETURN` |

The three loop stacks live side by side in page 5 and are plain LIFO arrays indexed by a one-byte counter each. They are completely independent of one another and of the two general-purpose stacks above them. The capacities are baked into the push routines as literal comparisons — e.g. `REPEAT` checks `CPX #&14` (20) and raises *Too many REPEATs* if the stack is full.


## How each construct uses its stack

**`FOR`/`NEXT`.** [`stmt_for`](address:B7C4@2?hex) builds a 15-byte control frame holding the loop variable's address, the limit, the `STEP`, and the loop-body text pointer, then bumps `zp_for_level` by 15. `NEXT` ([`stmt_next`](address:B695@2?hex)) reads the top frame, updates the variable, and either jumps back to the body or — when the limit is passed — drops the frame by decrementing the level.

**`REPEAT`/`UNTIL`.** [`stmt_repeat`](address:BBE4@2?hex) is the simplest of all: it pushes just the loop-start text pointer into `repeat_stack[level]` and does `INC zp_repeat_level`. [`stmt_until`](address:BBB1@2?hex) evaluates the condition; if false it reloads the saved pointer from the top frame and jumps back; if true it does `DEC zp_repeat_level` and falls through. Note that `REPEAT` stores nothing about the *condition* — that lives only in the `UNTIL` line — which is why the loop is genuinely a "repeat the body, then test" construct.

**`GOSUB`/`RETURN`.** [`stmt_gosub`](address:B888@2?hex) pushes the return text pointer into `gosub_stack[level]` and increments `zp_gosub_level`; [`stmt_return`](address:B8B6@2?hex) pops it. Straightforward.

**`PROC`/`FN`.** This is the interesting one, and the exception.


## The PROC/FN exception

When you call `PROCfoo`, [`call_proc_fn`](address:B197@2?hex) does something none of the loop constructs do — it manipulates the **6502 hardware stack**:

```
    TSX                       ; how much hardware stack is in use?
    TXA : CLC : ADC &04 ...    ; reserve that many bytes on the value stack
    ... copy &0100..&01FF onto the value stack ...
    TXS                       ; then EMPTY the hardware stack
    LDA token : PHA           ; push the PROC/FN token (lands at &01FF)
    ... push the caller's text pointers ...
    JSR <body>                ; run the procedure body
```

It snapshots the entire live hardware stack onto the BASIC value stack, then resets the hardware stack to empty before pushing a fresh call frame. This is what lets `PROC`s and `FN`s recurse far beyond the 256-byte limit of the 6502 stack — each level parks the previous level's hardware stack in the (much larger) value stack.

### The call frame

Because the hardware stack was just emptied, the new frame is built from the top of page 1 downwards, at fixed, known addresses. During the body it is ten bytes:

| Addr | Byte | Source |
|---|---|---|
| `&01FF` | `PROC` token `&F2` / `FN` `&A4` | [`zp_var_type`](address:0027@2?hex) |
| `&01FE` | caller text offset (PtrA) | [`zp_text_ptr_off`](address:000a@2?hex) |
| `&01FD` | caller text pointer low | `&0B` |
| `&01FC` | caller text pointer high | `&0C` |
| `&01FB` | `LOCAL`/parameter count | — |
| `&01FA` | PtrB offset | `&1B` |
| `&01F9` | PtrB low | `&19` |
| `&01F8` | PtrB high | `&1A` |
| `&01F7` | body return address high | `JSR <body>` |
| `&01F6` | body return address low | `JSR <body>` |

The addresses are absolute, not relative, precisely *because* the stack was emptied first — which is how two routines reach into the frame by hard-coded address. `ENDPROC` reads the framed token at `hw_stack_top` (`&01FF`) to confirm it really is inside a `PROC`, and [`stmt_local`](address:9323@2?hex) bumps the count through `frame_local_count` (`&0106,X`, which with the body's `S` = `&F5` resolves to `&01FB`). Both sit inside the 6502 hardware-stack page ([`hw_stack`](address:0100@2?hex), `&0100`).

### What rides on the value stack

Two things sit on the BASIC value stack across the call, beneath that frame:

- **the caller's entire hardware stack** — the snapshot taken on entry (the saved `S`, then every byte up to `&01FF`), copied back on return; and
- **the `LOCAL`/parameter restore list** — one *(variable address, saved value)* pair for every `LOCAL` variable and every formal parameter. [`stmt_local`](address:9323@2?hex) stacks a pair and bumps the frame's count byte; each parameter does the same as it is bound. The count at `&01FB` is simply how many pairs there are to replay.

### Unwinding

`ENDPROC` ([`stmt_endproc`](address:9356@2?hex)) and `FN`'s `=expr` do **not** pop the frame themselves — and that is the elegant part. Each verifies the framed token, then falls into the ordinary end-of-statement path. Because the body was entered by `JSR <body>`, the `RTS` ending that path pops the body return address (`&01F6/&01F7`) straight back into `call_proc_fn` (at `&B20E`). Only there does the real unwind happen: restore PtrB, replay the count by popping that many *(address, value)* pairs off the value stack to undo the `LOCAL`s and parameters, restore the caller's PtrA, then copy the saved hardware stack back into page 1 and fix up the value-stack pointer.

So `PROC`/`FN`/`ENDPROC` correctly tidy **two** stacks: the 6502 hardware stack and the BASIC value stack. The catch is in what they leave alone. Searching the ROM for every write to the three loop-level counters turns up exactly five sites — the loop statements themselves, plus one bulk reset — and **none of them is in `call_proc_fn` or `stmt_endproc`**. The loop stacks are global state that a procedure call neither saves nor restores.


## Legitimate control flow

The clean idioms are the ones where every push is matched by its own pop, on the same stack:

- `FOR i=…` … `NEXT i` — `stmt_for` pushes, `stmt_next` pops.
- `REPEAT` … `UNTIL c` — `stmt_repeat` pushes, `stmt_until` pops.
- `GOSUB n` … `RETURN` — `stmt_gosub` pushes, `stmt_return` pops.
- `DEFPROC` … `ENDPROC` (with no loop left open across the boundary) — `call_proc_fn` pushes a frame and saves the two general stacks, `stmt_endproc` returns and restores them.

Nesting these properly is fine to the documented depths (10 `FOR`s, 20 `REPEAT`s, 26 `GOSUB`s), because every level is balanced.


## Illegitimate control flow

The trouble starts whenever control leaves a construct by a path other than its matching terminator.

**Early exit from a loop (`GOTO` out).** Jumping out of a `FOR` or `REPEAT` with `GOTO` skips the `NEXT`/`UNTIL` that would have popped the frame. The counter is never decremented, so the frame leaks. Do it in a loop yourself and you march the counter up to its ceiling — *Too many FORs* / *Too many REPEATs*. This is the classic BBC BASIC wart, and it is a direct consequence of the loop stacks being separate, un-unwound arrays.

**Early exit from a procedure (`ENDPROC`).** By itself this is clean — `ENDPROC` is *designed* to be reached from anywhere in the body, and it restores both general-purpose stacks. A procedure with a guard clause that `ENDPROC`s near the top is perfectly well-formed:

```basic
1000 DEFPROCdraw(n%)
1010 IF n%=0 THEN ENDPROC     : REM nothing to draw — fine
1020 ...
1990 ENDPROC
```

**Early exit from a procedure *within a loop*.** This is where the two ideas collide, and it is the case worth understanding. Consider:

```basic
  10 REPEAT
  20   PROCfoo
  30 UNTIL done%
  ...
 100 DEFPROCfoo
 110 REPEAT
 120   IF bail% THEN ENDPROC   : REM early exit, still inside the inner REPEAT
 130 UNTIL inner%
 140 ENDPROC
```

When `PROCfoo` reaches the `ENDPROC` at line 120:

- The hardware stack and value stack are restored correctly, so the *return itself works* — no crash.
- But the inner `REPEAT` (line 110) pushed a frame and did `INC zp_repeat_level`, and nothing decremented it. `zp_repeat_level` comes back to line 30 **one too high**, with a dead frame — pointing at line 110 — sitting on top of the outer loop's frame.

Now the outer `UNTIL` at line 30 reads the *top* frame, which is the leaked inner one. Two failure modes follow:

1. **Enclosing-loop corruption.** If `done%` is still false, the outer `UNTIL` jumps back to line 110 — into the middle of a procedure that has already exited — instead of to line 10. The outer loop is now broken.
2. **Leak accumulation.** Even when the immediate jump happens to land somewhere survivable, the level counter is permanently skewed. Repeat the pattern enough times without clearing it and you hit *Too many REPEATs*.

The same reasoning applies to a `FOR` loop left open across an `ENDPROC`, with *Too many FORs* as the eventual symptom.


## Why casual misuse often seems to work

There is one more piece that explains why programmers got away with this more often than the analysis suggests they should have. The routine [`reset_data_and_stacks`](address:BD3A@2?hex) resets the value stack to `HIMEM`, the `DATA` pointer to `PAGE`, and **zeroes all three loop-level counters**. It runs whenever control returns to the immediate-mode prompt (from [`execute_line`](address:8B1A@2?hex)) and on `RUN`.

So a leaked frame from a single ill-advised `ENDPROC` is wiped the moment you get back to the `>` prompt. A program that early-exits a loop once, returns to the prompt, and is re-`RUN` will look perfectly healthy. The leak only bites when it *accumulates within a single run* — many early exits without passing through the prompt — or when a leaked inner frame sits on top of a live **outer** loop, as in the example above. Both are real; both are easy to trigger by accident; neither is reported as an error until the ceiling is hit.


## Practical guidance

- `ENDPROC` is a legitimate early-exit *from a procedure* — use it freely, including from guard clauses — **provided no `FOR` or `REPEAT` is open at the point you exit**.
- To exit a `REPEAT` early, fold the early-exit condition into the `UNTIL` so the loop terminates through its own pop:
  ```basic
  110 REPEAT
  120   ...
  130 UNTIL inner% OR bail%
  140 IF NOT bail% THEN ...
  ```
- To exit a `FOR` early, the same applies — there is no clean way to abandon a `FOR` mid-flight; restructure so `NEXT` is always reached (e.g. set the index to its limit).
- Never `GOTO` out of a `FOR` or `REPEAT`. It is the same leak by a different name.

The underlying rule is simple once the stacks are laid bare: **a loop's frame is removed only by that loop's own `NEXT`/`UNTIL` (or by the prompt reset).** Nothing else — not `GOTO`, not `ENDPROC`, not an error caught by `ON ERROR` short of returning to the prompt — tidies it for you.


## Cross-references

- [`call_proc_fn`](address:B197@2?hex) — saves the 6502 and value stacks across a call; leaves the loop stacks alone.
- [`stmt_endproc`](address:9356@2?hex) — the early-exit point; restores the two general stacks only.
- [`stmt_local`](address:9323@2?hex) — stacks each `LOCAL`'s old value and bumps the call frame's restore count at `&01FB`.
- [`stmt_for`](address:B7C4@2?hex) / [`stmt_next`](address:B695@2?hex), [`stmt_repeat`](address:BBE4@2?hex) / [`stmt_until`](address:BBB1@2?hex), [`stmt_gosub`](address:B888@2?hex) / [`stmt_return`](address:B8B6@2?hex) — the matched push/pop pairs.
- [`reset_data_and_stacks`](address:BD3A@2?hex) — the prompt/`RUN` reset that zeroes all three loop-level counters.
- Workspace: [`for_stack`](address:0500@2?hex), [`repeat_stack`](address:05A4@2?hex), [`gosub_stack`](address:05CC@2?hex), and the counters [`zp_for_level`](address:0026@2?hex), [`zp_repeat_level`](address:0024@2?hex), [`zp_gosub_level`](address:0025@2?hex).
