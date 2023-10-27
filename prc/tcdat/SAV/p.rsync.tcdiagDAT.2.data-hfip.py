#!/usr/bin/env python

from M import *

MF=MFutils()

years=['2007','2008','2009','2010','2011']
years=['2007','2009','2010','2011']
years=['2008']
years=range(2014,2015+1)
years=['2015']

sdir='/data/amb/hfip/fiorino/w21/dat/tcdiagDAT'
tdir='/data/hfip/fiorino/products/hfip/tcdiagDAT'

dorsync=1
dorm=0

ropt='norun'
ropt=''

for year in years:
    
    year=str(year)
    
    sdiryear="%s/%s"%(sdir,year)
    tdiryear="%s/%s"%(tdir,year)
    MF.ChkDir(tdiryear,'mk')
    
    spaths=glob.glob("%s/%s*"%(sdiryear,year))
    for spath in spaths:
        dtg=spath[-10:]
        if(dorsync):
            tpath="%s/%s"%(tdiryear,dtg)
            MF.ChkDir(tpath,'mk')
            cmd="rsync -alv %s/ %s/"%(spath,tpath)
            MF.runcmd(cmd,ropt)

        if(dorm):
            cmd="rm -r %s"%(spath)
            MF.runcmd(cmd,ropt)
        
