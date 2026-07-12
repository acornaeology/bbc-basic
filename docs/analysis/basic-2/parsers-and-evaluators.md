# Parsers and evaluators in BBC BASIC II: who reads text, and how the language reaches them

> **Scope.** This article maps the **BBC BASIC II** text-reading machinery — the tokeniser, the statement dispatcher, the expression evaluator and its factor-level readers, the lvalue parser, and the two string→value front doors `VAL` and `EVAL`. Every routine address is specific to this version and was read from the disassembly (which reassembles byte-identically to the ROM). It is a road-map: the deep dives on [tokenising](tokeniser-and-detokeniser.md), [control-flow stacks](control-flow-stacks.md), [floating point](floating-point-constants-and-precision.md) and [indirection lvalues](indirection-lvalue-parameters.md) cover the individual pieces.

BBC BASIC II is not one parser but several distinct text-reading machines, each reached from the language in different places. That structure accounts for a number of surface behaviours that otherwise look arbitrary: `VAL("&FF")` gives 0 while `EVAL("&FF")` gives 255; `TOP` reads as a pseudo-variable in some positions but as `TO` followed by `P` in others; an indirection can serve as a procedure parameter. Each follows from which machine reads the text, and where.

## The machines at a glance

| Layer | Routine(s) | Reads → produces | Reached from BASIC by |
|---|---|---|---|
| Tokeniser (crunch) | [`tokenise_line`](address:8951@2?hex) | source text → token bytes | every line as typed/edited; `EVAL` re-runs it on a string |
| Statement dispatch | [`next_statement`](address:8BA3@2?hex) / [`dispatch_token`](address:8BB1@2?hex) | a token → a handler | `RUN`, immediate mode, each `:`-separated statement |
| Expression evaluator | [`eval_expr`](address:9B1D@2?hex) → the precedence ladder | token stream → a typed value | anywhere an expression is wanted (`PRINT`, `=`, `IF`, arguments…) |
| Factor readers (level 1) | [`eval_factor`](address:ADEC@2?hex) and its sub-readers | one atom → a value | reached only *through* the evaluator |
| Lvalue parser | [`parse_lvalue`](address:9582@2?hex) / [`parse_var_ref`](address:95C9@2?hex) | text → an assignable location + type | `LET`, `FOR`, `LOCAL`, `PROC`/`FN` parameters |
| String→value front doors | [`fn_val`](address:AC2F@2?hex) (`VAL`), [`fn_eval`](address:ABE9@2?hex) (`EVAL`) | a string → a value | the `VAL` and `EVAL` functions |

The rest of this article walks the three layers behind those behaviours: the evaluator ladder, the factor-level *readers* (where the number/hex/string/variable splits live), and the two front doors.

## The expression evaluator: a precedence ladder

[`eval_expr`](address:9B1D@2?hex) is the single entry point. It copies the program pointer PtrA into the working pointer PtrB and enters the lowest-precedence level. Each level evaluates a higher-precedence operand, then loops consuming its own operators — a classic recursive-descent precedence climb:

| Level | Routine | Operators |
|---|---|---|
| 7 (lowest) | [`eval_or_eor`](address:9B29@2?hex) | `OR`, `EOR` |
| 6 | [`eval_and`](address:9B72@2?hex) | `AND` |
| 5 | [`eval_relational`](address:9B9C@2?hex) | `< <= = >= > <>` |
| 4 | [`eval_add_sub`](address:9C42@2?hex) | `+ -` (and string concatenation) |
| 3 | [`eval_mul_div`](address:9DD1@2?hex) | `* / DIV MOD` |
| 2 | [`eval_power`](address:9E20@2?hex) | `^` |
| 1 | [`eval_factor`](address:ADEC@2?hex) | the **atom** |

[`eval_factor`](address:ADEC@2?hex) is "level 1" — the highest-precedence rung and the one that actually *reads* things. It handles unary `-`, `+` and `NOT`; a parenthesised sub-expression; the `?`, `!`, `$` and `|` indirection operators; string literals; and the built-in functions. Unlike the higher levels it does **not** read the trailing operator — its caller does. Everything below is a sub-reader dispatched from here.

## The factor readers — where the splits live

This is the layer that explains the surface quirks. `eval_factor` looks at the first character of the atom and dispatches:

- **Decimal / floating-point numbers** → [`parse_number`](address:A07B@2?hex). Reads digits, a `.` and an `E` exponent, choosing integer or real (a point or exponent forces real). It is **decimal only** — there is no `&` branch in it, and a non-digit first character yields 0.
- **Hex constants** → [`factor_hex`](address:AE6D@2?hex), dispatched on a leading `&`. Folds `0-9` and **uppercase** `A-F` into a 32-bit cell as a bit pattern, with **no overflow check** (a 9th digit drops the top nibble; `&FFFFFFFF` = −1) and the sole error *Bad HEX* when no hex digit follows. Lowercase `a-f` ends the scan.
- **String literals** (`"..."`) → [`read_string_literal`](address:ADAD@2?hex).
- **Variables, array elements and indirection** as *values* → the scanner shared with the lvalue path ([`parse_var_ref`](address:95C9@2?hex)).
- **Built-in functions** → the per-token `fn_*` handlers, reached through the action-address table ([`action_table_lo`](address:836D@2?hex)) by token value. This is how `SIN`, `LEN`, `VAL`, `EVAL`, and the `TO`-token's [`fn_to`](address:AEDC@2?hex) (which reads `TOP`) are dispatched.

The decimal reader and the hex reader are different routines, and `&` is reachable only through `eval_factor`: `parse_number` never sees a `&`. That split is the root of the `VAL`/`EVAL` difference below.

## The lvalue parser: one routine, four exposures

Assignment *targets* are read by a separate machine, [`parse_lvalue`](address:9582@2?hex) (via [`parse_var_ref`](address:95C9@2?hex)). It returns a storage address plus a type byte, and — crucially — it is shared verbatim by **four** language constructs: the left of `LET`, the `FOR` control variable, each `LOCAL`, and each `PROC`/`FN` formal parameter. Because they all call the same routine they accept the same grammar, which is why a `?`/`!`/`$` indirection or an array element is a legal `FOR` variable, `LOCAL`, *and* formal parameter — see [indirection lvalues as parameters](indirection-lvalue-parameters.md).

## Two string→value front doors: `VAL` and `EVAL`

Both turn a string into a value, but through completely different machines:

- **`VAL`** ([`fn_val`](address:AC2F@2?hex)) runs the **decimal reader on the raw string**: [`ascii_to_number`](address:AC34@2?hex) handles an optional leading sign, then defers to [`parse_number`](address:A07B@2?hex). No tokenising, no operators, no `&`. It reads a number from the *start* of the string and stops at the first non-numeric character.
- **`EVAL`** ([`fn_eval`](address:ABE9@2?hex)) **tokenises the string and runs the full evaluator** on it: it copies the argument to the stack, appends a `CR`, crunches it in place (in mid-statement state, so `PTR`/`TIME` etc. tokenise as functions), and calls [`eval_expr`](address:9B1D@2?hex). So it accepts everything an expression can contain — `&` hex, `E` exponents, operators, parentheses, functions and in-scope variables.

That is the entire reason for the classic contrast:

| Input | `VAL(x$)` | `EVAL(x$)` | Why |
|---|---|---|---|
| `"1E3"` | 1000 | 1000 | both reach `parse_number`, which reads the `E` exponent |
| `"&FF"` | **0** | **255** | `VAL`'s `parse_number` has no `&` branch; `EVAL` tokenises and reaches `factor_hex` |
| `"12AB"` | 12 | (depends) | `VAL` stops at the first non-digit; `EVAL` evaluates `12` then sees `AB` as a variable/operator context |
| `"2+3"` | 2 | 5 | `VAL` reads one number; `EVAL` evaluates the whole expression |

`VAL` reads a literal; `EVAL` runs the interpreter. They are two separate readers, not one reader with a flag.

## Surface consequences, and where they're documented

Several of BASIC II's surface behaviours are these machine boundaries showing through:

- **`VAL` vs `EVAL` on hex** — the two-readers split above.
- **`TOP` is not a token** — the crunch emits `TO`+`'P'`; the pseudo-variable is resolved at *factor* time by [`fn_to`](address:AEDC@2?hex), only when the `TO` token is in operand position immediately followed by a bare `P`. See [tokeniser §1.7](tokeniser-and-detokeniser.md).
- **Indirection as a parameter** — `parse_lvalue` being shared by the `PROC`/`FN` binder. See [indirection lvalues](indirection-lvalue-parameters.md).
- **`&` is uppercase-only and wraps at 32 bits** — a property of `factor_hex`, not of "numbers" in general.
