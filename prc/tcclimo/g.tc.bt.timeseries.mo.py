#!/usr/bin/env python

"""%s

purpose:

  plot tc activity in time series by basin

usages:

  %s -y yyyymmopt -b basin [ -p prcopt -d pltdir ]

  -y  yyyymmopt  : YYYYMM1.YYYYMM2 for ran of yyyymm
  -b  basin      : wpac | epac | lant | nio | nhem | shem | global
 [-p  tcexpr      : [ts] | ty | tcstr ]
  -I             : run interactive

examples:

%s -y 200001.cur -b nhem
"""

import os
import sys
import posix
import posixpath
import getopt

import string
import glob

import TCw2 as TC
import mf
import w2

from tcbase import byearClimo,eyearClimo
from tcbase import setXgrads

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
gradsexeopt='-lbc'

#
# good basins
# 

basinopts=['wpac','epac','lant','nio','nhem','shem','global','sio','swpac']
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

if(narg > 0):

    try:
        (opts, args) = getopt.getopt(sys.argv[1:], "y:b:p:v:d:NI")

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
        if o in ("-I",""): gradsexeopt='-lc'

else:
    mf.usage(__doc__,pyfile,curdtg,curtime)
    sys.exit(1)

if(not(yyyymmopt) or not(basin)):
    print "EEE must set -y yyyymmopt -b basin"
    sys.exit()

tt=yyyymmopt.split('.')

if(len(tt) != 2):
    print 'EEE -y yyyymmopt must be in form yyyymm1.yyyymm2'
    sys.exit()

else:

    (yyyymm1,yyyymm2)=tt
    if(yyyymm2 == 'cur'): yyyymm2=curdtg[0:6]
    

dyyyymm=mf.yyyymmdiff(yyyymm1,yyyymm2)

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

pltfile="tc.act.mots.%s.%s.%s.%s"%(basin,yyyymm1,yyyymm2,tcexpr)

print 'ddddddddd ',pltdir,pltfile

gtime1=mf.yyyymm2gtime(yyyymm1)
gtime2=mf.yyyymm2gtime(yyyymm2)


datdir=w2.TcClimoDatDir

print 'ddddddddddddddddddddddddddddddddddd',dyyyymm

gsopt="%s %s %s %s %s %s %s %s %s %s %s"%(basin,
                                          gtime1,gtime2,
                                          datdir,
                                          pltdir,pltfile,
                                          curdtg,tcexpr,dyyyymm,
                                          byearClimo,eyearClimo)

(gsfile,ext)=os.path.splitext(pyfile)
gsfile=gsfile+'.gs'

xgrads=setXgrads(useStandard=0, useX11=0, returnBoth=0)

gradsexe="%s %s"%(xgrads,gradsexeopt)

print 'dddddddd ',gsopt

cmd="%s \"run %s %s\" -g 800x600-0+0"%(gradsexe,gsfile,gsopt);
print cmd
mf.runcmd(cmd,ropt)

sys.exit()
