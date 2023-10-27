#!/usr/bin/env python

from WxMAP2 import *
w2=W2()

from TCtmtrkN import TmTrkN,getCtlpathTaus
from tcbase import TcData,TcAidTrkAd2Bd2

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
            'override':         ['O',0,1,'override'],
            'GRIBoverride':     ['G',0,1,'GRIBoverride'],
            'TToverride':       ['T',0,1,'TToverride'],
            'GENoverride':      ['e',0,1,'GENoverride'],
            'overrideDatChk':   ['D',0,1,'override DataGENoverride'],
            'verb':             ['V',0,1,'verb=1 is verbose'],
            'ropt':             ['N','','norun',' norun is norun'],
            'dols':             ['l',0,1,'1 - list'],
            'doInv':            ['I',0,1,'1 - do inventory of trker'],
            'dolsLong':         ['L',0,1,'1 - long list'],
            'doClean':          ['K',0,1,'1 - os.unlink fort.?? and i/o files'],
            'doCleanTrk':       ['x',0,1,'clean trk files in TT.doTrk method'],
            'doCleanAll':       ['k',0,1,'kill off tmtrk*'],
            'dowindow':         ['W',0,1,'do grads window'],
            'dotrkonly':        ['t',0,1,'1 - run only in tracker mode'],
            'dogenonly':        ['g',0,1,'1 - do genesis tracker only'],
            'doAnl':            ['A',0,1,'1 - analyze inventory'],
            'doCpAdeck':        ['c',0,1,'1 - analyze inventory'],
            'doAdeckuPdate':    ['U',1,0,'do NOT update the adeck'],
            'doRelabel':        ['R',0,1,'relabel the tracks to NNB.YYYY'],
            'dorsync2kaze':     ['r',0,1,'1 - rsync 2 kaze if on kishou, default is to NOT...when do retro runs on kishou'],
            'doMFtrkN':         ['M',0,0,'ALWAYS do NOT MF tracker after...now done in w2-tc-runTrks.py'],
            'doTmtrkZip':       ['Z',1,0,'do NOT make YYYYMM.zip archive of tmtrkN adecks'],
            'doTmtrkZipAtEnd':  ['z',0,1,'make YYYYMM.zip archive of trk-tmtrkN adecks'],
            'doChkIfRunning':   ['r',1,0,'no NOT chk if running'],
            'doAdcO1':          ['1',1,0,'do NOT set O1 option in adc'],
            'mintauTC':         ['m:',132,'i','set the minimum tau to run tracker [132]'],
            'chkAd2Tracker':    ['C:',0,'i','check of tracker has been done for NN only (1) or both NN&9X (2)'],

        }

        self.purpose="""
run new version of Tim Marchok's genesis tracker"""

        self.examples='''
%s cur12 gfs2'''

        self.models=    ['gfs2','ecm5','cgd2','navg']
        self.models0618=['gfs2','navg']
        
        if(w2.Nwp2ModelsActW20012 != None): self.models=w2.Nwp2ModelsActW20012
        self.models.append('ecmt')
        
        if(w2.Nwp2ModelsActW20618 != None): self.models0618=w2.Nwp2ModelsActW20618

        self.purpose="""
run new version of Tim Marchok's genesis tracker
00/12 Models: %s
06/18 Models: %s"""%(self.models,self.models0618)

        self.examples='''
%s cur12 gfs2'''

def cycleDtgsModels(dtgopt,modelopt):

    dtgs=mf.dtg_dtgopt_prc(dtgopt)
    models=modelopt.split(',')

    if(len(models) > 1 or modelopt == 'all' or len(dtgs) > 1):

        for dtg in dtgs:

            if(modelopt == 'all'):
                models=CL.models
                if(MF.is0618Z(dtg)): models=CL.models0618

            for model in models:
                cmd="%s %s %s -r"%(CL.pypath,dtg,model)
                for o,a in CL.opts:
                    cmd="%s %s %s"%(cmd,o,a)
                mf.runcmd(cmd,ropt,lsopt='')

        sys.exit()

    else:
        model=modelopt
        dtg=dtgs[0]

    return(dtg,model)


def invAnl(dtgopt,modelopt):


    dtgs=mf.dtg_dtgopt_prc(dtgopt)
    models=modelopt.split(',')

    TT=TmTrkN(dtg=None,model=None,ctlpath=None,taus=None,maxtauModel=None,doInvOnly=1)

    inv=TT.invTmtrkN

    kk=inv.keys()

    dtgs=[]
    sumStms={}

    for k in kk:

        if(len(k) <= 2): continue

        if(mf.find(k[2],'sumStm')): 
            dtg=k[0]
            model=k[1]

            tt=inv[k]
            tt=inv[k].split()
            good=tt[2]
            fail=tt[4]
            stop=tt[6]

            dtgs.append(dtg)
            val="%s %s %s %s"%(model,good,fail,stop)
            MF.appendDictList(sumStms,dtg,val)


    dtgs=mf.uniq(dtgs)
    dtgs.sort()

    for dtg in dtgs:
        print dtg,sumStms[dtg]


    sys.exit()

def getAllCheck(tcA,model,dtg,dolsLong,dorcPrint=0):
    
    if(dolsLong):
        rc=tcA.getStatus(modelChk=model,doPrint=1)
    else:
        rc=tcA.getStatus(modelChk=model,doPrint=0)
        rc2=tcA.getStatus(modelChk=model,doPrint=0,returnAd2=2)
        if(dorcPrint):
            if(rc == 1):
                if(rc2[0] == 0 and rc2[1] == 0):
                    print "RC1 ALLL -- GOOD for model: ",model,'dtg: ',dtg,' but NO STORMS to track'
                else:
                    print "RC1 ALLL -- GOOD for model: ",model,'dtg: ',dtg
            else:
                print "RC1 ALLL -- NOT good DAME desu YO! model: ",model,'dtg: ',dtg
                rc2=None
                return(rc,rc2)
        
    
    if(dorcPrint):
        
        rc2=tcA.getStatus(modelChk=model,doPrint=0,returnAd2=2)
    
        # -- NN storms
        #
        if(rc2[0] == -3):
            print "RC2 NNNN -- OKAY tracker -- SHEM|IO subbasin mislabelled ----->>>>> ",rc2[2].upper(),' <<<<<----- model: ',model,'dtg: ',dtg
        elif(rc2[0] == -2):
            print "RC2 NNNN -- OKAY tracker -- ran on ALL storms but FAILED on one or more storms model: ",model,'dtg: ',dtg
        elif(rc2[0] == -1):
            print "RC2 NNNN -- !!!!!!!! need to run tracker for NNNN storms NOT run for model: ",model,'dtg: ',dtg
        elif(rc2[0] == 1):
            print "RC2 NNNN -- GOOD tracker for NN ad2 model: ",model,'dtg: ',dtg
         
        # -- 9X storms
        #
        if(rc2[1] == -3):
            print "RC2 99XX -- OKAY tracker -- SHEM|IO subbasin mislabelled ----->>>>> ",rc2[3].upper(),' <<<<<----- model: ',model,'dtg: ',dtg
        elif(rc2[1] == -3):
            print "RC2 99XX -- OKAY tracker -- ran on ALL storms but FAILED on one or more storms model: ",model,'dtg: ',dtg
        elif(rc2[1] == -1):
            print "RC2 99XX -- !!!!!!!! need to run tracker for 99XX storms NOT run for model: ",model,'dtg: ',dtg
        elif(rc2[1] == 1):
            print "RC2 99XX -- GOOD tracker for 9X ad2 model: ",model,'dtg: ',dtg
        
    return(rc,rc2)
    

#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# main
#

# -----------------------------------  default setting of max taus
#
maxtau=168

argv=sys.argv
CL=TmtrkCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

MF.sTimer('tmtrkN')

# -- check if running...if other at the same dtg...???
#
if(doChkIfRunning):
    nminWait=30
    jobopt="%s"%(dtgopt)
    rc=MF.chkRunning(pyfile, setJobopt=jobopt, strictChkIfRunning=0, verb=0, 
                     killjob=0, timesleep=10, nminWait=nminWait)
    
# -- set options
#
if(doRelabel): dols=1
dolsonly=(dols or dolsLong)

# -- analyze the inventory and exit
#
if(doAnl): invAnl(dtgopt,modelopt)

(dtg,model)=cycleDtgsModels(dtgopt,modelopt)

# -- use the new class to get status of run
#
tcA=TcAidTrkAd2Bd2(dtgopt=dtg,verb=verb)

# -- lllllllllllllllllllllllllllllllllllllllllllllllll dols and bail...
#
if(dols or dolsLong):
    (rc,rc2)=getAllCheck(tcA,model,dtg,dolsLong,dorcPrint=1)
    MF.dTimer('tmtrkN')
    sys.exit()


# -- check if already run in two ways:
#  1 - basic check
#  2 - if there are missing runs of the tracker for NN and/or 9X storms
#
(rc,rc2)=getAllCheck(tcA,model,dtg,dolsLong,dorcPrint=1)

if(chkAd2Tracker == 1):
    if(rc2 != None and rc2[0] != 1):
        dotrkonly=1
        override=1
        rc=0
        print 'NNNNNN -- chkAd2Tracker!!! redo NN storms only...'
        
elif(chkAd2Tracker == 2):
    if((rc2 != None and (rc2[0] != 1) or (rc2[1] != 1))):
        dotrkonly=1
        override=1
        rc=0
        print '999NNN -- chkAd2Tracker!!! redo NN & 9X storms...'
        
# -- basic check point after ad2 check
#
if(rc == 1):
    if(not(override) and not(doClean) and not(doCpAdeck)):
        print 'tcA.getStatus() == 1 for dtg: ',dtg,' model: ',model
        print 'override != 1 so bail...'
        sys.exit()
    
elif(rc == 0):
    print 'need to run..... dtg: ',dtg,' model: ',model,'......'
    if(ropt == 'norun'):
        print 'bailing because -N'
        sys.exit()

# -- kkkkkkkkkkkkkkkkkkkkkkk all -- with killing all files <= dtgout
#
if(doCleanAll):
    MF.sTimer('tmtrkN-cleanAll')
    TT=TmTrkN(None,None)
    TT.cleanAllFiles(dtgopt=dtgopt)
    MF.dTimer('tmtrkN-cleanAll')
    sys.exit()



# -- test age of dtg, of too old, don't do rsync2kaze
#
howold=mf.dtgdiff(dtg,curdtg)/24.0
tooold=(howold > w2.W2MaxOldRegen)
if(tooold):  dorsync2kaze=0

# -- tryarch inside here...set in w2switches
#
(ctlpath,taus,nfields,tauOffset)=getCtlpathTaus(model,dtg,maxtau=maxtau)

if(ctlpath == None and doClean == 0 and doRelabel == 0 and dolsonly == 0):
    print 'EEE(%s) no ctl for model: %s'%(pyfile,model),' dtg: ',dtg
    sys.exit()


# -- set all overrides if override
if(override):
    if(not(TToverride)): TToverride=1
    if(not(GRIBoverride)): GRIBoverride=1    
    if(not(GENoverride) and not(dotrkonly)): GENoverride=1    

# -- make a new TT if only doing track?
#
#if(dotrkonly): TToverride=1

# -- set grads
#
xgrads=setXgrads()
#xgrads='grads'

# -- make tracker object
#
MF.sTimer('tmtrkN-base')
TT=TmTrkN(dtg,model,ctlpath,taus,maxtau,
          nfields=nfields,
          mintauTC=mintauTC,
          dols=dolsonly,
          xgrads=xgrads,
          override=override)
MF.dTimer('tmtrkN-base')


# -- relabel adecks with NNN.YYYY
#
if(doRelabel):
    TT.relabelAdeckDirTrackers(verb=verb)
    MF.dTimer('tmtrkN')
    sys.exit()


# -- data status check
#
dchk=(not(TT.enoughTaus) or not(TT.datataus))
ochk=not(overrideDatChk)
if( dchk and ochk ):
    print 'EEE bailing because not(TT.enoughTaus):',TT.enoughTaus,' or not(TT.datataus):',TT.datataus
    TT.ls()
    MF.dTimer('tmtrkN')
    sys.exit()

# -- cleaning of files
#
if(doClean):
    print 'tmtrkN KKK only...'
    TT.cleanFiles()
    MF.dTimer('tmtrkN')
    sys.exit()

# -- cp of adecks to adeck dir/
#

if(doCpAdeck):
    TT.cpTrackers2AdeckDir()
    TT.relabelAdeckDirTrackers()
    
    MF.dTimer('tmtrkN')
    sys.exit()

# -- do inventory
#
if(doInv):
    TT.invTrk()
    MF.dTimer('tmtrkN')
    sys.exit()

# -- ttttttttttttttttttttttttttttttttttttttt actual tracking ttttttttttttttttttttttttttttttttttttttttttttttttttttt
#

# -- do data and tracking
#

TT=TT.doTrk(
    dotrkonly=dotrkonly,
    dogenonly=dogenonly,
    doClean=doCleanTrk,
    override=override,
    dowindow=dowindow,
    dolsonly=dolsonly,
    TToverride=TToverride,
    GRIBoverride=GRIBoverride,
    GENoverride=GENoverride,
)

rcTrkAfter=TT.allreadydone

# -- do not run adk if TT.allreadydone = -1 (do chking) = 1 (all ready done) = 0 (ran the tracker)
#
if(rcTrkAfter and not(override)): doAdeckuPdate=0

# -- put grads .ctl/.gmp on grib from TT.
#
if(not(doCleanTrk) and rcTrkAfter == 0):
    if(not(dogenonly)): TT.setGrads(type='trk',override=override)
    TT.setGrads(type='gen',override=override)

# -- cp trackers to adeckdir and relabel to tctrk*.NNB.YYYY if override or tracking done
#
if(rcTrkAfter >= 0 or override):  
    TT.cpTrackers2AdeckDir()
    TT.relabelAdeckDirTrackers()


# -- do zip here of tmtrkN only ... then do the trk-tmtrkN AFTER mftrkN the uses data ... in tmtrkN
#
if(doTmtrkZip):
    MF.sTimer('adk-ZIP-tmtrkN')
    cmd="%s/w2-tc-zip-adeck-tmtrkN.py %s -S tmtrkN"%(w2.PrcDirTcdatW2,dtg)
    mf.runcmd(cmd,ropt)
    MF.dTimer('adk-ZIP-tmtrkN')

# -- update adeck2
#
if(doAdeckuPdate):
    
    if(doAdeck2):
        # -- this makes AD2 for both NN and 9X
        #
        oopt=''
        if(doAdcO1): oopt='-O1'

        # -- 20201006 changed the filename from . to -
        #
        #pytfile.split('.')[0].split('-')[-1]
        ss=pyfile.split('.')
        srcType=ss[0].split('-')[-1]

        adcCmd='w2-tc-convert-tm-mftrkN-to-atcf-adeck.py'
        adkCmd='w2-tc-dss-adeck.py'

        MF.sTimer('ADC-AD2-update')
        cmd="%s/%s %s -d %s -A %s"%(w2.PrcDirTcdatW2,adcCmd,srcType,dtg,oopt)
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


# -- if running on kishou, put to kaze even though it comes back in rsync
#
if(onKishou and dorsync2kaze):
    # -- problem with setting this????
    MF.sTimer('tmtrkN-rsync2kaze')
    tdirKaze=TT.tdir.replace('/w21',w2.DATKazeBaseDir)
    cmd="rsync --protocol=29 -alv %s/*.txt %s"%(TT.tdir,tdirKaze)
    mf.runcmd(cmd,ropt)
    MF.dTimer('tmtrkN-rsync2kaze')

    
# -- run mftrkN -- zip is done in mftrkN
#
if(doMFtrkN):
    MF.sTimer('tmtrkN-doMFtrkN')
    overopt=''
    if(override): overopt='-O'
    adkupopt=''
    if(not(doAdeckuPdate)): adkupopt='-U'
    cmd='%s/w2-tc-mftrkN.py %s %s %s %s'%(w2.PrcDirTctrkW2,dtgopt,model,overopt,adkupopt)
    mf.runcmd(cmd,ropt)
    MF.dTimer('tmtrkN-doMFtrkN')

# -- NOW zip trk-tmtrkN????  if another ttc is running? -- no 20191228
#
if(doTmtrkZipAtEnd):
    roptZip='norun'
    roptZip=ropt
    MF.sTimer('adk-ZIP-tmtrkN')
    cmd="%s/w2-tc-zip-adeck-tmtrkN.py %s -S trk-tmtrkN"%(w2.PrcDirTcdatW2,dtg)
    mf.runcmd(cmd,roptZip)
    MF.dTimer('adk-ZIP-tmtrkN')

MF.dTimer('tmtrkN')
