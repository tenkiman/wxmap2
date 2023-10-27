#!/usr/bin/env python

from TCdiag import *  # imports tcbase

from M2 import setModel2

# -- top level vars
# -- 20201213 -- make separate from usual directory
#
tbdir=w2.TcTcanalDatDir0
#tbdir="%s/tc/tcanal"%(w2.HfipBaseDirDat)
prcdir='/w21/src-SAV/tcdiag'
prcdir='/w21/src/tcdiag'
prcdir=w2.PrcDirTcdiagW2
prcdirIships="%s/tclgem"%(w2.SrcBdirW2)
adeckSdir=w2.TcDatDirTMtrkN
# -- use hfip filesystem -- 
#adeckSdir="%s/tc/tmtrkN"%(w2.HfipBaseDirDat)
adeckSdir=TcAdecksMftrkNDir


class MyCmdLine(CmdLine):

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
            'TDoverride':       ['o:',None,'a','TDoverride invokes tests in lsDiagProc(): test-trkplot | test-htmlonly | test-plot-html'],
            'SSToverride':      ['z',0,1,'override just making oisst -- for old cases when grid changed'],
            'redoLsdiag':       ['R',0,1,'override just running the '],
            'verb':             ['V',0,1,'verb=1 is verbose'],
            'iVunlink':         ['v',0,1,'unlink invHash pypdb'],
            'quiet':            ['q',1,0,' turn OFF running GA in quiet mode'],
            'ropt':             ['N','','norun',' norun is norun'],
            'doTcFlds':         ['F',0,1,'''doTcFlds -- make f77 input files for lsdiags.x only'''],
            'dowindow':         ['w',0,1,'1 - dowindow in GA.setGA()'],
            'doLgemOnly':       ['G',0,1,'doLgemOnly'],
            'dowebserver':      ['W',1,0,'do NOT 1 - dowebserver=1 write to webserver for plotonly '],
            'doxv':             ['X',0,1,'1 - xv the plot'],
            'doplot':           ['P',1,0,'0 - do NOT make diag plots'],
            'aidSource':        ['T:',None,'a','aid.source to pull adeck from the adeck_source_year_pypdb'],
            'domandonly':       ['m',0,1,'DO        reduced levels only (sfc,850,500,200)'],
            'doStndOnly':       ['s',1,0,'do NOT do SHIPS levels (1000,850,700,500,400,300,250,200,150,100)'],
            'stmopt':           ['S:',None,'a','stmopt'],
            'getpYp':           ['Y',0,1,'1 - get from pyp'],
            'doclean':          ['k',0,1,'clean off files < dtgopt'],
            'docleanDpaths':    ['K',1,0,'do NOT clean off dpaths < dtgopt'],
            'dohtmlvars':       ['H',0,1,'do html for individual models'],
            'dothin':           ['t',0,1,'dothin -- reduce # of taus .dat files to reduce storage'],
            'lsInv':            ['i',0,1,'do html for individual models'],
            'doInv':            ['I',0,1,'do html for individual models'],
            'dols':             ['l',0,1,'do ls of TCs...'],
            'ndayback':         ['n:',25,'i','ndays back to do inventory from current dtg...'],
            'invtag':           ['g:',None,'a','tag to put on inventory file'],
            'zoomfact':         ['Z:',None,'a','zoomfact'],
            'dtype':            ['d:','w2flds','a','default source of fields'],
            'doall':            ['A',0,1,'do all processing for a dtg'],
            'doDiagOnly':       ['D',0,1,'do only diagfile processing'],
            'trkSource':        ['M:','mftrkN','a','tm|mftrk for trkSource'],
            'dotrkSource':      ['r',0,1,'run tracker to get track...'],
            'TRKoverride':      ['e',0,1,'set override=1 when running tracker to get track using -r option...'],
            'bypassRunChk':     ['y',0,1,'bypassRunChk track...'],
            'bmoverride':       ['B',1,0,'do NOT regen the basemaps'],
            'putAdeckOnly':     ['a',0,1,'just write out the adeck...'],
            'selectNN':         ['9',1,0,'default is 1 -- use NN, if 0 use 9X (more operational)'],
            'dobt':             ['b:',0,'i','use BT or working BT'],
            'doEra5sst':        ['5',0,1,'use ERA5 00z daily SST'],
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
if(verb): print CL.estr

# -- check if running already..
#
rc=w2.ChkIfRunningNWP(dtg=dtgopt,pyfile=pyfile,model=modelopt,verb=verb)
if(rc > 1 and not(dols) and not(bypassRunChk)):
    print 'AAA allready running...'
    sys.exit()

MF.ChangeDir(prcdir)

# -- set xgrads grads obj
#
xgrads=setXgrads()
gaP=GaProc(Quiet=quiet,Bin=xgrads)

# -- get dtgs
#
(dtgs,modelsDiag)=getDtgsModels(CL,dtgopt,modelopt)

# -- cycle because of memory leak in grads 
#
if(len(dtgs) > 1):
    
    for dtg in dtgs:
        cmd="%s %s %s"%(pypath,dtg,modelopt)
        for o,a in CL.opts:
            if(o != '-y'):
                cmd="%s %s %s"%(cmd,o,a)
                
        cmd="%s -y"%(cmd)
        mf.runcmd(cmd,ropt)

    sys.exit()

for dtg in dtgs:
    
    MF.sTimer('TcData')
    tD=TcData(dtgopt=dtg)
    MF.dTimer('TcData')

    models=modelsDiag[dtg]
    
    for model in models:

        # -- force 
        #
        iyear=int(dtg[0:4])
        if(model == 'era5' and iyear <= 2019):
            doEra5sst=1
            
        dobail=0
        if(ropt == 'norun'): dobail=0
        MF.sTimer('tcdiag')

        tG=TcDiagTau0(dtg,model,tD,
                      ttaus=[0],
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
                      dobail=dobail,doshort=dothin,
                      adeckSdir="%s/%s/%s"%(adeckSdir,dtg,model),
                      dlat=12.0,
                      doga=0,verb=verb)
        
        # -- get the status of the diag files
        #
        rc=tG.getTcdiagStatus()
        if(rc and not(override)):
            print 'TCdiagTau0 already done for: ',dtg,' model: ',model,' press...'
            continue


        # -- set the for roci/poci -- now that we're using opengrads2.2 same as usual
        #
        tG.grads21Cmd=xgrads
         
        tG.prcdir=prcdir
        MF.dTimer('tcdiag')

        tauOffSet=tG.tauOffset

        if(tauOffSet == 6):
            tG.targetTaus=[6]
            
        if(len(tG.stmids) == 0):
            print 'III - no storms for dtg: ',dtg,' press...'
            break

        if(tG.ctlpath == None):
            print 'WWW(%s): no ctlpath for dtg: '%(CL.pyfile),dtg,' model: ',model,' press...'
            continue

        # -- input fields
        #
        MF.sTimer('tcfldsdiag:%s:%s'%(dtg,model))

        # -- set taus based on available data, not ttaus
        #
        doregrid=1
        # -- doesn't work?
        #if(model == 'gfs2'): doregrid=0
        # -- use all storm ids to set the data grid vice just the storms we want...
        #    case where have shem storm but want to do westpac

        mfT=TcFldsDiag(dtg,model,tG.ctlpath,
                       taus=tG.targetTaus,
                       dstmids=tG.stmids,
                       tbdir=tG.tbdir,
                       dlat=0.5,
                       dlon=0.5,
                       doregrid=doregrid,
                       Quiet=quiet,
                       dols=dols,
                       )
        MF.dTimer('tcfldsdiag:%s:%s'%(dtg,model))
        

        if(not(mfT.sstDone and mfT.meteoDone) or override or SSToverride):

            MF.sTimer('fldinput:%s:%s'%(dtg,model))
            # -- start grads; decoreate the tG object (TcDiag()); open fld ctlpath
            mfT.makeFldInputGA(gaP)
            # -- SST
            overrideSST=0
            if(override or SSToverride): overrideSST=1
            
            if(doEra5sst):
                mfT.makeEra5sst(override=overrideSST)
            else:
                mfT.makeOisst(override=overrideSST)
            
            # -- meteo
            mfT.makeFldInput(override=override,verb=verb,doconst0=0,dogetValidTaus=0)
            
            # -- get the data status
            rc=mfT.getDpaths(verb=verb,useAvailTaus=1)

            # -- bail if bad data status...
            #
            if(rc == 0):
                print 'EEE-mfT.makeFldInput failed...sstDone: ',mfT.sstDone,' meteoDone: ',mfT.meteoDone,' sayounara...'
                sys.exit()
                
                
            # -- reinit ga
            mfT.reinitGA(gaP)
            MF.dTimer('fldinput:%s:%s'%(dtg,model))

        # -- turn off dup check!!!  only useful if doing storms by dtg -- really does happen, e.g., c1l.13 and c4l.13
        #
        dstmids=tD.getStmidDtg(dtg,dupchk=0)
        
        print 'qqqqqqqqqqq',dstmids
        
        #ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss
        # -- cycle by stmids
        #
        for stmid in dstmids:

            # -- get tctracker and make tc meta file -- this sets the aid and source for setDiagPath
            #

            if(tG.setTCtracker(stmid) == 0):
                #didIt=doInvAtEnd=0 #-- don't really need to kill inventory
                print 'III(%s) cycling by storms for dtg: %s model: %s no tracker continue to next stmid...'%(pyfile,dtg,model)
                continue
            rc=tG.makeTCmeta(tdir=mfT.tdir,taus=mfT.meteoTausDone)

            # -- set diagfile output path
            #
            (rc,dtime,dpath)=tG.setDiagPath(stmid,tdir=mfT.tdir)

            # -- run fortran
            #
            MF.sTimer('lsdiag.x:%s:%s:%s'%(dtg,model,stmid))
            rc=runLsDiag(mfT,tG)
            MF.dTimer('lsdiag.x:%s:%s:%s'%(dtg,model,stmid))

            # -- parse output ; this sets tG.taus
            #
            tG.parseDiag(stmid,dobail=0)

            # -- make plots; set the ctlpath to lsdiag binary
            #
            if(doplot):
                MF.sTimer('plots')
                
                # -- from w2-tc-lsdiag.py...
                # -- get the sst ctl...
                tG.oisstCtlpath=tG.ctlpath.replace(model,'oisst')
                # -- from jtdiag-plot ... use sstcpath from...
                #
                tG.oisstCtlpath=mfT.sstcpath
                # -- make new ga,ge using new tG.ctlpath
                tG.initGA(tG.gaopt)
                
                for tau in tG.taus:
                    
                    rc=tG.setLatLonTimeByTau(dtg,model,stmid,tau)
                    if(bmoverride): tG.pltBasemap(bmoverride=1)
                    
                    dotest=0
                    MF.sTimer('jt-%s-%s-%s-%s'%(stmid,model,dtg,tau))
                    tG.pltShear(dotest=dotest,override=override)
                    tG.pltDiv200(dotest=dotest,override=override)
                    tG.pltPrw(dotest=dotest,override=override)
                    tG.pltVmax(dotest=dotest,override=override)
                    tG.pltSst(dotest=dotest,override=override)
                    tG.pltPrecip(dotest=dotest,override=override)
                    tG.pltVort850(dotest=dotest,override=override)
                    MF.dTimer('jt-%s-%s-%s-%s'%(stmid,model,dtg,tau))

                # -- parse diag to get urls for plots
                #
                tG.parseDiag(stmid,dobail=0)

                MF.dTimer('plots')


            # -- put adecks and diagfiles
            #
            tG.putAdeckCards(stmid,verb=verb)

        # -- blow away ga2 here...
        #
        if(hasattr(tG,'ga2')): tG.ga2('quit')

        # -- clean dpaths
        #
        if(docleanDpaths):
            MF.sTimer('tcfldscleandpaths:%s:%s'%(dtg,model))
            mfT.cleanDpaths(ropt=ropt)
            MF.dTimer('tcfldscleandpaths:%s:%s'%(dtg,model))

        # -- clean dpaths
        #
        if(docleanDpaths):  mfT.cleanDpaths(ropt=ropt)


MF.dTimer(tag='all')
