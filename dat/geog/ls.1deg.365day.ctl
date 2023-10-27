dset ^ls.1deg.dat
title geog based on Navy 10 min using equal lon lat boxes
undef 1e+20
options big_endian 365_day_calendar
xdef 360 linear 0.00 1.0
ydef 181 linear -90.00 1.0
zdef 1 levels 1013
tdef 1 linear 00Z1jan1 1dy
vars 1
ls      0    8,  1,  0,  0 Model topography [m]
endvars
