# The constant that isn't quite *e*: BBC BASIC's 5-byte floats and the precision of its constant pool

> **Scope.** This article describes **BBC BASIC II** — the 16 KB language ROM of the BBC Micro — and the packed 5-byte floating-point format it uses for stored REAL constants. The format and the byte-level figures are specific to this version (BASIC IV is the same format at relocated addresses; BASIC V on ARM uses IEEE doubles). Addresses are version II.

Tucked into the maths section of the ROM is a pool of pre-computed REAL constants — *e*, π/2, ln 2, log₁₀*e*, the degree/radian conversion factors, and the coefficient tables for the trig and log series. Disassembling them raised a small but stubborn question: when the ROM says it holds *e*, does it?

Not exactly — but no finite representation could. *e* is irrational, so no 32-bit fraction equals it; the most any such format can do is store the *nearest representable* value, and that, not exactness, is the fair yardstick. The sharper question is whether the ROM holds *that* nearest value — and for *e* it does not. It stores the neighbouring value one step further out — and, as we'll see, not by accident: for *e* that value is the one that prints *correctly in decimal*. A look across the whole pool shows neither tidy nearest-rounding nor any single rule, but no carelessness either. This article works through the format in the base the machine actually uses, the evidence, and why the disassembly shows the full decoded value rather than a tidy rounded one.


## The 5-byte format

A packed BBC BASIC REAL is five bytes:

```
  +0      exponent    (excess-128 bias; 0 means the whole value is zero)
  +1..+4  significand (32 bits, big-endian)
```

The significand is a normalised fraction in `[0.5, 1)`, so its top bit (bit 31, the MSB of byte +1) is *always* 1. Rather than waste it, the format **overwrites that always-1 bit with the sign** and treats the leading 1 as implied. To decode, restore it:

```
  sign = byte1 & 0x80                       ; 1 = negative
  S    = ((byte1 | 0x80) << 24) | (byte2 << 16) | (byte3 << 8) | byte4
  value = ±S × 2^(exponent − 160)
```

(The `−160` folds together the `−128` exponent bias and the `2^−32` that turns the 32-bit integer `S` back into a fraction.)

That significand is where all the precision lives, and it is **32 bits — exactly eight hexadecimal digits**. The mapping is clean: four bits to a hexit, so the entire precision of any BBC REAL is those eight hex digits and nothing more. (A decimal-digit count would only ever be approximate, and drifts with magnitude — which is part of why hex is the honest unit here. We'll still write the constants in decimal where it helps say *which* number we mean; we just won't measure precision in decimal places.)

The smallest change the format can make to a value at a given magnitude is a change of 1 in that 8-hexit significand: a **unit in the last place**, or **ULP** — the gap between one representable number and the next. Everything below is measured in ULPs of the significand.


## *e*, hexit by hexit

The constant at [`&AAE4`](address:AAE4@2?hex) is five bytes:

```asm
.flt_e
    equb &82, &2d, &f8, &54, &58    ; bbc_float5 = 2.718281827867031  e
```

Exponent `&82` = 130; restoring the implied leading bit gives the significand `(0x2d|0x80) f8 54 58` = **`ADF85458`**.

Now carry the true value of *e* to more than 32 significand bits and line the two up:

```
  ROM significand    A D F 8 5 4 5 8
  true  e            A D F 8 5 4 5 8 . A2B…        (the bits past 32)
  nearest 32-bit     A D F 8 5 4 5 9               (round: leading dropped hexit A ≥ 8)
```

The ROM keeps all eight stored hexits of *e* exactly and simply **drops the continuation** `.A2B…`. That is a *truncation*: rounded to nearest, the first dropped hexit (`A`, which is ≥ 8) would have carried the last digit up to `ADF85459`. Acorn took the floor instead, so the stored significand sits one ULP below the round-to-nearest result (and, as the decimal below shows, about 0.64 ULP below *e* itself).

For the human reader, in decimal:

|                                              | value                          |
|----------------------------------------------|--------------------------------|
| ROM constant at `&AAE4` (= `ADF85458 / 2³⁰`) | `2.718281827867031`            |
| true *e*                                     | `2.718281828459045`            |
| difference                                   | `5.92 × 10⁻¹⁰`  (≈ `0.64` ULP) |

One ULP here is `2^(130−160) = 2^−30 ≈ 9.31 × 10⁻¹⁰`. The point isn't that the bytes aren't *e* — no 32-bit value is — but that they aren't even the *closest* value the format can hold: the nearest representable significand, `ADF85459`, lies `0.36` ULP from *e*, while the ROM keeps its lower neighbour `ADF85458` at `0.64` ULP. A better *binary* value was available in the same five bytes, and rounding down passed it over — which looks like a slip until you ask what the bytes *print as*. (They are the exact rational `ADF85458 / 2³⁰`.)


## Why round down? Decimal fidelity

The truncation looks like a slip only until you ask what the stored value *prints as*. BBC BASIC shows reals to ten significant figures, and to ten figures *e* is `2.718281828`. Convert *that* decimal back into the format and you land on significand `2918732888` = `ADF85458` — the value actually in the ROM. The binary-nearest value `ADF85459` would instead print `2.718281829`, a wrong tenth digit. So the binary-suboptimal choice is the *decimal-optimal* one: it is exactly what you get by writing *e* to ten figures and converting, faithful to the decimal at the cost of a fraction of a ULP in binary.

A real BBC Micro bears it out — `@% = &A0A` selects ten significant figures:

```
>@%=&A0A
>PRINT EXP(1)
2.718281828
>PRINT PI
3.141592653
```

`EXP(1)` evaluates to `e⁰ × e¹` with both factors exact, so it returns the raw `&AAE4` constant — and it reads `2.718281828`, not the `2.718281829` the binary-nearest value would have given. (`PRINT PI` showing `3.141592653` confirms the ten-figure display is live and rounding to nearest; that it lands one digit below true π is just the format running out of precision at the tenth figure — a separate effect.)

The likeliest mechanism is the dullest one: the constants were written down as decimals, to whatever length the source table carried, and an assembler converted them. The stored binary is then the nearest representable to *the decimal Acorn wrote*, not to the true irrational — and the two diverge exactly when the decimal's last digit and the binary's last bit disagree. The value isn't careless; it's loyal to its decimal.


## Not a uniform policy

Does that decimal loyalty explain the *whole* pool? Not quite. Restoring each named scalar's significand and comparing it with the true value carried past 32 bits:

| constant | addr    | exp | ROM significand | true significand (hex) | nearest 32-bit | ROM − nearest          |
|----------|---------|-----|-----------------|------------------------|----------------|------------------------|
| *e*      | `&AAE4` | 130 | `ADF85458`      | `ADF85458.A2B…`        | `ADF85459`     | **−1 ULP** (truncated) |
| π/2      | `&AA63` | 129 | `C90FDAA2`      | `C90FDAA2.216…`        | `C90FDAA2`     | 0                      |
| ln 2     | `&A86E` | 128 | `B17217F8`      | `B17217F7.D1C…`        | `B17217F8`     | 0 (rounded up)         |
| log₁₀*e* | `&A869` | 127 | `DE5BD8AA`      | `DE5BD8A9.372…`        | `DE5BD8A9`     | **+1 ULP**             |
| π/180    | `&AA68` | 123 | `8EFA3512`      | `8EFA3512.94E…`        | `8EFA3513`     | **−1 ULP** (truncated) |
| 180/π    | `&AA6D` | 134 | `E52EE0D3`      | `E52EE0D3.1E0…`        | `E52EE0D3`     | 0                      |

Read the last two columns together. Where the dropped continuation is far from `.8`, truncation and round-to-nearest land on the same hexit and the ROM is correct either way (π/2, 180/π). Where they differ, the behaviour is mixed:

- *e* and π/180 are **truncated** — the continuation begins with a hexit ≥ 8 (`A`, `9`) that should have rounded the last digit up, but didn't, leaving them one ULP low;
- **ln 2 is correctly rounded** — its true significand is `…F7.D1C…`, and the `.D` *did* carry `F7` up to `F8`;
- **log₁₀*e* sits one ULP *above* the correctly-rounded value** (`DE5BD8AA` where nearest is `DE5BD8A9`). It is *high*, so it cannot be a truncation at all.

So decimal fidelity explains *e* — and is consistent with π/180, whose truncation is decimally harmless (both neighbours print the same ten figures) — but it does not govern the whole pool. ln 2, π/2 and 180/π simply happen to be the nearest value in both bases at once. log₁₀*e*, though, is the odd one out: a ULP high in binary *and* wrong in its tenth decimal figure (`0.4342944820` against the true `0.4342944819`), worse in both bases than the value next door. That's the signature of a *computed* constant rather than a typed one — consistent with its having been formed as `1 / ln 10` from a slightly-low `ln 10` and never corrected. The honest summary: **most of the constants are faithful to a decimal, a couple are the nearest representable outright, and at least one is simply a little off — no single discipline, but no carelessness either.**


## A constant the interpreter can beat

The log₁₀*e* outlier is something you can watch happen. BBC BASIC effectively carries log₁₀*e* twice over: `LOG` reaches for the stored `&A869` constant (`LOG(x) = LN(x) × log₁₀e`), while `1/LN(10)` derives the same quantity afresh from the `ln 10` series, never touching the table.

The stored constant is `7F 5E 5B D8 AA` → `0.4342944819945842`, i.e. `0.4342944820` at ten figures and `0.79` ULP high. BASIC II has no float-indirection operator to read those ROM bytes back as a real, but the value reconstructs exactly as the significand over a power of two. On a real machine, with ten figures selected:

```
>@%=&A0A
>PRINT 1865280597/(2^32)
0.434294482
>PRINT 1/LN(10)
0.4342944819
```

The first line is the stored `&A869` constant, rebuilt arithmetically as `3730561194 / 2³³` (halved to `1865280597 / 2³²` to keep the literal representable) — and general format trims its trailing zero, so `0.4342944820` shows as `0.434294482`. The second is log₁₀*e* recomputed from the `ln 10` series. They diverge at the tenth figure: the stored value rounds *up* to `…820`, the computed one lands on the correct `…819`.

So the interpreter computes a *more accurate* log₁₀*e* than the one baked into its own ROM, and then ships the inferior value in `LOG`, the one function whose entire job is base-10 logarithms. The likeliest history is the one the survey pointed to: the constant was precomputed once — `1 / ln 10` from an `ln 10` a hair too low, rounded the wrong way — and never revisited, while the runtime series simply happens to be good enough that one-over-it lands on the right bit.


## Why the disassembly shows the full value

This is precisely why the typed-data annotation emits the whole decoded figure and not a rounded one:

```asm
    equb &82, &2d, &f8, &54, &58    ; bbc_float5 = 2.718281827867031  e
```

Printed as `2.718281828`, the constant would read as exact *e* and hide both facts at once — that it is a finite approximation, and that it isn't even the closest one the format allows. Anyone wondering why BASIC's `EXP`, `LN` or `DEG`/`RAD` disagree with a pocket calculator in the last digits is owed the value actually stored, not a flattering round of it: the *constants themselves* carry up to a ULP of error before a single multiply happens. The full repr makes the stored reality visible; the comment after it (`e`) names the *intent* without claiming the bytes achieve it.


## Working past the limit: the two-part π/2

Acorn knew 32 bits wasn't always enough, and one corner of the pool shows them engineering around it. Argument reduction for `SIN`/`COS` needs `x − n·(π/2)` accurately even when `n` is large, and a single 32-bit π/2 loses low-order bits in the product. So π/2 is stored **twice**, as a high part plus a correction — a textbook *Cody–Waite split*:

- [`&AA59`](address:AA59@2?hex): a deliberately *low-precision* high part, `−1.57080078125`, whose significand `C9100000` has its **bottom two bytes zeroed** — so `n × C₁` is computed with no rounding error in the product;
- [`&AA5E`](address:AA5E@2?hex): the correction `4.454455 × 10⁻⁶`, holding the bits the high part dropped.

Their sum is `−π/2` to about fourteen digits — far past what a single 32-bit value could carry — and the reduction subtracts the two parts in turn. It's a neat acknowledgement, in the ROM itself, of the very precision ceiling this article is about. (Both halves are typed `bbc_float5` in the disassembly, so their decoded values sit right beside the bytes.)


## In the disassembly

All 39 packed constants in the pool — the named scalars, the `1.0`/`−0.5` terms, and every coefficient of the ATN/SIN/EXP/LN continued-fraction tables — are marked with the `bbc_float5` typed-data type (dasmos 1.10.0). The five raw bytes are still emitted, so the image reassembles byte-identical, while the decoded value rides along as an annotation (and as a structured `decoded` field in the JSON). That is what makes a claim like "the *e* in the ROM is the rational `ADF85458 / 2³⁰` — a ULP short of the nearest value the format could hold" something you can read straight off the listing rather than having to work out by hand.


## Cross-references

- [`&AAE4`](address:AAE4@2?hex) — the *e* constant analysed above.
- [`&AA63`](address:AA63@2?hex) π/2, [`&A86E`](address:A86E@2?hex) ln 2, [`&A869`](address:A869@2?hex) log₁₀*e*, [`&AA68`](address:AA68@2?hex) π/180, [`&AA6D`](address:AA6D@2?hex) 180/π.
- [`&AA59`](address:AA59@2?hex) / [`&AA5E`](address:AA5E@2?hex) — the two-part π/2 for accurate range reduction.
- [`fp_eval_cont_frac`](address:A897@2?hex) — the evaluator that consumes the coefficient tables whose entries share this format.
