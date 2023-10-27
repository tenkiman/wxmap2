#!/usr/bin/env python


"""%s

purpose:

rsync  kishou://w21 <-> wjet 

usages:

-N -- nrun
-X -- run
-u -- update mode

"""

import os
import sys
import time
import getopt

import mf

#ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss

curdtg=mf.dtg()
curtime=mf.dtg('curtime')
curphr=mf.dtg('phr')
curdir=os.getcwd()

pyfile=sys.argv[0]

roptopt='norun'
doupdate=0

narg=len(sys.argv)-1

i=1
if(narg >= 1):

    try:
        (opts, args) = getopt.getopt(sys.argv[0:], "NXD:u")

    except getopt.GetoptError:
        mf.usage(__doc__,pyfile,curdtg,curtime)
        print "EEE invalid getopt opt"
        sys.exit(2)

    for o, a in opts:
        if o in ("-N",""): roptopt='norun'
        if o in ("-X",""): roptopt=''
        if o in ("-u",""): doupdate=1

else:
    mf.usage(__doc__,pyfile,curdtg,curtime)
    sys.exit(2)


sw21='/w21/web'
ssvr='fiorino@jetscp.rdhpcs.noaa.gov:'
ssvr=''
tw21='/w21/weba'
tsvr=''
dirs=['config']
    

for dir in dirs:

    print 'rsync dir: ',dir
    exfile='ex-w21.txt'
    uopt=''
    if(doupdate): uopt='-u'
    
    if(roptopt == 'norun'):
        xopt='-n'
	ropt=''
    elif(roptopt == ''):
        xopt=''
        ropt=''
        
    #
    # now rsync from storage5 to kishou
    #
    cmd="rsync --exclude-from=%s -alv %s %s \"%s%s/%s/.\"  \"%s%s/%s/.\""%(exfile,xopt,uopt,ssvr,sw21,dir,tsvr,tw21,dir)
    mf.runcmd(cmd,ropt)










