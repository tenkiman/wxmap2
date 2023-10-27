#!/usr/bin/env python

"""%s

purpose:

  run cola meteogram scripts

usages:

  %s dtgopt model -s stnid [-P -N -1]

  -C        = usecola=1 ; use cola server
  -P        = prodopt=1 ; production
  -N        = ropt='norun' ; don't run
  -S        = source [ncep|ncdc|ncep1]
  -1        = nam1hr ; 1hr nam
  -R        = userotating=1 ; use rotating archive at ncep
  
examples:

%s -d cur-6 -m gfs
%s -d cur-6 -m gfs -s dublin_ca -S ncep1|ncep|ncep5  # run using nomad1
"""

import os
import time
import sys
import getopt

import string
import glob

import w2
import mf

#
#  defaults
#

model=None
dtgopt=None
prcopt=None
stid=None
source='ncep'
prodopt=0
usecola=0
modelopt='nam3hr'
userotating=0
usearchive=0

ropt=''

verb=1

curdtg=mf.dtg()
curdir=os.getcwd()
curtime=mf.dtg('curtime')
curphr=mf.dtg('phr')
pyfile=sys.argv[0]

narg=len(sys.argv)-1

#
# options using getopt
#

if(narg >= 3):

    dtgopt=sys.argv[1]
    model=sys.argv[2]
    
    try:
        (opts, args) = getopt.getopt(sys.argv[3:], "m:d:p:s:S:NPC1R")

    except getopt.GetoptError:
        mf.usage(__doc__,pyfile,curdtg,curtime,curphr)
        print "EEE invalid getopt opt"
        sys.exit(2)

    for o, a in opts:
        if o in ("-p",""): prcopt=a
        if o in ("-s",""): stid=a
        if o in ("-S",""): source=a
        if o in ("-N",""): ropt='norun'
        if o in ("-P",""): prodopt=1
        if o in ("-C",""): usecola=1
        if o in ("-1",""): modelopt='nam1hr'
        if o in ("-R",""): userotating=1

else:
    mf.usage(__doc__,pyfile,curdtg,curtime,curphr)
    sys.exit(1)


try:
    (lon,lat)=w2.StationLonLat[stid]
except:
    print "EEEE: lon/lat for %s not available in w2.py"%(stid)
    print "current stid:"
    kk=w2.StationLonLat.keys()
    for k in kk:
        (lon,lat)=w2.StationLonLat[k]
        print "%20s :: lon: %6.1f  lat: %5.1f"%(k,lon,lat)
    sys.exit()


if(not(model) or not(dtgopt) or not(stid) ):
    print 'EEE must set -m model -d dtgopt -s dublin'
    sys.exit()

pdir=w2.W2BaseDirPlt+'/meteogram'
if(mf.find(dtgopt,'cur') and userotating):
    print 'ttttttttttt using rotating archive'
    archivetype='rotating'
elif(usearchive):
    print 'tttttttttt using archive ....'
    archivetype='archive'
else:
    print 'tttttttttt using realtime ....'
    archivetype='realtime'

dtg=mf.dtg_command_prc(dtgopt)

gradsexe='/tmp/grads/src/gradsdods'
gradsexe='/pcmdi/fiorino/grads19/rh9/bin/gradsdods'
gradsexe='/pcmdi/fiorino/grads19/rh8/bin/gradsdods'
gradsexe='gradsdods'
gradsexe='grads'

gradsopt='-pc'
if(prodopt): gradsopt='-pbc'
gradsgs=w2.MeteogramGs(model)

if(usecola): source='cola'

units='e'
if(stid == 'Reading_UK'): units='m'

if(ropt == ''):

    ctl=w2.MeteogramNomadsCtl(model,dtg,modelopt,source,archivetype)
    ctlpath='/tmp/nomads.%s.ctl'%(model)
    C=open(ctlpath,'w')
    C.writelines(ctl)
    C.close()

cmd="%s %s \"%s %s %s %5.1f %5.1f %s %s %s %s\""%\
     (gradsexe,gradsopt,gradsgs,stid,dtg,lon,lat,units,pdir,prodopt,usecola)


stimer=time.time()
mf.runcmd(cmd,ropt)
mf.Timer('done ',stimer)



