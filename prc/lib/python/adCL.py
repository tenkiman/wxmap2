from tcVM import *  # tcVM imports M, makes MFutils()
from adVM import *

ptmpBaseDir=w2.ptmpBaseDir


class LocalGfsEnsemble(MFbase):
    
    emean='faemn'
    esprd='faesp'
    
    nmembers=20
    members=[]
    for n in range(1,nmembers+1):
        members.append("nap%02d"%(n))
        
class LocalPsdRR2Ensemble(MFbase):
    
    emean='rr2em'
    esprd='rr2es'
    
    nmembers=10
    members=[]
    for n in range(1,nmembers+1):
        members.append("rr2%02d"%(n))
        
        
        
class EpsEnsemble(MFbase):
    
    emean='feemn'
    esprd='feesp'
    
    nmembers=50
    members=[]
    for n in range(1,nmembers+1):
        members.append("ep%02d"%(n))
        
class C41r2EpsEnsemble(MFbase):
    
    emean='fe4mn'
    esprd='fe4sp'
    
    nmembers=50
    members=[]
    for n in range(1,nmembers+1):
        members.append("e4%02d"%(n))
        
class NcepEpsEnsemble(MFbase):
    
    emean='neemn'
    esprd='neesp'
    
    nmembers=50
    nmembersHalf=25
    members=[]
    for n in range(1,nmembersHalf+1):
        members.append("nep%02d"%(n))
        
    for n in range(1,nmembersHalf+1):
        members.append("nen%02d"%(n))
            
        
class FimGfsEnsemble(MFbase):
    
    emean='ffgmn'
    esprd='ffgsp'
    
    nmembers=20
    nmembersHalf=10
    members=[]
    for n in range(nmembersHalf+1,nmembers+1):
        members.append("nap%02d"%(n))
        
    for n in range(1,nmembersHalf+1):
        members.append("tfe%02d"%(n))
            

class FimGfsPhysicsEnsemble(MFbase):
    
    emean='fgomn'
    esprd='fgosp'
    
    nmembers=5
    members=[]
        
    for n in range(1,nmembers+1):
        members.append("tfe%02d"%(n))
            
class FimGrellFrietasEnsemble(MFbase):
    
    emean='fgfmn'
    esprd='fgfsp'
    
    nmembers=5
    members=[]
        
    for n in range(1,nmembers+1):
        nn=n+5
        members.append("tfe%02d"%(nn))
            
        
    

class AdeckEnsemble(MFbase):

    validEmeans=[
        'psdr2','ngeps','eeps','e4ps','neeps',
        'fgeps','fgops','fgfps',
    ]
    
    def __init__(self,
                 tD,tstmids,A2DSs,B2DS,
                 dbnames,basins,byears,
                 emean='naemn',
                 dbtype=None,
                 tdir=None,
                 verb=0,
                 verb2=0,
                 overrideAD2=0,
                 dochkIfRunning=1,
                 etau=168,
                 dtau=12,
                 pyfile='w2-tc-dss-ad2.py',
                 corrTauInc=12,
                 ):

        self.taus=range(0,etau+1,dtau)
        self.emean=emean
        self.verb=verb
        self.verb2=verb
        self.overrideAD2=overrideAD2
        self.ens=None
        self.dochkIfRunning=dochkIfRunning
        self.pyfile=pyfile
        self.corrTauInc=corrTauInc

        self.dbtype=dbtype
        self.tdir=tdir
        self.dochkIfRunning=dochkIfRunning
        self.dbnames=dbnames
        self.basins=basins
        self.byears=byears
        
        
        if(not(emean in self.validEmeans)):
            print 'EEE invalid Ensemble class for emean: \'%s\''%(emean),' not in: ',self.validEmeans
            sys.exit()
            
        if(emean == 'psdr2'):  self.ens=LocalPsdRR2Ensemble()
        if(emean == 'ngeps'):  self.ens=LocalGfsEnsemble()
        if(emean == 'eeps'):   self.ens=EpsEnsemble()
        if(emean == 'e4ps'):   self.ens=C41r2EpsEnsemble()
        if(emean == 'neeps'):  self.ens=NcepEpsEnsemble()
        if(emean == 'fgeps'):  self.ens=FimGfsEnsemble()
        if(emean == 'fgops'):  self.ens=FimGfsPhysicsEnsemble()
        if(emean == 'fgfps'):  self.ens=FimGrellFrietasEnsemble()
        
        ad2s={}
        
        eaids=self.ens.members
        omodel=self.ens.emean
        smodel=self.ens.esprd
        

        for tstmid in tstmids:
            
            dobtMD2=1
            if(Is9X(tstmid)): dobtMD2=0
            mD2=tD.getDSsStm(tstmid,dobt=dobtMD2) 
            mD2C=tD.getDSsStm(tstmid,dobt=0)
            (Xsnum,Xb1id,byear,Xb2id,Xstm2id,Xstm1id)=getStmParams(tstmid)
            
            basin=getBasinFromStmid(tstmid)

            ATs={}
            a2DS=A2DSs[basin,byear]
            for taid in self.ens.members:   
                dskey="%s_%s"%(taid,tstmid.upper())
                (AT,BT,aD)=getAidAdeck2Bdeck2FromDss(a2DS,B2DS,taid,tstmid,verb=verb2,warn=1)
                if(AT != None): ATs[taid]=AT    
                    
            (emtrks,emacards)=self.setEnsMeanTrk(ATs,eaids,self.taus,omodel,tstmid,percentMin=40.0,verb=self.verb2)
            (estrks,esacards)=self.setEnsSpreadTrk(emtrks,ATs,BT,eaids,self.taus,smodel,tstmid,verb=self.verb2)

            if(len(emacards) == 0): continue
            # -- make Adeck2
            #
            MF.sTimer('ads-%s'%(tstmid))
            aD2=Adeck2s(tstmid,corrTauInc=corrTauInc,acards=emacards,mD2=mD2C)
            
            newad2s=aD2.getAD2s(tstmid)
            ad2s.update(newad2s)
            
            aD2=Adeck2s(tstmid,acards=esacards,corrTauInc=corrTauInc,mD2=mD2C)
            newad2s=aD2.getAD2s(tstmid)
            ad2s.update(newad2s)
            
            MF.dTimer('ads-%s'%(tstmid))            
        
        self.ad2s=ad2s
        self.basins=mf.uniq(basins)
        self.byears=byears
        
    def putAd2s(self,warn=0):
        
        if(self.dochkIfRunning == 0): rc=chkRunning(self.pyfile,strictChkIfRunning=1,killjob=1)
        
        MF.sTimer('ads-put')
        (aDSss,basins)=putAdeck2sDataSets(self.ad2s,dbtype=self.dbtype,dsbdir=self.tdir,
                                          doclean=self.overrideAD2,
                                          verb=self.verb)
        
        MF.dTimer('ads-put')
    
        for byear in self.byears:
            for basin in basins:
                try:
                    aDSs=aDSss[basin,byear]
                    asiz=MF.getPathSiz(aDSs.path)
                    asiz=float(asiz)/(1024*1024)
                    MF.sTimer('ads-put-%-5.0f Mb'%(asiz))
                    MF.dTimer('ads-put-%-5.0f Mb'%(asiz))
                except:
                    if(warn): print 'WWW(AdeckEnsemble.putAd2s): could not find aDSss for basin: ',basin,'byear: ',byear
                    continue
        
        
    def setEnsMeanTrk(self,ATs,eaids,taus,model,stmid,percentMin=40.0,minTau0=0,percentMin0=70.0,verb=0):
    
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
        acards=''
    
        for dtg in alldtgs:
    
            iokmean=0
            tau0ok=1
            pnll=999.
    
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
                        # -- handle new and old adecks
                        #
                        rc=aT[dtg][tau]
                        if(len(rc) == 4):
                            (lat,lon,vmax,pmin)=rc
                        elif(len(rc) == 7):
                            (lat,lon,vmax,pmin,r34,r50,r65)=rc
                            
                        lats.append(lat)
                        lons.append(lon)
                        if(vmax <= 0.0):
                            vmax=-999.0
                        if(pmin < 0.0):
                            pmin=-999.0
                        vmaxs.append(vmax)
                        pmins.append(pmin)
                        iok=1
                        iokAid=1
                    except:
                        iokAid=0
                        if(verb > 1): print 'NNNN tracks for: ',eaid,dtg,tau,' <- NNNNN'
    
                    if(verb > 1 and iokAid):
                        print 'FFFF tracks for: ',eaid,dtg,tau,lat,lon
    
    
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
                        print 'WWW tau0ok=0 pnll: %3.0f'%(pnll),' stmid: ',stmid,' dtg: ',dtg
                        tau0ok=0
    
                    if(nll > 0 and pnll >= percentMin and tau0ok):
                        iokmean=1
                        mlat=mlat/float(nll)
                        mlon=mlon/float(nll)
    
                        if(nvm > 0):
                            mvmax=mvmax/float(nvm)
    
                        if(npm > 0):
                            mpmin=mpmin/float(npm)
    
                        if(verb): print 'nll---- %7s %s %3d'%(self.emean,dtg,tau),\
                        "P: %4.0f or %2d/%2d"%(pnll,nll,nmembers)," Lat/Lon: %4.1f  %5.1f"%(mlat,mlon),\
                        ' nvm: %2d Vmax: %3.0f'%(nvm,mvmax),' npm: %2d Pmin: %4.0f '%(npm,mpmin)
    
                        try:
                            emtrks[dtg][tau]=(mlat,mlon,mvmax,mpmin,None,None,None,pnll)
                        except:
                            emtrks[dtg]={}
                            emtrks[dtg][tau]=(mlat,mlon,mvmax,mpmin,None,None,None,pnll)
    
    
            if(iokmean):
                acds=MakeAdeckCards(model,dtg,emtrks[dtg],stmid)
                for acd in acds:
                    acards=acards+acd
    
            elif(tau0ok):
                print 'WWW could not make mean track for         dtg: ',dtg,' ---------------'
    
        return(emtrks,acards)
    
    
    def setEnsSpreadTrk(self,emtrks,ATs,BT,eaids,taus,model,stmid,verb=0):
    
    
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
        acards=''
    
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
                    if(verb >= 1): print 'NNNN-------MMMM no mean posit for: ',dtg,tau
    
    
    
                mdist=0.0
                nd=0
                iok=0
                
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
                        iokSp=1
                    except:
                        iokSp=0
                        if(verb > 1): print 'NNNN posit for: ',eaid,dtg,tau,' <- NNNNN (spread)'
    
    
                    if(verb > 1 and iokSp):
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
                for acd in acds:
                    acards=acards+acd
    
            else:
                #trk=estrks[dtg]
                #acards[dtg]=AD.MakeAdeckCards(omodel,dtg,trk,stmid,verb=verb)
                print 'SSSS(spread) found NO mean tracks at ANY tau for dtg: ',dtg
    
    
    
        return(estrks,acards)


                    


                    
        
        
        
        
        



#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc -- AdeckSources -- set adecksource: fim retros, mf/tmtrkN...
#
#
class AdeckSources(MFbase):
    
    sources2009=['nhc','jtwc',
                 'rtfim','rtfimx','rtfimy',
                 'tacc','gfsenkf',
                 'ncep','ecmwf','ukmo',
                 'ncep_eps','cmc_eps',
                 'local','wxmap2','w2flds',
                 ]
    
    sources=['best','nhc','jtwc','ncep','ecmwf','ukmo','ncep_eps','cmc_eps',
             'local','wxmap2','w2flds',
             ]

    sourcesAll=sources+['tmtrkN','mftrkN']
    
    # -- sources where the file uses current dtg irrespective of storm.year
    #
    sourcesDtg=['tmtrkN','mftrkN','ncep','ecmwf','ecbufr']
    
    def __init__(self,sources=None,year=None,skipcarq=1,verb=0,dojettrack=0):
        """ add skipcarq to the AdeckSources object for use in Adeck()"""
        if(sources == None):
            self.sources=self.sources
        else:
            self.sources=sources

        self.verb=verb
        self.skipcarq=1
        self.dojettrack=dojettrack
        
    def getSourcesbyYear(self,year=None):
        
        if(year != None and year == '2009'):
            self.sources=self.sources2009
            return(self.sources2009)
        else:
            return(self.sources)

    def setAdeckSource(self,source,year,dojettrack=0,dtgopt=None,dochk=0,
                       useAdeckDir=0,
                       ZIPoverride=0,
                       usePtmpDir=0,
                       useZipArchive=1,
                       yearMasks=None,
                       verb=0):

        from tcbase import TcDataBdir

        self.dochk=dochk

        ad=None
        aliases=None

        self.skipcarq=1
        self.dojettrack=dojettrack
        
        if(source == 'gfsenkf' or source == 'gfsenkf_irwd' or source == 'gfsenkf_irwdx'
           ):

            
            bdir="%s/adeck/esrl/%s/%s"%(TcDataBdir,year,source)
            ad=AdeckSource(source=source,
                           year=year,
                           dirname=source,
                           bdir=bdir,
                           sdir=bdir,
                           stype=source,
                           )

            if(int(year) == 2009):
                smask="%s/track.%s*.txt"%(ad.bdir,ad.year)

            # -- new form where organized by dtg
            #
            elif(int(year) == 2011):
                smask="%s/??????????/track*%s*"%(ad.bdir,ad.year)
            else:
                smask="%s/??????????/tctrk.atcf.%s*.txt"%(ad.bdir,ad.year)
                
            print 'SSSSSS setAdeckSources.smask: ',smask
            ad.admasks=[smask]

        elif(mf.find(source,'jet_')):
            osource=source
            source=source.replace('jet_','')
            
            bdir="%s/adeck/esrl/%s/%s"%(TcDataBdir,year,source)
            ad=AdeckSource(source=source,
                           year=year,
                           dirname=source,
                           bdir=bdir,
                           sdir=bdir,
                           stype=source,
                           )

            smask="%s/track*%s*"%(ad.bdir,ad.year)
            source=osource
                
            print 'SSSSSS setAdeckSources.smask(jet_): ',smask
            ad.admasks=[smask]

        # -- latest MF tracker
        #
        elif(source == 'mftrkN' or source == 'mftrk'):
            
            dozip=1
            if(not(useZipArchive)): dozip=0
            
            mfVersion='v010'
            mfVersion='v011'
            # -- force using adeckdir
            #
            useAdeckDir=1
            
            osource=source
            bdir="%s/tmtrkN"%(TcDataBdir)
            sdir=bdir
            if(useAdeckDir):
                bdir="%s/adeck/mftrkN"%(TcDataBdir)

            ad=AdeckSource(source=source,
                           year=year,
                           dirname=source,
                           bdir=bdir,
                           sdir=sdir,
                           stype=source,
                           dozip=dozip,
                           ZIPoverride=ZIPoverride,
                           )

            if(usePtmpDir):
                ad.bdir=ad.tdirZIP
                ad.sdir=ad.bdir


            ad.admasks=[]
            ad.filemasks=[]

            if(dtgopt != None):
                dtgs=mf.dtg_dtgopt_prc(dtgopt)
                for dtg in dtgs:

                    admaskm1=None
                    curyear=dtg[0:4]

                    filemask="wxmap2.%s.*%s.*.%s"%(mfVersion,dtg,year)
                    if(useAdeckDir):
                        # -- 20140929 - since we're setting the admask here by dtg, check for shemover
                        #
                        if(int(curyear)-int(year) == -1):
                            admaskm1="%s/%s/%s/%s"%(ad.bdir,curyear,dtg,filemask)
                        admask="%s/%s/%s/%s"%(ad.bdir,year,dtg,filemask)
                    elif(usePtmpDir):
                        admask="%s/%s"%(ad.bdir,filemask)
                    else:
                        admask="%s/%s/*/%s"%(ad.bdir,dtg,filemask)
                        
                    if(admaskm1 != None):
                        ad.admasks.append(admaskm1)
                        ad.filemasks.append(filemask)
                        
                    ad.admasks.append(admask)
                    ad.filemasks.append(filemask)

            elif(yearMasks != None):
                ad.year=yearMasks[0]
                ad.yearp1=yearMasks[1]

                for year in yearMasks:
                    
                    filemask="wxmap2.%s.*.%s??????.*"%(mfVersion,year)
                    if(useAdeckDir):
                        admask="%s/%s/??????????/%s"%(ad.bdir,year,filemask)
                    elif(usePtmpDir):
                        admask="%s/%s"%(ad.bdir,filemask)
                        ad.dozip=0  # turn off zip
                    else:
                        admask="%s/%s??????/*/%s"%(ad.bdir,year,filemask)
                        
                    ad.filemasks.append(filemask)
                    ad.admasks.append(admask)

                print 'III adCL.setAdeckSource.yearMasks: ',yearMasks

            else:
                # -- use full stmid label in filename to get just the storms for a year
                #    only works with mftrack...20140107 -- changed tmtrkN to do the same
                # -- trackers org by NNB.YYYY as with mftrkN
                #    go back one year for SHEM storms
                #
                yearsAD=[mf.yyyyinc(year,-1),year]
                
                for yearAD in yearsAD:
                
                    filemask="wxmap2.%s.*.??????????.*.%s"%(mfVersion,year)
                    
                    if(useAdeckDir):
                        admask="%s/%s/??????????/%s"%(ad.bdir,yearAD,filemask)
                    elif(usePtmpDir):
                        filemask="wxmap2.%s.*.*.%s"%(mfVersion,year)
                        admask="%s/%s"%(ad.bdir,filemask)
                        ad.dozip=0   # turn off zip here...
                    else:
                        admask="%s/%s??????/*/%s"%(ad.bdir,yearAD,filemask)
                
                    ad.filemasks.append(filemask)
                    ad.admasks.append(admask)

            source=osource
            print 'SSS(smask) setAdeckSources.smask(mftrkN): ',ad.admasks

        # -- latest TM tracker
        #
        elif(source == 'tmtrkN'):

            dozip=1
            if(not(useZipArchive)): dozip=0
            
            osource=source
            
            # -- force using adeckdir
            #
            useAdeckDir=1
            
            bdir="%s/tmtrkN"%(TcDataBdir)
            # -- use adeck dir vice prc dir
            sdir=bdir
            if(useAdeckDir):
                bdir="%s/adeck/tmtrkN"%(TcDataBdir)
            
            ad=AdeckSource(source=source,
                           year=year,
                           dirname=source,
                           bdir=bdir,
                           sdir=sdir,
                           stype=source,
                           dozip=dozip,
                           ZIPoverride=ZIPoverride,
                           )
            if(usePtmpDir):
                ad.bdir=ad.tdirZIP
                ad.sdir=ad.bdir

            ad.admasks=[]
            ad.filemasks=[]

            if(dtgopt != None):
                dtgs=mf.dtg_dtgopt_prc(dtgopt)
                for dtg in dtgs:
                    admaskm1=None
                    curyear=dtg[0:4]
                    filemask="tctrk.atcf.%s.*.*.txt"%(dtg)
                    filemask="tctrk.atcf.??????????.*.*.%s"%(year)
                    # -- 20140929 - since we're setting the admask here by dtg, check for shemover
                    #
                    if(useAdeckDir):
                        if(int(curyear)-int(year) == -1):
                            admaskm1="%s/%s/%s/%s"%(ad.bdir,curyear,dtg,filemask)
                        admask="%s/%s/%s/%s"%(ad.bdir,year,dtg,filemask)
                    elif(usePtmpDir):
                        admask="%s/%s"%(ad.bdir,filemask)
                    else:
                        admask="%s/%s/*/%s"%(ad.bdir,dtg,filemask)

                    if(admaskm1 != None):
                        ad.admasks.append(admaskm1)
                        ad.filemasks.append(filemask)
                        
                    ad.admasks.append(admask)
                    ad.filemasks.append(filemask)
                
                print 'III adCL.setAdeckSource.dtgopt: ',year,ad.admasks

            elif(yearMasks != None):
                ad.year=yearMasks[0]
                ad.yearp1=yearMasks[1]

                for year in yearMasks:
                    
                    filemask="tctrk.atcf.%s??????.*.*.txt"%(year)
                    if(useAdeckDir):
                        admask="%s/%s/??????????/%s"%(ad.bdir,year,filemask)
                    elif(usePtmpDir):
                        admask="%s/%s"%(ad.bdir,filemask)
                        ad.dozip=0 # turn off zip...
                    else:
                        admask="%s/%s??????/*/%s"%(ad.bdir,year,filemask)
                                    
                    ad.filemasks.append(filemask)
                    ad.admasks.append(admask)

                print 'III adCL.setAdeckSource.yearMasks: ',yearMasks

            else:

                # -- trackers org by NNB.YYYY as with mftrkN
                #    go back one year for SHEM storms
                #
                yearsAD=[mf.yyyyinc(year,-1),year]
                
                for yearAD in yearsAD:
                    
                    filemask="tctrk.atcf.??????????.*.*.%s"%(year)
                    if(useAdeckDir):
                        admask="%s/%s/??????????/%s"%(ad.bdir,yearAD,filemask)
                    elif(usePtmpDir):
                        admask="%s/%s"%(ad.bdir,filemask)
                        ad.dozip=0 # turn off zip...
                    else:
                        admask="%s/%s??????/*/%s"%(ad.bdir,yearAD,filemask)
            
                    ad.admasks.append(admask)
                    ad.filemasks.append(filemask)
                    print "III(adCL.setAdeckSource.yearsAD): ",year,admask,filemask

            source=osource
                
            if(verb): print 'SSSSSS setAdeckSources.smask(tmtrkN): ',ad.admasks

        elif(source == 'local'):
            osource=source
            
            bdir="%s/adeck/local/%s"%(TcDataBdir,year)
            ad=AdeckSource(source=source,
                           year=year,
                           dirname=source,
                           bdir=bdir,
                           sdir=bdir,
                           stype=source,
                           )
            ad.bdir=bdir
            smask="%s/wxmap.*%s*"%(ad.bdir,ad.year)
            source=osource
                
            print 'SSSSSS setAdeckSources.smask(local): ',smask
            ad.admasks=[smask]

        elif(source == 'cfsrr'):

            bdir="%s/adeck/esrl/%s"%(TcDataBdir,source)
            ad=AdeckSource(source=source,
                           year=year,
                           dirname=source,
                           bdir=bdir,
                           sdir=bdir,
                           stype=source,
                           )
            
            smask="%s/track.%s*"%(ad.bdir,ad.year)
                
            print 'SSSSSS setAdeckSources.smask: ',smask
            ad.admasks=[smask]

            aliases={}
            aliases['cont']='cfsrrctrl'

        elif(source == 'rap'):

            bdir="%s/adeck/esrl/%s"%(TcDataBdir,source)
            ad=AdeckSource(source=source,
                           year=year,
                           dirname=source,
                           bdir=bdir,
                           sdir=bdir,
                           stype=source,
                           )
            
            smask="%s/tctrk.atcf.%s*.*.*.txt"%(ad.bdir,ad.year)

            print 'SSSSSS setAdeckSources.smask: ',smask
            ad.admasks=[smask]

            aliases={}
            #aliases['cont']='cfsrrctrl'

        elif(source == '3emn'):

            bdir='/w21/prj/tc/ncep_3emn_20110412'
            ad=AdeckSource(source=source,
                           year=year,
                           dirname=source,
                           bdir=bdir,
                           sdir=bdir,
                           stype=source,
                           )
            
            smask="%s/adeck*%s*.txt"%(ad.bdir,ad.year)
                
            print 'SSSSSS setAdeckSources.smask: ',smask
            ad.admasks=[smask]

            aliases={}
            aliases['3emn']='3emn'

        elif(source == 'carq'
             ):

            sourcedir='.'
            bdir="%s/adeck/%s"%(TcDataBdir,year)
            ad=AdeckSource(source=source,
                           year=year,
                           dirname=sourcedir,
                           bdir=bdir,
                           sdir=bdir,
                           stype=source,
                           )
            smask="%s/adeck.local.jtwc.*txt"%(ad.bdir)
            if(self.verb): print 'AdeckSources.setAdeckSource.smask: ',smask
            ad.admasks=[smask]
            self.skipcarq=0

        elif(source == 'rtfim'
             or source == 'rtfimx'
             or source == 'rtfimy'
             or source == 'rtfimz'
             or source == 'rtfim7'
             or source == 'rtfim9'
             or source == 'rtfimz9'
             or source == 'rtfimz_retro'
             or source == 'rtfimz_r1094'
             or source == 'rtfimR925w2flds'
             or source == 'rtfimz_r1163'
             or source == 'rtfim_r1174'
             or source == 'rtfim_r1094b'
             or source == 'rtfim_r1231'
             or source == 'rtfim_r1273'
             or source == 'rtfim_r1273enkf'
             or source == 'rtfim_r1273a'
             or source == 'rtfim_r1291g7'
             or source == 'rtfim_r1359enkf'
             or source == 'rtfim_r1411enkf'
             or source == 'rtfim_r1422enkf'
             or source == 'rtfim_r1422gfs'
             or source == 'rtfim_r1422gfsG7'
             or source == 'rtfim_r1422gfsG7L38'
             
             or source == 'rtfim_r1607gfsG7'
             or source == 'rtfim_r1607gfsG7cugd'
             or source == 'rtfim_r1607gfsG7cutneg'
             
             or source == 'rtfim_r1831plm1'
             or source == 'rtfim_r1831gfsg8'
             or source == 'rtfim_r1831plm1vdif05'
             or source == 'rtfim_r1831plm1vdif10'

             or source == 'rtfim_r1926'
             or source == 'rtfim_r1926phys1d'
             or source == 'rtfim_r2159intfc500'
             or source == 'rtfim_r2176sigma'
             or source == 'rtfim_r2093phys1dsig'
             or source == 'rtfim_r2220intfc150g9'
             or source == 'rtfim_r2220intfc150'
             or source == 'rtfim_r2371hyb'
             or source == 'rtfim_r2371vdiff'
             or source == 'rtfim_r2647jpgf'
             or source == 'rtfim9_esrlDAhyb'
             or source == 'rtfim_r2972_j0'
             or source == 'rtfim_r2972_j1'
             or source == 'rtfim_r2972_j2'
             or source == 'rtfim_r2972_j0rd3'
             or source == 'rtfim_r2972_j1rd3'
             or source == 'rtfim_r2972_j2rd3'
             or source == 'rtfim_r2972_j0ifs50'
             or source == 'rtfim_r3162_g9ops'
             or source == 'rtfim_r3162_g9'
             or source == 'rtfim_r3162_g9hyb'
             or source == 'rtfim_r3585_v3'
             or source == 'rtfim_r3585_v4'
             or source == 'rtfim_r4109ops'
             or source == 'rtfim_r4109'   # hfip 2014 model
             or source == 'rtfim_r4314'   # FIM9 new interp run on zeus
             ):

            sourcedir=source
            if(source == 'rtfimR925w2flds'): sourcedir='rtfimR925'
            bdir="%s/adeck/esrl/%s/w2flds"%(TcDataBdir,year)
            
            
            ad=AdeckSource(source=source,
                           year=year,
                           dirname=sourcedir,
                           bdir=bdir,
                           sdir=bdir,
                           stype=source,
                           )
            smask="%s/tctrk.atcf.%s*.%s.txt"%(ad.bdir,ad.year,sourcedir)
            if(self.verb): print 'AdeckSources.setAdeckSource.smask: ',smask
            ad.admasks=[smask]

            if(dojettrack):
                
                # -- need to do import here to not crash with earlier TDw2.py
                #
                from FM import rtfimRuns,lrootLocal
                dortfim=1
                rt=rtfimRuns()
                rt.getRmodel(source)
                bdir="%s/dat/%s"%(lrootLocal,rt.fimrun)
                if(not(dortfim)): bdir="%s/adeck/esrl/%s/%s"%(TcDataBdir,year,source)
                
                if(
                    source == 'rtfim9' or
                    source == 'rtfim7' or
                    source == 'rtfimx' or
                    source == 'rtfim'
                   ): bdir="%s/adeck/esrl/%s/%s"%(TcDataBdir,year,source)

                if(source == 'rtfim_r2220intfc150g9'):   bdir="%s/adeck/esrl/tmp/fim_9_64_800_%s*/tracker_C/168/"%(TcDataBdir,year)
                if(source == 'rtfim_r2371hyb'):          bdir="%s/adeck/esrl/retro/FIMRETRO2371_HYB/fim_8_64_240_%s*/tracker_C/120/"%(TcDataBdir,year)
                if(source == 'rtfim_r2371vdiff'):        bdir="%s/adeck/esrl/retro/FIMRETRO2371_VDIFF/fim_8_64_240_%s*/tracker_C/120/"%(TcDataBdir,year)
                if(source == 'rtfim_r2647jpgf'):         bdir="%s/adeck/esrl/retro/FIMRETRO_janjic_pgf"%(TcDataBdir)
                if(source == 'rtfim9_esrlDAhyb'):        bdir="%s/adeck/esrl/retro/FIM9_ESRL_DA_HYB"%(TcDataBdir)
                if(source == 'rtfim_r2972_j0'):          bdir="%s/adeck/esrl/retro/FIMRETRO_r2972_jan0"%(TcDataBdir)
                if(source == 'rtfim_r2972_j1'):          bdir="%s/adeck/esrl/retro/FIMRETRO_r2972_jan1"%(TcDataBdir)
                if(source == 'rtfim_r2972_j2'):          bdir="%s/adeck/esrl/retro/FIMRETRO_r2972_jan2"%(TcDataBdir)
                if(source == 'rtfim_r2972_j0rd3'):       bdir="%s/adeck/esrl/retro/FIMRETRO_r2972_jan0_RED_DIFF3"%(TcDataBdir)
                if(source == 'rtfim_r2972_j1rd3'):       bdir="%s/adeck/esrl/retro/FIMRETRO_r2972_jan1_RED_DIFF3"%(TcDataBdir)
                if(source == 'rtfim_r2972_j2rd3'):       bdir="%s/adeck/esrl/retro/FIMRETRO_r2972_jan2_RED_DIFF3"%(TcDataBdir)
                if(source == 'rtfim_r2972_j0ifs50'):     bdir="%s/adeck/esrl/retro/FIMRETRO_r2972_jan0_intsm50"%(TcDataBdir)
                if(source == 'rtfim_r3162_g9ops'):       bdir="%s/adeck/esrl/retro/FIMRETRO_r3162_g9_ops"%(TcDataBdir)  # using operational gfs 
                if(source == 'rtfim_r3162_g9'):          bdir="%s/adeck/esrl/retro/FIMRETRO_r3162_g9_new"%(TcDataBdir)  # using hybrid DA 2012; ersl-enkf enkf/hybrid 2010-11
                if(source == 'rtfim_r3162_g9hyb'):       bdir="%s/adeck/esrl/retro/FIMRETRO_r3162_g9_V_hyb"%(TcDataBdir) # using ncep hybrid DA 2010-12 - same as used by hrwf retros for hfip 2013
                # control for comp against 201205 gfs phys
                if(source == 'rtfim_r3585_v3'):          bdir="%s/adeck/esrl/retro/FIMRETRO_r3585_v3"%(TcDataBdir)  
                # control for comp against 201205 gfs phys
                if(source == 'rtfim_r3585_v4'):          bdir="%s/adeck/esrl/retro/FIMRETRO_r3585_v4"%(TcDataBdir)  
                if(source == 'rtfim_r4109ops'):          bdir="%s/adeck/esrl/retro/FIM9RETRO_HFIP"%(TcDataBdir)  
                if(source == 'rtfim_r4109'):             bdir="%s/adeck/esrl/retro/FIM9RETRO_HFIP_2014"%(TcDataBdir)  
                if(source == 'rtfim_r4314'):             bdir="%s/adeck/esrl/retro/FIM9RETRO_new_interp"%(TcDataBdir)  



                ad=AdeckSource(source=source,
                               year=year,
                               dirname=sourcedir,
                               bdir=bdir,
                               sdir=bdir,
                               stype=source,
                           )

                smask="%s/%s??????/track*"%(ad.bdir,ad.year)
                smask="%s/track.%s*"%(ad.bdir,ad.year)

                if(source == 'rtfim_r2220intfc150g9'
                   or source == 'rtfim_r2371hyb'
                   or source == 'rtfim_r2371vdiff'
                   or source == 'rtfim_r2647jpgf'
                   or source == 'rtfim9_esrlDAhyb'
                   ): smask="%s/track*%s*"%(ad.bdir,ad.year)

                if(source == 'rtfim_r3585_v3'):   smask="%s/track*%s*v3"%(ad.bdir,ad.year)
                if(source == 'rtfim_r3585_v4'):   smask="%s/track*%s*v4"%(ad.bdir,ad.year)
                if(mf.find(source,'r4109')):      smask="%s/track.*%s*"%(ad.bdir,ad.year)
                if(mf.find(source,'r4314')):      smask="%s/track.*%s*"%(ad.bdir,ad.year)

                if(not(dortfim)): smask="%s/track*"%(ad.bdir)
                if(self.verb): print 'dojettrack.AdeckSources.setAdeckSource.smask: ',smask
                ad.admasks=[smask]
                print ad.admasks

        elif(source == 'lgem'
             ):

            sourcedir=source
            if(source == 'rtfimR925w2flds'): sourcedir='rtfimR925'
            
            bdir="%s/adeck/esrl/%s/w2flds"%(TcDataBdir,year)
            bdir="/dat3/tc/tcanal"
            ad=AdeckSource(source=source,
                           year=year,
                           dirname=sourcedir,
                           bdir=bdir,
                           sdir=bdir,
                           stype=source,
                           )
            smask="%s/%s??????/*/ships.adk.*.txt"%(ad.bdir,ad.year)
            if(self.verb): print 'AdeckSources.setAdeckSource.smask: ',smask
            ad.admasks=[smask]

        elif(source == 'rtfimR925'):
        
            # -- data archived to fw drive
            #
            bdir='/FWV2/dat2/nwp2/rtfim'
            ad=AdeckSource(source=source,
                           year=year,
                           bdir=bdir,
                           dirname='FIM_retro_r925',
                           stype='rtfim',
                           )

        elif(source == 'gfs_para_2010'):
            bdir='/w21/dat/tc/adeck/ncep/gfs_para_2010'
            ad=AdeckSource(source=source,
                           year=year,
                           bdir=bdir,
                           sdir=bdir,
                           dirname='.',
                           )
            smask="%s/atcfunix.gfs.%s*"%(ad.bdir,ad.year)
            ad.admasks=[smask]

        elif(source == 'gfs_t574_2010'):
            bdir='/w21/dat/tc/adeck/ncep/gfs_t574_2010'
            ad=AdeckSource(source=source,
                           year=year,
                           bdir=bdir,
                           sdir=bdir,
                           dirname='.',
                           )
            smask="%s/atcfunix.gfs.%s??????"%(ad.bdir,ad.year)
            ad.admasks=[smask]

            aliases={}
            aliases['pre1']='gfs2010'
            
        elif(source == 'nrl_cotc'):
            bdir='/w21/dat/tc/adeck/nrl'
            ad=AdeckSource(source=source,
                           year=year,
                           bdir=bdir,
                           sdir=bdir,
                           dirname='.',
                           )
            smask="%s/%s/a????%s.dat"%(ad.bdir,ad.year,ad.year)
            ad.admasks=[smask]

            aliases={}
            aliases['cotc']='cotn'

        # -- trackers from ecmwf bufr
        #
        elif(source == 'ecbufr'
             ):

            dozip=1
            if(not(useZipArchive)): dozip=0
            bdir="%s/adeck/ecmwf/%s/%s"%(TcDataBdir,year,source)

            ad=AdeckSource(source=source,
                           year=year,
                           bdir=bdir,
                           sdir=bdir,
                           stype=source,
                           dozip=dozip,
                           ZIPoverride=ZIPoverride,
                           )
            smask="%s/msl_*%s*"%(ad.bdir,ad.year)
            smask="%s/adeck.*%s*"%(ad.bdir,ad.year)
            if(self.verb): print 'AdeckSources.setAdeckSource.smask: ',smask

            ad.admasks=[]
            ad.filemasks=[]

            if(dtgopt != None):
                dtgs=mf.dtg_dtgopt_prc(dtgopt)
                for dtg in dtgs:
                    filemask="adeck.*%s*"%(dtg)
                    ad.admasks.append("%s/%s"%(ad.bdir,filemask))
                    ad.filemasks.append(filemask)
                    print 'SSSSSSSSSSSSS(ectrkN): ',filemask
                

            else:
                filemask="adeck.*%s*"%(ad.year)
                ad.admasks.append("%s/%s"%(ad.bdir,filemask))
                ad.filemasks.append(filemask)
                print 'SSSSSSSSSSSSS(ectrkN): ',filemask




        # -- new ecmwf trackers from fernando
        #
        elif(source == 'ectrkN'
             ):

            bdir="%s/adeck/ecmwf/%s/%s"%(TcDataBdir,year,source)
            ad=AdeckSource(source=source,
                           year=year,
                           bdir=bdir,
                           sdir=bdir,
                           stype=source,
                           )
            smask="%s/adeck.ecmwf.tcbufr.%s*txt"%(ad.bdir,ad.year)
            print 'SSSSSSSSSSSSS(ectrkN): ',smask
            if(self.verb): print 'AdeckSources.setAdeckSource.smask: ',smask
            ad.admasks=[smask]

        # -- trackers from hfip stream 1.5
        #
        elif(source == 'hfip'
             ):

            bdir="%s/adeck/hfip/%s"%(TcDataBdir,year)
            ad=AdeckSource(source=source,
                           year=year,
                           bdir=bdir,
                           sdir=bdir,
                           stype=source,
                           )
            smask="%s/a*%s*.dat"%(ad.bdir,ad.year)
            if(self.verb): print 'AdeckSources.setAdeckSource.smask: ',smask
            ad.admasks=[smask]

        # -- chips trackers from mit
        #
        elif(source == 'mit'
             ):

            bdir="%s/%s"%(TcAdecksMitDir,year)
            ad=AdeckSource(source=source,
                           year=year,
                           bdir=bdir,
                           sdir=bdir,
                           stype=source,
                           )
            smask="%s/*%s*.xfer"%(ad.bdir,ad.year)
            print 'SSSSSSSSSSSSS ',source,smask
            if(self.verb): print 'AdeckSources.setAdeckSource.smask: ',smask
            ad.admasks=[smask]


        # -- 2012 ncep gfs || runs of enkf-gsi hybrid
        #    prd12q3h -- no relocation
        #
        #
        elif(source == 'prd12q3h' or source == 'prd12q3i' 
             ):

            bdir="%s/adeck/ncep/%s_atcf"%(TcDataBdir,source)
            ad=AdeckSource(source=source,
                           year=year,
                           bdir=bdir,
                           sdir=bdir,
                           stype=source,
                           )
            smask="%s/atcfunix.gfs.%s*"%(ad.bdir,ad.year)
            print 'SSSSSSSSSSSSS ',source,smask
            if(self.verb): print 'AdeckSources.setAdeckSource.smask: ',smask
            ad.admasks=[smask]


        # -- 2013 hfip retro 2010-12 of avn using 2012 hybrid-DA
        #
        elif(source == 'prd1h2013'
             ):

            bdir="%s/adeck/esrl/retro/ncep_hfip2013"%(TcDataBdir)
            ad=AdeckSource(source=source,
                           year=year,
                           bdir=bdir,
                           sdir=bdir,
                           stype=source,
                           )
            smask="%s/avn.%s*.trackatcfunix"%(ad.bdir,ad.year)
            print 'SSSSSSSSSSSSS-hfip2013 ',source,smask
            if(self.verb): print 'AdeckSources.setAdeckSource.smask: ',smask
            ad.admasks=[smask]


        # -- fim + gfs enkf ensemble (fimens) 2011
        #
        elif(source == 'fimens' or source == 'fimens2' or source == 'fimens3'  
             ):

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
                    if(verb): print 'III already updated: ',fimadeck,cards[0][0:50]
                    return

                for ocard in cards:
                    ncard=ocard.replace(oaid,naid)
                    newadeck.append(ncard)

                MF.WriteList2File(newadeck,fimadeck)

            
            bdir="%s/adeck/esrl/%s/gfsenkf"%(TcDataBdir,year)
            ad=AdeckSource(source=source,
                           year=year,
                           dirname=source,
                           bdir=bdir,
                           sdir=bdir,
                           stype=source,
                           )

            smask1="%s/%s??????/track.*%s*.FIM??"%(ad.bdir,ad.year,ad.year)
            smask2="%s/%s??????/track.*%s*.GE0[1-9]"%(ad.bdir,ad.year,ad.year)
            smask3="%s/%s??????//track.*%s*.GE1[0-1]"%(ad.bdir,ad.year,ad.year)
            smask4=None
            
            if(source == 'fimens2'):
                smask2="%s/%s??????//track.*%s*.GE1[1-9]"%(ad.bdir,ad.year,ad.year)
                smask3="%s/%s??????//track.*%s*.GE2[0-1]"%(ad.bdir,ad.year,ad.year)

            if(source == 'fimens3'):
                smask2="%s/%s??????//track.*%s*.GE0[1-9]"%(ad.bdir,ad.year,ad.year)
                smask3="%s/%s??????//track.*%s*.GE1[0-9]"%(ad.bdir,ad.year,ad.year)
                smask4="%s/%s??????//track.*%s*.GE2[0-1]"%(ad.bdir,ad.year,ad.year)
                

            # -- first fix aid name in fimens adecks
            #
            
            fimensAdecks=glob.glob(smask1)
            
            for fimadeck in fimensAdecks:
                fixFimensAidName(fimadeck)


            print 'SSSSSSSSSSSSS ',source,smask1,smask2,smask3
            if(self.verb): print 'AdeckSources.setAdeckSource.smask: ',smask
            ad.admasks=[smask1,smask2,smask3]
            if(smask4 != None):
                ad.admasks.append(smask4)

        # -- 2012 hfip gfsenkf
        #
        elif(source == 'gfsenkf2012' or source == 'gfsenkf2013'):

            dozip=1
            bdir="%s/adeck/esrl/%s/gfsenkf"%(TcDataBdir,year)
            ad=AdeckSource(source=source,
                           year=year,
                           dirname=source,
                           bdir=bdir,
                           sdir=bdir,
                           stype=source,
                           dozip=dozip,
                           ZIPoverride=ZIPoverride,
                           )
            ad.admasks=[]
            ad.filemasks=[]

            filemask="track.*%s*.GE??"%(ad.year)
            admask="%s/%s??????/%s"%(ad.bdir,ad.year,filemask)

            ad.admasks.append(admask)
            ad.filemasks.append(filemask)

            if(self.verb): print 'AdeckSources.setAdeckSource.admask(%s): %s'%(source,admask)

        # -- fim9 hfip 2013 
        #
        elif(source == 'fim9hfip2013' or source == 'fim9hfip2014'):

            dozip=0
            if(source == 'fim9hfip2013'): bdir="/ptmp/hfip2013"
            if(source == 'fim9hfip2014'): bdir="/ptmp/hfip2014"
            ad=AdeckSource(source=source,
                           year=year,
                           dirname=source,
                           bdir=bdir,
                           sdir=bdir,
                           stype=source,
                           dozip=dozip,
                           ZIPoverride=ZIPoverride,
                           )
            ad.admasks=[]
            ad.filemasks=[]

            filemask="a????%s_*"%(ad.year)
            admask="%s/%s"%(ad.bdir,filemask)

            ad.admasks.append(admask)
            ad.filemasks.append(filemask)

            if(self.verb): print 'AdeckSources.setAdeckSource.admask(%s): %s'%(source,admask)


        # -- 2012 hfip gfsenkf
        #
        elif(source == 'fimensg7'):

            dozip=1
            bdir="%s/adeck/esrl/%s/fimens/"%(TcDataBdir,year)
            ad=AdeckSource(source=source,
                           year=year,
                           dirname=source,
                           bdir=bdir,
                           sdir=bdir,
                           stype=source,
                           dozip=dozip,
                           ZIPoverride=ZIPoverride,
                           )
            ad.admasks=[]
            ad.filemasks=[]

            filemask="track.*%s*.FE??"%(ad.year)
            admask="%s/%s??????/%s"%(ad.bdir,ad.year,filemask)

            ad.admasks.append(admask)
            ad.filemasks.append(filemask)

            if(self.verb): print 'AdeckSources.setAdeckSource.admask(%s): %s'%(source,admask)

        elif(source == 'fimens2012'):

            tdtgs=None
            if(dtgopt != None):
                tdtgs=mf.dtg_dtgopt_prc(dtgopt)

            tbdir='/mnt/lfs2/projects/fim/fiorino/w21/dat/tc/adeck/esrl/2012/fimens/'
            MF.ChkDir(tbdir,'mk')
            
            def fixFimensAidName(fimadeck,dtg,verb=0,chk=self.dochk):

                newadeck=[]

                (sdir,file)=os.path.split(fimadeck)
                tdir='%s/%s'%(tbdir,dtg)
                MF.ChkDir(tdir,'mk')

                member=int(fimadeck[-2:])
                oaids=['F800','F801']
                naid='FE%02d'%(member)

                (base,ext)=os.path.splitext(file)
                ofimadeck="%s/%s.%s"%(tdir,base[0:-2],naid)
                
                cards=open(fimadeck).readlines()
                if(len(cards) == 0): return

                # -- don't do if already done
                done=0
                for oaid in oaids:
                    if(not(mf.find(cards[0],oaid)) and chk):
                        if(verb): print 'III already updated: ',fimadeck,cards[0][0:50]
                        done=1

                for ocard in cards:
                    ncard=ocard
                    for oaid in oaids:
                        ncard=ncard.replace(oaid,naid)
                    newadeck.append(ncard)

                if(done  == 0):  newadeck=cards
                
                if(verb): print 'WWW ',fimadeck,ofimadeck
                MF.WriteList2File(newadeck,ofimadeck,verb=0)

            
            # get  latest tau
            #
            bdirs=[]
            bdir="/pan2/projects/fim-njet/FIMENS/FIMrun/fim_8_64_240_%s*/tracker_*/??"%(year)
            bdir="/pan2/projects/fim-njet/FIMENS/FIMrun/fim_7_64_190_%s*/tracker_*/??"%(year)
            #bdirs=glob.glob(bdir)
            bdir="/pan2/projects/fim-njet/FIMENS/FIMrun/fim_8_64_240_%s*/tracker_*/???"%(year)
            bdir="/pan2/projects/fim-njet/FIMENS/FIMrun/fim_7_64_190_%s*/tracker_*/???"%(year)
            bdir="/pan2/projects/fim-njet/FIMENS_sjet/FIMrun/fim_7_64_144_%s*/tracker_*/???"%(year)
            
            # -- only one active
            #
            bdir="/pan2/projects/fim-njet/FIMENS_sjet/FIMrun/fim_8_64_144_%s*/tracker_*/???"%(year)
            bdirs=bdirs+glob.glob(bdir)
            
            members=[]
            dtgs={}
            latestbdirs={}
            for bdir in bdirs:
                tt=bdir.split('/')
                dtg=tt[-3][-12:-2]
                member=tt[-2][-2:]
                members.append(member)
                tau=tt[-1]
                MF.appendDictList(dtgs,member,dtg)
                key="%s_%s"%(dtg,member)
                latestbdirs[key]=bdir


            ad=AdeckSource(source=source,
                           year=year,
                           dirname=source,
                           bdir=bdir,
                           sdir=bdir,
                           stype=source,
                           )


            ad.admasks=[]

            members=mf.uniq(members)

            for member in members:
                mdtgs=dtgs[member]
                mdtgs=mf.uniq(mdtgs)

                for mdtg in mdtgs:

                    if(tdtgs != None and not(mdtg in tdtgs)): continue

                    try:
                        bdir=latestbdirs["%s_%s"%(mdtg,member)]
                    except:
                        bdir=None

                    if(bdir != None):

                        smask="%s/track.*%s*.F*"%(bdir,ad.year)
                        fimensAdecks=glob.glob(smask)

                        for fimadeck in fimensAdecks:
                            fixFimensAidName(fimadeck,mdtg,chk=self.dochk,verb=0)
            
            smask1="%s/%s??????/track.*%s*.FE*"%(tbdir,ad.year,ad.year)

            print 'SSS(fimens2012) ',source,smask1
            if(self.verb): print 'AdeckSources.setAdeckSource.smask: ',smask
            ad.admasks=[smask1]


        # for jet processing
        #
        elif(source == 'fim9hfip'):

            tdtgs=None
            if(dtgopt != None):
                tdtgs=mf.dtg_dtgopt_prc(dtgopt)

            tbdir='/mnt/lfs2/projects/fim/fiorino/w21/dat/tc/adeck/esrl/2012/fim9hfip'
            MF.ChkDir(tbdir,'mk')
            
            def fixFimensAidName(fimadeck,dtg,verb=0,chk=self.dochk):

                newadeck=[]

                (sdir,file)=os.path.split(fimadeck)
                tdir='%s/%s'%(tbdir,dtg)
                MF.ChkDir(tdir,'mk')

                oaids=['F9C']
                naid='FIM9'

                (base,ext)=os.path.splitext(file)
                ofimadeck="%s/%s.%s"%(tdir,base[0:-2],naid)
                
                cards=open(fimadeck).readlines()

                # -- don't do if already done
                done=0
                for oaid in oaids:
                    if(not(mf.find(cards[0],oaid)) and chk):
                        if(verb): print 'III already updated: ',fimadeck,cards[0][0:50]
                        done=1

                for ocard in cards:
                    ncard=ocard
                    for oaid in oaids:
                        ncard=ncard.replace(oaid,naid)
                    newadeck.append(ncard)

                if(done): newadeck=cards
                
                if(verb): print 'WWW ',fimadeck,ofimadeck
                MF.WriteList2File(newadeck,ofimadeck,verb=0)

            
            # get  latest tau
            #
            bdir="/pan2/projects/fim-njet/FIM9/FIMrun/fim_9_64_1200_%s*/tracker_C/??"%(year)
            bdirs=glob.glob(bdir)
            bdir="/pan2/projects/fim-njet/FIM9/FIMrun/fim_9_64_1200_%s*/tracker_C/???"%(year)
            bdirs=bdirs+glob.glob(bdir)
            dtgs={}
            latestbdirs={}
            for bdir in bdirs:
                tt=bdir.split('/')
                dtg=tt[-3][-12:-2]
                tau=tt[-1]
                key="%s"%(dtg)
                latestbdirs[key]=bdir


            ad=AdeckSource(source=source,
                           year=year,
                           dirname=source,
                           bdir=bdir,
                           sdir=bdir,
                           stype=source,
                           )


            ad.admasks=[]
            mdtgs=latestbdirs.keys()
            mdtgs.sort()

            for mdtg in mdtgs:

                if(tdtgs != None and not(mdtg in tdtgs)): continue
                    
                try:
                    bdir=latestbdirs["%s"%(mdtg)]
                except:
                    bdir=None

                if(bdir != None):

                    smask="%s/track.*%s*.F*"%(bdir,ad.year)
                    fimensAdecks=glob.glob(smask)
            
                    for fimadeck in fimensAdecks:
                        fixFimensAidName(fimadeck,mdtg,chk=self.dochk,verb=0)
            
            smask1="%s/%s??????/track.*%s*.F*"%(tbdir,ad.year,ad.year)

            print 'SSS(fim9hfip) ',source,smask1
            if(self.verb): print 'AdeckSources.setAdeckSource.smask: ',smask
            ad.admasks=[smask1]


        # -- 2013 hfip retro 2010-12 of avn using 2012 hybrid-DA
        #
        elif(source == 'tcvcip'
             ):

            bdir="%s/%s"%(TcDataBdir,source)
            ad=AdeckSource(source=source,
                           year=year,
                           bdir=bdir,
                           sdir=bdir,
                           stype=source,
                           )
            smask="%s/a??%s.dat"%(ad.bdir,ad.year)
            print 'SSSSSSSSSSSSS-TCVCIP ',source,smask
            if(self.verb): print 'AdeckSources.setAdeckSource.smask: ',smask
            ad.admasks=[smask]

        # -- alaises
        #
        if(ad == None):
            print '!!!!'
            print 'EEEE adCL.AdeckSources.setAdeckSource: invalid source: ',source
            print '!!!!'
            sys.exit()


            
        aliases={}
        if(source == 'rtfim'):
            aliases['rt8c']='fim8'
            aliases['f8c']='fim8'
            aliases['rtfi']='fim8'

        elif(source == 'rtfimx'):
            aliases['rtfi']='f8cx'
            aliases['f8c']='fimx'
            aliases['f7c']='fimx'

        elif(source == 'rtfimy'):
            aliases['rtfi']='f8cy'

        elif(source == 'jet_rtfim'):
            aliases['f8c']='jf8c'

        elif(source == 'jet_rtfimx'):
            aliases['f7c']='jf7cx'

        elif(source == 'jet_rtfimz'):
            aliases['f8c']='jf8cz'

        elif(source == 'jet_rtfimy'):
            aliases['f8c']='jf8cy'

        elif(source == 'local'):
            aliases['ncm2']='lcmc2'
            aliases['nec2']='lecm2'
            aliases['fim8']='lfim8'
            aliases['f8cy']='lfimy'
            aliases['ngf2']='lgfs2'
            aliases['nngc']='lngpc'
            aliases['nng2']='lngp2'
            aliases['nuk2']='lukm2'

        # -- coordinate with atcf.py
        elif(source == 'mftrkN' or source == 'mftrk'):
            aliases['fimx']='mfimx'
            aliases['fim7']='mfim7'
            aliases['fim8']='mfim8'
            aliases['fim9']='mfim9'
            aliases['f8c'] ='mf8c'
            aliases['f8cy']='mf8cy'
            aliases['ncm2']='mcmc2'
            aliases['ecm4']='mecm4'
            aliases['nec2']='mecm2'
            aliases['ngf2']='mgfs2'
            aliases['nng2']='mngp2'
            aliases['nnnn']='mngpj'
            aliases['emx'] ='mecmn'
            aliases['nngc']='mngpc'
            aliases['navg']='mnavg'
            aliases['nuk2']='mukm2'
            aliases['nukc']='mukmc'
            aliases['necn']='mecmn'
            aliases['ecmt']='mecmt'
            aliases['cgd6']='mcgd6'

        elif(source == 'tmtrkN'):
            aliases['fim7']='tfim7'
            aliases['tfim']='tfim8'
            aliases['fimx']='tfimx'
            aliases['fim8']='tfim8'
            aliases['fim9']='tfim9'
            aliases['f8c'] ='tf8c'
            aliases['rtfi']='tfim9'
            aliases['cmc2']='tcmc2'
            aliases['ecm4']='tecm4'
            aliases['ecm2']='tecm2'
            aliases['gfs2']='tgfs2'
            aliases['gfsc']='tgfsc'
            aliases['ngp2']='tngp2'
            aliases['ngpc']='tngpc'
            aliases['navg']='tnavg'
            aliases['ngpj']='tngpj'
            aliases['ukm2']='tukm2'
            aliases['ecmn']='tecmn'
            aliases['ecmt']='tecmt'
            aliases['cgd6']='tcgd6'

        elif(source == 'prd12q3h'):
            aliases['prd1']='prdh'

        elif(source == 'prd12q3i'):
            aliases['prd1']='prdi'

        elif(source == 'jet_rtfim7'):
            aliases['f7c']='jf7c'

        elif(source == 'rtfimz'):
            aliases['rtfi']='f8cz'

        elif(source == 'rtfim7'):
            aliases['rtfi']='fim7'
            aliases['f7c']='fim7'

        elif(source == 'rtfim9'):
            aliases['rtfi']='fim9'

        elif(source == 'rtfimz9'):
            aliases['rtfi']='f9cz'

        elif(source == 'rtfimR925'):
            aliases['f8c']='fr925'

        elif(source == 'rtfimz_retro' or source == 'rtfimz_r1094'):
            aliases['rtfi']='fzr1094'

        elif(source == 'rtfimz_r1163'):
            aliases['rtfi']='fzr1163'

        elif(source == 'rtfim_r1174'):
            aliases['rtfi']='fr1174'

        elif(source == 'rtfimR925w2flds'):
            aliases['rtfi']='fr925w2'

        elif(source == 'gfs_para_2010'):
            aliases['pru1']='gfs2010'

        elif(source == 'rtfim_r1094b'):
            aliases['rtfi']='fr1094b'

        elif(source == 'rtfim_r1231'):
            aliases['rtfi']='fr1231'

        elif(source == 'rtfim_r1273'):
            aliases['rtfi']='fr1273'

        elif(source == 'rtfim_r1273enkf'):
            aliases['rtfi']='fr1273enkf'

        elif(source == 'rtfim_r1273a'):
            aliases['rtfi']='fr1273a'

        elif(source == 'rtfim_r1291g7'):
            aliases['rtfi']='fr1291g7'

        elif(source == 'rtfim_r1359enkf'):
            aliases['rtfi']='fr1359enkf'

        elif(source == 'rtfim_r1422enkf'):
            aliases['rtfi']='fr1422enkf'

        elif(source == 'rtfim_r1422gfs'):
            aliases['rtfi']='fr1422gfs'

        elif(source == 'rtfim_r1422gfsG7L38'):
            aliases['rtfi']='fr1422gfsg7L38'

        elif(source == 'rtfim_r1422gfsG7'):
            if(dojettrack):
                aliases['f7c']='fr1422g7'
            else:
                aliases['rtfi']='fr1422g7'

        elif(source == 'rtfim_r1607gfsG7'):
            if(dojettrack):
                aliases['f7c']='fr1607g7'
            else:
                aliases['rtfi']='fr1607g7'

        elif(source == 'rtfim_r1607gfsG7cugd'):
            if(dojettrack):
                aliases['f7c']='fr1607g7cugd'
            else:
                aliases['rtfi']='fr1607g7cugd'
                
        elif(source == 'rtfim_r1607gfsG7cutneg'):
            aliases['rtfi']='fr1607g7cutneg'

        elif(source == 'rtfim_r1831plm1'):
            if(dojettrack):
                aliases['f8c']='fr1831plm1'
            else:
                aliases['rtfi']='fr1831plm1'

        elif(source == 'rtfim_r1831plm1vdif05'):
            if(dojettrack):
                aliases['f8c']='fr1831plm1vd05'
            else:
                aliases['rtfi']='fr1831plm1vd05'

        elif(source == 'rtfim_r1831plm1vdif10'):
            if(dojettrack):
                aliases['f8c']='fr1831plm1vd10'
            else:
                aliases['rtfi']='fr1831plm1vd10'

        elif(source == 'rtfim_r1831gfsg8'):
            if(dojettrack):
                aliases['f8c']='fr1831gfsg8'
            else:
                aliases['rtfi']='fr1831gfsg8'

        elif(source == 'rtfim_r1926'):
            if(dojettrack):
                aliases['f8c']='fr1926'
            else:
                aliases['rtfi']='fr1926'

        elif(source == 'rtfim_r1926phys1d'):
            if(dojettrack):
                aliases['f8c']='fr19261d'
            else:
                aliases['rtfi']='fr19261d'

        elif(source == 'rtfim_r2159intfc500'):
            if(dojettrack):
                aliases['f8c']='fr2159int'
            else:
                aliases['rtfi']='fr2159int'

        elif(source == 'rtfim_r2176sigma'):
            if(dojettrack):
                aliases['f8c']='fr2176sig'
            else:
                aliases['rtfi']='fr2176sig'

        elif(source == 'rtfim_r2093phys1dsig'):
            if(dojettrack):
                aliases['f8c']='fr2093sig'
            else:
                aliases['rtfi']='fr2093sig'

        elif(source == 'rtfim_r2220intfc150g9'):
            if(dojettrack):
                aliases['f9c']='fr2220g9'
            else:
                aliases['rtfi']='fr2220g9'

        elif(source == 'rtfim_r2220intfc150'):
            if(dojettrack):
                aliases['f8c']='fr2220g8'
            else:
                aliases['rtfi']='fr2220g8'

        elif(source == 'rtfim_r2371hyb'):
            if(dojettrack):
                aliases['f8c']='fr2371hyb'
            else:
                aliases['rtfi']='fr2371hyb'

        elif(source == 'rtfim_r2371vdiff'):
            if(dojettrack):
                aliases['f8c']='fr2371vdiff'
            else:
                aliases['rtfi']='fr2371vdiff'

        elif(source == 'rtfim_r2647jpgf'):
            if(dojettrack):
                aliases['f8c']='fr2647jpgf'
            else:
                aliases['rtfi']='fr2647jpgf'

        elif(source == 'rtfim9_esrlDAhyb'):
            if(dojettrack):
                aliases['f9c']='fim9eda'
            else:
                aliases['rtfi']='fim9eda'

        elif(source == 'rtfim_r2972_j0'):
            if(dojettrack):
                aliases['f8c']='fr2972j0'

        elif(source == 'rtfim_r2972_j1'):
            if(dojettrack):
                aliases['f8c']='fr2972j1'

        elif(source == 'rtfim_r2972_j2'):
            if(dojettrack):
                aliases['f8c']='fr2972j2'

        elif(source == 'rtfim_r2972_j0rd3'):
            if(dojettrack):
                aliases['f8c']='fr2972j0rd3'

        elif(source == 'rtfim_r2972_j1rd3'):
            if(dojettrack):
                aliases['f8c']='fr2972j1rd3'

        elif(source == 'rtfim_r2972_j2rd3'):
            if(dojettrack):
                aliases['f8c']='fr2972j2rd3'

        elif(source == 'rtfim_r2972_j0ifs50'):
            if(dojettrack):
                aliases['f8c']='fr2972j0ifs50'

        elif(source == 'rtfim_r3162_g9ops'):
            if(dojettrack):
                aliases['f9c']='fr3162g9ops'

        elif(source == 'rtfim_r3162_g9'):
            if(dojettrack):
                aliases['f9c']='fr3162g9'

        elif(source == 'rtfim_r3162_g9hyb'):
            if(dojettrack):
                aliases['f9c']='fr3162g9hyb'

        elif(source == 'rtfim_r3585_v3'):
            if(dojettrack):
                aliases['fimr']='fr3585v3'

        elif(source == 'rtfim_r3585_v4'):
            if(dojettrack):
                aliases['fimr']='fr3585v4'

        elif(source == 'prd1h2013'):
            aliases['prd1']='avnh13'
            aliases['avno']='avnh13'


        return(ad,aliases)

    
            


#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc -- AdeckSource -- methods for get/put adecks including zip
#

class AdeckSource(MFbase):
    
    def __init__(self,
                 source='rtfimR925',
                 dirname='FIM_retro_R925',
                 stype='rtfim',
                 year='2009',
                 bdir=None,
                 sdir=None,
                 dozip=0,
                 verb=0,
                 ZIPoverride=0,
                 ropt=''
                 ):

        from tcbase import TcDataBdir

        self.source=source
        self.stype=stype
        if(bdir == None):  self.bdir="%s/nwp2/%s"%(W2BaseDirDat,self.stype)
        else:              self.bdir=bdir
        self.dirname=dirname
        if(sdir == None):  self.sdir="%s/dat/%s"%(self.bdir,self.dirname)
        else:              self.sdir=sdir
        self.year=year
        self.verb=verb
        self.dozip=dozip

        self.zdir="%s/archive"%(sdir)
        MF.ChkDir(self.zdir,'mk')

        tdirZIP='%s/ptmp/%s'%(TcDataBdir,self.source)
        MF.ChkDir(tdirZIP,'mk')
        self.tdirZIP=tdirZIP

        if(dozip):
            
            MF.sTimer('ad2.zipfile-zipinv')

            self.zippath="%s/%s.%s.zip"%(self.zdir,self.source,self.year)
            # -- new feature to kill zipfile
            if(ZIPoverride):
                try:
                    os.unlink(self.zippath)
                    print 'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW(AdeckSource.dozip=1) killing: ',self.zippath
                except:
                    print 'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW(AdeckSource.dozip=1) ',self.zippath,' not there....'
                
                # -- kill files in tdirZIP
                #
                cmd="rm -r %s"%(self.tdirZIP)
                mf.runcmd(cmd,ropt)
                MF.ChkDir(self.tdirZIP,'mk')
            
            try:
                self.AZ=zipfile.ZipFile(self.zippath,'a')
            except:
                self.AZ=zipfile.ZipFile(self.zippath,'w')

            self.zipinv={}

            for info in self.AZ.infolist():
                file=info.filename
                siz=info.file_size
                zdtg=info.date_time
                self.zipinv[file]=(siz,zdtg)

            MF.dTimer('ad2.zipfile-zipinv')


    def setAdmask(self,year=None,dtgopt=None):

        if(year == None): year=self.year
        curyear=mf.dtg()[0:4]
        smask='%s/%s??????/track.*'%(self.sdir,year)
        
        self.admasks=[
            smask,
            ]

    def getAdecks(self,source=None,year=None,tstmids=None,dtgopt=None,override=0):

        MF.sTimer('ad2-getAdecks-open')
        if(self.dozip):
            adecks=self.getAdecksZip(override=override,dtgopt=dtgopt)
            MF.dTimer('ad2-getAdecks-open')
            return(adecks)

        if(year == None): year=self.year
        if(not(hasattr(self,'admasks'))):  self.setAdmask(year)
        if(self.verb): print 'ad2.getAdecks.admasks: ',self.admasks,self.filemasks
        
        
        adecks=[]
        for admask in self.admasks:
            adecks=adecks+glob.glob(admask)

        oadecks=[]
        for adeck in adecks:
            try:
                siz=os.path.getsize(adeck)
                if(siz > 0):
                    oadecks.append(adeck)
                    if(self.verb): print 'ad2.AdeckSource.getAdecks(): ',adeck
            except:
                continue
            
        MF.dTimer('ad2-getAdecks-open')

        return(oadecks)

    def getAdecksZip(self,source=None,year=None,tstmids=None,dtgopt=None,override=0,
                     selectLatest=1,selectBiggest=0):

        if(year == None): year=self.year
        if(not(hasattr(self,'admasks'))):  self.setAdmask(year)
        
        self.verb=1
        if(self.verb): print 'ad2.getAdecks.admasks: ',self.admasks,self.filemasks

        MF.sTimer('ad2.getAdecksZip-adecks')
        adecks=[]

        self.verb=1
        import fnmatch
        files=self.zipinv.keys()
        files.sort()
        fdtgs=[]
        ffiles={}

        # -- first get the dtgs and the files for that dtg
        #
        for filemask in self.filemasks:
            for file in files:
                try:
                    fdtg=file.split('.')[3].split('_')[0]
                    (zsiz,zdtg)=self.zipinv[file]
                    zdtg="%04d%02d%02d%02d%02d"%(zdtg[0],zdtg[1],zdtg[2],zdtg[3],zdtg[4])
                except:
                    print 'AdeckSource.getAdecksZip bad file: ',file,' press...'
                    continue
                
                #print 'fffffffff',file,filemask,fdtg,fnmatch.fnmatch(file,filemask),zdtg,zsiz,self.zipinv[file],self.tdirZIP
                if(fnmatch.fnmatch(file,filemask)):
                    tpath="%s/%s"%(self.tdirZIP,file)
                    tsiz=MF.GetPathSiz(tpath)
                    if(tsiz == None or override):
                        fdtgs.append(fdtg)
                        MF.appendDictList(ffiles, fdtg, (file,tpath,zsiz,zdtg))
                    
        fdtgs=MF.uniq(fdtgs)
        
        # -- cycle through dtgs and find latest and biggest file
        #
        self.verb=0
        for fdtg in fdtgs:
            biggest=-999
            latest=-999
            for n in range(0,len(ffiles[fdtg])):
                fsiz=ffiles[fdtg][n][2]
                ftime=int(ffiles[fdtg][n][3]) - int(ffiles[fdtg][0][3])
                if(ftime > latest): 
                    latest=ftime
                    nlatest=n
                if(fsiz > biggest):
                    biggest=fsiz
                    nbiggest=n
                
                if(self.verb): print 'fff',fsiz,ftime,n,'tttt',latest,nlatest,'sss',biggest,nbiggest,'ffff: ',ffiles[fdtg][n]
            
            # -- select adecks based on time or siz
            #
            if(selectLatest):
                (ffile,tpath,fsiz,fdtg12)=ffiles[fdtg][nlatest]
            elif(selectBiggest):
                (ffile,tpath,fsiz,fdtg12)=ffiles[fdtg][nbiggest].w
                
            tsiz=MF.GetPathSiz(tpath)
            if(tsiz == None or override):
                try:
                    self.AZ.extract(ffile,self.tdirZIP)
                    tpath="%s/%s"%(self.tdirZIP,ffile)
                    if(self.verb): print 'gotit: ',ffile,self.zipinv[ffile],tsiz,tpath
                except:
                    print 'WWW AdeckSource.AZ.extract failed for: ',file
                    continue
                
                adecks.append(tpath)
                

        MF.dTimer('ad2.getAdecksZip-adecks')
        
        return(adecks)


    def putAdecks(self,adecks,override=0,zdtgdiffMin=0.1):

        MF.sTimer('ad2.putAdecks')
        for adeck in adecks:
            (dir,file)=os.path.split(adeck)
            siz=MF.GetPathSiz(adeck)

            (dtimei,ldtg,gdtg)=MF.PathModifyTime(adeck)

            # -- get the dtg of the file in the archive and replace if adeck newer
            #
            try:
                (zsiz,zdtg)=self.zipinv[file]
                zdtg="%04d%02d%02d%02d"%(zdtg[0],zdtg[1],zdtg[2],zdtg[3])
                zdtgdiff=MF.PathModifyTimeDtgdiff(zdtg,adeck)
            except:
                zsiz=-999
                zdtg=-999
                zdtgdiff=-999

            if(self.verb): print 'ad2.putAdecks() candidate file: ',file,'siz: ',siz,' zsiz: ',zsiz,' zdtg: ',zdtg,' zdtgdiff: ',zdtgdiff

            if(siz != zsiz or zsiz == -999 or override or zdtgdiff > zdtgdiffMin):
                print 'III ad2.putAdecks() file: ',file,'siz: ',siz,' zsiz: ',zsiz,' zdtg: ',zdtg,' zdtgdiff: ',zdtgdiff
                print 'III put adeck:',dir,file,'to ',self.zippath
                self.AZ.write(adeck,file,zipfile.ZIP_DEFLATED)
                #self.AZ.write(adeck,file)

        MF.dTimer('ad2.putAdecks')

        # -- do zipinv after putadecks
        #
        MF.sTimer('ad2.putAdecks-zipinv')
        self.zipinv={}

        for info in self.AZ.infolist():
            file=info.filename
            siz=info.file_size
            zdtg=info.date_time
            self.zipinv[file]=(siz,zdtg)
            
        MF.dTimer('ad2.putAdecks-zipinv')





#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc -- ADutils
#
class ADutils(MFutils):


    def Smth121(self,data,npass=0):

        nd=len(data)

        if(npass == 0):
            tdata=copy.deepcopy(data)
            return(tdata)

        odata=copy.deepcopy(data)
        tdata=copy.deepcopy(data)

        for n in range(0,npass+1):

            for i in range(0,nd):
                if(i == 0 or i == nd-1):
                    tdata[i]=odata[i]
                else:
                    tdata[i]=0.25*odata[i-1]+0.5*odata[i]+0.25*odata[i+1]

            for i in range(0,nd):
                odata[i]=tdata[i]

        return(tdata)




    def FcTrackInterpFill(self,itrk,dtx=3,npass=0,dovmaxSmth=0,verb=0,idtmax=6,doExtrap=1):

        """
----------------------------------------------------------------------
 routine to smooth input track in lat,lon
 doextrap -- extrap from last point using previous motion to add
 taus  -- similar to nhc_interp.f except done on INuPT to rumterp
----------------------------------------------------------------------
"""
        itaus=itrk.keys()
        itaus.sort()

        btau=itaus[0]

        deftrk={}
        mottrk={}

        jtrk={}

        #  -- check for extra vars
        #
        
        doextra1=0
        doextra2=0
        dor34s=0
        dor50s=0
        dor64s=0
        
        for tau in itaus:

            if(type(tau) is IntType and int(tau)%idtmax != 0): continue

            flat=itrk[tau][0]
            flon=itrk[tau][1]
            fvmax=itrk[tau][2]
            itrkLen=len(itrk[tau])
            
            try:
                fpmin=itrk[tau][3]
            except:
                fpmin=-9999.
                
            # -- detect new BT2 with dir,speed,'TC' and 'NW' in -2 and -1 position
            #
            if(itrkLen == 5):
                fextra1=itrk[tau][-2]
                if(fextra1 != None and not( ( (type(fextra1) is StringType) and len(fextra1) == 2 ) ) ): doextra1=1
            
            if(itrkLen == 6):
                fextra2=itrk[tau][-1]
                if(fextra2 != None and not( ( (type(fextra2) is StringType) and len(fextra2) == 2 ) ) ): doextra2=1
                
        for tau in itaus:

            # -- filter out non 6 h trackers -- hwrf now hoursly 0-9 h, otherwise 3-h
            #    assumed tau was an integer for check --- not true for BT which is DTG
            # -- only do check if int -- assumes dtg are always 6 h
            # -- 20190910 -- add exception 
            if(type(tau) is IntType and int(tau)%idtmax != 0): 
                print 'WWW-ADutils-FcTrackInterpFill -- skipping tau: ',tau
                continue

            flat=itrk[tau][0]
            flon=itrk[tau][1]
            fvmax=itrk[tau][2]
            itrkLen=len(itrk[tau])

            try:
                fvmax=itrk[tau][2]
            except:
                fvmax=-9999.
            if(fvmax == None or fvmax == 0.0): fvmax=-9999.
            
            
            try:
                fpmin=itrk[tau][3]
            except:
                fpmin=-9999.
            if(fpmin == None or fpmin == 0.0): fpmin=-9999.

            
            # -- if itrkLen == 7 then will deal is have the three radii
            #
            if(itrkLen == 7):
                try:
                    fr34s=itrk[tau][4]
                except:
                    fr34s=None
                    
                try:
                    fr50s=itrk[tau][5]
                except:
                    fr50s=None
                    
                try:
                    fr64s=itrk[tau][6]
                except:
                    fr64s=None
                    

            try:
                fextra1=itrk[tau][-2]
            except:
                fextra1=-9999.
                
            if(fextra1 == None): fextra1=-9999.

            try:
                fextra2=itrk[tau][-1]
            except:
                fextra2=-9999.
                
            if(fextra2 == None): fextra2=-9999.

            # -- bounds check on latitude
            #
            if(flat < 85.0 and flat > -85.0):
                
                deftrk[tau]=[flat,flon,fvmax,fpmin]
                
                if(doextra1):
                    deftrk[tau]=[flat,flon,fvmax,fpmin,fextra1]
                    
                if(doextra2):
                    deftrk[tau]=[flat,flon,fvmax,fpmin,fextra1,fextra2]
              
                # -- wind radii
                #
                if(itrkLen == 7):
                    deftrk[tau]=[flat,flon,fvmax,fpmin,fr34s,fr50s,fr64s]
                    
                    

        deftaus=deftrk.keys()
        deftaus=deftrk.keys()
        deftaus.sort()

        ntaus=len(deftaus)

        etau=0
        if(ntaus>1): etau=deftaus[ntaus-1]


        #
        # bail if no forecasts
        #
        if(etau == 0):

            #
            # case of initial position only, return for phr=0...
            #
            try:
                jtrk[etau]=deftrk[etau]
            except:
                jtrk[etau]=[]
            return(jtrk,deftaus)

        #
        # get motion of defined track
        #

        for i in range(0,ntaus):

            tau=deftaus[i]

            i0=i
            ip1=i+1

            if(ntaus > 1):

                if(i0 < ntaus-1):
                    i0=i
                    ip1=i+1

                elif(i0 == ntaus-1):
                    i0=i-1
                    ip1=i

                try:
                    dtau=deftaus[ip1]-deftaus[i0]
                except:
                    dtau=mf.dtgdiff(deftaus[i0],deftaus[ip1])

            else:

                dtau=0.0

            
            if(dtau == 0.0):
                edir=270.0
                espd=0.0
                dvmax=0.0
                dpmin=0.0
                dextra1=0.0
                dextra2=0.0

            else:

                tau0=deftaus[i0]
                tau1=deftaus[ip1]

                flat0=deftrk[tau0][0]
                flon0=deftrk[tau0][1]
                fvmax0=deftrk[tau0][2]
                fpmin0=deftrk[tau0][3]
                
                if(doextra1):
                    fextra10=deftrk[tau0][4]
                    fextra11=deftrk[tau1][4]

                if(doextra2):
                    fextra20=deftrk[tau0][5]
                    fextra21=deftrk[tau1][5]
                    
                # -- wind radii
                #
                if(itrkLen == 7):
                    
                    fr34s0=deftrk[tau0][4]
                    fr34s1=deftrk[tau1][4]
                    
                    fr50s0=deftrk[tau0][5]
                    fr50s1=deftrk[tau1][5]

                    fr64s0=deftrk[tau0][6]
                    fr64s1=deftrk[tau1][6]
                    

                flat1=deftrk[tau1][0]
                flon1=deftrk[tau1][1]
                fvmax1=deftrk[tau1][2]
                fpmin1=deftrk[tau1][3]

                # -- 20190910 -- test for both vmax and pmin, if undef then set to 0.0 or persistence
                #
                if(fvmax1 > 0.0 and fvmax0 > 0.0 ):
                    dvmax=fvmax1-fvmax0
                else:
                    dvmax=0.0
                    
                if(fpmin1 > 0.0 and fpmin0 > 0.0):
                    dpmin=fpmin1-fpmin0
                else:
                    dpmin=0.0
                
                if(doextra1):
                    dextra1=fextra11-fextra10
                
                if(doextra2):
                    dextra2=fextra21-fextra20

                (course,speed,eiu,eiv)=rumhdsp(flat0,flon0,flat1,flon1,dtau)

            #
            # use penultimate motion for end motion
            # set vmax/pmin change to 0.0
            #

            if(i == ip1):
                otau=deftaus[ip1]
                dvmax=0.0
                dpmin=0.0
                if(doextra1): dextra1=0.0
                if(doextra2): dextra2=0.0

            else:
                otau=deftaus[i0]

            mottrk[otau]=[course,speed,dvmax,dpmin]
            if(doextra1):
                mottrk[otau]=[course,speed,dvmax,dpmin,dextra1]
            if(doextra2):
                mottrk[otau]=[course,speed,dvmax,dpmin,dextra1,dextra2]
                
            # -- wind radii --  assume no change in wind radii in the tau interval -- set to beginning
            #
            if(itrkLen == 7):
                mottrk[otau]=[course,speed,dvmax,dpmin,fr34s0,fr50s0,fr64s0]
                

        taus=mottrk.keys()
        taus.sort()
        
        'ffffffffffffffffffffffff',mottrk

        # -- only go out +dtx(3) h at the end for the smoother only
        # -- final extrap after bias corr + smoothing
        #
        
        etau=taus[-1]
        
        if(doExtrap):
            try:    
                etaux=etau+dtx
            except:
                etaux=mf.dtginc(etau,dtx)
        else:
            etaux=etau
            

        try:
            otaus=range(btau,etaux+1,dtx)
        except:
            otaus=mf.dtgrange(btau,mf.dtginc(etaux,1),dtx)

        nt=len(taus)

        n=0
        tau0=taus[n]
        if(nt >= 1): tau1=taus[n+1]

        
        # -- rhumb-line interpolation ""rumterp" to the dtx track (0,3,6,9,12), nhc_interpfcst.f uses linear
        #

        for otau in otaus:

            if(otau == tau0):
                dtau=0

            # -- otau  is beyond the bounding interval
            #

            elif(otau >= tau1):

                atend=0

                # -- increment to set the interval so that otau is equal to tau0 or between tao0 and tau1
                #
                n=n+1
                if(n == nt-1):
                    n=n-1
                    atend=1

                tau0=taus[n]

                #ssssssssssssssssssssssssssssssssssssssssssssssssss -- special treatment

                # -- dtx > delta of deftrk, e.g., deftrk is 3 h from RAP and target is 6 h
                #

                if(tau0 < otau):
                    while(tau0 < otau):
                        n=n+1

                        # -- check if beyond def trk
                        #
                        if(n > nt-1):
                            tau0=taus[-1]
                            n=nt-1
                            break
                        else:
                            tau0=taus[n]

                    # -- check if at end
                    #
                    if(n == nt-1):
                        n=n-1
                        atend=1


                    # -- case where tau0 = otau
                    #
                    if(tau0 == otau): dtau=0

                #ssssssssssssssssssssssssssssssssssssssssssssssssss -- special treatment

                if(nt >= 1): tau1=taus[n+1]

                dtau=0
                #
                # correct handling of extrap point
                #
                if(atend and doExtrap):
                    tau0=tau1
                    tau1=otaus[-1]
                    try:
                        dtau=otau-tau0
                    except:
                        dtau=mf.dtgdiff(tau0,otau)


            else:
                try:
                    dtau=otau-tau0
                except:
                    dtau=mf.dtgdiff(tau0,otau)

            rlat0=deftrk[tau0][0]
            rlon0=deftrk[tau0][1]
            vmax0=deftrk[tau0][2]
            pmin0=deftrk[tau0][3]
            if(doextra1): extra10=deftrk[tau0][4]
            if(doextra2): extra20=deftrk[tau0][5]

            course=mottrk[tau0][0]
            speed=mottrk[tau0][1]
            dvmax=mottrk[tau0][2]
            dpmin=mottrk[tau0][3]
            if(doextra1): dextra1=mottrk[tau0][4]
            if(doextra2): dextra2=mottrk[tau0][5]
            
            # -- wind radii at beginning of interval
            #
            if(itrkLen == 7):
                r34sI=mottrk[tau0][4]
                r50sI=mottrk[tau0][5]
                r64sI=mottrk[tau0][6]

            if(dtau > 0):
                (rlat1,rlon1)=rumltlg(course,speed,dtau,rlat0,rlon0)
                try:
                    dt=float((tau1-tau0))
                except:
                    dt=mf.dtgdiff(tau0,tau1)

                vfact=float(dtau)/dt
                vmax1=vmax0+vfact*dvmax
                pmin1=pmin0+vfact*dpmin
                if(doextra1): extra11=extra10+vfact*dextra1
                if(doextra2): extra21=extra20+vfact*dextra2
                
                # -- do radius interp here -- set to tau0 for now -- use fr??s0 and fr??s1
                #
                if(itrkLen == 7):
                    r34sI=mottrk[tau0][4]
                    r50sI=mottrk[tau0][5]
                    r64sI=mottrk[tau0][6]
                
            else:
                rlat1=rlat0
                rlon1=rlon0
                vmax1=vmax0
                pmin1=pmin0
                if(doextra1): extra11=extra10
                if(doextra2): extra21=extra20
                vfact=0.0
                
                # -- wind radii for dtau = 0
                #
                if(itrkLen == 7):
                    r34sI=mottrk[tau0][4]
                    r50sI=mottrk[tau0][5]
                    r64sI=mottrk[tau0][6]

            #
            # make sure
            #

            jtrk[otau]=[rlat1,rlon1,vmax1,pmin1]

            if(doextra1):
                jtrk[otau]=[rlat1,rlon1,vmax1,pmin1,extra11]
                
            if(doextra2):
                jtrk[otau]=[rlat1,rlon1,vmax1,pmin1,extra11,extra21]
            
            # -- wind radii -- the 'interpolated' from above
            #
            if(itrkLen == 7):
                jtrk[otau]=[rlat1,rlon1,vmax1,pmin1,r34sI,r50sI,r64sI]

        rlats=self.Dic2list(jtrk,0)
        srlats=self.Smth121(rlats,npass)

        rlons=self.Dic2list(jtrk,1)
        srlons=self.Smth121(rlons,npass)

        vmaxs=self.Dic2list(jtrk,2)
        if(dovmaxSmth):
            svmaxs=self.Smth121(vmaxs,npass)
        else:
            svmaxs=vmaxs

        pmins=self.Dic2list(jtrk,3)
        spmins=self.Smth121(pmins,npass)

        if(doextra1):
            extra1s=self.Dic2list(jtrk,4)
            sextra1s=self.Smth121(extra1s,npass)

        if(doextra2):
            extra2s=self.Dic2list(jtrk,5)
            sextra2s=self.Smth121(extra2s,npass)

        self.List2Dict(jtrk,srlats,0)
        self.List2Dict(jtrk,srlons,1)
        self.List2Dict(jtrk,svmaxs,2)
        self.List2Dict(jtrk,spmins,3)
        if(doextra1): self.List2Dict(jtrk,sextra1s,4)
        if(doextra2): self.List2Dict(jtrk,sextra2s,5)

        return(jtrk,deftaus)



    #bbbbbbbbbbbbbbbbbbbcccccccccccccccccccccccccccccc
    #
    # bias correct and 3-h interp track from above 
    #
    #bbbbbbbbbbbbbbbbbbbcccccccccccccccccccccccccccccc

    def BiasCorrFcTrackInterpFill(self,jtrk,itrk,deftaus,phr,dtx,
                                  btlat,btlon,btdir,btspd,btvmax,
                                  model,dtg,stm3id,
                                  latlontaucut=0.0,latlontaumin=120.0,latloncorrmin=1.0,  # for lat/lon ghmi
                                  
                                  # -- 20190904 -- can duplicate hwfi with hwfr06 with the older and more
                                  #    standard? setup...
                                  
                                  #latlontaucut=0.0,latlontaumin=24.0,latloncorrmin=0.0,  # for modern models with better small tau errors
                                  vmaxtaucut=0.0,vmaxtaumin=24.0,vmaxcorrmin=200.0,     # bad to make blow up if vmaxCorrScheme not set correctly
                                  dopc=1,vmaxmin=20.0,vmaxCorrScheme='global',verb=0):


        #------------------------------------------------------------------------------------

        def PersistCorr(tau,lat0,lon0,course,speed,
                        latfc,lonfc,
                        pctauend=12,pcmin=0.33):

            (latp,lonp)=rumltlg(course,speed,tau,lat0,lon0)

            if(tau <= pctauend):
                pcorr=pcmin+(1.0-(float(tau)/pctauend))*(1.0-pcmin)
                latpc=(1.0-pcorr)*latfc + pcorr*latp
                lonpc=(1.0-pcorr)*lonfc + pcorr*lonp
                #print 'vvvvvvvvv------------------ ',tau,pcmin,pcorr,' lat: ',latfc,latp,latpc,' lon: ',lonfc,lonp,lonpc
            return(latpc,lonpc)


        # hard-wired from nhc_interp.f for dt=3
        #

        def fiextrap(t,a,b,c):
            x=(2.0*a + t*(4.0*b - c - 3.0*a + t*(c - 2.0*b + a)))/2.0
            return(x)


        def setfvmaxoffact(tau,atend,
                           vmaxtaumin,vmaxtaucut,vmaxcorrmin):

            ftau=float(tau)
            if(vmaxtaumin  > 0.0):

                if((ftau >= vmaxtaucut and ftau <= vmaxtaumin) ):
                    fvmaxofffact=((vmaxtaumin-ftau)/(vmaxtaumin-vmaxtaucut))*(1.0-vmaxcorrmin) + vmaxcorrmin

                elif(ftau > vmaxtaumin or atend):
                    fvmaxofffact=vmaxcorrmin

                elif((ftau < 0) or (ftau >= 0 and ftau < vmaxtaucut) ):
                    fvmaxofffact=1.0

                else:
                    print 'EEEEEEEEEEEEEEEE setfvmaxoffact error'
                    sys.exit()


            else:
                fvmaxofffact=1.0

            if(fvmaxofffact < 0.0): fvmaxofffact=0.0
            if(vmaxtaumin == 0.0):  fvmaxofffact=1.0

            return(fvmaxofffact)



        if(vmaxCorrScheme == 'global'):
            vmaxtaucut=0.0
            vmaxtaumin=72.0
            vmaxcorrmin=0.0
        elif(vmaxCorrScheme == 'lame' or vmaxCorrScheme == 'limited'):
            vmaxtaucut=0.0
            vmaxtaumin=24.0
            vmaxcorrmin=0.0



        #------------------------------------------------------------------------------------


        itaus=itrk.keys()
        itaus.sort()

        otrk=copy.deepcopy(itrk)

        taus=jtrk.keys()
        taus.sort()

        #
        #
        #
        try:
            latoff=btlat-jtrk[phr][0]
            lonoff=btlon-jtrk[phr][1]
            fvmaxoff=btvmax-jtrk[phr][2]

        except:
            print 'WWWWW no jtrk for: ',stm3id,'  dtg: ',dtg,'  phr: ',phr
            return(otrk)



        #print 'OO11111 latoff,lonoff %02f %5.1f %5.1f %6.1f %6.1f :: %6.1f %6.1f '%(phr,btlat,jtrk[phr][0],btlon,jtrk[phr][1],latoff,lonoff)

        if(verb > 2):
            itaus=itrk.keys()
            itaus.sort()
            for tau in itaus:
                # ['2008061806', 9.5, 132.1, 21.0, 0.0, 42.3, 0.100001, 42.3, -16.3001, -38.9, -29.6, 30.0, [-999, -999, -999, -999], [-999, -999, -999, -999]]
                print 'III tau: %03d'%(tau)," %5.1f %6.1f %3.0f"%(itrk[tau][0],itrk[tau][1],itrk[tau][2])
            for tau in taus:
                print 'JJJ tau: %03d'%(tau)," %5.1f %6.1f %3.0f"%(jtrk[tau][0],jtrk[tau][1],jtrk[tau][2])



        jtrknopc={}

        for tau in taus:

            atend=0
            if(tau == taus[-1]): atend=1

            vmoff=0.0
            dtau=tau-phr

            vmoff=setfvmaxoffact(dtau,atend,
                                 vmaxtaumin,vmaxtaucut,vmaxcorrmin)

            factlloff=setfvmaxoffact(dtau,atend,
                                     latlontaumin,latlontaucut,latloncorrmin)
            latbc=jtrk[tau][0]+latoff*factlloff
            lonbc=jtrk[tau][1]+lonoff*factlloff
            vmaxbc=jtrk[tau][2]+fvmaxoff*vmoff

            # -- undef
            #
            if(jtrk[tau][2] <= 0.0):
                vmaxbc=0.0

            jtrknopc[tau]=[latbc,lonbc,vmaxbc]

            latcur=loncur=-999.
            if(dtau >= 3 and dtau <= 12 and dopc):
                (latpc,lonpc)=PersistCorr(dtau,btlat,btlon,btdir,btspd,
                                          latbc,lonbc
                                          )
                latbc=latpc
                lonbc=lonpc

            jtrk[tau][0]=latbc
            jtrk[tau][1]=lonbc
            jtrk[tau][2]=vmaxbc

        # --do the extrap
        #

        xtaus=range(taus[-1],taus[-1]+phr,dtx)

        try:
            etaum1=taus[-2]
        except:
            etaum1=taus[0]


        for xtau in xtaus:
            tm2=xtau-3*dtx
            tm1=xtau-2*dtx
            tm0=xtau-dtx
            jtrknopc[xtau]=[0,0,0]
            jtrk[xtau]=[0,0,0,[],[]]
            for j in range(0,3):
                a=jtrk[tm2][j]
                b=jtrk[tm1][j]
                c=jtrk[tm0][j]
                jtrk[xtau][j]=fiextrap(3,a,b,c)

                try:
                    if(j == 0 and verb):  print 'try',xtau
                except:
                    if(j == 0 and verb): print 'except',xtau
                    jtrk[xtau]=jtrk[taus[-1]]
                    jtrk[xtau][j]=fiextrap(3,a,b,c)

                jtrknopc[xtau][j]=jtrk[xtau][j]

            # -- set radii constant from etau -> last xtau
            #
            #for j in range(3,5):
            #    jtrk[xtau][j]=jtrk[etaum1][j]


        taus=jtrk.keys()
        taus.sort()

        if(verb > 2):
            for tau in taus:
                print 'FFF tau: %03d'%(tau)," lat: %5.1f PC: %5.1f  lon: %6.1f PC: %6.1f"%(jtrk[tau][0],jtrknopc[tau][0],
                                                                                           jtrk[tau][1],jtrknopc[tau][1])

        # -- put out final track; shift radii to phr from tau=0, i.e., do not interpolate but assume forecast unchanged
        #
        if(verb):
            print 'model: ',model,' dtg: ',dtg,' stm3id: ',stm3id,' phr: ',phr,\
                  ' btdir/spd: ',btdir,btspd,' offset: ',latoff,lonoff,'bt lat/lon/vmax: ',btlat,btlon,btvmax

        # -- relabel/recenter 
        #
        for tau in deftaus:
            
            otrk[tau][0]=jtrk[tau+phr][0]
            otrk[tau][1]=jtrk[tau+phr][1]

            # -- make sure intensity does not fall below vmaxmin
            #
            ovmax=jtrk[tau+phr][2]
            if(ovmax < vmaxmin):
                ovmax=vmaxmin
            otrk[tau][2]=ovmax

            # -- do not use interpolated radii; assume the forecast is the constant  
            #
            #otrk[tau][12]=jtrk[tau][3]
            #otrk[tau][13]=jtrk[tau][4]

            if(verb):
                print 'OOO tau: %03d'%(tau)," %5.1f | %6.1f |  %3.0f III:  %5.1f | %6.1f |  %3.0f "%(otrk[tau][0],otrk[tau][1],otrk[tau][2],
                                                                                                     itrk[tau][0],itrk[tau][1],itrk[tau][2]
                                                                                                     )


        return(otrk)
    


#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc -- Adeck
# main classes
#

class AdToAtcfInvHash(InvHash):

    def __init__(self,
                 source='',
                 byear=None,
                 bnameBase='Inv-adToAtcf',
                 tbdir=None,
                 diag=1,
                 verb=0,
                 overrideInv=0,
                 unlink=0):

        if(byear == None): byear=mf.dtg()[0:4]

        if(bnameBase == 'Inv-AD2'): 
            dbname="%s-%s-%s"%(bnameBase,source,byear)
        else:
            dbname="%s-%s-%s"%(bnameBase,source,byear)
            

        MF=MFutils()
        self.dbname=dbname
        self.tbdir=tbdir
        self.override=overrideInv
        self.verb=verb

        self.dbname=dbname
        self.dbfile=dbname

        if(tbdir == None):
            tbdir=ptmpBaseDir
            self.dsbdir="%s/DSs"%(tbdir)
        else:
            self.dsbdir=tbdir

        MF.ChkDir(self.dsbdir,'mk')

        self.DS=DataSet(bdir=self.dsbdir,name=self.dbfile,verb=verb,unlink=self.override)
        self.DS.verb=verb

        if(diag): MF.sTimer('setDSs')
            
        rc=self.DS.getPyp()
        
        if(rc != None):
            self.data=rc.data
        else:
            self.data={}

        if(self.override): 
            self.data={}

        if(diag): MF.dTimer('setDSs')

    def put(self,diag=1,override=0):
        if(diag): MF.sTimer('DS-put')
        self.DS.data=self.data
        # -- override at DataSet() above; or here if override set on in put()
        self.DS.putPyp(override=override)
        asiz=MF.getPathSiz(self.DS.pyppath)
        asiz=float(asiz)/(1024)
        MF.sTimer('DS-put-%-5.0f Kb'%(asiz))
        MF.dTimer('DS-put-%-5.0f Kb'%(asiz))
        
        if(diag): MF.dTimer('DS-put')


    def lsInv(self,
              ):

        kk=self.data.keys()
        for k in kk:
            print 'key: ',k,'data.val: ',self.data[k]




class ConAdeck(ADutils):
    
    """ Consensus Adeck Class
    """
    
    iAidsMcon={
        'avno':['nhc.jtwc.ncep', 1,1, ['tgfs2:tmtrkN']           ],
        'edet':['ecmwf',         1,1, ['tecm2:tmtrkN','emx:ncep']],
        'egrr':['nhc.jtwc',      1,1, ['tukm2:tmtrkN']           ],
        'hwrf':['nhc.jtwc',      0,1, [                         ]],
        'fim9':['rtfim9',        0,1, ['fim8:rtfim']             ],
    }    
                
    cAidMcon='conm'
    
                
    
    def __init__(self,dtg,stmid,iAids=None,cAid=None):
        
        
        self.dtg=dtg
        self.stmid=stmid
        
        if(iAids == None):
            iAids=self.iAidsMcon
        else:
            self.iAids=iAids
        if(cAid == None):
            self.cAid=self.cAidMcon
        else:
            self.cAid=cAid
        
        
class Adeck(ADutils):

    distminHIT=180.0
    distminHIT9X=300.0

    def __init__(self,adeckpathmasks,mD=None,dtgopt=None,taids=None,verb=0,warn=0,doVD=0,
                 skipcarq=1,
                 undef=-9999.,
                 chkb2id=1,
                 mDp1=None,
                 adyear=None,
                 adyearp1=None,
                 dofilt9x=0,
                 prependAid=None,
                 aliases=None,
                 adeckCards=None,
                 ):

        
        #
        # trick to dectect if mask is a list...
        #
        if(type(adeckpathmasks) is ListType):
            adeckpaths=[]
            for adeckpathmask in adeckpathmasks:
                adeckpaths=adeckpaths+glob.glob(adeckpathmask)

        else:
            adeckpaths=glob.glob(adeckpathmasks)

        if(dtgopt != None):
            self.tdtgs=dtgs=mf.dtg_dtgopt_prc(dtgopt,ddtg=6)


        if( (taids != None) and (type(taids) is not(ListType)) ):
            taids=[taids]

        self.mD=mD
        self.mDp1=mDp1

        self.dofilt9x=dofilt9x
        
        self.adyear=adyear
        self.adyearp1=adyearp1

        self.adecks=adeckpaths
        self.dtgopt=dtgopt
        self.taids=taids
        self.verb=verb
        self.warn=warn
        self.skipcarq=skipcarq
        self.undef=undef
        self.chkb2id=chkb2id
        self.aliases=aliases
        self.prependAid=prependAid

        self.initVars()
        if(adeckCards == None):
            self.initAdeckPaths(adeckpaths)
        else:
            self.getCards(adeckCards)
            
        self.initAdeck()

        if(doVD):
            import vdVM
            self.makeVdeck=VD.MakeVdeck
        

    def initVars(self,dob2idchk=0):

        self.dob2idchk=dob2idchk

        self.stm2ids=[]
        self.stm1ids=[]

        self.dtgs=[]
        self.aids=[]

        self.stmdtgs={}
        self.aiddtgs={}
        self.aidstms={}
        self.aidcards={}
        self.aidtaus={}
        self.aidtausStatus={}
        self.aidtrks={}
        self.adeckyears=[]
        self.adeckbasins=[]

    def getCards(self,adeckCards):

        #cards=[]
        #for adeckpath in adeckpaths:
            #(adyear,adbasin)=getAdeckYearBasinFromPath(adeckpath)
            #if(adyear != None):
                #self.adeckyears.append(adyear)
                #self.adeckbasins.append(adbasin)
            
            #try:
                #ttt=open(adeckpath).readlines()
            #except:
                #ttt=None

            #if(cards == None):
                #return
            #else:
                #cards=cards+ttt

        self.cards=adeckCards
        

    def initAdeckPaths(self,adeckpaths):

        cards=[]
        for adeckpath in adeckpaths:
            (adyear,adbasin)=getAdeckYearBasinFromPath(adeckpath)
            if(adyear != None):
                self.adeckyears.append(adyear)
                self.adeckbasins.append(adbasin)
            
            try:
                ttt=open(adeckpath).readlines()
            except:
                ttt=None

            if(cards == None):
                return
            else:
                cards=cards+ttt

        self.cards=cards
        
        self.adeckyears=mf.uniq(self.adeckyears)
        self.adeckbasins=mf.uniq(self.adeckbasins)


    def isValidB2id(self,b2id):

        rc=0
        if(b2id.upper() in Basin2toBasin1.keys()): rc=1
        return(rc)


    def isAidVmaxOnly(self,aid):

        rc=0
        if( aid == None): return(rc)

        if(
            aid.upper() == 'SHF5' or
            aid.upper() == 'SHFR' or
            aid.upper() == 'IVCN' or
            aid.upper() == 'ICON' or
            aid.upper() == 'ST11' or
            aid.upper() == 'ST5D' or
            aid.upper() == 'S5YY' or
            aid.upper() == 'DSHA' or
            aid.upper() == 'DSHN' or
            aid.upper() == 'CCON' or
            aid.upper() == 'DSHW' or
            aid.upper() == 'DTOP' or
            aid.upper() == 'SHIW' or
            aid.upper() == 'SHIP' or
            aid.upper() == 'S511' or
            aid.upper() == 'S5RI' or
            aid.upper() == 'SHIA' or
            aid.upper() == 'SHIE' or
            aid.upper() == 'SHIN' or
            aid.upper() == 'DSHE' or
# -- 20211028 -- from nhc
            aid.upper() == 'DSNS' or
            aid.upper() == 'SHNS' or
#
            aid.upper() == 'DSHP' or
            aid.upper() == 'CMES' or
            aid.upper() == 'CMSD' or
            aid.upper() == 'SHIU' or
            aid.upper() == 'DSHU' or
            aid.upper() == 'DC30' or
            
            aid.upper() == 'RI20' or
            aid.upper() == 'RI25' or
            aid.upper() == 'RI30' or
            aid.upper() == 'RI35' or
            aid.upper() == 'RI40' or
            aid.upper() == 'RI45' or
            aid.upper() == 'RI55' or
            aid.upper() == 'RI56' or
            aid.upper() == 'RI65' or
            aid.upper() == 'RI70' or
            aid.upper() == 'RICN' or
            aid.upper() == 'RIPA' or
            aid.upper() == 'RIDE' or
            aid.upper() == 'RD25' or

            aid.upper() == 'RVCN' or
            aid.upper() == 'RVCX' or
            aid.upper() == 'TVCC' or
            
            aid.upper() == 'IV15' or
            aid.upper() == 'IVCR' or
            aid.upper() == 'LGEM' or
            aid.upper() == 'SPC3' or
            aid.upper() == 'KSF5' or
            aid.upper() == 'KSFR' or
            aid.upper() == 'IVRI' or
            aid.upper() == 'KLGM' or
            aid.upper() == 'KSHP' or
            aid.upper() == 'KDSP' or
            aid.upper() == 'DSHF' or
            aid.upper() == 'CNTR' or
            #aid.upper() == 'PEST' or
            
            aid.upper() == 'TCCN' or
            #aid.upper() == 'SPC3' or
            #aid.upper() == 'SPC3' or
            #aid.upper() == 'SPC3' or
            aid.upper() == 'ICNW' or
            aid.upper() == 'ICNX' or
            aid.upper() == 'RD20' or
            aid.upper() == 'RD30' or
            aid.upper() == 'RD35' or
            aid.upper() == 'RD40' or
            aid.upper() == 'RD45' or
            aid.upper() == 'RD55' or
            aid.upper() == 'RD56' or
            aid.upper() == 'RD65' or
            aid.upper() == 'RD70' or
            aid.upper() == 'FRIA' or
            aid.upper() == 'ICNE' or
            aid.upper() == 'JTWX' or
            
            
            aid.upper() == 'S5XX'

            ): rc=1

        return(rc)




    def makeIposit(self,tt,card,ncards,ntt,verb=0,aid=None,ipositPrev=None):

        def tt2rad(tt):
            try:
                rad=(float(tt[13]),float(tt[14]),float(tt[15]),float(tt[16]))
            except:
                print 'error in tt2rad for tt: ',tt
            return(rad)
            
        #WP, 22, 2014112912, 03, FIM9, 108, 119N, 1385E,  77,  985, XX,  64, NEQ,   95,   69,    0,   85,
        #0    1           2   3     4    5     6      7    8     9  10   11   12    13    14    15    16
        # --------- get tau and lat/lons, vmax, p,in
        #
        try:
            tau=tt[5].strip()
            itau=int(tau)

            # -- basic sanity check, if alat=alon=0, and vmax is not there... noload
            #
            clat=tt[6].strip()
            clon=tt[7].strip()
        except:
            if(self.warn): print 'WWW gooned up card, failed tau,clat,clon: %6i'%(ncards),' card: ',card[0:-1],ntt
            return(None,None)

        try:     vmax=float(tt[8])
        except:  vmax=self.undef
        
        if(vmax == 0):
            vmax=self.undef

        try:
            (alat,alon)=Clatlon2Rlatlon(clat,clon)
        except:
            # -- set  blank clat,clon to 0.0 for next check
            #
            if(clat == '' and clon == ''):
                alat=0.0
                alon=0.0
            else:
                if(self.warn): print 'WWW gooned up clat,clon: %6i'%(ncards),'clat,clon: ',clat,clon,'card: ',card[0:-1],'ntt: ',ntt
                return(None,None)

        if((alat == 0.0 and (alon == 0.0 or alon == 360.0)) and not(self.isAidVmaxOnly(aid)) ):
            if(self.warn): print 'WWW(Adeck.makeIpost): 0N 0W NOLOAD aid: ',aid,'isVmaxOnly: ',self.isAidVmaxOnly(aid),'card: ',card[:-1]
            return(None,None)

        #if(alat == 0.0 and (alon == 0.0 or alon == 360.0) and vmax == 0.0):
        #    if(verb): print '0N 0W Vmax0 NOLOAD : ',card[:-1]
        #    return(None,None)

        try:      pmin=float(tt[9])
        except:   pmin=self.undef
        if(pmin == 0.0): pmin=self.undef

        # -- pull r34 by default if ipositPrev == None
        #
        if(ipositPrev == None):
            
            r34=None
            r50=None
            r64=None

            #r34=(self.undef,self.undef,self.undef,self.undef)
            #r50=(self.undef,self.undef,self.undef,self.undef)
            #r64=(self.undef,self.undef,self.undef,self.undef)

            try:
                if(len(tt) > 16 and int(tt[11]) == 34 and tt[12].strip() == 'NEQ'): r34=tt2rad(tt)
            except:
                if(self.warn):
                    print 'WWW(Adeck.makeIpost): bad card in getting r34 -- aid: ',aid,'card: ',card[:-1]
                    print 'WWW(Adeck.makeIpost): setting r34/r50/r64 to undef...'
            try:
                if(len(tt) > 16 and int(tt[11]) == 50 and tt[12].strip() == 'NEQ'): r50=tt2rad(tt)
            except:
                if(self.warn):
                    print 'WWW(Adeck.makeIpost): bad card in getting r34 -- aid: ',aid,'card: ',card[:-1]
                    print 'WWW(Adeck.makeIpost): setting r34/r50/r64 to undef...'
                
            try:
                if(len(tt) > 16 and int(tt[11]) == 64 and tt[12].strip() == 'NEQ'): r64=tt2rad(tt)
            except:
                if(self.warn):
                    print 'WWW(Adeck.makeIpost): bad card in getting r34 -- aid: ',aid,'card: ',card[:-1]
                    print 'WWW(Adeck.makeIpost): setting r34/r50/r64 to undef...'
                        
            iposit=(alat,alon,vmax,pmin,r34,r50,r64)

        # -- !!!!!!!! - need to add code class Adeck to pass in previous iposit to check if only updating r50,r64
        #
        else:

            print 'WWWWWWWWWWWWWWWWXXXXXXXXXXXXXXXXXXx - no code to handle passing in prevIposit into Adeck.makeIposit...bye'
            sys.exit()
            r34=(self.undef,self.undef,self.undef,self.undef)
            r50=(self.undef,self.undef,self.undef,self.undef)
            r64=(self.undef,self.undef,self.undef,self.undef)
            
            if(len(tt) > 16):
                if(int(tt[11]) == 34 and tt[12].strip() == 'NEQ'): r34=tt2rad(tt)
                if(int(tt[11]) == 50 and tt[12].strip() == 'NEQ'): r50=tt2rad(tt)
                if(int(tt[11]) == 64 and tt[12].strip() == 'NEQ'): r64=tt2rad(tt)
                
            iposit=(alat,alon,vmax,pmin,r34,r50,r64)

        return(itau,iposit)


    def setDtgNCard(self,tt):
        dtg=tt[2].strip()
        if(len(dtg) != 10):
            return(None)

        return(dtg)



    def makeBidDtg(self,tt,card,maxPrevYearDtgdiff=240.0):

        b2id=tt[0].strip()
        bnum=tt[1].strip()
        bnumi=bnum
        ibnum=bnum

        # check for ** in b2id  -- from rerun of tracker on tacc?
        #
        if(b2id == '**'):
            if(self.dob2idchk):
                print """EEEEEEEEEEE b2id check gives '**', we'll stop in initAdeck, until you mod the code want to just continue"""
                print 'card: ',card
                sys.exit()
            else:
                b2id='XX'

        elif(b2id.isdigit()):
            if(self.warn): print 'WWW --adeck-- gooned up acard: 2-char basin is a number: ',card[:-1],' ...'
            return(None)

        if(not(self.isValidB2id(b2id)) and self.chkb2id):
            if(self.warn): print 'WWW --adeck-- gooned up acard: 2-char basin is NOT standard: ',card[0:-1],' ...'
            return(None)

        #  check for unspecified bnum, e.g., when b2id == '**'
        #
        if(len(bnum) == 2):

            # -- handle new [A-Z][0-9] for 9X
            #
            bnum1=bnum[0].upper()
            if(ord(bnum1) >= 65 and ord(bnum1) <= 90):
                try:
                    bnum=90+int(bnum[1])
                    bnum=str(bnum)
                except:
                    print 'WWW bad acard in makeBidDtg(bad ord(bnum1): ',card[:-1],' bnum not defined...onward...'
                    return(None)

            try:      
                int(bnum)
            except:   
                print 'WWW bad acard in makeBidDtg(non int): ',card[:-1],' bnum not defined...onward...'
                return(None)

        # -- case when 3-char id in the basin id in the 'sink' format
        #
        elif(len(bnum) == 3):
            if(type(bnumi[0]) is str):
                bnumi="9%s"%(bnumi[1:])
            try:
                ibnum=int(bnumi[0:2])
                bnum=bnum[0:2]
            except:
                print 'WWW 333333 bad acard(Adeck): ',bnum,card[:-1],' bnum not defined...onward...'
                return(None)

        elif(len(bnum) >= 4):
            try:
                ibnum=int(bnum[0:2])
                bnum=bnum[0:2]
            except:
                print 'WWW 44444 bad acard: ',bnum,card[:-1],' bnum not defined...onward...'
                return(None)

        # -- case when 1-char id in the basin id in the 'sink' format
        #
        elif(len(bnum) == 1):
            try:
                ibnum=int(bnum[0])
                bnum="%02d"%(ibnum)
                print 'WWW single bnum: ',bnum,'stm2id: ',stm2id
            except:
                print 'WWW 111111 bad bnun in acard: ',bnum,card[:-1],' bnum not defined...onward...'
                return(None)

        # -- blank bnum
        #
        elif(len(bnum) == 0):
            print 'WWW 000000 bad bnum in acard: ',bnum,card[:-1],' bnum 0 length...onward...'
            return(None)

        # -- filter out 8X storms
        #
        if(ibnum >= 80 and ibnum <= 89): return(None)

        # -- check if adeck uses sss.yyyy form of storm id vice standard 2-char stm id
        #

        if(len(bnum.split('.')) == 2):
            bn=bnum.split('.')[0]
            b1=bn[2]
            bn=bn[0:2]
            by=bnum.split('.')[1]
            bnum=bn

        # -- 9999999999999999999999999999999999 filter out 9X
        #
        if(self.dofilt9x and Is9XSnum(bnum)): return(None)
        
        dtg=self.setDtgNCard(tt)
        if(dtg == None):
            print 'WWW Adeck().setDtgNCard bad dtg: ',dtg,card 
            return(None)


        byear=dtg[0:4]
        # -- handle shem...
        #
        stm2id="%s%s.%s"%(b2id,bnumi,byear)
        if(isShemBasinStm(stm2id)):  byear=getShemYear(dtg)
        
        # -- if not an adeck use -- return
        #
        if(not(hasattr(self,'adyear'))):
            #print '11111111111111111111 ',dtg,b2id,bnumi,byear
            return(dtg,b2id,bnumi,byear)
        
        # -- check byear for storms starting in previous year
        #
        if( (self.adyear != None and self.adyearp1 != None) ):

            yeardiffSH=0
            isSH=isShemBasinStm(b2id)
            if(isSH):  yeardiffSH=int(dtg[0:4])-int(self.adyear)

            yeardiff=int(byear)-int(self.adyear)

            if(yeardiff == -1 and not(isSH)):
                prevYearDtgdiff=mf.dtgdiff(dtg,"%4s010100"%(self.adyear[0:4]))
                if(prevYearDtgdiff > maxPrevYearDtgdiff):
                    print 'WWW Adeck().makeBidDtg() !!!!!!!!!!!!!!!!!!!!!! storm dtg < ',self.adyear,' prevYearDtgdiff: %4.0f'%(prevYearDtgdiff),\
                          ' > maxPrevYearDtgdiff: %4.0f'%(maxPrevYearDtgdiff),' card: ',card[0:40],'...press...'
                    return(None)
                else:
                    print 'WWW Adeck().makeBidDtg() storm dtg < ',self.adyear,' set to self.adyear when prevYearDtgdiff: %4.0f'%(prevYearDtgdiff),\
                          ' < maxPrevYearDtgdiff: %4.0f'%(maxPrevYearDtgdiff),' card: ',card[0:40]
                byear=self.adyear
            elif(yeardiffSH < -1):
                print 'EEE  Adeck().makeBidDtg() year diff too big for card: ',card[0:70]
                return(None)
            
        # -- check if byear in the adeckyears implied by the adeckpaths...if not, bail
        #
        if(len(self.adeckyears) > 0 and not(byear in self.adeckyears)): 
            print 'WWW Adeck.makeBidDtg byear of the storm NOT in the year implied by the adeck file name...press...',card[0:48]
            return(None)

        #print 'llllllllllllllllll',dtg,b2id,bnumi,byear
        return(dtg,b2id,bnumi,byear)


    def setAidNCard(self,tt):
        aid=tt[4].strip()
        return(aid)


    def makeAid(self,tt,card):

        aid=self.setAidNCard(tt)
        aid=aid.lower()


        # -- filter out carq
        #
        gotaid=0
        if(self.skipcarq and aid == 'carq'):
            return(gotaid,None,None)

        # -- aliases
        #
        if(self.aliases != None):
            for k in self.aliases.keys():
                if(aid == k):
                    oaid=self.aliases[k].upper()
                    iaid=aid.upper()

                    # -- convert 3-char aid -> 4-char
                    #
                    if(len(aid.upper()) <= 3): iaid="%4s"%(iaid)
                    card=card.replace(iaid,oaid)

                    # -- case where iaid is lowercase in card
                    #
                    card=card.replace(aid,oaid)
                    aid=oaid.lower()


        # --- replace _ with X in aid name
        #
        if(aid.replace('_','X')):
            aid=aid.replace('_','X')

        if(self.taids != None):
            gotaid=0
            for taid in self.taids:
                if(aid == taid):
                    gotaid=1
                    break
        else:
            gotaid=1

        return(gotaid,aid,card)


    def initAdeck(self,skipcarq=1,nlenmin=6,nlenmax=-999,filtHiFreq=1,maxDtau=6,verb=0):

        """  main method that parses the adeck cards and associates 9X storms with real NN storms using
        the mdeck object mD that has dicts and methods to get bt lat/lons

        """
        iposits={}
        
        ncards=1
        for card in self.cards:

            tt=card.split(',')
            ntt=len(tt)
            
            # -- check for blank card
            #
            if(ntt <= 1):
                continue
                
            # -- check for short cards
            #
            if(ntt <= nlenmin):
                print 'WWW short adeck card # ',ncards,card[:-1]
                continue

            #  -- check for long cards -- problem on jet/nccs in io from marchok tracker
            #
            if(nlenmax > 0 and ntt > nlenmax):
                print 'WWW LONG  adeck card # ',ncards,card[:-1]
                continue


            # -- get bid, dtg
            #
            rc=self.makeBidDtg(tt,card)
            if(rc == None): continue
            (dtg,b2id,bnum,byear)=rc

            # -- get aid
            #
            (gotaid,aidin,card)=self.makeAid(tt,card)
            if(hasattr(self,'prependAid')):
                if(self.prependAid != None):
                    aid="%1s%s"%(self.prependAid,aidin)
                else:
                    aid=aidin
            else:
                aid=aidin 
            
            if(self.aliases != None):
                try:
                    aidout=self.aliases[aidin.upper()]
                    card=card.replace(aidin.upper(),aidout,1)
                except:
                    None
            

            if(gotaid == 0): continue

            # -- get posit list
            #
            (itau,iposit)=self.makeIposit(tt,card,ncards,ntt,aid=aid)
            
            
            # -- filter out hi-frequency, e.g., hwrf in 2014 hourly 0-9 then 3 hourly
            #
            if(filtHiFreq and itau != None):
                if(itau%maxDtau != 0): continue
                
                
            if(itau == None): continue


            b2id=basin2Chk(b2id)

            stm2id="%s%s.%s"%(b2id,bnum,byear)
            stm2id=stm2id.lower()

            #######if(self.verb): print 'AAA ',aid,dtg,stm2id,itau
            # -- put correct 2-char basin in the input card
            #
            card=b2id+card[2:]

            # --- make lists and dicts
            #
            self.appendList(self.dtgs,dtg)
            self.appendList(self.stm2ids,stm2id)
            self.appendList(self.aids,aid)

            self.appendDictList(self.stmdtgs,stm2id,dtg)
            self.appendDictList(self.aiddtgs,(aid,stm2id),dtg)
            self.appendDictList(self.aidstms,aid,stm2id)
            self.appendDictList(self.aidtaus,(aid,stm2id,dtg),itau)

            self.append2KeyDictList(self.aidcards,(aid,stm2id),dtg,card)
            #self.append3KeyDictList(self.aidtrks,(aid,stm2id),dtg,itau,iposit)
            self.append3TupleKeyDictList(iposits,(aid,stm2id),dtg,itau,iposit)

            ncards=ncards+1
            
        kk=iposits.keys()
        kk.sort()
        for k in kk:
            k1=k[0]
            k2=k[1]
            k3=k[2]
            posits=iposits[k]
            
            r34Final=r50Final=r64Final=None
            
            if(len(posits) == 1):
                iposit=posits[0]
                if(verb):
                    print '1111111111',k1,k2,k3,'111: ',iposit
                
            elif(len(posits) == 2):
                
                iposit1=posits[0]
                iposit2=posits[1]
                
                r341=iposit1[-3]
                r501=iposit1[-2]
                r641=iposit1[-1]
                
                r342=iposit2[-3]
                r502=iposit2[-2]
                r642=iposit2[-1]
                
                if(verb):
                    print '2222222222',k1,k2,k3,'111: ',iposit1,' 222: ',iposit2
                    print '2222222222 r341:',r341,' r501: ',r501,' r641: ',r641
                    print '2222222222 r342:',r342,' r502: ',r502,' r642: ',r642
                    
                if(r341 != None): r34Final=r341
                if(r342 != None): r34Final=r342
                
                if(r501 != None): r50Final=r501
                if(r502 != None): r50Final=r502
                
                if(r641 != None): r64Final=r641
                if(r642 != None): r64Final=r642

                iposit=list(iposit1)
                iposit[-3]=r34Final
                iposit[-2]=r50Final
                iposit[-1]=r64Final
                iposit=tuple(iposit)

                
            elif(len(posits) == 3):

                iposit1=posits[0]
                iposit2=posits[1]
                iposit3=posits[2]

                r341=iposit1[-3]
                r501=iposit1[-2]
                r641=iposit1[-1]
                
                r342=iposit2[-3]
                r502=iposit2[-2]
                r642=iposit2[-1]
                
                r343=iposit3[-3]
                r503=iposit3[-2]
                r643=iposit3[-1]
                
                if(verb):
                    print '33333333',k1,k2,k3,'111: ',iposit1,' 222: ',iposit2
                    print '33333333 r341:',r341,' r501: ',r501,' r641: ',r641
                    print '33333333 r342:',r342,' r502: ',r502,' r642: ',r642
                    print '33333333 r343:',r343,' r503: ',r503,' r643: ',r643
                    
                if(r341 != None): r34Final=r341
                if(r342 != None): r34Final=r342
                if(r343 != None): r34Final=r343
                
                if(r501 != None): r50Final=r501
                if(r502 != None): r50Final=r502
                if(r503 != None): r50Final=r503
                
                if(r641 != None): r64Final=r641
                if(r642 != None): r64Final=r642
                if(r643 != None): r64Final=r643
                
                iposit=list(iposit1)
                iposit[-3]=r34Final
                iposit[-2]=r50Final
                iposit[-1]=r64Final
                
                iposit=tuple(iposit)
                
            if(verb): print 'FFFFFFFFF ',k1,k2,k3,iposit
            
            self.append3KeyDictList(self.aidtrks,k1,k2,k3,iposit)
                
        # --- uniq
        #

        self.dtgs=self.uniq(self.dtgs)
        self.aids=self.uniq(self.aids)
        self.stm2ids=self.uniq(self.stm2ids)
        self.uniqDictList(self.aidtaus)

        for stm2id in self.stm2ids:
            temp=self.uniq(self.stmdtgs[stm2id])
            self.stmdtgs[stm2id]=temp

        for aid in self.aids:
            for stm2id in self.stm2ids:
                try:
                    temp=self.uniq(self.aiddtgs[aid,stm2id])
                    self.aiddtgs[aid,stm2id]=temp
                except:
                    iok=0

        for aid in self.aids:
            self.aidstms[aid]=self.uniq(self.aidstms[aid])


        for stm2id in self.stm2ids:
            self.stm1ids.append(stm2idTostm1id(stm2id))

        self.dtgs.reverse()
        self.aids.sort()

        self.naids=len(self.aids)
        self.ndtgs=len(self.dtgs)

    #eeeeeeeeeeeeeeeee end of initAdeck methed




    def relabelAidcards(self,warn=1):

        for (aid,stm2id) in self.aiddtgs.keys():
            dtgs=self.aiddtgs[aid,stm2id]
            snum=int(stm2id[2:4])
            for dtg in dtgs:
                acards=self.aidcards[aid,stm2id][dtg]
                tau0=self.aidtaus[aid,stm2id,dtg][0]
                posit0=self.aidtrks[aid,stm2id][dtg][tau0]

                if(tau0 != 0 and warn):
                    print 'WWW AD.Adeck.relabelAidcards() initial tau for aid: ',aid,' stm2id: ',stm2id,' dtg: ',dtg,' tau0: ',tau0,' posit0: ',posit0,' MISSING'

                if(int(snum) >= 90 and int(snum) <=99):
                    alat=posit0[0]
                    alon=posit0[1]
                    self.relabel9X(stm2id,dtg,alat,alon)
                    if(self.gothit):
                        self.relabelAcards(acards,aid,stm2id,dtg)


    def getAiddtgsFromAidcards(self,tag=''):

        aiddtgs={}
        kk=self.aidcards.keys()
        kk.sort()
        for k in kk:
            (aid,stm2id)=k
            bnum=int(stm2id[2:4])
            if(bnum >= 80): continue
            kkk=self.aidcards[k]
            dtgs=kkk.keys()
            dtgs.sort()
            aiddtgs[k]=dtgs

        return(aiddtgs)


    def cmpAiddtgs(self,Bdtgs,Adtgs):
        astms=Adtgs.keys()
        bstms=Bdtgs.keys()

        allstms=astms+bstms
        allstms=self.uniq(allstms)

        for stm in allstms:
            try:    bds=Bdtgs[stm]
            except: bds=[]

            try:    ads=Adtgs[stm]
            except: ads=[]

            try:    aldtg=ads[-1]
            except: aldtg='None      '

            try:    bldtg=bds[-1]
            except: bldtg=' --None--  '

            print 'Stm: ',stm,"Before: %3d  After: %3d   Bldtg: %s  Aldtg: %s "%(len(bds),len(ads),bldtg,aldtg)



    def lsAidcards(self,tag='',dtgopt=None,warn=0):

        if(dtgopt != None):
            dtgs=mf.dtg_dtgopt_prc(dtgopt,ddtg=6)

        # -- new method to print the cards
        #
        if(hasattr(self,'acards')):
            
            kk=self.acards.keys()
            kk.sort()
    
            for k in kk:
                if(dtgopt == None or (dtgopt != None and  k in dtgs) ):
                    print
                    print 'bdtg: ',k,' aid: ',self.aid
                    cc=self.acards[k]
                    for c in cc:
                        print c[:-1]

        elif( (hasattr(self,'aidcards') and self.aidcards != None) and 
              (hasattr(self,'aiddtgs') and self.aiddtgs != None)
              ):

            # -- older form
            kk=self.aidcards.keys()
    
            for (aid,stm2id) in kk:
                bnum=int(stm2id[2:4])
                if(bnum >= 80): continue
                dtgs=self.aiddtgs[aid,stm2id]
                snum=stm2id[2:4]
                for dtg in dtgs:
                    print
                    print 'bdtg: ',dtg,' aid: ',self.taid
                    acards=self.aidcards[aid,stm2id][dtg]
                    for acard in acards:
                        print acard[0:156],'...'
                    #taus=self.aidtaus[aid,stm2id,dtg]
                    #posits=self.aidtrks[aid,stm2id][dtg]
                    
        else:
            if(warn):
                print   
                print 'IIIIIIIII' 
                print 'IIIIIIIIIIIIIII adCL.Adeck.lsAidcards -- no acards in newer AD for ',self.taid
                print 'IIIIIIIII' 
                


    def relabel9X(self,stm2id,dtg,alat,alon,verb=0):

        try:
            #tcs=self.mD.stm2dtg[dtg]
            tcs=self.mD.getTC2idsFromDtg(dtg,dofilt9x=1)
        except:
            print 'WWW no tcs for stm2id: ',stm2id,' for dtg: ',dtg
            self.gothit=0
            self.nstm2id=stm2id
            return


        stms=tcs.keys()

        distmin=1e20
        gothit=0
        for stm in stms:
            tt=tcs[stm]
            blat=tt[0]
            blon=tt[1]
            dist=gc_dist(blat,blon,alat,alon)
            if(dist < distmin):
                distmin=dist
                stm2idmin=stm

            if(verb): print 'RRRRRRRR ',stm2id,stm,dtg,alat,alon,blat,blon,dist,self.distminHIT,self.distminHIT9X
            if(distmin < self.distminHIT or
               (stm2id[2] == '9' and (distmin < self.distminHIT9X)) ):
                gothit=1


        if(gothit):
            if(verb): print 'HHHHHHHHHHH(relabel9X) ','stm2id: ',stm2id,' ==> nstm2id: ',stm2idmin," distmin: %6.2f"%(distmin),' dtg: ',dtg

        else:
            gohit=0
            stm2idmin=stm2id
            if(self.warn):
                print 'WWW in AD: could not find storm for stm2id: ',stm2id,' do not set here... ',alat,alon,dtg

        self.gothit=gothit
        self.nstm2id=stm2idmin



    def relabelAcards(self,acards,aid,stm2id,dtg):

        isnum=stm2id[2:4]

        ob2id=stm2id[0:2].upper()
        osnum=self.nstm2id[2:4]

        ostmid="%s, %s, "%(ob2id,osnum)

        #print '---------------------------------------------: ',ostmid,self.nstm2id,len(acards)

        ocards=[]
        for card in acards:
            istmid="%s, %s, "%(card[0:2],isnum)
            ncard=card.replace(istmid,ostmid)
            ocards.append(ncard)

        for ocard in ocards:
            self.append2KeyDictList(self.aidcards,(aid,self.nstm2id),dtg,ocard)


    def getAidTrk(self):


        try:
            ats=self.ats
        except:
            ats={}


        if(len(ats) == 0):
            AT=AidTrk()
            if(hasattr(self,'taid')):
                AT.aid=self.taid
            else:
                AT.aid='undef'
            return(AT)

        trks=ats

        dtgs=trks.keys()
        dtgs.sort()

        AT=AidTrk(dtgs,trks)

        if(hasattr(self,'taid')):
            AT.aid=self.taid
        else:
            AT.aid='undef'

        if(hasattr(self,'tstmid')):
            AT.stmid=self.tstmid
        else:
            AT.stmid='undef'

        return(AT)


    def getBestTrk(self):

        from tcCL import BestTrk
        
        try:
            btcs=self.bts
        except:
            btcs=None

        if(btcs != None):
            dtgs=btcs.keys()
            BT=BestTrk(dtgs,btcs)
            if(hasattr(self,'tstmid')):
                BT.stmid=self.tstmid
            else:
                BT.stmid='undef'
        else:
            BT=BestTrk()
            BT.stmid='undef'

        return(BT)



    def GetAidTrks(self,aid,stm2id=None,stm1id=None,verb=0):


        if(stm2id == None and stm1id != None): stm2id=stm1idTostm2id(stm1id)
        if(stm1id == None and stm2id != None): stm1id=stm2idTostm1id(stm2id)

        try:
            trks=self.aidtrks[aid,stm2id]
        except:
            trks={}


        if(len(trks) == 0):
            AT=AidTrk()
            AT.aid=aid
            AT.stmid=stm1id
            return(AT)

        dtgs=trks.keys()
        dtgs.sort()

        AT=AidTrk(dtgs,trks)
        AT.aid=aid
        AT.stmid=stm1id

        return(AT)


    def getBestTrks(self,stm1id):


        try:
            btcs=self.bts
        except:
            btcs=None

        if(btcs != None):
            dtgs=btcs.keys()
            BT=BestTrk(dtgs,btcs)
            BT.stmid=stm1id
        else:
            BT=BestTrk()

        return(BT)



    def GetAidStmids(self,taid):

        stmids=[]

        try:
            stm2ids=self.aidstms[taid]
        except:
            stm2ids=[]

        for tstm in stm2ids:
            stm1id=self.getAidStm1idFromStm2id(taid,tstm)
            if(stm1id != None):
                stmids.append(stm1id)

        stmids=self.uniq(stmids)

        return(stmids)


    def GetAidCards(self,aid,stm1id):

        try:
            stm2ids=self.stm1ids[stm1id.lower()]
        except:
            stm2id=stm1idTostm2id(stm1id.lower())
            stm2ids=[stm2id]

        stm2ids.sort()

        allcards={}

        for stm2id in stm2ids:
            try:
                acards=self.aidcards[aid,stm2id]
            except:
                acards={}

            allcards=self.DictAdd(allcards,acards,priority=1)

        return(allcards)



    def GetEaids(self,model,dtg=None,ncepSource='adeck',verb=0):

        iaids=self.aids
        eaids=[]
        if(model == 'esrl'):
            for iaid in iaids:
                if(verb): print 'iaid ',iaid
                if( (iaid[0:2].upper() == 'F8' and iaid[2:4].isdigit()) or iaid[0:4].upper() == 'F8EM' ):
                    eaids.append(iaid)

        elif((model == 'ncep' or model == 'nhc') and mf.find(ncepSource,'adeck') ):
            for iaid in iaids:
                if(verb): print 'iaid ',iaid
                if( (iaid[0:2].upper() == 'AP' and iaid[2:4].isdigit()) or iaid.upper() == 'AC00'):
                    eaids.append(iaid)

        elif(mf.find(model,'cmc') and ncepSource == 'adeck'):
            for iaid in iaids:
                if(verb): print 'iaid ',iaid
                if( (iaid[0:2].upper() == 'CP' and iaid[2:4].isdigit()) or iaid.upper() == 'CC00'):
                    eaids.append(iaid)

        else:
            for iaid in iaids:
                if(verb): print 'iaid ',iaid
                if(iaid != 'ecmt' and iaid != 'ecfx' and iaid != 'edet' and iaid != 'eanl' ):
                    eaids.append(iaid)

        eaids.sort()

        self.ensembleAids=eaids

        return(eaids)


    def GetDetaid(self,model,dtg,ncepSource='adeck',verb=0):

        iaids=self.aids

        if(model == 'esrl'):
            daid=None
            sdaids=['f9em','f8em']
            for iaid in iaids:
                for sdaid in sdaids:
                    if(iaid == sdaid):
                        daid=sdaid

        elif(model == 'ncep' and mf.find(ncepSource,'adeck') ):
            daid=None
            sdaids=['avno','avni']
            for iaid in iaids:
                for sdaid in sdaids:
                    if(iaid == sdaid):
                        daid=sdaid

        elif(model == 'ukmo'):
            daid=None
            sdaids=['ukm','egrr']
            for iaid in iaids:
                for sdaid in sdaids:
                    if(iaid == sdaid):
                        daid=sdaid


        elif(model == 'cmc' and ncepSource == 'adeck'):
            daid=None
            sdaids=['cmc']
            for iaid in iaids:
                for sdaid in sdaids:
                    if(iaid == sdaid):
                        daid=sdaid

        else:
            daid='edet'

        self.deterministicAid=daid
        return(daid)



    def writeAcards(self,taids=None,tstms=None,
                    tdir='/tmp',
                    odtgs=None,
                    dowrite=0,
                    tag=None,
                    aliases=None,
                    verb=0):

        if(taids == None):
            taids=self.aids
        if(tstms == None):
            tstms=self.stm2ids


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



        cards=[]

        for tstm in tstms:

            if(tag != None):  cards=[]

            for taid in taids:

                otaid=taid
                if(aliases != None):
                    for (iname,oname) in aliases:
                        if(taid.upper() == iname.upper()): otaid=oname.upper()

                acards=self.aidcards[taid,tstm]

                dtgs=acards.keys()
                dtgs.sort()

                for dtg in dtgs:
                    acds=acards[dtg]
                    for acd in acds:

                        acd=corrVmaxPmin(acd)
                        # the b2id in the adeck card is NOT changed, just the stm2id
                        # do the conversion here
                        #
                        b2id=acd[0:2]
                        b2id=basin2Chk(b2id)
                        acd=b2id+acd[2:]
                        if(aliases != None):
                            acd=acd.replace(taid.upper(),otaid)
                        if(verb): print acd[0:-1]
                        cards.append(acd)

                stm2id=tstm

                if(tag == None):
                    fpath="%s/a%s_%s.dat"%(tdir,stm2id.replace('.',''),otaid.lower())
                    MF.WriteList2File(cards,fpath,verb=1)

            if(tag != None):
                fpath="%s/a%s_%s.dat"%(tdir,stm2id.replace('.',''),tag)
                MF.WriteList2File(cards,fpath,verb=1)


class AdeckFromCards(Adeck):
    
    distminHIT=180.0
    distminHIT9X=300.0

    def __init__(self,acards,
                 mD=None,
                 dtgopt=None,
                 taids=None,
                 verb=0,warn=1,doVD=0,
                 skipcarq=1,
                 undef=-9999.,
                 chkb2id=1,
                 mDp1=None,
                 adyear=None,
                 adyearp1=None,
                 dofilt9x=0,
                 prependAid=None,
                 aliases=None):

        

        self.dofilt9x=dofilt9x
        
        self.adyear=adyear
        self.adyearp1=adyearp1

        self.cards=acards
        self.dtgopt=dtgopt
        self.taids=taids
        self.verb=verb
        self.warn=warn
        self.skipcarq=skipcarq
        self.undef=undef
        self.chkb2id=chkb2id
        self.aliases=aliases
        self.prependAid=prependAid

        self.initVars()
        self.initAdeck()


    def initVars(self,dob2idchk=0):

        self.dob2idchk=dob2idchk

        self.stm2ids=[]
        self.stm1ids=[]

        self.dtgs=[]
        self.aids=[]

        self.stmdtgs={}
        self.aiddtgs={}
        self.aidstms={}
        self.aidcards={}
        self.aidtaus={}
        self.aidtrks={}
        self.adeckyears=[]
        self.adeckbasins=[]





class Adeck2(Adeck):

    """ single adeck2 for a single aid single storm --  adeck2S() makes a set of adeck2
    """

    def __init__(self,acards,
                 mD2=None,
                 skipcarq=1,
                 undef=-9999.,
                 chkb2id=1,
                 dofilt9x=0,
                 verb=0,
                 warn=1,
                 # -- not used
                 aliases=None,
                 dtgopt=None,
                 taids=None,
                 tstmid=None,
                 corrTauDisCont=0,
                 corrTauInc=6,
                 ):

        if(dtgopt != None):
            self.tdtgs=dtgs=mf.dtg_dtgopt_prc(dtgopt,ddtg=6)

        if( (taids != None) and (type(taids) is not(ListType)) ):
            taids=[taids]

        if(mD2 == None):
            print 'EEEE(Adeck2.__init__): must set mD2 when making Adeck2...sayounara...'
            sys.exit()
            
        self.mD2=mD2
        (mdtrk,mddtgs)=mD2.getMDtrk()

        self.cards=acards
        self.dofilt9x=dofilt9x
        
        self.dtgopt=dtgopt
        self.taids=taids
        self.verb=verb
        self.warn=warn
        self.skipcarq=skipcarq
        self.undef=undef
        self.chkb2id=chkb2id
        self.aliases=aliases

        self.corrTauDisCont=corrTauDisCont
        self.corrTauInc=corrTauInc

        self.initVars()
        self.initAdeck()
        
        # -- check if aid dtgs in storm dtgs:
        #
        AidDtgsInStormDtgs=0
        for adtg in self.dtgs:
            if(adtg in mddtgs): 
                AidDtgsInStormDtgs=1
                break
            
        if(not(AidDtgsInStormDtgs)):
            print 'WWW(Adeck2.__init__): adeck dtgs not in storm dtgs...return None for tstmid: ',tstmid,' taid: ',self.aids
            self.AidDtgsInStormDtgs=AidDtgsInStormDtgs
            return
        
        # -- let the initializer set the best track bts
        #
        aid=self.aids[0]
        stm2id=self.stm2ids[0]
        
        # -- case for 13p.2015 jt adeck with 12s.2015 cards...
        #
        if(tstmid != None):
            (snum,b1id,year,b2id,tstm2id,tstm1id)=getStmParams(tstmid)
            
        self.addTau0(aid,stm2id,mdtrk,mddtgs)
        try:
            self.ats=self.aidtrks[aid,stm2id]
        except:
            print 'WWW(Adeck2.__init__) -- no aidtrks for aid: ',aid,' stm2ids: ',stm2id,' set to {} and press...'
            self.aidtrks[aid,stm2id]={}
            self.ats=self.aidtrks[aid,stm2id]
        
        if(tstmid != None):
            self.tstmid=tstmid
        else:
            self.tstmid=self.stm1ids[0]
            
        self.chkTauContinuity(dtau0=corrTauInc,verb=verb)
        
        
        #self.keepObjVars=['dtgs','aidcards','aiddtgs','taid','tstmid']   # for full listing
        self.keepObjVars=['dtgs','taid','tstmid']   # smaller 352K v 1069K for 6 aids 31w.13 ~ 30% of that for full listing
        self.keepObjClss=['AT']                     # smaller yet...
        
    def chkTauContinuity(self,dtau0=6,warn=0,verb=0):
        
        bypassAids=['jtwc','clip','jus1','jus5','ofcl','jgs5','jgs1','hunt','hpac','ecs1','ecs5','c120','avs5','xtrp','wrng',
                    'uks5','uks1','strt','st5d','sbam','nvs5','nvs1','mbam','recr','sfxx','jas5','gfs5','fbam','drcl','clim',
                    'jas1','gfs1','avs1','s5xx','gfdl','bams','clp5','mrcl','shfr','bamd','bamm','ngx','ofcp','bcd5','wbs1','wbs5',
                    'stfd','stid']
        
        bypassAids=[]
        
        def getDtau(taus):
            """ find dtau in list of taus
            """
            if(len(taus) == 1):
                rc=1
                dtau=dtau0
                btau=taus[0]
                etau=taus[0]
                
            elif(len(taus) <= 2): 
                rc=1
                dtau=dtau0
                btau=taus[0]
                etau=taus[1]
                
            else:
                dtaus=[]
                for n in range(1,len(taus)):
                    tdtau=taus[n]-taus[n-1]
                    dtaus.append(tdtau)
                    
                dtaus=mf.uniq(dtaus)
                
                # -- pick smallest
                #
                dtau=dtaus[0]
                
                if(len(dtaus) == 1 and dtau == 24):
                    rc=0
                    dtau=12
                elif(len(dtaus) > 1 and dtau > 0):
                    rc=0
                else:
                    rc=1
                    
                btau=taus[0]
                etau=taus[len(taus)-1]
                
            #if(rc == 0): print 'TTTTT',taus
                    
            return(rc,btau,etau,dtau)

        def fillTrkTauGaps(dtau,aid,stm,dtg,verb=0):
            itrk=self.aidtrks[aid,stm][dtg]

            (jtrk,itaus)=self.FcTrackInterpFill(itrk, dtx=dtau, npass=0, dovmaxSmth=0, 
                                                verb=verb, doExtrap=0,
                                                idtmax=6)            
            jtaus=jtrk.keys()
            jtaus.sort()
            
            if(verb): 
                print 'III[adCL.Adeck2.fillTrkTauGaps()] -- filling tau gaps for aid: %8s'%(aid),' stm: ',stm,' dtg: ',dtg,' len(itaus): %3d'%(len(itaus)), 'dtau: %2d'%(dtau),' itaus (input): ',itaus
                for jtau in jtaus:
                    print 'jjjjjjjjjjjjjjjjj',jtau,jtrk[jtau]
            
            self.aidtrks[aid,stm][dtg]=jtrk
            self.aidtaus[aid,stm,dtg]=jtaus
            
        for aid in self.aids:
            for stm in self.aidstms[aid]:
                for dtg in self.aiddtgs[aid,stm]:
                    taus=self.aidtaus[aid,stm,dtg]
                    taus.sort()
                    (rc,btau,etau,dtau)=getDtau(taus)
                    self.aidtausStatus[aid,stm,dtg]=(rc,btau,etau,dtau)
                    if(rc == 0 and self.corrTauDisCont and not(aid in bypassAids)):

                        if(dtau > dtau0 and (warn or verb)):
                            print 'WWW Adeck2.chkTauContinuity  dtau > dtau0 (%d) '%(dtau0),' for aid,stm,dtg: ',aid,stm,dtg,' set to dtau0...taus: ',taus
                            dtau=dtau0
                        fillTrkTauGaps(dtau,aid,stm,dtg,verb=verb)

    def addTau0(self,aid,stm2id,mdtrk,mddtgs,verb=0):

        for dtg in self.dtgs:
            try:
                taus=self.aidtaus[aid,stm2id,dtg]
            except:
                print 'WWW(Adeck2.addTau0) -- no taus for key: ',aid,stm2id,dtg,'press....'
                continue

            if(taus[0] != 0):
                atrks=self.aidtrks[aid,stm2id][dtg][taus[0]]
                if(dtg in mddtgs):
                    mdt=mdtrk[dtg]
                else:
                    print 'EEEEEEEEEE(Adeck2.addTau0): ',dtg,' not in: ',mddtgs[0],' to ',mddtgs[-1],\
                          'for aid: ',aid,' stm2id: ',stm2id
                    continue
                lat0=mdt[0]
                lon0=mdt[1]
                vmax0=mdt[2]
                pmin0=mdt[3]
                mtrk=(lat0,lon0,vmax0,pmin0,None,None,None)
                self.aidtrks[aid,stm2id][dtg][0]=mtrk
                self.aidtaus[aid,stm2id,dtg].append(0)
                if(verb): print 'ttt',dtg,taus,aid,stm2id,atrks,mtrk
        

    def makeVDs(self):
        
        from vdVM import MakeVdeckS
        VDs=MakeVdeckS(self.BT, self.AT)
        return(VDs)




class Bdeck2(MFbase):

    """ single bdeck2 for a single storm -- uses mdeck2 in mD2
    """
    
    def __init__(self,mD2,
                 verb=0,
                 ):


        #mD2.ls()
        if(mD2 == None): 
            print 'WWW(adCL.Bdeck2): no bd2 return None...should NOT get here from makeAdeck2s...'
            return(None)
        (bts,bdtgs)=mD2.getMDtrk() 
        self.stmid=mD2.stm1id
        self.stm1id=mD2.stm1id
        self.bts=bts
        self.keepObjVars=['stmid','stm1id']                       # smaller 352K v 1069K for 6 aids 31w.13 ~ 30% of that for full listing
        self.keepObjClss=['BT']
        
        self.BT=self.getBestTrk()
        
        #self.setObjVarsNone()

    def getBestTrk(self):

        from tcCL import BestTrk2
        
        try:
            btcs=self.bts
        except:
            btcs=None

        if(btcs != None):
            dtgs=btcs.keys()
            BT=BestTrk2(dtgs,btcs)
            
            if(hasattr(self,'stmid')):
                BT.stmid=self.stmid
            else:
                BT.stmid='undef'
        else:
            BT=BestTrk2()
            BT.stmid='undef'

        return(BT)
        
    



class Adeck2s(Adeck):

    """ make adeck2s to put cards through Adeck QC -- the getAD2s makes the actual Adeck2
    """
    
    def __init__(self,tstmid,adeckpathmasks=None,acards=None,
                 mD2=None,
                 tD=None,
                 skipcarq=1,
                 undef=-9999.,
                 chkb2id=1,
                 dofilt9x=0,
                 verb=0,
                 warn=1,
                 doVD=0,
                 # -- not used
                 aliases=None,
                 dtgopt=None,
                 taids=None,
                 prependAid=None,
                 corrTauDisCont=1,
                 corrTauInc=6,
                 ):
        
        self.tstmid=tstmid
        
        # -- set adyear and adyearp1 to handle storms crossing basin-year
        #
        self.adyear=tstmid.split('.')[1]
        self.adyearp1=str(int(self.adyear)+1)
        
        if(dtgopt != None):
            self.tdtgs=dtgs=mf.dtg_dtgopt_prc(dtgopt,ddtg=6)

        if( (taids != None) and (type(taids) is not(ListType)) ):
            taids=[taids]

        self.dofilt9x=dofilt9x
        
        self.verb=verb
        self.warn=warn
        self.skipcarq=skipcarq
        self.undef=undef
        self.chkb2id=chkb2id
        self.prependAid=prependAid
        self.aliases=aliases

        # -- not used
        #
        self.dtgopt=dtgopt
        self.taids=taids
        self.badNoData=0
        self.corrTauDisCont=corrTauDisCont
        self.corrTauInc=corrTauInc
        

        # -- initialize vars
        #
        self.initVars()

        # -- get acards
        #
        if(adeckpathmasks != None):
            MF.sTimer("adeck2s-glob-adecks")
            adeckpaths=[]
            if(type(adeckpathmasks) is ListType):
                for adeckpathmask in adeckpathmasks:
                    adeckpaths=adeckpaths+glob.glob(adeckpathmask)
            else:
                adeckpaths=adeckpaths+glob.glob(adeckpathmasks)
            self.initAdeckPaths(adeckpaths)
            MF.dTimer("adeck2s-glob-adecks")
            
        elif(acards != None):
            if(type(acards) is not(ListType)): 
                self.cards=acards.split('\n')
            else:
                self.cards=acards
            
        else:
            print 'EEE adCL.Adeck2s-- have to set adeckpathmasks OR acards',acards
            self.badNoData=1
            return

        # -- init adecks
        #
        self.initAdeck()
        
        # -- put mdeck2 and TcData
        #
        if(mD2 == None):
            if(verb): print 'not doing mD2 and tD in Adeck2s'
            return
        else:
            self.mD2=mD2
            self.tD=tD
        
    def initVars(self,dob2idchk=0):
        """reduced vars because we only use the origin Adeck to QC the cards
"""
        self.dob2idchk=dob2idchk

        self.adeckyears=[]
        self.adeckbasins=[]

        self.aids=[]
        self.aidcards={}
        
    def initAdeck(self,skipcarq=1,nlenmin=6,nlenmax=-999,filtHiFreq=1,maxDtau=6):

        """  updated from Adeck() to only QC cards and dump into aidcards by stm2id
"""

        ncards=1
        for card in self.cards:
            tt=card.split(',')
            ntt=len(tt)
            
            # -- check for blank card
            #
            if(ntt <= 1):
                continue

            # -- check for short cards
            #
            if(ntt <= nlenmin):
                print 'WWW short adeck card # ',ncards,card[:-1]
                continue

            #  -- check for long cards -- problem on jet/nccs in io from marchok tracker
            #
            if(nlenmax > 0 and ntt > nlenmax):
                print 'WWW LONG  adeck card # ',ncards,card[:-1]
                continue


            # -- get bid, dtg
            #
            rc=self.makeBidDtg(tt,card)
            if(rc == None): 
                if(self.warn): print 'WWW problem in makeBidDtg card: ',card
                continue
            
            (dtg,b2id,bnum,byear)=rc

            # -- get aid
            #
            (gotaid,aidin,card)=self.makeAid(tt,card)
            if(hasattr(self,'prependAid')):
                if(self.prependAid != None):
                    aid="%1s%s"%(self.prependAid,aidin)
                else:
                    aid=aidin
            else:
                aid=aidin    
                
            if(self.aliases != None):
                try:
                    aidout=self.aliases[aidin.upper()]
                    card=card.replace(aidin.upper(),aidout,1)
                except:
                    None

            if(gotaid == 0): continue

            # -- get posit list
            #
            (itau,iposit)=self.makeIposit(tt,card,ncards,ntt,aid=aid)

            # -- filter out hi-frequency, e.g., hwrf in 2014 hourly 0-9 then 3 hourly
            #
            if(filtHiFreq and itau != None):
                if(itau%maxDtau != 0): continue

            if(itau == None): continue

            b2id=basin2Chk(b2id)

            # -- put correct 2-char basin in the input card
            #
            card=b2id+card[2:]
            
            self.append2KeyDictList(self.aidcards,(aid,self.tstmid),dtg,card)
            self.appendList(self.aids,aid)
            ncards=ncards+1

        # --- uniq
        #
        self.aids=self.uniq(self.aids)
        
    #eeeeeeeeeeeeeeeee end of initAdeck methed
    
    def getAD2s(self,tstmid,doVD=0):
        
        ad2s={}
        #aidbtcs={}
        
        for aid in self.aids:

            #(bts,bdtgs)=mD2.getMDtrk()  
            #aidbtcs[tstmid]=(bts,bdtgs)
            #(bts,bdtgs)=aidbtcs[tstmid]
            
            acards=[]
            adtgs=self.aidcards[aid,tstmid].keys()
            adtgs.sort()
            
            for adtg in adtgs:
                ncards=len(self.aidcards[aid,tstmid][adtg])
                for n in range(0,ncards):
                    acard=self.aidcards[aid,tstmid][adtg][n]
                    acards.append(acard)

            ad2=Adeck2(acards, 
                       mD2=self.mD2,
                       skipcarq=self.skipcarq,
                       undef=self.undef,
                       chkb2id=self.chkb2id,
                       dofilt9x=self.dofilt9x,
                       verb=self.verb,
                       warn=self.warn,
                       tstmid=tstmid,
                       corrTauDisCont=self.corrTauDisCont,
                       corrTauInc=self.corrTauInc,
                       ) 

            
            ad2.taid=aid
            ad2.tstmid=tstmid
            AT=ad2.getAidTrk()
            ad2.AT=AT

            if(doVD):
                VDs=ad2.makeVDs()
                ad2.VDs=VDs
                
            # -- set vars to None if Adeck2 has keepObjVars
            #
            ad2.setObjVarsNone()
    
            # -- test if ad2 made -- for cases of no adeck AND a bdeck
            #
            key="%s_%s"%(aid,tstmid)
            if(hasattr(ad2,'AidDtgsInStormDtgs')):
                if(ad2.AidDtgsInStormDtgs):
                    ad2s[key]=ad2
            else:
                ad2s[key]=ad2
                
                
        return(ad2s)
                
class Adeck2NoLoad(Adeck):
    
    def __init__(self,BT,
                 skipcarq=1,
                 undef=-9999.,
                 chkb2id=1,
                 dofilt9x=0,
                 verb=0,
                 warn=1,
                 # -- not used
                 aliases=None,
                 dtgopt=None,
                 taids=None,
                 ):


        # make adeck cards using the best track
        #
        acards=[]
        dtgs=BT.btrk.keys()
        dtgs.sort()
        for dtg in dtgs:
            rc=BT.btrk[dtg]
            (lat,lon,vmax,pmin)=rc[0:4]
            trk={}
            trk[0]=(lat,lon,vmax,pmin)
            acds=MakeAdeckCards('noload',dtg,trk,BT.stmid)
            acards.append(acds[0])

        self.cards=acards
        self.dofilt9x=dofilt9x
        
        self.dtgopt=dtgopt
        self.taids=taids
        self.verb=verb
        self.warn=warn
        self.skipcarq=skipcarq
        self.undef=undef
        self.chkb2id=chkb2id
        self.aliases=aliases

        self.initVars()
        self.initAdeck()
                
        # -- let the initializer set the best track bts
        #
        aid='noload'
        if(len(self.stm2ids) > 0):
            stm2id=self.stm2ids[0]
            self.ats=self.aidtrks[aid,stm2id]
            atdtgs=self.ats.keys()
            stm1id=self.stm1ids[0]
            atdtgs.sort()
        else:
            print 'WWW(adCL.Adeck2NoLoad()): no stm2ids in adeck use BT.stmid & BT.dtgs...'
            stm1id=BT.stmid
            rc=getStmParams(stm1id)
            stm2id=rc[4]
            atdtgs=BT.dtgs
            atdtgs.sort()
        
        # -- no set initial lat to -99 so no cases are used...
        #
        for dtg in atdtgs:
            self.ats[dtg]={0:[-99.9,-99.9]}
        
        self.tstmid=stm1id
        
        #self.keepObjVars=['dtgs','aidcards','aiddtgs','taid','tstmid']   # for full listing
        self.keepObjVars=['dtgs','taid','tstmid']


#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc -- AdeckFixMd2
#

class AdeckFixMd2(Adeck):   


    def makeBidDtg(self,tt,card):

        b2id=tt[0].strip()
        bnum=tt[1].strip()

        if(b2id == '**'):
            b2id='IO'

        elif(b2id == 'SI'):
            b2id='SH'

        elif(b2id.isdigit()):
            print 'WWW -- md2 -- gooned up acard: 2-char basin is a number: ',card[:-1],' ...' ; return(None)

        if(not(self.isValidB2id(b2id)) and self.chkb2id):
            print 'WWW  -- md2 -- gooned up acard: 2-char basin is NOT standard: ',card[:-1],' ...' ; return(None)

        #  check for unspecified bnum, e.g., when b2id == '**'
        #
        if(len(bnum) == 2):

            # -- handle new [A-Z][0-9] for 9X
            #
            bnum1=bnum[0].upper()
            if(ord(bnum1) >= 65 and ord(bnum1) <= 90):
                bnum=90+int(bnum[1])
                bnum=str(bnum)

            try:      int(bnum)
            except:   print 'WWW bad acard: ',card[:-1],' bnum not defined...onward...' ; return(None)

        # -- case when 3-char id in the basin id in the 'sink' format
        #
        elif(len(bnum) == 3):
            try:
                ibnum=int(bnum[0:2])
                bnum=bnum[0:2]
            except:
                print 'WWW 333333 bad acard(AdeckFixMd2): ',bnum,card[:-1],' bnum not defined...onward...' ; return(None)

        # -- case when 1-char id in the basin id in the 'sink' format
        #
        elif(len(bnum) == 1):
            try:
                ibnum=int(bnum[0])
                bnum="%02d"%(ibnum)
                print 'WWW single bnum: ',bnum,'stm2id: ',stm2id
            except:
                print 'WWW 111111 bad bnun in acard: ',bnum,card[:-1],' bnum not defined...onward...' ; return(None)

        # -- filter out 8X storms
        #
        if(int(bnum) >= 80 and int(bnum) <= 89): return(None)

        # -- check if adeck uses sss.yyyy form of storm id vice standard 2-char stm id
        #

        if(len(bnum.split('.')) == 2):
            bn=bnum.split('.')[0]
            b1=bn[2]
            bn=bn[0:2]
            by=bnum.split('.')[1]
            bnum=bn

        dtg=self.setDtgNCard(tt)

        byear=dtg[0:4]
        # -- handle shem...
        #
        stm2id="%s%s.%s"%(b2id,bnum,byear)
        if(isShemBasinStm(stm2id)):  byear=getShemYear(dtg)

        return(dtg,b2id,bnum,byear)







#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc -- AdeckSink
#

class AdeckSink(Adeck):

    """ adeck made from 'sink' version of atcf output from gettrk_gen.x
    """
    

    def __init__(self,adeckpathmasks,mD=None,dtgopt=None,taids=None,verb=0,warn=1,
                 skipcarq=1,
                 dofilt9x=0,
                 undef=-9999.,
                 chkb2id=0,
                 aliases=None):
        
        from w2local import W2
        w2=W2()

        self.lf=w2.SetLandFrac()
        self.getlf=w2.GetLandFrac

        # -- dectect if mask is a list...
        #
        if(type(adeckpathmasks) is ListType):
            adeckpaths=[]
            for adeckpathmask in adeckpathmasks:
                adeckpaths=adeckpaths+glob.glob(adeckpathmask)
        else:
            adeckpaths=glob.glob(adeckpathmasks)


        if(dtgopt != None):
            self.tdtgs=dtgs=mf.dtg_dtgopt_prc(dtgopt,ddtg=6)

        if( (taids != None) and (type(taids) is not(ListType)) ):
            taids=[taids]

        self.mD=mD
        self.adecks=adeckpaths
        self.dtgopt=dtgopt
        self.taids=taids
        self.verb=verb
        self.warn=warn
        self.skipcarq=skipcarq
        self.undef=undef
        self.aliases=aliases
        self.chkb2id=chkb2id
        self.dofilt9x=dofilt9x

        self.initVars()
        self.initAdeckPaths(adeckpaths)
        self.initAdeck(nlenmax=31)

        del self.lf
        del self.getlf

    def setAidNCard(self,tt):
        aid=tt[5].strip()
        return(aid)

    def setDtgNCard(self,tt):
        dtg=tt[3].strip()
        return(dtg)



    def makeIposit(self,tt,card,ncards,ntt,aid=None):

        tau=tt[6].strip()
        itau=int(tau)

        clat=tt[7].strip()
        clon=tt[8].strip()

        if(tt[9].strip() == "***" or tt[9].strip() == "****"):
            vmax=-999
        else:
            vmax=float(tt[9])

        # -- check if vmax==0
        # 
        if(vmax == 0.0): vmax=self.undef
        
        try:
            (alat,alon)=Clatlon2Rlatlon(clat,clon)[0:2]
        except:
            print 'WWW gooned up clat,clon: ',ncards,card[0:-1],ntt
            return(None,None)

        if(alat == 0.0 and alon == 0.0 and (vmax == 0.0 or vmax == self.undef) ):
            if(self.verb): print 'NOLOAD: ',card[:-1]
            return(None,None)

        try:
            pmin=float(tt[10])
        except:
            pmin=self.undef

        if(pmin == 0.0): pmin=self.undef

        if(tt[18].strip() == "****"):
            poci=-999
        else:
            poci=float(tt[18].strip())

        try:    roci=float(tt[19].strip())
        except: roci=float(tt[19].strip())

        try:    rmax=float(tt[20].strip())
        except: rmax=float(tt[20].strip())

        try:    dir=float(tt[21].strip())
        except: dir=self.undef

        try:    spd=float(tt[22].strip())
        except: spd=self.undef

        try:    cpsB=float(tt[23].strip())
        except: cpsB=self.undef

        try:    cpsVTl=float(tt[24].strip())
        except: cpsVTl=self.undef

        try:    cpsVTu=float(tt[25].strip())
        except: cpsVTu=self.undef

        try:    z8mean=float(tt[26].strip())
        except: z8mean=self.undef

        try:    z8max=float(tt[27].strip())
        except: z8max=self.undef

        try:    z7mean=float(tt[28].strip())
        except: z7mean=self.undef

        try:    z7max=float(tt[29].strip())
        except: z7max=self.undef

        name=tt[30].strip()

        # -- put lf (landfrac) into the posit
        #

        alf=self.getlf(self.lf,alat,alon)
        # -- bug in doc on marchok 'sink' format lower then upper for cpsV
        # -- doc has upper/lower; code has it other way

        iposit=(alat,alon,vmax,pmin,alf,poci,roci,rmax,dir,spd,cpsB,cpsVTl,cpsVTu,z8mean,z8max,z7mean,z7max)

        return(itau,iposit)



    def GetAidStruct(self,aid,stm2id=None,stm1id=None,verb=0):

        if(stm2id == None and stm1id != None): stm2id=stm1idTostm2id(stm1id)
        if(stm1id == None and stm2id != None): stm1id=stm2idTostm1id(stm2id)

        try:
            trks=self.aidtrks[aid,stm2id]
        except:
            trks={}


        if(len(trks) == 0):
            AT=AidStruct()
            AT.aid=aid
            AT.stmid=stm1id
            return(AT)

        dtgs=trks.keys()
        dtgs.sort()

        AT=AidStruct(dtgs,trks)
        AT.aid=aid
        AT.stmid=stm1id

        return(AT)



#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc -- AdeckGen
#

class AdeckGen(Adeck):


    def __init__(self,dtgopt,modelopt,basinopt,
                 taids=None,verb=0,warn=1,
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


    def initVars(self,dob2idchk=0):


        self.dob2idchk=dob2idchk

        self.dtgs=[]
        self.aids=[]

        self.stmdtgs={}
        self.aiddtgs={}
        self.aidstms={}
        self.aidcards={}
        self.aidtaus={}
        self.aidtrks={}



    def initAdeckPaths(self):

        bcards={}
        cards=[]
        basins=[]


        adecks=[]
        oadecks=[]

        for dtg in self.tdtgs:

            year=dtg[0:4]

            sdir="%s/esrl/%s"%(AdeckBaseDir,year)

            for model in self.models:
                for basin in self.basins:
                    #sdir="/dat3/tc/tmtrkN/%s/%s"%(dtg,model)
                    #admask="%s/w2flds/%s.sink.%s.%s.%s.txt"%(sdir,self.trktype,basin,dtg,model)
                    admask="%s/%s.sink.%s.%s.%s.txt"%(sdir,self.trktype,basin,dtg,model)
                    adecks=adecks+glob.glob(admask)
                    if(self.verb): print 'adecks(tcgen): ',adecks

            for adeck in adecks:
                try:
                    siz=os.path.getsize(adeck)
                    if(siz > 0): oadecks.append(adeck)
                except:
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

            if(cards == None):
                return
            else:
                cards=cards+ttt

            self.addList2DictList(bcards,basin,cards)

        basins=self.uniq(basins)

        self.basins=basins
        self.bcards=bcards
        self.adecks=oadecks


    def initAdeck(self):

        undef=-9999.
        from tcVM import Clatlon2Rlatlon

        for basin in self.basins:

            ncards=1

            for card in self.bcards[basin]:

                tt=card.split(',')
                ntt=len(tt)
                
                #TG, 0001, 2009081212_F000_155N_1280E_FOF, 2009081212, 03, FIM8, 000, 155N, 1280E,  21, 1008, XX,  34, NEQ, 0000, 0000, 0000, 0000,
                # 0     1,                              2,          3,  4,    5,   6,    7,     8,   9,   10, 11,  12,  13,   14,   15,   16,   17,
                #...1009,   93, -99, 309,  45, -99, -9999, -9999,   81,   82,   64,   66, 0001 
                #     18,   19,  20,  21,  22,  23,    24,    25,   26,   27,   28,   29,    30


                if(ntt != 31):
                    print '''WWW invalid 'sink' adeck card# ''',ncards,card[:-1],len(tt)
                    continue

                # -- parsing
                #

                g2id=tt[0].strip()

                # -- only deal with gen tcs ... 'TG'
                #
                #if(g2id != 'TG'): continue

                snum=tt[1].strip()
                fofstmid=tt[2].strip()
                dtg=tt[3].strip()

                if(self.dtgopt != None):
                    gotdtg=0
                    for tdtg in self.tdtgs:
                        if(tdtg == dtg):
                            gotdtg=1
                            break
                else:
                    gotdtg=1

                if(gotdtg == 0): continue

                aid="%s%s"%(g2id,snum)
                aid=aid.lower()

                if(self.taids != None):
                    gotaid=0
                    for taid in self.taids:
                        if(aid == taid):
                            gotaid=1
                            break
                else:
                    gotaid=1

                if(gotaid == 0): continue

                tau=tt[6].strip()
                itau=int(tau)

                clat=tt[7].strip()
                clon=tt[8].strip()

                if(tt[9].strip() == "***" or tt[9].strip() == "****"):
                    vmax=-999
                else:
                    vmax=float(tt[9])

                try:
                    (alat,alon)=Clatlon2Rlatlon(clat,clon)
                except:
                    print 'WWW gooned up clat,clon: ',ncards,card[0:-1],ntt
                    continue

                if(alat == 0.0 and alon == 0.0 and (vmax == 0.0 or vmax == undef) ):
                    if(self.verb): print 'NOLOAD: ',card[:-1]
                    continue

                try:
                    pmin=float(tt[10])
                except:
                    pmin=undef

                if(pmin == 0.0): pmin=undef

                if(tt[18].strip() == "****"):
                    poci=-999
                else:
                    poci=float(tt[18].strip())

                roci=float(tt[19].strip())
                rmax=float(tt[20].strip())
                try: dir=float(tt[21].strip())
                except: dir=undef

                try:      spd=float(tt[22].strip())
                except:   spd=undef

                try:      cpsB=float(tt[23].strip())
                except:   cpsB=undef

                try:      cpsVTl=float(tt[24].strip())
                except:   cpsVTl=undef

                try:      cpsVTu=float(tt[25].strip())
                except:   cpsVTu=undef

                try:      z8mean=float(tt[26].strip())
                except:   z8mean=undef

                try:      z8max=float(tt[27].strip())
                except:   z8max=undef

                try:      z7mean=float(tt[28].strip())
                except:   z7mean=undef

                try:      z7max=float(tt[29].strip())
                except:   z7max=undef

                name=tt[30].strip()

                # -- put lf (landfrac) into the posit
                #

                alf=self.getlf(self.lf,alat,alon)
                iposit=(alat,alon,vmax,pmin,alf,poci,roci,rmax,dir,spd,cpsB,cpsVTl,cpsVTu,z8mean,z8max,z7mean,z7max)
                #print iposit


                self.appendList(self.dtgs,dtg)
                self.appendList(self.aids,aid)

                self.appendDictList(self.stmdtgs,basin,dtg)
                self.appendDictList(self.aiddtgs,(aid,basin),dtg)
                self.appendDictList(self.aidstms,aid,basin)
                #self.appendDictList(self.aidtaus,(aid,basin,dtg),itau)
                self.append2KeyDictList(self.aidtaus,(aid,basin),dtg,itau)

                self.append2KeyDictList(self.aidcards,(aid,basin),dtg,card)
                self.append3KeyDictList(self.aidtrks,(aid,basin),dtg,itau,iposit)


                ncards=ncards+1

            self.dtgs=self.uniq(self.dtgs)
            self.aids=self.uniq(self.aids)

            for aid in self.aids:
                for basin in self.basins:
                    try:
                        temp=self.uniq(self.aiddtgs[aid,basin])
                        self.aiddtgs[aid,basin]=temp
                    except:
                        iok=0

            for aid in self.aids:
                self.aidstms[aid]=self.uniq(self.aidstms[aid])

            # reverse sort to pick of the latest dtg, could be a problem for
            # carqs for 9X storms that didn't go to warning, storms don't go from [0-5]X->9X...
            #
            self.dtgs.reverse()
            self.aids.sort()

            nids=len(self.basins)
            self.naids=len(self.aids)
            self.ndtgs=len(self.dtgs)



    def mapAidStmid2BtStmid(self,gdisttol=180.0,verb=0):

        from tcVM import gc_dist
        
        self.map9X2NN={}

        aidstms=self.aiddtgs.keys()
        for aid,stmid in aidstms:
            aiddtgs=self.aiddtgs[aid,stmid]
            for dtg in aiddtgs:
                (astmids,abtcs)=self.getDtg(dtg,dupchk=1)
                for astmid in astmids:
                    (blat,blon)=abtcs[astmid][0:2]
                    taus=self.aidtrks[aid,stmid][dtg].keys()
                    taus.sort()
                    (alat,alon)=self.aidtrks[aid,stmid][dtg][taus[0]][0:2]
                    gdist=gc_dist(blat,blon,alat,alon)
                    if(gdist <= gdisttol):
                        self.map9X2NN[stmid]=astmid

        if(verb): 
            stmids=self.map9X2NN.keys()

            if(len(stmids) > 0):     print ; print 'map9X-NN'
            for stmid in stmids:
                astmid=self.map9X2NN[stmid]
                if(astmid != stmid):
                    print 'HHHHHHH(AD.AdeckGen.mapAidStmid2BtStmid) ',stmid,astmid
            if(len(stmids) > 0):     print

    def relabelAidtrks(self):

        nstmids=[]
        aidtrks={}
        aidtaus={}

        kk=self.aidtrks.keys()

        for aid,stmid in kk:
            try:
                nstmid=self.map9X2NN[stmid]
            except:
                nstmid=stmid

            aidtrks[aid,nstmid]=self.aidtrks[aid,stmid]
            try:
                aidtaus[aid,nstmid]=self.aidtaus[aid,stmid]
            except:
                print 'EEE in AD.relabelAidtrks() for stmid: ',stmid
                sys.exit()
            nstmids.append(nstmid)

        self.stmids=nstmids
        self.aidtrks=aidtrks
        self.aidtaus=aidtaus


    def gettrks(self,basin,dtg,ttau=None,dtau=12):
        """ for AdeckGen aid is the tcgen stmids"""
        trks={}
        for aid in self.aids:

            if(ttau != None):

                try:
                    tt=self.aidtrks[aid,basin][dtg][ttau]
                    taus=self.aidtaus[aid,basin][dtg]
                    trks[aid]={}
                    for tau in taus:
                        if(tau <= ttau and tau%dtau == 0):
                            try:
                                trks[aid][tau]=self.aidtrks[aid,basin][dtg][tau]
                            except:
                                trks[aid][tau]={}
                                trks[aid][tau]=self.aidtrks[aid,basin][dtg][tau]

                except:
                    continue

            else:

                try:
                    taus=self.aidtaus[aid,basin][dtg]
                except:
                    continue

                for tau in taus:
                    if(tau%dtau == 0):
                        try:
                            trks[aid][tau]=self.aidtrks[aid,basin][dtg][tau]
                        except:
                            try:
                                trks[aid][tau]={}
                            except:
                                trks[aid]={}
                                trks[aid][tau]=self.aidtrks[aid,basin][dtg][tau]


        return(trks)



    def getsTDds(self,basin,dtg,ttau,dtau=12,vmaxTD=25.0,vmaxMin=10.0):


        minvmax=1e20
        maxvmax=-1e20

        sTDds={}
        trks=self.gettrks(basin,dtg,ttau,dtau)
        kk=trks.keys()

        for stmid in kk:
            trk=trks[stmid]
            trkttau=trks[stmid][ttau]
            taus=trk.keys()
            taus.sort()
            if(len(taus) == 1):
                vmax=trk[taus[0]][2]
                if(vmax < 0): vmax=vmaxMin
                stdd=(vmax/vmaxTD)
                stddtime=dtau*0.5
                minvmax=maxvmax=vmax
            else:
                stdd=0.0
                stddtime=0.0
                for n in range(1,len(taus)):
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

            sTDds[stmid]=(stdd*(dtau/24.0),stddtime,trkttau[0],trkttau[1],trkttau[2],minvmax,maxvmax)


        return(sTDds)


#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc -- AdeckGenTctrk
#

class AdeckGenTctrk(AdeckGen):


    def __init__(self,tcD,dtgopt,modelopt,mD=None,taids=None,
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



    def initAdeckPaths(self):

        adecks=[]
        oadecks=[]

        for dtg in self.tdtgs:
            year=dtg[0:4]
            sdir="%s/esrl/%s"%(AdeckBaseDir,year)
            for model in self.models:
                admask="%s/w2flds/%s.%s.%s.%s.txt"%(sdir,self.trktype,self.atcftype,dtg,model)
                adecks=adecks+glob.glob(admask)
                if(self.verb): print 'adecks(tctrk): ',adecks

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

            if(cards == None):
                return
            else:
                cards=cards+ttt

        self.cards=cards



    def getStmidDtg(self,dtg,dupchk=0):
        stmid=self.tcD.getStmidDtg(dtg,dupchk=dupchk)
        return(stmid)


    def getStmidFrom3id(self,snum,dtg):
        stmid=self.tcD.getStmidFrom3id(snum,dtg)
        return(stmid)

    def getDtg(self,dtg,dupchk=1):
        (astmids,abtcs)=self.tcD.getDtg(dtg,dupchk=dupchk)
        return(astmids,abtcs)



    def initAdeck(self):


        from tcVM import Clatlon2Rlatlon
        
        def getStmid4Snum(snum,stmids):
            stmid=None
            for stmid in stmids:
                if(snum.upper() == stmid.split('.')[0]):
                    return(stmid)
            return(stmid)

        undef=-9999.

        stmids=[]
        for tdtg in self.tdtgs:
            stmids=stmids+self.getStmidDtg(tdtg,dupchk=0)

        stmids=MF.uniq(stmids)
        self.stmids=stmids

        ncards=1

        for card in self.cards:

            tt=card.split(',')
            ntt=len(tt)

            # --- sink from tcgen mode
            #TG, 0001, 2009081212_F000_155N_1280E_FOF, 2009081212, 03, FIM8, 000, 155N, 1280E,  21, 1008, XX,  34, NEQ, 0000, 0000, 0000, 0000,
            # 0     1,                              2,          3,  4,    5,   6,    7,     8,   9,   10, 11,  12,  13,   14,   15,   16,   17,
            #...1009,   93, -99, 309,  45, -99, -9999, -9999,   81,   82,   64,   66, 0001 
            #     18,   19,  20,  21,  22,  23,    24,    25,   26,   27,   28,   29,    30

            # --- sink from tracker -- no roci/poci/rmax
            #NA, 93A , 2010051800_F000_088N_0574E_93A, 2010051800, 03, ecm2, 162, 148N,  463E,  15, 1005, XX,  34, NEQ, 0000, 0000, 0000, 0000,
            # 0     1,                              2,          3,  4,    5,   6,    7,     8,   9,   10, 11,  12,  13,   14,   15,   16,   17,
            #     34, -999, -99, ***, ***,   2,   -91,    38,  110,  130,  213,  235, INVEST
            #     18,   19,  20,  21,  22,  23,    24,    25,   26,   27,   28,   29,    30

            if(ntt != 31):
                print '''WWW invalid 'sink' adeck card# ''',ncards,card[:-1],len(tt)
                continue

            # -- parsing
            #

            fofstmid=tt[2].strip()
            dtg=tt[3].strip()

            snum=tt[1].strip()
            stmid=self.getStmidFrom3id(snum,dtg)

            #stmid=getStmid4Snum(snum,stmids)
            #if(stmid == None): stmid="%s.9999"%(snum)

            if(self.dtgopt != None):
                gotdtg=0
                for tdtg in self.tdtgs:
                    if(tdtg == dtg):
                        gotdtg=1
                        break
            else:
                gotdtg=1

            if(gotdtg == 0): continue

            aid=tt[5].lower().strip()

            if(self.taids != None):
                gotaid=0
                for taid in self.taids:
                    if(aid == taid):
                        gotaid=1
                        break
            else:
                gotaid=1

            if(gotaid == 0): continue

            tau=tt[6].strip()
            itau=int(tau)

            clat=tt[7].strip()
            clon=tt[8].strip()

            if(tt[9].strip() == "***" or tt[9].strip() == "****"):
                vmax=-999
            else:
                vmax=float(tt[9])

            try:
                (alat,alon)=Clatlon2Rlatlon(clat,clon)[0:2]
            except:
                print 'WWW gooned up clat,clon: ',ncards,card[0:-1],ntt
                continue

            if(alat == 0.0 and alon == 0.0 and (vmax == 0.0 or vmax == undef) ):
                if(self.verb): print 'NOLOAD: ',card[:-1]
                continue

            try:
                pmin=float(tt[10])
            except:
                pmin=undef


            r34ne=r34se=r34sw=r34nw=undef
            r50ne=r50se=r50sw=r50nw=undef
            r64ne=r64se=r64sw=r64nw=undef

            if(int(tt[12]) == 34):
                r34ne=int(tt[14])
                r34se=int(tt[15])
                r34sw=int(tt[16])
                r34nw=int(tt[17])

            elif(int(tt[12]) == 50):
                r50ne=int(tt[14])
                r50se=int(tt[15])
                r50sw=int(tt[16])
                r50nw=int(tt[17])

            elif(int(tt[12]) == 64):
                r64ne=int(tt[14])
                r64se=int(tt[15])
                r64sw=int(tt[16])
                r64nw=int(tt[17])


            if(pmin == 0.0): pmin=undef

            # -- roci,poci not in the tracker kitchen sink???
            #
            if(tt[18].strip() == "****"):
                poci=-999
            else:
                poci=float(tt[18].strip())

            try:     roci=float(tt[19].strip())
            except:  roci=undef

            try:     rmax=float(tt[20].strip())
            except:  rmax=undef

            try:     dir=float(tt[21].strip())
            except:  dir=undef

            try:     spd=float(tt[22].strip())
            except:  spd=undef

            try:     cpsB=float(tt[23].strip())
            except:  cpsB=undef

            try:     cpsVTl=float(tt[24].strip())
            except:  cpsVTl=undef

            try:     cpsVTu=float(tt[25].strip())
            except:  cpsVTu=undef

            try:     z8mean=float(tt[26].strip())
            except:  z8mean=undef

            try:     z8max=float(tt[27].strip())
            except:  z8max=undef

            try:     z7mean=float(tt[28].strip())
            except:  z7mean=undef

            try:     z7max=float(tt[29].strip())
            except:  z7max=undef

            name=tt[30].strip()

            # -- put lf (landfrac) into the posit
            #

            alf=self.getlf(self.lf,alat,alon)
            iposit=(alat,alon,vmax,pmin,alf,poci,roci,rmax,dir,spd,cpsB,cpsVTl,cpsVTu,z8mean,z8max,z7mean,z7max)
            #print iposit

            self.appendList(self.dtgs,dtg)
            self.appendList(self.aids,aid)

            self.appendDictList(self.stmdtgs,stmid,dtg)
            self.appendDictList(self.aiddtgs,(aid,stmid),dtg)
            self.appendDictList(self.aidstms,aid,stmid)

            #self.appendDictList(self.aidtaus,(aid,stmid,dtg),itau)
            self.append2KeyDictList(self.aidtaus,(aid,stmid),dtg,itau)

            self.append2KeyDictList(self.aidcards,(aid,stmid),dtg,card)
            self.append3KeyDictList(self.aidtrks,(aid,stmid),dtg,itau,iposit)

            ncards=ncards+1

        self.dtgs=self.uniq(self.dtgs)
        self.aids=self.uniq(self.aids)

        for aid in self.aids:
            for stmid in self.stmids:
                try:
                    temp=self.uniq(self.aiddtgs[aid,stmid])
                    self.aiddtgs[aid,stmid]=temp
                except:
                    iok=0

        for aid in self.aids:
            self.aidstms[aid]=self.uniq(self.aidstms[aid])

        # reverse sort to pick of the latest dtg, could be a problem for
        # carqs for 9X storms that didn't go to warning, storms don't go from [0-5]X->9X...
        #
        self.dtgs.reverse()
        self.aids.sort()

        nids=len(self.stmids)
        self.naids=len(self.aids)
        self.ndtgs=len(self.dtgs)

        # -- delete the landfrac obj
        #
        del self.getlf
        del self.lf



    def gettrks(self,dtg,ttau=None,endtau=None,dtau=12):
        """ for AdeckGenTctrk -- organized by stmid vice aid """

        trks={}

        # -- if no aids -- no cards -- no trks -- return
        #
        if(len(self.aids) == 0):
            return(trks)

        # -- assume only one aid in a tctrk.sink adeck
        #
        aid=self.aids[0]

        for stmid in self.stmids:

            trks[stmid]={}
            taus=self.aidtrks[aid,stmid][dtg].keys()

            for tau in taus:

                if(ttau != None):
                    try:
                        tt=self.aidtrks[aid,stmid][dtg][ttau]
                        taus=self.aidtaus[aid,stmid][dtg]
                        for tau in taus:
                            if(tau <= ttau and tau%dtau == 0):
                                try:
                                    trks[stmid][tau]=self.aidtrks[aid,stmid][dtg][tau]
                                except:
                                    trks[stmid][tau]={}
                                    trks[stmid][tau]=self.aidtrks[aid,stmid][dtg][tau]
                    except:
                        continue

                else:

                    tautest=0
                    if(endtau != None):
                        if(tau <= endtau): tautest=1
                    else:  tautest=1

                    if(tau%dtau == 0 and tautest):
                        try:
                            trks[stmid][tau]=self.aidtrks[aid,stmid][dtg][tau]
                        except:
                            trks[stmid][tau]={}
                            trks[stmid][tau]=self.aidtrks[aid,stmid][dtg][tau]


        return(trks)








#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc -- AidTrk
#

class AidTrk(MFbase):

    def __init__(self,dtgs=None,trks=None):


        if(dtgs == None):
            self.dtgs=[]
        else:
            self.dtgs=dtgs

        if(trks == None):
            self.atrks=[]
        else:
            # -- convert trks to dict of lists v tuples
            #
            otrks={}
            odtgs=[]
            for dtg in trks.keys():
                odtgs.append(dtg)

                dd=trks[dtg]
                odd={}
                for d in dd.keys():
                    odd[d]=list(dd[d])

                otrks[dtg]=odd

            odtgs=mf.uniq(odtgs)
            self.dtgs=odtgs
            self.atrks=otrks

    def getLatLonVmaxPminFromAtrk(self,atrk,tau):
        rc=atrk[tau]
        lat1=rc[0]
        lon1=rc[1]
        vmax1=rc[2]
        pmin1=rc[3]
        
        return(lat1,lon1,vmax1,pmin1)
    
    def qcMotion(self,latT=30.0,vmaxT=35.0,vmaxM=55.0,
                 stmid=None,aid=None,
                 forspdAdjfact=1.35,
                 forspdMaxTau0=24,
                 verb=0):


        spdflgT={}
        spdtauT={}
        spdflgM={}
        spdtauM={}

        xspdlog=[]

        for dtg in self.dtgs:

            otaus=[]

            taus=self.atrks[dtg].keys()
            taus.sort()
            nt=len(taus)
            atrk=self.atrks[dtg]
            otrk={}

            err=-1

            spdflgT[dtg]=0
            spdtauT[dtg]=-999
            spdflgM[dtg]=0
            spdtauM[dtg]=-999

            if(nt > 0): 
                otaus.append(taus[0])

            for n in range(0,nt):

                course=270
                speed=0.0
                tau0=taus[0]
                tau1=taus[0]

                if(nt > 1):
                    if(n == 0):
                        n0=0
                        n1=1
                    elif(n == nt-1):
                        n0=n-1
                        n1=n
                    else:
                        n0=n
                        n1=n+1

                    tau0=taus[n0]
                    tau1=taus[n1]
                    dtau=tau1-tau0

                    rc0=atrk[tau0]
                    rc1=atrk[tau1]
                    
                    (lat0,lon0,vmax0,pmin0)=self.getLatLonVmaxPminFromAtrk(atrk,tau0)
                    (lat1,lon1,vmax1,pmin1)=self.getLatLonVmaxPminFromAtrk(atrk,tau1)

                    # -- bypass bad; single points
                    #
                    #if(dtau == 0 or (lat0 == lat1 and lon0 == lon1)): continue

                    try:
                        (course,speed,eiu,eiv)=rumhdsp(lat0,lon0,lat1,lon1,dtau)
                    except:
                        print 'EEEEEEEEEEEEEEEEEEEEEEEEEEE in qcSpeed.rumhdsp(lat0,lon0,lat1,lon1,dtau): ',tau0,tau1,lat0,lon0,lat1,lon1,dtau,\
                              ' stmid: ',self.stmid,'aid: ',self.aid,' dtg: ',dtg,' setting speed to 200 to kill off...'
                        speed=200.0

                    # -- similar to tcnavytrk/mf.modues.f  and mf.trackem.f -- allow faster motion in early period
                    #
                    vmaxTcomp=vmaxT
                    if(tau0 <= forspdMaxTau0):
                        vmaxTcomp=vmaxT*forspdAdjfact

                    if(abs(lat0) <= latT and speed >= vmaxTcomp):
                        card="AidTrk(): EEExssive speed in tropics stmid: %s aid: %s dtg: %s tau0: %3d speed: %7.1f lat0: %5.1f  vmaxTcomp: %5.0f"%\
                            (self.stmid,self.aid,dtg,tau0,speed,lat0,vmaxTcomp)
                        print card
                        xspdlog.append(card)

                        err=n0
                        spdflgT[dtg]=1
                        spdtauT[dtg]=tau1


                    if(abs(lat0) > latT and speed >= vmaxM):
                        card="AidTrk(): EEExssive speed in MIDLATS stmid: %s aid: %s dtg: %s tau0: %3d speed: %7.1f lat0: %5.1f  vmaxTcomp: %5.0f"%\
                            (self.stmid,self.aid,dtg,tau0,speed,lat0,vmaxTcomp)
                        print card
                        xspdlog.append(card)

                        err=n0
                        spdflgM[dtg]=1
                        spdtauM[dtg]=tau1

                    if(err >= 0):
                        break

                    else:
                        if(n != n1):
                            otaus.append(taus[n1])


            nto=len(otaus)
            nti=len(taus)
            if(verb): print 'dddd ',dtg,' nto: ',nto,' nti: ',nti
            if(nto < nti):
                for tau in otaus:
                    otrk[tau]=atrk[tau]

                self.atrks[dtg]=otrk
                if(verb): print 'dtg',dtg,tau0,course,speed,lat0,lon0,lat1,lon1,dtau,err

        self.spdflgT=spdflgT
        self.spdtauT=spdtauT
        self.spdflgM=spdflgM
        self.spdtauM=spdtauM

        self.xspdlog=xspdlog

    def lsAT(self,stmid,dtgopt=None):

        dtgs=self.atrks.keys()
        dtgs.sort()

        tdtgs=None
        if(dtgopt != None):
            tdtgs=mf.dtg_dtgopt_prc(dtgopt)
            
        for dtg in dtgs:

            if(tdtgs != None and not(dtg in tdtgs)): continue
            atrk=self.atrks[dtg]
            print
            print stmid,dtg,'aid: ',self.aid
            taus=atrk.keys()
            taus.sort()

            for tau in taus:
                vdtg=mf.dtginc(dtg,tau)
                aa=atrk[tau]
                alat=aa[0]
                alon=aa[1]
                try:
                    r34=aa[4]
                except:
                    r34=None

                if(r34 == None):
                    or34='[-99,-99,-99,-99]'
                else:
                    or34=str(r34)

                (clat,clon)=Rlatlon2Clatlon(alat,alon)
                if(aa[2] != None): ovmax="%3.0f"%(aa[2])
                else: ovmax="---"
                if(aa[3] != None): opmin="%4.0f"%(aa[3])
                else: opmin="____"
                print "%s(%03d) %s %s %s %s %s"%(vdtg,tau,clat,clon,ovmax,opmin,or34)



#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc -- AidStruct
#

class AidStruct(MFbase):

    def __init__(self,dtgs=None,trks=None):

        if(dtgs == None):
            self.dtgs=[]
        else:
            self.dtgs=dtgs

        if(trks == None):
            self.atrks=[]
        else:
            self.atrks=trks


#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc -- AtcfAdeckPaths
#

class AtcfAdeckPaths(MFutils):


    def setGenAdps(self):
        """ simple method to make adps object for 'gen' trackers"""

        self.genprops={}
        for adeck in self.paths:
            (dir,file)=os.path.split(adeck)
            tt=file.split('.')

            # prop=(basin,dtg,atcfname)
            if(len(tt) == 6):
                prop=(tt[2],tt[3],tt[4])
                self.genprops[adeck]=prop





    def __init__(self,dtgopt=None,stmopt=None,adecks=None,verb=0,adecktype='atcf'):
        """adecktype sets type of adeck = atcf|gen to suppoert 'sink' adeck format"""

        # --- genesis adecks; adecktype='gen'
        #

        if(adecktype == 'gen' and adecks != None):

            self.paths=adecks
            self.adecktype=adecktype
            self.setGenAdps()

            return

        # --- atcf adecks
        #
        curdtg=self.dtg()
        if(dtgopt != None):
            dtgs=mf.dtg_dtgopt_prc(dtgopt)
        else:
            dtgs=[curdtg]

        self.stm1ids=[]
        self.path={}
        self.size={}
        self.mtime={}

        # get properties of adecks...if comes in from option
        #
        if(adecks != None):

            self.size={}
            self.mtime={}
            self.paths=adecks

            for adeck in adecks:
                self.size[adeck]=self.GetPathSiz(adeck)
                self.mtime[adeck]=self.PathModifyTime(adeck)

            self.adptype='adecks'


        #
        # get the list of adecks
        #
        else:
            adecks=self.GetAtcfAdecks()
            #self.paths=[]
            #for adeck in adecks:
            #    self.paths.append(adeck)


        if(stmopt != None):

            self.paths=[]

            tstm1ids=MakeStmList(stmopt)

            for tstm1id in tstm1ids:

                tstm2id=stm1idTostm2id(tstm1id)
                adecks=self.GetAtcfAdecks(tstm2id)

                for adeck in adecks:
                    if(verb==0): print 'adeck: ',adeck
                    (dir,file)=os.path.split(adeck)
                    if(len(file) == 13):
                        bstm2id=file[1:5]+'.'+file[5:9]
                    else:
                        bstm2id=None

                    if(tstm2id == bstm2id):
                        if(verb): print 'hhhhh ',bstm2id,tstm1id

                        self.path[tstm1id]=adeck
                        self.size[tstm1id]=mf.GetPathSiz(adeck)
                        self.mtime[tstm1id]=mf.PathModifyTime(adeck)
                        self.stm1ids.append(tstm1id)
                        self.paths.append(adeck)

            self.adptype='stmopt'



        elif(dtgopt != None):

            stmids=[]
            for dtg in dtgs:
                (tstmids,tstmopt)=GetStmidsByDtg(dtg)
                stmids=stmids+tstmids

            stm1ids=[]
            stm2ids=[]
            for stmid in stmids:
                stm2id=stm1idTostm2id(stmid)
                stm2ids.append(stm2id)

            adeckpaths={}

            for dtg in dtgs:

                for adeck in adecks:

                    if(verb): print 'adeck: ',adeck
                    (dir,file)=os.path.split(adeck)
                    if(len(file) == 13):
                        bstm2id=file[1:5]+'.'+file[5:9]
                    else:
                        bstm2id=None

                    for stm2id in stm2ids:
                        if(stm2id == bstm2id):
                            stm1id=stmids[stm2ids.index(stm2id)]
                            if(verb): print 'hhhhh ',stm2id,stm1id
                            stm1ids.append(stm1id)
                            adeckpaths[dtg,stm1id]=adeck

            self.dtgs=dtgs
            self.stm1ids=stm1ids
            self.stm2ids=stm2ids
            self.adptype='dtgopt'
            self.paths=adeckpaths





    def GetAtcfAdecks(self,stm2id=None,yearopt=None,verb=0):

        from ATCF import PickBestDeck

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

        elif(yearopt != None):
            years=YearRanage(byear=yearopt)

        else:
            years=[yyyy]


        tadeck=None
        if(stm2id != None):
            years=[stm2id.split('.')[1]]
            tadeck=stm2id.replace('.','')+'.dat'


        adecks=[]

        for year in years:

            bdir=TcAdecksJtwcDir+"/%s"%(year)

            #
            # convert nrl/nhc adecks in lant/epac/cpac to my bt.local.form
            #


            if(int(year) >= yearneumann):
                bdiradeckal=TcAdecksNhcDir+"/%s"%(year)
                bdiradecksl=TcAdecksNhcDir+"/%s"%(year)
                bdiradeckep=TcAdecksNhcDir+"/%s"%(year)
                bdiradeckcp=TcAdecksNhcDir+"/%s"%(year)


            maskadeckal="%s/aal[0-9][0-9]%s.dat"%(bdiradeckal,year)
            maskadecksl="%s/asl[0-9][0-9]%s.dat"%(bdiradecksl,year)
            maskadeckep="%s/aep[0-9][0-9]%s.dat"%(bdiradeckep,year)
            #
            # handle case when cp storm -> jtwc aor
            # handle case where ep storm -> cpc -> jtwc updated
            #
            maskadeckcpnhc="%s/acp[0-9][0-9]%s.dat"%(bdiradeckcp,year)
            maskadeckcpjtwc="%s/acp[0-9][0-9]%s.dat"%(bdir,year)
            maskadeckepnhc="%s/aep[0-9][0-9]%s.dat"%(bdiradeckep,year)
            maskadeckepjtwc="%s/aep[0-9][0-9]%s.dat"%(bdir,year)
            maskadeckwp="%s/awp[0-9][0-9]%s.dat"%(bdir,year)
            maskadeckio="%s/aio[0-9][0-9]%s.dat"%(bdir,year)
            maskadecksh="%s/ash[0-9][0-9]%s.dat"%(bdir,year)

            if(verb):
                print 'MMMMal     ',maskadeckal
                print 'MMMMsl     ',maskadecksl
                print 'MMMMep     ',maskadeckep
                print 'MMMMcpnhc  ',maskadeckcpnhc
                print 'MMMMcpjtwc ',maskadeckcpnhc
                print 'MMMMepnhc  ',maskadeckepnhc
                print 'MMMMepjtwc ',maskadeckepnhc
                print 'MMMMwp     ',maskadeckwp
                print 'MMMMio     ',maskadeckio
                print 'MMMMsh     ',maskadecksh


            adeckswp=glob.glob(maskadeckwp)
            adecksio=glob.glob(maskadeckio)
            adeckssh=glob.glob(maskadecksh)

            adecksal=glob.glob(maskadeckal)
            adeckssl=glob.glob(maskadecksl)

            adeckscpnhc=glob.glob(maskadeckcpnhc)
            adeckscpjtwc=glob.glob(maskadeckcpjtwc)

            adecksepnhc=glob.glob(maskadeckepnhc)
            adecksepjtwc=glob.glob(maskadeckepjtwc)

            #
            # def to pick "correct" deck
            #

            adecksep=PickBestDeck(adecksepnhc,adecksepjtwc,verb=verb)
            adeckscp=PickBestDeck(adeckscpnhc,adeckscpjtwc,verb=verb)

            adecks= adecks + adeckswp + adecksio + adeckssh + adeckscp + adecksal + adeckssl + adecksep

            if(tadeck != None):
                oadecks=[]
                for adeck in adecks:
                    if(mf.find(adeck,tadeck)): oadecks.append(adeck)
                adecks=oadecks

        return(adecks)


#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc -- AdeckAcardsDtgHash
#

class AdeckAcardsDtgHash(Adeck):

    def __init__(self,mD,acards,dtgopt=None,taids=None,verb=0,warn=0,
                 skipcarq=1,
                 undef=-9999.,
                 adyear=None,
                 adyearp1=None,
                 dofilt9x=0,
                 aliases=None):

        self.mD=mD
        self.adecks='acardsDtgHash'
        self.dtgopt=dtgopt
        self.taids=taids
        self.verb=verb
        self.warn=warn
        self.skipcarq=skipcarq
        self.undef=undef
        
        self.dofilt9x=dofilt9x

        self.adyear=adyear
        self.adyearp1=adyearp1

        self.aliases=aliases

        self.initVars()

        kk=acards.keys()
        kk.sort()

        cards=[]
        for k in kk:
            aa=acards[k]
            for a in aa:
                cards.append(a)

        # --- dup check; for cases of dup storms in tcvitals
        #
        cards=MF.uniq(cards)
        self.cards=cards
        self.initAdeck(skipcarq=self.skipcarq)




#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc -- AdeckNoLoad
#

class AdeckNoLoad(Adeck):


    def __init__(self,stm1id,dtgopt=None,taids=None,verb=0,warn=0,
                 skipcarq=1,
                 undef=-9999.,
                 adyear=None,
                 adyearp1=None,
                 dofilt9x=0,
                 aliases=None):

        from tcbase import TcDssbdir

        year=stm1id.split('.')[1]

        dbname='mdecks'
        dbfile="%s.pypdb"%(dbname)
        DSs=DataSets(bdir=TcDssbdir,name=dbfile,dtype=dbname,verb=verb)

        print 'NOLOAD stm1id, year: ',stm1id,year
        self.mD=DSs.getDataSet(key=year).md
        self.adecks='noload'
        self.dtgopt=dtgopt
        self.taids=taids
        self.verb=verb
        self.warn=warn
        self.skipcarq=skipcarq
        self.undef=undef
        self.dofilt9x=dofilt9x

        self.adyear=adyear
        self.adyearp1=adyearp1

        self.aliases=aliases

        self.stm1id=stm1id
        try:    self.bts=self.mD.bts[stm1id]
        except: self.bts=None

        if(self.bts == None):
            print 'EEE error in making noload adeck in class AdeckNoLoad() for stm1id: ',stm1id
            sys.exit()

        # make adeck cards using the best track
        #
        acards={}
        dtgs=self.bts.keys()
        dtgs.sort()
        for dtg in dtgs:
            btdic=self.bts[dtg][0]
            (lat,lon,vmax,pmin,dum1,dum2)=btdic

            trk={}
            trk[0]=(lat,lon,vmax,pmin)
            acds=MakeAdeckCards('noload',dtg,trk,stm1id)
            acards[dtg]=acds


        self.initVars()

        kk=acards.keys()
        kk.sort()
        cards=[]
        for k in kk:
            aa=acards[k]
            for a in aa:
                cards.append(a)

        self.cards=cards
        self.initAdeck()

#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc -- TcFtBtGsf -- make .gs for plotting TCs in grads
#
class TcFtBtGsf(MFbase):


    gsfnameBT='prwtcbt'
    npnameBT='ntcbt'
    pnameBT='tcbt'

    gsfnameFT='prwtcft'
    npnameFT='ntcft'
    pnameFT='tcft'



    def __init__(self,source,tstmids,tdtg,taids,
                 tD=None,
                 dtx=6,
                 ATtauRange='-24.0',
                 BTtauRange='-24',
                 ATOtauRange=None,
                 dupchk=1,
                 verb=0
                 ):

        if(tD == None):      tD=TcData(dtgopt=tdtg)

        self.tD=tD
        self.source=source
        self.tstmids=tstmids
        self.tdtg=tdtg
        self.taids=taids
        self.dtx=dtx
        self.verb=verb

        self.ATtauRange=ATtauRange
        self.BTtauRange=BTtauRange
        self.ATOtauRange=ATOtauRange
        
        self.dupchk=dupchk

        selfverb=verb


    def getABs(self):

        (ABs,tstmids)=getATsBTs(
            tD=self.tD,
            source=self.source,
            tstmids=self.tstmids,
            tdtg=self.tdtg,
            taids=self.taids,
            ATtauRange=self.ATtauRange,
            BTtauRange=self.BTtauRange,
            ATOtauRange=self.ATOtauRange,
            dtx=self.dtx,
            dupchk=self.dupchk,
            verb=self.verb)


        self.ABs=ABs
        self.tstmids=tstmids


    def makeSetTcGsf(self,obttimes=None):

        # -- set the _bttau to last time in list of times -- for w2-plot.py that does just tau=0
        #

        bttimes=[]
        for tstmid in self.tstmids:
            for taid in self.taids:
                (satrk,satimes,sbtrk,sbtimes)=self.ABs[tstmid,taid]
                bttimes=bttimes+sbtimes

        bttimes=mf.uniq(bttimes)
        try:
            bttime=bttimes[-1]
        except:
            bttime=0

        if(0 in bttimes): bttime=0

        if(obttimes == None): obttimes=bttimes

        gsf="""function settcbt()
_btcoltc=3
_btcol=6
_btszscl=1.0
_bttau=%d

_ftszscl=1.0
_ftbcol=1
_ftfcol=2

# load the global data arrays
rc=%s()
rc=%s()

# -- new bt taus
#
_nbttaus=%d

"""%(bttime,self.gsfnameBT,self.gsfnameFT,len(obttimes))


        nb=1
        for obttime in obttimes:
            if(obttime < 0):
                obttime="m%03d"%(abs(obttime))
            else:
                obttime="%d"%(obttime)

            gsf="""%s
_bttaus.%d=%s"""%(gsf,nb,obttime)
            nb=nb+1


        gsf="""%s
return
"""%(gsf)
        return(gsf)


    def makeTcFtBtGsf(self,ttype):

        if(ttype == 'bt'):
            gsfname=self.gsfnameBT
            npname=self.npnameBT
            pname=self.pnameBT

        elif(ttype == 'ft'):
            gsfname=self.gsfnameFT
            npname=self.npnameFT
            pname=self.pnameFT

        else:
            print 'EEE invalid ttype: ',ttype,' in TcFtBtGsf.makeTcFtBtGsf'
            sys.exit()


        gsf="""function %s()"""%(gsfname)

        # -- all bts

        bposits={}
        taid=self.taids[0]
        alldattimes=[]
        for tstmid in self.tstmids:
            (satrk,satimes,sbtrk,sbtimes)=self.ABs[tstmid,taid]

            if(ttype == 'bt'):
                dattimes=sbtimes
                dattrk=sbtrk
            elif(ttype == 'ft'):
                dattimes=satimes
                dattrk=satrk
            else:
                print 'EEE invalid ttype: ',ttype,' in TcFtBtGsf.makeTcFtBtGsf'
                sys.exit()

            alldattimes=alldattimes+dattimes

            for btime in dattimes:
                try:
                    bposit=dattrk[btime]
                except:
                    bposit=None

                if(bposit != None):
                    MF.appendDictList(bposits,btime,bposit)


        alldattimes=mf.uniq(alldattimes)

        for btime in alldattimes:

            try:
                nbt=len(bposits[btime])
            except:
                nbt=0

            if(ttype == 'bt' and btime <= 0):
                otau="m%03d"%(abs(btime))
            else:
                otau="%d"%(btime)

            gsf="""%s
_%s.%s=%d"""%(gsf,npname,otau,nbt)

            for n in range(0,nbt):
                posit=bposits[btime][n]
                if(len(posit) == 0):
                    print 'WWW(AD.makeTCFtBtGsf) len(posit)=0 n: ',n,'continue'
                    continue
                np1=n+1
                gsf="""%s
_%s.%s.%d =\' %6.2f %7.2f %6.0f \'"""%(gsf,pname,otau,np1,
                                       posit[0],posit[1],posit[2])


        gsf="""%s
return
"""%(gsf)

        #if(len(bposits) == 0): gsf=''
        # no; output just so follow on scripts have the function, even if not used

        return(gsf)


    def makeDrawBtGsf(self):

        # -- draw bt
        #

        gsf="""
function drawtcbt()

#'set rgb 98   1   1   1'
#'set rgb 99 254 254 254'
# btc=99

nbttimes=_nbttaus


# -- force single bt
#
nbttime=1
nbttimes=1

while(nbttime <= nbttimes)

#bttau=_bttaus.nbttime
# -- set by function main
#
bttau=_bttau

fmt='m%03.0f'
if(substr(bttau,1,1) != 'm')
  if(bttau < 0) ; bttau=-1*bttau ; endif
  pbttau=math_format(fmt,bttau)
else
  pbttau=bttau
endif

if(_ntcbt.pbttau = 0) ; return ; endif

nbt=_ntcbt.pbttau

# -- if no bts, bail
#
if(nbt = 0 | substr(nbt,1,2) = '_n') ; return ; endif

btc=1
n=1
while(n<=nbt) 

  btmw=subwrd(_tcbt.pbttau.n,3)

  btsizmx=0.25
  btsizmn=0.15
  btsiz=btsizmx*(btmw/135)
  btsiz=0.50
  if(btsiz<btsizmn) ; btsiz=btsizmn ; endif
  btsym=41

  if(_btszscl != '' & _btszscl != '_btszscl' & _btszscl != 'reset' )
    if(_btszscl > 0)
       btsiz=btsiz*_btszscl
    else
       btsiz=-1*_btszscl
    endif
  endif

  btstrc=1
  domark=0

  if(btmw >= 65)
    btc=2
    if(_btcoltc != '_btcoltc') ; btc=_btcoltc ; endif
    btsym=41
    btstrc=btc
  endif

  if(btmw >= 35 & btmw < 65)
    btc=6
    if(_btcol != '_btcol') ; btc=_btcol ; endif
    btsym=40
    btstrc=btc
  endif

  if(btmw < 35)
    btc=6
    if(_btcol != '_btcol') ; btc=_btcol ; endif
    btsym=40
    btsym=2
    btstrc=btc
    mksiz=btsiz*0.5
    domark=1
  endif

  btlat=subwrd(_tcbt.pbttau.n,1)
  btlon=subwrd(_tcbt.pbttau.n,2)

#
# check if lon setting is deg w
#
  if(_lon1 < 0)
    btlon=btlon-360.0
  endif

  'q w2xy 'btlon' 'btlat

  x=subwrd(result,3)
  y=subwrd(result,6)
#
# test if a plot has been made...
#
drawtest=substr(result,1,10)
if(drawtest = 'No scaling'); return; endif

  xs=x+0.015
  ys=y-0.015
if(domark = 0)
  'draw wxsym 'btsym' 'xs' 'ys' 'btsiz' '0' 8'
  'draw wxsym 'btsym' 'x' 'y' 'btsiz' 'btc' 6'
endif

if(domark = 1)
  'set line 98 1 8'
  'draw mark 'btsym' 'xs' 'ys' 'mksiz' 98 8'
  'set line 'btc' 1 5'
  'draw mark 'btsym' 'x' 'y' 'mksiz' 'btc' 6'
  'set line 1'
endif

  btstrsiz=btsiz*0.15
  if(btmw >= 100) ;  btstrsiz=btsiz*0.125 ; endif

  'set strsiz 'btstrsiz

  'set string 0 c 10'
  'draw string 'x' 'y' 'btmw
  'set string 'btstrc' c 5'
  'draw string 'x' 'y' 'btmw

  n=n+1
endwhile

nbttime=nbttime+1
endwhile

return"""
        return(gsf)



    def makeDrawFtGsf(self):

        gsf="""
function drawtcft()

ftsiz=0.115
ftsizs=ftsiz+0.025
ftsizi=ftsiz-0.050
if(_ftszscl != '' & _ftszscl!='_ftszscl') ; ftsiz=ftsiz*_ftszscl ; endif

if(_nfcall = 0) ; return ; endif

n=1
while(n<=_ntcftall._tau) 


  ftlat=subwrd(_tcftall.n,1)
  ftlon=subwrd(_tcftall.n,2)
  fttype=subwrd(_tcftall.n,3)
#
# check if lon setting is deg w
#
if(ftlon = '') ; return ; endif
  if(_lon1 < 0)
    ftlon=ftlon-360.0
  endif

ftest=substr(ftlat,1,3)
if(ftest = '_tc') ; return ; endif

  'q w2xy 'ftlon' 'ftlat
if(subwrd(result,1) = 'No' | subwrd(result,1) = 'Query')
  return
endif
  x=subwrd(result,3)
  y=subwrd(result,6)

  xs=x-0.015
  ys=y+0.015

  ftc=3
  ftci=2
  if(fttype = -1); ftci=4; endif

  if(_ftbcol != '' & _ftbcol != '_ftbcol') ; ftc=_ftbcol ; endif
  if(_ftfcol != '' & _ftfcol != '_ftfcol') ; ftci=_ftfcol ; endif

  ftm=3

  'set line 0'
  'draw mark 'ftm' 'x' 'y' 'ftsizs

  'set line 'ftc
  'draw mark 'ftm' 'x' 'y' 'ftsiz

  'set line 'ftci
  'draw mark 'ftm' 'x' 'y' 'ftsizi

  n=n+1
endwhile

return

function ftposits(ttau,btau,dtau)

tau=ttau*1

maxtau=168
# no posits > 168 h so load all that are available
#
if(tau > maxtau)
  tau=maxtau
endif

jmax=400
i=1
while(tau>=btau)

  n=_ntcft.tau

# -- detect undefined n = the variable string
#
  if(n = '_ntcft.'tau)
    _ntcftall.ttau=0
    return(0)
  endif


  if(n >= 1 )
    j=1
    while(j<=n & j<jmax)

      posit=_tcft.tau.j' 'tau

#
# dtau=6 but posits may not be available
#
#print 'PPPPPP 'tau' posit: 'posit

pchk=substr(posit,1,3)
if(pchk = '_tc')
  j=jmax+1
else
  _tcftall.i=posit
  j=j+1
  i=i+1
endif
    endwhile
    if(j = jmax)
      return(999)
    endif
  endif
  tau=tau-dtau
endwhile

np=i-1
if(i=1); np=_ntcft.tau ; endif
_ntcftall.ttau=np
return(0)"""
        return(gsf)


class TcAidTrkAd2Bd2(MFbase):

    from ATCF import aidDescTechList
    ad=aidDescTechList()
    
    def __init__(self,stmopt=None,dtgopt=None,
                 do9Xonly=0,dobt=0,
                 source='tmtrkN',
                 dsbdir=None,
                 quiet=1,
                 verb=0):
        
        self.quiet=quiet
        self.verb=verb

        if(not(quiet)): MF.sTimer("TcAidTrkAd2Bd2")
        
        self.dtgopt=dtgopt
        self.dtgs=None
        if(dtgopt != None):
            self.dtgs=mf.dtg_dtgopt_prc(dtgopt)
        
        # -- get tstmids
        #
        if(do9Xonly): dobt=0
        (tstmids,tD,tstmids9Xall)=getTstmidsAD2FromStmoptDtgopt(stmopt,dtgopt,do9Xonly,dobt,source)    
        # -- get stmids as output from tracker
        #
        have9X=0
        ostmids={}
        for tstmid in tstmids:
            if(have9X == 0 and Is9X(tstmid)): have9X=1
            rc=getStmParams(tstmid, convert9x=1)
            ostmids[tstmid]=rc[-1]
            
        self.ostmids=ostmids
        
        AD2s9s=None
        (AD2ss,bd2s,dbnames,basins,ybears)=getAdeck2Bdeck2DSs(tstmids,dsbdir=dsbdir,verb=verb)
        if(have9X):
            (AD2s9s,bd29s,dbnames9,basins9,ybears9)=getAdeck2Bdeck2DSs(tstmids9Xall,dsbdir=dsbdir,verb=verb)
        
        self.tstmids=tstmids
        self.tD=tD
        self.tstmids9Xall=tstmids9Xall
        self.AD2ss=AD2ss
        self.AD2s9s=AD2s9s
        self.bd2s=bd2s
        self.source=source
        self.dbnames=dbnames
        self.basins=basins
        
        self.bD2s={}
        self.aD2s={}
        
        # -- get ad2/bd2 by stmid
        #
        for tstmid in tstmids:
            ostmid=ostmids[tstmid]
            try:	
                self.bD2s[ostmid]=bd2s[tstmid]
            except:
                self.bD2s[ostmid]=None
                
            (snum,b1id,stmyear,b2id,stm2id,stm1id)=getStmParams(tstmid)
            
            basin=b2id.lower()
            if(basin == 'cp'): basin='ep'   
        
            if(Is9X(tstmid)):
                try:	
                    self.bD2s[ostmid]=bd29s[tstmid]
                    gotbd9x=1
                except:
                    self.bD2s[ostmid]=None
                    gotbd9x=0
                            
                try:
                    self.aD2s[ostmid]=self.AD2s9s[basin,stmyear]
                except:
                    self.aD2s[ostmid]=None
                    
            else:
                try:
                    self.aD2s[ostmid]=self.AD2ss[basin,stmyear]
                except:
                    self.aD2s[ostmid]=None
                
            if(verb): print 'SSSSSSSSSSSSSSSSSSSSSSSSSS adCL.TcAidTrkAd2Bd2: ',ostmid,'AAA:',self.aD2s[ostmid],'BBB:',self.bD2s[ostmid]

        if(not(quiet)): MF.dTimer("TcAidTrkAd2Bd2")

    def getAidStatus(self,taid,tstmid,doprint=1):

        (snum,b1id,stmyear,b2id,stm2id,stm1id)=getStmParams(tstmid,convert9x=1)
        ostmid=self.ostmids[tstmid]
        astmid=ostmid
        (tnum,b1id,tstmyear,tb2id,tstm2id,tstm1id)=getStmParams(ostmid,convert9x=1)
        if(tnum == snum):
            astmid=ostmid
        
        aD2=self.getAidaD2(taid, astmid, tstmid)
        adtgs=aD2.dtgs
        adtgs.sort()
        dtgstr=MF.makeDtgsString(adtgs, msiz=1024, osiz=132, ndtg=10)
        odtgstr="Aid-Stm: %10s-%s  dtgs: %s"%(taid,tstmid,dtgstr)
        if(doprint): print odtgstr
        return(adtgs)
        
        
    def makeAidStatusCard(self,aD,aid,stm,aStat='',dtgopt=None,idtgs=None,
                          printZeros=0,doPrint=1,lsopt='l'):
        
        # -- find dtgs with longest, because of bug in updateAds of not setting nad.dtgs=
        #
        dtgs1=aD.dtgs
        dtgs2=[]
        if(hasattr(aD,'ats') and aD.ats != None):
            dtgs2=aD.ats.keys() 
        elif(hasattr(aD,'AT')):
            dtgs2=aD.AT.dtgs
            
        dtgs=dtgs1+dtgs2
        odtgs=mf.uniq(dtgs)
        odtgs.sort()
        tdtgs=[]
        if(dtgopt != None):
            tdtgs=mf.dtg_dtgopt_prc(dtgopt)
            
            
        # -- print the adeck cards
        #
        lsopt='f'
        if(lsopt == 'f' and dtgopt != None):
            aD.lsAidcards(dtgopt=dtgopt)


        fdtgs=[]
        if(len(tdtgs) > 0):
            for tdtg in tdtgs:
                if(tdtg in odtgs): fdtgs.append(tdtg)
                
        else:
            fdtgs=odtgs
                    
        doprint=1
        if(not(printZeros) and len(odtgs) == 0): doprint=0
        if(printZeros): doprint=1

        card='nnnnnnnnnnnnnnnnnnnn---------------------------------'
        if(doprint):  
            descA=self.ad.getAidDesc(aid)
            oaStat=aStat

            if(aStat == '..'):
                if(len(fdtgs) == 0): oaStat='mm'
                else: oaStat='  '

            card='%2s %8s'%(oaStat,aid)+" :: %-60s"%(descA[0:60])+' :: stm: %s  '%(stm)+MF.makeDtgsString(fdtgs)
            if(doPrint):
                print card
                
        return(card)

        

    def getStatus(self,modelChk=None,doPrint=1,returnAd2=0,verb=0):


        def getAtcfFileLen(taid,modtctTrk,stmid,asizMin=1000):
            
            aStat='na'
            try:
                aFiles=modtctTrk[taid[1:]]
            except:
                aFiles=None

            if(aFiles != None):

                tb3id=stmid.split('.')[0]
                
                tbshem=isShemBasinStm(tb3id)
                tbio=isIOBasinStm(tb3id)
                tb2num=tb3id[0:2]
                tb1id=tb3id[-1]
                
                for af in aFiles:
                    b3id=af.split('.')[0].upper()

                    bshem=isShemBasinStm(b3id)
                    bio=isIOBasinStm(b3id)
                    b2num=b3id[0:2]
                    b1id=b3id[-1]

                    asiz=int(af.split('.')[1])
                    testShem=(tbshem and bshem)
                    testIo=(tbio and bio)
                    testMisLabel=((testShem or testIo) and tb1id != b1id )
                    testNum=(tb2num == b2num)
                    
                    if(testNum and testShem and testMisLabel):
                        # -- first check if > minsiz
                        #
                        if(asiz < asizMin):
                            aStat='LL'
                        else:
                            aStat='mL t:%s%s s:%s%s'%(tb2num,tb1id,b2num,b1id)
                        return(aStat)
                    
                    if(testNum and testIo and testMisLabel):
                        # -- first check if > minsiz
                        #
                        if(asiz < asizMin):
                            aStat='LL'
                        else:
                            aStat='mL t:%s%s s:%s%s'%(tb2num,tb1id,b2num,b1id)
                        return(aStat)
                    
                    if(b3id == tb3id):
                        #print 'bingo: ',b3id,asiz,asizMin
                        if(asiz < asizMin):
                            aStat='LL'
                        else:
                            aStat='..'
                        return(aStat)
                    
                    
            else:
                aStat='--'
                
            return(aStat)
            
            
        def getAtcfStat(taid,modtctTrk,modtctTrkStdout,stmid,astmid,verb=0):


            aStat1=getAtcfFileLen(taid, modtctTrk, stmid)
            aStat2=getAtcfFileLen(taid, modtctTrk, astmid)
            aStat3=getAtcfFileLen(taid, modtctTrkStdout, astmid)

            ta1=(len(aStat1) > 2) and (len(aStat1.split()) == 3)
            ta2=(len(aStat2) > 2) and (len(aStat2.split()) == 3)
            ta3=(len(aStat3) > 2) and (len(aStat3.split()) == 3)

            if(ta1 or ta2 or ta3):
                aStat=aStat1
                return(aStat)

            aStat=aStat1[0:2]
            if(aStat2 == '..' or  aStat1 == '..'  or aStat3 == '..'): aStat='..'
            if(aStat2 == 'LL' or  aStat1 == 'LL'  or aStat3 == 'LL'): aStat='LL'
            if(aStat2 == 'na' and aStat1 == 'na' and aStat3 == 'na'): aStat='na'
            if(aStat2 == 'na' and aStat1 == 'na' and aStat3 == '..'): aStat='TF'
            
            if(self.verb): print '111--222--333',aStat1,aStat2,aStat3,'AAA:',aStat
            return(aStat)
        
        
        
        
        # ---------------------------------- main section
        
        if(not(self.quiet)): MF.sTimer("getStatus")
        tctdir="%s"%(w2.TcDatDirTMtrkN)
        rcS=-999
        
        self.stmids={}

        if(self.dtgopt != None):
            dtgs=mf.dtg_dtgopt_prc(self.dtgopt)
        else:
            print 'WWW-getStatus needs a dtgopt...None given...return'
            rcS=-1
            return(rcS)
        
        
        tstmids={}
        
        taidsG={}
        taidsT={}
        taidsTS={}
        
        rcTct=[]
        rcTcg=[]
        
        taidsTA={}
        rcTctA=[]
        rcTctS=[]
        
        for dtg in dtgs:
            
            if(not(self.quiet)):
                MF.sTimer("trk-%s"%(dtg))
                MF.dTimer("trk-%s"%(dtg))
                
            stmids=self.tD.getStmidDtg(dtg,verb=0)
            
            astmids={}

            for stmid in stmids:
                (snum,b1id,stmyear,b2id,stm2id,stm1id)=getStmParams(stmid,convert9x=1)
                for tstmid in self.tstmids:
                    ostmid=self.ostmids[tstmid]
                    (tnum,b1id,tstmyear,tb2id,tstm2id,tstm1id)=getStmParams(ostmid,convert9x=1)
                    if(tnum == snum):
                        astmids[stmid]=ostmid
                        break
                    
            #print 'OOOO',self.ostmids
            #print 'AAAA',astmids    
            #print 'KKKK',self.aD2s.keys()
                
            tstmids[dtg]=stmids
            stm3ids=[]
            for stmid in stmids:
                s3id=stmid[0:3].lower()
                stm3ids.append(s3id)
                
            modtctGen={}
            modtctTrk={}
            modtctTrkStdout={}
            modtctAllTrk={}
            
            byear=dtg[0:4]

            # -- always go for the zip file
            #
            tcgfiles={}
            doZipG=0
            if(self.source == 'tmtrkN'):
                rcZip=getAdeckPathsCardsZip(self.source, dtg, byear,stype='gen')
                (doZipG,tcgfiles,zipDir,tcgAllfiles,sopaths)=rcZip
            
            rcZip=getAdeckPathsCardsZip(self.source, dtg, byear,stype='atcf')
            (doZipA,tctfiles,zipDir,tctAllfiles,sopaths)=rcZip
            
            
            rcbad=1
            if(self.source == 'tmtrkN' and doZipG == 0 and doZipA == 0):
                print 'WWW -- no atcf adecks to zip or source: ',self.source,' dtg: ',dtg
                rcbad=-1
            
            if(doZipG == -1 or doZipA == -1):
                print 'WWW -- zip file bad...press...'
                rcbad=-2
            
            if(self.source == 'mftrkN' and doZipA == 0):
                print 'WWW -- no atcf adecks to zip or source: ',self.source,' dtg: ',dtg
                rcbad=-3
            
            if(rcbad < 0):
                if(returnAd2 == 1): rcS=[-1,None,None,None]
                if(returnAd2 == 2): rcS=(None,None,None,None)
                return(rcS)
                
                
            # -- tracker files
            #
            tctKeys=tctfiles.keys()
            for kk in tctKeys:
                (tsiz,st,sc)=tctfiles[kk]
                tt=kk.split('.')
                if(self.source == 'tmtrkN'):
                    model=tt[-3]
                elif(self.source == 'mftrkN'):
                    model=tt[-4]

                if(modelChk != None and model != modelChk): continue
                stm3id=tt[-2]
                ostm3id="%s.%-5d"%(stm3id,tsiz)
                if(tsiz > 0):
                    MF.appendDictList(modtctTrk,model,ostm3id)
            

            # -- tmtrkN stdout files
            #
            soKeys=sopaths.keys()
            for kk in soKeys:
                (ssiz,st,sc)=sopaths[kk]
                tt=kk.split('.')
                model=tt[-3]

                if(modelChk != None and model != modelChk): continue
                stm3id=tt[-2]
                ostm3id="%s.%-5d"%(stm3id,ssiz)
                if(ssiz > 0):
                    if(verb): print 'Stdout: ',model,ostm3id
                    MF.appendDictList(modtctTrkStdout,model,ostm3id)

            # -- tracker ALL files
            #
            tctKeys=tctAllfiles.keys()
            for kk in tctKeys:
                (tsiz,st,sc)=tctAllfiles[kk]
                tt=kk.split('.')
                model=tt[-2]

                if(modelChk != None and model != modelChk): continue
                stm3id='all'
                ostm3id="%s.%-5d"%(stm3id,tsiz)
                MF.appendDictList(modtctAllTrk,model,ostm3id)


            # -- tcgen files
            #
            tcgKeys=tcgfiles.keys()
            for kk in tcgKeys:
                (tsiz,st,sc)=tcgfiles[kk]
                tt=kk.split('.')
                model=tt[-2]
                if(modelChk != None and model != modelChk): continue
                basin=tt[-4]
                obasin="%4s.%-5d"%(basin,tsiz)
                MF.appendDictList(modtctGen,model,obasin)

            modelsG=modtctGen.keys()
            modelsT=modtctTrk.keys()
            modelsTS=modtctTrkStdout.keys()
            modelsTA=modtctAllTrk.keys()

            # -- run status test
            #
            testT=(len(modelsT) == 0 and (len(modelsG) == 0 and self.source == 'tmtrkN') and modelChk != None)
            testM=(len(modelsT) == 0 and self.source == 'mftrkN' and modelChk != None)
            
            # -- if no model trackers do a one-line print
            #
            if(testT):
                print 'NADA trackers for dtg: ',dtg,' model: ',modelChk
                rcS=2
                return(rcS)
            elif(testM):
                rcS=0
                return(rcS)
            
            modelsG.sort()
            modelsT.sort()
            modelsTS.sort()
            modelsTA.sort()
            
            rcS=1
            if(modelChk != None and doPrint == 0 and returnAd2 == 0):
                if(len(modelsG) == 0 and len(modelsT) == 0): rcS=0
                return(rcS)
    
            taidsG[dtg]=modelsG
            taidsT[dtg]=modelsT
            taidsTS[dtg]=modelsTS
            taidsTA[dtg]=modelsTA
            
            nbsnG=0
            for model in modelsG:
                nbsnG=nbsnG+len(modtctGen[model])
                
            nbsnGE=5
            nmodG=len(modelsG)
            nbsnGE=nbsnGE*nmodG
            nactG=nbsnG
            StatusG='copacetic...'
            if(nactG < nbsnG): StatusG=' <<<< missing'
            if(nactG > nbsnG): StatusG=' >>>>>>>>  too many!'
            
            modelsT.sort()
            ntrk=0
            for model in modelsT:
                ntrk=ntrk+len(modtctTrk[model])
            
            modelsTS.sort()
            ntrkS=0
            for model in modelsTS:
                ntrkS=ntrkS+len(modtctTrkStdout[model])
                
            ntcsT=len(stm3ids)
            nmodT=len(modelsT)
            nmodTS=len(modelsTS)
            nexpT=ntcsT*nmodT
            nexpTS=ntcsT*nmodTS
            nactT=ntrk
            nactTS=ntrkS
            StatusT='copacetic...'
            if(nactT < nexpT): StatusT=' <<<< missing'
            if(nactT > nexpT): StatusT=' >>>>>>>>  too many!'

            StatusTS='StdOut copacetic'
            if(nactTS < nexpTS): StatusTS=' tracker failed <<<< missing'
            if(nactTS > nexpTS): StatusTS=' tracker >>>>>>>>  too many!'

            rcAd2=[]
            rcTct=[]
            rcTctS=[]
            rtTctA=[]
            rcTcg=[]
    
            if(doPrint):
                print
                print 'tcGEN files for dtg: ',dtg,' Nbsns: %2d'%(nbsnG),' NMod: ',nmodG,'  Nact: %2d'%(nactG),' Nexp: %2d'%(nbsnGE),' Status: ',StatusG
    
            for model in modelsG:
                bsns=modtctGen[model]
                nbsns=len(bsns)
                card='%-4s  basins: '%(model),bsns
                rcTcg.append(card)
                if(doPrint): print '%-4s  basins: '%(model),bsns
                
            if(doPrint):
                print
                print 'tcTRK files  for dtg: ',dtg,' NTCs:  %2d'%(ntcsT),' NMod:  ',nmodT,'   Nact: %2d'%(nactT),'  Nexp: %2d'%(nexpT),' Status: ',StatusT
                print 'tcTRK STDOUT for dtg: ',dtg,' NTCs:  %2d'%(ntcsT),' NModS: ',nmodTS,'  NactS: %2d'%(nactTS),' NexpS: %2d'%(nexpTS),' StatusS: ',StatusTS
    
            for model in modelsT:
                stmsT=modtctTrk[model]
                nstms=len(stmsT)
                card='%-4s    stms: %-60s from tmtrkN '%(model,stmsT)
                rcTct.append(card)
                if(doPrint): print card
            
            for model in modelsTS:
                stmsTS=modtctTrkStdout[model]
                nstms=len(stmsTS)
                card='%-4s    stms: %-60s from tmtrkN stdout'%(model,stmsTS)
                rcTctS.append(card)
                if(doPrint): print card
            
            if(doPrint):
                print
                print 'tcTRK ALL file for dtg: ',dtg

            for model in modelsTA:
                siza=modtctAllTrk[model]
                card='%-4s    ALL siz: '%(model),siza
                rcTctA.append(card)
                if(doPrint): print card

            taids=[]
            
            # -- inspect the AD2 ...
            #
            if(doPrint and len(stmids) > 0):
                print
                print """tcAD2 status: ' ' -- good 'LL' -- low size 'na' -- not available 'TF' -- Tracker ran but Failed 'mL' -- bid mislabelled"""

            if(self.source == 'tmtrkN'):
                for model in modelsT:
                    taids.append("t%s"%(model))
            elif(self.source == 'mftrkN'):
                for model in modelsT:
                    taids.append("m%s"%(model))
                
            okNN=0
            ok9X=0
            exNN='nnnnnnn'
            ex9X='9999999'

            for stmid in stmids:
                
                astmid=astmids[stmid]
                
                try:
                    bD2=self.bD2s[astmid]
                    tstmid=self.ostmids.keys()[self.ostmids.values().index(astmid)]
                except:
                    print 'WWW-------> adCL.TcAidTrkAd2Bd2: no bD2 or ostmids for: ',astmid,' <--------'
                    okNN=ok9X=0
                    continue
                
                aD2=None
                for taid in taids:
                    aStat=getAtcfStat(taid, modtctTrk, modtctTrkStdout, stmid, astmid,verb=0)

                    if(verb):
                        print 'AAAASSSS',aStat
                    aD2=self.getAidaD2(taid, astmid, tstmid)

                    okNN=1
                    ok9X=1
                    exNN='nnnnnnn'
                    ex9X='9999999'
                    
                    if(IsNN(stmid)):
                        
                        if(aStat == 'na'): 
                            okNN=-1
                        
                        if(aStat == 'TF'): 
                            okNN=-2
                            
                        if(aStat[0:2] == 'mL'): 
                            okNN=-3
                            exNN=aStat[3:]
                    
                    elif(Is9X(stmid)):
                        if(aStat == 'na'):
                            ok9X=-1
                            
                        if(aStat == 'TF'):
                            ok9X=-2
                            
                        if(aStat[0:2] == 'mL'):
                            ok9X=-3
                            ex9X=aStat[3:]
                            
                            
                    if(aD2 != None): 
                        if(aStat == 'NN'):
                            descNA='--------------------------------- mondai ha desu ne! -- aD2 iin desu kedo, sorekara...'
                            card='%2s %8s'%(aStat,taid)+" :: %-60s"%(descNA)+' :: stm: %s  '%(stmid)+MF.makeDtgsString([])
                            a2card="%d %d %s"%(card)
                            rcAd2.append(acard)
                            if(doPrint): print card
                        else:
                            rc=self.makeAidStatusCard(aD2,taid,astmid,dtgopt=dtg,aStat=aStat[0:2],doPrint=doPrint)
                            acard="%d %d %s"%(okNN,ok9X,rc)
                            rcAd2.append(acard)
                        
                    else:
                        oaStat=aStat
                        if(aStat == '  '): oaStat='MM'
                        if(oaStat == 'MM'):
                            descNA='!!!!!!!!!!!!!!!!!!!! Komarimashite ne! atcf tracker NOT in aD2'
                        else:
                            descNA='--------------------------------- mondai ga desu ne! -- aD2 = naninomae'
                            
                        card='%2s %8s'%(oaStat,taid)+" :: %-60s"%(descNA[0:60])+' :: stm: %s  '%(astmid)+MF.makeDtgsString([])
                        rcAd2.append(card)
                        if(doPrint): print card
                        
                #if(doPrint): print
                        
            if(doPrint): print    

        if(not(self.quiet)): MF.dTimer("getStatus")

        if(returnAd2 == 1): rcS=[rcTct,rcTcg,rcTctA,rcTctS]
        if(returnAd2 == 2): rcS=(okNN,ok9X,exNN,ex9X)
        if(returnAd2 == 3): rcS=(modtctGen,modtctTrk,modtctTrkStdout,modtctAllTrk)
            
        return(rcS)
        
        
    def getAidaD2(self,taid,kstmid,tstmid,verb=0):
        
        key="%s_%s"%(taid,tstmid.upper())
        aD2ds=self.aD2s[kstmid]
        
        #aD2ds.ls()
        #kk=aD2ds.getKeys()
        #for k in kk:
        #    if(mf.find(k,taid)):
        #        print k

        try:
            aD2=aD2ds.getDataSet(key)
            gotit=1
        except:
            gotit=0
            aD2=None

        if(verb):
            if(gotit):
                print 'GGGGG',kstmid,'key: ',key,aD2
            else:
                print 'NNNN',kstmid,key
            
        return(aD2)
    
        #aidtrk=None
        #if(aD2 != None):

            #aD2dtgs=aD2.dtgs
            #aD2dtgs.sort()
            
            #if(dtg in aD2dtgs):
                #aidtrk=aD2.AT.atrks[dtg]
                #self.aid=taid
                #self.aidtrk=aidtrk
                #self.aidtaus=aidtrk.keys()
                #self.aidtaus.sort()
                #self.aidsource=source
                #self.aidname=taid
                #self.stmid=stmid
                #gotaid=1
            #else:
                #gotaid=0
        #else:
            #gotaid=0
            
        #return(aidtrk)
                
        
        




#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc -- AdeckCards
#

class AdeckCards(Adeck):

    def __init__(self,taid,tstmid,acards,verb=0):

        self.dtgs=acards.keys()
        self.dtgs.sort()

        self.aid=taid
        self.stmid=tstmid
        self.acards=acards



