#!/usr/bin/env python

from WxMAP2 import *
w2=W2()
from M import *
MF=MFutils()

from M2 import setModel2
from tcVM import findtcs,getTstmidsAD2FromStmoptDtgopt,getStmParams,Is9X,getStmSiz
from adVM import getAdeck2Bdeck2DSs
from TCtrk import tcgenModels
from TCdiag import tcdiagModels,tcdiagModels0618
from tcbase import TcData,TcAidTrkAd2Bd2
        
        
df2Chk=['centos','/dev/sd','hgfs','Filesy']
df2Exclude=[]

models2Chk=['gfs2','goes','navg','ecm5','ecmt','cgd2','jgsm']
modelsW2=['gfs2','navg','ecm5','cgd2','jgsm']
modelsW20012=modelsW2
modelsW20618=['gfs2','navg','jgsm']
nModW206=len(modelsW20618)
nModW200=len(modelsW20012)
    
modelsNwp2=['goes']
modelsExtra=['ecmt']

modelsChk={
    'gfs2':['cur-%s.%s.6','-W','24'],
    'jgsm':['cur-%s.%s.6','-W','24'],
    'ukm2':['cur-%s.%s.6','-W','24'],
    'navg':['cur-%s.%s.6','-W','24'],
    'goes':['cur-%s.%s.6','','24'],
    'ecm4':['cur12-%s.%s.12','-W','36'],
    'ecm5':['cur12-%s.%s.12','-W','36'],
    'cmc2':['cur12-%s.%s.12','-W','36'],
    'ecmt':['cur12-%s.%s-d2.12','-W','d7'],
    'cgd2':['cur12-%s.%s.12','-W','36'],
    }

def getModelCron(verb=0):
    
    cmd="crontab -l | grep -i ptmpdir | grep -v \# | grep -i do\-"
    cards=MF.runcmdLog(cmd,quiet=1)
    cmd="crontab -l | grep -i ptmpdir | grep -v \# | grep -i goes-loop"
    gcards=MF.runcmdLog(cmd,quiet=1)
    cmd="crontab -l | grep -i ptmpdir | grep -v \# | grep -i ecmt"
    ecards=MF.runcmdLog(cmd,quiet=1)

    modtimes={}
    for card in cards:
        if(len(card) == 0): continue
        tt=card.split()
        if(verb): print 'ttt',tt[1],len(tt)
        times=tt[1].strip()
        model=tt[6].split('/')
        model=model[-1][3:7]
        if(mf.find(card,'goes')):
            model='goes'
        MF.appendDictList(modtimes, model, times)

    if(len(gcards) == 2):
        for gcard in gcards:
            if(len(gcard) == 0): continue
            tt=gcard.split()
            if(verb): print 'ggg',tt[1],len(tt)
            times=tt[1].strip()
            model='goes'
            MF.appendDictList(modtimes, model, times)
        
    if(len(ecards) == 3):
        for ecard in ecards:
            if(len(ecard) == 0): continue
            tt=ecard.split()
            if(verb): print 'ggg',tt[1],len(tt)
            times=tt[1].strip()
            model='ecmt'
            MF.appendDictList(modtimes, model, times)
            break
                    
    kk=modtimes.keys()
    models=mf.uniq(kk)
    if(verb): print models
    for model in models:
        mts=modtimes[model]
        times=[]
        for mt in mts:
            mt.replace(""",""",'')
            mt=mt.split(',')
            for t in mt:
                it=int(t)
                if(model == 'goes'):
                    if((it-1)%6 == 0):
                        itm1=it-1
                        times.append(itm1)
                    times.append(it)
                else:
                    times.append(it)
                
                if(model == 'ecmt'):
                    itp1=it+1
                    times.append(itp1)
                    times.append(it)

        times.sort()
                    
        times.sort()
        modtimes[model]=times
    
    if(verb):
        for model in models:
            modtimes[model]=MF.uniq(modtimes[model])
            print 'mmmm',model,modtimes[model]
        
    return(modtimes)

def getIfModelRunning(ldtg,model,modtimes,curPSs,verb=0):
    curtime=int(mf.dtg('curtime')[0:2])
    rcc=0
    rcp=0
    for ps in curPSs:
        if(verb): print 'ps: ',ps
        for p in ps:
            if(verb): print 'ff',p,model,mf.find(p,model)
            if(mf.find(p,model)): rcp=1
    if(curtime in modtimes[model]): rcc=1
    if(verb): print 'rrrr',rcc,rcp,curtime,modtimes[model]
    return(rcc,rcp)
    
        

def getL2QprStatus(dtgs,nhback=12,verb=0):
    
    maxfilesHr=nhback+1
    maxfilesPr=maxfilesHr/2
    doP=not(WarnOnly)
    doW=not(doP)

    def GetQprFiles(source,dtype):

        if(source == 'qmorph'):
            sdir=w2.NhcQmorphFinalLocal
            sdirp=w2.NhcQmorphProductsGrib
        elif(source == 'cmorph'):
            sdir=w2.NhcCmorphFinalLocal
            sdirp=w2.NhcCmorphProductsGrib

        stitle=source.upper()

        year=yyyymm[0:4]
        yearm1=yyyymmm1[0:4]
        
        sfiles={}
        if(dtype == 'input'):
            mask="%s/%s/*%s*"%(sdir,year,yyyymm)
            maskm1="%s/%s/*%s*"%(sdir,yearm1,yyyymmm1)

            files=glob.glob(maskm1)+glob.glob(mask)
            for sfile in files:
                dtg=long(sfile.split(".")[-2])
                sfiles[dtg]=sfile
            title='hourly:'
            maxfiles=maxfilesHr

        elif(dtype == 'prod'):
            mask="%s/%s/*h_%s????.grb"%(sdirp,year,yyyymm)
            maskm1="%s/%s/*h_%s????.grb"%(sdirp,yearm1,yyyymmm1)

            files=glob.glob(maskm1)+glob.glob(mask)
            for sfile in files:
                dtg=long(sfile.split("_")[-1].split('.')[0])
                sfiles[dtg]=sfile            
            title='6-h products'
            maxfiles=maxfilesPr

        elif(dtype == 'globalprod'):
            mask="%s/%s/*h_global_%s????.grb"%(sdirp,year,yyyymm)
            maskm1="%s/%s/*h_global_%s????.grb"%(sdirp,yearm1,yyyymmm1)
            
            files=glob.glob(maskm1)+glob.glob(mask)
            for sfile in files:
                dtg=long(sfile.split("_")[-1].split('.')[0])
                sfiles[dtg]=sfile
            title='6-h GLOBAL products'
            maxfiles=maxfilesPr

        sdtgs=sfiles.keys()
        sdtgs.sort(key=int)
        nsdtgs=len(sdtgs)

        if(nsdtgs == 0):
            print 'WWW-l2.GetQprFiles no files for dtype: ',dtype
        else:
            files=[]
            nfback=nsdtgs-maxfiles
            if(nfback < 0): nfback=0
            for n in range(nsdtgs-1,nfback,-1):
                files.append(sfiles[sdtgs[n]])

        return(files,stitle,title)


    def PrintQprFiles(files,stitle,title,flen=80):

        print
        print "%s %s"%(stitle,title)
        for ffile in files:
            siz=MF.getPathSiz(ffile)
            fformat="%%-%ds"%(flen)
            print fformat%(ffile),' siz: %8d'%(siz)

    def StatQprFiles(files,source,dtype,minSiz=1382568):

        qStatus=1
        lastdtg=dtgs[-1]
        lastfile=files[0]
        (pdir,pfile)=os.path.split(lastfile)
        pdtg=pfile.split('.')[-2]
        if(mf.find(pdtg,'_')):
            pdtg=pdtg.split('_')[-1]
        dddtg=mf.dtgdiff(pdtg,curdtg)
        if(source == 'qmorph' and dddtg > 6.0): qStatus=0
        if(source == 'cmorph' and dddtg > 36.0): qStatus=0
        # -- check file sizes
        siz0=MF.GetPathSiz(files[0])
        for pfile in files:
            siz=MF.GetPathSiz(pfile)
            ndx=files.index(pfile)
            if(verb and dtype == 'input'): print '%s input: '%(source.upper()),pfile,' siz: ',siz
            if(siz < minSiz and source == 'qmorph' and dtype == 'input' and ndx > 0):
                qStatus=0
            
        return(qStatus)
            


    sources=['qmorph','cmorph']
    dtypes=['input','prod','globalprod']

    yyyymm=curdtg[0:6]
    yyyymmm1=mf.yyyymminc(yyyymm,-1)

    # -- get len of ffile
    #
    flenmax=-999
    for source in sources:
        for dtype in dtypes:
            (files,stitle,title)=GetQprFiles(source,dtype)
            for ffile in files:
                fl=len(ffile)
                if(fl > flenmax): flenmax=fl

    print
    for source in sources:
        for dtype in dtypes:
            (files,stitle,title)=GetQprFiles(source,dtype)
            qStatus=StatQprFiles(files,source,dtype)
            if(qStatus == 0):
                PrintQprFiles(files,stitle,title,flen=flenmax)
            if(qStatus):
                print '%s DaIJyoUBu Desu -- QPR: %s : %-15s '%(daiJyoPre,source,dtype)
            else:
                print
                print '%s MoNDaI DaTa! -- QPR: %s:%s '%(monDaiPre,source,dtype)
                print
                
            #sys.exit()
    print
    print 'Curdtg: ',curdtg,' curphr: ',curphr
    print
    


#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# -- command line setup
#

class w2CmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv

        self.argv=argv
        self.argopts={
            1:['dtgopt',    'DTG (YYYYMMDDHH)'],
        }

        self.options={
            'verb':                 ['V',0,1,'verb=1 is verbose'],
            'override':             ['O',0,1,'override for models'],
            'ropt':                 ['N','','norun',' norun is norun'],
            'doByDtgs':             ['D',0,1,'use input dtgopt...do not convert -- applies to tct only now...'],
            'doMftrkN':             ['M',0,1,"""set source='mftrkN' for tct..."""],
            'chkType':              ['t:','all','a','type of check: [all] tc|qpr|df|prw|mod|eps|tcd|tct|tcp'],
            'nhback':               ['b:',0,'i','N hours back...'],
            'runTcRedo':            ['R',0,1,'run w2-tc-redo-All.py if problems only...'],
            'WarnOnly':             ['W',0,1,'warn if problems only...'],
            'doCronPrcChk':         ['C',1,0,'do NOT do cron/prc check...'],
            'chkModelsExtra':       ['E',1,0,'do NOT check models Extra (ecmt) pull broken since 20210619'],
        }

        self.defaults={
            'dow2flds':1,
            'diag':0,

        }

        self.purpose='''
check status of wxmap2 data and tcs
(c) 2009-%s Michael Fiorino,NOAA ESRL CIRES'''%(w2.curyear)

        self.examples='''
%s cur12 '''

#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# -- cmdline
#

argv=sys.argv

CL=w2CmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

daiJyoPre='--'
monDaiPre='************************'

MF.sTimer('all')

idtgopt=dtgopt
dtgs=mf.dtg_dtgopt_prc(dtgopt)

tdtgopt='cur-24.%s'%(idtgopt)
if(nhback > 0): tdtgopt='cur-%d.%s'%(nhback,idtgopt)

webdir=os.getenv('W2_BDIRWEB')
if(webdir == None): print 'bad env var for web' ; sys.exit()

prcdir=os.getenv('W2_PRC_DIR')
if(prcdir == None): print 'bad env var' ; sys.exit()

pldir="%s/plt_loop"%(webdir)
epsdir=w2.TcTcepsWebDir

tcddir=w2.tcdiagBaseDirWeb

tctdir="%s"%(w2.TcDatDirTMtrkN)

# -- get cur pids
#
curPidPSs=getCurrentPids(pyfile,doArgs=1)
curPSs=curPidPSs.values()
if(verb): print 'curPSs: ',str(curPSs)
modtimes=getModelCron()

# -- print status in tcd
#
printTCstatus=0

doModels=0 ; doQpr=0 ; doTCs=0 ; doPrw=0 ; doEps=0 ; doTcd=0 ; doTct=0 ; doDf=0 ; doTcp=0

    
if(chkType == 'prw'): 
    doPrw=1
elif(chkType == 'tc'): 
    doTCs=1
elif(chkType == 'eps'): 
    doEps=1
elif(mf.find(chkType,'mod')):  
    doModels=1
elif(chkType == 'tcd'):
    doTcd=1
elif(chkType == 'tct'):
    doTct=1
elif(chkType == 'tcp'):
    doTcp=1
elif(chkType == 'qpr'):
    doQpr=1
elif(chkType == 'df'): 
        doDf=1
elif(chkType == 'mike4'):
    doModels=1 ; doQpr=1 ; doTCs=1 ; doDf=1 
elif(chkType == 'gmu'):
    doModels=1 ; doQpr=1 ; doTCs=1 ; doDf=1 ; doPrw=1 ; doEps=1
# -- aori
elif(mf.find(chkType,'ao')):
    doModels=0 ; doQpr=1 ; doTCs=1 ; doPrw=0 ; doEps=1 ; doTcd=0 ; doTct=0 ; doDf=0 ; doTcp=0
else:
    doModels=1 ; doQpr=1 ; doTCs=1 ; doPrw=1 ; doEps=1 ; doTcd=1 ; doTct=1 ; doDf=1 ; doTcp=1
    
tD=TcData(dtgopt=tdtgopt)


doP=not(WarnOnly)
doW=not(doP)


# -- DDDDDDDDDDDDDDDDDDDDDDDDDFFFFFFFFFFFFFFFFFFFFFFFFFFFF
#
if(doDf):
    print; print 'DDDDDFFFFF -- file systems ' ; print
    ocards={}
    cmd="df -h"
    cards=MF.runcmdLog(cmd,quiet=1)
    for card in cards:
        doprint=1
        for df2x in df2Exclude:
            #print 'xxx',card,df2x
            if(mf.find(card,df2x)): doprint=0
            
        for df2 in df2Chk:
            if(mf.find(card,df2) and doprint):
                ckey=card.split()[-1]
                tt=ckey.split('/')
                if(len(tt) == 1): ctitle=card
                elif(len(tt) > 1): 
                    ckey=tt[1]
                    rc=MF.appendDictList(ocards,ckey,card)


    dkeys=ocards.keys()
    dkeys.sort()
    
    print ctitle
    for dkey in dkeys:
        cards=ocards[dkey]
        for card in cards:
            print card
    

# -- TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCSSSSSSSSSSSSSSSSSSSSSSSSSSS
#
if(doTCs):

    def getLen(tt,tmax=2):
        n=0
        for t in tt:
            if(mf.find(t,'-N') or mf.find(t,'NB')):continue
            if(len(t) > tmax): n=n+1
        return(n)
    
    MF.sTimer('TCs')

    cmd="%s/tcdat/w2-tc-posit.py"%(prcdir)
    m1cards=MF.runcmdLog(cmd,quiet=1)
    nm1=getLen(m1cards)

    md2dtgopt='cur'
    cmd="%s/tcdat/w2-tc-dss-md2-anl.py -d cur-24.%s -R"%(prcdir,md2dtgopt) # -R to get all tcs as used in ttc
    m2cards=MF.runcmdLog(cmd,quiet=1)
    nm2=getLen(m2cards)

    if(nm2 >= nm1):
        tcStatus=1
        
    elif(nm2 < nm1):
        tcStatus=-2
        
    elif(nm1 < nm2):
        tcStatus=0
        
    else:
        tcStatus=-1
        
        
    if(doP or (tcStatus == 0)):
        print
        print 'TTTTTCCCCC MMMMM111111111 -- TCs using mdecks '
        print
    
        for card in m1cards:
            if(mf.find(card,'-h for help')): continue
            print card[0:-1]

    print; print 'TTTTTCCCCC MMMMM222222222 -- TCs using mdecks2 for dtgopt: ',dtgopt
    for card in m2cards:
        print card
        
    tcPre='TTTCCCSSS------MDECK2'
    print tcPre,' nm1: ',nm1,' nm2: ',nm2
    if(tcStatus == 1): 
        print '%s DaIJyoUBu Desu -- %s dtgopt: %s'%(daiJyoPre,tcPre,dtgopt)
    else:
        print '%s MoNDaI DaTa! -- %s dtgopt: %s nm1: %2d nm2: %2d tcStatus: %d'%(monDaiPre,tcPre,dtgopt,nm1,nm2,tcStatus)
    print


    
    MF.dTimer('TCs')
        
# -- MMMMMMMMMMMMOOOOOOOOOOOOOOOOOOODDDDDDDDDDDDDDDDDDDEEEEEEEEEEEEEEELLLLLLLLLLLLLLLLLSSSSSSSSSSSSSSS
#
if(doModels or doTcd):
    
    ldtg=dtgs[-1]
    
    MF.sTimer('models')
    if(doP): print; print 'MMMMMOOOOODDDDDEEEELLLLLSSSSS -- models for dtgopt: ',dtgopt
    
    mDtgs=[]
    mStatus={}

    mDtgsW2=[]
    mStatusW2={}
    mMissW2={}
    
    mDtgsNwp2=[]
    mStatusNwp2={}
    
    mDtgsExtra=[]
    mStatusExtra={}
    
    # -- set max age for doing cron/prc test
    #
    maxDtgAgeW2=12.0
    maxDtgAgeExtra=72.0
    
    for dtg in dtgs:
        dtgsW2=[]
        dtgsNwp2=[]
        dtgsExtra=[]
        
        for model in models2Chk:
            rc=modelsChk[model]
            (mdtgopt,l2opt,bhr)=rc

            if(nhback > 0):
                if(model == 'ecmt'):
                    ndb=mf.nint(nhback/24)
                    ndb=6+ndb
                    bhr="d%d"%(ndb)
                else:
                    bhr=str(nhback)

            odtgopt=idtgopt
            if(model == 'ecmt'): odtgopt='cur12'
            mdtgopt=mdtgopt%(bhr,odtgopt)
        
            if(model in modelsW2):
                mdtgsw2=mf.dtg_dtgopt_prc(mdtgopt)
                dtgsW2=dtgsW2+mdtgsw2
                
            elif(model in modelsNwp2):
                mdtgsnwp2=mf.dtg_dtgopt_prc(mdtgopt)
                dtgsNwp2=dtgsNwp2+mdtgsnwp2
                
            elif(model in modelsExtra):
                mdtgsext=mf.dtg_dtgopt_prc(mdtgopt)
                dtgsExtra=dtgsExtra+mdtgsext
            
        dtgsW2.sort()
        dtgsW2=mf.uniq(dtgsW2)
         
        dtgsNwp2=mf.uniq(dtgsNwp2)
        dtgsNwp2.sort()
         
        dtgsExtra=mf.uniq(dtgsExtra)
        dtgsExtra.sort()
         
        
        for model in models2Chk:
            rc=modelsChk[model]
            (mdtgopt,l2opt,bhr)=rc

            # -- use dtg opt for w2 models for nwp
            #
            if(model in modelsW2 or model in modelsNwp2):
                # -- handle case of 12 and 6 h w2models
                #
                mdtgs=dtgsW2
                mdtgs.sort()
                mdtgb=mdtgs[0]
                mdtge=mdtgs[-1]
                # -- create dtgopt from begin / end of dtgs
                #
                mdtgoptw2="%s.%s.6"%(mdtgb,mdtge)
                mdtgs=mf.dtg_dtgopt_prc(mdtgoptw2)
                
            elif(model in modelsNwp2):
                mdtgs=dtgsNwp2
                
            elif(model in modelsExtra):
                mdtgs=dtgsExtra
            
            for mdtg in mdtgs:
                
                card=w2.getL2ModelStatus(model,l2opt,mdtg,override=override,verb=verb)
                tt=card.split()
                if(len(tt) == 0): continue
                
                cmodel=tt[0]
                cdtg=tt[1]
                cflag=1
                if(len(cdtg) > 10): cflag=cdtg[0] ; cdtg=cdtg[-10:]
                ctau=tt[2]
                ctime=tt[3]
                cnflds=tt[4]
                cdir=tt[5]
                if(cflag == 'L'): cflag=-1; cdir=None
                if(cflag == 'N'): cflag=-2; cdir=None
                if(cflag == '0'): cflag=-3; cdir=None
                cvalue=(cflag,cdtg,ctau,ctime,cnflds,cdir)
                # -- collect all
                #
                mDtgs.append(cdtg)
                rc=MF.appendDictList(mStatus,(cmodel,cdtg),cvalue)

                # -- collect W2 models
                #
                if(cmodel in modelsW2):
                    mDtgsW2.append(cdtg)
                    rc=MF.appendDictList(mStatusW2,(cmodel,cdtg),cvalue)
                # -- collect Nwp2 models
                #
                elif(cmodel in modelsNwp2):
                    mDtgsNwp2.append(cdtg)
                    rc=MF.appendDictList(mStatusNwp2,(cmodel,cdtg),cvalue)
                # -- collect Extra models
                #
                elif(cmodel in modelsExtra):
                    mDtgsExtra.append(cdtg)
                    rc=MF.appendDictList(mStatusExtra,(cmodel,cdtg),cvalue)

                #print 'ttt',len(tt),cmodel,cdtg,'cflag:',cflag,cdtg,ctau,ctime,cnflds,cdir
            
    mDtgs=mf.uniq(mDtgs)
    mDtgs.sort()
    
    mDtgsW2=mf.uniq(mDtgsW2)
    mDtgsW2.sort()
    
    mDtgsNwp2=mf.uniq(mDtgsNwp2)
    mDtgsNwp2.sort()
    
    mDtgsExtra=mf.uniq(mDtgsExtra)
    mDtgsExtra.sort()
    
    mStatW2={}
    mStatNwp2={}
    mStatExtra={}
    pcards=[]
    
    
    for dtg in mDtgsW2:
        if(MF.is0012Z(dtg)): models=modelsW20012
        else:                models=modelsW20618
        for model in models:
            ckey=(model,dtg)
            try:
                cstat=mStatusW2[ckey]
            except:
                cstat=None
                
            if(cstat != None):
                
                stat=cstat[0]
                dtgage=mf.dtgdiff(dtg,curdtg)

                # -- first check if not done...
                #
                if(stat[0] == -2): 
                    cout="%s <---- NNNNNNN --not done yet"%(stat[1])
                    mStatW2[model,dtg]=-1
                    mMissW2[model,dtg]='w2flds: %s %s'%(model,cout)
                # -- now check non-not-done
                #
                elif( (stat[0] != 1 and (dtgage <= maxDtgAgeW2) ) and doCronPrcChk):
                    if(verb):
                        print 'CHK-CHK-CHK'
                        print model,dtg,stat[0]
                    (rcc,rcp)=getIfModelRunning(dtg, model, modtimes, curPSs,verb=0)
                    if(rcc):
                        cout="%s --->>> ccccccc in crontab"%(stat[1])
                        mStatW2[model,dtg]=1
                    if(rcp):
                        cout="%s <<<--- pppppp processing"%(stat[1])
                        mStatW2[model,dtg]=1

                
                elif(stat[0] == 1): 
                    #cout="%s %6s %3s"%(stat[1],stat[2],stat[3])
                    cout="%s ww %3s  %5s  %2s  %s"%(stat[1],stat[2],stat[3],stat[4],stat[5])
                    mStatW2[model,dtg]=1
                elif(stat[0] == -1): 
                    #cout="%s %6s %3s"%(stat[1],stat[2],stat[3])
                    cout="%s ww %3s  %5s  %2s  <--- LLLLLLL --- low count --- LLLLLL"%(stat[1],stat[2],stat[3],stat[4])
                    mStatW2[model,dtg]=0
                    mMissW2[model,dtg]='w2flds: %s %s'%(model,cout)
                elif(stat[0] == -3): 
                    #cout="%s %6s %3s"%(stat[1],stat[2],stat[3])
                    cout="%s ww %3s  %5s  %2s  <--- 0000000 --- incomplete run"%(stat[1],stat[2],stat[3],stat[4])
                    mStatW2[model,dtg]=-2
                    mMissW2[model,dtg]='w2flds: %s %s'%(model,cout)
                else:
                    cout="%s <---- NNNNNNN --not done yet"%(stat[1])
                    mStatW2[model,dtg]=-1
                    mMissW2[model,dtg]='w2flds: %s %s'%(model,cout)
                    
                pcards.append('w2flds: %s %s'%(model,cout))
                
            else:
                for curPS in curPSs:
                    curJob=curPS[0]
                    curArgs=curps[1]
                    print 'model',model,curJob,curArgs
                    if(mf.find(curPS,model)):
                        print 'HHHH',model
                
                mStatW2[model,dtg]=-999
                pcards.append('WWWW----WWWW2222 missing for %s %s'%(dtg,model))

        pcards.append(' ')

    for dtg in mDtgsNwp2:
        models=modelsNwp2
        for model in models:
            ckey=(model,dtg)
            try:
                cstat=mStatusNwp2[ckey]
            except:
                cstat=None
                
            if(cstat != None):
                stat=cstat[0]
                if(stat[0] == 1): 
                    cout="%s nn %3s  %5s  %2s  %s"%(stat[1],stat[2],stat[3],stat[4],stat[5])
                    mStatNwp2[model,dtg]=1
                else:
                    cout="%s <---- not done yet"%(stat[1])
                    mStatNwp2[model,dtg]=-1
                pcards.append('nwp2:   %s %s'%(model,cout))
            else:
                pcards.append('WWWW----2222 missing for %s %s'%(dtg,model))
                mStatNwp2[model,dtg]=-999
                

    pcards.append(' ')

    if(not(chkModelsExtra)): mDtgsExtra=[]
    
    for dtg in mDtgsExtra:
        models=modelsExtra
        for model in models:
            ckey=(model,dtg)
            try:
                cstat=mStatusExtra[ckey]
            except:
                cstat=None
                
            if(cstat != None):
                
                stat=cstat[0]
                dtgage=mf.dtgdiff(dtg,curdtg)
                if( (stat[0] != 1 and dtgage <= maxDtgAgeExtra) and 
                    dtg != mDtgsExtra[-1] and doCronPrcChk):
                    if(verb):
                        print 'CHK-CHK-CHK'
                        print model,dtg,stat[0]
                    (rcc,rcp)=getIfModelRunning(dtg, model, modtimes, curPSs,verb=0)
                    if(rcc):
                        cout="%s --->>> ccccccc in crontab"%(stat[1])
                        mStatExtra[model,dtg]=1
                    if(rcp):
                        cout="%s <<<--- pppppp processing"%(stat[1])
                        mStatExtra[model,dtg]=1
                
                elif(stat[0] == 1): 
                    cout="%s -- %3s  %5s  %2s  %s"%(stat[1],stat[2],stat[3],stat[4],stat[5])
                    mStatExtra[model,dtg]=1
                else:
                    cout="%s <---- not done yet"%(stat[1])
                    if(dtg == mDtgsExtra[-1]):
                        mStatExtra[model,dtg]=1
                    else:
                        mStatExtra[model,dtg]=-1
                        
                pcards.append('extra:  %s %s'%(model,cout))
            else:
                pcards.append('WWWW----EEEE missing for: %s %s'%(dtg,model))
                mStatExtra[model,dtg]=-999
                

    if(doP):
        for pcard in pcards:
            print pcard


       
    mSW2=1
    for mk in mStatW2.keys():
        if(mStatW2[mk] < 0): 
            mSW2=0
            break
            
    mSNwp2=1
    for mk in mStatNwp2.keys():
        if(mStatNwp2[mk] < 0): 
            mSNwp2=0
            break

    mSExtra=1
    for mk in mStatExtra.keys():
        if(mStatExtra[mk] < 0): 
            mSExtra=0
            break
        
    print
    mW2Pre='MMOODDEELLSS---WWW222'
    mN2Pre='MMOODDEELLSS--NNWWPP2'
    mExPre='MMOODDEELLSS--EXTRAAA'
    
    if(mSW2): 
        print '%s DaIJyoUBu Desu -- %s dtgopt: %s '%(daiJyoPre,mW2Pre,dtgopt)
    else:
        print '%s MoNDaI DaTa! -- %s dtgopt: %s '%(monDaiPre,mW2Pre,dtgopt)
        print '%s missing W2 runs:'%(monDaiPre)
        if(len(mMissW2.keys()) > 0 ):
            for kk in mMissW2.keys():
                print "%s %s"%(monDaiPre,mMissW2[kk])
            print
            
            if(runTcRedo):
                prcdir=w2.PrcDirWxmap2W2

                for kk in mMissW2.keys():
                    tt=mMissW2[kk].split()
                    model=tt[1]
                    dtg=tt[2]
                    cmd="%s/do-%s.py %s -O"%(prcdir,model,dtg)
                    mf.runcmd(cmd,ropt)
                
    if(mSNwp2): 
        print '%s DaIJyoUBu Desu -- %s dtgopt: %s '%(daiJyoPre,mN2Pre,dtgopt)
    else:
        print '%s MoNDaI DaTa! -- %s dtgopt: %s '%(monDaiPre,mN2Pre,dtgopt)

    if(chkModelsExtra):
        if(mSExtra): 
            print '%s DaIJyoUBu Desu -- %s dtgopt: %s '%(daiJyoPre,mExPre,dtgopt)
        else:
            print '%s MoNDaI DaTa! -- %s dtgopt: %s '%(monDaiPre,mExPre,dtgopt)
    

    print
                 

    MF.dTimer('models')
            
# -- QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQPPPPPPPPPPPPPPPPPPRRRRRRRRRRRRRRRRRRRRRRRRRRRR
#
if(doQpr):
    
    MF.sTimer('qpr')
    if(doP): print; print 'QQQQQQQPPPPPPPPPRRRRRR -- qmorph for dtgopt: ',dtgopt 
    qprnhback=12
    if(nhback > 0): qprnhback=nhback
    rc=getL2QprStatus(dtgs,qprnhback,verb=verb)
    MF.dTimer('qpr')


# -- PPPPPPPPPPPPPPPRRRRRRRRRRRRRWWWWWWWWWWWWWWW
#
if(doPrw):

    MF.sTimer('prw')
    pstat={}
    nareas=len(w2.W2AreasPrw)
    if(nhback > 0):
        dtgs=mf.dtg_dtgopt_prc('cur-%d.%s'%(nhback,dtgopt))
    else:
        dtgs=mf.dtg_dtgopt_prc('cur-24.%s'%(dtgopt))

    for dtg in dtgs:
        pmask='%s/prw.gfs2.%s.*'%(pldir,dtg)
        gmask='%s/gfs.goes*%s*'%(pldir,dtg)
        pfiles=glob.glob(pmask)
        gfiles=glob.glob(gmask)
        npfiles=len(pfiles)
        ngfiles=len(gfiles)
        npmiss=npfiles-nareas
        ngmiss=ngfiles-nareas
        if(verb): 
            print 'pmask:   ',pmask
            print 'gmask:   ',gmask
            print 'npfiles: ',npfiles
            print 'ngfiles: ',ngfiles
            
        pstat[dtg]=(npfiles,ngfiles,npmiss,ngmiss)

        if(verb):
            print
            for pfile in pfiles:
                print pfile

        if(verb):
            print
            for gfile in gfiles:
                print gfile

    if(doP):
        print; print 'PPPPPRRRRRWWWWW LLLLLOOOOOPPPPSSSSSS -- PRW/GOES for dtgopt: ',dtgopt 
        pdtgs=pstat.keys()
        pdtgs.sort()
        for pdtg in pdtgs:
            (npfiles,ngfiles,npmiss,ngmiss)=pstat[pdtg]
            if(doCronPrcChk):
                model='gfs2'
                if(verb):
                    print 'CHK-CHK-CHK-PPPRRRWWW'
                    print model,dtg,stat[0]
                (rcc,rcp)=getIfModelRunning(dtg, model, modtimes, curPSs,verb=0)
                (rccg,rcpg)=getIfModelRunning(dtg, 'goes', modtimes, curPSs,verb=0)
                if(rcc):
                    cout="%s --->>> ccccccc in crontab"
                if(rcp):
                    cout="%s <<<--- pppppp processing"
                if(npmiss < 0 and (rcc or rcp)):
                    npmiss=999
                    pstat[pdtg]=(npfiles,ngfiles,npmiss,ngmiss)
                if(ngmiss < 0 and (rccg or rcpg)):
                    ngmiss=999
                    pstat[pdtg]=(npfiles,ngfiles,npmiss,ngmiss)
            print
            print 'prw  loops for dtg: ',pdtg,' N: ',npfiles,' Nmiss: ',npmiss
            print 'goes loops for dtg: ',pdtg, ' N: ',ngfiles,' Nmiss: ',ngmiss
        print

        
    pStatus=1
    pdtgs=pstat.keys()
    pdtgs.sort()
    for pdtg in pdtgs:
        (npfiles,ngfiles,npmiss,ngmiss)=pstat[pdtg]
        if((npmiss != 0 and npmiss != 999) or
           (ngmiss != 0 and ngmiss != 999) ):
            pStatus=0
            break
    
    print
    prwPre='PRW-GOES-LLLOOOPPPSSS'
    
    if(pStatus): 
        print '%s DaIJyoUBu Desu -- %s dtgopt: %s '%(daiJyoPre,prwPre,dtgopt)
    else:
        print '%s MoNDaI DaTa! -- %s dtgopt: %s '%(monDaiPre,prwPre,dtgopt)
    
    print
    MF.dTimer('prw')
    
# -- EEEEEEEEEEEEEEEEEEEEEEEPPPPPPPPPPPPPPPPPPPPPPPPPPPPSSSSSSSSSSSSSSSSSSSSSSSSSSSSS
#
if(doEps):

    MF.sTimer('eps')

    if(doP): print; print 'EEEEEPPPPPSSSSS -- EPS for dtgopt: ',dtgopt 

    if(nhback > 0):
        dtgs=mf.dtg_dtgopt_prc('cur-%d.%s'%(nhback,dtgopt))
    else:
        dtgs=mf.dtg_dtgopt_prc('cur-24.%s'%(dtgopt))


    eStatus={}
    missEps=[]
    
    for dtg in dtgs:

        eStatus[dtg]=1
        nEpsModels=3
        if(w2.is0012Z(dtg)): nEpsModels=4
        stmids=tD.getStmidDtg(dtg)

        year=dtg[0:4]
        emask='%s/%s/%s/*skp*.gif'%(epsdir,year,dtg)
        efiles=glob.glob(emask)
        nefiles=len(efiles)

        modeps={}
        for efile in efiles:
            (ddir,dfile)=os.path.split(efile)
            tt=dfile.split('.')
            model=tt[2]
            stmid="%s.%s"%(tt[-4],tt[-3])
            #print 'eeee',efile,tt,model,stmid
            MF.appendDictList(modeps, model, stmid)
            
        models=modeps.keys()
        models.sort()
        ntcs=len(stmids)
        nmod=len(models)
        nmax=ntcs*nmod
        nact=nefiles
        
        if(nmod != nEpsModels and (nmod != 0) and dtg != dtgs[-1]): 
            eStatus[dtg]=0
            missEps.append(dtg)
            if(verb): print 'TTTCCC-EEEPPPSSS for: ',dtg,'nmod: ',nmod,'nEpsModels: ',nEpsModels,'nact: ',nact

        if(doP):
            print
            print 'EPS loops for dtg: ',dtg,' NTCs: ',ntcs,' NMod: ',nmod,'  Nact: ',nact,' NMAX: ',nmax
        elif(eStatus[dtg] == 0 and doW):
            print
            print '***************MMMMM--EPS loops for dtg: ',dtg,' NTCs: ',ntcs,' NMod: ',nmod,'  Nact: ',nact,' NMAX: ',nmax
                
        if((eStatus[dtg] == 0 and doW) or doP):
    
            for model in models:
                stms=modeps[model]
                nstms=len(stms)
                print '%-4s  stms: '%(model),stms
    
            if(verb):
                print
                for efile in efiles:
                    print efile
                    
            
    print
    eStatusNet=1
    for e in eStatus.keys():
        if(eStatus[e] == 0): eStatusNet=0 ; break
    
    tcePre='TTTCCCEEEPPPSSSSSSSSS'
    if(eStatusNet): 
        print '%s DaIJyoUBu Desu -- %s dtgopt: %s '%(daiJyoPre,tcePre,dtgopt)
    else:
        odtgopt=str(missEps)
        print '%s MoNDaI DaTa! -- %s ------------------ MISSing dtg: %s '%(monDaiPre,tcePre,odtgopt)
        
    print
    MF.dTimer('eps')
    
if(doTcd):


    MF.sTimer('tcd')

    if(doP): print; print 'TTTTTCCCCCDDDDD -- TCdiag for dtgopt: ',dtgopt 

    if(nhback > 0):
        dtgs=mf.dtg_dtgopt_prc('cur-%d.%s'%(nhback,dtgopt))
    else:
        dtgs=mf.dtg_dtgopt_prc('cur-24.%s'%(dtgopt))

    tdStatus=1
    tdMissDtg=[]
    
    for dtg in dtgs:

        if(w2.is0012Z(dtg)): nmodA=nModW200
        if(w2.is0618Z(dtg)): nmodA=nModW206
        
        stmids=tD.getStmidDtg(dtg)
        nstmids=len(stmids)
        
        w2Status={}

        tCTstatus={}
        tCGstatus={}
        tCDstatus={}
        
        if(MF.is0012Z(dtg)): 
            tcdModels=modelsW20012
        else:
            tcdModels=modelsW20618
        
        ntcdModels=0
        for model in tcdModels:
            tCTstatus[model]=0
            tCGstatus[model]=0
            card=w2.getL2ModelStatus(model,'-W',dtg,override=override,verb=verb)
            ntaus=int(card.split()[4])
            if(ntaus > 0): 
                ntcdModels=ntcdModels+1
                w2Status[model]=1
            else:
                w2Status[model]=0
                

        tcA=TcAidTrkAd2Bd2(dtgopt=dtg,verb=verb,quiet=1)
        rcA=tcA.getStatus(modelChk=None, doPrint=0,returnAd2=1)
        
        # -- dict with tdiagfiles
        #
        modtcd={}

        if(rcA != None and rcA[0] != -1):
            rcT=rcA[0]
            rcG=rcA[1]
        else:
            print 'WWW-doTcd: rcA == None for: ',dtg
            continue
        for r in rcT:
            tt=r.split()
            stms=tt[2]
            #rmodel=tt.split()[0]
            rmodel=tt[0]
            rcAm=tcA.getStatus(modelChk=rmodel, doPrint=0,returnAd2=3)
            (modtctGen,modtctTrk,modtctTrkStdout,modtctAllTrk)=rcAm
            stmSiz=modtctTrk[rmodel]
            rcS=getStmSiz(stmSiz)
            tCTstatus[rmodel]=rcS[0]

            # -- set the stmids in modtcd to stmid.siz list
            #
            if(rcS[0] == -2):
                modtcd[rmodel]=rcS[1]
            
        for r in rcG:
            tt=r[0]
            stms=r[1]
            rmodel=tt.split()[0]
            rnstms=len(stms)
            tCGstatus[rmodel]=1
            

        year=dtg[0:4]
        dmask='%s/%s/%s/DIAGFILES/tcdiag.*.txt'%(tcddir,year,dtg)
        tcdfiles=glob.glob(dmask)
        
        ntcdfiles=len(tcdfiles)
        for tcdfile in tcdfiles:
            (ddir,dfile)=os.path.split(tcdfile)
            tt=dfile.split('.')
            model=tt[1]
            tracker=tt[-2].split('-')[-1][0:2]
            stmid="%s.%s-%s"%(tt[-4],tt[-3],tracker)
            MF.appendDictList(modtcd, model, stmid)

        if(printTCstatus):
            print '-----------dtg: ',dtg,' nstmids: ',nstmids
        
        # -- all models where W2 is done...
        #
        nmodAW2=0
        for model in tcdModels:
            try:
                stms=modtcd[model]
                nstms=len(stms)
                nmodAW2=nmodAW2+1
            except:
                nstms=0
            
            try:
                tcTs=tCTstatus[model]
            except:
                tcTs=0

            if(nstms > 0):
                tCDstatus[model]=1
            else:
                tCDstatus[model]=0
            
            if(printTCstatus):
                print 'model: ',model,'W2: ',w2Status[model],' TCT: ',tCTstatus[model],\
                      ' TCG: ',tCGstatus[model],' TCD: ',tCDstatus[model]
            
            
        models=modtcd.keys()
        models.sort()
        ntcs=len(stmids)
        nmod=len(models)
        nmod=ntcdModels
        
        nexp=ntcs*nmod
        nact=ntcdfiles
        Status='copacetic...'
        
        if(nact < nexp and nmod != nmodAW2): 
            Status=' <<<< missing'
            tdStatus=0
            tdMissDtg.append(dtg)
            
        if(nact > nexp): Status=' >>>>>>>>  too many!'

        if(doP or tdStatus == 0):
            print
            print 'TCdiag files for dtg: ',dtg,' NTCs: ',ntcs,' NMod: ',nmod,'  Nact: ',nact,' Nexp: ',nexp,' Status: ',Status
    
    
            for model in tcdModels:
                try:
                    stms=modtcd[model]
                    nstms=len(stms)
                except:
                    nstms=0
                    
                if(nstms > 0):
                    print '%-4s  stms: '%(model),stms
                else:
                    if(diag):
                        print '%-4s  ---mmmmmm missing mmmmmm---'%(model)
    
            if(verb):
                print
                for tcdfile in tcdfiles:
                    print tcdfile

    print
    if(tdStatus): 
        print '%s DaIJyoUBu Desu -- TTTCCCDDDIIIAAAGGGGGG for dtgopt: %s '%(daiJyoPre,dtgopt)
    else:
        print '%s MoNDaI DaTa! -- TTTCCCDDDIIIAAAGGGGGG for dtgs: %s '%(monDaiPre,str(tdMissDtg))
      
    print  
    MF.dTimer('tcd')

if(doTct):

    MF.sTimer('tct')

    MF.sTimer('trackers')
    if(doP): print; print 'TTTTTCCCCCTTTTT--TTTRRRKKK--GGGEEENNN -- TCtrk for dtgopt: ',dtgopt 

    if(nhback > 0):
        ndtgopt="cur-%d.%s"%(nhback,idtgopt)
    else:
        ndtgopt="cur-24.%s"%(idtgopt)

    if(doByDtgs): ndtgopt=idtgopt
    
    #MF.sTimer('trackers-AD2')
    if(doMftrkN):
        tcA=TcAidTrkAd2Bd2(dtgopt=ndtgopt,verb=verb,source='mftrkN')
    else:
        tcA=TcAidTrkAd2Bd2(dtgopt=ndtgopt,verb=verb)
    #MF.dTimer('trackers-AD2')
    
    tcTstatus=tcA.getStatus(doPrint=doP)
    print
    if(tcTstatus): 
        print '%s DaIJyoUBu Desu -- TTTCCCTTTRRRAAACCCKKK for dtgopt: %s '%(daiJyoPre,dtgopt)
    else:
        print '%s MoNDaI DaTa! -- TTTCCCRRRAAACCCKKK for dtgopt: %s '%(monDaiPre,dtgopt)
        rcA=tcA.getStatus(doPrint=1)
    print
    MF.dTimer('tct')
    
if(doTcp):
    
    overOpt=''
    if(override): overOpt='-O'

    redoTcPrc=[]
    MF.sTimer('tcp')
    
    tcPstatus=1
    if(doP): print; print 'TTTTTCCCCCPPPPP--TTTCCCPPP--all-tc-prc -- TCtrk for dtgopt: ',tdtgopt; print 
    # -- run to get status of processing
    pycmd='w2-tc-redo-ALL.py'
    cmd='%s %s -N'%(pycmd,tdtgopt)
    rc=mf.runcmd2(cmd,ropt,lsopt='q',verb=verb)
    if(rc[0] == 1):
        for card in rc[1]:
            if(mf.find(card,'CCC')): 
                redoTcPrc.append(card)
                tcPstatus=0
            if(doP): print card
    else:
        print 'WWW-doTcp---'
    
    print

    overOpt=''
    if(override): overOpt='-O'

    if(tcPstatus): 
        print '%s DaIJyoUBu Desu -- TTTCCCRRREEEDDDOOOPPP for dtgopt: %s '%(daiJyoPre,dtgopt)
    else:
        print '%s MoNDaI DaTa! -- TTTCCCRRRREEEDDDOOOPPP for dtgopt: %s '%(monDaiPre,dtgopt)
        for cmd in redoTcPrc:
            ocmd="%s"%(cmd)
            print ocmd


        if(runTcRedo):
            print 'RRRRRRRRRRRRRRRRRRRRRRRRRRRRRredo:'
            cmd='%s %s -X %s'%(pycmd,tdtgopt,overOpt)
            mf.runcmd(cmd,'')
        else:
            print 'do...'
            print '%s %s -X %s'%(pycmd,tdtgopt,overOpt)
        

    print
            
    MF.dTimer('tcp')

MF.dTimer('all')

