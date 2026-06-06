# 6502 instruction set

6502 instruction set

                 INSTRUCTIONS                IMMEDIATE     ABSOLUTE    ZERO PAGE         ACCUM            IMPLIED            (IND,X)            (IND),Y        Z PAGE,X            ABS,X            ABS,Y        RELATIVE        INDIRECT        Z PAGE,Y       PROCESSOR STATUS CODES

      MNEMONIC   OPERATOR                    OP   n   #   OP   n   #   OP   n   #   OP     n     #   OP     n       #   OP     n       #   OP     n       #   OP   n      #   OP    n      #   OP    n      #   OP   n      #   OP   n      #   OP   n      #   N   V   •   B   D   I   Z   C   MNEM.

      ADC        A+M+C®A           (4) (1)   69   2   2   6D   4   3   65   3   2                                       61     6       2   71     5       2   75   4      2   7D     4     3   79     4     3                                                   N   V   •   •   •   •   Z   C   ADC

      AND        AÙM®A                (1)    29   2   2   2D   4   3   25   3   2                                       21     6       2   31     5       2   35   4      2   3D     4     3   39     4     3                                                   N   •   •   •   •   •   Z   •   AND

      ASL        C¬7        0¬0                           0E   6   3   06   5   2   0A     2     1                                                            16   6      2   1E     7     3                                                                    N   •   •   •   •   •   Z   C   ASL
      BCC        BRANCH ON C=0        (2)                                                                                                                                                                       90   2      2                                   •   •   •   •   •   •   •   •   BCC

      BCS        BRANCH ON C=1        (2)                                                                                                                                                                       B0   2      2                                   •   •   •   •   •   •   •   •   BCS

      BEQ        BRANCH ON Z=1        (2)                                                                                                                                                                       F0   2      2                                   •   •   •   •   •   •   •   •   BEQ

      BIT        AÙM                                      2C   4   3   24   3   2                                                                                                                                                                               M7 M6 •     •   •   •   Z   •   BIT
      BMI        BRANCH ON N=1        (2)                                                                                                                                                                       30   2      2                                   •   •   •   •   •   •   •   •   BMI

      BNE        BRANCH ON Z=0        (2)                                                                                                                                                                       D0   2      2                                   •   •   •   •   •   •   •   •   BNE

      BPL        BRANCH ON N=0        (2)                                                                                                                                                                       10   2      2                                   •   •   •   •   •   •   •   •   BPL

      BRK        BREAK                                                                               00      7      1                                                                                                                                           •   •   •   1   •   1   •   •   BRK

      BVC        BRANCH ON V=0        (2)                                                                                                                                                                       50   2      2                                   •   •   •   •   •   •   •   •   BVC

508
      BVS        BRANCH ON V=1        (2)                                                                                                                                                                       70   2      2                                   •   •   •   •   •   •   •   •   BVS

      CLC        0®C                                                                                 18      2      1                                                                                                                                           •   •   •   •   •   •   •   0   CLC

      CLD        0®D                                                                                 D8      2      1                                                                                                                                           •   •   •   •   0   •   •   •   CLD

      CLI        0®I                                                                                 58      2      1                                                                                                                                           •   •   •   •   •   0   •   •   CLI

      CLV        0®V                                                                                 B8      2      1                                                                                                                                           •   0   •   •   •   •   •   •   CLV
      CMP        A–M                         C9   2   2   CD   4   3   C5   3   2                                       C1     6       2   D1     5       2   D5   4      2   DD     4     3                                                                    N   •   •   •   •   •   Z   C   CMP

      CPX        X–M                         E0   2   2   EC   4   3   E4   3   2                                                                                                                                                                               N   •   •   •   •   •   Z   C   CPX

      CPY        Y–M                         C0   2   2   CC   4   3   C4   3   2                                                                                                                                                                               N   •   •   •   •   •   Z   C   CPY

      DEC        M–1®M                                    CE   6   3   C6   5   2                                                          D6     6       2   DE   7      1                                                                                     N   •   •   •   •   •   Z   •   DEC

      DEX        X–1®X                                                                               CA      2      1                                                                                                                                           N   •   •   •   •   •   Z   •   DEX

      DEY        Y–1®Y                                                                               88      2      1                                                                                                                                           N   •   •   •   •   •   Z   •   DEY

      EOR        AÅM®A                (1)    49   2   2   4D   4   3   45   3   2                                       41     6       2   51     5       2   55   4      2   5D     4     3   59     4     3                                                   N   •   •   •   •   •   Z   •   EOR

      INC        M+1®M                                    EE   6   3   E6   5   2                                                                             F6   6      2   FE     7     3                                                                    N   •   •   •   •   •   Z   •   INC

      INX        X+1®X                                                                               E8      2      1                                                                                                                                           N   •   •   •   •   •   Z   •   INX

      INY        Y+1®Y                                                                               C8      2      1                                                                                                                                           N   •   •   •   •   •   Z   •   INY
      JMP        JUMP TO NEW LOC                          4C   3   3                                                                                                                                                            8C   5      3                   •   •   •   •   •   •   •   •   JMP

      JSR        JUMP SUB                                 20   6   3                                                                                                                                                                                            •   •   •   •   •   •   •   •   JSR

      LDA        M®A                  (1)    A9   2   2   AD   4   3   A5   3   2                                       A1     6       2   B1     5       2   B5   4      2   BD     4     3   B9     4     3                                                   N   •   •   •   •   •   Z   •   LDA
      LDX   M®X                        (1)   A2   2   2   AE   4   3   A6   3   2                                                                                       BE   4   3              B6      4   2   N   •    •    •   •   •   Z   •   LDX

      LDY   M®Y                        (1)   A0   2   2   AC   4   3   A4   3   2                                                             B4   4   2   BC   4   3                           B6      4   2   N   •    •    •   •   •   Z   •   LDY

      LSR   0®7            0®C                            4E   6   3   46   5   2   4A   2   1                                                56   6   2   5E   7   3                                           0   •    •    •   •   •   Z   C   LSR
      NOP   NO OPERATION                                                                         EA   2   1                                                                                                     •   •    •    •   •   •   •   •   NOP

      ORA   AÚM®A                            09   2   2   0D   4   3   05   3   2                             01   6   2       11    5   2    15   4   2   1D   4   3   19   4   3                              N   •    •    •   •   •   Z   •   ORA

      PHA   A ® Ms                S–1®S                                                          48   3   1                                                                                                     •   •    •    •   •   •   •   •   PHA

      PHP   P ® Ms                S–1®S                                                          08   3   1                                                                                                     •   •    •    •   •   •   •   •   PHP

      PLA   S+1®S                  Ms ® A                                                        68   4   1                                                                                                     N   •    •    •   •   •   Z   •   PLA

      PLP   S+1®S                  Ms ® P                                                        28   4   1                                                                                                              (RESTORED)               PLP

      ROL   C¬7            0¬C                            2E   6   3   26   5   2   2A   2   1                                                36   6   2   3E   7   3                                           N   •    •    •   •   •   Z   C   ROL

      ROR   C®7            0®C                            6E   6   3   66   5   2   6A   2   1                                                76   6   2   7E   7   3                                           N   •    •    •   •   •   Z   C   ROR
      RTI   RETURN INT                                                                           40   6   1                                                                                                              (RESTORED)               RTI

      RTS   RETURN SUB                                                                           60   6   1                                                                                                     •   •    •    •   •   •   •   •   RTS

      SBC   A–M–C®A                    (1)   E9   2   2   ED   4   3   E5   3   2                             E1   6   2       F1    5   2    F5   4   2   FD   4   3   F9   4   3                              N   V    •    •   •   •   Z (3)   SBC

      SEC   1®C                                                                                  36   2   1                                                                                                     •   •    •    •   •   •   •   1   SEC

      SED   1®D                                                                                  FB   2   1                                                                                                     •   •    •    •   1   •   •   •   SED

      SEI   1®I                                                                                  78   2   1                                                                                                     •   •    •    •   •   1   •   •   SEI

      STA   A®M                                           8D   4   3   85   3   2                             81   6   2       91    6   2    95   4   2   9D   5   3   99   5   3                              •   •    •    •   •   •   •   •   STA

      STX   X®M                                           8E   4   3   86   3   2                                                                                                                96     4   2   •   •    •    •   •   •   •   •   STX

      STY   Y®M                                           8C   4   3   84   3   2                                                             94   4   2                                                        •   •    •    •   •   •   •   •   STY

509
      TAX   A®X                                                                                  AA   2   1                                                                                                     N   •    •    •   •   •   Z   •   TAX

      TAY   A®Y                                                                                  AB   2   1                                                                                                     N   •    •    •   •   •   Z   •   TAY

      TSX   S®X                                                                                  BA   2   1                                                                                                     N   •    •    •   •   •   Z   •   TSX

      TXA   X®A                                                                                  8A   2   1                                                                                                     N   •    •    •   •   •   Z   •   TXA

      TXS   X®S                                                                                  9A   2   1                                                                                                     N   •    •    •   •   •   Z   •   TXS

      TYA   Y®A                                                                                  98   2   1                                                                                                     N   •    •    •   •   •   Z   •   TYA

                     (1)         ADD 1 to N” IF PAGE BOUNDARY IS CROSSED                                                   X        INDEX X                                          +   ADD                        M7       MEMORY BIT 7
                     (2)         ADD 1 TO N” IF BRANCH OCCURS TO SAME PAGE                                                 Y        INDEX Y                                          –   SUBTRACT                   M6       MEMORY BIT 6
                                 ADD 2 TO N” IF BRANCH OCCURS TO DIFFERENT PAGE
                                                                                                                           A        ACCUMULATOR                                      Ù   AND                        n        NO. CYCLES
                     (3)         CARRY NOT = BORROW
                                                                                                                           M        MEMORY PER EFFECTIVE ADDRESS                     Ú   OR                         #        NO. BYTES
                     (4)         IF IN DECIMAL MODE Z FLAG IS INVALID
                                 ACCUMULATOR MUST BE CHECKED FOR ZERO RESULT                                               Ms       MEMORY PER STACK POINTER                         Å   EXCLUSIVE OR
