#!/usr/bin/env python

"""%s

purpose:

  merge osp/archive bt from jtwc/nhc with neumann bt

usages:

  %s yyyy

examples:


%s 1970

"""

import os
import sys
import posix
import posixpath
import time

import getopt

import string
import glob

import TCw2 as TC

import mf
import w2
import ATCF


#
#  defaults
#

popt=None
ropt=''

verb=0

curdtg=mf.dtg()
curyyyy=curdtg[0:4]
curtime=mf.dtg('curtime')
curdir=posix.getcwd()
pyfile=sys.argv[0]

do9Xstms=1
source='neumann'

narg=len(sys.argv)-1

#
# veriname is always arg #1
#

#
# options using getopt
#

if(narg > 0):

    yyyy=sys.argv[1]

    try:
        (opts, args) = getopt.getopt(sys.argv[2:], "b:p:v:s:VN")

    except getopt.GetoptError:
        mf.usage(__doc__,pyfile,curdtg,curtime)
        print "EEE invalid getopt opt"
        sys.exit(2)

    for o, a in opts:
        if o in ("-p",""): popt=a
        if o in ("-v",""): viopt=a
        if o in ("-s",""): source=a
        if o in ("-N",""): ropt='norun'
        if o in ("-V",""): verb=1

else:
    mf.usage(__doc__,pyfile,curdtg,curtime)
    sys.exit(1)

try:
    (yyyy1,yyyy2)=yyyy.split('.')
    years=range(int(yyyy1),int(yyyy2)+1)
except:
    years=[int(yyyy)]



def GetBtnAndBtoDics(year):

    try:
        tcns=TC.GetTCnamesHash(year)
        tcss=TC.GetTCstatsHash(year)
        bnns=tcns.keys()
    except:
        tcns=None
        tcss=None
        bnns=None
        

    return(tcns,tcss,bnns)




allbns=TC.BasinsAll


#yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy
#
# loop by years
#
#yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy


for year in years:

    ntca=0
    ntcs=0
    ntct=0
    stcdsum=0.0
    acesum=0.0
    
    (tcns,tcss,bnns)=GetBtnAndBtoDics(year)

    #kks=tcss.keys()
    #for kk in kks:
    #    print 'kkkkkkkk ',kk,tcss[kk][0],tcss[kk][2]
    #sys.exit()

    #  0  TY
    #  1 IVO         
    #  2 70
    #  3 8.8
    #  4 16.4
    #  5 255.8
    #  6 2007091518
    #  7 2007092412
    #  8 4.5  - stcd
    #  9 7.25 - tc days in stcd
    #  10 5.8 - ace
    #  11 4.25 - tc days in ace

    obasins=['C','W']
    doall=1
    
    for bnn in bnns:
        
        basin=bnn[1][2]

        if(doall):
            ts=tcss[bnn]
            vmax=ts[2]
            stcd=ts[8]
            ace=ts[10]
            ntca=ntca+1
            if(vmax >= 35):
                ntcs=ntcs+1
                if(vmax >= 65):
                    ntct=ntct+1
                    
            stcdsum=stcdsum+stcd
            acesum=acesum+ace
            
        else:
            for obasin in obasins:
                if(basin == obasin):
                    ts=tcss[bnn]
                    vmax=ts[2]
                    stcd=ts[8]
                    ace=ts[10]
                    ntca=ntca+1
                    if(vmax >= 35):
                        ntcs=ntcs+1
                    if(vmax >= 65):
                        ntct=ntct+1

                    stcdsum=stcdsum+stcd
                    acesum=acesum+ace
                

    print "%s, %3d, %3d, %3d, %5.1f, %5.1f"%(year,ntca,ntcs,ntct,stcdsum,acesum)
            
        
    
sys.exit()
