#!/usr/bin/env python

from TCdiag import *  # imports tcbase

from M2 import setModel2

# -- top level vars
#
tbdir=w2.TcTcanalDatDir
tbdirHfip="%s/tc/tcanal"%(w2.HfipBaseDirDat)
prcdir='/w21/src-SAV/tcdiag'
prcdir='/w21/src/tcdiag'
prcdir=w2.PrcDirTcdiagW2
prcdirIships="%s/tclgem"%(w2.SrcBdirW2)
adeckSdir=w2.TcDatDirTMtrkN
# -- use hfip filesystem -- 
#adeckSdir="%s/tc/tmtrkN"%(w2.HfipBaseDirDat)
adeckSdir=TcAdecksTmtrkNDir


class InvHash(InvHash):

    def lsInv(self,
              models,
              dtgs,
              override=0,
              ):


        kk=self.hash.keys()
        for k in kk:
            imodel=k[0]
            idtg=k[1]
            if((idtg in dtgs) and
               (imodel in models)
               ):
                print k,imodel,idtg,self.hash[k]



def getAtrkFromStmid(tD,stmid,dtg):

    atrk={}
    ttrk=None

    (bstmids,btcs)=tD.getDtg(dtg,dupchk=0,verb=0)

    if(stmid in bstmids):
        dss=tD.getDSsFullStm(stmid,dobt=0)
        if(dss == None):
            return(atrk)

        else:
            (ttrk,tdtgs)=dss.getMDtrk()

    if(ttrk != None):
        dtg0=dtg
        dtgm12=mf.dtginc(dtg,-12)

        trk0=ttrk[dtg0]

        try:
            trkm12=ttrk[dtgm12]
            type=1
        except:
            trkm12=None

        if(trkm12 == None):
            try:
                trkm12 = ttrk[mf.dtginc(dtg0,-6)]
                trk0   = ttrk[mf.dtginc(dtg0,+6)]
                type=2
            except:
                trk0=None
                trkm12=None

        if(trk0 == None):
            try:
                trkm12 = ttrk[mf.dtginc(dtg0,+0)]
                trk0   = ttrk[mf.dtginc(dtg0,+6)]
                type=3

            except:
                print 'WWW(getAtrkFromStmid) -- perverse case of single posit bt for stmid: ',stmid,' dtg: ',dtg
                return(atrk)


        print '000 ',type,trk0
        print '111 ',type,trkm12

        atrk[0]   =trk0[0:4]
        atrk[-12] =trkm12[0:4]


    return(atrk)



def Atrk2Icarq(atrk):

    (rlat0,rlon0,rvmax0,rpmin0)=atrk[0]
    (rlatm12,rlonm12,rvmaxm12,rpminm12)=atrk[-12]

    (course,speed,eiu,eiv)=rumhdsp(rlatm12,rlonm12,rlat0,rlon0,12)

    ihead=int(course+0.5)
    ispeed=int(speed+0.5)

    if(rlon0 >= 180.0): rlon0 = rlon0-360.0
    if(rlonm12 >= 180.0): rlonm12 = rlonm12-360.0

    print '000000',rlat0,rlon0,rvmax0,rpmin0
    print '121212',rlatm12,rlonm12,rvmaxm12,rpminm12

    ilat0=int("%5.0f"%(rlat0*10.0))
    ilon0=int("%5.0f"%(rlon0*10.0))
    ivmx0=int("%5.0f"%(rvmax0))

    ilatm12=int("%5.0f"%(rlatm12*10.0))
    ilonm12=int("%5.0f"%(rlonm12*10.0))
    ivmxm12=int("%5.0f"%(rvmaxm12))

    iper=ivmx0-ivmxm12

    print 'FFFFFF: %5.1f %6.1f  %5.1f %6.1f'%(rlat0,rlon0,rlatm12,rlonm12)

    ocard="%10s %5d %5d %5d %5d %5d %5d %5d %5d %5d"%(dtg,ilat0,ilon0,ilatm12,ilonm12,ivmx0,ivmxm12,ihead,ispeed,iper)
    print ocard
    return(ocard)

def lsDiagProc():

    for stmid in dstmids:

        # -- dols inside here
        #
        if(tG.setTCtracker(stmid,aidSource,quiet=1) == 0):
            print 'WWW nada in tG.setTCtracker for stmid: ',stmid,' press...'
            continue

        (rc,dtime,dpath)=tG.setDiagPath(stmid)

        # -- test of putting adeck/diag cards
        #
        if(putAdeckOnly):
            tG.putAdeckCards(stmid,verb=verb)
        else:
            tG.lsDiag(stmid,dobail=0)

        #tttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt 
        # -- if -o option; plot track, plots, etc.
        #
        if(TDoverride != None):

            # -- testing of plots
            #
            MF.sTimer('paresDiag-test')
            rc=tG.parseDiag(stmid,dobail=0)
            MF.dTimer('paresDiag-test')

            if(rc == 0): 
                print 'WWW(lsDiagProc) got rc=0 for tG.parseDiag for stmid: ',stmid,'returning...'
                return

            # -- redo trkplot
            #
            testtrkplotonly=0
            if(TDoverride == 'test-trkplot'): testtrkplotonly=1

            if(testtrkplotonly):
                MF.sTimer('tGtrk:%s:%s-test'%(dtg,model))
                tGtrk=TcTrkPlot(tG,stmid,zoomfact,doveribt=0,override=1,verb=verb,Quiet=1)
                MF.dTimer('tGtrk:%s:%s-test'%(dtg,model))
                continue

            # -- test html
            #
            testhtmlonly=0
            if(TDoverride == 'test-htmlonly'): testhtmlonly=1
            if(testhtmlonly):
                tGtrk=TcTrkPlot(tG,stmid,zoomfact,doveribt=0,override=1,verb=verb)
                MF.sTimer('tGh:%s:%s-test'%(dtg,model))
                tGh=TcDiagHtml(tG,tGtrk,verb=verb)
                tGh.doHtml()
                tGh.doPyp(verb=verb)
                tGhs=TcDiagHtmlVars(tG,verb=verb,keepmodels=keepmodels)
                tGhs.doHtml()
                MF.dTimer('tGh:%s:%s-test'%(dtg,model))
                return

            #tG.ls()

            # -- bail if not doing plotting/html at this point
            #
            if(TDoverride != 'test-plot-html'):
                print """WWW(lsDiagProc) if you got here, you haven't set TDoverride to 'test-plot-html'"""


            # -- set tGtrk so we can make html too
            MF.sTimer('tGtrk:%s:%s-test'%(dtg,model))
            tGtrk=TcTrkPlot(tG,stmid,zoomfact,doveribt=0,override=override,verb=verb)
            MF.dTimer('tGtrk:%s:%s-test'%(dtg,model))    

            MF.sTimer('make tG mFT-test')
            # -- set taus based on available data, not ttaus
            #
            mfT=TcFldsDiag(dtg,model,ctlpath,
                           ctlpath2=tG.ctlpath2,
                           taus=tG.targetTaus,
                           dstmids=dstmids,
                           tbdir=tG.tbdir,
                           dlat=0.5,
                           dlon=0.5,
                           Quiet=quiet,
                           dols=dols,
                           verb=verb,
                           )

            # -- use the fld output ctl to plot..
            #
            tG.ctlpath=mfT.ctlpathFldOutput

            # -- get the sst ctl...
            #
            tG.oisstCtlpath=tG.ctlpath.replace(model,'oisst')

            MF.dTimer('make tG mFT-test')

            #ppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp -- plots
            #
            if(not(hasattr(tG,'ga'))): tG.initGA(tG.gaopt)

            MF.sTimer('plots')

            ttaus=tG.taus
            #ttaus=[0,6]
            for tau in ttaus:

                rc=tG.setLatLonTimeByTau(dtg,model,stmid,tau)

                if(bmoverride): tG.pltBasemap(bmoverride=1)

                #tG.pltShear()
                tG.pltVort850()
                tG.pltDiv200()
                continue
                tG.pltAllSoundings()

                tG.pltVort850()
                tG.pltDiv200()

                tG.pltVmax()
                tG.pltHartCpsB()
                tG.pltPrw()
                tG.pltPrecip()
                tG.pltSst()

            MF.dTimer('plots')

            tG.parseDiag(stmid,dobail=0)

            # -- do html
            #
            MF.sTimer('tGh:%s:%s'%(dtg,model))
            tGh=TcDiagHtml(tG,tGtrk,verb=verb)
            tGh.doHtml()
            tGh.doPyp(verb=verb)
            tGhs=TcDiagHtmlVars(tG,verb=verb,keepmodels=keepmodels)
            tGhs.doHtml()
            MF.dTimer('tGh:%s:%s'%(dtg,model))
            return

        #tttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt 

    return

def rsync2data(ropt=''):
    
    tdbdir="%s/tcdiag"%(w2.W2BaseDirWebConfig)
    tdbdirHfip="%s/tcdiagDAT"%(w2.HfipWebBdir)
    cmd="rsync -alv %s/%s/ %s/%s/"%(tdbdir,curyear,tdbdirHfip,curyear)
    mf.runcmd(cmd,ropt)



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
            'dowebserver':1,
        }

        self.options={
            'override':         ['O',0,1,'override'],
            'TDoverride':       ['o:',None,'a','TDoverride invokes tests in lsDiagProc(): test-trkplot | test-htmlonly | test-plot-html'],
            'SSToverride':      ['z',0,1,'override just making oisst -- for old cases when grid changed'],
            'redoLsdiag':       ['R',0,1,'override just running the '],
            'doRealTime':       ['r',1,0,'default is to do real time'],
            'verb':             ['V',0,1,'verb=1 is verbose'],
            'iVunlink':         ['v',0,1,'unlink invHash pypdb'],
            'quiet':            ['q',1,0,' turn OFF running GA in quiet mode'],
            'ropt':             ['N','','norun',' norun is norun'],
            'doTcFlds':         ['F',0,1,'''doTcFlds -- make f77 input files for lsdiags.x only'''],
            'runInCron':        ['C',0,1,'''being run in crontab'''],
            'doCycle':          ['c',0,1,'cycle by dtgs'],
            'dowindow':         ['w',0,1,'1 - dowindow in GA.setGA()'],
            'doLgemOnly':       ['G',0,1,'doLgemOnly'],
            'doxv':             ['X',0,1,'1 - xv the plot'],
            'doplot':           ['P',1,0,'0 - do NOT make diag plots in lsdiag (now same as jtdiag-plot)'],
            'aidSource':        ['T:',None,'a','aid.source to pull adeck from the adeck_source_year_pypdb'],
            'domandonly':       ['m',0,1,'DO        reduced levels only (sfc,850,500,200)'],
            'doStndOnly':       ['s',1,0,'do NOT do SHIPS levels (1000,850,700,500,400,300,250,200,150,100)'],
            'stmopt':           ['S:',None,'a','stmopt'],
            'getpYp':           ['Y',0,1,'1 - get from pyp'],
            'doclean':          ['k',0,1,'clean off files < dtgopt'],
            'docleanDpaths':    ['K',1,0,'do NOT clean off dpaths for current dtg -- default is to clean'],
            'dohtmlvars':       ['H',0,1,'do html for individual models'],
            'dothin':           ['t',0,1,'dothin -- reduce # of taus .dat files to reduce storage'],
            'lsInv':            ['i',0,1,'do html for individual models'],
            'doInv':            ['I',0,1,'do html for individual models'],
            'dols':             ['l',0,1,'do ls of TCs...'],
            'dolsDiag':         ['L',0,1,'do ls the diag file...'],
            'ndayback':         ['n:',self.ndaybackDefault,'i','ndays back to do inventory from current dtg...'],
            'invtag':           ['g:',None,'a','tag to put on inventory file'],
            'zoomfact':         ['Z:',None,'a','zoomfact'],
            'dtype':            ['d:','w2flds','a','default source of fields'],
            'doall':            ['A',0,1,'do all processing for a dtg'],
            'doDiagOnly':       ['D',0,1,'do only diagfile processing'],
            'trkSource':        ['M:','tmtrkN','a','default tmtrk for trkSource'],
            'TRKoverride':      ['e',0,1,'set override=1 when running tracker to get track using -r option...'],
            'bypassRunChk':     ['y',0,1,'bypassRunChk track...'],
            'bmoverride':       ['B',1,0,'do NOT regen the basemaps'],
            'putAdeckOnly':     ['a',0,1,'just write out the adeck...'],
            'selectNN':         ['9',1,0,'default is 1 -- use NN, if 0 use 9X (more operational)'],
            'dobt':             ['b:',0,'i','use BT or working BT 2'],
            'nminWait':         ['W:',30,'i','set number of minutes to wait on other runs'],
            'doEra5sst':        ['5',0,1,'use ERA5 00z daily SST'],
            'useFldOutput':     ['U',0,1,'use fldoutput for plotting -- set to 1 for ERA5'],
            'doRoci':           ['p',1,0,'do NOT do roci/poci'],
            

        }

        self.purpose='''
purpose -- generate TC large-scale 'diag' file for lgem/ships/stips intensity models
 '''
        self.examples='''
%s 2010052500 gfs2
%s cur-6 gfs2 -l -o test-plot-html  # ls and html & track plot
%s cur12-12 ecm5 -l -o test-trkplot # ls track plot only
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

# -- check if running already..
# -- 20211022 -- change if doing test-plot for track...problem if three lsdiags going at once...
# -- 20211214 -- set at command line because jgsm 06/18 conflicts with cgd2 00/12
#
if(TDoverride != None): nminWait=2

MF.ChangeDir(prcdir)

(dtgs,modelsDiag)=getDtgsModels(CL,dtgopt,modelopt)

cTest=(len(dtgs) == 1 and len(modelsDiag[dtgs[0]]) == 1)

if(doCycle and not(cTest)):
    MF.sTimer('ALL-cycle-%s'%(dtgopt))
    for dtg in dtgs:
        
        models=modelsDiag[dtg]
        for model in models:
            
            overopt=''
            #if(override): overopt='-O'
            cmd="%s %s %s %s -y"%(pyfile,dtg,model,overopt)
            #print cmd
            for o,a in CL.opts:
                if(o != '-c'):
                    cmd="%s %s %s"%(cmd,o,a)
            mf.runcmd(cmd,ropt)    

    MF.dTimer('ALL-cycle-%s'%(dtgopt))
    sys.exit()
    
    
if(dolsDiag): dols=1
if(dols or dolsDiag): 
    bypassRunChk=1    
    doRoci=0

if(not(doCycle) and not(bypassRunChk)):
    rc=MF.chkRunning(pyfile, strictChkIfRunning=1, verb=0, killjob=0, 
                     timesleep=10, nminWait=nminWait)

    if(rc > 1 and not(dols) and not(bypassRunChk)):
        print 'AAA allready running...'
        sys.exit()


xgrads=setXgrads()


# -- do inventory if cur in dtgopt
#
doInvAtEnd=0
if((mf.find(dtgopt,'cur') or mf.find(dtgopt,'ops') or runInCron) and not(dols) ): doInvAtEnd=1


#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# clean
#
if(doclean):

    MF.sTimer('doclean')
    # -- base data dir and base dtg to remove all .dat <= bddtg
    #
    tbdir=w2.TcTcanalDatDir
    bddtg=dtgs[-1]
    year=bddtg[0:4]
    dmask="%s/%s/%s??????"%(tbdir,year,year)
    # -- get dtgs
    #
    alldtgs=[]
    ddtgs=glob.glob(dmask)
    for ddtg in ddtgs:
        if(os.path.isdir(ddtg)): alldtgs.append(ddtg.split('/')[-1])

    # -- get .dat files
    #
    #alldtgs=dtgs
    for ddtg in alldtgs:
        testdiff=mf.dtgdiff(bddtg,ddtg)
        print ddtg,bddtg,testdiff
        if(testdiff <= 0.0):
            datfiles=glob.glob("%s/%s/%s/*/*.dat"%(tbdir,year,ddtg))
            for dfile in datfiles:
                print "KKKilling: dfile: ",dfile
                if(ropt != 'norun'): os.unlink(dfile)

    MF.dTimer('doclean')
    sys.exit()


# -- grads processing object
#


gaP=GaProc(Quiet=quiet,Bin=xgrads)

useLsdiagDat=0
if(redoLsdiag): useLsdiagDat=1


didIt=0

# -- do TcData topside
#

if(ropt != 'norun'):

    # if doing inventory, use dtg from beginning of dtgrange
    # -- a problem ~ 0701 because use 06?? shemyear = curyear
    # -- 20160703 -- not sure we need to do this anymore -- turn off
    # -- 20170125 -- yeah because of the shift in getting nhem storms from previous year on 011500
    # -- 20221007 -- use dtgopt for cycling cases
    #
    dtgtcd=dtgs[-1]
    if(doInv or override or SSToverride or doInvAtEnd): dtgtcd=mf.dtginc(dtgtcd,-24*ndayback) 
    dtgtcd=dtgopt
    MF.sTimer('TcData:%s'%(dtgtcd))
    tD=TcData(dtgopt=dtgtcd)
    MF.dTimer('TcData:%s'%(dtgtcd))

# special case 09w.2012
#
keepmodels=None
if(stmopt == '09w.12'):
    invtag='09w.2012'
    keepmodels=['gfs2','ecmt','fim8','ukm2','ngpc']

for dtg in dtgs:

    models=modelsDiag[dtg]
    year=dtg[0:4]
    tbdirInv="%s/%s"%(tbdir,year)

    # -- inventory object
    #
    dbname='invTcdiag.%s'%(dtg)
    MF.sTimer('invTcdiag')
    iV=InvHash(dbname=dbname,
               tbdir=tbdirInv,
               override=override,
               unlink=iVunlink)

    if(lsInv):
        iV.lsInv(models,dtg)
        if(dtg == dtgs[-1]):
            sys.exit()

    MF.dTimer('invTcdiag')

    # -- check how old this run -- if 'tooold' force regen
    #
    HH=dtg[8:10] 
    howold=mf.dtgdiff(dtg,curdtg)/24.0
    tooold=(howold > w2.W2MaxOldRegen)

    itaus=CL.ttaus

    # -- defaults non era5
    #
    doSfc=0
    doTrkPlot=1
    
    if(modelopt == 'era5'): 
        doRealTime=0
        trkSource='tmtrkN'
        docleanDpaths=0
        doSfc=1
        doTrkPlot=0
        itaus=[0,6,12,18,24]
        useFldOutput=1
        
    if(tooold and doRealTime):
        # -- for 09w.12 on kishou
        #adeckSdirs="%s/adeck/mftrkN/%s"w2.TcDatDirTMtrkN
        adeckSdir=w2.TcDatDirTMtrkN

        if(modelopt == 'all'):
            models=tcdiagModels
            if(MF.is0618Z(dtg)): models=tcdiagModels0618

    for model in models:

        iyear=int(dtg[0:4])
        if(model == 'era5' and iyear <= 2021):
            doEra5sst=1

        # -- set trkSource
        #
        if(mf.find(trkSource,'mft')): trkSource='mftrkN'
        if(mf.find(trkSource,'tmt')): trkSource='tmtrkN'

        print 'DDDDDDDDDDDDD doing dtg: ',dtg,' model: %-10s'%(model),' trkSource: ',trkSource
        if(ropt == 'norun'): continue

        if(not(dols)):

            MF.sTimer('setModel2: %s dtg: %s'%(model,dtg))
            m=setModel2(model)
            fm=m.DataPath(dtg,dtype=dtype,diag=1)
            fd=fm.GetDataStatus(dtg)

            if(HH == '00' or HH == '12'):
                minTau=modelMinTau0012[model]
            else:
                minTau=modelMinTau0618[model]

            MF.dTimer('setModel2: %s dtg: %s'%(model,dtg))

            # -- check if mintau available
            #
            if(fd.dslatestCompleteTau < minTau and not(dothin)):
                print 'WWW(fd.dslatestCompleteTau): ',fd.dslatestCompleteTau,' is < minTau: ',minTau,' model: ',model,' continue...'
                #continue


        dobail=0
        if(ropt == 'norun'): dobail=0
        MF.sTimer('tcdiag')


        tG=TcDiag(dtg,model,
                  ttaus=itaus,
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
                  useLsdiagDat=useLsdiagDat,
                  xgrads=xgrads,
                  tD=tD,
                  doSfc=doSfc,
                  doRoci=doRoci,
                  doga=0,verb=verb)

        if(tG.ctlStatus == 0):
            print 'WWW--w2.tc.lsdiag--tG.ctlStatus=0 '
            continue
                
        # -- set the for roci/poci -- now that we're using opengrads2.2 same as usual
        #
        tG.grads21Cmd=xgrads
            
        tG.prcdir=prcdir
        MF.dTimer('tcdiag')

        if(doInv):
            MF.sTimer(tag='tGinventory-begin')

            # -- special cases...by storm
            if(stmopt == '09w.12'):
                tGi=TcdiagInv(tG,dtgopt=dtgopt,invtag=invtag,ndayback=ndayback,tstmid='09w.2012',keepmodels=keepmodels)
            else:
                tGi=TcdiagInv(tG,invtag=invtag,ndayback=ndayback,verb=verb)
            MF.dTimer(tag='tGinventory-begin')
            sys.exit()

        if(dothin):
            print 'III dothin = 1'
            tG.thinOutputByTaus(doall=doall)
            continue

        # -- tcs
        #
        rc=getStmids(dtg,tG.stmids,tG.adstm2ids,stmopt=stmopt,dols=dols,tD=tD)
        if(rc[0] == 0):
            tstmids=rc[1]
        elif(rc[0] == 1):
            tstmids=rc[1]
            nstmids=rc[-1]
            

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

        # -- check if done
        #
        chkOquiet=0
        (rc,todoStmids)=tG.chKOutput(iV,dstmids,aidSource=aidSource,quiet=chkOquiet)

        if(not(chkOquiet)):
            print 'III(chKOutput) rc: ',rc,' override: ',override,'TDoveride: ',TDoverride,'docleanDpaths',docleanDpaths,dols,redoLsdiag,aidSource

        if(rc == -2):
            print 'WWW(chKOutput) 22222 rc: ',rc,'need to do the following: ',todoStmids
        elif( (rc == 0) and not(override) and not(SSToverride) and not(redoLsdiag) and TDoverride == None and not(dols) ):
            print 'WWW(chKOutput) 00000 rc: ',rc,' override: ',override,' SSToverride: ',SSToverride,'TDoveride: ',TDoverride,'redoLsdiag: ',redoLsdiag,'dols: ',\
                  dols,'docleanPaths: ',docleanDpaths,' continue...'
            #doInvAtEnd=0
            continue

        if(ropt == 'norun'):  continue

        # -- check if a data tau 0
        #
        if(not(0 in tG.targetTaus)):
            print 'EEE no data tau0...continue...',ctlpath
            continue

        if(ctlpath != None and not(dothin)):
            print 'PPPPP process  dtg: ',dtg," model:  %-10s"%(model)," targetTaus: %3d-%-3d"%(tG.targetTaus[0],tG.targetTaus[-1]),' ctlpath: ',ctlpath
        
        # -- ls the diagfile and other testing/prcoessing llllllllllllllllllllllllllll
        #
        if(dolsDiag or dols): 
            if(dolsDiag): rc=lsDiagProc()
            continue

        # -- input fields
        #
        MF.sTimer('tcfldsdiag:%s:%s'%(dtg,model))

        # -- set taus based on available data, not ttaus
        #
        doregrid=1

        if(model == 'era5' and doSfc):
            # -- 20200405 -- for better vmax/rmax calc -- now works in TcFldsDiag
            #
            dlatRegrid=0.25
            dlonRegrid=0.25

        else:
            # -- 20200406 -- use coarser grid...less i/o...and use tracker vmax vice tcdiag vmax in plots
            #
            dlatRegrid=0.50
            dlonRegrid=0.50
        
        mfT=TcFldsDiag(dtg,model,ctlpath,
                       ctlpath2=tG.ctlpath2,
                       taus=tG.targetTaus,
                       dstmids=tG.stmids,
                       tbdir=tG.tbdir,
                       dlat=dlatRegrid,
                       dlon=dlonRegrid,
                       doregrid=doregrid,
                       Quiet=quiet,
                       dols=dols,
                       doSfc=tG.doSfc,
                       verb=verb,
                       )
        MF.dTimer('tcfldsdiag:%s:%s'%(dtg,model))

        if(mfT.status == 0):
            print 'mfT.status = 0'
            continue

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
            mfT.getDpaths(verb=verb,useAvailTaus=1)
            # -- reinit ga
            mfT.reinitGA(gaP)
            MF.dTimer('fldinput:%s:%s'%(dtg,model))
            
        # -- setup .ga using field output file
        #
        if(doplot):
            # -- use the fld output ctl to plot...if set at command line
            # -- use full res ctl to plot
            #
            if(tG.useFldOutput):
                tG.ctlpath=mfT.ctlpathFldOutput

            # -- get the sst ctl...
            #tG.oisstCtlpath=tG.ctlpath.replace(model,'oisst')

            # -- from jtdiag-plot ... use sstcpath from...
            #
            tG.oisstCtlpath=mfT.sstcpath
            
            # -- make new ga,ge using new tG.ctlpath
            tG.initGA(tG.gaopt)

        # -- make stms to do be what hasn't been done yet
        #
        if(not(dols) and not(override) and not(redoLsdiag)):
            dstmids=todoStmids


        # -- if we got this far, we're going to do something...
        #
        didIt=didIt+1

        #ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss
        # -- cycle by stmids
        #
        for stmid in dstmids:

            # make sure we got a valid tracker aD object
            #
            if(tG.didADlongest):
                try:
                    testFS=(tG.FtrkSource[stmid] == None)
                except:
                    print 'no joy getting Ftrksource for stmid: ',stmid,' bailing...'
                    testFS=0
                if(testFS):
                    print 'WWW(w2-tc-lsdiag.py): could not find suitable tracker for stmid: ',stmid
                    continue

            # -- get tctracker and make tc meta file -- this sets the aid and source for setDiagPath
            #

            if(tG.setTCtracker(stmid,aidSource,quiet=0) == 0):
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
            rcLsDiag=runLsDiag(mfT,tG)
            MF.dTimer('lsdiag.x:%s:%s:%s'%(dtg,model,stmid))

            if(rcLsDiag == 0):
                print 'EEE -- problem in either sst or meteo file'
                sys.exit()
            # -- run iships.x fortran app (ships/lgem)
            #
            MF.sTimer('iships.x:%s:%s:%s'%(dtg,model,stmid))
            runLgem(dpath,tG,tG.tD,dtg,model,stmid,
                    prcdir=prcdir,
                    prcdirIships=prcdirIships,
                    verb=1)
            MF.dTimer('iships.x:%s:%s:%s'%(dtg,model,stmid))

            # -- parse output ; this sets tG.taus
            #
            tG.parseDiag(stmid,dobail=0)

            # -- make plots; set the ctlpath to lsdiag binary
            #
            if(doplot):

                # -- condition for overrideing precip plot which makes the roci
                #
                
                overridePlot=0
                if(redoLsdiag or override): overridePlot=1
                
                MF.sTimer('plots')
                for tau in tG.taus:
                    
                    rc=tG.setLatLonTimeByTau(dtg,model,stmid,tau)
                    if(bmoverride): tG.pltBasemap(bmoverride=1)
                    
                    MF.sTimer('jt-%s-%s-%s-%s'%(stmid,model,dtg,tau))
                    tG.pltShear(override=override)
                    tG.pltDiv200(override=override)
                    tG.pltPrw(override=override)
                    tG.pltVmax(override=override)
                    tG.pltSst(override=override)
                    # -- always override precip plot to get roci/poci
                    tG.pltPrecip(override=overridePlot)
                    tG.pltVort850(override=override)
                    MF.dTimer('jt-%s-%s-%s-%s'%(stmid,model,dtg,tau))
                         

                # -- parse diag to get urls for plots
                #
                tG.parseDiag(stmid,dobail=0)

                MF.dTimer('plots')


            # -- do track plot -- this resets the open files
            #
            if(doTrkPlot):
                MF.sTimer('tGtrk:%s:%s:%s'%(dtg,model,stmid))
                TRKplotoverride=0
                if(redoLsdiag or doplot): TRKplotoverride=1
                tGtrk=TcTrkPlot(tG,stmid,zoomfact,doveribt=0,override=TRKplotoverride,verb=verb,Bin=xgrads)
                MF.dTimer('tGtrk:%s:%s:%s'%(dtg,model,stmid))

            # -- do html if NOT ERA5
            #
            if(model != 'era5'):
                tGh=TcDiagHtml(tG,tGtrk)
                tGh.doHtml()
                # -- old w2.tc.flddiag.py tGh.doPyp()

                tGhs=TcDiagHtmlVars(tG,verb=verb,keepmodels=keepmodels)
                tGhs.doHtml()
                
            # -- put adecks and diagfiles
            #
            tG.putAdeckCards(stmid,verb=verb)



        # -- 20221110 -- do all rocis here vice TcDiag()
        #
        MF.sTimer('pickle-rocis')
        
        kk=tG.AllRocis.keys()
        kk.sort()
        for k in kk:
            print 'rrr',k,tG.AllRocis[k]

        rociPypPath="%s/roci.%s.%s.pyp"%(tG.tdir,tG.model,tG.dtg)
        rociPS=open(rociPypPath,'w')
        pyp=tG.AllRocis
        pickle.dump(pyp,rociPS)
        rociPS.close()
        MF.dTimer('pickle-rocis')

        # -- load inventory
        #
        (rc,todoStmids)=tG.chKOutput(iV,dstmids,aidSource=aidSource,quiet=1)

        # -- blow away ga2 here...
        #
        if(hasattr(tG,'ga2')): tG.ga2('quit')

        # -- clean dpaths
        #
        if(docleanDpaths):
            MF.sTimer('tcfldscleandpaths:%s:%s'%(dtg,model))
            mfT.cleanDpaths(ropt=ropt)
            MF.dTimer('tcfldscleandpaths:%s:%s'%(dtg,model))

            
            
# -- rsync over from web-config/tcdiag/YYYY to $W2_HFIP...
#
if(ropt != 'norun' and model != 'era5'):
    rc=rsync2data()

# -- do inventory for tcdiag.php
#
if(((didIt > 0 and doInvAtEnd) or doInv) and not(dols) and dowebserver ):
    MF.sTimer(tag='tGinventory')
    tGi=TcdiagInv(tG,ndayback=ndayback,verb=verb)
    MF.dTimer(tag='tGinventory')

MF.dTimer(tag='all')
