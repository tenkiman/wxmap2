#!/usr/bin/env python

"""
%s

purpose:

  update current tau=0 graphics on web by cp from ../archive/YYYYMMDDHH to ../current

usages:

  %s dtg [-u]

examples:

  %s cur -u -- make current dtg main and set as current

(c) 2005 by Michael Fiorino, LLNL
"""


import os
import sys
import string
import glob
import time
import getopt

import mf

import wxmap

#
#  defaults
#
ropt=''
update=0

curdtg=mf.dtg()
curphr=mf.dtg('phr')
curyear=curdtg[0:4]
curtime=mf.dtg('curtime')
curdir=os.getcwd()
pyfile=sys.argv[0]

narg=len(sys.argv)-1

if(narg >= 1):

    dtgopt=sys.argv[1]

    if(len(dtgopt) == 21):
        tt=dtgopt.split('.')
        tdtg1=tt[0]
        tdtg2=tt[1]
        tdtgs=mf.dtgrange(tdtg1,tdtg2,6)
    else:
        (tdtg,tphr)=mf.dtg_phr_command_prc(dtgopt)
        tdtgs=[tdtg]

    try:
        (opts, args) = getopt.getopt(sys.argv[2:], "uNV")

    except getopt.GetoptError:
        mf.usage(__doc__,pyfile,curdtg,curtime,curphr)
        sys.exit(2)

    for o, a in opts:
        if o in ("-u",""): update=1
        if o in ("-N","--run"): ropt='norun'
        if o in ("-V","--verb"): verb=1

else:
    mf.usage(__doc__,pyfile,curdtg,curtime,curphr)
    sys.exit(1)


template=wxmap.htmMainTemplate
wdir=wxmap.wxhWeb

wxdtgs=wxmap.GetWxmapDtgs(tdtg)

models=wxdtgs.keys()
models.sort()

for model in models:
    mdtg=wxdtgs[model]
    sdir=wxmap.ModelGrfDir(model,mdtg)
    tt=sdir.split('/')
    ntt=len(tt)
    if(model != 'sst'):
        for i in range(0,ntt-2):
            if(i==0):
                tdir="%s"%(tt[i])
            else:
                tdir="%s/%s"%(tdir,tt[i])
        tdir=tdir+'/current'
        cmd="cp %s/*.*.000.*.png %s/."%(sdir,tdir)
        mf.runcmd(cmd,ropt)
    elif(model == 'sst'):
        for i in range(0,ntt-3):
            if(i==0):
                tdir="%s"%(tt[i])
            else:
                tdir="%s/%s"%(tdir,tt[i])
        tdir=tdir+'/current'
        sdir=sdir.replace('tropwpac','*')
        cmd="cp %s %s/."%(sdir,tdir)
        mf.runcmd(cmd,ropt)
        
    

sys.exit()
