#!/usr/bin/env python 

"""%s:
purpose:

  master script for running TC struct application

usages:

  %s bdtg edtg model
  
examples:

%s cur ngp
"""
import sys
import os
import glob
import string
import posix
import posixpath
sys.path.append("/home/fiorino/lib/python")
import mf

from tcanalsub import * 

curdtg=mf.dtg6()
curdir=posix.getcwd()

pyfile=sys.argv[0]

narg=len(sys.argv)-1
i=1
if(narg >= 3):
    bdtg=mf.dtg_command_prc(sys.argv[i]) ; i=i+1
    edtg=mf.dtg_command_prc(sys.argv[i]) ; i=i+1
    model=sys.argv[i] ; i=i+1
    if(mf.argopt(i)):  cmdtest=sys.argv[i] ; i=i+1
else:
    print __doc__%(pyfile,pyfile,pyfile)
    print "The Current DTG: ",curdtg
    sys.exit()

doit=1
ddtg=12
if(model == 'avn' or
   model == 'tc.db' or
   model == 'ngp'
   ): ddtg=6

dtgs=mf.dtgrange(bdtg,edtg,ddtg)

for dtg in dtgs:

    cmd="p.tc.tcstruct.py %s %s"%(dtg,model)
    print 'CCC: ',cmd
    if(doit): os.system(cmd)


