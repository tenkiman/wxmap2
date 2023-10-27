#!/usr/bin/env python

from TCdiag import *  # imports tcbase

from M2 import setModel2

# -- top level vars
#
tbdir=w2.TcTcanalDatDir
#tbdir="%s/tc/tcanal"%(w2.HfipBaseDirDat)
prcdir='/w21/src-SAV/tcdiag'
prcdir='/w21/src/tcdiag'
prcdir=w2.PrcDirTcdiagW2
prcdirIships="%s/tclgem"%(w2.SrcBdirW2)
adeckSdir=w2.TcDatDirTMtrkN
# -- use hfip filesystem -- 
#adeckSdir="%s/tc/tmtrkN"%(w2.HfipBaseDirDat)
adeckSdir=TcAdecksTmtrkNDir


class MyCmdLine(CmdLine):

    # -- set up here to put in an object
    #

    btau06=0
    etau06=48
    dtau06=6

    btau12=etau06+12
    etau12=168
    dtau12=12
    ndaybackDefault=25

    ttaus=range(btau06,etau06+1,dtau06)+range(btau12,etau12+1,dtau12)

    gaopt='-g 1024x768'

    def __init__(self,argv=sys.argv):



        if(argv == None): argv=sys.argv

        self.argv=argv
        self.argopts={
            1:['dtgopt',  'run dtgs'],
            2:['modelopt',    'model|model1,model2|all|allgen'],
        }

        self.defaults={
            'doupdate':0,
            'doga':1,
        }

        self.options={
            'override':         ['O',0,1,'override'],
            'SSToverride':      ['z',0,1,'override just making oisst -- for old cases when grid changed'],
            'verb':             ['V',0,1,'verb=1 is verbose'],
            'quiet':            ['q',1,0,' turn OFF running GA in quiet mode'],
            'ropt':             ['N','','norun',' norun is norun'],
            'dowindow':         ['w',0,1,'1 - dowindow in GA.setGA()'],
            'dowebserver':      ['W',1,0,'do NOT 1 - dowebserver=1 write to webserver for plotonly '],
            'aidSource':        ['T:',None,'a','aid.source to pull adeck from the adeck_source_year_pypdb'],
            'domandonly':       ['m',0,1,'DO        reduced levels only (sfc,850,500,200)'],
            'doStndOnly':       ['s',1,0,'do NOT do SHIPS levels (1000,850,700,500,400,300,250,200,150,100)'],
            'stmopt':           ['S:',None,'a','stmopt'],
            'dols':             ['l',0,1,'do ls of TCs...'],
            'dtype':            ['d:','w2flds','a','default source of fields'],
            'doDiagOnly':       ['D',0,1,'do only diagfile processing'],
            'trkSource':        ['M:','longest','a','default longest or tm|mftrk for trkSource'],
            'bmoverride':       ['B',1,0,'do NOT regen the basemaps'],
            'selectNN':         ['9',1,0,'default is 1 -- use NN, if 0 use 9X (more operational)'],
            'dobt':             ['b:',0,'i','use BT or working BT'],
            'plotAll':          ['A',0,1,'plot all'],
            'justPr':           ['j',0,1,'just plot precip/slp'],
            'cycle':            ['Y',1,0,'do NOT cycle dtgs'],
            'dochkIfRunning':   ['c',1,0,'do NOT using MF.chkIfJobIsRunning'],
            'docleanDpaths':    ['K',1,0,'do NOT clean off dpaths < dtgopt'],
        }

        self.purpose='''
purpose -- generate TC large-scale 'diag' file for lgem/ships/stips intensity models
 '''
        self.examples='''
%s 2010052500 gfs2
%s cur-6 gfs2 -l -o test-plot-html  # ls and do plot track
'''


def errAD(option,opt=None):

    if(option == 'tstmids'):
        print 'EEE # of tstmids = 0 :: no stms to verify...stmopt: ',stmopt
    elif(option == 'tstms'):
        print 'EEE # of tstms from stmopt: ',stmopt,' = 0 :: no stms to verify...'
    else:
        print 'Stopping in errAD: ',option

    sys.exit()



#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
# main
#

MF.sTimer(tag='all')

argv=sys.argv
CL=MyCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb):
    print CL.estr
    print CL.opts

# -- check if running already
#
rc=w2.ChkIfRunningNWP(dtg=dtgopt,pyfile=pyfile,model=modelopt,verb=verb)
if(rc > 1 and not(dols) and not(dochkIfRunning)):
    print 'AAA allready running...'
    sys.exit()


MF.ChangeDir(prcdir)

xgrads='grads'
xgrads=setXgrads(useX11=1)

(dtgs,modelsDiag)=getDtgsModels(CL,dtgopt,modelopt)

# -- cccccyyyyycccccllllling
#
if(cycle and len(dtgs) > 1):

    for dtg in dtgs:
        
        models=modelsDiag[dtg]
        
        for model in models:
            cmd="%s %s %s"%(pypath,dtg,model)
            for o,a in CL.opts:
                if(o != '-N' and o != '-i'):
                    cmd="%s %s %s"%(cmd,o,a)

            # -- add -c option to bypass chkifrunning
            cmd="%s -c"%(cmd)
            mf.runcmd(cmd,ropt,prefix="cycling")

    sys.exit()



# -- grads processing object
#
gaP=GaProc(Quiet=quiet,Bin=xgrads)

# -- do TcData topside
#

if(ropt != 'norun'):

    # if doing inventory, use dtg from beginning of dtgrange
    # -- a problem ~ 0701 because use 06?? shemyear = curyear
    # -- 20160703 -- not sure we need to do this anymore -- turn off
    # -- 20170125 -- yeah because of the shift in getting nhem storms from previous year on 011500
    #
    dtgtcd=dtgs[-1]
    MF.sTimer('TcData:%s'%(dtgtcd))
    tD=TcData(dtgopt=dtgtcd)
    MF.dTimer('TcData:%s'%(dtgtcd))

for dtg in dtgs:

    models=modelsDiag[dtg]

    for model in models:

        # -- set trkSource
        #
        if(mf.find(trkSource,'mft')): trkSource='mftrkN'
        if(mf.find(trkSource,'tmt')): trkSource='tmtrkN'

        print 'DDDDDDDDDDDDD doing dtg: ',dtg,' model: %-10s'%(model),' trkSource: ',trkSource

        MF.sTimer('setModel2: %s dtg: %s'%(model,dtg))
        m=setModel2(model)
        fm=m.DataPath(dtg,dtype=dtype,diag=1)
        fd=fm.GetDataStatus(dtg)
        if(ropt == 'norun'): continue
        
        MF.sTimer('tcdiag')
        
        # -- override lsdiag tbdir and webdir when on Taifuu during dev
        #
        #if(not(w2.onKaze) and not(w2.onKishou)):
        #    w2.HfipWebBdir='/w21/web'
        #    tbdir='/w21/dat/tc/tcdiag'
            
        tG=TcDiag(dtg,model,
                  ttaus=CL.ttaus,
                  gaopt=CL.gaopt,
                  domandonly=domandonly,
                  doStndOnly=doStndOnly,
                  doDiagOnly=doDiagOnly,
                  dols=dols,
                  tbdir=tbdir,
                  dowebserver=dowebserver,
                  trkSource=trkSource,
                  selectNN=selectNN,
                  dobt=dobt,
                  adeckSdir="%s/%s/%s"%(adeckSdir,dtg,model),
                  xgrads=xgrads,
                  tD=tD,
                  dlat=12.0,
                  doga=0,verb=verb)
        
        # -- check if data
        #
        if(tG.ctlpath == None or tG.ctlStatus == 0):
            print 'WWW(TcDiag) -- no data for dtg: ',dtg,' model: ',model,' press...'
            continue
        
        tG.grads21Cmd=xgrads
        
        tG.prcdir=prcdir
        MF.dTimer('tcdiag')
        
        # -- input fields
        #
        MF.sTimer('tcfldsdiag:%s:%s'%(dtg,model))

        # -- set taus based on available data, not ttaus
        #
        doregrid=1
        dlatRegrid=0.5
        dlonRegrid=0.5
        # -- use full res for ecm4 and higher res for ukm2 (0.23x0.16)
        # -- 20170214 - shift gfs2 to 0.25 data
        if(model == 'ecm4' or model == 'ecm5' or model == 'ukm2' or model == 'gfs2'):
            dlatRegrid=0.25
            dlonRegrid=0.25

        # -- 2017071112 - ukm2 went to 0.14x0.09 deg! (2560x1921)
        if(model == 'ukm2'):
            dlatRegrid=0.10
            dlonRegrid=0.10

        # -- doesn't work?
        #if(model == 'gfs2'): doregrid=0
        # -- use all storm ids to set the data grid vice just the storms we want...
        #    case where have shem storm but want to do westpac

        mfT=TcFldsDiag(dtg,model,tG.ctlpath,
                       taus=tG.targetTaus,
                       dstmids=tG.stmids,
                       tbdir=tG.tbdir,
                       dlat=dlatRegrid,
                       dlon=dlonRegrid,
                       doregrid=doregrid,
                       Quiet=quiet,
                       dols=dols,
                       verb=verb,
                       sstOnly=1,
                       )
        MF.dTimer('tcfldsdiag:%s:%s'%(dtg,model))

        if(mfT.status == 0):
            print 'mfT.status = 0'
            continue

        MF.sTimer('fldinput:%s:%s'%(dtg,model))
        # -- start grads; decoreate the tG object (TcDiag()); open fld ctlpath
        gaP=mfT.makeFldInputGA(gaP)
        # -- SST
        mfT.makeOisst(override=SSToverride)
        
        mfT.reinitGA(gaP)
        MF.dTimer('fldinput:%s:%s'%(dtg,model))
        
        tstmids=getStmids(dtg,tG.stmids,tG.adstm2ids,stmopt=stmopt,dols=dols)
        sleep(10)
        # -- if no TCs or no trackers...continue
        #
        if(len(tG.adstm2ids) == 0 or len(tG.stmids) == 0):
            print """WWW(%s) no TCs or trkSource: '%s' not run yet"""%(pyfile,trkSource)
            #didIt=0
            continue

        # -- get storms and make sure ctlpath there...
        #
        dstmids=tG.getTCdiagStorms(tstmids)
        ctlpath=tG.ctlpath

        # -- check if a data tau 0
        #
        if(not(0 in tG.targetTaus)):
            print 'EEE no data tau0...continue...',ctlpath
            continue

        if(ctlpath != None):
            print 'PPPPP process  dtg: ',dtg," model:  %-10s"%(model)," targetTaus: %3d-%-3d"%(tG.targetTaus[0],tG.targetTaus[-1]),' ctlpath: ',ctlpath

        tG.oisstCtlpath=mfT.sstcpath
        
        # -- ls the diagfile and other testing/prcoessing llllllllllllllllllllllllllll

        for stmid in dstmids:
    
            # -- dols inside here
            #
            if(tG.setTCtracker(stmid,aidSource,quiet=1) == 0):
                print 'WWW nada in tG.setTCtracker for stmid: ',stmid,' press...'
                continue
    
            (rc,dtime,dpath)=tG.setDiagPath(stmid,tdir=tG.webdiagdir)
    
    
            MF.sTimer('paresDiag-test')
            rc=tG.parseDiag(stmid,dobail=0)
            MF.dTimer('paresDiag-test') 
            if(rc == 0): continue
            #ppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp -- plots
            #
            if(not(hasattr(tG,'ga'))): tG.initGA(tG.gaopt,Quiet=1)
    
            ttaus=CL.ttaus
            for tau in ttaus:
                
                rc=tG.setLatLonTimeByTau(dtg,model,stmid,tau)
                
                # -- make sure there's a posit...
                #
                if(rc == 0): continue
                if(bmoverride): tG.pltBasemap(bmoverride=1)

                dotest=1
                dotest=0
                MF.sTimer('jt-%s-%s-%s-%s'%(stmid,model,dtg,tau))
                
                if(justPr):
                    tG.pltPrecip(dotest=dotest,override=override)
                    
                elif(plotAll):
                    tG.pltShear(dotest=dotest,override=override)
                    tG.pltDiv200(dotest=dotest,override=override)
                    tG.pltPrw(dotest=dotest,override=override)
                    tG.pltVmax(dotest=dotest,override=override)
                    tG.pltSst(dotest=dotest,override=override)
                    tG.pltPrecip(dotest=dotest,override=override)
                    tG.pltVort850(dotest=dotest,override=override)                    

                else:
                    #tG.pltShear(dotest=dotest,override=override)
                    #tG.pltDiv200(dotest=dotest,override=override)
                    #tG.pltPrw(dotest=dotest,override=override)
                    tG.pltVmax(dotest=dotest,override=override)
                    tG.pltSst(dotest=dotest,override=override)
                    #tG.pltPrecip(dotest=dotest,override=override)
                    #tG.pltVort850(dotest=dotest,override=override)                    
                MF.dTimer('jt-%s-%s-%s-%s'%(stmid,model,dtg,tau))


            # -- clean dpaths
            #
            if(docleanDpaths):
                MF.sTimer('tcfldscleandpaths:%s:%s'%(dtg,model))
                mfT.cleanDpaths(ropt=ropt)
                MF.dTimer('tcfldscleandpaths:%s:%s'%(dtg,model))
                
MF.dTimer(tag='all')
        
sys.exit()

