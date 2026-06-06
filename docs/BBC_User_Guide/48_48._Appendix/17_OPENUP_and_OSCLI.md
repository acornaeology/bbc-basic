# OPENUP and OSCLI

OPENUP open file for update
Purpose
This statement can be used with disc or Econet systems to open
a file for update – that is, simultaneous reading and/or writing.
With Econet, only one user may open a file for writing at any
one time and therefore OPENUP should only be
used in single user environments.

If a file of the given name exists already then that file will be
opened without any changes taking place to the file. If no file of
that name exists then OPENUP will fail to open the file
requested.

OPENUP is normally used with random access files on disc or
on the Level 2 Econet filing systems.

Example
   500 Y%=OPENUP("DATA")

Description
A function which returns the channel number allocated to a file
opened for both reading and writing. The file must exist before
this function can be used.

Syntax
<num-var> = OPENUP(<string>)

Associated keywords
OPENIN, OPENOUT, PTR#, EXT#, INPUT#,
PRINT#, BGET#, BPUT#, EOF#, CLOSE#

                               513
                      operating system
OSCLI                 command line interpreter

Purpose
It is very useful in a BASIC program to be able to send
commands to the operating system. Such commands might
include *FX commands followed by two numbers. When the
program is written you do not always know which numbers
are to follow the *FX statement. However, you cannot
substitute variables such as X and Y directly after the *FX
because these variables are not known to the command line
interpreter but are only known to the BASIC language. Thus the
statement
X=5:Y=3:*FX X,Y
would be meaningless to the operating system. The statement
OSCLI provides a neat way of passing variables to the
operating system in such cases. OSCLI is followed by a string
variable which is set to contain the values to be passed to the
operating system. Note that numbers must be converted to
string form by using the STR$ function; the above example
would work correctly with the following:
     10   X=5
     20   Y=3
     30   A$="FX "+STR$X+","+STR$Y
     40   OSCLI A$

Example
   10 FN$="XYZ" : REM FILE NAME
   20 START%=&4000 : REM START OF CODE
   30 END%=&6000 : REM END OF CODE
   40 EXEC%=&5000 : REM EXEC ADDRESS
  300 OSCLI "SAVE "+FN$+" "+STR$~(
START%)+" "+STR$~(END%)+" "+STR$~(
EXEC%)

Note that no * is needed in the string.

                              514
Description
A statement which passes its string argument to the operating
system command line interpreter.

Syntax
OSCLI<string>

Associated keywords
STR$, CHR$

                             515
516
