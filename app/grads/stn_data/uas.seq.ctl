dset ^uas.seq.obs
title four U.S. rawindsonde soundings (multilevel) WITH sfc observations
options sequential
dtype station
stnmap ^uas.seq.smp
undef 1e20
tdef 1 linear 12Z08Oct1995 12hr
vars  10
psl  0 0 sea level pressure [hPa]
ts   0 0 sfc air temperature [C]
tds  0 0 sfc air dewpoint temperature [C]
us   0 0 sfc u wind comp [m/s]
vs   0 0 sfc v wind comp [m/s]
z    1 0 geopotential height [m]
t    1 0 t [C}
td   1 0 td [C]
u    1 0 u [m/s]
v    1 0 v [m/s]
endvars
