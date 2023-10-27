#!/usr/bin/env python

"""
purpose:

  plot/process cpc q|cmorph grib

usage:

%s cur -S

dtgopt: dtg1.dtg2.ddtg | dtg1

examples:

%s cur -S cmoprh

(c) 2008 Michael Fiorino
"""

import os
import sys
import glob
import time
import getopt

import mf
import w2
import TCw2 as TC
import ATCF

curdtg=mf.dtg()
curphr=mf.dtg('phr')
curyear=curdtg[0:4]
curtime=mf.dtg('curtime')
curdir=os.getcwd()
pypath=sys.argv[0]
(pydir,pyfile)=os.path.split(pypath)
if(pydir == ''): pydir=curdir

#
#  defaults
#
ropt=''
narg=len(sys.argv)-1
ropt=''
verb=0
source=None
area=None

if(narg >= 1):

    dtgopt=sys.argv[1]

    try:
        (opts, args) = getopt.getopt(sys.argv[2:], "NVS:a:")

    except getopt.GetoptError:
        mf.usage(__doc__,pyfile,curdtg,curtime,curphr)
        sys.exit(2)

    for o, a in opts:
        if o in ("-N",""): ropt='norun'
        if o in ("-V",""): verb=1
        if o in ("-S",""): source=a
        if o in ("-a",""): area=a

else:
    mf.usage(__doc__,pyfile,curdtg,curtime,curphr)
    sys.exit(1)


    
#llllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll
#
# local



#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
# main



#
# when running from cron need to change dir...
#

mf.ChangeDir(pydir)

dtgs=mf.dtg_dtgopt_prc(dtgopt)


sopt='qmorph'
if(source != None):
    sopt=source

aopt=''
if(area != None):
    aopt=area

for dtg in dtgs:
    gacmd="grads -lc \"p.pr.qmorph.gs %s %s %s\""%(dtg,sopt,aopt)
    mf.runcmd(gacmd,ropt)


sys.exit()
