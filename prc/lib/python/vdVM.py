from M import *
MF=MFutils()

from tcVM import *
from tcbase import gc_dist,rumhdsp,rumltlg,dist_err,FormatLat,FormatLon,GetTCName
from ATCF import AidProp

from w2methods import *

#pypofile="all.%s.%s.pyp"%(stmid,filemodel)
#pypopath="%s/%s"%(vddir,pypofile)
#PA=open(pypopath,'w')

vmecutpoints=[-30,-10,10,30]

GcDist=gc_dist
RumHS=rumhdsp
RumLL=rumltlg
CtAt=dist_err

# -- vars from ATCF needed below

StartSynHourModel={}
DtauModelTracker={}
DtauModel={}
modelsalias=['bcon']

# -- vars from VT

maxTaids=10



# -- hfip track and intensity baseline/goals
# from .doc from bob gall 20101104

hfipBaseJtwc={'pe':
              {  0:( 13.5,1429),
                 12:( 38.6,1327),
                 24:( 62.3,1199),
                 36:( 83.2,1055),
                 48:(104.8,925),
                 72:(169.2,709),
                 96:(233.3,469),
                 120:(309.0,310), # from conw 06-08
                 144:(325.9,177), # interp between 120-168
                 168:(342.7,133), # as good as 5-d JTWC in 2006-08
                 }
              }

hfipBase={'pe':
          {  0:(  7.8,818),
             12:( 30.0,741),
             24:( 49.8,663),
             36:( 69.5,586),
             48:( 89.6,518),
             72:(132.0,411),
             96:(175.2,313),
             120:(221.9,247),
             144:(266.9,177),
             168:(314.0,133), # as good as 5-d OFCL in 2003
             },
          'vme':
          {  0:( 2.2,820),
             12:( 7.7,745),
             24:(10.1,667),
             36:(11.7,590),
             48:(13.7,522),
             72:(16.0,415),
             96:(16.6,316),
             120:(17.0,250),
             144:(18.0,247),
             168:(19.0,247),
             },
          'vbias':
          {0:(0.0,820),
           12:(0.0,745),
           24:(0.0,667),
           36:(0.0,590),
           48:(0.0,522),
           72:(0.0,415),
           96:(0.0,316),
           120:(0.0,250),
           144:(0.0,250),
           168:(0.0,250),
           },
          'fcvm':
          {0:(0.0,820),
           12:(0.0,745),
           24:(0.0,667),
           36:(0.0,590),
           48:(0.0,522),
           72:(0.0,415),
           96:(0.0,316),
           120:(0.0,250),
           144:(0.0,177),
           168:(0.0,133),
           },
          }

# -- based on clp5,shf5 2006-2008 homo with ofcl/cons
#
clipBase={'pe':
          {  0:(  7.7,818),
             12:( 44.5,741),
             24:( 93.3,663),
             36:(150.9,586),
             48:(212.2,518),
             72:(317.2,411),
             96:(396.5,313),
             120:(473.0,247),
             144:(523.1,177),
             168:(553.9,133),
             },          

          #{0:(7.8,818), from OCD5 directly
          #12:(44.9,775),
          #24:(94.2,697),
          #36:(150.1,618),
          #48:(210.1,548),
          #72:(320.7,435),
          #96:(414.4,338),
          #120:(492.3,262),
          #144:(523.1,177),
          #168:(553.9,133),
          #},
          'vme':  # from James 23 apr 09 .doc
          {  0:( 2.2,820),
             12:( 8.3,745),
             24:(11.5,667),
             36:(14.2,590),
             48:(16.1,522),
             72:(17.8,415),
             96:(19.3,316),
             120:(19.3,250),
             144:(20.0,177),
             168:(20.5,133),
             },
          'vbias':
          {0:(0.0,820),
           12:(0.0,745),
           24:(0.0,667),
           36:(0.0,590),
           48:(0.0,522),
           72:(0.0,415),
           96:(0.0,316),
           120:(0.0,250),
           144:(0.0,250),
           168:(0.0,250),
           },
          'fcvm':
          {0:(0.0,820),
           12:(0.0,745),
           24:(0.0,667),
           36:(0.0,590),
           48:(0.0,522),
           72:(0.0,415),
           96:(0.0,316),
           120:(0.0,250),
           144:(0.0,250),
           168:(0.0,250),
           },
          }


def GetLF(lat,lon):
    landfrac=GetLandFrac(self.lf,lat,lon)
    return(landfrac)


def getVdFromDSss(DSss,taid,tstmid,taidsRelabel=None,verb=0):

    kk=DSss.keys()
    try:
        otaid=taidsRelabel[taid]
    except:
        otaid=taid

    # -- go through all years
    #
    for k in kk:
        vDS=DSss[k]
        #print 'kkk',k
        #print 'kkk',taid,tstmid
        #print vDS.getKeys()
        if(verb > 1):
            print 'VVVVV--- trying to get taid, tstmid: ',taid,tstmid,' k: ',k,' otaid: ',otaid,taidsRelabel
        vd=getVdFromDSs(vDS,taid,tstmid,verb=verb)
        if(vd != None):
            if(verb):
                print 'VVVVV+++ GOT taid, tstmid: ',taid,tstmid,' k: ',k,vd
            return(vd,vDS,k)

    # -- get the vDS based on stmid
    #
    if(vd == None):
        rc=getStmParams(tstmid)
        byear=rc[2]
        if(byear in kk):
            vDS=DSss[byear]
            return(None,vDS,byear)



    return(None,None,None)


def getVdsFromDSss(DSss,taids,tstmids,taidsRelabel=None,aidSources=None,verb=0):

    kk=DSss.keys()

    otaids=[]
    ostmids=[]

    vds={}

    for taid in taids:

        gtaid=taid

        # -- relabeling
        #
        if(taidsRelabel != None):
            try:
                otaid=taidsRelabel[taid]
            except:
                otaid=taid
        else:
            otaid=taid


        for tstmid in tstmids:

            # -- handle bcon -- is handled in getFinalAidsByRelabel
            #
            #if(taid == 'bcon'):
            #    gtaid=getBcon4Stmid(tstmid)

            if(taid == 'hfip'):
                vds[otaid,tstmid]=None
                continue

            try:
                ssyys=aidSources[taid]
            except:
                ssyys=[]

            if(len(ssyys) > 0):
                for ssyy in ssyys:
                    try:
                        (source,year)=ssyy.split('-')
                    except:
                        print 'EEE invalid form of setting source-year for aids...was:  ',ssyy,'should be: SSS-YYYY'
                        sys.exit()

                    vDS=DSss[source,year]
                    if(verb > 1):
                        print 'SSSSS trying to get taid, tstmid: ',taid,tstmid,' source,year: ',source,year,' otaid: ',otaid,taidsRelabel

                    vd=GetVdsFromDSs(vDS,taid,tstmid,taidsRelabel=None,returnlist=1,verb=verb)

                    if(vd != None):

                        if(verb):
                            print 'SSSSS GOT taid, tstmid: ',taid,tstmid,' source,year: ',source,year,' otaid: ',otaid

                        if(not( (otaid,tstmid) in vds.keys())):
                            vds[otaid,tstmid]=vd
                            if(verb > 1): print 'SSSSS--- adding otaid...',otaid,'tstmid: ',tstmid
                            ostmids.append(tstmid)
                            otaids.append(otaid)
                        else:
                            if(verb > 1): print 'SSSSS--- ALREADY there...',otaid,'tstmid: ',tstmid
            else:

                vd=getVdFromDSss(DSss,gtaid,tstmid,taidsRelabel=None,verb=verb)
                if(vd != None):
                    if(not( (otaid,tstmid) in vds.keys())):
                        vds[otaid,tstmid]=vd
                        if(verb > 1): print 'VVVVV---  adding otaid...',otaid,'tstmid: ',tstmid
                        ostmids.append(tstmid)
                        otaids.append(otaid)
                    else:
                        if(verb > 1): print 'VVVVV--- ALREADY there...',otaid,'tstmid: ',tstmid


        otaids=mf.uniq(otaids)
        ostmids=mf.uniq(ostmids)

    return(vds,otaids,ostmids)

def makeVdsFromAB2DSs(A2DSs,B2DSs,years,dsbdir,overrideVD,
                      taids,tstmids,taidsRelabel=None,aidSources=None,
                      doHigherOrder=1,
                      tcunits=tcunits,
                      verirule='std',
                      override=0,warn=0,
                      verb=0):

    def openV2DSs(years,dowrite=0):

        V2DSs={}

        # -- open vdeck2 
        #
        for year in years:
            dbtype='vdeck2'
            dbname="%s_%s"%(dbtype,year)
            dbfile="%s.pypdb"%(dbname)
            V2DSs[year]=DataSets(bdir=dsbdir,name=dbfile,dtype=dbtype,verb=verb,unlink=overrideVD,doDSsWrite=dowrite)

        return(V2DSs)

    def closeV2DSs(V2DSs):
        kk=V2DSs.keys()
        for k in kk:
            V2DSs[k].closeDataSet()
        return


    if(verb): warn=1

    V2DSs=openV2DSs(years,dowrite=0)

    otaids=[]
    ostmids=[]

    vds={}
    vdsPut={}

    def getVD2s(taids,tstmids):

        for taid in taids:

            didAlias=0
            if(len(taid.split(":")) == 2):
                tt=taid.split(':')
                gtaid=tt[0]
                otaid=tt[1]
                didAlias=1

                print 'WWW aliasing: ',gtaid,'to: ',otaid
            else:
                gtaid=taid
                otaid=taid

            for tstmid in tstmids:

                tyear=tstmid.split('.')[-1]
                tstmid=tstmid.upper()
                bd2=B2DSs[tyear].getDataSet(key=tstmid)
                try:
                    BT=bd2.BT
                except:
                    if(warn): print 'WWW(makeVdsFromAB2DSs.getVD2s.bd2 not there for tstmid: ',tstmid,' press...'
                    continue

                # -- handle bcon -- is handled in getFinalAidsByRelabel
                #
                #if(taid == 'bcon'):
                #    gtaid=getBcon4Stmid(tstmid)

                a2dskey="%s_%s"%(taid,tstmid)
                (ad2,a2DS,a2year)=getVdFromDSss(A2DSs,gtaid,tstmid,taidsRelabel=None,verb=verb)
                (vd2,v2DS,v2year)=getVdFromDSss(V2DSs,gtaid,tstmid,taidsRelabel=None,verb=verb)

                didNoload=0
                if(ad2 == None and (vd2 == None or override) ):
                    from adCL import Adeck2NoLoad
                    A=Adeck2NoLoad(BT)
                    AT=A.getAidTrk()                
                    if(warn): print 'NNNN-noload for: ',a2dskey
                    a2year=tstmid.split('.')[-1]
                    didNoload=1
                elif(ad2 != None):
                    AT=ad2.AT

                if(v2year == None and v2DS == None):
                    v2DS=V2DSs[a2year]

                makeVD2=0

                if(vd2 == None and ad2 != None): 
                    makeVD2=1

                elif((vd2 != None and ad2 == None and not(didAlias)) or didNoload):
                    makeVD2=0

                else:

                    atdtgs=AT.dtgs
                    btdtgs=BT.dtgs
                    vddtgs=vd2.bdtg[0]
                    vdpods=vd2.pod[0]

                    #ad2.ls()
                    #print 'qqqqqqqqqqq',len(atdtgs)
                    #sys.exit()
                    vd2testAD=0

                    nadtrks=0
                    for atdtg in atdtgs:

                        # -- test if aid dtg in btdtgs, if not, continue
                        #
                        if(not(atdtg in btdtgs)): continue

                        try:
                            adtrk=AT.atrks[atdtg]
                            adtrktaus=adtrk.keys()
                            adtrktaus.sort()
                            adtau0=adtrktaus[0]
                            adtrk=adtrk[adtau0]
                        except:
                            adtrk=[]

                        try:
                            vdpod=vdpods[vddtgs.index(atdtg)]
                        except:
                            vdpod=None

                        if(vdpod != None and vdpod < 0 and len(adtrk) > 0): vd2testAD=1
                        nadtrks=nadtrks+1


                    if(nadtrks == 0): 
                        if(vd2 == None or override): 
                            print 'WWW(vdVM.makeVdsFromAB2DSs): len(atdtgs) == 0 for tstmid: ',tstmid,' otaid: ',otaid,\
                                  ' vd2==None or override...making a vd2 with no veri vars'
                            makeVD2=1
                        else:
                            makeVD2=0
                    else:
                        makeVD2=( (vdpod == None or vd2testAD) and (didNoload == 0) )

                if(makeVD2 or (override and not(didNoload)) ):

                    MF.sTimer('mkVD2s-%s-%s'%(otaid,tstmid))
                    vd2=MakeVdeckS(BT,AT,verb=verb,doHigherOrder=doHigherOrder,
                                   tcunits=tcunits,verirule=verirule)
                    vdsPut[otaid,tstmid]=vd2
                    ##rc=putVdToDSs(v2DS,vd2,taid,tstmid)
                    MF.dTimer('mkVD2s-%s-%s'%(otaid,tstmid))


                vds[otaid,tstmid]=vd2
                ostmids.append(tstmid)
                otaids.append(otaid)


        return(vds,vdsPut,ostmids,otaids)

    (vds,vdsPut,ostmids,otaids)=getVD2s(taids, tstmids)

    if(len(vdsPut) > 0):
        # -- close and reopen with write
        closeV2DSs(V2DSs)
        V2DSs=openV2DSs(years,dowrite=1)

        kk=vdsPut.keys()
        for k in kk:
            (taid,tstmid)=k
            MF.sTimer('putVD2s-%s-%s'%(taid,tstmid))
            (vd2Dum,v2DS,v2year)=getVdFromDSss(V2DSs,taid,tstmid,taidsRelabel=None,verb=verb)
            rc=putVdToDSs(v2DS,vdsPut[k],taid,tstmid)
            MF.dTimer('putVD2s-%s-%s'%(taid,tstmid))

        closeV2DSs(V2DSs)

    otaids=mf.uniq(otaids)
    ostmids=mf.uniq(ostmids)

    return(vds,otaids,ostmids)

def lsCases(taids,cases,casedtgs,verivars,ttau=72,dobigbias=0,printSource=0,veriwarn=None,
            undef=1e20,
            filterOpts=[],doplot=0):


    kk=cases.keys()
    kk.sort()

    ovars={}
    ovars2={}
    ocards={}
    ostmids={}

    try:
        tdtgs=casedtgs[ttau,verivars[0]]
    except:
        print 'WWW no cases for ttau: ',ttau
        return(ovars,ovars2)

    for tdtg in tdtgs:

        for k in kk:

            (aid,stmid,dtg,tau,verikey)=k

            if(dtg == tdtg):

                for taid in taids:
                    if(aid == taid and tau == ttau):

                        (stmid,vmax,vvar)=cases[k]
                        MF.loadDictList(ostmids,dtg,stmid)
                        try:
                            ocards[taid,stmid,dtg]
                        except:
                            ocards[taid,stmid,dtg]=''

                        if(len(ocards[taid,stmid,dtg]) > 0):
                            #rint 'tttttttt ',taid,stmid,dtg,ocards[taid,stmid,dtg]
                            ocards[taid,stmid,dtg]="%12s %6s %6.1f"%(ocards[taid,stmid,dtg],verikey,vvar)
                            #print 'tttttttt ',ocards[taid,stmid,dtg]
                            #print 'tt ',taid,vvar,verikey
                            MF.loadDictList(ovars,taid,vvar)
                            MF.append2KeyDictList(ovars2,taid,verikey,vvar)

                        else:
                            #print 'eeeeeee ',taid,stmid,dtg,vvar
                            vdtg=mf.dtginc(dtg,ttau)
                            ocards[taid,stmid,dtg]="%12s bdtg:%s vdtg:%s  %d %s %3d %6s %6.1f"%(taid,dtg,vdtg,ttau,stmid,vmax,verikey,vvar)
                            MF.loadDictList(ovars,taid,vvar)
                            MF.append2KeyDictList(ovars2,taid,verikey,vvar)




    MF.uniqDictList(ostmids)

    doFilter=0
    for filterOpt in filterOpts:
        if(mf.find(filterOpt,'be')):
            tt=filterOpt.split(':')
            if(len(tt) == 3):
                doFilter=1
                fcerrorMax=float(tt[2])



    focards=[]

    for tdtg in tdtgs:

        tstmids=ostmids[tdtg]

        for tstmid in tstmids:

            print 
            vvars=[]
            naids=len(taids)
            for n in range(0,naids):
                taid=taids[n]

                try:
                    ocard=ocards[taid,tstmid,tdtg]
                    doprint=1
                except:
                    ocard=None
                    doprint=0

                if(ocard == None): 
                    vdtg=mf.dtginc(tdtg,ttau)
                    otaid=taid[0:9]
                    lotaid=len(otaid)
                    otaid='N'*(12-lotaid-1)+'-'+otaid
                    ocard="%12s bdtg:%s vdtg:%s  %d %s NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN"%(otaid,tdtg,vdtg,ttau,tstmid)
                    print ocard

                if(doprint):
                    tt=ocard.split()
                    fcerror=float(tt[-1])

                    if(doFilter and fcerror < fcerrorMax): 
                        print 'FFF - ',taid,tdtg,tstmid
                        continue

                    vvars.append(fcerror)

                    try:
                        vvn=vvars[n]
                    except:
                        vvn=None
                        
                    try:
                        vvnaid=vvars[naids-1]
                    except:
                        vvnaid=None

                    if(vvn == None or vvars[n] == undef):
                        ocardlast=str(ocard.split()[-1])
                        ocard=ocard.replace(ocardlast,'')
                        ocard="%s NNNNNNN"%(ocard)

                    if(vvn != None and len(tt) > 0 and vvars[n] != undef):

                        if(n <= naids-1 and naids >= 2):
                            try:
                                dvar=vvars[n]-vvars[0]
                                if(dvar != 0):
                                    ocard="%s %6.1f"%(ocard,dvar)
                                if(printSource or doplot): ocard="%s "%(ocard)
                            except:
                                None
                        
                    print ocard   
                    focards.append(ocard)

    if(doplot):

        from tcbase import PrcDirTctrkW2

        # only if running lsCases()
        #
        for focard in focards:
            tt=focard.split()
            taid=tt[0]
            dtg=tt[1]
            stmid=tt[3]

            if(mf.find(focard,'source: ')): 
                usource=tt[-1]
            else:
                print 'EEE(vdVM.lsCases() -- trying to do trkplot but has not been set up for this option...sayoonara'
                sys.exit()

            cmd="%s/w2-tc-trkplt.py %s %s.%s -S %s -X -O -M 120"%(PrcDirTctrkW2,dtg,taid,usource,stmid)
            mf.runcmd(cmd,ropt)


        sys.exit()

        if(len(taids) > 1): print

    return(ovars,ovars2)

def getOvars4Cases(taids,cases,casedtgs,verivars,ttau=72,dobigbias=0,printSource=0,veriwarn=None,
                   filterOpts=[],doplot=0):


    kk=cases.keys()
    kk.sort()
    lkk=len(kk)

    ovars2={}
    ocards={}
    ostmids={}

    print 'qqqqqqqq',casedtgs.keys()
    print 'vvvvvvvvv',verivars
    
    try:
        tdtgs=casedtgs[ttau,verivars[0]]
    except:
        print 'WWW no cases for ttau: ',ttau
        return(ovars2)

    for tdtg in tdtgs:

        for k in kk:

            (aid,stmid,dtg,tau,verikey)=k

            if(dtg == tdtg):

                for taid in taids:

                    if(aid == taid and tau == ttau):

                        (stmid,vmax,vvar)=cases[k]
                        MF.loadDictList(ostmids,dtg,stmid)
                        try:
                            ocards[taid,stmid,dtg]
                        except:
                            ocards[taid,stmid,dtg]=''

                        if(len(ocards[taid,stmid,dtg]) > 0):
                            #rint 'tttttttt ',taid,stmid,dtg,ocards[taid,stmid,dtg]
                            ocards[taid,stmid,dtg]="%12s %6s %6.1f"%(ocards[taid,stmid,dtg],verikey,vvar)
                            #print 'tttttttt ',ocards[taid,stmid,dtg]
                            #print 'tt ',taid,vvar,verikey
                            #MF.append2KeyDictList(ovars2,taid,verikey,vvar)

                        else:
                            #print 'eeeeeee ',taid,stmid,dtg,vvar
                            vdtg=mf.dtginc(dtg,ttau)
                            ocards[taid,stmid,dtg]="%12s bdtg:%s vdtg:%s  %d %s %3d %6s %6.1f"%(taid,dtg,vdtg,ttau,stmid,vmax,verikey,vvar)

                        MF.append2KeyDictList(ovars2,taid,verikey,(vvar,vmax))

    return(ovars2)



#llllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll
# local methods
#

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




def filterListsbyTau(lists,taus,taids,verikey,fixtau):

    olists=copy.copy(lists)
    itaus=taus
    for taid in taids:
        key=(taid,fixtau,verikey)
        fixlist=lists[key]
        fL=VdList(fixlist,key)
        for tau in itaus:
            ilist=lists[taid,tau,verikey]
            iL=VdList(ilist,key)
            ifL=VdLists(iL,fL)
            ifL.compLists()
            ifL.L1.dict2list()
            olists[taid,tau,verikey]=ifL.L1.list

    return(olists)


def filterListsBbyTau(listsB,taus,taids,tstmids,verikey,fixtau):

    olistsB=copy.copy(listsB)
    itaus=taus
    for taid in taids:
        for tstmid in tstmids:
            key=(taid,tstmid,fixtau,verikey)
            fixlist=listsB[key]
            fL=VdList(fixlist,key)
            for tau in itaus:
                ilist=listsB[taid,tstmid,tau,verikey]
                iL=VdList(ilist,key)
                ifL=VdLists(iL,fL)
                ifL.compLists()
                ifL.L1.dict2list()
                olistsB[taid,tstmid,tau,verikey]=ifL.L1.list

    return(olistsB)



def filterListsbyDtgs(lists,filterdtgopt,taids,itaus,verikey):

    fdtgs=mf.dtg_dtgopt_prc(filterdtgopt)

    ##     if(len(dtgs) > 1):
    ##         fdtgs=[dtgs[0],dtgs[-1]]
    ##     else:
    ##         fdtgs=dtgs

    for taid in taids:
        for itau in itaus:
            key=(taid,itau,verikey)
            fixlist=lists[key]
            fL=VdList(fixlist,key)
            fL.filterDtgs(fdtgs)
            fL.dict2list()
            lists[taid,itau,verikey]=fL.list



def filterListsbySynopticHour(lists,fopt,taids,itaus,verikey):

##     if(len(dtgs) > 1):
##         fdtgs=[dtgs[0],dtgs[-1]]
##     else:
##         fdtgs=dtgs

    for taid in taids:
        for itau in itaus:
            key=(taid,itau,verikey)
            if(taid != 'hfip' and taid != 'hfip20' and taid != 'hclp' and taid != 'hfipj'):
                fixlist=lists[key]
                fL=VdList(fixlist,key)
                fL.filterSynoptic(fopt)
                fL.dict2list()
                lists[taid,itau,verikey]=fL.list

def filterListsbySynopticHourStorms(listsB,fopt,taids,tstmids,itaus,verikey):

##     if(len(dtgs) > 1):
##         fdtgs=[dtgs[0],dtgs[-1]]
##     else:
##         fdtgs=dtgs

    for taid in taids:
        for tstmid in tstmids:
            for itau in itaus:  
                key=(taid,tstmid,itau,verikey)
                if(taid != 'hfip' and taid != 'hfip20' and taid != 'hclp' and taid != 'hfipj'):
                    fixlist=listsB[key]
                    fL=VdList(fixlist,key)
                    fL.filterSynoptic(fopt)
                    fL.dict2list()
                    listsB[taid,tstmid,itau,verikey]=fL.list


def lagListsbyTau(lists,taids,verikey):

    otaids=[]
    ltaus=[12,24,48,72]
    ltaus=[12]
    for taid in taids:
        otaids.append(taid)
        taid2=taid+'LAG'
        otaids.append(taid2)
        for ltau in ltaus:

            key1=(taid,ltau,verikey)
            ilist1=lists[key1]
            iL=VdList(ilist1,key1)
            iL2=iL.copy()
            i12L=VdLists(iL,iL2)
            i12L.lagLists(dtau=12)

            olist1=i12L.L2.list
            olist2=i12L.L2.list

            key1=(taid,ltau,verikey)
            lists[key1]=olist1

            key2=(taid2,ltau,verikey)
            lists[key2]=olist2

    otaids=self.uniq(otaids)
    return(otaids,lists,ltaus)


def getVerivars(ptype):

    verivars=[
        ('uuu','mean','uuu')
    ]

    if(ptype == 'pe' or ptype == 'pe-line'):
        verivars=[
            ('pe','mean','pe'),
        ]

    elif(ptype == 'pe-frac'):
        verivars=[
            ('pe','mean','pe'),
        ]

    elif(ptype == 'pe-pcnt'):
        verivars=[
            ('pe','mean','pe'),
        ]

    elif(ptype == 'pe-imp' or ptype == 'pe-imps'):
        verivars=[
            ('pe','mean','pe'),
        ]

    elif(ptype == 'fe-imp' or ptype == 'fe-imps' or ptype == 'fe-norm'):
        verivars=[
            ('fe','mean','fe'),
        ]

    elif(ptype == 'fe' or ptype == 'fe-line'):
        verivars=[
            ('fe','mean','fe'),
        ]

    elif(ptype == 'fe0'):
        verivars=[
            ('fe0','mean','fe0'),
        ]

    elif(ptype == 'te'):
        verivars=[
            ('te','mean','te'),
        ]

    elif(ptype == 'pe-fe'):
        verivars=[
            ('pe','mean','pe'),
            ('fe','mean','fe'),
        ]

    elif(ptype == 'spe'):
        verivars=[
            ('spe','mean','spe'),
        ]

    elif(ptype == 'rmspe'):
        verivars=[
            ('pe','mean','pe'),
            ('pe','sigma','rmspe'),
        ]

    elif(ptype == 'gainxype'):
        verivars=[
            ('pe','gainxy','pe'),
        ]

    elif(ptype == 'gainxyfe'):
        verivars=[
            ('fe','gainxy','fe'),
        ]

    elif(ptype == 'gainxyte'):
        verivars=[
            ('te','gainxy','te'),
        ]
        
    elif(ptype == 'gainxyfe0'):
        verivars=[
            ('fe,fe0','mean','gainfe0'),
        ]

    elif(ptype == 'pod' or ptype == 'pod-line'):
        verivars=[
            ('pod','mean','pod'),
        ]

    elif(ptype == 'gainxyvmax'):
        verivars=[
            ('vme','gainxyvmax','vme'),
        ]

    elif(ptype == 'vbias'):
        verivars=[
            ('vme','mean','vbias'),
            ('vme','amean','vme'),
            ('fcvmax','mean','fcvm'),
        ]

    elif(ptype == 'nice'):
        verivars=[
            ('nice','amean','nice'),
            ('niceb','mean','niceb'),
        ]

    elif(ptype == 'pbias'):
        verivars=[
            ('pmine','mean','pbias'),
            ('pmine','amean','pmine'),
            ('fcpmin','mean','fcpmin'),
            ('btpmin','mean','btpmin'),
        ]

    elif(ptype == 'gainxyvbias'):
        verivars=[
            ('vme','gainxyvbias','vbias'),
            ('vme','gainxyvbias','vme'),
        ]

    elif(ptype == 'vmxmn'):
        verivars=[
            ('fcvmax','mean','fcvm'),
            ('btvmax','mean','btvm'),
        ]

    elif(ptype == 'r34e'):
        verivars=[
            ('r34e' ,'mean','r34e' ),
            ('r34bt','mean','r34bt'),
            ('r34fc','mean','r34fc'),
        ]   

    elif(ptype[0:2] == 'ls'):
        verivars=[
            ('pe','mean','pe'),
            ('cte','mean','cte'),
            ('ate','mean','ate'),
            ('btlat','mean','btlat'),
            ('btlon','mean','btlon'),
            ('btvmax','mean','btvmax'),
            ('tcflags','mean','tcflags'),
            ('vme','mean','vbias'),
            ('vme','amean','vme'),
            ('fcvmax','mean','fcvm'),
            ('pod','mean','pod'),
            ('vflag','mean','vflag'),
            ('bdtg','mean','bdtg'),   # -- get bdtg from VdeckS obj -- mod mfbase.SimpleListStats() to handle strings: val=undef
        ]
        doprint=0

    elif(ptype == 'pbetter'):
        verivars=[
            ('pe',ptype,ptype),
        ]

    return(verivars)


def getStats(ptype,taus,taids,tstmids,vds,
             B2DSs=None,
             filterdtgopt=None,
             tableReverse=0,
             doland=0,
             maxlandFrac=0.8,
             btMinLand=35.0,
             printRunOnly=0,
             veriwarn=None,
             filterOpts=[],
             overrideNL=0,
             doBystorm=0,
             dohomo=1,
             forcehomo=0,
             warn=0,
             verb=0,
             diag=1,
             lsopt=0,
             w2=None,
             doplotBE=0,
             override=0,
             doprintOstat=1,
             ):

    from vdCL import VdeckSAnl,SumStats
    from adCL import AdeckNoLoad

    pdtgs=None
    if(filterdtgopt != None): pdtgs=mf.dtg_dtgopt_prc(filterdtgopt)

    def getFilterOptBE(filterOpts):

        doListFilt=0
        filtTaus=[]
        filtErrs={}

        for filterOpt in filterOpts:

            if(mf.find(filterOpt,'be0') or mf.find(filterOpt,'be12')):
                tt=filterOpt.split(':')
                if(len(tt) == 2):
                    doListFilt=1
                    filtErr=float(tt[1])

                    if(tt[0] == 'be0'): 
                        filtTaus=[0]
                        filtErrs={ 0:filtErr,
                                   }

                    elif(tt[0] == 'be12'): 
                        filtTaus=[0,12]
                        filtErrs={ 0:filtErr*0.75,
                                   12:filtErr,
                                   }

        return(doListFilt,filtTaus,filtErrs)


    def dofilterListsbyTau(filterOpts,vlists,taus,taids,verikey):

        for filterOpt in filterOpts:

            if(mf.find(filterOpt,'tau')):

                lf=len(filterOpt)
                try:
                    fixtau=int(filterOpt[lf-3:])
                except:
                    print 'EEE invalid filterOpt: ',filterOpt,' for tau filtering tauNNN'
                    sys.exit()

                print 'IIIIIIIIIIIIII filtertaus, fixtau: ',fixtau
                vlists=filterListsbyTau(vlists,taus,taids,verikey,fixtau=fixtau)

        return(vlists)

    def dofilterListsBbyTau(filterOpts,vlistsB,taus,taids,tstmids,verikey):

        for filterOpt in filterOpts:

            if(mf.find(filterOpt,'tau')):

                lf=len(filterOpt)
                try:
                    fixtau=int(filterOpt[lf-3:])
                except:
                    print 'EEE invalid filterOpt: ',filterOpt,' for tau filtering tauNNN'
                    sys.exit()

                print 'IIIIIIIIIIIIII BBBBBBBBBBBB filtertaus, fixtau: ',fixtau
                vlistsB=filterListsBbyTau(vlistsB,taus,taids,tstmids,verikey,fixtau=fixtau)

        return(vlistsB)


    ostats={}
    allstats={}
    ostatsB={}
    allstatsB={}
    
    # -- hold stats by vvar (verivar from verivars)
    #
    allstatsVar={}


    # -- get vdeck anl object with getLF
    #
    vdA=VdeckSAnl()


    verivars=getVerivars(ptype)

    # -- take taids and copy to itaids so we can override with the hfipBase dic later
    #    forces calc using first model
    #

    itaids=copy.deepcopy(taids)

    # -- when getting errors -- remove hfip|hfip20
    #
    try:     itaids.remove('hfip')
    except:  None

    try:     itaids.remove('hfipj')
    except:  None

    try:     itaids.remove('hfip20')
    except:  None

    try:     itaids.remove('hclp')
    except:  None


    vlists={}
    vlistsB={}
    
    stats={}
    statsB={}

    cases={}
    casedtgs={}    
    
    casesBT={}

    # -- collect filter cases
    #
    filtCases={}
    filtStorms={}
    filtDtgs={}
    filtTauErrs={}

    keyBs=[]

    MF.sTimer('make lists ---- ')

    # -- get BE filteropts
    #
    (doListFilt,filtTaus,filtErrs)=getFilterOptBE(filterOpts)

    # -- get BTs
    #
    BTs={}
    for tstmid in tstmids:
        
        BTs[tstmid]=None
        
        if(B2DSs != None):
            rc=getStmParams(tstmid)
            year=rc[2]
            bds=B2DSs[year]
            bd2=B2DSs[year].getDataSet(key=tstmid)
            BT=bd2.BT.btrk
            BTs[tstmid]=BT
    

    for n in range(0,len(verivars)):

        vv=verivars[n]

        vvars=vv[0].split(',')
        
        nvvars=len(vvars)
        
        for nvv in range(0,nvvars):
            
            vvar=vvars[nvv]
    
            veristat=vv[1]
            verikey=vv[2]
    
            # -- collect lists of vvars
            #
            for tau in taus:
    
                errors={}
                errorsB={}
    
                for taid in itaids:
    
                    for tstmid in tstmids:

                        try:
                            vd=vds[taid,tstmid]
                        except:
                            vd=None
                            print 'WWW(getStats) vd=None'
    
                        if(vd == None):
                            continue
    
                        vdH=vd
    
                        # -- filter list
                        #
                        vlist=vd.GetVDVarlist(vvar,tau,verb=0)
                        
                        # -- LLLLLLLLLL land filter, works like in ga2.py if 0, then filter out over-land points
                        #
                        if(doland == 0):
    
                            listBTlat=vd.GetVDVarlist('btlat',tau)
                            listBTlon=vd.GetVDVarlist('btlon',tau)
    
                            for n in range(0,len(vlist)):
                                element=vlist[n]
                                key=element[0]
                                err=element[1]
                                (veriflag,dtg,stmid,vmax)=key
    
                                lat=listBTlat[n][1]
                                lon=listBTlon[n][1]
    
                                if(veriflag):
    
                                    lf=vdA.GetLF(lat,lon)

                                    if(lf >= maxlandFrac and vmax <= btMinLand):
                                        nveriflg=0
                                        undeperr=1e20
                                        # -- set the flag and err to undef
                                        #
                                        element=[[nveriflg,dtg,stmid,vmax],undeperr]
                                        vlist[n]=element
    
    
                        # -- FFFFFFFFFFFF filter list by filtdtgs
                        #
                        if(doListFilt):
    
                            for tt in vlist:
                                key=tt[0]
                                err=tt[1]
                                dtg=key[1]
                                stmid=key[2]
                                if(tau in filtTaus and err != 1e20 and err >= filtErrs[tau]):
                                    MF.appendDictList(filtDtgs,taid,dtg)
                                    MF.appendDictList(filtTauErrs,taid,(tau,stmid,err))
    
                            nlist=len(vlist)
                            for n in range(0,nlist):
                                element=vlist[n]
                                key=element[0]
                                err=element[1]
                                (veriflag,dtg,stmid,vmax)=key
    
                                try:
                                    filtdtgs=filtDtgs[taid]
                                except:
                                    filtdtgs=None
    
                                if(filtdtgs != None and (dtg in filtdtgs) ):
                                    if(veriflag):
                                        MF.append2KeyDictList(filtCases,taid,tau,(dtg,stmid,err))
                                    nveriflg=0
                                    undeperr=1e20

                                    # -- set the flag and err to undef
                                    #
                                    element=[[nveriflg,dtg,stmid,vmax],undeperr]
                                    vlist[n]=element
    
                        vd.addList2DictList(errors,taid,vlist)
    
                        # -- make lists by stmid
                        #
                        keyB=(taid,tstmid)
                        vd.addList2DictList(errorsB,keyB,vlist)
                        keyBs.append(keyB)
    
                if(len(itaids) > 1 and dohomo):
    
                    errors=vdH.HomoVDdics(errors,itaids,tstmid,tau,forcehomo=forcehomo,verb=verb)
    
                    # -- homo by stmid
                    #
                    errorsB=vdH.HomoVDdics(errorsB,itaids,tstmid,tau,
                                           tstmids=tstmids,
                                           forcehomo=forcehomo,verb=verb)
    
    
                for taid in itaids:
                    try:
                        vlist=errors[taid]
                    except:
                        vlist=[]
                    vlists[taid,tau,verikey]=vlist
                    
                for taid in itaids:
                    for tstmid in tstmids:
                        try:
                            vlist=errorsB[taid,tstmid]
                        except:
                            vlist=[]
    
                        vlistsB[taid,tstmid,tau,verikey]=vlist
    
    
    
            # make list of cases by tau
            #
            vlists=dofilterListsbyTau(filterOpts,vlists,taus,taids,verikey)
            vlistsB=dofilterListsBbyTau(filterOpts,vlistsB,taus,taids,tstmids,verikey)
    
            if(filterdtgopt != None):
                rc=filterListsbyDtgs(vlists,filterdtgopt,taids,taus,verikey)
    
            # -- added VD.filterSynop to filter by method
            #
            for filterOpt in filterOpts:
                if(filterOpt[0] == 'z'):
                    fopt=filterOpt[1:]
                    rc=filterListsbySynopticHour(vlists,fopt,taids,taus,verikey)
                    rc=filterListsbySynopticHourStorms(vlistsB,fopt,taids,tstmids,taus,verikey)
    
    
    
            #(taids,lists,taus)=lagListsbyTau(lists,taids,verikey)
            #taus=[24]
    
            # do the stats on the lists
            #
            if(diag): MF.sTimer('stats from lists')
            for tau in taus:
                fixtaid=taids[-1]
                fixvvar=None
                if(nvvars > 1 and nvv == nvvars-1): fixvvar=vvars[0]

                if(len(tstmids) > 0 and doBystorm):
                    rc=getOstats(ptype,vlistsB,tau,taids,vvar,verikey,veristat,stats,allstats,ostats,
                                 allstatsVar,
                                 tstmids=tstmids,
                                 fixtaid=fixtaid,fixvvar=fixvvar,
                                 doprint=doprintOstat,doBystorm=doBystorm,veriwarn=veriwarn,verb=verb)
                    
            for tau in taus:
                fixtaid=taids[-1]
                rc=getOstats(ptype,vlists,tau,taids,vvar,verikey,veristat,stats,allstats,ostats,
                             allstatsVar,
                             fixtaid=fixtaid,fixvvar=fixvvar,
                             doprint=doprintOstat,doBystorm=doBystorm,veriwarn=veriwarn,verb=verb)

    
    
    
            # -- ffffffffffffffffffffffffffffffffffff - filtercases
            for taid in itaids:
                for tau in taus:
                    try:
                        tt=filtCases[taid][tau]
                    except:
                        tt=None
    
                    if(tt != None):
                        for t in tt:
                            MF.appendDictList(filtStorms,taid,(t[1],t[0]))
    
            filtStorms=MF.uniqDict(filtStorms)
    
            # -- print atcf style stats
            #
            if(ptype[0:2] != 'ls'):
                verikeys=getVerikeys(allstats,ptype)
                rc=printStats(taids,taus,allstats,ptype,
                              w2=w2,
                              doplotBE=doplotBE,
                              override=override,
                              filtCases=filtCases,
                              filtStorms=filtStorms,
                              filtDtgs=filtDtgs,
                              filtTauErrs=filtTauErrs,
                              )
            if(diag): MF.dTimer('stats from lists')
    
    
            # collect cases
            #
            for taid in itaids:
                for tau in taus:
                    ll=vlists[taid,tau,verikey]
                    ll.sort()
                    
                    #print 'ASDFASDF',taid,tau,'ll:',len(ll),len(btlt),len(btln)
    
                    for n in range(0,len(ll)):
                        l=ll[n]
                        vflag=l[0][0]
                        vflagtest=(vflag >= 1)
                        if(veriwarn != None): vflagtest=(vflag == 2)
                        if(vflagtest):
                            dtg=l[0][1]
                            stmid=l[0][2]
                            vmax=l[0][3]
                            vvar=l[1]
                            try:
                                casedtgs[tau,verikey].append(dtg)
                            except:
                                casedtgs[tau,verikey]=[]
                                casedtgs[tau,verikey].append(dtg)
    
                            cases[taid,stmid,dtg,tau,verikey]=(stmid,vmax,vvar)
                            vdtg=mf.dtginc(dtg,tau)
                            
                            # -- add BT to cases
                            #
                            blat=blon=-999.
                            try:
                                bt=BTs[stmid][vdtg]
                                blat=bt[0]
                                blon=bt[1]
                            except:
                                None

                            casesBT[taid,stmid,dtg,tau,verikey]=(stmid,blat,blon,vmax,vvar)
    
            for tau in taus:
                try:    casedtgs[tau,verikey]=mf.uniq(casedtgs[tau,verikey])
                except: continue
    
    
            # -- reinit to get properties
            #
            
            ss=SumStats(taids,tstmids,
                        verivars[0],ostats,
                        cases,casedtgs)
            
            ostatsB=ostats
            
            rc=(ss,verivars[0],ostats,ostatsB,allstats,allstatsB,cases,casedtgs,
                casesBT,
                filtStorms,filtCases,filtDtgs,filtTauErrs)
    
    
    MF.dTimer('make lists ---- ')


    dolist=0
    if(dolist):
        kk=vlistsB.keys()
        for k in kk:
            print 'kkkkkkkkkkkk ',k,' listsB: '
            if(k[2] == 0):
                tt=vlistsB[k]
                for t in tt:
                    print 'ttttttttt ',t,t[1]

    # -- new ptype -- ls lllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll
    #
    if(ptype[0:2] == 'ls'):
        dspltable='pe'
        #-- experimental display btvmax and fcvmax; default is 'pe'
        if(mf.find(ptype,'vmax')): dspltable='vmax'

        rcls=lsStmStat(taids,tstmids,taus,vlistsB,
                       pdtgs=pdtgs,
                       tableReverse=tableReverse,
                       dspltable=dspltable,     
                       lsopt=lsopt,
                       dohomo=dohomo,
                       printRunOnly=printRunOnly,
                       veriwarn=veriwarn)


    return(rc)


def getOstats(ptype,vlists,tau,taids,vvar,verikey,veristat,stats,allstats,ostats,
              allstatsVar,
              tstmids=[],fixtaid=None,
              fixvvar=None,
              veriwarn=None,
              doBystorm=0,
              verb=0,
              doprint=1):


    if(verikey == 'tcflags'): return

    nstms=len(tstmids)
    nstmids=1
    if(nstms > 0): nstmids=nstms
    
    for ns in range(0,nstmids):

        if(fixtaid == 'hfip'):
            (mean,n)=hfipBase[verikey][tau]
            (meanfix,ameanfix,sigmafix,maxfix,minfix,nfix,ptl25fix,medianfix,ptl75fix,ptl90fix)=(mean,mean,0.0,mean,mean,n,mean,mean,mean,mean)
        
        elif(fixtaid == 'hfipj'):
            (mean,n)=hfipBaseJtwc[verikey][tau]
            (meanfix,ameanfix,sigmafix,maxfix,minfix,nfix,ptl25fix,medianfix,ptl75fix,ptl90fix)=(mean,mean,0.0,mean,mean,n,mean,mean,mean,mean)
        
        elif(fixtaid == 'hfip20'):
            (mean,n)=hfipBase[verikey][tau]
            mean=mean*0.80
            (meanfix,ameanfix,sigmafix,maxfix,minfix,nfix,ptl25fix,medianfix,ptl75fix,ptl90fix)=(mean,mean,0.0,mean,mean,n,mean,mean,mean,mean)
        
        elif(fixtaid == 'hclp'):
            (mean,n)=clipBase[verikey][tau]
            (meanfix,ameanfix,sigmafix,maxfix,minfix,nfix,ptl25fix,medianfix,ptl75fix,ptl90fix)=(mean,mean,0.0,mean,mean,n,mean,mean,mean,mean)

        else:
            
            if(nstms > 0):
                listfix=vlists[fixtaid,tstmids[ns],tau,verikey]
            else:
                listfix=vlists[fixtaid,tau,verikey]
                
            if(veristat != 'pbetter'):
                rcfix=SimpleListStats(listfix,verb=verb,undef=-999,flagval=veriwarn)
                (meanfix,ameanfix,sigmafix,maxfix,minfix,nfix,ptl25fix,medianfix,ptl75fix,ptl90fix)=rcfix
            else:
                None


        for taid in taids:

            #if(taids.index(taid) == 0 and (nstmids > 1 and doBystorm)): print

            if(taid == 'hfip'):
                (mean,n)=hfipBase[verikey][tau]
                (mean,amean,sigma,maxv,minv,n,ptl25,median,ptl75,ptl90)=(mean,mean,0.0,mean,mean,n,mean,mean,mean,mean)
            elif(taid == 'hfipj'):
                (mean,n)=hfipBaseJtwc[verikey][tau]
                (mean,amean,sigma,maxv,minv,n,ptl25,median,ptl75,ptl90)=(mean,mean,0.0,mean,mean,n,mean,mean,mean,mean)
            elif(taid == 'hfip20'):
                (mean,n)=hfipBase[verikey][tau]
                mean=mean*0.80
                (mean,amean,sigma,maxv,minv,n,ptl25,median,ptl75,ptl90)=(mean,mean,0.0,mean,mean,n,mean,mean,mean,mean)
            elif(taid == 'hclp'):
                (mean,n)=clipBase[verikey][tau]
                (mean,amean,sigma,maxv,minv,n,ptl25,median,ptl75,ptl90)=(mean,mean,0.0,mean,mean,n,mean,mean,mean,mean)
            else:
                if(nstms > 0):
                    vlist=vlists[taid,tstmids[ns],tau,verikey]
                else:
                    vlist=vlists[taid,tau,verikey]

                rc=SimpleListStats(vlist,verb=verb,undef=-999,flagval=veriwarn)
                (mean,amean,sigma,maxv,minv,n,ptl25,median,ptl75,ptl90)=rc

            if(nstms > 0):
                stats[taid,tstmids[ns],tau]=(mean,amean,sigma,n,ptl25,median,ptl75,ptl90)
            else:
                stats[taid,tau]=(mean,amean,sigma,n,ptl25,median,ptl75,ptl90)

            if(fixvvar != None and mf.find(verikey,'gain')):
    
                if(nstms > 0):
                    meanfix=allstatsVar[taid,tau,tstmids[ns],fixvvar][0][0]
                else:
                    meanfix=allstatsVar[taid,tau,fixvvar][0][0]
                    
                if(meanfix == 0.0):
                    gain=0.0
                else:
                    if(tau == 0):
                        #meanfix=15.0
                        meanfix=meanfix
                    gain=((meanfix-mean)/meanfix)*100.0

                ostat=(gain,n)

            elif(veristat == 'mean'):    ostat=(mean,n)
            
            elif(veristat == 'amean'): ostat=(amean,n)
            
            elif(veristat == 'sigma'): ostat=(sigma,n)

            elif(veristat == 'gainxy'):
                
                if(meanfix == 0.0):
                    gain=0.0
                else:
                    if(tau == 0 and (verikey == 'pe' or verikey == 'fe') ): 
                        #meanfix=15.0
                        meanfix=meanfix

                    gain=((meanfix-mean)/meanfix)*100.0

                # -- handle tau0 for gainxy
                #
                if(tau == 0 and (verikey != 'pe' and verikey != 'fe')):
                    gain=0.0
                    mean=amean=sigma=maxv=minv=-999
                    n=0
                
                # -- undef meanfix
                #
                if(meanfix == undef):
                    gain=0.0
                    mean=amean=sigma=maxv=minv=-999
                    n=0
                    
                ostat=(gain,n)

            elif(veristat == 'gainxyvbias'):

                if(tau == 0):
                    gain=0.0
                elif(amean > 0.0):
                    gain=(abs(mean)/amean)*100.0
                else:
                    gain=0.0
                ostat=(gain,n)
                
            elif(veristat == 'gainxyvmax'):
                if(tau == 0): 
                    gain=0.0
                elif(ameanfix == 0):
                    print 'EEE(vdVM.getOstats): tau: ',tau,'taid: ',taid,'veristat: ',veristat,' ameanfix = 0!!!'
                    sys.exit()
                else:
                    gain=((ameanfix-amean)/ameanfix)*100.0
                if(tau == 0): gain=0.0
                ostat=(gain,n)
                
            elif(veristat == 'pbetter'):
                if(taid != fixtaid):
                    (pstat1,pstat2,npstat)=listComp(vlist,listfix,method='pbetter')
                    ostat=(pstat1,n)
                else:
                    ostat=(pstat2,n)
            else:
                print 'EEEEEEEEEEE in getOstats, invalid veristat: ',veristat
                sys.exit()

            # -- PPPPPPPPPPPPP -- printing
            #
            #print 'PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP tau: ',tau,'taid: ',taid,' ns: ',ns,nstms,'by: ',doBystorm,'doprint: ',doprint

            if(nstms > 0):

                allstats[taid,tstmids[ns],tau,verikey]=(ostat,mean,amean,sigma,maxv,minv,n,ptl25,median,ptl75,ptl90)
                allstats['curkey']=verikey
                allstatsVar[taid,tstmids[ns],tau,vvar]=(ostat,mean,amean,sigma,maxv,minv,n,ptl25,median,ptl75,ptl90)
                allstatsVar['curkey']=vvar
                Nostat=(ostat[0],ostat[1],minv,ptl25,median,ptl75,ptl90,maxv)
                ostats[taid,tstmids[ns],tau,verikey]=Nostat
                if(doBystorm and doprint): printOstatB(allstats,taid,tstmids[ns],tau,verikey)

            else:
                allstats[taid,tau,verikey]=(ostat,mean,amean,sigma,maxv,minv,n,ptl25,median,ptl75,ptl90)
                allstats['curkey']=verikey
                allstatsVar[taid,tau,vvar]=(ostat,mean,amean,sigma,maxv,minv,n,ptl25,median,ptl75,ptl90)
                allstatsVar['curkey']=vvar
                Nostat=(ostat[0],ostat[1],minv,ptl25,median,ptl75,ptl90,maxv)
                ostats[taid,tau,verikey]=Nostat
                if(doprint): printOstat(allstats,taid,tau,verikey)
    
    # -- convert pe to fraction of mean by storm
    #
    if((doBystorm and nstmids > 1) and (
        ptype == 'pe-frac' or ptype == 'pe-pcnt' or 
        ptype == 'pe-imp' or ptype == 'pe-imps' or 
        ptype == 'fe-imp' or ptype == 'fe-imps' or
        ptype == 'fe-norm'
    )
       ):
      
        peGfs={
            0:16.2,12:26.5,24:41.1,36:54.4,48:68.3,72:108.2,96:150.5,120:198.3,
        }
        
        feGfs={
            0:4.4,12:8.8,24:14.5,36:21.1,48:28.5,72:50.7,96:82.8,120:133.6,
        }
      
        
        smmnns={}
        snns={}
        nns={}
        
        for taid in taids:

            smmnns[taid]=0.0
            snns[taid]=0
            nns[taid]=0

            for tstmid in tstmids:
                kk=(taid,tstmid,tau,verikey)
                rc=ostats[kk]
                mm=rc[0]
                nn=rc[1]
                if(mm != -999.):
                    snns[taid]=snns[taid]+nn
                    if(ptype == 'pe-frac'):
                        smmnns[taid]=smmnns[taid]+mm*nn
                    elif(ptype == 'pe-pcnt'):
                        smmnns[taid]=smmnns[taid]+nn
                    elif(ptype == 'pe-imp' or ptype == 'pe-imps' or 
                         ptype == 'fe-imp' or ptype == 'fe-imps' or
                         ptype == 'fe-norm'):
                        smmnns[taid]=smmnns[taid]+mm*nn
                        nns[taid]=nns[taid]+1
                        
                    
        for taid in taids:

            totFrac=0.0
            
            for tstmid in tstmids:
                
                kk=(taid,tstmid,tau,verikey)
                rc=ostats[kk]
                
                # -- grand mean accross storms
                #
                gmn=smmnns[taid]
                gnn=snns[taid]
                gmn=gmn/gnn
                fenorm=peGfs[tau]/feGfs[tau]
                
                mm=rc[0]
                nn=rc[1]
                
                if(mm != -999.):
                    
                    sc=(nn*1.0/snns[taid]*1.0)

                    if(ptype == 'pe-frac'):
                        frac=((mm*nn)/smmnns[taid])*100.0
                        
                    elif(ptype == 'pe-pcnt'):
                        frac=(nn/smmnns[taid])*100.0

                    elif(ptype == 'pe-imp' or ptype == 'fe-imp'):
                        frac=((gmn-mm)/gmn)*100.0
                        
                    elif(ptype == 'pe-imps' or ptype == 'fe-imps'):
                        frac=((gmn-mm)/gmn)*sc*100.0
                        totFrac=totFrac+frac

                    elif(ptype == 'fe-norm'):
                        frac=mm*fenorm
                        
                    ll=list(rc)
                    ll[0]=frac
                    tt=tuple(ll)
                    ostats[kk]=tt
                    
            if(ptype == 'fe-imps' or ptype == 'pe-imps'):
                print 'FFF for taid: ',taid,' totFrac: ',totFrac
                    

    return


def getAllTaus(tauopt):

    tt=tauopt.split(',')
    ttd=tauopt.split('-')
    
    if(tauopt == '0-72'):
        taus=[0,24,48,72]
        
    elif(tauopt == '48-72'):
        taus=[48,72]
            
    elif(tauopt == '24-120'):
        taus=[0,24,48,72,96,120]

    elif(tauopt == '72-120'):
        taus=[0,72,96,120]
        
    elif(len(ttd) == 2 and int(ttd[0]) == 0):
        lasttau=int(ttd[1])
        if(lasttau == 24):
            taus=[0,12,24]
        elif(lasttau == 36):
            taus=[0,12,24,36]
        elif(lasttau == 48):
            taus=[0,12,24,36,48]
        elif(lasttau == 72):
            taus=[0,12,24,36,48,72]
        elif(lasttau == 96):
            taus=[0,12,24,36,48,72,96]
        elif(lasttau == 120):
            taus=[0,12,24,36,48,72,96,120]
        elif(lasttau == 168):
            taus=[0,12,24,36,48,72,96,120,144,168]
        else:
            taus=[0,12,24,36,48,72,96,120]
    else:
        itaus=tt
        taus=[]
        for itau in itaus:
            taus.append(int(itau))

        taus=mf.uniq(taus)
        taus.sort()

    return(taus)


def getFinalAidsByRelabel(getaids,aidSources={},verb=0):

    # -- relabeling
    #
    taidsRelabel={}
    getaidsFinal=[]
    taidsFinal=[]

    if(getaids == None):
        getaidsFinal=getaids
        return(getaidsFinal,taidsFinal,taidsRelabel,aidSources)

    for getaid in getaids:
        if(getaid == 'bcon'):
            getaids.append('conu:bcon')
            getaids.append('tvcn:bcon')
            getaids.append('conw:bcon')

    for getaid in getaids:

        tt=getaid.split(':')
        getaidsFinal.append(tt[0])

        # -- test for SSS-YYYY format
        #
        settaid=1
        if(mf.find(str(aidSources[getaid]),'-')): settaid=0
        if(settaid): aidSources[tt[0]]=aidSources[getaid]

        taidsRelabel[tt[0]]=tt[0]

        # -- avoid dups when relabeling
        #
        if(len(tt) == 2):
            taidsRelabel[tt[0]]=tt[1]
            if(not(tt[1] in taidsFinal)): taidsFinal.append(tt[1])
        else:
            if(not(tt[0] in taidsFinal)): taidsFinal.append(tt[0])


    if(verb):

        for getaid in getaidsFinal:
            print 'GGGG ',getaid,taidsRelabel[getaid]
        for taid in taidsFinal:
            print 'TTT ',taid

    return(getaidsFinal,taidsFinal,taidsRelabel,aidSources)




def printOstat(allstats,taid,tau,verikey):
    (ostat,mean,amean,sigma,maxv,minv,n,p25,med,p75,p90)=allstats[taid,tau,verikey]
    print 'SSSSSHHHHH %18s %3d %10s'%(taid,tau,verikey),' %10.1f n: %3d'%(ostat[0],ostat[1]),\
          '   m,a,s,mn,p25,med,p75,p90,mx: %6.1f %6.1f %6.1f  Dist: %6.1f %6.1f  MD: %6.1f %6.1f %6.1f %6.1f'%\
          (mean,amean,sigma,minv,p25,med,p75,p90,maxv)

def printOstatB(allstatsB,taid,tstmid,tau,verikey):
    (ostat,mean,amean,sigma,maxv,minv,n,p25,med,p75,p90)=allstatsB[taid,tstmid,tau,verikey]
    print 'SSSSSBBBBB %8s%10s %3d %10s'%(tstmid,taid,tau,verikey),' %10.1f n: %3d'%(ostat[0],ostat[1]),\
          '   m,a,s,mn,p25,med,p75,p90,mx: %6.1f %6.1f %6.1f  Dist: %6.1f %6.1f  MD: %6.1f %6.1f %6.1f %6.1f'%\
          (mean,amean,sigma,minv,p25,med,p75,p90,maxv)

def getVerikeys(ostats,ptype):

    verikeys=[]
    kks=ostats.keys()
    for kk in kks:
        verikeys.append(kk[2])

    verikeys=mf.uniq(verikeys)
    if(ptype == 'vbias'):
        verikeys=['vme','vbias']
        verikeys=['vme','vme']

    if(ptype == 'nice'):
        verikeys=['nicea','nice']

    return(verikeys)

def printStats(taids,taus,allstats,ptype,
               w2=None,
               doplotBE=0,
               override=0,
               filtCases={},
               filtStorms={},
               filtDtgs={},
               filtTauErrs={},
               ):

    verikeys=[allstats['curkey']]

    print
    print '   VERIKEY: ',verikeys[0].upper()

    for verikey in verikeys:
        omeans={}
        Fcards={}
        for taid in taids:
            Fcard=None
            for tau in taus:
                try:
                    ntossed=len(filtCases[taid][tau])
                except:
                    ntossed=0
                if(ntossed > 0 and Fcard==None):
                    Fcard=" #Tossed(%5s)      "%(taid.upper())
                if(ntossed > 0 and Fcard != None):
                    Fcard="%s %-4d  "%(Fcard,ntossed)

            Fcards[taid]=Fcard

            if(taids.index(taid) == 0):
                Ncard="         #CASES      "

                for tau in taus:
                    (ostat,mean,amean,sigma,maxv,minv,n,p25,med,p75,p90)=allstats[taid,tau,verikey]
                    Ncard="%s %-4d  "%(Ncard,n)


                Tcard="                    "
                for tau in taus:
                    Tcard="%s  %03d  "%(Tcard,tau)

            for tau in taus:
                (ostat,mean,amean,sigma,maxv,minv,n,p25,med,p75,p90)=allstats[taid,tau,verikey]

                imean=mean
                if(verikey == 'vme'): imean=amean
                if(verikey == 'pbetter'): imean=ostat[0]
                MF.appendDictList(omeans,taid,imean)

        print Tcard
        for taid in taids:
            ocard="  %13s   "%(taid.upper())
            for omean in omeans[taid]:
                ocard="%s %6.1f"%(ocard,omean)
            print ocard

        print Ncard

        # -- print tossed cases
        #
        if(len(Fcards) > 0): 
            for taid in taids:
                try:
                    fcard=Fcards[taid]
                except:
                    fcard=None

                if(fcard != None):
                    print fcard


    print

    # -- filtcases

    BElabels={}
    if(len(filtCases) > 0):

        ntaids=0
        for taid in taids:
            try:
                fdtgs=filtDtgs[taid]
                ftauerrs=filtTauErrs[taid]
            except:
                fdtgs=None

            if(fdtgs == None): continue

            ntaids=ntaids+1
            if(ntaids > 1): print

            print 'BE filter Cases for: %s'%(taid.upper())
            print 'stmid     dtg         tau     BE[nmi]'
            for n in range(0,len(fdtgs)):
                (BEtau,BEstmid,BE)=ftauerrs[n]
                print "%s  %s  %3d  %6.0f"%(BEstmid,fdtgs[n],BEtau,BE)
                BElabels[fdtgs[n],BEstmid,taid]=(BEtau,BE)


    # -- 
    if(len(filtStorms) > 0):
        for taid in taids:
            try:
                stmdtgs=filtStorms[taid]
            except:
                stmdtgs=None

            if(stmdtgs != None):
                sdtgs={}
                for stmdtg in stmdtgs:
                    (stmid,dtg)=stmdtg
                    MF.appendDictList(sdtgs,stmid,dtg)

                stmids=sdtgs.keys()
                stmids.sort()

                for stmid in stmids:
                    for sdtg in sdtgs[stmid]:
                        taidcard=''

                        staid=taid
                        taidcard="%s%s"%(taidcard,staid)

                        try:
                            (BEtau,BE)=BElabels[sdtg,stmid,staid]
                        except:
                            continue

                        labeltag='BE:%4.0f tau:%3d'%(BE,BEtau)


                        ropt='norun'
                        if(doplotBE): ropt=''

                        oopt=''
                        if(override): oopt='-O'
                        dbopt=''
                        doDropbox=1
                        if(doDropbox): dbopt='-d'
                        cmd='''%s/w2-tc-trkplt.py %s %s -S %s -X %s -M 120 -t "%s" %s'''%(w2.PrcDirTctrkW2,
                                                                                          sdtg,taidcard,stmid,oopt,
                                                                                          labeltag,dbopt)
                        mf.runcmd(cmd,ropt)



def IsVmaxOnlyModel(model):
    rc=0
    if(
        (model == 'icnj') or
        (model == 'st5d') or
        (model == 'shf5') or
        (model == 'ivcn') or
        (model == 'spc3')

        ): rc=1

    return(rc)


def GetTrackModelAlias(model,stmid):
    b3id=stmid.split('.')[0]
    year=int(stmid.split('.')[1])
    b1id=b3id[2].lower()

    if(model == 'bcon'):
        if(b1id == 'l' or b1id == 'e' or b1id == 'c'):
            if(year >= 2008):
                amodel='tcn1'  # use the version of conm w/o ecmwf
                amodel='tvcn'
            elif(year >= 2004 and year <= 2007):
                amodel='conu'
            elif(year >= 2001 and year <= 2003):
                amodel='guna'
            elif(year == 2000):
                amodel='guns'
        elif(b1id == 'w' or b1id == 's' or b1id == 'p' or b1id == 'b' or b1id == 'a'):
            if(year >= 2003):
                amodel='conw'
            elif(year == 2002):
                amodel='conu'
            elif(year >= 2000 and year <= 2001):
                amodel='ncon'

        else:
            print "EEE invalid b1id: %s in vdVM.GetTrackModelAlias"%(b1id)
            sys.exit()



    else:
        print "EEE invalid alias model: %s in vdVM.GetTrackModelAlias"%(model)
        sys.exit()

    return(amodel)




def IsTrackModelAlias(model):
    rc=0
    for nmodel in modelsalias:
        if(model == nmodel): rc=1
    return(rc)


def stmlistcard(stmids,nmax=15):

    if(len(stmids) > nmax):
        return(None)

    rptcard='Storms: '
    for stmid in stmids:
        rptcard=rptcard+"%s "%(stmid)

    return(rptcard)

def ListMask(vlist,mask,undef=-999):
    """
    listmask
    """

    olist=[]
    for n in range(0,len(vlist)):
        if(mask[n]):
            olist.append(vlist[n])
        else:
            olist.append(undef)

    return(olist)



def ListMask2Ndx(vlist,mask):

    ndx=[]
    for n in range(0,len(vlist)):
        if(mask[n]):
            ndx.append(1)
        else:
            ndx.append(0)

    return(ndx)

def ListMath(list1,list2,operation='add'):

    listsum=[]
    if(len(list1) != len(list2)):
        print 'EEE cannot add two lists of unequal length'
        return(listsum)


    for n in range(0,len(list1)):
        if(operation == 'add'):
            listsum.append(list1[n]+list2[n])
        elif(operation == 'sub'):
            listsum.append(list1[n]-list2[n])
        else:
            print 'EEE invalid ListMath Operation ',operation
            return(listsum)


    return(listsum)


def ListFilter2Ndx(vlist,condition):

    ndx=[]
    for n in range(0,len(vlist)):
        ndx.append(0)
        if(condition == 'ge0'):
            if(vlist[n] >= 0.0): ndx[n]=1

        if(condition == 'eqm999'):
            if(vlist[n] != -999.): ndx[n]=1

    return(ndx)


def ListDiff(list1,list2):
    olist=[]
    for n in range(0,len(list1)):
        diff=list1[n]-list2[n]
        olist.append(diff)

    return(olist)



def ListReduce(vlist,ndx):
    nlist=[]
    for n in range(0,len(vlist)):
        if(ndx[n]): nlist.append(vlist[n])

    return(nlist)


#
# for arrays of arrays...
#
def TupleFilter2Ndx(tlist,condition):

    ndx=[]
    for n in range(0,len(tlist)):
        ndx.append(0)
        if(condition == 'gt0'):
            if(tlist[n][0] >= 0.0): ndx[n]=1
        elif(condition == 'eq0'):
            if(tlist[n][0] == 0.0): ndx[n]=1

    return(ndx)


def NdxMath(ndx1,ndx2,condition='and'):
    nndx=[]
    n1=len(ndx1)
    n2=len(ndx2)
    nn=n1

    for n in range(0,nn):
        nndx.append(0)
        if(condition == 'and'):
            if(ndx1[n] and ndx2[n]): nndx[n]=1
        elif(condition == 'ge1'):
            if(ndx1[n] and (ndx2[n]>= 1) ): nndx[n]=1
        elif(condition == 'or'):
            if(ndx1[n] or ndx2[n]): nndx[n]=1
        elif(condition == 'revand'):
            if(ndx1[n]==1 and ndx2[n] == 0): nndx[n]=1
        elif(condition == 'revandge1'):
            if(ndx1[n]>=1 and ndx2[n] == 0): nndx[n]=1


    return(nndx)

# redundant code.......
#
## def DupChk(sid,ndx,vdtg,model,verb=0):

##     osid=sid[0]
##     ondx=ndx[0]
##     ovdtg=vdtg[0]
##     if(len(sid) <= 2): return

##     for i in range(1,len(sid)):
##         if(sid[i] == osid and ondx == ndx[i] and ovdtg == vdtg[i]):
##             if(verb): print 'ddddddddddddddd dup for model: ',model,' i: ',i,' set flag to 0'
##             ndx[i]=0

##         osid=sid[i]
##         ondx=ndx[i]
##         ovdtg=vdtg[i]





def NdxHomo(sid1,sid2,ndx1,ndx2,vdtg1,vdtg2,verb=0):

    ndxh1=[]
    ndxh2=[]

    for i in range(0,len(ndx1)):
        ndxh1.append(0)

    for j in range(0,len(ndx2)):
        ndxh2.append(0)

    for i in range(0,len(ndx1)):
        t1=ndx1[i]
        if(t1):
            for j in range(0,len(ndx2)):
                if(
                    ndx2[j] and
                    (vdtg2[j] == vdtg1[i]) and
                    (sid2[j] == sid1[i])
                    ):
                    ndxh1[i]=1
                    ndxh2[j]=1


    if(verb):

        for i in range(0,len(ndxh1)):
            if(ndxh1[i]):
                print 'iii ',i,ndx1[i],ndxh1[i],vdtg1[i]
        print
        for j in range(0,len(ndxh2)):
            if(ndxh2[j]):
                print 'jjj ',j,ndx2[j],ndxh2[j],vdtg2[j]



    return(ndxh1,ndxh2)



def Nrun00(mhr0,mdtau,dtg):
    iok=0
    hh=dtg[8:10]

    if(mdtau == 6):
        iok=1
    elif(mdtau == 12 and mhr0 == 6 and (hh == '06' or hh == '18') ):
        iok=1
    elif(mdtau == 12 and (mhr0 == 0 or mhr0 == 12) and (hh == '00' or hh == '12') ):
        iok=1

    return(iok)


def IsCarq(tcflags):
    iscarq00=[]
    iscarqfc=[]
    for tcflag in tcflags:
        tt=tcflag.split()

        if(tt[2] == 'CQ'):
            iscarqfc.append(1)
        else:
            iscarqfc.append(0)

        if(tt[4] == 'CQ'):
            iscarq00.append(1)
        else:
            iscarq00.append(0)

    return(iscarq00,iscarqfc)


def IsCarqTCetc(tcflags):

    iscarq00=[]
    iscarqfc=[]
    istc00=[]
    isbt00=[]
    iswarn00=[]
    isvmax00=[]
    iscpac00=[]

    for tcflag in tcflags:
        tt=tcflag.split()

        if(tt[2] == 'CQ'):
            iscarq00.append(1)
        else:
            iscarq00.append(0)

        if(tt[2] == 'CQ'):
            iscarqfc.append(1)
        else:
            iscarqfc.append(0)

        if(tt[0] == 'TC'):
            istc00.append(1)
        else:
            istc00.append(0)

        isbt00.append(1)

        if(tt[3] == 'WN'):
            iswarn00.append(1)
        else:
            iswarn00.append(0)

        iscpac00.append(0)


    return(iscarq00,iscarqfc,istc00,isbt00,iswarn00,iscpac00)


def ModelRunMask(vdtg,model,nndx00):

    # -- new form in ATCF.py
    aP=AidProp(model)

    dtaumodel=aP.DdtgModelTracker
    synhrmodel=aP.StartSynHourModel

    rmask=[]
    for dtg in vdtg:
        hh=dtg[8:]
        runmodel=1

        if(dtaumodel == 12):
            if(synhrmodel == 0 and (hh == '06' or hh == '18') ): runmodel=0
            if(synhrmodel == 6 and (hh == '00' or hh == '12') ): runmodel=0
            if(synhrmodel == 12 and (hh == '06' or hh == '18') ): runmodel=0

        rmask.append(runmodel)
    #
    # special case -- ofcl -- rmask = if they made a forecast
    #
    if(model == 'ofcl'):
        rmask=copy.deepcopy(nndx00)

    return(rmask)


#
# 20080229 -- spent a day figuring this out....
#

def NCountsFC(tau,model,vdtg,
              pe,
              nndx,nndx00,nndx00filt,
              istc,isbt):

    #
    # nbt       - # of max bts under the tau0 filter
    # nfc       - # of forecasts
    # nmissfc   - # of missed forecasts (at that tau)
    # nrun      - # of runs that were made suppose to be made to produce fc at tau
    # nmissruns - # of runs missed so  nmissfc-nmissrun is # of failures to track
    #             whereas, nmissrun is number of failures to run the model
    # noverwarn - # of fc with no verifying bt
    #

    nfc=0
    nmissfc=0
    nbt=0
    nmissrun=0
    noverwarn=0

    filtopt='bt'
    #filtopt='all'

    #
    # this mask defines when the model is suppose to be run -- based on synoptic h and dtaumodel 
    #
    rmask=ModelRunMask(vdtg,model,nndx00)
    nc=len(nndx)

    for n in range(0,nc):

        #
        # first, only count cases where a run was suppose to be made
        #

        if(rmask[n]):
            #------------------- run counting
            #
            # first -- was the tau0 posit a TC? the
            #
            if(nndx00filt[n]):
                iok=0
                if(filtopt == 'bt'):
                    if(isbt[n]):
                        iok=1
                elif(filtopt == 'all'):
                    if(isbt[n] or istc[n]):
                        iok=1
                else:
                    if(isbt[n] and istc[n]):
                        iok=1
                if(iok):
                    #
                    # increment run
                    #
                    nbt=nbt+1
                    if(nndx[n] == 0):
                        #
                        # set as a missing run
                        #
                        nmissrun=nmissrun+1

            #-----------------------  fc counting
            #
            # first -- was a forecast made?
            #

            if(nndx[n]):

                nfc=nfc+1

            #---------------------- fc miss and overwarn
            #
            # first -- forecast NOT made
            #

            elif(nndx[n] == 0):

                #
                # second -- was storm a tc and a bt at the verifying time?
                #           does the the run come from a run in warning at tau0? if so a real mis
                #
                if(nndx00[n] == 1 and istc[n] and nndx00filt[n]):
                    nmissfc=nmissfc+1


                #
                #  pe set as a forecast made, but with no verifyable position, from a run that was in warning at tau0
                #
                if( ( pe[n] == -977.9 or pe[n] > 0.0) and istc[n] ):
                    noverwarn=noverwarn+1





    nrun=nbt-nmissrun
    return(nbt,nrun,nmissrun,nfc,nmissfc,noverwarn)


def WindRadiiMetric(vlist,type):

    olist=[]

    if(type == 'r34'):
        norm=100.0
        norm2=norm*norm

    elif(type == 'r50'):
        norm=50.0
        norm2=norm*norm


    for tt in vlist:
        m2=0.0
        n2=0.0
        for i in range(0,len(tt)):
            if(tt[i] >= 0.0):
                m2=m2+tt[i]*tt[i]
                n2=n2+1.0   
        if(n2 > 0.0):
            m2=m2/(norm2*n2)
        else:
            m2=0.0

        # -- make %
        #
        m2=m2*100.0

        olist.append(m2)

    return(olist)






def SimpleListHist(vlist,cuts,verb=0):

    nl=len(vlist)
    ncuts=len(cuts)

    counts=range(0,ncuts+1)
    pcounts=range(0,ncuts+1)

    for n in range(0,ncuts+1):
        counts[n]=0
        pcounts[n]=0.0

    for l in vlist:

        for n in range(0,ncuts+1):

            #
            # ob <
            #
            if(n == 0):
                nc=0
                if(l < cuts[n]):
                    counts[nc]=counts[nc]+1
                    break
            #
            # ob >
            #
            if(n == ncuts-1):
                nc=n+1
                if(l > cuts[n]):
                    counts[nc]=counts[nc]+1
                    break

            if(n < ncuts-1):
                nc=n+1
                if(l >= cuts[n] and l <= cuts[n+1]):
                    counts[nc]=counts[nc]+1
                    break

    if(nl > 0):
        pfact=100.0/float(nl)
    else:
        pfact=0.0

    nc=0
    for n in range(0,ncuts+1):
        pcounts[n]=counts[n]*pfact
        nc=nc+counts[n]

    ohist=''
    for k in range(0,ncuts+1):
        if(verb): print 'hist: %2d %3.0f'%(k,counts[k])
        ohist="%s%3.0f"%(ohist,pcounts[k])

    return(counts,pcounts,ohist)

def SimpleListStatsVD(vlist,verb=0,undef=-77):

    mean=0.0
    amean=0.0
    sigma=0.0
    mean2=0.0
    n=0
    for l in vlist:
        mean=mean+l
        mean2=mean2+l*l
        amean=amean+fabs(l)
        if(verb):
            print 'stats n: ',n,' val: ',l
        n=n+1

    if(n > 0):
        mean=mean/float(n)
        amean=amean/float(n)
        var=mean2/float(n) - mean*mean
        if(fabs(var) > epsilonm5):
            sigma=sqrt(var)
        else:
            sigma=0.0
    else:
        mean=None
        amean=None
        sigma=None
        mean=amean=sigma=undef

    return(mean,amean,sigma,n)



def SetTaus(tauopt):

    taui=12
    if(tauopt != None):
        tt=tauopt.split('.')

        if(len(tt) == 1):
            taub=taue=int(tauopt)

        elif(len(tt) == 2):
            taub=int(tt[0])
            taue=int(tt[1])

        elif(len(tt) == 3):
            taub=int(tt[0])
            taue=int(tt[1])
            taui=int(tt[2])

        taus=[]

        for tau in range(taub,taue+1,taui):
            taus.append(tau)


    else:
        taus=[0,12,24,36,48,72,96,120]

    return(taus)


def GetVdListDic(vd,model,stmids,tau,vdvar,filtdtgs=None):

    vlist=[]


    for stmid in stmids:

        if(filtdtgs != None):

            fmask=[]
            idtgs=vd[model,stmid].bdtg[tau]
            for n in range(0,len(idtgs)):
                fmask.append(0)

            for n in range(0,len(idtgs)):
                idtg=idtgs[n]
                for m in range(0,len(filtdtgs)):
                    fdtg=filtdtgs[m]
                    if(fdtg == idtg):
                        fmask[n]=1
                        break


        try:
            tt=vd[model,stmid].pe[tau]
        except:
            continue

        if(vdvar == 'pe'):
            ladd=vd[model,stmid].pe[tau]
        elif(vdvar == 'cte'):
            ladd=vd[model,stmid].cte[tau]
        elif(vdvar == 'ate'):
            ladd=vd[model,stmid].ate[tau]

        elif(vdvar == 'vme'):
            ladd=vd[model,stmid].vme[tau]

        elif(vdvar == 'tcYN'):
            ladd=vd[model,stmid].tcYN[tau]

        elif(vdvar == 'tc00YN'):
            ladd=vd[model,stmid].tc00YN[tau]

        elif(vdvar == 'btYN'):
            ladd=vd[model,stmid].btYN[tau]

        elif(vdvar == 'warnYN'):
            ladd=vd[model,stmid].warnYN[tau]

        elif(vdvar == 'cpacYN'):
            ladd=vd[model,stmid].cpacYN[tau]

        elif(vdvar == 'bdtg'):
            ladd=vd[model,stmid].bdtg[tau]
        elif(vdvar == 'vdtg'):
            ladd=vd[model,stmid].vdtg[tau]

        elif(vdvar == 'blf'):
            ladd=vd[model,stmid].blf[tau]
        elif(vdvar == 'flf'):
            ladd=vd[model,stmid].flf[tau]
        elif(vdvar == 'podflag'):
            ladd=vd[model,stmid].podflag[tau]
        elif(vdvar == 'tcflags'):
            ladd=vd[model,stmid].tcflags[tau]


        elif(vdvar == 'tcvmax'):
            ladd=vd[model,stmid].tcvmax[tau]
        elif(vdvar == 'tclat'):
            ladd=vd[model,stmid].tclat[tau]
        elif(vdvar == 'tclon'):
            ladd=vd[model,stmid].tclon[tau]

        elif(vdvar == 'r34'):
            ladd=vd[model,stmid].r34[tau]
        elif(vdvar == 'r50'):
            ladd=vd[model,stmid].r50[tau]

        elif(vdvar == 'fcvmax'):
            ladd=vd[model,stmid].fcvmax[tau]

        elif(vdvar == 'tcr34'):
            ladd=vd[model,stmid].tcr34[tau]
        elif(vdvar == 'tcr50'):
            ladd=vd[model,stmid].tcr50[tau]

        if(filtdtgs != None):
            nladd=[]
            for n in range(0,len(fmask)):
                if(fmask[n]):
                    nladd.append(ladd[n])

            ladd=nladd

        vlist=vlist+ladd

    return(vlist)


def GetVdListStmidDic(vd,model,stmids,tau):

    liststmid=[]

    for stmid in stmids:

        try:
            tt=vd[model,stmid].pe[tau]
        except:
            continue

        sladd=[]
        for n in range(0,len(tt)):
            sladd.append(stmid)

        liststmid=liststmid+sladd

    return(liststmid)


def f(Nrc):

    (nbt,nrun,nmissrun,nfc,nmissfc,noverwarn)=Nrc

    if(nbt > 0):
        pod=float(nfc)/float(nbt)*100.0
    else:
        pod=0.0

    ntotfc=nfc+nmissfc

    if(ntotfc > 0):
        pof=(1.0-(float(nmissfc)/float(ntotfc)))*100.0
    else:
        pof=0.0

    return(pod,pof)


def StatHash2allstats(stathash,mod1,taus):

    allstat=[]

    mpe1s={}
    mpe2s={}
    mcte1s={}
    mcte2s={}
    mate1s={}
    mate2s={}
    gainxys={}
    gaine6xs={}
    npe1s={}
    mpe2m1s={}
    pof1s={}
    pod1s={}

    mvear1s={}
    mvebr1s={}
    mvear2s={}
    mvebr2s={}

    nrun1s={}
    nrunmiss1s={}
    nbt1s={}
    nfc1s={}
    nfcmiss1s={}
    nfcover1s={}

    for tau in taus:

        try:
            (mpe1,mpe2,mcte1,mcte2,
             mate1,mate2,
             amvme1,amvme2,mvme1,mvme2,
             gainxy,gaine6x,npe1,
             mpe2m1,pof1,pod1,nrun1,
             nrunmiss1,nbt1,nfc1,
             nfcmiss1,nfcover1)=stathash[mod1,tau]
        except:
            continue


        mpe1s[tau]=mpe1
        mpe2s[tau]=mpe2
        mcte1s[tau]=mcte1
        mcte2s[tau]=mcte2
        mate1s[tau]=mate1
        mate2s[tau]=mate2
        gainxys[tau]=gainxy
        gaine6xs[tau]=gaine6x
        npe1s[tau]=npe1
        mpe2m1s[tau]=mpe2m1
        pof1s[tau]=pof1
        pod1s[tau]=pod1

        mvear1s[tau]=amvme1
        mvebr1s[tau]=mvme1
        mvear2s[tau]=amvme2
        mvebr2s[tau]=mvme2

        nrun1s[tau]=nrun1
        nrunmiss1s[tau]=nrunmiss1
        nbt1s[tau]=nbt1
        nfc1s[tau]=nfc1
        nfcmiss1s[tau]=nfcmiss1
        nfcover1s[tau]=nfcover1


    allstat=(mod1,mpe1s,mpe2s,mcte1s,mcte2s,
             mate1s,mate2s,
             mvear1s,mvear2s,mvebr1s,mvebr2s,
             gainxys,gaine6xs,npe1s,
             mpe2m1s,pof1s,pod1s,nrun1s,
             nrunmiss1s,nbt1s,nfc1s,
             nfcmiss1s,nfcover1s)


    return(allstat)


def CountOnes(vlist):

    n=0
    for l in vlist:
        if(l ==1): n=n+1

    return(n)


def SetTau00Filt(tau00filtopt,nndx,nndxrun,ndxpe,ndxtc00,isbt00,iswarn00):


    #
    # tau 00 filter options
    #

    if(tau00filtopt == 'tc'):
        nndx=NdxMath(nndx,ndxtc00)
        nndx00filt=ndxtc00

    elif(tau00filtopt == 'bt'):
        nndx=NdxMath(nndx,ndxtc00)
        nndx=NdxMath(nndx,isbt00)
        nndx00filt=NdxMath(ndxtc00,isbt00)

    elif(tau00filtopt == 'bt00'):
        nndx=NdxMath(nndx,isbt00)
        nndx00filt=isbt00

    elif(tau00filtopt == 'warn'):
        nndx=NdxMath(nndx,iswarn00)
        nndx00filt=iswarn00

    elif(tau00filtopt == 'all'):
        nndx=ndxpe
        nndx00filt=nndxrun

    else:
        print 'EEEEEEEEEEEEE localvdstat: invalid tau00filtopt: ',tau00filtopt
        sys.exit()

    return(nndx,nndx00filt)


def mkscardpre(stmid,model):

    scpre="%4s%2s_%-6s"%(stmid[0:4],stmid[6:8],model)
    return(scpre)


def mkncard(ns,scpre,taus,ntitle):

    ncard=scpre + "%26s: "%(ntitle)
    for tau in taus:
        on1="%5d"%(ns[tau])
        ncard=ncard+on1

    return(ncard)



def CountMaskFe(pe,pod,isbt,istc,vdtg,bdtg,
                nndx,nndxrun,n00filt,taus,
                n,cntmask,verirule='tc',
                veriwarn=0):

    for tau in taus:

        try:
            ipe=pe[tau][n]
        except:
            continue

        ibt=isbt[tau][n]
        itc=istc[tau][n]
        ipod=pod[tau][n]
        # -- not sure I really want to use this -- yes for defining if veri posit
        #
        inndx=nndx[tau][n]

        ibdtg=bdtg[n]
        ivdtg=vdtg[tau][n]
        runmodel=nndxrun[tau][n]
        n00f=n00filt[n]

        #print 'ppppppp ',ivdtg,tau,n,'istc: ',itc,ipod,ipe

        # -- ipod in four states
        #    0 -- no verifying posit; no forecast ; no modelrun
        #    1 -- verifying posit with forecast
        #    2 -- verifying posit in WARN stat with forecast
        #   -1 -- verifying posit but NO forecast
        #   -2 -- verifying posit but NO forecast in WARN stat
        # 999  --  forecast made not verified (overwarn) because not tc or because of rule

        # -- 20140513 -- mods to account where the initial time is verifiable
        #                correct handling of overwarn

        if(ipod  == 0 or runmodel == 0 or n00f == 0):
            cntmask[tau][n]=0

        elif(ipod == 1 and inndx == 1):
            cntmask[tau][n]=1

        elif(ipod == 2 and inndx == 1):
            cntmask[tau][n]=2

        elif(ipod == -1):
            cntmask[tau][n]=-1
            #if(inndx == 0): cntmask[tau][n]=0

        elif(ipod == -2):
            cntmask[tau][n]=-2
            #if(inndx == 0): cntmask[tau][n]=0

        elif((ipod == 999 or (inndx == 0 and (ipod == 1 or ipod == 2)))):
            cntmask[tau][n]=10  
            #if(inndx == 1): cntmask[tau][n]=10
            #if(inndx == 0): cntmask[tau][n]=0

        # no pe because a vmax only model
        #
        elif(ipe == -777.7):
            cntmask[tau][n]=15

        else:
            print 'EEE in localvdstat2.CountMaskpe invalid ipod: ',ipod
            sys.exit()

        # -- 20131211 tricky logic here -- 
        #    if cnt = -1 means model missed a verifying postion defined as posit == TC & BT, but was NOT in warning
        #
        if(veriwarn and (cntmask[tau][n] == -1) ):
            cntmask[tau][n]=0

        # -- 20131211 -- the nndx array determines if posit will be verified, set to 0 those fc not being verified
        #
        if(inndx == 0 and cntmask[tau][n] >= 1 and cntmask[tau][n] < 10):
            cntmask[tau][n]=0




    return



def FormatFe(pe,cntmask,taus,n):

    pecard=''
    for tau in taus:

        ipe=pe[tau][n]
        icnt=cntmask[tau][n]
        if(icnt == -1 or icnt == -2):
            ope='  MMM'
        elif(icnt == 0 or icnt == 15):
            ope='     '
        elif(icnt == 10):
            ope=' owrn'
        elif(icnt == 1 or icnt == 2):
            ope="%5.0f"%(ipe)
        else:
            print 'EEE in Formatpe icnt: ',icnt
            sys.exit()

        pecard=pecard+ope

    return(pecard)



def FormatVme(vme,cntmask,taus,n):

    vmecard=''
    for tau in taus:

        ivme=vme[tau][n]
        icnt=cntmask[tau][n]

        if(icnt == 0):
            ovme='     '
        elif(icnt == -1):
            ovme='  MMM'
        elif(icnt == -2):
            ovme='  MMM'
        elif(icnt == 10):
            ovme=' owrn'
        elif(ivme <= -999.0):
            ovme='     '
        else:
            ovme="%5.0f"%(ivme)

        vmecard=vmecard+ovme

    return(vmecard)


def FormatFeCsv(pe,cntmask,taus,n):

    pecard=''
    for tau in taus:

        ipe=pe[tau][n]
        icnt=cntmask[tau][n]

        if(icnt == 0 or icnt <= -1):
            ope="       ,"
        elif(icnt == 1 or icnt == 2):
            ope=" %5.0f ,"%(ipe)
        elif(icnt == 10):
            ope=" %5.0f ,"%(9999.)
        else:
            print 'EEE in FormatpeCsv icnt: ',icnt

        pecard=pecard+ope

    return(pecard)

def FormatVmeCsv(vme,cntmask,taus,n):

    vmecard=''
    for tau in taus:
        ivme=vme[tau][n]
        icnt=cntmask[tau][n]

        if(ivme <= -999.0 or icnt == 0 or icnt < 0):
            ovme='      , '
        else:
            ovme=" %5.0f, "%(ivme)

        vmecard=vmecard+ovme

    return(vmecard)

def FormatTauCsv(taus):

    taucard=''
    for tau in taus:
        otau="   %03i ,"%(int(tau))
        taucard=taucard+otau

    return(taucard)



def FormatCte(cte,cntmask,nndxrun,taus,n):

    ctecard=''
    for tau in taus:
        icte=cte[tau][n]
        icnt=cntmask[tau][n]
        if(icnt == -1 or icnt == -2):
            octe='  MMM'
        elif(icnt == 0):
            octe='     '
        elif(icte == 9999.9):
            octe='     '
        else:
            octe="%5.0f"%(icte)

        ctecard=ctecard+octe

    return(ctecard)


def StatAnal(pe,vme,vmep,
             cte,ate,
             tcvmax,
             stmid,model,
             tclat00,tclon00,tcvmax00,
             nndx,nndxvme,taus):

    stats={}

    mpe={}
    ampe={}
    sigpe={}

    mcte={}
    amcte={}
    sigcte={}

    mate={}
    amate={}
    sigate={}

    mtcvmax={}
    amtcvmax={}
    sigtcvmax={}

    mvme={}
    amvme={}
    sigvme={}

    mvmep={}
    amvmep={}
    sigvmep={}


    npe={}
    nvme={}
    nvmep={}

    vmehist={}

    undefpe=-999.
    undefmve=999.

    nl=ListReduce(tclat00,nndx[0])
    (mlat,amlat,siglat,nlat)=SimpleListStatsVD(nl)

    nl=ListReduce(tclon00,nndx[0])
    (mlon,amlon,siglon,nlon)=SimpleListStatsVD(nl)

    nl=ListReduce(tcvmax00,nndx[0])
    (mvmax,amvmax,sigvmax,nvmax)=SimpleListStatsVD(nl,undef=undefmve)

    for tau in taus:

        nlpe=ListReduce(pe[tau],nndx[tau])
        (mpe[tau],ampe[tau],sigpe[tau],npe[tau])=SimpleListStatsVD(nlpe,undef=undefpe)

        nlcte=ListReduce(cte[tau],nndx[tau])
        (mcte[tau],amcte[tau],sigcte[tau],ncte)=SimpleListStatsVD(nlcte,undef=undefpe)

        nlate=ListReduce(ate[tau],nndx[tau])
        (mate[tau],amate[tau],sigate[tau],nlat)=SimpleListStatsVD(nlate,undef=undefpe)

        nltcvmax=ListReduce(tcvmax[tau],nndxvme[tau])
        (mtcvmax[tau],amtcvmax[tau],sigtcvmax[tau],nlat)=SimpleListStatsVD(nltcvmax,undef=undefpe)

        nlvme=ListReduce(vme[tau],nndxvme[tau])
        (mvme[tau],amvme[tau],sigvme[tau],nvme[tau])=SimpleListStatsVD(nlvme,undef=undefmve)

        nlvmep=ListReduce(vmep[tau],nndxvme[tau])
        (mvmep[tau],amvmep[tau],sigvmep[tau],nvmep[tau])=SimpleListStatsVD(nlvmep,undef=undefmve)

        #
        # 5 bin histo for vme
        #

        (vmehist[tau],pcvme,ohistvme)=SimpleListHist(nlvme,vmecutpoints)



    stats=(npe,nvme,
           mpe,ampe,sigpe,
           mcte,amcte,sigcte,
           mate,amate,sigate,
           mtcvmax,amtcvmax,sigtcvmax,
           mvme,amvme,sigvme,
           mvmep,amvmep,sigvmep,
           vmehist,
           tclat00,tclon00,tcvmax00,
           mlat,mlon,mvmax,
           )


    return(stats)






def CountAnal(isbttaus,istctaus,
              cntmask,nndx,nndxrun,n00filt,
              stmid,model,
              taus,verirule='tc',dohomo=1,
              veriwarn=0):

    nfcs={}
    nmisss={}
    novers={}
    nmissruns={}
    nveris={}
    pods={}
    pofs={}


    for tau in taus:

        cnts=cntmask[tau]
        isbts=isbttaus[tau]
        istcs=istctaus[tau]

        nfc=0
        nmiss=0
        nover=0
        nmissrun=0

        nveri=0

        nbdtg=len(cnts)

        for n in range(0,nbdtg):
            cnt=cnts[n]
            ndxv=n00filt[n]
            isbt=isbts[n]
            istc=istcs[n]

            vflag=' '
            if(nndx[0][n]):
                vflag='+'
            else:
                if(n00filt[n]):
                    vflag='-'
                if(nndxrun[0][n] == 0):
                    vflag=' '
                else:
                    vflag='*'            

            if(verirule == 'all'):
                istc=1

            if(ndxv):
                if(cnt == 1 or cnt == 2):
                    nfc=nfc+1
                elif((cnt == -1 or cnt == -2) and ((dohomo and vflag != '*') or dohomo == 0)):
                    nmiss=nmiss+1       
                    nmissrun=nmissrun+1
                elif(cnt == 10 and ((dohomo and vflag != '*') or dohomo == 0)):
                    nover=nover+1

                if( veriwarn ):
                    if(abs(cnt) == 2 and ((dohomo and vflag != '*') or dohomo == 0)):
                        nveri=nveri+1
                else:
                    if( abs(cnt) >= 1 and ((dohomo and vflag != '*') or dohomo == 0)):
                        nveri=nveri+1       

        nfcs[tau]=nfc
        nmisss[tau]=nmiss
        novers[tau]=nover
        nmissruns[tau]=nmissrun
        nveris[tau]=nveri

        if(nveri > 0):
            pods[tau]=int((float(nfc)/float(nveri))*100.0)
        else:
            pods[tau]=0

        if(nfc > 0):
            pofs[tau]=int((float(nfc)/float(nfc+nmiss))*100.0)
        else:
            pofs[tau]=0

        #print "fff tau: %3d  Nfc: %3d  Nmiss/Run %3d : %3d  Nover: %3d  nveri: %3d "%(tau,nfc,nmiss,nmissrun,nover,nveri)


    counts=(nfcs,nmisss,novers,nmissruns,nveris,pods,pofs)

    return(counts)



def PrintStatCards(stats,taus,sctitle,doprint=1):


    (npe,nvme,
     mpe,ampe,sigpe,
     mcte,amcte,sigcte,
     mate,amate,sigate,
     mtcvmax,amtcvmax,sigtcvmax,
     mvme,amvme,sigvme,
     mvmep,amvmep,sigvmep,
     vmehist,
     tclat00,tclon00,tcvmax00,
     mlat,mlon,mvmax)=stats


    undefpe=-999.
    undefmve=999.

    omlat=FormatLat(mlat)
    omlon=FormatLon(mlon)
    omvmax="%3.0f"%(mvmax)


    s1card=sctitle  + "  mpe/amve %s %s %s "%(omlat,omlon,omvmax)
    s2card=sctitle  + '                pe/vme sig: '
    s2acard=sctitle + '                  vme bias: '
    s2ccard=sctitle + '                 mean fcvm: '
    s2dcard=sctitle + '                 mean TCvm: '
    s2bcard=sctitle + '              cte/ate bias: '
    s3card=sctitle  + '                         N: '

    for tau in taus:

        if(mpe[tau] == undefpe):
            ompe='     '
            omcte='     '
            osigpe='     '
        else:
            ompe="%5.0f"%(mpe[tau])
            omcte="%5.0f"%(mcte[tau])
            osigpe="%5.0f"%(sigpe[tau])

        onpe="%5d"%(npe[tau])
        oblank=5*' '

        s1card=s1card+ompe
        s2card=s2card+osigpe
        s2acard=s2acard+oblank
        s2ccard=s2ccard+oblank
        s2dcard=s2dcard+oblank
        s2bcard=s2bcard+omcte

        s3card=s3card+onpe

    s1card=s1card+ ' '
    s2card=s2card+ ' '
    s2acard=s2acard+ ' '
    s2ccard=s2ccard+ ' '
    s2dcard=s2dcard+ ' '
    s2bcard=s2bcard+ ' '
    s3card=s3card+ ' '

    for tau in taus:

        if(mvme[tau] == undefmve):
            oamvme=5*' '
            omvme=oamvme
            osigvme=oamvme
            omvmep=oamvme
            otcvmax=oamvme
        else:
            oamvme="%5.0f"%(amvme[tau])
            omvme="%5.0f"%(mvme[tau])
            osigvme="%5.0f"%(sigvme[tau])
            omvmep="%5.0f"%(mvmep[tau])
            otcvmax="%5.0f"%(mtcvmax[tau])

        if(mpe[tau] == undefpe):
            omate='     '
        else:
            omate="%5.0f"%(mate[tau])


        onvme="%5d"%(nvme[tau])


        s1card=s1card+oamvme
        s2card=s2card+osigvme
        s2acard=s2acard+omvme
        s2ccard=s2ccard+omvmep
        s2dcard=s2dcard+otcvmax
        s2bcard=s2bcard+omate
        s3card=s3card+onvme

    scards=[]

    scards.append(s1card)
    scards.append(s2card)
    scards.append(s2acard)
    scards.append(s2ccard)
    scards.append(s2dcard)
    scards.append(s2bcard)
    scards.append(s3card)

    if(doprint):
        print s1card
        print s2card
        print s2acard
        print s2ccard
        print s2dcard
        print
        print s2bcard
        print
        print s3card


    return(scards)




def PrintCountCards(counts,taus,sctitle,doprint=1):


    (nfcs,nmisss,novers,nmissruns,nveris,pods,pofs)=counts


    scards=[]

    scards.append(mkncard(nfcs,sctitle,taus,'Nfc'))
    scards.append(mkncard(nmisss,sctitle,taus,'Nmiss'))
    scards.append(mkncard(nveris,sctitle,taus,'Nveri'))

    scards.append(mkncard(pods,sctitle,taus,'POD'))
    scards.append(mkncard(pofs,sctitle,taus,'POF'))

    scards.append(mkncard(novers,sctitle,taus,'Nover'))
    scards.append(mkncard(nmissruns,sctitle,taus,'Nmissruns'))

    if(doprint):
        print scards[0]
        print scards[1]
        print scards[2]
        print
        print scards[3]
        print scards[4]
        print scards[5]
        print scards[6]

    return(scards)



def IsFeCardInValid(card):

    invalid=(mf.find(card,'norn') or mf.find(card,'MMM'))
    if(not(invalid) and len(card.split()) <= 8): invalid=1

    return(invalid)




def PrintFeVmeTable(model,printtable,
                    bdtg,pe,vme,cte,ate,tcvmax,cntmask,
                    tclat00,tclon00,tcvmax00,
                    nndx,nndxrun,n00filt,nndx00filt,
                    istc00,isbt00,iswarn00,iscarq00,
                    taus,
                    dspltable,
                    printall,
                    pdtgs=None,
                    docsv=1,
                    veriwarn=0,
                    printRunOnly=0,
                    ):

    ocards={}

    fcvmax={}

    # -- get forecast vmax
    #
    if(dspltable == 'vmax'):

        kk=tcvmax.keys()
        for k in kk:
            btvt=tcvmax[k]
            vmet=vme[k]
            fcvm=[]
            for n in range(0,len(btvt)):
                bt=btvt[n]
                fce=vmet[n]
                if(bt != -999):
                    fcv=bt+fce
                else:
                    fcv=-999
                fcvm.append(fcv)
            fcvmax[k]=fcvm


    if(pdtgs == None): pdtgs=bdtg
    nbdtg=len(bdtg)

    if(docsv):
        ocards=[]
        taucardCsv=FormatTauCsv(taus)
        headcardCsv="B# , YYYYMMDDHH ,   lat  ,  lon   , Vmax , Vf , %s%s"%\
            (taucardCsv,taucardCsv)
        print headcardCsv
        ocards.append(headcardCsv)
        printtable=0

    for n in range(0,nbdtg):

        if(not(bdtg[n] in pdtgs)): continue
        ddtg=0
        if(n> 0 and n < nbdtg):
            if(printRunOnly):
                if(nndxrun[0][n] == 0): continue

            ddtg=mf.dtgdiff(bdtg[n-1],bdtg[n])
            if(ddtg != 6):
                mdtg=mf.dtginc(bdtg[n-1],6)
                mcard="MM %s -"%(mdtg)
                if(printtable): print mcard

        try:
            otclat00=FormatLat(tclat00[n])
        except:
            continue

        otclon00=FormatLon(tclon00[n])

        if(dspltable == 'pe'):
            pecard     = FormatFe(pe,cntmask,taus,n)
            vmecard    = FormatVme(vme,cntmask,taus,n)
            pecardCsv  = FormatFeCsv(pe,cntmask,taus,n)
            vmecardCsv = FormatVmeCsv(vme,cntmask,taus,n)

        elif(dspltable == 'vmax'):
            pecard     = FormatFe(tcvmax,cntmask,taus,n)
            vmecard    = FormatVme(fcvmax,cntmask,taus,n)
            pecardCsv  = FormatFeCsv(tcvmax,cntmask,taus,n)
            vmecardCsv = FormatVmeCsv(fcvmax,cntmask,taus,n)


        else:
            ctecard=FormatCte(cte,cntmask,nndxrun,taus,n)
            atecard=FormatCte(ate,cntmask,nndxrun,taus,n)
            pecard=ctecard
            vmecard=atecard

        vflag=' '
        if(nndx[0][n]):
            vflag='+'
        else:
            if(n00filt[n]):
                vflag='-'
            if(nndxrun[0][n] == 0):
                vflag=' '
            else:
                vflag='*'

        card="%2d %s %d%d%d %d%d %d%d %s %s %3d%s%s %s"%\
            (n,bdtg[n],
             nndx[0][n],nndxrun[0][n],nndx00filt[0][n],istc00[n],isbt00[n],iswarn00[n],iscarq00[n],
             otclat00,otclon00,tcvmax00[n],vflag,
             pecard,vmecard
             )

        cardCsv="%02d , %s , %6.1f , %6.1f ,  %3.0f ,  %s , %s %s"%\
            (n,bdtg[n],
             tclat00[n],tclon00[n],tcvmax00[n],vflag,
             pecardCsv,vmecardCsv
             )

        if(docsv):
            ocards.append(cardCsv)
            print cardCsv

        if(printtable and not(docsv)):
            doprint=0
            if(printall == 2 and vflag == '+'):
                doprint=1
            elif(printall == 1 or (printall == 0 and not(IsFeCardInValid(card)))):
                doprint=1
            if(doprint):
                print card

        if(not(docsv)):    
            ocards[bdtg[n]]=card


    return(ocards)





def HomoVdeckHash(vd,models,vstmids,taus,verb=0,filtdtgs=None):

    mask={}
    pe1={}
    pe2={}

    maskfcvm={}
    fcvm1={}
    fcvm2={}

    for n in range(0,len(models)):
        model1=models[n]
        model2=models[n-1]

        if(verb):
            print '1111111111111111 ',model1
            print'22222222222222222 ',model2

        for stmid in vstmids[model1]:

            istmids=[stmid]

            for tau in taus:

                pe1[tau]=GetVdListDic(vd,model1,istmids,tau,'pe',filtdtgs)
                pe2[tau]=GetVdListDic(vd,model2,istmids,tau,'pe',filtdtgs)

                fcvm1[tau]=GetVdListDic(vd,model1,istmids,tau,'fcvmax',filtdtgs)
                fcvm2[tau]=GetVdListDic(vd,model2,istmids,tau,'fcvmax',filtdtgs)

                npe1=len(pe1[tau])
                npe2=len(pe2[tau])

                if(npe1 != npe2):
                    print 'EEEEEEEEEEE vdecks difperent sizes for models: ',model1,model2,' and storm: ',stmid,' rerun vd (alias to w2.tc.vdeck.py'
                    sys.exit()

                if(verb): print 'nnnnnnnnn ',npe1,npe2


                for j in range(0,npe1):

                    condition1=(pe1[tau][j] >= 0.0 and pe2[tau][j] >= 0.0)
                    condition2=(pe1[tau][j] == -977.9 and pe2[tau][j] >= -977.9)

                    condition3=(fcvm1[tau][j] > 0.0 and fcvm2[tau][j] > 0.0)

                    if(condition1 or condition2):
                        try:
                            mask[model1,stmid,tau].append(1)
                        except:
                            mask[model1,stmid,tau]=[]
                            mask[model1,stmid,tau].append(1)
                    else:
                        try:
                            mask[model1,stmid,tau].append(0)
                        except:
                            mask[model1,stmid,tau]=[]
                            mask[model1,stmid,tau].append(0)

                    if(condition3):
                        try:
                            maskfcvm[model1,stmid,tau].append(1)
                        except:
                            maskfcvm[model1,stmid,tau]=[]
                            maskfcvm[model1,stmid,tau].append(1)
                    else:
                        try:
                            maskfcvm[model1,stmid,tau].append(0)
                        except:
                            maskfcvm[model1,stmid,tau]=[]
                            maskfcvm[model1,stmid,tau].append(0)


                    if(mask[model1,stmid,tau][j] and verb):
                        print 'mmmmmmmmmmm ',n,model1,stmid,tau,j,pe1[tau][j],pe2[tau][j],' mask: ',mask[model1,stmid,tau][j]
                        print 'mmmmmVVVVVV ',n,model1,stmid,tau,j,'fcVM: ',fcvm1[tau][j],fcvm2[tau][j],' maskfcvm: ',maskfcvm[model1,stmid,tau][j]


    return(mask,maskfcvm)


def listcard(vars,format,title='',undef=-999):

    phead="% 20s"%(title)
    pcard=phead

    try:
        lformat=len(format%(0))
    except:
        lformat=len(format)


    for n in range(0,len(vars)):
        var=vars[n]

        if(n > 0 and n%15 == 0):
            pcard=pcard+'\n'+phead

        try:
            if(isundef(var,undef) != 1):
                ovar=format%var
            else:
                ovar=lformat*' '
        except:
            ovar=format
        pcard=pcard+ovar

    return(pcard)


def listcard2(vars,formats,undefs,allformat,title=''):

    phead="% 20s"%(title)
    pcard=phead

    nvar=len(vars)

    for n in range(0,nvar):
        lvar=len(vars[n])
        if(len(vars[n]) != len(vars[n-1])):
            pcard='var1s and var2s not the same size.............'
            return(pcard)

    for l in range(0,lvar):

        ss=[]

        ndef=0
        for n in range(0,nvar):

            f=formats[n]
            u=undefs[n]
            v=vars[n][l]


            try:
                lf=len(f%(0))
            except:
                lf=len(f)

            if(isundef(v,undef=u)):
                sv=lf*' '
            else:
                sv=f%(v)
                ndef=ndef+1

            ss.append(sv)

        ss=tuple(ss)
        allss=allformat%ss
        if(ndef == 0):
            allss=len(allss)*' '
        pcard=pcard+allss

    return(pcard)



def hashcard(hash,keys,format,title='',nozero=0,undef=-999.):

    undefs=[-999.0,999.0]

    phead="% 20s"%(title)
    pcard=phead
    for kk in keys:
        val=hash[kk]
        ovar=format%val
        if(isundef(val,undef)): ovar=len(ovar)*' '
        if(nozero and (val == 0.0 or ovar == '-0.0') ): ovar=len(ovar)*' '

        pcard=pcard+ovar

    return(pcard)

def hashcard2(hash1,hash2,keys,format1,format2,
              title='',nozero=0):

    phead="% 20s  "%(title)
    pcard=phead
    for kk in keys:

        dov1=dov2=1
        val1=hash1[kk]
        ovar1=format1%val1
        if(isundef(val1)): ovar1=len(ovar1)*' '
        if(nozero and val1 == 0 or (nozero and val1 == 0) ):
            dov1=0
            ovar1=len(ovar1)*' '

        val2=hash2[kk]
        ovar2=format2%val2
        if(isundef(val2) or (nozero and val2 == 0) ):
            dov2=0
            ovar2=len(ovar2)*' '

        if(dov1 and dov2):
            pcard=pcard+"%s/%s"%(ovar1,ovar2)
        else:
            pcard=pcard+"%s %s"%(ovar1,ovar2)



    return(pcard)

def intermodelstats(model1,model2,sstat,nvar):

    undef=-999.
    rc1=sstat[model1]
    rc2=sstat[model2]

    mpe1=rc1[nvar]
    mpe2=rc2[nvar]

    taus=mpe1.keys()
    taus.sort()

    gainxy={}
    dmpe={}

    for tau in taus:

        iok=( isundef(mpe2[tau]) or isundef(mpe1[tau]) or
              iszero(mpe2[tau]) or iszero(mpe1[tau]) ) 

        if(iok):
            gain=undef
            dm=undef

        else:
            dm=mpe2[tau]-mpe1[tau]
            if(mpe2[tau] > 0.0):
                gain=(dm/mpe2[tau])*100.0

        gainxy[tau]=gain
        dmpe[tau]=dm

    return(gainxy,dmpe)



def gainxystats(mpe1,mpe2):

    undef=-999.

    taus=mpe1.keys()
    taus.sort()

    gainxy={}
    dmpe={}

    for tau in taus:

        if(isundef(mpe2[tau]) or isundef(mpe1[tau])):
            gain=undef
            dm=undef

        else:
            dm=mpe2[tau]-mpe1[tau]
            if(mpe2[tau] > 0.0):
                gain=(dm/mpe2[tau])*100.0
            else:
                gain=undef
                dm=undef

        gainxy[tau]=gain
        dmpe[tau]=dm

    return(gainxy,dmpe)

def getstatsfromlist(rc):

##  00      npe,
##  01      nvme,
##  02      mpe,
##  03      ampe,
##  04      sigpe,
##  05      mcte,
##  06      amcte,
##  07      sigcte,
##  08      mate,
##  09      amate,
##  10      sigate,
##  11      mtcvmax,
##  12      amtcvmax,
##  13      sigtcvmax,
##  14      mvme,
##  15      amvme,
##  16      sigvme,
##  17      mvmep,
##  18      amvmep,
##  19      sigvmep,
##  20      vmehist,
##  21      tclat00,
##  22      tclon00,
##  23      tcvmax00,
##  24      mlat,
##  25      mlon,
##  26      mvmax,


    npe=rc[0]
    mpe=rc[2]
    mcte=rc[5]
    mate=rc[8]

    nvme=rc[1]
    mvme=rc[14]
    amvme=rc[15]
    mvmep=rc[17]
    amvmep=rc[18]
    mtcvmax=rc[11]

    rc=(npe,mpe,mcte,mate,nvme,mvme,amvme,mtcvmax,mvmep)
    return(rc)


def getcountsfromlist(rc):

    pods=rc[5]
    pofs=rc[6]
    rc=(pods,pofs)
    return(rc)





def titlecard(dohomo,models,model,lmodel,tau00filtopt,stmids,filtdtgs):

    nstm=len(stmids)

    if(dohomo):
        card="HOMO Comp tau00filt: %s   model: %s v %s  N: %d TCs"%\
            (tau00filtopt,model,lmodel,nstm)

    else:
        hd="Hetr Comp t00filt: %s"%(tau00filtopt)   
        card=listcard(models," %6s ",hd)
        card=card + " N: %d TCs"%nstm

    if(filtdtgs != None):
        card="%s DTGs: %s <-> %s"%(card,filtdtgs[0],filtdtgs[-1])

    return(card)



def PrintSumStmStat(models,vstmids,
                    sstat,simstat,
                    scnts,
                    vopts,
                    pvar,npvartag,pvartag,
                    doplot,
                    filtdtgs=None,
                    ):


    def mfe2char(taus,mpe,npe,smean,mmean,nsg,nmg,
                 gainxyvme,dmvme,sgain,mgain,
                 lmpe,lsmean,lmmean,
                 undef=-999):

        ctaus=[]
        for tau in taus:
            ctaus.append("%3d"%(tau))
        ctaus.append('nSE')
        ctaus.append('nME')

        cmpe={}

        for k in mpe.keys():
            kk="%3d"%(k)
            if(isundef(mpe[k]) or iszero(mpe[k])):
                cmpe[kk]="%s"%(5*' ')
            else:
                cmpe[kk]="%5.1f"%(mpe[k])

        cmpe['nSE']="%5.1f"%(smean)
        cmpe['nME']="%5.1f"%(mmean)

        if(isundef(mmean)):
            cmpe['nME']="%s"%(5*' ')
        else:
            cmpe['nME']="%5.1f"%(mmean)


        clmpe={}
        for k in lmpe.keys():
            kk="%3d"%(k)
            if(isundef(lmpe[k]) or iszero(lmpe[k])):
                clmpe[kk]="%s"%(5*' ')
            else:
                clmpe[kk]="%5.1f"%(lmpe[k])
        clmpe['nSE']="%5.1f"%(lsmean)

        if(isundef(lmmean)):
            clmpe['nME']="%s"%(5*' ')
        else:
            clmpe['nME']="%5.1f"%(lmmean)

        cnpe={}
        for k in npe.keys():
            kk="%3d"%(k)
            if(iszero(npe[k])):
                cnpe[kk]="%s"%(4*' ')
            else:
                cnpe[kk]="%4d"%(npe[k])
        cnpe['nSE']="%4d"%(nsg)
        if(iszero(nmg)):
            cnpe['nME']="%s"%(4*' ')
        else:
            cnpe['nME']="%4d"%(nmg)


        cgainxype={}
        for k in mpe.keys():
            kk="%3d"%(k)
            if(isundef(gainxype[k])):
                cgainxype[kk]="%s"%(5*' ')
            else:
                cgainxype[kk]="%4.0f%%"%(gainxype[k])
        cgainxype['nSE']="%4.0f%%"%(sgain)
        if(isundef(mgain)):
            cgainxype['nME']="%s"%(4*' ')
        else:
            cgainxype['nME']="%4.0f%%"%(mgain)


        return(ctaus,cmpe,cnpe,cgainxype,clmpe)




    if(doplot):
        from matplotlib import pylab as P
        from matplotlib.ticker import FormatStrFormatter
        from pylab import arange



    #mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm

    (veriopts,tau00filtopt,stmopt,stmoptall,tauls,dohomo)=vopts

    nmodels=len(models)
    lmodel=models[-1]

    ovstmids=reducestmids(vstmids[lmodel])

    rcards=[]

    nmod=nmodels
    if(dohomo): nmod=nmod-1

    if(not(dohomo)):
        rcards.append(titlecard(dohomo,models,lmodel,lmodel,tau00filtopt,vstmids[lmodel],filtdtgs))
        rcards.append(listcard(ovstmids," %s",'Storms:'))



    for n in range(0,nmod):

        model=models[n]

        rc=sstat[model]
        lrc=sstat[lmodel]

        irc=simstat[model]
        lirc=simstat[lmodel]

        crc=scnts[model]
        lcrc=scnts[lmodel]

        (npe,mpe,mcte,mate,nvme,mvme,amvme,mtcvmax,mvmep)=getstatsfromlist(rc)
        (lnpe,lmpe,lmcte,lmate,lnvme,lmvme,lamvme,lmtcvmax,lmvmep)=getstatsfromlist(lrc)

        (nimpe,p1betterpe)=irc

        (pods,pofs)=getcountsfromlist(crc)
        (lpods,lpofs)=getcountsfromlist(lcrc)

        taus=npe.keys()
        taus.sort()


        (gainxype,dmpe)=intermodelstats(models[n],lmodel,sstat,2)
        (gainxyvme,dmvme)=gainxystats(amvme,lamvme)

        (lsgain,lmgain,lnsg,lnmg,lsmean,lmmean)=StmStatOverall(lnpe,lmpe,lmcte,lmate,lnvme,lmvme,lamvme,gainxype,dmpe)

        (sgain,mgain,nsg,nmg,smean,mmean)=StmStatOverall(npe,mpe,mcte,mate,nvme,mvme,amvme,gainxype,dmpe)

        (ctaus,cmpe,cnpe,cgainxype,clmpe)=mpe2char(taus,mpe,npe,
                                                   smean,mmean,nsg,nmg,
                                                   gainxyvme,dmvme,sgain,mgain,
                                                   lmpe,lsmean,lmmean)
        #
        # count array for intermodel is the lastmodel or lnpe
        #

        putpvar(pvar,npvartag,pvartag,model,gainxype,model,lnpe,type='gainxype')
        putpvar(pvar,npvartag,pvartag,model,mpe,model,npe,type='pe')
        putpvar(pvar,npvartag,pvartag,model,amvme,model,npe,type='amvme')
        putpvar(pvar,npvartag,pvartag,model,mvme,model,npe,type='mvme')
        putpvar(pvar,npvartag,pvartag,model,mcte,model,npe,type='mcte')
        putpvar(pvar,npvartag,pvartag,model,mate,model,npe,type='mate')
        putpvar(pvar,npvartag,pvartag,model,pods,model,npe,type='pods')
        putpvar(pvar,npvartag,pvartag,model,pofs,model,npe,type='pofs')


        if(dohomo):
            rcards.append(titlecard(dohomo,models,model,lmodel,tau00filtopt,vstmids[model],filtdtgs))
            rcards.append(listcard(ovstmids," %s ",'Storms:'))

            putpvar(pvar,npvartag,pvartag,lmodel,gainxype,model,lnpe,type='gainxype')
            putpvar(pvar,npvartag,pvartag,lmodel,lmpe,lmodel,lnpe,type='pe')
            putpvar(pvar,npvartag,pvartag,lmodel,lamvme,lmodel,lnpe,type='amvme')
            putpvar(pvar,npvartag,pvartag,lmodel,lmvme,lmodel,lnpe,type='mvme')
            putpvar(pvar,npvartag,pvartag,lmodel,lmcte,lmodel,lnpe,type='mcte')
            putpvar(pvar,npvartag,pvartag,lmodel,lmate,lmodel,lnpe,type='mate')
            putpvar(pvar,npvartag,pvartag,lmodel,lpods,lmodel,lnpe,type='pods')
            putpvar(pvar,npvartag,pvartag,lmodel,lpofs,lmodel,lnpe,type='pofs')

        if(n==0):
            rcards.append(listcard(ctaus,'       %3s',' taus:'))
            rcards.append(listcard(ctaus,' ---------' ))


        rcards.append(hashcard(cmpe,ctaus,'     %s',"mpe %s:"%(model),nozero=1))


        if(dohomo):
            rcards.append(hashcard(clmpe,ctaus,'     %s',"mpe %s:"%(lmodel),nozero=1))



        rcards.append(hashcard(cnpe,ctaus,'      %4s','npe:',nozero=1))

        hd="G pe %s/%s:"%(models[n],lmodel)
        rcards.append(hashcard(cgainxype,ctaus,'     %5s',hd))

        hdbetter="%%N %s>%s:"%(models[n],lmodel)
        rcards.append(hashcard(p1betterpe,taus,'      %3.0f%%',hdbetter))

        rcards.append(hashcard(nimpe,taus,'      %4d','nimpe:',nozero=1))
        ctathd="cte/ate %s:"%(model)
        rcards.append(hashcard2(mcte,mate,taus,' %4.0f','%-4.0f',ctathd,nozero=1))
        rcards.append(hashcard(pods,taus,'      %4d','pod %s:'%(model),nozero=0))
        rcards.append(hashcard(pofs,taus,'      %4d','pof %s:'%(model),nozero=0))
        if(dohomo):
            ctathd="cte/ate %s:"%(lmodel)
            rcards.append(hashcard2(lmcte,lmate,taus,' %4.0f','%-4.0f',ctathd,nozero=1))
            rcards.append(hashcard(lpods,taus,'      %4d','pod %s:'%(lmodel),nozero=0))
            rcards.append(hashcard(lpofs,taus,'      %4d','pof %s:'%(lmodel),nozero=0))

        rcards.append('')

        mvehd="amvme/bias %s:"%(model)
        rcards.append(hashcard2(amvme,mvme,taus,' %4.0f','%-4.0f',mvehd,nozero=1))
        mvehd="TCvmx/fcvmx %s:"%(model)
        rcards.append(hashcard2(mtcvmax,mvmep,taus,' %4.0f','%-4.0f',mvehd,nozero=1))
        if(dohomo):
            mvehd="amvme/bias %s:"%(lmodel)
            rcards.append(hashcard2(lamvme,lmvme,taus,' %4.0f','%-4.0f',mvehd,nozero=1))
            mvehd="TCvmx/fcvmx %s:"%(lmodel)
            rcards.append(hashcard2(lmtcvmax,lmvmep,taus,' %4.0f','%-4.0f',mvehd,nozero=1))

        hdvme="G VME %s/%s:"%(models[n],lmodel)
        rcards.append(hashcard(gainxyvme,taus,'       %3.0f',hdvme))
        rcards.append(hashcard(nvme,taus,'      %4d','nvme:',nozero=1))
        rcards.append('')


        if(not(dohomo)):
            rcards.append('')


    for rcard in rcards:
        print rcard

    return(rcards)



def StmStatOverall(npe,mpe,mcte,mate,nvme,mvme,amvme,gainxy,dmpe,undef=-999.):

    staus=[24,48]
    mtaus=[72,96,120]

    sgain=0.0
    smean=0.0
    nsg=0

    mgain=0.0
    mmean=0.0
    nmg=0


    for tau in staus:
        sgain=sgain+gainxy[tau]*+npe[tau]
        nsg=nsg+npe[tau]
        smean=smean+mpe[tau]*npe[tau]

    for tau in mtaus:
        mgain=mgain+gainxy[tau]*+npe[tau]
        mmean=mmean+mpe[tau]*npe[tau]
        nmg=nmg+npe[tau]

    if(nsg > 0):
        sgain=sgain/nsg
        smean=smean/nsg
    else:
        sgain=undef
        smean=undef

    if(nmg > 0):
        mgain=mgain/nmg
        mmean=mmean/nmg
    else:
        mgain=undef
        mmean=undef

    return(sgain,mgain,nsg,nmg,smean,mmean)








def PrintStmStat(models,vstmids,
                 stats,imstats,counts,
                 vopts,doplot,lsopt,
                 filtdtgs=None,
                 ):

    if(doplot):

        from matplotlib import pylab as P
        from matplotlib.ticker import FormatStrFormatter
        from pylab import arange


    #mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm

    (veriopts,tau00filtopt,stmopt,stmoptall,tauls,dohomo)=vopts

    nmodels=len(models)
    lmodel=models[-1]
    nmod=nmodels
    if(dohomo): nmod=nmod-1

    for n in range(0,nmod):

        model=models[n]

        stmids=vstmids[model]
        nstm=len(stmids)

        for m in range(0,nstm):

            stmid=stmids[m]

            rc=stats[model,stmid]
            lrc=stats[lmodel,stmid]

            (npe,mpe,mcte,mate,nvme,mvme,amvme,mtcvmax,mvmep)=getstatsfromlist(rc)
            (lnpe,lmpe,lmcte,lmate,lnvme,lmvme,lamvme,lmtcvmax,lmvmep)=getstatsfromlist(lrc)
            (gainxy,dmpe)=gainxystats(mpe,lmpe)

            (sgain,mgain,nsg,nmg,smean,mmean)=StmStatOverall(npe,mpe,mcte,mate,nvme,mvme,amvme,gainxy,dmpe)

            taus=npe.keys()
            taus.sort()

            if(dohomo):
                if(lsopt > 0):
                    print titlecard(dohomo,models,model,lmodel,tau00filtopt,[stmid],filtdtgs)

                scard=listcard([stmids[m]]," %s ",'Storms:')
                scard=scard+listcard([sgain,nsg,mgain,nmg],' %4.0f','Short (24,48) & Med (72,96,120) gain: ')
                if(lsopt == 0):
                    scard="Storm: %s %-12s "%(stmid,GetTCName(stmid))
                    if(nsg > 0):
                        scard=scard+"Sht Gain: % 5.1f [%3d]"%(sgain,nsg)
                    if(nmg > 0):
                        scard=scard+" Med Gain: % 5.1f [%3d]"%(mgain,nmg)

                print scard

            if(lsopt > 0):
                if(n==0):
                    print listcard(taus,'       %3d',' taus:')
                    print listcard(taus,' ---------' )

                print hashcard(mpe,taus,'     %5.1f',"mpe %s:"%(model))


                if(dohomo):
                    print hashcard(lmpe,taus,'     %5.1f',"mpe %s:"%(lmodel))


            if(lsopt > 0):

                hd="gain %s/%s:"%(models[n],lmodel)
                print hashcard(gainxy,taus,'       %3.0f',hd)
                print hashcard(npe,taus,'      %4d','npe:',nozero=1)

                ctathd="cte/ate %s:"%(model)
                print hashcard2(mcte,mate,taus,' %4.0f','%-4.0f',ctathd,nozero=1)
                if(dohomo):
                    ctathd="cte/ate %s:"%(lmodel)
                    print hashcard2(lmcte,lmate,taus,' %4.0f','%-4.0f',ctathd,nozero=1)

                print


                mvehd="amvme/bias %s:"%(model)
                print hashcard2(amvme,mvme,taus,' %4.0f','%-4.0f',mvehd,nozero=1)
                mvehd="TCvmx/fcvmx %s:"%(model)
                print hashcard2(mtcvmax,mvmep,taus,' %4.0f','%-4.0f',mvehd,nozero=1)
                if(dohomo):
                    mvehd="amvme/bias %s:"%(lmodel)
                    print hashcard2(lamvme,lmvme,taus,' %4.0f','%-4.0f',mvehd,nozero=1)
                    mvehd="TCvmx/fcvmx %s:"%(lmodel)
                    print hashcard2(lmtcvmax,lmvmep,taus,' %4.0f','%-4.0f',mvehd,nozero=1)

                print hashcard(nvme,taus,'      %4d','nvme:',nozero=1)
                print


                if(not(dohomo)): print



    return


def PrintFeVmeReport(models,rpt,printall=0,domissing=1):

    nmodels=len(models)
    stmids=rpt['stmids']
    for stmid in stmids:
        hcards=rpt['head',stmid]
        for m in range(0,len(hcards)):
            if(m == len(hcards)-2):
                hmodel="% 8s"%('model')
            elif(m == len(hcards)-1):
                hmodel="%s"%(8*'-')
            else:
                hmodel="%s"%(8*' ')

            hcard=hcards[m]
            print hmodel,hcard

        rdtgs=[]
        for nm in range(0,len(models)):
            try:
                rdtgs=rdtgs+rpt[models[nm],stmid].keys()
            except:
                continue

        rdtgs=mf.uniq(rdtgs)

        nc=0
        for rdtg in rdtgs:
            for n in range(0,len(models)):
                model=models[n]

                try:
                    rcard=rpt[model,stmid][rdtg]
                    invalid=(mf.find(rcard,'norn'))
                    tt=rcard.split()
                    nn=len(tt)
                    nc=nc+1
                    if(nn == 8 and n==1 and printall and not(invalid)):
                        print "%s"%(8*' '),rpt[model,stmid][rdtg]
                    elif(nn > 8 and not(invalid)):
                        vflag=tt[7][-1]
                        if(vflag == '+' or vflag == '-' or (vflag == '*' and domissing)):
                            if(n == 0): print
                            card="% 8s "%(model)+rpt[model,stmid][rdtg]
                            card=card.replace('fc','  ')
                            print card

                except:
                    continue

    return



def lsStmStat(taids,tstmids,taus,listsB,
              pdtgs=None,
              tau00filtopt='tc',
              dspltable='pe',
              verirule='tc',
              dohomo=0,
              nocphc=1,
              lsopt=5,
              tableReverse=0,
              veriwarn=0,
              printRunOnly=0,
              ):


    def sortListB():

        olistsB={}
        ndxB={}
        kk=listsB.keys()

        for k in kk:

            tt=listsB[k]

            # -- each list may have a different order of dtg, get ndx for each
            #
            dtgs=[]
            for t in tt:
                dtg=t[0][1]
                dtgs.append(dtg)
                ndxB[dtg]=tt.index(t)
            dtgs.sort()

            # -- sort
            #
            ttN=copy.copy(tt)

            for n in range(0,len(dtgs)):
                dtg=dtgs[n]
                n2=ndxB[dtg]
                ttN[n]=tt[n2]

            olistsB[k]=ttN

        return(olistsB)


    def getListB(tau,key='bdtg',iundef=1e20,oundef=-999,doundef=1):

        blist=[]
        ndxS={}

        # -- not get a bdtg list -- assumed only one storm

        #if(key == 'bdtg'):
            #kk=listsB.keys()
            #tt=listsB[kk[0]]
            #for t in tt:
                ##val=t[0][1]
                #list.append(val)

        #elif(key == 'vdtg'):
            #kk=listsB.keys()
            #tt=listsB[kk[0]]
            #print 'ttttttt',tt  
            #for t in tt:
                #btdtg=t[0][1]
                #vtdtg=mf.dtginc(btdtg,tau)
                #list.append(vtdtg)

        # -- special case for pod
        #
        if(key == 'pod'):
            tt=listsB[model,stmid,tau,key]
            for t in tt:
                lkey=t[0]
                val=t[1]

                if(type(val) != StringType):
                    # -- undef check and check if vflag set in lkey from VD.HomoVDdics
                    if(doundef):
                        if(lkey[0] == 0 and val == 1): val=0

                blist.append(val)

        else:
            ikey=key
            if(key == 'vdtg'): ikey='bdtg'
            tt=listsB[model,stmid,tau,ikey]
            for t in tt:
                lkey=t[0]
                val=t[1]
                if(key == 'vdtg'): val=mf.dtginc(val, tau)
                if(type(val) != StringType):
                    # -- undef check and check if vflag set in lkey from VD.HomoVDdics
                    if(doundef):
                        if(lkey[0] == 0): val=iundef
                        if(val == iundef): val=oundef

                blist.append(val)

        return(blist)


    def reorderByVdtg(bdtg,pe,undef=-999):

        peD={}
        rpeD={}

        vpe={}

        taus=pe.keys()
        taus.sort()

        for tau in taus:
            #print 'rrrr ',tau,pe[tau]
            for n in range(0,len(pe[tau])):
                dtgb=bdtg[n]
                peD[dtgb,tau]=pe[tau][n]
                rpeD[dtgb,tau]=undef

        #for dtg in bdtg:
        #    for tau in taus:

        lastdtg=bdtg[-1]
        for dtg in bdtg:
            for tau in taus:
                vdtg=mf.dtginc(dtg,tau)
                ldt=mf.dtgdiff(vdtg,lastdtg)
                #print 'ddddd ',dtg,vdtg,tau,peD[dtg,tau],ldt
                if(ldt >= 0):
                    rpeD[vdtg,tau]=peD[dtg,tau]

        for tau in taus:
            vpe[tau]=[]
            for dtg in bdtg:
                vdtg=mf.dtginc(dtg,tau)
                rpe=rpeD[dtg,tau]
                vpe[tau].append(rpe)
                #print 'RRRR ',dtg,tau,'vdtg: ',vdtg,rpe

        return(vpe)



    curdtg=mf.dtg()

    dotable=0
    dostats=0
    printtable=printstats=0
    printalltable=printallstats=0
    docsv=0

    if(lsopt == 2):
        dotable=0
        dostats=1

    if(lsopt >= 3):
        dotable=1
        dostats=1

    if(lsopt == 3):
        printtable=printstats=1
        printalltable=printallstats=1

    if(lsopt == 4):
        printtable=printstats=1
        dotable=1
        dostats=1

    if(lsopt == 5):
        printalltable=2
        dotable=1
        dostats=1

    if(lsopt == 6):
        docsv=1


    # stat output hashes
    #

    stats={}
    counts={}
    countsmask={}
    statcards={}

    stmpes={}
    imstats={}
    pevmerpt={}
    pevmerpt['stmids']=[]


    nmodel=0

    nmodels=len(taids)

    models=taids

    for model in taids:

        nmodel=nmodel+1

        for stmid in tstmids:

            # variable input hashes
            #

            pe={}
            cte={}
            ate={}
            vme={}
            vmep={}
            tcvmax={}
            pod={}

            ndxpe={}
            nndx={}
            nndxvme={}
            ndxtc00={}
            nndxrun={}
            nndx00filt={}
            vdtg={}
            isbt={}
            istc={}
            iswarn={}
            iscpac={}

            impe={}

            istmids=[stmid]

            tau=0

            listsB=sortListB()

            bdtg=getListB(tau,key='bdtg',doundef=0)
            tclat00=getListB(tau,'btlat',doundef=0)
            tclon00=getListB(tau,'btlon',doundef=0)
            tcvmax00=getListB(tau,'btvmax',doundef=0)

            tcflags=getListB(tau,'tcflags',doundef=0)

            (iscarq00,iscarqfc,istc00,isbt00,iswarn00,iscpac00)=IsCarqTCetc(tcflags)


            if(nocphc):
                isbt00=NdxMath(isbt00,iscpac00,'revand')
                #
                # make sure istc = 1 if istc >= 1
                #
                istc00=NdxMath(istc00,iscpac00,'revandge1')
                iswarn00=NdxMath(iswarn00,iscpac00,'revand')


            for tau in taus:

                pe[tau]=getListB(tau,'pe')
                #pod[tau]=getListB(tau,'pod',iundef=0,oundef=0)
                pod[tau]=getListB(tau,'pod',doundef=1)

                cte[tau]=getListB(tau,'cte')
                ate[tau]=getListB(tau,'ate')
                vme[tau]=getListB(tau,'vbias',doundef=1)
                tcvmax[tau]=getListB(tau,'btvmax')
                vmep[tau]=ListMath(vme[tau],tcvmax[tau],'add')
                vdtg[tau]=getListB(tau,'vdtg')
                ndxpe[tau]=ListFilter2Ndx(pe[tau],'ge0')

                tcflags=getListB(tau,'tcflags')


                (iscarq,iscarqfc,istcFC,isbtFC,iswarnFC,iscpacFC)=IsCarqTCetc(tcflags)

                istc[tau]=istcFC
                isbt[tau]=isbtFC
                iscpac[tau]=iscpacFC
                iswarn[tau]=iswarnFC

                # -- basic filter, pe >= 0 -- basic veri is TC at tau0 and tau
                #
                nndx[tau]=ndxpe[tau]

                # -- now make sure a real bt
                #
                nndx[tau]=NdxMath(nndx[tau],isbt[tau])
                ndxtc00[tau]=ListMask2Ndx(pe[tau],istc00)
                nndxvme[tau]=ListFilter2Ndx(vme[tau],'eqm999')

                # -- if only verifying warn posits
                if(veriwarn): 
                    nndx[tau]=NdxMath(nndx[tau],iswarn[tau])
                    ndxtc00[tau]=NdxMath(ndxtc00[tau],iswarn[tau])
                    nndxvme[tau]=NdxMath(nndxvme[tau],iswarn[tau])

                if(tau ==0):
                    nndx00=nndx[0]


                #
                # take out cphc
                #

                if(nocphc):
                    nndx[tau]=NdxMath(nndx[tau],iscpac[tau],'revand')
                    nndxvme[tau]=NdxMath(nndxvme[tau],iscpac[tau],'revand')
                    ndxtc00[tau]=NdxMath(ndxtc00[tau],iscpac[tau],'revand')
                    isbt[tau]=NdxMath(isbt[tau],iscpac[tau],'revand')
                    #
                    # make sure istc = 1 if istc >= 1
                    #
                    istc[tau]=NdxMath(istc[tau],iscpac[tau],'revandge1')

                #
                # maskout non tc bt
                #
                if(verirule == 'tc'):
                    nndx[tau]=NdxMath(nndx[tau],istc[tau],condition='ge1')
                    nndxvme[tau]=NdxMath(nndxvme[tau],istc[tau],condition='ge1')

                if(IsTrackModelAlias(model)):
                    vdmodel=GetTrackModelAlias(model,stmid)
                else:
                    vdmodel=model

                nndxrun[tau]=ModelRunMask(vdtg[tau],vdmodel,nndx00)
                (nndx[tau],nndx00filt[tau])=SetTau00Filt(tau00filtopt,nndx[tau],nndxrun[tau],ndxpe[tau],ndxtc00[tau],isbt00,iswarn00)
                (nndxvme[tau],nndx00filtvme)=SetTau00Filt(tau00filtopt,nndxvme[tau],nndxrun[tau],ndxpe[tau],ndxtc00[tau],isbt00,iswarn00)

                if(tau == 0):
                    n00filt=nndx00filt[tau]

                #
                # for intermodel pe comps, hit with final mask and set undefs to -999
                #
                impe[tau]=ListMask(pe[tau],nndx[tau],undef=-999.9)

            cntmask=copy.deepcopy(pe)

            # -- reverse error table to output be verifying dtg vice run dtg (bdtg)
            #

            if(tableReverse):

                vpe=reorderByVdtg(bdtg,pe,undef=-999)
                vvme=reorderByVdtg(bdtg,vme,undef=-999)
                vpod=reorderByVdtg(bdtg,pod,undef=0)
                vistc=reorderByVdtg(bdtg,istc,undef=0)


            nbdtg=len(bdtg)

            for n in range(0,nbdtg):

                if(tableReverse):
                    CountMaskFe(vpe,vpod,isbt,vistc,vdtg,bdtg,
                                nndx,nndxrun,n00filt,taus,n,cntmask,verirule=verirule,
                                veriwarn=veriwarn)
                else:

                    CountMaskFe(pe,pod,isbt,istc,vdtg,bdtg,
                                nndx,nndxrun,n00filt,taus,n,cntmask,verirule=verirule,
                                veriwarn=veriwarn)


            #
            # collect variables for inter-model comps
            #
            stmpes[model,stmid]=impe

            #
            # stats by model stmid
            #

            stats[model,stmid]=StatAnal(pe,vme,vmep,
                                        cte,ate,
                                        tcvmax,
                                        stmid,model,
                                        tclat00,tclon00,tcvmax00,
                                        nndx,nndxvme,taus)
            #
            # counts by model/stmid
            #
            counts[model,stmid]=CountAnal(isbt,istc,
                                          cntmask,nndx,nndxrun,n00filt,
                                          stmid,model,
                                          taus,verirule,dohomo=dohomo,
                                          veriwarn=veriwarn)


            countsmask[model,stmid]=cntmask

            if(docsv):
                stmcardCsvData=" %s , %-12s , %-6s ,      ,   ,  pe = Forcast or track Error , VME = VMax wind or intensity Error  , "%(stmid,GetTCName(stmid),model)
                stmcardCsv=" strm ID  , name         , aid    ,"
                if(tableReverse):
                    stmcardCsv="%s , dtg is VERIFYING dtg"%(stmcardCsv)
                else:
                    stmcardCsv="%s dtg is RUN dtg ,"%(stmcardCsv)
                print stmcardCsv
                print stmcardCsvData

            if(dotable or dostats):
                #
                # storm title
                #
                stmhdcard="Storm: %s : %-12s  Model: %-6s Tau00Filt: %s"%(stmid,GetTCName(stmid),model,tau00filtopt)
                if(printtable):
                    print
                    print stmhdcard

            tophdcard="b#    bdtg    VR0 TB WC  lat    lon  vmax   00   12   24   36   48   72   96  120    00   12   24   36   48   72   96  120"
            topudcard="--    ----    --- -- --  ---    ---  ----   --   --   --   --   --   --   --  ---    --   --   --   --   --   --   --  ---"
            bothdcard="              stat       lat    lon  vmax   00   12   24   36   48   72   96  120    00   12   24   36   48   72   96  120"
            botudcard="              ----       ---    ---  ----   --   --   --   --   --   --   --  ---    --   --   --   --   --   --   --  ---"

            if(dotable):

                if(nmodel == 1):

                    card="Storm: %s : %-12s  Model: %-6s Tau00Filt: %s"%(stmid,GetTCName(stmid),model,tau00filtopt)

                    pevmerpt['stmids'].append(stmid)
                    pevmerpt['head',stmid]=[]
                    pevmerpt['head',stmid].append(card)

                    pevmerpt['head',stmid].append(tophdcard)
                    pevmerpt['head',stmid].append(topudcard)

                    if(printtable):

                        print
                        print tophdcard
                        print topudcard

                if(tableReverse):
                    pevmerpt[model,stmid]=PrintFeVmeTable(model,printtable,
                                                          bdtg,vpe,vvme,cte,ate,tcvmax,cntmask,
                                                          tclat00,tclon00,tcvmax00,
                                                          nndx,nndxrun,n00filt,nndx00filt,
                                                          istc00,isbt00,iswarn00,iscarq00,
                                                          taus,
                                                          dspltable,printalltable,
                                                          pdtgs=pdtgs,
                                                          docsv=docsv,
                                                          printRunOnly=printRunOnly,
                                                          veriwarn=veriwarn)
                else:
                    pevmerpt[model,stmid]=PrintFeVmeTable(model,printtable,
                                                          bdtg,pe,vme,cte,ate,tcvmax,cntmask,
                                                          tclat00,tclon00,tcvmax00,
                                                          nndx,nndxrun,n00filt,nndx00filt,
                                                          istc00,isbt00,iswarn00,iscarq00,
                                                          taus,
                                                          dspltable,printalltable,
                                                          pdtgs=pdtgs,
                                                          docsv=docsv,
                                                          printRunOnly=printRunOnly,
                                                          veriwarn=veriwarn)





            if(dostats):

                if(printstats):

                    print bothdcard
                    print botudcard

                sctitle=mkscardpre(stmid,model)
                (scards)=PrintStatCards(stats[model,stmid],taus,sctitle,doprint=printstats)

                sctitle=mkscardpre(stmid,model)
                ccards=PrintCountCards(counts[model,stmid],taus,sctitle,doprint=printstats)

                statcards[model]=(scards,ccards)



    if(lsopt == 5 and len(pevmerpt) > 0):

        PrintFeVmeReport(models,pevmerpt)

        spacer='        '
        print
        print spacer,bothdcard
        print spacer,botudcard

        (scards,ccards)=statcards[models[-1]]
        ns=len(scards)
        nc=len(ccards)

        for n in range(0,ns):
            for model in models:
                pcard=statcards[model][0][n]
                print spacer,pcard
            if(n == 1 or n == 4 or n == 5): print


        print
        for n in range(0,nc):
            for model in models:
                pcard=statcards[model][1][n]
                print spacer,pcard
            if(n == 1): print




def SumStmStatAnal(models,tstmids,
                   stats,imstats,
                   counts,countsmask,lsopt,
                   filtdtgs=None):


## 00    npe,
## 01    nvme,

## 02    mpe,
## 03    ampe,
## 04    sigpe,
## 05    mcte,
## 06    amcte,
## 07    sigcte,
## 08    mate,
## 09    amate,
## 10    sigate,

##  11      mtcvmax,
##  12      amtcvmax,
##  13      sigtcvmax,

##  14      mvme,
##  15      amvme,
##  16      sigvme,

##  17      mvmep,
##  18      amvmep,
##  19      sigvmep,

##  20      vmehist,

##  21      tclat00,
##  22      tclon00,
##  23      tcvmax00,
##  24      mlat,
##  25      mlon,
##  26      mvmax,



    mbpe=2
    mepe=10

    mbmve=11
    memve=19

    mbpod=5
    mepod=6

    mbcnt=0
    mecnt=4

##     00  nfcs,
##     01  nmisss,
##     02  novers,
##     03  nmissruns,
##     04  nbts,
##     05  pods,
##     06  pofs

    mbimpe=1
    meimpe=1


    def statave(sumstat,ss,sumimstat,ii,sumcnts,cc,stmids,verb=0):

        taus=sumstat[0].keys()
        taus.sort()

        ns=len(stmids)


        for tau in taus:

            #
            # pe stats
            #

            if(verb): print
            for m in range(mbpe,mepe+1):

                sumstatnpe=float(ss[0][0][tau])
                sumstat[m][tau]=ss[0][m][tau]*sumstatnpe

                for n in range(1,ns):

                    npe2=float(ss[n][0][tau])
                    sumstatnpe=sumstatnpe+npe2

                    if(verb):
                        print 'FFF   tau,m,n: %3d %3d %3d'%(tau,m,n),' npe1/sumstat: ',\
                              npe2,sumstatnpe,\
                              '   ss[n]: ',ss[n][m][tau],\
                              '  sumstat[m]: ',sumstat[m][tau]

                    sumstat[m][tau]=sumstat[m][tau] + ss[n][m][tau]*npe2

                if(sumstatnpe> 0.0):

                    sumstat[m][tau]=sumstat[m][tau]/sumstatnpe
                    sumstat[0][tau]=int(sumstatnpe)

                    if(verb):
                        print 'FFF SSS tau,n: %3d %3d    '%(tau,m),' npe1/2/sumstat: ',\
                              sumstatnpe,\
                              '  sumstat[m]: ',sumstat[m][tau]
                else:
                    sumstat[0][tau]=0


            #
            #-------------------  intermodel pe stats
            #
            verb=0
            if(verb): print
            for m in range(mbimpe,meimpe+1):

                sumimstatnpe=float(ii[0][0][tau])
                sumimstat[m][tau]=ii[0][m][tau]*sumimstatnpe

                for n in range(1,ns):

                    npe2=float(ii[n][0][tau])
                    sumimstatnpe=sumimstatnpe+npe2

                    if(verb):
                        print 'FFFIIIII   tau,m,n: %3d %3d %3d'%(tau,m,n),' npe1/sumimstat: ',\
                              npe2,sumimstatnpe,\
                              '   ii[n]: ',ii[n][m][tau],\
                              '  sumimstat[m]: ',sumimstat[m][tau]

                    sumimstat[m][tau]=sumimstat[m][tau] + ii[n][m][tau]*npe2

                if(sumimstatnpe> 0.0):

                    sumimstat[m][tau]=sumimstat[m][tau]/sumimstatnpe
                    sumimstat[0][tau]=int(sumimstatnpe)

                    if(verb):
                        print 'FFF SSS tau,n: %3d %3d    '%(tau,m),' npe1/2/sumimstat: ',\
                              sumimstatnpe,\
                              '  sumimstat[m]: ',sumimstat[m][tau]
                else:
                    sumimstat[0][tau]=0
            verb=0



            #
            # pod/pof stats
            #
            if(verb): print
            for m in range(mbpod,mepod+1):

                sumcntsnpod=float(cc[0][0][tau])
                sumcnts[m][tau]=cc[0][m][tau]*sumcntsnpod

                for n in range(1,ns):

                    npod2=float(cc[n][0][tau])
                    sumcntsnpod=sumcntsnpod+npod2

                    sumcnts[m][tau]=sumcnts[m][tau] + cc[n][m][tau]*npod2

                    if(verb):
                        print 'PPP   tau,m,n: %3d %3d %3d'%(tau,m,n),' npod2/sumcnts: ',\
                              npod2,sumcntsnpod,\
                              '   cc[n]: ',cc[n][m][tau],\
                              '  sumcnts[m]: ',sumcnts[m][tau]

                if(sumcntsnpod> 0.0):

                    sumcnts[m][tau]=sumcnts[m][tau]/sumcntsnpod
                    sumcnts[1][tau]=int(sumcntsnpod)

                    if(verb):
                        print 'PPP SSS tau,m: %3d %3d    '%(tau,m),' sumcnts: ',\
                              sumcntsnpod,\
                              '  sumcnts[m]: ',sumcnts[m][tau]

                else:
                    sumcnts[1][tau]=0





            #
            # mve stats
            #

            if(verb): print
            for m in range(mbmve,memve+1):

                sumstatnmve=float(ss[0][1][tau])
                sumstat[m][tau]=ss[0][m][tau]*sumstatnmve

                for n in range(1,ns):

                    nmve2=float(ss[n][1][tau])
                    sumstatnmve=sumstatnmve+nmve2

                    sumstat[m][tau]=sumstat[m][tau] + ss[n][m][tau]*nmve2

                    if(verb):
                        print 'VVV   tau,m,n: %3d %3d %3d'%(tau,m,n),' nmve2/sumstat: ',\
                              nmve2,sumstatnmve,\
                              '   ss[n]: ',ss[n][m][tau],\
                              '  sumstat[m]: ',sumstat[m][tau]

                if(sumstatnmve> 0.0):

                    sumstat[m][tau]=sumstat[m][tau]/sumstatnmve
                    sumstat[1][tau]=int(sumstatnmve)

                    if(verb):
                        print 'VVV SSS tau,m: %3d %3d    '%(tau,m),' sumstat: ',\
                              sumstatnmve,\
                              '  sumstat[m]: ',sumstat[m][tau]
                else:
                    sumstat[1][tau]=0

            #
            # pod/pof stats
            #
            if(verb): print
            for m in range(mbpod,mepod+1):

                sumcntsnpod=float(cc[0][0][tau])
                sumcnts[m][tau]=cc[0][m][tau]*sumcntsnpod

                for n in range(1,ns):

                    npod2=float(cc[n][0][tau])
                    sumcntsnpod=sumcntsnpod+npod2

                    sumcnts[m][tau]=sumcnts[m][tau] + cc[n][m][tau]*npod2

                    if(verb):
                        print 'PPP   tau,m,n: %3d %3d %3d'%(tau,m,n),' npod2/sumcnts: ',\
                              npod2,sumcntsnpod,\
                              '   cc[n]: ',cc[n][m][tau],\
                              '  sumcnts[m]: ',sumcnts[m][tau]

                if(sumcntsnpod> 0.0):

                    sumcnts[m][tau]=sumcnts[m][tau]/sumcntsnpod
                    sumcnts[1][tau]=int(sumcntsnpod)

                    if(verb):
                        print 'PPP SSS tau,m: %3d %3d    '%(tau,m),' sumcnts: ',\
                              sumcntsnpod,\
                              '  sumcnts[m]: ',sumcnts[m][tau]

                else:
                    sumcnts[1][tau]=0


            #
            # counts -- sum
            #
            if(verb): print
            for m in range(mbcnt,mecnt+1):

                sumcntsncnt=float(cc[0][m][tau])
                sumcnts[m][tau]=sumcntsncnt

                for n in range(1,ns):

                    ncnt2=float(cc[n][m][tau])
                    sumcntsncnt=sumcntsncnt+ncnt2
                    sumcnts[m][tau]=sumcnts[m][tau] + ncnt2

                    if(verb):
                        print 'PPP   tau,m,n: %3d %3d %3d'%(tau,m,n),' ncnt2/sumcnts: ',\
                              ncnt2,sumcntsncnt,\
                              '   cc[n]: ',cc[n][m][tau],\
                              '  sumcnts[m]: ',sumcnts[m][tau]

                if(sumcntsncnt > 0.0):
                    sumcnts[m][tau]=int(sumcntsncnt)
                    if(verb):
                        print 'PPP SSS tau,m: %3d %3d    '%(tau,m),' sumcnts: ',\
                              sumcntsncnt,\
                              '  sumcnts[m]: ',sumcnts[m][tau]
                else:
                    sumcnts[m][tau]=0

        return




    sstat={}
    scnts={}
    simstat={}

    for model in models:

        stmids=tstmids
        nstmids=len(stmids)

        if(nstmids > 1):

            ss=[]
            cc=[]
            ii=[]

            sumstat=copy.deepcopy(stats[model,stmids[0]])
            sumcnts=copy.deepcopy(counts[model,stmids[0]])
            sumimstat=copy.deepcopy(imstats[model,stmids[0]])

            for n in range(0,nstmids):
                ss.append(stats[model,stmids[n]])
                cc.append(counts[model,stmids[n]])
                ii.append(imstats[model,stmids[n]])

            statave(sumstat,ss,sumimstat,ii,sumcnts,cc,stmids)

            #for m in range(mbpe,mepe+1):
            #    print 'SSS: ',m,sum[m][0]

        else:

            try:
                sumstat=copy.deepcopy(stats[model,stmids[0]])
                sumcnts=copy.deepcopy(counts[model,stmids[0]])
                sumimstat=copy.deepcopy(imstats[model,stmids[0]])
            except:
                print
                print "EEE unable to deepcopy stats[model,stmids[0]] [%s,None]] in localvdstat.statave()"%(model)
                print
                sys.exit()

        sstat[model]=sumstat
        scnts[model]=sumcnts
        simstat[model]=sumimstat



    return(sstat,simstat,scnts)

def GetTcVdeckHash(stmid,model,verb=0,dtglatest='2008022920',ropt=''):

    (stmid,year)=stmid.split('.')
    b1id=stmid[2]
    stmnum=stmid[0:2]
    b2id=Basin1toBasin2[b1id].lower()

    hdir="%s/%s"%(VdeckDir,year)
    sys.path.append(hdir)

    vfile="v%s%s%s_%s"%(b2id,stmnum,year,model)
    vpath="%s/%s.py"%(hdir,vfile)
    if(verb): print vpath

    if(os.path.exists(vpath)):

        timei=os.path.getctime(vpath)
        ltimei=time.localtime(timei)
        gtimei=time.gmtime(timei)
        gdtimei=time.strftime("%Y%m%d%H%M",gtimei)

        dtgmn=dtglatest +'00'
        (isphr,modelopt)=IsModelPhr(model)

        phr=mf.dtgmndiff(gdtimei,dtgmn)
        if(phr > 0):
            mf.ChangeDir(BaseDirPrcTcDat)
            bopt=''
            if(isphr):  bopt='-B'
            cmd="w2.tc.vdeck.py %s.%s  %s %s"%(stmid,year,modelopt,bopt)
            mf.runcmd(cmd,ropt)
    else:

        ###print 'pppppppppppppppppppnnnnnnnnnnnnnnneeeeeeeeeeeeeeeee ',phr
        mf.ChangeDir(BaseDirPrcTcDat)
        bopt=''
        (isphr,modelopt)=IsModelPhr(model)
        print model,modelopt,isphr
        if(isphr): bopt='-B'
        cmd="w2.tc.vdeck.py %s.%s %s %s"%(stmid,year,modelopt,bopt)
        mf.runcmd(cmd,ropt)


    try:
        impcmd="import %s as VD"%(vfile)
        exec(impcmd)
        if(verb):
            print "Opening vdecks: %s/%s"%(hdir,vfile)
    except:
        VD=None
        if(verb >= 0):
            print "FAILED to TcVitals: %s/%s.py"%(hdir,vfile)

    return(VD)



def GetVdHashVstmids(models,stmids,taus,vopts,verb=0,filtdtgs=None):

    nmodels=len(models)

    curdtg=mf.dtg()

    (veriopts,tau00filtopt,stmopt,stmoptall,tauls,dohomo)=vopts

    vstmids={}
    vd={}

    nstms=0
    for model in models:
        for stmid in stmids:
            if(IsTrackModelAlias(model)):
                vdmodel=GetTrackModelAlias(model,stmid)
            else:
                vdmodel=model

            try:
                vd[model,stmid]=GetTcVdeckHash(stmid,vdmodel,verb=verb)
            except:
                vd[model,stmid]=None

        #
        # find stms with stats
        #

        vstmids[model]=[]

        for stmid in stmids:
            sss=[stmid]
            tau=0
            if(IsVmaxOnlyModel(model)):
                fff=GetVdListDic(vd,model,sss,tau,'tcvmax',filtdtgs)
                fff=ListFilter2Ndx(fff,'ge0')
            else:
                fff=GetVdListDic(vd,model,sss,tau,'pe',filtdtgs)
                fff=ListFilter2Ndx(fff,'ge0')
            nvalid=CountOnes(fff)
            if(nvalid > 0):
                vstmids[model].append(stmid)
                nstms=nstms+1

        #
        # uniq storms if doing comping model to self
        #
        vstmids[model]=mf.uniq(vstmids[model])


    if(nmodels > 1 and dohomo):

        vhstmids={}
        lmodel=models[-1]

        for n in range(0,nmodels-1):

            cmodel=models[n]
            for lstmid in vstmids[lmodel]:

                gotit=0
                for cstmid in vstmids[cmodel]:
                    if(cstmid == lstmid): gotit=1

                if(gotit):

                    try:
                        vhstmids[cmodel].append(lstmid)
                    except:
                        vhstmids[cmodel]=[]
                        vhstmids[cmodel].append(lstmid)

                    try:
                        vhstmids[lmodel].append(lstmid)
                    except:
                        vhstmids[lmodel]=[]
                        vhstmids[lmodel].append(lstmid)

        vstmids=vhstmids

    return(vd,vstmids,nstms)



def getcfcdata(cfcs,dtg,taus,verb=0):

    cfcdata={}
    ptaus=[-6,-12,-18,-24]

    for tau in taus:

        for ptau in ptaus:

            try:
                (outc,outf,outb)=cfcs[dtg,tau]
                c=outc[ptau][0:3]
                f=outf[ptau][0:3]
                if(verb):
                    if(c != None):
                        print 'cccccccccccccccc ',dtg,tau,ptau
                        print 'ccc ',c
                    if(f != None):
                        print 'fff ',f

            except:
                c=f=b=None


            try:
                (outc,outf,outb)=cfcs[dtg,tau]
                b=outb[ptau][0:3]
                if(verb):
                    if(b != None):
                        print 'bbb ',b

            except:
                b=None

            cfcdata[tau,ptau]=(c,f,b)

    return(cfcdata)

def getfcdata(fcs,dtg,taus):

    #fcs[bdtg,tau,'vmax']=[bvmax,fvmax,fve,fveu,fver]
    try:
        (bdir,bspd)=fcs[dtg,'mot']
    except:
        bdir=bspd=None

    fcdat={}
    fcmot={}

    fc0dist=0

    #
    # get tau0 lat/lon in case of single tau
    #
    tau0=0
    try:
        flat0=fcs[dtg,tau0][1]
        flon0=fcs[dtg,tau0][2]
    except:
        flat0=flon0=None


    for n in range(0,len(taus)):


        tau=taus[n]


        try:
            flat=fcs[dtg,tau][1]
            flon=fcs[dtg,tau][2]
            fpe=fcs[dtg,tau][5]
            bvmax=fcs[dtg,tau,'vmax'][0]
            fvmax=fcs[dtg,tau,'vmax'][1]
            fvme=fcs[dtg,tau,'vmax'][4]
            fpe=SetFEundef(fpe)
            btflgs=fcs[dtg,tau,'btflg']
        except:
            flat=flon=fvmax=fvme=bvmax=fpe=None

        if(flat != None and n > 0):
            flat0=fcs[dtg,taus[n-1]][1]
            flon0=fcs[dtg,taus[n-1]][2]

        if(tau > 0 and flat != None and chklatlat(flat,flat) ):
            fc0dist=fc0dist+GcDist(flat0,flon0,flat,flon)
        else:
            fc0dist=0

        fcdat[tau]=[flat,flon,bvmax,fvmax,fvme,fpe,fc0dist,btflgs]

    ntaus=len(taus)
    for n in range(0,ntaus):

        tau=taus[n]

        if(n == 0):
            fcspd=bspd
            fcdir=bdir

        else:

            tau0=taus[n-1]
            tau1=taus[n]

            dtau=tau1-tau0
            (flat0,flon0,bvmax0,fvmax0,fvme0,fpe0,fc0dist0,btflgs0)=fcdat[tau0]
            (flat1,flon1,bvmax1,fvmax1,fvme1,fpe1,fc0dist1,btflgs1)=fcdat[tau1]

            if(dtau > 0 and chklatlat(flat0,flat1)):
                (fcdir,fcspd,fcu,fcv)=rumhdsp(flat0,flon0,flat1,flon1,dtau)
            else:
                fcdir=-999.
                fcspd=-99.

        fcmot[tau]=[fcdir,fcspd]



    return(fcdat,fcmot)


def getlatlon(fcs,dtg,ttau):

    try:
        blat=fcs[dtg,ttau,'bt'][0]
        blon=fcs[dtg,ttau,'bt'][1]
        flat=fcs[dtg,ttau][1]
        flon=fcs[dtg,ttau][2]
        fpe=fcs[dtg,ttau][5]
        fcte=fcs[dtg,ttau][6]
        fate=fcs[dtg,ttau][7]
    except:
        blat=blon=flat=flon=fpe=fcte=fate=None

    return(blat,blon,flat,flon,fpe,fcte,fate)

def chklatlat(flat,blat):

    iokf=0
    if(flat != None and flat > -88.0 and flat < 88.0): iokf=1
    iokb=0
    if(blat != None and blat > -88.0 and blat < 88.0): iokb=1
    iok=0
    if(iokf and iokb): iok=1
    return(iok)

def undefMask(list,undef):

    ndx=[]
    for l in list:
        rc=1
        if(l == undef): rc=0
        ndx.append(rc)

    return(ndx)


def SetFEundef(pe,undef=-999.):

    if(pe < 0.0):
        pe=undef
    return(pe)




def loadlatlon(fcs,dtg1,dtg2,taus,fcsdat,fcsdtgs,baseddtg=6.0):

    fcsdtgs.append(dtg2)

    ntaus=len(taus)

    for n in range(0,ntaus):

        tau=taus[n]

        if(n > 0):
            taum1=taus[n-1]
        else:
            taum1=taus[n]

        (blat1,blon1,flat1,flon1,fpe1,fcte1,fate1)=getlatlon(fcs,dtg1,tau)
        (blat2,blon2,flat2,flon2,fpe2,fcte2,fate2)=getlatlon(fcs,dtg2,tau)
        #
        # check if fc data at both dtg1 and dtg2, if not go back baseddtg and check again...
        #
        doback12h=1
        if(doback12h):
            if(not(chklatlat(flat1,flat1)) and chklatlat(flat2,flat2) ):
                dtg1=mf.dtginc(dtg2,-2*baseddtg)
                (blat1,blon1,flat1,flon1,fpe1,fcte1,fate1)=getlatlon(fcs,dtg1,tau)
                if(not(chklatlat(flat1,flat1))):
                    dtg1=mf.dtginc(dtg2,-1*baseddtg)
                    (blat1,blon1,flat1,flon1,fpe1,fcte1,fate1)=getlatlon(fcs,dtg1,tau)

            ddtg=mf.dtgdiff(dtg1,dtg2)

            if(ddtg != baseddtg):
                (blat1m1,blon1m1,flat1m1,flon1m1,fpe1m1,fcte1m1,fate1m1)=getlatlon(fcs,dtg1,taum1)
                (blat2m1,blon2m1,flat2m1,flon2m1,fpe2m1,fcte2m1,fate2m1)=getlatlon(fcs,dtg2,taum1)
                fcsdat[dtg2,taum1]=[blat1m1,blon1m1,flat1m1,flon1m1,blat2m1,blon2m1,flat2m1,flon2m1,ddtg]

        #
        # check if dtg for earlier tau != basedtg and current tau undef...
        #
        if(n > 0):
            (blat1m1,blon1m1,flat1m1,flon1m1,blat2m1,blon2m1,flat2m1,flon2m1,ddtgm1)=fcsdat[dtg2,taum1]
        else:
            ddtgm1=baseddtg

        if(ddtgm1 != baseddtg):
            ddtg=ddtgm1
        else:
            ddtg=mf.dtgdiff(dtg1,dtg2)
        fcsdat[dtg2,tau]=[blat1,blon1,flat1,flon1,blat2,blon2,flat2,flon2,ddtg]

    return(fcsdat,fcsdtgs)

def GetVdsFromDSs(DSs,taids,tstmids,
                  taidsRelabel=None,
                  vds={},
                  verb=0,donone=1,returnlist=0):

    gotstms=[]
    if(type(tstmids) is not(ListType)):
        tstmids=[tstmids]

    if(type(taids) is not(ListType)):
        taids=[taids]

    for taid in taids:

        # -- relabeling
        #
        if(taidsRelabel != None):
            try:
                otaid=taidsRelabel[taid]
            except:
                otaid=taid
        else:
            otaid=taid

        for tstmid in tstmids:
            dskey="%s_%s"%(otaid,tstmid)
            try:
                vd=DSs.db[dskey]
                vds[otaid,tstmid]=vd
                gotstms.append(tstmid)
                if(verb): print 'VD.GetVdsFromDSs() getting: ',dskey
            except:
                if(verb > 1): print 'VD.GetVdsFromDSs() nojoy for: ',dskey
                if(donone):
                    vd=None
                    vds[otaid,tstmid]=vd

    if(len(taids) == 1 and len(tstmids) == 1 and returnlist):
        vds=vd

    if(verb and not(returnlist)):
        print 'VD.GetVdsFromDSs() vds.keys() ',vds.keys()
    return(vds)


def MakeVdeck(BT,AT,etau=120,dtau=12,
              verirule='std',
              verb=2):


    from vdCL import Vdeck

    # --- instantiate a vdeck
    #
    VD=Vdeck(etau=etau,dtau=dtau,verirule=verirule)

    btcs=BT.btcs
    btdtgs=BT.dtgs

    aid=AT.aid
    atdtgs=AT.dtgs

    # just use best track dtgs...
    #
    #dtgs=btdtgs+atdtgs
    dtgs=btdtgs
    dtgs=mf.uniq(dtgs)

    # put # of dtgs in vd
    #
    VD.ndtgs=len(dtgs)
    undef=VD.undef
    taus=VD.taus

    # aid properties
    #
    #aidprop=Aid(aid) -- use new version in ATCF.py
    aidprop=AidProp(aid)
    aidshh=aidprop.StartSynHourModel
    aidsdt=aidprop.DdtgModelTracker
    fcundef=aidprop.fcnoload
    fcvmxonly=aidprop.VmaxOnly
    fctrkonly=aidprop.TrackOnly



    # cycle by base dtgs
    #
    for bdtg in dtgs:

        try:
            ftrk=AT.atrks[bdtg]
            iokfc=1
        except:
            iokfc=0

        if(verb == 2): print 'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb ',bdtg,iokfc
        for tau in taus:

            vdtg=mf.dtginc(bdtg,tau)

            try:
                [btdic,cqdic,wndic,stdic,fldic,stdic,r34quad,r50quad]=btcs[vdtg]
                [blat,blon,bvmax,bpmin,bdir,bspd]=btdic

            except:
                (blat,blon,bvmax,bpmin,bdir,bspd)=(-99.9,-999.9,-99.9,-999.,-999.9,-99.9)
                #
                # case where aid has bad bdtg, e.g., from old 9X storm
                #
                if(tau == 0):
                    iokbdtg=0
                    break


            VD.bdtg[tau].append(bdtg)
            VD.vdtg[tau].append(vdtg)

            if(iokfc):
                try:
                    (flat,flon,fvmax,fpmin)=ftrk[tau]
                except:
                    (flat,flon,fvmax,fpmin)=fcundef
            else:
                (flat,flon,fvmax,fpmin)=fcundef


            (istc,isbt,iswarn,tsnum,tcstate,tcwarn)=VD.TcState(fldic,bvmax)

            if(tau == 0):
                bvmax00=bvmax
                tsnum00=fldic[6]
                istc00=istc
                isbt00=isbt
                iswarn00=iswarn
                isveri00=VD.IsAidStarthh(int(bdtg[8:10]),aidshh,aidsdt)


            isfctrk=VD.FcTrkState(flat)
            isveri=0
            if(VD.verirule == 'std'):
                isveri=(isveri00 and istc00 and istc and isbt)

            pod=VD.PodState(isfctrk,isveri)
            vflag=VD.VflagState(isfctrk,isveri)

            if(iokfc):
                if(verb):
                    if(tau == 0): print
                    print 'ffff 00:',bdtg,tau,vdtg,AT.stmid,BT.stmid,blat,blon,bvmax,bpmin,flat,flon,fvmax,istc,isbt,iswarn,tsnum,tcstate,tcwarn,
                    print 'ffff fc:',isveri00,istc00,istc,isbt,isveri

            VD.pod[tau].append(pod)
            VD.vflag[tau].append(vflag)

            VD.fcrunYN[tau].append(isveri)
            VD.fctrkYN[tau].append(isfctrk)
            VD.tcYN[tau].append(istc)
            VD.btYN[tau].append(isbt)
            VD.warnYN[tau].append(iswarn)
            VD.cpacYN[tau].append(VD.GetCpac(blat,blon))

            if(VD.FcTrkState(flat) == 1):
                fclf=VD.GetLF(flat,flon)
            else:
                fclf=undef

            if(VD.BtState(blat) == 1):
                btlf=VD.GetLF(blat,blon)
            else:
                btlf=undef

            if(vflag):
                VD.btlat[tau].append(blat)
                VD.btlon[tau].append(blon)
                VD.fclat[tau].append(flat)
                VD.fclon[tau].append(flon)
            else:
                VD.btlat[tau].append(undef)
                VD.btlon[tau].append(undef)
                VD.fclat[tau].append(undef)
                VD.fclon[tau].append(undef)

            VD.blf[tau].append(btlf)
            VD.flf[tau].append(fclf)


            #
            # errors
            #
            if(not(fcvmxonly) and pod == 1):
                vme=fvmax-bvmax
                if(fpmin > 0.0 and bpmin > 0.0):
                    pmine=fpmin-bpmin
                else:
                    pmine=undef
                fcvmax=fvmax
                fcpmin=fpmin
                btvmax=bvmax
                btpmin=bpmin
            else:
                vme=undef
                pmine=undef
                fcvmax=undef
                btvmax=undef
                btpmin=undef
                fcpmin=undef

            if(not(fctrkonly) and pod == 1):
                pe=gc_dist(flat,flon,blat,blon,tcunits=tcunits)
                if(tau > 0):
                    ic=taus.index(tau)
                    icm1=ic-1
                    taum1=taus[icm1]
                    dtau=tau-taum1

                    #(flat0,flon0,fvmax0,fpmin0)=ftrk[taum1]
                    #vdtgm1=mf.dtginc(bdtg,taum1)
                    #(blat0,blon0,bvmax0,bpmin0,bdir0,bspd0,btdic0,cqdic0,bwdic0,btr34quad0,btr50quad0)=btcs[vdtgm1]
                    #
                    # use rhumb line to find previous motion for ate/cte
                    #
                    (blat0,blon0)=rumltlg(bdir,bspd,-dtau,blat,blon)
                    (rr,biasx,biasy,biasew,biasns)=dist_err(blat,blon,blat0,blon0,flat,flon)
                    #print 'CCCCCCCCCC ',pe,rr,biasx,biasy
                    cte=biasx
                    ate=biasy
                else:
                    ate=0.0
                    cte=0.0
            else:
                pe=undef
                ate=undef
                cte=undef


            VD.pe[tau].append(pe)
            VD.ate[tau].append(ate)
            VD.cte[tau].append(cte)
            VD.vme[tau].append(vme)
            VD.pmine[tau].append(pmine)

            VD.btvmax[tau].append(btvmax)
            VD.fcvmax[tau].append(fcvmax)

            VD.btpmin[tau].append(bpmin)
            VD.fcpmin[tau].append(fpmin)

            if(verb == 2):
                print 'dtg ',bdtg,tau,vdtg,'iiii',bdtg,tau,istc,istc00,iswarn,isbt,tsnum,'isveri: ',isveri00,'bbbb',blat,flat,'pe ',pe



    del(VD.lf)
    VD.AT=AT
    VD.BT=BT
    VD.aid=aid
    VD.stmid=BT.stmid
    VD.aidprop=aidprop

    return(VD)


def MakeVdeckS(BT,AT,etau=168,dtau=12,
               verirule='std',
               veri9X=1,
               qcSpeed=1,
               qcPE0=1,
               pe0Max=150.0,

               #               vmaxT=35.0,
               #               vmaxM=55.0,
               # - bump up to filter out truly egregious
               #               
               vmaxT=50.0,
               vmaxM=75.0,
               dobtlen=1,
               verb=0,
               undef999=-999.0,
               doHigherOrder=1,
               tcunits='english',
               ):

    from vdCL import VdeckS

    if(doHigherOrder):
        from numpy import array
        from scipy import integrate

    def getbt4btcs(btcs,dtg):

        try:
            # --- old form
            #
            [btdic,cqdic,wndic,stdic,fldic,stdic,r34quad,r50quad]=btcs[dtg]
            [blat,blon,bvmax,bpmin,bdir,bspd]=btdic
            r34=r34quad
            rc=1
            r34m=None
            r50m=None

        except:
            # -- new form
            #
            r34=[-999.,-999.,-999.,-999.]

            try:
                (blat,blon,bvmax,bpmin,
                 cqdir,cqspd,
                 tccode,wncode,
                 bdir,bspd,cqdirtype,
                 b1id,tdo,ntrk,ndtgs,
                 r34m,r50m,alf,sname,
                 r34in,r50,depth)=btcs[dtg]

                # -- make fldic
                istc=IsTc(tccode)
                tsnum=-1
                flgtc='NT'
                if(istc):
                    tsnum=1
                    flgtc='TC'

                flgind=tccode
                flgcq=cqdirtype
                flgwn=wncode
                lf=alf

                fldic=[flgtc,flgind,flgcq,flgwn,tdo,lf,tsnum]

                if(r34in != None): r34=r34in

                if(r34m == None): r34m=-999.
                if(r50m == None): r50m=-999.

                rc=1

            except:

                (blat,blon,bvmax,bpmin,bdir,bspd,r34m,r50m)=(-99.9,-999.9,-99.9,-999.,-999.9,-99.9,-999.,-999.)
                fldic=[]
                rc=0
                # case where aid has bad bdtg, e.g., from old 9X storm
                #
                if(tau == 0): rc=-1

        return(rc,blat,blon,bvmax,bpmin,bdir,bspd,fldic,r34,r34m,r50m)

    def dvdt(f1,f0,dt,verb=0):

        if(f1 == 0.0 and f0 == 0.0):
            dvp=0.0
            dvn=0.0
            dvt=0.0

        elif(
            f1 >= 0.0 and f0 >= 0.0 or
            f1 <= 0.0 and f0 <= 0.0
            ):
            dvt=(f1+f0)*0.5*dt
            if(f1 > 0.0 or f0 > 0.0):
                dvp=dvt
                dvn=0.0
            else:
                dvn=dvt
                dvp=0.0
                dvt=abs(dvn)

            if(verb):
                if(dvt > 0.0):
                    print 'f0f1++ ',f1,f0,dvt,dvp,dvn
                else:
                    print 'f0f1-- ',f1,f0,dvt,dvp,dvn

        elif(f1 > 0.0 and f0 < 0.0):
            df=f1/(f1-f0)
            dvp=df*0.5*dt
            dvn=(df-1.0)*0.5*dt
            dvt=dvp+abs(dvn)
            if(verb): print 'f1++-- ',f1,f0,dvp,dvn,dvt

        elif(f1 < 0.0 and f0 > 0.0):
            df=f0/(f0-f1)
            dvp=df*0.5*dt
            dvn=(df-1.0)*0.5*dt
            dvt=dvp+abs(dvn)
            if(verb): print 'f0++-- ',f1,f0,dvp,dvn,dvt

        else:
            print 'EEEEEE special case ',f1,f0,dt
            sys.exit()

        return(dvp,dvn,dvt)

    # --- instantiate a vdeck
    #
    VD=VdeckS(etau=etau,dtau=dtau,verirule=verirule,veri9X=veri9X)

    aid=AT.aid
    btcs=BT.btcs
    btdtgs=BT.dtgs

    btdtgs.sort()
    
    #for btdtg in btdtgs:
    #    print 'bbb',btdtg,btcs[btdtg]

    # just use best track dtgs...now use both for RAP run every 3 h
    # no... make sure the BT has the AT dtgs, e.g., using TcData.getBT4Stmid
    #
    #dtgs=btdtgs+atdtgs
    dtgs=btdtgs
    dtgs=mf.uniq(dtgs)
    dtgs.sort()

    # put # of dtgs in vd
    #
    VD.ndtgs=len(dtgs)
    undef=VD.undef
    taus=VD.taus

    # aid properties
    #
    #aidprop=Aid(aid) use new version in ATCF.py
    aidprop=AidProp(aid,warn=0)
    aidshh=aidprop.StartSynHourModel
    aidsdt=aidprop.DdtgModelTracker
    fcundef=aidprop.fcnoload
    fcvmxonly=aidprop.VmaxOnly
    fctrkonly=aidprop.TrackOnly


    if(qcSpeed and not(fcvmxonly)):
        AT.qcMotion(stmid=AT.stmid,aid=AT.aid,
                    vmaxT=vmaxT,vmaxM=vmaxM)
    atdtgs=AT.dtgs

    VD.spdflgT=None
    VD.spdtauT=None
    VD.spdflgM=None
    VD.spdtauM=None
    VD.xspdlog=None

    if(hasattr(AT,'spdflgT')):
        VD.spdflgT=AT.spdflgT
        VD.spdtauT=AT.spdtauT
        VD.spdflgM=AT.spdflgM
        VD.spdtauM=AT.spdtauM
        VD.xspdlog=AT.xspdlog


    VD.AT=AT
    VD.BT=BT
    VD.aid=aid
    VD.stmid=BT.stmid
    VD.aidprop=aidprop
    VD.undef=undef

    # cycle by base dtgs
    #
    for bdtg in dtgs:

        try:
            ftrk=AT.atrks[bdtg]
            iokfc=1
        except:
            iokfc=0

        dvmes={}
        dbmes={}

        lenbt=0.
        lenbtfc=0.
        
        if(verb >= 1): print 'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb ',bdtg,iokfc

        # -- set qcPE0 flag
        #
        setqcPE0=0
        TE=0.0
        # -- 20190904 -- do fc len with TE since it should(?) be part of TE as a vector
        #
        lenfc=0.
        
        for tau in taus:

            vdtg=mf.dtginc(bdtg,tau)

            (rc,blat,blon,bvmax,bpmin,bdir,bspd,fldic,br34,br34m,br50m)=getbt4btcs(btcs,vdtg)


            # -- find length of bt
            #
            if(dobtlen):
                ndx=taus.index(tau)
                if(ndx > 0 and blat > -90.0):
                    taum1=taus[ndx-1]
                    vdtgm1=mf.dtginc(bdtg,taum1)
                    (rc,blatm1,blonm1,bvmaxm1,bpminm1,bdirm1,bspdm1,fldicm1,br34m1,
                     br34m1,br50m1)=getbt4btcs(btcs,vdtgm1)
                    lenbt=lenbt+gc_dist(blatm1,blonm1,blat,blon,tcunits=tcunits)

            VD.bdtg[tau].append(bdtg)

            # -- 20151214 -- set iokfcTau flag to not turn off vdeck once an undefined tau is hit
            #    originally, iokfc (entire track) was set to 0 if flat == None
            #
            if(iokfc):
                taundx=taus.index(tau)

                (flat,flon,fvmax,fpmin)=getLatLonVmaxPminFromFtrk(ftrk,tau)
                
                # -- get previous fc lat/lon
                #
                if(taundx > 0):
                    (flatP,flonP,fvmaxP,fpminP)=getLatLonVmaxPminFromFtrk(ftrk,taus[taundx-1])

                    # -- 20190904 -- handle case of skipped taus for dtau=12, e.g., ofcl
                    #
                    if(flatP == None and flat != None):
                        (flatP,flonP,fvmaxP,fpminP)=getLatLonVmaxPminFromFtrk(ftrk,taus[taundx-2])
                        if(flatP == None):
                            print 'WWW -- MakeVdeckS-flatP-TE == None for second backward try for bdtg: ',bdtg,' tau: ',tau,'aid: ',aid
                            print 'III -- set to fcundef'
                            (flat,flon,fvmax,fpmin)=fcundef
                            iokfcTau=0
                            #sys.exit()
                        
                else:
                    flatP=flat
                    flonP=flon
                    
                iokfcTau=1
                if(flat == None):
                    (flat,flon,fvmax,fpmin)=fcundef
                    iokfcTau=0
            else:
                (flat,flon,fvmax,fpmin)=fcundef
                iokfcTau=0

            # -- forecast R34
            #
            fr34=[-999.,-999.,-999.,-999.]
            if(iokfcTau and len(ftrk[tau]) > 4 and ftrk[tau][4] != None): fr34=ftrk[tau][4]


            (istc,isbt,iswarn,tsnum,tcstate,tcwarn)=VD.TcState(fldic,bvmax)

            if(tau == 0):
                bvmax00=bvmax
                fvmax00=fvmax
                
                blatm1=blat
                blonm1=blon
                
                lenbtfc=0.0

                # -- case of aid with no initial Vmax
                if(fvmax00 <= 0.0): 
                    fvmax00=bvmax00
                    fvmax=bvmax00

                tsnum00=fldic[6]
                istc00=istc
                isbt00=isbt
                iswarn00=iswarn
                isveri00=VD.IsAidStarthh(int(bdtg[8:10]),aidshh,aidsdt)
                

            isfctrk=VD.FcTrkState(flat)
            isfcvmax=VD.VmaxState(fvmax)
            isveri=0
            if(VD.verirule == 'std'):
                isveri=(isveri00 and (istc00 == 1) and (istc == 1) and isbt)
            elif(VD.verirule == 'td'):
                if(bvmax00 >= 20.0): 
                    istc00=1
                    isveri00=1
                if(bvmax >= 20.0):
                    istc=1
                    isbt=1

                isveri=(isveri00 and istc00 and istc and isbt)
                #print 'qqqqqqqqqq',bdtg,tau,bvmax00,bvmax,isveri




            iveri9X=(VD.veri9X and Is9X(VD.stmid))

            # -- if a 9X and veri9X then
            #
            if(VD.BtState(blat) == 0 and iveri9X): isbt=-1

            if(iveri9X and isbt >= 0): 
                isveri=1

            pod=VD.PodState(isfctrk,isveri,iswarn)
            vflag=VD.VflagState(isfctrk,isveri,iswarn)

            # -- if vmax only aid, calc pod/vflag based on a vmax fc
            #
            if(fcvmxonly):
                pod=VD.PodState(isfcvmax,isveri,iswarn)
                vflag=VD.VflagState(isfcvmax,isveri,iswarn)

            if(iokfcTau):
                if(verb >= 1):
                    print 'ffff iokfcTau=1 bdtg: ',bdtg,' tau: %-3d '%(tau),'ftrk: %5.1f'%(flat),flon,fvmax,fpmin,'bt: %5.1f'%(blat),blon,bvmax,tcstate,'flg: ',isveri00,istc00,istc,isbt,\
                          ' vflag,pod: ',vflag,pod
                    if(tau == 0):
                        print
                        print 'ffff 00: ',bdtg,tau,vdtg,AT.stmid,BT.stmid,blat,blon,bvmax,bpmin
                        print 'ffff fc: ',flat,flon,fvmax,istc,isbt,iswarn,tsnum,tcstate,tcwarn
                        print 'ffff flg: isveri00,istc00,istc,isbt,isveri,fldic: ',isveri00,istc00,istc,isbt,isveri,fldic

            VD.pod[tau].append(pod)
            VD.vflag[tau].append(vflag)

            if(verb > 1 and iokfcTau):
                print 'iiiiiiiiiiiiiiiiiiiiiiiiii',bdtg,tau,vdtg,AT.stmid,'istc,isbt,iswarn,tsnum,tcstate,tcwarn',istc,isbt,iswarn,tsnum,tcstate,tcwarn,'vflag: ',vflag
                print 'iiiiiiiiiiiiiiiiiiiiiiiiii pod: ',pod,' fcvmxonly: ',fcvmxonly

            # -- IIIIIIIIIIIIIIIIIIIEEEEEEEEEEEEEEEEEEEEEEEE - intensity errors
            #
            if(pod >= 1 and isfcvmax and pod != 999):
                vme=fvmax-bvmax
                vme0=bvmax-bvmax00
                dvme=fvmax-fvmax00
                dbme=bvmax-bvmax00

                if(tcunits == 'metric'):
                    vme=vme*knots2ms
                    vme0=vme0*knots2ms
                    dvme=dvme*knots2ms
                    dbme=dbme*knots2ms


                dvmes[tau]=dvme
                dbmes[tau]=dbme
                if(verb >=1): print '000000 ',tau,'vme: ',vme,'fvmax/00: ',fvmax,fvmax00,'bvmax/00: ',bvmax,bvmax00,' dvf/b: ',dvme,dbme

                if(fpmin > 0.0 and bpmin > 0.0):
                    pmine=fpmin-bpmin
                else:
                    pmine=undef999
                    
                fcvmax=fvmax
                fcpmin=fpmin
                btvmax=bvmax
                btpmin=bpmin
            else:
                vme=undef999
                vme0=undef999
                pmine=undef999
                fcvmax=undef999
                btvmax=bvmax
                btpmin=bpmin
                fcpmin=undef999

            ## -- RRRRRRRRRRR3333333333333444444444444444 - R34 errors
            ##
            fcbtr34=WindRadiiMetric([br34,fr34],'r34')
            r34err=fcbtr34[1]-fcbtr34[0]
            VD.r34e[tau].append(r34err)
            VD.r34bt[tau].append(fcbtr34[0])
            VD.r34fc[tau].append(fcbtr34[1])

            #print 'eeee333444: ',bdtg,tau,r34e,fcbtr34

            # -- PPPPPPPPPPPPPPPPEEEEEEEEEEEEEEEEEEEEE Position Errors -- calc if pod >= 1  and a BT available (pod != 999)
            #
            if(not(fcvmxonly) and pod >= 1 and pod != 999):
                
                pe=gc_dist(flat,flon,blat,blon,tcunits=tcunits)
                
                lenbtfc=lenbtfc+gc_dist(blatm1,blonm1,blat,blon,tcunits=tcunits)
                blatm1=blat
                blonm1=blon
                
                if(pe > pe0Max and tau == 0 and qcPE0):
                    setqcPE0=1
                    print 'WWWWWWWW -- PE0 > %s'%(pe0Max),'tau: ',tau,'bdtg: ',bdtg,' aid: ',aid,' bdtg: ',bdtg

                if(setqcPE0 and qcPE0):
                    pe=undef
                    ate=undef
                    cte=undef
                    ikeBT=undef
                    FE=undef
                    FE0=undef
                
                if(tau >= 0):
                    ic=taus.index(tau)
                    icm1=ic-1
                    taum1=taus[icm1]
                    dtau=tau-taum1

                    #(flat0,flon0,fvmax0,fpmin0)=ftrk[taum1]
                    #vdtgm1=mf.dtginc(bdtg,taum1)
                    #(blat0,blon0,bvmax0,bpmin0,bdir0,bspd0,btdic0,cqdic0,bwdic0,btr34quad0,btr50quad0)=btcs[vdtgm1]
                    #
                    # use rhumb line to find previous motion for ate/cte
                    #
                    # 20130409 -- hmmm now that we're doing tau0...
                    #
                    (blat0,blon0)=rumltlg(bdir,bspd,-dtau,blat,blon)
                    if(blat0 == None):
                        biasx=undef
                        biasy=undef
                    else:
                        (rr,biasx,biasy,biasew,biasns)=dist_err(blat,blon,blat0,blon0,flat,flon)

                    #print 'CCCCCCCCCC ',pe,rr,biasx,biasy
                    cte=biasx
                    ate=biasy
                    if(tcunits == 'metric'):
                        cte=cte*nm2km
                        ate=ate*nm2km
                else:
                    ate=0.0
                    cte=0.0
                    
                    
                # --- TTTTTTTTTTTTTTTTTTTTTEEEEEEEEEEEEEEEEEEEEEEEEEE  Track Error
                #
                if(tau > 0):
                    pt1=[flatP,flonP]
                    pt2=[flat,flon]
                    if(blatm1 > -90 and blat> -90):
                        pt3=[blatm1,blonm1] 
                        pt4=[blat,blon]
                        TEcur=getTrackArea(pt1, pt2, pt3, pt4,
                                           aid,tau,bdtg,AT.stmid,
                                           verb=verb)
                        lenfc=lenfc+gc_dist(flatP,flonP,flat,flon,tcunits=tcunits)
                    else:
                        TEcur=0.0
                        lenfc=0.0
                            
                    if(TEcur == None): 
                        TEcur=0.0
                        
                    TE=TE+TEcur
                        
                    if(tcunits == 'metric'): TE=TE*nm2km
                        
                    if(verb):
                        print 'stm: %s aid: %-7s bdtg: %s tau: %3d'%(AT.stmid,aid,bdtg,tau),'FC: %5.1f %6.1f BT: %5.1f %6.1f PE: %4.0f TE: %5.0f TEcur: %5.0f BTlen: %5.0f'%\
                              (flat,flon,blat,blon,pe,TE,TEcur,lenbt)
                        

                VmaxBTin=bvmax
                R34BTin=br34m
                PE=pe
                IE=vme
                IE0=vme0
                FE=-999.
                FE0=-999.
                if(pe != undef):
                    try:
                        (ikeBT,ikeFC,R34BT,FE,FE0)=makeIkeErrSimple(VmaxBTin, R34BTin, PE, IE) 
                    except:
                        print 'EEE -- error in makeIkeErrSimple for ',bdtg,BT.stmid
                        ikeBT=undef
                if(verb):
                    print 'qqqqq---- %03d'%(tau),'VmaxBTin: %3d'%(VmaxBTin),'R34BTin: %5.0f '%(R34BTin),\
                          'IE: %3.0f '%(IE),'IE0: %3.0f '%(IE0),'ikeBT: %5.1f'%(ikeBT),'ikeFC: %5.1f'%(ikeFC),\
                          'PE: %5.1f'%(PE),'R34BT: %5.0f'%(R34BT),'FE: %5.1f '%(FE),'FE0: %5.1f'%(FE0)


            else:
                
                pe=undef
                ate=undef
                cte=undef
                ikeBT=undef
                FE=undef
                FE0=undef


            if(verb >= 1): print 'FFF-PE bdtg: ',bdtg,' tau: ',tau,'PE,ATE,CTE: ',pe,ate,cte,' pod: ',pod


            # -- lenbt + scaled pe
            #
            pescaled=undef

            if(pe != undef and dobtlen):
                if(tau == 0):
                    pescaled=pe/IPerror
                elif(lenbt > 0):
                    pescaled=pe/lenbt

                # -- make percent
                #
                pescaled=pescaled*100.0

            VD.btlen[tau].append(lenbt)
            VD.spe[tau].append(pescaled)
            
            VD.btfclen[tau].append(lenbtfc)
            VD.fclen[tau].append(lenfc)
            
            # -- 20190904 -- seems to work...
            #print 'LLLLL stmid: ',VD.stmid,'tau: ',tau,' aid: ',VD.aid,'BTlen: ',lenbtfc,' FClen: ',lenfc

            VD.pe[tau].append(pe)
            VD.ate[tau].append(ate)
            VD.cte[tau].append(cte)
            VD.vme[tau].append(vme)
            VD.pmine[tau].append(pmine)

            VD.ikeBT[tau].append(ikeBT)
            VD.FE[tau].append(FE)
            VD.FE0[tau].append(FE0)
            VD.TE[tau].append(TE)

            if(tcunits == 'metric'):
                VD.btvmax[tau].append(btvmax*knots2ms)
                VD.btpmin[tau].append(btpmin)
                VD.fcvmax[tau].append(fcvmax*knots2ms)
                VD.fcpmin[tau].append(fcpmin)
            else:
                VD.btvmax[tau].append(btvmax)
                VD.btpmin[tau].append(btpmin)
                VD.fcvmax[tau].append(fcvmax)
                VD.fcpmin[tau].append(fcpmin)

            if(not(doHigherOrder)):
                continue    

            if(verb == 2):
                if(tau == 0): print
                print 'fffffffffffffffffffffffffff dtg ',bdtg,tau,vdtg,'istc: ',istc,tcstate,' 00:',istc00,iswarn,isbt,tsnum,'isveri: ',isveri,'bbbb',blat,flat,'pe ',pe

            # -- NNNNNNNNNNIIIIIIIIIIICCCCCCCCCCCCCCCEEEEEEEEEEEEEEEEE - net intensity change
            #

            dtaus=dvmes.keys()
            dtaus.sort()

            ddtau=0

            nicf=0.0
            nicfp=0.0
            nicfn=0.0
            nicfd=0.0

            nicb=0.0
            nicbp=0.0
            nicbn=0.0
            nicbd=0.0

            nicfa=0.0
            nicba=0.0

            x=[]
            yf=[]
            yfp=[]
            yfn=[]

            yb=[]
            ybp=[]
            ybn=[]

            x.append(0.0)

            yf.append(0.0)
            yfp.append(0.0)
            yfn.append(0.0)

            yb.append(0.0)
            ybp.append(0.0)
            ybn.append(0.0)

            for n in range(1,len(dtaus)):

                x0=dtaus[n]
                yf0=dvmes[dtaus[n]]
                yb0=dbmes[dtaus[n]]

                x.append(x0)

                yf.append(yf0)
                if(yf0 > 0.0):
                    yfp.append(yf0)
                else:
                    yfp.append(0.0)

                if(yf0 < 0.0):
                    yfn.append(yf0)
                else:
                    yfn.append(0.0)

                yb.append(yb0)
                if(yb0 > 0.0):
                    ybp.append(yb0)
                else:
                    ybp.append(0.0)

                if(yb0 < 0.0):
                    ybn.append(yb0)
                else:
                    ybn.append(0.0)

            # -- get t*dt
            #

            for n in range(1,len(dtaus)):

                dt=dtaus[n]-dtaus[n-1]
                ddtau=ddtau+dt


            nicf=nicfp=nicfn=0.0
            nicb=nicbp=nicbn=0.0

            # -- use numpy to integrate + and - area
            #

            if(ddtau > 0.0):

                x=array(x)

                yf=array(yf)
                yfp=array(yfp)
                yfn=array(yfn)

                nicf=integrate.simps(yf,x)/ddtau
                nicfp=integrate.simps(yfp,x)/ddtau
                nicfn=integrate.simps(yfn,x)/ddtau
                nicfd=nicfp+nicfn
                nicf=abs(nicf)

                # -- BT
                #
                nicb=integrate.simps(yb,x)/ddtau
                nicbp=integrate.simps(ybp,x)/ddtau
                nicbn=integrate.simps(ybn,x)/ddtau
                nicbd=nicbp+nicbn
                nicb=abs(nicb)

            nice=nicf-nicb
            niceb=nicfd-nicbd
            if(vme == undef):
                nicf=nicb=nicfa=nicba=undef
                nice=nicea=niceb=undef

            VD.btnic[tau].append(nicb)
            VD.fcnic[tau].append(nicf)
            VD.btnicp[tau].append(nicbp)
            VD.fcnicp[tau].append(nicfp)
            VD.btnicn[tau].append(nicbn)
            VD.fcnicn[tau].append(nicfn)
            VD.nice[tau].append(nice)
            VD.niceb[tau].append(niceb)

            if(vme != undef and verb):
                print 'ddd333---- ',bdtg,' tau: %03d'%(tau),'vme: %4.0f'%(vme),'  nicf %5.1f'%(nicf),' nicfp %5.1f'%(nicfp),' nicfn:  %5.1f'%(nicfn)
                print 'dddbbb---- ',bdtg,' tau: %03d'%(tau),'vme: %4.0f'%(vme),'  nicb %5.1f'%(nicb),' nicbp %5.1f'%(nicbp),' nicbn:  %5.1f'%(nicbn)
                print 'ddd333---- ',bdtg,' tau: %03d'%(tau),'vme: %4.0f'%(vme),'  nicf %5.1f'%(nicf),'  nicb %5.1f'%(nicb),'  nice:  %+5.1f'%(nice)
                print 'ddd333---- ',bdtg,' tau: %03d'%(tau),'vme: %4.0f'%(vme),' nicfd %5.1f'%(nicfd),' nicbd %5.1f'%(nicbd),' niceb:  %+5.1f'%(niceb)




    return(VD)


def getLatLonVmaxPminFromFtrk(ftrk,tau):

    try:
        rc=ftrk[tau]

        flat=rc[0]
        flon=rc[1]
        fvmax=rc[2]
        fpmin=rc[3]

    except:
        flat=flon=fvmax=fpmin=None

    return (flat,flon,fvmax,fpmin)




def MakeVdeckSDtg(BT,AT,tdtg,etau=120,dtau=12,
                  verirule='std',
                  qcSpeed=1,
                  qcPE0=150.0,
                  vmaxT=35.0,
                  vmaxM=55.0,
                  verb=0):

    from vdCL import VdeckS

    # --- instantiate a vdeck
    #
    VD=VdeckS(etau=etau,dtau=dtau,verirule=verirule)

    btcs=BT.btcs
    btdtgs=BT.dtgs

    aid=AT.aid
    if(qcSpeed):
        AT.qcMotion(stmid=AT.stmid,aid=AT.aid,
                    vmaxT=vmaxT,vmaxM=vmaxM)
    atdtgs=AT.dtgs

    VD.spdflgT=None
    VD.spdtauT=None
    VD.spdflgM=None
    VD.spdtauM=None

    if(hasattr(AT,'spdflgT')):
        VD.spdflgT=AT.spdflgT
        VD.spdtauT=AT.spdtauT
        VD.spdflgM=AT.spdflgM
        VD.spdtauM=AT.spdtauM


    # just use best track dtgs...
    #
    #dtgs=btdtgs+atdtgs
    dtgs=btdtgs
    dtgs=mf.uniq(dtgs)

    # put # of dtgs in vd
    #
    VD.ndtgs=len(dtgs)
    undef=VD.undef
    taus=VD.taus

    # aid properties
    #
    aidprop=Aid(aid)
    aidshh=aidprop.StartSynHourModel
    aidsdt=aidprop.DdtgModelTracker
    fcundef=aidprop.fcnoload
    fcvmxonly=aidprop.VmaxOnly
    fctrkonly=aidprop.TrackOnly


    # cycle by base dtgs
    #
    if(not(tdtg in dtgs)):
        print 'VD.MakeVdeckSDtg: tdtg: ',tdtg,' not in possible dtgs...return None'
        VD=None
        return(VD)


    try:
        ftrk=AT.atrks[tdtg]
        iokfc=1
    except:
        iokfc=0

    if(verb == 2): print 'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb ',tdtg,iokfc
    for tau in taus:

        vdtg=mf.dtginc(tdtg,tau)

        #try:
        [btdic,cqdic,wndic,stdic,fldic,stdic,r34quad,r50quad]=btcs[tdtg]
        [blat,blon,bvmax,bpmin,bdir,bspd]=btdic

        #except:
        #    (blat,blon,bvmax,bpmin,bdir,bspd)=(-99.9,-999.9,-99.9,-999.,-999.9,-99.9)
        #    #
        #    # case where aid has bad vdtg, e.g., from old 9X storm
        #    #
        #    if(tau == 0):
        #        iokvdtg=0
        #        break


        VD.bdtg[tau].append(vdtg)

        if(iokfc):
            try:
                (flat,flon,fvmax,fpmin)=ftrk[tau]
            except:
                (flat,flon,fvmax,fpmin)=fcundef
        else:
            (flat,flon,fvmax,fpmin)=fcundef


        (istc,isbt,iswarn,tsnum,tcstate,tcwarn)=VD.TcState(fldic,bvmax)

        if(tau == 0):
            bvmax00=bvmax
            tsnum00=fldic[6]
            istc00=istc
            isbt00=isbt
            iswarn00=iswarn
            isveri00=VD.IsAidStarthh(int(vdtg[8:10]),aidshh,aidsdt)


        isfctrk=VD.FcTrkState(flat)
        isveri=0
        if(VD.verirule == 'std'):
            isveri=(isveri00 and istc00 and istc and isbt)

        pod=VD.PodState(isfctrk,isveri,iswarn)
        vflag=VD.VflagState(isfctrk,isveri,iswarn)

        if(iokfc):
            if(verb):
                if(tau == 0): print
                print 'ffff 00:',vdtg,tau,vdtg,AT.stmid,BT.stmid,blat,blon,bvmax,bpmin,flat,flon,fvmax,istc,isbt,iswarn,tsnum,tcstate,tcwarn,
                print 'ffff fc:',isveri00,istc00,istc,isbt,isveri

        VD.pod[tau].append(pod)
        VD.vflag[tau].append(vflag)

        #
        # errors
        #
        if(not(fcvmxonly) and pod == 1 and fvmax > 0):
            vme=fvmax-bvmax
            if(fpmin > 0.0 and bpmin > 0.0):
                pmine=fpmin-bpmin
            else:
                pmine=undef
            fcvmax=fvmax
            fcpmin=fpmin
            btvmax=bvmax
            btpmin=bpmin
        else:
            vme=undef
            pmine=undef
            fcvmax=undef
            btvmax=undef
            btpmin=undef
            fcpmin=undef

        if(not(fctrkonly) and pod == 1):
            pe=gc_dist(flat,flon,blat,blon)
            if(tau > 0):
                ic=taus.index(tau)
                icm1=ic-1
                taum1=taus[icm1]
                dtau=tau-taum1

                #(flat0,flon0,fvmax0,fpmin0)=ftrk[taum1]
                #vdtgm1=mf.dtginc(vdtg,taum1)
                #(blat0,blon0,bvmax0,bpmin0,bdir0,bspd0,btdic0,cqdic0,bwdic0,btr34quad0,btr50quad0)=btcs[vdtgm1]
                #
                # use rhumb line to find previous motion for ate/cte
                #
                (blat0,blon0)=rumltlg(bdir,bspd,-dtau,blat,blon)
                (rr,biasx,biasy,biasew,biasns)=dist_err(blat,blon,blat0,blon0,flat,flon)
                #print 'CCCCCCCCCC ',pe,rr,biasx,biasy
                cte=biasx
                ate=biasy
            else:
                ate=0.0
                cte=0.0
        else:
            pe=undef
            ate=undef
            cte=undef

        print 'eeeeeeeeeeeeeeeeee pe: ',pe,ate,cte,vme,pmine

        VD.pe[tau].append(pe)
        VD.ate[tau].append(ate)
        VD.cte[tau].append(cte)
        VD.vme[tau].append(vme)
        VD.pmine[tau].append(pmine)

        VD.btvmax[tau].append(btvmax)
        VD.btpmin[tau].append(btpmin)
        VD.fcvmax[tau].append(fcvmax)
        VD.fcpmin[tau].append(fcpmin)

        if(verb == 2):
            print 'dtg ',vdtg,tau,vdtg,'iiii',vdtg,tau,istc,istc00,iswarn,isbt,tsnum,'isveri: ',isveri00,'bbbb',blat,flat,'pe ',pe



    VD.aid=aid
    VD.stmid=BT.stmid
    VD.aidprop=aidprop

    return(VD)


def ModelRunMaskOld(bdtgs,model):

    from ATCF import AidProp

    # -- new form in ATCF.py
    aP=AidProp(model)

    dtaumodel=aP.DdtgModelTracker
    synhrmodel=aP.StartSynHourModel

    rmask=[]
    for dtg in bdtgs:
        hh=dtg[8:]
        runmodel=1

        if(dtaumodel == 12):
            if(synhrmodel == 0 and (hh == '06' or hh == '18') ): runmodel=0
            if(synhrmodel == 6 and (hh == '00' or hh == '12') ): runmodel=0
            if(synhrmodel == 12 and (hh == '06' or hh == '18') ): runmodel=0

        rmask.append(runmodel)

    return(rmask)




def getCountsVds(vds,taus=[0,24,72,120],
                 filt0012=0,
                 filt00=0,
                 filt12=0,
                 filtPof=0,
                 filt0618=0,
                 filtVmax35=0,
                 stmidsByDtgs=None,
                 verb=0,
                 veriwarn=None,                 
                 warn=0,
                 ):
    """
20131206-
get counts of verifiable v forecast posits to get prob of detection (pod) and prob of overwarn (poo)
last looked at in 201107...modified Vdeck.PodState to better represent the state of a forecast

not sure if filtPof means anything now---did in WI at Madison talk
"""
    #mmmmmmmmmmmmmmmmmmmmmmmmmmmmm - to analysis pod/pof/por
    #

    vflagMax=1
    if(veriwarn != None): vflagMax=2

    MF=MFutils()

    counts={}

    vkeys=vds.keys()

    countstmids={}

    vkeys.sort()

    for vkey in vkeys:

        aid=vkey[0]
        stmid=vkey[1]
        isshem=isShemBasinStm(stmid)

        vd=vds[vkey]

        if(vd == None): continue

        # -- setup bdtgs and ibdtgs (dtgs to process) from stmidsByDtgs
        #
        bdtgs=vd.bdtg[0]
        ibdtgs=bdtgs

        if(stmidsByDtgs != None):
            try:
                ibdtgs=stmidsByDtgs[stmid.upper()]
            except:
                if(warn): print 'WWW(getCountsVds): no dtgs for stmid: ',stmid
                ibdtgs=[]


        pods00=vd.pod[0]
        vmax00=vd.btvmax[0]

        for tau in taus:

            pods=vd.pod[tau]
            vmaxs=vd.btvmax[tau]

            nveri=0
            nverifc=0
            nverifcover=0

            ndxModelRun=ModelRunMaskOld(bdtgs,aid)
            for n in range(0,len(bdtgs)):

                bdtg=bdtgs[n]

                # -- check if bdtg in ibdtgs
                #
                if(not(bdtg in ibdtgs)):
                    continue

                # -- synoptic hh filter
                #
                hh=bdtg[8:10]
                if(filt0012 and not(hh == '00' or hh == '12')): continue
                if(filt0618 and not(hh == '06' or hh == '18')): continue
                if(filt00  and not(hh == '00')): continue
                if(filt12  and not(hh == '12')): continue

                # -- get flags; only need pod flag
                #
                pod=pods[n]
                pod00=pods00[n]
                vmax=vmaxs[n]
                vmax0=vmax00[n]

                if(filtVmax35 and vmax0 < 35): continue
                
                modelrun=ndxModelRun[n]

                if(veriwarn != None):
                    pod00chk=(pod00 == 2 or pod00 == -2)
                    podchk=(pod == 2 or pod == -2)
                    pod00chkFC=(pod00 == 2)
                    podchkFC=(pod == 2)
                    #podchk=podchkFC
                    #pod00chk=pod00chkFC

                    if(filtPof):
                        pod00chk=(pod00 == 2)
                        podchk=((pod == 2 or pod == -2))
                        pod00chkFC=(pod00 == 2)
                        podchkFC=((pod == 2 or pod == -2))

                else:

                    pod00chk=(pod00 == 1 or pod00 == -1 or pod00 == 2 or pod00 == -2)
                    podchk=(pod == 1 or pod == -1 or pod == 2 or pod == -2)
                    pod00chkFC=(pod00 == 1 or pod00 == 2)
                    podchkFC=(pod == 1 or pod == 2)

                    if(filtPof):
                        pod00chk=(pod00 >= 1 and pod00 != 999)
                        pod00chkFC=(pod00 >= 1 and pod00 != 999)
                        podchk=(pod >= 1 or pod <= -1 and pod != 999)
                        podchkFC=(pod >= 1 and pod != 999)

                if(pod00chk and podchk and modelrun):
                    nveri=nveri+1
                    if(verb): print 'YYY--: ',aid,stmid,tau,bdtg,' pod: ',pod,' pod00: ',pod00,' nveri: ',nveri

                if(filtPof):
                    if(podchkFC and modelrun): nverifc=nverifc+1
                else:
                    if(podchkFC and pod00chkFC and modelrun): nverifc=nverifc+1

                if(pod == 999 and pod00chk and modelrun): nverifcover=nverifcover+1

                if(verb): print 'NNN--: %3d'%(tau),bdtg,veriwarn,' pod: %3d'%(pod),' pod00: %3d'%(pod00),'modelrun: ',modelrun,n,' podchk: ',\
                  podchk,'pod00chk: ',pod00chk

            #cases[taid,stmid,dtg,tau,verikey]=(stmid,vmax,vvar)
            counts[aid,stmid,tau]=(nveri,nverifc,nverifcover)
            if(verb): print 'TTT----: %10s %3d %s'%(aid,tau,stmid),' nveri: %3d'%(nveri),' nverifc: %3d'%(nverifc),' nverifcover: %3d'%(nverifcover)

    if(verb):

        kk=counts.keys()
        kk.sort()
        for k in kk:
            print 'CCC: ',k,counts[k]

    return(counts)





def getVdDss(source,tstmid,taid,verb=1):

    dbtype='vdeck'

    year=tstmid.split('.')[1]
    dsbdir="%s/DSs"%(TcDataBdir)

    dbname="%s_%s_%s"%(dbtype,source,year)
    dbfile="%s.pypdb"%(dbname)

    vDSs=DataSets(bdir=dsbdir,name=dbfile,dtype=dbtype,verb=verb)

    vdkey="%s_%s"%(taid,tstmid)
    vD=vDSs.getDataSet(vdkey)

    return(vD)



def GetVdsFromDSs(DSs,taids,tstmids,
                  taidsRelabel=None,
                  vds={},
                  verb=0,donone=1,returnlist=0):

    gotstms=[]
    if(type(tstmids) is not(ListType)):
        tstmids=[tstmids]

    if(type(taids) is not(ListType)):
        taids=[taids]

    for taid in taids:

        # -- relabeling
        #
        if(taidsRelabel != None):
            try:
                otaid=taidsRelabel[taid]
            except:
                otaid=taid
        else:
            otaid=taid

        for tstmid in tstmids:
            dskey="%s_%s"%(otaid,tstmid)
            try:
                vd=DSs.db[dskey]
                vds[otaid,tstmid]=vd
                gotstms.append(tstmid)
                if(verb): print 'VD.GetVdsFromDSs() getting: ',dskey
            except:
                if(verb > 1): print 'VD.GetVdsFromDSs() nojoy for: ',dskey
                if(donone):
                    vd=None
                    vds[otaid,tstmid]=vd

    if(len(taids) == 1 and len(tstmids) == 1 and returnlist):
        vds=vd

    if(verb and not(returnlist)):
        print 'VD.GetVdsFromDSs() vds.keys() ',vds.keys()
    return(vds)

def getVdFromDSs(DSs,taid,tstmid,
                 verb=0):

    vd=None
    dskey="%s_%s"%(taid,tstmid)
    try:    
        vd=DSs.db[dskey]
        gotstms.append(tstmid)
        if(verb): print 'VD.GetVdsFromDSs() getting: ',dskey
    except:
        if(verb > 1): print 'VD.GetVdsFromDSs() nojoy for: ',dskey

    if(verb):
        print 'VD.getVdFromDSs() got: ',taid,tstmid

    return(vd)


def putVdToDSs(DSs,vd,taid,tstmid,verb=0):

    # -- keys
    #
    dskey="%s_%s"%(taid,tstmid)

    try:
        dskCur=DSs.db['keys'].getData()
    except:
        dskCur=[]

    dskCur.append(dskey)

    dsk=DataSet(name='dskeys',dtype='hash')
    dsk.data=dskCur
    DSs.putDataSet(dsk,'keys')

    # -- put the vdeck
    #
    DSs.putDataSet(vd,dskey,verb=verb)    



def logicalAndVDlists(list1,list2,warn=0,verb=0):

    olist1=[]
    olist2=[]

    # check if lists begin with the same dtg/stm...

    if(len(list1) == 0 or len(list2) == 0):
        if(warn): print 'WWW len(list1) or len(list2) == 0; return'
        return(olist1,olist2)

    ll10=list1[0]
    ll20=list2[0]

    k10=ll10[0][1]
    k20=ll10[0][2]

    k11=ll20[0][1]
    k21=ll20[0][2]


    stmid0=k20
    stmid1=k21

    #if( ( (stmid0 == 'undef' and stmid1 != 'undef') and (stmid0 != 'undef' and stmid1 == 'undef') )
    #    and k10 == k11):
    #    print 'WWW stmid0 is undef and stmid1 != undef; but dtg0 = dtg1; return []',k10,k11,len(list1),len(list2)
    #    return(olist1,olist2)


    if(not(k10 == k11)):
        if(verb):
            print 'EEE list1 and list2 in VD.logicalAndVDlists(list1,list2) do NOT start with same dtg/stm...',k10,k10,k20,k21
            print 'list1[0]: ',ll10,' list2[0]: ',ll20

    if(not(k20 == k21)):
        if(verb):
            print ' list1 and list2 in VD.logicalAndVDlists(list1,list2) do NOT start with same STMID...',k10,k10,k20,k21

    jstart=0
    for i in range(0,len(list1)):
        ll=list1[i]
        k11=ll[0][1]
        k21=ll[0][2]

        gotj=0
        for j in range(jstart,len(list2)):
            ll=list2[j]
            k12=ll[0][1]
            k22=ll[0][2]

            if(k11 == k12 and k21 == k22):
                gotj=1
                jval=j
                ival=i
                jstart=j-1
                break

        if(gotj):
            olist1.append(list1[ival])
            olist2.append(list2[jval])


    return(olist1,olist2)



def VDList2Dict(list):

    dic={}

    for i in range(0,len(list)):
        k1=list[i][0][1]
        k2=list[i][0][2]
        kk="%s.%s"%(k1,k2)
        #print 'kkkkk ',kk,list[i]
        dic[kk]=list[i]

    return(dic)

def Dict2VDList(dic):

    kk=dic.keys()
    kk.sort()

    list=[]
    for k in kk:
        list.append(dic[k])

    return(list)


def ForceHomoVDlists(l0,l1,aid0,aid1,verb=1):

    if(verb):
        print 'ForceHomoVDlists 0000000000000000000000000000000 aid: ',aid0,' len: ',len(l0)
        if(verb > 1):
            for ll in l0:  print ll
        print 'ForceHomoVDlists 1111111111111111111111111111111 aid: ',aid1,' len: ',len(l1)
        if(verb > 1):
            for ll in l1:  print ll

    (l0,l1)=logicalAndVDlists(l0,l1)


    return(l0,l1)



def HomoVDdics(dics,aids,tstmid,tau,tstmids=[],forcehomo=1,verb=1,warn=0,error=1,undefE20=1e+20,
               maxLenDiff=5000):
    #verb=2
    if(len(aids) == 1):
        return(dics)
    else:

        # -- homo by stmids too...
        #

        nstms=len(tstmids)

        nstmids=1
        if(nstms > 0): nstmids=nstms
        for ns in range(0,nstmids):
            for npass in range(1,len(aids)):
                for i in range(1,len(aids)):
                    aid0=aids[i-1]
                    aid1=aids[i]
                    if(nstms > 0):
                        try:
                            l0=dics[aid0,tstmids[ns]]
                        except:
                            l0=[]
                        try:
                            l1=dics[aid1,tstmids[ns]]
                        except:
                            l1=[]
                    else:
                        try:
                            l0=dics[aid0]
                        except:
                            l0=[]
                        try:
                            l1=dics[aid1]
                        except:
                            l1=[]
                    if(len(l0) != len(l1)):
                        dlength=abs(len(l0)-len(l1))
                        if(forcehomo or dlength <= maxLenDiff):
                            if(warn or verb):
                                print 'WWW HomoDics length error aid0: ',aid0,len(l0),' aid1: ',aid1,len(l1),' run VD.ForceHomoVDlists... tstmid: ',tstmid,'  tau: ',tau
                            (l0,l1)=ForceHomoVDlists(l0,l1,aid0,aid1,verb=verb)
                        else:
                            if(error):
                                print '*****EEE HomoDics length error aid0: ',aid0,len(l0),' aid1: ',aid1,len(l1),' and dlength: ',dlength,' is bigger than maxLenDiff: ',maxLenDiff,'sayoonara in VD.HomoVDdics EEE****'
                            sys.exit()

                    # handle veriflag == 1 (TC) or 2 (TC and warning)
                    #
                    for j in range(0,len(l0)):
                        flg0=l0[j][0][0]
                        flg1=l1[j][0][0]
                        val0=float(l0[j][-1])
                        val1=float(l1[j][-1])
                        und0=(val0 == undefE20)
                        und1=(val1 == undefE20)
                        #print 'asdfasdf',j,'flg0',flg0,'flg1',flg1,'000---',l0[j],'111---',l1[j]
                        diff0=(flg0 == 0 or und0)
                        diff1=(flg1 == 0 or und1)
                        #print '0000111',diff0,diff1
                        diff2=( (flg0 and flg1) or (flg0 and flg1) )
                        diff2=(diff0 or diff1)

                        if( diff2 ):
                            l0[j][0][0]=0
                            l1[j][0][0]=0
                            if(verb > 1): print 'changing vflag ',npass,i,j,'diff0,diff1',diff0,diff1,l0[j],l1[j],aid0,aid1

                    if(nstms > 0):
                        dics[aid0,tstmids[ns]]=l0
                        dics[aid1,tstmids[ns]]=l1
                        
                        if(verb > 1):
                            
                            print '0000000'
                            for ll0 in l0:
                                if(ll0[0][0] != 0):
                                    print '00',tau,aid0,ll0[0],ll0[-1]
                                
                            print '1111111'
                            for ll1 in l1:
                                if(ll1[0][0] != 0):
                                    print '11',tau,aid1,ll1[0],ll1[-1]

                    else:
                        dics[aid0]=l0
                        dics[aid1]=l1

    return(dics)




class VdList(MFbase):

    def __init__(self,list,key):
        self.list=list
        self.key=key
        self.list2dict()

    def list2dict(self):

        self.dict={}
        for n in range(0,len(self.list)):

            ll=self.list[n]

            kflg=ll[0][0]
            kdtg=ll[0][1]
            kstm=ll[0][2]
            kvmx=ll[0][3]

            val=ll[1]
            self.dict[kdtg,kstm]=[n,val,kflg,kvmx]

    def filterDtgs(self,fdtgs):

        odict={}

        kk=self.dict.keys()
        for k in kk:
            (dtg,stm)=k
            if(dtg in fdtgs):
                odict[k]=self.dict[k]

##             if(len(fdtgs) == 1):
##                 fdtg=fdtgs[0]
##                 delta=MF.DtgDiff(fdtg,dtg)
##                 if(delta >= 0.0):
##                     #print 'ddd ',delta,dtg,fdtg
##                     odict[k]=self.dict[k]
##             elif(len(fdtgs) == 2):
##                 fdtg0=fdtgs[0]
##                 fdtg1=fdtgs[1]
##                 delta0=MF.DtgDiff(fdtg0,dtg)
##                 delta1=MF.DtgDiff(dtg,fdtg1)
##                 if(delta0 >= 0.0 and delta1 >= 0.0):
##                     #print 'qqqqq ',delta0,delta1,'fff ',fdtg0,dtg,fdtg1
##                     odict[k]=self.dict[k]


        self.dict=odict



    def filterSynoptic(self,fopt='00'):

        odict={}

        kk=self.dict.keys()
        for k in kk:
            (dtg,stm)=k
            hh=dtg[8:10]
            if(fopt == '00' and (hh == '00')): 
                odict[k]=self.dict[k]
            if(fopt == '12' and (hh == '12')): 
                odict[k]=self.dict[k]

            if(fopt == '0012' and ((hh == '00') or (hh == '12'))): 
                odict[k]=self.dict[k]

            if(fopt == '0618' and ((hh == '06') or (hh == '18'))): 
                odict[k]=self.dict[k]


        self.dict=odict





    def dict2list(self):

        self.list=[]
        kk=self.dict.keys()
        for k in kk:
            (kdtg,kstm)=k
            (n,val,kflg,kvmx)=self.dict[k]

            l0=[kflg,kdtg,kstm,kvmx]
            l1=val
            self.list.append([l0,l1])


    def lsList(self,kflg=1):

        for n in range(0,len(self.list)):
            ll=self.list[n]
            lflg=ll[0][0]
            val=ll[1]
            card='n: %4d flg: %1d '%(n,ll[0][0]) + " %s  %s  %6s "%(ll[0][1],ll[0][2],str(ll[0][3])) + '   val: %10.4g'%(val)
            if((kflg == 1 and lflg) or (kflg == 0) ):
                print card

    def lsDict(self):

        kk=self.dict.keys()
        kk.sort()

        for k in kk:
            print 'k: ',k,self.dict[k]

    def copy(self):
        import copy

        lcopy=copy.deepcopy(self)

        return(lcopy)

    def reduce(self):

        vals=[]

        for n in range(0,len(self.list)):
            ll=self.list[n]
            lflg=ll[0][0]
            if(lflg): vals.append(ll[1])


        self.vals=vals





class VdLists(VdList):

    def __init__(self,L1,L2):

        self.L1=L1
        self.L2=L2

    def compLists(self,type='and',verb=0):

        d1=self.L1.dict
        d2=self.L2.dict
        k1=d1.keys()
        k1.sort()

        for k in k1:

            l1=d1[k]
            try: l2=d2[k]
            except: l2=None

            kflg1=kval1=None
            if(l2 != None):
                kval1=l1[1]
                kflg1=l1[2]

            kflg2=kval2=None
            if(l2 != None):
                kval2=l2[1]
                kflg2=l2[2]

            if(type == 'and'):

                if(kflg1 and kflg2 == 0):
                    val=self.L1.dict[k]
                    val[2]=0
                    self.L1.dict[k]=val
                    if(verb): print '1111111111111 set dict1 kflg2=0',k

                elif(kflg1 == 0 and kflg2 == 1):
                    val=self.L2.dict[k]
                    val[2]=0
                    self.L2.dict[k]=val
                    if(verb): print '2222222222222 set dict2 kflg1=0',k

                if(kflg1 and kflg2):
                    if(verb): print 'AAAAAAAAAAAAA ',k,' l1: ',kflg1,kval1,'l2: ',kflg2,kval2

        return


    def lagLists(self,dtau=12,verb=1):

        d1=self.L1.dict
        d2=self.L2.dict

        if(verb):
            print
            print 'list1 BEFORE: '
            self.L1.lsList()
            print

        k1s=d1.keys()
        k1s.sort()

        nfound=0
        for k1 in k1s:

            l1=d1[k1]
            dtg1=k1[0]
            stm1=k1[1]
            dtg2=mf.dtginc(dtg1,dtau)
            k2=(dtg2,stm1)

            [n1,val1,kflg1,kvmx1]=l1

            try:
                l2=d2[k2]
                [n2,val2,kflg2,kvmx2]=l2
                kflg=(kflg1 and kflg2)
                if(kflg):
                    nfound=nfound+1
                    l2=[n1,val2,kflg,kvmx2]
                else:
                    l2=[n1,val1,kflg,kvmx1]

            except:
                kflg=0
                kflg2=0
                l2=[n1,val1,kflg,kvmx1]

            l1=[n1,val1,kflg,kvmx1]

            d1[k1]=l1
            d2[k1]=l2

            if(kflg and verb):
                print 'k1: ',k1,' l1: %7.1f'%(l1[1]),' l2: %7.1f'%(l2[1]),' k2: ',k2

        self.L1.dict=d1
        self.L2.dict=d2

        self.L1.dict2list()
        self.L2.dict2list()

        if(verb):
            print
            print 'list1 after: '
            self.L1.lsList()

            print
            print 'list2 after: '
            self.L2.lsList()

            print 'fffffffffff nfound: ',nfound

        self.L1.reduce()
        v1=self.L1.vals

        self.L2.reduce()
        v2=self.L2.vals

        for n in range(0,len(v1)):
            if(v1[n] > 150.0 or v2[n] > 150.0):
                print n,"v1: %7.2f  v2: %7.2f  dv: %7.2f"%(v1[n],v2[n],v1[n]-v2[n])


        print 'lllllllllllllll ',len(v1),len(v2)

        from scipy import linspace, polyval, polyfit, sqrt, stats, randn
        from pylab import plot, title, show , legend, scatter

        #(ar,br)=polyfit(v1,v2,1)
        #xr=polyval([ar,br],v1)
        scatter(v1,v2)
        #plot(v1,xr,'r')
        gradient, intercept, r_value, p_value, std_err = stats.linregress(v1,v2)
        print "Gradient and intercept", gradient, intercept
        print "R-squared", r_value**2
        print "p-value", p_value
        print "std_err: ",std_err
        title("""$R^2$ = %5.3f"""%(r_value**2))
        #legend(['lag0','lag12'])
        print stats.corrcoef(v1,v2)
        show()

def setVD2PlotVars(ptype,pcase,toptitle1=None,toptitle2=None,do2ndval=0,dohfiptitle=0):

    do2ndval=0
    dohfiptitle=0
    doErrBar=1

    if(ptype == 'pe' or ptype == 'gainxype'):
        
        pverikey='pe'
        pverikey1=pverikey
        if(mf.find(pcase,'ens') and dohfiptitle ):
            do1stplot=1
            do2ndplot=0
            toptitle1='HFIP 2009 Summer Demo Period -- Hi-Res Ensemble Systems -- Mean v Spread'
        else:
            do1stplot=0
            do2ndplot=1
            if(toptitle1 == None): toptitle1="Generic toptitle1, pcase: %s"%(pcase)

        if(dohfiptitle):
            if(pcase == 'ens.f8mn'):
                toptitle2='21 Member FIM G8 (30 km) using EnKF perturbation'
            elif(pcase == 'ens.gkmn'):
                toptitle2='21 Member GFS (T382) using EnKF'
            elif(pcase == 'ens.eemn'):
                toptitle2='51 Member ECMWF EPS (T399) using tropical SVs'
            else:
                toptitle2=None

        if(ptype == 'gainxype'): doErrBar=0

    elif(ptype == 'fe' or ptype == 'gainxyfe'):
        pverikey='fe'
        pverikey1=pverikey
        do1stplot=0
        do2ndplot=1
        if(ptype == 'gainxyfe'): doErrBar=0
        if(toptitle1 == None): toptitle1="Generic toptitle1, pcase: %s"%(pcase)

    elif(ptype == 'pe-frac' or ptype == 'pe-pcnt'):
        pverikey='pe'
        pverikey1=pverikey
        do1stplot=0
        do2ndplot=1   # this is the bar
        doErrBar=0
        if(toptitle1 == None): toptitle1="Generic toptitle1, pcase: %s"%(pcase)
    
    elif(ptype == 'pe-imp' or ptype == 'pe-imps'):
        pverikey='pe'
        pverikey1=pverikey
        do1stplot=0
        do2ndplot=1   # this is the bar
        doErrBar=0
        if(toptitle1 == None): toptitle1="Generic toptitle1, pcase: %s"%(pcase)
        
    elif(ptype == 'fe-imp' or ptype == 'fe-imps'):
        pverikey='fe'
        pverikey1=pverikey
        do1stplot=0
        do2ndplot=1   # this is the bar
        doErrBar=0
        if(toptitle1 == None): toptitle1="Generic toptitle1, pcase: %s"%(pcase)
    
    elif(ptype == 'fe-norm'):
        pverikey='fe'
        pverikey1=pverikey
        do1stplot=0
        do2ndplot=1   # this is the bar
        doErrBar=0
        if(toptitle1 == None): toptitle1="Generic toptitle1, pcase: %s"%(pcase)
        
    elif(ptype == 'te' or ptype == 'gainxyte'):
        pverikey='te'
        pverikey1=pverikey
        do1stplot=0
        do2ndplot=1
        if(ptype == 'gainxyte'): doErrBar=0
        if(toptitle1 == None): toptitle1="Generic toptitle1, pcase: %s"%(pcase)

    elif(ptype == 'fe0'):
        pverikey='fe0'
        pverikey1=pverikey
        do1stplot=0
        do2ndplot=1
        if(toptitle1 == None): toptitle1="Generic toptitle1, pcase: %s"%(pcase)
        
    elif(ptype == 'gainxyfe0'):
        pverikey='gainfe0'
        pverikey1=pverikey
        do1stplot=0
        do2ndplot=1
        doErrBar=0
        if(toptitle1 == None): toptitle1="Generic toptitle1, pcase: %s  ptype: %s"%(pcase,ptype)
        
    elif(ptype == 'fe-line'):
        ptype='fe'
        pverikey='fe'
        pverikey1=pverikey
        do1stplot=1
        do2ndplot=0

    elif(ptype == 'fe0'):
        pverikey='fe0'
        pverikey1='fe'
        do1stplot=1
        do2ndplot=2
        do2ndval=1

        if(toptitle1 == None): toptitle1="Generic toptitle1, pcase: %s"%(pcase)
        if(toptitle2 == None):
            toptitle2='...set for fe0'

    elif(ptype == 'pe-fe'):
        pverikey='pe'
        pverikey1='fe'
        do1stplot=1
        do2ndplot=2
        do2ndval=1

        if(toptitle1 == None): toptitle1="Generic toptitle1, pcase: %s"%(pcase)
        if(toptitle2 == None):
            toptitle2='...set for pe-fe'

    elif(ptype == 'fe0'):
        pverikey='fe0'
        pverikey1='fe'
        do1stplot=1
        do2ndplot=2
        do2ndval=1

        if(toptitle1 == None): toptitle1="Generic toptitle1, pcase: %s"%(pcase)
        if(toptitle2 == None):
            toptitle2='...set for fe0'

    elif(ptype == 'pe-line'):
        ptype='pe'
        pverikey='pe'
        pverikey1=pverikey
        do1stplot=1
        do2ndplot=0

    elif(ptype == 'fe-line'):
        ptype='fe'
        pverikey='fe'
        pverikey1=pverikey
        do1stplot=1
        do2ndplot=0

    elif(ptype == 'spe'):
        pverikey='spe'
        pverikey1=pverikey
        do1stplot=0
        do2ndplot=1

    elif(ptype == 'gainxyvmax'):
        pverikey='vme'
        pverikey1=pverikey
        do1stplot=0
        do2ndplot=1

    elif(ptype == 'pbetter'):
        pverikey=ptype
        pverikey1=pverikey
        do1stplot=0
        do2ndplot=1

    elif(ptype == 'vbias'):
        pverikey='vbias'
        pverikey1='vme'
        do1stplot=1
        do2ndplot=1
        do2ndval=1

        if(toptitle1 == None): toptitle1="Generic toptitle1, pcase: %s"%(pcase)
        if(toptitle2 == None):
            toptitle2='Bias = mean(diff) -- bars ; Error = mean(abs(diff)) -- lines'

    elif(ptype == 'ct-ate'):
        pverikey1='cte'
        pverikey='ate'
        do1stplot=1
        do2ndplot=1
        do2ndval=1

        if(toptitle1 == None): toptitle1="Generic toptitle1, pcase: %s"%(pcase)
        #toptitle2='Bias = mean(diff) -- bars ; Error = mean(abs(diff)) -- lines'

    elif(ptype == 'at-cte'):
        pverikey1='ate'
        pverikey='cte'
        do1stplot=1
        do2ndplot=1
        do2ndval=1

        if(toptitle1 == None): toptitle1="Generic toptitle1, pcase: %s"%(pcase)
        #toptitle2='Bias = mean(diff) -- bars ; Error = mean(abs(diff)) -- lines'

    elif(ptype == 'rmspe'):
        pverikey='pe'
        pverikey1='rmspe'
        do1stplot=1
        do2ndplot=1
        do2ndval=-1

        if(toptitle1 == None): toptitle1="Generic toptitle1, pcase: %s"%(pcase)
        toptitle2='RMS -- line ; Error = bar'

    elif(ptype == 'nice'):
        pverikey='niceb'
        pverikey1='nice'
        do1stplot=1
        do2ndplot=1
        do2ndval=1

        if(toptitle1 == None): toptitle1="Generic toptitle1, pcase: %s"%(pcase)
        if(toptitle2 == None):
            toptitle2='Bias = mean(diff) -- bars ; Error = mean(abs(diff)) -- lines'

    elif(ptype == 'pbias'):
        pverikey='pbias'
        pverikey1='pmine'
        do1stplot=1
        do2ndplot=1
        do2ndval=1
        if(toptitle2 == None):
            toptitle2='Bias = mean(diff) -- bars ; Error = mean(abs(diff)) -- lines'

    elif(ptype == 'pod'):
        pverikey='pod'
        pverikey1='over'

        do1stplot=1
        do2ndplot=1
        do2ndval=-1 # have pod 1st in table cells

        if(toptitle2 == None):
            toptitle2='Prob Of Detection [POD;%] -- bars ; Prob Of Overwarn [POO;%] -- lines'
        #ostats=ssPOD.ostats
        #ostatsB=ssPOD.ostatsB
        doErrBar=0

    elif(ptype == 'pod-line'):
        ptype='pod'
        pverikey='pod'
        pverikey1=pverikey

        do1stplot=1
        do2ndplot=0

        if(toptitle2 == None):
            toptitle2='Prob Of Detection [POD;%] -- line'
        #ostats=ssPOD.ostats
        #ostatsB=ssPOD.ostatsB
        doErrBar=0

    elif(ptype == 'pof'):
        pverikey='pod'
        pverikey1='over'
        do1stplot=1
        do2ndplot=1
        do2ndval=1

        if(toptitle2 == None):
            toptitle2='Prob Of Forecast [POF;%] -- bars ; Prob Of Overwarn [POO;%] -- lines'
        ostats=ss.ostats

    elif(ptype == 'gainxyvbias'):
        pverikey='vbias'
        pverikey1='vbias'
        do1stplot=0
        do2ndplot=1

        if(toptitle2 == None):
            toptitle2='Ratio abs(bias)/mean(abs) Intensity Error [%] :: percentage of Error from bias'

    elif(ptype == 'r34e'):
        pverikey='r34e'
        pverikey1='r34bt'
        do1stplot=1
        do2ndplot=1
        do2ndval=1
        if(toptitle1 == None): toptitle1="Generic toptitle1, pcase: %s"%(pcase)

    return(pverikey,pverikey1,do1stplot,do2ndplot,do2ndval,doErrBar,
           toptitle1,toptitle2)


def getPodFiltOpts(ptype,filterOpts):

    filtPof=0
    if(ptype == 'pof'): filtPof=1

    filt0012=0
    filt0618=0
    filt00=0
    filt12=0
    filtVmax35=0

    for filterOpt in filterOpts:
        if(filterOpt.upper() == 'Z0012'): filt0012=1
        if(filterOpt.upper() == 'Z0618'): filt0618=1
        if(filterOpt.upper() == 'Z00'):   filt00=1
        if(filterOpt.upper() == 'Z12'):   filt12=1
        if(filterOpt.upper() == 'V35'):   filtVmax35=1

    return(filtPof,filt0012,filt0618,filt00,filt12,filtVmax35)



def lsVD2_Cache(dsbdirVD2,verb=0):

    from ATCF import aidDescTechList
    V2DSs={}

    ad=aidDescTechList()

    aidsAll=[]
    vd2s=glob.glob('%s/vdeck2*pypdb'%(dsbdirVD2))
    if(len(vd2s) == 0):
        print 'vd2a.lsVD2_Casche -- no vdecks in dsbdirVD2: ',dsbdirVD2,'sayounara...'
        sys.exit()
    for vd2 in vd2s:
        (vdir,vfile)=os.path.split(vd2)
        (vbase,vext)=os.path.splitext(vfile)
        year=vbase.split('_')[-1]
        print
        print 'In vd2 Cache: ',vd2,' for year: ',year
        V2DSs[year]=DataSets(bdir=vdir,name=vfile,verb=verb)
        vd2=V2DSs[year]
        kk=vd2.getDataSet('keys')
        kk=kk.data

        storms=[]
        basins=[]
        aidbystorms={}
        stormsbybasin={}
        for k in kk:
            (aid,storm)=k.split("_")
            aidsAll.append(aid)
            MF.appendDictList(aidbystorms,storm,aid)
            storms.append(storm)
            b1id=storm[2]
            MF.appendDictList(stormsbybasin,b1id,storm)
            basins.append(b1id)

        storms=mf.uniq(storms)
        basins=mf.uniq(basins)

        for basin in basins:
            print
            print 'Basin: ',"""'%s' ="""%(basin),Basin1toBasinName[basin]
            storms=stormsbybasin[basin]
            storms=mf.uniq(storms)
            storms.sort()
            for storm in storms:
                card="%s: "%(storm)
                aids=mf.uniq(aidbystorms[storm])
                for aid in aids:
                    card="%s %6s,"%(card,aid)
                print card[0:-1]

    print
    aidsAll=mf.uniq(aidsAll)
    for aid in aidsAll:
        descA=ad.getAidDesc(aid)
        print '%7s'%(aid),' :: ',descA

    sys.exit()


def getFinalTaidsVD2(getaids,vtaids,verb=0):

    # -- check if aliases; put in ogetaids
    #
    ogetaids=[]
    
    for getaid in getaids:
        if(len(getaid.split(':')) == 2):
            ogetaids.append(getaid.split(':')[-1])
        else:
            ogetaids.append(getaid)

    taidsFinal=ogetaids
    #taidsFinal=taids

    # -- order the output aids by the input, but include only aids in the vdecks
    #
    otaids=[]
    for ftaid in taidsFinal:
        for otaid in vtaids:
            if( (otaid == ftaid and not(otaid in otaids)) or 
                (ftaid == 'hfip' and not(ftaid in otaids)) or
                (ftaid == 'hfipj' and not(ftaid in otaids)) or
                (ftaid == 'hclp' and not(ftaid in otaids)) or
                (ftaid == 'hfip20' and not(ftaid in otaids)) 
                ): otaids.append(ftaid)


    # -- uniq sorts...turned for for some reason...20130410 -- uncomment for this case:
    # vda rtfim9,rtfim_r2220intfc150g9 -S e.11,l.11,e.12,l.12 -T fr2220g9:fim9,fim9
    # -- 20130503 -- added code to handle dups in getFinalAidsByRelabel() when relabeling
    #
    #if(len(taidsFinal) != len(otaids)):
    #    print 'EEEE error outputing the aids in order of input...taids: ',taids,' otaids: ',otaids
    #    sys.exit()

    if(verb): print 'OOOO final otaids: ',otaids

    taids=otaids

    if(len(taids) == 0):
        print 'EEE(%s) no aids for getaids: ',getaids,' could also be a problem with bd2...'
        sys.exit()

    return(taids)

def getPvarivars(ptype,pcase,toptitle1):

    doErrBar=0
    do2ndplot=0
    do2ndval=0
    toptitle2=None

    if(ptype == 'pe' or ptype == 'gainxype'):
        pverikey='pe'
        pverikey1=pverikey
        do1stplot=0
        do2ndplot=1
        doErrBar=1
        if(ptype == 'gainxype'): doErrBar=0

    elif(ptype == 'fe' or ptype == 'gainxyfe'):
        pverikey='fe'
        pverikey1=pverikey
        do1stplot=0
        do2ndplot=1
        doErrBar=1
        if(ptype == 'gainxyfe'): doErrBar=0
        
    elif(ptype == 'te' or ptype == 'gainxyte'):
        pverikey='te'
        pverikey1=pverikey
        do1stplot=0
        do2ndplot=1
        doErrBar=1
        if(ptype == 'gainxyte'): doErrBar=0
        
    elif(ptype == 'pe-line'):
        ptype='pe'
        pverikey='pe'
        pverikey1=pverikey
        do1stplot=1
        do2ndplot=0

    elif(ptype == 'fe-line'):
        ptype='fe'
        pverikey='fe'
        pverikey1=pverikey
        do1stplot=1
        do2ndplot=0

    elif(ptype == 'fe0'):
        ptype='fe'
        pverikey='fe'
        pverikey1='fe0'
        do1stplot=1
        do2ndplot=2
        do2ndval=1
        doErrBar=0
        
    elif(ptype == 'pe-fe'):
        ptype='pe'
        pverikey='pe'
        pverikey1='fe'
        do1stplot=1
        do2ndplot=2
        do2ndval=1
        doErrBar=0

    elif(ptype == 'spe'):
        pverikey='spe'
        pverikey1=pverikey
        do1stplot=0
        do2ndplot=1

    elif(ptype == 'gainxyvmax'):
        pverikey='vme'
        pverikey1=pverikey
        do1stplot=0
        do2ndplot=1

    elif(ptype == 'pbetter'):
        pverikey=ptype
        pverikey1=pverikey
        do1stplot=0
        do2ndplot=1

    elif(ptype == 'vbias'):
        pverikey='vbias'
        pverikey1='vme'
        do1stplot=1
        do2ndplot=1
        do2ndval=1

        if(toptitle1 == None): toptitle1="Generic toptitle1, pcase: %s"%(pcase)
        toptitle2='Bias = mean(diff) -- bars ; Error = mean(abs(diff)) -- lines'

    elif(ptype == 'rmspe'):
        pverikey='pe'
        pverikey1='rmspe'
        do1stplot=1
        do2ndplot=1
        do2ndval=-1

        if(toptitle1 == None): toptitle1="Generic toptitle1, pcase: %s"%(pcase)
        toptitle2='RMS -- line ; Error = bar'

    elif(ptype == 'nice'):
        pverikey='niceb'
        pverikey1='nice'
        do1stplot=1
        do2ndplot=1
        do2ndval=1

        if(toptitle1 == None): toptitle1="Generic toptitle1, pcase: %s"%(pcase)
        toptitle2='Bias = mean(diff) -- bars ; Error = mean(abs(diff)) -- lines'

    elif(ptype == 'pbias'):
        pverikey='pbias'
        pverikey1='pmine'
        do1stplot=1
        do2ndplot=1
        do2ndval=1

        toptitle2='Bias = mean(diff) -- bars ; Error = mean(abs(diff)) -- lines'

    elif(ptype == 'pod'):
        pverikey='pod'
        pverikey1='over'

        do1stplot=1
        do2ndplot=1
        do2ndval=-1 # have pod 1st in table cells

        toptitle2='Prob Of Detection [POD;%] -- bars ; Prob Of Overwarn [POO;%] -- lines'
        doErrBar=0

    elif(ptype == 'pod-line'):
        ptype='pod'
        pverikey='pod'
        pverikey1='pod'

        do1stplot=1
        do2ndplot=0

    elif(ptype == 'pof'):
        pverikey='pod'
        pverikey1='over'
        do1stplot=1
        do2ndplot=1
        do2ndval=1

        toptitle2='Prob Of Forecast [POF;%] -- bars ; Prob Of Overwarn [POO;%] -- lines'

    elif(ptype == 'gainxyvbias'):
        pverikey='vbias'
        pverikey1='vbias'
        do1stplot=0
        do2ndplot=1

        toptitle2='Ratio abs(bias)/mean(abs) Intensity Error [%] :: percentage of Error from bias'

    elif(ptype == 'r34e'):
        pverikey='r34e'
        pverikey1='r34bt'
        do1stplot=1
        do2ndplot=1
        do2ndval=1
        if(toptitle1 == None): toptitle1="Generic toptitle1, pcase: %s"%(pcase)

    rc=(pverikey,pverikey1,do1stplot,do2ndplot,do2ndval,doErrBar,toptitle1,toptitle2)
    return(rc)


def getTrackArea(pt1,pt2,pt3,pt4,
                 aid,tau,bdtg,stmid,
                 verb=0,warn=0):
    
    """Track Error as sqrt(area between fc and bt line segments)
    
    """

    import math
    from area import area


    # -- local vars
    #
    # convert area units, also has error trapping
    # tested with Python24     vegaseat      01aug2005
    #create an empty dictionary
    areaD = {}
    # populate dictionary using indexing and assignment with units and conversion factors relative to sqmeter = 1.0
    # to convert x sqmeters to any of the other area units multiply by the factor
    # to convert x of any of the other area units to sqmeter divide by the factor
    # to convert x of any area unit to any of the other area units go over interim sqmeter
    # this minimizes the total number of conversion factors
    areaD['sqmeter']      = 1.0
    areaD['sqmillimeter'] = 1000000.0
    areaD['sqcentimeter'] = 10000.0
    areaD['sqkilometer']  = 0.000001
    areaD['hectare']      = 0.0001
    areaD['sqinch']       = 1550.003
    areaD['sqfoot']       = 10.76391
    areaD['sqyard']       = 1.19599
    areaD['acre']         = 0.0002471054
    areaD['sqmile']       = 0.0000003861022
    areaD['sqnm']         = areaD['sqmile']*0.868976
    
    # -- local defs
    #
    def convertArea(x, unit1, unit2):
        
        if (unit1 in areaD) and (unit2 in areaD):
            factor1 = areaD[unit1]
            factor2 = areaD[unit2]
            return factor2*x/factor1
        else:
            return False

    def intersectLines( pt1, pt2, ptA, ptB ): 
        """ this returns the intersection of Line(pt1,pt2) and Line(ptA,ptB)
            
            returns a tuple: (xi, yi, valid, r, s), where
            (xi, yi) is the intersection
            r is the scalar multiple such that (xi,yi) = pt1 + r*(pt2-pt1)
            s is the scalar multiple such that (xi,yi) = pt1 + s*(ptB-ptA)
                valid == 0 if there are 0 or inf. intersections (invalid)
                valid == 1 if it has a unique intersection ON the segment    """
    
        DET_TOLERANCE = 0.00000001
    
        # the first line is pt1 + r*(pt2-pt1)
        # in component form:
        x1, y1 = pt1;   x2, y2 = pt2
        dx1 = x2 - x1;  dy1 = y2 - y1
    
        # the second line is ptA + s*(ptB-ptA)
        x, y = ptA;   xB, yB = ptB;
        dx = xB - x;  dy = yB - y;
    
        # we need to find the (typically unique) values of r and s
        # that will satisfy
        #
        # (x1, y1) + r(dx1, dy1) = (x, y) + s(dx, dy)
        #
        # which is the same as
        #
        #    [ dx1  -dx ][ r ] = [ x-x1 ]
        #    [ dy1  -dy ][ s ] = [ y-y1 ]
        #
        # whose solution is
        #
        #    [ r ] = _1_  [  -dy   dx ] [ x-x1 ]
        #    [ s ] = DET  [ -dy1  dx1 ] [ y-y1 ]
        #
        # where DET = (-dx1 * dy + dy1 * dx)
        #
        # if DET is too small, they're parallel
        #
        DET = (-dx1 * dy + dy1 * dx)
    
        if math.fabs(DET) < DET_TOLERANCE: return (0,0,0,0,0)
    
        # now, the determinant should be OK
        DETinv = 1.0/DET
    
        # find the scalar amount along the "self" segment
        r = DETinv * (-dy  * (x-x1) +  dx * (y-y1))
    
        # find the scalar amount along the input line
        s = DETinv * (-dy1 * (x-x1) + dx1 * (y-y1))
    
        # return the average of the two descriptions
        xi = (x1 + r*dx1 + x + s*dx)/2.0
        yi = (y1 + r*dy1 + y + s*dy)/2.0
        return ( xi, yi, 1, r, s )
    
    
    def getIntersection(pt1,pt2,ptA,ptB,verb=0):
        """ prints out a test for checking by hand... """
        
        def getMaxMin(pt1,pt2):
            
            latmin=pt1[0]
            latmax=pt1[0]
            lonmin=pt1[1]
            lonmax=pt1[1]
            
            if(latmin > pt2[0]): latmin=pt2[0]
            if(latmax < pt2[0]): latmax=pt2[0]
            
            if(lonmin > pt2[1]): lonmin=pt2[1]
            if(lonmax < pt2[1]): lonmax=pt2[1]
            
            return(latmin,latmax,lonmin,lonmax)

        # -- check if none in pt1/2
        #
        if(pt1[0] == None or pt2[0] == None):
            print 'WWWW-getTrackArea-getIntersection- got None for aid: ',aid,' stmid: ',stmid,' bdtg: ',bdtg,' tau: ',tau
            rc=(None,None,None)
            return(rc)
            
        rcI = intersectLines( pt1, pt2, ptA, ptB )
           
        ilat=rcI[0]
        ilon=rcI[1]
        iflg=rcI[2]
        iR=rcI[3]
        iS=rcI[4]
        
        useLatLon=0
        # -- lat/lon check...doesn't work?
        #
        if(useLatLon):
            latok=0
            lonok=0

            if( (ilat > pt1[0] or ilat > ptA[0]) and (ilat < pt2[0] or ilat < ptB[0]) ): latok=1
            if( (ilon < pt1[1] or ilon < ptA[1]) and (ilon > pt2[1] or ilon > ptB[1]) ): lonok=1
        
            iok=0
            if(latok and lonok): iok=1

        else:
            # -- slope test from intersectLines()
            #
            iok=0
            if(iR > 0. and iS > 0.0 and ((iR+iS) <= 2.0)): iok=1

        rc=(iok,ilat,ilon)
        
        if(verb):
            print
            print "AAAAAAAAAAA ",stmid,aid,bdtg,tau
            print "Line segment #1 runs from %5.1f %6.1f to %5.1f %6.1f"%(pt1[0],pt1[1],pt2[0],pt2[1])
            print "Line segment #2 runs from %5.1f %6.1f to %5.1f %6.1f"%(ptA[0],ptA[1],ptB[0],ptB[1])
            if(useLatLon):
                print "LATmin 1: %5.1f I: %5.1f A: %5.1f"%(pt1[0],ilat,ptA[0])
                print "LATmax 1: %5.1f I: %5.1f B: %5.1f"%(pt2[0],ilat,ptB[0]),'latok: ',latok
                print "LONmin 1: %5.1f I: %5.1f A: %5.1f"%(pt1[1],ilon,ptA[1])
                print "LONmax 1: %5.1f I: %5.1f B: %5.1f"%(pt2[1],ilon,ptB[1]),'lonok: ',lonok
            print 'rcI: ',rcI,' rc: ',rc
            print
    
        return(rc)



    # -- case of start/end points identical
    #
    if( (pt1[0] == pt3[0]) and (pt1[1] == pt3[1]) ): pt3[0]=pt3[0]+0.01
    if( (pt2[0] == pt4[0]) and (pt2[1] == pt4[1]) ): pt4[0]=pt4[0]+0.01

    # -- get intersection
    #
    rc=getIntersection(pt1,pt2,pt3,pt4,verb=verb)
    isIntersection=rc[0]
    interLat=rc[1]
    interLon=rc[2]
    
    if(isIntersection == 0):
        
        tpoly={
            'type': 'Polygon',
            'coordinates': [
            [
            [pt1[1],pt1[0]],
            [pt2[1],pt2[0]],
            [pt4[1],pt4[0]],
            [pt3[1],pt3[0]],
            [pt1[1],pt1[0]]
            ]
            ]
            }
        
    elif(isIntersection == None):
        return(None)
            
    else:
        
        pti=[interLat,interLon]

        if(warn):
            print 'IIIIIIIIIIII------------- aid: %-7s bdtg: %s tau: %3d Intersection: %5.1f %6.1f  FC0: %5.1f %6.1f  FC1: %5.1f %6.1f  BT0: %5.1f %6.1f BT1: %5.1f %6.1f'%\
                  (aid,bdtg,tau,
                   interLat,interLon,
                   pt1[0],pt1[1],pt2[0],pt2[1],
                   pt3[0],pt3[1],pt4[0],pt4[1]
               )            
            
        tpoly={
            'type': 'Polygon',
            'coordinates': [
            [
            [pt1[1],pt1[0]],
            [pti[1],pti[0]],
            [pt4[1],pt4[0]],
            [pt2[1],pt2[0]],
            [pti[1],pti[0]],
            [pt3[1],pt3[0]],
            [pt1[1],pt1[0]]
            ]
            ]
            }
        


    #if(verb): print tpoly

    tarea2=area(tpoly)
    tarea2=convertArea(tarea2,'sqmeter','sqnm')
    tarea=math.sqrt(tarea2)
    return(tarea)



def makeIkeErrSimple(VmaxBTin,R34BTin,PE,IE,IEmean=15.0,IEmax=30.0,VmaxR34=35.0,R34Min=35.0,verb=0):

    from numpy import arange
    from scipy.optimize import ridder
    from scipy.integrate import quad
    from math import pow,exp,acos,log,pi

    def ikeTS(R18,R33):
        ike=-46.42 + 0.352*R18 + 0.00007*(R18-305.97)*(R18-305.97) + 0.187*R33 - 0.004*(R33-113.15)*(R33-113.15)
        return(ike)

    def ike25(R18,R26):
        ike=-23.3 + 0.05*R18 + 0.245*R26
        return(ike)

    def ikeHU(Vmax,Rmax,R18,R33):
        ike= -25.2 + 0.238*Vmax + 0.023*(Vmax-55.86)*(Vmax-55.86) + 0.235*R33 - 5.5*1.0e-4*(R33-113.15)*(R33-113.15) + 0.025*R18
        return(ike)

    def ikeLinear(Vmax,V18,R18):
        Vmax=Vmax*knots2ms
        V18=V18*knots2ms
        R18=R18*nm2km
        ike=0.25*(Vmax*Vmax + 2.0*Vmax*V18 + 3.0*V18)*R18*R18
        ike=ike*1.0e-6
        return(ike)

    def areaIntersectCircles(R1,R2,d,dtot=0.0001):

        if(d == 0.0): d=dtot
        a1f=(d*d + R1*R1 - R2*R2)/2.0
        A1=R1*R1 * acos((d*d + R1*R1 - R2*R2)/(2.0*d*R1))
        A2=R2*R2 * acos((d*d + R2*R2 - R1*R1)/(2.0*d*R2))

        A1tot=R1*R1 * acos((dtot*dtot + R1*R1 - R2*R2)/(2.0*dtot*R1))
        A2tot=R2*R2 * acos((dtot*dtot + R2*R2 - R1*R1)/(2.0*dtot*R2))

        f1=(R1+R2-d)
        f2=(d+R1-R2)
        f3=(d-R1+R2)
        f4=(d+R1+R2)
        fact1=f1*f2*f3*f4
        adiff=0.5*sqrt( fact1 )
    #    print 'A1',A1,' A2: ',A2,' adiff: ',adiff,' A1tot: ',A1tot,' A2tot:',A2tot
        A=A1+A2-adiff

        Af1=1.0-(A*0.5/A1tot)
        Af2=1.0-(A*0.5/A2tot)
        if(Af1 < dtot): Af1=0.0
        if(Af2 < dtot): Af2=0.0
        return(A,Af1,Af2)

    def getB(R,A):

        def f(b,R,A):
            ff=1.0-pow(R,b)-b*A
            return(ff)

        b=ridder(f,0.1,1.1,args=(R,A))
        return(b)

    def vR(r,Vmax,Rmax,b):
        V=(Vmax*(r/Rmax)*exp((1.0/b)*(1.0-pow((r/Rmax),b))))
        return(V)

    def vRL(r,Vmax,R34,V34):
        V=Vmax-(Vmax-V34)*(r/R34)
        return(V)

    def integrand(r,Vmax,Rmax,b):
        vv=vR(r, Vmax, Rmax, b)
        V=vv*vv*r
        return(V)

    def integrandL(r,Vmax,R34,V34):
        vv=vRL(r, Vmax, R34,V34)
        V=vv*vv*r
        return(V)

    def rmaxFromVmax(Vmax):
        rmax=49.67-0.24*Vmax
        return(rmax)

    def r34FromVmax(Vmax):
        """Quiring et al. 2011
"""
        r34=47.19+0.89*Vmax
        return(r34)


    def ikeProfile(Vmax,Rmax,R34,V34,M=pi,verb=0):

        iVmax=Vmax*knots2ms
        iRmax=Rmax*nm2km
        iR34=R34*nm2km
        iV34=V34*knots2ms

        if(verb): print 'NNNNN %3.0f %3.0f %3.0f %3.0f  '%(Vmax,Rmax,V34,R34),'MMMM: %3.0f %3.0f %3.0f %3.0f'%(iVmax,iRmax,iV34,iR34)
        R=iR34/iRmax
        A=log((iV34/iVmax)*(iRmax/iR34))
        try:
            b=getB(R,A)
            doLinear=0
        except:
            doLinear=1

        if(verb):
            for r in arange(0.0,iR34,10.0):
                if(doLinear):
                    VL=vRL(r, iVmax, iR34,iV34)
                    V=VL
                else:
                    VL=vRL(r, iVmax, iR34,iV34)
                    V=vR(r, iVmax, iRmax, b)
                print 'VVV %d %3.0f'%(doLinear,r),'  V: %3.0f VL: %3.0f'%(V,VL)


        if(doLinear):
            IL=quad(integrandL,0.0,iR34,args=(iVmax,iR34,iV34))
            I=IL
        else:
            IL=quad(integrandL,0.0,iR34,args=(iVmax,iR34,iV34))
            I=quad(integrand,0.0,iR34,args=(iVmax,iRmax,b))

        IKEL=M*IL[0]*1e-6
        IKE=M*I[0]*1e-6
        if(verb): print "iVmax: %3.0f iRmax: %3.0f  iR34: %3.0f IKE: %5.1f IKEL: %5.1f"%(iVmax,iRmax,iR34,IKE,IKEL)
        return(IKE)

    VmaxBT=VmaxBTin
    R34BT=R34BTin

    ikeBT=None
    if(VmaxBTin < 0.0):
        ikeBT=-999.
        return(ikeBT)

    # -- for TD and minimal TS
    #
    if(VmaxBTin < VmaxR34):
        vfact=VmaxBTin/VmaxR34
        vfact=vfact*0.5
        RmaxBT=rmaxFromVmax(VmaxR34)*vfact
        R34BT=r34FromVmax(VmaxR34)*vfact
        ikeBT0=ikeLinear(VmaxBTin, VmaxR34, R34BT)
        #print 'qqqqqqq',R34BT,RmaxBT,ikeBT0

    elif(VmaxBTin >= VmaxR34 and R34BTin < 0.0):
        R34BT=r34FromVmax(VmaxBTin)

    RmaxBT=rmaxFromVmax(VmaxBT)

    IEin=IE
    if(IEin > IEmax): IEin=IEmax
    
    # -- 20190904 -- for case where there is only a track forecast, e.g., tvcn
    #    use a typical mean
    
    if(IEin < 0.0): IEin=IEmean

    if(RmaxBT > R34BT):
        RmaxBT=0.75*R34BT

    RmaxFC=RmaxBT

    # -- scale IE so that it goes to 0 at 2*R34BT
    #
    PEfrac=PE/(2.0*R34BT)
    if(PEfrac> 1.0): PEfrac=1.0

    IEscale=1.0-PEfrac*PEfrac

    #print 'III %4.0f %4.0f IE %3.1f %5.2f %3.1f'%(PE,2.0*R34BT,abs(IEin),IEscale,abs(IEin)*IEscale)

    VmaxFC0=VmaxBT
    VmaxFC=VmaxBT+abs(IEin)*IEscale

    R34FC=R34BT

    # -- find BT ike
    #
    if(ikeBT == None):

        #print
        #print 'VVV Vm %3.0f Rm: %3.0f  R34: %3.0f'%(VmaxBT,RmaxBT,R34BT)

        ikeBT=ikeProfile(VmaxBT,RmaxBT,R34BT,34.0,verb=verb)
        ikeFC=ikeProfile(VmaxFC,RmaxFC,R34FC,34.0,verb=verb)

    ikeFC0=ikeBT

    R1=R34BT
    R2=R34FC

    # -- constraints circle radii
    #
    if(R1 < R34Min): R1=R34Min
    if(R2 < R34Min): R2=R34Min

    d=PE
    if(d > R1+R2):
        Af1=Af2=1.0+(d/(R1+R2))
    else:
        (areaI,Af1,Af2)=areaIntersectCircles(R1,R2,d)

    FE=ikeBT*Af1+ikeFC*Af2
    FE0=ikeBT*Af1+ikeFC0*Af2

    return(ikeBT,ikeFC,R34BT,FE,FE0)
