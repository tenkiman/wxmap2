#!/usr/bin/env python 

"""%s:
purpose:

  script for extracting sfc/850 wind fields for TC struct application

usages:

  %s YYYYmmddhh (cur, cur-NNN, cur+NNN) | model
  
examples:

%s cur ops
"""
import sys
import os
import glob
import string
import posix
import posixpath

import mf


from tcanalsub import * 

curdtg=mf.dtg6()
curdir=posix.getcwd()

pyfile=sys.argv[0]

narg=len(sys.argv)-1
i=1
if(narg >= 2):
    dtg=mf.dtg_command_prc(sys.argv[i]) ; i=i+1
    model=sys.argv[i] ; i=i+1
    if(mf.argopt(i)):  cmdtest=sys.argv[i] ; i=i+1
else:
    print __doc__%(pyfile,pyfile,pyfile)
    print "The Current DTG: ",curdtg
    sys.exit()

#iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
#
# input setup
#
#iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii


fdir=TcEnv['dat.fld']

res='10'
if(model == 'ukm'): res='12'
fpath="%s/%s.%s.%s.ctl"%(fdir,model,res,dtg)

print "FFF ",fpath

if(not(os.path.exists(fpath))):
    print "Fields for model: %s on dtg: %s NOT THERE..."%(model,dtg)
    print "fpath: %s"%(fpath)
    sys.exit()

#oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
#
# output setup
#
#oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

odir=TcEnv['dat.tcstruct']

odir="%s/%s"%(odir,dtg)

if not(os.path.isdir(odir)):                                                              
    print "odir ",odir," is not there -- mkdir"                                           
    os.mkdir(odir)                                                                        

opath="%s/fld.tcstruct.%s.%s.dat"%(odir,model,dtg)
cpath="%s/fld.tcstruct.%s.%s.ctl"%(odir,model,dtg)
cmd="grads -lbc \"run p.fld.data.tcsanal.gs %s %s %s %s\""%(dtg,model,fpath,opath)
print "CCC: ",cmd
doit=0
if(doit): os.system(cmd)

nt=11
if(model == 'ukm'): nt=8

gtime=mf.dtg2gtime(dtg)
ctl="""dset ^fld.tcstruct.avn.2002082812.dat
title fields for tcstruct analysis
undef 1e20
options big_endian
xdef 360 linear   0.0 1.0
ydef 181 linear -90.0 1.0
zdef   1 levels 1013
tdef  %s linear %s 12hr
vars 4
uas 0 0 uas
vas 0 0 vas
u8  0 0 u850
v8  0 0 v850
endvars"""%(nt,gtime)

c=open(cpath,'w')

c.writelines(ctl)
                                             
