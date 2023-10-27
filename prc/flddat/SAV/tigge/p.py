#!/usr/bin/env python

"""
%s dtg [-V -N]

dtg -- if != cur or ops then only process a single time
-N ropt='norun'
-V verb=1

purpose:

usages:

%s cur-12

(c) 2009 by Michael Fiorino, NOAA
"""

import os
import sys
import glob
import time
import getopt

import mf
import w2
import ecMARS as E

#ddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd
# defaults

ropt=''
verb=0


curdtg=mf.dtg()
curphr=mf.dtg('phr')
curyear=curdtg[0:4]
curtime=mf.dtg('curtime')
curdir=os.getcwd()

pypath=sys.argv[0]
(pydir,pyfile)=os.path.split(pypath)
narg=len(sys.argv)-1

if(narg >= 1):

    dtgopt=sys.argv[1]
    if(len(dtgopt.split('.')) == 1):
        (dtg,phr)=mf.dtg_phr_command_prc(dtgopt)
        dtgs=[dtg]
    else:
        dtgs=mf.dtg_dtgopt_prc(dtgopt)
            
    try:
        (opts, args) = getopt.getopt(sys.argv[2:], "VN")

    except getopt.GetoptError:
        mf.usage(__doc__,pyfile,curdtg,curtime,curphr)
        sys.exit(2)

    for o, a in opts:
        if o in ("-N",""): ropt='norun'
        if o in ("-V",""): verb=1

else:
    mf.usage(__doc__,pyfile,curdtg,curtime,curphr)
    sys.exit(1)


    

#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# main

S=E.MARS.yotc
fcstep='0/to/168/by/6'

for dtg in dtgs:

    ruaA=E.uaReq(dtg,type='an')
    ruaF=E.uaReq(dtg,type='fc',step=fcstep)
    rsfcA=E.sfcReq(dtg,type='an')
    rsfcF=E.sfcReq(dtg,type='fc',step=fcstep)
    
    S.retrieve(rsfcF.req)
    S.retrieve(ruaF.req)
    
sys.exit()

serveryotc.retrieve({
    'dataset'  : "yotc_od",
    'step'     : "0/to/12/by/6",
    'levtype'  : "sfc",
    'date'     : "%s/to/%s"%(ymd,ymd),
    'time'     : "%s"%(hh),
    'type'     : "fc",
    'param'    : "%s"%(sfcvars),
    'levelist' : "%s"%(plevs),
    'area'     : "global",
    'grid'     : "0.5/0.5",
    'target'   : "yotc.sfc.%s.grb1"%(dtg),
    })

