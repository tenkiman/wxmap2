#!/usr/bin/env python

from WxMAP2 import *

ropt='norun'
ropt=''
doRsync=1
doit=0
doit=1

mtcbdir='/w21/dat/tc'
stcbdir='/ssd2/dat/tc-2021'
utcbdir='/dat2/dat/tc'

tcdirs=open('tc-dat-ops-2021.txt').readlines()

gtot=0
for tcdir in tcdirs:
    tcdir=tcdir[:-1]
    if(not(doRsync)): 
        tcdir="%s/%s"%(stcbdir,tcdir)
    if(mf.find(tcdir,'#stop')): break
    if(mf.find(tcdir,'#')): continue

    if(doRsync):
        rsyncOpt='-alvn --size-only'
        if(ropt == '' and doit): rsyncOpt='-alv'
        
        mbase='/w21/dat/tc'
        sbase='/ssd2/dat/tc-2021'
        ubase='/dat2/dat/tc'

        sdir="%s/%s"%(sbase,tcdir)
        tdir="%s/%s"%(mbase,tcdir)
        if(ropt == ''): MF.ChkDir(tdir,'mk')
        cmd='rsync %s %s/ %s/'%(rsyncOpt,sdir,tdir)
        if(ropt == 'norun'):
            mf.runcmd(cmd,ropt)
        else:
            lines=MF.runcmdLogOutput(cmd,ropt)
            print lines
    else:
        cmd='usage.py %s'%(tcdir)
        lines=MF.runcmdLog(cmd,ropt,quiet=1)
        for line in lines:
            if(mf.find(line,'Total')):
                tctot=line.split()[-1].replace(',','')
                tctot=int(tctot)/1024
                tctot=tctot/1024.0
                gtot=gtot+tctot
                print '%-48s %6.1f GB'%(tcdir,tctot)

if(not(doRsync)):
    print '%-28s %6.1f GB'%('Grand Tot: ',gtot)
