# BBC BASIC's 5-byte floats and the precision of its constant pool

> **Scope.** This article describes **BBC BASIC II** — the 16 KB language ROM of the BBC Micro — and the packed 5-byte floating-point format it uses for stored REAL constants. The format, the addresses, and the byte-level figures are all specific to this version.

The maths section of the ROM holds a pool of pre-computed REAL constants — *e*, π/2, ln 2, log₁₀*e*, the degree/radian conversion factors, and the coefficient tables for the trig and log series. Each is a 32-bit approximation to an irrational or non-terminating value, so none is exact; the most the format can hold is a value within one unit in the last place (ULP) of the target.

For *e*, the stored value is not even the *nearest* representable one — it is the neighbour one step further out, which is the value that prints correctly when BBC BASIC rounds it to ten figures. Across the whole pool the rounding is not uniform: most constants are faithful to a written decimal, a couple are the nearest representable outright, and one is a ULP off in both bases. This article works through the format in the base the machine uses, sets out the value stored for each constant, and shows how the disassembly records the exact stored value.


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

The constant at `&AAE4` is five bytes:

```asm
    equb &82, &2d, &f8, &54, &58    ; float40 2.718281828  e
```

Exponent `&82` = 130; restoring the implied leading bit gives the significand `(0x2d|0x80) f8 54 58` = **`ADF85458`**. (`float40` is the disassembly's display label for the packed 5-byte type; the inline comment shows the value to ten significant figures, of which more below.)

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

One ULP here is `2^(130−160) = 2^−30 ≈ 9.31 × 10⁻¹⁰`. The bytes are not *e* — no 32-bit value is — but they are also not the *closest* value the format can hold: the nearest representable significand, `ADF85459`, lies `0.36` ULP from *e*, while the ROM keeps its lower neighbour `ADF85458` at `0.64` ULP. A better *binary* value was available in the same five bytes; rounding down passed it over. The reason emerges from what the bytes *print as* — they are the exact rational `ADF85458 / 2³⁰`.


## Why round down? Decimal fidelity

The reason is the decimal display. To ten significant figures *e* is `2.718281828`. Convert *that* decimal back into the format and you land on significand `2918732888` = `ADF85458` — the value actually in the ROM. The binary-nearest value `ADF85459` would instead print `2.718281829`, a wrong tenth digit. So the binary-suboptimal choice is the *decimal-optimal* one: it is exactly what you get by writing *e* to ten figures and converting, faithful to the decimal at the cost of a fraction of a ULP in binary.

A real BBC Micro bears it out. The default general format shows **nine** significant figures (`@%` powers on as `&0000090A`), at which the constants print correctly — `PRINT PI` gives `3.14159265`. Widening to ten with `@% = &A0A` is what exposes the last-figure differences:

```
>@%=&A0A
>PRINT EXP(1)
2.718281828
>PRINT PI
3.141592653
```

`EXP(1)` evaluates to `e⁰ × e¹` with both factors exact, so it returns the raw `&AAE4` constant — and it reads `2.718281828`, not the `2.718281829` the binary-nearest value would have given.

The companion `PRINT PI` shows `3.141592653`, one below true π's ten-figure value `3.141592654` — and here the last figure is genuinely wrong, for a reason that turns on this ROM storing π/2 rather than π. There is no stored π: [`fn_pi`](address:ABCB@2?hex) loads the π/2 constant and doubles it by incrementing the exponent (`INC zp_fwa_exp`), which is exact. But doubling the *nearest* representable π/2 does not give the nearest representable π. The stored π/2 significand is `C90FDAA2` (`⌊π/2 × 2³¹⌉`, which drops the `.006` past the 32nd bit); doubling leaves that significand unchanged at π's exponent, whereas the nearest π is `C90FDAA3` (`π × 2³⁰` rounds *up*, to `…426.99`). So `PI` comes out one ULP low, at `3.14159265347`, and the print routine correctly rounds *that* to `3.141592653`. Rounding π/2 and then doubling is not the same as rounding π; had the ROM stored π directly, `PRINT PI` would show the correct `3.141592654`. This surfaces only at ten figures: at the default nine, both the stored value and true π round to `3.14159265`, so the deficit sits just past the last digit shown.

The likely mechanism is prosaic: the constants were written down as decimals, to whatever length the source table carried, and an assembler converted them. The stored binary is then the nearest representable to *the decimal Acorn wrote*, not to the true irrational — and the two diverge exactly when the decimal's last digit and the binary's last bit disagree.


## Not a uniform policy

Does decimal fidelity explain the *whole* pool? Not quite. Restoring each named scalar's significand and comparing it with the true value carried past 32 bits:

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

So decimal fidelity explains *e* — and is consistent with π/180, whose truncation is decimally harmless (both neighbours print the same ten figures) — but it does not govern the whole pool. ln 2, π/2 and 180/π simply happen to be the nearest value in both bases at once. log₁₀*e*, though, is the odd one out: a ULP high in binary *and* wrong in its tenth decimal figure (`0.4342944820` against the true `0.4342944819`), worse in both bases than the value next door. That is the signature of a *computed* constant rather than a typed one — consistent with its having been formed as `1 / ln 10` from a slightly-low `ln 10` and never corrected. In summary: **most of the constants are faithful to a written decimal, a couple are the nearest representable outright, and at least one is a ULP off — no single rule across the pool.**


## A constant the interpreter computes more accurately than it stores

The log₁₀*e* outlier can be observed directly. BBC BASIC effectively carries log₁₀*e* twice over: `LOG` reaches for the stored `&A869` constant (`LOG(x) = LN(x) × log₁₀e`), while `1/LN(10)` derives the same quantity afresh from the `ln 10` series, never touching the table.

The stored constant is `7F 5E 5B D8 AA` → `0.4342944819945842`, i.e. `0.4342944820` at ten figures and `0.79` ULP high. BASIC II has no float-indirection operator to read those ROM bytes back as a real, but the value reconstructs exactly as the significand over a power of two. On a real machine, with ten figures selected:

```
>@%=&A0A
>PRINT 1865280597/(2^32)
0.434294482
>PRINT 1/LN(10)
0.4342944819
```

The first line is the stored `&A869` constant, rebuilt arithmetically as `3730561194 / 2³³` (halved to `1865280597 / 2³²` to keep the literal representable) — and general format trims its trailing zero, so `0.4342944820` shows as `0.434294482`. The second is log₁₀*e* recomputed from the `ln 10` series. They diverge at the tenth figure: the stored value rounds *up* to `…820`, the computed one lands on the correct `…819`.

So the interpreter computes a *more accurate* log₁₀*e* than the one stored in its own ROM, yet `LOG` — whose job is base-10 logarithms — uses the stored constant. The likely history: the constant was precomputed once as `1 / ln 10` from an `ln 10` slightly too low, rounded the wrong way, and never revised, while the runtime `ln 10` series is good enough that one over it lands on the correct bit.


## How the disassembly records the value

The typed-data annotation records each constant at two precisions. The `.asm` inline comment shows the value to ten significant figures — the honest width of a 32-bit mantissa, and the same figure BBC BASIC itself prints:

```asm
    equb &82, &2d, &f8, &54, &58    ; float40 2.718281828  e
```

At that width the stored constant is indistinguishable from true *e*: the two agree to ten figures, as *Why round down* showed, and the departure only appears at the eleventh. The exact stored value — the rational `ADF85458 / 2³⁰` = `2.718281827867031` — is carried full-precision in the JSON `decoded.value` field, where the gap from *e* is explicit. Anyone wondering why BASIC's `EXP`, `LN` or `DEG`/`RAD` disagree with a pocket calculator in the last digits can read the exact stored value there: the *constants themselves* carry up to a ULP of error before a single multiply happens. The trailing `e` in the comment names the *intent* without claiming the bytes achieve it.


## Working past the limit: the two-part π/2

Acorn knew 32 bits wasn't always enough, and one corner of the pool shows them engineering around it. Argument reduction for `SIN`/`COS` needs `x − n·(π/2)` accurately even when `n` is large, and a single 32-bit π/2 loses low-order bits in the product. So π/2 is stored **twice**, as a high part plus a correction — a textbook *Cody–Waite split*:

- `&AA59`: a deliberately *low-precision* high part, `−1.57080078125`, whose significand `C9100000` has its **bottom two bytes zeroed** — so `n × C₁` is computed with no rounding error in the product;
- `&AA5E`: the correction `4.454455 × 10⁻⁶`, holding the bits the high part dropped.

Their sum is `−π/2` to about fourteen digits — far past what a single 32-bit value could carry — and the reduction subtracts the two parts in turn. This works past the 32-bit ceiling the rest of this article describes. (Both halves carry the packed 5-byte type in the disassembly, so their decoded values sit beside the bytes.)


## In the disassembly

All 39 packed constants in the pool — the named scalars, the `1.0`/`−0.5` terms, and every coefficient of the ATN/SIN/EXP/LN continued-fraction tables consumed by [`fp_eval_cont_frac`](address:A897@2?hex) — are marked with the packed 5-byte typed-data type (display label `float40`). The five raw bytes are still emitted, so the image reassembles byte-identical, while the ten-figure value rides along as the inline annotation and the exact stored value as the `value` in the structured `decoded` field of the JSON. That is what makes a statement like "the *e* in the ROM is the rational `ADF85458 / 2³⁰` — a ULP short of the nearest value the format could hold" something you can read from the disassembly's data rather than work out by hand.
