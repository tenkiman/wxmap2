from WxMAP2 import *
w2=W2()

from tcVM import *
from adCL import Adeck,AdeckGen,AdeckGenTctrk

from TCtrk import TcPrBasin,tcgenModels,getBasinLatLonsPrecise,tcgenW3DatDir,\
     tcgenW3Dir,tcgenModelLabel,getBasinOptFromStmids,tcgenBasins,getGentaus,tcgenModelLabel

#from tcbase import AdeckBaseDir,YearTcBtNeumann
from tcbase import AdeckBaseDir

undef=-999

class TcPrcMonitor(MFbase):
    
        
    def __init__(self,stmopt,model,dobt,doBT,ls9x,
                 dtgopt=None,
                 tcD=None,
                 useHfip=0,
                 doprint=0,
                 verb=0):

        from tcbase import TcAdecksTmtrkNDir,TcAdecksMftrkNDir,TcDiagDatDir,TcGenDatDir,TcDataBdir

        tmtrkBdirLocal=TcAdecksTmtrkNDir
        mftrkBdirLocal=TcAdecksMftrkNDir
    
        tmtrkBdirHfip="%s/w21/dat/tc/adeck/tmtrkN"%(w2.DATKazeBaseDir)
        mftrkBdirHfip="%s/w21/dat/tc/adeck/mftrkN"%(w2.DATKazeBaseDir)

        stdout_tmtrkBdirLocal="%s/tmtrkN"%(TcDataBdir)
        stdout_tmtrkBdirHfip="%s/w21/dat/tc/tmtrkN"%(w2.DATKazeBaseDir)
    
        diagBdirLocal=TcDiagDatDir+'DAT'
        diagBdirHfip="%s/w21/dat/tcdiagDAT"%(w2.DATKazeBaseDir)
    
        genBdirLocal=TcGenDatDir
        genBdirHfip="%s/w21/dat/tcgenDAT"%(w2.DATKazeBaseDir)
        
        genBdir=genBdirLocal
        diagBdir=diagBdirLocal
        tmtrkBdir=tmtrkBdirLocal
        stmtrkBdir=stdout_tmtrkBdirLocal
        mftrkBdir=mftrkBdirLocal

        if(useHfip): 
            genBdir=genBdirHfip
            diagBdir=diagBdirHfip
            tmtrkBdir=tmtrkBdirHfip
            stmtrkBdir=stdout_tmtrkBdirHfip
            mftrkBdir=mftrkBdirHfip

        # -- always use hfip for tcdiag
        #
        diagBdir=diagBdirHfip

        self.stmtrkBdir=stmtrkBdir
        self.genBdir=genBdir
        self.diagBdir=diagBdir
        self.tmtrkBdir=tmtrkBdir
        self.mftrkBdir=mftrkBdir

        self.stmtrkBdirLocal=stdout_tmtrkBdirLocal
        self.genBdirLocal=genBdirLocal
        self.diagBdirLocal=diagBdirLocal
        self.tmtrkBdirLocal=tmtrkBdirLocal
        self.mftrkBdirLocal=mftrkBdirLocal

        self.stmtrkBdirHfip=stdout_tmtrkBdirHfip
        self.genBdirHfip=genBdirHfip
        self.diagBdirHfip=diagBdirHfip
        self.tmtrkBdirHfip=tmtrkBdirHfip
        self.mftrkBdirHfip=mftrkBdirHfip


        # -- output
        statusS={}
        pathsS={}
        dtgsS={}
        self.pTCdev={}        

        self.model=model
        self.verb=verb
        self.doprint=0

        if(tcD == None):
            if(stmopt != None):  
                tcD=TcData(stmopt=stmopt,verb=verb)
            elif(dtgopt != None and stmopt == None):
                tcD=TcData(dtgopt=dtgopt,verb=verb)
            else:
                print 'EEE(tcCL.TcPrcMonitor) -- must set either stmopt or dtgopt'
                sys.exit()
    
        dobtStms=0
     
        if(stmopt != None):
            if(dobt or doBT and stmopt[0] != '9'): dobtStms=1
            stmids=tcD.makeStmListMdeck(stmopt,dobt=dobtStms,cnvSubbasin=0)
            sdtgs=None
            
        elif(dtgopt != None):
            sdtgs=mf.dtg_dtgopt_prc(dtgopt=dtgopt)
            #stmids=tcD.getStmidDtgs(sdtgs,dobt=dobt)
            rstmids={}
            for sdtg in sdtgs:
                rstmids.update(tcD.getRawStm2idDtg(sdtgs[0],dobt=dobt,dupchk=1))
            
            stmids=rstmids.keys()
            stmids=sortStmids(stmids)
            
        
        self.stmids=stmids
        
        for stmid in stmids:
                    
            # -- merge both 9x and real/final bdeck
            #
            set9xfirst=1
            
            rstmid=rstmids[stmid][0]
            
            # -- mechanism to output only 9x in TcData.lsDSsStm
            #
            #if(ls9x or Is9X(stmid)): dobt=-1
            #if(doBT): dobt=2 ; set9xfirst=1 # -- want to show NN first vice 9X as for operational posits (default)

            set9xfirst=1
            (ocards,ocardsum)=tcD.getDSsStmCards(rstmid,dobt=dobt,
                                                 set9xfirst=set9xfirst,
                                                 convert9x=0,
                                                 verb=verb)
            
            dtgs=ocards.keys()
            dtgs.sort()

            for dtg in dtgs:
                if( (sdtgs != None and dtg in sdtgs) or sdtgs == None):
                    (statusCard,opathsS)=self.getTrkDiagGenStatus(dtg,model,ocards[dtg],ocardsum)
                    statusS[stmid,dtg]=statusCard
                    pathsS[stmid,dtg]=opathsS
                    MF.appendDictList(dtgsS, stmid, dtg)
            
        
        self.statusS=statusS
        self.dtgsS=dtgsS
        self.pathsS=pathsS


    def getTrkDiagGenStatus(self,dtg,model,ocard,ocardsum):
    
        def parseOcard(ocard):
            
            tt=ocard.split()
            stmid=tt[1]
            vmax=tt[2]
            clat=tt[4]
            clon=tt[5]
            
            return(stmid,vmax,clat,clon)
            
        def parseOcardSum(ocardsum):

            tt=ocardsum.split()
            year=tt[0]
            stmidNN="%s.%s"%(tt[1][0:3],year)
            if(mf.find(ocardsum,'9X:')):
                stmid9X="%s.%s"%(tt[-3],year)
            elif(mf.find(ocardsum,'NN:')):
                stmid9X=stmidNN
                stmidNN="%s.%s"%(tt[-1],year)
            else:
                stmid9X=stmidNN
                
            basin='xxxxx'
            b1id=stmidNN[2].lower()
            for basin in TcGenBasin2B1ids.keys():
                if(b1id in TcGenBasin2B1ids[basin]): break
                    
            return(stmidNN,stmid9X,basin)
            
        
        year=dtg[0:4]

        sdirTM="%s/%s/%s"%(self.tmtrkBdir,year,dtg)
        sdirTMs="%s/%s/%s"%(self.stmtrkBdir,dtg,model)
        sdirMF="%s/%s/%s"%(self.mftrkBdir,year,dtg)
        sdirDG="%s/%s/%s/DIAGFILES"%(self.diagBdir,year,dtg)
        sdirGN="%s/%s/%s"%(self.genBdir,year,dtg)
        
        (stmid,vmax,clat,clon)=parseOcard(ocard)
        (stmidNN,stmid9X,basin)=parseOcardSum(ocardsum)
        stmidNN=getStmParams(stmidNN,convert9x=1)[-1]
        stmid9X99=getStmParams(stmid9X,convert9x=1)[-1]
        stmid9X99I=getStmParams(stmid,convert9x=1)[-1]

        self.stmidNN=stmidNN
        self.stmid9X99=stmid9X99
        self.pTCdev[stmid9X]=1
        self.pTCdev[stmidNN]=1
        if(stmidNN == stmid9X99):
            self.pTCdev[stmid9X]=0
            self.pTCdev[stmidNN]=0

        if(self.verb):
            print 'bbbbbbbbbbb',basin
            print 'ddddddddddd',dtg,ocard
            print 'mmmmmmmmmmm',model
            print 'sssssssssss',stmid
            print 'uuuuuuuuuuu',stmidNN,stmid9X,stmid9X99,stmid9X99I
            
            print 'TM: ',sdirTM
            print 'MF: ',sdirMF
            print 'DG: ',sdirDG
            print 'GN: ',sdirGN
            
        afiles99I=glob.glob(("%s/tctrk.atcf.*.%s.%s")%(sdirTM,model,stmid9X99I))
        afiles99=glob.glob(("%s/tctrk.atcf.*.%s.%s")%(sdirTM,model,stmid9X99))
        afilesNN=glob.glob(("%s/tctrk.atcf.*.%s.%s")%(sdirTM,model,stmidNN))
        afiles99all=glob.glob(("%s/tctrk.atcf.*.%s.*")%(sdirTM,model))
        afilesNNall=glob.glob(("%s/tctrk.atcf.*.%s.*")%(sdirTM,model))
        
        smask99="%s/stdout.tctrk.%s.%s.%s.txt"%(sdirTMs,dtg,model,stmid9X99.lower().split('.')[0])
        smaskNN="%s/stdout.tctrk.%s.%s.%s.txt"%(sdirTMs,dtg,model,stmidNN.lower().split('.')[0])
        sfiles99=glob.glob(smask99)
        sfilesNN=glob.glob(smaskNN)
        smask99I="%s/stdout.tctrk.%s.%s.%s.txt"%(sdirTMs,dtg,model,stmid9X99I.lower().split('.')[0])
        sfiles99I=glob.glob(smask99I)
        
        
        nmask="%s/tcgen.atcf.%s.%s.%s.txt"%(sdirTM,basin,dtg,model)
        nfiles=glob.glob(nmask)
        dmask99I="%s/tcdiag.%s.%s.%s.*.txt"%(sdirDG,model,dtg,stmid9X99I.lower())
        dmask99="%s/tcdiag.%s.%s.%s.*.txt"%(sdirDG,model,dtg,stmid9X99.lower())
        dmaskNN="%s/tcdiag.%s.%s.%s.*.txt"%(sdirDG,model,dtg,stmidNN.lower())
        dfiles99I=glob.glob(dmask99I)
        dfiles99=glob.glob(dmask99)
        dfilesNN=glob.glob(dmaskNN)
        gfiles=glob.glob("%s/%s.%s.???.%s.*fcst*"%(sdirGN,model,dtg,basin))
        dfiles=dfiles99+dfilesNN+dfiles99I
        
        if(self.verb):
            print 'a99I:     ',afiles99I
            print 'a99:      ',afiles99
            print 'aNN:      ',afilesNN
            print 'a99all:   ',afiles99all
            print 'aNNall:   ',afilesNNall
            print 'aGen:     ',nfiles
            print 'dmask99I: ',dmask99I
            print 'dmask99:  ',dmask99
            print 'dmaskNN:  ',dmaskNN
            print 'diag:     ',dfiles
            print 'gen:      ',gfiles
            print 'smask99   ',sfiles99
            print 'smaskNN   ',sfilesNN
            
        tmTrkRun=0
        if(len(afiles99all) > 0 or len(afilesNNall) > 0): tmTrkRun=1
        
        gotTm=0
        if(len(afiles99) > 0 or len(afiles99I) > 0 or len(afilesNN) > 0): gotTm=1

        if(gotTm == 0 and (len(sfiles99) > 0 or len(sfilesNN) > 0)): gotTm='M'
            
        gotTmGen=0
        if(len(nfiles) > 0): gotTmGen=1
        
        gotDiag=0
        if(len(dfiles) > 0): gotDiag=1
        
        gotGen=0
        if(len(gfiles) > 0): gotGen=1
        
        statusTm="tmTrk:%1d%1s%d"%(tmTrkRun,str(gotTm),gotTmGen)
        statusDiag="tcDiag:%1d"%(gotDiag)
        statusGen="tcGen:%1d"%(gotGen)
        
        pathsS=(afiles99,afilesNN,dfiles,gfiles)
        statusCard="%s %s %3s %6s %6s  %s %s %s  %-8s"%(dtg,stmid,vmax,clat,clon,statusTm,statusDiag,statusGen,model)
        if(self.doprint): print statusCard

        
        return(statusCard,pathsS)


class AdeckGen2(AdeckGen):


    def __init__(self,dtgopt,modelopt,basinopt,stcgbdir,
                 taids=None,
                 verb=0,warn=1,
                 trktype='tcgen'):

        #from w2 import SetLandFrac
        #from w2 import GetLandFrac

        self.lf=w2.SetLandFrac()
        self.getlf=w2.GetLandFrac

        self.tdtgs=dtgs=mf.dtg_dtgopt_prc(dtgopt,ddtg=6)

        if( (taids != None) and (type(taids) is not(ListType)) ):
            taids=[taids]


        self.basins=basinopt.split(',')
        self.models=modelopt.split(',')
        self.stcgbdir=stcgbdir
        self.trktype=trktype

        self.dtgopt=dtgopt
        self.taids=taids
        self.verb=verb
        self.warn=warn

        self.initVars()
        self.initAdeckPaths()
        self.initAdeck()

        del self.lf
        del self.getlf

    def initAdeckPaths(self):
        
        """ use zip file to pull in adeck cards
"""

        bcards={}
        basins=[]

        adpaths=[]
        genprops={}

        for dtg in self.tdtgs:
            yyyy=dtg[0:4]
            yyyymm=dtg[0:6]
            zipPath="%s/%s/tmtrkN-%s.zip"%(self.stcgbdir,yyyy,yyyymm)
            rc=MF.ChkPath(zipPath)
            if(rc == 0):
                print 'WWW-AdeckGen2.initAdeckPathsZip zipPath: ',zipPath,' not there sayounara...press...'
                self.basins=basins
                self.bcards=bcards
                self.adecks=adpaths
                return
                
            AZ=zipfile.ZipFile(zipPath)
            zls=AZ.namelist()

            for model in self.models:
                
                for basin in self.basins:
                
                    adpath="%s/%s.sink.%s.%s.%s.txt"%(dtg,self.trktype,basin,dtg,model)

                    # -- get adeck if in zip archives
                    #
                    if(adpath in zls):
                        
                        (adir,afile)=os.path.split(adpath)
                        tt=afile.split('.')
                        if(len(tt) == 6):
                            prop=(tt[2],tt[3],tt[4])

                        basin=prop[0]
                        basin.lower()
                        basins.append(basin)
            
                        adeck=AZ.open(adpath).readlines()
                        self.addList2DictList(bcards,basin,adeck)
                        adpaths.append(adpath)

                    else:
                        print 'not there...press...'


            
            basins=self.uniq(basins)
            
            self.basins=basins
            self.bcards=bcards
            self.adecks=adpaths



    def initAdeckPathsOrig(self):

        bcards={}
        cards=[]
        basins=[]


        adecks=[]
        oadecks=[]

        for dtg in self.tdtgs:

            for model in self.models:
                sdir="%s/%s/%s"%(self.stcgbdir,dtg,model)
                if(mf.find(self.stcgbdir,'adeck')): sdir="%s/%s/%s"%(self.stcgbdir,dtg[0:4],dtg)
                for basin in self.basins:
                    admask="%s/%s.sink.%s.%s.%s.txt"%(sdir,self.trktype,basin,dtg,model)
                    print 'GGGG(AdeckGen2.initAdeckPaths.admask): ',admask
                    adecks=adecks+glob.glob(admask)
                    if(self.verb): print 'adecks(tcgen): ',adecks

            for adeck in adecks:
                try:
                    siz=os.path.getsize(adeck)
                    if(siz > 0): oadecks.append(adeck)
                except:
                    print 'WWW(AdeckGen2.initAdeckPaths) noadeck for ',adeck
                    continue


        for adeck in oadecks:

            genprops={}
            (dir,file)=os.path.split(adeck)
            tt=file.split('.')
            if(len(tt) == 6):
                prop=(tt[2],tt[3],tt[4])
                genprops[adeck]=prop


            prop=genprops[adeck]
            basin=prop[0]
            basin.lower()
            basins.append(basin)

            try:
                ttt=open(adeck).readlines()
            except:
                ttt=None

            if(cards is None):
                return
            else:
                cards=cards+ttt

            self.addList2DictList(bcards,basin,cards)

        basins=self.uniq(basins)

        self.basins=basins
        self.bcards=bcards
        self.adecks=oadecks

def makeAdeckGens2(dtgopt,modelopt,basinopt,stcgbdir,taids=None,verb=0):
    """ instantiate AdeckGen(Adeck) class"""
    A=AdeckGen2(dtgopt,modelopt,basinopt,stcgbdir,verb=verb)
    return(A)




class AdeckGenTctrk2(AdeckGenTctrk):

    def __init__(self,tcD,dtgopt,modelopt,stcgbdir,
                 mD=None,taids=None,
                 verb=0,warn=1,
                 aliases=None,
                 trktype='tctrk',
                 atcftype='sink',
                 ):

        # -- land/sea flag
        #from w2 import SetLandFrac
        #from w2 import GetLandFrac
        self.lf=w2.SetLandFrac()
        self.getlf=w2.GetLandFrac

        self.tcD=tcD

        self.dtgopt=dtgopt
        self.tdtgs=mf.dtg_dtgopt_prc(dtgopt,ddtg=6)
        self.models=modelopt.split(',')
        self.stcgbdir=stcgbdir
        self.mD=mD
        self.taids=taids
        self.verb=verb
        self.warn=warn
        self.aliases=aliases
        self.trktype=trktype
        self.atcftype=atcftype

        self.initVars()
        self.initAdeckPaths()
        self.initAdeck()



    def initAdeckPathsOrig(self):

        adecks=[]
        oadecks=[]

        for dtg in self.tdtgs:
            year=dtg[0:4]
            sdir="%s/esrl/%s"%(AdeckBaseDir,year)
            sdir="%s/%s"%(self.stcgbdir,dtg)
            if(mf.find(self.stcgbdir,'adeck')): sdir="%s/%s/%s"%(self.stcgbdir,dtg[0:4],dtg)

            for model in self.models:
                admask="%s/w2flds/%s.%s.%s.%s.txt"%(sdir,self.trktype,self.atcftype,dtg,model)
                admask="%s/%s/%s.%s.%s.%s.txt"%(sdir,model,self.trktype,self.atcftype,dtg,model)
                if(mf.find(self.stcgbdir,'adeck')): 
                    admask="%s/%s.%s.%s.*%s.txt"%(sdir,self.trktype,self.atcftype,dtg,model)
                print 'TTTT(admask): ',admask
                adecks=adecks+glob.glob(admask)
                if(self.verb): print 'adecks(tctrk): ',adecks

            if(len(adecks) == 0):
                print 'WWW(AdeckGenTctrk2.initAdeckPaths) noadecks admask: ',admask

            for adeck in adecks:
                try:
                    siz=os.path.getsize(adeck)
                    if(siz > 0): oadecks.append(adeck)
                except:
                    continue

        cards=[]
        for adeck in oadecks:
            try:
                ttt=open(adeck).readlines()
            except:
                ttt=None

            if(ttt is None):
                continue
            else:
                cards=cards+ttt
                
        # -- remove genesis tracks ('tg') basin, suppose to be for tctrk.sink
        #
        cards=self.filterTGcards(cards)
        self.cards=cards

    def initAdeckPaths(self):
        """ zip form of getting the full adeck ... a lot easier
"""
        # -- inialize cards...if none are there...
        #
        cards=[]
        
        for dtg in self.tdtgs:
            yyyy=dtg[0:4]
            yyyymm=dtg[0:6]
            zipPath="%s/%s/tmtrkN-%s.zip"%(self.stcgbdir,yyyy,yyyymm)
            rc=MF.ChkPath(zipPath)
            if(rc == 0):
                print 'WWW-AdeckGen2.initAdeckPathsZip zipPath: ',zipPath,' not there sayounara...press...'
                self.cards=cards
                return
                
            AZ=zipfile.ZipFile(zipPath)
            zls=AZ.namelist()
            
            if(self.verb):
                for zl in zls:
                    if(mf.find(zl,dtg)):
                        print zl

            for model in self.models:
                
                adpath="%s/%s.%s.%s.%s.txt"%(dtg,self.trktype,self.atcftype,dtg,model)

                # -- get adeck if in zip archives
                #
                if(adpath in zls):
                    cards=AZ.open(adpath).readlines()
                else:
                    print 'not there...press...'

        # -- remove genesis tracks ('tg') basin, suppose to be for tctrk.sink
        #
        cards=self.filterTGcards(cards)
        self.cards=cards

    def filterTGcards(self,cards):
        ocards=[]
        for card in cards:
            b2id=card.split(',')[0].strip().lower()
            if(b2id == 'tg'):
                continue
            else:
                ocards.append(card)

        return(ocards)

    def getStmidDtg(self,dtg,dupchk=0):
        (otrk,genstmids)=self.tcD.getTCtrkDtg(dtg,dobt=0,verb=0,dupchk=1)
        stmids=otrk.keys()
        return(stmids)


    def getStmidFrom3id(self,snum,dtg):
        stmid=self.tcD.getStmidFrom3id(snum,dtg)
        return(stmid)

    def getDtg(self,dtg,dupchk=1):
        (astmids,abtcs)=self.tcD.getDtg(dtg,dupchk=dupchk)
        return(astmids,abtcs)


    def getsTDd(self,trk,endtau,dtau=12,vmaxTD=25.0,vmaxMin=10.0):

        minvmax=1e20
        maxvmax=-1e20

        taus=trk.keys()
        taus.sort()

        try:
            trkttau=trk[endtau]
            ntaus=taus.index(endtau)+1
        except:
            trkttau=trk[taus[-1]]
            ntaus=len(taus)

        if(len(taus) == 1):
            vmax=trk[taus[0]][2]
            if(vmax < 0): vmax=vmaxMin
            stdd=(vmax/vmaxTD)
            stddtime=dtau*0.5
            minvmax=maxvmax=vmax
        else:
            stdd=0.0
            stddtime=0.0
            for n in range(1,ntaus):
                taum1=taus[n-1]
                taum0=taus[n]
                vmaxm1=trk[taum1][2]
                vmaxm0=trk[taum0][2]
                if(vmaxm1 < 0): vmaxm1=vmaxMin
                if(vmaxm0 < 0): vmaxm0=vmaxMin

                if(vmaxm1 > maxvmax): maxvmax=vmaxm1
                if(vmaxm1 < minvmax): minvmax=vmaxm1
                if(vmaxm0 > maxvmax): maxvmax=vmaxm0
                if(vmaxm0 < minvmax): minvmax=vmaxm0

                stdd=stdd+((vmaxm1+vmaxm0)*0.5)/vmaxTD
                stddtime=stddtime+(taum0-taum1)

        sTDd=(stdd*(dtau/24.0),stddtime,trkttau[0],trkttau[1],trkttau[2],minvmax,maxvmax)


        return(sTDd)

def makeAdeckGensTctrk2(tcD,dtgopt,modelopt,stcgbdir,taids=None,verb=0):
    """ instantiate AdeckGenTctrk(AdeckGen) class"""
    A=AdeckGenTctrk2(tcD,dtgopt,modelopt,stcgbdir,verb=verb)

    # -- do map between adeck stmids and bt stmids
    #
    A.mapAidStmid2BtStmid(verb=verb)

    A.relabelAidtrks()
    del A.tcD

    return(A)




class Tcgen(MFbase):

    distMinTC={
        0: 2.0*60.0,
        12: 3.0*60.0,
        24: 4.0*60.0,
        36: 4.5*60.0,
        48: 5.0*60.0,
        60: 5.5*60.0,
        72: 6.0*60.0,
        84: 6.5*60.0,
        96: 7.0*60.0,
        108: 7.5*60.0,
        120: 8.0*60.0,
        132: 9.0*60.0,
        144:10.0*60.0,
        168:10.0*60.0,
    }

    maxLatGenTc=40.0
    doTau120Rtfim9=0


    def __init__(self,
                 tcGP,
                 tcD,
                 iV,
                 tcB,
                 prB,
                 model,
                 basin,
                 dtg,
                 gentau,

                 dogendtg,
                 stcgbdir,  # source bdir for tcgen
                 omodelPlot=None,

                 # -- five settings orginially in gtc; now tcgen() is self contained
                 # -- does not use global vars from main
                 
                 tau0=0,
                 fcdtau=12,
                 landmax=0.5,
                 distminG0=180.0,
                 mintauFC=12,

                 verb=0,
                 diag=0,
                 override=0,
                 bypassTrkchk=0,
                 
                 overrideGA=0,
                 

                 ):


        # -- tc and model analysis cyclones
        """

"""

        # -- objs
        #
        self.tcGP=tcGP
        self.gaP=self.tcGP.gaP
            
        self.tcD=tcD
        self.iV=iV
        self.tcB=tcB
        self.prB=prB

        from M2 import setModel2

        # -- vars
        #
        self.model=model
        self.basin=basin
        self.dtg=dtg
        self.gentau=gentau
        self.dogendtg=dogendtg

        self.stcgbdir=stcgbdir
        self.omodelPlot=omodelPlot

        self.tau0=tau0
        self.fcdtau=fcdtau
        self.landmax=landmax
        self.distminG0=distminG0
        self.mintauFC=mintauFC
        
        self.verb=verb
        self.diag=diag
        self.override=override
        self.overrideGA=overrideGA

        self.xsize=tcGP.xsize
        self.ysize=tcGP.ysize

        self.bypassTrkchk=bypassTrkchk

        self.gentype='fcst'
        if(self.dogendtg):  self.gentype='veri'

        self.bdtg=dtg

        if(self.dogendtg):
            self.bdtg=mf.dtginc(self.dtg,-gentau)

        self.vdtg=mf.dtginc(self.bdtg,gentau)

        (ctlpath,taus,nfields,tauOffset)=w2.getCtlpathTaus(model,self.bdtg)

        self.ctlpath=ctlpath
        self.taus=taus

        self.datathere=1
        self.done=0
        self.bypass=0

        # -- check if data...
        #

        if(self.ctlpath == None):
            self.datathere=0
            print 'WWW(Tcgen) datathere = ',self.datathere,' for ctlpath: ',self.ctlpath
            if(overrideGA):
                None
            else:
                return

        # -- set m2 object and check if already done
        #
        self.m2=setModel2(model)

        if(self.isInInv() and not(override or overrideGA)):
            print 'III(Tcgen) already done... ',model,basin,'bdtg,vdtg: ',self.bdtg,self.vdtg,'gentau: ',gentau,'dogendtg: ',self.dogendtg
            self.done=1
            return

        # -- if bypassing by track then get this object and if there are no tcgen adecks bypass=1 in w2-tc-tcgen2.py
        #
        if(bypassTrkchk == 0):
            gtG=makeAdeckGens2(self.bdtg,self.model,self.basin,self.stcgbdir,verb=verb)
            if(len(gtG.adecks) == 0):
                self.bypass=1
                return

        


    def setTCgenProps(self,gentau,dogendtg,verb=0,dupchk=1):

        def getMaxTau(tG):
            maxtau=-999
            alltaus=[]
            kk=tG.aidtaus.keys()
            for k in kk:
                dicttaus=tG.aidtaus[k]
                jj=dicttaus.keys()
                for j in jj:
                    taus=dicttaus[j]
                    alltaus=alltaus+taus
                    
            alltaus=mf.uniq(alltaus)
            
            if(len(alltaus) == 0): 
                maxtau=0
            else:
                maxtau=max(alltaus)
            
            return(maxtau)
        

        tcState={}
        modtc0={}
        modALL={}        # -- all model here

        
        print
        print 'BBBBBB setTCgenProps ------------------- bdtg:',self.bdtg,'  vdtg:',self.vdtg,self.dogendtg

        if(verb):
            print 'doing: ',self.model,self.basin,self.bdtg,self.gentau
            print


        #oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
        # -- TCs -- 9X and NN at verifying dtg if dogendtg otherwise for forecasting use bdtg 
        #
        tcdtg=self.bdtg
        if(self.dogendtg): tcdtg=self.vdtg

        # -- set dobt=0 to get 9X -- changed the interface in tcbase.TcData
        #
        (otrk,genstmids)=self.tcD.getTCtrkDtg(tcdtg,dobt=0,dupchk=dupchk,verb=verb,
                                         renameSubbasin=1)
        if(verb): self.tcD.lsDSsDtgs(self.dtg,dupchk=dupchk)

        # -- gentau
        #
        stmids=otrk.keys()

        for stmid in stmids:
            oo=otrk[stmid]
            (blat,blon,bvmax,bpmin,bdir,bspd,btccode)=oo.getposit()
            isIn=self.tcB.isLLin(blat,blon,doTC=1)
            if(isIn):

                tcState[stmid]=('NT',oo.getposit())

                if(stmid in genstmids):
                    tcState[stmid]=('GN',oo.getposit())
                else:
                    if(IsTc(btccode)):
                        if(IsNN(stmid)):
                            tcState[stmid]=('NN',oo.getposit())
                        elif(Is9X(stmid)):
                            tcState[stmid]=('PTC',oo.getposit())
                    else:
                        if(IsNN(stmid)):
                            tcState[stmid]=('NT',oo.getposit())
                        elif(Is9X(stmid)):
                            tcState[stmid]=('PTC',oo.getposit())

                if(verb): print 'FFF:   TC:',self.basin,gentau,self.vdtg,stmid,btccode,tcState[stmid][0],'istc/NN/9X: ',IsTc(btccode),IsNN(stmid),Is9X(stmid)


        #mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
        # -- model
        # -- genesis track objects for verifying self.vdtg (gentau) and the forecast
        #
        gt0=makeAdeckGens2(self.vdtg,self.model,self.basin,self.stcgbdir,verb=verb)
        gtG=makeAdeckGens2(self.bdtg,self.model,self.basin,self.stcgbdir,verb=verb)
        
        gstmids=gtG.aids
        
        # -- get max tau for genesis tracks
        #
        maxtauG=getMaxTau(gtG)
        
        if(len(gtG.adecks) == 0):
            print 'IIIII 0000000 no genesis tracks ',self.model,self.basin,self.dtg,self.gentau,self.dogendtg
            print 'EEEEE need to run tmtrkN for model: ',self.model,' bdtg: ',self.bdtg,' basin: ',self.basin
            self.gt0=None
            self.gtG=None
            self.ftG=None
            self.ntcALL=0
            self.nmodALL=0
            self.nmodtc0=0
            self.modALL=None
            self.modtc0=None
            self.finalModelState={}
            self.tcState=tcState
            self.done=-999
            return


        # -- get the tau0 genesis tracks and std: look for non 9X/NN cyclones...
        #
        gtrk0=gt0.gettrks(self.basin,self.vdtg,self.tau0,dtau=self.fcdtau)
        gstd0=gt0.getsTDds(self.basin,self.vdtg,self.tau0,dtau=self.fcdtau)

        for stmid in gtrk0.keys():
            iposit=gtrk0[stmid]
            (rlat,rlon,vmax,pmin,alf,poci,roci,rmax,dir,spd,cpsB,cpsVTu,cpsVTl,z8mean,z8max,z7mean,z7max)=iposit[self.tau0]
            isIn=self.tcB.isLLin(rlat,rlon)

            if(isIn and stmid[0:2] == 'tg' and self.tcB.isLatTropical(rlat,dtg=self.bdtg) ):

                gstd=gstd0[stmid][0]
                if(verb): print '0000(bbbb): ',stmid,rlat,rlon,vmax,': %4.2f'%(alf),poci,roci,gstd
                
                # -- land check if mostly over h2o -- call it a non NN/9X system
                #
                if(alf < self.landmax):
                    (clat,clon)=Rlatlon2Clatlon(rlat,rlon,dodec=1)
                    if(verb): print '0000(!!!!): ',stmid,clat,clon,vmax,alf,self.landmax

                    # -- get the forecast track and require the canidate exist for >= mintauFC
                    gtrk0A=gt0.gettrks(self.basin,self.vdtg,dtau=6)
                    taus=gtrk0A[stmid].keys()
                    taus.sort()
                    lasttau=taus[-1]
                    if(lasttau >= self.mintauFC):
                        modtc0[stmid]=(rlat,rlon,vmax,pmin,poci,roci,gstd,lasttau)


        # -- stm forecast track objects from tctrk.sink vice tctrk.atcf
        #
        ftG=makeAdeckGensTctrk2(self.tcD,self.bdtg,self.model,self.stcgbdir,verb=verb)

        # -- get max tau for genesis tracks
        #
        maxtauF=getMaxTau(ftG)
        
        maxtauTrackers=max(maxtauF,maxtauG)

        self.maxtauTrackers=maxtauTrackers
        
        # -- check if there is a deterministic track
        #
        skipftG=0
        if(len(ftG.aids) == 0):
            skipftG=1
            self.amodel=ftG.models[0]

        # -- get the model tc forecast tracks
        #
        gentauPeriod=36
        dgentau=12
        gentaus=range(gentau-gentauPeriod,gentau+1,dgentau)

        ftrkG=None
        if(not(skipftG)):
            self.amodel=ftG.aids[0]

            # -- get the model tc forecast tracks
            #
            for gtau in gentaus:

                ftrkG=ftG.gettrks(self.bdtg,endtau=gtau)

                for stmid in ftrkG.keys():
                    isNNTC=IsNN(stmid)
                    iposit=ftrkG[stmid]
                    try:
                        (rlat,rlon,vmax,pmin,alf,poci,roci,rmax,dir,spd,cpsB,cpsVTu,cpsVTl,z8mean,z8max,z7mean,z7max)=iposit[gtau]
                    except:
                        rlat=None

                    if(rlat is not None):
                        isIn=self.tcB.isLLin(rlat,rlon,doTC=1)
                        isTrop=self.tcB.isLatTropical(rlat,dtg=self.bdtg)
                        if(verb and isIn):
                            print 'FFF(bbbbbbbbbbbbbb): ',stmid,rlat,rlon,'alf: %4.2f'%(alf),\
                                  ' vmax: ',vmax,' gentau: ',gtau,' isTrop: ',isTrop,' isNNTC: ',isNNTC
                            
                        # -- make sure over H20 
                        # -- not for 'fc' tracks
                        # -- always accept NN storms
                        alf=0.0
                        if(isIn and alf < self.landmax and (isTrop or isNNTC) ):
                            istd=ftG.getsTDd(ftrkG[stmid],endtau=gtau)
                            MF.appendDictList(modALL,stmid,(gtau,iposit,'fc','xxx',istd))
                            if(verb): print 'FFFF(!!!!--keeping): ',stmid,rlat,rlon,vmax,'alf: %4.2f'%(alf)



        # -- get genesis tracks at verifying time and tracks to the verifying tau
        #
        for gtau in gentaus:

            gtrkG=gtG.gettrks(self.basin,self.bdtg,gtau,dtau=self.fcdtau)

            # -- get genesis std
            #
            gstdG=gtG.getsTDds(self.basin,self.bdtg,gtau,dtau=self.fcdtau)
            
            for stmid in gtrkG.keys():
                
                dogstm=0
                if(stmid[0:2] == 'tg'): dogstm=1
                
                # convert to NN stmorm in tcgen to normal form
                #
                if(stmid[0:2] != 'tg' and len(stmid) == 5):
                    year=self.bdtg[0:4]
                    gstmid=stmid[2:].upper()+'.'+year
                    gtaus=gtrkG[stmid].keys()
                    gtaus.sort()
                    
                    if(ftrkG == None): continue
                    
                    fstmids=ftrkG.keys()
                    if(gstmid in fstmids):
                        ftaus=ftrkG[gstmid].keys()
                        ftaus.sort()
                        if(gtaus[-1] > ftaus[-1]): dogstm=2
                    
                iposit=gtrkG[stmid]
                istd=gstdG[stmid]

                try:
                    (rlat,rlon,vmax,pmin,alf,poci,roci,rmax,dir,spd,cpsB,cpsVTu,cpsVTl,z8mean,z8max,z7mean,z7max)=iposit[gtau]
                except:
                    rlat=None

                
                if(rlat is not None):
                    
                    isIn=self.tcB.isLLin(rlat,rlon,doTC=1)

                    if(verb): print'GGGG(0000): ',stmid,rlat,rlon,alf,'std: ',istd[0],iposit.keys(),' gentau: ',gtau,' dogstm: ',dogstm
                    
                    # -- filter out non 'tg' storms and NN storms in gtrkG with less taus than ftrkG
                    #
                    if(isIn and dogstm == 1):
                        if(verb): print 'GGGG(bbbb): ',stmid,rlat,rlon,alf,'std: ',istd[0],iposit.keys(),' gentau: ',gtau
                        
                        # -- make sure over H20
                        #
                        if(alf < self.landmax and self.tcB.isLatTropical(rlat,dtg=self.bdtg,override=1)):
                            (clat,clon)=Rlatlon2Clatlon(rlat,rlon,dodec=1)
                            if(verb): print 'GGGG(!!!!--keeping): ',stmid,clat,clon,vmax,alf,self.landmax,'gentau: ',gtau ; print
                            MF.appendDictList(modALL,stmid,(gtau,iposit,'tg','xxx',istd))

                    # -- NN trackers in gentracker output that has more taus than in tctracker
                    #
                    elif(isIn and dogstm == 2):
                        
                        if(verb): print 'FFGG(bbbb): ',stmid,rlat,rlon,alf,'std: ',istd[0],iposit.keys(),' gentau: ',gtau
                        
                        # -- make sure over H20 
                        # -- not for 'fc' tracks
                        alf=0.0
                        #if(isIn and alf < landmax and tcB.isLatTropical(rlat,dtg=self.bdtg) ):
                        if(isIn and alf < self.landmax):
                            MF.appendDictList(modALL,gstmid,(gtau,iposit,'fc','xxx',istd))
                            if(verb): print 'FFGG(!!!!--keeping): ',gstmid,rlat,rlon,vmax,'alf: %4.2f'%(alf)
                            
                            # -- replace the existing ft trk with one genesis tracker
                            #
                            (ftmodel,ftstm)=ftG.aidtrks.keys()[0]
                            
                            ftG.aidtrks[ftmodel,gstmid]=gtG.aidtrks[stmid,self.basin]
                            ftG.aidtaus[ftmodel,gstmid]=gtG.aidtaus[stmid,self.basin]
                            
                            




            # -- now comp these model tau0 storms against real 9X/NN
            #
            if(len(modtc0) > 0):

                tc0final={}
                for mstmid in modtc0.keys():
                    (glat,glon)=modtc0[mstmid][0:2]
                    gotit=1
                    for ostmid in tcState.keys():
                        tc0=tcState[ostmid][1]
                        (olat,olon)=tc0[0:2]
                        gdist=gc_dist(olat,olon,glat,glon)
                        if(gdist <= self.distminG0):
                            gotit=0
                            if(verb): print 'GGGG(000000000000000000): ',mstmid,glat,glon
                            if(verb): print 'GGGG(0000 !!!!--keeping): ',ostmid,olat,olon,' model: ',mstmid,glat,glon,'gdist: ',gdist
                    if(gotit):
                        tc0final[mstmid]=modtc0[mstmid]

                modtc0=tc0final


        #  check for dups
        #
        mAkeys=modALL.keys()
        mAkeys.sort()
        nmodALL=len(modALL.keys())
        
        diffbarMin=1.0   # deg lat of minimum separation
        pcommonMin=50.0  # min percent of common taus
        
        mAkeep={}
        for i in range(0,nmodALL):
            stmid0=mAkeys[i]
            mAkeep[stmid0]=1
        
        for i in range(0,nmodALL):
            ii=i+1
            
            for ii in range(ii,nmodALL):
                
                stmid0=mAkeys[i]
                stmid1=mAkeys[ii]
                
                m0=modALL[stmid0]
                m1=modALL[stmid1]

                trk0={}
                trk1={}
                
                gtaus0=[]
                gtaus1=[]
                gtaus=[]
                for m in m0:
                    gtau0=m[0]
                    trk0[gtau0]=m[1][gtau0][0:4]
                    gtaus.append(gtau0)
                    gtaus0.append(gtau0)
                    
                for m in m1:
                    gtau1=m[0]
                    trk1[gtau1]=m[1][gtau1][0:4]
                    gtaus.append(gtau1)
                    gtaus1.append(gtau1)
                    
                gtaus=mf.uniq(gtaus)
                
                diffbar=0.0
                ndiff=0
                
                gtau0max=gtaus0[-1]
                gtau1max=gtaus1[-1]

                for gtau in gtaus:
                    try:
                        p0=trk0[gtau]
                        p1=trk1[gtau]
                        dy=p0[0]-p1[0]
                        dx=p0[1]-p1[1]
                        diff=sqrt(dx*dx+dy*dy)
                        diffbar=diffbar+diff
                        ndiff=ndiff+1
                    except:
                        None
                        
                if(ndiff == 0):
                    ### - not really useful -- print 'WWW in setTCgenProps Dup check 0 length track for stmid0: ',stmid0,' stmid1: ',stmid1
                    continue

                ngtaus=len(gtaus)
                
                pcommon=(float(ndiff)/float(ngtaus))*100.0
                
                diffbar=diffbar/ndiff

                # -- 20160815 -- new feature -- require the two tracks have > 50% of taus in common...
                #
                if(verb): print 'DDD---check: stmid0,stmid1,diffbar,ndiff,pcommon: ',\
                  stmid0,len(gtaus0),stmid1,len(gtaus1),diffbar,ndiff,pcommon,' model/basin: ',self.model,self.basin,'gentau: ',self.gentau
                
                if(diffbar <= diffbarMin and pcommon >= pcommonMin):
                    
                    type0='tc'
                    if(stmid0[0:2] == 'tg'): type0='gen'

                    type1='tc'
                    if(stmid1[0:2] == 'tg'): type1='gen'
                    
                    if(type0 == 'tc' and type1 == 'gen'): 
                        mAkeep[stmid0]=1
                        mAkeep[stmid1]=0
                    elif(type0 == 'gen' and type1 == 'tc'): 
                        mAkeep[stmid0]=0
                        mAkeep[stmid1]=1
                    elif(len(gtaus0) >= len(gtaus1)):
                        mAkeep[stmid0]=0
                        mAkeep[stmid1]=1                            
                    else:
                        mAkeep[stmid0]=1
                        mAkeep[stmid1]=0                            


                    print 'DD'
                    pcard='DDD--------(setTCgenProps) have a dup between %8s %3s %2d'%(stmid0,type0,len(gtaus0)) + \
                        ' and %8s %3s %2d'%(stmid1,type1,len(gtaus1)) + \
                        ' model/basin: %s/%s'%(self.model,self.basin) + ' gentau: %3d'%(self.gentau)
                    if(mAkeep[stmid0]): pcard=pcard + ' ---(keeping): %8s %3d'%(stmid0,len(gtaus0))
                    if(mAkeep[stmid1]): pcard=pcard + ' ---(keeping): %8s %3d'%(stmid1,len(gtaus0))
                    print pcard
                    print 'DD'
                        
                    
        modALLFinal={}
        
        for i in range(0,nmodALL):
            stmid0=mAkeys[i]
            rc=IsValidStmid(stmid0)
            if(not(IsValidStmid(stmid0))): 
                print 'WWW not keeping stmid0: ',stmid0
                continue
            if(mAkeep[stmid0]): modALLFinal[stmid0]=modALL[stmid0]
            
        modALL=modALLFinal
        
        ntcALL=len(tcState.keys())
        nmodALL=len(modALL.keys())
        nmodtc0=len(modtc0.keys())
        
        if(verb and len(modtc0.keys()) > 0 ): print '00000 model Analyzed TCs'
        for stmid in modtc0.keys():
            (rlat,rlon,vmax,pmin,poci,roci,gstd,lasttau)=modtc0[stmid]
            (clat,clon)=Rlatlon2Clatlon(rlat,rlon,dodec=1)
            if(verb): print '00000 modtc0: %10s'%(stmid),' posit: ',clat,clon,vmax,gstd,self.vdtg,lasttau,'taus:',modtc0[stmid]
            
        if(verb and len(modtc0.keys()) > 0 ): print


        if(verb):

            for stmid in modALL.keys():
                modalls=modALL[stmid]
                for n in range(0,len(modalls)):
                    modall=modalls[n]
                    gtau=modall[0]
                    rc=self.isGenTC(stmid,modall[1])
                    taus=modall[1].keys()
                    taus.sort()
                    print 'modALL: %11s'%(stmid),'gentau: %3d'%(gtau),' taus: %50s'%str(taus),' isGenTc: ',rc,modall[2],' sTDd: ',modall[4]
                    lstaus=0
                    if(lstaus):
                        for tau in taus:
                            rc=modall[1][tau][0:3]
                            print stmid,tau,rc
            print

            for stmid in tcState.keys():
                tt=tcState[stmid]
                print 'tcState: %10s %3s %5.1f %6.1f'%(stmid,tt[0],tt[1][0],tt[1][1])
            
            print

            suffix=''
        if(nmodtc0 > 0): suffix='MMMMMMMMMMMMMM model tau0 cyclone?'
        if(verb): print 'NNNNNNNNNNN: ',self.model,self.basin,gentau,'  tcALL(N): ',ntcALL,' modtc0(N): ',nmodtc0,' modALL(N): ',nmodALL,suffix

        # -- use tau120 for 132 for fim9
        if(self.doTau120Rtfim9 and self.model == 'rtfim9' and gentau == 132 and self.maxtauTrackers <= 120 ): gentau=120

        self.gt0=gt0
        self.gtG=gtG
        self.ftG=ftG
        self.ntcALL=ntcALL
        self.nmodALL=nmodALL
        self.nmodtc0=nmodtc0
        self.modALL=modALL
        self.modtc0=modtc0
        self.tcState=tcState

        print 'EEEEEE setTCgenProps ------------------- bdtg:',self.bdtg,'  vdtg:',self.vdtg,self.dogendtg
        print

    def compMtoO(self,bdtg,gentau,dogendtg,verb=0):

        #print 'CCCCCCCCCCCCCC dogendtg: %d  gentau: %d'%(dogendtg,gentau)
        #print

        print 'BBBBBB compMtoO      ------------------- bdtg:',self.bdtg,'  vdtg:',self.vdtg,dogendtg

        finalModelState={}

        # -- use tau120 for 132 for fim9
        if(self.doTau120Rtfim9 and self.model == 'rtfim9' and gentau == 132 and self.maxtauTrackers <= 120 ): gentau=120

        distmin=self.distMinTC[gentau]

        modALL=self.modALL
        tcState=self.tcState
        modtc0=self.modtc0

        for mstmid in modALL.keys():

            mtrks=modALL[mstmid]

            if(verb):
                print
                print 'ccc000              ',mstmid,len(mtrks)

            for mtrk in mtrks:

                gothit=[]

                (gtau,iposit,mstate,mcode,mstd)=mtrk
                mstate=(mstate,mcode,mstd)
                mposit=iposit[gtau]
                if(verb): print 'ccc111              ',mstmid,gtau,mstate,mposit
                
                # -- comp to known TCs
                #
                
                # -- first find min distance between storms
                #
                minDistTCs={}
                
                for ostmid in self.tcState.keys():
                    ostate=tcState[ostmid][0]
                    tcob=tcState[ostmid][1]
                    (olat,olon)=tcob[0:2]
                    
                    mindist=1e20
                    for tstmid in self.tcState.keys():
                        
                        if(tstmid != ostmid):
                            tstate=tcState[tstmid][0]
                            tcob=tcState[tstmid][1]
                            (tlat,tlon)=tcob[0:2]
                            gdist=gc_dist(olat,olon,tlat,tlon)
                            if(gdist < mindist): mindist=gdist
                    
                    minDistTCs[ostmid]=mindist
                        
                    
                
                for ostmid in self.tcState.keys():

                    ostate=tcState[ostmid][0]
                    tcob=tcState[ostmid][1]
                    (olat,olon)=tcob[0:2]
                    
                    try:
                        (mlat,mlon)=mposit[0:2]
                    except:
                        print 'WWWWWWWWWWWWWWWWWWWWWWWWW no model lat,lon for mstmid: ',mstmid,' gentau: ',gentau
                        continue

                    (oclat,oclon)=Rlatlon2Clatlon(olat,olon,dodec=1)
                    (mclat,mclon)=Rlatlon2Clatlon(mlat,mlon,dodec=1)
                    gdist=gc_dist(olat,olon,mlat,mlon)
                    if(gdist <= distmin or                             #
                       # relax condition if model a forecast and is less than distance to nearest storm...
                       (mstate[0] == 'fc' and gdist <= minDistTCs[ostmid]) or
                       # -- just force it to accept if forecast and model stmid = obs stmid
                       (mstate[0] == 'fc' and (ostmid == mstmid) )
                       ):
                        gothit.append((ostmid,ostate,gdist,olat,olon,mstate))

                    if(verb): print 'ccc222               O: %8s M: %8s'%(ostmid,mstmid),'O:',oclat,oclon,'M:',\
                      mclat,mclon,"gdist: %5.0f distmin: %5.0f"%(gdist,distmin),ostate,mstate,minDistTCs[ostmid]


                # -- comp to model tau0 storms
                #
                for ostmid in modtc0.keys():
                    
                    ostate='MTC'
                    (olat,olon)=modtc0[ostmid][0:2]

                    try:
                        (mlat,mlon)=mposit[0:2]
                    except:
                        print 'WWWWWWWWWWWWWWWWWWWWWWWWW no model lat,lon for mstmid: ',mstmid,' gentau: ',gentau,' MMMMMMMModel tau 0 TC'
                        continue
                    
                    (oclat,oclon)=Rlatlon2Clatlon(olat,olon,dodec=1)
                    (mclat,mclon)=Rlatlon2Clatlon(mlat,mlon,dodec=1)
                    gdist=gc_dist(olat,olon,mlat,mlon)                    
                    if(gdist <= distmin): gothit.append((ostmid,ostate,gdist,olat,olon,mstate))
                    
                    if(verb): print 'ccc333-model tau0 TC O: %8s M: %8s'%(ostmid,mstmid),\
                      'O:',oclat,oclon,'M:',mclat,mclon,"gdist: %5.0f distmin: %5.0f"%(gdist,distmin),ostate,mstate


                # -- now see how many hits we got; hopefully just one per tc
                #
                if(dogendtg):
                    fmstate=self.setModelStateGen(mstmid,iposit,mposit,gothit,mstate)
                else:
                    fmstate=self.setModelStateFc(mstmid,iposit,mposit,mstate)

                # -- case of 7X storms...
                #
                if(fmstate == None): continue


                # -- output
                #
                (mlat,mlon)=fmstate[3][0:2]
                (mclat,mclon)=Rlatlon2Clatlon(mlat,mlon,dodec=1)
                (stdd,stlen)=fmstate[2][0:2]

                try:
                    (olat,olon)=fmstate[4]
                    (oclat,oclon)=Rlatlon2Clatlon(olat,olon,dodec=1)
                except:
                    (olat,olon)=(999.,999.)
                    (oclat,oclon)=('99999','999999')

            gvdtg=mf.dtginc(bdtg,gtau)
            print "FFFFinal(dogentg): %d -- gentau: %3d  gtau: %3d vdtg: %s"%(dogendtg,gentau,gtau,gvdtg),\
                  "%10s  %3s  sd: %4.1f  sdlen: %5.1f  M: %5.1f %5.1f  O: %5.1f  %5.1f"%(mstmid,fmstate[1],stdd,stlen,mlat,mlon,olat,olon)

            if(len(fmstate) == 6): 
                finalModelState[mstmid]=(gtau,fmstate[1],stdd,stlen,mlat,mlon,olat,olon,fmstate[-1])
            else:
                finalModelState[mstmid]=(gtau,fmstate[1],stdd,stlen,mlat,mlon,olat,olon)

        if(len(tcState.keys()) > 0):
            print
            for stmid in tcState.keys():
                tt=tcState[stmid]
                print 'tcState: %10s %3s %5.1f %6.1f'%(stmid,tt[0],tt[1][0],tt[1][1])

        self.finalModelState=finalModelState
        mstmids=finalModelState.keys()

        if(len(mstmids) > 0):
            print
            for mstmid in mstmids:
                print 'mstmid:  %10s'%(mstmid),finalModelState[mstmid]

        print 'EEEEEE compMtoO      ------------------- bdtg:',self.bdtg,'  vdtg:',self.vdtg,dogendtg


    def isInInv(self):

        vdtg=mf.dtginc(self.bdtg,self.gentau)
        odtg=self.bdtg
        if(self.dogendtg):
            odtg=vdtg

        key=(self.model,odtg,self.basin,self.gentau,self.gentype)
        print 'III isInInv(key): ',key
        try:
            self.iV.hash[key]
            rc=1
        except:
            rc=0

        return(rc)


    def getHashTrk(self,key):

        oTrks={}

        (model,dtg,basin,gentau,type)=key

        print
        print 'BBBBBB getHashTRk    ------------------- bdtg:',self.bdtg,'  vdtg:',self.vdtg,self.dogendtg
        
        if(self.gt0 != None): print 'gt0: ',self.gt0.aidtrks.keys()
        if(self.gtG != None): print 'gtG: ',self.gtG.aidtrks.keys()
        if(self.ftG != None): print 'ftG: ',self.ftG.aidtrks.keys()
        
        print
        
        self.gt0trks={}
        if(self.gt0 != None): self.gt0trks=self.gt0.aidtrks

        self.gtGtrks={}
        if(self.gtG != None): self.gtGtrks=self.gtG.aidtrks

        amodel=self.model
        self.ftGtrks={}
        if(self.ftG != None): 
            self.ftGtrks=self.ftG.aidtrks
            amodel=self.amodel
        else:
            print 'WWW nothing in getHashTrk for model,dtg,basin,gentau:',model,dtg,basin,' just return'
            return(oTrks)
            

        stmids=self.finalModelState.keys()

        for stmid in stmids:
            fs=self.finalModelState[stmid]
            tau=fs[0]
            sttype=fs[1]
            std=fs[2]
            stdt=fs[3]
            trk={}
            if( 
                (sttype == 'FTC' or sttype == 'FPT' or sttype == 'FGT' or sttype == 'FNT' or sttype == 'FMT')  # fron gothit in setModelStateGen
                or (sttype == 'DIS')                                                                            # from !(gothit) in setModelStateGen
                or (sttype == 'MFC' or sttype == 'MFP')                                                         # from setModelStateFc
                ):
                try:
                    trk=self.ftGtrks[(amodel,stmid)]
                except:
                    trk=None

                if(trk == None):
                    print 'EEE unable to find trk for amodel: ',amodel,' stmid: ',stmid,' basin: ',basin
                    sys.exit()

            if( (sttype == 'GTC' or sttype == 'GPT' or sttype == 'GGT' or sttype == 'GNT' or sttype == 'GMT')  # fron gothit in setModelStateGen
                or (sttype == 'SC1')                                                                   # from !(gothit) in setModelStateGen
                or (sttype == 'MGC' or sttype == 'MNN')                                                  # from setModelStateFc
                ):   
                try:
                    trk=self.gtGtrks[(stmid,basin)]
                except:
                    trk=None

                if(trk == None):
                    print 'EEE unable to find trk for amodel: ',amodel,' stmid: ',stmid,' basin: ',basin
                    sys.exit()


            trkkey=trk.keys()[0]

            oTrks[stmid]=trk[trkkey]
            print 'MMM----------------------: %10s %3d %3s %5.1f %5.1f  %-75s'%(stmid,tau,sttype,std,stdt,str(trk[trkkey].keys()))

        print 'EEEEEE getHashTRk    ------------------- bdtg:',self.bdtg,'  vdtg:',self.vdtg,self.dogendtg

        print
        
        return(oTrks)


    def doInv(self,iV,pr=None,overrideInv=0,verb=0):

        vdtg=mf.dtginc(self.bdtg,self.gentau)
        odtg=self.bdtg
        if(self.dogendtg):
            odtg=vdtg

        key=(self.model,odtg,self.basin,self.gentau,self.gentype)
        print
        print 'doInv(key): ',key,' val.pr: ',pr

        oTrks=self.getHashTrk(key)
        
        if(len(oTrks) == 0):
            print 'WWW doInv oTrks is empty, return...parseHash to set tracks...'
            # -- parsehash analyzes the tracks etc...
            #
            #iV.parseHash(key,hash=iV.hash[key],verb=self.verb)
            #iV.parseHashDone=1
            #return

        val=(self.tcState,self.finalModelState,pr,
             oTrks,
             self.ntcALL,self.nmodALL,self.nmodtc0,
             self.modALL,self.modtc0)

        # -- now put the val to the hash
        #
        MF.sTimer('doinv.put')
        iV.putHash(key,val,override=overrideInv,verb=verb)
        MF.dTimer('doinv.put')

        # -- parsehash analyzes the tracks etc...
        #
        iV.parseHash(key,hash=iV.hash[key],verb=self.verb)
        iV.parseHashDone=1
        


    def setiVCountsZero(self):

        self.iV.nSCs=0
        self.iV.stdSCs=0.0
        self.iV.stdFCGNs=0.0
        self.iV.stdpFCs=0.0
        self.iV.stdGCs=0.0

        self.iV.nGCs=0
        self.iV.nFCs=0
        self.iV.nNFCs=0
        self.iV.npFCs=0
        self.iV.nmFTCs=0
        self.iV.nmDTCs=0 # dissipated TCs

        self.iV.nFCGNs=0
        self.iV.gtcs={}
        self.iV.abtcs={}
        self.iV.fctcs={}
        self.iV.oTrks={}

        

    def setModelStateGen(self,mstmid,mtrk,mposit,gothit,mstate):

        rc=self.isGenTC(mstmid,mtrk)
        
        def setFMstate():
            
            if(tcstate == 'PTC'):
                if(mstate2[0] == 'fc'):
                    # -- check if associated with same storm; if not, the model TC has dissipated
                    if(ostmid != mstmid):
                        fmstate=[mstate2[0],'DIS',mstate2[2],mposit,(olat,olon)]
                    else:
                        fmstate=[mstate2[0],'FPT',mstate2[2],mposit,(olat,olon)]
                else:
                    fmstate=[mstate2[0],'GPT',mstate2[2],mposit,(olat,olon)]
                    
            # -- model tau0 TC
            #
            elif(tcstate == 'MTC'):
                if(mstate2[0] == 'fc'):
                    fmstate=[mstate2[0],'FMT',mstate2[2],mposit,(olat,olon)]
                else:
                    fmstate=[mstate2[0],'GMT',mstate2[2],mposit,(olat,olon)]

            elif(tcstate == 'NN'):
                if(mstate2[0] == 'fc'):
                    # -- check if associated with same storm; if not, the model TC has dissipated
                    if(ostmid != mstmid):
                        fmstate=[mstate2[0],'DIS',mstate2[2],mposit,(olat,olon)]
                    else:
                        fmstate=[mstate2[0],'FTC',mstate2[2],mposit,(olat,olon)]
                else:
                    fmstate=[mstate2[0],'GTC',mstate2[2],mposit,(olat,olon)]
                    
            elif(tcstate == 'NT'):
                if(mstate2[0] == 'fc'):
                    fmstate=[mstate2[0],'FNT',mstate2[2],mposit,(olat,olon)]
                else:
                    fmstate=[mstate2[0],'GNT',mstate2[2],mposit,(olat,olon)]
                    
            elif(tcstate == 'GN'):
                if(mstate2[0] == 'fc'):
                    # -- check if associated with same storm; if not, the model TC has dissipated
                    if(ostmid != mstmid):
                        fmstate=[mstate2[0],'DIS',mstate2[2],mposit,(olat,olon)]
                    else:
                        fmstate=[mstate2[0],'FGT',mstate2[2],mposit,(olat,olon)]
                else:
                    fmstate=[mstate2[0],'GGT',mstate2[2],mposit,(olat,olon)]
                    
            return(fmstate)



        if(len(gothit) == 1):

            ostmid=gothit[0][0]
            tcstate=gothit[0][1]
            gdist=gothit[0][2]
            olat=gothit[0][3]
            olon=gothit[0][4]
            mstate2=gothit[0][5]
            #if(mstate2[0] == 'fc'): tcstate='FGN'
            
            fmstate=setFMstate()
            fmstate.append(ostmid)

            print 'HHH 111 mstmid: ',ostmid,mstmid,tcstate,fmstate

        # -- multiple hits...  two 9x on opposite sides?

        elif(len(gothit) > 1):

            if(len(gothit) > 4):
                print 'EEE too many hits...sayoonara'
                sys.exit()

            # -- get closest
            #
            gdistMin=1e20
            nMin=-999

            for n in range(0,len(gothit)):
                gdist=gothit[n][2]
                if(gdist < gdistMin):
                    gdistMin=gdist
                    nMin=n


            ostmid=gothit[nMin][0]
            tcstate=gothit[nMin][1]
            gdist=gothit[nMin][2]
            olat=gothit[nMin][3]
            olon=gothit[nMin][4]
            mstate2=gothit[nMin][5]
            
            fmstate=setFMstate()
            fmstate.append(ostmid)
            
            print 'HHH 222222222222222222222222222 mstmid: ',self.bdtg,fmstate,nMin,gdist,' nMin: ',nMin

            return(fmstate)

        else:

            if(rc == 1):
                if(mstate[0] == 'fc'):
                    fmstate=[mstate[0],'DIS',mstate[2],mposit]
                else:
                    fmstate=[mstate[0],'SC1',mstate[2],mposit]
            else:
                # -- outside genesis latitudes
                #
                fmstate=[mstate[0],'NNN',mstate[2],mposit]

        return(fmstate)



    def setModelStateFc(self,mstmid,mtrk,mposit,mstate):
        
        rc=self.isGenTC(mstmid,mtrk)

        if(mstate[0] == 'fc'):
            if(IsNN(mstmid)):
                fmstate=[mstate[0],'MFC',mstate[2],mposit]
            elif(Is9X(mstmid)):
                fmstate=[mstate[0],'MFP',mstate[2],mposit]

        elif(mstate[0] == 'tg'):

            if(rc):
                fmstate=[mstate[0],'MGC',mstate[2],mposit]
            else:
                fmstate=[mstate[0],'MNN',mstate[2],mposit]

        return(fmstate)



    def isGenTC(self,stmid,trk):

        rc=1
        taus=trk.keys()
        taus.sort()

        for tau in taus:
            rlat=trk[tau][0]
            if(abs(rlat) > self.maxLatGenTc and stmid[0:2] == 'tg'):
                rc=0
                return(rc)

        return(rc)


    def getGAfromGaProc(self,
                        ):

        # -- force ga options from self -- now done by passing TcgenGP() to Tcgen
        #
        #if(not(hasattr(self,'gaP'))):
        #    self.gaP=GaProc(Quiet=self.gaQuiet,Opts=self.gaOpts)

        if(self.overrideGA):
            ga=None
            ge=None
            gp=None
            
        elif(not(hasattr(self,'ga'))):

            # -- doreinit reinits the grads obj
            #
            self.gaP.initGA(ctlpath=self.ctlpath,doreinit=1)
            ga=self.gaP.ga
            
            lsctl="%s/ls.1deg.ctl"%(w2.geodir)
            ga("open %s"%(lsctl))
            ge=ga.ge
            gp=ga.gp

            self.ga=ga
            self.ge=ge
            self.gp=gp

        else:
            # -- close only does the last file...reinit instead
            #self.ga('close 1')
            #self.ga('close 2')
            self.ga('reinit')
            self.ga('open %s'%(self.ctlpath))
            lsctl="%s/ls.1deg.ctl"%(w2.geodir)
            self.ga("open %s"%(lsctl))
            ga=self.ga
            ge=self.ge
            gp=self.gp
            
# experiment with reordering open and do a close not working because have to set dfile and set initial env
#         if(not(hasattr(self,'ga'))):

#             lsctl="%s/ls.1deg.ctl"%(w2.geodir)
#             self.gaP.initGA(ctlpath=lsctl)
#             ga=self.gaP.ga
#             ga("open %s"%(self.ctlpath))
#             ga('set dfile 2')
#             ge=ga.ge
#             gp=ga.gp

#             self.ga=ga
#             self.ge=ge
#             self.gp=gp

#         else:
#             self.ga("close 2")
#             self.ga("open %s"%(self.ctlpath))
#             self.ga('set dfile 2')
#             ga=self.ga
#             ge=self.ge
#             gp=self.gp




        return(ga,ge,gp)



    def fldDiagTcGen(self,basin,
                     gentau=120,
                     dogendtg=0,
                     doxv=0,
                     pngmethod='printim',
                     verb=0,
                     prOB=25.0,
                     undef=-999.,
                     quiet=0,
                     ):


        (ga,ge,gp)=self.getGAfromGaProc()

        latlons=getBasinLatLonsPrecise(basin)
        
        # -- sums to accumulate sums of pr and area
        #
        pcao=0.0
        pao=0.0
        areao=0.0
        
        for latlon in latlons:
            
            (ge.lat1,ge.lat2,ge.lon1,ge.lon2)=latlon

            ge.setLatLon()
    
            if(hasattr(self,'bdtg')):
                bdtg=self.bdtg
            else:
                if(dogendtg):
                    bdtg=mf.dtginc(self.dtg,-gentau)
                else:
                    bdtg=self.dtg
    
            datagentau=gentau
            
            # -- use tau120 for 132 for fim9
            if(self.doTau120Rtfim9 and self.model == 'rtfim9' and gentau == 132 and hasattr(self,'maxtauTrackers') and self.maxtauTrackers <= 120 ): gentau=120
            
            ge.setTimebyDtgTau(bdtg,datagentau)
    
            # -- get meta data to check if there's a prc...decorate both ge and ga
            #
    
            ge.getFileMeta(ga)
    
            #if(verb):
            #    ga('q file')
            #    ga('q dims')
            #    print 'vars: ',ge.vars
    
            # --- get model specific expr for pr in mm/day
            #
    
            if(hasattr(self.m2,'setprvar')):
                prvar=self.m2.setprvar(bdtg,gentau)
            else:
                prvar=self.m2.modelprvar
    
            if(gentau == 0 and hasattr(self.m2,'modelprvar00')): prvar=self.m2.modelprvar00
            if(gentau == 6 and hasattr(self.m2,'modelprvar06')): prvar=self.m2.modelprvar06
    
            prvar=prvar.split('=')[1]
    
    
            # -- check if there's a prc ...
            #
    
            if('prc' in ge.vars):
                prvarc=prvar.replace('pr','prc')
            else:
                prvarc="(const(pr,-999.0,-a))"
    
            if(not('pr' in ge.vars)):
                'EEE fldDiagTcGen: pr not there...making all undef'
                rc=(undef,undef,undef)
                return(rc)
                
            prvar=prvar.replace("'","")
            prvarc=prvarc.replace("'","")
    
            ga.dvar.re2('pc',prvarc,1.0,1.0)
            ga.dvar.re2('p',prvar,1.0,1.0)
    
            # -- use asum vice aave if there are more than one latitude band
            #
            
            pcao=pcao + ga.get.asum('maskout(pc,-ls.2(t=1))',ge)
            pao=pao + ga.get.asum('maskout(p,-ls.2(t=1))',ge)
            areao=areao + ga.get.asum('maskout(const(p,1),-ls.2(t=1))',ge)

            if(verb):
                print 'pppppppppppppp pcao: ',pcao/areao,prvarc
                print 'pppppppppppppp  pao: ',pao/areao,prvar
                print 'pppppppppppppp area: ',areao
                

        pcao=pcao/areao
        pao=pao/areao
        
        # -- bad pr for fim8 2009080412...
        #
        if(pao  > prOB or pao  == 0): pao=undef
        if(pcao > prOB or pcao == 0): pcao=undef

        if(pcao > 0.0 and pao > 0.0):
            ratioC2T=pcao/pao
        else:
            ratioC2T=undef
            if(pcao < 0.0): pcao=undef

        if(pao < 0.0): pao=undef

        if(verb):
            print 'RRRRRRRRRRRRRRRRRRRRRRRRR ',ratioC2T,pcao,pao

        rc=(ratioC2T,pcao,pao)
        return(rc)



    def w2PlotTcGenFld(self,
                       field='prp',
                       gentau=120,
                       dowindow=0,
                       dostdd=0,
                       doxv=0,
                       pngmethod='printim',
                       doland=0,
                       verb=0,
                       diag=0,
                       fcmode='fcst',
                       override=0,
                       quiet=1,
                       ptype='prp',
                       BMoverride=0,
                       warn=0,
                       doPngquant=1,
                       ):




        datagentau=self.gentau
        
        # -- use tau120 for 132 for fim9
        if(self.doTau120Rtfim9 and self.model == 'rtfim9' and gentau == 132 and self.maxtauTrackers <= 120 ): gentau=120
        
        datavdtg=mf.dtginc(self.bdtg,datagentau)
        odtg=self.bdtg
        if(self.dogendtg): odtg=self.vdtg

        iVkey=(self.model,odtg,self.basin,self.gentau,self.gentype)
        iVhash=self.iV.getHash(iVkey)
        if(not(hasattr(self.iV,'parseHashDone'))):
            self.iV.parseHash(iVkey,hash=iVhash,verb=verb)


        self.doland=doland
        self.pngmethod=pngmethod
        self.diag=diag
        self.fcmode=self.gentype
        self.dostdd=dostdd

        self.ptype=field

        self.allreadyDone=0

        self.parea=TcGenBasin2Area[self.basin]

        # -- define output
        #
        byear=self.bdtg[0:4]
        odir='%s/%s/%s'%(tcgenW3DatDir,byear,self.bdtg)
        MF.ChkDir(odir,'mk')
        
        # -- plot rename, e.g., use ecm4 for ecm2 plots
        #
        omodel=self.model
        if(self.omodelPlot != None): omodel=self.omodelPlot

        opath="%s/%s.%s.%03d.%s.%s.%s.%s.gentracker.png"%(odir,omodel,self.vdtg,self.gentau,self.basin,self.parea,self.ptype,self.fcmode)
        self.opath=opath
        if( not(override or not(MF.ChkPath(opath))) ):
            print 'III opath: ',opath,' already done...model: ',omodel,' bdtgs ',self.bdtg,' vdtg: ',self.vdtg,' gentau: ',self.gentau
            if(doxv):  os.system("xv -geometry +20+20 %s"%(self.opath))
            self.allreadyDone=1
            return
        elif( override and MF.ChkPath(opath)):
            if(warn): print 'III override, blow away file if already there -- issue on fat32 drive, not writing if already there and making file 0 size!!!!!!'
            try:
                os.unlink(opath)
                if(warn): print 'WWW failed to os.unlink(opath) opath: ',opath,' -------------------------------------------------------------wwwwwwwwwwww'
            except:
                None


        (ga,ge,gp)=self.getGAfromGaProc()

        # -- all vdtg to be overwritten by datavdtg
        #
        self.setw2Plot(ga,self.parea,datavdtg,self.gentau,BMoverride=BMoverride)

        # -- field plot
        #

        if(field == 'prp'):
            rc=self.w2PlotPrp()
        elif(field == 'n850'):
            rc=self.w2PlotNhc850vort()
        elif(field == 'uas'):
            rc=self.w2PlotSfcWind()

        if(not(rc)):
            print 'WWW not enough data to plot...sayoonara...'
            ge.clear()
            return

        # -- tracks
        #
        self.w2PlotTcGenTracks()

        # -- title
        #
        self.w2PlotTitle(field=field)

        print 'Pnging: ',self.opath

        gs="%s %s -b %s -t 0 x%d y%d png"%(self.pngmethod,self.opath,self.bmpngpath,self.xsize,self.ysize)
        #--- no bm gs="%s %s x%d y%d png"%(self.pngmethod,self.opath,self.xsize,self.ysize)
        print 'gs: ',gs
        self.ga(gs)
        xpngquant=self.tcGP.xpngquant
        if(doPngquant and xpngquant != None):
            cmd="%s --speed 10 -f 64 %s -o %s"%(xpngquant,self.opath,self.opath)
            mf.runcmd(cmd)
            
        if(doxv):  os.system("xv -geometry +20+20 %s"%(self.opath))

        # -- clear if we come back in...
        #
        if(dowindow): ga('q pos')
        ge.clear()

        return



    def w2PlotTitle(self,field='prp'):

        model=self.model
        basin=self.basin
        gentau=self.gentau
        ga=self.ga
        ge=self.ge
        gp=self.gp

        bdtg=self.bdtg
        vdtg=self.vdtg

        #bdtg=self.iV.bdtg
        #vdtg=self.iV.vdtg
        dostdd=self.dostdd

        rc=self.getTCgenProps(basin,gentau,verb=self.verb)
        if(rc == None):
            print 'III return None from getTCgenProps, bail...model: ',model,' bdtgs ',bdtg,' vdtg: ',vdtg,' gentau: ',gentau
            return
        (opr,oprc,orc2t,
         nTCs,
         nNTCs,
         nGNs,
         npTCs,
         naTCs,
         nSCs,
         stdSCs,
         stdGCs,
         stdFCGNs,
         stdpFCs,
         nGCs,
         nFCs,
         nNFCs,
         npFCs,
         nmFTCs,
         nmDTCs,
         nFCGNs,
         )=rc


        if(self.verb):
            print 'NNNNNNNN nTCs: ',nTCs
            print 'NNNNNNNN nNTCs: ',nNTCs
            print 'NNNNNNNN nGNs: ',nGNs
            print 'NNNNNNNN npTCs: ',npTCs
            print 'NNNNNNNN nSCs: ',nSCs
            print 'NNNNNNNN nGCs: ',nGCs
            print 'NNNNNNNN nFCs: ',nFCs
            print 'NNNNNNNN nNFCs: ',nNFCs
            print 'NNNNNNNN npFCs: ',npFCs
            print 'NNNNNNNN nmFTCs: ',nmFTCs
            print 'NNNNNNNN nmDTCs: ',nmDTCs
            print 'NNNNNNNN nFCGNs: ',nFCGNs

            print 'SSSSSSS stdGCs: ',stdGCs

        # -- title object
        #
        ttl=gp.title
        ttl.set(scale=0.85)

        mode=self.gentype.upper()
        omode=mode
        dayFcst="DAY-%1d"%(int(gentau)/24)
        omode="%s %s"%(dayFcst,mode)
        if(mode == 'VERI'): omode='`0%s %s`0'%(dayFcst,mode)

        if(mode == 'VERI'):
            t1="%s :: %-11s valid vdtg: %s  `3t`0=%3d [h]  pr: %s [mm/d]  prc2t: %s"%(omode,tcgenModelLabel[model],vdtg,int(gentau),opr,orc2t)

            t2="  run bdtg: %s :: OBS#[TCs:%1d NTCs:%1d pTCs:%d gTCs:%1d aTCs:%1d]"%(bdtg,nTCs,nNTCs,npTCs,nGNs,naTCs)
            t2="%s  MODEL#[TCs:%1d NTCs:%1d pTCs:%1d gTCs:%1d aTCs:%1d dTCs:%1d]"%(t2,nFCs,nNFCs,npFCs,nGCs,nmFTCs,nmDTCs)
            t2="%s #mod(spurTCs): %1d  mod(spurSTD): %4.1f d"%(t2,nSCs,stdSCs)


        else:
            t1="%s :: %-11s  run bdtg: %s  `3t`0=%3d [h]  pr: %s [mm/d]  prc2t: %s"%(omode,tcgenModelLabel[model],bdtg,int(gentau),opr,orc2t)

            t2="valid vdtg: %s :: OBS#[TCs:%1d NTCs:%1d pTCs:%d gTCs:%1d aTCs:%1d]"%(vdtg,nTCs,nNTCs,npTCs,nGNs,naTCs)
            t2="%s  MODEL#[TCs:%1d NTCs:%1d pTCs:%1d gTCs:%1d aTCs:%1d dTCs: %d]"%(t2,nFCs,nNFCs,npFCs,nGCs,nmFTCs,nmDTCs)            
            t2="%s #mod(formTCs): %1d  mod(formSTD): %4.1f d"%(t2,nFCGNs,stdFCGNs)


        #if(nNo > 0):
        #    t2="%s nNo: %2d stddNo: %4.1f "%(t2,nNo,sumStdd)

        ttl.t2scale=0.60
        ttl.top(t1,t2)

        pt1=pt2=None
        if(field == 'n850'):
            pt1='850 mb rel vort (*1e-5) + 200 mb winds (barbs) + 500 mb heights (dashed)'
        elif(field == 'prp'):
            pt1='precip (shaded; mm/d) + sea level pressure (mb)'
        elif(field == 'uas'):
            pt1='sfc wind (shaded; kts)'

        ttl.scale=1.0
        ttl.t1col=3
        ttl.t2col=3
        ttl.plot(pt1,pt2)


    def getTCgenProps(self,basin,gentau,
                      itcgcards=None,
                      warn=0,
                      verb=1):


        prc=pr=rc2t=None

        nNo=0
        sumStdd=0.0

        if(self.iV.prc != None):  oprc="%4.2f"%(self.iV.prc)
        else:             oprc='N/A'

        if(self.iV.pr != None):   opr="%4.2f"%(self.iV.pr)
        else:             opr='N/A'

        if(self.iV.rc2t != None and self.iV.rc2t > 0.0):  orc2t="%4.2f"%(self.iV.rc2t)
        else:                             orc2t='N/A'


        rc=(opr,oprc,orc2t,
            self.iV.nTCs,
            self.iV.nNTCs,
            self.iV.nGNs,
            self.iV.npTCs,
            self.iV.naTCs,
            self.iV.nSCs,
            self.iV.stdSCs,
            self.iV.stdGCs,
            self.iV.stdFCGNs,
            self.iV.stdpFCs,
            self.iV.nGCs,
            self.iV.nFCs,
            self.iV.nNFCs,
            self.iV.npFCs,
            self.iV.nmFTCs,
            self.iV.nmDTCs,
            self.iV.nFCGNs,
            )

        return(rc)




    def w2PlotTcGenTracks(self):

        model=self.model
        basin=self.basin
        gentau=self.gentau
        bdtg=self.bdtg
        doland=self.doland
        ga=self.ga
        ge=self.ge
        fcdtau=self.fcdtau
        dostdd=self.dostdd
        verb=self.verb
        vdtg=self.vdtg

        aW2=self.aW2

        if(self.done == -999):
            print 'Tcgen.w2PlotTcGenTracks() -- no trackers -- return'
            return


        rc=self.getTCgenProps(basin,gentau,verb=verb)
        if(rc == None):
            print 'III return None from getTCgenProps, bail...model: ',model,' bdtgs ',bdtg,' vdtg: ',vdtg,' gentau: ',gentau
            return


        self.diag=0

        abtcs=self.iV.abtcs
        gtcs=self.iV.gtcs
        fctcs=self.iV.fctcs
        fctrks=self.iV.oTrks

        genstmids=[]
        if(len(gtcs) > 0):  genstmids=gtcs.keys()

        gbt={}
        gbtstmids=[]
        gtcol=9
        mcol=2

        nhforBT=gentau
        nhforBT=0
        dtg0BT=bdtg
        if(self.gentype == 'veri'):
            nhforBT=0
            dtg0BT=vdtg

        # -- inline def to get blat/blon for checking if 
        #
        def getBTblatblon():

            if(self.dogendtg):

                try:
                    blat=bts[vdtg][0]
                    blon=bts[vdtg][1]
                except:
                    try:
                        blat=bts[bdtg][0]
                        blon=bts[bdtg][1]
                        print 'WWW(w2PlotTcGenTracks) no bt for vdtg and dogendtg =1 using bdtg...'
                    except:
                        print 'WWW(w2PlotTcGenTracks) - no bt for bdtg: ',vdtg,'stmid: ',stmid
                        return(None,None)
            else:
                
                try:
                    blat=bts[bdtg][0]
                    blon=bts[bdtg][1]
                except:
                    try:
                        blat=bts[vdtg][0]
                        blon=bts[vdtg][1]
                        print 'WWW(w2PlotTcGenTracks) no bt for BDTG and dogendtg = 0  using VDTG..'
                    except:
                        print 'WWW(w2PlotTcGenTracks) - no bt for vdtg: ',vdtg,'stmid: ',stmid
                        return(None,None)
                        
            return(blat,blon)

        # -- setup plot obj for BT
        #
        pbt={}
        finaly=-999


        btmcols=[2,7,3,5]*3  # -- case with > 8 storms!!!
        pbtstmids=[]
        bcol=0
        
        for stmid in abtcs.keys():

            bts=self.tcD.getBtLatLonVmax(stmid,stmdtg=dtg0BT)
            bbb=bts.keys()
            bbb.sort()
            (blat,blon)=getBTblatblon()
            
            if(len(bbb) == 0 or blat == None): continue

            if( (blat >= self.aW2.latS and blat <= self.aW2.latN) and
                (blon >= self.aW2.lonW and blon <= self.aW2.lonE) ):
                if(self.diag):
                    bbs=bts.keys()
                    bbs.sort()
                    for bt in bbs:
                        print 'bb--',stmid,bt,bts[bt]

                pbtstmids.append(stmid)

        # -- plot BT
        #

        for stmid in pbtstmids:

            # -- instantiate plot object here not as a hash
            #
            bcol=bcol+1
            bts=self.tcD.getBtLatLonVmax(stmid,stmdtg=dtg0BT)
            pb=self.gp.plotTcBt
            pb.set(bts,dtg0=dtg0BT,nhbak=72,nhfor=nhforBT,mcol=btmcols[bcol],ddtgfor=self.fcdtau,ddtgbak=self.fcdtau,mcolTD=6)

            btlgdcol=1
            for gstmid in genstmids:
                if(stmid == gstmid): btlgdcol=gtcol
            otimes=pb.otimesbak[:]+pb.otimesfor[:]
            otimes=MF.uniq(otimes)
            pb.dline(times=otimes,lcol=7,lthk=10)
            pb.dwxsym(times=otimes)
            resetfinaly=0
            if(finaly == -999): resetfinaly=1
            if(finaly != -999): pb.finaly=finaly
            pb.legend(ge,times=otimes,bttitle=stmid,btlgdcol=btlgdcol,resetfinaly=resetfinaly)
            finaly = pb.finaly-pb.dy
            
        # -- plot the genesis points
        #

        for stmid in genstmids:

            bts=self.tcD.getBtLatLonVmax(stmid,stmdtg=dtg0BT)

            gts=self.tcD.getBtLatLonVmax(stmid)
            dds=self.tcD.getDSsFullStm(stmid)
            
            if(dds != None):
                gendtgs=dds.gendtgs

            else:
                print 'WWW(Tcgen.w2PlotTcGenTracks): dds for stmid: ',stmid,' == None ... press'
                continue
                
            if(gendtgs == None):
                print 'WWW(Tcgen.w2PlotTcGenTracks): gendtgs == None ... press'
                continue

            
            # -- filter the gendtgs to every fcdtau
            #
            gendtgs=mf.dtgrange(gendtgs[0],gendtgs[-1],self.fcdtau)

            ggg=gts.keys()
            ggg.sort()

            glat=gtcs[stmid][0]
            glon=gtcs[stmid][1]
            
            # -- make sure the genlat lons are from a bt inside the plot area
            #
            
            (blat,blon)=getBTblatblon()
            
            if( (glat >= aW2.latS and glat <= aW2.latN) and
                (glon >= aW2.lonW and glon <= aW2.lonE) and
                (blat >= aW2.latS and blat <= aW2.latN) and
                (blon >= aW2.lonW and blon <= aW2.lonE) ):

                if(self.diag):
                    gbs=gts.keys()
                    gbs.sort()
                    for gt in gbs:
                        print 'gg--',gt,gts[gt]

                gb=self.gp.plotTcBt
                gb.set(gts,dtg0=gendtgs[-1],nhbak=24,nhfor=0,mcol=gtcol,ddtg=self.fcdtau,mcolTD=gtcol)
                gbt[stmid]=gb
                gbtstmids.append(stmid)

                # -- do plotting after instantiation
                #
                gb.dline(times=gendtgs,lcol=gtcol,lthk=10)
                #gb.dwxsym(times=gendtgs,wxcol=1,wxthk=20,wxsiz=0.25)
                #gb.dwxsym(times=gendtgs,wxcol=gtcol,wxthk=7)
                gb.dmark(times=gendtgs,mksym=3,mkthk=6,mkcol=gtcol,mksiz=0.04)



        # -- plot fcs
        #
        fcs={}

        fstmids=fctrks.keys()
        fstmids.sort()

        fcmkendcol=6
        fcmkendcolin=1
        fclcol=7

        gcmkendcol=2
        gcmkendcolin=1
        gclcol=7


        for fstmid in fstmids:

            ostmid=None
            mkendcol=fcmkendcol
            mkendcolin=fcmkendcolin

            fcs=fctrks[fstmid]
            fctaus=fcs.keys()
            fctaus.sort()

            if(len(fctcs[fstmid]) > 8):
                (fctau,fcstate,fcstd,fclife,fclat,fclon,vclat,vclon,ostmid)=fctcs[fstmid]
            else:
                (fctau,fcstate,fcstd,fclife,fclat,fclon,vclat,vclon)=fctcs[fstmid]

            mkendcol=4

            mkcolOuter=0
            mkcolInner=None
            mksizOuter=0.080
            mksizInner=0.050
            
            if(fcstate == 'MFC' or fcstate == 'FTC'):
                mkendcol=1
                
            if(fcstate == 'GTC'):
                mkendcol=5
                    
                
            elif(fcstate == 'GGT'):
                mkendcol=9
                mkcolOuter=3
                mkcolInner=mkendcol
                mksizOuter=0.090
                mksizInner=0.050                  
                
            # -- tau 0 storms -- from 'fc' pTC/TC tracker 
            #
            elif(fcstate == 'FMT'):
                
                mkendcol=1 
                mkcolOuter=mkendcol
                mkcolInner=2
                #mksizOuter=0.080
                #mksizInner=0.060                
            
            # -- tau 0 storms from genesis 'gn' tracker
            #
            elif(fcstate == 'GMT'):
                
                mkendcol=5  
                mkcolOuter=mkendcol
                mkcolInner=2
                #mksizOuter=0.100
                #mksizInner=0.060
                
             
            elif(fcstate == 'FGT'):
                mkendcol=9
                mkcolOuter=1
                mkcolInner=mkendcol
                mksizOuter=0.090
                mksizInner=0.050                  
                
                
            elif(fcstate == 'MGC'):
                mkendcol=10
            elif(fcstate == 'FPT' or fcstate == 'GPT' or fcstate == 'MFP'):
                mkendcol=7
                
            elif(fcstate == 'SC1'):
                mkendcol=2
                
            # dissipated storms either pTC or TC
            #
            elif(fcstate == 'DIS'):
                
                if(IsNN(fstmid)): mkendcol=1
                if(Is9X(fstmid)): mkendcol=7
                mkcolOuter=15
                
                #mkendcol=15
                mksizOuter=0.070
                mksizInner=0.030

            # -- set the color of the model track
            #
            fclcol=mkendcol

            # -- set inner dot color
            #
            if(mkcolInner == None): mkcolInner=mkendcol
            
            try:
                fcvmax=fcs[fctau][2]
            except:
                fcvmax=None

            # -- display max wind at end of period
            #
            if(fcvmax != None and fcvmax > 0):
                fcdlab="%3.0f"%(float(fcvmax))
            else:
                fcdlab=''
                print 'WWW fcvmax in w2PlotTcGenTracks is undef or None fcvmax: ',fcvmax,self.model,gentau

            fclabcol=2
            fclabthk=5
            fclabsiz=0.08

            # -- for model genesis cyclone (MGC) display sTD
            #
            if(fcstate == 'MGC' or fcstate == 'GN' or fcstate == 'SC1'):
                if(fcstd != None):
                    fcdlab="%3.1f"%(float(fcstd))
                else:
                    fcdlab='ggg'

                fclabcol=1
                fclabthk=6
                if(fcstate == 'SC1'):
                    fclabcol=2
                    fclabthk=9


            # -- for fc doland
            #
            pf=self.gp.plotTcFt
            pf.set(fcs,dovmaxflg=0,verb=0,doland=1)


            try:
                nl=fctaus.index(gentau)
            except:
                nl=len(fctaus)

            pfctaus=fctaus[0:nl+1]

            # -- thin taus by 
            #
            fctaus=[]
            for pt in pfctaus:
                if(pt%self.fcdtau == 0): fctaus.append(pt)


            if(gentau in fctaus):
                mfctime=[gentau]
            else:
                mfctime=[pfctaus[-1]]
                
            pf.dline(times=fctaus,lcol=fclcol)
            pf.dmark(times=fctaus,mkcol=mkcolOuter,mksiz=mksizOuter)
            pf.dmark(times=fctaus,mkcol=mkcolInner,mksiz=mksizInner)
            #pf.dmark(mksiz=0.125,mkcol=mkendcol,mksym=3,mkthk=4,times=[gentau])
            #pf.dmark(mksiz=0.050,mkcol=mkendcolin,times=[gentau])
            #pf.dlabel(times=[gentau],dlab=fcdlab,lbthk=fclabthk,lbcol=fclabcol)
            pf.dlabel(times=mfctime,lbsiz=fclabsiz,dlab=fcdlab,lbthk=20,lbcol=0)
            #pf.dlabel(times=[pfctaus[-1]],dlab=fcdlab,lbthk=fclabthk,lbcol=fclabcol)
            pf.dlabel(times=mfctime,lbsiz=fclabsiz,dlab=fcdlab,lbthk=fclabthk,lbcol=fclabcol)

            #pf.dlabel(times=[gentau],dlab=fcdlab,lbthk=1,lbcol=1)


        return


    def setw2Plot(self,ga,parea,vdtg,gentau,
                  dobm=1,
                  BMoverride=0,
                  ):

        ge=ga.ge
        gp=ga.gp

        def setGe(doclear=1,timelab='on'):
            
            if(doclear): ge.clear()
            
            self.gentau=gentau
            aW2=getW2Area(parea)
            self.aW2=aW2
    
            ge.timelab=timelab
            ge.lon1=aW2.lonW
            ge.lon2=aW2.lonE
            ge.lat1=aW2.latS
            ge.lat2=aW2.latN
            ge.xlint=aW2.xlint
            ge.ylint=aW2.ylint
            ge.pareaxl=0.5
            ge.pareaxr=9.5
            ge.pngmethod=self.pngmethod
    
            ge.mapcol=15
            ge.grid='on'
            ge.setMap()
            ge.setLatLon()
            ge.setXylint()
            ge.setParea()
            ge.setPlotScale()
            ge.setColorTable()
    
            # -- force setting xsize from self
            #
            ge.setXsize()
    
        setGe()
        
        bm=gp.basemap2
        
        bm.set(xsize=self.xsize,ysize=self.ysize,
               bmdir=tcgenW3Dir,
               bmname='%s'%(self.basin),
               )
        if(dobm):
            if(self.pngmethod == 'printim'):
                if(not(MF.ChkPath(bm.pngpath)) or BMoverride):
                    setGe(doclear=1,timelab='off')
                    print 'MMMMMMMMMMMMMMMMM making:',bm.pngpath,BMoverride
                    bm.draw()
                    bm.putPng()
                self.bmpngpath=bm.pngpath
                setGe()
            elif(self.pngmethod == 'gxyat'):
                bm.draw()
                
        ge.timelab='on'
        ge.setPlotScale()
        ge.setTimebyDtg(vdtg,verb=0)


    def chkDataThere(self,expr,pcntOK=80.0,verb=0):

        if(expr == None):
            rc=-999.0
            return(0)

        gxS=self.ga.getExprStats(expr)
        if(not(hasattr(gxS,'nvalid'))):
            print 'WWW something wrong in chkDataThere with expr: ',expr,'return undef)'
            return(0)
        
        nvalid=float(gxS.nvalid)
        nundef=float(gxS.nundef)
        ntot=nvalid+nundef
        pcntvalid=(nvalid/ntot)*100.0
        rc=(pcntvalid >= pcntOK)
        if(verb): print 'Tcgen.chkDataThere(): expr: ',expr,' pcntvalid,pcntOK,rc: ',pcntvalid,pcntOK,rc
        return(rc)


    def w2PlotPrp(self):

        prvar=None
        if(hasattr(self.m2,'setprvar')):
            prvar=self.m2.setprvar(self.bdtg,self.gentau)
        else:
            prvar=self.m2.modelprvar

        if(prvar != None):
            prvar=prvar.split('=')[1]
            prvar=prvar.replace("'","")

        prOK=self.chkDataThere(prvar)
        if(not(prOK)):
            print 'WWW no/insufficient data for expr: ',prvar,' gentau: ',self.gentau,' vdtg: ',self.vdtg
            return(0)


        pslvar=None

        if(hasattr(self.m2,'setpslvar')):
            pslvar=self.m2.setpslvar(self.bdtg)
        else:
            pslvar=self.m2.modelpslvar

        prOK=self.chkDataThere(prvar)
        pslOK=self.chkDataThere(pslvar)

        #d re(%s,360,linear,0.0,1.0,181,linear,-90.0,1.0)

        prlevs=' 1  2  4  8  16  32 64 128'
        prcols='0 59 58 57 55  53 75 73   71'
        
        prPcuts=prlevs.split()
        prPcols=prcols.split()
        
        # -- convert list of char to ints
        #
        prPcuts=[ int(x) for x in prPcuts ]
        prPcols=[ int(x) for x in prPcols ]
        
        gs="""
set clevs   %s
set grads off
set timelab on
set gxout shaded
set csmooth on
set cterp on
set rgb 98 185 255 00 50
set ccols 0 39 37 36 98 22 24 26 61
set ccols %s
set csmooth on
set cterp on
# turn off lat/lon labs -- take from basemap -- basemap.2 .png != from display of a variable?
set xlopts 1 0 0.0
set ylopts 1 0 0.0
d %s
pm=const(maskout(const(lat,-1),abs(lat)-30),0,-u)
pmt=const(maskout(const(lat,-1),abs(lat)-15),0,-u)
"""%(prlevs,prcols,prvar)

        self.ga(gs)

        # -- do explicitly
        #
        cb=self.gp.cbarn
        cb.draw(vert=0,sf=0.75,pcuts=prPcuts,pcols=prPcols)

        gs="""

#psl=smth2d(psl,100)  smth9 more effective
# -- new smoothing scheme for psl and over land by regridding to a 2deg grid and smth9
#

psl=%s
psl=smth9(smth9(smth9(smth9(smth9(psl)))))

p2=re(psl,2)
pl=maskout(lterp(p2,psl),lterp(ls.2(t=1)-0.5,psl))
pl=smth9(smth9(smth9(pl)))
plm=const(const(pl,-1),1,-u)
po=maskout(psl,plm)
pa=const(po,0,-u)+const(pl,0,-u)
slp=pa

set gxout contour
set clab off

set ccolor 0
set cthick 10
set cint 4
d slp

set ccolor rainbow
set rbrange 980 1032
set cthick 2
set cint 4
d slp

set ccolor 0
set cthick 10
set cint 2
d maskout(slp,pm)

set ccolor rainbow
set rbrange 980 1032
set cthick 4
set cint 2
d maskout(slp,pm)

set ccolor 0
set cthick 10
set cint 1
d maskout(slp,pmt)

set ccolor 3
set cthick 4
set cint 1
d maskout(slp,pmt)

return

"""%(pslvar)


        if(pslOK): self.ga(gs)

        return(1)

    def w2PlotSfcWind(self):

        # -- uas
        
        uasvar='uas'
        vasvar='vas'
        wasvar='ws'

        uasOK=self.chkDataThere(uasvar)
        vasOK=self.chkDataThere(vasvar)
        
        if(not(uasOK)):
            print 'WWW no/insufficient data for expr: ',uasvar,' gentau: ',self.gentau,' vdtg: ',self.vdtg
            return(0)

        # -- psl
        
        pslvar=None
        if(hasattr(self.m2,'setpslvar')):
            pslvar=self.m2.setpslvar(self.bdtg)
        else:
            pslvar=self.m2.modelpslvar

        pslOK=self.chkDataThere(pslvar)

        #d re(%s,360,linear,0.0,1.0,181,linear,-90.0,1.0)

        prlevs=' 1  2  4  8  16  32 64 128'
        prcols='0 59 58 57 55  53 75 73   71'
        
        uascols='0 49 47 43  21 25 29'
        uaslevs=' 10 15 20 30 50  65'
        
        uasPcuts=uaslevs.split()
        uasPcols=uascols.split()
        
        # -- convert list of char to ints
        #
        uasPcuts=[ int(x) for x in uasPcuts ]
        uasPcols=[ int(x) for x in uasPcols ]
        
        uasReDx='0.75'
        m2k=str(ms2knots)
        
        gs="""
# -- make defined vars
us=re(%s,%s)*%s
vs=re(%s,%s)*%s
mk=re(-1.0*ls.2(t=1),%s)
ws=mag(us,vs)

"""%(uasvar,uasReDx,m2k,
     vasvar,uasReDx,m2k,
     uasReDx
     )
        
        wskip=6
        gs=gs+"""
set grads off
set timelab on
set gxout shaded
set csmooth on
set cterp on
set rgb 47  10 80 160
set rgb 49  00 50 100
set clevs   10 15 20 30 50  65
set ccols 0 0 49 47 43  21 25 29
# - 20020212 - change min to 15 kts by setting 10-15 color to 0(CPT Cantrell request)
set clevs   15 20 30 50  65
set ccols 0 47 43  21 25 29

# turn off lat/lon labs -- take from basemap -- basemap.2 .png != from display of a variable?
set xlopts 1 0 0.0
set ylopts 1 0 0.0
d %s

set gxout contour
set clab off
set ccolor 0
set cthick 7
set clevs 15 20 30
d %s

set gxout stream
set strmden 5
set cthick 10
set ccolor 0
d re(%s,1.5);re(%s,1.5)

set cthick 4
set ccolor 34
d re(%s,1.5);re(%s,1.5)

set gxout barb
set digsiz 0.03

*	winds greater than 10 kts
*
set ccolor 0
set cthick 20
d skip(us,%d);maskout(vs,ws-10.0))

set cthick 4
set ccolor 1
d skip(us,%d);maskout(vs,ws-10.0))

set ccolor 0
set cthick 20
d skip(us,%d);maskout(vs,ws-24.0))

set cthick 4
set ccolor 12
d skip(us,%d);maskout(vs,ws-24.0))

set ccolor 0
set cthick 20
d skip(us,%d);maskout(vs,ws-34.0))

set cthick 4
set ccolor 8
d skip(us,%d);maskout(vs,ws-34.0))



# -- masks for slp 
pm=const(maskout(const(lat,-1),abs(lat)-30),0,-u)
pmt=const(maskout(const(lat,-1),abs(lat)-15),0,-u)
"""%(wasvar,wasvar,uasvar,vasvar,uasvar,vasvar,
     wskip,wskip,
     wskip,wskip,
     wskip,wskip,
     )

        self.ga(gs)

        # -- do explicitly
        #
        cb=self.gp.cbarn
        cb.draw(vert=0,sf=0.75,pcuts=uasPcuts,pcols=uasPcols)

        gs="""

slp=smth2d(%s,1)
set gxout contour
set clab off

set ccolor 0
set cthick 10
set cint 4
d slp

set ccolor rainbow
set rbrange 980 1032
set cthick 2
set cint 4
d slp

set ccolor 0
set cthick 10
set cint 2
d maskout(slp,pm)

set ccolor rainbow
set rbrange 980 1032
set cthick 4
set cint 2
d maskout(slp,pm)

set ccolor 0
set cthick 10
set cint 1
d maskout(slp,pmt)

set ccolor 3
set cthick 4
set cint 1
d maskout(slp,pmt)

"""%(pslvar)


        #if(pslOK): self.ga(gs)


        return(1)


    def w2PlotNhc850vort(self):


        pslvar=None

        if(hasattr(self.m2,'setpslvar')):
            pslvar=self.m2.setpslvar(self.bdtg)
        else:
            pslvar=self.m2.modelpslvar

        plev1=850
        plev2=200

        self.ge.setColorTable(table='jaecol.gsf')

        zg5expr='zg(lev=500)'
        if(self.model == 'era5' or self.model == 'ecm5'):
            zg5expr='zg(lev=500)/%f'%(gravity)
            
        
        if(self.model == 'ecm4' or self.model == 'ukm2' or self.model == 'gfs2'):
            vrtexpr="""rvrt8=hcurl(u8,v8)*1e5
    rvrt8=smth9(smth9(smth9(smth9(rvrt8))))"""
        else:
            vrtexpr="""rvrt8=hcurl(u8,v8)*1e5
rvrt8=smth9(rvrt8))"""
        
        gs="""
z5=%s

u8=ua(lev=%d)
v8=va(lev=%d)
%s
u2=ua(lev=%d)
v2=va(lev=%d)

cf=lat/abs(lat)
cf=const(cf,1,-u)

u8=u8*%f
v8=v8*%f
u2=u2*%f
v2=v2*%f

"""%(zg5expr,plev1,plev1,vrtexpr,
     plev2,plev2,ms2knots,ms2knots,ms2knots,ms2knots)

        uvskip=8
        v2e1='maskout(maskout(u2trop,w2-10),20-w2);skip(v2,%d)'%(uvskip)
        v2em='maskout(maskout(u2trop,w2-20),40-w2);skip(v2,%d)'%(uvskip)
        v2e2='maskout(maskout(u2trop,w2-40),100-w2);skip(v2,%d)'%(uvskip)
        
        vrtlevs='4   6    8    10    12    14   16  18    20'
        vrtcols='0   39  37   35    22   24    26   27   28   6'
        
        vrtPcuts=vrtlevs.split()
        vrtPcols=vrtcols.split()
        vrtPcuts=[ int(x) for x in vrtPcuts ]
        vrtPcols=[ int(x) for x in vrtPcols ]
        
        gs=gs+"""

set gxout shaded
set csmooth on
set clevs %s
set ccols %s
# turn off lat/lon labs -- take from basemap -- basemap.2 .png != from display of a variable?
# -- get two slightly different grid lines from the 1st to 2nd d ? why?
set xlab off
set ylab off
set xlopts 1 0 0.0
set ylopts 1 0 0.0

d rvrt8
"""%(vrtlevs,vrtcols)

        self.ga(gs)

        vrtvar='rvrt8'
        vrtOK=self.chkDataThere(vrtvar)
        if(not(vrtOK)):
            print 'WWW no/insufficient data for expr: ',vrtvar,' gentau: ',self.gentau,' vdtg: ',self.vdtg
            return(0)

        #self.ge.getShades()

        cb=self.gp.cbarn
        cb.draw(vert=0,sf=0.75,pcuts=vrtPcuts,pcols=vrtPcols)

        gs="""

u2=re(u2,0.5)
v2=re(v2,0.5)

w2=mag(u2,v2)
latr=re(lat,0.5)
u2trop=maskout(u2,30.0-abs(latr))
#u2trop=u2

ds2=0.04
set digsiz 0.03

set xlab on
set ylab on
set xlopts 1 0 0.0
set ylopts 1 0 0.0

set gxout barb
set cthick 20
set ccolor 0
d %s

set cthick 5
set ccolor 3
d %s

set cthick 20
set ccolor 0
d %s

set cthick 5
set ccolor 1
d %s

set cthick 20
set ccolor 0
d %s

set cthick 5
set ccolor 2
d %s

set gxout contour
set cint 60
set ccolor 1
set cthick 6
set cstyle 3
set clab off
d z5


set gxout contour
set cint 20
set ccolor 1
set cthick 5
set cstyle 3
set clab off
d maskout(z5,30-abs(lat)))


"""%(v2e1,v2e1,v2em,v2em,v2e2,v2e2)


        self.ga(gs)

        return(1)




class TcgenGA(Tcgen):

    def __init__(self,
                 gaQuiet=1,
                 gaWindow=0,
                 gadoLogger=0,
                 gaOpts='',
                 xsize=1440,
                 overrideGA=0,
                 xgrads='grads',
                 ):


        # --set put gaP objects...
        """

"""
        self.xsize=xsize
        aspect=w2.W2plotAspect
        self.ysize=int(self.xsize*aspect) 
        
        self.xgrads=xgrads
        self.xpngquant=setPngquant()
        #self.xpngquant=None
        self.gaopt='-g 20+20+%dx%d'%(self.xsize,self.ysize)
        self.gaopt=''
        self.gaQuiet=gaQuiet
        self.gaWindow=gaWindow
        self.gadoLogger=gadoLogger
        self.gaOpts=gaOpts
       

        if(not(overrideGA)):
            self.gaP=GaProc(
                Quiet=self.gaQuiet,
                Window=self.gaWindow,
                Opts=self.gaOpts,
                doLogger=self.gadoLogger,
                Bin=self.xgrads
            )
        else:
            self.gaP=None






class BestTrk(MFbase):

    def __init__(self,dtgs=[],btcs={}):

        self.dtgs=dtgs
        self.btcs=btcs
        self.btrk={}

        for dtg in dtgs:
            [btdic,cqdic,wndic,stdic,fldic,stdic,r34quad,r50quad]=btcs[dtg]
            self.btrk[dtg]=btdic


    def getwbt(self,dtg):

        btc=self.btcs[dtg]

        [btdic,cqdic,wndic,stdic,fldic,stdic,r34quad,r50quad]=btc

        [btlat,btlon,btvmax,btpmin,btdir,btspd]=btdic
        [cqlat,cqlon,cqvmax,cqpmin,cqdir,cqspd]=cqdic
        [wnlat,wnlon,wnvmax]=wndic
        [flgtc,flgind,flgcq,flgwn,tdo,lf,tsnum]=fldic

        [btvmax,r34,r50,rmax,reye,poci,roci,tcdepth]=stdic

        print cqdic
        print fldic

        return(0)

    def selectBestBtCqTau0(self,dtg,verb=0):

        try:
            btc=self.btcs[dtg]
        except:
            return(None,None,None,None,None)

        [btdic,cqdic,wndic,stdic,fldic,stdic,r34quad,r50quad]=btc

        [blat0,blon0,bvmax0,bpmin0,bdir0,bspd0]=btdic
        [cqlat0,cqlon0,cqvmax0,cqpmin0,cqdir0,cqspd0]=cqdic


        # bt/cq dir,spd init posit
        #

        if(cqspd0 > 0.0):
            btspd=cqspd0
            btdir=cqdir0
        else:
            btspd=bspd0
            btdir=bdir0

        if(cqvmax0 > 0.0):
            bvmax=cqvmax0
        else:
            bvmax=bvmax0

        if(cqlat0 > -88.0 and cqlat0 < 88.0):
            btlat=cqlat0
            btlon=cqlon0
        else:
            btlat=blat0
            btlon=blon0

        if(verb):
            print 'CCCCCCCCCCCiiiQQQ ',cqdir0,cqspd0,cqlat0,cqlon0
            print 'CCCCCCCCCCCiiibbb ',bdir0,bspd0,blat0,blon0
            print 'CCCCCCCCCCCoooooo ',btdir,btspd,btlat,btlon

        return(btlat,btlon,btdir,btspd,bvmax)


    def lsBT(self):

        dtgs=self.btrk.keys()
        dtgs.sort()

        for dtg in dtgs:

            btdic=self.btrk[dtg]
            print 'BestTrk(ls): ',dtg,btdic





class BestTrk2(MFbase):

    def __init__(self,dtgs=[],btcs={}):

        self.dtgs=dtgs
        self.btcs=btcs
        self.btrk={}
        dtgs.sort()
        
        for dtg in dtgs:

            # -- reorder new btcs to old
            #

            (btlat,btlon,btvmax,btpmin,
             btdir,btspd,
             tccode,wncode,
             cqtrkdir,cqtrkspd,cqdirtype,
             b1id,tdo,ntrk,ndtgs,
             r34m,r50m,alf,sname,
             r34,r50,depth)=btcs[dtg]

            # -- form consistent with BT in AD.py (mdecks)
            #
            if(btpmin == None): btpmin=-9999.

            self.btrk[dtg]=[btlat,btlon,float(btvmax),float(btpmin),btdir,btspd,tccode,wncode]

            # -- form from mdecks2
            #self.btrk[dtg]=[btlat,btlon,btvmax,btpmin,btdir,btspd,tccode,wncode]

            continue

            #(btlat,btlon,btvmax,btpmin,btdir,btspd,btdic,cqdic,bwdic,r34quad,r50quad)=btcs[dtg]
            #[flgtc,flgind,flgcq,flgwn,tdo,lf,cqlat,cqlon,cqvmax,wnlat,wnlon,wnvmax,tsnum]=btdic
            #[cqlat,cqlon,cqvmax,cqdir,cqspd,cqpmin]=cqdic
            #[bvmax,r34,r50,rmax,reye,poci,roci,tcdepth]=bwdic

            # from MD.py:
            #btdic=[blat,blon,bvmax,bpmin,bdir,bspd]
            #cqdic=[cqlat,cqlon,cqvmax,cqpmin,cqdir,cqspd]
            #wndic=[wlat,wlon,wvmax]
            #fldic=[flgtc,flgind,flgcq,flgwn,tdo,lf,tsnum]
            #stdic=[bvmax,r34,r50,rmax,reye,poci,roci,tcdepth]

            #btdic=[btlat,btlon,btvmax,btpmin,btdir,btspd]
            #cqdic=[cqlat,cqlon,cqvmax,cqpmin,cqdir,cqspd]
            #wndic=[wnlat,wnlon,wnvmax]
            #fldic=[flgtc,flgind,flgcq,flgwn,tdo,lf,tsnum]
            #stdic=[btvmax,r34,r50,rmax,reye,poci,roci,tcdepth]
            #self.btcs[dtg]=[btdic,cqdic,wndic,stdic,fldic,stdic,r34quad,r50quad]


    def getwbt(self,dtg):

        print 'GGG ',dtg
        btc=self.btcs[dtg]

        [btdic,cqdic,wndic,stdic,fldic,stdic,r34quad,r50quad]=btc

        [btlat,btlon,btvmax,btpmin,btdir,btspd]=btdic
        [cqlat,cqlon,cqvmax,cqpmin,cqdir,cqspd]=cqdic
        [wnlat,wnlon,wnvmax]=wndic
        [flgtc,flgind,flgcq,flgwn,tdo,lf,tsnum]=fldic

        [btvmax,r34,r50,rmax,reye,poci,roci,tcdepth]=stdic

        print cqdic
        print fldic

        return(0)

    def selectBestBtCqTau0(self,dtg,verb=0):

        try:
            btc=self.btcs[dtg]
        except:
            return(None,None,None,None,None)

        (btlat,btlon,btvmax,btpmin,
         btdir,btspd,
        tccode,wncode,
        cqtrkdir,cqtrkspd,cqdirtype,
        b1id,tdo,ntrk,ndtgs,
        r34m,r50m,alf,sname,
        r34,r50,depth)=btc
        
        # -- either CARQ or BT dir/spd/vmax ALWAYS goes into btdir/btspd/btvmax
        #    if(cqdirtype == 'C'): -- comes from CARQ tau0  BT -> cqtrkdir/spd
        #    if(cqdirtype == 'B'): -- comes from BT  BT-> cqtrkdir/spd
        #

        return(btlat,btlon,btdir,btspd,btvmax)


    def lsBT(self,dtgopt=None):

        dtgs=self.btrk.keys()
        dtgs.sort()
        
        tdtgs=dtgs
        if(dtgopt != None): tdtgs=mf.dtg_dtgopt_prc(dtgopt)

        for dtg in dtgs:

            if(not(dtg in tdtgs)): continue
            
            btdic=self.btrk[dtg]
            blat=btdic[0]
            blon=btdic[1]
            bvmax=btdic[2]
            bpmin=btdic[3]
            bdir=btdic[4]
            bspd=btdic[5]
            tccode=btdic[6]
            wncode=btdic[7]
            (clat,clon)=Rlatlon2Clatlon(blat,blon)
            print "%s      %s %s %3.0f %4.0f  D/S: %03.0f/%02.0f  T/W: %s/%s"%(dtg,clat,clon,bvmax,bpmin,bdir,bspd,tccode,wncode)            





class Trkdata(MFbase):


    def __init__(self,
                 rlat,
                 rlon,
                 vmax,
                 pmin=undef,
                 dir=undef,
                 spd=undef,
                 tccode='XX',
                 wncode='XX',
                 trkdir=undef,
                 trkspd=undef,
                 dirtype='X',
                 b1id='X',
                 tdo='XXX',
                 ntrk=0,
                 ndtgs=0,
                 r34m=undef,
                 r50m=undef,
                 r34=undef,
                 r50=undef,
                 alf=undef,
                 depth='X',
                 poci=undef,
                 roci=undef,
                 rmax=undef,
                 ):


        self.undef=undef
        self.rlat=rlat
        self.rlon=rlon
        self.vmax=vmax


        if(pmin  != self.undef):  self.pmin=pmin
        if(dir   != self.undef):  self.dir=dir
        if(spd   != self.undef):  self.spd=spd
        if(tccode != 'XX'):       self.tccode=tccode
        if(wncode != 'XX'):       self.wncode=wncode
        if(trkdir != self.undef): self.trkdir=trkdir
        if(trkspd != self.undef): self.trkdir=trkspd
        if(dirtype != 'X'):       self.dirtype=dirtype
        if(b1id    != 'X'):       self.b1id=b1id
        if(tdo     != 'XXX'):     self.tdo=tdo
        self.ntrk=ntrk
        self.ndtgs=ndtgs
        if(r34    != self.undef):  self.r34=r34
        if(r50    != self.undef):  self.r50=r50
        if(r34m   != self.undef):  self.r34m=r34m
        if(r50m   != self.undef):  self.r50m=r50m
        if(alf    != self.undef):  self.alf=alf
        if(depth  != 'X'):         self.depth=depth
        if(poci  != self.undef):   self.poci=poci
        if(roci  != self.undef):   self.roci=roci
        if(rmax  != self.undef):   self.rmax=rmax


    def gettrk(self):

        trk=(self.rlat,self.rlon,self.vmax,self.pmin,
             self.dir,self.spd,
             self.tccode,self.wncode,
             self.trkdir,self.trkspd,self.dirtype,
             self.b1id,self.tdo,self.ntrk,self.ndtgs,
             self.r34m,self.r50m,self.alf,self.sname,
             self.r34,self.r50,self.depth,
             )

        return(trk)


    def getposit(self):

        posit=(self.rlat,self.rlon,self.vmax,self.pmin,
               self.dir,self.spd,self.tccode,
               )
        return(posit)



class TcData(MFbase):

    """object for getting TC data"""

    # -- max NN number
    #
    maxNNnum=maxNNnum

    ncycles=10
    nsleep=0
    sleepytime=20.0

    distmin=90.0
    distmin9X=180.0
    distminCC=300.0
    doSubbasin=-1

    def __init__(self,
                 years=None,
                 dtgopt=None,
                 stmopt=None,
                 DSs=None,
                 verb=0,
                 backup=0,
                 doclean=0,
                 md2tag=None,
                 stmdtg=None,
                 basinopt=None,
                 #cacheOverride=0,
                 #keepPrevYears=0,
                 cpMD2name='copy',
                 doWorkingBT=0,
                 doBdeck2=0,
                 ):


        if(stmdtg != None and md2tag == None):
            year=int(stmdtg[0:4])
            years=[year]

        self.verb=verb
        self.backup=backup
        self.doclean=doclean
        self.mdstate=0
        self.doWorkingBT=doWorkingBT
        self.doBdeck2=doBdeck2
        self.years=None
        
        if(years != None):
            self.initmdDSsS(years)
        elif(dtgopt == None and md2tag == None and years == None and DSs == None and stmopt == None):
            curdtg=mf.dtg()
            years=getMd2Years(dtgopt=curdtg)
            self.years=years
            self.initmdDSsS(years)
        elif(dtgopt != None and md2tag == None):
            years=getMd2Years(dtgopt=dtgopt)
            self.years=years
            self.initmdDSsS(years)
        elif(stmopt != None and md2tag == None):
            years=getMd2Years(stmopt=stmopt)
            self.years=years
            self.initmdDSsS(years)
        else:
            #-- open old way
            #
            self.initmdDSs(DSs,md2tag)


    def getStmidFrom3id(self,snum,dtg):

        stmyear=dtg[0:4]
        if(isShemBasinStm(snum)):
            stmyear=getShemYear(dtg)

        stmid="%s.%s"%(snum.upper(),stmyear)

        return(stmid)


    def getDtg(self,dtg,renameSubbasin=1,verb=0,dobt=0,dupchk=1,selectNN=1,doGenStms=0,
               genwindowExpand=0,
               filtTCs=0):

        # -- check if dtg is 0/6/12/18Z
        #
        (rc,dt0)=MF.isSynopticHour(dtg)

        # -- do t interp of trk objects
        #
        if(rc == 0):

            dtg0=mf.dtginc(dtg,-dt0)
            dtg1=mf.dtginc(dtg,ddtgTrack-dt0)

            (otrk0,genstmids0)=self.getTCtrkDtg(dtg0,dobt=dobt,dupchk=dupchk,selectNN=selectNN,genwindowExpand=genwindowExpand)
            (otrk1,genstmids1)=self.getTCtrkDtg(dtg1,dobt=dobt,dupchk=dupchk,selectNN=selectNN,genwindowExpand=genwindowExpand)
            (otrk,genstmids)=self.interpTrkdataObjects(otrk0,genstmids0,otrk1,genstmids1,dt0)

        else:
            (otrk,genstmids)=self.getTCtrkDtg(dtg,dobt=dobt,verb=verb,dupchk=dupchk,selectNN=selectNN,genwindowExpand=genwindowExpand)

        stmids=otrk.keys()
        
        btcs={}
        nstmids=[]

        if(doGenStms): stmids=genstmids

        for stmid in stmids:
            if(renameSubbasin):
                nstmid=self.getSubbasinStmid(stmid)
                if(nstmid == None): nstmid=stmid
            else:
                nstmid=stmid
            
            tccode=otrk[stmid].tccode
            if(filtTCs and not(IsTc(tccode))):
                continue
            else:
                btcs[nstmid]=otrk[stmid].gettrk()
                nstmids.append(nstmid)
                
        return(nstmids,btcs)


    def getStmidDtg(self,dtg,dobt=0,dupchk=1,selectNN=1,verb=0):
        (stmids,btcs)=self.getDtg(dtg,dobt=dobt,dupchk=dupchk,selectNN=selectNN,verb=verb)
        return(stmids)


    def getStmidDtgs(self,dtgs,dobt=0,dupchk=1,selectNN=1):
        allstmids=[]
        for dtg in dtgs:
            stmids=self.getDSsDtg(dtg,dobt=dobt,dupchk=dupchk,selectNN=selectNN)
            allstmids=allstmids+stmids
        allstmids=mf.uniq(allstmids)
        return(allstmids)

    def getGenStmidsByDtg(self,dtg,dupchk=1,selectNN=1,
                          genwindowExpand=0):
        allstmids=[]
        (stmids,btcs)=self.getDtg(dtg,dupchk=dupchk,selectNN=selectNN,doGenStms=1)
        allstmids=allstmids+stmids
        allstmids=mf.uniq(allstmids)
        return(allstmids)

    def getGenStmidsByDtgGenBasin(self,dtg,basin,dupchk=1,selectNN=1,
                                  genwindowExpand=0):
        
        genb1ids=TcGenBasin2B1ids[basin]

        allstmids=[]
        (stmids,btcs)=self.getDtg(dtg,dupchk=dupchk,selectNN=selectNN,doGenStms=1,
                                  genwindowExpand=genwindowExpand)
        for stmid in stmids:
            (snum,b1id,year,b2id,stm2id,stm1id)=getStmParams(stmid)
            if(b1id.lower() in genb1ids):
                allstmids.append(stmid)
        allstmids=mf.uniq(allstmids)
        return(allstmids)

    def getsTDd(self,trk,endtime,vmaxTD=25.0,vmaxMin=10.0,timeback=None):

        minvmax=1e20
        maxvmax=-1e20

        times=trk.keys()
        times.sort()
        # -- calculate dtime, assumes evenly spaced
        #
        if(len(times) > 1):
            if(len(str(times[-1])) == 10):
                dtimetrk=mf.dtgdiff(times[-2],times[-1])
            else:
                dtimetrk=times[-1]-times[-2]
        else:
            dtimetrk=12.0

        try:
            trkttime=trk[endtime]
            ntimes=times.index(endtime)+1
        except:
            trkttime=trk[times[-1]]
            ntimes=len(times)

        ndtimes=ntimes
        if(timeback != None):
            ndtimes=int(timeback)/int(dtimetrk)+1

        if(ndtimes > ntimes): ndtimes=ntimes
        
        if(len(times) == 1):
            vmax=trk[times[0]][2]
            if(vmax < 0): vmax=vmaxMin
            stdd=(vmax/vmaxTD)
            stddtime=dtime*0.5
            minvmax=maxvmax=vmax
        else:
            bn=ntimes-ndtimes+1
            en=ntimes
            stdd=0.0
            stddtime=0.0
            for n in range(bn,en):
                timem1=times[n-1]
                timem0=times[n]
                vmaxm1=trk[timem1][2]
                vmaxm0=trk[timem0][2]
                # -- check if dtg
                #
                if(len(str(timem1)) == len(str(timem0)) == 10):
                    timem1=mf.dtgdiff(timem1,endtime)
                    timem0=mf.dtgdiff(timem0,endtime)
                    
                
                if(vmaxm1 < 0): vmaxm1=vmaxMin
                if(vmaxm0 < 0): vmaxm0=vmaxMin

                if(vmaxm1 > maxvmax): maxvmax=vmaxm1
                if(vmaxm1 < minvmax): minvmax=vmaxm1
                if(vmaxm0 > maxvmax): maxvmax=vmaxm0
                if(vmaxm0 < minvmax): minvmax=vmaxm0

                dtime=timem1-timem0
                stdd=stdd+(((vmaxm1+vmaxm0)*0.5)/vmaxTD)*(dtime/24.0)
                stddtime=stddtime+dtime

        sTDd=(stdd,stddtime,trkttime[0],trkttime[1],trkttime[2],minvmax,maxvmax)


        return(sTDd)


    def getStmidBtcsDtg(self,dtg,dupchk=1,selectNN=1):
        (stmids,btcs)=self.getDtg(dtg,dupchk=dupchk,selectNN=selectNN)
        return(stmids,btcs)


    def getBtc4StmidDtg(self,stmid,dtg,dupchk=1,selectNN=1):
        btc=[]
        (istmids,btcs)=self.getDtg(dtg,dupchk=dupchk,selectNN=selectNN)
        # -- make sure stmid upcase
        stmid=stmid.upper()
        (snum,sb1id,syear,sb2id,stm2id,stm1id)=getStmParams(stmid,convert9x=1)
        if(stm1id in istmids): btc=btcs[stm1id]
        return(btc)

    def getBtcs4Stmid(self,stmid,dtg=None,dobt=0,verb=1,dupchk=1,selectNN=1):

        btcs={}

        # -- handle general 9X -- finds the correct [a-z][0-9]X based on dtg
        #
        do9x=0
        if(stmid[0] == '9' or stmid[0].isalpha()): do9x=1

        if(do9x and dtg == None):
            print 'EEE in in TcData.getBtcs4Stmid for 9x storm, must set dtg: ',stmid
            sys.exit()

        if(do9x):
            btc=self.getBtc4StmidDtg(stmid,dtg,dupchk=dupchk,selectNN=selectNN)

            # -- if no btc for 9X could be because it went to warning at this dtg; redo with selectNN=0
            if(len(btc) == 0):
                btc=self.getBtc4StmidDtg(stmid,dtg,dupchk=dupchk,selectNN=0)

            if(len(btc) == 0):
                print 'WWW tD.getBtcs4Stmid no btc for stmid: ',stmid,' dtg: ',dtg
                return(btcs)

            all9xs=self.get9Xstmids(stmid)

            final9x=None
            for all9x in all9xs:
                dss9x=self.getDSsFullStm(all9x,dobt=0)

                # for all the 9x find the one with the dtg in its dtgs...
                if(dss9x != None and dtg in dss9x.dtgs):
                    final9x=all9x
                    break

            odds=self.getDSsFullStm(final9x,dobt=0)

        else:
            odds=self.getDSsFullStm(stmid,dobt=dobt,dowarn=1)

        if(odds == None):
            print 'WWW tD.getBtcs4Stmid NO odds for stmid:',stmid,' dtg: ',dtg,' dobt: ',dobt
            return(btcs)

        dtgs=odds.dtgs
        dtgs.sort()

        for dtg in dtgs:
            rc=odds.trk[dtg].gettrk()
            btcs[dtg]=rc

        return(btcs)

    def getOtrk4Stmid(self,stmid,dtg=None,dobt=0,verb=1,dupchk=1,selectNN=1):

        # -- handle general 9X -- finds the correct [a-z][0-9]X based on dtg
        #
        do9x=0
        if(stmid[0] == '9' or stmid[0].isalpha()): do9x=1

        if(do9x and dtg == None):
            print 'EEE in in TcData.getOtrk4Stmid for 9x storm, must set dtg: ',stmid
            sys.exit()

        if(do9x):
            btc=self.getBtc4StmidDtg(stmid,dtg,dupchk=dupchk,selectNN=selectNN)

            # -- if no btc for 9X could be because it went to warning at this dtg; redo with selectNN=0
            if(len(btc) == 0):
                btc=self.getBtc4StmidDtg(stmid,dtg,dupchk=dupchk,selectNN=0)

            if(len(btc) == 0):
                print 'WWW tD.getBtcs4Stmid no btc for stmid: ',stmid,' dtg: ',dtg
                return(btcs)

            all9xs=self.get9Xstmids(stmid)

            final9x=None
            for all9x in all9xs:
                dss9x=self.getDSsFullStm(all9x,dobt=0)

                # for all the 9x find the one with the dtg in its dtgs...
                if(dss9x != None and dtg in dss9x.dtgs):
                    final9x=all9x
                    break

            odds=self.getDSsFullStm(final9x,dobt=0)

        else:
            odds=self.getDSsFullStm(stmid,dobt=dobt)

        if(odds == None):
            print 'WWW tD.getOtrk4StmidNO odds for stmid:',stmid,' dtg: ',dtg
            return(odds)

        return(odds)

    def getBtLatLonVmax(self,stmid,stmdtg=None,dupchk=1,selectNN=1):

        btcs=self.getBtcs4Stmid(stmid,dtg=stmdtg,dupchk=dupchk,selectNN=selectNN)

        dtgs=btcs.keys()
        dtgs.sort()

        obts={}

        for dtg in dtgs:
            btc=btcs[dtg]
            lat=btc[0]
            lon=btc[1]
            vmax=btc[2]
            obts[dtg]=(lat,lon,vmax)

        return(obts)

    def getBtLatLonVmaxPmin(self,stmid,stmdtg=None,dupchk=1,selectNN=1):

        btcs=self.getBtcs4Stmid(stmid,dtg=stmdtg,dupchk=dupchk,selectNN=selectNN)

        obts=None

        dtgs=btcs.keys()
        dtgs.sort()

        for dtg in dtgs:
            btc=btcs[dtg]
            lat=btc[0]
            lon=btc[1]
            vmax=btc[2]
            pmin=btc[3]
            if(pmin == None): pmin=-999
            obts=(lat,lon,vmax,pmin)

        return(obts)



    def getRawStm2idDtg(self,dtg,dobt=0,verb=0,warn=0,dupchk=0,selectNN=1,
                            renameSubbasin=1):
        """get Trkdata objects by dtg directly from md2 dataset
used by getDtg
"""
        ostm2ids={}

        key=dtg
        keydtgs=self.mddtgs

        if(dobt):
            key=key+'.bt'
            keydtgs=self.mddtgsBT

        keydtgs=mf.uniq(keydtgs)

        if(key in keydtgs):

            # -- first get correct stm1id using lsDSsDtgs
            #
            rstm1ids={}
            (itrk,genstmids)=self.getTCtrkDtg(dtg,dobt=dobt,dupchk=dupchk,selectNN=selectNN,verb=verb)
            otrk=itrk
            
            stm1ids=otrk.keys()
            stm1ids.sort()
            stm1ids=sortStmids(stm1ids)
            for stm1id in stm1ids:

                trk=otrk[stm1id]
                fstm1id=self.getFinalStm1idFromRlonTcnames(stm1id,trk.rlon,trk.b1id,verb=verb)
                nstmid=self.getSubbasinStmid(fstm1id)
                if(nstmid == None): nstmid=fstm1id
                
                # -- convert the subbasin stm1id to basin stm1id for the raw stm2id below...
                #
                (xsnum,xb1id,xyear,xb2id,xstm2id,xstm1id)=getStmParams(stm1id)
                (xsnum,xb1id,xyear,xb2id,xstm2id,xstm1id)=getStmParams(xstm2id)
                
                stm1id=xstm1id
                rstm1ids[stm1id]=nstmid

            # -- now get the dds for the rstm2ids
            #
            mdDObjS=None
            if(hasattr(self,'mdD')):  
                mdDObj=self.mdD
            else:
                (rc,year,shemyear)=getNhemShemYearsFromDtg(dtg)
                
                mdDObj=self.mdDs[year]
                if(shemyear != year):
                    mdDObjS=self.mdDs[shemyear]
            
            ddsS=None
            dds=mdDObj.getDataSet(key=key)
            if(mdDObjS != None): ddsS=mdDObjS.getDataSet(key=key)
            
            # -- case where no storms in nhem, but some in shem
            #
            if(dds == None and ddsS != None): dds=ddsS
            
            # -- bail if dataset not there...
            #
            if(dds == None and ddsS == None):
                if(warn): print 'WWW(TcData.getTCtrkDtg) return None for getDataSet key: ',key,'ostmids: ',ostmids
                return(ostm2ids)
            
            if(verb): 
                dds.ls()
                if(ddsS != None): ddsS.ls()
            
            rstm2ids=dds.ostm2ids
            for rstm2id in rstm2ids:
                dds=self.getDSsFullStm(rstm2id)
                genstm2id='XXXX.XXXX'
                if(hasattr(dds,'stmidNN')): 
                    genstm1id=dds.stmidNN
                    (xsnum,xb1id,xyear,xb2id,genstm2id,xstm1id)=getStmParams(genstm1id)   
                
                (snum,sb1id,syear,sb2id,stm2id,stm1id)=getStmParams(rstm2id,convert9x=1)
                (snum,sb1id,syear,sb2id,stm2id,stm1id9)=getStmParams(rstm2id,convert9x=0)
                # -- check if weird NN gets in -- eg 50L.14
                #
                if(IsValidStmid(stm1id) and stm1id in rstm1ids.keys()):
                    rstm1id=rstm1ids[stm1id]    
                    ostm2ids[rstm1id]=(rstm2id,genstm2id)

            if(ddsS != None):
                
                rstm2ids=ddsS.ostm2ids
                for rstm2id in rstm2ids:
                    dds=self.getDSsFullStm(rstm2id)
                    genstm2id='XXXX.XXXX'
                    if(hasattr(dds,'stmidNN')): 
                        genstm1id=dds.stmidNN
                        (xsnum,xb1id,xyear,xb2id,genstm2id,xstm1id)=getStmParams(genstm1id)   
                    
                    (snum,sb1id,syear,sb2id,stm2id,stm1id)=getStmParams(rstm2id,convert9x=1)
                    # -- check if weird NN gets in -- eg 50L.14
                    #
                    if(IsValidStmid(stm1id)):
                        rstm1id=rstm1ids[stm1id]    
                        ostm2ids[rstm1id]=(rstm2id,genstm2id)
                    
        return(ostm2ids)
                
    def getRawStm1idDtg(self,dtg,dobt=0,verb=0,warn=0,dupchk=0,selectNN=1,
                            renameSubbasin=1):
        """get Trkdata objects by dtg directly from md2 dataset
used by getDtg
"""
        ostm1ids=[]
        ostm1ids={}
        
        key=dtg
        keydtgs=self.mddtgs

        if(dobt):
            key=key+'.bt'
            keydtgs=self.mddtgsBT

        keydtgs=mf.uniq(keydtgs)

        if(key in keydtgs):

            # -- first get correct stm1id using lsDSsDtgs
            #
            rstm1ids={}
            (itrk,genstmids)=self.getTCtrkDtg(dtg,dobt=dobt,dupchk=dupchk,selectNN=selectNN,verb=verb)
            otrk=itrk
            
            stm1ids=otrk.keys()
            stm1ids.sort()
            stm1ids=sortStmids(stm1ids)
            for stm1id in stm1ids:

                trk=otrk[stm1id]
                fstm1id=self.getFinalStm1idFromRlonTcnames(stm1id,trk.rlon,trk.b1id,verb=verb)
                nstmid=self.getSubbasinStmid(fstm1id)
                if(nstmid == None): nstmid=fstm1id
                
                # -- convert the subbasin stm1id to basin stm1id for the raw stm2id below...
                #
                (xsnum,xb1id,xyear,xb2id,xstm2id,xstm1id)=getStmParams(stm1id)
                (xsnum,xb1id,xyear,xb2id,xstm2id,xstm1id)=getStmParams(xstm2id)
                
                stm1id=xstm1id
                rstm1ids[stm1id]=nstmid

            # -- now get the dds for the rstm2ids
            #
            mdDObjS=None
            if(hasattr(self,'mdD')):  
                mdDObj=self.mdD
            else:
                (rc,year,shemyear)=getNhemShemYearsFromDtg(dtg)
                
                mdDObj=self.mdDs[year]
                if(shemyear != year):
                    try:
                        mdDObjS=self.mdDs[shemyear]
                    except:
                        None
            
            ddsS=None
            dds=mdDObj.getDataSet(key=key)
            if(mdDObjS != None): ddsS=mdDObjS.getDataSet(key=key)
            
            # -- case where no storms in nhem, but some in shem
            #
            if(dds == None and ddsS != None): dds=ddsS
            
            # -- bail if dataset not there...
            #
            if(dds == None and ddsS == None):
                if(warn): print 'WWW(TcData.getRasStm1idDtg) return None for getDataSet key: ',key,'ostmids: ',ostmids
                return(ostm1ids)
            
            if(verb): 
                dds.ls()
                if(ddsS != None): ddsS.ls()
                
            rstm2ids=dds.ostm2ids

            for rstm2id in rstm2ids:
                dds=self.getDSsFullStm(rstm2id)
                (snum,sb1id,syear,sb2id,stm2id,stm1id)=getStmParams(rstm2id,convert9x=0)
                (snum,sb1id,syear,sb2id,stm2id,stm1id9)=getStmParams(rstm2id,convert9x=1)
                if(IsValidStmid(stm1id) and stm1id in rstm1ids.keys()):
                    ostm1ids[stm1id]=stm1id
                elif(IsValidStmid(stm1id9) and stm1id9 in rstm1ids.keys()):
                    ostm1ids[stm1id.upper()]=rstm1ids[stm1id9]

            if(ddsS != None):
                
                rstm2ids=ddsS.ostm2ids
                for rstm2id in rstm2ids:
                    dds=self.getDSsFullStm(rstm2id)
                    (snum,sb1id,syear,sb2id,stm2id,stm1id)=getStmParams(rstm2id,convert9x=0)
                    # -- check if weird NN gets in -- eg 50L.14
                    #
                    (snum,sb1id,syear,sb2id,stm2id,stm1id9)=getStmParams(rstm2id,convert9x=1)
                    if(IsValidStmid(stm1id) and stm1id in rstm1ids.keys()):
                        ostm1ids[stm1id]=stm1id
                    elif(IsValidStmid(stm1id9) and stm1id9 in rstm1ids.keys()):
                        ostm1ids[stm1id]=rstm1ids[stm1id9]
                
        return(ostm1ids)
                
            
            

    def getTCtrkDtg(self,dtg,dobt=0,verb=0,warn=0,dupchk=0,selectNN=1,
                    genwindowExpand=0,
                    renameSubbasin=1):
        
        def getotrkgenstmids(dtg,year):
            """get Trkdata objects by dtg directly from md2 dataset
            used by getDtg
            """
            otrk={}
            stm1ids=[]
            rstm2ids={}
            ostm2ids={}
            genstmids=[]
    
            key=dtg
            keydtgs=self.mddtgs
    
            if(dobt):
                key=key+'.bt'
                keydtgs=self.mddtgsBT
    
            keydtgs=mf.uniq(keydtgs)
    
            if(key in keydtgs):

                otrkS=genstmidsS=None
    
                if(hasattr(self,'mdD')):  
                    mdDObj=self.mdD
                else:
                    # -- 20170703 -- will try to get shem year...if no storms yet will fail...
                    try:
                        mdDObj=self.mdDs[year]
                    except:
                        mdDObj=None
                        
                if(mdDObj == None):
                    dds=None
                else:
                    dds=mdDObj.getDataSet(key=key)
                
                # -- bail if dataset not there...
                #
                if(dds == None):
                    if(warn): print 'WWW(TcData.getTCtrkDtg) return None for getDataSet key: ',key
                    return(otrk,genstmids,0)
                
                if(verb): dds.ls()
    
                stm2ids=dds.trks.keys()
                stm2ids.sort()
                
                doprint=0
                set9xfirst=0
                for stm2id in stm2ids:
                    stm1id=stm2idTostm1id(stm2id)
                    stm1ids.append(stm1id)
                    ostm2ids[stm1id]=stm2id
    
                    # -- get storm dss and look for dtg in gendtgs force dobt=1
                    #
                    ddsS=self.getDSsFullStm(stm2id,dobt=1,set9xfirst=set9xfirst,doprint=doprint,dowarn=0)
                    tgendtgs=None
                    if(ddsS != None and hasattr(ddsS,'gendtgs')): 
                        tgendtgs=ddsS.gendtgs
                        if(genwindowExpand > 0):
                            if(verb): print 'BBBBBBBBBBBB: ',tgendtgs,genwindowExpand
                            btdtg=tgendtgs[0]
                            etdtg=tgendtgs[-1]
                            btdtg=mf.dtginc(btdtg,-genwindowExpand)
                            etdtg=mf.dtginc(etdtg,+genwindowExpand)
                            tgendtgs=mf.dtgrange(btdtg,etdtg)
                            if(verb): print 'EEEEEEEEEEE: ',tgendtgs
                        
                    if(tgendtgs != None and (dtg in tgendtgs)): genstmids.append(stm2id)
    
    
                stm1ids=mf.uniq(stm1ids)
                stm1ids.sort()
                
    
                # -- process genstmids
                #
                ogenstmids=[]
                for genstmid in genstmids:
    
                    (snum,sb1id,syear,sb2id,stm2id,stm1id)=getStmParams(genstmid,convert9x=1)
    
                    if(renameSubbasin):
                        ngenstmid=self.getSubbasinStmid(stm1id)
                        if(ngenstmid == None): ngenstmid=stm1id
                    else:
                        ngenstmid=stm1id
    
                    if(int(snum) > self.maxNNnum):
                        continue
                    else:
                        ogenstmids.append(ngenstmid)
    
                genstmids=ogenstmids
    
                # -- process all stmids
                #
                for stm1id in stm1ids:
                    (snum,sb1id,syear,sb2id,stm2id,stm1id)=getStmParams(stm1id,convert9x=1)
    
                    # -- sanity check; toss storms > 60 < 90
                    #
                    if(int(snum) > self.maxNNnum and int(snum) < 90): continue
    
                    stm2id=ostm2ids[stm1id]
                    trk=dds.trks[stm2id]
                    if(verb): trk.ls()
    
                    if(renameSubbasin):
                        nstm1id=self.getSubbasinStmid(stm1id)
                        if(nstm1id == None): nstm1id=stm1id
                    else:
                        nstm1id=stm1id
    
                    otrk[nstm1id]=trk
    
            if(dupchk):
                otrk=self.dupTCtrkDtg(otrk,genstmids,selectNN=selectNN,verb=verb)
                
            return(otrk,genstmids,1)
        
        (rc,year,shemyear)=getNhemShemYearsFromDtg(dtg)
        
        (otrk,genstmids,rcyear)=getotrkgenstmids(dtg,year)
        rcyearS=0
        if(shemyear != year):
            (otrkS,genstmidsS,rcyearS)=getotrkgenstmids(dtg,shemyear)
            otrk.update(otrkS)
            genstmids=genstmids+genstmidsS
        if(rcyear == 0 and rcyearS == 0):
            print 'WWW.getTCtrkDtg.getotrkgenstmids(): no stmids for dtg:',dtg
        return(otrk,genstmids)



    def getDSsDtg(self,dtg,dobt=0,dupchk=0,verb=0,selectNN=1):

        ostmids=[]
        if(dtg in self.mddtgs):
            (itrk,genstmids)=self.getTCtrkDtg(dtg,dobt=dobt,verb=verb)
            otrk=itrk

            if(dupchk):
                otrk=self.dupTCtrkDtg(itrk,genstmids,selectNN=selectNN)

            stm1ids=otrk.keys()
            stm1ids.sort()
            stm1ids=sortStmids(stm1ids)
            
            for stm1id in stm1ids:

                trk=otrk[stm1id]
                fstm1id=self.getFinalStm1idFromRlonTcnames(stm1id,trk.rlon,trk.b1id,verb=verb)
                ostmids.append(fstm1id)

        return(ostmids)


    def getDSsDtgBtcs(self,dtg,dobt=0,dupchk=0,verb=0,selectNN=1):

        btcs={}
        ostmids=[]
        if(dtg in self.mddtgs):
            (itrk,genstmids)=self.getTCtrkDtg(dtg,dobt=dobt,verb=verb)
            otrk=itrk

            if(dupchk):
                otrk=self.dupTCtrkDtg(itrk,genstmids,selectNN=selectNN)

            stm1ids=otrk.keys()
            stm1ids.sort()
            stm1ids=sortStmids(stm1ids)
            for stm1id in stm1ids:

                trk=otrk[stm1id]
                gentrk=0

                fstm1id=self.getFinalStm1idFromRlonTcnames(stm1id,trk.rlon,trk.b1id,verb=verb)
                btcs[fstm1id]=trk.gettrk()
                ostmids.append(fstm1id)

        return(ostmids,btcs)


    def getFinalStm1idFromRlonTcnames(self,stm1id,rlon,b1id,verb=0):

        (snum,sb1id,syear,sb2id,stm2id,stm1id)=getStmParams(stm1id)

        fstm1id=stm1id
        if(int(snum) <= maxNNnum):
            try:
                fstm1id=self.stmD.stm2idTOstm1id[stm2id].upper()
            except:
                None
        else:
            fstm1id=stm1id

        # -- case where b1id from a/bdecks is good
        #
        if(isIoShemSubbasinB1id(b1id)):
            fstm1id=fstm1id[0:2]+b1id+fstm1id[3:]
        elif(fstm1id == stm1id and IsIoShemBasin(sb2id) and b1id == None):
            fb1id=getIoShemB1idFromRlon(sb2id,rlon)
            fstm1id=fstm1id[0:2]+fb1id+fstm1id[3:]
            
        # -- look at TCnames
        #
        nstmid=self.getSubbasinStmid(fstm1id)
        if(nstmid == None): nstmid=fstm1id
        if(verb): print 'getFinalSTm1idFromRlonTcname ',stm1id,stm2id,fstm1id

        return(fstm1id)

    def getStmNameMD2(self,stmid):

        ocards=self.lsDSsStmCards(stmid)
        odtgs=ocards.keys()
        odtgs.sort()
        tt0=ocards[odtgs[-3]].split()
        tt1=ocards[odtgs[-2]].split()
        if(len(tt1) == 18): 
            sname=tt1[-1]
        elif(len(tt0) == 18):
            sname=tt0[-1]
        else:
            print 'III (TcData.getStmNameMD2) - problem with mdecks for: ',stmid,' returning None'
            sname=None
        
        return(sname)
        
        

    def getStmName3id(self,stmid):

        stm3id=stmid.split('.')[0].upper()
        stmyear=stmid.split('.')[1]

        tcnames=self.GetTCnamesHash(stmyear)

        kk=tcnames.keys()

        stmname='unknown'
        stmname=stmname.upper()

        for k in kk:
            stm3=k[1]
            if(stm3 == stm3id): stmname=tcnames[k]
            

        return(stm3id,stmname)

    def getSubbasinStmid(self,stmid):

        (snum,b1id,year,b2id,stm2id,stm1id)=getStmParams(stmid)
        stm3id=stm1id.split('.')[0].upper()
        stmyear=stm1id.split('.')[1]
        
        tcnames=self.GetTCnamesHash(stmyear)

        kk=tcnames.keys()

        stmname='unknown'
        stmname=stmname.upper()

        stmFullid=stmid
        if(isIoShemSubbasinStm1id(stmid)):
            stmFullid=stmid
            return(stmFullid)


        # -- only look for IO/SHEM subbasins in the tcnames.keys() if not a specific io/shem subbasin, i.e., 'i' or 's' or 'h'
        #
        for k in kk:
            stm3=k[1]
            if(isIoShemSubbasin(stmid,stm3)):
                stmFullid="%s.%s"%(stm3,stmyear)
                return(stmFullid)

        return(stmFullid)

    def get9XSubbasinFromStmid(self,stmid,doupper=1,warn=1):

        (snum,sb1id,syear,sb2id,stm2id,stm1id)=getStmParams(stmid)
        
        # -- this will always be true for ANY shem subbasin -- for 9X get the sub basin from the intial position
        #
        if(IsIoShemBasin(sb2id)):
            dds=self.getDSsFullStm(stm1id,dobt=0)
            if(dds != None):
                (trk,dtgs)=dds.getMDotrk()
                if(len(dtgs) > 0):
                    rlon=trk[dtgs[0]].rlon
                    fb1id=getIoShemB1idFromRlon(sb2id,rlon)
                    fstm1id=stm1id[0:2]+fb1id+stm1id[3:]
                else:
                    if(warn): print 'WWW warning in TcData.get9XSubbasinFromStmid() -- 0 length track for: ',stm1id
                    fstm1id=stm1id
                
            else:
                fstm1id=stm1id
        else:
            fstm1id=stm1id
            
        if(doupper): fstm1id=fstm1id.upper()
            
        return(fstm1id)

    def GetTCnamesHash(self,yyyy,source=''):

        from tcbase import TcNamesDatDir
        ndir=TcNamesDatDir
        sys.path.append(ndir)
        if(source == 'neumann'):
            impcmd="from TCnamesNeumann%s import tcnames"%(yyyy)
        else:
            impcmd="from TCnames%s import tcnames"%(yyyy)
            exec(impcmd)
        return(tcnames)


    def getStmStats(self,stmid):
        
        stm3id=stmid.split('.')[0].upper()
        stmyear=stmid.split('.')[1]
    
        tcstats=GetTCstatsHash(stmyear)
    
        kk=tcstats.keys()
    
        tcstat=[]
        for k in kk:
            stm3=k[1]
            if(stm3 == stm3id): tcstat=tcstats[k]
    
        return(tcstat)



    def interpTrkdataObjects(self,otrk0,genstmids0,otrk1,genstmids1,dt0,ddtgtrk=ddtgTrack):

        # -- gen stmids
        #
        genstmidsi=[]
        for genstmid in genstmids0:
            if(genstmid in genstmids1):
                genstmidsi.append(genstmid)

        # -- tracks objects
        #
        otrki={}

        stmids0=otrk0.keys()
        stmids1=otrk1.keys()
        fact1=dt0*1.0/ddtgtrk
        fact0=(1.0 - fact1)

        for stmid in stmids0:

            if(stmid in stmids1):

                trk0=otrk0[stmid]
                trk1=otrk1[stmid]

                trki=self.interpTrkdataObj(trk0,trk1,fact0,fact1)

                otrki[stmid]=trki

        return(otrki,genstmidsi)


    def interpTrkdataObj(self,trk0,trk1,fact0,fact1):

        trki=copy.deepcopy(trk0)

        dir0=trk0.dir
        dir1=trk1.dir
        diri=dir0*fact0 + dir1*fact1

        spd0=trk0.spd
        spd1=trk1.spd
        spdi=spd0*fact0 + spd1*fact1

        rlat0=trk0.rlat
        rlat1=trk1.rlat
        rlati=rlat0*fact0 + rlat1*fact1

        rlon0=trk0.rlon
        rlon1=trk1.rlon
        rloni=rlon0*fact0 + rlon1*fact1

        vmax0=trk0.vmax
        vmax1=trk1.vmax
        vmaxi=vmax0*fact0 + vmax1*fact1

        trkdir0=trk0.trkdir
        trkdir1=trk1.trkdir
        trkdiri=trkdir0*fact0 + trkdir1*fact1

        trkspd0=trk0.trkspd
        trkspd1=trk1.trkspd
        trkspdi=trkspd0*fact0 + trkspd1*fact1

        alf0=trk0.alf
        alf1=trk1.alf
        alfi=alf0*fact0 + alf1*fact1

        r34m0=trk0.r34m
        r34m1=trk1.r34m
        if(r34m0 != None and r34m1 != None):
            r34mi=r34m0*fact0 + r34m1*fact1
        elif(r34m0 != None and r34m1 == None):
            r34mi=r34m0
        elif(r34m0 == None and r34m1 != None):
            r34mi=r34m1
        else:
            r34mi=None

        r50m0=trk0.r50m
        r50m1=trk1.r50m
        if(r50m0 != None and r50m1 != None):
            r50mi=r50m0*fact0 + r50m1*fact1
        elif(r50m0 != None and r50m1 == None):
            r50mi=r50m0
        elif(r50m0 == None and r50m1 != None):
            r50mi=r50m1
        else:
            r50mi=None

        rmax0=trk0.rmax
        rmax1=trk1.rmax
        if(rmax0 != None and rmax1 != None):
            rmaxi=rmax0*fact0 + rmax1*fact1
        elif(rmax0 != None and rmax1 == None):
            rmaxi=rmax0
        elif(rmax0 == None and rmax1 != None):
            rmaxi=rmax1
        else:
            rmaxi=None

        roci0=trk0.roci
        roci1=trk1.roci
        if(roci0 != None and roci1 != None):
            rocii=roci0*fact0 + roci1*fact1
        elif(roci0 != None and roci1 == None):
            rocii=roci0
        elif(roci0 == None and roci1 != None):
            rocii=roci1
        else:
            rocii=None

        poci0=trk0.poci
        poci1=trk1.poci
        if(poci0 != None and poci1 != None):
            pocii=poci0*fact0 + poci1*fact1
        elif(poci0 != None and poci1 == None):
            pocii=poci0
        elif(poci0 == None and poci1 != None):
            pocii=poci1
        else:
            pocii=None

        pmin0=trk0.pmin
        pmin1=trk1.pmin
        if(pmin0 != None and pmin1 != None):
            pmini=pmin0*fact0 + pmin1*fact1
        elif(pmin0 != None and pmin1 == None):
            pmini=pmin0
        elif(pmin0 == None and pmin1 != None):
            pmini=pmin1
        else:
            pmini=None

        # -- pick which dtg to set non continuous values such as tdo
        #
        if(fact0 >= fact1):

            depthi=trk0.depth
            dirtypei=trk0.dirtype
            r34i=trk0.r34
            r50i=trk0.r50
            tccodei=trk0.tccode
            tdoi=trk0.tdo
            wncodei=trk0.wncode

        else:

            depthi=trk1.depth
            dirtypei=trk1.dirtype
            r34i=trk1.r34
            r50i=trk1.r50
            tccodei=trk1.tccode
            tdoi=trk1.tdo
            wncodei=trk1.wncode


        # -- set trki object

        trki.alf=alfi
        trki.depth=depthi
        trki.dir=diri
        trki.dirtype=dirtypei
        trki.pmin=pmini
        trki.poci=pocii
        trki.r34=r34i
        trki.r34m=r34mi
        trki.r50=r50i
        trki.r50m=r50mi
        trki.rlat=rlati
        trki.rlon=rloni
        trki.rmax=rmaxi
        trki.roci=rocii
        trki.spd=spdi
        trki.tccode=tccodei
        trki.tdo=tdoi
        trki.trkdir=trkdiri
        trki.trkspd=trkspdi
        trki.vmax=vmaxi
        trki.wncode=wncodei


        return(trki)




    def getTCvDtg(self,dtg,dobt=0,dupchk=1,selectNN=0,ddtgtrk=ddtgTrack):
        """ selectNN=0 to put 9X into tcvitals
"""

        # -- check if dtg is 0/6/12/18Z
        #
        (rc,dt0)=MF.isSynopticHour(dtg)

        # -- do t interp of trk objects
        #

        if(rc == 0):

            dtg0=mf.dtginc(dtg,-dt0)
            dtg1=mf.dtginc(dtg,ddtgtrk-dt0)
            dtginc=mf.dtgdiff(dtg0,dtg1)

            (otrk0,genstmids0)=self.getTCtrkDtg(dtg0,dobt=dobt,dupchk=dupchk,selectNN=selectNN)
            (otrk1,genstmids1)=self.getTCtrkDtg(dtg1,dobt=dobt,dupchk=dupchk,selectNN=selectNN)
            (otrki,genstmidsi)=self.interpTrkdataObjects(otrk0,genstmids0,otrk1,genstmids1,dt0,ddtgtrk=dtginc)

            trki=TrkDataDtg(dtg,otrki,genstmidsi,self.stmD)

            return(trki)

        else:

            (otrk,genstmids)=self.getTCtrkDtg(dtg,dobt=dobt,dupchk=dupchk,selectNN=selectNN)
            trk=TrkDataDtg(dtg,otrk,genstmids,self.stmD)

        return(trk)



    def get9Xstmids(self,stmid):

        stm2ids=[]
        (snum,b1id,year,b2id,stm2id,stm1id)=getStmParams(stmid)
        for stmid in self.mdstmids:
            if(mf.find(stmid,b2id.lower()) and
               mf.find(stmid,"%s."%(str(snum)[1])) and
               mf.find(stmid,year) and
               not(stmid[2].isdigit())
               ):
                stm2ids.append(stmid)

        return(stm2ids)


    def getDSsStm(self,stmid,dobt=0,verb=0):

        dds=None
        ddsALL=None
        (snum,b1id,year,b2id,stm2id,stm1id)=getStmParams(stmid)
        if(verb): print 'TcData.getDSsStm -- looking for stmid: ',stmid,stm2id
        if (stm2id in self.mdstmids):
            if(verb): print 'TcData.getDSsStm -------------- found: ',stmid,' in mdstmids'
            # -- get the year
            if(hasattr(self,'mdD')):  
                mdDObj=self.mdD
            else:
                year=int(stm2id.split('.')[-1])
                mdDObj=self.mdDs[year]
                
            if(dobt > 0):
                try:
                    dds=mdDObj.getDataSet(key=stm2id+'.bt')
                    ddsALL=mdDObj.getDataSet(key=stm2id)
                except:
                    None
            else:
                try:
                    dds=mdDObj.getDataSet(key=stm2id)
                except:
                    None

            # set vars for output dss (bt only) using values from dssALL (full mdeck)
            #
            if(dds == None): 
                # -- no .bt -- 9x -- set to all
                #
                dds=ddsALL

            if(ddsALL != None):

                if(hasattr(ddsALL,'stmid9x')): 
                    dds.stmid9x=ddsALL.stmid9x

                if(hasattr(ddsALL,'time2gen')):
                    dds.time2gen=ddsALL.time2gen
                    dds.genstdd=ddsALL.genstdd

                if(dobt == 2):
                    
                    dds.dtgs=ddsALL.dtgs
                    dds.ndtgs=ddsALL.ndtgs

                    dds.stmlife=ddsALL.stmlife
                    dds.stclife=ddsALL.stclife
                    dds.tclife=ddsALL.tclife

                    dds.latb=ddsALL.latb
                    dds.latmx=ddsALL.latmx
                    dds.latmn=ddsALL.latmn
                    
                    dds.lonb=ddsALL.lonb
                    dds.lonmx=ddsALL.lonmx
                    dds.lonmn=ddsALL.lonmn
                    
                    dds.ace=ddsALL.ace
                    dds.stcd=ddsALL.stcd
                    

        return(dds)


    def getDSsCCStm(self,stmid,dobt=0):

        dds=None
        (snum,b1id,year,b2id,stm2id,stm1id)=getStmParams(stmid)

        if (stm2id in self.mdstmidsCC):
            
            if(hasattr(self,'mdD')):  
                mdDObj=self.mdD
            else:
                year=int(stm2id.split('.')[-1])
                mdDObj=self.mdDs[year]
            
            try:
                dds=mdDObj.getDataSet(key=stm2id)
            except:
                None

        return(dds)

    def getBT4Dtg(self,dtg,dupchk=1,selectNN=1,bypassIO=1,verb=0):
        """ use rawstm1id for md2 and for pulling 9X from ad2
"""
        #(bstmids,btcs)=self.getDtg(dtg,renameSubbasin=1,dupchk=dupchk,selectNN=selectNN)
        rbstmids=self.getRawStm1idDtg(dtg,renameSubbasin=1,dupchk=dupchk,selectNN=selectNN)
        bstmids=rbstmids.keys()

        BTs={}
        fstmids=[]
        
        for bstmid in bstmids:
            gotIstm=0
            if(isShemBasinStm(bstmid)):
                (snum,b1id,byear,b2id,stm2id,stm1id)=getStmParams(bstmid)
                obstmid1=bstmid
                if(b1id.upper() == 'S'): b1id2='P'
                if(b1id.upper() == 'P'): b1id2='S'
                obstmid2="%s%s.%s"%(obstmid1[0:2],b1id2,byear)
                #print 'IIII---getATsBTs two shem stmids: ',obstmid1,obstmid2
                mstmids=self.makeStmListMdeck(obstmid1)+self.makeStmListMdeck(obstmid2)
                
            elif(isIOBasinStm(bstmid)):
                (snum,b1id,byear,b2id,stm2id,stm1id)=getStmParams(bstmid)
                
                obstmid1=bstmid
                if(b1id.upper() == 'I'): 
                    b1id='A'
                    b1id2='B'
                    obstmid1="%s%s.%s"%(bstmid[0:2],b1id,byear)
                    gotIstm=1
                    
                elif(b1id.upper() == 'A'):
                    b1id2='B'
                    
                if(b1id.upper() == 'B'): b1id2='A'
                obstmid2="%s%s.%s"%(obstmid1[0:2],b1id2,byear)
                if(gotIstm and not(bypassIO)):
                    if(verb): print 'IIII--- getATsBTs for two IO stmids: ',obstmid1,obstmid2
                    mstmids=self.makeStmListMdeck(obstmid1)+self.makeStmListMdeck(obstmid2)
                else:
                    if(verb): print 'IIII--- for IO use just I bi1d bypasssIO: ',bypassIO,' bstmid: ',bstmid
                    mstmids=[bstmid]
            else:
                mstmids=self.makeStmListMdeck(bstmid)

            if(len(mstmids) == 1):
                fstmid=mstmids[0].upper()
                fstmids.append(fstmid)
                BT=self.makeBestTrk2(fstmid)
                if(BT == None):
                    print 'WWW TcData.getBT4DTG fffffstmid: ',fstmid,' BT = None...press...'
                    continue
                
                if(gotIstm):
                    BTs[fstmid]=BT
                else:
                    BTs[bstmid]=BT
                
            else:
                for mstmid in mstmids:
                    BT=self.makeBestTrk2(mstmid)
                    if(verb): print 'BBBB--------- multiple mstmids: ',mstmid,' bstmid: ',bstmid
                    if(BT == None):
                        print 'WWW TcData.getBT4DTG mmmmmstmid: ',mstmid,' BT = None...press...'
                        continue
                    if(dtg in BT.dtgs):
                        BTs[bstmid]=BT
                        fstmids.append(mstmid.upper())
                        break

        return(BTs,bstmids,fstmids)


    def getBT4Stmid(self,stmid,dt=None,dobt=0,set9xfirst=0,verb=0):
        """ method to make BestTrk2 object interpolated to dt increment 1, 2, and 3 h
        """

        odds=self.getDSsFullStm(stmid,dobt=dobt,
                                set9xfirst=set9xfirst)


        itrk=odds.trk

        dtgs=odds.dtgs
        dtgs.sort()

        if(dt != None and not(dt == 6 or dt == 12) ):

            if((dt > 1 and dt <= 3) ):
                bdtg=dtgs[0]
                edtg=dtgs[-1]
                dtgs=mf.dtgrange(bdtg,edtg,dt)
            else:
                print 'EEE TcData.getBT4Stmid() only supports interp increments of 1, 2 and 3'
                sys.exit()

            otrk={}

            for dtg in dtgs:

                (rc,dt0)=MF.isSynopticHour(dtg)
                if(rc == 0):

                    dtg0=mf.dtginc(dtg,-dt0)
                    dtg1=mf.dtginc(dtg,ddtgTrack-dt0)

                    trk0=itrk[dtg0]
                    trk1=itrk[dtg1]

                    fact1=dt0*1.0/ddtgTrack
                    fact0=(1.0 - fact1)

                    trki=self.interpTrkdataObj(trk0,trk1,fact0,fact1)
                    otrk[dtg]=trki

                else:

                    otrk[dtg]=itrk[dtg]



            odtgs=otrk.keys()
            odtgs.sort()

            if(verb):
                for odtg in odtgs:
                    print 'ooogetBT4Stmid: %s %6.1f %6.1f'%(odtg,otrk[odtg].rlat,otrk[odtg].rlon)

        else:

            otrk=itrk
            odtgs=dtgs

        odds.trk=otrk
        odds.dtgs=odtgs


        btcs={}

        for dtg in odtgs:
            rc=odds.trk[dtg].gettrk()
            btcs[dtg]=rc

        BT=BestTrk2(dtgs,btcs)
        BT.stmid=stmid

        return(BT)





    def get9xDSs(self,dds,stmid,renameSubbasin=1,verb=0):

        stmid=stmid.upper()
        
        # -- 20120208 we really should get from the dds
        # -- 20230223 -- why?  can be a problem if during md2 processing...
        #
        try:
            stmid=dds.stm1id
        except:
            print 'WWW-TcData.get9XDSs() -- no dds.stm1id... press'
            

        if(renameSubbasin):
            nstmid=self.getSubbasinStmid(stmid)
            if(nstmid == None): nstmid=stmid
        else:
            nstmid=stmid

        stmid=nstmid


        if(hasattr(dds,'stmid9x')):
            
            (snum,b1id,year,b2id,stm2id,stm1id)=getStmParams(dds.stmid9x)
            dds9x=self.getDSsStm(stm2id)
            return(dds9x)
            
            
            

        dds9x=None

        (otrk,dtgs)=dds.getMDtrk()

        for dtg0 in dtgs:

            (trk0,genstmids)=self.getTCtrkDtg(dtg0)
            # -- 20131120 -- bail if stmid not in trk0...
            #
            try:
                tt=trk0[stmid]
            except:
                continue

            rlat1=tt.rlat
            rlon1=tt.rlon

            stmid0s=trk0.keys()
            
            for stmid0 in stmid0s:
                rlat0=trk0[stmid0].rlat
                rlon0=trk0[stmid0].rlon
                gdist=gc_dist(rlat0,rlon0,rlat1,rlon1)

                if(stmid0 != stmid and gdist <= self.distmin and stmid0[0] == '9'
                   ):
                    stmid9x=stmid0
                    ostm2id9x=trk0[stmid0].ostm2id
                    dds9x=self.getDSsStm(ostm2id9x)
                    
                    # -- return None if not there...
                    #
                    if(dds9x == None): return(dds9x)
                    dds9x.ostm2id9x=ostm2id9x

                    # -- convert 99. to [a-z]9
                    #
                    stmid9x=stm2idTostm1id(ostm2id9x)
                    dds9x.stmid9x=stmid9x

                    if(verb): print '999999999999999 ',stmid9x,stmid,dtg0,rlat0,rlon0,rlat1,rlon1,'gdist: ',gdist,ostm2id9x
                    return(dds9x)

        return(dds9x)


    def getCCDSs(self,dds,stmid,renameSubbasin=1,verb=1,diag=0):

        if(renameSubbasin):
            nstmid=self.getSubbasinStmid(stmid)
            if(nstmid == None): nstmid=stmid
        else:
            nstmid=stmid

        stmid=nstmid.upper()
        ddsCC=None

        (otrk,dtgs)=dds.getMDtrk()
        dtgs.sort()

        for dtg0 in dtgs:

            (trk0,genstmids)=self.getTCtrkDtg(dtg0,dupchk=0,selectNN=0)
            stmid9x=get9XstmidFromNewForm(stmid)
            try:
                tt=trk0[stmid9x]
            except:
                print 'EEE(tcCL.MD2trk.getCCDSs -- no trk0 for stmid9x: ',stmid9x,' better figure this out for compCC=1'
                sys.exit()                
            
            rlat1=tt.rlat
            rlon1=tt.rlon

            stmid0s=trk0.keys()

            for stmid0 in stmid0s:
                rlat0=trk0[stmid0].rlat
                rlon0=trk0[stmid0].rlon
                gdist=gc_dist(rlat0,rlon0,rlat1,rlon1)

                if(diag): print 'CCCC ',dtg0,stmid0,stmid,gdist,self.distminCC
                if(stmid0 != stmid and gdist <= self.distminCC and stmid0[0:2] == 'CC'):
                    stmidCC=stmid0
                    (snum,sb1id,syear,sb2id,stm2idCC,stm1idCC)=getStmParams(stmidCC)
                    ddsCC=self.getDSsCCStm(stmidCC)
                    if(ddsCC != None):
                        ddsCC.stmidCC=stmidCC

                    if(verb): print 'CCCCCCCCCCCCCCC ',stmidCC,stmid,dtg0,rlat0,rlon0,rlat1,rlon1,'gdist: ',gdist
                    return(ddsCC)

        return(ddsCC)


    def getNNDSs(self,dds,stmid,verb=1):

        stmid=stmid.upper()
        ddsNN=None

        (otrk,dtgs)=dds.getMDtrk()

        # -- 0 dtg to end of storm
        #
        dtg0=dtgs[-1]
        (trk0,genstmids)=self.getTCtrkDtg(dtg0)

        # -- convert to 9x form
        #
        stmid='9'+stmid[1:]

        tt=trk0[stmid]
        rlat1=tt.rlat
        rlon1=tt.rlon

        stmid0s=trk0.keys()

        for stmid0 in stmid0s:
            rlat0=trk0[stmid0].rlat
            rlon0=trk0[stmid0].rlon
            gdist=gc_dist(rlat0,rlon0,rlat1,rlon1)

            if(stmid0 != stmid and gdist <= self.distmin and stmid[0] == '9'):
                stmidNN=stmid0
                ostmidNN=trk0[stmid0].ostm2id
                ddsNN=self.getDSsStm(ostmidNN)
                if(verb): print 'NNNNNNNNNNNNNNNNN ',stmidNN,stmid,dtg0,rlat0,rlon0,rlat1,rlon1,'gdist: ',gdist,ostmidNN

        return(ddsNN)


    def getDSsFullStm(self,stmid,dobt=1,doprint=0,set9xfirst=0,dowarn=0):

        # -- new dobt option: if = 2 then merge best track into full
        #
        if(stmid == None):
            return(None)

        if(stmid[0:2] == 'CC'):
            odds=self.getDSsCCStm(stmid)
            return(odds)


        # -- 20131125 -- better logic for setting do9X
        #
        do9x=0
        (snum,b1id,year,b2id,stm2id,stm1id)=getStmParams(stmid)

        if((stm1id[0] == '9' or stm1id[0].isalpha())):
            if( (dobt == 0 or dobt == 2) ):
                do9x=1
                dobt=0
        elif(dobt == 2):
            dobt=0
                
        dds=self.getDSsStm(stmid,dobt=dobt)

        # -- add option for printing warning including a dowarn opt
        #
        if(dds == None and (IsNN(stmid) or do9x) ):
            if(dowarn): print'WWW(tcCL.getDSsFullStm): no data for stmid: ',stmid,' dobt: ',dobt,' do9x: ',do9x
            return(dds)

        # -- if dobt; only output bt -- deprecated?  because we merge vals from .bt and . in getDSsStm
        #
        if((not(do9x) and not(dobt)) or dobt == 2 ):
            dds9x=self.get9xDSs(dds,stmid)
            odds=self.merge9xDSsStm(dds,dds9x,doprint=doprint,set9xfirst=set9xfirst)
        else:
            odds=dds

        return(odds)




    def makeBestTrk2(self,stmid,dobt=0,set9xfirst=0,verb=0):


        odds=self.getDSsFullStm(stmid,dobt=dobt,
                                set9xfirst=set9xfirst)

        if(odds != None):
            dtgs=odds.dtgs
            dtgs.sort()
        else:
            BT=None
            return(BT)

        btcs={}

        for dtg in dtgs:
            rc=odds.trk[dtg].gettrk()
            btcs[dtg]=rc

        BT=BestTrk2(dtgs,btcs)
        return(BT)




    def initmdDSs(self,DSs,md2tag,md2key='md2keys'):

        from tcbase import TcDataBdir,Md2Dbname

        """ init main objects; if DSs passed in, then get db keys from
        DSs vice DSs.getDataSet(key='md2keys')"""

        dsbdir="%s/DSs"%(TcDataBdir)
        dbname=Md2Dbname
        verb=1
        if(md2tag != None): dbname='mdecks2-%s'%(md2tag)
        dbfile="%s.pypdb"%(dbname)

        dbpath="%s/%s"%(dsbdir,dbfile)

        self.dsbdir=dsbdir
        self.dbname=dbname
        self.dbfile=dbfile

        dogetkey=0
        md2=None

        if(self.verb): MF.sTimer('keys')

        if(DSs != None):
            self.mdD=DSs
        else:
            self.mdD=DataSets(bdir=self.dsbdir,name=self.dbfile,dtype=self.dbname,
                              verb=self.verb,backup=self.backup,unlink=self.doclean)
            dogetkey=1
        

        if(self.mdD == None):
            print 'WWW mdD not available for : ',self.dsbdir,self.dbname,' try initmdDSs again...'
            self.mdstate=0
            return

        self.stmD=self.mdD.getDataSet('storms')

        if(self.verb): MF.sTimer('keys')
        self.mdstate=1
        if(dogetkey): md2=self.mdD.getDataSet(key=md2key)

        if(md2 == None):

            if(hasattr(self.mdD,'mddtgs')):     self.mddtgs=self.mdD.mddtgs
            else:                               self.mddtgs=[]

            if(hasattr(self.mdD,'mddtgsBT')):   self.mddtgsBT=self.mdD.mddtgsBT
            else:                               self.mddtgsBT=[]

            if(hasattr(self.mdD,'mdstmids')):   self.mdstmids=self.mdD.mdstmids
            else:                               self.mdstmids=[]

            if(hasattr(self.mdD,'mdstmidsCC')): self.mdstmidsCC=self.mdD.mdstmidsCC
            else:                               self.mdstmidsCC=[]

        else:
            self.mddtgs=md2.mddtgs
            self.mddtgsBT=md2.mddtgsBT
            self.mdstmids=md2.mdstmids
            self.mdstmidsCC=md2.mdstmidsCC

        if(self.verb): MF.dTimer('keys')
        self.mdstate=1
        
        return


    def initmdDSsS(self,years,
                   md2key='md2keys',
                   verb=0,
                   ):

        if(verb):
            print 'III(TcData.initmdDSsS): started with years: ',years
            
        from tcbase import TcDataBdir,Md2Dbname

        """ init main objects; if DSs passed in, then get db keys from
        DSs vice DSs.getDataSet(key='md2keys')"""

        dsbdir="%s/DSs"%(TcDataBdir)

        mdDs={}
        stmDs={}
        md2s={}
        
        mddtgs=[]
        mddtgsBT=[]
        mdstmids=[]
        mdstmidsCC=[]
        
        mdD=None
        stmD=None

        for year in years:
            iyear=int(year)
            if(self.doBdeck2):
                dbname="%sBD2-%d"%(Md2Dbname,iyear)
            else:
                dbname="%s-%d"%(Md2Dbname,iyear)
            if(self.doWorkingBT and not(self.doBdeck2)): dbname="%s-W"%(dbname)
            dbfile="%s.pypdb"%(dbname)
            mdDs[year]=DataSets(bdir=dsbdir,name=dbfile,dtype=dbname,verb=self.verb)
            stmDs[year]=mdDs[year].getDataSet('storms')
            md2s[year]=mdDs[year].getDataSet(key=md2key)

            try:
                mddtgs=mddtgs+md2s[year].mddtgs
                mddtgsBT=mddtgsBT+md2s[year].mddtgsBT
                mdstmids=mdstmids+md2s[year].mdstmids
                mdstmidsCC=mdstmidsCC+md2s[year].mdstmidsCC
            except:
                
                print 'WWW -- TcData.initmdDSsS failed to add mddtgs... for year: ',year,' press...'
                print 'WWW -- typically at start of SHEM sesaon 1 JUL...'
                roptMD2=''
                cmd="%s/tcdat/w2-tc-dss-md2.py -y %s -Y"%(w2.W2BaseDirPrc,year)
                print 'III -- need to run md2...cmd: ',cmd,' roptMD2: ',roptMD2
                mf.runcmd(cmd,roptMD2)
                #sys.exit()
                
        
            if(stmD == None):
                stmD=stmDs[year]    

        md2=md2s[year]

        md2.mddtgs=mddtgs
        md2.mddtgsBT=mddtgsBT
        md2.mdstmids=mdstmids
        md2.mdstmidsCC=mdstmidsCC

        self.mdstate=1
        self.mdDs=mdDs
        self.stmD=stmD
        
        self.mddtgs=md2.mddtgs
        self.mddtgsBT=md2.mddtgsBT
        self.mdstmids=md2.mdstmids
        
        self.mdstmidsCC=md2.mdstmidsCC
        
        #s21=self.stmD.stm2idTOstm1id
        #s22=self.stmD.stm2Data
        
        return


    def makeStmListMdeck(self,stmopt,warn=0,dobt=0,cnvSubbasin=0,
                         doSubbasin=1,verb=0):

        if(verb): print 'III(tcCl.TcData.makeStmListMdeck): stmopt: ',stmopt

        self.doSubbasin=doSubbasin
        curdtg=mf.dtg()

        stmids=[]
        tt0=stmopt.split('-')
        tt1=stmopt.split(',')
        tt2=stmopt.split('.')

        if( len(tt0) > 1):
            
            # -- new multiyear storms
            #
            
            if(len(tt2) == 2):
            
                basin=tt2[0]
                yy=tt2[1].split('-')
                y1=int(yy[0])
                y2=int(yy[1])
                mstmopts=[]
                for year in range(y1,y2+1):
                    mstmopt="%s.%02d"%(basin,year)
                    mstmopts.append(mstmopt)

                mstmids=[]
                
                for mstmopt in mstmopts:
                    mstm=self.makeStmListMdeck(mstmopt,dobt=dobt)
                    mstmids=mstmids+mstm
                    
                return(mstmids)

         
            else:
                
                # -- multi-storms, multi-years
                #
    
                mstm=(len(tt0[0]) == 2)
                myr =(len(tt0[-1]) == 2)
                
                if(len(tt2) <= 2 and mstm):
                    
                    s1=tt0[0]
                    sstt=tt0[1].split('.')
    
                    yy=''
                    if(len(sstt) == 2):
                        yy=sstt[-1]
                        s2=sstt[0]
                    else:
                        s2=tt0[1]
    
                    sn1=int(s1)
                    sn2=int(s2[0:-1])
                    b1id=s2[-1]
                    
                    stm1ids=[]
                    sns=range(sn1,sn2+1)
                    for sn in sns:
                        if(yy != ''):
                            stm1id="%02d%1s.%s"%(sn,b1id,yy)
                        else:
                            stm1id="%02d%1s"%(sn,b1id)
                        stm1ids.append(stm1id)
                        
                    for stm1id in stm1ids:
                        stmids=stmids+self.makeStmListMdeck(stm1id,dobt=dobt)
                        
                    return(stmids)

                ostmids=MakeStmList(stmopt,dofilt9x=dobt)
            return(ostmids)
        
        if(len(tt1) > 1):
            for tt in tt1:
                stmids=stmids+self.makeStmListMdeck(tt,dobt=dobt)
            return(stmids)


        do9x=0
        doNN=0
        snum9x=-9
        byear=None

        tsnum=tt2[0]
        b1id=tt2[0][-1]
        
        # 20150504 - bug that crashed w2-plot.py because could not find mdeck
        b1id=b1id.lower()
        b2id=b1idTob2id(b1id)

        # -- year not specified
        #
        if(len(tt2) == 1):
            setcuryear=1
            years=[curdtg[0:4]]
        else:
            setcuryear=0
            years=getyears(tt2[1])
            

        # -- set shem year based on current season
        (shemoverlap,curyear,curyearp1)=CurShemOverlap(curdtg)

        if(Basin1toHemi[b1id.upper()] == 'shem' and len(years) == 1 and shemoverlap and setcuryear ):
            years=[curyearp1]

        # -- interate for 9x
        #
        if(len(tt2[0]) == 3 and tt2[0][0:2].lower() == '9x'):
            try:     yearopt=tt2[1]
            except:  yearopt=curdtg[0:4]
            years=[yearopt]
            if(mf.find(yearopt,'-')):  years=getyears(yearopt)
            for year in years:
                for n in range(90,100):
                    sopt="%2d"%(n)+tt2[0][2]+'.'+yearopt
                    nstmids=self.makeStmListMdeck(sopt,dobt=dobt)
                    for nstmid in nstmids:
                        if(cnvSubbasin): nstmid=self.getSubbasinStmid(nstmid)
                        stmids.append(nstmid)
            return(stmids)

        # - interate for years
        #
        if(len(years) > 1):
            stmids=[]
            for year in years:
                sopt=tt2[0]+'.'+year
                nstmids=self.makeStmListMdeck(sopt,dobt=dobt)
                for nstmid in nstmids:
                    if(cnvSubbasin): nstmid=self.getSubbasinStmid(nstmid)
                    stmids.append(nstmid)
            return(stmids)


        else:
            byear=years[0]

        if(len(byear) <= 2): byear=add2000(byear)

        lenstid=len(tsnum)

        if(lenstid == 3):

            if(tsnum[0:2].lower() == 'cc'):

                b1id=tsnum[2].upper()
                for stm2id in self.mdstmidsCC:
                    (snum,sb1id,syear,sb2id,stm2id,stm1id)=getStmParams(stm2id)

                    if(b1id == sb1id and byear == syear):
                        stm1id=stm2idTostm1id(stm2id)
                        if(cnvSubbasin): stm1id=self.getSubbasinStmid(stm1id)

                        stmids.append(stm1id)

                stmids=MF.uniq(stmids)

                return(stmids)


            else:
                if(tsnum[0:2].isdigit()):
                    if(tsnum[0] == '9'):
                        do9x=1
                        tsnum1=tsnum[1]
                    else:
                        doNN=1
                        tsnum1=tsnum[1]
                        tsnum=tsnum[0:2]

                elif(tsnum[0].isalpha()):
                    # -- mf 20161206 - bug - if set byear above... do not set based on current year
                    #
                    if(len(tt2) == 1):
                        if(byear == None):
                            byear=curdtg[0:4]
                    else:
                        byear=tt2[1]
                        
                    if(len(byear) <= 2): byear=add2000(byear)
                    nstmid="%s.%s"%(tsnum,byear)
                    
                    # - if b1id == 'h' or 'i' then use old method to get stmids
                    #
                    if(b1id == 'i'):
                        b1ids=['a','b']
                    elif(b1id == 'h'):
                        b1ids=['s','p']
                    else:
                        b1ids=[b1id]
                    
                    for b1id in b1ids:
                        nstmid=tsnum[0:2]+b1id+'.'+byear
                        bstmids=MakeStmList(nstmid)
                        for bstmid in bstmids:
                            if(cnvSubbasin): nstmid=self.getSubbasinStmid(bstmid)
                            stmids.append(nstmid)  
                        
                    return(stmids)


        elif(lenstid == 6):
            tsnum=tsnum[2:5]


        if(lenstid == 1): tsnum1=tsnum

        if(lenstid != 1 and lenstid != 3 and lenstid != 6 and not(do9x)): return(stmids)

        # -- find TCC CCNNNB.YYYY
        #
        if(lenstid == 6):
            for stm2id in self.mdstmidsCC:
                (snum,sb1id,syear,sb2id,stm2id,stm1id)=getStmParams(stm2id)

                if(tsnum == snum and b2id == sb2id and byear == syear):
                    stm1id=stm2idTostm1id(stm2id)
                    if(cnvSubbasin): stm1id=self.getSubbasinStmid(stm1id)
                    stmids.append(stm1id)

            stmids=MF.uniq(stmids)
            return(stmids)


        # -- NN/9X
        #
        if(b1id == 'i'):
            b1ids=['a','b']
        elif(b1id == 'h'):
            b1ids=['s','p']
        else:
            b1ids=[b1id]
        
        for stm2id in self.mdstmids:
            
            (snum,sb1id,syear,sb2id,stm2id,stm1id)=getStmParams(stm2id)

            Bstm1id=self.getSubbasinStmid(stm1id)
            
            # -- bypass if dobt and 9x
            #
            isit9x=snum[0].isalpha()
            if(do9x):
                None
            if(dobt and isit9x):
                continue

            # avoid weird snum, e.g., 70e.2013 from nhc (thank you...)
            #
            (snumC,sb1idC,syearC,sb2idC,stm2idC,stm1idC)=getStmParams(stm2id,convert9x=1)
            if(int(snumC) > self.maxNNnum and int(snumC) < 90): continue


            stt=stm2id.split('.')
            stt0=stt[0]
            stt1=stt[1]
            sb2id=stt0[0:2]
            syear=stt1
            if(stt0[2].isalpha()):
                stm1id=stm2idTostm1id(stm2id)
                Bstm1id=self.get9XSubbasinFromStmid(stm1id)
                
            (snumB,sb1idB,syearB,sb2idB,stm2idB,stm1idB)=getStmParams(Bstm1id,convert9x=1)
            
            sb1id=sb1idB.lower()

            test1=(sb1id in b1ids and syear == byear)
            test2=(sb2id == b2id and syear == byear)

            if(doSubbasin):
                btest=test1
            else:
                btest=test2
                
            if(btest):

                sis9x=stt0[2].isalpha()
                sisNN=stt0[2:4].isdigit()
                snum1=snum[1]
                do9xgotit=(sis9x and snum1 == tsnum1)
                doNNgotit=(snum == tsnum)
                if(do9x):
                    if(not(do9xgotit)):  continue
                elif(doNN):
                    if(not(doNNgotit)):  continue

                # -- new logic -- if doSubbasin -- use the converted Bstm1id that goes through getSubbasinStmid
                # 
                if(doSubbasin):
                    stm1id=Bstm1id
                    
                else:
                    stm1id=stm2idTostm1id(stm2id)
                
                    if(cnvSubbasin): 
                        if(sis9x):
                            stm1id=self.get9XSubbasinFromStmid(stm1id)
                        else:
                            stm1id=self.getSubbasinStmid(stm1id)

                stmids.append(stm1id)
        
        stmids=MF.uniq(stmids)
        
        if(warn and len(stmids) == 0):
            print """WWW(tcbase.makeStmListMdeck): no stmids...stmopt: '%s'"""%(stmopt),'years: ',years

        return(stmids)




    def lsStmids(self,year,b2id):

        oNx=[]
        o9x=[]
        for stmid in self.mdstmids:
            syear=int(stmid.split('.')[1])
            sb2id=stmid[0:2]
            snum=stmid[2:4]
            if(sb2id == b2id and syear == year and not(mf.find(stmid,'.bt'))):
                if(snum.isdigit()):
                    oNx.append(stmid)
                else:
                    o9x.append(stmid)

        nN=len(oNx)
        n9=len(o9x)
        nT=nN+n9
        if(n9 == 0): n9=nN
        formrate=(float(nN)/float(n9))*100.0
        card="%3d %3d "%(nN,n9)
        card=card+" %3.0f"%(formrate)
        card=card+' in b2id: %s'%(b2id)
        #print card
        return(card)




    def lsDSsDtgs(self,dtgs,dobt=0,dupchk=0,verb=0,selectNN=1,countsOnly=1,filtTCs=0):

        if(not(type(dtgs) is ListType)): dtgs=[dtgs]
        itrk=None

        dobtLs=dobt
        if(filtTCs): dobtLs=1

        cards=[]
        ncards=0
        nstrms=0
        for dtg in dtgs:

            if(dtg in self.mddtgs):
                if(not(countsOnly)): print 
                (itrk,genstmids)=self.getTCtrkDtg(dtg,dobt=dobtLs,dupchk=dupchk,selectNN=selectNN,verb=verb)
                
                nstrms=len(itrk.keys())
                otrk=itrk
                
                stm1ids=otrk.keys()
                stm1ids.sort()
                stm1ids=sortStmids(stm1ids)
                nstms=len(stm1ids)
                
                if(countsOnly): stm1ids=[]
                
                ncards=0
                for stm1id in stm1ids:
                    trk=otrk[stm1id]
                    gentrk=0
                    
                    fstm1id=self.getFinalStm1idFromRlonTcnames(stm1id,trk.rlon,trk.b1id,verb=verb)
                    if(fstm1id in genstmids): gentrk=1

                    nstmid=self.getSubbasinStmid(fstm1id)
                    if(nstmid == None): nstmid=fstm1id

                    if(len(trk.sname) == 0): trk.sname=GetTCName(nstmid)
                    
                    if(filtTCs and not(IsTc(trk.tccode))):
                        continue

                    card=printTrk(nstmid,dtg,trk.rlat,trk.rlon,trk.vmax,trk.pmin,
                                   trk.dir,trk.spd,trk.dirtype,trk.tdo,
                                   tccode=trk.tccode,wncode=trk.wncode,
                                   r34m=trk.r34m,r50m=trk.r50m,alf=trk.alf,
                                   ntrk=trk.ntrk,ndtgs=trk.ndtgs,
                                   sname=trk.sname,gentrk=gentrk)
                    cards.append(card)
                    ncards=ncards+1
                    
            else:
                nstms=0
                
            if(countsOnly):
                print dtg,'N: ',nstms
                    
            if(ncards == 0 and not(countsOnly)): 
                if(filtTCs): 
                    print "%s-N"%(dtg),'   NNNNNNNNNNNNNN: filtTCs: ',filtTCs,' nstrms All: ',nstrms
                else:
                    print "%s-N -- no storms for this dtg..."%(dtg)    

        return(cards)


    def dupTCtrkDtg(self,itrk,genstmids,verb=0,selectNN=0,maxNNnum=60,killCC=1):
        """ eliminate dups; selectNN=1 tosses 9X; =0 tosses NN
        selectNN=0 is more operational
        """

        otrk={}
        stmids=itrk.keys()
        nstms=len(stmids)

        dups=[]
        if(nstms > 1):
            for i in range(0,nstms-1):
                stm0=stmids[i]
                # -- bypass TCCs
                if(stm0[0:2] == 'CC'): continue
                istrt=i+1
                for j in range(istrt,nstms):
                    stm1=stmids[j]
                    if(stm1[0:2] == 'CC'): continue
                    (lat0,lon0)=(itrk[stm0].rlat,itrk[stm0].rlon)
                    (lat1,lon1)=(itrk[stm1].rlat,itrk[stm1].rlon)
                    gdist=gc_dist(lat0,lon0,lat1,lon1)
                    if(gdist <= self.distmin and (i != j) ):
                        dups.append((i,j))
                        if(verb): print 'dupTCtrkDtg ',i,j,'stm0: ',stm0,lat0,lon0,' stm1: ',stm1,lat1,lon1,gdist

        # dddd -- select which storm should be tossed
        #

        if(len(dups) > 0):
            ikills=[]
            for dup in dups:
                (i,j)=dup
                stmi=stmids[i]
                stmj=stmids[j]

                nstmi=int(stmi[0:2])
                nstmj=int(stmj[0:2])

                # -- select 9X over NN, if selectNN=0; 
                #
                ikill=i

                if(selectNN):

                    if(nstmi >= 90 and nstmj < self.maxNNnum): ikill=i
                    if(nstmj >= 90 and nstmi < self.maxNNnum): ikill=j

                else:

                    if(nstmj >= 90 and nstmi < self.maxNNnum): ikill=i
                    if(nstmi >= 90 and nstmj < self.maxNNnum): ikill=j


                # -- case of NN > maxNNnum and < 90 -- test storms

                if(nstmi >= 90 and nstmj > self.maxNNnum): ikill=j
                if(nstmj >= 90 and nstmi > self.maxNNnum): ikill=i

                if(nstmi < self.maxNNnum and nstmj < self.maxNNnum): ikill=-1

                ikills.append(ikill)

                if(verb): print 'iii: %2d nstmi: %2d jjj: %2d nstmj: %2d ikill: %2d'%(i,nstmi,j,nstmj,ikill)

            for i in range(0,nstms):
                iskip=0
                for ikill in ikills:
                    if(ikill != -1 and i == ikill):
                        iskip=1

                if(not(iskip)):
                    stmi=stmids[i]
                    otrk[stmi]=itrk[stmi]

        else:
            otrk=itrk


        if(verb):
            print 'BBB dupTCtrkDtg:',itrk.keys()
            print 'AAA dupTCtrkDtg:',otrk.keys()

        # -- throw away CC
        #
        if(killCC):

            ftrk={}
            for stmid in otrk.keys():
                if(stmid[0:2] != 'CC'):
                    ftrk[stmid]=otrk[stmid]

            otrk=ftrk


        return(otrk)






    def merge9xDSsStm(self,dds,dds9x,doprint=0,set9xfirst=0):
        """
        set9xfirst=1 :: look for 9x posits to show in the mdeck
        otrks = object trks
        trks  = trk dict

        """
        cards=[]
        trks={}
        otrks={}

        (trk,dtgs)=dds.getMDtrk()
        (otrk,odtgs)=dds.getMDotrk()

        trk9x={}
        dtgs9x=[]

        stmid=dds.stm1id

        (snum,sb1id,syear,sb2id,stm2id,stm1id)=getStmParams(stmid)

        stmid9x='xx'+sb1id+'.'+syear

        if(dds9x != None):
            (trk9x,dtgs9x)=dds9x.getMDtrk()
            (otrk9x,odtgs9x)=dds9x.getMDotrk()
            stmid9x=dds9x.stm1id


        dtgs=dtgs+dtgs9x
        dtgs=mf.uniq(dtgs)

        for dtg in dtgs:

            if(set9xfirst):

                try:
                    ttrk9x=trk9x[dtg]
                except:
                    ttrk9x=None
                
                try:
                    ttrk=trk[dtg]
                except:
                    ttrk=None
                    
                if(ttrk9x != None and ttrk == None):
                    trks[dtg]=ttrk9x
                    otrks[dtg]=otrk9x[dtg]
                    ostmid=stmid9x
                    
                elif(ttrk9x != None and ttrk != None):
                    wn9x=ttrk9x[7]
                    wnNN=ttrk[7]
                    if(wnNN == 'WN'):
                        trks[dtg]=ttrk
                        otrks[dtg]=otrk[dtg]
                        ostmid=stmid
                    else:
                        trks[dtg]=ttrk9x
                        otrks[dtg]=otrk9x[dtg]
                        ostmid=stmid9x
                else:
                    
                    trks[dtg]=ttrk
                    otrks[dtg]=otrk[dtg]
                    ostmid=stmid
                    
                    

            else:
                try:
                    trks[dtg]=trk[dtg]
                    otrks[dtg]=otrk[dtg]
                    ostmid=stmid
                except:
                    try:
                        trks[dtg]=trk9x[dtg]
                        otrks[dtg]=otrk9x[dtg]
                        ostmid=stmid9x
                    except:
                        None

            otrks[dtg].ostmid=ostmid

            if(doprint):

                (rlat,rlon,vmax,pmin,dir,spd,tccode,wncode,trkdir,trkspd,dirtype,b1id,tdo,
                 ntrk,ndtgs,r34m,r50m,alf,sname,
                 r34,r50,depth,
                 )=trks[dtg]

                card=printTrk(ostmid,dtg,rlat,rlon,vmax,pmin,dir,spd,dirtype,
                              tdo=tdo,tccode=tccode,wncode=wncode,
                              ntrk=ntrk,ndtgs=ndtgs,r34m=r34m,r50m=r50m,
                              alf=alf,sname=sname)
                cards.append(card)

        odds=dds

        # -- decorate o(bject)dds
        #
        odtgs=otrks.keys()
        odtgs.sort()

        odds.trk=otrks
        odds.dtgs=odtgs
        odds.stmid9x=stmid9x
        
        odds.cards=cards

        return(odds)




    def lsDSsStm(self,stmid,dobt=0,
                 set9xfirst=0,
                 convert9x=0,
                 sumonly=0,
                 printdtgs=0,
                 doprint=0,
                 doprintSum=1,
                 verb=0,
                 filtTCs=0):

        dobtLs=dobt
        if(filtTCs): dobtLs=dobt
        
        dds=self.getDSsFullStm(stmid,dobt=dobtLs,doprint=doprint,
                               set9xfirst=set9xfirst)
        
        ocard=None
        ocards=None
        if(verb == 2):
            kk=dds.trk.keys()
            kk.sort()
            for k in kk:
                print 'kkkkkkkkkkkkkkk',k
                dds.trk[k].ls()

        # -- ls the storms for these dtgs happens here !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #
        if(not(sumonly)):
            if(dds != None): ocards=dds.lsMDtrk(filtTCs=filtTCs)

        if(printdtgs):
            self.lsDSsDtgs(dds.dtgs,dobt=0,dupchk=0,filtTcs=filtTCs)
            
        try:
            # -- check if only want to output 9X
            #
            if(dobtLs == -1):
                if(Is9X(stmid)):
                    convert9x=1
                    ocard=self.lsDSsStmSummary(dds,stmid,convert9x=convert9x,doprint=doprintSum)
            else:
                ocard=self.lsDSsStmSummary(dds,stmid,convert9x=convert9x,doprint=doprintSum)

        except:
            print '!!!'
            print 'WWW-- something from with storm.table? in lsDSsStm.lsDSsStmSummary for stmid: ',stmid,'dobtLs: ',dobtLs,'dds: ',dds
            print '!!!'

        return(ocard,ocards)
    
    
    def getDSsStmCards(self,stmid,dobt=0,
                       set9xfirst=0,
                       convert9x=0,
                       verb=0):
        
        dds=self.getDSsFullStm(stmid,dobt=dobt,
                               set9xfirst=set9xfirst)

        if(dds != None): ocards=dds.lsMDtrk(doprint=0)
        
        try:
            # -- check if only want to output 9X
            #
            if(dobt == -1):
                if(Is9X(stmid)):
                    convert9x=1
                    ocard=self.lsDSsStmSummary(dds,stmid,convert9x=convert9x,doprint=0)
            else:
                ocard=self.lsDSsStmSummary(dds,stmid,convert9x=convert9x,doprint=0)

            ocardsum=ocard

        except:
            print '!!!'
            print 'WWW-- something from with storm.table? in getDSsStmCards for stmid: ',stmid,'dobt: ',dobt,'dds: ',dds
            print '!!!'
            ocards['sum']=None

        return(ocards,ocardsum)
    

    def lsDSsStmCards(self,stmid,dobt=0,doprint=0,sumonly=0,
                      set9xfirst=0,
                      printdtgs=1,
                      convert9x=1,
                      warn=0,
                      verb=0):

        dds=self.getDSsFullStm(stmid,dobt=dobt,doprint=doprint,
                               set9xfirst=set9xfirst)
        ocards={}
        if(dds == None):
            return(ocards)

        if(verb == 2):
            kk=dds.trk.keys()
            for k in kk:
                dds.trk[k].ls()

        # -- ls the storms for these dtgs happens here !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #
        if(sumonly):
            ocards={}
        else:
            ocards=dds.lsMDtrk(doprint=0)
            
            
        try:
            # -- check if only want to output 9X
            #
            if(dobt == -1):
                if(Is9X(stmid)):
                    ocard=self.lsDSsStmSummary(dds,stmid,doprint=0,convert9x=convert9x)
            else:
                ocard=self.lsDSsStmSummary(dds,stmid,doprint=0,convert9x=convert9x)
            
            ocards['summary']=ocard

        except:
            if(warn):
                print '!!!'
                print 'WWW-- something from with storm.table? in lsDSsStmCards.lsDSsStmSummary for stmid: ',stmid,' dobt: ',dobt
                print '!!!'

        return(ocards)



    def lsDSsStmSummary(self,dds,stmid,convert9x=1,cnvSubbasin=1,
                        lsCC=1,doprint=1,warn=0):

        # -- season storm card
        #
        
        rc=self.stmD.getStmData(stmid)
        if(rc != None):  sname=rc[0]
        else:            sname=dds.sname

        if(Is9X(stmid)): sname='---------'

        if(hasattr(dds,'ace')):

            curdtg=mf.dtg()
            curdtgm6=mf.dtginc(curdtg,-6)

            if(len(dds.dtgs) == 0):
                if(warn): print 'DDDDDDDDDDDDDDDDDd nada dtgs for stmid: ',stmid
                return

            bdtg=dds.dtgs[0]
            edtg=dds.dtgs[-1]
            
            # -- force convertion of 9x to standard form
            #
            if(Is9X(stmid) and self.doSubbasin != 1):
                ostmid=self.get9XSubbasinFromStmid(stmid)
                stmid=ostmid
                
            # -- check if subbasin already done...
            #
            if(cnvSubbasin and self.doSubbasin != 1):
                ostmid=self.getSubbasinStmid(stmid)
            else:
                ostmid=stmid
                
                
            (snum,b1id,yyyy,b2id,stm2id,stm1id)=getStmParams(ostmid)

            stm=snum+b1id

            livestatus=' '
            tctype=TCType(dds.vmax)
            edtgdiff=mf.dtgdiff(edtg,curdtg)
            if(edtg == curdtg or edtg == curdtgm6 or edtgdiff <= 0.0): livestatus='*'
            RIstatus='    '
            timeGen='      '
            if(dds.nRI > 0): RIstatus='rrRI'
            if(dds.nED > 0): RIstatus='rrED'
            if(dds.nRW > 0):
                RIstatus='ddRW'
                if(dds.nRI > 0): RIstatus='ddRI'
                if(dds.nED > 0): RIstatus='ddED'

            stm9x=''
            
            if(hasattr(dds,'stmidNN') and Is9X(stmid)):
                stmidNN=dds.stmidNN
                if(cnvSubbasin):
                    stmidNN=self.getSubbasinStmid(stmidNN)
                stm9x=stm9x+"NN: %s"%(stmidNN)

            if(hasattr(dds,'stmid9x') and not(Is9X(stmid))):
                ostmid9x=dds.stmid9x
                if(convert9x):
                    ostmid9x=get9XstmidFromNewForm(ostmid9x)
                    
                if(cnvSubbasin): 
                    ostmid9x=self.get9XSubbasinFromStmid(ostmid9x)
                    
                pad=''
                if(len(stm9x) > 0): pad=' '
                stm9x=stm9x+pad+"9X: %s"%(ostmid9x.split('.')[0])

            if(hasattr(dds,'stmidCC') and lsCC):
                pad=''
                if(len(stm9x) > 0): pad=' '
                stm9x=stm9x+pad+"CC: %s"%(dds.stmidCC)

            if(hasattr(dds,'time2gen') and not(Is9X(stmid))):
                if(dds.time2gen >= 0.0):
                    timeGen="tG:%3.0f"%(dds.time2gen)
                    
            oACE=dds.ace
            if(Is9X(stmid)): oACE=0.0


            ovmax="%3d"%(dds.vmax)
            if(dds.vmax == dds.undef): ovmax='***'

            if(mf.find(stmid,'CC')):
                tctype='___'

                ocard="%s %s%1s %3s %-10s :%s :%4.1f;%4.1f :%5.1f %5.1f :%s<->%s :%5.1f<->%-5.1f :%5.1f<->%-5.1f :%s"%\
                    (yyyy,stm,livestatus,tctype,sname[0:9],ovmax,dds.tclife,dds.stmlife,dds.latb,dds.lonb,bdtg,edtg,
                     dds.latmn,dds.latmx,dds.lonmn,dds.lonmx,
                     stm9x)
            else:

                try:
                    n=int(stm[0:2])
                    ogendtg=" 1st: %s"%(dds.gendtg[4:])
                except:
                    ogendtg=''

                ocard="%s %s%1s %3s %-10s :%s :%5.1f %5.1f :%5.1f %5.1f : %s<->%s :%5.1f<->%-5.1f :%5.1f<->%-5.1f :%4.1f :%4.1f :%2d:%2d:%2d:%s :%s %s %s"%\
                    (yyyy,stm,livestatus,tctype,sname[0:9],ovmax,dds.tclife,dds.stmlife,dds.latb,dds.lonb,bdtg[4:],edtg[4:],
                     dds.latmn,dds.latmx,dds.lonmn,dds.lonmx,
                     dds.stcd,oACE,
                     dds.nRI,dds.nED,dds.nRW,
                     RIstatus,timeGen,stm9x,ogendtg)

                
            if(doprint): 
                print ocard
            return(ocard)



    def anlDSsStmSummary(self,stmids,dobt=0,set9xfirst=0,doprint=0,anltype='time2gen'):

        for stmid in stmids:

            dds=self.getDSsFullStm(stmid,dobt=dobt,doprint=doprint,
                                   set9xfirst=set9xfirst)
            # -- season storm card
            #
            #rc=self.stmD.getStmData(stmid)
            #if(rc != None):  sname=rc[0]
            #else:            sname=dds.sname
            if(anltype == 'time2gen' and hasattr(dds,'time2gen')):
                #self.stats.append(dds.time2gen/24.0)
                self.stats.append(dds.time2gen)
            elif(anltype == 'tclife' and hasattr(dds,'tclife')):
                self.stats.append(dds.tclife)
            elif(anltype == 'stmlife' and hasattr(dds,'stmlife')):
                self.stats.append(dds.stmlife*24)
            else:
                stmlifeMin=0.5
                if(hasattr(dds,'stmlife') and dds.stmlife >= stmlifeMin):
                    self.stats.append(dds.stmlife)


    def anlDSsStmRI(self,stmids,dobt=1,set9xfirst=0,doprint=0,verb=0):

        def isSouthChinaSea(lat,lon):
            rc=0
            if(lat >= 0.0 and lat <= 22.5 and lon >= 105.0 and lon <= 122.0): rc=1
            return(rc)


        def getRI(trk,dtgs,dvmaxRI=30,dvmaxED=50,dvmaxRD=-30,verb=verb):

            def getRIperiods(RI,ddtg=6.0):

                RIs={}

                dtgs=RI.keys()
                dtgs.sort()

                ndtgs=len(dtgs)

                if(ndtgs == 1):
                    RR=RI[dtgs[0]]
                    isSCSRI=isSouthChinaSea(RR[1],RR[2])
                    RIs[dtgs[0]]=(RR,isSCSRI)

                else:

                    nRIs=1
                    RImax=-999

                    for n in range(1,ndtgs):
                        dtg0=dtgs[n]
                        dtgm1=dtgs[n-1]

                        if(RI[dtgm1] > RImax):
                            RImax=RI[dtgm1]
                            RIdtg=dtgm1


                        dtgdiffRI=mf.dtgdiff(dtgm1,dtg0)
                        if(dtgdiffRI != ddtg or n == ndtgs-1):

                            isSCSRI=isSouthChinaSea(RImax[1],RImax[2])
                            RIs[RIdtg]=(RImax,isSCSRI)

                            nRIs=nRIs+1
                            RImax=-999

                        if(RI[dtg0] > RImax):
                            RImax=RI[dtg0]
                            RIdtg=dtg0


                        if(verb): print 'RRII periods: ',dtgm1,dtg0,mf.dtgdiff(dtgm1,dtg0),RImax,RIdtg,'nRIs: ',nRIs


                return(RIs)

            #MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
            # main


            nRI=0
            nED=0
            nRW=0

            RI={}
            ED={}
            RW={}

            isSCS=0

            for dtg in dtgs:
                dtgm24=mf.dtginc(dtg,-24)
                if(dtgm24 in dtgs):
                    ttm24=trk[dtgm24]
                    tt=trk[dtg]
                    vmaxm24=ttm24.vmax
                    vmax=tt.vmax

                    if(vmax >= vmaxTS and isSouthChinaSea(tt.rlat,tt.rlon)): isSCS=1

                    if(vmax != None):
                        dvmax=vmax-vmaxm24
                    else:
                        continue

                    if(dvmax >= dvmaxRI):
                        nRI=nRI+1
                        RI[dtg]=(dvmax,tt.rlat,tt.rlon,ttm24.vmax,tt.vmax)

                    if(dvmax >= dvmaxED):
                        nED=nED+1
                        ED[dtg]=(dvmax,tt.rlat,tt.rlon,ttm24.vmax,tt.vmax)

                    if(dvmax <= dvmaxRD):
                        nRW=nRW+1
                        RW[dtg]=(dvmax,tt.rlat,tt.rlon,ttm24.vmax,tt.vmax)


            ridtgs=RI.keys()
            ridtgs.sort()

            if(verb):
                for ridtg in ridtgs:
                    print 'RRII ',ridtg,RI[ridtg]

            eddtgs=ED.keys()
            eddtgs.sort()

            if(verb):
                for eddtg in eddtgs:
                    print 'EEDD ',eddtg,ED[eddtg]

            rwdtgs=RW.keys()
            rwdtgs.sort()

            if(verb):
                for rwdtg in rwdtgs:
                    print 'RRWW ',rwdtg,RW[rwdtg]

            RIs=getRIperiods(RI)

            if(verb):
                dtgs=RIs.keys()
                dtgs.sort()

                for dtg in dtgs:
                    print 'RIperiod #',(dtgs.index(dtg)+1),' dtg: ',dtg,'RI ',RIs[dtg]

                print 'isSCS: ',isSCS


            return(RIs,isSCS)


        ocards=[]

        for stmid in stmids:

            dds=self.getDSsFullStm(stmid,dobt=dobt,doprint=doprint,
                                   set9xfirst=set9xfirst)

            (trk,dtgs)=dds.getMDotrk()

            (RIs,isSCS)=getRI(trk,dtgs)

            dtgs=RIs.keys()
            dtgs.sort()

            isSCSRIall=0
            isRIall=0

            if(len(dtgs) > 0): isRIall=1

            card=''
            for dtg in dtgs:
                nRI=dtgs.index(dtg)+1
                RI=RIs[dtg]
                lat=RI[0][1]
                lon=RI[0][2]
                dvmax=RI[0][0]
                bvmax=RI[0][3]
                isSCSRI=RI[1]

                if(isSCSRI): isSCSRIall=1
                card="%s RI#: %d  %s lat/lon: %5.1f %6.1f dvmax: %3d vmaxB: %3d isSCSRI: %d"%(card,nRI,dtg,lat,lon,dvmax,bvmax,isSCSRI)

            ocard='%s %-12s isRI: %d isSCS: %d isSCSRI: %d  %s'%(stmid,GetTCName(stmid),isRIall,isSCS,isSCSRIall,card)
            print ocard
            ocards.append(ocard)

        return(ocards)



    def filtStmSummaryBySeason(self,stmids,dobt=0,tlist=None,verb=0):

        statAll=[]
        statIn=[]
        statOut=[]


        def appendStat(stat,dpeak,dpeakB,dpeakA):

            statAll.append(stat)
            if(dpeak >= dpeakB or (dpeak <= 0.0 and dpeak <= dpeakA)):
                statOut.append(stat)
            else:
                statIn.append(stat)


        for stmid in stmids:

            if(Is9X(stmid)): continue
            dds=self.getDSsFullStm(stmid,dobt=dobt)
            if(dds == None): continue

            # -- season storm card
            #
            #rc=self.stmD.getStmData(stmid)
            #if(rc != None):  sname=rc[0]
            #else:            sname=dds.sname

        ## ace                         : 4.25591715976
        ## btdtgs                      : ['2007033018', '2007033100', '2007033106', '2007033112', '2007033118', '2007040100', '2007040106', '2007040112', '20 ... 
        ## curdtghms                   : ['20110406 20:10:09', '20110406 20:10:09']
        ## dED                         : -999
        ## dRI                         : 30
        ## dRW                         : -40
        ## dtgs                        : ['2007032912', '2007033012', '2007033018', '2007033100', '2007033106', '2007033112', '2007033118', '2007040100', '20 ... 
        ## gendtg                      : 2007033112
        ## gendtgs                     : ['2007033018', '2007033100', '2007033106', '2007033112', '2007033118', '2007040100']
        ## genstdd                     : 1.3
        ## latb                        : 11.1268292683
        ## latmn                       : 3.1
        ## latmx                       : 26.1
        ## lonb                        : 154.846341463
        ## lonmn                       : 144.1
        ## lonmx                       : 170.1
        ## nED                         : 0
        ## nRI                         : 1
        ## nRW                         : 5
        ## ndtgs                       : 27
        ## sname                       : KONG-REY
        ## stcd                        : 4.45673076923
        ## stclife                     : 0.0
        ## stm1id                      : 01W.2007
        ## stm2id                      : wp01.2007
        ## stmid9x                     : b2W.2007
        ## stmidCC                     : CC047W.2007
        ## stmlife                     : 10.0
        ## tclife                      : 4.5
        ## time2gen                    : 114.0

            
            #dds.ls()
            dtgb=dds.dtgs[len(dds.dtgs)/2]

            dtgpeak=dtgb[0:4]+'090100'
            dpeak=mf.dtgdiff(dtgb,dtgpeak)
            dpeak=dpeak/24.0
            dpeakB=120.0
            dpeakA=-75.0
            
            time2gen=dds.time2gen/24.0
            stmlife=dds.stmlife/24.0

            if(verb == 0):
                print 'dtgb: ',stmid,dtgb,dds.latb,dds.lonb,dds.stmlife,'time2gen: %3.0f'%(dds.time2gen),'dpeak: %3.0f'%(dpeak)

            if(tlist == 'latb'):
                appendStat(dds.latb,dpeak,dpeakB,dpeakA)
            elif(tlist == 'latmn'):
                appendStat(dds.latmn,dpeak,dpeakB,dpeakA)
            elif(tlist == 'stmlife'):
                appendStat(stmlife,dpeak,dpeakB,dpeakA)
            elif(tlist == 'time2gen'):
                appendStat(time2gen,dpeak,dpeakB,dpeakA)
            else:
                print 'EEEinvalid tlist option: ',tlist,' in tcbase.filtStmSummaryBySeason'
                sys.exit()

            
        return(statAll,statIn,statOut)



    def filtStmSummaryByDev(self,stmids,dobt=0,tlist=None,verb=0):

        statAll=[]
        statDev=[]
        statNonDev=[]


        def appendStat(stat,devflg):

            if(devflg == -1): return

            # -- if stat = 0.0 then only one dtg so make 0.25 d
            #
            if(stat == 0.0): stat=0.25

            statAll.append(stat)
            if(devflg):
                statDev.append(stat)
            else:
                statNonDev.append(stat)


        for stmid in stmids:

            dds=self.getDSsFullStm(stmid,dobt=dobt)
            #dds.ls('stm')

            devflg=-1
            if(Is9X(dds.stm1id)):
                if(hasattr(dds,'stmidNN')):
                    devflg=1
                else:
                    devflg=0

            #print 'SSSSSSSSSSSS ',stmid,devflg

            if(tlist == 'latb'):    appendStat(dds.latb,devflg)
            if(tlist == 'latmn'):    appendStat(dds.latmn,devflg)
            if(tlist == 'stmlife'):    appendStat(dds.stmlife,devflg)

        return(statAll,statDev,statNonDev)


    def filtStmSummaryByCC(self,stmids,dobt=0,tlist=None,
                           cctest='all',
                           verb=0):

        statAll=[]
        statDev=[]
        statNonDev=[]


        def appendStat(stat,ccflg):

            if(ccflg == -1): return
            statAll.append(stat)
            if(ccflg):
                statDev.append(stat)
            else:
                statNonDev.append(stat)


        for stmid in stmids:

            dds=self.getDSsFullStm(stmid,dobt=dobt)
            dds.ls('stm')

            ccflg=-1

            if(cctest == 'all'):
                stmtest=1
            elif(cctest == 'bt'):
                stmtest=IsNN(dds.stm1id)
            elif(cctest == '9x'):
                stmtest=Is9X(dds.stm1id)

            if(stmtest):
                if(hasattr(dds,'stmidCC')):
                    ccflg=1
                else:
                    ccflg=0


            if(tlist == 'latb'):    appendStat(dds.latb,ccflg)
            if(tlist == 'latmn'):    appendStat(dds.latmn,ccflg)
            if(tlist == 'stmlife'):    appendStat(dds.stmlife,ccflg)

        return(statAll,statDev,statNonDev)

    def filtStmSummaryByDev(self,stmids,dobt=0,tlist=None,verb=0):

        statAll=[]
        statDev=[]
        statNonDev=[]


        def appendStat(stat,devflg):

            if(devflg == -1): return
            statAll.append(stat)
            if(devflg):
                statDev.append(stat)
            else:
                statNonDev.append(stat)


        for stmid in stmids:

            (ocard,ocards)=self.lsDSsStm(stmid,dobt=dobt,sumonly=1,doprintSum=0)
            (ocardBT,ocardsBT)=self.lsDSsStm(stmid,dobt=1,sumonly=1,doprintSum=0)

            dds=self.getDSsFullStm(stmid,dobt=dobt)
            if(dds == None):
                print 'III no dds in filtStmSummaryByDev for stmid: ',stmid
                continue
            devflg=-1
            if(IsNN(dds.stm1id)):
                if(hasattr(dds,'stmid9x')):
                    devflg=1
                else:
                    devflg=0
            elif(Is9X(dds.stm1id)):
                devflg=0
                    
            stmlife=dds.stmlife
            
            if(tlist == 'latb'):    appendStat(dds.latb,devflg)
            if(tlist == 'latmn'):    appendStat(dds.latmn,devflg)
            if(tlist == 'stmlife'):    appendStat(stmlife,devflg)
            if(tlist == '9xlife'):
                if(devflg == 1 and hasattr(dds,'time2gen')):
                    t2gen=dds.time2gen/24.0
                    appendStat(t2gen,devflg)
                else:
                    appendStat(stmlife,devflg)

        return(statAll,statDev,statNonDev)


    def get9XDevNondevStmids(self,stmids,dobt=0,
                             devtype='all',
                             verb=0):

        stmidAll=[]
        stmidDev=[]
        stmidNonDev=[]

        def appendStmid(stmid,devflg):

            if(devflg == -1): return
            stmidAll.append(stmid)
            if(devflg):
                stmidDev.append(stmid)
            else:
                stmidNonDev.append(stmid)


        for stmid in stmids:

            dds=self.getDSsFullStm(stmid,dobt=dobt)
            dds.ls('stm')

            devflg=-1

            if(devtype == 'all'):
                stmtest=1
            elif(devtype == 'bt'):
                stmtest=IsNN(dds.stm1id)
            elif(devtype == '9x'):
                stmtest=Is9X(dds.stm1id)

            if(stmtest):
                if(hasattr(dds,'stmidNN')):
                    devflg=1
                else:
                    devflg=0

            appendStmid(stmid,devflg)

        return(stmidAll,stmidDev,stmidNonDev)


    def Carq2Ngtrp(self,dtg,verb=1):

        curdtg=mf.dtg()
        # -- use tcV object as with tmtrkN
        #
        tcV=self.getTCvDtg(dtg,dobt=0,dupchk=1)


        stmids=tcV.stmids
        stmids=sortStmids(stmids)

        ntc=len(stmids)

        ocards=[]

        #10  02071512     at 20020715  902841
        #05  11061012     at 20110613  902841
        card="%02d %8s     at %s  902841"%(ntc,dtg[2:],curdtg[0:8])
        ocards.append(card)

        for stmid in stmids:
            tt=tcV.trk[stmid]
            (clat,clon)=Rlatlon2Clatlon(tt.rlat,tt.rlon,dozero=1)

            snum=stmid[0:2]
            b1id=stmid[2]
            if(tt.b1id != None): b1id=tt.b1id

            r34bar='-999'
            r50bar='-999'
            if(tt.r34m != None): r34bar="%04.0f"%(tt.r34m)
            if(tt.r50m != None): r50bar="%04.0f"%(tt.r50m)
            curdir="%04.0f"%(tt.dir*10)
            curspd="%03.0f"%(tt.spd*10)

            #        137N 1359E 075 32 W  060 140  2954 140      second & subsequent
            #         A    B     C  D  E  F    G    H    I

            card="%s %s %03d %s %s %s %s %s %s"%(clat,clon,tt.vmax,snum,b1id,
                                                 r34bar,r50bar,curdir,curspd)

            ocards.append(card)

        return(ocards)

    # mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm from MD.py
    #
    def getTC2idsFromDtg(self,dtg,dofilt9x=0):

        try:
            stms=self.stm2dtg[dtg]
        except:
            stms=None

        ostms={}

        if(stms != None):
            stm2ids=stms.keys()
            stm2ids.sort()

            for stm2id in stm2ids:

                tc=stms[stm2id]
                snum=int(stm2id[2:4])

                if(dofilt9x and (snum >= 90 and snum <= 99) ): continue

                lat=tc[0]
                lon=tc[1]
                vmax=tc[2]

                ostms[stm2id]=(lat,lon,vmax)

        return(ostms)


    def rlatLon2clatLon(self,lat,lon):

        rlat0=float(lat)
        ihemns='N'

        if(rlat0<0.0):
            ihemns='S'
            rlat=rlat0*(-1.0)
        else:
            rlat=rlat0

        rlat=rlat*10

        clat="%03.0f%s"%(rlat,ihemns)

        rlon0=float(lon)
        ihemew='E'

        if(rlon0>180.0):
            ihemew='W'
            rlon=360.0-rlon0
        elif(rlon0<=0.0):
            ihemew='E'
            rlon=360.0+rlon0
        else:
            rlon=rlon0

        if(rlon < 0.0):
            ihemew='E'
            rlon=abs(rlon)

        rlon=rlon*10

        clon="%04.0f%s"%(rlon,ihemew)

        return(clat,clon)




class TrkDataDtg(Trkdata,TcData):

    undef=undef

    def __init__(self,dtg,trk,genstmids,stmD):

        kk=trk.keys()
        self.stmids=sortStmids(kk)
        self.genstmids=genstmids
        self.trk=trk
        self.dtg=dtg
        self.stmD=stmD


    def getTCv(self,stmid):

        posit=None
        if(stmid in self.stmids):
            posit=self.trk[stmid].getposit()
            #posit=self.trk[stmid].gettrk()

        return(posit)

    def lsStms(self):

        print 'DTG: ',self.dtg
        for stmid in self.stmids:
            card=stmid
            if(stmid in self.genstmids):
                card=card+" <--- genesis"
            print card


    def makeTCbogCard(self,stmid,verb=1):


        trk=self.trk[stmid]
        fstm1id=self.getFinalStm1idFromRlonTcnames(stmid,trk.rlon,trk.b1id,verb=verb)

        nstmid=self.getSubbasinStmid(fstm1id)
        if(nstmid == None): nstmid=fstm1id

        stm3id=nstmid.split('.')[0]

        rlat0=trk.rlat
        rlon0=trk.rlon
        vmax=trk.vmax
        rdir=trk.dir
        rspd=trk.spd
        pmin=trk.pmin
        r34=trk.r34m
        r50=trk.r50m

        if(r50 == None): r50=-999.
        if(r34 == None): r34=-999.
        if(pmin == None): pmin=-999.

        # use rhumb line to find u/v motion for tcgob
        #
        dt=-12
        (rlat1,rlon1)=rumltlg(rdir,rspd,dt,rlat0,rlon0)
        dt=12
        (rcourse,rspeed,umotion,vmotion)=rumhdsp(rlat1,rlon1,rlat0,rlon0,dt)


        tcbogcard="%s %s %3i %4i%6.1f%6.1f%5i%5i %5.1f %5.2f%7.2f%7.2f"%\
            (self.dtg,stm3id,
             int(vmax),int(pmin),
             rlat0,rlon0,
             int(r50),int(r34),
             rdir,rspd,
             umotion,vmotion)


        if(verb): print tcbogcard

        return(tcbogcard)

    def makeTCbogCards(self,override=0,writefile=0,verb=0,tcbogPath='/tmp/tcbog.txt'):

        cards=''
        for stmid in self.stmids:
            cards=cards+self.makeTCbogCard(stmid)+'\n'

        rc=MF.WriteString2File(cards,tcbogPath,verb=verb)
        return(cards)




    def makeTCvCard(self,stmid,verb=0):


        trk=self.trk[stmid]
        fstm1id=self.getFinalStm1idFromRlonTcnames(stmid,trk.rlon,trk.b1id,verb=verb)

        nstmid=self.getSubbasinStmid(fstm1id)
        if(nstmid == None): nstmid=fstm1id

        stm3id=nstmid.split('.')[0]

        (clat,clon)=Rlatlon2Clatlon(trk.rlat,trk.rlon,dozero=1)

        carqvmax=trk.vmax*knots2ms
        if(carqvmax > 0.0):
            vitvmax="%02d"%(mf.nint(carqvmax))
        else:
            carqvmax=-9
            vitvmax="%02d"%(carqvmax)


        if(trk.poci != None):
            carqpoci=trk.poci
            vitpoci="%04d"%(mf.nint(carqpoci))
        else:
            carqpoci=-999.
            vitpoci="%04d"%(carqpoci)


        if(trk.roci != None):
            carqroci=trk.roci*nm2km
            vitroci="%04d"%(mf.nint(carqroci))
        else:
            carqroci=-999
            vitroci="%04d"%(carqroci)

        if(trk.rmax != None):
            carqrmax=trk.rmax*nm2km
            vitrmax="%03d"%(mf.nint(carqrmax))
        else:
            carqrmax=-99
            vitrmax="%03d"%(carqrmax)


        tcdepth=trk.depth
        if(not(trk.depth == 'S' or trk.depth == 'M' or trk.depth == 'D')): tcdepth='X'

        # -- one posit for c7w.07
        #
        if(trk.dir == self.undef):
            vitdir='-99'
        else:
            vitdir="%03.0f"%(trk.dir)

        if(trk.spd == self.undef):
            vitspd='-99'
        else:
            vitspd="%03.0f"%(trk.spd*10.0*knots2ms)


        if(trk.pmin != None):
            vitpmin="%04d"%int(trk.pmin)
        else:
            pmin=-999
            vitpmin="%04d"%int(pmin)


        if(trk.r34 == None):
            carqr34ne=carqr34se=carqr34sw=carqr34nw=-999.
        else:
            carqr34ne=trk.r34[0]*nm2km
            carqr34se=trk.r34[1]*nm2km
            carqr34sw=trk.r34[2]*nm2km
            carqr34nw=trk.r34[3]*nm2km

        if(carqr34ne > 0.0):
            vitr34ne="%04.0f"%(carqr34ne)
        else:
            r34ne=-999.
            vitr34ne="%04.0f"%(r34ne)

        if(carqr34se > 0.0):
            vitr34se="%04.0f"%(carqr34se)
        else:
            r34se=-999.
            vitr34se="%04.0f"%(r34se)

        if(carqr34sw > 0.0):
            vitr34sw="%04.0f"%(carqr34sw)
        else:
            r34sw=-999.
            vitr34sw="%04.0f"%(r34sw)

        if(carqr34nw > 0.0):
            vitr34nw="%04.0f"%(carqr34nw)
        else:
            r34nw=-999.
            vitr34nw="%04.0f"%(r34nw)

        vitdepth=tcdepth

        # MFTC 97S UNKNOWN   20100415 1200 083S 1017E 130 007 1010 -999 -999 08 -99 -999 -999 -999 -999 X

        if(trk.sname != ''):
            sname=trk.sname
        else:
            # -- try names.py
            #
            sname=GetTCName(nstmid)
            sname=sname.upper()

        tcvitalscard="%4s %3s %-9s %8s %04d %s %s %s %s %s %s %s %s %s %s %s %s %s %s"%\
            (tcVcenterid,stm3id,sname[0:9],
             self.dtg[0:8],int(self.dtg[8:10])*100,
             clat,clon,
             vitdir,vitspd,
             vitpmin,
             vitpoci,vitroci,
             vitvmax,vitrmax,
             vitr34ne,vitr34se,vitr34sw,vitr34nw,
             vitdepth)

        if(verb): print tcvitalscard
        return(tcvitalscard)



    def makeTCvCards(self,basin=None,override=0,writefile=0,verb=0,scp2jet=0,ropt='quiet',filename='tcvitals',tcvPath=None,scp2theia=0):

        from tcbase import TcVitalsDatDir
        from tcbase import w2
        
        cards=''
        for stmid in self.stmids:
            cards=cards+self.makeTCvCard(stmid)+'\n'

        if(verb): 
            print
            for card in cards.split('\n'):
                if(len(card) > 1): print card

        if(tcvPath != None):
            self.tcvpath=tcvPath
            rc=MF.WriteString2File(cards,tcvPath,verb=0)
            return(cards)

        if(basin == None):
            self.tcvpath="%s/%s.%s.txt"%(TcVitalsDatDir,filename,self.dtg)
        else:
            self.tcvpath="%s/%s.%s.%s.txt"%(TcVitalsDatDir,filename,basin,self.dtg)

        (tcvdir,tcvfile)=os.path.split(self.tcvpath)

        MF.ChkDir(TcVitalsDatDir,'mk')



        if(len(self.stmids) == 0):
            self.tcvpath=None
            return(cards)

        if(writefile):
            rc=MF.WriteString2File(cards,self.tcvpath,verb=verb)


        if(scp2jet):

            jetpath="""%s@%s:%s/%s"""%(w2.WjetScpServerLogin,w2.WjetScpServer,w2.WjetTcvitals,tcvfile)
            MF.sTimer('scp2jet')
            cmd="scp  -o ConnectTimeout=30 %s %s"%(self.tcvpath,jetpath)
            print 'jetpath: ',jetpath
            ropt=''
            mf.runcmd(cmd,ropt)
            MF.dTimer('scp2jet')

        if(scp2theia):

            theiapath="""%s@%s:%s/%s"""%(w2.TheiaScpServerLogin,w2.TheiaScpServer,w2.TheiaTcvitals,tcvfile)
            MF.sTimer('scp2theia')
            print 'theiapath: ',theiapath
            cmd="scp -o ConnectTimeout=30 %s %s"%(self.tcvpath,theiapath)
            ropt=''
            mf.runcmd(cmd,ropt)
            MF.dTimer('scp2theia')

            herapath="""%s@%s:%s/%s"""%(w2.HeraScpServerLogin,w2.HeraScpServer,w2.HeraTcvitals,tcvfile)
            MF.sTimer('scp2hera')
            print 'herapath: ',herapath
            cmd="scp -o ConnectTimeout=30 %s %s"%(self.tcvpath,herapath)
            ropt=''
            mf.runcmd(cmd,ropt)
            MF.dTimer('scp2hera')

            # -- rsync form of scp -- takes a long time... -o ConnectTimeout=30 may not work...see md2.ScpTcDss2JettheiaKishou()
            #
            #cmd='''rsync --timeout=30 --protocol=29 -alv %s "%s"'''%(self.tcvpath,theiapath)
            #mf.runcmd(cmd,ropt)

        if(w2.W2doW3Rapb and not(w2.onWjet) and not(w2.onTheia) and w2.onKaze and writefile):
            cmd="cp -v -p %s  %s/."%(self.tcvpath,w2.TcvitalsDirW3)
            mf.runcmd(cmd,ropt)


        return(cards)




    def cpTcvitals(self,dtg,ropt='',verb=0):

        from tcbase import w2

        tvdir="%s/tc/tcvitals"%(w2.W2BaseDirDat)
        tdssdir="%s/tc/DSs"%(w2.W2BaseDirDat)


        #
        # tcvitals -- local and then scp to jet
        #

        if( not(type(dtgs) is ListType) ):
            dtgs=[dtgs]

        for dtg in dtgs:
            year=dtg[0:4]
            tvpath="%s/tcvitals.%s.txt"%(tvdir,dtg)
            cmd="w2-tc-posit.py %s -v %s"%(dtg,tvpath)
            mf.runcmd(cmd,ropt)

            if(W2doWjet):
####                cmd="scp %s %s@%s:/lfs2/projects/rtfim/tcvitals/."%(tvpath,w2.WjetScpServerLogin,w2.WjetScpServer)
                cmd="scp %s %s@%s:/lfs1/projects/rtfim/tcvitals/."%(tvpath,w2.WjetScpServerLogin,w2.WjetScpServer)
                mf.runcmd(cmd,ropt)

            if(W2doW3Rapb):
                cmd="cp %s  %s/."%(tvpath,TcvitalsDirW3)
                mf.runcmd(cmd,ropt)

        dssmdeck="%s/mdecks.pypdb"%(tdssdir)
####        cmd="scp %s %s@%s:/lfs2/projects/fim/fiorino/w21/dat/tc/DSs/."%(dssmdeck,w2.WjetScpServerLogin,w2.WjetScpServer)
        cmd="scp %s %s@%s:/lfs1/projects/fim/fiorino/w21/dat/tc/DSs/."%(dssmdeck,w2.WjetScpServerLogin,w2.WjetScpServer)
        mf.runcmd(cmd,ropt)

        return

class StormData(MFbase):

    from tcbase import JtwcBaseDir,NhcBaseDir
    
    jtStmTable="%s/storms.table.txt"%(JtwcBaseDir)
    jtStmTable="%s/storm.table"%(JtwcBaseDir)
    jtStmTables=glob.glob("%s/storm*"%(JtwcBaseDir))
    
    #nhcStmTable="%s/storm.table"%(NhcBaseDir)
    nhcStmTable="%s/storm_list.txt"%(NhcBaseDir)

    def __init__(self,verb=1):

        self.stm2Data={}
        self.stm1Data={}
        self.stm2idTOstm1id={}

        jtcards=[]
        for jtStmTable in self.jtStmTables:
            jtcards=jtcards+MF.ReadFile2List(jtStmTable)

        nhccards=MF.ReadFile2List(self.nhcStmTable)

        self.parseCards(jtcards,source='jt',verb=verb)
        self.parseCards(nhccards,source='nhc',verb=verb)

        

    def parseCards(self,cards,source='jt',verb=0,warn=0):
        

        for card in cards:
            tt=card.split(',')

            if(len(tt) < 5): continue
            
            name=tt[0].strip()
            ob2id=tt[1].strip()
            ob1id=tt[2].strip()
            p1b2id=p2b2id=p3b2id=p4b2id=None
            if(tt[3] != ' ' ):  p1b2id=tt[3].strip()
            if(tt[4] != ' ' ):  p2b2id=tt[4].strip()
            if(tt[5] != ' ' ):  p3b2id=tt[5].strip()
            if(tt[6] != ' ' ):  p4b2id=tt[6].strip()

            snum=tt[7].strip()
            year=tt[8].strip()
            tccode=tt[9].strip()
            # bugs
            if(tccode.lower() == 'gu'): tccode='hu'.upper()

            bdtg=tt[11].strip()
            edtg=tt[12].strip()
            
            # -- don't let nhc set jt basin names
            #
            if(source == 'nhc' and IsJtwcBasin(ob2id) == 1):
                if(warn): print """StormData.parseCards(source='nhc') bypass nhc setting jtwc name for""",ob2id,year
                continue

            if(verb):
                if(p1b2id != None):
                    print '11111111111111111 ',name,ob2id,ob1id,snum,year,tccode,bdtg,edtg,p1b2id,p2b2id,p3b2id,p4b2id
                if(p2b2id != None):
                    print '2222222222222222 ',tt[0:-1]
                    print '2222222222222222 ',name,ob2id,ob1id,snum,year,tccode,bdtg,edtg,p1b2id,p2b2id,p3b2id,p4b2id
                if(p3b2id != None):
                    print '33333333333333333 ',tt[0:-1]
                    print '33333333333333333 ',name,ob2id,ob1id,snum,year,tccode,bdtg,edtg,p1b2id,p2b2id,p3b2id,p4b2id

            if(ob2id == 'SL'): ob1id='q'
            
            stm2id="%s%s.%s"%(ob2id,snum,year)
            stm2id=stm2id.lower()

            stm1id="%s%s.%s"%(snum,ob1id,year)
            stm1id=stm1id.lower()

            #if(stm1id == '18p.2012'): print '0000000000000000 ',name,stm2id,stm1id,ob2id,ob1id,snum,year,tccode,bdtg,edtg,p1b2id,p2b2id,p3b2id,p4b2id
            if(verb): print '0000000000000000 ',name,stm2id,stm1id,ob2id,ob1id,snum,year,tccode,bdtg,edtg,p1b2id,p2b2id,p3b2id,p4b2id

            self.stm2Data[stm2id]=(name,tccode,bdtg,edtg,p1b2id,p2b2id,p3b2id,p4b2id)
            self.stm1Data[stm1id]=(name,tccode,bdtg,edtg,p1b2id,p2b2id,p3b2id,p4b2id)
            self.stm2idTOstm1id[stm2id]=stm1id
            

    def getStmData(self,stmid):

        stmid=stmid.lower()
        rc=None
        gotit=0

        try:
            rc=self.stm2Data[stmid]
            gotit=1
        except:              None
        if(gotit == 1): return(rc)
        
        try:     rc=self.stm1Data[stmid]
        except:  None
        return(rc)
            
        #rc=(name,tccode,bdtg,edtg,p1b2id,p2b2id,p3b2id,p4b2id)


class ABdata(MFbase):
    """TC vitals from ATCF A/Bdecks"""


    undef=-999

    def __init__(self,
                 rlat,rlon,
                 vmax,
                 pmin=undef,
                 dir=undef,
                 spd=undef,
                 tccode='XX',
                 tdo=undef,
                 poci=undef,
                 roci=undef,
                 rmax=undef,
                 deye=undef,
                 depth=undef,
                 name=undef,
                 b1id='X',
                 b2id='XX',
                 snum='XX',
                 verb=0):

        self.rlat=rlat
        self.rlon=rlon

        if(vmax  != self.undef): self.vmax=vmax
        if(vmax  == 0):          self.vmax=self.undef
        if(pmin  != self.undef): self.pmin=pmin
        if(dir   != self.undef): self.dir=dir
        if(spd   != self.undef): self.spd=spd
        if(tccode != 'XX'):      self.tccode=tccode
        if(b1id  != 'X'):        self.b1id=b1id
        if(b2id  != 'XX'):       self.b2id=b2id
        if(snum  != 'XX'):       self.snum=snum
        if(tdo   != self.undef): self.tdo=tdo
        if(poci  != self.undef): self.poci=poci
        if(roci  != self.undef): self.roci=roci
        if(rmax  != self.undef): self.rmax=rmax
        if(deye  != self.undef): self.deye=deye
        if(depth != self.undef): self.depth=depth
        if(name  != self.undef): self.name=name


    def setR30(self,r30):
        r30m=self.meanQuad(r30)
        self.r30=r30
        self.r30m=r30m

    def setR34(self,r34):
        (self.r34,self.r34m)=self.meanQuad(r34)

    def setR50(self,r50):
        (self.r50,self.r50m)=self.meanQuad(r50)

    def setR64(self,r64):
        (self.r64,self.r64m)=self.meanQuad(r64)

    def setR100(self,r100):
        (self.r100,self.r100m)=self.meanQuad(r100)

    def meanQuad(self,quad):
        mean=0.0
        nmean=0
        for q in quad:
            if(q != self.undef):
                mean=mean+q
                nmean=nmean+1

        if(nmean > 0):
            mean=mean/float(nmean)

        return(quad,mean)




class MDdataset(MFbase):

    undef=-999.
    
    def __init__(self,dtgs,stm2id):

        self.dtgs=dtgs
        self.stm2id=stm2id
        self.stm1id=stm2idTostm1id(stm2id)
        
        self.cq00={}
        self.cq12={}
        self.cq24={}
        self.best={}
        self.wrng={}
        self.of00={}
        self.of03={}
        self.of12={}
        self.of24={}


    def setMDtrk(self,verb=0,docq00=1,btonly=0,only6h=1,useVmax4TcCode=1,
                 dob1idSet=0):

        # -- look for breaks in the dtg
        #
        self.dtgs=self.chkDtgBreaks(self.dtgs,verb=verb)
        
        dtgs=self.dtgs
        dtgs.sort()

        ndtgs=len(dtgs)

        if(only6h):
            dtgs=[]
            for dtg in self.dtgs:
                ihmod=int(dtg[8:10])%6
                if(ihmod == 0):
                    dtgs.append(dtg)
            self.dtgs=dtgs

        self.trk={}
        self.btdtgs=[]

        # -- check to make sure there is eighter carq0 or bt0
        #
        
        idtgs=[]
        for dtg in dtgs:
            c0=None
            try:     c0=self.cq00[dtg]
            except:  None
            bt=None
            try:     bt=self.best[dtg]
            except:  None

            if(c0 == None and bt== None):
                print 'WWWW no c0 or bt for stmid: ',self.stm1id,' dtg: ',dtg
            else:
                idtgs.append(dtg)

        dtgs=idtgs
        self.dtgs=idtgs

        dtgs.sort()
        self.dtgs.sort()
        ndtgs=len(self.dtgs)

        # -- get btdtgs
        #

        for dtg in dtgs:
            
            bt=None
            try:     bt=self.best[dtg]
            except:  None

            if(bt == None): continue
            self.btdtgs.append(dtg)

            
        if(btonly):
            dtgs=self.btdtgs
            ndtgs=len(dtgs)
            self.dtgs=dtgs

        # -- get b1id

        b1ids=[]
        b1id=None
        sname=None
        
        for dtg in dtgs:

            c0=None
            try:     c0=self.cq00[dtg]
            except:  None

            
            if(c0 == None): continue
            if(hasattr(c0,'b1id')):
                if(c0.b1id != c0.undef): 
                    b1id=c0.b1id
                    b1ids.append(b1id)

        # -- check for case where beginning b1d in the carq card is different from the end
        #
        if(dob1idSet):
            if(len(b1ids) == 1): 
                b1id=b1ids[0]
            
            elif(len(b1ids) > 1):
                bb1id=b1ids[0]
                # -- check for multiple  b1ids in the CARQ, e.g., wpac -> IO
                for tb1 in b1ids[1:]:
                    if(tb1 != bb1id):
                        print
                        print
                        for x in range(0,5):
                            print 'WWWW---- b1id changes for stm1id: ',self.stm1id,'... use the first one: ',bb1id
                        print
                        print
                        break
                    
                b1id=bb1id
                    
            

                        

        ntrk=0
        for dtg in dtgs:

            c0=None
            try:     c0=self.cq00[dtg]
            except:  None

            c12=None
            try:     c12=self.cq12[dtg]
            except:  None

            c24=None
            try:     c24=self.cq24[dtg]
            except:  None

            bt=None
            try:     bt=self.best[dtg]
            except:  None

            o0=None
            try:     o0=self.of00[dtg]
            except:  None

            o12=None
            try:     o12=self.of12[dtg]
            except:  None

            o24=None
            try:     o24=self.of24[dtg]
            except:  None

            w0=None
            try:     w0=self.wrng[dtg]
            except:  None

            lf=rlat=rlon=vmax=pmin=spd=dir=tccode=r34m=r50m=sname=None
            clf=crlat=crlon=cvmax=cpmin=cspd=cdir=ctccode=cr34m=cr50m=csname=None
            blf=brlat=brlon=bvmax=bpmin=bspd=bdir=btccode=br34m=br50m=bsname=None
            depth=cdepth=bdepth=None
            r34=cr34=br34=r50=cr50=br50=None
            poci=cpoci=bpoci=None
            roci=croci=broci=None
            rmax=crmax=brmax=None


            if(verb):
                print 'DDDDDDD',dtg
                if(c0 != None):
                    print 'CCC000'
                    c0.ls('lat')
                    c0.ls('lon')
                    c0.ls('vmax')
                    
                if(w0 != None):
                    print 'WWW000'
                    c0.ls('lat')
                    c0.ls('lon')
                    c0.ls('vmax')
                    
                if(c12 != None):
                    print 'CCC1212'
                    c12.ls('lat')
                    c12.ls('lon')
                    c12.ls('vmax')
                if(bt != None):
                    print 'BBB000'
                    bt.ls('lat')
                    bt.ls('lon')
                    bt.ls('vmax')
            
                if(o0 != None):
                    print 'OOO000'

                if(o24 != None):
                    print 'OOO2424'

                if(o12 != None):
                    print 'OOO1212'

            if(o0 != None or w0 != None or o12 != None or o24 != None):
                wncode='WN'
                wtccode='TW'
            else:
                wncode='NW'
                wtccode=None
                
            ntrk=ntrk+1
            tdo='---'
            alf=None
            postype='X'
            
            
            if(o0 != None):
                if(hasattr(o0,'tdo')):
                    tdo=o0.tdo

            if(c0 != None):
                crlat=c0.rlat
                crlon=c0.rlon
                if(hasattr(c0,'vmax')): cvmax=c0.vmax
                if(hasattr(c0,'pmin')): cpmin=c0.pmin
                if(hasattr(c0,'dir')):  cdir=c0.dir
                if(hasattr(c0,'spd')):  cspd=c0.spd
                if(hasattr(c0,'r34m')):  cr34m=c0.r34m
                if(hasattr(c0,'r50m')):  cr50m=c0.r50m
                if(hasattr(c0,'tccode')):
                    if(c0.tccode != self.undef): ctccode=c0.tccode
                if(hasattr(c0,'alf')):  clf=c0.alf
                if(hasattr(c0,'sname')):  csname=c0.sname
                if(hasattr(c0,'depth')):  cdepth=c0.depth
                if(hasattr(c0,'r34')):    cr34=c0.r34
                if(hasattr(c0,'r50')):    cr50=c0.r50
                if(hasattr(c0,'poci')):   cpoci=c0.poci
                if(hasattr(c0,'roci')):   croci=c0.roci
                if(hasattr(c0,'rmax')):   crmax=c0.rmax

            crlatm12=crlonm12=None
            if(c12 != None):
                crlatm12=c12.rlat
                crlonm12=c12.rlon
                
            # -- calc CARQ motion from tau-12 to tau using CARQ posits
            #
            if(c0 != None and cdir == None and crlatm12 != None and crlonm12 != None):
                dt=12
                (cdir,cspd,umotion,vmotion)=rumhdsp(crlatm12,crlonm12,crlat,crlon,dt)
                postype='c'
            elif(c0 != None and cdir != None):
                postype='C'

            if(c0 != None and cdir == None):
                postype='b'


            if(bt != None):
                brlat=bt.rlat
                brlon=bt.rlon
                
                if(hasattr(bt,'vmax')): bvmax=bt.vmax
                if(hasattr(bt,'pmin')): bpmin=bt.pmin
                if(hasattr(bt,'dir')): bdir=bt.dir
                if(hasattr(bt,'spd')): bspd=bt.spd
                if(hasattr(bt,'tccode')):
                    if(bt.tccode != self.undef):  btccode=bt.tccode
                if(hasattr(bt,'r34m')):  br34m=bt.r34m
                if(hasattr(bt,'r50m')):  br50m=bt.r50m
                if(hasattr(bt,'alf')):   blf=bt.alf
                if(hasattr(bt,'sname')): bsname=bt.sname
                if(hasattr(bt,'depth')): bdepth=bt.depth
                if(hasattr(bt,'r34')):   br34=bt.r34
                if(hasattr(bt,'r50')):   br50=bt.r50
                if(hasattr(bt,'poci')):  bpoci=bt.poci
                if(hasattr(bt,'roci')):  broci=bt.roci
                if(hasattr(bt,'rmax')):  brmax=bt.rmax



            if(docq00):

                if(crlat != None): rlat=crlat
                if(crlon != None): rlon=crlon
                if(cvmax != None): vmax=cvmax
                if(cpmin != None): pmin=cpmin
                if(cdir  != None): dir=cdir
                if(cspd  != None): spd=cspd
                if(ctccode != None): tccode=ctccode
                if(cr34m   != None): r34m=cr34m
                if(cr34    != None): r34=cr34
                if(cr50m   != None): r50m=cr50m
                if(cr50    != None): r50=cr50
                if(clf     != None): alf=clf
                if(cdepth  != None): depth=cdepth
                if(cpoci   != None): poci=cpoci
                if(croci   != None): roci=croci
                if(crmax   != None): rmax=crmax

                # -- fallback to bt
                #
                if(rlat == None): 
                    rlat=brlat
                if(rlon == None): 
                    rlon=brlon
                    postype='b'
                    
                # -- check if undef too when it's 0 in bdeck -> undef
                #
                if(vmax == None or vmax == self.undef): vmax=bvmax
                if(pmin == None or pmin == self.undef): pmin=bpmin
                if(alf  == None): alf=blf
                if(cdepth == None): depth=bdepth
                if(ctccode == None): tccode=btccode

                if(r34m == None and br34m != None): r34m=br34m
                if(r34  == None and br34  != None): r34=br34
                if(r50  == None and br50  != None): r50=br50
                if(poci == None and bpoci != None): poci=bpoci
                if(roci == None and broci != None): roci=broci
                if(rmax == None and brmax != None): rmax=brmax
                

            if(btonly):
                
                postype='B'
                
                if(brlat   != None): rlat=brlat
                if(brlon   != None): rlon=brlon
                if(bvmax   != None): vmax=bvmax
                if(bpmin   != None): pmin=bpmin
                if(bdir    != None): dir=bdir
                if(bspd    != None): spd=bspd
                if(btccode != None): tccode=btccode
                if(br34m   != None): r34m=br34m
                if(br50m   != None): r50m=br50m
                if(blf     != None): alf=blf
                if(bdepth  != None): depth=bdepth
                if(br34    != None): r34=br34
                if(br50    != None): r50=br50
                if(bpoci   != None): poci=bpoci
                if(broci   != None): roci=broci
                if(brmax   != None): rmax=brmax

                
            if(csname  != None): sname=csname
            if(sname ==  None): sname=bsname

            if(tccode == None and wtccode == None):
                if(not(Is9X(self.stm1id))):
                    if(verb): print """WWW couldn't find tccode in carq or bt; set to 'NT'""",dtg,self.stm1id
                #print """WWW couldn't find tccode in carq or bt; exit and try to figure out what happen""",dtg,self.stm1id
                tccode='NT'
            
            if(wtccode != None and tccode == None):
                tccode=wtccode

            # -- use vmax
            #
            if(useVmax4TcCode and tccode == 'NT'):
                if(vmax != None and IsTcWind(vmax)):
                    tccode='TW'
                else:
                    tccode='NT'
                
            # -- final qc
            #
            if(vmax == None): vmax=-999

            if(verb):
                print 'WWW',dtg,tccode,wncode,wtccode,o0,w0,o12,o24,wncode
                print
            
            self.trk[dtg]=Trkdata(rlat,rlon,vmax,pmin,dir,spd,tccode,wncode,b1id=b1id,tdo=tdo,ntrk=ntrk,ndtgs=ndtgs,
                                  r34m=r34m,r50m=r50m,depth=depth,
                                  r34=r34,r50=r50,poci=poci,roci=roci,
                                  rmax=rmax)

            self.trk[dtg].tdo=tdo
            self.trk[dtg].alf=alf
            self.trk[dtg].sname=sname
            self.trk[dtg].stmid=self.stm1id
            self.trk[dtg].postype=postype


        # -- get prev 12-h track dir/spd
        #
        
        dirspd={}
        for n in range(0,ndtgs):

            dtg=dtgs[n]
            if(n == 0):
                nm1=n
                if(ndtgs > 2):  n0=n+2
                else:           n0=n+1
            elif(n == 1):
                nm1=n-1
                if(ndtgs > 2):  n0=n+1
                else:           n0=n+1
            elif(n == ndtgs-1):
                nm1=n-2
                if(ndtgs > 2):  n0=n
                else:           n0=n
            else:
                nm1=n-2
                n0=n

            if(n0 > ndtgs-1):
                trkdir=self.undef
                trkspd=self.undef
            else:
                
                rlatm1=self.trk[dtgs[nm1]].rlat
                rlonm1=self.trk[dtgs[nm1]].rlon
                rlat0=self.trk[dtgs[n0]].rlat
                rlon0=self.trk[dtgs[n0]].rlon
                
                dt=mf.dtgdiff(dtgs[nm1],dtgs[n0])
                (trkdir,trkspd,umotion,vmotion)=rumhdsp(rlatm1,rlonm1,rlat0,rlon0,dt)
                
            dirspd[dtg]=(trkdir,trkspd)

        self.ndtgs=ndtgs

        # -- look for warning status in shem/io if WN t-1 or t+2
        #

        if(IsIoShemBasin(self.stm2id[0:2])):
            self.interpWarn(dtgs,verb=verb)

        # -- set the bt dir/spd and dirtype
        #
        for dtg in dtgs:
            
            self.trk[dtg].dirtype=self.trk[dtg].postype

            if( (self.trk[dtg].dir == None) or btonly):
                (trkdir,trkspd)=dirspd[dtg]
                if(self.trk[dtg].postype == 'c'):
                    self.trk[dtg].dirtype='b'
                    
                self.trk[dtg].dir=trkdir   
                self.trk[dtg].spd=trkspd    
                
            self.trk[dtg].trkdir=trkdir   
            self.trk[dtg].trkspd=trkspd    


    def chkDtgBreaks(self,dtgs,maxdiff=240,verb=0):

        ndtgs=[]
        dtgs.sort()
        foundbreak=0

        ldtgs=len(dtgs)
        for n in range(len(dtgs)-2,-1,-1):
            dt=mf.dtgdiff(dtgs[n],dtgs[n+1])
            ndtgs.append(dtgs[n+1])
            if(verb): print 'dddd chkDtgBreaks:',n,dtgs[n],dtgs[n+1],dt
            if(dt > maxdiff):
                print 'WWW(tcCL.MDdataset.chkDtgBreaks n: ',n,' dt: ',dt,' dtgs[n]: ',dtgs[n],' dtgs[n+1]: ',dtgs[n+1],' foundbreak=1'
                foundbreak=1
                break

        if(not(foundbreak)): ndtgs=dtgs
        lndtgs=len(ndtgs)
        return(ndtgs)


    def interpWarn(self,odtgs,verb=0):

        ndtgs=len(odtgs)

        firstWN=0
        lastWN=ndtgs
        
        # -- find first and last warning
        #
        for n in range(0,ndtgs):
            wn0=self.trk[odtgs[n]].wncode
            if(wn0 == 'WN'): 
                firstWN=n
                break
            
        for n in range(ndtgs-1,0,-1):
            wn0=self.trk[odtgs[n]].wncode
            if(wn0 == 'WN'): 
                lastWN=n
                break
            
        if(verb): print 'firstWN: ',firstWN,'lastWN: ',lastWN,'ndtgs: ',ndtgs

        for n in range(firstWN,lastWN+1):
            
            if(ndtgs >= 2 and n <= ndtgs-2):
                
                if(n == 0):
                    nm1=n
                    n0=n
                    np1=n+1
                else:
                    nm1=n-1
                    n0=n
                    np1=n+1
                    
                wnm1=self.trk[odtgs[nm1]].wncode
                wn0=self.trk[odtgs[n0]].wncode
                wnp1=self.trk[odtgs[np1]].wncode
                    
                if(verb):
                    print 'nnnnn ',n,odtgs[n],'nm1:',nm1,wnm1,'n0:',n0,wn0,'np1:',np1,wnp1
                
                if( 
                    ( (wn0 == 'NW' and wnp1 == 'WN') or (wn0 == 'NW' and wnm1 == 'WN') )
                    ):

                    # -- don't interp back if first point or last
                    #
                    self.trk[odtgs[n0]].wncode='WN'
                    if(verb): print 'AAAAA ',ndtgs,n,nm1,n0,np1,self.trk[odtgs[n0]].wncode


    def cleanMD(self):

        #try: del self.cq00
        #except: None
        
        #try: del self.cq12
        #except: None
        
        #try: del self.cq24
        #except: None
        
        try: del self.best
        except: None
        
        try: del self.wrng
        except: None
        
        try: del self.of00
        except: None
        
        try: del self.of03
        except: None


    def getMDtrk(self):

        otrk={}
        dtgs=self.trk.keys()
        dtgs.sort()

        for dtg in dtgs:
            otrk[dtg]=self.trk[dtg].gettrk()

        return(otrk,dtgs)
    
    def getMDotrk(self):

        otrk={}
        dtgs=self.trk.keys()
        dtgs.sort()

        for dtg in dtgs:
            otrk[dtg]=self.trk[dtg]

        return(otrk,dtgs)

                
    def lsMDtrk(self,filtTCs=0,doprint=1):


        cards={}
        (otrk,dtgs)=self.getMDtrk()

        for dtg in dtgs:

            (rlat,rlon,vmax,pmin,dir,spd,tccode,wncode,trkdir,trkspd,dirtype,b1id,tdo,
             ntrk,ndtgs,r34m,r50m,alf,sname,r34,r50,depth)=self.trk[dtg].gettrk()
            
            ostmid=self.stm1id
            if(hasattr(self.trk[dtg],'ostmid')): ostmid=self.trk[dtg].ostmid

            gentrk=0
            if(hasattr(self,'gendtgs')):
                if(dtg in self.gendtgs): gentrk=1
            if(rlat != None):
                (clat,clon)=Rlatlon2Clatlon(rlat,rlon,dodec=1)
                if(filtTCs and not(IsTc(tccode))): 
                    card="%s -- not a TC...and filtTCs=1"
                else:
                    card=printTrk(ostmid,dtg,rlat,rlon,vmax,pmin,dir,spd,dirtype,
                                  tdo=tdo,tccode=tccode,wncode=wncode,
                                  ntrk=ntrk,ndtgs=ndtgs,r34m=r34m,r50m=r50m,
                                  alf=alf,sname=sname,gentrk=gentrk,doprint=doprint)
                    
                cards[dtg]=card

        return(cards)
                
                

class MDdeck(Adeck):


    def __init__(self,cards,
                 b2id,bnum,byear,
                 verb=0):

        #from w2 import SetLandFrac
        #from w2 import GetLandFrac

        self.b2id=b2id
        self.bnum=bnum
        self.byear=byear

        self.dofilt9x=0
        
        self.undef=-999
        self.skipcarq=0
        self.chkb2id=1
        self.warn=1
        self.verb=verb

        # -- all cards
        self.cards=cards.split('\n')

        # -- just mdeck related cards
        self.mdcards={}
        
        self.lf=w2.SetLandFrac()
        self.getlf=w2.GetLandFrac

        self.initMDcards()
        self.setMD()


    def initMDcards(self,warn=0,doGenesisCards=1):

        self.curb2id=-999
        self.curbnum=-999
        self.curbyear=-999
        
        for card in self.cards:
            tt=card.split(',')
            # -- scan for genesis nhc cards
            if(mf.find(card,'GENESIS')):
                if(warn): print 'WWW NHC genesis posit...ignore',card
                # -- maybe use?
                if(not(doGenesisCards)): continue
            
            if(len(tt) < 5):
                if(warn): print 'WWW short card in MDdeck.initMDcards: ',card
                continue
            aid=self.setAidNCard(tt)
            if(aid == 'BEST' or
               aid == 'CARQ' or aid == 'WRNG' or aid == 'CNTR' or aid == 'COMS' or
               aid == 'JTWC' or aid == 'OFCL'
               ):
                rc=self.makeBidDtg(tt,card)
                # -- bail for 80-89 storms, etc
                if(rc == None):
                    #print 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa ',rc
                    continue

                else:
                
                    (dtg,b2id,bnum,byear)=rc

                    if(self.chkStm2id() > 0):
                        print 'WWWWWWWWWWWW multiple stmids in this adeck...sayoonara'
                        sys.exit()

                    MF.loadDictList(self.mdcards,dtg,card)

        self.stm2id="%s%s.%s"%(self.b2id,self.bnum,self.byear)


    def chkStm2id(self):
        
        if(self.curb2id != self.b2id): self.curb2id=self.b2id
        if(self.curbnum != self.bnum): self.curbnum=self.bnum
        if(self.curbyear != self.byear): self.curbyear=self.byear

        rc=0
        if(self.curb2id != self.b2id): rc=1
        if(self.curbnum != self.bnum): rc=2
        if(self.curbyear != self.byear): rc=3

        return(rc)
        


    def setMD(self):

        dtgs=self.mdcards.keys()
        dtgs.sort()

        # -- stm2id
        #
        mD=MDdataset(dtgs,self.stm2id)
        
        for dtg in dtgs:
            cards=self.mdcards[dtg]
            
            for card in cards:
                self.ParseABdeckCard(mD,dtg,card)

        self.mD=mD


    def getMDByDtgs(self,dtgs,stm2id):


        # -- stm2id
        #
        mD=MDdataset(dtgs,stm2id)
        
        for dtg in dtgs:
            cards=self.mdcards[dtg]
            for card in cards:
                self.ParseABdeckCard(mD,dtg,card)

        return(mD)


    def getDtgRange(self,mD,nhours=48,diffdtgTol=36.0,ddtg=6,verb=0):
        
        """ adecks can have multiple storms because they are not cleaned like bdecks; look for a break in the dtgs > nhours
        """

        def checkDtgDdtg(dtgs,ddtg):
            chkddtg=ddtg*1.0
            cntDtgs=[]
            ndtgs=len(dtgs)
            # -- case for 1 dtg
            if(ndtgs == 1): 
                ne=1
            else:
                ne=ndtgs-1
                
            for n in range(0,ne):
                dtg0=dtgs[n]
                
                # -- handling 1 dtgs
                if(ndtgs == 1): 
                    dtg1=dtgs[n]
                    cntDtgs.append(dtg1)
                    print 'WWW:MDeck.getDtgRange 11111111111111 dtg -- set cntDtg to this one and return'
                    return(cntDtgs)
                else:
                    dtg1=dtgs[n+1]
                diffdtg=mf.dtgdiff(dtg0,dtg1)
                #print 'n:',n,ndtgs-1,dtg0,dtg1,diffdtg,chkddtg
                if(diffdtg != chkddtg):
                    print 'WWW:MDeck.getDtgRange.checkDtg6h() -- continuity problem n: %02d'%(n+1),' ndtgs: %2d'%(len(dtgs)),'dtg0: ',dtg0,'dtg1: ',dtg1
                    if(n+1 == ndtgs-1):
                        print 'problem at end -- remove dtg: ',dtg1,' by bumping n increment'
                        n=n+1
                    else:
                        # -- we use 18 h because of JTWC SHEM real storm bdecks can have gaps that will be filled in by 9X
                        # -- use 36 h because of JTWC 19W.16 had a 24.0 h gap when the did the renameing of e1w.16 -> 19w.16
                        #
                        if(diffdtg <= diffdtgTol):
                            cntDtgs.append(dtg0)
                        else:
                            print 'problem NOT at end and diffdtg > diffdtgTol ',diffdtgTol,'-- stop!'
                            sys.exit()
                else:
                    cntDtgs.append(dtg0)
                
                if(n == ndtgs-2):
                    cntDtgs.append(dtg1)
                    #print 'fffffffoooooo---finalize: %2d'%(n),dtg1,mD.stm1id
                    
            return(cntDtgs)
                        
        # -- mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
        #
        
        dtgs=mD.dtgs
        mD.uniqStmdtgs={}
        nd=len(dtgs)
        
        # -- check for posits
        #
        if(nd == 0):
            return
        
        bdtg=dtgs[0]
        for n in range(0,nd):
            dtg0=dtgs[n]
            if(n < nd-1):
                dtg1=dtgs[n+1]
            else:
                dtg1=dtg0

            dtgdiff=mf.dtgdiff(dtg0,dtg1)
            if(dtgdiff > nhours or n == nd-1):
                edtg=dtg0
                if(verb): print 'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB: ',n,' bdtg: ',bdtg,' edtg: ',edtg,' dtgdiff: ',dtgdiff

                alldtgs=[]
                for tdtg in mf.dtgrange(bdtg,edtg,ddtg):
                    if(tdtg in dtgs): alldtgs.append(tdtg)
                    
                # -- check continuity of dtgs
                #
                finaldtgs=checkDtgDdtg(alldtgs,ddtg)
                
                # -- if no dtgs do not set the uniqStmdtgs...
                #
                if(len(finaldtgs) > 0):
                    mD.uniqStmdtgs[bdtg]=finaldtgs
                
                # -- set bdtg of next serious to dtg1 with diff > nhours
                #
                bdtg=dtg1

        


    def getDtgRangeNN(self,mD,nhours=48,diffdtgTol=36.0,ddtg=6,verb=0):
        
        """ adecks can have multiple storms because they are not cleaned like bdecks; look for a break in the dtgs > nhours
        """

        def checkDtgDdtg(dtgs,ddtg):
            
            chkddtg=ddtg*1.0
            cntDtgs=[]
            ndtgs=len(dtgs)
            # -- case for 1 dtg
            if(ndtgs == 1): 
                ne=1
            else:
                ne=ndtgs-1
                
            n=0
            while(n < ne):
                dtg0=dtgs[n]
                
                # -- handling 1 dtgs
                if(ndtgs == 1): 
                    dtg1=dtgs[n]
                    cntDtgs.append(dtg1)
                    print 'WWW:MDeck.getDtgRangeNN.checkDtg6h() -- 1111111 dtg -- set cntDtg to this one and return'
                    return(cntDtgs)
                else:
                    dtg1=dtgs[n+1]
                    
                diffdtg=mf.dtgdiff(dtg0,dtg1)
                #print 'n------------------------------:',n,ndtgs-1,dtg0,dtg1,diffdtg,chkddtg
                if(diffdtg != chkddtg):
                    print 'WWW:MDeck.getDtgRangeNN.checkDtg6h() -- continuity problem n: %2d'%(n+1),' ndtgs: %2d'%(len(dtgs)),'dtg0: ',dtg0,'dtg1: ',dtg1,\
                          'diffdtg: ',diffdtg,' stmid: ',mD.stm1id   
                    if(n+1 == ndtgs-1):
                        print
                        print 'WWW:MDeck.getDtgRangeNN.checkDtg6h() -- problem at end -- remove dtg: ',dtg1,' by bumping n increment +2 for stmid: ',mD.stm1id
                        n=n+2
                    else:
                        # -- we use 18 h because of JTWC SHEM real storm bdecks can have gaps that will be filled in by 9X
                        # -- use 36 h because of JTWC 19W.16 had a 24.0 h gap when the did the renameing of e1w.16 -> 19w.16
                        #
                        if(diffdtg <= diffdtgTol):
                            cntDtgs.append(dtg0)
                            n=n+1
                        else:
                            print
                            print 'WWW:MDeck.getDtgRangeNN.checkDtg6h() -- problem NOT at end and diffdtg: ',diffdtg,' > diffdtgTol ',diffdtgTol,(n+1),ndtgs-1
                            if((n+1) <= 3 and ndtgs > 4):
                                print 'WWW:MDeck.getDtgRangeNN.checkDtg6h() -- problem at BEGINNING...toss first dtgs before the break at: ',dtg1,n,ndtgs
                                cntDtgs=[]
                                cntDtgs.append(dtg1)
                                
                            n=n+1
                                
                else:
                    cntDtgs.append(dtg0)
                    n=n+1
                
                if(n == ndtgs-1):
                    #print 'fffffffnnnnnn---finalize: %2d'%(n),dtg1,mD.stm1id
                    cntDtgs.append(dtg1)
                    
            return(cntDtgs)
                        
        # -- mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
        #
        
        dtgs=mD.dtgs
        mD.uniqStmdtgs={}
        nd=len(dtgs)
        
        # -- check for posits
        #
        if(nd == 0):
            return
        
        bdtg=dtgs[0]
        for n in range(0,nd):
            dtg0=dtgs[n]
            if(n < nd-1):
                dtg1=dtgs[n+1]
            else:
                dtg1=dtg0

            dtgdiff=mf.dtgdiff(dtg0,dtg1)
            if(dtgdiff > nhours or n == nd-1):
                edtg=dtg0
                if(verb): print 'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB: %2d'%(n),' bdtg: ',bdtg,' edtg: ',edtg,' dtgdiff: %3.0f'%(dtgdiff),mD.stm1id

                alldtgs=[]
                for tdtg in mf.dtgrange(bdtg,edtg,ddtg):
                    if(tdtg in dtgs): alldtgs.append(tdtg)
                    
                # -- check continuity of dtgs
                #
                finaldtgs=checkDtgDdtg(alldtgs,ddtg)
                
                if(len(finaldtgs) > 0):
                    bdtg=finaldtgs[0]
                    mD.uniqStmdtgs[bdtg]=finaldtgs
                    
                # -- set bdtg for next series
                #
                bdtg=dtg1


    def ParseABdeckCard(self,mD,dtg,adcard):
        """
atcf='''BASIN,CY,YYYYMMDDHH,TECHNUM/MIN,TECH,TAU,LatN/S,LonE/W,VMAX,MSLP,TY,RAD,WINDCODE,RAD1,RAD2,RAD3,RAD4,RADP,RRP,MRD,GUSTS,EYE,SUBREGION,MAXSEAS,INITIALS,DIR,SPEED,STORMNAME,DEPTH,SEAS,SEASCODE,SEAS1,SEAS2,SEAS3,SEAS4,USERDEFINED,userdata'''
ttt=atcf.split(',')
for n in range(0,len(ttt)):
    print '''        # %02d, %s'''%(n,ttt[n])
sys.exit()
"""


        # 00, BASIN
        # 01, CY
        # 02, YYYYMMDDHH
        # 03, TECHNUM/MIN
        # 04, TECH
        # 05, TAU
        # 06, LatN/S
        # 07, LonE/W
        # 08, VMAX
        # 09, MSLP
        # 10, TY
        # 11, RAD
        # 12, WINDCODE
        # 13, RAD1
        # 14, RAD2
        # 15, RAD3
        # 16, RAD4
        # 17, RADP
        # 18, RRP
        # 19, MRD
        # 20, GUSTS
        # 21, EYE
        # 22, SUBREGION
        # 23, MAXSEAS
        # 24, INITIALS
        # 25, DIR
        # 26, SPEED
        # 27, STORMNAME
        # 28, DEPTH
        # 29, SEAS
        # 30, SEASCODE
        # 31, SEAS1
        # 32, SEAS2
        # 33, SEAS3
        # 34, SEAS4
        # 35, USERDEFINED
        # 36, userdata


        undef=-999
        sname=''


        def chkRquad(quad):

            allundef=1
            for q in quad:
                if(q != undef): allundef=0

            return(allundef)
        
        def SC2(tt,nn):
            try:
                ostr=tt[nn].strip()
            except:
                ostr=''
            return(ostr)

        def SC(istr):
            ostr=istr[0:-1].strip()
            return(ostr)

        def setRadiicode(rwind):

            if(not(rwind.isdigit())):
                crcode=undef
                return(crcode)
            rwind=int(rwind)
            
            crcode=undef
            if(rwind == 30):                 crcode='r30'
            if(rwind == 35 or rwind == 34):  crcode='r34'
            if(rwind == 50):                 crcode='r50'
            if(rwind == 100):                crcode='r100'
            if(rwind == 64 or rwind == 65):  crcode='r64'
            return(crcode)


        def setDigit(cvar,nezero=0):
            if(cvar.isdigit() or ('-' in cvar)):
                cvar=int(cvar)
            else:
                cvar=undef
            if(nezero and cvar == 0): cvar=undef
            return(cvar)
            

        def setString(cvar,doalpha=1):
            if(not(cvar.isalpha()) and doalpha or (len(cvar) == 0) ):
                cvar=undef
            if(cvar == 'X'): cvar=undef
            return(cvar)


        def setRadii(mm,rcode,rquad):
            
            if(rcode == 'r30'  and chkRquad(rquad) == 0 ): mm.setR30(rquad)
            if(rcode == 'r34'  and chkRquad(rquad) == 0 ): mm.setR34(rquad)
            if(rcode == 'r50'  and chkRquad(rquad) == 0 ): mm.setR50(rquad)
            if(rcode == 'r64'  and chkRquad(rquad) == 0 ): mm.setR64(rquad)
            if(rcode == 'r100' and chkRquad(rquad) == 0 ): mm.setR100(rquad)



        # -- split the card
        tt=adcard.split(',')
        ntt=len(tt)

            
        if(self.verb):
            print '   ntt: ',ntt,' adcard: ',tt
            #adcard[:-1].strip()
            if(self.verb == 2):
                for i in range(0,ntt):
                    print 'adflds: ',i,tt[i]


        nn=0
        b2id=SC2(tt,nn)                                ; nn=nn+1 # 00
        snum=setDigit(SC2(tt,nn))                      ; nn=nn+1 # 01
        dtg=setString(SC2(tt,nn),doalpha=0)            ; nn=nn+1 # 02
        aidnum=setDigit(SC2(tt,nn))                    ; nn=nn+1 # 03
        aid=setString(SC2(tt,nn))                      ; nn=nn+1 # 04
        tau=setDigit(SC2(tt,nn))                       ; nn=nn+1 # 05
        clat=setString(SC2(tt,nn),doalpha=0)           ; nn=nn+1 # 06
        clon=setString(SC2(tt,nn),doalpha=0)           ; nn=nn+1 # 07
        vmax=setDigit(SC2(tt,nn))                      ; nn=nn+1 # 08
        pmin=setDigit(SC2(tt,nn),nezero=1)             ; nn=nn+1 # 09
        tccode=setString(SC2(tt,nn))                   ; nn=nn+1 # 10
        rcode=setRadiicode(SC2(tt,nn))                 ; nn=nn+1 # 11
        qcode=setString(SC2(tt,nn))                    ; nn=nn+1 # 12
        rne=setDigit(SC2(tt,nn),nezero=1)              ; nn=nn+1 # 13
        rse=setDigit(SC2(tt,nn),nezero=1)              ; nn=nn+1 # 14
        rsw=setDigit(SC2(tt,nn),nezero=1)              ; nn=nn+1 # 15
        rnw=setDigit(SC2(tt,nn),nezero=1)              ; nn=nn+1 # 16
        radii=[rne,rse,rsw,rnw]
        rquad=radii
        
        # -- convert radii to standard quadrants based on qcode
        #
        if(qcode != undef):   rquad=WindRadiiCode2Normal(qcode,radii)

        poci=setDigit(SC2(tt,nn))                      ; nn=nn+1 # 18
        roci=setDigit(SC2(tt,nn))                      ; nn=nn+1 # 19
        rmax=setDigit(SC2(tt,nn))                      ; nn=nn+1 # 20
        gusts=setDigit(SC2(tt,nn))                     ; nn=nn+1 # 20
        deye=setDigit(SC2(tt,nn),nezero=1)             ; nn=nn+1 # 21
        b1id=setString(SC2(tt,nn))                     ; nn=nn+1 # 22
        maxseas=setDigit(SC2(tt,nn))                   ; nn=nn+1 # 23
        tdo=setString(SC2(tt,nn))                      ; nn=nn+1 # 24
        dir=setDigit(SC2(tt,nn))                       ; nn=nn+1 # 25
        spd=setDigit(SC2(tt,nn))                       ; nn=nn+1 # 26
        name=setString(SC2(tt,nn),doalpha=0)           ; nn=nn+1 # 27
        depth=setString(SC2(tt,nn))                    ; nn=nn+1 # 28


        if(clat == undef):
            if(self.verb):
                print 'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW undef clat/clon in ParseABdeckCard ',dtg,snum,b2id
            return

        (rlat,rlon)=Clatlon2Rlatlon(clat,clon)

        # -- check for bad lat/lon
        if(not(rlat >= -90.0 and rlat <= 90.0)):
            print 'BBBBBBBBBBBBBBBBbaaaaaaaaaaaaaaaaddddddddddddd rlat; aid: ',aid,' dtg: ',dtg,' clat/clon: ',clat,clon
            return

        try:
            alf=self.getlf(self.lf,rlat,rlon)
        except:
            print 'ooooooooooooooopppppppppppppppppppppppssssssssssssssssssssssssss: ',rlat,rlon

        # 25W.1986 has a blank JTWC 12 h lat/lon card, if '' then return
        #
        noload=0
        if(clat == undef and self.verb):
            print 'WWWWWWW noload making mdeck from adeck card: ',adcard[:-1]
            noload=1

        abdata=ABdata(rlat,rlon,vmax,pmin,dir,spd,tccode,tdo,poci,roci,rmax,deye,depth,name,b1id,snum,b2id)
        abdata.alf=alf


        if(name != undef and sname != 'NONAME'):
            sname=name

        
        if(aid == 'CARQ' and tau == 0):

            try:
                mm=mD.cq00[dtg]
            except:
                mD.cq00[dtg]=abdata
                mm=mD.cq00[dtg]
                
            setRadii(mm,rcode,rquad)
            mm.sname=sname
            mD.cq00[dtg]=mm

        if(aid == 'BEST'):

            try:
                mm=mD.best[dtg]
            except:
                mD.best[dtg]=abdata
                mm=mD.best[dtg]

            setRadii(mm,rcode,rquad)
            mm.sname=sname
            mD.best[dtg]=mm
            

            if(self.verb): print 'bbbbb',b2id,b1id,snum,dtg,tau,aid,rlat,rlon,vmax,pmin,\
                           rcode,rquad,poci,roci,rmax,gusts,deye,tdo,dir,spd,name,depth
        
            
        if( (aid == 'OFCL' or aid == 'JTWC') and tau == 0):

            try:
                mm=mD.of00[dtg]
            except:
                mD.of00[dtg]=abdata
                mm=mD.of00[dtg]

            setRadii(mm,rcode,rquad)
            mD.of00[dtg]=mm

            
        if( (aid == 'OFCL' or aid == 'JTWC') and tau == 3):

            try:
                mm=mD.of03[dtg]
            except:
                mD.of03[dtg]=abdata
                mm=mD.of03[dtg]
            setRadii(mm,rcode,rquad)
            mD.of03[dtg]=mm

        if( (aid == 'OFCL' or aid == 'JTWC') and tau == 24):

            try:
                mm=mD.of24[dtg]
            except:
                mD.of24[dtg]=abdata
                mm=mD.of24[dtg]
            setRadii(mm,rcode,rquad)
            mD.of24[dtg]=mm

        if( (aid == 'OFCL' or aid == 'JTWC') and tau == 12):

            try:
                mm=mD.of12[dtg]
            except:
                mD.of12[dtg]=abdata
                mm=mD.of12[dtg]
            setRadii(mm,rcode,rquad)
            mD.of12[dtg]=mm

            
        if(aid == 'CARQ' and tau == -12):
            
            try:
                mm=mD.cq12[dtg]
            except:
                mD.cq12[dtg]=abdata
                mm=mD.cq12[dtg]
            setRadii(mm,rcode,rquad)
            mD.cq12[dtg]=mm
        
        if(aid == 'CARQ' and tau == -24):
            
            try:
                mm=mD.cq24[dtg]
            except:
                mD.cq24[dtg]=abdata
                mm=mD.cq24[dtg]
            setRadii(mm,rcode,rquad)
            mD.cq24[dtg]=mm

        if(aid == 'WRNG' and tau == 0):

            try:
                mm=mD.wrng[dtg]
            except:
                mD.wrng[dtg]=abdata
                mm=mD.wrng[dtg]
            setRadii(mm,rcode,rquad)
            mD.wrng[dtg]=mm

        
        return

    def lsBest(self,dtg):

        try:
            print 'BBB: ',dtg,self.mD.best[dtg].ls()
        except:
            print 'BBB(nada)'
            

class MDdtgs(MFbase):

    def __init__(self,dtg):

        self.dtg=dtg

        self.ostm2ids=[]
        self.stm2ids=[]
        self.genstmids=[]

        self.trks={}

    def loadDtg(self,ostm2id,stm2id,smD,dtg):

        trk=smD.trk[dtg]
        if(hasattr(smD,'sname')):
            trk.sname=smD.sname
        self.ostm2ids.append(ostm2id)
        self.ostm2ids=MF.uniq(self.ostm2ids)
        
        self.stm2ids.append(stm2id)
        self.stm2ids=MF.uniq(self.stm2ids)

        trk.ostm2id=ostm2id
        self.trks[stm2id]=trk

    def lsDtgTrk(self,dtg):

        for stmid in self.trks.keys():
            trk=self.trks[stmid]
            printTrk(stmid,dtg,trk.rlat,trk.rlon,trk.vmax,trk.pmin,
                     trk.dir,trk.spd,trk.dirtype,
                     tdo=trk.tdo,tccode=trk.tccode,wncode=trk.wncode,
                     r34m=trk.r34m,r50m=trk.r50m,
                     alf=trk.alf,sname=trk.sname)

        if(hasattr(self,'genstmids')):
            print 'GGGGG(MDdtgs.lsDtgTrk): ',dtg,self.genstmids


class TcBasin(MFbase):


    def __init__(self,basin=None):

        if(basin == None):
            self.basin=None
            self.parea=None
        else:
            self.getBasinPareaFromBasin(basin)

    def getBasinPareaFromStm1id(self,stm1id):

        (snum,b1id,year,b2id,stm2id,stm1id)=getStmParams(stm1id)
        basin=Basin1toFullBasin[b1id]
        self.getBasinPareaFromBasin(basin)
        return(self.parea)

    def isMidSeason(self,basin,dtg):
        
        rc=0
        mm=int(dtg[4:6])
        
        if(mf.find(basin,'wpac')):
            if(mm >= 7 and mm <=10): rc=1

        if(mf.find(basin,'epac')):
            if(mm >= 8 and mm <=9): rc=1
            
        if(mf.find(basin,'lant')):
            if(mm >= 7 and mm <=9): rc=1
            
        return(rc)
    

    def getBasinPareaFromBasin(self,basin):

        if(mf.find(basin,'epac')):

            self.basin='epac'
            self.parea='tropepac'
            self.tropicalLats=[-25,25]
            self.tropicalLatsMidSeason=[-30,30]

        elif(mf.find(basin,'cpac')):

            self.basin='cpac'
            self.parea='tropcpac'
            self.tropicalLats=[-25,25]


        elif(mf.find(basin,'wpac')):

            self.basin='wpac'
            self.parea='tropwpac'
            self.tropicalLats=[-25,25]
            self.tropicalLatsMidSeason=[-30,30]


        elif(mf.find(basin,'lant')):

            self.basin='lant'
            self.parea='troplant'
            self.tropicalLats=[-25,30]
            self.tropicalLatsMidSeason=[-30,35]
            

        elif(mf.find(basin,'slant')):

            self.basin='slant'
            self.parea='tropslant'
            self.tropicalLats=[-25,25]
            

        elif(mf.find(basin,'nio')):
            self.basin='nio'
            self.parea='tropnio'
            self.tropicalLats=[-25,25]

        elif(mf.find(basin,'sio')):
            self.basin='sio'
            self.parea='tropsio'
            self.tropicalLats=[-25,25]

        elif(mf.find(basin,'swpac')):
            self.basin='swpac'
            self.parea='tropswpac'
            self.tropicalLats=[-25,25]

        elif(mf.find(basin,'shem')):

            self.basin='shem'
            self.parea='tropshem'
            self.tropicalLats=[-25,25]
        

    def getBasinFromLatLon(self,lat,lon):

        self.isepac=( (lon >= 276 and lon <= 282 and lat <  9 ) or
                    (lon >= 273 and lon <  276 and lat < 12 ) or
                    (lon >= 267 and lon <  273 and lat < 15 ) or
                    (lon >= 261 and lon <  267 and lat < 17 ) or
                    (lon >= 180 and lon <  261 and lat >  0)
                    )

        self.isepacTC=( (lon >= 276 and lon <= 282 and lat <  9 ) or
                    (lon >= 273 and lon <  276 and lat < 12 ) or
                    (lon >= 267 and lon <  273 and lat < 15 ) or
                    (lon >= 261 and lon <  267 and lat < 17 ) or
                    (lon >= 160 and lon <  261 and lat >  0)
                    )
        
        self.iscpac=( (lon >= 180 and lon <= 220) and lat >=  0 )
        

        self.islant=( (lon >= 276 and lon <= 282 and lat >=  9 ) or
                    (lon >= 273 and lon <  276 and lat >= 12 ) or
                    (lon >= 267 and lon <  273 and lat >= 15 ) or
                    (lon >= 261 and lon <  267 and lat >= 17 ) or
                    (lon >= 276 and lon <= 360 and lat >   0 ) 
                    )
        
        self.iswpac=( (lon >= 100 and lon <= 180) and lat >=  0 )
        
        self.iswpacTC=( (lon >= 100 and lon <= 200) and lat >=  0 )
        
        self.isnio=( (lon >= 40 and lon <= 100) and lat >=  0 )
        
        self.isshem=( (lon >= 35 and lon <= (360-150)) and lat <  0 )


        self.llbasin=None
        
        if(self.isepac):  self.llbasin='epac'
        if(self.iscpac):  self.llbasin='cpac'
        if(self.iswpac):  self.llbasin='wpac'
        if(self.islant):  self.llbasin='lant'
        if(self.isnio):   self.llbasin='nio'
        if(self.isshem):  self.llbasin='shem'

        if(self.basin == None):

            if(self.llbasin == None):
                print "EEE in tc2.TcBAsin.getBasinFromLatLon: problem lat/lon: ",lat,lon
                sys.exit()

            self.getBasinPareaFromBasin(self.llbasin)


    def isLLin(self,lat,lon,doTC=0):

        self.getBasinFromLatLon(lat,lon)
        
        if(self.basin == 'epac'):
            if(doTC and hasattr(self,'isepacTC')): return(self.isepacTC)
            return(self.isepac)

        elif(self.basin == 'lant'):
            return(self.islant)

        elif(self.basin == 'wpac'):
            if(doTC and hasattr(self,'iswpacTC')): return(self.iswpacTC)
            return(self.iswpac)

        elif(self.basin == 'nio'):
            return(self.isnio)

        elif(self.basin == 'shem'):
            return(self.isshem)

    def isLatTropical(self,lat,dtg=None,override=0):
        
        if(override):
            rc=1
            return(rc)
        
        rc=0
        tlat0=self.tropicalLats[0]
        tlat1=self.tropicalLats[1]
        
        if(dtg != None):
            
            if(self.isMidSeason(self.basin,dtg) and hasattr(self,'tropicalLatsMidSeason')):
                tlat0=self.tropicalLatsMidSeason[0]
                tlat1=self.tropicalLatsMidSeason[1]
                

        if(lat >= tlat0 and lat <= tlat1): rc=1
        return(rc)


        
class MDpaths(MFbase):
    
    minCuroffset=6.5
    
    # -- CPHC can be very slow to update...
    #
    minCuroffsetCP=12.0
    
    def __init__(self,years=None,verb=1):

        from w2local import W2
        w2=W2()

        if(years == None):
            self.initCurState()
            (shemoverlatp,curyear,curyearp1)=CurShemOverlap(self.curdtg)
            if(curyearp1 != curyear):
                years=[curyear,curyearp1]
            else:
                years=[curyear]
                
        elif(not(type(years) is ListType)): years=[years]

        def fillprops(paths,hash,tag='aN',verb=0):
            
            for path in paths:
                (b2id,snum,stm1id,stm2id)=getB2idSnumFromPath(path)
                if(snum > 0):
                    siz=MF.GetPathSiz(path)
                    (gtimei,gdtimei)=MF.PathModifyTimei(path)
                    #(gtimei,gdtimei)=MF.PathCreateTimei(path)
                    prop=(stm1id,gtimei,siz)
                    if(verb): print '%s %s %10d %s'%(tag,stm1id,siz,gdtimei),gtimei
                    hash[path]=prop

            return(hash)
            
        
        abdirN=w2.TcAdecksNhcDir
        bbdirN=w2.TcBdecksNhcDir

        abdirJ=w2.TcAdecksJtwcDir
        bbdirJ=w2.TcBdecksJtwcDir

        self.curaNs={}
        self.curbNs={}
        self.curaJs={}
        self.curbJs={}

        aNs=[]
        aJs=[]
        
        bNs=[]
        bJs=[]
        
        for year in years:
            
            adsdirN="%s/%s"%(abdirN,year)
            bdsdirN="%s/%s"%(bbdirN,year)
            
            adsdirJ="%s/%s"%(abdirJ,year)
            bdsdirJ="%s/%s"%(bbdirJ,year)
            # -- 2016061700 -- for nhc always check the gzip files
            #
            aNs=aNs+glob.glob("%s/a????%s.dat.gz"%(adsdirN,year))
            aJs=aJs+glob.glob("%s/a????%s.dat"%(adsdirJ,year))

            bNs=bNs+glob.glob("%s/b????%s.dat"%(bdsdirN,year))
            bJs=bJs+glob.glob("%s/b????%s.dat"%(bdsdirJ,year))

        #print adsdirN,adsdirJ,aNs,aJs

        self.curaNs=fillprops(aNs,self.curaNs,'aN')
        self.curaJs=fillprops(aJs,self.curaJs,'aJ')
        
        self.curbNs=fillprops(bNs,self.curbNs,'bN')
        self.curbJs=fillprops(bJs,self.curbJs,'bJ')
        

    def getCurStmids(self,abD,year,override=0,overrideNhc=0,verb=0):


        def comp(cur,old,verb=0):

            hash={}
            for k in cur.keys():
                (stm1id,gtimei,siz)=cur[k]
                try:
                    (ostm1id,ogtimei,osiz)=old[k]
                except:
                    (ostm1id,ogtimei,osiz)=(None,None,None)

                toff=soff=ctoff=None
                
                ctimei=MF.getCurTimei()
                ctoff=MF.DeltaTimei(ctimei,gtimei)
            
                if(ogtimei != None):
                    
                    toff=MF.DeltaTimei(gtimei,ogtimei)
                    soff=siz-osiz
                    
                    if(verb):
                        print 'cccccc ',k,gtimei
                        print 'oooooo ',k,ogtimei
                        print 'dddddd ',k,stm1id,toff,soff,ctoff
                        
                # -- new storm
                #
                else:
                    toff=0.0
                    soff=0
                    
                hash[k]=(stm1id,toff,soff,ctoff)
                
            return(hash)

        def isAdeckDiffNhc(stm1id,toff,soff,ctoff,override):

            rc=0
            if(toff == None or
               # -- nhc handles cphc decks differently always do...
               (toff != 0.0 and soff != 0) or
               override):
                rc=1
                
            # failsafe if off old update
            #
            if(ctoff < self.minCuroffset): rc=1

            # failsafe if off old update for CPCH
            #
            if(stm1id[2] == 'C' and ctoff < self.minCuroffsetCP): rc=1
            return(rc)
            
                
        def isBdeckDiffNhc(stm1id,toff,soff,ctoff,override):
            rc=0
            if(toff == None or
               (toff != 0.0 and soff != 0) or
               # -- nhc handles cphc decks differently always do...
#              stm1id[2] == 'C' or
               override):
                rc=1
                return(rc)

            # failsafe if off old update
            #
            if(ctoff < self.minCuroffset): rc=1

            # failsafe if off old update for CPCH
            #
            if(stm1id[2] == 'C' and ctoff < self.minCuroffsetCP): rc=1
            
            return(rc)
            
                
        def isAdeckDiffJtwc(toff,soff,ctoff,override):
            rc=0
            if(toff == None or
               (toff != 0.0 or soff != 0) or
               override):
                rc=1
            return(rc)
            
                
        def isBdeckDiffJtwc(toff,soff,ctoff,override):
            rc=0
            if(toff == None or
               (toff != 0.0 or soff != 0) or
               override):
                rc=1
                return(rc)
            
            # failsafe if off old update, need comp to toff for smarter check
            #
            if(ctoff < self.minCuroffset): rc=1
            
            return(rc)
        
                

        ctoffs={}
        curstm1ids=[]

        compaNs=comp(self.curaNs,abD.curaNs)
        compaJs=comp(self.curaJs,abD.curaJs)
        compbNs=comp(self.curbNs,abD.curbNs)
        compbJs=comp(self.curbJs,abD.curbJs)


        aNkk=compaNs.keys()
        bNkk=compbNs.keys()
        aJkk=compaJs.keys()
        bJkk=compbJs.keys()
        
        aNkk.sort()
        bNkk.sort()
        aJkk.sort()
        bJkk.sort()
        
        for k in aNkk:
            (stm1id,toff,soff,ctoff)=compaNs[k]
            if(isAdeckDiffNhc(stm1id,toff,soff,ctoff,overrideNhc)):
                curstm1ids.append(stm1id)
                ctoffs[stm1id]=ctoff
                if(verb): print 'HHHHHHHHHHHHHAAAAANHC ',stm1id
            if(verb): print 'aaaaNNNN: ',stm1id,(toff,soff,ctoff)
        
        for k in aJkk:
            (stm1id,toff,soff,ctoff)=compaJs[k]
            if(isAdeckDiffJtwc(toff,soff,ctoff,override)):
                curstm1ids.append(stm1id)
                ctoffs[stm1id]=ctoff
                if(verb): print 'HHHHHHHHHHHHHAAAAAJTWC ',stm1id
            if(verb):print 'aaaaJJJJ: ',stm1id,(toff,soff,ctoff)
        
        for k in bNkk:
            (stm1id,toff,soff,ctoff)=compbNs[k]
            if(isBdeckDiffNhc(stm1id,toff,soff,ctoff,overrideNhc)):
                curstm1ids.append(stm1id)
                ctoffs[stm1id]=ctoff
                if(verb): print 'HHHHHHHHHHHHHBBBBBNHC ',stm1id
            if(verb): print 'bbbbNNNN: ',stm1id,(toff,soff,ctoff)
        
        for k in bJkk:
            (stm1id,toff,soff,ctoff)=compbJs[k]
            if(isBdeckDiffJtwc(toff,soff,ctoff,override)):
                curstm1ids.append(stm1id)
                ctoffs[stm1id]=ctoff
                if(verb): print 'HHHHHHHHHHHHHBBBBBJTWC ',stm1id
            if(verb): print 'bbbbJJJJ: ',stm1id,(toff,soff,ctoff)

        curstm1ids=mf.uniq(curstm1ids)

        icurstm1ids=sortStmidsMD2update(curstm1ids)
        
        # check if weird number storm (e.g., 77) got in the decks
        #
        curstm1ids=[]
        for icurstm in icurstm1ids:
            if(IsNN(icurstm) or Is9X(icurstm)):
                curstm1ids.append(icurstm)
        
        if(verb):
            for curstm1id in curstm1ids:
                print 'CCC-MDpaths ',curstm1id,' ctoff: ',ctoffs[curstm1id]
                
        # -- check if curstm1ids are in year (> 1 jul go to next year shem season)
        #
        
        ycurstm1ids=[]
        
        for curstm1id in curstm1ids:
            stmyear=curstm1id.split('.')[-1]
            if(stmyear == year): ycurstm1ids.append(curstm1id)
            
        return(ycurstm1ids,ctoffs)

        
            

class MD2trk(MDdataset):

    def __init__(self,smD,DSs,dds=None,verb=0,dobt=1,doPutDSs=1):

        self.tD=TcData(DSs=DSs)

        self.smD=smD
        self.DSs=DSs
        self.stm1id=smD.stm1id
        self.stm2id=smD.stm2id
        self.doPutDSs=doPutDSs
        if(dds == None):
            self.dds=self.tD.getDSsFullStm(smD.stm1id,dobt=dobt,doprint=verb)
        else:
            self.dds=dds

        if(self.dds == None):
            self.doPutDSs=0
            self.status=-999
        else:
            (self.trk,self.dtgs)=self.dds.getMDotrk()
            self.status=1

        
    def anlMDtrk(self,stmD=None,verb=1,comp9XCC=1,compCC=0):

        try:
            (ltln,latmn,latmx,lonmn,lonmx,latb,lonb)=self.getlatlon()
        except:
            print 'EEE(tcCL.MD2trk.anlMDtrk -- no lat/lon for: ',self.stm1id,' better figure this out -- no 9x?'
            return(0)
        
        (gendtg,gendtgs,genstdd,time2gen)=self.getgenesis()
        sname=self.getname()
        (vmax,ace,stcd)=self.getvmax()
        (nRI,nED,nRW,dRI,dED,dRW)=self.getRI()
        (tclife,stclife,stmlife)=self.gettclife()
        syear=self.stm1id.split('.')[1]

        # -- use storm class object for name if given
        #
        if(stmD != None):
            rc=stmD.getStmData(self.smD.stm2id)
            if(rc != None): sname=rc[0]


        # -- if a warning is put, set stmlife to tcgen -- for 9X with warnings in the adecks
        #
        if(time2gen > 0 and Is9X(self.stm1id)):
            stmlife=time2gen/24.0


        if(verb):
            print 'FFFFFFFFFF(stm1|2id0:  ',self.smD.stm2id,self.smD.stm1id
            print 'FFFFFFFFFF(tclife):    ',tclife
            print 'FFFFFFFFFF(stclife):   ',stclife
            print 'FFFFFFFFFF(stmlife):   ',stmlife

            print 'FFFFFFFFFF(ace):       ',ace
            print 'FFFFFFFFFF(stcd):      ',stcd

            print 'FFFFFFFFFF(latb):      ',latb
            print 'FFFFFFFFFF(lonb):      ',lonb
            
            print 'FFFFFFFFFF(latmn):     ',latmn
            print 'FFFFFFFFFF(latmx):     ',latmx
            print 'FFFFFFFFFF(lonmn):     ',lonmn
            print 'FFFFFFFFFF(lonmx):     ',lonmx

            print 'FFFFFFFFFF(gendtg):    ',gendtg
            print 'FFFFFFFFFF(gendtgs):   ',gendtgs
            print 'FFFFFFFFFF(genstdd):   ',genstdd
            print 'FFFFFFFFFF(time2gen):  ',time2gen
            print 'FFFFFFFFFF(sname):     ',sname
            print 'FFFFFFFFFF(vmax):      ',vmax

            print 'FFFFFFFF(nRI):         ',nRI
            print 'FFFFFFFF(nED):         ',nED
            print 'FFFFFFFF(nRW):         ',nRW

            print 'FFFFFFFF(dRI):         ',dRI
            print 'FFFFFFFF(dED):         ',dED
            print 'FFFFFFFF(dRW):         ',dRW


        # -- decorate stm Dataset
        #
        
        self.smD.gendtg=gendtg
        self.smD.gendtgs=gendtgs
        self.smD.genstdd=genstdd
        self.smD.time2gen=time2gen

        self.smD.sname=sname
        self.smD.vmax=vmax

        self.smD.ace=ace
        self.smD.stcd=stcd

        self.smD.tclife=tclife
        self.smD.stclife=stclife
        self.smD.stmlife=stmlife

        self.smD.latb=latb
        self.smD.lonb=lonb
        
        self.smD.latmn=latmn
        self.smD.lonmn=lonmn
        
        self.smD.latmx=latmx
        self.smD.lonmx=lonmx
    
        self.smD.nRI=nRI
        self.smD.nED=nED
        self.smD.nRW=nRW
        self.smD.dRI=dRI
        self.smD.dED=dED
        self.smD.dRW=dRW

        if(comp9XCC):
            
            # -- find 9X storm
            #
            stmid=self.smD.stm1id
            if(IsNN(stmid)):
                dds9x=self.tD.get9xDSs(self.smD,stmid,verb=0)
                if(dds9x != None):
                    # -- decorate the NN smD
                    self.smD.stmid9x=dds9x.stmid9x

                    # -- decorate the 9x smD and save
                    dds9x.stmidNN=stmid
                    if(self.doPutDSs): self.DSs.putDataSet(dds9x,key=dds9x.ostm2id9x,verb=verb)


            if(Is9X(stmid) and compCC):
                ddsCC=self.tD.getCCDSs(self.smD,stmid,verb=1)
                if(ddsCC != None):
                    # -- decorate the NN smD
                    self.smD.stmidCC=ddsCC.stmidCCs


            if(IsNN(stmid) and compCC):
                ddsCC=self.tD.getCCDSs(self.smD,stmid,verb=1)
                if(ddsCC != None):
                    # -- decorate the NN smD
                    self.smD.stmidCC=ddsCC.stmidCC



    def loadMDdtg(self):

        for dtg in self.smD.gendtgs:

            dds=self.DSs.getDataSet(key=dtg)
            if(dds == None): dds=MDdtgs(dtg)

            if(not(hasattr(dds,'genstmids'))):   dds.genstmids=[]
            dds.genstmids.append(self.smD.stm1id)
            dds.genstmids=MF.uniq(dds.genstmids)

            if(self.doPutDSs): self.DSs.putDataSet(dds,key=dtg)

        
        
        
    def getRI(self,dvmaxRI=30,dvmaxED=50,dvmaxRD=-30):

        dRI=dED=-999
        dRW=999
        nRI=0
        nED=0
        nRW=0
        
        for dtg in self.dtgs:
            dtgm24=mf.dtginc(dtg,-24)
            if(dtgm24 in self.dtgs):
                ttm24=self.trk[dtgm24]
                tt=self.trk[dtg]
                vmaxm24=ttm24.vmax
                vmax=tt.vmax
                if(vmax != None):
                    dvmax=vmax-vmaxm24
                else:
                    continue
                if(dvmax >= dvmaxRI):
                    nRI=nRI+1
                    if(dvmax > dRI and dvmax < dvmaxED): dRI=dvmax
                
                if(dvmax >= dvmaxED):
                    nED=nED+1
                    if(dvmax > dED): dED=dvmax

                if(dvmax <= dvmaxRD):
                    nRW=nRW+1
                    if(dvmax < dRW): dRW=dvmax
                

                

        return(nRI,nED,nRW,dRI,dED,dRW)


        


    def getvmax(self,ddtg=6):
        """assume ddtg=6h"""
        vmax=-999
        ace=0.0
        stcd=0.0
        n=0
        ns=0
        
        for dtg in self.dtgs:
            tt=self.trk[dtg]
            svmax=tt.vmax
            if(svmax > vmax and svmax != self.undef): vmax=tt.vmax

            tace=aceTC(svmax)
            if(tace > 0.0):
                ace=ace+tace*ddtg
                ns=ns+1

            stcd=stcd+scaledTC(svmax)
            n=n+1

        stcd=stcd*0.25

        if(ns > 0):
            ace=ace/(24.0*tymin*tymin)

        return(vmax,ace,stcd)




    def getname(self):

        sname='---------'
        snames={}
        for dtg in self.dtgs:
            tt=self.trk[dtg]
            if(tt.sname[0:5] != 'NONAM' and tt.sname[0:5] != 'INVES' and tt.sname != ''):
                MF.appendDictList(snames,tt.sname,tt.sname)

        nmax=-999
        for k in snames.keys():
            n=len(snames[k])
            if(n > nmax):
                nmax=n
                sname=k

        return(sname)

        
    def getgenesis(self,dtgm=-18,dtgp=+12,vmaxTD=25.0,vmaxMin=10.0,verb=0):

        time2gen=-999.
        gendtg=gendtgWN=gendtgBT=None
        stdd=0.0
        
        gendtgs=[]
        genstd=None

        minvmax=1e20
        maxvmax=-1e20
        
        for dtg in self.dtgs:
            tt=self.trk[dtg]
            if(tt.wncode.lower() == 'wn' and gendtgWN == None): gendtgWN=dtg

        # -- if gendtg = None; then no warnings!  use when became tc...
        #
        tcCodeWind=0
        for dtg in self.dtgs:
            tt=self.trk[dtg]
            istc=IsTc(tt.tccode)
            if(tt.tccode == 'TW'):tcCodeWind=1
            if(istc >= 1 and gendtgBT == None): gendtgBT=dtg

        if(gendtgWN != None):
            if(tcCodeWind >= 0):  gendtg=gendtgWN
            else:                 gendtg=gendtgBT
            
        if(gendtg == None and gendtgBT != None): gendtg=gendtgBT
        
        if(gendtg != None):

            time2gen=mf.dtgdiff(self.dtgs[0],gendtg)
            
            bdtg=mf.dtginc(gendtg,dtgm)
            edtg=mf.dtginc(gendtg,dtgp)
            gendtgs=mf.dtgrange(bdtg,edtg)


            stddtime=0.0
            ngd=len(gendtgs)
            for n in range(1,ngd):
                dtgm1=gendtgs[n-1]
                dtg0=gendtgs[n]
                
                if(dtg0 in self.dtgs and dtgm1 in self.dtgs):

                    dtau=mf.dtgdiff(dtgm1,dtg0)
                    ttm1=self.trk[dtgm1]
                    tt0=self.trk[dtg0]
                    
                    vmaxm1=ttm1.vmax
                    vmaxm0=tt0.vmax
                    if(vmaxm1 < 0): vmaxm1=vmaxMin
                    if(vmaxm0 < 0): vmaxm0=vmaxMin

                    if(vmaxm1 > maxvmax): maxvmax=vmaxm1
                    if(vmaxm1 < minvmax): minvmax=vmaxm1
                    if(vmaxm0 > maxvmax): maxvmax=vmaxm0
                    if(vmaxm0 < minvmax): minvmax=vmaxm0
                    
                    stdd=stdd+(((vmaxm1+vmaxm0)*0.5)/vmaxTD)*dtau
                    stddtime=stddtime+dtau

                    if(verb): print 'ggggggggggg ',dtau,dtg0,dtgm1,vmaxm1,vmaxm0,stdd,stddtime

            if(stddtime > 0.0):

                stdd=stdd/24.0
                if(verb): print 'ggggggggggg final stdd: ',stdd


        genstdd=stdd

        if(verb):
            print 'ggggggg ',gendtg
            print 'ggggggg ',gendtgs
            print 'ggggggg ',genstdd
            print 'ggggggg ',time2gen

        return(gendtg,gendtgs,genstdd,time2gen)

        
    
    def getlatlon(self):

        latb=0.0
        lonb=0.0
        
        latmn=999
        latmx=-999
        lonmn=999
        lonmx=-999

        latlon={}
        n=0
            
        for dtg in self.dtgs:
            tt=self.trk[dtg]

            tlat=tt.rlat
            if(n==0):  tlonPri=tt.rlon
            tlon=tt.rlon
            
            # -- cross prime meridion
            if(tlon < primeMeridianChk and tlonPri > primeMeridianChk): tlon=tlon+360.0
            
            if(tlat > latmx): latmx=tlat
            if(tlon > lonmx): lonmx=tlon
            if(tlat < latmn): latmn=tlat
            if(tlon < lonmn): lonmn=tlon
            n=n+1
            latb=latb+tlat
            lonb=lonb+tlon
            latlon[dtg]=(tlat,tlon)
            tlonPri=tlon

            

        if(n>0):
            latb=latb/n
            lonb=lonb/n

        ndtgs=len(self.dtgs)
        for n in range(0,ndtgs):
            dtg=self.dtgs[n]
            tt=self.trk[dtg]
            
        return(latlon,latmn,latmx,lonmn,lonmx,latb,lonb)


    def gettclife(self):

        tclife=0
        stclife=0
        stmlife=0
        
        ndtgs=len(self.dtgs)

        if(ndtgs == 0):
            return(tclife,stclife,stmlife)
            
        for n in range(1,ndtgs):
            tt=self.trk[self.dtgs[n]]
            dtau=mf.dtgdiff(self.dtgs[n-1],self.dtgs[n])
            stmlife=stmlife+dtau
            if(IsTc(tt.tccode) == 1):
                tclife=tclife+dtau
            if(IsTc(tt.tccode) == 2):
                stclife=stclife+dtau
            
        tclife=tclife/24.0
        stclife=stclife/24.0
        stmlife=stmlife/24.0

        return(tclife,stclife,stmlife)
            


class TcAidTrkOld(MFbase):


    def __init__(self,model,dtg,
                 verb=0):


        self.model=model
        self.dtg=dtg
        self.verb=verb
        
        self.initAD()

        

    def initAD(self,verb=1):

        import AD

        apath="%s/%s/w2flds/tctrk.atcf.%s.%s.txt"%(TcAdecksEsrlDir,self.dtg[0:4],self.dtg,self.model)
        spath="%s/%s/w2flds/tctrk.sink.%s.%s.txt"%(TcAdecksEsrlDir,self.dtg[0:4],self.dtg,self.model)

        self.aid=self.model

        self.aD=AD.Adeck(apath,verb=verb)
        self.apath=apath
        
        # -- since we're only doing one aid, pull first aid in aids
        #
        if(len(self.aD.aids) > 0): self.aidname=self.aD.aids[0]

        self.aDS=AD.AdeckSink(spath,verb=self.verb)
        if(self.verb or verb):
            print 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA apath: ',apath,' self.aid: ',self.aid,' model: ',self.model
            print 'SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS spath: ',spath

        self.adstm2ids=self.aD.stm2ids


    def initTC(self,dtg):
        
        if(not(hasattr(self,'tD'))): self.tD=TcData()
        self.stmids=self.tD.getStmidDtg(dtg)
        self.stmids.sort()


    def lsTC(self):

        print "Dtg: %s"%(self.dtg)
        for stmid in self.stmids:
            (lat,lon,vmax,pmin)=self.tD.getBtLatLonVmaxPmin(stmid)
            (clat,clon)=self.tD.rlatLon2clatLon(lat,lon)
            print "%s %s %s %03d %4.0f"%(stmid,clat,clon,int(vmax),float(pmin))

        

    def setTCtracker(self,stmid,maxtau=168,quiet=0):

        # -- first source is adecks from TMtrker from w2flds...
        #
        if(self.aD != None):
            self.stmid=stmid
            self.getAidtrk(self.dtg,self.stmid)
            self.getAidcards(self.dtg,self.stmid)
            ntaus1=0
            lasttau1=0
            if(self.aidtaus != None):
                aidtrks1=self.aidtrk
                aidtaus1=self.aidtaus
                ntaus1=len(self.aidtaus)
                lasttau1=aidtaus1[-1]


        # -- second source is from external adecks in dss form ('ncep','jtwc','ecmwf'), adeck sources and aid set in M2.py
        #
        self.getAidtrkFromAdss(self.dtg,self.stmid)
        ntaus2=0
        lasttau2=0
        adecksources2=[]
        if(self.ADaidtaus != None):
            aidtrks2=self.ADaidtrk
            aidtaus2=self.ADaidtaus
            ntaus2=len(self.ADaidtaus)
            lasttau2=aidtaus2[-1]
            adecksources2=self.adecksources

        # -- third and last source is local adecks using my old tracker in dss form ('local')
        #
        adecksources=['local']
        adecksources3=adecksources
        self.getAidtrkFromAdss(self.dtg,self.stmid,sources=adecksources,adeckaid=self.model)
        ntaus3=0
        lasttau3=0
        aidtrks3=[]
        aidtaus3=[]
        if(self.ADaidtaus != None):
            aidtrks3=self.ADaidtrk
            aidtaus3=self.ADaidtaus
            ntaus3=len(self.ADaidtaus)
            lasttau3=aidtaus3[-1]
            adecksources3=adecksources

        # -- now select best source
        #

        if(self.verb):
            print '11111111 ',ntaus1,lasttau1
            print '22222222 ',ntaus2,lasttau2,adecksources2
            print '33333333 ',ntaus3,lasttau3,adecksources3
            
        finalsource=3
        
        # -- limit how much more tau the local tracker has before beating the tmtrk(w2flds)
        #
        dtau3v1=12
        dtau3v2=12
        if( (lasttau1 >= lasttau2) and (lasttau1 >= lasttau3-dtau3v1) and ntaus1 > 0):
            finalsource=1
        if( (lasttau2 > lasttau1) and (lasttau2 > lasttau3-dtau3v2) and ntaus2 > 0):
            finalsource=2


        # -- bail point -- no tracker
        #
        if(ntaus1 == 0 and ntaus2 == 0 and ntaus3 == 0): 
            print 'WWW(%s)'%(self.basename),'no tracker taus for dtg: ',self.dtg,' model: ',self.model,' stmid: ',self.stmid,' bailing...'
            return(0)
            

        if(self.verb): print 'fffffffffffff ',finalsource,self.model,self.stmid

        if(finalsource == 1):
            self.aidtrk=aidtrks1
            self.aidtaus=aidtaus1
            self.aidsource='w2flds'

        if(finalsource == 2):
            self.aidtrk=aidtrks2
            self.aidtaus=aidtaus2
            self.aidsource='external'

        if(finalsource == 3):
            self.aidtrk=aidtrks3
            self.aidtaus=aidtaus3
            self.aidsource='local'

        # -- bail point 2 -- no tracker taus for aid
        #
        if(len(self.aidtaus) == 0):
            print 'WWW(%s)'%(self.basename),'no final  tracker taus for dtg: ',self.dtg,' model: ',self.model,' stmid: ',self.stmid,' bailing...'
            return(0)
            

            
        
        self.diagpath="%s/diag.%s.%s.txt"%(self.pltdir,self.stmid,self.model)

        self.pyppath="%s/diag.%s.pyp"%(self.pltdir,self.stmid)
        self.pyppathHtml="%s/html.%s.pyp"%(self.pltdir,self.stmid)
        self.pyppathData="%s/data.%s.pyp"%(self.pltdir,self.stmid)
        self.diagpathALL="%s/diag.all.%s.%s.txt"%(self.pltdir,self.stmid,self.model)
        self.diagpathWebALL="%s/diag.all.%s.%s.txt"%(self.webdiagdir,self.stmid,self.model)
        
        self.pyppathDataALL="%s/data.all.%s.pyp"%(self.pltdir,self.stmid)
        if(self.doDiagOnly):
            self.diagpath=self.diagpathALL
            self.pyppathData=self.pyppathDataALL

        if(self.aidtrk != None and not(quiet)):
            print 'TCTCTCTCTCTCTCTCTCTCTCTCTCTCTCTCTCTCTCTCTC got tracker from aidsource: %-10s'%(self.aidsource),' model: %-6s'%(self.model),' stmid: ',self.stmid,' ntaus: %3d'%(len(self.aidtaus)),' lasttau: %3d'%(self.aidtaus[-1])

        # -- limit taus
        ataus=[]
        if(maxtau != None):
            for atau in self.aidtaus:
                if(atau in self.targetTaus):
                    ataus.append(atau)
            self.aidtaus=ataus
            

        return(1)


        
    def getAidtrkFromAdss(self,dtg,stmid,
                          sources=None,adeckaid=None,
                          set2AD=1,forceAD=0):
        """
        get aid track for adeck DSs; handles multiply sources
        """

        if(sources != None):
            sources=sources.split(',')
        if(adeckaid == None):
            self.ADaid=self.adeckaid
        else:
            self.ADaid=adeckaid

        self.adecksources=sources

        aDSs=AD.getAdssFromDss(sources,stmid,self.ADaid,verb=self.verb)
        kk=aDSs.keys()

        aTs={}
        for k in kk:
            aD=aDSs[k]

            try:
                aTs[k]=aD.ats[dtg]
            except:
                aTs[k]={}


        # -- get track with most taus from multiply sources
        #
        longest=-999
        longestK=None

        for k in kk:
            sizK=len(aTs[k])
            if( sizK > longest):
                longest=sizK
                longestK=k

        if(longest > 0):
            self.ADaidtrk=aTs[longestK]
            self.ADaidtaus=self.ADaidtrk.keys()
            self.ADaidtaus.sort()
        else:
            self.ADaidtrk=None
            self.ADaidtaus=None
            

        if(self.verb and self.ADaidtaus != None):
            if(len(self.ADaidtaus) > 0):
                print 'ADaidtrk:  '
                for tau in self.ADaidtaus:
                    tt=list(self.ADaidtrk[tau])
                    print "%03d  %5.1f  %6.1f  %4.1f  %6.1f"%(int(tau),tt[0],tt[1],tt[2],tt[3])


    
    def getAidcards(self,dtg,stmid):

        try:
            self.aidcards=self.aD.GetAidCards(self.aid,stmid)[dtg]

        except:
            self.aidcards=[]
            if(self.verb): print 'WWW(%s) no adeck cards    for aid: %s stmid: %s'%(self.basename,self.model,stmid)
            return




class TcAidTrk(MFbase):


    def __init__(self,dtg,aids=None,
                 verb=1):


        self.dtg=dtg
        self.verb=verb
        
        self.initTC()

        self.ADaids={}
        self.ADaidtrk={}
        self.ADaidtaus={}


    def getATs(self):
        
        self.ADaids={}
        self.ADaidtrk={}
        self.ADaidtaus={}

        for stmid in self.stmids:
            ATs=self.getAidtrkFromAdss(self.dtg,stmid,adeckaids=aids)

        self.ATs=ATs
            
        


    def initTC(self):
        
        if(not(hasattr(self,'tD'))): self.tD=TcData(dtgopt=self.dtg)
        (self.stmids,self.btcs)=self.tD.getDtg(self.dtg)



    def lsTC(self):

        print "Dtg: %s"%(self.dtg)
        for stmid in self.stmids:
            rc=self.btcs[stmid]
            (lat,lon,vmax,pmin)=rc[0:4]
            if(pmin == None): pmin=-999
            (clat,clon)=Rlatlon2Clatlon(lat,lon)
            print "%s %s %s %03d %4.0f"%(stmid,clat,clon,int(vmax),float(pmin))



    def getAidtrksFromAdss(self,dtg,stmid,
                          sources=None,
                          adeckaids=None,
                          set2AD=1,forceAD=0):
        """
        get aid track for adeck DSs; handles multiply sources == returns hash
        """

        if(sources == None):
            # -- look in the operational adecks...
            #
            if(IsJtwcBasin(stmid)): sources=['jtwc']
            elif(IsNhcBasin(stmid)): sources=['nhc']
            else: sources=['jtwc','nhc']

            
        if(adeckaids == None):
            # -- set operational aids
            #
            if(IsJtwcBasin(stmid)): adeckaids=['jtwc','jtwi']
            elif(IsNhcBasin(stmid)): adeckaids=['ofcl','ofci']
            else: adeckaids=['jtwc','jtwi','ofcl','ofci']

        self.aids=adeckaids

        self.adecksources=sources

        for ADaid in self.aids:
            aDSs=AD.getAdssFromDss(sources,stmid,ADaid,verb=self.verb)
            asources=aDSs.keys()

            # -- kk are the source keys..
            aTs={}
            for source in asources:
                aD=aDSs[source]

                try:
                    aTs[source]=aD.ats[dtg]
                except:
                    aTs[source]={}

            if(len(aTs[source]) > 0):
                
                MF.loadDictList(self.ADaids,stmid,ADaid)
                self.ADaidtrk[stmid,ADaid]=aTs[source]
                self.ADaidtaus[stmid,ADaid]=self.ADaidtrk[stmid,ADaid].keys()
                self.ADaidtaus[stmid,ADaid].sort()


                if(self.verb and self.ADaidtaus != None):
                    if(len(self.ADaidtaus[stmid,ADaid]) > 0):
                        print 'ADaidtrk:  '
                        for tau in self.ADaidtaus[stmid,ADaid]:
                            tt=list(self.ADaidtrk[stmid,ADaid][tau])
                            print "aid: %s  %03d  %5.1f  %6.1f  %4.1f  %6.1f"%(ADaid,int(tau),tt[0],tt[1],tt[2],tt[3])



    def getAidtrkFromAdss(self,dtg,stmid,
                          sources=None,adeckaid=None,
                          set2AD=1,forceAD=0):
        """
        get aid track for adeck DSs; handles multiply sources
        """

        if(sources == None):
            sources=self.adecksource.split(',')
        if(adeckaid == None):
            self.ADaid=self.adeckaid
        else:
            self.ADaid=adeckaid

        self.adecksources=sources

        aDSs=AD.getAdssFromDss(sources,stmid,self.ADaid,verb=self.verb)
        kk=aDSs.keys()

        aTs={}
        for k in kk:
            aD=aDSs[k]

            try:
                aTs[k]=aD.ats[dtg]
            except:
                aTs[k]={}


        # -- get track with most taus from multiply sources
        #
        longest=-999
        longestK=None

        for k in kk:
            sizK=len(aTs[k])
            if( sizK > longest):
                longest=sizK
                longestK=k

        if(longest > 0):
            self.ADaidtrk=aTs[longestK]
            self.ADaidtaus=self.ADaidtrk.keys()
            self.ADaidtaus.sort()
        else:
            self.ADaidtrk=None
            self.ADaidtaus=None
            

        if(self.verb and self.ADaidtaus != None):
            if(len(self.ADaidtaus) > 0):
                print 'ADaidtrk:  '
                for tau in self.ADaidtaus:
                    tt=list(self.ADaidtrk[tau])
                    print "%03d  %5.1f  %6.1f  %4.1f  %6.1f"%(int(tau),tt[0],tt[1],tt[2],tt[3])


    
        

    def setTCtracker(self,stmid,maxtau=168,quiet=0):

        # -- first source is adecks from TMtrker from w2flds...
        #
        if(self.aD != None):
            self.stmid=stmid
            self.getAidtrk(self.dtg,self.stmid)
            self.getAidcards(self.dtg,self.stmid)
            ntaus1=0
            lasttau1=0
            if(self.aidtaus != None):
                aidtrks1=self.aidtrk
                aidtaus1=self.aidtaus
                ntaus1=len(self.aidtaus)
                lasttau1=aidtaus1[-1]


        # -- second source is from external adecks in dss form ('ncep','jtwc','ecmwf'), adeck sources and aid set in M2.py
        #
        self.getAidtrkFromAdss(self.dtg,self.stmid)
        ntaus2=0
        lasttau2=0
        adecksources2=[]
        if(self.ADaidtaus != None):
            aidtrks2=self.ADaidtrk
            aidtaus2=self.ADaidtaus
            ntaus2=len(self.ADaidtaus)
            lasttau2=aidtaus2[-1]
            adecksources2=self.adecksources

        # -- third and last source is local adecks using my old tracker in dss form ('local')
        #
        adecksources=['local']
        adecksources3=adecksources
        self.getAidtrkFromAdss(self.dtg,self.stmid,sources=adecksources,adeckaid=self.model)
        ntaus3=0
        lasttau3=0
        aidtrks3=[]
        aidtaus3=[]
        if(self.ADaidtaus != None):
            aidtrks3=self.ADaidtrk
            aidtaus3=self.ADaidtaus
            ntaus3=len(self.ADaidtaus)
            lasttau3=aidtaus3[-1]
            adecksources3=adecksources

        # -- now select best source
        #

        if(self.verb):
            print '11111111 ',ntaus1,lasttau1
            print '22222222 ',ntaus2,lasttau2,adecksources2
            print '33333333 ',ntaus3,lasttau3,adecksources3
            
        finalsource=3
        
        # -- limit how much more tau the local tracker has before beating the tmtrk(w2flds)
        #
        dtau3v1=12
        dtau3v2=12
        if( (lasttau1 >= lasttau2) and (lasttau1 >= lasttau3-dtau3v1) and ntaus1 > 0):
            finalsource=1
        if( (lasttau2 > lasttau1) and (lasttau2 > lasttau3-dtau3v2) and ntaus2 > 0):
            finalsource=2


        # -- bail point -- no tracker
        #
        if(ntaus1 == 0 and ntaus2 == 0 and ntaus3 == 0): 
            print 'WWW(%s)'%(self.basename),'no tracker taus for dtg: ',self.dtg,' model: ',self.model,' stmid: ',self.stmid,' bailing...'
            return(0)
            

        if(self.verb): print 'fffffffffffff ',finalsource,self.model,self.stmid

        if(finalsource == 1):
            self.aidtrk=aidtrks1
            self.aidtaus=aidtaus1
            self.aidsource='w2flds'

        if(finalsource == 2):
            self.aidtrk=aidtrks2
            self.aidtaus=aidtaus2
            self.aidsource='external'

        if(finalsource == 3):
            self.aidtrk=aidtrks3
            self.aidtaus=aidtaus3
            self.aidsource='local'

        # -- bail point 2 -- no tracker taus for aid
        #
        if(len(self.aidtaus) == 0):
            print 'WWW(%s)'%(self.basename),'no final  tracker taus for dtg: ',self.dtg,' model: ',self.model,' stmid: ',self.stmid,' bailing...'
            return(0)
            

            
        
        self.diagpath="%s/diag.%s.%s.txt"%(self.pltdir,self.stmid,self.model)

        self.pyppath="%s/diag.%s.pyp"%(self.pltdir,self.stmid)
        self.pyppathHtml="%s/html.%s.pyp"%(self.pltdir,self.stmid)
        self.pyppathData="%s/data.%s.pyp"%(self.pltdir,self.stmid)
        self.diagpathALL="%s/diag.all.%s.%s.txt"%(self.pltdir,self.stmid,self.model)
        self.diagpathWebALL="%s/diag.all.%s.%s.txt"%(self.webdiagdir,self.stmid,self.model)
        
        self.pyppathDataALL="%s/data.all.%s.pyp"%(self.pltdir,self.stmid)
        if(self.doDiagOnly):
            self.diagpath=self.diagpathALL
            self.pyppathData=self.pyppathDataALL

        if(self.aidtrk != None and not(quiet)):
            print 'TCTCTCTCTCTCTCTCTCTCTCTCTCTCTCTCTCTCTCTCTC got tracker from aidsource: %-10s'%(self.aidsource),' model: %-6s'%(self.model),' stmid: ',self.stmid,' ntaus: %3d'%(len(self.aidtaus)),' lasttau: %3d'%(self.aidtaus[-1])

        # -- limit taus
        ataus=[]
        if(maxtau != None):
            for atau in self.aidtaus:
                if(atau in self.targetTaus):
                    ataus.append(atau)
            self.aidtaus=ataus
            

        return(1)


        
    def getAidcards(self,dtg,stmid):

        try:
            self.aidcards=self.aD.GetAidCards(self.aid,stmid)[dtg]

        except:
            self.aidcards=[]
            if(self.verb): print 'WWW(%s) no adeck cards    for aid: %s stmid: %s'%(self.basename,self.model,stmid)
            return





class MD2Keys(MFbase):
    

    def __init__(self,mddtgs,mddtgsBT,mdstmids,mdstmidsCC):
        self.mddtgs=mddtgs
        self.mddtgsBT=mddtgsBT
        self.mdstmids=mdstmids
        self.mdstmidsCC=mdstmidsCC

    def getKeys(self):
        return(self.mddtgs,self.mddtgsBT,self.mdstmids,self.mdstmidsCC)

    
    def sortStmidsMD2update(stm1ids):
    
        stm1ids.sort()
        basinorder=['l','e','c','w','i','a','b','s','p','q']
        ostm1ids=[]
    
        for bo in basinorder:
            for stm1id in stm1ids:
                b1id=stm1id.split('.')[0][-1]
                if(bo.upper() == b1id): ostm1ids.append(stm1id)
    
        stm1ids=ostm1ids
        ostm1ids=[]
        for bo in basinorder:
            stm9x=[]
            stmNN=[]
            for stm1id in stm1ids:
                b1id=stm1id.split('.')[0][-1]
                snum=int(stm1id.split('.')[0][0:2])
                if(snum >= 90 and (bo.upper() == b1id) ): stm9x.append(stm1id)
                if(snum <= 79 and (bo.upper() == b1id) ): stmNN.append(stm1id)
            ostm1ids=ostm1ids+stm9x+stmNN
    
        return(ostm1ids)
    
        
    #mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
    # unbounded methods for the classes
    #
            
    def initDSsMD2Keys(DSs,override=0,md2key='md2keys'):
    
        try:
            md2=DSs.getDataSet(key=md2key)
        except:
            md2=None
    
        if(md2 == None or override):
            DSs.mddtgs=[]
            DSs.mddtgsBT=[]
            DSs.mdstmids=[]
            DSs.mdstmidsCC=[]
        else:
            DSs.mddtgs=md2.mddtgs
            DSs.mddtgsBT=md2.mddtgsBT
            DSs.mdstmids=md2.mdstmids
            DSs.mdstmidsCC=md2.mdstmidsCC
        return
    
    # -- dss put methods for stms and dtgs
    #
    
    def putDssSmdDataSet(DSs,smD,stmid,verb=1):
    
        DSs.putDataSet(smD,key=stmid,verb=verb)
        if(not(stmid in DSs.mdstmids)):
            DSs.mdstmids.append(stmid)
            if(verb): print 'PPP putting stmid: ',stmid,' to DSs.mdstmids'
    
    
    def putDssSmdCCDataSet(DSs,smD,stmid,verb=0):
    
        DSs.putDataSet(smD,key=stmid,verb=verb)
        if(not(stmid in DSs.mdstmidsCC)):
            DSs.mdstmidsCC.append(stmid)
            if(verb): print 'PPP putting CC stmid: ',stmid,' to DSs.mdstmidsCC'
    
    
    
    def putDssDtgDataSet(DSs,dds,dtg,verb=0):
    
        DSs.putDataSet(dds,key=dtg,verb=verb)
        if(not(dtg in DSs.mddtgs)):
            DSs.mddtgs.append(dtg)
    
    
    
    def putDssDtgBTDataSet(DSs,dds,dtg,verb=0):
    
        DSs.putDataSet(dds,key=dtg,verb=verb)
        if(not(dtg in DSs.mddtgsBT)):
            DSs.mddtgsBT.append(dtg)
    
        
    
    def putDSsMD2Keys(DSs,override=0,md2key='md2keys',verb=0):
    
        md2=MD2Keys(DSs.mddtgs,DSs.mddtgsBT,DSs.mdstmids,DSs.mdstmidsCC)
        DSs.putDataSet(md2,key=md2key,verb=verb)
    
            
    
    def setDSsMD2Keys(DSs,override=1,md2key='md2keys'):
    
        MF.sTimer('keys')
        md2=DSs.getDataSet(key=md2key)
    
        if(md2 == None or override):
            mddtgs=[]
            mddtgsBT=[]
            mdstmids=[]
            mdstmidsCC=[]
            kk=DSs.getKeys()
    
        else:
            return
        
        for k in kk:
            if(mf.find(k,'.')):
                tt=k.split('.')
                if(tt[0].isdigit() and tt[1] == 'bt'):
                    mddtgsBT.append(k.lower())
                else:
                    mdstmids.append(k.lower())
            else:
                mddtgs.append(k)
    
        md2=MD2Keys(mddtgs,mddtgsBT,mdstmids)
        DSs.putDataSet(md2,key=md2key)
        
        MF.dTimer('keys')
    
            
    def getCtlpathTaus(model,dtg,maxtau=168):
        
        from WxMAP2 import W2
        w2=W2()
        
        ctlpath=taus=nfields=None
        rc=w2.getW2fldsRtfimCtlpath(model,dtg,maxtau=maxtau,verb=1)
        if(rc[0]):
            ctlpath=rc[1]
            taus=rc[2]
            nfields=rc[-2]
            tauOffset=rc[-1]
    
        return(ctlpath,taus,nfields)
    
class Bdeck(MFutils):
    

    def __init__(self,dtgopt=None,stmopt=None,verb=0):

        import ATCF
        from types import ListType

        yearneumann=YearTcBtNeumann

        minagephr=-8.0

        curdtg=mf.dtg()
        curyyyy=curdtg[0:4]
        
        (shemoverlap,yyyy1,yyyy2)=CurShemOverlap(curdtg)
        
        yyyy=curyyyy
        mm=curdtg[4:6]
        
        
        #
        # set years to two years to cover shem overlap
        #
        if(shemoverlap):
            years=[yyyy1,yyyy2]
            
        #
        # do previous year to catch overlap of storms crossing year
        #
        elif( (yyyy == curyyyy) and (int(mm) == 1)):
            yyyym1=int(yyyy)-1
            yyyym1=str(yyyym1)
            years=[yyyym1,yyyy]
            
        else:
            years=[curyyyy]

        #
        # get the list of stm2ids
        #

        if(stmopt != None):

            if(type(stmopt) is not(ListType)):
                stmids=MakeStmList(stmopt)
            else:
                stmids=stmopt

            stm2ids=[]
            for stmid in stmids:
                stm2id=stm1to2id(stmid)
                stm2ids.append(stm2id)

            years=[]
        
            for stm2id in stm2ids:
                years.append(stm2id.split('.')[1])

            years=mf.uniq(years)
            years.sort()


        if(dtgopt != None):
            dtgs=mf.dtg_dtgopt_prc(dtgopt)
        else:
            dtgs=[curdtg]


        bdecks=[]

        for year in years:

            (shemid,nioid)=TCNum2Stmid(year)

            bdir=w2.TcBdecksJtwcDir+"/%s"%(year)

            #
            # convert nrl/nhc bdecks in lant/epac/cpac to my bt.local.form
            #


            if(int(year) >= yearneumann):
                bdirbdeckal=w2.TcBdecksNhcDir+"/%s"%(year)
                bdirbdecksl=w2.TcBdecksNhcDir+"/%s"%(year)
                bdirbdeckep=w2.TcBdecksNhcDir+"/%s"%(year)
                bdirbdeckcp=w2.TcBdecksNhcDir+"/%s"%(year)

            maskbdeckal="%s/bal??%s.dat"%(bdirbdeckal,year)
            maskbdecksl="%s/bsl??%s.dat"%(bdirbdecksl,year)
            maskbdeckep="%s/bep??%s.dat"%(bdirbdeckep,year)
            #
            # handle case when cp storm -> jtwc aor
            # handle case where ep storm -> cpc -> jtwc updated
            #
            maskbdeckcpnhc="%s/bcp??%s.dat"%(bdirbdeckcp,year)
            maskbdeckcpjtwc="%s/bcp??%s.dat"%(bdir,year)
            maskbdeckepnhc="%s/bep??%s.dat"%(bdirbdeckep,year)
            maskbdeckepjtwc="%s/bep??%s.dat"%(bdir,year)
            maskbdeckwp="%s/bwp??%s.dat"%(bdir,year)
            maskbdeckio="%s/bio??%s.dat"%(bdir,year)
            maskbdecksh="%s/bsh??%s.dat"%(bdir,year)

            if(verb):
                print 'MMMMal     ',maskbdeckal
                print 'MMMMsl     ',maskbdecksl
                print 'MMMMep     ',maskbdeckep
                print 'MMMMcpnhc  ',maskbdeckcpnhc
                print 'MMMMcpjtwc ',maskbdeckcpnhc
                print 'MMMMepnhc  ',maskbdeckepnhc
                print 'MMMMepjtwc ',maskbdeckepnhc
                print 'MMMMwp     ',maskbdeckwp
                print 'MMMMio     ',maskbdeckio
                print 'MMMMsh     ',maskbdecksh


            bdeckswp=glob.glob(maskbdeckwp)
            bdecksio=glob.glob(maskbdeckio)
            bdeckssh=glob.glob(maskbdecksh)

            bdecksal=glob.glob(maskbdeckal)
            bdeckssl=glob.glob(maskbdecksl)

            bdeckscpnhc=glob.glob(maskbdeckcpnhc)
            bdeckscpjtwc=glob.glob(maskbdeckcpjtwc)

            bdecksepnhc=glob.glob(maskbdeckepnhc)
            bdecksepjtwc=glob.glob(maskbdeckepjtwc)

            #
            # def to pick "correct" deck
            #

            bdecksep=ATCF.PickBestDeck(bdecksepnhc,bdecksepjtwc,verb=verb)
            bdeckscp=ATCF.PickBestDeck(bdeckscpnhc,bdeckscpjtwc,verb=verb)

            bdecks= bdecks + bdeckswp + bdecksio + bdeckssh + bdeckscp + bdecksal + bdeckssl + bdecksep

        if(stmopt != None):

            self.bdeckcards={}
            self.stm1ids=[]
            self.paths=[]
            self.size={}
            self.mtime={}

            for bdeck in bdecks:
                
                for n in range(0,len(stmids)):
                    
                    stm2id=stm2ids[n]
                    stm1id=stmids[n]

                    tbdeck=stm2id.replace('.','')+'.dat'
                    
                    if(mf.find(bdeck,tbdeck)):
                        
                        if(verb): print 'hhhhh ',stm2id,bdeck
                    
                        self.paths.append(bdeck)
                        self.size[stm1id]=mf.GetPathSiz(bdeck)
                        self.mtime[stm1id]=mf.PathModifyTime(bdeck)
                        self.stm1ids.append(stm1id)
                        
                        try:
                            self.bdeckcards[stm1id]=open(bdeck).readlines()
                        except:
                            self.bdeckcards[stm1id]=None
                    



            self.bdptype=stmopt
                    

        else:
            
            stm2ids=[]

            for dtg in dtgs:

                (stmids,stmopt)=GetStmidsByDtg(dtg)

                for stmid in stmids:
                    stm2id=stm1to2id(stmid)
                    stm2ids.append(stm2id)

            stm2ids=mf.uniq(stm2ids)
            stm2ids.sort()
            curbdecks={}

            self.bdeckcards={}
            
            for bdeck in bdecks:

                (dir,file)=os.path.split(bdeck)
                if(len(file) == 13):
                    bstm2id=file[1:5]+'.'+file[5:9]
                else:
                    bstm2id=None

                for stm2id in stm2ids:
                    if(stm2id == bstm2id):
                        stm1id=stmids[stm2ids.index(stm2id)]
                        if(verb): print 'hhhhh ',stm2id,stm1id
                        curbdecks[dtg,stm1id]=bdeck

                try:
                    self.bdeckcards[bdeck]=open(bdeck).readlines()
                except:
                    self.bdeckcards[bdeck]=None
                    

            self.dtgs=dtgs
            self.curbdecks=curbdecks
