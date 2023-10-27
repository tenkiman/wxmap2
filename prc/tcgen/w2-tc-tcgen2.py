#!/usr/bin/env python
from M import MFutils
MFd=MFutils()
diag=1

if(diag): MFd.sTimer('load')
from tcbase import *

from TCtrk import TcPrBasin,tcgenModels,getBasinLatLonsPrecise,tcgenW3DatDir,\
     tcgenW3Dir,tcgenModelLabel,getBasinOptFromStmids,tcgenBasins,getGentaus,tcgenModelLabel

from M2 import setModel2
from FM import wjetmodels
if(diag): MFd.dTimer('load')


doTau120Rtfim9=0

# -- tmp
#tcgenW3DatDir='/dat3/tc/hfip'
# -- kaze/kishou location of tcgen.pypdb

if(w2.onTaifuu or w2.onKishou or w2.onTenki):
    ttcBaseGenDir="/w21/dat/tc/tcgen"
else:
    ttcBaseGenDir="%s../w22/dat/tc/tcgen"%(w2.HfipProducts)


anlSCdir="%s/anlSC"%(ttcBaseGenDir)
MF.ChkDir(anlSCdir,'mk')


class InvHash(Tcgen,DataSet):

    def __init__(self,
                 dsname,
                 tbdir=None,
                 diag=0,
                 verb=0,
                 override=0,
                 unlink=0):

        self.dsname=dsname

        if(tbdir == None):
            tbdir='/tmp'
            self.dsbdir="%s/DSs"%(tbdir)
        else:
            self.dsbdir=tbdir

        MF.ChkDir(self.dsbdir,'mk')

        self.bdir=self.dsbdir

        self.pyppath="%s/%s.pyp"%(self.dsbdir,self.dsname)

        iH=self.getPyp()

        if(iH == None):
            self.hash={}
        else:
            self.hash=iH.hash

        if(override): self.hash={}


    def putHash(self,key,value,override=0,verb=1):

        if(not(hasattr(self,'hash'))):
            print 'IIII making hash'
            self.hash={}

        try:
            haskey=self.hash.has_key(key)
        except:
            haskey=0

        try:
            lkey=len(self.hash[key])
        except:
            lkey=0


        if(not(haskey) or override or ( lkey != len(value)) ):
            self.hash[key]=value

        else:
            if(verb):  print 'hash for key: ',key,' already there'



    def getHash(self,key,verb=0):

        try:
            rc=self.hash[key]
        except:
            if(verb): print 'GGG no joy for key: ',key
            rc=None
        return(rc)


    def chkHash(self,key,hash=None,verb=0):

        self.parseHash(key,verb=verb)

        if(self.loadundef):
            rc=0
            if(verb): 
                print
                print 'KEY: ',key,' no joy .......'
                print 'bdtg ; vdtg: ',self.bdtg,self.vdtg
                print
                
            return(rc)

        else:
            rc=1
            if(verb): 
                print
                print 'KEY: ',key
                print 'bdtg ; vdtg: ',self.bdtg,self.vdtg
                print 'tcstate: ',self.tcState.keys()
            
            if(self.modALL != None): 
                if(verb): print 'modALL:  ',self.modALL.keys()
            else:
                print 'chkHash: modALL: -- None for key: ',key
                rc=0

            if(self.modtc0 != None): 
                if(verb): print 'modtc0:  ',self.modtc0.keys()
            else:
                print 'chkHash: modtc0: -- None for key ',key
                rc=0
                
            return(rc)

    def printFinalModelState(self,mstmid,doprint=0,do24hCPS=1,undef999=-9999.0):
        
        #04L.2014 (132, 'DIS', 12.719999999999999, 132.0, 64.60000000000001, 335.5, 18.400000000000002, 269.8, '05L.2014')
        #tg0023 (132, 'SC1', 2.6999999999999997, 72.0, 22.400000000000002, 290.8, 999.0, 999.0)
        
        rc=self.finalModelState[mstmid]

        alltrk=self.oTrks[mstmid]

        mtau=rc[0]
        mstate=rc[1]
        mstdd=rc[2]
        mnhourtrk=rc[3]
        mlat=rc[4]
        mlon=rc[5]
        olat=rc[6]
        olon=rc[7]

        iposit=alltrk[mtau]
        alat=iposit[0]
        alon=iposit[1]
        avmax=iposit[2]
        apmin=iposit[3]
        aalf=iposit[4]
        apoci=iposit[5]
        aroci=iposit[6]
        armax=iposit[7]
        adir=iposit[8]
        aspd=iposit[9]
        
        # -- find mean in prevous 24-h of cps
        #
        if(do24hCPS):
            
            alltaus=alltrk.keys()
            alltaus.sort()
            
            acpsB=[]
            acpsVTl=[]
            acpsVTu=[]

            try:
                acpsB.append(alltrk[alltaus[-1]][10])
            except:
                acpsB.append(undef999)
            
            try:
                acpsB.append(alltrk[alltaus[-2]][10])
            except:
                acpsB.append(undef999)
                
            try:
                acpsB.append(alltrk[alltaus[-3]][10])
            except:
                acpsB.append(undef999)
            
            try:
                acpsVTl.append(alltrk[alltaus[-1]][11])
            except:
                acpsVTl.append(undef999)
                
            try:
                acpsVTl.append(alltrk[alltaus[-2]][11])
            except:
                acpsVTl.append(undef999)
                
            try:
                acpsVTl.append(alltrk[alltaus[-3]][11])
            except:
                acpsVTl.append(undef999)
            
            try:
                acpsVTu.append(alltrk[alltaus[-1]][12])
            except:
                acpsVTu.append(undef999)
                
            try:
                acpsVTu.append(alltrk[alltaus[-2]][12])
            except:
                acpsVTu.append(undef999)
                
            try:
                acpsVTu.append(alltrk[alltaus[-3]][12])
            except:
                acpsVTu.append(undef999)
            
            if(len(acpsB) > 0):
                acpsBM=0.0
                nB=0
                for aB in acpsB:
                    if(verb): print 'AB',aB
                    if(aB != undef999):
                        acpsBM=acpsBM+aB    
                        nB=nB+1 
                if(nB > 0):
                    acpsBM=acpsBM/nB
                else:
                    acpsBM=undef999
                
            else:
                acpsBM=undef999



            if(len(acpsVTl) > 0):
                acpsVTlM=0.0
                nB=0
                for aB in acpsVTl:
                    if(verb): print 'VTl',aB
                    if(aB != undef999):
                        acpsVTlM=acpsVTlM+aB
                        nB=nB+1 
                if(nB > 0):
                    acpsVTlM=acpsVTlM/nB
                else:
                    acpsVTlM=undef999
                    
            else:
                acpsVTlM=undef999
                
            if(len(acpsVTu) > 0):
                acpsVTuM=0.0
                nB=0
                for aB in acpsVTu:
                    if(verb): print 'VTu',aB
                    if(aB != undef999):
                        acpsVTuM=acpsVTuM+aB
                        nB=nB+1 
                if(nB > 0):
                    acpsVTuM=acpsVTuM/nB
                else:
                    acpsVTuM=undef999
                    
            else:
                acpsVTuM=undef999
                    

            acpsB=acpsBM
            acpsVTl=acpsVTlM
            acpsVTu=acpsVTuM
            
            if(doprint == 2):
                print '%-10s %s %03d %5.0f  B: %4.0f  VTl: %6.0f  VTu: %6.0f'%(mstmid,mstate,mtau,avmax,acpsB,acpsVTl,acpsVTu)
                
        else:
        
            acpsB=iposit[10]
            acpsVTl=iposit[11]
            acpsVTu=iposit[12]
            
        (clatm,clonm)=Rlatlon2Clatlon(mlat,mlon,dodec=1)
        mcard="| %-10s %s sTDd: %4.1f %3d CPS(B,VTl,VTu): %5.0f %5.0f %5.0f  Pos(tau,lat,lon): %03d %s %s "%(mstmid,mstate,mstdd,int(mnhourtrk),
                                                                                                             acpsB,acpsVTl,acpsVTu,
                                                                                                             mtau,clatm,clonm)
            
        if(doprint):
            print mcard 

        rcStruct=(alat,alon,avmax,apmin,aalf,apoci,aroci,armax,adir,aspd,acpsB,acpsVTl,acpsVTu)
        return(mcard,rcStruct)
        
    
    def lsHash(self,key,hash=None,oneline=0):

        doprint=1
        if(oneline): doprint=0
        
        self.parseHash(key,verb=0)

        card=''
        if(self.loadundef):
            kcard='KEY: %s'%(str(key))
            kcard.strip()
            dcard='b:%s; v:%s'%(self.bdtg,self.vdtg)
            if(not(oneline)):
                print
                print 'KEY: ',key,' no joy .......'
                print 'bdtg ; vdtg: ',self.bdtg,self.vdtg
                
            return

        else:
            
            kcard='%s'%(str(key))
            kcard=kcard.replace(' ','')
            dcard='b:%s v:%s'%(self.bdtg,self.vdtg)
            tscard=str(self.tcState.keys())
            tscard=tscard.replace(' ','')
            tcard='TCs: %s'%(tscard)
            if(not(oneline)):
                print
                print 'KEY: ',key
                print 'bdtg ; vdtg: ',self.bdtg,self.vdtg
                print 'tcstate: ',self.tcState.keys()
                
            mcard='mTC:'
            if(self.modALL != None): 
                for mstmid in self.modALL.keys():
                    rc=self.printFinalModelState(mstmid,doprint=doprint)
                    #mcard=mcard+rc[0]
                    mcard="%s %s"%(mcard,mstmid)
            else:
                mcard='mALL: -- None '
                if(not(oneline)): print mcard

            if(self.modtc0 != None): 
                mcard0='mTC0: %s'%(str(self.modtc0.keys()))
                if(not(oneline)): print 'modtc0:  ',self.modtc0.keys()
            else:
                mcard0='modtc0: -- None '
                if(not(oneline)): print mcard0
                
            if(self.modtc0 == None and self.modALL == None):
                print 'WWW(lsHash.parseHash = None'
                return
            
            mcard0=mcard0.replace(' ','')
            
        stmids=self.fctcs.keys()

        for stmid in stmids:

            fctrk=self.oTrks[stmid]
            taus=fctrk.keys()
            taus.sort()

            fs=self.fctcs[stmid]
            self.lsFstate(stmid,fs,taus,doprint=doprint)

        pcard="pr: %4.2f prc: %4.2f rc2t: %4.2f "%(self.pr,self.prc,self.rc2t)
        
        if(not(oneline)):
            print "PR:   pr: %4.2f  prc: %4.2f  rc2t: %4.2f "%(self.pr,self.prc,self.rc2t)
            print 'TTTTT nTCs: ',self.nTCs,' npTCs: ',self.npTCs,' nGNs: ',self.nGNs,' naTCs: ',self.naTCs
            print 'MMMMM nSCs: ',self.nSCs,' stdSCs: ',self.stdSCs,' nGCs: ',self.nGCs,' nFCs: ',self.nFCs,' npFCs: ',self.npFCs,' nFCGNs: ',self.nFCGNs,' stdFCGNs: ',self.stdFCGNs
            print

        card="%s %s %s %s %s %s"%(kcard,dcard,tcard,pcard,mcard,mcard0)
        if(oneline): print card 
            

    
    def isGenTcMatch(self,fcstate):
        rc=0
        if(fcstate == 'GGT' or fcstate == 'FGT'):rc=1
        return(rc)


    def anlHashGen(self,key,genstmid,btcs,allgenstmids,verb=0,didrerun=0,warn=0):

        self.parseHash(key,verb=0)

        obsttd=tcD.getsTDd(btcs,self.vdtg,timeback=24)

        cards=[]
        noload=0
        mstmidUndef='UNDEF'

        if(self.loadundef):
            card="%-8s %s %-10s %s %03d O: %4.1f %4.0f %5.1f %5.1f NA"%(self.model,genstmid,mstmidUndef,self.vdtg,self.gentau,
                                                                           obsttd[0],obsttd[4],obsttd[2],obsttd[3])
            if(verb): print 'NNNNN: ',card
            cards.append(card)
            return(cards)
        else:
            card="%-8s %s %-10s %s %03d O: %4.1f %4.0f %5.1f %5.1f"%(self.model,genstmid,mstmidUndef,self.vdtg,self.gentau,
                                                               obsttd[0],obsttd[4],obsttd[2],obsttd[3])

        alltcs=self.tcState.keys()
        
        # -- check for multiple genesis stmids
        #
        ngenstms=0
        for alltc in alltcs:
            if(alltc in allgenstmids):
                ngenstms=ngenstms+1
            
        if(ngenstms > 1):
            if(warn): print 'WWW InvHash.lsHashGen -- multiple genesis storms for dtg: ',self.vdtg,'basin: ',self.basin,' genstmids: ',allgenstmids
            if(not(didrerun)): 
                print 'need to rerun with -O to add ostmid to fmstate...'
                sys.exit()
        
        mstmids=self.fctcs.keys()

        gotGenHits=0
        for igenstmid in allgenstmids:
            
            for mstmid in mstmids:
    
                ostmid=None
                fctrk=self.oTrks[mstmid]
                fctaus=fctrk.keys()
                fctaus.sort()
    
                fsM=self.fctcs[mstmid]
                fctrk=self.genfctrks[mstmid]
                fcvmax=fctrk[2]
                
                if(len(fsM) > 8):
                    (fctau,fcstate,fcstd,fclife,fclat,fclon,vclat,vclon,ostmid)=fsM
                    fs=(fctau,fcstate,fcstd,fcvmax,fclife,fclat,fclon,vclat,vclon,ostmid)
                else:
                    (fctau,fcstate,fcstd,fclife,fclat,fclon,vclat,vclon)=fsM
                    fs=(fctau,fcstate,fcstd,fcvmax,fclife,fclat,fclon,vclat,vclon)
                
                if( (ostmid != None and ostmid == genstmid) or self.isGenTcMatch(fcstate)):
    
                    # -- use mod tclife for obsTDd
                    #
                    obsttd=tcD.getsTDd(btcs,self.vdtg,timeback=fclife)
                    (cardls,rcStruct)=self.lsFstate(mstmid,fsM,fctaus,doprint=0,anltype='sc')
                    #print 'CCCC',cardls,rcStruct
                    
                    card="%-8s %s %-10s %s %03d O: %4.1f %4.0f %5.1f %5.1f"%(self.model,genstmid,mstmid,self.vdtg,self.gentau,
                                                                       obsttd[0],obsttd[4],obsttd[2],obsttd[3])
                    
                    card="%s M: %4.1f %4.0f %5.1f %5.1f %s %03d %5.1f"%(card,fcstd,fcvmax,fclat,fclon,fcstate,fctau,fclife)
                    card="%s CPS: %4.0f %5.0f %5.0f"%(card,rcStruct[-3],rcStruct[-2],rcStruct[-1])
                    if(verb): 
                        #print "FC:  %8s "%(stmid),"Fstate fctau: %03d  fcstate: %3s  fcstd: %4.1f  fcvmax: %4.0f fclife: %5.1f  fclat/lon:(%5.1f,%5.1f)  vclat/lon:(%5.1f,%5.1f)  ostmid: %s"%(fs)  
                        print 'YYYYY: ',card
                    cards.append(card)
                    gotGenHits=1
                
            if(not(gotGenHits)):
                card="%s FAILED"%(card)
                cards.append(card)
                
            if(len(cards) > 1):
                ncards=[]
                nbesttype=-1
                longest=-999
                strongest=-999
                # -- initialize to 0 for case when all fail
                nlong=nstrong=nbesttype=0

                for n in range(0,len(cards)):
                    if(verb): print 'multiple card: ',n,cards[n]
                    tt=cards[n].split()
                    if(tt[-1] == 'FAILED'): continue
                    gtime=float(tt[12])
                    gstd=float(tt[11])
                    gtype=tt[15]
                    
                    gstmid=tt[2]
                    olat=float(tt[8])
                    olon=float(tt[9])
                    glat=float(tt[13])
                    glon=float(tt[14])
                    
                    gdist=gc_dist(olat,olon,glat,glon)
                    # -- check if located within

                    if(gdist >= self.distMinTC[self.gentau]):
                        if(warn): print 'WWW out of bounds for n: ',n,' gstmid: ',gstmid,' gdist: %5.0f'%(gdist)
                        continue
                    
                    if(gtype == 'FGT' or gtype == 'GGT'):  nbesttype=n
                    if(gtime > longest): longest=gtime   ; nlong=n
                    if(gstd > strongest): strongest=gstd ; nstrong=n
                
                if(nlong == nstrong == nbesttype): 
                    nbest=nlong
                    ntype='longest/strongest/best'
                    if(verb): print 'selecting ',ntype,nbest
                elif(nlong == nstrong):
                    nbest=nlong
                    ntype='longest/strongest'
                    if(verb): print 'selecting ',ntype,nbest
                else:
                    nbest=nstrong
                    ntype='strongest'
                    if(verb): print'selecting  ',ntype,nbest
                    
                if(warn): print 'WWWW have multiple genstm hits: %-8s %s %s %3d'%(self.model,genstmid,self.vdtg,self.gentau),' -- picking the ',ntype,' '
                
                ncards.append(cards[nbest])
                cards=ncards
        
        return(cards)



    def lsFstate(self,stmid,fs,fctaus,doprint=1,anltype=None):
        
        fctrk=self.genfctrks[stmid]
        fcvmax=fctrk[2]
        ostmid=None
        card=None
        alltrk=self.oTrks[stmid]
        taus=alltrk.keys()
        taus.sort()
        if(len(fs) > 8):
            (fctau,fcstate,fcstd,fclife,fclat,fclon,vclat,vclon,ostmid)=fs
            fs=(fctau,fcstate,fcstd,fcvmax,fclife,fclat,fclon,vclat,vclon,ostmid)
        else:
            (fctau,fcstate,fcstd,fclife,fclat,fclon,vclat,vclon)=fs
            fs=(fctau,fcstate,fcstd,fcvmax,fclife,fclat,fclon,vclat,vclon)

        (fclatc,fclonc)=Rlatlon2Clatlon(fclat,fclon)
        if(ostmid != None):
            card="FC:  %8s %4.1f %s %s"%(stmid,fcstd,fclatc,fclonc)
            card2="Fstate fctau: %03d  fcstate: %3s  fcstd: %4.1f  fcvmax: %4.0f fclife: %5.1f  fclat/lon:(%5.1f,%5.1f)  vclat/lon:(%5.1f,%5.1f) ostmid: %s"%(fs)
        else:
            card="FC:  %8s %4.1f %s %s"%(stmid,fcstd,fclatc,fclonc)
            card2="Fstate fctau: %03d  fcstate: %3s  fcstd: %4.1f  fcvmax: %4.0f fclife: %5.1f  fclat/lon:(%5.1f,%5.1f)  vclat/lon:(%5.1f,%5.1f) "%(fs),' tau: ',fctaus
            
        rcStruct=None
        if(anltype == 'sc'):
            (card,rcStruct)=self.printFinalModelState(stmid)
            if(doprint): print card
            
        return(card,rcStruct)



    def parseHash(self,key,hash=None,loadundef=1,undefSC=-99,undefPR=-999.,verb=1):


        if(hash == None):
            rc=self.getHash(key,verb=0)
        else:
            rc=hash

        if(verb): print ; print 'KEY: ',key,' in parseHash'
        if(rc == None):
            if(verb): print 'Nada for key: ',key,' loadundef: ',loadundef
            if(loadundef):
                self.nSCs=undefSC
                self.nGCs=undefSC
                self.nFCs=undefSC
                self.nNFCs=undefSC
                self.npFCs=undefSC
                self.nFCGNs=undefSC

                self.nTCs=undefSC
                self.nNTCs=undefSC
                self.nGNs=undefSC
                self.npTCs=undefSC
                self.naTCs=undefSC
                
                self.stdSCs=undefSC
                self.stdFCGNs=undefSC
                self.stdpFCs=undefSC
                self.stdGCs=undefSC
                self.rc2t=undefPR
                self.prc=undefPR
                self.pr=undefPR
                self.loadundef=1
            else:
                print 'EEE tcgen.parseHash: loadundef=0, sayoonara' 
                sys.exit()

        else:
            loadundef=0


        (model,dtg,basin,gentau,gentype)=key

        if(gentype == 'veri'):
            vdtg=dtg
            bdtg=mf.dtginc(dtg,-gentau)
        else:
            bdtg=dtg
            vdtg=mf.dtginc(dtg,+gentau)

        self.model=model
        self.basin=basin
        self.gentau=gentau
        self.gentype=gentype
        self.bdtg=bdtg
        self.vdtg=vdtg

        self.loadundef=loadundef

        if(loadundef): return

        (tcState,finalModelState,pr,
         oTrks,
         ntcALL,nmodALL,nmodtc0,
         modALL,modtc0)=rc

        self.finalModelState=finalModelState
        self.modALL=modALL
        self.modtc0=modtc0

        if(verb):
            print 'bdtg ; vdtg: ',bdtg,vdtg
            print 'tcstate: ',tcState.keys()
            if(modALL != None):
                print 'modALL:  ',modALL.keys()
            else:
                print 'parseHash modALL = None'
            if(modtc0 != None):
                print 'modtc0:  ',modtc0.keys()
            else:
                print 'parseHash modtc0 = None'


        # -- fc tracks
        #
        stmids=finalModelState.keys()
        fctcs={}

        for stmid in stmids:
            fs=finalModelState[stmid]
            fctcs[stmid]=fs


        self.fctcs=fctcs
        self.oTrks=oTrks

        self.tcState=tcState

        stmids=tcState.keys()

        gtcs={}
        abtcs={}
        for stmid in stmids:
            fs=tcState[stmid]

            if(fs[0] == 'GN'):
                gtcs[stmid]=fs[1]
                abtcs[stmid]=fs[1]
            else:
                abtcs[stmid]=fs[1]


        self.gtcs=gtcs
        self.abtcs=abtcs

        # -- precip
        #
        self.rc2t=pr[0]
        self.prc=pr[1]
        self.pr=pr[2]


        # -- count/std analysis
        #

        tstmids=tcState.keys()
        mstmids=finalModelState.keys()

        # -- real TCs
        #
        nNTCs=0
        nTCs=0
        nGNs=0
        npTCs=0

        for stmid in tstmids:
            tcstate=tcState[stmid][0]
            tcvmax=tcState[stmid][1][2]

            if(Is9X(stmid)):
                npTCs=npTCs+1

            if(IsNN(stmid)):
                if(tcstate == 'NT'):
                    nNTCs=nNTCs+1
                else:
                    nTCs=nTCs+1

            if(tcstate == 'GN'):
                nGNs=nGNs+1

            if(verb): print 'TTT ',stmid,tcstate,tcvmax
            
        # -- model tau0 cyclones in analysis
        #
        

        naTCs=0
        if(modtc0 != None):
            for stmid in modtc0.keys():
                naTCs=naTCs+1


        nSCs=0
        stdSCs=0.0
        stdFCGNs=0.0
        stdpFCs=0.0
        stdGCs=0.0

        nGCs=0
        nFCs=0
        nNFCs=0
        npFCs=0
        nmFTCs=0
        nmDTCs=0 # dissipated TCs

        nFCGNs=0

        genfctrks={}

        if(mstmids != None):
            
            for stmid in mstmids:
    
                ostmid=None
                try:
                    tcstate=tcState[stmid][0]
                except:
                    tcstate=None
    
                fctrk=self.oTrks[stmid]
                fctaus=fctrk.keys()
                fctaus.sort()

                # -- get full posit at gentau if available
                #
                if(gentau in fctaus):
                    genfctrk=fctrk[gentau]
                else:
                    genfctrk=fctrk[fctaus[-1]]
                    
                genfctrks[stmid]=genfctrk
                
                fs=finalModelState[stmid]
                if(len(fs) > 8):
                    (fctau,fcstate,fcstd,fclife,fclat,fclon,vclat,vclon,ostmid)=fs
                else:
                    (fctau,fcstate,fcstd,fclife,fclat,fclon,vclat,vclon)=fs
    
                if(fcstate == 'SC1'):
                    nSCs=nSCs+1
                    stdSCs=stdSCs+fcstd
    
                elif( (fcstate == 'FTC' or fcstate == 'FGT') or (fcstate == 'GTC') or (fcstate == 'MFC') ):
                    nFCs=nFCs+1
    
                elif( fcstate == 'FNT' or fcstate == 'GNT' ):
                    nNFCs=nNFCs+1
    
                elif( fcstate == 'FPT' or fcstate == 'GPT' or fcstate == 'MFP'):
                    npFCs=npFCs+1
                    stdpFCs=stdpFCs+fcstd
              
                elif( fcstate == 'FMT' or fcstate == 'GMT'):
                    nmFTCs=nmFTCs+1
    
                elif( fcstate == 'DIS'):
                    nmDTCs=nmDTCs+1
    
                elif( fcstate == 'MGC' or fcstate == 'MNN'):
                    nFCGNs=nFCGNs+1
                    stdFCGNs=stdFCGNs+fcstd
    
                if( fcstate == 'FGT' or fcstate == 'GGT' or (fcstate == 'MFC' and tcstate == 'GN') ):
                    nGCs=nGCs+1
                    stdGCs=stdGCs+fcstd
    
                if(verb): print 'MMM ',stmid,fcstate,fcstd
    
        self.genfctrks=genfctrks
        
        # -- real TCs
        #
        self.nTCs=nTCs
        self.nNTCs=nNTCs
        self.nGNs=nGNs
        self.npTCs=npTCs
        
        # -- model analysis TCs
        
        self.naTCs=naTCs

        # -- model TCs
        #
        self.nSCs=nSCs
        self.nGCs=nGCs
        self.nNFCs=nNFCs
        self.nFCs=nFCs
        self.npFCs=npFCs
        self.nmFTCs=nmFTCs
        self.nmDTCs=nmDTCs
        self.nFCGNs=nFCGNs

        # -- model spuricanes
        #
        self.stdSCs=stdSCs
        self.stdFCGNs=stdFCGNs
        self.stdpFCs=stdpFCs
        self.stdGCs=stdGCs

        return



    def lsInv(self,
              models,
              basins,
              dtgs,
              gentaus,
              dogendtg,
              mode='ls',
              oneline=0,
              ):


        gentype='fcst'
        if(dogendtg): gentype='veri'

        rc=1
        
        for model in models:
            for basin in basins:
                for dtg in dtgs:
                    for gentau in gentaus:
                        key=(model,dtg,basin,gentau,gentype)
                        if(mode == 'ls'): self.lsHash(key,oneline=oneline)
                        if(mode == 'chk'): 
                            rc=self.chkHash(key)
                            if(rc == 0): return(rc)
        if(oneline): print


        return(rc)

    def anlInvSpur(self,
                   spurCards,
                   models,
                   basins,
                   dtg,
                   gentaus,
                   dogendtg,
                   verb=0,
              ):    

        gentype='fcst'
        if(dogendtg): gentype='veri'

        rc=1
        
        for model in models:
            for basin in basins:
                for gentau in gentaus:
                    print 'AAAA-SSSCCC: ',dtg,model,basin,gentau
                    key=(model,dtg,basin,gentau,gentype)
                    gstmids=tcD.getGenStmidsByDtgGenBasin(dtg, basin)
                    
                    allcards=[] 
                    for gstmid in gstmids:
                        allcards=anlTcGen(tcD,gstmid,[model],gentaus,allcards,verb=verb,didrerun=1)
                        
                    gencard=' _ no-gen'
                    for allcard in allcards:
                        tt=allcard.split()
                        adtg=tt[3]
                     
                        if(adtg == dtg):
                            gencard=' _ %s'%(allcard)
                            
                    card=self.anlHashSpur(key,verb=verb)
                    if(card != None):   
                        card=card+gencard
                    spurCards[model,dtg,basin,gentau]=card


        return(rc)

    def anlHashSpur(self,key,hash=None,verb=0):

        self.parseHash(key,verb=verb)
        
        (model,dtg,basin,gentau,gentype)=key

        if(self.loadundef and verb):
            print
            print 'KEY: ',key,' no joy .......'
            print 'bdtg ; vdtg: ',self.bdtg,self.vdtg
            print
            return(None)

        else:
            if(verb):
                print
                print 'KEY: ',key
                print 'bdtg ; vdtg: ',self.bdtg,self.vdtg
                print 'tcstate: ',self.tcState.keys()
                if(self.modALL != None): 
                    print 'modALL:  ',self.modALL.keys()
                else:
                    print 'modALL: -- None '

                if(self.modtc0 != None): 
                    print 'modtc0:  ',self.modtc0.keys()
                else:   
                    print 'modtc0: -- None '
                
                if(self.modtc0 == None and self.modALL == None):
                    print 'WWW(lsHash.parseHash = None'
                    return
            
        try:
            stmids=self.fctcs.keys()
            stmids.sort()
        except:
            print 'WWW - no fctcs for ',key
            return(None)
        
        #print "PR:   pr: %4.2f  prc: %4.1f  rc2t: %4.1f "%(self.pr,self.prc,self.rc2t)
        ocard="%-8s %-6s %03d  %s  pr: %4.2f  prc: %4.1f  rc2t: %4.2f"%(model,basin,gentau,self.vdtg,self.pr,self.prc,self.rc2t)
        
        if(verb):
            print 'TTTTT nTCs: ',self.nTCs,' npTCs: ',self.npTCs,' nGNs: ',self.nGNs,' naTCs: ',self.naTCs
            print 'MMMMM nSCs: ',self.nSCs,' stdSCs: ',self.stdSCs,' nGCs: ',self.nGCs,' nFCs: ',self.nFCs,' npFCs: ',self.npFCs,' nFCGNs: ',self.nFCGNs,' stdFCGNs: ',self.stdFCGNs

        
        for stmid in stmids:

            fctrk=self.oTrks[stmid]
            taus=fctrk.keys()
            taus.sort()

            fs=self.fctcs[stmid]
            (card,rcStruct)=self.lsFstate(stmid,fs,taus,doprint=0,anltype='sc')
            ocard="%s %s"%(ocard,card)
            
        if(verb): print 'InvHash.anlHashSpur: ',ocard
        
        return(ocard)





#BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB
# unbounded methods

def setTmtrkNDir(dtg,dtgBaseGen=None,dogendtg=0,gentaus=[],maxold=5):
    
    testdtg=dtg
    if(dogendtg): testdtg=mf.dtginc(dtg,-gentaus[-1])
    howold=mf.dtgdiff(testdtg,dtgBaseGen)/24.0

    if(w2.onTenki):
        stcgbdir='/w21/dat/tc/tmtrkN'
        stcgbdir='/w21/dat/tc/adeck/tmtrkN'
    elif(w2.onGmu):
        stcgbdir='/w21/dat/tc/tmtrkN'
        stcgbdir='/w21/dat/tc/adeck/tmtrkN'
    elif(not(w2.onKaze)):  
        stcgbdir='/w21/dat/tc/tmtrkN'
    elif(w2.onTaifuu):
        stcgbdir='/w21/dat/tc/tmtrkN'
    else:
        print 'EEE--w2-tc-tcgen2.py in setTmtrkNdir'
        sys.exit()
        
    ttcgbdir="%s/%s"%(ttcBaseGenDir,dtgBaseGen[0:4])
    MF.ChkDir(ttcgbdir,'mk')
        
    return(ttcgbdir,stcgbdir)




def anlTcGen(tcD,stmid,models,gentaus,allcards,mode='veri',didrerun=0,verb=0):

    dogendtg=1
    
    gentype='fcst'
    if(mode == 'veri'): gentype='veri'
    
    dds=tcD.getDSsStm(stmid)
    igendtgs=dds.gendtgs
    gendtgs=MF.get0012fromDtgs(igendtgs)
    basins=getBasinOptFromStmids(stmid)
    btcs=tcD.getBtcs4Stmid(stmid)
    
    for model in models:
        for basin in basins: 
            for gendtg in gendtgs:
                allgenstmids=tcD.getGenStmidsByDtgGenBasin(gendtg,basin)
                (ttcgbdir,stcgbdir)=setTmtrkNDir(gendtg,dtgBaseGen=gendtg)
                iV=InvHash(dsname='invTcgen.%s'%(gendtg),
                           tbdir=ttcgbdir,
                           diag=diag,
                           verb=verb,
                           override=doclean,
                           unlink=doclean)
                
                for gentau in gentaus:
                    key=(model,gendtg,basin,gentau,gentype)
                    cards=iV.anlHashGen(key,stmid,btcs,allgenstmids,verb=verb,didrerun=didrerun)
                    allcards=allcards+cards
                    
                    
                    
    return(allcards)
                    
                    
        


def getGenDtgsByStorm(tcD,stmids,filt00z12z=1,verb=0):

    gendtgs=[]
    for stmid in stmids:
        dss=tcD.getDSsFullStm(stmid,dobt=1)

        if(dss != None):
            gendtgs=gendtgs+dss.gendtgs
            if(verb): print 'GGGendtgs for stmid: ',stmid,' gendtgs: ',gendtgs

    finaldtgs=[]
    for gendtg in gendtgs:
        hh=gendtg[8:10]
        if(filt00z12z and (hh == '00' or  hh == '12')): finaldtgs.append(gendtg)

    finaldtgs=MF.uniq(finaldtgs)

    return(finaldtgs)


#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# command line setup
#

class AdgenCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv is None): argv=sys.argv

        self.argv=argv
        self.argopts={
            1:['dtgopt',  'run dtgs'],
            2:['modelopt',    'model|model1,model2|all|allgen'],
        }

        self.defaults={
            'doupdate':0,
            'BMoverride':0,
        }

        self.options={
            'override':      ['O',0,1,'override'],
            'overrideGA':    ['0',0,1,'overrideGA -- just track anl'],
            'trkoverride':   ['o',0,1,'override in dotrk'],
            'PRoverride':    ['p',0,1,"""do Pr analysis vice pulling from .pypdb"""],
            'verb':          ['V',0,1,'verb=1 is verbose'],
            'quiet':         ['q',1,0,' run GA in NOT quiet mode'],
            'diag':          ['d',0,1,' extra diagnostics'],
            'ropt':          ['N','','norun',' norun is norun'],
            'doplot':        ['P',1,0,'do NOT make plots'],
            'anlType':       ['A:',None,'a','analyze type for tcgen: verigen | sc-SSS where sc is spuricane and SSS is tag of .pypdb files'],
            'runInCron':     ['C',0,1,'''being run in crontab'''],
            'doLatest':      ['a',0,1,'''do cp to latest...'''],
            'cycle':         ['Y',0,1,'cycle models/dtgs'],
            'doxv':          ['X',0,1,'1 - doxv in w2PlotGen'],
            'dowindow':      ['W',0,1,'1 - dowindow in GA.setGA()'],
            'gentauOpt':     ['t:','all','a',"""gentauOpt -- fc tau opt for genesis: 'all'|'allgen'|'all24h'"""],
            'basinopt':      ['b:','all','a',' basin with gen adecks'],
            'ndayback':      ['n:',30,'i','ndayback in inventory'],
            'parea':         ['a:',None,'a',' w2 plot area'],
            'dogendtg':      ['T',0,1,' dogendtg -- set bdtg, gentau back from dtgopt'],
            'lsInv':         ['l',0,1,' ls from inv'],
            'invopt':        ['I:',None,'a','invopt -- make inventory for tcgen.php'],
            'invoverride':   ['i',1,0,'invoverride -- do NOT force inventory at end'],
            'verioverride':  ['v',0,1,'verioverride -- do NOT force running verification mode at end'],
            'stmopt':        ['S:',None,'a','stmopt'],
            'doclean':       ['K',0,1,"""blow away .pypdb file because shelf created with 'c' option """],
            'doland':        ['L',0,1,' doland -- plot/analyze land points'],
            'bypassTrkchk':  ['B',1,0,' do NOT bypass trk chk to make plot...needed by invJs'],
            'dochkIfRunning':['c',1,0,'do NOT using MF.chkIfJobIsRunning'],
            'redoOnChkInv':  ['R',0,1,'DO redoOnChkInv=1 -- redo based on lsInv check'],  # 20160922 -- not sure why we need this...
        }



        self.purpose='''
purpose -- parse and create adeck card data shelves
	 m2models: %s
   wjetmodels: %s
  tcgenModels: %s
  tcgenBasins: %s
 '''%(w2.Nwp2ModelsAll,wjetmodels,tcgenModels,tcgenBasins)
        self.examples='''
%s 2009080100 rtfimR925 -b wpac,epac,lant -G
'''

argv=sys.argv
CL=AdgenCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr


# -- put check in here if running, if so bail
#
if(ropt != 'norun' and lsInv == 0 and dochkIfRunning and anlType == None):
    rc=MF.chkRunning(pyfile, strictChkIfRunning=1, verb=0, killjob=0, 
                     timesleep=15, nminWait=15)


MF.sTimer('all')

dtgs=mf.dtg_dtgopt_prc(dtgopt)
models=modelopt.split(',')
if(modelopt == 'all'): models=tcgenModels
if(basinopt == 'all'): basins=tcgenBasins
else:                  basins=basinopt.split(',')

gentaus=getGentaus(gentauOpt)

#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# main 

# -- get stmids and gendtgs
#
stmids=None
gendtgs=None

if(stmopt != None):

    if(diag): MF.sTimer(tag='tcD-stmopt')
    if(ropt != 'norun'): tcD=TcData(stmopt=stmopt)
    if(diag): MF.dTimer(tag='tcD-stmopt')

    stmids=MakeStmList(stmopt,dofilt9x=1,verb=verb)
    gendtgs=getGenDtgsByStorm(tcD,stmids)
    basins=getBasinOptFromStmids(stmids)
    
    if(len(gendtgs) > 0):
        dtgs=gendtgs
    else:
        print 'EEEEEEEEEEEEEEEE no gendtgs for stmopt: ',stmopt
        sys.exit()

else:

    if(diag): MF.sTimer(tag='tcD')
    if(ropt != 'norun'): tcD=TcData(dtgopt=dtgopt)
    if(diag): MF.dTimer(tag='tcD')

    gendtgs=None


# -- AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
#
if(anlType != None):
    
    # -- genesis
    #
    dogendtg=1
    
    if(anlType == 'verigen' or anlType == 'vg'):

        if(stmopt == None):
            print 'EEE(%s) for anlType: %s -- must set -S stmopt -- ja sayounara'%(pyfile,anlType)
            sys.exit()

        allcards=[] 
        for stmid in stmids:
            allcards=anlTcGen(tcD,stmid,models,gentaus,allcards,verb=verb,didrerun=1)
            
        opath="%s/verigen.%s.%s.%s.txt"%(ttcBaseGenDir,modelopt,stmopt,gentauOpt)
        print 'OOO: ',opath
        MF.WriteList2File(allcards,opath)
        
        for card in allcards:
            print card
            
    # -- spuricanes
    #
    elif(mf.find(anlType,'spur') or mf.find(anlType,'sc') ):
        
        tt=anlType.split('-')
        anlTag='misc'
        if(len(tt) == 2): anlTag=tt[1]

        dsname='spuricane-%s'%(anlTag)
        sC=DataSet(name=dsname,bdir=anlSCdir,verb=verb)
        rc=sC.getPyp()
        if(rc == None): sC.data={}
        
        spurCards=sC.data
        diag=1
        for dtg in dtgs:
            (ttcgbdir,stcgbdir)=setTmtrkNDir(dtg,dtgBaseGen=dtg)
            if(diag): MF.sTimer(tag='anlSpur-%s'%(dtg))
            iV=InvHash(dsname='invTcgen.%s'%(dtg),
                       tbdir=ttcgbdir,
                       diag=diag,
                       verb=verb,
                       override=doclean,unlink=doclean,
                       )
            iV.anlInvSpur(spurCards,models,basins,dtg,gentaus,dogendtg,verb=verb)
            if(diag): MF.dTimer(tag='anlSpur-%s'%(dtg))
            

        sC.putPyp()
        
    MF.dTimer('all')
    sys.exit()

# -- LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL
#
if(lsInv):

    for dtg in dtgs:
        (ttcgbdir,stcgbdir)=setTmtrkNDir(dtg,dtgBaseGen=dtg)
        if(diag): MF.sTimer(tag='inV.ls')
        iV=InvHash(dsname='invTcgen.%s'%(dtg),
                   tbdir=ttcgbdir,
                   diag=diag,
                   verb=verb,
                   #override=doclean,unlink=doclean, -- no cleaing if doing ls...
                   )
        iV.lsInv(models,basins,[dtg],gentaus,dogendtg,oneline=1)
        if(diag): MF.dTimer(tag='inV.ls')
    MF.dTimer('all')
    sys.exit()

#if(doplot): doxv=1
# -- iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii -- do inventory for tcgen.php
#
MF.sTimer('tcgen.inv')
doTCGinventory=(invopt == 'all' or (invopt in tcgenBasins) or invopt != None )
if(doTCGinventory ):
    MF.sTimer('tcgen.inv.js')
    rc=makeTcgenJsInventory(dtgopt,gendtgs,stmids,basins,invopt=invopt,
                            gentaus=gentaus,
                            verb=verb,ndayback=ndayback)
    # -- 20200317 -- now rsync to wxmap2
    #
    rc=rsync2Wxmap2('tcgen')
    
    MF.dTimer('tcgen.inv.js')
    sys.exit()

# -- cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc -- cycling
#

if(cycle and len(models) > 1):

    for model in models:
        cmd="%s %s %s"%(pypath,dtgopt,model)
        for o,a in CL.opts:
            if(o != '-Y' and o != '-i'):
                cmd="%s %s %s"%(cmd,o,a)

        # -- add -c option to bypass chkifrunning
        cmd="%s -c"%(cmd)
        mf.runcmd(cmd,ropt,prefix="cycling")

    sys.exit()

# -- make gaP object
#
xgrads=setXgrads(useStandard=0,useX11=0,returnBoth=0)

tcGP=TcgenGA(gaQuiet=quiet,overrideGA=overrideGA,xgrads=xgrads)

# -- mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm models
#
didPrc=0
for model in models:

    # -- 20160818 -- force fim8 to bypassTrkchk during hfip on jet because it's very late...
    #
    ibypassTrkchk=bypassTrkchk
    iredoOnChkInv=redoOnChkInv
    if(model == 'fim8' or model == 'rtfim9'): 
        ibypassTrkchk=0
        iredoOnChkInv=0
    
    
    # -- dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd dtgs
    #
    for dtg in dtgs:

        # -- set the source/target dirs for tmtrkN/tcgen.pypdb
        #
        (ttcgbdir,stcgbdir)=setTmtrkNDir(dtg,dtgBaseGen=dtg,
                                         dogendtg=dogendtg,gentaus=gentaus)

        if(ropt != 'norun'):
            if(diag): MF.sTimer(tag='inV')
            iV=InvHash(dsname='invTcgen.%s'%(dtg),
                       tbdir=ttcgbdir,
                       diag=diag,
                       verb=verb,
                       override=doclean,
                       unlink=doclean)
            rc=iV.lsInv([model],basins,[dtg],gentaus,dogendtg,mode='chk')
            
            # -- run lsInv in 'chk' mode -- for cases of bad hashes?
            #
            print
            print 'CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC lsInv.chk model: ',model,' dtg: ',dtg,' rc: ',rc,\
                  'redoOnChkInv: ',iredoOnChkInv
            print
            
            if(rc == 0 and iredoOnChkInv and not(override)):
                print 'RRRRREEEEDDDDOOOO: ',model,dtg,gentaus,' rc: ',rc
                dogendtgOpt=''
                if(dogendtg): dogendtgOpt='-T'
                cmd="%s %s %s -b %s %s -t %s -O -c"%(pypath,dtg,model,basinopt,dogendtgOpt,gentauOpt)
                mf.runcmd(cmd,ropt)
                continue
                        
            if(diag): MF.dTimer(tag='inV')
            
        # -- bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb basins
        #
        for basin in basins:

            if(len(basins) == 1 and len(dtgs) == 1 and len(models) == 1 ): print
            print 'TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT TCgen2 model: %9s dtg: %s basin: %5s '%(model,dtg,basin),' gentaus: ',gentaus,' doplot: ',doplot,' bypassTrkchk: ',ibypassTrkchk
            if(len(basins) == 1 and len(dtgs) == 1 and len(models) == 1 ): print
            if(ropt == 'norun'): continue

            # -- get basin obj
            #
            tcB=TcBasin(basin)
            
            # -- get precip state obj
            #
            prB=TcPrBasin(model,basin,dtg)
            
            # -- loop by gentaus
            #
            for gentau in gentaus:

                bdtg=dtg
                if(dogendtg):
                    bdtg=mf.dtginc(dtg,-gentau)
                    prB=TcPrBasin(model,basin,bdtg)

                # -- make tcG object -- put in the dtg, bdtg will be calc inside the obj
                #
                omodelPlot=None
                if(model == 'ecm4'): omodelPlot='ecm2'
                
                tcG=Tcgen(tcGP,tcD,iV,tcB,prB,model,basin,dtg,gentau,dogendtg,stcgbdir,
                          omodelPlot=omodelPlot,
                          bypassTrkchk=ibypassTrkchk,
                          verb=verb,
                          override=override,
                          overrideGA=overrideGA)

                # -- if no gen adecks then bail if ibypassTrkchk
                #
                if(ibypassTrkchk == 0 and tcG.bypass and not(override)):
                    print 'BBBBYYYYYPPPPASSS-ibpassTrkchk == 0 and trackers not there...press...'
                    continue
                
                
                # -- check if data there
                #
                if(not(tcG.datathere)):
                    print 'WWW no ctlpath for model: ',model,' dtg: ',dtg,' basin: ',basin,' gentau: ',gentau,' dogendtg: ',dogendtg
                    if(overrideGA):
                        print 'WWW overrideGA -- just do track anl'
                    else:
                        continue

                # -- get precip
                #
                pr=prB.getPrsTau(gentau)
                tcG.pr=pr
                
                # -- processing tests -- dopr for either PRoverride | override  
                #
                if(pr == None): 
                    prall1=0
                else:
                    prall1=(pr[0] == 1 and pr[1] == 1 and pr[2] == 1)
                    
                dopr=( pr == None or (len(pr) == 2) or ( len(pr) == 3 and pr[2] == -999. ) or prall1 or PRoverride or override)
                dosettcgen=( tcG.done == 0 or override or overrideGA)
                if(overrideGA): dopr=0
                
                # -- if not done, look at the fields and get...TcPrBasin is only a container
                #
                if(dopr):
                    pr=tcG.fldDiagTcGen(basin,gentau,dogendtg,quiet=quiet,verb=verb)
                    # -- old data
                    try:
                        prB.prs[gentau]=pr
                    except:
                        prB.prs={}
                        prB.prs[gentau]=pr
                    
                # -- put precip
                #
                if(dogendtg or dopr or override):
                    MF.sTimer('putPrs')
                    prB.putPrs()
                    MF.dTimer('putPrs')

                # -- get trackers and compare model to obs
                # -- setTCgenProps get the maxtau for setting rtfim9 d5 tau to 132 or 120 using doTau120Rtfim9 at top
                #
                if(dosettcgen or dopr):
                    
                    tcG.setTCgenProps(gentau,dogendtg,verb=verb)
                    
                    # -- if tcG.done == -999 => no trackers available
                    if(tcG.done != -999):
                        tcG.compMtoO(dtg,gentau,dogendtg,verb=verb) 
                    
                    # -- do and put inventory; always put hash to pypdb
                    #
                    MF.sTimer('doInv-loop')
                    tcG.doInv(iV,pr,overrideInv=1)
                    MF.dTimer('doInv-loop')

                # -- bail if no tracker -- doInv always gets counts -- let the plotting proceed...
                # 20130925 -- no -- indicates the gen tracker failed
                if(tcG.done == -999 and not(bypassTrkchk) and not(overrideGA) ):  
                    print 'WWW no plotting because tcG.done: ',tcG.done,' bypassTrkchk: ',bypassTrkchk,'continue...'
                    continue

                # -- only plot if pr has a value
                #
                BMoverride=0
                if(not(overrideGA) and (doplot or doxv and (pr[2] != -999.)) ):
                    # -- PPPLLLOOOTTT - prp
                    #
                    tcG.w2PlotTcGenFld(field='prp',dostdd=1,doxv=doxv,
                                       dowindow=dowindow,doland=doland,BMoverride=BMoverride,
                                       verb=verb,override=override,quiet=quiet)
                    if(not(tcG.allreadyDone)): didPrc=didPrc+1

                    # -- PPPLLLOOOTTT - n850
                    #
                    tcG.w2PlotTcGenFld(field='n850',dostdd=1,doxv=doxv,
                                       dowindow=dowindow,doland=doland,BMoverride=BMoverride,
                                       verb=verb,override=override,quiet=quiet)
                    if(not(tcG.allreadyDone)): didPrc=didPrc+1

                    # -- PPPLLLOOOTTT - uas
                    #
                    tcG.w2PlotTcGenFld(field='uas',dostdd=1,doxv=doxv,
                                       dowindow=dowindow,doland=doland,BMoverride=BMoverride,
                                       verb=verb,override=override,quiet=quiet)
                    if(not(tcG.allreadyDone)): didPrc=didPrc+1
                    
            # -- put prs for basin
            #
            if(not(overrideGA)):
                prB.putPrs()    


        # -- iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
        #    invoverride default is 1, set to 0 if doing a single model ot single gentau-- do inventory for tcgen.php
        #
        if(ropt != 'norun'):
            MF.sTimer('doInv-putPyp')
            iV.putPyp()
            MF.dTimer('doInv-putPyp')

# -- stop the grads process
#
try:   tcGP.gaP.ga('quit')
except: None

# -- do verification
#
if(not(verioverride) and not(dogendtg)):
    MF.sTimer('all-veri')
    cmd="%s %s %s"%(pypath,dtgopt,modelopt)
    for o,a in CL.opts:
        if(o != '-c'):
            cmd="%s %s %s"%(cmd,o,a)
    
    cmd="%s -T -i -c"%(cmd)
    mf.runcmd(cmd,ropt,prefix="veri")
    MF.dTimer('all-veri')

if(not(invoverride) and not(overrideGA)):
    None
else:
    if( didPrc == 0 or (len(gentaus) <= 2 and len(models) == 1 and len(basins) == 1) or ropt == 'norun' or cycle ): invoverride=0

if(didPrc == 0):
    print 'AAALLLRRREEEAAADDDYYY done didPrc: ',didPrc
    
if(not(invoverride)):
    None
    MF.dTimer('all')
else:
    
    MF.sTimer('tcgen.inv-atend')
    if(invopt == None): invopt='all'
    MF.sTimer('tcgen.inv.js')
    # -- dtgopt sets tdtgs in makeTcgenJsInventory
    # -- if 'ops12' get all dtgs from the beginning of the year to ops12
    #
    dtgoptjs=dtgopt
    if(mf.find(dtgopt,'cur') or runInCron): dtgoptjs='ops12'
    rc=makeTcgenJsInventory(dtgoptjs,gendtgs,stmids,basins,invopt=invopt,
                            gentaus=gentaus,
                            verb=verb,ndayback=ndayback)
    # -- 20200317 -- now rsync to wxmap2
    #
    rc=rsync2Wxmap2('tcgen')
    
    MF.dTimer('tcgen.inv.js')
    MF.dTimer('tcgen.inv-atend')
    
    # -- put 'latest' to products/tcgen/latest -- only if real-time runs
    #
    chkLatest=0
    if(mf.find(dtgopt,'cur') or mf.find(dtgopt,'ops') or runInCron): chkLatest=1
    
    if(chkLatest and doLatest):
        MF.sTimer('tcgen-latest')
        cmd="%s/w2.tc.tcgen2-latest.py -X"%(CL.pydir)
        mf.runcmd(cmd,ropt)
        MF.dTimer('tcgen-latest')
        
    MF.dTimer('all')

#iV.lsKeys()

