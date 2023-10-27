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
    yyyy=sys.argv[i] ; i=i+1
    if(mf.argopt(i)):  cmdtest=sys.argv[i] ; i=i+1
else:
    print "usage: %s "%sys.argv[0]+" yyyy"
    sys.exit()

basin='wp'
cf='carq.%s.0.%s.txt'%(basin,yyyy)
jf='jtwc.%s.0.%s.txt'%(basin,yyyy)

carq=open(cf).readlines()

ncarq=len(carq)
print "nnn: ",ncarq
#WP, 01, 2001021600, 01, CARQ,   0, 115N, 1374E,  15
#WP, 03, 2001050900, 01, CARQ,   0, 119N, 1218E,  25, 1002, XX,  35, NEQ,    0,    0,    0,    0, 1006,  120,  30,   0,   0,   W,   0,   X, 273,   8, 

for c in carq:
    tt=string.split(c,',')
    stmid=tt[1]
    dtg=tt[2]
    clat=tt[6]
    clon=tt[7]
    vmax=tt[8]
    pmin=-999
    if(len(tt) >= 18):
        pmin=tt[9]
        

        
    
    print stmid,dtg,clat,clon,vmax,pmin


sys.exit()

