"""dasmos driver for Acorn BBC BASIC II.

BBC BASIC II is a 16 kB sideways language ROM mapped at &8000-&BFFF
on the BBC Micro. This script drives dasmos to produce an annotated,
byte-faithful disassembly: the generated assembly reassembles with
beebasm to a byte-identical copy of the original ROM.

The driver is run by ``fantasm disassemble 2``, which sets FANTASM_ROM
and FANTASM_OUTPUT_DIR. When run standalone, it falls back to the
in-tree paths.

Zero-page and workspace names follow Colin Pharo's "Advanced BASIC ROM
User Guide" chapter 7 (the BASIC memory map); the keyword/action table
layout and the statement-dispatch mechanism follow the same chapter and
J.G. Harston's source reconstruction.
"""
import os
import sys
from pathlib import Path

import dasmos
from dasmos import Align

_script_dirpath = Path(__file__).resolve().parent
_version_dirpath = _script_dirpath.parent
_rom_filepath = os.environ.get(
    'FANTASM_ROM', str(_version_dirpath / 'rom' / 'basic-2.rom')
)
_output_dirpath = Path(
    os.environ.get('FANTASM_OUTPUT_DIR', str(_version_dirpath / 'output'))
)

d = dasmos.Disassembler.create(
    cpu='6502',
    auto_label_data_prefix='l',
    auto_label_code_prefix='c',
    auto_label_subroutine_prefix='sub_c',
    auto_label_loop_prefix='loop_c',
)
d.load(_rom_filepath, 0x8000)

# Standard environments for an Acorn sideways language ROM. No
# filing-system or FDC environments: BBC BASIC is a language ROM.
d.use_environment('acorn_mos')
d.use_environment('acorn_model_b_hardware')
d.use_environment('acorn_sideways_rom')

# Code entry points. BASIC's language entry at &8000 is inline code
# (CMP #1 / BEQ start / RTS), not a JMP abs, so the sideways-ROM
# environment cannot auto-seed it. The ROM type byte (&60) has bit 7
# clear, so BASIC has no service entry: the bytes at &8003 are the tail
# of the language-entry instructions, not a separate handler.
d.entry(0x8000)
d.entry(0x8023)  # Language startup (the BEQ target)
d.entry(0xb402)  # BASIC error handler, installed into BRKV at startup

# ----------------------------------------------------------------------
# Language entry and startup.
# ----------------------------------------------------------------------
d.comment(
    0x8000,
    'Language entry: CMP #1 / BEQ language_startup / RTS',
    align=Align.INLINE,
)
d.label(0x8add, 'immediate_loop')   # The ">" prompt / command loop
d.label(0xb402, 'brk_handler')      # Reached via BRKV on any error

d.subroutine(
    0x8023, 'language_startup',
    title='Language startup',
    description="""Reached from the language entry when the MOS starts BASIC
(A = 1). Reads HIMEM and PAGE from the MOS, clears the print and
formatting state, seeds the random-number generator if it is cold,
installs the BASIC error handler in BRKV, and jumps to the
immediate ("> ") loop.
""",
)
d.comment(0x8035, 'LISTO = 0: no LIST indentation', align=Align.INLINE)
d.comment(0x8037, '@% high two bytes = 0', align=Align.INLINE)
d.comment(0x803e, 'WIDTH = &FF: no automatic line wrap', align=Align.INLINE)
d.comment(0x8042, '@% = &0000090A: default PRINT format', align=Align.INLINE)
d.comment(0x804b, 'OR the RND seed bytes (&0D-&11) together', align=Align.INLINE)
d.comment(0x8055, 'Seed already non-zero: leave it', align=Align.INLINE)
d.comment(0x8057, 'Cold seed: set RND to "ARW" (&575241)', align=Align.INLINE)
d.comment(0x8063, 'Install brk_handler (&B402) into BRKV', align=Align.INLINE)
d.comment(0x806d, 'Enable IRQs and enter the immediate loop', align=Align.INLINE)

# ----------------------------------------------------------------------
# Zero page (Pharo ch. 7.1 "Zero Page Dedicated Locations"). All
# two-byte pointers are stored low byte first.
# ----------------------------------------------------------------------
d.label(0x0000, 'zp_lomem')           # Start of BASIC variables
d.label(0x0002, 'zp_vartop')          # End of BASIC variables
d.label(0x0004, 'zp_stack_ptr')       # Most recent BASIC-stack entry
d.label(0x0006, 'zp_himem')           # Start of screen / top of BASIC
d.label(0x0008, 'zp_erl')             # Line number that last errored
d.label(0x000a, 'zp_text_ptr_off')    # Offset into current text line
d.label(0x000b, 'zp_text_ptr')        # Start of current text line
d.label(0x000d, 'zp_rnd_seed')        # RND work area (&0D-&11)
d.label(0x0012, 'zp_top')             # End of program (excl. variables)
d.label(0x0014, 'zp_print_bytes')     # Bytes in current print field
d.label(0x0015, 'zp_print_flag')      # 0 = decimal, -ve = hexadecimal
d.label(0x0016, 'zp_error_vec')       # Address of BASIC error routine
d.label(0x0018, 'zp_page')            # PAGE DIV 256 (program start page)
d.label(0x0019, 'zp_text_ptr2')       # Secondary text pointer
d.label(0x001b, 'zp_text_ptr2_off')   # Secondary text-pointer offset
d.label(0x001c, 'zp_data_ptr')        # Pointer to next DATA item
d.label(0x001e, 'zp_count')           # Bytes printed since last newline
d.label(0x001f, 'zp_listo')           # LISTO flag
d.label(0x0020, 'zp_trace_flag')      # &00 = trace off, &FF = trace on
d.label(0x0021, 'zp_trace_max')       # Maximum TRACE line number
d.label(0x0023, 'zp_width')           # WIDTH setting
d.label(0x0024, 'zp_repeat_level')    # Nested REPEATs outstanding
d.label(0x0025, 'zp_gosub_level')     # Nested GOSUBs outstanding
d.label(0x0026, 'zp_for_level')       # 15 * nested FOR loops outstanding
d.label(0x0027, 'zp_var_type')        # Type of the value just fetched
d.label(0x0028, 'zp_opt_flag')        # bit0 list, bit1 errors, bit2 reloc
d.label(0x0029, 'zp_asm_opcode')      # Assembler: opcode byte

# Zero page (Pharo ch. 7.2 "Zero Page Multiple Use Locations"). These
# overlap by design; the labels mark each region's primary use.
d.label(0x002a, 'zp_iwa')             # Integer work area / accumulator
d.label(0x002e, 'zp_fwa')             # Floating point work area A
d.label(0x0036, 'zp_strbuf_len')      # Length of the string buffer
d.label(0x0037, 'zp_general')         # General work area (&37-&3A)
d.label(0x0039, 'zp_fileblk')         # LOAD/SAVE control block (&39-&44)
d.label(0x003b, 'zp_fwb')             # Floating point work area B
d.label(0x0043, 'zp_fp_temp')         # Floating point temporary area

# ----------------------------------------------------------------------
# Page 4 / 5 / 6 / 7 RAM workspace (Pharo ch. 7.3-7.6).
# ----------------------------------------------------------------------
d.label(0x0400, 'resint_at')          # @% print-format resident integer
for _i, _name in enumerate('abcdefghijklmnopqrstuvwxyz'):
    d.label(0x0404 + 4 * _i, f'resint_{_name}')  # A%..Z%
for _i in range(1, 5):
    d.label(0x046c + 5 * (_i - 1), f'fp_temp{_i}')  # FP TEMP1..TEMP4
d.label(0x0480, 'var_ptr_table')      # Variable lookup table (by initial)
d.label(0x0500, 'for_gosub_stack')    # FOR/REPEAT/GOSUB stack
d.label(0x0600, 'string_work')        # String work area / CALL block
d.label(0x0700, 'line_input_buf')     # Line input buffer

# ----------------------------------------------------------------------
# Keyword / token table (Pharo ch. 7.7). Each entry is the keyword text
# in ASCII, a token byte (bit 7 set), and a tokeniser flag byte.
# ----------------------------------------------------------------------
d.subroutine(
    0x8071, 'keyword_table',
    title='Keyword / tokeniser table',
    description="""Each entry is the keyword in ASCII, then a token byte (bit 7
set), then a flag byte that drives tokenising:

  bit 0  conditional: do not tokenise if followed by a letter
  bit 1  enter "middle of statement" mode
  bit 2  enter "start of statement" mode
  bit 3  FN/PROC: do not tokenise the following name
  bit 4  start tokenising a line number (after GOTO etc.)
  bit 5  do not tokenise the rest of the line (REM, DATA)
  bit 6  pseudo-variable: add &40 to the token at the start of
         a statement (so e.g. PTR is &8F as a function and &CF
         as an assignment target)

Entries are ordered so that the first acceptable abbreviation of
each keyword is unambiguous. The table runs to the action-address
tables at action_table_lo.
""",
)

# ----------------------------------------------------------------------
# Statement / function action-address tables (Pharo ch. 7.7). Tokens
# &8E-&FF have a handler whose address is held split across two parallel
# tables: low bytes at &836D, high bytes at &83DF, indexed by
# (token - &8E). The interpreter loads the address into (&37) and does
# JMP (&0037). Lower tokens (&80-&8D) are handled inline by the
# interpreter and the expression evaluator.
# ----------------------------------------------------------------------
ACTION_TABLE_LO = 0x836d
ACTION_TABLE_HI = 0x83df
FIRST_DISPATCH_TOKEN = 0x8e
NUM_DISPATCH_TOKENS = 0x72  # tokens &8E..&FF

# token -> handler base name (from the keyword table). Tokens <= &C5 are
# value-returning functions (fn_*); the rest are statements (stmt_*).
# Token &CE has no keyword (a gap in the table). The five pseudo-variable
# names recur at both their function token (&8F-&93) and their assignment
# token (&CF-&D3); the fn_/stmt_ prefix keeps the labels distinct.
KEYWORD_HANDLERS = {
    0x8e: 'openin', 0x8f: 'ptr', 0x90: 'page', 0x91: 'time',
    0x92: 'lomem', 0x93: 'himem', 0x94: 'abs', 0x95: 'acs',
    0x96: 'adval', 0x97: 'asc', 0x98: 'asn', 0x99: 'atn',
    0x9a: 'bget', 0x9b: 'cos', 0x9c: 'count', 0x9d: 'deg',
    0x9e: 'erl', 0x9f: 'err', 0xa0: 'eval', 0xa1: 'exp',
    0xa2: 'ext', 0xa3: 'false', 0xa4: 'fn', 0xa5: 'get',
    0xa6: 'inkey', 0xa7: 'instr', 0xa8: 'int', 0xa9: 'len',
    0xaa: 'ln', 0xab: 'log', 0xac: 'not', 0xad: 'openup',
    0xae: 'openout', 0xaf: 'pi', 0xb0: 'point', 0xb1: 'pos',
    0xb2: 'rad', 0xb3: 'rnd', 0xb4: 'sgn', 0xb5: 'sin',
    0xb6: 'sqr', 0xb7: 'tan', 0xb8: 'to', 0xb9: 'true',
    0xba: 'usr', 0xbb: 'val', 0xbc: 'vpos', 0xbd: 'chrs',
    0xbe: 'gets', 0xbf: 'inkeys', 0xc0: 'lefts', 0xc1: 'mids',
    0xc2: 'rights', 0xc3: 'strs', 0xc4: 'strings', 0xc5: 'eof',
    0xc6: 'auto', 0xc7: 'delete', 0xc8: 'load', 0xc9: 'list',
    0xca: 'new', 0xcb: 'old', 0xcc: 'renumber', 0xcd: 'save',
    0xcf: 'ptr', 0xd0: 'page', 0xd1: 'time', 0xd2: 'lomem',
    0xd3: 'himem', 0xd4: 'sound', 0xd5: 'bput', 0xd6: 'call',
    0xd7: 'chain', 0xd8: 'clear', 0xd9: 'close', 0xda: 'clg',
    0xdb: 'cls', 0xdc: 'data', 0xdd: 'def', 0xde: 'dim',
    0xdf: 'draw', 0xe0: 'end', 0xe1: 'endproc', 0xe2: 'envelope',
    0xe3: 'for', 0xe4: 'gosub', 0xe5: 'goto', 0xe6: 'gcol',
    0xe7: 'if', 0xe8: 'input', 0xe9: 'let', 0xea: 'local',
    0xeb: 'mode', 0xec: 'move', 0xed: 'next', 0xee: 'on',
    0xef: 'vdu', 0xf0: 'plot', 0xf1: 'print', 0xf2: 'proc',
    0xf3: 'read', 0xf4: 'rem', 0xf5: 'repeat', 0xf6: 'report',
    0xf7: 'restore', 0xf8: 'return', 0xf9: 'run', 0xfa: 'stop',
    0xfb: 'colour', 0xfc: 'trace', 0xfd: 'until', 0xfe: 'width',
    0xff: 'oscli',
}

d.label(ACTION_TABLE_LO, 'action_table_lo')
d.label(ACTION_TABLE_HI, 'action_table_hi')

# Read the ROM so we can resolve each table entry to its handler address
# and declare it as a subroutine (which gives fantasm's call graph real
# structure). Several tokens share a handler (e.g. DATA and DEF both
# dispatch to the same "skip to end of line" routine), so declare each
# distinct target only once; the duplicate table entries render
# symbolically against the first declaration.
_rom_bytes = Path(_rom_filepath).read_bytes()
_declared_handlers: dict[int, str] = {}
for _i in range(NUM_DISPATCH_TOKENS):
    _token = FIRST_DISPATCH_TOKEN + _i
    # Seed the trace and render the split table entry symbolically.
    d.code_ptr(ACTION_TABLE_LO + _i, ACTION_TABLE_HI + _i)
    _base = KEYWORD_HANDLERS.get(_token)
    if _base is None:
        continue  # Token &CE: unused gap in the keyword table.
    _target = (
        _rom_bytes[(ACTION_TABLE_LO - 0x8000) + _i]
        | (_rom_bytes[(ACTION_TABLE_HI - 0x8000) + _i] << 8)
    )
    if _target in _declared_handlers:
        continue
    _name = ('fn_' if _token <= 0xc5 else 'stmt_') + _base
    d.subroutine(_target, _name)
    _declared_handlers[_target] = _name

# ----------------------------------------------------------------------
# Core leaf utilities, named bottom-up from the call graph. These are
# called all over the interpreter, so naming them lifts readability
# across the whole listing.
# ----------------------------------------------------------------------
d.subroutine(
    0x8a97, 'skip_spaces',
    title='Skip spaces at the text pointer',
    description="""Advance the primary text pointer past any spaces and return the
first non-space character. The workhorse of the tokeniser and
interpreter: most statements call it between syntax elements.
""",
    on_entry={
        'zp_text_ptr (&0B)': 'points at the line being interpreted',
        'zp_text_ptr_off (&0A)': 'offset of the next character',
    },
    on_exit={
        'A': 'first non-space character',
        'Y': 'its offset within the line',
        'zp_text_ptr_off (&0A)': 'advanced past that character',
    },
)
d.subroutine(
    0x8a8c, 'skip_spaces_ptr2',
    title='Skip spaces at the secondary text pointer',
    description="""As skip_spaces, but works on the secondary text pointer
(zp_text_ptr2, &19) and its offset (&1B). Used while the primary
pointer is preserved, e.g. when scanning ahead during assignment.
""",
    on_exit={
        'A': 'first non-space character',
        'Y': 'its offset',
        '&1B': 'advanced past that character',
    },
)
d.subroutine(
    0x8aae, 'skip_spaces_expect_comma',
    title='Skip spaces and require a comma',
    description="""Call skip_spaces, then check the character is a comma. Raises
"Missing ," if it is not. Used by statements that take a
comma-separated argument list.
""",
)
d.subroutine(
    0x8942, 'read_via_ptr_general',
    title='Read a byte via the general pointer, then advance it',
    description="""Load the byte at (zp_general),Y and fall through to
inc_ptr_general to step the 16-bit pointer on by one.
""",
)
d.subroutine(
    0x8944, 'inc_ptr_general',
    title='Increment the general 16-bit pointer',
    description="""Increment the little-endian pointer held in zp_general
(&37/&38) by one, carrying into the high byte.
""",
)
d.comment(0x8a9d, 'Loop while the character is a space', align=Align.INLINE)
d.comment(0x8a92, 'Loop while the character is a space', align=Align.INLINE)

ir = d.disassemble()
output = str(
    ir.render(
        'beebasm',
        boundary_label_prefix='pydis_',
        byte_column=True,
        byte_column_format='py8dis',
        default_byte_cols=12,
        default_word_cols=6,
    )
)
_output_dirpath.mkdir(parents=True, exist_ok=True)
output_filepath = _output_dirpath / 'basic-2.asm'
output_filepath.write_text(output, encoding='utf-8')
print(f'Wrote {output_filepath}', file=sys.stderr)
json_filepath = _output_dirpath / 'basic-2.json'
json_filepath.write_text(str(ir.render('json')), encoding='utf-8')
print(f'Wrote {json_filepath}', file=sys.stderr)
