dset ^uv.850.tcfilt.dat
title test
undef 1e20
options sequential
xdef 360 linear   0.0 1.0
ydef 181 linear -90.0 1.0
zdef   1 levels 850
tdef   1 linear 12z6sep1989 12hr
vars 14
u    0 0 input u
us   0 0 whole-field smoothed u
ud   0 0 disturbance u (u-us); in hurricane zone = uhd + uhz
ufd  0 0 vortectomised ud
uhd  0 0 hurricane part of ufd
uhz  0 0 non-hurricane part of ud in hurricane zone
uf   0 0 final vortectomised u
v    0 0 input v
vs   0 0 whole-field smoothed v
vd   0 0 disturbance v (v-vs); in hurricane zone = vhd + vhz
vfd  0 0 vortectomised ud
vhd  0 0 hurricane part of vfd
vhz  0 0 non-hurricane part of vd in hurrican zone
vf   0 0 final vortectomised v = us + ufd
endvars

