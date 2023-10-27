dset ^tovsfb.19%y2%m2%d2%h2.obs
title 1dvar feedback from OI
dtype station
options sequential template big_endian
stnmap ^tovsfb.8609.smp
undef 1e20
tdef   1 linear 00Z1Sep1986 6hr
vars 27
sid   0 0 satellite id
cf    0 0 path 1=clear 2=p.cloudy 3=cloudy
ls    0 0 land sea mask (0=land,1=sea)
stt   0 0 status of Tv in trop (p>=100)
sts   0 0 status of Tv in strat(p>100)
srt   0 0 status of RH in lower trop (<=700)
tv850 0 0 obs Tv from 1000-700 thk
tv600 0 0 obs Tv from 700-500 thk
tv400 0 0 obs Tv from 500-300 thk
tv200 0 0 obs Tv from 300-200 thk
rh925 0 0 obs RH 1000-850 
rh775 0 0 obs RH 850-700
rh600 0 0 obs RH 700-500 
tv850f 0 0 obs-fg Tv from 1000-700 thk
tv600f 0 0 obs-fg Tv from 700-500 thk
tv400f 0 0 obs-fg Tv from 500-300 thk
tv200f 0 0 obs-fg Tv from 300-200 thk
rh925f 0 0 obs-fg RH 1000-850 
rh775f 0 0 obs-fg RH 850-700
rh600f 0 0 obs-fg RH 700-500 
tv850a 0 0 obs-an Tv from 1000-700 thk
tv600a 0 0 obs-an Tv from 700-500 thk
tv400a 0 0 obs-an Tv from 500-300 thk
tv200a 0 0 obs-an Tv from 300-200 thk
rh925a 0 0 obs-an RH 1000-850 
rh775a 0 0 obs-an RH 850-700
rh600a 0 0 obs-an RH 700-500
endvars
