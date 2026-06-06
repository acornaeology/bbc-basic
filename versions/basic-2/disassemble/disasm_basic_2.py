"""dasmos driver for Acorn BBC BASIC II.

BBC BASIC II is a 16 kB sideways language ROM mapped at &8000-&BFFF
on the BBC Micro. This script drives dasmos to produce an annotated,
byte-faithful disassembly: the generated assembly reassembles with
beebasm to a byte-identical copy of the original ROM.

The driver is run by ``fantasm disassemble 2``, which sets FANTASM_ROM
and FANTASM_OUTPUT_DIR. When run standalone, it falls back to the
in-tree paths.
"""
import os
import sys
from pathlib import Path

import dasmos

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

# Seed the trace from the language and service entry points. BASIC's
# language entry is inline code (CMP #1 / BEQ ...), not a JMP abs, so
# the sideways-ROM environment cannot auto-seed it.
d.entry(0x8000)
d.entry(0x8003)

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
