#!/usr/bin/env python

from WxMAP2 import *
w2=W2()
import FM
from FM import Qsub

from HFIP import FimRunTaccGrids 
from HFIP import setFEtacc


#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
#
# command line setup
#
from M import CmdLine

class FimPost2CmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv

        self.argv=argv
        self.argopts={
            1:['dtgopt', 'no default'],
            2:['model' , 'no default'],
        }

        self.options={
            'override1':                    ['O',0,2,'BIG override=2'],
            'override2':                    ['o',0,1,'small override=1'],
            'gribver':                      ['1',0,1,'grib1'],
            'gribver':                      ['2',0,2,'grib2'],
            'verb':                         ['V',0,1,'verb=1 is verbose'],
            'ropt':                         ['N','','norun',' norun is norun'],
            'dols':                         ['l',0,1,'1 - list'],
            'dolslong':                     ['L',0,1,'1 - list'],
            'dotmtrk':                      ['T',0,1,' if set do tmtrk'],
            'dotrkonly':                    ['t',0,1,' dotrkonly in FM.runTCtrk()'],
            'dorsync':                      ['R',0,1,'dorsync=1'],
            'cnv1to2':                      ['C',0,1,'convert grib1->grib2'],
            'DSoverride':                   ['D',0,1,'DSoverride=1'],
            'doCleanRun':                   ['c:',0,'i','set CleanRun level; 1 - basic ; 2 full'],
            'min4dtg':                      ['m:',10,'i','how many minutes in qsub per dtg 25 default'],
            'fmodel':                       ['F:',None,'a','e.g., fmodel=FIMXnew'],
            'expopt':                       ['E:',None,'a','e.g., expopt=FIMX001'],
            'npes':                         ['n:',None,'a','e.g., npes=800 for fimchem'],
            'glvl':                         ['g:',None,'a','e.g., glvl=7 for fimx(fimchem)'],
            'doqsub':                       ['Q',0,1,"""make qsub.sh and qsub"""],
            'doVerif':                      ['v',0,1,"""parse wfm verif .log for stats"""],
            'doVerifGrbndx':                ['X',0,1,"""make grbindex files for gfs verification analysis files"""],
            'overridedoFimPost2DataOnly':   ['p',0,1,"""override w2.W2doFimPost2DataOnly"""],
            'doRsync2Kishou':               ['K',1,0,"""do NOT rsync 2 kishou if on kaze"""]
        }


        self.defaults={
            'dotimeseries':0,
            'gribver':2,
            'queue': 'batch',
        }


        self.rt=FM.rtfimRuns()

        self.purpose='''
purpose: further post process the fim output

1) parse stdout
2) filter grib? fields for a reduced data set
3) local tc trackers
4) save FIMnamelist and trackers
5) put pyp in shelve database

rtfimRuns:

%s
'''%(self.rt.getRunlist())


        self.examples='''
  %s cur12-12 rtfimy
  %s 2010011712.cur12 rtfimx001 -F FIMXnew -E FIMX001 -l
'''


    def chkLs(self):

        self.lsonly=0
        self.lsopt=''
        self.doSdatAge=0
        self.override=0
        if(self.dols or self.dolslong): self.lsonly=1
        if(self.dols): self.lsopt='Last'
        if(self.dols): self.lsopt='Last'
        if(self.dolslong): self.lsopt='l'

        if(w2.onWjet or w2.onZeus): self.doSdatAge=1
        self.estr='''%slsopt='%s'\n'''%(self.estr,self.lsopt)
        self.estr='''%slsonly=%d\n'''%(self.estr,self.lsonly)
        self.estr='''%soverride=%d\n'''%(self.estr,self.override)
        if(self.override1):
            self.estr='''%soverride=%d\n'''%(self.estr,self.override1)
        if(self.override2):
            self.estr='''%soverride=%d\n'''%(self.estr,self.override2)


    def chkFimRun(self,model):

        rtmodels=self.rt.runs.keys()

        if(not(model in rtmodels)):
            print 'EEE model: ',model,' not in FM.rtfimRuns.runs...sayoonara'
            sys.exit()

        else:
            CL.whereRun=self.rt.getRun(model).whereRun


def printOcards(ocards,dosort=0):

    ocardS={}

    for ocard in ocards:
        tt=ocard.split()

        if(not(dosort)):    print ocard

        if(len(tt) >= 5):
            age=tt[3]
            if(age != 'NO'):
                age=float(age)/24.0
                ocardS[age]=ocard


    if(not(dosort)): return
    kk=ocardS.keys()
    kk.sort()
    if(len(kk) > 0):
        print
        print 'Completed runs sorted by age in days'
        print

        for k in kk:
            print "%5.1f %s"%(k,ocardS[k])

        print
        print '#runs made: ',len(kk)," in the last: %3.0f days from current dtg: %s"%(int(kk[0]*-1.0+0.5),mf.dtg())




#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
# main
#

CL=FimPost2CmdLine(argv=sys.argv)
CL.CmdLine()
CL.chkLs()
exec(CL.estr)
if(verb): print CL.estr

# -- switches from w2switches
#
if(w2.W2doFimPost2DataOnly and not(dotmtrk)): dotmtrk=0

if(doqsub):
    qs=Qsub(sys.argv,project='fim-njet',qname='fp2',doqsub=doqsub,min4dtg=min4dtg,
            queue='batch')
    sys.exit()


if(model == 'all' or len(model.split(',')) > 1):

    if(model == 'all'):
        models=FM.models
    else:
        models=model.split(',')

    for model in models:
        cmd="%s %s %s"%(CL.pypath,dtgopt,model)
        for o,a in CL.opts:
            cmd="%s %s %s"%(cmd,o,a)
        mf.runcmd(cmd,ropt)

# -- check if model ok...
#
CL.chkFimRun(model)

# -- for fimchem always do ctl
#
alwaysDoCtl=0
if(model == 'rtfimchem' or model == 'rtfimz' or model == 'rtfim9'):  alwaysDoCtl=1
if(model == 'rtfimz'):   alwaysDoCtl=1
dofimx=0
if(model == 'rtfimx'): dofimx=1

docpalways=1
if(doCleanRun > 0 or doVerif): docpalways=0

# -- switches from w2switches
#
if(w2.W2doFimPost2DataOnly and not(overridedoFimPost2DataOnly)): dotmtrk=0


#pppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp
# main prc

trkprcdir=w2.PrcDirTctrkW2

ocards=[]
dopost=1
if(doCleanRun > 0): dopost=0

if(lsonly or dorsync or cnv1to2): dopost=0

if(not(w2.onKishou or w2.onKaze) and not(w2.onWjet or w2.onZeus)):
    dsbdirRemote="%s/DSs"%(FM.lrootLocal)
    rssvr=FM.rsyncServerKishou
else:
    if(CL.whereRun == 'zeus'):
        dsbdirRemote="%s/DSs"%(FM.trootZeus)
        rssvr=FM.rsyncServerZeus
    else:
        dsbdirRemote="%s/DSs"%(FM.trootWjet)
        rssvr=FM.rsyncServerJet

if(w2.onWjet or w2.onZeus):
    dsbdirLocal="%s/DSs"%(FM.lrootWjet)
else:
    dsbdirLocal="%s/DSs"%(FM.lrootLocal)

dbname=FM.SetDBname(model)

if(verb):
    print 'dsbdirRemote:  ',dsbdirRemote
    print 'dsbdirLocal:   ',dsbdirLocal


#dddddddddddddddddddddddddddddddddddddddddddddddddddddd loop on dtgs
#
rt=CL.rt.getRun(model)
if(dtgopt == 'all' and hasattr(rt,'dtgs')):
    dtgs=rt.dtgs
else:
    dtgs=mf.dtg_dtgopt_prc(dtgopt)


for dtg in dtgs:

    MF.sTimer('lsonly')

    # datasets setup
    #
    if(mf.find(w2.remoteHost,'zeus') or CL.whereRun == 'zeus'): dbRemote="%s_zeus_%s.pypdb"%(dbname,dtg)
    else:                                                       dbRemote="%s_wjet_%s.pypdb"%(dbname,dtg)

    dblocal="%s_local_%s.pypdb"%(dbname,dtg)
    
    # -- make DSswjet
    #
    if(w2.onWjet or w2.onZeus):
        DSswjet=FM.DataSets(bdir=dsbdirRemote,name=dbRemote,dtype='model',verb=verb,doDSsWrite=1)
    else:
        if(not(lsonly) and not(w2.onWjet or w2.onZeus) ):
            print 'rsync over the wjet DSs: ',dsbdirRemote
            MF.sTimer('rsyncDSS')
            FM.Rsync2Local(dsbdirRemote,dsbdirLocal,rs=rssvr)
            MF.dTimer('rsyncDSS')
            
        DSswjet=FM.DataSets(bdir=dsbdirLocal,name=dbRemote,dtype='model',verb=verb)
        DSslocal=FM.DataSets(bdir=dsbdirLocal,name=dblocal,dtype='model',verb=verb,doDSsWrite=1)


    FR1=None

    # set the dataset key
    #
    dskey="%s.%s"%(model,dtg)

    dswjet=DSswjet.getDataSet(dskey)

    # wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww - wjet
    #
    if(w2.onWjet or w2.onZeus):

        writeDS=0
        if(dswjet == None or dopost or override):

            # make FimExp object
            #
            FE=FM.setFE(dtg,model,fmodel=fmodel,expopt=expopt,npes=npes,glvl=glvl)

            # always make a grib1 FimRun object doallctl and qsub, this will make the tdir
            #
            fr1override=0
            if(override): fr1override=3
            FR1=FM.FimRun(FE,gribver=1,override=fr1override,
                          docpalways=docpalways,dofimx=dofimx)

            # make the FimRun object
            #
            if(gribver == 1): FR=FM.FimRun(FE,gribver=1,override=override,verb=verb,
                                           docpalways=docpalways,dofimx=dofimx)
            if(gribver == 2): FR=FM.FimRun(FE,gribver=2,override=override,verb=verb,
                                           docpalways=docpalways,dofimx=dofimx)
            
            # grib filter, make sure both sdir and tdir there (from the FR1)
            #
            if(gribver == 1 and FR.datathere == 1):
                FQ=FM.FieldRequest1()
                FR.DoGrib(FQ,override=override)
            elif(gribver == 2 and FR.datathere == 1):
                FQ=FM.FieldRequest2()
                FR.DoGrib(FQ,override=override,alwaysDoCtl=alwaysDoCtl,verb=verb)

            FR.LsGrib(override=override)

            writeDS=1

            # if neither sdir or tdir there => FR1 failed
            if(FR.datathere == 0): writeDS=0

        else:
            # restore from DSs
            FR=dswjet.FR
            FE=FR.FE

        if(dswjet == None):
            print 'making first instance of dataset: %s'%(dskey)
            dswjet=FM.DataSet(name=model,dtype='model')
            print 'making first instance of dataset: %s'%(dskey)
            writeDS=1

        if(writeDS):
            dswjet.FR=FR
            if(FR1     != None): dswjet.FR1=FR1
            DSswjet.verb=1
            rc=DSswjet.putDataSet(dswjet,dskey,unlinkException=1)

            if(rc == -1):
                dswjet=FM.DataSet(name=model,dtype='model')
                dswjet.FR=FR
                if(FR1     != None): dswjet.FR1=FR1
                rc=DSswjet.putDataSet(dswjet,dskey,unlinkException=0)
                if(rc == -1): print 'EEE bad unklink/remake of DSwet, sayoonara'; sys.exit()


    # llllllllllllllllllllllllllllllllllllllllllllllllll - local
    #
    else:

        writeDS=0
        dslocal=DSslocal.getDataSet(dskey)

        dorsynclocal=0
        (FE,FR)=FM.getDswjet(dswjet,dtg,model,fmodel,expopt,DSoverride)
        if(dslocal == None): dorsynclocal=1

        if(dorsync or dorsynclocal or dotmtrk):

            # rsync from wjet -> local, must have dswjet or override 
            # run LsGrib after to complete FRlocal -- because we read FRlocal from db and
            # will not be set on first write/read, set override=1 in LsGrib to force making inventory
            #
            if(FE == None): continue

            (FRlocal)=FM.getDslocal(FE,FR,dslocal,dtg,model,override=1)
            if(FRlocal == None): continue

            if(not(w2.onKishou or w2.onKaze)):
                sdir=FRlocal.tDirNotag
            else:
                sdir=FR.tDir


            MF.sTimer('rsyncDSS')
            FM.Rsync2Local(sdir,tdir=FRlocal.tDirNotag,rs=rssvr)
            MF.dTimer('rsyncDSS')

            # force override if dorsynclocal = 1
            #
            FRlocal.LsGrib(lsopt=lsopt,override=dorsynclocal)

            if(dslocal == None):
                dslocal=FM.DataSet(name=model,dtype='model')
                dslocal.FR=FRlocal
            else:
                dslocal.FR=FRlocal

            writeDS=1

        # get the local FR...
        #
        (FRlocal)=FM.getDslocal(FE,FR,dslocal,dtg,model,override=override)
        if(override): WriteDS=1

        if(FRlocal == None):
            print 'WWW no FRlocal! ',dtg,model
            continue

        # convert old grib1 -> grib2 for qsub and old wfm grib1
        #
        if(cnv1to2):
            FQ=FM.FieldRequest2()
            FRlocal.CnvGrib1to2(ropt=ropt)


        # dataset output
        #
        if(dslocal == None):
            print 'making first instance of dataset: %s'%(dskey)
            dslocal=FM.DataSet(name=model,dtype='model')
            writeDS=1

        if(writeDS or override):

            if(dotmtrk == 0):
                try:      del FRlocal.TT
                except:   None
            dslocal.FR=FRlocal
            # mf 20100114 -- test if put failed, if so unlink and remake
            #
            rc=DSslocal.putDataSet(dslocal,dskey,unlinkException=0)

            if(rc == -1):
                # -- unlink the create new data set...
                rc=DSslocal.putDataSet(dslocal,dskey,unlinkException=1)
                dslocal=FM.DataSet(name=model,dtype='model')
                FRlocal=FM.getDslocal(FE,FR,dslocal,dtg,model,override=1)
                dslocal.FR=FRlocal
                rc=DSslocal.putDataSet(dslocal,dskey,unlinkException=0)
                if(rc == -1): print 'EEE bad unklink/remake of DSslocal, sayoonara'; sys.exit()

    # -- processing section  pppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp
    #

    if(doCleanRun > 0):

        if(w2.onWjet or w2.onZeus):
            FR.cleanRun(doCleanRun=doCleanRun,ropt=ropt)
            continue


    if(doVerif):

        if(w2.onWjet or w2.onZeus):
            FR.parseVerifLog(ropt=ropt,verb=verb)
            continue


    # -- listing only
    #
    if(lsonly):
        if(w2.onWjet or w2.onZeus):
            rc=FR.LsGrib(lsopt=lsopt,override=override,verb=verb)
        else:
            rc=FRlocal.LsGrib(lsopt=lsopt,override=override,doSdatCurAge=0)

            if(dotmtrk):
                #TT=FRlocal.runTCtrk(dolsonly=1)
                #try: TT.lstrk()
                #except: None
                cmd="%s/w2.tc.tmtrkN.py %s %s -l"%(trkprcdir,dtg,model)
                mf.runcmd(cmd,ropt)

        print 'DDD lsonly: ',rc[1]
        ocards.append(rc[1])
        MF.dTimer('lsonly')


    # -- run tc tacker...
    #
    else:

        if(not(w2.onWjet or w2.onZeus)):
            if(dotmtrk):
                #TT=FRlocal.runTCtrk(override=override,dotrkonly=dotrkonly)
                # -- blow away .grb
                #cmd="%s/w2.tc.tmtrkN.py %s %s -K"%(trkprcdir,dtg,model) -- bug -K ONLY does Klean added -x which does clean in doTrk
                # -- 20121207 -- doKlean in doTrk() doesn't seem to work?
                #cmd="%s/w2.tc.tmtrkN.py %s %s -x"%(trkprcdir,dtg,model)
                # -- run both trackers so don't do the kill
                overrideOpt=''
                if(override == 2): overrideOpt='-O'
                cmd="%s/w2.tc.tmtrkN.py %s %s %s -M"%(trkprcdir,dtg,model,overrideOpt)
                mf.runcmd(cmd,ropt)

                #cmd="%s/w2.tc.mftrkN.py %s %s %s"%(trkprcdir,dtg,model,overrideOpt)
                #mf.runcmd(cmd,ropt)


    # -- rsync from kaze to kishou so we can process on kishou (tcgen and/or tcdiag)
    #
    if(w2.onKaze and doRsync2Kishou and not(lsonly)):

        tdirLocal=FRlocal.tOutDir
        tdirKishou='/w21/dat/nwp2/rtfim/dat/FIM9/'
        tdirKishou=tdirLocal.replace(FRlocal.tRoot,'fiorino@kishou.fsl.noaa.gov:/dat2/w21/dat/nwp2/rtfim')
        (tdirKishou,file)=os.path.split(tdirKishou)
        FM.rsync2Kishou(tdirLocal,tdirKishou,ropt)



if(lsonly): printOcards(ocards)





if(dotimeseries):
    gvar='gprc'
    gvar='gmass'
    gvar='gwnoise'

    XY1=FM.SetPlotXY(F1,gvar)
    XY2=FM.SetPlotXY(F2,gvar)
    xys=[XY1,XY2]
    FP=FM.PlotXYs(xys)
    FP.t1="%s %s"%(F1.stdout.vardesc[gvar],dtg)
    FP.t2="%s(red) v %s(blue)"%(fefim.expopt.upper(),fefimy.expopt.upper())
    FP.plot()

#sys.exit()
