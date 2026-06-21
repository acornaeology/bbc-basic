# Tokenising and de-tokenising BBC BASIC II: the keyword table, the crunch, and LIST

> **Scope.** This article describes **BBC BASIC II** — the 16 KB language ROM of the BBC Micro. Every token value, flag bit, table address, and ROM entry point below is specific to this version and was read directly from the disassembly (which reassembles byte-identically to the original ROM). BASIC IV (Master) keeps the same scheme but moves the addresses; BASIC V (Archimedes / ARM) uses a different, multi-byte token scheme. Treat the *mechanism* as portable and the *values* as version II only.

Everything here is derived from three routines and one table:

| Thing                         | Label                                                                      | Address         |
|-------------------------------|----------------------------------------------------------------------------|-----------------|
| Keyword / token / flag table  | [`keyword_table`](address:8071@2?hex)                                      | `&8071`–`&836C` |
| Tokeniser ("crunch")          | [`tokenise_line`](address:8951@2?hex) / [`tok_scan`](address:8957@2?hex)   | `&8951`         |
| Line-number reference encoder | [`encode_line_number`](address:88F5@2?hex)                                 | `&88F5`         |
| Line-number reference decoder | [`decode_line_number`](address:97EB@2?hex)                                 | `&97EB`         |
| De-tokeniser (token → text)   | [`print_token`](address:B50E@2?hex)                                        | `&B50E`         |
| `LIST` line walker            | [`stmt_list`](address:B59C@2?hex) / [`list_char_loop`](address:B639@2?hex) | `&B59C`         |

---

## 1. The keyword / token table

### 1.1 Structure

The table at [`keyword_table`](address:8071@2?hex) is a flat byte stream of variable-length entries. Each entry is:

```
<keyword ASCII, all bytes < &80> <token byte, bit 7 set> <flag byte>
```

There are no length prefixes and no separators: a scanner reads ASCII characters until it hits a byte with bit 7 set (the **token**), and the byte after that is the **flag**. The table runs from `&8071` up to [`action_table_lo`](address:836D@2?hex) at `&836D`. It holds **126 entries**.

### 1.2 The complete table, in ROM (scan) order

`token` is the byte produced/recognised; `flag` drives tokenising (§2.1); `bits` is the flag in binary (`76543210`); `@addr` is where the entry begins.

```
token keyword    flag bits        @addr     
80    AND        00  00000000     @8071     
94    ABS        00  00000000     @8076     
95    ACS        00  00000000     @807B     
96    ADVAL      00  00000000     @8080     
97    ASC        00  00000000     @8087     
98    ASN        00  00000000     @808C     
99    ATN        00  00000000     @8091     
C6    AUTO       10  00010000     @8096     
9A    BGET       01  00000001     @809C     
D5    BPUT       03  00000011     @80A2     
FB    COLOUR     02  00000010     @80A8     
D6    CALL       02  00000010     @80B0     
D7    CHAIN      02  00000010     @80B6     
BD    CHR$       00  00000000     @80BD     
D8    CLEAR      01  00000001     @80C3     
D9    CLOSE      03  00000011     @80CA     
DA    CLG        01  00000001     @80D1     
DB    CLS        01  00000001     @80D6     
9B    COS        00  00000000     @80DB     
9C    COUNT      01  00000001     @80E0     
DC    DATA       20  00100000     @80E7     
9D    DEG        00  00000000     @80ED     
DD    DEF        00  00000000     @80F2     
C7    DELETE     10  00010000     @80F7     
81    DIV        00  00000000     @80FF     
DE    DIM        02  00000010     @8104     
DF    DRAW       02  00000010     @8109     
E1    ENDPROC    01  00000001     @810F     
E0    END        01  00000001     @8118     
E2    ENVELOPE   02  00000010     @811D     
8B    ELSE       14  00010100     @8127     
A0    EVAL       00  00000000     @812D     
9E    ERL        01  00000001     @8133     
85    ERROR      04  00000100     @8138     
C5    EOF        01  00000001     @813F     
82    EOR        00  00000000     @8144     
9F    ERR        01  00000001     @8149     
A1    EXP        00  00000000     @814E     
A2    EXT        01  00000001     @8153     
E3    FOR        02  00000010     @8158     
A3    FALSE      01  00000001     @815D     
A4    FN         08  00001000     @8164     
E5    GOTO       12  00010010     @8168     
BE    GET$       00  00000000     @816E
A5    GET        00  00000000     @8174
E4    GOSUB      12  00010010     @8179
E6    GCOL       02  00000010     @8180
93    HIMEM      43  01000011     @8186
E8    INPUT      02  00000010     @818D
E7    IF         02  00000010     @8194
BF    INKEY$     00  00000000     @8198
A6    INKEY      00  00000000     @81A0
A8    INT        00  00000000     @81A7
A7    INSTR(     00  00000000     @81AC
C9    LIST       10  00010000     @81B4
86    LINE       00  00000000     @81BA
C8    LOAD       02  00000010     @81C0
92    LOMEM      43  01000011     @81C6
EA    LOCAL      02  00000010     @81CD
C0    LEFT$(     00  00000000     @81D4
A9    LEN        00  00000000     @81DC
E9    LET        04  00000100     @81E1
AB    LOG        00  00000000     @81E6
AA    LN         00  00000000     @81EB
C1    MID$(      00  00000000     @81EF
EB    MODE       02  00000010     @81F6
83    MOD        00  00000000     @81FC
EC    MOVE       02  00000010     @8201
ED    NEXT       02  00000010     @8207
CA    NEW        01  00000001     @820D
AC    NOT        00  00000000     @8212
CB    OLD        01  00000001     @8217
EE    ON         02  00000010     @821C
87    OFF        00  00000000     @8220
84    OR         00  00000000     @8225
8E    OPENIN     00  00000000     @8229
AE    OPENOUT    00  00000000     @8231
AD    OPENUP     00  00000000     @823A
FF    OSCLI      02  00000010     @8242
F1    PRINT      02  00000010     @8249
90    PAGE       43  01000011     @8250
8F    PTR        43  01000011     @8256
AF    PI         01  00000001     @825B
F0    PLOT       02  00000010     @825F
B0    POINT(     00  00000000     @8265
F2    PROC       0A  00001010     @826D
B1    POS        01  00000001     @8273
F8    RETURN     01  00000001     @8278
F5    REPEAT     00  00000000     @8280
F6    REPORT     01  00000001     @8288
F3    READ       02  00000010     @8290
F4    REM        20  00100000     @8296
F9    RUN        01  00000001     @829B
B2    RAD        00  00000000     @82A0
F7    RESTORE    12  00010010     @82A5
C2    RIGHT$(    00  00000000     @82AE
B3    RND        01  00000001     @82B7
CC    RENUMBER   10  00010000     @82BC
88    STEP       00  00000000     @82C6
CD    SAVE       02  00000010     @82CC
B4    SGN        00  00000000     @82D2
B5    SIN        00  00000000     @82D7
B6    SQR        00  00000000     @82DC
89    SPC        00  00000000     @82E1
C3    STR$       00  00000000     @82E6
C4    STRING$(   00  00000000     @82EC
D4    SOUND      02  00000010     @82F6
FA    STOP       01  00000001     @82FD
B7    TAN        00  00000000     @8303
8C    THEN       14  00010100     @8308
B8    TO         00  00000000     @830E
8A    TAB(       00  00000000     @8312
FC    TRACE      12  00010010     @8318
91    TIME       43  01000011     @831F
B9    TRUE       01  00000001     @8325
FD    UNTIL      02  00000010     @832B
BA    USR        00  00000000     @8332
EF    VDU        02  00000010     @8337
BB    VAL        00  00000000     @833C
BC    VPOS       01  00000001     @8341
FE    WIDTH      02  00000010     @8347
── end of tokeniser scan (WIDTH's &FE = sentinel) ──
D0    PAGE       00  00000000     @834E
CF    PTR        00  00000000     @8354
D1    TIME       00  00000000     @8359
D2    LOMEM      00  00000000     @835F
D3    HIMEM      00  00000000     @8366
```

### 1.3 Token range and "no multi-byte tokens" (Q2)

**Confirmed: the token range is `&80`–`&FF`, single byte, no extended/prefix tokens.** Every token byte in the table has bit 7 set; the tokeniser emits exactly one byte per keyword (plus the special 3-byte line-number form, §3). BASIC II has **nothing** like BASIC V's `&C6`/`&C7`/`&C8` two-byte prefixes — in *this* ROM `&C6`/`&C7`/`&C8` are the ordinary keywords `AUTO`/`DELETE`/`LOAD`. Two byte values in `&80`–`&FF` are **not** keyword tokens:

- **`&8D`** — the **line-number token** (§3). It is not in the table; it is produced by the tokeniser and special-cased by `LIST`.
- **`&CE`** — an **unused gap**. No keyword and no handler ([`disasm_basic_2.py:727`](address:8071@2?hex) notes "Token &CE: unused gap").

### 1.4 The version-sensitive keywords (Q3)

These are the BASIC **II** values — use them, not a BASIC I table:

| Keyword | Token(s) | Notes |
|---|---|---|
| `OPENIN`  | `&8E` | function form only |
| `OPENOUT` | `&AE` | |
| `OPENUP`  | `&AD` | |
| `PTR`     | `&8F` (function) / `&CF` (assignment target) | pseudo-variable, see §1.6 |
| `PAGE`    | `&90` / `&D0` | pseudo-variable |
| `TIME`    | `&91` / `&D1` | pseudo-variable |
| `LOMEM`   | `&92` / `&D2` | pseudo-variable |
| `HIMEM`   | `&93` / `&D3` | pseudo-variable |

### 1.5 Tokens that only one side uses (Q4)

The scheme is *almost* perfectly symmetric, with two wrinkles:

1. **`&8D` (line number)** is produced by the tokeniser and consumed by `LIST`, so it is used by both — but it is special-cased on both sides (it is not a table entry; the tokeniser builds it in [`parse_decimal_u16`](address:8897@2?hex)/`encode_line_number`, and `LIST` intercepts it before `print_token` at [`&B655`](address:B655@2?hex)).

2. **The five assignment-form tokens `&CF`–`&D3`** (`PTR=`,`PAGE=`,`TIME=`,`LOMEM=`,`HIMEM=`) are *produced* by the tokeniser arithmetically (bit 6, §1.6) but their **table entries are reachable only by the de-tokeniser**. The tokeniser stops scanning at `WIDTH`'s token `&FE`, which doubles as the table-end sentinel (see [`&8A12`](address:8A12@2?hex): `cmp #&fe` → give up). The five `&CF`–`&D3` entries sit *after* `WIDTH`, so the crunch never matches them; they exist purely so `print_token` can render `PTR=` etc. back to text.

### 1.6 Pseudo-variables and the `&40` trick

`PTR`, `PAGE`, `TIME`, `LOMEM`, `HIMEM` each have flag `&43` (bits 0, 1, 6). **Bit 6** means: *if this keyword is tokenised at the start of a statement, add `&40` to the token byte* ([`&8A4D`–`&8A53`](address:8A4D@2?hex)). So the same source word produces two different tokens by context:

- `X = PTR#3` → function position → token `&8F`
- `PTR#3 = X` → statement start (assignment target) → token `&8F + &40 = &CF`

That is why the table carries the keyword twice — once at the function token (`&8F`–`&93`, scanned by the crunch) and once at the assignment token (`&CF`–`&D3`, used only by `LIST`).

### 1.7 `TOP` is *not* a keyword — the `TO`+`P` trap

`TOP` (the top-of-program pseudo-variable) looks like it belongs with the pseudo-variables above, but it is the odd one out: **it has no table entry, no token, and no flag bits.** The table holds `TO` (`&B8`, flag `&00`) and nothing beginning `TOP`. `TOP` is recognised purely at *run time*.

This matters because `TO` is **not** conditional (flag `&00`, no bit 0), so it tokenises at a name-run start even when a name character follows (§2.2). So the crunch turns the source `TOP` into the two bytes `[TO]` + `'P'` — the `TO` token followed by a literal ASCII `P` left in the line as ordinary name text. There is no longest-match step that could ever produce a `TOP` token, because no such token exists. A tokeniser that carries `TOP` as a keyword and does longest-match will mis-split `FORi=0TOPI*2` as `… 0 TOP I …`; the ROM produces `… 0 TO PI …` (`PI` = `&AF`), because at the run-start after the digit `0` the crunch matches `TO`, resumes at `PI`, and matches that.

At run time, when the evaluator dispatches the `TO` token *as a value* it calls [`fn_to`](address:AEDC@2?hex) (`&AEDC`), which peeks the **immediately following byte**: if it is ASCII `'P'` (`&50`) it consumes it and returns [`zp_top`](address:0012@2?hex) (`&12/&13`); anything else is a syntax error. So:

- `PRINT TOP` → `[PRINT][TO]'P'` → `fn_to` sees `'P'` → top-of-program. (No space-skip: `TO P` with a space is *not* `TOP`.)
- `0TOPI` → `[TO][PI]` → the byte after `TO` is the `PI` token `&AF`, not `'P'`, so this is never read as `TOP` — and in a `FOR` the `TO` is the loop separator anyway ([`stmt_for`](address:B7C4@2?hex) requires `&B8` at `&B7ED`), so `fn_to` never runs.

For a faithful tokeniser: do **not** list `TOP` as a keyword; emit `TO` wherever it matches at a run start; and recognise the `TOP` pseudo-variable only at expression-evaluation time, as a `TO` token immediately followed by a bare `P`.

---

## 2. Flag bits and the crunch algorithm

### 2.1 What each flag bit means (Q5)

Read straight from [`tok_kw_found`](address:8A37@2?hex) onward, the flag byte is processed bit-by-bit (`LSR` walks bits 0→5; bit 6 is tested with `BIT`):

| Bit | Mask  | Meaning                                                                                                                                                            | Code                          |
|-----|-------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------|
| 0   | `&01` | **Conditional**: if the character *after* the matched keyword is a name character (`is_alphanumeric`), do **not** tokenise — keep it as part of a name/identifier. | [`&8A3E`](address:8A3E@2?hex) |
| 1   | `&02` | Enter **middle-of-statement** mode (set state flag `&3B = &FF`; clear `&3C`).                                                                                      | [`&8A5E`](address:8A5E@2?hex) |
| 2   | `&04` | Enter **start-of-statement** mode (set `&3B = 0`; clear `&3C`).                                                                                                    | [`&8A66`](address:8A66@2?hex) |
| 3   | `&08` | **FN/PROC**: do not tokenise the following name (skip the identifier whole).                                                                                       | [`&8A6D`](address:8A6D@2?hex) |
| 4   | `&10` | **Start a line number**: set the line-number flag `&3C = &FF` so the next decimal literal is encoded with the `&8D` token.                                         | [`&8A81`](address:8A81@2?hex) |
| 5   | `&20` | **Stop tokenising the rest of the line** (`REM`, `DATA`): return from the crunch immediately.                                                                      | [`&8A86`](address:8A86@2?hex) |
| 6   | `&40` | **Pseudo-variable**: if at statement start, add `&40` to the token (assignment form).                                                                              | [`&8A49`](address:8A49@2?hex) |
| 7   | —     | unused (no flag byte exceeds `&43`).                                                                                                                               |                               |

Mapping the questions:

- *"following operand is a line number"* → **bit 4**. Keywords: `AUTO`, `DELETE`, `ELSE`, `GOSUB`, `GOTO`, `LIST`, `RENUMBER`, `RESTORE`, `THEN`, `TRACE` (every entry whose flag ANDs `&10`).
- *"stop tokenising the rest of the line"* → **bit 5**: `REM` and `DATA` only. **`*` is *not* bit 5** — it is handled separately (§2.5) and also stops tokenising, but by a different path.
- *"start-of-statement"* → **bit 2** sets that *state*: `THEN`, `ELSE` (`&14` = bits 2+4), `ERROR`, `LET` (`&04`). There is no "this token is legal only at statement start" flag; statement-vs-function dispatch happens later, at *run* time, in [`next_statement`](address:8BA3@2?hex)/[`dispatch_token`](address:8BB1@2?hex) by token value (`< &CF` ⇒ assignment, `>= &C6` ⇒ command).
- *"pseudo-variable"* → **bit 6** (§1.6).
- *"conditional"* → **bit 0**: suppress the token when a name character follows, so `END` inside `ENDOWMENT` (a variable) is not tokenised, and `TIME` in `TIMER` stays a name.

### 2.2 Matching strategy: first full match in table order (Q6)

The crunch does **not** do longest-match, and it does not do plain prefix-match. For the character at the cursor it scans entries **in table order** ([`tok_try_keyword`](address:89EC@2?hex)):

1. The table is grouped by ascending first letter. If an entry's first letter is **greater** than the cursor letter, give up — it's a name (`BCC` at [`&89FA`](address:89FA@2?hex)). (There are no keywords past `W`; `X`/`Y`/`Z` and all lowercase short-circuit to "name" at [`&89EC`](address:89EC@2?hex).)
2. Otherwise compare the **whole** keyword character-by-character ([`tok_kw_match_loop`](address:89FE@2?hex)). A full match (next table byte has bit 7 set) → emit that token.
3. A character mismatch → if the cursor character is `.`, accept the abbreviation (§2.3); else advance to the next entry and retry.

Because matching is *exact and full*, table order is what guarantees correctness for shared prefixes. **`INPUT` vs `INT`:** `INPUT` (`&E8`) appears before `INT` (`&A8`); source `INPUT` matches `INPUT` fully on the first try, source `INT` fails `INPUT`/`IF`/`INKEY$`/`INKEY` in turn (each a full-compare mismatch) and then matches `INT` exactly. No prefix shadows another because the comparison always runs to the end of the keyword unless a `.` intervenes.

**Where matching is even attempted — name-run starts only.** The scan above runs *only at the first character of a run of name characters* (`0-9 A-Z a-z _`, per `is_alphanumeric`). A run begins at the start of the line and after any non-name character (space, operator, `=`, punctuation, a digit) or an emitted token. If that first character does **not** yield a surviving keyword, control falls to [`tok_name`](address:89D0@2?hex)/[`tok_name_loop`](address:89D2@2?hex), which swallows the **entire** rest of the run as one identifier and **never re-attempts keyword matching inside it**. So a keyword that begins *partway* through a run is never tokenised:

- `GDIV40`, `GONE`, `STORE`, `SANDY`, `XPRINT` all stay **literal** — the interior `DIV`/`ON`/`TO`/`AND`/`PRINT` is never looked at, because the run was already claimed as a name at its first letter. (Insert a boundary and it tokenises: `G DIV40` → `G·[DIV]·40`.)

When a keyword *is* emitted at a run start, the scanner resumes at the next character, which is itself a fresh run start — so abutting keywords each tokenise: `DIVMOD` → `[DIV][MOD]`, `TOPRINT` → `[TO][PRINT]`. And a surviving leading keyword tokenises even with an identifier tail: `TOTAL` → `[TO]TAL`, `PRINTX` → `[PRINT]X`, `FORM` → `[FOR]M`, `INPUTS` → `[INPUT]S`.

The bit-0 *conditional* (§2.1) layers on top, and its effect compounds: a run-start keyword with bit 0 set is suppressed when a name character follows, and *because suppression hands the whole run to `tok_name`*, any keyword abutting it is skipped too. So `TIMER`, `TRUER`, `TRUEELSE`, `TIMEPRINT`, `FALSEAND`, `ENDPROCPRINT` are **all literal** (the second keyword is never reached), whereas `TRUE+`, `TIME=0` and `=TRUE ELSE=` tokenise — the character after the conditional keyword is not a name character. This is the rule to verify a tokeniser against: keywords match at run starts only, and a suppressed conditional swallows everything to the end of the run.

### 2.3 Abbreviations: prefix + `.`, first table entry wins (Q7)

There is **no per-keyword minimum length**. The rule is *any prefix that, in table order, first reaches a `.`* ([`tok_kw_abbrev`](address:8A18@2?hex)): during the full-compare, a character mismatch where the **source** character is `.` is accepted, and the scan jumps to that entry's token. The dot is consumed.

The winner on a shared prefix is therefore **the first table entry the typed letters match**. Examples (`P` group order is `PRINT, PAGE, PTR, PI, PLOT, POINT(, POS, PROC`):

- `P.` → `PRINT` (first `P` entry)
- `PR.` → `PRINT` (still matches `PRINT` before `PROC`; the `.` lands after `P,R`)
- `PRO.` → `PROC` (`PRINT` now mismatches at `O` vs `I` with no dot, so the scan reaches `PROC`)
- `PT.` → `PTR`

The curated table order is exactly what makes "the shortest unambiguous abbreviation" resolve correctly; the driver banner at [`keyword_table`](address:8071@2?hex) notes the entries are "ordered so that the first acceptable abbreviation of each keyword is unambiguous."

A leading `.` with **no** preceding letter is not an abbreviation — it is treated as the start of a number (e.g. `.5`), see [`&89A3`](address:89A3@2?hex).

### 2.4 The start-of-statement state machine (Q8)

Two zero-page bytes hold the crunch state:

- **`&3B`** (`zp_fwb_sign`): `0` = start of statement, `&FF` = middle of statement.
- **`&3C`** (`zp_fwb_ovf`): the **"next number is a line number"** flag (`&FF` = encode the next literal with `&8D`). Its only role in the crunch is line-number arming — string handling does not use it. (`&3C` is a much-reused scratch byte elsewhere; `LIST`'s own quote-state flag, by contrast, lives at `&4D`.)

`&3B` is reset to **start of statement** by:

- line start — [`tokenise_line`](address:8951@2?hex) sets `&3B = 0` (and the immediate-mode entry [`execute_line`](address:8B0B@2?hex) does likewise before [`tok_scan`](address:8957@2?hex));
- a `:` statement separator — [`tok_check_colon`](address:898C@2?hex) sets `&3B = 0`, `&3C = 0`;
- flag **bit 2** — `THEN` and `ELSE` (so the text after them begins a fresh statement).

`&3B` is set to **middle of statement** by: flag **bit 1** (most commands), and by reading a name ([`tok_not_keyword`](address:89E3@2?hex)/[`tok_resume_mid`](address:89C2@2?hex)) or a number. Note a **comma does not reset** the state ([`tok_check_comma_star`](address:8996@2?hex) just skips it) — that is deliberate, so `ON X GOTO 10,20,30` keeps `&3C` armed and encodes every number in the list as a line number.

There is no "recognised only at statement start" *class* of keywords in the crunch — a keyword tokenises at any name-run start where it survives (§2.2), regardless of statement position (subject to bit 0 / bit 6). The start/mid distinction only changes pseudo-variable tokens (bit 6) and line-number arming.

### 2.5 Suppression contexts — where tokenising turns off, and resumes (Q9)

| Context               | Entry                                        | Behaviour                                                                                  | Resumes                                                                                  |
|-----------------------|----------------------------------------------|--------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------|
| String literal `"…"`  | [`tok_check_string`](address:897C@2?hex)     | copy bytes verbatim through the closing `"`                                                | after the closing quote                                                                  |
| Unterminated string   | [`&8987`](address:8987@2?hex)                | if `CR` is hit before a closing `"`, **return** — the rest of the line stays literal       | (line ends)                                                                              |
| After `REM` / `DATA`  | flag bit 5, [`&8A86`](address:8A86@2?hex)    | **return** from the crunch — rest of line literal                                          | not until next line (`:` does **not** resume — colons are part of the `DATA`/`REM` text) |
| Statement-leading `*` | [`&899A`](address:899A@2?hex)                | at statement start (`&3B = 0`) → **return**, rest of line literal (`*command` for `OSCLI`) | (line ends)                                                                              |
| Mid-statement `*`     | same                                         | when `&3B ≠ 0`, `*` is the multiply operator — *not* suppression; scanning continues       | —                                                                                        |
| `&`-hex constant      | [`tok_check_hex`](address:8966@2?hex)        | copy `&` and the run of hex digits `0-9 A-F` verbatim                                      | after the hex digits                                                                     |
| Plain number          | [`tok_skip_number_loop`](address:89B5@2?hex) | digit/`.` runs copied verbatim (unless line-number-armed, §3)                              | after the number                                                                         |

**`DATA` is left literal to end-of-line**, colons included — bit 5 returns from the whole crunch, so `DATA 1,2:X` stores `:X` as data text (matching the runtime `DATA` handler [`stmt_data`](address:8B7D@2?hex), which also scans to `CR`).

### 2.6 After `FN` / `PROC` (Q10)

`FN` (flag `&08`, bit 3) and `PROC` (flag `&0A`, bits 1+3) set the FN/PROC bit, which makes the crunch **skip the following identifier without tokenising it** ([`tok_skip_fnproc_loop`](address:8A72@2?hex)). The name is delimited by `is_alphanumeric` — it runs while characters are `0-9 A-Z a-z _` and stops at the first non-name character. So `PROCEND` is *not* split (the `END` is consumed as part of the procedure name), and `PROCdraw_box(x)` skips `draw_box` and resumes tokenising at `(`. Only the **one** identifier immediately after `FN`/`PROC` is protected.

### 2.7 Case sensitivity (Q11)

**Confirmed: only uppercase `A`–`W` initiate keyword matching; lowercase never tokenises.** The dispatch at [`tok_check_letter`](address:89DF@2?hex) requires `>= 'A'`, then [`tok_try_keyword`](address:89EC@2?hex) rejects anything `>= 'X'` — which includes all lowercase (`'a'` = `&61` ≥ `'X'` = `&58`). Lowercase letters are consumed as name characters. And the inner compare ([`&8A03`](address:8A03@2?hex)) is an exact byte comparison against the uppercase table text, so even reaching it, a lowercase byte cannot match.

---

## 3. Line-number encoding (Q12, Q13)

### 3.1 The three-byte `&8D` form

A referenced line number is stored as **`&8D` then three bytes**. The point of the encoding is that none of the three bytes can collide with `&0D` (the line terminator) or stray into token range — they are lifted into `&40`–`&FF` and the four "dangerous" high bits are gathered into one scrambled control byte. The exact transform, from [`encode_line_number`](address:88F5@2?hex), for a 16-bit line number with low byte `LO` and high byte `HI`:

```
byte1 (control) = ( ((LO & 0xC0) | ((HI & 0xC0) >> 2)) >> 2 ) ^ 0x54
byte2           = (LO & 0x3F) | 0x40
byte3           = HI | 0x40
```

So the stored reference is `8D <byte1> <byte2> <byte3>`. The `^ 0x54` (`EOR #&54` at [`&8915`](address:8915@2?hex)) is the "scramble" that keeps the control byte clear of `&0D`/`&8D`.

The inverse, from [`decode_line_number`](address:97EB@2?hex) (`LIST` and the program editor both use it):

```
t  = control << 2          ; 8-bit
LO = (t & 0xC0) ^ byte2
HI = (t << 2) ^ byte3      ; i.e. (control << 4) ^ byte3
```

**Verified by simulation against the ROM logic:** this round-trips exactly for line numbers **0–32767**, and **no** encoded byte ever equals `&0D` across the whole range. For values ≥ 32768 the codec does *not* round-trip (the high bit is lost), which is the mechanism behind the 32767 line-number ceiling (§5.2). Worked examples:

```
line     1 -> 8D 54 41 40
line    10 -> 8D 54 4A 40
line   100 -> 8D 44 64 40
line  1000 -> 8D 64 68 43
line 32767 -> 8D 60 7F 7F
```

### 3.2 What arms line-number encoding (Q13)

A following decimal literal is encoded as a line number **only when the crunch is "armed"** — i.e. flag bit 4 set `&3C = &FF` and it has not yet been cleared. The arming keywords are exactly the bit-4 set:

> `AUTO`, `DELETE`, `ELSE`, `GOSUB`, `GOTO`, `LIST`, `RENUMBER`, `RESTORE`, `THEN`, `TRACE`

The qualification rule, from [`tok_check_number`](address:89A3@2?hex):

- The literal must be an **immediate unsigned decimal run** (`0`–`9`). Leading **spaces are allowed** (the scanner skips spaces without disarming, [`tok_scan`](address:8957@2?hex)).
- A **sign or any non-digit disarms**: `-`, `+`, `.`, or a letter routes through [`tok_check_letter`](address:89DF@2?hex)/[`tok_not_keyword`](address:89E3@2?hex), which clears `&3C`. So `GOTO -5` does **not** line-number-encode the `5`, and `GOTO X` (a computed line, `GOTO` of a variable) leaves `X` as an ordinary name.
- `&3C` stays armed across commas but not across `:`/identifiers, so `RESTORE 100,200`-style lists encode each literal, while `THEN PRINT` (bit 2 also set) drops straight into a new statement.

The leading line number of a program line you type uses the *same* `&8D` machinery: immediate mode ([`execute_line`](address:8B0B@2?hex)) pre-arms `&3C = &FF`, so the first number on the line is encoded; [`check_line_number`](address:97DF@2?hex) then decodes it back and that value becomes the stored 2-byte line number (§5.1). `AUTO` and `RENUMBER` reuse `encode_line_number` directly ([`&906A`](address:906A@2?hex)).

---

## 4. De-tokenising / `LIST`

### 4.1 Is `LIST` a pure inverse? (Q14)

Essentially yes for the body. `print_token` ([`&B50E`](address:B50E@2?hex)) maps a token byte back to its keyword text and **adds no spaces of its own**; bytes `< &80` are printed as-is. The `LIST` line walker ([`list_char_loop`](address:B639@2?hex)) inserts no cosmetic spacing around tokens either — the only spacing it adds is **LISTO** indentation (§4.2). The tokeniser likewise *preserves spaces verbatim* (spaces are skipped over but left in the stored line), so:

```
detokenise(tokenise("PRINT X"))  ==  "PRINT X"     (whitespace preserved)
```

The two changes that make the round-trip **not** byte-identical in source text are:

1. **Abbreviations are expanded** — `P.` tokenises to the `PRINT` token, which `LIST`s as `PRINT`.
2. With default `LISTO 0`, the leading line number is printed right-justified in a **5-character field** (see §4.3), so column alignment differs from what you typed.

Round-trip tests should compare *tokenised bytes*, not source text, except where abbreviations are involved.

### 4.2 LISTO indentation and quote tracking

`LIST` ([`stmt_list`](address:B59C@2?hex)) walks each line byte-by-byte. It maintains its own **quote flag** (`&4D`, toggled at [`&B643`](address:B643@2?hex)); while inside a quoted string every byte is printed **literally** with no de-tokenising. Outside quotes:

- `&8D` → decode + print the line number (§4.3);
- `FOR`/`NEXT`/`REPEAT`/`UNTIL` adjust the two LISTO indent counters (`&3B`,`&3C`);
- everything else → `print_token`.

LISTO (`&1F`, default **0**, set by [`stmt_listo`](address:B58A@2?hex), via [`print_listo_indent`](address:B577@2?hex)) bits, matching the User Guide:

| LISTO bit | Value | Effect |
|---|---|---|
| 0 | 1 | one space after the line number |
| 1 | 2 | indent `FOR…NEXT` bodies (2 spaces per level) |
| 2 | 4 | indent `REPEAT…UNTIL` bodies (2 spaces per level) |

At the default `LISTO 0`, **none** of these apply.

### 4.3 How `LIST` renders line numbers (Q15)

Two different renderings, both via the decimal formatter [`print_line_number`](address:991F@2?hex) (leading-zero-suppressed, units always shown, no trailing space):

- **The line's own number** (start of each listed line) is printed in a **5-character right-justified field** ([`list_print_num`](address:B61D@2?hex) → [`trace_print_number`](address:9923@2?hex), width 5): `    1`, `   10`, `  100`, `32767`.
- **An embedded line-number reference** (`&8D`, after `GOTO` etc.) is printed as **plain decimal, no padding** ([`&B65E`](address:B65E@2?hex), width 0).

### 4.4 Any token whose `LIST`ed spelling differs from what tokenises to it? (Q16)

No. `print_token` prints the literal table text of whichever entry holds that token byte, so a token always `LIST`s as a spelling that re-tokenises to the same token. The pseudo-variable assignment forms are the case to watch, and they are consistent: `&CF` `LIST`s as `PTR` (via the trailing table entry, §1.5), and `PTR` at statement start re-tokenises to `&CF`. The only non-identity is abbreviation expansion (§4.1), which is a property of the *input*, not of any token.

---

## 5. Byte-level layout, limits, and edge cases

### 5.1 One line's storage layout (Q17)

```
&0D  <lineNo-hi>  <lineNo-lo>  <length>  <body…>          (repeat)  …  &0D &FF
```

- `&0D` is the **start-of-line** marker (not an end marker), confirmed by the walkers [`find_program_line`](address:9970@2?hex) and [`list_check_high`](address:B602@2?hex), which read the high byte at offset 1, low byte at offset 2, length at offset 3, body at offset 4.
- The **length byte counts the whole record** — from this `&0D` up to (not including) the next `&0D`. The walkers advance to the next line by *adding the length byte to the line pointer* ([`&9982`–`&9988`](address:9980@2?hex)). So `length = 4 + len(body)`; maximum `255`, giving a maximum body of `251` bytes.
- The line number in the header is a plain 2-byte big-endian-ish pair (`hi` then `lo`), **not** the `&8D` encoding (that form is only for references inside bodies).
- **End-of-program marker:** `&0D &FF` — a line marker followed by `&FF` where the high byte would be. Any high byte `>= &FF` halts the walk ([`find_program_line`](address:997E@2?hex)).
- **Empty program:** exactly `&0D &FF` stored at `PAGE`, with `TOP = PAGE + 2` ([`start_new_program`](address:8ADD@2?hex)).

### 5.2 Line-number range (Q18)

Valid line numbers are **0–32767**:

- `0` is valid (`GOTO 0`, a line numbered `0`).
- `AUTO` stops as soon as the number would exceed 32767 — [`&90D7`](address:90D7@2?hex) `BPL auto_loop` ends the loop when the high bit sets.
- Numbers above 32767 do not survive the `&8D` reference codec (§3.1): both typed leading line numbers and references pass through `encode`/`decode`, which only round-trips ≤ 32767. There is no explicit "line number too big" error — values above the ceiling mis-encode rather than being rejected.

### 5.3 Maximum input line length and overflow (Q19)

A typed line is read by OSWORD 0 into the input buffer at **`&0700`** with a **maximum length of 238 bytes** (`&EE`) and accepted characters in `&20`–`&FF` ([`read_input_line`](address:BC02@2?hex), `LDA #&EE` at [`&BC0D`](address:BC0D@2?hex)). OSWORD 0 enforces the limit (it refuses further characters and only accepts `CR` once at/under the cap). Tokenising happens *in place* afterwards; note it can *grow* a line (a short line reference such as `GOTO 1` expands from 6 source bytes to the 4-byte `&8D` form), so the stored record (capped by the 1-byte length field, §5.1) is the binding limit, not the 238-byte input.

### 5.4 Top-bit-set bytes inside string literals (Q20)

There is no collision, on either side:

- **Tokenise:** inside `"…"` the crunch copies bytes **verbatim** ([`tok_string_loop`](address:8980@2?hex)) — a `&80`–`&FF` byte in a string is stored unchanged and never interpreted as a token.
- **`LIST`:** while its quote flag says "inside a string" ([`&B651`](address:B651@2?hex)), every byte is sent straight to `print_char` with **no** table lookup — so a stored `&C8` inside a string prints as the raw character, *not* as `LOAD`.

The one caveat is the editor, not the codec: you cannot *type* a literal `&0D` (it terminates the line) or a top-bit byte the keyboard/OSWORD won't deliver. But any such byte already present in a tokenised string is round-tripped faithfully.

---

## Appendix: routine cross-reference (Q21)

| Concern | Label / address |
|---|---|
| Keyword/token/flag table | [`keyword_table`](address:8071@2?hex) `&8071`; sentinel = `WIDTH` token `&FE` |
| Action-address tables (token → handler) | [`action_table_lo`](address:836D@2?hex) `&836D`, [`action_table_hi`](address:83DF@2?hex) `&83DF` |
| Crunch entry (line) | [`tokenise_line`](address:8951@2?hex) `&8951`; immediate-mode entry [`execute_line`](address:8B0B@2?hex)→[`tok_scan`](address:8957@2?hex) |
| Keyword match loop | [`tok_try_keyword`](address:89EC@2?hex) `&89EC`, [`tok_kw_found`](address:8A37@2?hex) `&8A37` |
| Flag-bit dispatch | [`tok_emit_token`](address:8A48@2?hex) `&8A48` … [`tok_flag_skipline`](address:8A86@2?hex) `&8A86` |
| Abbreviation accept | [`tok_kw_abbrev`](address:8A18@2?hex) `&8A18` |
| Decimal accumulate + arm | [`parse_decimal_u16`](address:8897@2?hex) `&8897` |
| Line-number encode | [`encode_line_number`](address:88F5@2?hex) `&88F5` |
| Line-number detect/decode | [`check_line_number`](address:97DF@2?hex) `&97DF`, [`decode_line_number`](address:97EB@2?hex) `&97EB` |
| Decimal print | [`print_line_number`](address:991F@2?hex) `&991F`, 5-wide variant [`trace_print_number`](address:9923@2?hex) `&9923` |
| Token → text | [`print_token`](address:B50E@2?hex) `&B50E` |
| `TOP` (`TO`+`P`) run-time read | [`fn_to`](address:AEDC@2?hex) `&AEDC` |
| `LIST` line walk | [`stmt_list`](address:B59C@2?hex) `&B59C`, [`list_char_loop`](address:B639@2?hex) `&B639` |
| LISTO option / indent | [`stmt_listo`](address:B58A@2?hex) `&B58A`, [`print_listo_indent`](address:B577@2?hex) `&B577` |
| Line search / framing | [`find_program_line`](address:9970@2?hex) `&9970`, [`advance_to_next_line`](address:909F@2?hex) `&909F` |
| Insert / delete line | [`insert_line`](address:BC8D@2?hex) `&BC8D`, [`delete_program_line`](address:BC2D@2?hex) `&BC2D` |
| Empty program / NEW | [`start_new_program`](address:8ADD@2?hex) `&8ADD` |
| Read input line (OSWORD 0) | [`read_input_line`](address:BC02@2?hex) `&BC02` |
