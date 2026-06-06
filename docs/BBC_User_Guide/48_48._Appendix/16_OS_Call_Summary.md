# OS Call Summary

Routine          Vector       Summary of function
Name   Address   Name Address

                 UPTV      222   User print routine
                 EVNTV     220   Event interrupt
                 FSCV      21E   File system control entry
OSFIND   FFCE    FINDV     21C   Open or close a file
OSGBPB   FFD1    GBPBV     21A   Load or save a block of
                                 memory to a file
OSBPUT   FFD4    BPUTV     218   Save a single byte to file
                                 from A
OSBGET   FFD7    BGETV     216   Load a single byte to A
                                 from file
OSARGS   FFDA ARGSV        214   Load or save data about
                                 a file
OSFILE   FFDD FILEV        212   Load or save a complete
                                 file
OSRDCH   FFE0    RDCHV     210   Read character (from
                                 keyboard) to A
OSASCI   FFE3      —       —     Write a character (to
                                 screen) from A plus LF if
                                 (A)=&0D
OSNEWL   FFE7      —       —     Write LF,CR (&0A,&0D)
                                 to screen
OSWRCH   FFEE    WRCHV     20E   Write character (to
                                 screen) from A
OSWORD   FFF1    WORDV     20C   Perform miscellaneous
                                 OS operation using
                                 control block to pass
                                 parameters
OSBYTE   FFF4    BYTEV     20A   Perform miscellaneous
                                 OS operation using
                                 registers to pass
                                 parameters
OSCLI    FFF7    CLIV      208   Interpret the command
                                 line given
                 IRQ2V     206   Unrecognised IRQ
                                 vector
                 IRQ1V     204   All IRQ vector
                 BRKV      202   Break vector
                 USERV     200   Reserved

                         512
