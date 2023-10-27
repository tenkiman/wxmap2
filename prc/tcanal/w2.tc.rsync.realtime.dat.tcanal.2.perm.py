#!/usr/bin/env python 
"""%s:
purpose:

 rsync realtime (/work/wxmap2/dat/tc/tcanal) -> "perm (new 300 gb drive)" (/data/wxmap2/dat/tc/tcanal)

usages:

  %s YYYY (year)|cur [-n -R]

  -n :: ndayback 
  -N :: norun
  
examples:

%s 2007

"""

import sys
import os
import glob
import string
import getopt

import mf
import w2
import TCw2 as TC


#
#  defaults
#

dosrcrm=0

ropt=''

ndayback=w2.w2NdayClean

curdtg=mf.dtg()
curphr=mf.dtg('phr')
curyear=curdtg[0:4]
curtime=mf.dtg('curtime')
curdir=os.getcwd()

pypath=sys.argv[0]
(pydir,pyfile)=os.path.split(pypath)
basedtg=None

narg=len(sys.argv)-1

if(narg >= 1):

    dtgopt=sys.argv[1]
    
    try:
        (opts, args) = getopt.getopt(sys.argv[2:], "n:N")

    except getopt.GetoptError:
        mf.usage(__doc__,pyfile,curdtg,curtime,curphr)
        print "EEE invalid getopt opt: ",opts,args
        sys.exit(2)

    for o, a in opts:
        if o in ("-n",""): ndayback=float(a)
        if o in ("-N",""): ropt='norun'

else:
    mf.usage(__doc__,pyfile,curdtg,curtime)
    sys.exit(1)


if(dtgopt == None):
    print 'EEE set dtgopt to set the dtg to go ndabyback: ',ndayback
    sys.exit()

#
# rsync real-time to perm
#

bdirrt=w2.TcDatDir
bdirperm=w2.TcDatDir2

mf.ChangeDir(bdirrt)
rcmd="rsync -rulptv tcanal %s"%(bdirperm)
mf.runcmd(rcmd,ropt)
