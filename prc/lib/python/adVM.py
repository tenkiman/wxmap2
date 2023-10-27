from tcbase import *
from tcVM import *  # MFutils imported in tcVM


def getATsBTs(tD,source,tstmids,tdtg,taids,
              ATtauRange='-24.0',BTtauRange='-24',ATOtauRange=None,
              dupchk=1,
              verb=0,dtx=6):

    from tcbase import TcDataBdir,ADutils
    
    aDu=ADutils()

    def shiftTrkTaus(itrk,itaus,oattaus,offset):

        strk={}
        staus=[]
        for itau in itaus:
            stau=itau-offset
            if(stau < 0): continue
            if(len(oattaus) > 0 and not(stau in oattaus)): continue

            try:
                strk[stau]=itrk[itau]
                staus.append(stau)
            except:
                continue

        return(strk,staus)



    def shiftBTdtgs(btrk,bdtgs,finaldtg,bytaus=1):

        strk={}
        otimes=[]

        for bdtg in bdtgs:
            btau=mf.dtgdiff(finaldtg,bdtg)
            otime=bdtg
            if(bytaus): otime=btau
            # -- always add the otime to the list even if no data
            otimes.append(otime)
            try:
                strk[otime]=btrk[bdtg]
            except:
                continue

        return(strk,otimes)



    def getBtauEtau(taurange):

        tt=taurange.split('.')
        if(len(tt) == 1):
            btau=int(tt[0])
            etau=0
        elif(len(tt) == 2):
            btau=int(tt[0])
            etau=int(tt[1])
        else:
            CL.CmdLine()

        return(btau,etau)


    def getATotaus(taurange,dtx):

        tt=taurange.split('.')
        if(len(tt) == 1):
            etau=int(tt[0])
            btau=0
        elif(len(tt) == 2):
            btau=int(tt[0])
            etau=int(tt[1])
        else:
            CL.CmdLine()

        oattaus=range(btau,etau+dtx,dtx)
        return(oattaus)

    (btddtgBeg,btddtgEnd)=getBtauEtau(BTtauRange)
    (atddtgBeg,atddtgEnd)=getBtauEtau(ATtauRange)

    ibtdtgs=mf.dtgrange(mf.dtginc(tdtg,btddtgBeg),mf.dtginc(tdtg,btddtgEnd),dtx)
    iatdtgs=mf.dtgrange(mf.dtginc(tdtg,atddtgBeg),mf.dtginc(tdtg,atddtgEnd),dtx)

    if(ATOtauRange == None):
        oattaus=[]
    else:
        oattaus=getATotaus(ATOtauRange,dtx)

    ABs={}

    # -- get BTs
    #
    #(BTs,bstmids,fstmids)=tD.getBT4Dtg(tdtg,dupchk=dupchk)


    abstmids=[]
    aBTs={}

    # -- look through entire bdtg range for stmids and put in aBTs
    #

    for btdtg in ibtdtgs:
        (BTs,bstmids,fstmids)=tD.getBT4Dtg(btdtg,dupchk=1)
        
        #if(len(BTs.keys()) > 0): print 'qqqqqqqq',btdtg,'bbbb',bstmids,BTs.keys()
        btstmids=BTs.keys()
        for kk in btstmids:
            aBTs[kk]=BTs[kk]
            
        abstmids=abstmids+btstmids
            
    bstmids=mf.uniq(abstmids)
    

    if(tstmids != None):
        bstmids=tstmids

    goTtstmids=[]
    
    for tstmid in bstmids:
        
        (DSss,bd2s)=getAdeck2Bdeck2DSsByStmids(tstmid,verb=verb)
        DSs=DSss[tstmid]

        for taid in taids:

            MF.sTimer('aD2: %s %s'%(taid,tstmid))
            (AT,BT,aD)=getAidAdeck2Bdeck2FromDss(DSs,bd2s,taid,tstmid,verb=verb,warn=1)
            MF.dTimer('aD2: %s %s'%(taid,tstmid))

            if(AT == None):
                ABs[tstmid,taid]=(None,None,None)
                print 'WWW no data for taid: ',taid,' tstmid: ',tstmid
            else:
                if(tstmid != aD.tstmid): 
                    print
                    print 'WWWW got different tstmid from getAidAdeck2Bdeck2FromDss: ',tstmid,' aD.tstmid: ',aD.tstmid
                    tstmid=aD.tstmid
                    print
                    
                goTtstmids.append(tstmid)
                ABs[tstmid,taid]=(AT,BT,aD)
                
    if(goTtstmids != bstmids): bstmids=goTtstmids            
        
    print 'ggg get AtsBTs: ',goTtstmids,' bstmids: ',bstmids

    for tstmid in bstmids:
        
        if(isShemBasinStm(tstmid)):
            (snum,b1id,byear,b2id,stm2id,stm1id)=getStmParams(tstmid)
            tstmid1=tstmid
            if(b1id.upper() == 'S'): b1id2='P'
            if(b1id.upper() == 'P'): b1id2='S'
            tstmid2="%s%s.%s"%(tstmid1[0:2],b1id2,byear)
            try:
                BT2=aBTs[tstmid1]
            except:
                try:
                    print 'WWW---got second Bt...',tstmid2
                    BT2=aBTs[tstmid2]
                    #tstmid=tstmid2
                except:
                    print 'WWWWW no BT2 for tstmid: ',tstmid
        else:

            try:
                BT2=aBTs[tstmid]
            except:
                print 'WWW!!! no BT2 for tstmid: ',tstmid,' maybe wrong b1id? or mdk needs to be redone?  bad 9x?'''
                BT2=None
                
        
        for taid in taids:

            satrk={}
            sbtrk={}
            satimes=[]
            sbtimes=[]

            if(BT2 == None):
                ABs[tstmid,taid]=(satrk,satimes,sbtrk,sbtimes)
            else:

                print
                print 'Working-------- tstmid:',tstmid,' taid:',taid, ' tdtg:',tdtg

                (AT,BT,aD)=ABs[tstmid,taid]


                if(verb):
                    kk=BT.btrk.keys()
                    kk.sort()
                    for k in kk:
                        print '111 ',k,BT.btrk[k]

                    kk=BT2.btrk.keys()
                    kk.sort()
                    for k in kk:
                        print '222 ',k,BT2.btrk[k]

                # -- use md2 BT
                #
                BT=BT2

                doAT=1
                if(AT == None):
                    doAT=0
                    print 'WWW no AT for tstmid: ',tstmid,' taid: ',taid,' if in shem/io try other subbasin id...'

                    # -- do all shem storms...
                    #
                    rc=getStmParams(tstmid)
                    b1id=rc[1]
                    if(isShemBasinStm(tstmid)):
                        if(b1id == 'P'): nb1id='S'
                        if(b1id == 'S'): nb1id='P'
                        ntstmid=tstmid[0:2]+nb1id+tstmid[3:]
                        (AT,nBT,naD)=GetAidBestTrksFromDss(DSs,taid,ntstmid)

                        doAT=1
                        if(AT == None):
                            print 'WWW no joy for nstmid: ',ntstmid,' taid: ',taid,'...'
                            doAT=0


                #AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAATTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT
                #

                satrk={}
                satimes=[]

                if(doAT):
                    adtgs=AT.dtgs
                    atrk={}
                    adtgs.sort()

                    adtg=None

                    for dtg in iatdtgs:
                        if(dtg in adtgs):
                            adtg=dtg
                            if(verb): print 'HHHHHHHHHH for dtg: ',tstmid,dtg
                            atrk=AT.atrks[adtg]

                    if(adtg == None):
                        print 'WWW no AT.tracks in dtgrange: ',tstmid,iatdtgs
                    else:

                        adtgMhour=mf.dtgdiff(adtg,tdtg)
                        print 'AAA------------ adtg: ',adtg,'tdtg:',tdtg,'adtgMhour:',adtgMhour,'dtx: ',dtx

                        (iatrk,itaus)=aDu.FcTrackInterpFill(atrk,dtx=dtx)
                        
                        attaus=iatrk.keys()
                        attaus.sort()

                        if(verb):
                            for attau in attaus:
                                print 'AAA: ',attau,iatrk[attau]

                        (satrk,satimes)=shiftTrkTaus(iatrk,attaus,oattaus,offset=adtgMhour)

                        if(verb):
                            staus=satrk.keys()
                            for stau in staus:
                                print 'FFFAAA: ',stau,satrk[stau]

                #BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT
                #

                btrk=BT.btrk
                (ibtrk,ibtdtgsDEFINED)=aDu.FcTrackInterpFill(btrk,dtx=dtx)

                # -- ibtdtgs out of fctrackinterpfile has DEFINED times only! put it somewhere else...
                #

                if(verb):
                    btdtgs=ibtrk.keys()
                    btdtgs.sort()
                    for btdtg in btdtgs:
                        print 'BBB: ',btdtg,ibtrk[btdtg]

                (sbtrk,sbtimes)=shiftBTdtgs(ibtrk,ibtdtgs,tdtg)

                if(verb):
                    btdtgs=sbtrk.keys()
                    btdtgs.sort()
                    for btdtg in btdtgs:
                        print 'FFFBBB: ',btdtg,sbtrk[btdtg]

                ABs[tstmid,taid]=(satrk,satimes,sbtrk,sbtimes)

    return(ABs,bstmids)


def getATsBTsNew(tD,source,tstmids,tdtg,taids,
              ATtauRange='-24.0',BTtauRange='-24',ATOtauRange=None,
              dupchk=1,
              verb=0,dtx=6):
    
    """ new version that only uses ad2/bd2
"""

    
    from tcbase import TcDataBdir,ADutils
    
    aDu=ADutils()

    def shiftTrkTaus(itrk,itaus,oattaus,offset):

        strk={}
        staus=[]
        for itau in itaus:
            stau=itau-offset
            if(stau < 0): continue
            if(len(oattaus) > 0 and not(stau in oattaus)): continue

            try:
                strk[stau]=itrk[itau]
                staus.append(stau)
            except:
                continue

        return(strk,staus)


    def shiftBTdtgs(btrk,bdtgs,finaldtg,bytaus=1):

        strk={}
        otimes=[]

        for bdtg in bdtgs:
            btau=mf.dtgdiff(finaldtg,bdtg)
            otime=bdtg
            if(bytaus): otime=btau
            # -- always add the otime to the list even if no data
            otimes.append(otime)
            try:
                strk[otime]=btrk[bdtg]
            except:
                continue

        return(strk,otimes)


    def getBtauEtau(taurange):

        tt=taurange.split('.')
        if(len(tt) == 1):
            btau=int(tt[0])
            etau=0
        elif(len(tt) == 2):
            btau=int(tt[0])
            etau=int(tt[1])
        else:
            CL.CmdLine()

        return(btau,etau)


    def getATotaus(taurange,dtx):

        tt=taurange.split('.')
        if(len(tt) == 1):
            etau=int(tt[0])
            btau=0
        elif(len(tt) == 2):
            btau=int(tt[0])
            etau=int(tt[1])
        else:
            CL.CmdLine()

        oattaus=range(btau,etau+dtx,dtx)
        return(oattaus)

    # -- mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm main section
    #

    (btddtgBeg,btddtgEnd)=getBtauEtau(BTtauRange)
    (atddtgBeg,atddtgEnd)=getBtauEtau(ATtauRange)

    ibtdtgs=mf.dtgrange(mf.dtginc(tdtg,btddtgBeg),mf.dtginc(tdtg,btddtgEnd),dtx)
    iatdtgs=mf.dtgrange(mf.dtginc(tdtg,atddtgBeg),mf.dtginc(tdtg,atddtgEnd),dtx)

    if(ATOtauRange == None):
        oattaus=[]
    else:
        oattaus=getATotaus(ATOtauRange,dtx)

    abstmids=[]
    ABs={}

    for btdtg in ibtdtgs:
        (BTs,bstmids,fstmids)=tD.getBT4Dtg(btdtg,dupchk=1)
        abstmids=abstmids+bstmids
            
    bstmids=mf.uniq(abstmids)

    if(tstmids != None):
        bstmids=tstmids

    # -- now scan through bstmids and get ABs[]
    #
    
    goTtstmids=[]
    
    for tstmid in bstmids:
        
        (DSss,bd2s)=getAdeck2Bdeck2DSsByStmids(tstmid,verb=verb)
        DSs=DSss[tstmid]

        for taid in taids:

            MF.sTimer('aD2: %s %s'%(taid,tstmid))
            (AT,BT,aD)=getAidAdeck2Bdeck2FromDss(DSs,bd2s,taid,tstmid,verb=verb,warn=1)
            MF.dTimer('aD2: %s %s'%(taid,tstmid))

            if(AT == None):
                ABs[tstmid,taid]=(None,None,None)
                print 'WWW no data for taid: ',taid,' tstmid: ',tstmid
            else:
                if(tstmid != aD.tstmid): 
                    print
                    print 'WWWW got different tstmid from getAidAdeck2Bdeck2FromDss: ',tstmid,' aD.tstmid: ',aD.tstmid
                    tstmid=aD.tstmid
                    print
                    
                goTtstmids.append(tstmid)
                ABs[tstmid,taid]=(AT,BT,aD)
                
    bstmids=goTtstmids            
    verb=1

    for tstmid in bstmids:
        
        for taid in taids:

            satrk={}
            sbtrk={}
            satimes=[]
            sbtimes=[]

            print
            print 'Working-------- tstmid:',tstmid,' taid:',taid, ' tdtg:',tdtg

            (AT,BT,aD)=ABs[tstmid,taid]
            
            adtgs=AT.dtgs
            atrk={}
            adtgs.sort()

            adtg=None

            for dtg in iatdtgs:

                #AT.ls()
                
                if(dtg in adtgs):
                    adtg=dtg
                    if(verb): print 'HHHHHHHHHH for dtg: ',tstmid,dtg
                    atrk=AT.atrks[adtg]
                    print 'aaatttrrrkkk ',atrk

                    if(adtg == None):
                        print 'WWW no AT.tracks in dtgrange: ',tstmid,iatdtgs
                    else:
                
                        adtgMhour=mf.dtgdiff(adtg,tdtg)
                        print 'AAA------------ adtg: ',adtg,'tdtg:',tdtg,'adtgMhour:',adtgMhour,'dtx: ',dtx
                
                        (iatrk,itaus)=aDu.FcTrackInterpFill(atrk,dtx=dtx)
                        attaus=iatrk.keys()
                        attaus.sort()
                
                        if(verb):
                            for attau in attaus:
                                print 'AAA: ',attau,iatrk[attau]
                
                        (satrk,satimes)=shiftTrkTaus(iatrk,attaus,oattaus,offset=adtgMhour)
                
                        if(verb):
                            staus=satrk.keys()
                            for stau in staus:
                                print 'FFFAAA: ',stau,satrk[stau]
                
            #BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT
            #
        
            btrk=BT.btrk
            (ibtrk,ibtdtgsDEFINED)=aDu.FcTrackInterpFill(btrk,dtx=dtx)
        
            # -- ibtdtgs out of fctrackinterpfile has DEFINED times only! put it somewhere else...
            #
        
            if(verb):
                btdtgs=ibtrk.keys()
                btdtgs.sort()
                for btdtg in btdtgs:
                    print 'BBB: ',btdtg,ibtrk[btdtg]
        
            (sbtrk,sbtimes)=shiftBTdtgs(ibtrk,ibtdtgs,tdtg)
        
            if(verb):
                btdtgs=sbtrk.keys()
                btdtgs.sort()
                for btdtg in btdtgs:
                    print 'FFFBBB: ',btdtg,sbtrk[btdtg]
        
            ABs[tstmid,taid]=(satrk,satimes,sbtrk,sbtimes)


    return(ABs,bstmids)



def errAD(option,opt=None):

    if(option == 'tstmids'):
        print 'EEE # of tstmids = 0 :: no stms to verify...stmopt: ',opt
    elif(option == 'tstms'):
        print 'EEE # of tstms from stmopt: ',opt,' = 0 :: no stms to verify...'
    else:
        print 'Stopping in errAD: ',opt

    sys.exit()


def makeEnsMeanAdeck(aDS,mD,source,tstms,year,dtau=12,etau=168,doput=1,verb=0,override=0):
    """
given adeck aDS and mdeck mD find ensemble/con mean and spread
and put to aDS
    """
    taus=range(0,etau+1,dtau)

    omodel=None
    smodel=None
    emtrks={}
    estrks={}
    vds={}

    (omodel,smodel)=SetMeanSpreadOmodels(source)
    if(omodel == None): errAD('omodel',source)

    ## # -- code to check if already done...but not useful during season as storms are updated...
    ## #
    ## (omodels,ostmids)=GetAidsStormsFromDss(aDS,None,tstms,dofilt9x=1)
    ## dostms=[]
    ## for ostmid in ostmids:
    ##     (omodels,dstmids)=GetAidsStormsFromDss(aDS,omodel,ostmid,dofilt9x=1)
    ##     if(len(omodels) == 1 and not(override)):
    ##         print 'WWW',omodel,' already done and override=0 for tstm: ',tstmid
    ##     else:
    ##         dostms.append(tstm)

    ## if(len(dostms) == 0):
    ##     return(None,None,[])

    taids=None
    (eaids,tstmids)=GetAidsStormsFromDss(aDS,taids,tstms,dofilt9x=1)
    (eaids,daid,dsource)=FilterEaids(eaids,source,year)

    if(len(tstmids) == 0): errAD('tstmids')


    ATs={}

    naidsMaxMissing=3
    naidsEns=len(eaids)

    ostmids=[]
    for tstmid in tstmids:
        fBT=None
        naids=0
        for eaid in eaids:
            (AT,BT,taD)=GetAidBestTrksFromDss(aDS,eaid,tstmid,verb=verb)
            if(BT != None and fBT == None): fBT=BT
            ATs[eaid]=AT
            if(AT == None): continue
            print 'AAAA GOT adeck for: ',eaid,tstmid
            naids=naids+1

        naidsMissing=naidsEns-naids
        print 'naids: ',naids,' naidsMissing: ',naidsMissing
        if(naidsMissing >= naidsMaxMissing or naids == 0):
            print 'WWW naidsMissing: ',naidsMissing,' >= naidsMaxMissing: ',naidsMaxMissing,' bypass... or naids=0: ',naids
            print 'eaids: ',eaids
            continue

        (emtrks,emacards)=setEnsMeanTrk(ATs,eaids,taus,omodel,tstmid,percentMin=40.0,verb=verb)
        (estrks,esacards)=setEnsSpreadTrk(emtrks,ATs,fBT,eaids,taus,smodel,tstmid,verb=verb)


        emad=makeAdeckByCards(mD,emacards)
        # -- add mean and spread ads to aDS datasets
        #
        if(emad != None):  addAdeck2DataSets(emad,aDS)
        else:               print 'WWW no   mean adecks for source: ',source,' tstmid: ',tstmid

        if(estrks == None):
            print 'WWWWWWSSSSSSSS in makeEnsMeanAdeck: estrks = None for tstm: ',tstmid
        else:
            esad=makeAdeckByCards(mD,esacards)
            if(esad != None):  addAdeck2DataSets(esad,aDS)
            else:               print 'WWW no spread adecks for source: ',source,' tstmid: ',tstmid
        ostmids.append(tstmid)


    ostmids=mf.uniq(ostmids)
    return(omodel,smodel,ostmids)

        #return(emtrks,emacards,estrks,esacards)



def FilterEaids(eaids,source,year):
    """
based on pull out only ensemble member aids
    """
    oeaids=[]

    if(mf.find(source,'ecm')):
        for eaid in eaids:
            try:
                enum=int(eaid[2:4])
            except:
                enum=-999
            if(eaid[0:2] == 'ep' and (enum >= 1 and enum <= 50) or eaid == 'ecnt'):
                oeaids.append(eaid)

        daid='edet'
        dsource=source


    elif(mf.find(source,'ecbufr')):
        for eaid in eaids:
            try:
                enum=int(eaid[2:4])
            except:
                enum=-999
            if(eaid[0:2] == 'ee' and (enum >= 1 and enum <= 50) or eaid == 'ecme'):
                oeaids.append(eaid)

        daid='ecmo'
        dsource=source


    elif(mf.find(source,'ukm')):
        oeaids=eaids
        daid='ukmo'
        daid='egrr'
        dsource=['nhc','jtwc']

    elif(source == 'gfsenkf' or source == 'gfsenkf2012'):

        for eaid in eaids:
            try:
                enum=int(eaid[2:4])
            except:
                enum=-999

            #if(eaid[0:2] == 'ge' and (enum >= 1 and enum <= 21)): -- 2009 version, below is for 2010 running tim marchok genesis tracker
            #if(eaid[0:2] == 'gk' and (enum >= 1 and enum <= 20)): -- 2010 special case
            #if(eaid[0:2] == 'ge' and (enum >= 1 and enum <= 21)):    # 2009 version
            if(int(year) == 2011):
                if(eaid[0:2] == 'ge' and (enum >= 1 and enum <= 21)):   # for 2008,2010->
                    oeaids.append(eaid)
            elif(int(year) == 2012):
                if(eaid[0:2] == 'ge' and (enum >= 1 and enum <= 20)):   # for 2008,2010->
                    oeaids.append(eaid)
            else:
                if(eaid[0:2] == 'gk' and (enum >= 1 and enum <= 20)):   # for 2008,2010->
                    oeaids.append(eaid)

        daid='avno'
        dsource='ncep'

    elif(source == 'fimens'):

        oeaidsfe=[]
        for eaid in eaids:
            try:
                enum=int(eaid[2:4])
            except:
                enum=-999

            #if(eaid[0:2] == 'ge' and (enum >= 1 and enum <= 21)): -- 2009 version, below is for 2010 running tim marchok genesis tracker
            #if(eaid[0:2] == 'gk' and (enum >= 1 and enum <= 20)): -- 2010 special case
            #if(eaid[0:2] == 'ge' and (enum >= 1 and enum <= 21)):    # 2009 version

            # for 2008,2010->
            if(int(year) == 2011):
                if(
                    eaid[0:2] == 'ge' and (enum >= 1 and enum <= 11) or
                    eaid[0:2] == 'fe' and (enum >= 1 and enum <= 10) 
                    ):   
                    oeaids.append(eaid)
            elif(int(year) == 2012):
                if(
                    eaid[0:2] == 'fe' and (enum >= 1 and enum <= 10) 
                    ):   
                    oeaidsfe.append(eaid)
                if(
                    eaid[0:2] == 'ge' and (enum >= 1 and enum <= 10) or
                    eaid[0:2] == 'fe' and (enum >= 1 and enum <= 10) 
                    ):   
                    oeaids.append(eaid)
            else:
                if(eaid[0:2] == 'gk' and (enum >= 1 and enum <= 20)):   # for 2008,2010->
                    oeaids.append(eaid)

        ## dddddddddd can't work because taids are all aids in the database
        ## # -- check if there are fimens aids, if not set oeads=[]
        ## #
        ## if(len(oeaidsfe) == 0):
        ##     print 'WWW(FilterEaids,fimens,2012): no fimens aids for the combined fimens + gfsenkf'
        ##     oeaids=[]


        daid='avno'
        dsource='ncep'

    elif(source == 'fimensg7'):

        oeaidsfe=[]
        for eaid in eaids:
            try:
                enum=int(eaid[2:4])
            except:
                enum=-999

            #if(eaid[0:2] == 'ge' and (enum >= 1 and enum <= 21)): -- 2009 version, below is for 2010 running tim marchok genesis tracker
            #if(eaid[0:2] == 'gk' and (enum >= 1 and enum <= 20)): -- 2010 special case
            #if(eaid[0:2] == 'ge' and (enum >= 1 and enum <= 21)):    # 2009 version

            # for 2008,2010->
            if(int(year) == 2011):
                if(
                    eaid[0:2] == 'ge' and (enum >= 1 and enum <= 11) or
                    eaid[0:2] == 'fe' and (enum >= 1 and enum <= 10) 
                    ):   
                    oeaids.append(eaid)
            elif(int(year) == 2012):
                if(
                    eaid[0:2] == 'fe' and (enum >= 1 and enum <= 10) 
                    ):   
                    oeaidsfe.append(eaid)
                if(
                    eaid[0:2] == 'ge' and (enum >= 1 and enum <= 10) or
                    eaid[0:2] == 'fe' and (enum >= 1 and enum <= 10) 
                    ):   
                    oeaids.append(eaid)
            else:
                if(eaid[0:2] == 'gk' and (enum >= 1 and enum <= 20)):   # for 2008,2010->
                    oeaids.append(eaid)

        ## dddddddddd can't work because taids are all aids in the database
        ## # -- check if there are fimens aids, if not set oeads=[]
        ## #
        ## if(len(oeaidsfe) == 0):
        ##     print 'WWW(FilterEaids,fimens,2012): no fimens aids for the combined fimens + gfsenkf'
        ##     oeaids=[]


        daid='avno'
        dsource='ncep'

    elif(source == 'fimens0'):
        for eaid in eaids:
            try:
                enum=int(eaid[2:4])
            except:
                enum=-999

            if(
                eaid[0:2] == 'fe' and (enum >= 1 and enum <= 10) 
                ):   
                oeaids.append(eaid)

        daid='avno'
        dsource='ncep'

    elif(source == 'fimens2'):
        for eaid in eaids:
            try:
                enum=int(eaid[2:4])
            except:
                enum=-999

            if(int(year) == 2011):
                if(
                    eaid[0:2] == 'ge' and (enum >= 11 and enum <= 21) or
                    eaid[0:2] == 'fe' and (enum >= 1 and enum <= 10) 
                    ):   
                    oeaids.append(eaid)
            else:
                if(eaid[0:2] == 'gk' and (enum >= 1 and enum <= 20)):   # for 2008,2010->
                    oeaids.append(eaid)

        daid='avno'
        dsource='ncep'

    elif(source == 'fimens3'):
        for eaid in eaids:
            try:
                enum=int(eaid[2:4])
            except:
                enum=-999

            if(int(year) == 2011):
                if(
                    eaid[0:2] == 'ge' and (enum >= 1 and enum <= 21) or
                    eaid[0:2] == 'fe' and (enum >= 1 and enum <= 10) 
                    ):   
                    oeaids.append(eaid)

        daid='avno'
        dsource='ncep'

    elif(source == 'gfsenkf_irwd'):
        for eaid in eaids:
            try:
                enum=int(eaid[2:4])
            except:
                enum=-999
            #if(eaid[0:2] == 'ge' and (enum >= 1 and enum <= 21)): -- 2009 version, below is for 2010 running tim marchok genesis tracker
            if(eaid[0:2] == 'gi' and (enum >= 1 and enum <= 20)):
                oeaids.append(eaid)

        daid='avno'
        dsource='ncep'

    elif(source == 'gfsenkf_irwdx'):
        for eaid in eaids:
            try:
                enum=int(eaid[2:4])
            except:
                enum=-999
            #if(eaid[0:2] == 'ge' and (enum >= 1 and enum <= 21)): -- 2009 version, below is for 2010 running tim marchok genesis tracker
            if(eaid[0:2] == 'gx' and (enum >= 1 and enum <= 20)):
                oeaids.append(eaid)

        daid='avno'
        dsource='ncep'

    elif(mf.find(source,'ncep') or mf.find(source,'nhc')):
        for eaid in eaids:
            try:
                enum=int(eaid[2:4])
            except:
                enum=-999
            if(eaid[0:2] == 'ap' and (enum >= 1 and enum <= 20) or eaid == 'ac00'):
                oeaids.append(eaid)

            daid='avno'
            dsource=source

    elif(mf.find(source,'cmc') ):

        for eaid in eaids:
            try:
                enum=int(eaid[2:4])
            except:
                enum=-999
            if(eaid[0:2] == 'cp' and (enum >= 1 and enum <= 20) or eaid == 'cc00'):
                oeaids.append(eaid)

            daid='cmc'
            dsource=source

    elif(mf.find(source,'tacc')):
        for eaid in eaids:
            try:
                enum=int(eaid[2:4])
            except:
                enum=-999
            if(eaid[0:2] == 'f8' and (enum >= 1 and enum <= 20) or eaid == 'f8em'):
                oeaids.append(eaid)

            daid='f9em'
            dsource=source

    else:
        oeaids=eaids
        daid='MMMM'

    return(oeaids,daid,dsource)


def getEaidsTrks(DSs,eaids,stmid,verb=1,warn=1,do9xrelab=0):

    if(type(eaids) is not(ListType)):
        eaids=[eaids]

    tstmid=stmid.upper()

    trks={}
    dtgs=[]
    ats=None
    bts=None
    ac=None
    A=None

    n=0
    for eaid in eaids:

        dskey="%s_%s"%(eaid,tstmid)
        if(verb): print 'getting: ',dskey
        try:
            ac=DSs.db[dskey]
        except:
            if(warn): print 'WWWWWWWWWWWWWWW getEaidsTrks -- no adecks for ',dskey
            continue

        if(do9xrelab):
            if(verb): print 'before Relabe9XAcards len(ac.acards): ',len(ac.acards)
            ac=Relabel9xAcards(ac,tstmid)
            if(verb): print 'after  Relabe9XAcards len(ac.acards): ',len(ac.acards)

        A=AD.AdeckAcardsDtgHash(ac.acards)

        BT=A.GetBestTrk(stmid)
        if(BT == None): continue
        btdtgs=BT.dtgs
        btdtgs.sort()

        if(verb): print 'before  RemoveNonBtAcards len(ac.acards): ',len(ac.acards)
        ac=RemoveNonBtAcards(ac,stmid,btdtgs,verb=1)
        if(verb): print 'after   RemoveNonBtAcards len(ac.acards): ',len(ac.acards)

        # cycle if no valid posits in acards
        #
        if(len(ac.acards) == 0): continue


        A=AD.AdeckAcardsDtgHash(ac.acards)
        ats=A.GetAidTrk(eaid,tstmid)
        bts=A.GetBestTrk(tstmid)

        trks[eaid]=ats.trks
        dtgs=dtgs+trks[eaid].keys()

        for dtg in trks[eaid].keys():
            taus=trks[eaid][dtg].keys()

            for tau in taus:
                trks[eaid,dtg,tau]=trks[eaid][dtg][tau]

        dtgs=MF.uniq(dtgs)
        n=n+1

    return(trks,dtgs,ats,bts,ac,A)


def SetMeanSpreadOmodels(source):

    omodel=smodel=None
    if(source == 'ecmwf'):
        omodel='eemn'
        smodel='eesp'

    elif(source == 'ecbufr'):
        omodel='ecmn'
        smodel='ecsp'

    elif(source == 'ukmo'):
        omodel='uemn'
        smodel='uesp'

    elif(source == 'ncep_eps' or source == 'nhc'):
        omodel='nemn'
        smodel='nesp'

    elif(source == 'gfsenkf' or source == 'gfsenkf2012'):
        omodel='gkmn'
        smodel='gksp'

    elif(source == 'fimens' or source == 'fimensg7'):
        omodel='fgmn'
        smodel='fgsp'

    elif(source == 'fimens0'):
        omodel='femn'
        smodel='fesp'

    elif(source == 'fimens2'):
        omodel='fg2mn'
        smodel='fg2sp'

    elif(source == 'fimens3'):
        omodel='fg3mn'
        smodel='fg3sp'

    elif(source == 'gfsenkf_irwd'):
        omodel='gimn'
        smodel='gisp'

    elif(source == 'gfsenkf_irwdx'):
        omodel='gxmn'
        smodel='gxsp'

    elif(source == 'cmc_eps'):
        omodel='ccmn'
        smodel='ccsp'

    elif(source == 'tacc'):
        omodel='f8mn'
        smodel='f8sp'

    return(omodel,smodel)




def setEnsMeanTrk(ATs,eaids,taus,model,stmid,percentMin=40.0,minTau0=0,percentMin0=70.0,verb=0):

    # ensemble mean track + member tracks
    #

    alldtgs=[]
    for eaid in eaids:
        try:     adtgs=ATs[eaid].dtgs
        except:  adtgs=[]
        alldtgs=alldtgs+adtgs

    alldtgs=MF.uniq(alldtgs)

    nmembers=len(eaids)

    emtrks={}
    acards={}

    for dtg in alldtgs:

        iokmean=0
        tau0ok=1

        for tau in taus:

            lats=[]
            lons=[]
            pmins=[]
            vmaxs=[]
            iok=0

            for eaid in eaids:

                try:
                    aT=ATs[eaid].atrks
                except:
                    if(verb): print 'WWWW no AT for eaid: ',eaid,tau,dtg
                    continue

                try:
                    (lat,lon,vmax,pmin,r34,r50,r65)=aT[dtg][tau]
                    lats.append(lat)
                    lons.append(lon)
                    if(vmax <= 0.0):
                        vmax=-999.0
                    if(pmin < 0.0):
                        pmin=-999.0
                    vmaxs.append(vmax)
                    pmins.append(pmin)
                    iok=1
                except:
                    if(verb >= 1): print 'NNNN tracks for: ',eaid,dtg,tau,' <- NNNNN'

                if(verb and iok):
                    print 'FFFF tracks for: ',eaid,dtg,tau


            if(iok):
                mlat=0.0
                mlon=0.0
                mpmin=0.0
                mvmax=0.0
                nll=0
                nvm=0
                npm=0

                for n in range(0,len(lats)):
                    mlat=mlat+lats[n]
                    mlon=mlon+lons[n]
                    if(pmins[n] > 0.0):
                        mpmin=mpmin+pmins[n]
                        npm=npm+1
                    if(vmaxs[n] > 0.0):
                        mvmax=mvmax+vmaxs[n]
                        nvm=nvm+1

                    nll=nll+1

                pnll=(float(nll)/float(nmembers))*100.0

                # -- require >= percentMin0 (70) at tau=minTau0 (0) to continue doing mean
                #
                if(tau <= minTau0 and nll > 0 and pnll < percentMin0):
                    print 'WWW tau0ok=0 pnll: ',pnll,' stmid: ',stmid,' dtg: ',dtg
                    tau0ok=0

                if(nll > 0 and pnll >= percentMin and tau0ok):
                    iokmean=1
                    mlat=mlat/float(nll)
                    mlon=mlon/float(nll)

                    if(nvm > 0):
                        mvmax=mvmax/float(nvm)

                    if(npm > 0):
                        mpmin=mpmin/float(npm)

                    if(verb): print 'nll---- ',eaid,dtg,tau,"%4.1f"%(pnll),nmembers,nll,mlat,mlon,' nvm ',nvm,mvmax,' npm ',npm,mpmin

                    try:
                        emtrks[dtg][tau]=(mlat,mlon,mvmax,mpmin,None,None,None,pnll)
                    except:
                        emtrks[dtg]={}
                        emtrks[dtg][tau]=(mlat,mlon,mvmax,mpmin,None,None,None,pnll)


        if(iokmean):
            acds=MakeAdeckCards(model,dtg,emtrks[dtg],stmid)
            acards[dtg]=acds

        else:
            print 'WWW found NO mean tracks at ANY tau for dtg: ',dtg

    return(emtrks,acards)


def setEnsSpreadTrk(emtrks,ATs,BT,eaids,taus,model,stmid,verb=0):


    alldtgs=emtrks.keys()
    alldtgs.sort()

    nmembers=len(eaids)

    try:
        btcs=BT.btcs
        btdtgs=BT.dtgs
    except:
        print 'WWWW no bts in setEnsSpreadTrk...'
        return(None,None)

    estrks={}
    acards={}

    print alldtgs
    print btdtgs
    
    for dtg in alldtgs:

        iokmean=0
        for tau in taus:

            vdtg=mf.dtginc(dtg,tau)

            try:
                rc=btcs[vdtg]
                blat=rc[0]
                blon=rc[1]
                bvmax=rc[2]
                bpmin=rc[3]
                bdir=rc[4]
                bspd=rc[5]
                iokbt=1
            except:
                (blat,blon,bvmax,bpmin,bdir,bspd)=(-99.9,-999.9,-99.9,-999.,-999.9,-99.9)
                iokbt=0

            iokm=1
            try:
                (mlat,mlon,mvmax,mpmin,evar1,evar2,evar3,pnll)=emtrks[dtg][tau]
                if(mvmax <= 0.0):
                    mvmax=-999.0
                if(mpmin < 0.0):
                    mpmin=-999.0
            except:
                iokm=0
                if(verb >= 1): print 'NNNN no tracks for ',dtg,tau



            mdist=0.0
            nd=0
            for eaid in eaids:

                try:
                    aT=ATs[eaid].atrks
                except:
                    if(verb): print 'WWWW no AT for eaid: ',eaid,tau,dtg
                    continue

                try:
                    (lat,lon,vmax,pmin,r34,r50,r64)=aT[dtg][tau]
                    if(vmax <= 0.0):
                        vmax=-999.0
                    if(pmin < 0.0):
                        pmin=-999.0
                    iok=1
                except:
                    iok=0
                    if(verb >= 1): print 'NNNN tracks for: ',eaid,dtg,tau,' <- NNNNN (spread)'


                if(verb and iok):
                    print 'FFFF tracks for: ',eaid,dtg,tau,iok,iokm,' <- FFFF (spread)'


                if(iok and iokm):
                    dlat=lat-mlat
                    dlon=lon-mlon
                    dvmax=vmax-mvmax
                    dist=gc_dist(lat,lon,mlat,mlon)
                    mdist=mdist+dist
                    nd=nd+1

            # project the mean of the spread (distance between mean and member)
            # from the bt so 'fe' calc in vdeck will give the mean spread
            #
            if(nd > 1):

                mdist=mdist/nd

                if(iokbt):
                    course=90.0
                    dt=12.0
                    speed=mdist/dt
                    (slat,slon)=rumltlg(course,speed,dt,blat,blon)
                    svmax=65.0
                    spmin=990.0
                else:
                    continue

                pnll=(float(nd)/float(nmembers))*100.0

                try:
                    estrks[dtg][tau]=(slat,slon,svmax,spmin,None,None,None,pnll)
                except:
                    estrks[dtg]={}
                    estrks[dtg][tau]=(slat,slon,svmax,spmin,None,None,None,pnll)

                iokmean=1

        if(iokmean):
            acds=MakeAdeckCards(model,dtg,estrks[dtg],stmid)
            acards[dtg]=acds

        else:
            #trk=estrks[dtg]
            #acards[dtg]=AD.MakeAdeckCards(omodel,dtg,trk,stmid,verb=verb)
            print 'SSSS(spread) found NO mean tracks at ANY tau for dtg: ',dtg



    return(estrks,acards)







def CmpAdeckMtimeSize(mtime1,size1,mtime2,size2,timeonly=0,sizeonly=0):

    rc=1
    (dtg1,mmss1)=mtime1.split(':')
    (dtg2,mmss2)=mtime2.split(':')

    dtg1=int(dtg1)
    dtg2=int(dtg2)
    mmss1=int(mmss1)
    mmss2=int(mmss2)

    timecmp=(dtg1 == dtg2 and mmss1 == mmss2)
    sizecmp=(size1 == size2)

    if(timeonly):
        if(timecmp): rc=0
    elif(sizeonly):
        if(sizecmp):
            rc=0
    else:
        if(timecmp and sizecmp):  rc=0

    return(rc)


def makeNewAdecksStmids(newadecks,year,aliases,skipcarq=1):

    from adCL import AtcfAdeckPaths
    
    nadps=AtcfAdeckPaths(adecks=newadecks)
    nads=MakeAdecksByYear(nadps,year,aliases=aliases,skipcarq=skipcarq)
    kk=nads.keys()
    kstmids=MF.uniq(kk)
    stmids=[]
    for kstmid in kstmids:
        stmid=kstmid.split('_')[1]
        stmids.append(stmid)

    stmids=MF.uniq(stmids)

    return(nads,stmids)


def updateAds(nads,source,docp1st=0,verb=1):

    from tcbase import TcDataBdir
    dsbdir="%s/DSs"%(TcDataBdir)
    dbtype='adeck'
    backup=0
    chkifopen=0

    oads={}

    ndskeys=nads.keys()

    DSsS={}
    dskeysS={}

    # -- get storm year from keys
    #
    
    if(len(ndskeys) == 0):
        # -- no ads to update return
        print 'III(AD.updateAds): len(ndskeys) = 0 -- no new ads to update -- return...' 
        return(oads,nads,DSsS)
    
    for dskey in ndskeys:
        year=dskey.split('.')[1]
        MF.loadDictList(dskeysS,year,dskey)

    years=dskeysS.keys()
    years=mf.uniq(years)

    # -- make DSs for each storm year
    #
    for year in years:
        dbname="%s_%s_%s"%(dbtype,source,year)
        dbfile="%s.pypdb"%(dbname)
        DSsS[year]=DataSets(bdir=dsbdir,name=dbfile,dtype=dbtype,verb=verb,chkifopen=chkifopen,docp1st=docp1st,doDSsWrite=1)


    for dskey in ndskeys:
        year=dskey.split('.')[1]
        DSs=DSsS[year]

        try:
            oads[dskey]=DSs.getDataSet(dskey)
        except:
            pass

    for dskey in ndskeys:

        year=dskey.split('.')[1]
        DSs=DSsS[year]
        nad=nads[dskey]

        if(verb):
            nkks=nad.ats.keys()
            nkks.sort()
            print 'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB ',nkks

        try:
            oad=oads[dskey]
        except:
            oad=None

        fats={}
        facards={}
        if(oad and nad):

            if(verb): print 'AD.updateAds: need to merge key: ',dskey

            if(not(hasattr(oad,'ats'))): continue

            oats=oad.ats
            nats=nad.ats
            oaacs=oad.acards
            naacs=nad.acards

            odtgs=oats.keys()
            ndtgs=nats.keys()

            odtgs.sort()
            ndtgs.sort()

            fdtgs=odtgs+ndtgs
            fdtgs=MF.uniq(fdtgs)

            fdtgs.sort()

            if(len(odtgs) != len(fdtgs) and verb):
                print 'AD.updateAds dtgs for dskey: ',dskey,odtgs[-1],len(odtgs),ndtgs[-1],len(ndtgs),fdtgs[-1],len(fdtgs)

            fadtgs=[]
            for fdtg in fdtgs:
                try:
                    ftn=nats[fdtg]
                    facs=naacs[fdtg]
                except:
                    ftn=oats[fdtg]
                    facs=oaacs[fdtg]

                fats[fdtg]=ftn
                facards[fdtg]=facs
                fadtgs.append(fdtg)


            nad.ats=fats
            nad.acards=facards
            nad.dtgs=fadtgs

            nad.updatedtghms=mf.dtg('dtg.hms')

            if(verb):
                okks=oad.ats.keys()
                okks.sort()
                print 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA ',okks

        nads[dskey]=nad

    return(oads,nads,DSsS)



def updateAcs(nacs,verb=0):

    kk=nacs.keys()

    oacs={}
    for k in kk:
        try:
            oacs[k]=DSs.getDataSet(k)
        except:
            pass

    for k in kk:
        nac=nacs[k]
        try:
            oac=oacs[k]
        except:
            oac=None

        if(oac and nac):
            if(verb): print 'need to merge key: ',k
            dtgs=oac.dtgs+nac.dtgs
            dtgs=MF.uniq(dtgs)
            acards={}
            for dtg in dtgs:
                try:
                    ocard=oac.acards[dtg]
                except:
                    ocard=None
                try:
                    ncard=nac.acards[dtg]
                except:
                    ncard=None

                if(ncard != None):
                    acards[dtg]=ncard
                elif(ocard != None):
                    acards[dtg]=ocard
                else:
                    print 'EEE ocard and ncard = None'
                    sys.exit()

            nac.dtgs=dtgs
            nac.acards=acards
            nac.updatedtghms=mf.dtg('dtg.hms')

        nacs[k]=nac

    return(nacs)



def getNewadecks(curadps,oldadps,sizeonly=0,timeonly=0):

    newadecks=[]
    for cpath in curadps.paths:
        cmtime=curadps.mtime[cpath][0]
        csize=curadps.size[cpath]
        try:
            omtime=oldadps.mtime[cpath][0]
            osize=oldadps.size[cpath]
        except:
            print 'WWW new adeck',cpath
            newadecks.append(cpath)
            continue

        if(CmpAdeckMtimeSize(cmtime,csize,omtime,osize,sizeonly=sizeonly,timeonly=timeonly)):
            print 'WWW different size/age adeck: ',cpath,'size: ',csize,osize,' time: ',cmtime,omtime
            newadecks.append(cpath)

    return(newadecks)





def updateDSs(nads,oldkeys,curadps,stmids,DSsS,DSsAdpsKeys=None,verb=1):

    newkeys=nads.keys()
    newkeys.sort()
    if(len(newkeys) == 0): return(0)

    # get all keys
    #
    allkeys=newkeys+oldkeys
    allkeys=MF.uniq(allkeys)
    allkeys.sort()

    # adeck objects
    #
    MF.sTimer('AD.updateDSs.newkeys')
    for newkey  in newkeys:

        year=newkey.split('.')[1]
        DSs=DSsS[year]

        # turn on  for DSs
        #
        if(verb): DSs.verb=1

        ds=nads[newkey]
        DSs.putDataSet(ds,newkey,verb=1)

    MF.dTimer('AD.updateDSs.newkeys')

    # -- keys,paths,etc...come in on the current year DSs,
    #    if at end of year there are not curyear NHEM storms then they would be put
    #    on the SHEM year vice the curyear
    # -- orginal 
    # -- put keys, paths, stmids on first year DSsS
    years=DSsS.keys()
    years.sort()
    DSs=DSsS[years[0]]
    
    # -- optionally put on curyear DSs vice first!
    #
    if(DSsAdpsKeys != None):  DSs=DSsAdpsKeys

    # keys
    #
    key='keys'
    MF.sTimer('AD.updateDSs.keys')
    dsk=DataSet(name=key,dtype='hash')
    dsk.data=allkeys
    DSs.putDataSet(dsk,key)
    MF.dTimer('AD.updateDSs.keys')

    # adeck paths
    #
    key='adps'
    MF.sTimer('AD.updateDSs.adps')
    dsk=DataSet(name=key,dtype='hash')
    dsk.data=curadps
    DSs.putDataSet(dsk,key)
    MF.dTimer('AD.updateDSs.adps')

    # new stmids paths as dict w/ time stamp key
    #
    key='updatestmids'
    dsk=DSs.getDataSet(key)
    if(dsk == None):
        dsk=DataSet(name=key,dtype='hash')

    try:
        ostmids=dsk.data
    except:
        ostmids={}

    updatedtghms=mf.dtg('dtg.hms')
    try:
        ostmids[updatedtghms]=stmids
    except:
        ostmids={}
        ostmids[updatedtghms]=stmids

    MF.sTimer('AD.updateDSs.updatestmids')
    dsk.data=ostmids
    DSs.putDataSet(dsk,key)
    MF.dTimer('AD.updateDSs.updatestmids')

    # -- close causing probs with -d -u -- don't close here do in adk
    #
    #DSs.closeDataSet()

    # turn off verb for DSs
    #
    if(verb): DSs.verb=0

    return(1)


def GetAdmaskAdecks(source,year,tstmids=None,dtgopt=None):

    from adCL import AdeckSources
    from tcVM import getStmParams
    from tcbase import AdeckBaseDir
    
    AS=AdeckSources()
    sources=AS.getSourcesbyYear(year=year)

    admasks=None
    if(not(source in sources)):
        print 'EEE invalid source in AD.GetAdmaskAdecks source: ',source,' year: ',year
        sys.exit()


    # -- exclude new [A-Z][0-9] for 9x at nhc and jtwc
    #
    if(source == 'nhc'):
        sdir="%s/nhc/%s"%(AdeckBaseDir,year)
        smask="%s/a??[0-9]?%s*dat"%(sdir,year)

    # -- do by basin in case there are problems
    #
    elif(source == 'jtwc'):
        sdir="%s/jtwc/%s"%(AdeckBaseDir,year)
        smask='%s/a??[0-5][0-9]%s.dat'%(sdir,year)
        smaskwp='%s/awp[0-5][0-9]%s.dat'%(sdir,year)
        # -- for cases going from epac -> cpac -> wpac
        smaskep='%s/aep[0-5][0-9]%s.dat'%(sdir,year)
        smaskcp='%s/acp[0-5][0-9]%s.dat'%(sdir,year)
        smaskio='%s/aio[0-5][0-9]%s.dat'%(sdir,year)
        smasksh='%s/ash[0-5][0-9]%s.dat'%(sdir,year)
        # make like nhc 2013 with 9x causeing failure
        #smask='%s/a??[A-Z,0-9]?%s.dat'%(sdir,year)
        #smask='%s/awp30%s.dat'%(sdir,year)
        # test 20100408 smask='%s/a[c,e]p9?%s.dat'%(sdir,year)
        
        admasks=[
            smaskwp,
            smaskio,
            smasksh,
            smaskep,
            smaskcp,
        ]
        
    # -- big master file at ncep
    #
    elif(source == 'ncep'):
        sdir="%s/ncep/%s"%(AdeckBaseDir,year)
        smask='%s/tracks.atcfunix.%02d'%(sdir,int(str(year)[2:4]))
        smask='%s/tracks.all.%s*.txt'%(sdir,year)

        yearp1=int(year)+1
        yearp1=str(yearp1)
        sdirp1="%s/%s/%s"%(AdeckBaseDir,source,yearp1)
        smaskp1='%s/tracks.all.%s*.txt'%(sdirp1,yearp1)

        if(dtgopt != None):
            admasks=[]
            dtgs=mf.dtg_dtgopt_prc(dtgopt)
            for dtg in dtgs:
                smask='%s/tracks.all.%s.txt'%(sdir,dtg)
                admasks.append(smask)

            dtgopt=None

        else:
            admasks=[smask]
            
    # -- adecks from tigge servers
    #
    elif(source == 'ecmwf' or source == 'ukmo'):
        sdir="%s/%s/%s"%(AdeckBaseDir,source,year)
        yearp1=int(year)+1
        yearp1=str(yearp1)
        sdirp1="%s/%s/%s"%(AdeckBaseDir,source,yearp1)
        if(int(year) >= 2007): 
            smask='%s/a????????.*'%(sdir)
            smaskp1='%s/a????????.*'%(sdirp1)
            admasks=[smask]
        else:
            smask='%s/wxmap/wxmap.????.%s??????.???'%(sdir,year)

    # -- adecks from ncep tigge server for ncep and cmc
    #
    elif(source == 'ncep_eps'):
        sdir="%s/ncep/%s/%s??????/"%(AdeckBaseDir,year,year)
        smaskc='%s/ac00*unix'%(sdir)
        smaskp='%s/ap??*unix'%(sdir)
        admasks=[smaskc,smaskp]

    elif(source == 'cmc_eps'):
        sdir="%s/cmc/%s/%s??????/"%(AdeckBaseDir,year,year)
        smaskc='%s/cc00*unix'%(sdir)
        smaskp='%s/cp??*unix'%(sdir)
        admasks=[smaskc,smaskp]

    # -- deprecated....................
    #
    #if(source == 'gfsenkf'):
        #sdir="%s/esrl/%s/%s"%(AdeckBaseDir,year,source)
        #smask="%s/track*%s*"%(sdir,year)

    #elif(source == 'local'):
        #sdir="%s/local/%s"%(AdeckBaseDir,year)
        #smask="%s/wxmap.*.%s*"%(sdir,year)

    #elif(source == 'wxmap2'):
        #sdir="%s/%s/%s"%(AdeckBaseDir,source,year)
        #smask="%s/w2.adeck.*.*.%s*"%(sdir,year)

    #elif(source == 'tacc'):
        #sdir="%s/esrl/%s"%(AdeckBaseDir,year)
        #smask='%s/tacc/track.%s*'%(sdir,year)

    #elif(source == 'w2flds'):
        #sdir="%s/esrl/%s/w2flds"%(AdeckBaseDir,year)
        #smask="%s/tctrk.atcf.??????????.*.txt"%(sdir)
        #admasks=[
            #"%s/tctrk.atcf.??????????.ecm2.txt"%(sdir),
            #"%s/tctrk.atcf.??????????.fim8.txt"%(sdir),
            #"%s/tctrk.atcf.??????????.gfs2.txt"%(sdir),
            #"%s/tctrk.atcf.??????????.ngp2.txt"%(sdir),
            #"%s/tctrk.atcf.??????????.ngpc.txt"%(sdir),
            #"%s/tctrk.atcf.??????????.ukm2.txt"%(sdir),
        #]

        #admasks=[smask]

    #elif(source == 'rtfim' or source == 'rtfimx' or source == 'rtfimy'):
    #    sdir="%s/esrl/%s"%(AdeckBaseDir,year)
    #    smask='%s/%s/track.%s*'%(sdir,source,year)

    if(admasks == None):
        admasks=[
            smask,
        ]

    adecks=[]
    for admask in admasks:
        adecks=adecks+glob.glob(admask)
        print 'AD.GetAdmaskAdecks.admask: ',admask

    oadecks=[]
    for adeck in adecks:
        try:
            siz=os.path.getsize(adeck)
            if(siz > 0 and tstmids == None and dtgopt == None): oadecks.append(adeck)
        except:
            continue

        if(dtgopt != None):
            dtgs=mf.dtg_dtgopt_prc(dtgopt,ddtg=6)

        if(tstmids != None):

            for tstmid in tstmids:
                (snum,b1id,year,b2id,stm2id,stm1id)=getStmParams(tstmid)
                s2id="%s%s"%(b2id.lower(),snum)
                s1id="%s%s"%(snum,b1id.lower())
                adl=adeck.lower()
                if( mf.find(adl,s2id) or mf.find(adl,s1id) ):
                    if(dtgopt != None):
                        for dtg in dtgs:
                            if(mf.find(adl,dtg)):
                                oadecks.append(adeck)
                            else:
                                continue
                    else:
                        oadecks.append(adeck)


    return(oadecks)


def GetAdeckAliases(source):

    aliases={}

    if(source == 'rtfim'): aliases['f8c']='fim8'
    if(source == 'rtfimx'): aliases['f8c']='f8cx'
    if(source == 'rtfimy'): aliases['f8c']='f8cy'
    if(source == 'rtfimz'): aliases['rtfi']='f8cz'
    if(source == 'tacc'): aliases['f9c']='fim9'

    if(source == 'local'):
        aliases['ncm2']='lcmc2'
        aliases['nec2']='lecm2'
        aliases['fim8']='lfim8'
        aliases['f8cy']='lfimy'
        aliases['ngf2']='lgfs2'
        aliases['nngc']='lngpc'
        aliases['nng2']='lngp2'
        aliases['nuk2']='lukm2'


    return(aliases)


def GetAdmaskAdeckGens(dtg,model,admasks=None):

    sdir="%s/dat/%s"%(W2fldsBaseDir,model)
    smask='%s/%s/tctrk/tcgen.sink.*.*txt'%(sdir,dtg)
    admask=smask

    if(admasks == None):
        admasks=[
            smask,
        ]

    adecks=[]
    for admask in admasks:
        adecks=adecks+glob.glob(admask)

    oadecks=[]
    for adeck in adecks:
        try:
            siz=os.path.getsize(adeck)
            if(siz > 0): oadecks.append(adeck)
        except:
            continue

    return(oadecks)



def MakeAdecksByYear(adps,year,aids=None,stmopt=None,
                     doadeckonly=0,adecktype='atcf',
                     skipcarq=1,fixmd2=0,
                     doplusrelabel=0,
                     aliases=None,verb=0,
                     yearMasks=None,
                     dofilt9x=0,
                     warn=1):

    """
    adecktype = atcf|gen to instantiate either Adeck of AdeckGen(Adeck) class
    using yearly mdeck Dss
    """
    from tcbase import TcDataBdir
    from tcVM import CurShemOverlap
    from adCL import Adeck
    
    # --- get mdecks
    #
    dsbdir="%s/DSs"%(TcDataBdir)
    dbname='mdecks'
    dbfile="%s.pypdb"%(dbname)
    DSs=DataSets(bdir=dsbdir,name=dbfile,dtype=dbname,verb=verb,doDSsWrite=1)
    try:
        mD=DSs.getDataSet(key=year).md
    except:
        print 'EEE(MakeAdecksByYear) no year: ',year,' mdeck; run mdk -y ',year
        sys.exit()

    # -- handle situation of next year's shem storms in the current year ( > 070100 and <= 121318 )
    #
    curdtg=mf.dtg()
    (shemoverlap,cyear,cyearp1)=CurShemOverlap(curdtg)
    cyearm1=str(int(cyear)-1)

    # -- if not current year...why????...becauseit used in A=Adeck below!
    #
    if(year < cyear):
        cyear=year
        cyearp1=str(int(year)+1)
        shemoverlap=1

    # -- 20140103 -- how to override when we're doing setYearMask in adk
    #
    if(yearMasks != None):
        cyear=yearMasks[0]
        cyearp1=yearMasks[1]
        shemoverlap=1

    mDp1=None
    if(shemoverlap):
        try:
            mDp1=DSs.getDataSet(key=cyearp1).md
        except:
            print 'EEE(MakeAdecksByYear) no cyearp1: ',cyearp1,' mdeck; run mdk -y ',cyearp1
            sys.exit()

    mdm1=None
    try:
        mDm1=DSs.getDataSet(key=cyearm1).md
    except:
        print 'EEE(MakeAdecksByYear) no cyearm1: ',cyearm1,' mdeck; run mdk -y ',cyearm1
        sys.exit()

    adpaths=adps.paths

    if(adecktype == 'atcf'):
        if(fixmd2):
            A=AdeckFixMd2(adpaths,mD,aliases=aliases,warn=0,skipcarq=skipcarq)
        else:
            A=Adeck(adpaths,mD,mDp1=mDp1,aliases=aliases,warn=0,skipcarq=skipcarq,
                    adyear=cyear,adyearp1=cyearp1,
                    dofilt9x=dofilt9x,
                    verb=verb)

        Baiddtgs=A.getAiddtgsFromAidcards()
        A.relabelAidcards()
        Aaiddtgs=A.getAiddtgsFromAidcards()
        A.cmpAiddtgs(Baiddtgs,Aaiddtgs)

    elif(adecktype == 'gen'):
        A=AdeckGen(adps,mD)


    ads={}
    kk=A.aidcards.keys()

    for k in kk:
        (aid,stm2id)=k

        ayear=stm2id.split('.')[1]

        if(ayear == cyear):
            imD=mD
        elif(ayear == cyearp1):
            imD=mDp1
        elif(ayear == cyearm1):
            imD=mDm1
        else:
            print 'EEE(MakeADecksByYear) no mD for ayear: ',ayear,' bailing...',stm2id,' not in cyear ',cyear,'cyearp1: ',cyearp1,' or cyearm1: ',cyearm1

            # -- real important to continue so as to not get bad years in oads returned
            continue
            #try:
                #imD=DSs.getDataSet(key=year).md
            #except:
                #print 'EEE(MakeAdecksByYear) going backward for year: ',year,' mdeck; run mdk -y ',year
                #sys.exit()

        # by pass carq ---
        #
        if(aid == 'carq' and skipcarq): continue

        acards=A.aidcards[k]

        # all multiply ads to com back from the acards
        #
        oads=makeAdeckByCards(imD,acards,aliases=aliases,skipcarq=skipcarq,
                              adyear=cyear,adyearp1=cyearp1,
                              doplusrelabel=doplusrelabel,verb=verb)
        for ad in oads:
            # -- skip if ad is None
            #
            if(ad == None):
                print 'WWW None ad for : ',k
                continue

            # -- put ad in ad dict
            #
            ackey="%s_%s"%(ad.aid,ad.stm1id)
            ads[ackey]=ad

    return(ads)




def makeAdeckByCards(mD,acards,stmopt=None,doadeckonly=0,adecktype='atcf',
                     skipcarq=1,do2stmids=0,doplusrelabel=0,
                     adyear=None,adyearp1=None,
                     dofilt9x=0,
                     aliases=None,verb=0,diag=0):

    """
    adecktype = atcf|gen to instantiate either Adeck of AdeckGen(Adeck) class
    using yearly mdeck Dss
    """

    from adCL import AdeckAcardsDtgHash
    from tcVM import getStmParams,stm2idTostm1id
    
    oads=[]
    ad=AdeckAcardsDtgHash(mD,acards,skipcarq=skipcarq,
                          adyear=adyear,adyearp1=adyearp1,
                          dofilt9x=dofilt9x,
                          verb=verb)

    if(len(ad.stm2ids) == 1):
        if(verb): print '111111111111111111 one stm2id in ad.stm2ids in AdeckAcardsDtgHash ',ad.stm2ids
        ad.stm2id=ad.stm2ids[0]
    elif(len(ad.stm2ids) == 2 and do2stmids):
        if(verb): print '222222222222222222 two stm2id in ad.stm2ids in AdeckAcardsDtgHash '
        ad.stm2id=ad.stm2ids[0]
    elif(len(ad.stm2ids) == 0):
        if(verb): print '000000000000000000  NO stm2id in ad.stm2ids in AdeckAcardsDtgHash '
        # 20120326 -- return oads to press
        #
        return(oads)
    else:
        if(diag): print 'WWW problem in makeAdeckByCards with more than one stm2ids in acards ad.stm2ids: ',ad.stm2ids,' diagnosing...'

        mdstm2ids=mD.stm1ids.keys()
        n9xstms=0
        nstms=len(ad.stm2ids)

        for stm2id in ad.stm2ids:
            snum=int(stm2id[2:4])
            if(snum >= 90 and snum <= 99): n9xstms=n9xstms+1
            if(stm2id in mdstm2ids):
                if(diag): print 'HHH stm2id: ',stm2id,' in mD.stm1ids.keys() '
                stm1id=mD.stm1ids[stm2id]
                kk=mD.bts[stm1id].keys()
                kk.sort()
                if(diag):
                    for k in kk:
                        btdic=mD.bts[stm1id][k][0]
                        print 'dtg: ',k,' bt: %5.1f %6.1f   %4.0f '%(btdic[0],btdic[1],btdic[2])

        if(nstms == n9xstms):
            if(diag): 
                print 'WWW multiple stm2ids are 9X storms nstms: ',nstms,' :: case of 9X tracker not properly synced real 9x storm'
                print 'WWW return empty dict... onward...'
            # 20120326 -- return oads to press
            #
            return(oads)
        else:
            if(diag):
                print 'EEEWWW--- because you need to understand what happened and define appopriate behaviour'
                print 'EEEWWW--- allow multiply realy storms in adeck, e.g., when gfdl runs in 9X -> real in both cpac/epac adecks at jtwc'
            #sys.exit()

    if(len(ad.aids) == 1):
        if(verb): print '111111111111111111 one    aid in    ad.aids in AdeckAcardsDtgHash'
        ad.aid=ad.aids[0]
    elif(len(ad.aids) == 2 and do2stmids):
        if(verb): print '222222222222222222 two    aid in    ad.aids in AdeckAcardsDtgHash go with first'
        ad.aid=ad.aids[0]
    else:
        print 'EEE problem in makeAdeckByCards with more than one aids in acards, sayoonnara'
        kk=acards.keys()
        kk.sort()
        for k in kk:
            for acard in acards[k]:
                print acard[:-1]

        sys.exit()


    for stm2id in ad.stm2ids:

        if(len(ad.stm2ids) > 1 and not(do2stmids)):
            ado=copy.copy(ad)
            # add - to end of aid name to indicate an 'extra'
            #
            if(doplusrelabel):
                ado.aid=ad.aids[0]+'+'
            else:
                ado.aid=ad.aids[0]
        else:
            ado=ad

        ado.stm2id=stm2id

        # -- redecorate with info from MD
        #
        
        try:    ado.stm1id=ado.mD.stm1ids[ado.stm2id]
        except:
            try:
                ado.stm1id=stm2idTostm1id(ado.stm2id)
            except:
                print 'oops in AD.py AAAA '
                for acard in acards:
                    print acard
                sys.exit()

        try:
            ado.stmname=ado.mD.stmnames[ado.stm2id]
        except:
            ado.stmname='undef'

        try:    ado.bts=ado.mD.bts[ado.stm1id]
        except: ado.bts=None

        atrks={}
        acards={}
        atkk=ado.aidtrks.keys()

        # -- check if relabeling worked, should only have one aid/storm
        #
        if(len(atkk) != 1):
            if(doplusrelabel): print 'EEEWWW--- relabeling failed in MakeAdecksByYear for aid: ',ad.aids[0],' so relabel aid to: ',ado.aid,' stm1id: ',ado.stm1id,ado.stm2id
            #print 'change atkk to pull trks by stm2ids atkk: ',atkk,' BBBBBBBBBBBBBefore'
            #ado.ls()
            atkk=[(ado.aids[0],ado.stm2id)]
            #print 'change atkk to pull trks by stm2ids atkk: ',atkk,' AAAAAAAAAAAAAfter'
            #sys.exit()

        for atk in atkk:
            dtgs=ado.aidtrks[atk].keys()
            dtgs.sort()
            for dtg in dtgs:
                trk=ado.aidtrks[atk][dtg]
                atrks[dtg]=trk

        # -- put atrks to ad object, del full tracks aidtrks
        #
        ado.ats=atrks

        atkk=ado.aidcards.keys()
        if(len(atkk) != 1):
            print 'EEEWWW--- relabeling failed in MakeAdecksByYear for aid: ',atkk,' stm2id: ',stm2id,' in aidcards, proceed anyway...'
            #sys.exit()

        for atk in atkk:
            dtgs=ado.aidcards[atk].keys()
            dtgs.sort()
            for dtg in dtgs:
                trk=ado.aidcards[atk][dtg]
                acards[dtg]=trk

        ado.acards=acards

        #ado.mD.ls()
        # -- lighten object, a lot by taking off mD

        del ado.mD
        del ado.aidtrks
        del ado.cards
        del ado.stm2ids,ado.stmdtgs,ado.verb,ado.warn,ado.aliases
        del ado.aiddtgs,ado.aids,ado.aidstms,ado.aidtaus
        del ado.taids,ado.naids,ado.ndtgs,ado.dtgopt,ado.dob2idchk
        del ado.aidcards

        oads.append(ado)

    return(oads)

def addAdeck2DataSets(ad,DSs,verb=1):

    # new form of output from makeAdeckByCards -- a list of ads not a single ad
    #

    if(len(ad) == 0):
        return
    if(len(ad) == 1):  ad=ad[0]

    ndskey="%s_%s"%(ad.aid,ad.stm1id)
    # keys
    #
    DSs.verb=verb
    dsk=DSs.getDataSet('keys')
    if(not(ndskey in dsk.data)):
        dsk.data.append(ndskey)
        dsk.data=MF.uniq(dsk.data)
        DSs.putDataSet(dsk,'keys')

    # adeck object
    #
    DSs.putDataSet(ad,ndskey)
    DSs.verb=0

    # adeck paths -- don't do if adding an ad not generated from adecks
    #
    #dsk=DataSet(name='adps',dtype='hash')
    #dsk.data=adps
    #DSs.putDataSet(dsk,'adps')



def makeAdeckGens(dtgopt,modelopt,basinopt,taids=None,verb=0):
    """ instantiate AdeckGen(Adeck) class"""
    A=AdeckGen(dtgopt,modelopt,basinopt,verb=verb)

    return(A)


def makeAdeckGensTctrk(tcD,dtgopt,modelopt,taids=None,verb=0):
    """ instantiate AdeckGenTctrk(AdeckGen) class"""
    A=AdeckGenTctrk(tcD,dtgopt,modelopt,verb=verb)

    # -- do map between adeck stmids and bt stmids
    #
    A.mapAidStmid2BtStmid()
    A.relabelAidtrks()
    return(A)



def PutDsDict2DataSets(dss,DSs):

    dskeyscurrent=DSs.getDataSet('keys')
    dskeys=dss.keys()
    if(dskeyscurrent != None):
        dskkc=dskeyscurrent.getData()
        dskeysc=dskeys+dskkc
    else:
        dskeysc=dskeys

    dskeysc=MF.uniq(dskeysc)

    # put data set keys
    #
    key='keys'
    dsk=DataSet(name=key,dtype='hash')
    dsk.data=dskeysc

    DSs.putDataSet(dsk,key)

    # put data sets
    #
    for dskey  in dskeys:
        ds=dss[dskey]
        DSs.putDataSet(ds,dskey)

def PutDsDictKeys2DataSets(dss,DSs):

    dskeyscurrent=DSs.getDataSet('keys')
    dskeys=dss.keys()
    if(dskeyscurrent != None):
        dskkc=dskeyscurrent.getData()
        dskeysc=dskeys+dskkc
    else:
        dskeysc=dskeys

    dskeysc=MF.uniq(dskeysc)

    # put data set keys
    #
    key='keys'
    dsk=DataSet(name=key,dtype='hash')
    dsk.data=dskeysc

    DSs.putDataSet(dsk,key)

# -- adeck V1 - 111111111111111111111111111111111111111111111111111111111111111
#

def PutAdecks2DataSets(ads,adps,source,dbtype='adeck',dsbdir=None,doclean=0,
                       setOutputYear=None,
                       verb=1):

    if(dsbdir == None):
        from tcbase import TcDataBdir
        dsbdir="%s/DSs"%(TcDataBdir)
    
    backup=0
    chkifopen=0

    # analyze keys
    #
    dskeys=ads.keys()

    DSsS={}
    dskeysS={}

    # -- get storm year from keys
    #
    for dskey in dskeys:
        year=dskey.split('.')[1]
        MF.loadDictList(dskeysS,year,dskey)

    years=dskeysS.keys()
    years=mf.uniq(years)

    if(setOutputYear != None):
        years=[setOutputYear]
        
    for year in years:

        # -- make DSs for each storm year
        #
        dbname="%s_%s_%s"%(dbtype,source,year)
        dbfile="%s.pypdb"%(dbname)
        DSs=DataSets(bdir=dsbdir,name=dbfile,dtype=dbtype,verb=verb,doDSsWrite=1,backup=backup,unlink=doclean,chkifopen=chkifopen)

        dsk=DataSet(name='dskeys',dtype='hash')
        dsk.data=dskeysS[year]
        DSs.putDataSet(dsk,'keys')

        # adeck objects by key: storm_year
        #
        for dskey  in dskeysS[year]:
            ds=ads[dskey]
            DSs.putDataSet(ds,dskey,verb=verb)

        # adeck paths -- avoid for doing phr bias corrs to original adecks
        #
        doAdpsPut=0
        if(adps == None):
            doAdpsPut=0
        elif(adps != None or (ListType(adps) and len(adps) > 0) ): doAdpsPut=1

        if(doAdpsPut):
            dsk=DataSet(name='adps',dtype='hash')
            dsk.data=adps
            DSs.putDataSet(dsk,'adps')

        # -- close it
        #
        DSs.closeDataSet()
        DSsS[year]=DSs

    return(DSsS)


#-- adeck V2 - 22222222222222222222222222222222222222222222222222222222222222222222222
#

def getAdecks2DataSets(source,years,dsbdir=None,
                       verb=0):

    dbtype=AD2dbname
    if(dsbdir == None):
        from tcbase import TcDataBdir
        dsbdir="%s/DSs"%(TcDataBdir)

    ad2s={}

    for year in years:

        # -- get DSs for each year
        #
        dbname="%s_%s_%s"%(dbtype,source,year)
        dbfile="%s.pypdb"%(dbname)
        DSs=DataSets(bdir=dsbdir,name=dbfile,dtype=dbtype,verb=verb,doDSsWrite=0)

        dskeys=DSs.getDataSet('keys').data

        for dskey in dskeys:
            ad2s[dskey]=DSs.getDataSet(dskey)
            
        DSs.closeDataSet()

    return(ad2s)


def getBdecks2DataSets(byears,
                       dsbdir=None,
                       verb=0,
                       warn=0):

    dbtype=BD2dbname
    
    if(dsbdir == None):
        from tcbase import TcDataBdir
        dsbdir="%s/DSs"%(TcDataBdir)

    bd2s={}
    rcs={}

    for byear in byears:
        rcs[byear]=1
        dbname="%s-%s"%(dbtype,byear)
        dbfile="%s.pypdb"%(dbname)
        DSs=DataSets(bdir=dsbdir,name=dbfile,dtype=dbtype,verb=verb,doDSsWrite=0)

        # -- case where bdeck2 is not there yet...
        #
        MF.sTimer('getBd2-keys')
        try:
            dskeys=DSs.getDataSet('keys').data
        except:
            dskeys=[]
        
        if(warn): MF.dTimer('getBd2-keys')
    
        MF.sTimer('getBd2-load-dskeys')
        
        dskeys=mf.uniq(dskeys)
        for dskey in dskeys:
            # -- filter out non byear keys -- why they're there????
            #
            dskeyYear=dskey.split('.')[-1]
            if(dskeyYear != byear): continue
            
            # -- getDataSet always does a return by using try:except
            #
            bd2=DSs.getDataSet(dskey,verb=verb,warn=0)
                
            if(bd2 != None):
                bd2s[dskey]=bd2
            else:
                if(warn):
                    print 'WWW(getBdecks2DataSets) bd2=None for dskey: ',dskey
                rcs[byear]=0
            
        DSs.closeDataSet()
        if(warn): MF.dTimer('getBd2-load-dskeys')
        
    rc=1
    for byear in rcs.keys():
        if(rcs[byear] == 0): rc=0
        
    return(bd2s,rc)


def getBasinsFromDskeys(dskeys):
    
    basins=[]
    dskeysB={}
    for dskey in dskeys:
        basin=getBasinFromDskey(dskey)
        MF.appendDictList(dskeysB, basin, dskey)
        basins.append(basin)
        
    basins=mf.uniq(basins)
    
    return(basins,dskeysB)
    
    
def getBasinFromDskey(dskey):
    tstmid=dskey.split('_')[1]
    (snum,b1id,year,b2id,stm2id,stm1id)=getStmParams(tstmid)
    basin=b2id.lower()
    if(basin == 'cp'): basin='ep'
    return(basin)



def getBasinsFromStmids(stmids):
    
    istmids=stmids
    if(not(type(stmids) is ListType)): istmids=[stmids]
    basins=[]
    dskeysB={}
    for stmid in istmids:
        basin=getBasinFromStmid(stmid)
        basins.append(basin)
        
    basins=mf.uniq(basins)
    
    return(basins)
    
    
def getBasinFromStmid(stmid):
    (snum,b1id,year,b2id,stm2id,stm1id)=getStmParams(stmid)
    basin=b2id.lower()
    if(basin == 'cp'): basin='ep'
    return(basin)    


def getBasinDbtypesFromStmids(stmids):
    basin_dbtypes={}
    for stmid in stmids:
        dbtype=getDbtypeFromStmid(stmid)
        basin=getBasinFromStmid(stmid)
        basin_dbtypes[stmid]=(basin,dbtype)
        
    return(basin_dbtypes)


def getDbtypeFromStmid(stmid):
    dbtype=AD2dbname
    if(Is9X(stmid)): dbtype="%s-9X"%(AD2dbname)
    return(dbtype)
    

def putAdeck2sDataSets(ads,dbtype=None,dsbdir=None,doclean=0,
                       verb=1):

    if(dbtype == None):  dbtype=AD2dbname
    
    if(dsbdir == None):
        from tcbase import TcDataBdir
        dsbdir="%s/DSs"%(TcDataBdir)
    
    # analyze keys
    #
    dskeys=ads.keys()
    
    
    DSsS={}
    dskeysS={}

    # -- get storm year from keys
    #
    for dskey in dskeys:
        year=dskey.split('.')[1]
        MF.loadDictList(dskeysS,year,dskey)

    years=dskeysS.keys()
    years=mf.uniq(years)
    obasins=[]
    for year in years:
        
        dskeys=dskeysS[year]
        (basins,dskeysBasin)=getBasinsFromDskeys(dskeys)
        obasins=obasins+basins
        for basin in basins:
            
            # -- make DSs for each storm year
            #
            dbname="%s-%s-%s"%(dbtype,basin,year)
            dbfile="%s.pypdb"%(dbname)
            
            DSs=DataSets(bdir=dsbdir,name=dbfile,dtype=dbtype,verb=verb,doDSsWrite=1,unlink=doclean)
            
            try:
                dskCur=DSs.db['keys'].getData()
            except:
                dskCur=[]
                
            dskCur.sort()
            dskCur=dskCur+dskeysBasin[basin]
    
            dsk=DataSet(name='dskeys',dtype='hash')
            dsk.data=dskCur
            DSs.putDataSet(dsk,'keys')
    
            # adeck objects by key: storm_year
            #
            nkeys=len(dskeysBasin[basin])
            MF.sTimer('PUT N(%-6d) basin: %s year: %s ds'%(nkeys,basin,year))
            for dskey  in dskeysBasin[basin]:
                ds=ads[dskey]
                DSs.putDataSet(ds,dskey,verb=verb)
            MF.dTimer('PUT N(%-6d) basin: %s year: %s ds'%(nkeys,basin,year))
    
            # -- close it
            #
            MF.sTimer('closeDS')
            DSs.closeDataSet()
            DSsS[basin,year]=DSs
            MF.dTimer('closeDS')

    obasins=mf.uniq(obasins)
    return(DSsS,obasins)

def putBdeck2sDataSets(bds,dbtype=None,dsbdir=None,doclean=0,
                       verb=1):
    
    if(dbtype == None): dbtype=BD2dbname

    if(dsbdir == None):
        from tcbase import TcDataBdir
        dsbdir="%s/DSs"%(TcDataBdir)
    
    backup=0
    chkifopen=0

    # analyze keys
    #
    dskeys=bds.keys()
    dskeys=mf.uniq(dskeys)
    
    dskeysS={}
    
    for dskey in dskeys:
        (snum,b1id,stmyear,b2id,stm2id,stm1id)=getStmParams(dskey)
        MF.appendDictList(dskeysS,stmyear,dskey)
        
        
    byears=getYearsFromStmids(dskeys)
    
    DSsS={}

    for byear in byears:
        
        # -- make DSs for each storm year
        #
        dbname="%s-%s"%(dbtype,byear)
        dbfile="%s.pypdb"%(dbname)
        DSs=DataSets(bdir=dsbdir,name=dbfile,dtype=dbtype,verb=verb,doDSsWrite=1,unlink=doclean)
        
        try:
            dskCur=DSs.db['keys'].getData()
        except:
            dskCur=[]
        
        dskCur.sort()
        dskCur=mf.uniq(dskCur)
        dskCur=dskCur+dskeys

        dsk=DataSet(name='dskeys',dtype='hash')
        dsk.data=dskCur
        DSs.putDataSet(dsk,'keys')

        # put individual bdeck2 by key: storm
        #
        for dskey  in dskeysS[byear]:
            try:
                ds=bds[dskey]
                DSs.putDataSet(ds,dskey,verb=verb)
            except:
                print 'WWW no bds for dskey: ',dskey,' in putBdeck2sDataSet'
                continue

        # -- close it
        #
        DSs.closeDataSet()
        DSsS[byear]=DSs

    return(DSsS)


def getBcon4Stmid(stmid):

    b1id=stmid[2]
    syear=int(stmid.split('.')[1])

    if(IsNhcBasin(b1id)):
        if(syear >= 2008):
            bconaid='tvcn'
        else:
            bconaid='conu'

    if(IsJtwcBasin(b1id)):
        bconaid='conw'

    return(bconaid)



def GetAidsStormsFromDss(DSs,taids=None,tstms=None,dofilt9x=0,warn=0):

    aids=[]
    stms=[]
    try:
        dskeys=DSs.db['keys'].getData()
        dskeys.sort()
    except:
        if(warn): print 'WWW(AD.GetAidsStormsFromDss()) DSs is None -- return empty lists -- DSs.name:',DSs.name
        return(aids,stms)

    if(taids != None and type(taids) != ListType): taids=[taids]
    if(tstms != None and type(tstms) != ListType): tstms=[tstms]

    doaid=0
    dostm=0
    for dskey in dskeys:

        aid=dskey.split('_')[0]
        stm=dskey.split('_')[1]

        if(stm[0].isalpha()):
            stmnum=90+int(stm[1])
        else:
            stmnum=int(stm[0:2])
            
        if(dofilt9x and (stmnum >= 90 and stmnum <= 99)): dostm=0

        if(tstms != None):
            dostm=0
            for tstm in tstms:
                if(mf.find(stm,tstm.upper())):
                    dostm=1
                if(dofilt9x and (stmnum >= 90 and stmnum <= 99)): dostm=0
                #print 'dddddddddddd ',dskey,stm,tstm.upper(),mf.find(stm,tstm.upper()),stmnum,dostm
        else:
            stms.append(stm)

        if(taids != None):
            doaid=0
            for taid in taids:

                if(aid == taid.lower()): 
                    doaid=1

        else:
            aids.append(aid)

        test1=(doaid and taids != None and dostm and tstms != None)
        test2=(doaid and taids != None and tstms == None)
        test3=(dostm and tstms != None and taids == None)

        if(test1):
            aids.append(aid)
            stms.append(stm)

        elif(test2):
            aids.append(aid)
            stms.append(stm)

        elif(test3): 
            aids.append(aid)
            stms.append(stm)

    aids=MF.uniq(aids)
    stms=MF.uniq(stms)

    aids.sort()
    stms.sort()

    return(aids,stms)


def GetAidsStormsFromDsss(DSss,taids=None,tstms=None,dofilt9x=0):

    aids=[]
    stms=[]

    years=DSss.keys()

    for year in years:

        DSs=DSss[year]
        (yaids,ystms)=GetAidsStormsFromDss(DSs)
        aids=aids+yaids
        stms=stms+ystms

    return(aids,stms)


def LsAidsStormsDss(DSs,tstms=None,taids=None,dofilt9x=0,lsopt='s',
                    dtgopt=None,printZeros=1,
                    warn=0,
                    verb=0):

    from ATCF import aidDescTechList
    ad=aidDescTechList()
    dssName=DSs.name    

    dtgs=None
    if(dtgopt != None):
        dtgs=mf.dtg_dtgopt_prc(dtgopt)
    
    if(dtgs != None and tstms == None):
        print 'adVM.LsAidsStormsDss dtgs != None and tstms == None -- does not work...sayoonara...'
        sys.exit()

        ##from tcCL import TcData
        ##dtg=dtgs[-1]
        ##tD=TcData(dtgopt=dtg)
        ## -- use same method as in TCvitals
        ##
        ##tstms=tD.getDSsDtg(dtg)

        ### -- don't need this if using getDSsDtg
        ### -- convert 2-char basin id to subbasin
        ###
        ##tstmids=[]
        ##for tstm in tstms:
            ##stmid=tD.getSubbasinStmid(tstm)
            ##tstmids.append(stmid)

        ##tstms=tstmids

    aids={}
    stms=[]

    try:
        dskeys=DSs.db['keys'].getData()
        dskeys.sort()
    except:
        print 'WWW(LsAidsSTormsDss) -- no keys in DSs:',DSs.path,'for tstms: ',tstms
        return(aids,stms)

    ## -- convert A[0-9] to 9X -- don't need for adeck2
    ##
    #otstms=[]
    #for tstm in tstms:
        #(snum,b1id,year,b2id,stm2id,stm1id)=getStmParams(tstm,convert9x=1)
        #otstms.append(stm1id)
    
    allStms=[]
    for dskey in dskeys:

        aid=dskey.split('_')[0]
        stm=dskey.split('_')[1]
        allStms.append(stm)
        
        (snum,b1id,year,b2id,stm2id,stm1id)=getStmParams(stm,convert9x=1)

        if(dofilt9x and (snum >= 90 and snum <= 99) ): continue

        doaid=1
        dostm=1
        stmnum=snum

        if(dofilt9x and (stmnum >= 90 and stmnum <= 99)): dostm=0

        if(tstms != None):
            dostm=0
            if(type(tstms) != ListType): tstms=[tstms]
            for tstm in tstms:
                if(mf.find(stm,tstm.upper())): dostm=1
                if(dofilt9x and (stmnum >= 90 and stmnum <= 99)): dostm=0

        if(taids != None):
            doaid=0
            if(type(taids) != ListType): taids=[taids]
            for taid in taids:
                if(mf.find(aid,taid.lower())): doaid=1

        if(doaid): MF.loadDictList(aids,stm,aid)
        if(dostm): stms.append(stm)

    allStms=MF.uniq(allStms)
    stms=MF.uniq(stms)
    
    MF.uniqDictList(aids)

    # -- find intersection of allStms from DSs and tstms
    #
    interList=list(set(allStms) & set(tstms))
    
    if(len(stms) == 0):
        if(warn): print 'WWW(AD.LsAidsStormsDss) no storms in: ',dssName,' for tstms: ',tstms
        return(aids,stms)

    kk=aids.keys()
    kk.sort()

    for stm in stms:
        try:       aa=aids[stm]
        except:    continue

        aa.sort()
        lsext=''
        if(lsopt == 's'):
            nstrlen=128
            if(len(str(aa)) > nstrlen): lsext='...'
            card='stmid: %s'%(stm)+' aids: %s %s'%(str(aa)[0:nstrlen],lsext)
            print card

        if(lsopt == 'l'):
            nstrlen=-1
            lsext=''
            card='stmid: %s'%(stm)+' aids:'
            for n in range(0,len(aa)):
                card="%s %5s"%(card,aa[n])
                if(n%20 == 0 and n > 0): card="%s %s"%(card,aa[n])+'\n'
            #if(dtgopt != None): print card


    if(lsopt != 'f' and lsopt != 'l' and dtgopt == None):
        return(aids,stms)

    idtgs=None
    if(dtgopt != None):
        idtgs=mf.dtg_dtgopt_prc(dtgopt)
        if(verb): print 'Searching for dtgs: ',idtgs
        printZeros=0


    # -- new form of output, aid,stm,dtgs
    #
    for stm in stms:
        try:       oaids=aids[stm]
        except:    continue
        for aid in oaids:
            #aP=Aid(aid)
            dskey="%s_%s"%(aid,stm)
            
            DSs.verb=0
            aD=DSs.getDataSet(dskey)
            #aD.ls()
            #aD.AT.ls()
            #aD.mD2.ls()
            #print 'aaaaaaaaaaaaaaaaaaa--------------aid',aid,dskey,aD
            
            if(aD == None): continue

            if(aD.__module__ == 'VD' or aD.__module__ == 'vdCL'):

                bdtgs=aD.bdtg[0]
                vflags=aD.vflag[0]

                gotlong=0
                if(hasattr(aD,'vdecktype')):
                    if(aD.vdecktype == 'long'):
                        warns=aD.warnYN[0]
                        fcruns=aD.fcrunYN[0]
                        tflags=aD.tcYN[0]
                        gotlong=1

                for n in range(0,len(bdtgs)):
                    bdtg=bdtgs[n]
                    hh=bdtg[8:10]
                    if(gotlong):
                        warn=warns[n]
                        vflag=vflags[n]
                        fcrun=fcruns[n]
                        tcflg=tflags[n]
                        print bdtg,hh,warn,vflag,fcrun,tcflg
                dtgs=bdtgs
                odtgs=dtgs

            else:

                # -- find dtgs with longest, because of bug in updateAds of not setting nad.dtgs=
                #
                dtgs1=aD.dtgs
                if(hasattr(aD,'ats') and aD.ats != None):
                    dtgs2=aD.ats.keys() 
                elif(hasattr(aD,'AT')):
                    dtgs2=aD.AT.dtgs
                    
                dtgs=dtgs1
                if(len(dtgs2) >= len(dtgs1)): 
                    dtgs=dtgs2
                    odtgs=[]
                    cdtgs=idtgs
                    if(idtgs == None): cdtgs=dtgs
                    for dtg in dtgs:
                        if(dtg in cdtgs): odtgs.append(dtg)
                else:
                    odtgs=dtgs

                # -- print the adeck cards
                #
                if(lsopt == 'f'):
                    aD.lsAidcards(dtgopt=dtgopt)

            odtgs.sort()

            doprint=1
            if(not(printZeros) and len(odtgs) == 0): doprint=0
            if(printZeros): doprint=1


            if(doprint):  
                descA=ad.getAidDesc(aid)
                card='%8s'%(aid)+" :: %-60s"%(descA[0:60])+' :: stm: %s  '%(stm)+MF.makeDtgsString(odtgs)
                print card



    return(aids,stms)

    
def getAD2StatusByAidDtg(dtgopt,taid,
                         warn=0,
                         verb=0):

    from ATCF import aidDescTechList
    ad=aidDescTechList()
    
    stmopt=None
    dtgs=mf.dtg_dtgopt_prc(dtgopt)
    
    dbtype=None
    dsbdir=None
    taids=[taid]
    model=None
    (tstmids,tD,tstmids9Xall)=getTstmidsAD2FromStmoptDtgopt(stmopt,dtgopt)
    
    rc=0
    for dtg in dtgs:
        for tstmid in tstmids:
            (ATs,BT,nadecks)=getModelAD2s(dtg,tstmid,taids,model)
            if(rc == 0 and nadecks > 0): rc=1
            if(verb): print 'tttttttt',dtg,tstmid,nadecks
        
    return(rc)
        



def MakeAdeckCards(model,dtg,trk,stmid,ttaus=None,doString=0,verb=0):


    taus=trk.keys()
    taus.sort()

    stmid=stmid.upper()
    from ATCF import Aid
    AA=Aid(model)

    stmnum=stmid[0:2]
    basin1=stmid[2:3]
    basin2=Basin1toBasin2[basin1]
    adeckname=AA.AdeckName
    adecknum=AA.AdeckNum

    # use model name for adeckname AA return generic model name
    #
    adeckname=model.upper()

    acards=[]
    acardsString=''

    for tau in taus:

        if(ttaus != None and not(tau in ttaus)): continue
        
        itau=int(tau)

        vmax=-99
        pmin=0
        r34quad=None
        r50quad=None
        r64quad=None

        extra=None
        tt=trk[tau]
        for i in range(0,len(tt)):
            if(i == 0): lat=tt[i]
            if(i == 1): lon=tt[i]
            if(i == 2): vmax=tt[i]
            if(i == 3): pmin=tt[i]
            if(i == 4): r34quad=tt[i]
            if(i == 5): r50quad=tt[i]
            if(i == 6): r60quad=tt[i]
            if(i == 7): extra=tt[i]


        if(lat < -88.0 or lat > 88.0): continue

        ivmax=int(vmax)
        try:
            ipmin=int(pmin)
        except:
            ipmin=0

        if(ipmin < 0): ipmin=0

        (clat,clon,ilat,ilon,hemns,hemew)=Rlatlon2ClatlonFull(lat,lon)

        try:
            (r34ne,r34se,r34sw,r34nw)=r34quad
        except:
            r34ne=r34se=r34sw=r34nw=0

        try:
            (r50ne,r50se,r50sw,r50nw)=r50quad
            gotr50=1
        except:
            r50ne=r50se=r50sw=r50nw=0
            gotr50=0

        try:
            (r64ne,r64se,r64sw,r64nw)=r64quad
            gotr64=1
        except:
            r64ne=r64se=r64sw=r64nw=0
            gotr64=0

        acard1=''
        acard2=''
        acard3=''

        acard0="%2s, %2s, %10s, %2s, %4s, %3d,"%(basin2,stmnum,dtg,adecknum,adeckname,itau)

        if(extra == None):
            oextra=''
        else:
            oextra=" PMBR, %4d,"%(int(extra))

        # add \n at end of card to be consistent with real adecks
        #
        acard1=acard0+" %3d%1s, %4d%1s, %3d, %4d,   ,  34, NEQ, %4d, %4d, %4d, %4d,%s\n"%\
            (ilat,hemns,ilon,hemew,ivmax,ipmin,r34ne,r34se,r34sw,r34nw,oextra)

        if(verb): print acard1[0:-1]
        acards.append(acard1)
        
        if(doString): acardsString=acardsString+acard1

        if(gotr50):
            acard2=acard0+" %3d%1s, %4d%1s, %3d, %4d,   ,  50, NEQ, %4d, %4d, %4d, %4d,\n"%\
                (ilat,hemns,ilon,hemew,ivmax,ipmin,r50ne,r50se,r50sw,r50nw)
            acards.append(acard2)
            if(doString): acardsString=acardsString+acard2


        if(gotr64):
            acard3=acard0+" %3d%1s, %4d%1s, %3d, %4d,   ,  64, NEQ, %4d, %4d, %4d, %4d,\n"%\
                (ilat,hemns,ilon,hemew,ivmax,ipmin,r64ne,r64se,r64sw,r64nw)
            acards.append(acard3)
            if(doString): acardsString=acardsString+acard3

    if(doString): acards=acardsString

    return(acards)




def AcardsFromAds(aDSs,taids,tstms,dtgopt=None,tdir='/ptmp',dowrite=0,tag=None,aliases=None,dohfip=0,hfipver=None,
                  dofilt9x=1,override=0,
                  verb=0):


    tdtgs=None
    if(dtgopt != None):
        tdtgs=mf.dtg_dtgopt_prc(dtgopt)

    (taids,tstms)=GetAidsStormsFromDss(aDSs,taids=taids,tstms=tstms,dofilt9x=dofilt9x)

    def corrVmaxPmin(card):

        tt=card.split(',')
        vmax=tt[8]
        pmin=tt[9]

        if(vmax == ' ***'): tt[8]='    '
        if(pmin == '  -99'): tt[9]='     '

        ocard=''
        for n in range(0,len(tt)):
            t1=tt[n]
            if(n == len(tt)-1):
                ocard="%s%s"%(ocard,t1)
            else:
                ocard="%s%s,"%(ocard,t1)

        return(ocard)



    if(hfipver != None): fimver=hfipver

    for tstm in tstms:

        if(tag != None):  cards=[]

        for taid in taids:
            adkey="%s_%s"%(taid,tstm)

            otaid=taid
            if(aliases != None):
                for (iname,oname) in aliases:
                    print taid.upper(),iname.upper(),otaid,oname
                    if(taid.upper() == iname.upper()): otaid=oname.upper()



            try:
                ad=aDSs.getDataSet(adkey)
            except:
                print 'no adeck for taid: ',taid,' tstm: ',tstm
                continue

            if(ad == None): continue

            if(tag == None):
                cards=[]

            dtgs=ad.acards.keys()
            dtgs.sort()
            for dtg in dtgs:

                if(tdtgs != None and not(dtg in tdtgs)): continue

                if(dohfip): cards=[]
                acds=ad.acards[dtg]
                for acd in acds:

                    acd=corrVmaxPmin(acd)
                    # the b2id in the adeck card is NOT changed, just the stm2id
                    # do the conversion here
                    #
                    b2id=acd[0:2]
                    b2id=basin2Chk(b2id)
                    acd=b2id+acd[2:]
                    if(aliases != None):
                        acd=acd.replace(taid.upper(),otaid.upper())
                    if(verb): print acd[0:-1]
                    cards.append(acd)

                if(dohfip):
                    hfiptype='d' # for ops
                    hfiptype='h' # for retro
                    fpath="%s/a%s_%s_%s%s_%s.dat"%(tdir,ad.stm2id.replace('.',''),otaid.upper(),hfiptype,fimver,dtg)
                    if(MF.ChkPath(fpath,verb=0) == 0 or override):
                        print 'MMMaking: ',fpath
                        ad.WriteList2File(cards,fpath,verb=verb)
                    else:
                        print 'DDDone: ',fpath


            if(tag == None and not(dohfip)):
                fpath="%s/a%s_%s.dat"%(tdir,ad.stm2id.replace('.',''),otaid.lower())
                ad.WriteList2File(cards,fpath,verb=1)

        if(tag != None and not(dohfip)):
            fpath="%s/a%s_%s.dat"%(tdir,ad.stm2id.replace('.',''),tag)
            ad.WriteList2File(cards,fpath,verb=1)


def GetAidBestTrksFromDss(DSs,taid,stmid,verb=1,warn=1):
    """ get single aid/best trks for taid and tstmid"""

    tstmid=stmid.upper()

    AT=None
    BT=None

    dskey="%s_%s"%(taid,tstmid)
    
    try:
        aD=DSs.db[dskey]
        if(verb): print 'III(GetAidBestTrksFromDss) -- got adecks for: ',dskey
    except:
        if(warn): print 'WWW(GetAidBestTrksFromDss) -- NO adecks for: ',dskey
        return(None,None,None)

    aD.taid=taid
    aD.tstmid=tstmid
    if(hasattr(aD,'AT')):
        AT=aD.AT
    else:
        AT=aD.getAidTrk()
    
    if(hasattr(aD,'BT')):
        BT=aD.BT
    else:
        BT=aD.getBestTrk()
        
    return(AT,BT,aD)

def getAidAdeck2Bdeck2FromDss(DSs,bd2s,taid,tstmid,verb=1,warn=1):
    """ get single aid/best trks for taid and tstmid
from DSs.Adeck2 and bd2s of Bdeck2
"""
    
    AT=None
    # -- SHEM handling
    #
    if(isShemBasinStm(tstmid)):
        
        got1=got2=0
        
        # -- look for storms starting in on one side and going to the other...
        #
        (snum,b1id,byear,b2id,stm2id,stm1id)=getStmParams(tstmid)
        dskey1="%s_%s"%(taid,tstmid.upper())
        if(b1id.upper() == 'S'): b1id2='P'
        if(b1id.upper() == 'P'): b1id2='S'
        tstmid2="%s%s.%s"%(tstmid[0:2],b1id2,byear)
        dskey2="%s_%s"%(taid,tstmid2.upper())
        try:
            aD1=DSs.db[dskey1]
            got1=1
        except:
            got1=0
            
        if(got1 == 0):
            try:
                aD2=DSs.db[dskey2]
                got2=1
            except:
                got2=0
                
        if(got1):
            dskey=dskey1
            print 'SHEM-11111 storm: ',tstmid,' got tracker for dskey: ',dskey1
            
        elif(got2): 
            dskey=dskey2
            tstmid=tstmid2
            print 'SHEM-22222 storm: ',tstmid,' got tracker for dskey: ',dskey2
            
        else:
            dskey="%s_%s"%(taid,tstmid.upper())
    
    # -- 20210329 -- IO handling        
    #
    if(isIOBasinStm(tstmid)):
        
        got1=got2=0
        
        # -- look for storms starting in on one side and going to the other...
        #
        (snum,b1id,byear,b2id,stm2id,stm1id)=getStmParams(tstmid)

        tstmid1=tstmid
        dskey1="%s_%s"%(taid,tstmid.upper())

        if(b1id.upper() == 'A'): b1id2='B'
        if(b1id.upper() == 'B'): b1id2='A'
        gotIstm=0
        if(b1id.upper() == 'I'):
            b1id2='B'
            b1id='A'
            tstmid1="%s%s.%s"%(tstmid[0:2],b1id,byear)
            dskey1="%s_%s"%(taid,tstmid1.upper())
            gotIstm=1
        
        tstmid2="%s%s.%s"%(tstmid[0:2],b1id2,byear)
        dskey2="%s_%s"%(taid,tstmid2.upper())
        try:
            aD1=DSs.db[dskey1]
            got1=1
        except:
            got1=0
            
        if(got1 == 0):
            try:
                aD2=DSs.db[dskey2]
                got2=1
            except:
                got2=0
                
        if(got1):
            dskey=dskey1
            if(not(gotIstm)): tstmid=tstmid1
            print 'IO-11111 storm: ',tstmid,' got tracker for dskey: ',dskey1
            
        elif(got2): 
            dskey=dskey2
            if(not(gotIstm)): tstmid=tstmid2
            print 'IO-22222 storm: ',tstmid,' got tracker for dskey: ',dskey2
            
        else:
            dskey="%s_%s"%(taid,tstmid.upper())
    else:
        tstmid2=tstmid
        dskey="%s_%s"%(taid,tstmid.upper())
    
    
    try:
        aD=DSs.db[dskey]
        if(verb): print 'III(getAidAdeck2Bdeck2FromDss) -- got adecks for: ',dskey,DSs.name
    except:
        if(warn): print 'WWW(getAidAdeck2Bdeck2FromDss) -- NO adecks for: ',dskey,DSs.name
        return(None,None,None)

    aD.taid=taid
    aD.tstmid=tstmid
    if(hasattr(aD,'AT')):
        AT=aD.AT
    else:
        AT=aD.getAidTrk()
        
    try:
        bD2=bd2s[tstmid.upper()]
        BT=bD2.BT
    except:
        print 'WWW no bd2 for tstmid: ',tstmid,' try 2nd tsmids2....'

        try:
            bD2=bd2s[tstmid2.upper()]
            BT=bD2.BT
        except:
            print 'EEE no bd2 for tstmid2: ',tstmid2,' set BT=None and continue....'
            BT=None
            #sys.exit()

    
    return(AT,BT,aD)



def GetStm2idFromAdeck(ad,stmid,verb=1):

    for stm2id in ad.stm2ids:
        stm1id=stm2idTostm1id(stm2id)
        if(verb): print 'adVM.GetStm2idFromAdeck: stm2id: ',stm2id,' stm1id: ',stm1id,' STMID: ',stmid
        if(stmid == stm1id):
            return(stm2id)

    return(None)




def getAdssFromDss(sources,tstmid,taid,dbtype='adeck',verb=0):

    from vdVM import GetVdsFromDSs
    from tcbase import TcDataBdir

    if( type(sources) is not(ListType) ):
        sources=[sources]

    aDSs={}

    year=tstmid.split('.')[1]
    dsbdir="%s/DSs"%(TcDataBdir)

    for source in sources:

        dbname="%s_%s_%s"%(dbtype,source,year)
        dbfile="%s.pypdb"%(dbname)
        aDS=DataSets(bdir=dsbdir,name=dbfile,dtype=dbtype,verb=verb)

        if(verb):   print 'III(AD.getAdssFromDss) trying to get taid, tstmid: ',taid,tstmid
        aDSs[source]=GetVdsFromDSs(aDS,taid,tstmid,donone=1,returnlist=1,verb=verb)

        tstmids=[tstmid]
        taids=[taid]


    return(aDSs)


def getCarqFromDss(tstmid,verb=0):

    from vdVM import GetVdsFromDSs
    from tcbase import TcDataBdir

    dbtype='adeck'
    source='carq'
    taid='carq'

    year=tstmid.split('.')[1]
    dsbdir="%s/DSs"%(TcDataBdir)

    dbname="%s_%s_%s"%(dbtype,source,year)
    dbfile="%s.pypdb"%(dbname)
    aDSs=DataSets(bdir=dsbdir,name=dbfile,dtype=dbtype,verb=verb)

    if(verb):   print 'III(AD.getCarqFromDss) trying to get taid, tstmid: ',taid,tstmid,'dbname: ',dbname
    aDcarq=GetVdsFromDSs(aDSs,taid,tstmid,donone=1,returnlist=1)

    return(aDcarq)


def getAdsFromDss(source,tstmid=None,taid=None,verb=0):

    from tcbase import TcDataBdir
    dbtype='adeck'
    aDSs={}

    year=tstmid.split('.')[1]
    dsbdir="%s/DSs"%(TcDataBdir)

    dbname="%s_%s_%s"%(dbtype,source,year)
    dbfile="%s.pypdb"%(dbname)

    aDS=DataSets(bdir=dsbdir,name=dbfile,dtype=dbtype,verb=verb)


    return(aDS)


def getYearsFromStmids(stmids):

    years=[]
    if(type(stmids) != ListType): stmids=[stmids]
    
    for stmid in stmids:
        year=getYearFromStmid(stmid)
        years.append(year)

    years=mf.uniq(years)

    return(years)

def getYearFromStmid(stmid):
    (snum,b1id,year,b2id,tstm2id,stm1id)=getStmParams(stmid)
    return(year)



def getAtcfABdeckFromStmid(stmid,dtype):

    adeckName=None
    (snum,b1id,year,b2id,tstm2id,stm1id)=getStmParams(stmid)
    
    if(dtype.lower() == 'a'):
        adeckName='a%s%s%s.dat'%(b2id.lower(),snum.upper(),year)
        
    elif(dtype.lower() == 'b'):
        adeckName='b%s%s%s.dat'%(b2id.lower(),snum.upper(),year)
    
    else:
        print """""EEE(adVM.getAtcfABdeckFromStmid) dtype != 'a' or 'b' - sayoonara """
        sys.exit()
        
    
    return(adeckName,year)
    
def getAdeck2Bdeck2DSs(tstmids,dbtype=None,dsbdir=None,
                 verb=0,quiet=1):

    do9Xonly=0
    if(areStmids9X(tstmids)): do9Xonly=1    
    if(dbtype == None):  dbtype=AD2dbname
    
    if(dsbdir == None):
        from tcbase import TcDataBdir
        dsbdir="%s/DSs"%(TcDataBdir)
        
    if(do9Xonly):  dbtype='%s-9X'%(AD2dbname)
    
        
    # -- OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO - open DSs file
    #
    DSss={}
    dbnames={}
    byears=getYearsFromStmids(tstmids)
    basins=getBasinsFromStmids(tstmids)

    # -- only use first year for listing
    #
    for byear in byears:
        for basin in basins:
            if(not(quiet)): MF.sTimer('ad2-openDss-dolisting-doacardout-basin-year:%s-%s'%(basin,byear))
            dbname="%s-%s-%s"%(dbtype,basin,byear)
            dbfile="%s.pypdb"%(dbname)
            DSs=DataSets(bdir=dsbdir,name=dbfile,dtype=dbtype)
            DSss[basin,byear]=DSs
            dbnames[basin,byear]=dbname
            if(not(quiet)): MF.dTimer('ad2-openDss-dolisting-doacardout-basin-year:%s-%s'%(basin,byear))
    
    (bd2s,rcbd2s)=getBdecks2DataSets(byears,dsbdir=dsbdir,verb=verb)

    return(DSss,bd2s,dbnames,basins,byears)

def getModelAD2s(dtg,stmid,taids,verb=0):

    (DSss,bd2s)=getAdeck2Bdeck2DSsByStmids(stmid,verb=verb)
    DSs=DSss[stmid]

    if(type(taids) is not(ListType)):
        taids=[taids]
    nadecks=0
    ATs={}
    oBT=None
    for aid in taids:
        (AT,BT,aD)=getAidAdeck2Bdeck2FromDss(DSs,bd2s,aid,stmid,verb=verb,warn=1)
        if(BT != None and oBT == None): oBT=BT
        if(AT != None and dtg in AT.dtgs):
            ATs[aid]=AT.atrks[dtg]
            nadecks=nadecks+1
        else:
            ATs[aid]=None
    
    return(ATs,oBT,nadecks)

def getAdeck2Bdeck2DSsByStmids(tstmids,dsbdir=None,
                               verb=0):
    
    if(type(tstmids) is not(ListType)):
        tstmids=[tstmids]

    if(dsbdir == None):
        from tcbase import TcDataBdir
        dsbdir="%s/DSs"%(TcDataBdir)
    
    # -- OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO - open DSs file
    #
    DSss={}
    dbnames={}
    byears=getYearsFromStmids(tstmids)

    # -- only use first year for listing
    #
    for tstmid in tstmids:
        
        basin=getBasinFromStmid(tstmid)
        byear=getYearFromStmid(tstmid)
        dbtype=getDbtypeFromStmid(tstmid)
        
        MF.sTimer('ad2-openDss tstmid: %s basin: %s year: %s dbtype: %s'%(tstmid,basin,byear,dbtype))
        dbname="%s-%s-%s"%(dbtype,basin,byear)
        dbfile="%s.pypdb"%(dbname)
        DSs=DataSets(bdir=dsbdir,name=dbfile,dtype=dbtype)
        DSss[tstmid]=DSs
        MF.dTimer('ad2-openDss tstmid: %s basin: %s year: %s dbtype: %s'%(tstmid,basin,byear,dbtype))
        
    (bd2s,rcbd2s)=getBdecks2DataSets(byears,dsbdir=dsbdir,verb=verb)

    return(DSss,bd2s)


def getVdeck2DSs(tstmids,dsbdir=None,dbtype='vdeck2',
                 verb=0):
    
    if(dsbdir == None):
        from tcbase import TcDataBdir
        dsbdir="%s/DSs-VD2"%(TcDataBdir)
    
    # -- OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO - open DSs file
    #
    DSss={}
    yearsAll=getYearsFromStmids(tstmids)

    # -- only use first year for listing
    #
    for year in yearsAll:
    
        MF.sTimer('vdk-openDss-year:%s'%(year))
        dbname="%s_%s"%(dbtype,year)
        dbfile="%s.pypdb"%(dbname)
        DSs=DataSets(bdir=dsbdir,name=dbfile,dtype=dbtype)
        DSss[year]=DSs
        MF.dTimer('vdk-openDss-year:%s'%(year))
    

    return(DSss)

    
    

def getAcards(source,tstmid,ad2Is,taids=[],tstmids9Xall=[],dtgopt=None,
              filt0012=0,filt0618=0,filt00=0,filt12=0,
              chkNhcJtwcAdeck=0,              
              override=0):

    # -- lllllllllllllllllddddddddddddddddeeeeeeeeeeeeffffffffffffffffssssssssssssssss
    
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
    

    def doHHfilt(dtg,filt0012,filt0618,filt00,filt12):
        rc=0
        HH=dtg[8:10]
        
        if(filt0012 or filt00 and HH == '00'): rc=1
        if(filt0618 and (HH =='06' or HH == '18')): rc=1
        if(filt0012 or filt12 and HH == '12'): rc=1
        if(filt0012 == 0 and filt0618 == 0 and filt00 == 0 and filt12 == 0): rc=1
        
        return(rc)
        

    # -- mmmmmmmmmmmmmmmmmmmmmmmmaaaaaaaaaaaaaaaiiiiiiiiiiiiiiiiiiinnnnnnnnnnnnnnnn

    (snum,b1id,stmyear,b2id,stm2id,stm1id)=getStmParams(tstmid)
    
    byear=stmyear
    
    sdir="%s/%s/%s"%(TcAdecksAtcfFormDir,byear,source)
    sfile="a%s%s%s.dat"%(b2id.lower(),snum,stmyear)

    prependAid=None

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

    elif(source == 'tmtrkN'):
        
        adcurpath="%s/%s"%(sdir,sfile)
        acards=getcards(adcurpath,source,tstmid,ad2Is)
        prependAid='t'

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

    elif(source == 'rtfim' or source == 'rtfim9'):
        
        adcurpath="%s/%s"%(sdir,sfile)
        acards=getcards(adcurpath,source,tstmid,ad2I)
        prependAid='j'
        
    else:
        print 'EEE ad2.getAcards -- invalid source: ',source
        sys.exit()

    tdtgs=None
    if(dtgopt != None): tdtgs=mf.dtg_dtgopt_prc(dtgopt)
    
    if(filt0012 or filt0618 or filt00 or filt12 or tdtgs != None):
        
        acards=acards.split('\n')
        
        # -- now pull out the aids
        #
        ocards=[]
        for taid in taids:  
            ttaid=taid
            if(prependAid != None): ttaid=taid[1:]
            for acard in acards:
                if(len(acard) == 0): continue
                dtg=acard.split(',')[2].strip()
                if(len(acard) > 0 and mf.find(acard.lower(),ttaid.lower()) and 
                   doHHfilt(dtg,filt0012,filt0618,filt00,filt12)): 
                    if(tdtgs != None and not(dtg in tdtgs)): continue
                    ocard=acard
                    ocards.append(ocard)
        acards=''
        for n in range(0,len(ocards)):
            ocard=ocards[n]
            acards=acards+ocard
            if(n < len(ocards)-1): acards=acards+'\n'

    return(acards,byear,prependAid)
    

def uniqAcards(acards,source='UNSPEC',tstmid='XXX.YYYY',verb=0,warn=1):
    
    from adCL import AdeckFromCards
    
    # -- reason this works is because making the adeck using AdeckFromCards by storm aid does uniq except by tau 
    #    allows multiple cards for each wind radii
    #
    def uniqAd(acards):
        oacards=[]
        ocards={}
        taus=[]
        for acard in acards:
            tt=acard.split()
            tau=int(tt[5].split(',')[0])
            taus.append(tau)
            MF.appendDictList(ocards, tau, acard)
            
        taus=mf.uniq(taus)
        taus.sort()
        
        for tau in taus:
            tcards=ocards[tau]
            oacards=oacards+mf.uniq(tcards)

        return(oacards)
            
            
        

    nci=len(acards)
    
    if(warn > 1): MF.sTimer('Ni: %-7d makeAdeck'%(nci))
    adA=AdeckFromCards(acards)
    if(warn > 1): MF.dTimer('Ni: %-7d makeAdeck'%(nci))

    dtgs=adA.dtgs
    dtgs.reverse()
    
    aids=adA.aids
    aidstms=adA.aidstms
    
    allcards=[]
    
    for dtg in dtgs:
        
        for aid in aids:
            nuniq=0
            for stm in aidstms[aid]: 
                akey=(aid,stm)
                try:
                    acards=adA.aidcards[akey][dtg]
                    ni=len(acards)
                    ocards=uniqAd(acards)
                    no=len(ocards)
                
                    if(ni != no):

                        nuniq=nuniq+1
                        
                        if(verb): 
                            for acard in acards:
                                print 'A: ',acard[0:-1]
                            print 
                            print 'output: '
                            print
                            for ocard in ocards:
                                print 'O: ',ocard[0:-1]
                                    
                    allcards=allcards+ocards
                except:
                    None
            
        if(warn and nuniq > 0): print 'Nuniq: %4d  source: %-10s'%(nuniq,source),' stmid: ',tstmid,' dtg: ',dtg
                    
    nco=len(allcards)
    if(warn and nuniq > 0):
        MF.sTimer('No: %-7d makeAdeck'%(nco))
        MF.dTimer('No: %-7d makeAdeck'%(nco))

    return(allcards)

def doUniqAd2(ipath,source,tstmid,backup=0,warn=0,verb=0):

    (idir,ifile)=os.path.split(ipath)
    if(warn): MF.sTimer('read    %s'%(ifile))
    acards=open(ipath).readlines()
    if(warn): MF.dTimer('read    %s'%(ifile))

    opath=ipath

    if(backup):
        bpath="%s-BAK"%(ipath)
        rc=MF.WriteList2Path(acards,bpath)

    allcards=uniqAcards(acards,source,tstmid,verb=verb)

    nci=len(acards)
    nco=len(allcards)

    opath=ipath
    (odir,ofile)=os.path.split(opath)
    if(warn): MF.sTimer('write   %s'%(ofile))
    rc=MF.WriteList2Path(allcards,opath)
    if(warn): MF.dTimer('write   %s'%(ofile))

    return(rc)


def getAdeckPathsCardsZip(source,dtg,byear,stype='atcf'):
    
    yyyy=dtg[0:4]
    yyyymm=dtg[0:6]
    
    sfileMask=None
    sopaths={}
    
    if(stype == 'atcf' and source == 'tmtrkN'):
        afileMask="tctrk.atcf.%s"%(dtg)
        afileMask1=None
        afileMask2=None
        sfileMask="stdout.tctrk.%s"%(dtg)
    elif(stype == 'gen' and source == 'tmtrkN'):
        afileMask="%s"%(dtg)
        afileMask1="tcgen.atcf"
        afileMask2=None
        
    elif(stype == 'atcf' and source == 'mftrkN'):
        afileMask1="%s"%(dtg)
        afileMask="wxmap2.v01"
        #afileMask2=".%s"%(byear)
        afileMask2=None
    else:
        print 'EEE-adVM.getAdeckPathsZip invalid stype: ',stype,'press...'
        sys.exit()

    if(source == 'tmtrkN'):
        zipDir=TcAdecksTmtrkNDir
        zipDirStdout=TcTmtrkNDir
        
    elif(source == 'mftrkN'):
        zipDir=TcAdecksMftrkNDir
        zipDirStdout=None
        
    MF.ChkDir(zipDir,'mk')
    zipPath="%s/%s/%s-%s.zip"%(zipDir,yyyy,source,yyyymm)
    rc=MF.ChkPath(zipPath)
    if(rc == 0):
        print 'EEE-AdeckGen2.initAdeckPathsZip zipPath: ',zipPath,' not there return 0,None,None'
        return(0,None,None,None,None)

    try:
        AZ=zipfile.ZipFile(zipPath)
    except:
        print 'bad zipfile: ',zipPath,' return -1'
        return(-1,None,None,None,None)


    if(zipDirStdout != None):
        zipPathStdout="%s/%s/trk-%s-%s.zip"%(zipDirStdout,yyyy,source,yyyymm)
        rc=MF.ChkPath(zipPathStdout)
        if(rc == 0):
            print 'EEE-trk-tmtrkN-Stdout zipPath: ',zipPathStdout,' not there...press...'

        try:
            AZS=zipfile.ZipFile(zipPathStdout)
        except:
            print 'bad zipfile: ',zipPathStdout,' return -1...press...'
            AZS=None
    
    else:
        AZS=None
    
    if(AZS != None and sfileMask != None):
        szls=AZS.namelist()
        for szl in szls:
            if(mf.find(szl,dtg) and mf.find(szl,sfileMask)):
                zi=AZS.getinfo(szl)
                zt=zi.date_time
                zs=zi.file_size
                zc=AZS.open(szl).readlines()
                zrc=(zs,zt,zc)
                sopaths[szl]=zrc
        
        
    zls=AZ.namelist()
    adpaths={}
    adAllpaths={}
    
    zls.sort()
    for zl in zls:
        
        # -- 20211222 -- find the .txt file with all trackers
        #
        if(mf.find(zl,dtg)):
            lzl=len(zl.split('.'))
            if(stype == 'atcf' and lzl == 5 and mf.find(zl,afileMask)):
                zi=AZ.getinfo(zl)
                zt=zi.date_time
                zs=zi.file_size
                zc=AZ.open(zl).readlines()
                zrc=(zs,zt,zc)
                adAllpaths[zl]=zrc
        
        # -- if this is the allfile continue to next file in zip archive
        #
        if(mf.find(zl,'.txt') and stype == 'atcf'): continue
        
        # -- look for individual tracker output
        #
        t1=mf.find(zl,afileMask)

        if(not(t1)): continue
        ztest=t1
        if(afileMask1 != None): 
            t2=mf.find(zl,afileMask1)
            if(afileMask2 != None):
                tt=zl.split('.')
                tyear=tt[-1]
                t3=(tyear == byear)
                ztest=t1 and t2 and t3
                #print '222',zl,t1,t2,t3,byear,'tt',ztest
            else:
                ztest=(t1 and t2)
                #print '111',zl,t1,t2,'tt',ztest

        if(ztest):
            zi=AZ.getinfo(zl)
            zt=zi.date_time
            zs=zi.file_size
            zc=AZ.open(zl).readlines()
            zrc=(zs,zt,zc)
            adpaths[zl]=zrc
    
    if(len(adpaths) == 0): doZip=0
    else:  doZip=1

    allRc=(doZip,adpaths,zipDir,adAllpaths,sopaths)
    return(allRc)

            
if (__name__ == "__main__"):
    dtg='2019120500'
    source='tmtrkN'
    byear='2019'
    rc=getAdeckPathsCardsZip(source, dtg, byear)
    
    ads=rc[1]
    kk=ads.keys()
    
    for k in kk:
        print k
        cards=ads[k][-1]
        for card in cards:
            print card[0:-1][0:100]
    
    sys.exit()



