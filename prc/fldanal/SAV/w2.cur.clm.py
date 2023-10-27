#!/usr/bin/env python

"""
%s

purpose:

  current wind climo processing

usages:

  %s dtg [-m model]

  -P  - no plots just .gif and .htm
  
model:
  gsm

(c) 2005 by Michael Fiorino, LLNL
"""


import os
import sys
import string
import glob
import time
import getopt
import copy

import mf
import w2
import w2env
import wxmap

w2env=w2env.W2env()

#
#  defaults
#
ropt=''
noplots=0
modopt=None

curdtg=mf.dtg()
curphr=mf.dtg('phr')
curyear=curdtg[0:4]
curtime=mf.dtg('curtime')
curdir=os.getcwd()
pyfile=sys.argv[0]

narg=len(sys.argv)-1

if(narg >= 1):

    dtgopt=sys.argv[1]
    (dtg,phr)=mf.dtg_phr_command_prc(dtgopt) 
    
    try:
        (opts, args) = getopt.getopt(sys.argv[2:], "m:LJFNVP")

    except getopt.GetoptError:
        mf.usage(__doc__,pyfile,curdtg,curtime,curphr)
        sys.exit(2)

    for o, a in opts:
        if o in ("-m",""): modopt=a
        if o in ("-N","--run"): ropt='norun'
        if o in ("-P",""): noplots=1
        if o in ("-V","--verb"): verb=1

else:
    mf.usage(__doc__,pyfile,curdtg,curtime,curphr)
    sys.exit(1)


curpid=os.getpid()

pltdir=w2.PrcDirFldanalW2
webdir=w2.PrcDirWebW2
datdir=w2.PrcDirFlddatW2

if(modopt == None):
    models=w2.w2PlotClmModels
else:
    models=[modopt]


areas=w2env.W2_AREAS_CLIMO

#cccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# 
# make the current climo
#
#cccccccccccccccccccccccccccccccccccccccccccccccccccccccc

os.chdir(datdir)
cmd="w2.r1.climo.dat.py %s"%(dtg)
mf.runcmd(cmd,ropt)

#pppppppppppppppppppppppppppppppppppppppppppppppppppppppp
#
# make plots
#
#pppppppppppppppppppppppppppppppppppppppppppppppppppppppp

os.chdir(pltdir)

pmodels=copy.copy(models)
if(noplots): pmodels=[]

for pmodel in pmodels:
    cmd="w2-plot.py %s %s -p clm"%(dtg,pmodel)
    mf.runcmd(cmd,ropt)


#llllllllllllllllllllllllllllllllllllllllllllllllllllllll
#
# loop the clm and models
#
#llllllllllllllllllllllllllllllllllllllllllllllllllllllll


os.chdir(pltdir)

plts=w2.ClimoPlots

moddelay=125
clmdelay=2*moddelay

if(noplots): plts=[]

for plt in plts:
    
    pngs={}
    for model in models:
        
        isnwp2=w2.IsModel2(model)
        if(isnwp2):
            pmodel=w2.Model2Model2PlotModel(model)
        else:
            pmodel=model
        
        gdir=w2.W2BaseDirWeb+'/'+w2.W2ModelPltDir(pmodel)
        for area in areas:
            png="%s/%s/%s.clm.%s.%s.%s.mod.png"%(gdir,dtg,pmodel,plt,dtg,area)
            try:
                pngs[area].append(png)
            except:
                pngs[area]=[]
                pngs[area].append(png)
                

    for model in models:

        isnwp2=w2.IsModel2(model)
        if(isnwp2):
            pmodel=w2.Model2Model2PlotModel(model)
        else:
            pmodel=model

        for area in areas:
            
            print 'mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm ',pmodel,plt,area
            gdir=w2.W2BaseDirWeb+'/'+w2.W2ModelPltDir(pmodel)
            cpng="%s/%s/%s.clm.%s.%s.%s.clm.png"%(gdir,dtg,pmodel,plt,dtg,area)
            ccmd="convert -loop 0 -delay %d %s"%(clmdelay,cpng)
            
            allpngs=pngs[area]
            for png in allpngs:
                ccmd="%s -delay %s %s"%(ccmd,moddelay,png)
            lcmd=ccmd
            loopgif="%s/%s/%s.clm.%s.%s.%s.loop.gif"%(gdir,dtg,pmodel,plt,dtg,area)
            lcmd="%s %s"%(lcmd,loopgif)
            mf.runcmd(lcmd,ropt)

#hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh
#
# make the html
#
#hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh

hdir=w2.wxhWebClm

nareas=len(areas)

for n in range(nareas):
    area=areas[n]
    nother=n+1
    if(nother > nareas-1): nother=n-1
    otherarea=areas[nother]
    hpath="%s/wx.clm.cur.%s.htm"%(hdir,area)
    print 'HHH hpath ',hpath
    wxmap.HtmlCurClimo(dtg,hpath,area,otherarea)


sys.exit()


