#!/usr/bin/env python 

"""%s:
purpose:

  script for extracting sfc/850 wind fields for TC struct application

usages:

  %s YYYYmmddhh (cur, cur-NNN, cur+NNN) | model
  
examples:

%s cur ngp
"""
import sys
import os
import glob
import string
import posix
import posixpath

import mf
import w2

specopt=None

from tcanalsub import * 

curdtg=mf.dtg6()
curdir=posix.getcwd()

pyfile=sys.argv[0]

narg=len(sys.argv)-1
i=1
if(narg >= 4):
    dtg=mf.dtg_command_prc(sys.argv[i]) ; i=i+1
    model=sys.argv[i] ; i=i+1
    fldpath=sys.argv[i] ; i=i+1
    oddir=sys.argv[i] ; i=i+1
    if(mf.argopt(i)):  specopt=sys.argv[i] ; i=i+1
else:
    print __doc__%(pyfile,pyfile,pyfile)
    print "The Current DTG: ",curdtg
    sys.exit()

print "FFF ",fldpath

if(not(os.path.exists(fldpath))):
    print "Fields for model: %s on dtg: %s NOT THERE..."%(model,dtg)
    print "fldpath: %s"%(fldpath)
    sys.exit()

#oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
#
# output setup
#
#oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo


if not(os.path.isdir(oddir)):                                                              
    print "EEEEEEEEEEEEEEEEEEEEEEEEE error oddir should have already been made..."
    sys.exit()

opath="%s/fld.tcstruct.%s.%s.dat"%(oddir,model,dtg)
cpath="%s/fld.tcstruct.%s.%s.ctl"%(oddir,model,dtg)
cmd="grads2 -lbc \"run p.fld.data.tcstruct.gs %s %s %s %s\""%(dtg,model,fldpath,opath)
print "CCC: ",cmd
doit=1
if(doit): os.system(cmd)

nt=11
if(model == 'ukm'): nt=8

gtime=mf.dtg2gtime(dtg)
ctl="""dset ^fld.tcstruct.%s.%s.dat
title fields for tcstruct analysis
undef 1e20
xdef 360 linear   0.0 1.0
ydef 181 linear -90.0 1.0
zdef   1 levels 1013
tdef  %s linear %s 12hr
vars 4
uas 0 0 uas
vas 0 0 vas
u8  0 0 u850
v8  0 0 v850
endvars"""%(model,dtg,nt,gtime)

c=open(cpath,'w')

c.writelines(ctl)
                                             

