#!/usr/bin/env python

"""%s

purpose:

  lat/lon maps of tc activity over a time period by basin

usages:

  %s -y dtg -b basin [ -p prcopt -d pltdir ] 

  -y  dtg        : bdtg.edtg for ran of yyyymm
  -b  basin      : wpac | niopac | epac | epaclant | lant | shem | nhem
 [-p  tcexpr      : [ts] | ty  ]
 [-d  pltdir     : target dir to put plots  ]
 
  -R  flagrl=1 or this is a current time plot -- don't use mid-month scale factor

examples:

%s -y 200001.cur -b wpac 
"""

import posix
from tcbase import *

byearClimo=1981
eyearClimo=2010

#
#  defaults
#

pltdir=None
yyyymmopt=None
basin=None
prcopt=None
tcexpr='ts'
#
# default is scaled tc (tcstr) vice ts
#
tcexpr='tcstr'
gradsexeopt='-pbc'
#
# flag if real time so we don't multiply by the month factor
#
flagrl=0

#
# good basins
# 

basinopts=['wpac','niopack','epaclant','epac','lant','nio','shem','nhem','global','sio','swpac']
ropt='norun'
ropt=''

verb=0

curdtg=mf.dtg()
curtime=mf.dtg('curtime')
curdir=posix.getcwd()
pyfile=sys.argv[0]

narg=len(sys.argv)-1

#
# veriname is always arg #1
#

#
# options using getopt
#
override=0
if(narg > 0):

    try:
        (opts, args) = getopt.getopt(sys.argv[1:], "y:b:p:v:d:ONIR")

    except getopt.GetoptError:
        mf.usage(__doc__,pyfile,curdtg,curtime)
        print "EEE invalid getopt opt"
        sys.exit(2)

    for o, a in opts:
        if o in ("-y",""): yyyymmopt=a
        if o in ("-b",""): basin=a
        if o in ("-p",""): tcexpr=a
        if o in ("-v",""): viopt=a
        if o in ("-d",""): pltdir=a
        if o in ("-N",""): ropt='norun'
        if o in ("-O",""): override=1
        if o in ("-I",""): gradsexeopt='-pc'
        if o in ("-R",""): flagrl=1

else:
    mf.usage(__doc__,pyfile,curdtg,curtime)
    sys.exit(1)

if(not(yyyymmopt) or not(basin)):
    print "EEE must set -y yyyymmopt -b basin"
    sys.exit()


def yyyymm2dtg(yyyymm):
    
    if(len(yyyymm) == 3 and yyyymm == 'cur'):
        dtg=curdtg
    elif(len(yyyymm) == 6):
        dtg=yyyymm+'0100'
    elif(len(yyyymm) == 10):
        dtg=yyyymm
    else:
        print "EEE invalid yyyymm: %s"%(yyyymm)
        sys.exit()
    return(dtg)

tt=yyyymmopt.split('.')

if(len(tt) != 2):
    print 'EEE -y yyyymmopt must be in form yyyymm1.yyyymm2'
    sys.exit()

(yyyymm1,yyyymm2)=tt

dtg1=yyyymm2dtg(yyyymm1)
dtg2=yyyymm2dtg(yyyymm2)

print 'dddd ',dtg1,dtg2

#
# basin check
#

basingood=0
for basinopt in basinopts:
    if(basin == basinopt): basingood=1

if(not(basingood)):
    print "EEE invalid basin: %s"%(basin)
    sys.exit()

if(pltdir == None):
    pltdir=TC.PltTcClimoDir

pltfile="tc.cnt.%s.%s.%s.%s"%(basin,yyyymm1,yyyymm2,tcexpr)

pltfile="tc.act.llmap.%s.%s.%s.%s"%(basin,dtg1[0:8],dtg2[0:8],tcexpr)

btdfile="%s/climo/current/btclimo.%s.ctl"%(w2.TcDatDir,dtg2)

if(MF.getPathSiz(btdfile) <= 0 or override):
    cmd="make.tc.bt.climo.ll.py -y %s"%(yyyymmopt)
    mf.runcmd(cmd,ropt)

#btdfile="%s/climo/bt.climo.ctl"%(w2.HfipTcDatDir)
gsopt="%s %s %s %s %s %s %s %s %d %s %s"%(basin,dtg1,dtg2,pltdir,pltfile,tcexpr,curdtg,btdfile,flagrl,
                                          byearClimo,eyearClimo)

(gsfile,ext)=os.path.splitext(pyfile)
gsfile=gsfile+'.gs'


xgrads=setXgrads(useStandard=0, useX11=0, returnBoth=0)

gradsexe="%s %s"%(xgrads,gradsexeopt)

cmd="%s \"run %s %s\" -g 600x800-0+0"%(gradsexe,gsfile,gsopt);
mf.runcmd(cmd,ropt)

sys.exit()
