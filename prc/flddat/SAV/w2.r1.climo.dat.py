#!/usr/bin/env python 

"""create smoothed daily wind climo for a dtg

   %s dtg opt [ opt1 | opt2 ]

   dtg: curNNN ; NNN=+12,+6,-6,-12


example:

 %s cur
 %s 200401 -M

 
"""

import sys
import os
import glob
import string
import posix
import getopt

import mf
import w2

#
#  defaults
#
ropt=''
moclimo=0
verb=0
override=0

curdtg=mf.dtg()
curphr=mf.dtg('phr')
curyear=curdtg[0:4]
curtime=mf.dtg('curtime')
curdir=os.getcwd()
pyfile=sys.argv[0]

narg=len(sys.argv)-1

if(narg > 0):

    (dtg,phr)=mf.dtg_phr_command_prc(sys.argv[1]) 

    try:
        (opts, args) = getopt.getopt(sys.argv[2:], "MNVO")

    except getopt.GetoptError:
        mf.usage(__doc__,pyfile,curdtg,curtime,curphr)
        sys.exit(2)

    for o, a in opts:
        if o in ("-N",""): ropt='norun'
        if o in ("-O",""): override=1
        if o in ("-V",""): verb=1
        if o in ("-M",""): moclimo=1

else:
    mf.usage(__doc__,pyfile,curdtg,curtime,curphr)
    sys.exit(1)


ddir=w2.R1ClimoDatDir
byr=w2.R1ClimoByear
eyr=w2.R1ClimoEyear

nd=w2.R1ClimoNday

if(moclimo): nd=15

print 'qqqq ',w2.R1ClimoNday,nd

bdtg=dtg
if(moclimo):
    edtg=mf.dtginc(bdtg,24)
else:
    edtg=mf.dtginc(bdtg,nd*24)

print "QQQ ",bdtg,edtg

uapath='%s/ua.%s.%s.ac.365.ctl'%(ddir,byr,eyr)
vapath='%s/va.%s.%s.ac.365.ctl'%(ddir,byr,eyr)

print "QQQ ",uapath
print "QQQ ",vapath

gs=w2.R1ClimoPrc(bdtg,edtg,uapath,vapath,verb,nd)

print gs
if(gs == 0): sys.exit()

print "gs: "

gspath="/tmp/p.r1.clm.%s.gs"%(bdtg)

gsfile=open(gspath,'w')

for gg in gs:
    gg=gg+'\n'
    print gg[:-1]
    gsfile.write(gg)

gsfile.close()

cmd="grads -lbc \"run %s\" "%(gspath)
print "CCC: ",cmd
os.system(cmd)

os.system("rm %s"%gspath)


sys.exit()

