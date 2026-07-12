# Acorn BBC BASIC

[![Verify disassembly](https://github.com/acornaeology/bbc-basic/actions/workflows/verify.yml/badge.svg)](https://github.com/acornaeology/bbc-basic/actions/workflows/verify.yml)

BBC BASIC is the BASIC interpreter built into the BBC Micro, written by Sophie Wilson at Acorn Computers. It is a 16 kB sideways language ROM combining a line editor, a keyword tokeniser and de-tokeniser, a statement interpreter, an expression evaluator with full operator precedence, integer and 40-bit floating-point arithmetic, string handling, and variable storage. BBC BASIC is renowned for its structured-programming features — named procedures and functions (PROC/FN) with local variables, REPEAT/UNTIL loops, and IF/THEN/ELSE — and for its built-in 6502 assembler, which lets machine code be written inline and assembled directly from a BASIC program. Version II is the most widely used BBC Micro release.

This repository contains an annotated disassembly of the Acorn BBC BASIC ROM, produced by reverse-engineering the original 6502 machine code. The disassembly includes named labels, comments explaining the logic, and cross-references between subroutines.

## Versions

- **Acorn BBC BASIC II**
  - [Formatted disassembly on acornaeology.uk](https://acornaeology.uk/bbc-basic/2.html)
  - [BBC BASIC II in The BBC Micro ROM Library](https://tobylobster.github.io/rom_library/?md5=2cc67be4624df4dc66617742571a8e3d)

## How it works

The disassembly is produced by a Python script that drives [dasmos](https://github.com/acornaeology/dasmos), a programmable disassembler for 6502 binaries. The script feeds the original ROM image to dasmos along with annotations — entry points, labels, constants, and comments — to produce readable assembly output.

The output is verified by reassembling with [beebasm](https://github.com/stardot/beebasm) and comparing the result byte-for-byte against the original ROM. This round-trip verification runs automatically in CI on every push.

The analysis surface around dasmos (verify, lint, audit, cfg, comments, address mapping across versions, …) is provided by [fantasm](https://acornaeology.github.io/fantasm/) — see its docs for the full command and API reference.

## Disassembling locally

Requires [uv](https://docs.astral.sh/uv/) and [beebasm](https://github.com/stardot/beebasm) (v1.10+).

```sh
uv sync
uv run fantasm disassemble 2
uv run fantasm verify 2
```

## (Re-)Assembling locally

To assemble the `.asm` file back into a ROM image using [beebasm](https://github.com/stardot/beebasm):

```sh
beebasm -i versions/basic-2/output/basic-2.asm -o basic-2.rom
```

## References

- [tobylobster's BBC Micro MOS disassembly](https://tobylobster.github.io/mos/)
  tobylobster's fully annotated disassembly of the BBC Micro MOS — a reference for the OSBYTE / OSWORD / vector-call semantics and zero-page / workspace names BBC BASIC relies on.
- [The Advanced BASIC ROM User Guide (Colin Pharo)](https://www.retro-kit.co.uk/user/custom/BBC/Books/Advanced-BASIC-ROM-User-Guide.pdf)
  A detailed reference to the internals of the BBC BASIC ROM: zero-page usage, the keyword table, the interpreter loop, variable storage, and the floating-point routines.
- [BBC Microcomputer System User Guide (John Coll)](https://archive.org/details/BBCUserGuide)
  The official BBC Micro user guide. Much of it documents the BBC BASIC language: statements, functions, operators, and the assembler.
- [J.G. Harston's BBC BASIC source reconstruction](https://mdfs.net/Software/BBCBasic/BBC/)
  A multi-target reconstruction of the BBC BASIC source that reassembles (with the BBC BASIC assembler) to byte-identical ROMs, with zero-page maps and entry/exit documentation. The primary external source of BBC BASIC II labels.
- [tobylobster's BBC BASIC tokeniser/detokeniser](https://github.com/TobyLobster/basic_tokens)
  A Python BBC BASIC tokeniser and detokeniser — a clean reference for the keyword/token table and the tokenising rules.
- [hoglet's BBC BASIC 4r32 disassembly](https://github.com/hoglet67/BBCBasic4r32)
  A byte-identical disassembly of BBC BASIC 4r32. A later, reorganised cousin of BASIC II, useful for cross-referencing structure and label names.
- [BBC BASIC II in The BBC Micro ROM Library](https://tobylobster.github.io/rom_library/?md5=2cc67be4624df4dc66617742571a8e3d)
  The exact ROM image catalogued by tobylobster's ROM library, identified by MD5.

## Credits

- [dasmos](https://github.com/acornaeology/dasmos) — programmable 6502 disassembler used to drive the annotation pipeline. dasmos is a ground-up rewrite of [py8dis](https://github.com/acornaeology/py8dis) (originally by [SteveF](https://github.com/ZornsLemma), forked for acornaeology), to which it owes its core ideas
- [beebasm](https://github.com/stardot/beebasm) by Rich Mayfield and contributors
- [The BBC Micro ROM Library](https://tobylobster.github.io/rom_library/) by tobylobster

## License

The annotations and disassembly scripts in this repository are released under the [MIT License](LICENSE). The original ROM images remain the property of their respective copyright holders.
