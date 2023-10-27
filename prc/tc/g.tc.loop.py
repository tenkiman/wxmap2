#!/usr/bin/env python

"""%s

purpose:

usages:

  %s -d edtg.bdtg.ddtg -m model -p plotopt -a areaopt

-N norun
-V verb
-F plus hours
-D delayloop (ms)
examples:

%s -d cur.cur-d5.12 -m avn -p uas -F 72 -D 50
%s -d cur-6.edtg-d5.6 -m avn -p w20 -a wconus -F 120
"""

import os
import sys
import getopt

import string
import glob

import mf
import w2

#
#  defaults
#
bdtg=None
edtg=None
dtgopt=None
plotopt=None
areaopt=None
fcstopt=None
delayopt=None

tau='000'
ddtg=24

ropt=''

verb=0

curdtg=mf.dtg()
curtime=mf.dtg('curtime')
curphr=mf.dtg('phr')
cyear=curdtg[0:4]
curdir=os.getcwd()

pyfile=sys.argv[0]

narg=len(sys.argv)-1

#
# options using getopt
#

if(narg > 0):


    try:
        (opts, args) = getopt.getopt(sys.argv[1:], "d:m:p:a:F:D:NV")

    except getopt.GetoptError:
        mf.usage(__doc__,pyfile,curdtg,curtime)
        sys.exit(2)

    for o, a in opts:
        if o in ("-d",""): dtgopt=a
        if o in ("-m",""): modelopt=a
        if o in ("-p",""): plotopt=a
        if o in ("-a",""): areaopt=a
        if o in ("-N",""): ropt='norun'
        if o in ("-F",""): fcstopt=a
        if o in ("-D",""): delayopt=a
        if o in ("-V",""): verb=1

else:
    mf.usage(__doc__,pyfile,curdtg,curtime,curphr)
    sys.exit(1)


if(not(modelopt and plotopt and dtgopt and areaopt)):
    print 'EEEE must set -d edtg.bdtg.ddtg -m model -p plot -a area'
    sys.exit()



#
# dtg options
#

tt=dtgopt.split('.')
if(len(tt) >= 2):
    edtg=tt[0]
    bdtg=tt[1]
else:
    print "EEE dtgopt must be in form -d bdtg.edtg[.ddtg]"
    sys.exit()
    
if(len(tt) == 3):
    ddtg=tt[2]

print edtg
edtg=mf.dtg_command_prc(edtg)

print 'eee ',bdtg
if(mf.find(bdtg,'edtg')):
    try:
        dd=bdtg.split('-')[1]
    except:
        print 'EEE improper form for edtg-dNNN where NNN is number of days back ...'
        sys.exit()

    if(dd[0] == 'd'):
        nhback=int(dd[1:len(dd)+1])*(-24)

    bdtg=mf.dtginc(edtg,nhback)
    print 'adfasdf',dd,nhback,edtg,bdtg
else:
    bdtg=mf.dtg_command_prc(bdtg)

#
# fcstopt
#

edtg0=edtg
if(fcstopt):
    plustau=int(fcstopt)
    edtg=mf.dtginc(edtg0,plustau)

dtgs=mf.dtgrange(bdtg,edtg,ddtg)

#
# delayopt
#
if(delayopt):
    delayloop=int(delayopt)
else:
    delayloop=75

delayfracfc=1.75
delayloopfc=int(float(delayloop)*delayfracfc)

delaypause=delayloop*3

#
# model options
#

tt=modelopt.split('.')

if(len(tt) == 1):
    model=tt[0]
else:
    print "EEE single model only your modelopt=",modelopt
    sys.exit()



gdir=w2.ModelWxmap1GrfDir(model)
res=w2.ModelResGrf(model)

print 'gdir ',gdir

convertexe='/pcmdi/tenki_opt/linux/bin/convert'


tdir='/tmp'


ndtgs=len(dtgs)
np=0
print len(dtgs)


ppaths=[]


taumin=999.0
taumax=-999.0
nplots=0

for dtg in dtgs:

    tau=mf.dtgdiff(edtg0,dtg)
    ctau="%03d"%(int(tau))

    if(tau >= taumax): taumax=tau
    if(tau <= taumin): taumin=tau

    if(tau > 0.0):
        pdir="%s/archive/%s"%(gdir,edtg0)
        ppath="%s/%s%s.%s.%s.%s.png"%(pdir,model,res,plotopt,ctau,areaopt)
        if(not(os.path.exists(ppath))):
            ppath="%s/%s%s.%s.%s.%s.gif"%(pdir,model,res,plotopt,ctau,areaopt)
        
    else:
        ctau='000'
        pdir="%s/archive/%s"%(gdir,dtg)
        ppath="%s/%s%s.%s.%s.%s.png"%(pdir,model,res,plotopt,ctau,areaopt)
        if(not(os.path.exists(ppath))):
            ppath="%s/%s%s.%s.%s.%s.gif"%(pdir,model,res,plotopt,ctau,areaopt)
            


    print ctau,ppath

    if(os.path.exists(ppath)):
        ppaths.append((ppath,tau))
        print dtg,ppath
        nplots=nplots+1

print taumin,taumax,nplots
ctaumin="T-%03.0f"%(abs(taumin))
ctaumax="T+%03.0f"%(abs(taumax))

tgifpath="%s/%s%s.000.%s.%s.%s.%s.%s.anal.fcst.loop.gif"%(tdir,model,res,plotopt,areaopt,edtg0,ctaumin,ctaumax)

np=0

for ppath in ppaths:

    path=ppath[0]
    tau=ppath[1]
    
    if(np == 0):
        ccmd="%s -loop 0 -delay %s %s"%(convertexe,delaypause,path)
    elif(np == nplots-1 or tau == 0.0):
        ccmd="%s -delay %s %s"%(ccmd,delaypause,path)
    elif( (tau >= 0.0) and (np != nplots-1) ):
        ccmd="%s -delay %s %s"%(ccmd,delayloopfc,path)
    else:
        ccmd="%s -delay %s %s"%(ccmd,delayloop,path)

    np=np+1
    

print np
ccmd="%s %s"%(ccmd,tgifpath)
mf.runcmd(ccmd,ropt)



