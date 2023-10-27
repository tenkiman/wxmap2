#!/usr/bin/env python

from WxMAP2 import *
w2=W2()

w2.ls('DSs')

smask="%s/mdecks2*.pypdb"%(w2.TcDatDirDSs)

md2s=glob.glob(smask)
ropt='norun'
ropt=''

for md2 in md2s:
    (fdir,ffile)=os.path.split(md2)
    (fbase,fext)=os.path.splitext(ffile)
    tt=fbase.split('-')
    try:
        year=int(tt[-1])
    except:
        year=None

    if(len(tt) == 2 and year != None and (year >= 1900 and year <= 2020)):
        print 'gggg good: ',md2
        isgood=1
    else:
        isgood=0
        
    if(not(isgood)):
        cmd="rm %s"%(md2)
        mf.runcmd(cmd,ropt)


