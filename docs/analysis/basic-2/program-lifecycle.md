# Program lifecycle in BBC BASIC II: what `NEW`, `OLD`, `CLEAR`, `RUN` and `CHAIN` inherit and leave behind

> **Scope.** This article covers the **BBC BASIC II** commands that start, clear, and re-run a program — `NEW`, `OLD`, `CLEAR`, `RUN`, `CHAIN` — and exactly what state each resets versus preserves. Every routine and workspace address is specific to this version and was read from the disassembly (which reassembles byte-identically to the ROM). The expression/parsing machinery these commands hand control to is mapped in [parsers and evaluators](parsers-and-evaluators.md); the loop stacks they reset are detailed in [control flow on five stacks](control-flow-stacks.md).

The single fact that explains the whole family:

> All five commands funnel through one routine, [`clear_vars_heap_stack`](address:BD20@2?hex), which wipes the **dynamic-variable world** — every named variable, array, string and `PROC`/`FN` — but **deliberately preserves the resident integer variables `@%` and `A%`–`Z%`**, along with `HIMEM` and `PAGE`. That preservation is not an accident: it is the documented channel for passing data into a `CHAIN`ed program.

## The shared clear

[`clear_vars_heap_stack`](address:BD20@2?hex) does exactly three things:

1. `LOMEM = VARTOP = TOP` — the dynamic-variable heap is emptied by resetting its top back to the end of the program.
2. [`reset_data_and_stacks`](address:BD3A@2?hex) — the `DATA` pointer is reset to `PAGE` (an implicit `RESTORE`), the BASIC value stack to `HIMEM`, and the `FOR`/`REPEAT`/`GOSUB` level counters to empty.
3. [`clear_var_table`](address:BD2F@2?hex) — zeroes the per-letter variable chain-head table.

Step 3 is the crux, and it is precise about its range. It clears **`&0480`–`&04FF`** only:

```
.clear_var_table
    ldx #&80
    lda #0
.clear_var_table_loop
    sta var_table_base,x        ; var_table_base = &047F, so &0480..&04FF
    dex
    bne clear_var_table_loop
```

It starts at `&0480` and never descends into `&0400`–`&047F`.

## The page-4 map: why resident integers survive

That `&0480` boundary lines up with the page-4 workspace layout:

| Range | Contents | Cleared by the lifecycle commands? |
|---|---|---|
| `&0400`–`&046B` | [`resint_at`](address:0400@2?hex): the resident integers — `@%` at `&0400`, then `A%`–`Z%` at `&0404`–`&046B` (four bytes each) | **No** — never touched |
| `&046C`–`&047F` | [`fp_temps`](address:046C@2?hex): four 5-byte floating-point scratch temporaries | No (scratch, not user-visible) |
| `&0480`–`&04FF` | [`var_ptr_table`](address:0480@2?hex): the dynamic-variable chain heads (two bytes per initial-character class) | **Yes** — zeroed every time |

So `@%` and `A%`–`Z%` live *below* the cleared region and ride through `NEW`, `OLD`, `CLEAR`, `RUN` and `CHAIN` untouched. Because `@%` is also the `PRINT`/`STR$` number-format control word, **the print format carries over too** — an easily missed consequence.

## The five commands, side by side

| Command | Handler | Program text | Dynamic vars / arrays / strings / `PROC`·`FN` | Resident `@%`/`A%`–`Z%` | `LOMEM` | `DATA` ptr | `FOR`/`REPEAT`/`GOSUB` + value stack | Then |
|---|---|---|---|---|---|---|---|---|
| `NEW` | [`start_new_program`](address:8ADD@2?hex) | emptied (`CR`,`&FF` at `PAGE`; recoverable by `OLD`) | cleared | **preserved** | `=TOP` | `=PAGE` | cleared | `TRACE` off; → immediate |
| `OLD` | [`stmt_old`](address:8AB6@2?hex) | recovered + `TOP` re-derived | cleared | **preserved** | `=TOP` | `=PAGE` | cleared | → immediate |
| `CLEAR` | [`stmt_clear`](address:928D@2?hex) | kept | cleared | **preserved** | `=TOP` | `=PAGE` | cleared | → next statement |
| `RUN` | [`stmt_run`](address:BD11@2?hex) | kept | cleared | **preserved** | `=TOP` | `=PAGE` | cleared | execute from `PAGE` |
| `CHAIN` | [`stmt_chain`](address:BF2A@2?hex) | **replaced** by the loaded file | cleared | **preserved** | `=TOP` | `=PAGE` | cleared | execute from `PAGE` |

`HIMEM` and `PAGE` are preserved by every one of them — [`clear_vars_heap_stack`](address:BD20@2?hex) *reads* `HIMEM` to reset the stack but never writes it, and `PAGE` is where each program lives.

A few per-command details worth knowing:

- **`NEW`** doesn't actually erase the program — [`start_new_program`](address:8ADD@2?hex) just writes the empty-program markers (`&0D &FF`) at `PAGE`, sets `TOP = PAGE+2`, and turns `TRACE` off. The old bytes remain, which is exactly what `OLD` exploits.
- **`OLD`** removes the end marker, re-validates the lines with `check_program` (re-deriving `TOP`), then clears the heap. It only succeeds if the text hasn't been overwritten since `NEW` (by typing a new program, `LOAD`, or `CHAIN`).
- **`CLEAR`** is the pure case: it runs the shared clear and nothing else — program kept, not executed.
- **`RUN`** is `clear` then "execute from `PAGE`".
- **`CHAIN`** is `LOAD` then `RUN`: [`load_program`](address:BE62@2?hex) does an `OSFILE` load over the old program at `PAGE` and re-derives `TOP`, then falls into [`run_clear`](address:BD14@2?hex). It clears no variables itself — all the clearing is the shared `RUN` path.
- **`TRACE`** is turned off only by `NEW`; `CLEAR`/`RUN`/`CHAIN` leave the trace flag as it was.

## Carried over by every command

- **The resident integers `A%`–`Z%` and `@%`** (`&0400`–`&046B`) — values *and* `@%`'s print-format role.
- **`HIMEM`**, and therefore any memory the program reserved above it (`DIM x% N` blocks above `HIMEM`, machine code, etc.).
- **`PAGE`**.

This is why the idiom for `CHAIN` data-passing works: set `A%`…`Z%` (or stash bytes above a lowered `HIMEM`) before `CHAIN`, and read them back in the chained program.

## Two clears you might not expect

- **Editing any program line clears all variables.** Inserting or deleting a line goes through [`insert_line`](address:BC8D@2?hex) and then immediately calls [`clear_vars_heap_stack`](address:BD20@2?hex) (`&90C9`). So adding a line in the middle of a debugging session wipes the dynamic variables (the resident integers, again, survive). The out-of-room path raises *LINE space* after the same clear.
- **An error does *not* clear variables** — by contrast. The error path calls only [`reset_data_and_stacks`](address:BD3A@2?hex) (`&B41B`), which resets the `DATA` pointer and the `FOR`/`REPEAT`/`GOSUB`/value stacks but leaves every variable intact. So after an error or `Escape`, your variables are still readable at the prompt, but the loop stacks and `DATA` position are gone (this is also why `GOTO`ing back into a loop after an error misbehaves — see [control-flow stacks](control-flow-stacks.md)).

## For a compiler

Model the lifecycle as: `NEW`/`OLD`/`CLEAR`/`RUN`/`CHAIN` all reset the dynamic-variable environment (heap, arrays, strings, `PROC`/`FN` table, `LOMEM`, `DATA` position, all stacks) but **preserve** the resident integers `@%`/`A%`–`Z%`, `HIMEM` (and reserved memory above it), and `PAGE`. `CHAIN` additionally swaps the program text. The resident-integer survival is observable behaviour a faithful implementation must reproduce — programs rely on it both for `CHAIN` parameter passing and for `@%` formatting persisting across a `RUN`.

## Cross-references

- [`clear_vars_heap_stack`](address:BD20@2?hex) — the shared clear; [`clear_var_table`](address:BD2F@2) (`&BD2F`, zeroes `&0480`–`&04FF`) and [`reset_data_and_stacks`](address:BD3A@2?hex).
- [`start_new_program`](address:8ADD@2?hex) (`NEW`), [`stmt_old`](address:8AB6@2?hex) (`OLD`), [`stmt_clear`](address:928D@2?hex) (`CLEAR`), [`stmt_run`](address:BD11@2?hex)/[`run_clear`](address:BD14@2?hex) (`RUN`), [`stmt_chain`](address:BF2A@2?hex)/[`load_program`](address:BE62@2?hex) (`CHAIN`).
- Workspace: [`resint_at`](address:0400@2?hex) (`@%`, `A%`–`Z%`), [`var_ptr_table`](address:0480@2?hex), and the pointers [`LOMEM`](address:0000@2?hex), [`VARTOP`](address:0002@2?hex), [`HIMEM`](address:0006@2?hex), [`TOP`](address:0012@2?hex), [`PAGE`](address:0018@2?hex).
- [Control flow on five stacks](control-flow-stacks.md) — what `reset_data_and_stacks` empties, and the early-exit hazards.
