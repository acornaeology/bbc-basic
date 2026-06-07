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
# Cold seed for the RND generator: if the whole 33-bit LFSR state is
# zero (which it is at power-on) install a fixed non-zero seed. Nothing
# else re-seeds unless the program calls RND(-n), so each program's
# random sequence is deterministic from a cold start.
d.comment(0x8049, 'Test the LFSR state for all-zero...', align=Align.INLINE)
d.comment(0x804b, '...only bit 0 of &11 belongs to the register',
          align=Align.INLINE)
d.comment(0x804d, 'OR bits 0-7', align=Align.INLINE)
d.comment(0x804f, 'bits 8-15', align=Align.INLINE)
d.comment(0x8051, 'bits 16-23', align=Align.INLINE)
d.comment(0x8053, 'bits 24-31', align=Align.INLINE)
d.comment(0x8055, 'Non-zero: keep the existing state', align=Align.INLINE)
d.comment(
    0x8057,
    'The generator needs a non-zero state. At power-on the work\n'
    'area is zero, so a fixed seed is installed here. The bytes\n'
    '&41, &52, &57 spell "ARW": the initials of Roger (now Sophie)\n'
    'Wilson, who wrote BBC BASIC. Nothing else re-seeds unless the\n'
    'program calls RND(-n), so a sequence is deterministic from a\n'
    'cold start.',
    word_wrap=False,
)
d.comment(0x8057, 'Cold seed: state becomes &00575241; load &41',
          align=Align.INLINE)
d.comment(0x8059, 'byte 0', align=Align.INLINE)
d.comment(0x805b, 'load &52', align=Align.INLINE)
d.comment(0x805d, 'byte 1', align=Align.INLINE)
d.comment(0x805f, 'load &57', align=Align.INLINE)
d.comment(0x8061, 'byte 2 (bytes 3 and 4 stay zero)', align=Align.INLINE)
d.comment(0x8063, 'Install brk_handler (&B402) into BRKV', align=Align.INLINE)
d.comment(0x806d, 'Enable IRQs and enter the immediate loop', align=Align.INLINE)

# ----------------------------------------------------------------------
# Zero page (Pharo ch. 7.1 "Zero Page Dedicated Locations"). All
# two-byte pointers are stored low byte first.
# ----------------------------------------------------------------------
d.label(0x0000, 'zp_lomem')           # Start of BASIC variables
d.label(0x0002, 'zp_vartop')          # End of BASIC variables (heap top)
d.label(0x0003, 'zp_vartop_1')
d.label(0x0004, 'zp_stack_ptr')       # Top of the BASIC value stack
d.label(0x0005, 'zp_stack_ptr_1')
d.label(0x0006, 'zp_himem')           # Start of screen / top of BASIC
d.label(0x0008, 'zp_erl')             # Line number that last errored
d.label(0x000a, 'zp_text_ptr_off')    # Offset into current text line
d.label(0x000b, 'zp_text_ptr')        # Start of current text line
# RND work area (&0D-&11): a 33-bit LFSR state. &0D-&10 are a 32-bit
# little-endian value (bits 0-31); bit 0 of &11 is bit 32. See rnd_step.
d.label(0x000d, 'zp_rnd_seed')        # LFSR bits 0-7
d.label(0x000e, 'zp_rnd_seed_1')      # LFSR bits 8-15
d.label(0x000f, 'zp_rnd_seed_2')      # LFSR bits 16-23
d.label(0x0010, 'zp_rnd_seed_3')      # LFSR bits 24-31
d.label(0x0011, 'zp_rnd_seed_4')      # LFSR bit 32 (in bit 0; overflow)
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
# Integer work area / accumulator (IWA): 32-bit signed, little-endian.
d.label(0x002a, 'zp_iwa')             # IWA byte 0 (least significant)
d.label(0x002b, 'zp_iwa_1')
d.label(0x002c, 'zp_iwa_2')
d.label(0x002d, 'zp_iwa_3')           # IWA byte 3 (most significant)
# Floating point work area A (FWA), the unpacked 8-byte accumulator.
d.label(0x002e, 'zp_fwa_sign')        # Sign (bit 7 set = negative)
d.label(0x002f, 'zp_fwa_ovf')         # Overflow / guard byte
d.label(0x0030, 'zp_fwa_exp')         # Exponent (excess-128; 0 = value 0)
d.label(0x0031, 'zp_fwa_m1')          # Mantissa MSB (normalised: bit 7 = 1)
d.label(0x0032, 'zp_fwa_m2')
d.label(0x0033, 'zp_fwa_m3')
d.label(0x0034, 'zp_fwa_m4')          # Mantissa LSB
d.label(0x0035, 'zp_fwa_rnd')         # Rounding byte (extra precision)
d.label(0x0036, 'zp_strbuf_len')      # Length of the string buffer
d.label(0x0037, 'zp_general')         # General work area (&37-&3A)
d.label(0x0039, 'zp_fileblk')         # LOAD/SAVE control block (&39-&44)
# Floating point work area B (FWB), same layout as FWA.
d.label(0x003b, 'zp_fwb_sign')
d.label(0x003c, 'zp_fwb_ovf')
d.label(0x003d, 'zp_fwb_exp')
d.label(0x003e, 'zp_fwb_m1')
d.label(0x003f, 'zp_fwb_m2')
d.label(0x0040, 'zp_fwb_m3')
d.label(0x0041, 'zp_fwb_m4')
d.label(0x0042, 'zp_fwb_rnd')
d.label(0x0043, 'zp_fp_temp')         # Floating point temporary area
d.label(0x004b, 'zp_fp_ptr')          # Pointer to a packed fp variable
d.label(0x004c, 'zp_fp_ptr_1')        # (high byte; used by the FP routines)

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

# Optional (title, description) for individual handlers, attached when
# the handler is declared below. The mathematical functions (Pharo
# ch. 5) each evaluate their argument into the floating-point
# accumulator then fall into a pure routine (argument already in FWA)
# a few bytes later, whose address is noted.
HANDLER_INFO = {
    'fn_sin': ('SIN', 'FWA = sin(FWA), argument in radians. '
                      'Pure routine at &A99B.'),
    'fn_cos': ('COS', 'FWA = cos(FWA), argument in radians. '
                      'Pure routine at &A990.'),
    'fn_tan': ('TAN', 'FWA = tan(FWA), argument in radians. '
                      'Pure routine at &A6C1.'),
    'fn_asn': ('ASN', 'FWA = arcsin(FWA), result in radians. '
                      'Pure routine at &A8DD.'),
    'fn_acs': ('ACS', 'FWA = arccos(FWA), result in radians. '
                      'Computed as arcsin then adjusted at &A927.'),
    'fn_atn': ('ATN', 'FWA = arctan(FWA), result in radians. '
                      'Pure routine at &A90A.'),
    'fn_ln': ('LN', 'FWA = natural log of FWA. Pure routine at &A801.'),
    'fn_log': ('LOG', 'FWA = base-10 log of FWA. Pure routine at &ABAB.'),
    'fn_exp': ('EXP', 'FWA = e to the power FWA. Pure routine at &AA94.'),
    'fn_sqr': ('SQR', 'FWA = square root of FWA. Pure routine at &A7B7.'),
    'fn_deg': ('DEG', 'FWA = FWA radians expressed in degrees. '
                      'Pure routine at &ABC5.'),
    'fn_rad': ('RAD', 'FWA = FWA degrees expressed in radians. '
                      'Pure routine at &ABB4.'),
    'fn_pi': ('PI', 'FWA = pi (3.14159265). Takes no argument.'),
    # Non-maths function handlers.
    'fn_abs': ('ABS', 'Absolute value of a number. ABS numeric.'),
    'fn_int': ('INT', 'Integer part (floor) of a number. INT numeric.'),
    'fn_sgn': ('SGN', 'Sign of a number: -1, 0 or +1. SGN numeric.'),
    'fn_not': ('NOT', 'Bitwise NOT (one\'s complement) of an integer. '
                      'NOT numeric.'),
    'fn_true': ('TRUE', 'The constant TRUE (-1). Sets IWA = -1; this is '
                        'also the ineg1 integer primitive.'),
    'fn_false': ('FALSE', 'The constant FALSE (0). Sets IWA = 0; this is '
                          'also the izero integer primitive.'),
    'fn_to': ('TO', 'The TO keyword of FOR. It has no standalone action; '
                    'reaching it as a statement token is an error.'),
    'fn_asc': ('ASC', 'ASCII code of the first character of a string, or '
                      '-1 if empty. ASC string.'),
    'fn_len': ('LEN', 'Length of a string. LEN string.'),
    'fn_val': ('VAL', 'Number parsed from the start of a string. '
                      'VAL string.'),
    'fn_eval': ('EVAL', 'Evaluate a string as a BASIC expression. '
                        'EVAL string.'),
    'fn_instr': ('INSTR', 'Position of one string within another, '
                          'optionally from a start. INSTR(a$, b$ [,n]).'),
    'fn_count': ('COUNT', 'Characters printed since the last newline. '
                          'COUNT.'),
    'fn_pos': ('POS', 'Horizontal text-cursor position in the window. POS.'),
    'fn_vpos': ('VPOS', 'Vertical text-cursor position in the window. VPOS.'),
    'fn_point': ('POINT', 'Logical colour of a graphics point. '
                          'POINT(x, y).'),
    'fn_erl': ('ERL', 'Line number where the last error occurred. ERL.'),
    'fn_err': ('ERR', 'Error number of the last error. ERR.'),
    'fn_get': ('GET', 'Wait for a key and return its ASCII code. GET.'),
    'fn_inkey': ('INKEY', 'Read a key within a time limit, test a key, or '
                          'read the machine ID. INKEY numeric.'),
    'fn_adval': ('ADVAL', 'Read an analogue (A/D) channel or a buffer '
                          'status. ADVAL numeric.'),
    'fn_usr': ('USR', 'Call machine code and return the result registers '
                      'packed into a value. USR address.'),
    'fn_rnd': ('RND', 'Random number; the form depends on the argument '
                      '(see rnd_*). RND[(numeric)].'),
    # File functions.
    'fn_openin': ('OPENIN', 'Open a file for input, returning its channel '
                            '(0 if not found). OPENIN string.'),
    'fn_openout': ('OPENOUT', 'Create a file for output, returning its '
                              'channel. OPENOUT string.'),
    'fn_openup': ('OPENUP', 'Open a file for update (read and write), '
                            'returning its channel. OPENUP string.'),
    'fn_bget': ('BGET', 'Read a byte from an open file. BGET#channel.'),
    'fn_ext': ('EXT', 'Length (extent) of an open file. EXT#channel.'),
    'fn_eof': ('EOF', 'TRUE when at the end of an open file. EOF#channel.'),
    # Pseudo-variable reads (the assignment forms are the stmt_* twins).
    'fn_ptr': ('=PTR', 'Read the sequential pointer of an open file. '
                       'PTR#channel.'),
    'fn_page': ('=PAGE', 'Read PAGE, the start of the BASIC program. PAGE.'),
    'fn_time': ('=TIME', 'Read the centisecond elapsed-time clock. TIME.'),
    'fn_lomem': ('=LOMEM', 'Read LOMEM, the start of variable storage. '
                           'LOMEM.'),
    'fn_himem': ('=HIMEM', 'Read HIMEM, the top of memory for BASIC. '
                           'HIMEM.'),
    # String functions.
    'fn_chrs': ('CHR$', 'One-character string for an ASCII code. '
                        'CHR$ numeric.'),
    'fn_strs': ('STR$', 'String form of a number (STR$~ for hex). '
                        'STR$[~] numeric.'),
    'fn_strings': ('STRING$', 'A string repeated n times. '
                              'STRING$(n, string).'),
    'fn_lefts': ('LEFT$', 'Leftmost n characters of a string. '
                          'LEFT$(string, n).'),
    'fn_rights': ('RIGHT$', 'Rightmost n characters of a string. '
                            'RIGHT$(string, n).'),
    'fn_mids': ('MID$', 'Substring from a start position. '
                        'MID$(string, start [,length]).'),
    'fn_gets': ('GET$', 'Read a key as a one-character string, or a byte / '
                        'line from a file. GET$[#channel].'),
    'fn_inkeys': ('INKEY$', 'Read a key within a time limit as a string. '
                            'INKEY$ numeric.'),
    'fn_fn': ('FN', 'Call a user-defined function and return its value. '
                    'FNname[(params)].'),
    # Statement handlers (behaviour written here; syntax forms cross-
    # checked against JGH and the BBC User Guide).
    'stmt_auto': ('AUTO', 'Generate line numbers automatically during '
                          'program entry until Escape. AUTO [start[,step]].'),
    'stmt_bput': ('BPUT', 'Write a byte to an open file. '
                          'BPUT#channel, value.'),
    'stmt_call': ('CALL', 'Call machine code, passing the resident integer '
                          'variables and an optional parameter block. '
                          'CALL address [,params...].'),
    'stmt_chain': ('CHAIN', 'Load a BASIC program and run it. CHAIN string.'),
    'stmt_clear': ('CLEAR', 'Discard all variables and the stack. CLEAR.'),
    'stmt_clg': ('CLG', 'Clear the graphics window to the graphics '
                        'background colour. CLG.'),
    'stmt_close': ('CLOSE', 'Close an open file, or all files with #0. '
                            'CLOSE#channel.'),
    'stmt_cls': ('CLS', 'Clear the text window to the text background '
                        'colour. CLS.'),
    'stmt_colour': ('COLOUR', 'Select the text colour or redefine a logical '
                              'colour. COLOUR n.'),
    'stmt_data': ('DATA / DEF / REM / ELSE',
                  'Skip to the end of the line. DATA introduces inline data '
                  '(read by READ), DEF a PROC/FN definition, REM a comment, '
                  'and ELSE the alternative of a taken IF: none execute '
                  'inline, so all four share this skip-to-end handler.'),
    'stmt_delete': ('DELETE', 'Delete a range of program lines. '
                              'DELETE start, end.'),
    'stmt_dim': ('DIM', 'Dimension an array, or reserve a block of bytes. '
                        'DIM var(subscripts) | DIM var size.'),
    'stmt_draw': ('DRAW', 'Draw a line from the graphics cursor to a point '
                          '(PLOT 5). DRAW x, y.'),
    'stmt_end': ('END', 'End the program and return to the immediate '
                        'prompt. END.'),
    'stmt_endproc': ('ENDPROC', 'Return from a procedure, restoring LOCAL '
                                'values and the caller\'s text pointer. '
                                'ENDPROC.'),
    'stmt_envelope': ('ENVELOPE', 'Define a pitch/amplitude envelope for '
                                  'SOUND. ENVELOPE n,t,... (14 parameters).'),
    'stmt_for': ('FOR', 'Begin a counted loop, stacking the control '
                        'variable, limit and step. '
                        'FOR var = start TO limit [STEP step].'),
    'stmt_gcol': ('GCOL', 'Set the graphics colour and plotting action. '
                          'GCOL action, colour.'),
    'stmt_gosub': ('GOSUB', 'Call a subroutine at a line number, stacking '
                            'the return position. GOSUB line.'),
    'stmt_goto': ('GOTO', 'Jump to a line number. GOTO line.'),
    'stmt_himem': ('HIMEM=', 'Set HIMEM, the top of memory available to '
                             'BASIC. HIMEM = address.'),
    'stmt_if': ('IF', 'Conditional execution: evaluate the expression and '
                      'run the THEN part, else skip to ELSE or the end of '
                      'the line. IF expr [THEN] ... [ELSE ...].'),
    'stmt_input': ('INPUT', 'Read values from the keyboard, or a file with '
                            '#, into variables. INPUT [LINE] [prompt] '
                            'var,...'),
    'stmt_let': ('LET', 'Assign an expression to a variable; the LET '
                        'keyword is optional. [LET] var = expr.'),
    'stmt_list': ('LIST', 'List program lines, de-tokenising them. '
                          'LIST [start[,end]].'),
    'stmt_load': ('LOAD', 'Load a BASIC program without running it. '
                          'LOAD string.'),
    'stmt_local': ('LOCAL', 'Make variables local to the current PROC/FN, '
                            'stacking their old values. LOCAL var,...'),
    'stmt_lomem': ('LOMEM=', 'Set LOMEM, the start of variable storage. '
                             'LOMEM = address.'),
    'stmt_mode': ('MODE', 'Select a screen mode, resetting the display. '
                          'MODE n.'),
    'stmt_move': ('MOVE', 'Move the graphics cursor without drawing '
                          '(PLOT 4). MOVE x, y.'),
    'stmt_new': ('NEW', 'Clear the current program and its variables. NEW.'),
    'stmt_next': ('NEXT', 'End a FOR loop: update the counter and loop back '
                          'unless the limit is passed. NEXT [var,...].'),
    'stmt_old': ('OLD', 'Recover the program cleared by NEW, if memory is '
                        'intact. OLD.'),
    'stmt_on': ('ON', 'ON expr GOTO/GOSUB computed jump, or ON ERROR error '
                      'trapping. ON expr GOTO/GOSUB list | ON ERROR stmts.'),
    'stmt_oscli': ('OSCLI', 'Pass a string to the OS command-line '
                            'interpreter. OSCLI string.'),
    'stmt_page': ('PAGE=', 'Set PAGE, the start of the BASIC program. '
                           'PAGE = address.'),
    'stmt_plot': ('PLOT', 'Plot a point, line or shape with a given mode. '
                          'PLOT mode, x, y.'),
    'stmt_print': ('PRINT', 'Print expressions to the screen, or a file '
                            'with #, with formatting controlled by @% and '
                            'separators. PRINT [~][items][;][,].'),
    'stmt_proc': ('PROC', 'Call a named procedure, stacking parameters and '
                          'the return position. PROCname[(params)].'),
    'stmt_ptr': ('PTR#=', 'Set the sequential pointer of an open file. '
                          'PTR#channel = position.'),
    'stmt_read': ('READ', 'Read values from DATA statements into variables. '
                          'READ var,...'),
    'stmt_renumber': ('RENUMBER', 'Renumber program lines and fix up line '
                                  'references. RENUMBER [start[,step]].'),
    'stmt_repeat': ('REPEAT', 'Begin a REPEAT...UNTIL loop, stacking the '
                              'loop position. REPEAT.'),
    'stmt_report': ('REPORT', 'Print the message for the last error. '
                              'REPORT.'),
    'stmt_restore': ('RESTORE', 'Reset the DATA pointer, optionally to a '
                                'given line. RESTORE [line].'),
    'stmt_return': ('RETURN', 'Return from a GOSUB to the stacked return '
                              'position. RETURN.'),
    'stmt_run': ('RUN', 'Run the current program from the start. RUN.'),
    'stmt_save': ('SAVE', 'Save the current program to the filing system. '
                          'SAVE string.'),
    'stmt_sound': ('SOUND', 'Make a sound on a channel. '
                            'SOUND channel, amplitude, pitch, duration.'),
    'stmt_stop': ('STOP', 'Stop the program, reporting "STOP at line nnnn". '
                          'STOP.'),
    'stmt_time': ('TIME=', 'Set the centisecond elapsed-time clock. '
                           'TIME = value.'),
    'stmt_trace': ('TRACE', 'Trace executed line numbers for debugging. '
                            'TRACE ON | OFF | line.'),
    'stmt_until': ('UNTIL', 'End a REPEAT loop: loop back unless the '
                           'condition is true. UNTIL expr.'),
    'stmt_vdu': ('VDU', 'Send bytes to the VDU drivers; ";" sends a 16-bit '
                        'word. VDU n[,|;]...'),
    'stmt_width': ('WIDTH', 'Set the output line width for PRINT. WIDTH n.'),
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
    _info = HANDLER_INFO.get(_name)
    if _info:
        d.subroutine(_target, _name, title=_info[0], description=_info[1])
    else:
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
    on_entry={'zp_iwa (&2A)': '32-bit integer'},
    on_exit={'zp_iwa': 'negated', 'X': 'preserved (A, Y, P destroyed)'},
)
d.subroutine(
    0xad71, 'iwa_abs',
    title='Make the integer accumulator positive',
    description='IWA = ABS(IWA).',
    on_entry={'zp_iwa (&2A)': '32-bit integer'},
    on_exit={'zp_iwa': 'made positive', 'X': 'preserved'},
)
d.subroutine(
    0x9c5b, 'iwa_add',
    title='Integer add',
    description='IWA = IWA + the integer operand on the BASIC stack.',
    on_entry={
        'zp_iwa (&2A)': 'one 32-bit operand',
        '(zp_stack_ptr) (&04)': 'the other operand on the BASIC stack',
        'X': '4',
    },
    on_exit={'zp_iwa': 'the sum'},
)
d.subroutine(
    0x9cc2, 'iwa_rsub',
    title='Reverse integer subtract',
    description='IWA = stacked operand - IWA.',
    on_entry={
        'zp_iwa (&2A)': 'the subtrahend',
        '(zp_stack_ptr) (&04)': 'the minuend on the BASIC stack',
        'X': '4',
    },
    on_exit={'zp_iwa': 'operand - IWA'},
)
d.subroutine(
    0x9d6d, 'iwa_mul',
    title='Integer multiply',
    description="""IWA = IWA * the stacked operand. A product wider than
16 bits is truncated to 16 significant bits.""",
    on_entry={
        'zp_iwa (&2A)': 'one factor',
        '(zp_stack_ptr) (&04)': 'the other factor on the BASIC stack',
        'zp_var_type (&27)': '4',
    },
    on_exit={'zp_iwa': 'the product'},
)
d.subroutine(
    0x9e0a, 'iwa_div',
    title='Integer divide',
    description="""IWA = IWA DIV the integer operand. Raises "Division by
zero" if the divisor is zero.""",
    on_entry={'zp_iwa (&2A)': 'the dividend'},
    on_exit={'zp_iwa': 'the quotient'},
)
d.subroutine(
    0x9e01, 'iwa_mod',
    title='Integer remainder',
    description="""IWA = IWA MOD the integer operand. Raises "Division by
zero" if the divisor is zero.""",
    on_entry={'zp_iwa (&2A)': 'the dividend'},
    on_exit={'zp_iwa': 'the remainder'},
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
    on_entry={'A': 'low byte', 'Y': 'high byte'},
    on_exit={'zp_iwa': '256*Y + A (sign-extended)'},
)
d.subroutine(
    0xb336, 'iwa_load_var',
    title='Load an integer variable into the accumulator',
    description='Copy the 4-byte integer addressed by zp_iwa into IWA.',
    on_entry={'zp_iwa (&2A/&2B)': 'a pointer to the 4-byte integer variable'},
    on_exit={'zp_iwa': 'the loaded integer', 'X': 'preserved'},
)
d.subroutine(
    0xb4c6, 'iwa_store_var',
    title='Store the accumulator into an integer variable',
    description='Copy IWA into the 4-byte integer variable addressed by &37.',
    on_entry={
        '(zp_general) (&37/&38)': 'a pointer to the integer variable',
        '&39': 'non-zero',
    },
    on_exit={'X': 'preserved'},
)
d.subroutine(
    0xaf56, 'iwa_load_zp',
    title='Load a zero-page integer variable into the accumulator',
    description='Copy a 4-byte integer from a zero-page location into IWA.',
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

# ----------------------------------------------------------------------
# Conversions (Pharo ch. 4). The interpreter converts between ASCII (in
# the string work area, SWA, &0600; length in zp_strbuf_len, &36), the
# integer accumulator and the floating-point accumulator. The radix
# flag (&15) selects decimal (0) or hex (-1); the @% fields at &0400
# control print formatting.
# ----------------------------------------------------------------------
d.subroutine(
    0xac34, 'ascii_to_number',
    title='Convert an ASCII number to a value',
    description="""Convert the ASCII number in the string work area to a value:
an integer in IWA or a real in FWA. Underlies VAL and numeric
tokenising. A binary zero is appended to the SWA.
""",
    on_entry={
        'zp_strbuf_len (&36)': 'length of the ASCII number in the SWA',
        'string work area (&0600)': 'the ASCII number',
    },
    on_exit={
        'zp_iwa / zp_fwa': 'the result (integer or real)',
        'A, zp_var_type (&27)': 'type: &40 = integer, &FF = real',
    },
)
d.subroutine(
    0x9edf, 'number_to_ascii',
    title='Convert the current value to an ASCII number',
    description="""Convert the integer (IWA) or real (FWA) value to an ASCII
string in the string work area, in decimal or hex per the radix
flag and the @% print format. Underlies PRINT and STR$.
""",
    on_entry={
        'zp_print_flag (&15)': '0 for decimal, -1 for hexadecimal',
        '@% (&0400)': 'print format fields',
        'Y': '&FF',
    },
    on_exit={
        'string work area (&0600)': 'the ASCII result',
        'zp_strbuf_len (&36)': 'length of the result',
    },
)
d.subroutine(
    0xa3e4, 'fwa_to_int',
    title='Convert the FP accumulator to an integer',
    description='Convert FWA to a 4-byte integer in IWA (variant 1).',
)
d.subroutine(
    0xa3fe, 'fwa_to_int2',
    title='Convert the FP accumulator to an integer (variant 2)',
    description='Convert FWA to a 4-byte integer in IWA (variant 2).',
)
d.subroutine(
    0xa2be, 'int_to_fwa',
    title='Convert the integer accumulator to floating point',
    description='Convert the integer in IWA to a real in FWA.',
)

# ----------------------------------------------------------------------
# Random numbers (RND). The generator is a 33-bit linear-feedback shift
# register held in the work area zp_rnd_seed (&0D-&11): &0D-&10 are a
# 32-bit little-endian value (bits 0-31) and bit 0 of &11 is bit 32.
# rnd_step advances it; the RND forms below build their results from the
# state. Verified against the running ROM (see rnd_step).
# ----------------------------------------------------------------------
d.subroutine(
    0xaf87, 'rnd_step',
    title='Advance the random-number LFSR by 32 steps',
    description="""Advance the 33-bit linear-feedback shift register in
zp_rnd_seed by exactly 32 single-bit steps (one RND call). The
register uses the primitive trinomial x^33 + x^20 + 1, i.e. taps
(33, 20, 0): each step feeds (bit 19 XOR bit 32) into bit 0 and
shifts the whole register left by one.

Per step: take byte 2 (bits 16-23), shift right 3 so bit 19 reaches
bit 0, EOR with byte 4 to bring in bit 32, rotate to put the feedback
bit into carry, then ROL the five state bytes so carry enters bit 0.
""",
)
d.subroutine(
    0xaf51, 'rnd_integer',
    title='RND: a full-range random integer',
    description="""Bare RND. Advance the generator (rnd_step) then read the
32-bit state (&0D-&10) into IWA as a signed integer, returning the
integer type (&40). The result spans the full signed 32-bit range.
""",
)
d.subroutine(
    0xaf69, 'rnd_fraction',
    title='RND(1): a random real in [0, 1)',
    description="""Advance the generator (rnd_step) then fall into rnd_repeat to
build the fraction. The value is the byte-reversed 32-bit state
divided by 2^32: a real in [0, 1).
""",
)
d.subroutine(
    0xaf6c, 'rnd_repeat',
    title='RND(0): repeat the last RND(1) without advancing',
    description="""Build the floating-point fraction from the CURRENT generator
state WITHOUT stepping it (so RND(0) repeats the last RND(1)). The
mantissa bytes m1..m4 are loaded most-significant-first from the
little-endian state &0D,&0E,&0F,&10, which byte-reverses the 32-bit
value; with exponent &80 and after normalisation the result is
state-reversed / 2^32, a real in [0, 1).
""",
)
d.subroutine(
    0xaf24, 'rnd_range',
    title='RND(X), X>=2: a random integer 1 to X',
    description="""Compute 1 + INT(RND(1) * X). int_to_fwa(X), push X
(stack_real), take a fraction (rnd_fraction), pop X back into the
operand (unstack_real), multiply (fwa_mul_var_raw), convert to an
integer (fwa_to_int) and add one (iwa_inc), giving a value in 1..X.
""",
)
d.subroutine(
    0xaf3f, 'rnd_seed',
    title='RND(-X): seed the generator and return X',
    description="""Store the integer argument into the 32-bit state (&0D-&10) and
set &11 to &40. Only bit 0 of &11 is part of the LFSR, so the
overflow bit becomes 0. Returns the argument as an integer.
""",
)
d.subroutine(
    0x9222, 'iwa_inc',
    title='Increment the integer accumulator',
    description='IWA = IWA + 1, carrying through all four bytes.',
)
d.subroutine(
    0xbd7e, 'unstack_real',
    title='Pop a real off the BASIC stack',
    description="""Point zp_fp_ptr at the 5-byte real on top of the BASIC stack
and drop it (advance the stack pointer by 5), so an FP routine can
use the popped value as its (zp_fp_ptr) operand.
""",
)
d.label(0xaf0a, 'rnd_dispatch')   # RND(expr): select the form by argument

# rnd_step (&AF87): one RND advance = 32 LFSR steps, trinomial (33,20,0)
d.comment(0xaf87, '32 single-bit steps make one RND advance', align=Align.INLINE)
d.comment(0xaf89, 'Byte 2 holds register bits 16-23', align=Align.INLINE)
d.comment(0xaf8b, 'Shift right so bit 19 (tap 20)...', align=Align.INLINE)
d.comment(0xaf8c, '...', align=Align.INLINE)
d.comment(0xaf8d, '...reaches bit 0', align=Align.INLINE)
d.comment(0xaf8e, 'EOR byte 4 to bring in bit 32: bit19 XOR bit32', align=Align.INLINE)
d.comment(0xaf90, 'Rotate the feedback bit into carry', align=Align.INLINE)
d.comment(0xaf91, 'Shift the register left, feedback into bit 0', align=Align.INLINE)
d.comment(0xaf93, 'bits 8-15', align=Align.INLINE)
d.comment(0xaf95, 'bits 16-23', align=Align.INLINE)
d.comment(0xaf97, 'bits 24-31', align=Align.INLINE)
d.comment(0xaf99, 'bit 32', align=Align.INLINE)
d.comment(0xaf9b, 'Next step', align=Align.INLINE)
d.comment(0xaf9c, 'Loop for all 32 steps', align=Align.INLINE)
d.comment(0xaf9e, 'The register has advanced', align=Align.INLINE)

# rnd_dispatch (&AF0A): RND(expr) chooses a form by the argument value
d.comment(0xaf0a, 'Skip the "("', align=Align.INLINE)
d.comment(0xaf0c, 'Evaluate the argument expression', align=Align.INLINE)
d.comment(0xaf0f, 'Coerce it to an integer', align=Align.INLINE)
d.comment(0xaf12, 'Examine the argument: high byte', align=Align.INLINE)
d.comment(0xaf14, 'Negative: re-seed the generator', align=Align.INLINE)
d.comment(0xaf16, 'Any of bits 16-31 set...', align=Align.INLINE)
d.comment(0xaf18, '...(magnitude >= 256)', align=Align.INLINE)
d.comment(0xaf1a, 'Large: RND(X) over a range', align=Align.INLINE)
d.comment(0xaf1c, 'Low byte', align=Align.INLINE)
d.comment(0xaf1e, 'RND(0): repeat the last fraction', align=Align.INLINE)
d.comment(0xaf20, 'RND(1)?', align=Align.INLINE)
d.comment(0xaf22, 'RND(1): a fresh fraction (else 2..255: RND(X))', align=Align.INLINE)

# rnd_range (&AF24): 1 + INT(RND(1) * X)
d.comment(0xaf24, 'FWA = X', align=Align.INLINE)
d.comment(0xaf27, 'Push X onto the stack', align=Align.INLINE)
d.comment(0xaf2a, 'FWA = a fraction in [0, 1)', align=Align.INLINE)
d.comment(0xaf2d, 'Pop X back as the multiply operand', align=Align.INLINE)
d.comment(0xaf30, 'FWA = fraction * X', align=Align.INLINE)
d.comment(0xaf33, 'Normalise the product', align=Align.INLINE)
d.comment(0xaf36, 'IWA = INT(fraction * X) = 0..X-1', align=Align.INLINE)
d.comment(0xaf39, 'Add one: 1..X', align=Align.INLINE)
d.comment(0xaf3c, 'Integer result', align=Align.INLINE)
d.comment(0xaf3e, 'Return RND(X)', align=Align.INLINE)

# rnd_seed (&AF3F): RND(-X)
d.comment(0xaf3f, 'Point at the state bytes (&0D)', align=Align.INLINE)
d.comment(0xaf41, 'Store the argument as the 32-bit state', align=Align.INLINE)
d.comment(0xaf44, 'Bit-32 byte =', align=Align.INLINE)
d.comment(0xaf46, '&40: bit 32 (its bit 0) becomes 0', align=Align.INLINE)
d.comment(0xaf48, 'Return the argument (A = &40 = integer)', align=Align.INLINE)

# fn_rnd (&AF49): RND with or without an argument
d.comment(0xaf49, 'Look at the character after RND', align=Align.INLINE)
d.comment(0xaf4b, '(get it)', align=Align.INLINE)
d.comment(0xaf4d, 'Is it "("? then RND(expr)', align=Align.INLINE)
d.comment(0xaf4f, 'Yes: select the RND form', align=Align.INLINE)

# rnd_integer (&AF51): bare RND
d.comment(0xaf51, 'Advance the generator', align=Align.INLINE)
d.comment(0xaf54, 'Point at the state (&0D), then copy it to IWA',
          align=Align.INLINE)

# iwa_load_zp (&AF56): copy the 4-byte integer at (&00+X) into IWA
d.comment(0xaf56, 'Copy 4-byte value at &00+X into IWA: byte 0', align=Align.INLINE)
d.comment(0xaf58, '(store)', align=Align.INLINE)
d.comment(0xaf5a, 'byte 1', align=Align.INLINE)
d.comment(0xaf5c, '(store)', align=Align.INLINE)
d.comment(0xaf5e, 'byte 2', align=Align.INLINE)
d.comment(0xaf60, '(store)', align=Align.INLINE)
d.comment(0xaf62, 'byte 3', align=Align.INLINE)
d.comment(0xaf64, '(store)', align=Align.INLINE)
d.comment(0xaf66, 'Integer type', align=Align.INLINE)
d.comment(0xaf68, 'Return the integer', align=Align.INLINE)

# rnd_fraction (&AF69) -> rnd_repeat (&AF6C): build the [0,1) fraction
d.comment(0xaf69, 'Advance the generator, then build the fraction',
          align=Align.INLINE)
d.comment(0xaf6c, 'Zero for the FP fields', align=Align.INLINE)
d.comment(0xaf6e, 'Sign positive', align=Align.INLINE)
d.comment(0xaf70, 'Clear overflow', align=Align.INLINE)
d.comment(0xaf72, 'Clear rounding', align=Align.INLINE)
d.comment(0xaf74, 'Exponent &80 (= 2^0)', align=Align.INLINE)
d.comment(0xaf76, '(store it)', align=Align.INLINE)
d.comment(0xaf78, 'State byte X (little-endian)...', align=Align.INLINE)
d.comment(0xaf7a, '...into mantissa byte X (MSB first): byte-reverses',
          align=Align.INLINE)
d.comment(0xaf7c, 'next byte', align=Align.INLINE)
d.comment(0xaf7d, 'all four?', align=Align.INLINE)
d.comment(0xaf7f, 'loop', align=Align.INLINE)
d.comment(0xaf81, 'Normalise: value = reversed-state / 2^32', align=Align.INLINE)
d.comment(0xaf84, 'Real result type', align=Align.INLINE)
d.comment(0xaf86, 'Return RND(1) / RND(0)', align=Align.INLINE)

# iwa_inc (&9222): 32-bit IWA = IWA + 1
d.comment(0x9222, 'Increment IWA: byte 0', align=Align.INLINE)
d.comment(0x9224, 'No carry: done', align=Align.INLINE)
d.comment(0x9226, 'Carry into byte 1', align=Align.INLINE)
d.comment(0x9228, 'done', align=Align.INLINE)
d.comment(0x922a, 'byte 2', align=Align.INLINE)
d.comment(0x922c, 'done', align=Align.INLINE)
d.comment(0x922e, 'byte 3', align=Align.INLINE)
d.comment(0x9230, 'IWA incremented', align=Align.INLINE)

# unstack_real (&BD7E): pop a 5-byte real, leaving zp_fp_ptr at it
d.comment(0xbd7e, 'Stack top is where the real sits...', align=Align.INLINE)
d.comment(0xbd80, 'clear carry for the add', align=Align.INLINE)
d.comment(0xbd81, '...point the fp operand there', align=Align.INLINE)
d.comment(0xbd83, 'Drop 5 bytes (a packed real)', align=Align.INLINE)
d.comment(0xbd85, '(store the new stack low byte)', align=Align.INLINE)
d.comment(0xbd87, 'Stack-pointer high byte', align=Align.INLINE)
d.comment(0xbd89, 'into the fp-operand pointer too', align=Align.INLINE)
d.comment(0xbd8b, 'Carry into the high byte', align=Align.INLINE)
d.comment(0xbd8d, '(store it)', align=Align.INLINE)
d.comment(0xbd8f, 'zp_fp_ptr now addresses the popped real', align=Align.INLINE)

# ======================================================================
# Inline comments, added bottom-up from the call-graph leaves. The aim
# is to explain intent and the structures involved, not to restate the
# opcodes (the field labels already carry much of that).
# ======================================================================

# --- fwa_sign (&A1DA): sign of FWA in A (Z=zero, N=negative, +1=pos) --
d.comment(0xa1da, 'OR the mantissa and rounding bytes to test for zero',
          align=Align.INLINE)
d.comment(0xa1dc, '(mantissa byte 2)', align=Align.INLINE)
d.comment(0xa1de, '(mantissa byte 3)', align=Align.INLINE)
d.comment(0xa1e0, '(mantissa byte 4)', align=Align.INLINE)
d.comment(0xa1e2, '(rounding) - a non-zero value is never all zero',
          align=Align.INLINE)
d.comment(0xa1e4, 'All zero: clean up and return zero', align=Align.INLINE)
d.comment(0xa1e6, 'Non-zero: the sign is in bit 7 of the sign byte',
          align=Align.INLINE)
d.comment(0xa1e8, 'Bit 7 set: negative, return with A < 0', align=Align.INLINE)
d.comment(0xa1ea, 'Otherwise positive: return A = +1', align=Align.INLINE)
d.comment(0xa1ec, 'A and the flags now give the sign', align=Align.INLINE)
d.comment(0xa1ed, 'Zero path: force a clean zero - sign,', align=Align.INLINE)
d.comment(0xa1ef, 'exponent,', align=Align.INLINE)
d.comment(0xa1f1, 'and overflow byte, then return A = 0', align=Align.INLINE)

# --- iwa_from_ya: build a 16-bit (unsigned) integer in the IWA -------
d.comment(0xaeee, 'Clear the top 16 bits: the result is 0-65535',
          align=Align.INLINE)
d.comment(0xaef4, 'Report the value as an integer (type &40)',
          align=Align.INLINE)

# --- fwa_unpack_var: packed 5-byte -> unpacked 8-byte FWA ------------
d.comment(0xa3b5, 'Copy the packed value, exponent last',
          align=Align.INLINE)
d.comment(0xa3c8, 'Packed mantissa MSB holds the sign in bit 7',
          align=Align.INLINE)
d.comment(0xa3cf, 'Clear the rounding and overflow bytes (Y=0)',
          align=Align.INLINE)
d.comment(0xa3d3, 'A=exponent; OR the mantissa to test for zero',
          align=Align.INLINE)
d.comment(0xa3db, 'All zero: leave the mantissa MSB clear',
          align=Align.INLINE)
d.comment(0xa3df, 'Non-zero: restore the implied leading 1',
          align=Align.INLINE)

# --- renames discovered during the leaf pass --------------------------
d.subroutine(
    0xa2a4, 'fwa_round_carry',
    title='Add to the rounding byte and ripple the carry up',
    description="""Add A to the FWA rounding byte, then propagate any carry up
through the mantissa (m4 -> m1). A carry out of the top renormalises
the exponent (and may overflow). Used to round the mantissa up.
""",
)
d.label(0xa66c, 'err_too_big')   # BRK error block: "Too big"
d.label(0x8cb7, 'err_no_room')   # BRK error block: "No room"

# --- reserve_stack: the common stack-overflow check for the pushers ---
d.subroutine(
    0xbe2e, 'reserve_stack',
    title='Set the stack pointer and check for room',
    description="""Set the BASIC value-stack pointer to a new top (low byte in A,
borrow already taken into the high byte) and check it has not run
down into the top of variable storage (zp_vartop). Raises "No room"
on collision; otherwise returns with the stack lowered.
""",
    on_entry={'A': 'proposed new stack-pointer low byte',
              'carry': 'clear if the subtraction borrowed'},
)
d.comment(0xbe36, 'Compare the new top against the heap top', align=Align.INLINE)
d.comment(0xbe41, 'Stack meets heap: No room', align=Align.INLINE)

# --- BASIC value-stack push/pop primitives ---------------------------
d.comment(0xbd97, 'Lower the stack by 4 bytes (an integer)', align=Align.INLINE)
d.comment(0xbd54, 'Lower the stack by 5 bytes (a packed real)',
          align=Align.INLINE)
d.comment(0xbd62, 'Pack: fold the sign into the mantissa MSB', align=Align.INLINE)
d.comment(0xbdb5, 'Lower the stack by length+1 bytes (carry clear)',
          align=Align.INLINE)

# --- fwa_pack_var: unpacked FWA -> packed 5-byte at (zp_fp_ptr) -------
d.comment(0xa396, 'Isolate the sign bit', align=Align.INLINE)
d.comment(0xa39c, 'Drop the implied leading 1 from the mantissa MSB',
          align=Align.INLINE)
d.comment(0xa39e, 'and fold the sign back into its bit 7', align=Align.INLINE)

# --- fwa_normalise: shift the mantissa until bit 7 of m1 is set -------
d.comment(0xa305, 'Top bit already set: nothing to do', align=Align.INLINE)
d.comment(0xa30d, 'Mantissa entirely zero: the value is zero',
          align=Align.INLINE)
d.comment(0xa313, 'Shift up a whole byte while the MSB byte is zero',
          align=Align.INLINE)
d.comment(0xa32c, 'each byte shift advances the exponent by 8',
          align=Align.INLINE)
d.comment(0xa33a, 'Then shift left one bit at a time to normalise',
          align=Align.INLINE)

# --- fwa_round: round FWA using the rounding byte ---------------------
d.comment(0xa65c, 'The rounding byte holds the bits below the LSB',
          align=Align.INLINE)
d.comment(0xa660, 'Below half: round down (truncate)', align=Align.INLINE)
d.comment(0xa662, 'Exactly half: special-case the LSB', align=Align.INLINE)
d.comment(0xa664, 'Above half: round up by adding 1', align=Align.INLINE)
d.comment(0xa67c, 'Clear the now-spent rounding byte', align=Align.INLINE)
d.comment(0xa680, 'A carry may have overflowed the mantissa', align=Align.INLINE)
d.comment(0xa684, 'Overflowed the exponent range: Too big', align=Align.INLINE)

# --- floating-point addition (FWA = FWA + FWB) -----------------------
# Align the two operands by the difference of their exponents (shifting
# the smaller mantissa right), then add the mantissas if the signs
# match or subtract the smaller from the larger if they differ.
d.label(0xa5df, 'fp_mantissas_add')   # same-sign path: add the mantissas
d.label(0xa5b7, 'fp_mantissas_sub')   # opposite-sign path: subtract
d.comment(0xa503, 'Adding zero leaves FWA unchanged', align=Align.INLINE)
d.comment(0xa50e, 'FWA is zero: the sum is simply FWB', align=Align.INLINE)
d.comment(0xa515, 'Exponent difference is the alignment shift',
          align=Align.INLINE)
d.comment(0xa517, 'Equal exponents: already aligned', align=Align.INLINE)
d.comment(0xa519, 'FWA the smaller: align it to FWB instead',
          align=Align.INLINE)
d.comment(0xa51d, 'Differ by >= 37 bits: FWB too small to count',
          align=Align.INLINE)
d.comment(0xa520, 'Whole-byte part of the shift (difference / 8)',
          align=Align.INLINE)
d.comment(0xa528, 'Shift FWB down a byte at a time', align=Align.INLINE)
d.comment(0xa53e, 'then the remaining bits, to finish aligning FWB',
          align=Align.INLINE)
d.comment(0xa552, 'FWB the smaller: shift FWA to align', align=Align.INLINE)
d.comment(0xa58c, 'Result takes the larger exponent', align=Align.INLINE)
d.comment(0xa592, 'Compare the operand signs', align=Align.INLINE)
d.comment(0xa594, 'Same sign: add; opposite: subtract smaller from larger',
          align=Align.INLINE)
d.comment(0xa5b4, 'Equal magnitudes of opposite sign cancel to zero',
          align=Align.INLINE)

# --- interpreter core: execute_line / statement_loop / dispatch ------
d.comment(0x8b0b, 'Restore the default error handler (ON ERROR OFF)',
          align=Align.INLINE)
d.comment(0x8b13, 'OPT = &FF: not inside the [ ] assembler', align=Align.INLINE)
d.comment(0x8b19, 'Reset the 6502 hardware stack', align=Align.INLINE)
d.comment(0x8b1a, 'Clear the DATA pointer and the BASIC stacks',
          align=Align.INLINE)
d.comment(0x8b1e, 'Point the general pointer at the line text',
          align=Align.INLINE)
d.comment(0x8b2d, 'Tokenise; carry set if the line starts with a number',
          align=Align.INLINE)
d.comment(0x8b32, 'Numbered line: insert it into the program', align=Align.INLINE)
d.comment(0x8b3b, 'Token >= &C6 is a command: dispatch it', align=Align.INLINE)
d.comment(0x8b3f, 'Otherwise treat it as a variable assignment',
          align=Align.INLINE)
d.comment(0x8b65, '"=" returns a value from a function (FN)', align=Align.INLINE)
d.comment(0x8b69, '"*" passes the rest of the line to OSCLI', align=Align.INLINE)
d.comment(0x8b6d, '"[" enters the inline assembler', align=Align.INLINE)
d.comment(0x8b9b, 'Fetch the next character of the statement',
          align=Align.INLINE)
d.comment(0x8b9f, 'A colon separates statements on a line', align=Align.INLINE)
d.comment(0x8ba3, 'Skip spaces to the next statement', align=Align.INLINE)
d.comment(0x8bad, 'Below &CF: a variable assignment, not a command',
          align=Align.INLINE)
d.comment(0x8bb2, 'Handler low byte = action_table_lo[token - &8E]',
          align=Align.INLINE)
d.comment(0x8bb7, 'Handler high byte from action_table_hi', align=Align.INLINE)
d.comment(0x8bbc, 'Jump to the keyword handler', align=Align.INLINE)
d.label(0x8b73, 'exec_star_command')   # embedded *command -> OSCLI

# --- tokeniser character scan (front end of tokenise) ----------------
# Walks the source line at (zp_general), passing literals through
# untouched and resetting state at statement boundaries; keyword
# matching against keyword_table follows. NB &3B/&3C (normally FWB) are
# reused here as tokeniser state: start-of-statement and quote flags.
d.comment(0x8951, 'Tokeniser state (&3B/&3C): start of statement',
          align=Align.INLINE)
d.comment(0x8957, 'Scan the next source character', align=Align.INLINE)
d.comment(0x895b, 'Carriage return ends the line', align=Align.INLINE)
d.comment(0x895f, 'Skip spaces', align=Align.INLINE)
d.comment(0x8966, 'An "&" introduces a hex constant: copy it unchanged',
          align=Align.INLINE)
d.comment(0x897c, 'A quote starts a string literal: copy it verbatim',
          align=Align.INLINE)
d.comment(0x898c, 'A colon starts a new statement: reset the state',
          align=Align.INLINE)
d.comment(0x899a, 'A "*" at statement start: rest is a *command',
          align=Align.INLINE)

# --- variable / PROC / FN lookup -------------------------------------
# Variables live in linked lists, one per initial character (plus PROC
# and FN lists), headed by the pointers in var_ptr_table. Each entry is
# a 2-byte link to the next, the rest of the name (first letter implied
# by the list) and a NUL, then the value. The chain pointer is held in
# &3A-&3D (the FWB / general bytes, reused here).
d.subroutine(
    0x945b, 'find_proc_fn',
    title='Find a PROC or FN definition by name',
    description="""Search the PROC (token &F2) or FN linked list for a definition
whose name starts at (zp_general)+1. Shares the chain walk with
find_variable; returns a pointer to the body, or "not found".
""",
)
d.subroutine(
    0x9469, 'find_variable',
    title='Find a variable by name',
    description="""Search the heap for a variable whose name starts at
(zp_general)+1. The initial character selects one of the per-letter
linked lists via the variable table; the chain is walked comparing
the rest of the name. On a match, returns a pointer to the value in
zp_iwa/zp_iwa_1; otherwise reports it is not present.
""",
)
d.comment(0x945f, 'Index the PROC / FN entries of the variable table',
          align=Align.INLINE)
d.comment(0x946d, 'Two bytes per entry: double the initial letter',
          align=Align.INLINE)
d.comment(0x946f, 'Head of the chain from the variable table (&0400+2*ch)',
          align=Align.INLINE)
d.comment(0x9479, 'End of the chain: variable not found', align=Align.INLINE)
d.comment(0x9495, 'Compare the rest of the name against this entry',
          align=Align.INLINE)
d.comment(0x94a7, 'Match: return a pointer to the value', align=Align.INLINE)
d.comment(0x94b3, 'No match: follow the link to the next entry',
          align=Align.INLINE)

# --- expression evaluator: the operator-precedence ladder ------------
# eval_expr enters at the lowest precedence and each level calls the
# next-higher one for its operands, then applies its own operators in a
# loop. Each level returns the next (unconsumed) operator token in X and
# the result type in A / zp_var_type. Level 1 (eval_factor) handles
# unary operators, parentheses, literals and functions.
for _addr, _name, _title, _desc in [
    (0x9b29, 'eval_or_eor', 'Evaluator level 7: OR, EOR',
     'Lowest precedence: bitwise OR (&84) and EOR (&82) on integers.'),
    (0x9b72, 'eval_and', 'Evaluator level 6: AND',
     'Bitwise AND (&80) on integers.'),
    (0x9b9c, 'eval_relational', 'Evaluator level 5: < <= = >= > <>',
     'The relational operators, yielding TRUE (-1) or FALSE (0).'),
    (0x9c42, 'eval_add_sub', 'Evaluator level 4: + -',
     'Addition and subtraction (numeric, or string concatenation).'),
    (0x9dd1, 'eval_mul_div', 'Evaluator level 3: * / DIV MOD',
     'Multiplication, division and the integer DIV and MOD operators.'),
]:
    d.subroutine(_addr, _name, title=_title, description=_desc)

d.comment(0x9b1d, 'Start evaluating: copy PtrA to the working PtrB',
          align=Align.INLINE)
d.comment(0x9b29, 'Evaluate the higher-precedence (AND) operand first',
          align=Align.INLINE)
d.comment(0x9b2c, 'Is the next operator OR or EOR at this level?',
          align=Align.INLINE)
d.comment(0x9b3a, 'OR: stack the left operand, evaluate the right',
          align=Align.INLINE)
d.comment(0x9b43, 'Combine the two integers with OR', align=Align.INLINE)
d.comment(0x9b53, 'Loop to handle any further OR / EOR', align=Align.INLINE)
d.comment(0x9b75, 'Apply AND only if the next operator is AND',
          align=Align.INLINE)
d.comment(0x9c45, 'Apply + or - if that is the next operator',
          align=Align.INLINE)

# --- FOR / NEXT: counted loops on the FOR stack ----------------------
# Each FOR pushes a 15-byte frame on the FOR/GOSUB stack (&0500),
# indexed by zp_for_level (= 15 * the nesting depth): the control-
# variable pointer, the limit and the step, plus the loop-back position.
d.comment(0xb7c4, 'Parse the control variable (numvar =)', align=Align.INLINE)
d.comment(0xb7cb, 'Evaluate and assign the initial value', align=Align.INLINE)
d.comment(0xb7d4, 'Index the FOR stack by nesting level', align=Align.INLINE)
d.comment(0xb7d6, 'At most 10 nested FOR loops (10 * 15)', align=Align.INLINE)
d.comment(0xb7da, 'Save the control-variable pointer in the frame',
          align=Align.INLINE)
d.comment(0xb7ed, 'Require the TO keyword', align=Align.INLINE)
d.comment(0xb7fa, 'Save the loop limit in the frame', align=Align.INLINE)
d.comment(0xb816, 'Optional STEP (otherwise step defaults to 1)',
          align=Align.INLINE)
d.comment(0xb695, 'Parse the optional control variable', align=Align.INLINE)
d.comment(0xb6a9, 'Find the matching FOR frame on the stack', align=Align.INLINE)
d.comment(0xb6be, 'Not this loop: discard the frame and look outward',
          align=Align.INLINE)
d.comment(0xb6d7, 'Found: reload the control variable to update it',
          align=Align.INLINE)

# --- GOSUB / GOTO / RETURN and line lookup ---------------------------
# The GOSUB stack keeps 26 return text-pointers in parallel arrays at
# &05CC (low) / &05E6 (high), indexed by zp_gosub_level.
d.subroutine(
    0xb99a, 'find_line_target',
    title='Resolve a line-number operand to a program line',
    description="""Read a line-number argument (an embedded tokenised line number
or an evaluated integer expression) and locate that line in the
program via find_program_line. Used by GOTO, GOSUB and RESTORE.
Raises "No such line" if absent.
""",
)
d.subroutine(
    0x9970, 'find_program_line',
    title='Search the program for a line number',
    description="""Walk the program text looking for the given line number,
returning a pointer to the line (carry set if found).
""",
)
d.label(0xb8a2, 'err_too_many_gosubs')   # GOSUB stack full
d.label(0xb8af, 'err_no_gosub')          # RETURN with no GOSUB pending
d.label(0xb9b5, 'err_no_such_line')      # line number not in the program
d.comment(0xb888, 'Resolve the destination line', align=Align.INLINE)
d.comment(0xb88e, 'Index the GOSUB return stack', align=Align.INLINE)
d.comment(0xb890, 'At most 26 nested GOSUBs', align=Align.INLINE)
d.comment(0xb894, 'Push the return position (text pointer)', align=Align.INLINE)
d.comment(0xb8b9, 'RETURN with nothing on the GOSUB stack: error',
          align=Align.INLINE)
d.comment(0xb8bd, 'Pop the return position', align=Align.INLINE)
d.comment(0xb8c9, 'Resume execution after the GOSUB', align=Align.INLINE)
d.comment(0xb8d2, 'TRACE: report the destination line number',
          align=Align.INLINE)
d.comment(0xb8dd, 'Point the interpreter at the destination line',
          align=Align.INLINE)

# --- REPEAT / UNTIL: condition loop on a 20-entry stack --------------
# REPEAT saves the loop-start position in parallel arrays at &05A4 (low)
# / &05B8 (high), indexed by zp_repeat_level; UNTIL exits when the
# condition is true, otherwise loops back.
d.label(0xbba6, 'err_no_repeat')         # UNTIL with no REPEAT pending
d.label(0xbbd6, 'err_too_many_repeats')  # REPEAT stack full
d.comment(0xbbe4, 'Index the REPEAT stack', align=Align.INLINE)
d.comment(0xbbe6, 'At most 20 nested REPEATs', align=Align.INLINE)
d.comment(0xbbed, 'Push the loop-start position', align=Align.INLINE)
d.comment(0xbbb1, 'Evaluate the UNTIL condition', align=Align.INLINE)
d.comment(0xbbba, 'UNTIL with no REPEAT pending: error', align=Align.INLINE)
d.comment(0xbbc6, 'Condition false: loop back to the REPEAT', align=Align.INLINE)
d.comment(0xbbc8, 'Condition true: pop the frame and continue',
          align=Align.INLINE)
d.comment(0xbbcd, 'Reload the saved loop-start position', align=Align.INLINE)

# --- LET assignment --------------------------------------------------
d.subroutine(
    0x9582, 'parse_lvalue',
    title='Parse an assignment target variable',
    description="""Parse the variable reference being assigned to and return a
pointer to its storage plus its type, creating the variable if it
does not yet exist. Shared by LET and FOR.
""",
)
d.subroutine(
    0x9813, 'eval_after_eq',
    title='Expect "=" then evaluate the right-hand side',
    description="""Skip spaces, require an "=" sign, then evaluate the expression
that follows, leaving the value in the accumulator with its type in
zp_var_type.
""",
)
d.subroutine(
    0x8c1e, 'assign_string',
    title='Store a string value into a variable',
    description="""Assign the string in the string buffer to the string variable
whose descriptor address is on the stack. Reuses the existing
allocation if the new string fits, otherwise grabs fresh space from
the heap.
""",
)
d.subroutine(
    0xb4b4, 'assign_number',
    title='Store a numeric value into a variable',
    description="""Assign the current numeric value (integer or real) to the
variable whose address is on the stack, in the variable's own type.
""",
)
d.label(0x8c0e, 'err_type_mismatch')   # BRK error block: "Type mismatch"
d.comment(0x8be4, 'Parse the variable being assigned', align=Align.INLINE)
d.comment(0x8beb, 'Stack the destination address', align=Align.INLINE)
d.comment(0x8bee, 'Expect "=" and evaluate the right-hand side',
          align=Align.INLINE)
d.comment(0x8bf3, 'A string variable needs a string value', align=Align.INLINE)
d.comment(0x8bf5, 'Store the string', align=Align.INLINE)
d.comment(0x8c03, 'A numeric variable needs a numeric value', align=Align.INLINE)
d.comment(0x8c05, 'Store the number', align=Align.INLINE)
d.comment(0x8c23, 'An absolute $-string address?', align=Align.INLINE)
d.comment(0x8c2b, 'Does the new string fit the existing allocation?',
          align=Align.INLINE)
d.comment(0x8c2f, 'Otherwise allocate space from the heap', align=Align.INLINE)

# --- PRINT: items, separators and @% formatting ----------------------
# The field width and hex/decimal flag come from @% (resint_at, &0400);
# zp_print_bytes is the current field width and zp_print_flag selects
# hex. Items are evaluated then printed, numbers right-justified.
d.subroutine(
    0x8e70, 'print_special_item',
    title="Handle the PRINT ' TAB and SPC items",
    description="""Recognise and act on the special PRINT items: apostrophe
(force a newline), TAB(x[,y]) and SPC(n). Returns carry clear when
it consumed one, so the caller skips ordinary expression printing.
""",
)
d.comment(0x8d9d, 'A leading # directs output to a file (PRINT#)',
          align=Align.INLINE)
d.comment(0x8da6, 'Comma: pad with spaces to the next @% field',
          align=Align.INLINE)
d.comment(0x8dbc, 'Take the field width from @% (&0400)', align=Align.INLINE)
d.comment(0x8dc1, 'A tilde "~" switches to hexadecimal', align=Align.INLINE)
d.comment(0x8dd6, 'Comma: advance to the next print field', align=Align.INLINE)
d.comment(0x8dda, 'Semicolon: print the next item with no gap',
          align=Align.INLINE)
d.comment(0x8dde, "Handle the ' TAB and SPC print items", align=Align.INLINE)
d.comment(0x8deb, 'Evaluate the expression to print', align=Align.INLINE)
d.comment(0x8df9, 'A string value: print it directly', align=Align.INLINE)
d.comment(0x8dfb, 'A number: convert to an ASCII string', align=Align.INLINE)
d.comment(0x8dfe, 'and right-justify it within the field width',
          align=Align.INLINE)

# --- PROC / FN / LOCAL / ENDPROC -------------------------------------
d.subroutine(
    0xb197, 'call_proc_fn',
    title='Enter a PROC or FN',
    description="""The procedure/function call mechanism. First copies the live
6502 hardware stack onto the BASIC value stack and resets the
hardware stack -- this is how BBC BASIC lets PROCs and FNs nest far
beyond the 256-byte 6502 stack. Then pushes the call context (the
PROC/FN token and the caller's text pointers), locates the named
definition, binds any parameters, and transfers control to the body.
ENDPROC / =expr unwind this frame.
""",
    on_entry={'A': 'PROC token &F2 or FN token &A4'},
)
d.subroutine(
    0xb30d, 'stack_local',
    title='Save a variable for LOCAL',
    description="""Push a variable's current value and identity onto the BASIC
stack so ENDPROC can restore it, implementing LOCAL.
""",
)
d.comment(0x9304, "Remember the call site in PtrB", align=Align.INLINE)
d.comment(0x9310, 'Enter the procedure (PROC token &F2)', align=Align.INLINE)
d.comment(0xb199, 'Copy the 6502 stack onto the BASIC stack', align=Align.INLINE)
d.comment(0xb19e, 'so procedures can nest far beyond 256 bytes',
          align=Align.INLINE)
d.comment(0xb1b4, "Push the call context and return pointers", align=Align.INLINE)
d.comment(0x9323, 'LOCAL is only meaningful inside a PROC/FN', align=Align.INLINE)
d.comment(0x932d, "Save the variable's value for restoration", align=Align.INLINE)
d.comment(0x9337, 'Initialise the local to zero / empty', align=Align.INLINE)
d.comment(0x934c, 'A comma introduces another LOCAL', align=Align.INLINE)
d.comment(0x9356, 'ENDPROC needs a PROC frame on the stack', align=Align.INLINE)
d.comment(0x935e, 'The framed call must be a PROC', align=Align.INLINE)
d.comment(0x9362, 'Return to the caller, restoring locals', align=Align.INLINE)

# ======================================================================
# DEPTH 0 LEAVES — full per-instruction coverage (see ANNOTATION_PROGRESS)
# ======================================================================

# shared return points and small helpers filling the leaf extents
d.comment(0xa1f3, 'Return (shared)', align=Align.INLINE)
d.comment(0xa2bd, 'Return (shared)', align=Align.INLINE)
d.comment(0xaece, 'String operand here is a Type mismatch', align=Align.INLINE)

# fwb_half_fwa (&A23F) / fwb_div2 (&A242): FWB = FWA / 2, and FWB >>= 1
d.subroutine(0xa242, 'fwb_div2', title='Divide FWB by two',
             description='Shift the FWB mantissa right one bit (FWB = FWB / 2).')
d.label(0xa23f, 'fwb_half_fwa')   # FWB = FWA, then halve it
d.comment(0xa23f, 'FWB = FWA, then halve it', align=Align.INLINE)
d.comment(0xa242, 'Shift FWB right one bit (/2): mantissa MSB', align=Align.INLINE)
d.comment(0xa244, 'byte 2', align=Align.INLINE)
d.comment(0xa246, 'byte 3', align=Align.INLINE)
d.comment(0xa248, 'byte 4', align=Align.INLINE)
d.comment(0xa24a, 'rounding byte', align=Align.INLINE)
d.comment(0xa24c, 'FWB halved', align=Align.INLINE)

# fwa_pack_temp2/3 (&A37D/&A381): point at FP TEMP2/TEMP3, then pack
d.comment(0xa37d, 'Point at FP TEMP2 (&0471): low byte', align=Align.INLINE)
d.comment(0xa37f, 'join the common pack code', align=Align.INLINE)
d.comment(0xa381, 'Point at FP TEMP3 (&0476): low byte', align=Align.INLINE)
d.comment(0xa383, 'join the common pack code', align=Align.INLINE)

# stack_value (&BD90): push the current value, choosing format by type
d.subroutine(0xbd90, 'stack_value', title='Push the current value by type',
             description="""Push the current value onto the BASIC stack in the form
matching its type: a string (stack_string), a real (stack_real) or,
falling through, an integer (stack_integer).""")
d.comment(0xbd90, 'Type 0 (string): stack as a string', align=Align.INLINE)
d.comment(0xbd92, 'Negative (real): stack 5 bytes; else integer below',
          align=Align.INLINE)

# drop_stack_integer (&BDFF): advance the stack pointer past a 4-byte int
d.subroutine(0xbdff, 'drop_stack_integer', title='Drop an integer off the stack',
             description='Advance the BASIC stack pointer by four bytes.')
d.comment(0xbdff, 'Prepare to add', align=Align.INLINE)
d.comment(0xbe00, 'Drop four bytes: stack pointer...', align=Align.INLINE)
d.comment(0xbe02, '...+ 4', align=Align.INLINE)
d.comment(0xbe04, '(store)', align=Align.INLINE)
d.comment(0xbe06, 'No carry: done', align=Align.INLINE)
d.comment(0xbe08, 'Carry into the high byte', align=Align.INLINE)
d.comment(0xbe0a, 'Return (shared)', align=Align.INLINE)

# unstack_int_to_zp (&BE0D): pop the stacked integer into 4 zp bytes at X
d.subroutine(0xbe0d, 'unstack_int_to_zp',
             title='Pop a stacked integer into a zero-page variable',
             description="""Copy the four-byte integer on top of the BASIC stack into
the zero-page bytes at (X .. X+3), then drop it from the stack. The
&BE0B entry uses X = &37 (the general work area).""")
d.label(0xbe0b, 'unstack_int_to_general')
d.comment(0xbe0b, 'Default destination: zp_general (&37)', align=Align.INLINE)
d.comment(0xbe0d, 'Copy the stacked integer to (X): top byte', align=Align.INLINE)
d.comment(0xbe0f, '(read)', align=Align.INLINE)
d.comment(0xbe11, '...byte 3', align=Align.INLINE)
d.comment(0xbe13, 'next', align=Align.INLINE)
d.comment(0xbe14, '(read)', align=Align.INLINE)
d.comment(0xbe16, 'byte 2', align=Align.INLINE)
d.comment(0xbe18, 'next', align=Align.INLINE)
d.comment(0xbe19, '(read)', align=Align.INLINE)
d.comment(0xbe1b, 'byte 1', align=Align.INLINE)
d.comment(0xbe1d, 'next', align=Align.INLINE)
d.comment(0xbe1e, '(read)', align=Align.INLINE)
d.comment(0xbe20, 'byte 0', align=Align.INLINE)
d.comment(0xbe22, 'Now drop the integer from the stack', align=Align.INLINE)
d.comment(0xbe23, 'stack pointer...', align=Align.INLINE)
d.comment(0xbe25, '...+ 4', align=Align.INLINE)
d.comment(0xbe27, '(store)', align=Align.INLINE)
d.comment(0xbe29, 'No carry: done', align=Align.INLINE)
d.comment(0xbe2b, 'Carry into the high byte', align=Align.INLINE)
d.comment(0xbe2d, 'Return', align=Align.INLINE)

# fn_eof (&ACB8): EOF#channel
d.comment(0xacb8, 'Evaluate the channel number', align=Align.INLINE)
d.comment(0xacbb, 'Channel to X', align=Align.INLINE)
d.comment(0xacbc, 'OSBYTE &7F: test for end of file', align=Align.INLINE)
d.comment(0xacc2, 'Return TRUE/FALSE per the EOF flag', align=Align.INLINE)

# fn_get (&AFB9): GET; fn_pos (&AB6D): POS
d.comment(0xafbc, 'Return the key code as an integer', align=Align.INLINE)
d.comment(0xab6d, 'OSBYTE &86: read the text cursor position', align=Align.INLINE)
d.comment(0xab73, 'Return the column as an integer', align=Align.INLINE)

# fwa_clear (&A686): FWA = 0.0
d.comment(0xa686, 'Zero to write into every field', align=Align.INLINE)
d.comment(0xa688, 'Clear the sign', align=Align.INLINE)
d.comment(0xa68a, 'Clear the overflow byte', align=Align.INLINE)
d.comment(0xa68c, 'Exponent 0 is the special "value is zero"', align=Align.INLINE)
d.comment(0xa68e, 'Clear mantissa byte 1 (most significant)', align=Align.INLINE)
d.comment(0xa690, 'Clear mantissa byte 2', align=Align.INLINE)
d.comment(0xa692, 'Clear mantissa byte 3', align=Align.INLINE)
d.comment(0xa694, 'Clear mantissa byte 4 (least significant)', align=Align.INLINE)
d.comment(0xa696, 'Clear the rounding byte', align=Align.INLINE)
d.comment(0xa698, 'FWA now holds 0.0', align=Align.INLINE)

# fwa_set_one (&A699): FWA = 1.0
d.comment(0xa699, 'Start from 0.0', align=Align.INLINE)
d.comment(0xa69c, 'Mantissa MSB &80 is the implied leading 1', align=Align.INLINE)
d.comment(0xa69e, 'Set mantissa byte 1', align=Align.INLINE)
d.comment(0xa6a0, 'Y = &81', align=Align.INLINE)
d.comment(0xa6a1, 'Exponent &81 makes the value exactly 1.0', align=Align.INLINE)
d.comment(0xa6a3, 'Return non-zero (A = exponent) to flag a real', align=Align.INLINE)
d.comment(0xa6a4, 'FWA now holds 1.0', align=Align.INLINE)

# fwa_copy_from_fwb (&A4DC): FWA = FWB
d.comment(0xa4dc, "Copy FWB's sign...", align=Align.INLINE)
d.comment(0xa4de, '...into FWA', align=Align.INLINE)
d.comment(0xa4e0, 'Copy the overflow byte...', align=Align.INLINE)
d.comment(0xa4e2, '...into FWA', align=Align.INLINE)
d.comment(0xa4e4, 'Copy the exponent...', align=Align.INLINE)
d.comment(0xa4e6, '...into FWA', align=Align.INLINE)
d.comment(0xa4e8, 'Copy mantissa byte 1...', align=Align.INLINE)
d.comment(0xa4ea, '...into FWA', align=Align.INLINE)
d.comment(0xa4ec, 'Copy mantissa byte 2...', align=Align.INLINE)
d.comment(0xa4ee, '...into FWA', align=Align.INLINE)
d.comment(0xa4f0, 'Copy mantissa byte 3...', align=Align.INLINE)
d.comment(0xa4f2, '...into FWA', align=Align.INLINE)
d.comment(0xa4f4, 'Copy mantissa byte 4...', align=Align.INLINE)
d.comment(0xa4f6, '...into FWA', align=Align.INLINE)
d.comment(0xa4f8, 'Copy the rounding byte...', align=Align.INLINE)
d.comment(0xa4fa, '...into FWA', align=Align.INLINE)
d.comment(0xa4fc, 'FWA is now a copy of FWB', align=Align.INLINE)

# fwa_normalise (&A303): shift the mantissa left until bit 7 of m1 is set
d.comment(0xa303, 'Mantissa MSB...', align=Align.INLINE)
d.comment(0xa307, 'OR in the lower mantissa bytes (byte 2)', align=Align.INLINE)
d.comment(0xa309, '(byte 3)', align=Align.INLINE)
d.comment(0xa30b, '(byte 4) to test the whole mantissa', align=Align.INLINE)
d.comment(0xa30f, 'so jump away to handle the zero value', align=Align.INLINE)
d.comment(0xa311, 'Load the exponent to adjust as we shift', align=Align.INLINE)
d.comment(0xa315, 'Bit 7 set: already normalised, return', align=Align.INLINE)
d.comment(0xa317, 'MSB byte non-zero but bit 7 clear: bit-shift', align=Align.INLINE)
d.comment(0xa319, 'Shift the mantissa up a byte: load m2', align=Align.INLINE)
d.comment(0xa31b, 'store as m1', align=Align.INLINE)
d.comment(0xa31d, 'load m3', align=Align.INLINE)
d.comment(0xa31f, 'store as m2', align=Align.INLINE)
d.comment(0xa321, 'load m4', align=Align.INLINE)
d.comment(0xa323, 'store as m3', align=Align.INLINE)
d.comment(0xa325, 'load the rounding byte', align=Align.INLINE)
d.comment(0xa327, 'store as m4', align=Align.INLINE)
d.comment(0xa329, 'rounding <- 0', align=Align.INLINE)
d.comment(0xa32b, 'Prepare to reduce the exponent', align=Align.INLINE)
d.comment(0xa32e, 'Store the reduced exponent', align=Align.INLINE)
d.comment(0xa330, 'Loop to shift another byte if MSB still zero', align=Align.INLINE)
d.comment(0xa332, 'Borrow into the overflow byte', align=Align.INLINE)
d.comment(0xa334, 'Continue the byte-shift loop', align=Align.INLINE)
d.comment(0xa336, 'Bit-shift loop: re-check the MSB', align=Align.INLINE)
d.comment(0xa338, 'Bit 7 set: normalised, return', align=Align.INLINE)
d.comment(0xa33c, 'Shift the mantissa left one bit: byte 4', align=Align.INLINE)
d.comment(0xa33e, 'byte 3', align=Align.INLINE)
d.comment(0xa340, 'byte 2', align=Align.INLINE)
d.comment(0xa342, 'byte 1 (MSB)', align=Align.INLINE)
d.comment(0xa344, 'Reduce the exponent by one', align=Align.INLINE)
d.comment(0xa346, 'Store it', align=Align.INLINE)
d.comment(0xa348, 'Loop until the MSB bit is set', align=Align.INLINE)
d.comment(0xa34a, 'Borrow into the overflow byte', align=Align.INLINE)
d.comment(0xa34c, 'Continue the bit-shift loop', align=Align.INLINE)

# fwa_pack_var (&A38D): pack FWA into the 5-byte value at (zp_fp_ptr)
d.comment(0xa38d, 'Write packed bytes from offset 0', align=Align.INLINE)
d.comment(0xa38f, 'Packed byte 0 is the exponent', align=Align.INLINE)
d.comment(0xa391, '(store it)', align=Align.INLINE)
d.comment(0xa393, 'next byte', align=Align.INLINE)
d.comment(0xa394, 'Take the sign byte', align=Align.INLINE)
d.comment(0xa398, 'keep only the sign bit', align=Align.INLINE)
d.comment(0xa39a, 'Mantissa MSB', align=Align.INLINE)
d.comment(0xa3a0, 'Packed byte 1 = sign + mantissa MSB', align=Align.INLINE)
d.comment(0xa3a2, 'Mantissa byte 2', align=Align.INLINE)
d.comment(0xa3a4, 'next byte', align=Align.INLINE)
d.comment(0xa3a5, 'Packed byte 2', align=Align.INLINE)
d.comment(0xa3a7, 'Mantissa byte 3', align=Align.INLINE)
d.comment(0xa3a9, 'next byte', align=Align.INLINE)
d.comment(0xa3aa, 'Packed byte 3', align=Align.INLINE)
d.comment(0xa3ac, 'Mantissa byte 4', align=Align.INLINE)
d.comment(0xa3ae, 'next byte', align=Align.INLINE)
d.comment(0xa3af, 'Packed byte 4', align=Align.INLINE)
d.comment(0xa3b1, 'The 5-byte packed value is stored', align=Align.INLINE)

# fwa_unpack_var (&A3B5): unpack the 5-byte value at (zp_fp_ptr) into FWA
d.comment(0xa3b7, 'Packed byte 4...', align=Align.INLINE)
d.comment(0xa3b9, '...is mantissa byte 4', align=Align.INLINE)
d.comment(0xa3bb, 'next byte', align=Align.INLINE)
d.comment(0xa3bc, 'byte 3...', align=Align.INLINE)
d.comment(0xa3be, '...mantissa byte 3', align=Align.INLINE)
d.comment(0xa3c0, 'next byte', align=Align.INLINE)
d.comment(0xa3c1, 'byte 2...', align=Align.INLINE)
d.comment(0xa3c3, '...mantissa byte 2', align=Align.INLINE)
d.comment(0xa3c5, 'next byte', align=Align.INLINE)
d.comment(0xa3c6, 'byte 1 (sign + mantissa MSB)...', align=Align.INLINE)
d.comment(0xa3ca, 'next byte', align=Align.INLINE)
d.comment(0xa3cb, 'byte 0...', align=Align.INLINE)
d.comment(0xa3cd, '...is the exponent', align=Align.INLINE)
d.comment(0xa3d1, 'clear the overflow byte too', align=Align.INLINE)
d.comment(0xa3d5, '(mantissa byte 2)', align=Align.INLINE)
d.comment(0xa3d7, '(mantissa byte 3)', align=Align.INLINE)
d.comment(0xa3d9, '(mantissa byte 4)', align=Align.INLINE)
d.comment(0xa3dd, 'Non-zero: take the packed MSB (carrying the sign)',
          align=Align.INLINE)
d.comment(0xa3e1, 'Store the true mantissa MSB', align=Align.INLINE)
d.comment(0xa3e3, 'FWA now holds the unpacked value', align=Align.INLINE)

# fn_true (&ACC4): TRUE = -1 (also the ineg1 integer primitive)
d.comment(0xacc4, 'TRUE is -1: load &FF into every IWA byte', align=Align.INLINE)
d.comment(0xacc6, 'byte 0', align=Align.INLINE)
d.comment(0xacc8, 'byte 1', align=Align.INLINE)
d.comment(0xacca, 'byte 2', align=Align.INLINE)
d.comment(0xaccc, 'byte 3: IWA = -1', align=Align.INLINE)
d.comment(0xacce, 'Result type = integer', align=Align.INLINE)
d.comment(0xacd0, 'Return TRUE', align=Align.INLINE)

# fn_false (&AECA): FALSE = 0
d.comment(0xaeca, 'FALSE is 0', align=Align.INLINE)
d.comment(0xaecc, 'Return 0 as an integer', align=Align.INLINE)

# fn_pi (&ABCB): FWA = pi
d.comment(0xabcb, 'Load the constant pi/2 into FWA', align=Align.INLINE)
d.comment(0xabce, 'Double it (exponent + 1) to get pi', align=Align.INLINE)
d.comment(0xabd0, 'Flag a non-zero real result', align=Align.INLINE)
d.comment(0xabd1, 'FWA = pi', align=Align.INLINE)

# fn_count (&AEF7): COUNT
d.comment(0xaef7, 'COUNT: characters printed since the last newline',
          align=Align.INLINE)
d.comment(0xaef9, 'Return it as an integer', align=Align.INLINE)

# unstack_integer (&BDEA): pop a 4-byte integer into IWA (stack not dropped)
d.comment(0xbdea, 'Index the stacked integer (4 bytes, MSB first)',
          align=Align.INLINE)
d.comment(0xbdec, 'Top byte (MSB)...', align=Align.INLINE)
d.comment(0xbdee, '...into IWA byte 3', align=Align.INLINE)
d.comment(0xbdf0, 'next byte', align=Align.INLINE)
d.comment(0xbdf1, 'byte 2...', align=Align.INLINE)
d.comment(0xbdf3, '...into IWA', align=Align.INLINE)
d.comment(0xbdf5, 'next byte', align=Align.INLINE)
d.comment(0xbdf6, 'byte 1...', align=Align.INLINE)
d.comment(0xbdf8, '...into IWA', align=Align.INLINE)
d.comment(0xbdfa, 'last byte', align=Align.INLINE)
d.comment(0xbdfb, 'byte 0 (LSB)...', align=Align.INLINE)
d.comment(0xbdfd, '...into IWA (the caller drops the stack)', align=Align.INLINE)

# fwa_pack_temp1/2/3 (&A385/&A37D/&A381): point at an FP temp, then pack
d.comment(0xa385, 'Point at FP TEMP1 (&046C): low byte', align=Align.INLINE)
d.comment(0xa387, 'set the fp-variable pointer', align=Align.INLINE)
d.comment(0xa389, 'high byte &04', align=Align.INLINE)
d.comment(0xa38b, 'then fall into fwa_pack_var', align=Align.INLINE)
d.comment(0xa3b2, 'Point at FP TEMP1, then unpack it into FWA',
          align=Align.INLINE)

# iwa_from_ya (&AEEA): IWA = unsigned 256*Y + A
d.comment(0xaeea, 'Low byte (A) into IWA byte 0', align=Align.INLINE)
d.comment(0xaeec, 'High byte (Y) into IWA byte 1', align=Align.INLINE)
d.comment(0xaef0, 'Clear IWA byte 2', align=Align.INLINE)
d.comment(0xaef2, 'Clear byte 3: the value is unsigned 0-65535', align=Align.INLINE)
d.comment(0xaef6, 'Return the integer', align=Align.INLINE)

# fwa_round_carry (&A2A4): add A to rounding, ripple carry up the mantissa
d.comment(0xa2a4, 'Add the round increment to the rounding byte',
          align=Align.INLINE)
d.comment(0xa2a6, 'Store it back', align=Align.INLINE)
d.comment(0xa2a8, 'No carry out: done', align=Align.INLINE)
d.comment(0xa2aa, 'Carry: bump mantissa byte 4', align=Align.INLINE)
d.comment(0xa2ac, 'No further carry: done', align=Align.INLINE)
d.comment(0xa2ae, 'Ripple into byte 3', align=Align.INLINE)
d.comment(0xa2b0, 'done if no carry', align=Align.INLINE)
d.comment(0xa2b2, 'into byte 2', align=Align.INLINE)
d.comment(0xa2b4, 'done if no carry', align=Align.INLINE)
d.comment(0xa2b6, 'into byte 1 (the MSB)', align=Align.INLINE)
d.comment(0xa2b8, 'done if no carry', align=Align.INLINE)
d.comment(0xa2ba, 'Carry out of the mantissa: renormalise (exponent up)',
          align=Align.INLINE)

# fwb_copy_from_fwa (&A21E): FWB = FWA
d.comment(0xa21e, "Copy FWA's sign...", align=Align.INLINE)
d.comment(0xa220, '...into FWB', align=Align.INLINE)
d.comment(0xa222, 'Copy the overflow byte...', align=Align.INLINE)
d.comment(0xa224, '...into FWB', align=Align.INLINE)
d.comment(0xa226, 'Copy the exponent...', align=Align.INLINE)
d.comment(0xa228, '...into FWB', align=Align.INLINE)
d.comment(0xa22a, 'Copy mantissa byte 1...', align=Align.INLINE)
d.comment(0xa22c, '...into FWB', align=Align.INLINE)
d.comment(0xa22e, 'Copy mantissa byte 2...', align=Align.INLINE)
d.comment(0xa230, '...into FWB', align=Align.INLINE)
d.comment(0xa232, 'Copy mantissa byte 3...', align=Align.INLINE)
d.comment(0xa234, '...into FWB', align=Align.INLINE)
d.comment(0xa236, 'Copy mantissa byte 4...', align=Align.INLINE)
d.comment(0xa238, '...into FWB', align=Align.INLINE)
d.comment(0xa23a, 'Copy the rounding byte...', align=Align.INLINE)
d.comment(0xa23c, '...into FWB', align=Align.INLINE)
d.comment(0xa23e, 'FWB is now a copy of FWA', align=Align.INLINE)

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
