from WxMAP2 import *
w2=W2()

from ga2 import setGA,GaLatsQ
from tcCL import TcData
from tcVM import isIOBasinStm,isShemBasinStm

# -- lllllocal vvvvvars
#
tcgenBasins=['lant','epac','wpac','shem','nio']


# -- lllllllllllllllllllllllllocal defs
#

SetLandFrac=w2.SetLandFrac
GetLandFrac=w2.GetLandFrac

lf=SetLandFrac()

def getLF(lf,lat,lon):
    landfrac=GetLandFrac(lf,lat,lon)
    return(landfrac)

def cycleDtgsModels(CL,dtgopt,modelopt,ropt='',doCycling=0):

    dtgs=mf.dtg_dtgopt_prc(dtgopt)
    models=modelopt.split(',')

    if( (len(models) > 1 or modelopt == 'all' or len(dtgs) > 1) and doCycling):

        for dtg in dtgs:

            if(modelopt == 'all'):
                models=CL.models
                if(MF.is0618Z(dtg)): models=CL.models0618

            for model in models:
                cmd="%s %s %s"%(CL.pypath,dtg,model)
                for o,a in CL.opts:
                    if(o != '-N'):
                        cmd="%s %s %s"%(cmd,o,a)
                mf.runcmd(cmd,ropt,lsopt='')

        sys.exit()

    else:

        return(dtgs,models)



#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# local classes
#

class Qsub(MFbase):

    def __init__(self,
                 argv=None,
                 project='fim-njet',
                 vmem='1.0G',
                 qname='tctrk',
                 partition='njet:tjet:ujet:vjet:sjet',
                 runcmd='/lfs2/projects/fim/fiorino/w21/run.cron.tcsh',
                 logdir='/lfs2/projects/fim/fiorino/tmp',
                 doqsub=1,
                 queue='batch',
                 ropt='',
                 min4dtg=40,
                 tottimeMin=None,
                 dtgopt=None,
                 modelopt=None,
                 qsubcmd=None,
                 doKshUnlink=1,
                 procs=2,
                 ):

        if(w2.onZeus): 
            project='fim'
            partition='zeus'
            runcmd='/scratch1/portfolios/BMC/fim/fiorino/w21/run.cron.tcsh'
            logdir='/scratch1/portfolios/BMC/fim/fiorino/tmp'

        if(w2.onTheia): 
            project='fim'
            partition='theia'
            runcmd='/scratch3/BMC/fim/fiorino/w21/run.cron.tcsh'
            logdir='/scratch3/BMC/fim/fiorino/tmp'

        self.argv=argv
        self.qsubcmd=qsubcmd

        if(self.argv != None):  (pydir,pycmd)=os.path.split(self.argv[0])

        if(self.qsubcmd != None):
            (pydir,pycmd)=os.path.split(self.qsubcmd)

        self.pydir=pydir
        self.pycmd=pycmd

        self.project=project
        self.vmem=vmem
        self.qname=qname
        self.queue=queue
        self.procs=procs
        self.partition=partition
        self.runcmd=runcmd

        self.logdir=logdir
        self.doqsub=doqsub
        self.ropt=ropt
        self.min4dtg=min4dtg
        self.tottimeMin=tottimeMin
        self.dtgopt=dtgopt
        self.modelopt=modelopt
        self.doKshUnlink=doKshUnlink

        self.initQsub()



    def initQsub(self):


        dtgs=[]
        if( (self.argv != None and len(self.argv) > 1 )and self.dtgopt == None and self.tottimeMin == None): 
            self.dtgopt=self.argv[1]
            
        if(self.dtgopt != None): 
            dtgs=mf.dtg_dtgopt_prc(self.dtgopt)
            
        elif(self.tottimeMin == None):
            print 'EEE Qsub.initQsub: both self.argv and self.tottimeMin and self.dtgopt == None, sayoonara...'
            sys.exit()

        if(self.argv != None and len(self.argv) > 2 and self.modelopt == None): 
            self.modelopt=self.argv[2]
            
        if(self.modelopt != None):
            modelopt=self.modelopt
        else:
            print 'EEE Qsub.initQsub: both self.argv and self.modelopt == None, sayoonara...'
            sys.exit()


        ndtgs=len(dtgs)
        if(self.tottimeMin == None and ndtgs > 0):
            totmin=self.min4dtg*ndtgs
        else:
            totmin=self.tottimeMin
            
        nmin=totmin%60
        nhour=totmin/60
        
        rttime="%02d:%02d:00"%(nhour,nmin)

        if(ndtgs == 0):
            nargstart=1
            pyopt=''
        elif(ndtgs == 1):
            dtg=dtgs[0]
            pyopt=dtg
            nargstart=2
        else:
            pyopt=self.dtgopt
            nargstart=2

        pytag="%s_%s"%(self.qname,modelopt)
        for arg in self.argv[nargstart:]:
            if(arg != '-Q' and arg != '-V' and arg != '-N'):
                arg=arg.strip()
                pyopt="%s %s"%(pyopt,arg)
            elif(arg == '-N'):
                self.ropt='norun'

        curdtg=mf.dtg('dtg_mn')
        outpath="%s/out_%s_%s.txt"%(self.logdir,pytag,curdtg)
        logpath="%s/log_%s_%s.txt"%(self.logdir,pytag,curdtg)

        self.qname=pytag


        # -- new qsub system on both jet and zeus
        #

        qsubshHead='''
#!/bin/sh --login
#PBS -d .
#PBS -N %s
#PBS -A %s 
#PBS -l procs=%d
#PBS -l partition=%s
#PBS -q %s
#PBS -l walltime=%s
#PBS -j oe
#PBS -o %s
'''%(self.qname,
     self.project,
     self.procs,
     self.partition,
     self.queue,
     rttime,logpath)


        qsubshuNix='''
# Set up paths to unix commands
RM=/bin/rm
CP=/bin/cp
MV=/bin/mv
LN=/bin/ln
MKDIR=/bin/mkdir
CAT=/bin/cat
ECHO=/bin/echo
CUT=/bin/cut
WC=/usr/bin/wc
DATE=/bin/date
AWK="/bin/awk --posix"
SED=/bin/sed
TAIL=/usr/bin/tail
'''

        qsubshMain='''
# Executable script and path
RUNCMD='%s'
PYDIR="%s"
PYCMD="%s"

# Set CWD to script location and execute redirecting stdout/stderr
cd $PYDIR
$RUNCMD "$PYDIR/$PYCMD %s" >> %s 2>&1

# Check for exit status of script
error=$?
if [ ${error} -ne 0 ]; then
  ${ECHO} "ERROR: ${PYCMD} crashed  Exit status=${error}"
  exit ${error}
fi

# Sucessful exit
exit 0'''%(self.runcmd,
           self.pydir,
           self.pycmd,
           pyopt,outpath)


        qsubsh=qsubshHead+qsubshuNix+qsubshMain
        qpath="%s/p.qsub.%s.ksh"%(self.pydir,pytag)
        rc=MF.WriteString2File(qsubsh,qpath)

        print 'QQQ  qpath: ',qpath

        if(self.doqsub and self.ropt != 'norun'):

            cmd="qsub %s"%(qpath)
            MF.runcmd(cmd,self.ropt)

            if(self.doKshUnlink):
                try:     os.unlink(qpath)
                except:  None

        else:

            print
            print qsubsh
            print




class TmTrkSimple(MFbase):

    def __init__(self,
                 dtg,
                 model,
                 atcfname,
                 tdir,
                 ctlpath,
                 taus,
                 tdirAdeck=None,
                 tbdirAdeckStm=None,
                 ptable=None,
                 maxtauModel=168,
                 tcD=None,
                 mintauTC=120,
                 maxtauTC=168,
                 verb=0,
                 override=0,
                 trkmode='tracker',
                 dolstcs=0,
                 quiet=0,
                 regridTracker=0.5,
                 regridGen=1.0,
                 doClean=1,
                 trkApp='gettrk_genN.x',
                 doTrk3=0,
                 xgrads='grads',
                 ):

        self.dtg=dtg
        self.model=model
        self.atcfname=atcfname
        self.tdir=tdir
        if(tdirAdeck == None):  self.tdirAdeck=tdir
        else:                   self.tdirAdeck=tdirAdeck

        if(tbdirAdeckStm == None):  self.tbdirAdeckStm=self.tdirAdeck
        else:                       self.tbdirAdeckStm=tbdirAdeckStm
            
        self.taus=taus
        self.ptable=ptable
        self.maxtauModel=maxtauModel
        self.doga2=0
        self.trkApp=trkApp
        self.doClean=doClean
        self.doTrk3=doTrk3
        self.xgrads=xgrads
        
        MF.ChkDir(tdir,'mk')
        
        self.ctlpath=ctlpath

        self.mintauTC=mintauTC
        self.maxtauTC=maxtauTC

        self.verb=verb
        self.override=override
        self.quiet=quiet
        self.dolstcs=dolstcs

        self.initCurState() # from MFbase

        MF.ChkDir(self.tdir,'mk')
        MF.ChkDir(self.tdirAdeck,'mk')
        MF.ChkDir(self.tbdirAdeckStm,'mk')

        self.prcdir="%s/tctrk"%(os.getenv("W2_PRC_DIR"))


        self.trkmode=trkmode
        self.regridGen=regridGen
        self.regridTracker=regridTracker
        
        # -- option to input tcD
        #
        if(tcD == None):
            self.tcD=TcData(dtgopt=self.dtg,verb=verb)
        else:
            self.tcD=tcD

        

    def get4stm3id(self,stm3id,stmids):
        ostmid=None
        gotit=0
        b1id=stm3id[2]
        for stmid in stmids:
            tstm3id=stmid.split('.')[0]
            tstmyear=stmid.split('.')[1]
            tb1id=tstm3id[2]
            if( (
                (stm3id.upper() == tstm3id.upper()) or
                (isIOBasinStm(stmid) and isIOBasinStm(stm3id)) or
                (isShemBasinStm(stmid) and isShemBasinStm(stm3id))
                )
                and gotit == 0):
                gotit=1
                ostmid="%s.%s"%(stm3id,tstmyear)

        return(ostmid)


    def getStatPaths(self,dolsonly=0):
        
        # -- PPPPPAAAAATTTTTHHHHHSSSSS - target dirs/paths
        #
        
        self.topath="%s/tmtrk"%(self.tdir)
        
        self.grbpath="%s.grb"%(self.topath)
        self.grbixpath="%s.grb.ix"%(self.topath)
        self.grbctlpath="%s.grb.ctl"%(self.topath)
        self.grbgmppath="%s.grb.gmp"%(self.topath)

        self.grb10path="%s.1p0deg.grb"%(self.topath)
        self.grbix10path="%s.grb.1p0deg.ix"%(self.topath)
        self.grbctl10path="%s.grb.1p0deg.ctl"%(self.topath)
        self.grbgmp10path="%s.grb.1p0deg.gmp"%(self.topath)

        # -- tcgen
        #
        omodel=self.model
        if(self.atcfname != None): omodel=self.atcfname
        omodel=omodel.lower()

        self.otctrkpath="%s/tctrk.atcf.%s.%s.txt"%(self.tdirAdeck,self.dtg,omodel)
        self.otctrksinkpath="%s/tctrk.sink.%s.%s.txt"%(self.tdirAdeck,self.dtg,omodel)
        self.otctrksnk2path="%s/tctrk.snk2.%s.%s.txt"%(self.tdirAdeck,self.dtg,omodel)
        
        self.otctrkpathStat=MF.getPathSiz(self.otctrkpath)
        self.otctrksinkpathStat=MF.getPathSiz(self.otctrksinkpath)
        self.otctrksnk2pathStat=MF.getPathSiz(self.otctrksnk2path)
        
        omodel=self.model
        if(self.atcfname != None): omodel=self.atcfname
        omodel=omodel.lower()

        otcgenPaths={}
        statTCgenS={}

        
        # -- SSSTTTAAATTTuuuSSS of trackers
        #
        statusTCgen=1

        for basin in tcgenBasins:
            
            otcgenpath    ="%s/tcgen.atcf.%s.%s.%s.txt"%(self.tdirAdeck,basin,self.dtg,omodel)    # - fort.64
            otcgensinkpath="%s/tcgen.sink.%s.%s.%s.txt"%(self.tdirAdeck,basin,self.dtg,omodel)    # - fort.68
            ofile         ="%s/stdout.tcgen.%s.%s.%s.txt"%(self.tdir,basin,self.dtg,omodel)

            if(self.doTrk3):
                otcgensnk2path="%s/tcgen.snk2.%s.%s.%s.txt"%(self.tdirAdeck,basin,self.dtg,omodel)    # - fort.69
                otcgenextrpath="%s/tcgen.extr.%s.%s.%s.txt"%(self.tdirAdeck,basin,self.dtg,omodel)    # - fort.66

            otcgenpathStat=MF.getPathSiz(otcgenpath)
            otcgensinkpathStat=MF.getPathSiz(otcgensinkpath)
            ofileStat=MF.getPathSiz(ofile)

            if(self.doTrk3):
                otcgensnk2pathStat=MF.getPathSiz(otcgensnk2path)
                otcgenextrpathStat=MF.getPathSiz(otcgenextrpath)
            
            statTCgenS[basin]=otcgenpathStat
            
            if(self.verb):
                print 'TTTCCCGGGEEENNN - ',basin
                print 'otcgenpath:     ',otcgenpath,otcgenpathStat
                print 'otcgensinkpath: ',otcgensinkpath,otcgensinkpathStat
                print 'ofile:          ',ofile,ofileStat

                if(self.doTrk3):
                    print 'otcgensnk2path: ',otcgensnk2path,otcgensnk2pathStat
                    print 'otcgenextrpath: ',otcgenextrpath,otcgenextrpathStat
                
            if(self.doTrk3):
                otcgenPaths[basin]=(otcgenpath,otcgensinkpath,otcgensnk2path,otcgenextrpath,ofile)
            else:
                otcgenPaths[basin]=(otcgenpath,otcgensinkpath,ofile)


        for basin in tcgenBasins:
            if(statTCgenS[basin] <= 0):
                statusTCgen=0
                break

        # -- TTTTTTTTTTTTTTTTTTTTTTTTTTCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS
        #
        # -- TTTTCCCC - get tcV for this dtg
        #
        self.tcV=self.tcD.getTCvDtg(self.dtg)
        
        # -- TTTTCCCC - set up tcvitals and tracker i/o paths -- cp tcvitals do not ln ... and don't write out file
        #
        writefile=1
        if(dolsonly): writefile=0
        verbTCV=0
        if(self.dolstcs): verbTCV=1
        
        self.tcVcards=self.tcV.makeTCvCards(override=self.override,filename='tcvitals',verb=verbTCV,writefile=writefile)
        self.tcvpath=self.tcV.tcvpath

        haveTcs=0
        if(len(self.tcVcards) > 0): haveTcs=1
        self.haveTcs=haveTcs

        # -- PPPPPAAAAATTTTTHHHHHSSSSS - paths for trtrk if TCs
        #
        otctrkPaths={}


        if(self.haveTcs):

            statusTCtrk=1
            
            if(hasattr(self,'tcVcards')):
                tcvits=self.tcVcards
                tcvits=tcvits.split('\n')
            else:
                tcvits=open(self.tcvpath).readlines()
                
            self.tcvits=tcvits

            ostmids=[]
            
            statTCtrkS={}
            
            for tcvit in tcvits:

                if(len(tcvit) == 0): continue
                
                stm3id=tcvit.split()[1]
                ostmid=self.get4stm3id(stm3id,self.tcV.stmids)
                if(ostmid != None):
                    ostmids.append(ostmid)
                    ostmyear=ostmid.split('.')[1]

                    tdirAdeckStm="%s/%s"%(self.tbdirAdeckStm,ostmyear)
                    if(not(dolsonly)):
                        MF.ChkDir(tdirAdeckStm,'mk')

                otctrkpathSTM    ="tctrk.atcf.%s.%s.%s.txt"%(self.dtg,omodel,stm3id.lower()) # fort.64 - standard
                #otctrkgtcvpathSTM="tctrk.gtcv.%s.%s.%s.txt"%(self.dtg,omodel,stm3id.lower()) # fort.67 - genesis tcvitals

                if(ostmid != None):
                    otctrkpathSTM="%s/tctrk.atcf.%s.%s.%s"%(tdirAdeckStm,self.dtg,omodel,ostmid.upper())
                    otctrksinkpathSTM="%s/tctrk.sink.%s.%s.%s"%(tdirAdeckStm,self.dtg,omodel,ostmid.upper())
                    otctrkpathSTMStat=MF.getPathSiz(otctrkpathSTM)
                    otctrksinkpathSTMStat=MF.getPathSiz(otctrksinkpathSTM)
                    statTCtrkS[ostmid]=otctrkpathSTMStat
                    
                    if(self.doTrk3):
                        otctrksnk2pathSTM="%s/tctrk.snk2.%s.%s.%s"%(tdirAdeckStm,self.dtg,omodel,ostmid.upper())
                        otctrkWradpathSTM="%s/tctrk.wrad.%s.%s.%s"%(tdirAdeckStm,self.dtg,omodel,ostmid.upper())
                        otctrkWfrcpathSTM="%s/tctrk.wfrc.%s.%s.%s"%(tdirAdeckStm,self.dtg,omodel,ostmid.upper())
                        otctrkWikepathSTM="%s/tctrk.wike.%s.%s.%s"%(tdirAdeckStm,self.dtg,omodel,ostmid.upper())
                        otctrkWpdfpathSTM="%s/tctrk.wpdf.%s.%s.%s"%(tdirAdeckStm,self.dtg,omodel,ostmid.upper())
                        otctrksnk2pathSTMStat=MF.getPathSiz(otctrksnk2pathSTM)
                        otctrkWradpathSTMStat=MF.getPathSiz(otctrkWradpathSTM)
                        otctrkWfrcpathSTMStat=MF.getPathSiz(otctrkWfrcpathSTM)
                        otctrkWikepathSTMStat=MF.getPathSiz(otctrkWikepathSTM)
                        otctrkWpdfpathSTMStat=MF.getPathSiz(otctrkWpdfpathSTM)

                else:
                    otctrkpathSTMStat=0
                    otctrksinkpathSTMStat=0

                    
                ofile="%s/stdout.tctrk.%s.%s.%s.txt"%(self.tdir,self.dtg,omodel,stm3id.lower())
                ofileStat=MF.getPathSiz(ofile)

                if(self.verb):
                    print 'TTTCCCTTTRRRKKK  - ',ostmid
                    print 'otctrkpathSTM:     ',otctrkpathSTM,otctrkpathSTMStat
                    print 'otctrksinkpathSTM: ',otctrksinkpathSTM,otctrksinkpathSTMStat
                    print 'ofile:             ',ofile,ofileStat

                    if(self.doTrk3):
                        print 'otctrksnk2pathSTM: ',otctrksnk2pathSTM,otctrksnk2pathSTMStat
                        print 'otctrkWradpathSTM: ',otctrkWradpathSTM,otctrkWradpathSTMStat
                        print 'otctrkWfrcpathSTM: ',otctrkWfrcpathSTM,otctrkWfrcpathSTMStat
                        print 'otctrkWikepathSTM: ',otctrkWikepathSTM,otctrkWikepathSTMStat
                        print 'otctrkWpdfpathSTM: ',otctrkWpdfpathSTM,otctrkWpdfpathSTMStat

                if(self.doTrk3):
                    otctrkPaths[ostmid]=(otctrkpathSTM,
                                         otctrksinkpathSTM,otctrksnk2pathSTM,
                                         otctrkWradpathSTM,otctrkWfrcpathSTM,
                                         otctrkWikepathSTM,otctrkWpdfpathSTM,
                                         ofile)
                else:
                    otctrkPaths[ostmid]=(otctrkpathSTM,
                                         otctrksinkpathSTM,
                                         ofile)

            for ostmid in ostmids:
                nzero=0
                nthere=0
                if(statTCtrkS[ostmid] <= 0):
                    nzero=nzero+1
                elif(statTCtrkS[ostmid] > 0):
                    nthere=nthere+1
                    

            if(nthere == 0):
                statusTCtrk=0
        else:
            statusTCtrk=-1
 
        self.omodel=omodel
        self.otcgenPaths=otcgenPaths
        self.otctrkPaths=otctrkPaths
        self.statTCgenS=statTCgenS
        self.statTCtrkS=statTCtrkS
        self.statusTCgen=statusTCgen
        self.statusTCtrk=statusTCtrk
         
        # -- test for tcgen and tctrk grib paths
        #
        #genTest=(                   not(os.path.exists(self.grb10path)) and (statusTCgen == 0) )
        #detTest=( (self.haveTcs and not(os.path.exists(self.grbpath)))  and (statusTCtrk == 0) )

        self.genTest= (self.statusTCgen == 0) 
        self.detTest= (self.haveTcs == 1 and self.statusTCtrk == 0) 
        
        self.genGribTest=(MF.getPathSiz(self.grb10path) > 0)
        self.detGribTest=(MF.getPathSiz(self.grbpath) > 0)
        

    def setStatus(self):

        print
        print 'SSSSSSSSSSSSSSSSSSSSSS - tracking status for ',self.omodel,' dtg: ',self.dtg
        print 'TCs  haveTcs: ',self.haveTcs
        print 'GRIB  -- gen: ',self.genGribTest
        print 'GRIB  -- trk: ',self.detGribTest
        print 'DDDD detTest: ',self.detTest
        print 'GGGG genTest: ',self.genTest
        if(not(self.detTest) and not(self.genTest) and not(self.override)):
            print 'AAAAAAAAAAAAAAAAAAAAAAAAAA - tracking alldone for ',self.omodel,' dtg: ',self.dtg,\
                  ' detTest: %1d'%(int(self.detTest)),' genTest: %1d '%(int(self.genTest)),' press---------------'
            rc=0
        else:
            print 'DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD - doit.....'
            rc=1
        print
        return(rc)
    
    
    def doLS(self):
        
        lbasin='lant'
        #self.setStatus()
        (gdir,gfile)=os.path.split(self.otcgenPaths[lbasin][0])
        tfile=os.path.split(self.otctrkpath)[-1]
        gsiz=self.statTCgenS[lbasin]
        tsiz=self.otctrkpathStat
        
        print 'Tdir: %-100s'%(gdir.replace('//','/'))
        print 'DetTrkAll: %6d  %-75s '%(tsiz,tfile)
        print 'Gen[%s]: %6d  %-75s'%(lbasin,gsiz,gfile)


    def doTrk(self,
              dotrkonly=0,
              dogenonly=0,
              ropt='',
              dowindow=0,
              gaopt='-g 1024x768',
              quiet=0,
              ):


        # -- print current status...and bail if done
        #
        rc=self.setStatus()
        if(rc == 0):
            return
        
        # -- CCCCCTTTTTDDDDDIIIIIRRRRR - change to tdir, so can run mulitply instances
        #
        rc=MF.ChangeDir(self.tdir,verb=1)
        
        # -- start timer
        #
        MF.sTimer(tag='all')


        # -- GGRRIIBB - 1.0 deg data for tcgen -- make grads obj
        #
        didGenGrib=0
        if( ((self.genTest and not(self.genGribTest)) or self.override) and ropt != 'norun'):

            MF.sTimer('latstcgen')
            ga=setGA(Opts=gaopt,Quiet=quiet,Window=dowindow,Bin=self.xgrads,verb=self.verb)
            ga.fh=ga.open(self.ctlpath)
            ge=ga.ge

            self.gribArea='areaGen'
            rc=self.gribInput2TmTrk(ga,ge,self.dtg,self.model,self.taus,self.grb10path,regrid=self.regridGen,smth2d=0)
            MF.dTimer('latstcgen')
            didGenGrib=1
            
        # -- GGRRIIBB - full res (0.5 deg)  data for tracker mode
        #
        didTrkGrib=0
        if( ( (self.detTest and not(self.detGribTest)) or self.override) and ropt != 'norun'):
            MF.sTimer('latstctrk')
            ga2=setGA(Opts=gaopt,Quiet=quiet,Window=dowindow,Bin=self.xgrads,verb=self.verb)
            ga2.fh=ga2.open(self.ctlpath)
            ge2=ga2.ge

            self.gribArea='area'
            rc=self.gribInput2TmTrk(ga2,ge2,self.dtg,self.model,self.taus,self.grbpath,regrid=self.regridTracker,dotrkonly=dotrkonly)
            MF.dTimer('latstctrk')
            dotracker=1
            didTrkGrib=1

        # -- CCCCCHHHHHEEEEECCCCCKKKKK - if no grib then bail - and get status...
        #
        if(didGenGrib == 0 and didTrkGrib == 0 and not(self.detTest) and not(self.genTest)):
            self.setStatus()
            print 'WWWW -- not gribs to do tracker...returning...'
            return


        # -- GGRRIIBB - make index files and kill the grads process...
        #
        if( not(os.path.exists(self.grbix10path)) or didGenGrib ):
            cmd="time %s/grbindex.x %s %s"%(self.prcdir,self.grb10path,self.grbix10path)
            MF.runcmd(cmd,ropt)
            
        if( not(os.path.exists(self.grbixpath))   or didTrkGrib ):
            cmd="time %s/grbindex.x %s %s"%(self.prcdir,self.grbpath,self.grbixpath)
            MF.runcmd(cmd,ropt)
            

        # -- TTMMTTRRKK - make fcst_minutes file for both tracker and tcgen mode
        #
        ifcmin='./fcst_minutes'
        fcmin=self.makeFcst_minutes()
        MF.WriteString2Path(fcmin,ifcmin)
        
        if(os.path.exists(ifcmin)):
            cmd="ln -f -s %s fort.15"%(ifcmin)
            MF.runcmd(cmd,ropt,lsopt='q')

        # -- TTMMTTRRKK - only run deterministic tracker if there are TCs...
        #
        if(self.haveTcs):

            if(self.tcvpath != None and os.path.exists(self.tcvpath) and self.haveTcs):
                cmd="cp %s fort.12"%(self.tcvpath)
                MF.runcmd(cmd,ropt,lsopt='q')

                # -- 3.9a uses this file for tcvitals
                #
                if(self.doTrk3):
                    cmd="cp %s tcvit_rsmc_storms.txt"%(self.tcvpath)
                    MF.runcmd(cmd,ropt,lsopt='q')
                
                
            else:
                print 'WWW(TCtrk) no tcvitals for ',self.dtg,' in: ',self.tcvpath
                haveTcs=0


            if(os.path.exists(self.grbpath)):
                cmd="ln -f -s %s fort.11"%(self.grbpath)
                MF.runcmd(cmd,ropt)

            if(os.path.exists(self.grbixpath)):
                cmd="ln -f -s %s fort.31"%(self.grbixpath)
                MF.runcmd(cmd,ropt)

            # --- make namelist for tracker mode
            #
            nltctrk='namelist.tctrk'
            if(self.doTrk3):
                namelist=self.makeNamelist3(self.trkmode)
            else:
                namelist=self.makeNamelist(self.trkmode)
                
            MF.WriteString2File(namelist,nltctrk)

            
            # -- cycle by storms, in case one fails...
            #
            
            for tcvit in self.tcvits:

                if(len(tcvit) == 0): continue

                print 'TTT - tracking: ',tcvit
                stm3id=tcvit.split()[1]
                stmpath="fort.12.%s"%(stm3id)
                MF.WriteString2File(tcvit,stmpath)
                
                if(self.doTrk3):
                    cmd="cp %s tcvit_rsmc_storms.txt"%(stmpath)
                    MF.runcmd(cmd,ropt,lsopt='q')
                    
                    
                ostmid=self.get4stm3id(stm3id,self.tcV.stmids)

                if(self.doTrk3):
                    (otctrkpathSTM,
                     otctrksinkpathSTM,otctrksnk2pathSTM,
                     otctrkWradpathSTM,otctrkWfrcpathSTM,
                     otctrkWikepathSTM,otctrkWpdfpathSTM,
                     ofile)=self.otctrkPaths[ostmid]
                else:
                    (otctrkpathSTM,
                     otctrksinkpathSTM,
                     ofile)=self.otctrkPaths[ostmid]

                if((self.statTCtrkS[ostmid] <= 0) or self.override):

                    try:     os.unlink(self.otctrkpath)
                    except:  cmd="touch %s"%(self.otctrkpath); mf.runcmd(cmd,ropt,lsopt='q')
                    try:     os.unlink(self.otctrksinkpath)
                    except:  cmd="touch %s"%(self.otctrksinkpath); mf.runcmd(cmd,ropt,lsopt='q')
                    if(self.doTrk3):
                        try:     os.unlink(self.otctrksnk2path)
                        except:  cmd="touch %s"%(self.otctrksnk2path); mf.runcmd(cmd,ropt,lsopt='q')
                    
                    cmd="ln -f -s %s fort.12"%(stmpath)
                    MF.runcmd(cmd,ropt)
                    cmd="ln -f -s %s fort.64"%(otctrkpathSTM)
                    MF.runcmd(cmd,ropt)
                    cmd="ln -f -s %s fort.68"%(otctrksinkpathSTM)
                    MF.runcmd(cmd,ropt)
                    
                    if(self.doTrk3):
                        cmd="ln -f -s %s fort.69"%(otctrksnk2pathSTM)
                        MF.runcmd(cmd,ropt)
                        cmd="ln -f -s %s fort.72"%(otctrkWradpathSTM)
                        MF.runcmd(cmd,ropt)
                        cmd="ln -f -s %s fort.73"%(otctrkWfrcpathSTM)
                        MF.runcmd(cmd,ropt)
                        cmd="ln -f -s %s fort.74"%(otctrkWikepathSTM)
                        MF.runcmd(cmd,ropt)
                        cmd="ln -f -s %s fort.76"%(otctrkWpdfpathSTM)
                        MF.runcmd(cmd,ropt)

                    
                    # --- run tracker mode -- use full res data
                    #
                    tag="tctrk %s"%(stm3id)
                    MF.sTimer(tag)
                    cmd="time %s/%s < %s > %s"%(self.prcdir,self.trkApp,nltctrk,ofile)
                    MF.runcmd(cmd,ropt)
                    MF.dTimer(tag)
                    
                    cmd="cat %s >> %s"%(otctrkpathSTM,self.otctrkpath)
                    mf.runcmd(cmd,ropt,lsopt='q')
                    
                    cmd="cat %s >> %s"%(otctrksinkpathSTM,self.otctrksinkpath)
                    mf.runcmd(cmd,ropt,lsopt='q')
                    
                    if(self.doTrk3):
                        cmd="cat %s >> %s"%(otctrksnk2pathSTM,self.otctrksnk2path)
                        mf.runcmd(cmd,ropt,lsopt='q')
                    

        # -- TTMMTTRRKK - GGGEEENNNEEESSSIIISSS - tcgen mode -- always use 1.0 deg data -- by areas
        #
        if(os.path.exists(self.grb10path) ):
            cmd="ln -f -s %s fort.11"%(self.grb10path)
            MF.runcmd(cmd,ropt)

        if(os.path.exists(self.grbix10path) ):
            cmd="ln -f -s %s fort.31"%(self.grbix10path)
            MF.runcmd(cmd,ropt)


        trkmode='tcgen'
        
        # cycle by basins
        #
        for basin in tcgenBasins:
            
            # -- make all tcvitals here, in case we want to do tcvitals by basin
            #
            try:     os.unlink('fort.12')
            except:  None
            
            if(self.haveTcs):
                if(hasattr(self,'tcVcards')):
                    MF.WriteString2File(self.tcVcards,'fort.12')
                else:
                    self.tcV.makeTCvCards(override=self.override,filename='tcvitals',verb=1,writefile=1)
                    cmd="cp %s fort.12"%(self.tcV.tcvpath)
                    MF.runcmd(cmd,ropt,lsopt='q')

                    
            MF.sTimer(tag=basin)

            if(self.doTrk3):
                (otcgenpath,otcgensinkpath,otcgensnk2path,otcgenextrpath,ofile)=self.otcgenPaths[basin]
            else:
                (otcgenpath,otcgensinkpath,ofile)=self.otcgenPaths[basin]
            

            if( (self.statTCgenS[basin] <= 0) or self.override):

                nltcgen='namelist.tcgen.%s'%(basin)
                if(self.doTrk3):
                    namelist=self.makeNamelist3(trkmode,basin)
                else:
                    namelist=self.makeNamelist(trkmode,basin)
                MF.WriteCtl(namelist,nltcgen)
                
                # run in tcgen mode
                #
                cmd="ln -f -s %s fort.64"%(otcgenpath)
                MF.runcmd(cmd,ropt)
                cmd="ln -f -s %s fort.68"%(otcgensinkpath)
                MF.runcmd(cmd,ropt)
                if(self.doTrk3):
                    cmd="ln -f -s %s fort.69"%(otcgensnk2path)
                    MF.runcmd(cmd,ropt)
                    cmd="ln -f -s %s fort.66"%(otcgenextrpath)
                    MF.runcmd(cmd,ropt)
                    
                cmd="time %s/%s < %s > %s"%(self.prcdir,self.trkApp,nltcgen,ofile)
                MF.runcmd(cmd,ropt)
                
            MF.dTimer(tag=basin)

        # - CCCLLLEEEAAANNN - clean off working files in tdir
        #
        if(self.doClean): self.cleanTrk(ropt=ropt)
        
        MF.dTimer(tag='all')
        


    def cleanTrk(self,ropt=''):

        MF.ChangeDir(self.tdir)
        
        # -- only blow off ctlpath if in tdir
        #
        if(mf.find(self.ctlpath,self.tdir)):
            cmd="rm %s"%(self.ctlpath)
            mf.runcmd(cmd,ropt)

        cmd="rm  f*"
        mf.runcmd(cmd,ropt)

        if(self.doTrk3):
            cmd="rm  tcvit*"
            mf.runcmd(cmd,ropt)

        cmd="rm  namelist*"
        mf.runcmd(cmd,ropt)

        cmd="rm  *.grb*"
        mf.runcmd(cmd,ropt)

        cmd="rm  stdout*"
        mf.runcmd(cmd,ropt)


    def setFldGrid(self,ropt='',override=0):

        if(len(self.istmids) == 0):
            aa=TmTrkAreaGlobal()
            aa=None
        else:
            dx=dy=0.5
            if(self.regridTracker != 0): dx=dy=self.regridTracker
            self.hemigrid=getHemis(self.istmids)

            if(self.hemigrid == 'nhem'):   aa=TmTrkAreaNhem(dx=dx,dy=dy)
            if(self.hemigrid == 'shem'):   aa=TmTrkAreaShem(dx=dx,dy=dy)
            if(self.hemigrid == 'global'): aa=TmTrkAreaGlobal(dx=dx,dy=dy)

        self.area=aa
        dx=dy=1.0
        if(self.regridGen != 0): dx=dy=self.regridGen
        self.areaGen=TmTrkAreaTropics(dx=dx,dy=dy)

        # override to test with more general code
        #
        #self.area=W2areaGlobal()

    def setReargs(self,area):

        aa=area

        if(aa == None):
            print 'WWW(TmTrkN.setReargs) - doing -t?  need -t -O to regen the .pyp...if this fails...'
            
        if(self.remethod == ''):
            self.reargs="%d,%s,%f,%f,%d,%s,%f,%f"%(aa.ni,self.rexopt,aa.lonW,aa.dx,aa.nj,self.reyopt,aa.latS,aa.dy)
        else:
            self.reargs="%d,%s,%f,%f,%d,%s,%f,%f,%s"%(aa.ni,self.rexopt,aa.lonW,aa.dx,aa.nj,self.reyopt,aa.latS,aa.dy,self.remethod)

        if(not(self.doregrid)): self.reargs=None



    def makeNamelist(self,trkmode='tracker',basin='global'):

        dtg=self.dtg
        atcfname=self.atcfname

        cc=dtg[0:2]
        yy=dtg[2:4]
        mm=dtg[4:6]
        dd=dtg[6:8]
        hh=dtg[8:10]

        modtyp='global'
        gridtype='global'

        if(hasattr(self,'area') and mf.find(trkmode,'tracker') ):
            lat1=self.area.latS
            lat2=self.area.latN
            lon1=self.area.lonW
            lon2=self.area.lonE
            modtyp='regional'
            gridtype='regional'

        elif(hasattr(self,'areaGen') and mf.find(trkmode,'tcgen') ):
            lat1=self.areaGen.latS
            lat2=self.areaGen.latN
            lon1=self.areaGen.lonW
            lon2=self.areaGen.lonE
            modtyp='regional'
            gridtype='regional'

        # -- get search lat/lon based on basin
        #
        (lat1,lat2,lon1,lon2)=self.getBasinLatLons(basin)

        if(trkmode == 'trackeronly'):
            trkmode='tracker'
            pflag='n'
        elif(trkmode == 'tracker'):
            pflag='y'
        elif(trkmode == 'tcgen'):
            pflag='y'
        else:
            print 'EEE invalid trkmode: ',trkmode
            sys.exit()


        if(hasattr(self,'searchLatS')): lat1=self.searchLatS
        if(hasattr(self,'searchLatN')): lat2=self.searchLatN

        # -- pull last 4 char from name -- limitation of gettrk_genN.x application
        #
        atcfnameNL=atcfname[-4:]

        # ---- turn off tcstruct
        #
        namelist="""&datein
  inp%%bcc=%s,
  inp%%byy=%s,
  inp%%bmm=%s,
  inp%%bdd=%s,
  inp%%bhh=%s,
  inp%%model=17,
  inp%%modtyp='%s',
  inp%%lt_units='hours'
  inp%%file_seq='onebig',
  inp%%nesttyp='',
/
&atcfinfo
  atcfnum=83,
  atcfname='%s',
  atcfymdh=%s
/
&trackerinfo
  trkrinfo%%southbd=%5.1f,
  trkrinfo%%northbd=%5.1f,
  trkrinfo%%westbd=%5.1f,
  trkrinfo%%eastbd=%5.1f,
  trkrinfo%%type='%s',
  trkrinfo%%mslpthresh=0.0015,
  trkrinfo%%v850thresh=1.5000,
  trkrinfo%%gridtype='%s',
  trkrinfo%%contint=100.0,
  trkrinfo%%out_vit='y'
/
&phaseinfo 
  phaseflag='%s',
  phasescheme='both',
  wcore_depth=1.0
/
&structinfo 
  structflag='n',
  ikeflag='n'
/
&fnameinfo
  gmodname='gfso',
  rundescr='xxxx',
  atcfdescr='xxxx'
/
&verbose
  verb=2
/
"""%(cc,yy,mm,dd,hh,modtyp,atcfnameNL,dtg,lat1,lat2,lon1,lon2,trkmode,gridtype,pflag)

        return(namelist)

    def makeNamelist3(self,trkmode='tracker',basin='global'):

        dtg=self.dtg
        atcfname=self.atcfname

        cc=dtg[0:2]
        yy=dtg[2:4]
        mm=dtg[4:6]
        dd=dtg[6:8]
        hh=dtg[8:10]

        modtyp='global'
        gridtype='global'

        if(hasattr(self,'area') and mf.find(trkmode,'tracker') ):
            lat1=self.area.latS
            lat2=self.area.latN
            lon1=self.area.lonW
            lon2=self.area.lonE
            modtyp='regional'
            gridtype='regional'

        elif(hasattr(self,'areaGen') and mf.find(trkmode,'tcgen') ):
            lat1=self.areaGen.latS
            lat2=self.areaGen.latN
            lon1=self.areaGen.lonW
            lon2=self.areaGen.lonE
            modtyp='regional'
            gridtype='regional'

        # -- get search lat/lon based on basin
        #
        (lat1,lat2,lon1,lon2)=self.getBasinLatLons(basin)
        
        sflag='y'

        if(trkmode == 'trackeronly'):
            trkmode='tracker'
            pflag='n'
        
        elif(trkmode == 'tracker'):
            pflag='y'

        elif(trkmode == 'tcgen'):
            pflag='y'
            sflag='n'

        else:
            print 'EEE invalid trkmode: ',trkmode
            sys.exit()


        if(hasattr(self,'searchLatS')): lat1=self.searchLatS
        if(hasattr(self,'searchLatN')): lat2=self.searchLatN

        # -- pull last 4 char from name -- limitation of gettrk_genN.x application
        #
        atcfnameNL=atcfname[-4:]

        # ---- turn on tcstruct for version 3.9a
        #
        namelist="""&datein
  inp%%bcc=%s,
  inp%%byy=%s,
  inp%%bmm=%s,
  inp%%bdd=%s,
  inp%%bhh=%s,
  inp%%model=17,
  inp%%modtyp='%s',
  inp%%lt_units='hours'
  inp%%file_seq='onebig',
  inp%%nesttyp='',
/
&atcfinfo
  atcfnum=83,
  atcfname='%s',
  atcfymdh=%s
/
&trackerinfo
  trkrinfo%%southbd=%5.1f,
  trkrinfo%%northbd=%5.1f,
  trkrinfo%%westbd=%5.1f,
  trkrinfo%%eastbd=%5.1f,
  trkrinfo%%type='%s',
  trkrinfo%%mslpthresh=0.0015,
  trkrinfo%%v850thresh=1.5000,
  trkrinfo%%gridtype='%s',
  trkrinfo%%contint=100.0,
  trkrinfo%%out_vit='y'
  trkrinfo%%use_land_mask = "n",
  trkrinfo%%inp_data_type = "grib",
  trkrinfo%%gribver = 1,
  trkrinfo%%g2_jpdtn = 0,
  trkrinfo%%g2_mslp_parm_id = 192,
  trkrinfo%%g1_mslp_parm_id = 2,
  trkrinfo%%g1_sfcwind_lev_typ = 105,
  trkrinfo%%g1_sfcwind_lev_val = 10,

/
&phaseinfo 
  phaseflag='%s',
  phasescheme='both',
  wcore_depth=1.0
/
&structinfo 
  structflag='%s',
  ikeflag='%s'
/
&fnameinfo
  gmodname='gfso',
  rundescr='xxxx',
  atcfdescr='xxxx'
/
&parmpreflist
  user_wants_to_track_zeta700 = "y",
  user_wants_to_track_wcirc850 = "y",
  user_wants_to_track_wcirc700 = "y",
  user_wants_to_track_gph850 = "y",
  user_wants_to_track_gph700 = "y",
  user_wants_to_track_mslp = "y",
  user_wants_to_track_wcircsfc = "y",
  user_wants_to_track_zetasfc = "y",
  user_wants_to_track_thick500850 = "y",
  user_wants_to_track_thick200500 = "y",
  user_wants_to_track_thick200850 = "y",
  user_wants_to_track_zeta850 = "y",
/
&verbose
  verb=0,
  verb_g2=0,
/
"""%(cc,yy,mm,dd,hh,modtyp,atcfnameNL,dtg,lat1,lat2,lon1,lon2,trkmode,gridtype,pflag,
     sflag,sflag)

        return(namelist)

    def makeFcst_minutes(self):

        for n in range(0,len(self.taus)):
            nn=n+1
            if(n == 0):
                fcmin='''%2d %7d'''%(nn,self.taus[n]*60)
            else:
                fcmin='''%s
%2d %7d'''%(fcmin,nn,self.taus[n]*60)

        return(fcmin)

    def setFldVars(self):
        
        zgmfact=1.0/gravity

        uavars=[]
        uavars.append(('ua','instant',[850,700,500]))
        uavars.append(('va','instant',[850,700,500]))
        uavars.append(('zg','instant',[900,850,800,750,700,650,600,550,500,450,400,350,300],zgmfact,None))
        uavars.append(('ta','instant',[401]))
        
        self.uavars=uavars

        svars=[]
        svars.append(('psl','instant'))
        svars.append(('uas','instant'))
        svars.append(('vas','instant'))

        self.svars=svars
        
        

    def gribInput2TmTrk(self,ga,ge,dtg,model,taus,grbpath,
                        regrid=0,dotrkonly=0,smth2d=0):


        areaObj=None
        if(hasattr(self,'gribArea')):
            if(self.gribArea == 'areaGen' and hasattr(self,'areaGen')):
                areaObj=self.areaGen
                self.setReargs(areaObj)

        if(hasattr(self,'gribArea')):
            if(self.gribArea == 'area' and hasattr(self,'area')):
                areaObj=self.area
                self.setReargs(areaObj)

        latS=latN=lonW=lonE=None
        if(areaObj != None):
            latS=areaObj.latS
            latN=areaObj.latN
            lonW=areaObj.lonW
            lonE=areaObj.lonE


        (topath,ext)=os.path.splitext(grbpath)

        reargs=None
        if(hasattr(self,'reargs')): reargs=self.reargs


        # -- make galats object
        #
        gl=GaLatsQ(ga,ge,
                   dtg=dtg,model=model,taus=taus,
                   regrid=regrid,
                   reargs=reargs,
                   smth2d=smth2d,
                   ptable=self.ptable,
                   )

        gl.create(topath)
        gl.basetime(dtg)
        gl.grid(areaObj)

        self.setFldVars()
        uavars=self.uavars
        svars=self.svars
        

        if(len(uavars) > 0):
            gl.plevdim(uavars)

        gl.plevvars(uavars)

        gl.sfcvars(svars)

        gl.outvars(svars,uavars,verb=0)
        gl.close()

        rc=0

        return(rc)



    def getBasinLatLons(self,basin):

        if(basin == 'global'):
            lat1=-30.0
            lat2=30.0
            lon1=0.0
            lon2=359.0

        elif(basin == 'lant'):

            lat1=0.0
            lat2=30.0
            lon1=360.0-100.0
            lon2=360.0-10.0

        elif(basin == 'epac'):

            lat1=0.0
            lat2=30.0
            lon1=180.0
            lon2=360.0-75.0

        elif(basin == 'wpac'):

            lat1=0.0
            lat2=30.0
            lon1=100.0
            lon2=180.0

        elif(basin == 'shem'):

            lat1=-30.0
            lat2=0.0
            lon1=35.0
            lon2=360.0-150.0

        elif(basin == 'nio'):

            lat1=0.0
            lat2=30.0
            lon1=40.0
            lon2=100.0

        else:
            print 'EEE invalid basin in getBasinLatLon: ',basin
            sys.exit()

        return(lat1,lat2,lon1,lon2)


