#!/usr/bin/env python
from WxMAP2 import *

def makeCmorphV10Ctl(nt,year,ropt='norun'):
    
    yearm1=int(year)-1
    ctlpath="cmorph-v10-%s.ctl"%(year)
    ctl="""dset ^grib/%%y4/%%y4%%m2/cmorph-v10.%%y4%%m2%%d2%%h2.grb
title c|qmorph pr
undef 1e+20
dtype grib
index ^cmorph-V10-%s.gmp
options template
xdef 1440 linear  0.125 0.25
ydef 480 linear -59.875 0.25
zdef 1 levels 1013
tdef %d linear 00Z31Dec%d 30mn
vars 1
pr        0   59,  1,  0,  0 qmorph precip. (mm/hr) []
endvars"""%(year,nt,yearm1)

    rc=MF.WriteCtl(ctl,ctlpath)
    cmd="time gribmap -E -0 -i %s"%(ctlpath)
    mf.runcmd(cmd,ropt)
	




byear=1999
eyear=2019
#byear=1998
#eyear=1998

years=range(byear,eyear+1)

tbdir='/w21/dat/pr/cmorph-v10'
MF.ChangeDir(tbdir,verb=1)

ropt='norun'
ropt=''

for year in years:
    nt=17520
    if(int(year)%4 == 0):
        nt=17568
        print 'LLLL',year,nt
    nt=nt+48*2  # start a day before and go a day forward
    rc=makeCmorphV10Ctl(nt,year,ropt)
