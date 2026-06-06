# ASCII Teletext Alphanumeric

0          10       20          30    40    50   60   70   80   90   100   110      120
    nothing   down       nothing     move
0                                    cursor
                                     to 0,0

    next to   up         disable     move
1   printer              VDU         cursor

    start     clear      select
2   printer   screen     mode

    stop      start of   reprogram
3   printer   line       charac’s

    nothing   paged      nothing
4             mode

    nothing   scroll     nothing
5             mode

    enable    nothing    nothing
6   VDU

    beep      nothing    nothing                                                         back
7                                                                                        space &
                                                                                         delete

    back      nothing    nothing                                                         nothing
8

    forward   nothing    nothing                                                         alpha
9                                                                                        red

    Teletext (MODE 7) Displayed Alphanumeric Characters
    Each code produces a unique character. Thus VDU 78 or PRINT CHR$(78)
    would display an N since column 70, row 8 shows an N.

                                              486
   130          140         150      160   170   180   190   200   210   220   230   240   250
alpha       normal *     graphic
green       height       cyan

alpha       double       graphic
yellow      height       white

alpha       nothing      conceal
blue                     display

alpha       nothing     contiguous
magenta                 graphics *

alpha       nothing      separated
cyan                     graphics

alpha *     graphic      nothing
white       red

flash       graphic      black *
            green        backgr’nd

steady *    graphic      new
            yellow       backgr’nd

nothing     graphic      hold
            blue         graphics

nothing     graphic      release *
            magenta      graphics

* every line starts with these options

                                                 487
