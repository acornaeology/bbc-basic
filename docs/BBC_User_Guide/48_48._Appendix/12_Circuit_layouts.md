# Circuit layouts

0v               +5v
                                           R162
                           26              4K7

                BUSY                            74LS244
                 ACK                              IC70                    40
                                       18                                      CA1             23
                   D7                                          2           9         CS0                 VIAB (&FE60)
                                        3                                      PA7             24
                   D6                                          17          8         CS1                 2MHzE
                                       16                                      PA6
                   D5                                          4           7
                                        5                                      PA5            35
      PRINTER      D4                                          15          6           A3
                                       14                                      PA4            36
    CONNECTOR      D3                                          6           5           A2
                                        7                                      PA3            37
        PL9        D2                                          13          4           A1
                                       12                                      PA2            38
                   D1                                          8           3           A0
                                        9                                      PA1
                   D0                                          11          2
                                                                               PA0     D7     26
              STROBE                            1     19                          6522        27
                   0v             1                            0v         17
                                                                               PB7 IC69       28
                 PB7                                                      16                  29
                                                                               PB6
                 PB6                                                      15                  30
                                                                               PB5     D3
                 PB5                                                      14                  31
      USER                                                                     PB4     D2
                                                                                              32
  INPUT/OUTPUT PB4                                                        13
                                                                               PB3     D1
                                                                                              33
   CONNECTOR     PB3                                                      12           D0
                                                                               PB2            25
       PL10      PB2                                                      11                                 1MHzE
                                                                             PB1              22
                 PB1                                                      10                                 R/W
                                                                             PB0               21
                 PB0                                                      19                                 IRQ
                                                                             CB2               34
                 CB2                                                      18                                 RST
                                                                             CB1 CA2
                 CB1                                +5v
                  +5v                                          R170              39
                                                               2K2
                            4K7
                             R6

                                                                                                                     ADDRESS BUS
                                                S1         6          5

                                                                                                                                    DATA BUS
                                                                                   +5v
                                                                      4
                             Q11                               IC27
                            BC239                              7438

                                           0v

                                                                                    9            11             A7
                                                                                         74LS244
                                                                                    7      IC71  13
              AUDIO                                                                 5            15
             OUTPUT                                                                 3            17
               PL16                                                                18            2
                                                                                   16            4
                                      0v                                           14            6
                                           0v                                      12            8              A0
                   0v
                   A7
               A6 A5                                                                     1         19
               A4 A3                                                                                    0v
               A2 A1                                                                6            14                                D7
               A0 0v
                                                                                    7 74LS245 13
               D7 D6                                                                             12
                                                                                    8   IC72
               D5 D4                                                                             11
                                                                                    9
               D3 D2
                                                                                    4 A      B 16
  1MHz         D1 D0                                                                3            17
EXTENSION   ANALOG IN                                      ANALOG                                15
   BUS                                                                              5
                NRST                                       RST                                   18                                D0
   PL11                                                                             2
               NPGFD                                       JIM                        T/R CE
                                                           FRED                                     +5v
               NPGFC                                                                  1       19
                 NIRQ                                      IRQ                                      R108
                NNMI                                       NMI                                       3K3
               1MHzE                                       1MHzE
                R/NW                                                                                D         D15
                                  1        +5v                                                      14
                  +5v                                                                                        2x
                                                                                         R/W                 1N4148
                                                                                              FRED       JIM
                                                                                             &FC00       &FD00

Printer, User I/O and 1MHz Bus circuits

                                                                503
                                                       BLUE               68                  R111                  3        4             RGB
                                                      GREEN               68                  R113                       6
                                                                                                                2                5         CONNECTOR
                                                       RED                68                  R112                                         SK3
                                                                                                                    1

                                                                                                              +5v
                                                                      +5v                +5v
                                                                                                                             0v
                               2K2 1K                 3K9                                S31              9

                                                            1K R115

                                                                          68 R110
                                                                                                                             8
                                                                                       0v                10

                                               R116
                                 R117
                                        R118
                                                                                    R129                              IC48
                                                                                    68                               74LS86
                                                                                                                                            VIDEO
                                                                                                                                            OUT
                                                                              Q7 BC309                                                      (BNC)
                                          470                                                                                               SK2
                                                                                    CSYNC                                            0v
                                          R123
                                                                           0v             R140
                                                                                           1K

                                                                                    R141 2K7
                                                                      S39                                      +5v +5v
                                                                                                        R127
                                                               1K
                                                               R134                                     1K5

                                                                                                               UM1233                      TV
                                                                                                  C50           -E36                       SK 1
                                                             C58                    R126          47p
                                                            470p                     3K9

                                                                                        0v
Video outputs
                                                                                                                    0v

                                                                               +5v
                                                                                                       C43
                                               DS3691N                    1         4                  47pF                                            DATA OUT
                                                IC75                                         16                                            DATA IN
                                                                      2
                                                                                          15           47pF C46
                                                                      7                   9                                  RTS              E    A
                                                                      8                   10              R95 2K2
            DS88LS120N IC74                                                                                                                        C
                     +5v                                              3       5 6
                                                                                                                                              D    B
                  5 16 11                                                                                     R97 2K2
                1         15                                                  0v                                                     CTS
                7          4                                                                                                                            RS423
                6          3                                –5v                     R93                  R96                                            CONNECTOR
                9         12                                                        3K3                  3K3                                      0v    SK4
               10         13
                                  OPTIONAL
                                  RECEIVER
C39          C38 8 2    14
                                  TERMINATION                                                     0v
2n2F         2n2F
                                  NORMALLY
       0v                 S23 S24 OPEN

RS423 interface

                                                                                        504
                                                                                             +5v
                                                                                                          +5v                   1
                                      25       RD
                         NRDS
                                      24                                            R71                 LPSTB                             9
                         NWDS                  WR IC73
                                       15                                           2K7                    0v                   2
                                               D7
                                       16                                                                   I1                        10
                                                  µPD7002
                                       17                                                                  0v                   3
                                                                                                                                                PADDLE
                                                                         8
                                       18                     VREF                                                                    11        AND LIGHT
                                               D4                            C25 C27               1N4148 x 3
                                                                                                                                4
                                       19      D3                            33nF 1µF              D8                                           PEN
                                       20                                4                                                            12
                                                                                                                                                CONNECTOR
                                               D2                  CI                              D7                           5
                                       21      D1                                                                                               SK6
                                                                         6                                          I0
                                       22                    CI                                    D6                                 13
                                               D0                        10                                                     6
                                       27                   CH3                                                     0v
                                               A1                        11                                                           14
                                       26                   CH2
                                               A0                        12                                                     7
                                       28                   CH1
     EOC                                       EOC          CH0          13                                                           15
                R171                   23                                9
                             ADC               CS                                                                               8
                100                      2                AGND
                         1MHzE                 X1       GND
                                                          3
                                                                          0v

Analogue inputs

                                                            1K               C13 1nF
                                              +5v           R33                                                           +5v
                                                                                                                                                   10
                                                                                                74LS123                                                       8
                                              150                        7          6                                               S9 9
                                              R49 10                                          12 IC87               R65
                                                                                         Q                          3K3         RST
                                                                                              5                                                        IC27
                                                                          CLR            Q                    +5v                     0v
                                                        9
                                                                        11                                                      4             11
                                                                                                        R22         R23             RST         INT     30
                                                                           +5v  +5v
                                                        IC79             1K R37
                                                                                                        150         150    28 FAULT CNT/
                                                                                                                                     OPI
                   S4                                          2                                                                                        25
                                              3                                                                                               PLO/SS
                                                               1                                                            1              24
                                   2 x 7438                                                                                   TRST     CS
                                                                                                                           33 WR PROT
              34                                       IC80                                                                31 TRK 0
                                              11               13                                                          35 WR EN
SIDE SELECT                                                    12            IC80                                          27
                                                                                                                              RD DATA
READ DATA                                                                           10                                     29 WR DATA
                                                                     8
WRITE PROTECT                                                                        9                                                    7
                                                       IC80 4
TRACK 0                                       6                                                                            36 SEEK DACK
                                                                                                                              STEP
WRITE ENABLE                                                5                IC80 1
                                                                                                                           37 DIR      A1 22
WRITE DATA                                                          3
                                                                                    2                                                  A0 21
SEEK STEP                                     IC79             10                                                                IC78
                                                                                                                                 8271
DIRECTION
                                                               9             IC79                                                     DB7 19
LOAD HEAD                       S8            8
                                                                    11
                                                                                    12                                     38 LD HEAD DB6 18
                                                       IC79                         13                                      6 SEL 1   DB5 17
DRIVE SEL 1                                   6                5                                                            2 SEL 0   DB4 16
DRIVE SEL 0                                                    4                                                           34 INDEX DB3 15
INDEX                                                                                                                      26 DATA W DB2 14
                                                                                                                            3 CLOCK DB1 13
                                                      IC81                                5                                32 RDY 0 DB0 12
    PL8                                             74LS393                              3                    6             5 RDY 1
                                                  12 CLR                                  4                                         RD          WR
                        0v                                                       +5v                                            9             10
                                                  13          QC 9        11                 1
                                                                                              2
                                                                 8        10                 13
                                                              QD                                              12
                       S10                                                   9           8         74LS10
                                                                                                    IC82

Disc interface

                                                                505
                                                     +5v
                                       RL1
                                                                   2
                                 +5v                           4        5
                     5       4         220nF                                    CASSETTE
                         +        7                        1                3   CONNECTOR
                     6 –                                                        SK5
                                       C34
                             IC35                          6                7
                                         R86                           0v
                                                           R79
                                             220K
                             R87                    – 9
                                                           820K 0v
                                                 IC35 10
                             8K2               8    +
                                          R82    150K    820pF 820pF
                                          150K            C31   C35
                                               0v R78

Cassette interface

                                                    506
