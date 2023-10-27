#!/usr/bin/env python


"""%s

purpose:

rsync  kishou://wxamp2 after travel storage5 

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
tw2='%s/wxmap2'%(b5)
sw2='/wxmap2'

tmf='%s/home/mfiorino'%(b5)
smf='/home/mfiorino'

exopt="--exclude-from=%s/ex-wxmap2.txt"%(b5)

xopt=''
if(ropt == 'norun'):
    xopt='-n'
    ropt=''

#cd /home/mfiorino/
#rsync -alv  . $base5/home/mfiorino/

cmd="rsync -av %s %s %s/. %s/."%(xopt,exopt,smf,tmf)
mf.runcmd(cmd,ropt)


#cd /wxmap2/
#rsync -alv --delete --exclude-from=$base5/ex-wxmap2.txt . /storage5/kishou/wxmap2/
cmd="rsync --delete -av %s %s %s/. %s/."%(xopt,exopt,smf,tmf)

sys.exit()



dirs=['trunk/prc']

dirs=['dat/tc/vdeck']


for dir in dirs:
    xopt=''
    if(ropt == 'norun'):
        xopt='-n'
        ropt=''
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










