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
# BASIC's language entry at &8000 is inline code (CMP #1 / BEQ start /
# RTS), not a JMP abs, so tell the environment to seed it as code. The
# ROM type byte (&60) has bit 7 clear: BASIC has no service entry, so
# the bytes at &8003 are the tail of the language-entry instructions,
# not a separate handler.
d.use_environment(
    'acorn_sideways_rom', language_entry='code', service_entry='none',
)

# Code entry points. The language entry (&8000) and language_startup
# (&8023, the BEQ target) are reached by the trace from the env-seeded
# language entry, so they need no explicit entry() here.
d.entry(0xb402)  # BASIC error handler, installed into BRKV at startup

# ----------------------------------------------------------------------
# Language entry and startup.
# ----------------------------------------------------------------------
d.label(0xb402, 'brk_handler')      # Reached via BRKV on any error

d.subroutine(
    0x8023, 'language_startup',
    title='Language startup',
    description="""Reached from the language entry when the MOS starts BASIC
(A = 1). Reads HIMEM and PAGE from the MOS, clears the print and
formatting state, seeds the random-number generator if it is cold,
installs the BASIC error handler in BRKV, and jumps to
start_new_program, which clears any program and enters the
immediate ("> ") loop.
""",
)

# ----------------------------------------------------------------------
# Interpreter core: the immediate loop, line execution, the statement
# loop, and the token dispatch that drives the fn_*/stmt_* handlers.
# ----------------------------------------------------------------------
d.subroutine(
    0x8add, 'start_new_program',
    title='Clear program and enter the immediate loop',
    description="""Entered from language_startup. Sets up an empty program (as the
NEW command does) and falls through into the immediate loop.
""",
)
d.subroutine(
    0x8af6, 'immediate_loop',
    title='Immediate ("> ") loop',
    description="""Print the prompt, read a line into the input buffer, and
tokenise it. A line that begins with a line number is inserted into
the program; otherwise it is executed immediately.
""",
)
d.subroutine(
    0x8b0b, 'execute_line',
    title='Execute the line at the program pointer',
    description="""Run the tokenised statements on the line addressed by the
program pointer (zp_text_ptr, &0B), starting at offset zp_text_ptr_off.
""",
)
d.subroutine(
    0x8b9b, 'statement_loop',
    title='Statement execution loop',
    description="""The main interpreter loop: fetch the next statement's leading
token and dispatch it, then advance to the next statement (after a
colon) or line. Returns here after each statement completes.
""",
)
d.subroutine(
    0x8bb1, 'dispatch_token',
    title='Dispatch a tokenised function or command',
    description="""Index the action-address table by (token - &8E): load the
handler address into zp_general (&37/&38) and JMP (&0037). This is
the indirect jump that reaches every fn_* / stmt_* handler.
""",
    on_entry={'A': 'a command/function token (&8E-&FF)'},
)
d.subroutine(
    0x8bbf, 'try_variable_assignment',
    title='Not a command token: try an assignment',
    description="""Reached when the statement does not begin with a command token:
treat it as an implied-LET variable assignment, or one of the
=, * (OSCLI) or [ (assembler) special statement forms.
""",
)
d.subroutine(
    0x8b60, 'check_eq_star_bracket',
    title='Check for =, * and [ statements',
    description="""Recognise the statement forms that are not introduced by a
token: "=" (return a value from FN), "*" (pass the rest of the line
to OSCLI), and "[" (enter the inline assembler).
""",
)
d.subroutine(
    0x8951, 'tokenise_line',
    title='Tokenise a line',
    description="""Convert the line being entered into its internal form, replacing
keywords with tokens via the keyword_table while leaving strings,
line numbers and names intact. Works through the buffer using the
general pointer (zp_general, &37).
""",
)
d.subroutine(
    0x84fd, 'assembler_exit',
    title='Finish the inline assembler',
    description="""Leave the inline 6502 assembler (reached at "]") and resume
interpreting BASIC.
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

# ----------------------------------------------------------------------
# Expression evaluator and numeric-stack primitives. The interpreter
# keeps the current value in the integer accumulator (zp_iwa, &2A-&2D)
# or the floating-point accumulator (zp_fwa, &2E-&35), with its type in
# zp_var_type (&27), and spills values onto the BASIC stack (grows down
# from HIMEM, top in zp_stack_ptr &04). Naming these unlocks the maths
# functions, PRINT, and the assignment paths.
# ----------------------------------------------------------------------
d.subroutine(
    0x9857, 'check_end_of_statement',
    title='Check for end of statement',
    description="""Skip spaces and require the statement to end here: a colon, an
end-of-line (&0D), or ELSE. Anything else raises "Syntax error".
Also polls for Escape.
""",
)
d.subroutine(
    0x9b1d, 'eval_expr',
    title='Evaluate an expression',
    description="""The interpreter's main expression entry point. Copies the
primary text pointer (PtrA: zp_text_ptr / zp_text_ptr_off) to the
secondary pointer (PtrB: zp_text_ptr2 / &1B) and evaluates the
expression there.
""",
    on_exit={
        'zp_var_type (&27)': 'result type (integer / real / string)',
        'zp_iwa / zp_fwa': 'the result value',
        '&1B': 'advanced past the expression',
    },
)
d.subroutine(
    0x8821, 'eval_expr_to_integer',
    title='Evaluate an integer expression',
    description="""Evaluate the expression at the text pointer (eval_expr) and
coerce the result to an integer (coerce_to_integer), then copy the
secondary text offset back to the primary pointer. Used wherever a
statement needs an integer argument.
""",
    on_exit={'zp_iwa (&2A)': '4-byte integer result'},
)
d.subroutine(
    0xadec, 'eval_factor',
    title='Evaluate a factor (evaluator level 1)',
    description="""Evaluate the highest-precedence level of an expression at PtrB:
unary minus, unary plus and NOT; parenthesised sub-expressions;
the ?, !, $ and | indirection operators; string literals; and the
built-in functions.
""",
)
d.subroutine(
    0x92f0, 'coerce_to_integer',
    title='Coerce the current value to an integer',
    description="""Check the type of the last evaluated value (in A from
zp_var_type): a string raises "Type mismatch", an integer returns
unchanged, and a real is converted to a 4-byte integer in the
integer accumulator.
""",
    on_entry={'A': 'value type from zp_var_type (&27)'},
)
d.subroutine(
    0xa1da, 'fwa_sign',
    title='Get the sign of the FP accumulator',
    description="""Determine the sign of the floating-point accumulator:
zero, positive or negative (Z set when FWA is zero). Tests the
mantissa bytes (&31-&35) and the sign.
""",
)
d.subroutine(
    0xa3b5, 'fwa_unpack_var',
    title='Unpack a floating-point variable into FWA',
    description="""Unpack the packed five-byte floating-point value addressed by
(&4B/&4C) into the floating-point accumulator (FWA).
""",
)
d.subroutine(
    0xbd94, 'stack_integer',
    title='Push the integer accumulator onto the BASIC stack',
    description="""Reserve four bytes on the BASIC stack (zp_stack_ptr, &04) and
copy the integer accumulator (zp_iwa) onto it. Errors if the stack
would collide with the heap.
""",
)
d.subroutine(
    0xbd51, 'stack_real',
    title='Push the floating-point accumulator onto the BASIC stack',
    description="""Reserve five bytes on the BASIC stack and copy the packed
floating-point accumulator onto it.
""",
)
d.subroutine(
    0xbdb2, 'stack_string',
    title='Push the current string onto the BASIC stack',
    description="""Copy the string from the string buffer (length zp_strbuf_len,
&36; text at &0600) onto the BASIC stack, length last.
""",
)
d.subroutine(
    0xbdea, 'unstack_integer',
    title='Pop an integer from the BASIC stack',
    description="""Copy the four-byte integer on top of the BASIC stack into the
integer accumulator (zp_iwa) and drop it.
""",
)

# ----------------------------------------------------------------------
# Integer-accumulator (IWA, &2A-&2D) arithmetic. These 32-bit signed
# routines are documented in Pharo ch. 2; the interpreter calls them
# for INTEGER (%) arithmetic and wherever a value has been coerced to
# an integer. The two pseudo-variable handlers fn_true / fn_false
# double as the "IWA = -1" / "IWA = 0" primitives.
# ----------------------------------------------------------------------
d.subroutine(
    0xad93, 'iwa_negate',
    title='Negate the integer accumulator',
    description='IWA = -IWA (two\'s-complement negate the 32-bit integer).',
)
d.subroutine(
    0xad71, 'iwa_abs',
    title='Make the integer accumulator positive',
    description='IWA = ABS(IWA).',
)
d.subroutine(
    0x9c5b, 'iwa_add',
    title='Integer add',
    description='IWA = IWA + the integer operand.',
)
d.subroutine(
    0x9cc2, 'iwa_rsub',
    title='Reverse integer subtract',
    description='IWA = operand - IWA.',
)
d.subroutine(
    0x9d6d, 'iwa_mul',
    title='Integer multiply',
    description='IWA = IWA * the integer operand.',
)
d.subroutine(
    0x9e0a, 'iwa_div',
    title='Integer divide',
    description='IWA = IWA DIV the integer operand.',
)
d.subroutine(
    0x9e01, 'iwa_mod',
    title='Integer remainder',
    description='IWA = IWA MOD the integer operand.',
)
d.subroutine(
    0x9aad, 'iwa_test_var',
    title='Compare an integer variable with the accumulator',
    description='Compare the integer operand against IWA and set flags.',
)
d.subroutine(
    0xaeea, 'iwa_from_ya',
    title='Set the integer accumulator to a small integer',
    description='IWA = 256*Y + A.',
)
d.subroutine(
    0xb336, 'iwa_load_var',
    title='Load an integer variable into the accumulator',
    description='Copy a 4-byte integer variable into IWA.',
)
d.subroutine(
    0xb4c6, 'iwa_store_var',
    title='Store the accumulator into an integer variable',
    description='Copy IWA into a 4-byte integer variable.',
)
d.subroutine(
    0xaf56, 'iwa_load_zp',
    title='Load a zero-page integer variable into the accumulator',
    description='Copy a 4-byte integer from zero page into IWA.',
)
d.subroutine(
    0xbe44, 'iwa_store_zp',
    title='Store the accumulator into a zero-page integer variable',
    description='Copy IWA into a 4-byte zero-page integer variable.',
)

# ----------------------------------------------------------------------
# Floating-point arithmetic (Pharo ch. 3). BBC BASIC keeps reals in two
# accumulators: FWA (zp_fwa, &2E-&35) and FWB (zp_fwb, &3B-&42), in an
# unpacked work form; values are stored packed (5 bytes). Routines that
# take a "fp var" operand expect (&4B/&4C) to point at it. These are
# the primitives the maths functions and real arithmetic build on.
# ----------------------------------------------------------------------
d.subroutine(0xa686, 'fwa_clear', title='FWA = 0',
             description='Set the floating-point accumulator to zero.')
d.subroutine(0xa699, 'fwa_set_one', title='FWA = 1',
             description='Set the floating-point accumulator to 1.')
d.subroutine(0xad7e, 'fwa_negate', title='FWA = -FWA',
             description='Negate the floating-point accumulator.')
d.subroutine(0xa303, 'fwa_normalise', title='Normalise FWA',
             description='Normalise the floating-point accumulator.')
d.subroutine(0xa65c, 'fwa_round', title='Round FWA',
             description='Round the floating-point accumulator.')
d.subroutine(0xa6a5, 'fwa_reciprocal', title='FWA = 1 / FWA',
             description='Reciprocal of the FP accumulator (normalised, rounded).')
d.subroutine(0xa4dc, 'fwa_copy_from_fwb', title='FWA = FWB',
             description='Copy FWB into FWA.')
d.subroutine(0xa4d6, 'fwa_swap_var', title='Swap FWA and a fp variable',
             description='Exchange the FP accumulator with the fp variable operand.')
d.subroutine(0xa5ff, 'fwa_compare_var', title='Compare FWA with a fp variable',
             description='Test the fp variable operand against FWA.')
# Add / subtract.
d.subroutine(0xa500, 'fwa_add_var', title='FWA = FWA + fp var',
             description='Add the fp variable operand to FWA (normalised, rounded).')
d.subroutine(0xa505, 'fwa_add_fwb', title='FWA = FWA + FWB',
             description='Add FWB to FWA (normalised, rounded).')
d.subroutine(0xa50b, 'fwa_add_fwb_raw', title='FWA = FWA + FWB (unrounded)',
             description='Add FWB to FWA, normalised but not rounded.')
d.subroutine(0xa4fd, 'fwa_rsub_var', title='FWA = fp var - FWA',
             description='Reverse subtract: operand minus FWA (normalised, rounded).')
# Multiply / divide.
d.subroutine(0xa656, 'fwa_mul_var', title='FWA = FWA * fp var',
             description='Multiply FWA by the fp variable operand (normalised, rounded).')
d.subroutine(0xa606, 'fwa_mul_var_raw', title='FWA = FWA * fp var (raw)',
             description='Multiply FWA by the operand, unnormalised and unrounded.')
d.subroutine(0xa1f4, 'fwa_mul10', title='FWA = FWA * 10',
             description='Multiply FWA by ten, unnormalised and unrounded.')
d.subroutine(0xa6ad, 'fwa_rdiv_var', title='FWA = fp var / FWA',
             description='Reverse divide: operand divided by FWA (normalised, rounded).')
d.subroutine(0xa24d, 'fwa_div10', title='FWA = FWA / 10',
             description='Divide FWA by ten, unnormalised and unrounded.')
# Pack / unpack between the accumulator and 5-byte stored form.
d.subroutine(0xa38d, 'fwa_pack_var', title='Pack FWA into a fp variable',
             description='Pack FWA into the five-byte fp variable at (&4B/&4C).')
d.subroutine(0xa385, 'fwa_pack_temp1', title='Pack FWA into TEMP1',
             description='Pack FWA into the floating-point temporary at &046C.')
d.subroutine(0xa37d, 'fwa_pack_temp2', title='Pack FWA into TEMP2',
             description='Pack FWA into the floating-point temporary at &0471.')
d.subroutine(0xa381, 'fwa_pack_temp3', title='Pack FWA into TEMP3',
             description='Pack FWA into the floating-point temporary at &0476.')
d.subroutine(0xa3b2, 'fwa_unpack_temp1', title='Unpack TEMP1 into FWA',
             description='Unpack the floating-point temporary at &046C into FWA.')
# FWB helpers.
d.subroutine(0xa453, 'fwb_clear', title='FWB = 0',
             description='Set the second floating-point accumulator to zero.')
d.subroutine(0xa21e, 'fwb_copy_from_fwa', title='FWB = FWA',
             description='Copy FWA into FWB.')
d.subroutine(0xa34e, 'fwb_unpack_var', title='Unpack a fp variable into FWB',
             description='Unpack the fp variable at (&4B/&4C) into FWB.')

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
