#!/usr/bin/env python

from M import *

sleepytime=5
dol2=0
docagips=0

while(1):


    print
    print 'CurDTG+phms: ',mf.dtg('dtg.phms'),' <<<<<<<<ccccccccccccccccccccccccccccccccccccccccccccccccccccc'
    print
    

    bdir='/dat/cagips/datadir'           #jwtc
    bdir='/dat1/dat/cagips'              #esrl
    bdir='/data/amb/hfip/fiorino/dat/cagips'              #esrl

    l2cmd='/w21/prc/flddat/l2.py'        #jtwc
    l2cmd='/dat1/w21/prc/flddat/l2.py'   #esrl
    l2cmd='/data/amb/users/fiorino/w21/prc/flddat/l2.py'   #esrl

    dirs=['WXMAP_AOI','WXMAP_GFS','WXMAP_JMA','WXMAP_UKM']

    if(docagips):
        for dir in dirs:
            cmd="usage.py  %s/%s | grep -v \"\-\-\-\" | grep -v Files | grep -v Dirs"%(bdir,dir)
            mf.runcmd(cmd,lsopt='q')

    
    print
    cmd='ps -ef | grep python | grep -v root | grep -v keeplive | grep -v grep | grep -v wing'
    mf.runcmd(cmd,lsopt='q')

    if(dol2):
        cmd='%s cur gfsc,ngpc'%(l2cmd)
        mf.runcmd(cmd,lsopt='q')

        cmd='%s cur gfsc,ngpc -F'%(l2cmd)
        mf.runcmd(cmd,lsopt='q')

        cmd='%s cur-6 gfsc,ngpc'%(l2cmd)
        mf.runcmd(cmd,lsopt='q')

        cmd='%s cur-6 gfsc,ngpc -F'%(l2cmd)
        mf.runcmd(cmd,lsopt='q')

        cmd='%s cur-12 gfsc,ngpc'%(l2cmd)
        mf.runcmd(cmd,lsopt='q')

        cmd='%s cur-12 gfsc,ngpc -F'%(l2cmd)
        mf.runcmd(cmd,lsopt='q')

    time.sleep(sleepytime)



    
