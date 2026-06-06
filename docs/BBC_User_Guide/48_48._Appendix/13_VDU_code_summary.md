# VDU code summary

ASCII abbrev.

                                       Bytes extra
Decimal

                CTRL
          Hex

                                                     Meaning
  0 0 @ NUL                             0            does nothing
  1 1 A SOH                             1            send next character to printer only
  2 2 B STX                             0            enable printer
  3 3 C ETX                             0            disable printer
  4 4 D EOT                             0            write text at text cursor
  5 5 E ENQ                             0            write text at graphics cursor
  6 6 F ACK                             0            enable vdu drivers
  7 7 G BEL                             0            make a short beep
  8 8 H BS                              0            backspace cursor one character
  9 9 I HT                              0            forwardspace cursor one character
 10 A J LF                              0            move cursor down one line
 11 B K VT                              0            move cursor up one line
 12 C L    FF                           0            clear text area
 13 D M CR                              0            move cursor to start of current line
 14 E N SO                              0            page mode on
 15 F O    SI                           0            page mode off
 16 10 P DLE                            0            clear graphics area
 17 11 Q DC1                            1            define text colour
 18 12 R DC2                            2            define graphics colour
 19 13 S DC3                            5            define logical colour
 20 14 T DC4                            0            restore default logical colours
 21 15 U NAK                            0            disable vdu drivers or delete current line
 22 16 V SYN                            1            select screen mode
 23 17 W ETB                            9            re-program display character
 24 18 X CAN                            8            define graphics window
 25 19 Y EM                             5            PLOT K,x,y
 26 1A Z SUB                            0            restore default windows
 27 1B [ ESC                            0            does nothing
 28 1C \   FS                           4            define text window
 29 1D ] GS                             4            define graphics origin
 30 1E ^ RS                             0            home text cursor to top left
 31 1F __ US                            2            move text cursor to x,y
127 7F   DEL                            0            backspace and delete

VDU code summary
                                                             507
