#!/usr/bin/env python

"""
%s

purpose:

  rename wxmap1 fields from jtwc to wxmap2 names

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
import w2
import w2env

#
#  defaults
#
ropt=''

model='avn'

curdtg=mf.dtg()
curphr=mf.dtg('phr')
curyear=curdtg[0:4]
curtime=mf.dtg('curtime')
curdir=os.getcwd()
pyfile=sys.argv[0]

curpid=os.getpid()
prcopt='get'

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
        if o in ("-m",""): model=a
        if o in ("-N","--run"): ropt='norun'
        if o in ("-V","--verb"): verb=1

else:
    mf.usage(__doc__,pyfile,curdtg,curtime,curphr)
    sys.exit(1)


(ftpserver,remotedir,sdir,
 mask,renmask,modelrename)=w2.ModelArchiveDirs(model,dtg,center='jtwc')

tdir=w2.NwpDataBdir(modelrename)

print 'FFFFF          model: ',model
print 'FFFFF      ftpserver: ',ftpserver
print 'FFFFF       sdir: ',sdir
print 'FFFFF       tdir: ',tdir
print 'FFFFF           mask: ',mask
print 'FFFFF        renmask: ',renmask
print 'FFFFF    modelrename: ',modelrename

if(ropt=='norun'): sys.exit()


#
# rename avn -> gfs
#
def ModelRenameNewPath(path,modelrename):

    if(mf.find(path,'.bak')):
        opath=npath=nmask=oldext=None
    else:
        (dir,file)=os.path.split(path)
        (base,oldext)=os.path.splitext(file)

        if(modelrename != None):
            oname=file
            nname=modelrename+oname[len(model):]
            opath="%s/%s"%(sdir,oname)
            npath="%s/%s"%(tdir,nname)
            nmask="%s/%s*"%(tdir,nname[0:len(nname)-4])
        else:
            oname=file
            nname=oname
            opath="%s/%s"%(sdir,oname)
            npath="%s/%s"%(sdir,nname)
            nmask="%s/%s*"%(sdir,nname[0:len(nname)-4])

    return(opath,npath,nmask,oldext)

if(modelrename != None):

    paths=glob.glob("%s/%s"%(sdir,mask))
    print 'qqqq mask',mask
    for path in paths:

        (opath,npath,nmask,oldext)=ModelRenameNewPath(path,modelrename)

        print 'qqqq opath',opath
        print 'qqqq npath',npath

        ropt='norun'
        if(oldext == '.ctl'):
            cmd="replace.pl '%s.' '%s.' %s"%(model,modelrename,opath)
            mf.runcmd(cmd,ropt)

            bakpath="%s.bak"%(path)
            if(os.path.exists(bakpath)):
                cmd="rm %s"%(bakpath)
                mf.runcmd(cmd,ropt)


        cmd="mv %s %s"%(opath,npath)
        mf.runcmd(cmd,ropt)




sys.exit()











pltdir=w2.PrcDirFldanalW2
webdir=w2.PrcDirWebW2
datdir=w2.PrcDirFlddatW2

print models

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

for model in models:
    cmd="wxmap.plot.clm.pl %s %s"%(dtg,model)
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

for plt in plts:
    
    pngs=[]
    for model in models:
        gdir=w2.W2ModelPltDir(model)
        png="%s/%s.clm.%s.%s.mod.png"%(gdir,model,plt,dtg)
        pngs.append(png)


    for model in models:
        print 'mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm ',model,plt
        gdir=w2.W2ModelPltDir(model)
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

hdir=w2.wxhWebClm
hpath="%s/wx.clm.cur.htm"%(hdir)


wxmap.HtmlCurClimo(dtg,hpath)


sys.exit()


