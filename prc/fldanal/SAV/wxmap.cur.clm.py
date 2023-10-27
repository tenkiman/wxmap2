#!/usr/bin/env python

"""
%s

purpose:

  current wind climo processing

usages:

  %s dtg [-m model]
  
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

import mf

import wxmap

#
#  defaults
#
ropt=''

models=['avn','ngp']

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
        (opts, args) = getopt.getopt(sys.argv[2:], "m:LJFNV")

    except getopt.GetoptError:
        mf.usage(__doc__,pyfile,curdtg,curtime,curphr)
        sys.exit(2)

    for o, a in opts:
        if o in ("-m",""): models=[a]
        if o in ("-N","--run"): ropt='norun'
        if o in ("-V","--verb"): verb=1

else:
    mf.usage(__doc__,pyfile,curdtg,curtime,curphr)
    sys.exit(1)


curpid=os.getpid()

pwdir=wxmap.wxpdWxmap
phdir=wxmap.wxpdHtml
pddir=wxmap.wxpdDat

print models

#cccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# 
# make the current climo
#
#cccccccccccccccccccccccccccccccccccccccccccccccccccccccc

os.chdir(pddir)
cmd="wxmap.r1.climo.dat.py %s"%(dtg)
mf.runcmd(cmd,ropt)

#pppppppppppppppppppppppppppppppppppppppppppppppppppppppp
#
# make plots
#
#pppppppppppppppppppppppppppppppppppppppppppppppppppppppp

os.chdir(pwdir)

for model in models:
    cmd="wxmap.plot.clm.pl %s %s"%(dtg,model)
    mf.runcmd(cmd,ropt)


#llllllllllllllllllllllllllllllllllllllllllllllllllllllll
#
# loop the clm and models
#
#llllllllllllllllllllllllllllllllllllllllllllllllllllllll

os.chdir(pwdir)

plts=wxmap.ClimoPlots

moddelay=125
clmdelay=2*moddelay

for plt in plts:
    
    pngs=[]
    for model in models:
        gdir=wxmap.ModelGrfDir(model,dtg)
        png="%s/%s.clm.%s.%s.mod.png"%(gdir,model,plt,dtg)
        pngs.append(png)


    for model in models:
        print 'mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm ',model,plt
        gdir=wxmap.ModelGrfDir(model,dtg)
        cpng="%s/%s.clm.%s.%s.clm.png"%(gdir,model,plt,dtg)
        ccmd="convert -loop 0 -delay %d %s"%(clmdelay,cpng)
        for png in pngs:
            ccmd="%s -delay %s %s"%(ccmd,moddelay,png)
        lcmd=ccmd
        loopgif="%s/%s.clm.%s.%s.loop.gif"%(gdir,model,plt,dtg)
        lcmd="%s %s"%(lcmd,loopgif)
        mf.runcmd(lcmd,ropt)

#hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh
#
# make the html
#
#hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh

hdir=wxmap.wxhWebClm
hpath="%s/wx.clm.cur.htm"%(hdir)


wxmap.HtmlCurClimo(dtg,hpath)


sys.exit()


