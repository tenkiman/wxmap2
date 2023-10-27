#!/usr/bin/env python


"""%s

purpose:

rsync storage5 to kishou://wxamp2 after travel

usages:

-N -- nrun
-X -- run



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

ropt='norun'

narg=len(sys.argv)-1

i=1
if(narg >= 1):

    try:
        (opts, args) = getopt.getopt(sys.argv[1:], "NX")

    except getopt.GetoptError:
        mf.usage(__doc__,pyfile,curdtg,curtime)
        print "EEE invalid getopt opt"
        sys.exit(2)

    for o, a in opts:
        if o in ("-N",""): ropt='norun'
        if o in ("-X",""): ropt=''

else:
    mf.usage(__doc__,pyfile,curdtg,curtime)
    sys.exit(2)


b5='/storage5/kishou'
sw2='%s/wxmap2'%(b5)
tw2='/wxmap2'

exopt="--exclude-from=%s/ex-wxmap2.txt"%(b5)

dirs=['trunk/prc']

dirs=['dat/tc']
dirs=['dat/tc/vdeck']


for dir in dirs:
    xopt=''
    if(ropt == 'norun'):
        xopt='-n'
        ropt='norun'
    #
    # first update from kishou in case i changed files
    #
    cmd="rsync -u -av %s %s %s/%s/. %s/%s/."%(xopt,exopt,tw2,dir,sw2,dir)
    mf.runcmd(cmd,ropt)

    #
    # now rsync from storage5 to kishou
    #
    cmd="rsync -av %s %s %s/%s/. %s/%s/."%(xopt,exopt,sw2,dir,tw2,dir)
    mf.runcmd(cmd,ropt)










