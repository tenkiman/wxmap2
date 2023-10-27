#!/usr/bin/env python

"""%s

purpose:

  generate cliper TC track forecasts

usages:

  %s dtg
  %s all dtgb dtge [dt]      # range of forecasts
  
examples:

%s cur
"""

import os
import sys
import posix
import posixpath

import string
import glob
import getopt

import TCw2 as TC
import TCclip

import mf
import w2

from tcanalsub import *

#
#  defaults
#
verb=0
ropt=''
overwrite=1
stmidset='all'
usecarq=0

curdtg=mf.dtg()
curphr=mf.dtg('phr')
curyear=curdtg[0:4]
curtime=mf.dtg('curtime')
curdir=os.getcwd()
pyfile=sys.argv[0]

narg=len(sys.argv)-1

if(narg > 0):

    dtgopt=sys.argv[1]
    
    try:
        (opts, args) = getopt.getopt(sys.argv[2:], "NVOC")

    except getopt.GetoptError:
        mf.usage(__doc__,pyfile,curdtg,curtime,curphr)
        sys.exit(2)

    for o, a in opts:
        if o in ("-N",""): ropt='norun'
        if o in ("-V",""): verb=1
        if o in ("-O",""): overwrite=0
        if o in ("-C",""): usecarq=1

else:
    mf.usage(__doc__,pyfile,curdtg,curtime,curphr)
    sys.exit(1)

    
dd=dtgopt.split('.')
ddtg=6

if(len(dd) == 1):
    bdtg=mf.dtg_command_prc(dtgopt)
    edtg=bdtg
    dtg=bdtg

if(len(dd) >= 2):
    bdtg=mf.dtg_command_prc(dd[0])
    edtg=mf.dtg_command_prc(dd[1])

if(len(dd) == 3):
    ddtg=dd[2]

if(bdtg == -1 or edtg == -1):
    print "EEE bad dtginput: ",dtgopt
    sys.exit()

dtgs=mf.dtgrange(bdtg,edtg,ddtg)

for dtg in dtgs:

    #
    # set up the directories
    #

    (cdir,bdir,prcddir,\
     odir,ogdir,osdir,otdir,oddir,opdir,\
     oadir,pdir,\
     wpddir,wgddir)=SetTcanalDirs(dtg)

    print cdir,bdir

    if(usecarq):
        (stmidscq,stmdatacq,stmmotioncq)=ParseCarqStorms(dtg,stmidset)
        (stmidsbt,stmdatabt,stmmotionbt)=ParseBdeckStorms(dtg,stmidset)
        (stmids,stmdata,stmmotion)=UniqStorms(stmidscq,stmdatacq,stmmotioncq,
                                              stmidsbt,stmdatabt,stmmotionbt)
    else:
        (stmids,stmdata,stmmotion)=ParseBtOpsStorms(dtg,stmidset)

    if(stmids[0] == 'notcs'):
        print "No TCs in adeck (CARQ) or bdeck (BEST)"
        next

    clpdir=otdir

    clppath=clpdir+"/tc.clp.%s.tracks.txt"%(dtg)
    if(usecarq):
        (hcards,tccards)=TCclip.MakeCliperForecast2(dtg,stmids,stmdata,stmmotion)
    else:
        (hcards,tccards)=TCclip.MakeCliperForecast3(dtg,stmids,stmdata,stmmotion)
        
    if(hcards == 0): continue

    #
    #  output
    #

    o=open(clppath,'w')

    for card in hcards:
        if(verb): print card
        card=card+'\n'
        o.write(card)

    for card in tccards:
        if(verb): print card
        card=card+'\n'
        o.write(card)

    print 'CCCCCCCCCCCCCCCCCC: ',clppath
    o.close()


sys.exit()

