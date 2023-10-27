#!/usr/bin/env python

"""%s

purpose:

  relabel using ln -s 9x wxmap adecks to numbered adecks

usages:

  %s YYYYMM | dtgopt -s SSS

  -s  source = jtwc | nhc | [ nrl | nasa | ncep | jma | ecmwf -- need to implement 
  -N         = norun
  -V         = verb
  -O         override=1
   
examples:

%s cur-12 -s local
%s 200809 -s local # do all maps for 200809

"""

import os
import time
import sys
import getopt

import string
import glob
import copy

import w2
import mf

#
#  tc stuff
#

import TCw2 as TC
import ATCF

from const import *        

#
#  defaults
#
tyear=None
dtgopt=None
imodel=None
omodel=None
source=None
doclean=0
override=0
opsdtg=None
ropt=''
stmopt=None

verb=0

curdtg=mf.dtg()
curdir=os.getcwd()
curtime=mf.dtg('curtime')
curphr=mf.dtg('phr')
curyear=curdtg[0:4]
pyfile=sys.argv[0]

narg=len(sys.argv)-1


#
# options using getopt
#

if(narg > 1):

    dtgopt = sys.argv[1]
    
    try:
        (opts, args) = getopt.getopt(sys.argv[2:], "s:NVKWO")

    except getopt.GetoptError:
        mf.usage(__doc__,pyfile,curdtg,curtime)
        print "EEE invalid getopt opt"
        sys.exit(2)

    for o, a in opts:
        if o in ("-s",""): source=a
        if o in ("-N",""): ropt='norun'
        if o in ("-V",""): verb=1
        if o in ("-K",""): doclean=1
        if o in ("-O",""): override=1

else:
    mf.usage(__doc__,pyfile,curdtg,curtime,curphr)
    sys.exit(1)

#lllllllllllllllllllllllllllllllllllllllllllllllllllllllllll 

import zipfile

def GetWxmapAdecks(dtg,source,istmid,ostmid,override=0,verb=0):

    istm3id=istmid.split('.')[0]
    istmyear=istmid.split('.')[1]

    ostm3id=ostmid.split('.')[0]
    ostmyear=ostmid.split('.')[1]

    if(istmyear != ostmyear):
        print 'EEEE 9x and Nx storm must have the same year...'
        sys.exit()
    else:
        stmyear=istmyear

    if(source == 'jtwc'):
        sdir=TC.AdeckDirJtwc
        
    elif(source == 'nhc'):
        sdir=TC.AdeckDirNhc
        
    elif(source == 'ncep'):
        adir=TC.AdeckDirNcep

    elif(source == 'tpc'):
        sdir=TC.AdeckDirTpc

    elif(source == 'jma'):
        sdir=TC.AdeckDirJma

    elif(source == 'ecmwf'):
        sdir=TC.AdeckDirEcmwf
        
    elif(source == 'local'):
        sdir=TC.AdeckDirLocal

    elif(source == 'hrd'):
        sdir=TC.AdeckDirHrd

    sdir="%s/%s/wxmap"%(sdir,stmyear)

    mf.ChangeDir(sdir)
    
    archzippath="adeck.wxmap.%s.%s.zip"%(istm3id,istmyear)
    try:
        ZZ=zipfile.ZipFile(archzippath,'a')
    except:
        ZZ=zipfile.ZipFile(archzippath,'w')

    
    smask="wxmap.*.%s"%(istm3id)
    adecks=glob.glob(smask)

    for iadeck in adecks:
        addtg=iadeck.split('.')[2]
        diffdtg=mf.dtgdiff(addtg,dtg)/24.0
        #
        # if diffdtg > 2.0 [d] -- means we have a future storm...
        #
        if(verb):
            print 'aaaaaaaaaaaaaaaaa iadeck: ',iadeck,' dtg: ',dtg,' addtg: ',addtg,'  diffdtg: ',diffdtg

        if(diffdtg >= -1.0 and diffdtg <= 10.0 or override):
            if(verb):
                print 'yyyyyyyyyyyyyyy ',dtg,addtg
            print 'ppppppppp ',iadeck,' dtg: ',dtg,'  diffdtg: ',diffdtg
            ZZ.write(iadeck,iadeck,zipfile.ZIP_DEFLATED)
            (base,exe)=os.path.splitext(iadeck)
            oadeck="%s.%s"%(base,ostm3id)
            #
            # before mv make sure we don't already have the target deck, i.e., if nhc/jtwc does NOT
            # drop the 9x storm when went to warning, e.g., 97E -> 05E.2005
            #
            if(os.path.exists(oadeck) and override == 0):
                print 'WWWWW oadeck: ',oadeck,' already there do not overwrite and kill off since it is in the zipfile...'
                os.unlink(iadeck)
            else:
                cmd="mv %s %s"%(iadeck,oadeck)
                mf.runcmd(cmd,ropt)

    ZZ.close()
        
    return


#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
# input check
#
dtgs=mf.dtg_dtgopt_prc(dtgopt)

#
# do months...
#

if(len(dtgopt) == 6):
    dtgs=[]
    mappaths=glob.glob("%s/%s/map*%s*"%(w2.TcCarqDatDir,dtgopt[0:4],dtgopt))
    for mappath in mappaths:
        (dir,file)=os.path.split(mappath)
        tt=file.split('.')
        dtg=tt[1]
        dtgs.append(dtg)
                       

if(source == 'all'):
    sources=['nhc','jtwc','local','tpc','ecmwf','jma']

else:
    sources=[source]

for dtg in dtgs:
    map9x=TC.GetMap9xDtg(dtg)
    
    if(len(map9x) > 0):
        
        istmids=map9x.keys()
        istmids.sort()
        for istmid in istmids:
            ostmid=map9x[istmid]
            print 'dtg: ',dtg,' istmid: ',istmid,' ostmid: ',ostmid

            for source in sources:
                GetWxmapAdecks(dtg,source,istmid,ostmid,override=override,verb=verb)

sys.exit()

