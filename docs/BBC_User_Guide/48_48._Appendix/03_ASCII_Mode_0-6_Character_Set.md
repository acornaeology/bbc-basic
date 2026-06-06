# ASCII Mode 0-6 Character Set

0           10           20      30       40    50   60   70   80   90   100
    nothing    down       default     move text
0                         logical     cursor
                          colours     to 0,0

    next to    up         disable     move
1   printer               VDU         text
                                      cursor

    start      clear      select
2   printer    screen     mode

    stop       start of   reprogram
3   printer    line       charac’s

    separate   paged      define
4   cursors    mode       graphics
                          area

    join       scroll     plot
5   cursors    mode

    enable     clear      default
6   VDU        graphics   text/
                          graphics
                          areas
    beep       define     nothing
7              text
               colour

    back       define     define
8              graphics   text
               colour     area

    forward    define     define
9              logical    graphics
               colours    origin

    ASCII (MODES 0 to 6) Displayed Character Set and Control Codes
    Each displayed character consists of 8 rows of 8 dots.

                                                  490
110    120     130   140   150   160   170     180   190   200     210   220   230   240   250

                                             ALL CHARACTERS
                                             UNDEFINED INITIALLY

      back
      space
      &
      delete

                                        491
