# Memory maps

HEX     DECIMAL
                                                        &FFFF   65535
                              OPERATING SYSTEM ROM
                                                        &FF00   65280
                           MEMORY MAPPED INPUT/OUTPUT
                                                        &FC00   64512

                              OPERATING SYSTEM ROM

                                                        &C000   49152

                             4 PAGED ROMS e.g. BASIC

                                                        &8000   32768

                                  RAM USED FOR
                            HIGH RESOLUTION GRAPHICS
                                                        MOVEABLE BOUNDARY
                  HIMEM            BASIC STACK

  32K RAM
IN MODEL B                                              &4000   16384
 TO &8000

                  LOMEM     DYNAMIC VARIABLE STORAGE
                                                        MOVEABLE BOUNDARY
       16K RAM       TOP
     IN MODEL A                                         &2000   8192
      TO &4000              USER’S BASIC PROGRAM AREA

                   PAGE                                 &0E00   3584
                             RESERVED FOR OPERATING
                                   SYSTEM USE
                                                        &0000   0

Memory map

                                  500
                                                      &0E00   3584
       space for operating system resident routines
                                                      &0D00   3328
            user defined character definitions
                                                      &0C00   3072
           user defined function key definitions
                                                      &0B00   2816
                      various buffers
                                                      &0A00   2560
                      various buffers
                                                      &0900   2304
                      misc. workspace
                                                      &0800   2048

                language ROM workspace

                                                      &0400   1024
                      misc. workspace
                                                      &0300   768
              operating system workspace
                                                      &0200   512
                        6502 stack
                                                      &0100   256
                         zero page
                                                      &0000   0

Memory map (detail)

                                     501
