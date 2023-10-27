#!/usr/bin/python

import mf 
years=range(1973,2018+1)
years=[2004]
ropt='norun'
ropt=''

for year in years:

    syear=str(year)
    syearp1=str(year+1)
    
    cmd="w2-tc-bt-adeck-final.py %s -p clean.all"%(syear)
    mf.runcmd(cmd,ropt)
    
    cmd="w2-tc-bt-bdeck-final.py %s -p clean.all"%(syear)
    mf.runcmd(cmd,ropt)

    cmd="w2-tc-bt-mdeck-final.py %s -p clean.all"%(syear)
    mf.runcmd(cmd,ropt)
    
    
    cmd="w2-tc-posit.py %s010100.%s123118.6 -C"%(syear,syear)
    mf.runcmd(cmd,ropt)
