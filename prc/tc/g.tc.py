#!/usr/bin/env python

"""%s

purpose:

usages:

  %s  VVV (verifile) -s SSS.YYYY (stmid) -m MMM (Model)

  -P prodopt
  -I interactive mode
  
examples:
%s ops.2004.shem -s 04S.2004 -m ukm
"""

import os
import sys
import posix
import posixpath
import getopt

import string
import glob

from time import sleep
import TCw2 as TC


mflibdir=TC.MfLibrary

sys.path.append(mflibdir)
import mf


convertexe='/pcmdi/tenki_opt/linux/bin/convert'


#
#  defaults
#

stmopt=None
veriname=None
modelopt=None
taumax=120
hhopt='00_12'
hhopt='all'
interact=None

popt='ops'
batchopt=None
prodopt=None

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

    veriname=sys.argv[1]

    try:
        (opts, args) = getopt.getopt(sys.argv[2:], "s:m:p:v:BNPIV")

    except getopt.GetoptError:
        mf.usage(__doc__,pyfile,curdtg,curtime)
        print "EEE invalid getopt opt"
        sys.exit(2)

    for o, a in opts:
        if o in ("-s","--vopt"): stmopt=a
        if o in ("-m","--vopt"): modelopt=a
        if o in ("-p","--vopt"): popt=a
        if o in ("-B","--vopt"): batchopt=1
        if o in ("-P","--vopt"): prodopt=1
        if o in ("-N","--vopt"): ropt='norun'
        if o in ("-I","--vopt"): interact=1
        if o in ("-V",""): verb=1

else:
    mf.usage(__doc__,pyfile,curdtg,curtime)
    sys.exit(1)

if(not(veriname) or not(stmopt) or not(modelopt)):
    print "EEE run using -v veriname -s stmopt -m model"
    sys.exit()

try:
    (tstmid,tyear)=stmopt.split('.')
except:
    print "EEE unable to split stmopt use -s SSS.YYYY"
    sys.exit()

tmodel=modelopt

tt=veriname.split('.')
if( (len(tt) == 3) and (tt[0] == 'ops') ):
    opsyear=tt[1]
    opshemi=tt[2]
else:
    opsyear=None
    opshemi=None

tcnames=TC.GetTCnamesHash(tyear)
tcstats=TC.GetTCstatsHash(tyear)

btdir=TC.BtDir
mddir=TC.MdeckDir
ftdir=TC.FcOpsDir
vddir=TC.VdeckDir

veridir=TC.VeriDir
pltdir=TC.PltOpsTrackDir

if(opsyear and opshemi):
    pltdir="%s/%s.%s"%(pltdir,opsyear,opshemi)
    print 'pp ',pltdir
    if(not(os.path.isdir(pltdir))):
        try:
            os.mkdir(pltdir)
            print 'DDDDDD made: ',pltdir
        except:
            print "EEE unable to mkdir: "%(pltdir)
            sys.exit()
    
bid=tstmid[2:3]
bname=TC.Basin1toBasin3[bid]
mdmask="%s/%s/MD.%s.%s.%s.*.txt"%(mddir,tyear,bname,tyear,tstmid)
mdpaths=glob.glob(mdmask)
print mdmask
if(len(mdpaths) == 0):
    print 'EEE no bts for mdmask: ',mdmask
    sys.exit()
else:
    mdpath=mdpaths[0]
    
vimask="%s/%s/vdeck.%s.%s.%s.%s.*txt"%(vddir,tyear,bname,tyear,tstmid,tmodel)
vipaths=glob.glob(vimask)
if(len(vipaths) == 0):
    print 'EEE no vdeck for vimask: ',vimask
    sys.exit()
else:
    vipath=vipaths[0]

ftgpath="/tmp/g.w2.tc.fc.txt"
pystat="TCfcStat"
verirule='jtwc.hetero'
#verirule='jtwc.mod.hetero'

#
#  synoptic time and last veri tau
#

synopt='syn00_12'

if(bid == 'P' or bid == 'S'):
    opt3='48veri'
    taufcveristat='48'
else:
    opt3='72veri'
    taufcveristat='72'


stipath="%s/tc.veri.sum.%s.%s.py"%(veridir,veriname,verirule)
vpath="%s/tc.veri.%s.tc.ctl"%(vddir,tyear);


if(not(os.path.exists(stipath))):
    print "EEE  stipath: %s does not exist"%(stipath)
    sys.exit()
else:
    cmd="cp %s %s.py"%(stipath,pystat)
    mf.runcmd(cmd)
    from TCfcStat import tcfc


try:
    tstmname=tcnames[tyear,tstmid]
except:
    tstmname='NoName'

try:
    tstmstat=tcstats[tyear,tstmid]
    tstmtype=tstmstat[0]
except:
    tstmtype='TC'
    print "EEEEEEEEEEEEEEEE problem with tcstats: %s %s"%(tyear,tstmid)
    for tcstat in tcstats:
        print 'qqq ',tcstat
    print tcstats[tyear,tstmid]
    sys.exit()

try:
    tcfcstat=tcfc[tyear,tstmid]
except:
    tcfcstat=None

tstmtype=tstmtype.strip()

TC.TcFcStatLegend(tcfcstat,tmodel,bid,taufcveristat,verb=0)
    

if(verb):
    print "TTT     tstmid:  %s"%(tstmid)
    print "TTT   tstmtype:  %s"%(tstmtype)
    print "TTT   tcfcstat: ",tcfcstat
    
    print "DDD      mddir:  %s"%(mddir)
    print "DDD      ftdir:  %s"%(ftdir)
    print "DDD      vddir:  %s"%(vddir)

    print "PPP     mdpath:  %s"%(mdpath)
    print "PPP     vipath:  %s"%(vipath)
    
#
# grep out to speed up get model fc tracks
#

cards=open(vipath).readlines()

#for card in cards:
#    print card
#sys.exit()
#cmd="grep -h -s %s %s | grep %s > %s"%(stmopt,vipath,tmodel,ftipath)
#mf.runcmd(cmd,ropt)
#cards=open(ftipath).readlines()

tcs={}
dtgs=[]

for c in cards:
    (model,tau,sid,snum,sbasin,bdtg,vdtg,flat,flon,blat,blon,
     fe,bvmax,fvmax,cte,ate,fve,fveu)=TC.vcparse(c)
    stmid=sid.split('.')[0]
    stmyyyy=sid.split('.')[1]
    if(model == tmodel and stmid == tstmid and stmyyyy == tyear):
        #print 'qqqqqqqqqqqqqqqq ', model,tmodel,tau,bdtg,sid,stmid,tstmid,stmyyyy,flat,flon
        dtgs.append(bdtg)
        try:
            tcs[bdtg].append([model,tau,flat,flon,fvmax,fe])
        except:
            tcs[bdtg]=[]
            tcs[bdtg].append([model,tau,flat,flon,fvmax,fe])


if(len(dtgs) == 0):
    print "WWWWWWWW no forecasts for: %s and storm: %s"%(tmodel,tstmid)
    ###sys.exit()

else:
    dtgs=mf.uniq(dtgs)

O=open(ftgpath,'w')

#
# check the which cycle JT is running in SHEM
#

if( (bid == 'P' or bid == 'S') and tmodel == 'ofc'):
    cnt00=0
    cnt06=0
    for dtg in dtgs:
        shour=dtg[8:]
        for t in tcs[dtg]:
            tau=t[1]
            if(tau == '000'):
                lat=float(t[2])
                if((shour == '00' or shour == '12') and lat > -80.0): cnt00=cnt00+1
                if((shour == '06' or shour == '18') and lat > -80.0): cnt06=cnt06+1
                
    print 'cccc 0000 ',cnt00
    print 'cccc 6666 ',cnt06

    if(cnt06 > cnt00): synopt='syn06_18'


if(synopt == 'syn00_12'):
    synhours=['00','12']
elif(synopt == 'syn06_18'):
    synhours=['06','18']

#
# set opt2 as synopt to g.tc.gs
#
opt2=synopt

for dtg in dtgs:
    csynhour=dtg[8:]
    
    doit=0
    for synhour in synhours:
        if(csynhour == synhour): doit=1

    if(not(doit)): continue

    card="%s %s ::"%(tmodel,dtg)
    n=0
    ltcs=len(tcs[dtg])
    for t in tcs[dtg]:
        (m,tau,lat,lon,vmax,fe)=t
        if(lat < 90.0 and int(tau) <= taumax and lat != -88.8):
            card="%s %s %5.1f %5.1f %s %5.0f"%(card,tau,lat,lon,vmax,fe)
            if(n != ltcs-1):
                card="%s :"%(card)
        
        n=n+1
        #print dtg,tau

    scard=card[0:len(card)-1]
    O.writelines(scard+'\n')

O.close()

siz=os.path.getsize(ftgpath)
print 'sssssssssssss ',siz
#
# if no tracks to plot,
#

plot='y'
vtype='hetero'
ptype='batch'
opt='null'
xsize='1024x768'
xsize='800x600'
vmodel=tmodel
nstorm=tstmid[0:2]
opt1="%s %s %s"%('name',tstmtype,tstmname)
nbasin=TC.Basin1toBasinNumber[bid]

gclinput="%s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s"%\
          (ptype,mdpath,ftgpath,vpath,pltdir,plot,vmodel,tstmid,nstorm,nbasin,veriname,vtype,bname,tyear,
           opt1,opt2,opt3)

gradsexe='grads'
if(prodopt):
    gradsopt='-lbc'
else:
    gradsopt='-lc'


looppath="%s/tc.trk.%s.%s.%s.%s.%s.loop.gif"%(pltdir,vmodel,tyear,tstmid,tstmname,tstmtype)
#tc.trk.ofc.2005.22P.INGRID.STY.png

cmd="rm /tmp/tc.fc.??.*"
mf.runcmd(cmd,ropt)

cmd="%s %s \"run g.tc.gs %s\" -g %s"%(gradsexe,gradsopt,gclinput,xsize)
mf.runcmd(cmd,ropt)

loopmask="/tmp/tc.fc.??.png"
pngs=glob.glob(loopmask)

delayloop=50
delaylast=200

n=1
npngs=len(pngs)
for png in pngs:

    if(n == 1):
        cmd="%s -loop 0 -delay %s /tmp/tc.fc.%02d.png "%(convertexe,delayloop,n)
    elif(n == npngs):
        cmd="%s -delay %s /tmp/tc.fc.%02d.png "%(cmd,delaylast,n)
    else:
        cmd="%s -delay %s /tmp/tc.fc.%02d.png "%(cmd,delayloop,n)
    n=n+1

cmd="%s %s"%(cmd,looppath)
mf.runcmd(cmd,ropt)


sys.exit()

