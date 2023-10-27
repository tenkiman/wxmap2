dset ^tcbog.obs
#
#  new comment
#
title five TCBOG wind profile retrievals
dtype station
stnmap ^tcbog.smp
options sequential
undef 1e20
tdef 1 linear 00Z7Sep1987 6hr
vars  13
z     1 0 1000 h z [m]
uf    1 0 u fg [m/s]
vf    1 0 v fg [m/s]
ufb   1 0 u bias correction factor [m/s]
vfb   1 0 v bias correction factor [m/s]
ufc   1 0 u corrected fg [m/s]
vfc   1 0 v corrected fg [m/s]
um    1 0 u tc motion [m/s]
vm    1 0 v tc motion [m/s]
utr   1 0 u tc rankine [m/s]
vtr   1 0 v tc rankine [m/s]
u     1 0 u final [m/s]
v     1 0 v final [m/s]
endvars
