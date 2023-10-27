#!/usr/bin/env python

"""
%s

purpose:

usages:

  %s bdtg[.edtg[.ddtg]] model

models:
  ecm | ngp | gfs | ukm | cmc | all

-N  -- norun
-O  -- override=1 (force plot)
-I  -- interact
-T  -- test (no rm of .gs)

examples:

 %s cur-12 ngp -t 0 -a tropsio -p prp -O -I  | interactively create tau0 prp plot for tropsio and overwrite (-O disable exist check)
 
(c) 2009 Michael Fiorino
"""

import os
import sys
import string
import glob
import time
import getopt

import mf
import M2
import grads


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
verb=0

plotopt='all'
tauopt='all'
areaopt='all'

override=0
interact=0
dotest=0
doforce=0
donocagips=0
doregen=0
test=0

narg=len(sys.argv)-1

if(narg >= 2 and not(test)):

    dtgopt=sys.argv[1]
    modelopt=sys.argv[2]
    
    try:
        (opts, args) = getopt.getopt(sys.argv[3:], "m:a:p:t:DNVGOITFkR")

    except getopt.GetoptError:
        mf.usage(__doc__,pyfile,curdtg,curtime,curphr)
        sys.exit(2)

    for o, a in opts:
        if o in ("-a",""): areaopt=a
        if o in ("-p",""): plotopt=a
        if o in ("-t",""): tauopt=a
        if o in ("-N",""): ropt='norun'
        if o in ("-F",""): doforce=1
        if o in ("-V",""): verb=1
        if o in ("-O",""): override=1
        if o in ("-G",""): dogribmap=1
        if o in ("-I",""): interact=1
        if o in ("-T",""): dotest=1
        if o in ("-k",""): donocagips=1
        if o in ("-R",""): doregen=1

elif(not(test)):
    mf.usage(__doc__,pyfile,curdtg,curtime,curphr)
    sys.exit(1)


#llllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll
#
# local 
#

def makeprwexpr(pvar,blon,elon,blat,elat):
    expr="aave(%s,lon=%f,lon=%f,lat=%f,lat=%f)"%(pvar,blon,elon,blat,elat)
    return(expr)

def setcline(ccol,csty,cthk):
    ga("set cmark 0")
    ga("set cstyle %d"%(csty))
    ga("set cthick %d"%(cthk))
    ga("set ccolor %d"%(ccol))





#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
# main
#


if(test):
    dtgopt='cur-18'
    modelopt='gfs2'
    
curpid=os.getpid()

if(dtgopt == None):
    print 'EEE must set the dtg opt ...'
    sys.exit()

dtgs=mf.dtg_dtgopt_prc(dtgopt)
model=modelopt

m2=M2.Model2()
ga=grads.GaNum(Bin='grads2',Window=1)

donwp2=m2.IsModel2(model)

if(not(donwp2)): sys.exit()

dtg=dtgs[0]

models=['gfs2','fim8','geo05']
fhs=[]

for model in models:
    (dpath,dthere)=m2.DataPath(model,dtg)
    print 'dpath    : ',dpath
    print 'dthere   : ',dthere

    if(dthere):
        fh=ga.open(dpath)
        fhs.append(fh)
    

sys.exit()

dtg='2009031912'
gfspath='/w21/dat/nwp2/ncep/gfs2/%s/gfs2.%s.ctl'%(dtg,dtg)
fimpath='/w21/dat/nwp2/esrl/fim8/%s/fim8.%s.ctl'%(dtg,dtg)
geopath='/w21/dat/geog/lf.gfs.05deg.ctl'


fhfim=ga.open(fimpath)
fhgfs=ga.open(gfspath)
fhgeo=ga.open(geopath)

ga('set grads off')
ga('lm=lf.3(t=1)')
ga('lm=maskout(lm,lm-0.5)')
ga('set gxout shaded')
ga('d maskout(prw,lm)')
ga('cbarn')
ga("draw title gfs prw `3t`0=0 %s\using gfs 0.5 deg land-sea fraction"%(dtg))
ga("print /tmp/prw.eps")
ga("gxyat /tmp/prw.pdf")

ga('q pos')
ga('c')

cde=ga.query('dims')
btime=cde.time[0]

mf.gtime2dtg(btime)

fchr=144
bdtg=mf.gtime2dtg(btime)
edtg=mf.dtginc(bdtg,fchr)

etime=mf.dtg2gtime(edtg)
ga('set time %s %s'%(btime,etime))
ga('set y 1')
ga('set lon 0 360')
ga('set x 1')
ga('set yflip on')

blat=-30.0
elat= 15.0
blon=-120.0
elon= -30.0

blong=blon
elong=elon
if(blong < 0): blong=blong+360.0
if(elong < 0): elong=elong+360.0

pvargfs="maskout(prw.1,lm)"
pvarfim="maskout(prw.2,lm)"

e1=makeprwexpr(pvargfs,blong,elong,blat,elat)
e2=makeprwexpr(pvarfim,blong,elong,blat,elat)

ga("ptg=%s"%(e1))
ga("ptf=%s"%(e2))

np1=ga.exp('ptg')
np2=ga.exp('ptf')

np1max=np1.max()
np1min=np1.min()

np2max=np2.max()
np2min=np2.min()

pmax=np1max
if(np2max > pmax): pmax=np2max

pmin=np1min
if(np2min < pmin): pmin=np2min

dp=(pmax-pmin)*0.40

ga('c')
ga('set grads off')

ga("set vrange %f %f"%(pmin-dp,pmax+dp))
setcline(3,1,10)
ga('d ptg')
    
setcline(2,1,10)
ga('d ptf')

(clatb,clonb,ilat,ilon,ihemns,jhemns)=TC.Rlatlon2Clatlon(blat,blon,dotens=0)
(clate,clone,ilat,ilon,ihemns,jhemns)=TC.Rlatlon2Clatlon(elat,elon,dotens=0)

model1='GFS'
model2='FIM2'
ga("draw title %s prw %s(green) v %s(red) [LAND ONLY] \lon[%s <-> %s] lat[%s <-> %s]"%(dtg,model1,model2,
                                                                                       clonb,clone,clatb,clate))

ga('q pos')

ga('print /tmp/ts.eps')







