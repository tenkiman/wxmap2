dset ^veg_clss.dat
title ISLCSP veg class
options sequential yrev
undef 1e20
xdef 360 linear -179.5 1
ydef 180 linear  -89.5 1
zdef   1 levels 1013
tdef   1 linear jan1900 1mo
vars 1
v 0 0 veg
endvars
