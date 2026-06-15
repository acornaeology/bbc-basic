# Data files in BBC BASIC II: channels, raw bytes, and the backwards `PRINT#`

> **Scope.** This article is about **data files** in **BBC BASIC II** — the channel-based file I/O reached through `OPENIN`/`OPENOUT`/`OPENUP`, `CLOSE`, `BGET#`/`BPUT#`, `PRINT#`/`INPUT#`, and `PTR#`/`EXT#`/`EOF#`. It is *not* about loading and saving whole programs: `LOAD`, `SAVE` and `CHAIN` are a separate mechanism — a single `OSFILE` call driven by an 18-byte control block — documented in the [`load_program`](address:BE62@2?hex) banner, and out of scope here. Every address and value below is specific to BASIC II and was read from the disassembly (which reassembles byte-identically to the ROM).

The headline, for the impatient:

> **`PRINT#` does not write text.** `PRINT#channel, 42` does not write the characters `4` `2`. It writes a 1-byte *type tag* and then the number's raw bytes **in reverse** — five bytes `40 00 00 00 2A`. Strings go out backwards too. The format is private to BASIC; a `PRINT#` file is meant to be read back only by `INPUT#`.

---

## 1. The channel model

BBC BASIC owns no file logic of its own — every data-file word is a thin wrapper over a MOS (operating-system) call. A file is identified by a one-byte **handle** returned when it is opened. The whole vocabulary maps onto five MOS calls (see [`eval_channel`](address:BFB5@2?hex), the shared `#handle` parser):

| BASIC                | MOS call | A   | Notes |
|----------------------|----------|-----|-------|
| `OPENIN f$`          | `OSFIND` | `&40` | open existing for input |
| `OPENOUT f$`         | `OSFIND` | `&80` | create for output |
| `OPENUP f$`          | `OSFIND` | `&C0` | open existing for update |
| `CLOSE #h`           | `OSFIND` | `&00` | `CLOSE#0` closes *every* open file |
| `BPUT# h, b`         | `OSBPUT` | —   | write one byte (`A`), handle in `Y` |
| `=BGET# h`           | `OSBGET` | —   | read one byte, handle in `Y` |
| `PTR# h =`           | `OSARGS` | `&01` | write the sequential pointer |
| `=PTR# h`            | `OSARGS` | `&00` | read the sequential pointer |
| `=EXT# h`            | `OSARGS` | `&02` | read the extent (length) |
| `=EOF# h`            | `OSBYTE` | `&7F` | test for end of file |

The handle is passed in `Y` (except `OSFILE`/`OSARGS`, which take a control block / a zero-page value address). **`OSFIND` returns the new handle in `A`, or 0 if the open failed** — which is why the idiom is `chan=OPENIN("x"):IF chan=0 THEN ...`. Two things follow from this being pure MOS plumbing: the *meaning* of a handle, the maximum number of open files, and the on-media layout all belong to the current filing system, not to BASIC; and `PTR#`/`EXT#` work in whatever units (usually bytes) that filing system uses.

The `#` itself is mandatory and is parsed by [`eval_channel`](address:BFB5@2?hex) (raising *Missing #* if absent); the handle is evaluated as an integer into IWA (`&2A`).

---

## 2. The lowest level: `BGET#` and `BPUT#`

These are the primitives — one byte each, no interpretation:

- **`BPUT# h, v`** ([`stmt_bput`](address:BF58@2?hex)) evaluates `v`, coerces it to an integer, and calls `OSBPUT` with the low byte in `A` and the handle in `Y`.
- **`=BGET# h`** ([`fn_bget`](address:BF6F@2?hex)) calls `OSBGET` (handle in `Y`) and returns the byte as an integer.

Everything in §3 is built out of these.

---

## 3. `PRINT#` / `INPUT#`: a type-tagged, byte-reversed record format

This is the part that surprises people, and the reason data files written on a BBC are awkward to read on anything else.

### 3.1 What `PRINT#` actually emits

[`print_file`](address:8D2B@2?hex) ignores all of screen `PRINT`'s formatting — there is no `TAB`, no `~`, no `;`/`'` handling. It simply walks a **comma-separated** value list ([`print_file_loop`](address:8D30@2?hex), which loops only while the next character is `,`), and for each value writes a **type tag** byte followed by the value's bytes:

| First byte (tag) | Type | Then | Order |
|------------------|------|------|-------|
| `&40`            | integer | 4 bytes from IWA | **MSB first** ([`print_file_int_loop`](address:8D4D@2?hex), `LDX #3 … DEX`) |
| `&FF` (negative) | real | 5 packed FP bytes | **MSB first** ([`print_file_real`](address:8D57@2?hex), `LDX #4 … DEX`) |
| `&00`            | string | 1 length byte, then the characters | **reversed** ([`print_file_str`](address:8D64@2?hex), `LDX len … DEX`) |

The tag is BASIC's own internal type code for the value (`zp_var_type`, `&27`): `0` string, `&40` integer, `&FF` real. The disassembly's own inline comments name the quirk outright — [`&8D52`](address:8D52@2?hex) "next byte (MSB first)" and [`&8D72`](address:8D72@2?hex) "next character (written in reverse)".

### 3.2 Worked examples

```
PRINT#h, &12345678        ->  40 12 34 56 78
                              tag  ── value, high byte first ──
                              (IWA holds 78 56 34 12 little-endian;
                               written +3,+2,+1,+0)

PRINT#h, "AB"             ->  00 02 42 41
                              tag len 'B' 'A'   (characters reversed)

PRINT#h, 42               ->  40 00 00 00 2A    (an integer, NOT "42")
```

### 3.3 Why "reversed"

It is not a deliberate wire format so much as a consequence of the copy loops: each value is emitted by a single down-counting loop (`LDX #count … DEX`), so the highest-indexed byte goes out first. The numbers therefore land big-endian (the reverse of the 6502's native little-endian), and a string lands last-character-first.

The point is that **`INPUT#` undoes it by counting down too**, so the asymmetry cancels:

- [`inputf_skip_hash`](address:B9CF@2?hex) reads the tag byte ([`&B9F6`](address:B9F6@2?hex)) and checks it against the target variable's type (raising *Type mismatch* otherwise).
- An integer is read with `LDX #3 … STA zp_iwa,x … DEX` ([`inputf_int_loop`](address:BA21@2?hex)) — the first byte off the file lands in `iwa+3`, restoring little-endian.
- A real likewise into `fp_temp1+4…+0` then unpacked ([`inputf_real`](address:BA2B@2?hex)).
- A string reads the length, then `STA strbuf_base,x … DEX` ([`inputf_read_loop`](address:BA0A@2?hex)) — the inline comment reads "into the buffer (reversed)" — so the original character order is recovered.

So `PRINT#` and `INPUT#` are exact mirror images, and the on-disc bytes are an implementation detail neither side ever has to reason about. The practical consequences for anyone *outside* BASIC:

- A file written by `PRINT#` is only sanely read by `INPUT#`. To consume one elsewhere you must parse the tag bytes and **byte-reverse** each field (and reverse string characters).
- `PRINT#` and `INPUT#` must agree on the value types in order — `INPUT#` validates the tag and errors on a mismatch; it does not coerce.
- Mixing `BPUT#`/`BGET#` (raw bytes) with `PRINT#`/`INPUT#` (tagged records) on the same file means tracking the tag/length framing yourself.

---

## 4. Position and extent: `PTR#`, `EXT#`, `EOF#`

The sequential pointer and the file length are 32-bit values handled by `OSARGS`, which transfers a 4-byte quantity through a zero-page address in `X` — BASIC uses IWA (`&2A`):

- **`PTR# h = n`** ([`stmt_ptr`](address:BF30@2?hex)) — `OSARGS` `A=1`, `X=&2A`, `Y=handle`: set the sequential pointer.
- **`=PTR# h`** ([`fn_ptr`](address:BF47@2?hex)) — `OSARGS` `A=0`: read it.
- **`=EXT# h`** ([`fn_ext`](address:BF46@2?hex)) — `OSARGS` `A=2`: read the extent (length). `fn_ext` and `fn_ptr` share code, selecting the `OSARGS` sub-function from the carry flag.
- **`=EOF# h`** ([`fn_eof`](address:ACB8@2?hex)) — *not* `OSARGS`: it calls `OSBYTE &7F`, which returns end-of-file status in `X` (`0` = at EOF), and BASIC turns that into `TRUE`/`FALSE`.

Setting `PTR#` allows random access on an `OPENUP` channel; `BGET#`/`BPUT#` then operate at that position and advance it.

---

## 5. Routine reference

| Concern | Label | Address |
|---|---|---|
| `#channel` parser (shared) | [`eval_channel`](address:BFB5@2?hex) | `&BFB5` |
| `OPENIN`/`OPENOUT`/`OPENUP` (shared open) | [`openup_action`](address:BF82@2?hex) | `&BF82` |
| `CLOSE` | [`stmt_close`](address:BF99@2?hex) | `&BF99` |
| `BPUT#` | [`stmt_bput`](address:BF58@2?hex) | `&BF58` |
| `=BGET#` | [`fn_bget`](address:BF6F@2?hex) | `&BF6F` |
| `PRINT#` writer | [`print_file`](address:8D2B@2?hex) | `&8D2B` |
| — integer / real / string payload | [`print_file_int_loop`](address:8D4D@2?hex) / [`print_file_real`](address:8D57@2?hex) / [`print_file_str`](address:8D64@2?hex) | `&8D4D` / `&8D57` / `&8D64` |
| `INPUT#` reader | [`inputf_skip_hash`](address:B9CF@2?hex) | `&B9CF` |
| — integer / real / string payload | [`inputf_int_loop`](address:BA21@2?hex) / [`inputf_real`](address:BA2B@2?hex) / [`inputf_read_loop`](address:BA0A@2?hex) | `&BA21` / `&BA2B` / `&BA0A` |
| `PTR#=` / `=PTR#` / `=EXT#` | [`stmt_ptr`](address:BF30@2?hex) / [`fn_ptr`](address:BF47@2?hex) / [`fn_ext`](address:BF46@2?hex) | `&BF30` / `&BF47` / `&BF46` |
| `=EOF#` | [`fn_eof`](address:ACB8@2?hex) | `&ACB8` |

> **See also:** whole-program loading (`LOAD`/`SAVE`/`CHAIN`) uses `OSFILE` and the 18-byte control block, not channels — see the [`load_program`](address:BE62@2?hex) banner. The control-flow and value stacks that hold evaluated values during `PRINT#`/`INPUT#` are covered in [Control flow on five stacks](control-flow-stacks.md).
