#!/usr/bin/env python 

"""%s:
purpose:

  master script for running TC struct application

usages:

  %s YYYYmmddhh (cur, cur-NNN, cur+NNN) | {avn;ukm;ngp;gsm;ngp.npmoc.ldm;all | tc.ls | tc.db} | [popt = ls.tc]

  -C  -- clean dir before processing
  -c  -- NO cagips for ngp
  -R  -- realtime=1
  -T  -- do tracker only
  -s  -- stmidset = stmopt
  -O  -- override=1 -- force field data
  -P  -- dopostprocess=1 -- default is to do the vdeck, adeck, con postprocessing in w2.tc.tcanal.py
  
examples:

%s cur ngp
%s cur ngp.npmoc.ldm
%s cur tc.ls -- list TCs to do struct anal
"""
import sys
import os
import glob
import string
import getopt

import mf
import w2
import TCw2 as TC
import TCveri as TCV
import ATCF
import tcbase as tc2

from tcanalsub import * 


curdtg=mf.dtg()
curphr=mf.dtg('phr')
curtime=mf.dtg('curtime')

curdir=os.getcwd()

curdtg=mf.dtg()
curphr=mf.dtg('phr')
curyear=curdtg[0:4]
curtime=mf.dtg('curtime')

pypath=sys.argv[0]
(pydir,pyfile)=os.path.split(pypath)


#
# blow off dir by default, not good if doing multiply models....
#

stmidset='all'
popt='all'
popt2='all'
docycling=0
donocagips=0
verb=0
doclean=0
ropt=''
specopt=''
realtime=0
dosfctrk=0
dotrackeronly=0
override=0
dopostprocess=0
dorsyncweb=1
docpreftrk=1

narg=len(sys.argv)-1

if(narg >= 2):

    dtgopt=sys.argv[1]
    model=sys.argv[2]

    try:
        (opts, args) = getopt.getopt(sys.argv[3:], "p:VNCcRSTNs:OP")

    except getopt.GetoptError:
        mf.usage(__doc__,pyfile,curdtg,curtime,curphr)
        print "EEE invalid getopt opt: ",opts,args
        sys.exit(2)

    for o, a in opts:
        if o in ("-p",""): popt=a
        if o in ("-V",""): verb=1
        if o in ("-N",""): ropt='norun'
        if o in ("-C",""): doclean=1
        if o in ("-c",""): donocagips=1
        if o in ("-R",""): realtime=1
        if o in ("-S",""): dosfctrk=1
        if o in ("-T",""): dotrackeronly=1
        if o in ("-s",""): stmidset=a
        if o in ("-O",""): override=1
        if o in ("-P",""): dopostprocess=1
        if o in ("-w",""): dorsyncweb=0

else:
    mf.usage(__doc__,pyfile,curdtg,curtime)
    sys.exit(1)


if(stmidset != 'all'):
    stmidset=TCV.MakeStmList(stmidset)[0]


dd=dtgopt.split('.')
ddtg=6
if(len(dd) == 1):
    bdtg=mf.dtg_command_prc(dtgopt)
    edtg=bdtg
    dtg=bdtg

if(len(dd) >= 2):
    bdtg=mf.dtg_command_prc(dd[0])
    edtg=mf.dtg_command_prc(dd[1])

if(len(dd) == 3):
    ddtg=dd[2]

dtgs=mf.dtgrange(bdtg,edtg,ddtg)

if(len(dtgs) == 1):
    dtg=bdtg
else:
    docycling=1

#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
# main loop
#


#
# directories
#
cdirnhc=w2.TcAdecksNhcDir
prcddir=w2.PrcDirTcdatW2
prcadir=w2.PrcDirTcanalW2

#
# change to prc dir
#

mf.ChangeDir(prcadir)

#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
#
#  cycle through models  -- new common code to set models by syn hour
#
#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc


if(model == 'all' and docycling == 0 ):

    models=SetModels(dtg,'all')
    
    for model in models:
        cmd="%s %s %s"%(pypath,dtg,model)
        for o,a in opts:
            cmd="%s %s %s"%(cmd,o,a)
        print "Cycling Models MMM: ",cmd
        mf.runcmd(cmd,ropt)

    sys.exit()


#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
#
#  cycle through dtgs
#
#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc


if(docycling):

    modelopt=model

    for dtg in dtgs:

        if(modelopt == 'all'):
            models=SetModels(dtg,'all')
        else:
            models=[modelopt]

        for model in models:

            cmd="%s %s %s"%(pypath,dtg,model)
            for o,a in opts:
                cmd="%s %s %s"%(cmd,o,a)
                print "Cycling CCC: ",cmd

            mf.runcmd(cmd,ropt)


    sys.exit()



#----------------------------------------------------------------------
# command line ops
#----------------------------------------------------------------------

if(narg == 2 and ( model == 'tc.db' or model == 'tc.ls') ):
    popt=model


#
# 20041026 -- check if using npmoc.ldm data for nogaps
#

#
# chk if doing ngp from cagips...
#
if(model != 'tc.db' and model != 'tc.ls' and not(w2.IsModel2(model))):
    dongpcagips=w2.IsNogapsCagips(model,dtg)


if(donocagips):
    dongpcagips=0

omodel=model
if(model == 'ngp.npmoc.ldm'):
    model='ngp'
    omodel='ngp'
    specopt='npmoc.ldm'

elif(model == 'ngp' and dongpcagips):
    specopt='cagips'

elif(model == 'ukm.jtwc'):
    omodel='ukm'
    
elif(model == 'gfs.jtwc'):
    omodel='gfs'


amodel=model
#if(w2.IsModel2(model)): amodel=model[0:3]

#tttttttttttttttttttttttttttttttttttttttttttttttttt
#
# do tracker only
#

#if(w2.IsModel2(model)):
#    print 'WWWWWWWWWWWWWWW dotrackeronly for 2222222222 model: ',model
#    dotrackeronly=1


if(not(popt == 'tc.ls' or popt == 'tc.db') and popt != 'all' and len(popt) != 3):
    print "EEE invalid popt: %s"%(popt)
    sys.exit(0)

if(popt != 'tc.ls' and popt != 'all' and len(popt) == 3):
    stmidset=popt


if(popt2 != 'tc.ls'): popt2=''



#----------------------------------------------------------------------
# do opt
#----------------------------------------------------------------------

docarqfiles=0
doflds=0
doobsctl=0
dotcsapp=0
dobmapplt=0
dofldplt=0
domapplt=0
doprofileplt=1

doall=0
doall=1

if(doall):
    docarqfiles=1
    doflds=1
    doobsctl=1
    dotcsapp=1
    dobmapplt=1
    domapplt=1
    dofldplt=1
    doprofileplt=1

#----------------------------------------------------------------------
# basic params
#----------------------------------------------------------------------

yyyy=dtg[0:4]

xsize=900
xsize=1024
ysize=float(xsize)*0.75
ysize=int(ysize)

xgrads='grads2'
#xgrads='grads'

gradsopt='-lc'
gradsopt='-lbc'


(cdir,bdir,prcddir,\
 odir,ogdir,osdir,otdir,oddir,opdir,\
 oadir,pdir,\
 wpddir,wgddir)=SetTcanalDirs(dtg,realtime)



#
# check if output dir and output plt stat dir are there; if not mkdir
#

doclean=0
if(doclean and os.path.isdir(odir)):
    print 'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW blowing off: ',odir
    cmd="rm -r %s"%(odir)
    mf.runcmd(cmd,ropt)

if not(os.path.isdir(odir)):
    print "odir: ",odir," is not there -- mkdir"
    os.mkdir(odir)
                                                                                          
if not(os.path.isdir(ogdir)):
    print "ogdir: ",ogdir," is not there -- mkdir"
    os.mkdir(ogdir)

if not(os.path.isdir(osdir)):
    print "osdir: ",osdir," is not there -- mkdir"
    os.mkdir(osdir)

if not(os.path.isdir(otdir)):
    print "otdir: ",otdir," is not there -- mkdir"
    os.mkdir(otdir)

if not(os.path.isdir(oddir)):
    print "oddir: ",oddir," is not there -- mkdir"
    os.mkdir(oddir)

if not(os.path.isdir(opdir)):
    print "opdir: ",opdir," is not there -- mkdir"
    os.mkdir(opdir)



#
# fld .ctl and orog .ctl for making basemap
#

cfldpath="%s/fld.tcstruct.%s.%s.ctl"%(oddir,model,dtg)
orogpath="%s/geo.1deg.ctl"%(wgddir)

#pppppppppppppppppppppppppppppppppppppppppppppppppp
#
#  paths
#
#pppppppppppppppppppppppppppppppppppppppppppppppppp

ngtrkngtrppath="%s/ngtrk.ngtrp.%s.%s.txt"%(otdir,omodel,dtg)
ngtrkfldpath="%s/ngtrk.fld.%s.%s.dat"%(oddir,omodel,dtg)
ngtrkctlpath="%s/ngtrk.fld.%s.%s.ctl"%(oddir,omodel,dtg)

ngtrktrackpath="%s/ngtrk.track.%s.%s.txt"%(otdir,omodel,dtg)
ngtrkdiagpath="%s/ngtrk.track.diag.%s.%s.txt"%(otdir,omodel,dtg)
ngtrkdiagmfpath="%s/ngtrk.track.diag.mf.%s.%s.txt"%(otdir,omodel,dtg)

ngtrktrackpath1="%s/ngtrk.track.%s.%s.sfc.txt"%(otdir,omodel,dtg)
ngtrkdiagpath1="%s/ngtrk.track.diag.%s.%s.sfc.txt"%(otdir,omodel,dtg)
ngtrkdiagmfpath1="%s/ngtrk.track.diag.mf.%s.%s.sfc.txt"%(otdir,omodel,dtg)

ngtrktrackpath2="%s/ngtrk.track.%s.%s.vort8.txt"%(otdir,omodel,dtg)
ngtrkdiagpath2="%s/ngtrk.track.diag.%s.%s.vort8.txt"%(otdir,omodel,dtg)
ngtrkdiagmfpath2="%s/ngtrk.track.diag.mf.%s.%s.vort8.txt"%(otdir,omodel,dtg)

ngtrktcbtftgsfpath="%s/ngtrk.tcbtft.%s.%s.gsf"%(otdir,amodel,dtg)
ngtrktcbtofgsfpath="%s/ngtrk.tcbtof.%s.%s.gsf"%(otdir,amodel,dtg)


#----------------------------------------------------------------------
#
# parse the carq cards for storms and struct data
# punch out will happenin ParseCarqStorms if no TCs
#
#----------------------------------------------------------------------
#(stmidscq,stmdatacq,stmmotioncq)=ParseCarqStorms(dtg,stmidset)
#(stmidsbt,stmdatabt,stmmotionbt)=ParseBdeckStorms(dtg,stmidset)
#(stmidsbo,stmdatabo,stmmotionbo)=ParseBtOpsStorms(dtg,stmidset)
#(stmids,stmdata,stmmotion)=UniqStorms(stmidscq,stmdatacq,stmmotioncq,
#                                      stmidsbt,stmdatabt,stmmotionbt,
#                                      stmidsbo,stmdatabo,stmmotionbo)

(stmids,stmdata,stmmotion)=ParseBtOpsStorms(dtg,stmidset)

stm3tofull={}

for stmid in stmids:
    stm3=stmid.split('.')[0]
    stm3tofull[stm3]=stmid



#
# create db card for dtg
#
if(popt == 'tc.db'):
    TcstructDataCards(dtg,stmdata,stm3tofull,otdir,ogdir,osdir,bdir,verb=0)
    sys.exit()


if(verb):
    print 'stmids      ',stmids
    kk=stmdata.keys()

    for s in stmids:
        print 'ssss ',s
    for k in kk:
        print 'qqq ',k,stmdata[k]

    kk=stm3tofull.keys()
    kk.sort()

    for k in kk:
        print k,stm3tofull[k]

#
# 20050419 -- filter out non-westpac storms for gsm limited area grid
#
stmids=FiltStormIds(stmids,omodel)

if(stmids[0] == 'notcs'):
   print "No TCs in adeck (CARQ) or bdeck (BEST)"
   sys.exit()

Carq2Ngtrp(dtg,stmids,stmdata,stmmotion,ngtrkngtrppath)

#----------------------------------------------------------------------
#
#  print out stm info
#
#----------------------------------------------------------------------

PrintCarqCards(dtg,omodel,stmids,stmdata)

if(popt == 'tc.ls'): sys.exit()


#----------------------------------------------------------------------
#
#  Fields Check
#
#----------------------------------------------------------------------

#
# do field checks in w2.tc.tcanal.py driver script
#
dofldrestore=0
didrestore=0
(rc,fldpath)=FieldsThere(model,dtg,specopt)

if(rc == 1):
    print "FFFFFFF fields there for: %s %s"%(model,dtg)
        
else:
    #
    # check if tracker fields made before trying...
    #
    if(not(os.path.exists(ngtrkfldpath))):
        
        print "FFFFFFF fields NOT there for %s %s ; try restore...."%(model,dtg)
        if(dofldrestore==0):
            print "FFFFFFFFF restore turned off; arrivaderla........."
            sys.exit()
        rc=FieldsRestore(model,dtg)
        (rc,fldpath)=FieldsThere(model,dtg)
        if(rc == 0):
            print "FFFFFFF ...... no joy restoring: %s %s ......"%(model,dtg)
            sys.exit(0)
        else:
            didrestore=1



#----------------------------------------------------------------------
#
# do tracking because TC input from adecks which might not
#
#----------------------------------------------------------------------

dongtrk=1
dongtrkflds=1
if(dongtrk == 0): dongtrkflds=0

print 'fldpath ',fldpath

# 
# check if made input fields to tracker
#

isflddone=os.path.exists(ngtrkfldpath)
print 'nnnn ',ngtrkfldpath,isflddone,override

if((dongtrkflds and not(isflddone)) or override):
    gradscmd="%s -lbc \"p.fld.data.ngtrk.gs %s %s %s %s\""%(xgrads,dtg,model,fldpath,ngtrkfldpath)
    NgtrkFldCtl(ngtrkfldpath,ngtrkctlpath)
    mf.runcmd(gradscmd,ropt)

if(dongtrk):
    if(dosfctrk):
        copt='-S'
    else:
        copt=''
    #
    # do both sfc and vort trk
    #

    copt='-S'
    ngtrkcmd="ngtrk.x %s %s %s %s %s %s"%\
              (ngtrkngtrppath,ngtrkfldpath,ngtrktrackpath1,ngtrkdiagpath1,ngtrkdiagmfpath1,copt)
    mf.runcmd(ngtrkcmd,ropt)

    copt='-V 4 6.5'
    ngtrkcmd="ngtrk.x %s %s %s %s %s %s"%\
              (ngtrkngtrppath,ngtrkfldpath,ngtrktrackpath2,ngtrkdiagpath2,ngtrkdiagmfpath2,copt)
    mf.runcmd(ngtrkcmd,ropt)

    trk1=(ngtrktrackpath1,ngtrkdiagmfpath1,ngtrkngtrppath)
    trk2=(ngtrktrackpath2,ngtrkdiagmfpath2,ngtrkngtrppath)

(ntcfs,modstmids,modstmdata,stmidsng,stmdatang)=Ngtrk2Adeck(dtg,omodel,trk1,trk2,otdir,oadir)

#----------------------------------------------------------------------
#
# make .gsf to plot bt/ft and bt/fc and bt/ofc posits in g.wxmap.gs
# current system is too slow and limited to 100 posits because
# of # char in line in grads
#
#----------------------------------------------------------------------

TcStruct2BtFtGs(dtg,model,
                modstmids,modstmdata,stmidsng,stmdatang,
                ngtrktcbtftgsfpath)

TcStruct2BtOfGs(dtg,model,otdir,
                ngtrktcbtofgsfpath,verb=0)

if(dotrackeronly):
    TcstructDataCards(dtg,stmdata,stm3tofull,otdir,ogdir,osdir,bdir)
    if(dopostprocess):
        TcAnalPost(dtg,model)
    sys.exit()
    

#----------------------------------------------------------------------
#
# make the carq files with storm struct data by storm/model
# and cp the model track for the tcsanal.x application
#
#----------------------------------------------------------------------

(carqcards)=MakeCarqStormFile(model,otdir,prcadir,pdir,wpddir,
                              dtg,stmids,stmdata)


#----------------------------------------------------------------------
#
# get the fields using the p.fld.tcstruct.py script
#
#----------------------------------------------------------------------

if(doflds):
    cmd="p.fld.data.tcstruct.py %s %s %s %s %s"%(dtg,model,fldpath,oddir,specopt)
    mf.runcmd(cmd,ropt)

#----------------------------------------------------------------------
#
# cycle through the storms and run the analyzer
#
#----------------------------------------------------------------------

for stmid in stmids:

    stm3=stmid.split('.')[0]
    try:
        ntcf=ntcfs[stm3]
    except:
        ntcf=0

    print 'NNNNN ',ntcf
    if(ntcf == 0):
        print "WWWWWWWWWW no forecast posits for stmid: %s"%(stmid)
        continue

    #----------------------------------------------------------------------
    # set up namelist for tcsanal.x application
    # the .ctl files for output from tcsanal.x
    #----------------------------------------------------------------------


    (nlpath)=NlSetup(otdir,oddir,osdir,opdir,omodel,model,stmid,stm3,dtg)

    (profilectlpath)=CtlSetup(oddir,omodel,model,stmid,dtg,ntcf)


    (alats,alons,refaid,reftau,reftrk)=tc2.GetOpsRefTrk(dtg,stmid,override=override)

    (latplotmin,latplotmax,lonplotmin,lonplotmax)=tc2.LatLonOpsPlotBounds(alats,alons,verb=1)
    print 'LLLLLLLLLLLLLLLLL stmid: ',stmid,latplotmin,latplotmax,lonplotmin,lonplotmax

    #(latplotmin,latplotmax,lonplotmin,lonplotmax)=JtwcLatLonBounds(cdir,cdirnhc,stmid,stmdata,stmmotion,dtg)


    #--------------------------------------------------
    # run the tcsanal.x application driven by namelist
    #--------------------------------------------------


    if(dotcsapp):
        cmd="tcsanal.x %s"%(nlpath)
        print "CCC: ",cmd
        tcsout=os.popen(cmd).readlines()
        for t in tcsout:
            print t[0:-1]


    #--------------------------------------------------
    # now set up the obs .ctl from the tcsanal.x app
    #--------------------------------------------------

    if(doobsctl):
        ObsCtlSetup(oddir,omodel,model,stmid,dtg,ntcf)


    #--------------------------------------------------
    # if 999 no forecast track to base field plot on;
    # set dofldplt to 0 and reset to input
    #--------------------------------------------------

    if(latplotmin == 999):
        dofldpltin=dofldplt
        domappltin=domapplt
        dofldplt=0
        domapplt=0
        
    #--------------------------------------------------
    # basemap plot
    #--------------------------------------------------

    SetPlotGsf(w2.GradsGslibDir,opdir)

    if(dobmapplt and dofldplt):

        (bmappath)=BaseMapPlot(ogdir,opdir,stmid,model,dtg,
                               gradsopt,orogpath,
                               latplotmin,latplotmax,
                               lonplotmin,lonplotmax,
                               xsize,ysize,dobmapplt)

    #--------------------------------------------------
    # field plot
    #--------------------------------------------------

    if(dofldplt):

        FldPlot(ogdir,otdir,oddir,opdir,
                prcadir,stmid,stm3,carqcards,
                gradsopt,omodel,model,dtg,
                cfldpath,bmappath,ntcf,
                latplotmin,latplotmax,
                lonplotmin,lonplotmax,
                xsize,ysize,dofldplt)



        #
        # create animated gif of 0,24,48,72
        #

        AnimateGifPlot(ogdir,stmid,omodel,dtg)


    if(latplotmin == 999):
        dofldplt=dofldpltin
        domapplt=domappltin

    #--------------------------------------------------
    # radial profile plot
    #--------------------------------------------------

    if(doprofileplt):

        ProfilePlot(ogdir,opdir,prcadir,stmid,model,dtg,carqcards,ntcf,
                    gradsopt,profilectlpath,
                    xsize,ysize,doprofileplt)


#
# create db card for dtg
#
TcstructDataCards(dtg,stmdata,stm3tofull,otdir,ogdir,osdir,bdir)


#----------------------------------------------------------------------
#
#  remove fields if restored from pzal
#
#----------------------------------------------------------------------

dormrestore=1
dormrestore=0
if(didrestore == 1 and dormrestore == 1):
    rc=FieldsRemove(model,dtg)

#----------------------------------------------------------------------
#
#  push trk/stt/plt to pzal
#
#----------------------------------------------------------------------

if(w2.PushTcstruct2Pzal == 1):
    cmd="%s/wxmap.ftp.tcstruct.2.pzal.pl %s"%(prcddir,dtg)
    mf.runcmd(cmd,ropt)

if(dorsyncweb):
    cmd="%s/w2.tc.rsync.tcanal.2.web.py %s"%(prcadir,dtg)
    mf.runcmd(cmd,ropt)
    
if(dopostprocess):
    TcAnalPost(dtg,model)


if(docpreftrk):
    #
    # put reftrks to /w3/rapb/fiorino/tcvitals
    #
    rc=w2.cpReftrk2W3(dtg)
    

sys.exit()

