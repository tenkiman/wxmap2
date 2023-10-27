dset ^sfc.grb2
index ^sfc.gmp
undef 9.999E+20
title data.grib
*  produced by g2ctl v0.0.4m
* griddef=1:0:(2400 x 602):grid_template=0: lat-lon grid:(2400 x 602) units 1e-06 input WE:NS output WE:SN res 48 lat 80.099998 to -10.050000 by 0.149995 lon 0.000000 to 359.850000 by 0.149994 #points=1444800:winds(N/S)

dtype grib2
ydef 602 linear -10.050000 0.149995
xdef 2400 linear 0.000000 0.149994
tdef 1 linear 06Z01oct2009 1mo
zdef 1 linear 1 1
vars 3
pmsl  0,101   0,3,0 ** mean sea level pressure [Pa]
u10m   0,103,10   0,2,2 ** 10 m above ground u_velocity [m/s]
v10m   0,103,10   0,2,3 ** 10 m above ground v_velocity [m/s]
ENDVARS
