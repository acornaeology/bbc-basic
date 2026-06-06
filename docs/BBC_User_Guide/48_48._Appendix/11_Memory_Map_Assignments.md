# Memory Map Assignments

Memory Map Assignments

FF00 - FFFF   Operating System rom
FE00 - FEFF   Internal memory mapped input/output
              (sheila)
FD00 - FDFF   External memory mapped input/output (jim)
FC00 - FCFF   External memory mapped input/output (fred)
C000 - FBFF   Operating System rom
8000 - BFFF   One or more languages roms (e.g.
              basic, pascal)
4000 - 7FFF   Optional ram on Model B
0000 - 3FFF   always ram
E00           Default setting of PAGE
D80 - DFF     allocated to machine operating system
D00 - D7F     Used by NMI routines (eg by Disc or Econet
              filing systems)
C00 - CFF     User defined character definitions
B00 - BFF     User defined function key definitions
A00 - AFF     RS423 receive, and cassette workspace
900 - 9FF     RS423 transmit, cassette, sound and speech
              workspace
800 - 8FF     Miscellaneous workspace
400 - 7FF     Language rom workspace
300 - 3FF     Miscellaneous workspace
200 - 2FF     Operating system workspace and
              indirection vectors
100 - 1FF     6502 stack
000 - 0FF     Zero page

Zero Page
FF            The top bit is set during an ESCAPE condition
FD - FE       Address following detected BRK instruction
FC            User IRQ routine save slot for register A
D0 to FB      allocated to machine operating system
B0 to CF      allocated to current filing system
90 to AF      allocated to machine operating system
70 to 8F      free for user routines
00 to 6F      basic language

                           502
