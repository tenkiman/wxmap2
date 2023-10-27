#!/usr/bin/env python

"""%s

purpose:

  generate cliper TC track forecasts

usages:

  %s dtg ops|neumann                     # single forecast
  %s all dtgb dtge ops|neumann [dt]      # range of forecasts
  
examples:

%s cur ops
"""

import os
import sys
import posix
import posixpath

import string
import glob

import TC
import TCclip

mflibdir=TC.MfLibrary

sys.path.append(mflibdir)
import mf

#
#  defaults
#

opt1=opt2=opt3=opt4=opt5='NULL'
verb=1

source='ops'

curdtg=mf.dtg()
curdir=posix.getcwd()

pyfile=sys.argv[0]

narg=len(sys.argv)-1
i=1
nargmax=3

if(narg == 0):
    nargmax=1
elif(sys.argv[1] == 'all'):
    nargmax=4
else:
    nargmax=2

if(narg >= nargmax):
    opt1=sys.argv[i] ; i=i+1
    if(mf.argopt(i)): opt2=sys.argv[i] ; i=i+1
    if(mf.argopt(i)): opt3=sys.argv[i] ; i=i+1
    if(mf.argopt(i)): opt4=sys.argv[i] ; i=i+1
    if(mf.argopt(i)): opt5=sys.argv[i] ; i=i+1
else:
    print __doc__%(pyfile,pyfile,pyfile,pyfile)
    print "The Current DTG and UTC time: ",curdtg
    sys.exit(2)

if(nargmax == 2):
    dtg=opt1
    source=opt2

    dtg=mf.cur2dtg(dtg)

    if(len(dtg) < 10):
        print "Error 1:"
        print "Invalid target dtg: ",dtg
        sys.exit(1)

elif(nargmax == 4):

    dtgb=opt2
    dtge=opt3
    source=opt4
    dtgb=mf.cur2dtg(dtgb)
    dtge=mf.cur2dtg(dtge)

    if(opt5 != 'NULL'): dt=string.atoi(opt5)


if( not(source == 'neumann' or source == 'ops') ):
    print "EEE invalid source: %s"%(source)
    sys.exit()

#
# set up the output dir
#

if(source == 'neumann'):
    clpdir=TC.FtExpDir

elif(source == 'ops'):
    clpdir=TC.FtOpsDir


#
# set single/multi runs
#

if(opt1 != 'all'):

    dtgb=dtg
    dtge=dtg
    dt=12

else:

    dt=12

print "qqq ",dtgb,dtge,dt

dtgs=mf.dtgrange(dtgb,dtge,dt)

for dtg in dtgs:

    clppath=clpdir+"/tc.clp.%s.tracks.txt"%(dtg)
    (hcards,tccards)=TCclip.MakeCliperForecast(dtg,source)
    print "RRR ",hcards
    
    if(hcards == 0): continue

    #
    #  output
    #

    o=open(clppath,'w')

    for card in hcards:
        if(verb): print card
        card=card+'\n'
        o.write(card)

    for card in tccards:
        if(verb): print card
        card=card+'\n'
        o.write(card)


sys.exit()

