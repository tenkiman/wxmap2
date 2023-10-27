#!/usr/bin/env python

"""%s

examples:
  
"""

from TC import *

import FM
from FM import onWjet
from FM import FimRunModel2

from WxMAP2 import Nwp2DataBdir

import GA


def getDSs(model,dtg,taccmodels,verb=0,lsonly=0):
    
    DSswjet=DSslocal=None
    
    dbname='w2flds'
    troot="%s/%s/%s"%(FM.sbaseWjet,Nwp2DataBdir,dbname)
    lroot="%s/%s"%(Nwp2DataBdir,dbname)
    
    for tmodel in taccmodels:
        if(model == tmodel):
            dbname='tacc2009'
            troot="%s/rtfim"%(FM.sbaseWjet)
            lroot="%s/rtfim"%(Nwp2DataBdir)
            break

    dsbdirwjet="%s/DSs"%(troot)
    dsbdirlocal="%s/DSs"%(lroot)

    dbwjet="%s_wjet_%s.pypdb"%(dbname,dtg)
    dblocal="%s_local_%s.pypdb"%(dbname,dtg)

    if(onWjet):
        DSswjet=FM.DataSets(bdir=dsbdirwjet,name=dbwjet,type='model',verb=verb)
    else:
        if(not(lsonly)):
            print 'rsync over the wjet DSs: ',dsbdirwjet
            FM.Rsync2Local(dsbdirwjet,dsbdirlocal)
        DSswjet=FM.DataSets(bdir=dsbdirlocal,name=dbwjet,type='model',verb=verb)
        DSslocal=FM.DataSets(bdir=dsbdirlocal,name=dblocal,type='model',verb=verb)

    return(dbname,DSswjet,DSslocal)


def getLantStmids(stmids):

    ostmids=[]
    
    for stmid in stmids:
        if(stmid[2].lower() == 'l'):
            stm2id=TC.stm1to2id(stmid)
            stm2id.lower()
            stm2id=stm2id.replace(".",'')
            stm2id='a'+stm2id
            ostmids.append(stm2id)
            
    return(ostmids)


def gribHfipTier2(ga,ge,dtg,model,taus,grbpath,regrid=0,dotrkonly=0):

    gl=GA.GaLatsQ(ga,ge,dtg,model,taus=taus,
                  outconv='grads_grib',
                  regrid=regrid,
                  doyflip=1,
                  frequency='forecast_minutes',
                  )

    (topath,ext)=os.path.splitext(grbpath)

    gl.create(topath)
    gl.basetime(dtg)
    gl.grid()

    plevs=[850,700,500,300,200]

    uavars=[]
    uavars.append(('ua','instant',plevs))
    uavars.append(('va','instant',plevs))
    uavars.append(('zg','instant',plevs))
    uavars.append(('hur','instant',plevs))

    if(len(uavars) > 0):
        gl.plevdim(uavars)

    gl.plevvars(uavars)

    svars=[]
    svars.append(('ts','instant'))
    svars.append(('psl','instant'))
    svars.append(('pr','accum'))
    svars.append(('prw','instant'))
    svars.append(('uas','instant'))
    svars.append(('vas','instant'))
    svars.append(('hurs','instant'))

    gl.sfcvars(svars)

    gl.outvars(svars,uavars)
    gl.close()

    return(gl)


    


#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
#
# command line setup
#
from M import CmdLine

class HfipCmdLine(CmdLine):

    taccmodels=['f8em','fim9','f9em','f0em']
    wjetmodels=['fim8']

    
    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv
        
        self.argv=argv
        self.argopts={
            1:['dtgopt',    'no default'],
            2:['modelopt',  'no default'],
            }
            
        self.options={
            'override':['O',0,1,'override'],
            'verb':['V',0,1,'verb=1 is verbose'],
            'ropt':['N','','norun',' norun is norun'],
            'dols':['l',0,1,'1 - list'],
            'dolslong':['L',0,1,'1 - list'],
            'dorsync':['R',0,1,'1 - list'],
            }

        self.defaults={
            'startga':0,
            }

        self.purpose='''
purpose -- apply fimrun class to model2 for hfip tier2 data'''
        self.examples='''
%s test
'''

    def chkLs(self):

        self.lsonly=0
        self.lsopt=''
        self.doSdatAge=0
        if(self.dols or self.dolslong): self.lsonly=1
        if(self.dols): self.lsopt='s'
        if(self.dols): self.lsopt='Last'
        if(self.dolslong): self.lsopt='l'

        if(onWjet): self.doSdatAge=1
        self.estr='''%slsopt='%s'\n'''%(self.estr,self.lsopt)
        self.estr='''%slsonly=%d\n'''%(self.estr,self.lsonly)
        self.estr='''%sdoSdatAge=%d\n'''%(self.estr,self.doSdatAge)

#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# main
#

dowindow=0
gaopt='-g 1024x768'
odir='/data/amb/projects/hfip/fim_tier2'

argstr="pyfile 2009082712 f8em"
argstr="pyfile 2009080100 fim8"
argv=argstr.split()
argv=sys.argv
CL=HfipCmdLine(argv=argv)
CL.CmdLine()
CL.chkLs()
exec(CL.estr)
if(verb): print CL.estr

MF=MFutils()

models=modelopt.split(',')
dtgs=mf.dtg_dtgopt_prc(dtgopt)

# --- start grads
#
if(ropt != 'norun' and not(dols) and startga == 0):
    ga=GA.setGA(window=dowindow,opt=gaopt)
    startga=1

for dtg in dtgs:

    for model in models:

        if(model in (FM.wjetmodels + FM.taccmodels) ):

            dsbdirlocal="%s/DSs"%(FM.lrootLocal)
            dbname=FM.SetDBname(model)
            dblocal="%s_local_%s.pypdb"%(dbname,dtg)

            DSslocal=FM.DataSets(bdir=dsbdirlocal,name=dblocal,type='model',verb=verb)

            if(DSslocal == None): continue

            dskey="%s.%s"%(model,dtg)
            dslocal=DSslocal.getDataSet(dskey)
            if(dslocal == None): continue

            FR=dslocal.FR
            ctlpath=FR.ctlpath
            maxtau=168

        else:
            FR=FimRunModel2(model,dtg,verb=verb,override=override)
            if(FR.tdatathere == 0): continue
            ctlpath=FR.ctlpathM2
            maxtau=FR.m2.maxtau


        # -- skip if no ctlpath...
        #
        if(MF.GetPathSiz(ctlpath) == None): continue

        ofile="aglxx%s_%s_%s"%(dtg[0:4],model.upper(),dtg)
        opath="%s/%s"%(odir,ofile)

        FR.LsGrib(lsopt=0)

        try:
            taus=FR.tdattausData
        except:
            print 'WWWWWWWWWWWWWWWW no tdatatausData in FR object...use 0,6,12,...,168'
            taus=range(0,168+1,6)
        
        if(startga):
            ge=GA.GradsEnv(ga)
            ga.fh=ga.open(ctlpath)
            print 'oooooooooooooo ',opath
            gl=gribHfipTier2(ga,ge,dtg,model,taus,opath)

        
        


        

