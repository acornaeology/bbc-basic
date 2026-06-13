# The constant that isn't quite *e*: BBC BASIC's 5-byte floats and the precision of its constant pool

> **Scope.** This article describes **BBC BASIC II** — the 16 KB language ROM of the BBC Micro — and the packed 5-byte floating-point format it uses for stored REAL constants. The format and the byte-level figures are specific to this version (BASIC IV is the same format at relocated addresses; BASIC V on ARM uses IEEE doubles). Addresses are version II.

Tucked into the maths section of the ROM is a pool of pre-computed REAL constants — *e*, π/2, ln 2, log₁₀*e*, the degree/radian conversion factors, and the coefficient tables for the trig and log series. Disassembling them raised a small but stubborn question: when the ROM says it holds *e*, does it?

It does not. It holds a 32-bit approximation that matches *e* in every bit the format can store but is still, in the last bit, demonstrably *not e*. A close look at the whole pool shows something more: the rounding of that last bit isn't even consistent from one constant to the next. This article works through the format in the base the machine actually uses, the evidence, and why the disassembly shows the full decoded value rather than a tidy rounded one.


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

| | value |
|---|---|
| ROM constant at `&AAE4` (= `ADF85458 / 2³⁰`) | `2.718281827867031` |
| true *e* | `2.718281828459045` |
| difference | `5.92 × 10⁻¹⁰`  (≈ `0.64` ULP) |

One ULP here is `2^(130−160) = 2^−30 ≈ 9.31 × 10⁻¹⁰`, so the shortfall of `0.64` ULP is exactly the size of error you get from reducing an irrational number to 32 significand bits. The bytes are not *e*; they are the rational `ADF85458 / 2³⁰`.


## Not a uniform policy

The obvious next hypothesis — "these tables were all truncated" — turns out to be wrong. Restoring each named scalar's significand and comparing it with the true value carried past 32 bits:

| constant | addr | exp | ROM significand | true significand (hex) | nearest 32-bit | ROM − nearest |
|---|---|---|---|---|---|---|
| *e* | `&AAE4` | 130 | `ADF85458` | `ADF85458.A2B…` | `ADF85459` | **−1 ULP** (truncated) |
| π/2 | `&AA63` | 129 | `C90FDAA2` | `C90FDAA2.216…` | `C90FDAA2` | 0 |
| ln 2 | `&A86E` | 128 | `B17217F8` | `B17217F7.D1C…` | `B17217F8` | 0 (rounded up) |
| log₁₀*e* | `&A869` | 127 | `DE5BD8AA` | `DE5BD8A9.372…` | `DE5BD8A9` | **+1 ULP** |
| π/180 | `&AA68` | 123 | `8EFA3512` | `8EFA3512.94E…` | `8EFA3513` | **−1 ULP** (truncated) |
| 180/π | `&AA6D` | 134 | `E52EE0D3` | `E52EE0D3.1E0…` | `E52EE0D3` | 0 |

Read the last two columns together. Where the dropped continuation is far from `.8`, truncation and round-to-nearest land on the same hexit and the ROM is correct either way (π/2, 180/π). Where they differ, the behaviour is mixed:

- *e* and π/180 are **truncated** — the continuation begins with a hexit ≥ 8 (`A`, `9`) that should have rounded the last digit up, but didn't, leaving them one ULP low;
- **ln 2 is correctly rounded** — its true significand is `…F7.D1C…`, and the `.D` *did* carry `F7` up to `F8`;
- **log₁₀*e* sits one ULP *above* the correctly-rounded value** (`DE5BD8AA` where nearest is `DE5BD8A9`). It is *high*, so it cannot be a truncation at all.

So the pool was not produced by one clean rule. Every constant is within a single ULP of the truth — as good as a 32-bit significand gets — but whoever generated the table did not apply a uniform round-to-nearest discipline. (log₁₀*e* coming out a ULP high is consistent with its having been formed as `1 / ln 10` from a slightly-low `ln 10` and never corrected.) The honest summary is: **each value is right to within ±1 ULP of the best 32-bit approximation, and the last bit is idiosyncratic.**


## Why the disassembly shows the full value

This is precisely why the typed-data annotation emits the whole decoded figure and not a rounded one:

```asm
    equb &82, &2d, &f8, &54, &58    ; bbc_float5 = 2.718281827867031  e
```

Printed as `2.718281828`, the constant would read as exact *e* and hide the truncation entirely. Anyone reasoning about the ROM — or wondering why BASIC's `EXP`, `LN` or `DEG`/`RAD` disagree with a pocket calculator in the last digits — would be misled into thinking the inputs were perfect and the routines lossy. They aren't: the *constants themselves* are already a ULP off, before a single multiply happens. The full repr makes the stored reality visible; the comment after it (`e`) names the *intent* without claiming the bytes achieve it.


## Working past the limit: the two-part π/2

Acorn knew 32 bits wasn't always enough, and one corner of the pool shows them engineering around it. Argument reduction for `SIN`/`COS` needs `x − n·(π/2)` accurately even when `n` is large, and a single 32-bit π/2 loses low-order bits in the product. So π/2 is stored **twice**, as a high part plus a correction — a textbook *Cody–Waite split*:

- [`&AA59`](address:AA59@2?hex): a deliberately *low-precision* high part, `−1.57080078125`, whose significand `C9100000` has its **bottom two bytes zeroed** — so `n × C₁` is computed with no rounding error in the product;
- [`&AA5E`](address:AA5E@2?hex): the correction `4.454455 × 10⁻⁶`, holding the bits the high part dropped.

Their sum is `−π/2` to about fourteen digits — far past what a single 32-bit value could carry — and the reduction subtracts the two parts in turn. It's a neat acknowledgement, in the ROM itself, of the very precision ceiling this article is about. (Both halves are typed `bbc_float5` in the disassembly, so their decoded values sit right beside the bytes.)


## In the disassembly

All 39 packed constants in the pool — the named scalars, the `1.0`/`−0.5` terms, and every coefficient of the ATN/SIN/EXP/LN continued-fraction tables — are marked with the `bbc_float5` typed-data type (dasmos 1.10.0). The five raw bytes are still emitted, so the image reassembles byte-identical, while the decoded value rides along as an annotation (and as a structured `decoded` field in the JSON). That is what makes a claim like "the *e* in the ROM is `ADF85458 / 2³⁰`, not *e*" something you can read straight off the listing rather than having to work out by hand.


## Cross-references

- [`&AAE4`](address:AAE4@2?hex) — the *e* constant analysed above.
- [`&AA63`](address:AA63@2?hex) π/2, [`&A86E`](address:A86E@2?hex) ln 2, [`&A869`](address:A869@2?hex) log₁₀*e*, [`&AA68`](address:AA68@2?hex) π/180, [`&AA6D`](address:AA6D@2?hex) 180/π.
- [`&AA59`](address:AA59@2?hex) / [`&AA5E`](address:AA5E@2?hex) — the two-part π/2 for accurate range reduction.
- [`fp_eval_cont_frac`](address:A897@2?hex) — the evaluator that consumes the coefficient tables whose entries share this format.
