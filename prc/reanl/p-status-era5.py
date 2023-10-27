#!/usr/bin/env python

from WxMAP2 import *
w2=W2()

#curyears=['1979.1980','1990.1998']
curyears=['1990.1993','1994','1996']
curyears=['1990.1994','2019']
curyears=['1984.1989']
curyears=['1979.1983']
curyears=['2019']
curyears=['2020']

verb=0
lsopt='q'
ocards={}

misses={}

doAll=1
#doAll=0

invOpt='-E'
invOptAll='-E -A'
if(doAll):  invOpt='-E -A'

print
for curyear in curyears:
    
    if(curyear == '2019' or curyear == '2020'):
        cmd="p-era5-active-inv.py %s %s | grep -B 4 SSS"%(curyear,invOptAll)
    else:
        cmd="p-era5-active-inv.py %s %s | grep -B 5 SSS"%(curyear,invOpt)
        
    rc=mf.runcmd2(cmd, ropt='', verb=verb, lsopt=lsopt, prefix='', postfix='', 
              ostdout=1, wait=False)
    
    if(len(rc) == 2):
        slines=rc[1]
        rc=rc[0]

        year=None
        oyears=[]
        for sline in slines:

            if(mf.find(sline.lower(),'mb') or mf.find(sline.lower(),'gb') and
               not(mf.find(sline.lower(),'sss'))
               ):
                
                dd=sline.split()
                ldtg=dd[0]
                ldtgtime="%s %s"%(dd[-2],dd[-1])
                
            if(year == None and mf.find(sline.lower(),'sss')):
                ss=sline.split()
                year=ss[-1]
                units=ss[-4]
                siz=ss[-5]
                try:
                    ldtg
                except:
                    ldtg='1776070400'
                    ldtgtime='18-12-00'
                    
                oyears.append(year)
                ocards[year]=(siz,units,ldtg,ldtgtime)
                year=None
            

    # -- missings:
    #
    cmd="p-era5-active-inv.py %s %s | grep -i miss | cut -c13-30"%(curyear,invOpt)

    rc=mf.runcmd2(cmd, ropt='', verb=verb, lsopt=lsopt, prefix='', postfix='', 
                  ostdout=1, wait=False)
    
    if(len(rc) == 2):
        missings=rc[-1]
        if(mf.find(str(missings),'probl')):  missings=['']
        misses[curyear]=missings
        
        
 
oyears=ocards.keys()
oyears.sort()

for oyear in oyears:
    
    (siz,units,ldtg,ldtgtime)=ocards[oyear]
    statcard="%s  %s   siz: %3d %s  at: %s"%(oyear,ldtg,int(siz),units,ldtgtime)
    print statcard
    if(oyear == '1980' or oyear == '1995' or oyear == '2019' or oyear == '2020'): print

print 
print 'MMMissings...'
print
for curyear in curyears:
    mm=misses[curyear]
    mtest0=(len(mm) == 1 and len(mm[0]) == 0)
    if(mtest0):
        print 'NNNOOO-missing for curyear: %10s'%(curyear)
    else:
        print 'MMMissing for curyear: ',curyear
        for m in mm:
            print m
        
    
