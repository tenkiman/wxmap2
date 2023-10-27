#!/usr/bin/env python 

"""%s:
purpose:

  generate .gsf for g.wxmap.gs to plot bt/ft posits using tcstruct ouptut

usages:

  %s YYYYmmddhh (cur, cur-NNN, cur+NNN) | {avn;ukm;ngp;gsm;ngp.npmoc.ldm;all | tc.ls | tc.db} | [popt = ls.tc]
  %s all bdtg edtg model [popt = tc.ls]
  
examples:

%s cur ngp
%s cur ngp.npmoc.ldm
%s cur tc.ls -- list TCs to do struct anal
"""
import sys
import os
import glob
import string
import posix
import posixpath
sys.path.append("/home/fiorino/lib/python")
import mf

from tcanalsub import * 


curdtg=mf.dtg()
curphr=mf.dtg('phr')
curtime=mf.dtg('curtime')

curdir=posix.getcwd()

pyfile=sys.argv[0]

stmidset='all'
popt='all'
popt2='all'
docycling=0
spectopt=None

narg=len(sys.argv)-1
i=1
if(narg >= 4):
    popt=sys.argv[i] ; i=i+1
    bdtg=mf.dtg_command_prc(sys.argv[i]) ; i=i+1
    edtg=mf.dtg_command_prc(sys.argv[i]) ; i=i+1
    model=sys.argv[i] ; i=i+1
    if(mf.argopt(i)):  popt2=sys.argv[i] ; i=i+1
    docycling=1
    
elif(narg >= 2 and narg <= 3):
    dtg=mf.dtg_command_prc(sys.argv[i]) ; i=i+1
    model=sys.argv[i] ; i=i+1
    if(mf.argopt(i)):  popt=sys.argv[i] ; i=i+1
else:
    mf.usage(__doc__,pyfile,curdtg,curtime,curphr)
    sys.exit()

#----------------------------------------------------------------------
# command line ops
#----------------------------------------------------------------------

#
# 20041026 -- check if using npmoc.ldm data for nogaps
#

modelopt=model
specopt=''

if(model == 'ngp.npmoc.ldm' or model == 'ngp'):
    model='ngp'
    specopt='npmoc.ldm'
    

if(popt != 'tc.ls' and popt != 'all' and len(popt) != 3):
    print "EEE invalid popt: %s"%(popt)
    sys.exit(0)

if(popt != 'tc.ls' and popt != 'all' and len(popt) == 3):
    stmidset=popt

if(narg == 2 and ( model == 'tc.db' or model == 'tc.ls') ):
    popt=model

if(popt2 != 'tc.ls'): popt2=''

#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
#
#  cycle through models
#
#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc


if(model == 'all' and docycling == 0 ):

    models=SetModels(dtg,'all')
    
    for model in models:
        cmd="%s %s %s %s"%(pyfile,dtg,model,popt2)
        print "Cycling Models MMM: ",cmd
        os.system(cmd)

    sys.exit()


#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
#
#  cycle through dtgs
#
#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

if(docycling):


    models=SetModels('all','all')
    
    for model in models:
        
        dtau=DtauModel[model]
        dtgs=mf.dtgrange(bdtg,edtg,dtau)

        if(popt2 != 'tc.ls'): popt2=''
        for dtg in dtgs:
        
            cmd="%s %s %s %s"%(pyfile,dtg,model,popt2)
            print "Cycling CCC: ",cmd
            os.system(cmd)

    sys.exit()


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

xsize=700
ysize=float(xsize)*0.75
ysize=int(ysize)

gradsopt='-lc'
gradsopt='-lbc'

#
# directories
#

cdir=TcEnv['dat.jtwc']
cdirnhc=TcEnv['dat.nhc']
fdir=TcEnv['dat.fld']
bdir=TcEnv['dat.tcstruct']
prcddir=TcEnv['wxmap.prc.dat']


odir="%s/%s"%(bdir,dtg)
ogdir="%s/plt"%(odir)
osdir="%s/stt"%(odir)
otdir="%s/trk"%(odir)
oddir="%s/dat"%(odir)
opdir="%s/prc"%(odir)

oadir=TcEnv['dat.atcf']

pdir=TcEnv['prc.track']
wpddir=TcEnv['wxmap.prc.dat']
wddir=TcEnv['wxmap.dat']

#
# check if output dir and output plt stat dir are there; if not mkdir
#

if not(os.path.isdir(odir)):
    print "EEE tcstruct data files unavailable..."
    sys.exit()


#pppppppppppppppppppppppppppppppppppppppppppppppppp
#
#  paths
#
#pppppppppppppppppppppppppppppppppppppppppppppppppp

ngtrkngtrppath="%s/ngtrk.ngtrp.%s.%s.txt"%(otdir,model,dtg)
ngtrkfldpath="%s/ngtrk.fld.%s.%s.dat"%(oddir,model,dtg)
ngtrktrackpath="%s/ngtrk.track.%s.%s.txt"%(otdir,model,dtg)
ngtrkdiagpath="%s/ngtrk.track.diag.%s.%s.txt"%(otdir,model,dtg)
ngtrkdiagmfpath="%s/ngtrk.track.diag.mf.%s.%s.txt"%(otdir,model,dtg)
ngtrktcbtftgsfpath="%s/ngtrk.tcbtft.%s.%s.gsf"%(otdir,model,dtg)


TcStruct2BtFtGs(dtg,model,
                ngtrktrackpath,ngtrkdiagmfpath,ngtrkngtrppath,
                ngtrktcbtftgsfpath)


sys.exit()

