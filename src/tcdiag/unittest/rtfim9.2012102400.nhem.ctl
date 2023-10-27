dset ^rtfim9.2012102400.nhem.f%f3.dat
title test
undef -1e+20
options sequential template
xdef 720 linear    0.00   0.500
ydef 161 linear    0.00   0.500
zdef  10 levels 1000 850 700 500 400 300 250 200 150 100
tdef 19 linear 00Z24Oct2012 6hr
vars 28
uas          0 0 uas [m/s]
vas          0 0 vas [m/s]
psl          0 0 psl [mb]
prw          0 0 psl [mb]
pr           0 0 pr 6-h rate [mm/day]
vrt925       0 0 rel vort 925 [*1e5 /s]
vrt850       0 0 rel vort 850 [*1e5 /s]
vrt700       0 0 rel vort 700 [*1e5 /s]
zthklo       0 0 600-900 thick [m]
zthkup       0 0 300-600 thick [m]
z900         0 0 900 [m]
z850         0 0 850 [m]
z800         0 0 800 [m]
z750         0 0 750 [m]
z700         0 0 700 [m]
z650         0 0 650 [m]
z600         0 0 600 [m]
z550         0 0 550 [m]
z500         0 0 500 [m]
z450         0 0 450 [m]
z400         0 0 400 [m]
z350         0 0 350 [m]
z300         0 0 300 [m]
ua          10 0 ua [m/s]
va          10 0 va [m/s]
hur         10 0 hur [%]
ta          10 0 ta [K]
zg          10 0 zg [m]
endvars