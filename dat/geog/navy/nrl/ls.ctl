dset ^ls.dat
title land (1) sea (0) masks
undef 1e20
options big_endian
xdef 360 linear    0.500    1.000
ydef 180 linear  -89.500    1.000
zdef   1 levels 1013.0
tdef   1 linear 0z1jan1990 1mo
vars   1
w 0 0 ls mask
endvars
