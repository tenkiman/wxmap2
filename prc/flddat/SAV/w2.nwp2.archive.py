#!/usr/bin/env python

"""
%s

purpose:

rsync nwp2 data coming from ncep -> snap drive /storage3 to new 1tb drive /storage0

usages:
%s yyyymm model [all|gfdl|hwrf|gfs2grib] -N -X

%s 200710 all -X

-N :: ropt='norun'
-X :: dormsrc=1
-t target = 'local' | 'local10'  | 'local11' | 'snap' | 'rmonly'

example:

%s 200801 all -t rmonly -X -- just kill off on src /storage3
%s 200712 all -t snap -X -- rsync to snap drive /storage4 and rm

(c) 2008 Michael Fiorino
"""

import os
import sys
import glob
import time
import getopt

import mf
import w2
import ncep
import hwrf

curdtg=mf.dtg()
curphr=mf.dtg('phr')
curyear=curdtg[0:4]
curtime=mf.dtg('curtime')
curdir=os.getcwd()
pypath=sys.argv[0]
(pydir,pyfile)=os.path.split(pypath)

#
#  defaults
#
ropt=''
model=None
dormsrc=0
target='local'

narg=len(sys.argv)-1

if(narg >= 2):

    yyyymm=sys.argv[1]
    model=sys.argv[2]
    try:
        (opts, args) = getopt.getopt(sys.argv[3:], "NXt:")

    except getopt.GetoptError:
        mf.usage(__doc__,pyfile,curdtg,curtime,curphr)
        sys.exit(2)

    for o, a in opts:
        if o in ("-N",""): ropt='norun'
        if o in ("-X",""): dormsrc=1
        if o in ("-t",""): target=a

else:
    mf.usage(__doc__,pyfile,curdtg,curtime,curphr)
    sys.exit(1)


dorsync=1
if(target == 'local'):
    targetbdir=w2.Nwp2DataArchiveBdirLocal
elif(target == 'local10'):
    targetbdir=w2.Nwp2DataArchiveBdirLocal10
elif(target == 'local11'):
    targetbdir=w2.Nwp2DataArchiveBdirLocal11
elif(target == 'snap'):
    targetbdir=w2.Nwp2DataArchiveBdirSnap
elif(target == 'rmonly'):
    targetbdir='/dev/null'
    dorsync=0
else:
    print 'EEE invalid target: ',target
    sys.exit()

if(model == 'all'):
    models=w2.Nwp2Models
    models.append('gfdl')
    models.append('hwrf')
    models.append('gfs2grib2')
    
else:
    models=[model]

# rsync -alv /storage3/nwp2/ncep/OUTDAT/gfs/prod/gfs.2007100? /storage0/nwp2/200710/ncep/OUTDAT/gfs/prod/
for model in models:

    if(not(w2.IsModel2(model)) and model != 'gfdl' and model != 'hwrf' and model != 'gfs2grib2'):
        print 'EEEE not a nwp2 model: ',model
        sys.exit()

    if(model == 'gfdl'):
        sdir=hwrf.GfdlBaseInDat
    elif(model == 'hwrf'):
        sdir=hwrf.HwrfBaseInDat
    elif(model == 'gfs2grib2'):
        sdir="%s/ncep/OUTDAT/gfs/prod"%(w2.Nwp2DataBdir)
    else:
        sdir=w2.Nwp2DataBdirModel(model)

    dd=sdir.split('/')
    modelroot="%s/%s"%(dd[len(dd)-2],dd[len(dd)-1])
    tdir="%s/%s/%s"%(targetbdir,yyyymm,modelroot)

    if(model == 'hwrf' or model == 'gfdl'):
        smask="%s/%s.%s*"%(sdir,model,yyyymm)
    elif(model == 'gfs2grib2'):
        smask="%s/gfs.%s??"%(sdir,yyyymm)
    else:
        smask="%s/%s*"%(sdir,yyyymm)

    print 'ttttttttttttt ',tdir,smask,dormsrc
    if(dorsync):

        if(model == 'gfs2grib2'):
            modelroot='ncep/OUTDAT/gfs/prod'
            tdir="%s/%s/%s"%(targetbdir,yyyymm,modelroot)

        if(ropt == ''):
            mf.ChkDir(tdir,'mk')

        rcmd="rsync -alv %s %s"%(smask,tdir)
        mf.runcmd(rcmd,ropt)
    
    if(dormsrc):
        cmd="rm -r %s"%(smask)
        mf.runcmd(cmd,ropt)



