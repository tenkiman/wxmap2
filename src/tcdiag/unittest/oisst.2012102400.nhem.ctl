dset ^oisst.2012102400.nhem.dat
title test
undef 1e+20
options sequential template
xdef 720 linear    0.00    0.50
ydef 161 linear    0.00    0.50
zdef  1 levels 1013
tdef 1 linear 00Z24Oct2012 6hr
vars 3
sst        0 0 sst with mask [K]
sstall     0 0 sst filled in mask [K]
ssta       0 0 sst anom [C]
endvars