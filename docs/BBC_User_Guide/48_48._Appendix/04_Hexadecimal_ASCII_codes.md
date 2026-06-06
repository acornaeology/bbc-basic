# Hexadecimal ASCII codes

MSB         8                    9           A   B   C   D    E       F
                                LSB             0                    1           2   3   4   5    6       7
                                0000 0       Nothing         Clear graphics
                                                                                     0   @   P    £       p
                                                                   area
                                0001 1    Next to printer   Define text colour   !   1   A   Q    a       q
                                0010 2        Start          Define graphic
                                                                                 “   2   B   R    b       r
                                             printer              colour
                                0011 3         Stop           Define logical
                                                                                 #   3   C   S    c       s
                                             printer              colour
                                0100 4      Separate         Default logical
                                                                                 $   4   D   T    d       t
                                             cursors             colours
                                0101 5         Join           Erase line or
                                                                                 %   5   E   U    e       u

      Hexadecimal ASCII Codes
                                             cursors          Disable VDU
                                0110 6     Enable VDU          Select mode       &   6   F   V    f       v
                                0111 7        beep             Reprogram
                                                                                 ‘   7   G   W    g       w

492
                                                                characters
                                1000 8         back          Define graphics
                                                                                 (   8   H   X    h       x
                                                                   area
                                1001 9       forward                Plot         )   9   I   Y    i       y
                                1010 A        down           Default screen
                                                                                 *   :   J   Z    j       z
                                                                   areas
                                1011 B          up               Nothing         +   ;   K   [    k       {
                                1100 C    Clear text area    Define text area    ,   <   L   \    l       ¦
                                1101 D       Carriage        Define graphic
                                                                                 –   =   M   ]    m       }
                                              return              origin
                                1110 E     Paged mode           Move text
                                                                                 .   >   N   ^    n       ~
                                                on            cursor to 0,0
                                1111 F     Paged mode           Move text                             Backspace
                                                                                 /   ?   O   __   o
                                                off           cursor to X,Y                           and delete
