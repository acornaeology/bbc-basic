# Glossary

**BBC BASIC**
: The BASIC interpreter built into the BBC Micro, written by Roger Wilson (now Sophie Wilson) at Acorn. A 16 kB sideways language ROM providing a line editor, tokeniser, statement interpreter, expression evaluator, and floating-point arithmetic.

  BBC BASIC is notable for its structured-programming features (named
  PROC/FN procedures and functions with local variables, REPEAT/UNTIL,
  IF/THEN/ELSE) and its built-in 6502 assembler, which assembles inline
  machine code directly from a BASIC program.

**Language ROM**
: A sideways ROM that the MOS can enter as the current language via its language entry point at &8000. When selected, BASIC takes over the machine, setting up its workspace and presenting the `>` prompt. Contrast with a service-only ROM (such as a filing system) that never becomes the current language.

**Sideways ROM**
: One of up to 16 ROM images mapped into the &8000-&BFFF address space on the BBC Micro. Only one is paged in at a time, selected via the ROM latch at &FE30. BBC BASIC is a 16 kB sideways ROM.

**ROM header**
: The fixed-shape structure at &8000 that identifies a sideways ROM to the MOS: language entry (&8000), service entry (&8003), ROM type byte (&8006), copyright-offset pointer (&8007), binary version (&8008), NUL-terminated title (&8009), then the copyright string.

**MOS** (Machine Operating System)
: The BBC Micro's built-in operating system ROM, providing the OS call interface (OSWRCH, OSRDCH, OSBYTE, OSWORD, OSFILE, …), language and service dispatch, and hardware abstraction. BASIC calls the MOS for all I/O and filing-system access.

**Service call**
: The MOS mechanism for broadcasting events (initialisation, unrecognised command, error, language entry, …) to sideways ROMs via the service entry point at &8003. BASIC's service handler is minimal compared with a filing system's.

**Token**
: A single-byte code (≥ &80) that stands for a BASIC keyword in the stored program. Tokenising a line replaces each keyword with its token, saving space and speeding interpretation; listing reverses the process.

**Keyword table**
: The table near the start of the ROM listing every BASIC keyword as text plus its token byte and a flag byte. The tokeniser scans it to encode keywords typed by the user; the de-tokeniser uses it to expand tokens back to text when listing.

**Tokeniser**
: The routine that converts a line of typed BASIC text into its internal tokenised form, replacing keywords with token bytes using the keyword table, while leaving strings, line numbers, and variable names intact.

**Interpreter loop**
: The central dispatch loop that fetches the next tokenised statement, looks up the handler for its leading token, and executes it, then advances to the next statement or line.

**Expression evaluator**
: The routine that parses and evaluates BASIC expressions, honouring operator precedence and handling integer, floating-point, and string operands. Results are returned on BASIC's internal stack or in the floating-point accumulator.

**Floating-point accumulator** (FPA / FPB)
: Zero-page working registers holding BASIC's 40-bit (5-byte) floating-point values during arithmetic. BASIC's real-number format is a sign-and-magnitude mantissa with a binary exponent. Two accumulators allow binary operations (add, multiply, …) between a working value and an operand.

**Zero page**
: The first 256 bytes of 6502 memory (&00-&FF), accessed by fast zero-page addressing modes. BASIC makes heavy use of zero page for the program/text pointers, the expression and GOSUB stacks, variable pointers, and the floating-point accumulators.

**LOMEM / HIMEM / PAGE / TOP**
: BASIC's memory boundaries. PAGE is the start of the BASIC program; TOP is the address just past the program text; LOMEM is the start of variable storage (defaults to TOP); HIMEM is the top of memory available to BASIC (the stack grows down from here).

**PROC / FN**
: BASIC's named procedures (`PROC`) and functions (`FN`). Each can take parameters and declare LOCAL variables. Calls are tracked on BASIC's stack, which records return positions and saved local values.

**Line editor**
: The routine that reads a line of input from the keyboard with editing (copy/cursor keys), used both at the `>` prompt and for `INPUT`. Entered lines are passed to the tokeniser.

**BRK error**
: The 6502 `BRK` instruction used by the MOS for error reporting. A BRK is followed by an error-number byte and a NUL-terminated message string; the MOS routes it through BRKV (&0202). BASIC raises errors this way and traps them through its `ON ERROR` mechanism.

**OSWRCH / OSRDCH / OSBYTE / OSWORD**
: Core MOS entry points BASIC uses constantly: OSWRCH (&FFEE) writes a character, OSRDCH (&FFE0) reads one, OSBYTE (&FFF4) and OSWORD (&FFF1) perform miscellaneous and word-sized OS functions selected by the accumulator.

**Inline assembler**
: BASIC's built-in 6502 assembler, invoked between `[` and `]`. It assembles mnemonics into memory at the address held in `P%`, allowing machine code to be written and assembled directly from a BASIC program.
