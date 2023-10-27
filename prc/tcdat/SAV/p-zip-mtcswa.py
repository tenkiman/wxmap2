#!/usr/bin/env python

from WxMAP2 import *

sdir='/dat1/tc/cira/mtcswa'
sdir='/dat10/dat/tc/cira/mtcswa'
sdir='/dat10/dat/tc/cira/mtcswa_Late'
MF.ChangeDir(sdir)

year='2019'
year='2020'
byyyy=2005 ; eyyyy=2018
byyyy=2010 ; eyyyy=2018

years=mf.yyyyrange(byyyy, eyyyy)
ropt='norun'
#ropt=''

for year in years:
    stms=glob.glob('%s/???'%(year))
    stms.sort()

    for stm in stms:
        tt=stm.split('/')
        istm=tt[-1]
        cmd="zip -r -m -u %s/%s-%s.zip %s/%s"%(year,istm,year,year,istm)
        mf.runcmd(cmd,ropt)
        