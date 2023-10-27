#!/usr/bin/env python

from tcbase import *
import datetime

def doRsync2Kishou(sdir,tdir,
                   doupdate=0,dosizeonly=0,dodelete=0,
                   ropt=''):

    pdir=w2.W2BaseDirEtc
    
    rupopt=''
    if(doupdate): rupopt='-u'

    sizonly=''
    if(dosizeonly):  sizonly='--size-only'

    delopt=''
    if(dodelete): delopt='--delete'

    rsyncopt="%s %s %s --timeout=30 --protocol=29 -alv --exclude-from=%s/ex-w21.txt"%(delopt,rupopt,sizonly,pdir)

    MF.sTimer('adc-doRsync2Kishou')
    cmd="rsync %s %s %s"%(rsyncopt,sdir,tdir)
    MF.runcmd(cmd,ropt)
    MF.dTimer('adc-doRsync2Kishou')

def getOstmidFromOstmidsAll(model,stmid,dtg,byear,ostm2idsAll,komariStmids,blackList=None):
    
    alldtgs=ostm2idsAll.keys()
    alldtgs.sort()
    
    def getON(dtg,stmid):
        
        ostm2id=None
        NNstmid=None

        (rc,year,shemyear)=getNhemShemYearsFromDtg(dtg)
        year=str(year)
        shemyear=str(shemyear)
        stmyear=stmid.split('.')[-1]
        chkshemyear=0
        if(rc ==2 and stmyear != shemyear): chkshemyear=1

        chknhemyear=0
        if(rc == 1): chknhemyear=1

        #print stmid,'------------------stmyear: ',stmyear,'rc:',rc,'year:',year,'sheyear: ',shemyear,'ccc',chknhemyear,chkshemyear

        ostm2ids=ostm2idsAll[dtg]
        try:
            (ostm2id,NNstmid)=ostm2ids[stmid]
        except:
            None
            
        # -- check if curyear storm crosses new years in NHEM
        #
        if(year != stmyear and chknhemyear and IsNhemBasin(stmid)): 
            istmyear=year
            stmidN=stmid[0:3]+'.'+istmyear
            
            try:
                (ostm2id,NNstmid)=ostm2ids[stmidN]
                stmyear=istmyear
            except:
                None
            
        if(IsIoSubBasin(stmid)):

            stmidA=stmid[0:2]+'A.'+stmyear
            stmidB=stmid[0:2]+'B.'+stmyear

            try:
                (ostm2id,NNstmid)=ostm2ids[stmidA]
            except:
                None
            try:
                (ostm2id,NNstmid)=ostm2ids[stmidB]
            except:
                None
                
        elif(IsShemSubBasin(stmid)):
        
            if(year != stmyear and chkshemyear): stmyear=year

            stmidP=stmid[0:2]+'P.'+stmyear
            stmidS=stmid[0:2]+'S.'+stmyear
            #print 'yyyyyyyyyyyyyyyyyyyyyyyyyyy',year,stmyear,chkshemyear,stmidP,stmidS

            # -- if crosses 070100, then try previous year - since stmid calc in Adeck based on dtg
            #
            try:
                (ostm2id,NNstmid)=ostm2ids[stmidP]
            except:
                None
            try:
                (ostm2id,NNstmid)=ostm2ids[stmidS]
            except:
                None
            
        #print 'eeeeeeeeeeeeeeeeeeeeeeeee',ostm2id,NNstmid
        return(ostm2id,NNstmid)

    (snum,b1id,year,b2id,blstm2id,stm1id)=getStmParams(stmid)
    blKey=(model,dtg,blstm2id)
    
    if(blKey in blackList):
        print 'BBBBB----LLLLLL model: ',model,' dtg: ',dtg,' stm2id: ',blstm2id,' is blacklisted'
        return(None,None)
    
    
    # ------------------------------------- main section
    #
    (ostm2id,NNstmid)=getON(dtg,stmid)
    if(ostm2id == None):
        (ostm2id,NNstmid)=getON(mf.dtginc(dtg,-6),stmid)
        if(ostm2id == None):
            (ostm2id,NNstmid)=getON(mf.dtginc(dtg,6),stmid)
            if(ostm2id == None):
                (ostm2id,NNstmid)=getON(mf.dtginc(dtg,-12),stmid)
                if(ostm2id == None):
                    (ostm2id,NNstmid)=getON(mf.dtginc(dtg,12),stmid)

    if(ostm2id != None):
        # -- got one
        return(ostm2id,NNstmid)
    
    else:
        (snum,b1id,year,b2id,tstm2id,stm1id)=getStmParams(stmid)
        (snum,b1id,year,b2id,stm2id,tstmid)=getStmParams(tstm2id)
        if(IsNN(tstm2id) and year == byear):
            if(not(tstm2id in komariStmids)):
                print """NNNNN-Komarimashita nee...can't find ostm2id for stmid: %s model: %-10s at dtg: %s ...press..."""%(stmid,model,dtg)
            ostm2id=None
            NNstmid=None
            komariStmids.append(tstm2id)
        elif(year == byear):
            if(not(tstm2id in komariStmids)):
                print """99999-Komarimashita nee...can't find ostm2id for stmid: %s model: %-10s at dtg: %s ... just set to stm2id: %s"""%(stmid,model,dtg,tstm2id)
            ostm2id=tstm2id
            NNstmid='XXXX.XXXX'
            komariStmids.append(tstm2id)
        return (ostm2id,NNstmid)
    
    return(ostm2id,NNstmid)
        

def replaceStm2Id(adeck,stmid,NNstmid,acards=None):

    ocards=[]
    
    if(acards != None):
        cards=acards
    else:
        cards=MF.ReadFile2List(adeck)
        if(len(cards) == 0):
            print '0 len adeck: ',adeck
            return(ocards)
    
    tt=cards[0].split(',')
    ib2=tt[0].strip()
    inn=tt[1].strip()
    
    ob2=NNstmid[0:2].upper()
    onn=NNstmid[2:4]
    for card in cards:
        card=card.replace(ib2,ob2,1)
        card=card.replace(inn,onn,1)
        ocards.append(card)
    
    return(ocards)


def getConvertAcardsFromAtcfAdeck(adeck,model,tdir,dtg,byear,ostm2idsAll,
                                  komariStmids,
                                  acards=None,
                                  aliases=None,
                                  doCat=1,verb=0,warn=0,warnA=1,warnB=0,warnC=0):
    
    
    blackList=[
        ('ncep','2014040912','al23.2014'),
        ('ncep','2014040918','al23.2014'),
        ('ncep','2014041000','al23.2014'),
        ('ncep','2014041006','al23.2014'),
        ('ncep','2014041012','al23.2014'),
        ('ncep','2014041018','al23.2014'),
        ('ncep','2014041100','al23.2014'),
        ('ncep','2014041106','al23.2014'),
        ('ncep','2014041112','al23.2014'),
        ('ncep','2014041118','al23.2014'),
    ]
    

    ostm2ids=[]
    tpathsOut=[]
    
    if(verb): print 'ADECK: ',adeck
    
    if(acards == None):
        acards=open(adeck).readlines()
    
    # -- reduced form of Adeck() class for simply getting the cards
    #

    #print 'AAAAAAA'
    #for acard in acards:
    #    print acard.strip()
        
    aD2s=AdeckFromCards(acards=acards,warn=warn,aliases=aliases)
    
    # -- singleton -- bail
    #
    if(len(aD2s.aids) == 0):
        if(warnB): print 'WWW no valid cards in adeck: ',adeck,' bail...'
        return(ostm2ids,tpathsOut)
    
    tdiryear=tdir.split('/')[-2]
    
    #aD2s.ls()
    #kk=aD2s.aidtrks[('emdt','ep08.2020')]
    #tt=kk['2020072300']
    #taus=tt.keys()
    #taus.sort()
    #for tau in taus:
        #print 'tau: ',tau,tt[tau]

    #sys.exit()
    
    
    for aid in aD2s.aids:
        
        for stm2id in aD2s.stm2ids:
            
            if(IsValidStmid(stm2id) == 0):
                if(warnB): print 'IIIInvalid stm2id: ',stm2id,' press....'
                continue
            
            (snumT,b1idT,stmyearT,b2idT,stm2idT,stm1id)=getStmParams(stm2id)
            (ostm2id,NNstmid)=getOstmidFromOstmidsAll(model,stm1id,dtg,byear,ostm2idsAll,
                                                      komariStmids,blackList=blackList)
            
            
            # -- get stmyear from ostm2id
            #
            if(ostm2id != None):
                (snumT,b1idT,stmyear,b2idT,stm2idT,stm1idT)=getStmParams(ostm2id)
                
            #if(verb): print 'sss',stm2id,ostm2id,NNstmid,aid,dtg,stmyear
                
    
            # -- bail if no real stm found or stmyear is not target byear
            #
            if(ostm2id == None or stmyear != byear): continue
            
            ostm2ids.append(ostm2id)
            
            tstm2id=ostm2id.replace('.','')
            tstmyear=tstm2id[4:]
            tstm2id=tstm2id[0:2]+tstm2id[2:4].upper()+tstmyear
            otdir=tdir.replace(tdiryear,tstmyear)
            MF.ChkDir(otdir,'mk')
            tpathostm2="%s/a%s.dat"%(otdir,tstm2id)
            
            if(doCat == 0): continue
            
            oacards=[]
            
            try:
                dtgs=aD2s.aiddtgs[aid,stm2id]
                for dtg in dtgs:
                    oacards=oacards+aD2s.aidcards[aid,stm2id][dtg]
            except:
                if(warnC): print 'WWW getConvertAcardsFromAtcfAdeck: 0 for aid: ',aid,' stm2id: ',stm2id
                
            # -- run the uniq for adeck cards ???
            #
            #MF.sTimer('uniq-%s-%s'%(aid,stm2id))
            #oacards=uniqAcards(oacards,warn=1)
            #MF.dTimer('uniq-%s-%s'%(aid,stm2id))
            
            # -- always cat (append=1) to target even if 9X
            #
            tpathsOut.append(tpathostm2)
            MF.WriteList2Path(oacards, tpathostm2, append=1)
            # -- if 9X associated with a NN -- relabel and cat to NN
            #
            tpathNNstm=None
            if(NNstmid[0] != 'X'):
                tNNstmid=NNstmid.replace('.','')
                tpathNNstm="%s/a%s.dat"%(otdir,tNNstmid)
                
            if(tpathNNstm != None and len(oacards) > 0):
                ocards=replaceStm2Id(adeck,stm1id,NNstmid,acards=oacards)
                MF.WriteList2Path(ocards,tpathNNstm,append=1)

    tpathsOut=mf.uniq(tpathsOut)
    ostm2ids=mf.uniq(ostm2ids)
    
    return(ostm2ids,tpathsOut)       
        
        
                
def getConvertAcards(source,dtgs,byear,ad2I,
                     overrideChkAdeck=0,
                     overrideKillAdeck=0,
                     doCat=1,
                     warn=0,
                     ropt='quiet',
                     verb=0,
                     relabelAid=None,
                     doSizOnly=1,
                     ):        

    def getMaskExpr(source,dyear,dtg,byear):

        doZip=0
        rcZip=(doZip,None,None)
        
        # -- target dir
        #
        tdir="%s/%s/%s"%(TcAdecksAtcfFormDir,byear,source)
        MF.ChkDir(tdir,'mk')
        
        # -- get zip adeck and acards
        #
        if(source == 'tmtrkN' or source == 'mftrkN'):
            (doZip,adpaths,zipDir,adAllpaths,sopaths)=getAdeckPathsCardsZip(source, dtg, byear)
            rcZip=(doZip,adpaths,zipDir)
            

        if(source == 'tmtrkN'):
    
            maskexpr=[]
            maskstr="%s/%s/%s/tctrk.atcf.%s.*.???.%s"
            maskexpr.append(maskstr%(TcAdecksTmtrkNDir,dyear,dtg,dtg,byear))
            
        elif(source == 'mftrkN'):
    
            maskexpr=[]
            maskstr="%s/%s/%s/wxmap2.v011.*.%s.???.%s"
            maskexpr=maskstr%(TcAdecksMftrkNDir,dyear,dtg,dtg,byear)

        elif(source == 'psdRR2'):
            
            maskexpr=[]     
            maskstr="%s/%s/%s/tctrk.atcf.%s.*.???.%s"
            maskexpr.append(maskstr%(TcAdecksPsdRR2Dir,dyear,dtg,dtg,byear))
                
        elif(source == 'erai'):
            
            maskexpr=[]     
            maskstr="%s/%s/tctrk.atcf.%s.*.???.%s"
            maskexpr.append(maskstr%(TcAdecksEraiDir,dyear,dtg,byear))
                
        elif(source == 'era5'):
            
            maskexpr=[]     
            maskstr="%s/%s/tctrk.atcf.%s.*.???.%s"
            maskexpr.append(maskstr%(TcAdecksEra5Dir,dyear,dtg,byear))
                
        elif(source == 'cmc'):
            maskexpr=[]     
            maskstr="%s/%s/*.%s.???.%s.*.txt"
            maskexpr.append(maskstr%(TcAdecksCmcDir,byear,dtg,byear))
    
        elif(source == 'gefs'):
            maskexpr=[]     
            maskstr="%s/%s/*.%s.???.%s.*.txt"
            maskexpr.append(maskstr%(TcAdecksNcepDir,byear,dtg,byear))

        elif(source == 'rtfim9' or source == 'rtfim'):
    
            maskstr="%s/%s/%s/track.%s00.*"
            maskexpr=maskstr%(TcAdecksEsrlDir,dyear,source,dtg)
    
        elif(source == 'ecmwf'):
    
            maskstr="%s/%s/a????????.%s.???.*_tigg*txt"
            maskexpr=maskstr%(TcAdecksEcmwfDir,byear,dtg)
            
            # -- h/w for c41r2 || runs
            #maskstr="%s/tctrk.atcf.%s.*.???.%s"
            #TcAdecksEcmwfDir= '/w21/prj/tc/20160406_ecmwf_c41r2-2016030812_trackers/ops/adeck'
            #TcAdecksEcmwfDir= '/w21/prj/tc/20160406_ecmwf_c41r2-2016030812_trackers/c41r2/adeck'
            #maskexpr=maskstr%(TcAdecksEcmwfDir,dtg,byear)

        elif(source == 'ecbufr'):
    
            maskstr="%s/%s/ecbufr/adeck.ecmwf.tcbufr.%s_*.txt"
            maskexpr=maskstr%(TcAdecksEcmwfDir,dyear,dtg)

        elif(source == 'ec-wmo'):
    
            maskstr="%s/%s/wmo/adeck-ecmwf-wmo.%s.???.%s"
            maskexpr=maskstr%(TcAdecksEcmwfDir,byear,dtg,byear)

        elif(source == 'ukmo'):
    
            maskstr="%s/%s/a????%s.%s.*.txt"
            maskexpr=maskstr%(TcAdecksUkmoDir,byear,byear,dtg)
            
        elif(source == 'clip'):
    
            maskexpr=[]
            maskstr="%s/%s/%s/tctrk.atcf.%s.*.???.%s"
            maskexpr.append(maskstr%(TcAdecksClipDir,dyear,dtg,dtg,byear))

        return(rcZip,maskexpr,tdir)
        
        
    def getModelStmid(source,tt):
        
        if(source == 'mftrkN' or source == 'tmtrkN' or 
           source == 'psdRR2' or source == 'erai' or source == 'era5' or
           source == 'clip'):
            stmid="%s.%s"%(tt[-2],tt[-1])   
            model=tt[-3]
            stmid=None
            model=source

        elif(source == 'ecmwf' or source == 'ecbufr' or source == 'ec-wmo'):
            stmid=None
            model=source

        elif(source == 'ukmo'):
            stmid="%s.%s"%(tt[-4],tt[-3])
            stmid=None
            model=source

        elif(source == 'ncep' or source == 'cmc' or source == 'gefs' or
             source == 'rtfim9' or source == 'rtfim'):
            stmid=None
            model=source
            
        return(model,stmid)

    def getModelAliases(source):

        aliases=None
        
        if(source == 'mftrkN'):
            aliases={
                'NUK2':'UKM2',
                'NGF2':'GFS2',
                'NCM2':'CMC2',
                'NEC2':'ECM2',
                'NNG2':'NGP2',
            }

        return(aliases)
        
    ostm2idsAll={}
    
    if(ropt == 'norun'): 
        print 'DDDoing source: ',source,'dtgs: ',dtgs[0],' to ',dtgs[-1],' byear: ',byear
        return
    
    MF.sTimer("%s-all-adecks"%(source))
    

    # -- get the ostm2ids +/- 12 for checking in getOstmidFromOstmidsAll()
    #
    MF.sTimer('get-ostm2ids')
    
    bdtg=mf.dtginc(dtgs[0],-12)
    edtg=mf.dtginc(dtgs[-1],+12)
    odtgs=mf.dtgrange(bdtg,edtg,6)
    
    apathsOut=[]
    stmidsOut=[]
    
    oldyear=9999999
    oldshemyear=9999999
    for odtg in odtgs:
        
        # -- get tD
        curyear=odtg[0:4]
        shemyear=getShemYear(odtg)
        if(curyear != oldyear or shemyear != oldshemyear):
            MF.sTimer('setting TcData-%s'%(odtg))
            oldyear=curyear
            oldshemyear=shemyear
            tD=TcData(dtgopt=odtg)
            MF.dTimer('setting TcData-%s'%(odtg))
            
        ostm2ids=tD.getRawStm2idDtg(odtg,dupchk=0)
        if(verb): print '1111111111111111',odtg,ostm2ids.keys()
        ostm2idsAll[odtg]=ostm2ids

    MF.dTimer('get-ostm2ids')
    if(ropt == 'norun'): sys.exit()

    # -- set return code to no cards processed
    #
    rcA=0
    
    komariStmids=[]
    for dtg in dtgs:
        
        # -- get the stmids for trackers
        #
        stmids=[]
        
        dyear=dtg[0:4]
        (rcZip,adeckpathmask,tdir)=getMaskExpr(source,dyear,dtg,byear)
        
        if(verb): print 'AAA adeckpathmask: ',adeckpathmask
        if(dtg == dtgs[0] and overrideKillAdeck):
            cmd="rm %s/a????????.dat"%(tdir)
            MF.runcmd(cmd,'')
            
        if(type(adeckpathmask) is ListType):
            adecks=[]
            for admask in adeckpathmask:
                adecks=adecks+glob.glob(admask)
            
        else:
            adecks=glob.glob(adeckpathmask)
            
        #print 'AAA',adecks
        # -- if no adecks...return
        #
        if(len(adecks) == 0 and rcZip[0] != 1):

            if(warn): print 'WWW -- getConvertAcards -- no adeck files and no adecks in .zip for dtg: ',dtg,'...press...'
            #MF.dTimer("%s-all-adecks"%(source))
            #return(0)
            continue
        

        doZip=rcZip[0]
        #print 'ZZZ',rcZip[1].keys()

        if(doZip):
            zadecks=[]
            if(rcZip[1] != None):
                zadecks=rcZip[1]
                zdir=rcZip[2]
    
            adkk=ad2I.data.keys()
    
            if(verb > 1):
                for ak in adkk:
                    if(mf.find(ak,dtg)):
                        print 'ak:',ak,ad2I.data[ak]
            
            adecks=zadecks.keys()
            adecks.sort()
    
            for adeck in adecks:
                zdeck="%s/%s/%s"%(zdir,dtg[0:4],adeck)
                if(verb > 1): print 'AA',adeck,'siz, time',zadecks[adeck][0:1]
                if(zdeck in adkk):
                    if(verb > 1): print 'IIIZZZ',zdeck,ad2I.data[zdeck]
                elif(adeck in adkk):
                    if(verb > 1): print 'IIIAAA',adeck,ad2I.data[adeck]
    
            if(verb > 1):
                for adk in adkk:
                    if(mf.find(adk,dtg)): 
                        print 'ZZ',zdir,adk
                
        # -- code a modify aliases -- for converting fm8z -> fm8t when zeus went away
        # -- will do in separate script...
        #
        aliases=getModelAliases(source)
        if(relabelAid != None):
            tt=relabelAid.split(":")
            newaliases={tt[0].upper():tt[1].upper()}
            if(aliases != None):
                aliases.update(newaliases)
            else:
                aliases=newaliases

        # -- check if we will get to cards by storm or if using Adeck2s...
        #
        stmid=None
        for adeck in adecks:
            
            if(doZip):
                (asiz,atime,acards)=zadecks[adeck]
            else:
                asiz=MF.GetPathSiz(adeck)
                (atime,atimei)=MF.PathModifyTimei(adeck)
                
            if(asiz == 0):
                if(warn): print 'WWW a2a.getConvertAcards() for adeck: ',adeck,' zero sized...'
                continue

            if(doZip):
                
                zdeck="%s/%s/%s"%(zdir,dtg[0:4],adeck)
                try:
                    (asizI,zatimeI)=ad2I.data[zdeck]
                    gotInv=2
                    #print 'ZZZZZ----',asizI,zatimeI,zdeck
                except:
                    gotInv=0
                    
                if(gotInv == 0):
                    
                    try:
                        (asizI,zatimeI)=ad2I.data[adeck]
                        #print 'OOOOO-----',asizI,zatimeI,adeck
                        gotInv=1
                    except:
                        gotInv=0
                    
                if(gotInv > 0):
                    if(gotInv == 2):
                        atimeI=zatimeI
                    else:
                        atimeI=zatimeI
                        if(len(atimeI) == 6):
                            atimeI=atimeI+(0,0,0)
                        
                    atime=atime+(0,0,0)
                    atime=time.struct_time(atime)
                    #print 'ooooo--aaaaaaaa',atime
                    
            else:
                # -- file adeck
                #
                try:
                    (asizI,atimeI)=ad2I.data[adeck]
                    gotInv=1
                except:
                    gotInv=0
                    
            # -- comp this adeck to the inventory
            #
            doAdeck=1
            dsiz=-1
            dt=-1
            dtTest=False
            if(gotInv):
                
                dt=MF.DeltaTimei(atime,atimeI)
                dsiz=asiz-asizI
                dtTest=(abs(dt) > 0.01)
                doAdeck=0
                if(doSizOnly):
                    if(dsiz != 0): doAdeck=1
                else:
                    if(dsiz != 0 or dtTest): doAdeck=1
                    else: doAdeck=0

            if(verb): print  'AAA----------------------------: ',adeck,'dsiz: ',dsiz,'dt: ',\
              dt,' dtTest: ',dtTest,' doAdeck: ',doAdeck,' doSizOnly: ',doSizOnly,overrideChkAdeck
            
            if(doAdeck or overrideChkAdeck):
                (pdir,pfile)=os.path.split(adeck)
                tt=pfile.split('.')
                (model,stmid)=getModelStmid(source,tt)
                
                acards=None
                if(doZip):
                    acards=zadecks[adeck][-1]

                if(stmid == None):
                    (stmids,opaths)=getConvertAcardsFromAtcfAdeck(adeck,model,tdir,dtg,byear,ostm2idsAll,
                                                                  komariStmids,
                                                                  acards=acards,
                                                                  aliases=aliases,warn=verb,
                                                                  doCat=doCat,verb=verb)
                    ad2I.data[adeck]=(asiz,atime)
                    if((adeck == adecks[0] or verb) and len(stmids) > 0): 
                        print '0000-adeck-convert: %-40s %s '%(pfile,dtg),stmids
                        
                    apathsOut=apathsOut+opaths
                    stmidsOut=stmidsOut+stmids
                        
        
        # -- bail uniq if no storms
        #
        if(len(stmidsOut) == 0): continue         
        
        apathsOut=mf.uniq(apathsOut)
        stmidsOut=mf.uniq(stmidsOut)
        

    rcA=0
    if(len(apathsOut) > 0): rcA=1
    
    # -- do uniq AFTER we've done the merge
    #
    if((rcA or overrideChkAdeck) and doUniq):
        MF.sTimer("uniq-%s-Napaths-%03d"%(source,len(apathsOut)))
        for apath in apathsOut:
            (adir,afile)=os.path.split(apath)
            stm2id=afile[1:5]+"."+afile[5:9]
            rc=getStmParams(stm2id)
            stm1id=rc[-1]
            doUniqAd2(apath,source,stm1id,warn=1)

        MF.dTimer("uniq-%s-Napaths-%03d"%(source,len(apathsOut)))


    MF.dTimer("%s-all-adecks"%(source))
        
    return(rcA)
	    
	    
def getModelDtgsByYear(source,byear):
    
    byearm1=str(int(byear)-1)
    
    
    if(source == 'ecmwf' or source == 'ecbufr' or 
       source == 'erai' or source == 'era5' or
       source == 'cmc' or 
       source == 'ukmo' 
       ):
        dtgoptShem="%s07.%s12.12"%(byearm1,byearm1)
        dtgoptNhem="%s01.%s12.12"%(byear,byear)
        
    elif(source == 'tmtrkN' or source == 'mftrkN' or 
         source == 'psdRR2' or source == 'ec-wmo' or
         source == 'ncep' or source == 'clip' or
         source == 'gefs'
         ):
        dtgoptShem="%s07.%s12.6"%(byearm1,byearm1)
        dtgoptNhem="%s01.%s12.6"%(byear,byear)
    
    else:
        print "EEE invalid source..."%(source3)
        sys.exit()
        
    dtgsS=mf.dtg_dtgopt_prc(dtgoptShem)
    dtgsN=mf.dtg_dtgopt_prc(dtgoptNhem)
    
    return(byearm1,dtgsS,dtgsN)

def getByearsByDtgs(dtgopt,dtgs):
    tD=TcData(dtgopt=dtgopt)
    bstmids=tD.getStmidDtgs(dtgs)
    byears=getYearsFromStmids(bstmids)
    return(byears)
    
    
        
#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
#
# command line setup
#

class TCVCAdeckCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):
        
        if(argv == None): argv=sys.argv
        
        self.argv=argv
        self.argopts={
            1:['source',  '''source1[,source2,...,sourceN]'''],
            }
            
        self.options={
            'overrideOpt':         ['O:',0,'i','override -O1 :: overrideChkAdeck=1  -O2 :: overrideInv=1   -O3 :: overrideInv/Kill/ChkAdeck=1   '],
            'verb':                ['V',0,1,'verb is verbose'],
            'ropt':                ['N','','norun',' norun is norun'],
            'dtgopt':              ['d:',None,'a','year'],
            'byear':               ['y:',None,'a','year'],
            'doCat':               ['C',1,0,'1 - do NOT make data files'],
            'runAdeck2':           ['A',0,1,'1 run adeck2'],
            'doUniq':              ['U',1,0,'do NOT do acards uniq'],
            'put2Kaze':            ['K',0,1,'''if on kishou, process directly to kaze $W2_HFIP'''],
            'relabelAid':          ['R:',None,'a','relabel CCC0:NNN0 where CCC0 is current name and NNN0 is new'],
            'doRsync2Kaze':        ['r',0,1,'DO rsysc dss to kaze if on kishou'],
            }

        self.defaults={
            'diag':              0,
            }

        self.purpose='''
purpose -- convert tm|mftrKN|ec*|ncep... locally processed adecks to ATCF-standard adeck as at JTWC/NHC
sources: %s'''%(w2.TCsourcesActive)
        self.examples='''
%s tmtrkN -d 2014090700.2014090800 -y 2014
'''

        
        
#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# -- main
#

CL=TCVCAdeckCmdLine(argv=sys.argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

# -- inv bdir
#
dsbdir="%s/DSs"%(TcDataBdir)

# -- make sure ad2 is not running
#
pyfileAD2='w2-tc-dss-ad2.py'
rc=MF.chkRunning(pyfileAD2,strictChkIfRunning=1,killjob=1,nminWait=5)

# -- check if running with method in adVM
#
rc=MF.chkRunning(pyfile,strictChkIfRunning=0,killjob=0,nminWait=5)


if(byear == None and dtgopt == None):
    print 'EEE(%s) - must set byear using -y YYYY|cur OR set dtgopt'%(pyfile)
    sys.exit()
    
# -- OOOOOO override opts
#
overrideInv=0
overrideChkAdeck=0
overrideKillAdeck=0
if(overrideOpt == 1): overrideChkAdeck=1
if(overrideOpt == 2): overrideInv=1
if(overrideOpt == 3): overrideInv=1 ;overrideKillAdeck=1; overrideChkAdeck=1


MF.sTimer('ALL-ADC')

# -- sources
#
if(byear == 'cur'): byear=curyear

if(source == 'all'):
    sources=w2.TCsourcesActive
else:
    sources=source.split(',')
    source=sources[0]
    
byearm1=None

if(dtgopt != None):
    dtgs=mf.dtg_dtgopt_prc(dtgopt,ddtg=6)
    if(byear == None):
        byears=getByearsByDtgs(dtgopt,dtgs)
    else: byears=[byear]
else:
    byears=[byear]

for source in sources:
    
    doSizOnly=0
    if(source == 'ncep'): doSizOnly=1
    
    ad2Done=0
    rcAall=0
    rcA=None

    for byear in byears:

        if(dtgopt == None):
            (byearm1,dtgsS,dtgsN)=getModelDtgsByYear(source,byear)
            
        ad2I=AdToAtcfInvHash(source,byear,
                             tbdir=dsbdir,
                             verb=verb,
                             overrideInv=overrideInv,
                             )

        if(byearm1 != None):
            
            rc=getConvertAcards(source,dtgsS,byear,ad2I,overrideChkAdeck,overrideKillAdeck,doCat,doSizOnly=doSizOnly,
                                verb=verb,ropt=ropt,relabelAid=relabelAid)
            
            # -- make sure overridekilladeck = 0 if done the first time
            #
            overrideKillAdeck=0
            rcA=getConvertAcards(source,dtgsN,byear,ad2I,overrideChkAdeck,overrideKillAdeck,doCat,doSizOnly=doSizOnly,
                                verb=verb,ropt=ropt,relabelAid=relabelAid)
        else:
            btag='BBBBB-adc year: %s %s-%s'%(byear,dtgs[0],dtgs[-1])
            print
            print 'BBBBB-adc'
            print btag
            print 'BBBBB-adc'
            print
            
            MF.sTimer(btag)
            rcA=getConvertAcards(source,dtgs,byear,ad2I,overrideChkAdeck,overrideKillAdeck,doCat,doSizOnly=doSizOnly,
                                verb=verb,ropt=ropt,relabelAid=relabelAid)
            if(rcA): rcAall=1
            print
            print 'BBBBB-adc-DONE'
            MF.dTimer(btag)
            print 'BBBBB-adc-DONE-TIMER'
            print
            
        
    if(ropt != 'norun' and rcA != None): ad2I.put()
    
    rcATest=0
    if(rcAall == 1): rcATest=1
    if( (rcAall == 0 and overrideKillAdeck) or overrideChkAdeck ): rcATest=1
        
    if(runAdeck2 and rcATest == 0):
        print 'WWW-wanted to do runAdeck2...rcATest=0...rcA: ',rcAall,' overrideKillAdeck: ',overrideKillAdeck
        
    if( (dtgopt != None and rcATest or overrideChkAdeck) and (runAdeck2 and ad2Done == 0) ):
        rsyncOpt=''
        if(doRsync2Kaze): rsyncOpt='-r'
        oOpt=''
        if(overrideChkAdeck): oOpt='-O1'
        print
        print 'AAAAA-adc-NN'
        print 'AAAAA-adc-NN %s dtgopt: %s'%(byear,dtgopt)
        print 'AAAAA-adc-NN'
        print
        
        cmd="%s/w2-tc-dss-ad2.py %s -d %s %s %s"%(pydir,source,dtgopt,rsyncOpt,oOpt)
        mf.runcmd(cmd,ropt)

        # -- do 9X in here
        #
        print
        print 'AAAAA-adc-9X'
        print 'AAAAA-adc-9X %s dtgopt: %s'%(byear,dtgopt)
        print 'AAAAA-adc-9X'
        print
        
        cmd="%s/w2-tc-dss-ad2.py %s -d %s %s %s -9"%(pydir,source,dtgopt,rsyncOpt,oOpt)
        mf.runcmd(cmd,ropt)
        
        ad2Done=1
        
    if(put2Kaze and w2.onKishou):
        sdir="%s/%s/%s/"%(TcAdecksAtcfFormDir,byear,source)
        tdir="%s/%s/%s/"%(TcAdecksAtcfFormDirKishou,byear,source)
        doRsync2Kishou(sdir,tdir,ropt=ropt)
            

MF.dTimer('ALL-ADC')

sys.exit()
    
