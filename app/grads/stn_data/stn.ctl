dset ^stn.dat
dtype station
stnmap ^stn.map
undef -999.0
title point values from global spectral coeffs
tdef      4 linear 0z9mar1990   24hr
vars  12
gz    0 99 surface geopotential height(m)
ps    0 99 surface pressure(mb)
zeflx 0 99 total column vorticity flux(N/m**3)
tflx  0 99 total column heat flux(w/m**2)
qflx  0 99 total column moisture flux(w/m**2)
u     1 99 east-west component of wind(m/s)
v     1 99 north-south component of wind(m/s)
tv    1 99 virtual temperature(K)
t     1 99 temperature(K)
q     1 99 specific humidity(gm/gm)
div   1 99 divergence(1/s)
vor   1 99 vorticity(1/s)
endvars
