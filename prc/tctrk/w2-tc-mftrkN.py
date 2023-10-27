#!/usr/bin/env python

from tcbase   import *
from TCtrk    import TmTrk
from TCdiag   import tcdiagModels
from TCmftrk  import mfTracker
from TCtmtrkN import TmTrkN,getCtlpathTaus


class mfTrackerN(mfTracker,TmTrk):


    remethod='ba'
    remethod='bl'
    remethod='' # use re default for change in res  'ba' for fine->coarse and 'bl' for coarse->fine
    
    rexopt='linear'
    reyopt='linear'
    
    def __init__(self,model,dtg,
                 area=None,
                 taus=None,
                 tauoffset=0,
                 vars=None,
                 doregrid=1,
                 tdir=None,
                 tbdir='/dat3/tc/mftrk',
                 ctlpath=None,
                 mintauTC=120,
                 maxtauTC=168,   # try to run tracker for 168 h
                 doLogger=0,
                 Quiet=1,
                 verb=0,
                 doByTau=1,
                 version=1.1,
                 adecksource='wxmap2',
                 dbname='invMftrkN',
                 doInvOnly=0,
                 diag=1,
                 trackerName='mftrkN',
                 trackerAdmask="wxmap2*",
                 ):

        from M2 import setModel2

        self.trackerName=trackerName
        self.trackerAdmask=trackerAdmask

        self.model=model

        # -- WxMAP2.py has the capability to do tau offset
        #
        mdtg=mf.dtginc(dtg,-tauoffset)
        print 'DDDDDDDDDDDDDDDDDDDDDDddd',tauoffset,dtg,'model dtg',mdtg
       
        self.dtg=dtg
        self.mdtg=mdtg
        self.tauoffset=tauoffset        
        self.area=area
        self.taus=taus
        self.tauoffset=tauoffset
        self.vars=vars
        self.doregrid=doregrid
        self.tbdir=tbdir
        self.maxtauTC=maxtauTC
        self.GAdoLogger=doLogger
        self.GAQuiet=Quiet
        self.dpaths={}
        self.sstdpath=None
        self.areaname=None
        self.verb=verb
        self.doByTau=doByTau
        self.version=version
        self.adecksource=adecksource
        self.prcdir="%s/tctrk"%(os.getenv("W2_PRC_DIR"))

        # -- inventory
        #
        self.dbname=dbname
        self.dbfile="%s.pypdb"%(dbname)
        self.dsbdir="%s/DSs"%(tbdir)
        MF.ChkDir(self.dsbdir,'mk')

        # -- inventory
        #
        MF.sTimer('setDSs')

        self.DSs=DataSets(bdir=self.dsbdir,name=self.dbfile,dtype=self.dbname,verb=verb)
        MF.dTimer('setDSs')
        self.dbkeyLocal='local'
        
        try:
            self.dsL=self.DSs.getDataSet(key=self.dbkeyLocal,verb=verb)
            self.invN=self.dsL.data
        except:
            self.dsL=DataSet(name=self.dbkeyLocal,dtype='hash')
            self.invN={}

        self.setTCs()
        if(ctlpath == None): return 

        # -- get m2 object with model details
        #
        self.m2=setModel2(model)
        
        # -- set grid before setting vars
        #
        if(area == None): self.setGridMFtracker()

        # -- abspath tdir set here
        #
        self.setCtl(ctlpath,tbdir)
        self.initVars()
        self.initNgtrkVars()
        self.setNgtrkOutput(verb=verb)

        if(doInvOnly): return 
        self.setNgtrp(verb=verb)

        filename="%s.%s"%(self.model,self.dtg)
        self.setOutput(filename=filename)
        self.setNgtrkNl()

        if(not(mintauTC in self.taus)):
            print 'WW insufficient taus...latest: ',self.taus[-1]
            self.enoughTaus=0
        else:
            self.enoughTaus=1
        



#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# command line setup
#
class TmtrkCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv
        
        self.argv=argv
        self.argopts={
            1:['dtgopt',    'dtgs'],
            2:['modelopt',  """models: MMM1 | MMM1,MMM2,...,MMMn | 'all'"""],
            }

        self.defaults={
            'doupdate':0,
            'doAdeck2':1,
            }

        self.options={
            'override':          ['O',0,1,'override'],
            'overrideDatChk':    ['D',0,1,'override DataGENoverride'],
            'verb':              ['V',0,1,'verb=1 is verbose'],
            'ropt':              ['N','','norun',' norun is norun'],
            'dols':              ['l',0,1,'1 - list'],
            'dolsLong':          ['L',0,1,'1 - list'],
            'doClean':           ['K',1,0,'0 - do NOT clean up .dat files'],
            'doCleanOnly':       ['k',0,1,'0 - just clean up .dat files'],
            'dotrkonly':         ['t',0,1,'1 - force running of tracker'],
            'TMoverride':        ['M',0,1,'1 - run only in tracker mode'],
            'doTmtrkClean':      ['c',1,0,'do NOT clean tmtrkN'],
            'doTmtrkZip':        ['Z',1,0,'do NOT make YYYYMM.zip archive of tmtrkN adecks'],
            'doInv':             ['I',0,1,'1 - do inventory of trker'],
            'doAnl':             ['A',0,1,'1 - analyze inventory'],
            'doCpAdeck':         ['C',0,1,'only cp adecks to adeck directory'],
            'doAdeckuPdate':     ['U',1,0,'do NOT update the adeck'],
            'doNgtrk2AdeckOnly': ['a',0,1,'only convert the ngtrk output to adeck'],
            'doAdcO1':           ['1',1,0,'do NOT set O1 option in adc'],
            'mintauTC':          ['m:',132,'i','set the minimum tau to run tracker [132]'],

            }

        self.purpose="""
run new version of Mike's 3-fix tracker"""
        
        self.examples='''
%s cur12 fim8'''
        
        self.models=['gfs2','fim8','ecm2','ecm4','ukm2','navg','cmc2','rtfim9']
        self.models0618=['gfs2','ukm2','navg']

        self.models=['gfs2','cgd2','ecm5','navg','ecmt']
        self.models0618=['gfs2','navg']



#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
# main
#

dowindow=0
gaopt='-g 1024x768'

argv=sys.argv
CL=TmtrkCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

dtgs=mf.dtg_dtgopt_prc(dtgopt)

models=modelopt.split(',')
if(len(models) > 1 or modelopt == 'all' or len(dtgs) > 1):

    if(modelopt == 'all'): allmodels=CL.models

    for dtg in dtgs:

        allmodels=models
        if(modelopt == 'all'):
            if(dtg[8:10] == '06' or dtg[8:10] == '18'): allmodels=CL.models0618
            else:                                         allmodels=CL.models
           
        for model in allmodels:
            cmd="%s %s %s"%(CL.pypath,dtg,model)
            for o,a in CL.opts:
                cmd="%s %s %s"%(cmd,o,a)
            mf.runcmd(cmd,ropt,lsopt='')

    sys.exit()

else:
    model=modelopt


if(doNgtrk2AdeckOnly):
    doTmtrkClean=0
    doClean=0

if(doClean == 0):
    doTmtrkClean=0
    
TRKoverride=0
if(dotrkonly or override): TRKoverride=1
    
ctlpath=None

MF.sTimer('mftrkN')

for dtg in dtgs:

    # -- check if status of
    #
    tcA=TcAidTrkAd2Bd2(dtgopt=dtg,verb=verb,source='mftrkN')
    
    if(dols or dolsLong):
        rc=tcA.getStatus(modelChk=model,doPrint=1)
        continue
        #sys.exit()
    
    
    rc=tcA.getStatus(modelChk=model,doPrint=1)
    
    if(doCpAdeck):
        print 'doCpAdeck rc tcA.getStatus: ',rc,' press...'
    
    elif(rc == 1 and not(override)):
        print 'tcA.getStatus() == 1 for dtg: ',dtg,' model: ',model,' source: mftrkN'
        print 'override != 1 so bail...'
        sys.exit()

    elif(rc == 0):
        print 'need to run..... dtg: ',dtg,' model: ',model,'......'
        if(ropt == 'norun'):
            print 'bailing because -N'
            sys.exit()
        
    
    cpTrkDone=0

    if(model == 'rtfim9' or model == 'ukmc'): mintauTC=120
    
    # -- old form...tcA=TcAidTrk(dtg)
    #tcA.lsTC()

    MF.sTimer('MTC-dtg')
    MF.sTimer('MTC-TmTrkN')
    
    (ctlpath,taus,nfields,tauOffset)=getCtlpathTaus(model,dtg)
    if(ctlpath == None):
        print 'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW no data for model: ',model,' dtg: ',dtg,' .... '
        sys.exit()
    
    xgrads=setXgrads(useX11=1)
    #xgrads='grads'
    
    # -- tim's tracker object for ctlfiles
    #
    TT=TmTrkN(dtg,model,ctlpath,taus,
              mintauTC=mintauTC,
              maxtauModel=None,
              xgrads=xgrads,
              doInventory=1)

    if(not(TT.enoughTaus) and not(overrideDatChk)):
        print 'EEE(%s): TT.enoughTaus: %d'%(pyfile,TT.enoughTaus)
        sys.exit()

    runTmTrk=TT.chkInv(verb=verb) or TMoverride and not(dols) and not(dolsLong) and not(doNgtrk2AdeckOnly)
    if(doCpAdeck or dotrkonly): runTmTrk=0
    
    if(runTmTrk):
        TT=TT.doTrk(doClean=0,GRIBoverride=TMoverride,TToverride=TMoverride)

    MF.dTimer('MTC-TmTrkN')

    # -- set the ctlpath
    #
    if(not(MF.ChkPath(TT.grbpath)) or override):
        MFctlpath=ctlpath
        MFarea=None

    else:
        MFctlpath=TT.grbctlpath
        MFarea=TT.area
        if(not(dols) and not(dolsLong) and not(doInv)):
            TT.setGrads(type='trk',override=override)
            TT.setGrads(type='gen',override=override)

    # -- my tracker
    #

    MF.sTimer('MTC-mftrkN')
    
    mintauTC=132
    if(model == 'rtfim9'): mintauTC=120

    mfT=mfTrackerN(model,dtg,area=MFarea,
                   taus=None,
                   tauoffset=tauOffset,
                   tbdir=TT.tbdir,
                   mintauTC=mintauTC,
                   ctlpath=MFctlpath,
                   doregrid=1,doByTau=1,
                   doInvOnly=doInv,
                   verb=verb)

    MF.dTimer('MTC-mftrkN')

    rcABefore=mfT.chkAdecks()
    
    # -- brute force cleaning -- normally done through f77Output class in WxMAP2
    #
    if(doCleanOnly):
        #mfT.clean() from WxMAP2
        (dir,file)=os.path.split(mfT.dpath)
        files=glob.glob("%s/%s*.f???.dat"%(dir,model))
        print 'CCCCCCConly nfiles: ',len(files)
        for file in files:
            os.unlink(file)

        sys.exit()

    # -- convert to adeck only
    #
    if(doNgtrk2AdeckOnly):
        MF.sTimer('MTC-adeck')
        mfT.ngtrk2Adeck(docpLocal=0,verb=verb)
        MF.dTimer('MTC-adeck')
        continue
        

    if(not(mfT.enoughTaus)):
        print 'EEE mfT.enoughTaus = 0'
        sys.exit()
    
    # -- cp to tc/adecks
    #
    if(doCpAdeck):
        mfT.cpTrackers2AdeckDir()
        sys.exit()

    # -- do inventory
    #
    if(doInv):
        mfT.invTrk(override=override)
        MF.dTimer('MTC-mftrkN')
        sys.exit()
        
    # -- ls
    #
    if(dols or dolsLong):
        lsopt='s'
        if(dolsLong): lsopt='l'
        mfT.lsAdecks(lsopt=lsopt)
        continue

    if(mfT.chkAdecks() and not(TRKoverride)):
        print 'WWWWWWWWWWWWWWWWWWWW not(TRKoverride) and mfT.chkAdecks()'
        continue

    MF.sTimer('MTC-fldinput')
    if(ropt == ''):
        mfT.makeFldInput(override=override,doconst0=0)
    MF.dTimer('MTC-fldinput')

    
    MF.sTimer('MTC-trk')
    if(ropt == ''):
        mfT.runTracker(override=TRKoverride)
    MF.dTimer('MTC-trk')

    MF.sTimer('MTC-adeck')
    if(ropt == ''):
        mfT.ngtrk2Adeck(docpLocal=0,verb=verb)
    MF.dTimer('MTC-adeck')

    if(ropt == 'norun'): sys.exit()

    if(ropt == ''):
        mfT.cpTrackers2AdeckDir()
        cpTrkDone=1

    MF.dTimer('MTC-dtg')


if(dols or dolsLong):
    MF.dTimer('mftrkN')
    sys.exit()
    
rcAAfter=mfT.chkAdecks()
if(rcABefore and rcAAfter and not(override)): doAdeckuPdate=0

# -- update adeck2
#
if(doAdeckuPdate):

    if(doAdeck2):
        
        # -- this now makes AD2 for both NN and 9X
        #
        oopt=''
        if(doAdcO1): oopt='-O1'
        
        ss=pyfile.split('.')
        srcType=ss[0].split('-')[-1]
        
        adcCmd='w2-tc-convert-tm-mftrkN-to-atcf-adeck.py'
        adkCmd='w2-tc-dss-adeck.py'
        
        MF.sTimer('ADC-AD2-update')
        cmd="%s/%s %s -d %s -A"%(w2.PrcDirTcdatW2,adcCmd,srcType,dtg)
        mf.runcmd(cmd,ropt)
        MF.dTimer('ADC-AD2-update')

        MF.sTimer('adk-in-ad2-update')
        cmd="%s/%s %s -u -d %s"%(w2.PrcDirTcdatW2,adkCmd,srcType,dtg)
        mf.runcmd(cmd,ropt)
        MF.dTimer('adk-in-ad2-update')
        
    else:
        
        MF.sTimer('adk-update')
        cmd="%s/%s %s -u -d %s"%(w2.PrcDirTcdatW2,adkCmd,srcType,dtg)
        mf.runcmd(cmd,ropt)
        MF.dTimer('adk-update')


if(doTmtrkZip):
    MF.sTimer('adk-ZIP-mftrkN')
    cmd="%s/w2-tc-zip-adeck-tmtrkN.py %s -S mftrkN"%(w2.PrcDirTcdatW2,dtg)
    mf.runcmd(cmd,ropt)
    MF.dTimer('adk-ZIP-mftrkN')
    
MF.dTimer('mftrkN')
    

