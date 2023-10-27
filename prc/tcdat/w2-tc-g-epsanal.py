#!/usr/bin/env python

from tcbase import *


taumaxBack=120
taumaxForward=168

#llllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll
#
#  move ecmwf files to data dir
#


def chkModelAdecks(dtg,stmid,model,nmembers,verb=0,reqdet=1):

    adSource=None
    sbdir2=None
    mask2=None
    mask2p1=None
    detmaskp1=None
    (shemoverlap,cy,cyp1)=CurShemOverlap(dtg)

    mask=None
    detmask=None

    year=dtg[0:4]
    detmask=''
    stm3id=stmid.split('.')[0]
    if(mf.find(model,'ecm')):
        sbdir=w2.TcAdecksEcmwfDir
        sbdirdet=w2.TcAdecksEcmwfDir
        mask="a*.%s.%s.ecmwf_tigge.txt"%(dtg,stmid)
        detmask="wxmap/*%s.%s"%(dtg,stm3id)
        
    elif(model == 'ukmo'):
        sbdir=w2.TcAdecksuKmoDir
        mask="a*.%s.%s.ukmo_tigge.txt"%(dtg,stmid)
        
        # go after det from nhc/jtwc adecks
        #
        rc=getadeckdet(stmid,year,cyp1,ncepSource)
        (sbdirdet,sbdir2,mask2,mask2p1,detmask,detmask2,detmaskp1)=rc


    elif(model == 'ncep'):

        if(not(mf.find(ncepSource,'adeck'))):
            sbdir=w2.TcAdecksNcepDir
            mask="a*.%s.%s.ncep_tigge.txt"%(dtg,stmid)

            sbdir2=w2.TcAdecksNcepDir
            mask2="tracks.all.%s.txt"%(dtg)

        elif(ncepSource == 'adeckonly'):
            sbdir=w2.TcAdecksNhcDir
            stm2id=stm1idTostm2id(stmid).split('.')[0]
            mask="a%s%s.dat"%(stm2id,year)
            
            sbdir2=w2.TcAdecksJtwcNhcDir
            mask2="ncep_a%s%s.dat"%(stm2id,year)
            
        else:
            sbdir=w2.TcAdecksNhcDir
            stm2id=stm1idTostm2id(stmid).split('.')[0]
            mask="a%s%s.dat"%(stm2id,year)
            
            sbdir=w2.TcAdecksNcepDir
            mask="%s/a???.*.cyclone.*atcfunix"%(dtg)

            sbdir=w2.TcAdecksNcepDir
            mask="tracks.all.%s.txt"%(dtg)

        # go after det from nhc/jtwc adecks
        #
        rc=getadeckdet(stmid,year,cyp1,ncepSource='adeckonly')
        (sbdirdet,sbdir2,mask2,mask2p1,detmask,detmask2,detmaskp1)=rc
        
    elif(model == 'cmc'):

        if(not(mf.find(ncepSource,'adeck'))):
            sbdir=w2.TcAdecksCmcDir
            mask="a*.%s.%s.cmc_tigge.txt"%(dtg,stmid)
            detmask="a*.%s.%s.cmc_cmct_tigge.txt"%(dtg,stmid)

            sbdir2=w2.TcAdecksNcepDir
            mask2="tracks.all.%s.txt"%(dtg)
            
        elif(ncepSource == 'adeckonly'):
            sbdir=w2.TcAdecksNhcDir
            stm2id=stm1idTostm2id(stmid).split('.')[0]
            mask="a%s%s.dat"%(stm2id,year)
            
            sbdir2=w2.TcAdecksJtwcNhcDir
            mask2="ncep_a%s%s.dat"%(stm2id,year)
            mask2p1=None
            
            sbdir=w2.TcAdecksCmcDir
            sbdirdet=w2.TcAdecksCmcDir
            mask="%s/c???.*.cyclone.*atcfunix"%(dtg)
            detmask="%s/cmc.*.cyclone.*atcfunix"%(dtg)
            detmaskp1=None

        else:
            sbdir=w2.TcAdecksCmcDir
            sbdirdet=w2.TcAdecksCmcDir
            mask="%s/c???.*.cyclone.*atcfunix"%(dtg)
            detmask="%s/cmc.*.cyclone.*atcfunix"%(dtg)
            detmaskp1=None

            # -- ncep from master alltracks file
            sbdir=w2.TcAdecksNcepDir
            mask="tracks.all.%s.txt"%(dtg)

        print 'CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCccc ',ncepSource,'mask: ',mask

        # go after det from nhc/jtwc adecks
        #
        rc=getadeckdet(stmid,year,cyp1,ncepSource)
        (sbdirdet,sbdir2,mask2,mask2p1,detmask,detmask2,detmaskp1)=rc

        
    elif(model == 'esrl'):
        sbdir=w2.TcAdecksEsrlDir
        sbdirdet=w2.TcAdecksEsrlDir
        mask="tacc/*%s*"%(dtg)
        detmask="tacc/*%s*.F9EM"%(dtg)

    elif(model == 'gfsenkf'):
        
        sbdir=w2.TcAdecksEsrlDir
        sbdirdet=w2.TcAdecksEsrlDir

        mask="%s/%s/track.%s.GE??"%(model,dtg,dtg)
        detmask="%s/%s/track.%s.GE00"%(model,dtg,dtg)

    elif(model == 'fimens'):

        def fixFimensAidName(fimadeck,verb=0):

            newadeck=[]

            member=int(fimadeck[-2:])
            cards=open(fimadeck).readlines()
            oaid='FIM0'
            if(member <= 9):
                oaid='FIM0'
            elif(member >= 10):
                oaid='FIM1'
            
            naid='FE%02d'%(member)

            # -- don't do if already done
            if(not(mf.find(cards[0],oaid))):
                print 'III already updated: ',fimadeck,cards[0][0:50]
                return

            for ocard in cards:
                ncard=ocard.replace(oaid,naid)
                newadeck.append(ncard)

            MF.WriteList2File(newadeck,fimadeck)

            
        sbdir=w2.TcAdecksTmtrkNDir
        sbdirdet=w2.TcAdecksTmtrkNDir

        dmodel='f9hj'
        mask="%s/tctrk.atcf.%s.fe??.???.????"%(dtg,dtg)
        detmask="%s/tctrk.atcf.%s.%s.???.????"%(dtg,dtg,dmodel)

        #for fimadeck in fimadecks:
        #    fixFimensAidName(fimadeck)

        sbdirGEFS=w2.TcAdecksNcepDir
        maskGEFS="tracks.all.%s.txt"%(dtg)

    if(mask != None):
        adeckpathmask=("%s/%s/%s"%(sbdir,year,mask))
        adecks=glob.glob(adeckpathmask)
    
    adecksGEFS=glob.glob('%s/%s/%s'%(sbdirGEFS,year,maskGEFS))
    adecks=adecks+adecksGEFS

    if(detmask != None):
        detadeckpathmask=("%s/%s/%s"%(sbdir,year,detmask))
        detadecks=glob.glob(detadeckpathmask)

    rc=0
    print 'III #adecks: ',len(adecks),'nmembers: ',nmembers
    if(reqdet and (len(detadecks) == 1) and len(adecks) >= nmembers ): rc=1
    elif(len(adecks) >= nmembers): rc=1 

    rc=1
    return(rc)




def GetModelAdecks(dtg,stmid,model,verb=0):

    def getadeckdet(stmid,year,cyp1,ncepSource):
        
        # -- always go to the jt/nhc adecks for deterministic -- egrr
        # -- detmask2 is to allow for a secondary source of det trackers
        
        detmask2=None
        b1id=stmid[2]
        if(IsJtwcBasin(b1id)):
            sbdirdet=w2.TcAdecksJtwcDir
            stm2id=stm1idTostm2id(stmid).split('.')[0]
            sbdir2=w2.TcAdecksJtwcNhcDir
            mask2="ncep_a%s%s.dat"%(stm2id,year)
            mask2p1="ncep_a%s%s.dat"%(stm2id,cyp1)
            # -- look for standard adecks in jtwc adecks...
            mask2="a%s%s.dat"%(stm2id,year)
            mask2p1="a%s%s.dat"%(stm2id,cyp1)
        else:
            mask2=mask2p1=None
            sbdir2=None
            sbdirdet=w2.TcAdecksNhcDir
            stm2id=stm1idTostm2id(stmid).split('.')[0]

        if(ncepSource == 'adeckonly'):
            detmask=None
            detmaskp1=None
        else:
            detmask="a%s%s.dat"%(stm2id,year)
            detmaskp1="a%s%s.dat"%(stm2id,cyp1)

        if(model == 'ncep' or model == 'cmc'):
            
            if(IsJtwcBasin(b1id)):
                sbdir2=w2.TcAdecksJtwcDir
            else:
                sbdir2=w2.TcAdecksNhcDir

            sbdirdet=w2.TcAdecksNcepDir
            detmask="tracks.all.%s.txt"%(dtg)

            # -- use ncep adecks or nhc/jwtc for det...
            detmask2="a%s%s.dat"%(stm2id,year)
            
        elif(model == 'ukmo'):
            
            mask2=mask2p1=None

            sbdirdet="%s"%(w2.TcAdecksTmtrkNDir)
            detmask="%s/tctrk.atcf.%s.ukm2.%s"%(dtg,dtg,stmid)

            sbdir2=w2.TcAdecksuKmoDir
            detmask2="a*.%s.%s.ukmo_det_tigge.txt"%(dtg,stmid)
            
           
        

        return(sbdirdet,sbdir2,mask2,mask2p1,detmask,detmask2,detmaskp1)

        

    adSource=None
    sbdir2=None
    mask2=None
    mask2p1=None
    detmaskp1=None
    detmask2=None
    (shemoverlap,cy,cyp1)=CurShemOverlap(dtg)


    year=dtg[0:4]
    detmask=''
    stm3id=stmid.split('.')[0]

    if(model == 'ncep-ecmwf'):

        adSource='ncep'
        print 'AAAAAAAAAAAAAAAAAAA: adSource ',adSource
        
    elif(mf.find(model,'ecm')):
        sbdir=w2.TcAdecksEcmwfDir
        sbdirdet=w2.TcAdecksEcmwfDir
        mask="a*.%s.%s.ecmwf_tigge.txt"%(dtg,stmid)
        detmask="wxmap/*%s.%s"%(dtg,stm3id)
        
    elif(model == 'ukmo'):
        sbdir=w2.TcAdecksuKmoDir
        mask="a*.%s.%s.ukmo_tigge.txt"%(dtg,stmid)
        
        # go after det from nhc/jtwc adecks
        #
        rc=getadeckdet(stmid,year,cyp1,ncepSource)
        (sbdirdet,sbdir2,mask2,mask2p1,detmask,detmask2,detmaskp1)=rc


    elif(model == 'ncep'):

        if(ncepSource == 'tigge'):
            sbdir=w2.TcAdecksNcepDir
            mask="a*.%s.%s.ncep_tigge.txt"%(dtg,stmid)

        elif(ncepSource == 'adeckonly'):
            sbdir=w2.TcAdecksNhcDir
            stm2id=stm1idTostm2id(stmid).split('.')[0]
            mask="a%s%s.dat"%(stm2id,year)
            
            sbdir2=w2.TcAdecksJtwcNhcDir
            mask2="ncep_a%s%s.dat"%(stm2id,year)
            
        else:
            sbdir=w2.TcAdecksNhcDir
            stm2id=stm1idTostm2id(stmid).split('.')[0]
            mask="a%s%s.dat"%(stm2id,year)
            
            sbdir=w2.TcAdecksNcepDir
            mask="%s/a???.*.cyclone.*atcfunix"%(dtg)

            sbdir=w2.TcAdecksNcepDir
            mask="tracks.%s.txt"%(dtg)

        # go after det from nhc/jtwc adecks
        #
        rc=getadeckdet(stmid,year,cyp1,ncepSource)
        (sbdirdet,sbdir2,mask2,mask2p1,detmask,detmask2,detmaskp1)=rc
        
    elif(model == 'cmc'):

        if(ncepSource == 'tigge'):
            sbdir=w2.TcAdecksCmcDir
            sbdirdet=w2.TcAdecksCmcDir
            mask="a*.%s.%s.cmc_tigge.txt"%(dtg,stmid)
            detmask="a*.%s.%s.cmc_cmct_tigge.txt"%(dtg,stmid)
            detmaskp1=None

            sbdir2=w2.TcAdecksNcepDir
            mask2="tracks.all.%s.txt"%(dtg)

        elif(ncepSource == 'adeckonly'):
            sbdir=w2.TcAdecksNhcDir
            stm2id=stm1idTostm2id(stmid).split('.')[0]
            mask="a%s%s.dat"%(stm2id,year)
            
            sbdir2=w2.TcAdecksJtwcNhcDir
            mask2="ncep_a%s%s.dat"%(stm2id,year)
            mask2p1=None
            
            sbdir=w2.TcAdecksCmcDir
            sbdirdet=w2.TcAdecksCmcDir
            mask="%s/c???.*.cyclone.*atcfunix"%(dtg)
            detmask="%s/cmc.*.cyclone.*atcfunix"%(dtg)
            detmaskp1=None

        else:
            sbdir=w2.TcAdecksCmcDir
            sbdirdet=w2.TcAdecksCmcDir
            mask="%s/c???.*.cyclone.*atcfunix"%(dtg)
            detmask="%s/cmc.*.cyclone.*atcfunix"%(dtg)
            detmaskp1=None
            
            sbdir=w2.TcAdecksNcepDir
            mask="tracks.all.%s.txt"%(dtg)
            print 'mmmmmmmmmmmmmmmmmmmmm ',mask

        print 'CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCccc ',ncepSource,'mask: ',mask

        # go after det from nhc/jtwc adecks
        #
        rc=getadeckdet(stmid,year,cyp1,ncepSource)
        (sbdirdet,sbdir2,mask2,mask2p1,detmask,detmask2,detmaskp1)=rc


        
    elif(model == 'esrl'):
        sbdir=w2.TcAdecksEsrlDir
        sbdirdet=w2.TcAdecksEsrlDir
        mask="tacc/*%s*"%(dtg)
        detmask="tacc/*%s*.F9EM"%(dtg)

    elif(model == 'gfsenkf'):

        sbdir=w2.TcAdecksEsrlDir
        sbdirdet=w2.TcAdecksEsrlDir

        mask="%s/%s/track.%s.GE??"%(model,dtg,dtg)
        detmask="%s/%s/track.%s.GE00"%(model,dtg,dtg)


    elif(model == 'fimens'):

        sbdir=w2.TcAdecksTmtrkNDir
        sbdirdet=w2.TcAdecksTmtrkNDir

        dmodel='f9hj'
        mask="%s/tctrk.atcf.%s.fe??.???.????"%(dtg,dtg)
        detmask="%s/tctrk.atcf.%s.%s.???.????"%(dtg,dtg,dmodel)

        #for fimadeck in fimadecks:
        #    fixFimensAidName(fimadeck)

        sbdir2=w2.TcAdecksNcepDir
        mask2="tracks.all.%s.txt"%(dtg)


    elif(model == 'fnmoc'):
        adSource='dss'

    else:
        print 'EEE invalid model: ',model
        sys.exit()

    # -- get adecks from dss model=ncep-ecmwf
    #
    if(adSource != None):

        aDS=getAdsFromDss(adSource,stmid,verb=1)
        keys=aDS.getDataSet('keys').data

        ads={}
        taids=[]
        tstmids=[]

        for key in keys:
            taid=key.split('_')[0]
            tstmid=key.split('_')[1]
            taids.append(taid)
            tstmids.append(tstmid)

        taids=MF.uniq(taids)
        tstmids=MF.uniq(tstmids)

        for taid in taids:

            if( taid == 'ec00' or taid == 'emx' or(taid[0:2] == 'ep' or taid[0:2] == 'en' and taid[2:4].isdigit())):
                dskey="%s_%s"%(taid,stmid)
                try:
                    ad=aDS.db[dskey]
                    if(dtg in ad.dtgs):
                        ads[taid,stmid]=ad
                except:
                    None

        return(ads)




        
    else:

        adeckpathmask=("%s/%s/%s"%(sbdir,year,mask))

        if(detmask != None):
            adeckpathdetmask=("%s/%s/%s"%(sbdirdet,year,detmask))
            adeckpathmasks=[adeckpathdetmask]
            adeckpathmasks.append(adeckpathmask)

            print 'AAAA(w2-tc-g-epsanal.py) DDDDDDD: ',adeckpathmasks

            if(shemoverlap):
                if(detmaskp1 != None):
                    adeckpathdetmaskp1=("%s/%s/%s"%(sbdirdet,cyp1,detmaskp1))
                    adeckpathmasks.append(adeckpathdetmaskp1)

                adeckpathmaskp1=("%s/%s/%s"%(sbdir,cyp1,mask))
                adeckpathmasks.append(adeckpathmaskp1)

            if(detmask2 != None):
                adeckpathdetmask2=("%s/%s/%s"%(sbdir2,year,detmask2))
                adeckpathmasks.append(adeckpathdetmask2)


        else:
            adeckpathmasks=[adeckpathmask]
            if(shemoverlap):
                adeckpathmaskp1=("%s/%s/%s"%(sbdir,cyp1,mask))
                adeckpathmasks.append(adeckpathmaskp1)

        if(mask2 != None):
            adeckpathmask2=("%s/%s/%s"%(sbdir2,year,mask2))
            adeckpathmasks.append(adeckpathmask2)
            if(shemoverlap):
                if(mask2p1 != None):
                    adeckpathmask2p1=("%s/%s/%s"%(sbdir2,cyp1,mask2p1))
                    adeckpathmasks.append(adeckpathmask2p1)

        if(verb): print 'AAA GetModelAdecks: ',adeckpathmasks,dtg
        print 'AAA GetModelAdecks: ',adeckpathmasks,dtg,shemoverlap

        ad=Adeck(adeckpathmasks,dtgopt=dtg,verb=verb)

    return(ad)
        



def RegionalGrid(blat,elat,dlat,blon,elon,dlon,undef,taus,nmembers=None):

    from numpy import zeros
    
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
            grid=zeros((nmembers,nij))
        else:
            grid=zeros((nij))

        return(ni,nj,nij,grid)

        
    nt=len(taus)
    for tau in taus:
        
        if(nmembers != None):
            grid=zeros((nmembers,nij,nt))

        else:
            grid=zeros((nij,nt))
                    
            
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

    i=(lon - lon0)/dlon
    j=(lat - lat0)/dlat

    if(wrapx):
        if(i<=0):  i=ni+i
        if(i>=ni): i=i-ni

    i=int(i+0.5)
    j=int(j+0.5)

    ii=j*ni + i

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


def GetEaids(ad,model,dtg,verb=0):

    def IsEaid(iaid):
        rc=0
        if(iaid[0:2] == 'ep' and iaid[2].isdigit() and iaid[3].isdigit() ): rc=1
        return(rc)
            

    iaids=ad.aids
    eaids=[]
    if(model == 'esrl'):
        for iaid in iaids:
            if(verb): print 'iaid ',iaid
            if( (iaid[0:2].upper() == 'F8' and iaid[2:4].isdigit()) or iaid[0:4].upper() == 'F8EM' ):
                eaids.append(iaid)

    elif(model == 'gfsenkf'):
        for iaid in iaids:
            member=int(iaid[2:4])
            if(verb): print 'iaid gfsenkf',iaid,' model: ',model,' member: ',member
            # -- 2010: if( (iaid[0:2].upper() == 'GK') and (member >= 1 and member <= 21) ):  eaids.append(iaid)
            if( (iaid[0:2].upper() == 'GE') and (member >= 1 and member <= 21) ):  eaids.append(iaid)


    elif(model == 'fimens'):
        for iaid in iaids:
            member=999
            if(iaid[2:4].isdigit()):   member=int(iaid[2:4])
            if(verb): print 'iaid fimens',iaid,' model: ',model,' member: ',member
            iSgfsaid=( (iaid[0:2].upper() == 'AP') and (member >= 11 and member <= 20) )
            iSfimaid=( (iaid[0:2].upper() == 'FE') and (member >= 1 and member <= 10) )
            if(iSgfsaid or iSfimaid):  eaids.append(iaid)


    elif(model == 'ncep' and mf.find(ncepSource,'adeck') ):
        for iaid in iaids:
            if(verb): print 'iaid ncep ',iaid
            if( (iaid[0:2].upper() == 'AP' and iaid[2:4].isdigit()) or iaid.upper() == 'AC00'):
                eaids.append(iaid)

    elif(model == 'cmc' and mf.find(ncepSource,'adeck') ):
        for iaid in iaids:
            if(verb): print 'iaid cmc',iaid
            #if( (iaid[0:2].upper() == 'EP' and iaid[2:4].isdigit()) or iaid.upper() == 'ECNT'):
            if( (iaid[0:2].upper() == 'CP' and iaid[2:4].isdigit()) or iaid.upper() == 'CC00'):
                eaids.append(iaid)

    elif(model == 'fnmoc'):
        for iaid in iaids:
            if(verb): print 'iaid ',iaid,' model: ',model
            if( (iaid[0:2].upper() == 'NG' and iaid[2:4].isdigit()) ):
                eaids.append(iaid)

    else:
        for iaid in iaids:
            if(verb): print 'iaid ',iaid
            if(iaid != 'ecmt' and iaid != 'ecfx' and iaid != 'edet' and iaid != 'eanl' and IsEaid(iaid) ):
                eaids.append(iaid)
                
    eaids.sort()

    return(eaids)

def GetEaidsADs(ads,model,dtg,verb=0):

    kk=ads.keys()
    eaids=[]
    for k in kk:
        taid=k[0]
        if(taid == 'ec00' or (taid[0:2] == 'ep' or taid[0:2] == 'en' and taid[2:4].isdigit()) and model == 'ncep-ecmwf'):
            eaids.append(taid)

    eaids.sort()

    return(eaids)

def GetDetaidADs(ads,model,dtg,stm2id,verb=0):

    kk=ads.keys()
    iaids=[]
    for k in kk:
        iaids.append(k[0])

    eaids.sort()

    daid=None
    if('emx' in iaids): daid='emx'
    return(daid)


            


def GetDetaid(ad,model,dtg,stm2id,verb=0):

    def chkdtg(ad,dtg,sdaid,stm2id):
        rc=0
        try:
            sdtgs=ad.aiddtgs[sdaid,stm2id]
        except:
            sdtgs=[]

        if(dtg in sdtgs):
            rc=1
            return(rc)

        return(rc)
            

        
    iaids=ad.aids

    daid=None

    if(model == 'esrl'):
        sdaids=['f9em','f8em']

    elif(model == 'gfsenkf'):
        # 2010: sdaids=['gkdt']
        sdaids=['ge00']

    elif(model == 'fimens'):
        sdaids=['f9hj']

    #    elif(model == 'ncep' and mf.find(ncepSource,'adeck') ):
    elif(model == 'ncep'):
        sdaids=['avno','avni']

    elif(model == 'cmc' ):
        sdaids=['cmc']

    # go to adecks for ukmo deteriministic run --egrr
    #
    elif(model == 'ukmo'):
        sdaids=['egrr','egri','ukm2']

    elif(mf.find(model,'ecm')):
        sdaids=['edet']
    else:
        return(daid)

    for sdaid in sdaids:
        if(sdaid in iaids):
            rc=chkdtg(ad,dtg,sdaid,stm2id)
            if(rc):   daid=sdaid ;   return(daid)
                

    return(daid)


            

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


def MakeAdeckFile(ad,model,aids,stmid,dtg,taus,ddir,verb=0):

    adeckpath="%s/adeck.%s.%s.%s.txt"%(ddir,model,stmid,dtg)
    if(verb): print 'adeckpath ',adeckpath

    oadeck=[]
    
    for aid in aids:
        
        adeck=[]

        if(verb): 'MakeAdeckFile working aid: ',aid,'in ad.aids:',ad.aids
        if(not(aid in ad.aids)): continue

        for stm2id in ad.stm2ids:
            try:
                cards=ad.aidcards[aid,stm2id][dtg]
                if(verb): print 'YYYYYEEEESSSS got aid: ',aid,stm2id,' in MakeAdeckFile'
            except:
                cards=[]
                if(verb): print 'NNNNNNOOOOOOO got aid: ',aid,stm2id,' in MakeAdeckFile'
                continue

            for card in cards:
                adeck.append(card[:-1])

            for aa in adeck:
                #if(oaid != aid):
                #    iaidc="%4s"%(aid.upper())
                #    oaidc=oaid.upper()
                #    aa=aa.replace(iaidc,oaidc)
                oadeck.append(aa)

    if(len(oadeck) > 0):
        mf.WriteList(oadeck,adeckpath,verb=0)

    return(1)


def MakeAdeckFileADs(ads,model,aids,stmid,dtg,taus,ddir,verb=0):

    adeckpath="%s/adeck.%s.%s.%s.txt"%(ddir,model,stmid,dtg)
    if(verb): print 'adeckpath ',adeckpath

    oadeck=[]
    
    for aid in aids:
        
        adeck=[]

        cards=ads[aid,stmid].acards[dtg]

        if(verb): print 'aid: ',aid
        
        for card in cards:
            adeck.append(card[:-1])

        for aa in adeck:
            #if(oaid != aid):
            #    iaidc="%4s"%(aid.upper())
            #    oaidc=oaid.upper()
            #    aa=aa.replace(iaidc,oaidc)
            oadeck.append(aa)

    if(len(oadeck) > 0):
        mf.WriteList(oadeck,adeckpath,verb=0)

    return(1)




def AnalyzeMembers2Grid(tdir,model,ad,dtg,stmid,stm2id,taus,
                        dlatHit,dlonHit,
                        dlatSkp,dlonSkp,
                        undef,nmembers,
                        critdist=160.0,
                        dtinterp=3,
                        override=0,
                        veribt=0,
                        nhbackEps=taumaxBack, # change # h to display bt GetOpsRefTrk has nhback=48 which is ok 
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

    astm2id=stm2id

    # -- output the trackers for w2-tc-g-epsanal.gs -- deterministic
    #
    
    TE=open(trkepath,'w')
    TD=open(trkdpath,'w')

    dcard=''
    if(type(ad) is DictType):
        daid=GetDetaidADs(ad,model,dtg,stm2id)
    else:
        daid=GetDetaid(ad,model,dtg,stm2id)
    
    
    if(daid != None):

        print 'DDDeterministic got daid: ',daid,' DDDDDDDDDDDDDD'
    
        if(type(ad) is DictType):
            iad=ad[daid,stmid]
            for tau in taus:
                try:
                    (lat,lon,pmin,vmax,r34,r50,r64)=iad.ats[dtg][tau]
                    dcard="%s %5.1f %6.1f"%(dcard,lat,lon)
                except:
                    if(verb): print 'WWWDDD--dict no tracks deterministic aid: ',daid,stmid,dtg,tau

        else:
            for tau in taus:
                try:
                    (lat,lon,pmin,vmax,r34,r50,r64)=ad.aidtrks[daid,astm2id][dtg][tau]
                    dcard="%s %5.1f %6.1f"%(dcard,lat,lon)
                except:
                    if(verb): print 'WWWDDD-obj no tracks deterministic aid: ',daid,astm2id,dtg,tau
                    
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

            if(type(ad) is DictType):
                iad=ad[eaid,stmid]
                try:
                    (lat,lon,pmin,vmax)=iad.ats[dtg][tau]
                    lats.append(lat)
                    lons.append(lon)
                    pmins.append(pmin)
                    vmaxs.append(vmax)
                except:
                    if(verb): print 'NNNN no ads.tracks for ',eaid,stmid,dtg,tau


            else:
                try:
                    (lat,lon,pmin,vmax,r34,r50,r64)=ad.aidtrks[eaid,astm2id][dtg][tau]
                    lats.append(lat)
                    lons.append(lon)
                    pmins.append(pmin)
                    vmaxs.append(vmax)
                except:
                    if(verb): print 'NNNN no tracks for ',eaid,astm2id,dtg,tau

            
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
            if(type(ad) is DictType):
                iad=ad[eaid,stmid]
                try:
                    (lat,lon,pmin,vmax)=iad.ats[dtg][tau]
                    lats.append(lat)
                    lons.append(lon)
                    ecard="%s %5.1f %6.1f"%(ecard,lat,lon)
                except:
                    if(verb): print 'NNNN no ads.tracks for ',eaid,stmid,dtg,tau


            else:
                try:
                    (lat,lon,pmin,vmax,r34,r50,r64)=ad.aidtrks[eaid,astm2id][dtg][tau]
                    lats.append(lat)
                    lons.append(lon)
                    ecard="%s %5.1f %6.1f"%(ecard,lat,lon)

                except:
                    if(verb): print 'NNNN no tracks for ',eaid,astm2id,dtg,tau

        ecard=ecard+'\n'
        TE.writelines(ecard)

    TE.close()

    
    # -- bts
    #

    (btcards,btcardsgt0,btlats,btlons,btvmaxs,btpmins)=GetBtcardsLatLonsFromMdeck(stmid,dtg,nhback=nhbackEps,
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

    mf.WriteList(btcards,btpath)
    mf.WriteList(btcardsgt0,btpathgt0)

    astm2id=stm2id
    if(astm2id == None):
        print 'WWW**** unable to find stm2id in adeck corresponding to stmid: ',stmid
        return(0)

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
    
    itrks={}
    jtrks={}
    jtrkDeftaus={}



    if(type(ad) is DictType):

        iads=ad
        for eaid in eaids:
            iad=iads[eaid,stmid]
            try:
                iad=iads[eaid,stmid]
                itrks[eaid]=iad.ats[dtg]
                gotit=1
            except:
                gotit=0
                if(verb): print 'NNN-dicttype no tracks for eaid: ',eaid,astm2id,dtg
            if(gotit):
                (jtrks[eaid],jtrkDeftaus[eaid])=iad.FcTrackInterpFill(itrks[eaid],dtx=dtinterp,npass=0,verb=verb)


    else:
        
        for eaid in eaids:
            try:
                itrks[eaid]=ad.aidtrks[eaid,astm2id][dtg]
                gotit=1
            except:
                gotit=0
                if(verb): print 'NNN-objtype no tracks for eaid: ',eaid,astm2id,dtg
            if(gotit):
                (jtrks[eaid],jtrkDeftaus[eaid])=ad.FcTrackInterpFill(itrks[eaid],dtx=dtinterp,npass=0,verb=verb)


    if(override2 or veribt): doanal=0

    if(doanal):

        MF.sTimer(tag='doanal')
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

        for l in range(0,len(taus)):

            tau=taus[l]

            for n in range(0,len(eaids)):
                eaid=eaids[n]

                try:
                    rc=jtrks[eaid][tau][0:4]
                    (lat,lon,vmax,pmin)=rc
                    gotit=1
                except:
                    gotit=0
                    if(verb): print 'NNN no jjjjjjjjtracks for eaid: ',eaid,astm2id,dtg,tau

                if(gotit and ChkLatLonBounds(lat,lon,blat,blon,elat,elon) == 0):
                    gotit=0

                if(gotit):
                    itau=int(tau)
                    ii=ll2ii(lon,lat,dlonHit,dlatHit,blon,blat,nihit,njhit)
                    (i,j)=ii2ij(ii,nihit,njhit)
                    if(verb): print 'AAAA0000 ',eaid,tau,blat,' aidlat',lat,elat,blon,' aidlon',lon,elon
                    grid[ii,l]=grid[ii,l]+1.0
                    ntau[tau]=ntau[tau]+1.0


        #ssssssssssssssssssssssssssssssssssssssssssssssssss
        #
        # strike prob - grids

        otaus=range(0,taus[-1]+1,dtinterp)

        MF.sTimer(tag='make skp grids')
        (niskp,njskp,nijskp,grid2)=RegionalGrid(blat,elat,dlatSkp,blon,elon,dlonSkp,undef,otaus,nmembers)
        (niskp,njskp,nijskp,gridsp)=RegionalGrid(blat,elat,dlatSkp,blon,elon,dlonSkp,undef,otaus)
        (niskp,njskp,nijskp,grid1n)=RegionalGrid(blat,elat,dlatSkp,blon,elon,dlonSkp,undef,None,nmembers)
        RegionalCtl(dsetSkp,cpathSkp,dtg,niskp,njskp,blat,dlatSkp,blon,dlonSkp,undef,taus,var='sp')
        MF.dTimer(tag='make skp grids')


        #ssssssssssssssssssssssssssssssssssssssssssssssssss
        #
        # strike prob - analysis

        MF.sTimer(tag='skp analysis ')
        
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
                    if(verb): print 'NNN no tracks for eaid: ',eaid,astm2id,dtg,tau

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

        MF.dTimer(tag='skp analysis ')

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

        MF.dTimer(tag='doanal')
        
    print 'AAA out of doanal'


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
models:  ncep; cmc; ecmwf; ukmo; esrl; gfsenkf; fimens'''
        
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

if(w2.W2doTcepsAnl == 0):
    print 'WWWWWWWWWWWWWWWWWW - turned off in w2switches.py'
    sys.exit()


ncepSource=w2.TcTcepsNcepSource
if(adeckonly): ncepSource='adeckonly'
if(doxml):     ncepSource='xml'

dtgs=mf.dtg_dtgopt_prc(dtgopt,ddtg=6)

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
#

xsize=1200

xgrads=setXgrads(useX11=0)
if(mf.find(W2Host,'clim')): xgrads='grads2p1'

prcdir=w2.PrcDirTcdatW2
mf.ChangeDir(prcdir)

year=dtg[0:4]


#----------------------------------------------
# model/ dir setup
#

allmodels=['ecmt','ukmo','ncep','cmc','esrl','gfsenkf','fimens']
allmodels06=['ncep','gfsenkf','fimens']

allmodels=['ecmt','ukmo','ncep','cmc']
allmodels06=['ncep','ukmo']

if(model == 'ncep-ecmwf'):
    
    sbdir=w2.TcAdecksEcmwfDir
    tbdir=w2.TcTcepsEcmwfDir
    nmembers=w2.TcTcepsEcmwfNmembers
    
elif(mf.find(model,'ecm')):
    
    sbdir=w2.TcAdecksEcmwfDir
    tbdir=w2.TcTcepsEcmwfDir
    nmembers=w2.TcTcepsEcmwfNmembers
    model='ecmt'
    
elif(mf.find(model,'ukm')):

    sbdir=w2.TcAdecksuKmoDir
    tbdir=w2.TcTcepsuKmoDir
    nmembers=w2.TcTcepsuKmoNmembers
    model='ukmo'

elif(mf.find(model,'ncep')):

    sbdir=w2.TcAdecksNcepDir
    tbdir=w2.TcTcepsNcepDir
    nmembers=w2.TcTcepsNcepNmembers
    model='ncep'

elif(mf.find(model,'cmc')):

    sbdir=w2.TcAdecksCmcDir
    tbdir=w2.TcTcepsCmcDir
    nmembers=w2.TcTcepsCmcNmembers
    model='cmc'

elif(mf.find(model,'esrl')):

    sbdir=w2.TcAdecksEsrlDir
    tbdir=w2.TcTcepsEsrlDir
    nmembers=w2.TcTcepsEsrlNmembers
    model='esrl'

elif(mf.find(model,'gfsenkf')):

    sbdir=w2.TcAdecksGfsenkfDir
    tbdir=w2.TcTcepsGfsenkfDir
    nmembers=w2.TcTcepsGfsenkfNmembers
    model='gfsenkf'

elif(mf.find(model,'fimens')):

    sbdir=w2.TcAdecksGfsenkfDir
    tbdir=w2.TcTcepsFimensDir
    MF.ChkDir(tbdir,'mk')
    nmembers=w2.TcTcepsFimensNmembers
    model='fimens'

elif(mf.find(model,'fnmoc')):

    sbdir=w2.TcAdecksFnmocDir
    tbdir=w2.TcTcepsFnmocDir
    nmembers=w2.TcTcepsFnmocNmembers
    model='fnmoc'

elif(model == 'all'):
    
    for model in allmodels:
        cmd="%s %s %s"%(pyfile,dtgopt,model)
        for o,a in CL.opts:
            cmd="%s %s %s"%(cmd,o,a)
        mf.runcmd(cmd,ropt)

    sys.exit()

else:
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

tD=TcData(dtgopt=dtg)
stmids=tD.getStmidDtg(dtg, dobt=0, dupchk=0, selectNN=1, verb=0)

if(stmopt != None):
    stmids=MakeStmList(stmopt,verb=0)
    

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

print 'NNN  nplotsDONE: ',nplotsDONE
print 'NNN   ndaidDONE: ',ndaidDONE
print 'NNN  neaidsDONE: ',neaidsDONE

nplots=0
didplots=0
for stmid in stmids:
    
    MF.sTimer("DID stmid: %s dtg: %s"%(stmid,dtg))

    # -- check # members/det trackers -- for gfsenkf now...
    #
    #if(model == 'gfsenkf' or model == 'fimens'):
    #    rc=chkModelAdecks(dtg,stmid,model,nmembers,verb=verb,reqdet=0)
    #    if(rc == 0):
    #        print 'III not all adecks available for model: ',model,' at dtg: ',dtg,' stmid: ',stmid
    #        continue


    # -- make Adeck object; and get ensemble eaids and deterministic aids
    #
    ad=GetModelAdecks(dtg,stmid,model,verb=verb)
    
    stm2id=stm1idTostm2id(stmid)

    if(model == 'ncep-ecmwf'):
        eaids=GetEaidsADs(ad,model,dtg,verb=verb)
        daid=GetDetaidADs(ad,model,dtg,stm2id,verb=verb)
    else:
        eaids=GetEaids(ad,model,dtg,verb=verb)
        daid=GetDetaid(ad,model,dtg,stm2id,verb=verb)
    
    if(daid != None):
        allaids=eaids+[daid]
    else:
        allaids=eaids

    if(model == 'ncep-ecmwf'):
        etrksThere=0
        if(len(eaids) > 0): etrksThere=1

        dtrkThere=0
        if(daid != None): dtrkThere=1

    else:
        etrksThere=ChkEaids(ad,eaids,stm2id,dtg)
        dtrkThere=ChkDaid(ad,daid,stm2id)

        
    print 'Eaids: ',eaids,stm2id,etrksThere
    print ' Daid: ',daid,' dtrkThere: ',dtrkThere

    ## if(type(ad) is DictType and len(allaids) > 0):
    ##     iads=ad
    ##     for k in iads.keys():
    ##         aa=iads[k]
    ##         aa.ls()
    ##     sys.exit()
        
    # 20120825 -- check log to see if we need to redo the plots...
    # -- for the case of det aid now available, typically gfsenkf

    if(nplotsDONE > 0 and ndaidDONE == 0 and daid != None):
        print 'III setting override2=1'
        override2=1
        
    
    #if(model == 'gfsenkf' and ( (len(eaids) < nmembers or daid == None) ) ):
    # -- for the gfsenkf require the detaid be there
    if(model == 'gfsenkf' and ( (len(eaids) < nmembers) ) and dtrkThere):
        print 'WWW(gfsenkf) no or not enough member trackers and det tracker for stmid: ',stmid,' stm2id: ',stm2id
        continue

    elif(model == 'fimens' and (len(eaids) <= 1  or len(eaids) < nmembers or etrksThere == 0 ) ):
        print 'WWW(fimens) no or not enough trackers...stmid: ',stmid,' stm2id: ',stm2id
        continue

    elif(len(eaids) <= 1 or etrksThere == 0):
        print 'WWW no or not enough trackers for model: ',model,' and stmid: ',stmid,' stm2id: ',stm2id,eaids
        continue

    try:
        adecksthere= (len(ad.stmdtgs[stm2id]) > 0 and findstmdtg(ad.stmdtgs[stm2id],dtg) )
    except:
        adecksthere=0

    if(type(ad) is DictType and len(allaids) > 0):
        adecksthere=1

    docleanPlots=0
    if(override or override2):
        docleanPlots=1

    # -- check if plots made
    #
    (nplots,plots)=GetPlotPaths(pdir,stmid,model,taus,ptypes,doclean=docleanPlots)
    (nplots,plots)=GetPlotPaths(wdir,stmid,model,taus,ptypes,doclean=docleanPlots)

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
        print 'WWWWWWW plots already done, override: %s, verbbt: %s for stmid: %s'%(override,veribt,stmid)
        
        # -- override2 -- just plot, no analysis
        #
        if(override2):
            doplots=1
        elif(override == 0 and veribt == 0 and doadeckonly == 0):
            continue

    if(veribt): doplots=1

    # -- make adeck file for display
    #
    if(type(ad) is DictType):
        rc=MakeAdeckFileADs(ad,model,allaids,stmid,dtg,taus,pdir,verb=verb)
    else:
        rc=MakeAdeckFile(ad,model,allaids,stmid,dtg,taus,pdir,verb=verb)

    cmd="cp %s/adeck.*.txt %s/."%(pdir,wdir)
    mf.runcmd(cmd,'')
    if(doadeckonly): continue

        
    if( adecksthere and doplots or (override != 0) ):

        rc=AnalyzeMembers2Grid(ddir,model,ad,dtg,stmid,stm2id,taus,
                               dlatHit,dlonHit,
                               dlatSkp,dlonSkp,
                               undef,nmembers,
                               critdist,
                               override=override,
                               veribt=veribt,
                               verb=verb)


        stmname=GetTCName(stmid)
        stmname=stmname.upper()
        print 'SSS   stmid: ',stmid
        print 'SSS stmname: ',stmname
        
        if(rc):

            #
            # make tau pngs
            #
            curpid=os.getpid()
            gscrp='w2-tc-g-epsanal.gs'
            gsopt="%s %s %s %s %s %s %5.0f %i %i %i %i %i %i"%(stmid,stmname,dtg,model,ddir,pdir,critdist,nmembers,ntaumax,dtau,veribt,xsize,int(curpid))
            gacmd="%s -lbc \"%s %s\""%(xgrads,gscrp,gsopt)
            mf.runcmd(gacmd,ropt)

            #
            # make animated loop gifs
            #
            for ptype in ptypes:
                MakeAnimatedGif(pdir,stmid,model,taus,ptype,convertexe,
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

            MF.dTimer("DID stmid: %s dtg: %s"%(stmid,dtg))


# 20120825 -- log
#

if(len(stmids) == 0):
    print 'WWW(w2-tc-g-epsanal.py) no storms from the xml/adecks...sayoonara'
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

