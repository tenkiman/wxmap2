#!/usr/bin/env python
from WxMAP2 import *
w2=W2()

byear=1998
byear=2018
byear=2019
eyear=2019

# -- 20211209 -- stops at 201912 :(
byear=2020
eyear=2021

bmo=1
emo=12

byear=2018
eyear=2018

bmo=12
emo=12

byear=2016 ; eyear=2016 ; bmo=1;emo=1
ropt='norun'
years=range(byear,eyear+1)
months=range(bmo,emo+1)

#tbdir='/dat13/dat/pr/cmorph-v10'
tbdir=w2.PrCV10DatRoot
tdir="%s/incoming"%(tbdir)
ropt='norun'
ropt=''

for year in years:
    itdir="%s/%4d"%(tdir,year)
    MF.ChkDir(itdir,'mk')
    
    for month in months:
        cmd='''wget --mirror --timeout=15 -t 2 --waitretry=15 -nd -np -l1 -A "*%4d%02d*.tar" -P %s "ftp://ftp@ftp.cpc.ncep.noaa.gov//precip/CMORPH_V1.0/CRT/8km-30min/%4d/"'''%(year,month,itdir,year)
        mf.runcmd(cmd,ropt)

    
                                                                                                                                                    
