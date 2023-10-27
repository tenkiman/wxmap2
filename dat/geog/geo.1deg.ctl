dset ^geo.1deg.grb
title geog based on Navy 10 min using equal lon lat boxes
undef 1e+20
dtype grib
index ^geo.1deg.gmp
xdef 360 linear 0.000000 1.000000
ydef 181 linear -90.000000 1.000000
zdef 1 levels 1013
tdef 1 linear 00Z1jan1 1dy
vars 2
orog      0    8,  1,  0,  0 Model topography [m]
sftlf     0  252,  1,  0,  0 Sfc type % land [%]
endvars
