#!/usr/bin/env python

from tcbase import *

MF.sTimer(tag='numpy')
import numpy
MF.dTimer(tag='numpy')

allmodels=['ecmb','ukmo','ncep','cmc']
allmodels06=['ncep','ukmo','ecmb']


def getBtcardsLatLonsFromBT2(BT,stmid,dtg,nhback=120,nhplus=168,verb=0):

    btcards=[]
    btcardsgt0=[]

    lats=[]
    lons=[]
    vmaxs=[]
    pmins=[]

    if(BT == None):
        nbt0=0
        btcardsgt0.append("N bt: %d"%(nbt0))
        print 'WWW--getBtcardsLatLonsFromBT2 BT == None'
        return(btcards,btcardsgt0,lats,lons,vmaxs,pmins)
        
    btrk=BT.btrk
    btdtgs=BT.dtgs
    
    btdtgs.sort()
        
    if(btdtgs == None):
        print 'WWW(getBtcardsLatLonsFromBT2): no bts for stmid: ',stmid
        return(btcards,btcardsgt0,lats,lons,vmaxs,pmins)


    btdtgs.sort()

    obtdtgs=[]
    obtdtgsgt0=[]
    for btdtg in btdtgs:
        dt=mf.dtgdiff(dtg,btdtg)
        if(dt <= 0 and dt >= -nhback):
            obtdtgs.append(btdtg)
        if(dt >= 0):
            obtdtgsgt0.append(btdtg)


    btcard="N bt: %d"%(len(obtdtgs))
    btcards.append(btcard)

    for dtg in obtdtgs:

        (blat,blon,bvmax,bpmin,bdir,bspd,flgtc,flgwn)=btrk[dtg]

        flgveri=VeriTcFlag(flgtc,flgwn)

        btcard="%s %6.1f %6.1f %3d %2d %6.0f"%(dtg,blat,blon,int(bvmax),flgveri,bpmin)
        btcards.append(btcard)
        lats.append(blat)
        lons.append(blon)
        vmaxs.append(bvmax)
        pmins.append(bpmin)

    btcardgt0="N bt: %d"%(len(obtdtgsgt0))
    btcardsgt0.append(btcardgt0)

    nbt0=0
    # -- 20130703 -- caused gfs2 to crash on plotting in lsdiag
    if(len(obtdtgsgt0) > 0):
        dtg0=obtdtgsgt0[0]

    for dtg in obtdtgsgt0:
        dt=mf.dtgdiff(dtg0,dtg)
        if(dt%12): continue
        dhplus=mf.dtgdiff(dtg0,dtg)
        if(dhplus > nhplus): continue

        nbt0=nbt0+1

        (blat,blon,bvmax,bpmin,bdir,bspd,flgtc,flgwn)=btrk[dtg]

        flgveri=VeriTcFlag(flgtc,flgwn)

        btcard="%s %6.1f %6.1f %3d %2d %6.0f"%(dtg,blat,blon,int(bvmax),flgveri,bpmin)
        btcardsgt0.append(btcard)
        lats.append(blat)
        lons.append(blon)
        vmaxs.append(bvmax)
        pmins.append(bpmin)

    # replace nbt with count from culling out tau12 increment

    btcardsgt0[0]="N bt: %d"%(nbt0)
    return(btcards,btcardsgt0,lats,lons,vmaxs,pmins)


def makeAdeckFileAD2s(ATs,model,aids,stmid,ostmid,dtg,taus,ddir,verb=0):

    rc=0
    adeckpath="%s/adeck.%s.%s.%s.txt"%(ddir,model,ostmid,dtg)
    if(verb): print 'adeckpath ',adeckpath

    adeck=[]
    for aid in aids:
        
        trk=ATs[aid]
        if(trk == None):
            cards=[]
        else:
            cards=MakeAdeckCards(aid,dtg,trk,ostmid,ttaus=taus,verb=verb)
            
        for card in cards:
            adeck.append(card[0:-1])
        

    if(len(adeck) > 0):
        MF.WriteList2Path(adeck,adeckpath,verb=0)
        rc=1
    else:
        rc=0

    return(rc)





def getEaids(model,nmembers,useNcep=0,verb=0):

    eaids=[]
    if(model == 'ecmb'):
        for n in range(1,nmembers+1):
            eaid='ee%02d'%(n)
            eaid='em%02d'%(n) # -- wmo bufr
            eaids.append(eaid)

    elif(model == 'ukmo'):
        for n in range(1,nmembers+1):
            eaid='uep%02d'%(n)
            eaids.append(eaid)

    elif(model == 'ncep'):

        # -- optionally use ncep...
        #
        if(useNcep):
            eaid='nac00'
            eaids.append(eaid)
            for n in range(1,nmembers):
                eaid='nap%02d'%(n)
                eaids.append(eaid)
        else:
            eaid='ac00'
            eaids.append(eaid)
            for n in range(1,nmembers):
                eaid='ap%02d'%(n)
                eaids.append(eaid)
                
            
    elif(model == 'cmc'):
        eaid='ncc00'
        eaids.append(eaid)
        for n in range(1,nmembers):
            eaid='ncp%02d'%(n)
            eaids.append(eaid)


    eaids.sort()

    return(eaids)

def getDetaid(model,verb=0):

    daid=None
    if(model == 'ecmb'):
        daid='ecmo'
        daid='emdt' # -- wmo bufr
        daid=['emdt','ecmf','tecm4']
        
    elif(model == 'ukmo'):
        daid='tukm2'
        daid=['tukm2','uedet','ukm','ukmi']

    elif(model == 'ncep'):
        daid=['tgfs2','avno','avni']

    elif(model == 'cmc'):
        daid=['tcmc2','ncmc']

    return(daid)



def getModelAD2s(dtg,stmid,taids,model,verb=0):

    (DSss,bd2s)=getAdeck2Bdeck2DSsByStmids(stmid,verb=verb)
    DSs=DSss[stmid]
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
        
def getAtsBt(dtg,stmid,model,nmembers,useNcep=0,verb=0):
    
    eaids=getEaids(model,nmembers,useNcep=useNcep,verb=verb)
    daid=getDetaid(model,verb=verb)
    
    if(daid != None):
        if(type(daid) == ListType):
            allaids=eaids+daid
        else:
            allaids=eaids+[daid]
    else:
        allaids=eaids

    # -- use the [A-Z]X to get the ATs and BT
    #
    (ATEs,BTE,nEadecks)=getModelAD2s(dtg, stmid, eaids, model,verb=verb)
    (ATs,BT,nadecks)=getModelAD2s(dtg, stmid, allaids, model,verb=verb)
    
    # -- check if we got Eadecks...require at least 50%
    #
    gotEaids=(nEadecks >= nmembers/2)
    
    return(eaids,daid,allaids,ATs,BT,nadecks,gotEaids)
    


def RegionalGrid(blat,elat,dlat,blon,elon,dlon,undef,taus,nmembers=None):

    
    InitialValue=0.0

    latsiz=elat-blat
    lonsiz=elon-blon
    
    grid={}
    ni=int(lonsiz/dlon)+1
    nj=int(latsiz/dlat)+1
    nij=ni*nj

    
    Initial=0.0

    if(taus == None):
        if(nmembers != None):
            grid=numpy.zeros((nmembers,nij))
        else:
            grid=numpy.zeros((nij))

        return(ni,nj,nij,grid)

        
    nt=len(taus)
    for tau in taus:
        
        if(nmembers != None):
            grid=numpy.zeros((nmembers,nij,nt))

        else:
            grid=numpy.zeros((nij,nt))
                    
            
    return(ni,nj,nij,grid)


def RegionalCtl(dset,cpath,dtg,ni,nj,blat,dlat,blon,dlon,undef,taus,var):

    nt=len(taus)
    dt=12
    gtime=mf.dtg2gtime(dtg)
    
    ctl="""dset ^%s
title test
undef %s
xdef %3d linear %5.1f  %5.1f
ydef %3d linear %5.1f  %5.1f
zdef   1 levels 1013
tdef %3d linear %s %dhr
vars 1
%s   0 0 # of ensembles per grid box and tau [nd] 
endvars"""%(dset,
            str(undef),
            ni,blon,dlon,
            nj,blat,dlat,
            nt,gtime,dt,
            var)

    #print ctl

    c=open(cpath,'w')
    c.writelines(ctl)
    c.close()

    return
                          


def GlobalGrid(dlon,dlat,undef,taus):

    grid={}
    ni=int(360.0/dlon)
    nj=int(180.0/dlat)+1
    nij=ni*nj

    InitialGrid=0.0

    for tau in taus:
        for i in range(0,ni):
            for j in range(0,nj):
                ii=j*ni + i
                grid[ii,tau]=InitialGrid
    
            
    return(ni,nj,nij,grid)



def ij2ii(i,j,ni,nj):
    ii=j*ni + i
    return(ii)
    

def ii2ij(ii,ni,nj):
    j=ii/ni
    i=ii-j*ni
    return(i,j)
    

def ll2ii(lon,lat,dlon,dlat,lon0,lat0,ni,nj,wrapx=0):

    nij=ni*nj
    i=(lon - lon0)/dlon
    j=(lat - lat0)/dlat

    if(wrapx):
        if(i<=0):  i=ni+i
        if(i>=ni): i=i-ni

    i=int(i+0.5)
    j=int(j+0.5)

    ii=j*ni + i
    
    if(ii >= nij):
        print 'WWW-!!!!!-ll2ii ii>nij !!!!!'
        print 'WWW-!!!!!- w2-tc-g-epsanal-dss-ad2.py-ll2ii ii>nij: ',lat0,lat,dlat,' lon: ',lon0,lon,dlon
        print 'WWW-!!!!!-ll2ii ii>nij !!!!! '
        ii=nij-1

    return(ii)


def ll2ij(lon,lat,dlon,dlat,lon0,lat0,ni,nj,wrapx=0):

    i=(lon - lon0)/dlon
    j=(lat - lat0)/dlat

    if(wrapx):
        if(i<=0):  i=ni+i
        if(i>=ni): i=i-ni

    ii=int(i+0.5)
    jj=int(j+0.5)

    return(i,j,ii,jj)


def ij2ll(i,j,dlon,dlat,lon0,lat0,ni,nj):

    lon=i*dlon+lon0
    lat=j*dlat+lat0

    return(lat,lon)



            

def GetLatLons(ad,dtg,stmid,taus,eaids,verb=0):

    lats=[]
    lons=[]

    astm2id=AD.GetStm2idFromAdeck(ad,stmid)
    
    nposits=0
    for eaid in eaids:
        for tau in taus:
            try:
                (lat,lon,pmin,vmax,r34,r50,r64)=ad.aidtrks[eaid,astm2id][dtg][tau]
                lats.append(lat)
                lons.append(lon)
                nposits=nposits+1
            except:
                if(verb): print 'NNNN111 no tracks for ',eaid,astm2id,dtg,tau

    return(nposits,lats,lons)






def ChkLatLonBounds(lat,lon,blat,blon,elat,elon):
    rc=1
    if(lat < blat or lat >= elat or lon < blon or lon >= elon):
        rc=0
    return(rc)


def ChkTrkData(jtrks,eaids,tau):
    rc=0
    for eaid in eaids:
        try:
            (lat,lon,vmax,pmin)=jtrks[eaid][tau][0:4]
            gotit=1
        except:
            gotit=0

        if(gotit):
            rc=1
            return(rc)
        
    return(rc)



def AnalyzeMembers2Grid(ATs,model,dtg,stmid,eaids,daid,tdir,
                        taus,
                        dlatHit,dlonHit,
                        dlatSkp,dlonSkp,
                        undef,nmembers,
                        critdist=160.0,
                        dtinterp=3,
                        override=0,
                        taumaxBack=120,
                        taumaxForward=168,
                        veribt=0,
                        verb=0):


    doanal=1

    dsetbase="tceps.grid.%s.%s.%s"%(stmid,dtg,model)
    
    dsetHit="%s.hit.dat"%(dsetbase)
    dsetSkp="%s.skp.dat"%(dsetbase)

    dpathHit="%s/%s"%(tdir,dsetHit)
    dpathSkp="%s/%s"%(tdir,dsetSkp)

    cpathHit="%s/%s.hit.ctl"%(tdir,dsetbase)
    cpathSkp="%s/%s.skp.ctl"%(tdir,dsetbase)

    trkepath="%s/tctrk.ensemble.%s.%s.%s.txt"%(tdir,stmid,dtg,model)
    trkdpath="%s/tctrk.det.%s.%s.%s.txt"%(tdir,stmid,dtg,model)

    btpath="%s/bt.%s.%s.%s.txt"%(tdir,stmid,dtg,model)
    btpathgt0="%s/bt.gt0.%s.%s.%s.txt"%(tdir,stmid,dtg,model)


    print 'TTT trkepath: ',trkepath
    print 'TTT trkdpath: ',trkdpath


    if(override2 and os.path.exists(dpathHit) and os.path.exists(dpathSkp)):
        return(1)


    # -- output the trackers for w2-tc-g-epsanal.gs -- deterministic
    #
    
    TE=open(trkepath,'w')
    TD=open(trkdpath,'w')

    dcard=''
    
    if(daid != None and ATs[daid] != None):

        print 'DDDeterministic got daid: ',daid,' DDDDDDDDDDDDDD'
    
        trk=ATs[daid]
        for tau in taus:
            try:
                rc=trk[tau]
                if(len(rc) >= 4):
                    lat=rc[0]
                    lon=rc[1]
                dcard="%s %5.1f %6.1f"%(dcard,lat,lon)
            except:
                if(verb == 0): print 'NNNNN-daids --dict no posit deterministic aid: ',daid,stmid,dtg,tau

                    
    if(len(dcard) > 0):
        dcard=dcard+'\n'
    else:
        dcard='99.9 999.9\n'

    TD.writelines(dcard)
    TD.close()

    # -- output the trackers for w2-tc-g-epsanal.gs -- ensemble mean track + member tracks
    #

    emtrk={}
    emcard=''
    
    for tau in taus:

        lats=[]
        lons=[]
        pmins=[]
        vmaxs=[]
        
        for eaid in eaids:

            if(ATs[eaid] != None):
                
                trk=ATs[eaid]
                try:
                    rc=trk[tau]
                    if(len(rc) >= 4):
                        lat=rc[0]
                        lon=rc[1]
                        vmax=rc[2]
                        pmin=rc[3]
                    else:
                        print 'AnalyzeMember2Grid: bad trk dict'
                        sys.exit()
                        
                    if(pmin == None): pmin=-999.
                    lats.append(lat)
                    lons.append(lon)
                    pmins.append(pmin)
                    vmaxs.append(vmax)
                except:
                    if(verb): print 'NNNN-emean no AD2.tracks for ',eaid,stmid,dtg,tau
                    
            else:
                if(verb): print 'NNNN-emean no AD2.tracks AT ALL for ',eaid,stmid,dtg

        mlat=0.0
        mlon=0.0
        mpmin=0.0
        mvmax=0.0
        nll=0
        nllPcntMin=40.0

        nllmin=(nllPcntMin/100.0)*float(nmembers)
        nllmin=int(nllmin+0.5)

        for n in range(0,len(lats)):
            mlat=mlat+lats[n]
            mlon=mlon+lons[n]
            mpmin=mpmin+pmins[n]
            mvmax=mvmax+vmaxs[n]
            nll=nll+1

        if(nll > nllmin):
            mlat=mlat/float(nll)
            mlon=mlon/float(nll)
            mpmin=mpmin/float(nll)
            mvmax=mvmax/float(nll)
            emcard="%s %5.1f %6.1f"%(emcard,mlat,mlon)

        emtrk[tau]=(mlat,mlon,mvmax,mpmin)


    if(len(emcard) > 0):
        emcard=emcard+'\n'
    else:
        emcard='99.9 999.9\n'
        
    TE.writelines(emcard)

    for eaid in eaids:
        ecard=''
        for tau in taus:
            
            if(ATs[eaid] != None):

                trk=ATs[eaid]
                try:
                    rc=trk[tau]
                    if(len(rc) >= 4):
                        lat=rc[0]
                        lon=rc[1]
                        vmax=rc[2]
                        pmin=rc[3]
                    else:
                        print 'AnalyzeMember2Grid: bad trk dict'
                        sys.exit()
                        
                    lats.append(lat)
                    lons.append(lon)
                    ecard="%s %5.1f %6.1f"%(ecard,lat,lon)
                except:
                    if(verb): print 'NNNN-eaids no AD2.tracks for ',eaid,stmid,dtg,tau

            else:
                if(verb): print 'NNNN-eaids no at all for AD2.tracks for ',eaid,stmid,dtg


        if(len(emcard) > 0):
            ecard=ecard+'\n'
        else:
            ecard='99.9 999.9\n'

        TE.writelines(ecard)

    TE.close()

    # -- bts
    #

    (btcards,btcardsgt0,btlats,btlons,btvmaxs,btpmins)=getBtcardsLatLonsFromBT2(BT,stmid,dtg,
                                                                                nhback=taumaxBack,
                                                                                nhplus=taumaxForward,
                                                                                verb=verb)
    if(len(btcards) == 0):
        return(0)

    nbtposits=int(btcards[0].split()[2])
    #
    # check for no bt old 9X storms -- use what's in btops.dtg.txt
    #

    if(nbtposits == 0):
        tcs=findtcs(dtg,srcopt='mdeck')
        for tc in tcs:
            istmid=tc.split()[1]
            if(istmid == stmid):
                tt=tc.split()
                btdtg=tt[0]
                btvmax=tt[2]
                btpmin=tt[3]
                btlat=tt[4]
                btlon=tt[5]
                btvflg=0
                btcard="%s %s %s %s %d %s"%(btdtg,btlat,btlon,btvmax,btvflg,btpmin)
                btcards[0]="N bt: 1"
                btcards.append(btcard)

    MF.WriteList2Path(btcards,btpath)
    MF.WriteList2Path(btcardsgt0,btpathgt0)

    print 'DDD     hit: ',dpathHit
    print 'DDD     skp: ',dpathSkp
    print 'CCC     hit: ',cpathHit
    print 'CCC     skp: ',cpathSkp
    print 'TTT    trke: ',trkepath
    print 'TTT    trkd: ',trkdpath
    print 'TTT      bt: ',btpath
    print 'TTT     btG: ',btpathgt0


    (alats,alons,refaid,reftau,reftrk)=GetOpsRefTrk(dtg,stmid,override=overridereftrk,
                                                        verb=overridereftrk)

    #wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww
    #
    # bail if no bt or ops posits, at all

    if(len(alats)  == 0):
        print 'WWWWWWWW no bt or ops posits for ',stmid,dtg
        return(0)

    #bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb
    #
    # lat/lon bounds of grid (and plot)

    (blat,elat,blon,elon)=LatLonOpsPlotBounds(alats,alons,verb=verb)
    
    if(stmid == '14L.2016'):
        blat=5.0
        elat=40.0
        blon=360.0-95.0
        elon=360.0-40.0
        
    print 'LLLLLLLLLLLLLLLLL stmid: ',stmid,blat,elat,blon,elon
    
    #if(model == 'ncep'): return(0)

    #tttttttttttttttttttttttttttttttttttttttttttttttttt
    #
    # trks both input/original (itrk) and interpolated (jtrk)
    
    ADu=ADutils()
    itrks={}
    jtrks={}
    jtrkDeftaus={}

    for eaid in eaids:
        try:
            itrks[eaid]=ATs[eaid]
            gotit=1
        except:
            gotit=0
            if(verb): print 'NNN-objtype no tracks for eaid: ',eaid,astm2id,dtg
        if(itrks[eaid] == None): gotit=0
        if(gotit):
            (jtrks[eaid],jtrkDeftaus[eaid])=ADu.FcTrackInterpFill(itrks[eaid],dtx=dtinterp,npass=0,verb=verb)


    if(override2 or veribt): doanal=0

    if(doanal):

        MF.sTimer('doanal-%s'%(dtg))
        #hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh
        #
        # hit - grids

        (nihit,njhit,nijhit,grid)=RegionalGrid(blat,elat,dlatHit,blon,elon,dlonHit,undef,taus)
        RegionalCtl(dsetHit,cpathHit,dtg,nihit,njhit,blat,dlatHit,blon,dlonHit,undef,taus,var='n')

        ntau={}
        for tau in taus:
            ntau[tau]=0.0

        #hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh
        #
        # hit - analysis
        MF.sTimer('hit-analysis-%s'%(dtg))
        for l in range(0,len(taus)):

            tau=taus[l]

            for n in range(0,len(eaids)):
                eaid=eaids[n]

                try:
                    rc=jtrks[eaid][tau]
                    (lat,lon,vmax,pmin)=rc[0:4]
                    gotit=1
                except:
                    gotit=0
                    if(verb): print 'NNN no jjjjjjjjtracks for eaid: ',eaid,' stmid/dtg/tau: ',stmid,dtg,tau

                if(gotit and ChkLatLonBounds(lat,lon,blat,blon,elat,elon) == 0):
                    gotit=0

                if(gotit):
                    itau=int(tau)
                    ii=ll2ii(lon,lat,dlonHit,dlatHit,blon,blat,nihit,njhit)
                    (i,j)=ii2ij(ii,nihit,njhit)
                    if(verb): print 'AAAA0000 ',eaid,tau,blat,' aidlat',lat,elat,blon,' aidlon',lon,elon,' ni/njhit: ',nihit,njhit,ii,nihit*njhit
                    grid[ii,l]=grid[ii,l]+1.0
                    ntau[tau]=ntau[tau]+1.0

                    
        MF.dTimer('hit-analysis-%s'%(dtg))

        #ssssssssssssssssssssssssssssssssssssssssssssssssss
        #
        # strike prob - grids

        otaus=range(0,taus[-1]+1,dtinterp)

        (niskp,njskp,nijskp,grid2)=RegionalGrid(blat,elat,dlatSkp,blon,elon,dlonSkp,undef,otaus,nmembers)
        (niskp,njskp,nijskp,gridsp)=RegionalGrid(blat,elat,dlatSkp,blon,elon,dlonSkp,undef,otaus)
        (niskp,njskp,nijskp,grid1n)=RegionalGrid(blat,elat,dlatSkp,blon,elon,dlonSkp,undef,None,nmembers)
        RegionalCtl(dsetSkp,cpathSkp,dtg,niskp,njskp,blat,dlatSkp,blon,dlonSkp,undef,taus,var='sp')


        #ssssssssssssssssssssssssssssssssssssssssssssssssss
        #
        # strike prob - analysis

        MF.sTimer(tag='skp-analysis-%s'%(dtg))
        
        distCrit=critdist*km2nm

        for l in range(0,len(otaus)):

            tau=otaus[l]

            if(not(ChkTrkData(jtrks,eaids,tau))): continue

            for n in range(0,nmembers):

                try:
                    eaid=eaids[n]
                except:
                    continue

                try:
                    (lat,lon,vmax,pmin)=jtrks[eaid][tau][0:4]
                    gotit=1
                except:
                    gotit=0
                    if(verb): print 'NNN no tracks for eaid: ',eaid,'stmid/dtg/tau: ',stmid,dtg,tau

                if(gotit and ChkLatLonBounds(lat,lon,blat,blon,elat,elon) == 0):
                    gotit=0

                if(gotit):

                    (i,j,i1,j1)=ll2ij(lon,lat,dlonSkp,dlatSkp,blon,blat,niskp,njskp)
                    if(verb): print 'AAAA ',eaid,tau,lat,lon,ii,i,j,i1,j1

                    for i2 in range(i1-2,i1+3):
                        for j2 in range(j1-2,j1+3):

                            (tlat,tlon)=ij2ll(i2,j2,dlonSkp,dlatSkp,blon,blat,niskp,njskp)

                            dist=gc_dist(lat,lon,tlat,tlon)
                            if(dist <= distCrit and ChkLatLonBounds(tlat,tlon,blat,blon,elat,elon) ):
                                ii2=ij2ii(i2,j2,niskp,njskp)
                                grid2[n,ii2,l]=1.0


            #
            #  integrate in tau -- set a mask grid1n if the N member cyclone strikes the grid point
            #
            for n in range(0,nmembers):
                for j in range(0,njskp):
                    for i in range(0,niskp):
                        ii=ij2ii(i,j,niskp,njskp)
                        if(grid2[n,ii,l] == 1.0 and grid1n[n,ii] == 0.0):
                            grid1n[n,ii]=1.0

            for n in range(0,nmembers):
                for j in range(0,njskp):
                    for i in range(0,niskp):
                        ii=ij2ii(i,j,niskp,njskp)
                        gridsp[ii,l]=gridsp[ii,l]+grid1n[n,ii]


            for j in range(0,njskp):
                for i in range(0,niskp):
                    ii=ij2ii(i,j,niskp,njskp)
                    gridsp[ii,l]=(gridsp[ii,l]/(nmembers))*100.0

                    
        MF.dTimer(tag='skp-analysis-%s'%(dtg))

        import array

        gh=array.array('f')
        gs=array.array('f')

        (dir,file)=os.path.split(cpathHit)
        (base,ext)=os.path.splitext(file)

        DH=open(dpathHit,'wb')
        DS=open(dpathSkp,'wb')

        for tau in taus:

            l=taus.index(tau)
            lo=otaus.index(tau)

            ngridhit=[]
            ngridsp=[]

            for j in range(0,njhit):
                for i in range(0,nihit):

                    ii=ij2ii(i,j,nihit,njhit)

                    valhit=grid[ii,l]
                    ngridhit.append(valhit)


            for j in range(0,njskp):
                for i in range(0,niskp):

                    ii=ij2ii(i,j,niskp,njskp)

                    valsp=gridsp[ii,lo]
                    if(valsp > 100.0):  print 'valsp ',valsp,tau
                    ngridsp.append(valsp)

            gh.fromlist(ngridhit)
            gs.fromlist(ngridsp)

        gs.tofile(DS)
        DS.close()

        gh.tofile(DH)
        DH.close()

        MF.dTimer('doanal-%s'%(dtg))
        

    return(1)



def MakeAnimatedGif(pdir,stmid,model,taus,ptype,convertexe,
                    delayfactorloop,delayfactorlarge,delayfactorend,
                    veribt):

    if(veribt):
        tgiffile="esrl.eps.veri.%s.%s.loop.%s.%s.gif"%(model,ptype,stmid,dtg)
    else:
        tgiffile="esrl.eps.%s.%s.loop.%s.%s.gif"%(model,ptype,stmid,dtg)
    tgifpath="%s/%s"%(pdir,tgiffile)
    
    #
    #  animated gif
    # 
    np=0
    tauend=taus[-1]
    ccmd=''
    for tau in taus:
        otau="%03d"%(tau)
        if(veribt):
            ppath="%s/esrl.eps.veri.%s.%s.%s.%s.png"%(pdir,model,ptype,stmid,otau)
        else:
            ppath="%s/esrl.eps.%s.%s.%s.%s.png"%(pdir,model,ptype,stmid,otau)
            
        if(not(os.path.exists(ppath))): continue
        if(np == 0):
            ccmd="%s -loop 0 -delay %s %s"%(convertexe,delayfactorloop,ppath)
        elif(tau == 24 or tau == 48 or tau == 72):
            ccmd="%s -delay %s %s"%(ccmd,delayfactorlarge,ppath)
        elif(tau == tauend):
            ccmd="%s -delay %s %s"%(ccmd,delayfactorend,ppath)
        else:
            ccmd="%s -delay %s %s"%(ccmd,delayfactorloop,ppath)
        np=np+1
        
    if(ccmd != ''):
        ccmd="%s %s"%(ccmd,tgifpath)
        mf.runcmd(ccmd)





def GetPlotPaths(pdir,stmid,model,taus,ptypes,doclean=0):

    nplots=0
    plots={}

    for ptype in ptypes:

        pngmask="%s/esrl.eps.%s.%s.%s.*.png"%(pdir,model,ptype,stmid)
        pngs=glob.glob(pngmask)
        pngs.sort()
        if(doclean):
            for png in pngs:
                print 'clean: ',png
                os.unlink(png)
            pngs=[]

        if(len(pngs) > 0):
            plots[ptype]=[]
            plots[ptype]=plots[ptype]+pngs
            nplots=nplots+len(pngs)


        gifmask="%s/esrl.eps.%s.%s.loop.%s.*.gif"%(pdir,model,ptype,stmid)
        gifs=glob.glob(gifmask)
        gifs.sort()

        if(doclean):
            for gif in gifs:
                print 'clean gif: ',gif
                os.unlink(gif)
            gifs=[]

        if(len(gifs) > 0 and len(pngs) > 0):
            plots[ptype]=plots[ptype]+gifs
            nplots=nplots+len(gifs)


    return(nplots,plots)

def findstmdtg(stmdtgs,tdtg):
    
    for stmdtg in stmdtgs:
        if(stmdtg == tdtg):
            return(1)
    return(0)

def ChkEaids(ad,eaids,stm2id,dtg):

    if(stm2id == None):
        return(0)
    
    rc=0
    for eaid in eaids:
        stms=ad.aidstms[eaid]
        for stm in stms:
            if(stm2id == stm):
                try:
                    nc=len(ad.aidcards[eaid,stm2id][dtg])
                except:
                    nc=0
                if(verb == 0): print 'ChkEaids dtg: ',dtg,' eaid: ',eaid,'stm2id: ',stm2id,' ncards: ',nc
                if(nc > 0):
                    rc=1
                    break

    return(rc)
    

        
def ChkDaid(ad,daid,stm2id):

    if(stm2id == None):
        return(0)
    
    rc=0
    for aid in ad.aids:
        if(aid == daid):
            stms=ad.aidstms[daid]
            for stm in stms:
                if(stm2id == stm):
                    rc=1
                    break

    return(rc)
    

        
        
            


#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
# main
#
class MdeckCmdLine(CmdLine):

    otags=getMd2DSsTags()
    
    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv

        self.argv=argv

        self.argopts={
            1:['dtgopt',    'no default'],
            2:['model',    'no default'],
            }

        self.defaults={
            }

        self.options={
            'ropt':            ['N','','norun',' norun is norun'],
            'verb':            ['V',0,1,'verb=1 is verbose'],
            'veribt':          ['v',0,1,'verify using the bt'],
            'override':        ['O',0,1,'override'],
            'override2':       ['o',0,1,'override2'],
            'doinventory':     ['I',0,1,'do inventory'],
            'doxml':           ['X',0,1,"""set the ncepsource to 'xml'"""],
            'overridereftrk':  ['R',0,1,'redo the reftrk file'],
            'adeckonly':       ['A',0,1,"""set ncepSource to 'adeckonly'"""],
            'doretro':         ['r',0,1,"""doretro"""],
            'doadeckonly':     ['D',0,1,"""only do adecks"""],
            'stmopt':          ['S:',None,'a','stmopt'],
            }

        self.purpose='''
make eps graphics
models:  %s'''%(str(allmodels))
        
        self.examples='''
%s cur12 ncep -A'''


    
#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# -- main
#

MF.sTimer('all')

argv=sys.argv
CL=MdeckCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr


dtgs=mf.dtg_dtgopt_prc(dtgopt)

if(len(model.split(',')) > 1):
    models=model.split(',')
else:
    models=[model]

if(len(dtgs) > 1 or len(models) > 1):
    #
    # cycle by dtgs
    #
    for dtg in dtgs:
        for model in models:
            cmd="%s %s %s"%(pyfile,dtg,model)
            for o,a in CL.opts:
                cmd="%s %s %s"%(cmd,o,a)
            mf.runcmd(cmd,ropt)

    sys.exit()

else:
    dtg=dtgs[0]


#ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss
#
# setup

xsize=1200
xgrads='grads'  # 'set grid on 3 15 5' works in my version 1.10
xgrads=setXgrads(useX11=0)  # make good graphics
if(mf.find(W2Host,'clim')): xgrads='grads2p1'

prcdir=w2.PrcDirTcdatW2
mf.ChangeDir(prcdir)

year=dtg[0:4]

#----------------------------------------------
# model/ dir setup
#


if(model == 'all'):
    
    for model in allmodels:
        cmd="%s %s %s"%(pyfile,dtgopt,model)
        for o,a in CL.opts:
            cmd="%s %s %s"%(cmd,o,a)
        mf.runcmd(cmd,ropt)

    sys.exit()

elif(not(model in allmodels)):
    print 'EEE invalid model: ',model,' valid models: ',allmodels
    sys.exit()


#------------------------------------------------------------
# check if model available...
#

hh=dtg[8:10]

if(hh == '06' or hh == '18'):
    doit=0
    for tmodel in allmodels06:
        if(tmodel == model): doit=1

    if(not(doit)):
        print 'WWWWWWWWWWWWWWWWWWWWWW model: ',model,' is not available at off times...'
        sys.exit()


#ddddddddddddddddddddddddddddddd
# dir setup
#

if(model == 'ecmb'):
    tbdir=w2.TcTcepsEcmwfDir
    nmembers=w2.TcTcepsEcmwfNmembers
    
elif(model == 'ukmo'):
    tbdir=w2.TcTcepsuKmoDir
    nmembers=w2.TcTcepsuKmoNmembers

elif(model == 'ncep'):
    tbdir=w2.TcTcepsNcepDir
    nmembers=w2.TcTcepsNcepNmembers
    
elif(model == 'cmc'):
    tbdir=w2.TcTcepsCmcDir
    nmembers=w2.TcTcepsCmcNmembers
    
else:
    print 'invalid model to set tbdir: ',model
    sys.exit()


twdir=w2.TcTcepsWebDir

ddir="%s/%s/%s/dat"%(tbdir,year,dtg)
mf.ChkDir(ddir,'mk')
pdir="%s/%s/%s/plt"%(tbdir,year,dtg)
mf.ChkDir(pdir,'mk')
wdir="%s/%s/%s"%(twdir,year,dtg)
mf.ChkDir(wdir,'mk')

# -- 20120825 -- add log dir
logdir="%s/%s/%s/log"%(tbdir,year,dtg)
mf.ChkDir(logdir,'mk')



#ttttttttttttttttttttttttttttttttt
# taus to plot
#

taus=[0,12,24,36,48,60,72,84,96,108,120]
taus=[0,12,24,36,48,60,72,84,96,108,120,132,144,156,168]
dtau=12
ntaumax=(taus[-1]/dtau) + 1

#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
# analysis parameters
#

dLatLonEPSAnalysisHit=1.0
dlonHit=dlatHit=dLatLonEPSAnalysisHit

dLatLonEPSAnalysisSkp=0.5
dlonSkp=dlatSkp=dLatLonEPSAnalysisSkp

critdist=120.0 # in km
undef=1e20

#gggggggggggggggggggggggggggggggggg
# animated gif
#

convertexe='convert'
convertexe='convert.ksh'
delayfactorlarge=150
delayfactorloop=50
delayfactorend=500

ptypes=['hit','skp']


#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
# main processing section
#

(stmids,tD,tstmids9Xall)=getTstmidsAD2FromStmoptDtgopt(stmopt,dtgopt)

# 20120825 -- log
#
logs=glob.glob("%s/log.%s.%s.*.txt"%(logdir,model,dtg))
logs.sort()

nplotsDONE=-999
ndaidDONE=-999
neaidsDONE=-999

if(len(logs) > 0):
    tt=logs[-1].split('.')
    nplotsDONE=tt[-3]
    ndaidDONE=tt[-4]
    neaidsDONE=tt[-5]

print 'WWWorking   DTG: ',dtg
print 'NNN       model: ',model
print 'NNN  nplotsDONE: ',nplotsDONE
print 'NNN   ndaidDONE: ',ndaidDONE
print 'NNN  neaidsDONE: ',neaidsDONE

nplots=0
didplots=0

for stmid in stmids:

    # -- convert [A-Z]X to 9X form for output
    #
    rc=getStmParams(stmid, convert9x=1)
    ostmid=rc[-1]
    
    MF.sTimer("doing ostmid: %s dtg: %s"%(ostmid,dtg))

    if(model == 'ncep'):
        
        (eaids,daid,allaids,ATs,BT,nadecks,gotEaids)=getAtsBt(dtg,stmid,model,nmembers,useNcep=0,verb=verb)
        print '0000000000 useNcep Model: %s  gotEaids: %d'%(model,gotEaids),' nadecks: ',nadecks

        # -- try ncep ad2s
        #
        if(not(gotEaids)):
            (eaids,daid,allaids,ATs,BT,nadecks,gotEaids)=getAtsBt(dtg,stmid,model,nmembers,useNcep=1,verb=verb)
            print '1111111111 useNcep Model: %s  gotEaids: %d'%(model,gotEaids),' nadecks: ',nadecks
        
    else:
        (eaids,daid,allaids,ATs,BT,nadecks,gotEaids)=getAtsBt(dtg,stmid,model,nmembers,useNcep=0,verb=verb)

    # -- find the det aid
    #
    gotdaid=0
    for dd in daid:
        if(dd in ATs.keys()):
            if(ATs[dd] != None):
                gotdaid=1
                daid=dd
                break
        
    if(not(gotdaid)): daid=None

    print '     DTG: ',dtg 
    print '   stmid: ',stmid
    print '  ostmid: ',ostmid
    print '   Eaids: ',eaids[0:2],'...',eaids[-2:]
    print ' gotEaids: ',gotEaids
    print '    Daid: ',daid
    print ' nadecks: ',nadecks

    if(nplotsDONE > 0 and ndaidDONE == 0 and daid != None):
        print 'III setting override2=1'
        override2=1
        
    docleanPlots=0
    if(override or override2):
        docleanPlots=1
    # -- check if plots made
    #
    (nplots,plots)=GetPlotPaths(pdir,ostmid,model,taus,ptypes,doclean=docleanPlots)
    (nplots,plots)=GetPlotPaths(wdir,ostmid,model,taus,ptypes,doclean=docleanPlots)
    
    doplots=1
    if(nplots > 0):
        doplots=0
        if(verb):
            ptypes=plots.keys()
            ptypes.sort()
            for ptype in ptypes:
                pps=plots[ptype]
                for pp in pps:
                    print 'ppp ',ptype,pp
                    
        if(not(veribt)):
            print 'WWWWWWW plots already done, override: %s, verbbt: %s for ostmid: %s'%(override,veribt,ostmid)
        
        # -- override2 -- just plot, no analysis
        #
        if(override2 or veribt):
            doplots=1
        elif(override == 0 and veribt == 0 and doadeckonly == 0):
            continue
        elif(doadeckonly):
            print 'III -- doadeckonly...continue'
        else:
            print 'IIII - no overrides so continue to next stmid...'
            continue

    if(veribt): doplots=1

    # -- make adeck file for display
    #
    rc=makeAdeckFileAD2s(ATs,model,allaids,stmid,ostmid,dtg,taus,pdir,verb=verb)
    
    if(rc == 0):
        print 'WWW no ATs for ostmid: ',ostmid,' dtg: ',dtg,' press...'
        continue

    cmd="cp %s/adeck.*.txt %s/."%(pdir,wdir)
    mf.runcmd(cmd,ropt)
    if(doadeckonly): continue
        
    # -- require one det and one eaid or 2 eaids
    #
    if( nadecks >= 2 and doplots or (override != 0 or override2) or veribt):

        if(override2):
            rc=1
        else:
            rc=AnalyzeMembers2Grid(ATs,model,dtg,ostmid,eaids,daid,ddir,
                                   taus,
                                   dlatHit,dlonHit,
                                   dlatSkp,dlonSkp,
                                   undef,nmembers,
                                   critdist,
                                   override=override,
                                   veribt=veribt,
                                   verb=verb)


        stmname=GetTCName(ostmid)
        stmname=stmname.upper()
        print 'SSS  ostmid: ',ostmid
        print 'SSS stmname: ',stmname
        
        if(rc):

            #
            # make tau pngs
            #
            curpid=os.getpid()
            gscrp='w2-tc-g-epsanal-dss-ad2.gs'
            gsopt="%s %s %s %s %s %s %5.0f %i %i %i %i %i %i"%(ostmid,stmname,dtg,model,ddir,pdir,critdist,nmembers,ntaumax,dtau,veribt,xsize,int(curpid))
            gacmd="%s -lbc \"%s %s\""%(xgrads,gscrp,gsopt)
            mf.runcmd(gacmd,ropt)

            #
            # make animated loop gifs
            #
            for ptype in ptypes:
                MakeAnimatedGif(pdir,ostmid,model,taus,ptype,convertexe,
                                delayfactorloop,delayfactorlarge,delayfactorend,
                                veribt)


            #
            # cp to web dir
            #
            if(veribt):
                cmd="cp %s/*esrl.eps.veri.*%s* %s/."%(pdir,model,wdir)
            else:
                cmd="cp %s/*esrl.eps.*%s* %s/."%(pdir,model,wdir)

            mf.runcmd(cmd,ropt)

            cmd="cp %s/db.* %s/."%(pdir,wdir)
            mf.runcmd(cmd,ropt)
            cmd="cp %s/db.* %s/."%(ddir,wdir)
            mf.runcmd(cmd,ropt)

            didplots=1

    MF.dTimer("doing ostmid: %s dtg: %s"%(ostmid,dtg))


# 20120825 -- log
#

if(len(stmids) == 0):
    print 'WWW(w2-tc-g-epsanal-dss-ad2.py) no storms from the AD2 adecks...sayoonara'
    sys.exit()
    
ndaid=0
neaids=len(eaids)
if(eaids != None): ndaid=1

curdtgms=mf.dtg('dtg_ms')
logpath="%s/log.%s.%s.%02d.%1d.%02d.%s.txt"%(logdir,model,dtg,neaids,ndaid,nplots,curdtgms)
cmd="touch %s"%(logpath)
mf.runcmd(cmd,ropt)
    
ndayback=mf.dtgdiff(curdtg,dtg)/24.0
ndayback=int(-ndayback+0.5)

doveri=0

if(didplots or override != 0 or doinventory):

    if(not(doretro) and not(veribt)):

        #
        # sleep for 5 secs, to allow cp above to catch up
        #
        rc=sleep(5)
        
        #
        # always inventory from current dtg
        #
        mf.ChangeDir(prcdir)
        cmd="w2-tc-inventory-epsanal.py %s "%(curdtg)
        mf.runcmd(cmd,ropt)
        
        if(ndayback < 6 and doveri):
            
            invdtg=dtg
            #
            #
            #
            cmd="%s cur-d5.cur %s -v"%(pyfile,model)
            mf.runcmd(cmd,ropt)

if(doadeckonly):
    cmd="w2-tc-inventory-epsanal.py %s -n 0"%(dtg)
    mf.runcmd(cmd,ropt)
    
        
if(doretro):

    if(doveri):
        cmd="%s %s %s -v"%(pyfile,dtg,model)
        mf.runcmd(cmd,ropt)

    ndayback=ndayback+5
    print 'rrrrrrrrrrr ndayback: ',ndayback
    
    mf.ChangeDir(prcdir)
    cmd="w2-tc-inventory-epsanal.py %s -r -n %d"%(curdtg,ndayback)
    mf.runcmd(cmd,ropt)

    sys.exit()
    


MF.dTimer('all')

sys.exit()

