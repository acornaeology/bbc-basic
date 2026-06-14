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
from dasmos.hooks import stringhi_hook

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
# Language-specific data types: registers the packed 5-byte
# floating-point type "bbc_float5" used for the REAL constant pool.
d.use_environment('bbc_basic_6502')

# Code entry points. The language entry (&8000) and language_startup
# (&8023, the BEQ target) are reached by the trace from the env-seeded
# language entry, so they need no explicit entry() here.
d.entry(0xb402)  # BASIC error handler, installed into BRKV at startup

# ----------------------------------------------------------------------
# Floating-point constant pool. BASIC's REAL constants are packed
# 5-byte floats (excess-128 exponent, sign in the mantissa MSB). Type
# each one with the bbc_float5 data type: the raw bytes are emitted for
# byte-faithful reassembly, with the decoded value surfaced as an
# annotation. override=True reclaims bytes the tracer/auto-detector
# classified as code or string. The continued-fraction coefficient
# tables are a count byte then that many 5-byte coefficients, with one
# trailing constant before the next routine.
# ----------------------------------------------------------------------
def _fp_coeff_table(count_addr, count, name, trailing_comment):
    """Type a continued-fraction table: count byte, count x bbc_float5,
    then one trailing constant before the next routine."""
    d.byte(count_addr, 1, override=True)            # coefficient count
    for _i in range(count):
        d.typed_data(count_addr + 1 + 5 * _i, 'bbc_float5',
                     comment=f'{name} c{_i}', override=True)
    d.typed_data(count_addr + 1 + 5 * count, 'bbc_float5',
                 comment=trailing_comment, override=True)


# LN: log10(e) and ln 2 scalars, then the LN continued-fraction table.
d.typed_data(0xa869, 'bbc_float5', comment='log10(e) = 1/ln(10)', override=True)
d.typed_data(0xa86e, 'bbc_float5', comment='ln 2', override=True)
_fp_coeff_table(0xa873, 6, 'ln', '-0.5')
# ATN continued-fraction table.
_fp_coeff_table(0xa95a, 9, 'atn', None)   # trailing constant 0.92730
# The two-part pi/2, pi/2, and the RAD/DEG conversion factors, then SIN.
d.typed_data(0xaa59, 'bbc_float5', comment='pi/2, high part (Cody-Waite)',
             override=True)
d.typed_data(0xaa5e, 'bbc_float5', comment='pi/2, low part (Cody-Waite)',
             override=True)
d.typed_data(0xaa63, 'bbc_float5', comment='pi/2', override=True)
d.typed_data(0xaa68, 'bbc_float5', comment='pi/180 (degrees -> radians, RAD)',
             override=True)
d.typed_data(0xaa6d, 'bbc_float5', comment='180/pi (radians -> degrees, DEG)',
             override=True)
_fp_coeff_table(0xaa72, 5, 'sin', '1.0')
# e, then the EXP continued-fraction table.
d.typed_data(0xaae4, 'bbc_float5', comment='e', override=True)
_fp_coeff_table(0xaae9, 7, 'exp', '1.0')

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
d.label(0x0001, 'zp_lomem_1')
d.label(0x0002, 'zp_vartop')          # End of BASIC variables (heap top)
d.label(0x0003, 'zp_vartop_1')
d.label(0x0004, 'zp_stack_ptr')       # Top of the BASIC value stack
d.label(0x0005, 'zp_stack_ptr_1')
d.label(0x0006, 'zp_himem')           # Start of screen / top of BASIC
d.label(0x0007, 'zp_himem_1')
d.label(0x0008, 'zp_erl')             # Line number that last errored
d.label(0x0009, 'zp_erl_1')
d.label(0x000a, 'zp_text_ptr_off')    # Offset into current text line
d.label(0x000b, 'zp_text_ptr')        # Start of current text line
d.label(0x000c, 'zp_text_ptr_1')
# RND work area (&0D-&11): a 33-bit LFSR state. &0D-&10 are a 32-bit
# little-endian value (bits 0-31); bit 0 of &11 is bit 32. See rnd_step.
d.label(0x000d, 'zp_rnd_seed')        # LFSR bits 0-7
d.label(0x000e, 'zp_rnd_seed_1')      # LFSR bits 8-15
d.label(0x000f, 'zp_rnd_seed_2')      # LFSR bits 16-23
d.label(0x0010, 'zp_rnd_seed_3')      # LFSR bits 24-31
d.label(0x0011, 'zp_rnd_seed_4')      # LFSR bit 32 (in bit 0; overflow)
d.label(0x0012, 'zp_top')             # End of program (excl. variables)
d.label(0x0013, 'zp_top_1')
d.label(0x0014, 'zp_print_bytes')     # Bytes in current print field
d.label(0x0015, 'zp_print_flag')      # 0 = decimal, -ve = hexadecimal
d.label(0x0016, 'zp_error_vec')       # Address of BASIC error routine
d.label(0x0017, 'zp_error_vec_1')
d.label(0x0018, 'zp_page')            # PAGE DIV 256 (program start page)
d.label(0x0019, 'zp_text_ptr2')       # Secondary text pointer
d.label(0x001a, 'zp_text_ptr2_1')
d.label(0x001b, 'zp_text_ptr2_off')   # Secondary text-pointer offset
d.label(0x001c, 'zp_data_ptr')        # Pointer to next DATA item
d.label(0x001d, 'zp_data_ptr_1')
d.label(0x001e, 'zp_count')           # Bytes printed since last newline
d.label(0x001f, 'zp_listo')           # LISTO flag
d.label(0x0020, 'zp_trace_flag')      # &00 = trace off, &FF = trace on
d.label(0x0021, 'zp_trace_max')       # Maximum TRACE line number
d.label(0x0023, 'zp_width')           # WIDTH setting
d.label(0x0024, 'zp_repeat_level')    # REPEAT stack depth; not saved by PROC
d.label(0x0025, 'zp_gosub_level')     # GOSUB stack depth; not saved by PROC
d.label(0x0026, 'zp_for_level')       # FOR stack depth (x15); not saved by PROC
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
d.label(0x0038, 'zp_general_1')       # general pointer high byte
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
d.label(0x0048, 'zp_dp_flag')         # decimal-point-seen flag (conversion)
d.label(0x0049, 'zp_dec_exp')         # decimal exponent (conversion)
d.label(0x004b, 'zp_fp_ptr')          # Pointer to a packed fp variable
d.label(0x004c, 'zp_fp_ptr_1')        # (high byte; used by the FP routines)
d.label(0x00fd, 'zp_error_ptr')       # Pointer to the current error block

# ----------------------------------------------------------------------
# Page 4 / 5 / 6 / 7 RAM workspace (Pharo ch. 7.3-7.6).
# ----------------------------------------------------------------------
d.label(0x0400, 'resint_at')          # @% print-format resident integer
for _i, _name in enumerate('abcdefghijklmnopqrstuvwxyz'):
    d.label(0x0404 + 4 * _i, f'resint_{_name}')  # A%..Z%
for _i in range(1, 5):
    d.label(0x046c + 5 * (_i - 1), f'fp_temp{_i}')  # FP TEMP1..TEMP4
d.label(0x0480, 'var_ptr_table')      # Variable lookup table (by initial)
# Control-flow stacks (page 5). Three independent LIFO arrays, one per
# loop construct, each indexed by its own zero-page level counter:
#   for_stack    &0500  15-byte frames, counter zp_for_level    (&26)
#   repeat_stack &05A4   2-byte frames, counter zp_repeat_level (&24)
#   gosub_stack  &05CC   2-byte frames, counter zp_gosub_level  (&25)
# These are distinct from the 6502 hardware stack and the BASIC value
# stack, and -- unlike those two -- are NOT saved/restored across a
# PROC/FN call. See call_proc_fn (&B197).
d.label(0x0500, 'for_stack')          # FOR stack (&0500-&0595, 10 frames)
d.label(0x05a4, 'repeat_stack')       # REPEAT loop-start ptrs (low bytes)
d.label(0x05b8, 'repeat_stack_hi')    # REPEAT loop-start ptrs (high bytes)
d.label(0x05cc, 'gosub_stack')        # GOSUB return ptrs (low bytes)
d.label(0x05e6, 'gosub_stack_hi')     # GOSUB return ptrs (high bytes)
d.label(0x0600, 'string_work')        # String work area / CALL block
d.label(0x0700, 'line_input_buf')     # Line input buffer

# ----------------------------------------------------------------------
# Keyword / token table (Pharo ch. 7.7). Each entry is the keyword text
# in ASCII, a token byte (bit 7 set), and a tokeniser flag byte.
# ----------------------------------------------------------------------
d.subroutine(
    0x8071, 'keyword_table',
    is_entry_point=False,   # data table: banner only, do not trace as code
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
                                'values, the caller\'s text pointer and the '
                                'saved 6502/value stacks. It does NOT tidy the '
                                'FOR/REPEAT/GOSUB stacks, so ENDPROC from '
                                'inside a loop leaks that loop\'s frame. '
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
d.subroutine(0xa4d0, 'fwa_sub_var', title='FWA = FWA - fp var',
             description='Subtract the fp variable operand from FWA '
                         '(reverse subtract, then negate).')
d.subroutine(0xa486, 'fp_split_int_frac',
             title='Split FWA into integer part (&4A) and fraction (FWA)',
             description='Round FWA to the nearest integer, leaving that '
                         'integer in &4A and the signed remainder (in '
                         '[-0.5, 0.5]) in FWA. Used by EXP to separate the '
                         'integer and fractional powers.')
d.subroutine(0xab12, 'fwa_int_power', title='FWA = FWA ^ n (n in A)',
             description='Raise FWA to an integer power by repeated '
                         'multiplication; a negative exponent reciprocates '
                         'first. Used by EXP to form e^(integer part).')
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

# Transcendental helpers (shared by ATN/ASN/ACS/SIN/COS).
d.subroutine(0xa897, 'fp_eval_cont_frac',
             title='Evaluate a continued-fraction approximation',
             description='X,Y point at a coefficient table: a count byte '
                         'followed by that many five-byte fp coefficients. '
                         'The argument is held in TEMP1; the routine folds '
                         'the table from the top, alternating FWA = arg / FWA '
                         'and FWA = FWA + next coefficient, to evaluate the '
                         'continued fraction used by the trig kernels.')
d.subroutine(0xa927, 'fwa_complement_half_pi', title='FWA = pi/2 - FWA',
             description='Subtract FWA from pi/2 using the two-part constant '
                         'at &AA59/&AA5E for extra precision, then negate. '
                         'Used for ACS (pi/2 - ASN) and the large-argument '
                         'arctan identity atn(x) = pi/2 - atn(1/x).')
d.subroutine(0xaa48, 'point_half_pi_hi',
             title='Point the fp pointer at the high part of pi/2 (&AA59)')
d.subroutine(0xaa4c, 'point_half_pi_lo',
             title='Point the fp pointer at the low part of pi/2 (&AA5E)')
d.subroutine(0xaa55, 'point_const_half_pi',
             title='Point the fp pointer at the pi/2 constant (&AA63)')
d.subroutine(0xa9d3, 'sin_cos_reduce',
             title='Range-reduce the SIN/COS argument',
             description='Divide the argument by pi/2 to find the quadrant '
                         '(stored in &4A) and Cody-Waite reduce to the '
                         'principal range using the two-part pi/2 constant, '
                         'leaving the reduced angle in FWA for the series.')

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
d.comment(0x9228, 'no carry: done', align=Align.INLINE)
d.comment(0x922a, 'byte 2', align=Align.INLINE)
d.comment(0x922c, 'no carry: done', align=Align.INLINE)
d.comment(0x922e, 'byte 3', align=Align.INLINE)
d.comment(0x9230, 'Return', align=Align.INLINE)

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
d.comment(0x9b43, 'stacked byte', align=Align.INLINE)
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
d.comment(0xb7cb, 'Stack the variable pointer', align=Align.INLINE)
d.comment(0xb7d4, 'Index the FOR stack by nesting level', align=Align.INLINE)
d.comment(0xb7d6, 'At most 10 nested FOR loops (10 * 15)', align=Align.INLINE)
d.comment(0xb7da, 'Store the variable pointer in the frame (+0)',
          align=Align.INLINE)
d.comment(0xb7ed, 'Require the TO keyword', align=Align.INLINE)
d.comment(0xb7fa, 'Store the limit in the frame (+8)', align=Align.INLINE)
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
d.comment(0x8c2f, 'Tentative new address = heap top', align=Align.INLINE)

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
d.comment(0x8dc1, 'Set the hex/dec flag (~ selects hex)', align=Align.INLINE)
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

Note what is NOT saved: only the 6502 hardware stack and the BASIC
value stack are preserved across the call. The FOR, REPEAT and GOSUB
stacks (page 5, counters &24/&25/&26) are global and untouched. So a
loop opened inside the body and left via an early ENDPROC (or GOTO)
leaks its frame -- the counter is never decremented. See stmt_endproc
(&9356) and the page-5 control-flow stacks at &0500.
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

d.subroutine(0xbe62, 'load_program', title='Load a program from the filing system',
             description='Used by LOAD and CHAIN to read a BASIC program into memory.')
d.subroutine(0xbe6f, 'check_program', title='Validate the program and set TOP',
             description='Walk the lines from PAGE checking each is well-formed (CR-terminated, non-zero length), set TOP past the end; "Bad program" otherwise.')

# load_program (&BE62)
d.comment(0xbe62, 'Set the OSFILE load address to PAGE', align=Align.INLINE)
d.comment(0xbe65, '...', align=Align.INLINE)
d.comment(0xbe66, 'OSFILE &FF: load the named file', align=Align.INLINE)
d.comment(0xbe68, 'exec address = 0 (load to the given address)', align=Align.INLINE)
d.comment(0xbe6a, 'control block at &37', align=Align.INLINE)
d.comment(0xbe6f, 'Set TOP = PAGE: high', align=Align.INLINE)
d.comment(0xbe71, '(TOP high)', align=Align.INLINE)
d.comment(0xbe73, 'low 0', align=Align.INLINE)
d.comment(0xbe75, '(store)', align=Align.INLINE)
d.comment(0xbe77, 'Y = 1', align=Align.INLINE)
d.comment(0xbe78, 'step back to the byte before the line', align=Align.INLINE)
d.comment(0xbe79, 'get it', align=Align.INLINE)
d.comment(0xbe7b, 'each line must be CR-terminated', align=Align.INLINE)
d.comment(0xbe7d, 'not a CR: Bad program', align=Align.INLINE)
d.comment(0xbe7f, 'step to the line number / end marker', align=Align.INLINE)
d.comment(0xbe80, 'get it', align=Align.INLINE)
d.comment(0xbe82, 'high bit set: end of program', align=Align.INLINE)
d.comment(0xbe84, 'line length is at offset 3', align=Align.INLINE)
d.comment(0xbe86, 'get it', align=Align.INLINE)
d.comment(0xbe88, 'zero length: Bad program', align=Align.INLINE)
d.comment(0xbe8a, 'advance to the next line', align=Align.INLINE)
d.comment(0xbe8b, 'TOP += line length', align=Align.INLINE)
d.comment(0xbe8e, 'loop over all lines', align=Align.INLINE)
d.comment(0xbe90, 'End of program: skip the &FF marker', align=Align.INLINE)
d.comment(0xbe91, '...', align=Align.INLINE)
d.comment(0xbe92, 'TOP += Y', align=Align.INLINE)
d.comment(0xbe93, 'add: low', align=Align.INLINE)
d.comment(0xbe95, '(store)', align=Align.INLINE)
d.comment(0xbe97, 'no carry', align=Align.INLINE)
d.comment(0xbe99, 'carry into high', align=Align.INLINE)
d.comment(0xbe9b, 'return Y=1 (NE)', align=Align.INLINE)
d.comment(0xbe9d, 'Return', align=Align.INLINE)
d.comment(0xbe9e, 'Bad program: print the message', align=Align.INLINE)
d.comment(0xbeae, '(string terminator)', align=Align.INLINE)
d.comment(0xbeaf, 'back to the immediate loop', align=Align.INLINE)
d.comment(0xbeb2, 'Point the general pointer at the string buffer: low', align=Align.INLINE)
d.comment(0xbeb4, '(store)', align=Align.INLINE)
d.comment(0xbeb6, 'high (&06)', align=Align.INLINE)
d.comment(0xbeb8, '(store)', align=Align.INLINE)
d.comment(0xbeba, 'Terminate the string buffer with a CR:', align=Align.INLINE)
d.comment(0xbebc, 'CR', align=Align.INLINE)
d.comment(0xbebe, 'at the end of the buffer', align=Align.INLINE)
d.comment(0xbec1, 'Return', align=Align.INLINE)

d.subroutine(0xbd20, 'clear_vars_heap_stack',
             title='Clear all variables, the heap and the stack',
             description='Reset variable storage, the heap and the BASIC stack (NEW/CLEAR).')
d.subroutine(0xbc02, 'read_input_line', title='Print the prompt and read a line',
             description='Print the character in A as a prompt, then read a line into the input buffer.')
d.subroutine(0x95c9, 'parse_var_ref',
             title='Parse a variable reference / lvalue',
             description='Scan a variable name or indirection operator at the '
                         'text pointer. On success returns A=&FF, CLC, with '
                         'the value address in &2A/&2B and a type byte in '
                         '&2C (4=integer, 5=real, &80=$ indirection, '
                         '&81=byte/word indirection or array element). '
                         'Returns A=0, SEC when the name is undefined.')
d.subroutine(0x92fa, 'eval_real', title='Evaluate an expression as a real',
             description='Evaluate a factor and ensure the result is real, '
                         'converting an integer with int_to_fwa.')
d.subroutine(0x92fd, 'ensure_real', title='Coerce the result to a real',
             description='Type mismatch for a string, leave a real, or '
                         'convert an integer to FWA.')
d.subroutine(0x97df, 'check_line_number',
             title='Test for an embedded line number',
             description='If the text pointer is at a line-number token, '
                         'decode it into IWA and return carry set; otherwise '
                         'carry clear.')
d.subroutine(0x97eb, 'decode_line_number',
             title='Decode a 3-byte line number into IWA',
             description='Reverse the GOTO three-byte encoding, reconstructing '
                         'the 16-bit line number in IWA.')
d.subroutine(0x9841, 'expect_eq', title='Require "=" at the parser pointer',
             description='Skip spaces and raise Mistake unless the next '
                         'character is "=".')
d.subroutine(0x88f5, 'encode_line_number',
             title='Encode a 16-bit line number into 3 bytes',
             description='Pack the line number in &3D/&3E into the BBC '
                         'three-byte GOTO encoding (a control byte holding '
                         'the scrambled top bits, then low|&40 and high|&40) '
                         'so the bytes never collide with tokens.')
d.subroutine(0x8926, 'is_alphanumeric',
             title='Test A for a name character',
             description='Return carry set if A is 0-9, A-Z, a-z or _, the '
                         'characters allowed in a variable or FN/PROC name.')
d.subroutine(0x85ba, 'asm_parse_mnemonic',
             title='Parse and compact an assembler mnemonic',
             description='Skip to the mnemonic, handling end-of-statement and '
                         'labels, then pack its three letters (5 bits each) '
                         'into &3D/&3E for the opcode-table lookup.')
d.subroutine(0x9a9e, 'eval_and_compare',
             title='Evaluate the next operand and compare',
             description='Stack the current value, evaluate the next '
                         'arithmetic operand and compare the two (integer, '
                         'real or string), returning the ordering flags for '
                         'the relational operators.')
d.subroutine(0x9a5f, 'fp_compare',
             title='Compare FWA with a fp variable',
             description='Unpack the operand into FWB and compare it with FWA '
                         'by sign, exponent and mantissa bytes, returning the '
                         'ordering for the relational operators.')
d.subroutine(0x8897, 'parse_decimal_u16',
             title='Parse a 16-bit decimal number',
             description='Accumulate decimal digits from (&37) into &3D/&3E '
                         'as value*10 + digit, with overflow detection. The '
                         'first digit is in A on entry; stops at the first '
                         'non-digit. Used to read line numbers.')
d.subroutine(0xaed8, 'int_result_a',
             title='Return A as an integer result',
             description='Set the result to the unsigned byte in A (high '
                         'bytes zero) and mark it integer. The common tail '
                         'for functions returning a small integer.')
d.subroutine(0xb50e, 'print_token',
             title='De-tokenise and print a character or token',
             description='Print A directly if below &80, otherwise look the '
                         'token up in the keyword table at &8071 and print '
                         'its expanded text.')
d.subroutine(0xb545, 'print_hex_byte', title='Print A as two hex digits')
d.subroutine(0xb550, 'print_hex_digit',
             title='Print the low nibble of A as a hex digit')
d.subroutine(0xb577, 'print_listo_indent',
             title='Print LISTO indentation',
             description='If the LISTO flag bit in A is set, print 2*X spaces '
                         'of indentation for the listing.')
d.subroutine(0xb58a, 'stmt_listo', title='LISTO - set the listing options',
             description='Evaluate the option value and store it in the LISTO '
                         'flag (&1F).')
d.subroutine(0xb558, 'print_char',
             title='Print a character with column tracking',
             description='Output A through the print formatter, handling CR '
                         'specially and maintaining the print column COUNT.')
d.subroutine(0xb565, 'print_space',
             title='Print a space through the print formatter')
d.subroutine(0x9e20, 'eval_power',
             title='Expression Level 2 - the ^ operator',
             description='Evaluate a factor, then for each ^ raise it to the '
                         'power: an integer exponent uses repeated '
                         'multiplication, otherwise x^y = x^int * exp(frac * '
                         'ln x).')
d.subroutine(0xbc2d, 'delete_program_line',
             title='Delete a program line and close the gap',
             description='Find the line, then shift every later line down '
                         'over it (source &37, destination &12) and update '
                         'the top of program. No-ops if the line is absent.')
d.subroutine(0xbb50, 'next_data_item',
             title='Advance the DATA pointer to the next item',
             description='Move the DATA pointer past the current item to the '
                         'next comma- or DATA-separated value, searching '
                         'forward through the program for the next DATA '
                         'statement at end of line; raises Out of DATA.')
d.subroutine(0x8cc1, 'unstack_value_to_var',
             title='Restore a stacked value into a variable',
             description='Pop the value at the BASIC stack (&04) into the '
                         'variable at &37, dispatched by the type/size byte '
                         '&39: a numeric value of that many bytes, a $addr '
                         'string (CR terminated), or a string variable '
                         '(copied into its heap allocation). Used by the '
                         'FN/PROC LOCAL and parameter machinery.')
d.subroutine(0x99be, 'iwa_divide',
             title='Unsigned/signed 32-bit integer division',
             description='Evaluate the right operand, take absolute values, '
                         'and do a 32-step shift-subtract division. The '
                         'dividend/quotient builds in &39-&3C and the '
                         'remainder in &3D-&40; the divisor is IWA. The '
                         'quotient sign is the XOR of the operand signs in '
                         '&37, the remainder sign the dividend sign in &38. '
                         'Raises Division by zero. Shared by DIV and MOD.')
d.subroutine(0x9905, 'trace_line',
             title='Print [line] when TRACE is active',
             description='If the current line number is within the TRACE '
                         'ceiling, print the line number in brackets.')
d.subroutine(0x991f, 'print_line_number',
             title='Print a 16-bit line number in decimal',
             description='Convert the value in IWA to decimal by repeated '
                         'subtraction of the powers of ten at &996B/&99B9, '
                         'suppressing leading zeros, optionally right-'
                         'justified in a field.')
d.subroutine(0x8832, 'asm_opcode_add4',
             title='Step the opcode to the next addressing-mode column (+4)',
             description='Add 4 to the base opcode in &29 to select the next '
                         '6502 addressing-mode encoding.')
d.subroutine(0x882f, 'asm_opcode_add8',
             title='Advance the opcode by two addressing-mode columns (+8)')
d.subroutine(0x882c, 'asm_opcode_add16',
             title='Advance the opcode by four addressing-mode columns (+16)')
d.subroutine(0x97ba, 'check_subscript_bound',
             title='Check a subscript against a dimension extent',
             description='Raise Subscript if the subscript in IWA is negative '
                         'or not less than the dimension size stored at '
                         '(&37),Y; advances Y past the two-byte extent.')
d.subroutine(0x96df, 'index_array',
             title='Locate an array and evaluate one subscript',
             description='Find the named array and step the value pointer to '
                         'the addressed element; raises Array on a missing '
                         'array.')
d.subroutine(0x94fc, 'create_variable', title='Create a new variable',
             description='Allocate a new entry for a variable that does not yet exist.')

# skip_spaces (&8A97) / skip_spaces_ptr2 (&8A8C)
d.comment(0x8a97, 'Get the text offset', align=Align.INLINE)
d.comment(0x8a99, 'advance it for next time', align=Align.INLINE)
d.comment(0x8a9b, 'Read the character', align=Align.INLINE)
d.comment(0x8a9f, 'Space: keep skipping', align=Align.INLINE)
d.comment(0x8aa1, 'Return the first non-space character', align=Align.INLINE)
d.comment(0x8aa2, 'BRK error block ("Missing ,") follows', align=Align.INLINE)
d.comment(0x8a8c, 'Get the secondary text offset', align=Align.INLINE)
d.comment(0x8a8e, 'advance it', align=Align.INLINE)
d.comment(0x8a90, 'Read the character', align=Align.INLINE)
d.comment(0x8a94, 'Space: keep skipping', align=Align.INLINE)
d.comment(0x8a96, 'Return the first non-space character', align=Align.INLINE)

# start_new_program (&8ADD): set up an empty program
d.comment(0x8add, 'Empty program is a single CR...', align=Align.INLINE)
d.comment(0x8adf, 'TOP starts at PAGE: high byte', align=Align.INLINE)
d.comment(0x8ae1, '(TOP high)', align=Align.INLINE)
d.comment(0x8ae3, 'low byte 0', align=Align.INLINE)
d.comment(0x8ae5, 'TOP low = PAGE', align=Align.INLINE)
d.comment(0x8ae7, 'TRACE off', align=Align.INLINE)
d.comment(0x8ae9, '...stored as the end marker at PAGE', align=Align.INLINE)
d.comment(0x8aeb, '&FF...', align=Align.INLINE)
d.comment(0x8aed, 'next byte', align=Align.INLINE)
d.comment(0x8aee, '...marks the program end at PAGE+1', align=Align.INLINE)
d.comment(0x8af0, 'TOP = PAGE + 2', align=Align.INLINE)
d.comment(0x8af1, '(store)', align=Align.INLINE)
d.comment(0x8af3, 'Clear variables, heap and stack', align=Align.INLINE)

# immediate_loop (&8AF6)
d.comment(0x8af6, 'PtrA = &0700, the input buffer: high byte', align=Align.INLINE)
d.comment(0x8af8, '(store)', align=Align.INLINE)
d.comment(0x8afa, 'low byte 0', align=Align.INLINE)
d.comment(0x8afc, '(store)', align=Align.INLINE)
d.comment(0x8afe, 'ON ERROR OFF: default handler at &B433', align=Align.INLINE)
d.comment(0x8b00, '(low)', align=Align.INLINE)
d.comment(0x8b02, '(high)', align=Align.INLINE)
d.comment(0x8b04, '(store)', align=Align.INLINE)
d.comment(0x8b06, 'The ">" prompt', align=Align.INLINE)
d.comment(0x8b08, 'Print it and read a line into the buffer', align=Align.INLINE)

# check_eq_star_bracket (&8B60)
d.comment(0x8b60, 'Step back to the introducing character', align=Align.INLINE)
d.comment(0x8b62, '...', align=Align.INLINE)
d.comment(0x8b63, 'fetch it', align=Align.INLINE)
d.comment(0x8b67, '"=": return a value from a function', align=Align.INLINE)
d.comment(0x8b6b, '"*": an embedded OSCLI command', align=Align.INLINE)
d.comment(0x8b6f, '"[": enter the assembler', align=Align.INLINE)
d.comment(0x8b71, 'otherwise check for end of statement', align=Align.INLINE)
d.comment(0x8b73, 'Point PtrA at the command text', align=Align.INLINE)
d.comment(0x8b76, 'XY -> the command string', align=Align.INLINE)
d.comment(0x8b78, '(high byte)', align=Align.INLINE)
d.comment(0x8b7a, 'Pass it to OSCLI', align=Align.INLINE)

# try_variable_assignment (&8BBF)
d.comment(0x8bbf, 'Copy PtrA to PtrB: low', align=Align.INLINE)
d.comment(0x8bc1, '(store)', align=Align.INLINE)
d.comment(0x8bc3, 'high', align=Align.INLINE)
d.comment(0x8bc5, '(store)', align=Align.INLINE)
d.comment(0x8bc7, 'offset', align=Align.INLINE)
d.comment(0x8bc9, 'Parse a variable / indirection reference', align=Align.INLINE)
d.comment(0x8bcc, 'Existing variable: do the assignment', align=Align.INLINE)
d.comment(0x8bce, 'Not a variable: try =, * or [', align=Align.INLINE)
d.comment(0x8bd0, 'New variable: position for "="', align=Align.INLINE)
d.comment(0x8bd2, 'Require "="', align=Align.INLINE)
d.comment(0x8bd5, 'Create the new variable', align=Align.INLINE)
d.comment(0x8bd8, 'Type 5 = floating point', align=Align.INLINE)
d.comment(0x8bda, 'Is the destination a float?', align=Align.INLINE)
d.comment(0x8bdc, 'no', align=Align.INLINE)
d.comment(0x8bde, 'X = 6', align=Align.INLINE)
d.comment(0x8bdf, 'Evaluate and store the value', align=Align.INLINE)
d.comment(0x8be2, 'Step back, continue', align=Align.INLINE)

# dispatch_token (&8BB1) remaining
d.comment(0x8bb1, 'Token to X for indexing', align=Align.INLINE)
d.comment(0x8bb5, 'Store the handler low byte', align=Align.INLINE)
d.comment(0x8bba, 'Store the handler high byte', align=Align.INLINE)

# eval_expr (&9B1D) remaining: copy PtrA to PtrB
d.comment(0x9b1f, 'PtrB low = PtrA', align=Align.INLINE)
d.comment(0x9b21, 'PtrA high...', align=Align.INLINE)
d.comment(0x9b23, '...to PtrB high', align=Align.INLINE)
d.comment(0x9b25, 'PtrA offset...', align=Align.INLINE)
d.comment(0x9b27, '...to PtrB offset', align=Align.INLINE)
d.subroutine(0xbfb5, 'eval_channel', title='Evaluate a #channel argument',
             description='Evaluate the #handle of a file operation, leaving it in IWA.')
d.subroutine(0xafad, 'read_key_timed', title='Read a key within a time limit (INKEY)',
             description='Wait up to the given time for a key; the INKEY/INKEY$ primitive.')

# fn_gets (&AFBF): GET$ - a key as a one-character string
d.comment(0xafbf, 'Wait for a key', align=Align.INLINE)
d.comment(0xafc2, 'Store it as the one-character string body', align=Align.INLINE)
d.comment(0xafc5, 'Length 1', align=Align.INLINE)
d.comment(0xafc7, '(store)', align=Align.INLINE)
d.comment(0xafc9, 'String type', align=Align.INLINE)
d.comment(0xafcb, 'Return the one-character string', align=Align.INLINE)

# fn_inkeys (&B026): INKEY$ - a timed key as a string
d.comment(0xb026, 'Read a key within the time limit', align=Align.INLINE)
d.comment(0xb029, 'X holds the key', align=Align.INLINE)
d.comment(0xb02a, 'Y=0 means a key was read', align=Align.INLINE)
d.comment(0xb02c, 'Got one: return it as a 1-char string', align=Align.INLINE)
d.comment(0xb02e, 'Timeout: empty string', align=Align.INLINE)
d.comment(0xb030, 'length 0', align=Align.INLINE)
d.comment(0xb032, 'Return the (possibly empty) string', align=Align.INLINE)
d.comment(0xb033, 'Type mismatch (shared)', align=Align.INLINE)
d.comment(0xb036, 'Missing , error (shared)', align=Align.INLINE)

# fn_fn (&B195): FN calls a user function via call_proc_fn
d.comment(0xb195, 'FN token: enter via the PROC/FN call mechanism', align=Align.INLINE)

# fn_time (&AEB4): =TIME reads the centisecond clock
d.comment(0xaeb4, 'Point OSWORD at IWA: low byte', align=Align.INLINE)
d.comment(0xaeb6, 'high byte', align=Align.INLINE)
d.comment(0xaeb8, 'OSWORD &01: read the centisecond clock into IWA', align=Align.INLINE)
d.comment(0xaebd, 'Integer result', align=Align.INLINE)
d.comment(0xaebf, 'Return TIME', align=Align.INLINE)

# fn_ext (&BF46) / fn_ptr (&BF47): =EXT / =PTR via OSARGS
d.comment(0xbf46, 'Carry set selects EXT (otherwise PTR)', align=Align.INLINE)
d.comment(0xbf47, 'Build the OSARGS sub-function from the carry...', align=Align.INLINE)
d.comment(0xbf49, '...0 = PTR, non-zero = EXT', align=Align.INLINE)
d.comment(0xbf4a, '(BBC: A becomes 0 or 2)', align=Align.INLINE)
d.comment(0xbf4b, 'Save the function code', align=Align.INLINE)
d.comment(0xbf4c, 'Evaluate the #handle, point at IWA', align=Align.INLINE)
d.comment(0xbf4f, 'X -> IWA for the result', align=Align.INLINE)
d.comment(0xbf51, 'Restore the function code', align=Align.INLINE)
d.comment(0xbf52, 'OSARGS: read PTR or EXT into IWA', align=Align.INLINE)
d.comment(0xbf55, 'Integer result', align=Align.INLINE)
d.comment(0xbf57, 'Return PTR/EXT', align=Align.INLINE)

# fn_bget (&BF6F): BGET#channel
d.comment(0xbf6f, 'Evaluate the #handle', align=Align.INLINE)
d.comment(0xbf72, 'OSBGET: read a byte from the channel', align=Align.INLINE)
d.comment(0xbf75, 'Return the byte as an integer', align=Align.INLINE)

# fn_openin (&BF78) / fn_openout (&BF7C): OSFIND open
d.comment(0xbf78, 'OSFIND &40: open an existing file for input', align=Align.INLINE)
d.comment(0xbf7a, 'do the open', align=Align.INLINE)
d.comment(0xbf7c, 'OSFIND &80: create a file for output', align=Align.INLINE)
d.comment(0xbf7e, 'do the open', align=Align.INLINE)

# stmt_lomem (&926F): LOMEM = value
d.comment(0x926f, 'Step past "=", evaluate an integer', align=Align.INLINE)
d.comment(0x9272, 'Set LOMEM (and empty the variables): low byte', align=Align.INLINE)
d.comment(0x9274, 'LOMEM low', align=Align.INLINE)
d.comment(0x9276, 'VARTOP low (no variables yet)', align=Align.INLINE)
d.comment(0x9278, 'high byte', align=Align.INLINE)
d.comment(0x927a, 'LOMEM high', align=Align.INLINE)
d.comment(0x927c, 'VARTOP high', align=Align.INLINE)
d.comment(0x927e, 'Clear all dynamic variables', align=Align.INLINE)
d.comment(0x9281, 'Back to the execution loop', align=Align.INLINE)

# stmt_move (&93E4): MOVE = PLOT 4
d.comment(0x93e4, 'MOVE is PLOT 4 (move the cursor, no draw)', align=Align.INLINE)
d.comment(0x93e6, 'do the PLOT', align=Align.INLINE)

# stmt_load (&BF24) / stmt_chain (&BF2A)
d.comment(0xbf24, 'Load the named program', align=Align.INLINE)
d.comment(0xbf27, 'Back to the immediate loop', align=Align.INLINE)
d.comment(0xbf2a, 'Load the named program', align=Align.INLINE)
d.comment(0xbf2d, 'then RUN it', align=Align.INLINE)

d.subroutine(0x8f1e, 'usr_call', title='Call user machine code (USR/CALL)',
             description="""Load A, X, Y and the flags from the resident integer
variables, then call the routine at the address in IWA. On return the
registers are captured back.""")

# read_via_ptr_general (&8942) / inc_ptr_general (&8944) / sub_c894b
d.comment(0x8942, 'Read the byte at (zp_general)+Y, then advance', align=Align.INLINE)
d.comment(0x8944, 'Increment the general pointer: low byte', align=Align.INLINE)
d.comment(0x8946, 'No carry: done', align=Align.INLINE)
d.comment(0x8948, 'Carry into the high byte', align=Align.INLINE)
d.comment(0x894a, 'Return (shared)', align=Align.INLINE)
d.comment(0x894b, 'Advance the pointer...', align=Align.INLINE)
d.comment(0x894e, '...then read the next byte', align=Align.INLINE)
d.comment(0x8950, 'Return the byte', align=Align.INLINE)

# fn_cos (&A98D): COS = SIN with a quadrant shift
d.comment(0xa98d, 'Evaluate the argument as a real', align=Align.INLINE)
d.comment(0xa990, 'Compute the SIN/COS kernel', align=Align.INLINE)
d.comment(0xa993, 'Shift the quadrant: cos x = sin(x + pi/2)', align=Align.INLINE)
d.comment(0xa995, 'Finish (shared with SIN)', align=Align.INLINE)

# fn_deg (&ABC2): radians -> degrees (multiply by 180/pi)
d.comment(0xabc2, 'Evaluate the argument as a real', align=Align.INLINE)
d.comment(0xabc5, 'Point at the constant 180/pi: low byte', align=Align.INLINE)
d.comment(0xabc7, 'high byte', align=Align.INLINE)
d.comment(0xabc9, 'Multiply FWA by it (radians -> degrees)', align=Align.INLINE)

# fn_usr (&ABD2): USR(addr) calls machine code, returns A,X,Y,P packed
d.comment(0xabd2, 'Evaluate the address argument as an integer', align=Align.INLINE)
d.comment(0xabd5, 'Set up registers and call the code', align=Align.INLINE)
d.comment(0xabd8, 'Returned A...', align=Align.INLINE)
d.comment(0xabda, '...and X into the low result bytes', align=Align.INLINE)
d.comment(0xabdc, 'Returned Y', align=Align.INLINE)
d.comment(0xabde, 'Returned flags...', align=Align.INLINE)
d.comment(0xabdf, '...', align=Align.INLINE)
d.comment(0xabe0, '...into the top result byte', align=Align.INLINE)
d.comment(0xabe2, 'Clear decimal mode the code may have left set', align=Align.INLINE)
d.comment(0xabe3, 'Integer result', align=Align.INLINE)
d.comment(0xabe5, 'Return the packed A,X,Y,P', align=Align.INLINE)
d.comment(0xabe6, 'Non-numeric address: Type mismatch', align=Align.INLINE)

# fn_not (&ACD1): NOT = one's complement of the integer
d.comment(0xacd1, 'Evaluate the argument as an integer', align=Align.INLINE)
d.comment(0xacd4, 'Complement all four IWA bytes', align=Align.INLINE)
d.comment(0xacd6, 'byte X...', align=Align.INLINE)
d.comment(0xacd8, "...one's complement", align=Align.INLINE)
d.comment(0xacda, '(store)', align=Align.INLINE)
d.comment(0xacdc, 'next byte', align=Align.INLINE)
d.comment(0xacdd, 'loop', align=Align.INLINE)
d.comment(0xacdf, 'Integer result', align=Align.INLINE)
d.comment(0xace1, 'Return NOT value', align=Align.INLINE)

# fn_to (&AEDC): TO followed by "P" returns TOP (end of program)
d.comment(0xaedc, 'Look at the character after TO', align=Align.INLINE)
d.comment(0xaede, '(get it)', align=Align.INLINE)
d.comment(0xaee0, 'Is it "P"? TO + P spells TOP', align=Align.INLINE)
d.comment(0xaee2, 'No: a bare TO here is a syntax error', align=Align.INLINE)
d.comment(0xaee4, 'Consume the P', align=Align.INLINE)
d.comment(0xaee6, 'TOP: end-of-program address, low byte', align=Align.INLINE)
d.comment(0xaee8, 'high byte (returned as an integer)', align=Align.INLINE)

# iwa_mod (&9E01): IWA = IWA MOD operand (shares the DIV/MOD core)
d.comment(0x9e01, 'MOD: divide', align=Align.INLINE)
d.comment(0x9e04, 'remainder takes the dividend sign', align=Align.INLINE)
d.comment(0x9e06, 'save the sign', align=Align.INLINE)
d.comment(0x9e07, 'load the remainder (&3D-&40) and apply the sign', align=Align.INLINE)

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

# fwa_div10 (&A24D): FWA = FWA / 10
d.comment(
    0xa24d,
    'Divide FWA by ten. In binary 1/10 = 0.000110011001100...,\n'
    'so x/10 is x/16 plus a series of progressively shifted terms.\n'
    'Each term is built in FWB as a byte/bit-shifted copy of the\n'
    "mantissa and accumulated into FWA. The result is unnormalised\n"
    'and unrounded (the caller normalises).',
    word_wrap=False,
)
d.comment(0xa24d, 'x/16: subtract 4 from the exponent', align=Align.INLINE)
d.comment(0xa24e, '(exponent)', align=Align.INLINE)
d.comment(0xa250, '(- 4)', align=Align.INLINE)
d.comment(0xa252, '(store)', align=Align.INLINE)
d.comment(0xa254, 'no borrow: continue', align=Align.INLINE)
d.comment(0xa256, 'borrow into the overflow byte', align=Align.INLINE)
d.comment(0xa258, 'FWB = x/2', align=Align.INLINE)
d.comment(0xa25b, 'accumulate a shifted term into FWA', align=Align.INLINE)
d.comment(0xa25e, 'FWB = x/2 again', align=Align.INLINE)
d.comment(0xa261, 'FWB /= 2', align=Align.INLINE)
d.comment(0xa264, 'FWB /= 2', align=Align.INLINE)
d.comment(0xa267, 'FWB /= 2', align=Align.INLINE)
d.comment(0xa26a, 'accumulate the next term', align=Align.INLINE)
d.comment(0xa26d, 'Form a byte-shifted copy in FWB: clear MSB', align=Align.INLINE)
d.comment(0xa26f, '(store)', align=Align.INLINE)
d.comment(0xa271, 'mantissa m1...', align=Align.INLINE)
d.comment(0xa273, '...to FWB m2', align=Align.INLINE)
d.comment(0xa275, 'm2...', align=Align.INLINE)
d.comment(0xa277, '...to m3', align=Align.INLINE)
d.comment(0xa279, 'm3...', align=Align.INLINE)
d.comment(0xa27b, '...to m4', align=Align.INLINE)
d.comment(0xa27d, 'm4...', align=Align.INLINE)
d.comment(0xa27f, '...to the rounding byte', align=Align.INLINE)
d.comment(0xa281, 'next mantissa bit...', align=Align.INLINE)
d.comment(0xa283, '...into the carry', align=Align.INLINE)
d.comment(0xa284, 'accumulate this term', align=Align.INLINE)
d.comment(0xa287, 'Form a copy shifted down two bytes: clear', align=Align.INLINE)
d.comment(0xa289, 'the top two mantissa bytes', align=Align.INLINE)
d.comment(0xa28b, '(store)', align=Align.INLINE)
d.comment(0xa28d, 'm1...', align=Align.INLINE)
d.comment(0xa28f, '...to m3', align=Align.INLINE)
d.comment(0xa291, 'm2...', align=Align.INLINE)
d.comment(0xa293, '...to m4', align=Align.INLINE)
d.comment(0xa295, 'm3...', align=Align.INLINE)
d.comment(0xa297, '...to rounding', align=Align.INLINE)
d.comment(0xa299, 'next bit...', align=Align.INLINE)
d.comment(0xa29b, '...into the carry', align=Align.INLINE)
d.comment(0xa29c, 'accumulate this term', align=Align.INLINE)
d.comment(0xa29f, 'continue propagating the shifted mantissa bits', align=Align.INLINE)
d.comment(0xa2a1, '...', align=Align.INLINE)
d.comment(0xa2a2, '...', align=Align.INLINE)

# fwb_unpack_var (&A34E): unpack the 5-byte value at (zp_fp_ptr) into FWB
d.comment(0xa34e, 'Copy the packed value, exponent last', align=Align.INLINE)
d.comment(0xa350, 'Packed byte 4...', align=Align.INLINE)
d.comment(0xa352, '...mantissa byte 4', align=Align.INLINE)
d.comment(0xa354, 'next byte', align=Align.INLINE)
d.comment(0xa355, 'byte 3...', align=Align.INLINE)
d.comment(0xa357, '...mantissa byte 3', align=Align.INLINE)
d.comment(0xa359, 'next byte', align=Align.INLINE)
d.comment(0xa35a, 'byte 2...', align=Align.INLINE)
d.comment(0xa35c, '...mantissa byte 2', align=Align.INLINE)
d.comment(0xa35e, 'next byte', align=Align.INLINE)
d.comment(0xa35f, 'byte 1 (sign + mantissa MSB)...', align=Align.INLINE)
d.comment(0xa361, '...into the sign byte', align=Align.INLINE)
d.comment(0xa363, 'next byte', align=Align.INLINE)
d.comment(0xa364, 'Clear the rounding byte (Y=0)', align=Align.INLINE)
d.comment(0xa366, 'and the overflow byte', align=Align.INLINE)
d.comment(0xa368, 'byte 0...', align=Align.INLINE)
d.comment(0xa36a, '...is the exponent', align=Align.INLINE)
d.comment(0xa36c, 'Test for zero: OR exponent with the mantissa...', align=Align.INLINE)
d.comment(0xa36e, 'm2,', align=Align.INLINE)
d.comment(0xa370, 'm3,', align=Align.INLINE)
d.comment(0xa372, 'm4', align=Align.INLINE)
d.comment(0xa374, 'All zero: leave the mantissa MSB clear', align=Align.INLINE)
d.comment(0xa376, 'Non-zero: restore the implied leading 1...', align=Align.INLINE)
d.comment(0xa378, 'set the top bit', align=Align.INLINE)
d.comment(0xa37a, 'Store the true mantissa MSB', align=Align.INLINE)
d.comment(0xa37c, 'FWB now holds the unpacked value', align=Align.INLINE)

# reserve_stack (&BE2E) remaining: collision check against the heap top
d.comment(0xbe2e, 'Set the new stack-pointer low byte', align=Align.INLINE)
d.comment(0xbe30, 'No borrow: high byte unchanged', align=Align.INLINE)
d.comment(0xbe32, 'Borrow: decrement the high byte', align=Align.INLINE)
d.comment(0xbe34, 'New stack-pointer high byte', align=Align.INLINE)
d.comment(0xbe38, 'New top below the heap page: No room', align=Align.INLINE)
d.comment(0xbe3a, 'Clearly above the heap: room available', align=Align.INLINE)
d.comment(0xbe3c, 'Same page: compare the low bytes', align=Align.INLINE)
d.comment(0xbe3e, 'Below the heap top: No room', align=Align.INLINE)
d.comment(0xbe40, 'Room available: return', align=Align.INLINE)

# find_proc_fn (&945B) remaining
d.comment(0x945b, 'Look at the PROC/FN token', align=Align.INLINE)
d.comment(0x945d, 'get it', align=Align.INLINE)
d.comment(0x9461, 'Is it PROC (&F2)?', align=Align.INLINE)
d.comment(0x9463, 'PROC: scan the PROC list', align=Align.INLINE)
d.comment(0x9465, 'FN: point at the FN list head', align=Align.INLINE)
d.comment(0x9467, 'scan the FN list', align=Align.INLINE)

# find_variable (&9469): walk the name's chain looking for a match
d.comment(
    0x9469,
    'Each variable chain (one per initial letter) is a list of\n'
    'entries: a 2-byte link to the next, the rest of the name, a\n'
    'NUL, then the value. The walk alternates two node pointers\n'
    '(&3A/&3B and &3C/&3D), reading one node\'s link while it\n'
    'compares the other - so it never copies a whole pointer.\n'
    'On a match IWA points at the value; zp_fileblk holds the\n'
    'length of the name being sought.',
    word_wrap=False,
)
d.comment(0x9469, 'Point at the first character of the name', align=Align.INLINE)
d.comment(0x946b, 'get it', align=Align.INLINE)
d.comment(0x946e, 'Y = 2 * char: index into the variable table', align=Align.INLINE)
d.comment(0x9472, 'Chain head low byte -> node pointer (&3A)', align=Align.INLINE)
d.comment(0x9474, 'Chain head high byte (&0400 + 1 + 2*char)', align=Align.INLINE)
d.comment(0x9477, 'node pointer high (&3B)', align=Align.INLINE)
d.comment(0x947b, 'Zero high byte: end of chain, not found', align=Align.INLINE)
d.comment(0x947d, 'Read the node: offset 0', align=Align.INLINE)
d.comment(0x947f, 'link low byte...', align=Align.INLINE)
d.comment(0x9481, '...saved (&3C)', align=Align.INLINE)
d.comment(0x9483, 'offset 1', align=Align.INLINE)
d.comment(0x9484, 'link high byte...', align=Align.INLINE)
d.comment(0x9486, '...saved (&3D)', align=Align.INLINE)
d.comment(0x9488, 'offset 2: first stored name character', align=Align.INLINE)
d.comment(0x9489, 'get it', align=Align.INLINE)
d.comment(0x948b, 'Non-null: compare the name', align=Align.INLINE)
d.comment(0x948d, 'Null name (the base entry): ...', align=Align.INLINE)
d.comment(0x948e, 'did the search name end too?', align=Align.INLINE)
d.comment(0x9490, 'no: follow the link', align=Align.INLINE)
d.comment(0x9492, 'advance', align=Align.INLINE)
d.comment(0x9493, 'match: compute the value pointer', align=Align.INLINE)
d.comment(0x9496, 'next stored name character', align=Align.INLINE)
d.comment(0x9498, 'entry name ended early: no match', align=Align.INLINE)
d.comment(0x949a, 'compare with the search name', align=Align.INLINE)
d.comment(0x949c, 'differ: follow the link', align=Align.INLINE)
d.comment(0x949e, 'reached the end of the search name?', align=Align.INLINE)
d.comment(0x94a0, 'no: keep comparing', align=Align.INLINE)
d.comment(0x94a2, 'does the entry name end here too?', align=Align.INLINE)
d.comment(0x94a3, '...', align=Align.INLINE)
d.comment(0x94a5, 'entry name is longer: no match', align=Align.INLINE)
d.comment(0x94a8, 'value pointer = node + name length: low', align=Align.INLINE)
d.comment(0x94aa, '(IWA low)', align=Align.INLINE)
d.comment(0x94ac, 'node high...', align=Align.INLINE)
d.comment(0x94ae, '+ carry', align=Align.INLINE)
d.comment(0x94b0, 'IWA high = pointer to the value', align=Align.INLINE)
d.comment(0x94b2, 'Return (IWA = value pointer, or not found)', align=Align.INLINE)
d.comment(0x94b5, 'Zero high byte: end of chain, not found', align=Align.INLINE)
d.comment(0x94b7, 'Read the next node via its saved link (&3C)', align=Align.INLINE)
d.comment(0x94b9, 'link low byte...', align=Align.INLINE)
d.comment(0x94bb, '...into the node pointer (&3A)', align=Align.INLINE)
d.comment(0x94bd, 'offset 1', align=Align.INLINE)
d.comment(0x94be, 'link high byte...', align=Align.INLINE)
d.comment(0x94c0, '...(&3B)', align=Align.INLINE)
d.comment(0x94c2, 'offset 2: name character', align=Align.INLINE)
d.comment(0x94c3, 'get it', align=Align.INLINE)
d.comment(0x94c5, 'Non-null: compare the name', align=Align.INLINE)
d.comment(0x94c7, 'Null name: ...', align=Align.INLINE)
d.comment(0x94c8, 'did the search name end too?', align=Align.INLINE)
d.comment(0x94ca, 'no: back to the other-pointer loop', align=Align.INLINE)
d.comment(0x94cc, 'advance', align=Align.INLINE)
d.comment(0x94cd, 'match: compute the value pointer', align=Align.INLINE)
d.comment(0x94cf, 'compare loop', align=Align.INLINE)
d.comment(0x94d0, 'next stored character', align=Align.INLINE)
d.comment(0x94d2, 'entry name ended: no match', align=Align.INLINE)
d.comment(0x94d4, 'compare with the search name', align=Align.INLINE)
d.comment(0x94d6, 'differ: next entry', align=Align.INLINE)
d.comment(0x94d8, 'end of the search name?', align=Align.INLINE)
d.comment(0x94da, 'no: keep comparing', align=Align.INLINE)
d.comment(0x94dc, 'does the entry name end here too?', align=Align.INLINE)
d.comment(0x94dd, '...', align=Align.INLINE)
d.comment(0x94df, 'entry name is longer: no match', align=Align.INLINE)
d.comment(0x94e1, 'value pointer = node + name length: low', align=Align.INLINE)
d.comment(0x94e2, '...', align=Align.INLINE)
d.comment(0x94e4, '(IWA low)', align=Align.INLINE)
d.comment(0x94e6, 'node high...', align=Align.INLINE)
d.comment(0x94e8, '+ carry', align=Align.INLINE)
d.comment(0x94ea, 'IWA high = pointer to the value', align=Align.INLINE)
d.comment(0x94ec, 'Return the value pointer', align=Align.INLINE)
# sub_c94ed (&94ED): pick the PROC or FN chain head
d.comment(0x94ed, 'Look at the PROC/FN token', align=Align.INLINE)
d.comment(0x94ef, 'get it', align=Align.INLINE)
d.comment(0x94f1, 'to X', align=Align.INLINE)
d.comment(0x94f2, 'PROC list index (&F6)', align=Align.INLINE)
d.comment(0x94f4, 'Is it PROC?', align=Align.INLINE)
d.comment(0x94f6, 'PROC: use that chain', align=Align.INLINE)
d.comment(0x94f8, 'FN list index (&F8)', align=Align.INLINE)
d.comment(0x94fa, 'use the FN chain', align=Align.INLINE)

d.subroutine(0x909f, 'advance_to_next_line',
             title='Advance the general pointer to the next program line',
             description='Add the line length (at offset 3) to zp_general; carry clear on return.')

# stmt_renumber (&8FA3): RENUMBER [start[,step]]
d.comment(
    0x8fa3,
    'RENUMBER in three passes. Pass 1 records every line\'s\n'
    'original number in a table built upwards from the heap (via\n'
    '&3B/&3C), erroring if it reaches HIMEM. Pass 2 writes the new\n'
    'numbers (start, step) into the lines. Pass 3 scans the\n'
    'program for line-number references (the &8D token) and\n'
    'rewrites each via the old->new table.',
    word_wrap=False,
)
d.comment(0x8fa3, 'Parse the start and step arguments', align=Align.INLINE)
d.comment(0x8fa6, 'Pop the step into the file block (&39)', align=Align.INLINE)
d.comment(0x8fa8, '(pop it)', align=Align.INLINE)
d.comment(0x8fab, 'Pop the start number', align=Align.INLINE)
d.comment(0x8fae, 'Point at the program start and the table', align=Align.INLINE)
d.comment(0x8fb1, 'Pass 1: for each line, read its number', align=Align.INLINE)
d.comment(0x8fb3, 'high byte', align=Align.INLINE)
d.comment(0x8fb5, 'high bit set marks the end of program', align=Align.INLINE)
d.comment(0x8fb7, 'Store the old number in the table', align=Align.INLINE)
d.comment(0x8fb9, 'low byte', align=Align.INLINE)
d.comment(0x8fba, '...', align=Align.INLINE)
d.comment(0x8fbc, '(store)', align=Align.INLINE)
d.comment(0x8fbe, 'Advance the table pointer by 2: low', align=Align.INLINE)
d.comment(0x8fbf, '...', align=Align.INLINE)
d.comment(0x8fc0, '...', align=Align.INLINE)
d.comment(0x8fc2, '(store)', align=Align.INLINE)
d.comment(0x8fc4, 'keep the low byte', align=Align.INLINE)
d.comment(0x8fc5, 'table pointer high...', align=Align.INLINE)
d.comment(0x8fc7, '+ carry', align=Align.INLINE)
d.comment(0x8fc9, '(store)', align=Align.INLINE)
d.comment(0x8fcb, 'Has the table reached HIMEM?', align=Align.INLINE)
d.comment(0x8fcd, '...', align=Align.INLINE)
d.comment(0x8fcf, 'yes: no room for the table', align=Align.INLINE)
d.comment(0x8fd1, 'Advance to the next program line', align=Align.INLINE)
d.comment(0x8fd4, 'loop over all lines', align=Align.INLINE)
d.comment(0x8fd6, 'RENUMBER ran out of space: error', align=Align.INLINE)
d.comment(0x8fdf, 'error block', align=Align.INLINE)
d.comment(0x8fe7, 'Pass 2: reset to the program start', align=Align.INLINE)
d.comment(0x8fea, 'for each line:', align=Align.INLINE)
d.comment(0x8fec, 'line number high byte', align=Align.INLINE)
d.comment(0x8fee, 'end of program: go to pass 3', align=Align.INLINE)
d.comment(0x8ff0, 'Write the new number: high byte', align=Align.INLINE)
d.comment(0x8ff2, '(into the line)', align=Align.INLINE)
d.comment(0x8ff4, 'low byte', align=Align.INLINE)
d.comment(0x8ff6, 'advance', align=Align.INLINE)
d.comment(0x8ff7, '(into the line)', align=Align.INLINE)
d.comment(0x8ff9, 'Add the step to the running number: low', align=Align.INLINE)
d.comment(0x8ffa, '...', align=Align.INLINE)
d.comment(0x8ffc, '...', align=Align.INLINE)
d.comment(0x8ffe, '(store)', align=Align.INLINE)
d.comment(0x9000, 'high byte...', align=Align.INLINE)
d.comment(0x9002, '+ carry', align=Align.INLINE)
d.comment(0x9004, 'keep it a valid line number (< &8000)', align=Align.INLINE)
d.comment(0x9006, '(store)', align=Align.INLINE)
d.comment(0x9008, 'Advance to the next line', align=Align.INLINE)
d.comment(0x900b, 'loop', align=Align.INLINE)
d.comment(0x900d, 'Pass 3: scan from PAGE, high byte', align=Align.INLINE)
d.comment(0x900f, '(text pointer high)', align=Align.INLINE)
d.comment(0x9011, 'low byte 0', align=Align.INLINE)
d.comment(0x9013, '(store)', align=Align.INLINE)
d.comment(0x9015, 'advance', align=Align.INLINE)
d.comment(0x9016, 'read the line number high byte', align=Align.INLINE)
d.comment(0x9018, 'end of program: done', align=Align.INLINE)
d.comment(0x901a, 'Scan the line from offset 4 (past the header)', align=Align.INLINE)
d.comment(0x901c, 'next token', align=Align.INLINE)
d.comment(0x901e, 'Is it the line-number prefix &8D?', align=Align.INLINE)
d.comment(0x9020, 'yes: rewrite the reference', align=Align.INLINE)
d.comment(0x9022, 'advance', align=Align.INLINE)
d.comment(0x9023, 'end of line (CR)?', align=Align.INLINE)
d.comment(0x9025, 'no: keep scanning', align=Align.INLINE)
d.comment(0x9027, "read the next line's header", align=Align.INLINE)
d.comment(0x9029, 'end of program', align=Align.INLINE)
d.comment(0x902b, 'line length is at offset 3', align=Align.INLINE)
d.comment(0x902d, 'get it', align=Align.INLINE)
d.comment(0x902f, 'advance to the next line: low', align=Align.INLINE)
d.comment(0x9030, '...', align=Align.INLINE)
d.comment(0x9032, '(store)', align=Align.INLINE)
d.comment(0x9034, 'loop', align=Align.INLINE)
d.comment(0x9036, 'carry into high byte', align=Align.INLINE)
d.comment(0x9038, 'loop', align=Align.INLINE)
d.comment(0x903a, 'Done: back to the immediate loop', align=Align.INLINE)
d.comment(0x903d, 'Decode the &8D-encoded line number', align=Align.INLINE)
d.comment(0x9040, 'Point at the old->new table', align=Align.INLINE)
d.comment(0x9043, 'Search the table for this old number:', align=Align.INLINE)
d.comment(0x9045, 'table end marker?', align=Align.INLINE)
d.comment(0x9047, 'not found: reference to a missing line', align=Align.INLINE)
d.comment(0x9049, 'old number high...', align=Align.INLINE)
d.comment(0x904b, 'advance', align=Align.INLINE)
d.comment(0x904c, 'match the referenced number high?', align=Align.INLINE)
d.comment(0x904e, 'no: next table entry', align=Align.INLINE)
d.comment(0x9050, 'old number low...', align=Align.INLINE)
d.comment(0x9052, 'match low?', align=Align.INLINE)
d.comment(0x9054, 'no: next entry', align=Align.INLINE)
d.comment(0x9056, 'Found: take the new number high', align=Align.INLINE)
d.comment(0x9058, '(save)', align=Align.INLINE)
d.comment(0x905a, 'new number low', align=Align.INLINE)
d.comment(0x905b, '...', align=Align.INLINE)
d.comment(0x905d, '(save)', align=Align.INLINE)
d.comment(0x905f, 'position within the line', align=Align.INLINE)
d.comment(0x9061, '...', align=Align.INLINE)
d.comment(0x9062, 'Point at the reference in the line: low', align=Align.INLINE)
d.comment(0x9064, '...', align=Align.INLINE)
d.comment(0x9066, 'high', align=Align.INLINE)
d.comment(0x9068, '...', align=Align.INLINE)
d.comment(0x906a, 'Re-encode the new line number in place', align=Align.INLINE)
d.comment(0x906d, 'resume scanning', align=Align.INLINE)
d.comment(0x906f, 'continue the line scan', align=Align.INLINE)
d.comment(0x9071, 'Next table entry: advance...', align=Align.INLINE)
d.comment(0x9074, '...the table pointer by 2', align=Align.INLINE)
d.comment(0x9076, '...', align=Align.INLINE)
d.comment(0x9078, '(store)', align=Align.INLINE)
d.comment(0x907a, 'loop', align=Align.INLINE)
d.comment(0x907c, 'carry', align=Align.INLINE)
d.comment(0x907e, 'loop', align=Align.INLINE)
d.comment(0x9080, 'Reference to a missing line: report it', align=Align.INLINE)
d.comment(0x9083, 'build the "Failed at <line>" message...', align=Align.INLINE)
d.comment(0x9085, '...', align=Align.INLINE)
d.comment(0x9087, '...', align=Align.INLINE)
d.comment(0x9089, '...', align=Align.INLINE)
d.comment(0x908c, 'print it', align=Align.INLINE)
# advance_to_next_line (&909F)
d.comment(0x909f, 'Line length is at offset 3', align=Align.INLINE)
d.comment(0x90a0, 'get the line length', align=Align.INLINE)
d.comment(0x90a2, 'add it to the pointer: low', align=Align.INLINE)
d.comment(0x90a4, '(store)', align=Align.INLINE)
d.comment(0x90a6, 'no carry: done', align=Align.INLINE)
d.comment(0x90a8, 'carry into the high byte', align=Align.INLINE)
d.comment(0x90aa, 'clear carry for the caller', align=Align.INLINE)
d.comment(0x90ab, 'Return at the next line', align=Align.INLINE)

d.subroutine(0x9531, 'clear_value_bytes', title='Zero a run of value bytes',
             description='Write X zero bytes after the variable name (initialise its value).')
d.subroutine(0x9559, 'validate_var_name', title='Validate / measure a variable name',
             description='Scan a variable name, counting its characters (letters, digits, _); a leading digit is rejected.')

# statement_loop (&8B9B) remaining
d.comment(0x8b9d, 'Get the current character', align=Align.INLINE)
d.comment(0x8ba1, 'Not a colon: check for ELSE / end of line', align=Align.INLINE)
d.comment(0x8ba5, 'advance past the colon', align=Align.INLINE)
d.comment(0x8ba7, 'Get the next character', align=Align.INLINE)
d.comment(0x8ba9, 'Skip spaces', align=Align.INLINE)
d.comment(0x8bab, 'loop', align=Align.INLINE)
d.comment(0x8baf, 'Below &CF: a variable assignment', align=Align.INLINE)

# usr_call (&8F1E)
d.comment(0x8f1e, 'C% supplies the carry...', align=Align.INLINE)
d.comment(0x8f21, '...shifted into the carry flag', align=Align.INLINE)
d.comment(0x8f22, 'A from A%', align=Align.INLINE)
d.comment(0x8f25, 'X from X%', align=Align.INLINE)
d.comment(0x8f28, 'Y from Y%', align=Align.INLINE)
d.comment(0x8f2b, 'Call the routine at the address in IWA', align=Align.INLINE)
d.comment(0x8f2e, 'error (shared)', align=Align.INLINE)

# create_variable (&94FC): append a new entry to the name's chain
d.comment(0x94fc, 'First character of the name', align=Align.INLINE)
d.comment(0x94fe, 'get it', align=Align.INLINE)
d.comment(0x9500, 'double it to index the variable table', align=Align.INLINE)
d.comment(0x9501, 'chain pointer low (&3A)', align=Align.INLINE)
d.comment(0x9503, 'table base high page (&04)', align=Align.INLINE)
d.comment(0x9505, 'chain pointer high (&3B)', align=Align.INLINE)
d.comment(0x9507, 'Walk to the end of the chain: link high', align=Align.INLINE)
d.comment(0x9509, 'zero: found the end, append here', align=Align.INLINE)
d.comment(0x950b, 'save it', align=Align.INLINE)
d.comment(0x950c, 'link low', align=Align.INLINE)
d.comment(0x950d, '...', align=Align.INLINE)
d.comment(0x950f, 'follow the link: low', align=Align.INLINE)
d.comment(0x9511, 'high', align=Align.INLINE)
d.comment(0x9513, 'advance', align=Align.INLINE)
d.comment(0x9514, 'loop', align=Align.INLINE)
d.comment(0x9516, 'Link the new entry (at VARTOP): high...', align=Align.INLINE)
d.comment(0x9518, '...into the previous link', align=Align.INLINE)
d.comment(0x951a, 'low...', align=Align.INLINE)
d.comment(0x951c, '...', align=Align.INLINE)
d.comment(0x951d, '(store)', align=Align.INLINE)
d.comment(0x951f, 'the new entry header', align=Align.INLINE)
d.comment(0x9520, '...', align=Align.INLINE)
d.comment(0x9521, '(store)', align=Align.INLINE)
d.comment(0x9523, 'name length reached?', align=Align.INLINE)
d.comment(0x9525, 'done', align=Align.INLINE)
d.comment(0x9527, 'Copy the name into the entry:', align=Align.INLINE)
d.comment(0x9528, 'name char...', align=Align.INLINE)
d.comment(0x952a, '...into the entry', align=Align.INLINE)
d.comment(0x952c, 'all of the name?', align=Align.INLINE)
d.comment(0x952e, 'loop', align=Align.INLINE)
d.comment(0x9530, 'Return', align=Align.INLINE)
d.comment(0x9531, 'Zero X value bytes after the name:', align=Align.INLINE)
d.comment(0x9533, 'advance', align=Align.INLINE)
d.comment(0x9534, 'clear a byte', align=Align.INLINE)
d.comment(0x9536, 'count down', align=Align.INLINE)
d.comment(0x9537, 'loop', align=Align.INLINE)
d.comment(0x9539, 'Advance VARTOP past the new entry:', align=Align.INLINE)
d.comment(0x953a, 'Y = bytes used', align=Align.INLINE)
d.comment(0x953b, 'low', align=Align.INLINE)
d.comment(0x953d, 'no carry into the high byte', align=Align.INLINE)
d.comment(0x953f, 'carry into high', align=Align.INLINE)
d.comment(0x9541, "Check VARTOP hasn't reached the stack:", align=Align.INLINE)
d.comment(0x9543, 'compare high', align=Align.INLINE)
d.comment(0x9545, 'below: room', align=Align.INLINE)
d.comment(0x9547, 'above: no room', align=Align.INLINE)
d.comment(0x9549, 'equal: compare low', align=Align.INLINE)
d.comment(0x954b, 'below: room', align=Align.INLINE)
d.comment(0x954d, 'No room: unlink the new entry...', align=Align.INLINE)
d.comment(0x954f, 'link field offset', align=Align.INLINE)
d.comment(0x9551, '(clear the link)', align=Align.INLINE)
d.comment(0x9553, 'No room error', align=Align.INLINE)
d.comment(0x9556, 'Commit the new VARTOP', align=Align.INLINE)
d.comment(0x9558, 'Return', align=Align.INLINE)
d.comment(0x9559, 'Validate the name from offset 1:', align=Align.INLINE)
d.comment(0x955b, 'character...', align=Align.INLINE)
d.comment(0x955d, 'below "0": end of name', align=Align.INLINE)
d.comment(0x955f, '...', align=Align.INLINE)
d.comment(0x9561, 'in the digit/symbol range?', align=Align.INLINE)
d.comment(0x9563, 'letter range: continue', align=Align.INLINE)
d.comment(0x9565, '":" or above (not a digit)?', align=Align.INLINE)
d.comment(0x9567, 'not a name character: stop', align=Align.INLINE)
d.comment(0x9569, 'is this the first character?', align=Align.INLINE)
d.comment(0x956b, "names can't start with a digit", align=Align.INLINE)
d.comment(0x956d, 'count the character', align=Align.INLINE)
d.comment(0x956e, 'next', align=Align.INLINE)
d.comment(0x956f, 'loop', align=Align.INLINE)
d.comment(0x9571, 'below "_"?', align=Align.INLINE)
d.comment(0x9573, '...', align=Align.INLINE)
d.comment(0x9575, 'A-Z?', align=Align.INLINE)
d.comment(0x9577, 'letter: accept', align=Align.INLINE)
d.comment(0x9579, 'Return', align=Align.INLINE)
d.comment(0x957a, 'a-z?', align=Align.INLINE)
d.comment(0x957c, 'accept', align=Align.INLINE)
d.comment(0x957e, 'Return', align=Align.INLINE)
d.comment(0x957f, 'Zero the value bytes of the new variable', align=Align.INLINE)

# read_key_timed (&AFAD) remaining
d.comment(0xafad, 'Evaluate the time-limit argument', align=Align.INLINE)
d.comment(0xafb0, 'OSBYTE &81: INKEY (read a key with a timeout)', align=Align.INLINE)
d.comment(0xafb2, 'time limit low', align=Align.INLINE)
d.comment(0xafb4, 'time limit high', align=Align.INLINE)

# stmt_repeat (&BBE4) remaining
d.comment(0xbbe8, 'Too many nested REPEATs', align=Align.INLINE)
d.comment(0xbbea, 'Point PtrA at the loop start', align=Align.INLINE)
d.comment(0xbbef, 'Store the loop position: low', align=Align.INLINE)
d.comment(0xbbf2, 'high', align=Align.INLINE)
d.comment(0xbbf4, '(store)', align=Align.INLINE)
d.comment(0xbbf7, 'One more REPEAT outstanding', align=Align.INLINE)
d.comment(0xbbf9, 'Continue execution', align=Align.INLINE)
d.comment(0xbbfc, 'Point at the string buffer (&0600): low', align=Align.INLINE)
d.comment(0xbbfe, 'high', align=Align.INLINE)
d.comment(0xbc00, '...', align=Align.INLINE)

# clear_vars_heap_stack (&BD20)
d.comment(0xbd20, 'LOMEM and VARTOP = TOP: low', align=Align.INLINE)
d.comment(0xbd22, 'LOMEM low', align=Align.INLINE)
d.comment(0xbd24, 'VARTOP low', align=Align.INLINE)
d.comment(0xbd26, 'high', align=Align.INLINE)
d.comment(0xbd28, 'LOMEM high', align=Align.INLINE)
d.comment(0xbd2a, 'VARTOP high', align=Align.INLINE)
d.comment(0xbd2c, 'Clear the DATA pointer and the stacks', align=Align.INLINE)
d.comment(0xbd2f, 'Clear the variable table (&0480-&04FF):', align=Align.INLINE)
d.comment(0xbd31, '...', align=Align.INLINE)
d.comment(0xbd33, 'clear a byte', align=Align.INLINE)
d.comment(0xbd36, 'count down', align=Align.INLINE)
d.comment(0xbd37, 'loop', align=Align.INLINE)
d.comment(0xbd39, 'Return', align=Align.INLINE)
d.comment(0xbd3a, 'DATA pointer = PAGE: high', align=Align.INLINE)
d.comment(0xbd3c, '(data pointer high)', align=Align.INLINE)
d.comment(0xbd3e, 'STACK = HIMEM: low', align=Align.INLINE)
d.comment(0xbd40, '(store)', align=Align.INLINE)
d.comment(0xbd42, 'HIMEM high', align=Align.INLINE)
d.comment(0xbd44, '(store)', align=Align.INLINE)
d.comment(0xbd46, 'Clear the loop/subroutine levels:', align=Align.INLINE)
d.comment(0xbd48, 'REPEAT', align=Align.INLINE)
d.comment(0xbd4a, 'FOR', align=Align.INLINE)
d.comment(0xbd4c, 'GOSUB', align=Align.INLINE)
d.comment(0xbd4e, 'DATA pointer low = 0 (= PAGE)', align=Align.INLINE)
d.comment(0xbd50, 'Return', align=Align.INLINE)

# iwa_store_zp (&BE44): copy IWA into the 4-byte variable at &00+X
d.comment(0xbe44, 'Copy IWA to the zp variable at X: byte 0', align=Align.INLINE)
d.comment(0xbe46, '(&00+X)', align=Align.INLINE)
d.comment(0xbe48, 'byte 1', align=Align.INLINE)
d.comment(0xbe4a, '(&01+X)', align=Align.INLINE)
d.comment(0xbe4c, 'byte 2', align=Align.INLINE)
d.comment(0xbe4e, '(&02+X)', align=Align.INLINE)
d.comment(0xbe50, 'byte 3', align=Align.INLINE)
d.comment(0xbe52, '(&03+X)', align=Align.INLINE)
d.comment(0xbe54, 'Done', align=Align.INLINE)
# sub_cbe55 (&BE55): scale FWB by adding Y to its exponent
d.comment(0xbe55, 'Add without carry', align=Align.INLINE)
d.comment(0xbe56, 'A = the amount (Y)', align=Align.INLINE)
d.comment(0xbe57, 'add it to the FWB exponent', align=Align.INLINE)
d.comment(0xbe59, '(store)', align=Align.INLINE)
d.comment(0xbe5b, 'no carry: done', align=Align.INLINE)
d.comment(0xbe5d, 'carry into the mantissa MSB', align=Align.INLINE)
d.comment(0xbe5f, 'Y = 1', align=Align.INLINE)
d.comment(0xbe61, 'Return', align=Align.INLINE)

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

# print_inline_string (&BFCF): print the bit-7-terminated string that
# follows the JSR, then resume at the terminator byte (an opcode).
d.hook_subroutine(0xbfcf, 'print_inline_string', stringhi_hook)
d.comment(0xbfcf, 'Pull the return address: it points at the string',
          align=Align.INLINE)
d.comment(0xbfd0, '(low)', align=Align.INLINE)
d.comment(0xbfd2, '(pull high)', align=Align.INLINE)
d.comment(0xbfd3, '(high)', align=Align.INLINE)
d.comment(0xbfd5, 'Start before the first character', align=Align.INLINE)
d.comment(0xbfd7, 'jump in to fetch it', align=Align.INLINE)
d.comment(0xbfd9, 'Print the character', align=Align.INLINE)
d.comment(0xbfdc, 'Advance and fetch the next character', align=Align.INLINE)
d.comment(0xbfdf, 'Loop while bit 7 is clear', align=Align.INLINE)
d.comment(0xbfe1, 'Resume at the terminator (the next instruction)',
          align=Align.INLINE)

# ======================================================================
# DEPTH 1 routines
# ======================================================================

d.subroutine(0xbdcb, 'unstack_string', title='Pop a string off the BASIC stack',
             description='Copy the string on top of the stack into the string buffer and drop it.')
d.subroutine(0x9236, 'imul16', title='16-bit integer multiply (IWA * FWB)',
             description='Multiply IWA by the value in the FWB mantissa by shift-and-add; "Too big" on overflow.')

# stack_integer (&BD94): push the 4-byte IWA, MSB first
d.comment(0xbd94, 'From the stack top...', align=Align.INLINE)
d.comment(0xbd96, 'prepare subtraction', align=Align.INLINE)
d.comment(0xbd99, 'reserve the space (check for room)', align=Align.INLINE)
d.comment(0xbd9c, 'Copy IWA, MSB first: byte 3', align=Align.INLINE)
d.comment(0xbd9e, '...', align=Align.INLINE)
d.comment(0xbda0, '(store)', align=Align.INLINE)
d.comment(0xbda2, 'next', align=Align.INLINE)
d.comment(0xbda3, 'byte 2', align=Align.INLINE)
d.comment(0xbda5, '(store)', align=Align.INLINE)
d.comment(0xbda7, 'next', align=Align.INLINE)
d.comment(0xbda8, 'byte 1', align=Align.INLINE)
d.comment(0xbdaa, '(store)', align=Align.INLINE)
d.comment(0xbdac, 'next', align=Align.INLINE)
d.comment(0xbdad, 'byte 0 (LSB)', align=Align.INLINE)
d.comment(0xbdaf, '(store)', align=Align.INLINE)
d.comment(0xbdb1, 'Integer pushed', align=Align.INLINE)

# stack_real (&BD51): push the packed 5-byte FWA
d.comment(0xbd51, 'From the stack top...', align=Align.INLINE)
d.comment(0xbd53, 'prepare subtraction', align=Align.INLINE)
d.comment(0xbd56, 'reserve the space', align=Align.INLINE)
d.comment(0xbd59, 'Packed byte 0 = exponent', align=Align.INLINE)
d.comment(0xbd5b, '...', align=Align.INLINE)
d.comment(0xbd5d, '(store)', align=Align.INLINE)
d.comment(0xbd5f, 'advance', align=Align.INLINE)
d.comment(0xbd60, 'Take the sign...', align=Align.INLINE)
d.comment(0xbd64, 'keep just the sign bit', align=Align.INLINE)
d.comment(0xbd66, 'mantissa MSB', align=Align.INLINE)
d.comment(0xbd68, 'drop the implied 1', align=Align.INLINE)
d.comment(0xbd6a, 'fold in the sign', align=Align.INLINE)
d.comment(0xbd6c, 'byte 1', align=Align.INLINE)
d.comment(0xbd6e, 'advance', align=Align.INLINE)
d.comment(0xbd6f, 'byte 2', align=Align.INLINE)
d.comment(0xbd71, '(store)', align=Align.INLINE)
d.comment(0xbd73, 'advance', align=Align.INLINE)
d.comment(0xbd74, 'byte 3', align=Align.INLINE)
d.comment(0xbd76, '(store)', align=Align.INLINE)
d.comment(0xbd78, 'advance', align=Align.INLINE)
d.comment(0xbd79, 'byte 4', align=Align.INLINE)
d.comment(0xbd7b, '(store)', align=Align.INLINE)
d.comment(0xbd7d, 'Real pushed', align=Align.INLINE)

# stack_string (&BDB2) / unstack_string (&BDCB)
d.comment(0xbdb2, 'From the stack top...', align=Align.INLINE)
d.comment(0xbdb3, '...', align=Align.INLINE)
d.comment(0xbdb7, 'reserve the space', align=Align.INLINE)
d.comment(0xbdba, 'string length', align=Align.INLINE)
d.comment(0xbdbc, 'zero length: just push the length', align=Align.INLINE)
d.comment(0xbdbe, 'Copy the string from the buffer (&0600): char Y', align=Align.INLINE)
d.comment(0xbdc1, '(onto the stack)', align=Align.INLINE)
d.comment(0xbdc3, 'next', align=Align.INLINE)
d.comment(0xbdc4, 'loop', align=Align.INLINE)
d.comment(0xbdc6, 'Push the length last', align=Align.INLINE)
d.comment(0xbdc8, '(store)', align=Align.INLINE)
d.comment(0xbdca, 'String pushed', align=Align.INLINE)
d.comment(0xbdcb, 'Pop a string: read its length', align=Align.INLINE)
d.comment(0xbdcd, '...', align=Align.INLINE)
d.comment(0xbdcf, '(store)', align=Align.INLINE)
d.comment(0xbdd1, 'zero length: just drop the length', align=Align.INLINE)
d.comment(0xbdd3, 'Y = length', align=Align.INLINE)
d.comment(0xbdd4, 'Copy the string to the buffer: char Y', align=Align.INLINE)
d.comment(0xbdd6, '(into the buffer)', align=Align.INLINE)
d.comment(0xbdd9, 'next', align=Align.INLINE)
d.comment(0xbdda, 'loop', align=Align.INLINE)
d.comment(0xbddc, 'Drop the string: get its length', align=Align.INLINE)
d.comment(0xbdde, '...', align=Align.INLINE)
d.comment(0xbde0, '...', align=Align.INLINE)
d.comment(0xbde1, 'advance the stack pointer past it: low', align=Align.INLINE)
d.comment(0xbde3, '(store)', align=Align.INLINE)
d.comment(0xbde5, 'done', align=Align.INLINE)
d.comment(0xbde7, 'carry into high', align=Align.INLINE)
d.comment(0xbde9, 'Return', align=Align.INLINE)

# imul16 (&9231/&9236): IWA = IWA * FWB (shift-and-add)
d.comment(0x9231, 'Unstack the multiplier (into &3F area)', align=Align.INLINE)
d.comment(0x9233, '...', align=Align.INLINE)
d.comment(0x9236, 'Clear the running product (X:Y)', align=Align.INLINE)
d.comment(0x9238, 'high in X, low in Y', align=Align.INLINE)
d.comment(0x923a, 'Shift the multiplier right: next bit into carry', align=Align.INLINE)
d.comment(0x923c, 'low byte (next bit -> carry)', align=Align.INLINE)
d.comment(0x923e, 'bit clear: skip the add', align=Align.INLINE)
d.comment(0x9240, 'bit set: add the multiplicand (IWA)', align=Align.INLINE)
d.comment(0x9241, 'product low...', align=Align.INLINE)
d.comment(0x9242, 'low', align=Align.INLINE)
d.comment(0x9244, '(into Y)', align=Align.INLINE)
d.comment(0x9245, 'product high...', align=Align.INLINE)
d.comment(0x9246, 'high', align=Align.INLINE)
d.comment(0x9248, '(into X)', align=Align.INLINE)
d.comment(0x9249, 'overflow: Too big', align=Align.INLINE)
d.comment(0x924b, 'Double the multiplicand: low', align=Align.INLINE)
d.comment(0x924d, 'high', align=Align.INLINE)
d.comment(0x924f, 'more multiplier bits?', align=Align.INLINE)
d.comment(0x9251, 'any multiplier bits left?', align=Align.INLINE)
d.comment(0x9253, 'loop', align=Align.INLINE)
d.comment(0x9255, 'Store the product: low', align=Align.INLINE)
d.comment(0x9257, 'high', align=Align.INLINE)
d.comment(0x9259, 'Return', align=Align.INLINE)
d.comment(0x925a, 'overflow error', align=Align.INLINE)

# fwa_mul10 (&A1F4): FWA = FWA * 10
d.comment(0xa1f4, 'x*8: add 3 to the exponent', align=Align.INLINE)
d.comment(0xa1f5, '...', align=Align.INLINE)
d.comment(0xa1f7, '...', align=Align.INLINE)
d.comment(0xa1f9, '(store)', align=Align.INLINE)
d.comment(0xa1fb, 'no carry', align=Align.INLINE)
d.comment(0xa1fd, 'carry into overflow', align=Align.INLINE)
d.comment(0xa1ff, 'FWB = x*8', align=Align.INLINE)
d.comment(0xa202, 'FWB = x*4', align=Align.INLINE)
d.comment(0xa205, 'FWB = x*2', align=Align.INLINE)
d.comment(0xa208, 'FWA = x*8 + x*2 = x*10', align=Align.INLINE)
d.comment(0xa20b, 'no overflow: done', align=Align.INLINE)
d.comment(0xa20d, 'Overflow: shift right, bump exponent: m1', align=Align.INLINE)
d.comment(0xa20f, 'm2', align=Align.INLINE)
d.comment(0xa211, 'm3', align=Align.INLINE)
d.comment(0xa213, 'm4', align=Align.INLINE)
d.comment(0xa215, 'rounding', align=Align.INLINE)
d.comment(0xa217, 'exponent + 1', align=Align.INLINE)
d.comment(0xa219, 'done', align=Align.INLINE)
d.comment(0xa21b, 'exponent overflow', align=Align.INLINE)
d.comment(0xa21d, 'Return', align=Align.INLINE)

d.subroutine(0xadad, 'read_string_literal', title='Read a string literal',
             description='Read a quoted ("...", with "" for a literal quote) or unquoted string into the string buffer.')

# fwa_round (&A65C) remaining
d.comment(0xa65e, 'compare with half (&80)', align=Align.INLINE)
d.comment(0xa666, 'add 1 via the carry ripple', align=Align.INLINE)
d.comment(0xa669, 'then finish', align=Align.INLINE)
d.comment(0xa66c, 'BRK error block: "Too big"', align=Align.INLINE)
d.comment(0xa676, 'Exactly half: force the mantissa LSB', align=Align.INLINE)
d.comment(0xa678, '...', align=Align.INLINE)
d.comment(0xa67a, '(store)', align=Align.INLINE)
d.comment(0xa67e, 'clear the rounding byte', align=Align.INLINE)
d.comment(0xa682, 'no overflow: done', align=Align.INLINE)

# stmt_until (&BBB1) remaining
d.comment(0xbbb4, 'Check for end of statement', align=Align.INLINE)
d.comment(0xbbb7, 'coerce the condition to an integer', align=Align.INLINE)
d.comment(0xbbbc, 'UNTIL with no REPEAT: error', align=Align.INLINE)
d.comment(0xbbbe, 'Test the condition for true (non-zero):', align=Align.INLINE)
d.comment(0xbbc0, '...', align=Align.INLINE)
d.comment(0xbbc2, '...', align=Align.INLINE)
d.comment(0xbbc4, '...', align=Align.INLINE)
d.comment(0xbbca, 'true: exit the loop, continue', align=Align.INLINE)
d.comment(0xbbd0, 'Reload the loop position: high', align=Align.INLINE)
d.comment(0xbbd3, 'jump back to the REPEAT', align=Align.INLINE)
d.comment(0xbbd6, 'BRK error block: too many REPEATs', align=Align.INLINE)

# eval_channel (&BFB5) remaining
d.comment(0xbfb5, 'Skip spaces', align=Align.INLINE)
d.comment(0xbfb8, 'Require "#"', align=Align.INLINE)
d.comment(0xbfba, 'missing: error', align=Align.INLINE)
d.comment(0xbfbc, 'Evaluate the handle as an integer', align=Align.INLINE)
d.comment(0xbfbf, 'Y = the handle', align=Align.INLINE)
d.comment(0xbfc1, 'A = the handle too', align=Align.INLINE)
d.comment(0xbfc2, 'Return', align=Align.INLINE)
d.comment(0xbfc3, 'BRK error block ("Missing #")', align=Align.INLINE)

# stmt_close (&BF99) + sub_cbfa9 (set PtrB = PtrA)
d.comment(0xbf99, 'Evaluate the #handle', align=Align.INLINE)
d.comment(0xbf9c, 'Check for end of statement', align=Align.INLINE)
d.comment(0xbf9f, 'Y = the handle', align=Align.INLINE)
d.comment(0xbfa1, 'OSFIND &00: close the file', align=Align.INLINE)
d.comment(0xbfa6, 'Back to execution', align=Align.INLINE)
d.comment(0xbfa9, 'Set PtrB = PtrA: offset', align=Align.INLINE)
d.comment(0xbfab, '...', align=Align.INLINE)
d.comment(0xbfad, 'low', align=Align.INLINE)
d.comment(0xbfaf, '...', align=Align.INLINE)
d.comment(0xbfb1, 'high', align=Align.INLINE)
d.comment(0xbfb3, '...', align=Align.INLINE)

# stmt_oscli (&BEC2) + sub_cbed2 / sub_cbedd / sub_cbee7
d.comment(0xbec2, 'Evaluate the command string, CR-terminate it', align=Align.INLINE)
d.comment(0xbec5, 'XY -> the string (&0600): low', align=Align.INLINE)
d.comment(0xbec7, 'high byte &06', align=Align.INLINE)
d.comment(0xbec9, 'Pass it to OSCLI', align=Align.INLINE)
d.comment(0xbecc, 'Back to execution', align=Align.INLINE)
d.comment(0xbecf, 'not a string: Type mismatch', align=Align.INLINE)
d.comment(0xbed2, 'Evaluate the expression', align=Align.INLINE)
d.comment(0xbed5, 'not a string: error', align=Align.INLINE)
d.comment(0xbed7, 'CR-terminate the string buffer', align=Align.INLINE)
d.comment(0xbeda, 'Check for end of statement', align=Align.INLINE)
d.comment(0xbedd, 'Evaluate the filename, CR-terminate', align=Align.INLINE)
d.comment(0xbee0, '...', align=Align.INLINE)
d.comment(0xbee1, 'LOAD address low = 0', align=Align.INLINE)
d.comment(0xbee3, 'LOAD address high = PAGE', align=Align.INLINE)
d.comment(0xbee5, '(store)', align=Align.INLINE)
d.comment(0xbee7, 'OSBYTE &82: read the high-order address', align=Align.INLINE)
d.comment(0xbeec, 'set the LOAD high word', align=Align.INLINE)
d.comment(0xbeee, '...', align=Align.INLINE)
d.comment(0xbef0, '...', align=Align.INLINE)
d.comment(0xbef2, 'Return', align=Align.INLINE)

# iwa_negate (&AD93): IWA = -IWA
d.comment(0xad93, 'Negate IWA: compute 0 - IWA', align=Align.INLINE)
d.comment(0xad94, '...', align=Align.INLINE)
d.comment(0xad96, 'Y = 0 for the subtractions', align=Align.INLINE)
d.comment(0xad97, 'byte 0', align=Align.INLINE)
d.comment(0xad99, '(store)', align=Align.INLINE)
d.comment(0xad9b, '0...', align=Align.INLINE)
d.comment(0xad9c, 'byte 1', align=Align.INLINE)
d.comment(0xad9e, '(store)', align=Align.INLINE)
d.comment(0xada0, '0...', align=Align.INLINE)
d.comment(0xada1, 'byte 2', align=Align.INLINE)
d.comment(0xada3, '(store)', align=Align.INLINE)
d.comment(0xada5, '0...', align=Align.INLINE)
d.comment(0xada6, 'byte 3', align=Align.INLINE)
d.comment(0xada8, '(store)', align=Align.INLINE)
d.comment(0xadaa, 'integer result', align=Align.INLINE)
d.comment(0xadac, 'Return -IWA', align=Align.INLINE)
d.comment(0xadad, 'Read a string literal: skip spaces', align=Align.INLINE)
d.comment(0xadb0, 'a quote?', align=Align.INLINE)
d.comment(0xadb2, 'quoted string', align=Align.INLINE)
d.comment(0xadb4, 'Unquoted: read until CR or comma', align=Align.INLINE)
d.comment(0xadb6, 'char', align=Align.INLINE)
d.comment(0xadb8, 'into the buffer', align=Align.INLINE)
d.comment(0xadbb, 'next', align=Align.INLINE)
d.comment(0xadbc, '...', align=Align.INLINE)
d.comment(0xadbd, 'CR?', align=Align.INLINE)
d.comment(0xadbf, 'end', align=Align.INLINE)
d.comment(0xadc1, 'comma?', align=Align.INLINE)
d.comment(0xadc3, 'loop', align=Align.INLINE)
d.comment(0xadc5, 'step back', align=Align.INLINE)
d.comment(0xadc6, 'finish', align=Align.INLINE)
d.comment(0xadc9, 'Quoted: read until the closing quote', align=Align.INLINE)
d.comment(0xadcb, 'advance', align=Align.INLINE)
d.comment(0xadcc, 'char', align=Align.INLINE)
d.comment(0xadce, 'CR (unterminated)?', align=Align.INLINE)
d.comment(0xadd0, 'Missing " error', align=Align.INLINE)
d.comment(0xadd2, 'next', align=Align.INLINE)
d.comment(0xadd3, 'into the buffer', align=Align.INLINE)
d.comment(0xadd6, '...', align=Align.INLINE)
d.comment(0xadd7, 'a quote?', align=Align.INLINE)
d.comment(0xadd9, 'no: keep copying', align=Align.INLINE)
d.comment(0xaddb, 'doubled "" = a literal quote?', align=Align.INLINE)
d.comment(0xaddd, '...', align=Align.INLINE)
d.comment(0xaddf, 'yes: keep it', align=Align.INLINE)
d.comment(0xade1, 'drop the trailing character', align=Align.INLINE)
d.comment(0xade2, 'set the string length', align=Align.INLINE)
d.comment(0xade4, 'update the text offset', align=Align.INLINE)
d.comment(0xade6, 'string type', align=Align.INLINE)
d.comment(0xade8, 'Return the string', align=Align.INLINE)
d.comment(0xade9, 'Missing " error', align=Align.INLINE)

d.comment(0xa50b, 'Is FWA zero?', align=Align.INLINE)
d.subroutine(0xa197, 'mant_mul10', title='Multiply the FWA mantissa by 10',
             description='Mantissa-only x10 (x4 + x1, then x2) used by the number<->ASCII conversions.')

d.subroutine(0xa7e9, 'point_fp_temp4', title='Point zp_fp_ptr at FP TEMP4 (&047B)')
d.subroutine(0xa7ed, 'point_fp_temp2', title='Point zp_fp_ptr at FP TEMP2 (&0471)')
d.subroutine(0xa7f1, 'point_fp_temp3', title='Point zp_fp_ptr at FP TEMP3 (&0476)')
d.subroutine(0xa7f5, 'point_fp_temp1', title='Point zp_fp_ptr at FP TEMP1 (&046C)')

d.subroutine(0xa040, 'output_top_digit', title='Output the leading decimal digit of FWA',
             description='Emit the integer part of the FWA mantissa as a digit, then multiply the remaining fraction by 10.')
d.subroutine(0xa052, 'output_byte_decimal', title='Output a byte (0-99) in decimal')
d.subroutine(0xa064, 'output_digit', title='Output A as a decimal digit (A + "0")')
d.subroutine(0xa066, 'output_char', title='Append a character to the output string')

# number_to_ascii (&9EDF): format the value into the SWA per @% / radix
d.comment(0x9edf, 'Get the @% format byte', align=Align.INLINE)
d.comment(0x9ee2, 'valid (< 3)?', align=Align.INLINE)
d.comment(0x9ee4, 'yes: use it', align=Align.INLINE)
d.comment(0x9ee6, 'invalid: use General format', align=Align.INLINE)
d.comment(0x9ee8, 'store the format type', align=Align.INLINE)
d.comment(0x9eea, 'digit count from @%', align=Align.INLINE)
d.comment(0x9eed, 'zero: check the format', align=Align.INLINE)
d.comment(0x9eef, '>= 10 digits?', align=Align.INLINE)
d.comment(0x9ef1, 'yes: cap at 10', align=Align.INLINE)
d.comment(0x9ef3, 'use the specified count', align=Align.INLINE)
d.comment(0x9ef5, 'fixed format?', align=Align.INLINE)
d.comment(0x9ef7, 'yes: zero digits', align=Align.INLINE)
d.comment(0x9ef9, 'default to 10 digits', align=Align.INLINE)
d.comment(0x9efb, 'store the digit count', align=Align.INLINE)
d.comment(0x9efd, '(copy)', align=Align.INLINE)
d.comment(0x9eff, 'output length = 0...', align=Align.INLINE)
d.comment(0x9f01, '...', align=Align.INLINE)
d.comment(0x9f03, 'decimal exponent = 0 (&49)', align=Align.INLINE)
d.comment(0x9f05, 'hex mode (radix flag bit 7)?', align=Align.INLINE)
d.comment(0x9f07, 'yes: hex conversion', align=Align.INLINE)
d.comment(0x9f09, 'an integer value?', align=Align.INLINE)
d.comment(0x9f0a, 'already a real', align=Align.INLINE)
d.comment(0x9f0c, 'convert the integer to a real', align=Align.INLINE)
d.comment(0x9f0f, 'sign of the value', align=Align.INLINE)
d.comment(0x9f12, 'non-zero: format it', align=Align.INLINE)
d.comment(0x9f14, 'zero, not General format?', align=Align.INLINE)
d.comment(0x9f16, 'fixed/exponential zero', align=Align.INLINE)
d.comment(0x9f18, "output a single '0'", align=Align.INLINE)
d.comment(0x9f1a, '...and return', align=Align.INLINE)
d.comment(0x9f1d, 'output zero in fixed/exp format', align=Align.INLINE)
d.comment(0x9f20, 'FWA = 1.0', align=Align.INLINE)
d.comment(0x9f23, '...', align=Align.INLINE)
d.comment(0x9f25, 'exponent < 4 (value < 10)?', align=Align.INLINE)
d.comment(0x9f27, 'yes: ready to convert', align=Align.INLINE)
d.comment(0x9f29, 'exponent != 4: too big, divide', align=Align.INLINE)
d.comment(0x9f2b, 'mantissa top byte', align=Align.INLINE)
d.comment(0x9f2d, 'less than &A0 (value < 10)?', align=Align.INLINE)
d.comment(0x9f2f, 'yes: ready to convert', align=Align.INLINE)
d.comment(0x9f31, 'FWA = FWA / 10', align=Align.INLINE)
d.comment(0x9f34, 'count one decimal place up', align=Align.INLINE)
d.comment(0x9f36, 'check the magnitude again', align=Align.INLINE)
d.comment(0x9f39, 'Save FWA in TEMP1 (a fraction in [1,10)):', align=Align.INLINE)
d.comment(0x9f3b, '...', align=Align.INLINE)
d.comment(0x9f3d, '...', align=Align.INLINE)
d.comment(0x9f40, 'digit count', align=Align.INLINE)
d.comment(0x9f42, '...', align=Align.INLINE)
d.comment(0x9f44, 'print format', align=Align.INLINE)
d.comment(0x9f46, 'not fixed format?', align=Align.INLINE)
d.comment(0x9f48, 'do exponent/general', align=Align.INLINE)
d.comment(0x9f4a, 'fixed: digits + decimal exponent', align=Align.INLINE)
d.comment(0x9f4c, 'negative: round to zero', align=Align.INLINE)
d.comment(0x9f4e, '...', align=Align.INLINE)
d.comment(0x9f50, '> 10?', align=Align.INLINE)
d.comment(0x9f52, 'no', align=Align.INLINE)
d.comment(0x9f54, 'cap at 10', align=Align.INLINE)
d.comment(0x9f56, '...', align=Align.INLINE)
d.comment(0x9f58, 'switch to General', align=Align.INLINE)
d.comment(0x9f5a, '...', align=Align.INLINE)
d.comment(0x9f5c, 'Build a rounding constant 0.5e-n:', align=Align.INLINE)
d.comment(0x9f5f, '...', align=Align.INLINE)
d.comment(0x9f61, '...', align=Align.INLINE)
d.comment(0x9f63, '...', align=Align.INLINE)
d.comment(0x9f65, '...', align=Align.INLINE)
d.comment(0x9f67, 'shift it down by the digit count:', align=Align.INLINE)
d.comment(0x9f69, '...', align=Align.INLINE)
d.comment(0x9f6b, 'rounding /= 10', align=Align.INLINE)
d.comment(0x9f6e, 'count', align=Align.INLINE)
d.comment(0x9f6f, 'loop', align=Align.INLINE)
d.comment(0x9f71, 'point at the saved value (TEMP1)', align=Align.INLINE)
d.comment(0x9f74, 'FWB = the value', align=Align.INLINE)
d.comment(0x9f77, '...', align=Align.INLINE)
d.comment(0x9f79, '...', align=Align.INLINE)
d.comment(0x9f7b, 'add the rounding constant', align=Align.INLINE)
d.comment(0x9f7e, 'Re-normalise to [1,10): exponent', align=Align.INLINE)
d.comment(0x9f80, '< 4?', align=Align.INLINE)
d.comment(0x9f82, 'in range', align=Align.INLINE)
d.comment(0x9f84, 'shift the mantissa right:', align=Align.INLINE)
d.comment(0x9f86, '...', align=Align.INLINE)
d.comment(0x9f88, '...', align=Align.INLINE)
d.comment(0x9f8a, '...', align=Align.INLINE)
d.comment(0x9f8c, '...', align=Align.INLINE)
d.comment(0x9f8e, 'and bump the exponent', align=Align.INLINE)
d.comment(0x9f90, 'loop', align=Align.INLINE)
d.comment(0x9f92, 'mantissa top byte', align=Align.INLINE)
d.comment(0x9f94, '>= 10 after rounding?', align=Align.INLINE)
d.comment(0x9f96, 'yes: re-divide', align=Align.INLINE)
d.comment(0x9f98, 'digit count', align=Align.INLINE)
d.comment(0x9f9a, 'non-zero', align=Align.INLINE)
d.comment(0x9f9c, 'fixed format?', align=Align.INLINE)
d.comment(0x9f9e, 'output the value', align=Align.INLINE)
d.comment(0x9fa0, 'Clear FWA (zero / underflow):', align=Align.INLINE)
d.comment(0x9fa3, '...', align=Align.INLINE)
d.comment(0x9fa5, '...', align=Align.INLINE)
d.comment(0x9fa7, '...', align=Align.INLINE)
d.comment(0x9fa9, '...', align=Align.INLINE)
d.comment(0x9fab, '...', align=Align.INLINE)
d.comment(0x9fad, 'General format?', align=Align.INLINE)
d.comment(0x9faf, '...', align=Align.INLINE)
d.comment(0x9fb1, 'output the value', align=Align.INLINE)
d.comment(0x9fb3, 'decimal exponent', align=Align.INLINE)
d.comment(0x9fb5, 'negative: leading zeros', align=Align.INLINE)
d.comment(0x9fb7, 'within the digit count?', align=Align.INLINE)
d.comment(0x9fb9, 'no: use E-notation', align=Align.INLINE)
d.comment(0x9fbb, '...', align=Align.INLINE)
d.comment(0x9fbd, '...', align=Align.INLINE)
d.comment(0x9fbf, '...', align=Align.INLINE)
d.comment(0x9fc1, 'output the value', align=Align.INLINE)
d.comment(0x9fc3, 'fixed format?', align=Align.INLINE)
d.comment(0x9fc5, '...', align=Align.INLINE)
d.comment(0x9fc7, '...', align=Align.INLINE)
d.comment(0x9fc9, '...', align=Align.INLINE)
d.comment(0x9fcb, 'far below: use E-notation', align=Align.INLINE)
d.comment(0x9fcd, '...', align=Align.INLINE)
d.comment(0x9fcf, "leading '0'", align=Align.INLINE)
d.comment(0x9fd1, '...', align=Align.INLINE)
d.comment(0x9fd4, "decimal '.'", align=Align.INLINE)
d.comment(0x9fd6, '...', align=Align.INLINE)
d.comment(0x9fd9, "prepare '0'", align=Align.INLINE)
d.comment(0x9fdb, 'leading zeros for the fraction:', align=Align.INLINE)
d.comment(0x9fdd, '...', align=Align.INLINE)
d.comment(0x9fdf, 'output a zero', align=Align.INLINE)
d.comment(0x9fe2, 'loop', align=Align.INLINE)
d.comment(0x9fe4, '...', align=Align.INLINE)
d.comment(0x9fe6, 'digit position counter', align=Align.INLINE)
d.comment(0x9fe8, 'Emit each digit:', align=Align.INLINE)
d.comment(0x9feb, 'at the decimal point?', align=Align.INLINE)
d.comment(0x9fed, 'no', align=Align.INLINE)
d.comment(0x9fef, "emit '.'", align=Align.INLINE)
d.comment(0x9ff1, '...', align=Align.INLINE)
d.comment(0x9ff4, 'more digits?', align=Align.INLINE)
d.comment(0x9ff6, 'loop', align=Align.INLINE)
d.comment(0x9ff8, 'General format: trim trailing zeros', align=Align.INLINE)
d.comment(0x9ffa, '...', align=Align.INLINE)
d.comment(0x9ffb, '...', align=Align.INLINE)
d.comment(0x9ffd, '...', align=Align.INLINE)
d.comment(0x9ffe, '...', align=Align.INLINE)
d.comment(0xa000, 'scan back from the end:', align=Align.INLINE)
d.comment(0xa002, '...', align=Align.INLINE)
d.comment(0xa003, 'a character', align=Align.INLINE)
d.comment(0xa006, "a '0'?", align=Align.INLINE)
d.comment(0xa008, 'yes: trim it', align=Align.INLINE)
d.comment(0xa00a, "a '.'?", align=Align.INLINE)
d.comment(0xa00c, 'trim it too', align=Align.INLINE)
d.comment(0xa00e, 'keep this one', align=Align.INLINE)
d.comment(0xa00f, 'set the trimmed length', align=Align.INLINE)
d.comment(0xa011, 'a decimal exponent to print?', align=Align.INLINE)
d.comment(0xa013, 'no: done', align=Align.INLINE)
d.comment(0xa015, "output 'E'", align=Align.INLINE)
d.comment(0xa017, '...', align=Align.INLINE)
d.comment(0xa01a, 'the exponent', align=Align.INLINE)
d.comment(0xa01c, 'positive', align=Align.INLINE)
d.comment(0xa01e, "negative: output '-'", align=Align.INLINE)
d.comment(0xa020, '...', align=Align.INLINE)
d.comment(0xa023, 'negate the exponent', align=Align.INLINE)
d.comment(0xa024, '...', align=Align.INLINE)
d.comment(0xa026, '...', align=Align.INLINE)
d.comment(0xa028, 'output the exponent in decimal', align=Align.INLINE)
d.comment(0xa02b, 'General format?', align=Align.INLINE)
d.comment(0xa02d, 'done', align=Align.INLINE)
d.comment(0xa02f, "pad: a space", align=Align.INLINE)
d.comment(0xa031, '...', align=Align.INLINE)
d.comment(0xa033, '...', align=Align.INLINE)
d.comment(0xa035, 'output it', align=Align.INLINE)
d.comment(0xa038, '...', align=Align.INLINE)
d.comment(0xa03a, 'done', align=Align.INLINE)
d.comment(0xa03c, 'output a final space', align=Align.INLINE)
d.comment(0xa03f, 'Return', align=Align.INLINE)
# output_top_digit (&A040)
d.comment(0xa040, 'Integer part: top nibble', align=Align.INLINE)
d.comment(0xa042, '...', align=Align.INLINE)
d.comment(0xa043, '...', align=Align.INLINE)
d.comment(0xa044, '...', align=Align.INLINE)
d.comment(0xa045, '...', align=Align.INLINE)
d.comment(0xa046, 'output it as a digit', align=Align.INLINE)
d.comment(0xa049, 'mask off the integer part:', align=Align.INLINE)
d.comment(0xa04b, '...', align=Align.INLINE)
d.comment(0xa04d, '...', align=Align.INLINE)
d.comment(0xa04f, 'multiply the fraction by 10', align=Align.INLINE)
# output_byte_decimal (&A052)
d.comment(0xa052, 'count the tens:', align=Align.INLINE)
d.comment(0xa054, '...', align=Align.INLINE)
d.comment(0xa055, 'subtract 10...', align=Align.INLINE)
d.comment(0xa056, '...', align=Align.INLINE)
d.comment(0xa058, 'until it goes negative', align=Align.INLINE)
d.comment(0xa05a, 'add 10 back (the units)', align=Align.INLINE)
d.comment(0xa05c, 'save the units', align=Align.INLINE)
d.comment(0xa05d, 'the tens digit', align=Align.INLINE)
d.comment(0xa05e, 'no tens: skip', align=Align.INLINE)
d.comment(0xa060, 'output the tens digit', align=Align.INLINE)
d.comment(0xa063, 'units digit', align=Align.INLINE)
d.comment(0xa064, 'make it a digit ("0" + A)', align=Align.INLINE)
# output_char (&A066)
d.comment(0xa066, 'save X', align=Align.INLINE)
d.comment(0xa068, 'append at the end of the buffer', align=Align.INLINE)
d.comment(0xa06a, '...', align=Align.INLINE)
d.comment(0xa06d, 'restore X', align=Align.INLINE)
d.comment(0xa06f, 'one longer', align=Align.INLINE)
d.comment(0xa071, 'Return', align=Align.INLINE)
d.comment(0xa072, 'set the rounding byte and test the sign', align=Align.INLINE)
d.comment(0xa073, '...', align=Align.INLINE)
d.comment(0xa075, '...', align=Align.INLINE)
d.comment(0xa078, 'real result', align=Align.INLINE)
d.comment(0xa07a, 'Return', align=Align.INLINE)

d.subroutine(0xb112, 'find_def', title='Find a PROC/FN definition by name',
             description='Search the program for the DEF line whose name matches, then cache its body address in the variable entry.')

# fn_strings (&B0C2): STRING$(n, s$) - n copies of s$
d.comment(0xb0c2, 'Evaluate the count (n) as an integer', align=Align.INLINE)
d.comment(0xb0c5, 'stack it', align=Align.INLINE)
d.comment(0xb0c8, 'require a comma', align=Align.INLINE)
d.comment(0xb0cb, 'evaluate the string s$', align=Align.INLINE)
d.comment(0xb0ce, 'not a string: Type mismatch', align=Align.INLINE)
d.comment(0xb0d0, 'recover the count', align=Align.INLINE)
d.comment(0xb0d3, 'source string length', align=Align.INLINE)
d.comment(0xb0d5, 'empty source: empty result', align=Align.INLINE)
d.comment(0xb0d7, 'count = 0?', align=Align.INLINE)
d.comment(0xb0d9, 'yes: empty result', align=Align.INLINE)
d.comment(0xb0db, 'one copy is already there; need count-1 more', align=Align.INLINE)
d.comment(0xb0dd, 'count = 1: done', align=Align.INLINE)
d.comment(0xb0df, 'Append another copy:', align=Align.INLINE)
d.comment(0xb0e1, 'source char...', align=Align.INLINE)
d.comment(0xb0e4, '...appended', align=Align.INLINE)
d.comment(0xb0e7, 'next source', align=Align.INLINE)
d.comment(0xb0e8, 'next dest', align=Align.INLINE)
d.comment(0xb0e9, 'too long: error', align=Align.INLINE)
d.comment(0xb0eb, 'end of this copy?', align=Align.INLINE)
d.comment(0xb0ed, 'no: keep copying', align=Align.INLINE)
d.comment(0xb0ef, 'one fewer copy', align=Align.INLINE)
d.comment(0xb0f1, 'loop', align=Align.INLINE)
d.comment(0xb0f3, 'set the result length', align=Align.INLINE)
d.comment(0xb0f5, 'string type', align=Align.INLINE)
d.comment(0xb0f7, 'Return', align=Align.INLINE)
d.comment(0xb0f8, 'empty result (length 0)', align=Align.INLINE)
d.comment(0xb0fa, 'Return', align=Align.INLINE)
d.comment(0xb0fb, 'String too long error', align=Align.INLINE)
# find_def (&B112) and the "No such FN/PROC" path
d.comment(0xb0fe, 'No such FN/PROC: restore the text pointer', align=Align.INLINE)
d.comment(0xb0ff, '...', align=Align.INLINE)
d.comment(0xb101, '...', align=Align.INLINE)
d.comment(0xb102, '...', align=Align.INLINE)
d.comment(0xb104, '"No such FN/PROC" error block', align=Align.INLINE)
d.comment(0xb112, 'Search from PAGE: high', align=Align.INLINE)
d.comment(0xb114, '...', align=Align.INLINE)
d.comment(0xb116, 'low 0', align=Align.INLINE)
d.comment(0xb118, '...', align=Align.INLINE)
d.comment(0xb11a, 'line number high byte', align=Align.INLINE)
d.comment(0xb11c, '...', align=Align.INLINE)
d.comment(0xb11e, 'end of program: not found', align=Align.INLINE)
d.comment(0xb120, 'skip to the line body', align=Align.INLINE)
d.comment(0xb122, 'advance', align=Align.INLINE)
d.comment(0xb123, 'char', align=Align.INLINE)
d.comment(0xb125, 'skip leading spaces', align=Align.INLINE)
d.comment(0xb127, '...', align=Align.INLINE)
d.comment(0xb129, 'DEF token at the start?', align=Align.INLINE)
d.comment(0xb12b, 'yes: check the name', align=Align.INLINE)
d.comment(0xb12d, 'no DEF: skip to the next line', align=Align.INLINE)
d.comment(0xb12f, 'line length', align=Align.INLINE)
d.comment(0xb131, '...', align=Align.INLINE)
d.comment(0xb132, '...', align=Align.INLINE)
d.comment(0xb134, '...', align=Align.INLINE)
d.comment(0xb136, '...', align=Align.INLINE)
d.comment(0xb138, '...', align=Align.INLINE)
d.comment(0xb13a, 'next line', align=Align.INLINE)
d.comment(0xb13c, 'DEF found: skip past the FN/PROC token', align=Align.INLINE)
d.comment(0xb13d, '...', align=Align.INLINE)
d.comment(0xb13f, 'skip spaces', align=Align.INLINE)
d.comment(0xb142, 'point at the definition name:', align=Align.INLINE)
d.comment(0xb143, '...', align=Align.INLINE)
d.comment(0xb144, '...', align=Align.INLINE)
d.comment(0xb145, '...', align=Align.INLINE)
d.comment(0xb147, '...', align=Align.INLINE)
d.comment(0xb149, '...', align=Align.INLINE)
d.comment(0xb14b, '...', align=Align.INLINE)
d.comment(0xb14c, '...', align=Align.INLINE)
d.comment(0xb14d, '...', align=Align.INLINE)
d.comment(0xb14f, '(save pointer low)', align=Align.INLINE)
d.comment(0xb151, '...', align=Align.INLINE)
d.comment(0xb152, '...', align=Align.INLINE)
d.comment(0xb154, '(save pointer high)', align=Align.INLINE)
d.comment(0xb156, 'Compare the definition name with the called name:', align=Align.INLINE)
d.comment(0xb158, '...', align=Align.INLINE)
d.comment(0xb159, '...', align=Align.INLINE)
d.comment(0xb15a, 'definition char', align=Align.INLINE)
d.comment(0xb15c, 'vs called char', align=Align.INLINE)
d.comment(0xb15e, 'differ: next line', align=Align.INLINE)
d.comment(0xb160, 'end of the called name?', align=Align.INLINE)
d.comment(0xb162, 'no: keep comparing', align=Align.INLINE)
d.comment(0xb164, 'definition name also ends?', align=Align.INLINE)
d.comment(0xb165, '...', align=Align.INLINE)
d.comment(0xb167, 'alphanumeric?', align=Align.INLINE)
d.comment(0xb16a, 'definition name is longer: next line', align=Align.INLINE)
d.comment(0xb16c, 'Match: cache the definition', align=Align.INLINE)
d.comment(0xb16d, '...', align=Align.INLINE)
d.comment(0xb16e, 'point PtrA at the body', align=Align.INLINE)
d.comment(0xb171, 'create/find the FN/PROC entry', align=Align.INLINE)
d.comment(0xb174, 'init it', align=Align.INLINE)
d.comment(0xb176, '...', align=Align.INLINE)
d.comment(0xb179, 'store the body pointer:', align=Align.INLINE)
d.comment(0xb17b, '...', align=Align.INLINE)
d.comment(0xb17d, '...', align=Align.INLINE)
d.comment(0xb17f, '...', align=Align.INLINE)
d.comment(0xb180, '...', align=Align.INLINE)
d.comment(0xb182, '...', align=Align.INLINE)
d.comment(0xb184, 'advance VARTOP', align=Align.INLINE)
d.comment(0xb187, 'continue', align=Align.INLINE)
d.comment(0xb18a, 'error block', align=Align.INLINE)

# stmt_next (&B695) remaining: update the control variable, test the limit
d.comment(0xb698, 'a variable named after NEXT?', align=Align.INLINE)
d.comment(0xb69a, 'innermost FOR frame', align=Align.INLINE)
d.comment(0xb69c, 'no FOR active: error', align=Align.INLINE)
d.comment(0xb69e, 'no variable: use the innermost loop', align=Align.INLINE)
d.comment(0xb6a0, 'not a variable: error', align=Align.INLINE)
d.comment(0xb6a3, '...', align=Align.INLINE)
d.comment(0xb6a5, 'Search the FOR stack for the named variable:', align=Align.INLINE)
d.comment(0xb6a7, 'not found: error', align=Align.INLINE)
d.comment(0xb6ab, 'match the variable address low?', align=Align.INLINE)
d.comment(0xb6ae, 'no: next frame', align=Align.INLINE)
d.comment(0xb6b0, 'address high', align=Align.INLINE)
d.comment(0xb6b2, '...', align=Align.INLINE)
d.comment(0xb6b5, 'no: next frame', align=Align.INLINE)
d.comment(0xb6b7, 'type', align=Align.INLINE)
d.comment(0xb6b9, '...', align=Align.INLINE)
d.comment(0xb6bc, 'match: this loop', align=Align.INLINE)
d.comment(0xb6bf, 'step out one frame (15 bytes)', align=Align.INLINE)
d.comment(0xb6c0, '...', align=Align.INLINE)
d.comment(0xb6c2, '...', align=Align.INLINE)
d.comment(0xb6c3, '...', align=Align.INLINE)
d.comment(0xb6c5, 'keep searching', align=Align.INLINE)
d.comment(0xb6c7, 'No FOR error block', align=Align.INLINE)
d.comment(0xb6da, 'control variable address: low', align=Align.INLINE)
d.comment(0xb6dc, 'high', align=Align.INLINE)
d.comment(0xb6df, '...', align=Align.INLINE)
d.comment(0xb6e1, 'type', align=Align.INLINE)
d.comment(0xb6e4, 'a real (float) loop?', align=Align.INLINE)
d.comment(0xb6e6, 'yes: float NEXT', align=Align.INLINE)
d.comment(0xb6e8, 'Integer: add STEP to the variable:', align=Align.INLINE)
d.comment(0xb6ea, 'byte 0', align=Align.INLINE)
d.comment(0xb6ec, '+ step byte 0', align=Align.INLINE)
d.comment(0xb6ef, '(store)', align=Align.INLINE)
d.comment(0xb6f1, '(keep)', align=Align.INLINE)
d.comment(0xb6f3, 'byte 1', align=Align.INLINE)
d.comment(0xb6f4, '...', align=Align.INLINE)
d.comment(0xb6f6, '+ step byte 1', align=Align.INLINE)
d.comment(0xb6f9, '(store)', align=Align.INLINE)
d.comment(0xb6fb, '(keep)', align=Align.INLINE)
d.comment(0xb6fd, 'byte 2', align=Align.INLINE)
d.comment(0xb6fe, '...', align=Align.INLINE)
d.comment(0xb700, '+ step byte 2', align=Align.INLINE)
d.comment(0xb703, '(store)', align=Align.INLINE)
d.comment(0xb705, '(keep)', align=Align.INLINE)
d.comment(0xb707, 'byte 3', align=Align.INLINE)
d.comment(0xb708, '...', align=Align.INLINE)
d.comment(0xb70a, '+ step byte 3', align=Align.INLINE)
d.comment(0xb70d, '(store)', align=Align.INLINE)
d.comment(0xb70f, '(keep)', align=Align.INLINE)
d.comment(0xb710, 'Compare the new value with LIMIT:', align=Align.INLINE)
d.comment(0xb712, '...', align=Align.INLINE)
d.comment(0xb713, 'value - limit: byte 0', align=Align.INLINE)
d.comment(0xb716, '(keep)', align=Align.INLINE)
d.comment(0xb718, 'byte 1', align=Align.INLINE)
d.comment(0xb71a, '...', align=Align.INLINE)
d.comment(0xb71d, '(keep)', align=Align.INLINE)
d.comment(0xb71f, 'byte 2', align=Align.INLINE)
d.comment(0xb721, '...', align=Align.INLINE)
d.comment(0xb724, '(keep)', align=Align.INLINE)
d.comment(0xb726, 'byte 3', align=Align.INLINE)
d.comment(0xb727, '...', align=Align.INLINE)
d.comment(0xb72a, 'exactly equal to the limit?', align=Align.INLINE)
d.comment(0xb72c, '...', align=Align.INLINE)
d.comment(0xb72e, '...', align=Align.INLINE)
d.comment(0xb730, 'at the limit: last iteration, continue', align=Align.INLINE)
d.comment(0xb732, 'Past the limit? (sign of step vs difference)', align=Align.INLINE)
d.comment(0xb733, '...', align=Align.INLINE)
d.comment(0xb736, '...', align=Align.INLINE)
d.comment(0xb739, '...', align=Align.INLINE)
d.comment(0xb73b, 'within range: continue', align=Align.INLINE)
d.comment(0xb73d, 'past: exit the loop', align=Align.INLINE)
d.comment(0xb73f, 'past: exit the loop', align=Align.INLINE)
d.comment(0xb741, 'Continue: reload the loop-back position:', align=Align.INLINE)
d.comment(0xb744, '...', align=Align.INLINE)
d.comment(0xb747, '(text pointer)', align=Align.INLINE)
d.comment(0xb749, '...', align=Align.INLINE)
d.comment(0xb74b, 'restore the offset', align=Align.INLINE)
d.comment(0xb74e, 'jump back to the loop body', align=Align.INLINE)
d.comment(0xb751, 'Exit: pop the FOR frame:', align=Align.INLINE)
d.comment(0xb753, '...', align=Align.INLINE)
d.comment(0xb754, '...', align=Align.INLINE)
d.comment(0xb756, '...', align=Align.INLINE)
d.comment(0xb758, 'continue after NEXT:', align=Align.INLINE)
d.comment(0xb75a, '...', align=Align.INLINE)
d.comment(0xb75c, 'another NEXT variable (comma)?', align=Align.INLINE)
d.comment(0xb75f, '...', align=Align.INLINE)
d.comment(0xb761, 'no: end of statement', align=Align.INLINE)
d.comment(0xb763, 'yes: handle the next variable', align=Align.INLINE)
d.comment(0xb766, 'Float loop: load the control variable', align=Align.INLINE)
d.comment(0xb769, 'point at the STEP in the frame:', align=Align.INLINE)
d.comment(0xb76b, '...', align=Align.INLINE)
d.comment(0xb76c, '...', align=Align.INLINE)
d.comment(0xb76e, '...', align=Align.INLINE)
d.comment(0xb770, '...', align=Align.INLINE)
d.comment(0xb772, '...', align=Align.INLINE)
d.comment(0xb774, 'add STEP to the variable', align=Align.INLINE)
d.comment(0xb777, 'store it back:', align=Align.INLINE)
d.comment(0xb779, '...', align=Align.INLINE)
d.comment(0xb77b, '...', align=Align.INLINE)
d.comment(0xb77d, '...', align=Align.INLINE)
d.comment(0xb77f, 'store the updated variable', align=Align.INLINE)
d.comment(0xb782, 'point at the LIMIT:', align=Align.INLINE)
d.comment(0xb784, '...', align=Align.INLINE)
d.comment(0xb786, '...', align=Align.INLINE)
d.comment(0xb787, '...', align=Align.INLINE)
d.comment(0xb789, '...', align=Align.INLINE)
d.comment(0xb78b, '...', align=Align.INLINE)
d.comment(0xb78d, '...', align=Align.INLINE)
d.comment(0xb78f, 'compare the variable with LIMIT', align=Align.INLINE)
d.comment(0xb792, 'at the limit: continue', align=Align.INLINE)
d.comment(0xb794, 'sign of STEP...', align=Align.INLINE)
d.comment(0xb797, '...', align=Align.INLINE)
d.comment(0xb799, 'within range: continue', align=Align.INLINE)
d.comment(0xb79b, 'past: exit', align=Align.INLINE)
d.comment(0xb79d, 'within range: continue', align=Align.INLINE)
d.comment(0xb79f, 'past: exit', align=Align.INLINE)
d.comment(0xb7a1, 'End of statement', align=Align.INLINE)
d.comment(0xb7a4, 'No FOR error block', align=Align.INLINE)
d.comment(0xb7b0, 'error block', align=Align.INLINE)
d.comment(0xb7bd, 'error block', align=Align.INLINE)

# iwa_mul (&9D6D): 32-bit signed integer multiply
d.comment(0x9d6d, 'Save the right operand sign', align=Align.INLINE)
d.comment(0x9d6f, '...', align=Align.INLINE)
d.comment(0x9d70, 'take |right|', align=Align.INLINE)
d.comment(0x9d73, 'save it (via &39)', align=Align.INLINE)
d.comment(0x9d75, '...', align=Align.INLINE)
d.comment(0x9d78, 'unstack the left operand', align=Align.INLINE)
d.comment(0x9d7b, 'recover the right operand sign', align=Align.INLINE)
d.comment(0x9d7c, 'product sign = sign XOR sign', align=Align.INLINE)
d.comment(0x9d7e, '(save it)', align=Align.INLINE)
d.comment(0x9d80, 'take |left|', align=Align.INLINE)
d.comment(0x9d83, 'Clear the running product:', align=Align.INLINE)
d.comment(0x9d85, '...', align=Align.INLINE)
d.comment(0x9d87, '...', align=Align.INLINE)
d.comment(0x9d89, '...', align=Align.INLINE)
d.comment(0x9d8b, 'Shift the multiplier right: next bit', align=Align.INLINE)
d.comment(0x9d8d, '...', align=Align.INLINE)
d.comment(0x9d8f, 'bit clear: skip the add', align=Align.INLINE)
d.comment(0x9d91, 'bit set: add the multiplicand', align=Align.INLINE)
d.comment(0x9d92, 'byte 0', align=Align.INLINE)
d.comment(0x9d93, '...', align=Align.INLINE)
d.comment(0x9d95, '...', align=Align.INLINE)
d.comment(0x9d96, 'byte 1', align=Align.INLINE)
d.comment(0x9d97, '...', align=Align.INLINE)
d.comment(0x9d99, '...', align=Align.INLINE)
d.comment(0x9d9a, 'byte 2', align=Align.INLINE)
d.comment(0x9d9c, '...', align=Align.INLINE)
d.comment(0x9d9e, '...', align=Align.INLINE)
d.comment(0x9da0, 'byte 3', align=Align.INLINE)
d.comment(0x9da2, '...', align=Align.INLINE)
d.comment(0x9da4, '...', align=Align.INLINE)
d.comment(0x9da6, 'Shift the multiplicand left', align=Align.INLINE)
d.comment(0x9da8, '...', align=Align.INLINE)
d.comment(0x9daa, '...', align=Align.INLINE)
d.comment(0x9dac, '...', align=Align.INLINE)
d.comment(0x9dae, 'more multiplier bits?', align=Align.INLINE)
d.comment(0x9db0, '...', align=Align.INLINE)
d.comment(0x9db2, 'loop', align=Align.INLINE)
d.comment(0x9db4, 'store the product (low 2 bytes)', align=Align.INLINE)
d.comment(0x9db6, '...', align=Align.INLINE)
d.comment(0x9db8, 'product sign', align=Align.INLINE)
d.comment(0x9dba, '...', align=Align.INLINE)
d.comment(0x9dbb, 'load the product into IWA', align=Align.INLINE)
d.comment(0x9dbd, '...', align=Align.INLINE)
d.comment(0x9dc0, 'Apply the sign', align=Align.INLINE)
d.comment(0x9dc1, 'positive: done', align=Align.INLINE)
d.comment(0x9dc3, 'negative: negate the product', align=Align.INLINE)
d.comment(0x9dc6, 'restore the operator', align=Align.INLINE)
d.comment(0x9dc8, 'loop for further * / DIV MOD', align=Align.INLINE)
d.comment(0x9dcb, 'bounce back to the multiply code', align=Align.INLINE)
d.comment(0x9dce, 'stack the operand, then multiply', align=Align.INLINE)

# fn_sqr (&A7B4): SQR via Newton's method
d.comment(0xa7b4, 'Evaluate the argument as a real', align=Align.INLINE)
d.comment(0xa7b7, 'Sign of the argument', align=Align.INLINE)
d.comment(0xa7ba, 'zero: the root is zero', align=Align.INLINE)
d.comment(0xa7bc, 'negative: -ve root error', align=Align.INLINE)
d.comment(0xa7be, 'Save the argument in TEMP1', align=Align.INLINE)
d.comment(0xa7c1, 'Initial guess: halve the exponent', align=Align.INLINE)
d.comment(0xa7c3, '...', align=Align.INLINE)
d.comment(0xa7c4, '(re-bias)', align=Align.INLINE)
d.comment(0xa7c6, '...', align=Align.INLINE)
d.comment(0xa7c8, '5 Newton iterations', align=Align.INLINE)
d.comment(0xa7ca, '(counter)', align=Align.INLINE)
d.comment(0xa7cc, 'point at TEMP2 (the guess)', align=Align.INLINE)
d.comment(0xa7cf, 'save the current guess', align=Align.INLINE)
d.comment(0xa7d2, 'point at TEMP1 (the argument)', align=Align.INLINE)
d.comment(0xa7d4, '...', align=Align.INLINE)
d.comment(0xa7d6, 'FWA = argument / guess', align=Align.INLINE)
d.comment(0xa7d9, 'point at TEMP2 (the guess)', align=Align.INLINE)
d.comment(0xa7db, '...', align=Align.INLINE)
d.comment(0xa7dd, 'FWA = arg/guess + guess', align=Align.INLINE)
d.comment(0xa7e0, 'halve it: next guess', align=Align.INLINE)
d.comment(0xa7e2, 'count', align=Align.INLINE)
d.comment(0xa7e4, 'iterate', align=Align.INLINE)
d.comment(0xa7e6, 'real result', align=Align.INLINE)
d.comment(0xa7e8, 'Return the root', align=Align.INLINE)
d.comment(0xa7e9, 'TEMP4 low (&7B)', align=Align.INLINE)
d.comment(0xa7eb, '...', align=Align.INLINE)
d.comment(0xa7ed, 'TEMP2 low (&71)', align=Align.INLINE)
d.comment(0xa7ef, '...', align=Align.INLINE)
d.comment(0xa7f1, 'TEMP3 low (&76)', align=Align.INLINE)
d.comment(0xa7f3, '...', align=Align.INLINE)
d.comment(0xa7f5, 'TEMP1 low (&6C)', align=Align.INLINE)
d.comment(0xa7f7, 'set the pointer low', align=Align.INLINE)
d.comment(0xa7f9, 'high &04', align=Align.INLINE)
d.comment(0xa7fb, '...', align=Align.INLINE)
d.comment(0xa7fd, 'Return', align=Align.INLINE)

# fn_asn (&A8DA): ASN = arcsin, via the arctan relationship
d.comment(0xa8da, 'Evaluate the argument as a real', align=Align.INLINE)
d.comment(0xa8dd, 'Sign of the argument', align=Align.INLINE)
d.comment(0xa8e0, 'positive: compute directly', align=Align.INLINE)
d.comment(0xa8e2, 'negative: take |x|...', align=Align.INLINE)
d.comment(0xa8e4, 'compute asn(|x|)', align=Align.INLINE)
d.comment(0xa8e7, '...and negate the result', align=Align.INLINE)
d.comment(0xa8ea, 'Save x in TEMP3', align=Align.INLINE)
d.comment(0xa8ed, 'compute sqrt(1 - x^2)', align=Align.INLINE)
d.comment(0xa8f0, 'is it zero (x = 1)?', align=Align.INLINE)
d.comment(0xa8f3, 'yes: result is pi/2', align=Align.INLINE)
d.comment(0xa8f5, 'point at x (TEMP3)', align=Align.INLINE)
d.comment(0xa8f8, 'FWA = x / sqrt(1 - x^2)', align=Align.INLINE)
d.comment(0xa8fb, 'asn(x) = atn(that)', align=Align.INLINE)
d.comment(0xa8fe, 'x = 1: load pi/2', align=Align.INLINE)
d.comment(0xa901, '...', align=Align.INLINE)
d.comment(0xa904, 'real result', align=Align.INLINE)
d.comment(0xa906, 'Return', align=Align.INLINE)

# fp_eval_cont_frac (&A897): evaluate the trig continued fraction.
d.comment(0xa897, 'Save the coefficient table pointer (low)', align=Align.INLINE)
d.comment(0xa899, '...and high', align=Align.INLINE)
d.comment(0xa89b, 'Stash the argument in TEMP1', align=Align.INLINE)
d.comment(0xa89e, 'First table byte is the coefficient count', align=Align.INLINE)
d.comment(0xa8a0, '...', align=Align.INLINE)
d.comment(0xa8a2, 'use it as the loop counter', align=Align.INLINE)
d.comment(0xa8a4, 'Advance past the count byte to coefficient 0', align=Align.INLINE)
d.comment(0xa8a6, '...', align=Align.INLINE)
d.comment(0xa8a8, '...', align=Align.INLINE)
d.comment(0xa8aa, 'Point the fp pointer at the first coefficient', align=Align.INLINE)
d.comment(0xa8ac, '...', align=Align.INLINE)
d.comment(0xa8ae, '...', align=Align.INLINE)
d.comment(0xa8b0, '...', align=Align.INLINE)
d.comment(0xa8b2, 'FWA = coefficient 0', align=Align.INLINE)
d.comment(0xa8b5, 'Point at the argument in TEMP1', align=Align.INLINE)
d.comment(0xa8b8, 'FWA = arg / FWA', align=Align.INLINE)
d.comment(0xa8bb, 'Advance the pointer to the next coefficient', align=Align.INLINE)
d.comment(0xa8bc, '...(five bytes per coefficient)', align=Align.INLINE)
d.comment(0xa8be, '...', align=Align.INLINE)
d.comment(0xa8c0, '...', align=Align.INLINE)
d.comment(0xa8c2, '...', align=Align.INLINE)
d.comment(0xa8c4, '...', align=Align.INLINE)
d.comment(0xa8c6, '...', align=Align.INLINE)
d.comment(0xa8c8, '...', align=Align.INLINE)
d.comment(0xa8ca, '...', align=Align.INLINE)
d.comment(0xa8cc, 'FWA = FWA + next coefficient', align=Align.INLINE)
d.comment(0xa8cf, 'One coefficient done', align=Align.INLINE)
d.comment(0xa8d1, 'loop until the table is exhausted', align=Align.INLINE)
d.comment(0xa8d3, 'Return the continued-fraction value', align=Align.INLINE)

# fn_acs (&A8D4): ACS(x) = pi/2 - ASN(x).
d.comment(0xa8d4, 'Compute asn(x)', align=Align.INLINE)
d.comment(0xa8d7, 'Result = pi/2 - asn(x)', align=Align.INLINE)

# fn_atn (&A907): ATN = arctan, result in radians.
d.comment(0xa907, 'Evaluate the argument as a real', align=Align.INLINE)
d.comment(0xa90a, 'Sign of the argument', align=Align.INLINE)
d.comment(0xa90d, 'zero: atn(0) = 0, return it', align=Align.INLINE)
d.comment(0xa90f, 'positive: compute directly', align=Align.INLINE)
d.comment(0xa911, 'negative: clear the sign to take |x|', align=Align.INLINE)
d.comment(0xa913, 'compute atn(|x|)', align=Align.INLINE)
d.comment(0xa916, 'set the result sign negative', align=Align.INLINE)
d.comment(0xa918, '...so atn(-x) = -atn(x)', align=Align.INLINE)
d.comment(0xa91a, 'Return', align=Align.INLINE)
d.comment(0xa91b, 'Exponent of |x|', align=Align.INLINE)
d.comment(0xa91d, '|x| < 1?', align=Align.INLINE)
d.comment(0xa91f, 'yes: evaluate the series directly', align=Align.INLINE)
d.comment(0xa921, '|x| >= 1: FWA = 1 / x', align=Align.INLINE)
d.comment(0xa924, 'atn(1/x) via the series', align=Align.INLINE)
d.comment(0xa927, 'atn(x) = pi/2 - atn(1/x)', align=Align.INLINE)
d.comment(0xa92a, '...', align=Align.INLINE)
d.comment(0xa92d, '...', align=Align.INLINE)
d.comment(0xa930, '...', align=Align.INLINE)
d.comment(0xa933, '...', align=Align.INLINE)
d.comment(0xa936, 'Exponent of the (reduced) argument', align=Align.INLINE)
d.comment(0xa938, 'very small (|x| < 2^-13)?', align=Align.INLINE)
d.comment(0xa93a, 'yes: atn(x) = x to working precision', align=Align.INLINE)
d.comment(0xa93c, 'Save the argument x in TEMP3', align=Align.INLINE)
d.comment(0xa93f, 'Set FWB = 1...', align=Align.INLINE)
d.comment(0xa942, '...', align=Align.INLINE)
d.comment(0xa944, '...', align=Align.INLINE)
d.comment(0xa946, '...', align=Align.INLINE)
d.comment(0xa948, '...', align=Align.INLINE)
d.comment(0xa94a, 'Add it to the argument', align=Align.INLINE)
d.comment(0xa94d, 'Evaluate the arctan continued fraction', align=Align.INLINE)
d.comment(0xa94f, '(coefficients at &A95A)', align=Align.INLINE)
d.comment(0xa951, '...', align=Align.INLINE)
d.comment(0xa954, 'Scale by x (in TEMP3): atn(x) = x * P', align=Align.INLINE)
d.comment(0xa957, 'real result', align=Align.INLINE)
d.comment(0xa959, 'Return', align=Align.INLINE)

# Constant loaders for the two-part pi/2 and the rounded pi/2.
d.comment(0xaa48, 'High part of pi/2: low byte', align=Align.INLINE)
d.comment(0xaa4a, '...(shared tail)', align=Align.INLINE)
d.comment(0xaa4c, 'Low part of pi/2: low byte', align=Align.INLINE)
d.comment(0xaa4e, 'Set the fp pointer low', align=Align.INLINE)
d.comment(0xaa50, 'high &AA', align=Align.INLINE)
d.comment(0xaa52, '...', align=Align.INLINE)
d.comment(0xaa54, 'Return', align=Align.INLINE)
d.comment(0xaa55, 'pi/2 constant: low byte', align=Align.INLINE)
d.comment(0xaa57, '...(shared tail)', align=Align.INLINE)

# fn_rad (&ABB1): RAD(x) = x * pi/180 (degrees -> radians).
d.comment(0xabb1, 'Evaluate the argument as a real', align=Align.INLINE)
d.comment(0xabb4, 'Point at the constant pi/180: low byte', align=Align.INLINE)
d.comment(0xabb6, 'high byte', align=Align.INLINE)
d.comment(0xabb8, 'Set the fp pointer low', align=Align.INLINE)
d.comment(0xabba, '...and high', align=Align.INLINE)
d.comment(0xabbc, 'FWA = x * pi/180', align=Align.INLINE)
d.comment(0xabbf, 'Flag a non-zero real result', align=Align.INLINE)
d.comment(0xabc1, 'Return', align=Align.INLINE)

# fn_sin (&A998) and the shared SIN/COS body.
d.comment(0xa998, 'Evaluate the argument as a real', align=Align.INLINE)
d.comment(0xa99b, 'Range-reduce: leaves the angle in FWA, quadrant in &4A',
          align=Align.INLINE)
d.comment(0xa99e, 'Quadrant', align=Align.INLINE)
d.comment(0xa9a0, 'second or third quadrant (result negative)?',
          align=Align.INLINE)
d.comment(0xa9a2, 'no: compute and return directly', align=Align.INLINE)
d.comment(0xa9a4, 'compute the magnitude...', align=Align.INLINE)
d.comment(0xa9a7, '...then negate it', align=Align.INLINE)
d.comment(0xa9aa, 'Odd quadrant (use cosine instead of sine)?',
          align=Align.INLINE)
d.comment(0xa9ac, 'even: evaluate the sine series', align=Align.INLINE)
d.comment(0xa9ae, 'odd: evaluate the sine series...', align=Align.INLINE)
d.comment(0xa9b1, 'Save sin into TEMP1', align=Align.INLINE)
d.comment(0xa9b4, 'FWA = sin^2', align=Align.INLINE)
d.comment(0xa9b7, '...', align=Align.INLINE)
d.comment(0xa9ba, 'FWA = 1', align=Align.INLINE)
d.comment(0xa9bd, 'FWA = 1 - sin^2', align=Align.INLINE)
d.comment(0xa9c0, 'cos = sqrt(1 - sin^2)', align=Align.INLINE)
d.comment(0xa9c3, 'Save the reduced angle r in TEMP3', align=Align.INLINE)
d.comment(0xa9c6, 'FWA = r^2', align=Align.INLINE)
d.comment(0xa9c9, 'Point at the sine coefficient table: low byte',
          align=Align.INLINE)
d.comment(0xa9cb, '...high', align=Align.INLINE)
d.comment(0xa9cd, 'Evaluate the sine continued fraction in r^2',
          align=Align.INLINE)
d.comment(0xa9d0, 'Scale by r (in TEMP3): sin(r) = r * P', align=Align.INLINE)

# sin_cos_reduce (&A9D3): argument reduction for SIN/COS.
d.comment(0xa9d3, 'Exponent of the argument', align=Align.INLINE)
d.comment(0xa9d5, 'too large to reduce accurately?', align=Align.INLINE)
d.comment(0xa9d7, 'yes: report the error', align=Align.INLINE)
d.comment(0xa9d9, 'Save the argument in TEMP1', align=Align.INLINE)
d.comment(0xa9dc, 'Point at pi/2...', align=Align.INLINE)
d.comment(0xa9df, '...and unpack it into FWB', align=Align.INLINE)
d.comment(0xa9e2, 'Take the argument sign...', align=Align.INLINE)
d.comment(0xa9e4, '...for FWB', align=Align.INLINE)
d.comment(0xa9e6, 'Halve FWB to +/- pi/4 (rounding bias)', align=Align.INLINE)
d.comment(0xa9e8, 'FWA = argument +/- pi/4', align=Align.INLINE)
d.comment(0xa9eb, 'FWA = that / (pi/2): integer part is the quadrant',
          align=Align.INLINE)
d.comment(0xa9ee, 'Take the integer part', align=Align.INLINE)
d.comment(0xa9f1, 'Low byte of the quadrant count', align=Align.INLINE)
d.comment(0xa9f3, 'save it in &4A', align=Align.INLINE)
d.comment(0xa9f5, 'Is the whole quadrant count zero?', align=Align.INLINE)
d.comment(0xa9f7, '...', align=Align.INLINE)
d.comment(0xa9f9, '...', align=Align.INLINE)
d.comment(0xa9fb, 'yes: argument already in range, use it as is',
          align=Align.INLINE)
d.comment(0xa9fd, 'Rebuild the quadrant count as a real: exponent',
          align=Align.INLINE)
d.comment(0xa9ff, '...', align=Align.INLINE)
d.comment(0xaa01, 'clear the rounding byte', align=Align.INLINE)
d.comment(0xaa03, '...', align=Align.INLINE)
d.comment(0xaa05, 'Sign of the count', align=Align.INLINE)
d.comment(0xaa07, '...', align=Align.INLINE)
d.comment(0xaa09, 'positive: skip', align=Align.INLINE)
d.comment(0xaa0b, 'negative: negate the mantissa', align=Align.INLINE)
d.comment(0xaa0e, 'Normalise the quadrant count', align=Align.INLINE)
d.comment(0xaa11, 'Save it in TEMP2', align=Align.INLINE)
d.comment(0xaa14, 'Cody-Waite reduce: FWA = count * (pi/2 high part)',
          align=Align.INLINE)
d.comment(0xaa17, '...', align=Align.INLINE)
d.comment(0xaa1a, 'FWA = argument - count*(pi/2 high)', align=Align.INLINE)
d.comment(0xaa1d, '...', align=Align.INLINE)
d.comment(0xaa20, 'Save the partial reduction in TEMP1', align=Align.INLINE)
d.comment(0xaa23, 'Reload the quadrant count', align=Align.INLINE)
d.comment(0xaa26, '...', align=Align.INLINE)
d.comment(0xaa29, 'FWA = count * (pi/2 low part)', align=Align.INLINE)
d.comment(0xaa2c, '...', align=Align.INLINE)
d.comment(0xaa2f, 'Subtract the low part too: FWA = reduced angle',
          align=Align.INLINE)
d.comment(0xaa32, '...', align=Align.INLINE)
d.comment(0xaa35, 'Argument in range: reduced angle is the argument',
          align=Align.INLINE)
d.comment(0xaa38, 'Argument too large: error', align=Align.INLINE)

# caad1: shared finish - scale the series result by the saved argument.
d.comment(0xaad1, 'Point at the saved argument in TEMP3', align=Align.INLINE)
d.comment(0xaad4, 'FWA = series * argument', align=Align.INLINE)
d.comment(0xaad7, 'real result', align=Align.INLINE)
d.comment(0xaad9, 'Return', align=Align.INLINE)
d.comment(0xaada, 'Point at the coefficient table: low byte',
          align=Align.INLINE)
d.comment(0xaadc, '...high', align=Align.INLINE)
d.comment(0xaade, 'Evaluate the continued fraction', align=Align.INLINE)
d.comment(0xaae1, 'real result', align=Align.INLINE)
d.comment(0xaae3, 'Return', align=Align.INLINE)

# ----------------------------------------------------------------------
# eval_add_sub (&9C42): expression Level 4 - binary + and -.
# Evaluates a higher-precedence (* / DIV MOD) operand, then while the
# next token is + or - combines it with another such operand. Each
# operand may be integer, real or string; the arms below convert to a
# common type (string concat for +, numeric otherwise).
# ----------------------------------------------------------------------
d.comment(0x9c42, 'Evaluate a * / DIV MOD operand', align=Align.INLINE)
d.comment(0x9c47, 'yes: addition', align=Align.INLINE)
d.comment(0x9c49, 'next operator "-"?', align=Align.INLINE)
d.comment(0x9c4b, 'yes: subtraction', align=Align.INLINE)
d.comment(0x9c4d, 'neither: expression complete', align=Align.INLINE)
d.comment(0x9c4e, 'Addition: type of the left operand', align=Align.INLINE)
d.comment(0x9c4f, 'string: concatenate', align=Align.INLINE)
d.comment(0x9c51, 'real: handle as float add', align=Align.INLINE)
d.comment(0x9c53, 'integer: stack it and evaluate the right operand',
          align=Align.INLINE)
d.comment(0x9c56, 'Type of the right operand', align=Align.INLINE)
d.comment(0x9c57, 'string: Type mismatch', align=Align.INLINE)
d.comment(0x9c59, 'real: convert the left integer to float', align=Align.INLINE)
# iwa_add (&9C5B): integer + integer, 32-bit, operand on the stack.
d.comment(0x9c5b, 'int + int: add the 32-bit stacked value to IWA',
          align=Align.INLINE)
d.comment(0x9c5d, '...byte 0', align=Align.INLINE)
d.comment(0x9c5e, '...', align=Align.INLINE)
d.comment(0x9c60, '...', align=Align.INLINE)
d.comment(0x9c62, '...', align=Align.INLINE)
d.comment(0x9c64, '...byte 1', align=Align.INLINE)
d.comment(0x9c65, '...', align=Align.INLINE)
d.comment(0x9c67, '...', align=Align.INLINE)
d.comment(0x9c69, '...', align=Align.INLINE)
d.comment(0x9c6b, '...byte 2', align=Align.INLINE)
d.comment(0x9c6c, '...', align=Align.INLINE)
d.comment(0x9c6e, '...', align=Align.INLINE)
d.comment(0x9c70, '...', align=Align.INLINE)
d.comment(0x9c72, '...byte 3', align=Align.INLINE)
d.comment(0x9c73, '...', align=Align.INLINE)
d.comment(0x9c75, '...', align=Align.INLINE)
d.comment(0x9c77, 'Drop the operand from the stack', align=Align.INLINE)
d.comment(0x9c79, '...', align=Align.INLINE)
d.comment(0x9c7a, '...', align=Align.INLINE)
d.comment(0x9c7c, '...(four bytes)', align=Align.INLINE)
d.comment(0x9c7e, '...', align=Align.INLINE)
d.comment(0x9c80, 'Result type = integer', align=Align.INLINE)
d.comment(0x9c82, 'loop for further + or -', align=Align.INLINE)
d.comment(0x9c84, '...', align=Align.INLINE)
d.comment(0x9c86, '...', align=Align.INLINE)
d.comment(0x9c88, 'Type mismatch error', align=Align.INLINE)
d.comment(0x9c8b, 'Left real: stack it, evaluate the right operand',
          align=Align.INLINE)
d.comment(0x9c8e, '...', align=Align.INLINE)
d.comment(0x9c91, 'Type of the right operand', align=Align.INLINE)
d.comment(0x9c92, 'string: Type mismatch', align=Align.INLINE)
d.comment(0x9c94, 'remember it for later', align=Align.INLINE)
d.comment(0x9c96, 'real: no conversion needed', align=Align.INLINE)
d.comment(0x9c98, 'integer: convert the right operand to float',
          align=Align.INLINE)
d.comment(0x9c9b, 'Pop the stacked real as the fp operand', align=Align.INLINE)
d.comment(0x9c9e, 'FWA = left + right', align=Align.INLINE)
d.comment(0x9ca1, 'Restore the next character', align=Align.INLINE)
d.comment(0x9ca3, 'Result type = real', align=Align.INLINE)
d.comment(0x9ca5, 'loop for further + or -', align=Align.INLINE)
d.comment(0x9ca7, 'Left int, right real: save the operator', align=Align.INLINE)
d.comment(0x9ca9, 'pop the stacked left integer', align=Align.INLINE)
d.comment(0x9cac, 'stack the right real', align=Align.INLINE)
d.comment(0x9caf, 'convert the left integer to float', align=Align.INLINE)
d.comment(0x9cb2, 'then do float + float', align=Align.INLINE)
d.comment(0x9cb5, 'Subtraction: type of the left operand', align=Align.INLINE)
d.comment(0x9cb6, 'string: Type mismatch', align=Align.INLINE)
d.comment(0x9cb8, 'real: handle as float subtract', align=Align.INLINE)
d.comment(0x9cba, 'integer: stack it, evaluate the right operand',
          align=Align.INLINE)
d.comment(0x9cbd, 'Type of the right operand', align=Align.INLINE)
d.comment(0x9cbe, 'string: Type mismatch', align=Align.INLINE)
d.comment(0x9cc0, 'real: convert and subtract as floats', align=Align.INLINE)
# iwa_rsub (&9CC2): integer - integer (stacked - IWA), 32-bit.
d.comment(0x9cc2, 'int - int: stacked value minus IWA, byte 0',
          align=Align.INLINE)
d.comment(0x9cc3, '...', align=Align.INLINE)
d.comment(0x9cc5, '...', align=Align.INLINE)
d.comment(0x9cc7, '...', align=Align.INLINE)
d.comment(0x9cc9, '...', align=Align.INLINE)
d.comment(0x9ccb, '...byte 1', align=Align.INLINE)
d.comment(0x9ccc, '...', align=Align.INLINE)
d.comment(0x9cce, '...', align=Align.INLINE)
d.comment(0x9cd0, '...', align=Align.INLINE)
d.comment(0x9cd2, '...byte 2', align=Align.INLINE)
d.comment(0x9cd3, '...', align=Align.INLINE)
d.comment(0x9cd5, '...', align=Align.INLINE)
d.comment(0x9cd7, '...', align=Align.INLINE)
d.comment(0x9cd9, '...byte 3', align=Align.INLINE)
d.comment(0x9cda, '...', align=Align.INLINE)
d.comment(0x9cdc, '...', align=Align.INLINE)
d.comment(0x9cde, 'store byte 3, drop the operand and loop', align=Align.INLINE)
d.comment(0x9ce1, 'Left real: stack it, evaluate the right operand',
          align=Align.INLINE)
d.comment(0x9ce4, '...', align=Align.INLINE)
d.comment(0x9ce7, 'Type of the right operand', align=Align.INLINE)
d.comment(0x9ce8, 'string: Type mismatch', align=Align.INLINE)
d.comment(0x9cea, 'remember it', align=Align.INLINE)
d.comment(0x9cec, 'real: no conversion needed', align=Align.INLINE)
d.comment(0x9cee, 'integer: convert the right operand to float',
          align=Align.INLINE)
d.comment(0x9cf1, 'Pop the stacked real as the fp operand', align=Align.INLINE)
d.comment(0x9cf4, 'FWA = left - right', align=Align.INLINE)
d.comment(0x9cf7, 'set result type and loop', align=Align.INLINE)
d.comment(0x9cfa, 'Left int, right real: save the operator', align=Align.INLINE)
d.comment(0x9cfc, 'pop the stacked left integer', align=Align.INLINE)
d.comment(0x9cff, 'stack the right real', align=Align.INLINE)
d.comment(0x9d02, 'convert the left integer to float', align=Align.INLINE)
d.comment(0x9d05, 'pop the stacked right real', align=Align.INLINE)
d.comment(0x9d08, 'FWA = left - right', align=Align.INLINE)
d.comment(0x9d0b, 'set result type and loop', align=Align.INLINE)

# fwa_to_int2 (&A3FE): FWA float -> 64-bit fixed integer (FWA:FWB).
# Denormalises the mantissa to exponent &A0 (an exact integer), the low
# bits spilling into FWB. Used by INT and the SIN/COS reduction.
d.comment(0xa3fe, 'Exponent of FWA', align=Align.INLINE)
d.comment(0xa400, '< 1: result is zero', align=Align.INLINE)
d.comment(0xa402, 'Clear the low-order extension (FWB)', align=Align.INLINE)
d.comment(0xa405, 'Sign of FWA', align=Align.INLINE)
d.comment(0xa408, 'non-zero: denormalise', align=Align.INLINE)
d.comment(0xa40a, 'zero: nothing to do', align=Align.INLINE)
d.comment(0xa40c, 'Exponent', align=Align.INLINE)
d.comment(0xa40e, 'already a 32-bit integer (exp = +32)?', align=Align.INLINE)
d.comment(0xa410, 'yes: check it fits', align=Align.INLINE)
d.comment(0xa412, 'within a byte-shift of integer?', align=Align.INLINE)
d.comment(0xa414, 'yes: finish with bit shifts', align=Align.INLINE)
d.comment(0xa416, 'Fast path: shift right one byte (exp += 8)',
          align=Align.INLINE)
d.comment(0xa418, '...', align=Align.INLINE)
d.comment(0xa41a, 'shift the mantissa down a byte, low byte into FWB',
          align=Align.INLINE)
d.comment(0xa41c, '...', align=Align.INLINE)
d.comment(0xa41e, '...', align=Align.INLINE)
d.comment(0xa420, '...', align=Align.INLINE)
d.comment(0xa422, '...', align=Align.INLINE)
d.comment(0xa424, '...', align=Align.INLINE)
d.comment(0xa426, '...', align=Align.INLINE)
d.comment(0xa428, '...', align=Align.INLINE)
d.comment(0xa42a, '...', align=Align.INLINE)
d.comment(0xa42c, '...', align=Align.INLINE)
d.comment(0xa42e, '...', align=Align.INLINE)
d.comment(0xa430, '...', align=Align.INLINE)
d.comment(0xa432, '...', align=Align.INLINE)
d.comment(0xa434, '...', align=Align.INLINE)
d.comment(0xa436, '...', align=Align.INLINE)
d.comment(0xa438, '...', align=Align.INLINE)
d.comment(0xa43a, 'loop', align=Align.INLINE)
d.comment(0xa43c, 'Slow path: shift FWA:FWB right one bit', align=Align.INLINE)
d.comment(0xa43e, '...', align=Align.INLINE)
d.comment(0xa440, '...', align=Align.INLINE)
d.comment(0xa442, '...', align=Align.INLINE)
d.comment(0xa444, '...', align=Align.INLINE)
d.comment(0xa446, '...', align=Align.INLINE)
d.comment(0xa448, '...', align=Align.INLINE)
d.comment(0xa44a, '...', align=Align.INLINE)
d.comment(0xa44c, 'exp += 1', align=Align.INLINE)
d.comment(0xa44e, 'loop until an exact integer', align=Align.INLINE)
d.comment(0xa450, 'Magnitude too large: Too big error', align=Align.INLINE)

# fwb_clear (&A453): zero the second FP accumulator.
d.comment(0xa453, 'Zero every byte of FWB', align=Align.INLINE)
d.comment(0xa455, '...sign', align=Align.INLINE)
d.comment(0xa457, '...overflow', align=Align.INLINE)
d.comment(0xa459, '...exponent', align=Align.INLINE)
d.comment(0xa45b, '...mantissa byte 1', align=Align.INLINE)
d.comment(0xa45d, '...byte 2', align=Align.INLINE)
d.comment(0xa45f, '...byte 3', align=Align.INLINE)
d.comment(0xa461, '...byte 4', align=Align.INLINE)
d.comment(0xa463, '...rounding byte', align=Align.INLINE)
d.comment(0xa465, 'Return', align=Align.INLINE)
d.comment(0xa466, 'Exponent > 32: Too big error', align=Align.INLINE)
d.comment(0xa468, 'Positive: integer ready, return', align=Align.INLINE)
d.comment(0xa46a, 'positive: nothing to do', align=Align.INLINE)
d.comment(0xa46c, 'Negative: negate the 32-bit mantissa', align=Align.INLINE)
d.comment(0xa46d, 'low byte first: 0...', align=Align.INLINE)
d.comment(0xa46f, 'minus m4,', align=Align.INLINE)
d.comment(0xa471, '(store)', align=Align.INLINE)
d.comment(0xa473, '0...', align=Align.INLINE)
d.comment(0xa475, 'minus m3 (borrow in),', align=Align.INLINE)
d.comment(0xa477, '(store)', align=Align.INLINE)
d.comment(0xa479, '0...', align=Align.INLINE)
d.comment(0xa47b, 'minus m2 (borrow in),', align=Align.INLINE)
d.comment(0xa47d, '(store)', align=Align.INLINE)
d.comment(0xa47f, '0...', align=Align.INLINE)
d.comment(0xa481, 'minus m1 (borrow in)', align=Align.INLINE)
d.comment(0xa483, '(store)', align=Align.INLINE)

# Multiply-level (eval_mul_div) float-coercion tails (&9D0E).
d.comment(0x9d0e, 'Convert the right integer to float', align=Align.INLINE)
d.comment(0x9d11, 'Pop the stacked left integer', align=Align.INLINE)
d.comment(0x9d14, 'stack the right real', align=Align.INLINE)
d.comment(0x9d17, 'convert the left integer to float', align=Align.INLINE)
d.comment(0x9d1a, 'then do float * float', align=Align.INLINE)
d.comment(0x9d1d, 'Convert the left integer to float', align=Align.INLINE)
d.comment(0x9d20, 'Stack the left real', align=Align.INLINE)
d.comment(0x9d23, 'evaluate the next (^ level) operand', align=Align.INLINE)
d.comment(0x9d26, 'remember the operand type', align=Align.INLINE)
d.comment(0x9d28, '...', align=Align.INLINE)
d.comment(0x9d29, 'ensure the operand is real', align=Align.INLINE)
d.comment(0x9d2c, 'Pop the stacked left real', align=Align.INLINE)
d.comment(0x9d2f, 'FWA = left * right', align=Align.INLINE)

# fwa_sub_var (&A4D0): FWA = FWA - operand.
d.comment(0xa4d0, 'operand - FWA...', align=Align.INLINE)
d.comment(0xa4d3, '...then negate to give FWA - operand', align=Align.INLINE)

# fp_split_int_frac (&A486): integer part -> &4A, fraction -> FWA.
d.comment(0xa486, 'Exponent of FWA', align=Align.INLINE)
d.comment(0xa488, '|x| >= 1: has an integer part', align=Align.INLINE)
d.comment(0xa48a, '|x| < 1: integer part is zero', align=Align.INLINE)
d.comment(0xa48c, '...', align=Align.INLINE)
d.comment(0xa48e, 'return the fraction (= x)', align=Align.INLINE)
d.comment(0xa491, 'Convert to a fixed integer (fraction into FWB)',
          align=Align.INLINE)
d.comment(0xa494, 'Low byte of the integer part...', align=Align.INLINE)
d.comment(0xa496, '...kept in &4A', align=Align.INLINE)
d.comment(0xa498, 'Bring the fractional bits back into FWA', align=Align.INLINE)
d.comment(0xa49b, 'Exponent for a value in [0,1)', align=Align.INLINE)
d.comment(0xa49d, '...', align=Align.INLINE)
d.comment(0xa49f, 'Top fraction bit set (fraction >= 0.5)?', align=Align.INLINE)
d.comment(0xa4a1, 'no: fraction already in range', align=Align.INLINE)
d.comment(0xa4a3, 'Round to nearest: flip the fraction sign', align=Align.INLINE)
d.comment(0xa4a5, '...', align=Align.INLINE)
d.comment(0xa4a7, 'positive: round the integer part up', align=Align.INLINE)
d.comment(0xa4a9, '...', align=Align.INLINE)
d.comment(0xa4ab, '...', align=Align.INLINE)
d.comment(0xa4ae, 'negative: round the integer part down', align=Align.INLINE)
d.comment(0xa4b0, 'Negate the fraction mantissa', align=Align.INLINE)
d.comment(0xa4b3, 'Normalise the fraction', align=Align.INLINE)
d.comment(0xa4b6, 'Increment the integer-part mantissa (carry up)',
          align=Align.INLINE)
d.comment(0xa4b8, '...', align=Align.INLINE)
d.comment(0xa4ba, '...', align=Align.INLINE)
d.comment(0xa4bc, '...', align=Align.INLINE)
d.comment(0xa4be, '...', align=Align.INLINE)
d.comment(0xa4c0, '...', align=Align.INLINE)
d.comment(0xa4c2, '...', align=Align.INLINE)
d.comment(0xa4c4, 'overflow: Too big', align=Align.INLINE)
d.comment(0xa4c6, 'Return', align=Align.INLINE)
d.comment(0xa4c7, 'Decrement the mantissa magnitude (negate, +1, negate)',
          align=Align.INLINE)
d.comment(0xa4ca, '...', align=Align.INLINE)
d.comment(0xa4cd, '...', align=Align.INLINE)

# fn_exp (&AA91): EXP(x) = e^x = e^int(x) * e^frac(x).
d.comment(0xaa91, 'Evaluate the argument as a real', align=Align.INLINE)
d.comment(0xaa94, 'Exponent of x', align=Align.INLINE)
d.comment(0xaa96, 'x small enough to compute directly?', align=Align.INLINE)
d.comment(0xaa98, 'yes: compute', align=Align.INLINE)
d.comment(0xaa9a, 'much too large: handle the overflow case', align=Align.INLINE)
d.comment(0xaa9c, 'borderline: test the mantissa', align=Align.INLINE)
d.comment(0xaa9e, '...against the overflow threshold', align=Align.INLINE)
d.comment(0xaaa0, 'below it: still computable', align=Align.INLINE)
d.comment(0xaaa2, 'Sign of x', align=Align.INLINE)
d.comment(0xaaa4, 'x very negative: e^x underflows to 0', align=Align.INLINE)
d.comment(0xaaa6, 'FWA = 0', align=Align.INLINE)
d.comment(0xaaa9, 'real result', align=Align.INLINE)
d.comment(0xaaab, 'Return', align=Align.INLINE)
d.comment(0xaaac, 'x very positive: Exp range error', align=Align.INLINE)
d.comment(0xaab8, 'Split x into integer (&4A) and fraction', align=Align.INLINE)
d.comment(0xaabb, 'FWA = e^frac via the series', align=Align.INLINE)
d.comment(0xaabe, 'Save e^frac in TEMP3', align=Align.INLINE)
d.comment(0xaac1, 'Point at the constant e: low byte', align=Align.INLINE)
d.comment(0xaac3, '...', align=Align.INLINE)
d.comment(0xaac5, 'high byte', align=Align.INLINE)
d.comment(0xaac7, '...', align=Align.INLINE)
d.comment(0xaac9, 'FWA = e', align=Align.INLINE)
d.comment(0xaacc, 'Integer part of x', align=Align.INLINE)
d.comment(0xaace, 'FWA = e^int', align=Align.INLINE)
# AAD1 continues into caad1: FWA = e^int * e^frac (already commented).

# fn_ln (&A7FE): LN(x) = ln(mantissa) + binary_exponent * ln 2.
d.comment(0xa7fe, 'Evaluate the argument as a real', align=Align.INLINE)
d.comment(0xa801, 'Sign of x', align=Align.INLINE)
d.comment(0xa804, 'zero: error', align=Align.INLINE)
d.comment(0xa806, 'positive: compute', align=Align.INLINE)
d.comment(0xa808, 'zero or negative: Log range error', align=Align.INLINE)
d.comment(0xa814, 'Set FWB = -1 (to form mantissa - 1)', align=Align.INLINE)
d.comment(0xa817, '...', align=Align.INLINE)
d.comment(0xa819, '...', align=Align.INLINE)
d.comment(0xa81b, '...', align=Align.INLINE)
d.comment(0xa81d, '...', align=Align.INLINE)
d.comment(0xa81e, '...', align=Align.INLINE)
d.comment(0xa820, 'Binary exponent of x', align=Align.INLINE)
d.comment(0xa822, 'zero mantissa exponent?', align=Align.INLINE)
d.comment(0xa824, 'Mantissa top byte', align=Align.INLINE)
d.comment(0xa826, 'below sqrt(2)?', align=Align.INLINE)
d.comment(0xa828, 'yes: keep this exponent', align=Align.INLINE)
d.comment(0xa82a, 'no: scale mantissa to [sqrt(1/2), sqrt(2)]', align=Align.INLINE)
d.comment(0xa82b, '...and adjust the exponent', align=Align.INLINE)
d.comment(0xa82c, 'Save the adjusted binary exponent', align=Align.INLINE)
d.comment(0xa82d, '...', align=Align.INLINE)
d.comment(0xa82e, 'Set the mantissa exponent', align=Align.INLINE)
d.comment(0xa830, 'FWA = mantissa - 1', align=Align.INLINE)
d.comment(0xa833, 'Save (m-1) in TEMP4', align=Align.INLINE)
d.comment(0xa835, '...', align=Align.INLINE)
d.comment(0xa838, 'Point at the ln coefficient table: low byte',
          align=Align.INLINE)
d.comment(0xa83a, '...high', align=Align.INLINE)
d.comment(0xa83c, 'Evaluate the ln continued fraction', align=Align.INLINE)
d.comment(0xa83f, 'Point at (m-1) in TEMP4', align=Align.INLINE)
d.comment(0xa842, 'Scale by (m-1)...', align=Align.INLINE)
d.comment(0xa845, '...and again', align=Align.INLINE)
d.comment(0xa848, 'Add (m-1): FWA = ln(mantissa)', align=Align.INLINE)
d.comment(0xa84b, 'Save ln(mantissa) in TEMP1', align=Align.INLINE)
d.comment(0xa84e, 'Recover the adjusted exponent', align=Align.INLINE)
d.comment(0xa84f, '...', align=Align.INLINE)
d.comment(0xa850, 'Binary exponent e = adjusted - &81', align=Align.INLINE)
d.comment(0xa852, 'FWA = e', align=Align.INLINE)
d.comment(0xa855, 'Point at the constant ln 2: low byte', align=Align.INLINE)
d.comment(0xa857, '...', align=Align.INLINE)
d.comment(0xa859, 'high byte', align=Align.INLINE)
d.comment(0xa85b, '...', align=Align.INLINE)
d.comment(0xa85d, 'FWA = e * ln 2', align=Align.INLINE)
d.comment(0xa860, 'Point at ln(mantissa) in TEMP1', align=Align.INLINE)
d.comment(0xa863, 'LN(x) = e*ln2 + ln(mantissa)', align=Align.INLINE)
d.comment(0xa866, 'real result', align=Align.INLINE)
d.comment(0xa868, 'Return', align=Align.INLINE)

# fwa_int_power (&AB12): FWA = FWA ^ n, n in A.
d.comment(0xab12, 'Exponent n', align=Align.INLINE)
d.comment(0xab13, 'positive?', align=Align.INLINE)
d.comment(0xab15, 'negative: use |n| and reciprocate', align=Align.INLINE)
d.comment(0xab16, '...', align=Align.INLINE)
d.comment(0xab17, '...', align=Align.INLINE)
d.comment(0xab19, 'save the count', align=Align.INLINE)
d.comment(0xab1a, 'FWA = 1 / FWA', align=Align.INLINE)
d.comment(0xab1d, 'restore the count', align=Align.INLINE)
d.comment(0xab1e, 'Save the count', align=Align.INLINE)
d.comment(0xab1f, 'Stash the base in TEMP1', align=Align.INLINE)
d.comment(0xab22, 'FWA = 1 (running product)', align=Align.INLINE)
d.comment(0xab25, 'Count remaining', align=Align.INLINE)
d.comment(0xab26, 'zero: done', align=Align.INLINE)
d.comment(0xab28, 'One multiplication fewer', align=Align.INLINE)
d.comment(0xab29, '...', align=Align.INLINE)
d.comment(0xab2b, '...', align=Align.INLINE)
d.comment(0xab2c, 'FWA = FWA * base', align=Align.INLINE)
d.comment(0xab2f, 'loop', align=Align.INLINE)

# fwa_to_int (&A3E4): convert FWA real to the integer accumulator.
d.comment(0xa3e4, 'Denormalise FWA to a fixed integer', align=Align.INLINE)
d.comment(0xa3e7, 'Copy the 32-bit mantissa into IWA: byte 3', align=Align.INLINE)
d.comment(0xa3e9, '...', align=Align.INLINE)
d.comment(0xa3eb, 'byte 2', align=Align.INLINE)
d.comment(0xa3ed, '...', align=Align.INLINE)
d.comment(0xa3ef, 'byte 1', align=Align.INLINE)
d.comment(0xa3f1, '...', align=Align.INLINE)
d.comment(0xa3f3, 'byte 0', align=Align.INLINE)
d.comment(0xa3f5, '...', align=Align.INLINE)
d.comment(0xa3f7, 'Return', align=Align.INLINE)
d.comment(0xa3f8, '|x| < 1: FWB = FWA', align=Align.INLINE)
d.comment(0xa3fb, 'integer is zero', align=Align.INLINE)

# iwa_test_var (&9AAD): signed 32-bit compare of stacked int vs IWA.
# Flips the sign bits so an unsigned subtract orders signed values, then
# subtracts and returns the comparison in the C and Z flags (Z = equal).
d.comment(0x9aad, 'Flip the sign bit of the IWA top byte', align=Align.INLINE)
d.comment(0x9aaf, '...', align=Align.INLINE)
d.comment(0x9ab1, '...', align=Align.INLINE)
d.comment(0x9ab3, 'Subtract IWA from the stacked integer: byte 0',
          align=Align.INLINE)
d.comment(0x9ab4, '...', align=Align.INLINE)
d.comment(0x9ab6, '...', align=Align.INLINE)
d.comment(0x9ab8, '...', align=Align.INLINE)
d.comment(0x9aba, '...', align=Align.INLINE)
d.comment(0x9abc, 'byte 1', align=Align.INLINE)
d.comment(0x9abd, '...', align=Align.INLINE)
d.comment(0x9abf, '...', align=Align.INLINE)
d.comment(0x9ac1, '...', align=Align.INLINE)
d.comment(0x9ac3, 'byte 2', align=Align.INLINE)
d.comment(0x9ac4, '...', align=Align.INLINE)
d.comment(0x9ac6, '...', align=Align.INLINE)
d.comment(0x9ac8, '...', align=Align.INLINE)
d.comment(0x9aca, 'byte 3 (top)', align=Align.INLINE)
d.comment(0x9acb, '...', align=Align.INLINE)
d.comment(0x9acd, '...', align=Align.INLINE)
d.comment(0x9acf, 'flip its sign bit too', align=Align.INLINE)
d.comment(0x9ad1, 'finish the signed subtract: sets C', align=Align.INLINE)
d.comment(0x9ad3, 'OR the low bytes...', align=Align.INLINE)
d.comment(0x9ad5, '...', align=Align.INLINE)
d.comment(0x9ad7, '...to set Z when the values are equal', align=Align.INLINE)
d.comment(0x9ad9, 'Save the comparison flags', align=Align.INLINE)
d.comment(0x9ada, 'Drop the integer from the stack', align=Align.INLINE)
d.comment(0x9adb, '...', align=Align.INLINE)
d.comment(0x9add, '...', align=Align.INLINE)
d.comment(0x9adf, '...', align=Align.INLINE)
d.comment(0x9ae1, '...', align=Align.INLINE)
d.comment(0x9ae3, '...', align=Align.INLINE)
d.comment(0x9ae5, 'Restore the flags', align=Align.INLINE)
d.comment(0x9ae6, 'Return', align=Align.INLINE)

# ----------------------------------------------------------------------
# eval_relational (&9B9C): expression Level 5 - comparisons.
# Evaluates a + - operand, then if the next token is a relational
# operator (< = >) parses the full operator (<, <=, <>, =, >, >=),
# compares the two operands and returns -1 (TRUE) or 0 (FALSE) as an
# integer.
# ----------------------------------------------------------------------
d.comment(0x9b9c, 'Evaluate a + - operand', align=Align.INLINE)
d.comment(0x9b9f, "next token past '>'?", align=Align.INLINE)
d.comment(0x9ba1, 'yes: not a comparison, return', align=Align.INLINE)
d.comment(0x9ba3, "before '<'?", align=Align.INLINE)
d.comment(0x9ba5, 'a relational operator: handle it', align=Align.INLINE)
d.comment(0x9ba7, 'not a comparison: return', align=Align.INLINE)
d.comment(0x9ba8, "'<' family?", align=Align.INLINE)
d.comment(0x9baa, "'>' family?", align=Align.INLINE)
d.comment(0x9bac, 'yes', align=Align.INLINE)
d.comment(0x9bae, "'=': compare for equality", align=Align.INLINE)
d.comment(0x9baf, 'evaluate the right operand and compare', align=Align.INLINE)
d.comment(0x9bb2, 'not equal: result FALSE (0)', align=Align.INLINE)
d.comment(0x9bb4, 'equal: result TRUE (Y = &FF)', align=Align.INLINE)
d.comment(0x9bb5, 'Store 0/-1 in all four IWA bytes', align=Align.INLINE)
d.comment(0x9bb7, '...', align=Align.INLINE)
d.comment(0x9bb9, '...', align=Align.INLINE)
d.comment(0x9bbb, '...', align=Align.INLINE)
d.comment(0x9bbd, 'Result type = integer', align=Align.INLINE)
d.comment(0x9bbf, 'Return', align=Align.INLINE)
d.comment(0x9bc0, "'<' family: discard the operator", align=Align.INLINE)
d.comment(0x9bc1, 'Peek at the next source character', align=Align.INLINE)
d.comment(0x9bc3, '...', align=Align.INLINE)
d.comment(0x9bc5, "'='?  (<=)", align=Align.INLINE)
d.comment(0x9bc7, 'yes', align=Align.INLINE)
d.comment(0x9bc9, "'>'?  (<>)", align=Align.INLINE)
d.comment(0x9bcb, 'yes', align=Align.INLINE)
d.comment(0x9bcd, 'plain "<": evaluate and compare', align=Align.INLINE)
d.comment(0x9bd0, 'less: TRUE', align=Align.INLINE)
d.comment(0x9bd2, 'not less: FALSE', align=Align.INLINE)
d.comment(0x9bd4, "'<=': step past the '='", align=Align.INLINE)
d.comment(0x9bd6, 'evaluate and compare', align=Align.INLINE)
d.comment(0x9bd9, 'equal: TRUE', align=Align.INLINE)
d.comment(0x9bdb, 'less: TRUE', align=Align.INLINE)
d.comment(0x9bdd, 'greater: FALSE', align=Align.INLINE)
d.comment(0x9bdf, "'<>': step past the '>'", align=Align.INLINE)
d.comment(0x9be1, 'evaluate and compare', align=Align.INLINE)
d.comment(0x9be4, 'unequal: TRUE', align=Align.INLINE)
d.comment(0x9be6, 'equal: FALSE', align=Align.INLINE)
d.comment(0x9be8, "'>' family: discard the operator", align=Align.INLINE)
d.comment(0x9be9, 'Peek at the next source character', align=Align.INLINE)
d.comment(0x9beb, '...', align=Align.INLINE)
d.comment(0x9bed, "'='?  (>=)", align=Align.INLINE)
d.comment(0x9bef, 'yes', align=Align.INLINE)
d.comment(0x9bf1, 'plain ">": evaluate and compare', align=Align.INLINE)
d.comment(0x9bf4, 'equal: FALSE', align=Align.INLINE)
d.comment(0x9bf6, 'greater: TRUE', align=Align.INLINE)
d.comment(0x9bf8, 'less: FALSE', align=Align.INLINE)
d.comment(0x9bfa, "'>=': step past the '='", align=Align.INLINE)
d.comment(0x9bfc, 'evaluate and compare', align=Align.INLINE)
d.comment(0x9bff, 'greater or equal: TRUE', align=Align.INLINE)
d.comment(0x9c01, 'less: FALSE', align=Align.INLINE)

# fn_log (&ABA8): LOG(x) = log10(x) = ln(x) * log10(e).
d.comment(0xaba8, 'FWA = ln(x)', align=Align.INLINE)
d.comment(0xabab, 'Point at the constant log10(e): low byte', align=Align.INLINE)
d.comment(0xabad, 'high byte', align=Align.INLINE)
d.comment(0xabaf, 'FWA = ln(x) * log10(e)', align=Align.INLINE)

# assign_number (&B4B4): store a numeric value into a numeric variable.
d.comment(0xb4b4, 'Pop the variable data address from the stack',
          align=Align.INLINE)
d.comment(0xb4b7, "Variable's size/type byte", align=Align.INLINE)
d.comment(0xb4b9, 'size 5 = real variable?', align=Align.INLINE)
d.comment(0xb4bb, 'yes: store as a real', align=Align.INLINE)
d.comment(0xb4bd, 'Type of the value', align=Align.INLINE)
d.comment(0xb4bf, 'string: Type mismatch', align=Align.INLINE)
d.comment(0xb4c1, 'integer: store directly', align=Align.INLINE)
d.comment(0xb4c3, 'real value, integer variable: convert', align=Align.INLINE)

# ----------------------------------------------------------------------
# stmt_if (&98C2): the IF statement.
# Evaluates the condition, then for a true result executes the THEN
# part (a statement or a GOTO line number); for false it scans the rest
# of the line for ELSE and runs what follows, else moves to the next
# line.
# ----------------------------------------------------------------------
d.comment(0x98c2, 'Evaluate the condition', align=Align.INLINE)
d.comment(0x98c5, 'string: handle elsewhere', align=Align.INLINE)
d.comment(0x98c7, 'integer: use as is', align=Align.INLINE)
d.comment(0x98c9, 'real: convert to integer', align=Align.INLINE)
d.comment(0x98cc, 'Advance the text pointer past the condition',
          align=Align.INLINE)
d.comment(0x98ce, '...', align=Align.INLINE)
d.comment(0x98d0, 'Is the condition value zero (false)?', align=Align.INLINE)
d.comment(0x98d2, '...', align=Align.INLINE)
d.comment(0x98d4, '...', align=Align.INLINE)
d.comment(0x98d6, '...', align=Align.INLINE)
d.comment(0x98d8, 'false: look for ELSE', align=Align.INLINE)
d.comment(0x98da, 'true: is the next token THEN?', align=Align.INLINE)
d.comment(0x98dc, 'yes', align=Align.INLINE)
d.comment(0x98de, 'no THEN: execute the statement that follows',
          align=Align.INLINE)
d.comment(0x98e1, 'Step past THEN', align=Align.INLINE)
d.comment(0x98e3, 'Is a line number following (THEN <line>)?',
          align=Align.INLINE)
d.comment(0x98e6, 'no: execute the statements after THEN', align=Align.INLINE)
d.comment(0x98e8, 'yes: set up the line number...', align=Align.INLINE)
d.comment(0x98eb, '...', align=Align.INLINE)
d.comment(0x98ee, '...and GOTO it', align=Align.INLINE)
d.comment(0x98f1, 'False: scan the rest of the line for ELSE',
          align=Align.INLINE)
d.comment(0x98f3, 'Next character', align=Align.INLINE)
d.comment(0x98f5, 'end of line?', align=Align.INLINE)
d.comment(0x98f7, 'yes: move to the next line', align=Align.INLINE)
d.comment(0x98f9, 'advance', align=Align.INLINE)
d.comment(0x98fa, 'ELSE token?', align=Align.INLINE)
d.comment(0x98fc, 'no: keep scanning', align=Align.INLINE)
d.comment(0x98fe, 'found ELSE: point past it', align=Align.INLINE)
d.comment(0x9900, 'execute what follows ELSE', align=Align.INLINE)
d.comment(0x9902, 'No ELSE: continue at the next line', align=Align.INLINE)

# parse_lvalue (&9582): parse a target, creating the variable if needed.
d.comment(0x9582, 'Parse the variable reference', align=Align.INLINE)
d.comment(0x9585, 'found: return', align=Align.INLINE)
d.comment(0x9587, 'indirection/array: return', align=Align.INLINE)
d.comment(0x9589, 'undefined: create the variable', align=Align.INLINE)
d.comment(0x958c, 'Decide how many value bytes to clear', align=Align.INLINE)
d.comment(0x958e, '...', align=Align.INLINE)
d.comment(0x9590, '...', align=Align.INLINE)
d.comment(0x9592, '...', align=Align.INLINE)
d.comment(0x9593, 'then retry the parse so it is found', align=Align.INLINE)
# Top-level indirection operators (?addr, !addr, $addr) as an lvalue.
d.comment(0x9595, "'!' indirection?", align=Align.INLINE)
d.comment(0x9597, 'yes: word indirection', align=Align.INLINE)
d.comment(0x9599, "'$' indirection?", align=Align.INLINE)
d.comment(0x959b, 'yes: string indirection', align=Align.INLINE)
d.comment(0x959d, "'?' indirection?", align=Align.INLINE)
d.comment(0x959f, 'yes: byte indirection', align=Align.INLINE)
d.comment(0x95a1, 'none: not an lvalue', align=Align.INLINE)
d.comment(0x95a3, '...', align=Align.INLINE)
d.comment(0x95a4, 'Return', align=Align.INLINE)
d.comment(0x95a5, "'!': word width (4)", align=Align.INLINE)
d.comment(0x95a7, 'Save the width', align=Align.INLINE)
d.comment(0x95a8, 'step past the operator', align=Align.INLINE)
d.comment(0x95aa, 'evaluate the address', align=Align.INLINE)
d.comment(0x95ad, 'finish as an indirection', align=Align.INLINE)
d.comment(0x95b0, "'$': step past the operator", align=Align.INLINE)
d.comment(0x95b2, 'evaluate the address', align=Align.INLINE)
d.comment(0x95b5, 'address in zero page?', align=Align.INLINE)
d.comment(0x95b7, 'yes: $ range error', align=Align.INLINE)
d.comment(0x95b9, 'Type = string indirection (&80)', align=Align.INLINE)
d.comment(0x95bb, '...', align=Align.INLINE)
d.comment(0x95bd, 'found: SEC', align=Align.INLINE)
d.comment(0x95be, 'Return', align=Align.INLINE)
d.comment(0x95bf, '$ range error', align=Align.INLINE)

# ----------------------------------------------------------------------
# parse_var_ref (&95C9): parse a variable reference or indirection.
# Scans text via &19/&1A (offset &1B), building the value pointer in
# &2A/&2B and a type byte in &2C; &37/&38 points at the name, &39 its
# length. Handles resident integers (@%, A%-Z% at &0400 + char*4),
# named variables and arrays, and the ?, ! and $ indirection operators.
# ----------------------------------------------------------------------
d.comment(0x95c9, 'Copy the text pointer into the scan pointer',
          align=Align.INLINE)
d.comment(0x95cb, '...', align=Align.INLINE)
d.comment(0x95cd, '...', align=Align.INLINE)
d.comment(0x95cf, '...', align=Align.INLINE)
d.comment(0x95d1, 'Start one before the text offset', align=Align.INLINE)
d.comment(0x95d3, '...', align=Align.INLINE)
d.comment(0x95d4, 'Advance', align=Align.INLINE)
d.comment(0x95d5, 'Record the scan offset', align=Align.INLINE)
d.comment(0x95d7, 'Next character', align=Align.INLINE)
d.comment(0x95d9, 'space?', align=Align.INLINE)
d.comment(0x95db, 'skip spaces', align=Align.INLINE)
d.comment(0x95dd, "below '@': an indirection operator", align=Align.INLINE)
d.comment(0x95df, '...', align=Align.INLINE)
d.comment(0x95e1, "above 'Z'?", align=Align.INLINE)
d.comment(0x95e3, 'yes: a named (dynamic) variable', align=Align.INLINE)
d.comment(0x95e5, 'Resident integer: hash char to &0400 + char*4',
          align=Align.INLINE)
d.comment(0x95e6, '...', align=Align.INLINE)
d.comment(0x95e7, 'value pointer low', align=Align.INLINE)
d.comment(0x95e9, 'page &04', align=Align.INLINE)
d.comment(0x95eb, '...', align=Align.INLINE)
d.comment(0x95ed, 'Second character', align=Align.INLINE)
d.comment(0x95ee, '...', align=Align.INLINE)
d.comment(0x95f0, '...', align=Align.INLINE)
d.comment(0x95f1, "must be '%' for a resident integer", align=Align.INLINE)
d.comment(0x95f3, 'not %: treat as a named variable', align=Align.INLINE)
d.comment(0x95f5, 'Type = integer', align=Align.INLINE)
d.comment(0x95f7, '...', align=Align.INLINE)
d.comment(0x95f9, 'Following character', align=Align.INLINE)
d.comment(0x95fb, "'('  -> array element", align=Align.INLINE)
d.comment(0x95fd, 'yes: handle as an array', align=Align.INLINE)
d.comment(0x95ff, 'Named variable: type = real/string (5)', align=Align.INLINE)
d.comment(0x9601, '...', align=Align.INLINE)
d.comment(0x9603, 'Point &37/&38 at the name in the text', align=Align.INLINE)
d.comment(0x9605, '...', align=Align.INLINE)
d.comment(0x9606, '...', align=Align.INLINE)
d.comment(0x9608, '...', align=Align.INLINE)
d.comment(0x960a, '...', align=Align.INLINE)
d.comment(0x960c, '...', align=Align.INLINE)
d.comment(0x960d, '...', align=Align.INLINE)
d.comment(0x960e, '...', align=Align.INLINE)
d.comment(0x9610, '...', align=Align.INLINE)
d.comment(0x9612, '...', align=Align.INLINE)
d.comment(0x9614, '...', align=Align.INLINE)
d.comment(0x9615, '...', align=Align.INLINE)
d.comment(0x9617, 'Reset the length counter', align=Align.INLINE)
d.comment(0x9619, '...', align=Align.INLINE)
d.comment(0x961b, 'Scan the name: next character', align=Align.INLINE)
d.comment(0x961d, "below 'A'?", align=Align.INLINE)
d.comment(0x961f, 'no: check letters', align=Align.INLINE)
d.comment(0x9621, 'a digit?', align=Align.INLINE)
d.comment(0x9623, 'no: name ends', align=Align.INLINE)
d.comment(0x9625, '...', align=Align.INLINE)
d.comment(0x9627, 'no: name ends', align=Align.INLINE)
d.comment(0x9629, 'count this character', align=Align.INLINE)
d.comment(0x962a, '...', align=Align.INLINE)
d.comment(0x962b, 'continue', align=Align.INLINE)
d.comment(0x962d, "above 'Z'?", align=Align.INLINE)
d.comment(0x962f, 'yes: check lower case', align=Align.INLINE)
d.comment(0x9631, 'A-Z: count it', align=Align.INLINE)
d.comment(0x9632, '...', align=Align.INLINE)
d.comment(0x9633, 'continue', align=Align.INLINE)
d.comment(0x9635, "below '_'?", align=Align.INLINE)
d.comment(0x9637, 'yes: name ends', align=Align.INLINE)
d.comment(0x9639, "above 'z'?", align=Align.INLINE)
d.comment(0x963b, 'yes: name ends', align=Align.INLINE)
d.comment(0x963d, '_ or a-z: count it', align=Align.INLINE)
d.comment(0x963e, '...', align=Align.INLINE)
d.comment(0x963f, 'continue', align=Align.INLINE)
d.comment(0x9641, 'Back up to the terminator', align=Align.INLINE)
d.comment(0x9642, 'empty name: undefined', align=Align.INLINE)
d.comment(0x9644, "'$' suffix -> string variable", align=Align.INLINE)
d.comment(0x9646, 'yes', align=Align.INLINE)
d.comment(0x9648, "'%' suffix -> integer variable", align=Align.INLINE)
d.comment(0x964a, 'no: real variable', align=Align.INLINE)
d.comment(0x964c, 'mark the type integer', align=Align.INLINE)
d.comment(0x964e, 'step past the %', align=Align.INLINE)
d.comment(0x964f, '...', align=Align.INLINE)
d.comment(0x9650, '...', align=Align.INLINE)
d.comment(0x9651, 'check the following character', align=Align.INLINE)
d.comment(0x9653, '...', align=Align.INLINE)
d.comment(0x9654, 'Record the name length', align=Align.INLINE)
d.comment(0x9656, "'('  -> array element", align=Align.INLINE)
d.comment(0x9658, 'yes', align=Align.INLINE)
d.comment(0x965a, 'Look the variable up in storage', align=Align.INLINE)
d.comment(0x965d, 'not found: undefined', align=Align.INLINE)
d.comment(0x965f, 'Update the scan offset past the name', align=Align.INLINE)
d.comment(0x9661, 'Next character after the name', align=Align.INLINE)
d.comment(0x9663, '...', align=Align.INLINE)
d.comment(0x9665, "'!' indirection following?", align=Align.INLINE)
d.comment(0x9667, 'yes: word indirection', align=Align.INLINE)
d.comment(0x9669, "'?' indirection following?", align=Align.INLINE)
d.comment(0x966b, 'yes: byte indirection', align=Align.INLINE)
d.comment(0x966d, 'Plain variable: found', align=Align.INLINE)
d.comment(0x966e, 'save the scan offset', align=Align.INLINE)
d.comment(0x9670, 'A = &FF (found)', align=Align.INLINE)
d.comment(0x9672, 'Return', align=Align.INLINE)
d.comment(0x9673, 'Undefined: A=0, SEC', align=Align.INLINE)
d.comment(0x9675, '...', align=Align.INLINE)
d.comment(0x9676, 'Return', align=Align.INLINE)
d.comment(0x9677, 'Found: A=0, CLC', align=Align.INLINE)
d.comment(0x9679, '...', align=Align.INLINE)
d.comment(0x967a, 'Return', align=Align.INLINE)
d.comment(0x967b, "'?' indirection: byte type (1)", align=Align.INLINE)
d.comment(0x967d, '...', align=Align.INLINE)
d.comment(0x967f, "'!' indirection: word type (4)", align=Align.INLINE)
d.comment(0x9681, 'Save the indirection width', align=Align.INLINE)
d.comment(0x9682, 'step past the operator', align=Align.INLINE)
d.comment(0x9683, '...', align=Align.INLINE)
d.comment(0x9685, 'Stack the base address', align=Align.INLINE)
d.comment(0x9688, 'evaluate it as an integer', align=Align.INLINE)
d.comment(0x968b, 'Save the offset expression...', align=Align.INLINE)
d.comment(0x968d, '...', align=Align.INLINE)
d.comment(0x968e, '...', align=Align.INLINE)
d.comment(0x9690, '...', align=Align.INLINE)
d.comment(0x9691, 'evaluate the index expression', align=Align.INLINE)
d.comment(0x9694, 'address = base + index', align=Align.INLINE)
d.comment(0x9695, '...', align=Align.INLINE)
d.comment(0x9696, '...', align=Align.INLINE)
d.comment(0x9698, '...', align=Align.INLINE)
d.comment(0x969a, '...', align=Align.INLINE)
d.comment(0x969b, '...', align=Align.INLINE)
d.comment(0x969d, '...', align=Align.INLINE)
d.comment(0x969f, 'Restore the indirection type', align=Align.INLINE)
d.comment(0x96a0, '...', align=Align.INLINE)
d.comment(0x96a2, 'found: A=&FF, CLC', align=Align.INLINE)
d.comment(0x96a3, '...', align=Align.INLINE)
d.comment(0x96a5, 'Return', align=Align.INLINE)
d.comment(0x96a6, 'Resident-integer array: step past "("', align=Align.INLINE)
d.comment(0x96a7, '...', align=Align.INLINE)
d.comment(0x96a9, 'index the array', align=Align.INLINE)
d.comment(0x96ac, 'check for trailing ! or ?', align=Align.INLINE)
d.comment(0x96af, 'String variable: step past "$"', align=Align.INLINE)
d.comment(0x96b0, '...', align=Align.INLINE)
d.comment(0x96b1, 'record the name length', align=Align.INLINE)
d.comment(0x96b3, '...', align=Align.INLINE)
d.comment(0x96b4, 'mark the type string', align=Align.INLINE)
d.comment(0x96b6, 'following character', align=Align.INLINE)
d.comment(0x96b8, "'('  -> string array", align=Align.INLINE)
d.comment(0x96ba, 'yes', align=Align.INLINE)
d.comment(0x96bc, 'Look the string variable up', align=Align.INLINE)
d.comment(0x96bf, 'not found: undefined', align=Align.INLINE)
d.comment(0x96c1, 'Update the scan offset', align=Align.INLINE)
d.comment(0x96c3, 'Type = string lvalue (&81)', align=Align.INLINE)
d.comment(0x96c5, '...', align=Align.INLINE)
d.comment(0x96c7, 'found: SEC', align=Align.INLINE)
d.comment(0x96c8, 'Return', align=Align.INLINE)
d.comment(0x96c9, 'String array: step past "("', align=Align.INLINE)
d.comment(0x96ca, 'record the name length', align=Align.INLINE)
d.comment(0x96cc, 'mark the type string', align=Align.INLINE)
d.comment(0x96ce, 'index the array', align=Align.INLINE)
d.comment(0x96d1, 'Type = string lvalue (&81)', align=Align.INLINE)
d.comment(0x96d3, '...', align=Align.INLINE)
d.comment(0x96d5, 'found: SEC', align=Align.INLINE)
d.comment(0x96d6, 'Return', align=Align.INLINE)
d.comment(0x96d7, 'No such array: Array error', align=Align.INLINE)

# index_array (&96DF): locate the array and step to one element.
d.comment(0x96df, 'Find the array', align=Align.INLINE)
d.comment(0x96e2, 'missing: Array error', align=Align.INLINE)
d.comment(0x96e4, 'Update the scan offset', align=Align.INLINE)
d.comment(0x96e6, 'Save the variable type...', align=Align.INLINE)
d.comment(0x96e8, '...', align=Align.INLINE)
d.comment(0x96e9, '...and the array data pointer', align=Align.INLINE)
d.comment(0x96eb, '...', align=Align.INLINE)
d.comment(0x96ec, '...', align=Align.INLINE)
d.comment(0x96ee, '...', align=Align.INLINE)
d.comment(0x96ef, 'Number of dimensions', align=Align.INLINE)
d.comment(0x96f1, '...', align=Align.INLINE)
d.comment(0x96f3, 'more than a few?', align=Align.INLINE)
d.comment(0x96f5, 'no: handle the small case', align=Align.INLINE)
d.comment(0x96f7, 'Accumulate the flattened index', align=Align.INLINE)
d.comment(0x96f8, '...', align=Align.INLINE)
d.comment(0x96fb, 'one subscript so far', align=Align.INLINE)
d.comment(0x96fd, '...', align=Align.INLINE)

# ----------------------------------------------------------------------
# Array element address (&96FF): evaluate the comma-separated subscripts
# and flatten them to a linear element offset by Horner's method
# (index = index * extent + subscript) with a bounds check per
# dimension, then scale by the element size (5 bytes real/string, 4
# integer) and add the array base, leaving the element address in &2A.
# ----------------------------------------------------------------------
d.comment(0x96ff, 'Stack the running index', align=Align.INLINE)
d.comment(0x9702, 'Evaluate the next subscript', align=Align.INLINE)
d.comment(0x9705, 'step past it', align=Align.INLINE)
d.comment(0x9707, "comma (another subscript)?", align=Align.INLINE)
d.comment(0x9709, 'no: wrong dimension count -> Array', align=Align.INLINE)
d.comment(0x970b, 'Unstack the running index', align=Align.INLINE)
d.comment(0x970d, '...', align=Align.INLINE)
d.comment(0x9710, 'dimension descriptor offset', align=Align.INLINE)
d.comment(0x9712, 'Recover the array base pointer', align=Align.INLINE)
d.comment(0x9713, '...', align=Align.INLINE)
d.comment(0x9715, '...', align=Align.INLINE)
d.comment(0x9716, '...', align=Align.INLINE)
d.comment(0x9718, 're-stack it', align=Align.INLINE)
d.comment(0x9719, '...', align=Align.INLINE)
d.comment(0x971b, '...', align=Align.INLINE)
d.comment(0x971c, 'Bounds-check this subscript', align=Align.INLINE)
d.comment(0x971f, 'advance to the next dimension', align=Align.INLINE)
d.comment(0x9721, "This dimension's extent: low", align=Align.INLINE)
d.comment(0x9723, '...', align=Align.INLINE)
d.comment(0x9725, '...high', align=Align.INLINE)
d.comment(0x9726, '...', align=Align.INLINE)
d.comment(0x9728, '...', align=Align.INLINE)
d.comment(0x972a, 'Add the subscript into the running index', align=Align.INLINE)
d.comment(0x972c, '...', align=Align.INLINE)
d.comment(0x972e, '...', align=Align.INLINE)
d.comment(0x9730, '...', align=Align.INLINE)
d.comment(0x9732, '...', align=Align.INLINE)
d.comment(0x9734, '...', align=Align.INLINE)
d.comment(0x9736, 'index *= this extent (Horner)', align=Align.INLINE)
d.comment(0x9739, 'Dimensions processed so far', align=Align.INLINE)
d.comment(0x973b, '...', align=Align.INLINE)
d.comment(0x973c, '...', align=Align.INLINE)
d.comment(0x973e, '...', align=Align.INLINE)
d.comment(0x9740, 'more dimensions to come?', align=Align.INLINE)
d.comment(0x9742, 'yes: next subscript', align=Align.INLINE)
d.comment(0x9744, 'Stack the running index', align=Align.INLINE)
d.comment(0x9747, 'Evaluate the final subscript', align=Align.INLINE)
d.comment(0x974a, '...as an integer', align=Align.INLINE)
d.comment(0x974d, 'Recover the array base', align=Align.INLINE)
d.comment(0x974e, '...', align=Align.INLINE)
d.comment(0x9750, '...', align=Align.INLINE)
d.comment(0x9751, '...', align=Align.INLINE)
d.comment(0x9753, 'Unstack the running index', align=Align.INLINE)
d.comment(0x9755, '...', align=Align.INLINE)
d.comment(0x9758, 'dimension descriptor offset', align=Align.INLINE)
d.comment(0x975a, 'Bounds-check the final subscript', align=Align.INLINE)
d.comment(0x975d, 'Add it into the index', align=Align.INLINE)
d.comment(0x975e, '...', align=Align.INLINE)
d.comment(0x9760, '...', align=Align.INLINE)
d.comment(0x9762, '...', align=Align.INLINE)
d.comment(0x9764, '...', align=Align.INLINE)
d.comment(0x9766, '...', align=Align.INLINE)
d.comment(0x9768, '...', align=Align.INLINE)
d.comment(0x976a, 'scale by the element size', align=Align.INLINE)
d.comment(0x976c, 'One subscript: evaluate it', align=Align.INLINE)
d.comment(0x976f, '...as an integer', align=Align.INLINE)
d.comment(0x9772, 'Recover the array base', align=Align.INLINE)
d.comment(0x9773, '...', align=Align.INLINE)
d.comment(0x9775, '...', align=Align.INLINE)
d.comment(0x9776, '...', align=Align.INLINE)
d.comment(0x9778, 'descriptor offset 1', align=Align.INLINE)
d.comment(0x977a, 'Bounds-check the subscript', align=Align.INLINE)
d.comment(0x977d, 'Element type', align=Align.INLINE)
d.comment(0x977e, '...', align=Align.INLINE)
d.comment(0x9780, 'real/string (5 bytes)?', align=Align.INLINE)
d.comment(0x9782, 'no: integer (4 bytes)', align=Align.INLINE)
d.comment(0x9784, 'index *= 5 (x*4 + x)', align=Align.INLINE)
d.comment(0x9786, '...', align=Align.INLINE)
d.comment(0x9788, '...', align=Align.INLINE)
d.comment(0x978a, '...', align=Align.INLINE)
d.comment(0x978c, '...', align=Align.INLINE)
d.comment(0x978e, '...', align=Align.INLINE)
d.comment(0x9790, '...', align=Align.INLINE)
d.comment(0x9792, '...', align=Align.INLINE)
d.comment(0x9794, '...', align=Align.INLINE)
d.comment(0x9795, '...', align=Align.INLINE)
d.comment(0x9797, '...', align=Align.INLINE)
d.comment(0x9799, '...', align=Align.INLINE)
d.comment(0x979b, 'index *= 4', align=Align.INLINE)
d.comment(0x979d, '...', align=Align.INLINE)
d.comment(0x979f, '...', align=Align.INLINE)
d.comment(0x97a1, '...', align=Align.INLINE)
d.comment(0x97a3, 'Add the element offset within the descriptor',
          align=Align.INLINE)
d.comment(0x97a4, '...', align=Align.INLINE)
d.comment(0x97a6, '...', align=Align.INLINE)
d.comment(0x97a8, '...', align=Align.INLINE)
d.comment(0x97aa, '...', align=Align.INLINE)
d.comment(0x97ac, '...', align=Align.INLINE)
d.comment(0x97ad, 'Element address = base + offset', align=Align.INLINE)
d.comment(0x97af, '...', align=Align.INLINE)
d.comment(0x97b1, '...', align=Align.INLINE)
d.comment(0x97b3, '...', align=Align.INLINE)
d.comment(0x97b5, '...', align=Align.INLINE)
d.comment(0x97b7, '...', align=Align.INLINE)
d.comment(0x97b9, 'Return', align=Align.INLINE)

# check_subscript_bound (&97BA): Subscript error if out of range.
d.comment(0x97ba, 'Top bits of the subscript', align=Align.INLINE)
d.comment(0x97bc, 'keep just bits 6-7', align=Align.INLINE)
d.comment(0x97be, 'combine with the high bytes...', align=Align.INLINE)
d.comment(0x97c0, '...', align=Align.INLINE)
d.comment(0x97c2, 'negative or huge: Subscript', align=Align.INLINE)
d.comment(0x97c4, 'Compare against the dimension extent', align=Align.INLINE)
d.comment(0x97c6, 'subscript low vs extent low', align=Align.INLINE)
d.comment(0x97c8, 'next extent byte', align=Align.INLINE)
d.comment(0x97c9, 'subscript high...', align=Align.INLINE)
d.comment(0x97cb, 'minus the extent high', align=Align.INLINE)
d.comment(0x97cd, 'not less than the extent: Subscript', align=Align.INLINE)
d.comment(0x97cf, 'advance past the extent', align=Align.INLINE)
d.comment(0x97d0, 'Return', align=Align.INLINE)
d.comment(0x97d1, 'Subscript error', align=Align.INLINE)

# ======================================================================
# Inline 6502 assembler - operand and addressing-mode parser.
# Reached once a mnemonic has matched: X is the opcode's table index and
# selects which addressing modes are legal. The base opcode is in &29;
# each recognised mode adds 4/8/16 to it and sets Y to the instruction
# length, then jumps to the store loop (&862B) which writes the bytes
# to P% (and O% during offset assembly).
# ======================================================================
# opcode_found (&8620): start assembling the matched opcode.
d.comment(0x8620, 'Base opcode from the table', align=Align.INLINE)
d.comment(0x8623, 'Save it', align=Align.INLINE)
d.comment(0x8625, 'Assume a one-byte instruction', align=Align.INLINE)
d.comment(0x8627, 'index &1A+ takes an operand?', align=Align.INLINE)
d.comment(0x8629, 'yes: parse the addressing mode', align=Align.INLINE)
# Store loop (&862B): write the assembled bytes to P%/O%.
d.comment(0x862b, "P% low -> destination", align=Align.INLINE)
d.comment(0x862e, '...', align=Align.INLINE)
d.comment(0x8630, 'Save the byte count', align=Align.INLINE)
d.comment(0x8632, 'OPT setting', align=Align.INLINE)
d.comment(0x8634, 'offset assembly (OPT >= 4)?', align=Align.INLINE)
d.comment(0x8636, 'P% high', align=Align.INLINE)
d.comment(0x8639, '...', align=Align.INLINE)
d.comment(0x863b, 'no offset: assemble at P%', align=Align.INLINE)
d.comment(0x863d, 'offset: assemble at O% instead', align=Align.INLINE)
d.comment(0x8640, '...', align=Align.INLINE)
d.comment(0x8643, 'Store the destination pointer', align=Align.INLINE)
d.comment(0x8645, '...', align=Align.INLINE)
d.comment(0x8647, 'Any bytes to store?', align=Align.INLINE)
d.comment(0x8648, 'none: done', align=Align.INLINE)
d.comment(0x864a, 'positive count: store opcode bytes', align=Align.INLINE)
d.comment(0x864c, 'EQUS: length from the string buffer', align=Align.INLINE)
d.comment(0x864e, 'empty: done', align=Align.INLINE)
d.comment(0x8650, 'Next byte index', align=Align.INLINE)
d.comment(0x8651, 'Opcode/operand byte', align=Align.INLINE)
d.comment(0x8654, 'storing string (EQUS) bytes?', align=Align.INLINE)
d.comment(0x8656, 'no: store the opcode byte', align=Align.INLINE)
d.comment(0x8658, 'yes: take it from the string buffer', align=Align.INLINE)
d.comment(0x865b, 'Store the byte at the destination', align=Align.INLINE)
d.comment(0x865d, 'Advance P%', align=Align.INLINE)
d.comment(0x8660, '...', align=Align.INLINE)
d.comment(0x8662, '...', align=Align.INLINE)
d.comment(0x8665, 'offset assembly?', align=Align.INLINE)
d.comment(0x8667, 'yes: advance O% too', align=Align.INLINE)
d.comment(0x866a, '...', align=Align.INLINE)
d.comment(0x866c, '...', align=Align.INLINE)
d.comment(0x866f, 'More bytes?', align=Align.INLINE)
d.comment(0x8670, 'loop', align=Align.INLINE)
d.comment(0x8672, 'Return', align=Align.INLINE)
# Branch operand (&8673): relative branch, range-checked.
d.comment(0x8673, 'index &22+ is not a branch?', align=Align.INLINE)
d.comment(0x8675, 'yes: other operand forms', align=Align.INLINE)
d.comment(0x8677, 'Evaluate the target address', align=Align.INLINE)
d.comment(0x867a, 'Offset = target - (P% + 2)', align=Align.INLINE)
d.comment(0x867b, '...', align=Align.INLINE)
d.comment(0x867d, '...', align=Align.INLINE)
d.comment(0x8680, '...', align=Align.INLINE)
d.comment(0x8681, '...', align=Align.INLINE)
d.comment(0x8683, '...', align=Align.INLINE)
d.comment(0x8686, '...', align=Align.INLINE)
d.comment(0x8688, '...', align=Align.INLINE)
d.comment(0x8689, '...', align=Align.INLINE)
d.comment(0x868b, 'in forward range?', align=Align.INLINE)
d.comment(0x868d, 'in backward range?', align=Align.INLINE)
d.comment(0x868f, '...', align=Align.INLINE)
d.comment(0x8691, 'OPT setting', align=Align.INLINE)
d.comment(0x8692, 'errors enabled?', align=Align.INLINE)
d.comment(0x8693, '...', align=Align.INLINE)
d.comment(0x8694, 'no: ignore the range error', align=Align.INLINE)
d.comment(0x8696, 'Out of range error', align=Align.INLINE)
d.comment(0x86a5, 'Use the offset byte', align=Align.INLINE)
d.comment(0x86a6, 'as the operand', align=Align.INLINE)
d.comment(0x86a8, 'Two-byte instruction', align=Align.INLINE)
d.comment(0x86aa, 'store it', align=Align.INLINE)
d.comment(0x86ad, 'forward: check the high byte', align=Align.INLINE)
d.comment(0x86ae, 'in range', align=Align.INLINE)
d.comment(0x86b0, 'out of range', align=Align.INLINE)
d.comment(0x86b2, 'backward: check the high byte', align=Align.INLINE)
d.comment(0x86b3, 'in range', align=Align.INLINE)
d.comment(0x86b5, 'out of range', align=Align.INLINE)
# Immediate operand (&86B7).
d.comment(0x86b7, "index &29+ : not immediate?", align=Align.INLINE)
d.comment(0x86b9, 'yes: indexed/absolute modes', align=Align.INLINE)
d.comment(0x86be, "'#' immediate prefix?", align=Align.INLINE)
d.comment(0x86c0, 'no: absolute', align=Align.INLINE)
d.comment(0x86c2, 'Immediate mode: adjust the opcode', align=Align.INLINE)
d.comment(0x86c5, 'Evaluate the immediate value', align=Align.INLINE)
d.comment(0x86c8, 'high byte zero (fits in a byte)?', align=Align.INLINE)
d.comment(0x86ca, 'yes: two-byte instruction', align=Align.INLINE)
d.comment(0x86cc, 'Byte error (value > 255)', align=Align.INLINE)
# (zp),Y and (zp,X) parsers (&86D3).
d.comment(0x86d3, 'index &36 : the (zp),Y / (zp,X) group?', align=Align.INLINE)
d.comment(0x86d5, 'no: absolute/indexed group', align=Align.INLINE)
d.comment(0x86da, "'(' opening an indirect mode?", align=Align.INLINE)
d.comment(0x86dc, 'no: absolute', align=Align.INLINE)
d.comment(0x86de, 'Evaluate the zero-page address', align=Align.INLINE)
d.comment(0x86e4, "')' -> (zp),Y form", align=Align.INLINE)
d.comment(0x86e6, "no: try (zp,X)", align=Align.INLINE)
d.comment(0x86ef, 'adjust the opcode for (zp),Y', align=Align.INLINE)
d.comment(0x86f9, 'process as a two-byte instruction', align=Align.INLINE)
d.comment(0x870d, 'Index error', align=Align.INLINE)
d.comment(0x8715, 'Back up over the "("', align=Align.INLINE)
d.comment(0x8717, 'Evaluate the address', align=Align.INLINE)
d.comment(0x8721, 'adjust the opcode for absolute,X/,Y', align=Align.INLINE)
d.comment(0x872f, 'Adjust the opcode for the indexed form', align=Align.INLINE)
d.comment(0x8732, 'process the absolute operand', align=Align.INLINE)
# abs / abs,X (&8735).
d.comment(0x8735, 'Adjust the opcode for absolute mode', align=Align.INLINE)
d.comment(0x8738, 'address fits in zero page (high byte 0)?',
          align=Align.INLINE)
d.comment(0x873a, 'no: assemble as absolute (three bytes)', align=Align.INLINE)
d.comment(0x873c, 'yes: assemble as two bytes', align=Align.INLINE)
# Addressing-mode dispatch by opcode class (&873F).
d.comment(0x873f, 'index &2F+ : a different operand class?', align=Align.INLINE)
d.comment(0x8741, 'yes', align=Align.INLINE)
d.comment(0x8743, 'index &2D+ (accumulator-or-absolute)?', align=Align.INLINE)
d.comment(0x8745, 'yes', align=Align.INLINE)
d.comment(0x874e, 'Back up a character', align=Align.INLINE)
d.comment(0x8750, 'Evaluate the address', align=Align.INLINE)
d.comment(0x875a, 'adjust the opcode for indexed mode', align=Align.INLINE)
d.comment(0x8767, 'Accumulator form: adjust the opcode', align=Align.INLINE)
d.comment(0x876a, 'one byte', align=Align.INLINE)
d.comment(0x876c, 'store it', align=Align.INLINE)
d.comment(0x876e, 'index &32+ : implied/branch class?', align=Align.INLINE)
d.comment(0x8770, 'yes', align=Align.INLINE)
d.comment(0x8772, 'index &31 (immediate-only)?', align=Align.INLINE)
d.comment(0x8774, 'yes', align=Align.INLINE)
d.comment(0x8780, 'Back up a character', align=Align.INLINE)
d.comment(0x8782, 'Evaluate the value', align=Align.INLINE)
d.comment(0x8785, 'assemble as absolute', align=Align.INLINE)
d.comment(0x8788, 'index &33 (no operand)?', align=Align.INLINE)
d.comment(0x878a, 'yes', align=Align.INLINE)
d.comment(0x878c, 'index &34+ : other forms', align=Align.INLINE)
d.comment(0x8795, 'Back up a character', align=Align.INLINE)
d.comment(0x8797, 'Evaluate the address', align=Align.INLINE)
d.comment(0x879a, 'Three-byte instruction', align=Align.INLINE)
d.comment(0x879c, 'store it', align=Align.INLINE)
d.comment(0x879f, 'Indirect: adjust the opcode', align=Align.INLINE)
d.comment(0x87a2, '...', align=Align.INLINE)
d.comment(0x87a5, 'evaluate the address', align=Align.INLINE)
d.comment(0x87ab, "')' to close?", align=Align.INLINE)
d.comment(0x87ad, 'yes: three-byte instruction', align=Align.INLINE)
d.comment(0x87b2, 'index &39+ : EQU directives', align=Align.INLINE)
d.comment(0x87b4, 'yes', align=Align.INLINE)
d.comment(0x87b6, 'Register letter from the mnemonic', align=Align.INLINE)
d.comment(0x87b7, '...', align=Align.INLINE)
d.comment(0x87b9, '...', align=Align.INLINE)
d.comment(0x87ba, 'save it', align=Align.INLINE)
d.comment(0x87bb, 'index &37+ (two-register form)?', align=Align.INLINE)
d.comment(0x87bd, 'yes', align=Align.INLINE)
d.comment(0x87c2, "'#' immediate?", align=Align.INLINE)
d.comment(0x87c4, 'no: absolute', align=Align.INLINE)
d.comment(0x87c6, 'discard the saved register, do immediate', align=Align.INLINE)
d.comment(0x87cc, 'Back up a character', align=Align.INLINE)
d.comment(0x87ce, 'Evaluate the address', align=Align.INLINE)
d.comment(0x87d1, 'recover the register letter', align=Align.INLINE)
d.comment(0x87d3, '...', align=Align.INLINE)
d.comment(0x87d6, "',' index register?", align=Align.INLINE)
d.comment(0x87d8, 'yes', align=Align.INLINE)
d.comment(0x87da, 'no: assemble as absolute', align=Align.INLINE)
d.comment(0x87de, 'Index register letter', align=Align.INLINE)
d.comment(0x87e0, '...', align=Align.INLINE)
d.comment(0x87e2, 'matches the expected register?', align=Align.INLINE)
d.comment(0x87e4, 'no: Index error', align=Align.INLINE)
d.comment(0x87e7, 'adjust the opcode for the indexed form',
          align=Align.INLINE)
d.comment(0x87ea, 'assemble as absolute', align=Align.INLINE)
d.comment(0x87ed, 'Index error', align=Align.INLINE)
d.comment(0x87f0, 'Evaluate the address', align=Align.INLINE)
d.comment(0x87f3, 'recover the register letter', align=Align.INLINE)
d.comment(0x87f5, '...', align=Align.INLINE)
d.comment(0x87f8, "',' index register?", align=Align.INLINE)
d.comment(0x87fa, 'no: single operand', align=Align.INLINE)
d.comment(0x87fc, 'Index register letter', align=Align.INLINE)
d.comment(0x87fe, '...', align=Align.INLINE)
d.comment(0x8800, 'matches?', align=Align.INLINE)
d.comment(0x8802, 'no: Index error', align=Align.INLINE)
d.comment(0x8804, 'adjust the opcode for indexed mode', align=Align.INLINE)
d.comment(0x8807, 'high byte zero?', align=Align.INLINE)
d.comment(0x8809, 'yes: continue', align=Align.INLINE)
d.comment(0x880b, 'Byte error (value > 255)', align=Align.INLINE)
d.comment(0x8810, 'Assemble as zero-page', align=Align.INLINE)
d.comment(0x8813, 'index &39 (OPT)?', align=Align.INLINE)
d.comment(0x8815, 'no: EQU directives', align=Align.INLINE)
d.comment(0x8817, 'OPT: evaluate the new setting', align=Align.INLINE)
d.comment(0x881a, 'store it as the OPT flag', align=Align.INLINE)
d.comment(0x881c, 'no bytes to assemble', align=Align.INLINE)
d.comment(0x881e, 'finish', align=Align.INLINE)

# eval_expr_to_integer (&8821): inline body.
d.comment(0x8821, 'Evaluate the expression', align=Align.INLINE)
d.comment(0x8824, 'coerce to an integer', align=Align.INLINE)
d.comment(0x8827, 'Sync the primary text offset', align=Align.INLINE)
d.comment(0x8829, '...', align=Align.INLINE)
d.comment(0x882b, 'Return', align=Align.INLINE)
# Opcode addressing-mode adjusters.
d.comment(0x882c, 'add 8 then fall through (+16 total)', align=Align.INLINE)
d.comment(0x882f, 'add 4 then fall through (+8 total)', align=Align.INLINE)
d.comment(0x8832, 'Opcode += 4 (next addressing-mode column)',
          align=Align.INLINE)
d.comment(0x8834, '...', align=Align.INLINE)
d.comment(0x8835, '...', align=Align.INLINE)
d.comment(0x8837, '...', align=Align.INLINE)
d.comment(0x8839, 'Return', align=Align.INLINE)

# EQUB/EQUW/EQUD/EQUS directives (&883A).
d.comment(0x883a, 'Assume one byte (EQUB)', align=Align.INLINE)
d.comment(0x883c, 'Next character of the directive', align=Align.INLINE)
d.comment(0x883e, '...', align=Align.INLINE)
d.comment(0x883f, '...', align=Align.INLINE)
d.comment(0x8841, "'B' (EQUB)?", align=Align.INLINE)
d.comment(0x8843, 'yes', align=Align.INLINE)
d.comment(0x8844, 'two bytes (EQUW)', align=Align.INLINE)
d.comment(0x8845, "'W' (EQUW)?", align=Align.INLINE)
d.comment(0x8847, 'yes', align=Align.INLINE)
d.comment(0x8849, 'four bytes (EQUD)', align=Align.INLINE)
d.comment(0x884b, "'D' (EQUD)?", align=Align.INLINE)
d.comment(0x884d, 'yes', align=Align.INLINE)
d.comment(0x884f, "'S' (EQUS)?", align=Align.INLINE)
d.comment(0x8851, 'yes', align=Align.INLINE)
d.comment(0x8853, 'none: Mistake (syntax error)', align=Align.INLINE)
d.comment(0x8858, 'Save the byte count', align=Align.INLINE)
d.comment(0x8859, '...', align=Align.INLINE)
d.comment(0x885a, 'Evaluate the value', align=Align.INLINE)
d.comment(0x885d, 'Store it into the opcode bytes', align=Align.INLINE)
d.comment(0x885f, '...', align=Align.INLINE)
d.comment(0x8862, 'recover the byte count', align=Align.INLINE)
d.comment(0x8863, '...', align=Align.INLINE)
d.comment(0x8864, 'Assemble the bytes', align=Align.INLINE)
d.comment(0x8867, 'String expected: Type mismatch', align=Align.INLINE)
d.comment(0x886a, 'EQUS: save the OPT flag', align=Align.INLINE)
d.comment(0x886b, '...', align=Align.INLINE)
d.comment(0x886c, 'evaluate the string expression', align=Align.INLINE)
d.comment(0x886f, 'not a string: Type mismatch', align=Align.INLINE)
d.comment(0x8871, 'restore the OPT flag', align=Align.INLINE)
d.comment(0x8873, '...', align=Align.INLINE)
d.comment(0x8875, 'sync the text offset', align=Align.INLINE)
d.comment(0x8878, 'flag EQUS (length from the string buffer)',
          align=Align.INLINE)
d.comment(0x887a, 'assemble the string bytes', align=Align.INLINE)

# sub_c887c (&887C): shift bytes up to make room / move a line tail.
d.comment(0x887c, 'Save the byte to insert', align=Align.INLINE)
d.comment(0x887d, 'Source = dest + Y', align=Align.INLINE)
d.comment(0x887e, '...', align=Align.INLINE)
d.comment(0x887f, '...', align=Align.INLINE)
d.comment(0x8881, '...', align=Align.INLINE)
d.comment(0x8883, '...', align=Align.INLINE)
d.comment(0x8885, '...', align=Align.INLINE)
d.comment(0x8886, '...', align=Align.INLINE)
d.comment(0x8888, '...', align=Align.INLINE)
d.comment(0x888a, 'Store the inserted byte', align=Align.INLINE)
d.comment(0x888d, 'Copy the rest of the line up', align=Align.INLINE)
d.comment(0x888e, '...', align=Align.INLINE)
d.comment(0x8890, '...', align=Align.INLINE)
d.comment(0x8892, 'until the carriage return', align=Align.INLINE)
d.comment(0x8894, '...', align=Align.INLINE)
d.comment(0x8896, 'Return', align=Align.INLINE)

# eval_factor (&ADEC): expression Level 1 - the atom.
d.comment(0xadec, 'Next character', align=Align.INLINE)
d.comment(0xadee, '...', align=Align.INLINE)
d.comment(0xadf0, '...', align=Align.INLINE)
d.comment(0xadf2, 'space?', align=Align.INLINE)
d.comment(0xadf4, 'skip it', align=Align.INLINE)
d.comment(0xadf6, "'-' unary minus?", align=Align.INLINE)
d.comment(0xadf8, 'yes', align=Align.INLINE)
d.comment(0xadfa, "'\"' string literal?", align=Align.INLINE)
d.comment(0xadfc, 'yes', align=Align.INLINE)
d.comment(0xadfe, "'+' unary plus?", align=Align.INLINE)
d.comment(0xae00, 'no: classify the token', align=Align.INLINE)
d.comment(0xae02, 'unary plus: re-read the next character', align=Align.INLINE)
d.comment(0xae05, 'below the lowest function token?', align=Align.INLINE)
d.comment(0xae07, 'yes: indirection, number or variable', align=Align.INLINE)
d.comment(0xae09, 'above the highest function token?', align=Align.INLINE)
d.comment(0xae0b, 'yes: No such variable', align=Align.INLINE)
d.comment(0xae0d, 'a function: dispatch it', align=Align.INLINE)
d.comment(0xae10, "'?' (byte indirection) or higher?", align=Align.INLINE)
d.comment(0xae12, 'yes: variable or indirection', align=Align.INLINE)
d.comment(0xae14, "'.' or a digit?", align=Align.INLINE)
d.comment(0xae16, 'yes: a number', align=Align.INLINE)
d.comment(0xae18, "'&' hex number?", align=Align.INLINE)
d.comment(0xae1a, 'yes', align=Align.INLINE)
d.comment(0xae1c, "'(' sub-expression?", align=Align.INLINE)
d.comment(0xae1e, 'yes', align=Align.INLINE)
d.comment(0xae20, 'Back up to the name', align=Align.INLINE)
d.comment(0xae22, 'Parse the variable reference', align=Align.INLINE)
d.comment(0xae25, 'undefined: handle below', align=Align.INLINE)
d.comment(0xae27, 'load the variable value', align=Align.INLINE)
d.comment(0xae2a, 'Parse the decimal number', align=Align.INLINE)
d.comment(0xae2d, 'ok', align=Align.INLINE)
d.comment(0xae2e, 'Return', align=Align.INLINE)
d.comment(0xae30, 'Undefined: OPT flag', align=Align.INLINE)
d.comment(0xae32, 'ignore-undefined set?', align=Align.INLINE)
d.comment(0xae34, 'no: No such variable', align=Align.INLINE)
d.comment(0xae36, 'bad name: No such variable', align=Align.INLINE)
d.comment(0xae38, 'accept; advance the offset', align=Align.INLINE)
d.comment(0xae3a, 'Use P% as the value', align=Align.INLINE)
d.comment(0xae3d, '...', align=Align.INLINE)
d.comment(0xae3f, 'return it as an integer', align=Align.INLINE)
d.comment(0xae43, 'No such variable error', align=Align.INLINE)
d.comment(0xae56, 'Sub-expression: evaluate it', align=Align.INLINE)
d.comment(0xae59, 'step past', align=Align.INLINE)
d.comment(0xae5b, "')' to close?", align=Align.INLINE)
d.comment(0xae5d, 'no: Missing )', align=Align.INLINE)
d.comment(0xae5f, 'flag the result type', align=Align.INLINE)
d.comment(0xae60, 'Return', align=Align.INLINE)
d.comment(0xae61, 'Missing ) error', align=Align.INLINE)
d.comment(0xae6d, 'Hex number: clear IWA', align=Align.INLINE)
d.comment(0xae6f, '...', align=Align.INLINE)
d.comment(0xae71, '...', align=Align.INLINE)
d.comment(0xae73, '...', align=Align.INLINE)
d.comment(0xae75, '...', align=Align.INLINE)
d.comment(0xae77, 'scan offset', align=Align.INLINE)
d.comment(0xae79, 'Next character', align=Align.INLINE)
d.comment(0xae7b, "below '0'?", align=Align.INLINE)
d.comment(0xae7d, 'yes: end of number', align=Align.INLINE)
d.comment(0xae7f, 'a digit 0-9?', align=Align.INLINE)
d.comment(0xae81, 'yes', align=Align.INLINE)
d.comment(0xae83, "fold A-F to 10-15", align=Align.INLINE)
d.comment(0xae85, 'below 10 (a gap char)?', align=Align.INLINE)
d.comment(0xae87, 'yes: end of number', align=Align.INLINE)
d.comment(0xae89, 'above F?', align=Align.INLINE)
d.comment(0xae8b, 'yes: end of number', align=Align.INLINE)
d.comment(0xae8d, 'Shift the digit into the high nibble', align=Align.INLINE)
d.comment(0xae8e, '...', align=Align.INLINE)
d.comment(0xae8f, '...', align=Align.INLINE)
d.comment(0xae90, '...', align=Align.INLINE)
d.comment(0xae91, 'four bits to shift', align=Align.INLINE)
d.comment(0xae93, 'Shift one bit into IWA', align=Align.INLINE)
d.comment(0xae94, '...', align=Align.INLINE)
d.comment(0xae96, '...', align=Align.INLINE)
d.comment(0xae98, '...', align=Align.INLINE)
d.comment(0xae9a, '...', align=Align.INLINE)
d.comment(0xae9c, '...', align=Align.INLINE)
d.comment(0xae9d, 'next bit', align=Align.INLINE)
d.comment(0xae9f, 'advance', align=Align.INLINE)
d.comment(0xaea0, 'next digit', align=Align.INLINE)
d.comment(0xaea2, 'Any digits seen?', align=Align.INLINE)
d.comment(0xaea3, 'no: Bad HEX', align=Align.INLINE)
d.comment(0xaea5, 'Save the offset', align=Align.INLINE)
d.comment(0xaea7, 'Type = integer', align=Align.INLINE)
d.comment(0xaea9, 'Return', align=Align.INLINE)
d.comment(0xaeaa, 'Bad HEX error', align=Align.INLINE)

# eval_or_eor (&9B29): expression Level 7 - bitwise OR and EOR.
d.comment(0x9b2e, 'yes', align=Align.INLINE)
d.comment(0x9b30, 'EOR token?', align=Align.INLINE)
d.comment(0x9b32, 'yes', align=Align.INLINE)
d.comment(0x9b34, 'neither: back up over the token', align=Align.INLINE)
d.comment(0x9b36, 'set the result-type flags', align=Align.INLINE)
d.comment(0x9b37, '...', align=Align.INLINE)
d.comment(0x9b39, 'Return', align=Align.INLINE)
d.comment(0x9b3d, 'ensure the right operand is integer', align=Align.INLINE)
d.comment(0x9b3e, '...', align=Align.INLINE)
d.comment(0x9b41, 'Four bytes', align=Align.INLINE)
d.comment(0x9b45, 'OR with IWA', align=Align.INLINE)
d.comment(0x9b48, 'store back', align=Align.INLINE)
d.comment(0x9b4b, 'next byte', align=Align.INLINE)
d.comment(0x9b4c, '...', align=Align.INLINE)
d.comment(0x9b4e, 'Drop the stacked operand', align=Align.INLINE)
d.comment(0x9b51, 'Result type = integer', align=Align.INLINE)
d.comment(0x9b55, 'EOR: stack the left operand, evaluate the right',
          align=Align.INLINE)
d.comment(0x9b58, 'ensure the right operand is integer', align=Align.INLINE)
d.comment(0x9b59, '...', align=Align.INLINE)
d.comment(0x9b5c, 'Four bytes', align=Align.INLINE)
d.comment(0x9b5e, 'stacked byte', align=Align.INLINE)
d.comment(0x9b60, 'EOR with IWA', align=Align.INLINE)
d.comment(0x9b63, 'store back', align=Align.INLINE)
d.comment(0x9b66, 'next byte', align=Align.INLINE)
d.comment(0x9b67, '...', align=Align.INLINE)
d.comment(0x9b69, 'drop and loop', align=Align.INLINE)
# sub_c9b6b: coerce, stack, then evaluate the next operand.
d.comment(0x9b6b, 'Coerce the left operand to integer', align=Align.INLINE)
d.comment(0x9b6c, '...', align=Align.INLINE)
d.comment(0x9b6f, 'stack it', align=Align.INLINE)
# eval_and (&9B72): expression Level 6 - bitwise AND.
d.comment(0x9b72, 'Evaluate a relational operand', align=Align.INLINE)
d.comment(0x9b77, 'yes', align=Align.INLINE)
d.comment(0x9b79, 'no: return', align=Align.INLINE)
d.comment(0x9b7a, 'Coerce the left operand to integer', align=Align.INLINE)
d.comment(0x9b7b, '...', align=Align.INLINE)
d.comment(0x9b7e, 'stack it', align=Align.INLINE)
d.comment(0x9b81, 'evaluate the right operand', align=Align.INLINE)
d.comment(0x9b84, 'ensure it is integer', align=Align.INLINE)
d.comment(0x9b85, '...', align=Align.INLINE)
d.comment(0x9b88, 'Four bytes', align=Align.INLINE)
d.comment(0x9b8a, 'stacked byte', align=Align.INLINE)
d.comment(0x9b8c, 'AND with IWA', align=Align.INLINE)
d.comment(0x9b8f, 'store back', align=Align.INLINE)
d.comment(0x9b92, 'next byte', align=Align.INLINE)
d.comment(0x9b93, '...', align=Align.INLINE)
d.comment(0x9b95, 'Drop the stacked operand', align=Align.INLINE)
d.comment(0x9b98, 'Result type = integer', align=Align.INLINE)
d.comment(0x9b9a, 'loop for further AND', align=Align.INLINE)

# check_end_of_statement (&9857): require ':', end-of-line or ELSE.
d.comment(0x9857, 'Program pointer offset', align=Align.INLINE)
d.comment(0x9859, 'step back', align=Align.INLINE)
d.comment(0x985a, 'Next character', align=Align.INLINE)
d.comment(0x985b, '...', align=Align.INLINE)
d.comment(0x985d, 'space?', align=Align.INLINE)
d.comment(0x985f, 'skip it', align=Align.INLINE)
d.comment(0x9861, "':' statement separator?", align=Align.INLINE)
d.comment(0x9863, 'yes', align=Align.INLINE)
d.comment(0x9865, 'end of line?', align=Align.INLINE)
d.comment(0x9867, 'yes', align=Align.INLINE)
d.comment(0x9869, 'ELSE token?', align=Align.INLINE)
d.comment(0x986b, 'none: Mistake (syntax error)', align=Align.INLINE)
d.comment(0x986d, 'Advance the program pointer past the statement',
          align=Align.INLINE)
d.comment(0x986e, '...', align=Align.INLINE)
d.comment(0x986f, '...', align=Align.INLINE)
d.comment(0x9871, '...', align=Align.INLINE)
d.comment(0x9873, '...', align=Align.INLINE)
d.comment(0x9875, '...', align=Align.INLINE)
d.comment(0x9877, 'Reset the offset to 1', align=Align.INLINE)
d.comment(0x9879, '...', align=Align.INLINE)
d.comment(0x987b, 'Escape pressed (ESCFLG)?', align=Align.INLINE)
d.comment(0x987d, 'yes: raise Escape', align=Align.INLINE)
d.comment(0x987f, 'Return', align=Align.INLINE)

# step_statement (&9880): advance to the next statement, with TRACE.
d.comment(0x9880, 'Check this statement is terminated', align=Align.INLINE)
d.comment(0x9883, 'Re-read the terminator', align=Align.INLINE)
d.comment(0x9884, '...', align=Align.INLINE)
d.comment(0x9886, "':' (more on this line)?", align=Align.INLINE)
d.comment(0x9888, 'yes: continue on the line', align=Align.INLINE)
d.comment(0x988a, 'At the end of program memory?', align=Align.INLINE)
d.comment(0x988c, '...', align=Align.INLINE)
d.comment(0x988e, 'yes: return to immediate mode', align=Align.INLINE)
d.comment(0x9890, 'Next byte (line-number marker)', align=Align.INLINE)
d.comment(0x9891, '...', align=Align.INLINE)
d.comment(0x9893, 'end of program: immediate mode', align=Align.INLINE)
d.comment(0x9895, 'TRACE on?', align=Align.INLINE)
d.comment(0x9897, 'no: skip the line number', align=Align.INLINE)
d.comment(0x9899, 'Save the offset', align=Align.INLINE)
d.comment(0x989a, '...', align=Align.INLINE)
d.comment(0x989b, 'Line number high byte', align=Align.INLINE)
d.comment(0x989c, '...', align=Align.INLINE)
d.comment(0x989e, '...', align=Align.INLINE)
d.comment(0x989f, 'Line number low byte', align=Align.INLINE)
d.comment(0x98a0, '...', align=Align.INLINE)
d.comment(0x98a2, '...', align=Align.INLINE)
d.comment(0x98a3, '...', align=Align.INLINE)
d.comment(0x98a4, 'IWA = line number', align=Align.INLINE)
d.comment(0x98a7, 'trace it', align=Align.INLINE)
d.comment(0x98aa, 'Restore the offset', align=Align.INLINE)
d.comment(0x98ab, '...', align=Align.INLINE)
d.comment(0x98ac, 'Step past the 3-byte line header', align=Align.INLINE)
d.comment(0x98ad, '...', align=Align.INLINE)
d.comment(0x98ae, '...', align=Align.INLINE)
d.comment(0x98af, '...', align=Align.INLINE)
d.comment(0x98b1, '...', align=Align.INLINE)
d.comment(0x98b3, '...', align=Align.INLINE)
d.comment(0x98b5, '...', align=Align.INLINE)
d.comment(0x98b7, 'Reset the offset to 1', align=Align.INLINE)
d.comment(0x98b9, '...', align=Align.INLINE)
d.comment(0x98bb, 'Return', align=Align.INLINE)
d.comment(0x98bc, 'End of program: immediate mode', align=Align.INLINE)
d.comment(0x98bf, 'Type mismatch error', align=Align.INLINE)

# trace_line (&9905): print [line] when within the TRACE ceiling.
d.comment(0x9905, 'Line number vs TRACE ceiling', align=Align.INLINE)
d.comment(0x9907, '...', align=Align.INLINE)
d.comment(0x9909, '...', align=Align.INLINE)
d.comment(0x990b, '...', align=Align.INLINE)
d.comment(0x990d, 'above the ceiling: do not trace', align=Align.INLINE)
d.comment(0x990f, "Print '['", align=Align.INLINE)
d.comment(0x9911, '...', align=Align.INLINE)
d.comment(0x9914, 'print the line number', align=Align.INLINE)
d.comment(0x9917, "Print ']'", align=Align.INLINE)
d.comment(0x9919, '...', align=Align.INLINE)
d.comment(0x991c, 'and a space', align=Align.INLINE)

# print_line_number (&991F): IWA -> decimal.
d.comment(0x991f, 'Default: no field padding', align=Align.INLINE)
d.comment(0x9921, '...', align=Align.INLINE)
d.comment(0x9923, 'TRACE entry: 5-digit field', align=Align.INLINE)
d.comment(0x9925, 'Field width', align=Align.INLINE)
d.comment(0x9927, 'Five powers of ten, index 4..0', align=Align.INLINE)
d.comment(0x9929, 'Clear this digit', align=Align.INLINE)
d.comment(0x992b, '...', align=Align.INLINE)
d.comment(0x992e, 'Subtract this power of ten from IWA', align=Align.INLINE)
d.comment(0x9930, '...', align=Align.INLINE)
d.comment(0x9933, '...', align=Align.INLINE)
d.comment(0x9934, '...', align=Align.INLINE)
d.comment(0x9936, '...', align=Align.INLINE)
d.comment(0x9939, 'underflow: digit complete', align=Align.INLINE)
d.comment(0x993b, 'keep the remainder', align=Align.INLINE)
d.comment(0x993d, '...', align=Align.INLINE)
d.comment(0x993f, 'count the digit', align=Align.INLINE)
d.comment(0x9941, 'subtract again', align=Align.INLINE)
d.comment(0x9943, 'Next power of ten', align=Align.INLINE)
d.comment(0x9944, '...', align=Align.INLINE)
d.comment(0x9946, 'Find the most significant non-zero digit',
          align=Align.INLINE)
d.comment(0x9948, '...', align=Align.INLINE)
d.comment(0x9949, '...', align=Align.INLINE)
d.comment(0x994b, '...', align=Align.INLINE)
d.comment(0x994d, '...', align=Align.INLINE)
d.comment(0x994f, 'Index of the top digit', align=Align.INLINE)
d.comment(0x9951, 'Field padding requested?', align=Align.INLINE)
d.comment(0x9953, 'no', align=Align.INLINE)
d.comment(0x9955, 'leading spaces = field - digits', align=Align.INLINE)
d.comment(0x9957, 'none', align=Align.INLINE)
d.comment(0x9959, '...', align=Align.INLINE)
d.comment(0x995a, 'print a leading space', align=Align.INLINE)
d.comment(0x995d, '...', align=Align.INLINE)
d.comment(0x995e, '...', align=Align.INLINE)
d.comment(0x9960, 'Digit', align=Align.INLINE)
d.comment(0x9962, 'to ASCII', align=Align.INLINE)
d.comment(0x9964, 'print it', align=Align.INLINE)
d.comment(0x9967, 'next digit', align=Align.INLINE)
d.comment(0x9968, '...', align=Align.INLINE)
d.comment(0x996a, 'Return', align=Align.INLINE)

# iwa_divide (&99BE): shift-subtract 32-bit integer division.
d.comment(0x99be, 'Coerce the divisor to integer', align=Align.INLINE)
d.comment(0x99bf, '...', align=Align.INLINE)
d.comment(0x99c2, 'Save the divisor sign', align=Align.INLINE)
d.comment(0x99c4, '...', align=Align.INLINE)
d.comment(0x99c5, 'take |divisor|', align=Align.INLINE)
d.comment(0x99c8, 'Stack it, evaluate the dividend', align=Align.INLINE)
d.comment(0x99cb, 'remember the operator', align=Align.INLINE)
d.comment(0x99cd, 'coerce the dividend to integer', align=Align.INLINE)
d.comment(0x99ce, '...', align=Align.INLINE)
d.comment(0x99d1, 'Recover the divisor sign', align=Align.INLINE)
d.comment(0x99d2, 'remainder takes the dividend sign', align=Align.INLINE)
d.comment(0x99d4, 'quotient sign = divisor XOR dividend', align=Align.INLINE)
d.comment(0x99d6, '...', align=Align.INLINE)
d.comment(0x99d8, 'take |dividend|', align=Align.INLINE)
d.comment(0x99db, 'Move the dividend to the work area (&39-&3C)',
          align=Align.INLINE)
d.comment(0x99dd, '...', align=Align.INLINE)
d.comment(0x99e0, 'Clear the remainder (&3D-&40)', align=Align.INLINE)
d.comment(0x99e2, '...', align=Align.INLINE)
d.comment(0x99e4, '...', align=Align.INLINE)
d.comment(0x99e6, '...', align=Align.INLINE)
d.comment(0x99e8, 'Divisor zero?', align=Align.INLINE)
d.comment(0x99ea, '...', align=Align.INLINE)
d.comment(0x99ec, '...', align=Align.INLINE)
d.comment(0x99ee, '...', align=Align.INLINE)
d.comment(0x99f0, 'yes: Division by zero', align=Align.INLINE)
d.comment(0x99f2, '32 bits', align=Align.INLINE)
d.comment(0x99f4, 'Normalise: count down', align=Align.INLINE)
d.comment(0x99f5, 'dividend exhausted: done', align=Align.INLINE)
d.comment(0x99f7, 'shift the dividend left until the top bit is set',
          align=Align.INLINE)
d.comment(0x99f9, '...', align=Align.INLINE)
d.comment(0x99fb, '...', align=Align.INLINE)
d.comment(0x99fd, '...', align=Align.INLINE)
d.comment(0x99ff, 'loop', align=Align.INLINE)
d.comment(0x9a01, 'Shift a bit from dividend into the remainder',
          align=Align.INLINE)
d.comment(0x9a03, '...', align=Align.INLINE)
d.comment(0x9a05, '...', align=Align.INLINE)
d.comment(0x9a07, '...', align=Align.INLINE)
d.comment(0x9a09, '...', align=Align.INLINE)
d.comment(0x9a0b, '...', align=Align.INLINE)
d.comment(0x9a0d, '...', align=Align.INLINE)
d.comment(0x9a0f, '...', align=Align.INLINE)
d.comment(0x9a11, 'Try remainder - divisor', align=Align.INLINE)
d.comment(0x9a12, '...', align=Align.INLINE)
d.comment(0x9a14, '...', align=Align.INLINE)
d.comment(0x9a16, '...', align=Align.INLINE)
d.comment(0x9a17, '...', align=Align.INLINE)
d.comment(0x9a19, '...', align=Align.INLINE)
d.comment(0x9a1b, '...', align=Align.INLINE)
d.comment(0x9a1c, '...', align=Align.INLINE)
d.comment(0x9a1e, '...', align=Align.INLINE)
d.comment(0x9a20, '...', align=Align.INLINE)
d.comment(0x9a21, '...', align=Align.INLINE)
d.comment(0x9a23, '...', align=Align.INLINE)
d.comment(0x9a25, "doesn't fit: leave the remainder", align=Align.INLINE)
d.comment(0x9a27, 'fits: keep the new remainder (quotient bit = 1)',
          align=Align.INLINE)
d.comment(0x9a29, '...', align=Align.INLINE)
d.comment(0x9a2b, '...', align=Align.INLINE)
d.comment(0x9a2c, '...', align=Align.INLINE)
d.comment(0x9a2e, '...', align=Align.INLINE)
d.comment(0x9a2f, '...', align=Align.INLINE)
d.comment(0x9a31, 'next bit', align=Align.INLINE)
d.comment(0x9a33, 'discard the trial subtraction', align=Align.INLINE)
d.comment(0x9a34, '...', align=Align.INLINE)
d.comment(0x9a35, 'Next bit', align=Align.INLINE)
d.comment(0x9a36, 'loop', align=Align.INLINE)
d.comment(0x9a38, 'Return', align=Align.INLINE)

# Level-3 multiply (&9D32): real result tail, then the integer path.
d.comment(0x9d32, 'real result', align=Align.INLINE)
d.comment(0x9d34, 'restore the operator', align=Align.INLINE)
d.comment(0x9d36, 'loop for further * / DIV MOD', align=Align.INLINE)
d.comment(0x9d39, 'String operand: Type mismatch', align=Align.INLINE)
d.comment(0x9d3c, 'Left operand type', align=Align.INLINE)
d.comment(0x9d3d, 'string: Type mismatch', align=Align.INLINE)
d.comment(0x9d3f, 'real: floating-point multiply', align=Align.INLINE)
d.comment(0x9d41, 'Integer: does it fit signed 16 bits?', align=Align.INLINE)
d.comment(0x9d43, '...', align=Align.INLINE)
d.comment(0x9d45, 'no: floating-point multiply', align=Align.INLINE)
d.comment(0x9d47, 'high word zero (positive)?', align=Align.INLINE)
d.comment(0x9d48, 'yes', align=Align.INLINE)
d.comment(0x9d4a, 'high word all ones (negative)?', align=Align.INLINE)
d.comment(0x9d4c, 'no: floating-point multiply', align=Align.INLINE)
d.comment(0x9d4e, 'sign consistent with bit 15?', align=Align.INLINE)
d.comment(0x9d50, 'no: floating-point multiply', align=Align.INLINE)
d.comment(0x9d52, 'Stack it, evaluate the right operand', align=Align.INLINE)
d.comment(0x9d55, 'remember the operator', align=Align.INLINE)
d.comment(0x9d57, 'right operand type', align=Align.INLINE)
d.comment(0x9d58, 'string: Type mismatch', align=Align.INLINE)
d.comment(0x9d5a, 'real: floating-point multiply', align=Align.INLINE)
d.comment(0x9d5c, 'fits signed 16 bits?', align=Align.INLINE)
d.comment(0x9d5e, '...', align=Align.INLINE)
d.comment(0x9d60, 'no: floating-point multiply', align=Align.INLINE)
d.comment(0x9d62, 'positive?', align=Align.INLINE)
d.comment(0x9d63, 'yes', align=Align.INLINE)
d.comment(0x9d65, 'negative?', align=Align.INLINE)
d.comment(0x9d67, 'no: floating-point multiply', align=Align.INLINE)
d.comment(0x9d69, 'sign consistent?', align=Align.INLINE)
d.comment(0x9d6b, 'no: floating-point multiply', align=Align.INLINE)
# iwa_mod (&9E01) and iwa_div (&9E0A).
d.comment(0x9e0a, 'DIV: divide', align=Align.INLINE)
d.comment(0x9e0d, 'Shift the quotient up by one', align=Align.INLINE)
d.comment(0x9e0f, '...', align=Align.INLINE)
d.comment(0x9e11, '...', align=Align.INLINE)
d.comment(0x9e13, '...', align=Align.INLINE)
d.comment(0x9e15, 'quotient sign', align=Align.INLINE)
d.comment(0x9e17, '...', align=Align.INLINE)
d.comment(0x9e18, 'load the quotient (&39-&3C)', align=Align.INLINE)
d.comment(0x9e1a, '...and apply the sign', align=Align.INLINE)
d.comment(0x9e1d, 'Stack the integer, evaluate the next ^ operand',
          align=Align.INLINE)

# eval_power (&9E20): the ^ operator.
d.comment(0x9e20, 'Evaluate the base', align=Align.INLINE)
d.comment(0x9e23, 'Save the result type', align=Align.INLINE)
d.comment(0x9e24, 'Next character', align=Align.INLINE)
d.comment(0x9e26, '...', align=Align.INLINE)
d.comment(0x9e28, '...', align=Align.INLINE)
d.comment(0x9e2a, 'space?', align=Align.INLINE)
d.comment(0x9e2c, 'skip it', align=Align.INLINE)
d.comment(0x9e2e, 'keep the operator', align=Align.INLINE)
d.comment(0x9e2f, 'restore the type', align=Align.INLINE)
d.comment(0x9e30, "'^'?", align=Align.INLINE)
d.comment(0x9e32, 'yes', align=Align.INLINE)
d.comment(0x9e34, 'no: return', align=Align.INLINE)
d.comment(0x9e35, 'Ensure the base is real', align=Align.INLINE)
d.comment(0x9e36, '...', align=Align.INLINE)
d.comment(0x9e39, 'stack the base', align=Align.INLINE)
d.comment(0x9e3c, 'evaluate the exponent as a real', align=Align.INLINE)
d.comment(0x9e3f, 'Exponent magnitude', align=Align.INLINE)
d.comment(0x9e41, 'large (>= 2^7)?', align=Align.INLINE)
d.comment(0x9e43, 'yes: use exp(y*ln x)', align=Align.INLINE)
d.comment(0x9e45, 'Split into integer and fractional parts', align=Align.INLINE)
d.comment(0x9e48, 'fractional part nonzero?', align=Align.INLINE)
d.comment(0x9e4a, 'no: integer power - unstack the base', align=Align.INLINE)
d.comment(0x9e4d, '...', align=Align.INLINE)
d.comment(0x9e50, 'integer exponent', align=Align.INLINE)
d.comment(0x9e52, 'FWA = base ^ int', align=Align.INLINE)
d.comment(0x9e55, 'real result', align=Align.INLINE)
d.comment(0x9e57, 'continue', align=Align.INLINE)
d.comment(0x9e59, 'Fractional exponent: save the fraction', align=Align.INLINE)
d.comment(0x9e5c, 'point at the stacked base', align=Align.INLINE)
d.comment(0x9e5e, '...', align=Align.INLINE)
d.comment(0x9e60, '...', align=Align.INLINE)
d.comment(0x9e62, '...', align=Align.INLINE)
d.comment(0x9e64, 'load the base', align=Align.INLINE)
d.comment(0x9e67, 'integer part of the exponent', align=Align.INLINE)
d.comment(0x9e69, 'FWA = base ^ int', align=Align.INLINE)
d.comment(0x9e6c, 'save base^int in TEMP2', align=Align.INLINE)
d.comment(0x9e6f, 'unstack the base', align=Align.INLINE)
d.comment(0x9e72, '...', align=Align.INLINE)
d.comment(0x9e75, 'ln(base)', align=Align.INLINE)
d.comment(0x9e78, 'times the fractional exponent', align=Align.INLINE)
d.comment(0x9e7b, 'exp(that) = base^frac', align=Align.INLINE)
d.comment(0x9e7e, 'point at base^int', align=Align.INLINE)
d.comment(0x9e81, 'FWA = base^int * base^frac', align=Align.INLINE)
d.comment(0x9e84, 'real result', align=Align.INLINE)
d.comment(0x9e86, 'continue', align=Align.INLINE)
d.comment(0x9e88, 'Large exponent: x^y = exp(y * ln x)', align=Align.INLINE)
d.comment(0x9e8b, '...', align=Align.INLINE)
d.comment(0x9e8e, 'evaluate it', align=Align.INLINE)

# fn_lefts (&AFCC): LEFT$(s$, n) - keep the first n characters.
d.comment(0xafcc, 'Evaluate the source string', align=Align.INLINE)
d.comment(0xafcf, 'not a string: Type mismatch', align=Align.INLINE)
d.comment(0xafd1, "','?", align=Align.INLINE)
d.comment(0xafd3, 'no: Missing ,', align=Align.INLINE)
d.comment(0xafd5, 'step past', align=Align.INLINE)
d.comment(0xafd7, 'Stack the string', align=Align.INLINE)
d.comment(0xafda, 'Evaluate the count, expect )', align=Align.INLINE)
d.comment(0xafdd, 'coerce to integer', align=Align.INLINE)
d.comment(0xafe0, 'Restore the string', align=Align.INLINE)
d.comment(0xafe3, 'Count', align=Align.INLINE)
d.comment(0xafe5, 'count >= length?', align=Align.INLINE)
d.comment(0xafe7, 'yes: keep the whole string', align=Align.INLINE)
d.comment(0xafe9, 'truncate to the count', align=Align.INLINE)
d.comment(0xafeb, 'String result', align=Align.INLINE)
d.comment(0xafed, 'Return', align=Align.INLINE)

# fn_rights (&AFEE): RIGHT$(s$, n) - keep the last n characters.
d.comment(0xafee, 'Evaluate the source string', align=Align.INLINE)
d.comment(0xaff1, 'not a string: Type mismatch', align=Align.INLINE)
d.comment(0xaff3, "','?", align=Align.INLINE)
d.comment(0xaff5, 'no: Missing ,', align=Align.INLINE)
d.comment(0xaff7, 'step past', align=Align.INLINE)
d.comment(0xaff9, 'Stack the string', align=Align.INLINE)
d.comment(0xaffc, 'Evaluate the count, expect )', align=Align.INLINE)
d.comment(0xafff, 'coerce to integer', align=Align.INLINE)
d.label(0xb017, 'rights_copy_down')   # RIGHT$ tail-to-front shift loop
d.comment(0xb002, 'Restore the string', align=Align.INLINE)
d.comment(0xb005, 'Start = length - count', align=Align.INLINE)
d.comment(0xb007, 'ready the subtract', align=Align.INLINE)
d.comment(0xb008, 'minus the count: A = start offset', align=Align.INLINE)
d.comment(0xb00a, 'count > length: keep the whole string', align=Align.INLINE)
d.comment(0xb00c, 'count == length: keep it', align=Align.INLINE)
d.comment(0xb00e, 'Start offset', align=Align.INLINE)
d.comment(0xb00f, 'New length = count', align=Align.INLINE)
d.comment(0xb011, 'store the new (shorter) length', align=Align.INLINE)
d.comment(0xb013, 'zero: empty string', align=Align.INLINE)
d.comment(0xb015, 'Copy the last count chars to the front', align=Align.INLINE)
d.comment(0xb017, 'Read a kept char from the tail (at X)', align=Align.INLINE)
d.comment(0xb01a, 'Pack it down to the front (at Y)', align=Align.INLINE)
d.comment(0xb01d, 'Advance the read cursor', align=Align.INLINE)
d.comment(0xb01e, 'Advance the write cursor', align=Align.INLINE)
d.comment(0xb01f, 'One fewer char to move', align=Align.INLINE)
d.comment(0xb021, 'Until all `count` chars are shifted down', align=Align.INLINE)
d.comment(0xb023, 'Keep the whole string', align=Align.INLINE)
d.comment(0xb025, 'Return', align=Align.INLINE)

# fn_mids (&B039): MID$(s$, p [, n]) - substring from position p.
d.comment(0xb039, 'Evaluate the source string', align=Align.INLINE)
d.comment(0xb03c, 'not a string: Type mismatch', align=Align.INLINE)
d.comment(0xb03e, "','?", align=Align.INLINE)
d.comment(0xb040, 'no: Missing ,', align=Align.INLINE)
d.comment(0xb042, 'Stack the string', align=Align.INLINE)
d.comment(0xb045, 'step past', align=Align.INLINE)
d.comment(0xb047, 'Evaluate the start position', align=Align.INLINE)
d.comment(0xb04a, 'Save it', align=Align.INLINE)
d.comment(0xb04c, '...', align=Align.INLINE)
d.comment(0xb04d, 'Default length = 255', align=Align.INLINE)
d.comment(0xb04f, '...', align=Align.INLINE)
d.comment(0xb051, 'step past', align=Align.INLINE)
d.comment(0xb053, "')' (no length given)?", align=Align.INLINE)
d.comment(0xb055, 'yes: use the default', align=Align.INLINE)
d.comment(0xb057, "','?", align=Align.INLINE)
d.comment(0xb059, 'no: Missing ,', align=Align.INLINE)
d.comment(0xb05b, 'Evaluate the length, expect )', align=Align.INLINE)
d.comment(0xb05e, 'coerce to integer', align=Align.INLINE)
d.comment(0xb061, 'Restore the string', align=Align.INLINE)
d.comment(0xb064, 'Start position', align=Align.INLINE)
d.comment(0xb065, '...', align=Align.INLINE)
d.comment(0xb066, '...', align=Align.INLINE)
d.comment(0xb067, 'position 0: treat as 1', align=Align.INLINE)
d.comment(0xb069, 'past the end?', align=Align.INLINE)
d.comment(0xb06b, 'yes: empty string', align=Align.INLINE)
d.comment(0xb06d, 'Zero-based start = p - 1', align=Align.INLINE)
d.comment(0xb06e, '...', align=Align.INLINE)
d.comment(0xb06f, 'Save the start offset', align=Align.INLINE)
d.comment(0xb071, '...', align=Align.INLINE)
d.comment(0xb072, 'Destination index', align=Align.INLINE)
d.comment(0xb074, 'Available = length - start', align=Align.INLINE)
d.comment(0xb076, '...', align=Align.INLINE)
d.comment(0xb077, '...', align=Align.INLINE)
d.comment(0xb079, 'more than requested?', align=Align.INLINE)
d.comment(0xb07b, 'no: use the available count', align=Align.INLINE)
d.comment(0xb07d, 'clamp the length', align=Align.INLINE)
d.comment(0xb07f, 'Length', align=Align.INLINE)
d.comment(0xb081, 'zero: empty string', align=Align.INLINE)
d.comment(0xb083, 'Copy the substring to the front', align=Align.INLINE)
d.comment(0xb086, '...', align=Align.INLINE)
d.comment(0xb089, '...', align=Align.INLINE)
d.comment(0xb08a, '...', align=Align.INLINE)
d.comment(0xb08b, '...', align=Align.INLINE)
d.comment(0xb08d, 'loop', align=Align.INLINE)
d.comment(0xb08f, 'Set the result length', align=Align.INLINE)
d.comment(0xb091, 'String result', align=Align.INLINE)
d.comment(0xb093, 'Return', align=Align.INLINE)

# fn_instr (&ACE2): INSTR(s$, search$ [, start]) -> position or 0.
d.comment(0xace2, 'Evaluate the searched string', align=Align.INLINE)
d.comment(0xace5, 'not a string: Type mismatch', align=Align.INLINE)
d.comment(0xace7, "','?", align=Align.INLINE)
d.comment(0xace9, 'no: Missing ,', align=Align.INLINE)
d.comment(0xaceb, 'step past', align=Align.INLINE)
d.comment(0xaced, 'Stack the searched string', align=Align.INLINE)
d.comment(0xacf0, 'Evaluate the search string', align=Align.INLINE)
d.comment(0xacf3, 'not a string: Type mismatch', align=Align.INLINE)
d.comment(0xacf5, 'Default start position = 1', align=Align.INLINE)
d.comment(0xacf7, '...', align=Align.INLINE)
d.comment(0xacf9, 'step past', align=Align.INLINE)
d.comment(0xacfb, "')' (no start given)?", align=Align.INLINE)
d.comment(0xacfd, 'yes: search from 1', align=Align.INLINE)
d.comment(0xacff, "','?", align=Align.INLINE)
d.comment(0xad01, 'yes: a start position follows', align=Align.INLINE)
d.comment(0xad03, 'Missing , error', align=Align.INLINE)
d.comment(0xad06, 'Stack the search string', align=Align.INLINE)
d.comment(0xad09, 'Evaluate the start, expect )', align=Align.INLINE)
d.comment(0xad0c, 'coerce to integer', align=Align.INLINE)
d.comment(0xad0f, 'Restore the search string', align=Align.INLINE)
d.comment(0xad12, 'Destination index', align=Align.INLINE)
d.comment(0xad14, 'Start position', align=Align.INLINE)
d.comment(0xad16, 'non-zero?', align=Align.INLINE)
d.comment(0xad18, 'force at least 1', align=Align.INLINE)
d.comment(0xad1a, 'Current match position', align=Align.INLINE)
d.comment(0xad1c, 'Zero-based start = start - 1', align=Align.INLINE)
d.comment(0xad1d, '...', align=Align.INLINE)
d.comment(0xad1e, '...', align=Align.INLINE)
d.comment(0xad20, 'Point at s$ + (start-1)', align=Align.INLINE)
d.comment(0xad21, '...', align=Align.INLINE)
d.comment(0xad23, '...', align=Align.INLINE)
d.comment(0xad25, '...', align=Align.INLINE)
d.comment(0xad26, '...', align=Align.INLINE)
d.comment(0xad28, '...', align=Align.INLINE)
d.comment(0xad2a, 'Length of s$', align=Align.INLINE)
d.comment(0xad2c, 'minus the start offset...', align=Align.INLINE)
d.comment(0xad2d, '...', align=Align.INLINE)
d.comment(0xad2f, 'start beyond the end: not found', align=Align.INLINE)
d.comment(0xad31, 'minus the search length', align=Align.INLINE)
d.comment(0xad33, "won't fit: not found", align=Align.INLINE)
d.comment(0xad35, 'Number of start positions to try', align=Align.INLINE)
d.comment(0xad37, '...', align=Align.INLINE)
d.comment(0xad39, 'Re-point at the stacked string', align=Align.INLINE)
d.comment(0xad3c, 'Compare from index 0', align=Align.INLINE)
d.comment(0xad3e, 'Search length', align=Align.INLINE)
d.comment(0xad40, 'empty search: matches here', align=Align.INLINE)
d.comment(0xad42, 's$ character', align=Align.INLINE)
d.comment(0xad44, 'vs search character', align=Align.INLINE)
d.comment(0xad47, 'mismatch: advance', align=Align.INLINE)
d.comment(0xad49, 'next', align=Align.INLINE)
d.comment(0xad4a, '...', align=Align.INLINE)
d.comment(0xad4b, 'all matched?', align=Align.INLINE)
d.comment(0xad4d, 'Match: result is the position', align=Align.INLINE)
d.comment(0xad4f, 'return it as an integer', align=Align.INLINE)
d.comment(0xad52, 'Not found: drop the stacked string', align=Align.INLINE)
d.comment(0xad55, 'result = 0', align=Align.INLINE)
d.comment(0xad57, 'return it', align=Align.INLINE)
d.comment(0xad59, 'Advance the match position', align=Align.INLINE)
d.comment(0xad5b, 'one fewer position to try', align=Align.INLINE)
d.comment(0xad5d, 'exhausted: not found', align=Align.INLINE)
d.comment(0xad5f, 'advance the s$ pointer', align=Align.INLINE)
d.comment(0xad61, 'retry', align=Align.INLINE)
d.comment(0xad63, '...', align=Align.INLINE)
d.comment(0xad65, 'retry', align=Align.INLINE)

# ----------------------------------------------------------------------
# stmt_print (&8D9A): the PRINT statement.
# Walks the print list, handling the @% field width and the ~ (hex), ,
# (next field) and ; (no gap) modifiers, the TAB/SPC tokens, and string
# and numeric items, padding numbers to the field width.
# ----------------------------------------------------------------------
d.comment(0x8d9a, 'Next non-space character', align=Align.INLINE)
d.comment(0x8d9f, "'#': PRINT# to a file", align=Align.INLINE)
d.comment(0x8da1, 'Back up over the character', align=Align.INLINE)
d.comment(0x8da3, 'enter the print loop', align=Align.INLINE)
d.comment(0x8da9, 'zero: no padding', align=Align.INLINE)
d.comment(0x8dab, 'Current column (COUNT)', align=Align.INLINE)
d.comment(0x8dad, 'at column 0: no padding', align=Align.INLINE)
d.comment(0x8daf, 'reduce by the field width...', align=Align.INLINE)
d.comment(0x8db2, '...until COUNT mod width', align=Align.INLINE)
d.comment(0x8db4, 'spaces needed to the next field', align=Align.INLINE)
d.comment(0x8db5, 'print a space', align=Align.INLINE)
d.comment(0x8db8, '...', align=Align.INLINE)
d.comment(0x8db9, 'loop', align=Align.INLINE)
d.comment(0x8dbb, 'Prepare for decimal', align=Align.INLINE)
d.comment(0x8dbf, '...', align=Align.INLINE)
d.comment(0x8dc3, 'Next non-space character', align=Align.INLINE)
d.comment(0x8dc6, "':' end of statement?", align=Align.INLINE)
d.comment(0x8dc8, 'yes', align=Align.INLINE)
d.comment(0x8dca, 'end of line?', align=Align.INLINE)
d.comment(0x8dcc, 'yes', align=Align.INLINE)
d.comment(0x8dce, 'ELSE?', align=Align.INLINE)
d.comment(0x8dd0, 'yes', align=Align.INLINE)
d.comment(0x8dd2, "'~' hex mode?", align=Align.INLINE)
d.comment(0x8dd4, 'yes: set the flag', align=Align.INLINE)
d.comment(0x8dd8, 'yes', align=Align.INLINE)
d.comment(0x8ddc, 'yes', align=Align.INLINE)
d.comment(0x8de1, 'handled: next item', align=Align.INLINE)
d.comment(0x8de3, 'Save the field width...', align=Align.INLINE)
d.comment(0x8de5, '...', align=Align.INLINE)
d.comment(0x8de6, '...and flags (the evaluator may PRINT)', align=Align.INLINE)
d.comment(0x8de8, '...', align=Align.INLINE)
d.comment(0x8de9, 'Back up to the item', align=Align.INLINE)
d.comment(0x8dee, 'Restore the flags...', align=Align.INLINE)
d.comment(0x8def, '...', align=Align.INLINE)
d.comment(0x8df1, '...and the field width', align=Align.INLINE)
d.comment(0x8df2, '...', align=Align.INLINE)
d.comment(0x8df4, 'Update the program pointer', align=Align.INLINE)
d.comment(0x8df6, '...', align=Align.INLINE)
d.comment(0x8df8, 'String item?', align=Align.INLINE)
d.comment(0x8e00, 'minus the string length', align=Align.INLINE)
d.comment(0x8e01, '...', align=Align.INLINE)
d.comment(0x8e03, 'longer than the field: print as is', align=Align.INLINE)
d.comment(0x8e05, 'equal: print as is', align=Align.INLINE)
d.comment(0x8e07, 'spaces to pad with', align=Align.INLINE)
d.comment(0x8e08, 'print a leading space', align=Align.INLINE)
d.comment(0x8e0b, '...', align=Align.INLINE)
d.comment(0x8e0c, 'loop', align=Align.INLINE)
d.comment(0x8e0e, 'String length', align=Align.INLINE)
d.comment(0x8e10, 'empty: next item', align=Align.INLINE)
d.comment(0x8e12, 'From the start', align=Align.INLINE)
d.comment(0x8e14, 'String character', align=Align.INLINE)
d.comment(0x8e17, 'print it', align=Align.INLINE)
d.comment(0x8e1a, 'next', align=Align.INLINE)
d.comment(0x8e1b, '...', align=Align.INLINE)
d.comment(0x8e1d, 'loop', align=Align.INLINE)
d.comment(0x8e1f, 'next item', align=Align.INLINE)
# PRINT end of statement (&8D7D) and semicolon handling.
d.comment(0x8d7d, 'Print a newline', align=Align.INLINE)
d.comment(0x8d80, 'next statement', align=Align.INLINE)
d.comment(0x8d83, 'Semicolon: clear the field width...', align=Align.INLINE)
d.comment(0x8d85, '...', align=Align.INLINE)
d.comment(0x8d87, '...and flags', align=Align.INLINE)
d.comment(0x8d89, 'Next non-space character', align=Align.INLINE)
d.comment(0x8d8c, "':' end?", align=Align.INLINE)
d.comment(0x8d8e, 'yes: end without a newline', align=Align.INLINE)
d.comment(0x8d90, 'end of line?', align=Align.INLINE)
d.comment(0x8d92, 'yes', align=Align.INLINE)
d.comment(0x8d94, 'ELSE?', align=Align.INLINE)
d.comment(0x8d96, 'yes', align=Align.INLINE)
d.comment(0x8d98, 'otherwise continue the print loop', align=Align.INLINE)

# TAB()/SPC handler (&8E24), called from print_special_item.
d.comment(0x8e21, 'Missing , error', align=Align.INLINE)
d.comment(0x8e24, "',' TAB(x,y) form?", align=Align.INLINE)
d.comment(0x8e26, 'no: TAB(x) or SPC', align=Align.INLINE)
d.comment(0x8e28, 'Save the x coordinate', align=Align.INLINE)
d.comment(0x8e2a, '...', align=Align.INLINE)
d.comment(0x8e2b, 'Evaluate y, expect )', align=Align.INLINE)
d.comment(0x8e2e, 'coerce to integer', align=Align.INLINE)
d.comment(0x8e31, 'VDU 31 (move cursor)', align=Align.INLINE)
d.comment(0x8e33, '...', align=Align.INLINE)
d.comment(0x8e36, 'x coordinate', align=Align.INLINE)
d.comment(0x8e37, '...', align=Align.INLINE)
d.comment(0x8e3a, 'y coordinate', align=Align.INLINE)
d.comment(0x8e3d, 'next item', align=Align.INLINE)
d.comment(0x8e40, 'TAB(x): evaluate x', align=Align.INLINE)
d.comment(0x8e43, 'skip spaces', align=Align.INLINE)
d.comment(0x8e46, "')'?", align=Align.INLINE)
d.comment(0x8e48, 'no: TAB(x,y)', align=Align.INLINE)
d.comment(0x8e4a, 'Spaces = x - COUNT', align=Align.INLINE)
d.comment(0x8e4c, '...', align=Align.INLINE)
d.comment(0x8e4e, 'already at column x: nothing to do', align=Align.INLINE)
d.comment(0x8e50, 'count', align=Align.INLINE)
d.comment(0x8e51, 'past column x: skip', align=Align.INLINE)
d.comment(0x8e53, 'Newline to reach a fresh line', align=Align.INLINE)
d.comment(0x8e56, '...', align=Align.INLINE)
d.comment(0x8e58, '...', align=Align.INLINE)
d.comment(0x8e5b, 'spaces = x', align=Align.INLINE)
d.comment(0x8e5d, 'none', align=Align.INLINE)
d.comment(0x8e5f, 'Print a space', align=Align.INLINE)
d.comment(0x8e62, '...', align=Align.INLINE)
d.comment(0x8e63, 'loop', align=Align.INLINE)
d.comment(0x8e65, 'next item', align=Align.INLINE)
d.comment(0x8e67, 'SPC: print a newline', align=Align.INLINE)
d.comment(0x8e6a, 'Sync the program pointer', align=Align.INLINE)
d.comment(0x8e6b, '...', align=Align.INLINE)
d.comment(0x8e6d, '...', align=Align.INLINE)
d.comment(0x8e6f, 'Return', align=Align.INLINE)

# ----------------------------------------------------------------------
# stmt_for (&B7C4): the FOR statement.
# Builds a 15-byte control frame on the FOR stack at &0500, indexed by
# the FOR level &26: loop-variable pointer (+0..+2), STEP (+3), limit
# (+8) and the loop-body text pointer (+D). Integer loops store 4-byte
# values; real loops store packed 5-byte reals.
# ----------------------------------------------------------------------
d.comment(0xb7c7, 'not a variable: error', align=Align.INLINE)
d.comment(0xb7c9, 'indirection: error', align=Align.INLINE)
d.comment(0xb7ce, 'Expect "="', align=Align.INLINE)
d.comment(0xb7d1, 'Assign the initial value', align=Align.INLINE)
d.comment(0xb7d8, 'yes: error', align=Align.INLINE)
d.comment(0xb7dc, '...', align=Align.INLINE)
d.comment(0xb7df, '...', align=Align.INLINE)
d.comment(0xb7e1, '...', align=Align.INLINE)
d.comment(0xb7e4, '...and its type (+2)', align=Align.INLINE)
d.comment(0xb7e6, '...', align=Align.INLINE)
d.comment(0xb7e9, 'keep the type', align=Align.INLINE)
d.comment(0xb7ea, 'Next character', align=Align.INLINE)
d.comment(0xb7ef, 'no: No TO error', align=Align.INLINE)
d.comment(0xb7f1, 'real loop variable?', align=Align.INLINE)
d.comment(0xb7f3, 'yes: real FOR loop', align=Align.INLINE)
d.comment(0xb7f5, 'Integer: evaluate the limit', align=Align.INLINE)
d.comment(0xb7f8, 'FOR level', align=Align.INLINE)
d.comment(0xb7fc, '...', align=Align.INLINE)
d.comment(0xb7ff, '...', align=Align.INLINE)
d.comment(0xb801, '...', align=Align.INLINE)
d.comment(0xb804, '...', align=Align.INLINE)
d.comment(0xb806, '...', align=Align.INLINE)
d.comment(0xb809, '...', align=Align.INLINE)
d.comment(0xb80b, '...', align=Align.INLINE)
d.comment(0xb80e, 'Default STEP = 1', align=Align.INLINE)
d.comment(0xb810, '...', align=Align.INLINE)
d.comment(0xb813, 'Next character', align=Align.INLINE)
d.comment(0xb818, 'no: use the default', align=Align.INLINE)
d.comment(0xb81a, 'Evaluate the step', align=Align.INLINE)
d.comment(0xb81d, '...', align=Align.INLINE)
d.comment(0xb81f, 'Sync the program pointer', align=Align.INLINE)
d.comment(0xb821, 'FOR level', align=Align.INLINE)
d.comment(0xb823, 'Store the step in the frame (+3)', align=Align.INLINE)
d.comment(0xb825, '...', align=Align.INLINE)
d.comment(0xb828, '...', align=Align.INLINE)
d.comment(0xb82a, '...', align=Align.INLINE)
d.comment(0xb82d, '...', align=Align.INLINE)
d.comment(0xb82f, '...', align=Align.INLINE)
d.comment(0xb832, '...', align=Align.INLINE)
d.comment(0xb834, '...', align=Align.INLINE)
d.comment(0xb837, 'Step over the loop body to find its start',
          align=Align.INLINE)
d.comment(0xb83a, 'FOR level', align=Align.INLINE)
d.comment(0xb83c, 'Store the loop-body pointer (+D)', align=Align.INLINE)
d.comment(0xb83e, '...', align=Align.INLINE)
d.comment(0xb841, '...', align=Align.INLINE)
d.comment(0xb843, '...', align=Align.INLINE)
d.comment(0xb846, 'Advance the FOR level by 15', align=Align.INLINE)
d.comment(0xb847, '...', align=Align.INLINE)
d.comment(0xb848, '...', align=Align.INLINE)
d.comment(0xb84a, '...', align=Align.INLINE)
d.comment(0xb84c, 'Continue execution', align=Align.INLINE)
# Real FOR path.
d.comment(0xb84f, 'Evaluate the limit', align=Align.INLINE)
d.comment(0xb852, 'ensure it is real', align=Align.INLINE)
d.comment(0xb855, 'Point at frame +8 (limit slot)', align=Align.INLINE)
d.comment(0xb857, '...', align=Align.INLINE)
d.comment(0xb858, '...', align=Align.INLINE)
d.comment(0xb85a, '...', align=Align.INLINE)
d.comment(0xb85c, '...', align=Align.INLINE)
d.comment(0xb85e, '...', align=Align.INLINE)
d.comment(0xb860, 'Pack the limit there', align=Align.INLINE)
d.comment(0xb863, 'Default STEP = 1.0', align=Align.INLINE)
d.comment(0xb866, 'Next character', align=Align.INLINE)
d.comment(0xb869, 'STEP token?', align=Align.INLINE)
d.comment(0xb86b, 'no: use the default', align=Align.INLINE)
d.comment(0xb86d, 'Evaluate the step', align=Align.INLINE)
d.comment(0xb870, 'ensure it is real', align=Align.INLINE)
d.comment(0xb873, '...', align=Align.INLINE)
d.comment(0xb875, 'Sync the program pointer', align=Align.INLINE)
d.comment(0xb877, 'Point at frame +3 (step slot)', align=Align.INLINE)
d.comment(0xb879, '...', align=Align.INLINE)
d.comment(0xb87a, '...', align=Align.INLINE)
d.comment(0xb87c, '...', align=Align.INLINE)
d.comment(0xb87e, '...', align=Align.INLINE)
d.comment(0xb880, '...', align=Align.INLINE)
d.comment(0xb882, 'Pack the step there', align=Align.INLINE)
d.comment(0xb885, 'Join the common tail', align=Align.INLINE)

# ----------------------------------------------------------------------
# stmt_dim (&912F): the DIM statement - allocate an array.
# Parses the array name and element size (5 real, 4 integer/string),
# reads the comma-separated dimension bounds into the descriptor at the
# variable top, computes the total size as the product of (bound+1) times
# the element size, claims that space below the stack and zeroes it.
# ----------------------------------------------------------------------
d.comment(0x912f, 'Skip spaces', align=Align.INLINE)
d.comment(0x9132, 'Point &37/&38 at the name', align=Align.INLINE)
d.comment(0x9133, '...', align=Align.INLINE)
d.comment(0x9134, '...', align=Align.INLINE)
d.comment(0x9136, '...', align=Align.INLINE)
d.comment(0x9138, '...', align=Align.INLINE)
d.comment(0x913a, '...', align=Align.INLINE)
d.comment(0x913b, '...', align=Align.INLINE)
d.comment(0x913c, '...', align=Align.INLINE)
d.comment(0x913e, '...', align=Align.INLINE)
d.comment(0x9140, '...', align=Align.INLINE)
d.comment(0x9141, '...', align=Align.INLINE)
d.comment(0x9143, '...', align=Align.INLINE)
d.comment(0x9145, 'Default element size = 5 (real)', align=Align.INLINE)
d.comment(0x9147, '...', align=Align.INLINE)
d.comment(0x9149, 'Name offset', align=Align.INLINE)
d.comment(0x914b, 'Validate the name', align=Align.INLINE)
d.comment(0x914e, 'empty name?', align=Align.INLINE)
d.comment(0x9150, 'yes: Bad DIM', align=Align.INLINE)
d.comment(0x9152, "'(' array?", align=Align.INLINE)
d.comment(0x9154, 'yes', align=Align.INLINE)
d.comment(0x9156, "'$' string?", align=Align.INLINE)
d.comment(0x9158, 'yes', align=Align.INLINE)
d.comment(0x915a, "'%' integer?", align=Align.INLINE)
d.comment(0x915c, 'no: DIM var n (byte block)', align=Align.INLINE)
d.comment(0x915e, 'Element size = 4 (integer/string)', align=Align.INLINE)
d.comment(0x9160, 'step past the suffix', align=Align.INLINE)
d.comment(0x9161, '...', align=Align.INLINE)
d.comment(0x9162, 'following character', align=Align.INLINE)
d.comment(0x9164, "'(' array?", align=Align.INLINE)
d.comment(0x9166, 'yes', align=Align.INLINE)
d.comment(0x9168, 'DIM var n: allocate a byte block', align=Align.INLINE)
d.comment(0x916b, 'Array: save the name length', align=Align.INLINE)
d.comment(0x916d, '...', align=Align.INLINE)
d.comment(0x916f, 'Already defined?', align=Align.INLINE)
d.comment(0x9172, 'yes: Bad DIM (re-DIM)', align=Align.INLINE)
d.comment(0x9174, 'Create the array variable', align=Align.INLINE)
d.comment(0x9177, 'Clear its pointer', align=Align.INLINE)
d.comment(0x9179, '...', align=Align.INLINE)
d.comment(0x917c, 'Save the element size', align=Align.INLINE)
d.comment(0x917e, '...', align=Align.INLINE)
d.comment(0x917f, 'Dimension count starts at 1', align=Align.INLINE)
d.comment(0x9181, '...', align=Align.INLINE)
d.comment(0x9182, 'running size = 1', align=Align.INLINE)
d.comment(0x9185, 'Stack the running size', align=Align.INLINE)
d.comment(0x9188, 'Evaluate the next bound', align=Align.INLINE)
d.comment(0x918b, 'fits in 14 bits?', align=Align.INLINE)
d.comment(0x918d, '...', align=Align.INLINE)
d.comment(0x918f, '...', align=Align.INLINE)
d.comment(0x9191, '...', align=Align.INLINE)
d.comment(0x9193, 'no: Bad DIM', align=Align.INLINE)
d.comment(0x9195, 'Extent = bound + 1', align=Align.INLINE)
d.comment(0x9198, 'Restore the descriptor offset', align=Align.INLINE)
d.comment(0x9199, '...', align=Align.INLINE)
d.comment(0x919a, 'Store the extent in the descriptor', align=Align.INLINE)
d.comment(0x919c, '...', align=Align.INLINE)
d.comment(0x919e, '...', align=Align.INLINE)
d.comment(0x919f, '...', align=Align.INLINE)
d.comment(0x91a1, '...', align=Align.INLINE)
d.comment(0x91a3, '...', align=Align.INLINE)
d.comment(0x91a4, 'save the offset', align=Align.INLINE)
d.comment(0x91a5, '...', align=Align.INLINE)
d.comment(0x91a6, 'Multiply the running size by the extent', align=Align.INLINE)
d.comment(0x91a9, 'Skip spaces', align=Align.INLINE)
d.comment(0x91ac, "','  another dimension?", align=Align.INLINE)
d.comment(0x91ae, 'yes', align=Align.INLINE)
d.comment(0x91b0, "')' end of dimensions?", align=Align.INLINE)
d.comment(0x91b2, 'yes', align=Align.INLINE)
d.comment(0x91b4, 'otherwise Bad DIM', align=Align.INLINE)
d.comment(0x91b7, 'Recover the element size', align=Align.INLINE)
d.comment(0x91b8, '...', align=Align.INLINE)
d.comment(0x91ba, '...', align=Align.INLINE)
d.comment(0x91bb, '...', align=Align.INLINE)
d.comment(0x91bd, '...', align=Align.INLINE)
d.comment(0x91bf, '...', align=Align.INLINE)
d.comment(0x91c1, 'Total = element count * element size', align=Align.INLINE)
d.comment(0x91c4, 'Store the dimension count in the descriptor',
          align=Align.INLINE)
d.comment(0x91c6, '...', align=Align.INLINE)
d.comment(0x91c8, '...', align=Align.INLINE)
d.comment(0x91ca, 'Add it to the total size', align=Align.INLINE)
d.comment(0x91cc, '...', align=Align.INLINE)
d.comment(0x91ce, '...', align=Align.INLINE)
d.comment(0x91d0, '...', align=Align.INLINE)
d.comment(0x91d2, 'Point at the current variable top', align=Align.INLINE)
d.comment(0x91d4, '...', align=Align.INLINE)
d.comment(0x91d6, '...', align=Align.INLINE)
d.comment(0x91d8, '...', align=Align.INLINE)
d.comment(0x91da, 'New top = top + total size', align=Align.INLINE)
d.comment(0x91db, '...', align=Align.INLINE)
d.comment(0x91dd, '...', align=Align.INLINE)
d.comment(0x91de, '...', align=Align.INLINE)
d.comment(0x91e0, '...', align=Align.INLINE)
d.comment(0x91e2, 'overflow: No room', align=Align.INLINE)
d.comment(0x91e4, '...', align=Align.INLINE)
d.comment(0x91e5, 'collides with the stack?', align=Align.INLINE)
d.comment(0x91e7, '...', align=Align.INLINE)
d.comment(0x91e9, 'yes: No room', align=Align.INLINE)
d.comment(0x91eb, 'Commit the new variable top', align=Align.INLINE)
d.comment(0x91ed, '...', align=Align.INLINE)
d.comment(0x91ef, 'Zero the array storage from the old top', align=Align.INLINE)
d.comment(0x91f1, '...', align=Align.INLINE)
d.comment(0x91f3, '...', align=Align.INLINE)
d.comment(0x91f4, '...', align=Align.INLINE)
d.comment(0x91f6, '...', align=Align.INLINE)
d.comment(0x91f8, '...', align=Align.INLINE)
d.comment(0x91fa, '...', align=Align.INLINE)
d.comment(0x91fc, 'store a zero byte', align=Align.INLINE)
d.comment(0x91fe, '...', align=Align.INLINE)
d.comment(0x91ff, '...', align=Align.INLINE)
d.comment(0x9201, '...', align=Align.INLINE)
d.comment(0x9203, 'reached the new top?', align=Align.INLINE)
d.comment(0x9205, '...', align=Align.INLINE)
d.comment(0x9207, '...', align=Align.INLINE)
d.comment(0x9209, 'loop', align=Align.INLINE)
d.comment(0x920b, 'Skip spaces', align=Align.INLINE)
d.comment(0x920e, "','  another array?", align=Align.INLINE)
d.comment(0x9210, 'yes', align=Align.INLINE)
d.comment(0x9212, 'no: next statement', align=Align.INLINE)
d.comment(0x9215, 'DIM the next array', align=Align.INLINE)
d.comment(0x9218, 'No room error', align=Align.INLINE)

# ----------------------------------------------------------------------
# stmt_on (&B915): ON ERROR, or ON n GOTO/GOSUB <list>.
# Evaluates n and selects the n-th destination in the comma-separated
# list; an out-of-range n falls through to a trailing ELSE or raises
# ON range.
# ----------------------------------------------------------------------
d.comment(0xb915, 'Next character', align=Align.INLINE)
d.comment(0xb918, 'ERROR token?', align=Align.INLINE)
d.comment(0xb91a, 'yes: ON ERROR', align=Align.INLINE)
d.comment(0xb91c, 'Back up over the character', align=Align.INLINE)
d.comment(0xb91e, 'Evaluate the selector', align=Align.INLINE)
d.comment(0xb921, 'coerce to integer', align=Align.INLINE)
d.comment(0xb924, 'Advance past it', align=Align.INLINE)
d.comment(0xb926, '...', align=Align.INLINE)
d.comment(0xb927, '...', align=Align.INLINE)
d.comment(0xb929, 'GOTO token?', align=Align.INLINE)
d.comment(0xb92b, 'yes', align=Align.INLINE)
d.comment(0xb92d, 'GOSUB token?', align=Align.INLINE)
d.comment(0xb92f, 'no: syntax error', align=Align.INLINE)
d.comment(0xb931, 'Save the GOTO/GOSUB token', align=Align.INLINE)
d.comment(0xb932, '...', align=Align.INLINE)
d.comment(0xb933, 'Selector > 255?', align=Align.INLINE)
d.comment(0xb935, '...', align=Align.INLINE)
d.comment(0xb937, '...', align=Align.INLINE)
d.comment(0xb939, 'yes: out of range', align=Align.INLINE)
d.comment(0xb93b, 'Selector zero?', align=Align.INLINE)
d.comment(0xb93d, 'yes: out of range', align=Align.INLINE)
d.comment(0xb93f, 'Count down to the n-th destination', align=Align.INLINE)
d.comment(0xb940, 'reached it: use the first', align=Align.INLINE)
d.comment(0xb942, 'Line index', align=Align.INLINE)
d.comment(0xb944, 'Next character', align=Align.INLINE)
d.comment(0xb946, '...', align=Align.INLINE)
d.comment(0xb947, 'end of line?', align=Align.INLINE)
d.comment(0xb949, 'yes: out of range', align=Align.INLINE)
d.comment(0xb94b, "':' end of statement?", align=Align.INLINE)
d.comment(0xb94d, 'yes: out of range', align=Align.INLINE)
d.comment(0xb94f, 'ELSE?', align=Align.INLINE)
d.comment(0xb951, 'yes: out of range', align=Align.INLINE)
d.comment(0xb953, "',' separator?", align=Align.INLINE)
d.comment(0xb955, 'no: keep scanning', align=Align.INLINE)
d.comment(0xb957, 'count this destination', align=Align.INLINE)
d.comment(0xb958, 'not yet reached: continue', align=Align.INLINE)
d.comment(0xb95a, 'Save the line index', align=Align.INLINE)
d.comment(0xb95c, 'Read the destination line number', align=Align.INLINE)
d.comment(0xb95f, 'Recover the token', align=Align.INLINE)
d.comment(0xb960, 'GOSUB?', align=Align.INLINE)
d.comment(0xb962, 'yes', align=Align.INLINE)
d.comment(0xb964, 'GOTO: update the index and check Escape',
          align=Align.INLINE)
d.comment(0xb967, 'jump to the line', align=Align.INLINE)
d.comment(0xb96a, 'GOSUB: line pointer', align=Align.INLINE)
d.comment(0xb96c, 'Next character', align=Align.INLINE)
d.comment(0xb96e, '...', align=Align.INLINE)
d.comment(0xb96f, 'end of line?', align=Align.INLINE)
d.comment(0xb971, 'yes: return point here', align=Align.INLINE)
d.comment(0xb973, "':' separator?", align=Align.INLINE)
d.comment(0xb975, 'no: keep scanning to the return point', align=Align.INLINE)
d.comment(0xb977, 'Set the return index', align=Align.INLINE)
d.comment(0xb978, '...', align=Align.INLINE)
d.comment(0xb97a, 'do the GOSUB', align=Align.INLINE)
d.comment(0xb97d, 'Out of range: line index', align=Align.INLINE)
d.comment(0xb97f, 'drop the token', align=Align.INLINE)
d.comment(0xb980, 'Next character', align=Align.INLINE)
d.comment(0xb982, '...', align=Align.INLINE)
d.comment(0xb983, 'ELSE?', align=Align.INLINE)
d.comment(0xb985, 'yes: use it', align=Align.INLINE)
d.comment(0xb987, 'end of line?', align=Align.INLINE)
d.comment(0xb989, 'no: keep scanning', align=Align.INLINE)
d.comment(0xb98b, 'ON range error', align=Align.INLINE)
d.comment(0xb995, 'Step past ELSE', align=Align.INLINE)
d.comment(0xb997, 'execute what follows', align=Align.INLINE)

# ----------------------------------------------------------------------
# find_program_line (&9970): find the first line >= the target number.
# Walks the program from PAGE. Each line is <&0D> <hi> <lo> <len> <body>,
# stored in ascending order. Returns the line pointer in &3D/&3E; carry
# is clear when an exact match is found.
# ----------------------------------------------------------------------
d.comment(0x9970, 'Pointer low = 0', align=Align.INLINE)
d.comment(0x9972, '...', align=Align.INLINE)
d.comment(0x9974, 'Pointer high = PAGE', align=Align.INLINE)
d.comment(0x9976, '...', align=Align.INLINE)
d.comment(0x9978, "This line's number: high byte", align=Align.INLINE)
d.comment(0x997a, '...', align=Align.INLINE)
d.comment(0x997c, 'vs the target high byte', align=Align.INLINE)
d.comment(0x997e, '>=: a candidate', align=Align.INLINE)
d.comment(0x9980, 'Line length', align=Align.INLINE)
d.comment(0x9982, '...', align=Align.INLINE)
d.comment(0x9984, 'Advance to the next line', align=Align.INLINE)
d.comment(0x9986, '...', align=Align.INLINE)
d.comment(0x9988, '...', align=Align.INLINE)
d.comment(0x998a, '...', align=Align.INLINE)
d.comment(0x998c, 'continue', align=Align.INLINE)
d.comment(0x998e, 'high byte greater: found (not exact)', align=Align.INLINE)
d.comment(0x9990, "This line's number: low byte", align=Align.INLINE)
d.comment(0x9992, '...', align=Align.INLINE)
d.comment(0x9994, 'vs the target low byte', align=Align.INLINE)
d.comment(0x9996, 'less: next line', align=Align.INLINE)
d.comment(0x9998, 'greater: found (not exact)', align=Align.INLINE)
d.comment(0x999a, 'Exact match: leave the pointer at this line',
          align=Align.INLINE)
d.comment(0x999b, '...', align=Align.INLINE)
d.comment(0x999d, '...', align=Align.INLINE)
d.comment(0x999f, '...', align=Align.INLINE)
d.comment(0x99a1, '...', align=Align.INLINE)
d.comment(0x99a3, 'flag the exact match (carry clear)', align=Align.INLINE)
d.comment(0x99a4, 'Point at the line number', align=Align.INLINE)
d.comment(0x99a6, 'Return', align=Align.INLINE)

# find_line_target (&B99A): read a line number then locate the line.
d.comment(0xb99a, 'Embedded line-number token?', align=Align.INLINE)
d.comment(0xb99d, 'yes: use it', align=Align.INLINE)
d.comment(0xb99f, 'Evaluate the line-number expression', align=Align.INLINE)
d.comment(0xb9a2, 'ensure integer', align=Align.INLINE)
d.comment(0xb9a5, 'Update the program pointer', align=Align.INLINE)
d.comment(0xb9a7, '...', align=Align.INLINE)
d.comment(0xb9a9, 'Mask the high byte to 7 bits', align=Align.INLINE)
d.comment(0xb9ab, '(so GOTO &8000+n == GOTO n)', align=Align.INLINE)
d.comment(0xb9ad, '...', align=Align.INLINE)
d.comment(0xb9af, 'Find the line', align=Align.INLINE)
d.comment(0xb9b2, 'not found: No such line', align=Align.INLINE)
d.comment(0xb9b4, 'Return', align=Align.INLINE)

# ----------------------------------------------------------------------
# assign_string (&8C1E): store the string buffer into a string variable.
# The variable descriptor at (&2A) holds the data pointer, the bytes
# allocated and the current length. If the new string fits the existing
# allocation it is reused; otherwise space is claimed at the string heap
# top (&02/&03), extending the block in place if it is already on top.
# The &80 type is a $addr indirection, stored with a CR terminator.
# ----------------------------------------------------------------------
d.comment(0x8c1e, 'Unstack the variable descriptor address', align=Align.INLINE)
d.comment(0x8c21, 'Variable type', align=Align.INLINE)
d.comment(0x8c25, 'yes', align=Align.INLINE)
d.comment(0x8c27, 'Bytes currently allocated', align=Align.INLINE)
d.comment(0x8c29, '...', align=Align.INLINE)
d.comment(0x8c2d, 'yes: reuse the allocation', align=Align.INLINE)
d.comment(0x8c31, '...', align=Align.INLINE)
d.comment(0x8c33, '...', align=Align.INLINE)
d.comment(0x8c35, '...', align=Align.INLINE)
d.comment(0x8c37, 'Round the size up (min 8, granularity 8)', align=Align.INLINE)
d.comment(0x8c39, '...', align=Align.INLINE)
d.comment(0x8c3b, '...', align=Align.INLINE)
d.comment(0x8c3d, '...', align=Align.INLINE)
d.comment(0x8c3f, '...', align=Align.INLINE)
d.comment(0x8c41, 'cap at 255', align=Align.INLINE)
d.comment(0x8c43, '...', align=Align.INLINE)
d.comment(0x8c44, 'Save the new allocation size', align=Align.INLINE)
d.comment(0x8c45, '...', align=Align.INLINE)
d.comment(0x8c46, 'Is the existing block at the heap top?', align=Align.INLINE)
d.comment(0x8c48, '...', align=Align.INLINE)
d.comment(0x8c4a, '(data address + allocated == top?)', align=Align.INLINE)
d.comment(0x8c4c, '...', align=Align.INLINE)
d.comment(0x8c4e, 'no: allocate fresh space', align=Align.INLINE)
d.comment(0x8c50, '...', align=Align.INLINE)
d.comment(0x8c51, '...', align=Align.INLINE)
d.comment(0x8c53, '...', align=Align.INLINE)
d.comment(0x8c55, 'no: allocate fresh space', align=Align.INLINE)
d.comment(0x8c57, 'yes: extend in place from this block', align=Align.INLINE)
d.comment(0x8c59, '...', align=Align.INLINE)
d.comment(0x8c5a, '...', align=Align.INLINE)
d.comment(0x8c5b, '...', align=Align.INLINE)
d.comment(0x8c5c, 'reclaim the old allocation', align=Align.INLINE)
d.comment(0x8c5e, '...', align=Align.INLINE)
d.comment(0x8c5f, 'New heap top = top + allocation', align=Align.INLINE)
d.comment(0x8c60, '...', align=Align.INLINE)
d.comment(0x8c61, '...', align=Align.INLINE)
d.comment(0x8c63, '...', align=Align.INLINE)
d.comment(0x8c64, '...', align=Align.INLINE)
d.comment(0x8c66, '...', align=Align.INLINE)
d.comment(0x8c68, 'collides with the stack?', align=Align.INLINE)
d.comment(0x8c6a, '...', align=Align.INLINE)
d.comment(0x8c6b, '...', align=Align.INLINE)
d.comment(0x8c6d, 'yes: No room', align=Align.INLINE)
d.comment(0x8c6f, 'Commit the new heap top', align=Align.INLINE)
d.comment(0x8c71, '...', align=Align.INLINE)
d.comment(0x8c73, 'Store the new allocation size', align=Align.INLINE)
d.comment(0x8c74, '...', align=Align.INLINE)
d.comment(0x8c76, '...', align=Align.INLINE)
d.comment(0x8c78, 'Store the new data address', align=Align.INLINE)
d.comment(0x8c79, '...', align=Align.INLINE)
d.comment(0x8c7b, 'extended in place: keep the address', align=Align.INLINE)
d.comment(0x8c7d, '...', align=Align.INLINE)
d.comment(0x8c7f, '...', align=Align.INLINE)
d.comment(0x8c80, '...', align=Align.INLINE)
d.comment(0x8c82, '...', align=Align.INLINE)
d.comment(0x8c84, 'Store the current length', align=Align.INLINE)
d.comment(0x8c86, '...', align=Align.INLINE)
d.comment(0x8c88, '...', align=Align.INLINE)
d.comment(0x8c8a, 'empty string: done', align=Align.INLINE)
d.comment(0x8c8c, 'Fetch the data address', align=Align.INLINE)
d.comment(0x8c8d, '...', align=Align.INLINE)
d.comment(0x8c8e, '...', align=Align.INLINE)
d.comment(0x8c90, '...', align=Align.INLINE)
d.comment(0x8c92, '...', align=Align.INLINE)
d.comment(0x8c93, '...', align=Align.INLINE)
d.comment(0x8c95, '...', align=Align.INLINE)
d.comment(0x8c97, 'Copy the string buffer to the storage', align=Align.INLINE)
d.comment(0x8c9a, '...', align=Align.INLINE)
d.comment(0x8c9c, '...', align=Align.INLINE)
d.comment(0x8c9d, '...', align=Align.INLINE)
d.comment(0x8c9f, 'loop', align=Align.INLINE)
d.comment(0x8ca1, 'Return', align=Align.INLINE)
d.comment(0x8ca2, '$addr: prepare the destination', align=Align.INLINE)
d.comment(0x8ca5, 'empty string?', align=Align.INLINE)
d.comment(0x8ca7, 'yes: just the terminator', align=Align.INLINE)
d.comment(0x8ca9, 'Copy the string to the address', align=Align.INLINE)
d.comment(0x8cac, '...', align=Align.INLINE)
d.comment(0x8cae, '...', align=Align.INLINE)
d.comment(0x8caf, 'loop', align=Align.INLINE)
d.comment(0x8cb1, 'First character', align=Align.INLINE)
d.comment(0x8cb4, 'Store it (with the CR terminator following)',
          align=Align.INLINE)
d.comment(0x8cb6, 'Return', align=Align.INLINE)
d.comment(0x8cb7, 'No room error', align=Align.INLINE)

# unstack_value_to_var (&8CC1): pop a stacked value into a variable.
d.comment(0x8cc1, 'Type/size byte', align=Align.INLINE)
d.comment(0x8cc3, '$addr string?', align=Align.INLINE)
d.comment(0x8cc5, 'yes', align=Align.INLINE)
d.comment(0x8cc7, 'numeric?', align=Align.INLINE)
d.comment(0x8cc9, 'String variable: length on the stack', align=Align.INLINE)
d.comment(0x8ccb, '...', align=Align.INLINE)
d.comment(0x8ccd, '...', align=Align.INLINE)
d.comment(0x8cce, 'empty: just set the length', align=Align.INLINE)
d.comment(0x8cd0, 'Data address - 1 (for 1-based copy)', align=Align.INLINE)
d.comment(0x8cd2, '...', align=Align.INLINE)
d.comment(0x8cd4, '...', align=Align.INLINE)
d.comment(0x8cd6, '...', align=Align.INLINE)
d.comment(0x8cd7, '...', align=Align.INLINE)
d.comment(0x8cd9, '...', align=Align.INLINE)
d.comment(0x8cdb, '...', align=Align.INLINE)
d.comment(0x8cdd, 'Copy the string bytes', align=Align.INLINE)
d.comment(0x8cdf, '...', align=Align.INLINE)
d.comment(0x8ce1, '...', align=Align.INLINE)
d.comment(0x8ce2, '...', align=Align.INLINE)
d.comment(0x8ce3, 'loop', align=Align.INLINE)
d.comment(0x8ce5, 'String length', align=Align.INLINE)
d.comment(0x8ce7, 'descriptor offset 3', align=Align.INLINE)
d.comment(0x8ce9, 'Store the length', align=Align.INLINE)
d.comment(0x8ceb, 'drop the value from the stack', align=Align.INLINE)
d.comment(0x8cee, '$addr: length on the stack', align=Align.INLINE)
d.comment(0x8cf0, '...', align=Align.INLINE)
d.comment(0x8cf2, '...', align=Align.INLINE)
d.comment(0x8cf3, 'empty: just the terminator', align=Align.INLINE)
d.comment(0x8cf5, 'Copy the string to the address', align=Align.INLINE)
d.comment(0x8cf6, '...', align=Align.INLINE)
d.comment(0x8cf8, '...', align=Align.INLINE)
d.comment(0x8cf9, '...', align=Align.INLINE)
d.comment(0x8cfb, '...', align=Align.INLINE)
d.comment(0x8cfc, '...', align=Align.INLINE)
d.comment(0x8cfd, 'loop', align=Align.INLINE)
d.comment(0x8cff, 'CR terminator', align=Align.INLINE)
d.comment(0x8d01, 'store it', align=Align.INLINE)
d.comment(0x8d03, 'Numeric: copy byte 0', align=Align.INLINE)
d.comment(0x8d05, '...', align=Align.INLINE)
d.comment(0x8d07, '...', align=Align.INLINE)
d.comment(0x8d09, '...', align=Align.INLINE)
d.comment(0x8d0a, 'all bytes done?', align=Align.INLINE)
d.comment(0x8d0c, 'yes', align=Align.INLINE)
d.comment(0x8d0e, 'Copy byte 1', align=Align.INLINE)
d.comment(0x8d10, '...', align=Align.INLINE)
d.comment(0x8d12, 'byte 2', align=Align.INLINE)
d.comment(0x8d13, '...', align=Align.INLINE)
d.comment(0x8d15, '...', align=Align.INLINE)
d.comment(0x8d17, 'byte 3', align=Align.INLINE)
d.comment(0x8d18, '...', align=Align.INLINE)
d.comment(0x8d1a, '...', align=Align.INLINE)
d.comment(0x8d1c, '...', align=Align.INLINE)
d.comment(0x8d1d, 'all bytes done?', align=Align.INLINE)
d.comment(0x8d1f, 'yes', align=Align.INLINE)
d.comment(0x8d21, 'byte 4 (real only)', align=Align.INLINE)
d.comment(0x8d23, '...', align=Align.INLINE)
d.comment(0x8d25, '...', align=Align.INLINE)
d.comment(0x8d26, 'Bytes copied', align=Align.INLINE)
d.comment(0x8d27, '...', align=Align.INLINE)
d.comment(0x8d28, 'drop them from the stack', align=Align.INLINE)

# ----------------------------------------------------------------------
# fn_eval (&ABE9): EVAL string$ - tokenise and evaluate at run time.
# Appends a CR to the argument string, stacks it (so string operations
# during evaluation cannot clobber it), points the parser at the stacked
# copy, tokenises it in place and runs the expression evaluator.
# ----------------------------------------------------------------------
d.comment(0xabe9, 'Evaluate the argument string', align=Align.INLINE)
d.comment(0xabec, 'not a string: error', align=Align.INLINE)
d.comment(0xabee, 'Append a CR terminator', align=Align.INLINE)
d.comment(0xabf0, '...', align=Align.INLINE)
d.comment(0xabf2, '...', align=Align.INLINE)
d.comment(0xabf4, '...', align=Align.INLINE)
d.comment(0xabf7, 'Stack the string', align=Align.INLINE)
d.comment(0xabfa, 'Save the parser pointer', align=Align.INLINE)
d.comment(0xabfc, '...', align=Align.INLINE)
d.comment(0xabfd, '...', align=Align.INLINE)
d.comment(0xabff, '...', align=Align.INLINE)
d.comment(0xac00, '...', align=Align.INLINE)
d.comment(0xac02, '...', align=Align.INLINE)
d.comment(0xac03, 'Point at the stacked string', align=Align.INLINE)
d.comment(0xac05, '...', align=Align.INLINE)
d.comment(0xac07, 'step over the length byte', align=Align.INLINE)
d.comment(0xac08, 'parser pointer low', align=Align.INLINE)
d.comment(0xac0a, 'name pointer low', align=Align.INLINE)
d.comment(0xac0c, '...', align=Align.INLINE)
d.comment(0xac0e, 'carry into the high byte', align=Align.INLINE)
d.comment(0xac0f, 'parser pointer high', align=Align.INLINE)
d.comment(0xac11, 'name pointer high', align=Align.INLINE)
d.comment(0xac13, 'Quote flag reset', align=Align.INLINE)
d.comment(0xac15, '...', align=Align.INLINE)
d.comment(0xac17, 'Offset back to the start', align=Align.INLINE)
d.comment(0xac18, '...', align=Align.INLINE)
d.comment(0xac1a, 'Tokenise the stacked string', align=Align.INLINE)
d.comment(0xac1d, 'Evaluate the expression', align=Align.INLINE)
d.comment(0xac20, 'Drop the stacked string', align=Align.INLINE)
d.comment(0xac23, 'Restore the parser pointer', align=Align.INLINE)
d.comment(0xac24, '...', align=Align.INLINE)
d.comment(0xac26, '...', align=Align.INLINE)
d.comment(0xac27, '...', align=Align.INLINE)
d.comment(0xac29, '...', align=Align.INLINE)
d.comment(0xac2a, '...', align=Align.INLINE)
d.comment(0xac2c, 'Result type', align=Align.INLINE)
d.comment(0xac2e, 'Return', align=Align.INLINE)

# ----------------------------------------------------------------------
# call_proc_fn (&B197): invoke a PROC or FN.
# Saves the 6502 stack onto the BASIC stack (so calls can nest beyond
# 256 bytes / recurse), pushes the return context, parses and locates
# the definition (heap cache then program scan), runs the body, restores
# any LOCAL/parameter values, and unwinds the saved stack.
# ----------------------------------------------------------------------
d.comment(0xb197, 'Save the PROC/FN token', align=Align.INLINE)
d.comment(0xb19a, '...', align=Align.INLINE)
d.comment(0xb19b, '...', align=Align.INLINE)
d.comment(0xb19c, 'Drop the BASIC stack by the 6502 stack size',
          align=Align.INLINE)
d.comment(0xb1a1, 'Store the 6502 stack pointer first', align=Align.INLINE)
d.comment(0xb1a3, '...', align=Align.INLINE)
d.comment(0xb1a4, '...', align=Align.INLINE)
d.comment(0xb1a6, 'Copy each 6502 stack byte', align=Align.INLINE)
d.comment(0xb1a7, '...', align=Align.INLINE)
d.comment(0xb1a8, '...', align=Align.INLINE)
d.comment(0xb1ab, '...', align=Align.INLINE)
d.comment(0xb1ad, '...', align=Align.INLINE)
d.comment(0xb1af, 'loop', align=Align.INLINE)
d.comment(0xb1b1, 'Empty the 6502 stack', align=Align.INLINE)
d.comment(0xb1b2, 'PROC/FN token', align=Align.INLINE)
d.comment(0xb1b5, 'return line offset', align=Align.INLINE)
d.comment(0xb1b7, '...', align=Align.INLINE)
d.comment(0xb1b8, 'return line pointer', align=Align.INLINE)
d.comment(0xb1ba, '...', align=Align.INLINE)
d.comment(0xb1bb, '...', align=Align.INLINE)
d.comment(0xb1bd, '...', align=Align.INLINE)
d.comment(0xb1be, 'Point &37/&38 at the PROC/FN name', align=Align.INLINE)
d.comment(0xb1c0, '...', align=Align.INLINE)
d.comment(0xb1c1, '...', align=Align.INLINE)
d.comment(0xb1c2, '...', align=Align.INLINE)
d.comment(0xb1c4, '...', align=Align.INLINE)
d.comment(0xb1c6, '...', align=Align.INLINE)
d.comment(0xb1c8, '...', align=Align.INLINE)
d.comment(0xb1c9, '...', align=Align.INLINE)
d.comment(0xb1ca, '...', align=Align.INLINE)
d.comment(0xb1cc, '...', align=Align.INLINE)
d.comment(0xb1ce, '...', align=Align.INLINE)
d.comment(0xb1cf, '...', align=Align.INLINE)
d.comment(0xb1d1, '...', align=Align.INLINE)
d.comment(0xb1d3, 'Validate the name', align=Align.INLINE)
d.comment(0xb1d5, '...', align=Align.INLINE)
d.comment(0xb1d8, 'no valid characters?', align=Align.INLINE)
d.comment(0xb1da, 'yes: Bad call', align=Align.INLINE)
d.comment(0xb1dc, 'Offset past the name', align=Align.INLINE)
d.comment(0xb1de, 'Name length', align=Align.INLINE)
d.comment(0xb1df, '...', align=Align.INLINE)
d.comment(0xb1e1, 'Look it up in the heap cache', align=Align.INLINE)
d.comment(0xb1e4, 'found: jump to it', align=Align.INLINE)
d.comment(0xb1e6, 'not cached: scan the program', align=Align.INLINE)
d.comment(0xb1e9, 'Set PtrA to the definition address', align=Align.INLINE)
d.comment(0xb1eb, '...', align=Align.INLINE)
d.comment(0xb1ed, '...', align=Align.INLINE)
d.comment(0xb1ef, '...', align=Align.INLINE)
d.comment(0xb1f0, '...', align=Align.INLINE)
d.comment(0xb1f2, '...', align=Align.INLINE)
d.comment(0xb1f4, 'Push the parameter count (0 so far)', align=Align.INLINE)
d.comment(0xb1f6, '...', align=Align.INLINE)
d.comment(0xb1f7, '...', align=Align.INLINE)
d.comment(0xb1f9, 'Next character', align=Align.INLINE)
d.comment(0xb1fc, "'(' parameters?", align=Align.INLINE)
d.comment(0xb1fe, 'yes: bind them', align=Align.INLINE)
d.comment(0xb200, 'no: back up', align=Align.INLINE)
d.comment(0xb202, 'Save the parser pointer', align=Align.INLINE)
d.comment(0xb204, '...', align=Align.INLINE)
d.comment(0xb205, '...', align=Align.INLINE)
d.comment(0xb207, '...', align=Align.INLINE)
d.comment(0xb208, '...', align=Align.INLINE)
d.comment(0xb20a, '...', align=Align.INLINE)
d.comment(0xb20b, 'Execute the body', align=Align.INLINE)
d.comment(0xb20e, 'Restore the parser pointer', align=Align.INLINE)
d.comment(0xb20f, '...', align=Align.INLINE)
d.comment(0xb211, '...', align=Align.INLINE)
d.comment(0xb212, '...', align=Align.INLINE)
d.comment(0xb214, '...', align=Align.INLINE)
d.comment(0xb215, '...', align=Align.INLINE)
d.comment(0xb217, 'Number of LOCAL/parameter values to restore',
          align=Align.INLINE)
d.comment(0xb218, 'none: skip', align=Align.INLINE)
d.comment(0xb21a, 'count', align=Align.INLINE)
d.comment(0xb21c, 'Unstack the variable address', align=Align.INLINE)
d.comment(0xb21f, 'restore its saved value', align=Align.INLINE)
d.comment(0xb222, 'one done', align=Align.INLINE)
d.comment(0xb224, 'loop', align=Align.INLINE)
d.comment(0xb226, 'Restore PtrA', align=Align.INLINE)
d.comment(0xb227, '...', align=Align.INLINE)
d.comment(0xb229, '...', align=Align.INLINE)
d.comment(0xb22a, '...', align=Align.INLINE)
d.comment(0xb22c, '...', align=Align.INLINE)
d.comment(0xb22d, '...', align=Align.INLINE)
d.comment(0xb22f, 'Recover the saved 6502 stack pointer', align=Align.INLINE)
d.comment(0xb230, '...', align=Align.INLINE)
d.comment(0xb232, '...', align=Align.INLINE)
d.comment(0xb234, '...', align=Align.INLINE)
d.comment(0xb235, 'restore it', align=Align.INLINE)
d.comment(0xb236, 'Copy each byte back to the 6502 stack', align=Align.INLINE)
d.comment(0xb237, '...', align=Align.INLINE)
d.comment(0xb238, '...', align=Align.INLINE)
d.comment(0xb23a, '...', align=Align.INLINE)
d.comment(0xb23d, '...', align=Align.INLINE)
d.comment(0xb23f, 'loop', align=Align.INLINE)
d.comment(0xb241, 'Adjust the BASIC stack pointer back up', align=Align.INLINE)
d.comment(0xb242, '...', align=Align.INLINE)
d.comment(0xb244, '...', align=Align.INLINE)
d.comment(0xb246, '...', align=Align.INLINE)
d.comment(0xb248, '...', align=Align.INLINE)
d.comment(0xb24a, 'Return the PROC/FN token', align=Align.INLINE)
d.comment(0xb24c, 'Return', align=Align.INLINE)

# Parameter binding (&B24D): collect the formal parameters.
# Each formal variable's current value is stacked (for LOCAL-style
# restore on return) and its identity recorded, then the actual
# arguments are evaluated and assigned.
d.comment(0xb24d, 'Save the parser pointer', align=Align.INLINE)
d.comment(0xb24f, '...', align=Align.INLINE)
d.comment(0xb250, '...', align=Align.INLINE)
d.comment(0xb252, '...', align=Align.INLINE)
d.comment(0xb253, '...', align=Align.INLINE)
d.comment(0xb255, '...', align=Align.INLINE)
d.comment(0xb256, 'Parse a formal parameter variable', align=Align.INLINE)
d.comment(0xb259, 'invalid: error', align=Align.INLINE)
d.comment(0xb25b, 'Update the program pointer', align=Align.INLINE)
d.comment(0xb25d, '...', align=Align.INLINE)
d.comment(0xb25f, 'Restore the parser pointer', align=Align.INLINE)
d.comment(0xb260, '...', align=Align.INLINE)
d.comment(0xb262, '...', align=Align.INLINE)
d.comment(0xb263, '...', align=Align.INLINE)
d.comment(0xb265, '...', align=Align.INLINE)
d.comment(0xb266, '...', align=Align.INLINE)
d.comment(0xb268, 'Recover the running count', align=Align.INLINE)
d.comment(0xb269, '...', align=Align.INLINE)
d.comment(0xb26a, "Push the formal's type/address", align=Align.INLINE)
d.comment(0xb26c, '...', align=Align.INLINE)
d.comment(0xb26d, '...', align=Align.INLINE)
d.comment(0xb26f, '...', align=Align.INLINE)
d.comment(0xb270, '...', align=Align.INLINE)
d.comment(0xb272, '...', align=Align.INLINE)
d.comment(0xb273, 'count this parameter', align=Align.INLINE)
d.comment(0xb274, '...', align=Align.INLINE)
d.comment(0xb275, '...', align=Align.INLINE)
d.comment(0xb276, 'Stack the current value for LOCAL restore',
          align=Align.INLINE)
d.comment(0xb279, 'Skip spaces', align=Align.INLINE)
d.comment(0xb27c, "','  another parameter?", align=Align.INLINE)
d.comment(0xb27e, 'yes', align=Align.INLINE)
d.comment(0xb280, "')' end of parameter list?", align=Align.INLINE)
d.comment(0xb282, 'no: error', align=Align.INLINE)
d.comment(0xb284, 'Push the end marker', align=Align.INLINE)
d.comment(0xb286, '...', align=Align.INLINE)
d.comment(0xb287, 'Expect "(" for the arguments', align=Align.INLINE)
d.comment(0xb28a, '...', align=Align.INLINE)
d.comment(0xb28c, 'missing: error', align=Align.INLINE)
# Evaluate the actual arguments and bind them to the formals.
d.comment(0xb28e, 'Evaluate an argument', align=Align.INLINE)
d.comment(0xb291, 'stack its value', align=Align.INLINE)
d.comment(0xb294, 'save the type', align=Align.INLINE)
d.comment(0xb296, '...', align=Align.INLINE)
d.comment(0xb298, 'stack the type', align=Align.INLINE)
d.comment(0xb29b, 'Bump the argument count', align=Align.INLINE)
d.comment(0xb29c, '...', align=Align.INLINE)
d.comment(0xb29d, '...', align=Align.INLINE)
d.comment(0xb29e, '...', align=Align.INLINE)
d.comment(0xb29f, '...', align=Align.INLINE)
d.comment(0xb2a0, 'Skip spaces', align=Align.INLINE)
d.comment(0xb2a3, "','  another argument?", align=Align.INLINE)
d.comment(0xb2a5, 'yes', align=Align.INLINE)
d.comment(0xb2a7, "')' end of arguments?", align=Align.INLINE)
d.comment(0xb2a9, 'no: error', align=Align.INLINE)
d.comment(0xb2ab, 'Recover the argument count', align=Align.INLINE)
d.comment(0xb2ac, 'and the formal count', align=Align.INLINE)
d.comment(0xb2ad, '...', align=Align.INLINE)
d.comment(0xb2af, '...', align=Align.INLINE)
d.comment(0xb2b1, 'counts match?', align=Align.INLINE)
d.comment(0xb2b3, 'yes: bind them', align=Align.INLINE)
d.comment(0xb2b5, 'Reset the stack', align=Align.INLINE)
d.comment(0xb2b7, '...', align=Align.INLINE)
d.comment(0xb2b8, 'restore PtrA', align=Align.INLINE)
d.comment(0xb2b9, '...', align=Align.INLINE)
d.comment(0xb2bb, '...', align=Align.INLINE)
d.comment(0xb2bc, '...', align=Align.INLINE)
d.comment(0xb2be, 'Arguments error', align=Align.INLINE)
d.comment(0xb2ca, 'Unstack the argument type', align=Align.INLINE)
d.comment(0xb2cd, 'Unstack the formal address/type', align=Align.INLINE)
d.comment(0xb2ce, '...', align=Align.INLINE)
d.comment(0xb2d0, '...', align=Align.INLINE)
d.comment(0xb2d1, '...', align=Align.INLINE)
d.comment(0xb2d3, '...', align=Align.INLINE)
d.comment(0xb2d4, '...', align=Align.INLINE)
d.comment(0xb2d6, 'string formal?', align=Align.INLINE)
d.comment(0xb2d8, 'Argument type', align=Align.INLINE)
d.comment(0xb2da, 'string argument: Arguments error', align=Align.INLINE)
d.comment(0xb2dc, 'numeric: set the formal address', align=Align.INLINE)
d.comment(0xb2de, '...', align=Align.INLINE)
d.comment(0xb2e0, '...', align=Align.INLINE)
d.comment(0xb2e3, 'Argument type', align=Align.INLINE)
d.comment(0xb2e5, 'integer?', align=Align.INLINE)
d.comment(0xb2e7, 'real: unstack the real value', align=Align.INLINE)
d.comment(0xb2ea, '...', align=Align.INLINE)
d.comment(0xb2ed, 'assign it', align=Align.INLINE)
d.comment(0xb2f0, 'unstack the integer value', align=Align.INLINE)
d.comment(0xb2f3, 'Assign to the formal', align=Align.INLINE)
d.comment(0xb2f6, 'next argument', align=Align.INLINE)
d.comment(0xb2f9, 'String formal: argument type', align=Align.INLINE)
d.comment(0xb2fb, 'numeric argument: Arguments error', align=Align.INLINE)
d.comment(0xb2fd, 'Unstack the string', align=Align.INLINE)
d.comment(0xb300, 'assign it', align=Align.INLINE)
d.comment(0xb303, 'One parameter bound', align=Align.INLINE)
d.comment(0xb305, 'loop', align=Align.INLINE)
d.comment(0xb307, 'Push the parameter count for restore', align=Align.INLINE)
d.comment(0xb309, '...', align=Align.INLINE)
d.comment(0xb30a, 'Execute the body', align=Align.INLINE)

# delete_program_line (&BC2D): remove a line and compact memory.
d.comment(0xbc2d, 'Find the line', align=Align.INLINE)
d.comment(0xbc30, 'not present: nothing to do', align=Align.INLINE)
d.comment(0xbc32, 'Destination = line start', align=Align.INLINE)
d.comment(0xbc34, '...', align=Align.INLINE)
d.comment(0xbc36, '...', align=Align.INLINE)
d.comment(0xbc38, '...', align=Align.INLINE)
d.comment(0xbc3a, '...', align=Align.INLINE)
d.comment(0xbc3c, '...', align=Align.INLINE)
d.comment(0xbc3e, '...', align=Align.INLINE)
d.comment(0xbc40, '...', align=Align.INLINE)
d.comment(0xbc42, '...', align=Align.INLINE)
d.comment(0xbc44, '...', align=Align.INLINE)
d.comment(0xbc46, "Line length", align=Align.INLINE)
d.comment(0xbc48, '...', align=Align.INLINE)
d.comment(0xbc4a, 'Source = the next line', align=Align.INLINE)
d.comment(0xbc4b, '...', align=Align.INLINE)
d.comment(0xbc4d, '...', align=Align.INLINE)
d.comment(0xbc4f, '...', align=Align.INLINE)
d.comment(0xbc51, '...', align=Align.INLINE)
d.comment(0xbc53, 'From offset 0', align=Align.INLINE)
d.comment(0xbc55, 'Copy a byte down', align=Align.INLINE)
d.comment(0xbc57, '...', align=Align.INLINE)
d.comment(0xbc59, 'end of line?', align=Align.INLINE)
d.comment(0xbc5b, 'yes: handle the line boundary', align=Align.INLINE)
d.comment(0xbc5d, 'next byte', align=Align.INLINE)
d.comment(0xbc5e, '...', align=Align.INLINE)
d.comment(0xbc60, 'cross a page', align=Align.INLINE)
d.comment(0xbc62, '...', align=Align.INLINE)
d.comment(0xbc64, 'continue', align=Align.INLINE)
d.comment(0xbc66, 'Step past the CR', align=Align.INLINE)
d.comment(0xbc67, '...', align=Align.INLINE)
d.comment(0xbc69, '...', align=Align.INLINE)
d.comment(0xbc6b, '...', align=Align.INLINE)
d.comment(0xbc6d, 'Next line marker', align=Align.INLINE)
d.comment(0xbc6f, '...', align=Align.INLINE)
d.comment(0xbc71, 'end of program?', align=Align.INLINE)
d.comment(0xbc73, 'no: copy the line number', align=Align.INLINE)
d.comment(0xbc76, '...and the length byte', align=Align.INLINE)
d.comment(0xbc79, 'continue with the line body', align=Align.INLINE)
d.comment(0xbc7c, 'Set the new top of program', align=Align.INLINE)
d.comment(0xbc7f, '...', align=Align.INLINE)
d.comment(0xbc80, 'Return', align=Align.INLINE)
d.comment(0xbc81, 'Copy one byte (source -> destination)', align=Align.INLINE)
d.comment(0xbc82, '...', align=Align.INLINE)
d.comment(0xbc84, 'cross a page', align=Align.INLINE)
d.comment(0xbc86, '...', align=Align.INLINE)
d.comment(0xbc88, '...', align=Align.INLINE)
d.comment(0xbc8a, '...', align=Align.INLINE)
d.comment(0xbc8c, 'Return', align=Align.INLINE)

# Insert a program line (&BC8D): make room and store the typed line.
d.comment(0xbc8d, 'Save the line-buffer pointer', align=Align.INLINE)
d.comment(0xbc8f, 'Delete any existing line with this number',
          align=Align.INLINE)
d.comment(0xbc92, 'Point past the line header', align=Align.INLINE)
d.comment(0xbc94, '...', align=Align.INLINE)
d.comment(0xbc96, 'Measure the new line: from offset 0', align=Align.INLINE)
d.comment(0xbc98, 'CR', align=Align.INLINE)
d.comment(0xbc9a, 'empty line (deletion only)?', align=Align.INLINE)
d.comment(0xbc9c, 'yes: done', align=Align.INLINE)
d.comment(0xbc9e, 'Scan to the CR', align=Align.INLINE)
d.comment(0xbc9f, '...', align=Align.INLINE)
d.comment(0xbca1, '...', align=Align.INLINE)
d.comment(0xbca3, 'Add the 4-byte header', align=Align.INLINE)
d.comment(0xbca4, '(continued)', align=Align.INLINE)
d.comment(0xbca5, '(continued)', align=Align.INLINE)
d.comment(0xbca6, 'Line length', align=Align.INLINE)
d.comment(0xbca8, '...', align=Align.INLINE)
d.comment(0xbcaa, 'Old top of program', align=Align.INLINE)
d.comment(0xbcac, '...', align=Align.INLINE)
d.comment(0xbcae, '...', align=Align.INLINE)
d.comment(0xbcb0, '...', align=Align.INLINE)
d.comment(0xbcb2, 'New top = old top + line length', align=Align.INLINE)
d.comment(0xbcb5, '...', align=Align.INLINE)
d.comment(0xbcb7, '...', align=Align.INLINE)
d.comment(0xbcb9, '...', align=Align.INLINE)
d.comment(0xbcbb, '...', align=Align.INLINE)
d.comment(0xbcbc, 'New top vs HIMEM', align=Align.INLINE)
d.comment(0xbcbe, '...', align=Align.INLINE)
d.comment(0xbcc0, '...', align=Align.INLINE)
d.comment(0xbcc2, '...', align=Align.INLINE)
d.comment(0xbcc4, 'fits: shift the program up', align=Align.INLINE)
d.comment(0xbcc6, 'no room: tidy up', align=Align.INLINE)
d.comment(0xbcc9, 'clear variables/heap/stack', align=Align.INLINE)
d.comment(0xbccc, 'LINE space error', align=Align.INLINE)
d.comment(0xbcd6, 'Shift a byte up', align=Align.INLINE)
d.comment(0xbcd8, '...', align=Align.INLINE)
d.comment(0xbcda, '...', align=Align.INLINE)
d.comment(0xbcdb, '...', align=Align.INLINE)
d.comment(0xbcdd, 'cross a page', align=Align.INLINE)
d.comment(0xbcdf, '...', align=Align.INLINE)
d.comment(0xbce1, 'Next byte down', align=Align.INLINE)
d.comment(0xbce2, '...', align=Align.INLINE)
d.comment(0xbce3, '...', align=Align.INLINE)
d.comment(0xbce5, '...', align=Align.INLINE)
d.comment(0xbce7, '...', align=Align.INLINE)
d.comment(0xbce9, '...', align=Align.INLINE)
d.comment(0xbcea, 'reached the insertion point?', align=Align.INLINE)
d.comment(0xbcec, '...', align=Align.INLINE)
d.comment(0xbced, '...', align=Align.INLINE)
d.comment(0xbcef, 'no: keep shifting', align=Align.INLINE)
d.comment(0xbcf1, 'Write the new line header', align=Align.INLINE)
d.comment(0xbcf2, '...', align=Align.INLINE)
d.comment(0xbcf4, 'line number high', align=Align.INLINE)
d.comment(0xbcf6, '...', align=Align.INLINE)
d.comment(0xbcf8, '...', align=Align.INLINE)
d.comment(0xbcf9, 'line number low', align=Align.INLINE)
d.comment(0xbcfb, '...', align=Align.INLINE)
d.comment(0xbcfd, '...', align=Align.INLINE)
d.comment(0xbcfe, 'line length', align=Align.INLINE)
d.comment(0xbd00, '...', align=Align.INLINE)
d.comment(0xbd02, 'Set the new top of program', align=Align.INLINE)
d.comment(0xbd05, 'Copy the line body in: offset 0', align=Align.INLINE)
d.comment(0xbd07, '...', align=Align.INLINE)
d.comment(0xbd08, 'buffer byte', align=Align.INLINE)
d.comment(0xbd0a, 'store it', align=Align.INLINE)
d.comment(0xbd0c, 'until the CR', align=Align.INLINE)
d.comment(0xbd0e, 'loop', align=Align.INLINE)

# print_token (&B50E): de-tokenise and print.
d.comment(0xb50e, 'Save the character', align=Align.INLINE)
d.comment(0xb510, 'a token?', align=Align.INLINE)
d.comment(0xb512, 'no: print it directly', align=Align.INLINE)
d.comment(0xb514, 'Point at the token table (&8071)', align=Align.INLINE)
d.comment(0xb516, '...', align=Align.INLINE)
d.comment(0xb518, '...', align=Align.INLINE)
d.comment(0xb51a, '...', align=Align.INLINE)
d.comment(0xb51c, 'save Y', align=Align.INLINE)
d.comment(0xb51e, 'Start of an entry', align=Align.INLINE)
d.comment(0xb520, 'Scan to the token byte', align=Align.INLINE)
d.comment(0xb521, '...', align=Align.INLINE)
d.comment(0xb523, '...(skip the keyword text)', align=Align.INLINE)
d.comment(0xb525, 'this token?', align=Align.INLINE)
d.comment(0xb527, 'yes: print its keyword', align=Align.INLINE)
d.comment(0xb529, 'Advance to the next entry', align=Align.INLINE)
d.comment(0xb52a, '...', align=Align.INLINE)
d.comment(0xb52b, '...', align=Align.INLINE)
d.comment(0xb52c, '...', align=Align.INLINE)
d.comment(0xb52e, '...', align=Align.INLINE)
d.comment(0xb530, '...', align=Align.INLINE)
d.comment(0xb532, '...', align=Align.INLINE)
d.comment(0xb534, 'continue', align=Align.INLINE)
d.comment(0xb536, 'Print the keyword text: from the start', align=Align.INLINE)
d.comment(0xb538, 'Next character', align=Align.INLINE)
d.comment(0xb53a, 'token byte: done', align=Align.INLINE)
d.comment(0xb53c, 'print it', align=Align.INLINE)
d.comment(0xb53f, 'next', align=Align.INLINE)
d.comment(0xb540, 'loop', align=Align.INLINE)
d.comment(0xb542, 'Restore Y', align=Align.INLINE)
d.comment(0xb544, 'Return', align=Align.INLINE)
# print_hex_byte (&B545).
d.comment(0xb545, 'Save the byte', align=Align.INLINE)
d.comment(0xb546, 'High nibble', align=Align.INLINE)
d.comment(0xb547, '...', align=Align.INLINE)
d.comment(0xb548, '...', align=Align.INLINE)
d.comment(0xb549, '...', align=Align.INLINE)
d.comment(0xb54a, 'print it', align=Align.INLINE)
d.comment(0xb54d, 'Low nibble', align=Align.INLINE)
d.comment(0xb54e, '...', align=Align.INLINE)
# print_hex_digit (&B550).
d.comment(0xb550, 'above 9?', align=Align.INLINE)
d.comment(0xb552, 'no', align=Align.INLINE)
d.comment(0xb554, "adjust for A-F", align=Align.INLINE)
d.comment(0xb556, 'to ASCII, then fall into print_char', align=Align.INLINE)
# print_char (&B558).
d.comment(0xb558, 'carriage return?', align=Align.INLINE)
d.comment(0xb55a, 'no: format and print', align=Align.INLINE)
d.comment(0xb55c, 'print the CR', align=Align.INLINE)
d.comment(0xb55f, 'reset the column', align=Align.INLINE)
d.comment(0xb562, 'Print A as hex then a space', align=Align.INLINE)
d.comment(0xb565, 'Space', align=Align.INLINE)
d.comment(0xb567, 'Save the character', align=Align.INLINE)
d.comment(0xb568, 'WIDTH limit', align=Align.INLINE)
d.comment(0xb56a, 'vs the current column', align=Align.INLINE)
d.comment(0xb56c, 'within the width', align=Align.INLINE)
d.comment(0xb56e, 'else auto-newline', align=Align.INLINE)
d.comment(0xb571, 'Recover the character', align=Align.INLINE)
d.comment(0xb572, 'Advance the column', align=Align.INLINE)
d.comment(0xb574, 'Print it via WRCHV', align=Align.INLINE)
# print_listo_indent (&B577).
d.comment(0xb577, 'LISTO bit set?', align=Align.INLINE)
d.comment(0xb579, 'no: no indent', align=Align.INLINE)
d.comment(0xb57b, 'Indent count', align=Align.INLINE)
d.comment(0xb57c, 'zero: none', align=Align.INLINE)
d.comment(0xb57e, 'single space', align=Align.INLINE)
d.comment(0xb580, 'Print a space...', align=Align.INLINE)
d.comment(0xb583, '...and a space (two per level)', align=Align.INLINE)
d.comment(0xb586, 'next level', align=Align.INLINE)
d.comment(0xb587, 'loop', align=Align.INLINE)
d.comment(0xb589, 'Return', align=Align.INLINE)
# stmt_listo (&B58A): LISTO n.
d.comment(0xb58a, 'Step past LISTO', align=Align.INLINE)
d.comment(0xb58c, 'Evaluate the option value', align=Align.INLINE)
d.comment(0xb58f, 'check the statement ends', align=Align.INLINE)
d.comment(0xb592, 'coerce to a byte', align=Align.INLINE)
d.comment(0xb595, 'Store the LISTO flag', align=Align.INLINE)
d.comment(0xb597, '...', align=Align.INLINE)
d.comment(0xb599, 'next statement', align=Align.INLINE)

# int_result_a (&AED8).
d.comment(0xaed8, 'High byte zero', align=Align.INLINE)
d.comment(0xaeda, 'return A as the integer', align=Align.INLINE)

# fn_point (&AB41): POINT(x, y) - read a pixel colour.
d.comment(0xab41, 'Evaluate x', align=Align.INLINE)
d.comment(0xab44, 'stack it', align=Align.INLINE)
d.comment(0xab47, 'Expect a comma', align=Align.INLINE)
d.comment(0xab4a, 'Evaluate y, expect )', align=Align.INLINE)
d.comment(0xab4d, 'coerce to integer', align=Align.INLINE)
d.comment(0xab50, 'Save y', align=Align.INLINE)
d.comment(0xab52, '...', align=Align.INLINE)
d.comment(0xab54, '...', align=Align.INLINE)
d.comment(0xab56, '...', align=Align.INLINE)
d.comment(0xab57, 'Recover x', align=Align.INLINE)
d.comment(0xab5a, 'into the OSWORD block', align=Align.INLINE)
d.comment(0xab5b, '...', align=Align.INLINE)
d.comment(0xab5d, '...', align=Align.INLINE)
d.comment(0xab5f, '...', align=Align.INLINE)
d.comment(0xab61, 'Read the pixel colour', align=Align.INLINE)
d.comment(0xab63, '...', align=Align.INLINE)
d.comment(0xab65, '...', align=Align.INLINE)
d.comment(0xab68, 'off-screen?', align=Align.INLINE)

# Real SGN path (&AB7F).
d.comment(0xab7f, 'Sign of the real', align=Align.INLINE)
d.comment(0xab82, 'zero: 0', align=Align.INLINE)
d.comment(0xab84, 'positive: 1', align=Align.INLINE)
d.comment(0xab86, 'negative: -1', align=Align.INLINE)
# fn_sgn (&AB88): SGN(x).
d.comment(0xab88, 'Evaluate the argument', align=Align.INLINE)
d.comment(0xab8b, 'string: error', align=Align.INLINE)
d.comment(0xab8d, 'real: use the FP sign', align=Align.INLINE)
d.comment(0xab8f, 'Integer: test for zero', align=Align.INLINE)
d.comment(0xab91, '...', align=Align.INLINE)
d.comment(0xab93, '...', align=Align.INLINE)
d.comment(0xab95, '...', align=Align.INLINE)
d.comment(0xab97, 'zero: 0', align=Align.INLINE)
d.comment(0xab99, 'Sign bit', align=Align.INLINE)
d.comment(0xab9b, 'positive: 1', align=Align.INLINE)
d.comment(0xab9d, 'negative: -1', align=Align.INLINE)
d.comment(0xaba0, 'Result = 1', align=Align.INLINE)
d.comment(0xaba2, 'return it', align=Align.INLINE)
d.comment(0xaba5, 'Result = 0 (integer)', align=Align.INLINE)
d.comment(0xaba7, 'Return', align=Align.INLINE)

# fn_int (&AC78): INT(x) - floor to integer.
d.comment(0xac78, 'Evaluate the argument', align=Align.INLINE)
d.comment(0xac7b, 'string: error', align=Align.INLINE)
d.comment(0xac7d, 'already integer: return it', align=Align.INLINE)
d.comment(0xac7f, 'Real: remember the sign', align=Align.INLINE)
d.comment(0xac81, '...', align=Align.INLINE)
d.comment(0xac82, 'Take the integer part', align=Align.INLINE)
d.comment(0xac85, 'sign', align=Align.INLINE)
d.comment(0xac86, 'positive: no adjustment', align=Align.INLINE)
d.comment(0xac88, 'Negative: any fractional bits?', align=Align.INLINE)
d.comment(0xac8a, '...', align=Align.INLINE)
d.comment(0xac8c, '...', align=Align.INLINE)
d.comment(0xac8e, '...', align=Align.INLINE)
d.comment(0xac90, 'none: exact', align=Align.INLINE)
d.comment(0xac92, 'round down (floor of a negative)', align=Align.INLINE)
d.comment(0xac95, 'Copy the integer to IWA', align=Align.INLINE)
d.comment(0xac98, 'integer result', align=Align.INLINE)
d.comment(0xac9a, 'Return', align=Align.INLINE)

# fn_asc (&AC9E): ASC(s$).
d.comment(0xac9e, 'Evaluate the string', align=Align.INLINE)
d.comment(0xaca1, 'not a string: error', align=Align.INLINE)
d.comment(0xaca3, 'String length', align=Align.INLINE)
d.comment(0xaca5, 'empty: -1', align=Align.INLINE)
d.comment(0xaca7, 'First character', align=Align.INLINE)
d.comment(0xacaa, 'return it', align=Align.INLINE)

# fn_len (&AED1): LEN(s$).
d.comment(0xaed1, 'Evaluate the string', align=Align.INLINE)
d.comment(0xaed4, 'not a string: error', align=Align.INLINE)
d.comment(0xaed6, 'Length, returned as an integer', align=Align.INLINE)

# fn_strs (&B094): STR$(x) and STR$~(x).
d.comment(0xb094, 'Next character', align=Align.INLINE)
d.comment(0xb097, 'assume hex', align=Align.INLINE)
d.comment(0xb099, "'~' hex prefix?", align=Align.INLINE)
d.comment(0xb09b, 'yes', align=Align.INLINE)
d.comment(0xb09d, 'no: decimal', align=Align.INLINE)
d.comment(0xb09f, 'back up', align=Align.INLINE)
d.comment(0xb0a1, 'Save the hex/dec flag', align=Align.INLINE)
d.comment(0xb0a2, '...', align=Align.INLINE)
d.comment(0xb0a3, 'Evaluate the number', align=Align.INLINE)
d.comment(0xb0a6, 'string: error', align=Align.INLINE)
d.comment(0xb0a7, '...', align=Align.INLINE)
d.comment(0xb0a8, 'Restore the flag', align=Align.INLINE)
d.comment(0xb0a9, '...', align=Align.INLINE)
d.comment(0xb0ab, '@% formatting set?', align=Align.INLINE)
d.comment(0xb0ae, 'yes: use it', align=Align.INLINE)
d.comment(0xb0b0, 'Default conversion', align=Align.INLINE)
d.comment(0xb0b2, '...', align=Align.INLINE)
d.comment(0xb0b5, 'string result', align=Align.INLINE)
d.comment(0xb0b7, 'Return', align=Align.INLINE)
d.comment(0xb0b9, 'Formatted conversion (@%)', align=Align.INLINE)
d.comment(0xb0bc, 'string result', align=Align.INLINE)
d.comment(0xb0be, 'Return', align=Align.INLINE)
d.comment(0xb0bf, 'Type mismatch error', align=Align.INLINE)

# stmt_gosub (&B888), stmt_return (&B8B6), stmt_goto (&B8CC), ON ERROR.
d.comment(0xb88b, 'Check the statement ends', align=Align.INLINE)
d.comment(0xb892, 'too many: error', align=Align.INLINE)
d.comment(0xb896, '...', align=Align.INLINE)
d.comment(0xb899, 'return position high byte', align=Align.INLINE)
d.comment(0xb89b, '...', align=Align.INLINE)
d.comment(0xb89e, 'one more nesting level', align=Align.INLINE)
d.comment(0xb8a0, 'jump to the line', align=Align.INLINE)
d.comment(0xb8a2, 'Too many GOSUBs error', align=Align.INLINE)
d.comment(0xb8af, 'No GOSUB error', align=Align.INLINE)
d.comment(0xb8b6, 'Check the statement ends', align=Align.INLINE)
d.comment(0xb8bb, 'nothing stacked: error', align=Align.INLINE)
d.comment(0xb8bf, 'return position low byte', align=Align.INLINE)
d.comment(0xb8c2, '...high byte', align=Align.INLINE)
d.comment(0xb8c5, 'restore the text pointer', align=Align.INLINE)
d.comment(0xb8c7, '...', align=Align.INLINE)
d.comment(0xb8cc, 'Resolve the destination line', align=Align.INLINE)
d.comment(0xb8cf, 'check the statement ends', align=Align.INLINE)
d.comment(0xb8d4, 'TRACE off?', align=Align.INLINE)
d.comment(0xb8d6, 'trace the line', align=Align.INLINE)
d.comment(0xb8d9, 'Destination line pointer', align=Align.INLINE)
d.comment(0xb8db, '...', align=Align.INLINE)
d.comment(0xb8df, '...', align=Align.INLINE)
d.comment(0xb8e1, 'execute from there', align=Align.INLINE)
d.comment(0xb8e4, 'Check the statement ends', align=Align.INLINE)
d.comment(0xb8e7, 'Restore the default error handler', align=Align.INLINE)
d.comment(0xb8e9, '...', align=Align.INLINE)
d.comment(0xb8eb, '...', align=Align.INLINE)
d.comment(0xb8ed, '...', align=Align.INLINE)
d.comment(0xb8ef, 'next statement', align=Align.INLINE)
d.comment(0xb8f2, 'Next character', align=Align.INLINE)
d.comment(0xb8f5, 'OFF token?', align=Align.INLINE)
d.comment(0xb8f7, 'yes: ON ERROR OFF', align=Align.INLINE)
d.comment(0xb8f9, 'Point at the handler statement', align=Align.INLINE)
d.comment(0xb8fb, '...', align=Align.INLINE)
d.comment(0xb8fc, '...', align=Align.INLINE)
d.comment(0xb8ff, 'Set the error handler to this line', align=Align.INLINE)
d.comment(0xb901, '...', align=Align.INLINE)
d.comment(0xb903, '...', align=Align.INLINE)
d.comment(0xb905, '...', align=Align.INLINE)
d.comment(0xb907, 'skip the rest of the line', align=Align.INLINE)
d.comment(0xb90a, 'ON syntax error', align=Align.INLINE)

# stmt_proc (&9304), stmt_local (&9323), stmt_endproc (&9356).
d.comment(0x9306, '...', align=Align.INLINE)
d.comment(0x9308, '...', align=Align.INLINE)
d.comment(0x930a, '...', align=Align.INLINE)
d.comment(0x930c, '...', align=Align.INLINE)
d.comment(0x930e, '...', align=Align.INLINE)
d.comment(0x9312, 'call it', align=Align.INLINE)
d.comment(0x9315, 'check the statement ends', align=Align.INLINE)
d.comment(0x9318, 'next statement', align=Align.INLINE)
d.comment(0x931b, 'Clear the local string length', align=Align.INLINE)
d.comment(0x931d, '...', align=Align.INLINE)
d.comment(0x931f, '...', align=Align.INLINE)
d.comment(0x9321, 'always', align=Align.INLINE)
d.comment(0x9324, 'inside a PROC/FN?', align=Align.INLINE)
d.comment(0x9326, 'no: Not LOCAL error', align=Align.INLINE)
d.comment(0x9328, 'Parse the local variable', align=Align.INLINE)
d.comment(0x932b, 'not a variable: error', align=Align.INLINE)
d.comment(0x9330, 'string variable?', align=Align.INLINE)
d.comment(0x9332, 'yes: leave it cleared', align=Align.INLINE)
d.comment(0x9334, 'stack the variable address', align=Align.INLINE)
d.comment(0x9339, 'value zero', align=Align.INLINE)
d.comment(0x933c, 'integer type', align=Align.INLINE)
d.comment(0x933e, 'assign it', align=Align.INLINE)
d.comment(0x9341, 'Bump the local count in the frame', align=Align.INLINE)
d.comment(0x9342, '...', align=Align.INLINE)
d.comment(0x9345, 'Sync the program pointer', align=Align.INLINE)
d.comment(0x9347, '...', align=Align.INLINE)
d.comment(0x9349, 'Skip spaces', align=Align.INLINE)
d.comment(0x934e, 'yes', align=Align.INLINE)
d.comment(0x9350, 'next statement', align=Align.INLINE)
d.comment(0x9353, 'not a variable: error', align=Align.INLINE)
d.comment(0x9357, '...', align=Align.INLINE)
d.comment(0x9359, 'no frame: Not PROC error', align=Align.INLINE)
d.comment(0x935b, 'Framed call token', align=Align.INLINE)
d.comment(0x9360, 'not PROC: error', align=Align.INLINE)
d.comment(0x9365, 'No PROC error', align=Align.INLINE)
d.comment(0x936b, 'Not LOCAL error', align=Align.INLINE)
d.comment(0x9372, 'Bad statement error', align=Align.INLINE)

# stmt_gcol (&937A): GCOL mode, colour -> VDU 18.
d.comment(0x937a, 'Evaluate the GCOL mode', align=Align.INLINE)
d.comment(0x937d, 'save it', align=Align.INLINE)
d.comment(0x937f, '...', align=Align.INLINE)
d.comment(0x9380, 'Step past the comma, evaluate the colour',
          align=Align.INLINE)
d.comment(0x9383, 'check the statement ends', align=Align.INLINE)
d.comment(0x9386, 'VDU 18 (GCOL)', align=Align.INLINE)
d.comment(0x9388, '...', align=Align.INLINE)
d.comment(0x938b, 'send the mode and colour', align=Align.INLINE)
# stmt_colour (&938E): COLOUR n -> VDU 17.
d.comment(0x938e, 'VDU 17 (COLOUR)', align=Align.INLINE)
d.comment(0x9390, '...', align=Align.INLINE)
d.comment(0x9391, 'Evaluate the colour', align=Align.INLINE)
d.comment(0x9394, 'check the statement ends', align=Align.INLINE)
d.comment(0x9397, 'send VDU 17 and the colour', align=Align.INLINE)
# stmt_mode (&939A): MODE n -> VDU 22, with memory checks.
d.comment(0x939a, 'VDU 22 (MODE)', align=Align.INLINE)
d.comment(0x939c, '...', align=Align.INLINE)
d.comment(0x939d, 'Evaluate the mode number', align=Align.INLINE)
d.comment(0x93a0, 'check the statement ends', align=Align.INLINE)
d.comment(0x93a3, 'Read the high word of the machine address', align=Align.INLINE)
d.comment(0x93a6, 'not &xxFF: skip the memory test', align=Align.INLINE)
d.comment(0x93a8, '...', align=Align.INLINE)
d.comment(0x93aa, 'not all ones: skip the memory test', align=Align.INLINE)
d.comment(0x93ac, '...', align=Align.INLINE)
d.comment(0x93ae, 'Stack not empty (STACK != HIMEM)?', align=Align.INLINE)
d.comment(0x93b0, '...', align=Align.INLINE)
d.comment(0x93b2, 'yes: Bad MODE', align=Align.INLINE)
d.comment(0x93b4, '...', align=Align.INLINE)
d.comment(0x93b6, '...', align=Align.INLINE)
d.comment(0x93b8, 'Bad MODE', align=Align.INLINE)
d.comment(0x93ba, 'Top of RAM for this mode', align=Align.INLINE)
d.comment(0x93bc, '...', align=Align.INLINE)
d.comment(0x93c1, 'below the variables?', align=Align.INLINE)
d.comment(0x93c3, '...', align=Align.INLINE)
d.comment(0x93c4, '...', align=Align.INLINE)
d.comment(0x93c6, 'yes: Bad MODE', align=Align.INLINE)
d.comment(0x93c8, 'below the program top?', align=Align.INLINE)
d.comment(0x93ca, '...', align=Align.INLINE)
d.comment(0x93cb, '...', align=Align.INLINE)
d.comment(0x93cd, 'yes: Bad MODE', align=Align.INLINE)
d.comment(0x93cf, 'Set HIMEM and STACK to the new top', align=Align.INLINE)
d.comment(0x93d1, '...', align=Align.INLINE)
d.comment(0x93d3, '...', align=Align.INLINE)
d.comment(0x93d5, '...', align=Align.INLINE)
d.comment(0x93d7, 'Reset the print column', align=Align.INLINE)
d.comment(0x93da, 'Send the stacked VDU byte', align=Align.INLINE)
d.comment(0x93db, '...', align=Align.INLINE)
d.comment(0x93de, 'Send the parameter', align=Align.INLINE)
d.comment(0x93e1, 'next statement', align=Align.INLINE)

# stmt_plot (&93F1): PLOT mode, x, y -> VDU 25.
d.comment(0x93f1, 'Evaluate the plot mode', align=Align.INLINE)
d.comment(0x93f4, 'save it', align=Align.INLINE)
d.comment(0x93f6, '...', align=Align.INLINE)
d.comment(0x93f7, 'Step past the comma', align=Align.INLINE)
d.comment(0x93fa, 'Evaluate the X coordinate', align=Align.INLINE)
d.comment(0x93fd, 'ensure integer', align=Align.INLINE)
d.comment(0x9400, 'stack X', align=Align.INLINE)
d.comment(0x9403, 'Step past the comma, evaluate Y', align=Align.INLINE)
d.comment(0x9406, 'check the statement ends', align=Align.INLINE)
d.comment(0x9409, 'VDU 25 (PLOT)', align=Align.INLINE)
d.comment(0x940b, '...', align=Align.INLINE)
d.comment(0x940e, 'Send the plot action', align=Align.INLINE)
d.comment(0x940f, '...', align=Align.INLINE)
d.comment(0x9412, 'Pop X', align=Align.INLINE)
d.comment(0x9415, 'Send X low', align=Align.INLINE)
d.comment(0x9417, '...', align=Align.INLINE)
d.comment(0x941a, 'Send X high', align=Align.INLINE)
d.comment(0x941c, '...', align=Align.INLINE)
d.comment(0x941f, 'Send Y low', align=Align.INLINE)
d.comment(0x9422, 'Send Y high', align=Align.INLINE)
d.comment(0x9424, '...', align=Align.INLINE)
d.comment(0x9427, 'next statement', align=Align.INLINE)
d.comment(0x942a, 'Send the high byte', align=Align.INLINE)
d.comment(0x942c, '...', align=Align.INLINE)

# stmt_cls (&8EC4): CLS -> VDU 12.
d.comment(0x8ec4, 'Check the statement ends', align=Align.INLINE)
d.comment(0x8ec7, 'Reset the print column', align=Align.INLINE)
d.comment(0x8eca, 'VDU 12 (clear screen)', align=Align.INLINE)
d.comment(0x8ecc, 'send it', align=Align.INLINE)
d.comment(0x8ecf, 'next statement', align=Align.INLINE)

# stmt_trace (&9295): TRACE line / TRACE ON / TRACE OFF.
d.comment(0x9295, 'Line number following?', align=Align.INLINE)
d.comment(0x9298, 'yes: TRACE to that line', align=Align.INLINE)
d.comment(0x929a, 'ON token?', align=Align.INLINE)
d.comment(0x929c, 'yes', align=Align.INLINE)
d.comment(0x929e, 'OFF token?', align=Align.INLINE)
d.comment(0x92a0, 'yes', align=Align.INLINE)
d.comment(0x92a2, 'Evaluate the trace ceiling', align=Align.INLINE)
d.comment(0x92a5, 'check the statement ends', align=Align.INLINE)
d.comment(0x92a8, 'Set the trace ceiling', align=Align.INLINE)
d.comment(0x92aa, '...', align=Align.INLINE)
d.comment(0x92ac, '...', align=Align.INLINE)
d.comment(0x92ae, '...', align=Align.INLINE)
d.comment(0x92b0, 'TRACE on', align=Align.INLINE)
d.comment(0x92b2, 'Set the TRACE flag', align=Align.INLINE)
d.comment(0x92b4, 'next statement', align=Align.INLINE)
d.comment(0x92b7, 'TRACE ON: step past', align=Align.INLINE)
d.comment(0x92b9, 'check the statement ends', align=Align.INLINE)
d.comment(0x92bc, 'ceiling = max', align=Align.INLINE)
d.comment(0x92be, 'set it on', align=Align.INLINE)
d.comment(0x92c0, 'TRACE OFF: step past', align=Align.INLINE)
d.comment(0x92c2, 'check the statement ends', align=Align.INLINE)
d.comment(0x92c5, 'flag = 0', align=Align.INLINE)
d.comment(0x92c7, 'set it off', align=Align.INLINE)

# stmt_time (&92C9): TIME = n -> OSWORD 2.
d.comment(0x92c9, 'Step past "=", evaluate the value', align=Align.INLINE)
d.comment(0x92cc, 'Point at IWA', align=Align.INLINE)
d.comment(0x92ce, '...', align=Align.INLINE)
d.comment(0x92d0, 'clear the 5th byte', align=Align.INLINE)
d.comment(0x92d2, 'OSWORD 2 (write clock)', align=Align.INLINE)
d.comment(0x92d7, 'next statement', align=Align.INLINE)
d.comment(0x92da, 'Step past the comma', align=Align.INLINE)
d.comment(0x92dd, 'Evaluate the expression', align=Align.INLINE)
d.comment(0x92e0, '...and coerce to integer', align=Align.INLINE)

# stmt_old (&8AB6): OLD - recover a NEWed program.
d.comment(0x8ab6, 'Check the statement ends', align=Align.INLINE)
d.comment(0x8ab9, 'Point at PAGE', align=Align.INLINE)
d.comment(0x8abb, '...', align=Align.INLINE)
d.comment(0x8abd, '...', align=Align.INLINE)
d.comment(0x8abf, '...', align=Align.INLINE)
d.comment(0x8ac1, 'Remove the end marker', align=Align.INLINE)
d.comment(0x8ac3, 'Re-check the program and set TOP', align=Align.INLINE)
d.comment(0x8ac6, 'clear heap and return to immediate mode', align=Align.INLINE)
# stmt_end (&8AC8) and stmt_stop (&8AD0).
d.comment(0x8ac8, 'Check the statement ends', align=Align.INLINE)
d.comment(0x8acb, 'Check the program', align=Align.INLINE)
d.comment(0x8ace, 'return to immediate mode (keep variables)',
          align=Align.INLINE)
d.comment(0x8ad0, 'Check the statement ends', align=Align.INLINE)
d.comment(0x8ad3, 'STOP error', align=Align.INLINE)

# stmt_let (&8BE4) remaining gaps.
d.comment(0x8be7, 'end of statement: error', align=Align.INLINE)
d.comment(0x8be9, 'numeric target?', align=Align.INLINE)
d.comment(0x8bf1, 'value type', align=Align.INLINE)
d.comment(0x8bf8, 'next statement', align=Align.INLINE)
d.comment(0x8bfb, 'Stack the destination address', align=Align.INLINE)
d.comment(0x8bfe, 'Expect "=" and evaluate', align=Align.INLINE)
d.comment(0x8c01, 'value type', align=Align.INLINE)
d.comment(0x8c08, 'next statement', align=Align.INLINE)
d.comment(0x8c0b, 'Mistake (syntax) error', align=Align.INLINE)

# stmt_delete (&8F31): DELETE start, end.
d.comment(0x8f31, 'Read the start line number', align=Align.INLINE)
d.comment(0x8f34, 'none: Syntax error', align=Align.INLINE)
d.comment(0x8f36, 'stack it', align=Align.INLINE)
d.comment(0x8f39, 'Skip spaces', align=Align.INLINE)
d.comment(0x8f3c, "','?", align=Align.INLINE)
d.comment(0x8f3e, 'no: error', align=Align.INLINE)
d.comment(0x8f40, 'Read the end line number', align=Align.INLINE)
d.comment(0x8f43, 'none: error', align=Align.INLINE)
d.comment(0x8f45, 'check the statement ends', align=Align.INLINE)
d.comment(0x8f48, 'Save the end line', align=Align.INLINE)
d.comment(0x8f4a, '...', align=Align.INLINE)
d.comment(0x8f4c, '...', align=Align.INLINE)
d.comment(0x8f4e, '...', align=Align.INLINE)
d.comment(0x8f50, 'Recover the start line', align=Align.INLINE)
d.comment(0x8f53, 'Delete the line', align=Align.INLINE)
d.comment(0x8f56, 'Find the next line number', align=Align.INLINE)
d.comment(0x8f59, 'Advance the line counter', align=Align.INLINE)
d.comment(0x8f5c, 'past the end line?', align=Align.INLINE)
d.comment(0x8f5e, '...', align=Align.INLINE)
d.comment(0x8f60, '...', align=Align.INLINE)
d.comment(0x8f62, '...', align=Align.INLINE)
d.comment(0x8f64, 'no: delete the next', align=Align.INLINE)
d.comment(0x8f66, 'done: immediate mode', align=Align.INLINE)

# sub_c8f69 (&8F69): parse a line-number range/increment (default 10).
d.comment(0x8f69, 'Default start = 10', align=Align.INLINE)
d.comment(0x8f6b, '...', align=Align.INLINE)
d.comment(0x8f6e, 'Read the start line if given', align=Align.INLINE)
d.comment(0x8f71, 'stack it', align=Align.INLINE)
d.comment(0x8f74, 'Default increment = 10', align=Align.INLINE)
d.comment(0x8f76, '...', align=Align.INLINE)
d.comment(0x8f79, 'Skip spaces', align=Align.INLINE)
d.comment(0x8f7c, "','  increment given?", align=Align.INLINE)
d.comment(0x8f7e, 'no: use the default', align=Align.INLINE)
d.comment(0x8f80, 'Read the increment', align=Align.INLINE)
d.comment(0x8f83, 'zero?', align=Align.INLINE)
d.comment(0x8f85, 'no', align=Align.INLINE)
d.comment(0x8f87, '...', align=Align.INLINE)
d.comment(0x8f89, 'zero increment: error', align=Align.INLINE)
d.comment(0x8f8b, 'step past', align=Align.INLINE)
d.comment(0x8f8d, 'back up', align=Align.INLINE)
d.comment(0x8f8f, 'check the statement ends', align=Align.INLINE)

# stmt_auto (&90AC): AUTO start, increment.
d.comment(0x90ac, 'Parse the start and increment', align=Align.INLINE)
d.comment(0x90af, 'Save the increment', align=Align.INLINE)
d.comment(0x90b1, '...', align=Align.INLINE)
d.comment(0x90b2, 'Recover the start line', align=Align.INLINE)
d.comment(0x90b5, 'Stack the line number', align=Align.INLINE)
d.comment(0x90b8, 'Print it', align=Align.INLINE)
d.comment(0x90bb, 'Print a space and read a line', align=Align.INLINE)
d.comment(0x90bd, '...', align=Align.INLINE)
d.comment(0x90c0, 'Pop the line number', align=Align.INLINE)
d.comment(0x90c3, 'Tokenise the line', align=Align.INLINE)
d.comment(0x90c6, 'Insert it into the program', align=Align.INLINE)
d.comment(0x90c9, 'Clear variables and heap', align=Align.INLINE)
d.comment(0x90cc, 'Increment', align=Align.INLINE)
d.comment(0x90cd, '...', align=Align.INLINE)
d.comment(0x90ce, 'Next line number = line + increment', align=Align.INLINE)
d.comment(0x90cf, '...', align=Align.INLINE)
d.comment(0x90d1, '...', align=Align.INLINE)
d.comment(0x90d3, '...', align=Align.INLINE)
d.comment(0x90d5, '...', align=Align.INLINE)
d.comment(0x90d7, 'still in range: loop', align=Align.INLINE)
d.comment(0x90d9, 'overflow: stop', align=Align.INLINE)

# stmt_width (&B4A0): WIDTH n.
d.comment(0xb4a0, 'Evaluate the width', align=Align.INLINE)
d.comment(0xb4a3, 'check the statement ends', align=Align.INLINE)
d.comment(0xb4a6, 'Auto-newline column = width - 1', align=Align.INLINE)
d.comment(0xb4a8, '...', align=Align.INLINE)
d.comment(0xb4a9, 'store it', align=Align.INLINE)
d.comment(0xb4ab, 'next statement', align=Align.INLINE)

# stmt_run (&BD11): RUN.
d.comment(0xbd11, 'Check the statement ends', align=Align.INLINE)
d.comment(0xbd14, 'Clear variables, heap and stack', align=Align.INLINE)
d.comment(0xbd17, 'Point PtrA at PAGE', align=Align.INLINE)
d.comment(0xbd19, '...', align=Align.INLINE)
d.comment(0xbd1b, '...', align=Align.INLINE)
d.comment(0xbd1d, 'execute from the start', align=Align.INLINE)

# stmt_restore (&BAE6): RESTORE [line].
d.comment(0xbae6, 'DATA pointer = PAGE', align=Align.INLINE)
d.comment(0xbae8, '...', align=Align.INLINE)
d.comment(0xbaea, '...', align=Align.INLINE)
d.comment(0xbaec, '...', align=Align.INLINE)
d.comment(0xbaee, 'Skip spaces', align=Align.INLINE)
d.comment(0xbaf1, 'back up', align=Align.INLINE)
d.comment(0xbaf3, "':' end?", align=Align.INLINE)
d.comment(0xbaf5, 'yes: restore to PAGE', align=Align.INLINE)
d.comment(0xbaf7, 'end of line?', align=Align.INLINE)
d.comment(0xbaf9, 'yes', align=Align.INLINE)
d.comment(0xbafb, 'ELSE?', align=Align.INLINE)
d.comment(0xbafd, 'yes', align=Align.INLINE)
d.comment(0xbaff, 'Find the given line', align=Align.INLINE)
d.comment(0xbb02, 'point at it', align=Align.INLINE)
d.comment(0xbb04, '...', align=Align.INLINE)
d.comment(0xbb07, 'Check the statement ends', align=Align.INLINE)
d.comment(0xbb0a, 'Set the DATA pointer', align=Align.INLINE)
d.comment(0xbb0c, '...', align=Align.INLINE)
d.comment(0xbb0e, '...', align=Align.INLINE)
d.comment(0xbb10, '...', align=Align.INLINE)
d.comment(0xbb12, 'next statement', align=Align.INLINE)
d.comment(0xbb15, 'Skip spaces', align=Align.INLINE)
d.comment(0xbb18, "','?", align=Align.INLINE)
d.comment(0xbb1a, 'yes: READ', align=Align.INLINE)
d.comment(0xbb1c, 'next statement', align=Align.INLINE)

# stmt_save (&BEF3): SAVE - build an OSFILE block and save the program.
d.comment(0xbef3, 'Check the program, set TOP', align=Align.INLINE)
d.comment(0xbef6, 'End address = TOP', align=Align.INLINE)
d.comment(0xbef8, '...', align=Align.INLINE)
d.comment(0xbefa, '...', align=Align.INLINE)
d.comment(0xbefc, '...', align=Align.INLINE)
d.comment(0xbefe, 'Exec address = language startup', align=Align.INLINE)
d.comment(0xbf00, '...', align=Align.INLINE)
d.comment(0xbf02, '...', align=Align.INLINE)
d.comment(0xbf04, '...', align=Align.INLINE)
d.comment(0xbf06, 'Start address = PAGE', align=Align.INLINE)
d.comment(0xbf08, '...', align=Align.INLINE)
d.comment(0xbf0a, 'Read the machine high address words', align=Align.INLINE)
d.comment(0xbf0d, 'Fill the address high words', align=Align.INLINE)
d.comment(0xbf0f, '...', align=Align.INLINE)
d.comment(0xbf11, '...', align=Align.INLINE)
d.comment(0xbf13, '...', align=Align.INLINE)
d.comment(0xbf15, '...', align=Align.INLINE)
d.comment(0xbf17, '...', align=Align.INLINE)
d.comment(0xbf19, 'Load address low = PAGE', align=Align.INLINE)
d.comment(0xbf1b, '...', align=Align.INLINE)
d.comment(0xbf1c, 'Point at the OSFILE block (&37)', align=Align.INLINE)
d.comment(0xbf1e, 'Save the file', align=Align.INLINE)
d.comment(0xbf21, 'next statement', align=Align.INLINE)

# parse_decimal_u16 (&8897): accumulate value*10 + digit.
d.comment(0x8897, 'First digit', align=Align.INLINE)
d.comment(0x8899, 'Value low = digit', align=Align.INLINE)
d.comment(0x889b, 'Value high = 0', align=Align.INLINE)
d.comment(0x889d, 'Next character', align=Align.INLINE)
d.comment(0x889e, 'read it', align=Align.INLINE)
d.comment(0x88a0, 'above 9?', align=Align.INLINE)
d.comment(0x88a2, 'not a digit: done', align=Align.INLINE)
d.comment(0x88a4, 'below 0?', align=Align.INLINE)
d.comment(0x88a6, 'not a digit: done', align=Align.INLINE)
d.comment(0x88a8, 'Digit value', align=Align.INLINE)
d.comment(0x88aa, 'save it', align=Align.INLINE)
d.comment(0x88ab, 'value high', align=Align.INLINE)
d.comment(0x88ad, 'value low', align=Align.INLINE)
d.comment(0x88af, 'value * 2', align=Align.INLINE)
d.comment(0x88b0, 'into the high byte', align=Align.INLINE)
d.comment(0x88b2, 'overflow', align=Align.INLINE)
d.comment(0x88b4, 'value * 4', align=Align.INLINE)
d.comment(0x88b5, 'into the high byte', align=Align.INLINE)
d.comment(0x88b7, 'overflow', align=Align.INLINE)
d.comment(0x88b9, '+ value = value * 5', align=Align.INLINE)
d.comment(0x88bb, 'store the low byte', align=Align.INLINE)
d.comment(0x88bd, 'now the high byte:', align=Align.INLINE)
d.comment(0x88be, '+ the x4 high byte (= x5)', align=Align.INLINE)
d.comment(0x88c0, '* 2 = value * 10', align=Align.INLINE)
d.comment(0x88c2, 'into the high byte', align=Align.INLINE)
d.comment(0x88c3, 'overflow', align=Align.INLINE)
d.comment(0x88c5, 'overflow', align=Align.INLINE)
d.comment(0x88c7, 'store the high byte', align=Align.INLINE)
d.comment(0x88c9, 'Add the digit', align=Align.INLINE)
d.comment(0x88ca, 'add the digit to the low byte,', align=Align.INLINE)
d.comment(0x88cc, 'store it', align=Align.INLINE)
d.comment(0x88ce, 'next digit', align=Align.INLINE)
d.comment(0x88d0, 'carry into the high byte', align=Align.INLINE)
d.comment(0x88d2, 'next digit', align=Align.INLINE)
d.comment(0x88d4, 'overflow marker', align=Align.INLINE)
d.comment(0x88d5, 'Discard the saved digit', align=Align.INLINE)
d.comment(0x88d6, 'Offset 0', align=Align.INLINE)
d.comment(0x88d8, 'flag a value was read', align=Align.INLINE)
d.comment(0x88d9, 'Return', align=Align.INLINE)

# Hex conversion (&9E90): IWA/FWA -> hex string (PRINT~ / STR$~).
d.comment(0x9e90, 'Real?', align=Align.INLINE)
d.comment(0x9e91, 'no', align=Align.INLINE)
d.comment(0x9e93, 'convert to integer', align=Align.INLINE)
d.comment(0x9e96, 'Expand 4 bytes into 8 nibbles', align=Align.INLINE)
d.comment(0x9e98, '...', align=Align.INLINE)
d.comment(0x9e9a, 'Byte', align=Align.INLINE)
d.comment(0x9e9d, 'save it', align=Align.INLINE)
d.comment(0x9e9e, 'low nibble', align=Align.INLINE)
d.comment(0x9ea0, '...', align=Align.INLINE)
d.comment(0x9ea2, 'high nibble', align=Align.INLINE)
d.comment(0x9ea3, '...', align=Align.INLINE)
d.comment(0x9ea4, '...', align=Align.INLINE)
d.comment(0x9ea5, '...', align=Align.INLINE)
d.comment(0x9ea6, '...', align=Align.INLINE)
d.comment(0x9ea7, '...', align=Align.INLINE)
d.comment(0x9ea8, '...', align=Align.INLINE)
d.comment(0x9eaa, '...', align=Align.INLINE)
d.comment(0x9eab, '...', align=Align.INLINE)
d.comment(0x9eac, 'all four bytes?', align=Align.INLINE)
d.comment(0x9eae, 'no: continue', align=Align.INLINE)
d.comment(0x9eb0, 'Skip leading zero nibbles', align=Align.INLINE)
d.comment(0x9eb1, 'all zero: output one zero', align=Align.INLINE)
d.comment(0x9eb3, '...', align=Align.INLINE)
d.comment(0x9eb5, '...', align=Align.INLINE)
d.comment(0x9eb7, 'Next nibble', align=Align.INLINE)
d.comment(0x9eb9, 'above 9?', align=Align.INLINE)
d.comment(0x9ebb, 'no', align=Align.INLINE)
d.comment(0x9ebd, 'adjust for A-F', align=Align.INLINE)
d.comment(0x9ebf, 'to ASCII', align=Align.INLINE)
d.comment(0x9ec1, 'output the digit', align=Align.INLINE)
d.comment(0x9ec4, 'next', align=Align.INLINE)
d.comment(0x9ec5, 'loop', align=Align.INLINE)
d.comment(0x9ec7, 'Return', align=Align.INLINE)

# fp_compare (&9A39 setup / &9A5F): FWA vs operand.
d.comment(0x9a39, 'Int vs real: save the operator', align=Align.INLINE)
d.comment(0x9a3b, 'unstack the integer', align=Align.INLINE)
d.comment(0x9a3e, 'stack the real', align=Align.INLINE)
d.comment(0x9a41, 'convert the integer to FWA', align=Align.INLINE)
d.comment(0x9a44, 'FWB = it', align=Align.INLINE)
d.comment(0x9a47, 'unstack the real operand', align=Align.INLINE)
d.comment(0x9a4a, 'into FWA', align=Align.INLINE)
d.comment(0x9a4d, 'compare', align=Align.INLINE)
d.comment(0x9a50, 'Real vs real: stack the left', align=Align.INLINE)
d.comment(0x9a53, 'evaluate the right operand', align=Align.INLINE)
d.comment(0x9a56, 'save the operator', align=Align.INLINE)
d.comment(0x9a58, 'type', align=Align.INLINE)
d.comment(0x9a59, 'ensure real', align=Align.INLINE)
d.comment(0x9a5c, 'unstack the left operand', align=Align.INLINE)
d.comment(0x9a5f, 'Unpack the operand into FWB', align=Align.INLINE)
d.comment(0x9a62, 'Restore the operator', align=Align.INLINE)
d.comment(0x9a64, 'assume equal', align=Align.INLINE)
d.comment(0x9a66, 'FWB sign', align=Align.INLINE)
d.comment(0x9a68, '...', align=Align.INLINE)
d.comment(0x9a6a, '...', align=Align.INLINE)
d.comment(0x9a6c, 'FWA sign', align=Align.INLINE)
d.comment(0x9a6e, '...', align=Align.INLINE)
d.comment(0x9a70, 'signs differ?', align=Align.INLINE)
d.comment(0x9a72, 'yes: unequal', align=Align.INLINE)
d.comment(0x9a74, 'Compare exponents', align=Align.INLINE)
d.comment(0x9a76, '...', align=Align.INLINE)
d.comment(0x9a78, 'differ', align=Align.INLINE)
d.comment(0x9a7a, 'Compare mantissa byte 1', align=Align.INLINE)
d.comment(0x9a7c, '...', align=Align.INLINE)
d.comment(0x9a7e, 'differ', align=Align.INLINE)
d.comment(0x9a80, 'byte 2', align=Align.INLINE)
d.comment(0x9a82, '...', align=Align.INLINE)
d.comment(0x9a84, 'differ', align=Align.INLINE)
d.comment(0x9a86, 'byte 3', align=Align.INLINE)
d.comment(0x9a88, '...', align=Align.INLINE)
d.comment(0x9a8a, 'differ', align=Align.INLINE)
d.comment(0x9a8c, 'byte 4', align=Align.INLINE)
d.comment(0x9a8e, '...', align=Align.INLINE)
d.comment(0x9a90, 'differ', align=Align.INLINE)

# ----------------------------------------------------------------------
# Inline assembler driver (&84FD): the [ ... ] block.
# Assembles each instruction, and when OPT bit 1 is set prints the
# listing line (P% in hex, the assembled bytes, the source text).
# ----------------------------------------------------------------------
d.comment(0x84fd, 'Leaving the assembler: OPT = BASIC mode', align=Align.INLINE)
d.comment(0x84ff, '...', align=Align.INLINE)
d.comment(0x8501, 'resume execution', align=Align.INLINE)
d.comment(0x8504, 'Entering: default OPT 3', align=Align.INLINE)
d.comment(0x8506, '...', align=Align.INLINE)
d.comment(0x8508, 'Skip spaces', align=Align.INLINE)
d.comment(0x850b, "']' end of assembler?", align=Align.INLINE)
d.comment(0x850d, 'yes: exit', align=Align.INLINE)
d.comment(0x850f, 'Skip to the statement', align=Align.INLINE)
d.comment(0x8512, 'back up', align=Align.INLINE)
d.comment(0x8514, 'Assemble one instruction', align=Align.INLINE)
d.comment(0x8517, 'back up', align=Align.INLINE)
d.comment(0x8519, 'OPT listing bit set?', align=Align.INLINE)
d.comment(0x851b, '...', align=Align.INLINE)
d.comment(0x851c, 'no: skip the listing', align=Align.INLINE)
d.comment(0x851e, 'Column for the source text', align=Align.INLINE)
d.comment(0x8520, '...', align=Align.INLINE)
d.comment(0x8522, '...', align=Align.INLINE)
d.comment(0x8524, 'Print P% high', align=Align.INLINE)
d.comment(0x8526, '...', align=Align.INLINE)
d.comment(0x8529, 'Print P% low', align=Align.INLINE)
d.comment(0x852b, '...', align=Align.INLINE)
d.comment(0x852e, 'Byte count', align=Align.INLINE)
d.comment(0x8530, 'String (EQUS) length?', align=Align.INLINE)
d.comment(0x8532, '...', align=Align.INLINE)
d.comment(0x8534, '...', align=Align.INLINE)
d.comment(0x8536, 'Bytes to list', align=Align.INLINE)
d.comment(0x8538, 'none', align=Align.INLINE)
d.comment(0x853a, 'From byte 0', align=Align.INLINE)
d.comment(0x853c, 'Count printed on this line', align=Align.INLINE)
d.comment(0x853d, 'still on the line', align=Align.INLINE)
d.comment(0x853f, 'Newline and indent for a continuation', align=Align.INLINE)
d.comment(0x8542, '...', align=Align.INLINE)
d.comment(0x8544, 'Print a space', align=Align.INLINE)
d.comment(0x8547, '...', align=Align.INLINE)
d.comment(0x8548, 'loop', align=Align.INLINE)
d.comment(0x854a, 'reset the per-line count', align=Align.INLINE)
d.comment(0x854c, 'Assembled byte', align=Align.INLINE)
d.comment(0x854e, 'print it as hex', align=Align.INLINE)
d.comment(0x8551, 'next', align=Align.INLINE)
d.comment(0x8552, 'all bytes?', align=Align.INLINE)
d.comment(0x8554, 'no: continue', align=Align.INLINE)
d.comment(0x8556, 'Pad to the source column', align=Align.INLINE)
d.comment(0x8557, 'done', align=Align.INLINE)
d.comment(0x8559, 'print a space', align=Align.INLINE)
d.comment(0x855c, '...', align=Align.INLINE)
d.comment(0x855f, '...', align=Align.INLINE)
d.comment(0x8562, 'loop', align=Align.INLINE)
d.comment(0x8565, 'Print the source: from offset 0', align=Align.INLINE)
d.comment(0x8567, 'Next character', align=Align.INLINE)
d.comment(0x8569, "':' end of statement?", align=Align.INLINE)
d.comment(0x856b, 'yes', align=Align.INLINE)
d.comment(0x856d, 'end of line?', align=Align.INLINE)
d.comment(0x856f, 'yes', align=Align.INLINE)
d.comment(0x8571, 'de-tokenise and print', align=Align.INLINE)
d.comment(0x8574, 'next', align=Align.INLINE)
d.comment(0x8575, 'loop', align=Align.INLINE)
d.comment(0x8577, 'reached the statement end?', align=Align.INLINE)
d.comment(0x8579, 'no: continue', align=Align.INLINE)
d.comment(0x857b, 'Newline', align=Align.INLINE)
d.comment(0x857e, 'Advance to the next statement', align=Align.INLINE)
d.comment(0x8580, '...', align=Align.INLINE)
d.comment(0x8581, 'scan for the end', align=Align.INLINE)
d.comment(0x8582, '...', align=Align.INLINE)
d.comment(0x8584, "':'?", align=Align.INLINE)
d.comment(0x8586, 'yes', align=Align.INLINE)
d.comment(0x8588, 'end of line?', align=Align.INLINE)
d.comment(0x858a, 'no: continue', align=Align.INLINE)
d.comment(0x858c, 'Check Escape and advance', align=Align.INLINE)
d.comment(0x858f, 'Re-read the terminator', align=Align.INLINE)
d.comment(0x8590, '...', align=Align.INLINE)
d.comment(0x8592, "':'?", align=Align.INLINE)
d.comment(0x8594, 'yes: same line', align=Align.INLINE)
d.comment(0x8596, 'at end of program memory?', align=Align.INLINE)
d.comment(0x8598, '...', align=Align.INLINE)
d.comment(0x859a, 'no: next line', align=Align.INLINE)
d.comment(0x859c, 'yes: immediate mode', align=Align.INLINE)
d.comment(0x859f, 'Move to the next line', align=Align.INLINE)
d.comment(0x85a2, 'continue assembling', align=Align.INLINE)
d.comment(0x85a5, 'Label: parse the variable', align=Align.INLINE)
d.comment(0x85a8, 'end: error', align=Align.INLINE)
d.comment(0x85aa, 'indirection: error', align=Align.INLINE)
d.comment(0x85ac, 'stack the address', align=Align.INLINE)
d.comment(0x85af, 'value = P%', align=Align.INLINE)
d.comment(0x85b2, 'integer type', align=Align.INLINE)
d.comment(0x85b4, 'assign P% to the label', align=Align.INLINE)
d.comment(0x85b7, 'sync the pointer', align=Align.INLINE)

# asm_parse_mnemonic (&85BA): compact three letters into &3D/&3E.
d.comment(0x85ba, 'Three characters', align=Align.INLINE)
d.comment(0x85bc, 'Skip spaces', align=Align.INLINE)
d.comment(0x85bf, 'Clear the compacted value', align=Align.INLINE)
d.comment(0x85c1, '...', align=Align.INLINE)
d.comment(0x85c3, "':' end of statement?", align=Align.INLINE)
d.comment(0x85c5, 'yes: no instruction', align=Align.INLINE)
d.comment(0x85c7, 'end of line?', align=Align.INLINE)
d.comment(0x85c9, 'yes', align=Align.INLINE)
d.comment(0x85cb, 'comment?', align=Align.INLINE)
d.comment(0x85cd, 'yes', align=Align.INLINE)
d.comment(0x85cf, "'.' label?", align=Align.INLINE)
d.comment(0x85d1, 'yes: define it', align=Align.INLINE)
d.comment(0x85d3, 'back up', align=Align.INLINE)
d.comment(0x85d5, 'Next character', align=Align.INLINE)
d.comment(0x85d7, '...', align=Align.INLINE)
d.comment(0x85d9, '...', align=Align.INLINE)
d.comment(0x85db, 'token: tokenised AND/EOR/OR', align=Align.INLINE)
d.comment(0x85dd, 'space?', align=Align.INLINE)
d.comment(0x85df, 'skip it', align=Align.INLINE)
d.comment(0x85e1, 'Compact the character (5 bits)', align=Align.INLINE)
d.comment(0x85e3, '...', align=Align.INLINE)
d.comment(0x85e4, '...', align=Align.INLINE)
d.comment(0x85e5, '...', align=Align.INLINE)
d.comment(0x85e6, 'shift into the value', align=Align.INLINE)
d.comment(0x85e7, '...', align=Align.INLINE)
d.comment(0x85e9, '...', align=Align.INLINE)
d.comment(0x85eb, '...', align=Align.INLINE)
d.comment(0x85ec, '...', align=Align.INLINE)
d.comment(0x85ee, 'next character', align=Align.INLINE)
d.comment(0x85ef, 'loop for three', align=Align.INLINE)

# execute_line (&8B0B) and the immediate-mode dispatch gaps.
d.comment(0x8b0d, '...', align=Align.INLINE)
d.comment(0x8b0f, '...', align=Align.INLINE)
d.comment(0x8b11, '...', align=Align.INLINE)
d.comment(0x8b15, '...', align=Align.INLINE)
d.comment(0x8b17, 'Clear the machine-stack marker', align=Align.INLINE)
d.comment(0x8b1d, 'Y = 0', align=Align.INLINE)
d.comment(0x8b20, '...', align=Align.INLINE)
d.comment(0x8b22, '...', align=Align.INLINE)
d.comment(0x8b24, '...', align=Align.INLINE)
d.comment(0x8b26, 'clear the quote flag', align=Align.INLINE)
d.comment(0x8b28, 'and the offset', align=Align.INLINE)
d.comment(0x8b2a, 'Tokenise the line', align=Align.INLINE)
d.comment(0x8b30, 'no line number: execute it', align=Align.INLINE)
d.comment(0x8b35, 'inserted: immediate loop', align=Align.INLINE)
d.comment(0x8b41, 'Back to immediate mode', align=Align.INLINE)
d.comment(0x8b44, 'Enter the assembler', align=Align.INLINE)
d.comment(0x8b47, 'Inside a function call?', align=Align.INLINE)
d.comment(0x8b48, '...', align=Align.INLINE)
d.comment(0x8b4a, 'no: error', align=Align.INLINE)
d.comment(0x8b4c, 'Pushed token', align=Align.INLINE)
d.comment(0x8b4f, 'FN?', align=Align.INLINE)
d.comment(0x8b51, 'no: error', align=Align.INLINE)
d.comment(0x8b53, 'Evaluate the return value', align=Align.INLINE)
d.comment(0x8b56, 'check end, return from the function', align=Align.INLINE)
d.comment(0x8b7d, 'CR', align=Align.INLINE)
d.comment(0x8b7f, 'Line offset', align=Align.INLINE)
d.comment(0x8b81, '...', align=Align.INLINE)
d.comment(0x8b82, 'Scan to the end of line', align=Align.INLINE)
d.comment(0x8b83, '...', align=Align.INLINE)
d.comment(0x8b85, '...', align=Align.INLINE)
d.comment(0x8b87, 'ELSE?', align=Align.INLINE)
d.comment(0x8b89, 'yes: skip to end of line', align=Align.INLINE)
d.comment(0x8b8b, 'In the command buffer?', align=Align.INLINE)
d.comment(0x8b8d, '...', align=Align.INLINE)
d.comment(0x8b8f, 'yes: immediate mode', align=Align.INLINE)
d.comment(0x8b91, 'Check for end of program, step past CR', align=Align.INLINE)
d.comment(0x8b94, 'more: next statement', align=Align.INLINE)

# read_input_line (&BC02): print a prompt char, read a line (OSWORD 0).
d.comment(0xbc02, 'Print the prompt character', align=Align.INLINE)
d.comment(0xbc05, 'Input buffer at &0700', align=Align.INLINE)
d.comment(0xbc07, '...', align=Align.INLINE)
d.comment(0xbc09, '...', align=Align.INLINE)
d.comment(0xbc0b, '...', align=Align.INLINE)
d.comment(0xbc0d, 'Max length 238', align=Align.INLINE)
d.comment(0xbc0f, '...', align=Align.INLINE)
d.comment(0xbc11, 'Lowest accepted character', align=Align.INLINE)
d.comment(0xbc13, '...', align=Align.INLINE)
d.comment(0xbc15, 'Highest accepted character (&FF)', align=Align.INLINE)
d.comment(0xbc17, '...', align=Align.INLINE)
d.comment(0xbc19, '...', align=Align.INLINE)
d.comment(0xbc1a, 'Point at the OSWORD block', align=Align.INLINE)
d.comment(0xbc1c, '...', align=Align.INLINE)
d.comment(0xbc1d, 'Read a line', align=Align.INLINE)
d.comment(0xbc20, 'ok: reset the column', align=Align.INLINE)
d.comment(0xbc22, 'Escape: raise it', align=Align.INLINE)
d.comment(0xbc25, 'Print a newline', align=Align.INLINE)
d.comment(0xbc28, 'Reset the column to 0', align=Align.INLINE)
d.comment(0xbc2a, '...', align=Align.INLINE)
d.comment(0xbc2c, 'Return', align=Align.INLINE)

# INPUT# (&B9CF): read variables from an open file via OSBGET.
d.comment(0xb9cf, 'Back up over "#"', align=Align.INLINE)
d.comment(0xb9d1, 'Get the file handle', align=Align.INLINE)
d.comment(0xb9d4, 'Sync the program pointer', align=Align.INLINE)
d.comment(0xb9d6, '...', align=Align.INLINE)
d.comment(0xb9d8, 'save the handle', align=Align.INLINE)
d.comment(0xb9da, 'Skip spaces', align=Align.INLINE)
d.comment(0xb9dd, "','  another variable?", align=Align.INLINE)
d.comment(0xb9df, 'no: done', align=Align.INLINE)
d.comment(0xb9e1, 'Save the handle', align=Align.INLINE)
d.comment(0xb9e3, '...', align=Align.INLINE)
d.comment(0xb9e4, 'Parse the target variable', align=Align.INLINE)
d.comment(0xb9e7, 'end: error', align=Align.INLINE)
d.comment(0xb9e9, 'Sync the program pointer', align=Align.INLINE)
d.comment(0xb9eb, '...', align=Align.INLINE)
d.comment(0xb9ed, 'Recover the handle', align=Align.INLINE)
d.comment(0xb9ee, '...', align=Align.INLINE)
d.comment(0xb9f0, '...', align=Align.INLINE)
d.comment(0xb9f1, 'Stack the variable address', align=Align.INLINE)
d.comment(0xb9f4, 'Handle', align=Align.INLINE)
d.comment(0xb9f6, 'Read the type byte', align=Align.INLINE)
d.comment(0xb9f9, 'save it', align=Align.INLINE)
d.comment(0xb9fb, '...', align=Align.INLINE)
d.comment(0xb9fc, 'string?', align=Align.INLINE)
d.comment(0xb9fe, 'String type byte', align=Align.INLINE)
d.comment(0xba00, 'mismatch: error', align=Align.INLINE)
d.comment(0xba02, 'Read the length', align=Align.INLINE)
d.comment(0xba05, '...', align=Align.INLINE)
d.comment(0xba07, '...', align=Align.INLINE)
d.comment(0xba08, 'empty', align=Align.INLINE)
d.comment(0xba0a, 'Read a character', align=Align.INLINE)
d.comment(0xba0d, '...', align=Align.INLINE)
d.comment(0xba10, '...', align=Align.INLINE)
d.comment(0xba11, 'loop', align=Align.INLINE)
d.comment(0xba13, 'Assign the string', align=Align.INLINE)
d.comment(0xba16, 'next variable', align=Align.INLINE)
d.comment(0xba19, 'Numeric type byte', align=Align.INLINE)
d.comment(0xba1b, 'mismatch: error', align=Align.INLINE)
d.comment(0xba1d, 'real?', align=Align.INLINE)
d.comment(0xba1f, 'Integer: 4 bytes', align=Align.INLINE)
d.comment(0xba21, 'Read a byte', align=Align.INLINE)
d.comment(0xba24, '...', align=Align.INLINE)
d.comment(0xba26, '...', align=Align.INLINE)
d.comment(0xba27, 'loop', align=Align.INLINE)
d.comment(0xba29, 'assign', align=Align.INLINE)
d.comment(0xba2b, 'Real: 5 bytes', align=Align.INLINE)
d.comment(0xba2d, 'Read a byte', align=Align.INLINE)
d.comment(0xba30, '...', align=Align.INLINE)
d.comment(0xba33, '...', align=Align.INLINE)
d.comment(0xba34, 'loop', align=Align.INLINE)
d.comment(0xba36, 'unpack into FWA', align=Align.INLINE)
d.comment(0xba39, 'Assign the number', align=Align.INLINE)
d.comment(0xba3c, 'next variable', align=Align.INLINE)
d.comment(0xba3f, 'Drop the stacked values', align=Align.INLINE)
d.comment(0xba40, '...', align=Align.INLINE)
d.comment(0xba41, 'done', align=Align.INLINE)

# Tokeniser line-number insertion (&88DA) and encode_line_number (&88F5).
d.comment(0x88da, 'Back up', align=Align.INLINE)
d.comment(0x88db, 'Line-number token &8D', align=Align.INLINE)
d.comment(0x88dd, 'Make room for the 3 encoded bytes', align=Align.INLINE)
d.comment(0x88e0, 'Destination = source + 2', align=Align.INLINE)
d.comment(0x88e2, '...', align=Align.INLINE)
d.comment(0x88e4, '...', align=Align.INLINE)
d.comment(0x88e6, '...', align=Align.INLINE)
d.comment(0x88e8, '...', align=Align.INLINE)
d.comment(0x88ea, '...', align=Align.INLINE)
d.comment(0x88ec, 'Shift the bytes up', align=Align.INLINE)
d.comment(0x88ee, '...', align=Align.INLINE)
d.comment(0x88f0, '...', align=Align.INLINE)
d.comment(0x88f1, 'loop', align=Align.INLINE)
d.comment(0x88f3, 'Three encoded bytes', align=Align.INLINE)
d.comment(0x88f5, 'Byte 2 = low | &40', align=Align.INLINE)
d.comment(0x88f7, '...', align=Align.INLINE)
d.comment(0x88f9, '...', align=Align.INLINE)
d.comment(0x88fb, '...', align=Align.INLINE)
d.comment(0x88fc, 'Byte 1 = high (6 bits) | &40', align=Align.INLINE)
d.comment(0x88fe, '...', align=Align.INLINE)
d.comment(0x8900, '...', align=Align.INLINE)
d.comment(0x8902, '...', align=Align.INLINE)
d.comment(0x8904, 'Byte 0: scramble the top bits', align=Align.INLINE)
d.comment(0x8905, '...', align=Align.INLINE)
d.comment(0x8907, '...', align=Align.INLINE)
d.comment(0x8909, '...', align=Align.INLINE)
d.comment(0x890b, '...', align=Align.INLINE)
d.comment(0x890d, '...', align=Align.INLINE)
d.comment(0x890f, '...', align=Align.INLINE)
d.comment(0x8910, '...', align=Align.INLINE)
d.comment(0x8911, '...', align=Align.INLINE)
d.comment(0x8913, '...', align=Align.INLINE)
d.comment(0x8914, '...', align=Align.INLINE)
d.comment(0x8915, '...', align=Align.INLINE)
d.comment(0x8917, 'store the control byte', align=Align.INLINE)
d.comment(0x8919, 'Advance past the 3 bytes', align=Align.INLINE)
d.comment(0x891c, '...', align=Align.INLINE)
d.comment(0x891f, '...', align=Align.INLINE)
d.comment(0x8922, '...', align=Align.INLINE)
d.comment(0x8924, 'not a name character', align=Align.INLINE)
d.comment(0x8925, '...', align=Align.INLINE)

# is_alphanumeric (&8926).
d.comment(0x8926, "above 'z'?", align=Align.INLINE)
d.comment(0x8928, 'yes: no', align=Align.INLINE)
d.comment(0x892a, "'_' or above?", align=Align.INLINE)
d.comment(0x892c, 'yes: name char', align=Align.INLINE)
d.comment(0x892e, "'[' to '^'?", align=Align.INLINE)
d.comment(0x8930, 'yes: no', align=Align.INLINE)
d.comment(0x8932, "'A' or above?", align=Align.INLINE)
d.comment(0x8934, 'yes: name char', align=Align.INLINE)
d.comment(0x8936, "above '9'?", align=Align.INLINE)
d.comment(0x8938, 'yes: no', align=Align.INLINE)
d.comment(0x893a, "digit?", align=Align.INLINE)
d.comment(0x893c, 'carry set if so', align=Align.INLINE)
d.comment(0x893d, "'.'?", align=Align.INLINE)
d.comment(0x893f, 'no: test alphanumeric', align=Align.INLINE)
d.comment(0x8941, 'Return', align=Align.INLINE)

# PRINT# (&8D2B): write values to an open file via OSBPUT.
d.comment(0x8d2b, 'Back up over "#"', align=Align.INLINE)
d.comment(0x8d2d, 'Get the file handle', align=Align.INLINE)
d.comment(0x8d30, 'Save the handle', align=Align.INLINE)
d.comment(0x8d31, '...', align=Align.INLINE)
d.comment(0x8d32, 'Skip spaces', align=Align.INLINE)
d.comment(0x8d35, "','  another value?", align=Align.INLINE)
d.comment(0x8d37, 'no: done', align=Align.INLINE)
d.comment(0x8d39, 'Evaluate the value', align=Align.INLINE)
d.comment(0x8d3c, 'pack it (in case real)', align=Align.INLINE)
d.comment(0x8d3f, 'Recover the handle', align=Align.INLINE)
d.comment(0x8d40, '...', align=Align.INLINE)
d.comment(0x8d41, 'Type byte', align=Align.INLINE)
d.comment(0x8d43, 'write it', align=Align.INLINE)
d.comment(0x8d46, '...', align=Align.INLINE)
d.comment(0x8d47, 'string?', align=Align.INLINE)
d.comment(0x8d49, 'real?', align=Align.INLINE)
d.comment(0x8d4b, 'Integer: 4 bytes', align=Align.INLINE)
d.comment(0x8d4d, 'Write a byte', align=Align.INLINE)
d.comment(0x8d4f, '...', align=Align.INLINE)
d.comment(0x8d52, '...', align=Align.INLINE)
d.comment(0x8d53, 'loop', align=Align.INLINE)
d.comment(0x8d55, 'next value', align=Align.INLINE)
d.comment(0x8d57, 'Real: 5 bytes', align=Align.INLINE)
d.comment(0x8d59, 'Write a byte', align=Align.INLINE)
d.comment(0x8d5c, '...', align=Align.INLINE)
d.comment(0x8d5f, '...', align=Align.INLINE)
d.comment(0x8d60, 'loop', align=Align.INLINE)
d.comment(0x8d62, 'next value', align=Align.INLINE)
d.comment(0x8d64, 'String: write the length', align=Align.INLINE)
d.comment(0x8d66, '...', align=Align.INLINE)
d.comment(0x8d69, '...', align=Align.INLINE)
d.comment(0x8d6a, 'empty', align=Align.INLINE)
d.comment(0x8d6c, 'Write a character', align=Align.INLINE)
d.comment(0x8d6f, '...', align=Align.INLINE)
d.comment(0x8d72, '...', align=Align.INLINE)
d.comment(0x8d73, 'loop', align=Align.INLINE)
d.comment(0x8d75, 'next value', align=Align.INLINE)
d.comment(0x8d77, 'Recover the handle', align=Align.INLINE)
d.comment(0x8d78, 'sync the pointer', align=Align.INLINE)
d.comment(0x8d7a, 'next statement', align=Align.INLINE)

# iwa_store_var (&B4C6): store IWA into a variable (size in &39).
d.comment(0xb4c6, 'Offset 0', align=Align.INLINE)
d.comment(0xb4c8, 'Store byte 1', align=Align.INLINE)
d.comment(0xb4ca, '...', align=Align.INLINE)
d.comment(0xb4cc, 'Size byte', align=Align.INLINE)
d.comment(0xb4ce, '1-byte value: done', align=Align.INLINE)
d.comment(0xb4d0, 'Store byte 2', align=Align.INLINE)
d.comment(0xb4d2, '...', align=Align.INLINE)
d.comment(0xb4d3, '...', align=Align.INLINE)
d.comment(0xb4d5, 'Store byte 3', align=Align.INLINE)
d.comment(0xb4d7, '...', align=Align.INLINE)
d.comment(0xb4d8, '...', align=Align.INLINE)
d.comment(0xb4da, 'Store byte 4', align=Align.INLINE)
d.comment(0xb4dc, '...', align=Align.INLINE)
d.comment(0xb4dd, '...', align=Align.INLINE)

# check_line_number (&97DF) / decode_line_number (&97EB).
d.comment(0x97df, 'Next character', align=Align.INLINE)
d.comment(0x97e1, '...', align=Align.INLINE)
d.comment(0x97e3, 'space?', align=Align.INLINE)
d.comment(0x97e5, 'skip it', align=Align.INLINE)
d.comment(0x97e7, 'line-number token?', align=Align.INLINE)
d.comment(0x97e9, 'no: carry clear', align=Align.INLINE)
d.comment(0x97eb, 'Control byte', align=Align.INLINE)
d.comment(0x97ec, 'read the packed top-bits byte', align=Align.INLINE)
d.comment(0x97ee, 'recover the top bits', align=Align.INLINE)
d.comment(0x97ef, '(shifted left by two)', align=Align.INLINE)
d.comment(0x97f0, 'keep a copy for the high byte', align=Align.INLINE)
d.comment(0x97f1, 'low byte top bits', align=Align.INLINE)
d.comment(0x97f3, 'next encoded byte', align=Align.INLINE)
d.comment(0x97f4, 'XOR the encoded low byte', align=Align.INLINE)
d.comment(0x97f6, 'line number low', align=Align.INLINE)
d.comment(0x97f8, 'high byte top bits', align=Align.INLINE)
d.comment(0x97f9, 'shift the high byte top bits into place,', align=Align.INLINE)
d.comment(0x97fa, '(two places)', align=Align.INLINE)
d.comment(0x97fb, 'next encoded byte', align=Align.INLINE)
d.comment(0x97fc, 'XOR the encoded high byte', align=Align.INLINE)
d.comment(0x97fe, 'line number high', align=Align.INLINE)
d.comment(0x9800, 'step past the 3 bytes', align=Align.INLINE)
d.comment(0x9801, 'save the advanced text offset', align=Align.INLINE)
d.comment(0x9803, 'carry set: found', align=Align.INLINE)
d.comment(0x9804, 'Return', align=Align.INLINE)
d.comment(0x9805, 'carry clear: not a line number', align=Align.INLINE)
d.comment(0x9806, 'Return', align=Align.INLINE)

# sub_c9807: copy PtrA to PtrB, then expect "=" and evaluate.
d.comment(0x9807, 'Copy PtrA to PtrB', align=Align.INLINE)
d.comment(0x9809, '...', align=Align.INLINE)
d.comment(0x980b, '...', align=Align.INLINE)
d.comment(0x980d, '...', align=Align.INLINE)
d.comment(0x980f, '...', align=Align.INLINE)
d.comment(0x9811, '...', align=Align.INLINE)
d.comment(0x9813, 'Next character', align=Align.INLINE)
d.comment(0x9815, '...', align=Align.INLINE)
d.comment(0x9817, '...', align=Align.INLINE)
d.comment(0x9819, 'space?', align=Align.INLINE)
d.comment(0x981b, 'skip it', align=Align.INLINE)
d.comment(0x981d, '"="?', align=Align.INLINE)
d.comment(0x981f, 'yes: evaluate', align=Align.INLINE)
d.comment(0x9821, 'Mistake error', align=Align.INLINE)
d.comment(0x982a, 'Mistake error', align=Align.INLINE)
d.comment(0x9838, 'Escape error', align=Align.INLINE)
d.comment(0x9841, 'Skip spaces', align=Align.INLINE)
d.comment(0x9844, '"="?', align=Align.INLINE)
d.comment(0x9846, 'no: Mistake', align=Align.INLINE)
d.comment(0x9848, 'Return', align=Align.INLINE)
d.comment(0x9849, 'Evaluate the right-hand side', align=Align.INLINE)
d.comment(0x984c, 'Result type', align=Align.INLINE)
d.comment(0x984d, 'Sync the program pointer', align=Align.INLINE)
d.comment(0x984f, 'check the statement ends', align=Align.INLINE)
d.comment(0x9852, 'Sync the program pointer', align=Align.INLINE)
d.comment(0x9854, 'check the statement ends', align=Align.INLINE)

# Comparison result and the compare helper (&9A92).
d.comment(0x9a92, 'Equal: return', align=Align.INLINE)
d.comment(0x9a93, 'Combine the compare carry...', align=Align.INLINE)
d.comment(0x9a94, '...with the sign', align=Align.INLINE)
d.comment(0x9a96, '...for the ordering', align=Align.INLINE)
d.comment(0x9a97, 'result nonzero', align=Align.INLINE)
d.comment(0x9a99, 'Return', align=Align.INLINE)
d.comment(0x9a9a, 'Type mismatch error', align=Align.INLINE)
d.comment(0x9a9d, 'Current type', align=Align.INLINE)
d.comment(0x9a9e, 'string: compare strings', align=Align.INLINE)
d.comment(0x9aa0, 'float: compare floats', align=Align.INLINE)
d.comment(0x9aa2, 'Stack the integer', align=Align.INLINE)
d.comment(0x9aa5, 'evaluate the next operand', align=Align.INLINE)
d.comment(0x9aa8, 'type', align=Align.INLINE)
d.comment(0x9aa9, 'string: Type mismatch', align=Align.INLINE)
d.comment(0x9aab, 'float: compare floats', align=Align.INLINE)

# String comparison loop (&9B03).
d.comment(0x9b03, 'Reached the shorter length?', align=Align.INLINE)
d.comment(0x9b05, 'yes: compare lengths', align=Align.INLINE)
d.comment(0x9b07, 'Next character', align=Align.INLINE)
d.comment(0x9b08, 'stacked string', align=Align.INLINE)
d.comment(0x9b0a, 'vs current string', align=Align.INLINE)
d.comment(0x9b0d, 'equal: continue', align=Align.INLINE)
d.comment(0x9b0f, 'differ', align=Align.INLINE)
d.comment(0x9b11, 'Compare the lengths', align=Align.INLINE)
d.comment(0x9b13, '...', align=Align.INLINE)
d.comment(0x9b15, 'Save the result', align=Align.INLINE)
d.comment(0x9b16, 'Drop the stacked string', align=Align.INLINE)
d.comment(0x9b19, '...', align=Align.INLINE)
d.comment(0x9b1b, 'Restore the result', align=Align.INLINE)
d.comment(0x9b1c, 'Return', align=Align.INLINE)

# String concatenation (&9C15): str + str.
d.comment(0x9c15, 'Stack the left string', align=Align.INLINE)
d.comment(0x9c18, 'Evaluate the right operand', align=Align.INLINE)
d.comment(0x9c1b, 'type', align=Align.INLINE)
d.comment(0x9c1c, 'number: Type mismatch', align=Align.INLINE)
d.comment(0x9c1e, 'New length = left + right', align=Align.INLINE)
d.comment(0x9c1f, '...', align=Align.INLINE)
d.comment(0x9c21, '...', align=Align.INLINE)
d.comment(0x9c23, '...', align=Align.INLINE)
d.comment(0x9c25, '...', align=Align.INLINE)
d.comment(0x9c27, 'over 255: error', align=Align.INLINE)
d.comment(0x9c29, 'Save the new length', align=Align.INLINE)
d.comment(0x9c2a, '...', align=Align.INLINE)
d.comment(0x9c2b, 'Move the right string up', align=Align.INLINE)
d.comment(0x9c2d, '...', align=Align.INLINE)
d.comment(0x9c30, '...', align=Align.INLINE)
d.comment(0x9c33, '...', align=Align.INLINE)
d.comment(0x9c34, '...', align=Align.INLINE)
d.comment(0x9c35, 'loop', align=Align.INLINE)
d.comment(0x9c37, 'Prepend the left string', align=Align.INLINE)
d.comment(0x9c3a, 'Set the new length', align=Align.INLINE)
d.comment(0x9c3b, '...', align=Align.INLINE)
d.comment(0x9c3d, '...', align=Align.INLINE)
d.comment(0x9c3f, 'string result', align=Align.INLINE)
d.comment(0x9c40, 'loop for further + or -', align=Align.INLINE)

# DIM var n (&90DF): allocate an n+1 byte block at the variable top.
d.comment(0x90dc, 'No room error', align=Align.INLINE)
d.comment(0x90df, 'Back up to the variable', align=Align.INLINE)
d.comment(0x90e1, 'Parse it', align=Align.INLINE)
d.comment(0x90e4, 'not a variable: Bad DIM', align=Align.INLINE)
d.comment(0x90e6, 'indirection: Bad DIM', align=Align.INLINE)
d.comment(0x90e8, 'Stack the variable address', align=Align.INLINE)
d.comment(0x90eb, 'Evaluate the size', align=Align.INLINE)
d.comment(0x90ee, 'n + 1 bytes', align=Align.INLINE)
d.comment(0x90f1, 'fits in 16 bits?', align=Align.INLINE)
d.comment(0x90f3, '...', align=Align.INLINE)
d.comment(0x90f5, 'no: Bad DIM', align=Align.INLINE)
d.comment(0x90f7, 'New top = top + size', align=Align.INLINE)
d.comment(0x90f8, '...', align=Align.INLINE)
d.comment(0x90fa, '...', align=Align.INLINE)
d.comment(0x90fc, '...', align=Align.INLINE)
d.comment(0x90fd, '...', align=Align.INLINE)
d.comment(0x90ff, '...', align=Align.INLINE)
d.comment(0x9101, '...', align=Align.INLINE)
d.comment(0x9102, 'collides with the stack?', align=Align.INLINE)
d.comment(0x9104, '...', align=Align.INLINE)
d.comment(0x9106, 'yes: No room', align=Align.INLINE)
d.comment(0x9108, 'Block address = old top', align=Align.INLINE)
d.comment(0x910a, '...', align=Align.INLINE)
d.comment(0x910c, '...', align=Align.INLINE)
d.comment(0x910e, '...', align=Align.INLINE)
d.comment(0x9110, 'Commit the new top', align=Align.INLINE)
d.comment(0x9112, '...', align=Align.INLINE)
d.comment(0x9114, 'Result is the address', align=Align.INLINE)
d.comment(0x9116, '...', align=Align.INLINE)
d.comment(0x9118, '...', align=Align.INLINE)
d.comment(0x911a, 'integer type', align=Align.INLINE)
d.comment(0x911c, '...', align=Align.INLINE)
d.comment(0x911e, 'assign the address to the variable', align=Align.INLINE)

# language_entry (&8000): the ROM language entry point.
d.comment(0x8000, 'A=1: language start?', align=Align.INLINE)
d.comment(0x8002, 'yes: start BASIC', align=Align.INLINE)
d.comment(0x8004, 'otherwise return', align=Align.INLINE)

# fn_abs (&AD6A): ABS(x).
d.comment(0xad6a, 'Evaluate the argument', align=Align.INLINE)
d.comment(0xad6d, 'zero: return it', align=Align.INLINE)
d.comment(0xad6f, 'real: clear the sign', align=Align.INLINE)

# fn_himem (&AF03): HIMEM.
d.comment(0xaf03, 'HIMEM low', align=Align.INLINE)
d.comment(0xaf05, 'HIMEM high', align=Align.INLINE)
d.comment(0xaf07, 'return as an integer', align=Align.INLINE)

# stmt_clg (&8EBD): CLG -> VDU 16.
d.comment(0x8ebd, 'Check the statement ends', align=Align.INLINE)
d.comment(0x8ec0, 'VDU 16 (clear graphics)', align=Align.INLINE)
d.comment(0x8ec2, 'send it', align=Align.INLINE)

# stmt_clear (&928D): CLEAR.
d.comment(0x928d, 'Check the statement ends', align=Align.INLINE)
d.comment(0x9290, 'Clear variables, heap and stack', align=Align.INLINE)
d.comment(0x9293, 'next statement', align=Align.INLINE)

# coerce_to_integer (&92F0) / eval_real (&92FA) / ensure_real (&92FD).
d.comment(0x92f0, 'string?', align=Align.INLINE)
d.comment(0x92f2, 'integer: return', align=Align.INLINE)
d.comment(0x92f4, 'real: convert to integer', align=Align.INLINE)
d.comment(0x92f7, 'Type mismatch error', align=Align.INLINE)
d.comment(0x92fa, 'Evaluate a factor', align=Align.INLINE)
d.comment(0x92fd, 'string?', align=Align.INLINE)
d.comment(0x92ff, 'real: return', align=Align.INLINE)
d.comment(0x9301, 'integer: convert to real', align=Align.INLINE)

# sub_c92e3: evaluate a factor as an integer.
d.comment(0x92e3, 'Evaluate a factor', align=Align.INLINE)
d.comment(0x92e6, 'string: Type mismatch', align=Align.INLINE)
d.comment(0x92e8, 'real: convert to integer', align=Align.INLINE)
d.comment(0x92ea, 'Return', align=Align.INLINE)
d.comment(0x92eb, 'Expect "=" and evaluate', align=Align.INLINE)
d.comment(0x92ee, 'Result type, then coerce to integer', align=Align.INLINE)

# stmt_report (&BFE4): REPORT - print the last error message.
d.comment(0xbfe4, 'Check the statement ends', align=Align.INLINE)
d.comment(0xbfe7, 'Newline', align=Align.INLINE)
d.comment(0xbfea, 'From offset 1', align=Align.INLINE)
d.comment(0xbfec, 'Error message byte', align=Align.INLINE)
d.comment(0xbfee, 'terminator: done', align=Align.INLINE)
d.comment(0xbff0, 'print it', align=Align.INLINE)
d.comment(0xbff3, 'next', align=Align.INLINE)
d.comment(0xbff4, 'loop', align=Align.INLINE)
d.comment(0xbff6, 'next statement', align=Align.INLINE)

# fn_point continuation gaps.
d.comment(0xab55, '...', align=Align.INLINE)
d.comment(0xab59, '...', align=Align.INLINE)
d.comment(0xab5c, '...', align=Align.INLINE)
d.comment(0xab66, 'Result sign (off-screen = -1)', align=Align.INLINE)

# fn_openup (&BF80): OPENIN/OPENOUT/OPENUP -> OSFIND.
d.comment(0xbf80, 'OPENUP action &C0', align=Align.INLINE)
d.comment(0xbf82, 'Save the action', align=Align.INLINE)
d.comment(0xbf83, 'Evaluate the filename', align=Align.INLINE)
d.comment(0xbf86, 'not a string: error', align=Align.INLINE)
d.comment(0xbf88, 'CR-terminate it', align=Align.INLINE)
d.comment(0xbf8b, 'Point at the string buffer', align=Align.INLINE)
d.comment(0xbf8d, '...', align=Align.INLINE)
d.comment(0xbf8f, 'recover the action', align=Align.INLINE)
d.comment(0xbf90, 'Open the file', align=Align.INLINE)
d.comment(0xbf93, 'return the handle', align=Align.INLINE)
d.comment(0xbf96, 'Type mismatch error', align=Align.INLINE)

# stmt_ptr (&BF30): PTR#n = value -> OSARGS.
d.comment(0xbf30, 'Evaluate the #handle', align=Align.INLINE)
d.comment(0xbf33, 'save it', align=Align.INLINE)
d.comment(0xbf34, 'Expect "=" and evaluate', align=Align.INLINE)
d.comment(0xbf37, 'coerce to integer', align=Align.INLINE)
d.comment(0xbf3a, 'Recover the handle', align=Align.INLINE)
d.comment(0xbf3b, '...', align=Align.INLINE)
d.comment(0xbf3c, 'Point at the value', align=Align.INLINE)
d.comment(0xbf3e, 'Write the file pointer', align=Align.INLINE)
d.comment(0xbf43, 'next statement', align=Align.INLINE)

# stmt_vdu loop (&9432): output bytes via OSWRCH.
d.comment(0x9432, "':' end of statement?", align=Align.INLINE)
d.comment(0x9434, 'yes', align=Align.INLINE)
d.comment(0x9436, 'end of line?', align=Align.INLINE)
d.comment(0x9438, 'yes', align=Align.INLINE)
d.comment(0x943a, 'ELSE?', align=Align.INLINE)
d.comment(0x943c, 'yes', align=Align.INLINE)
d.comment(0x943e, 'Back up to the value', align=Align.INLINE)
d.comment(0x9440, 'Evaluate it', align=Align.INLINE)
d.comment(0x9443, 'send the low byte', align=Align.INLINE)
d.comment(0x9446, 'Next character', align=Align.INLINE)
d.comment(0x9449, "','  another byte?", align=Align.INLINE)
d.comment(0x944b, 'yes', align=Align.INLINE)
d.comment(0x944d, "';'  16-bit value?", align=Align.INLINE)
d.comment(0x944f, 'no: check the statement ends', align=Align.INLINE)
d.comment(0x9451, 'yes: send the high byte too', align=Align.INLINE)
d.comment(0x9453, 'next statement', align=Align.INLINE)

# sub_c8f92 / sub_c8f9a: set up pointers for the program scan.
d.comment(0x8f92, 'Copy TOP to &3B/&3C', align=Align.INLINE)
d.comment(0x8f94, '...', align=Align.INLINE)
d.comment(0x8f96, '...', align=Align.INLINE)
d.comment(0x8f98, '...', align=Align.INLINE)
d.comment(0x8f9a, 'Point &37/&38 at PAGE', align=Align.INLINE)
d.comment(0x8f9c, '...', align=Align.INLINE)
d.comment(0x8f9e, '...', align=Align.INLINE)
d.comment(0x8fa0, '...', align=Align.INLINE)
d.comment(0x8fa2, 'Return', align=Align.INLINE)

# stmt_sound (&B44C): SOUND chan, amp, pitch, dur -> OSWORD 7.
d.comment(0xb44c, 'Evaluate the first parameter', align=Align.INLINE)
d.comment(0xb44f, 'three more', align=Align.INLINE)
d.comment(0xb451, 'Stack the 16-bit value', align=Align.INLINE)
d.comment(0xb453, '...', align=Align.INLINE)
d.comment(0xb454, '...', align=Align.INLINE)
d.comment(0xb456, '...', align=Align.INLINE)
d.comment(0xb457, 'save the counter', align=Align.INLINE)
d.comment(0xb458, '...', align=Align.INLINE)
d.comment(0xb459, 'step past the comma, evaluate the next', align=Align.INLINE)
d.comment(0xb45c, 'restore the counter', align=Align.INLINE)
d.comment(0xb45d, '...', align=Align.INLINE)
d.comment(0xb45e, '...', align=Align.INLINE)
d.comment(0xb45f, 'loop', align=Align.INLINE)
d.comment(0xb461, 'Check the statement ends', align=Align.INLINE)
d.comment(0xb464, 'Last value to the block end', align=Align.INLINE)
d.comment(0xb466, '...', align=Align.INLINE)
d.comment(0xb468, '...', align=Align.INLINE)
d.comment(0xb46a, '...', align=Align.INLINE)
d.comment(0xb46c, 'OSWORD 7, 6 bytes', align=Align.INLINE)
d.comment(0xb46e, '...', align=Align.INLINE)
d.comment(0xb470, 'pop into the block and call', align=Align.INLINE)

# stmt_envelope (&B472): ENVELOPE 14 params -> OSWORD 8.
d.comment(0xb472, 'Evaluate the first parameter', align=Align.INLINE)
d.comment(0xb475, '13 more', align=Align.INLINE)
d.comment(0xb477, 'Stack the 8-bit value', align=Align.INLINE)
d.comment(0xb479, '...', align=Align.INLINE)
d.comment(0xb47a, 'save the counter', align=Align.INLINE)
d.comment(0xb47b, '...', align=Align.INLINE)
d.comment(0xb47c, 'step past the comma, evaluate the next', align=Align.INLINE)
d.comment(0xb47f, 'restore the counter', align=Align.INLINE)
d.comment(0xb480, '...', align=Align.INLINE)
d.comment(0xb481, '...', align=Align.INLINE)
d.comment(0xb482, 'loop', align=Align.INLINE)
d.comment(0xb484, 'Check the statement ends', align=Align.INLINE)
d.comment(0xb487, 'Last value to the block end', align=Align.INLINE)
d.comment(0xb489, '...', align=Align.INLINE)
d.comment(0xb48b, 'OSWORD 8, 12 bytes', align=Align.INLINE)
d.comment(0xb48d, '...', align=Align.INLINE)
d.comment(0xb48f, 'Pop a byte into the control block', align=Align.INLINE)
d.comment(0xb490, '...', align=Align.INLINE)
d.comment(0xb492, '...', align=Align.INLINE)
d.comment(0xb493, 'loop', align=Align.INLINE)
d.comment(0xb495, 'OSWORD number', align=Align.INLINE)
d.comment(0xb496, 'Point at the control block', align=Align.INLINE)
d.comment(0xb498, '...', align=Align.INLINE)
d.comment(0xb49d, 'next statement', align=Align.INLINE)

# Assembler opcode-table match (&85F1) and tokenised AND/EOR/OR.
d.comment(0x85f1, 'Point to the end of the opcode table', align=Align.INLINE)
d.comment(0x85f3, 'Compacted mnemonic low byte', align=Align.INLINE)
d.comment(0x85f5, 'Compare the low half', align=Align.INLINE)
d.comment(0x85f8, 'no match: next entry', align=Align.INLINE)
d.comment(0x85fa, 'High half', align=Align.INLINE)
d.comment(0x85fd, '...', align=Align.INLINE)
d.comment(0x85ff, 'matched', align=Align.INLINE)
d.comment(0x8601, 'Next entry', align=Align.INLINE)
d.comment(0x8602, 'loop', align=Align.INLINE)
d.comment(0x8604, 'not matched: Mistake', align=Align.INLINE)
d.comment(0x8607, "opcode index for AND", align=Align.INLINE)
d.comment(0x8609, 'tokenised AND?', align=Align.INLINE)
d.comment(0x860b, 'yes', align=Align.INLINE)
d.comment(0x860d, 'EOR index', align=Align.INLINE)
d.comment(0x860e, 'tokenised EOR?', align=Align.INLINE)
d.comment(0x8610, 'yes', align=Align.INLINE)
d.comment(0x8612, 'ORA index', align=Align.INLINE)
d.comment(0x8613, 'tokenised OR?', align=Align.INLINE)
d.comment(0x8615, 'no: Mistake', align=Align.INLINE)
d.comment(0x8617, "step past, expect 'A'", align=Align.INLINE)
d.comment(0x8619, '...', align=Align.INLINE)
d.comment(0x861a, '...', align=Align.INLINE)
d.comment(0x861c, "'A'?", align=Align.INLINE)
d.comment(0x861e, 'no: Mistake', align=Align.INLINE)
# Addressing-mode parser skip-spaces / register checks.
d.comment(0x86bb, 'Skip spaces', align=Align.INLINE)
d.comment(0x86d7, 'Skip spaces', align=Align.INLINE)
d.comment(0x86e1, 'Skip spaces', align=Align.INLINE)
d.comment(0x86e8, 'Skip spaces', align=Align.INLINE)
d.comment(0x86eb, "','?", align=Align.INLINE)
d.comment(0x86ed, 'no: Index error', align=Align.INLINE)
d.comment(0x86f2, 'Skip spaces', align=Align.INLINE)
d.comment(0x86f5, "'Y'?", align=Align.INLINE)
d.comment(0x86f7, 'no: Index error', align=Align.INLINE)
d.comment(0x86fb, "','?", align=Align.INLINE)
d.comment(0x86fd, 'no: Index error', align=Align.INLINE)
d.comment(0x86ff, 'Skip spaces', align=Align.INLINE)
d.comment(0x8702, "'X'?", align=Align.INLINE)
d.comment(0x8704, 'no: Index error', align=Align.INLINE)
d.comment(0x8706, 'Skip spaces', align=Align.INLINE)
d.comment(0x8709, "')'?", align=Align.INLINE)
d.comment(0x870b, 'yes: process', align=Align.INLINE)
d.comment(0x871a, 'Skip spaces', align=Align.INLINE)
d.comment(0x871d, "','?", align=Align.INLINE)
d.comment(0x871f, 'no: process as absolute', align=Align.INLINE)
d.comment(0x8724, 'Skip spaces', align=Align.INLINE)
d.comment(0x8727, "'X'?", align=Align.INLINE)
d.comment(0x8729, 'yes: abs,X', align=Align.INLINE)
d.comment(0x872b, "'Y'?", align=Align.INLINE)
d.comment(0x872d, 'no: Index error', align=Align.INLINE)
d.comment(0x8747, 'Skip spaces', align=Align.INLINE)
d.comment(0x874a, "'A' (accumulator)?", align=Align.INLINE)
d.comment(0x874c, 'yes', align=Align.INLINE)
d.comment(0x8753, 'Skip spaces', align=Align.INLINE)
d.comment(0x8756, "','?", align=Align.INLINE)
d.comment(0x8758, 'no: process', align=Align.INLINE)
d.comment(0x875d, 'Skip spaces', align=Align.INLINE)
d.comment(0x8760, "'X'?", align=Align.INLINE)
d.comment(0x8762, 'yes: address,X', align=Align.INLINE)
d.comment(0x8764, 'Index error', align=Align.INLINE)
d.comment(0x8776, 'Skip spaces', align=Align.INLINE)
d.comment(0x8779, "'#' immediate?", align=Align.INLINE)
d.comment(0x877b, 'no: address', align=Align.INLINE)
d.comment(0x877d, 'immediate', align=Align.INLINE)
d.comment(0x878e, 'Skip spaces', align=Align.INLINE)
d.comment(0x8791, "'(' indirect?", align=Align.INLINE)
d.comment(0x8793, 'yes', align=Align.INLINE)
d.comment(0x87a8, 'Skip spaces', align=Align.INLINE)
d.comment(0x87af, 'Index error', align=Align.INLINE)
d.comment(0x87bc, 'Save the register', align=Align.INLINE)
d.comment(0x87bf, 'two-register form?', align=Align.INLINE)
d.comment(0x87c8, 'discard the register', align=Align.INLINE)
d.comment(0x87c9, 'do immediate', align=Align.INLINE)
d.comment(0x87db, 'process as absolute', align=Align.INLINE)
d.comment(0x87e5, 'register mismatch?', align=Align.INLINE)
d.comment(0x880d, 'Byte error', align=Align.INLINE)
d.comment(0x8818, 'OPT value', align=Align.INLINE)
d.comment(0x8846, 'two bytes', align=Align.INLINE)
d.comment(0x8855, 'Mistake (syntax) error', align=Align.INLINE)
d.comment(0x8872, 'recover the byte count', align=Align.INLINE)
d.comment(0x888b, 'store the inserted byte', align=Align.INLINE)

# Scattered tails.
d.comment(0x8ada, 'Check the statement ends', align=Align.INLINE)
d.comment(0x8b38, 'Skip spaces', align=Align.INLINE)
d.comment(0x8b3d, 'command token: dispatch it', align=Align.INLINE)
d.comment(0x8b59, 'No FN error', align=Align.INLINE)
d.comment(0x8b96, 'Back up', align=Align.INLINE)
d.comment(0x8b98, 'check the statement ends', align=Align.INLINE)
d.comment(0x8c0e, 'Type mismatch error', align=Align.INLINE)
d.comment(0x908d, "This line's number", align=Align.INLINE)
d.comment(0x908e, '...', align=Align.INLINE)
d.comment(0x9090, '...', align=Align.INLINE)
d.comment(0x9092, '...', align=Align.INLINE)
d.comment(0x9093, '...', align=Align.INLINE)
d.comment(0x9095, '...', align=Align.INLINE)
d.comment(0x9097, 'print it', align=Align.INLINE)
d.comment(0x909a, 'newline', align=Align.INLINE)
d.comment(0x909d, 'loop', align=Align.INLINE)
d.comment(0x9121, 'sync the pointer', align=Align.INLINE)
d.comment(0x9124, 'continue', align=Align.INLINE)
d.comment(0x9127, 'Bad DIM error', align=Align.INLINE)
d.comment(0x942f, 'Next character', align=Align.INLINE)
d.comment(0x9456, 'Send the low byte to OSWRCH', align=Align.INLINE)
d.comment(0x9458, '...', align=Align.INLINE)
d.comment(0x97dd, 'Advance', align=Align.INLINE)
d.comment(0x992d, '...', align=Align.INLINE)
d.comment(0x99a7, 'Division by zero error', align=Align.INLINE)
d.comment(0x9ae7, 'String compare: stack the left', align=Align.INLINE)
d.comment(0x9aea, 'evaluate the right operand', align=Align.INLINE)
d.comment(0x9aed, 'type', align=Align.INLINE)
d.comment(0x9aee, 'number: Type mismatch', align=Align.INLINE)
d.comment(0x9af0, 'Save the current pointer', align=Align.INLINE)
d.comment(0x9af2, 'current length', align=Align.INLINE)
d.comment(0x9af4, 'from 0', align=Align.INLINE)
d.comment(0x9af6, 'stacked length', align=Align.INLINE)
d.comment(0x9af8, 'save it', align=Align.INLINE)
d.comment(0x9afa, 'compare lengths', align=Align.INLINE)
d.comment(0x9afc, 'use the shorter', align=Align.INLINE)
d.comment(0x9afe, '...', align=Align.INLINE)
d.comment(0x9aff, 'shorter length', align=Align.INLINE)
d.comment(0x9b01, 'compare from 0', align=Align.INLINE)
d.comment(0x9c03, 'String too long error', align=Align.INLINE)
d.comment(0x9ec8, 'positive?', align=Align.INLINE)
d.comment(0x9eca, "negative: output '-'", align=Align.INLINE)
d.comment(0x9ecc, '...', align=Align.INLINE)
d.comment(0x9ece, '...', align=Align.INLINE)
d.comment(0x9ed1, 'Exponent', align=Align.INLINE)
d.comment(0x9ed3, '>= 1?', align=Align.INLINE)
d.comment(0x9ed5, 'yes: output the integer part', align=Align.INLINE)
d.comment(0x9ed7, '< 1: multiply by 10', align=Align.INLINE)
d.comment(0x9eda, 'decrement the decimal exponent', align=Align.INLINE)
d.comment(0x9edc, 'loop', align=Align.INLINE)
d.comment(0xa485, 'Return', align=Align.INLINE)
d.comment(0xab32, 'Return', align=Align.INLINE)
d.comment(0xab6a, 'return as an integer', align=Align.INLINE)
d.comment(0xac2f, 'Evaluate the argument', align=Align.INLINE)
d.comment(0xac32, 'not a string: error', align=Align.INLINE)
d.comment(0xac9b, 'Type mismatch error', align=Align.INLINE)
d.comment(0xad67, 'Type mismatch error', align=Align.INLINE)
d.comment(0xae2f, 'Return', align=Align.INLINE)
d.comment(0xae40, 'return as a 16-bit integer', align=Align.INLINE)
d.comment(0xb0b8, 'Return', align=Align.INLINE)
d.comment(0xb4ae, 'Type mismatch error', align=Align.INLINE)
d.comment(0xb4b1, 'Evaluate the value', align=Align.INLINE)
d.comment(0xb4df, 'Return', align=Align.INLINE)
d.comment(0xb4e0, 'Value type', align=Align.INLINE)
d.comment(0xb4e2, 'string: Type mismatch', align=Align.INLINE)
d.comment(0xb4e4, 'real: store it', align=Align.INLINE)
d.comment(0xb4e6, 'integer: convert to real', align=Align.INLINE)
d.comment(0xb4e9, 'Store the 5-byte real: exponent', align=Align.INLINE)
d.comment(0xb4eb, '...', align=Align.INLINE)
d.comment(0xb4ed, '...', align=Align.INLINE)
d.comment(0xb4ef, '...', align=Align.INLINE)
d.comment(0xb4f0, 'Pack the sign into the mantissa', align=Align.INLINE)
d.comment(0xb4f2, '...', align=Align.INLINE)
d.comment(0xb4f4, '...', align=Align.INLINE)
d.comment(0xb4f6, '...', align=Align.INLINE)
d.comment(0xb4f8, '...', align=Align.INLINE)
d.comment(0xb4fa, '...', align=Align.INLINE)
d.comment(0xb4fc, '...', align=Align.INLINE)
d.comment(0xb4fe, 'mantissa 2', align=Align.INLINE)
d.comment(0xb4ff, '...', align=Align.INLINE)
d.comment(0xb501, '...', align=Align.INLINE)
d.comment(0xb503, 'mantissa 3', align=Align.INLINE)
d.comment(0xb504, '...', align=Align.INLINE)
d.comment(0xb506, '...', align=Align.INLINE)
d.comment(0xb508, 'mantissa 4', align=Align.INLINE)
d.comment(0xb509, '...', align=Align.INLINE)
d.comment(0xb50b, '...', align=Align.INLINE)
d.comment(0xb50d, 'Return', align=Align.INLINE)
d.comment(0xb68e, 'No FN error', align=Align.INLINE)
d.comment(0xb9b5, 'No such line error', align=Align.INLINE)
d.comment(0xb9c4, 'Type mismatch error', align=Align.INLINE)
d.comment(0xb9c7, 'Mistake error', align=Align.INLINE)
d.comment(0xb9ca, 'Sync the pointer', align=Align.INLINE)
d.comment(0xb9cc, 'check the statement ends', align=Align.INLINE)
d.comment(0xbd10, 'Return', align=Align.INLINE)

# ----------------------------------------------------------------------
# stmt_input (&BA44): the INPUT statement.
# Handles INPUT, INPUT LINE and INPUT#. Prints any prompt items, reads a
# line from the keyboard, then for each variable extracts the next
# comma-separated field and assigns it (the whole line in LINE mode).
# &4D holds flags (bit6 = LINE, bit7 = item-seen), &4E the prompt flag.
# ----------------------------------------------------------------------
d.comment(0xba44, 'Next non-space character', align=Align.INLINE)
d.comment(0xba47, "'#': INPUT# from a file", align=Align.INLINE)
d.comment(0xba49, '...', align=Align.INLINE)
d.comment(0xba4b, 'LINE token?', align=Align.INLINE)
d.comment(0xba4d, 'yes: LINE mode (carry set)', align=Align.INLINE)
d.comment(0xba4f, 'no: step back, carry clear', align=Align.INLINE)
d.comment(0xba51, '...', align=Align.INLINE)
d.comment(0xba52, 'Record the LINE flag in bit 6', align=Align.INLINE)
d.comment(0xba54, '...', align=Align.INLINE)
d.comment(0xba56, 'Prompt flag = -1', align=Align.INLINE)
d.comment(0xba58, '...', align=Align.INLINE)
d.comment(0xba5a, 'Process a prompt item', align=Align.INLINE)
d.comment(0xba5d, 'none found: parse a variable', align=Align.INLINE)
d.comment(0xba5f, 'Process further prompt items', align=Align.INLINE)
d.comment(0xba62, '...', align=Align.INLINE)
d.comment(0xba64, 'A printed item suppresses the ? prompt', align=Align.INLINE)
d.comment(0xba66, '...', align=Align.INLINE)
d.comment(0xba68, '...', align=Align.INLINE)
d.comment(0xba69, 'Preserve the item-seen flag', align=Align.INLINE)
d.comment(0xba6a, '...', align=Align.INLINE)
d.comment(0xba6c, '...', align=Align.INLINE)
d.comment(0xba6d, '...', align=Align.INLINE)
d.comment(0xba6f, "','  next item?", align=Align.INLINE)
d.comment(0xba71, 'yes', align=Align.INLINE)
d.comment(0xba73, "';'  next item?", align=Align.INLINE)
d.comment(0xba75, 'yes', align=Align.INLINE)
d.comment(0xba77, 'Back up to the variable', align=Align.INLINE)
d.comment(0xba79, 'Save the flags...', align=Align.INLINE)
d.comment(0xba7b, '...', align=Align.INLINE)
d.comment(0xba7c, '...', align=Align.INLINE)
d.comment(0xba7e, '...', align=Align.INLINE)
d.comment(0xba7f, 'Parse the target variable', align=Align.INLINE)
d.comment(0xba82, 'end of statement: done', align=Align.INLINE)
d.comment(0xba84, 'Restore the flags', align=Align.INLINE)
d.comment(0xba85, '...', align=Align.INLINE)
d.comment(0xba87, '...', align=Align.INLINE)
d.comment(0xba88, '...', align=Align.INLINE)
d.comment(0xba8a, 'Update the program pointer', align=Align.INLINE)
d.comment(0xba8c, '...', align=Align.INLINE)
d.comment(0xba8e, 'Save the LINE flag', align=Align.INLINE)
d.comment(0xba8f, 'Still reading the current input line?', align=Align.INLINE)
d.comment(0xba91, 'yes: no new prompt', align=Align.INLINE)
d.comment(0xba93, 'Prompt flag', align=Align.INLINE)
d.comment(0xba95, 'item already printed?', align=Align.INLINE)
d.comment(0xba97, 'yes: read without a ? prompt', align=Align.INLINE)
d.comment(0xba99, 'LINE mode?', align=Align.INLINE)
d.comment(0xba9b, 'yes: no ? prompt', align=Align.INLINE)
d.comment(0xba9d, "Print '?'", align=Align.INLINE)
d.comment(0xba9f, '...', align=Align.INLINE)
d.comment(0xbaa2, 'Read an input line', align=Align.INLINE)
d.comment(0xbaa5, 'Store its length', align=Align.INLINE)
d.comment(0xbaa7, 'Mark the input line as fresh', align=Align.INLINE)
d.comment(0xbaa9, '...', align=Align.INLINE)
d.comment(0xbaaa, '...', align=Align.INLINE)
d.comment(0xbaac, 'LINE mode?', align=Align.INLINE)
d.comment(0xbaae, 'yes: take the whole line', align=Align.INLINE)
d.comment(0xbab0, 'Set the read offset', align=Align.INLINE)
d.comment(0xbab2, 'Point at the input buffer (&0600)', align=Align.INLINE)
d.comment(0xbab4, '...', align=Align.INLINE)
d.comment(0xbab6, '...', align=Align.INLINE)
d.comment(0xbab8, '...', align=Align.INLINE)
d.comment(0xbaba, 'Read the field literal', align=Align.INLINE)
d.comment(0xbabd, 'Skip spaces', align=Align.INLINE)
d.comment(0xbac0, "','  field delimiter?", align=Align.INLINE)
d.comment(0xbac2, 'yes', align=Align.INLINE)
d.comment(0xbac4, 'end of line?', align=Align.INLINE)
d.comment(0xbac6, 'no: keep scanning', align=Align.INLINE)
d.comment(0xbac8, 'mark end of input', align=Align.INLINE)
d.comment(0xbaca, 'Note the next field offset', align=Align.INLINE)
d.comment(0xbacb, '...', align=Align.INLINE)
d.comment(0xbacd, 'Recover the LINE flag', align=Align.INLINE)
d.comment(0xbace, 'LINE mode: assign the whole line', align=Align.INLINE)
d.comment(0xbad0, 'Stack the variable address', align=Align.INLINE)
d.comment(0xbad3, 'Parse the field as a number', align=Align.INLINE)
d.comment(0xbad6, 'assign it', align=Align.INLINE)
d.comment(0xbad9, 'next variable', align=Align.INLINE)
d.comment(0xbadc, 'LINE: string type', align=Align.INLINE)
d.comment(0xbade, '...', align=Align.INLINE)
d.comment(0xbae0, 'assign the line as a string', align=Align.INLINE)
d.comment(0xbae3, 'next variable', align=Align.INLINE)

# ----------------------------------------------------------------------
# stmt_read (&BB1F): the READ statement.
# For each variable, advances the DATA pointer to the next item and
# assigns it (number or string), then records the new DATA position.
# ----------------------------------------------------------------------
d.comment(0xbb1f, 'Parse the target variable', align=Align.INLINE)
d.comment(0xbb22, 'end of statement: done', align=Align.INLINE)
d.comment(0xbb24, 'string variable?', align=Align.INLINE)
d.comment(0xbb26, 'Numeric: find the next DATA item', align=Align.INLINE)
d.comment(0xbb29, 'Stack the variable address', align=Align.INLINE)
d.comment(0xbb2c, 'read the value and assign it', align=Align.INLINE)
d.comment(0xbb2f, 'update the DATA pointer', align=Align.INLINE)
d.comment(0xbb32, 'String: find the next DATA item', align=Align.INLINE)
d.comment(0xbb35, 'Stack the variable address', align=Align.INLINE)
d.comment(0xbb38, 'read the DATA item as a string', align=Align.INLINE)
d.comment(0xbb3b, 'string type', align=Align.INLINE)
d.comment(0xbb3d, 'assign it', align=Align.INLINE)
d.comment(0xbb40, 'Advance the DATA pointer past the item', align=Align.INLINE)
d.comment(0xbb41, '...', align=Align.INLINE)
d.comment(0xbb43, '...', align=Align.INLINE)
d.comment(0xbb45, '...', align=Align.INLINE)
d.comment(0xbb47, '...', align=Align.INLINE)
d.comment(0xbb49, '...', align=Align.INLINE)
d.comment(0xbb4b, '...', align=Align.INLINE)
d.comment(0xbb4d, 'next variable', align=Align.INLINE)

# next_data_item (&BB50): step the DATA pointer to the next value.
d.comment(0xbb50, 'Save the program pointer', align=Align.INLINE)
d.comment(0xbb52, '...', align=Align.INLINE)
d.comment(0xbb54, 'Point at the DATA position', align=Align.INLINE)
d.comment(0xbb56, '...', align=Align.INLINE)
d.comment(0xbb58, '...', align=Align.INLINE)
d.comment(0xbb5a, '...', align=Align.INLINE)
d.comment(0xbb5c, 'From offset 0', align=Align.INLINE)
d.comment(0xbb5e, '...', align=Align.INLINE)
d.comment(0xbb60, 'Next character', align=Align.INLINE)
d.comment(0xbb63, "','  item separator?", align=Align.INLINE)
d.comment(0xbb65, 'yes: at the next item', align=Align.INLINE)
d.comment(0xbb67, 'DATA token?', align=Align.INLINE)
d.comment(0xbb69, 'yes: at the first item', align=Align.INLINE)
d.comment(0xbb6b, 'end of line?', align=Align.INLINE)
d.comment(0xbb6d, 'yes: find the next DATA line', align=Align.INLINE)
d.comment(0xbb6f, 'Scan to the item end: next character', align=Align.INLINE)
d.comment(0xbb72, "','  separator?", align=Align.INLINE)
d.comment(0xbb74, 'yes', align=Align.INLINE)
d.comment(0xbb76, 'end of line?', align=Align.INLINE)
d.comment(0xbb78, 'no: keep scanning', align=Align.INLINE)
d.comment(0xbb7a, 'Line marker', align=Align.INLINE)
d.comment(0xbb7c, '...', align=Align.INLINE)
d.comment(0xbb7e, 'end of program: Out of DATA', align=Align.INLINE)
d.comment(0xbb80, 'Skip the line number', align=Align.INLINE)
d.comment(0xbb81, '...', align=Align.INLINE)
d.comment(0xbb82, 'Line length', align=Align.INLINE)
d.comment(0xbb84, '...', align=Align.INLINE)
d.comment(0xbb85, 'Next character', align=Align.INLINE)
d.comment(0xbb86, '...', align=Align.INLINE)
d.comment(0xbb88, 'space?', align=Align.INLINE)
d.comment(0xbb8a, 'skip leading spaces', align=Align.INLINE)
d.comment(0xbb8c, 'DATA token?', align=Align.INLINE)
d.comment(0xbb8e, 'yes: use this line', align=Align.INLINE)
d.comment(0xbb90, 'Advance to the next line', align=Align.INLINE)
d.comment(0xbb91, '...', align=Align.INLINE)
d.comment(0xbb92, '...', align=Align.INLINE)
d.comment(0xbb94, '...', align=Align.INLINE)
d.comment(0xbb96, '...', align=Align.INLINE)
d.comment(0xbb98, '...', align=Align.INLINE)
d.comment(0xbb9a, 'continue', align=Align.INLINE)
d.comment(0xbb9c, 'Out of DATA error', align=Align.INLINE)
d.comment(0xbba6, 'No REPEAT error', align=Align.INLINE)
d.comment(0xbbad, 'Step past the DATA token', align=Align.INLINE)
d.comment(0xbbae, 'record the offset', align=Align.INLINE)
d.comment(0xbbb0, 'Return', align=Align.INLINE)

# ----------------------------------------------------------------------
# stmt_list (&B59C): the LIST statement.
# Parses an optional line range (default 0..32767), finds the first
# line, and for each line up to the end prints the line number and
# de-tokenises the body, tracking quote state and LISTO indentation
# (&3B/&3C, adjusted by structure keywords).
# ----------------------------------------------------------------------
d.comment(0xb59c, 'Peek at the next character', align=Align.INLINE)
d.comment(0xb59d, '...', align=Align.INLINE)
d.comment(0xb59f, "'O' (LISTO)?", align=Align.INLINE)
d.comment(0xb5a1, 'yes: set the option', align=Align.INLINE)
d.comment(0xb5a3, 'Clear the indent levels', align=Align.INLINE)
d.comment(0xb5a5, '...', align=Align.INLINE)
d.comment(0xb5a7, '...', align=Align.INLINE)
d.comment(0xb5a9, 'Start line default 0', align=Align.INLINE)
d.comment(0xb5ac, 'Embedded start line number?', align=Align.INLINE)
d.comment(0xb5af, 'remember whether one was given', align=Align.INLINE)
d.comment(0xb5b0, 'Stack the start line', align=Align.INLINE)
d.comment(0xb5b3, 'End line default 32767', align=Align.INLINE)
d.comment(0xb5b5, '...', align=Align.INLINE)
d.comment(0xb5b7, '...', align=Align.INLINE)
d.comment(0xb5b9, '...', align=Align.INLINE)
d.comment(0xb5bb, 'Was a start line given?', align=Align.INLINE)
d.comment(0xb5bc, 'no: check for a range comma', align=Align.INLINE)
d.comment(0xb5be, 'Skip spaces', align=Align.INLINE)
d.comment(0xb5c1, "','  range separator?", align=Align.INLINE)
d.comment(0xb5c3, 'yes: read the end line', align=Align.INLINE)
d.comment(0xb5c5, 'Single line: end = start', align=Align.INLINE)
d.comment(0xb5c8, '...', align=Align.INLINE)
d.comment(0xb5cb, 'back up', align=Align.INLINE)
d.comment(0xb5cd, '...', align=Align.INLINE)
d.comment(0xb5cf, 'Skip spaces', align=Align.INLINE)
d.comment(0xb5d2, "','  range separator?", align=Align.INLINE)
d.comment(0xb5d4, 'yes', align=Align.INLINE)
d.comment(0xb5d6, 'back up', align=Align.INLINE)
d.comment(0xb5d8, 'Read the end line number', align=Align.INLINE)
d.comment(0xb5db, 'Save the end line', align=Align.INLINE)
d.comment(0xb5dd, '...', align=Align.INLINE)
d.comment(0xb5df, '...', align=Align.INLINE)
d.comment(0xb5e1, '...', align=Align.INLINE)
d.comment(0xb5e3, 'Check the statement ends', align=Align.INLINE)
d.comment(0xb5e6, 'Check a program is present', align=Align.INLINE)
d.comment(0xb5e9, 'Recover the start line', align=Align.INLINE)
d.comment(0xb5ec, 'Find the first line', align=Align.INLINE)
d.comment(0xb5ef, 'Point at it', align=Align.INLINE)
d.comment(0xb5f1, '...', align=Align.INLINE)
d.comment(0xb5f3, '...', align=Align.INLINE)
d.comment(0xb5f5, '...', align=Align.INLINE)
d.comment(0xb5f7, 'exact line: start here', align=Align.INLINE)
d.comment(0xb5f9, '...', align=Align.INLINE)
d.comment(0xb5fa, '...', align=Align.INLINE)
d.comment(0xb5fc, 'Newline after the previous line', align=Align.INLINE)
d.comment(0xb5ff, 'check Escape', align=Align.INLINE)
d.comment(0xb602, "This line's number: high byte", align=Align.INLINE)
d.comment(0xb604, '...', align=Align.INLINE)
d.comment(0xb606, '...', align=Align.INLINE)
d.comment(0xb607, '...low byte', align=Align.INLINE)
d.comment(0xb609, '...', align=Align.INLINE)
d.comment(0xb60b, 'skip the length byte', align=Align.INLINE)
d.comment(0xb60c, '...', align=Align.INLINE)
d.comment(0xb60d, '...', align=Align.INLINE)
d.comment(0xb60f, 'Past the end line?', align=Align.INLINE)
d.comment(0xb611, '...', align=Align.INLINE)
d.comment(0xb612, '...', align=Align.INLINE)
d.comment(0xb614, '...', align=Align.INLINE)
d.comment(0xb616, '...', align=Align.INLINE)
d.comment(0xb618, 'no: list this line', align=Align.INLINE)
d.comment(0xb61a, 'yes: done', align=Align.INLINE)
d.comment(0xb61d, 'Print the line number', align=Align.INLINE)
d.comment(0xb620, 'Reset the quote flag', align=Align.INLINE)
d.comment(0xb622, '...', align=Align.INLINE)
d.comment(0xb624, 'Print the LISTO leading space', align=Align.INLINE)
d.comment(0xb626, '...', align=Align.INLINE)
d.comment(0xb629, 'FOR/REPEAT indent', align=Align.INLINE)
d.comment(0xb62b, 'LISTO bit 1 indent', align=Align.INLINE)
d.comment(0xb62d, '...', align=Align.INLINE)
d.comment(0xb630, 'second indent level', align=Align.INLINE)
d.comment(0xb632, 'LISTO bit 2 indent', align=Align.INLINE)
d.comment(0xb634, '...', align=Align.INLINE)
d.comment(0xb637, 'Line offset', align=Align.INLINE)
d.comment(0xb639, 'Next character', align=Align.INLINE)
d.comment(0xb63b, 'end of line?', align=Align.INLINE)
d.comment(0xb63d, 'yes: next line', align=Align.INLINE)
d.comment(0xb63f, 'quote?', align=Align.INLINE)
d.comment(0xb641, 'no: a token or literal', align=Align.INLINE)
d.comment(0xb643, 'toggle the quote flag', align=Align.INLINE)
d.comment(0xb645, '...', align=Align.INLINE)
d.comment(0xb647, '...', align=Align.INLINE)
d.comment(0xb649, 'print the quote', align=Align.INLINE)
d.comment(0xb64b, '...', align=Align.INLINE)
d.comment(0xb64e, 'next character', align=Align.INLINE)
d.comment(0xb64f, '...', align=Align.INLINE)
d.comment(0xb651, 'Inside a quoted string?', align=Align.INLINE)
d.comment(0xb653, 'yes: print literally', align=Align.INLINE)
d.comment(0xb655, 'line-number token?', align=Align.INLINE)
d.comment(0xb657, 'no', align=Align.INLINE)
d.comment(0xb659, 'decode the embedded line number', align=Align.INLINE)
d.comment(0xb65c, '...', align=Align.INLINE)
d.comment(0xb65e, 'no field padding', align=Align.INLINE)
d.comment(0xb660, '...', align=Align.INLINE)
d.comment(0xb662, 'print it', align=Align.INLINE)
d.comment(0xb665, 'continue', align=Align.INLINE)
d.comment(0xb668, 'FOR token?', align=Align.INLINE)
d.comment(0xb66a, 'no', align=Align.INLINE)
d.comment(0xb66c, 'increase the indent', align=Align.INLINE)
d.comment(0xb66e, 'NEXT token?', align=Align.INLINE)
d.comment(0xb670, 'no', align=Align.INLINE)
d.comment(0xb672, 'indent active?', align=Align.INLINE)
d.comment(0xb674, 'no', align=Align.INLINE)
d.comment(0xb676, 'decrease the indent', align=Align.INLINE)
d.comment(0xb678, 'REPEAT token?', align=Align.INLINE)
d.comment(0xb67a, 'no', align=Align.INLINE)
d.comment(0xb67c, 'increase the indent', align=Align.INLINE)
d.comment(0xb67e, 'UNTIL token?', align=Align.INLINE)
d.comment(0xb680, 'no', align=Align.INLINE)
d.comment(0xb682, 'indent active?', align=Align.INLINE)
d.comment(0xb684, 'no', align=Align.INLINE)
d.comment(0xb686, 'decrease the indent', align=Align.INLINE)
d.comment(0xb688, 'De-tokenise and print the character', align=Align.INLINE)
d.comment(0xb68b, 'next', align=Align.INLINE)
d.comment(0xb68c, 'loop', align=Align.INLINE)

# eval_mul_div (&9DD1): Level 3 - * / DIV MOD
d.comment(0x9dd1, 'Evaluate the higher level (^, level 2) operand', align=Align.INLINE)
d.comment(0x9dd4, 'next operator "*"?', align=Align.INLINE)
d.comment(0x9dd6, 'yes: multiply', align=Align.INLINE)
d.comment(0x9dd8, '"/"?', align=Align.INLINE)
d.comment(0x9dda, 'yes: divide', align=Align.INLINE)
d.comment(0x9ddc, 'MOD token?', align=Align.INLINE)
d.comment(0x9dde, 'yes: integer remainder', align=Align.INLINE)
d.comment(0x9de0, 'DIV token?', align=Align.INLINE)
d.comment(0x9de2, 'yes: integer divide', align=Align.INLINE)
d.comment(0x9de4, 'no operator: return', align=Align.INLINE)
d.comment(0x9de5, 'Divide: ensure the left operand is real', align=Align.INLINE)
d.comment(0x9de6, '...', align=Align.INLINE)
d.comment(0x9de9, 'stack it', align=Align.INLINE)
d.comment(0x9dec, 'evaluate the right operand', align=Align.INLINE)
d.comment(0x9def, 'remember the operator', align=Align.INLINE)
d.comment(0x9df1, 'ensure the right operand is real', align=Align.INLINE)
d.comment(0x9df2, '...', align=Align.INLINE)
d.comment(0x9df5, 'pop the left operand as the fp operand', align=Align.INLINE)
d.comment(0x9df8, 'FWA = left / right', align=Align.INLINE)
d.comment(0x9dfb, 'restore the operator', align=Align.INLINE)
d.comment(0x9dfd, 'real result', align=Align.INLINE)
d.comment(0x9dff, 'loop for further * / DIV MOD', align=Align.INLINE)

# stack_local (&B30D): save a variable's value and identity for LOCAL
d.comment(0xb30d, 'Variable type', align=Align.INLINE)
d.comment(0xb30f, 'an integer?', align=Align.INLINE)
d.comment(0xb311, 'no', align=Align.INLINE)
d.comment(0xb313, 'integer: address its 4 bytes via &37', align=Align.INLINE)
d.comment(0xb315, '...', align=Align.INLINE)
d.comment(0xb318, "Load the variable's current value by type", align=Align.INLINE)
d.comment(0xb31b, 'save the type flags', align=Align.INLINE)
d.comment(0xb31c, 'push the value onto the stack', align=Align.INLINE)
d.comment(0xb31f, 'restore the type', align=Align.INLINE)
d.comment(0xb320, 'byte/string', align=Align.INLINE)
d.comment(0xb322, '...', align=Align.INLINE)
d.comment(0xb324, 'integer: reload', align=Align.INLINE)
d.comment(0xb326, '...', align=Align.INLINE)
d.comment(0xb329, 'push the variable identity (as an integer)', align=Align.INLINE)
d.comment(0xb32c, 'Load the variable by type:', align=Align.INLINE)
d.comment(0xb32e, 'string', align=Align.INLINE)
d.comment(0xb330, 'byte', align=Align.INLINE)
d.comment(0xb332, 'real?', align=Align.INLINE)
d.comment(0xb334, 'real (else integer)', align=Align.INLINE)

# stmt_call (&8ED2): CALL address [,params...]
d.comment(0x8ed2, 'Evaluate the call address', align=Align.INLINE)
d.comment(0x8ed5, 'coerce to an integer', align=Align.INLINE)
d.comment(0x8ed8, 'stack the address', align=Align.INLINE)
d.comment(0x8edb, 'Build the parameter block at &0600:', align=Align.INLINE)
d.comment(0x8edd, 'zero the parameter count', align=Align.INLINE)
d.comment(0x8ee0, '...', align=Align.INLINE)
d.comment(0x8ee3, 'next parameter?', align=Align.INLINE)
d.comment(0x8ee6, 'a comma?', align=Align.INLINE)
d.comment(0x8ee8, 'no: end of the parameters', align=Align.INLINE)
d.comment(0x8eea, 'parse the parameter (a variable)', align=Align.INLINE)
d.comment(0x8eec, '...', align=Align.INLINE)
d.comment(0x8eef, 'bad parameter: error', align=Align.INLINE)
d.comment(0x8ef1, 'append its address to the block:', align=Align.INLINE)
d.comment(0x8ef4, '...', align=Align.INLINE)
d.comment(0x8ef5, 'address low', align=Align.INLINE)
d.comment(0x8ef7, '...', align=Align.INLINE)
d.comment(0x8efa, '...', align=Align.INLINE)
d.comment(0x8efb, 'address high', align=Align.INLINE)
d.comment(0x8efd, '...', align=Align.INLINE)
d.comment(0x8f00, '...', align=Align.INLINE)
d.comment(0x8f01, 'type', align=Align.INLINE)
d.comment(0x8f03, '...', align=Align.INLINE)
d.comment(0x8f06, 'one more parameter', align=Align.INLINE)
d.comment(0x8f09, 'next parameter', align=Align.INLINE)
d.comment(0x8f0c, 'Check for end of statement', align=Align.INLINE)
d.comment(0x8f0e, '...', align=Align.INLINE)
d.comment(0x8f11, 'pop the address into IWA', align=Align.INLINE)
d.comment(0x8f14, 'set up registers and call the code', align=Align.INLINE)
d.comment(0x8f17, 'clear decimal mode on return', align=Align.INLINE)
d.comment(0x8f18, 'Back to execution', align=Align.INLINE)
d.comment(0x8f1b, 'parameter error (shared)', align=Align.INLINE)

# fwa_acc_fwb (&A178): FWA mantissa += FWB mantissa
d.comment(0xa178, 'Add the mantissas: rounding byte', align=Align.INLINE)
d.comment(0xa17a, '+ FWB rounding', align=Align.INLINE)
d.comment(0xa17c, '(store)', align=Align.INLINE)
d.comment(0xa17e, 'm4', align=Align.INLINE)
d.comment(0xa180, '+ FWB m4', align=Align.INLINE)
d.comment(0xa182, '(store)', align=Align.INLINE)
d.comment(0xa184, 'm3', align=Align.INLINE)
d.comment(0xa186, '- FWB m3', align=Align.INLINE)
d.comment(0xa188, '(store)', align=Align.INLINE)
d.comment(0xa18a, 'm2', align=Align.INLINE)
d.comment(0xa18c, '- FWB m2', align=Align.INLINE)
d.comment(0xa18e, '(store)', align=Align.INLINE)
d.comment(0xa190, 'm1', align=Align.INLINE)
d.comment(0xa192, '- FWB m1', align=Align.INLINE)
d.comment(0xa194, '(store)', align=Align.INLINE)
d.comment(0xa196, 'Return (carry = overflow)', align=Align.INLINE)
# mant_mul10 (&A197): x4 + x1 = x5, then x2
d.comment(0xa197, 'Save A', align=Align.INLINE)
d.comment(0xa198, 'keep m4 in X', align=Align.INLINE)
d.comment(0xa19a, 'save the mantissa (m1..m3):', align=Align.INLINE)
d.comment(0xa19c, 'push m1,', align=Align.INLINE)
d.comment(0xa19d, 'm2,', align=Align.INLINE)
d.comment(0xa19f, 'push m2,', align=Align.INLINE)
d.comment(0xa1a0, 'm3,', align=Align.INLINE)
d.comment(0xa1a2, 'push m3 (m4 already in X)', align=Align.INLINE)
d.comment(0xa1a3, 'x2: shift the mantissa left', align=Align.INLINE)
d.comment(0xa1a5, 'shift the low byte left,', align=Align.INLINE)
d.comment(0xa1a6, 'carrying up through m4,', align=Align.INLINE)
d.comment(0xa1a8, 'm3,', align=Align.INLINE)
d.comment(0xa1aa, 'm2,', align=Align.INLINE)
d.comment(0xa1ac, 'm1 (mantissa now x2)', align=Align.INLINE)
d.comment(0xa1ae, 'x2 again (now x4)', align=Align.INLINE)
d.comment(0xa1af, 'm4,', align=Align.INLINE)
d.comment(0xa1b1, 'm3,', align=Align.INLINE)
d.comment(0xa1b3, 'm2,', align=Align.INLINE)
d.comment(0xa1b5, 'm1 (now x4)', align=Align.INLINE)
d.comment(0xa1b7, 'add the saved original (x4 + x1 = x5): rnd', align=Align.INLINE)
d.comment(0xa1b9, '(store)', align=Align.INLINE)
d.comment(0xa1bb, 'm4', align=Align.INLINE)
d.comment(0xa1bc, '+ original m4 (was in X)', align=Align.INLINE)
d.comment(0xa1be, '(store)', align=Align.INLINE)
d.comment(0xa1c0, 'm3', align=Align.INLINE)
d.comment(0xa1c1, '+ original m3 (pulled)', align=Align.INLINE)
d.comment(0xa1c3, '(store)', align=Align.INLINE)
d.comment(0xa1c5, 'm2', align=Align.INLINE)
d.comment(0xa1c6, '+ original m2 (pulled)', align=Align.INLINE)
d.comment(0xa1c8, '(store)', align=Align.INLINE)
d.comment(0xa1ca, 'm1', align=Align.INLINE)
d.comment(0xa1cb, '+ original m1 -> kept in A', align=Align.INLINE)
d.comment(0xa1cd, 'x2 (now x10): shift left', align=Align.INLINE)
d.comment(0xa1cf, 'carrying up through m4,', align=Align.INLINE)
d.comment(0xa1d1, 'm3,', align=Align.INLINE)
d.comment(0xa1d3, 'm2,', align=Align.INLINE)
d.comment(0xa1d5, 'm1 (still in A): mantissa now x10', align=Align.INLINE)
d.comment(0xa1d6, 'store m1', align=Align.INLINE)
d.comment(0xa1d8, 'restore A', align=Align.INLINE)
d.comment(0xa1d9, 'Return', align=Align.INLINE)

# fwa_rsub_var / fwa_add_fwb / fwa_mul_var / fwa_reciprocal (wrappers)
d.comment(0xa4fd, 'Negate FWA, then add the variable: var - FWA', align=Align.INLINE)
d.comment(0xa505, 'FWA = FWA + FWB (raw)', align=Align.INLINE)
d.comment(0xa508, 'then round', align=Align.INLINE)
d.comment(0xa656, 'FWA = FWA * fp var (raw)', align=Align.INLINE)
d.comment(0xa659, 'normalise (round below)', align=Align.INLINE)
d.comment(0xa6a5, 'Save FWA (the divisor) in TEMP1', align=Align.INLINE)
d.comment(0xa6a8, 'FWA = 1', align=Align.INLINE)
d.comment(0xa6ab, 'divide 1 by the saved value', align=Align.INLINE)

# stmt_bput (&BF58): BPUT#channel, value
d.comment(0xbf58, 'Evaluate the #handle', align=Align.INLINE)
d.comment(0xbf5b, 'save it', align=Align.INLINE)
d.comment(0xbf5c, 'require a comma', align=Align.INLINE)
d.comment(0xbf5f, 'evaluate the value', align=Align.INLINE)
d.comment(0xbf62, 'coerce to an integer', align=Align.INLINE)
d.comment(0xbf65, 'recover the handle', align=Align.INLINE)
d.comment(0xbf66, 'Y = handle', align=Align.INLINE)
d.comment(0xbf67, 'A = the byte to write', align=Align.INLINE)
d.comment(0xbf69, 'OSBPUT: write the byte', align=Align.INLINE)
d.comment(0xbf6c, 'Back to execution', align=Align.INLINE)

# language_startup (&8023) remaining
d.comment(0x8023, 'OSBYTE &84: read HIMEM', align=Align.INLINE)
d.comment(0x802a, 'HIMEM high byte', align=Align.INLINE)
d.comment(0x802c, 'OSBYTE &83: read OSHWM (PAGE)', align=Align.INLINE)
d.comment(0x8033, 'X = 0', align=Align.INLINE)
d.comment(0x803a, '@% byte 3 = 0', align=Align.INLINE)
d.comment(0x803d, 'X = &FF', align=Align.INLINE)
d.comment(0x8040, '@% = &0000090A: byte 0 = &0A', align=Align.INLINE)
d.comment(0x8045, 'X = &09', align=Align.INLINE)
d.comment(0x8046, '@% byte 1 = &09', align=Align.INLINE)
d.comment(0x8065, '(BRKV low)', align=Align.INLINE)
d.comment(0x8068, 'high byte &B4', align=Align.INLINE)
d.comment(0x806a, '(BRKV high)', align=Align.INLINE)
d.comment(0x806e, 'Enter via NEW and the immediate loop', align=Align.INLINE)
d.subroutine(0xa07b, 'parse_number', title='Parse an unsigned number at PtrB',
             description='Parse a decimal/hex number (integer or real) into the accumulator.')
d.subroutine(0xb3c5, 'find_error_line', title='Find the line an error occurred in',
             description='Walk the program to locate the line containing the current text pointer and set ERL.')

# ascii_to_number (&AC34): convert the SWA string to a value (VAL)
d.comment(0xac34, 'NUL-terminate the SWA string', align=Align.INLINE)
d.comment(0xac36, '...', align=Align.INLINE)
d.comment(0xac38, '...', align=Align.INLINE)
d.comment(0xac3b, 'Save PtrB (we point it at the SWA):', align=Align.INLINE)
d.comment(0xac3d, '...', align=Align.INLINE)
d.comment(0xac3e, '...', align=Align.INLINE)
d.comment(0xac40, '...', align=Align.INLINE)
d.comment(0xac41, '...', align=Align.INLINE)
d.comment(0xac43, '...', align=Align.INLINE)
d.comment(0xac44, 'Point PtrB at the SWA (&0600): offset 0', align=Align.INLINE)
d.comment(0xac46, '...', align=Align.INLINE)
d.comment(0xac48, 'low 0', align=Align.INLINE)
d.comment(0xac4a, '...', align=Align.INLINE)
d.comment(0xac4c, 'high &06', align=Align.INLINE)
d.comment(0xac4e, '...', align=Align.INLINE)
d.comment(0xac50, 'skip spaces', align=Align.INLINE)
d.comment(0xac53, 'minus sign?', align=Align.INLINE)
d.comment(0xac55, 'negative number', align=Align.INLINE)
d.comment(0xac57, 'plus sign?', align=Align.INLINE)
d.comment(0xac59, 'no sign', align=Align.INLINE)
d.comment(0xac5b, 'skip the plus', align=Align.INLINE)
d.comment(0xac5e, 'step back', align=Align.INLINE)
d.comment(0xac60, 'parse the number', align=Align.INLINE)
d.comment(0xac63, 'finish', align=Align.INLINE)
d.comment(0xac66, 'negative: skip the minus', align=Align.INLINE)
d.comment(0xac69, 'step back', align=Align.INLINE)
d.comment(0xac6b, 'parse the number', align=Align.INLINE)
d.comment(0xac6e, 'integer: done', align=Align.INLINE)
d.comment(0xac70, 'real: negate it', align=Align.INLINE)
d.comment(0xac73, 'store the result type', align=Align.INLINE)
d.comment(0xac75, 'restore PtrB and return', align=Align.INLINE)

# fn_chrs (&B3BD): CHR$
d.comment(0xb3bd, 'Evaluate the integer argument', align=Align.INLINE)
d.comment(0xb3c0, 'A = the character code', align=Align.INLINE)
d.comment(0xb3c2, 'return a one-character string', align=Align.INLINE)
# find_error_line (&B3C5)
d.comment(0xb3c5, 'Clear ERL:', align=Align.INLINE)
d.comment(0xb3c7, '...', align=Align.INLINE)
d.comment(0xb3c9, '...', align=Align.INLINE)
d.comment(0xb3cb, 'Scan the program from PAGE: high', align=Align.INLINE)
d.comment(0xb3cd, '...', align=Align.INLINE)
d.comment(0xb3cf, 'low 0', align=Align.INLINE)
d.comment(0xb3d1, 'past the error position?', align=Align.INLINE)
d.comment(0xb3d3, '...', align=Align.INLINE)
d.comment(0xb3d5, 'reached it: done', align=Align.INLINE)
d.comment(0xb3d7, '...', align=Align.INLINE)
d.comment(0xb3d9, 'read a program byte', align=Align.INLINE)
d.comment(0xb3dc, 'a line end (CR)?', align=Align.INLINE)
d.comment(0xb3de, 'no: keep scanning', align=Align.INLINE)
d.comment(0xb3e0, 'is this line past the error?', align=Align.INLINE)
d.comment(0xb3e2, '...', align=Align.INLINE)
d.comment(0xb3e4, '...', align=Align.INLINE)
d.comment(0xb3e6, 'yes: keep the previous line', align=Align.INLINE)
d.comment(0xb3e8, 'read the line number high byte', align=Align.INLINE)
d.comment(0xb3eb, 'end of program?', align=Align.INLINE)
d.comment(0xb3ed, 'yes: done', align=Align.INLINE)
d.comment(0xb3ef, 'record ERL high', align=Align.INLINE)
d.comment(0xb3f1, 'line number low byte', align=Align.INLINE)
d.comment(0xb3f4, 'record ERL low', align=Align.INLINE)
d.comment(0xb3f6, 'skip the line length byte', align=Align.INLINE)
d.comment(0xb3f9, 'still before the error?', align=Align.INLINE)
d.comment(0xb3fb, '...', align=Align.INLINE)
d.comment(0xb3fd, '...', align=Align.INLINE)
d.comment(0xb3ff, 'yes: scan the next line', align=Align.INLINE)
d.comment(0xb401, 'Return', align=Align.INLINE)
# brk_handler (&B402): the BASIC error handler (via BRKV)
d.comment(0xb402, 'Find the line number (set ERL)', align=Align.INLINE)
d.comment(0xb405, 'TRACE off', align=Align.INLINE)
d.comment(0xb407, 'error number', align=Align.INLINE)
d.comment(0xb409, 'non-zero: an ON ERROR handler is active', align=Align.INLINE)
d.comment(0xb40b, 'no handler: reset to the default (ON ERROR OFF)', align=Align.INLINE)
d.comment(0xb40d, '...', align=Align.INLINE)
d.comment(0xb40f, '...', align=Align.INLINE)
d.comment(0xb411, '...', align=Align.INLINE)
d.comment(0xb413, 'Point the program pointer at the handler code: low', align=Align.INLINE)
d.comment(0xb415, '...', align=Align.INLINE)
d.comment(0xb417, 'high', align=Align.INLINE)
d.comment(0xb419, '...', align=Align.INLINE)
d.comment(0xb41b, 'clear DATA and the stacks', align=Align.INLINE)
d.comment(0xb41e, 'offset 0', align=Align.INLINE)
d.comment(0xb41f, '...', align=Align.INLINE)
d.comment(0xb421, 'OSBYTE &DA: flush the VDU queue', align=Align.INLINE)
d.comment(0xb426, 'OSBYTE &7E: acknowledge any Escape', align=Align.INLINE)
d.comment(0xb42b, 'reset the 6502 stack...', align=Align.INLINE)
d.comment(0xb42d, 'OPT = &FF', align=Align.INLINE)
d.comment(0xb42f, '...', align=Align.INLINE)
d.comment(0xb430, 'enter the execution loop at the handler', align=Align.INLINE)
d.subroutine(0xb34f, 'load_byte_var', title='Load a byte variable into IWA')
d.subroutine(0xb354, 'load_real_var', title='Load a real variable into FWA')
d.subroutine(0xb384, 'load_string_var', title='Load a string variable into the buffer')
d.subroutine(0xa2ed, 'small_int_to_fwa', title='Convert a small (8-bit) integer in A to FWA')

# int_to_fwa (&A2BE): IWA -> FWA
d.comment(0xa2be, 'Clear the rounding...', align=Align.INLINE)
d.comment(0xa2c0, '...', align=Align.INLINE)
d.comment(0xa2c2, '...and overflow bytes', align=Align.INLINE)
d.comment(0xa2c4, 'Sign of IWA (top byte)', align=Align.INLINE)
d.comment(0xa2c6, 'positive: sign byte = 0', align=Align.INLINE)
d.comment(0xa2c8, 'negative: make it positive...', align=Align.INLINE)
d.comment(0xa2cb, '...and set the sign byte', align=Align.INLINE)
d.comment(0xa2cd, '(store the sign)', align=Align.INLINE)
d.comment(0xa2cf, 'Copy IWA into the mantissa (MSB first):', align=Align.INLINE)
d.comment(0xa2d1, 'byte 0 -> m4', align=Align.INLINE)
d.comment(0xa2d3, '...', align=Align.INLINE)
d.comment(0xa2d5, 'byte 1 -> m3', align=Align.INLINE)
d.comment(0xa2d7, '...', align=Align.INLINE)
d.comment(0xa2d9, 'byte 2 -> m2', align=Align.INLINE)
d.comment(0xa2db, '...', align=Align.INLINE)
d.comment(0xa2dd, 'byte 3 -> m1 (MSB)', align=Align.INLINE)
d.comment(0xa2df, 'Exponent &A0 (= 32): a 32-bit integer', align=Align.INLINE)
d.comment(0xa2e1, '(store)', align=Align.INLINE)
d.comment(0xa2e3, 'normalise the result', align=Align.INLINE)
d.comment(0xa2e6, 'Zero: clear sign,', align=Align.INLINE)
d.comment(0xa2e8, 'exponent,', align=Align.INLINE)
d.comment(0xa2ea, 'overflow', align=Align.INLINE)
d.comment(0xa2ec, 'Return', align=Align.INLINE)
d.comment(0xa2ed, 'Small int to FWA: save it', align=Align.INLINE)
d.comment(0xa2ee, 'clear FWA', align=Align.INLINE)
d.comment(0xa2f1, 'recover it', align=Align.INLINE)
d.comment(0xa2f2, 'zero: done', align=Align.INLINE)
d.comment(0xa2f4, 'positive', align=Align.INLINE)
d.comment(0xa2f6, 'negative: set the sign...', align=Align.INLINE)
d.comment(0xa2f8, '...', align=Align.INLINE)
d.comment(0xa2fa, '...', align=Align.INLINE)
d.comment(0xa2fb, '...and negate the value', align=Align.INLINE)
d.comment(0xa2fd, 'value into the mantissa MSB', align=Align.INLINE)
d.comment(0xa2ff, 'Exponent &88 (= 8): an 8-bit value', align=Align.INLINE)
d.comment(0xa301, '(store; falls into normalise)', align=Align.INLINE)

# iwa_load_var (&B336) and the byte / real / string loaders
d.comment(0xb336, 'Load a 4-byte integer (MSB first): byte 3', align=Align.INLINE)
d.comment(0xb338, '...', align=Align.INLINE)
d.comment(0xb33a, '(into IWA)', align=Align.INLINE)
d.comment(0xb33c, 'next', align=Align.INLINE)
d.comment(0xb33d, 'byte 2', align=Align.INLINE)
d.comment(0xb33f, '...', align=Align.INLINE)
d.comment(0xb341, 'next', align=Align.INLINE)
d.comment(0xb342, 'byte 1', align=Align.INLINE)
d.comment(0xb344, '(keep in X)', align=Align.INLINE)
d.comment(0xb345, 'next', align=Align.INLINE)
d.comment(0xb346, 'byte 0', align=Align.INLINE)
d.comment(0xb348, '(store last)', align=Align.INLINE)
d.comment(0xb34a, 'byte 1 from X', align=Align.INLINE)
d.comment(0xb34c, 'integer type', align=Align.INLINE)
d.comment(0xb34e, 'Return the integer', align=Align.INLINE)
d.comment(0xb34f, 'Read the byte', align=Align.INLINE)
d.comment(0xb351, 'return as an integer', align=Align.INLINE)
d.comment(0xb354, 'Unpack a 5-byte real into FWA: byte 4...', align=Align.INLINE)
d.comment(0xb355, 'read it', align=Align.INLINE)
d.comment(0xb357, '-> m4', align=Align.INLINE)
d.comment(0xb359, 'next', align=Align.INLINE)
d.comment(0xb35a, 'byte 3...', align=Align.INLINE)
d.comment(0xb35c, '-> m3', align=Align.INLINE)
d.comment(0xb35e, 'next', align=Align.INLINE)
d.comment(0xb35f, 'byte 2...', align=Align.INLINE)
d.comment(0xb361, '-> m2', align=Align.INLINE)
d.comment(0xb363, 'next', align=Align.INLINE)
d.comment(0xb364, 'byte 1 (sign + MSB)...', align=Align.INLINE)
d.comment(0xb366, '-> sign byte', align=Align.INLINE)
d.comment(0xb368, 'next', align=Align.INLINE)
d.comment(0xb369, 'byte 0...', align=Align.INLINE)
d.comment(0xb36b, '-> exponent', align=Align.INLINE)
d.comment(0xb36d, 'clear rounding', align=Align.INLINE)
d.comment(0xb36f, 'clear overflow', align=Align.INLINE)
d.comment(0xb371, 'test for zero...', align=Align.INLINE)
d.comment(0xb373, 'm2,', align=Align.INLINE)
d.comment(0xb375, 'm3,', align=Align.INLINE)
d.comment(0xb377, 'm4', align=Align.INLINE)
d.comment(0xb379, 'zero: leave the MSB clear', align=Align.INLINE)
d.comment(0xb37b, 'restore the implied 1...', align=Align.INLINE)
d.comment(0xb37d, 'set the top bit', align=Align.INLINE)
d.comment(0xb37f, 'store the mantissa MSB', align=Align.INLINE)
d.comment(0xb381, 'real type', align=Align.INLINE)
d.comment(0xb383, 'Return the real', align=Align.INLINE)
d.comment(0xb384, '$-string (absolute address)?', align=Align.INLINE)
d.comment(0xb386, 'yes', align=Align.INLINE)
d.comment(0xb388, 'normal string: length at offset 3', align=Align.INLINE)
d.comment(0xb38a, 'read it', align=Align.INLINE)
d.comment(0xb38c, 'string length', align=Align.INLINE)
d.comment(0xb38e, 'empty: done', align=Align.INLINE)
d.comment(0xb390, 'string pointer high', align=Align.INLINE)
d.comment(0xb392, 'read it', align=Align.INLINE)
d.comment(0xb394, 'into the source pointer (high)', align=Align.INLINE)
d.comment(0xb396, 'low', align=Align.INLINE)
d.comment(0xb397, 'read it', align=Align.INLINE)
d.comment(0xb399, 'and the low byte', align=Align.INLINE)
d.comment(0xb39b, 'copy into the buffer:', align=Align.INLINE)
d.comment(0xb39d, 'char...', align=Align.INLINE)
d.comment(0xb39e, 'read it', align=Align.INLINE)
d.comment(0xb3a0, '-> buffer', align=Align.INLINE)
d.comment(0xb3a3, 'count', align=Align.INLINE)
d.comment(0xb3a4, 'loop', align=Align.INLINE)
d.comment(0xb3a6, 'Return the string', align=Align.INLINE)
d.comment(0xb3a7, '$-string: copy until CR', align=Align.INLINE)
d.comment(0xb3a9, 'null pointer: empty', align=Align.INLINE)
d.comment(0xb3ab, 'from the start', align=Align.INLINE)
d.comment(0xb3ad, 'char...', align=Align.INLINE)
d.comment(0xb3af, '-> buffer', align=Align.INLINE)
d.comment(0xb3b2, 'CR?', align=Align.INLINE)
d.comment(0xb3b4, 'yes: end', align=Align.INLINE)
d.comment(0xb3b6, 'next', align=Align.INLINE)
d.comment(0xb3b7, 'loop', align=Align.INLINE)
d.comment(0xb3b9, 'ran 256 chars without CR: length 0', align=Align.INLINE)
d.comment(0xb3ba, 'set the length', align=Align.INLINE)
d.comment(0xb3bc, 'Return', align=Align.INLINE)

# print_special_item (&8E70): the ' TAB SPC items, and inline strings
d.comment(0x8e70, 'Save PtrA into PtrB: low', align=Align.INLINE)
d.comment(0x8e72, '...', align=Align.INLINE)
d.comment(0x8e74, 'high', align=Align.INLINE)
d.comment(0x8e76, '...', align=Align.INLINE)
d.comment(0x8e78, 'offset', align=Align.INLINE)
d.comment(0x8e7a, '...', align=Align.INLINE)
d.comment(0x8e7c, 'an apostrophe?', align=Align.INLINE)
d.comment(0x8e7e, 'yes: force a newline', align=Align.INLINE)
d.comment(0x8e80, 'TAB token?', align=Align.INLINE)
d.comment(0x8e82, 'yes: handle TAB', align=Align.INLINE)
d.comment(0x8e84, 'SPC token?', align=Align.INLINE)
d.comment(0x8e86, 'yes: handle SPC', align=Align.INLINE)
d.comment(0x8e88, 'none: not consumed (carry set)', align=Align.INLINE)
d.comment(0x8e89, 'Return', align=Align.INLINE)
d.comment(0x8e8a, 'Skip spaces, then handle a special item', align=Align.INLINE)
d.comment(0x8e8d, '...', align=Align.INLINE)
d.comment(0x8e90, 'consumed: done', align=Align.INLINE)
d.comment(0x8e92, 'a string literal (quote)?', align=Align.INLINE)
d.comment(0x8e94, 'yes: print it inline', align=Align.INLINE)
d.comment(0x8e96, 'not consumed', align=Align.INLINE)
d.comment(0x8e97, 'Return', align=Align.INLINE)
d.comment(0x8e98, 'Missing " error block', align=Align.INLINE)
d.comment(0x8ea4, 'print a character', align=Align.INLINE)
d.comment(0x8ea7, 'Print the inline string: advance', align=Align.INLINE)
d.comment(0x8ea8, 'char', align=Align.INLINE)
d.comment(0x8eaa, 'CR (unterminated)?', align=Align.INLINE)
d.comment(0x8eac, 'Missing " error', align=Align.INLINE)
d.comment(0x8eae, 'a quote?', align=Align.INLINE)
d.comment(0x8eb0, 'no: print it', align=Align.INLINE)
d.comment(0x8eb2, 'advance', align=Align.INLINE)
d.comment(0x8eb3, 'update the offset', align=Align.INLINE)
d.comment(0x8eb5, 'doubled ""?', align=Align.INLINE)
d.comment(0x8eb7, '...', align=Align.INLINE)
d.comment(0x8eb9, 'no: end of the string', align=Align.INLINE)
d.comment(0x8ebb, 'yes: print one quote', align=Align.INLINE)

d.subroutine(0xa178, 'fwa_acc_fwb', title='Add FWB into FWA',
             description='FWA = FWA + FWB on the aligned mantissas (used by multiply, *10 and /10).')

# fwa_mul_var_raw (&A606): FWA = FWA * fp variable (shift-and-add)
d.comment(0xa606, 'Is FWA zero?', align=Align.INLINE)
d.comment(0xa609, 'zero: the product is zero', align=Align.INLINE)
d.comment(0xa60b, 'FWB = the fp variable (the multiplier)', align=Align.INLINE)
d.comment(0xa60e, 'non-zero: multiply', align=Align.INLINE)
d.comment(0xa610, 'multiplier zero: the product is zero', align=Align.INLINE)
d.comment(0xa613, 'Add the exponents:', align=Align.INLINE)
d.comment(0xa614, '...', align=Align.INLINE)
d.comment(0xa616, '...', align=Align.INLINE)
d.comment(0xa618, 'no carry', align=Align.INLINE)
d.comment(0xa61a, 'carry into overflow', align=Align.INLINE)
d.comment(0xa61c, '...', align=Align.INLINE)
d.comment(0xa61d, 'remove the excess-128 bias (added twice)', align=Align.INLINE)
d.comment(0xa61f, 'store the product exponent', align=Align.INLINE)
d.comment(0xa621, 'no borrow', align=Align.INLINE)
d.comment(0xa623, 'borrow into overflow', align=Align.INLINE)
d.comment(0xa625, 'Move FWA aside as the multiplicand and clear FWA:', align=Align.INLINE)
d.comment(0xa627, '...', align=Align.INLINE)
d.comment(0xa629, 'copy a FWA byte...', align=Align.INLINE)
d.comment(0xa62b, '...to the multiplicand', align=Align.INLINE)
d.comment(0xa62d, 'clear the FWA byte', align=Align.INLINE)
d.comment(0xa62f, 'count', align=Align.INLINE)
d.comment(0xa630, 'loop', align=Align.INLINE)
d.comment(0xa632, 'Product sign = FWA sign XOR FWB sign:', align=Align.INLINE)
d.comment(0xa634, '...', align=Align.INLINE)
d.comment(0xa636, '(store)', align=Align.INLINE)
d.comment(0xa638, '32 iterations, one per multiplier bit', align=Align.INLINE)
d.comment(0xa63a, 'Shift the multiplier right: next bit into carry', align=Align.INLINE)
d.comment(0xa63c, '...', align=Align.INLINE)
d.comment(0xa63e, '...', align=Align.INLINE)
d.comment(0xa640, '...', align=Align.INLINE)
d.comment(0xa642, '...', align=Align.INLINE)
d.comment(0xa644, 'Shift the running product left (&43-&46):', align=Align.INLINE)
d.comment(0xa646, '...', align=Align.INLINE)
d.comment(0xa648, '...', align=Align.INLINE)
d.comment(0xa64a, '...', align=Align.INLINE)
d.comment(0xa64c, 'multiplier bit clear: skip the add', align=Align.INLINE)
d.comment(0xa64e, 'bit set: add the multiplicand', align=Align.INLINE)
d.comment(0xa64f, 'FWA += FWB', align=Align.INLINE)
d.comment(0xa652, 'count', align=Align.INLINE)
d.comment(0xa653, 'loop', align=Align.INLINE)
d.comment(0xa655, 'Return the product', align=Align.INLINE)

# fwa_add_fwb_raw (&A50B) remaining: alignment shifts and add/subtract
d.comment(0xa510, 'Y = 0 (the byte shifted in)', align=Align.INLINE)
d.comment(0xa512, 'prepare the exponent compare', align=Align.INLINE)
d.comment(0xa513, 'FWA exponent...', align=Align.INLINE)
d.comment(0xa51b, 'differ by >= 37 bits?', align=Align.INLINE)
d.comment(0xa51f, 'save the shift count', align=Align.INLINE)
d.comment(0xa522, 'no whole-byte shift: go to the bit shift', align=Align.INLINE)
d.comment(0xa524, 'shift count / 8...', align=Align.INLINE)
d.comment(0xa525, '...', align=Align.INLINE)
d.comment(0xa526, '= whole-byte shifts', align=Align.INLINE)
d.comment(0xa527, 'X = byte-shift count', align=Align.INLINE)
d.comment(0xa52a, 'shift FWB down a byte: m4 -> rnd', align=Align.INLINE)
d.comment(0xa52c, 'm3...', align=Align.INLINE)
d.comment(0xa52e, '-> m4', align=Align.INLINE)
d.comment(0xa530, 'm2...', align=Align.INLINE)
d.comment(0xa532, '-> m3', align=Align.INLINE)
d.comment(0xa534, 'm1...', align=Align.INLINE)
d.comment(0xa536, '-> m2', align=Align.INLINE)
d.comment(0xa538, 'm1 = 0', align=Align.INLINE)
d.comment(0xa53a, 'count', align=Align.INLINE)
d.comment(0xa53b, 'loop', align=Align.INLINE)
d.comment(0xa53d, 'recover the shift count', align=Align.INLINE)
d.comment(0xa540, 'no bit shift: add the mantissas', align=Align.INLINE)
d.comment(0xa542, 'X = bit-shift count', align=Align.INLINE)
d.comment(0xa543, 'shift FWB right one bit: m1', align=Align.INLINE)
d.comment(0xa545, 'm2', align=Align.INLINE)
d.comment(0xa547, 'm3', align=Align.INLINE)
d.comment(0xa549, 'm4', align=Align.INLINE)
d.comment(0xa54b, 'rnd', align=Align.INLINE)
d.comment(0xa54d, 'count', align=Align.INLINE)
d.comment(0xa54e, 'loop', align=Align.INLINE)
d.comment(0xa550, 'aligned: add the mantissas', align=Align.INLINE)
d.comment(0xa553, 'FWB exponent - FWA exponent', align=Align.INLINE)
d.comment(0xa555, '...', align=Align.INLINE)
d.comment(0xa557, 'differ by >= 37 bits?', align=Align.INLINE)
d.comment(0xa559, 'FWA negligible: result is FWB', align=Align.INLINE)
d.comment(0xa55b, 'save the shift count', align=Align.INLINE)
d.comment(0xa55c, 'whole-byte part', align=Align.INLINE)
d.comment(0xa55e, 'none: go to the bit shift', align=Align.INLINE)
d.comment(0xa560, '/ 8...', align=Align.INLINE)
d.comment(0xa561, '...', align=Align.INLINE)
d.comment(0xa562, '= whole-byte shifts', align=Align.INLINE)
d.comment(0xa563, 'X = byte-shift count', align=Align.INLINE)
d.comment(0xa564, 'shift FWA down a byte: m4 -> rnd', align=Align.INLINE)
d.comment(0xa566, '...', align=Align.INLINE)
d.comment(0xa568, 'm3 -> m4', align=Align.INLINE)
d.comment(0xa56a, '...', align=Align.INLINE)
d.comment(0xa56c, 'm2 -> m3', align=Align.INLINE)
d.comment(0xa56e, '...', align=Align.INLINE)
d.comment(0xa570, 'm1 -> m2', align=Align.INLINE)
d.comment(0xa572, '...', align=Align.INLINE)
d.comment(0xa574, 'm1 = 0', align=Align.INLINE)
d.comment(0xa576, 'count', align=Align.INLINE)
d.comment(0xa577, 'loop', align=Align.INLINE)
d.comment(0xa579, 'recover the shift count', align=Align.INLINE)
d.comment(0xa57a, 'bit part', align=Align.INLINE)
d.comment(0xa57c, 'none: take the larger exponent', align=Align.INLINE)
d.comment(0xa57e, 'X = bit-shift count', align=Align.INLINE)
d.comment(0xa57f, 'shift FWA right one bit: m1', align=Align.INLINE)
d.comment(0xa581, 'm2', align=Align.INLINE)
d.comment(0xa583, 'm3', align=Align.INLINE)
d.comment(0xa585, 'm4', align=Align.INLINE)
d.comment(0xa587, 'rnd', align=Align.INLINE)
d.comment(0xa589, 'count', align=Align.INLINE)
d.comment(0xa58a, 'loop', align=Align.INLINE)
d.comment(0xa58e, 'store the larger exponent', align=Align.INLINE)
d.comment(0xa590, 'Compare the signs: load FWA sign', align=Align.INLINE)
d.comment(0xa596, 'Opposite signs: compare magnitudes (m1)', align=Align.INLINE)
d.comment(0xa598, '...', align=Align.INLINE)
d.comment(0xa59a, 'differ: subtract', align=Align.INLINE)
d.comment(0xa59c, 'm2', align=Align.INLINE)
d.comment(0xa59e, '...', align=Align.INLINE)
d.comment(0xa5a0, 'differ: subtract', align=Align.INLINE)
d.comment(0xa5a2, 'm3', align=Align.INLINE)
d.comment(0xa5a4, '...', align=Align.INLINE)
d.comment(0xa5a6, 'differ: subtract', align=Align.INLINE)
d.comment(0xa5a8, 'm4', align=Align.INLINE)
d.comment(0xa5aa, '...', align=Align.INLINE)
d.comment(0xa5ac, 'differ: subtract', align=Align.INLINE)
d.comment(0xa5ae, 'rnd', align=Align.INLINE)
d.comment(0xa5b0, '...', align=Align.INLINE)
d.comment(0xa5b2, 'differ: subtract', align=Align.INLINE)
d.comment(0xa5b7, 'FWA >= FWB? choose the subtraction order', align=Align.INLINE)
d.comment(0xa5b9, 'FWB - FWA: rnd', align=Align.INLINE)
d.comment(0xa5ba, '...', align=Align.INLINE)
d.comment(0xa5bc, '...', align=Align.INLINE)
d.comment(0xa5be, '(store)', align=Align.INLINE)
d.comment(0xa5c0, 'm4', align=Align.INLINE)
d.comment(0xa5c2, '...', align=Align.INLINE)
d.comment(0xa5c4, '(store)', align=Align.INLINE)
d.comment(0xa5c6, 'm3', align=Align.INLINE)
d.comment(0xa5c8, '...', align=Align.INLINE)
d.comment(0xa5ca, '(store)', align=Align.INLINE)
d.comment(0xa5cc, 'm2', align=Align.INLINE)
d.comment(0xa5ce, '...', align=Align.INLINE)
d.comment(0xa5d0, '(store)', align=Align.INLINE)
d.comment(0xa5d2, 'm1', align=Align.INLINE)
d.comment(0xa5d4, '...', align=Align.INLINE)
d.comment(0xa5d6, '(store)', align=Align.INLINE)
d.comment(0xa5d8, 'result takes FWB\'s sign', align=Align.INLINE)
d.comment(0xa5da, '(store)', align=Align.INLINE)
d.comment(0xa5dc, 'normalise the difference', align=Align.INLINE)
d.comment(0xa5df, 'Same sign: add the mantissas', align=Align.INLINE)
d.comment(0xa5e0, 'FWA += FWB', align=Align.INLINE)
d.comment(0xa5e3, 'FWA - FWB: rnd', align=Align.INLINE)
d.comment(0xa5e4, '...', align=Align.INLINE)
d.comment(0xa5e6, '...', align=Align.INLINE)
d.comment(0xa5e8, '(store)', align=Align.INLINE)
d.comment(0xa5ea, 'm4', align=Align.INLINE)
d.comment(0xa5ec, '...', align=Align.INLINE)
d.comment(0xa5ee, '(store)', align=Align.INLINE)
d.comment(0xa5f0, 'm3', align=Align.INLINE)
d.comment(0xa5f2, '...', align=Align.INLINE)
d.comment(0xa5f4, '(store)', align=Align.INLINE)
d.comment(0xa5f6, 'm2', align=Align.INLINE)
d.comment(0xa5f8, '...', align=Align.INLINE)
d.comment(0xa5fa, '(store)', align=Align.INLINE)
d.comment(0xa5fc, 'm1', align=Align.INLINE)

# tokenise_line (&8951): match keywords against keyword_table and
# replace them with tokens, driven by each keyword's flag byte.
d.comment(0x8953, 'Start-of-statement flag (&3B)', align=Align.INLINE)
d.comment(0x8955, 'Clear the quote flag (&3C)', align=Align.INLINE)
d.comment(0x8959, 'CR: end of line', align=Align.INLINE)
d.comment(0x895d, 'space: skip it', align=Align.INLINE)
d.comment(0x8961, 'advance and read the next character', align=Align.INLINE)
d.comment(0x8964, 'loop', align=Align.INLINE)
d.comment(0x8968, 'not "&": check the other cases', align=Align.INLINE)
d.comment(0x896a, 'Hex constant: advance and get a character', align=Align.INLINE)
d.comment(0x896d, 'a digit?', align=Align.INLINE)
d.comment(0x8970, 'yes: keep copying', align=Align.INLINE)
d.comment(0x8972, "below 'A'?", align=Align.INLINE)
d.comment(0x8974, 'not hex: resume scanning', align=Align.INLINE)
d.comment(0x8976, "'A'..'F'?", align=Align.INLINE)
d.comment(0x8978, 'hex letter: keep copying', align=Align.INLINE)
d.comment(0x897a, 'past F: resume', align=Align.INLINE)
d.comment(0x897e, 'not a quote: check for a colon', align=Align.INLINE)
d.comment(0x8980, 'String literal: copy to the closing quote', align=Align.INLINE)
d.comment(0x8983, 'a quote?', align=Align.INLINE)
d.comment(0x8985, 'yes: end of string', align=Align.INLINE)
d.comment(0x8987, 'CR (unterminated)?', align=Align.INLINE)
d.comment(0x8989, 'no: keep copying', align=Align.INLINE)
d.comment(0x898b, 'Return', align=Align.INLINE)
d.comment(0x898e, 'not a colon: check for a comma', align=Align.INLINE)
d.comment(0x8990, 'Colon: back to start-of-statement', align=Align.INLINE)
d.comment(0x8992, 'clear the quote flag', align=Align.INLINE)
d.comment(0x8994, 'continue', align=Align.INLINE)
d.comment(0x8996, 'a comma?', align=Align.INLINE)
d.comment(0x8998, 'yes: skip it', align=Align.INLINE)
d.comment(0x899c, 'not "*": try a keyword or name', align=Align.INLINE)
d.comment(0x899e, 'at the start of a statement?', align=Align.INLINE)
d.comment(0x89a0, 'yes: "*command", skip the rest of the line', align=Align.INLINE)
d.comment(0x89a2, 'Return', align=Align.INLINE)
d.comment(0x89a3, 'a "." (abbreviation dot)?', align=Align.INLINE)
d.comment(0x89a5, 'yes', align=Align.INLINE)
d.comment(0x89a7, 'a digit?', align=Align.INLINE)
d.comment(0x89aa, 'no: a letter or symbol', align=Align.INLINE)
d.comment(0x89ac, 'inside a quote?', align=Align.INLINE)
d.comment(0x89ae, 'no: a line number', align=Align.INLINE)
d.comment(0x89b0, 'tokenise the line number', align=Align.INLINE)
d.comment(0x89b3, 'continue', align=Align.INLINE)
d.comment(0x89b5, 'Skip a number: read a character', align=Align.INLINE)
d.comment(0x89b7, 'a digit or "."?', align=Align.INLINE)
d.comment(0x89ba, 'no: end of the number', align=Align.INLINE)
d.comment(0x89bc, 'advance', align=Align.INLINE)
d.comment(0x89bf, 'loop', align=Align.INLINE)
d.comment(0x89c2, 'Now in the middle of a statement:', align=Align.INLINE)
d.comment(0x89c4, 'set the flag', align=Align.INLINE)
d.comment(0x89c6, 'clear the quote flag', align=Align.INLINE)
d.comment(0x89c8, 'resume scanning', align=Align.INLINE)
d.comment(0x89cb, 'Skip a variable name: alphanumeric?', align=Align.INLINE)
d.comment(0x89ce, 'no: not a name', align=Align.INLINE)
d.comment(0x89d0, 'Read the next name character:', align=Align.INLINE)
d.comment(0x89d2, '...', align=Align.INLINE)
d.comment(0x89d4, 'alphanumeric?', align=Align.INLINE)
d.comment(0x89d7, 'no: end of the name', align=Align.INLINE)
d.comment(0x89d9, 'advance', align=Align.INLINE)
d.comment(0x89dc, 'loop', align=Align.INLINE)
d.comment(0x89df, "a letter ('A'+)?", align=Align.INLINE)
d.comment(0x89e1, 'yes: try to match a keyword', align=Align.INLINE)
d.comment(0x89e3, 'Not a keyword: middle of statement', align=Align.INLINE)
d.comment(0x89e5, '...', align=Align.INLINE)
d.comment(0x89e7, '...', align=Align.INLINE)
d.comment(0x89e9, 'continue scanning', align=Align.INLINE)
d.comment(0x89ec, "'X' or above?", align=Align.INLINE)
d.comment(0x89ee, 'nothing starts with X/Y/Z: skip the name', align=Align.INLINE)
d.comment(0x89f0, 'Point at the keyword table (&8071): low', align=Align.INLINE)
d.comment(0x89f2, '...', align=Align.INLINE)
d.comment(0x89f4, 'high &80', align=Align.INLINE)
d.comment(0x89f6, '...', align=Align.INLINE)
d.comment(0x89f8, 'Compare the first letter with this entry', align=Align.INLINE)
d.comment(0x89fa, 'entry past our letter: not a keyword', align=Align.INLINE)
d.comment(0x89fc, 'first letter differs: next entry', align=Align.INLINE)
d.comment(0x89fe, 'matches: compare the rest of the keyword', align=Align.INLINE)
d.comment(0x89ff, 'entry char (bit 7 = the token)', align=Align.INLINE)
d.comment(0x8a01, 'whole keyword matched: got a token', align=Align.INLINE)
d.comment(0x8a03, 'compare with the line', align=Align.INLINE)
d.comment(0x8a05, 'match: next character', align=Align.INLINE)
d.comment(0x8a07, 'mismatch: a "." abbreviation?', align=Align.INLINE)
d.comment(0x8a09, '...', align=Align.INLINE)
d.comment(0x8a0b, 'yes: accept the abbreviation', align=Align.INLINE)
d.comment(0x8a0d, 'Skip to the next entry: past the name', align=Align.INLINE)
d.comment(0x8a0e, '...', align=Align.INLINE)
d.comment(0x8a10, 'until the token byte (bit 7 set)', align=Align.INLINE)
d.comment(0x8a12, 'end of the table?', align=Align.INLINE)
d.comment(0x8a14, 'no', align=Align.INLINE)
d.comment(0x8a16, 'end: not a keyword (skip the name)', align=Align.INLINE)
d.comment(0x8a18, 'Abbreviation: skip to this entry\'s token', align=Align.INLINE)
d.comment(0x8a19, '...', align=Align.INLINE)
d.comment(0x8a1b, 'token byte: got it', align=Align.INLINE)
d.comment(0x8a1d, 'advance the table pointer', align=Align.INLINE)
d.comment(0x8a1f, '...', align=Align.INLINE)
d.comment(0x8a21, 'carry into high', align=Align.INLINE)
d.comment(0x8a23, 'loop', align=Align.INLINE)
d.comment(0x8a25, 'Advance past this entry to the next:', align=Align.INLINE)
d.comment(0x8a26, '...', align=Align.INLINE)
d.comment(0x8a27, '...', align=Align.INLINE)
d.comment(0x8a28, 'low', align=Align.INLINE)
d.comment(0x8a2a, '...', align=Align.INLINE)
d.comment(0x8a2c, '...', align=Align.INLINE)
d.comment(0x8a2e, 'carry into high', align=Align.INLINE)
d.comment(0x8a30, 'reset Y', align=Align.INLINE)
d.comment(0x8a32, 're-read the first letter', align=Align.INLINE)
d.comment(0x8a34, 'try the next entry', align=Align.INLINE)
d.comment(0x8a37, 'Token byte found: keep it in X', align=Align.INLINE)
d.comment(0x8a38, 'the flag byte follows', align=Align.INLINE)
d.comment(0x8a39, 'get the token flag', align=Align.INLINE)
d.comment(0x8a3b, '(save it in &3D)', align=Align.INLINE)
d.comment(0x8a3d, '...', align=Align.INLINE)
d.comment(0x8a3e, 'flag bit 0: conditional tokenisation?', align=Align.INLINE)
d.comment(0x8a3f, 'no', align=Align.INLINE)
d.comment(0x8a41, 'a letter follows?', align=Align.INLINE)
d.comment(0x8a43, '...', align=Align.INLINE)
d.comment(0x8a46, 'yes: keep it as a name, not a token', align=Align.INLINE)
d.comment(0x8a48, 'Emit the token: A = token byte', align=Align.INLINE)
d.comment(0x8a49, 'flag bit 6: pseudo-variable?', align=Align.INLINE)
d.comment(0x8a4b, 'no', align=Align.INLINE)
d.comment(0x8a4d, 'at the start of a statement?', align=Align.INLINE)
d.comment(0x8a4f, 'no', align=Align.INLINE)
d.comment(0x8a51, '...', align=Align.INLINE)
d.comment(0x8a52, 'assignment form: token + &40', align=Align.INLINE)
d.comment(0x8a54, 'Write the token over the keyword', align=Align.INLINE)
d.comment(0x8a55, '...', align=Align.INLINE)
d.comment(0x8a58, 'reset Y', align=Align.INLINE)
d.comment(0x8a5a, '...', align=Align.INLINE)
d.comment(0x8a5c, 'Apply the state-change flags:', align=Align.INLINE)
d.comment(0x8a5e, 'bit 0 (already used)', align=Align.INLINE)
d.comment(0x8a5f, 'bit 1: enter middle-of-statement?', align=Align.INLINE)
d.comment(0x8a60, 'no', align=Align.INLINE)
d.comment(0x8a62, 'set middle-of-statement', align=Align.INLINE)
d.comment(0x8a64, 'clear quote', align=Align.INLINE)
d.comment(0x8a66, 'bit 2: enter start-of-statement?', align=Align.INLINE)
d.comment(0x8a67, 'no', align=Align.INLINE)
d.comment(0x8a69, 'set start-of-statement', align=Align.INLINE)
d.comment(0x8a6b, 'clear quote', align=Align.INLINE)
d.comment(0x8a6d, 'bit 3: FN/PROC (do not tokenise the name)?', align=Align.INLINE)
d.comment(0x8a6e, 'no', align=Align.INLINE)
d.comment(0x8a70, 'save A', align=Align.INLINE)
d.comment(0x8a71, 'skip the FN/PROC name untokenised:', align=Align.INLINE)
d.comment(0x8a72, 'char', align=Align.INLINE)
d.comment(0x8a74, 'alphanumeric?', align=Align.INLINE)
d.comment(0x8a77, 'no: end of the name', align=Align.INLINE)
d.comment(0x8a79, 'advance', align=Align.INLINE)
d.comment(0x8a7c, 'loop', align=Align.INLINE)
d.comment(0x8a7f, '...', align=Align.INLINE)
d.comment(0x8a80, 'restore A', align=Align.INLINE)
d.comment(0x8a81, 'bit 4: start a line number?', align=Align.INLINE)
d.comment(0x8a82, 'no', align=Align.INLINE)
d.comment(0x8a84, 'set the line-number flag', align=Align.INLINE)
d.comment(0x8a86, 'bit 5: skip the rest of the line (REM/DATA)?', align=Align.INLINE)
d.comment(0x8a87, 'yes: stop tokenising', align=Align.INLINE)
d.comment(0x8a89, 'continue scanning', align=Align.INLINE)

d.comment(0x9fc0, 'output the value', align=Align.INLINE)
d.subroutine(0xa6e7, 'fp_divide', title='FWA = FWA / divisor (restoring long division)',
             description='Floating-point divide: 32 quotient bits plus guard bits by repeated compare/subtract/shift; the quotient builds in &43-&46.')

# fn_tan (&A6BE): TAN = sin / cos
d.comment(0xa6be, 'Evaluate the argument as a real', align=Align.INLINE)
d.comment(0xa6c1, 'Compute the trig kernel', align=Align.INLINE)
d.comment(0xa6c4, 'save the quadrant', align=Align.INLINE)
d.comment(0xa6c6, '...', align=Align.INLINE)
d.comment(0xa6c7, 'save the first result (cos) in TEMP4', align=Align.INLINE)
d.comment(0xa6ca, '...', align=Align.INLINE)
d.comment(0xa6cd, 'shift the quadrant (cos -> sin)', align=Align.INLINE)
d.comment(0xa6cf, 'compute the other (sin)', align=Align.INLINE)
d.comment(0xa6d2, 'point at TEMP4', align=Align.INLINE)
d.comment(0xa6d5, 'swap FWA (sin) with TEMP4 (cos)', align=Align.INLINE)
d.comment(0xa6d8, 'restore the quadrant', align=Align.INLINE)
d.comment(0xa6d9, '...', align=Align.INLINE)
d.comment(0xa6db, 'finish the trig (cos in FWA)', align=Align.INLINE)
d.comment(0xa6de, 'point at TEMP4 (sin)', align=Align.INLINE)
d.comment(0xa6e1, 'TAN = sin / cos', align=Align.INLINE)
d.comment(0xa6e4, 'real result', align=Align.INLINE)
d.comment(0xa6e6, 'Return TAN', align=Align.INLINE)
# fp_divide (&A6E7)
d.comment(0xa6e7, 'Is the dividend (FWA) zero?', align=Align.INLINE)
d.comment(0xa6ea, 'zero: result is zero', align=Align.INLINE)
d.comment(0xa6ec, 'unpack the divisor into FWB', align=Align.INLINE)
d.comment(0xa6ef, 'divisor zero: Division by zero', align=Align.INLINE)
d.comment(0xa6f1, 'result sign = sign XOR sign', align=Align.INLINE)
d.comment(0xa6f3, '...', align=Align.INLINE)
d.comment(0xa6f5, '...', align=Align.INLINE)
d.comment(0xa6f7, 'result exponent = dividend - divisor:', align=Align.INLINE)
d.comment(0xa6f8, '...', align=Align.INLINE)
d.comment(0xa6fa, '...', align=Align.INLINE)
d.comment(0xa6fc, '...', align=Align.INLINE)
d.comment(0xa6fe, 'borrow into overflow', align=Align.INLINE)
d.comment(0xa700, '...', align=Align.INLINE)
d.comment(0xa701, 're-bias the exponent', align=Align.INLINE)
d.comment(0xa703, '...', align=Align.INLINE)
d.comment(0xa705, '...', align=Align.INLINE)
d.comment(0xa707, '...', align=Align.INLINE)
d.comment(0xa709, '...', align=Align.INLINE)
d.comment(0xa70a, '32 quotient bits (restoring long division):', align=Align.INLINE)
d.comment(0xa70c, 'remainder >= divisor?', align=Align.INLINE)
d.comment(0xa70e, 'compare FWA (remainder) with FWB (divisor):', align=Align.INLINE)
d.comment(0xa710, '...', align=Align.INLINE)
d.comment(0xa712, '...', align=Align.INLINE)
d.comment(0xa714, '...', align=Align.INLINE)
d.comment(0xa716, '...', align=Align.INLINE)
d.comment(0xa718, '...', align=Align.INLINE)
d.comment(0xa71a, '...', align=Align.INLINE)
d.comment(0xa71c, '...', align=Align.INLINE)
d.comment(0xa71e, '...', align=Align.INLINE)
d.comment(0xa720, '...', align=Align.INLINE)
d.comment(0xa722, '...', align=Align.INLINE)
d.comment(0xa724, 'less: quotient bit 0', align=Align.INLINE)
d.comment(0xa726, 'subtract the divisor from the remainder:', align=Align.INLINE)
d.comment(0xa728, '...', align=Align.INLINE)
d.comment(0xa72a, '...', align=Align.INLINE)
d.comment(0xa72c, '...', align=Align.INLINE)
d.comment(0xa72e, '...', align=Align.INLINE)
d.comment(0xa730, '...', align=Align.INLINE)
d.comment(0xa732, '...', align=Align.INLINE)
d.comment(0xa734, '...', align=Align.INLINE)
d.comment(0xa736, '...', align=Align.INLINE)
d.comment(0xa738, '...', align=Align.INLINE)
d.comment(0xa73a, '...', align=Align.INLINE)
d.comment(0xa73c, '...', align=Align.INLINE)
d.comment(0xa73e, 'quotient bit 1', align=Align.INLINE)
d.comment(0xa73f, 'shift the quotient left, bring in the bit:', align=Align.INLINE)
d.comment(0xa741, '...', align=Align.INLINE)
d.comment(0xa743, '...', align=Align.INLINE)
d.comment(0xa745, '...', align=Align.INLINE)
d.comment(0xa747, 'shift the remainder left:', align=Align.INLINE)
d.comment(0xa749, '...', align=Align.INLINE)
d.comment(0xa74b, '...', align=Align.INLINE)
d.comment(0xa74d, '...', align=Align.INLINE)
d.comment(0xa74f, 'count', align=Align.INLINE)
d.comment(0xa750, 'loop 32 times', align=Align.INLINE)
d.comment(0xa752, '7 guard bits:', align=Align.INLINE)
d.comment(0xa754, 'remainder >= divisor?', align=Align.INLINE)
d.comment(0xa756, '...', align=Align.INLINE)
d.comment(0xa758, '...', align=Align.INLINE)
d.comment(0xa75a, '...', align=Align.INLINE)
d.comment(0xa75c, '...', align=Align.INLINE)
d.comment(0xa75e, '...', align=Align.INLINE)
d.comment(0xa760, '...', align=Align.INLINE)
d.comment(0xa762, '...', align=Align.INLINE)
d.comment(0xa764, '...', align=Align.INLINE)
d.comment(0xa766, '...', align=Align.INLINE)
d.comment(0xa768, '...', align=Align.INLINE)
d.comment(0xa76a, '...', align=Align.INLINE)
d.comment(0xa76c, 'less: bit 0', align=Align.INLINE)
d.comment(0xa76e, 'subtract:', align=Align.INLINE)
d.comment(0xa770, '...', align=Align.INLINE)
d.comment(0xa772, '...', align=Align.INLINE)
d.comment(0xa774, '...', align=Align.INLINE)
d.comment(0xa776, '...', align=Align.INLINE)
d.comment(0xa778, '...', align=Align.INLINE)
d.comment(0xa77a, '...', align=Align.INLINE)
d.comment(0xa77c, '...', align=Align.INLINE)
d.comment(0xa77e, '...', align=Align.INLINE)
d.comment(0xa780, '...', align=Align.INLINE)
d.comment(0xa782, '...', align=Align.INLINE)
d.comment(0xa784, '...', align=Align.INLINE)
d.comment(0xa786, '...', align=Align.INLINE)
d.comment(0xa787, 'shift in the guard bit', align=Align.INLINE)
d.comment(0xa789, 'shift the remainder:', align=Align.INLINE)
d.comment(0xa78b, '...', align=Align.INLINE)
d.comment(0xa78d, '...', align=Align.INLINE)
d.comment(0xa78f, '...', align=Align.INLINE)
d.comment(0xa791, 'count', align=Align.INLINE)
d.comment(0xa792, 'loop', align=Align.INLINE)
d.comment(0xa794, 'final guard bit', align=Align.INLINE)
d.comment(0xa796, 'move the quotient into the FWA mantissa:', align=Align.INLINE)
d.comment(0xa798, '...', align=Align.INLINE)
d.comment(0xa79a, '...', align=Align.INLINE)
d.comment(0xa79c, '...', align=Align.INLINE)
d.comment(0xa79e, '...', align=Align.INLINE)
d.comment(0xa7a0, '...', align=Align.INLINE)
d.comment(0xa7a2, '...', align=Align.INLINE)
d.comment(0xa7a4, '...', align=Align.INLINE)
d.comment(0xa7a6, 'normalise and round', align=Align.INLINE)
d.comment(0xa7a9, 'SQR of a negative: error block', align=Align.INLINE)
d.subroutine(0xa140, 'parse_exponent', title='Parse the "E" exponent (optional sign, 1-2 digits)')

# parse_number (&A07B): parse a decimal number at PtrB into the accumulator
d.comment(0xa07b, 'Clear FWA:', align=Align.INLINE)
d.comment(0xa07d, '...', align=Align.INLINE)
d.comment(0xa07f, '...', align=Align.INLINE)
d.comment(0xa081, '...', align=Align.INLINE)
d.comment(0xa083, '...', align=Align.INLINE)
d.comment(0xa085, '...', align=Align.INLINE)
d.comment(0xa087, 'clear the decimal-point flag', align=Align.INLINE)
d.comment(0xa089, 'decimal exponent = 0', align=Align.INLINE)
d.comment(0xa08b, 'a leading decimal point?', align=Align.INLINE)
d.comment(0xa08d, 'yes', align=Align.INLINE)
d.comment(0xa08f, "not a digit (>= ':')?", align=Align.INLINE)
d.comment(0xa091, 'finish', align=Align.INLINE)
d.comment(0xa093, 'convert to binary 0-9', align=Align.INLINE)
d.comment(0xa095, 'not a digit: finish', align=Align.INLINE)
d.comment(0xa097, 'store the digit', align=Align.INLINE)
d.comment(0xa099, 'next character', align=Align.INLINE)
d.comment(0xa09a, '...', align=Align.INLINE)
d.comment(0xa09c, 'a decimal point?', align=Align.INLINE)
d.comment(0xa09e, 'no', align=Align.INLINE)
d.comment(0xa0a0, 'already had one?', align=Align.INLINE)
d.comment(0xa0a2, 'yes: end of the number', align=Align.INLINE)
d.comment(0xa0a4, 'set the decimal-point flag', align=Align.INLINE)
d.comment(0xa0a6, 'next char', align=Align.INLINE)
d.comment(0xa0a8, "'E' (exponent)?", align=Align.INLINE)
d.comment(0xa0aa, 'yes: scan the exponent', align=Align.INLINE)
d.comment(0xa0ac, 'not a digit?', align=Align.INLINE)
d.comment(0xa0ae, 'finish', align=Align.INLINE)
d.comment(0xa0b0, 'convert to binary', align=Align.INLINE)
d.comment(0xa0b2, 'not a digit: finish', align=Align.INLINE)
d.comment(0xa0b4, 'mantissa top byte', align=Align.INLINE)
d.comment(0xa0b6, 'room for another digit?', align=Align.INLINE)
d.comment(0xa0b8, 'yes: add it', align=Align.INLINE)
d.comment(0xa0ba, 'too big: had a decimal point?', align=Align.INLINE)
d.comment(0xa0bc, 'yes: just skip the digit', align=Align.INLINE)
d.comment(0xa0be, 'no: bump the exponent and skip', align=Align.INLINE)
d.comment(0xa0c0, '...', align=Align.INLINE)
d.comment(0xa0c2, 'had a decimal point?', align=Align.INLINE)
d.comment(0xa0c4, 'no', align=Align.INLINE)
d.comment(0xa0c6, 'yes: decrement the exponent', align=Align.INLINE)
d.comment(0xa0c8, 'FWA mantissa *= 10', align=Align.INLINE)
d.comment(0xa0cb, 'add the digit to the low byte', align=Align.INLINE)
d.comment(0xa0cd, '...', align=Align.INLINE)
d.comment(0xa0cf, 'no carry: next digit', align=Align.INLINE)
d.comment(0xa0d1, 'carry up through the mantissa', align=Align.INLINE)
d.comment(0xa0d3, '...', align=Align.INLINE)
d.comment(0xa0d5, '...', align=Align.INLINE)
d.comment(0xa0d7, '...', align=Align.INLINE)
d.comment(0xa0d9, '...', align=Align.INLINE)
d.comment(0xa0db, '...', align=Align.INLINE)
d.comment(0xa0dd, '...', align=Align.INLINE)
d.comment(0xa0df, 'next digit', align=Align.INLINE)
d.comment(0xa0e1, 'scan the E exponent', align=Align.INLINE)
d.comment(0xa0e4, 'add to the decimal exponent', align=Align.INLINE)
d.comment(0xa0e6, '...', align=Align.INLINE)
d.comment(0xa0e8, 'store the text offset', align=Align.INLINE)
d.comment(0xa0ea, 'any exponent or decimal point?', align=Align.INLINE)
d.comment(0xa0ec, '...', align=Align.INLINE)
d.comment(0xa0ee, 'no: return an integer', align=Align.INLINE)
d.comment(0xa0f0, 'value zero?', align=Align.INLINE)
d.comment(0xa0f3, 'yes: done', align=Align.INLINE)
d.comment(0xa0f5, 'Set the FWA exponent (40-bit mantissa)...', align=Align.INLINE)
d.comment(0xa0f7, '...', align=Align.INLINE)
d.comment(0xa0f9, '...', align=Align.INLINE)
d.comment(0xa0fb, 'clear overflow', align=Align.INLINE)
d.comment(0xa0fd, 'clear sign', align=Align.INLINE)
d.comment(0xa0ff, 'normalise', align=Align.INLINE)
d.comment(0xa102, 'apply the decimal exponent:', align=Align.INLINE)
d.comment(0xa104, 'negative: divide', align=Align.INLINE)
d.comment(0xa106, 'zero: done', align=Align.INLINE)
d.comment(0xa108, 'positive: multiply by 10', align=Align.INLINE)
d.comment(0xa10b, '...', align=Align.INLINE)
d.comment(0xa10d, 'loop', align=Align.INLINE)
d.comment(0xa10f, 'done', align=Align.INLINE)
d.comment(0xa111, 'divide by 10', align=Align.INLINE)
d.comment(0xa114, '...', align=Align.INLINE)
d.comment(0xa116, 'loop', align=Align.INLINE)
d.comment(0xa118, 'round the result', align=Align.INLINE)
d.comment(0xa11b, 'real result', align=Align.INLINE)
d.comment(0xa11c, '...', align=Align.INLINE)
d.comment(0xa11e, 'Return (real)', align=Align.INLINE)
d.comment(0xa11f, 'Integer: does it fit in 32 signed bits?', align=Align.INLINE)
d.comment(0xa121, '...', align=Align.INLINE)
d.comment(0xa123, '...', align=Align.INLINE)
d.comment(0xa125, 'top byte set (too big)?', align=Align.INLINE)
d.comment(0xa127, 'yes: use a real instead', align=Align.INLINE)
d.comment(0xa129, 'Copy the mantissa to IWA:', align=Align.INLINE)
d.comment(0xa12b, '...', align=Align.INLINE)
d.comment(0xa12d, '...', align=Align.INLINE)
d.comment(0xa12f, '...', align=Align.INLINE)
d.comment(0xa131, '...', align=Align.INLINE)
d.comment(0xa133, '...', align=Align.INLINE)
d.comment(0xa135, 'integer result', align=Align.INLINE)
d.comment(0xa137, '...', align=Align.INLINE)
d.comment(0xa138, 'Return (integer)', align=Align.INLINE)
d.comment(0xa139, 'negative exponent: scan the digits', align=Align.INLINE)
d.comment(0xa13c, 'negate it', align=Align.INLINE)
d.comment(0xa13e, '...', align=Align.INLINE)
d.comment(0xa13f, 'Return', align=Align.INLINE)
d.comment(0xa140, 'Scan exponent: next character', align=Align.INLINE)
d.comment(0xa141, 'read it', align=Align.INLINE)
d.comment(0xa143, "'-'?", align=Align.INLINE)
d.comment(0xa145, 'yes: negative exponent', align=Align.INLINE)
d.comment(0xa147, "'+'?", align=Align.INLINE)
d.comment(0xa149, 'no sign', align=Align.INLINE)
d.comment(0xa14b, 'skip the sign', align=Align.INLINE)
d.comment(0xa14c, 'read the digit after the sign', align=Align.INLINE)
d.comment(0xa14e, 'a digit?', align=Align.INLINE)
d.comment(0xa150, 'no: exponent = 0', align=Align.INLINE)
d.comment(0xa152, 'convert', align=Align.INLINE)
d.comment(0xa154, 'not a digit: exponent = 0', align=Align.INLINE)
d.comment(0xa156, 'store the first exponent digit', align=Align.INLINE)
d.comment(0xa158, 'second digit?', align=Align.INLINE)
d.comment(0xa159, 'read it', align=Align.INLINE)
d.comment(0xa15b, 'above 9?', align=Align.INLINE)
d.comment(0xa15d, 'one digit only', align=Align.INLINE)
d.comment(0xa15f, 'convert', align=Align.INLINE)
d.comment(0xa161, 'not a digit', align=Align.INLINE)
d.comment(0xa163, 'two digits: exp = d1*10 + d2', align=Align.INLINE)
d.comment(0xa164, 'save d2', align=Align.INLINE)
d.comment(0xa166, 'd1', align=Align.INLINE)
d.comment(0xa168, 'd1 * 10...', align=Align.INLINE)
d.comment(0xa169, '(d1 * 4)', align=Align.INLINE)
d.comment(0xa16a, '+ d1 (now * 5)', align=Align.INLINE)
d.comment(0xa16c, '* 2 (now * 10)', align=Align.INLINE)
d.comment(0xa16d, '+ d2', align=Align.INLINE)
d.comment(0xa16f, 'Return the exponent', align=Align.INLINE)
d.comment(0xa170, '1-digit exponent', align=Align.INLINE)
d.comment(0xa172, 'carry clear for the caller ADC', align=Align.INLINE)
d.comment(0xa173, 'Return', align=Align.INLINE)
d.comment(0xa174, 'no exponent: 0', align=Align.INLINE)
d.comment(0xa176, 'carry clear for the caller ADC', align=Align.INLINE)
d.comment(0xa177, 'Return', align=Align.INLINE)

# fwa_swap_var (&A4D6): exchange FWA with the fp variable
d.comment(0xa4d6, 'FWB = the fp variable', align=Align.INLINE)
d.comment(0xa4d9, 'Store FWA into the variable; FWA = old variable', align=Align.INLINE)
# fwa_add_var (&A500): FWA = FWA + fp variable
d.comment(0xa500, 'FWB = the fp variable', align=Align.INLINE)
# fwa_compare_var (&A5FF): compare FWA with the fp variable
d.comment(0xa5ff, 'Shift the comparison result, then normalise', align=Align.INLINE)
d.comment(0xa602, 'normalise the difference', align=Align.INLINE)
d.comment(0xa605, 'Return', align=Align.INLINE)
# fn_lomem (&AEFC): =LOMEM
d.comment(0xaefc, 'LOMEM low byte', align=Align.INLINE)
d.comment(0xaefe, 'high byte', align=Align.INLINE)
d.comment(0xaf00, 'Return LOMEM as an integer', align=Align.INLINE)
# fn_erl (&AF9F): ERL
d.comment(0xaf9f, 'ERL high byte', align=Align.INLINE)
d.comment(0xafa1, 'low byte', align=Align.INLINE)
d.comment(0xafa3, 'Return ERL as an integer', align=Align.INLINE)
# fn_err (&AFA6): ERR
d.comment(0xafa6, 'Read the error number...', align=Align.INLINE)
d.comment(0xafa8, '...from the error block (&FD)', align=Align.INLINE)
d.comment(0xafaa, 'Return ERR as an integer', align=Align.INLINE)
# skip_spaces_expect_comma (&8AAE)
d.comment(0x8aae, 'Skip spaces at PtrB', align=Align.INLINE)
d.comment(0x8ab1, 'Require a comma', align=Align.INLINE)
d.comment(0x8ab3, 'Missing: "Missing ," error', align=Align.INLINE)
d.comment(0x8ab5, 'Return', align=Align.INLINE)
# stmt_page (&9283): PAGE = value
d.comment(0x9283, 'Step past "=", evaluate an integer', align=Align.INLINE)
d.comment(0x9286, 'PAGE is a page number (the high byte)', align=Align.INLINE)
d.comment(0x9288, '(store)', align=Align.INLINE)
d.comment(0x928a, 'Back to execution', align=Align.INLINE)
# stmt_draw (&93E8): DRAW = PLOT 5
d.comment(0x93e8, 'DRAW is PLOT 5 (draw a line)', align=Align.INLINE)
d.comment(0x93ea, 'Save the plot mode', align=Align.INLINE)
d.comment(0x93eb, 'Evaluate the X coordinate', align=Align.INLINE)
d.comment(0x93ee, 'evaluate Y and plot', align=Align.INLINE)
# fn_page (&AEC0): =PAGE
d.comment(0xaec0, 'PAGE low byte is always 0...', align=Align.INLINE)
d.comment(0xaec2, '...high byte is the page number', align=Align.INLINE)
d.comment(0xaec4, 'Return PAGE as an integer', align=Align.INLINE)
d.comment(0xaec7, 'syntax error (shared)', align=Align.INLINE)
# fn_inkey (&ACAD): INKEY
d.comment(0xacad, 'Read a key within the time limit', align=Align.INLINE)
d.comment(0xacb0, 'timed out?', align=Align.INLINE)
d.comment(0xacb2, 'no key: return -1 (TRUE)', align=Align.INLINE)
d.comment(0xacb4, 'X = the key code', align=Align.INLINE)
d.comment(0xacb5, 'Return the key code as an integer', align=Align.INLINE)
# iwa_abs (&AD71): make IWA positive
d.comment(0xad71, 'Test the sign of IWA (top byte)', align=Align.INLINE)
d.comment(0xad73, 'Negative: negate it', align=Align.INLINE)
d.comment(0xad75, 'Positive: leave it', align=Align.INLINE)
d.comment(0xad77, 'ABS of a real: get the sign', align=Align.INLINE)
d.comment(0xad7a, 'positive/zero: done', align=Align.INLINE)
d.comment(0xad7c, 'negative: clear the sign', align=Align.INLINE)
# fwa_rdiv_var (&A6AD): FWA = fp var / FWA
d.comment(0xa6ad, 'Is FWA (the divisor) zero?', align=Align.INLINE)
d.comment(0xa6b0, 'yes: Division by zero', align=Align.INLINE)
d.comment(0xa6b2, 'FWB = FWA (the divisor)', align=Align.INLINE)
d.comment(0xa6b5, 'FWA = the fp variable (the dividend)', align=Align.INLINE)
d.comment(0xa6b8, 'non-zero: do the division', align=Align.INLINE)
d.comment(0xa6ba, 'dividend zero: result is zero', align=Align.INLINE)
d.comment(0xa6bb, 'Division by zero error', align=Align.INLINE)
# stmt_himem (&925D): HIMEM = value
d.comment(0x925d, 'Step past "=", evaluate an integer', align=Align.INLINE)
d.comment(0x9260, 'Set HIMEM and the stack: low', align=Align.INLINE)
d.comment(0x9262, 'HIMEM low', align=Align.INLINE)
d.comment(0x9264, 'stack pointer low', align=Align.INLINE)
d.comment(0x9266, 'high', align=Align.INLINE)
d.comment(0x9268, 'HIMEM high', align=Align.INLINE)
d.comment(0x926a, 'stack pointer high', align=Align.INLINE)
d.comment(0x926c, 'Back to execution', align=Align.INLINE)
# fwa_negate (&AD7E): FWA = -FWA
d.comment(0xad7e, 'Is FWA zero?', align=Align.INLINE)
d.comment(0xad81, 'zero: nothing to negate', align=Align.INLINE)
d.comment(0xad83, 'Toggle the sign bit...', align=Align.INLINE)
d.comment(0xad85, '...', align=Align.INLINE)
d.comment(0xad87, '(store)', align=Align.INLINE)
d.comment(0xad89, 'real result type', align=Align.INLINE)
d.comment(0xad8b, 'Return', align=Align.INLINE)
d.comment(0xad8c, 'Unary minus: evaluate the operand', align=Align.INLINE)
d.comment(0xad8f, 'zero: leave it', align=Align.INLINE)
d.comment(0xad91, 'real: negate FWA', align=Align.INLINE)
# fn_adval (&AB33): ADVAL
d.comment(0xab33, 'Evaluate the integer argument', align=Align.INLINE)
d.comment(0xab36, 'X = the channel / buffer number', align=Align.INLINE)
d.comment(0xab38, 'OSBYTE &80: read ADC / buffer status', align=Align.INLINE)
d.comment(0xab3d, 'result low byte (X)', align=Align.INLINE)
d.comment(0xab3e, 'Return as an integer', align=Align.INLINE)
# fn_vpos (&AB76): VPOS
d.comment(0xab76, 'OSBYTE &86: read the cursor position', align=Align.INLINE)
d.comment(0xab7c, 'Return the row (Y) as an integer', align=Align.INLINE)

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
