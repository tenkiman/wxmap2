#!/usr/bin/env python 
"""%s:
purpose:

  rsync tcanal output to usb2 drive

based on: rsync -alv --delete 2007/2007010100 /media/NO_NAME/kishou/work/wxmap2/dat/tc/tcanal/2007

usages:

  %s YYYY (year)|cur [-n -R]

  -R :: remove source data
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

from tcanalsub import * 

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

narg=len(sys.argv)-1

if(narg >= 1):

    dtgopt=sys.argv[1]
    
    try:
        (opts, args) = getopt.getopt(sys.argv[2:], "n:NR")

    except getopt.GetoptError:
        mf.usage(__doc__,pyfile,curdtg,curtime,curphr)
        print "EEE invalid getopt opt: ",opts,args
        sys.exit(2)

    for o, a in opts:
        if o in ("-n",""): ndayback=float(a)
        if o in ("-N",""): ropt='norun'
        if o in ("-R",""): dosrcrm=1

else:
    mf.usage(__doc__,pyfile,curdtg,curtime)
    sys.exit(1)


idtg=mf.dtg_command_prc(dtgopt)

year=idtg[0:4]

bdir=w2.TcTcanalDatDir
sdir=bdir+'/' + year
#
# 20070420 -- new 500 Gb usb2 drive for kishou
#
tdir=TC.TcanalDatDirusb2

idtgs=glob.glob("%s/%s??????"%(sdir,year))
idtgs.sort()

dtgs=[]
for idtg in idtgs:
    dtg=idtg.split('/')[8]
    dtgs.append(dtg)



os.chdir(bdir)

#
# sync db files to usbdrive
#
cmddb="rsync -alv --delete tc.db.*.txt %s"%(tdir)
mf.runcmd(cmddb,ropt)


#
# rsync and rm 
#
for dtg in dtgs:
    
    kdtgdiff=mf.dtgdiff(dtg,curdtg)/24.0
    if(kdtgdiff > ndayback):
        cmd="rsync -alv --delete %s/%s %s/%s"%(year,dtg,tdir,year)
        mf.runcmd(cmd,ropt)
        if(dosrcrm):
            cmdrm="rm -r %s/%s"%(year,dtg)
            mf.runcmd(cmdrm,ropt)


#
# rm db .txt files
#
if(dosrcrm):
    
    idbdtgs=glob.glob("%s/tc.db.??????????.txt"%(bdir))
    dbdtgs=[]
    for idbdtg in idbdtgs:
        (dir,file)=os.path.split(idbdtg)
        dtg=file.split('.')[2]
        dbdtgs.append(dtg)

    dbdtgs.sort()

    for dbdtg in dbdtgs:
        kdtgdiff=mf.dtgdiff(dbdtg,curdtg)/24.0
        if(kdtgdiff > ndayback):
            cmdrmdb="rm tc.db.%s.txt"%(dbdtg)
            mf.runcmd(cmdrmdb,ropt)

               

