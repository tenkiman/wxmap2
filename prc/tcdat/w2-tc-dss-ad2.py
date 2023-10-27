#!/usr/bin/env python

from tcbase import *

#llllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll
# local unbounded methods

def doRsyncDSS2Kaze(spath,reverse=0,
                    doupdate=1,dosizeonly=0,dodelete=0,
                    ropt=''):

    (sdir,sfile)=os.path.split(spath)
    
    if(w2.onKaze):
        tdir='fiorino@%s:%s/DSs'%(w2.KishouScpServer,w2.KishouTcDatDir)
    elif(w2.onKishou):        
        tdir="%s/w21/dat/tc/DSs"%(DATKazeBaseDir)
    
    tdir=tdir.replace('//','/')
    sdir=sdir.replace('//','/')

    tpath="%s/%s"%(tdir,sfile)

    pdir=w2.W2BaseDirEtc
    
    if(reverse):
        tt=spath
        spath=tpath
        tpath=tt
    
    rupopt=''
    if(doupdate): rupopt='-u'

    sizonly=''
    if(dosizeonly):  sizonly='--size-only'

    delopt=''
    if(dodelete): delopt='--delete'

    rsyncopt="%s %s %s --timeout=30 --protocol=29 -alv --exclude-from=%s/ex-w21.txt"%(delopt,rupopt,sizonly,pdir)

    MF.sTimer('adk-doRsyncDSS2Kaze')
    cmd="rsync %s %s %s"%(rsyncopt,spath,tpath)
    MF.runcmd(cmd,ropt)
    MF.dTimer('adk-doRsyncDSS2Kaze')
    

def grepAidsFromAdeck(adeck,taids=['avno','hwrf','cotc','gfdn','gfdl','clp5','c120'],
                      prependAid=None,dtgs=None,taidsOnly=0):
    
    allwaysKeep=['carq','wrng','jtwc','ofcl']
    if(taidsOnly): allwaysKeep=[]
    
    acards=adeck.split('\n')
    
    itaids=taids
    if(prependAid != None):
        itaids=[]
        for taid in taids:
            itaid=taid[1:]
            itaids.append(itaid)
            
    chkAids=allwaysKeep+itaids
    
    odeck=''
    for acard in acards:
        att=acard.split(',')
        if(len(att) > 1):
            aid=att[4].strip()
            aid=aid.lower()
            dtg=att[2].strip()
            dtgChk=1
            if(dtgs != None): dtgChk=(dtg in dtgs)

            if(aid in chkAids and dtgChk):
                odeck=odeck+str(acard+'\n')
                
    return(odeck)
                
def removeJtwcOfclFromAdeck(adeck,
                            #taids=['jtwc','ofcl'],
                            taids=['ofcl'],   # for ncep.emc test
                            ):
    
    acards=adeck.split('\n')
    odeck=''
    for acard in acards:
        att=acard.split(',')
        if(len(att) > 1):
            aid=att[4].strip()
            aid=aid.lower()
            if(aid in taids):
                None
            else:
                odeck=odeck+str(acard+'\n')
    return(odeck)
                
def getAcards(source,tstmid,ad2Is,tstmids9Xall=[],
              chkNhcJtwcAdeck=0,
              uniqOverride=0,
              override=0):

    # -- 20170807 - doesn't work added uniqAcards and doUniqAd2 to adVM
    #
    #def uniqAcards(acards):
        #dacards={}
        #oacards=''
        #lacards=acards.split('\n')
        #for lacard in lacards:
            #if(len(lacard) > 0):
                #tt=lacard.split(',')
                #dtg=tt[2].strip()
                #MF.appendDictList(dacards, dtg, lacard)
            
        #dtgs=dacards.keys()
        #dtgs.sort()
        
        #MF.uniqDictList(dacards)
        
        #for dtg in dtgs:
            #for dacard in dacards[dtg]:
                #oacards=oacards+dacard+'\n'


        #return(oacards)
                
        
    def getcards(adcurpath,source,tstmid,ad2Is):
        (snum,b1id,stmyear,b2id,stm2id,stm1id)=getStmParams(tstmid)
        ad2I=ad2Is[stmyear]
        
        try:
            (asizC,agtimeiC)=ad2I.data[source,tstmid]
            gotInv=1
        except:
            agtimeiC=None
            gotInv=0

        if(agtimeiC == None): gotInv=0
        asiz=MF.getPathSiz(adcurpath)
        (agtimei,agdtimei)=MF.PathModifyTimei(adcurpath)
        ad2I.data[source,tstmid]=(asiz,agtimei)
        # -- check if adcurpath there...if not return ''
        if(asiz < 0):
            acards=''
            return(acards)
        
        doAdeck=1
        if(gotInv):
            dt=MF.DeltaTimei(agtimei,agtimeiC)
            dsiz=asiz-asizC
            if(dsiz != 0 or dt != 0.0): doAdeck=1
            else: doAdeck=0
            
        acards=''
        if(doAdeck or override):
            MF.sTimer('read-acards-%s'%(source))    
            acards=MF.ReadFile2String(adcurpath)
            MF.dTimer('read-acards-%s'%(source))
            
        return(acards)
        
    def getcards9x(aduniqzippath,source,tstmid,ad2Is):
        """ based on tcVM.get9xAuniq + inventory
"""
        (snum,b1id,stmyear,b2id,stm2id,stm1id)=getStmParams(tstmid)
        ad2I=ad2Is[stmyear]
        
        try:
            (asizC,agtimeiC)=ad2I.data[source,tstmid]
            gotInv=1
        except:
            agtimeiC=None
            gotInv=0

        if(agtimeiC == None): gotInv=0
        asiz=MF.getPathSiz(adcurpath)
        (agtimei,agdtimei)=MF.PathModifyTimei(adcurpath)
        ad2I.data[source,tstmid]=(asiz,agtimei)

        # -- check if adcurpath there...if not return ''
        if(asiz < 0):
            acards=''
            return(acards)
        
        doAdeck=1
        if(gotInv):
            dt=MF.DeltaTimei(agtimei,agtimeiC)
            dsiz=asiz-asizC
            if(dsiz != 0 or dt != 0.0): doAdeck=1
            else: doAdeck=0
            
        acards=''
        if(doAdeck or override):
            MF.sTimer('read-acards-999-%s'%(source))    

            icharId=tstmid[0].lower()
    
            try:
                AZ=zipfile.ZipFile(aduniqzippath)
                afiles=AZ.namelist()
            except:
                afiles=[]
        
            lenAfiles=len(afiles)
            len9Xfiles=len(tstmids9Xall)
            
            avalIcharID=ord(icharId)
            gotAfile=0
            for n in range(0,lenAfiles):
                afile=afiles[n]
                ocharId=chr(icharA+n)
                avalOcharId=icharA+n
                if(icharId == ocharId):
                    ocards=AZ.read(afile)
                    acards=acards+ocards
                    gotAfile=1
                    break
            
            # -- case where 9X bdeck  and NO 9x adeck
            # -- go for latest
            #
            if( lenAfiles < len9Xfiles and not(gotAfile) ):
                
                if(len(afiles) > 0):
                    nLatestAfile=afiles.index(afiles[-1])
                else:
                    nLatestAfile=0
                    
                print 'WWWWWWWW(%s.getAcards) -- 9X missing for stmopt: %s ... use latest n: %d'%(pyfile,stmopt,nLatestAfile)
                if(nLatestAfile != 0):
                    afile=afiles[-1]
                    ocards=AZ.read(afile)
                    acards=acards+ocards
                else:
                    ocards=''
                
            MF.dTimer('read-acards-999-%s'%(source))
    
        return(acards)
    

    (snum,b1id,stmyear,b2id,stm2id,stm1id)=getStmParams(tstmid)
    
    byear=stmyear
    
    sdir="%s/%s/%s"%(TcAdecksAtcfFormDir,byear,source)
    sfile="a%s%s%s.dat"%(b2id.lower(),snum,stmyear)

    prependAid=None
    doUniqAdeck=0

    if(source == 'jt-nhc'):

        tstmidAB=tstmid
        
        if(Is9X(tstmid)):
            rc=getStmParams(tstmid,convert9x=1)
            tstmidAB=rc[-1]
            
        rc=getABsDirsPaths(tstmidAB,chkNhcJtwcAdeck=chkNhcJtwcAdeck)

        (snum,b2id,byear,abdir,bbdir,
         adarchdir,adarchzippath,aduniqzippath,
         bdarchdir,bdarchzippath,bduniqzippath,
         adcurpath,bdcurpath)=rc       
         
        if(Is9X(tstmid)):
            acards=getcards9x(aduniqzippath,source,tstmid,ad2Is)
        else:
            acards=getcards(adcurpath,source,tstmid,ad2Is)

    elif(source == 'hrd'):
        
        sdir="%s/%s"%(TcAdecksHrdDir,byear)
        adcurpath="%s/%s"%(sdir,sfile)
        acards=getcards(adcurpath,source,tstmid,ad2Is)
        prependAid='h'

    elif(source == 'tmtrkN' or source == 'erai' or source == 'era5'):
        
        adcurpath="%s/%s"%(sdir,sfile)
        acards=getcards(adcurpath,source,tstmid,ad2Is)
        prependAid='t'

    elif(source == 'psdRR2'):
        
        adcurpath="%s/%s"%(sdir,sfile)
        acards=getcards(adcurpath,source,tstmid,ad2Is)

    elif(source == 'mftrkN'):
        
        adcurpath="%s/%s"%(sdir,sfile)
        acards=getcards(adcurpath,source,tstmid,ad2Is)
        prependAid='m'

    elif(source == 'fim7ss'):
        
        adcurpath="%s/%s"%(sdir,sfile)
        acards=getcards(adcurpath,source,tstmid,ad2Is)

    elif(source == 'ecmwf'):
        
        adcurpath="%s/%s"%(sdir,sfile)
        acards=getcards(adcurpath,source,tstmid,ad2Is)

    elif(source == 'ecbufr'):
        
        adcurpath="%s/%s"%(sdir,sfile)
        acards=getcards(adcurpath,source,tstmid,ad2Is)

    elif(source == 'ec-wmo'):
        
        adcurpath="%s/%s"%(sdir,sfile)
        acards=getcards(adcurpath,source,tstmid,ad2Is)

    elif(source == 'clip'):
            
        adcurpath="%s/%s"%(sdir,sfile)
        acards=getcards(adcurpath,source,tstmid,ad2Is)

    elif(source == 'ukmo'):
        
        adcurpath="%s/%s"%(sdir,sfile)
        acards=getcards(adcurpath,source,tstmid,ad2Is)
        prependAid='u'

    elif(source == 'ncep'):
        
        adcurpath="%s/%s"%(sdir,sfile)
        acards=getcards(adcurpath,source,tstmid,ad2Is)
        prependAid='n'

    elif(source == 'cmc'):
        
        adcurpath="%s/%s"%(sdir,sfile)
        acards=getcards(adcurpath,source,tstmid,ad2Is)
        prependAid='c'

    elif(source == 'gefs'):
        
        adcurpath="%s/%s"%(sdir,sfile)
        acards=getcards(adcurpath,source,tstmid,ad2Is)
        prependAid='g'

    elif(source == 'rtfim' or source == 'rtfim9'):
        
        adcurpath="%s/%s"%(sdir,sfile)
        acards=getcards(adcurpath,source,tstmid,ad2I)
        prependAid='j'
        
    else:
        print 'EEE ad2.getAcards -- invalid source: ',source
        sys.exit()
        
    # -- uniq the acards for the new way of handling R34/R50/R60
    # -- implmemented new version to atcf-form adecks in w2.tc.convert-tm-mftr*.py
    #
    #if(doUniqAdeck and not(uniqOverride)):
        #MF.sTimer('uniqAcards-%s'%(source))
        #uacards=uniqAcards(acards)
        #MF.dTimer('uniqAcards-%s'%(source))
    #else:
    
    uacards=acards
        
    return(uacards,byear,prependAid)
    


def doListing(dsbdir,dbtype,tstmids,taids,
              dolsong=0,dolsfull=0,
              dofilt9x=0,
              verb=0,
              dtgopt=None):
    
    MF.sTimer('dolisting-AD2-%s'%(dbtype))
    (DSss,bd2s,dbnames,basins,byears)=getAdeck2Bdeck2DSs(tstmids,dbtype,dsbdir=dsbdir,verb=verb)
    lsopt='s'
    if(dolslong): lsopt='l'
    if(dolsfull): lsopt='f'

    otaids={}
    ostmids=[]
    for byear in byears:
        for basin in basins:
            DSs=DSss[basin,byear]
            (ftaids,fstmids)=LsAidsStormsDss(DSs,tstmids,taids,dofilt9x=dofilt9x,lsopt=lsopt,dtgopt=dtgopt)
            otaids.update(ftaids)
            ostmids=ostmids+fstmids
            
    ostmids=mf.uniq(ostmids)
        
    if(tstmids == None):  tstmids=ostmids
    
    if(otaids != None): 
        taids=otaids
    elif(otaids == None or len(otaids) == 0):
        print 'WWW[ad2.doListing] -- no aids for dtgopt: ',dtgopt,' tstmids: ',tstmids
        dolsfull=0
    
    if(dolsfull):
        lsBT=1
        BTs={}
        
        for tstmid in tstmids:
            tyear=tstmid.split('.')[-1]
            basin=getBasinFromStmid(tstmid)
            DSs=DSss[basin,tyear]

            if(len(taids) == 0):
                print 'taids = 0 for tstmids: ',tstmids,' press...'
                continue
            aids=taids[tstmid]
            for aid in aids:
                
                (AT,BT,aD)=getAidAdeck2Bdeck2FromDss(DSs,bd2s,aid,tstmid,verb=verb,warn=1)
                BTs[tstmid]=BT
                AT.lsAT(tstmid,dtgopt=dtgopt)
                
        if(lsBT):
            btstmids=BTs.keys()
            btstmids.sort()

            for btstmid in btstmids:
                BT=BTs[btstmid]
                if(BT != None):
                    print
                    print 'BT for: ',btstmid
                    BT.lsBT(dtgopt=dtgopt)
                    
    MF.dTimer('dolisting-AD2-%s'%(dbtype))


def makeAdeck2s(tstmids,taids,source,tD,ad2Is,tstmids9Xall=[],
                dtgopt=None,
                corrTauDisCont=1,warn=1,
                corrTauInc=12,
                overrideInvChk=0,overrideBD2=0,verb=0):
    
    bd2s={}
    ad2s={}
    
    tdtgs=None
    if(dtgopt != None):  tdtgs=mf.dtg_dtgopt_prc(dtgopt)
        
    byears=getYearsFromStmids(tstmids)
    
    MF.sTimer('makeAD2s-bd2')
    (bd2s,rcbd2s)=getBdecks2DataSets(byears,verb=verb)
    if(overrideBD2 or (rcbd2s == 0)): bd2s={}
    MF.dTimer('makeAD2s-bd2')
    
    byears=[]
    
    for tstmid in tstmids:
        
        # -- get ATCF adeck cards
        #
        (acards,byear,prependAid)=getAcards(source,tstmid,ad2Is,tstmids9Xall,
                                            chkNhcJtwcAdeck=chkNhcJtwcAdeck,
                                            uniqOverride=uniqOverride,
                                            override=overrideInvChk)
        if(taids != None and len(acards) > 0):
            MF.sTimer('grep-%s-acards'%(aidopt))
            acards=grepAidsFromAdeck(acards,taids,dtgs=tdtgs,prependAid=prependAid,taidsOnly=1)
            MF.dTimer('grep-%s-acards'%(aidopt))
            
        byears.append(byear)
         
        # -- get the mdeck2 for this storm; dobt=1 based soley on bdeck
        #
        dobtMD2=1
        if(Is9X(tstmid)): dobtMD2=0
        mD2=tD.getDSsStm(tstmid,dobt=dobtMD2,verb=verb) 
        mD2C=tD.getDSsStm(tstmid,dobt=0,verb=verb)
        if(mD2 == None):
            print 'WWW(ad2.makeAdeck2s() no mdeck2 for tstmid: ',tstmid,' dobtMD: ',dobtMD2,' press...'
            continue

        # -- make Bdeck2
        #
        MF.sTimer('bds-%s'%(tstmid))
        bd2s[tstmid]=Bdeck2(mD2,verb=0)
        MF.dTimer('bds-%s'%(tstmid))
    
        # -- make Adeck2
        #
        MF.sTimer('ads-%s'%(tstmid))
        
        MF.sTimer('ads-aD2-%s'%(tstmid))
        aD2=Adeck2s(tstmid,acards=acards,mD2=mD2C,prependAid=prependAid,
                    corrTauDisCont=corrTauDisCont,corrTauInc=corrTauInc,
                    warn=warn)
        MF.dTimer('ads-aD2-%s'%(tstmid))
        
        MF.sTimer('ads-getADs%s'%(tstmid))
        newad2s=aD2.getAD2s(tstmid)
        ad2s.update(newad2s)
        
        MF.dTimer('ads-getADs%s'%(tstmid))
        
        MF.dTimer('ads-%s'%(tstmid))
        
    byears=mf.uniq(byears)
    #if(len(byears) > 1):
    #    print 'EEE (ad2.makeAdeck2s() -- more than one year in tstmids'
    #else:
    #    byear=byears[0]    
    return(ad2s,bd2s,byears)


def makeAdeck2Interp(tstmids,taids,phr,tD,
                     verb=0,warn=1):

    def removePrevInterpAids(taid):
        
        rc=1
        if(len(taid) >= 6 and 
           (taid[-2:] == '00' or taid[-2:] == '06' or taid[-2:] == '12' or taid[-2:] == '18')
           ): rc=0
        
        return(rc)
        
        

    from ATCF import AidProp
    
    (DSss,bd2s,dbnames,basins,byears)=getAdeck2Bdeck2DSs(tstmids)
    
    dtx=3
    
    ad2s={}
    bd2sO={}
    
    byears=[]
    
    for tstmid in tstmids:
        
        byear=tstmid.split('.')[-1]
        byears.append(byear)
        
        basins=getBasinsFromStmids(tstmid)
        basin=basins[0]
        
        acards={}
        stm3id=tstmid.split('.')[0]
        DSs=DSss[basin,byear]
        
        # -- always get ops Mdeck2 for interp
        #
        dobtMD2Interp=0  # if 0 use ops = CARQ | WBT depending on BT in mdeck2
        mD2=tD.getDSsStm(tstmid,dobt=dobtMD2Interp)
    
        # -- make Bdeck2
        #
        MF.sTimer('bds-%s'%(tstmid))
        bd2sO[tstmid]=Bdeck2(mD2,verb=0)
        MF.dTimer('bds-%s'%(tstmid))
        
        for taid in taids:  
            
            if(not(removePrevInterpAids(taid))): 
                if(warn): 
                    print 'WWW(ad2.makeAdeck2Inter()) tossing taid: ',taid,' -- previously done'
                continue
            
            MF.sTimer('ads-makeADs-phr-%02d-%s-%s'%(phr,tstmid,taid))

            acards=''

            aP=AidProp(taid)
            
            otaid="%s%02d"%(taid,phr)
            otaids=[otaid]
            
            (AT,BT,aD)=getAidAdeck2Bdeck2FromDss(DSs,bd2sO,taid,tstmid,verb=verb,warn=0)
            
            if( not(hasattr(AT,'dtgs')) or len(AT.dtgs) == 0 ): 
                print 'WWW phr != None, do AT from GetAidAdeck2Bdeck2FromDss for tstmid: ',tstmid,' taid: ',taid
                continue
            dtgs=AT.dtgs
            
            for dtg in dtgs:
                btdtg=mf.dtginc(dtg,phr)
                (btlat,btlon,btdir,btspd,btvmax)=BT.selectBestBtCqTau0(btdtg,verb=verb)
                if(btlat == None): 
                    print 'WWW no bt for dtg: ',dtg
                    continue
                itrk=AT.atrks[dtg]
                
                (jtrk,jtaus)=aD.FcTrackInterpFill(itrk,npass=10,dovmaxSmth=0)

                otrk=aD.BiasCorrFcTrackInterpFill(jtrk,itrk,jtaus,phr,dtx,
                                                  btlat,btlon,btdir,btspd,btvmax,
                                                  taid,dtg,stm3id,
                                                  vmaxCorrScheme=aP.vmaxCorrScheme,
                                                  dopc=1,vmaxmin=20.0,verb=verb)
                
                
                acards=acards+MakeAdeckCards(otaid,btdtg,otrk,tstmid,doString=1,verb=verb)
                MF.sTimer('ads-aD2-%s'%(tstmid))

            # -- use BT for making Adeck2
            #
            
            dobtMD2AD2=1
            mD2=tD.getDSsStm(tstmid,dobt=dobtMD2AD2)
            aD2=Adeck2s(tstmid,acards=acards,mD2=mD2)                

            newad2s=aD2.getAD2s(tstmid)
            
            ad2s.update(newad2s)
            try:
                ad2=ad2s["%s_%s"%(otaid,tstmid)]
            except:
                ad2=None
                
            if(ad2 == None):
                print
                print 'FFF---'
                print 'FFAAIILLEEDD-make-ads-makeADs-phr-%02d-%s-%s'%(phr,tstmid,taid)
                print 'FFF---'
                print
            
            MF.dTimer('ads-makeADs-phr-%02d-%s-%s'%(phr,tstmid,taid))
        
    byears=mf.uniq(byears)
    if(len(byears) > 1):
        print 'EEE (ad2.makeAdeck2Interp() -- more than one year in tstmids'
    else:
        byear=byears[0]
        
    return(ad2s,bd2s,byears)
        
def relabelAdeck2Aids(tstmids,taids,
                      dsbdir=None,
                      override=0,
                      verb=0):       

    from ATCF import AidProp
    
    (DSss,bd2s,dbnames,basins,byears)=getAdeck2Bdeck2DSs(tstmids,dsbdir=dsbdir)
    
    ad2s={}
    byears=[]
    
    for tstmid in tstmids:
        
        byear=tstmid.split('.')[-1]
        byears.append(byear)
        
        basins=getBasinsFromStmids(tstmid)
        basin=basins[0]
        
        DSs=DSss[basin,byear]
        
        for taid in taids:  
            
            tt=taid.split(':')
            if(len(tt) != 2):
                print 'WWW(relabelAdeck2Aids) - invalid alias form taid: ',taid,' press...'
                continue
            
            curAid=tt[0]
            newAid=tt[1]
            curKey="%s_%s"%(curAid,tstmid)
            newKey="%s_%s"%(newAid,tstmid)
            
            try:
                curad2=DSs.db[curKey]
            except:
                curad2=None

            try:
                newad2=DSs.db[newKey]
            except:
                newad2=None

            if(curad2 != None and (newad2 == None or override)):  # -- bug -- 20160727 -- curad2 HAS to != None
                print 'WWW(relabelAdeck2Aids) -found ad2 form curKey: ',curKey,' setting to newKey: ',newKey,' for tstmids: ',tstmid
                ad2s[newKey]=curad2
        
    if(len(ad2s) == 0):
        print 'WWW(relabelAdeck2Aids) -- no ad2s for tstmids: ',tstmids[0],'...',tstmids[-1],' taids: ',taids
        
    byears=mf.uniq(byears)
    if(len(byears) > 1):
        print 'EEE (ad2.makeAdeck2Interp() -- more than one year in tstmids'
    else:
        byear=byears[0]
        
    return(ad2s,byears)
     
#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# -- command line setup
#

class Adeck2CmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv
        
        self.argv=argv
        self.argopts={
            1:['source',  '''source1[,source2,...,sourceN]'''],
            }

        self.defaults={
            }
            
        self.options={
            'dssDir':              ['D:',None,'a','set base dir for DSs'],
            'overrideOpt':         ['O:',0,'i',"""

overrideOpt:
-O1 :: overrideInvChk=1
-O2 :: overrideBD2=1 
-O3 :: overrideBD2=1 ; overrideAD2=1   
-O4 :: overrideInv=1   
-O5 :: overrideInv=1 ; overrideInvChk=1; overrideBD2=1; overrideAD2=1
-O6 :: overrideReLabelAD2=1
"""
                                    ],
            'verb':                ['V',0,1,'verb is verbose'],
            'quiet':               ['q',0,1,'1 - turn off all diag messages'],
            'ropt':                ['N','','norun',' norun is norun'],
            'killAd2':             ['K',0,1,'kill the .pypdb norun is norun'],
            'dobt':                ['b',1,0,'dobt=1 UNLESS set...do ALL TCs and pTCs'],
            'relabelAD2':          ['E',0,1,'relabel aids; set using -T CCCC:NNNN where CCCC is current name and NNNN is new name'],
            'do9Xonly':            ['9',0,1,'just do 9X'],
            'doAdeck2':            ['A',1,0,'do NOT do Adeck2 processing'],
            'stmopt':              ['S:',None,'a','stmopt'],
            'dtgopt':              ['d:',None,'a','dtgopt to get tstmids'],
            'aidopt':              ['T:',None,'a','taid'],
            'doput':               ['P',1,0,'do NOT put a|vdeck2'],
            'phr':                 ['h:',None,'i',"""phr -- do 'I' (6) and '2'(12) trackers"""],
            'dols':                ['l',0,1,'1 - list'],
            'dolslong':            ['L',0,1,'1 - long list'],
            'dolsfull':            ['F',0,1,'1 - full list'],
            'dochkIfRunning':      ['o',0,1,'do chkifrunning in M.DataSets MF.chkIfFileIsOpen'],
            'doRsync2Kishou':      ['R',1,0,'do NOT rysnc dss to kishou'],
            'doRsync2Kaze':        ['r',0,1,'DO rsysc dss to kaze if on kishou'],
            'strictChkIfRunning':  ['s',1,0,'do NOT do strict check if running -- any instance'],
            'corrTauDisCont':      ['C',0,1,'correct tau discontinuity by interp -- mainly for ecmwf trackers'],
            'chkNhcJtwcAdeck':     ['J',0,1,'check both JTWC and NHC for adecks'],
            'uniqOverride':        ['u',0,1,'override uniq in getAcards'],
            'dolocalDSs':          ['x',1,0,'do NOT use local DSs dir'],
            }

        self.defaults={
            'diag':              0,
            }

        self.purpose='''
purpose -- create adecks for TCVCIP
sources: %s'''%(w2.TCsourcesActive)
        self.examples='''
%s -S w.15 -T c120:clip5 -E  # relabel and add c120 -> clip5
%s -S 29w.15 -L -T ecm       # long list of all aids with 'ecm'
'''


def errAD(option,opt=None):

    if(option == 'tstmids'):
        print 'EEE # of tstmids = 0 :: no stms to verify...stmopt: ',stmopt,' for errAD option: ',option
    elif(option == 'stmopt'):
        print 'EEE must set -S stmopt OR -d dtgopt'
    elif(option == 'source'):
        print 'EEE must set source for no plain args and NOT doing -l -L'
    else:
        print 'Stopping in errAD: ',option
    sys.exit()
        

def warnAD(option,opt=None):

    if(option == 'taids'):
        print 'WWW # of taids = 0 :: no stms to verify...stmopt: ',stmopt
    else:
        print 'continuing in warnAD: ',option



#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
# main
#

CL=Adeck2CmdLine(argv=sys.argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr
    
# -- OOOOOO override opts
#
overrideInv=0
overrideInvChk=0
overrideBD2=0
overrideAD2=0
overrideReLabelAD2=0
if(overrideOpt == 1): overrideInvChk=1
if(overrideOpt == 2): overrideBD2=1
if(overrideOpt == 3): overrideInvChk=1; overrideAD2=1
if(overrideOpt == 4): overrideInv=1
if(overrideOpt == 5): overrideInv=1 ; overrideInvChk=1; overrideBD2=1; overrideAD2=1
if(overrideOpt == 6): overrideReLabelAD2=1


# -- CCCCCC chk if running of kaze if doing rsync 2 kaze
#
if(w2.onKishou and doRsync2Kaze):
    rcKaze=chkifRunningOnKaze(pyfile,verb=verb)
    if(rcKaze and w2.onKishou): print 'WWW(%s) already running on wxmap2 or tcops...sayounara...'%(pyfile) ;  sys.exit()
    
    
MF.sTimer('all-AD2')

# -- LLLLLL set up listing
#
if( (mf.find(source,'-') and source != 'ec-wmo') and not(mf.find(source,'jt') or mf.find(source,'nhc')) ):
    if( ('-l' in sys.argv) or ('-L' in sys.argv) or ('-h' in sys.argv) or ('-E' in sys.argv)  or ('-F' in sys.argv)  ):
        cmd="%s jt-nhc -o"%(CL.pypath)
        for arg in sys.argv[1:]:
            cmd="%s %s"%(cmd,arg)
        mf.runcmd(cmd,ropt)
        sys.exit()
        
    else:
        errAD('source')
            

# -- DSs dir
#
if(dssDir != None):
    dsbdir=dssDir
    
else:
    # -- local for DSs or DSs-local in .
    #
    dsbdir="%s/DSs"%(TcDataBdir)
    localDSs=os.path.abspath('./DSs')
    localDSsLocal=os.path.abspath('./DSs-local')
    
    if(os.path.exists(localDSs) and dolocalDSs):
        print 'llllllllllll',localDSs
        dsbdir=localDSs
        
    elif(os.path.exists(localDSsLocal) and dolocalDSs):
        print 'llllllllllll--------lllllllllll',localDSsLocal
        dsbdir=localDSsLocal

    else:
        dsbdir="%s/DSs"%(TcDataBdir)
        
# -- sources
#
if(source == 'all'):
    isources=w2.TCsourcesActive
else:
    isources=source.split(',')

sources=[]
for isource in isources:
    source=isource
    if( (mf.find(source,'jt') or mf.find(source,'nh') ) ): source='jt-nhc'
    sources.append(source)	

# -- stmids
#
if(stmopt == None and dtgopt == None): errAD('stmopt')

#if(stmopt != None and (mf.find(stmopt,'all') and not(do9Xonly))): -- allow for 9x if all
if(stmopt != None and (mf.find(stmopt,'all'))):
    stmopt=getAllStmopt(stmopt)

# -- loop
#

if(len(sources) > 1):
    for source in sources:
        cmd="%s %s -o"%(CL.pypath,source)
        for o,a in CL.opts:
            cmd="%s %s %s"%(cmd,o,a)
        mf.runcmd(cmd,ropt)
        
    sys.exit()

# -- taids
#
taids=None

if(aidopt != None):
    
    taids=aidopt.split(',')

    # -- detect relabeling
    #
    relabelAD2=0
    otaids=[]
    for taid in taids:
        tt=taid.split(':')
        if(len(tt) == 2): 
            relabelAD2=1
            otaids.append(taid)
    if(relabelAD2 and otaids != taids):
        print 'WWW(relabelAD2) some taid in taids not in CCCC:NNNN form taids: ',taids,' using taids: ',otaids
        
# -- test if stmopt 9X
#

if(stmopt != None and (do9Xonly == 0 and Is9Xstmopt(stmopt))): do9Xonly=1

# -- get tstmids
#
if(do9Xonly): dobt=0
(tstmids,tD,tstmids9Xall)=getTstmidsAD2FromStmoptDtgopt(stmopt,dtgopt,do9Xonly,dobt,source)

if(ropt == 'norun'):
    print 'NNN will do tstmids:',tstmids
    sys.exit()

# -- YYYYYYYYYYYYYYYYYYYYYYYYYYYY years
#
syears=getYearsFromStmids(tstmids)

# -- LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL -- listing
#

# -- check if all are 9X, if so then do9Xonly
#
if(areStmids9X(tstmids)): do9Xonly=1    

dbtype=None
if(do9Xonly):  dbtype='%s-9X'%(AD2dbname)

if(dols or dolslong or dolsfull):
    rc=doListing(dsbdir,dbtype,tstmids,taids,dofilt9x=dobt,dolsong=dolslong,dolsfull=dolsfull,dtgopt=dtgopt,verb=verb)
    sys.exit()

# -- inventory of acards
#
ad2Is={}
if(ropt != 'norun' and not(relabelAD2)):
    for syear in syears:
        ad2Is[syear]=AdToAtcfInvHash(source,byear=syear,bnameBase='Inv-AD2',
                                      tbdir=dsbdir,
                                      verb=1,
                                      overrideInv=overrideInv,
                                      )



# -- mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm -- main processing section
#
MF.sTimer('ads-all')

# -- auto set corrTauDisCont
#
if(source == 'ecmwf' or source == 'ecbufr' or source == 'ec-wmo' or
   source == 'jt-nhc' or # -- handle aids with discontinuous taus or dtau >= 24.0
   source == 'tmtrkN' or source == 'mftrkN'): corrTauDisCont=1



# -- AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA -- make Adeck2()
#
if(doAdeck2 and relabelAD2):
    MF.sTimer('ads-relabel')
    (ad2s,byears)=relabelAdeck2Aids(tstmids,taids,dsbdir=dsbdir,verb=verb,override=overrideReLabelAD2)
    bd2s=None
    MF.dTimer('ads-relabel')

elif(doAdeck2 and phr == None):
    (ad2s,bd2s,byears)=makeAdeck2s(tstmids,taids,source,tD,ad2Is,tstmids9Xall,
                                   corrTauDisCont=corrTauDisCont,
                                   corrTauInc=6,dtgopt=dtgopt,
                                   overrideInvChk=overrideInvChk,overrideBD2=overrideBD2)

# -- IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII -- make 'I'|'2' Adeck2()
#
elif(phr != None and taids != None):
    MF.sTimer('ads-tinterp')
    (ad2s,bd2s,byears)=makeAdeck2Interp(tstmids,taids,phr,tD)
    MF.dTimer('ads-tinterp')
    
MF.dTimer('ads-all')

# -- PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP -- put Adeck2 to .pypdb file
#
if(doput and len(ad2s.keys()) > 0 and doAdeck2):
    
    # -- RRRRRR - check if running...
    #
    if(dochkIfRunning == 0): rc=MF.chkRunning(pyfile,strictChkIfRunning=1,killjob=1,nminWait=3)


    # -- PPPPAAAA - put Adeck2
    #
    MF.sTimer('ads-put')
    (aDSss,basins)=putAdeck2sDataSets(ad2s,dbtype=dbtype,dsbdir=dsbdir,doclean=killAd2,
                                      verb=verb)
    
    MF.dTimer('ads-put')

    for byear in byears:
        for basin in basins:
            try:
                aDSs=aDSss[basin,byear]
                asiz=MF.getPathSiz(aDSs.path)
                asiz=float(asiz)/(1024*1024)
                MF.sTimer('ads-put-%-5.0f Mb'%(asiz))
                MF.dTimer('ads-put-%-5.0f Mb'%(asiz))
            except:
                print 'WWW-ads-put no ADSs for byear: ',byear,' basin: ',basin
                #continue
        


    # -- PPPPBBBB - put Bdeck2
    #
    if(phr == None and bd2s != None):
        
        MF.sTimer('bds-put')
        bDSs=putBdeck2sDataSets(bd2s,dsbdir=dsbdir,
                                 doclean=overrideBD2,
                                 verb=verb)
    
        MF.dTimer('bds-put')

        for byear in byears:
            bsiz=MF.getPathSiz(bDSs[byear].path)
            bsiz=float(bsiz)/(1024)
            MF.sTimer('bds-put-%-5.0f Kb'%(bsiz))
            MF.dTimer('bds-put-%-5.0f Kb'%(bsiz))
        
else:
    aDSss={}
        
if(ropt != 'norun' and len(ad2Is) > 0): 
    for syear in syears:
        ad2Is[syear].put()


if(not(relabelAD2) and len(aDSss) > 0 and ( (w2.onKaze and doRsync2Kishou) or (w2.onKishou and doRsync2Kaze) ) ):
    rcKaze=chkifRunningOnKaze(pyfile,verb=verb)
    if(rcKaze and w2.onKishou): print 'WWW(%s) already running on wxmap2 or tcops...do NOT do rsync...sayounara...'%(pyfile) ;  sys.exit()
    
    for byear in byears:
        for basin in basins:
            try:
                aDSs=aDSss[basin,byear]
                spath=aDSs.path
                rc=doRsyncDSS2Kaze(spath,ropt=ropt)
            except:
                print 'WWW-rsync no ADSs for byear: ',byear,' basin: ',basin
                #continue

    # -- only do bdeck if not doing phr=0,6,12,...
    #
    if(phr == None):
        for byear in byears:
            bpath=bDSs[byear].path
            rc=doRsyncDSS2Kaze(bpath)


MF.dTimer('all-AD2')

sys.exit()
    
