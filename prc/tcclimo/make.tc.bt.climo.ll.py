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

ropt='norun'
ropt=''

verb=0

curdtg=mf.dtg()
curtime=mf.dtg('curtime')
pyfile=sys.argv[0]

narg=len(sys.argv)-1


if(narg > 0):

    try:
        (opts, args) = getopt.getopt(sys.argv[1:], "y:NIR")

    except getopt.GetoptError:
        mf.usage(__doc__,pyfile,curdtg,curtime)
        print "EEE invalid getopt opt"
        sys.exit(2)

    for o, a in opts:
        if o in ("-y",""): yyyymmopt=a
        if o in ("-N",""): ropt='norun'
        if o in ("-I",""): gradsexeopt='-pc'
        if o in ("-R",""): flagrl=1

else:
    mf.usage(__doc__,pyfile,curdtg,curtime)
    sys.exit(1)

if(not(yyyymmopt)):
    print "EEE must set -y yyyymmopt"
    sys.exit()

def makeCtl(dtg2):
    
    gtime=mf.dtg2gtime(dtg2)
    ctl="""dset ^btclimo.%s.dat
title frequence of occurance
undef 1e20
xdef 144 linear   0 2.5
ydef  73 linear -90 2.5
zdef   1 levels 1013
tdef   1 linear %s 6hr
vars 9
tcstr    0 0 scaled TC days  ts=0.5 ty=1.0 sty=2.0
ctcstr   0 0 climo scaled TC days  ts=0.5 ty=1.0 sty=2.0
atcstr   0 0 anom scaled TC days  ts=0.5 ty=1.0 sty=2.0
tcace    0 0 ACE (vmax*vmax if vmax >= 35)
ctcace   0 0 climo ACE (vmax*vmax if vmax >= 35)
atcace   0 0 anom ACE (vmax*vmax if vmax >= 35)
huace    0 0 Hurricane ACE (vmax*vmax if vmax >= 65)
chuace   0 0 climo Hurricane ACE (vmax*vmax if vmax >= 65)
ahuace   0 0 anom Hurricane ACE (vmax*vmax if vmax >= 65)
endvars"""%(dtg2,gtime)
    
    return(ctl)

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

btdfile="%s/climo/bt.climo.ctl"%(w2.TcDatDir)
#btdfile="%s/climo/bt.climo.ctl"%(w2.HfipTcDatDir)
#obtdir="%s/climo/current"%(w2.HfipTcDatDir)
obtdir="%s/climo/current"%(w2.TcDatDir)
cbtctl="%s/btclimo.%s.ctl"%(obtdir,dtg2)
gsopt="%s %s %s %s %d %s %s"%(dtg1,dtg2,obtdir,btdfile,flagrl,
                           byearClimo,eyearClimo)

(gsfile,ext)=os.path.splitext(pyfile)
gsfile=gsfile+'.gs'

xgrads=setXgrads(useStandard=0, useX11=0, returnBoth=0)
gradsexe="%s %s"%(xgrads,gradsexeopt)

print 'dddddddd ',gsopt

cmd="%s \"run %s %s\" -g 600x800-0+0"%(gradsexe,gsfile,gsopt);
mf.runcmd(cmd,ropt)

MF.WriteString2Path(makeCtl(dtg2),cbtctl)

sys.exit()
