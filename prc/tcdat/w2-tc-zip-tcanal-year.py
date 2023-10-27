#!/usr/bin/env python

from M import *
MF=MFutils()

from WxMAP2 import *


ropt='norun'
years=range(2011,2017)
years=[2018]
years=[2018]

years=range(2015,2019)

years=[2021]

bmo=1
emo=12
ropt=''
#ropt='norun'

sdir='.'
zopt='-u -m -r'

for year in years:

    MF.ChangeDir('./%s'%(year),verb=1)
    
    zfile="../tcanal-%d.zip"%(year)
    masks=['0[0-5]??','0???','1[0-5]??','1???','2[0-5]??','2???','????']
    
    for mo in range(bmo,emo+1):
        
        ym="%s%02d"%(str(year),mo)
        print ym
        
        tmask="%s/*.%s????.*"%(sdir,ym)
        cmd="zip %s %s %s"%(zopt,zfile,tmask)
        mf.runcmd(cmd,ropt)
    
        print
        for mask in masks:
            
            zmask="%s/%s%s/*/*"%(sdir,ym,mask)
            cmd="zip %s %s %s"%(zopt,zfile,zmask)
            mf.runcmd(cmd,ropt)
        
        print
    
