#!/usr/bin/env python 

import sys
import os
import glob
import string
sys.path.append("/home/fiorino/lib/python")
import mf

from tcanalsub import * 

narg=len(sys.argv)-1
i=1
if(narg >= 1):
    dtg=mf.dtg_command_prc(sys.argv[i]) ; i=i+1
    if(mf.argopt(i)):  cmdtest=sys.argv[i] ; i=i+1
else:
    print "usage: %s "%sys.argv[0]+" yyyy"
    sys.exit()

basin='wp'

dd=TcEnv['dat.jtwc']

yyyy=dtg[0:4]

cf='carq.%s.0.%s.txt'%(basin,yyyy)
jf='jtwc.%s.0.%s.txt'%(basin,yyyy)

cmd="grep -h '%s,   0,' %s/a%s??%s.dat > %s"%('CARQ',dd,basin,yyyy,cf)
cmd="grep -h '%s,   0,' %s/a%s??%s.dat | grep -h %s "%('CARQ',dd,basin,yyyy,dtg)
run(cmd,1)

cmd="grep -h '%s,   0,' %s/a%s??%s.dat > %s"%('JTWC',dd,basin,yyyy,jf)
cmd="grep -h '%s,   0,' %s/a%s??%s.dat | grep -h %s "%('JTWC',dd,basin,yyyy,dtg)
run(cmd,1)

sys.exit()

