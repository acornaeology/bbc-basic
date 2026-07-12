import hashlib
import os
import sys
from pathlib import Path

import dasmos
from dasmos import Align
from dasmos.expr import param, group, ref, char
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

# ----------------------------------------------------------------------
# Inline-assembler mnemonic tables (&8450). Three parallel byte arrays,
# indexed by the same X: asm_mnemonic_lo / asm_mnemonic_hi hold the low
# / high halves of a 15-bit "packed name" hash of each mnemonic, and
# asm_base_opcode holds the base ("mode 0") opcode. The banner rendered
# at &8450 describes the full scheme, packing, and index ordering.
# ----------------------------------------------------------------------
ASM_MNEMONIC_LO_BASE = 0x8450
ASM_MNEMONIC_HI_BASE = 0x848a
ASM_BASE_OPCODE_BASE = 0x84c4
# The labels sit on each table's real first entry (BRK), one past the
# *_BASE addressing base; the code reads the tables as `<label> - 1,x`.
ASM_MNEMONIC_LO = 0x8451
ASM_MNEMONIC_HI = 0x848b
ASM_BASE_OPCODE = 0x84c5

# Mnemonic recognised at each table index. Index &00 is dead padding
# (the scan runs X = &3A..1, so index 0 is never tested). Indices &39 /
# &3A are the OPT and EQU directives, which have no base-opcode entry.
ASM_MNEMONICS = [
    None,                                                          # &00 padding
    'BRK', 'CLC', 'CLD', 'CLI', 'CLV', 'DEX', 'DEY', 'INX', 'INY', 'NOP',
    'PHA', 'PHP', 'PLA', 'PLP', 'RTI', 'RTS', 'SEC', 'SED', 'SEI',
    'TAX', 'TAY', 'TSX', 'TXA', 'TXS', 'TYA',                       # ..&19 implied
    'BCC', 'BCS', 'BEQ', 'BMI', 'BNE', 'BPL', 'BVC', 'BVS',         # &1A..&21 branches
    'AND', 'EOR', 'ORA', 'ADC', 'CMP', 'LDA', 'SBC',               # &22..&28 full modes
    'ASL', 'LSR', 'ROL', 'ROR',                                    # &29..&2C A or memory
    'DEC', 'INC',                                                  # &2D..&2E memory only
    'CPX', 'CPY',                                                  # &2F..&30 #/zp/abs
    'BIT',                                                         # &31 abs/zp
    'JMP', 'JSR',                                                  # &32..&33
    'LDX', 'LDY', 'STA',                                           # &34..&36
    'STX', 'STY',                                                  # &37..&38 two-register
    'OPT',                                                         # &39 directive
    'EQU',                                                         # &3A directive (EQUB/W/D/S)
]

# Base ("mode 0") opcode for indices &00..&38. The bytes are the group's
# addressing-mode column-0 value; the operand parser adds column offsets
# via asm_opcode_add4/8/16, so a few (e.g. BIT &20, LDX/LDY-immediate
# &A2/&A0) are the slot value, not a legal standalone opcode.
ASM_BASE_OPCODES = [
    0x16,                                                          # &00 padding
    0x00, 0x18, 0xd8, 0x58, 0xb8, 0xca, 0x88, 0xe8, 0xc8, 0xea,
    0x48, 0x08, 0x68, 0x28, 0x40, 0x60, 0x38, 0xf8, 0x78,
    0xaa, 0xa8, 0xba, 0x8a, 0x9a, 0x98,
    0x90, 0xb0, 0xf0, 0x30, 0xd0, 0x10, 0x50, 0x70,
    0x21, 0x41, 0x01, 0x61, 0xc1, 0xa1, 0xe1,
    0x06, 0x46, 0x26, 0x66,
    0xc6, 0xe6,
    0xe0, 0xc0,
    0x20,
    0x4c, 0x20,
    0xa2, 0xa0, 0x81,
    0x86, 0x84,
]


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

# Shared calling conventions for the dispatched handlers.
#
# Every keyword handler is reached through the indirect jump in
# dispatch_token (&8BB1): the token in A indexes the action-address
# table, the handler address is placed in zp_general (&37/&38) and
# JMP (&0037) enters the handler. The two families therefore share an
# entry/exit contract, established once here and applied to every
# table-generated banner; an individual HANDLER_INFO entry may override
# either dict (see below).
#
# stmt_* handlers run from statement_loop (&8B9B) / execute_line, reading
# the program through PtrA (zp_text_ptr, &0B/&0C; offset &0A). They run
# the statement and rejoin the interpreter loop without returning a value.
STMT_ON_ENTRY = {
    'A': 'the statement keyword token (>= &C6)',
    'zp_text_ptr (&0B/&0C)': 'the program text pointer (PtrA)',
    'zp_text_ptr_off (&0A)': 'offset just past the keyword token',
}
STMT_ON_EXIT = {
    'control': 'rejoins statement_loop; no value, registers not preserved',
}
# fn_* handlers run from eval_factor (&ADEC) while evaluating an
# expression, reading through PtrB (zp_text_ptr2, &19/&1A; offset &1B).
# They consume their argument(s) and return a typed result.
FN_ON_ENTRY = {
    'A': 'the function keyword token (&8E-&C5)',
    'zp_text_ptr2 (&19/&1A)': 'the expression text pointer (PtrB)',
    'zp_text_ptr2_off (&1B)': 'offset just past the function token',
}
FN_ON_EXIT = {
    'A': 'result type: <0 = float in fwa, >0 = integer in iwa, 0 = string',
    'zp_iwa (&2A-&2D) / zp_fwa (&2E-&35) / string_work (&0600)':
        'the result, selected by the type in A',
    'zp_text_ptr2_off (&1B)': 'advanced past the consumed argument(s)',
}

# Optional (title, description) for individual handlers, attached when
# the handler is declared below. An entry may also carry on_entry /
# on_exit as a 3rd / 4th tuple element to override the shared family
# contract above (None = use the family default). The mathematical
# functions (Pharo ch. 5) each evaluate their argument into the
# floating-point accumulator then fall into a pure routine (argument
# already in FWA) a few bytes later, whose address is noted.
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
    'fn_to': ('TO', 'The TO keyword. "TO P" reads TOP, the end of the BASIC '
                    'program, as an integer; any other TO is a syntax error.'),
    'fn_asc': ('ASC', 'ASCII code of the first character of a string, or '
                      '-1 if empty. ASC string.'),
    'fn_len': ('LEN', 'Length of a string. LEN string.'),
    'fn_val': ('VAL',
               'Read a number from the start of a string, through the '
               'decimal reader only (ascii_to_number then parse_number): an '
               'optional leading sign, digits, a "." and an "E" exponent. It '
               'does NOT read "&" hex, so VAL("&FF") is 0; it stops at the '
               'first non-numeric character (VAL("12AB") is 12) and yields 0 '
               'when no number leads. Returns an integer (IWA) or a real '
               '(FWA). Contrast EVAL, which evaluates the whole string. '
               'VAL string.'),
    'fn_eval': ('EVAL',
                'Tokenise a string and evaluate it as a full BASIC '
                'expression. The argument is copied onto the stack, given a '
                'CR, tokenised in place (mid-statement, so PTR/TIME etc. '
                'tokenise as functions, not assignment targets) and run '
                'through the expression evaluator - so it accepts everything '
                'the evaluator does: "&" hex (factor_hex), "E"-exponent '
                'decimals, operators, parentheses, functions and in-scope '
                'variables. Hence EVAL("&FF") is 255 where VAL("&FF") is 0, '
                'though both read "1E3" as 1000. EVAL string.'),
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
    'stmt_endproc': ('ENDPROC', 'Return from a procedure. Checks a PROC frame '
                                'is present (the framed token at &01FF must be '
                                '&F2), then falls into the end-of-statement '
                                'path whose rts unwinds the frame back through '
                                'call_proc_fn (&B197) -- restoring LOCAL '
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

# Read the ROM so we can resolve each table entry to its handler address
# and declare it as a subroutine (which gives fantasm's call graph real
# structure). Several tokens share a handler (e.g. DATA and DEF both
# dispatch to the same "skip to end of line" routine), so declare each
# distinct target only once; the duplicate table entries render
# symbolically against the first declaration.
_rom_bytes = Path(_rom_filepath).read_bytes()
_declared_handlers: dict[int, str] = {}

# Keyword table runs from &8071 up to the action-address tables.
# Keyword/tokeniser table token addresses (&8071..&836C): the only bytes
# with bit 7 set are the token bytes, so each marks the end of a keyword's
# text and the start of its token + flag suffix.
KEYWORD_TOKEN_ADDRS = [_a for _a in range(0x8071, ACTION_TABLE_LO)
                       if _rom_bytes[_a - 0x8000] >= 0x80]
# --- expression evaluator: the operator-precedence ladder ------------
# eval_expr enters at the lowest precedence and each level calls the
# next-higher one for its operands, then applies its own operators in a
# loop. Each level returns the next (unconsumed) operator token in X and
# the result type in A / zp_var_type. Level 1 (eval_factor) handles
# unary operators, parentheses, literals and functions.
#
# Shared contract for the precedence-climbing levels (2-7): read the
# (sub)expression at PtrB and return a typed value plus the lookahead.
EVAL_LEVEL_ON_ENTRY = {
    'zp_text_ptr2 (&19/&1A)': 'PtrB at the (sub)expression to evaluate',
    'zp_text_ptr2_off (&1B)': 'offset into the text',
}
EVAL_LEVEL_ON_EXIT = {
    'A': 'result type: <0 = float in fwa, >0 = integer in iwa, 0 = string',
    'zp_iwa / zp_fwa / string_work (&0600)': 'the value, selected by the type in A',
    'X': 'the next unconsumed operator token (lookahead)',
    'zp_text_ptr2_off (&1B)': 'advanced past the consumed text',
}
# Macros that re-derive a packed-name hash byte from a mnemonic's three
# letters: the low 5 bits of each letter, packed MSB-first into a 15-bit
# key, then split into low (AND &FF) and high (DIV &100) halves. dasmos
# emits a real MACRO ... ENDMACRO per backend and one invocation per
# table entry, so the mnemonic string stays visible and verify proves
# each invocation assembles back to the original ROM byte.
_mnem = param("mnem")
_pack_key = group((_mnem[0] & 0x1F) * 0x400
                  + (_mnem[1] & 0x1F) * 0x20
                  + (_mnem[2] & 0x1F))
pack_mnemonic_lo = d.define_macro("pack_mnemonic_lo", ["mnem"], _pack_key & 0xFF)
pack_mnemonic_hi = d.define_macro("pack_mnemonic_hi", ["mnem"], _pack_key // 0x100)

d.set_file_header(
    title='Acorn BBC BASIC II',
    description=f"""Annotated disassembly of the BBC BASIC II interpreter ROM:
the 16 kB sideways language ROM mapped at &8000 on the BBC Micro.

Generated from the original ROM by a dasmos driver
(`versions/basic-2/disassemble/disasm_basic_2.py`) and reassembles
byte-for-byte to the original ROM. This file is generated - do not edit it by
hand. Edit the driver and regenerate with `fantasm disassemble 2`.

- Source ROM: {len(_rom_bytes)} bytes
- md5: `{hashlib.md5(_rom_bytes).hexdigest()}`
- sha256: `{hashlib.sha256(_rom_bytes).hexdigest()}`
""",
)


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
    rom_title='Acorn BBC BASIC II',
)
# Language-specific data types: registers the packed 5-byte
# floating-point type "bbc_float5" used for the REAL constant pool.
d.use_environment('bbc_basic_6502')

# ----------------------------------------------------------------------
# Zero page (Pharo ch. 7.1 "Zero Page Dedicated Locations"). All
# two-byte pointers are stored low byte first.
# ----------------------------------------------------------------------
d.label(0x0000, 'zp_lomem', length=2, group='zero_page', access='rw',
        description="""LOMEM: the start of variable storage. Defaults to [`TOP`](address:0012) when a program is run and grows upward as variables are created (tracked by [`VARTOP`](address:0002)); settable with `LOMEM=`.""")
d.label(0x0001, 'zp_lomem_1')
for _i in range(1, 5):
    d.label(0x046c + 5 * (_i - 1), f'fp_temp{_i}')  # FP TEMP1..TEMP4
d.label(0x0002, 'zp_vartop', length=2, group='zero_page', access='rw',
        description="""VARTOP: the address just past the last allocated variable — where the next new variable goes. Runs from [`LOMEM`](address:0000) up toward [`zp_stack_ptr`](address:0004); the two meeting is "No room".""")
d.label(0x0003, 'zp_vartop_1')
d.label(0x0004, 'zp_stack_ptr', length=2, group='zero_page', access='rw',
        description="""Pointer to the top of BASIC's value stack, which grows
downward from [`HIMEM`](address:0006). The stack carries expression
temporaries, strings pushed during evaluation, and — across a PROC/FN
call — a saved copy of the 6502 hardware stack. "No room" is raised if
it descends to meet [`VARTOP`](address:0002).""")
d.label(0x0005, 'zp_stack_ptr_1')
d.label(0x0006, 'zp_himem', length=2, group='zero_page', access='rw',
        description="""HIMEM: the top of memory available to BASIC. The value stack ([`zp_stack_ptr`](address:0004)) grows down from here; settable with `HIMEM=`. Read from the MOS (OSBYTE &84) at startup.""")
d.label(0x0007, 'zp_himem_1')
d.label(0x0008, 'zp_erl', length=2, group='zero_page', access='r',
        description="""ERL: the line number in which the last error occurred, set by the error handler and read by the `ERL` function (0 in immediate mode).""")
d.label(0x0009, 'zp_erl_1')
d.label(0x000a, 'zp_text_ptr_off', length=1, group='zero_page', access='rw',
        description="""PtrA offset: the offset of the next character within the program line addressed by [`zp_text_ptr`](address:000b). The interpreter reads the tokenised program through this pointer/offset pair.""")
d.label(0x000b, 'zp_text_ptr', length=2, group='zero_page', access='rw',
        description="""PtrA: the primary program/text pointer — the base address of the line currently being interpreted. Combined with [`zp_text_ptr_off`](address:000a) to fetch tokens.""")
d.label(0x000c, 'zp_text_ptr_1')
# RND work area (&0D-&11): a 33-bit LFSR state. &0D-&10 are a 32-bit
# little-endian value (bits 0-31); bit 0 of &11 is bit 32. See rnd_step.
d.label(0x000d, 'zp_rnd_seed', length=5, group='zero_page', access='rw',
        description="""RND state: the 33-bit linear-feedback shift register behind `RND`. &0D-&10 are a little-endian 32-bit value (bits 0-31); bit 0 of &11 is bit 32. Advanced 32 steps per `RND` call; reseeded by `RND(-n)`.""")
d.label(0x000e, 'zp_rnd_seed_1')      # LFSR bits 8-15
d.label(0x000f, 'zp_rnd_seed_2')      # LFSR bits 16-23
d.label(0x0010, 'zp_rnd_seed_3')      # LFSR bits 24-31
d.label(0x0011, 'zp_rnd_seed_4')      # LFSR bit 32 (in bit 0; overflow)
d.label(0x0012, 'zp_top', length=2, group='zero_page', access='rw',
        description="""TOP: the address just past the end of the tokenised program text (and the default for [`LOMEM`](address:0000)). Read by the `TOP` pseudo-variable and set when the program is edited.""")
d.label(0x0013, 'zp_top_1')
d.label(0x0014, 'zp_print_bytes', length=1, group='zero_page', access='rw',
        description="""Print field width: the @%-derived field width used while formatting a number for `PRINT`, counting the characters emitted so far in the current field.""")
d.label(0x0015, 'zp_print_flag', length=1, group='zero_page', access='rw',
        description="""Number-base flag for output: 0 selects decimal, negative selects hexadecimal (set by `STR$~` and `PRINT ~`).""")
d.label(0x0016, 'zp_error_vec', length=2, group='zero_page', access='rw',
        description="""`ON ERROR` handler address: where the interpreter jumps when an error is trapped. Reset to the default handler (&B433) at the start of each statement line; set by `ON ERROR`.""")
d.label(0x0017, 'zp_error_vec_1')
d.label(0x0018, 'zp_page', length=1, group='zero_page', access='r',
        description="""PAGE high byte: the start of the BASIC program as a page number (PAGE = this × 256). Read from OSHWM at startup; the `PAGE` pseudo-variable exposes it.""")
d.label(0x0019, 'zp_text_ptr2', length=2, group='zero_page', access='rw',
        description="""PtrB: the secondary text pointer, used by the expression evaluator and the tokeniser while [`zp_text_ptr`](address:000b) (PtrA) is preserved. Paired with [`zp_text_ptr2_off`](address:001b).""")
d.label(0x001a, 'zp_text_ptr2_1')
d.label(0x001b, 'zp_text_ptr2_off', length=1, group='zero_page', access='rw',
        description="""PtrB offset: the offset of the next character for the secondary text pointer [`zp_text_ptr2`](address:0019).""")
d.label(0x001c, 'zp_data_ptr', length=2, group='zero_page', access='rw',
        description="""DATA pointer: the address of the next `DATA` item to be `READ`. Set to the program start by `RESTORE` (or a line by `RESTORE n`) and advanced as items are read.""")
d.label(0x001d, 'zp_data_ptr_1')
d.label(0x001e, 'zp_count', length=1, group='zero_page', access='rw',
        description="""COUNT: the number of characters printed since the last newline (the print column). Used for `,` field alignment and the `WIDTH` auto-newline; read by the `COUNT` function.""")
d.label(0x001f, 'zp_listo', length=1, group='zero_page', access='rw',
        description="""LISTO flags: the listing-indent options set by `LISTO n`. Control whether `LIST` indents `FOR`/`REPEAT` bodies and spaces tokens.""")
d.label(0x0020, 'zp_trace_flag', length=1, group='zero_page', access='rw',
        description="""TRACE flag: &00 = tracing off, &FF = on (`TRACE ON`/`TRACE OFF`). When on, executed line numbers are printed in brackets up to [`zp_trace_max`](address:0021).""")
d.label(0x0021, 'zp_trace_max', length=2, group='zero_page', access='rw',
        description="""TRACE ceiling: the highest line number that `TRACE` reports (`TRACE n`). Lines above it are not traced.""")
# workspace / zero-page and FOR/REPEAT/GOSUB frame-field labels
d.label(0x0022, 'zp_trace_max_1')
d.label(0x0023, 'zp_width', length=1, group='zero_page', access='rw',
        description="""WIDTH: the print line width for the auto-newline (`WIDTH n`). &FF (the default) means no automatic wrap; compared against [`zp_count`](address:001e).""")
d.label(0x0024, 'zp_repeat_level', length=1, group='zero_page', access='rw',
        description="""REPEAT stack depth: how many `REPEAT` loops are open, indexing [`repeat_stack`](address:05a4). Not saved across a PROC/FN call, so leaving a loop via `ENDPROC`/`GOTO` leaks its entry.""")
d.label(0x0025, 'zp_gosub_level', length=1, group='zero_page', access='rw',
        description="""GOSUB stack depth: how many `GOSUB` calls are open, indexing [`gosub_stack`](address:05cc). Not saved across a PROC/FN call.""")
d.label(0x0026, 'zp_for_level', length=1, group='zero_page', access='rw',
        description="""FOR stack depth: how many `FOR` loops are open (×15 gives the byte offset into [`for_stack`](address:0500)). Not saved across a PROC/FN call.""")
d.label(0x0027, 'zp_var_type', length=1, group='zero_page', access='rw',
        description="""Value type of the most recently fetched/evaluated value: 0 = string, positive (&40) = integer, negative = real. Drives the type dispatch throughout the evaluator.""")
d.label(0x0028, 'zp_opt_flag', length=1, group='zero_page', access='rw',
        description="""Inline-assembler OPT flags (`OPT n`): bit 0 prints a listing, bit 1 enables error reporting, bit 2 assembles to the offset address O% instead of P%. &FF outside `[ ]` marks "not assembling".""")
d.label(0x0029, 'zp_asm_opcode', length=1, group='zero_page', access='rw',
        description="""Inline assembler: the opcode byte being built for the instruction currently being assembled, before its operand bytes are appended.""")

# Zero page (Pharo ch. 7.2 "Zero Page Multiple Use Locations"). These
# overlap by design; the labels mark each region's primary use.
# Integer work area / accumulator (IWA): 32-bit signed, little-endian.
d.label(0x002a, 'zp_iwa', length=4, group='zero_page', access='rw',
        description="""IWA — the 32-bit integer work accumulator. Holds the integer operand/result of the evaluator and the integer arithmetic primitives, and doubles as a pointer to a variable’s value during a fetch.""")
d.label(0x002b, 'zp_iwa_1')
d.label(0x002c, 'zp_iwa_2')
d.label(0x002d, 'zp_iwa_3')           # IWA byte 3 (most significant)
# Floating point work area A (FWA), the unpacked 8-byte accumulator.
d.label(0x002e, 'zp_fwa_sign', length=8, group='zero_page', access='rw',
        description="""FWA — floating-point work accumulator A (&2E-&35): sign (&2E), overflow/guard (&2F), excess-128 exponent (&30), 32-bit mantissa MSB-first (&31-&34) and a rounding byte (&35). The main register for real arithmetic; see [`zp_fwb_sign`](address:003b).""")
d.label(0x002f, 'zp_fwa_ovf')         # Overflow / guard byte
d.label(0x0030, 'zp_fwa_exp')         # Exponent (excess-128; 0 = value 0)
d.label(0x0031, 'zp_fwa_m1')          # Mantissa MSB (normalised: bit 7 = 1)
d.label(0x0032, 'zp_fwa_m2')
d.label(0x0033, 'zp_fwa_m3')
d.label(0x0034, 'zp_fwa_m4')          # Mantissa LSB
d.label(0x0035, 'zp_fwa_rnd')         # Rounding byte (extra precision)
d.label(0x0036, 'zp_strbuf_len', length=1, group='zero_page', access='rw',
        description="""Length of the string currently in the string work area at [`string_work`](address:0600).""")
d.label(0x0037, 'zp_general', length=2, group='zero_page', access='rw',
        description="""General-purpose work pointer (&37-&3A). Reused widely — the tokeniser/line scanner, the variable-chain walk, the program editor — as a scratch 16-bit pointer.""")
d.label(0x0038, 'zp_general_1')       # general pointer high byte
d.label(0x0039, 'zp_fileblk', length=2, group='zero_page', access='rw',
        description="""Filing-system control block (&39 onward): the OSFILE / load-save parameter block. Filing is not active during arithmetic, so this overlaps the FP workspace below ([`zp_fwb_sign`](address:003b) onward).""")
d.label(0x003a, 'zp_fileblk_1')
# Floating point work area B (FWB), same layout as FWA.
d.label(0x003b, 'zp_fwb_sign', length=8, group='zero_page', access='rw',
        description="""FWB — floating-point work accumulator B (&3B-&42), same layout as [`zp_fwa_sign`](address:002e). Supplies the second operand for binary floating-point operations (add, multiply, divide).""")
d.label(0x003c, 'zp_fwb_ovf',
        description="""FWB overflow byte (&3C), part of [`zp_fwb_sign`](address:003b). A much-reused scratch location: outside floating point it serves as the tokeniser's line-number-arming flag (&FF after GOTO etc. means encode the next number as a line number), a variable-chain walk pointer, an array dimension-descriptor offset, and LIST's REPEAT/UNTIL indent counter. Read each use in its own context rather than assuming a single global meaning.""")
d.label(0x003d, 'zp_fwb_exp')
d.label(0x003e, 'zp_fwb_m1')
d.label(0x003f, 'zp_fwb_m2')
d.label(0x0040, 'zp_fwb_m3')
d.label(0x0041, 'zp_fwb_m4')
d.label(0x0042, 'zp_fwb_rnd')
d.label(0x0043, 'zp_fp_temp', length=5, group='zero_page', access='rw',
        description="""Floating-point temporary / scratch (&43-&47). Holds spill bytes for the FP routines and serves as the quotient build area for integer `DIV`/`MOD`.""")
d.label(0x0044, 'zp_fp_temp_1')
d.label(0x0045, 'zp_fp_temp_2')
d.label(0x0046, 'zp_fp_temp_3')
d.label(0x0047, 'zp_fp_temp_4')
d.label(0x0048, 'zp_dp_flag', length=1, group='zero_page', access='rw',
        description="""Decimal-point-seen flag, set while parsing a number literal so a second `.` is rejected and the fractional digits are scaled.""")
d.label(0x0049, 'zp_dec_exp', length=1, group='zero_page', access='rw',
        description="""Decimal exponent accumulated while parsing the `E` part of a real literal.""")
d.label(0x004a, 'zp_int_exp', length=1, group='zero_page', access='rw',
        description="""Integer-part / exponent scratch: holds the integer exponent during number parsing and the integer part of a value in `EXP` and the int/fraction split.""")
d.label(0x004b, 'zp_fp_ptr', length=2, group='zero_page', access='rw',
        description="""Pointer to a packed 5-byte floating-point value (a variable or an FP temporary) for the pack/unpack routines.""")
d.label(0x004c, 'zp_fp_ptr_1')        # (high byte; used by the FP routines)
d.label(0x004d, 'zp_coeff_ptr', length=2, group='zero_page', access='rw',
        description="""Pointer to the current coefficient table, used while evaluating the continued-fraction approximations in the trig functions.""")
d.label(0x004e, 'zp_coeff_ptr_1')
d.label(0x00fd, 'zp_error_ptr', length=2, group='zero_page', access='rw',
        description="""Pointer to the error block currently being reported (the bytes after a `BRK`): the error number and message the handler is processing.""")

d.label(0x00ff, 'zp_escflg', length=1, group='zero_page', access='rw',
        description="""ESCFLG — the MOS escape flag. Its top bit is set when Escape is pressed; BASIC polls it between statements, acknowledges it via OSBYTE, and raises the "Escape" error.""")
d.label(0x0100, 'hw_stack', length=256, group='stack_6502', access='rw',
        description="""The 6502 hardware stack (page 1), used normally for JSR/RTS and register saves. A PROC/FN call copies a snapshot of the live stack onto the BASIC value stack and restores it on return, so call nesting is bounded by free stack space rather than a fixed table.""")
d.index_base(0x0106, 'frame_local_count')
d.label(0x01ff, 'hw_stack_top')
# ----------------------------------------------------------------------
# Page 4 / 5 / 6 / 7 RAM workspace (Pharo ch. 7.3-7.6).
# ----------------------------------------------------------------------
d.label(0x0400, 'resint_at', length=108, group='resident_vars', access='rw',
        description="""The resident integer variables, four bytes each: @% here at &0400, then A%-Z% at &0404-&046B. @% sets the `PRINT`/`STR$` number format. Two slots double as the inline assembler's counters — O% (the 'O' slot, &043C) is the offset-assembly address and P% (the 'P' slot, &0440) the program counter.""")
d.label(0x0401, 'resint_at_1')
d.label(0x0402, 'resint_at_2')
d.label(0x0403, 'resint_at_3')
for _i, _name in enumerate('abcdefghijklmnopqrstuvwxyz'):
    d.label(0x0404 + 4 * _i, f'resint_{_name}')  # A%..Z%
d.label(0x043d, 'resint_o_1')
d.label(0x0441, 'resint_p_1')
d.label(0x046c, 'fp_temps', length=20, group='resident_vars', access='rw',
        description="""Four 5-byte packed floating-point temporaries: TEMP1 (&046C), TEMP2 (&0471), TEMP3 (&0476) and TEMP4 (&047B). The maths routines stash intermediate reals here while reusing [`FWA`](address:002e) / [`FWB`](address:003b).""")

d.index_base(0x047f, 'var_table_base')
d.label(0x0480, 'var_ptr_table', length=128, group='resident_vars', access='rw',
        description="""The dynamic-variable chain-head table: a two-byte head pointer per initial-character class (A-Z, a-z, `_`, `@`), addressed as &0400 + 2×char. find_variable walks the linked list of variables sharing an initial character; create_variable links a new one in at the head.""")
d.index_base(0x04f1, 'for_var_lo')
d.index_base(0x04f2, 'for_var_hi')
d.index_base(0x04f3, 'for_type')
d.index_base(0x04f4, 'for_step0')
d.index_base(0x04f5, 'for_step1')
d.index_base(0x04f6, 'for_step2')
d.index_base(0x04f7, 'for_step3')
d.index_base(0x04f9, 'for_limit0')
d.index_base(0x04fa, 'for_limit1')
d.index_base(0x04fb, 'for_limit2')
d.index_base(0x04fc, 'for_limit3')
d.index_base(0x04fe, 'for_loopback_lo')
d.index_base(0x04ff, 'for_loopback_hi')
# Control-flow stacks (page 5). Three independent LIFO arrays, one per
# loop construct, each indexed by its own zero-page level counter:
#   for_stack    &0500  15-byte frames, counter zp_for_level    (&26)
#   repeat_stack &05A4   2-byte frames, counter zp_repeat_level (&24)
#   gosub_stack  &05CC   2-byte frames, counter zp_gosub_level  (&25)
# These are distinct from the 6502 hardware stack and the BASIC value
# stack, and -- unlike those two -- are NOT saved/restored across a
# PROC/FN call. See call_proc_fn (&B197).
d.index_base(0x0500, 'for_stack', length=150, group='basic_stacks',
        description="""The `FOR` stack: up to 10 frames of 15 bytes each (&0500-&0595; depth in [`zp_for_level`](address:0026)). Each frame holds the control-variable address and type, the STEP and limit values, and the loop-back text pointer — pushed by `FOR`, consulted and updated by `NEXT`.""")
d.index_base(0x0501, 'for_set_ptr_hi')
d.index_base(0x0502, 'for_set_type')
d.index_base(0x0503, 'for_set_step0')
d.index_base(0x0504, 'for_set_step1')
d.index_base(0x0505, 'for_set_step2')
d.index_base(0x0506, 'for_set_step3')
d.index_base(0x0508, 'for_set_limit0')
d.index_base(0x0509, 'for_set_limit1')
d.index_base(0x050a, 'for_set_limit2')
d.index_base(0x050b, 'for_set_limit3')
d.index_base(0x050d, 'for_set_loop_lo')
d.index_base(0x050e, 'for_set_loop_hi')
d.index_base(0x05a3, 'repeat_loop_lo')
d.index_base(0x05a4, 'repeat_stack', length=20, group='basic_stacks',
        description="""`REPEAT` loop-start text pointers, low bytes — up to 20 nested (depth in [`zp_repeat_level`](address:0024)); high bytes in [`repeat_stack_hi`](address:05b8). `UNTIL` reloads the pointer to re-test its condition.""")
d.index_base(0x05b7, 'repeat_loop_hi')
d.index_base(0x05b8, 'repeat_stack_hi', length=20, group='basic_stacks',
        description="""High bytes of the `REPEAT` loop-start pointers; low bytes in [`repeat_stack`](address:05a4).""")
d.index_base(0x05cb, 'gosub_return_lo')
d.index_base(0x05cc, 'gosub_stack', length=26, group='basic_stacks',
        description="""`GOSUB` return text pointers, low bytes — up to 26 nested (depth in [`zp_gosub_level`](address:0025)); high bytes in [`gosub_stack_hi`](address:05e6). `RETURN` pops the top entry.""")
d.index_base(0x05e5, 'gosub_return_hi')
d.index_base(0x05e6, 'gosub_stack_hi', length=26, group='basic_stacks',
        description="""High bytes of the `GOSUB` return pointers; low bytes in [`gosub_stack`](address:05cc).""")
d.index_base(0x05ff, 'strbuf_base')
d.label(0x0600, 'string_work', length=256, group='buffers', access='rw',
        description="""The string work area / `CALL` parameter block. BASIC builds string results here — the text of `STR$`, the digits of a number conversion, a popped string for comparison — with the length in [`zp_strbuf_len`](address:0036). `CALL` also assembles its parameter block here.""")
d.label(0x06ff, 'call_block_base')

d.label(0x0700, 'line_input_buf', length=256, group='buffers', access='rw',
        description="""The line input buffer. The line editor reads a typed line (at the `>` prompt or for `INPUT`) into here via OSWORD 0; the tokeniser then processes it in place.""")

# language_entry (&8000): the ROM language entry point.
d.comment(0x8000, 'A=1: language start?', align=Align.INLINE)
d.comment(0x8002, 'yes: start BASIC', align=Align.INLINE)
d.comment(0x8004, 'otherwise return', align=Align.INLINE)

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
    on_entry={'A': '1 (MOS language-start reason code)'},
    on_exit={'zp_himem (&06/&07) / zp_page (&18)': 'read from the MOS',
             'control': 'jumps to start_new_program (does not return)'},
)

# language_startup (&8023) remaining
d.comment(0x8023, 'OSBYTE &84: read HIMEM', align=Align.INLINE)
d.comment(0x802a, 'HIMEM high byte', align=Align.INLINE)
d.comment(0x802c, 'OSBYTE &83: read OSHWM (PAGE)', align=Align.INLINE)
d.comment(0x8033, 'X = 0', align=Align.INLINE)
d.comment(0x8035, 'LISTO = 0: no LIST indentation', align=Align.INLINE)
d.comment(0x8037, '@% high two bytes = 0', align=Align.INLINE)
d.comment(0x803a, '@% byte 3 = 0', align=Align.INLINE)
d.comment(0x803d, 'X = &FF', align=Align.INLINE)
d.comment(0x803e, 'WIDTH = &FF: no automatic line wrap', align=Align.INLINE)
d.comment(0x8040, '@% = &0000090A: byte 0 = &0A', align=Align.INLINE)
d.comment(0x8042, '@% = &0000090A: default PRINT format', align=Align.INLINE)
d.comment(0x8045, 'X = &09', align=Align.INLINE)
d.comment(0x8046, '@% byte 1 = &09', align=Align.INLINE)
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
    'area is zero, so a fixed seed is installed here. The three\n'
    "bytes &41/&52/&57 are the ASCII codes of Wilson's initials,\n"
    "a nod to BBC BASIC's author. Nothing else re-seeds unless the\n"
    'program calls RND(-n), so a sequence is deterministic from a\n'
    'cold start.',
    word_wrap=False,
)
d.comment(0x8057, 'Cold seed: state becomes &00575241; load &41',
          align=Align.INLINE)
d.char_literal(0x8058)
d.comment(0x8059, 'byte 0', align=Align.INLINE)
d.comment(0x805b, 'load &52', align=Align.INLINE)
d.char_literal(0x805c)
d.comment(0x805d, 'byte 1', align=Align.INLINE)
d.comment(0x805f, 'load &57', align=Align.INLINE)
d.char_literal(0x8060)
d.comment(0x8061, 'byte 2 (bytes 3 and 4 stay zero)', align=Align.INLINE)
d.comment(0x8063, 'Install brk_handler (&B402) into BRKV', align=Align.INLINE)
d.label(0x8063, 'lang_install_brkv')
d.comment(0x8065, '(BRKV low)', align=Align.INLINE)
d.comment(0x8068, 'high byte &B4', align=Align.INLINE)
d.comment(0x806a, '(BRKV high)', align=Align.INLINE)
d.comment(0x806d, 'Enable IRQs and enter the immediate loop', align=Align.INLINE)

d.comment(0x806e, 'Enter via NEW and the immediate loop', align=Align.INLINE)
# ----------------------------------------------------------------------
# Keyword / token table (Pharo ch. 7.7). Each entry is the keyword text
# in ASCII, a token byte (bit 7 set), and a tokeniser flag byte.
# ----------------------------------------------------------------------
d.subroutine(
    0x8071, 'keyword_table',
    is_entry_point=False,   # data table: banner only, do not trace as code
    title='Keyword / tokeniser table',
    description="""Each entry is the keyword in ASCII, then a token byte (bit 7
set), then a flag byte that drives tokenising. The flag bits are:

| Bit | Meaning |
|-----|---------|
| 0 | Conditional: do not tokenise if followed by a name char (0-9 A-Z a-z _) |
| 1 | Enter "middle of statement" mode |
| 2 | Enter "start of statement" mode |
| 3 | FN/PROC: do not tokenise the following name |
| 4 | Start tokenising a line number (after GOTO etc.) |
| 5 | Do not tokenise the rest of the line (REM, DATA) |
| 6 | Pseudo-variable: add &40 to the token in a statement |

Bit 6 is why a pseudo-variable like PTR reads as &8F in a function
position but &CF as an assignment target. Entries are ordered so that
the first acceptable abbreviation of each keyword is unambiguous.

The tokeniser scan stops at WIDTH's token &FE, which doubles as the
end-of-table sentinel (see the `cmp #&fe` in the keyword search). The
final five entries — the PTR/PAGE/TIME/LOMEM/HIMEM *assignment* forms
&CF-&D3 — sit past that sentinel, so the tokeniser never matches them
(it produces those tokens arithmetically via bit 6). They exist only
for the de-tokeniser (`print_token`, which has no sentinel and scans by
token value) to render `PTR=` etc. back to text. The data then runs on
to the action-address tables at action_table_lo.
""",
)

# Declare each keyword entry's structure explicitly: EQUS "<keyword>" then
# EQUB <token>, <flag>. dasmos's auto string-detection otherwise merges a
# printable flag byte into the following keyword's text (DATA's &20 becomes
# " DEG"; HIMEM/LOMEM/PAGE/PTR/TIME's &43 prefixes 'C' to the next keyword;
# REM's &20 likewise), which also makes short keywords (FN, IF, LN) look
# missing. Each keyword's text runs from the previous suffix to its token.
for _kw_i, _kw_tok in enumerate(KEYWORD_TOKEN_ADDRS):
    _kw_text = 0x8071 if _kw_i == 0 else KEYWORD_TOKEN_ADDRS[_kw_i - 1] + 2
    d.string(_kw_text, _kw_tok - _kw_text, override=True)  # EQUS "<keyword>"
    d.byte(_kw_tok, 2, override=True)                      # EQUB <token>, <flag>

d.label(ACTION_TABLE_LO, 'action_table_lo')
d.label(ACTION_TABLE_HI, 'action_table_hi')

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
    _is_fn = _name.startswith('fn_')
    _info = HANDLER_INFO.get(_name)
    # Apply the shared family contract, allowing per-entry overrides via
    # the optional 3rd / 4th tuple elements (None = use the default).
    _on_entry = FN_ON_ENTRY if _is_fn else STMT_ON_ENTRY
    _on_exit = FN_ON_EXIT if _is_fn else STMT_ON_EXIT
    if _info and len(_info) >= 3 and _info[2] is not None:
        _on_entry = _info[2]
    if _info and len(_info) >= 4 and _info[3] is not None:
        _on_exit = _info[3]
    if _info:
        d.subroutine(_target, _name, title=_info[0], description=_info[1],
                     on_entry=_on_entry, on_exit=_on_exit)
    else:
        d.subroutine(_target, _name, on_entry=_on_entry, on_exit=_on_exit)
    _declared_handlers[_target] = _name

d.subroutine(
    0x84fd, 'assembler_exit',
    title='Finish the inline assembler',
    description="""Leave the inline 6502 assembler (reached at "]"): set the OPT
flag to &FF (not assembling) and jump back into the statement
interpreter.
""",
    on_exit={'zp_opt_flag (&28)': '&FF (BASIC mode, not assembling)',
             'control': 'resumes the statement interpreter (does not return)'},
)
# ----------------------------------------------------------------------
# Inline assembler driver (&84FD): the [ ... ] block.
# Assembles each instruction, and when OPT bit 1 is set prints the
# listing line (P% in hex, the assembled bytes, the source text).
# ----------------------------------------------------------------------
d.comment(0x84fd, 'Leaving the assembler: OPT = BASIC mode', align=Align.INLINE)
d.comment(0x84ff, 'store &FF (not assembling)', align=Align.INLINE)
d.comment(0x8501, 'resume execution', align=Align.INLINE)
d.comment(0x8504, 'Entering: default OPT 3', align=Align.INLINE)
d.subroutine(
    0x8504, 'asm_enter',
    title='Enter the inline assembler',
    description="""Reached by the `jmp asm_enter` at &8B44, in
check_eq_star_bracket, when a "[" opens an assembler block. Sets the
default OPT 3 (listing + error reporting, assemble to P%) and falls
into asm_loop, which assembles one instruction or directive per
statement, optionally lists it, and advances. The loop runs until "]"
(-> assembler_exit, back to the interpreter) or the end of the program
(-> immediate_loop). Does not return.
""",
    on_exit={'control': 'does not return; exits to assembler_exit on "]" '
                        'or immediate_loop at end of program'},
)
d.comment(0x8506, 'store it', align=Align.INLINE)
d.comment(0x8508, 'Skip spaces', align=Align.INLINE)
d.label(0x8508, 'asm_loop')
d.comment(0x850b, "']' end of assembler?", align=Align.INLINE)
d.char_literal(0x850c)
d.comment(0x850d, 'yes: exit', align=Align.INLINE)
d.comment(0x850f, 'Skip to the statement', align=Align.INLINE)
d.comment(0x8512, 'back up', align=Align.INLINE)
d.comment(0x8514, 'Assemble one instruction', align=Align.INLINE)
d.comment(0x8517, 'back up', align=Align.INLINE)
d.comment(0x8519, 'OPT listing bit set?', align=Align.INLINE)
d.comment(0x851b, 'shift the list bit into carry', align=Align.INLINE)
d.comment(0x851c, 'no: skip the listing', align=Align.INLINE)
d.comment(0x851e, 'Column for the source text', align=Align.INLINE)
d.comment(0x8520, 'COUNT + 4,', align=Align.INLINE)
d.comment(0x8522, 'source column (&3F)', align=Align.INLINE)
d.comment(0x8524, 'Print P% high', align=Align.INLINE)
d.comment(0x8526, 'as two hex digits', align=Align.INLINE)
d.comment(0x8529, 'Print P% low', align=Align.INLINE)
d.comment(0x852b, 'as two hex digits', align=Align.INLINE)
d.comment(0x852e, 'Byte count', align=Align.INLINE)
d.comment(0x8530, 'String (EQUS) length?', align=Align.INLINE)
d.comment(0x8532, 'not EQUS: use the byte count,', align=Align.INLINE)
d.comment(0x8534, 'EQUS: use the string length', align=Align.INLINE)
d.comment(0x8536, 'Bytes to list', align=Align.INLINE)
d.label(0x8536, 'asm_list_count')
d.comment(0x8538, 'none', align=Align.INLINE)
d.comment(0x853a, 'From byte 0', align=Align.INLINE)
d.comment(0x853c, 'Count printed on this line', align=Align.INLINE)
d.label(0x853c, 'asm_list_byte_loop')
d.comment(0x853d, 'still on the line', align=Align.INLINE)
d.comment(0x853f, 'Newline and indent for a continuation', align=Align.INLINE)
d.comment(0x8542, 'indent to the hex column', align=Align.INLINE)
d.comment(0x8544, 'Print a space', align=Align.INLINE)
d.label(0x8544, 'asm_list_indent_loop')
d.comment(0x8547, 'one fewer space', align=Align.INLINE)
d.comment(0x8548, 'loop', align=Align.INLINE)
d.comment(0x854a, 'reset the per-line count', align=Align.INLINE)
d.comment(0x854c, 'Assembled byte', align=Align.INLINE)
d.label(0x854c, 'asm_list_byte')
d.comment(0x854e, 'print it as hex', align=Align.INLINE)
d.comment(0x8551, 'next', align=Align.INLINE)
d.comment(0x8552, 'all bytes?', align=Align.INLINE)
d.comment(0x8554, 'no: continue', align=Align.INLINE)
d.comment(0x8556, 'Pad to the source column', align=Align.INLINE)
d.label(0x8556, 'asm_list_pad_loop')
d.comment(0x8557, 'done', align=Align.INLINE)
d.comment(0x8559, 'print a space', align=Align.INLINE)
d.comment(0x855c, 'two more spaces,', align=Align.INLINE)
d.comment(0x855f, '(continued)', align=Align.INLINE)
d.comment(0x8562, 'loop', align=Align.INLINE)
d.comment(0x8565, 'Print the source: from offset 0', align=Align.INLINE)
d.label(0x8565, 'asm_list_source')
d.comment(0x8567, 'Next character', align=Align.INLINE)
d.label(0x8567, 'asm_list_src_loop')
d.comment(0x8569, "':' end of statement?", align=Align.INLINE)
d.char_literal(0x856a)
d.comment(0x856b, 'yes', align=Align.INLINE)
d.comment(0x856d, 'end of line?', align=Align.INLINE)
d.comment(0x856f, 'yes', align=Align.INLINE)
d.comment(0x8571, 'de-tokenise and print', align=Align.INLINE)
d.label(0x8571, 'asm_list_src_print')
d.comment(0x8574, 'next', align=Align.INLINE)
d.comment(0x8575, 'loop', align=Align.INLINE)
d.comment(0x8577, 'reached the statement end?', align=Align.INLINE)
d.label(0x8577, 'asm_list_src_end')
d.comment(0x8579, 'no: continue', align=Align.INLINE)
d.comment(0x857b, 'Newline', align=Align.INLINE)
d.label(0x857b, 'asm_list_newline')
d.comment(0x857e, 'Advance to the next statement', align=Align.INLINE)
d.label(0x857e, 'asm_next_statement')
d.comment(0x8580, 'back up (loop pre-increments)', align=Align.INLINE)
d.comment(0x8581, 'scan for the end', align=Align.INLINE)
d.label(0x8581, 'asm_scan_end_loop')
d.comment(0x8582, 'read a character', align=Align.INLINE)
d.comment(0x8584, "':'?", align=Align.INLINE)
d.char_literal(0x8585)
d.comment(0x8586, 'yes', align=Align.INLINE)
d.comment(0x8588, 'end of line?', align=Align.INLINE)
d.comment(0x858a, 'no: continue', align=Align.INLINE)
d.comment(0x858c, 'Check Escape and advance', align=Align.INLINE)
d.label(0x858c, 'asm_stmt_end')
d.comment(0x858f, 'Re-read the terminator', align=Align.INLINE)
d.comment(0x8590, 'read it', align=Align.INLINE)
d.comment(0x8592, "':'?", align=Align.INLINE)
d.char_literal(0x8593)
d.comment(0x8594, 'yes: same line', align=Align.INLINE)
d.comment(0x8596, 'at end of program memory?', align=Align.INLINE)
d.comment(0x8598, 'page &07 (immediate buffer)?', align=Align.INLINE)
d.comment(0x859a, 'no: next line', align=Align.INLINE)
d.comment(0x859c, 'yes: immediate mode', align=Align.INLINE)
d.comment(0x859f, 'Move to the next line', align=Align.INLINE)
d.label(0x859f, 'asm_next_line')
d.comment(0x85a2, 'continue assembling', align=Align.INLINE)
d.label(0x85a2, 'asm_continue')
d.comment(0x85a5, 'Label: parse the variable', align=Align.INLINE)
d.label(0x85a5, 'asm_define_label')

d.comment(0x85a8, 'end: error', align=Align.INLINE)
d.comment(0x85aa, 'indirection: error', align=Align.INLINE)
d.comment(0x85ac, 'stack the address', align=Align.INLINE)
d.comment(0x85af, 'value = P%', align=Align.INLINE)
d.comment(0x85b2, 'integer type', align=Align.INLINE)
d.comment(0x85b4, 'assign P% to the label', align=Align.INLINE)
d.comment(0x85b7, 'sync the pointer', align=Align.INLINE)

d.subroutine(0x85ba, 'asm_parse_mnemonic',
             title='Parse and compact an assembler mnemonic',
             description='Skip to the mnemonic at PtrA, handling end-of-statement '
                         'and labels, then pack its three letters (5 bits each) '
                         'into &3D/&3E for the opcode-table lookup.',
             on_entry={'zp_text_ptr (&0B/&0C)': 'the source pointer (PtrA)',
                       'zp_text_ptr_off (&0A)': 'offset of the next character'},
             on_exit={'zp_fwb_exp (&3D/&3E)': 'the three letters packed 5 bits each',
                      'zp_text_ptr_off (&0A)': 'advanced past the mnemonic'})
# asm_parse_mnemonic (&85BA): compact three letters into &3D/&3E.
d.comment(0x85ba, 'Three characters', align=Align.INLINE)
d.comment(0x85bc, 'Skip spaces', align=Align.INLINE)
d.comment(0x85bf, 'Clear the compacted value', align=Align.INLINE)
d.comment(0x85c1, 'low byte (&3D)', align=Align.INLINE)
d.comment(0x85c3, "':' end of statement?", align=Align.INLINE)
d.char_literal(0x85c4)
d.comment(0x85c5, 'yes: no instruction', align=Align.INLINE)
d.comment(0x85c7, 'end of line?', align=Align.INLINE)
d.comment(0x85c9, 'yes', align=Align.INLINE)
d.comment(0x85cb, 'comment?', align=Align.INLINE)
d.char_literal(0x85cc)
d.comment(0x85cd, 'yes', align=Align.INLINE)
d.comment(0x85cf, "'.' label?", align=Align.INLINE)
d.char_literal(0x85d0)
d.comment(0x85d1, 'yes: define it', align=Align.INLINE)
d.comment(0x85d3, 'back up', align=Align.INLINE)
d.comment(0x85d5, 'Next character', align=Align.INLINE)
# asm_parse_mnemonic internals
d.label(0x85d5, 'asm_mn_char_loop')
d.comment(0x85d7, 'advance the offset,', align=Align.INLINE)
d.comment(0x85d9, 'read it', align=Align.INLINE)
d.comment(0x85db, 'token: tokenised AND/EOR/OR', align=Align.INLINE)
d.comment(0x85dd, 'space?', align=Align.INLINE)
d.char_literal(0x85de)
d.comment(0x85df, 'skip it', align=Align.INLINE)
d.comment(0x85e1, 'Compact the character (5 bits)', align=Align.INLINE)
d.comment(0x85e3, 'shift the char up by 3,', align=Align.INLINE)
d.comment(0x85e4, '(continued)', align=Align.INLINE)
d.comment(0x85e5, '(continued)', align=Align.INLINE)
d.comment(0x85e6, 'shift into the value', align=Align.INLINE)
d.label(0x85e6, 'asm_mn_pack_loop')
d.comment(0x85e7, 'carry into &3D,', align=Align.INLINE)
d.comment(0x85e9, 'and &3E,', align=Align.INLINE)
d.comment(0x85eb, 'next bit,', align=Align.INLINE)
d.comment(0x85ec, 'all 5 bits', align=Align.INLINE)
d.comment(0x85ee, 'next character', align=Align.INLINE)
d.comment(0x85ef, 'loop for three', align=Align.INLINE)

# Assembler opcode-table match (&85F1) and tokenised AND/EOR/OR.
d.comment(0x85f1, 'Point to the end of the opcode table', align=Align.INLINE)
d.label(0x85f1, 'asm_mn_search')
d.comment(0x85f3, 'Compacted mnemonic low byte', align=Align.INLINE)
d.comment(0x85f5, 'Compare the low half', align=Align.INLINE)
d.label(0x85f5, 'asm_mn_search_loop')
d.expr(0x85f6, ref(ASM_MNEMONIC_LO) - 1)   # cmp asm_mnemonic_lo-1,x (1-based)
d.comment(0x85f8, 'no match: next entry', align=Align.INLINE)
d.comment(0x85fa, 'High half', align=Align.INLINE)
d.expr(0x85fb, ref(ASM_MNEMONIC_HI) - 1)   # ldy asm_mnemonic_hi-1,x (1-based)
d.comment(0x85fd, 'match the high half?', align=Align.INLINE)
d.comment(0x85ff, 'matched', align=Align.INLINE)
d.comment(0x8601, 'Next entry', align=Align.INLINE)
d.label(0x8601, 'asm_mn_search_next')
d.comment(0x8602, 'loop', align=Align.INLINE)
d.comment(0x8604, 'not matched: Mistake', align=Align.INLINE)
d.label(0x8604, 'asm_mistake')
d.comment(0x8607, "opcode index for AND", align=Align.INLINE)
d.label(0x8607, 'asm_logic_mnemonic')
d.comment(0x8609, 'tokenised AND?', align=Align.INLINE)
d.comment(0x860b, 'yes', align=Align.INLINE)
d.comment(0x860d, 'EOR index', align=Align.INLINE)
d.comment(0x860e, 'tokenised EOR?', align=Align.INLINE)
d.comment(0x8610, 'yes', align=Align.INLINE)
d.comment(0x8612, 'ORA index', align=Align.INLINE)
d.comment(0x8613, 'tokenised OR?', align=Align.INLINE)
d.comment(0x8615, 'no: Mistake', align=Align.INLINE)
d.comment(0x8617, "step past, expect 'A'", align=Align.INLINE)
d.comment(0x8619, 'advance,', align=Align.INLINE)
d.comment(0x861a, 'read the next character', align=Align.INLINE)
d.comment(0x861c, "'A'?", align=Align.INLINE)
d.char_literal(0x861d)
d.comment(0x861e, 'no: Mistake', align=Align.INLINE)
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
d.label(0x8620, 'asm_got_opcode')
d.expr(0x8621, ref(ASM_BASE_OPCODE) - 1)   # lda asm_base_opcode-1,x (1-based)
d.comment(0x8623, 'Save it', align=Align.INLINE)
d.comment(0x8625, 'Assume a one-byte instruction', align=Align.INLINE)
d.comment(0x8627, 'index &1A+ takes an operand?', align=Align.INLINE)
d.comment(0x8629, 'yes: parse the addressing mode', align=Align.INLINE)
# Store loop (&862B): write the assembled bytes to P%/O%.
d.comment(0x862b, "P% low -> destination", align=Align.INLINE)
d.subroutine(
    0x862b, 'asm_emit',
    title='Emit assembled bytes to P%/O%',
    description="""The inline assembler's byte-emit routine. Copies the assembled bytes
to the destination given by P% (resint_p, &0440), or by O% (resint_o,
&043C) when OPT selects offset assembly (OPT >= 4), then advances P%
(and O% for offset assembly) past them. Y is the signed byte count: 0
emits nothing; a positive count stores that many opcode/operand bytes
from the assembly buffer at zp_asm_opcode (&29); a negative count is
an EQUS, storing zp_strbuf_len (&36) bytes taken from string_work
(&0600).
""",
    on_entry={
        'Y': 'signed byte count: 0 = none, positive N = N opcode bytes from zp_asm_opcode (&29), negative = EQUS string from string_work (&0600)',
        'zp_opt_flag (&28)': 'current OPT setting (bit 2 selects offset assembly to O%)',
        'zp_strbuf_len (&36)': 'string length when emitting an EQUS',
        'resint_p (&0440)': 'P%, the assembly program counter',
        'resint_o (&043C)': 'O%, the offset-assembly destination',
    },
    on_exit={
        'resint_p (&0440)': 'P% advanced past the emitted bytes',
        'resint_o (&043C)': 'O% advanced too when offset assembly is active',
    },
)
d.comment(0x862e, 'to &37', align=Align.INLINE)
d.comment(0x8630, 'Save the byte count', align=Align.INLINE)
d.comment(0x8632, 'OPT setting', align=Align.INLINE)
d.comment(0x8634, 'offset assembly (OPT >= 4)?', align=Align.INLINE)
d.comment(0x8636, 'P% high', align=Align.INLINE)
d.comment(0x8639, 'to &38', align=Align.INLINE)
d.comment(0x863b, 'no offset: assemble at P%', align=Align.INLINE)
d.comment(0x863d, 'offset: assemble at O% instead', align=Align.INLINE)
d.comment(0x8640, 'O% high', align=Align.INLINE)
d.comment(0x8643, 'Store the destination pointer', align=Align.INLINE)
d.label(0x8643, 'asm_emit_dest')
d.comment(0x8645, 'high byte (&3B)', align=Align.INLINE)
d.comment(0x8647, 'Any bytes to store?', align=Align.INLINE)
d.comment(0x8648, 'none: done', align=Align.INLINE)
d.comment(0x864a, 'positive count: store opcode bytes', align=Align.INLINE)
d.comment(0x864c, 'EQUS: length from the string buffer', align=Align.INLINE)
d.comment(0x864e, 'empty: done', align=Align.INLINE)
d.comment(0x8650, 'Next byte index', align=Align.INLINE)
d.label(0x8650, 'asm_emit_loop')
d.comment(0x8651, 'Opcode/operand byte', align=Align.INLINE)
d.comment(0x8654, 'storing string (EQUS) bytes?', align=Align.INLINE)
d.comment(0x8656, 'no: store the opcode byte', align=Align.INLINE)
d.comment(0x8658, 'yes: take it from the string buffer', align=Align.INLINE)
d.comment(0x865b, 'Store the byte at the destination', align=Align.INLINE)
d.label(0x865b, 'asm_emit_store')
d.comment(0x865d, 'Advance P%', align=Align.INLINE)
d.comment(0x8660, 'no carry,', align=Align.INLINE)
d.comment(0x8662, 'carry into P% high', align=Align.INLINE)
d.comment(0x8665, 'offset assembly?', align=Align.INLINE)
d.label(0x8665, 'asm_emit_advance')
d.comment(0x8667, 'yes: advance O% too', align=Align.INLINE)
d.comment(0x866a, 'no carry,', align=Align.INLINE)
d.comment(0x866c, 'carry into O% high', align=Align.INLINE)
d.comment(0x866f, 'More bytes?', align=Align.INLINE)
d.label(0x866f, 'asm_emit_more')
d.comment(0x8670, 'loop', align=Align.INLINE)
d.comment(0x8672, 'Return', align=Align.INLINE)
# Branch operand (&8673): relative branch, range-checked.
d.comment(0x8673, 'index &22+ is not a branch?', align=Align.INLINE)
d.label(0x8673, 'asm_operand')
d.comment(0x8675, 'yes: other operand forms', align=Align.INLINE)
d.comment(0x8677, 'Evaluate the target address', align=Align.INLINE)
d.comment(0x867a, 'Offset = target - (P% + 2)', align=Align.INLINE)
d.comment(0x867b, 'target low,', align=Align.INLINE)
d.comment(0x867d, 'minus P% low (- 1),', align=Align.INLINE)
d.comment(0x8680, 'offset low in Y,', align=Align.INLINE)
d.comment(0x8681, 'target high,', align=Align.INLINE)
d.comment(0x8683, 'minus P% high,', align=Align.INLINE)
d.comment(0x8686, 'offset >= 1?,', align=Align.INLINE)
d.comment(0x8688, 'offset - 1 (for PC+2),', align=Align.INLINE)
d.comment(0x8689, 'borrow into the high byte', align=Align.INLINE)
d.comment(0x868b, 'in forward range?', align=Align.INLINE)
d.comment(0x868d, 'in backward range?', align=Align.INLINE)
d.comment(0x868f, 'high byte &FF: in range', align=Align.INLINE)
d.comment(0x8691, 'OPT setting', align=Align.INLINE)
d.label(0x8691, 'asm_branch_range_err')
d.comment(0x8692, 'errors enabled?', align=Align.INLINE)
d.comment(0x8693, 'errors enabled (bit 1)?', align=Align.INLINE)
d.comment(0x8694, 'no: ignore the range error', align=Align.INLINE)
d.comment(0x8696, 'Out of range error', align=Align.INLINE)
d.comment(0x86a5, 'Use the offset byte', align=Align.INLINE)
d.label(0x86a5, 'asm_branch_ok')
d.comment(0x86a6, 'as the operand', align=Align.INLINE)
d.label(0x86a6, 'asm_set_operand')
d.comment(0x86a8, 'Two-byte instruction', align=Align.INLINE)
d.label(0x86a8, 'asm_two_byte')
d.comment(0x86aa, 'store it', align=Align.INLINE)
d.comment(0x86ad, 'forward: check the high byte', align=Align.INLINE)
d.label(0x86ad, 'asm_branch_fwd')
d.comment(0x86ae, 'in range', align=Align.INLINE)
d.comment(0x86b0, 'out of range', align=Align.INLINE)
d.comment(0x86b2, 'backward: check the high byte', align=Align.INLINE)
d.label(0x86b2, 'asm_branch_back')
d.comment(0x86b3, 'in range', align=Align.INLINE)
d.comment(0x86b5, 'out of range', align=Align.INLINE)
# Immediate operand (&86B7).
d.comment(0x86b7, "index &29+ : not immediate?", align=Align.INLINE)
d.label(0x86b7, 'asm_mode_imm')
d.comment(0x86b9, 'yes: indexed/absolute modes', align=Align.INLINE)
# Addressing-mode parser skip-spaces / register checks.
d.comment(0x86bb, 'Skip spaces', align=Align.INLINE)
d.comment(0x86be, "'#' immediate prefix?", align=Align.INLINE)
d.char_literal(0x86bf)
d.comment(0x86c0, 'no: absolute', align=Align.INLINE)
d.comment(0x86c2, 'Immediate mode: adjust the opcode', align=Align.INLINE)
d.comment(0x86c5, 'Evaluate the immediate value', align=Align.INLINE)
d.label(0x86c5, 'asm_imm_eval')
d.comment(0x86c8, 'high byte zero (fits in a byte)?', align=Align.INLINE)
d.label(0x86c8, 'asm_imm_byte')
d.comment(0x86ca, 'yes: two-byte instruction', align=Align.INLINE)
d.comment(0x86cc, 'Byte error (value > 255)', align=Align.INLINE)
d.label(0x86cc, 'asm_byte_error')
# (zp),Y and (zp,X) parsers (&86D3).
d.comment(0x86d3, 'index &36 : the (zp),Y / (zp,X) group?', align=Align.INLINE)
d.label(0x86d3, 'asm_mode_indirect')
d.comment(0x86d5, 'no: absolute/indexed group', align=Align.INLINE)
d.comment(0x86d7, 'Skip spaces', align=Align.INLINE)
d.comment(0x86da, "'(' opening an indirect mode?", align=Align.INLINE)
d.char_literal(0x86db)
d.label(0x86da, 'asm_try_indirect')
d.comment(0x86dc, 'no: absolute', align=Align.INLINE)
d.comment(0x86de, 'Evaluate the zero-page address', align=Align.INLINE)
d.comment(0x86e1, 'Skip spaces', align=Align.INLINE)
d.comment(0x86e4, "')' -> (zp),Y form", align=Align.INLINE)
d.char_literal(0x86e5)
d.comment(0x86e6, "no: try (zp,X)", align=Align.INLINE)
d.comment(0x86e8, 'Skip spaces', align=Align.INLINE)
d.comment(0x86eb, "','?", align=Align.INLINE)
d.char_literal(0x86ec)
d.comment(0x86ed, 'no: Index error', align=Align.INLINE)
d.comment(0x86ef, 'adjust the opcode for (zp),Y', align=Align.INLINE)
d.comment(0x86f2, 'Skip spaces', align=Align.INLINE)
d.comment(0x86f5, "'Y'?", align=Align.INLINE)
d.char_literal(0x86f6)
d.comment(0x86f7, 'no: Index error', align=Align.INLINE)
d.comment(0x86f9, 'process as a two-byte instruction', align=Align.INLINE)
d.comment(0x86fb, "','?", align=Align.INLINE)
d.char_literal(0x86fc)
d.label(0x86fb, 'asm_indirect_zpx')
d.comment(0x86fd, 'no: Index error', align=Align.INLINE)
d.comment(0x86ff, 'Skip spaces', align=Align.INLINE)
d.comment(0x8702, "'X'?", align=Align.INLINE)
d.char_literal(0x8703)
d.comment(0x8704, 'no: Index error', align=Align.INLINE)
d.comment(0x8706, 'Skip spaces', align=Align.INLINE)
d.comment(0x8709, "')'?", align=Align.INLINE)
d.char_literal(0x870a)
d.comment(0x870b, 'yes: process', align=Align.INLINE)
d.comment(0x870d, 'Index error', align=Align.INLINE)
d.label(0x870d, 'asm_index_error')
d.comment(0x8715, 'Back up over the "("', align=Align.INLINE)
d.label(0x8715, 'asm_abs_from_paren')
d.comment(0x8717, 'Evaluate the address', align=Align.INLINE)
d.comment(0x871a, 'Skip spaces', align=Align.INLINE)
d.comment(0x871d, "','?", align=Align.INLINE)
d.char_literal(0x871e)
d.comment(0x871f, 'no: process as absolute', align=Align.INLINE)
d.comment(0x8721, 'adjust the opcode for absolute,X/,Y', align=Align.INLINE)
d.comment(0x8724, 'Skip spaces', align=Align.INLINE)
d.comment(0x8727, "'X'?", align=Align.INLINE)
d.char_literal(0x8728)
d.comment(0x8729, 'yes: abs,X', align=Align.INLINE)
d.comment(0x872b, "'Y'?", align=Align.INLINE)
d.char_literal(0x872c)
d.comment(0x872d, 'no: Index error', align=Align.INLINE)
d.comment(0x872f, 'Adjust the opcode for the indexed form', align=Align.INLINE)
d.label(0x872f, 'asm_indexed_adjust')
d.comment(0x8732, 'process the absolute operand', align=Align.INLINE)
# abs / abs,X (&8735).
d.comment(0x8735, 'Adjust the opcode for absolute mode', align=Align.INLINE)
d.subroutine(
    0x8735, 'asm_absolute',
    title='Assemble a zero-page or absolute operand',
    description="""Adjust the opcode being built for absolute addressing
(asm_opcode_add4), then fall into asm_zp_or_abs, which tests the high
byte of the evaluated operand address in zp_iwa: high byte zero emits
the two-byte zero-page form (asm_two_byte), otherwise the three-byte
absolute form (asm_indexed_adjust). The inline assembler's addressing-mode handler for absolute / zero-page operands.
""",
    on_entry={
        'zp_iwa (&2A/&2B)': 'the evaluated operand address (low/high)',
        'zp_asm_opcode (&29)': 'the opcode being built',
    },
    on_exit={
        'control': 'tail-calls asm_two_byte (zero page, 2 bytes) or asm_indexed_adjust (absolute, 3 bytes); does not return here',
    },
)
d.comment(0x8738, 'address fits in zero page (high byte 0)?',
          align=Align.INLINE)
d.label(0x8738, 'asm_zp_or_abs')
d.comment(0x873a, 'no: assemble as absolute (three bytes)', align=Align.INLINE)
d.comment(0x873c, 'yes: assemble as two bytes', align=Align.INLINE)
# Addressing-mode dispatch by opcode class (&873F).
d.comment(0x873f, 'index &2F+ : a different operand class?', align=Align.INLINE)
d.label(0x873f, 'asm_mode_class2')
d.comment(0x8741, 'yes', align=Align.INLINE)
d.comment(0x8743, 'index &2D+ (accumulator-or-absolute)?', align=Align.INLINE)
d.comment(0x8745, 'yes', align=Align.INLINE)
d.comment(0x8747, 'Skip spaces', align=Align.INLINE)
d.comment(0x874a, "'A' (accumulator)?", align=Align.INLINE)
d.char_literal(0x874b)
d.comment(0x874c, 'yes', align=Align.INLINE)
d.comment(0x874e, 'Back up a character', align=Align.INLINE)
d.comment(0x8750, 'Evaluate the address', align=Align.INLINE)
d.label(0x8750, 'asm_acc_or_abs')
d.comment(0x8753, 'Skip spaces', align=Align.INLINE)
d.comment(0x8756, "','?", align=Align.INLINE)
d.char_literal(0x8757)
d.comment(0x8758, 'no: process', align=Align.INLINE)
d.comment(0x875a, 'adjust the opcode for indexed mode', align=Align.INLINE)
d.comment(0x875d, 'Skip spaces', align=Align.INLINE)
d.comment(0x8760, "'X'?", align=Align.INLINE)
d.char_literal(0x8761)
d.comment(0x8762, 'yes: address,X', align=Align.INLINE)
d.comment(0x8764, 'Index error', align=Align.INLINE)
d.comment(0x8767, 'Accumulator form: adjust the opcode', align=Align.INLINE)
d.label(0x8767, 'asm_accumulator')
d.comment(0x876a, 'one byte', align=Align.INLINE)
d.comment(0x876c, 'store it', align=Align.INLINE)
d.comment(0x876e, 'index &32+ : implied/branch class?', align=Align.INLINE)
d.label(0x876e, 'asm_mode_class3')
d.comment(0x8770, 'yes', align=Align.INLINE)
d.comment(0x8772, 'index &31 (immediate-only)?', align=Align.INLINE)
d.comment(0x8774, 'yes', align=Align.INLINE)
d.comment(0x8776, 'Skip spaces', align=Align.INLINE)
d.comment(0x8779, "'#' immediate?", align=Align.INLINE)
d.char_literal(0x877a)
d.comment(0x877b, 'no: address', align=Align.INLINE)
d.comment(0x877d, 'immediate', align=Align.INLINE)
d.comment(0x8780, 'Back up a character', align=Align.INLINE)
d.label(0x8780, 'asm_imm1_backup')
d.comment(0x8782, 'Evaluate the value', align=Align.INLINE)
d.label(0x8782, 'asm_imm1_eval')
d.comment(0x8785, 'assemble as absolute', align=Align.INLINE)
d.comment(0x8788, 'index &33 (no operand)?', align=Align.INLINE)
d.label(0x8788, 'asm_mode_noop')
d.comment(0x878a, 'yes', align=Align.INLINE)
d.comment(0x878c, 'index &34+ : other forms', align=Align.INLINE)
d.comment(0x878e, 'Skip spaces', align=Align.INLINE)
d.comment(0x8791, "'(' indirect?", align=Align.INLINE)
d.char_literal(0x8792)
d.comment(0x8793, 'yes', align=Align.INLINE)
d.comment(0x8795, 'Back up a character', align=Align.INLINE)
d.comment(0x8797, 'Evaluate the address', align=Align.INLINE)
d.label(0x8797, 'asm_addr_eval')
d.comment(0x879a, 'Three-byte instruction', align=Align.INLINE)
d.label(0x879a, 'asm_three_byte')
d.comment(0x879c, 'store it', align=Align.INLINE)
d.label(0x879c, 'asm_three_emit')
d.comment(0x879f, 'Indirect: adjust the opcode', align=Align.INLINE)
d.label(0x879f, 'asm_jmp_indirect')
d.comment(0x87a2, '(continued)', align=Align.INLINE)
d.comment(0x87a5, 'evaluate the address', align=Align.INLINE)
d.comment(0x87a8, 'Skip spaces', align=Align.INLINE)
d.comment(0x87ab, "')' to close?", align=Align.INLINE)
d.char_literal(0x87ac)
d.comment(0x87ad, 'yes: three-byte instruction', align=Align.INLINE)
d.comment(0x87af, 'Index error', align=Align.INLINE)
d.comment(0x87b2, 'index &39+ : EQU directives', align=Align.INLINE)
d.label(0x87b2, 'asm_mode_equ')
d.comment(0x87b4, 'yes', align=Align.INLINE)
d.comment(0x87b6, 'Register letter from the mnemonic', align=Align.INLINE)
d.comment(0x87b9, 'toggle bit 0', align=Align.INLINE)
d.comment(0x87ba, 'save it', align=Align.INLINE)
d.comment(0x87bb, 'index &37+ (two-register form)?', align=Align.INLINE)
d.comment(0x87bc, 'Save the register', align=Align.INLINE)
d.comment(0x87bd, 'yes', align=Align.INLINE)
d.comment(0x87bf, 'two-register form?', align=Align.INLINE)
d.comment(0x87c2, "'#' immediate?", align=Align.INLINE)
d.comment(0x87c4, 'no: absolute', align=Align.INLINE)
d.char_literal(0x87c5)
d.comment(0x87c6, 'discard the saved register, do immediate', align=Align.INLINE)
d.comment(0x87c8, 'discard the register', align=Align.INLINE)
d.comment(0x87c9, 'do immediate', align=Align.INLINE)
d.comment(0x87cc, 'Back up a character', align=Align.INLINE)
d.label(0x87cc, 'asm_equ_backup')
d.comment(0x87ce, 'Evaluate the address', align=Align.INLINE)
d.comment(0x87d1, 'recover the register letter', align=Align.INLINE)
d.comment(0x87d3, 'into &37', align=Align.INLINE)
d.comment(0x87d6, "',' index register?", align=Align.INLINE)
d.comment(0x87d8, 'yes', align=Align.INLINE)
d.char_literal(0x87d8)
d.comment(0x87da, 'no: assemble as absolute', align=Align.INLINE)
d.comment(0x87db, 'process as absolute', align=Align.INLINE)
d.comment(0x87de, 'Index register letter', align=Align.INLINE)
d.label(0x87de, 'asm_equ_index')
d.comment(0x87e2, 'matches the expected register?', align=Align.INLINE)
d.comment(0x87e4, 'no: Index error', align=Align.INLINE)
d.comment(0x87e5, 'register mismatch?', align=Align.INLINE)
d.comment(0x87e7, 'adjust the opcode for the indexed form',
          align=Align.INLINE)
d.comment(0x87ea, 'assemble as absolute', align=Align.INLINE)
d.comment(0x87ed, 'Index error', align=Align.INLINE)
d.label(0x87ed, 'asm_equ_index_err')
d.comment(0x87f0, 'Evaluate the address', align=Align.INLINE)
d.label(0x87f0, 'asm_equ_eval')
d.comment(0x87f3, 'recover the register letter', align=Align.INLINE)
d.comment(0x87f5, 'into &37', align=Align.INLINE)
d.comment(0x87f8, "',' index register?", align=Align.INLINE)
d.comment(0x87fa, 'no: single operand', align=Align.INLINE)
d.char_literal(0x87fa)
d.comment(0x87fc, 'Index register letter', align=Align.INLINE)
d.comment(0x87fe, 'read the index register letter', align=Align.INLINE)
d.comment(0x8800, 'matches?', align=Align.INLINE)
d.comment(0x8802, 'no: Index error', align=Align.INLINE)
d.comment(0x8804, 'adjust the opcode for indexed mode', align=Align.INLINE)
d.comment(0x8807, 'high byte zero?', align=Align.INLINE)
d.comment(0x8809, 'yes: continue', align=Align.INLINE)
d.comment(0x880b, 'Byte error (value > 255)', align=Align.INLINE)
d.comment(0x880d, 'Byte error', align=Align.INLINE)
d.comment(0x8810, 'Assemble as zero-page', align=Align.INLINE)
d.label(0x8810, 'asm_force_zp')
d.comment(0x8813, 'index &39 (OPT)?', align=Align.INLINE)
d.label(0x8813, 'asm_opt_directive')

d.comment(0x8815, 'no: EQU directives', align=Align.INLINE)
d.comment(0x8817, 'OPT: evaluate the new setting', align=Align.INLINE)
d.comment(0x8818, 'OPT value', align=Align.INLINE)
d.comment(0x881a, 'store it as the OPT flag', align=Align.INLINE)
d.comment(0x881c, 'no bytes to assemble', align=Align.INLINE)
d.comment(0x881e, 'finish', align=Align.INLINE)

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
# eval_expr_to_integer (&8821): inline body.
d.comment(0x8821, 'Evaluate the expression', align=Align.INLINE)
d.comment(0x8824, 'coerce to an integer', align=Align.INLINE)
d.comment(0x8827, 'Sync the primary text offset', align=Align.INLINE)
# final batch: EQU/INPUT/READ/DATA/program-edit/file routines
d.label(0x8827, 'eeti_sync')
d.comment(0x8829, 'copy PtrB offset to PtrA', align=Align.INLINE)
d.comment(0x882b, 'Return', align=Align.INLINE)
d.subroutine(0x882c, 'asm_opcode_add16',
             title='Advance the opcode by four addressing-mode columns (+16)',
             description='Add 16 to the base opcode in zp_asm_opcode (via +8, +4, '
                         '+4) to select an addressing mode four columns along.',
             on_entry={'zp_asm_opcode (&29)': 'the base opcode'},
             on_exit={'zp_asm_opcode (&29)': 'the opcode + 16', 'A': 'the new opcode',
                      'X': 'preserved', 'Y': 'preserved'})
# Opcode addressing-mode adjusters.
d.comment(0x882c, 'add 8 then fall through (+16 total)', align=Align.INLINE)
d.subroutine(0x882f, 'asm_opcode_add8',
             title='Advance the opcode by two addressing-mode columns (+8)',
             description='Add 8 to the base opcode in zp_asm_opcode (via +4, +4) '
                         'to select an addressing mode two columns along.',
             on_entry={'zp_asm_opcode (&29)': 'the base opcode'},
             on_exit={'zp_asm_opcode (&29)': 'the opcode + 8', 'A': 'the new opcode',
                      'X': 'preserved', 'Y': 'preserved'})
d.comment(0x882f, 'add 4 then fall through (+8 total)', align=Align.INLINE)
d.subroutine(0x8832, 'asm_opcode_add4',
             title='Step the opcode to the next addressing-mode column (+4)',
             description='Add 4 to the base opcode in &29 to select the next '
                         '6502 addressing-mode encoding.',
             on_entry={'zp_asm_opcode (&29)': 'the base opcode'},
             on_exit={'zp_asm_opcode (&29)': 'the opcode + 4', 'A': 'the new opcode',
                      'X': 'preserved', 'Y': 'preserved'})
d.comment(0x8832, 'Opcode += 4 (next addressing-mode column)',
          align=Align.INLINE)
d.comment(0x8834, 'clear carry,', align=Align.INLINE)
d.comment(0x8835, 'add 4 (next mode column),', align=Align.INLINE)
d.comment(0x8837, 'store the opcode', align=Align.INLINE)
d.comment(0x8839, 'Return', align=Align.INLINE)

# EQUB/EQUW/EQUD/EQUS directives (&883A).
d.comment(0x883a, 'Assume one byte (EQUB)', align=Align.INLINE)
d.label(0x883a, 'equb_directive')
d.comment(0x883c, 'Next character of the directive', align=Align.INLINE)
d.comment(0x883e, 'consume that character', align=Align.INLINE)
d.comment(0x8841, "'B' (EQUB)?", align=Align.INLINE)
d.comment(0x8843, 'yes', align=Align.INLINE)
d.char_literal(0x8843)
d.comment(0x8844, 'two bytes (EQUW)', align=Align.INLINE)
d.comment(0x8845, "'W' (EQUW)?", align=Align.INLINE)
d.comment(0x8846, 'two bytes', align=Align.INLINE)
d.comment(0x8847, 'yes', align=Align.INLINE)
d.char_literal(0x8848)
d.comment(0x8849, 'four bytes (EQUD)', align=Align.INLINE)
d.comment(0x884b, "'D' (EQUD)?", align=Align.INLINE)
d.comment(0x884d, 'yes', align=Align.INLINE)
d.char_literal(0x884e)
d.comment(0x884f, "'S' (EQUS)?", align=Align.INLINE)
d.comment(0x8851, 'yes', align=Align.INLINE)
d.char_literal(0x8852)
d.comment(0x8853, 'none: Mistake (syntax error)', align=Align.INLINE)
d.comment(0x8855, 'Mistake (syntax) error', align=Align.INLINE)
d.comment(0x8858, 'Save the byte count', align=Align.INLINE)
d.label(0x8858, 'equb_save_count')
d.comment(0x8859, 'push it', align=Align.INLINE)
d.comment(0x885a, 'Evaluate the value', align=Align.INLINE)
d.comment(0x885d, 'Store it into the opcode bytes', align=Align.INLINE)
d.comment(0x885f, 'into &29 onward', align=Align.INLINE)
d.comment(0x8862, 'recover the byte count', align=Align.INLINE)
d.comment(0x8863, 'into Y', align=Align.INLINE)
d.comment(0x8864, 'Assemble the bytes', align=Align.INLINE)
d.label(0x8864, 'equb_emit_loop')
d.comment(0x8867, 'String expected: Type mismatch', align=Align.INLINE)
d.label(0x8867, 'equs_type_error')
d.comment(0x886a, 'EQUS: save the OPT flag', align=Align.INLINE)
d.label(0x886a, 'equs_save_opt')
d.comment(0x886c, 'push the OPT flag', align=Align.INLINE)
d.comment(0x886f, 'evaluate the string expression', align=Align.INLINE)
d.comment(0x8871, 'not a string: Type mismatch', align=Align.INLINE)
d.comment(0x8872, 'restore the OPT flag', align=Align.INLINE)
d.comment(0x8873, 'store it back', align=Align.INLINE)
d.comment(0x8875, 'sync the text offset', align=Align.INLINE)
d.comment(0x8878, 'flag EQUS (length from the string buffer)',
          align=Align.INLINE)
d.comment(0x887a, 'assemble the string bytes', align=Align.INLINE)

# sub_c887c (&887C): shift bytes up to make room / move a line tail.
d.comment(0x887c, 'Save the byte to insert', align=Align.INLINE)
d.label(0x887c, 'insert_byte')
d.comment(0x887d, 'Source = dest + Y', align=Align.INLINE)
d.comment(0x887e, 'offset to A,', align=Align.INLINE)
d.comment(0x887f, '+ dest low,', align=Align.INLINE)
d.comment(0x8881, 'source low (&39),', align=Align.INLINE)
d.comment(0x8883, 'reset the index,', align=Align.INLINE)
d.comment(0x8885, 'A = 0,', align=Align.INLINE)
d.comment(0x8886, '+ dest high,', align=Align.INLINE)
d.comment(0x8888, 'source high (&3A)', align=Align.INLINE)
d.comment(0x888a, 'recover the byte to insert', align=Align.INLINE)
d.comment(0x888b, 'store the inserted byte', align=Align.INLINE)

d.comment(0x888d, 'Copy the rest of the line up', align=Align.INLINE)
d.label(0x888d, 'insert_byte_loop')
d.comment(0x888e, 'read from source+Y,', align=Align.INLINE)
d.comment(0x8890, 'write to dest+Y,', align=Align.INLINE)
d.comment(0x8892, 'until the carriage return', align=Align.INLINE)
d.comment(0x8894, 'until the CR', align=Align.INLINE)
d.comment(0x8896, 'Return', align=Align.INLINE)

d.subroutine(0x8897, 'parse_decimal_u16',
             title='Tokenise a line-number reference',
             description='Accumulate the decimal digits at (zp_general),Y into '
                         'a 16-bit value (value*10 + digit, in &3D/&3E) and, on '
                         'success, replace them in place with the three-byte '
                         '&8D line-number token (the GOTO/GOSUB encoding). Stops '
                         'at the first non-digit; reports overflow if the value '
                         'exceeds 16 bits.',
             on_entry={'A': 'the first decimal digit',
                       'zp_general (&37/&38)': 'the source text pointer',
                       'Y': 'offset of the first digit'},
             on_exit={'(zp_general)': 'the digits replaced by the &8D 3-byte token',
                      'C': 'clear on success, set on overflow (too large)'})
# parse_decimal_u16 (&8897): accumulate value*10 + digit.
d.comment(0x8897, 'First digit', align=Align.INLINE)
d.comment(0x8899, 'Value low = digit', align=Align.INLINE)
d.comment(0x889b, 'Value high = 0', align=Align.INLINE)
d.comment(0x889d, 'Next character', align=Align.INLINE)
d.label(0x889d, 'parse_dec_loop')
d.comment(0x889e, 'read it', align=Align.INLINE)
d.comment(0x88a0, 'above 9?', align=Align.INLINE)
d.expr(0x88a1, char(ord('9')) + 1)  # &3A: one past '9'
d.comment(0x88a2, 'not a digit: done', align=Align.INLINE)
d.comment(0x88a4, 'below 0?', align=Align.INLINE)
d.char_literal(0x88a5)
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
d.label(0x88d5, 'parse_dec_overflow')
d.comment(0x88d6, 'Offset 0', align=Align.INLINE)
d.comment(0x88d8, 'flag a value was read', align=Align.INLINE)
d.comment(0x88d9, 'Return', align=Align.INLINE)

# Tokeniser line-number insertion (&88DA) and encode_line_number (&88F5).
d.comment(0x88da, 'Back up', align=Align.INLINE)
d.label(0x88da, 'parse_dec_encode')
d.comment(0x88db, 'Line-number token &8D', align=Align.INLINE)
d.comment(0x88dd, 'Make room for the 3 encoded bytes', align=Align.INLINE)
d.comment(0x88e0, 'Destination = source + 2', align=Align.INLINE)
d.comment(0x88e2, 'source low + 2', align=Align.INLINE)
d.comment(0x88e4, 'dest low', align=Align.INLINE)
d.comment(0x88e6, 'source high...', align=Align.INLINE)
d.comment(0x88e8, '+ carry', align=Align.INLINE)
d.comment(0x88ea, 'dest high', align=Align.INLINE)
d.comment(0x88ec, 'Shift the bytes up', align=Align.INLINE)
d.label(0x88ec, 'parse_dec_shift_loop')
d.comment(0x88ee, 'up two bytes', align=Align.INLINE)
d.comment(0x88f0, 'next', align=Align.INLINE)
d.comment(0x88f1, 'loop', align=Align.INLINE)
d.comment(0x88f3, 'Three encoded bytes', align=Align.INLINE)
d.subroutine(0x88f5, 'encode_line_number',
             title='Encode a 16-bit line number into 3 bytes',
             description='Pack the line number in &3D/&3E into the BBC '
                         'three-byte GOTO encoding (a control byte holding '
                         'the scrambled top bits, then low|&40 and high|&40) '
                         'so the bytes never collide with tokens. The control '
                         'byte carries only four high bits, so the encoding is '
                         'exact only for line numbers 0-32767 (above that the '
                         'top bit is lost - the documented line-number '
                         'ceiling), and no encoded byte is ever &0D.',
             on_entry={'zp_fwb_exp (&3D/&3E)': 'the 16-bit line number',
                       'zp_general (&37/&38)': 'the destination text pointer',
                       'Y': 'offset of the last of the three bytes'},
             on_exit={'(zp_general)': 'the three encoded bytes (after the &8D token)'})
d.comment(0x88f5, 'Byte 2 = line-number high | &40', align=Align.INLINE)
d.comment(0x88f7, '| &40 (lift out of token range)', align=Align.INLINE)
d.comment(0x88f9, 'store byte 2', align=Align.INLINE)
d.comment(0x88fb, 'back to byte 1', align=Align.INLINE)
d.comment(0x88fc, 'Byte 1 = line-number low (6 bits) | &40', align=Align.INLINE)
d.comment(0x88fe, 'keep the low 6 bits,', align=Align.INLINE)
d.comment(0x8900, '| &40', align=Align.INLINE)
d.comment(0x8902, 'store byte 1', align=Align.INLINE)
d.comment(0x8904, 'Byte 0: scramble the top bits', align=Align.INLINE)
d.comment(0x8905, 'low byte: its top 2 bits...', align=Align.INLINE)
d.comment(0x8907, 'mask them,', align=Align.INLINE)
d.comment(0x8909, '(hold them)', align=Align.INLINE)
d.comment(0x890b, 'high byte: its top 2 bits...', align=Align.INLINE)
d.comment(0x890d, 'mask them,', align=Align.INLINE)
d.comment(0x890f, 'shift down,', align=Align.INLINE)
d.comment(0x8910, '(continued)', align=Align.INLINE)
d.comment(0x8911, 'merge with the low byte pair,', align=Align.INLINE)
d.comment(0x8913, 'shift the four bits down,', align=Align.INLINE)
d.comment(0x8914, '(continued)', align=Align.INLINE)
d.comment(0x8915, 'scramble (EOR &54)', align=Align.INLINE)
d.comment(0x8917, 'store the control byte', align=Align.INLINE)
d.comment(0x8919, 'Advance past the 3 bytes', align=Align.INLINE)
d.comment(0x891c, '(continued)', align=Align.INLINE)
d.comment(0x891f, '(continued)', align=Align.INLINE)
d.comment(0x8922, 'done: reset Y for the caller', align=Align.INLINE)
d.comment(0x8924, 'not a name character', align=Align.INLINE)
d.label(0x8924, 'not_name_char')
d.comment(0x8925, 'return (carry clear)', align=Align.INLINE)

d.subroutine(0x8926, 'is_alphanumeric',
             title='Test A for a name character',
             description='Return carry set if A is 0-9, A-Z, a-z or _, the '
                         'characters allowed in a variable or FN/PROC name.',
             on_entry={'A': 'the character to test'},
             on_exit={'C': 'set if A is a name character',
                      'A': 'preserved', 'X': 'preserved', 'Y': 'preserved'})
# is_alphanumeric (&8926).
d.comment(0x8926, "above 'z'?", align=Align.INLINE)
d.char_literal(0x8927)
d.comment(0x8928, 'yes: no', align=Align.INLINE)
d.comment(0x892a, "'_' or above?", align=Align.INLINE)
d.char_literal(0x892b)
d.comment(0x892c, 'yes: name char', align=Align.INLINE)
d.comment(0x892e, "'[' to '^'?", align=Align.INLINE)
d.char_literal(0x892f)
d.comment(0x8930, 'yes: no', align=Align.INLINE)
d.comment(0x8932, "'A' or above?", align=Align.INLINE)
d.char_literal(0x8933)
d.comment(0x8934, 'yes: name char', align=Align.INLINE)
d.comment(0x8936, "above '9'?", align=Align.INLINE)
d.char_literal(0x8937)
d.label(0x8936, 'is_digit')
d.comment(0x8938, 'yes: no', align=Align.INLINE)
d.comment(0x893a, "digit?", align=Align.INLINE)
d.char_literal(0x893b)
d.comment(0x893c, 'carry set if so', align=Align.INLINE)
d.comment(0x893d, "'.'?", align=Align.INLINE)
d.char_literal(0x893e)
d.label(0x893d, 'is_dot_or_digit')
d.comment(0x893f, 'no: test alphanumeric', align=Align.INLINE)
d.comment(0x8941, 'Return', align=Align.INLINE)

d.subroutine(
    0x8942, 'read_via_ptr_general',
    title='Read a byte via the general pointer, then advance it',
    description="""Load the byte at (zp_general),Y and fall through to
inc_ptr_general to step the 16-bit pointer on by one.
""",
    on_entry={'(zp_general) (&37/&38)': 'the pointer to read through',
              'Y': 'offset added to the pointer'},
    on_exit={'A': 'the byte read', 'zp_general': 'advanced by one',
             'X': 'preserved', 'Y': 'preserved'},
)
# read_via_ptr_general (&8942) / inc_ptr_general (&8944) / sub_c894b
d.comment(0x8942, 'Read the byte at (zp_general)+Y, then advance', align=Align.INLINE)
d.subroutine(
    0x8944, 'inc_ptr_general',
    title='Increment the general 16-bit pointer',
    description="""Increment the little-endian pointer held in zp_general
(&37/&38) by one, carrying into the high byte.
""",
    on_entry={'zp_general (&37/&38)': 'the pointer to advance'},
    on_exit={'zp_general': 'incremented by one',
             'A': 'preserved', 'X': 'preserved', 'Y': 'preserved'},
)
d.comment(0x8944, 'Increment the general pointer: low byte', align=Align.INLINE)
d.comment(0x8946, 'No carry: done', align=Align.INLINE)
d.comment(0x8948, 'Carry into the high byte', align=Align.INLINE)
d.comment(0x894a, 'Return (shared)', align=Align.INLINE)
d.comment(0x894b, 'Advance the pointer...', align=Align.INLINE)
d.subroutine(
    0x894b, 'general_next_byte',
    title='Advance the general pointer and read the next byte',
    description="""Call inc_ptr_general to increment the 16-bit general pointer
zp_general (&37/&38) by one (carrying into the high byte), then load
the byte at (zp_general),Y and return it in A. The tokeniser's fetch-next-character primitive for hex constants and string literals.
""",
    on_entry={
        'zp_general (&37)': 'the pointer to advance (&37/&38)',
        'Y': 'index added to the pointer for the read (usually 0)',
    },
    on_exit={
        'A': 'the byte read at the incremented pointer',
        'zp_general (&37)': 'incremented by one',
        'Y': 'preserved',
    },
)

d.comment(0x894e, '...then read the next byte', align=Align.INLINE)
d.comment(0x8950, 'Return the byte', align=Align.INLINE)

d.subroutine(
    0x8951, 'tokenise_line',
    title='Tokenise a line',
    description="""Convert the line being entered into its internal form, replacing
keywords with tokens via the keyword_table while leaving strings,
line numbers and names intact. Works through the buffer using the
general pointer (zp_general, &37).

Three entry points share this scanner, differing only in how much of
the &3B/&3C state they reset:
 - tokenise_line (&8951): start a fresh line; clear both the
   start-of-statement flag &3B and the line-number flag &3C.
 - tokenise_resume (&8955): clear only &3C; the caller has already set
   &3B. EVAL enters here with &3B = mid-statement so a re-tokenised
   string reads PTR etc. as functions, not assignment targets.
 - tok_scan (&8957): clear neither; execute_line enters here having
   pre-armed &3C = &FF so a typed leading line number is encoded with
   the &8D token (then recovered by check_line_number, see &8B2D).
""",
    on_entry={'zp_general (&37/&38)': 'a pointer to the line text to tokenise'},
    on_exit={'(zp_general)': 'the line rewritten with keyword tokens'},
)
# --- tokeniser character scan (front end of tokenise) ----------------
# Walks the source line at (zp_general), passing literals through
# untouched and resetting state at statement boundaries; keyword
# matching against keyword_table follows. NB &3B/&3C (normally FWB) are
# reused here as tokeniser state: start-of-statement and line-number
# flags. &3C arms line-number encoding (after GOTO etc.); strings are
# copied inline and need no quote-state flag.
d.comment(0x8951, 'Tokeniser state (&3B/&3C): start of statement',
          align=Align.INLINE)
# tokenise_line (&8951): match keywords against keyword_table and
# replace them with tokens, driven by each keyword's flag byte.
d.comment(0x8953, 'Start-of-statement flag (&3B)', align=Align.INLINE)
d.comment(0x8955, 'Clear the line-number flag (&3C)', align=Align.INLINE)
# tokenise_line internals
d.label(0x8955, 'tokenise_resume')
d.comment(0x8957, 'Scan the next source character', align=Align.INLINE)
d.label(0x8957, 'tok_scan')
d.comment(0x8959, 'CR: end of line', align=Align.INLINE)
d.comment(0x895b, 'Carriage return ends the line', align=Align.INLINE)
d.comment(0x895d, 'space: skip it', align=Align.INLINE)
d.char_literal(0x895e)
d.comment(0x895f, 'Skip spaces', align=Align.INLINE)
d.comment(0x8961, 'advance and read the next character', align=Align.INLINE)
d.label(0x8961, 'tok_advance')
d.comment(0x8964, 'loop', align=Align.INLINE)
d.comment(0x8966, 'An "&" introduces a hex constant: copy it unchanged',
          align=Align.INLINE)
d.char_literal(0x8967)
d.label(0x8966, 'tok_check_hex')
d.comment(0x8968, 'not "&": check the other cases', align=Align.INLINE)
d.comment(0x896a, 'Hex constant: advance and get a character', align=Align.INLINE)
d.label(0x896a, 'tok_hex_loop')
d.comment(0x896d, 'a digit?', align=Align.INLINE)
d.comment(0x8970, 'yes: keep copying', align=Align.INLINE)
d.comment(0x8972, "below 'A'?", align=Align.INLINE)
d.char_literal(0x8973)
d.comment(0x8974, 'not hex: resume scanning', align=Align.INLINE)
d.comment(0x8976, "'A'..'F'?", align=Align.INLINE)
d.char_literal(0x8977)
d.comment(0x8978, 'hex letter: keep copying', align=Align.INLINE)
d.comment(0x897a, 'past F: resume', align=Align.INLINE)
d.comment(0x897c, 'A quote starts a string literal: copy it verbatim',
          align=Align.INLINE)
d.char_literal(0x897d)
d.label(0x897c, 'tok_check_string')
d.comment(0x897e, 'not a quote: check for a colon', align=Align.INLINE)
d.comment(0x8980, 'String literal: copy to the closing quote', align=Align.INLINE)
d.label(0x8980, 'tok_string_loop')
d.comment(0x8983, 'a quote?', align=Align.INLINE)
d.char_literal(0x8984)
d.comment(0x8985, 'yes: end of string', align=Align.INLINE)
d.comment(0x8987, 'CR (unterminated)?', align=Align.INLINE)
d.comment(0x8989, 'no: keep copying', align=Align.INLINE)
d.comment(0x898b, 'Return', align=Align.INLINE)
d.comment(0x898c, 'A colon starts a new statement: reset the state',
          align=Align.INLINE)
d.char_literal(0x898d)
d.label(0x898c, 'tok_check_colon')
d.comment(0x898e, 'not a colon: check for a comma', align=Align.INLINE)
d.comment(0x8990, 'Colon: back to start-of-statement', align=Align.INLINE)
d.comment(0x8992, 'clear the line-number flag', align=Align.INLINE)
d.comment(0x8994, 'continue', align=Align.INLINE)
d.comment(0x8996, 'a comma?', align=Align.INLINE)
d.char_literal(0x8997)
d.label(0x8996, 'tok_check_comma_star')
d.comment(0x8998, 'yes: skip it', align=Align.INLINE)
d.comment(0x899a, '"*": maybe a *command (statement position checked next)',
          align=Align.INLINE)
d.char_literal(0x899b)

d.comment(0x899c, 'not "*": try a keyword or name', align=Align.INLINE)
d.comment(0x899e, 'at the start of a statement?', align=Align.INLINE)
d.comment(0x89a0, 'no (mid-statement): "*" is the multiply operator',
          align=Align.INLINE)
d.comment(0x89a2, 'yes: *command - RTS leaves the rest untokenised',
          align=Align.INLINE)
d.comment(0x89a3, 'a "." (abbreviation dot)?', align=Align.INLINE)
d.char_literal(0x89a4)
d.label(0x89a3, 'tok_check_number')
d.comment(0x89a5, 'yes', align=Align.INLINE)
d.comment(0x89a7, 'a digit?', align=Align.INLINE)
d.comment(0x89aa, 'no: a letter or symbol', align=Align.INLINE)
d.comment(0x89ac, 'line-number armed (after GOTO etc.)?', align=Align.INLINE)
d.comment(0x89ae, 'not armed: an ordinary number', align=Align.INLINE)
d.comment(0x89b0, 'tokenise the line number', align=Align.INLINE)
d.comment(0x89b3, 'continue', align=Align.INLINE)
d.comment(0x89b5, 'Skip a number: read a character', align=Align.INLINE)
d.label(0x89b5, 'tok_skip_number_loop')
d.comment(0x89b7, 'a digit or "."?', align=Align.INLINE)
d.comment(0x89ba, 'no: end of the number', align=Align.INLINE)
d.comment(0x89bc, 'advance', align=Align.INLINE)
d.comment(0x89bf, 'loop', align=Align.INLINE)
d.comment(0x89c2, 'Now in the middle of a statement:', align=Align.INLINE)
d.label(0x89c2, 'tok_resume_mid')
d.comment(0x89c4, 'set the flag', align=Align.INLINE)
d.comment(0x89c6, 'clear the line-number flag', align=Align.INLINE)
d.comment(0x89c8, 'resume scanning', align=Align.INLINE)
d.comment(0x89cb, 'Skip a variable name: alphanumeric?', align=Align.INLINE)
d.label(0x89cb, 'tok_skip_name')
d.comment(0x89ce, 'no: not a name', align=Align.INLINE)
d.comment(0x89d0, 'Consume the whole name run; no interior keyword match',
          align=Align.INLINE)
d.label(0x89d0, 'tok_name')
d.comment(0x89d2, 'read it', align=Align.INLINE)
d.label(0x89d2, 'tok_name_loop')
d.comment(0x89d4, 'alphanumeric?', align=Align.INLINE)
d.comment(0x89d7, 'no: end of the name', align=Align.INLINE)
d.comment(0x89d9, 'advance', align=Align.INLINE)
d.comment(0x89dc, 'loop', align=Align.INLINE)
d.comment(0x89df, "a letter ('A'+)?", align=Align.INLINE)
d.char_literal(0x89e0)
d.label(0x89df, 'tok_check_letter')
d.comment(0x89e1, 'yes: try to match a keyword', align=Align.INLINE)
d.comment(0x89e3, 'Not a keyword: middle of statement', align=Align.INLINE)
d.label(0x89e3, 'tok_not_keyword')
d.comment(0x89e5, 'set mid-statement,', align=Align.INLINE)
d.comment(0x89e7, 'clear the line-number flag', align=Align.INLINE)
d.comment(0x89e9, 'continue scanning', align=Align.INLINE)
d.label(0x89e9, 'tok_continue')
d.comment(0x89ec, "'X' or above?", align=Align.INLINE)
d.char_literal(0x89ed)
d.label(0x89ec, 'tok_try_keyword')
d.comment(0x89ee, 'nothing starts with X/Y/Z: skip the name', align=Align.INLINE)
d.comment(0x89f0, 'Point at the keyword table (&8071): low', align=Align.INLINE)
d.comment(0x89f2, '(store)', align=Align.INLINE)
d.comment(0x89f4, 'high &80', align=Align.INLINE)
d.comment(0x89f6, '(store)', align=Align.INLINE)
d.comment(0x89f8, 'Compare the first letter with this entry', align=Align.INLINE)
d.label(0x89f8, 'tok_kw_entry')
d.comment(0x89fa, 'entry past our letter: not a keyword', align=Align.INLINE)
d.comment(0x89fc, 'first letter differs: next entry', align=Align.INLINE)
d.comment(0x89fe, 'matches: compare the rest of the keyword', align=Align.INLINE)
d.label(0x89fe, 'tok_kw_match_loop')
d.comment(0x89ff, 'entry char (bit 7 = the token)', align=Align.INLINE)
d.comment(0x8a01, 'whole keyword matched: got a token', align=Align.INLINE)
d.comment(0x8a03, 'compare with the line', align=Align.INLINE)
d.comment(0x8a05, 'match: next character', align=Align.INLINE)
d.comment(0x8a07, 'mismatch: a "." abbreviation?', align=Align.INLINE)
d.comment(0x8a09, 'is it "."?', align=Align.INLINE)
d.char_literal(0x8a0a)
d.comment(0x8a0b, 'yes: accept the abbreviation', align=Align.INLINE)
d.comment(0x8a0d, 'Skip to the next entry: past the name', align=Align.INLINE)
d.label(0x8a0d, 'tok_kw_check_end')
d.comment(0x8a0e, 'read it', align=Align.INLINE)
d.comment(0x8a10, 'until the token byte (bit 7 set)', align=Align.INLINE)
d.comment(0x8a12, 'WIDTH token &FE doubles as the end-of-table sentinel',
          align=Align.INLINE)
d.comment(0x8a14, 'no: a real token, try the next entry', align=Align.INLINE)
d.comment(0x8a16, 'sentinel: not a keyword (skip the name)', align=Align.INLINE)
d.comment(0x8a18, 'Abbreviation: skip to this entry\'s token', align=Align.INLINE)
d.label(0x8a18, 'tok_kw_abbrev')
d.comment(0x8a19, 'read it', align=Align.INLINE)
d.label(0x8a19, 'tok_kw_skip_loop')
d.comment(0x8a1b, 'token byte: got it', align=Align.INLINE)
d.comment(0x8a1d, 'advance the table pointer', align=Align.INLINE)
d.comment(0x8a1f, 'no wrap', align=Align.INLINE)
d.comment(0x8a21, 'carry into high', align=Align.INLINE)
d.comment(0x8a23, 'loop', align=Align.INLINE)
d.comment(0x8a25, 'Advance past this entry to the next:', align=Align.INLINE)
d.label(0x8a25, 'tok_kw_next_entry')
d.comment(0x8a26, '(include the token byte)', align=Align.INLINE)
d.comment(0x8a27, 'offset...', align=Align.INLINE)
d.comment(0x8a28, 'low', align=Align.INLINE)
d.comment(0x8a2a, '(store)', align=Align.INLINE)
d.comment(0x8a2c, 'no carry', align=Align.INLINE)
d.comment(0x8a2e, 'carry into high', align=Align.INLINE)
d.comment(0x8a30, 'reset Y', align=Align.INLINE)
d.label(0x8a30, 'tok_kw_retry')
d.comment(0x8a32, 're-read the first letter', align=Align.INLINE)
d.comment(0x8a34, 'try the next entry', align=Align.INLINE)
d.comment(0x8a37, 'Token byte found: keep it in X', align=Align.INLINE)
d.label(0x8a37, 'tok_kw_found')
d.comment(0x8a38, 'the flag byte follows', align=Align.INLINE)
d.comment(0x8a39, 'get the token flag', align=Align.INLINE)
d.comment(0x8a3b, '(save it in &3D)', align=Align.INLINE)
d.comment(0x8a3d, 'back up Y', align=Align.INLINE)
d.comment(0x8a3e, 'flag bit 0: conditional tokenisation?', align=Align.INLINE)
d.comment(0x8a3f, 'no', align=Align.INLINE)
d.comment(0x8a41, 'a name char follows? (then keep it as a name)',
          align=Align.INLINE)
d.comment(0x8a43, 'test it', align=Align.INLINE)
d.comment(0x8a46, 'yes: keep it as a name, not a token', align=Align.INLINE)
d.comment(0x8a48, 'Emit the token: A = token byte', align=Align.INLINE)
d.label(0x8a48, 'tok_emit_token')
d.comment(0x8a49, 'flag bit 6: pseudo-variable?', align=Align.INLINE)
d.comment(0x8a4b, 'no', align=Align.INLINE)
d.comment(0x8a4d, 'at the start of a statement?', align=Align.INLINE)
d.comment(0x8a4f, 'no', align=Align.INLINE)
d.comment(0x8a51, 'superfluous: all paths reach here carry-clear',
          align=Align.INLINE)
d.comment(0x8a52, 'assignment form: token + &40', align=Align.INLINE)
d.comment(0x8a54, 'Write the token over the keyword', align=Align.INLINE)
d.label(0x8a54, 'tok_write_token')
d.comment(0x8a55, 'overwrite the keyword', align=Align.INLINE)
d.comment(0x8a58, 'reset Y', align=Align.INLINE)
d.comment(0x8a5a, 'X = &FF (mid-statement marker)', align=Align.INLINE)
d.comment(0x8a5c, 'Apply the state-change flags:', align=Align.INLINE)
d.comment(0x8a5e, 'bit 0 (already used)', align=Align.INLINE)
d.comment(0x8a5f, 'bit 1: enter middle-of-statement?', align=Align.INLINE)
d.comment(0x8a60, 'no', align=Align.INLINE)
d.comment(0x8a62, 'set middle-of-statement', align=Align.INLINE)
d.comment(0x8a64, 'clear the line-number flag', align=Align.INLINE)
d.comment(0x8a66, 'bit 2: enter start-of-statement?', align=Align.INLINE)
d.label(0x8a66, 'tok_flag_start_stmt')
d.comment(0x8a67, 'no', align=Align.INLINE)
d.comment(0x8a69, 'set start-of-statement', align=Align.INLINE)
d.comment(0x8a6b, 'clear the line-number flag', align=Align.INLINE)
d.comment(0x8a6d, 'bit 3: FN/PROC (do not tokenise the name)?', align=Align.INLINE)
d.label(0x8a6d, 'tok_flag_fnproc')
d.comment(0x8a6e, 'no', align=Align.INLINE)
d.comment(0x8a70, 'save A', align=Align.INLINE)
d.comment(0x8a71, 'skip the FN/PROC name untokenised:', align=Align.INLINE)
d.comment(0x8a72, 'char', align=Align.INLINE)
d.label(0x8a72, 'tok_skip_fnproc_loop')
d.comment(0x8a74, 'alphanumeric?', align=Align.INLINE)
d.comment(0x8a77, 'no: end of the name', align=Align.INLINE)
d.comment(0x8a79, 'advance', align=Align.INLINE)
d.comment(0x8a7c, 'loop', align=Align.INLINE)
d.comment(0x8a7f, 'step back', align=Align.INLINE)
d.label(0x8a7f, 'tok_skip_fnproc_done')
d.comment(0x8a80, 'restore A', align=Align.INLINE)
d.comment(0x8a81, 'bit 4: start a line number?', align=Align.INLINE)
d.label(0x8a81, 'tok_flag_linenum')
d.comment(0x8a82, 'no', align=Align.INLINE)
d.comment(0x8a84, 'set the line-number flag', align=Align.INLINE)
d.comment(0x8a86, 'bit 5: skip the rest of the line (REM/DATA)?', align=Align.INLINE)
d.label(0x8a86, 'tok_flag_skipline')

d.comment(0x8a87, 'yes: stop tokenising', align=Align.INLINE)
d.comment(0x8a89, 'continue scanning', align=Align.INLINE)

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
d.comment(0x8a8c, 'Get the secondary text offset', align=Align.INLINE)
d.comment(0x8a8e, 'advance it', align=Align.INLINE)
d.comment(0x8a90, 'Read the character', align=Align.INLINE)
d.comment(0x8a92, 'Loop while the character is a space', align=Align.INLINE)
d.char_literal(0x8a93)

d.comment(0x8a94, 'Space: keep skipping', align=Align.INLINE)
d.comment(0x8a96, 'Return the first non-space character', align=Align.INLINE)

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
# skip_spaces (&8A97) / skip_spaces_ptr2 (&8A8C)
d.comment(0x8a97, 'Get the text offset', align=Align.INLINE)
d.comment(0x8a99, 'advance it for next time', align=Align.INLINE)
d.comment(0x8a9b, 'Read the character', align=Align.INLINE)
d.comment(0x8a9d, 'Loop while the character is a space', align=Align.INLINE)
d.char_literal(0x8a9e)
d.comment(0x8a9f, 'Space: keep skipping', align=Align.INLINE)
d.comment(0x8aa1, 'Return the first non-space character', align=Align.INLINE)
d.comment(0x8aa2, 'BRK error block ("Missing ,") follows', align=Align.INLINE)
d.subroutine(
    0x8aa2, 'missing_comma',
    title='Raise "Missing ," error',
    description="""Raise BASIC error &05, "Missing ,", via a BRK error block. Reached
from the argument-list parsers when a required comma is absent. Does
not return.
""",
    on_exit={
        'control': 'raises BRK error &05 "Missing ,"; does not return to the caller',
    },
)
d.subroutine(
    0x8aae, 'skip_spaces_expect_comma',
    title='Skip spaces and require a comma',
    description="""Skip spaces at PtrB, then check the character is a comma.
Raises "Missing ," if it is not. Used by statements that take a
comma-separated argument list.
""",
    on_entry={'zp_text_ptr2 (&19/&1A)': 'PtrB at the parser position'},
    on_exit={'A': 'the comma (consumed)',
             'zp_text_ptr2_off (&1B)': 'advanced past the comma',
             'BRK': 'Missing , if a comma is absent'},
)
# skip_spaces_expect_comma (&8AAE)
d.comment(0x8aae, 'Skip spaces at PtrB', align=Align.INLINE)
d.comment(0x8ab1, 'Require a comma', align=Align.INLINE)
d.char_literal(0x8ab2)
d.comment(0x8ab3, 'Missing: "Missing ," error', align=Align.INLINE)
d.comment(0x8ab5, 'Return', align=Align.INLINE)
# stmt_old (&8AB6): OLD - recover a NEWed program.
d.comment(0x8ab6, 'Check the statement ends', align=Align.INLINE)
d.comment(0x8ab9, 'Point at PAGE', align=Align.INLINE)
d.comment(0x8abb, 'high byte (&38),', align=Align.INLINE)
d.comment(0x8abd, 'low byte 0,', align=Align.INLINE)
d.comment(0x8abf, 'to &37', align=Align.INLINE)
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

# Scattered tails.
d.comment(0x8ada, 'Check the statement ends', align=Align.INLINE)
# ----------------------------------------------------------------------
# Interpreter core: the immediate loop, line execution, the statement
# loop, and the token dispatch that drives the fn_*/stmt_* handlers.
# ----------------------------------------------------------------------
d.subroutine(
    0x8add, 'start_new_program',
    title='Clear program and enter the immediate loop',
    description="""Entered from language_startup. Sets up an empty program (a CR
and an &FF end marker at PAGE, TOP = PAGE+2), clears variables/heap/stack,
and falls through into the immediate loop. Does not return.
""",
    on_entry={'zp_page (&18)': 'PAGE, the start of program memory'},
    on_exit={'control': 'falls into immediate_loop (does not return)'},
)
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

d.label(0x8af3, 'clear_then_immediate')
d.subroutine(
    0x8af6, 'immediate_loop',
    title='Immediate ("> ") loop',
    description="""Print the prompt, read a line into the input buffer (PtrA =
&0700), and tokenise it. A line that begins with a line number is
inserted into the program; otherwise it is executed immediately. The
top-level loop - does not return.
""",
    on_exit={'control': 'loops forever reading and running immediate lines'},
)
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
d.char_literal(0x8b07)
d.comment(0x8b08, 'Print it and read a line into the buffer', align=Align.INLINE)

d.subroutine(
    0x8b0b, 'execute_line',
    title='Execute the line at the program pointer',
    description="""Run the tokenised statements on the line addressed by the
program pointer (zp_text_ptr, &0B), starting at offset zp_text_ptr_off.
Resets the error handler and the 6502 stack, tokenises the line, and
either inserts a numbered line or runs it via the statement loop.
""",
    on_entry={'zp_text_ptr (&0B/&0C)': 'the line to execute',
              'zp_text_ptr_off (&0A)': 'the starting offset'},
    on_exit={'control': 'runs the line (numbered lines are inserted instead)'},
)
# --- interpreter core: execute_line / statement_loop / dispatch ------
d.comment(0x8b0b, 'Restore the default error handler (ON ERROR OFF)',
          align=Align.INLINE)
# execute_line (&8B0B) and the immediate-mode dispatch gaps.
d.comment(0x8b0d, 'low byte = &33,', align=Align.INLINE)
d.comment(0x8b0f, 'high byte = &B4,', align=Align.INLINE)
d.comment(0x8b11, 'store it (handler at &B433)', align=Align.INLINE)
d.comment(0x8b13, 'OPT = &FF: not inside the [ ] assembler', align=Align.INLINE)
d.comment(0x8b15, 'store the OPT flag', align=Align.INLINE)
d.comment(0x8b17, 'Arm line-number encoding (&3C) for a leading line number',
          align=Align.INLINE)
d.comment(0x8b19, 'Reset the 6502 hardware stack', align=Align.INLINE)
d.comment(0x8b1a, 'Clear the DATA pointer and the BASIC stacks',
          align=Align.INLINE)
d.comment(0x8b1d, 'Y = 0', align=Align.INLINE)
d.comment(0x8b1e, 'Point the general pointer at the line text',
          align=Align.INLINE)
d.comment(0x8b20, 'low byte,', align=Align.INLINE)
d.comment(0x8b22, 'high byte,', align=Align.INLINE)
d.comment(0x8b24, 'store it', align=Align.INLINE)
d.comment(0x8b26, 'start of statement (&3B = 0)', align=Align.INLINE)
d.comment(0x8b28, 'and the offset', align=Align.INLINE)
d.comment(0x8b2a, 'Tokenise (&3C pre-armed for a leading number)',
          align=Align.INLINE)
d.comment(0x8b2d, 'reuse the &8D codec: decode the leading line number',
          align=Align.INLINE)
d.comment(0x8b30, 'no line number: execute it', align=Align.INLINE)
d.comment(0x8b32, 'numbered line: insert it (IWA = the line number)',
          align=Align.INLINE)
d.comment(0x8b35, 'inserted: immediate loop', align=Align.INLINE)
d.comment(0x8b38, 'Skip spaces', align=Align.INLINE)
d.label(0x8b38, 'exec_dispatch')
d.comment(0x8b3b, 'Token >= &C6 is a command: dispatch it', align=Align.INLINE)
d.comment(0x8b3d, 'command token: dispatch it', align=Align.INLINE)
d.comment(0x8b3f, 'Otherwise treat it as a variable assignment',
          align=Align.INLINE)
d.comment(0x8b41, 'Back to immediate mode', align=Align.INLINE)
d.label(0x8b41, 'exec_immediate')
d.comment(0x8b44, 'Enter the assembler', align=Align.INLINE)
d.label(0x8b44, 'exec_assembler')
d.comment(0x8b47, 'Inside a function call?', align=Align.INLINE)
d.label(0x8b47, 'fn_return')
d.comment(0x8b48, 'stack near empty (no FN frame)?', align=Align.INLINE)
d.comment(0x8b4a, 'no: error', align=Align.INLINE)
d.comment(0x8b4c, 'Pushed token', align=Align.INLINE)
d.comment(0x8b4f, 'FN?', align=Align.INLINE)
d.comment(0x8b51, 'no: error', align=Align.INLINE)
d.comment(0x8b53, 'Evaluate the return value', align=Align.INLINE)
d.comment(0x8b56, 'check end, return from the function', align=Align.INLINE)
d.comment(0x8b59, 'No FN error', align=Align.INLINE)
d.label(0x8b59, 'no_fn_error')
d.subroutine(
    0x8b60, 'check_eq_star_bracket',
    title='Check for =, * and [ statements',
    description="""Recognise the statement forms that are not introduced by a
token: "=" (return a value from FN), "*" (pass the rest of the line
to OSCLI), and "[" (enter the inline assembler). Dispatches to the
matching handler, otherwise checks for end of statement.
""",
    on_entry={'zp_text_ptr (&0B/&0C)': 'the program text pointer (PtrA)',
              'zp_text_ptr_off (&0A)': 'offset just past the introducing character'},
    on_exit={'control': 'tail-jumps to the FN-return, OSCLI or assembler handler, '
                        'else falls into the end-of-statement check'},
)
# check_eq_star_bracket (&8B60)
d.comment(0x8b60, 'Step back to the introducing character', align=Align.INLINE)
d.comment(0x8b62, 'one character back', align=Align.INLINE)
d.comment(0x8b63, 'fetch it', align=Align.INLINE)
d.comment(0x8b65, '"=" returns a value from a function (FN)', align=Align.INLINE)
d.char_literal(0x8b66)
d.comment(0x8b67, '"=": return a value from a function', align=Align.INLINE)
d.comment(0x8b69, '"*" passes the rest of the line to OSCLI', align=Align.INLINE)
d.char_literal(0x8b6a)
d.comment(0x8b6b, '"*": an embedded OSCLI command', align=Align.INLINE)
d.comment(0x8b6d, '"[" enters the inline assembler', align=Align.INLINE)
d.char_literal(0x8b6e)
d.comment(0x8b6f, '"[": enter the assembler', align=Align.INLINE)
d.comment(0x8b71, 'otherwise check for end of statement', align=Align.INLINE)
d.label(0x8b73, 'exec_star_command')   # embedded *command -> OSCLI

d.comment(0x8b73, 'Point PtrA at the command text', align=Align.INLINE)
d.comment(0x8b76, 'XY -> the command string', align=Align.INLINE)
d.comment(0x8b78, '(high byte)', align=Align.INLINE)
d.comment(0x8b7a, 'Pass it to OSCLI', align=Align.INLINE)

d.comment(0x8b7d, 'CR', align=Align.INLINE)
d.comment(0x8b7f, 'Line offset', align=Align.INLINE)
d.comment(0x8b81, 'back up one (the loop pre-increments)', align=Align.INLINE)
d.comment(0x8b82, 'Scan to the end of line', align=Align.INLINE)
d.label(0x8b82, 'data_scan_loop')
d.comment(0x8b83, 'reached the CR?', align=Align.INLINE)
d.comment(0x8b85, 'no: keep scanning', align=Align.INLINE)
d.comment(0x8b87, 'ELSE?', align=Align.INLINE)
d.label(0x8b87, 'stmt_eol')
d.comment(0x8b89, 'yes: skip to end of line', align=Align.INLINE)
d.comment(0x8b8b, 'In the command buffer?', align=Align.INLINE)
d.comment(0x8b8d, 'page &07 (command buffer)?', align=Align.INLINE)
d.comment(0x8b8f, 'yes: immediate mode', align=Align.INLINE)
d.comment(0x8b91, 'Check for end of program, step past CR', align=Align.INLINE)
d.comment(0x8b94, 'more: next statement', align=Align.INLINE)

d.comment(0x8b96, 'Back up', align=Align.INLINE)
d.label(0x8b96, 'stmt_backup_end')
d.comment(0x8b98, 'check the statement ends', align=Align.INLINE)
d.label(0x8b98, 'stmt_check_end')
d.subroutine(
    0x8b9b, 'statement_loop',
    title='Statement execution loop',
    description="""The main interpreter loop: fetch the next statement's leading
token and dispatch it, then advance to the next statement (after a
colon) or line. Statement handlers jmp back here when they finish, so
it is the common continuation rather than a callable subroutine.
""",
    on_entry={'zp_text_ptr (&0B/&0C)': 'the program text pointer (PtrA)',
              'zp_text_ptr_off (&0A)': 'offset at the next statement'},
    on_exit={'control': 'dispatches the statement; handlers return here'},
)
d.comment(0x8b9b, 'Fetch the next character of the statement',
          align=Align.INLINE)
# statement_loop (&8B9B) remaining
d.comment(0x8b9d, 'Get the current character', align=Align.INLINE)
d.comment(0x8b9f, 'A colon separates statements on a line', align=Align.INLINE)
d.char_literal(0x8ba0)
d.comment(0x8ba1, 'Not a colon: check for ELSE / end of line', align=Align.INLINE)
d.comment(0x8ba3, 'Skip spaces to the next statement', align=Align.INLINE)
d.subroutine(
    0x8ba3, 'next_statement',
    title='Execute the next statement on the line',
    description="""The interpreter's per-statement entry point. Read the character at
PtrA+offset while advancing zp_text_ptr_off (&0A) past the ':'
separator, skipping spaces. A token >= &CF falls into dispatch_token,
which indexes the action-address table and JMP (&0037)s to its
handler; a byte below &CF is not a command token, so it branches to
try_variable_assignment for an implied LET. Non-returning: every path
transfers to a statement handler.
""",
    on_entry={
        'zp_text_ptr (&0B)': 'the program text pointer (PtrA)',
        'zp_text_ptr_off (&0A)': "offset at the statement start (the ':' or first character)",
    },
    on_exit={
        'control': 'non-returning; dispatches via dispatch_token JMP (&0037) to a keyword handler, or branches to try_variable_assignment',
    },
)
d.comment(0x8ba5, 'advance past the colon', align=Align.INLINE)
d.comment(0x8ba7, 'Get the next character', align=Align.INLINE)
d.comment(0x8ba9, 'Skip spaces', align=Align.INLINE)
d.char_literal(0x8baa)
d.comment(0x8bab, 'loop', align=Align.INLINE)
d.comment(0x8bad, 'Below &CF: a variable assignment, not a command',
          align=Align.INLINE)
d.comment(0x8baf, 'Below &CF: a variable assignment', align=Align.INLINE)

d.subroutine(
    0x8bb1, 'dispatch_token',
    title='Dispatch a tokenised function or command',
    description="""Index the action-address table by (token - &8E): load the
handler address into zp_general (&37/&38) and JMP (&0037). This is
the indirect jump that reaches every fn_* / stmt_* handler.
""",
    on_entry={'A': 'a command/function token (&8E-&FF)'},
)
# dispatch_token (&8BB1) remaining
d.comment(0x8bb1, 'Token to X for indexing', align=Align.INLINE)
d.comment(0x8bb2, 'Handler low byte = action_table_lo[token - &8E]',
          align=Align.INLINE)
# The statement dispatcher indexes the action-address tables by the raw
# token (&8E..&FF): `lda action_table_lo - &8E,x`. The -&8E bases (&82DF /
# &8351) fall inside the keyword table, so express them as offsets from
# action_table_lo/hi rather than labels there (which would collide with
# the keyword strings, e.g. &8351 is the "E" of PAGE).
d.expr(0x8bb3, ref(ACTION_TABLE_LO) - 0x8e)   # lda action_table_lo - &8E,x
d.comment(0x8bb5, 'Store the handler low byte', align=Align.INLINE)
d.comment(0x8bb7, 'Handler high byte from action_table_hi', align=Align.INLINE)
d.expr(0x8bb8, ref(ACTION_TABLE_HI) - 0x8e)   # lda action_table_hi - &8E,x
# ----------------------------------------------------------------------
# Inline-assembler mnemonic tables (&8450-&84FC).
# ----------------------------------------------------------------------
d.banner(
    ASM_MNEMONIC_LO,
    title='Inline-assembler mnemonic tables',
    description="""Three parallel byte arrays, all indexed by the same X, that turn a
typed mnemonic into a base opcode:

| Array           | Holds                                     |
|-----------------|-------------------------------------------|
| asm_mnemonic_lo | low byte of the mnemonic's packed-name hash |
| asm_mnemonic_hi | high byte of the mnemonic's packed-name hash |
| asm_base_opcode | the base ("mode 0") opcode for that mnemonic |

[`asm_parse_mnemonic`](address:85ba) reads the three mnemonic letters, keeps the
low 5 bits of each (A=1..Z=26) and packs them MSB-first into a 15-bit
value in `&3D` (low) / `&3E` (high). [`asm_mn_search`](address:85f1) then scans X
from &3A down to 1, comparing the low half against `asm_mnemonic_lo,x`
and, on a hit, the high half against [`asm_mnemonic_hi`](address:848b),x; the matching
index selects [`asm_base_opcode`](address:84c5),x. Tokenised `AND`/`EOR`/`OR` reach the same
indices directly via [`asm_logic_mnemonic`](address:8607).

Because the two hash tables are pure functions of the mnemonic text,
each `asm_mnemonic_lo` / `asm_mnemonic_hi` byte is emitted as the beebasm
expression that re-derives it from the three letters (the assembled
value is shown in the address comment). `asm_base_opcode` holds real
6502 opcodes and stays a plain byte.

The index order is meaningful: the operand parser keys its
addressing-mode handler off `cpx` thresholds on the matched index.

| Index   | Mnemonics     | Operand form               |
|---------|---------------|----------------------------|
| &01-&19 | BRK..TYA      | implied (opcode only)      |
| &1A-&21 | BCC..BVS      | relative branch            |
| &22-&28 | AND..SBC      | #/zp/abs/(zp,X)/(zp),Y/,X/,Y|
| &29-&2C | ASL..ROR      | accumulator (A) or memory  |
| &2D-&2E | DEC, INC      | memory only                |
| &2F-&30 | CPX, CPY      | #/zp/abs                   |
| &31     | BIT           | abs/zp                     |
| &32-&33 | JMP, JSR      | abs; JMP also (abs)        |
| &34-&36 | LDX, LDY, STA | with index register        |
| &37-&38 | STX, STY      | two-register form          |
| &39     | OPT           | directive (sets OPT flag)  |
| &3A     | EQU           | directive (EQUB/W/D/S)     |

Base opcodes are each group's column-0 value; the operand parser adds
addressing-mode offsets via [`asm_opcode_add4`](address:8832) / [`add8`](address:882f) / [`add16`](address:882c), so a few bases (e.g.
`BIT &20`, `LDX`/`LDY`-immediate `&A2`/`&A0`) are the slot value, not a legal
standalone opcode. `OPT` (&39) and `EQU` (&3A) are directives and have no
`asm_base_opcode` entry.

The tables are indexed 1-based by the mnemonic number: the scan runs X
from &3A (EQU) down to 1 (BRK), so each label sits on entry 1 (BRK) and
the code reads the table as `<label> - 1,x` (the [`&85F5`](address:85f5) / [`&85FA`](address:85fa) / [`&8620`](address:8620)
sites).""",
)

# The tables are indexed 1-based (X = the mnemonic number 1..58): each
# label sits on entry 1 (BRK), one past its *_BASE, so the code reads
# them as `<label> - 1,x`. The loops walk *_BASE + i for i in 1..N and
# emit one EQUB item per byte so each per-index inline comment gets its
# own line.
d.index_base(ASM_MNEMONIC_LO, 'asm_mnemonic_lo')
for _i in range(1, len(ASM_MNEMONICS)):             # 1..58 (BRK..EQU)
    d.byte(ASM_MNEMONIC_LO_BASE + _i, 1, override=True)
    d.expr(ASM_MNEMONIC_LO_BASE + _i, pack_mnemonic_lo(ASM_MNEMONICS[_i]))
    _dir = ' directive' if _i >= 0x39 else ''
    d.comment(ASM_MNEMONIC_LO_BASE + _i,
              f'[&{_i:02x}] {ASM_MNEMONICS[_i]}{_dir} lo-byte',
              align=Align.INLINE)

d.index_base(ASM_MNEMONIC_HI, 'asm_mnemonic_hi')
for _i in range(1, len(ASM_MNEMONICS)):             # 1..58 (BRK..EQU)
    d.byte(ASM_MNEMONIC_HI_BASE + _i, 1, override=True)
    d.expr(ASM_MNEMONIC_HI_BASE + _i, pack_mnemonic_hi(ASM_MNEMONICS[_i]))
    _dir = ' directive' if _i >= 0x39 else ''
    d.comment(ASM_MNEMONIC_HI_BASE + _i,
              f'[&{_i:02x}] {ASM_MNEMONICS[_i]}{_dir} hi-byte',
              align=Align.INLINE)

d.index_base(ASM_BASE_OPCODE, 'asm_base_opcode')
for _i in range(1, len(ASM_BASE_OPCODES)):          # 1..56 (BRK..STY)
    d.byte(ASM_BASE_OPCODE_BASE + _i, 1, override=True)
    d.comment(ASM_BASE_OPCODE_BASE + _i,
              f'[&{_i:02x}] {ASM_MNEMONICS[_i]}: base opcode '
              f'&{ASM_BASE_OPCODES[_i]:02x}', align=Align.INLINE)

d.comment(0x8bba, 'Store the handler high byte', align=Align.INLINE)

d.comment(0x8bbc, 'Jump to the keyword handler', align=Align.INLINE)
d.subroutine(
    0x8bbf, 'try_variable_assignment',
    title='Not a command token: try an assignment',
    description="""Reached when the statement does not begin with a command token:
copy PtrA to PtrB, parse a variable / indirection reference, and perform
an implied-LET assignment (creating the variable if new). Falls back to
the =, * (OSCLI) or [ (assembler) special statement forms.
""",
    on_entry={'zp_text_ptr (&0B/&0C)': 'the program text pointer (PtrA)',
              'Y': 'offset of the statement start'},
    on_exit={'control': 'performs the assignment then rejoins statement_loop, '
                        'or dispatches to the =, * or [ form'},
)
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
d.label(0x8bdf, 'assign_new_var')
d.comment(0x8be2, 'Step back, continue', align=Align.INLINE)

d.comment(0x8be4, 'Parse the variable being assigned', align=Align.INLINE)
# stmt_let (&8BE4) remaining gaps.
d.comment(0x8be7, 'end of statement: error', align=Align.INLINE)
d.comment(0x8be9, 'numeric target?', align=Align.INLINE)
d.label(0x8be9, 'let_assign')
d.comment(0x8beb, 'Stack the destination address', align=Align.INLINE)
d.comment(0x8bee, 'Expect "=" and evaluate the right-hand side',
          align=Align.INLINE)
d.comment(0x8bf1, 'value type', align=Align.INLINE)
d.comment(0x8bf3, 'A string variable needs a string value', align=Align.INLINE)
d.comment(0x8bf5, 'Store the string', align=Align.INLINE)
d.comment(0x8bf8, 'next statement', align=Align.INLINE)
d.comment(0x8bfb, 'Stack the destination address', align=Align.INLINE)
d.label(0x8bfb, 'let_numeric')
d.comment(0x8bfe, 'Expect "=" and evaluate', align=Align.INLINE)
d.comment(0x8c01, 'value type', align=Align.INLINE)
d.comment(0x8c03, 'A numeric variable needs a numeric value', align=Align.INLINE)
d.comment(0x8c05, 'Store the number', align=Align.INLINE)
d.comment(0x8c08, 'next statement', align=Align.INLINE)
d.comment(0x8c0b, 'Mistake (syntax) error', align=Align.INLINE)

d.label(0x8c0b, 'let_mistake')

d.subroutine(
    0x8c0e, 'err_type_mismatch',
    title='Raise "Type mismatch" error',
    description="""Raise BASIC error &06, "Type mismatch", via a BRK error block. Reached
(18 callers) whenever a routine finds a string where a number is
required, or vice versa. Does not return.
""",
    on_exit={
        'control': 'raises BRK error &06 "Type mismatch"; does not return to the caller',
    },
)
d.comment(0x8c0e, 'Type mismatch error', align=Align.INLINE)
d.subroutine(
    0x8c1e, 'assign_string',
    title='Store a string value into a variable',
    description="""Assign the string in the string buffer to the string variable
whose descriptor address is on the stack. Reuses the existing
allocation if the new string fits, otherwise grabs fresh space from
the heap.
""",
    on_entry={'(zp_stack_ptr) (&04/&05)': 'the variable descriptor address',
              'string_work (&0600)': 'the string characters',
              'zp_strbuf_len (&36)': 'the string length'},
    on_exit={'the string variable': 'updated (allocation reused or grown)'},
)
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
# assign_string
d.subroutine(
    0x8c21, 'assign_string_to',
    title='Assign a string to a variable descriptor already in IWA',
    description="""Alternate entry to assign_string that assumes the variable descriptor
address is already in zp_iwa (&2A/&2B) rather than on the stack.
Assign the string in the string buffer to that variable, reusing the
existing allocation if the new string fits, otherwise growing it in
place or grabbing fresh heap space.
""",
    on_entry={
        'zp_iwa (&2A/&2B)': 'the variable descriptor address',
        'zp_iwa_2 (&2C)': 'the variable type (&80 = absolute $-string address)',
        'string_work (&0600)': 'the string characters',
        'zp_strbuf_len (&36)': 'the string length',
    },
)
d.comment(0x8c23, 'An absolute $-string address?', align=Align.INLINE)
d.comment(0x8c25, 'yes', align=Align.INLINE)
d.comment(0x8c27, 'Bytes currently allocated', align=Align.INLINE)
d.comment(0x8c29, 'read it', align=Align.INLINE)
d.comment(0x8c2b, 'Does the new string fit the existing allocation?',
          align=Align.INLINE)
d.comment(0x8c2d, 'yes: reuse the allocation', align=Align.INLINE)
d.comment(0x8c2f, 'Tentative new address = heap top', align=Align.INLINE)

d.comment(0x8c31, '(low)', align=Align.INLINE)
d.comment(0x8c33, 'high...', align=Align.INLINE)
d.comment(0x8c35, '(high)', align=Align.INLINE)
d.comment(0x8c37, 'Round the size up (min 8, granularity 8)', align=Align.INLINE)
d.comment(0x8c39, 'at least 8?', align=Align.INLINE)
d.comment(0x8c3b, 'under 8: take it as is', align=Align.INLINE)
d.comment(0x8c3d, 'else add 7 (round up),', align=Align.INLINE)
d.comment(0x8c3f, 'no overflow', align=Align.INLINE)
d.comment(0x8c41, 'cap at 255', align=Align.INLINE)
d.comment(0x8c43, '(clear carry)', align=Align.INLINE)
d.label(0x8c43, 'assign_str_alloc_size')
d.comment(0x8c44, 'Save the new allocation size', align=Align.INLINE)
d.comment(0x8c45, 'keep the size in X', align=Align.INLINE)
d.comment(0x8c46, 'Is the existing block at the heap top?', align=Align.INLINE)
d.comment(0x8c48, 'offset 0 (data low)', align=Align.INLINE)
d.comment(0x8c4a, '(data address + allocated == top?)', align=Align.INLINE)
d.comment(0x8c4c, 'compare with heap top low', align=Align.INLINE)
d.comment(0x8c4e, 'no: allocate fresh space', align=Align.INLINE)
d.comment(0x8c50, 'high byte:', align=Align.INLINE)
d.comment(0x8c51, '+ allocated,', align=Align.INLINE)
d.comment(0x8c53, '== heap top high?', align=Align.INLINE)
d.comment(0x8c55, 'no: allocate fresh space', align=Align.INLINE)
d.comment(0x8c57, 'yes: extend in place from this block', align=Align.INLINE)
d.comment(0x8c59, 'new size...', align=Align.INLINE)
d.comment(0x8c5a, 'offset 2 (old allocation)', align=Align.INLINE)
d.comment(0x8c5b, 'new - old...', align=Align.INLINE)
d.comment(0x8c5c, 'reclaim the old allocation', align=Align.INLINE)
d.comment(0x8c5e, 'X = extra bytes needed', align=Align.INLINE)
d.comment(0x8c5f, 'New heap top = top + allocation', align=Align.INLINE)
d.label(0x8c5f, 'assign_str_alloc')
d.comment(0x8c60, '(clear carry)', align=Align.INLINE)
d.comment(0x8c61, '+ heap top low,', align=Align.INLINE)
d.comment(0x8c63, '(low in Y)', align=Align.INLINE)
d.comment(0x8c64, 'heap top high...', align=Align.INLINE)
d.comment(0x8c66, '+ carry (new top high)', align=Align.INLINE)
d.comment(0x8c68, 'collides with the stack?', align=Align.INLINE)
d.comment(0x8c6a, '(keep the new top high)', align=Align.INLINE)
d.comment(0x8c6b, 'new top - stack pointer', align=Align.INLINE)
d.comment(0x8c6d, 'yes: No room', align=Align.INLINE)
d.comment(0x8c6f, 'Commit the new heap top', align=Align.INLINE)
d.comment(0x8c71, '(high)', align=Align.INLINE)
d.comment(0x8c73, 'Store the new allocation size', align=Align.INLINE)
d.comment(0x8c74, 'offset 2', align=Align.INLINE)
d.comment(0x8c76, '(store)', align=Align.INLINE)
d.comment(0x8c78, 'Store the new data address', align=Align.INLINE)
d.comment(0x8c79, 'data address high', align=Align.INLINE)
d.comment(0x8c7b, 'extended in place: keep the address', align=Align.INLINE)
d.comment(0x8c7d, 'store the data high,', align=Align.INLINE)
d.comment(0x8c7f, 'offset 0', align=Align.INLINE)
d.comment(0x8c80, 'data low...', align=Align.INLINE)
d.comment(0x8c82, '(store)', align=Align.INLINE)
d.comment(0x8c84, 'Store the current length', align=Align.INLINE)
d.label(0x8c84, 'assign_str_store')
d.comment(0x8c86, 'the length', align=Align.INLINE)
d.comment(0x8c88, '(store)', align=Align.INLINE)
d.comment(0x8c8a, 'empty string: done', align=Align.INLINE)
d.comment(0x8c8c, 'Fetch the data address', align=Align.INLINE)
d.comment(0x8c8d, '(to offset 1)', align=Align.INLINE)
d.comment(0x8c8e, 'high...', align=Align.INLINE)
d.comment(0x8c90, '(high)', align=Align.INLINE)
d.comment(0x8c92, 'offset 0', align=Align.INLINE)
d.comment(0x8c93, 'low...', align=Align.INLINE)
d.comment(0x8c95, '(low)', align=Align.INLINE)
d.comment(0x8c97, 'Copy the string buffer to the storage', align=Align.INLINE)
d.label(0x8c97, 'assign_str_copy_loop')
d.comment(0x8c9a, 'to storage', align=Align.INLINE)
d.comment(0x8c9c, 'next', align=Align.INLINE)
d.comment(0x8c9d, 'done?', align=Align.INLINE)
d.comment(0x8c9f, 'loop', align=Align.INLINE)
d.comment(0x8ca1, 'Return', align=Align.INLINE)
d.comment(0x8ca2, '$addr: prepare the destination', align=Align.INLINE)
d.label(0x8ca2, 'assign_str_addr')
d.comment(0x8ca5, 'empty string?', align=Align.INLINE)
d.comment(0x8ca7, 'yes: just the terminator', align=Align.INLINE)
d.comment(0x8ca9, 'Copy the string to the address', align=Align.INLINE)
d.label(0x8ca9, 'assign_str_addr_loop')
d.comment(0x8cac, 'store it', align=Align.INLINE)
d.comment(0x8cae, 'next (downwards)', align=Align.INLINE)
d.comment(0x8caf, 'loop', align=Align.INLINE)
d.comment(0x8cb1, 'First character', align=Align.INLINE)
d.comment(0x8cb4, 'Store it (with the CR terminator following)',
          align=Align.INLINE)
d.label(0x8cb4, 'assign_str_addr_cr')
d.comment(0x8cb6, 'Return', align=Align.INLINE)
d.subroutine(
    0x8cb7, 'err_no_room',
    title='Raise the "No room" error',
    description="""Raise BASIC error &00, "No room", via a BRK error block. Reached when
there is insufficient memory for the requested operation. Does not
return.
""",
    on_exit={
        'control': 'raises BRK error &00 "No room"; does not return to the caller',
    },
)

d.comment(0x8cb7, 'No room error', align=Align.INLINE)

d.subroutine(0x8cc1, 'unstack_value_to_var',
             title='Restore a stacked value into a variable',
             description='Pop the value on top of the BASIC stack into the '
                         'variable at zp_general, dispatched by the type/size '
                         'byte: a numeric value of that many bytes, a $addr '
                         'string (CR terminated), or a string variable '
                         '(copied into its heap allocation). Used by the '
                         'FN/PROC LOCAL and parameter machinery.',
             on_entry={'zp_general (&37/&38)': 'the destination variable address',
                       'zp_fileblk (&39)': 'the type/size byte',
                       '(zp_stack_ptr) (&04/&05)': 'the saved value on top of stack'},
             on_exit={'the variable': 'restored from the stack',
                      'zp_stack_ptr': 'advanced past the popped value'})
# unstack_value_to_var (&8CC1): pop a stacked value into a variable.
d.comment(0x8cc1, 'Type/size byte', align=Align.INLINE)
d.comment(0x8cc3, '$addr string?', align=Align.INLINE)
d.comment(0x8cc5, 'yes', align=Align.INLINE)
d.comment(0x8cc7, 'numeric?', align=Align.INLINE)
d.comment(0x8cc9, 'String variable: length on the stack', align=Align.INLINE)
d.comment(0x8ccb, 'read the length,', align=Align.INLINE)
d.comment(0x8ccd, 'into X as the byte count', align=Align.INLINE)
d.comment(0x8cce, 'empty: just set the length', align=Align.INLINE)
d.comment(0x8cd0, 'Data address - 1 (for 1-based copy)', align=Align.INLINE)
d.comment(0x8cd2, 'low byte - 1,', align=Align.INLINE)
d.comment(0x8cd4, 'dest pointer low (&39),', align=Align.INLINE)
d.comment(0x8cd6, 'next', align=Align.INLINE)
d.comment(0x8cd7, 'high byte', align=Align.INLINE)
d.comment(0x8cd9, '- borrow,', align=Align.INLINE)
d.comment(0x8cdb, 'dest pointer high (&3A)', align=Align.INLINE)
d.comment(0x8cdd, 'Copy the string bytes', align=Align.INLINE)
# unstack_value_to_var
d.label(0x8cdd, 'unstack_str_copy')
d.comment(0x8cdf, 'into the heap allocation,', align=Align.INLINE)
d.comment(0x8ce1, 'next byte,', align=Align.INLINE)
d.comment(0x8ce2, 'count down', align=Align.INLINE)
d.comment(0x8ce3, 'loop', align=Align.INLINE)
d.comment(0x8ce5, 'String length', align=Align.INLINE)
d.label(0x8ce5, 'unstack_str_setlen')
d.comment(0x8ce7, 'descriptor offset 3', align=Align.INLINE)
d.comment(0x8ce9, 'Store the length', align=Align.INLINE)
d.label(0x8ce9, 'unstack_str_drop')
d.comment(0x8ceb, 'drop the value from the stack', align=Align.INLINE)
d.comment(0x8cee, '$addr: length on the stack', align=Align.INLINE)
d.label(0x8cee, 'unstack_addr')
d.comment(0x8cf0, 'read the length,', align=Align.INLINE)
d.comment(0x8cf2, 'into X as the count', align=Align.INLINE)
d.comment(0x8cf3, 'empty: just the terminator', align=Align.INLINE)
d.comment(0x8cf5, 'Copy the string to the address', align=Align.INLINE)
d.label(0x8cf5, 'unstack_addr_copy')
d.comment(0x8cf6, 'read a char from the stack,', align=Align.INLINE)
d.comment(0x8cf8, 'back to the destination offset,', align=Align.INLINE)
d.comment(0x8cf9, 'store it at the address,', align=Align.INLINE)
d.comment(0x8cfb, 'advance,', align=Align.INLINE)
d.comment(0x8cfc, 'count down', align=Align.INLINE)
d.comment(0x8cfd, 'loop', align=Align.INLINE)
d.comment(0x8cff, 'CR terminator', align=Align.INLINE)
d.label(0x8cff, 'unstack_addr_cr')
d.comment(0x8d01, 'store it', align=Align.INLINE)
d.comment(0x8d03, 'Numeric: copy byte 0', align=Align.INLINE)
d.label(0x8d03, 'unstack_numeric')
d.comment(0x8d05, 'read it,', align=Align.INLINE)
d.comment(0x8d07, 'store it,', align=Align.INLINE)
d.comment(0x8d09, 'next byte', align=Align.INLINE)
d.comment(0x8d0a, 'all bytes done?', align=Align.INLINE)
d.comment(0x8d0c, 'yes', align=Align.INLINE)
d.comment(0x8d0e, 'Copy byte 1', align=Align.INLINE)
d.comment(0x8d10, 'store it', align=Align.INLINE)
d.comment(0x8d12, 'byte 2', align=Align.INLINE)
d.comment(0x8d13, 'read it,', align=Align.INLINE)
d.comment(0x8d15, 'store it,', align=Align.INLINE)
d.comment(0x8d17, 'byte 3', align=Align.INLINE)
d.comment(0x8d18, 'read it,', align=Align.INLINE)
d.comment(0x8d1a, 'store it,', align=Align.INLINE)
d.comment(0x8d1c, 'next byte', align=Align.INLINE)
d.comment(0x8d1d, 'all bytes done?', align=Align.INLINE)
d.comment(0x8d1f, 'yes', align=Align.INLINE)
d.comment(0x8d21, 'byte 4 (real only)', align=Align.INLINE)
d.comment(0x8d23, 'store it,', align=Align.INLINE)
d.comment(0x8d25, 'next byte', align=Align.INLINE)
d.comment(0x8d26, 'Bytes copied', align=Align.INLINE)
d.label(0x8d26, 'unstack_numeric_drop')
d.comment(0x8d27, 'carry clear for the stack drop', align=Align.INLINE)
d.comment(0x8d28, 'drop them from the stack', align=Align.INLINE)

# PRINT# (&8D2B): write values to an open file via OSBPUT.
d.comment(0x8d2b, 'Back up over "#"', align=Align.INLINE)
# PRINT# file write and PRINT separators (in stmt_print's extent)
d.label(0x8d2b, 'print_file')
d.comment(0x8d2d, 'Get the file handle', align=Align.INLINE)
d.comment(0x8d30, 'Save the handle', align=Align.INLINE)
d.label(0x8d30, 'print_file_loop')
d.comment(0x8d31, '(push it)', align=Align.INLINE)
d.comment(0x8d32, 'Skip spaces', align=Align.INLINE)
d.comment(0x8d35, "','  another value?", align=Align.INLINE)
d.char_literal(0x8d36)
d.comment(0x8d37, 'no: done', align=Align.INLINE)
d.comment(0x8d39, 'Evaluate the value', align=Align.INLINE)
d.comment(0x8d3c, 'pack it (in case real)', align=Align.INLINE)
d.comment(0x8d3f, 'Recover the handle', align=Align.INLINE)
d.comment(0x8d40, 'into Y for OSBPUT', align=Align.INLINE)
d.comment(0x8d41, 'Type byte', align=Align.INLINE)
d.comment(0x8d43, 'write it', align=Align.INLINE)
d.comment(0x8d46, 'examine the type byte', align=Align.INLINE)
d.comment(0x8d47, 'string?', align=Align.INLINE)
d.comment(0x8d49, 'real?', align=Align.INLINE)
d.comment(0x8d4b, 'Integer: 4 bytes', align=Align.INLINE)
d.comment(0x8d4d, 'Write a byte', align=Align.INLINE)
d.label(0x8d4d, 'print_file_int_loop')
d.comment(0x8d4f, 'send it,', align=Align.INLINE)
d.comment(0x8d52, 'next byte (MSB first)', align=Align.INLINE)
d.comment(0x8d53, 'loop', align=Align.INLINE)
d.comment(0x8d55, 'next value', align=Align.INLINE)
d.comment(0x8d57, 'Real: 5 bytes', align=Align.INLINE)
d.label(0x8d57, 'print_file_real')
d.comment(0x8d59, 'Write a byte', align=Align.INLINE)
d.label(0x8d59, 'print_file_real_loop')
d.comment(0x8d5c, 'send it,', align=Align.INLINE)
d.comment(0x8d5f, 'next byte (MSB first)', align=Align.INLINE)
d.comment(0x8d60, 'loop', align=Align.INLINE)
d.comment(0x8d62, 'next value', align=Align.INLINE)
d.comment(0x8d64, 'String: write the length', align=Align.INLINE)
d.label(0x8d64, 'print_file_str')
d.comment(0x8d66, 'send it,', align=Align.INLINE)
d.comment(0x8d69, 'empty string?', align=Align.INLINE)
d.comment(0x8d6a, 'empty', align=Align.INLINE)
d.comment(0x8d6c, 'Write a character', align=Align.INLINE)
d.label(0x8d6c, 'print_file_str_loop')
d.comment(0x8d6f, 'send it,', align=Align.INLINE)
d.comment(0x8d72, 'next character (written in reverse)', align=Align.INLINE)
d.comment(0x8d73, 'loop', align=Align.INLINE)
d.comment(0x8d75, 'next value', align=Align.INLINE)
d.comment(0x8d77, 'Recover the handle', align=Align.INLINE)
d.label(0x8d77, 'print_file_done')
d.comment(0x8d78, 'sync the pointer', align=Align.INLINE)
d.comment(0x8d7a, 'next statement', align=Align.INLINE)

# PRINT end of statement (&8D7D) and semicolon handling.
d.comment(0x8d7d, 'Print a newline', align=Align.INLINE)
d.label(0x8d7d, 'print_newline')
d.comment(0x8d80, 'next statement', align=Align.INLINE)
d.label(0x8d80, 'print_done')
d.comment(0x8d83, 'Semicolon: clear the field width...', align=Align.INLINE)
d.label(0x8d83, 'print_semicolon')

d.comment(0x8d85, 'the field width,', align=Align.INLINE)
d.comment(0x8d87, '...and flags', align=Align.INLINE)
d.comment(0x8d89, 'Next non-space character', align=Align.INLINE)
d.comment(0x8d8c, "':' end?", align=Align.INLINE)
d.char_literal(0x8d8d)
d.comment(0x8d8e, 'yes: end without a newline', align=Align.INLINE)
d.comment(0x8d90, 'end of line?', align=Align.INLINE)
d.comment(0x8d92, 'yes', align=Align.INLINE)
d.comment(0x8d94, 'ELSE?', align=Align.INLINE)
d.comment(0x8d96, 'yes', align=Align.INLINE)
d.comment(0x8d98, 'otherwise continue the print loop', align=Align.INLINE)

# ----------------------------------------------------------------------
# stmt_print (&8D9A): the PRINT statement.
# Walks the print list, handling the @% field width and the ~ (hex), ,
# (next field) and ; (no gap) modifiers, the TAB/SPC tokens, and string
# and numeric items, padding numbers to the field width.
# ----------------------------------------------------------------------
d.comment(0x8d9a, 'Next non-space character', align=Align.INLINE)
d.comment(0x8d9d, 'A leading # directs output to a file (PRINT#)',
          align=Align.INLINE)
d.char_literal(0x8d9e)
d.comment(0x8d9f, "'#': PRINT# to a file", align=Align.INLINE)
d.comment(0x8da1, 'Back up over the character', align=Align.INLINE)
d.comment(0x8da3, 'enter the print loop', align=Align.INLINE)
d.comment(0x8da6, 'Comma: pad with spaces to the next @% field',
          align=Align.INLINE)
# stmt_print
d.label(0x8da6, 'print_comma')
d.comment(0x8da9, 'zero: no padding', align=Align.INLINE)
d.comment(0x8dab, 'Current column (COUNT)', align=Align.INLINE)
d.comment(0x8dad, 'at column 0: no padding', align=Align.INLINE)
d.label(0x8dad, 'print_field_loop')
d.comment(0x8daf, 'reduce by the field width...', align=Align.INLINE)
d.comment(0x8db2, '...until COUNT mod width', align=Align.INLINE)
d.comment(0x8db4, 'spaces needed to the next field', align=Align.INLINE)
d.comment(0x8db5, 'print a space', align=Align.INLINE)
d.label(0x8db5, 'print_pad_loop')
d.comment(0x8db8, 'count up to zero', align=Align.INLINE)
d.comment(0x8db9, 'loop', align=Align.INLINE)
d.comment(0x8dbb, 'Prepare for decimal', align=Align.INLINE)
d.label(0x8dbb, 'print_item')
d.comment(0x8dbc, 'Take the field width from @% (&0400)', align=Align.INLINE)
d.comment(0x8dbf, 'as the print field width', align=Align.INLINE)
d.comment(0x8dc1, 'Set the hex/dec flag (~ selects hex)', align=Align.INLINE)
d.label(0x8dc1, 'print_set_hex')
d.comment(0x8dc3, 'Next non-space character', align=Align.INLINE)
d.label(0x8dc3, 'print_next')
d.comment(0x8dc6, "':' end of statement?", align=Align.INLINE)
d.char_literal(0x8dc7)
d.comment(0x8dc8, 'yes', align=Align.INLINE)
d.comment(0x8dca, 'end of line?', align=Align.INLINE)
d.comment(0x8dcc, 'yes', align=Align.INLINE)
d.comment(0x8dce, 'ELSE?', align=Align.INLINE)
d.comment(0x8dd0, 'yes', align=Align.INLINE)
d.comment(0x8dd2, "'~' hex mode?", align=Align.INLINE)
d.char_literal(0x8dd3)
d.label(0x8dd2, 'print_check_sep')
d.comment(0x8dd4, 'yes: set the flag', align=Align.INLINE)
d.comment(0x8dd6, 'Comma: advance to the next print field', align=Align.INLINE)
d.char_literal(0x8dd7)
d.comment(0x8dd8, 'yes', align=Align.INLINE)
d.comment(0x8dda, 'Semicolon: print the next item with no gap',
          align=Align.INLINE)
d.char_literal(0x8ddb)
d.comment(0x8ddc, 'yes', align=Align.INLINE)
d.comment(0x8dde, "Handle the ' TAB and SPC print items", align=Align.INLINE)
d.comment(0x8de1, 'handled: next item', align=Align.INLINE)
d.comment(0x8de3, 'Save the field width...', align=Align.INLINE)
d.comment(0x8de5, 'push it', align=Align.INLINE)
d.comment(0x8de6, '...and flags (the evaluator may PRINT)', align=Align.INLINE)
d.comment(0x8de8, 'push it', align=Align.INLINE)
d.comment(0x8de9, 'Back up to the item', align=Align.INLINE)
d.comment(0x8deb, 'Evaluate the expression to print', align=Align.INLINE)
d.comment(0x8dee, 'Restore the flags...', align=Align.INLINE)
d.comment(0x8def, 'store them', align=Align.INLINE)
d.comment(0x8df1, '...and the field width', align=Align.INLINE)
d.comment(0x8df2, 'store it', align=Align.INLINE)
d.comment(0x8df4, 'Update the program pointer', align=Align.INLINE)
d.comment(0x8df6, 'from PtrB offset (&1B)', align=Align.INLINE)
d.comment(0x8df8, 'String item?', align=Align.INLINE)
d.comment(0x8df9, 'A string value: print it directly', align=Align.INLINE)
d.comment(0x8dfb, 'A number: convert to an ASCII string', align=Align.INLINE)
d.comment(0x8dfe, 'and right-justify it within the field width',
          align=Align.INLINE)

d.comment(0x8e00, 'minus the string length', align=Align.INLINE)
d.comment(0x8e01, 'width - string length = pad count', align=Align.INLINE)
d.comment(0x8e03, 'longer than the field: print as is', align=Align.INLINE)
d.comment(0x8e05, 'equal: print as is', align=Align.INLINE)
d.comment(0x8e07, 'spaces to pad with', align=Align.INLINE)
d.comment(0x8e08, 'print a leading space', align=Align.INLINE)
d.label(0x8e08, 'print_num_pad')
d.comment(0x8e0b, 'one fewer pad space', align=Align.INLINE)
d.comment(0x8e0c, 'loop', align=Align.INLINE)
d.comment(0x8e0e, 'String length', align=Align.INLINE)
d.label(0x8e0e, 'print_string')
d.comment(0x8e10, 'empty: next item', align=Align.INLINE)
d.comment(0x8e12, 'From the start', align=Align.INLINE)
d.comment(0x8e14, 'String character', align=Align.INLINE)
d.label(0x8e14, 'print_string_loop')
d.comment(0x8e17, 'print it', align=Align.INLINE)
d.comment(0x8e1a, 'next', align=Align.INLINE)
d.comment(0x8e1b, 'printed all characters?', align=Align.INLINE)
d.comment(0x8e1d, 'loop', align=Align.INLINE)
d.comment(0x8e1f, 'next item', align=Align.INLINE)
# TAB()/SPC handler (&8E24), called from print_special_item.
d.comment(0x8e21, 'Missing , error', align=Align.INLINE)
d.label(0x8e21, 'print_tab_error')
d.comment(0x8e24, "',' TAB(x,y) form?", align=Align.INLINE)
d.char_literal(0x8e25)
d.label(0x8e24, 'print_tab_xy')
d.comment(0x8e26, 'no: TAB(x) or SPC', align=Align.INLINE)
d.comment(0x8e28, 'Save the x coordinate', align=Align.INLINE)
d.comment(0x8e2a, 'push it', align=Align.INLINE)
d.comment(0x8e2b, 'Evaluate y, expect )', align=Align.INLINE)
d.comment(0x8e2e, 'coerce to integer', align=Align.INLINE)
d.comment(0x8e31, 'VDU 31 (move cursor)', align=Align.INLINE)
d.comment(0x8e33, 'send the VDU 31 control code', align=Align.INLINE)
d.comment(0x8e36, 'x coordinate', align=Align.INLINE)
d.comment(0x8e37, 'send the x coordinate', align=Align.INLINE)
d.comment(0x8e3a, 'y coordinate', align=Align.INLINE)
d.comment(0x8e3d, 'next item', align=Align.INLINE)
d.comment(0x8e40, 'TAB(x): evaluate x', align=Align.INLINE)
d.label(0x8e40, 'print_tab_x')
d.comment(0x8e43, 'skip spaces', align=Align.INLINE)
d.comment(0x8e46, "')'?", align=Align.INLINE)
d.char_literal(0x8e47)
d.comment(0x8e48, 'no: TAB(x,y)', align=Align.INLINE)
d.comment(0x8e4a, 'Spaces = x - COUNT', align=Align.INLINE)
d.comment(0x8e4c, 'subtract the current column', align=Align.INLINE)
d.comment(0x8e4e, 'already at column x: nothing to do', align=Align.INLINE)
d.comment(0x8e50, 'count', align=Align.INLINE)
d.comment(0x8e51, 'past column x: skip', align=Align.INLINE)
d.comment(0x8e53, 'Newline to reach a fresh line', align=Align.INLINE)
d.comment(0x8e56, 'fresh line: pad to column x', align=Align.INLINE)
d.comment(0x8e58, 'SPC(n): evaluate the count', align=Align.INLINE)
d.label(0x8e58, 'print_spc')
d.comment(0x8e5b, 'spaces = x', align=Align.INLINE)
d.label(0x8e5b, 'print_spc_count')
d.comment(0x8e5d, 'none', align=Align.INLINE)
d.comment(0x8e5f, 'Print a space', align=Align.INLINE)
d.label(0x8e5f, 'print_spc_loop')
d.comment(0x8e62, 'one fewer space', align=Align.INLINE)
d.comment(0x8e63, 'loop', align=Align.INLINE)
d.comment(0x8e65, 'next item', align=Align.INLINE)
d.comment(0x8e67, 'SPC: print a newline', align=Align.INLINE)
d.label(0x8e67, 'print_spc_newline')
d.comment(0x8e6a, 'Sync the program pointer', align=Align.INLINE)
d.label(0x8e6a, 'print_sync')
d.comment(0x8e6b, 'load PtrB offset (&1B),', align=Align.INLINE)
d.comment(0x8e6d, 'store to PtrA offset (&0A)', align=Align.INLINE)
d.comment(0x8e6f, 'Return', align=Align.INLINE)

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
    on_entry={'zp_text_ptr (&0B/&0C)': 'the program text pointer (PtrA)',
              'zp_text_ptr_off (&0A)': 'offset at the PRINT item'},
    on_exit={'C': 'clear if a special item was consumed and printed, else set',
             'zp_text_ptr_off (&0A)': 'advanced past a consumed item'},
)
# print_special_item (&8E70): the ' TAB SPC items, and inline strings
d.comment(0x8e70, 'Save PtrA into PtrB: low', align=Align.INLINE)
d.comment(0x8e72, 'store it', align=Align.INLINE)
d.comment(0x8e74, 'high', align=Align.INLINE)
d.comment(0x8e76, 'store it', align=Align.INLINE)
d.comment(0x8e78, 'offset', align=Align.INLINE)
d.comment(0x8e7a, 'store it', align=Align.INLINE)
d.comment(0x8e7c, 'an apostrophe?', align=Align.INLINE)
d.char_literal(0x8e7d)
d.comment(0x8e7e, 'yes: force a newline', align=Align.INLINE)
d.comment(0x8e80, 'TAB token?', align=Align.INLINE)
d.comment(0x8e82, 'yes: handle TAB', align=Align.INLINE)
d.comment(0x8e84, 'SPC token?', align=Align.INLINE)
d.comment(0x8e86, 'yes: handle SPC', align=Align.INLINE)
d.comment(0x8e88, 'none: not consumed (carry set)', align=Align.INLINE)
d.comment(0x8e89, 'Return', align=Align.INLINE)
d.comment(0x8e8a, 'Skip spaces, then handle a special item', align=Align.INLINE)
# print_special_item
d.subroutine(
    0x8e8a, 'print_special_skip',
    title='Skip spaces then handle a PRINT special item',
    description="""Skip spaces at PtrA, then dispatch the next PRINT item to
print_special_item (which handles ~, TAB, SPC, ' and so on). If that
consumed the item, return with carry clear; if the next character is a
string literal (a double-quote), print it inline via
print_inline_loop; otherwise return with carry set, leaving the
character in A.
""",
    on_entry={
        'zp_text_ptr (&0B)': 'PtrA, at the item being scanned',
        'zp_text_ptr_off (&0A)': 'offset within the line',
    },
    on_exit={
        'C': 'clear if the item was consumed or printed, set if not recognised',
        'A': 'the unconsumed character when carry is set',
    },
)
d.comment(0x8e8d, 'handle it', align=Align.INLINE)
d.comment(0x8e90, 'consumed: done', align=Align.INLINE)
d.comment(0x8e92, 'a string literal (quote)?', align=Align.INLINE)
d.char_literal(0x8e93)
d.comment(0x8e94, 'yes: print it inline', align=Align.INLINE)
d.comment(0x8e96, 'not consumed', align=Align.INLINE)
d.comment(0x8e97, 'Return', align=Align.INLINE)
d.comment(0x8e98, 'Missing " error block', align=Align.INLINE)
d.label(0x8e98, 'missing_quote')
d.comment(0x8ea4, 'print a character', align=Align.INLINE)
d.label(0x8ea4, 'print_inline_char')
d.comment(0x8ea7, 'Print the inline string: advance', align=Align.INLINE)
d.label(0x8ea7, 'print_inline_loop')

d.comment(0x8ea8, 'char', align=Align.INLINE)
d.comment(0x8eaa, 'CR (unterminated)?', align=Align.INLINE)
d.comment(0x8eac, 'Missing " error', align=Align.INLINE)
d.comment(0x8eae, 'a quote?', align=Align.INLINE)
d.char_literal(0x8eaf)
d.comment(0x8eb0, 'no: print it', align=Align.INLINE)
d.comment(0x8eb2, 'advance', align=Align.INLINE)
d.comment(0x8eb3, 'update the offset', align=Align.INLINE)
d.comment(0x8eb5, 'doubled ""?', align=Align.INLINE)
d.comment(0x8eb7, 'is it another quote?', align=Align.INLINE)
d.char_literal(0x8eb8)
d.comment(0x8eb9, 'no: end of the string', align=Align.INLINE)
d.comment(0x8ebb, 'yes: print one quote', align=Align.INLINE)

# stmt_clg (&8EBD): CLG -> VDU 16.
d.comment(0x8ebd, 'Check the statement ends', align=Align.INLINE)
d.comment(0x8ec0, 'VDU 16 (clear graphics)', align=Align.INLINE)
d.comment(0x8ec2, 'send it', align=Align.INLINE)

# stmt_cls (&8EC4): CLS -> VDU 12.
d.comment(0x8ec4, 'Check the statement ends', align=Align.INLINE)
d.comment(0x8ec7, 'Reset the print column', align=Align.INLINE)
d.comment(0x8eca, 'VDU 12 (clear screen)', align=Align.INLINE)
d.comment(0x8ecc, 'send it', align=Align.INLINE)
# stmt_cls / stmt_call / usr_call
d.label(0x8ecc, 'cls_send')
d.comment(0x8ecf, 'next statement', align=Align.INLINE)

# stmt_call (&8ED2): CALL address [,params...]
d.comment(0x8ed2, 'Evaluate the call address', align=Align.INLINE)
d.comment(0x8ed5, 'coerce to an integer', align=Align.INLINE)
d.comment(0x8ed8, 'stack the address', align=Align.INLINE)
d.comment(0x8edb, 'Build the parameter block at &0600:', align=Align.INLINE)
d.comment(0x8edd, 'zero the parameter count', align=Align.INLINE)
d.comment(0x8ee0, 'reset the block write offset', align=Align.INLINE)
d.label(0x8ee0, 'call_block_init')
d.comment(0x8ee3, 'next parameter?', align=Align.INLINE)
d.comment(0x8ee6, 'a comma?', align=Align.INLINE)
d.char_literal(0x8ee7)
d.comment(0x8ee8, 'no: end of the parameters', align=Align.INLINE)
d.comment(0x8eea, 'parse the parameter (a variable)', align=Align.INLINE)
d.comment(0x8eec, 'resolve it to an address', align=Align.INLINE)
d.comment(0x8eef, 'bad parameter: error', align=Align.INLINE)
d.comment(0x8ef1, 'append its address to the block:', align=Align.INLINE)
d.comment(0x8ef4, 'advance to the next slot', align=Align.INLINE)
d.comment(0x8ef5, 'address low', align=Align.INLINE)
d.comment(0x8ef7, 'store it', align=Align.INLINE)
d.comment(0x8efa, 'next slot', align=Align.INLINE)
d.comment(0x8efb, 'address high', align=Align.INLINE)
d.comment(0x8efd, 'store it', align=Align.INLINE)
d.comment(0x8f00, 'next slot', align=Align.INLINE)
d.comment(0x8f01, 'type', align=Align.INLINE)
d.comment(0x8f03, 'store it', align=Align.INLINE)
d.comment(0x8f06, 'one more parameter', align=Align.INLINE)
d.comment(0x8f09, 'next parameter', align=Align.INLINE)
d.comment(0x8f0c, 'Check for end of statement', align=Align.INLINE)
d.label(0x8f0c, 'call_check_end')
d.comment(0x8f0e, 'error if more follows', align=Align.INLINE)
d.comment(0x8f11, 'pop the address into IWA', align=Align.INLINE)
d.comment(0x8f14, 'set up registers and call the code', align=Align.INLINE)
d.comment(0x8f17, 'clear decimal mode on return', align=Align.INLINE)
d.comment(0x8f18, 'Back to execution', align=Align.INLINE)
d.comment(0x8f1b, 'parameter error (shared)', align=Align.INLINE)

d.label(0x8f1b, 'call_param_error')
d.subroutine(0x8f1e, 'usr_call', title='Call user machine code (USR/CALL)',
             description="""Load A, X, Y and the carry from the resident integer
variables A%, X%, Y% and C%, then JMP (IWA) to the user routine. Its RTS
returns to usr_call's caller, which captures the registers back.""",
             on_entry={'zp_iwa (&2A/&2B)': 'the address to call',
                       'resint_a/x/y/c (A%, X%, Y%, C%)': 'the register values'},
             on_exit={'A': 'as left by the called code',
                      'X': 'as left by the called code',
                      'Y': 'as left by the called code',
                      'P': 'as left by the called code'})

# usr_call (&8F1E)
d.comment(0x8f1e, 'C% supplies the carry...', align=Align.INLINE)
d.comment(0x8f21, '...shifted into the carry flag', align=Align.INLINE)
d.comment(0x8f22, 'A from A%', align=Align.INLINE)
d.comment(0x8f25, 'X from X%', align=Align.INLINE)
d.comment(0x8f28, 'Y from Y%', align=Align.INLINE)
d.comment(0x8f2b, 'Call the routine at the address in IWA', align=Align.INLINE)
d.comment(0x8f2e, 'error (shared)', align=Align.INLINE)

d.label(0x8f2e, 'call_arg_error')
# stmt_delete (&8F31): DELETE start, end.
d.comment(0x8f31, 'Read the start line number', align=Align.INLINE)
d.comment(0x8f34, 'none: Syntax error', align=Align.INLINE)
d.comment(0x8f36, 'stack it', align=Align.INLINE)
d.comment(0x8f39, 'Skip spaces', align=Align.INLINE)
d.comment(0x8f3c, "','?", align=Align.INLINE)
d.char_literal(0x8f3d)
d.comment(0x8f3e, 'no: error', align=Align.INLINE)
d.comment(0x8f40, 'Read the end line number', align=Align.INLINE)
d.comment(0x8f43, 'none: error', align=Align.INLINE)
d.comment(0x8f45, 'check the statement ends', align=Align.INLINE)
d.comment(0x8f48, 'Save the end line', align=Align.INLINE)
d.comment(0x8f4a, 'low to &39,', align=Align.INLINE)
d.comment(0x8f4c, 'high byte,', align=Align.INLINE)
d.comment(0x8f4e, 'to &3A', align=Align.INLINE)
d.comment(0x8f50, 'Recover the start line', align=Align.INLINE)
d.comment(0x8f53, 'Delete the line', align=Align.INLINE)
# stmt_delete and the line-range parser
d.label(0x8f53, 'delete_loop')
d.comment(0x8f56, 'Find the next line number', align=Align.INLINE)
d.comment(0x8f59, 'Advance the line counter', align=Align.INLINE)
d.comment(0x8f5c, 'past the end line?', align=Align.INLINE)
d.comment(0x8f5e, 'end low - line low,', align=Align.INLINE)
d.comment(0x8f60, 'end high,', align=Align.INLINE)
d.comment(0x8f62, '- line high', align=Align.INLINE)
d.comment(0x8f64, 'no: delete the next', align=Align.INLINE)
d.comment(0x8f66, 'done: immediate mode', align=Align.INLINE)

# sub_c8f69 (&8F69): parse a line-number range/increment (default 10).
d.comment(0x8f69, 'Default start = 10', align=Align.INLINE)
d.subroutine(
    0x8f69, 'parse_line_range',
    title='Parse an optional start,step line-number range',
    description="""Parse the optional [start[,step]] arguments shared by AUTO and
RENUMBER: default the start line to 10, read an explicit start if
present and push it on the BASIC stack; then default the step to 10
and, if a comma follows, read an explicit step, raising "Silly" if the
step is zero. Tail-calls check_end_of_statement to verify nothing else
follows.
""",
    on_entry={
        'zp_text_ptr (&0B/&0C)': 'PtrA, at the text following the keyword',
        'zp_text_ptr_off (&0A)': 'offset within the line',
    },
    on_exit={
        'zp_iwa (&2A)': 'the step increment (default 10), &2A-&2D',
        'control': 'the start line number is left pushed on the BASIC stack; returns via check_end_of_statement',
    },
)
d.comment(0x8f6b, 'IWA = 10', align=Align.INLINE)
d.comment(0x8f6e, 'Read the start line if given', align=Align.INLINE)
d.comment(0x8f71, 'stack it', align=Align.INLINE)
d.comment(0x8f74, 'Default increment = 10', align=Align.INLINE)
d.comment(0x8f76, 'IWA = 10', align=Align.INLINE)
d.comment(0x8f79, 'Skip spaces', align=Align.INLINE)
d.comment(0x8f7c, "','  increment given?", align=Align.INLINE)
d.char_literal(0x8f7d)
d.comment(0x8f7e, 'no: use the default', align=Align.INLINE)
d.comment(0x8f80, 'Read the increment', align=Align.INLINE)
d.comment(0x8f83, 'zero?', align=Align.INLINE)
d.comment(0x8f85, 'no', align=Align.INLINE)
d.comment(0x8f87, 'low byte zero too?', align=Align.INLINE)
d.comment(0x8f89, 'zero increment: error', align=Align.INLINE)
d.comment(0x8f8b, 'step past', align=Align.INLINE)
d.comment(0x8f8d, 'back up', align=Align.INLINE)
d.label(0x8f8d, 'range_backup')
d.comment(0x8f8f, 'check the statement ends', align=Align.INLINE)

# sub_c8f92 / sub_c8f9a: set up pointers for the program scan.
d.comment(0x8f92, 'Copy TOP to &3B/&3C', align=Align.INLINE)
d.subroutine(
    0x8f92, 'setup_scan_top',
    title='Point the RENUMBER scan pointers at TOP and PAGE',
    description="""Copy TOP (&12/&13) into the table pointer at &3B/&3C, then fall into
point_general_page to set the program-scan pointer at &37/&38 to PAGE
(low byte forced to 1, the first line-number byte). Used by RENUMBER
to initialise the old-number table (built from the heap at TOP) and
the pointer that walks the program from PAGE.
""",
    on_entry={
        'zp_top (&12/&13)': 'TOP, the top of the program / base of the heap',
        'zp_page (&18)': 'PAGE, the start of program text',
    },
    on_exit={
        'zp_fwb_sign (&3B/&3C)': 'table pointer set to TOP',
        'zp_general (&37/&38)': 'scan pointer set to PAGE, low byte 1 (first line-number byte)',
        'A': 'corrupted',
    },
)
d.comment(0x8f94, 'low to &3B,', align=Align.INLINE)
d.comment(0x8f96, 'high byte,', align=Align.INLINE)
d.comment(0x8f98, 'to &3C', align=Align.INLINE)
d.comment(0x8f9a, 'Point &37/&38 at PAGE', align=Align.INLINE)
d.label(0x8f9a, 'point_general_page')
d.comment(0x8f9c, 'page to &38,', align=Align.INLINE)
d.comment(0x8f9e, 'offset 1,', align=Align.INLINE)
d.comment(0x8fa0, 'low byte &37', align=Align.INLINE)
d.comment(0x8fa2, 'Return', align=Align.INLINE)

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
# stmt_renumber
d.label(0x8fb1, 'renum_pass1_loop')
d.comment(0x8fb3, 'high byte', align=Align.INLINE)
d.comment(0x8fb5, 'high bit set marks the end of program', align=Align.INLINE)
d.comment(0x8fb7, 'Store the old number in the table', align=Align.INLINE)
d.comment(0x8fb9, 'low byte', align=Align.INLINE)
d.comment(0x8fba, 'read the line number low', align=Align.INLINE)
d.comment(0x8fbc, '(store)', align=Align.INLINE)
d.comment(0x8fbe, 'Advance the table pointer by 2: low', align=Align.INLINE)
d.comment(0x8fbf, 'offset to A,', align=Align.INLINE)
d.comment(0x8fc0, '+ table pointer (carry adds 2)', align=Align.INLINE)
d.comment(0x8fc2, '(store)', align=Align.INLINE)
d.comment(0x8fc4, 'keep the low byte', align=Align.INLINE)
d.comment(0x8fc5, 'table pointer high...', align=Align.INLINE)
d.comment(0x8fc7, '+ carry', align=Align.INLINE)
d.comment(0x8fc9, '(store)', align=Align.INLINE)
d.comment(0x8fcb, 'Has the table reached HIMEM?', align=Align.INLINE)
d.comment(0x8fcd, 'high byte vs HIMEM', align=Align.INLINE)
d.comment(0x8fcf, 'yes: no room for the table', align=Align.INLINE)
d.comment(0x8fd1, 'Advance to the next program line', align=Align.INLINE)
d.comment(0x8fd4, 'loop over all lines', align=Align.INLINE)
d.comment(0x8fd6, 'RENUMBER ran out of space: error', align=Align.INLINE)
d.label(0x8fd6, 'renum_no_space')
d.comment(0x8fdf, 'error block', align=Align.INLINE)
d.label(0x8fdf, 'silly_error')
d.comment(0x8fe7, 'Pass 2: reset to the program start', align=Align.INLINE)
d.label(0x8fe7, 'renum_pass2')
d.comment(0x8fea, 'for each line:', align=Align.INLINE)
d.label(0x8fea, 'renum_pass2_loop')
d.comment(0x8fec, 'line number high byte', align=Align.INLINE)
d.comment(0x8fee, 'end of program: go to pass 3', align=Align.INLINE)
d.comment(0x8ff0, 'Write the new number: high byte', align=Align.INLINE)
d.comment(0x8ff2, '(into the line)', align=Align.INLINE)
d.comment(0x8ff4, 'low byte', align=Align.INLINE)
d.comment(0x8ff6, 'advance', align=Align.INLINE)
d.comment(0x8ff7, '(into the line)', align=Align.INLINE)
d.comment(0x8ff9, 'Add the step to the running number: low', align=Align.INLINE)
d.comment(0x8ffa, 'step low,', align=Align.INLINE)
d.comment(0x8ffc, '+ current number low', align=Align.INLINE)
d.comment(0x8ffe, '(store)', align=Align.INLINE)
d.comment(0x9000, 'high byte...', align=Align.INLINE)
d.comment(0x9002, '+ carry', align=Align.INLINE)
d.comment(0x9004, 'keep it a valid line number (< &8000)', align=Align.INLINE)
d.comment(0x9006, '(store)', align=Align.INLINE)
d.comment(0x9008, 'Advance to the next line', align=Align.INLINE)
d.comment(0x900b, 'loop', align=Align.INLINE)
d.comment(0x900d, 'Pass 3: scan from PAGE, high byte', align=Align.INLINE)
d.label(0x900d, 'renum_pass3')
d.comment(0x900f, '(text pointer high)', align=Align.INLINE)
d.comment(0x9011, 'low byte 0', align=Align.INLINE)
d.comment(0x9013, '(store)', align=Align.INLINE)
d.comment(0x9015, 'advance', align=Align.INLINE)
d.comment(0x9016, 'read the line number high byte', align=Align.INLINE)
d.comment(0x9018, 'end of program: done', align=Align.INLINE)
d.comment(0x901a, 'Scan the line from offset 4 (past the header)', align=Align.INLINE)
d.label(0x901a, 'renum_line_loop')
d.comment(0x901c, 'next token', align=Align.INLINE)
d.label(0x901c, 'renum_scan_loop')
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
d.comment(0x9030, '+ text pointer low', align=Align.INLINE)
d.comment(0x9032, '(store)', align=Align.INLINE)
d.comment(0x9034, 'loop', align=Align.INLINE)
d.comment(0x9036, 'carry into high byte', align=Align.INLINE)
d.comment(0x9038, 'loop', align=Align.INLINE)
d.comment(0x903a, 'Done: back to the immediate loop', align=Align.INLINE)
d.label(0x903a, 'renum_done')
d.comment(0x903d, 'Decode the &8D-encoded line number', align=Align.INLINE)
d.label(0x903d, 'renum_ref')
d.comment(0x9040, 'Point at the old->new table', align=Align.INLINE)
d.comment(0x9043, 'Search the table for this old number:', align=Align.INLINE)
d.label(0x9043, 'renum_table_search')
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
d.comment(0x905b, 'read it from the table', align=Align.INLINE)
d.comment(0x905d, '(save)', align=Align.INLINE)
d.comment(0x905f, 'position within the line', align=Align.INLINE)
d.comment(0x9061, 'back up to the &8D token', align=Align.INLINE)
d.comment(0x9062, 'Point at the reference in the line: low', align=Align.INLINE)
d.comment(0x9064, 'reference pointer low', align=Align.INLINE)
d.comment(0x9066, 'high', align=Align.INLINE)
d.comment(0x9068, 'reference pointer high', align=Align.INLINE)
d.comment(0x906a, 'Re-encode the new line number in place', align=Align.INLINE)
d.comment(0x906d, 'resume scanning', align=Align.INLINE)
d.label(0x906d, 'renum_resume')
d.comment(0x906f, 'continue the line scan', align=Align.INLINE)
d.comment(0x9071, 'Next table entry: advance...', align=Align.INLINE)
d.label(0x9071, 'renum_table_next')
d.comment(0x9074, '...the table pointer by 2', align=Align.INLINE)
d.comment(0x9076, 'low + 2', align=Align.INLINE)
d.comment(0x9078, '(store)', align=Align.INLINE)
d.comment(0x907a, 'loop', align=Align.INLINE)
d.comment(0x907c, 'carry', align=Align.INLINE)
d.comment(0x907e, 'loop', align=Align.INLINE)
d.comment(0x9080, 'Reference to a missing line: report it', align=Align.INLINE)
d.label(0x9080, 'renum_missing_line')
d.comment(0x9083, 'build the "Failed at <line>" message...', align=Align.INLINE)
d.comment(0x908c, 'print it', align=Align.INLINE)
d.comment(0x908d, "This line's number", align=Align.INLINE)
d.comment(0x908e, 'high byte,', align=Align.INLINE)
d.comment(0x9090, 'store high,', align=Align.INLINE)
d.comment(0x9092, 'low byte,', align=Align.INLINE)
d.comment(0x9093, 'read it,', align=Align.INLINE)
d.comment(0x9095, 'store low', align=Align.INLINE)
d.comment(0x9097, 'print it', align=Align.INLINE)
d.comment(0x909a, 'newline', align=Align.INLINE)
d.comment(0x909d, 'loop', align=Align.INLINE)
d.subroutine(0x909f, 'advance_to_next_line',
             title='Advance the general pointer to the next program line',
             description='Add the line length byte (at offset 3 of the current '
                         'line) to zp_general so it addresses the next program '
                         'line. Clears carry for the caller.',
             on_entry={'zp_general (&37/&38)': 'a pointer to the current line',
                       'Y': '2 (offset just before the length byte)',
                       'C': 'clear (it is the carry-in to the add)'},
             on_exit={'zp_general': 'addresses the next line',
                      'C': 'clear', 'X': 'preserved'})

# advance_to_next_line (&909F)
d.comment(0x909f, 'Line length is at offset 3', align=Align.INLINE)
d.comment(0x90a0, 'get the line length', align=Align.INLINE)
d.comment(0x90a2, 'add it to the pointer: low', align=Align.INLINE)
d.comment(0x90a4, '(store)', align=Align.INLINE)
d.comment(0x90a6, 'no carry: done', align=Align.INLINE)
d.comment(0x90a8, 'carry into the high byte', align=Align.INLINE)
d.comment(0x90aa, 'clear carry for the caller', align=Align.INLINE)
d.comment(0x90ab, 'Return at the next line', align=Align.INLINE)

# stmt_auto (&90AC): AUTO start, increment.
d.comment(0x90ac, 'Parse the start and increment', align=Align.INLINE)
d.comment(0x90af, 'Save the increment', align=Align.INLINE)
d.comment(0x90b1, 'push it', align=Align.INLINE)
d.comment(0x90b2, 'Recover the start line', align=Align.INLINE)
d.comment(0x90b5, 'Stack the line number', align=Align.INLINE)
# stmt_auto
d.label(0x90b5, 'auto_loop')
d.comment(0x90b8, 'Print it', align=Align.INLINE)
d.comment(0x90bb, 'Print a space and read a line', align=Align.INLINE)
d.char_literal(0x90bc)
d.comment(0x90bd, 'do it', align=Align.INLINE)
d.comment(0x90c0, 'Pop the line number', align=Align.INLINE)
d.comment(0x90c3, 'Tokenise the line', align=Align.INLINE)
d.comment(0x90c6, 'Insert it into the program', align=Align.INLINE)
d.comment(0x90c9, 'Clear variables and heap', align=Align.INLINE)
d.comment(0x90cc, 'Increment', align=Align.INLINE)
d.comment(0x90cd, 'keep it stacked', align=Align.INLINE)
d.comment(0x90ce, 'Next line number = line + increment', align=Align.INLINE)
d.comment(0x90cf, '+ current line low,', align=Align.INLINE)
d.comment(0x90d1, 'store low,', align=Align.INLINE)
d.comment(0x90d3, 'no carry: loop,', align=Align.INLINE)
d.comment(0x90d5, 'carry into the high byte', align=Align.INLINE)
d.comment(0x90d7, 'still in range: loop', align=Align.INLINE)
d.comment(0x90d9, 'overflow: stop', align=Align.INLINE)

# DIM var n (&90DF): allocate an n+1 byte block at the variable top.
d.comment(0x90dc, 'No room error', align=Align.INLINE)
# stmt_dim
d.label(0x90dc, 'dim_no_room_jmp')
d.comment(0x90df, 'Back up to the variable', align=Align.INLINE)
d.label(0x90df, 'dim_byte_block')
d.comment(0x90e1, 'Parse it', align=Align.INLINE)
d.comment(0x90e4, 'not a variable: Bad DIM', align=Align.INLINE)
d.comment(0x90e6, 'indirection: Bad DIM', align=Align.INLINE)
d.comment(0x90e8, 'Stack the variable address', align=Align.INLINE)
d.comment(0x90eb, 'Evaluate the size', align=Align.INLINE)
d.comment(0x90ee, 'n + 1 bytes', align=Align.INLINE)
d.comment(0x90f1, 'fits in 16 bits?', align=Align.INLINE)
d.comment(0x90f3, 'OR byte 2 (any => > 65535)', align=Align.INLINE)
d.comment(0x90f5, 'no: Bad DIM', align=Align.INLINE)
d.comment(0x90f7, 'New top = top + size', align=Align.INLINE)
d.comment(0x90f8, 'size low,', align=Align.INLINE)
d.comment(0x90fa, '+ VARTOP low,', align=Align.INLINE)
d.comment(0x90fc, 'new top low in Y,', align=Align.INLINE)
d.comment(0x90fd, 'size high,', align=Align.INLINE)
d.comment(0x90ff, '+ VARTOP high,', align=Align.INLINE)
d.comment(0x9101, 'new top high in X', align=Align.INLINE)
d.comment(0x9102, 'collides with the stack?', align=Align.INLINE)
d.comment(0x9104, 'high byte vs the stack', align=Align.INLINE)
d.comment(0x9106, 'yes: No room', align=Align.INLINE)
d.comment(0x9108, 'Block address = old top', align=Align.INLINE)
d.comment(0x910a, 'address low,', align=Align.INLINE)
d.comment(0x910c, 'high byte,', align=Align.INLINE)
d.comment(0x910e, 'address high', align=Align.INLINE)
d.comment(0x9110, 'Commit the new top', align=Align.INLINE)
d.comment(0x9112, 'high byte', align=Align.INLINE)
d.comment(0x9114, 'Result is the address', align=Align.INLINE)
d.comment(0x9116, 'clear byte 2,', align=Align.INLINE)
d.comment(0x9118, 'and byte 3', align=Align.INLINE)
d.comment(0x911a, 'integer type', align=Align.INLINE)
d.comment(0x911c, 'set the type', align=Align.INLINE)
d.comment(0x911e, 'assign the address to the variable', align=Align.INLINE)

d.comment(0x9121, 'sync the pointer', align=Align.INLINE)
d.comment(0x9124, 'continue', align=Align.INLINE)
d.comment(0x9127, 'Bad DIM error', align=Align.INLINE)
d.subroutine(
    0x9127, 'bad_dim',
    title='Raise the "Bad DIM" error',
    description="""Raise BASIC error &0A, "Bad DIM", via a BRK error block (the message
ends with the DIM token &DE). Reached by the DIM/array machinery on an
empty name, a re-DIM of an existing array, a bound exceeding 16383, or
another invalid dimension. Does not return.
""",
    on_exit={
        'control': 'raises BRK error &0A "Bad DIM"; does not return to the caller',
    },
)
# stmt_dim (&912F): the DIM statement - allocate an array.
# Parses the array name and element size (5 real, 4 integer/string),
# reads the comma-separated dimension bounds into the descriptor at the
# variable top, computes the total size as the product of (bound+1) times
# the element size, claims that space below the stack and zeroes it.
# ----------------------------------------------------------------------
d.comment(0x912f, 'Skip spaces', align=Align.INLINE)
d.comment(0x9132, 'Point &37/&38 at the name', align=Align.INLINE)
d.comment(0x9133, 'Clear carry for the add', align=Align.INLINE)
d.comment(0x9134, 'Name offset + text pointer low', align=Align.INLINE)
d.comment(0x9136, 'Text pointer high in X', align=Align.INLINE)
d.comment(0x9138, 'No carry into the high byte', align=Align.INLINE)
d.comment(0x913a, 'Carry into the high byte', align=Align.INLINE)
d.comment(0x913b, 'Clear carry to back up by one', align=Align.INLINE)
d.comment(0x913c, 'Back up one byte (validate reads from offset 1): low', align=Align.INLINE)
d.label(0x913c, 'dim_name')
d.comment(0x913e, '&37 = name pointer low', align=Align.INLINE)
d.comment(0x9140, 'High byte', align=Align.INLINE)
d.comment(0x9141, 'Back up one byte: high', align=Align.INLINE)
d.comment(0x9143, '&38 = name pointer high', align=Align.INLINE)
d.comment(0x9145, 'Default element size = 5 (real)', align=Align.INLINE)
d.comment(0x9147, 'Stash it as the element size (zp_fwb_m2)', align=Align.INLINE)
d.comment(0x9149, 'Name offset', align=Align.INLINE)
d.comment(0x914b, 'Validate the name', align=Align.INLINE)
d.comment(0x914e, 'empty name?', align=Align.INLINE)
d.comment(0x9150, 'yes: Bad DIM', align=Align.INLINE)
d.comment(0x9152, "'(' array?", align=Align.INLINE)
d.char_literal(0x9153)
d.comment(0x9154, 'yes', align=Align.INLINE)
d.comment(0x9156, "'$' string?", align=Align.INLINE)
d.char_literal(0x9157)
d.comment(0x9158, 'yes', align=Align.INLINE)
d.comment(0x915a, "'%' integer?", align=Align.INLINE)
d.char_literal(0x915b)
d.comment(0x915c, 'no: DIM var n (byte block)', align=Align.INLINE)
d.comment(0x915e, 'Element size = 4 (integer/string)', align=Align.INLINE)
d.label(0x915e, 'dim_check_paren')
d.comment(0x9160, 'step past the suffix', align=Align.INLINE)
d.comment(0x9161, 'Count the suffix char in the name length too', align=Align.INLINE)
d.comment(0x9162, 'following character', align=Align.INLINE)
d.comment(0x9164, "'(' array?", align=Align.INLINE)
d.char_literal(0x9165)
d.comment(0x9166, 'yes', align=Align.INLINE)
d.comment(0x9168, 'DIM var n: allocate a byte block', align=Align.INLINE)
d.label(0x9168, 'dim_byte')
d.comment(0x916b, 'Array: save the name length', align=Align.INLINE)
d.label(0x916b, 'dim_array')
d.comment(0x916d, 'Save the name offset too (&0a)', align=Align.INLINE)
d.comment(0x916f, 'Already defined?', align=Align.INLINE)
d.comment(0x9172, 'yes: Bad DIM (re-DIM)', align=Align.INLINE)
d.comment(0x9174, 'Create the array variable', align=Align.INLINE)
d.comment(0x9177, 'Clear its pointer', align=Align.INLINE)
d.comment(0x9179, 'Zero the value byte', align=Align.INLINE)
d.comment(0x917c, 'Save the element size', align=Align.INLINE)
d.comment(0x917e, 'Push it for the post-loop multiply', align=Align.INLINE)
d.comment(0x917f, 'Descriptor write offset starts at 1', align=Align.INLINE)
d.comment(0x9181, 'Push the descriptor write offset', align=Align.INLINE)
d.comment(0x9182, 'running size = 1', align=Align.INLINE)
d.comment(0x9185, 'Stack the running size', align=Align.INLINE)
d.label(0x9185, 'dim_bound_loop')
d.comment(0x9188, 'Evaluate the next bound', align=Align.INLINE)
d.comment(0x918b, 'fits in 14 bits?', align=Align.INLINE)
d.comment(0x918d, 'Isolate the top 2 bits of the bound high byte', align=Align.INLINE)
d.comment(0x918f, 'OR in byte 2,', align=Align.INLINE)
d.comment(0x9191, 'and byte 3 (any set => bound > 16383)', align=Align.INLINE)
d.comment(0x9193, 'no: Bad DIM', align=Align.INLINE)
d.comment(0x9195, 'Extent = bound + 1', align=Align.INLINE)
d.comment(0x9198, 'Restore the descriptor offset', align=Align.INLINE)
d.comment(0x9199, 'into Y as the descriptor write index', align=Align.INLINE)
d.comment(0x919a, 'Store the extent in the descriptor', align=Align.INLINE)
d.comment(0x919c, 'extent low byte,', align=Align.INLINE)
d.comment(0x919e, 'advance to the high byte,', align=Align.INLINE)
d.comment(0x919f, 'extent high byte,', align=Align.INLINE)
d.comment(0x91a1, 'store it,', align=Align.INLINE)
d.comment(0x91a3, 'advance past the extent', align=Align.INLINE)
d.comment(0x91a4, 'save the offset', align=Align.INLINE)
d.comment(0x91a5, 'Push the updated descriptor offset', align=Align.INLINE)
d.comment(0x91a6, 'Multiply the running size by the extent', align=Align.INLINE)
d.comment(0x91a9, 'Skip spaces', align=Align.INLINE)
d.comment(0x91ac, "','  another dimension?", align=Align.INLINE)
d.char_literal(0x91ad)
d.comment(0x91ae, 'yes', align=Align.INLINE)
d.comment(0x91b0, "')' end of dimensions?", align=Align.INLINE)
d.char_literal(0x91b1)
d.comment(0x91b2, 'yes', align=Align.INLINE)
d.comment(0x91b4, 'otherwise Bad DIM', align=Align.INLINE)
d.comment(0x91b7, 'Recover the data offset (1 + 2*dims)', align=Align.INLINE)
d.label(0x91b7, 'dim_alloc')
d.comment(0x91b8, 'save it', align=Align.INLINE)
d.comment(0x91ba, 'Recover the element size', align=Align.INLINE)
d.comment(0x91bb, 'as the multiplier low byte', align=Align.INLINE)
d.comment(0x91bd, 'element size high = 0', align=Align.INLINE)
d.comment(0x91bf, '(16-bit element size in zp_fwb_m2/m3)', align=Align.INLINE)
d.comment(0x91c1, 'Total = element count * element size', align=Align.INLINE)
d.comment(0x91c4, 'Store the data offset in descriptor byte 0',
          align=Align.INLINE)
d.comment(0x91c6, 'the saved offset (1 + 2*dims)', align=Align.INLINE)
d.comment(0x91c8, 'into descriptor byte 0', align=Align.INLINE)
d.comment(0x91ca, 'Add it to the total size', align=Align.INLINE)
d.comment(0x91cc, 'total size low = header + data,', align=Align.INLINE)
d.comment(0x91ce, 'no carry into the high byte', align=Align.INLINE)
d.comment(0x91d0, 'carry into the total size high byte', align=Align.INLINE)
d.comment(0x91d2, 'Point at the current variable top', align=Align.INLINE)
d.label(0x91d2, 'dim_clear')
d.comment(0x91d4, 'high byte to &38,', align=Align.INLINE)
d.comment(0x91d6, 'low byte', align=Align.INLINE)
d.comment(0x91d8, 'to &37 (saved old top)', align=Align.INLINE)
d.comment(0x91da, 'New top = top + total size', align=Align.INLINE)
d.comment(0x91db, '+ total size low,', align=Align.INLINE)
d.comment(0x91dd, 'new top low held in Y,', align=Align.INLINE)
d.comment(0x91de, 'high byte', align=Align.INLINE)
d.comment(0x91e0, '+ total size high', align=Align.INLINE)
d.comment(0x91e2, 'overflow: No room', align=Align.INLINE)
d.comment(0x91e4, 'new top high in X', align=Align.INLINE)
d.comment(0x91e5, 'collides with the stack?', align=Align.INLINE)
d.comment(0x91e7, 'high byte vs stack high (16-bit compare)', align=Align.INLINE)
d.comment(0x91e9, 'yes: No room', align=Align.INLINE)
d.comment(0x91eb, 'Commit the new variable top', align=Align.INLINE)
d.comment(0x91ed, 'high byte', align=Align.INLINE)
d.comment(0x91ef, 'Zero the array storage from the old top', align=Align.INLINE)
d.comment(0x91f1, 'skip the descriptor header to the data,', align=Align.INLINE)
d.comment(0x91f3, 'data start offset in Y,', align=Align.INLINE)
d.comment(0x91f4, 'zero byte to fill with,', align=Align.INLINE)
d.comment(0x91f6, 'pointer low = 0 (Y carries the offset)', align=Align.INLINE)
d.comment(0x91f8, 'no page crossing', align=Align.INLINE)
d.comment(0x91fa, 'step the pointer to the next page', align=Align.INLINE)
d.comment(0x91fc, 'store a zero byte', align=Align.INLINE)
d.label(0x91fc, 'dim_clear_loop')
d.comment(0x91fe, 'next byte,', align=Align.INLINE)
d.comment(0x91ff, 'no page wrap', align=Align.INLINE)
d.comment(0x9201, 'cross into the next page', align=Align.INLINE)
d.comment(0x9203, 'reached the new top?', align=Align.INLINE)
d.label(0x9203, 'dim_clear_check')
d.comment(0x9205, 'low byte not at top yet: keep zeroing', align=Align.INLINE)
d.comment(0x9207, 'compare the page to the new top page', align=Align.INLINE)
d.comment(0x9209, 'not there yet: keep zeroing', align=Align.INLINE)
d.comment(0x920b, 'Skip spaces', align=Align.INLINE)
d.label(0x920b, 'dim_after')
d.comment(0x920e, "','  another array?", align=Align.INLINE)
d.char_literal(0x920f)
d.comment(0x9210, 'yes', align=Align.INLINE)
d.comment(0x9212, 'no: next statement', align=Align.INLINE)
d.comment(0x9215, 'DIM the next array', align=Align.INLINE)
d.label(0x9215, 'dim_next_array')
d.comment(0x9218, 'No room error', align=Align.INLINE)

d.label(0x9218, 'dim_no_room')

d.subroutine(
    0x9222, 'iwa_inc',
    title='Increment the integer accumulator',
    description='IWA = IWA + 1, carrying through all four bytes.',
    on_entry={'zp_iwa (&2A-&2D)': 'the integer to increment'},
    on_exit={'zp_iwa': 'incremented by one',
             'X': 'preserved', 'Y': 'preserved'},
)
# iwa_inc (&9222): 32-bit IWA = IWA + 1
d.comment(0x9222, 'Increment IWA: byte 0', align=Align.INLINE)
d.comment(0x9224, 'No carry: done', align=Align.INLINE)
d.comment(0x9226, 'Carry into byte 1', align=Align.INLINE)
d.comment(0x9228, 'no carry: done', align=Align.INLINE)
d.comment(0x922a, 'byte 2', align=Align.INLINE)
d.comment(0x922c, 'no carry: done', align=Align.INLINE)
d.comment(0x922e, 'byte 3', align=Align.INLINE)
d.comment(0x9230, 'Return', align=Align.INLINE)

# imul16 (&9231/&9236): IWA = IWA * FWB (shift-and-add)
d.comment(0x9231, 'Unstack the multiplier (into &3F area)', align=Align.INLINE)
d.label(0x9231, 'unstack_multiplier')
d.comment(0x9233, 'into the &3F area', align=Align.INLINE)
d.subroutine(0x9236, 'imul16', title='16-bit integer multiply (IWA * FWB)',
             description='Multiply IWA by the 16-bit multiplier in the FWB '
                         'mantissa (m2/m3) by shift-and-add, leaving the 16-bit '
                         'product in IWA low/high. Raises Too big on overflow. '
                         'Used for array subscript arithmetic.',
             on_entry={'zp_iwa (&2A/&2B)': 'the multiplicand',
                       'zp_fwb_m2 (&3F/&40)': 'the 16-bit multiplier'},
             on_exit={'zp_iwa (&2A/&2B)': 'the 16-bit product',
                      'X': 'corrupted', 'Y': 'corrupted',
                      'BRK': 'Too big on overflow'})

d.comment(0x9236, 'Clear the running product (X:Y)', align=Align.INLINE)
d.comment(0x9238, 'high in X, low in Y', align=Align.INLINE)
d.comment(0x923a, 'Shift the multiplier right: next bit into carry', align=Align.INLINE)
# imul16 / stmt_page / stmt_trace
d.label(0x923a, 'imul_loop')
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
d.label(0x924b, 'imul_double')
d.comment(0x924d, 'high', align=Align.INLINE)
d.comment(0x924f, 'more multiplier bits?', align=Align.INLINE)
d.comment(0x9251, 'any multiplier bits left?', align=Align.INLINE)
d.comment(0x9253, 'loop', align=Align.INLINE)
d.comment(0x9255, 'Store the product: low', align=Align.INLINE)
d.comment(0x9257, 'high', align=Align.INLINE)
d.comment(0x9259, 'Return', align=Align.INLINE)
d.comment(0x925a, 'overflow error', align=Align.INLINE)

d.label(0x925a, 'imul_overflow')
# stmt_himem (&925D): HIMEM = value
d.comment(0x925d, 'Step past "=", evaluate an integer', align=Align.INLINE)
d.comment(0x9260, 'Set HIMEM and the stack: low', align=Align.INLINE)
d.comment(0x9262, 'HIMEM low', align=Align.INLINE)
d.comment(0x9264, 'stack pointer low', align=Align.INLINE)
d.comment(0x9266, 'high', align=Align.INLINE)
d.comment(0x9268, 'HIMEM high', align=Align.INLINE)
d.comment(0x926a, 'stack pointer high', align=Align.INLINE)
d.comment(0x926c, 'Back to execution', align=Align.INLINE)
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

# stmt_page (&9283): PAGE = value
d.comment(0x9283, 'Step past "=", evaluate an integer', align=Align.INLINE)
d.comment(0x9286, 'PAGE is a page number (the high byte)', align=Align.INLINE)
d.comment(0x9288, '(store)', align=Align.INLINE)
d.comment(0x928a, 'Back to execution', align=Align.INLINE)
d.label(0x928a, 'page_done')
# stmt_clear (&928D): CLEAR.
d.comment(0x928d, 'Check the statement ends', align=Align.INLINE)
d.comment(0x9290, 'Clear variables, heap and stack', align=Align.INLINE)
d.comment(0x9293, 'next statement', align=Align.INLINE)

# stmt_trace (&9295): TRACE line / TRACE ON / TRACE OFF.
d.comment(0x9295, 'Line number following?', align=Align.INLINE)
d.comment(0x9298, 'yes: TRACE to that line', align=Align.INLINE)
d.comment(0x929a, 'ON token?', align=Align.INLINE)
d.comment(0x929c, 'yes', align=Align.INLINE)
d.comment(0x929e, 'OFF token?', align=Align.INLINE)
d.comment(0x92a0, 'yes', align=Align.INLINE)
d.comment(0x92a2, 'Evaluate the trace ceiling', align=Align.INLINE)
d.comment(0x92a5, 'check the statement ends', align=Align.INLINE)
d.label(0x92a5, 'trace_check_end')
d.comment(0x92a8, 'Set the trace ceiling', align=Align.INLINE)
d.comment(0x92aa, 'low byte,', align=Align.INLINE)
d.comment(0x92ac, 'high byte,', align=Align.INLINE)
d.comment(0x92ae, 'to &22', align=Align.INLINE)
d.label(0x92ae, 'trace_ceiling_loop')
d.comment(0x92b0, 'TRACE on', align=Align.INLINE)
d.comment(0x92b2, 'Set the TRACE flag', align=Align.INLINE)
d.label(0x92b2, 'trace_set_flag')
d.comment(0x92b4, 'next statement', align=Align.INLINE)
d.comment(0x92b7, 'TRACE ON: step past', align=Align.INLINE)
d.label(0x92b7, 'trace_on')
d.comment(0x92b9, 'check the statement ends', align=Align.INLINE)
d.comment(0x92bc, 'ceiling = max', align=Align.INLINE)
d.comment(0x92be, 'set it on', align=Align.INLINE)
d.comment(0x92c0, 'TRACE OFF: step past', align=Align.INLINE)
d.label(0x92c0, 'trace_off')
d.comment(0x92c2, 'check the statement ends', align=Align.INLINE)
d.comment(0x92c5, 'flag = 0', align=Align.INLINE)
d.comment(0x92c7, 'set it off', align=Align.INLINE)

# stmt_time (&92C9): TIME = n -> OSWORD 2.
d.comment(0x92c9, 'Step past "=", evaluate the value', align=Align.INLINE)
d.comment(0x92cc, 'Point at IWA', align=Align.INLINE)
d.comment(0x92ce, 'high byte of the address', align=Align.INLINE)
d.comment(0x92d0, 'clear the 5th byte', align=Align.INLINE)
d.comment(0x92d2, 'OSWORD 2 (write clock)', align=Align.INLINE)
d.comment(0x92d7, 'next statement', align=Align.INLINE)
d.comment(0x92da, 'Step past the comma', align=Align.INLINE)
# The integer-argument evaluators: a stack of entry points sharing the
# coerce_to_integer tail. Each evaluates at PtrB and returns the integer
# in IWA, raising Type mismatch on a string. (eval_expr_to_integer at
# &8821 is the PtrA sibling that also syncs the primary pointer.)
d.subroutine(
    0x92da, 'eval_comma_integer',
    title='Evaluate a comma-separated integer argument',
    description="""Skip a comma at PtrB (Missing , if absent), then fall into
eval_expr_integer to evaluate the following expression as an integer.
""",
    on_entry={'zp_text_ptr2 (&19/&1A)': 'PtrB at the comma'},
    on_exit={'zp_iwa (&2A-&2D)': 'the integer result',
             'BRK': 'Missing , or Type mismatch'},
)
d.comment(0x92dd, 'Evaluate the expression', align=Align.INLINE)
d.subroutine(
    0x92dd, 'eval_expr_integer',
    title='Evaluate an expression as an integer',
    description="""Evaluate the expression at PtrB (eval_or_eor) and coerce the
result to an integer (coerce_to_integer). Unlike eval_expr_to_integer
it does not sync the primary pointer, so the caller keeps managing PtrB.
""",
    on_entry={'zp_text_ptr2 (&19/&1A)': 'PtrB at the expression'},
    on_exit={'zp_iwa (&2A-&2D)': 'the integer result',
             'BRK': 'Type mismatch on a string'},
)
d.comment(0x92e0, '...and coerce to integer', align=Align.INLINE)

d.comment(0x92e3, 'Evaluate a factor', align=Align.INLINE)
d.subroutine(
    0x92e3, 'eval_factor_integer',
    title='Evaluate a single factor as an integer',
    description="""Evaluate one factor at PtrB (eval_factor, so without applying
any operators) and coerce it to an integer: a string raises Type
mismatch, a real is converted, an integer is returned unchanged.
""",
    on_entry={'zp_text_ptr2 (&19/&1A)': 'PtrB at the factor'},
    on_exit={'zp_iwa (&2A-&2D)': 'the integer result',
             'BRK': 'Type mismatch on a string'},
)
d.comment(0x92e6, 'string: Type mismatch', align=Align.INLINE)
d.comment(0x92e8, 'real: convert to integer', align=Align.INLINE)
d.comment(0x92ea, 'Return', align=Align.INLINE)
d.comment(0x92eb, 'Expect "=" and evaluate', align=Align.INLINE)
d.subroutine(
    0x92eb, 'eval_eq_integer',
    title='Require "=" then evaluate an integer',
    description="""Copy PtrA to PtrB and require an "=" (sub_c9807), evaluate the
value that follows, then fall into coerce_var_to_integer. Used by the
pseudo-variable assignments (TIME=, PAGE=, ...).
""",
    on_entry={'zp_text_ptr (&0B/&0C)': 'PtrA before the "="'},
    on_exit={'zp_iwa (&2A-&2D)': 'the integer result',
             'BRK': 'Mistake if "=" is missing, Type mismatch on a string'},
)
d.comment(0x92ee, 'Result type, then coerce to integer', align=Align.INLINE)

d.subroutine(
    0x92ee, 'coerce_var_to_integer',
    title='Coerce the current value to an integer',
    description="""Load the value type from zp_var_type and fall into
coerce_to_integer, converting the just-evaluated value to an integer.
The entry to use when the type is in zp_var_type rather than A.
""",
    on_entry={'zp_var_type (&27)': 'the value type',
              'zp_iwa / zp_fwa': 'the value'},
    on_exit={'zp_iwa (&2A-&2D)': 'the integer result',
             'BRK': 'Type mismatch on a string'},
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
# coerce_to_integer (&92F0) / eval_real (&92FA) / ensure_real (&92FD).
d.comment(0x92f0, 'string?', align=Align.INLINE)
d.comment(0x92f2, 'integer: return', align=Align.INLINE)
d.comment(0x92f4, 'real: convert to integer', align=Align.INLINE)
d.label(0x92f4, 'coerce_real')
d.comment(0x92f7, 'Type mismatch error', align=Align.INLINE)
d.label(0x92f7, 'coerce_type_error')
d.subroutine(0x92fa, 'eval_real', title='Evaluate an expression as a real',
             description='Evaluate a factor at PtrB and ensure the result is '
                         'real, converting an integer with int_to_fwa.',
             on_entry={'zp_text_ptr2 (&19/&1A)': 'PtrB at the factor to evaluate'},
             on_exit={'zp_fwa (&2E-&35)': 'the value as a real',
                      'A': 'real type marker (negative)',
                      'BRK': 'Type mismatch on a string'})
d.comment(0x92fa, 'Evaluate a factor', align=Align.INLINE)
d.subroutine(0x92fd, 'ensure_real', title='Coerce the result to a real',
             description='Leave a real unchanged, convert an integer to FWA '
                         '(int_to_fwa), or raise Type mismatch for a string.',
             on_entry={'A': 'the value type (negative real, positive integer, 0 string)',
                       'zp_iwa / zp_fwa': 'the value'},
             on_exit={'zp_fwa (&2E-&35)': 'the value as a real',
                      'A': 'real type marker (negative)',
                      'BRK': 'Type mismatch on a string'})
d.comment(0x92fd, 'string?', align=Align.INLINE)
d.comment(0x92ff, 'real: return', align=Align.INLINE)
d.comment(0x9301, 'integer: convert to real', align=Align.INLINE)

d.comment(0x9304, "Remember the call site in PtrB", align=Align.INLINE)
# stmt_proc (&9304), stmt_local (&9323), stmt_endproc (&9356).
d.comment(0x9306, 'PtrA low to PtrB,', align=Align.INLINE)
d.comment(0x9308, 'high byte,', align=Align.INLINE)
d.comment(0x930a, 'to PtrB high,', align=Align.INLINE)
d.comment(0x930c, 'offset,', align=Align.INLINE)
d.comment(0x930e, 'to PtrB offset', align=Align.INLINE)
d.comment(0x9310, 'Enter the procedure (PROC token &F2)', align=Align.INLINE)
d.comment(0x9312, 'call it', align=Align.INLINE)
d.comment(0x9315, 'check the statement ends', align=Align.INLINE)
d.comment(0x9318, 'next statement', align=Align.INLINE)
d.comment(0x931b, 'Clear the local string length', align=Align.INLINE)
# stmt_proc / stmt_local / stmt_endproc
d.label(0x931b, 'proc_clear_loop')
d.comment(0x931d, 'zero,', align=Align.INLINE)
d.comment(0x931f, 'string length = 0 (offset 3)', align=Align.INLINE)
d.comment(0x9321, 'always', align=Align.INLINE)
d.comment(0x9323, 'LOCAL is only meaningful inside a PROC/FN', align=Align.INLINE)
d.comment(0x9324, 'inside a PROC/FN?', align=Align.INLINE)
d.comment(0x9326, 'no: Not LOCAL error', align=Align.INLINE)
d.comment(0x9328, 'Parse the local variable', align=Align.INLINE)
d.comment(0x932b, 'not a variable: error', align=Align.INLINE)
d.comment(0x932d, "Save the variable's value for restoration", align=Align.INLINE)
d.comment(0x9330, 'string variable?', align=Align.INLINE)
d.comment(0x9332, 'yes: leave it cleared', align=Align.INLINE)
d.comment(0x9334, 'stack the variable address', align=Align.INLINE)
d.comment(0x9337, 'Initialise the local to zero / empty', align=Align.INLINE)
d.comment(0x9339, 'value zero', align=Align.INLINE)
d.comment(0x933c, 'integer type', align=Align.INLINE)
d.comment(0x933e, 'assign it', align=Align.INLINE)
d.comment(0x9341, 'Bump the local count in the frame', align=Align.INLINE)
d.label(0x9341, 'local_bump')
d.comment(0x9342, 'at frame offset +6', align=Align.INLINE)
d.comment(0x9345, 'Sync the program pointer', align=Align.INLINE)
d.comment(0x9347, 'from the PtrB offset', align=Align.INLINE)
d.comment(0x9349, 'Skip spaces', align=Align.INLINE)
d.comment(0x934c, 'A comma introduces another LOCAL', align=Align.INLINE)
d.char_literal(0x934d)
d.comment(0x934e, 'yes', align=Align.INLINE)
d.comment(0x9350, 'next statement', align=Align.INLINE)
d.comment(0x9353, 'not a variable: error', align=Align.INLINE)
d.label(0x9353, 'local_not_var')
d.comment(0x9356, 'ENDPROC needs a PROC frame on the stack', align=Align.INLINE)
d.comment(0x9357, 'stack near empty (no PROC frame)?', align=Align.INLINE)
d.comment(0x9359, 'no frame: Not PROC error', align=Align.INLINE)
d.comment(0x935b, 'Framed call token', align=Align.INLINE)
d.comment(0x935e, 'The framed call must be a PROC', align=Align.INLINE)
d.comment(0x9360, 'not PROC: error', align=Align.INLINE)
d.comment(0x9362, 'Return to the caller, restoring locals', align=Align.INLINE)

d.comment(0x9365, 'No PROC error', align=Align.INLINE)
d.label(0x9365, 'no_proc_error')
d.comment(0x936b, 'Not LOCAL error', align=Align.INLINE)
d.label(0x936b, 'not_local_error')
d.comment(0x9372, 'Bad statement error', align=Align.INLINE)

d.label(0x9372, 'bad_statement')
# stmt_gcol (&937A): GCOL mode, colour -> VDU 18.
d.comment(0x937a, 'Evaluate the GCOL mode', align=Align.INLINE)
d.comment(0x937d, 'save it', align=Align.INLINE)
d.comment(0x937f, 'push the GCOL mode', align=Align.INLINE)
d.comment(0x9380, 'Step past the comma, evaluate the colour',
          align=Align.INLINE)
d.comment(0x9383, 'check the statement ends', align=Align.INLINE)
d.comment(0x9386, 'VDU 18 (GCOL)', align=Align.INLINE)
d.comment(0x9388, 'send it', align=Align.INLINE)
d.comment(0x938b, 'send the mode and colour', align=Align.INLINE)
# stmt_colour (&938E): COLOUR n -> VDU 17.
d.comment(0x938e, 'VDU 17 (COLOUR)', align=Align.INLINE)
d.comment(0x9390, 'push it for later', align=Align.INLINE)
d.comment(0x9391, 'Evaluate the colour', align=Align.INLINE)
d.comment(0x9394, 'check the statement ends', align=Align.INLINE)
d.comment(0x9397, 'send VDU 17 and the colour', align=Align.INLINE)
# stmt_mode (&939A): MODE n -> VDU 22, with memory checks.
d.comment(0x939a, 'VDU 22 (MODE)', align=Align.INLINE)
d.comment(0x939c, 'push it for later', align=Align.INLINE)
d.comment(0x939d, 'Evaluate the mode number', align=Align.INLINE)
d.comment(0x93a0, 'check the statement ends', align=Align.INLINE)
d.comment(0x93a3, 'Read the high word of the machine address', align=Align.INLINE)
d.comment(0x93a6, 'not &xxFF: skip the memory test', align=Align.INLINE)
d.comment(0x93a8, 'addr not &xxFF: skip the check', align=Align.INLINE)
d.comment(0x93aa, 'not all ones: skip the memory test', align=Align.INLINE)
d.comment(0x93ac, 'high byte &FF too: skip the check', align=Align.INLINE)
d.comment(0x93ae, 'Stack not empty (STACK != HIMEM)?', align=Align.INLINE)
d.comment(0x93b0, 'STACK low vs HIMEM low', align=Align.INLINE)
d.comment(0x93b2, 'yes: Bad MODE', align=Align.INLINE)
d.comment(0x93b4, 'STACK high,', align=Align.INLINE)
d.comment(0x93b6, 'vs HIMEM high', align=Align.INLINE)
d.comment(0x93b8, 'Bad MODE', align=Align.INLINE)
d.comment(0x93ba, 'Top of RAM for this mode', align=Align.INLINE)
d.comment(0x93bc, 'OSBYTE &85', align=Align.INLINE)
d.comment(0x93c1, 'below the variables?', align=Align.INLINE)
d.comment(0x93c3, 'new top high,', align=Align.INLINE)
d.comment(0x93c4, 'vs VARTOP high', align=Align.INLINE)
d.comment(0x93c6, 'yes: Bad MODE', align=Align.INLINE)
d.comment(0x93c8, 'below the program top?', align=Align.INLINE)
d.comment(0x93ca, 'new top high,', align=Align.INLINE)
d.comment(0x93cb, 'vs TOP high', align=Align.INLINE)
d.comment(0x93cd, 'yes: Bad MODE', align=Align.INLINE)
d.comment(0x93cf, 'Set HIMEM and STACK to the new top', align=Align.INLINE)
d.comment(0x93d1, 'STACK low,', align=Align.INLINE)
d.comment(0x93d3, 'HIMEM high,', align=Align.INLINE)
d.comment(0x93d5, 'STACK high', align=Align.INLINE)
d.comment(0x93d7, 'Reset the print column', align=Align.INLINE)
# stmt_mode / stmt_draw / stmt_plot / stmt_vdu
d.label(0x93d7, 'mode_reset_col')
d.comment(0x93da, 'Send the stacked VDU byte', align=Align.INLINE)
d.label(0x93da, 'mode_send')
d.comment(0x93db, 'send it', align=Align.INLINE)
d.comment(0x93de, 'Send the parameter', align=Align.INLINE)
d.comment(0x93e1, 'next statement', align=Align.INLINE)

# stmt_move (&93E4): MOVE = PLOT 4
d.comment(0x93e4, 'MOVE is PLOT 4 (move the cursor, no draw)', align=Align.INLINE)
d.comment(0x93e6, 'do the PLOT', align=Align.INLINE)

# stmt_draw (&93E8): DRAW = PLOT 5
d.comment(0x93e8, 'DRAW is PLOT 5 (draw a line)', align=Align.INLINE)
d.comment(0x93ea, 'Save the plot mode', align=Align.INLINE)
d.label(0x93ea, 'draw_save_mode')
d.comment(0x93eb, 'Evaluate the X coordinate', align=Align.INLINE)
d.comment(0x93ee, 'evaluate Y and plot', align=Align.INLINE)
# stmt_plot (&93F1): PLOT mode, x, y -> VDU 25.
d.comment(0x93f1, 'Evaluate the plot mode', align=Align.INLINE)
d.comment(0x93f4, 'save it', align=Align.INLINE)
d.comment(0x93f6, 'push the plot mode', align=Align.INLINE)
d.comment(0x93f7, 'Step past the comma', align=Align.INLINE)
d.comment(0x93fa, 'Evaluate the X coordinate', align=Align.INLINE)
d.comment(0x93fd, 'ensure integer', align=Align.INLINE)
d.label(0x93fd, 'plot_coord')
d.comment(0x9400, 'stack X', align=Align.INLINE)
d.comment(0x9403, 'Step past the comma, evaluate Y', align=Align.INLINE)
d.comment(0x9406, 'check the statement ends', align=Align.INLINE)
d.comment(0x9409, 'VDU 25 (PLOT)', align=Align.INLINE)
d.comment(0x940b, 'send it', align=Align.INLINE)
d.comment(0x940e, 'Send the plot action', align=Align.INLINE)
d.comment(0x940f, 'send it', align=Align.INLINE)
d.comment(0x9412, 'Pop X', align=Align.INLINE)
d.comment(0x9415, 'Send X low', align=Align.INLINE)
d.comment(0x9417, 'send it', align=Align.INLINE)
d.comment(0x941a, 'Send X high', align=Align.INLINE)
d.comment(0x941c, 'send it', align=Align.INLINE)
d.comment(0x941f, 'Send Y low', align=Align.INLINE)
d.comment(0x9422, 'Send Y high', align=Align.INLINE)
d.comment(0x9424, 'send it', align=Align.INLINE)
d.comment(0x9427, 'next statement', align=Align.INLINE)
d.comment(0x942a, 'Send the high byte', align=Align.INLINE)
d.label(0x942a, 'plot_send_hi')
d.comment(0x942c, 'send it', align=Align.INLINE)

d.comment(0x942f, 'Next character', align=Align.INLINE)
# stmt_vdu loop (&9432): output bytes via OSWRCH.
d.comment(0x9432, "':' end of statement?", align=Align.INLINE)
d.char_literal(0x9433)
d.label(0x9432, 'vdu_loop')
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
d.char_literal(0x944a)
d.comment(0x944b, 'yes', align=Align.INLINE)
d.comment(0x944d, "';'  16-bit value?", align=Align.INLINE)
d.char_literal(0x944e)
d.comment(0x944f, 'no: check the statement ends', align=Align.INLINE)
d.comment(0x9451, 'yes: send the high byte too', align=Align.INLINE)
d.comment(0x9453, 'next statement', align=Align.INLINE)

d.label(0x9453, 'vdu_done')
d.comment(0x9456, 'Send the low byte to OSWRCH', align=Align.INLINE)
d.subroutine(
    0x9456, 'vdu_send_byte',
    title='Send the integer accumulator low byte to OSWRCH',
    description="""Load the low byte of the integer work accumulator and send it to the
VDU by jumping through WRCHV (OSWRCH), which returns to the caller.
Used to output a computed byte value.
""",
    on_entry={
        'zp_iwa (&2A)': 'the byte to send (IWA low byte)',
    },
    on_exit={
        'A': 'the byte sent (written to the VDU via OSWRCH)',
    },
)

d.comment(0x9458, 'jump through WRCHV (OSWRCH)', align=Align.INLINE)
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
    on_entry={'(zp_general) (&37/&38)': 'the reference (PROC/FN token at +1)',
              'zp_fileblk (&39)': 'the length of the name being sought'},
    on_exit={'zp_iwa (&2A/&2B)': 'pointer to the definition body (when found)',
             'Z': 'clear if found, set if not present'},
)
# find_proc_fn (&945B) remaining
d.comment(0x945b, 'Look at the PROC/FN token', align=Align.INLINE)
d.comment(0x945d, 'get it', align=Align.INLINE)
d.comment(0x945f, 'Index the PROC / FN entries of the variable table',
          align=Align.INLINE)
d.comment(0x9461, 'Is it PROC (&F2)?', align=Align.INLINE)
d.comment(0x9463, 'PROC: scan the PROC list', align=Align.INLINE)
d.comment(0x9465, 'FN: point at the FN list head', align=Align.INLINE)
d.comment(0x9467, 'scan the FN list', align=Align.INLINE)

d.subroutine(
    0x9469, 'find_variable',
    title='Find a variable by name',
    description="""Search the heap for a variable whose name starts at
(zp_general)+1. The initial character selects one of the per-letter
linked lists via the variable table; the chain is walked comparing
the rest of the name. On a match, returns a pointer to the value in
zp_iwa/zp_iwa_1; otherwise reports it is not present.
""",
    on_entry={'(zp_general) (&37/&38)': 'the variable reference (name at +1)',
              'zp_fileblk (&39)': 'the length of the name being sought'},
    on_exit={'zp_iwa (&2A/&2B)': 'pointer to the value (when found)',
             'Z': 'clear if found, set if not present'},
)
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
d.comment(0x946d, 'Two bytes per entry: double the initial letter',
          align=Align.INLINE)
d.comment(0x946e, 'Y = 2 * char: index into the variable table', align=Align.INLINE)
d.comment(0x946f, 'Head of the chain from the variable table (&0400+2*ch)',
          align=Align.INLINE)
# find_variable (alternating two-pointer chain walk)
d.label(0x946f, 'findvar_chain_head')
d.comment(0x9472, 'Chain head low byte -> node pointer (&3A)', align=Align.INLINE)
d.comment(0x9474, 'Chain head high byte (&0400 + 1 + 2*char)', align=Align.INLINE)
d.comment(0x9477, 'node pointer high (&3B)', align=Align.INLINE)
d.comment(0x9479, 'End of the chain: variable not found', align=Align.INLINE)
d.label(0x9479, 'findvar_walk')
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
d.comment(0x9495, 'Compare the rest of the name against this entry',
          align=Align.INLINE)
d.label(0x9495, 'findvar_cmp_a_loop')
d.comment(0x9496, 'next stored name character', align=Align.INLINE)
d.comment(0x9498, 'entry name ended early: no match', align=Align.INLINE)
d.comment(0x949a, 'compare with the search name', align=Align.INLINE)
d.label(0x949a, 'findvar_cmp_a')
d.comment(0x949c, 'differ: follow the link', align=Align.INLINE)
d.comment(0x949e, 'reached the end of the search name?', align=Align.INLINE)
d.comment(0x94a0, 'no: keep comparing', align=Align.INLINE)
d.comment(0x94a2, 'does the entry name end here too?', align=Align.INLINE)
d.comment(0x94a3, 'read the stored name char', align=Align.INLINE)
d.comment(0x94a5, 'entry name is longer: no match', align=Align.INLINE)
d.comment(0x94a7, 'Match: return a pointer to the value', align=Align.INLINE)
d.label(0x94a7, 'findvar_match_a')
d.comment(0x94a8, 'value pointer = node + name length: low', align=Align.INLINE)
d.comment(0x94aa, '(IWA low)', align=Align.INLINE)
d.comment(0x94ac, 'node high...', align=Align.INLINE)
d.comment(0x94ae, '+ carry', align=Align.INLINE)
d.comment(0x94b0, 'IWA high = pointer to the value', align=Align.INLINE)
d.comment(0x94b2, 'Return (IWA = value pointer, or not found)', align=Align.INLINE)
d.comment(0x94b3, 'No match: follow the link to the next entry',
          align=Align.INLINE)

d.label(0x94b3, 'findvar_walk_b')
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
d.label(0x94cf, 'findvar_cmp_b_loop')
d.comment(0x94d0, 'next stored character', align=Align.INLINE)
d.comment(0x94d2, 'entry name ended: no match', align=Align.INLINE)
d.comment(0x94d4, 'compare with the search name', align=Align.INLINE)
d.label(0x94d4, 'findvar_cmp_b')
d.comment(0x94d6, 'differ: next entry', align=Align.INLINE)
d.comment(0x94d8, 'end of the search name?', align=Align.INLINE)
d.comment(0x94da, 'no: keep comparing', align=Align.INLINE)
d.comment(0x94dc, 'does the entry name end here too?', align=Align.INLINE)
d.comment(0x94dd, 'read the stored name char', align=Align.INLINE)
d.comment(0x94df, 'entry name is longer: no match', align=Align.INLINE)
d.comment(0x94e1, 'value pointer = node + name length: low', align=Align.INLINE)
d.label(0x94e1, 'findvar_match_b')
d.comment(0x94e2, 'plus the node low', align=Align.INLINE)
d.comment(0x94e4, '(IWA low)', align=Align.INLINE)
d.comment(0x94e6, 'node high...', align=Align.INLINE)
d.comment(0x94e8, '+ carry', align=Align.INLINE)
d.comment(0x94ea, 'IWA high = pointer to the value', align=Align.INLINE)
d.comment(0x94ec, 'Return the value pointer', align=Align.INLINE)
# sub_c94ed (&94ED): pick the PROC or FN chain head
d.comment(0x94ed, 'Look at the PROC/FN token', align=Align.INLINE)
d.label(0x94ed, 'create_def_entry')
d.comment(0x94ef, 'get it', align=Align.INLINE)
d.comment(0x94f1, 'to X', align=Align.INLINE)
d.comment(0x94f2, 'PROC list index (&F6)', align=Align.INLINE)
d.comment(0x94f4, 'Is it PROC?', align=Align.INLINE)
d.comment(0x94f6, 'PROC: use that chain', align=Align.INLINE)
d.comment(0x94f8, 'FN list index (&F8)', align=Align.INLINE)
d.comment(0x94fa, 'use the FN chain', align=Align.INLINE)

d.subroutine(0x94fc, 'create_variable', title='Create a new variable',
             description='Append a new variable entry at VARTOP: walk to the end '
                         'of the per-letter chain, link in the new node, and copy '
                         'the name into it. The caller initialises the value bytes '
                         '(clear_value_bytes) and advances VARTOP (sub_c9539).',
             on_entry={'(zp_general) (&37/&38)': 'the variable reference (name at +1)',
                       'zp_fileblk (&39)': 'the name length',
                       'zp_vartop (&02/&03)': 'top of the variable heap'},
             on_exit={'(zp_vartop)': 'a new linked entry with its name',
                      'Y': 'offset of the last name byte in the entry'})

# create_variable (&94FC): append a new entry to the name's chain
d.comment(0x94fc, 'First character of the name', align=Align.INLINE)
d.comment(0x94fe, 'get it', align=Align.INLINE)
d.comment(0x9500, 'double it to index the variable table', align=Align.INLINE)
d.comment(0x9501, 'chain pointer low (&3A)', align=Align.INLINE)
# create_variable
d.label(0x9501, 'createvar_chain')
d.comment(0x9503, 'table base high page (&04)', align=Align.INLINE)
d.comment(0x9505, 'chain pointer high (&3B)', align=Align.INLINE)
d.comment(0x9507, 'Walk to the end of the chain: link high', align=Align.INLINE)
d.label(0x9507, 'createvar_walk_loop')
d.comment(0x9509, 'zero: found the end, append here', align=Align.INLINE)
d.comment(0x950b, 'save it', align=Align.INLINE)
d.comment(0x950c, 'link low', align=Align.INLINE)
d.comment(0x950d, 'read it', align=Align.INLINE)
d.comment(0x950f, 'follow the link: low', align=Align.INLINE)
d.comment(0x9511, 'high', align=Align.INLINE)
d.comment(0x9513, 'advance', align=Align.INLINE)
d.comment(0x9514, 'loop', align=Align.INLINE)
d.comment(0x9516, 'Link the new entry (at VARTOP): high...', align=Align.INLINE)
d.label(0x9516, 'createvar_link')
d.comment(0x9518, '...into the previous link', align=Align.INLINE)
d.comment(0x951a, 'low...', align=Align.INLINE)
d.comment(0x951c, 'point at the low link byte', align=Align.INLINE)
d.comment(0x951d, '(store)', align=Align.INLINE)
d.comment(0x951f, 'the new entry header', align=Align.INLINE)
d.comment(0x9520, 'next entry byte', align=Align.INLINE)
d.comment(0x9521, '(store)', align=Align.INLINE)
d.comment(0x9523, 'name length reached?', align=Align.INLINE)
d.comment(0x9525, 'done', align=Align.INLINE)
d.comment(0x9527, 'Copy the name into the entry:', align=Align.INLINE)
d.label(0x9527, 'createvar_copy_loop')
d.comment(0x9528, 'name char...', align=Align.INLINE)
d.comment(0x952a, '...into the entry', align=Align.INLINE)
d.comment(0x952c, 'all of the name?', align=Align.INLINE)
d.comment(0x952e, 'loop', align=Align.INLINE)
d.comment(0x9530, 'Return', align=Align.INLINE)
d.subroutine(0x9531, 'clear_value_bytes', title='Zero a run of value bytes',
             description='Write X zero bytes after a new variable name at '
                         '(zp_vartop),Y, initialising its value to zero.',
             on_entry={'X': 'the number of value bytes to clear',
                       'zp_vartop (&02/&03)': 'base of the new variable entry',
                       'Y': 'offset of the last name byte'},
             on_exit={'(zp_vartop)': 'X value bytes zeroed',
                      'Y': 'advanced past the cleared bytes',
                      'X': '0', 'A': '0'})
d.comment(0x9531, 'Zero X value bytes after the name:', align=Align.INLINE)
d.comment(0x9533, 'advance', align=Align.INLINE)
# clear_value_bytes / VARTOP advance
d.label(0x9533, 'clearval_loop')
d.comment(0x9534, 'clear a byte', align=Align.INLINE)
d.comment(0x9536, 'count down', align=Align.INLINE)
d.comment(0x9537, 'loop', align=Align.INLINE)
d.comment(0x9539, 'Advance VARTOP past the new entry:', align=Align.INLINE)
d.label(0x9539, 'advance_vartop')
d.comment(0x953a, 'Y = bytes used', align=Align.INLINE)
d.comment(0x953b, 'low', align=Align.INLINE)
d.comment(0x953d, 'no carry into the high byte', align=Align.INLINE)
d.comment(0x953f, 'carry into high', align=Align.INLINE)
d.comment(0x9541, "Check VARTOP hasn't reached the stack:", align=Align.INLINE)
d.label(0x9541, 'vartop_check')
d.comment(0x9543, 'compare high', align=Align.INLINE)
d.comment(0x9545, 'below: room', align=Align.INLINE)
d.comment(0x9547, 'above: no room', align=Align.INLINE)
d.comment(0x9549, 'equal: compare low', align=Align.INLINE)
d.comment(0x954b, 'below: room', align=Align.INLINE)
d.comment(0x954d, 'No room: unlink the new entry...', align=Align.INLINE)
d.label(0x954d, 'vartop_no_room')
d.comment(0x954f, 'link field offset', align=Align.INLINE)
d.comment(0x9551, '(clear the link)', align=Align.INLINE)
d.comment(0x9553, 'No room error', align=Align.INLINE)
d.comment(0x9556, 'Commit the new VARTOP', align=Align.INLINE)
d.label(0x9556, 'vartop_commit')
d.comment(0x9558, 'Return', align=Align.INLINE)
d.subroutine(0x9559, 'validate_var_name', title='Validate / measure a variable name',
             description='Scan the variable name at (zp_general)+1, stopping at '
                         'the first non-name character (letters, digits and _ are '
                         'accepted; a leading digit is rejected, giving an empty '
                         'name). Advances X as the running text offset.',
             on_entry={'(zp_general) (&37/&38)': 'a pointer to the name (name at +1)',
                       'X': 'the current text offset'},
             on_exit={'Y': 'one past the name (Y-1 = length; Y=1 means invalid)',
                      'X': 'the text offset advanced past the name',
                      'A': 'the terminating non-name character'})

d.comment(0x9559, 'Validate the name from offset 1:', align=Align.INLINE)
d.comment(0x955b, 'character...', align=Align.INLINE)
# validate_var_name
d.label(0x955b, 'valname_loop')
d.comment(0x955d, 'below "0": end of name', align=Align.INLINE)
d.char_literal(0x955e)
d.comment(0x955f, 'below "0": stop', align=Align.INLINE)
d.comment(0x9561, 'in the digit/symbol range?', align=Align.INLINE)
d.char_literal(0x9562)
d.comment(0x9563, 'letter range: continue', align=Align.INLINE)
d.comment(0x9565, '":" or above (not a digit)?', align=Align.INLINE)
d.char_literal(0x9566)
d.comment(0x9567, 'not a name character: stop', align=Align.INLINE)
d.comment(0x9569, 'is this the first character?', align=Align.INLINE)
d.comment(0x956b, "names can't start with a digit", align=Align.INLINE)
d.comment(0x956d, 'count the character', align=Align.INLINE)
d.label(0x956d, 'valname_count')
d.comment(0x956e, 'next', align=Align.INLINE)
d.comment(0x956f, 'loop', align=Align.INLINE)
d.comment(0x9571, 'below "_"?', align=Align.INLINE)
d.char_literal(0x9572)
d.label(0x9571, 'valname_check_uc')
d.comment(0x9573, '"_" or lower-case: accept', align=Align.INLINE)
d.comment(0x9575, 'A-Z?', align=Align.INLINE)
d.char_literal(0x9576)
d.comment(0x9577, 'letter: accept', align=Align.INLINE)
d.comment(0x9579, 'Return', align=Align.INLINE)
d.comment(0x957a, 'a-z?', align=Align.INLINE)
d.char_literal(0x957b)
d.label(0x957a, 'valname_check_lc')
d.comment(0x957c, 'accept', align=Align.INLINE)
d.comment(0x957e, 'Return', align=Align.INLINE)
d.comment(0x957f, 'Zero the value bytes of the new variable', align=Align.INLINE)

d.label(0x957f, 'zero_new_value')
# --- LET assignment --------------------------------------------------
d.subroutine(
    0x9582, 'parse_lvalue',
    title='Parse an assignment target variable',
    description="""Parse the variable reference being assigned to (parse_var_ref)
and return a pointer to its storage plus its type, creating the variable
(create_variable + clear_value_bytes) if it does not yet exist. Shared
by LET, FOR ([`stmt_for`](address:b7c4)), LOCAL ([`stmt_local`](address:9323))
and the PROC/FN parameter binder ([`call_proc_fn`](address:b197)) — so any
assignable target, including `?`, `!` and `$` indirections and array
elements, is equally valid as a LET target, a loop control variable, a
LOCAL, or a formal parameter.
""",
    on_entry={'zp_text_ptr (&0B/&0C)': 'the program text pointer (PtrA)',
              'zp_text_ptr_off (&0A)': 'offset of the target reference'},
    on_exit={'zp_iwa (&2A/&2B)': 'a pointer to the variable storage',
             'zp_iwa_2 (&2C)': 'the variable type byte'},
)
# parse_lvalue (&9582): parse a target, creating the variable if needed.
d.comment(0x9582, 'Parse the variable reference', align=Align.INLINE)
d.comment(0x9585, 'found: return', align=Align.INLINE)
d.comment(0x9587, 'indirection/array: return', align=Align.INLINE)
d.comment(0x9589, 'undefined: create the variable', align=Align.INLINE)
d.comment(0x958c, 'Decide how many value bytes to clear', align=Align.INLINE)
d.comment(0x958e, 'integer type (4) or real (5)?', align=Align.INLINE)
d.comment(0x9590, 'integer: clear 5 bytes', align=Align.INLINE)
d.comment(0x9592, 'real: clear 6 bytes', align=Align.INLINE)
d.comment(0x9593, 'then retry the parse so it is found', align=Align.INLINE)
# Top-level indirection operators (?addr, !addr, $addr) as an lvalue.
d.comment(0x9595, "'!' indirection?", align=Align.INLINE)
d.char_literal(0x9596)
# parse_lvalue
d.label(0x9595, 'lvalue_indirect')
d.comment(0x9597, 'yes: word indirection', align=Align.INLINE)
d.comment(0x9599, "'$' indirection?", align=Align.INLINE)
d.char_literal(0x959a)
d.comment(0x959b, 'yes: string indirection', align=Align.INLINE)
d.comment(0x959d, "'?' indirection?", align=Align.INLINE)
d.comment(0x959f, 'yes: byte indirection', align=Align.INLINE)
d.comment(0x95a1, 'none: not an lvalue', align=Align.INLINE)
d.comment(0x95a3, 'set carry (not an lvalue)', align=Align.INLINE)
d.comment(0x95a4, 'Return', align=Align.INLINE)
d.comment(0x95a5, "'!': word width (4)", align=Align.INLINE)
d.label(0x95a5, 'lvalue_word')
d.comment(0x95a7, 'Save the width', align=Align.INLINE)
d.label(0x95a7, 'lvalue_save_width')
d.comment(0x95a8, 'step past the operator', align=Align.INLINE)
d.comment(0x95aa, 'evaluate the address', align=Align.INLINE)
d.comment(0x95ad, 'finish as an indirection', align=Align.INLINE)
d.comment(0x95b0, "'$': step past the operator", align=Align.INLINE)
d.label(0x95b0, 'lvalue_dollar')
d.comment(0x95b2, 'evaluate the address', align=Align.INLINE)
d.comment(0x95b5, 'address in zero page?', align=Align.INLINE)
d.comment(0x95b7, 'yes: $ range error', align=Align.INLINE)
d.comment(0x95b9, 'Type = string indirection (&80)', align=Align.INLINE)
d.comment(0x95bb, 'store the type byte', align=Align.INLINE)
d.comment(0x95bd, 'found: SEC', align=Align.INLINE)
d.comment(0x95be, 'Return', align=Align.INLINE)
d.comment(0x95bf, '$ range error', align=Align.INLINE)

d.label(0x95bf, 'lvalue_range_error')

d.subroutine(0x95c9, 'parse_var_ref',
             title='Parse a variable reference / lvalue',
             description='Scan a variable name, array element, or indirection '
                         'operator at the text pointer. Sets the value address '
                         'in &2A/&2B and a type byte in &2C: 0=? byte '
                         'indirection, 4=integer (also ! word indirection), '
                         '5=real, &80=$ indirection, &81=string lvalue. '
                         'Returns A nonzero when resolved; A=0 carry clear for '
                         'a valid name not yet defined (caller creates it), '
                         'A=0 carry set when no name is present.',
             on_entry={'zp_text_ptr (&0B/&0C)': 'the program text pointer (PtrA)',
                       'zp_text_ptr_off (&0A)': 'offset of the reference'},
             on_exit={'zp_iwa (&2A/&2B)': 'the value address (when resolved)',
                      'zp_iwa_2 (&2C)': 'the type byte (0/4/5/&80/&81)',
                      'A': 'nonzero if resolved, 0 if a name needs creating / absent',
                      'C': 'with A=0: clear = create the name, set = no name'})
# ----------------------------------------------------------------------
# parse_var_ref (&95C9): parse a variable reference or indirection.
# Scans text via &19/&1A (offset &1B), building the value pointer in
# &2A/&2B and a type byte in &2C; &37/&38 points at the name, &39 its
# length. Handles resident integers (@%, A%-Z% at &0400 + char*4),
# named variables and arrays, and the ?, ! and $ indirection operators.
# ----------------------------------------------------------------------
d.comment(0x95c9, 'Copy the text pointer into the scan pointer',
          align=Align.INLINE)
d.comment(0x95cb, 'low byte,', align=Align.INLINE)
d.comment(0x95cd, 'high byte,', align=Align.INLINE)
d.comment(0x95cf, 'store it', align=Align.INLINE)
d.comment(0x95d1, 'Start one before the text offset', align=Align.INLINE)
d.comment(0x95d3, '(the scan loop pre-increments)', align=Align.INLINE)
d.comment(0x95d4, 'Advance', align=Align.INLINE)
# parse_var_ref
d.label(0x95d4, 'pvr_advance')
d.comment(0x95d5, 'Record the scan offset', align=Align.INLINE)
d.label(0x95d5, 'pvr_record_offset')
d.comment(0x95d7, 'Next character', align=Align.INLINE)
d.comment(0x95d9, 'space?', align=Align.INLINE)
d.char_literal(0x95da)
d.comment(0x95db, 'skip spaces', align=Align.INLINE)
d.comment(0x95dd, "below '@': an indirection operator", align=Align.INLINE)
d.char_literal(0x95de)
d.subroutine(
    0x95dd, 'pvr_parse',
    title='Parse a variable reference at the scan pointer',
    description="""Alternate entry to parse_var_ref for callers that have already pointed
the scan pointer zp_text_ptr2 (&19/&1A) at the first non-space
character (in A). Classify the reference as an indirection operator, a
resident integer (A%..Z%), or a named/array variable, setting the
value address in zp_iwa (&2A/&2B) and the type byte in zp_iwa_2 (&2C).
""",
    on_entry={
        'A': 'the first non-space character of the reference',
        'zp_text_ptr2 (&19/&1A)': 'the scan pointer at the reference',
        'zp_text_ptr2_off (&1B)': 'the scan offset of the character in A',
    },
    on_exit={
        'zp_iwa (&2A/&2B)': 'the value address (when resolved)',
        'zp_iwa_2 (&2C)': 'the type byte (0/4/5/&80/&81)',
        'A': 'nonzero if resolved, 0 if a name needs creating / absent',
        'C': 'with A=0: clear = create the name, set = no name',
    },
)
d.comment(0x95df, "below '@': handle as indirection ($ ! ?)", align=Align.INLINE)
d.comment(0x95e1, "above 'Z'?", align=Align.INLINE)
d.char_literal(0x95e2)
d.comment(0x95e3, 'yes: a named (dynamic) variable', align=Align.INLINE)
d.comment(0x95e5, 'Resident integer: hash char to &0400 + char*4',
          align=Align.INLINE)
d.comment(0x95e6, '(continued)', align=Align.INLINE)
d.comment(0x95e7, 'value pointer low', align=Align.INLINE)
d.comment(0x95e9, 'page &04', align=Align.INLINE)
d.comment(0x95eb, 'value pointer high byte (&2B)', align=Align.INLINE)
d.comment(0x95ed, 'Second character', align=Align.INLINE)
d.comment(0x95ee, 'read it', align=Align.INLINE)
d.comment(0x95f0, 'advance the scan offset', align=Align.INLINE)
d.comment(0x95f1, "must be '%' for a resident integer", align=Align.INLINE)
d.char_literal(0x95f2)
d.comment(0x95f3, 'not %: treat as a named variable', align=Align.INLINE)
d.comment(0x95f5, 'Type = integer', align=Align.INLINE)
d.comment(0x95f7, 'store in the type byte (&2C)', align=Align.INLINE)
d.comment(0x95f9, 'Following character', align=Align.INLINE)
d.comment(0x95fb, "'('  -> array element", align=Align.INLINE)
d.char_literal(0x95fc)
d.comment(0x95fd, 'yes: handle as an array', align=Align.INLINE)
d.comment(0x95ff, 'Named variable: type = real/string (5)', align=Align.INLINE)
d.label(0x95ff, 'pvr_named')
d.comment(0x9601, 'store in the type byte (&2C)', align=Align.INLINE)
d.comment(0x9603, 'Point &37/&38 at the name in the text', align=Align.INLINE)
d.comment(0x9605, 'offset + scan pointer:', align=Align.INLINE)
d.comment(0x9606, 'low byte,', align=Align.INLINE)
d.comment(0x9608, 'high byte in X,', align=Align.INLINE)
d.comment(0x960a, 'no carry into the high byte', align=Align.INLINE)
d.comment(0x960c, 'carry into the high byte', align=Align.INLINE)
d.comment(0x960d, 'clear carry to back up one', align=Align.INLINE)
d.comment(0x960e, 'back up one (name reads from offset 1): low', align=Align.INLINE)
d.label(0x960e, 'pvr_name_setup')
d.comment(0x9610, '&37 = name pointer low', align=Align.INLINE)
d.comment(0x9612, 'no borrow into the high byte', align=Align.INLINE)
d.comment(0x9614, 'borrow into the high byte', align=Align.INLINE)
d.comment(0x9615, '&38 = name pointer high', align=Align.INLINE)
d.label(0x9615, 'pvr_name_ptr_hi')
d.comment(0x9617, 'Reset the length counter', align=Align.INLINE)
d.comment(0x9619, 'scan the name from offset 1', align=Align.INLINE)
d.comment(0x961b, 'Scan the name: next character', align=Align.INLINE)
d.label(0x961b, 'pvr_scan_loop')
d.comment(0x961d, "below 'A'?", align=Align.INLINE)
d.char_literal(0x961e)
d.comment(0x961f, 'no: check letters', align=Align.INLINE)
d.comment(0x9621, 'a digit?', align=Align.INLINE)
d.char_literal(0x9622)
d.comment(0x9623, 'no: name ends', align=Align.INLINE)
d.comment(0x9625, "above '9'?", align=Align.INLINE)
d.char_literal(0x9626)
d.comment(0x9627, 'no: name ends', align=Align.INLINE)
d.comment(0x9629, 'count this character', align=Align.INLINE)
d.comment(0x962a, 'advance the scan', align=Align.INLINE)
d.comment(0x962b, 'continue', align=Align.INLINE)
d.comment(0x962d, "above 'Z'?", align=Align.INLINE)
d.char_literal(0x962e)
d.label(0x962d, 'pvr_scan_check_uc')
d.comment(0x962f, 'yes: check lower case', align=Align.INLINE)
d.comment(0x9631, 'A-Z: count it', align=Align.INLINE)
d.comment(0x9632, 'advance the scan', align=Align.INLINE)
d.comment(0x9633, 'continue', align=Align.INLINE)
d.comment(0x9635, "below '_'?", align=Align.INLINE)
d.char_literal(0x9636)
d.label(0x9635, 'pvr_scan_check_lc')
d.comment(0x9637, 'yes: name ends', align=Align.INLINE)
d.comment(0x9639, "above 'z'?", align=Align.INLINE)
d.char_literal(0x963a)
d.comment(0x963b, 'yes: name ends', align=Align.INLINE)
d.comment(0x963d, '_ or a-z: count it', align=Align.INLINE)
d.comment(0x963e, 'advance the scan', align=Align.INLINE)
d.comment(0x963f, 'continue', align=Align.INLINE)
d.comment(0x9641, 'Back up to the terminator', align=Align.INLINE)
d.label(0x9641, 'pvr_name_end')
d.comment(0x9642, 'empty name: undefined', align=Align.INLINE)
d.comment(0x9644, "'$' suffix -> string variable", align=Align.INLINE)
d.char_literal(0x9645)
d.comment(0x9646, 'yes', align=Align.INLINE)
d.comment(0x9648, "'%' suffix -> integer variable", align=Align.INLINE)
d.char_literal(0x9649)
d.comment(0x964a, 'no: real variable', align=Align.INLINE)
d.comment(0x964c, 'mark the type integer', align=Align.INLINE)
d.comment(0x964e, 'step past the %', align=Align.INLINE)
d.comment(0x964f, 'count the % in the name length', align=Align.INLINE)
d.comment(0x9650, 'peek at the following character', align=Align.INLINE)
d.comment(0x9651, 'check the following character', align=Align.INLINE)
d.comment(0x9653, 'step back to the %', align=Align.INLINE)
d.comment(0x9654, 'Record the name length', align=Align.INLINE)
d.label(0x9654, 'pvr_name_len')
d.comment(0x9656, "'('  -> array element", align=Align.INLINE)
d.char_literal(0x9657)
d.comment(0x9658, 'yes', align=Align.INLINE)
d.comment(0x965a, 'Look the variable up in storage', align=Align.INLINE)
d.comment(0x965d, 'not found: undefined', align=Align.INLINE)
d.comment(0x965f, 'Update the scan offset past the name', align=Align.INLINE)
d.comment(0x9661, 'Next character after the name', align=Align.INLINE)
d.label(0x9661, 'pvr_after_name')
d.comment(0x9663, 'read it', align=Align.INLINE)
d.comment(0x9665, "'!' indirection following?", align=Align.INLINE)
d.char_literal(0x9666)
d.label(0x9665, 'pvr_check_indirect')
d.comment(0x9667, 'yes: word indirection', align=Align.INLINE)
d.comment(0x9669, "'?' indirection following?", align=Align.INLINE)
d.char_literal(0x966a)
d.comment(0x966b, 'yes: byte indirection', align=Align.INLINE)
d.comment(0x966d, 'Plain variable: found', align=Align.INLINE)
d.comment(0x966e, 'save the scan offset', align=Align.INLINE)
d.comment(0x9670, 'A = &FF (found)', align=Align.INLINE)
d.comment(0x9672, 'Return', align=Align.INLINE)
d.comment(0x9673, 'No name found: A=0, SEC', align=Align.INLINE)
d.label(0x9673, 'pvr_no_name')
d.comment(0x9675, '(set carry: caller errors)', align=Align.INLINE)
d.comment(0x9676, 'Return', align=Align.INLINE)
d.comment(0x9677, 'Valid name, undefined: A=0, CLC', align=Align.INLINE)
d.label(0x9677, 'pvr_undefined')
d.comment(0x9679, '(clear carry: caller creates it)', align=Align.INLINE)
d.comment(0x967a, 'Return', align=Align.INLINE)
d.comment(0x967b, "'?' indirection: byte type (1)", align=Align.INLINE)
d.label(0x967b, 'pvr_byte_indirect')
d.comment(0x967d, 'always taken', align=Align.INLINE)
d.comment(0x967f, "'!' indirection: word type (4)", align=Align.INLINE)
d.label(0x967f, 'pvr_word_indirect')
d.comment(0x9681, 'Save the indirection width', align=Align.INLINE)
d.label(0x9681, 'pvr_save_width')
d.comment(0x9682, 'step past the operator', align=Align.INLINE)
d.comment(0x9683, 'record the new scan offset', align=Align.INLINE)
d.comment(0x9685, 'Stack the base address', align=Align.INLINE)
d.comment(0x9688, 'evaluate it as an integer', align=Align.INLINE)
d.comment(0x968b, 'Save the base address:', align=Align.INLINE)
d.comment(0x968d, 'push high byte,', align=Align.INLINE)
d.comment(0x968e, 'low byte,', align=Align.INLINE)
d.comment(0x9690, 'push it too', align=Align.INLINE)
d.comment(0x9691, 'evaluate the index expression', align=Align.INLINE)
d.comment(0x9694, 'address = base + index', align=Align.INLINE)
d.comment(0x9695, 'pull base low,', align=Align.INLINE)
d.comment(0x9696, '+ index low,', align=Align.INLINE)
d.comment(0x9698, 'store low,', align=Align.INLINE)
d.comment(0x969a, 'pull base high,', align=Align.INLINE)
d.comment(0x969b, '+ index high,', align=Align.INLINE)
d.comment(0x969d, 'store high', align=Align.INLINE)
d.comment(0x969f, 'Restore the indirection type', align=Align.INLINE)
d.label(0x969f, 'pvr_restore_type')
d.comment(0x96a0, 'into the type byte (0=? or 4=!)', align=Align.INLINE)
d.comment(0x96a2, 'found: A=&FF, CLC', align=Align.INLINE)
d.comment(0x96a3, 'A = &FF (found)', align=Align.INLINE)
d.comment(0x96a5, 'Return', align=Align.INLINE)
d.comment(0x96a6, 'Resident-integer array: step past "("', align=Align.INLINE)
d.label(0x96a6, 'pvr_resint_array')
d.comment(0x96a7, 'count the "(" in the name length too', align=Align.INLINE)
d.comment(0x96a9, 'index the array', align=Align.INLINE)
d.comment(0x96ac, 'check for trailing ! or ?', align=Align.INLINE)
d.comment(0x96af, 'String variable: step past "$"', align=Align.INLINE)
d.label(0x96af, 'pvr_string')
d.comment(0x96b0, 'advance the scan', align=Align.INLINE)
d.comment(0x96b1, 'record the name length', align=Align.INLINE)
d.comment(0x96b3, 'peek at the char after the $', align=Align.INLINE)
d.comment(0x96b4, 'mark the type string', align=Align.INLINE)
d.comment(0x96b6, 'following character', align=Align.INLINE)
d.comment(0x96b8, "'('  -> string array", align=Align.INLINE)
d.char_literal(0x96b9)
d.comment(0x96ba, 'yes', align=Align.INLINE)
d.comment(0x96bc, 'Look the string variable up', align=Align.INLINE)
d.comment(0x96bf, 'not found: undefined', align=Align.INLINE)
d.comment(0x96c1, 'Update the scan offset', align=Align.INLINE)
d.comment(0x96c3, 'Type = string lvalue (&81)', align=Align.INLINE)
d.comment(0x96c5, 'store in the type byte (&2C)', align=Align.INLINE)
d.comment(0x96c7, 'found: SEC', align=Align.INLINE)
d.comment(0x96c8, 'Return', align=Align.INLINE)
d.comment(0x96c9, 'String array: step past "("', align=Align.INLINE)
d.label(0x96c9, 'pvr_string_array')
d.comment(0x96ca, 'record the name length', align=Align.INLINE)
d.comment(0x96cc, 'mark the type string', align=Align.INLINE)
d.comment(0x96ce, 'index the array', align=Align.INLINE)
d.comment(0x96d1, 'Type = string lvalue (&81)', align=Align.INLINE)
d.comment(0x96d3, 'store in the type byte (&2C)', align=Align.INLINE)
d.comment(0x96d5, 'found: SEC', align=Align.INLINE)
d.comment(0x96d6, 'Return', align=Align.INLINE)
d.comment(0x96d7, 'No such array: Array error', align=Align.INLINE)

d.label(0x96d7, 'array_error')
d.subroutine(0x96df, 'index_array',
             title='Locate an array and evaluate one subscript',
             description='Find the named array (find_variable) and step the '
                         'value pointer to the addressed element, evaluating one '
                         'subscript at PtrB and bounds-checking it. Raises Array '
                         'on a missing array, Subscript on an out-of-range index.',
             on_entry={'(zp_general) (&37/&38)': 'the array name reference',
                       'zp_text_ptr2 (&19/&1A)': 'PtrB at the subscript'},
             on_exit={'zp_iwa (&2A/&2B)': 'a pointer to the element',
                      'zp_iwa_2 (&2C)': 'the element type',
                      'BRK': 'Array / Subscript on error'})
# index_array (&96DF): locate the array and step to one element.
d.comment(0x96df, 'Find the array', align=Align.INLINE)
d.comment(0x96e2, 'missing: Array error', align=Align.INLINE)
d.comment(0x96e4, 'Update the scan offset', align=Align.INLINE)
d.comment(0x96e6, 'Save the variable type...', align=Align.INLINE)
d.comment(0x96e8, 'push the type', align=Align.INLINE)
d.comment(0x96e9, '...and the array data pointer', align=Align.INLINE)
d.comment(0x96eb, 'push the low byte', align=Align.INLINE)
d.comment(0x96ec, 'high byte', align=Align.INLINE)
d.comment(0x96ee, 'push it', align=Align.INLINE)
d.comment(0x96ef, 'Offset to the array data (1 + 2*dims)', align=Align.INLINE)
d.comment(0x96f1, 'read it', align=Align.INLINE)
d.comment(0x96f3, 'more than a few?', align=Align.INLINE)
d.comment(0x96f5, 'no: handle the small case', align=Align.INLINE)
d.comment(0x96f7, 'Accumulate the flattened index', align=Align.INLINE)
d.comment(0x96f8, 'running index = 0', align=Align.INLINE)
d.comment(0x96fb, 'one subscript so far', align=Align.INLINE)
d.comment(0x96fd, 'store it', align=Align.INLINE)

# ----------------------------------------------------------------------
# Array element address (&96FF): evaluate the comma-separated subscripts
# and flatten them to a linear element offset by Horner's method
# (index = index * extent + subscript) with a bounds check per
# dimension, then scale by the element size (5 bytes real/string, 4
# integer) and add the array base, leaving the element address in &2A.
# ----------------------------------------------------------------------
d.comment(0x96ff, 'Stack the running index', align=Align.INLINE)
# index_array
d.label(0x96ff, 'idxarr_loop')
d.comment(0x9702, 'Evaluate the next subscript', align=Align.INLINE)
d.comment(0x9705, 'step past it', align=Align.INLINE)
d.comment(0x9707, "comma (another subscript)?", align=Align.INLINE)
d.char_literal(0x9708)
d.comment(0x9709, 'no: wrong dimension count -> Array', align=Align.INLINE)
d.comment(0x970b, 'Unstack the running index', align=Align.INLINE)
d.comment(0x970d, 'into &39/&3A', align=Align.INLINE)
d.comment(0x9710, 'dimension descriptor offset', align=Align.INLINE)
d.comment(0x9712, 'Recover the array base pointer', align=Align.INLINE)
d.comment(0x9713, 'high byte', align=Align.INLINE)
d.comment(0x9715, 'low byte', align=Align.INLINE)
d.comment(0x9716, 'set the pointer', align=Align.INLINE)
d.comment(0x9718, 're-stack it', align=Align.INLINE)
d.comment(0x9719, 'high byte', align=Align.INLINE)
d.comment(0x971b, 'push it too', align=Align.INLINE)
d.comment(0x971c, 'Bounds-check this subscript', align=Align.INLINE)
d.comment(0x971f, 'advance to the next dimension', align=Align.INLINE)
d.comment(0x9721, "This dimension's extent: low", align=Align.INLINE)
d.comment(0x9723, 'store it', align=Align.INLINE)
d.comment(0x9725, '...high', align=Align.INLINE)
d.comment(0x9726, 'read it', align=Align.INLINE)
d.comment(0x9728, 'store it', align=Align.INLINE)
d.comment(0x972a, 'Add the subscript into the running index', align=Align.INLINE)
d.comment(0x972c, '+ subscript low,', align=Align.INLINE)
d.comment(0x972e, 'store the low byte', align=Align.INLINE)
d.comment(0x9730, 'high byte', align=Align.INLINE)
d.comment(0x9732, '+ subscript high,', align=Align.INLINE)
d.comment(0x9734, 'store the high byte', align=Align.INLINE)
d.comment(0x9736, 'index *= this extent (Horner)', align=Align.INLINE)
d.comment(0x9739, 'Dimensions processed so far', align=Align.INLINE)
d.comment(0x973b, 'set carry for subtract', align=Align.INLINE)
d.comment(0x973c, 'data offset (byte 0)', align=Align.INLINE)
d.comment(0x973e, 'minus the offset reached', align=Align.INLINE)
d.comment(0x9740, 'more dimensions to come?', align=Align.INLINE)
d.comment(0x9742, 'yes: next subscript', align=Align.INLINE)
d.comment(0x9744, 'Stack the running index', align=Align.INLINE)
d.comment(0x9747, 'Evaluate the final subscript', align=Align.INLINE)
d.comment(0x974a, '...as an integer', align=Align.INLINE)
d.comment(0x974d, 'Recover the array base', align=Align.INLINE)
d.comment(0x974e, 'high byte', align=Align.INLINE)
d.comment(0x9750, 'low byte', align=Align.INLINE)
d.comment(0x9751, 'set the pointer', align=Align.INLINE)
d.comment(0x9753, 'Unstack the running index', align=Align.INLINE)
d.comment(0x9755, 'into &39/&3A', align=Align.INLINE)
d.comment(0x9758, 'dimension descriptor offset', align=Align.INLINE)
d.comment(0x975a, 'Bounds-check the final subscript', align=Align.INLINE)
d.comment(0x975d, 'Add it into the index', align=Align.INLINE)
d.comment(0x975e, 'subscript low', align=Align.INLINE)
d.comment(0x9760, 'plus the index low,', align=Align.INLINE)
d.comment(0x9762, 'store it', align=Align.INLINE)
d.comment(0x9764, 'subscript high', align=Align.INLINE)
d.comment(0x9766, 'plus the index high,', align=Align.INLINE)
d.comment(0x9768, 'store it', align=Align.INLINE)
d.comment(0x976a, 'scale by the element size', align=Align.INLINE)
d.comment(0x976c, 'One subscript: evaluate it', align=Align.INLINE)
d.label(0x976c, 'idxarr_one')
d.comment(0x976f, '...as an integer', align=Align.INLINE)
d.comment(0x9772, 'Recover the array base', align=Align.INLINE)
d.comment(0x9773, 'high byte', align=Align.INLINE)
d.comment(0x9775, 'low byte', align=Align.INLINE)
d.comment(0x9776, 'set the pointer', align=Align.INLINE)
d.comment(0x9778, 'descriptor offset 1', align=Align.INLINE)
d.comment(0x977a, 'Bounds-check the subscript', align=Align.INLINE)
d.comment(0x977d, 'Element type', align=Align.INLINE)
d.label(0x977d, 'idxarr_type')
d.comment(0x977e, 'store it', align=Align.INLINE)
d.comment(0x9780, 'real/string (5 bytes)?', align=Align.INLINE)
d.comment(0x9782, 'no: integer (4 bytes)', align=Align.INLINE)
d.comment(0x9784, 'index *= 5 (x*4 + x)', align=Align.INLINE)
d.comment(0x9786, 'keep the original low', align=Align.INLINE)
d.comment(0x9788, 'index x2:', align=Align.INLINE)
d.comment(0x978a, 'carry up to the high byte,', align=Align.INLINE)
d.comment(0x978c, 'index x4:', align=Align.INLINE)
d.comment(0x978e, 'carry up again', align=Align.INLINE)
d.comment(0x9790, 'add the original (x5),', align=Align.INLINE)
d.comment(0x9792, 'store the low byte', align=Align.INLINE)
d.comment(0x9794, 'original high byte', align=Align.INLINE)
d.comment(0x9795, 'add x4 high (x5),', align=Align.INLINE)
d.comment(0x9797, 'store the high byte', align=Align.INLINE)
d.comment(0x9799, 'done: skip the x4 path', align=Align.INLINE)
d.comment(0x979b, 'index *= 4', align=Align.INLINE)
d.label(0x979b, 'idxarr_scale')
d.comment(0x979d, 'carry into the high byte,', align=Align.INLINE)
d.comment(0x979f, 'index x4:', align=Align.INLINE)
d.comment(0x97a1, 'carry up again', align=Align.INLINE)
d.comment(0x97a3, 'Add the element offset within the descriptor',
          align=Align.INLINE)
d.label(0x97a3, 'idxarr_offset')
d.comment(0x97a4, 'plus the scaled index low,', align=Align.INLINE)
d.comment(0x97a6, 'store the low byte', align=Align.INLINE)
d.comment(0x97a8, 'no carry into the high byte', align=Align.INLINE)
d.comment(0x97aa, 'else bump the high byte', align=Align.INLINE)
d.comment(0x97ac, 'clear carry for the base add', align=Align.INLINE)
d.comment(0x97ad, 'Element address = base + offset', align=Align.INLINE)
d.label(0x97ad, 'idxarr_addr')
d.comment(0x97af, 'plus the offset low,', align=Align.INLINE)
d.comment(0x97b1, 'store the low byte', align=Align.INLINE)
d.comment(0x97b3, 'base high byte', align=Align.INLINE)
d.comment(0x97b5, 'plus the offset high,', align=Align.INLINE)
d.comment(0x97b7, 'store it: element address in IWA', align=Align.INLINE)
d.comment(0x97b9, 'Return', align=Align.INLINE)

d.subroutine(0x97ba, 'check_subscript_bound',
             title='Check a subscript against a dimension extent',
             description='Raise Subscript if the subscript in IWA is negative '
                         'or not less than the two-byte dimension extent at '
                         '(zp_general),Y, otherwise advance Y past the extent.',
             on_entry={'zp_iwa (&2A-&2D)': 'the subscript to check',
                       'zp_general (&37/&38)': 'a pointer to the dimension data',
                       'Y': 'offset of the two-byte extent'},
             on_exit={'Y': 'advanced past the two-byte extent',
                      'X': 'preserved', 'BRK': 'Subscript if out of range'})
# check_subscript_bound (&97BA): Subscript error if out of range.
d.comment(0x97ba, 'Top bits of the subscript', align=Align.INLINE)
d.comment(0x97bc, 'keep just bits 6-7', align=Align.INLINE)
d.comment(0x97be, 'combine with the high bytes...', align=Align.INLINE)
d.comment(0x97c0, 'and byte 3', align=Align.INLINE)
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

# check_subscript_bound / check_line_number space skip
d.label(0x97d1, 'subscript_error')
d.comment(0x97dd, 'Advance', align=Align.INLINE)
d.label(0x97dd, 'chkline_skip')

d.subroutine(0x97df, 'check_line_number',
             title='Test for an embedded line number',
             description='Skip spaces at the text pointer; if the next token is '
                         'a line-number token (&8D), fall into decode_line_number '
                         'to decode it into IWA and return carry set, otherwise '
                         'return carry clear.',
             on_entry={'zp_text_ptr (&0B/&0C)': 'the program text pointer (PtrA)',
                       'zp_text_ptr_off (&0A)': 'offset of the next character'},
             on_exit={'C': 'set if a line number was found and decoded',
                      'zp_iwa (&2A/&2B)': 'the line number (when found)',
                      'zp_text_ptr_off (&0A)': 'advanced past it (when found)'})
# check_line_number (&97DF) / decode_line_number (&97EB).
d.comment(0x97df, 'Next character', align=Align.INLINE)
d.comment(0x97e1, 'read it', align=Align.INLINE)
d.comment(0x97e3, 'space?', align=Align.INLINE)
d.char_literal(0x97e4)
d.comment(0x97e5, 'skip it', align=Align.INLINE)
d.comment(0x97e7, 'line-number token?', align=Align.INLINE)
d.comment(0x97e9, 'no: carry clear', align=Align.INLINE)
d.subroutine(0x97eb, 'decode_line_number',
             title='Decode a 3-byte line number into IWA',
             description='Reverse the three-byte &8D line-number encoding, '
                         'reconstructing the 16-bit line number in IWA (the two '
                         'high-bit pairs are recovered from the control byte). '
                         'The inverse of encode_line_number, and like it exact '
                         'only for 0-32767.',
             on_entry={'zp_text_ptr (&0B/&0C)': 'the program text pointer (PtrA)',
                       'Y': 'offset of the &8D token'},
             on_exit={'zp_iwa (&2A/&2B)': 'the decoded 16-bit line number',
                      'zp_text_ptr_off (&0A)': 'advanced past the 3 bytes',
                      'C': 'set (line number found)'})
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
# decode_line_number / eval_after_eq / expect_eq
d.label(0x9805, 'not_line_number')
d.comment(0x9806, 'Return', align=Align.INLINE)

# sub_c9807: copy PtrA to PtrB, then expect "=" and evaluate.
d.comment(0x9807, 'Copy PtrA to PtrB', align=Align.INLINE)
d.label(0x9807, 'copy_ptra_to_ptrb')
d.comment(0x9809, '(low)', align=Align.INLINE)
d.comment(0x980b, 'high...', align=Align.INLINE)
d.comment(0x980d, '(high)', align=Align.INLINE)
d.comment(0x980f, 'offset...', align=Align.INLINE)
d.comment(0x9811, '(offset)', align=Align.INLINE)
d.subroutine(
    0x9813, 'eval_after_eq',
    title='Expect "=" then evaluate the right-hand side',
    description="""Skip spaces at PtrB, require an "=" sign, then evaluate the
expression that follows, leaving the value in the accumulator with its
type in zp_var_type. Raises Mistake if "=" is missing.
""",
    on_entry={'zp_text_ptr2 (&19/&1A)': 'PtrB before the "="'},
    on_exit={'A': 'the result type (also in zp_var_type, &27)',
             'zp_iwa / zp_fwa / string_work (&0600)': 'the evaluated value',
             'BRK': 'Mistake if "=" is missing'},
)
d.comment(0x9813, 'Next character', align=Align.INLINE)
d.comment(0x9815, 'and advance', align=Align.INLINE)
d.comment(0x9817, 'read it', align=Align.INLINE)
d.comment(0x9819, 'space?', align=Align.INLINE)
d.char_literal(0x981a)
d.comment(0x981b, 'skip it', align=Align.INLINE)
d.comment(0x981d, '"="?', align=Align.INLINE)
d.char_literal(0x981e)
d.comment(0x981f, 'yes: evaluate', align=Align.INLINE)
d.comment(0x9821, 'Mistake error', align=Align.INLINE)
d.label(0x9821, 'mistake_error')
d.comment(0x982a, 'Mistake error', align=Align.INLINE)
d.subroutine(
    0x982a, 'syntax_error',
    title='Raise "Syntax error" error',
    description="""Raise BASIC error &10, "Syntax error", via a BRK error block. Reached
when a statement or expression is malformed (e.g. from
check_end_of_statement when unexpected text follows a statement). Does
not return.
""",
    on_exit={
        'control': 'raises BRK error &10 "Syntax error"; does not return to the caller',
    },
)
d.comment(0x9838, 'Escape error', align=Align.INLINE)
d.label(0x9838, 'escape_error')
d.subroutine(0x9841, 'expect_eq', title='Require "=" at the parser pointer',
             description='Skip spaces at PtrB and raise Mistake unless the next '
                         'character is "=".',
             on_entry={'zp_text_ptr2 (&19/&1A)': 'PtrB at the parser position'},
             on_exit={'A': 'the "=" character (consumed)',
                      'zp_text_ptr2_off (&1B)': 'advanced past the "="',
                      'BRK': 'Mistake if "=" is missing'})
d.comment(0x9841, 'Skip spaces', align=Align.INLINE)
d.comment(0x9844, '"="?', align=Align.INLINE)
d.char_literal(0x9845)
d.comment(0x9846, 'no: Mistake', align=Align.INLINE)
d.comment(0x9848, 'Return', align=Align.INLINE)
d.comment(0x9849, 'Evaluate the right-hand side', align=Align.INLINE)
d.label(0x9849, 'eval_rhs')
d.comment(0x984c, 'Result type', align=Align.INLINE)
d.subroutine(
    0x984c, 'assign_check_end',
    title='Sync PtrB offset and require statement end after an assignment',
    description="""Tail shared by assignment and function-return paths once the right-hand-side value has been computed: move the pending result byte into
A, resync Y to PtrB's offset (zp_text_ptr2_off, &1B), and tail-jump
into check_end_of_statement at cend_check to demand the statement
terminator against PtrA. Unlike eval_rhs (&9849) it does not evaluate
the RHS itself; the value is assumed already in place.
""",
    on_entry={
        'X': 'the result byte left by the assignment / RHS evaluation (the value type)',
        'zp_text_ptr (&0B)': 'the program text pointer (PtrA)',
        'zp_text_ptr2_off (&1B)': "PtrB's offset at the end of the parsed RHS",
    },
    on_exit={
        'control': 'jumps into check_end_of_statement (cend_check); returns via its rts with PtrA advanced past the statement, or BRK Syntax error / Escape',
    },
)
d.comment(0x984d, 'Sync the program pointer', align=Align.INLINE)
d.comment(0x984f, 'check the statement ends', align=Align.INLINE)
d.comment(0x9852, 'Sync the program pointer', align=Align.INLINE)
d.subroutine(
    0x9852, 'sync_text_ptr',
    title="Resync PtrA's offset to PtrB, then require statement end",
    description="""Load the resume position from PtrB's offset (zp_text_ptr2_off, &1B)
into Y and tail-jump into check_end_of_statement at cend_back. Used
after a sub-parse that tracked its position in PtrB (e.g. FOR /
assignment operands): it resumes at PtrB's offset against the PtrA
text pointer and demands the statement end there, advancing PtrA to
the next statement.
""",
    on_entry={
        'zp_text_ptr (&0B)': 'the program text pointer (PtrA)',
        'zp_text_ptr2_off (&1B)': 'PtrB offset to resume from',
    },
    on_exit={
        'control': 'jumps into check_end_of_statement (cend_back); returns via its rts with PtrA advanced past the statement, or BRK Syntax error / Escape',
    },
)
d.comment(0x9854, 'check the statement ends', align=Align.INLINE)

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
    on_entry={'zp_text_ptr (&0B/&0C)': 'the program text pointer (PtrA)',
              'zp_text_ptr_off (&0A)': 'offset of the next character'},
    on_exit={'zp_text_ptr_off (&0A)': 'at the statement terminator',
             'A': 'the terminator character',
             'BRK': 'Syntax error if more text follows'},
)
# check_end_of_statement (&9857): require ':', end-of-line or ELSE.
d.comment(0x9857, 'Program pointer offset', align=Align.INLINE)
d.comment(0x9859, 'step back', align=Align.INLINE)
# check_end_of_statement and statement advance
d.label(0x9859, 'cend_back')
d.comment(0x985a, 'Next character', align=Align.INLINE)
d.label(0x985a, 'cend_skip_loop')
d.comment(0x985b, 'read it', align=Align.INLINE)
d.comment(0x985d, 'space?', align=Align.INLINE)
d.char_literal(0x985e)
d.comment(0x985f, 'skip it', align=Align.INLINE)
d.comment(0x9861, "':' statement separator?", align=Align.INLINE)
d.char_literal(0x9862)
d.label(0x9861, 'cend_check')
d.comment(0x9863, 'yes', align=Align.INLINE)
d.comment(0x9865, 'end of line?', align=Align.INLINE)
d.comment(0x9867, 'yes', align=Align.INLINE)
d.comment(0x9869, 'ELSE token?', align=Align.INLINE)
d.comment(0x986b, 'none: Mistake (syntax error)', align=Align.INLINE)
d.comment(0x986d, 'Advance the program pointer past the statement',
          align=Align.INLINE)
d.subroutine(
    0x986d, 'skip_to_statement_end',
    title='Advance PtrA past the current statement',
    description="""Add the terminator offset in Y to the PtrA text pointer (zp_text_ptr,
&0B/&0C), carrying into the high byte, so PtrA now addresses the
statement terminator; reset the character offset zp_text_ptr_off (&0A)
to 1; then poll ESCFLG and raise Escape if pressed before returning.
The common tail of the end-of-statement check and several statement
handlers.
""",
    on_entry={
        'Y': 'offset of the statement terminator within the line',
        'zp_text_ptr (&0B)': 'the program text pointer (PtrA)',
    },
    on_exit={
        'zp_text_ptr (&0B)': 'advanced to the terminator (&0B/&0C)',
        'zp_text_ptr_off (&0A)': 'reset to 1',
        'A': '1 (from the reset offset)',
        'control': 'rts, unless Escape is pending (jumps to escape_error)',
    },
)
d.comment(0x986e, 'offset to A,', align=Align.INLINE)
d.comment(0x986f, '+ pointer low,', align=Align.INLINE)
d.comment(0x9871, 'store low,', align=Align.INLINE)
d.comment(0x9873, 'no carry into the high byte', align=Align.INLINE)
d.comment(0x9875, 'carry into the high byte', align=Align.INLINE)
d.comment(0x9877, 'Reset the offset to 1', align=Align.INLINE)
d.label(0x9877, 'reset_offset_1')
d.comment(0x9879, 'store it (&0A)', align=Align.INLINE)
d.comment(0x987b, 'Escape pressed (ESCFLG)?', align=Align.INLINE)
d.label(0x987b, 'check_escape')
d.comment(0x987d, 'yes: raise Escape', align=Align.INLINE)
d.comment(0x987f, 'Return', align=Align.INLINE)

# step_statement (&9880): advance to the next statement, with TRACE.
d.comment(0x9880, 'Check this statement is terminated', align=Align.INLINE)
d.label(0x9880, 'check_statement_terminated')
d.comment(0x9883, 'Re-read the terminator', align=Align.INLINE)
d.comment(0x9884, 'read it', align=Align.INLINE)
d.comment(0x9886, "':' (more on this line)?", align=Align.INLINE)
d.char_literal(0x9887)
d.comment(0x9888, 'yes: continue on the line', align=Align.INLINE)
d.comment(0x988a, 'At the end of program memory?', align=Align.INLINE)
d.comment(0x988c, 'in the &0700 buffer (immediate)?', align=Align.INLINE)
d.comment(0x988e, 'yes: return to immediate mode', align=Align.INLINE)
d.comment(0x9890, 'Next byte (line-number marker)', align=Align.INLINE)
d.subroutine(
    0x9890, 'step_to_next_line',
    title='Advance PtrA to the next program line',
    description="""Step from the current line's terminating CR onto the next line: if the
next line-number marker has bit 7 set the program has ended and
control jumps to immediate_loop; otherwise, when TRACE is enabled,
load the line number into zp_iwa and call trace_line, then skip the
3-byte line header and reset the character offset. Returns with Z
clear so callers can branch to run the next statement.
""",
    on_entry={
        'zp_text_ptr (&0B/&0C)': 'the current program line (PtrA)',
        'Y': "offset of the current line's terminating CR within the line",
    },
    on_exit={
        'zp_text_ptr (&0B/&0C)': 'advanced to the next program line',
        'zp_text_ptr_off (&0A)': 'reset to 1',
        'zp_iwa (&2A/&2B)': 'the new line number, when TRACE is on',
        'control': 'rts with Z clear (more program follows); at end of program jmps to immediate_loop and does not return',
    },
)
d.comment(0x9891, 'read it', align=Align.INLINE)
d.comment(0x9893, 'end of program: immediate mode', align=Align.INLINE)
d.comment(0x9895, 'TRACE on?', align=Align.INLINE)
d.comment(0x9897, 'no: skip the line number', align=Align.INLINE)
d.comment(0x9899, 'Save the offset', align=Align.INLINE)
d.comment(0x989a, 'push it', align=Align.INLINE)
d.comment(0x989b, 'Line number high byte', align=Align.INLINE)
d.comment(0x989c, 'read it,', align=Align.INLINE)
d.comment(0x989e, 'push it', align=Align.INLINE)
d.comment(0x989f, 'Line number low byte', align=Align.INLINE)
d.comment(0x98a0, 'read it,', align=Align.INLINE)
d.comment(0x98a2, 'low byte to Y,', align=Align.INLINE)
d.comment(0x98a3, 'high byte to A', align=Align.INLINE)
d.comment(0x98a4, 'IWA = line number', align=Align.INLINE)
d.comment(0x98a7, 'trace it', align=Align.INLINE)
d.comment(0x98aa, 'Restore the offset', align=Align.INLINE)
d.comment(0x98ab, 'into Y', align=Align.INLINE)
d.comment(0x98ac, 'Step past the 3-byte line header', align=Align.INLINE)
d.label(0x98ac, 'step_past_line_header')
d.comment(0x98ad, 'set carry (advance by offset + 1),', align=Align.INLINE)
d.comment(0x98ae, 'offset to A,', align=Align.INLINE)
d.comment(0x98af, '+ pointer low,', align=Align.INLINE)
d.comment(0x98b1, 'store low,', align=Align.INLINE)
d.comment(0x98b3, 'no carry into the high byte', align=Align.INLINE)
d.comment(0x98b5, 'carry into the high byte', align=Align.INLINE)
d.comment(0x98b7, 'Reset the offset to 1', align=Align.INLINE)
d.label(0x98b7, 'line_reset_offset')
d.comment(0x98b9, 'store it (&0A)', align=Align.INLINE)
d.comment(0x98bb, 'Return', align=Align.INLINE)
d.comment(0x98bc, 'End of program: immediate mode', align=Align.INLINE)
d.label(0x98bc, 'to_immediate')
d.comment(0x98bf, 'Type mismatch error', align=Align.INLINE)

d.label(0x98bf, 'if_type_error')
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
# stmt_if
d.label(0x98cc, 'if_skip_cond')
d.comment(0x98ce, 'copy it to PtrA', align=Align.INLINE)
d.comment(0x98d0, 'Is the condition value zero (false)?', align=Align.INLINE)
d.comment(0x98d2, 'or byte 1,', align=Align.INLINE)
d.comment(0x98d4, 'byte 2,', align=Align.INLINE)
d.comment(0x98d6, 'byte 3', align=Align.INLINE)
d.comment(0x98d8, 'false: look for ELSE', align=Align.INLINE)
d.comment(0x98da, 'true: is the next token THEN?', align=Align.INLINE)
d.comment(0x98dc, 'yes', align=Align.INLINE)
d.comment(0x98de, 'no THEN: execute the statement that follows',
          align=Align.INLINE)
d.label(0x98de, 'if_no_then')
d.comment(0x98e1, 'Step past THEN', align=Align.INLINE)
d.label(0x98e1, 'if_then')
d.comment(0x98e3, 'Is a line number following (THEN <line>)?',
          align=Align.INLINE)
d.label(0x98e3, 'if_then_line')
d.comment(0x98e6, 'no: execute the statements after THEN', align=Align.INLINE)
d.comment(0x98e8, 'yes: set up the line number...', align=Align.INLINE)
d.comment(0x98eb, 'to the line start, test Escape', align=Align.INLINE)
d.comment(0x98ee, '...and GOTO it', align=Align.INLINE)
d.comment(0x98f1, 'False: scan the rest of the line for ELSE',
          align=Align.INLINE)
d.label(0x98f1, 'if_false')
d.comment(0x98f3, 'Next character', align=Align.INLINE)
d.label(0x98f3, 'if_scan_else_loop')
d.comment(0x98f5, 'end of line?', align=Align.INLINE)
d.comment(0x98f7, 'yes: move to the next line', align=Align.INLINE)
d.comment(0x98f9, 'advance', align=Align.INLINE)
d.comment(0x98fa, 'ELSE token?', align=Align.INLINE)
d.comment(0x98fc, 'no: keep scanning', align=Align.INLINE)
d.comment(0x98fe, 'found ELSE: point past it', align=Align.INLINE)
d.comment(0x9900, 'execute what follows ELSE', align=Align.INLINE)
d.comment(0x9902, 'No ELSE: continue at the next line', align=Align.INLINE)

d.label(0x9902, 'if_no_else')

d.subroutine(0x9905, 'trace_line',
             title='Print [line] when TRACE is active',
             description='If the line number in IWA is at or below the TRACE '
                         'ceiling, print it in brackets; otherwise do nothing.',
             on_entry={'zp_iwa (&2A/&2B)': 'the current line number',
                       'zp_trace_max (&21/&22)': 'the TRACE ceiling'},
             on_exit={'the output': '[line] when traced, nothing otherwise'})
# trace_line (&9905): print [line] when within the TRACE ceiling.
d.comment(0x9905, 'Line number vs TRACE ceiling', align=Align.INLINE)
d.comment(0x9907, 'vs ceiling low,', align=Align.INLINE)
d.comment(0x9909, 'line high', align=Align.INLINE)
d.comment(0x990b, 'minus ceiling high', align=Align.INLINE)
d.comment(0x990d, 'above the ceiling: do not trace', align=Align.INLINE)
d.comment(0x990f, "Print '['", align=Align.INLINE)
d.char_literal(0x9910)
d.comment(0x9911, 'output it', align=Align.INLINE)
d.comment(0x9914, 'print the line number', align=Align.INLINE)
d.comment(0x9917, "Print ']'", align=Align.INLINE)
d.char_literal(0x9918)
d.comment(0x9919, 'output it', align=Align.INLINE)
d.comment(0x991c, 'and a space', align=Align.INLINE)

d.subroutine(0x991f, 'print_line_number',
             title='Print a 16-bit line number in decimal',
             description='Convert the value in IWA to decimal by repeated '
                         'subtraction of the powers of ten at &996B/&99B9, '
                         'suppressing leading zeros, optionally right-'
                         'justified in a field (the sub_c9923 entry uses a '
                         '5-digit TRACE field).',
             on_entry={'zp_iwa (&2A/&2B)': 'the line number to print'},
             on_exit={'the output': 'the decimal digits printed',
                      'zp_count (&1E)': 'the print column, advanced'})
# print_line_number (&991F): IWA -> decimal.
d.comment(0x991f, 'Default: no field padding', align=Align.INLINE)
d.comment(0x9921, 'always: skip the TRACE entry', align=Align.INLINE)
d.comment(0x9923, 'TRACE entry: 5-digit field', align=Align.INLINE)
# print_line_number + powers-of-ten tables
d.subroutine(
    0x9923, 'trace_print_number',
    title='Print a line number in a 5-digit field',
    description="""Alternate entry to print_line_number that prints the value in zp_iwa
as a decimal line number right-justified in a 5-character field (used
by TRACE and LIST). Loads a field width of 5, then joins
print_line_number at plnum_setwidth.
""",
    on_entry={
        'zp_iwa (&2A/&2B)': 'the line number to print',
    },
    on_exit={
        'zp_count (&1E)': 'the print column, advanced past the 5-character field',
    },
)
d.comment(0x9925, 'Field width', align=Align.INLINE)
d.label(0x9925, 'plnum_setwidth')
d.comment(0x9927, 'Five powers of ten, index 4..0', align=Align.INLINE)
d.comment(0x9929, 'Clear this digit', align=Align.INLINE)
d.label(0x9929, 'plnum_clear_loop')
d.comment(0x992b, 'zero its count', align=Align.INLINE)
d.comment(0x992d, 'set carry for the subtraction', align=Align.INLINE)
d.comment(0x992e, 'Subtract this power of ten from IWA', align=Align.INLINE)
d.label(0x992e, 'plnum_sub_loop')
d.comment(0x9930, 'minus the low byte,', align=Align.INLINE)
d.comment(0x9933, 'stash the low result', align=Align.INLINE)
d.comment(0x9934, 'IWA high byte', align=Align.INLINE)
d.comment(0x9936, 'minus the high byte', align=Align.INLINE)
d.comment(0x9939, 'underflow: digit complete', align=Align.INLINE)
d.comment(0x993b, 'keep the remainder', align=Align.INLINE)
d.comment(0x993d, '(low byte too)', align=Align.INLINE)
d.comment(0x993f, 'count the digit', align=Align.INLINE)
d.comment(0x9941, 'subtract again', align=Align.INLINE)
d.comment(0x9943, 'Next power of ten', align=Align.INLINE)
d.label(0x9943, 'plnum_next_power')
d.comment(0x9944, 'until all five powers used', align=Align.INLINE)
d.comment(0x9946, 'Find the most significant non-zero digit',
          align=Align.INLINE)
d.comment(0x9948, 'step down to the next digit', align=Align.INLINE)
d.label(0x9948, 'plnum_digit_loop')
d.comment(0x9949, 'units digit: always shown', align=Align.INLINE)
d.comment(0x994b, 'is this digit zero?', align=Align.INLINE)
d.comment(0x994d, 'yes: skip the leading zero', align=Align.INLINE)
d.comment(0x994f, 'Index of the top digit', align=Align.INLINE)
d.label(0x994f, 'plnum_top_digit')
d.comment(0x9951, 'Field padding requested?', align=Align.INLINE)
d.comment(0x9953, 'no', align=Align.INLINE)
d.comment(0x9955, 'leading spaces = field - digits', align=Align.INLINE)
d.comment(0x9957, 'none', align=Align.INLINE)
d.comment(0x9959, 'space count into Y', align=Align.INLINE)
d.comment(0x995a, 'print a leading space', align=Align.INLINE)
d.label(0x995a, 'plnum_space_loop')
d.comment(0x995d, 'one fewer space', align=Align.INLINE)
d.comment(0x995e, 'until the field is padded', align=Align.INLINE)
d.comment(0x9960, 'Digit', align=Align.INLINE)
d.label(0x9960, 'plnum_print_loop')
d.comment(0x9962, 'to ASCII', align=Align.INLINE)
d.char_literal(0x9963)
d.comment(0x9964, 'print it', align=Align.INLINE)
d.comment(0x9967, 'next digit', align=Align.INLINE)
d.comment(0x9968, 'until all digits printed', align=Align.INLINE)
d.comment(0x996a, 'Return', align=Align.INLINE)

d.index_base(0x996b, 'powers_of_ten_lo')
d.subroutine(
    0x9970, 'find_program_line',
    title='Search the program for a line number',
    description="""Walk the program text from PAGE looking for the target line
number in IWA. Returns a scratch pointer (zp_fwb_exp/zp_fwb_m1) to the
matching line, or to the first line with a greater number (the insertion
point) when there is no exact match.
""",
    on_entry={'zp_iwa (&2A/&2B)': 'the target line number',
              'zp_page (&18)': 'PAGE, the start of the program'},
    on_exit={'(zp_fwb_exp) (&3D/&3E)': 'pointer to the line (or insertion point)',
             'C': 'clear if an exact match was found, set if not found'},
)
# ----------------------------------------------------------------------
# find_program_line (&9970): find the first line >= the target number.
# Walks the program from PAGE. Each line is <&0D> <hi> <lo> <len> <body>,
# stored in ascending order. Returns the line pointer in &3D/&3E; carry
# is clear when an exact match is found.
# ----------------------------------------------------------------------
d.comment(0x9970, 'Pointer low = 0', align=Align.INLINE)
d.comment(0x9972, 'scratch pointer in fwb_exp/m1', align=Align.INLINE)
d.comment(0x9974, 'Pointer high = PAGE', align=Align.INLINE)
d.comment(0x9976, 'pointer high', align=Align.INLINE)
d.comment(0x9978, "This line's number: high byte", align=Align.INLINE)
# find_program_line
d.label(0x9978, 'fpl_check_high')
d.comment(0x997a, 'read it', align=Align.INLINE)
d.comment(0x997c, 'vs the target high byte', align=Align.INLINE)
d.comment(0x997e, '>=: a candidate', align=Align.INLINE)
d.comment(0x9980, 'Line length', align=Align.INLINE)
d.label(0x9980, 'fpl_next_loop')
d.comment(0x9982, 'read it', align=Align.INLINE)
d.comment(0x9984, 'Advance to the next line', align=Align.INLINE)
d.comment(0x9986, 'pointer low', align=Align.INLINE)
d.comment(0x9988, 'no carry: same page', align=Align.INLINE)
d.comment(0x998a, 'carry into the pointer high', align=Align.INLINE)
d.comment(0x998c, 'continue', align=Align.INLINE)
d.comment(0x998e, 'high byte greater: found (not exact)', align=Align.INLINE)
d.label(0x998e, 'fpl_found')
d.comment(0x9990, "This line's number: low byte", align=Align.INLINE)
d.comment(0x9992, 'read it', align=Align.INLINE)
d.comment(0x9994, 'vs the target low byte', align=Align.INLINE)
d.comment(0x9996, 'less: next line', align=Align.INLINE)
d.comment(0x9998, 'greater: found (not exact)', align=Align.INLINE)
d.comment(0x999a, 'Exact match: leave the pointer at this line',
          align=Align.INLINE)
d.comment(0x999b, 'point at the line number', align=Align.INLINE)
d.comment(0x999d, '(store)', align=Align.INLINE)
d.comment(0x999f, 'no carry', align=Align.INLINE)
d.comment(0x99a1, 'carry into the pointer high', align=Align.INLINE)
d.comment(0x99a3, 'flag the exact match (carry clear)', align=Align.INLINE)
d.comment(0x99a4, 'Point at the line number', align=Align.INLINE)
d.label(0x99a4, 'fpl_return')
d.comment(0x99a6, 'Return', align=Align.INLINE)

d.comment(0x99a7, 'Division by zero error', align=Align.INLINE)
d.label(0x99a7, 'div_zero_error')
d.index_base(0x99b9, 'powers_of_ten_hi')
d.subroutine(0x99be, 'iwa_divide',
             title='Unsigned/signed 32-bit integer division',
             description='Divide the dividend (IWA, the left operand) by the '
                         'divisor (the right operand, evaluated here at PtrB). '
                         'Both are made positive and a 32-step shift-subtract '
                         'division runs with the dividend/quotient in &39-&3C '
                         'and the remainder in &3D-&40. The quotient sign is the '
                         'XOR of the operand signs (&37), the remainder sign the '
                         'dividend sign (&38). Raises Division by zero. Shared '
                         'by DIV (reads the quotient) and MOD (the remainder).',
             on_entry={'zp_iwa (&2A-&2D)': 'the dividend (left operand)',
                       'zp_text_ptr2 (&19/&1A)': 'PtrB at the divisor operand'},
             on_exit={'(&39-&3C)': 'the quotient',
                      '(&3D-&40)': 'the remainder',
                      '(&37) / (&38)': 'the quotient sign / remainder sign',
                      'BRK': 'Division by zero'})
# iwa_divide (&99BE): shift-subtract 32-bit integer division.
d.comment(0x99be, 'Coerce the dividend to integer', align=Align.INLINE)
d.comment(0x99bf, 'IWA = the integer dividend', align=Align.INLINE)
d.comment(0x99c2, 'Save the dividend sign', align=Align.INLINE)
d.comment(0x99c4, 'push it', align=Align.INLINE)
d.comment(0x99c5, 'take |dividend|', align=Align.INLINE)
d.comment(0x99c8, 'Stack it, evaluate the divisor', align=Align.INLINE)
d.comment(0x99cb, 'remember the operator', align=Align.INLINE)
d.comment(0x99cd, 'coerce the divisor to integer', align=Align.INLINE)
d.comment(0x99ce, 'IWA = the integer divisor', align=Align.INLINE)
d.comment(0x99d1, 'Recover the dividend sign', align=Align.INLINE)
d.comment(0x99d2, 'remainder takes the dividend sign', align=Align.INLINE)
d.comment(0x99d4, 'quotient sign = dividend XOR divisor', align=Align.INLINE)
d.comment(0x99d6, 'store the quotient sign (&37)', align=Align.INLINE)
d.comment(0x99d8, 'take |divisor|', align=Align.INLINE)
d.comment(0x99db, 'Move the dividend to the work area (&39-&3C)',
          align=Align.INLINE)
d.comment(0x99dd, 'unpack starting at &39', align=Align.INLINE)
d.comment(0x99e0, 'Clear the remainder (&3D-&40)', align=Align.INLINE)
d.comment(0x99e2, '&3E,', align=Align.INLINE)
d.comment(0x99e4, '&3F,', align=Align.INLINE)
d.comment(0x99e6, '&40', align=Align.INLINE)
d.comment(0x99e8, 'Divisor zero?', align=Align.INLINE)
d.comment(0x99ea, 'OR the low byte,', align=Align.INLINE)
d.comment(0x99ec, '&2B,', align=Align.INLINE)
d.comment(0x99ee, '&2C (all zero => /0)', align=Align.INLINE)
d.comment(0x99f0, 'yes: Division by zero', align=Align.INLINE)
d.comment(0x99f2, '32 bits', align=Align.INLINE)
d.comment(0x99f4, 'Normalise: count down', align=Align.INLINE)
# iwa_divide
d.label(0x99f4, 'idiv_norm_loop')
d.comment(0x99f5, 'dividend exhausted: done', align=Align.INLINE)
d.comment(0x99f7, 'shift the dividend left until the top bit is set',
          align=Align.INLINE)
d.comment(0x99f9, 'carrying up through &3A,', align=Align.INLINE)
d.comment(0x99fb, '&3B,', align=Align.INLINE)
d.comment(0x99fd, '&3C (until bit 7 is set)', align=Align.INLINE)
d.comment(0x99ff, 'loop', align=Align.INLINE)
d.comment(0x9a01, 'Shift a bit from dividend into the remainder',
          align=Align.INLINE)
d.label(0x9a01, 'idiv_shift_loop')
d.comment(0x9a03, 'dividend &3A,', align=Align.INLINE)
d.comment(0x9a05, '&3B,', align=Align.INLINE)
d.comment(0x9a07, '&3C,', align=Align.INLINE)
d.comment(0x9a09, 'into remainder &3D,', align=Align.INLINE)
d.comment(0x9a0b, '&3E,', align=Align.INLINE)
d.comment(0x9a0d, '&3F,', align=Align.INLINE)
d.comment(0x9a0f, '&40 (remainder high)', align=Align.INLINE)
d.comment(0x9a11, 'Try remainder - divisor', align=Align.INLINE)
d.comment(0x9a12, 'low byte &3D,', align=Align.INLINE)
d.comment(0x9a14, 'minus divisor low,', align=Align.INLINE)
d.comment(0x9a16, 'save the result,', align=Align.INLINE)
d.comment(0x9a17, 'byte &3E,', align=Align.INLINE)
d.comment(0x9a19, 'minus divisor &2B,', align=Align.INLINE)
d.comment(0x9a1b, 'save it,', align=Align.INLINE)
d.comment(0x9a1c, 'byte &3F,', align=Align.INLINE)
d.comment(0x9a1e, 'minus divisor &2C,', align=Align.INLINE)
d.comment(0x9a20, 'hold it in X,', align=Align.INLINE)
d.comment(0x9a21, 'high byte &40,', align=Align.INLINE)
d.comment(0x9a23, 'minus divisor high', align=Align.INLINE)
d.comment(0x9a25, "doesn't fit: leave the remainder", align=Align.INLINE)
d.comment(0x9a27, 'fits: keep the new remainder (quotient bit = 1)',
          align=Align.INLINE)
d.comment(0x9a29, 'and &3F,', align=Align.INLINE)
d.comment(0x9a2b, 'pull &3E,', align=Align.INLINE)
d.comment(0x9a2c, 'store it,', align=Align.INLINE)
d.comment(0x9a2e, 'pull &3D,', align=Align.INLINE)
d.comment(0x9a2f, 'store it', align=Align.INLINE)
d.comment(0x9a31, 'next bit', align=Align.INLINE)
d.comment(0x9a33, 'discard the trial subtraction', align=Align.INLINE)
d.label(0x9a33, 'idiv_restore')
d.comment(0x9a34, '(continued)', align=Align.INLINE)
d.comment(0x9a35, 'Next bit', align=Align.INLINE)
d.label(0x9a35, 'idiv_next_bit')
d.comment(0x9a36, 'loop', align=Align.INLINE)
d.comment(0x9a38, 'Return', align=Align.INLINE)

# fp_compare (&9A39 setup / &9A5F): FWA vs operand.
d.comment(0x9a39, 'Int vs real: save the operator', align=Align.INLINE)
# fp_compare (int/real/real dispatch + byte compare)
d.label(0x9a39, 'cmp_int_real')
d.comment(0x9a3b, 'unstack the integer', align=Align.INLINE)
d.comment(0x9a3e, 'stack the real', align=Align.INLINE)
d.comment(0x9a41, 'convert the integer to FWA', align=Align.INLINE)
d.comment(0x9a44, 'FWB = it', align=Align.INLINE)
d.comment(0x9a47, 'unstack the real operand', align=Align.INLINE)
d.comment(0x9a4a, 'into FWA', align=Align.INLINE)
d.comment(0x9a4d, 'compare', align=Align.INLINE)
d.comment(0x9a50, 'Real vs real: stack the left', align=Align.INLINE)
d.label(0x9a50, 'cmp_real_real')
d.comment(0x9a53, 'evaluate the right operand', align=Align.INLINE)
d.comment(0x9a56, 'save the operator', align=Align.INLINE)
d.comment(0x9a58, 'type', align=Align.INLINE)
d.comment(0x9a59, 'ensure real', align=Align.INLINE)
d.comment(0x9a5c, 'unstack the left operand', align=Align.INLINE)
d.subroutine(0x9a5f, 'fp_compare',
             title='Compare FWA with a fp variable',
             description='Unpack the packed real operand into FWB and compare it '
                         'with FWA by sign, exponent and mantissa, returning the '
                         'ordering for the relational operators.',
             on_entry={'zp_fwa (&2E-&35)': 'the left operand',
                       '(zp_fp_ptr) (&4B/&4C)': 'the packed real right operand'},
             on_exit={'Z': 'set if the values are equal',
                      'C': 'the sign-corrected ordering when they differ',
                      'A': 'nonzero when they differ'})
d.comment(0x9a5f, 'Unpack the operand into FWB', align=Align.INLINE)
d.comment(0x9a62, 'Restore the operator', align=Align.INLINE)
d.label(0x9a62, 'cmp_bytes')
d.comment(0x9a64, 'assume equal', align=Align.INLINE)
d.comment(0x9a66, 'FWB sign', align=Align.INLINE)
d.comment(0x9a68, 'keep the sign bit', align=Align.INLINE)
d.comment(0x9a6a, '(store)', align=Align.INLINE)
d.comment(0x9a6c, 'FWA sign', align=Align.INLINE)
d.comment(0x9a6e, 'keep the sign bit', align=Align.INLINE)
d.comment(0x9a70, 'signs differ?', align=Align.INLINE)
d.comment(0x9a72, 'yes: unequal', align=Align.INLINE)
d.comment(0x9a74, 'Compare exponents', align=Align.INLINE)
d.comment(0x9a76, 'vs FWA exp', align=Align.INLINE)
d.comment(0x9a78, 'differ', align=Align.INLINE)
d.comment(0x9a7a, 'Compare mantissa byte 1', align=Align.INLINE)
d.comment(0x9a7c, 'vs FWA m1', align=Align.INLINE)
d.comment(0x9a7e, 'differ', align=Align.INLINE)
d.comment(0x9a80, 'byte 2', align=Align.INLINE)
d.comment(0x9a82, 'vs FWA m2', align=Align.INLINE)
d.comment(0x9a84, 'differ', align=Align.INLINE)
d.comment(0x9a86, 'byte 3', align=Align.INLINE)
d.comment(0x9a88, 'vs FWA m3', align=Align.INLINE)
d.comment(0x9a8a, 'differ', align=Align.INLINE)
d.comment(0x9a8c, 'byte 4', align=Align.INLINE)
d.comment(0x9a8e, 'vs FWA m4', align=Align.INLINE)
d.comment(0x9a90, 'differ', align=Align.INLINE)

# Comparison result and the compare helper (&9A92).
d.comment(0x9a92, 'Equal: return', align=Align.INLINE)
d.comment(0x9a93, 'Combine the compare carry...', align=Align.INLINE)
d.label(0x9a93, 'cmp_combine')
d.comment(0x9a94, '...with the sign', align=Align.INLINE)
d.comment(0x9a96, '...for the ordering', align=Align.INLINE)
d.comment(0x9a97, 'result nonzero', align=Align.INLINE)
d.comment(0x9a99, 'Return', align=Align.INLINE)
d.comment(0x9a9a, 'Type mismatch error', align=Align.INLINE)
d.label(0x9a9a, 'cmp_type_error')
d.comment(0x9a9d, 'Current type', align=Align.INLINE)
d.subroutine(
    0x9a9d, 'compare_values',
    title='Compare the current value with the next operand',
    description="""Take the already-evaluated left value (whose type is in X), stack it,
evaluate the next arithmetic operand at PtrB, then compare the two -
integer, real or string - returning the ordering flags for the
relational operators. A one-instruction head (txa) on eval_and_compare
that supplies the left type in X.
""",
    on_entry={
        'X': 'the type of the left value (already evaluated)',
        'zp_iwa (&2A) / zp_fwa (&2E) / string_work (&0600)': 'the left value',
        'zp_text_ptr2 (&19/&1A)': 'PtrB at the right operand',
    },
    on_exit={
        'C': 'the ordering of left vs right',
        'Z': 'set if equal',
        'X': 'the next unconsumed operator token',
    },
)
d.subroutine(0x9a9e, 'eval_and_compare',
             title='Evaluate the next operand and compare',
             description='Stack the already-evaluated left value, evaluate the '
                         'next arithmetic operand at PtrB, then compare the two '
                         '(integer, real or string), returning the ordering '
                         'flags for the relational operators.',
             on_entry={'A': 'the type of the left value (already evaluated)',
                       'zp_iwa / zp_fwa / string_work (&0600)': 'the left value',
                       'zp_text_ptr2 (&19/&1A)': 'PtrB at the right operand'},
             on_exit={'C': 'the ordering of left vs right',
                      'Z': 'set if equal',
                      'X': 'the next unconsumed operator token'})
d.comment(0x9a9e, 'string: compare strings', align=Align.INLINE)
d.comment(0x9aa0, 'float: compare floats', align=Align.INLINE)
d.comment(0x9aa2, 'Stack the integer', align=Align.INLINE)
d.comment(0x9aa5, 'evaluate the next operand', align=Align.INLINE)
d.comment(0x9aa8, 'type', align=Align.INLINE)
d.comment(0x9aa9, 'string: Type mismatch', align=Align.INLINE)
d.comment(0x9aab, 'float: compare floats', align=Align.INLINE)

d.subroutine(
    0x9aad, 'iwa_test_var',
    title='Compare an integer variable with the accumulator',
    description='Signed 32-bit compare of the integer on top of the BASIC stack '
                'against IWA: bias both sign bits so an unsigned subtract orders '
                'signed values, then subtract, returning the ordering in C and Z '
                '(Z = equal).',
    on_entry={'(zp_stack_ptr) (&04/&05)': 'the stacked integer (left operand)',
              'zp_iwa (&2A-&2D)': 'the accumulator (right operand)'},
    on_exit={'C': 'set if stacked >= IWA', 'Z': 'set if equal',
             'zp_iwa (&2A-&2D)': 'corrupted (holds the difference)'},
)
# iwa_test_var (&9AAD): signed 32-bit compare of stacked int vs IWA.
# Flips the sign bits so an unsigned subtract orders signed values, then
# subtracts and returns the comparison in the C and Z flags (Z = equal).
d.comment(0x9aad, 'Flip the sign bit of the IWA top byte', align=Align.INLINE)
d.comment(0x9aaf, 'toggle bit 7 (bias to unsigned),', align=Align.INLINE)
d.comment(0x9ab1, 'store it back', align=Align.INLINE)
d.comment(0x9ab3, 'Subtract IWA from the stacked integer: byte 0',
          align=Align.INLINE)
d.comment(0x9ab4, 'from offset 0,', align=Align.INLINE)
d.comment(0x9ab6, 'stacked low byte,', align=Align.INLINE)
d.comment(0x9ab8, 'minus IWA low,', align=Align.INLINE)
d.comment(0x9aba, 'store the difference', align=Align.INLINE)
d.comment(0x9abc, 'byte 1', align=Align.INLINE)
d.comment(0x9abd, 'stacked byte 1,', align=Align.INLINE)
d.comment(0x9abf, 'minus IWA &2B,', align=Align.INLINE)
d.comment(0x9ac1, 'store it', align=Align.INLINE)
d.comment(0x9ac3, 'byte 2', align=Align.INLINE)
d.comment(0x9ac4, 'stacked byte 2,', align=Align.INLINE)
d.comment(0x9ac6, 'minus IWA &2C,', align=Align.INLINE)
d.comment(0x9ac8, 'store it', align=Align.INLINE)
d.comment(0x9aca, 'byte 3 (top)', align=Align.INLINE)
d.comment(0x9acb, 'stacked top byte,', align=Align.INLINE)
d.comment(0x9acd, 'reset Y (bytes done)', align=Align.INLINE)
d.comment(0x9acf, 'flip its sign bit too', align=Align.INLINE)
d.comment(0x9ad1, 'finish the signed subtract: sets C', align=Align.INLINE)
d.comment(0x9ad3, 'OR the low bytes...', align=Align.INLINE)
d.comment(0x9ad5, 'and &2B,', align=Align.INLINE)
d.comment(0x9ad7, '...to set Z when the values are equal', align=Align.INLINE)
d.comment(0x9ad9, 'Save the comparison flags', align=Align.INLINE)
d.comment(0x9ada, 'Drop the integer from the stack', align=Align.INLINE)
d.comment(0x9adb, '4 bytes,', align=Align.INLINE)
d.comment(0x9add, '+ stack pointer low,', align=Align.INLINE)
d.comment(0x9adf, 'store low,', align=Align.INLINE)
d.comment(0x9ae1, 'no carry into the high byte', align=Align.INLINE)
d.comment(0x9ae3, 'carry into the high byte', align=Align.INLINE)
d.comment(0x9ae5, 'Restore the flags', align=Align.INLINE)
# iwa_test_var + string compare
d.label(0x9ae5, 'itest_done')
d.comment(0x9ae6, 'Return', align=Align.INLINE)

d.comment(0x9ae7, 'String compare: stack the left', align=Align.INLINE)
d.label(0x9ae7, 'str_compare')
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
d.comment(0x9afe, 'stacked shorter: X = its length', align=Align.INLINE)
d.comment(0x9aff, 'shorter length', align=Align.INLINE)
d.label(0x9aff, 'strcmp_shorter')
d.comment(0x9b01, 'compare from 0', align=Align.INLINE)
# String comparison loop (&9B03).
d.comment(0x9b03, 'Reached the shorter length?', align=Align.INLINE)
d.label(0x9b03, 'strcmp_loop')
d.comment(0x9b05, 'yes: compare lengths', align=Align.INLINE)
d.comment(0x9b07, 'Next character', align=Align.INLINE)
d.comment(0x9b08, 'stacked string', align=Align.INLINE)
d.comment(0x9b0a, 'vs current string', align=Align.INLINE)
d.comment(0x9b0d, 'equal: continue', align=Align.INLINE)
d.comment(0x9b0f, 'differ', align=Align.INLINE)
d.comment(0x9b11, 'Compare the lengths', align=Align.INLINE)
d.label(0x9b11, 'strcmp_lengths')
d.comment(0x9b13, 'stacked length vs current', align=Align.INLINE)
d.comment(0x9b15, 'Save the result', align=Align.INLINE)
d.label(0x9b15, 'strcmp_result')

d.comment(0x9b16, 'Drop the stacked string', align=Align.INLINE)
d.comment(0x9b19, 'restore the saved pointer (X)', align=Align.INLINE)
d.comment(0x9b1b, 'Restore the result', align=Align.INLINE)
d.comment(0x9b1c, 'Return', align=Align.INLINE)

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
d.comment(0x9b1d, 'Start evaluating: copy PtrA to the working PtrB',
          align=Align.INLINE)
# eval_expr (&9B1D) remaining: copy PtrA to PtrB
d.comment(0x9b1f, 'PtrB low = PtrA', align=Align.INLINE)
d.comment(0x9b21, 'PtrA high...', align=Align.INLINE)
d.comment(0x9b23, '...to PtrB high', align=Align.INLINE)
d.comment(0x9b25, 'PtrA offset...', align=Align.INLINE)
d.comment(0x9b27, '...to PtrB offset', align=Align.INLINE)
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
    d.subroutine(_addr, _name, title=_title, description=_desc,
                 on_entry=EVAL_LEVEL_ON_ENTRY, on_exit=EVAL_LEVEL_ON_EXIT)

d.comment(0x9b29, 'Evaluate the higher-precedence (AND) operand first',
          align=Align.INLINE)
d.comment(0x9b2c, 'Is the next operator OR or EOR at this level?',
          align=Align.INLINE)
# eval_or_eor / eval_and (bitwise)
d.label(0x9b2c, 'eval_or_loop')
# eval_or_eor (&9B29): expression Level 7 - bitwise OR and EOR.
d.comment(0x9b2e, 'yes', align=Align.INLINE)
d.comment(0x9b30, 'EOR token?', align=Align.INLINE)
d.comment(0x9b32, 'yes', align=Align.INLINE)
d.comment(0x9b34, 'neither: back up over the token', align=Align.INLINE)
d.comment(0x9b36, 'set the result-type flags', align=Align.INLINE)
d.comment(0x9b37, 'store it', align=Align.INLINE)
d.comment(0x9b39, 'Return', align=Align.INLINE)
d.comment(0x9b3a, 'OR: stack the left operand, evaluate the right',
          align=Align.INLINE)
d.label(0x9b3a, 'do_or')
d.comment(0x9b3d, 'ensure the right operand is integer', align=Align.INLINE)
d.comment(0x9b3e, 'coerce it', align=Align.INLINE)
d.comment(0x9b41, 'Four bytes', align=Align.INLINE)
d.comment(0x9b43, 'stacked byte', align=Align.INLINE)
d.label(0x9b43, 'or_byte_loop')
d.comment(0x9b45, 'OR with IWA', align=Align.INLINE)
d.comment(0x9b48, 'store back', align=Align.INLINE)
d.comment(0x9b4b, 'next byte', align=Align.INLINE)
d.comment(0x9b4c, 'until all four OR-ed', align=Align.INLINE)
d.comment(0x9b4e, 'Drop the stacked operand', align=Align.INLINE)
d.label(0x9b4e, 'or_drop_stack')
d.comment(0x9b51, 'Result type = integer', align=Align.INLINE)
d.comment(0x9b53, 'Loop to handle any further OR / EOR', align=Align.INLINE)
d.comment(0x9b55, 'EOR: stack the left operand, evaluate the right',
          align=Align.INLINE)
d.label(0x9b55, 'do_eor')
d.comment(0x9b58, 'ensure the right operand is integer', align=Align.INLINE)
d.comment(0x9b59, 'coerce it', align=Align.INLINE)
d.comment(0x9b5c, 'Four bytes', align=Align.INLINE)
d.comment(0x9b5e, 'stacked byte', align=Align.INLINE)
d.label(0x9b5e, 'eor_byte_loop')
d.comment(0x9b60, 'EOR with IWA', align=Align.INLINE)
d.comment(0x9b63, 'store back', align=Align.INLINE)
d.comment(0x9b66, 'next byte', align=Align.INLINE)
d.comment(0x9b67, 'until all four EOR-ed', align=Align.INLINE)
d.comment(0x9b69, 'drop and loop', align=Align.INLINE)
# sub_c9b6b: coerce, stack, then evaluate the next operand.
d.comment(0x9b6b, 'Coerce the left operand to integer', align=Align.INLINE)
d.label(0x9b6b, 'coerce_left_int')
d.comment(0x9b6c, 'coerce it', align=Align.INLINE)
d.comment(0x9b6f, 'stack it', align=Align.INLINE)
# eval_and (&9B72): expression Level 6 - bitwise AND.
d.comment(0x9b72, 'Evaluate a relational operand', align=Align.INLINE)
d.comment(0x9b75, 'Apply AND only if the next operator is AND',
          align=Align.INLINE)
d.label(0x9b75, 'eval_and_loop')
d.comment(0x9b77, 'yes', align=Align.INLINE)
d.comment(0x9b79, 'no: return', align=Align.INLINE)
d.comment(0x9b7a, 'Coerce the left operand to integer', align=Align.INLINE)
d.label(0x9b7a, 'do_and')
d.comment(0x9b7b, 'coerce it', align=Align.INLINE)
d.comment(0x9b7e, 'stack it', align=Align.INLINE)
d.comment(0x9b81, 'evaluate the right operand', align=Align.INLINE)
d.comment(0x9b84, 'ensure it is integer', align=Align.INLINE)
d.comment(0x9b85, 'coerce it', align=Align.INLINE)
d.comment(0x9b88, 'Four bytes', align=Align.INLINE)
d.comment(0x9b8a, 'stacked byte', align=Align.INLINE)
d.label(0x9b8a, 'and_byte_loop')
d.comment(0x9b8c, 'AND with IWA', align=Align.INLINE)
d.comment(0x9b8f, 'store back', align=Align.INLINE)
d.comment(0x9b92, 'next byte', align=Align.INLINE)
d.comment(0x9b93, 'until all four AND-ed', align=Align.INLINE)
d.comment(0x9b95, 'Drop the stacked operand', align=Align.INLINE)
d.comment(0x9b98, 'Result type = integer', align=Align.INLINE)
d.comment(0x9b9a, 'loop for further AND', align=Align.INLINE)

# ----------------------------------------------------------------------
# eval_relational (&9B9C): expression Level 5 - comparisons.
# Evaluates a + - operand, then if the next token is a relational
# operator (< = >) parses the full operator (<, <=, <>, =, >, >=),
# compares the two operands and returns -1 (TRUE) or 0 (FALSE) as an
# integer.
# ----------------------------------------------------------------------
d.comment(0x9b9c, 'Evaluate a + - operand', align=Align.INLINE)
d.comment(0x9b9f, "next token past '>'?", align=Align.INLINE)
d.char_literal(0x9ba0)
d.comment(0x9ba1, 'yes: not a comparison, return', align=Align.INLINE)
d.comment(0x9ba3, "before '<'?", align=Align.INLINE)
d.char_literal(0x9ba4)
d.comment(0x9ba5, 'a relational operator: handle it', align=Align.INLINE)
d.comment(0x9ba7, 'not a comparison: return', align=Align.INLINE)
d.comment(0x9ba8, "'<' family?", align=Align.INLINE)
# eval_relational
d.label(0x9ba8, 'rel_lt_family')
d.comment(0x9baa, "'>' family?", align=Align.INLINE)
d.char_literal(0x9bab)
d.comment(0x9bac, 'yes', align=Align.INLINE)
d.comment(0x9bae, "'=': compare for equality", align=Align.INLINE)
d.comment(0x9baf, 'evaluate the right operand and compare', align=Align.INLINE)
d.comment(0x9bb2, 'not equal: result FALSE (0)', align=Align.INLINE)
d.comment(0x9bb4, 'equal: result TRUE (Y = &FF)', align=Align.INLINE)
d.label(0x9bb4, 'rel_true')
d.comment(0x9bb5, 'Store 0/-1 in all four IWA bytes', align=Align.INLINE)
d.label(0x9bb5, 'store_bool')
d.comment(0x9bb7, 'byte 1,', align=Align.INLINE)
d.comment(0x9bb9, 'byte 2,', align=Align.INLINE)
d.comment(0x9bbb, 'byte 3', align=Align.INLINE)
d.comment(0x9bbd, 'Result type = integer', align=Align.INLINE)
d.comment(0x9bbf, 'Return', align=Align.INLINE)
d.comment(0x9bc0, "'<' family: discard the operator", align=Align.INLINE)
d.label(0x9bc0, 'rel_lt')
d.comment(0x9bc1, 'Peek at the next source character', align=Align.INLINE)
d.comment(0x9bc3, 'read it', align=Align.INLINE)
d.comment(0x9bc5, "'='?  (<=)", align=Align.INLINE)
d.char_literal(0x9bc6)
d.comment(0x9bc7, 'yes', align=Align.INLINE)
d.comment(0x9bc9, "'>'?  (<>)", align=Align.INLINE)
d.char_literal(0x9bca)
d.comment(0x9bcb, 'yes', align=Align.INLINE)
d.comment(0x9bcd, 'plain "<": evaluate and compare', align=Align.INLINE)
d.comment(0x9bd0, 'less: TRUE', align=Align.INLINE)
d.comment(0x9bd2, 'not less: FALSE', align=Align.INLINE)
d.comment(0x9bd4, "'<=': step past the '='", align=Align.INLINE)
d.label(0x9bd4, 'rel_le')
d.comment(0x9bd6, 'evaluate and compare', align=Align.INLINE)
d.comment(0x9bd9, 'equal: TRUE', align=Align.INLINE)
d.comment(0x9bdb, 'less: TRUE', align=Align.INLINE)
d.comment(0x9bdd, 'greater: FALSE', align=Align.INLINE)
d.comment(0x9bdf, "'<>': step past the '>'", align=Align.INLINE)
d.label(0x9bdf, 'rel_ne')
d.comment(0x9be1, 'evaluate and compare', align=Align.INLINE)
d.comment(0x9be4, 'unequal: TRUE', align=Align.INLINE)
d.comment(0x9be6, 'equal: FALSE', align=Align.INLINE)
d.comment(0x9be8, "'>' family: discard the operator", align=Align.INLINE)
d.label(0x9be8, 'rel_gt')
d.comment(0x9be9, 'Peek at the next source character', align=Align.INLINE)
d.comment(0x9beb, 'read it', align=Align.INLINE)
d.comment(0x9bed, "'='?  (>=)", align=Align.INLINE)
d.char_literal(0x9bee)
d.comment(0x9bef, 'yes', align=Align.INLINE)
d.comment(0x9bf1, 'plain ">": evaluate and compare', align=Align.INLINE)
d.comment(0x9bf4, 'equal: FALSE', align=Align.INLINE)
d.comment(0x9bf6, 'greater: TRUE', align=Align.INLINE)
d.comment(0x9bf8, 'less: FALSE', align=Align.INLINE)
d.comment(0x9bfa, "'>=': step past the '='", align=Align.INLINE)
d.label(0x9bfa, 'rel_ge')
d.comment(0x9bfc, 'evaluate and compare', align=Align.INLINE)
d.comment(0x9bff, 'greater or equal: TRUE', align=Align.INLINE)
d.comment(0x9c01, 'less: FALSE', align=Align.INLINE)

d.comment(0x9c03, 'String too long error', align=Align.INLINE)
d.label(0x9c03, 'string_too_long')
# String concatenation (&9C15): str + str.
d.comment(0x9c15, 'Stack the left string', align=Align.INLINE)
d.label(0x9c15, 'relstr_stack_loop')
d.comment(0x9c18, 'Evaluate the right operand', align=Align.INLINE)
d.comment(0x9c1b, 'type', align=Align.INLINE)
d.comment(0x9c1c, 'number: Type mismatch', align=Align.INLINE)
d.comment(0x9c1e, 'New length = left + right', align=Align.INLINE)
d.comment(0x9c1f, 'save the pending operator (X)', align=Align.INLINE)
d.comment(0x9c21, 'index the stacked left length', align=Align.INLINE)
d.comment(0x9c23, 'left length', align=Align.INLINE)
d.comment(0x9c25, 'plus the right length', align=Align.INLINE)
d.comment(0x9c27, 'over 255: error', align=Align.INLINE)
d.comment(0x9c29, 'Save the new length', align=Align.INLINE)
d.comment(0x9c2a, 'keep it on the stack', align=Align.INLINE)
d.comment(0x9c2b, 'Move the right string up', align=Align.INLINE)
d.comment(0x9c2d, 'right string byte (at Y)', align=Align.INLINE)
d.label(0x9c2d, 'relstr_cmp_loop')
d.comment(0x9c30, 'to the new tail (at X)', align=Align.INLINE)
d.comment(0x9c33, 'back one destination', align=Align.INLINE)
d.comment(0x9c34, 'back one source', align=Align.INLINE)
d.comment(0x9c35, 'loop', align=Align.INLINE)
d.comment(0x9c37, 'Prepend the left string', align=Align.INLINE)
d.comment(0x9c3a, 'Set the new length', align=Align.INLINE)
d.comment(0x9c3b, 'store it', align=Align.INLINE)
d.comment(0x9c3d, 'restore the pending operator', align=Align.INLINE)
d.comment(0x9c3f, 'string result', align=Align.INLINE)
d.comment(0x9c40, 'loop for further + or -', align=Align.INLINE)

# ----------------------------------------------------------------------
# eval_add_sub (&9C42): expression Level 4 - binary + and -.
# Evaluates a higher-precedence (* / DIV MOD) operand, then while the
# next token is + or - combines it with another such operand. Each
# operand may be integer, real or string; the arms below convert to a
# common type (string concat for +, numeric otherwise).
# ----------------------------------------------------------------------
d.comment(0x9c42, 'Evaluate a * / DIV MOD operand', align=Align.INLINE)
d.comment(0x9c45, 'Apply + or - if that is the next operator',
          align=Align.INLINE)
d.char_literal(0x9c46)

# eval_add_sub
d.label(0x9c45, 'addsub_check')
d.comment(0x9c47, 'yes: addition', align=Align.INLINE)
d.comment(0x9c49, 'next operator "-"?', align=Align.INLINE)
d.char_literal(0x9c4a)
d.comment(0x9c4b, 'yes: subtraction', align=Align.INLINE)
d.comment(0x9c4d, 'neither: expression complete', align=Align.INLINE)
d.comment(0x9c4e, 'Addition: type of the left operand', align=Align.INLINE)
d.label(0x9c4e, 'do_add')

d.comment(0x9c4f, 'string: concatenate', align=Align.INLINE)
d.comment(0x9c51, 'real: handle as float add', align=Align.INLINE)
d.comment(0x9c53, 'integer: stack it and evaluate the right operand',
          align=Align.INLINE)
d.comment(0x9c56, 'Type of the right operand', align=Align.INLINE)
d.comment(0x9c57, 'string: Type mismatch', align=Align.INLINE)
d.comment(0x9c59, 'real: convert the left integer to float', align=Align.INLINE)
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
# iwa_add (&9C5B): integer + integer, 32-bit, operand on the stack.
d.comment(0x9c5b, 'int + int: add the 32-bit stacked value to IWA',
          align=Align.INLINE)
d.comment(0x9c5d, '...byte 0', align=Align.INLINE)
d.comment(0x9c5e, 'stacked low,', align=Align.INLINE)
d.comment(0x9c60, '+ IWA low,', align=Align.INLINE)
d.comment(0x9c62, 'store,', align=Align.INLINE)
d.comment(0x9c64, '...byte 1', align=Align.INLINE)
d.comment(0x9c65, 'stacked,', align=Align.INLINE)
d.comment(0x9c67, '+ IWA &2B,', align=Align.INLINE)
d.comment(0x9c69, 'store,', align=Align.INLINE)
d.comment(0x9c6b, '...byte 2', align=Align.INLINE)
d.comment(0x9c6c, 'stacked,', align=Align.INLINE)
d.comment(0x9c6e, '+ IWA &2C,', align=Align.INLINE)
d.comment(0x9c70, 'store,', align=Align.INLINE)
d.comment(0x9c72, '...byte 3', align=Align.INLINE)
d.comment(0x9c73, 'stacked,', align=Align.INLINE)
d.comment(0x9c75, '+ IWA &2D (high)', align=Align.INLINE)
d.comment(0x9c77, 'store the high byte', align=Align.INLINE)
# iwa_add (+ operator with type coercion)
d.label(0x9c77, 'iadd_store_drop')
d.comment(0x9c79, 'Drop the operand (stack += 4),', align=Align.INLINE)
d.comment(0x9c7a, 'low byte,', align=Align.INLINE)
d.comment(0x9c7c, '+ 4,', align=Align.INLINE)
d.comment(0x9c7e, 'store low,', align=Align.INLINE)
d.comment(0x9c80, 'Result type = integer', align=Align.INLINE)
d.comment(0x9c82, 'loop for further + or -', align=Align.INLINE)
d.comment(0x9c84, 'carry into the high byte,', align=Align.INLINE)
d.comment(0x9c86, 'back for a further + or -', align=Align.INLINE)
d.comment(0x9c88, 'Type mismatch error', align=Align.INLINE)
d.label(0x9c88, 'arith_type_error')
d.comment(0x9c8b, 'Left real: stack it, evaluate the right operand',
          align=Align.INLINE)
d.label(0x9c8b, 'add_real_left')
d.comment(0x9c8e, 'evaluate the right operand', align=Align.INLINE)
d.comment(0x9c91, 'Type of the right operand', align=Align.INLINE)
d.comment(0x9c92, 'string: Type mismatch', align=Align.INLINE)
d.comment(0x9c94, 'remember it for later', align=Align.INLINE)
d.comment(0x9c96, 'real: no conversion needed', align=Align.INLINE)
d.comment(0x9c98, 'integer: convert the right operand to float',
          align=Align.INLINE)
d.comment(0x9c9b, 'Pop the stacked real as the fp operand', align=Align.INLINE)
d.label(0x9c9b, 'add_floats')
d.comment(0x9c9e, 'FWA = left + right', align=Align.INLINE)
d.comment(0x9ca1, 'Restore the next character', align=Align.INLINE)
d.label(0x9ca1, 'arith_result_loop')
d.comment(0x9ca3, 'Result type = real', align=Align.INLINE)
d.comment(0x9ca5, 'loop for further + or -', align=Align.INLINE)
d.comment(0x9ca7, 'Left int, right real: save the operator', align=Align.INLINE)
d.label(0x9ca7, 'add_int_real')
d.comment(0x9ca9, 'pop the stacked left integer', align=Align.INLINE)
d.comment(0x9cac, 'stack the right real', align=Align.INLINE)
d.comment(0x9caf, 'convert the left integer to float', align=Align.INLINE)
d.comment(0x9cb2, 'then do float + float', align=Align.INLINE)
d.comment(0x9cb5, 'Subtraction: type of the left operand', align=Align.INLINE)
d.label(0x9cb5, 'sub_dispatch')
d.comment(0x9cb6, 'string: Type mismatch', align=Align.INLINE)
d.comment(0x9cb8, 'real: handle as float subtract', align=Align.INLINE)
d.comment(0x9cba, 'integer: stack it, evaluate the right operand',
          align=Align.INLINE)
d.comment(0x9cbd, 'Type of the right operand', align=Align.INLINE)
d.comment(0x9cbe, 'string: Type mismatch', align=Align.INLINE)
d.comment(0x9cc0, 'real: convert and subtract as floats', align=Align.INLINE)
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
# iwa_rsub (&9CC2): integer - integer (stacked - IWA), 32-bit.
d.comment(0x9cc2, 'int - int: stacked value minus IWA, byte 0',
          align=Align.INLINE)
d.comment(0x9cc3, 'from offset 0,', align=Align.INLINE)
d.comment(0x9cc5, 'stacked low,', align=Align.INLINE)
d.comment(0x9cc7, '- IWA low,', align=Align.INLINE)
d.comment(0x9cc9, 'store,', align=Align.INLINE)
d.comment(0x9ccb, '...byte 1', align=Align.INLINE)
d.comment(0x9ccc, 'stacked,', align=Align.INLINE)
d.comment(0x9cce, '- IWA &2B,', align=Align.INLINE)
d.comment(0x9cd0, 'store,', align=Align.INLINE)
d.comment(0x9cd2, '...byte 2', align=Align.INLINE)
d.comment(0x9cd3, 'stacked,', align=Align.INLINE)
d.comment(0x9cd5, '- IWA &2C,', align=Align.INLINE)
d.comment(0x9cd7, 'store,', align=Align.INLINE)
d.comment(0x9cd9, '...byte 3', align=Align.INLINE)
d.comment(0x9cda, 'stacked,', align=Align.INLINE)
d.comment(0x9cdc, '- IWA &2D (high)', align=Align.INLINE)
d.comment(0x9cde, 'store byte 3, drop the operand and loop', align=Align.INLINE)
d.comment(0x9ce1, 'Left real: stack it, evaluate the right operand',
          align=Align.INLINE)
# iwa_rsub (- operator) and the * / DIV MOD operand coercion
d.label(0x9ce1, 'sub_real_left')
d.comment(0x9ce4, 'evaluate the right operand', align=Align.INLINE)
d.comment(0x9ce7, 'Type of the right operand', align=Align.INLINE)
d.comment(0x9ce8, 'string: Type mismatch', align=Align.INLINE)
d.comment(0x9cea, 'remember it', align=Align.INLINE)
d.comment(0x9cec, 'real: no conversion needed', align=Align.INLINE)
d.comment(0x9cee, 'integer: convert the right operand to float',
          align=Align.INLINE)
d.comment(0x9cf1, 'Pop the stacked real as the fp operand', align=Align.INLINE)
d.label(0x9cf1, 'sub_floats')
d.comment(0x9cf4, 'FWA = left - right', align=Align.INLINE)
d.comment(0x9cf7, 'set result type and loop', align=Align.INLINE)
d.comment(0x9cfa, 'Left int, right real: save the operator', align=Align.INLINE)
d.label(0x9cfa, 'sub_int_real')
d.comment(0x9cfc, 'pop the stacked left integer', align=Align.INLINE)
d.comment(0x9cff, 'stack the right real', align=Align.INLINE)
d.comment(0x9d02, 'convert the left integer to float', align=Align.INLINE)
d.comment(0x9d05, 'pop the stacked right real', align=Align.INLINE)
d.comment(0x9d08, 'FWA = left - right', align=Align.INLINE)
d.comment(0x9d0b, 'set result type and loop', align=Align.INLINE)

# Multiply-level (eval_mul_div) float-coercion tails (&9D0E).
d.comment(0x9d0e, 'Convert the right integer to float', align=Align.INLINE)
d.label(0x9d0e, 'mul_conv_right')
d.comment(0x9d11, 'Pop the stacked left integer', align=Align.INLINE)
d.label(0x9d11, 'mul_conv_both')
d.comment(0x9d14, 'stack the right real', align=Align.INLINE)
d.comment(0x9d17, 'convert the left integer to float', align=Align.INLINE)
d.comment(0x9d1a, 'then do float * float', align=Align.INLINE)
d.comment(0x9d1d, 'Convert the left integer to float', align=Align.INLINE)
d.label(0x9d1d, 'mul_conv_left')
d.comment(0x9d20, 'Stack the left real', align=Align.INLINE)
d.label(0x9d20, 'mul_real_left')
d.comment(0x9d23, 'evaluate the next (^ level) operand', align=Align.INLINE)
d.comment(0x9d26, 'remember the operand type', align=Align.INLINE)
d.comment(0x9d28, 'test the operand type', align=Align.INLINE)
d.comment(0x9d29, 'ensure the operand is real', align=Align.INLINE)
d.comment(0x9d2c, 'Pop the stacked left real', align=Align.INLINE)
d.label(0x9d2c, 'mul_floats')
d.comment(0x9d2f, 'FWA = left * right', align=Align.INLINE)

# Level-3 multiply (&9D32): real result tail, then the integer path.
d.comment(0x9d32, 'real result', align=Align.INLINE)
d.comment(0x9d34, 'restore the operator', align=Align.INLINE)
d.comment(0x9d36, 'loop for further * / DIV MOD', align=Align.INLINE)
d.comment(0x9d39, 'String operand: Type mismatch', align=Align.INLINE)
d.label(0x9d39, 'mul_type_error')
d.comment(0x9d3c, 'Left operand type', align=Align.INLINE)
d.label(0x9d3c, 'mul_dispatch')
d.comment(0x9d3d, 'string: Type mismatch', align=Align.INLINE)
d.comment(0x9d3f, 'real: floating-point multiply', align=Align.INLINE)
d.comment(0x9d41, 'Integer: does it fit signed 16 bits?', align=Align.INLINE)
d.comment(0x9d43, 'byte 3 == byte 2 (sign-extended)?', align=Align.INLINE)
d.comment(0x9d45, 'no: floating-point multiply', align=Align.INLINE)
d.comment(0x9d47, 'high word zero (positive)?', align=Align.INLINE)
d.comment(0x9d48, 'yes', align=Align.INLINE)
d.comment(0x9d4a, 'high word all ones (negative)?', align=Align.INLINE)
d.comment(0x9d4c, 'no: floating-point multiply', align=Align.INLINE)
d.comment(0x9d4e, 'sign consistent with bit 15?', align=Align.INLINE)
d.label(0x9d4e, 'mul_right_signed')
d.comment(0x9d50, 'no: floating-point multiply', align=Align.INLINE)
d.comment(0x9d52, 'Stack it, evaluate the right operand', align=Align.INLINE)
d.comment(0x9d55, 'remember the operator', align=Align.INLINE)
d.comment(0x9d57, 'right operand type', align=Align.INLINE)
d.comment(0x9d58, 'string: Type mismatch', align=Align.INLINE)
d.comment(0x9d5a, 'real: floating-point multiply', align=Align.INLINE)
d.comment(0x9d5c, 'fits signed 16 bits?', align=Align.INLINE)
d.comment(0x9d5e, 'byte 3 == byte 2 (sign-extended)?', align=Align.INLINE)
d.comment(0x9d60, 'no: floating-point multiply', align=Align.INLINE)
d.comment(0x9d62, 'positive?', align=Align.INLINE)
d.comment(0x9d63, 'yes', align=Align.INLINE)
d.comment(0x9d65, 'negative?', align=Align.INLINE)
d.comment(0x9d67, 'no: floating-point multiply', align=Align.INLINE)
d.comment(0x9d69, 'sign consistent?', align=Align.INLINE)
d.label(0x9d69, 'mul_left_signed')
d.comment(0x9d6b, 'no: floating-point multiply', align=Align.INLINE)
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
# iwa_mul (&9D6D): 32-bit signed integer multiply
d.comment(0x9d6d, 'Save the right operand sign', align=Align.INLINE)
d.comment(0x9d6f, 'push it', align=Align.INLINE)
d.comment(0x9d70, 'take |right|', align=Align.INLINE)
d.comment(0x9d73, 'save it (via &39)', align=Align.INLINE)
d.comment(0x9d75, 'store it as the multiplier', align=Align.INLINE)
d.comment(0x9d78, 'unstack the left operand', align=Align.INLINE)
d.comment(0x9d7b, 'recover the right operand sign', align=Align.INLINE)
d.comment(0x9d7c, 'product sign = sign XOR sign', align=Align.INLINE)
d.comment(0x9d7e, '(save it)', align=Align.INLINE)
d.comment(0x9d80, 'take |left|', align=Align.INLINE)
d.comment(0x9d83, 'Clear the running product:', align=Align.INLINE)
d.comment(0x9d85, 'byte 1 (in X),', align=Align.INLINE)
d.comment(0x9d87, 'byte 2,', align=Align.INLINE)
d.comment(0x9d89, 'and byte 3', align=Align.INLINE)
d.comment(0x9d8b, 'Shift the multiplier right: next bit', align=Align.INLINE)
# iwa_mul (16-bit integer multiply)
d.label(0x9d8b, 'iwamul_loop')
d.comment(0x9d8d, 'low byte; bit 0 -> carry', align=Align.INLINE)
d.comment(0x9d8f, 'bit clear: skip the add', align=Align.INLINE)
d.comment(0x9d91, 'bit set: add the multiplicand', align=Align.INLINE)
d.comment(0x9d92, 'byte 0', align=Align.INLINE)
d.comment(0x9d93, '+ multiplicand byte 0,', align=Align.INLINE)
d.comment(0x9d95, 'back to product byte 0', align=Align.INLINE)
d.comment(0x9d96, 'byte 1', align=Align.INLINE)
d.comment(0x9d97, '+ byte 1,', align=Align.INLINE)
d.comment(0x9d99, 'back to product byte 1', align=Align.INLINE)
d.comment(0x9d9a, 'byte 2', align=Align.INLINE)
d.comment(0x9d9c, '+ byte 2,', align=Align.INLINE)
d.comment(0x9d9e, 'back to product byte 2', align=Align.INLINE)
d.comment(0x9da0, 'byte 3', align=Align.INLINE)
d.comment(0x9da2, '+ byte 3,', align=Align.INLINE)
d.comment(0x9da4, 'back to product byte 3', align=Align.INLINE)
d.comment(0x9da6, 'Shift the multiplicand left', align=Align.INLINE)
d.label(0x9da6, 'iwamul_double')
d.comment(0x9da8, 'byte 1,', align=Align.INLINE)
d.comment(0x9daa, 'byte 2,', align=Align.INLINE)
d.comment(0x9dac, 'byte 3 (multiplicand now x2)', align=Align.INLINE)
d.comment(0x9dae, 'more multiplier bits?', align=Align.INLINE)
d.comment(0x9db0, 'OR in the high byte', align=Align.INLINE)
d.comment(0x9db2, 'loop', align=Align.INLINE)
d.comment(0x9db4, 'store the product (low 2 bytes)', align=Align.INLINE)
d.comment(0x9db6, 'and byte 1 (bytes 2-3 already in place)', align=Align.INLINE)
d.comment(0x9db8, 'product sign', align=Align.INLINE)
d.comment(0x9dba, 'save its N flag', align=Align.INLINE)
d.comment(0x9dbb, 'load the product into IWA', align=Align.INLINE)
d.label(0x9dbb, 'iwamul_result')
d.comment(0x9dbd, 'copy &3D..&40 into IWA', align=Align.INLINE)
d.label(0x9dbd, 'iwamul_copy')
d.comment(0x9dc0, 'Apply the sign', align=Align.INLINE)
d.comment(0x9dc1, 'positive: done', align=Align.INLINE)
d.comment(0x9dc3, 'negative: negate the product', align=Align.INLINE)
d.comment(0x9dc6, 'restore the operator', align=Align.INLINE)
d.label(0x9dc6, 'iwamul_restore_op')
d.comment(0x9dc8, 'loop for further * / DIV MOD', align=Align.INLINE)
d.comment(0x9dcb, 'bounce back to the multiply code', align=Align.INLINE)
d.label(0x9dcb, 'iwamul_bounce')
d.comment(0x9dce, 'stack the operand, then multiply', align=Align.INLINE)

d.subroutine(
    0x9dce, 'mul_stack_eval',
    title='Stack the integer, then evaluate a * / DIV / MOD expression',
    description="""Push the pending integer accumulator onto the arithmetic stack via
stack_integer, then fall into eval_mul_div to evaluate the higher-precedence (^) operand and apply any * / DIV / MOD operators. A
trampoline used when the caller already holds an integer that must be
preserved across the multiply-level evaluation.
""",
    on_entry={
        'zp_iwa (&2A)': 'integer value to push onto the stack',
        'zp_text_ptr2 (&19/&1A)': 'PtrB at the expression to evaluate',
        'zp_text_ptr2_off (&1B)': 'offset into the text',
    },
    on_exit={
        'A': 'result type (<0 float in fwa, >0 integer in iwa, 0 string)',
        'zp_iwa (&2A) / zp_fwa (&2E) / string_work (&0600)': 'the value, selected by the type',
        'X': 'the next unconsumed operator token',
        'zp_text_ptr2_off (&1B)': 'advanced past the consumed text',
    },
)
d.comment(0x9dd1, 'Evaluate the higher level (^, level 2) operand', align=Align.INLINE)
d.comment(0x9dd4, 'next operator "*"?', align=Align.INLINE)
d.char_literal(0x9dd5)
# eval_mul_div / iwa_div
d.label(0x9dd4, 'muldiv_check')
d.comment(0x9dd6, 'yes: multiply', align=Align.INLINE)
d.comment(0x9dd8, '"/"?', align=Align.INLINE)
d.char_literal(0x9dd9)
d.comment(0x9dda, 'yes: divide', align=Align.INLINE)
d.comment(0x9ddc, 'MOD token?', align=Align.INLINE)
d.comment(0x9dde, 'yes: integer remainder', align=Align.INLINE)
d.comment(0x9de0, 'DIV token?', align=Align.INLINE)
d.comment(0x9de2, 'yes: integer divide', align=Align.INLINE)
d.comment(0x9de4, 'no operator: return', align=Align.INLINE)
d.comment(0x9de5, 'Divide: ensure the left operand is real', align=Align.INLINE)
d.label(0x9de5, 'do_divide')
d.comment(0x9de6, 'convert if integer', align=Align.INLINE)
d.comment(0x9de9, 'stack it', align=Align.INLINE)
d.comment(0x9dec, 'evaluate the right operand', align=Align.INLINE)
d.comment(0x9def, 'remember the operator', align=Align.INLINE)
d.comment(0x9df1, 'ensure the right operand is real', align=Align.INLINE)
d.comment(0x9df2, 'convert if integer', align=Align.INLINE)
d.comment(0x9df5, 'pop the left operand as the fp operand', align=Align.INLINE)
d.comment(0x9df8, 'FWA = left / right', align=Align.INLINE)
d.comment(0x9dfb, 'restore the operator', align=Align.INLINE)
d.comment(0x9dfd, 'real result', align=Align.INLINE)
d.comment(0x9dff, 'loop for further * / DIV MOD', align=Align.INLINE)

d.subroutine(
    0x9e01, 'iwa_mod',
    title='Integer remainder',
    description="""IWA = IWA MOD the integer operand. Raises "Division by
zero" if the divisor is zero.""",
    on_entry={'zp_iwa (&2A)': 'the dividend'},
    on_exit={'zp_iwa': 'the remainder'},
)
# iwa_mod (&9E01): IWA = IWA MOD operand (shares the DIV/MOD core)
d.comment(0x9e01, 'MOD: divide', align=Align.INLINE)
d.comment(0x9e04, 'remainder takes the dividend sign', align=Align.INLINE)
d.comment(0x9e06, 'save the sign', align=Align.INLINE)
d.comment(0x9e07, 'load the remainder (&3D-&40) and apply the sign', align=Align.INLINE)

d.subroutine(
    0x9e0a, 'iwa_div',
    title='Integer divide',
    description="""IWA = IWA DIV the integer operand. Raises "Division by
zero" if the divisor is zero.""",
    on_entry={'zp_iwa (&2A)': 'the dividend'},
    on_exit={'zp_iwa': 'the quotient'},
)
# iwa_mod (&9E01) and iwa_div (&9E0A).
d.comment(0x9e0a, 'DIV: divide', align=Align.INLINE)
d.comment(0x9e0d, 'Shift the quotient up by one', align=Align.INLINE)
d.comment(0x9e0f, 'through &3A,', align=Align.INLINE)
d.comment(0x9e11, '&3B,', align=Align.INLINE)
d.comment(0x9e13, '&3C', align=Align.INLINE)
d.comment(0x9e15, 'quotient sign', align=Align.INLINE)
d.comment(0x9e17, 'save the sign flags', align=Align.INLINE)
d.comment(0x9e18, 'load the quotient (&39-&3C)', align=Align.INLINE)
d.comment(0x9e1a, '...and apply the sign', align=Align.INLINE)
d.comment(0x9e1d, 'Stack the integer, evaluate the next ^ operand',
          align=Align.INLINE)

d.subroutine(
    0x9e1d, 'pow_stack_eval',
    title='Stack the integer, then evaluate a ^ expression',
    description="""Push the pending integer accumulator onto the arithmetic stack via
stack_integer, then fall into eval_power to evaluate the next factor
and apply any ^ operators. A trampoline used when the caller already
holds an integer that must be preserved across the power-level
evaluation.
""",
    on_entry={
        'zp_iwa (&2A)': 'integer value to push onto the stack',
        'zp_text_ptr2 (&19/&1A)': 'PtrB at the expression to evaluate',
        'zp_text_ptr2_off (&1B)': 'offset into the text',
    },
    on_exit={
        'A': 'result type (<0 float in fwa, >0 integer in iwa, 0 string)',
        'zp_iwa (&2A) / zp_fwa (&2E) / string_work (&0600)': 'the value, selected by the type',
        'X': 'the next unconsumed operator token',
        'zp_text_ptr2_off (&1B)': 'advanced past the consumed text',
    },
)

d.subroutine(0x9e20, 'eval_power',
             title='Expression Level 2 - the ^ operator',
             description='Evaluate a factor, then for each ^ raise it to the '
                         'power: an integer exponent uses repeated '
                         'multiplication, otherwise x^y = x^int * exp(frac * '
                         'ln x).',
             on_entry=EVAL_LEVEL_ON_ENTRY, on_exit=EVAL_LEVEL_ON_EXIT)
# eval_power (&9E20): the ^ operator.
d.comment(0x9e20, 'Evaluate the base', align=Align.INLINE)
d.comment(0x9e23, 'Save the result type', align=Align.INLINE)
# eval_power
d.label(0x9e23, 'pow_result')
d.comment(0x9e24, 'Next character', align=Align.INLINE)
d.label(0x9e24, 'pow_op_loop')
d.comment(0x9e26, 'advance the offset', align=Align.INLINE)
d.comment(0x9e28, 'read it', align=Align.INLINE)
d.comment(0x9e2a, 'space?', align=Align.INLINE)
d.char_literal(0x9e2b)
d.comment(0x9e2c, 'skip it', align=Align.INLINE)
d.comment(0x9e2e, 'keep the operator', align=Align.INLINE)
d.comment(0x9e2f, 'restore the type', align=Align.INLINE)
d.comment(0x9e30, "'^'?", align=Align.INLINE)
d.char_literal(0x9e31)
d.comment(0x9e32, 'yes', align=Align.INLINE)
d.comment(0x9e34, 'no: return', align=Align.INLINE)
d.comment(0x9e35, 'Ensure the base is real', align=Align.INLINE)
d.label(0x9e35, 'pow_apply')
d.comment(0x9e36, 'convert if integer', align=Align.INLINE)
d.comment(0x9e39, 'stack the base', align=Align.INLINE)
d.comment(0x9e3c, 'evaluate the exponent as a real', align=Align.INLINE)
d.comment(0x9e3f, 'Exponent magnitude', align=Align.INLINE)
d.comment(0x9e41, 'large (>= 2^7)?', align=Align.INLINE)
d.comment(0x9e43, 'yes: use exp(y*ln x)', align=Align.INLINE)
d.comment(0x9e45, 'Split into integer and fractional parts', align=Align.INLINE)
d.comment(0x9e48, 'fractional part nonzero?', align=Align.INLINE)
d.comment(0x9e4a, 'no: integer power - unstack the base', align=Align.INLINE)
d.comment(0x9e4d, 'load it into FWA', align=Align.INLINE)
d.comment(0x9e50, 'integer exponent', align=Align.INLINE)
d.comment(0x9e52, 'FWA = base ^ int', align=Align.INLINE)
d.comment(0x9e55, 'real result', align=Align.INLINE)
d.comment(0x9e57, 'continue', align=Align.INLINE)
d.comment(0x9e59, 'Fractional exponent: save the fraction', align=Align.INLINE)
d.label(0x9e59, 'pow_frac')
d.comment(0x9e5c, 'point at the stacked base', align=Align.INLINE)
d.comment(0x9e5e, 'low byte', align=Align.INLINE)
d.comment(0x9e60, 'high byte', align=Align.INLINE)
d.comment(0x9e62, 'set the fp pointer', align=Align.INLINE)
d.comment(0x9e64, 'load the base', align=Align.INLINE)
d.comment(0x9e67, 'integer part of the exponent', align=Align.INLINE)
d.comment(0x9e69, 'FWA = base ^ int', align=Align.INLINE)
d.comment(0x9e6c, 'save base^int in TEMP2', align=Align.INLINE)
d.label(0x9e6c, 'pow_combine')
d.comment(0x9e6f, 'unstack the base', align=Align.INLINE)
d.comment(0x9e72, 'load it into FWA', align=Align.INLINE)
d.comment(0x9e75, 'ln(base)', align=Align.INLINE)
d.comment(0x9e78, 'times the fractional exponent', align=Align.INLINE)
d.comment(0x9e7b, 'exp(that) = base^frac', align=Align.INLINE)
d.comment(0x9e7e, 'point at base^int', align=Align.INLINE)
d.comment(0x9e81, 'FWA = base^int * base^frac', align=Align.INLINE)
d.comment(0x9e84, 'real result', align=Align.INLINE)
d.comment(0x9e86, 'continue', align=Align.INLINE)
d.comment(0x9e88, 'Large exponent: x^y = exp(y * ln x)', align=Align.INLINE)
d.label(0x9e88, 'pow_large')
d.comment(0x9e8b, 'base^int = 1 (no integer part)', align=Align.INLINE)
d.comment(0x9e8e, 'evaluate it', align=Align.INLINE)

# Hex conversion (&9E90): IWA/FWA -> hex string (PRINT~ / STR$~).
d.comment(0x9e90, 'Real?', align=Align.INLINE)
# hex string conversion (STR$~ / PRINT~) and number sign/normalise
d.label(0x9e90, 'hex_convert')
d.comment(0x9e91, 'no', align=Align.INLINE)
d.comment(0x9e93, 'convert to integer', align=Align.INLINE)
d.comment(0x9e96, 'Expand 4 bytes into 8 nibbles', align=Align.INLINE)
d.label(0x9e96, 'hex_expand')
d.comment(0x9e98, 'byte index = 0', align=Align.INLINE)
d.comment(0x9e9a, 'Byte', align=Align.INLINE)
d.label(0x9e9a, 'hex_expand_loop')
d.comment(0x9e9d, 'save it', align=Align.INLINE)
d.comment(0x9e9e, 'low nibble', align=Align.INLINE)
d.comment(0x9ea0, 'store it', align=Align.INLINE)
d.comment(0x9ea2, 'high nibble', align=Align.INLINE)
d.comment(0x9ea3, 'shift the high nibble down,', align=Align.INLINE)
d.comment(0x9ea4, '(continued)', align=Align.INLINE)
d.comment(0x9ea5, '(continued)', align=Align.INLINE)
d.comment(0x9ea6, '(continued)', align=Align.INLINE)
d.comment(0x9ea7, 'next nibble slot', align=Align.INLINE)
d.comment(0x9ea8, 'store it', align=Align.INLINE)
d.comment(0x9eaa, 'next nibble slot', align=Align.INLINE)
d.comment(0x9eab, 'next byte', align=Align.INLINE)
d.comment(0x9eac, 'all four bytes?', align=Align.INLINE)
d.comment(0x9eae, 'no: continue', align=Align.INLINE)
d.comment(0x9eb0, 'Skip leading zero nibbles', align=Align.INLINE)
d.label(0x9eb0, 'hex_skip_zeros')
d.comment(0x9eb1, 'all zero: output one zero', align=Align.INLINE)
d.comment(0x9eb3, 'this nibble zero?', align=Align.INLINE)
d.comment(0x9eb5, 'yes: skip it', align=Align.INLINE)
d.comment(0x9eb7, 'Next nibble', align=Align.INLINE)
d.label(0x9eb7, 'hex_digit_loop')
d.comment(0x9eb9, 'above 9?', align=Align.INLINE)
d.comment(0x9ebb, 'no', align=Align.INLINE)
d.comment(0x9ebd, 'adjust for A-F', align=Align.INLINE)
d.comment(0x9ebf, 'to ASCII', align=Align.INLINE)
d.char_literal(0x9ec0)
d.label(0x9ebf, 'hex_to_ascii')
d.comment(0x9ec1, 'output the digit', align=Align.INLINE)
d.comment(0x9ec4, 'next', align=Align.INLINE)
d.comment(0x9ec5, 'loop', align=Align.INLINE)
d.comment(0x9ec7, 'Return', align=Align.INLINE)

d.comment(0x9ec8, 'positive?', align=Align.INLINE)
d.label(0x9ec8, 'num_sign')
d.comment(0x9eca, "negative: output '-'", align=Align.INLINE)
d.char_literal(0x9ecb)
d.comment(0x9ecc, 'also clears the sign bit (bit 7 = 0)', align=Align.INLINE)
d.comment(0x9ece, 'print it', align=Align.INLINE)
d.comment(0x9ed1, 'Exponent', align=Align.INLINE)
d.label(0x9ed1, 'num_normalize_loop')

d.comment(0x9ed3, '>= 1?', align=Align.INLINE)
d.comment(0x9ed5, 'yes: output the integer part', align=Align.INLINE)
d.comment(0x9ed7, '< 1: multiply by 10', align=Align.INLINE)
d.comment(0x9eda, 'decrement the decimal exponent', align=Align.INLINE)
d.comment(0x9edc, 'loop', align=Align.INLINE)
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
# number_to_ascii (&9EDF): format the value into the SWA per @% / radix
d.comment(0x9edf, 'Get the @% format byte', align=Align.INLINE)
d.comment(0x9ee2, 'valid (< 3)?', align=Align.INLINE)
d.comment(0x9ee4, 'yes: use it', align=Align.INLINE)
d.comment(0x9ee6, 'invalid: use General format', align=Align.INLINE)
d.comment(0x9ee8, 'store the format type', align=Align.INLINE)
# number_to_ascii (float -> decimal string)
d.label(0x9ee8, 'nta_store_format')
d.comment(0x9eea, 'digit count from @%', align=Align.INLINE)
d.comment(0x9eed, 'zero: check the format', align=Align.INLINE)
d.comment(0x9eef, '>= 10 digits?', align=Align.INLINE)
d.comment(0x9ef1, 'yes: cap at 10', align=Align.INLINE)
d.comment(0x9ef3, 'use the specified count', align=Align.INLINE)
d.comment(0x9ef5, 'fixed format?', align=Align.INLINE)
d.label(0x9ef5, 'nta_check_fixed')
d.comment(0x9ef7, 'yes: zero digits', align=Align.INLINE)
d.comment(0x9ef9, 'default to 10 digits', align=Align.INLINE)
d.label(0x9ef9, 'nta_default_digits')
d.comment(0x9efb, 'store the digit count', align=Align.INLINE)
d.label(0x9efb, 'nta_store_count')
d.comment(0x9efd, '(copy)', align=Align.INLINE)
d.comment(0x9eff, 'output length = 0...', align=Align.INLINE)
d.comment(0x9f01, '(length = 0)', align=Align.INLINE)
d.comment(0x9f03, 'decimal exponent = 0 (&49)', align=Align.INLINE)
d.comment(0x9f05, 'hex mode (radix flag bit 7)?', align=Align.INLINE)
d.comment(0x9f07, 'yes: hex conversion', align=Align.INLINE)
d.comment(0x9f09, 'an integer value?', align=Align.INLINE)
d.comment(0x9f0a, 'already a real', align=Align.INLINE)
d.comment(0x9f0c, 'convert the integer to a real', align=Align.INLINE)
d.comment(0x9f0f, 'sign of the value', align=Align.INLINE)
d.label(0x9f0f, 'nta_sign')
d.comment(0x9f12, 'non-zero: format it', align=Align.INLINE)
d.comment(0x9f14, 'zero, not General format?', align=Align.INLINE)
d.comment(0x9f16, 'fixed/exponential zero', align=Align.INLINE)
d.comment(0x9f18, "output a single '0'", align=Align.INLINE)
d.char_literal(0x9f19)
d.comment(0x9f1a, '...and return', align=Align.INLINE)
d.comment(0x9f1d, 'output zero in fixed/exp format', align=Align.INLINE)
d.label(0x9f1d, 'nta_output_zero')
d.comment(0x9f20, 'FWA = 1.0', align=Align.INLINE)
d.label(0x9f20, 'nta_set_one')
d.comment(0x9f23, 'always taken (count a place)', align=Align.INLINE)
d.comment(0x9f25, 'exponent < 4 (value < 10)?', align=Align.INLINE)
d.label(0x9f25, 'nta_check_mag')
d.comment(0x9f27, 'yes: ready to convert', align=Align.INLINE)
d.comment(0x9f29, 'exponent != 4: too big, divide', align=Align.INLINE)
d.comment(0x9f2b, 'mantissa top byte', align=Align.INLINE)
d.comment(0x9f2d, 'less than &A0 (value < 10)?', align=Align.INLINE)
d.comment(0x9f2f, 'yes: ready to convert', align=Align.INLINE)
d.comment(0x9f31, 'FWA = FWA / 10', align=Align.INLINE)
d.label(0x9f31, 'nta_div10')
d.comment(0x9f34, 'count one decimal place up', align=Align.INLINE)
d.label(0x9f34, 'nta_count_up')
d.comment(0x9f36, 'check the magnitude again', align=Align.INLINE)
d.comment(0x9f39, 'Save FWA in TEMP1 (a fraction in [1,10)):', align=Align.INLINE)
d.label(0x9f39, 'nta_save_temp1')
d.comment(0x9f3b, 'stash the rounding byte,', align=Align.INLINE)
d.comment(0x9f3d, 'pack the mantissa', align=Align.INLINE)
d.comment(0x9f40, 'digit count', align=Align.INLINE)
d.comment(0x9f42, '(store)', align=Align.INLINE)
d.comment(0x9f44, 'print format', align=Align.INLINE)
d.comment(0x9f46, 'not fixed format?', align=Align.INLINE)
d.comment(0x9f48, 'do exponent/general', align=Align.INLINE)
d.comment(0x9f4a, 'fixed: digits + decimal exponent', align=Align.INLINE)
d.comment(0x9f4c, 'negative: round to zero', align=Align.INLINE)
d.comment(0x9f4e, '(store the digit count)', align=Align.INLINE)
d.comment(0x9f50, '> 10?', align=Align.INLINE)
d.comment(0x9f52, 'no', align=Align.INLINE)
d.comment(0x9f54, 'cap at 10', align=Align.INLINE)
d.comment(0x9f56, '(store)', align=Align.INLINE)
d.comment(0x9f58, 'switch to General', align=Align.INLINE)
d.comment(0x9f5a, '(store)', align=Align.INLINE)
d.comment(0x9f5c, 'Build a rounding constant 0.5e-n:', align=Align.INLINE)
d.label(0x9f5c, 'nta_round_const')
d.comment(0x9f5f, 'mantissa = &A0...', align=Align.INLINE)
d.comment(0x9f61, '(MSB)', align=Align.INLINE)
d.comment(0x9f63, 'exponent = &83 (0.5),', align=Align.INLINE)
d.comment(0x9f65, '(store)', align=Align.INLINE)
d.comment(0x9f67, 'shift it down by the digit count:', align=Align.INLINE)
d.comment(0x9f69, 'no shift needed', align=Align.INLINE)
d.comment(0x9f6b, 'rounding /= 10', align=Align.INLINE)
d.label(0x9f6b, 'nta_round_loop')
d.comment(0x9f6e, 'count', align=Align.INLINE)
d.comment(0x9f6f, 'loop', align=Align.INLINE)
d.comment(0x9f71, 'point at the saved value (TEMP1)', align=Align.INLINE)
d.label(0x9f71, 'nta_point_temp1')
d.comment(0x9f74, 'FWB = the value', align=Align.INLINE)
d.comment(0x9f77, 'the saved rnd byte...', align=Align.INLINE)
d.comment(0x9f79, '(into FWB)', align=Align.INLINE)
d.comment(0x9f7b, 'add the rounding constant', align=Align.INLINE)
d.comment(0x9f7e, 'Re-normalise to [1,10): exponent', align=Align.INLINE)
d.label(0x9f7e, 'nta_renorm_loop')
d.comment(0x9f80, '< 4?', align=Align.INLINE)
d.comment(0x9f82, 'in range', align=Align.INLINE)
d.comment(0x9f84, 'shift the mantissa right:', align=Align.INLINE)
d.comment(0x9f86, 'm2,', align=Align.INLINE)
d.comment(0x9f88, 'm3,', align=Align.INLINE)
d.comment(0x9f8a, 'm4,', align=Align.INLINE)
d.comment(0x9f8c, 'rnd', align=Align.INLINE)
d.comment(0x9f8e, 'and bump the exponent', align=Align.INLINE)
d.comment(0x9f90, 'loop', align=Align.INLINE)
d.comment(0x9f92, 'mantissa top byte', align=Align.INLINE)
d.label(0x9f92, 'nta_renorm_mant')
d.comment(0x9f94, '>= 10 after rounding?', align=Align.INLINE)
d.comment(0x9f96, 'yes: re-divide', align=Align.INLINE)
d.comment(0x9f98, 'digit count', align=Align.INLINE)
d.comment(0x9f9a, 'non-zero', align=Align.INLINE)
d.comment(0x9f9c, 'fixed format?', align=Align.INLINE)
d.label(0x9f9c, 'nta_check_fixed2')
d.comment(0x9f9e, 'output the value', align=Align.INLINE)
d.comment(0x9fa0, 'Clear FWA (zero / underflow):', align=Align.INLINE)
d.label(0x9fa0, 'nta_zero')
d.comment(0x9fa3, '0...', align=Align.INLINE)
d.comment(0x9fa5, 'decimal exponent = 0,', align=Align.INLINE)
d.comment(0x9fa7, 'original digit count...', align=Align.INLINE)
d.comment(0x9fa9, '(store)', align=Align.INLINE)
d.comment(0x9fab, 'plus one', align=Align.INLINE)
d.comment(0x9fad, 'General format?', align=Align.INLINE)
d.label(0x9fad, 'nta_check_general')
d.comment(0x9faf, 'is the format General (1)?', align=Align.INLINE)
d.comment(0x9fb1, 'output the value', align=Align.INLINE)
d.comment(0x9fb3, 'decimal exponent', align=Align.INLINE)
d.comment(0x9fb5, 'negative: leading zeros', align=Align.INLINE)
d.comment(0x9fb7, 'within the digit count?', align=Align.INLINE)
d.comment(0x9fb9, 'no: use E-notation', align=Align.INLINE)
d.comment(0x9fbb, 'within range: clear the exponent,', align=Align.INLINE)
d.comment(0x9fbd, '(store)', align=Align.INLINE)
d.comment(0x9fbf, 'one more digit', align=Align.INLINE)
d.comment(0x9fc0, 'output the value', align=Align.INLINE)
d.comment(0x9fc1, 'output the value', align=Align.INLINE)
d.comment(0x9fc3, 'fixed format?', align=Align.INLINE)
d.label(0x9fc3, 'nta_check_fixed3')
d.comment(0x9fc5, 'fixed format (2)?', align=Align.INLINE)
d.comment(0x9fc7, 'yes', align=Align.INLINE)
d.comment(0x9fc9, '(General marker)', align=Align.INLINE)
d.comment(0x9fcb, 'far below: use E-notation', align=Align.INLINE)
d.comment(0x9fcd, 'not far below: output', align=Align.INLINE)
d.comment(0x9fcf, "leading '0'", align=Align.INLINE)
d.char_literal(0x9fd0)
d.label(0x9fcf, 'nta_leading_zero')
d.comment(0x9fd1, 'emit it', align=Align.INLINE)
d.comment(0x9fd4, "decimal '.'", align=Align.INLINE)
d.char_literal(0x9fd5)
d.comment(0x9fd6, 'emit it', align=Align.INLINE)
d.comment(0x9fd9, "prepare '0'", align=Align.INLINE)
d.char_literal(0x9fda)
d.comment(0x9fdb, 'leading zeros for the fraction:', align=Align.INLINE)
d.label(0x9fdb, 'nta_frac_zeros_loop')
d.comment(0x9fdd, 'exponent reached 0: done', align=Align.INLINE)
d.comment(0x9fdf, 'output a zero', align=Align.INLINE)
d.comment(0x9fe2, 'loop', align=Align.INLINE)
d.comment(0x9fe4, 'all digits (no point yet)', align=Align.INLINE)
d.label(0x9fe4, 'nta_all_digits')
d.comment(0x9fe6, 'digit position counter', align=Align.INLINE)
d.label(0x9fe6, 'nta_digit_pos')
d.comment(0x9fe8, 'Emit each digit:', align=Align.INLINE)
d.label(0x9fe8, 'nta_emit_loop')
d.comment(0x9feb, 'at the decimal point?', align=Align.INLINE)
d.comment(0x9fed, 'no', align=Align.INLINE)
d.comment(0x9fef, "emit '.'", align=Align.INLINE)
d.char_literal(0x9ff0)
d.comment(0x9ff1, 'emit it', align=Align.INLINE)
d.comment(0x9ff4, 'more digits?', align=Align.INLINE)
d.label(0x9ff4, 'nta_more_digits')
d.comment(0x9ff6, 'loop', align=Align.INLINE)
d.comment(0x9ff8, 'General format: trim trailing zeros', align=Align.INLINE)
d.comment(0x9ffa, 'general 1 (E)?', align=Align.INLINE)
d.comment(0x9ffb, 'yes: go to the exponent', align=Align.INLINE)
d.comment(0x9ffd, 'general 2 (fixed)?', align=Align.INLINE)
d.comment(0x9ffe, 'fixed: skip trimming', align=Align.INLINE)
d.comment(0xa000, 'scan back from the end:', align=Align.INLINE)
d.comment(0xa002, 'previous char', align=Align.INLINE)
d.label(0xa002, 'nta_trim_loop')
d.comment(0xa003, 'a character', align=Align.INLINE)
d.comment(0xa006, "a '0'?", align=Align.INLINE)
d.char_literal(0xa007)
d.comment(0xa008, 'yes: trim it', align=Align.INLINE)
d.comment(0xa00a, "a '.'?", align=Align.INLINE)
d.char_literal(0xa00b)
d.comment(0xa00c, 'trim it too', align=Align.INLINE)
d.comment(0xa00e, 'keep this one', align=Align.INLINE)
d.comment(0xa00f, 'set the trimmed length', align=Align.INLINE)
d.label(0xa00f, 'nta_set_length')
d.comment(0xa011, 'a decimal exponent to print?', align=Align.INLINE)
d.label(0xa011, 'nta_check_exp')
d.comment(0xa013, 'no: done', align=Align.INLINE)
d.comment(0xa015, "output 'E'", align=Align.INLINE)
d.char_literal(0xa016)
d.label(0xa015, 'nta_output_e')
d.comment(0xa017, 'emit it', align=Align.INLINE)
d.comment(0xa01a, 'the exponent', align=Align.INLINE)
d.comment(0xa01c, 'positive', align=Align.INLINE)
d.comment(0xa01e, "negative: output '-'", align=Align.INLINE)
d.char_literal(0xa01f)
d.comment(0xa020, 'emit it', align=Align.INLINE)
d.comment(0xa023, 'negate the exponent', align=Align.INLINE)
d.comment(0xa024, '0...', align=Align.INLINE)
d.comment(0xa026, 'minus the exponent', align=Align.INLINE)
d.comment(0xa028, 'output the exponent in decimal', align=Align.INLINE)
d.label(0xa028, 'nta_output_exp')
d.comment(0xa02b, 'General format?', align=Align.INLINE)
d.comment(0xa02d, 'done', align=Align.INLINE)
d.comment(0xa02f, "pad: a space", align=Align.INLINE)
d.char_literal(0xa030)
d.comment(0xa031, 'check the exponent sign', align=Align.INLINE)
d.comment(0xa033, 'negative: no pad', align=Align.INLINE)
d.comment(0xa035, 'output it', align=Align.INLINE)
d.comment(0xa038, 'any field width left?', align=Align.INLINE)
d.label(0xa038, 'nta_field_pad')

d.comment(0xa03a, 'done', align=Align.INLINE)
d.comment(0xa03c, 'output a final space', align=Align.INLINE)
d.comment(0xa03f, 'Return', align=Align.INLINE)
d.subroutine(0xa040, 'output_top_digit', title='Output the leading decimal digit of FWA',
             description='Emit the integer part (top nibble of the mantissa MSB) '
                         'as a decimal digit, mask it off, then multiply the '
                         'remaining fraction by 10 ready for the next digit. The '
                         'inner step of the real-to-ASCII conversion.',
             on_entry={'zp_fwa_m1 (&31)': 'mantissa MSB; top nibble is the digit'},
             on_exit={'string_work (&0600)': 'the digit appended',
                      'zp_strbuf_len (&36)': 'incremented',
                      'zp_fwa (&31-&35)': 'fraction times ten for the next digit'})
# output_top_digit (&A040)
d.comment(0xa040, 'Integer part: top nibble', align=Align.INLINE)
d.comment(0xa042, 'shift the top nibble down,', align=Align.INLINE)
d.comment(0xa043, '(continued)', align=Align.INLINE)
d.comment(0xa044, '(continued)', align=Align.INLINE)
d.comment(0xa045, '(continued)', align=Align.INLINE)
d.comment(0xa046, 'output it as a digit', align=Align.INLINE)
d.comment(0xa049, 'mask off the integer part:', align=Align.INLINE)
d.comment(0xa04b, 'keep the low nibble', align=Align.INLINE)
d.comment(0xa04d, '(store)', align=Align.INLINE)
d.comment(0xa04f, 'multiply the fraction by 10', align=Align.INLINE)
d.subroutine(0xa052, 'output_byte_decimal', title='Output a byte (0-99) in decimal',
             description='Append a byte 0-99 to the output string as one or two '
                         'decimal digits (a leading-zero tens digit is dropped) '
                         'by repeated subtraction of ten.',
             on_entry={'A': 'the value 0-99 to output'},
             on_exit={'string_work (&0600)': 'the digits appended',
                      'zp_strbuf_len (&36)': 'advanced', 'X': 'the tens count'})
# output_byte_decimal (&A052)
d.comment(0xa052, 'count the tens:', align=Align.INLINE)
d.comment(0xa054, 'ready the subtract', align=Align.INLINE)
d.comment(0xa055, 'subtract 10...', align=Align.INLINE)
# output_byte_decimal / output_char tail
d.label(0xa055, 'obd_tens_loop')
d.comment(0xa056, 'minus 10', align=Align.INLINE)
d.comment(0xa058, 'until it goes negative', align=Align.INLINE)
d.comment(0xa05a, 'add 10 back (the units)', align=Align.INLINE)
d.comment(0xa05c, 'save the units', align=Align.INLINE)
d.comment(0xa05d, 'the tens digit', align=Align.INLINE)
d.comment(0xa05e, 'no tens: skip', align=Align.INLINE)
d.comment(0xa060, 'output the tens digit', align=Align.INLINE)
d.comment(0xa063, 'units digit', align=Align.INLINE)
d.label(0xa063, 'obd_units')
d.subroutine(0xa064, 'output_digit', title='Output A as a decimal digit (A + "0")',
             description='Convert the digit value in A to ASCII ("0" + A) and '
                         'append it via output_char.',
             on_entry={'A': 'a digit value 0-9'},
             on_exit={'string_work (&0600)': 'the digit appended',
                      'zp_strbuf_len (&36)': 'incremented', 'X': 'preserved'})
d.comment(0xa064, 'make it a digit ("0" + A)', align=Align.INLINE)
d.char_literal(0xa065)
d.subroutine(0xa066, 'output_char', title='Append a character to the output string',
             description='Append the character in A to the end of the output '
                         'string buffer and bump its length.',
             on_entry={'A': 'the character to append',
                       'zp_strbuf_len (&36)': 'the current buffer length'},
             on_exit={'string_work (&0600)': 'A stored at the old length',
                      'zp_strbuf_len (&36)': 'incremented', 'X': 'preserved'})

# output_char (&A066)
d.comment(0xa066, 'save X', align=Align.INLINE)
d.comment(0xa068, 'append at the end of the buffer', align=Align.INLINE)
d.comment(0xa06a, 'write it', align=Align.INLINE)
d.comment(0xa06d, 'restore X', align=Align.INLINE)
d.comment(0xa06f, 'one longer', align=Align.INLINE)
d.comment(0xa071, 'Return', align=Align.INLINE)
d.comment(0xa072, 'set the rounding byte and test the sign', align=Align.INLINE)
d.label(0xa072, 'make_real_result')
d.comment(0xa073, '(rnd = 0)', align=Align.INLINE)
d.comment(0xa075, 'test the sign', align=Align.INLINE)
d.comment(0xa078, 'real result', align=Align.INLINE)
d.comment(0xa07a, 'Return', align=Align.INLINE)

d.subroutine(0xa07b, 'parse_number', title='Parse an unsigned number at PtrB',
             description='Parse an unsigned decimal number at PtrB into the '
                         'accumulator: digits, a "." and an "E" exponent, '
                         'choosing integer or real form (a decimal point or '
                         'exponent forces real). Decimal only - there is no '
                         '"&" hex path here; "&" constants are read separately '
                         'by [`factor_hex`](address:ae6d), and a non-digit '
                         'first character yields 0. Shared by the expression '
                         'decimal factor ([`eval_factor`](address:adec)) and '
                         'VAL (via [`ascii_to_number`](address:ac34)).',
             on_entry={'zp_text_ptr2 (&19/&1A)': 'PtrB at the first digit'},
             on_exit={'A': 'result type: <0 float in fwa, >0 integer in iwa',
                      'zp_iwa / zp_fwa': 'the parsed value',
                      'zp_text_ptr2_off (&1B)': 'advanced past the number'})
# parse_number (&A07B): parse a decimal number at PtrB into the accumulator
d.comment(0xa07b, 'Clear FWA:', align=Align.INLINE)
d.comment(0xa07d, 'mantissa byte 1 (top),', align=Align.INLINE)
d.comment(0xa07f, 'byte 2,', align=Align.INLINE)
d.comment(0xa081, 'byte 3,', align=Align.INLINE)
d.comment(0xa083, 'byte 4,', align=Align.INLINE)
d.comment(0xa085, 'and the guard byte', align=Align.INLINE)
d.comment(0xa087, 'clear the decimal-point flag', align=Align.INLINE)
d.comment(0xa089, 'decimal exponent = 0', align=Align.INLINE)
d.comment(0xa08b, 'a leading decimal point?', align=Align.INLINE)
d.char_literal(0xa08c)
d.comment(0xa08d, 'yes', align=Align.INLINE)
d.comment(0xa08f, "not a digit (>= ':')?", align=Align.INLINE)
d.char_literal(0xa090)
d.comment(0xa091, 'finish', align=Align.INLINE)
d.comment(0xa093, 'convert to binary 0-9', align=Align.INLINE)
d.comment(0xa095, 'not a digit: finish', align=Align.INLINE)
d.comment(0xa097, 'store the digit', align=Align.INLINE)
d.comment(0xa099, 'next character', align=Align.INLINE)
# parse_number
d.label(0xa099, 'pn_loop')
d.comment(0xa09a, 'read it', align=Align.INLINE)
d.comment(0xa09c, 'a decimal point?', align=Align.INLINE)
d.char_literal(0xa09d)
d.comment(0xa09e, 'no', align=Align.INLINE)
d.comment(0xa0a0, 'already had one?', align=Align.INLINE)
d.label(0xa0a0, 'pn_dup_point')
d.comment(0xa0a2, 'yes: end of the number', align=Align.INLINE)
d.comment(0xa0a4, 'set the decimal-point flag', align=Align.INLINE)
d.comment(0xa0a6, 'next char', align=Align.INLINE)
d.comment(0xa0a8, "'E' (exponent)?", align=Align.INLINE)
d.char_literal(0xa0a9)
d.label(0xa0a8, 'pn_check_e')
d.comment(0xa0aa, 'yes: scan the exponent', align=Align.INLINE)
d.comment(0xa0ac, 'not a digit?', align=Align.INLINE)
d.char_literal(0xa0ad)
d.comment(0xa0ae, 'finish', align=Align.INLINE)
d.comment(0xa0b0, 'convert to binary', align=Align.INLINE)
d.comment(0xa0b2, 'not a digit: finish', align=Align.INLINE)
d.comment(0xa0b4, 'mantissa top byte', align=Align.INLINE)
d.comment(0xa0b6, 'room for another digit?', align=Align.INLINE)
d.comment(0xa0b8, 'yes: add it', align=Align.INLINE)
d.comment(0xa0ba, 'too big: had a decimal point?', align=Align.INLINE)
d.comment(0xa0bc, 'yes: just skip the digit', align=Align.INLINE)
d.comment(0xa0be, 'no: bump the exponent and skip', align=Align.INLINE)
d.comment(0xa0c0, 'skip this over-large digit', align=Align.INLINE)
d.comment(0xa0c2, 'had a decimal point?', align=Align.INLINE)
d.label(0xa0c2, 'pn_check_point')
d.comment(0xa0c4, 'no', align=Align.INLINE)
d.comment(0xa0c6, 'yes: decrement the exponent', align=Align.INLINE)
d.comment(0xa0c8, 'FWA mantissa *= 10', align=Align.INLINE)
d.label(0xa0c8, 'pn_mant_x10')
d.comment(0xa0cb, 'add the digit to the low byte', align=Align.INLINE)
d.comment(0xa0cd, 'store the new low mantissa byte', align=Align.INLINE)
d.comment(0xa0cf, 'no carry: next digit', align=Align.INLINE)
d.comment(0xa0d1, 'carry up through the mantissa', align=Align.INLINE)
d.comment(0xa0d3, 'absorbed in byte 4: next digit', align=Align.INLINE)
d.comment(0xa0d5, 'wrapped: carry into byte 3,', align=Align.INLINE)
d.comment(0xa0d7, 'absorbed: next digit', align=Align.INLINE)
d.comment(0xa0d9, 'byte 2,', align=Align.INLINE)
d.comment(0xa0db, 'absorbed: next digit', align=Align.INLINE)
d.comment(0xa0dd, 'byte 1 (top)', align=Align.INLINE)
d.comment(0xa0df, 'next digit', align=Align.INLINE)
d.comment(0xa0e1, 'scan the E exponent', align=Align.INLINE)
d.label(0xa0e1, 'pn_scan_e')
d.comment(0xa0e4, 'add to the decimal exponent', align=Align.INLINE)
d.comment(0xa0e6, 'store it back', align=Align.INLINE)
d.comment(0xa0e8, 'store the text offset', align=Align.INLINE)
d.label(0xa0e8, 'pn_store_offset')
d.comment(0xa0ea, 'any exponent or decimal point?', align=Align.INLINE)
d.comment(0xa0ec, 'combine with the decimal-point flag', align=Align.INLINE)
d.comment(0xa0ee, 'no: return an integer', align=Align.INLINE)
d.comment(0xa0f0, 'value zero?', align=Align.INLINE)
d.comment(0xa0f3, 'yes: done', align=Align.INLINE)
d.comment(0xa0f5, 'Set the FWA exponent (40-bit mantissa)...', align=Align.INLINE)
d.label(0xa0f5, 'pn_set_exp_loop')
d.comment(0xa0f7, 'store the exponent', align=Align.INLINE)
d.comment(0xa0f9, 'zero for overflow and sign', align=Align.INLINE)
d.comment(0xa0fb, 'clear overflow', align=Align.INLINE)
d.comment(0xa0fd, 'clear sign', align=Align.INLINE)
d.comment(0xa0ff, 'normalise', align=Align.INLINE)
d.comment(0xa102, 'apply the decimal exponent:', align=Align.INLINE)
d.comment(0xa104, 'negative: divide', align=Align.INLINE)
d.comment(0xa106, 'zero: done', align=Align.INLINE)
d.comment(0xa108, 'positive: multiply by 10', align=Align.INLINE)
d.label(0xa108, 'pn_exp_mul_loop')
d.comment(0xa10b, 'one fewer power of ten to apply', align=Align.INLINE)
d.comment(0xa10d, 'loop', align=Align.INLINE)
d.comment(0xa10f, 'done', align=Align.INLINE)
d.comment(0xa111, 'divide by 10', align=Align.INLINE)
d.label(0xa111, 'pn_exp_div')
d.comment(0xa114, 'count the exponent up toward zero', align=Align.INLINE)
d.comment(0xa116, 'loop', align=Align.INLINE)
d.comment(0xa118, 'round the result', align=Align.INLINE)
d.label(0xa118, 'pn_round')
d.comment(0xa11b, 'real result', align=Align.INLINE)
d.label(0xa11b, 'pn_real_result')
d.comment(0xa11c, 'A = &FF: real result', align=Align.INLINE)
d.comment(0xa11e, 'Return (real)', align=Align.INLINE)
d.comment(0xa11f, 'Integer: does it fit in 32 signed bits?', align=Align.INLINE)
d.label(0xa11f, 'pn_check_int')
d.comment(0xa121, 'stash byte 2 as the IWA top byte', align=Align.INLINE)
d.comment(0xa123, 'isolate its sign bit', align=Align.INLINE)
d.comment(0xa125, 'top byte set (too big)?', align=Align.INLINE)
d.comment(0xa127, 'yes: use a real instead', align=Align.INLINE)
d.comment(0xa129, 'Copy the mantissa to IWA:', align=Align.INLINE)
d.comment(0xa12b, 'guard byte -> IWA low,', align=Align.INLINE)
d.comment(0xa12d, 'byte 4', align=Align.INLINE)
d.comment(0xa12f, '-> IWA byte 1,', align=Align.INLINE)
d.comment(0xa131, 'byte 3', align=Align.INLINE)
d.comment(0xa133, '-> IWA byte 2', align=Align.INLINE)
d.comment(0xa135, 'integer result', align=Align.INLINE)
d.comment(0xa137, 'carry set: a valid number', align=Align.INLINE)
d.comment(0xa138, 'Return (integer)', align=Align.INLINE)
d.comment(0xa139, 'negative exponent: scan the digits', align=Align.INLINE)
d.label(0xa139, 'pn_neg_exp_loop')
d.comment(0xa13c, 'negate it', align=Align.INLINE)
d.comment(0xa13e, 'carry so caller adc completes the negate', align=Align.INLINE)
d.comment(0xa13f, 'Return', align=Align.INLINE)
d.subroutine(0xa140, 'parse_exponent', title='Parse the "E" exponent (optional sign, 1-2 digits)',
             description='Read the one- or two-digit decimal exponent after "E" '
                         'at PtrB, returning its magnitude in A (0 if no digits). '
                         'The sign is handled on a separate entry path; the '
                         'caller adds the result to the FWA exponent.',
             on_entry={'zp_text_ptr2 (&19/&1A)': 'the expression text pointer (PtrB)',
                       'Y': 'offset of the "E" character'},
             on_exit={'A': 'the exponent magnitude (0-99)',
                      'Y': 'advanced past the exponent digits',
                      'C': 'clear (ready for the caller to add it)'})

d.comment(0xa140, 'Scan exponent: next character', align=Align.INLINE)
d.comment(0xa141, 'read it', align=Align.INLINE)
d.comment(0xa143, "'-'?", align=Align.INLINE)
d.char_literal(0xa144)
d.comment(0xa145, 'yes: negative exponent', align=Align.INLINE)
d.comment(0xa147, "'+'?", align=Align.INLINE)
d.char_literal(0xa148)
d.comment(0xa149, 'no sign', align=Align.INLINE)
d.comment(0xa14b, 'skip the sign', align=Align.INLINE)
# parse_exponent
d.label(0xa14b, 'pe_skip_sign')
d.comment(0xa14c, 'read the digit after the sign', align=Align.INLINE)
d.comment(0xa14e, 'a digit?', align=Align.INLINE)
d.char_literal(0xa14f)
d.label(0xa14e, 'pe_digit')
d.comment(0xa150, 'no: exponent = 0', align=Align.INLINE)
d.comment(0xa152, 'convert', align=Align.INLINE)
d.comment(0xa154, 'not a digit: exponent = 0', align=Align.INLINE)
d.comment(0xa156, 'store the first exponent digit', align=Align.INLINE)
d.comment(0xa158, 'second digit?', align=Align.INLINE)
d.comment(0xa159, 'read it', align=Align.INLINE)
d.comment(0xa15b, 'above 9?', align=Align.INLINE)
d.char_literal(0xa15c)
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
d.label(0xa170, 'pe_one_digit')
d.comment(0xa172, 'carry clear for the caller ADC', align=Align.INLINE)
d.comment(0xa173, 'Return', align=Align.INLINE)
d.comment(0xa174, 'no exponent: 0', align=Align.INLINE)
d.label(0xa174, 'pe_no_exp')

d.comment(0xa176, 'carry clear for the caller ADC', align=Align.INLINE)
d.comment(0xa177, 'Return', align=Align.INLINE)

# fwa_acc_fwb (&A178): FWA mantissa += FWB mantissa
d.comment(0xa178, 'Add the mantissas: rounding byte', align=Align.INLINE)
d.subroutine(0xa178, 'fwa_acc_fwb', title='Add FWB into FWA',
             description='Add the FWB mantissa (rnd, m4-m1) into the FWA '
                         'mantissa with a single carry chain. Mantissa-only: '
                         'exponents must already be aligned by the caller. Used '
                         'by multiply, *10 and /10.',
             on_entry={'zp_fwa (&31-&35)': 'mantissa + rnd of accumulator A',
                       'zp_fwb (&3E-&42)': 'mantissa + rnd of accumulator B',
                       'C': 'clear (it is the carry-in to the addition)'},
             on_exit={'zp_fwa (&31-&35)': 'the summed mantissa',
                      'C': 'carry out of the mantissa MSB (overflow)',
                      'X': 'preserved', 'Y': 'preserved'})

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
d.subroutine(0xa197, 'mant_mul10', title='Multiply the FWA mantissa by 10',
             description='Multiply the FWA mantissa (m1-m4 and the rounding '
                         'byte) by ten as x4 + x1 = x5 then x2, leaving the '
                         'exponent untouched. Used by the number<->ASCII '
                         'conversions, which track the decimal point separately.',
             on_entry={'zp_fwa (&31-&35)': 'the mantissa to scale'},
             on_exit={'zp_fwa (&31-&35)': 'the mantissa times ten',
                      'C': 'carry out of the mantissa MSB',
                      'A': 'preserved', 'Y': 'preserved',
                      'X': 'corrupted (holds the original m4)'})

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

d.subroutine(
    0xa1da, 'fwa_sign',
    title='Get the sign of the FP accumulator',
    description="""Determine the sign of the floating-point accumulator by
OR-ing the mantissa and rounding bytes (&31-&35) to test for zero, then
reading the sign byte. Forces a clean zero (sign, exponent and overflow
byte cleared) when the mantissa is empty.
""",
    on_entry={'zp_fwa (&2E-&35)': 'the floating-point accumulator A'},
    on_exit={
        'A': '+1 positive, 0 zero, &FF negative',
        'N': 'set when FWA is negative', 'Z': 'set when FWA is zero',
        'X': 'preserved', 'Y': 'preserved',
    },
)
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
# small FP primitives
d.label(0xa1ed, 'sign_force_zero')
d.comment(0xa1ef, 'exponent,', align=Align.INLINE)
d.comment(0xa1f1, 'and overflow byte, then return A = 0', align=Align.INLINE)

# ======================================================================
# DEPTH 0 LEAVES — full per-instruction coverage (see ANNOTATION_PROGRESS)
# ======================================================================

# shared return points and small helpers filling the leaf extents
d.comment(0xa1f3, 'Return (shared)', align=Align.INLINE)
d.subroutine(0xa1f4, 'fwa_mul10', title='FWA = FWA * 10',
             description='Multiply FWA by ten as x8 + x2: scale the exponent by '
                         'eight, build x2 in FWB, and add. Left unnormalised and '
                         'unrounded (the caller normalises). Uses FWB as scratch.',
             on_entry={'zp_fwa (&2E-&35)': 'the value to scale'},
             on_exit={'zp_fwa (&2E-&35)': 'ten times FWA, unnormalised',
                      'zp_fwb (&3B-&42)': 'corrupted (scratch)'})
# fwa_mul10 (&A1F4): FWA = FWA * 10
d.comment(0xa1f4, 'x*8: add 3 to the exponent', align=Align.INLINE)
d.comment(0xa1f5, 'exponent...', align=Align.INLINE)
d.comment(0xa1f7, '+ 3', align=Align.INLINE)
d.comment(0xa1f9, '(store)', align=Align.INLINE)
d.comment(0xa1fb, 'no carry', align=Align.INLINE)
d.comment(0xa1fd, 'carry into overflow', align=Align.INLINE)
d.comment(0xa1ff, 'FWB = x*8', align=Align.INLINE)
d.label(0xa1ff, 'mul10_x8')
d.comment(0xa202, 'FWB = x*4', align=Align.INLINE)
d.comment(0xa205, 'FWB = x*2', align=Align.INLINE)
d.comment(0xa208, 'FWA = x*8 + x*2 = x*10', align=Align.INLINE)
d.subroutine(
    0xa208, 'fwa_acc10',
    title='Add FWB into FWA with carry renormalisation',
    description="""Add FWB into FWA via fwa_acc_fwb, then renormalise (fwa_carry_renorm):
if the mantissa addition overflowed, shift FWA's mantissa right one
bit and increment the exponent. Used repeatedly by the x10 / decimal-conversion routines to accumulate shifted terms into FWA.
""",
    on_entry={
        'zp_fwa (&2E-&35)': 'floating-point accumulator A',
        'zp_fwb (&3B-&42)': 'floating-point accumulator B, the term to add',
    },
    on_exit={
        'zp_fwa (&2E-&35)': 'FWA + FWB, renormalised (mantissa shifted right and exponent bumped on overflow)',
        'X': 'preserved',
    },
)
d.comment(0xa20b, 'no overflow: done', align=Align.INLINE)
d.label(0xa20b, 'fwa_carry_renorm')
d.comment(0xa20d, 'Overflow: shift right, bump exponent: m1', align=Align.INLINE)
d.comment(0xa20f, 'm2', align=Align.INLINE)
d.comment(0xa211, 'm3', align=Align.INLINE)
d.comment(0xa213, 'm4', align=Align.INLINE)
d.comment(0xa215, 'rounding', align=Align.INLINE)
d.comment(0xa217, 'exponent + 1', align=Align.INLINE)
d.comment(0xa219, 'done', align=Align.INLINE)
d.comment(0xa21b, 'exponent overflow', align=Align.INLINE)
d.comment(0xa21d, 'Return', align=Align.INLINE)

d.subroutine(0xa21e, 'fwb_copy_from_fwa', title='FWB = FWA',
             description='Copy all ten bytes of FWA into FWB.',
             on_entry={'zp_fwa (&2E-&35)': 'the floating-point accumulator A'},
             on_exit={'zp_fwb (&3B-&42)': 'a copy of FWA', 'X': 'preserved'})
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

d.subroutine(
    0xa23f, 'fwb_half_fwa',
    title='FWB = FWA / 2',
    description="""Copy FWA into FWB (fwb_copy_from_fwa), then fall into fwb_div2 to
shift the FWB mantissa (including the rounding byte) right one bit.
The exponent is left unchanged, so the result is de-normalised; used
to build the progressively shifted terms in fwa_div10.
""",
    on_entry={
        'zp_fwa (&2E-&35)': 'floating-point accumulator A',
    },
    on_exit={
        'zp_fwb (&3B-&42)': 'FWA with its mantissa shifted right one bit (rounding byte included)',
        'X': 'preserved',
        'C': 'the bit shifted out of the rounding byte',
    },
)
d.comment(0xa23f, 'FWB = FWA, then halve it', align=Align.INLINE)
# fwb_half_fwa (&A23F) / fwb_div2 (&A242): FWB = FWA / 2, and FWB >>= 1
d.subroutine(0xa242, 'fwb_div2', title='Divide FWB by two',
             description='Shift the FWB mantissa right one bit (FWB = FWB / 2). '
                         'Leaves the exponent alone, so the result is left '
                         'de-normalised; used to align exponents before adding.',
             on_entry={'zp_fwb (&3B-&42)': 'the floating-point accumulator B'},
             on_exit={'zp_fwb': 'mantissa shifted right one bit (rnd byte included)',
                      'X': 'preserved', 'C': 'the bit shifted out of the rnd byte'})
d.comment(0xa242, 'Shift FWB right one bit (/2): mantissa MSB', align=Align.INLINE)
d.comment(0xa244, 'byte 2', align=Align.INLINE)
d.comment(0xa246, 'byte 3', align=Align.INLINE)
d.comment(0xa248, 'byte 4', align=Align.INLINE)
d.comment(0xa24a, 'rounding byte', align=Align.INLINE)
d.comment(0xa24c, 'FWB halved', align=Align.INLINE)

d.subroutine(0xa24d, 'fwa_div10', title='FWA = FWA / 10',
             description='Divide FWA by ten using the binary expansion of 1/10 '
                         '(x/16 plus progressively shifted terms accumulated via '
                         'FWB). Left unnormalised and unrounded (the caller '
                         'normalises). Uses FWB as scratch.',
             on_entry={'zp_fwa (&2E-&35)': 'the value to divide'},
             on_exit={'zp_fwa (&2E-&35)': 'FWA / 10, unnormalised',
                      'zp_fwb (&3B-&42)': 'corrupted (scratch)'})
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
d.label(0xa258, 'div10_step')
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
d.comment(0xa2a1, '...into the carry', align=Align.INLINE)
d.comment(0xa2a2, 'next bit...', align=Align.INLINE)

# --- renames discovered during the leaf pass --------------------------
d.subroutine(
    0xa2a4, 'fwa_round_carry',
    title='Add to the rounding byte and ripple the carry up',
    description="""Add A (plus the carry-in) to the FWA rounding byte, then
propagate any carry up through the mantissa (m4 -> m1). A carry out of
the top renormalises the exponent (shift right, exponent + 1) and may
set the overflow byte. Used to round the mantissa up.
""",
    on_entry={'A': 'the rounding increment to add to the rnd byte',
              'C': 'carry-in to the addition',
              'zp_fwa (&31-&35)': 'the mantissa + rnd to round'},
    on_exit={'zp_fwa (&30-&35)': 'the rounded mantissa (exponent may step up)',
             'X': 'preserved', 'Y': 'preserved'},
)
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

d.comment(0xa2bd, 'Return (shared)', align=Align.INLINE)
d.subroutine(
    0xa2be, 'int_to_fwa',
    title='Convert the integer accumulator to floating point',
    description='Convert the signed 32-bit integer in IWA to a normalised real '
                'in FWA: record the sign (negating IWA if needed), copy the '
                'magnitude into the mantissa with exponent 32, and normalise.',
    on_entry={'zp_iwa (&2A-&2D)': 'the signed integer to convert'},
    on_exit={'zp_fwa (&2E-&35)': 'the value as a normalised real',
             'zp_iwa': 'made positive if it was negative', 'X': 'corrupted'},
)

# int_to_fwa (&A2BE): IWA -> FWA
d.comment(0xa2be, 'Clear the rounding...', align=Align.INLINE)
d.comment(0xa2c0, '(rnd = 0)', align=Align.INLINE)
d.comment(0xa2c2, '...and overflow bytes', align=Align.INLINE)
d.comment(0xa2c4, 'Sign of IWA (top byte)', align=Align.INLINE)
d.comment(0xa2c6, 'positive: sign byte = 0', align=Align.INLINE)
d.comment(0xa2c8, 'negative: make it positive...', align=Align.INLINE)
d.comment(0xa2cb, '...and set the sign byte', align=Align.INLINE)
d.comment(0xa2cd, '(store the sign)', align=Align.INLINE)
# int_to_fwa / fwa_mul10 / fwa_normalise
d.label(0xa2cd, 'itf_store_sign')
d.comment(0xa2cf, 'Copy IWA into the mantissa (MSB first):', align=Align.INLINE)
d.comment(0xa2d1, 'byte 0 -> m4', align=Align.INLINE)
d.comment(0xa2d3, 'read it', align=Align.INLINE)
d.comment(0xa2d5, 'byte 1 -> m3', align=Align.INLINE)
d.comment(0xa2d7, 'read it', align=Align.INLINE)
d.comment(0xa2d9, 'byte 2 -> m2', align=Align.INLINE)
d.comment(0xa2db, 'read it', align=Align.INLINE)
d.comment(0xa2dd, 'byte 3 -> m1 (MSB)', align=Align.INLINE)
d.comment(0xa2df, 'Exponent &A0 (= 32): a 32-bit integer', align=Align.INLINE)
d.comment(0xa2e1, '(store)', align=Align.INLINE)
d.comment(0xa2e3, 'normalise the result', align=Align.INLINE)
d.comment(0xa2e6, 'Zero: clear sign,', align=Align.INLINE)
d.label(0xa2e6, 'itf_zero')
d.comment(0xa2e8, 'exponent,', align=Align.INLINE)
d.comment(0xa2ea, 'overflow', align=Align.INLINE)
d.comment(0xa2ec, 'Return', align=Align.INLINE)
d.subroutine(0xa2ed, 'small_int_to_fwa', title='Convert a small (8-bit) integer in A to FWA',
             description='Convert the signed 8-bit integer in A to a normalised '
                         'real in FWA (clears FWA, places the magnitude in the '
                         'mantissa MSB with exponent 8, sets the sign, and '
                         'normalises).',
             on_entry={'A': 'the signed 8-bit integer to convert'},
             on_exit={'zp_fwa (&2E-&35)': 'the value as a normalised real'})

d.comment(0xa2ed, 'Small int to FWA: save it', align=Align.INLINE)
d.comment(0xa2ee, 'clear FWA', align=Align.INLINE)
d.comment(0xa2f1, 'recover it', align=Align.INLINE)
d.comment(0xa2f2, 'zero: done', align=Align.INLINE)
d.comment(0xa2f4, 'positive', align=Align.INLINE)
d.comment(0xa2f6, 'negative: set the sign...', align=Align.INLINE)
d.comment(0xa2f8, '0...', align=Align.INLINE)
d.comment(0xa2fa, 'minus the value:', align=Align.INLINE)
d.comment(0xa2fb, '...and negate the value', align=Align.INLINE)
d.comment(0xa2fd, 'value into the mantissa MSB', align=Align.INLINE)
d.label(0xa2fd, 'si8_set_mantissa')
d.comment(0xa2ff, 'Exponent &88 (= 8): an 8-bit value', align=Align.INLINE)
d.comment(0xa301, '(store; falls into normalise)', align=Align.INLINE)

d.subroutine(0xa303, 'fwa_normalise', title='Normalise FWA',
             description='Shift the FWA mantissa left until bit 7 of the MSB is '
                         'set, decrementing the exponent by 8 per whole-byte '
                         'shift and by 1 per bit, so the implied leading 1 is '
                         'restored. An all-zero mantissa is forced to a clean '
                         'zero. Underflow is handled via the overflow byte.',
             on_entry={'zp_fwa (&2E-&35)': 'an unnormalised accumulator'},
             on_exit={'zp_fwa (&2E-&35)': 'normalised (mantissa MSB bit 7 set) '
                                          'or a clean zero'})
# fwa_normalise (&A303): shift the mantissa left until bit 7 of m1 is set
d.comment(0xa303, 'Mantissa MSB...', align=Align.INLINE)
# --- fwa_normalise: shift the mantissa until bit 7 of m1 is set -------
d.comment(0xa305, 'Top bit already set: nothing to do', align=Align.INLINE)
d.comment(0xa307, 'OR in the lower mantissa bytes (byte 2)', align=Align.INLINE)
d.comment(0xa309, '(byte 3)', align=Align.INLINE)
d.comment(0xa30b, '(byte 4) to test the whole mantissa', align=Align.INLINE)
d.comment(0xa30d, 'Mantissa entirely zero: the value is zero',
          align=Align.INLINE)
d.comment(0xa30f, 'so jump away to handle the zero value', align=Align.INLINE)
d.comment(0xa311, 'Load the exponent to adjust as we shift', align=Align.INLINE)
d.comment(0xa313, 'Shift up a whole byte while the MSB byte is zero',
          align=Align.INLINE)
d.label(0xa313, 'norm_byte_loop')
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
d.comment(0xa32c, 'each byte shift advances the exponent by 8',
          align=Align.INLINE)
d.comment(0xa32e, 'Store the reduced exponent', align=Align.INLINE)
d.comment(0xa330, 'Loop to shift another byte if MSB still zero', align=Align.INLINE)
d.comment(0xa332, 'Borrow into the overflow byte', align=Align.INLINE)
d.comment(0xa334, 'Continue the byte-shift loop', align=Align.INLINE)
d.comment(0xa336, 'Bit-shift loop: re-check the MSB', align=Align.INLINE)
d.label(0xa336, 'norm_bit_check')
d.comment(0xa338, 'Bit 7 set: normalised, return', align=Align.INLINE)
d.comment(0xa33a, 'Then shift left one bit at a time to normalise',
          align=Align.INLINE)

d.label(0xa33a, 'norm_bit_loop')
d.comment(0xa33c, 'Shift the mantissa left one bit: byte 4', align=Align.INLINE)
d.comment(0xa33e, 'byte 3', align=Align.INLINE)
d.comment(0xa340, 'byte 2', align=Align.INLINE)
d.comment(0xa342, 'byte 1 (MSB)', align=Align.INLINE)
d.comment(0xa344, 'Reduce the exponent by one', align=Align.INLINE)
d.comment(0xa346, 'Store it', align=Align.INLINE)
d.comment(0xa348, 'Loop until the MSB bit is set', align=Align.INLINE)
d.comment(0xa34a, 'Borrow into the overflow byte', align=Align.INLINE)
d.comment(0xa34c, 'Continue the bit-shift loop', align=Align.INLINE)

d.subroutine(0xa34e, 'fwb_unpack_var', title='Unpack a fp variable into FWB',
             description='Expand the packed five-byte float addressed by '
                         'zp_fp_ptr into the unpacked FWB accumulator: split '
                         'the sign out of the mantissa MSB, restore the implied '
                         'leading 1 (unless the value is zero), and clear the '
                         'overflow and rounding bytes.',
             on_entry={'(zp_fp_ptr) (&4B/&4C)': 'a packed five-byte float'},
             on_exit={'zp_fwb (&3B-&42)': 'the unpacked value', 'X': 'preserved'})

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
d.label(0xa37a, 'fwb_unpack_msb')
d.comment(0xa37c, 'FWB now holds the unpacked value', align=Align.INLINE)

d.subroutine(0xa37d, 'fwa_pack_temp2', title='Pack FWA into TEMP2',
             description='Point zp_fp_ptr at FP TEMP2 (&0471), then pack FWA '
                         'into it via fwa_pack_var.',
             on_entry={'zp_fwa (&2E-&35)': 'the value to store'},
             on_exit={'(&0471)': 'FWA packed into five bytes',
                      'zp_fp_ptr (&4B/&4C)': '= &0471', 'X': 'preserved'})
# fwa_pack_temp2/3 (&A37D/&A381): point at FP TEMP2/TEMP3, then pack
d.comment(0xa37d, 'Point at FP TEMP2 (&0471): low byte', align=Align.INLINE)
d.comment(0xa37f, 'join the common pack code', align=Align.INLINE)
d.subroutine(0xa381, 'fwa_pack_temp3', title='Pack FWA into TEMP3',
             description='Point zp_fp_ptr at FP TEMP3 (&0476), then pack FWA '
                         'into it via fwa_pack_var.',
             on_entry={'zp_fwa (&2E-&35)': 'the value to store'},
             on_exit={'(&0476)': 'FWA packed into five bytes',
                      'zp_fp_ptr (&4B/&4C)': '= &0476', 'X': 'preserved'})
d.comment(0xa381, 'Point at FP TEMP3 (&0476): low byte', align=Align.INLINE)
d.comment(0xa383, 'join the common pack code', align=Align.INLINE)

d.subroutine(0xa385, 'fwa_pack_temp1', title='Pack FWA into TEMP1',
             description='Point zp_fp_ptr at FP TEMP1 (&046C), then pack FWA '
                         'into it via fwa_pack_var.',
             on_entry={'zp_fwa (&2E-&35)': 'the value to store'},
             on_exit={'(&046C)': 'FWA packed into five bytes',
                      'zp_fp_ptr (&4B/&4C)': '= &046C', 'X': 'preserved'})
# fwa_pack_temp1/2/3 (&A385/&A37D/&A381): point at an FP temp, then pack
d.comment(0xa385, 'Point at FP TEMP1 (&046C): low byte', align=Align.INLINE)
d.comment(0xa387, 'set the fp-variable pointer', align=Align.INLINE)
d.label(0xa387, 'pack_temp_tail')
d.comment(0xa389, 'high byte &04', align=Align.INLINE)
d.comment(0xa38b, 'then fall into fwa_pack_var', align=Align.INLINE)
# Pack / unpack between the accumulator and 5-byte stored form.
d.subroutine(0xa38d, 'fwa_pack_var', title='Pack FWA into a fp variable',
             description='Compress the unpacked FWA accumulator into the packed '
                         'five-byte form addressed by zp_fp_ptr: exponent, then '
                         'the sign folded into bit 7 of the mantissa MSB (the '
                         'implied leading 1 is dropped), then mantissa bytes 2-4.',
             on_entry={'zp_fwa (&2E-&35)': 'the value to store',
                       'zp_fp_ptr (&4B/&4C)': 'where to write the five bytes'},
             on_exit={'(zp_fp_ptr)': 'the packed five-byte float',
                      'zp_fwa_sign (&2E)': 'reduced to its sign bit',
                      'X': 'preserved'})
# fwa_pack_var (&A38D): pack FWA into the 5-byte value at (zp_fp_ptr)
d.comment(0xa38d, 'Write packed bytes from offset 0', align=Align.INLINE)
d.comment(0xa38f, 'Packed byte 0 is the exponent', align=Align.INLINE)
d.comment(0xa391, '(store it)', align=Align.INLINE)
d.comment(0xa393, 'next byte', align=Align.INLINE)
d.comment(0xa394, 'Take the sign byte', align=Align.INLINE)
# --- fwa_pack_var: unpacked FWA -> packed 5-byte at (zp_fp_ptr) -------
d.comment(0xa396, 'Isolate the sign bit', align=Align.INLINE)
d.comment(0xa398, 'keep only the sign bit', align=Align.INLINE)
d.comment(0xa39a, 'Mantissa MSB', align=Align.INLINE)
d.comment(0xa39c, 'Drop the implied leading 1 from the mantissa MSB',
          align=Align.INLINE)
d.comment(0xa39e, 'and fold the sign back into its bit 7', align=Align.INLINE)

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

d.subroutine(0xa3b2, 'fwa_unpack_temp1', title='Unpack TEMP1 into FWA',
             description='Point zp_fp_ptr at FP TEMP1 (&046C), then unpack it '
                         'into FWA via fwa_unpack_var.',
             on_entry={'(&046C)': 'a packed five-byte float'},
             on_exit={'zp_fwa (&2E-&35)': 'the unpacked value',
                      'zp_fp_ptr (&4B/&4C)': '= &046C', 'X': 'preserved'})
d.comment(0xa3b2, 'Point at FP TEMP1, then unpack it into FWA',
          align=Align.INLINE)

d.subroutine(
    0xa3b5, 'fwa_unpack_var',
    title='Unpack a floating-point variable into FWA',
    description="""Expand the packed five-byte float addressed by zp_fp_ptr into
the unpacked FWA accumulator: split the sign out of the mantissa MSB,
restore the implied leading 1 (unless the value is zero), and clear the
overflow and rounding bytes.
""",
    on_entry={'(zp_fp_ptr) (&4B/&4C)': 'a packed five-byte float'},
    on_exit={'zp_fwa (&2E-&35)': 'the unpacked value', 'X': 'preserved'},
)
# --- fwa_unpack_var: packed 5-byte -> unpacked 8-byte FWA ------------
d.comment(0xa3b5, 'Copy the packed value, exponent last',
          align=Align.INLINE)
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
d.comment(0xa3c8, 'Packed mantissa MSB holds the sign in bit 7',
          align=Align.INLINE)
d.comment(0xa3ca, 'next byte', align=Align.INLINE)
d.comment(0xa3cb, 'byte 0...', align=Align.INLINE)
d.comment(0xa3cd, '...is the exponent', align=Align.INLINE)
d.comment(0xa3cf, 'Clear the rounding and overflow bytes (Y=0)',
          align=Align.INLINE)
d.comment(0xa3d1, 'clear the overflow byte too', align=Align.INLINE)
d.comment(0xa3d3, 'A=exponent; OR the mantissa to test for zero',
          align=Align.INLINE)
d.comment(0xa3d5, '(mantissa byte 2)', align=Align.INLINE)
d.comment(0xa3d7, '(mantissa byte 3)', align=Align.INLINE)
d.comment(0xa3d9, '(mantissa byte 4)', align=Align.INLINE)
d.comment(0xa3db, 'All zero: leave the mantissa MSB clear',
          align=Align.INLINE)
d.comment(0xa3dd, 'Non-zero: take the packed MSB (carrying the sign)',
          align=Align.INLINE)
d.comment(0xa3df, 'Non-zero: restore the implied leading 1',
          align=Align.INLINE)

d.comment(0xa3e1, 'Store the true mantissa MSB', align=Align.INLINE)
d.label(0xa3e1, 'fwa_unpack_msb')
d.comment(0xa3e3, 'FWA now holds the unpacked value', align=Align.INLINE)

d.subroutine(
    0xa3e4, 'fwa_to_int',
    title='Convert the FP accumulator to an integer',
    description='Convert FWA to a 4-byte integer in IWA by denormalising '
                '(fwa_to_int2) and copying the mantissa into IWA. Truncates '
                'toward zero.',
    on_entry={'zp_fwa (&2E-&35)': 'the real to convert'},
    on_exit={'zp_iwa (&2A-&2D)': 'the integer part of FWA',
             'zp_fwb (&3B-&42)': 'corrupted (holds the fraction)'},
)
# fwa_to_int (&A3E4): convert FWA real to the integer accumulator.
d.comment(0xa3e4, 'Denormalise FWA to a fixed integer', align=Align.INLINE)
d.comment(0xa3e7, 'Copy the 32-bit mantissa into IWA: byte 3', align=Align.INLINE)
# fwa_to_int / fwa_to_int2
d.label(0xa3e7, 'mantissa_to_iwa')
d.comment(0xa3e9, 'store it', align=Align.INLINE)
d.comment(0xa3eb, 'byte 2', align=Align.INLINE)
d.comment(0xa3ed, 'store it', align=Align.INLINE)
d.comment(0xa3ef, 'byte 1', align=Align.INLINE)
d.comment(0xa3f1, 'store it', align=Align.INLINE)
d.comment(0xa3f3, 'byte 0', align=Align.INLINE)
d.comment(0xa3f5, 'store it', align=Align.INLINE)
d.comment(0xa3f7, 'Return', align=Align.INLINE)
d.comment(0xa3f8, '|x| < 1: FWB = FWA', align=Align.INLINE)
d.label(0xa3f8, 'fti_small')
d.comment(0xa3fb, 'integer is zero', align=Align.INLINE)

d.subroutine(
    0xa3fe, 'fwa_to_int2',
    title='Denormalise FWA to a fixed-point integer',
    description='Shift the FWA mantissa so it represents the integer part at a '
                'fixed scale (exponent &A0), pushing the fractional bits out into '
                'FWB. The shared core of fwa_to_int and fp_split_int_frac; the '
                'caller reads the integer from the mantissa.',
    on_entry={'zp_fwa (&2E-&35)': 'the real to convert'},
    on_exit={'zp_fwa (&31-&34)': 'the integer part in the mantissa',
             'zp_fwb (&3B-&42)': 'the fractional bits shifted out'},
)
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
d.label(0xa40c, 'fti2_exp')
d.comment(0xa40e, 'already a 32-bit integer (exp = +32)?', align=Align.INLINE)
d.comment(0xa410, 'yes: check it fits', align=Align.INLINE)
d.comment(0xa412, 'within a byte-shift of integer?', align=Align.INLINE)
d.comment(0xa414, 'yes: finish with bit shifts', align=Align.INLINE)
d.comment(0xa416, 'Fast path: shift right one byte (exp += 8)',
          align=Align.INLINE)
d.comment(0xa418, '(store)', align=Align.INLINE)
d.comment(0xa41a, 'shift the mantissa down a byte, low byte into FWB',
          align=Align.INLINE)
d.comment(0xa41c, 'into fwb m4,', align=Align.INLINE)
d.comment(0xa41e, 'm2...', align=Align.INLINE)
d.comment(0xa420, 'into fwb m3,', align=Align.INLINE)
d.comment(0xa422, 'm1...', align=Align.INLINE)
d.comment(0xa424, 'into fwb m2,', align=Align.INLINE)
d.comment(0xa426, 'fwa m4...', align=Align.INLINE)
d.comment(0xa428, 'into fwb m1,', align=Align.INLINE)
d.comment(0xa42a, 'm3...', align=Align.INLINE)
d.comment(0xa42c, 'into fwa m4,', align=Align.INLINE)
d.comment(0xa42e, 'm2...', align=Align.INLINE)
d.comment(0xa430, 'into fwa m3,', align=Align.INLINE)
d.comment(0xa432, 'm1...', align=Align.INLINE)
d.comment(0xa434, 'into fwa m2,', align=Align.INLINE)
d.comment(0xa436, 'zero...', align=Align.INLINE)
d.comment(0xa438, 'into fwa m1 (top)', align=Align.INLINE)
d.comment(0xa43a, 'loop', align=Align.INLINE)
d.comment(0xa43c, 'Slow path: shift FWA:FWB right one bit', align=Align.INLINE)
d.label(0xa43c, 'fti2_shift_loop')
d.comment(0xa43e, 'through fwa m2,', align=Align.INLINE)
d.comment(0xa440, 'm3,', align=Align.INLINE)
d.comment(0xa442, 'm4,', align=Align.INLINE)
d.comment(0xa444, 'then fwb m1,', align=Align.INLINE)
d.comment(0xa446, 'm2,', align=Align.INLINE)
d.comment(0xa448, 'm3,', align=Align.INLINE)
d.comment(0xa44a, 'm4', align=Align.INLINE)
d.comment(0xa44c, 'exp += 1', align=Align.INLINE)
d.comment(0xa44e, 'loop until an exact integer', align=Align.INLINE)
d.comment(0xa450, 'Magnitude too large: Too big error', align=Align.INLINE)

d.label(0xa450, 'fti2_too_big')
# FWB helpers.
d.subroutine(0xa453, 'fwb_clear', title='FWB = 0',
             description='Zero every byte of FWB. Exponent 0 is the special '
                         'encoding for the value zero.',
             on_exit={'zp_fwb (&3B-&42)': '0.0', 'A': '0',
                      'X': 'preserved', 'Y': 'preserved'})
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
d.label(0xa466, 'fti2_exp_over')
d.comment(0xa468, 'Positive: integer ready, return', align=Align.INLINE)
d.label(0xa468, 'fti2_positive')
d.comment(0xa46a, 'positive: nothing to do', align=Align.INLINE)
d.comment(0xa46c, 'Negative: negate the 32-bit mantissa', align=Align.INLINE)
d.label(0xa46c, 'fti2_negate')
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

d.comment(0xa485, 'Return', align=Align.INLINE)
d.subroutine(0xa486, 'fp_split_int_frac',
             title='Split FWA into integer part (&4A) and fraction (FWA)',
             description='Round FWA to the nearest integer, leaving that '
                         'integer in &4A and the signed remainder (in '
                         '[-0.5, 0.5]) in FWA. Used by EXP to separate the '
                         'integer and fractional powers.',
             on_entry={'zp_fwa (&2E-&35)': 'the value to split'},
             on_exit={'(&4A)': 'the integer part (low byte)',
                      'zp_fwa (&2E-&35)': 'the signed fraction in [-0.5, 0.5]',
                      'zp_fwb (&3B-&42)': 'corrupted (scratch)'})
# fp_split_int_frac (&A486): integer part -> &4A, fraction -> FWA.
d.comment(0xa486, 'Exponent of FWA', align=Align.INLINE)
d.comment(0xa488, '|x| >= 1: has an integer part', align=Align.INLINE)
d.comment(0xa48a, '|x| < 1: integer part is zero', align=Align.INLINE)
d.comment(0xa48c, 'store it', align=Align.INLINE)
d.comment(0xa48e, 'return the fraction (= x)', align=Align.INLINE)
d.comment(0xa491, 'Convert to a fixed integer (fraction into FWB)',
          align=Align.INLINE)
# fp_split_int_frac
d.label(0xa491, 'sif_convert')
d.comment(0xa494, 'Low byte of the integer part...', align=Align.INLINE)
d.comment(0xa496, '...kept in &4A', align=Align.INLINE)
d.comment(0xa498, 'Bring the fractional bits back into FWA', align=Align.INLINE)
d.comment(0xa49b, 'Exponent for a value in [0,1)', align=Align.INLINE)
d.comment(0xa49d, 'set it', align=Align.INLINE)
d.comment(0xa49f, 'Top fraction bit set (fraction >= 0.5)?', align=Align.INLINE)
d.comment(0xa4a1, 'no: fraction already in range', align=Align.INLINE)
d.comment(0xa4a3, 'Round to nearest: flip the fraction sign', align=Align.INLINE)
d.comment(0xa4a5, 'store it back', align=Align.INLINE)
d.comment(0xa4a7, 'remainder positive: round the integer down', align=Align.INLINE)
d.comment(0xa4a9, 'remainder negative: round the integer up', align=Align.INLINE)
d.comment(0xa4ab, 'done: go negate the remainder', align=Align.INLINE)
d.comment(0xa4ae, 'negative: round the integer part down', align=Align.INLINE)
d.label(0xa4ae, 'sif_round_down')
d.comment(0xa4b0, 'Negate the fraction mantissa', align=Align.INLINE)
d.label(0xa4b0, 'sif_negate_frac')
d.comment(0xa4b3, 'Normalise the fraction', align=Align.INLINE)
d.label(0xa4b3, 'sif_normalise_frac')
d.comment(0xa4b6, 'Increment the integer-part mantissa (carry up)',
          align=Align.INLINE)
d.label(0xa4b6, 'inc_int_mantissa')
d.comment(0xa4b8, 'done if byte 4 did not wrap', align=Align.INLINE)
d.comment(0xa4ba, 'wrapped: carry into byte 3,', align=Align.INLINE)
d.comment(0xa4bc, 'done if no wrap', align=Align.INLINE)
d.comment(0xa4be, 'byte 2,', align=Align.INLINE)
d.comment(0xa4c0, 'done if no wrap', align=Align.INLINE)
d.comment(0xa4c2, 'byte 1 (top)', align=Align.INLINE)
d.comment(0xa4c4, 'overflow: Too big', align=Align.INLINE)
d.comment(0xa4c6, 'Return', align=Align.INLINE)
d.comment(0xa4c7, 'Decrement the mantissa magnitude (negate, +1, negate)',
          align=Align.INLINE)
d.label(0xa4c7, 'negate_mantissa')

d.comment(0xa4ca, 'add one to the magnitude', align=Align.INLINE)
d.comment(0xa4cd, 'negate back', align=Align.INLINE)

d.subroutine(0xa4d0, 'fwa_sub_var', title='FWA = FWA - fp var',
             description='Subtract the packed real operand from FWA: compute '
                         'operand - FWA (fwa_rsub_var) then negate the result.',
             on_entry={'zp_fwa (&2E-&35)': 'the minuend',
                       '(zp_fp_ptr) (&4B/&4C)': 'the packed real subtrahend'},
             on_exit={'zp_fwa (&2E-&35)': 'FWA - operand',
                      'zp_fwb (&3B-&42)': 'corrupted (scratch)'})
# fwa_sub_var (&A4D0): FWA = FWA - operand.
d.comment(0xa4d0, 'operand - FWA...', align=Align.INLINE)
d.comment(0xa4d3, '...then negate to give FWA - operand', align=Align.INLINE)

d.subroutine(0xa4d6, 'fwa_swap_var', title='Swap FWA and a fp variable',
             description='Exchange FWA with the packed real at zp_fp_ptr: unpack '
                         'the operand into FWB, pack FWA into the variable, then '
                         'copy FWB into FWA.',
             on_entry={'zp_fwa (&2E-&35)': 'the accumulator value',
                       '(zp_fp_ptr) (&4B/&4C)': 'the packed real variable'},
             on_exit={'zp_fwa (&2E-&35)': 'the former variable value',
                      '(zp_fp_ptr)': 'the former FWA value',
                      'zp_fwb (&3B-&42)': 'corrupted (scratch)'})
# fwa_swap_var (&A4D6): exchange FWA with the fp variable
d.comment(0xa4d6, 'FWB = the fp variable', align=Align.INLINE)
d.comment(0xa4d9, 'Store FWA into the variable; FWA = old variable', align=Align.INLINE)
d.subroutine(0xa4dc, 'fwa_copy_from_fwb', title='FWA = FWB',
             description='Copy all ten bytes of FWB into FWA.',
             on_entry={'zp_fwb (&3B-&42)': 'the floating-point accumulator B'},
             on_exit={'zp_fwa (&2E-&35)': 'a copy of FWB', 'X': 'preserved'})
# fwa_copy_from_fwb (&A4DC): FWA = FWB
d.comment(0xa4dc, "Copy FWB's sign...", align=Align.INLINE)
d.comment(0xa4de, '...into FWA', align=Align.INLINE)
d.comment(0xa4e0, 'Copy the overflow byte...', align=Align.INLINE)
d.comment(0xa4e2, '...into FWA', align=Align.INLINE)
d.comment(0xa4e4, 'Copy the exponent...', align=Align.INLINE)
d.comment(0xa4e6, '...into FWA', align=Align.INLINE)
d.comment(0xa4e8, 'Copy mantissa byte 1...', align=Align.INLINE)
d.label(0xa4e8, 'copy_fwb_mantissa')
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

d.subroutine(0xa4fd, 'fwa_rsub_var', title='FWA = fp var - FWA',
             description='Reverse subtract: negate FWA then add the packed real '
                         'operand, giving operand - FWA (normalised, rounded).',
             on_entry={'zp_fwa (&2E-&35)': 'the subtrahend',
                       '(zp_fp_ptr) (&4B/&4C)': 'the packed real operand'},
             on_exit={'zp_fwa (&2E-&35)': 'operand - FWA',
                      'zp_fwb (&3B-&42)': 'corrupted (scratch)'})
# fwa_rsub_var / fwa_add_fwb / fwa_mul_var / fwa_reciprocal (wrappers)
d.comment(0xa4fd, 'Negate FWA, then add the variable: var - FWA', align=Align.INLINE)
# Add / subtract.
d.subroutine(0xa500, 'fwa_add_var', title='FWA = FWA + fp var',
             description='Unpack the packed real operand into FWB and add it to '
                         'FWA (normalised, rounded).',
             on_entry={'zp_fwa (&2E-&35)': 'the augend',
                       '(zp_fp_ptr) (&4B/&4C)': 'the packed real operand'},
             on_exit={'zp_fwa (&2E-&35)': 'the sum',
                      'zp_fwb (&3B-&42)': 'corrupted (scratch)'})
# fwa_add_var (&A500): FWA = FWA + fp variable
d.comment(0xa500, 'FWB = the fp variable', align=Align.INLINE)
d.comment(0xa503, 'Adding zero leaves FWA unchanged', align=Align.INLINE)
d.subroutine(0xa505, 'fwa_add_fwb', title='FWA = FWA + FWB',
             description='Add FWB to FWA (fwa_add_fwb_raw then fwa_round), '
                         'normalised and rounded.',
             on_entry={'zp_fwa (&2E-&35)': 'the augend',
                       'zp_fwb (&3B-&42)': 'the addend'},
             on_exit={'zp_fwa (&2E-&35)': 'the rounded sum'})
d.comment(0xa505, 'FWA = FWA + FWB (raw)', align=Align.INLINE)
d.comment(0xa508, 'then round', align=Align.INLINE)
d.subroutine(0xa50b, 'fwa_add_fwb_raw', title='FWA = FWA + FWB (unrounded)',
             description='Add FWB to FWA: align the smaller operand to the '
                         'larger exponent, add the mantissas and normalise. Left '
                         'unrounded (the caller rounds). Operands differing by '
                         '>= 37 bits leave FWA unchanged.',
             on_entry={'zp_fwa (&2E-&35)': 'the augend',
                       'zp_fwb (&3B-&42)': 'the addend'},
             on_exit={'zp_fwa (&2E-&35)': 'the sum, normalised but unrounded'})
d.comment(0xa50b, 'Is FWA zero?', align=Align.INLINE)
d.comment(0xa50e, 'FWA is zero: the sum is simply FWB', align=Align.INLINE)
# fwa_add_fwb_raw (&A50B) remaining: alignment shifts and add/subtract
d.comment(0xa510, 'Y = 0 (the byte shifted in)', align=Align.INLINE)
d.comment(0xa512, 'prepare the exponent compare', align=Align.INLINE)
d.comment(0xa513, 'FWA exponent...', align=Align.INLINE)
d.comment(0xa515, 'Exponent difference is the alignment shift',
          align=Align.INLINE)
d.comment(0xa517, 'Equal exponents: already aligned', align=Align.INLINE)
d.comment(0xa519, 'FWA the smaller: align it to FWB instead',
          align=Align.INLINE)
d.comment(0xa51b, 'differ by >= 37 bits?', align=Align.INLINE)
d.comment(0xa51d, 'Differ by >= 37 bits: FWB too small to count',
          align=Align.INLINE)
d.comment(0xa51f, 'save the shift count', align=Align.INLINE)
d.comment(0xa520, 'Whole-byte part of the shift (difference / 8)',
          align=Align.INLINE)
d.comment(0xa522, 'no whole-byte shift: go to the bit shift', align=Align.INLINE)
d.comment(0xa524, 'shift count / 8...', align=Align.INLINE)
d.comment(0xa525, '(continued)', align=Align.INLINE)
d.comment(0xa526, '= whole-byte shifts', align=Align.INLINE)
d.comment(0xa527, 'X = byte-shift count', align=Align.INLINE)
d.comment(0xa528, 'Shift FWB down a byte at a time', align=Align.INLINE)
# fwa_add_fwb_raw (exponent align + add)
d.label(0xa528, 'addf_shift_fwb_byte')
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
d.label(0xa53d, 'addf_fwb_bits')
d.comment(0xa53e, 'then the remaining bits, to finish aligning FWB',
          align=Align.INLINE)
d.comment(0xa540, 'no bit shift: add the mantissas', align=Align.INLINE)
d.comment(0xa542, 'X = bit-shift count', align=Align.INLINE)
d.comment(0xa543, 'shift FWB right one bit: m1', align=Align.INLINE)
d.label(0xa543, 'addf_shift_fwb_bit')
d.comment(0xa545, 'm2', align=Align.INLINE)
d.comment(0xa547, 'm3', align=Align.INLINE)
d.comment(0xa549, 'm4', align=Align.INLINE)
d.comment(0xa54b, 'rnd', align=Align.INLINE)
d.comment(0xa54d, 'count', align=Align.INLINE)
d.comment(0xa54e, 'loop', align=Align.INLINE)
d.comment(0xa550, 'aligned: add the mantissas', align=Align.INLINE)
d.comment(0xa552, 'FWA the smaller: shift FWA down to align', align=Align.INLINE)
d.label(0xa552, 'addf_align_fwa')
d.comment(0xa553, 'FWB exponent - FWA exponent', align=Align.INLINE)
d.comment(0xa555, 'minus FWA exponent', align=Align.INLINE)
d.comment(0xa557, 'differ by >= 37 bits?', align=Align.INLINE)
d.comment(0xa559, 'FWA negligible: result is FWB', align=Align.INLINE)
d.comment(0xa55b, 'save the shift count', align=Align.INLINE)
d.comment(0xa55c, 'whole-byte part', align=Align.INLINE)
d.comment(0xa55e, 'none: go to the bit shift', align=Align.INLINE)
d.comment(0xa560, '/ 8...', align=Align.INLINE)
d.comment(0xa561, '(continued)', align=Align.INLINE)
d.comment(0xa562, '= whole-byte shifts', align=Align.INLINE)
d.comment(0xa563, 'X = byte-shift count', align=Align.INLINE)
d.comment(0xa564, 'shift FWA down a byte: m4 -> rnd', align=Align.INLINE)
d.label(0xa564, 'addf_shift_fwa_byte')
d.comment(0xa566, '(store)', align=Align.INLINE)
d.comment(0xa568, 'm3 -> m4', align=Align.INLINE)
d.comment(0xa56a, '(store)', align=Align.INLINE)
d.comment(0xa56c, 'm2 -> m3', align=Align.INLINE)
d.comment(0xa56e, '(store)', align=Align.INLINE)
d.comment(0xa570, 'm1 -> m2', align=Align.INLINE)
d.comment(0xa572, '(store)', align=Align.INLINE)
d.comment(0xa574, 'm1 = 0', align=Align.INLINE)
d.comment(0xa576, 'count', align=Align.INLINE)
d.comment(0xa577, 'loop', align=Align.INLINE)
d.comment(0xa579, 'recover the shift count', align=Align.INLINE)
d.label(0xa579, 'addf_fwa_bits')
d.comment(0xa57a, 'bit part', align=Align.INLINE)
d.comment(0xa57c, 'none: take the larger exponent', align=Align.INLINE)
d.comment(0xa57e, 'X = bit-shift count', align=Align.INLINE)
d.comment(0xa57f, 'shift FWA right one bit: m1', align=Align.INLINE)
d.label(0xa57f, 'addf_shift_fwa_bit')
d.comment(0xa581, 'm2', align=Align.INLINE)
d.comment(0xa583, 'm3', align=Align.INLINE)
d.comment(0xa585, 'm4', align=Align.INLINE)
d.comment(0xa587, 'rnd', align=Align.INLINE)
d.comment(0xa589, 'count', align=Align.INLINE)
d.comment(0xa58a, 'loop', align=Align.INLINE)
d.comment(0xa58c, 'Result takes the larger exponent', align=Align.INLINE)
d.label(0xa58c, 'addf_take_exp')
d.comment(0xa58e, 'store the larger exponent', align=Align.INLINE)
d.comment(0xa590, 'Compare the signs: load FWA sign', align=Align.INLINE)
d.label(0xa590, 'addf_compare_signs')
d.comment(0xa592, 'Compare the operand signs', align=Align.INLINE)
d.comment(0xa594, 'Same sign: add; opposite: subtract smaller from larger',
          align=Align.INLINE)
d.comment(0xa596, 'Opposite signs: compare magnitudes (m1)', align=Align.INLINE)
d.comment(0xa598, 'against FWB', align=Align.INLINE)
d.comment(0xa59a, 'differ: subtract', align=Align.INLINE)
d.comment(0xa59c, 'm2', align=Align.INLINE)
d.comment(0xa59e, 'against FWB', align=Align.INLINE)
d.comment(0xa5a0, 'differ: subtract', align=Align.INLINE)
d.comment(0xa5a2, 'm3', align=Align.INLINE)
d.comment(0xa5a4, 'against FWB', align=Align.INLINE)
d.comment(0xa5a6, 'differ: subtract', align=Align.INLINE)
d.comment(0xa5a8, 'm4', align=Align.INLINE)
d.comment(0xa5aa, 'against FWB', align=Align.INLINE)
d.comment(0xa5ac, 'differ: subtract', align=Align.INLINE)
d.comment(0xa5ae, 'rnd', align=Align.INLINE)
d.comment(0xa5b0, 'against FWB', align=Align.INLINE)
d.comment(0xa5b2, 'differ: subtract', align=Align.INLINE)
d.comment(0xa5b4, 'Equal magnitudes of opposite sign cancel to zero',
          align=Align.INLINE)

d.label(0xa5b7, 'fp_mantissas_sub')   # opposite-sign path: subtract
d.comment(0xa5b7, 'FWA >= FWB? choose the subtraction order', align=Align.INLINE)
d.comment(0xa5b9, 'FWB - FWA: rnd', align=Align.INLINE)
d.comment(0xa5ba, 'FWB rnd...', align=Align.INLINE)
d.comment(0xa5bc, '- FWA rnd,', align=Align.INLINE)
d.comment(0xa5be, '(store)', align=Align.INLINE)
d.comment(0xa5c0, 'm4', align=Align.INLINE)
d.comment(0xa5c2, '- FWA m4,', align=Align.INLINE)
d.comment(0xa5c4, '(store)', align=Align.INLINE)
d.comment(0xa5c6, 'm3', align=Align.INLINE)
d.comment(0xa5c8, '- FWA m3,', align=Align.INLINE)
d.comment(0xa5ca, '(store)', align=Align.INLINE)
d.comment(0xa5cc, 'm2', align=Align.INLINE)
d.comment(0xa5ce, '- FWA m2,', align=Align.INLINE)
d.comment(0xa5d0, '(store)', align=Align.INLINE)
d.comment(0xa5d2, 'm1', align=Align.INLINE)
d.comment(0xa5d4, '- FWA m1', align=Align.INLINE)
d.comment(0xa5d6, '(store)', align=Align.INLINE)
d.comment(0xa5d8, 'result takes FWB\'s sign', align=Align.INLINE)
d.comment(0xa5da, '(store)', align=Align.INLINE)
d.comment(0xa5dc, 'normalise the difference', align=Align.INLINE)
# --- floating-point addition (FWA = FWA + FWB) -----------------------
# Align the two operands by the difference of their exponents (shifting
# the smaller mantissa right), then add the mantissas if the signs
# match or subtract the smaller from the larger if they differ.
d.label(0xa5df, 'fp_mantissas_add')   # same-sign path: add the mantissas
d.comment(0xa5df, 'Same sign: add the mantissas', align=Align.INLINE)
d.comment(0xa5e0, 'FWA += FWB', align=Align.INLINE)
d.comment(0xa5e3, 'FWA - FWB: rnd', align=Align.INLINE)
d.label(0xa5e3, 'addf_subtract')
d.comment(0xa5e4, 'FWA rnd...', align=Align.INLINE)
d.comment(0xa5e6, '- FWB rnd,', align=Align.INLINE)
d.comment(0xa5e8, '(store)', align=Align.INLINE)
d.comment(0xa5ea, 'm4', align=Align.INLINE)
d.comment(0xa5ec, '- FWB m4,', align=Align.INLINE)
d.comment(0xa5ee, '(store)', align=Align.INLINE)
d.comment(0xa5f0, 'm3', align=Align.INLINE)
d.comment(0xa5f2, '- FWB m3,', align=Align.INLINE)
d.comment(0xa5f4, '(store)', align=Align.INLINE)
d.comment(0xa5f6, 'm2', align=Align.INLINE)
d.comment(0xa5f8, '- FWB m2,', align=Align.INLINE)
d.comment(0xa5fa, '(store)', align=Align.INLINE)
d.comment(0xa5fc, 'm1', align=Align.INLINE)
d.comment(0xa5fe, '- FWB m1,', align=Align.INLINE)
d.comment(0xa600, '(store)', align=Align.INLINE)
d.comment(0xa602, 'normalise the difference', align=Align.INLINE)
d.comment(0xa605, 'Return', align=Align.INLINE)
d.subroutine(0xa606, 'fwa_mul_var_raw', title='FWA = FWA * fp var (raw)',
             description='Multiply FWA by the packed real operand (sign XOR, '
                         'exponents added, mantissas multiplied by shift-and-add). '
                         'A zero operand gives zero. Left unnormalised and '
                         'unrounded (the caller finishes).',
             on_entry={'zp_fwa (&2E-&35)': 'the multiplicand',
                       '(zp_fp_ptr) (&4B/&4C)': 'the packed real multiplier'},
             on_exit={'zp_fwa (&2E-&35)': 'the product, unnormalised',
                      'zp_fwb (&3B-&42)': 'corrupted (scratch)'})
# fwa_mul_var_raw (&A606): FWA = FWA * fp variable (shift-and-add)
d.comment(0xa606, 'Is FWA zero?', align=Align.INLINE)
d.comment(0xa609, 'zero: the product is zero', align=Align.INLINE)
d.comment(0xa60b, 'FWB = the fp variable (the multiplier)', align=Align.INLINE)
d.comment(0xa60e, 'non-zero: multiply', align=Align.INLINE)
d.comment(0xa610, 'multiplier zero: the product is zero', align=Align.INLINE)
d.comment(0xa613, 'Add the exponents:', align=Align.INLINE)
# fwa_mul_var_raw / fwa_mul_var
d.label(0xa613, 'mulf_add_exp')
d.comment(0xa614, 'FWA exp...', align=Align.INLINE)
d.comment(0xa616, '+ FWB exp', align=Align.INLINE)
d.comment(0xa618, 'no carry', align=Align.INLINE)
d.comment(0xa61a, 'carry into overflow', align=Align.INLINE)
d.comment(0xa61c, '(clear carry)', align=Align.INLINE)
d.comment(0xa61d, 'remove the excess-128 bias (added twice)', align=Align.INLINE)
d.label(0xa61d, 'mulf_unbias')
d.comment(0xa61f, 'store the product exponent', align=Align.INLINE)
d.comment(0xa621, 'no borrow', align=Align.INLINE)
d.comment(0xa623, 'borrow into overflow', align=Align.INLINE)
d.comment(0xa625, 'Move FWA aside as the multiplicand and clear FWA:', align=Align.INLINE)
d.label(0xa625, 'mulf_setup')
d.comment(0xa627, 'Y = 0 (to clear FWA with)', align=Align.INLINE)
d.comment(0xa629, 'copy a FWA byte...', align=Align.INLINE)
d.label(0xa629, 'mulf_copy_loop')
d.comment(0xa62b, '...to the multiplicand', align=Align.INLINE)
d.comment(0xa62d, 'clear the FWA byte', align=Align.INLINE)
d.comment(0xa62f, 'count', align=Align.INLINE)
d.comment(0xa630, 'loop', align=Align.INLINE)
d.comment(0xa632, 'Product sign = FWA sign XOR FWB sign:', align=Align.INLINE)
d.comment(0xa634, 'XOR FWB sign', align=Align.INLINE)
d.comment(0xa636, '(store)', align=Align.INLINE)
d.comment(0xa638, '32 iterations, one per multiplier bit', align=Align.INLINE)
d.comment(0xa63a, 'Shift the multiplier right: next bit into carry', align=Align.INLINE)
d.label(0xa63a, 'mulf_bit_loop')
d.comment(0xa63c, 'm2,', align=Align.INLINE)
d.comment(0xa63e, 'm3,', align=Align.INLINE)
d.comment(0xa640, 'm4,', align=Align.INLINE)
d.comment(0xa642, 'rnd', align=Align.INLINE)
d.comment(0xa644, 'Shift the running product left (&43-&46):', align=Align.INLINE)
d.comment(0xa646, 'through &45,', align=Align.INLINE)
d.comment(0xa648, '&44,', align=Align.INLINE)
d.comment(0xa64a, '&43 (high)', align=Align.INLINE)
d.comment(0xa64c, 'multiplier bit clear: skip the add', align=Align.INLINE)
d.comment(0xa64e, 'bit set: add the multiplicand', align=Align.INLINE)
d.comment(0xa64f, 'FWA += FWB', align=Align.INLINE)
d.comment(0xa652, 'count', align=Align.INLINE)
d.label(0xa652, 'mulf_count')
d.comment(0xa653, 'loop', align=Align.INLINE)
d.comment(0xa655, 'Return the product', align=Align.INLINE)

# Multiply / divide.
d.subroutine(0xa656, 'fwa_mul_var', title='FWA = FWA * fp var',
             description='Multiply FWA by the packed real operand '
                         '(fwa_mul_var_raw then normalise and round).',
             on_entry={'zp_fwa (&2E-&35)': 'the multiplicand',
                       '(zp_fp_ptr) (&4B/&4C)': 'the packed real multiplier'},
             on_exit={'zp_fwa (&2E-&35)': 'the product, normalised and rounded',
                      'zp_fwb (&3B-&42)': 'corrupted (scratch)'})
d.comment(0xa656, 'FWA = FWA * fp var (raw)', align=Align.INLINE)
d.comment(0xa659, 'normalise (round below)', align=Align.INLINE)
d.label(0xa659, 'mulf_normalise')
d.subroutine(0xa65c, 'fwa_round', title='Round FWA',
             description='Round FWA to the mantissa LSB using the rounding byte: '
                         'round to nearest, ties handled by the LSB. A carry out '
                         'of the top renormalises and can raise Too big.',
             on_entry={'zp_fwa (&2E-&35)': 'the value to round (rnd byte holds '
                                           'the bits below the LSB)'},
             on_exit={'zp_fwa (&2E-&34)': 'the rounded value',
                      'BRK': 'Too big on overflow'})
# --- fwa_round: round FWA using the rounding byte ---------------------
d.comment(0xa65c, 'The rounding byte holds the bits below the LSB',
          align=Align.INLINE)
# fwa_round (&A65C) remaining
d.comment(0xa65e, 'compare with half (&80)', align=Align.INLINE)
d.comment(0xa660, 'Below half: round down (truncate)', align=Align.INLINE)
d.comment(0xa662, 'Exactly half: special-case the LSB', align=Align.INLINE)
d.comment(0xa664, 'Above half: round up by adding 1', align=Align.INLINE)
d.comment(0xa666, 'add 1 via the carry ripple', align=Align.INLINE)
d.comment(0xa669, 'then finish', align=Align.INLINE)
d.label(0xa66c, 'err_too_big')   # BRK error block: "Too big"
d.comment(0xa66c, 'BRK error block: "Too big"', align=Align.INLINE)
d.comment(0xa676, 'Exactly half: force the mantissa LSB', align=Align.INLINE)
# fwa_round / fwa_rdiv_var
d.label(0xa676, 'round_half')
d.comment(0xa678, 'set the LSB', align=Align.INLINE)
d.comment(0xa67a, '(store)', align=Align.INLINE)
d.comment(0xa67c, 'Clear the now-spent rounding byte', align=Align.INLINE)
d.label(0xa67c, 'round_clear')
d.comment(0xa67e, 'clear the rounding byte', align=Align.INLINE)
d.comment(0xa680, 'A carry may have overflowed the mantissa', align=Align.INLINE)
d.comment(0xa682, 'no overflow: done', align=Align.INLINE)

d.comment(0xa684, 'Overflowed the exponent range: Too big', align=Align.INLINE)

# ----------------------------------------------------------------------
# Floating-point arithmetic (Pharo ch. 3). BBC BASIC keeps reals in two
# accumulators: FWA (zp_fwa, &2E-&35) and FWB (zp_fwb, &3B-&42), in an
# unpacked work form; values are stored packed (5 bytes). Routines that
# take a "fp var" operand expect (&4B/&4C) to point at it. These are
# the primitives the maths functions and real arithmetic build on.
# ----------------------------------------------------------------------
d.subroutine(0xa686, 'fwa_clear', title='FWA = 0',
             description='Zero every byte of FWA. Exponent 0 is the special '
                         'encoding for the value zero.',
             on_exit={'zp_fwa (&2E-&35)': '0.0', 'A': '0',
                      'X': 'preserved', 'Y': 'preserved'})
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

d.subroutine(0xa699, 'fwa_set_one', title='FWA = 1',
             description='Set the floating-point accumulator to 1.0 (mantissa MSB '
                         '&80, exponent &81).',
             on_exit={'zp_fwa (&2E-&35)': '1.0',
                      'A': 'nonzero (flags a real result)'})
# fwa_set_one (&A699): FWA = 1.0
d.comment(0xa699, 'Start from 0.0', align=Align.INLINE)
d.comment(0xa69c, 'Mantissa MSB &80 is the implied leading 1', align=Align.INLINE)
d.comment(0xa69e, 'Set mantissa byte 1', align=Align.INLINE)
d.comment(0xa6a0, 'Y = &81', align=Align.INLINE)
d.comment(0xa6a1, 'Exponent &81 makes the value exactly 1.0', align=Align.INLINE)
d.comment(0xa6a3, 'Return non-zero (A = exponent) to flag a real', align=Align.INLINE)
d.comment(0xa6a4, 'FWA now holds 1.0', align=Align.INLINE)

d.subroutine(0xa6a5, 'fwa_reciprocal', title='FWA = 1 / FWA',
             description='Reciprocal: save FWA in TEMP1, set FWA = 1, then divide '
                         'by the saved value (normalised, rounded). Raises '
                         'Division by zero if FWA was zero.',
             on_entry={'zp_fwa (&2E-&35)': 'the value to invert'},
             on_exit={'zp_fwa (&2E-&35)': '1 / FWA',
                      '(&046C)': 'corrupted (TEMP1 scratch)',
                      'BRK': 'Division by zero if FWA was zero'})
d.comment(0xa6a5, 'Save FWA (the divisor) in TEMP1', align=Align.INLINE)
d.comment(0xa6a8, 'FWA = 1', align=Align.INLINE)
d.comment(0xa6ab, 'divide 1 by the saved value', align=Align.INLINE)

d.subroutine(0xa6ad, 'fwa_rdiv_var', title='FWA = fp var / FWA',
             description='Reverse divide: copy FWA (the divisor) into FWB, unpack '
                         'the packed real operand (the dividend) into FWA, then '
                         'divide, giving operand / FWA. Raises Division by zero '
                         'if FWA is zero.',
             on_entry={'zp_fwa (&2E-&35)': 'the divisor',
                       '(zp_fp_ptr) (&4B/&4C)': 'the packed real dividend'},
             on_exit={'zp_fwa (&2E-&35)': 'operand / FWA',
                      'BRK': 'Division by zero if FWA was zero'})
# fwa_rdiv_var (&A6AD): FWA = fp var / FWA
d.comment(0xa6ad, 'Is FWA (the divisor) zero?', align=Align.INLINE)
d.comment(0xa6b0, 'yes: Division by zero', align=Align.INLINE)
d.comment(0xa6b2, 'FWB = FWA (the divisor)', align=Align.INLINE)
d.comment(0xa6b5, 'FWA = the fp variable (the dividend)', align=Align.INLINE)
d.comment(0xa6b8, 'non-zero: do the division', align=Align.INLINE)
d.comment(0xa6ba, 'dividend zero: result is zero', align=Align.INLINE)
d.comment(0xa6bb, 'Division by zero error', align=Align.INLINE)
d.label(0xa6bb, 'fp_div_zero')

# fn_tan (&A6BE): TAN = sin / cos
d.comment(0xa6be, 'Evaluate the argument as a real', align=Align.INLINE)
d.comment(0xa6c1, 'Compute the trig kernel', align=Align.INLINE)
d.comment(0xa6c4, 'save the quadrant', align=Align.INLINE)
d.comment(0xa6c6, 'push it', align=Align.INLINE)
d.comment(0xa6c7, 'save the first result (cos) in TEMP4', align=Align.INLINE)
d.comment(0xa6ca, 'pack FWA (cos) there', align=Align.INLINE)
d.comment(0xa6cd, 'shift the quadrant (cos -> sin)', align=Align.INLINE)
d.comment(0xa6cf, 'compute the other (sin)', align=Align.INLINE)
d.comment(0xa6d2, 'point at TEMP4', align=Align.INLINE)
d.comment(0xa6d5, 'swap FWA (sin) with TEMP4 (cos)', align=Align.INLINE)
d.comment(0xa6d8, 'restore the quadrant', align=Align.INLINE)
d.comment(0xa6d9, 'store it', align=Align.INLINE)
d.comment(0xa6db, 'finish the trig (cos in FWA)', align=Align.INLINE)
d.comment(0xa6de, 'point at TEMP4 (sin)', align=Align.INLINE)
d.comment(0xa6e1, 'TAN = sin / cos', align=Align.INLINE)
d.comment(0xa6e4, 'real result', align=Align.INLINE)
d.comment(0xa6e6, 'Return TAN', align=Align.INLINE)
d.subroutine(0xa6e7, 'fp_divide', title='FWA = FWA / divisor (restoring long division)',
             description='Floating-point divide of FWA by the packed real '
                         'divisor: sign XOR, exponents subtracted, then 32 '
                         'quotient bits plus guard bits by restoring long '
                         'division (compare/subtract/shift). Raises Division by '
                         'zero on a zero divisor; a zero dividend gives zero.',
             on_entry={'zp_fwa (&2E-&35)': 'the dividend',
                       '(zp_fp_ptr) (&4B/&4C)': 'the packed real divisor'},
             on_exit={'zp_fwa (&2E-&35)': 'the quotient',
                      'zp_fwb (&3B-&42)': 'corrupted (scratch)',
                      'BRK': 'Division by zero on a zero divisor'})

# fp_divide (&A6E7)
d.comment(0xa6e7, 'Is the dividend (FWA) zero?', align=Align.INLINE)
d.comment(0xa6ea, 'zero: result is zero', align=Align.INLINE)
d.comment(0xa6ec, 'unpack the divisor into FWB', align=Align.INLINE)
d.comment(0xa6ef, 'divisor zero: Division by zero', align=Align.INLINE)
d.comment(0xa6f1, 'result sign = sign XOR sign', align=Align.INLINE)
# fp_divide (restoring long division)
d.label(0xa6f1, 'div_signs')
d.comment(0xa6f3, 'XOR the divisor sign', align=Align.INLINE)
d.comment(0xa6f5, '(store)', align=Align.INLINE)
d.comment(0xa6f7, 'result exponent = dividend - divisor:', align=Align.INLINE)
d.comment(0xa6f8, 'dividend exp...', align=Align.INLINE)
d.comment(0xa6fa, 'minus divisor exp', align=Align.INLINE)
d.comment(0xa6fc, 'no borrow', align=Align.INLINE)
d.comment(0xa6fe, 'borrow into overflow', align=Align.INLINE)
d.comment(0xa700, '(set carry again)', align=Align.INLINE)
d.comment(0xa701, 're-bias the exponent', align=Align.INLINE)
d.label(0xa701, 'div_rebias')
d.comment(0xa703, '(store)', align=Align.INLINE)
d.comment(0xa705, 'no carry', align=Align.INLINE)
d.comment(0xa707, 'carry into overflow', align=Align.INLINE)
d.comment(0xa709, '(clear carry)', align=Align.INLINE)
d.comment(0xa70a, '32 quotient bits (restoring long division):', align=Align.INLINE)
d.label(0xa70a, 'div_quotient')
d.comment(0xa70c, 'remainder >= divisor?', align=Align.INLINE)
d.label(0xa70c, 'div_cmp1')
d.comment(0xa70e, 'compare FWA (remainder) with FWB (divisor):', align=Align.INLINE)
d.comment(0xa710, 'vs divisor m1,', align=Align.INLINE)
d.comment(0xa712, 'differ: decided', align=Align.INLINE)
d.comment(0xa714, 'else m2...', align=Align.INLINE)
d.comment(0xa716, 'vs m2,', align=Align.INLINE)
d.comment(0xa718, 'differ: decided', align=Align.INLINE)
d.comment(0xa71a, 'else m3...', align=Align.INLINE)
d.comment(0xa71c, 'vs m3,', align=Align.INLINE)
d.comment(0xa71e, 'differ: decided', align=Align.INLINE)
d.comment(0xa720, 'else m4...', align=Align.INLINE)
d.comment(0xa722, 'vs m4', align=Align.INLINE)
d.comment(0xa724, 'less: quotient bit 0', align=Align.INLINE)
d.label(0xa724, 'div_bit0_1')
d.comment(0xa726, 'subtract the divisor from the remainder:', align=Align.INLINE)
d.label(0xa726, 'div_sub1')
d.comment(0xa728, '- divisor m4,', align=Align.INLINE)
d.comment(0xa72a, '(store)', align=Align.INLINE)
d.comment(0xa72c, 'm3...', align=Align.INLINE)
d.comment(0xa72e, '- divisor m3,', align=Align.INLINE)
d.comment(0xa730, '(store)', align=Align.INLINE)
d.comment(0xa732, 'm2...', align=Align.INLINE)
d.comment(0xa734, '- divisor m2,', align=Align.INLINE)
d.comment(0xa736, '(store)', align=Align.INLINE)
d.comment(0xa738, 'm1...', align=Align.INLINE)
d.comment(0xa73a, '- divisor m1,', align=Align.INLINE)
d.comment(0xa73c, '(store)', align=Align.INLINE)
d.comment(0xa73e, 'quotient bit 1', align=Align.INLINE)
d.comment(0xa73f, 'shift the quotient left, bring in the bit:', align=Align.INLINE)
d.label(0xa73f, 'div_shift1')
d.comment(0xa741, 'through &45,', align=Align.INLINE)
d.comment(0xa743, '&44,', align=Align.INLINE)
d.comment(0xa745, '&43 (high)', align=Align.INLINE)
d.comment(0xa747, 'shift the remainder left:', align=Align.INLINE)
d.comment(0xa749, 'm3,', align=Align.INLINE)
d.comment(0xa74b, 'm2,', align=Align.INLINE)
d.comment(0xa74d, 'm1', align=Align.INLINE)
d.comment(0xa74f, 'count', align=Align.INLINE)
d.comment(0xa750, 'loop 32 times', align=Align.INLINE)
d.comment(0xa752, '7 guard bits:', align=Align.INLINE)
d.comment(0xa754, 'remainder >= divisor?', align=Align.INLINE)
d.label(0xa754, 'div_cmp2')
d.comment(0xa756, 'compare remainder vs divisor: m1...', align=Align.INLINE)
d.comment(0xa758, 'vs m1,', align=Align.INLINE)
d.comment(0xa75a, 'differ: decided', align=Align.INLINE)
d.comment(0xa75c, 'else m2...', align=Align.INLINE)
d.comment(0xa75e, 'vs m2,', align=Align.INLINE)
d.comment(0xa760, 'differ: decided', align=Align.INLINE)
d.comment(0xa762, 'else m3...', align=Align.INLINE)
d.comment(0xa764, 'vs m3,', align=Align.INLINE)
d.comment(0xa766, 'differ: decided', align=Align.INLINE)
d.comment(0xa768, 'else m4...', align=Align.INLINE)
d.comment(0xa76a, 'vs m4', align=Align.INLINE)
d.comment(0xa76c, 'less: bit 0', align=Align.INLINE)
d.label(0xa76c, 'div_bit0_2')
d.comment(0xa76e, 'subtract:', align=Align.INLINE)
d.label(0xa76e, 'div_sub2')
d.comment(0xa770, '- divisor m4,', align=Align.INLINE)
d.comment(0xa772, '(store)', align=Align.INLINE)
d.comment(0xa774, 'm3...', align=Align.INLINE)
d.comment(0xa776, '- divisor m3,', align=Align.INLINE)
d.comment(0xa778, '(store)', align=Align.INLINE)
d.comment(0xa77a, 'm2...', align=Align.INLINE)
d.comment(0xa77c, '- divisor m2,', align=Align.INLINE)
d.comment(0xa77e, '(store)', align=Align.INLINE)
d.comment(0xa780, 'm1...', align=Align.INLINE)
d.comment(0xa782, '- divisor m1,', align=Align.INLINE)
d.comment(0xa784, '(store)', align=Align.INLINE)
d.comment(0xa786, 'guard bit 1', align=Align.INLINE)
d.comment(0xa787, 'shift in the guard bit', align=Align.INLINE)
d.label(0xa787, 'div_shift2')
d.comment(0xa789, 'shift the remainder:', align=Align.INLINE)
d.comment(0xa78b, 'm3,', align=Align.INLINE)
d.comment(0xa78d, 'm2,', align=Align.INLINE)
d.comment(0xa78f, 'm1', align=Align.INLINE)
d.comment(0xa791, 'count', align=Align.INLINE)
d.comment(0xa792, 'loop', align=Align.INLINE)
d.comment(0xa794, 'final guard bit', align=Align.INLINE)
d.comment(0xa796, 'move the quotient into the FWA mantissa:', align=Align.INLINE)
d.comment(0xa798, '-> m4,', align=Align.INLINE)
d.comment(0xa79a, '&45...', align=Align.INLINE)
d.comment(0xa79c, '-> m3,', align=Align.INLINE)
d.comment(0xa79e, '&44...', align=Align.INLINE)
d.comment(0xa7a0, '-> m2,', align=Align.INLINE)
d.comment(0xa7a2, '&43...', align=Align.INLINE)
d.comment(0xa7a4, '-> m1', align=Align.INLINE)
d.comment(0xa7a6, 'normalise and round', align=Align.INLINE)
d.comment(0xa7a9, 'SQR of a negative: error block', align=Align.INLINE)
d.label(0xa7a9, 'sqr_neg_error')

# fn_sqr (&A7B4): SQR via Newton's method
d.comment(0xa7b4, 'Evaluate the argument as a real', align=Align.INLINE)
d.comment(0xa7b7, 'Sign of the argument', align=Align.INLINE)
# fn_sqr / fn_ln
d.label(0xa7b7, 'sqr_sign')
d.comment(0xa7ba, 'zero: the root is zero', align=Align.INLINE)
d.comment(0xa7bc, 'negative: -ve root error', align=Align.INLINE)
d.comment(0xa7be, 'Save the argument in TEMP1', align=Align.INLINE)
d.comment(0xa7c1, 'Initial guess: halve the exponent', align=Align.INLINE)
d.comment(0xa7c3, 'halve the exponent', align=Align.INLINE)
d.comment(0xa7c4, '(re-bias)', align=Align.INLINE)
d.comment(0xa7c6, 'store the guess exponent', align=Align.INLINE)
d.comment(0xa7c8, '5 Newton iterations', align=Align.INLINE)
d.comment(0xa7ca, '(counter)', align=Align.INLINE)
d.comment(0xa7cc, 'point at TEMP2 (the guess)', align=Align.INLINE)
d.comment(0xa7cf, 'save the current guess', align=Align.INLINE)
d.label(0xa7cf, 'sqr_iter_loop')
d.comment(0xa7d2, 'point at TEMP1 (the argument)', align=Align.INLINE)
d.comment(0xa7d4, 'store the pointer low', align=Align.INLINE)
d.comment(0xa7d6, 'FWA = argument / guess', align=Align.INLINE)
d.comment(0xa7d9, 'point at TEMP2 (the guess)', align=Align.INLINE)
d.comment(0xa7db, 'store the pointer low', align=Align.INLINE)
d.comment(0xa7dd, 'FWA = arg/guess + guess', align=Align.INLINE)
d.comment(0xa7e0, 'halve it: next guess', align=Align.INLINE)
d.comment(0xa7e2, 'count', align=Align.INLINE)
d.comment(0xa7e4, 'iterate', align=Align.INLINE)
d.comment(0xa7e6, 'real result', align=Align.INLINE)
d.label(0xa7e6, 'sqr_done')
d.comment(0xa7e8, 'Return the root', align=Align.INLINE)
d.subroutine(0xa7e9, 'point_fp_temp4', title='Point zp_fp_ptr at FP TEMP4 (&047B)',
             description='Set zp_fp_ptr to FP TEMP4, ready for a pack/unpack.',
             on_exit={'zp_fp_ptr (&4B/&4C)': '= &047B',
                      'X': 'preserved', 'Y': 'preserved'})
d.comment(0xa7e9, 'TEMP4 low (&7B)', align=Align.INLINE)
d.comment(0xa7eb, 'set it (shared tail)', align=Align.INLINE)
d.subroutine(0xa7ed, 'point_fp_temp2', title='Point zp_fp_ptr at FP TEMP2 (&0471)',
             description='Set zp_fp_ptr to FP TEMP2, ready for a pack/unpack.',
             on_exit={'zp_fp_ptr (&4B/&4C)': '= &0471',
                      'X': 'preserved', 'Y': 'preserved'})
d.comment(0xa7ed, 'TEMP2 low (&71)', align=Align.INLINE)
d.comment(0xa7ef, 'set it (shared tail)', align=Align.INLINE)
d.subroutine(0xa7f1, 'point_fp_temp3', title='Point zp_fp_ptr at FP TEMP3 (&0476)',
             description='Set zp_fp_ptr to FP TEMP3, ready for a pack/unpack.',
             on_exit={'zp_fp_ptr (&4B/&4C)': '= &0476',
                      'X': 'preserved', 'Y': 'preserved'})
d.comment(0xa7f1, 'TEMP3 low (&76)', align=Align.INLINE)
d.comment(0xa7f3, 'set it (shared tail)', align=Align.INLINE)
d.subroutine(0xa7f5, 'point_fp_temp1', title='Point zp_fp_ptr at FP TEMP1 (&046C)',
             description='Set zp_fp_ptr to FP TEMP1, ready for a pack/unpack.',
             on_exit={'zp_fp_ptr (&4B/&4C)': '= &046C',
                      'X': 'preserved', 'Y': 'preserved'})

d.comment(0xa7f5, 'TEMP1 low (&6C)', align=Align.INLINE)
d.comment(0xa7f7, 'set the pointer low', align=Align.INLINE)
d.label(0xa7f7, 'set_fp_ptr')
d.comment(0xa7f9, 'high &04', align=Align.INLINE)
d.comment(0xa7fb, 'pointer high', align=Align.INLINE)
d.comment(0xa7fd, 'Return', align=Align.INLINE)

# AAD1 continues into caad1: FWA = e^int * e^frac (already commented).

# fn_ln (&A7FE): LN(x) = ln(mantissa) + binary_exponent * ln 2.
d.comment(0xa7fe, 'Evaluate the argument as a real', align=Align.INLINE)
d.comment(0xa801, 'Sign of x', align=Align.INLINE)
d.label(0xa801, 'ln_compute')
d.comment(0xa804, 'zero: error', align=Align.INLINE)
d.comment(0xa806, 'positive: compute', align=Align.INLINE)
d.comment(0xa808, 'zero or negative: Log range error', align=Align.INLINE)
d.label(0xa808, 'log_range_error')
d.comment(0xa814, 'Set FWB = -1 (to form mantissa - 1)', align=Align.INLINE)
d.label(0xa814, 'ln_setup')
d.comment(0xa817, 'Y = &80,', align=Align.INLINE)
d.comment(0xa819, 'sign = negative,', align=Align.INLINE)
d.comment(0xa81b, 'mantissa top = &80,', align=Align.INLINE)
d.comment(0xa81d, 'Y = &81,', align=Align.INLINE)
d.comment(0xa81e, 'exponent = &81 (value -1.0)', align=Align.INLINE)
d.comment(0xa820, 'Binary exponent of x', align=Align.INLINE)
d.comment(0xa822, 'zero mantissa exponent?', align=Align.INLINE)
d.comment(0xa824, 'Mantissa top byte', align=Align.INLINE)
d.comment(0xa826, 'below sqrt(2)?', align=Align.INLINE)
d.comment(0xa828, 'yes: keep this exponent', align=Align.INLINE)
d.comment(0xa82a, 'no: scale mantissa to [sqrt(1/2), sqrt(2)]', align=Align.INLINE)
d.label(0xa82a, 'ln_scale')
d.comment(0xa82b, '...and adjust the exponent', align=Align.INLINE)
d.comment(0xa82c, 'Save the adjusted binary exponent', align=Align.INLINE)
d.label(0xa82c, 'ln_save_exp')
d.comment(0xa82d, 'push it', align=Align.INLINE)
d.comment(0xa82e, 'Set the mantissa exponent', align=Align.INLINE)
d.comment(0xa830, 'FWA = mantissa - 1', align=Align.INLINE)
d.comment(0xa833, 'Save (m-1) in TEMP4', align=Align.INLINE)
d.comment(0xa835, 'pack FWA there', align=Align.INLINE)
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
d.comment(0xa84f, 'set carry for the subtract', align=Align.INLINE)
d.comment(0xa850, 'Binary exponent e = adjusted - &81', align=Align.INLINE)
d.comment(0xa852, 'FWA = e', align=Align.INLINE)
d.comment(0xa855, 'Point at the constant ln 2: low byte', align=Align.INLINE)
d.comment(0xa857, 'store the pointer low', align=Align.INLINE)
d.comment(0xa859, 'high byte', align=Align.INLINE)
d.comment(0xa85b, 'store the pointer high', align=Align.INLINE)
d.comment(0xa85d, 'FWA = e * ln 2', align=Align.INLINE)
d.comment(0xa860, 'Point at ln(mantissa) in TEMP1', align=Align.INLINE)
d.comment(0xa863, 'LN(x) = e*ln2 + ln(mantissa)', align=Align.INLINE)
d.comment(0xa866, 'real result', align=Align.INLINE)
d.comment(0xa868, 'Return', align=Align.INLINE)

# Transcendental helpers (shared by ATN/ASN/ACS/SIN/COS).
d.subroutine(0xa897, 'fp_eval_cont_frac',
             title='Evaluate a continued-fraction approximation',
             description='A (low) and Y (high) point at a coefficient table: a '
                         'count byte followed by that many five-byte fp '
                         'coefficients. The argument is stashed in TEMP1; the '
                         'routine folds the table from the top, alternating '
                         'FWA = arg / FWA and FWA = FWA + next coefficient, to '
                         'evaluate the continued fraction used by the trig '
                         'kernels.',
             on_entry={'A': 'coefficient table address low byte',
                       'Y': 'coefficient table address high byte',
                       'zp_fwa (&2E-&35)': 'the argument'},
             on_exit={'zp_fwa (&2E-&35)': 'the continued-fraction value',
                      '(&046C)': 'corrupted (TEMP1 holds the argument)'})
# fp_eval_cont_frac (&A897): evaluate the trig continued fraction.
d.comment(0xa897, 'Save the coefficient table pointer (low)', align=Align.INLINE)
d.comment(0xa899, '...and high', align=Align.INLINE)
d.comment(0xa89b, 'Stash the argument in TEMP1', align=Align.INLINE)
d.comment(0xa89e, 'First table byte is the coefficient count', align=Align.INLINE)
d.comment(0xa8a0, 'read it', align=Align.INLINE)
d.comment(0xa8a2, 'use it as the loop counter', align=Align.INLINE)
d.comment(0xa8a4, 'Advance past the count byte to coefficient 0', align=Align.INLINE)
d.comment(0xa8a6, 'no carry into the high byte', align=Align.INLINE)
d.comment(0xa8a8, 'else bump the high byte', align=Align.INLINE)
d.comment(0xa8aa, 'Point the fp pointer at the first coefficient', align=Align.INLINE)
# fp_eval_cont_frac / fn_asn / fn_atn / complement
d.label(0xa8aa, 'cfrac_first')
d.comment(0xa8ac, 'low byte -> fp_ptr', align=Align.INLINE)
d.comment(0xa8ae, 'high byte', align=Align.INLINE)
d.comment(0xa8b0, '-> fp_ptr+1', align=Align.INLINE)
d.comment(0xa8b2, 'FWA = coefficient 0', align=Align.INLINE)
d.comment(0xa8b5, 'Point at the argument in TEMP1', align=Align.INLINE)
d.label(0xa8b5, 'cfrac_loop')
d.comment(0xa8b8, 'FWA = arg / FWA', align=Align.INLINE)
d.comment(0xa8bb, 'Advance the pointer to the next coefficient', align=Align.INLINE)
d.comment(0xa8bc, '...(five bytes per coefficient)', align=Align.INLINE)
d.comment(0xa8be, 'low byte + 5', align=Align.INLINE)
d.comment(0xa8c0, 'store the table pointer low', align=Align.INLINE)
d.comment(0xa8c2, 'and the fp pointer low', align=Align.INLINE)
d.comment(0xa8c4, 'high byte', align=Align.INLINE)
d.comment(0xa8c6, 'plus any carry', align=Align.INLINE)
d.comment(0xa8c8, 'store the table pointer high', align=Align.INLINE)
d.comment(0xa8ca, 'and the fp pointer high', align=Align.INLINE)
d.comment(0xa8cc, 'FWA = FWA + next coefficient', align=Align.INLINE)
d.comment(0xa8cf, 'One coefficient done', align=Align.INLINE)
d.comment(0xa8d1, 'loop until the table is exhausted', align=Align.INLINE)
d.comment(0xa8d3, 'Return the continued-fraction value', align=Align.INLINE)

# fn_acs (&A8D4): ACS(x) = pi/2 - ASN(x).
d.comment(0xa8d4, 'Compute asn(x)', align=Align.INLINE)
d.comment(0xa8d7, 'Result = pi/2 - asn(x)', align=Align.INLINE)

# fn_asn (&A8DA): ASN = arcsin, via the arctan relationship
d.comment(0xa8da, 'Evaluate the argument as a real', align=Align.INLINE)
d.comment(0xa8dd, 'Sign of the argument', align=Align.INLINE)
d.comment(0xa8e0, 'positive: compute directly', align=Align.INLINE)
d.comment(0xa8e2, 'negative: take |x|...', align=Align.INLINE)
d.comment(0xa8e4, 'compute asn(|x|)', align=Align.INLINE)
d.comment(0xa8e7, '...and negate the result', align=Align.INLINE)
d.comment(0xa8ea, 'Save x in TEMP3', align=Align.INLINE)
d.label(0xa8ea, 'asn_save')
d.comment(0xa8ed, 'compute sqrt(1 - x^2)', align=Align.INLINE)
d.comment(0xa8f0, 'is it zero (x = 1)?', align=Align.INLINE)
d.comment(0xa8f3, 'yes: result is pi/2', align=Align.INLINE)
d.comment(0xa8f5, 'point at x (TEMP3)', align=Align.INLINE)
d.comment(0xa8f8, 'FWA = x / sqrt(1 - x^2)', align=Align.INLINE)
d.comment(0xa8fb, 'asn(x) = atn(that)', align=Align.INLINE)
d.comment(0xa8fe, 'x = 1: load pi/2', align=Align.INLINE)
d.label(0xa8fe, 'asn_one')
d.comment(0xa901, 'unpack pi/2 into FWA', align=Align.INLINE)
d.comment(0xa904, 'real result', align=Align.INLINE)
d.label(0xa904, 'asn_done')
d.comment(0xa906, 'Return', align=Align.INLINE)

# fn_atn (&A907): ATN = arctan, result in radians.
d.comment(0xa907, 'Evaluate the argument as a real', align=Align.INLINE)
d.comment(0xa90a, 'Sign of the argument', align=Align.INLINE)
d.label(0xa90a, 'atn_sign')
d.comment(0xa90d, 'zero: atn(0) = 0, return it', align=Align.INLINE)
d.comment(0xa90f, 'positive: compute directly', align=Align.INLINE)
d.comment(0xa911, 'negative: clear the sign to take |x|', align=Align.INLINE)
d.comment(0xa913, 'compute atn(|x|)', align=Align.INLINE)
d.comment(0xa916, 'set the result sign negative', align=Align.INLINE)
d.label(0xa916, 'atn_neg')
d.comment(0xa918, '...so atn(-x) = -atn(x)', align=Align.INLINE)
d.comment(0xa91a, 'Return', align=Align.INLINE)
d.comment(0xa91b, 'Exponent of |x|', align=Align.INLINE)
d.label(0xa91b, 'atn_large')
d.comment(0xa91d, '|x| < 1?', align=Align.INLINE)
d.comment(0xa91f, 'yes: evaluate the series directly', align=Align.INLINE)
d.comment(0xa921, '|x| >= 1: FWA = 1 / x', align=Align.INLINE)
d.comment(0xa924, 'atn(1/x) via the series', align=Align.INLINE)
d.subroutine(0xa927, 'fwa_complement_half_pi', title='FWA = pi/2 - FWA',
             description='Subtract FWA from pi/2 using the two-part constant '
                         'at &AA59/&AA5E for extra precision, then negate. '
                         'Used for ACS (pi/2 - ASN) and the large-argument '
                         'arctan identity atn(x) = pi/2 - atn(1/x).',
             on_entry={'zp_fwa (&2E-&35)': 'the angle to complement'},
             on_exit={'zp_fwa (&2E-&35)': 'pi/2 - FWA',
                      'zp_fwb (&3B-&42)': 'corrupted (scratch)'})
d.comment(0xa927, 'atn(x) = pi/2 - atn(1/x)', align=Align.INLINE)
d.comment(0xa92a, 'add the high part of pi/2', align=Align.INLINE)
d.comment(0xa92d, 'point at the low part', align=Align.INLINE)
d.comment(0xa930, 'add the low part', align=Align.INLINE)
d.comment(0xa933, 'negate: result is pi/2 - FWA (tail)', align=Align.INLINE)
d.comment(0xa936, 'Exponent of the (reduced) argument', align=Align.INLINE)
d.label(0xa936, 'chp_exp')
d.comment(0xa938, 'very small (|x| < 2^-13)?', align=Align.INLINE)
d.comment(0xa93a, 'yes: atn(x) = x to working precision', align=Align.INLINE)
d.comment(0xa93c, 'Save the argument x in TEMP3', align=Align.INLINE)
d.comment(0xa93f, 'Set FWB = 1...', align=Align.INLINE)
d.comment(0xa942, 'the constant &80', align=Align.INLINE)
d.comment(0xa944, 'exponent,', align=Align.INLINE)
d.comment(0xa946, 'mantissa top byte,', align=Align.INLINE)
d.comment(0xa948, 'and sign byte', align=Align.INLINE)
d.comment(0xa94a, 'Add it to the argument', align=Align.INLINE)
d.comment(0xa94d, 'Evaluate the arctan continued fraction', align=Align.INLINE)
d.comment(0xa94f, '(coefficients at &A95A)', align=Align.INLINE)
d.comment(0xa951, 'evaluate the fraction', align=Align.INLINE)
d.comment(0xa954, 'Scale by x (in TEMP3): atn(x) = x * P', align=Align.INLINE)
d.comment(0xa957, 'real result', align=Align.INLINE)
d.comment(0xa959, 'Return', align=Align.INLINE)

# fn_cos (&A98D): COS = SIN with a quadrant shift
d.comment(0xa98d, 'Evaluate the argument as a real', align=Align.INLINE)
d.comment(0xa990, 'Compute the SIN/COS kernel', align=Align.INLINE)
d.comment(0xa993, 'Shift the quadrant: cos x = sin(x + pi/2)', align=Align.INLINE)
d.comment(0xa995, 'Finish (shared with SIN)', align=Align.INLINE)

# fn_sin (&A998) and the shared SIN/COS body.
d.comment(0xa998, 'Evaluate the argument as a real', align=Align.INLINE)
d.comment(0xa99b, 'Range-reduce: leaves the angle in FWA, quadrant in &4A',
          align=Align.INLINE)
d.comment(0xa99e, 'Quadrant', align=Align.INLINE)
# fn_sin / sin_cos_reduce
d.label(0xa99e, 'sin_quadrant')
d.comment(0xa9a0, 'second or third quadrant (result negative)?',
          align=Align.INLINE)
d.comment(0xa9a2, 'no: compute and return directly', align=Align.INLINE)
d.comment(0xa9a4, 'compute the magnitude...', align=Align.INLINE)
d.comment(0xa9a7, '...then negate it', align=Align.INLINE)
d.comment(0xa9aa, 'Odd quadrant (use cosine instead of sine)?',
          align=Align.INLINE)
d.label(0xa9aa, 'sin_odd_quad')
d.comment(0xa9ac, 'even: evaluate the sine series', align=Align.INLINE)
d.comment(0xa9ae, 'odd: evaluate the sine series...', align=Align.INLINE)
d.comment(0xa9b1, 'Save sin into TEMP1', align=Align.INLINE)
d.label(0xa9b1, 'sin_series')
d.comment(0xa9b4, 'FWA = sin^2', align=Align.INLINE)
d.comment(0xa9b7, 'save sin^2 to the work var', align=Align.INLINE)
d.comment(0xa9ba, 'FWA = 1', align=Align.INLINE)
d.comment(0xa9bd, 'FWA = 1 - sin^2', align=Align.INLINE)
d.comment(0xa9c0, 'cos = sqrt(1 - sin^2)', align=Align.INLINE)
d.comment(0xa9c3, 'Save the reduced angle r in TEMP3', align=Align.INLINE)
d.label(0xa9c3, 'sin_save_r')
d.comment(0xa9c6, 'FWA = r^2', align=Align.INLINE)
d.comment(0xa9c9, 'Point at the sine coefficient table: low byte',
          align=Align.INLINE)
d.comment(0xa9cb, '...high', align=Align.INLINE)
d.comment(0xa9cd, 'Evaluate the sine continued fraction in r^2',
          align=Align.INLINE)
d.comment(0xa9d0, 'Scale by r (in TEMP3): sin(r) = r * P', align=Align.INLINE)

d.subroutine(0xa9d3, 'sin_cos_reduce',
             title='Range-reduce the SIN/COS argument',
             description='Divide the argument by pi/2 to find the quadrant '
                         '(stored in &4A) and Cody-Waite reduce to the '
                         'principal range using the two-part pi/2 constant, '
                         'leaving the reduced angle in FWA for the series. '
                         'Errors if the argument is too large to reduce.',
             on_entry={'zp_fwa (&2E-&35)': 'the angle in radians'},
             on_exit={'zp_fwa (&2E-&35)': 'the reduced angle',
                      '(&4A)': 'the quadrant (0-3)',
                      'BRK': 'on an argument too large to reduce'})

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
d.comment(0xa9f7, 'or byte 2,', align=Align.INLINE)
d.comment(0xa9f9, 'or byte 1', align=Align.INLINE)
d.comment(0xa9fb, 'yes: argument already in range, use it as is',
          align=Align.INLINE)
d.comment(0xa9fd, 'Rebuild the quadrant count as a real: exponent',
          align=Align.INLINE)
d.comment(0xa9ff, 'set it', align=Align.INLINE)
d.comment(0xaa01, 'clear the rounding byte', align=Align.INLINE)
d.comment(0xaa03, 'store it', align=Align.INLINE)
d.comment(0xaa05, 'Sign of the count', align=Align.INLINE)
d.comment(0xaa07, 'into the sign byte', align=Align.INLINE)
d.comment(0xaa09, 'positive: skip', align=Align.INLINE)
d.comment(0xaa0b, 'negative: negate the mantissa', align=Align.INLINE)
d.comment(0xaa0e, 'Normalise the quadrant count', align=Align.INLINE)
d.label(0xaa0e, 'reduce_norm_quad')
d.comment(0xaa11, 'Save it in TEMP2', align=Align.INLINE)
d.comment(0xaa14, 'Cody-Waite reduce: FWA = count * (pi/2 high part)',
          align=Align.INLINE)
d.comment(0xaa17, 'multiply by it', align=Align.INLINE)
d.comment(0xaa1a, 'FWA = argument - count*(pi/2 high)', align=Align.INLINE)
d.comment(0xaa1d, 'add the argument', align=Align.INLINE)
d.comment(0xaa20, 'Save the partial reduction in TEMP1', align=Align.INLINE)
d.comment(0xaa23, 'Reload the quadrant count', align=Align.INLINE)
d.comment(0xaa26, 'into FWA', align=Align.INLINE)
d.comment(0xaa29, 'FWA = count * (pi/2 low part)', align=Align.INLINE)
d.comment(0xaa2c, 'multiply by it', align=Align.INLINE)
d.comment(0xaa2f, 'Subtract the low part too: FWA = reduced angle',
          align=Align.INLINE)
d.comment(0xaa32, 'add it (tail call)', align=Align.INLINE)
d.comment(0xaa35, 'Argument in range: reduced angle is the argument',
          align=Align.INLINE)
d.label(0xaa35, 'reduce_in_range')
d.comment(0xaa38, 'Argument too large: error', align=Align.INLINE)

d.label(0xaa38, 'reduce_too_big')
d.subroutine(0xaa48, 'point_half_pi_hi',
             title='Point the fp pointer at the high part of pi/2 (&AA59)',
             description='Set zp_fp_ptr to the high half of the extended-'
                         'precision pi/2 constant, ready to unpack.',
             on_exit={'zp_fp_ptr (&4B/&4C)': '= &AA59',
                      'X': 'preserved', 'Y': 'preserved'})
# Constant loaders for the two-part pi/2 and the rounded pi/2.
d.comment(0xaa48, 'High part of pi/2: low byte', align=Align.INLINE)
d.comment(0xaa4a, '...(shared tail)', align=Align.INLINE)
d.subroutine(0xaa4c, 'point_half_pi_lo',
             title='Point the fp pointer at the low part of pi/2 (&AA5E)',
             description='Set zp_fp_ptr to the low half of the extended-'
                         'precision pi/2 constant, ready to unpack.',
             on_exit={'zp_fp_ptr (&4B/&4C)': '= &AA5E',
                      'X': 'preserved', 'Y': 'preserved'})
d.comment(0xaa4c, 'Low part of pi/2: low byte', align=Align.INLINE)
d.comment(0xaa4e, 'Set the fp pointer low', align=Align.INLINE)
d.label(0xaa4e, 'set_pi_ptr')
d.comment(0xaa50, 'high &AA', align=Align.INLINE)
d.comment(0xaa52, 'pointer high', align=Align.INLINE)
d.comment(0xaa54, 'Return', align=Align.INLINE)
d.subroutine(0xaa55, 'point_const_half_pi',
             title='Point the fp pointer at the pi/2 constant (&AA63)',
             description='Set zp_fp_ptr to the packed pi/2 constant, ready to '
                         'unpack (used by the range reduction in SIN/COS).',
             on_exit={'zp_fp_ptr (&4B/&4C)': '= &AA63',
                      'X': 'preserved', 'Y': 'preserved'})
d.comment(0xaa55, 'pi/2 constant: low byte', align=Align.INLINE)
d.comment(0xaa57, '...(shared tail)', align=Align.INLINE)

# fn_exp (&AA91): EXP(x) = e^x = e^int(x) * e^frac(x).
d.comment(0xaa91, 'Evaluate the argument as a real', align=Align.INLINE)
d.comment(0xaa94, 'Exponent of x', align=Align.INLINE)
# fn_exp / fwa_int_power
d.label(0xaa94, 'exp_compute')
d.comment(0xaa96, 'x small enough to compute directly?', align=Align.INLINE)
d.comment(0xaa98, 'yes: compute', align=Align.INLINE)
d.comment(0xaa9a, 'much too large: handle the overflow case', align=Align.INLINE)
d.comment(0xaa9c, 'borderline: test the mantissa', align=Align.INLINE)
d.comment(0xaa9e, '...against the overflow threshold', align=Align.INLINE)
d.comment(0xaaa0, 'below it: still computable', align=Align.INLINE)
d.comment(0xaaa2, 'Sign of x', align=Align.INLINE)
d.label(0xaaa2, 'exp_sign')
d.comment(0xaaa4, 'x very negative: e^x underflows to 0', align=Align.INLINE)
d.comment(0xaaa6, 'FWA = 0', align=Align.INLINE)
d.comment(0xaaa9, 'real result', align=Align.INLINE)
d.comment(0xaaab, 'Return', align=Align.INLINE)
d.comment(0xaaac, 'x very positive: Exp range error', align=Align.INLINE)
d.label(0xaaac, 'exp_range_error')
d.comment(0xaab8, 'Split x into integer (&4A) and fraction', align=Align.INLINE)
d.label(0xaab8, 'exp_split')
d.comment(0xaabb, 'FWA = e^frac via the series', align=Align.INLINE)
d.comment(0xaabe, 'Save e^frac in TEMP3', align=Align.INLINE)
d.comment(0xaac1, 'Point at the constant e: low byte', align=Align.INLINE)
d.comment(0xaac3, 'store the pointer low', align=Align.INLINE)
d.comment(0xaac5, 'high byte', align=Align.INLINE)
d.comment(0xaac7, 'store the pointer high', align=Align.INLINE)
d.comment(0xaac9, 'FWA = e', align=Align.INLINE)
d.comment(0xaacc, 'Integer part of x', align=Align.INLINE)
d.comment(0xaace, 'FWA = e^int', align=Align.INLINE)
# caad1: shared finish - scale the series result by the saved argument.
d.comment(0xaad1, 'Point at the saved argument in TEMP3', align=Align.INLINE)
d.label(0xaad1, 'mul_by_temp3')
d.comment(0xaad4, 'FWA = series * argument', align=Align.INLINE)
d.comment(0xaad7, 'real result', align=Align.INLINE)
d.comment(0xaad9, 'Return', align=Align.INLINE)
d.comment(0xaada, 'Point at the coefficient table: low byte',
          align=Align.INLINE)
d.label(0xaada, 'exp_coeff_table')
d.comment(0xaadc, '...high', align=Align.INLINE)
d.comment(0xaade, 'Evaluate the continued fraction', align=Align.INLINE)
d.comment(0xaae1, 'real result', align=Align.INLINE)
d.comment(0xaae3, 'Return', align=Align.INLINE)

d.subroutine(0xab12, 'fwa_int_power', title='FWA = FWA ^ n (n in A)',
             description='Raise FWA to an integer power by repeated '
                         'multiplication; a negative exponent reciprocates '
                         'first. Used by EXP to form e^(integer part).',
             on_entry={'A': 'the signed integer exponent n',
                       'zp_fwa (&2E-&35)': 'the base'},
             on_exit={'zp_fwa (&2E-&35)': 'FWA raised to the n-th power',
                      'zp_fwb (&3B-&42)': 'corrupted (scratch)'})
# fwa_int_power (&AB12): FWA = FWA ^ n, n in A.
d.comment(0xab12, 'Exponent n', align=Align.INLINE)
d.comment(0xab13, 'positive?', align=Align.INLINE)
d.comment(0xab15, 'negative: use |n| and reciprocate', align=Align.INLINE)
d.comment(0xab16, 'n-1 into A', align=Align.INLINE)
d.comment(0xab17, 'complement to give |n|', align=Align.INLINE)
d.comment(0xab19, 'save the count', align=Align.INLINE)
d.comment(0xab1a, 'FWA = 1 / FWA', align=Align.INLINE)
d.comment(0xab1d, 'restore the count', align=Align.INLINE)
d.comment(0xab1e, 'Save the count', align=Align.INLINE)
d.label(0xab1e, 'intpow_loop')
d.comment(0xab1f, 'Stash the base in TEMP1', align=Align.INLINE)
d.comment(0xab22, 'FWA = 1 (running product)', align=Align.INLINE)
d.comment(0xab25, 'Count remaining', align=Align.INLINE)
d.label(0xab25, 'intpow_check')

d.comment(0xab26, 'zero: done', align=Align.INLINE)
d.comment(0xab28, 'One multiplication fewer', align=Align.INLINE)
d.comment(0xab29, 'decrement the count', align=Align.INLINE)
d.comment(0xab2b, 'save it back', align=Align.INLINE)
d.comment(0xab2c, 'FWA = FWA * base', align=Align.INLINE)
d.comment(0xab2f, 'loop', align=Align.INLINE)

d.comment(0xab32, 'Return', align=Align.INLINE)
# fn_adval (&AB33): ADVAL
d.comment(0xab33, 'Evaluate the integer argument', align=Align.INLINE)
d.comment(0xab36, 'X = the channel / buffer number', align=Align.INLINE)
d.comment(0xab38, 'OSBYTE &80: read ADC / buffer status', align=Align.INLINE)
d.comment(0xab3d, 'result low byte (X)', align=Align.INLINE)
d.comment(0xab3e, 'Return as an integer', align=Align.INLINE)
# fn_point (&AB41): POINT(x, y) - read a pixel colour.
d.comment(0xab41, 'Evaluate x', align=Align.INLINE)
d.comment(0xab44, 'stack it', align=Align.INLINE)
d.comment(0xab47, 'Expect a comma', align=Align.INLINE)
d.comment(0xab4a, 'Evaluate y, expect )', align=Align.INLINE)
d.comment(0xab4d, 'coerce to integer', align=Align.INLINE)
d.comment(0xab50, 'Save y', align=Align.INLINE)
d.comment(0xab52, 'push the low byte', align=Align.INLINE)
d.comment(0xab54, 'high byte', align=Align.INLINE)
# fn_point continuation gaps.
d.comment(0xab55, 'push it', align=Align.INLINE)
d.comment(0xab57, 'Recover x', align=Align.INLINE)
d.comment(0xab59, 'pull y high', align=Align.INLINE)
d.comment(0xab5a, 'into the OSWORD block', align=Align.INLINE)
d.comment(0xab5c, 'pull y low', align=Align.INLINE)
d.comment(0xab5d, 'y low into the block', align=Align.INLINE)
d.comment(0xab5f, 'point X at the block (&2A)', align=Align.INLINE)
d.comment(0xab61, 'Read the pixel colour', align=Align.INLINE)
d.comment(0xab66, 'Result sign (off-screen = -1)', align=Align.INLINE)

d.comment(0xab68, 'off-screen?', align=Align.INLINE)

d.comment(0xab6a, 'return as an integer', align=Align.INLINE)
d.comment(0xab6d, 'OSBYTE &86: read the text cursor position', align=Align.INLINE)
d.comment(0xab73, 'Return the column as an integer', align=Align.INLINE)

# fn_vpos (&AB76): VPOS
d.comment(0xab76, 'OSBYTE &86: read the cursor position', align=Align.INLINE)
d.comment(0xab7c, 'Return the row (Y) as an integer', align=Align.INLINE)

# Real SGN path (&AB7F).
d.comment(0xab7f, 'Sign of the real', align=Align.INLINE)
# SGN / RAD / USR / EVAL
d.label(0xab7f, 'sgn_real_loop')
d.comment(0xab82, 'zero: 0', align=Align.INLINE)
d.comment(0xab84, 'positive: 1', align=Align.INLINE)
d.comment(0xab86, 'negative: -1', align=Align.INLINE)
# fn_sgn (&AB88): SGN(x).
d.comment(0xab88, 'Evaluate the argument', align=Align.INLINE)
d.comment(0xab8b, 'string: error', align=Align.INLINE)
d.comment(0xab8d, 'real: use the FP sign', align=Align.INLINE)
d.comment(0xab8f, 'Integer: test for zero', align=Align.INLINE)
d.comment(0xab91, 'OR &2C,', align=Align.INLINE)
d.comment(0xab93, '&2B,', align=Align.INLINE)
d.comment(0xab95, '&2A (all zero => SGN 0)', align=Align.INLINE)
d.comment(0xab97, 'zero: 0', align=Align.INLINE)
d.comment(0xab99, 'Sign bit', align=Align.INLINE)
d.comment(0xab9b, 'positive: 1', align=Align.INLINE)
d.comment(0xab9d, 'negative: -1', align=Align.INLINE)
d.label(0xab9d, 'sgn_negative')
d.comment(0xaba0, 'Result = 1', align=Align.INLINE)
d.label(0xaba0, 'sgn_positive')
d.comment(0xaba2, 'return it', align=Align.INLINE)
d.label(0xaba2, 'sgn_return')
d.comment(0xaba5, 'Result = 0 (integer)', align=Align.INLINE)
d.label(0xaba5, 'sgn_zero')
d.comment(0xaba7, 'Return', align=Align.INLINE)

# fn_log (&ABA8): LOG(x) = log10(x) = ln(x) * log10(e).
d.comment(0xaba8, 'FWA = ln(x)', align=Align.INLINE)
d.comment(0xabab, 'Point at the constant log10(e): low byte', align=Align.INLINE)
d.comment(0xabad, 'high byte', align=Align.INLINE)
d.comment(0xabaf, 'FWA = ln(x) * log10(e)', align=Align.INLINE)

# fn_rad (&ABB1): RAD(x) = x * pi/180 (degrees -> radians).
d.comment(0xabb1, 'Evaluate the argument as a real', align=Align.INLINE)
d.comment(0xabb4, 'Point at the constant pi/180: low byte', align=Align.INLINE)
d.comment(0xabb6, 'high byte', align=Align.INLINE)
d.comment(0xabb8, 'Set the fp pointer low', align=Align.INLINE)
d.label(0xabb8, 'degrad_set_ptr')
d.comment(0xabba, '...and high', align=Align.INLINE)
d.comment(0xabbc, 'FWA = x * pi/180', align=Align.INLINE)
d.comment(0xabbf, 'Flag a non-zero real result', align=Align.INLINE)
d.comment(0xabc1, 'Return', align=Align.INLINE)

# fn_deg (&ABC2): radians -> degrees (multiply by 180/pi)
d.comment(0xabc2, 'Evaluate the argument as a real', align=Align.INLINE)
d.comment(0xabc5, 'Point at the constant 180/pi: low byte', align=Align.INLINE)
d.comment(0xabc7, 'high byte', align=Align.INLINE)
d.comment(0xabc9, 'Multiply FWA by it (radians -> degrees)', align=Align.INLINE)

# fn_pi (&ABCB): FWA = pi
d.comment(0xabcb, 'Load the constant pi/2 into FWA', align=Align.INLINE)
d.comment(0xabce, 'Double it (exponent + 1) to get pi', align=Align.INLINE)
d.comment(0xabd0, 'Flag a non-zero real result', align=Align.INLINE)
d.comment(0xabd1, 'FWA = pi', align=Align.INLINE)

# fn_usr (&ABD2): USR(addr) calls machine code, returns A,X,Y,P packed
d.comment(0xabd2, 'Evaluate the address argument as an integer', align=Align.INLINE)
d.comment(0xabd5, 'Set up registers and call the code', align=Align.INLINE)
d.comment(0xabd8, 'Returned A...', align=Align.INLINE)
d.comment(0xabda, '...and X into the low result bytes', align=Align.INLINE)
d.comment(0xabdc, 'Returned Y', align=Align.INLINE)
d.comment(0xabde, 'Returned flags...', align=Align.INLINE)
d.comment(0xabdf, 'pull them into A', align=Align.INLINE)
d.comment(0xabe0, '...into the top result byte', align=Align.INLINE)
d.comment(0xabe2, 'Clear decimal mode the code may have left set', align=Align.INLINE)
d.comment(0xabe3, 'Integer result', align=Align.INLINE)
d.comment(0xabe5, 'Return the packed A,X,Y,P', align=Align.INLINE)
d.comment(0xabe6, 'Non-numeric address: Type mismatch', align=Align.INLINE)

d.label(0xabe6, 'usr_type_error')
# ----------------------------------------------------------------------
# fn_eval (&ABE9): EVAL string$ - tokenise and evaluate at run time.
# Appends a CR to the argument string, stacks it (so string operations
# during evaluation cannot clobber it), points the parser at the stacked
# copy, tokenises it in place and runs the expression evaluator.
# ----------------------------------------------------------------------
d.comment(0xabe9, 'Evaluate the argument string', align=Align.INLINE)
d.comment(0xabec, 'not a string: error', align=Align.INLINE)
d.comment(0xabee, 'Append a CR terminator', align=Align.INLINE)
d.comment(0xabf0, 'index the new last byte,', align=Align.INLINE)
d.comment(0xabf2, 'CR,', align=Align.INLINE)
d.comment(0xabf4, 'append it', align=Align.INLINE)
d.comment(0xabf7, 'Stack the string', align=Align.INLINE)
d.comment(0xabfa, 'Save the parser pointer', align=Align.INLINE)
d.comment(0xabfc, 'push low,', align=Align.INLINE)
d.comment(0xabfd, 'high,', align=Align.INLINE)
d.comment(0xabff, 'push high,', align=Align.INLINE)
d.comment(0xac00, 'offset,', align=Align.INLINE)
d.comment(0xac02, 'push offset', align=Align.INLINE)
d.comment(0xac03, 'Point at the stacked string', align=Align.INLINE)
d.comment(0xac05, 'high byte in X', align=Align.INLINE)
d.comment(0xac07, 'step over the length byte', align=Align.INLINE)
d.comment(0xac08, 'parser pointer low', align=Align.INLINE)
d.comment(0xac0a, 'name pointer low', align=Align.INLINE)
d.comment(0xac0c, 'no carry into the high byte', align=Align.INLINE)
d.comment(0xac0e, 'carry into the high byte', align=Align.INLINE)
d.comment(0xac0f, 'parser pointer high', align=Align.INLINE)
d.label(0xac0f, 'eval_ptr_hi')
d.comment(0xac11, 'name pointer high', align=Align.INLINE)
d.comment(0xac13, 'Tokenise as mid-statement (&3B = &FF):', align=Align.INLINE)
d.comment(0xac15, 'so PTR etc. tokenise as functions, not assignments',
          align=Align.INLINE)
d.comment(0xac17, 'Offset back to the start', align=Align.INLINE)
d.comment(0xac18, 'offset = 0 (start of string)', align=Align.INLINE)
d.comment(0xac1a, 'Tokenise the stacked string', align=Align.INLINE)
d.comment(0xac1d, 'Evaluate the expression', align=Align.INLINE)
d.comment(0xac20, 'Drop the stacked string', align=Align.INLINE)
d.comment(0xac23, 'Restore the parser pointer', align=Align.INLINE)
d.label(0xac23, 'eval_restore_ptr')
d.comment(0xac24, 'the offset,', align=Align.INLINE)
d.comment(0xac26, 'pull the high byte,', align=Align.INLINE)
d.comment(0xac27, 'high,', align=Align.INLINE)
d.comment(0xac29, 'pull the low byte,', align=Align.INLINE)
d.comment(0xac2a, 'low', align=Align.INLINE)
d.comment(0xac2c, 'Result type', align=Align.INLINE)
d.comment(0xac2e, 'Return', align=Align.INLINE)

d.comment(0xac2f, 'Evaluate the argument', align=Align.INLINE)
d.comment(0xac32, 'not a string: error', align=Align.INLINE)
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
    description="""Convert the ASCII number in the string work area to a value
(an integer in IWA or a real in FWA) — the decimal/float reader behind
VAL and numeric tokenising. It accepts an optional leading sign, then
defers to [`parse_number`](address:a07b) for the digits, "." and "E"
exponent. It is decimal only: there is no "&" hex branch here (that is
[`factor_hex`](address:ae6d), reached from eval_factor), so a string led
by "&" reads no digits and yields 0, and scanning stops at the first
non-numeric character. A binary zero is appended to the SWA first.
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
# ascii_to_number (&AC34): convert the SWA string to a value (VAL)
d.comment(0xac34, 'NUL-terminate the SWA string', align=Align.INLINE)
d.comment(0xac36, 'the zero byte', align=Align.INLINE)
d.comment(0xac38, 'store it past the digits', align=Align.INLINE)
d.comment(0xac3b, 'Save PtrB (we point it at the SWA):', align=Align.INLINE)
d.comment(0xac3d, 'push the low byte', align=Align.INLINE)
d.comment(0xac3e, 'high byte', align=Align.INLINE)
d.comment(0xac40, 'push it', align=Align.INLINE)
d.comment(0xac41, 'and the offset', align=Align.INLINE)
d.comment(0xac43, 'push it', align=Align.INLINE)
d.comment(0xac44, 'Point PtrB at the SWA (&0600): offset 0', align=Align.INLINE)
d.comment(0xac46, 'set the offset', align=Align.INLINE)
d.comment(0xac48, 'low 0', align=Align.INLINE)
d.comment(0xac4a, 'set the low byte', align=Align.INLINE)
d.comment(0xac4c, 'high &06', align=Align.INLINE)
d.comment(0xac4e, 'set the high byte', align=Align.INLINE)
d.comment(0xac50, 'skip spaces', align=Align.INLINE)
d.comment(0xac53, 'minus sign?', align=Align.INLINE)
d.char_literal(0xac54)
d.comment(0xac55, 'negative number', align=Align.INLINE)
d.comment(0xac57, 'plus sign?', align=Align.INLINE)
d.char_literal(0xac58)
d.comment(0xac59, 'no sign', align=Align.INLINE)
d.comment(0xac5b, 'skip the plus', align=Align.INLINE)
d.comment(0xac5e, 'step back', align=Align.INLINE)
# ascii_to_number (VAL) / INT
d.label(0xac5e, 'a2n_back')
d.comment(0xac60, 'parse the number', align=Align.INLINE)
d.comment(0xac63, 'finish', align=Align.INLINE)
d.comment(0xac66, 'negative: skip the minus', align=Align.INLINE)
d.label(0xac66, 'a2n_negative')
d.comment(0xac69, 'step back', align=Align.INLINE)
d.comment(0xac6b, 'parse the number', align=Align.INLINE)
d.comment(0xac6e, 'integer: done', align=Align.INLINE)
d.comment(0xac70, 'real: negate it', align=Align.INLINE)
d.comment(0xac73, 'store the result type', align=Align.INLINE)
d.label(0xac73, 'a2n_store_type')
d.comment(0xac75, 'restore PtrB and return', align=Align.INLINE)

# fn_int (&AC78): INT(x) - floor to integer.
d.comment(0xac78, 'Evaluate the argument', align=Align.INLINE)
d.comment(0xac7b, 'string: error', align=Align.INLINE)
d.comment(0xac7d, 'already integer: return it', align=Align.INLINE)
d.comment(0xac7f, 'Real: remember the sign', align=Align.INLINE)
d.comment(0xac81, 'save the sign flags', align=Align.INLINE)
d.comment(0xac82, 'Take the integer part', align=Align.INLINE)
d.comment(0xac85, 'sign', align=Align.INLINE)
d.comment(0xac86, 'positive: no adjustment', align=Align.INLINE)
d.comment(0xac88, 'Negative: any fractional bits?', align=Align.INLINE)
d.comment(0xac8a, 'OR &3F,', align=Align.INLINE)
d.comment(0xac8c, '&40,', align=Align.INLINE)
d.comment(0xac8e, '&41 (any set => not exact)', align=Align.INLINE)
d.comment(0xac90, 'none: exact', align=Align.INLINE)
d.comment(0xac92, 'round down (floor of a negative)', align=Align.INLINE)
d.comment(0xac95, 'Copy the integer to IWA', align=Align.INLINE)
d.label(0xac95, 'int_to_iwa')
d.comment(0xac98, 'integer result', align=Align.INLINE)
d.comment(0xac9a, 'Return', align=Align.INLINE)

d.comment(0xac9b, 'Type mismatch error', align=Align.INLINE)
d.label(0xac9b, 'num_type_error')
# fn_asc (&AC9E): ASC(s$).
d.comment(0xac9e, 'Evaluate the string', align=Align.INLINE)
d.comment(0xaca1, 'not a string: error', align=Align.INLINE)
d.comment(0xaca3, 'String length', align=Align.INLINE)
d.comment(0xaca5, 'empty: -1', align=Align.INLINE)
d.comment(0xaca7, 'First character', align=Align.INLINE)
d.comment(0xacaa, 'return it', align=Align.INLINE)

d.label(0xacaa, 'asc_result')
# fn_inkey (&ACAD): INKEY
d.comment(0xacad, 'Read a key within the time limit', align=Align.INLINE)
d.comment(0xacb0, 'timed out?', align=Align.INLINE)
d.comment(0xacb2, 'no key: return -1 (TRUE)', align=Align.INLINE)
d.comment(0xacb4, 'X = the key code', align=Align.INLINE)
d.comment(0xacb5, 'Return the key code as an integer', align=Align.INLINE)
# fn_eof (&ACB8): EOF#channel
d.comment(0xacb8, 'Evaluate the channel number', align=Align.INLINE)
d.comment(0xacbb, 'Channel to X', align=Align.INLINE)
d.comment(0xacbc, 'OSBYTE &7F: test for end of file', align=Align.INLINE)
d.comment(0xacc2, 'Return TRUE/FALSE per the EOF flag', align=Align.INLINE)

# fn_true (&ACC4): TRUE = -1 (also the ineg1 integer primitive)
d.comment(0xacc4, 'TRUE is -1: load &FF into every IWA byte', align=Align.INLINE)
d.comment(0xacc6, 'byte 0', align=Align.INLINE)
d.comment(0xacc8, 'byte 1', align=Align.INLINE)
d.comment(0xacca, 'byte 2', align=Align.INLINE)
d.comment(0xaccc, 'byte 3: IWA = -1', align=Align.INLINE)
d.comment(0xacce, 'Result type = integer', align=Align.INLINE)
d.comment(0xacd0, 'Return TRUE', align=Align.INLINE)

# fn_not (&ACD1): NOT = one's complement of the integer
d.comment(0xacd1, 'Evaluate the argument as an integer', align=Align.INLINE)
d.comment(0xacd4, 'Complement all four IWA bytes', align=Align.INLINE)
d.comment(0xacd6, 'byte X...', align=Align.INLINE)
d.label(0xacd6, 'not_loop')
d.comment(0xacd8, "...one's complement", align=Align.INLINE)
d.comment(0xacda, '(store)', align=Align.INLINE)
d.comment(0xacdc, 'next byte', align=Align.INLINE)
d.comment(0xacdd, 'loop', align=Align.INLINE)
d.comment(0xacdf, 'Integer result', align=Align.INLINE)
d.comment(0xace1, 'Return NOT value', align=Align.INLINE)

# fn_instr (&ACE2): INSTR(s$, search$ [, start]) -> position or 0.
d.comment(0xace2, 'Evaluate the searched string', align=Align.INLINE)
d.comment(0xace5, 'not a string: Type mismatch', align=Align.INLINE)
d.comment(0xace7, "','?", align=Align.INLINE)
d.char_literal(0xace8)
d.comment(0xace9, 'no: Missing ,', align=Align.INLINE)
d.comment(0xaceb, 'step past', align=Align.INLINE)
d.comment(0xaced, 'Stack the searched string', align=Align.INLINE)
d.comment(0xacf0, 'Evaluate the search string', align=Align.INLINE)
d.comment(0xacf3, 'not a string: Type mismatch', align=Align.INLINE)
d.comment(0xacf5, 'Default start position = 1', align=Align.INLINE)
d.comment(0xacf7, 'store as the start position', align=Align.INLINE)
d.comment(0xacf9, 'step past', align=Align.INLINE)
d.comment(0xacfb, "')' (no start given)?", align=Align.INLINE)
d.char_literal(0xacfc)
d.comment(0xacfd, 'yes: search from 1', align=Align.INLINE)
d.comment(0xacff, "','?", align=Align.INLINE)
d.char_literal(0xad00)
d.comment(0xad01, 'yes: a start position follows', align=Align.INLINE)
d.comment(0xad03, 'Missing , error', align=Align.INLINE)
# fn_instr
d.label(0xad03, 'instr_missing_comma')
d.comment(0xad06, 'Stack the search string', align=Align.INLINE)
d.label(0xad06, 'instr_stack')
d.comment(0xad09, 'Evaluate the start, expect )', align=Align.INLINE)
d.comment(0xad0c, 'coerce to integer', align=Align.INLINE)
d.comment(0xad0f, 'Restore the search string', align=Align.INLINE)
d.comment(0xad12, 'Destination index', align=Align.INLINE)
d.label(0xad12, 'instr_dest_index')
d.comment(0xad14, 'Start position', align=Align.INLINE)
d.comment(0xad16, 'non-zero?', align=Align.INLINE)
d.comment(0xad18, 'force at least 1', align=Align.INLINE)
d.comment(0xad1a, 'Current match position', align=Align.INLINE)
d.label(0xad1a, 'instr_match_pos')
d.comment(0xad1c, 'Zero-based start = start - 1', align=Align.INLINE)
d.comment(0xad1d, 'start - 1,', align=Align.INLINE)
d.comment(0xad1e, 'save the zero-based start', align=Align.INLINE)
d.comment(0xad20, 'Point at s$ + (start-1)', align=Align.INLINE)
d.comment(0xad21, '+ stack pointer low,', align=Align.INLINE)
d.comment(0xad23, 'pointer low,', align=Align.INLINE)
d.comment(0xad25, 'A = 0 (from Y),', align=Align.INLINE)
d.comment(0xad26, '+ stack pointer high,', align=Align.INLINE)
d.comment(0xad28, 'pointer high', align=Align.INLINE)
d.comment(0xad2a, 'Length of s$', align=Align.INLINE)
d.comment(0xad2c, 'minus the start offset...', align=Align.INLINE)
d.comment(0xad2d, 'len(s$) - (start-1)', align=Align.INLINE)
d.comment(0xad2f, 'start beyond the end: not found', align=Align.INLINE)
d.comment(0xad31, 'minus the search length', align=Align.INLINE)
d.comment(0xad33, "won't fit: not found", align=Align.INLINE)
d.comment(0xad35, 'Number of start positions to try', align=Align.INLINE)
d.comment(0xad37, 'positions to try', align=Align.INLINE)
d.comment(0xad39, 'Re-point at the stacked string', align=Align.INLINE)
d.comment(0xad3c, 'Compare from index 0', align=Align.INLINE)
d.label(0xad3c, 'instr_compare')
d.comment(0xad3e, 'Search length', align=Align.INLINE)
d.comment(0xad40, 'empty search: matches here', align=Align.INLINE)
d.comment(0xad42, 's$ character', align=Align.INLINE)
d.label(0xad42, 'instr_cmp_loop')
d.comment(0xad44, 'vs search character', align=Align.INLINE)
d.comment(0xad47, 'mismatch: advance', align=Align.INLINE)
d.comment(0xad49, 'next', align=Align.INLINE)
d.comment(0xad4a, 'one fewer char to match', align=Align.INLINE)
d.comment(0xad4b, 'all matched?', align=Align.INLINE)
d.comment(0xad4d, 'Match: result is the position', align=Align.INLINE)
d.label(0xad4d, 'instr_match')
d.comment(0xad4f, 'return it as an integer', align=Align.INLINE)
d.label(0xad4f, 'instr_result')
d.comment(0xad52, 'Not found: drop the stacked string', align=Align.INLINE)
d.label(0xad52, 'instr_not_found')
d.comment(0xad55, 'result = 0', align=Align.INLINE)
d.label(0xad55, 'instr_zero')
d.comment(0xad57, 'return it', align=Align.INLINE)
d.comment(0xad59, 'Advance the match position', align=Align.INLINE)
d.label(0xad59, 'instr_advance')
d.comment(0xad5b, 'one fewer position to try', align=Align.INLINE)
d.comment(0xad5d, 'exhausted: not found', align=Align.INLINE)
d.comment(0xad5f, 'advance the s$ pointer', align=Align.INLINE)
d.comment(0xad61, 'retry', align=Align.INLINE)
d.comment(0xad63, 'carry into the high byte', align=Align.INLINE)
d.comment(0xad65, 'retry', align=Align.INLINE)

d.comment(0xad67, 'Type mismatch error', align=Align.INLINE)
d.label(0xad67, 'instr_type_error')

# fn_abs (&AD6A): ABS(x).
d.comment(0xad6a, 'Evaluate the argument', align=Align.INLINE)
d.comment(0xad6d, 'zero: return it', align=Align.INLINE)
d.comment(0xad6f, 'real: clear the sign', align=Align.INLINE)

d.subroutine(
    0xad71, 'iwa_abs',
    title='Make the integer accumulator positive',
    description='IWA = ABS(IWA).',
    on_entry={'zp_iwa (&2A)': '32-bit integer'},
    on_exit={'zp_iwa': 'made positive', 'X': 'preserved'},
)
# iwa_abs (&AD71): make IWA positive
d.comment(0xad71, 'Test the sign of IWA (top byte)', align=Align.INLINE)
d.comment(0xad73, 'Negative: negate it', align=Align.INLINE)
d.comment(0xad75, 'Positive: leave it', align=Align.INLINE)
d.comment(0xad77, 'ABS of a real: get the sign', align=Align.INLINE)
# iwa_abs / fwa_negate / iwa_negate
d.label(0xad77, 'abs_real')
d.comment(0xad7a, 'positive/zero: done', align=Align.INLINE)
d.comment(0xad7c, 'negative: clear the sign', align=Align.INLINE)
d.subroutine(0xad7e, 'fwa_negate', title='FWA = -FWA',
             description='Negate FWA by flipping the sign bit (a zero value is '
                         'left unchanged).',
             on_entry={'zp_fwa (&2E-&35)': 'the value to negate'},
             on_exit={'zp_fwa_sign (&2E)': 'sign bit toggled (unless zero)',
                      'A': 'real type marker (&FF)'})
# fwa_negate (&AD7E): FWA = -FWA
d.comment(0xad7e, 'Is FWA zero?', align=Align.INLINE)
d.comment(0xad81, 'zero: nothing to negate', align=Align.INLINE)
d.comment(0xad83, 'Toggle the sign bit...', align=Align.INLINE)
d.label(0xad83, 'fneg_toggle')
d.comment(0xad85, 'flip bit 7', align=Align.INLINE)
d.comment(0xad87, '(store)', align=Align.INLINE)
d.comment(0xad89, 'real result type', align=Align.INLINE)
d.label(0xad89, 'fneg_done')
d.comment(0xad8b, 'Return', align=Align.INLINE)
d.comment(0xad8c, 'Unary minus: evaluate the operand', align=Align.INLINE)
d.label(0xad8c, 'unary_minus')
d.comment(0xad8f, 'zero: leave it', align=Align.INLINE)
d.label(0xad8f, 'fneg_zero')
d.comment(0xad91, 'real: negate FWA', align=Align.INLINE)
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
# iwa_negate (&AD93): IWA = -IWA
d.comment(0xad93, 'Negate IWA: compute 0 - IWA', align=Align.INLINE)
d.comment(0xad94, 'from zero', align=Align.INLINE)
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
d.label(0xadaa, 'ineg_done')
d.comment(0xadac, 'Return -IWA', align=Align.INLINE)
d.subroutine(0xadad, 'read_string_literal', title='Read a string literal',
             description='Read a quoted ("...", with "" for a literal quote) or '
                         'unquoted string at PtrB into the string buffer.',
             on_entry={'zp_text_ptr2 (&19/&1A)': 'PtrB at the string'},
             on_exit={'string_work (&0600)': 'the string characters',
                      'zp_strbuf_len (&36)': 'the string length',
                      'zp_text_ptr2_off (&1B)': 'advanced past the literal'})

d.comment(0xadad, 'Read a string literal: skip spaces', align=Align.INLINE)
d.comment(0xadb0, 'a quote?', align=Align.INLINE)
d.char_literal(0xadb1)
d.comment(0xadb2, 'quoted string', align=Align.INLINE)
d.comment(0xadb4, 'Unquoted: read until CR or comma', align=Align.INLINE)
d.comment(0xadb6, 'char', align=Align.INLINE)
# read_string_literal
d.label(0xadb6, 'rsl_unquoted_loop')
d.comment(0xadb8, 'into the buffer', align=Align.INLINE)
d.comment(0xadbb, 'next', align=Align.INLINE)
d.comment(0xadbc, 'and the buffer index', align=Align.INLINE)
d.comment(0xadbd, 'CR?', align=Align.INLINE)
d.comment(0xadbf, 'end', align=Align.INLINE)
d.comment(0xadc1, 'comma?', align=Align.INLINE)
d.char_literal(0xadc2)
d.comment(0xadc3, 'loop', align=Align.INLINE)
d.comment(0xadc5, 'step back', align=Align.INLINE)
d.label(0xadc5, 'rsl_unquoted_end')
d.comment(0xadc6, 'finish', align=Align.INLINE)
d.comment(0xadc9, 'Quoted: read until the closing quote', align=Align.INLINE)
d.label(0xadc9, 'rsl_quoted')
d.comment(0xadcb, 'advance', align=Align.INLINE)
d.label(0xadcb, 'rsl_quoted_adv')
d.comment(0xadcc, 'char', align=Align.INLINE)
d.label(0xadcc, 'rsl_quoted_loop')
d.comment(0xadce, 'CR (unterminated)?', align=Align.INLINE)
d.comment(0xadd0, 'Missing " error', align=Align.INLINE)
d.comment(0xadd2, 'next', align=Align.INLINE)
d.comment(0xadd3, 'into the buffer', align=Align.INLINE)
d.comment(0xadd6, 'advance the buffer index', align=Align.INLINE)
d.comment(0xadd7, 'a quote?', align=Align.INLINE)
d.char_literal(0xadd8)
d.comment(0xadd9, 'no: keep copying', align=Align.INLINE)
d.comment(0xaddb, 'doubled "" = a literal quote?', align=Align.INLINE)
d.comment(0xaddd, 'also a quote?', align=Align.INLINE)
d.char_literal(0xadde)
d.comment(0xaddf, 'yes: keep it', align=Align.INLINE)
d.comment(0xade1, 'drop the trailing character', align=Align.INLINE)
d.label(0xade1, 'rsl_drop_trail')
d.comment(0xade2, 'set the string length', align=Align.INLINE)
d.comment(0xade4, 'update the text offset', align=Align.INLINE)
d.comment(0xade6, 'string type', align=Align.INLINE)
d.comment(0xade8, 'Return the string', align=Align.INLINE)
d.comment(0xade9, 'Missing " error', align=Align.INLINE)

d.label(0xade9, 'rsl_missing_quote')
d.subroutine(
    0xadec, 'eval_factor',
    title='Evaluate a factor (evaluator level 1)',
    description="""Evaluate the highest-precedence level of an expression at PtrB:
unary minus, unary plus and NOT; parenthesised sub-expressions;
the ?, !, $ and | indirection operators; string literals; and the
built-in functions. Unlike the higher levels, it does not read the
trailing operator - the caller does that.
""",
    on_entry={'zp_text_ptr2 (&19/&1A)': 'PtrB at the factor to evaluate',
              'zp_text_ptr2_off (&1B)': 'offset into the text'},
    on_exit={'A': 'result type: <0 = float in fwa, >0 = integer in iwa, 0 = string',
             'zp_iwa / zp_fwa / string_work (&0600)':
                 'the value, selected by the type in A',
             'zp_text_ptr2_off (&1B)': 'advanced past the factor'},
)
# eval_factor (&ADEC): expression Level 1 - the atom.
d.comment(0xadec, 'Next character', align=Align.INLINE)
d.comment(0xadee, 'advance the offset', align=Align.INLINE)
d.comment(0xadf0, 'read it', align=Align.INLINE)
d.comment(0xadf2, 'space?', align=Align.INLINE)
d.char_literal(0xadf3)
d.comment(0xadf4, 'skip it', align=Align.INLINE)
d.comment(0xadf6, "'-' unary minus?", align=Align.INLINE)
d.char_literal(0xadf7)
d.comment(0xadf8, 'yes', align=Align.INLINE)
d.comment(0xadfa, "'\"' string literal?", align=Align.INLINE)
d.char_literal(0xadfb)
d.comment(0xadfc, 'yes', align=Align.INLINE)
d.comment(0xadfe, "'+' unary plus?", align=Align.INLINE)
d.char_literal(0xadff)
d.comment(0xae00, 'no: classify the token', align=Align.INLINE)
d.comment(0xae02, 'unary plus: re-read the next character', align=Align.INLINE)
# eval_factor
d.label(0xae02, 'factor_unary_plus')
d.comment(0xae05, 'below the lowest function token?', align=Align.INLINE)
d.label(0xae05, 'factor_classify')
d.comment(0xae07, 'yes: indirection, number or variable', align=Align.INLINE)
d.comment(0xae09, 'above the highest function token?', align=Align.INLINE)
d.comment(0xae0b, 'yes: No such variable', align=Align.INLINE)
d.comment(0xae0d, 'a function: dispatch it', align=Align.INLINE)
d.comment(0xae10, "'?' (byte indirection) or higher?", align=Align.INLINE)
d.char_literal(0xae11)
d.label(0xae10, 'factor_indirect')
d.comment(0xae12, 'yes: variable or indirection', align=Align.INLINE)
d.comment(0xae14, "'.' or a digit?", align=Align.INLINE)
d.char_literal(0xae15)
d.comment(0xae16, 'yes: a number', align=Align.INLINE)
d.comment(0xae18, "'&' hex number?", align=Align.INLINE)
d.char_literal(0xae19)
d.comment(0xae1a, 'yes', align=Align.INLINE)
d.comment(0xae1c, "'(' sub-expression?", align=Align.INLINE)
d.char_literal(0xae1d)
d.comment(0xae1e, 'yes', align=Align.INLINE)
d.comment(0xae20, 'Back up to the name', align=Align.INLINE)
d.label(0xae20, 'factor_name')
d.comment(0xae22, 'Parse the variable reference', align=Align.INLINE)
d.comment(0xae25, 'undefined: handle below', align=Align.INLINE)
d.comment(0xae27, 'load the variable value', align=Align.INLINE)
d.comment(0xae2a, 'Parse the decimal number', align=Align.INLINE)
d.label(0xae2a, 'factor_number')
d.comment(0xae2d, 'ok', align=Align.INLINE)
d.comment(0xae2e, 'Return', align=Align.INLINE)
d.comment(0xae2f, 'Return', align=Align.INLINE)
d.comment(0xae30, 'Undefined: OPT flag', align=Align.INLINE)
d.label(0xae30, 'factor_undefined')
d.comment(0xae32, 'ignore-undefined set?', align=Align.INLINE)
d.comment(0xae34, 'no: No such variable', align=Align.INLINE)
d.comment(0xae36, 'bad name: No such variable', align=Align.INLINE)
d.comment(0xae38, 'accept; advance the offset', align=Align.INLINE)
d.comment(0xae3a, 'Use P% as the value', align=Align.INLINE)
d.label(0xae3a, 'factor_pcounter')
d.comment(0xae3f, 'return it as an integer', align=Align.INLINE)
d.comment(0xae40, 'return as a 16-bit integer', align=Align.INLINE)
d.comment(0xae43, 'No such variable error', align=Align.INLINE)
d.subroutine(
    0xae43, 'no_such_variable',
    title='Raise "No such variable" error',
    description="""Raise BASIC error &1A, "No such variable", via a BRK error block.
Reached when an expression or lvalue names a variable that has not
been created. Does not return.
""",
    on_exit={
        'control': 'raises BRK error &1A "No such variable"; does not return to the caller',
    },
)
d.comment(0xae56, 'Sub-expression: evaluate it', align=Align.INLINE)
d.subroutine(
    0xae56, 'eval_subexpr',
    title='Evaluate a parenthesised sub-expression',
    description="""Evaluate a full expression at PtrB via eval_or_eor, then require a
closing ")" - raising Missing ) if the terminating operator is
anything else. Used wherever a bracketed sub-expression appears in the
grammar.
""",
    on_entry={
        'zp_text_ptr2 (&19/&1A)': 'PtrB, positioned just after the opening "("',
        'zp_text_ptr2_off (&1B)': 'offset into the text',
    },
    on_exit={
        'A': 'result type (<0 float in fwa, >0 integer in iwa, 0 string)',
        'Y': 'copy of the result type',
        'zp_iwa (&2A) / zp_fwa (&2E) / string_work (&0600)': 'the value, selected by the type',
        'zp_text_ptr2_off (&1B)': 'advanced past the ")"',
    },
)
d.comment(0xae59, 'step past', align=Align.INLINE)
d.comment(0xae5b, "')' to close?", align=Align.INLINE)
d.char_literal(0xae5c)
d.comment(0xae5d, 'no: Missing )', align=Align.INLINE)
d.comment(0xae5f, 'flag the result type', align=Align.INLINE)
d.comment(0xae60, 'Return', align=Align.INLINE)
d.comment(0xae61, 'Missing ) error', align=Align.INLINE)
d.label(0xae61, 'missing_paren')
d.banner(
    0xae6d,
    title='Scan an & hex constant',
    description="""Shift each hex digit's nibble into the 32-bit IWA
(&2A-&2D); the bit rolled off the top is discarded, so there is **no**
overflow check — a 9th or later digit silently drops the high nibble and
only the low 32 bits survive (so `&AABBCCDD` is accepted as the signed
integer -1430532899, and `&FFFFFFFF` as -1). The digit run is unbounded;
the sole error is Bad HEX, raised only when `&` is followed by no hex
digits at all. The accepted digits are `0-9` and uppercase `A-F` only —
a lowercase `a-f` ends the scan, so `&ff` reads no digits and faults Bad
HEX whereas `&Ff` is 15. This is the only `&` reader, reached from
[`eval_factor`](address:adec); VAL's number reader
([`parse_number`](address:a07b)) is decimal-only. Returns type &40
(integer).""",
)
d.comment(0xae6d, 'Hex number: clear IWA', align=Align.INLINE)
d.label(0xae6d, 'factor_hex')
d.comment(0xae6f, 'byte 0,', align=Align.INLINE)
d.comment(0xae71, 'byte 1,', align=Align.INLINE)
d.comment(0xae73, 'byte 2,', align=Align.INLINE)
d.comment(0xae75, 'byte 3', align=Align.INLINE)
d.comment(0xae77, 'scan offset', align=Align.INLINE)
d.comment(0xae79, 'Next character', align=Align.INLINE)
d.label(0xae79, 'factor_hex_loop')
d.comment(0xae7b, "below '0'?", align=Align.INLINE)
d.char_literal(0xae7c)
d.comment(0xae7d, 'yes: end of number', align=Align.INLINE)
d.comment(0xae7f, 'a digit 0-9?', align=Align.INLINE)
d.char_literal(0xae80)
d.comment(0xae81, 'yes', align=Align.INLINE)
d.comment(0xae83, "fold A-F to 10-15", align=Align.INLINE)
d.comment(0xae85, 'below 10 (a gap char)?', align=Align.INLINE)
d.comment(0xae87, 'yes: end of number', align=Align.INLINE)
d.comment(0xae89, 'above F? (also rejects lowercase a-f)', align=Align.INLINE)
d.comment(0xae8b, 'yes: end of number', align=Align.INLINE)
d.comment(0xae8d, 'Shift the digit into the high nibble', align=Align.INLINE)
d.label(0xae8d, 'factor_hex_nibble')
d.comment(0xae8e, '(continued)', align=Align.INLINE)
d.comment(0xae8f, '(continued)', align=Align.INLINE)
d.comment(0xae90, '(continued)', align=Align.INLINE)
d.comment(0xae91, 'four bits to shift', align=Align.INLINE)
d.comment(0xae93, 'Shift one bit into IWA', align=Align.INLINE)
d.label(0xae93, 'factor_hex_shift')
d.comment(0xae94, 'byte 0,', align=Align.INLINE)
d.comment(0xae96, 'byte 1,', align=Align.INLINE)
d.comment(0xae98, 'byte 2,', align=Align.INLINE)
d.comment(0xae9a, 'byte 3 (bit rolled out here is dropped: no check)',
          align=Align.INLINE)
d.comment(0xae9c, 'one of four bits done', align=Align.INLINE)
d.comment(0xae9d, 'next bit', align=Align.INLINE)
d.comment(0xae9f, 'advance', align=Align.INLINE)
d.comment(0xaea0, 'next digit: unbounded run, low 32 bits survive',
          align=Align.INLINE)
d.comment(0xaea2, 'Any digits seen?', align=Align.INLINE)
d.label(0xaea2, 'factor_hex_check')
d.comment(0xaea3, 'no: Bad HEX', align=Align.INLINE)
d.comment(0xaea5, 'Save the offset', align=Align.INLINE)
d.comment(0xaea7, 'Type = integer', align=Align.INLINE)
d.comment(0xaea9, 'Return', align=Align.INLINE)
d.comment(0xaeaa, 'Bad HEX error', align=Align.INLINE)

d.label(0xaeaa, 'bad_hex')

# fn_time (&AEB4): =TIME reads the centisecond clock
d.comment(0xaeb4, 'Point OSWORD at IWA: low byte', align=Align.INLINE)
d.comment(0xaeb6, 'high byte', align=Align.INLINE)
d.comment(0xaeb8, 'OSWORD &01: read the centisecond clock into IWA', align=Align.INLINE)
d.comment(0xaebd, 'Integer result', align=Align.INLINE)
d.comment(0xaebf, 'Return TIME', align=Align.INLINE)

# fn_page (&AEC0): =PAGE
d.comment(0xaec0, 'PAGE low byte is always 0...', align=Align.INLINE)
d.comment(0xaec2, '...high byte is the page number', align=Align.INLINE)
d.comment(0xaec4, 'Return PAGE as an integer', align=Align.INLINE)
d.comment(0xaec7, 'syntax error (shared)', align=Align.INLINE)
# pseudo-var / FALSE / RND state
d.label(0xaec7, 'pseudovar_syntax_error')
# fn_false (&AECA): FALSE = 0
d.comment(0xaeca, 'FALSE is 0', align=Align.INLINE)
d.comment(0xaecc, 'Return 0 as an integer', align=Align.INLINE)

d.comment(0xaece, 'String operand here is a Type mismatch', align=Align.INLINE)

d.label(0xaece, 'bool_type_error')
# fn_len (&AED1): LEN(s$).
d.comment(0xaed1, 'Evaluate the string', align=Align.INLINE)
d.comment(0xaed4, 'not a string: error', align=Align.INLINE)
d.comment(0xaed6, 'Length, returned as an integer', align=Align.INLINE)

d.subroutine(0xaed8, 'int_result_a',
             title='Return A as an integer result',
             description='Set IWA to the unsigned byte in A (high bytes zero) '
                         'and report the integer type. The common tail for '
                         'functions returning a small integer.',
             on_entry={'A': 'the unsigned byte to return'},
             on_exit={'zp_iwa (&2A-&2D)': 'A zero-extended to 32 bits',
                      'A': 'integer type marker (&40)',
                      'X': 'preserved'})
# int_result_a (&AED8).
d.comment(0xaed8, 'High byte zero', align=Align.INLINE)
d.comment(0xaeda, 'return A as the integer', align=Align.INLINE)

# fn_to (&AEDC): TO followed by "P" returns TOP (end of program)
d.comment(0xaedc, 'Look at the character after TO', align=Align.INLINE)
d.comment(0xaede, '(get it)', align=Align.INLINE)
d.comment(0xaee0, 'Is it "P"? TO + P spells TOP', align=Align.INLINE)
d.char_literal(0xaee1)
d.comment(0xaee2, 'No: a bare TO here is a syntax error', align=Align.INLINE)
d.comment(0xaee4, 'Consume the P', align=Align.INLINE)
d.comment(0xaee6, 'TOP: end-of-program address, low byte', align=Align.INLINE)
d.comment(0xaee8, 'high byte (returned as an integer)', align=Align.INLINE)

d.subroutine(
    0xaeea, 'iwa_from_ya',
    title='Set the integer accumulator to a small integer',
    description='IWA = 256*Y + A, zero-extended to 32 bits (unsigned '
                '0-65535), then report the integer type.',
    on_entry={'A': 'low byte', 'Y': 'high byte'},
    on_exit={'zp_iwa (&2A-&2D)': '256*Y + A (unsigned, top two bytes zero)',
             'A': 'integer type marker (&40)', 'X': 'preserved'},
)
# iwa_from_ya (&AEEA): IWA = unsigned 256*Y + A
d.comment(0xaeea, 'Low byte (A) into IWA byte 0', align=Align.INLINE)
d.comment(0xaeec, 'High byte (Y) into IWA byte 1', align=Align.INLINE)
# --- iwa_from_ya: build a 16-bit (unsigned) integer in the IWA -------
d.comment(0xaeee, 'Clear the top 16 bits: the result is 0-65535',
          align=Align.INLINE)
d.comment(0xaef0, 'Clear IWA byte 2', align=Align.INLINE)
d.comment(0xaef2, 'Clear byte 3: the value is unsigned 0-65535', align=Align.INLINE)
d.comment(0xaef4, 'Report the value as an integer (type &40)',
          align=Align.INLINE)

d.comment(0xaef6, 'Return the integer', align=Align.INLINE)

# fn_count (&AEF7): COUNT
d.comment(0xaef7, 'COUNT: characters printed since the last newline',
          align=Align.INLINE)
d.comment(0xaef9, 'Return it as an integer', align=Align.INLINE)

# fn_lomem (&AEFC): =LOMEM
d.comment(0xaefc, 'LOMEM low byte', align=Align.INLINE)
d.comment(0xaefe, 'high byte', align=Align.INLINE)
d.comment(0xaf00, 'Return LOMEM as an integer', align=Align.INLINE)
# fn_himem (&AF03): HIMEM.
d.comment(0xaf03, 'HIMEM low', align=Align.INLINE)
d.comment(0xaf05, 'HIMEM high', align=Align.INLINE)
d.comment(0xaf07, 'return as an integer', align=Align.INLINE)

d.label(0xaf0a, 'rnd_dispatch')   # RND(expr): select the form by argument

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

d.subroutine(
    0xaf24, 'rnd_range',
    title='RND(X), X>=2: a random integer 1 to X',
    description="""Compute 1 + INT(RND(1) * X). int_to_fwa(X), push X
(stack_real), take a fraction (rnd_fraction), pop X back into the
operand (unstack_real), multiply (fwa_mul_var_raw), convert to an
integer (fwa_to_int) and add one (iwa_inc), giving a value in 1..X.
""",
    on_entry={'zp_iwa (&2A-&2D)': 'the upper bound X (>= 2)'},
    on_exit={'zp_iwa (&2A-&2D)': 'a random integer in 1..X',
             'zp_fwa / zp_fwb': 'corrupted (scratch)'},
)
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

d.subroutine(
    0xaf3f, 'rnd_seed',
    title='RND(-X): seed the generator and return X',
    description="""Store the integer argument into the 32-bit state (&0D-&10) and
set &11 to &40. Only bit 0 of &11 is part of the LFSR, so the
overflow bit becomes 0. Returns the argument as an integer.
""",
    on_entry={'zp_iwa (&2A-&2D)': 'the seed value'},
    on_exit={'zp_rnd_seed (&0D-&11)': 'reseeded from IWA',
             'zp_iwa': 'unchanged (the returned value)',
             'A': 'integer type marker (&40)'},
)
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
d.char_literal(0xaf4e)
d.comment(0xaf4f, 'Yes: select the RND form', align=Align.INLINE)

d.subroutine(
    0xaf51, 'rnd_integer',
    title='RND: a full-range random integer',
    description="""Bare RND. Advance the generator (rnd_step) then read the
32-bit state (&0D-&10) into IWA as a signed integer, returning the
integer type (&40). The result spans the full signed 32-bit range.
""",
    on_entry={'zp_rnd_seed (&0D-&11)': 'the current generator state'},
    on_exit={'zp_rnd_seed': 'advanced one step',
             'zp_iwa (&2A-&2D)': 'the random 32-bit integer',
             'A': 'integer type marker (&40)'},
)
# rnd_integer (&AF51): bare RND
d.comment(0xaf51, 'Advance the generator', align=Align.INLINE)
d.comment(0xaf54, 'Point at the state (&0D), then copy it to IWA',
          align=Align.INLINE)

d.subroutine(
    0xaf56, 'iwa_load_zp',
    title='Load a zero-page integer variable into the accumulator',
    description='Copy the 4-byte integer at &00+X (a resident integer variable '
                'A%-Z% or @%) into IWA, then report the integer type.',
    on_entry={'X': 'zero-page offset of the source variable (from &00)'},
    on_exit={'zp_iwa (&2A-&2D)': 'the loaded integer',
             'A': 'integer type marker (&40)',
             'X': 'preserved', 'Y': 'preserved'},
)
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

d.subroutine(
    0xaf69, 'rnd_fraction',
    title='RND(1): a random real in [0, 1)',
    description="""Advance the generator (rnd_step) then fall into rnd_repeat to
build the fraction. The value is the byte-reversed 32-bit state
divided by 2^32: a real in [0, 1).
""",
    on_entry={'zp_rnd_seed (&0D-&11)': 'the current generator state'},
    on_exit={'zp_rnd_seed': 'advanced one step',
             'zp_fwa (&2E-&35)': 'a normalised real in [0, 1)',
             'A': 'real type marker (&FF)'},
)
# rnd_fraction (&AF69) -> rnd_repeat (&AF6C): build the [0,1) fraction
d.comment(0xaf69, 'Advance the generator, then build the fraction',
          align=Align.INLINE)
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
    on_entry={'zp_rnd_seed (&0D-&10)': 'the current 32-bit generator state'},
    on_exit={'zp_fwa (&2E-&35)': 'a normalised real in [0, 1)',
             'A': 'real type marker (&FF)', 'X': 'corrupted'},
)
d.comment(0xaf6c, 'Zero for the FP fields', align=Align.INLINE)
d.comment(0xaf6e, 'Sign positive', align=Align.INLINE)
d.comment(0xaf70, 'Clear overflow', align=Align.INLINE)
d.comment(0xaf72, 'Clear rounding', align=Align.INLINE)
d.comment(0xaf74, 'Exponent &80 (= 2^0)', align=Align.INLINE)
d.comment(0xaf76, '(store it)', align=Align.INLINE)
d.comment(0xaf78, 'State byte X (little-endian)...', align=Align.INLINE)
d.label(0xaf78, 'rnd_state_loop')
d.comment(0xaf7a, '...into mantissa byte X (MSB first): byte-reverses',
          align=Align.INLINE)
d.comment(0xaf7c, 'next byte', align=Align.INLINE)
d.comment(0xaf7d, 'all four?', align=Align.INLINE)
d.comment(0xaf7f, 'loop', align=Align.INLINE)
d.comment(0xaf81, 'Normalise: value = reversed-state / 2^32', align=Align.INLINE)
d.comment(0xaf84, 'Real result type', align=Align.INLINE)
d.comment(0xaf86, 'Return RND(1) / RND(0)', align=Align.INLINE)

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
    on_entry={'zp_rnd_seed (&0D-&11)': 'the 33-bit generator state'},
    on_exit={'zp_rnd_seed': 'advanced by 32 steps',
             'X': 'preserved'},
)
# rnd_step (&AF87): one RND advance = 32 LFSR steps, trinomial (33,20,0)
d.comment(0xaf87, '32 single-bit steps make one RND advance', align=Align.INLINE)
d.comment(0xaf89, 'Byte 2 holds register bits 16-23', align=Align.INLINE)
d.label(0xaf89, 'rnd_step_loop')
d.comment(0xaf8b, 'Shift right so bit 19 (tap 20)...', align=Align.INLINE)
d.comment(0xaf8c, 'shifting it down', align=Align.INLINE)
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

# fn_erl (&AF9F): ERL
d.comment(0xaf9f, 'ERL high byte', align=Align.INLINE)
d.comment(0xafa1, 'low byte', align=Align.INLINE)
d.comment(0xafa3, 'Return ERL as an integer', align=Align.INLINE)
# fn_err (&AFA6): ERR
d.comment(0xafa6, 'Read the error number...', align=Align.INLINE)
d.comment(0xafa8, '...from the error block (&FD)', align=Align.INLINE)
d.comment(0xafaa, 'Return ERR as an integer', align=Align.INLINE)
d.subroutine(0xafad, 'read_key_timed', title='Read a key within a time limit (INKEY)',
             description='Evaluate the time-limit argument at PtrB into IWA, then '
                         'tail-call OSBYTE &81 (INKEY) to read a key with that '
                         'timeout. Shared by the INKEY and INKEY$ functions.',
             on_entry={'zp_text_ptr2 (&19/&1A)': 'PtrB at the time-limit argument'},
             on_exit={'X': 'the key code (or internal key number on a scan)',
                      'Y': '0 if a key was read, &FF on timeout, &1B on Escape',
                      'C': 'per OSBYTE &81'})

# read_key_timed (&AFAD) remaining
d.comment(0xafad, 'Evaluate the time-limit argument', align=Align.INLINE)
d.comment(0xafb0, 'OSBYTE &81: INKEY (read a key with a timeout)', align=Align.INLINE)
d.comment(0xafb2, 'time limit low', align=Align.INLINE)
d.comment(0xafb4, 'time limit high', align=Align.INLINE)

# fn_get (&AFB9): GET; fn_pos (&AB6D): POS
d.comment(0xafbc, 'Return the key code as an integer', align=Align.INLINE)
# fn_gets (&AFBF): GET$ - a key as a one-character string
d.comment(0xafbf, 'Wait for a key', align=Align.INLINE)
d.comment(0xafc2, 'Store it as the one-character string body', align=Align.INLINE)
# string functions: GET$/LEFT$/RIGHT$/INKEY$/MID$/STR$/STRING$
d.label(0xafc2, 'gets_char')
d.comment(0xafc5, 'Length 1', align=Align.INLINE)
d.comment(0xafc7, '(store)', align=Align.INLINE)
d.comment(0xafc9, 'String type', align=Align.INLINE)
d.comment(0xafcb, 'Return the one-character string', align=Align.INLINE)

# fn_lefts (&AFCC): LEFT$(s$, n) - keep the first n characters.
d.comment(0xafcc, 'Evaluate the source string', align=Align.INLINE)
d.comment(0xafcf, 'not a string: Type mismatch', align=Align.INLINE)
d.comment(0xafd1, "','?", align=Align.INLINE)
d.char_literal(0xafd2)
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
d.label(0xafeb, 'lefts_result')
d.comment(0xafed, 'Return', align=Align.INLINE)

# fn_rights (&AFEE): RIGHT$(s$, n) - keep the last n characters.
d.comment(0xafee, 'Evaluate the source string', align=Align.INLINE)
d.comment(0xaff1, 'not a string: Type mismatch', align=Align.INLINE)
d.comment(0xaff3, "','?", align=Align.INLINE)
d.char_literal(0xaff4)
d.comment(0xaff5, 'no: Missing ,', align=Align.INLINE)
d.comment(0xaff7, 'step past', align=Align.INLINE)
d.comment(0xaff9, 'Stack the string', align=Align.INLINE)
d.comment(0xaffc, 'Evaluate the count, expect )', align=Align.INLINE)
d.comment(0xafff, 'coerce to integer', align=Align.INLINE)
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
d.label(0xb017, 'rights_copy_down')   # RIGHT$ tail-to-front shift loop
d.comment(0xb017, 'Read a kept char from the tail (at X)', align=Align.INLINE)
d.comment(0xb01a, 'Pack it down to the front (at Y)', align=Align.INLINE)
d.comment(0xb01d, 'Advance the read cursor', align=Align.INLINE)
d.comment(0xb01e, 'Advance the write cursor', align=Align.INLINE)
d.comment(0xb01f, 'One fewer char to move', align=Align.INLINE)
d.comment(0xb021, 'Until all `count` chars are shifted down', align=Align.INLINE)
d.comment(0xb023, 'Keep the whole string', align=Align.INLINE)
d.label(0xb023, 'rights_whole')
d.comment(0xb025, 'Return', align=Align.INLINE)

# fn_inkeys (&B026): INKEY$ - a timed key as a string
d.comment(0xb026, 'Read a key within the time limit', align=Align.INLINE)
d.comment(0xb029, 'X holds the key', align=Align.INLINE)
d.comment(0xb02a, 'Y=0 means a key was read', align=Align.INLINE)
d.comment(0xb02c, 'Got one: return it as a 1-char string', align=Align.INLINE)
d.comment(0xb02e, 'Timeout: empty string', align=Align.INLINE)
d.label(0xb02e, 'inkeys_timeout')
d.comment(0xb030, 'length 0', align=Align.INLINE)
d.comment(0xb032, 'Return the (possibly empty) string', align=Align.INLINE)
d.comment(0xb033, 'Type mismatch (shared)', align=Align.INLINE)
d.label(0xb033, 'str_type_error')
d.comment(0xb036, 'Missing , error (shared)', align=Align.INLINE)

d.label(0xb036, 'str_missing_comma')
# fn_mids (&B039): MID$(s$, p [, n]) - substring from position p.
d.comment(0xb039, 'Evaluate the source string', align=Align.INLINE)
d.comment(0xb03c, 'not a string: Type mismatch', align=Align.INLINE)
d.comment(0xb03e, "','?", align=Align.INLINE)
d.char_literal(0xb03f)
d.comment(0xb040, 'no: Missing ,', align=Align.INLINE)
d.comment(0xb042, 'Stack the string', align=Align.INLINE)
d.comment(0xb045, 'step past', align=Align.INLINE)
d.comment(0xb047, 'Evaluate the start position', align=Align.INLINE)
d.comment(0xb04a, 'Save it', align=Align.INLINE)
d.comment(0xb04c, 'push the start position', align=Align.INLINE)
d.comment(0xb04d, 'Default length = 255', align=Align.INLINE)
d.comment(0xb04f, 'as the length', align=Align.INLINE)
d.comment(0xb051, 'step past', align=Align.INLINE)
d.comment(0xb053, "')' (no length given)?", align=Align.INLINE)
d.char_literal(0xb054)
d.comment(0xb055, 'yes: use the default', align=Align.INLINE)
d.comment(0xb057, "','?", align=Align.INLINE)
d.char_literal(0xb058)
d.comment(0xb059, 'no: Missing ,', align=Align.INLINE)
d.comment(0xb05b, 'Evaluate the length, expect )', align=Align.INLINE)
d.comment(0xb05e, 'coerce to integer', align=Align.INLINE)
d.comment(0xb061, 'Restore the string', align=Align.INLINE)
d.label(0xb061, 'mids_restore')
d.comment(0xb064, 'Start position', align=Align.INLINE)
d.comment(0xb065, 'into Y (also tests for 0),', align=Align.INLINE)
d.comment(0xb066, 'clear carry for the compare', align=Align.INLINE)
d.comment(0xb067, 'position 0: treat as 1', align=Align.INLINE)
d.comment(0xb069, 'past the end?', align=Align.INLINE)
d.comment(0xb06b, 'yes: empty string', align=Align.INLINE)
d.comment(0xb06d, 'Zero-based start = p - 1', align=Align.INLINE)
d.comment(0xb06e, 'A = start - 1', align=Align.INLINE)
d.comment(0xb06f, 'Save the start offset', align=Align.INLINE)
d.label(0xb06f, 'mids_start')
d.comment(0xb071, 'also into X (source index)', align=Align.INLINE)
d.comment(0xb072, 'Destination index', align=Align.INLINE)
d.comment(0xb074, 'Available = length - start', align=Align.INLINE)
d.comment(0xb076, 'set carry,', align=Align.INLINE)
d.comment(0xb077, 'length - start offset', align=Align.INLINE)
d.comment(0xb079, 'more than requested?', align=Align.INLINE)
d.comment(0xb07b, 'no: use the available count', align=Align.INLINE)
d.comment(0xb07d, 'clamp the length', align=Align.INLINE)
d.comment(0xb07f, 'Length', align=Align.INLINE)
d.label(0xb07f, 'mids_length')
d.comment(0xb081, 'zero: empty string', align=Align.INLINE)
d.comment(0xb083, 'Copy the substring to the front', align=Align.INLINE)
d.label(0xb083, 'mids_copy_loop')
d.comment(0xb086, 'to the front,', align=Align.INLINE)
d.comment(0xb089, 'next dest,', align=Align.INLINE)
d.comment(0xb08a, 'next source,', align=Align.INLINE)
d.comment(0xb08b, 'copied the requested length?', align=Align.INLINE)
d.comment(0xb08d, 'loop', align=Align.INLINE)
d.comment(0xb08f, 'Set the result length', align=Align.INLINE)
d.comment(0xb091, 'String result', align=Align.INLINE)
d.comment(0xb093, 'Return', align=Align.INLINE)

# fn_strs (&B094): STR$(x) and STR$~(x).
d.comment(0xb094, 'Next character', align=Align.INLINE)
d.comment(0xb097, 'assume hex', align=Align.INLINE)
d.comment(0xb099, "'~' hex prefix?", align=Align.INLINE)
d.char_literal(0xb09a)
d.comment(0xb09b, 'yes', align=Align.INLINE)
d.comment(0xb09d, 'no: decimal', align=Align.INLINE)
d.comment(0xb09f, 'back up', align=Align.INLINE)
d.comment(0xb0a1, 'Save the hex/dec flag', align=Align.INLINE)
d.label(0xb0a1, 'strs_save_flag')
d.comment(0xb0a2, 'push it', align=Align.INLINE)
d.comment(0xb0a3, 'Evaluate the number', align=Align.INLINE)
d.comment(0xb0a6, 'string: error', align=Align.INLINE)
d.comment(0xb0a8, 'Restore the flag', align=Align.INLINE)
d.comment(0xb0a9, 'recover the hex/dec flag', align=Align.INLINE)
d.comment(0xb0ab, '@% formatting set?', align=Align.INLINE)
d.comment(0xb0ae, 'yes: use it', align=Align.INLINE)
d.comment(0xb0b0, 'Default conversion', align=Align.INLINE)
d.comment(0xb0b2, 'clear &37 (default format)', align=Align.INLINE)
d.comment(0xb0b5, 'string result', align=Align.INLINE)
d.comment(0xb0b7, 'Return', align=Align.INLINE)
d.comment(0xb0b8, 'Return', align=Align.INLINE)
d.comment(0xb0b9, 'Formatted conversion (@%)', align=Align.INLINE)
d.label(0xb0b9, 'strs_formatted')
d.comment(0xb0bc, 'string result', align=Align.INLINE)
d.comment(0xb0be, 'Return', align=Align.INLINE)
d.comment(0xb0bf, 'Type mismatch error', align=Align.INLINE)

d.label(0xb0bf, 'strs_type_error')
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
d.label(0xb0df, 'strings_append')
d.comment(0xb0e1, 'source char...', align=Align.INLINE)
d.label(0xb0e1, 'strings_copy_loop')
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
d.label(0xb0f5, 'strings_type')
d.comment(0xb0f7, 'Return', align=Align.INLINE)
d.comment(0xb0f8, 'empty result (length 0)', align=Align.INLINE)
d.label(0xb0f8, 'strings_empty')
d.comment(0xb0fa, 'Return', align=Align.INLINE)
d.comment(0xb0fb, 'String too long error', align=Align.INLINE)
d.label(0xb0fb, 'strings_too_long')
# find_def (&B112) and the "No such FN/PROC" path
d.comment(0xb0fe, 'No such FN/PROC: restore the text pointer', align=Align.INLINE)
d.label(0xb0fe, 'no_such_fn_proc')

d.comment(0xb0ff, 'pointer high', align=Align.INLINE)
d.comment(0xb101, 'pull the low byte', align=Align.INLINE)
d.comment(0xb102, 'pointer low', align=Align.INLINE)
d.comment(0xb104, '"No such FN/PROC" error block', align=Align.INLINE)
d.subroutine(0xb112, 'find_def', title='Find a PROC/FN definition by name',
             description='Walk the program from PAGE for the DEF PROC/FN line '
                         'whose name matches the reference at (zp_general), then '
                         'cache its body address in the variable entry so later '
                         'calls resolve quickly. Raises No such FN/PROC.',
             on_entry={'(zp_general) (&37/&38)': 'the PROC/FN name reference'},
             on_exit={'the variable entry': 'updated with the cached body address',
                      'BRK': 'No such FN/PROC if no matching DEF exists'})

d.comment(0xb112, 'Search from PAGE: high', align=Align.INLINE)
d.comment(0xb114, '(store)', align=Align.INLINE)
d.comment(0xb116, 'low 0', align=Align.INLINE)
d.comment(0xb118, '(store)', align=Align.INLINE)
d.comment(0xb11a, 'line number high byte', align=Align.INLINE)
# find_def
d.label(0xb11a, 'finddef_scan')
d.comment(0xb11c, 'read it', align=Align.INLINE)
d.comment(0xb11e, 'end of program: not found', align=Align.INLINE)
d.comment(0xb120, 'skip to the line body', align=Align.INLINE)
d.comment(0xb122, 'advance', align=Align.INLINE)
d.label(0xb122, 'finddef_advance')
d.comment(0xb123, 'char', align=Align.INLINE)
d.comment(0xb125, 'skip leading spaces', align=Align.INLINE)
d.char_literal(0xb126)
d.comment(0xb127, 'skip it', align=Align.INLINE)
d.comment(0xb129, 'DEF token at the start?', align=Align.INLINE)
d.comment(0xb12b, 'yes: check the name', align=Align.INLINE)
d.comment(0xb12d, 'no DEF: skip to the next line', align=Align.INLINE)
d.label(0xb12d, 'finddef_next_line')
d.comment(0xb12f, 'line length', align=Align.INLINE)
d.comment(0xb131, 'add the line length...', align=Align.INLINE)
d.comment(0xb132, 'to the pointer low,', align=Align.INLINE)
d.comment(0xb134, '(store)', align=Align.INLINE)
d.comment(0xb136, 'no carry', align=Align.INLINE)
d.comment(0xb138, 'carry into the pointer high', align=Align.INLINE)
d.comment(0xb13a, 'next line', align=Align.INLINE)
d.comment(0xb13c, 'DEF found: skip past the FN/PROC token', align=Align.INLINE)
d.label(0xb13c, 'finddef_found')
d.comment(0xb13d, '(store the offset)', align=Align.INLINE)
d.comment(0xb13f, 'skip spaces', align=Align.INLINE)
d.comment(0xb142, 'point at the definition name:', align=Align.INLINE)
d.comment(0xb143, 'X = the name offset', align=Align.INLINE)
d.comment(0xb144, 'pointer + offset:', align=Align.INLINE)
d.comment(0xb145, 'low,', align=Align.INLINE)
d.comment(0xb147, 'high,', align=Align.INLINE)
d.comment(0xb149, 'no carry', align=Align.INLINE)
d.comment(0xb14b, 'carry into high', align=Align.INLINE)
d.comment(0xb14c, '(borrow for the -1)', align=Align.INLINE)
d.comment(0xb14d, 'minus 1 (loop pre-increments Y)', align=Align.INLINE)
d.label(0xb14d, 'finddef_name_setup')
d.comment(0xb14f, '(save pointer low)', align=Align.INLINE)
d.comment(0xb151, 'high byte...', align=Align.INLINE)
d.comment(0xb152, 'minus the borrow', align=Align.INLINE)
d.comment(0xb154, '(save pointer high)', align=Align.INLINE)
d.comment(0xb156, 'Compare the definition name with the called name:', align=Align.INLINE)
d.comment(0xb158, 'next char', align=Align.INLINE)
d.label(0xb158, 'finddef_match_loop')
d.comment(0xb159, 'advance both cursors', align=Align.INLINE)
d.comment(0xb15a, 'definition char', align=Align.INLINE)
d.comment(0xb15c, 'vs called char', align=Align.INLINE)
d.comment(0xb15e, 'differ: next line', align=Align.INLINE)
d.comment(0xb160, 'end of the called name?', align=Align.INLINE)
d.comment(0xb162, 'no: keep comparing', align=Align.INLINE)
d.comment(0xb164, 'definition name also ends?', align=Align.INLINE)
d.comment(0xb165, 'read the next def char', align=Align.INLINE)
d.comment(0xb167, 'alphanumeric?', align=Align.INLINE)
d.comment(0xb16a, 'definition name is longer: next line', align=Align.INLINE)
d.comment(0xb16c, 'Match: cache the definition', align=Align.INLINE)
d.comment(0xb16d, 'Y = name length', align=Align.INLINE)
d.comment(0xb16e, 'point PtrA at the body', align=Align.INLINE)
d.comment(0xb171, 'create/find the FN/PROC entry', align=Align.INLINE)
d.comment(0xb174, 'init it', align=Align.INLINE)
d.comment(0xb176, 'initialise the value', align=Align.INLINE)
d.comment(0xb179, 'store the body pointer:', align=Align.INLINE)
d.comment(0xb17b, 'pointer low...', align=Align.INLINE)
d.comment(0xb17d, '(store)', align=Align.INLINE)
d.comment(0xb17f, 'next byte', align=Align.INLINE)
d.comment(0xb180, 'pointer high...', align=Align.INLINE)
d.comment(0xb182, '(store)', align=Align.INLINE)
d.comment(0xb184, 'advance VARTOP', align=Align.INLINE)
d.comment(0xb187, 'continue', align=Align.INLINE)
d.comment(0xb18a, 'error block', align=Align.INLINE)

d.label(0xb18a, 'finddef_not_found')
# fn_fn (&B195): FN calls a user function via call_proc_fn
d.comment(0xb195, 'FN token: enter via the PROC/FN call mechanism', align=Align.INLINE)

# --- PROC / FN / LOCAL / ENDPROC -------------------------------------
d.subroutine(
    0xb197, 'call_proc_fn',
    title='Enter a PROC or FN',
    description="""The procedure/function call mechanism. It lets PROCs and FNs
nest far beyond the 256-byte 6502 stack by *moving* that stack out of
the way for each call:

1. Copy the whole live 6502 stack onto the BASIC value stack (the
   saved stack pointer first, then every byte), then empty the
   hardware stack (`txs` with X = &FF). The frame below is therefore
   built from &01FF downwards.
2. Push the call frame (the table).
3. Locate the named definition (heap cache, else a program scan),
   bind any parameters, and `jsr next_statement` to run the body.

The 10-byte call frame, on the freshly emptied hardware stack while
the body runs (deepest byte first):

| Addr  | Byte                    | From |
|-------|-------------------------|------|
| &01FF | PROC token &F2 / FN &A4 | &27  |
| &01FE | caller PtrA offset      | &0A  |
| &01FD | caller PtrA low         | &0B  |
| &01FC | caller PtrA high        | &0C  |
| &01FB | LOCAL/parameter count   | -    |
| &01FA | PtrB offset             | &1B  |
| &01F9 | PtrB low                | &19  |
| &01F8 | PtrB high               | &1A  |
| &01F7 | body return high        | jsr  |
| &01F6 | body return low         | jsr  |

The addresses are absolute because the stack was just emptied -- which
is why [`stmt_endproc`](address:9356) reads the framed token at
`hw_stack_top` (&01FF) and [`stmt_local`](address:9323) bumps the count
through `frame_local_count` (&0106,X with X = &F5, i.e. &01FB).

Unwinding is indirect: ENDPROC and `=expr` do not pop the frame. They
verify the framed token, then fall into the end-of-statement path
whose `rts` pops the body return (&01F6/&01F7) straight back here, to
&B20E. From there this routine restores PtrB, replays the count by
popping that many (variable address, saved value) pairs off the BASIC
value stack to undo the LOCALs/parameters, restores the caller's PtrA,
and copies the saved 6502 stack back into page 1.

What is NOT saved: only the hardware stack and the BASIC value stack
are preserved. The FOR/REPEAT/GOSUB stacks (page 5, counters
&26/&24/&25) are global and untouched, so a loop left early via
ENDPROC or GOTO leaks its frame. See [`stmt_endproc`](address:9356)
and the page-5 control-flow stacks at &0500.
""",
    on_entry={'A': 'PROC token &F2 or FN token &A4'},
)
# ----------------------------------------------------------------------
# call_proc_fn (&B197): invoke a PROC or FN.
# Saves the 6502 stack onto the BASIC stack (so calls can nest beyond
# 256 bytes / recurse), pushes the return context, parses and locates
# the definition (heap cache then program scan), runs the body, restores
# any LOCAL/parameter values, and unwinds the saved stack.
# ----------------------------------------------------------------------
d.comment(0xb197, 'Save the PROC/FN token', align=Align.INLINE)
d.comment(0xb199, 'Copy the 6502 stack onto the BASIC stack', align=Align.INLINE)
d.comment(0xb19a, 'stack pointer to A,', align=Align.INLINE)
d.comment(0xb19b, 'add the BASIC stack pointer', align=Align.INLINE)
d.comment(0xb19c, 'Drop the BASIC stack by the 6502 stack size',
          align=Align.INLINE)
d.comment(0xb19e, 'so procedures can nest far beyond 256 bytes',
          align=Align.INLINE)
d.comment(0xb1a1, 'Store the 6502 stack pointer first', align=Align.INLINE)
d.comment(0xb1a3, 'the saved SP,', align=Align.INLINE)
d.comment(0xb1a4, 'at offset 0', align=Align.INLINE)
d.comment(0xb1a6, 'Copy each 6502 stack byte', align=Align.INLINE)
# call_proc_fn
d.label(0xb1a6, 'callpf_save_stack')
d.comment(0xb1a7, 'next dest,', align=Align.INLINE)
d.comment(0xb1a8, 'read a stack byte,', align=Align.INLINE)
d.comment(0xb1ab, 'to the BASIC stack,', align=Align.INLINE)
d.comment(0xb1ad, 'whole stack copied?', align=Align.INLINE)
d.comment(0xb1af, 'loop', align=Align.INLINE)
d.comment(0xb1b1, 'Empty the 6502 stack', align=Align.INLINE)
d.comment(0xb1b2, 'PROC/FN token', align=Align.INLINE)
d.comment(0xb1b4, "Push the call context and return pointers", align=Align.INLINE)
d.comment(0xb1b5, 'return line offset', align=Align.INLINE)
d.comment(0xb1b7, 'push it', align=Align.INLINE)
d.comment(0xb1b8, 'return line pointer', align=Align.INLINE)
d.comment(0xb1ba, 'push low,', align=Align.INLINE)
d.comment(0xb1bb, 'high byte,', align=Align.INLINE)
d.comment(0xb1bd, 'push high', align=Align.INLINE)
d.comment(0xb1be, 'Point &37/&38 at the PROC/FN name', align=Align.INLINE)
d.comment(0xb1c0, 'keep the offset,', align=Align.INLINE)
d.comment(0xb1c1, 'add the parser pointer:', align=Align.INLINE)
d.comment(0xb1c2, 'low byte,', align=Align.INLINE)
d.comment(0xb1c4, 'high byte in Y,', align=Align.INLINE)
d.comment(0xb1c6, 'no carry,', align=Align.INLINE)
d.comment(0xb1c8, 'carry into high,', align=Align.INLINE)
d.comment(0xb1c9, 'clear carry,', align=Align.INLINE)
d.comment(0xb1ca, 'back up one: low,', align=Align.INLINE)
d.label(0xb1ca, 'callpf_back')
d.comment(0xb1cc, 'to &37,', align=Align.INLINE)
d.comment(0xb1ce, 'high byte,', align=Align.INLINE)
d.comment(0xb1cf, 'with borrow,', align=Align.INLINE)
d.comment(0xb1d1, 'to &38', align=Align.INLINE)
d.comment(0xb1d3, 'Validate the name', align=Align.INLINE)
d.comment(0xb1d5, 'scan it from offset 2', align=Align.INLINE)
d.comment(0xb1d8, 'no valid characters?', align=Align.INLINE)
d.comment(0xb1da, 'yes: Bad call', align=Align.INLINE)
d.comment(0xb1dc, 'Offset past the name', align=Align.INLINE)
d.comment(0xb1de, 'Name length', align=Align.INLINE)
d.comment(0xb1df, 'store it (&39)', align=Align.INLINE)
d.comment(0xb1e1, 'Look it up in the heap cache', align=Align.INLINE)
d.comment(0xb1e4, 'found: jump to it', align=Align.INLINE)
d.comment(0xb1e6, 'not cached: scan the program', align=Align.INLINE)
d.comment(0xb1e9, 'Set PtrA to the definition address', align=Align.INLINE)
d.label(0xb1e9, 'callpf_set_ptr')
d.comment(0xb1eb, 'low byte,', align=Align.INLINE)
d.comment(0xb1ed, 'to PtrA low,', align=Align.INLINE)
d.comment(0xb1ef, 'next,', align=Align.INLINE)
d.comment(0xb1f0, 'high byte,', align=Align.INLINE)
d.comment(0xb1f2, 'to PtrA high', align=Align.INLINE)
d.comment(0xb1f4, 'Push the parameter count (0 so far)', align=Align.INLINE)
d.label(0xb1f4, 'callpf_push_count')
d.comment(0xb1f6, 'push it,', align=Align.INLINE)
d.comment(0xb1f7, 'offset = 0', align=Align.INLINE)
d.comment(0xb1f9, 'Next character', align=Align.INLINE)
d.comment(0xb1fc, "'(' parameters?", align=Align.INLINE)
d.char_literal(0xb1fd)
d.comment(0xb1fe, 'yes: bind them', align=Align.INLINE)
d.comment(0xb200, 'no: back up', align=Align.INLINE)
d.comment(0xb202, 'Save the parser pointer', align=Align.INLINE)
d.label(0xb202, 'callpf_save_parser')
d.comment(0xb204, 'push offset,', align=Align.INLINE)
d.comment(0xb205, 'low byte,', align=Align.INLINE)
d.comment(0xb207, 'push low,', align=Align.INLINE)
d.comment(0xb208, 'high byte,', align=Align.INLINE)
d.comment(0xb20a, 'push high', align=Align.INLINE)
d.comment(0xb20b, 'Execute the body', align=Align.INLINE)
d.comment(0xb20e, 'Restore the parser pointer', align=Align.INLINE)
d.comment(0xb20f, 'high byte,', align=Align.INLINE)
d.comment(0xb211, 'pull low,', align=Align.INLINE)
d.comment(0xb212, 'low byte,', align=Align.INLINE)
d.comment(0xb214, 'pull offset,', align=Align.INLINE)
d.comment(0xb215, 'offset', align=Align.INLINE)
d.comment(0xb217, 'Number of LOCAL/parameter values to restore',
          align=Align.INLINE)
d.comment(0xb218, 'none: skip', align=Align.INLINE)
d.comment(0xb21a, 'count', align=Align.INLINE)
d.comment(0xb21c, 'Unstack the variable address', align=Align.INLINE)
d.label(0xb21c, 'callpf_restore_locals')
d.comment(0xb21f, 'restore its saved value', align=Align.INLINE)
d.comment(0xb222, 'one done', align=Align.INLINE)
d.comment(0xb224, 'loop', align=Align.INLINE)
d.comment(0xb226, 'Restore PtrA', align=Align.INLINE)
d.label(0xb226, 'callpf_restore_ptr')
d.comment(0xb227, 'high byte,', align=Align.INLINE)
d.comment(0xb229, 'pull low,', align=Align.INLINE)
d.comment(0xb22a, 'low byte,', align=Align.INLINE)
d.comment(0xb22c, 'pull offset,', align=Align.INLINE)
d.comment(0xb22d, 'offset', align=Align.INLINE)
d.comment(0xb22f, 'Recover the saved 6502 stack pointer', align=Align.INLINE)
d.comment(0xb230, 'from offset 0,', align=Align.INLINE)
d.comment(0xb232, 'the saved SP,', align=Align.INLINE)
d.comment(0xb234, 'into X', align=Align.INLINE)
d.comment(0xb235, 'restore it', align=Align.INLINE)
d.comment(0xb236, 'Copy each byte back to the 6502 stack', align=Align.INLINE)
d.label(0xb236, 'callpf_restore_stack')
d.comment(0xb237, 'next slot,', align=Align.INLINE)
d.comment(0xb238, 'read from the BASIC stack,', align=Align.INLINE)
d.comment(0xb23a, 'to the 6502 stack,', align=Align.INLINE)
d.comment(0xb23d, 'whole stack restored?', align=Align.INLINE)
d.comment(0xb23f, 'loop', align=Align.INLINE)
d.comment(0xb241, 'Adjust the BASIC stack pointer back up', align=Align.INLINE)
d.comment(0xb242, 'free the copied bytes,', align=Align.INLINE)
d.comment(0xb244, 'store low,', align=Align.INLINE)
d.comment(0xb246, 'no carry,', align=Align.INLINE)
d.comment(0xb248, 'carry into high', align=Align.INLINE)
d.comment(0xb24a, 'Return the PROC/FN token', align=Align.INLINE)
d.label(0xb24a, 'callpf_return')
d.comment(0xb24c, 'Return', align=Align.INLINE)

# Parameter binding (&B24D): collect the formal parameters.
d.banner(
    0xb24d,
    title='Bind the PROC/FN parameters',
    description="""Each formal is parsed by [`parse_lvalue`](address:9582)
— the same lvalue parser LET, FOR and LOCAL use — so a formal need not
be a name: a `?`, `!` or `$` indirection or an array element is a legal
parameter, and binding it is a scoped assignment to that location. Each
formal's current value is stacked (for LOCAL-style restore on return via
[`stack_local`](address:b30d)) and its identity recorded, then the
actual arguments are evaluated and assigned.""",
)
d.comment(0xb24d, 'Save the parser pointer', align=Align.INLINE)
d.label(0xb24d, 'callpf_save_parser2')
d.comment(0xb24f, 'push offset,', align=Align.INLINE)
d.comment(0xb250, 'low byte,', align=Align.INLINE)
d.comment(0xb252, 'push low,', align=Align.INLINE)
d.comment(0xb253, 'high byte,', align=Align.INLINE)
d.comment(0xb255, 'push high', align=Align.INLINE)
d.comment(0xb256, 'Parse a formal parameter (any lvalue: parse_lvalue)',
          align=Align.INLINE)
d.comment(0xb259, 'invalid: error', align=Align.INLINE)
d.comment(0xb25b, 'Update the program pointer', align=Align.INLINE)
d.comment(0xb25d, 'from the PtrB offset', align=Align.INLINE)
d.comment(0xb25f, 'Restore the parser pointer', align=Align.INLINE)
d.comment(0xb260, 'high byte,', align=Align.INLINE)
d.comment(0xb262, 'pull low,', align=Align.INLINE)
d.comment(0xb263, 'low byte,', align=Align.INLINE)
d.comment(0xb265, 'pull offset,', align=Align.INLINE)
d.comment(0xb266, 'offset', align=Align.INLINE)
d.comment(0xb268, 'Recover the running count', align=Align.INLINE)
d.comment(0xb269, 'into X', align=Align.INLINE)
d.comment(0xb26a, "Push the formal's type/address", align=Align.INLINE)
d.comment(0xb26c, 'push type,', align=Align.INLINE)
d.comment(0xb26d, 'address high,', align=Align.INLINE)
d.comment(0xb26f, 'push it,', align=Align.INLINE)
d.comment(0xb270, 'address low,', align=Align.INLINE)
d.comment(0xb272, 'push it', align=Align.INLINE)
d.comment(0xb273, 'count this parameter', align=Align.INLINE)
d.comment(0xb274, 'the new count,', align=Align.INLINE)
d.comment(0xb275, 'push it', align=Align.INLINE)
d.comment(0xb276, 'Stack the current value for LOCAL restore',
          align=Align.INLINE)
d.comment(0xb279, 'Skip spaces', align=Align.INLINE)
d.comment(0xb27c, "','  another parameter?", align=Align.INLINE)
d.char_literal(0xb27d)
d.comment(0xb27e, 'yes', align=Align.INLINE)
d.comment(0xb280, "')' end of parameter list?", align=Align.INLINE)
d.char_literal(0xb281)
d.comment(0xb282, 'no: error', align=Align.INLINE)
d.comment(0xb284, 'Push the end marker', align=Align.INLINE)
d.comment(0xb286, 'push it', align=Align.INLINE)
d.comment(0xb287, 'Expect "(" for the arguments', align=Align.INLINE)
d.comment(0xb28a, "'(' ?", align=Align.INLINE)
d.char_literal(0xb28b)
d.comment(0xb28c, 'missing: error', align=Align.INLINE)
# Evaluate the actual arguments and bind them to the formals.
d.comment(0xb28e, 'Evaluate an argument', align=Align.INLINE)
d.label(0xb28e, 'callpf_arg_loop')
d.comment(0xb291, 'stack its value', align=Align.INLINE)
d.comment(0xb294, 'save the type', align=Align.INLINE)
d.comment(0xb296, 'keep it', align=Align.INLINE)
d.comment(0xb298, 'stack the type', align=Align.INLINE)
d.comment(0xb29b, 'Bump the argument count', align=Align.INLINE)
d.comment(0xb29c, 'into X,', align=Align.INLINE)
d.comment(0xb29d, 'increment,', align=Align.INLINE)
d.comment(0xb29e, 'back to A,', align=Align.INLINE)
d.comment(0xb29f, 'push it', align=Align.INLINE)
d.comment(0xb2a0, 'Skip spaces', align=Align.INLINE)
d.comment(0xb2a3, "','  another argument?", align=Align.INLINE)
d.char_literal(0xb2a4)
d.comment(0xb2a5, 'yes', align=Align.INLINE)
d.comment(0xb2a7, "')' end of arguments?", align=Align.INLINE)
d.char_literal(0xb2a8)
d.comment(0xb2a9, 'no: error', align=Align.INLINE)
d.comment(0xb2ab, 'Recover the argument count', align=Align.INLINE)
d.comment(0xb2ac, 'and the formal count', align=Align.INLINE)
d.comment(0xb2ad, 'to &4D,', align=Align.INLINE)
d.comment(0xb2af, 'and &4E', align=Align.INLINE)
d.comment(0xb2b1, 'counts match?', align=Align.INLINE)
d.comment(0xb2b3, 'yes: bind them', align=Align.INLINE)
d.comment(0xb2b5, 'Reset the stack', align=Align.INLINE)
d.label(0xb2b5, 'callpf_reset_stack')
d.comment(0xb2b7, 'set SP = &FB', align=Align.INLINE)
d.comment(0xb2b8, 'restore PtrA', align=Align.INLINE)
d.comment(0xb2b9, 'high byte,', align=Align.INLINE)
d.comment(0xb2bb, 'pull low,', align=Align.INLINE)
d.comment(0xb2bc, 'low byte', align=Align.INLINE)
d.comment(0xb2be, 'Arguments error', align=Align.INLINE)
d.comment(0xb2ca, 'Unstack the argument type', align=Align.INLINE)
d.label(0xb2ca, 'callpf_unstack_arg')
d.comment(0xb2cd, 'Unstack the formal address/type', align=Align.INLINE)
d.comment(0xb2ce, 'address low,', align=Align.INLINE)
d.comment(0xb2d0, 'pull high,', align=Align.INLINE)
d.comment(0xb2d1, 'address high,', align=Align.INLINE)
d.comment(0xb2d3, 'pull type,', align=Align.INLINE)
d.comment(0xb2d4, 'type', align=Align.INLINE)
d.comment(0xb2d6, 'string formal?', align=Align.INLINE)
d.comment(0xb2d8, 'Argument type', align=Align.INLINE)
d.comment(0xb2da, 'string argument: Arguments error', align=Align.INLINE)
d.comment(0xb2dc, 'numeric: set the formal address', align=Align.INLINE)
d.comment(0xb2de, 'address via &37,', align=Align.INLINE)
d.comment(0xb2e0, 'copy the address there', align=Align.INLINE)
d.comment(0xb2e3, 'Argument type', align=Align.INLINE)
d.comment(0xb2e5, 'integer?', align=Align.INLINE)
d.comment(0xb2e7, 'real: unstack the real value', align=Align.INLINE)
d.comment(0xb2ea, 'into FWA', align=Align.INLINE)
d.comment(0xb2ed, 'assign it', align=Align.INLINE)
d.comment(0xb2f0, 'unstack the integer value', align=Align.INLINE)
d.label(0xb2f0, 'callpf_assign_int')
d.comment(0xb2f3, 'Assign to the formal', align=Align.INLINE)
d.label(0xb2f3, 'callpf_assign')
d.comment(0xb2f6, 'next argument', align=Align.INLINE)
d.comment(0xb2f9, 'String formal: argument type', align=Align.INLINE)
d.label(0xb2f9, 'callpf_string_formal')
d.comment(0xb2fb, 'numeric argument: Arguments error', align=Align.INLINE)
d.comment(0xb2fd, 'Unstack the string', align=Align.INLINE)
d.comment(0xb300, 'assign it', align=Align.INLINE)
d.comment(0xb303, 'One parameter bound', align=Align.INLINE)
d.label(0xb303, 'callpf_bound')

d.comment(0xb305, 'loop', align=Align.INLINE)
d.comment(0xb307, 'Push the parameter count for restore', align=Align.INLINE)
d.comment(0xb309, 'push it', align=Align.INLINE)
d.comment(0xb30a, 'Execute the body', align=Align.INLINE)

d.subroutine(
    0xb30d, 'stack_local',
    title='Save a variable for LOCAL',
    description="""Push a variable's current value and identity (address and type)
onto the BASIC stack so ENDPROC can restore it, implementing LOCAL.
""",
    on_entry={'zp_iwa (&2A/&2B)': 'the variable address',
              'zp_iwa_2 (&2C)': 'the variable type'},
    on_exit={'zp_stack_ptr (&04/&05)': 'lowered past the saved value and identity'},
)
# stack_local (&B30D): save a variable's value and identity for LOCAL
d.comment(0xb30d, 'Variable type', align=Align.INLINE)
d.comment(0xb30f, 'an integer?', align=Align.INLINE)
d.comment(0xb311, 'no', align=Align.INLINE)
d.comment(0xb313, 'integer: address its 4 bytes via &37', align=Align.INLINE)
d.comment(0xb315, 'copy them there', align=Align.INLINE)
d.comment(0xb318, "Load the variable's current value by type", align=Align.INLINE)
# stack_local / typed loaders / fn_chrs
d.label(0xb318, 'local_load_value')
d.comment(0xb31b, 'save the type flags', align=Align.INLINE)
d.comment(0xb31c, 'push the value onto the stack', align=Align.INLINE)
d.comment(0xb31f, 'restore the type', align=Align.INLINE)
d.comment(0xb320, 'byte/string', align=Align.INLINE)
d.comment(0xb322, 'or string', align=Align.INLINE)
d.comment(0xb324, 'integer: reload', align=Align.INLINE)
d.comment(0xb326, 'from &37', align=Align.INLINE)
d.comment(0xb329, 'push the variable identity (as an integer)', align=Align.INLINE)
d.label(0xb329, 'local_push_id')
d.comment(0xb32c, 'Load the variable by type:', align=Align.INLINE)
d.subroutine(
    0xb32c, 'load_var_by_type',
    title='Load a variable by type',
    description="""Dispatch on the variable type code in zp_iwa_2 and load the variable
addressed by (zp_iwa) into the appropriate accumulator: a string into
the string buffer (load_string_var), a byte or 4-byte integer into IWA
(iwa_load_var / load_byte_var), or a 5-byte real into FWA
(load_real_var). Negative = string, 0 = byte, 5 = real, anything else
= integer.
""",
    on_entry={
        'zp_iwa (&2A)': 'pointer to the variable (&2A/&2B)',
        'zp_iwa_2 (&2C)': 'the variable type code (<0 string, 0 byte, 5 real, else integer)',
    },
    on_exit={
        'A': 'value-type marker (&40 integer, &FF real)',
        'zp_iwa (&2A)': 'the integer, if integer/byte',
        'zp_fwa (&2E)': 'the unpacked real, if real (&2E-&35)',
        'string_work (&0600)': 'the string characters, if string; length in zp_strbuf_len (&36)',
    },
)
d.comment(0xb32e, 'string', align=Align.INLINE)
d.comment(0xb330, 'byte', align=Align.INLINE)
d.comment(0xb332, 'real?', align=Align.INLINE)
d.comment(0xb334, 'real (else integer)', align=Align.INLINE)

d.subroutine(
    0xb336, 'iwa_load_var',
    title='Load an integer variable into the accumulator',
    description='Copy the 4-byte integer addressed by zp_iwa into IWA.',
    on_entry={'zp_iwa (&2A/&2B)': 'a pointer to the 4-byte integer variable'},
    on_exit={'zp_iwa': 'the loaded integer', 'X': 'preserved'},
)
# iwa_load_var (&B336) and the byte / real / string loaders
d.comment(0xb336, 'Load a 4-byte integer (MSB first): byte 3', align=Align.INLINE)
d.comment(0xb338, 'read it', align=Align.INLINE)
d.comment(0xb33a, '(into IWA)', align=Align.INLINE)
d.comment(0xb33c, 'next', align=Align.INLINE)
d.comment(0xb33d, 'byte 2', align=Align.INLINE)
d.comment(0xb33f, '(into IWA)', align=Align.INLINE)
d.comment(0xb341, 'next', align=Align.INLINE)
d.comment(0xb342, 'byte 1', align=Align.INLINE)
d.comment(0xb344, '(keep in X)', align=Align.INLINE)
d.comment(0xb345, 'next', align=Align.INLINE)
d.comment(0xb346, 'byte 0', align=Align.INLINE)
d.comment(0xb348, '(store last)', align=Align.INLINE)
d.comment(0xb34a, 'byte 1 from X', align=Align.INLINE)
d.comment(0xb34c, 'integer type', align=Align.INLINE)
d.comment(0xb34e, 'Return the integer', align=Align.INLINE)
d.subroutine(0xb34f, 'load_byte_var', title='Load a byte variable into IWA',
             description='Read the byte addressed by zp_iwa and return it as an '
                         'unsigned integer in IWA (via iwa_from_ya). Part of the '
                         'typed variable loader.',
             on_entry={'(zp_iwa) (&2A/&2B)': 'a pointer to the byte variable',
                       'Y': 'offset of the byte (0)'},
             on_exit={'zp_iwa (&2A-&2D)': 'the byte, zero-extended',
                      'A': 'integer type marker (&40)'})
d.comment(0xb34f, 'Read the byte', align=Align.INLINE)
d.comment(0xb351, 'return as an integer', align=Align.INLINE)
d.subroutine(0xb354, 'load_real_var', title='Load a real variable into FWA',
             description='Unpack the 5-byte packed real addressed by zp_iwa '
                         '(used here as a pointer to the variable) into FWA, '
                         'restoring the implied leading 1 unless the value is '
                         'zero. Part of the typed variable loader.',
             on_entry={'(zp_iwa) (&2A/&2B)': 'a pointer to the 5-byte real',
                       'Y': '5 (the byte count to copy back)'},
             on_exit={'zp_fwa (&2E-&35)': 'the unpacked real',
                      'X': 'preserved'})
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
d.label(0xb37f, 'lrv_set_msb')
d.comment(0xb381, 'real type', align=Align.INLINE)
d.comment(0xb383, 'Return the real', align=Align.INLINE)
d.subroutine(0xb384, 'load_string_var', title='Load a string variable into the buffer',
             description='Copy a string variable into the string buffer. A '
                         'normal string variable carries its pointer and length '
                         'in the descriptor at (zp_iwa); a $-string (Y = &80) '
                         'is read from (zp_iwa) up to the terminating CR. Part '
                         'of the typed variable loader.',
             on_entry={'(zp_iwa) (&2A/&2B)': 'a pointer to the string variable',
                       'Y': 'the string type byte (&80 = $-string)'},
             on_exit={'string_work (&0600)': 'the loaded string characters',
                      'zp_strbuf_len (&36)': 'the string length',
                      'zp_general (&37/&38)': 'corrupted (used as the source ptr)'})
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
d.label(0xb39d, 'lsv_copy_loop')
d.comment(0xb39e, 'read it', align=Align.INLINE)
d.comment(0xb3a0, '-> buffer', align=Align.INLINE)
d.comment(0xb3a3, 'count', align=Align.INLINE)
d.comment(0xb3a4, 'loop', align=Align.INLINE)
d.comment(0xb3a6, 'Return the string', align=Align.INLINE)
d.comment(0xb3a7, '$-string: copy until CR', align=Align.INLINE)
d.label(0xb3a7, 'lsv_dollar')
d.comment(0xb3a9, 'null pointer: empty', align=Align.INLINE)
d.comment(0xb3ab, 'from the start', align=Align.INLINE)
d.comment(0xb3ad, 'char...', align=Align.INLINE)
d.label(0xb3ad, 'lsv_dollar_loop')
d.comment(0xb3af, '-> buffer', align=Align.INLINE)
d.comment(0xb3b2, 'CR?', align=Align.INLINE)
d.comment(0xb3b4, 'yes: end', align=Align.INLINE)
d.comment(0xb3b6, 'next', align=Align.INLINE)
d.comment(0xb3b7, 'loop', align=Align.INLINE)
d.comment(0xb3b9, 'ran 256 chars without CR: length 0', align=Align.INLINE)
d.comment(0xb3ba, 'set the length', align=Align.INLINE)
d.label(0xb3ba, 'lsv_set_length')
d.comment(0xb3bc, 'Return', align=Align.INLINE)

# fn_chrs (&B3BD): CHR$
d.comment(0xb3bd, 'Evaluate the integer argument', align=Align.INLINE)
d.comment(0xb3c0, 'A = the character code', align=Align.INLINE)
d.label(0xb3c0, 'chrs_code')
d.comment(0xb3c2, 'return a one-character string', align=Align.INLINE)
d.subroutine(0xb3c5, 'find_error_line', title='Find the line an error occurred in',
             description='Walk the program from PAGE to locate the line whose '
                         'text span contains the current program pointer and '
                         'record its number in ERL (0 in immediate mode).',
             on_entry={'zp_text_ptr (&0B/&0C)': 'the program pointer at the error',
                       'zp_page (&18)': 'PAGE, the start of the program'},
             on_exit={'zp_erl (&08/&09)': 'the line number (ERL), or 0'})

# find_error_line (&B3C5)
d.comment(0xb3c5, 'Clear ERL:', align=Align.INLINE)
d.comment(0xb3c7, '(low)', align=Align.INLINE)
d.comment(0xb3c9, '(high)', align=Align.INLINE)
d.comment(0xb3cb, 'Scan the program from PAGE: high', align=Align.INLINE)
d.comment(0xb3cd, '(store)', align=Align.INLINE)
d.comment(0xb3cf, 'low 0', align=Align.INLINE)
d.comment(0xb3d1, 'past the error position?', align=Align.INLINE)
d.comment(0xb3d3, 'page 7 (the input line)?', align=Align.INLINE)
d.comment(0xb3d5, 'reached it: done', align=Align.INLINE)
d.comment(0xb3d7, 'X = error position low', align=Align.INLINE)
d.comment(0xb3d9, 'read a program byte', align=Align.INLINE)
# find_error_line / SOUND / ENVELOPE / WIDTH / assign
d.label(0xb3d9, 'fel_scan_loop')
d.comment(0xb3dc, 'a line end (CR)?', align=Align.INLINE)
d.comment(0xb3de, 'no: keep scanning', align=Align.INLINE)
d.comment(0xb3e0, 'is this line past the error?', align=Align.INLINE)
d.comment(0xb3e2, 'error high...', align=Align.INLINE)
d.comment(0xb3e4, 'minus the scan high', align=Align.INLINE)
d.comment(0xb3e6, 'yes: keep the previous line', align=Align.INLINE)
d.comment(0xb3e8, 'read the line number high byte', align=Align.INLINE)
d.comment(0xb3eb, 'end of program?', align=Align.INLINE)
d.comment(0xb3ed, 'yes: done', align=Align.INLINE)
d.comment(0xb3ef, 'record ERL high', align=Align.INLINE)
d.comment(0xb3f1, 'line number low byte', align=Align.INLINE)
d.comment(0xb3f4, 'record ERL low', align=Align.INLINE)
d.comment(0xb3f6, 'skip the line length byte', align=Align.INLINE)
d.comment(0xb3f9, 'still before the error?', align=Align.INLINE)
d.label(0xb3f9, 'fel_check')
d.comment(0xb3fb, 'error high...', align=Align.INLINE)
d.comment(0xb3fd, 'minus the scan high', align=Align.INLINE)
d.comment(0xb3ff, 'yes: scan the next line', align=Align.INLINE)
d.comment(0xb401, 'Return', align=Align.INLINE)
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
d.typed_data(0xa869, 'bbc_float5', comment='log10(e) = 1/ln(10); 1 ULP high',
             override=True)
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
d.typed_data(0xaa68, 'bbc_float5', comment='pi/180 (deg -> rad, RAD); 1 ULP low',
             override=True)
d.typed_data(0xaa6d, 'bbc_float5', comment='180/pi (radians -> degrees, DEG)',
             override=True)
_fp_coeff_table(0xaa72, 5, 'sin', '1.0')
# e, then the EXP continued-fraction table.
d.typed_data(0xaae4, 'bbc_float5', comment='e (stored 1 ULP low)', override=True)
_fp_coeff_table(0xaae9, 7, 'exp', '1.0')

# ----------------------------------------------------------------------
# Language entry and startup.
# ----------------------------------------------------------------------
d.label(0xb402, 'brk_handler')      # Reached via BRKV on any error

# brk_handler (&B402): the BASIC error handler (via BRKV)
d.comment(0xb402, 'Find the line number (set ERL)', align=Align.INLINE)
d.comment(0xb405, 'TRACE off', align=Align.INLINE)
d.comment(0xb407, 'error number', align=Align.INLINE)
d.comment(0xb409, 'non-zero: an ON ERROR handler is active', align=Align.INLINE)
d.comment(0xb40b, 'no handler: reset to the default (ON ERROR OFF)', align=Align.INLINE)
d.comment(0xb40d, 'default handler &B433: low,', align=Align.INLINE)
d.comment(0xb40f, 'high...', align=Align.INLINE)
d.comment(0xb411, '(store)', align=Align.INLINE)
d.comment(0xb413, 'Point the program pointer at the handler code: low', align=Align.INLINE)
d.label(0xb413, 'fel_set_handler')
d.comment(0xb415, '(low)', align=Align.INLINE)
d.comment(0xb417, 'high', align=Align.INLINE)
d.comment(0xb419, '(store)', align=Align.INLINE)
d.comment(0xb41b, 'clear DATA and the stacks', align=Align.INLINE)
d.comment(0xb41e, 'offset 0', align=Align.INLINE)
d.comment(0xb41f, '(store)', align=Align.INLINE)
d.comment(0xb421, 'OSBYTE &DA: flush the VDU queue', align=Align.INLINE)
d.comment(0xb426, 'OSBYTE &7E: acknowledge any Escape', align=Align.INLINE)
d.comment(0xb42b, 'reset the 6502 stack...', align=Align.INLINE)
d.comment(0xb42d, 'OPT = &FF', align=Align.INLINE)
d.comment(0xb42f, 'S = &FF (empty the stack)', align=Align.INLINE)
d.comment(0xb430, 'enter the execution loop at the handler', align=Align.INLINE)
# stmt_sound (&B44C): SOUND chan, amp, pitch, dur -> OSWORD 7.
d.comment(0xb44c, 'Evaluate the first parameter', align=Align.INLINE)
d.comment(0xb44f, 'three more', align=Align.INLINE)
d.comment(0xb451, 'Stack the 16-bit value', align=Align.INLINE)
d.label(0xb451, 'sound_stack_loop')
d.comment(0xb453, 'push low,', align=Align.INLINE)
d.comment(0xb454, 'high,', align=Align.INLINE)
d.comment(0xb456, 'push high', align=Align.INLINE)
d.comment(0xb457, 'save the counter', align=Align.INLINE)
d.comment(0xb458, 'push it', align=Align.INLINE)
d.comment(0xb459, 'step past the comma, evaluate the next', align=Align.INLINE)
d.comment(0xb45c, 'restore the counter', align=Align.INLINE)
d.comment(0xb45d, 'into X,', align=Align.INLINE)
d.comment(0xb45e, 'one fewer parameter', align=Align.INLINE)
d.comment(0xb45f, 'loop', align=Align.INLINE)
d.comment(0xb461, 'Check the statement ends', align=Align.INLINE)
d.comment(0xb464, 'Last value to the block end', align=Align.INLINE)
d.comment(0xb466, 'low byte to &3D,', align=Align.INLINE)
d.comment(0xb468, 'high,', align=Align.INLINE)
d.comment(0xb46a, 'high byte to &3E', align=Align.INLINE)
d.comment(0xb46c, 'OSWORD 7, 6 bytes', align=Align.INLINE)
d.comment(0xb46e, '6-byte block (X=5)', align=Align.INLINE)
d.comment(0xb470, 'pop into the block and call', align=Align.INLINE)

# stmt_envelope (&B472): ENVELOPE 14 params -> OSWORD 8.
d.comment(0xb472, 'Evaluate the first parameter', align=Align.INLINE)
d.comment(0xb475, '13 more', align=Align.INLINE)
d.comment(0xb477, 'Stack the 8-bit value', align=Align.INLINE)
d.label(0xb477, 'env_stack_loop')
d.comment(0xb479, 'push it', align=Align.INLINE)
d.comment(0xb47a, 'save the counter', align=Align.INLINE)
d.comment(0xb47b, 'push it', align=Align.INLINE)
d.comment(0xb47c, 'step past the comma, evaluate the next', align=Align.INLINE)
d.comment(0xb47f, 'restore the counter', align=Align.INLINE)
d.comment(0xb480, 'into X,', align=Align.INLINE)
d.comment(0xb481, 'one fewer parameter', align=Align.INLINE)
d.comment(0xb482, 'loop', align=Align.INLINE)
d.comment(0xb484, 'Check the statement ends', align=Align.INLINE)
d.comment(0xb487, 'Last value to the block end', align=Align.INLINE)
d.comment(0xb489, 'into &44 (the block end)', align=Align.INLINE)
d.comment(0xb48b, 'OSWORD 8, 12 bytes', align=Align.INLINE)
d.comment(0xb48d, 'OSWORD number 8', align=Align.INLINE)
d.comment(0xb48f, 'Pop a byte into the control block', align=Align.INLINE)
d.label(0xb48f, 'env_pop_loop')
d.comment(0xb490, 'store at offset X,', align=Align.INLINE)
d.comment(0xb492, 'next lower offset', align=Align.INLINE)
d.comment(0xb493, 'loop', align=Align.INLINE)
d.comment(0xb495, 'OSWORD number', align=Align.INLINE)
d.comment(0xb496, 'Point at the control block', align=Align.INLINE)
d.comment(0xb498, 'block address high', align=Align.INLINE)
d.comment(0xb49d, 'next statement', align=Align.INLINE)

# stmt_width (&B4A0): WIDTH n.
d.comment(0xb4a0, 'Evaluate the width', align=Align.INLINE)
d.comment(0xb4a3, 'check the statement ends', align=Align.INLINE)
d.comment(0xb4a6, 'Auto-newline column = width - 1', align=Align.INLINE)
d.comment(0xb4a8, 'width - 1', align=Align.INLINE)
d.comment(0xb4a9, 'store it', align=Align.INLINE)
d.comment(0xb4ab, 'next statement', align=Align.INLINE)

d.comment(0xb4ae, 'Type mismatch error', align=Align.INLINE)
d.label(0xb4ae, 'width_type_error')
d.comment(0xb4b1, 'Evaluate the value', align=Align.INLINE)
d.subroutine(
    0xb4b1, 'width_eval_value',
    title='Evaluate a numeric value and assign it to a variable',
    description="""Evaluate the numeric expression at PtrB via eval_or_eor, then fall
straight into assign_number, which pops the variable's data address
off the BASIC stack and stores the value there, coercing to the
variable's own type.
""",
    on_entry={
        'zp_text_ptr2 (&19/&1A)': 'PtrB at the value expression',
        '(zp_stack_ptr) (&04/&05)': 'the destination variable data address on top of the BASIC stack',
    },
)
d.subroutine(
    0xb4b4, 'assign_number',
    title='Store a numeric value into a variable',
    description="""Assign the current numeric value (integer or real) to the
variable whose data address is on the stack, coercing to the variable's
own type (real variables get the value converted to FP). An integer
value is written raw and wraps — there is no range check — so
`A%=&AABBCCDD` or `!p=&AABBCCDD` stores the four bytes verbatim and never
errors. The only numeric-overflow error (Too big) lives on the
real→integer convert branch ([`fwa_to_int`](address:a3e4)), reached only
when a *float* value lands in an integer cell, so `A%=1E10` does raise
Too big.
""",
    on_entry={'(zp_stack_ptr) (&04/&05)': 'the variable data address',
              'zp_iwa / zp_fwa': 'the value to store',
              'zp_var_type (&27)': 'the value type'},
    on_exit={'the numeric variable': 'updated in its own type'},
)
# assign_number (&B4B4): store a numeric value into a numeric variable.
d.comment(0xb4b4, 'Pop the variable data address from the stack',
          align=Align.INLINE)
d.comment(0xb4b7, "Variable's size/type byte", align=Align.INLINE)
d.label(0xb4b7, 'assign_num_by_type')
d.comment(0xb4b9, 'size 5 = real variable?', align=Align.INLINE)
d.comment(0xb4bb, 'yes: store as a real', align=Align.INLINE)
d.comment(0xb4bd, 'Type of the value', align=Align.INLINE)
d.comment(0xb4bf, 'string: Type mismatch', align=Align.INLINE)
d.comment(0xb4c1, 'integer: store raw, 4-byte wrap (no range check)',
          align=Align.INLINE)
d.comment(0xb4c3, 'real value, integer variable: convert', align=Align.INLINE)

d.subroutine(
    0xb4c6, 'iwa_store_var',
    title='Store the accumulator into an integer variable',
    description="""Copy IWA into the integer variable addressed by &37. The
width comes from &39, which is the lvalue *type* byte rather than a
separate size field: it rode in as byte 2 of the stacked destination
address ([`parse_lvalue`](address:9582) packs the address in &2A/&2B and
the type in &2C, and [`unstack_int_to_general`](address:be0b) lands byte
2 in &39). Type 0 (`?` byte indirection) writes 1 byte; type 4 (`!` word
indirection, an integer variable, or an array element) writes 4.""",
    on_entry={
        '(zp_general) (&37/&38)': 'a pointer to the integer variable',
        '&39': 'the lvalue type byte: 0 stores 1 byte, nonzero stores 4',
    },
    on_exit={'X': 'preserved'},
)
# iwa_store_var (&B4C6): store IWA into a variable (width from &39).
d.comment(0xb4c6, 'Offset 0', align=Align.INLINE)
d.comment(0xb4c8, 'Store byte 1', align=Align.INLINE)
d.comment(0xb4ca, 'write it', align=Align.INLINE)
d.comment(0xb4cc, 'Size byte: 0 -> 1-byte (? indir), else 4 bytes',
          align=Align.INLINE)
d.comment(0xb4ce, '1-byte value: done', align=Align.INLINE)
d.comment(0xb4d0, 'Store byte 2', align=Align.INLINE)
d.comment(0xb4d2, 'next byte slot', align=Align.INLINE)
d.comment(0xb4d3, 'write it', align=Align.INLINE)
d.comment(0xb4d5, 'Store byte 3', align=Align.INLINE)
d.comment(0xb4d7, 'next byte slot', align=Align.INLINE)
d.comment(0xb4d8, 'write it', align=Align.INLINE)
d.comment(0xb4da, 'Store byte 4', align=Align.INLINE)
d.comment(0xb4dc, 'next byte slot', align=Align.INLINE)
d.comment(0xb4dd, 'write it', align=Align.INLINE)

d.comment(0xb4df, 'Return', align=Align.INLINE)
d.comment(0xb4e0, 'Value type', align=Align.INLINE)
d.label(0xb4e0, 'store_var_type')
d.comment(0xb4e2, 'string: Type mismatch', align=Align.INLINE)
d.comment(0xb4e4, 'real: store it', align=Align.INLINE)
d.comment(0xb4e6, 'integer: convert to real', align=Align.INLINE)
d.comment(0xb4e9, 'Store the 5-byte real: exponent', align=Align.INLINE)
d.label(0xb4e9, 'store_real')
d.comment(0xb4eb, 'load the exponent', align=Align.INLINE)
d.comment(0xb4ed, 'to variable+0', align=Align.INLINE)
d.comment(0xb4ef, 'next byte slot', align=Align.INLINE)
d.comment(0xb4f0, 'Pack the sign into the mantissa', align=Align.INLINE)
d.comment(0xb4f2, 'keep only the sign bit', align=Align.INLINE)
d.comment(0xb4f4, 'save it', align=Align.INLINE)
d.comment(0xb4f6, 'mantissa top byte', align=Align.INLINE)
d.comment(0xb4f8, 'drop its implicit top bit', align=Align.INLINE)
d.comment(0xb4fa, 'merge the sign bit in', align=Align.INLINE)
d.comment(0xb4fc, 'to variable+1', align=Align.INLINE)
d.comment(0xb4fe, 'mantissa 2', align=Align.INLINE)
d.comment(0xb4ff, 'load it', align=Align.INLINE)
d.comment(0xb501, 'to variable+2', align=Align.INLINE)
d.comment(0xb503, 'mantissa 3', align=Align.INLINE)
d.comment(0xb504, 'load it', align=Align.INLINE)
d.comment(0xb506, 'to variable+3', align=Align.INLINE)
d.comment(0xb508, 'mantissa 4', align=Align.INLINE)
d.comment(0xb509, 'load it', align=Align.INLINE)
d.comment(0xb50b, 'to variable+4', align=Align.INLINE)
d.comment(0xb50d, 'Return', align=Align.INLINE)
d.subroutine(0xb50e, 'print_token',
             title='De-tokenise and print a character or token',
             description='Print A directly if below &80, otherwise look the '
                         'token up in the keyword table at &8071 and print '
                         'its expanded keyword text.',
             on_entry={'A': 'the character or keyword token to print'},
             on_exit={'the output': 'the character or expanded keyword',
                      'zp_count (&1E)': 'the print column, advanced',
                      'zp_general (&37/&38)': 'corrupted (scratch)'})
# print_token (&B50E): de-tokenise and print.
d.comment(0xb50e, 'Save the character', align=Align.INLINE)
d.comment(0xb510, 'a token?', align=Align.INLINE)
d.comment(0xb512, 'no: print it directly', align=Align.INLINE)
d.comment(0xb514, 'Point at the token table (&8071)', align=Align.INLINE)
d.comment(0xb516, 'pointer low = &71', align=Align.INLINE)
d.comment(0xb518, 'pointer high = &80', align=Align.INLINE)
d.comment(0xb51a, 'set it', align=Align.INLINE)
d.comment(0xb51c, 'save Y', align=Align.INLINE)
d.comment(0xb51e, 'Start of an entry', align=Align.INLINE)
# print_token / print_char / print helpers
d.label(0xb51e, 'ptok_entry_start')
d.comment(0xb520, 'Scan to the token byte', align=Align.INLINE)
d.label(0xb520, 'ptok_scan_loop')
d.comment(0xb521, 'read it', align=Align.INLINE)
d.comment(0xb523, '...(skip the keyword text)', align=Align.INLINE)
d.comment(0xb525, 'this token?', align=Align.INLINE)
d.comment(0xb527, 'yes: print its keyword', align=Align.INLINE)
d.comment(0xb529, 'Advance to the next entry', align=Align.INLINE)
d.comment(0xb52a, 'offset into A', align=Align.INLINE)
d.comment(0xb52b, 'set carry: +1 past the flag byte', align=Align.INLINE)
d.comment(0xb52c, 'add to the pointer low,', align=Align.INLINE)
d.comment(0xb52e, 'store it', align=Align.INLINE)
d.comment(0xb530, 'no carry: scan the next entry', align=Align.INLINE)
d.comment(0xb532, 'else carry into the high byte', align=Align.INLINE)
d.comment(0xb534, 'continue', align=Align.INLINE)
d.comment(0xb536, 'Print the keyword text: from the start', align=Align.INLINE)
d.label(0xb536, 'ptok_print')
d.comment(0xb538, 'Next character', align=Align.INLINE)
d.label(0xb538, 'ptok_print_loop')
d.comment(0xb53a, 'token byte: done', align=Align.INLINE)
d.comment(0xb53c, 'print it', align=Align.INLINE)
d.comment(0xb53f, 'next', align=Align.INLINE)
d.comment(0xb540, 'loop', align=Align.INLINE)
d.comment(0xb542, 'Restore Y', align=Align.INLINE)
d.label(0xb542, 'ptok_restore_y')
d.comment(0xb544, 'Return', align=Align.INLINE)
d.subroutine(0xb545, 'print_hex_byte', title='Print A as two hex digits',
             description='Print the byte in A as two hex digits (high nibble '
                         'then low) via print_hex_digit / print_char.',
             on_entry={'A': 'the byte to print'},
             on_exit={'zp_count (&1E)': 'the print column, advanced',
                      'A': 'corrupted', 'X': 'corrupted', 'Y': 'corrupted'})
# print_hex_byte (&B545).
d.comment(0xb545, 'Save the byte', align=Align.INLINE)
d.comment(0xb546, 'High nibble', align=Align.INLINE)
d.comment(0xb547, 'shift it down,', align=Align.INLINE)
d.comment(0xb548, '(continued)', align=Align.INLINE)
d.comment(0xb549, '(continued)', align=Align.INLINE)
d.comment(0xb54a, 'print it', align=Align.INLINE)
d.comment(0xb54d, 'Low nibble', align=Align.INLINE)
d.comment(0xb54e, 'keep the low nibble', align=Align.INLINE)
d.subroutine(0xb550, 'print_hex_digit',
             title='Print the low nibble of A as a hex digit',
             description='Convert A (0-15) to the ASCII hex digit 0-9 / A-F and '
                         'fall into print_char to emit it with column tracking.',
             on_entry={'A': 'a value 0-15 (the low nibble to print)'},
             on_exit={'zp_count (&1E)': 'the print column, advanced',
                      'A': 'corrupted', 'X': 'corrupted', 'Y': 'corrupted'})
# print_hex_digit (&B550).
d.comment(0xb550, 'above 9?', align=Align.INLINE)
d.comment(0xb552, 'no', align=Align.INLINE)
d.comment(0xb554, "adjust for A-F", align=Align.INLINE)
d.comment(0xb556, 'to ASCII, then fall into print_char', align=Align.INLINE)
d.char_literal(0xb557)
d.label(0xb556, 'phd_ascii')
d.subroutine(0xb558, 'print_char',
             title='Print a character with column tracking',
             description='Output A through the print formatter, handling CR '
                         'specially and maintaining the print column COUNT. '
                         'Auto-newlines when the column reaches WIDTH.',
             on_entry={'A': 'the character to print',
                       'zp_count (&1E)': 'the current print column',
                       'zp_width (&23)': 'the print WIDTH limit'},
             on_exit={'zp_count (&1E)': 'updated (reset by CR, else advanced)',
                      'X': 'corrupted', 'Y': 'corrupted'})
# print_char (&B558).
d.comment(0xb558, 'carriage return?', align=Align.INLINE)
d.comment(0xb55a, 'no: format and print', align=Align.INLINE)
d.comment(0xb55c, 'print the CR', align=Align.INLINE)
d.comment(0xb55f, 'reset the column', align=Align.INLINE)
d.comment(0xb562, 'Print A as hex then a space', align=Align.INLINE)
d.subroutine(
    0xb562, 'print_hex_space',
    title='Print A as two hex digits then a space',
    description="""Print the byte in A as two hexadecimal digits (print_hex_byte), then
fall through into print_space to emit a trailing space through the
print formatter, which auto-newlines when the column reaches WIDTH.
""",
    on_entry={
        'A': 'the byte to print as hex',
        'zp_count (&1E)': 'the current print column',
        'zp_width (&23)': 'the print WIDTH limit',
    },
    on_exit={
        'zp_count (&1E)': 'advanced past the digits and the space',
        'A': 'space (&20)',
        'X': 'corrupted',
        'Y': 'corrupted',
    },
)
d.subroutine(0xb565, 'print_space',
             title='Print a space through the print formatter',
             description='Print a space via print_char, auto-newlining when the '
                         'column reaches WIDTH.',
             on_entry={'zp_count (&1E)': 'the current print column',
                       'zp_width (&23)': 'the print WIDTH limit'},
             on_exit={'zp_count (&1E)': 'advanced past the space',
                      'A': 'space (&20)', 'X': 'corrupted', 'Y': 'corrupted'})
d.comment(0xb565, 'Space', align=Align.INLINE)
d.char_literal(0xb566)
d.comment(0xb567, 'Save the character', align=Align.INLINE)
d.label(0xb567, 'print_char_body')
d.comment(0xb568, 'WIDTH limit', align=Align.INLINE)
d.comment(0xb56a, 'vs the current column', align=Align.INLINE)
d.comment(0xb56c, 'within the width', align=Align.INLINE)
d.comment(0xb56e, 'else auto-newline', align=Align.INLINE)
d.comment(0xb571, 'Recover the character', align=Align.INLINE)
d.label(0xb571, 'print_char_emit')
d.comment(0xb572, 'Advance the column', align=Align.INLINE)
d.comment(0xb574, 'Print it via WRCHV', align=Align.INLINE)
d.subroutine(0xb577, 'print_listo_indent',
             title='Print LISTO indentation',
             description='If the LISTO flag bit in A is set against zp_listo, '
                         'print 2*X spaces of indentation for a LIST line.',
             on_entry={'A': 'the LISTO bit mask to test',
                       'X': 'the indent depth (spaces = 2*X)',
                       'zp_listo (&1F)': 'the LISTO flags'},
             on_exit={'the output': 'the indentation spaces (none if disabled)'})
# print_listo_indent (&B577).
d.comment(0xb577, 'LISTO bit set?', align=Align.INLINE)
d.comment(0xb579, 'no: no indent', align=Align.INLINE)
d.comment(0xb57b, 'Indent count', align=Align.INLINE)
d.comment(0xb57c, 'zero: none', align=Align.INLINE)
d.comment(0xb57e, 'single space', align=Align.INLINE)
d.comment(0xb580, 'Print a space...', align=Align.INLINE)
d.label(0xb580, 'listo_space_loop')

d.comment(0xb583, '...and a space (two per level)', align=Align.INLINE)
d.comment(0xb586, 'next level', align=Align.INLINE)
d.comment(0xb587, 'loop', align=Align.INLINE)
d.comment(0xb589, 'Return', align=Align.INLINE)
d.subroutine(0xb58a, 'stmt_listo', title='LISTO - set the listing options',
             description='Evaluate the option value and store it in the LISTO '
                         'flag (&1F), which controls LIST indentation and '
                         'spacing. LISTO n.',
             on_entry=STMT_ON_ENTRY,
             on_exit={'zp_listo (&1F)': 'the new LISTO flags',
                      'control': 'rejoins statement_loop'})
# stmt_listo (&B58A): LISTO n.
d.comment(0xb58a, 'Step past LISTO', align=Align.INLINE)
d.comment(0xb58c, 'Evaluate the option value', align=Align.INLINE)
d.comment(0xb58f, 'check the statement ends', align=Align.INLINE)
d.comment(0xb592, 'coerce to a byte', align=Align.INLINE)
d.comment(0xb595, 'Store the LISTO flag', align=Align.INLINE)
d.comment(0xb597, 'into &1F', align=Align.INLINE)
d.comment(0xb599, 'next statement', align=Align.INLINE)

# ----------------------------------------------------------------------
# stmt_list (&B59C): the LIST statement.
# Parses an optional line range (default 0..32767), finds the first
# line, and for each line up to the end prints the line number and
# de-tokenises the body, tracking quote state and LISTO indentation
# (&3B/&3C, adjusted by structure keywords).
# ----------------------------------------------------------------------
d.comment(0xb59c, 'Peek at the next character', align=Align.INLINE)
d.comment(0xb59d, 'read it', align=Align.INLINE)
d.comment(0xb59f, "'O' (LISTO)?", align=Align.INLINE)
d.char_literal(0xb5a0)
d.comment(0xb5a1, 'yes: set the option', align=Align.INLINE)
d.comment(0xb5a3, 'Clear the indent levels', align=Align.INLINE)
d.comment(0xb5a5, 'FOR/REPEAT indent = 0,', align=Align.INLINE)
d.comment(0xb5a7, 'second indent = 0', align=Align.INLINE)
d.comment(0xb5a9, 'Start line default 0', align=Align.INLINE)
d.comment(0xb5ac, 'Embedded start line number?', align=Align.INLINE)
d.comment(0xb5af, 'remember whether one was given', align=Align.INLINE)
d.comment(0xb5b0, 'Stack the start line', align=Align.INLINE)
d.comment(0xb5b3, 'End line default 32767', align=Align.INLINE)
d.comment(0xb5b5, 'low byte = &FF,', align=Align.INLINE)
d.comment(0xb5b7, 'high byte &7F,', align=Align.INLINE)
d.comment(0xb5b9, 'high byte (= 32767)', align=Align.INLINE)
d.comment(0xb5bb, 'Was a start line given?', align=Align.INLINE)
d.comment(0xb5bc, 'no: check for a range comma', align=Align.INLINE)
d.comment(0xb5be, 'Skip spaces', align=Align.INLINE)
d.comment(0xb5c1, "','  range separator?", align=Align.INLINE)
d.char_literal(0xb5c2)
d.comment(0xb5c3, 'yes: read the end line', align=Align.INLINE)
d.comment(0xb5c5, 'Single line: end = start', align=Align.INLINE)
d.comment(0xb5c8, 're-stack it', align=Align.INLINE)
d.comment(0xb5cb, 'back up', align=Align.INLINE)
d.comment(0xb5cd, 'always taken', align=Align.INLINE)
d.comment(0xb5cf, 'Skip spaces', align=Align.INLINE)
# stmt_list
d.label(0xb5cf, 'list_skip_spaces')
d.comment(0xb5d2, "','  range separator?", align=Align.INLINE)
d.char_literal(0xb5d3)
d.comment(0xb5d4, 'yes', align=Align.INLINE)
d.comment(0xb5d6, 'back up', align=Align.INLINE)
d.comment(0xb5d8, 'Read the end line number', align=Align.INLINE)
d.label(0xb5d8, 'list_end_line')
d.comment(0xb5db, 'Save the end line', align=Align.INLINE)
d.label(0xb5db, 'list_save_end')
d.comment(0xb5dd, 'low to &31,', align=Align.INLINE)
d.comment(0xb5df, 'high byte,', align=Align.INLINE)
d.comment(0xb5e1, 'high to &32', align=Align.INLINE)
d.comment(0xb5e3, 'Check the statement ends', align=Align.INLINE)
d.comment(0xb5e6, 'Check a program is present', align=Align.INLINE)
d.comment(0xb5e9, 'Recover the start line', align=Align.INLINE)
d.comment(0xb5ec, 'Find the first line', align=Align.INLINE)
d.comment(0xb5ef, 'Point at it', align=Align.INLINE)
d.comment(0xb5f1, 'pointer low,', align=Align.INLINE)
d.comment(0xb5f3, 'high byte,', align=Align.INLINE)
d.comment(0xb5f5, 'pointer high', align=Align.INLINE)
d.comment(0xb5f7, 'exact line: start here', align=Align.INLINE)
d.comment(0xb5f9, 'back up the offset,', align=Align.INLINE)
d.comment(0xb5fa, 'inexact: start at the next line', align=Align.INLINE)
d.comment(0xb5fc, 'Newline after the previous line', align=Align.INLINE)
d.label(0xb5fc, 'list_line_loop')
d.comment(0xb5ff, 'check Escape', align=Align.INLINE)
d.comment(0xb602, "This line's number: high byte", align=Align.INLINE)
d.label(0xb602, 'list_check_high')
d.comment(0xb604, 'store high,', align=Align.INLINE)
d.comment(0xb606, 'next byte', align=Align.INLINE)
d.comment(0xb607, '...low byte', align=Align.INLINE)
d.comment(0xb609, 'store low', align=Align.INLINE)
d.comment(0xb60b, 'skip the length byte', align=Align.INLINE)
d.comment(0xb60c, '(continued)', align=Align.INLINE)
d.comment(0xb60d, 'save the body offset', align=Align.INLINE)
d.comment(0xb60f, 'Past the end line?', align=Align.INLINE)
d.label(0xb60f, 'list_past_end')
d.comment(0xb611, 'clear carry,', align=Align.INLINE)
d.comment(0xb612, 'line - end low,', align=Align.INLINE)
d.comment(0xb614, 'high byte,', align=Align.INLINE)
d.comment(0xb616, 'line - end high', align=Align.INLINE)
d.comment(0xb618, 'no: list this line', align=Align.INLINE)
d.comment(0xb61a, 'yes: done', align=Align.INLINE)
d.comment(0xb61d, 'Print the line number', align=Align.INLINE)
d.label(0xb61d, 'list_print_num')
d.comment(0xb620, 'Reset the quote flag', align=Align.INLINE)
d.comment(0xb622, 'store it (&4D)', align=Align.INLINE)
d.comment(0xb624, 'Print the LISTO leading space', align=Align.INLINE)
d.comment(0xb626, 'do it', align=Align.INLINE)
d.comment(0xb629, 'FOR/REPEAT indent', align=Align.INLINE)
d.comment(0xb62b, 'LISTO bit 1 indent', align=Align.INLINE)
d.comment(0xb62d, 'do it', align=Align.INLINE)
d.comment(0xb630, 'second indent level', align=Align.INLINE)
d.comment(0xb632, 'LISTO bit 2 indent', align=Align.INLINE)
d.comment(0xb634, 'do it', align=Align.INLINE)
d.comment(0xb637, 'Line offset', align=Align.INLINE)
d.label(0xb637, 'list_line_offset')
d.comment(0xb639, 'Next character', align=Align.INLINE)
d.label(0xb639, 'list_char_loop')
d.comment(0xb63b, 'end of line?', align=Align.INLINE)
d.comment(0xb63d, 'yes: next line', align=Align.INLINE)
d.comment(0xb63f, 'quote?', align=Align.INLINE)
d.char_literal(0xb640)
d.comment(0xb641, 'no: a token or literal', align=Align.INLINE)
d.comment(0xb643, 'toggle the quote flag', align=Align.INLINE)
d.comment(0xb645, 'flip the flag,', align=Align.INLINE)
d.comment(0xb647, 'store it', align=Align.INLINE)
d.comment(0xb649, 'print the quote', align=Align.INLINE)
d.char_literal(0xb64a)
d.comment(0xb64b, 'do it', align=Align.INLINE)
d.label(0xb64b, 'list_emit')
d.comment(0xb64e, 'next character', align=Align.INLINE)
d.comment(0xb64f, 'continue the line', align=Align.INLINE)
d.comment(0xb651, 'Inside a quoted string?', align=Align.INLINE)
d.label(0xb651, 'list_in_quote')
d.comment(0xb653, 'yes: print literally', align=Align.INLINE)
d.comment(0xb655, 'line-number token?', align=Align.INLINE)
d.comment(0xb657, 'no', align=Align.INLINE)
d.comment(0xb659, 'decode the embedded line number', align=Align.INLINE)
d.comment(0xb65c, 'save the advanced offset', align=Align.INLINE)
d.comment(0xb65e, 'no field padding', align=Align.INLINE)
d.comment(0xb660, 'clear the field width', align=Align.INLINE)
d.comment(0xb662, 'print it', align=Align.INLINE)
d.comment(0xb665, 'continue', align=Align.INLINE)
d.comment(0xb668, 'FOR token?', align=Align.INLINE)
d.label(0xb668, 'list_for_token')
d.comment(0xb66a, 'no', align=Align.INLINE)
d.comment(0xb66c, 'increase the indent', align=Align.INLINE)
d.comment(0xb66e, 'NEXT token?', align=Align.INLINE)
d.label(0xb66e, 'list_next_token')
d.comment(0xb670, 'no', align=Align.INLINE)
d.comment(0xb672, 'indent active?', align=Align.INLINE)
d.comment(0xb674, 'no', align=Align.INLINE)
d.comment(0xb676, 'decrease the indent', align=Align.INLINE)
d.comment(0xb678, 'REPEAT token?', align=Align.INLINE)
d.label(0xb678, 'list_repeat_token')
d.comment(0xb67a, 'no', align=Align.INLINE)
d.comment(0xb67c, 'increase the indent', align=Align.INLINE)
d.comment(0xb67e, 'UNTIL token?', align=Align.INLINE)
d.label(0xb67e, 'list_until_token')
d.comment(0xb680, 'no', align=Align.INLINE)
d.comment(0xb682, 'indent active?', align=Align.INLINE)
d.comment(0xb684, 'no', align=Align.INLINE)
d.comment(0xb686, 'decrease the indent', align=Align.INLINE)
d.comment(0xb688, 'De-tokenise and print the character', align=Align.INLINE)
d.label(0xb688, 'list_print_char')
d.comment(0xb68b, 'next', align=Align.INLINE)
d.comment(0xb68c, 'loop', align=Align.INLINE)

d.comment(0xb68e, 'No FN error', align=Align.INLINE)
d.label(0xb68e, 'list_error')
d.comment(0xb695, 'Parse the optional control variable', align=Align.INLINE)
# stmt_next (&B695) remaining: update the control variable, test the limit
d.comment(0xb698, 'a variable named after NEXT?', align=Align.INLINE)
d.comment(0xb69a, 'innermost FOR frame', align=Align.INLINE)
d.comment(0xb69c, 'no FOR active: error', align=Align.INLINE)
d.comment(0xb69e, 'no variable: use the innermost loop', align=Align.INLINE)
d.comment(0xb6a0, 'not a variable: error', align=Align.INLINE)
# stmt_next
d.label(0xb6a0, 'next_not_var')
d.comment(0xb6a3, 'string/array: not a loop variable', align=Align.INLINE)
d.label(0xb6a3, 'next_bad_var')
d.comment(0xb6a5, 'Search the FOR stack for the named variable:', align=Align.INLINE)
d.comment(0xb6a7, 'not found: error', align=Align.INLINE)
d.comment(0xb6a9, 'Find the matching FOR frame on the stack', align=Align.INLINE)
d.label(0xb6a9, 'next_find_frame')
d.comment(0xb6ab, 'match the variable address low?', align=Align.INLINE)
d.comment(0xb6ae, 'no: next frame', align=Align.INLINE)
d.comment(0xb6b0, 'address high', align=Align.INLINE)
d.comment(0xb6b2, 'match the frame address high?', align=Align.INLINE)
d.comment(0xb6b5, 'no: next frame', align=Align.INLINE)
d.comment(0xb6b7, 'type', align=Align.INLINE)
d.comment(0xb6b9, 'match the frame type?', align=Align.INLINE)
d.comment(0xb6bc, 'match: this loop', align=Align.INLINE)
d.comment(0xb6be, 'Not this loop: discard the frame and look outward',
          align=Align.INLINE)
d.label(0xb6be, 'next_discard_frame')
d.comment(0xb6bf, 'step out one frame (15 bytes)', align=Align.INLINE)
d.comment(0xb6c0, 'minus 15 bytes,', align=Align.INLINE)
d.comment(0xb6c2, 'new frame index,', align=Align.INLINE)
d.comment(0xb6c3, 'update the FOR level', align=Align.INLINE)
d.comment(0xb6c5, 'keep searching', align=Align.INLINE)
d.comment(0xb6c7, 'No FOR error block', align=Align.INLINE)
d.comment(0xb6d7, 'Found: reload the control variable to update it',
          align=Align.INLINE)

d.label(0xb6d7, 'next_found')
d.comment(0xb6da, 'control variable address: low', align=Align.INLINE)
d.comment(0xb6dc, 'high', align=Align.INLINE)
d.comment(0xb6df, 'address high', align=Align.INLINE)
d.comment(0xb6e1, 'type', align=Align.INLINE)
d.comment(0xb6e4, 'a real (float) loop?', align=Align.INLINE)
d.comment(0xb6e6, 'yes: float NEXT', align=Align.INLINE)
d.comment(0xb6e8, 'Integer: add STEP to the variable:', align=Align.INLINE)
d.comment(0xb6ea, 'byte 0', align=Align.INLINE)
d.comment(0xb6ec, '+ step byte 0', align=Align.INLINE)
d.comment(0xb6ef, '(store)', align=Align.INLINE)
d.comment(0xb6f1, '(keep)', align=Align.INLINE)
d.comment(0xb6f3, 'byte 1', align=Align.INLINE)
d.comment(0xb6f4, 'variable byte 1', align=Align.INLINE)
d.comment(0xb6f6, '+ step byte 1', align=Align.INLINE)
d.comment(0xb6f9, '(store)', align=Align.INLINE)
d.comment(0xb6fb, '(keep)', align=Align.INLINE)
d.comment(0xb6fd, 'byte 2', align=Align.INLINE)
d.comment(0xb6fe, 'variable byte 2', align=Align.INLINE)
d.comment(0xb700, '+ step byte 2', align=Align.INLINE)
d.comment(0xb703, '(store)', align=Align.INLINE)
d.comment(0xb705, '(keep)', align=Align.INLINE)
d.comment(0xb707, 'byte 3', align=Align.INLINE)
d.comment(0xb708, 'variable byte 3', align=Align.INLINE)
d.comment(0xb70a, '+ step byte 3', align=Align.INLINE)
d.comment(0xb70d, '(store)', align=Align.INLINE)
d.comment(0xb70f, '(keep)', align=Align.INLINE)
d.comment(0xb710, 'Compare the new value with LIMIT:', align=Align.INLINE)
d.comment(0xb712, 'set carry for the subtract', align=Align.INLINE)
d.comment(0xb713, 'value - limit: byte 0', align=Align.INLINE)
d.comment(0xb716, '(keep)', align=Align.INLINE)
d.comment(0xb718, 'byte 1', align=Align.INLINE)
d.comment(0xb71a, 'minus limit byte 1', align=Align.INLINE)
d.comment(0xb71d, '(keep)', align=Align.INLINE)
d.comment(0xb71f, 'byte 2', align=Align.INLINE)
d.comment(0xb721, 'minus limit byte 2', align=Align.INLINE)
d.comment(0xb724, '(keep)', align=Align.INLINE)
d.comment(0xb726, 'byte 3', align=Align.INLINE)
d.comment(0xb727, 'minus limit byte 3', align=Align.INLINE)
d.comment(0xb72a, 'exactly equal to the limit?', align=Align.INLINE)
d.comment(0xb72c, 'OR byte 1,', align=Align.INLINE)
d.comment(0xb72e, 'byte 2 (all zero => equal)', align=Align.INLINE)
d.comment(0xb730, 'at the limit: last iteration, continue', align=Align.INLINE)
d.comment(0xb732, 'Past the limit? (sign of step vs difference)', align=Align.INLINE)
d.comment(0xb733, 'XOR the step sign,', align=Align.INLINE)
d.comment(0xb736, 'XOR the limit sign,', align=Align.INLINE)
d.comment(0xb739, 'sign positive: use the carry test', align=Align.INLINE)
d.comment(0xb73b, 'within range: continue', align=Align.INLINE)
d.comment(0xb73d, 'past: exit the loop', align=Align.INLINE)
d.comment(0xb73f, 'past: exit the loop', align=Align.INLINE)
d.label(0xb73f, 'next_exit')
d.comment(0xb741, 'Continue: reload the loop-back position:', align=Align.INLINE)
d.label(0xb741, 'next_continue')
d.comment(0xb744, 'loop-back pointer high', align=Align.INLINE)
d.comment(0xb747, '(text pointer)', align=Align.INLINE)
d.comment(0xb749, 'text pointer high', align=Align.INLINE)
d.comment(0xb74b, 'restore the offset', align=Align.INLINE)
d.comment(0xb74e, 'jump back to the loop body', align=Align.INLINE)
d.comment(0xb751, 'Exit: pop the FOR frame:', align=Align.INLINE)
d.label(0xb751, 'next_pop_frame')
d.comment(0xb753, 'set carry,', align=Align.INLINE)
d.comment(0xb754, 'minus 15 bytes,', align=Align.INLINE)
d.comment(0xb756, 'pop the frame', align=Align.INLINE)
d.comment(0xb758, 'continue after NEXT:', align=Align.INLINE)
d.comment(0xb75a, 'sync the program offset', align=Align.INLINE)
d.comment(0xb75c, 'another NEXT variable (comma)?', align=Align.INLINE)
d.comment(0xb75f, "','?", align=Align.INLINE)
d.char_literal(0xb760)
d.comment(0xb761, 'no: end of statement', align=Align.INLINE)
d.comment(0xb763, 'yes: handle the next variable', align=Align.INLINE)
d.comment(0xb766, 'Float loop: load the control variable', align=Align.INLINE)
d.label(0xb766, 'next_float')
d.comment(0xb769, 'point at the STEP in the frame:', align=Align.INLINE)
d.comment(0xb76b, 'clear carry,', align=Align.INLINE)
d.comment(0xb76c, 'level + &F4,', align=Align.INLINE)
d.comment(0xb76e, 'pointer low,', align=Align.INLINE)
d.comment(0xb770, 'page &05,', align=Align.INLINE)
d.comment(0xb772, 'pointer high (STEP address)', align=Align.INLINE)
d.comment(0xb774, 'add STEP to the variable', align=Align.INLINE)
d.comment(0xb777, 'store it back:', align=Align.INLINE)
d.comment(0xb779, 'var address low,', align=Align.INLINE)
d.comment(0xb77b, 'high byte,', align=Align.INLINE)
d.comment(0xb77d, 'var address high', align=Align.INLINE)
d.comment(0xb77f, 'store the updated variable', align=Align.INLINE)
d.comment(0xb782, 'point at the LIMIT:', align=Align.INLINE)
d.comment(0xb784, 'stash the level in &27,', align=Align.INLINE)
d.comment(0xb786, 'clear carry,', align=Align.INLINE)
d.comment(0xb787, 'level + &F9,', align=Align.INLINE)
d.comment(0xb789, 'pointer low,', align=Align.INLINE)
d.comment(0xb78b, 'page &05,', align=Align.INLINE)
d.comment(0xb78d, 'pointer high (LIMIT address)', align=Align.INLINE)
d.comment(0xb78f, 'compare the variable with LIMIT', align=Align.INLINE)
d.comment(0xb792, 'at the limit: continue', align=Align.INLINE)
d.comment(0xb794, 'sign of STEP...', align=Align.INLINE)
d.comment(0xb797, 'negative step', align=Align.INLINE)
d.comment(0xb799, 'within range: continue', align=Align.INLINE)
d.comment(0xb79b, 'past: exit', align=Align.INLINE)
d.comment(0xb79d, 'within range: continue', align=Align.INLINE)
d.label(0xb79d, 'next_in_range')
d.comment(0xb79f, 'past: exit', align=Align.INLINE)
d.comment(0xb7a1, 'End of statement', align=Align.INLINE)
d.label(0xb7a1, 'next_end')
d.comment(0xb7a4, 'No FOR error block', align=Align.INLINE)
d.label(0xb7a4, 'no_for_error')
d.comment(0xb7b0, 'error block', align=Align.INLINE)
d.label(0xb7b0, 'too_many_fors')
d.comment(0xb7bd, 'error block', align=Align.INLINE)

d.label(0xb7bd, 'cant_match_for')
# --- FOR / NEXT: counted loops on the FOR stack ----------------------
# Each FOR pushes a 15-byte frame on the FOR/GOSUB stack (&0500),
# indexed by zp_for_level (= 15 * the nesting depth): the control-
# variable pointer, the limit and the step, plus the loop-back position.
d.comment(0xb7c4, 'Parse the control variable (numvar =)', align=Align.INLINE)
# ----------------------------------------------------------------------
# stmt_for (&B7C4): the FOR statement.
# Builds a 15-byte control frame on the FOR stack at &0500, indexed by
# the FOR level &26: loop-variable pointer (+0..+2), STEP (+3), limit
# (+8) and the loop-body text pointer (+D). Integer loops store 4-byte
# values; real loops store packed 5-byte reals.
# ----------------------------------------------------------------------
d.comment(0xb7c7, 'not a variable: error', align=Align.INLINE)
d.comment(0xb7c9, 'indirection: error', align=Align.INLINE)
d.comment(0xb7cb, 'Stack the variable pointer', align=Align.INLINE)
d.comment(0xb7ce, 'Expect "="', align=Align.INLINE)
d.comment(0xb7d1, 'Assign the initial value', align=Align.INLINE)
d.comment(0xb7d4, 'Index the FOR stack by nesting level', align=Align.INLINE)
d.comment(0xb7d6, 'At most 10 nested FOR loops (10 * 15)', align=Align.INLINE)
d.comment(0xb7d8, 'yes: error', align=Align.INLINE)
d.comment(0xb7da, 'Store the variable pointer in the frame (+0)',
          align=Align.INLINE)
d.comment(0xb7dc, 'pointer low (+0),', align=Align.INLINE)
d.comment(0xb7df, 'high byte,', align=Align.INLINE)
d.comment(0xb7e1, 'pointer high (+1)', align=Align.INLINE)
d.comment(0xb7e4, '...and its type (+2)', align=Align.INLINE)
d.comment(0xb7e6, 'type (+2)', align=Align.INLINE)
d.comment(0xb7e9, 'keep the type', align=Align.INLINE)
d.comment(0xb7ea, 'Next character', align=Align.INLINE)
d.comment(0xb7ed, 'Require the TO keyword', align=Align.INLINE)
d.comment(0xb7ef, 'no: No TO error', align=Align.INLINE)
d.comment(0xb7f1, 'real loop variable?', align=Align.INLINE)
d.comment(0xb7f3, 'yes: real FOR loop', align=Align.INLINE)
d.comment(0xb7f5, 'Integer: evaluate the limit', align=Align.INLINE)
d.comment(0xb7f8, 'FOR level', align=Align.INLINE)
d.comment(0xb7fa, 'Store the limit in the frame (+8)', align=Align.INLINE)
d.comment(0xb7fc, 'limit byte 0 (+8),', align=Align.INLINE)
d.comment(0xb7ff, 'byte 1,', align=Align.INLINE)
d.comment(0xb801, '(+9),', align=Align.INLINE)
d.comment(0xb804, 'byte 2,', align=Align.INLINE)
d.comment(0xb806, '(+A),', align=Align.INLINE)
d.comment(0xb809, 'byte 3,', align=Align.INLINE)
d.comment(0xb80b, '(+B)', align=Align.INLINE)
d.comment(0xb80e, 'Default STEP = 1', align=Align.INLINE)
d.comment(0xb810, 'IWA = 1', align=Align.INLINE)
d.comment(0xb813, 'Next character', align=Align.INLINE)
d.comment(0xb816, 'Optional STEP (otherwise step defaults to 1)',
          align=Align.INLINE)
d.comment(0xb818, 'no: use the default', align=Align.INLINE)
d.comment(0xb81a, 'Evaluate the step', align=Align.INLINE)
d.comment(0xb81d, 'update the offset', align=Align.INLINE)
d.comment(0xb81f, 'Sync the program pointer', align=Align.INLINE)
# stmt_for
d.label(0xb81f, 'for_sync')
d.comment(0xb821, 'FOR level', align=Align.INLINE)
d.comment(0xb823, 'Store the step in the frame (+3)', align=Align.INLINE)
d.comment(0xb825, 'step byte 0 (+3),', align=Align.INLINE)
d.comment(0xb828, 'byte 1,', align=Align.INLINE)
d.comment(0xb82a, '(+4),', align=Align.INLINE)
d.comment(0xb82d, 'byte 2,', align=Align.INLINE)
d.comment(0xb82f, '(+5),', align=Align.INLINE)
d.comment(0xb832, 'byte 3,', align=Align.INLINE)
d.comment(0xb834, '(+6)', align=Align.INLINE)
d.comment(0xb837, 'Step over the loop body to find its start',
          align=Align.INLINE)
d.label(0xb837, 'for_skip_body')
d.comment(0xb83a, 'FOR level', align=Align.INLINE)
d.comment(0xb83c, 'Store the loop-body pointer (+D)', align=Align.INLINE)
d.comment(0xb83e, 'low (+D),', align=Align.INLINE)
d.comment(0xb841, 'high byte,', align=Align.INLINE)
d.comment(0xb843, '(+E)', align=Align.INLINE)
d.comment(0xb846, 'Advance the FOR level by 15', align=Align.INLINE)
d.comment(0xb847, 'level to A,', align=Align.INLINE)
d.comment(0xb848, '+ 15,', align=Align.INLINE)
d.comment(0xb84a, 'store it', align=Align.INLINE)
d.comment(0xb84c, 'Continue execution', align=Align.INLINE)
# Real FOR path.
d.comment(0xb84f, 'Evaluate the limit', align=Align.INLINE)
d.label(0xb84f, 'for_eval_limit')
d.comment(0xb852, 'ensure it is real', align=Align.INLINE)
d.comment(0xb855, 'Point at frame +8 (limit slot)', align=Align.INLINE)
d.comment(0xb857, 'level + 8:', align=Align.INLINE)
d.comment(0xb858, 'offset,', align=Align.INLINE)
d.comment(0xb85a, 'pointer low,', align=Align.INLINE)
d.comment(0xb85c, 'page &05,', align=Align.INLINE)
d.comment(0xb85e, 'pointer high', align=Align.INLINE)
d.comment(0xb860, 'Pack the limit there', align=Align.INLINE)
d.comment(0xb863, 'Default STEP = 1.0', align=Align.INLINE)
d.comment(0xb866, 'Next character', align=Align.INLINE)
d.comment(0xb869, 'STEP token?', align=Align.INLINE)
d.comment(0xb86b, 'no: use the default', align=Align.INLINE)
d.comment(0xb86d, 'Evaluate the step', align=Align.INLINE)
d.comment(0xb870, 'ensure it is real', align=Align.INLINE)
d.comment(0xb873, 'update the offset', align=Align.INLINE)
d.comment(0xb875, 'Sync the program pointer', align=Align.INLINE)
d.label(0xb875, 'for_sync2')

d.comment(0xb877, 'Point at frame +3 (step slot)', align=Align.INLINE)
d.comment(0xb879, 'level + 3:', align=Align.INLINE)
d.comment(0xb87a, 'offset,', align=Align.INLINE)
d.comment(0xb87c, 'pointer low,', align=Align.INLINE)
d.comment(0xb87e, 'page &05,', align=Align.INLINE)
d.comment(0xb880, 'pointer high', align=Align.INLINE)
d.comment(0xb882, 'Pack the step there', align=Align.INLINE)
d.comment(0xb885, 'Join the common tail', align=Align.INLINE)

d.comment(0xb888, 'Resolve the destination line', align=Align.INLINE)
# stmt_gosub (&B888), stmt_return (&B8B6), stmt_goto (&B8CC), ON ERROR.
d.comment(0xb88b, 'Check the statement ends', align=Align.INLINE)
d.label(0xb88b, 'gosub_check_end')
d.comment(0xb88e, 'Index the GOSUB return stack', align=Align.INLINE)
d.comment(0xb890, 'At most 26 nested GOSUBs', align=Align.INLINE)
d.comment(0xb892, 'too many: error', align=Align.INLINE)
d.comment(0xb894, 'Push the return position (text pointer)', align=Align.INLINE)
d.comment(0xb896, 'low byte', align=Align.INLINE)
d.comment(0xb899, 'return position high byte', align=Align.INLINE)
d.comment(0xb89b, 'store it', align=Align.INLINE)
d.comment(0xb89e, 'one more nesting level', align=Align.INLINE)
d.comment(0xb8a0, 'jump to the line', align=Align.INLINE)
d.label(0xb8a2, 'err_too_many_gosubs')   # GOSUB stack full
d.comment(0xb8a2, 'Too many GOSUBs error', align=Align.INLINE)
d.label(0xb8af, 'err_no_gosub')          # RETURN with no GOSUB pending
d.comment(0xb8af, 'No GOSUB error', align=Align.INLINE)
d.comment(0xb8b6, 'Check the statement ends', align=Align.INLINE)
d.comment(0xb8b9, 'RETURN with nothing on the GOSUB stack: error',
          align=Align.INLINE)
d.comment(0xb8bb, 'nothing stacked: error', align=Align.INLINE)
d.comment(0xb8bd, 'Pop the return position', align=Align.INLINE)
d.comment(0xb8bf, 'return position low byte', align=Align.INLINE)
d.comment(0xb8c2, '...high byte', align=Align.INLINE)
d.comment(0xb8c5, 'restore the text pointer', align=Align.INLINE)
d.comment(0xb8c7, 'high byte', align=Align.INLINE)
d.comment(0xb8c9, 'Resume execution after the GOSUB', align=Align.INLINE)
d.comment(0xb8cc, 'Resolve the destination line', align=Align.INLINE)
d.comment(0xb8cf, 'check the statement ends', align=Align.INLINE)
d.comment(0xb8d2, 'TRACE: report the destination line number',
          align=Align.INLINE)
# stmt_goto / stmt_on
d.label(0xb8d2, 'goto_trace')
d.comment(0xb8d4, 'TRACE off?', align=Align.INLINE)
d.comment(0xb8d6, 'trace the line', align=Align.INLINE)
d.comment(0xb8d9, 'Destination line pointer', align=Align.INLINE)
d.label(0xb8d9, 'goto_dest_ptr')
d.comment(0xb8db, 'high byte', align=Align.INLINE)
d.comment(0xb8dd, 'Point the interpreter at the destination line',
          align=Align.INLINE)

d.label(0xb8dd, 'goto_jump')
d.comment(0xb8df, 'PtrA high', align=Align.INLINE)
d.comment(0xb8e1, 'execute from there', align=Align.INLINE)
d.comment(0xb8e4, 'Check the statement ends', align=Align.INLINE)
d.label(0xb8e4, 'goto_check_end')
d.comment(0xb8e7, 'Restore the default error handler', align=Align.INLINE)
d.comment(0xb8e9, 'low byte = &33,', align=Align.INLINE)
d.comment(0xb8eb, 'high byte = &B4,', align=Align.INLINE)
d.comment(0xb8ed, 'handler at &B433', align=Align.INLINE)
d.comment(0xb8ef, 'next statement', align=Align.INLINE)
d.comment(0xb8f2, 'Next character', align=Align.INLINE)
d.label(0xb8f2, 'goto_char_loop')
d.comment(0xb8f5, 'OFF token?', align=Align.INLINE)
d.comment(0xb8f7, 'yes: ON ERROR OFF', align=Align.INLINE)
d.comment(0xb8f9, 'Point at the handler statement', align=Align.INLINE)
d.comment(0xb8fb, 'back up,', align=Align.INLINE)
d.comment(0xb8fc, 'check Escape', align=Align.INLINE)
d.comment(0xb8ff, 'Set the error handler to this line', align=Align.INLINE)
d.comment(0xb901, 'low byte,', align=Align.INLINE)
d.comment(0xb903, 'high byte,', align=Align.INLINE)
d.comment(0xb905, 'store it', align=Align.INLINE)
d.comment(0xb907, 'skip the rest of the line', align=Align.INLINE)
d.comment(0xb90a, 'ON syntax error', align=Align.INLINE)

d.label(0xb90a, 'on_syntax_error')
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
d.comment(0xb926, 'past the token,', align=Align.INLINE)
d.comment(0xb927, 'sync the offset', align=Align.INLINE)
d.comment(0xb929, 'GOTO token?', align=Align.INLINE)
d.comment(0xb92b, 'yes', align=Align.INLINE)
d.comment(0xb92d, 'GOSUB token?', align=Align.INLINE)
d.comment(0xb92f, 'no: syntax error', align=Align.INLINE)
d.comment(0xb931, 'Save the GOTO/GOSUB token', align=Align.INLINE)
d.label(0xb931, 'on_save_token')
d.comment(0xb932, 'push it', align=Align.INLINE)
d.comment(0xb933, 'Selector > 255?', align=Align.INLINE)
d.comment(0xb935, 'OR byte 2,', align=Align.INLINE)
d.comment(0xb937, 'byte 3 (any => > 255)', align=Align.INLINE)
d.comment(0xb939, 'yes: out of range', align=Align.INLINE)
d.comment(0xb93b, 'Selector zero?', align=Align.INLINE)
d.comment(0xb93d, 'yes: out of range', align=Align.INLINE)
d.comment(0xb93f, 'Count down to the n-th destination', align=Align.INLINE)
d.comment(0xb940, 'reached it: use the first', align=Align.INLINE)
d.comment(0xb942, 'Line index', align=Align.INLINE)
d.comment(0xb944, 'Next character', align=Align.INLINE)
d.label(0xb944, 'on_char_loop')
d.comment(0xb946, 'advance', align=Align.INLINE)
d.comment(0xb947, 'end of line?', align=Align.INLINE)
d.comment(0xb949, 'yes: out of range', align=Align.INLINE)
d.comment(0xb94b, "':' end of statement?", align=Align.INLINE)
d.char_literal(0xb94c)
d.comment(0xb94d, 'yes: out of range', align=Align.INLINE)
d.comment(0xb94f, 'ELSE?', align=Align.INLINE)
d.comment(0xb951, 'yes: out of range', align=Align.INLINE)
d.comment(0xb953, "',' separator?", align=Align.INLINE)
d.char_literal(0xb954)
d.comment(0xb955, 'no: keep scanning', align=Align.INLINE)
d.comment(0xb957, 'count this destination', align=Align.INLINE)
d.comment(0xb958, 'not yet reached: continue', align=Align.INLINE)
d.comment(0xb95a, 'Save the line index', align=Align.INLINE)
d.comment(0xb95c, 'Read the destination line number', align=Align.INLINE)
d.label(0xb95c, 'on_read_dest')
d.comment(0xb95f, 'Recover the token', align=Align.INLINE)
d.comment(0xb960, 'GOSUB?', align=Align.INLINE)
d.comment(0xb962, 'yes', align=Align.INLINE)
d.comment(0xb964, 'GOTO: update the index and check Escape',
          align=Align.INLINE)
d.comment(0xb967, 'jump to the line', align=Align.INLINE)
d.comment(0xb96a, 'GOSUB: line pointer', align=Align.INLINE)
d.label(0xb96a, 'on_gosub_ptr')
d.comment(0xb96c, 'Next character', align=Align.INLINE)
d.label(0xb96c, 'on_skip_loop')
d.comment(0xb96e, 'advance', align=Align.INLINE)
d.comment(0xb96f, 'end of line?', align=Align.INLINE)
d.comment(0xb971, 'yes: return point here', align=Align.INLINE)
d.comment(0xb973, "':' separator?", align=Align.INLINE)
d.char_literal(0xb974)
d.comment(0xb975, 'no: keep scanning to the return point', align=Align.INLINE)
d.comment(0xb977, 'Set the return index', align=Align.INLINE)
d.label(0xb977, 'on_return_index')
d.comment(0xb978, 'save it', align=Align.INLINE)
d.comment(0xb97a, 'do the GOSUB', align=Align.INLINE)
d.comment(0xb97d, 'Out of range: line index', align=Align.INLINE)
d.label(0xb97d, 'on_out_of_range')
d.comment(0xb97f, 'drop the token', align=Align.INLINE)
d.comment(0xb980, 'Next character', align=Align.INLINE)
d.label(0xb980, 'on_scan_loop')
d.comment(0xb982, 'advance', align=Align.INLINE)
d.comment(0xb983, 'ELSE?', align=Align.INLINE)
d.comment(0xb985, 'yes: use it', align=Align.INLINE)
d.comment(0xb987, 'end of line?', align=Align.INLINE)
d.comment(0xb989, 'no: keep scanning', align=Align.INLINE)
d.comment(0xb98b, 'ON range error', align=Align.INLINE)
d.comment(0xb995, 'Step past ELSE', align=Align.INLINE)
d.label(0xb995, 'on_else')
d.comment(0xb997, 'execute what follows', align=Align.INLINE)

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
    on_entry={'zp_text_ptr (&0B/&0C)': 'the program text pointer (PtrA)',
              'zp_text_ptr_off (&0A)': 'offset at the line-number operand'},
    on_exit={'(zp_fwb_exp) (&3D/&3E)': 'a pointer to the target line',
             'BRK': 'No such line if the line is absent'},
)
# find_line_target (&B99A): read a line number then locate the line.
d.comment(0xb99a, 'Embedded line-number token?', align=Align.INLINE)
d.comment(0xb99d, 'yes: use it', align=Align.INLINE)
d.comment(0xb99f, 'Evaluate the line-number expression', align=Align.INLINE)
d.comment(0xb9a2, 'ensure integer', align=Align.INLINE)
d.comment(0xb9a5, 'Update the program pointer', align=Align.INLINE)
d.comment(0xb9a7, 'from the PtrB offset', align=Align.INLINE)
d.comment(0xb9a9, 'Mask the high byte to 7 bits', align=Align.INLINE)
d.comment(0xb9ab, '(so GOTO &8000+n == GOTO n)', align=Align.INLINE)
d.comment(0xb9ad, 'store the masked high byte', align=Align.INLINE)
d.comment(0xb9af, 'Find the line', align=Align.INLINE)
# find_line_target
d.label(0xb9af, 'flt_find')
d.comment(0xb9b2, 'not found: No such line', align=Align.INLINE)
d.comment(0xb9b4, 'Return', align=Align.INLINE)

d.label(0xb9b5, 'err_no_such_line')      # line number not in the program
d.comment(0xb9b5, 'No such line error', align=Align.INLINE)
d.comment(0xb9c4, 'Type mismatch error', align=Align.INLINE)
d.label(0xb9c4, 'flt_type_error')
d.comment(0xb9c7, 'Mistake error', align=Align.INLINE)
d.label(0xb9c7, 'flt_mistake')
d.comment(0xb9ca, 'Sync the pointer', align=Align.INLINE)
d.label(0xb9ca, 'flt_sync')
d.comment(0xb9cc, 'check the statement ends', align=Align.INLINE)
# INPUT# (&B9CF): read variables from an open file via OSBGET.
d.comment(0xb9cf, 'Back up over "#"', align=Align.INLINE)
# INPUT# file read
d.label(0xb9cf, 'inputf_skip_hash')
d.comment(0xb9d1, 'Get the file handle', align=Align.INLINE)
d.comment(0xb9d4, 'Sync the program pointer', align=Align.INLINE)
d.comment(0xb9d6, 'from the PtrB offset', align=Align.INLINE)
d.comment(0xb9d8, 'save the handle', align=Align.INLINE)
d.comment(0xb9da, 'Skip spaces', align=Align.INLINE)
d.label(0xb9da, 'inputf_skip_spaces')
d.comment(0xb9dd, "','  another variable?", align=Align.INLINE)
d.char_literal(0xb9de)
d.comment(0xb9df, 'no: done', align=Align.INLINE)
d.comment(0xb9e1, 'Save the handle', align=Align.INLINE)
d.comment(0xb9e3, 'push it', align=Align.INLINE)
d.comment(0xb9e4, 'Parse the target variable', align=Align.INLINE)
d.comment(0xb9e7, 'end: error', align=Align.INLINE)
d.comment(0xb9e9, 'Sync the program pointer', align=Align.INLINE)
d.comment(0xb9eb, 'from the PtrB offset', align=Align.INLINE)
d.comment(0xb9ed, 'Recover the handle', align=Align.INLINE)
d.comment(0xb9ee, 'store it (&4D),', align=Align.INLINE)
d.comment(0xb9f0, 'save the type flags', align=Align.INLINE)
d.comment(0xb9f1, 'Stack the variable address', align=Align.INLINE)
d.comment(0xb9f4, 'Handle', align=Align.INLINE)
d.comment(0xb9f6, 'Read the type byte', align=Align.INLINE)
d.comment(0xb9f9, 'save it', align=Align.INLINE)
d.comment(0xb9fb, 'restore the type flags', align=Align.INLINE)
d.comment(0xb9fc, 'string?', align=Align.INLINE)
d.comment(0xb9fe, 'String type byte', align=Align.INLINE)
d.comment(0xba00, 'mismatch: error', align=Align.INLINE)
d.comment(0xba02, 'Read the length', align=Align.INLINE)
d.comment(0xba05, 'store the length,', align=Align.INLINE)
d.comment(0xba07, 'into X as the count', align=Align.INLINE)
d.comment(0xba08, 'empty', align=Align.INLINE)
d.comment(0xba0a, 'Read a character', align=Align.INLINE)
d.label(0xba0a, 'inputf_read_loop')
d.comment(0xba0d, 'into the buffer (reversed),', align=Align.INLINE)
d.comment(0xba10, 'next character', align=Align.INLINE)
d.comment(0xba11, 'loop', align=Align.INLINE)
d.comment(0xba13, 'Assign the string', align=Align.INLINE)
d.label(0xba13, 'inputf_assign_str')
d.comment(0xba16, 'next variable', align=Align.INLINE)
d.comment(0xba19, 'Numeric type byte', align=Align.INLINE)
d.label(0xba19, 'inputf_numeric')
d.comment(0xba1b, 'mismatch: error', align=Align.INLINE)
d.comment(0xba1d, 'real?', align=Align.INLINE)
d.comment(0xba1f, 'Integer: 4 bytes', align=Align.INLINE)
d.comment(0xba21, 'Read a byte', align=Align.INLINE)
d.label(0xba21, 'inputf_int_loop')
d.comment(0xba24, 'into IWA (MSB first),', align=Align.INLINE)
d.comment(0xba26, 'next byte', align=Align.INLINE)
d.comment(0xba27, 'loop', align=Align.INLINE)
d.comment(0xba29, 'assign', align=Align.INLINE)
d.comment(0xba2b, 'Real: 5 bytes', align=Align.INLINE)
d.label(0xba2b, 'inputf_real')
d.comment(0xba2d, 'Read a byte', align=Align.INLINE)
d.label(0xba2d, 'inputf_real_loop')
d.comment(0xba30, 'into TEMP1 (MSB first),', align=Align.INLINE)
d.comment(0xba33, 'next byte', align=Align.INLINE)
d.comment(0xba34, 'loop', align=Align.INLINE)
d.comment(0xba36, 'unpack into FWA', align=Align.INLINE)
d.comment(0xba39, 'Assign the number', align=Align.INLINE)
d.label(0xba39, 'inputf_assign_num')
d.comment(0xba3c, 'next variable', align=Align.INLINE)
d.comment(0xba3f, 'Drop the stacked values', align=Align.INLINE)
d.label(0xba3f, 'inputf_drop_loop')

d.comment(0xba40, '(continued)', align=Align.INLINE)
d.comment(0xba41, 'done', align=Align.INLINE)

# ----------------------------------------------------------------------
# stmt_input (&BA44): the INPUT statement.
# Handles INPUT, INPUT LINE and INPUT#. Prints any prompt items, reads a
# line from the keyboard, then for each variable extracts the next
# comma-separated field and assigns it (the whole line in LINE mode).
# &4D holds flags (bit6 = LINE, bit7 = item-seen), &4E the prompt flag.
# ----------------------------------------------------------------------
d.comment(0xba44, 'Next non-space character', align=Align.INLINE)
d.comment(0xba47, "'#': INPUT# from a file", align=Align.INLINE)
d.char_literal(0xba48)
d.comment(0xba49, 'go handle INPUT#', align=Align.INLINE)
d.comment(0xba4b, 'LINE token?', align=Align.INLINE)
d.comment(0xba4d, 'yes: LINE mode (carry set)', align=Align.INLINE)
d.comment(0xba4f, 'no: step back, carry clear', align=Align.INLINE)
d.comment(0xba51, 'carry clear (not LINE)', align=Align.INLINE)
d.comment(0xba52, 'Record the LINE flag in bit 6', align=Align.INLINE)
d.label(0xba52, 'input_line_flag')
d.comment(0xba54, 'shift it into bit 6', align=Align.INLINE)
d.comment(0xba56, 'Prompt flag = -1', align=Align.INLINE)
d.comment(0xba58, 'store it (&4E)', align=Align.INLINE)
d.comment(0xba5a, 'Process a prompt item', align=Align.INLINE)
d.label(0xba5a, 'input_prompt')
d.comment(0xba5d, 'none found: parse a variable', align=Align.INLINE)
d.comment(0xba5f, 'Process further prompt items', align=Align.INLINE)
d.label(0xba5f, 'input_prompt_loop')
d.comment(0xba62, 'more printed items: loop', align=Align.INLINE)
d.comment(0xba64, 'A printed item suppresses the ? prompt', align=Align.INLINE)
d.comment(0xba66, 'flag = -1 (printed),', align=Align.INLINE)
d.comment(0xba68, 'carry clear', align=Align.INLINE)
d.comment(0xba69, 'Preserve the item-seen flag', align=Align.INLINE)
d.label(0xba69, 'input_item_flag')
d.comment(0xba6a, 'shift out the old bit,', align=Align.INLINE)
d.comment(0xba6c, 'recover the flag,', align=Align.INLINE)
d.comment(0xba6d, 'rotate it into bit 7', align=Align.INLINE)
d.comment(0xba6f, "','  next item?", align=Align.INLINE)
d.char_literal(0xba70)
d.comment(0xba71, 'yes', align=Align.INLINE)
d.comment(0xba73, "';'  next item?", align=Align.INLINE)
d.char_literal(0xba74)
d.comment(0xba75, 'yes', align=Align.INLINE)
d.comment(0xba77, 'Back up to the variable', align=Align.INLINE)
d.comment(0xba79, 'Save the flags...', align=Align.INLINE)
d.comment(0xba7b, 'push &4D,', align=Align.INLINE)
d.comment(0xba7c, '&4E,', align=Align.INLINE)
d.comment(0xba7e, 'push it', align=Align.INLINE)
d.comment(0xba7f, 'Parse the target variable', align=Align.INLINE)
d.comment(0xba82, 'end of statement: done', align=Align.INLINE)
d.comment(0xba84, 'Restore the flags', align=Align.INLINE)
d.comment(0xba85, '&4E,', align=Align.INLINE)
d.comment(0xba87, 'pull &4D,', align=Align.INLINE)
d.comment(0xba88, 'store it', align=Align.INLINE)
d.comment(0xba8a, 'Update the program pointer', align=Align.INLINE)
d.comment(0xba8c, 'from the PtrB offset', align=Align.INLINE)
d.comment(0xba8e, 'Save the LINE flag', align=Align.INLINE)
d.comment(0xba8f, 'Still reading the current input line?', align=Align.INLINE)
d.comment(0xba91, 'yes: no new prompt', align=Align.INLINE)
d.comment(0xba93, 'Prompt flag', align=Align.INLINE)
d.comment(0xba95, 'item already printed?', align=Align.INLINE)
d.comment(0xba97, 'yes: read without a ? prompt', align=Align.INLINE)
d.comment(0xba99, 'LINE mode?', align=Align.INLINE)
d.label(0xba99, 'input_line_mode')
d.comment(0xba9b, 'yes: no ? prompt', align=Align.INLINE)
d.comment(0xba9d, "Print '?'", align=Align.INLINE)
d.char_literal(0xba9e)
d.comment(0xba9f, 'do it', align=Align.INLINE)
d.comment(0xbaa2, 'Read an input line', align=Align.INLINE)
d.label(0xbaa2, 'input_read_line')
d.comment(0xbaa5, 'Store its length', align=Align.INLINE)
d.comment(0xbaa7, 'Mark the input line as fresh', align=Align.INLINE)
d.comment(0xbaa9, 'clear carry,', align=Align.INLINE)
d.comment(0xbaaa, 'rotate into bit 7', align=Align.INLINE)
d.comment(0xbaac, 'LINE mode?', align=Align.INLINE)
d.comment(0xbaae, 'yes: take the whole line', align=Align.INLINE)
d.comment(0xbab0, 'Set the read offset', align=Align.INLINE)
d.label(0xbab0, 'input_set_offset')
d.comment(0xbab2, 'Point at the input buffer (&0600)', align=Align.INLINE)
d.comment(0xbab4, 'PtrB low = 0,', align=Align.INLINE)
d.comment(0xbab6, 'page &06,', align=Align.INLINE)
d.comment(0xbab8, 'PtrB high', align=Align.INLINE)
d.comment(0xbaba, 'Read the field literal', align=Align.INLINE)
d.comment(0xbabd, 'Skip spaces', align=Align.INLINE)
d.label(0xbabd, 'input_skip_spaces')
d.comment(0xbac0, "','  field delimiter?", align=Align.INLINE)
d.char_literal(0xbac1)
d.comment(0xbac2, 'yes', align=Align.INLINE)
d.comment(0xbac4, 'end of line?', align=Align.INLINE)
d.comment(0xbac6, 'no: keep scanning', align=Align.INLINE)
d.comment(0xbac8, 'mark end of input', align=Align.INLINE)
d.comment(0xbaca, 'Note the next field offset', align=Align.INLINE)
d.label(0xbaca, 'input_field_offset')
d.comment(0xbacb, 'store it (&4E)', align=Align.INLINE)
d.comment(0xbacd, 'Recover the LINE flag', align=Align.INLINE)
d.label(0xbacd, 'input_recover_flag')
d.comment(0xbace, 'LINE mode: assign the whole line', align=Align.INLINE)
d.comment(0xbad0, 'Stack the variable address', align=Align.INLINE)
d.comment(0xbad3, 'Parse the field as a number', align=Align.INLINE)
d.comment(0xbad6, 'assign it', align=Align.INLINE)
d.comment(0xbad9, 'next variable', align=Align.INLINE)
d.comment(0xbadc, 'LINE: string type', align=Align.INLINE)
d.label(0xbadc, 'input_line_string')
d.comment(0xbade, 'type 0 (string)', align=Align.INLINE)
d.comment(0xbae0, 'assign the line as a string', align=Align.INLINE)
d.comment(0xbae3, 'next variable', align=Align.INLINE)

# stmt_restore (&BAE6): RESTORE [line].
d.comment(0xbae6, 'DATA pointer = PAGE', align=Align.INLINE)
d.comment(0xbae8, 'low byte 0 (&3D),', align=Align.INLINE)
d.comment(0xbaea, 'PAGE,', align=Align.INLINE)
d.comment(0xbaec, 'high byte (&3E)', align=Align.INLINE)
d.comment(0xbaee, 'Skip spaces', align=Align.INLINE)
d.comment(0xbaf1, 'back up', align=Align.INLINE)
d.comment(0xbaf3, "':' end?", align=Align.INLINE)
d.char_literal(0xbaf4)
d.comment(0xbaf5, 'yes: restore to PAGE', align=Align.INLINE)
d.comment(0xbaf7, 'end of line?', align=Align.INLINE)
d.comment(0xbaf9, 'yes', align=Align.INLINE)
d.comment(0xbafb, 'ELSE?', align=Align.INLINE)
d.comment(0xbafd, 'yes', align=Align.INLINE)
d.comment(0xbaff, 'Find the given line', align=Align.INLINE)
d.comment(0xbb02, 'point at it', align=Align.INLINE)
d.comment(0xbb04, 'set the pointer to the line', align=Align.INLINE)
d.comment(0xbb07, 'Check the statement ends', align=Align.INLINE)
d.label(0xbb07, 'restore_check_end')
d.comment(0xbb0a, 'Set the DATA pointer', align=Align.INLINE)
d.comment(0xbb0c, 'low byte (&1C),', align=Align.INLINE)
d.comment(0xbb0e, 'high byte,', align=Align.INLINE)
d.comment(0xbb10, 'high (&1D)', align=Align.INLINE)
d.comment(0xbb12, 'next statement', align=Align.INLINE)
d.comment(0xbb15, 'Skip spaces', align=Align.INLINE)
d.label(0xbb15, 'restore_skip_spaces')
d.comment(0xbb18, "','?", align=Align.INLINE)
d.char_literal(0xbb19)
d.comment(0xbb1a, 'yes: READ', align=Align.INLINE)
d.comment(0xbb1c, 'next statement', align=Align.INLINE)

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
d.label(0xbb32, 'read_string')
d.comment(0xbb35, 'Stack the variable address', align=Align.INLINE)
d.comment(0xbb38, 'read the DATA item as a string', align=Align.INLINE)
d.comment(0xbb3b, 'string type', align=Align.INLINE)
d.comment(0xbb3d, 'assign it', align=Align.INLINE)
d.comment(0xbb40, 'Advance the DATA pointer past the item', align=Align.INLINE)
d.label(0xbb40, 'read_advance')
d.comment(0xbb41, 'PtrB offset,', align=Align.INLINE)
d.comment(0xbb43, '+ PtrB low,', align=Align.INLINE)
d.comment(0xbb45, 'DATA pointer low,', align=Align.INLINE)
d.comment(0xbb47, 'PtrB high,', align=Align.INLINE)
d.comment(0xbb49, '+ carry,', align=Align.INLINE)
d.comment(0xbb4b, 'DATA pointer high', align=Align.INLINE)
d.comment(0xbb4d, 'next variable', align=Align.INLINE)

d.subroutine(0xbb50, 'next_data_item',
             title='Advance the DATA pointer to the next item',
             description='Move the DATA pointer past the current item to the '
                         'next comma- or DATA-separated value, searching '
                         'forward through the program for the next DATA '
                         'statement at end of line; raises Out of DATA.',
             on_entry={'zp_data_ptr (&1C)': 'the current DATA read position'},
             on_exit={'zp_text_ptr2 (&19/&1A)': 'PtrB at the next DATA value',
                      'zp_data_ptr (&1C)': 'advanced',
                      'BRK': 'Out of DATA if none remain'})
# next_data_item (&BB50): step the DATA pointer to the next value.
d.comment(0xbb50, 'Save the program pointer', align=Align.INLINE)
d.comment(0xbb52, '(save)', align=Align.INLINE)
d.comment(0xbb54, 'Point at the DATA position', align=Align.INLINE)
d.comment(0xbb56, '(low)', align=Align.INLINE)
d.comment(0xbb58, 'high...', align=Align.INLINE)
d.comment(0xbb5a, '(high)', align=Align.INLINE)
d.comment(0xbb5c, 'From offset 0', align=Align.INLINE)
d.comment(0xbb5e, '(offset 0)', align=Align.INLINE)
d.comment(0xbb60, 'Next character', align=Align.INLINE)
d.comment(0xbb63, "','  item separator?", align=Align.INLINE)
d.char_literal(0xbb64)
d.comment(0xbb65, 'yes: at the next item', align=Align.INLINE)
d.comment(0xbb67, 'DATA token?', align=Align.INLINE)
d.comment(0xbb69, 'yes: at the first item', align=Align.INLINE)
d.comment(0xbb6b, 'end of line?', align=Align.INLINE)
d.comment(0xbb6d, 'yes: find the next DATA line', align=Align.INLINE)
d.comment(0xbb6f, 'Scan to the item end: next character', align=Align.INLINE)
d.label(0xbb6f, 'ndi_scan_loop')
d.comment(0xbb72, "','  separator?", align=Align.INLINE)
d.char_literal(0xbb73)
d.comment(0xbb74, 'yes', align=Align.INLINE)
d.comment(0xbb76, 'end of line?', align=Align.INLINE)
d.comment(0xbb78, 'no: keep scanning', align=Align.INLINE)
d.comment(0xbb7a, 'Line marker', align=Align.INLINE)
d.label(0xbb7a, 'ndi_line_marker')
d.comment(0xbb7c, 'read it', align=Align.INLINE)
d.comment(0xbb7e, 'end of program: Out of DATA', align=Align.INLINE)
d.comment(0xbb80, 'Skip the line number', align=Align.INLINE)
d.comment(0xbb81, 'past the low byte', align=Align.INLINE)
d.comment(0xbb82, 'Line length', align=Align.INLINE)
d.comment(0xbb84, 'X = length', align=Align.INLINE)
d.comment(0xbb85, 'Next character', align=Align.INLINE)
d.label(0xbb85, 'ndi_scan_loop2')
d.comment(0xbb86, 'read it', align=Align.INLINE)
d.comment(0xbb88, 'space?', align=Align.INLINE)
d.char_literal(0xbb89)
d.comment(0xbb8a, 'skip leading spaces', align=Align.INLINE)
d.comment(0xbb8c, 'DATA token?', align=Align.INLINE)
d.comment(0xbb8e, 'yes: use this line', align=Align.INLINE)
d.comment(0xbb90, 'Advance to the next line', align=Align.INLINE)
d.comment(0xbb91, 'add the length...', align=Align.INLINE)
d.comment(0xbb92, 'to the pointer low,', align=Align.INLINE)
d.comment(0xbb94, '(store)', align=Align.INLINE)
d.comment(0xbb96, 'no carry', align=Align.INLINE)
d.comment(0xbb98, 'carry into high', align=Align.INLINE)
d.comment(0xbb9a, 'continue', align=Align.INLINE)
d.comment(0xbb9c, 'Out of DATA error', align=Align.INLINE)
d.label(0xbb9c, 'out_of_data')
# --- REPEAT / UNTIL: condition loop on a 20-entry stack --------------
# REPEAT saves the loop-start position in parallel arrays at &05A4 (low)
# / &05B8 (high), indexed by zp_repeat_level; UNTIL exits when the
# condition is true, otherwise loops back.
d.label(0xbba6, 'err_no_repeat')         # UNTIL with no REPEAT pending
d.comment(0xbba6, 'No REPEAT error', align=Align.INLINE)
d.comment(0xbbad, 'Step past the DATA token', align=Align.INLINE)
d.label(0xbbad, 'ndi_skip_token')
d.comment(0xbbae, 'record the offset', align=Align.INLINE)
d.comment(0xbbb0, 'Return', align=Align.INLINE)

d.comment(0xbbb1, 'Evaluate the UNTIL condition', align=Align.INLINE)
# stmt_until (&BBB1) remaining
d.comment(0xbbb4, 'Check for end of statement', align=Align.INLINE)
d.comment(0xbbb7, 'coerce the condition to an integer', align=Align.INLINE)
d.comment(0xbbba, 'UNTIL with no REPEAT pending: error', align=Align.INLINE)
d.comment(0xbbbc, 'UNTIL with no REPEAT: error', align=Align.INLINE)
d.comment(0xbbbe, 'Test the condition for true (non-zero):', align=Align.INLINE)
d.comment(0xbbc0, 'byte 1,', align=Align.INLINE)
d.comment(0xbbc2, 'byte 2,', align=Align.INLINE)
d.comment(0xbbc4, 'byte 3', align=Align.INLINE)
d.comment(0xbbc6, 'Condition false: loop back to the REPEAT', align=Align.INLINE)
d.comment(0xbbc8, 'Condition true: pop the frame and continue',
          align=Align.INLINE)
d.comment(0xbbca, 'true: exit the loop, continue', align=Align.INLINE)
d.comment(0xbbcd, 'Reload the saved loop-start position', align=Align.INLINE)

d.label(0xbbcd, 'until_reload')
d.comment(0xbbd0, 'Reload the loop position: high', align=Align.INLINE)
d.comment(0xbbd3, 'jump back to the REPEAT', align=Align.INLINE)
d.label(0xbbd6, 'err_too_many_repeats')  # REPEAT stack full
d.comment(0xbbd6, 'BRK error block: too many REPEATs', align=Align.INLINE)

d.comment(0xbbe4, 'Index the REPEAT stack', align=Align.INLINE)
d.comment(0xbbe6, 'At most 20 nested REPEATs', align=Align.INLINE)
# stmt_repeat (&BBE4) remaining
d.comment(0xbbe8, 'Too many nested REPEATs', align=Align.INLINE)
d.comment(0xbbea, 'Point PtrA at the loop start', align=Align.INLINE)
d.comment(0xbbed, 'Push the loop-start position', align=Align.INLINE)
d.comment(0xbbef, 'Store the loop position: low', align=Align.INLINE)
d.comment(0xbbf2, 'high', align=Align.INLINE)
d.comment(0xbbf4, '(store)', align=Align.INLINE)
d.comment(0xbbf7, 'One more REPEAT outstanding', align=Align.INLINE)
d.comment(0xbbf9, 'Continue execution', align=Align.INLINE)
d.comment(0xbbfc, 'Point at the string buffer (&0600): low', align=Align.INLINE)
d.label(0xbbfc, 'point_string_buffer')
d.comment(0xbbfe, 'high', align=Align.INLINE)
d.comment(0xbc00, 'set it (shared tail)', align=Align.INLINE)

d.subroutine(0xbc02, 'read_input_line', title='Print the prompt and read a line',
             description='Print the character in A as a prompt, then read a line '
                         'into the input buffer at &0700 via OSWORD 0.',
             on_entry={'A': 'the prompt character to print'},
             on_exit={'the input buffer (&0700)': 'the line read (CR terminated)',
                      'C': 'set if the read was terminated by Escape'})
# read_input_line (&BC02): print a prompt char, read a line (OSWORD 0).
d.comment(0xbc02, 'Print the prompt character', align=Align.INLINE)
d.comment(0xbc05, 'Input buffer at &0700', align=Align.INLINE)
d.comment(0xbc07, 'high byte &07', align=Align.INLINE)
d.comment(0xbc09, 'address low = &00', align=Align.INLINE)
d.label(0xbc09, 'ril_set_addr')
d.comment(0xbc0b, 'address high = &07', align=Align.INLINE)
d.comment(0xbc0d, 'Max length 238', align=Align.INLINE)
d.comment(0xbc0f, 'store it', align=Align.INLINE)
d.comment(0xbc11, 'Lowest accepted character', align=Align.INLINE)
d.char_literal(0xbc12)
d.comment(0xbc13, 'store it', align=Align.INLINE)
d.comment(0xbc15, 'Highest accepted character (&FF)', align=Align.INLINE)
d.comment(0xbc17, 'store it', align=Align.INLINE)
d.comment(0xbc19, 'Y wraps back to 0', align=Align.INLINE)
d.comment(0xbc1a, 'Point at the OSWORD block', align=Align.INLINE)
d.comment(0xbc1c, 'A = 0: OSWORD read line', align=Align.INLINE)
d.comment(0xbc1d, 'Read a line', align=Align.INLINE)
d.comment(0xbc20, 'ok: reset the column', align=Align.INLINE)
d.comment(0xbc22, 'Escape: raise it', align=Align.INLINE)
d.comment(0xbc25, 'Print a newline', align=Align.INLINE)
d.subroutine(
    0xbc25, 'emit_newline',
    title='Print a newline and reset the print column',
    description="""Emit a newline via OSNEWL, then fall through into reset_print_column
to zero the print-column counter. The standard way BASIC ends an
output line so the column-tracking auto-newline logic stays in step.
""",
    on_exit={
        'zp_count (&1E)': 'reset to 0 (print column)',
        'A': '0',
        'X': 'preserved',
        'Y': 'preserved',
    },
)
d.comment(0xbc28, 'Reset the column to 0', align=Align.INLINE)
d.label(0xbc28, 'reset_print_column')
d.comment(0xbc2a, 'store it', align=Align.INLINE)
d.comment(0xbc2c, 'Return', align=Align.INLINE)

d.subroutine(0xbc2d, 'delete_program_line',
             title='Delete a program line and close the gap',
             description='Find the line (find_program_line), then shift every '
                         'later line down over it and update TOP. No-op if the '
                         'line is absent.',
             on_entry={'zp_iwa (&2A/&2B)': 'the line number to delete'},
             on_exit={'the program': 'the line removed and memory compacted',
                      'zp_top (&12/&13)': 'TOP reduced by the deleted line'})
# delete_program_line (&BC2D): remove a line and compact memory.
d.comment(0xbc2d, 'Find the line', align=Align.INLINE)
d.comment(0xbc30, 'not present: nothing to do', align=Align.INLINE)
d.comment(0xbc32, 'Destination = line start', align=Align.INLINE)
d.comment(0xbc34, 'line start - 2,', align=Align.INLINE)
d.comment(0xbc36, 'destination low (&37),', align=Align.INLINE)
d.comment(0xbc38, 'also &3D,', align=Align.INLINE)
d.comment(0xbc3a, 'and TOP (&12),', align=Align.INLINE)
d.comment(0xbc3c, 'high byte,', align=Align.INLINE)
d.comment(0xbc3e, 'with borrow,', align=Align.INLINE)
d.comment(0xbc40, 'destination high (&38),', align=Align.INLINE)
d.comment(0xbc42, 'and TOP+1 (&13),', align=Align.INLINE)
d.comment(0xbc44, 'and &3E', align=Align.INLINE)
d.comment(0xbc46, "Line length", align=Align.INLINE)
d.comment(0xbc48, 'read it (offset 3)', align=Align.INLINE)
d.comment(0xbc4a, 'Source = the next line', align=Align.INLINE)
d.comment(0xbc4b, 'destination + length,', align=Align.INLINE)
d.comment(0xbc4d, 'source low,', align=Align.INLINE)
d.comment(0xbc4f, 'no carry into the high byte', align=Align.INLINE)
d.comment(0xbc51, 'carry into the high byte', align=Align.INLINE)
d.comment(0xbc53, 'From offset 0', align=Align.INLINE)
d.label(0xbc53, 'del_copy_start')
d.comment(0xbc55, 'Copy a byte down', align=Align.INLINE)
d.label(0xbc55, 'del_copy_loop')
d.comment(0xbc57, 'to the destination', align=Align.INLINE)
d.comment(0xbc59, 'end of line?', align=Align.INLINE)
d.comment(0xbc5b, 'yes: handle the line boundary', align=Align.INLINE)
d.comment(0xbc5d, 'next byte', align=Align.INLINE)
d.label(0xbc5d, 'del_copy_next')
d.comment(0xbc5e, 'no page wrap', align=Align.INLINE)
d.comment(0xbc60, 'cross a page', align=Align.INLINE)
d.comment(0xbc62, 'destination page too', align=Align.INLINE)
d.comment(0xbc64, 'continue', align=Align.INLINE)
d.comment(0xbc66, 'Step past the CR', align=Align.INLINE)
d.label(0xbc66, 'del_skip_cr')
d.comment(0xbc67, 'no page wrap,', align=Align.INLINE)
d.comment(0xbc69, 'source page,', align=Align.INLINE)
d.comment(0xbc6b, 'destination page', align=Align.INLINE)
d.comment(0xbc6d, 'Next line marker', align=Align.INLINE)
d.label(0xbc6d, 'del_next_marker')
d.comment(0xbc6f, 'copy it down', align=Align.INLINE)
d.comment(0xbc71, 'end of program?', align=Align.INLINE)
d.comment(0xbc73, 'no: copy the line number', align=Align.INLINE)
d.comment(0xbc76, '...and the length byte', align=Align.INLINE)
d.comment(0xbc79, 'continue with the line body', align=Align.INLINE)
d.comment(0xbc7c, 'Set the new top of program', align=Align.INLINE)
d.label(0xbc7c, 'del_set_top')
d.comment(0xbc7f, 'carry clear: line was deleted', align=Align.INLINE)
d.comment(0xbc80, 'Return', align=Align.INLINE)
d.comment(0xbc81, 'Copy one byte (source -> destination)', align=Align.INLINE)
d.subroutine(
    0xbc81, 'copy_byte',
    title='Copy one byte, advancing the offset',
    description="""Increment the shared offset Y (bumping both pointer high bytes on a
page crossing), then copy one byte from (zp_general) to (zp_top). The
per-byte helper used by delete_program_line to copy the line-number
and length bytes while compacting the program.
""",
    on_entry={
        'Y': 'the current copy offset',
        '(zp_general) (&37/&38)': 'source pointer',
        '(zp_top) (&12/&13)': 'destination pointer',
    },
    on_exit={
        'Y': 'advanced by 1 (with page carry into &38/&13)',
        'A': 'the byte copied',
        '(zp_top) (&12/&13)': 'receives the copied byte',
    },
)
d.comment(0xbc82, 'no page wrap', align=Align.INLINE)
d.comment(0xbc84, 'cross a page', align=Align.INLINE)
d.comment(0xbc86, 'source page too', align=Align.INLINE)
d.comment(0xbc88, 'read the byte,', align=Align.INLINE)
d.label(0xbc88, 'copy_byte_read')
d.comment(0xbc8a, 'write it down', align=Align.INLINE)
d.comment(0xbc8c, 'Return', align=Align.INLINE)

# Insert a program line (&BC8D): make room and store the typed line.
d.comment(0xbc8d, 'Save the line-buffer pointer', align=Align.INLINE)
d.subroutine(
    0xbc8d, 'insert_line',
    title='Insert a tokenised program line',
    description="""Insert the numbered, tokenised line held in the &0700 input buffer
into the program. First deletes any existing line with the same number
(delete_program_line); if the buffer holds only a CR the edit was a
pure deletion and it returns. Otherwise it measures the line, checks
the new TOP still fits below HIMEM (raising 'LINE space' after tidying
if not), shifts the program up to open a gap, writes the 4-byte line
header (line number + length), copies the line body in, and sets the
new TOP.
""",
    on_entry={
        'zp_iwa (&2A)': 'the line number (&2A/&2B)',
        'Y': 'offset within the &0700 input buffer of the tokenised line text',
        'zp_top (&12)': 'current TOP, the end of the program (&12/&13)',
    },
    on_exit={
        'zp_top (&12)': 'updated past the new line (&12/&13)',
        'control': "raises 'LINE space' (BRK) if the line will not fit below HIMEM",
    },
)
d.comment(0xbc8f, 'Delete any existing line with this number',
          align=Align.INLINE)
d.comment(0xbc92, 'Point past the line header', align=Align.INLINE)
d.comment(0xbc94, 'save offset 7 in &3C', align=Align.INLINE)
d.comment(0xbc96, 'Measure the new line: from offset 0', align=Align.INLINE)
d.comment(0xbc98, 'CR', align=Align.INLINE)
d.comment(0xbc9a, 'empty line (deletion only)?', align=Align.INLINE)
d.comment(0xbc9c, 'yes: done', align=Align.INLINE)
d.comment(0xbc9e, 'Scan to the CR', align=Align.INLINE)
d.label(0xbc9e, 'insline_scan')
d.comment(0xbc9f, 'CR yet?', align=Align.INLINE)
d.comment(0xbca1, 'keep scanning', align=Align.INLINE)
d.comment(0xbca3, 'Add the 4-byte header', align=Align.INLINE)
d.comment(0xbca4, '(continued)', align=Align.INLINE)
d.comment(0xbca5, '(continued)', align=Align.INLINE)
d.comment(0xbca6, 'Line length', align=Align.INLINE)
d.comment(0xbca8, 'include the CR', align=Align.INLINE)
d.comment(0xbcaa, 'Old top of program', align=Align.INLINE)
d.comment(0xbcac, 'low to &39,', align=Align.INLINE)
d.comment(0xbcae, 'high byte,', align=Align.INLINE)
d.comment(0xbcb0, 'to &3A', align=Align.INLINE)
d.comment(0xbcb2, 'New top = old top + line length', align=Align.INLINE)
d.comment(0xbcb5, 'new top low (&37),', align=Align.INLINE)
d.comment(0xbcb7, 'high byte,', align=Align.INLINE)
d.comment(0xbcb9, 'new top high (&38),', align=Align.INLINE)
d.comment(0xbcbb, 'index the last byte (length-1)', align=Align.INLINE)
d.comment(0xbcbc, 'New top vs HIMEM', align=Align.INLINE)
d.comment(0xbcbe, 'low byte vs TOP,', align=Align.INLINE)
d.comment(0xbcc0, 'high byte,', align=Align.INLINE)
d.comment(0xbcc2, 'HIMEM >= new top?', align=Align.INLINE)
d.comment(0xbcc4, 'fits: shift the program up', align=Align.INLINE)
d.comment(0xbcc6, 'no room: tidy up', align=Align.INLINE)
d.comment(0xbcc9, 'clear variables/heap/stack', align=Align.INLINE)
d.comment(0xbccc, 'LINE space error', align=Align.INLINE)
d.comment(0xbcd6, 'Shift a byte up', align=Align.INLINE)
d.label(0xbcd6, 'insline_shift')
d.comment(0xbcd8, 'to the higher address,', align=Align.INLINE)
d.comment(0xbcda, 'at a page boundary?,', align=Align.INLINE)
d.comment(0xbcdb, 'no', align=Align.INLINE)
d.comment(0xbcdd, 'cross a page', align=Align.INLINE)
d.comment(0xbcdf, 'destination page too', align=Align.INLINE)
d.comment(0xbce1, 'Next byte down', align=Align.INLINE)
d.label(0xbce1, 'insline_shift_next')
d.comment(0xbce2, 'offset to A,', align=Align.INLINE)
d.comment(0xbce3, '+ source low,', align=Align.INLINE)
d.comment(0xbce5, 'source high in X,', align=Align.INLINE)
d.comment(0xbce7, 'no carry,', align=Align.INLINE)
d.comment(0xbce9, 'carry into the high byte', align=Align.INLINE)
d.comment(0xbcea, 'reached the insertion point?', align=Align.INLINE)
d.label(0xbcea, 'insline_check')
d.comment(0xbcec, 'high byte,', align=Align.INLINE)
d.comment(0xbced, 'source vs the insertion point', align=Align.INLINE)
d.comment(0xbcef, 'no: keep shifting', align=Align.INLINE)
d.comment(0xbcf1, 'Write the new line header', align=Align.INLINE)
d.comment(0xbcf2, 'from offset 1', align=Align.INLINE)
d.comment(0xbcf4, 'line number high', align=Align.INLINE)
d.comment(0xbcf6, 'store it,', align=Align.INLINE)
d.comment(0xbcf8, 'next', align=Align.INLINE)
d.comment(0xbcf9, 'line number low', align=Align.INLINE)
d.comment(0xbcfb, 'store it,', align=Align.INLINE)
d.comment(0xbcfd, 'next', align=Align.INLINE)
d.comment(0xbcfe, 'line length', align=Align.INLINE)
d.comment(0xbd00, 'store it', align=Align.INLINE)
d.comment(0xbd02, 'Set the new top of program', align=Align.INLINE)
d.comment(0xbd05, 'Copy the line body in: offset 0', align=Align.INLINE)
d.comment(0xbd07, 'advance the index', align=Align.INLINE)
d.label(0xbd07, 'insline_advance')
d.comment(0xbd08, 'buffer byte', align=Align.INLINE)
d.comment(0xbd0a, 'store it', align=Align.INLINE)
d.comment(0xbd0c, 'until the CR', align=Align.INLINE)
d.comment(0xbd0e, 'loop', align=Align.INLINE)

d.comment(0xbd10, 'Return', align=Align.INLINE)

# stmt_run (&BD11): RUN.
d.comment(0xbd11, 'Check the statement ends', align=Align.INLINE)
d.comment(0xbd14, 'Clear variables, heap and stack', align=Align.INLINE)
d.label(0xbd14, 'run_clear')
d.comment(0xbd17, 'Point PtrA at PAGE', align=Align.INLINE)
d.comment(0xbd19, 'page to the high byte,', align=Align.INLINE)
d.comment(0xbd1b, 'low byte = 0 (X)', align=Align.INLINE)
d.comment(0xbd1d, 'execute from the start', align=Align.INLINE)

d.subroutine(0xbd20, 'clear_vars_heap_stack',
             title='Clear all variables, the heap and the stack',
             description='Reset LOMEM and VARTOP to TOP, empty the per-letter '
                         'variable table, and clear the DATA pointer and the '
                         'BASIC stacks (NEW/CLEAR/RUN).',
             on_entry={'zp_top (&12/&13)': 'TOP, the end of the program'},
             on_exit={'zp_lomem (&00/&01)': '= TOP', 'zp_vartop (&02/&03)': '= TOP',
                      'the variable table and stacks': 'cleared'})
# clear_vars_heap_stack (&BD20)
d.comment(0xbd20, 'LOMEM and VARTOP = TOP: low', align=Align.INLINE)
d.comment(0xbd22, 'LOMEM low', align=Align.INLINE)
d.comment(0xbd24, 'VARTOP low', align=Align.INLINE)
d.comment(0xbd26, 'high', align=Align.INLINE)
d.comment(0xbd28, 'LOMEM high', align=Align.INLINE)
d.comment(0xbd2a, 'VARTOP high', align=Align.INLINE)
d.comment(0xbd2c, 'Clear the DATA pointer and the stacks', align=Align.INLINE)
d.comment(0xbd2f, 'Clear the variable table (&0480-&04FF):', align=Align.INLINE)
d.label(0xbd2f, 'clear_var_table')
d.comment(0xbd31, 'zero byte', align=Align.INLINE)
d.comment(0xbd33, 'clear a byte', align=Align.INLINE)
d.label(0xbd33, 'clear_var_table_loop')
d.comment(0xbd36, 'count down', align=Align.INLINE)
d.comment(0xbd37, 'loop', align=Align.INLINE)
d.comment(0xbd39, 'Return', align=Align.INLINE)
d.comment(0xbd3a, 'DATA pointer = PAGE: high', align=Align.INLINE)
d.subroutine(
    0xbd3a, 'reset_data_and_stacks',
    title='Reset the DATA pointer and the BASIC stacks',
    description="""Reset the READ/DATA pointer to PAGE and empty the FOR/REPEAT/GOSUB and
value stacks: point the stack pointer back at HIMEM and zero the
REPEAT, FOR and GOSUB nesting levels. Variables and the heap are left
intact. Called on NEW/CLEAR/RUN as part of clear_vars_heap_stack, and
on the error path.
""",
    on_entry={
        'zp_page (&18)': 'PAGE, the start of the program',
        'zp_himem (&06)': 'HIMEM, the top of memory (&06/&07)',
    },
    on_exit={
        'zp_data_ptr (&1C)': 'reset to PAGE (&1C/&1D)',
        'zp_stack_ptr (&04)': 'reset to HIMEM (stacks emptied) (&04/&05)',
        'zp_repeat_level (&24)': '0',
        'zp_for_level (&26)': '0',
        'zp_gosub_level (&25)': '0',
    },
)
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

d.subroutine(
    0xbd51, 'stack_real',
    title='Push the floating-point accumulator onto the BASIC stack',
    description="""Reserve five bytes on the BASIC stack and copy the packed
floating-point accumulator onto it. Errors if the stack meets the heap.
""",
    on_entry={'zp_fwa (&2E-&35)': 'the real to push'},
    on_exit={'zp_stack_ptr (&04/&05)': 'lowered by 5 (real pushed)'},
)
# stack_real (&BD51): push the packed 5-byte FWA
d.comment(0xbd51, 'From the stack top...', align=Align.INLINE)
d.comment(0xbd53, 'prepare subtraction', align=Align.INLINE)
d.comment(0xbd54, 'Lower the stack by 5 bytes (a packed real)',
          align=Align.INLINE)
d.comment(0xbd56, 'reserve the space', align=Align.INLINE)
d.comment(0xbd59, 'Packed byte 0 = exponent', align=Align.INLINE)
d.comment(0xbd5b, 'read it', align=Align.INLINE)
d.comment(0xbd5d, '(store)', align=Align.INLINE)
d.comment(0xbd5f, 'advance', align=Align.INLINE)
d.comment(0xbd60, 'Take the sign...', align=Align.INLINE)
d.comment(0xbd62, 'Pack: fold the sign into the mantissa MSB', align=Align.INLINE)
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

d.subroutine(
    0xbd7e, 'unstack_real',
    title='Pop a real off the BASIC stack',
    description="""Point zp_fp_ptr at the 5-byte real on top of the BASIC stack
and drop it (advance the stack pointer by 5), so an FP routine can
use the popped value as its (zp_fp_ptr) operand.
""",
    on_entry={'(zp_stack_ptr) (&04/&05)': 'a packed 5-byte real on top of stack'},
    on_exit={'zp_fp_ptr (&4B/&4C)': 'addresses the popped real',
             'zp_stack_ptr': 'advanced by 5 (real dropped)',
             'X': 'preserved', 'Y': 'preserved'},
)
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

# stack_value (&BD90): push the current value, choosing format by type
d.subroutine(0xbd90, 'stack_value', title='Push the current value by type',
             description="""Push the current value onto the BASIC stack in the form
matching its type: a string (stack_string), a real (stack_real) or,
falling through, an integer (stack_integer).""",
             on_entry={'A': 'value type: 0 string, negative real, else integer',
                       'zp_iwa / zp_fwa / string_work (&0600)':
                           'the value, selected by the type in A'},
             on_exit={'zp_stack_ptr (&04/&05)': 'lowered past the pushed value'})
d.comment(0xbd90, 'Type 0 (string): stack as a string', align=Align.INLINE)
d.comment(0xbd92, 'Negative (real): stack 5 bytes; else integer below',
          align=Align.INLINE)

d.subroutine(
    0xbd94, 'stack_integer',
    title='Push the integer accumulator onto the BASIC stack',
    description="""Reserve four bytes on the BASIC stack (zp_stack_ptr, &04) and
copy the integer accumulator (zp_iwa) onto it. Errors if the stack
would collide with the heap.
""",
    on_entry={'zp_iwa (&2A-&2D)': 'the integer to push'},
    on_exit={'zp_stack_ptr (&04/&05)': 'lowered by 4 (integer pushed)'},
)
# stack_integer (&BD94): push the 4-byte IWA, MSB first
d.comment(0xbd94, 'From the stack top...', align=Align.INLINE)
d.comment(0xbd96, 'prepare subtraction', align=Align.INLINE)
# --- BASIC value-stack push/pop primitives ---------------------------
d.comment(0xbd97, 'Lower the stack by 4 bytes (an integer)', align=Align.INLINE)
d.comment(0xbd99, 'reserve the space (check for room)', align=Align.INLINE)
d.comment(0xbd9c, 'Copy IWA, MSB first: byte 3', align=Align.INLINE)
d.comment(0xbd9e, 'read it', align=Align.INLINE)
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

d.subroutine(
    0xbdb2, 'stack_string',
    title='Push the current string onto the BASIC stack',
    description="""Copy the string from the string buffer (length zp_strbuf_len,
&36; text at &0600) onto the BASIC stack, length last. Errors if the
stack meets the heap.
""",
    on_entry={'string_work (&0600)': 'the string characters',
              'zp_strbuf_len (&36)': 'the string length'},
    on_exit={'zp_stack_ptr (&04/&05)': 'lowered by length+1 (string pushed)'},
)
# stack_string (&BDB2) / unstack_string (&BDCB)
d.comment(0xbdb2, 'From the stack top...', align=Align.INLINE)
d.comment(0xbdb3, 'low...', align=Align.INLINE)
d.comment(0xbdb5, 'Lower the stack by length+1 bytes (carry clear)',
          align=Align.INLINE)

d.comment(0xbdb7, 'reserve the space', align=Align.INLINE)
d.comment(0xbdba, 'string length', align=Align.INLINE)
d.comment(0xbdbc, 'zero length: just push the length', align=Align.INLINE)
d.comment(0xbdbe, 'Copy the string from the buffer (&0600): char Y', align=Align.INLINE)
d.label(0xbdbe, 'ss_copy_loop')
d.comment(0xbdc1, '(onto the stack)', align=Align.INLINE)
d.comment(0xbdc3, 'next', align=Align.INLINE)
d.comment(0xbdc4, 'loop', align=Align.INLINE)
d.comment(0xbdc6, 'Push the length last', align=Align.INLINE)
d.label(0xbdc6, 'ss_push_length')
d.comment(0xbdc8, '(store)', align=Align.INLINE)
d.comment(0xbdca, 'String pushed', align=Align.INLINE)
# ======================================================================
# DEPTH 1 routines
# ======================================================================

d.subroutine(0xbdcb, 'unstack_string', title='Pop a string off the BASIC stack',
             description='Copy the length-prefixed string on top of the stack '
                         'into the string buffer and drop it (advance the stack '
                         'pointer past the length byte and the characters).',
             on_entry={'(zp_stack_ptr) (&04/&05)':
                           'a length-prefixed string on top of stack'},
             on_exit={'string_work (&0600)': 'the popped string characters',
                      'zp_strbuf_len (&36)': 'the string length',
                      'zp_stack_ptr': 'advanced past the string',
                      'X': 'preserved'})
d.comment(0xbdcb, 'Pop a string: read its length', align=Align.INLINE)
d.comment(0xbdcd, 'read it', align=Align.INLINE)
d.comment(0xbdcf, '(store)', align=Align.INLINE)
d.comment(0xbdd1, 'zero length: just drop the length', align=Align.INLINE)
d.comment(0xbdd3, 'Y = length', align=Align.INLINE)
d.comment(0xbdd4, 'Copy the string to the buffer: char Y', align=Align.INLINE)
d.label(0xbdd4, 'us_copy_loop')
d.comment(0xbdd6, '(into the buffer)', align=Align.INLINE)
d.comment(0xbdd9, 'next', align=Align.INLINE)
d.comment(0xbdda, 'loop', align=Align.INLINE)
d.comment(0xbddc, 'Drop the string: get its length', align=Align.INLINE)
d.subroutine(
    0xbddc, 'drop_stacked_string',
    title='Drop a string off the BASIC stack',
    description="""Read the length byte of the length-prefixed string on top of the BASIC
stack and advance the stack pointer past both the length byte and the
string characters, discarding the string without copying it.
""",
    on_entry={
        'zp_stack_ptr (&04)': 'a length-prefixed string on top of the BASIC stack (&04/&05)',
    },
    on_exit={
        'zp_stack_ptr (&04)': 'advanced past the length byte and characters (string dropped)',
        'X': 'preserved',
    },
)
d.comment(0xbdde, 'read it', align=Align.INLINE)
d.comment(0xbde0, 'so the +1 covers the length byte', align=Align.INLINE)
d.comment(0xbde1, 'advance the stack pointer past it: low', align=Align.INLINE)
d.label(0xbde1, 'drop_string_adv')
d.comment(0xbde3, '(store)', align=Align.INLINE)
d.comment(0xbde5, 'done', align=Align.INLINE)
d.comment(0xbde7, 'carry into high', align=Align.INLINE)
d.comment(0xbde9, 'Return', align=Align.INLINE)

d.subroutine(
    0xbdea, 'unstack_integer',
    title='Pop an integer from the BASIC stack',
    description="""Copy the four-byte integer on top of the BASIC stack into the
integer accumulator (zp_iwa), then fall into drop_stack_integer to
advance the stack pointer past it.
""",
    on_entry={'(zp_stack_ptr) (&04/&05)':
                  'a 4-byte integer (MSB first) on top of stack'},
    on_exit={'zp_iwa (&2A-&2D)': 'the popped integer',
             'zp_stack_ptr': 'advanced by 4 (integer dropped)',
             'X': 'preserved'},
)

# unstack_integer (&BDEA): pop a 4-byte integer into IWA, then drop it
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
d.comment(0xbdfd, '...into IWA, then fall into drop_stack_integer', align=Align.INLINE)

# drop_stack_integer (&BDFF): advance the stack pointer past a 4-byte int
d.subroutine(0xbdff, 'drop_stack_integer', title='Drop an integer off the stack',
             description='Advance the BASIC stack pointer by four bytes.',
             on_entry={'zp_stack_ptr (&04/&05)': 'the BASIC stack pointer'},
             on_exit={'zp_stack_ptr': 'advanced by 4',
                      'X': 'preserved', 'Y': 'preserved'})
d.comment(0xbdff, 'Prepare to add', align=Align.INLINE)
d.comment(0xbe00, 'Drop four bytes: stack pointer...', align=Align.INLINE)
d.comment(0xbe02, '...+ 4', align=Align.INLINE)
d.comment(0xbe04, '(store)', align=Align.INLINE)
d.comment(0xbe06, 'No carry: done', align=Align.INLINE)
d.comment(0xbe08, 'Carry into the high byte', align=Align.INLINE)
d.comment(0xbe0a, 'Return (shared)', align=Align.INLINE)

d.subroutine(
    0xbe0b, 'unstack_int_to_general',
    title='Pop a stacked integer into the general work area',
    description="""Set the destination to zp_general (&37) and fall into
unstack_int_to_zp, which copies the 4-byte integer on top of the BASIC
stack to (&37..&3A) and drops it from the stack.
""",
    on_entry={
        'zp_stack_ptr (&04)': 'a 4-byte integer (MSB first) on top of the BASIC stack (&04/&05)',
    },
    on_exit={
        'zp_general (&37)': 'the popped integer (&37-&3A)',
        'zp_stack_ptr (&04)': 'advanced by 4 (integer dropped)',
        'X': 'preserved (= &37)',
    },
)
d.comment(0xbe0b, 'Default destination: zp_general (&37)', align=Align.INLINE)
# unstack_int_to_zp (&BE0D): pop the stacked integer into 4 zp bytes at X
d.subroutine(0xbe0d, 'unstack_int_to_zp',
             title='Pop a stacked integer into a zero-page variable',
             description="""Copy the four-byte integer on top of the BASIC stack into
the zero-page bytes at (X .. X+3), then drop it from the stack. The
&BE0B entry uses X = &37 (the general work area).""",
             on_entry={'X': 'the destination zero-page offset (from &00)',
                       '(zp_stack_ptr) (&04/&05)': 'a 4-byte integer on top of stack'},
             on_exit={'(&00+X .. +3)': 'the popped integer',
                      'zp_stack_ptr': 'advanced by 4 (integer dropped)',
                      'X': 'preserved'})
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
# reserve_stack (&BE2E) remaining: collision check against the heap top
d.comment(0xbe2e, 'Set the new stack-pointer low byte', align=Align.INLINE)
d.comment(0xbe30, 'No borrow: high byte unchanged', align=Align.INLINE)
d.comment(0xbe32, 'Borrow: decrement the high byte', align=Align.INLINE)
d.comment(0xbe34, 'New stack-pointer high byte', align=Align.INLINE)
d.label(0xbe34, 'rs_set_high')
d.comment(0xbe36, 'Compare the new top against the heap top', align=Align.INLINE)
d.comment(0xbe38, 'New top below the heap page: No room', align=Align.INLINE)
d.comment(0xbe3a, 'Clearly above the heap: room available', align=Align.INLINE)
d.comment(0xbe3c, 'Same page: compare the low bytes', align=Align.INLINE)
d.comment(0xbe3e, 'Below the heap top: No room', align=Align.INLINE)
d.comment(0xbe40, 'Room available: return', align=Align.INLINE)

d.comment(0xbe41, 'Stack meets heap: No room', align=Align.INLINE)

d.label(0xbe41, 'stack_no_room')
d.subroutine(
    0xbe44, 'iwa_store_zp',
    title='Store the accumulator into a zero-page integer variable',
    description='Copy IWA into the 4-byte resident integer variable at &00+X '
                '(the inverse of iwa_load_zp).',
    on_entry={'zp_iwa (&2A-&2D)': 'the integer to store',
              'X': 'zero-page offset of the destination (from &00)'},
    on_exit={'(&00+X .. +3)': 'a copy of IWA',
             'X': 'preserved', 'Y': 'preserved'},
)

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
d.label(0xbe55, 'fwb_scale_clc')
d.comment(0xbe56, 'A = the amount (Y)', align=Align.INLINE)
d.label(0xbe56, 'fwb_scale')
d.comment(0xbe57, 'add it to the FWB exponent', align=Align.INLINE)
d.comment(0xbe59, '(store)', align=Align.INLINE)
d.comment(0xbe5b, 'no carry: done', align=Align.INLINE)
d.comment(0xbe5d, 'carry into the mantissa MSB', align=Align.INLINE)
d.comment(0xbe5f, 'Y = 1', align=Align.INLINE)
d.label(0xbe5f, 'fwb_scale_done')
d.comment(0xbe61, 'Return', align=Align.INLINE)

d.subroutine(0xbe62, 'load_program', title='Load a program from the filing system',
             description="""Set the OSFILE load address to PAGE and call OSFILE &FF
to read the named BASIC program into memory. Used by LOAD and CHAIN.

LOAD/SAVE drive OSFILE through an 18-byte control block in zero page,
pointed at by XY = &0037. Each address field is 4 bytes (the BBC's
32-bit address space; the high words come from OSBYTE &82):

| Addr    | Field            |
|---------|------------------|
| &37-&38 | filename pointer |
| &39-&3C | load address     |
| &3D-&40 | exec address     |
| &41-&44 | start address    |
| &45-&48 | end address      |

This routine fills only the filename pointer, the load address (PAGE),
and exec = 0 (so OSFILE &FF loads to the block's load address rather
than the file's own). [`stmt_save`](address:bef3) fills all four
address fields and calls OSFILE &00.
""",
             on_entry={'the filename block': 'set up for OSFILE (control block at &37)',
                       'zp_page (&18)': 'PAGE, where the program loads'},
             on_exit={'memory from PAGE': 'the loaded program'})
# load_program (&BE62)
d.comment(0xbe62, 'Set the OSFILE load address to PAGE', align=Align.INLINE)
d.comment(0xbe65, 'Y = 0 (for the exec address)', align=Align.INLINE)
d.comment(0xbe66, 'OSFILE &FF: load the named file', align=Align.INLINE)
d.comment(0xbe68, 'exec address = 0 (load to the given address)', align=Align.INLINE)
d.comment(0xbe6a, 'control block at &37', align=Align.INLINE)
d.subroutine(0xbe6f, 'check_program', title='Validate the program and set TOP',
             description='Walk the lines from PAGE checking each is well-formed '
                         '(CR-terminated, non-zero length), and set TOP past the '
                         'end. Raises "Bad program" if a line is malformed.',
             on_entry={'zp_page (&18)': 'PAGE, the start of the program'},
             on_exit={'zp_top (&12/&13)': 'TOP, just past the last line',
                      'BRK': 'Bad program if a line is malformed'})

d.comment(0xbe6f, 'Set TOP = PAGE: high', align=Align.INLINE)
d.comment(0xbe71, '(TOP high)', align=Align.INLINE)
d.comment(0xbe73, 'low 0', align=Align.INLINE)
d.comment(0xbe75, '(store)', align=Align.INLINE)
d.comment(0xbe77, 'Y = 1', align=Align.INLINE)
d.comment(0xbe78, 'step back to the byte before the line', align=Align.INLINE)
d.label(0xbe78, 'chkprog_loop')
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
d.label(0xbe90, 'chkprog_end')
d.comment(0xbe91, 'clear carry for TOP += Y', align=Align.INLINE)
d.comment(0xbe92, 'TOP += Y', align=Align.INLINE)
d.label(0xbe92, 'add_y_to_top')
d.comment(0xbe93, 'add: low', align=Align.INLINE)
d.label(0xbe93, 'add_y_to_top_lo')
d.comment(0xbe95, '(store)', align=Align.INLINE)
d.comment(0xbe97, 'no carry', align=Align.INLINE)
d.comment(0xbe99, 'carry into high', align=Align.INLINE)
d.comment(0xbe9b, 'return Y=1 (NE)', align=Align.INLINE)
d.label(0xbe9b, 'chkprog_ok')
d.comment(0xbe9d, 'Return', align=Align.INLINE)
d.comment(0xbe9e, 'Bad program: print the message', align=Align.INLINE)
d.label(0xbe9e, 'bad_program')
d.comment(0xbeae, '(string terminator)', align=Align.INLINE)
d.comment(0xbeaf, 'back to the immediate loop', align=Align.INLINE)
d.comment(0xbeb2, 'Point the general pointer at the string buffer: low', align=Align.INLINE)
d.label(0xbeb2, 'point_strbuf_lo')
d.comment(0xbeb4, '(store)', align=Align.INLINE)
d.comment(0xbeb6, 'high (&06)', align=Align.INLINE)
d.comment(0xbeb8, '(store)', align=Align.INLINE)
d.comment(0xbeba, 'Terminate the string buffer with a CR:', align=Align.INLINE)
d.subroutine(
    0xbeba, 'terminate_strbuf',
    title='Terminate the string buffer with a CR',
    description="""Write a carriage return (&0D) into string_work (&0600) at the offset
given by zp_strbuf_len, marking the end of the string buffer. Reached
both by fall-through from point_strbuf_lo and by jsr from
assign_str_addr and &BF88.
""",
    on_entry={
        'zp_strbuf_len (&36)': 'the current string length (offset of the terminator)',
    },
    on_exit={
        'string_work (&0600)': 'the buffer, terminated with a CR at offset zp_strbuf_len',
        'Y': 'the string length',
        'A': '&0D',
    },
)
d.comment(0xbebc, 'CR', align=Align.INLINE)
d.comment(0xbebe, 'at the end of the buffer', align=Align.INLINE)
d.comment(0xbec1, 'Return', align=Align.INLINE)

# stmt_oscli (&BEC2) + sub_cbed2 / sub_cbedd / sub_cbee7
d.comment(0xbec2, 'Evaluate the command string, CR-terminate it', align=Align.INLINE)
d.comment(0xbec5, 'XY -> the string (&0600): low', align=Align.INLINE)
d.comment(0xbec7, 'high byte &06', align=Align.INLINE)
d.comment(0xbec9, 'Pass it to OSCLI', align=Align.INLINE)
d.comment(0xbecc, 'Back to execution', align=Align.INLINE)
d.comment(0xbecf, 'not a string: Type mismatch', align=Align.INLINE)
d.label(0xbecf, 'oscli_type_error')
d.comment(0xbed2, 'Evaluate the expression', align=Align.INLINE)
d.subroutine(
    0xbed2, 'eval_string_arg',
    title='Evaluate a string argument and CR-terminate it',
    description="""Evaluate an expression via eval_expr, require it to be a string (Type
mismatch otherwise), CR-terminate it in the string buffer, and check
that the statement ends. Used by OSCLI-style commands and
eval_filename to fetch a single string argument.
""",
    on_entry={
        'zp_text_ptr (&0B/&0C)': 'PtrA at the string expression',
        'zp_text_ptr_off (&0A)': 'offset just past the keyword',
    },
    on_exit={
        'string_work (&0600)': 'the string, terminated with a carriage return',
        'zp_strbuf_len (&36)': 'the string length',
    },
)
d.comment(0xbed5, 'not a string: error', align=Align.INLINE)
d.comment(0xbed7, 'CR-terminate the string buffer', align=Align.INLINE)
d.comment(0xbeda, 'Check for end of statement', align=Align.INLINE)
d.comment(0xbedd, 'Evaluate the filename, CR-terminate', align=Align.INLINE)
d.subroutine(
    0xbedd, 'eval_filename',
    title='Evaluate a filename and build the OSFILE load address',
    description="""Evaluate a CR-terminated filename string via eval_string_arg, then set
the load address to PAGE (low byte 0, high byte PAGE) and read the
machine's high-order address word via OSBYTE &82. Shared setup for
SAVE/LOAD/CHAIN.
""",
    on_entry={
        'zp_text_ptr (&0B/&0C)': 'PtrA at the filename expression',
        'zp_text_ptr_off (&0A)': 'offset just past the keyword',
    },
    on_exit={
        'string_work (&0600)': 'the CR-terminated filename',
        'zp_fileblk (&39)': 'load address low = 0',
        'zp_fileblk_1 (&3A)': 'load address high = PAGE',
        'zp_fwb_sign (&3B)': 'high-order address low (X from OSBYTE &82)',
        'zp_fwb_ovf (&3C)': 'high-order address high (Y from OSBYTE &82)',
        'A': 'zero',
    },
)
d.comment(0xbee0, 'Y = 0 for the low byte', align=Align.INLINE)
d.comment(0xbee1, 'LOAD address low = 0', align=Align.INLINE)
d.comment(0xbee3, 'LOAD address high = PAGE', align=Align.INLINE)
d.comment(0xbee5, '(store)', align=Align.INLINE)
d.comment(0xbee7, 'OSBYTE &82: read the high-order address', align=Align.INLINE)
d.label(0xbee7, 'read_himem_byte')
d.comment(0xbeec, 'set the LOAD high word', align=Align.INLINE)
d.comment(0xbeee, 'high word: X and Y', align=Align.INLINE)
d.comment(0xbef0, 'A = 0', align=Align.INLINE)
d.comment(0xbef2, 'Return', align=Align.INLINE)

# stmt_save (&BEF3): SAVE - build an OSFILE block and save the program.
d.comment(0xbef3, 'Check the program, set TOP', align=Align.INLINE)
d.comment(0xbef6, 'End address = TOP', align=Align.INLINE)
d.comment(0xbef8, 'low byte to &45,', align=Align.INLINE)
d.comment(0xbefa, 'high byte,', align=Align.INLINE)
d.comment(0xbefc, 'to &46', align=Align.INLINE)
d.comment(0xbefe, 'Exec address = language startup', align=Align.INLINE)
d.comment(0xbf00, 'low byte &23 to &3D,', align=Align.INLINE)
d.comment(0xbf02, 'high byte &80,', align=Align.INLINE)
d.comment(0xbf04, 'to &3E (exec &8023)', align=Align.INLINE)
d.comment(0xbf06, 'Start address = PAGE', align=Align.INLINE)
d.comment(0xbf08, 'PAGE to &42', align=Align.INLINE)
d.comment(0xbf0a, 'Read the machine high address words', align=Align.INLINE)
d.comment(0xbf0d, 'Fill the address high words', align=Align.INLINE)
d.comment(0xbf0f, '&40,', align=Align.INLINE)
d.comment(0xbf11, '&43,', align=Align.INLINE)
d.comment(0xbf13, '&44,', align=Align.INLINE)
d.comment(0xbf15, '&47,', align=Align.INLINE)
d.comment(0xbf17, '&48', align=Align.INLINE)
d.comment(0xbf19, 'Load address low = PAGE', align=Align.INLINE)
d.comment(0xbf1b, 'into Y too', align=Align.INLINE)
d.comment(0xbf1c, 'Point at the OSFILE block (&37)', align=Align.INLINE)
d.comment(0xbf1e, 'Save the file', align=Align.INLINE)
d.comment(0xbf21, 'next statement', align=Align.INLINE)

# stmt_load (&BF24) / stmt_chain (&BF2A)
d.comment(0xbf24, 'Load the named program', align=Align.INLINE)
d.comment(0xbf27, 'Back to the immediate loop', align=Align.INLINE)
d.comment(0xbf2a, 'Load the named program', align=Align.INLINE)
d.comment(0xbf2d, 'then RUN it', align=Align.INLINE)

# stmt_ptr (&BF30): PTR#n = value -> OSARGS.
d.comment(0xbf30, 'Evaluate the #handle', align=Align.INLINE)
d.comment(0xbf33, 'save it', align=Align.INLINE)
d.comment(0xbf34, 'Expect "=" and evaluate', align=Align.INLINE)
d.comment(0xbf37, 'coerce to integer', align=Align.INLINE)
d.comment(0xbf3a, 'Recover the handle', align=Align.INLINE)
d.comment(0xbf3b, 'Y = the handle', align=Align.INLINE)
d.comment(0xbf3c, 'Point at the value', align=Align.INLINE)
d.comment(0xbf3e, 'Write the file pointer', align=Align.INLINE)
d.comment(0xbf43, 'next statement', align=Align.INLINE)

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

# fn_bget (&BF6F): BGET#channel
d.comment(0xbf6f, 'Evaluate the #handle', align=Align.INLINE)
d.comment(0xbf72, 'OSBGET: read a byte from the channel', align=Align.INLINE)
d.comment(0xbf75, 'Return the byte as an integer', align=Align.INLINE)

# fn_openin (&BF78) / fn_openout (&BF7C): OSFIND open
d.comment(0xbf78, 'OSFIND &40: open an existing file for input', align=Align.INLINE)
d.comment(0xbf7a, 'do the open', align=Align.INLINE)
d.comment(0xbf7c, 'OSFIND &80: create a file for output', align=Align.INLINE)
d.comment(0xbf7e, 'do the open', align=Align.INLINE)

# fn_openup (&BF80): OPENIN/OPENOUT/OPENUP -> OSFIND.
d.comment(0xbf80, 'OPENUP action &C0', align=Align.INLINE)
d.comment(0xbf82, 'Save the action', align=Align.INLINE)
d.label(0xbf82, 'openup_action')
d.comment(0xbf83, 'Evaluate the filename', align=Align.INLINE)
d.comment(0xbf86, 'not a string: error', align=Align.INLINE)
d.comment(0xbf88, 'CR-terminate it', align=Align.INLINE)
d.comment(0xbf8b, 'Point at the string buffer', align=Align.INLINE)
d.comment(0xbf8d, 'high byte = &06 (&0600)', align=Align.INLINE)
d.comment(0xbf8f, 'recover the action', align=Align.INLINE)
d.comment(0xbf90, 'Open the file', align=Align.INLINE)
d.comment(0xbf93, 'return the handle', align=Align.INLINE)
d.comment(0xbf96, 'Type mismatch error', align=Align.INLINE)

d.label(0xbf96, 'openup_type_error')
# stmt_close (&BF99) + sub_cbfa9 (set PtrB = PtrA)
d.comment(0xbf99, 'Evaluate the #handle', align=Align.INLINE)
d.comment(0xbf9c, 'Check for end of statement', align=Align.INLINE)
d.comment(0xbf9f, 'Y = the handle', align=Align.INLINE)
d.comment(0xbfa1, 'OSFIND &00: close the file', align=Align.INLINE)
d.comment(0xbfa6, 'Back to execution', align=Align.INLINE)
d.comment(0xbfa9, 'Set PtrB = PtrA: offset', align=Align.INLINE)
d.subroutine(
    0xbfa9, 'sync_ptrb_from_ptra',
    title='Copy PtrA to PtrB, then evaluate a #channel',
    description="""Copy the three fields of the primary text pointer PtrA (offset &0A,
low &0B, high &0C) into the secondary pointer PtrB (offset &1B, low
&19, high &1A), then fall straight through into eval_channel. In
effect: rewind PtrB to PtrA's position and parse the '#channel' file
handle that follows.
""",
    on_entry={
        'zp_text_ptr_off (&0A)': 'PtrA offset',
        'zp_text_ptr (&0B)': 'PtrA pointer low/high (&0B/&0C)',
    },
    on_exit={
        'zp_text_ptr2 (&19)': 'PtrB set equal to PtrA (offset &1B, low &19, high &1A)',
        'control': 'falls through to eval_channel, returning with zp_iwa (&2A) = channel handle, or BRK Missing #',
    },
)
d.comment(0xbfab, '(store)', align=Align.INLINE)
d.comment(0xbfad, 'low', align=Align.INLINE)
d.comment(0xbfaf, '(store)', align=Align.INLINE)
d.comment(0xbfb1, 'high', align=Align.INLINE)
d.comment(0xbfb3, '(store)', align=Align.INLINE)

d.subroutine(0xbfb5, 'eval_channel', title='Evaluate a #channel argument',
             description="""Require "#" at PtrB then evaluate the file handle as an
integer, leaving it in IWA. Raises Missing # if the "#" is absent.

The shared entry point for the channel-based file words. BBC BASIC's
file vocabulary maps onto five MOS calls; the handle is passed in Y
(except OSFILE), and OSARGS reads/writes its 4-byte value through
X -> IWA (&2A):

| BASIC          | MOS call | A   |
|----------------|----------|-----|
| OPENIN f$      | OSFIND   | &40 |
| OPENOUT f$     | OSFIND   | &80 |
| OPENUP f$      | OSFIND   | &C0 |
| CLOSE #h       | OSFIND   | &00 |
| =PTR# h        | OSARGS   | &00 |
| PTR# h =       | OSARGS   | &01 |
| =EXT# h        | OSARGS   | &02 |
| =BGET# h       | OSBGET   | -   |
| BPUT# h, b     | OSBPUT   | -   |
| LOAD / CHAIN   | OSFILE   | &FF |
| SAVE           | OSFILE   | &00 |

OSFIND returns the new handle in A (0 = open failed); CLOSE #0 closes
every open file. OSFILE uses the control block at &37 (see
[`load_program`](address:be62)), not a handle.
""",
             on_entry={'zp_text_ptr2 (&19/&1A)': 'PtrB before the "#channel"'},
             on_exit={'zp_iwa (&2A-&2D)': 'the channel handle',
                      'A': 'the handle low byte', 'Y': 'the handle low byte',
                      'BRK': 'Missing # if "#" is absent'})
# eval_channel (&BFB5) remaining
d.comment(0xbfb5, 'Skip spaces', align=Align.INLINE)
d.comment(0xbfb8, 'Require "#"', align=Align.INLINE)
d.char_literal(0xbfb9)
d.comment(0xbfba, 'missing: error', align=Align.INLINE)
d.comment(0xbfbc, 'Evaluate the handle as an integer', align=Align.INLINE)
d.comment(0xbfbf, 'Y = the handle', align=Align.INLINE)
d.comment(0xbfc1, 'A = the handle too', align=Align.INLINE)
d.comment(0xbfc2, 'Return', align=Align.INLINE)
d.comment(0xbfc3, 'BRK error block ("Missing #")', align=Align.INLINE)

d.label(0xbfc3, 'missing_hash')
# print_inline_string (&BFCF): print the bit-7-terminated string that
# follows the JSR, then resume at the terminator byte (an opcode).
d.banner(
    0xbfcf,
    title='Print an inline string following the call',
    description="""Print the string embedded in the code immediately after the JSR to
this routine. It pulls the return address into zp_general as a text
pointer, then walks forward with general_next_byte printing each byte
through osasci, stopping at the first byte with bit 7 set. It resumes
execution at that terminating byte via jmp (zp_general) - so the
terminator doubles as the opcode of the continuation.
""",
    on_exit={
        'control': 'resumes at the string terminator (the byte after the string) as the next instruction; A, Y and zp_general (&37/&38) are corrupted',
    },
)
d.hook_subroutine(0xbfcf, 'print_inline_string', stringhi_hook)
d.comment(0xbfcf, 'Pull the return address: it points at the string',
          align=Align.INLINE)
d.comment(0xbfd0, '(low)', align=Align.INLINE)
d.comment(0xbfd2, '(pull high)', align=Align.INLINE)
d.comment(0xbfd3, '(high)', align=Align.INLINE)
d.comment(0xbfd5, 'Start before the first character', align=Align.INLINE)
d.comment(0xbfd7, 'jump in to fetch it', align=Align.INLINE)
d.comment(0xbfd9, 'Print the character', align=Align.INLINE)
d.label(0xbfd9, 'print_msg_loop')
d.comment(0xbfdc, 'Advance and fetch the next character', align=Align.INLINE)
d.label(0xbfdc, 'print_msg_next')
d.comment(0xbfdf, 'Loop while bit 7 is clear', align=Align.INLINE)
d.comment(0xbfe1, 'Resume at the terminator (the next instruction)',
          align=Align.INLINE)

# stmt_report (&BFE4): REPORT - print the last error message.
d.comment(0xbfe4, 'Check the statement ends', align=Align.INLINE)
d.comment(0xbfe7, 'Newline', align=Align.INLINE)
d.comment(0xbfea, 'From offset 1', align=Align.INLINE)
d.comment(0xbfec, 'Error message byte', align=Align.INLINE)
d.label(0xbfec, 'report_loop')
d.comment(0xbfee, 'terminator: done', align=Align.INLINE)
d.comment(0xbff0, 'print it', align=Align.INLINE)
d.comment(0xbff3, 'next', align=Align.INLINE)
d.comment(0xbff4, 'loop', align=Align.INLINE)
d.comment(0xbff6, 'next statement', align=Align.INLINE)























d.label(0xbff6, 'report_done')



ir = d.disassemble()
output = str(
    ir.render(
        'beebasm',
        include_build_instructions=True,
        listing_filename='basic-2.asm',
        build_output_name='basic-2.rom',
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

tass_output = str(
    ir.render(
        '64tass',
        include_build_instructions=True,
        listing_filename='basic-2.s',
        build_output_name='basic-2.rom',
        byte_column=True,
        default_byte_cols=12,
        default_word_cols=6,
    )
)
tass_filepath = _output_dirpath / 'basic-2.s'
tass_filepath.write_text(tass_output, encoding='utf-8')
print(f'Wrote {tass_filepath}', file=sys.stderr)
json_filepath = _output_dirpath / 'basic-2.json'
json_filepath.write_text(str(ir.render('json')), encoding='utf-8')
print(f'Wrote {json_filepath}', file=sys.stderr)
