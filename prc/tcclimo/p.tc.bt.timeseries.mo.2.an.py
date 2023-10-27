#!/usr/bin/env python

"""%s

purpose:

usages:

  -y  yyyymmopt  : YYYYMM1.YYYYMM2 for ran of yyyymm
  -b  basin      : wpac | epac | lant | nhem | shem | global
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
from w2base import setXgrads

verb=0

curdtg=mf.dtg()
curtime=mf.dtg('curtime')
curdir=posix.getcwd()
pyfile=sys.argv[0]

narg=len(sys.argv)-1

#
# defaults
#

gradsexeopt='-lbc'
ropt=''

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

datdir=w2.TcClimoDatDir

gsopt="%s "%(datdir)

(gsfile,ext)=os.path.splitext(pyfile)
gsfile=gsfile+'.gs'

xgrads=setXgrads(useStandard=0, useX11=1, returnBoth=0)
gradsexe="%s %s"%(xgrads,gradsexeopt)

print 'dddddddd ',gsopt

cmd="%s \"run %s %s\" -g 800x600-0+0"%(gradsexe,gsfile,gsopt);
mf.runcmd(cmd,ropt)

sys.exit()
