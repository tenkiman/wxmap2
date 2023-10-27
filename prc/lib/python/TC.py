from M import *

from w2local import W2
W2=W2()

TcDataBdir=W2.TcDatDir
W2BaseDirDat=W2.W2BaseDirDat

TcNamesDatDir=W2.TcNamesDatDir
SetLandFrac=W2.SetLandFrac
GetLandFrac=W2.GetLandFrac

from ATCF import *

MdeckBaseDir="%s/mdeck"%(TcDataBdir)

TcEcmwfBaseDir="%s/ecmwf"%(TcDataBdir)

TcAdecksNhcDir="%s/adeck/nhc"%(TcDataBdir)
TcAdecksJtwcDir="%s/adeck/jtwc"%(TcDataBdir)
TcBdecksNhcDir="%s/bdeck/nhc"%(TcDataBdir)
TcBdecksJtwcDir="%s/bdeck/jtwc"%(TcDataBdir)
TcAdecksEsrlDir="%s/adeck/esrl"%(TcDataBdir)
TcAdecksNcepDir="%s/adeck/ncep"%(TcDataBdir)
TcAdecksEcmwfDir="%s/adeck/ecmwf"%(TcDataBdir)
TcAdecksLocalDir="%s/adeck/local"%(TcDataBdir)

TcRefTrkDatDir="%s/reftrk"%(TcDataBdir)
TcVitalsDatDir="%s/tcvitals"%(TcDataBdir)
TcGenDatDir="%s/tcgen"%(TcDataBdir)
TcDiagDatDir="%s/tcdiag"%(TcDataBdir)

TcObsMtcswaSourceDir="%s/cira/mtcswa"%(TcDataBdir)
TcObsSatWindsDir="%s/obs/satwinds"%(TcDataBdir)

EcmwfBufrLocalDir=TcEcmwfBaseDir + '/ecbufr'
EcmwfBufrJetDir=W2BaseDirDat + '/ecnogaps/ecbufr'


TcDssbdir="%s/DSs"%(TcDataBdir)

AdeckBaseDir="%s/adeck"%(TcDataBdir)
W2fldsBaseDir="%s/nwp2/w2flds"%(W2BaseDirDat)
YearTcBtNeumann=1945

MF=MFutils()

Basin1toBasin2 = {
    'A':'IO',
    'B':'IO',
    'B':'IO',
    'L':'AL',
    'I':'IO',
    'S':'SH',
    'P':'SH',
    'W':'WP',
    'C':'CP',
    'E':'EP',
    'Q':'SL',
    'T':'SA',
    'X':'XX',
    }

Basin2toBasin1 = {
    'IO':'I',
#    'SH':'S',
    'SH':'P',
    'SI':'S',
    'SP':'P',
    'WP':'W',
    'CP':'C',
    'EP':'E',
    'AT':'L',
    'AL':'L',
    'NA':'A',
    'SL':'Q',
    'SA':'T',
    'BB':'B',
    'AS':'A',
    'XX':'X',
    # -- default in gettrk_gen.x  how he handles 'I' storms...
    'HC':'I',
    }



TcGenBasin2Area={
    'lant':'troplant',
    'epac':'tropepac',
    'wpac':'tropwpac',
    'shem':'tropsio',
    'nio':'tropnio',
    }




centerid='MFTC'


class TcBasin(MFbase):


    def __init__(self,basin):

        if(mf.find(basin,'epac')):

            self.basin='epac'


        elif(mf.find(basin,'wpac')):

            self.basin='wpac'


        elif(mf.find(basin,'lant')):

            self.basin='lant'

        elif(mf.find(basin,'nio')):

            self.basin='nio'

        elif(mf.find(basin,'shem')):

            self.basin='shem'




    def isLLin(self,lat,lon):

        if(self.basin == 'epac'):

            epac=( (lon >= 276 and lon <= 282 and lat <  9 ) or
                   (lon >= 273 and lon <  276 and lat < 12 ) or
                   (lon >= 267 and lon <  273 and lat < 15 ) or
                   (lon >= 261 and lon <  267 and lat < 17 ) or
                   (lon >= 180 and lon <  261 and lat >  0)
                   )
            return(epac)

        elif(self.basin == 'lant'):

            lant=( (lon >= 276 and lon <= 282 and lat >=  9 ) or
                   (lon >= 273 and lon <  276 and lat >= 12 ) or
                   (lon >= 267 and lon <  273 and lat >= 15 ) or
                   (lon >= 261 and lon <  267 and lat >= 17 ) or
                   (lon >= 276 and lon <= 360 and lat >   0 ) 
                   )
            return(lant)


        elif(self.basin == 'wpac'):
            wpac=( (lon >= 100 and lon <= 180) and lat >=  0 )
            return(wpac)

        elif(self.basin == 'nio'):
            nio=( (lon >= 40 and lon <= 100) and lat >=  0 )
            return(nio)

        elif(self.basin == 'shem'):
            shem=( (lon >= 35 and lon <= (360-150)) and lat <  0 )
            return(shem)

            


    
class TcData(MFbase):

    dsbdir="%s/DSs"%(TcDataBdir)
    dbname='mdecks'
    dbfile="%s.pypdb"%(dbname)

    ncycles=10
    nsleep=0
    sleepytime=5.0
        
    def __init__(self,
                 mdDSs=None,
                 mdD=None,
                 mdDs=None,
                 mdDg=None,
                 verb=0,
                 backup=0,
                 doclean=0,
                 dotcgen=1,
                 ):


        self.verb=verb
        self.backup=backup
        self.doclean=doclean
        self.dotcgen=dotcgen

        if(mdDSs != None): self.mdDSs=mdDSs
        if(mdD != None): self.mdD=mdD
        if(mdDs != None): self.mdDs=mdDs
        if(mdDg != None): self.mdDg=mdDg
        
        self.initmdDSs()
        
        while(self.nsleep < self.ncycles and (self.mdstate == 0) ):
            time.sleep(self.sleepytime)
            self.initmdDSs()
            self.nsleep=self.nsleep+1

        if(self.nsleep >= self.ncycles):
            print 'EEE cycled: ',self.ncycles,' times waiting for mdecks.pypdb to come over...sayoonara'
            sys.exit()

        self.stmdtg=self.mdD.stm1dtg
        self.tcvitalsdtg=self.mdD.tcvitalsdtg
        self.gendtg=self.mdDg.gen1dtg

        try:
            self.sbts=self.mdDs.sbts
        except:
            print 'EEE TC.TcData failed to set mdDs.sbts ... return None'
            self=None
            return


    def initmdDSs(self):
        
        if(not(hasattr(self,'mdDSs'))):

            if(self.verb): self.sTimer(tag='mddss')
            mdDSs=DataSets(bdir=self.dsbdir,name=self.dbfile,dtype=self.dbname,
                           verb=self.verb,
                           backup=self.backup,
                           unlink=self.doclean)
            
            self.mdDSs=mdDSs
            if(self.verb): self.dTimer(tag='mddss')

            if(self.verb): MF.sTimer(tag='mdD')
            self.mdD=self.mdDSs.getDataSet(key='mdeck_dtg')
            if(self.verb): self.dTimer(tag='mdD')

            if(self.verb): self.sTimer(tag='mdDs')
            self.mdDs=self.mdDSs.getDataSet(key='mdeck_stmid')
            if(self.verb): self.dTimer(tag='mdDs')

            if(self.dotcgen):
                if(self.verb): MF.sTimer(tag='mdDg')
                self.mdDg=self.mdDSs.getDataSet(key='mdeck_dtg_gen')
                if(self.verb): MF.dTimer(tag='mdDg')
            else:
                self.mdDg=None

        self.mdstate=1
        if(self.mdD == None):
            print 'WWW mdD not available for : ',self.dsbdir,self.dbname,' try initmdDSs again...'
            self.mdstate=0

        if(self.mdDg == None and self.dotcgen):
            print 'WWW mdDg not available for : ',self.dsbdir,self.dbname,' try initmdDSs again...'
            self.mdstate=0



    def dupChkBtcs(self,stmids,btcs,gdisttol,verb=0):

        nstms=len(stmids)
        if(nstms > 1):
            dups=[]
            for i in range(0,nstms-1):
                stm0=stmids[i]
                istrt=i+1
                for j in range(istrt,nstms):
                    stm1=stmids[j]
                    (lat0,lon0)=btcs[stm0][0:2]
                    (lat1,lon1)=btcs[stm1][0:2]
                    gdist=gc_dist(lat0,lon0,lat1,lon1)
                    if(gdist <= gdisttol and (i != j) ):
                        dups.append((i,j))
                        if(verb): print 'dddddd ',i,j,'stm0: ',stm0,lat0,lon0,' stm1: ',stm1,lat1,lon1,gdist

        # dddd -- select which storm should be tossed
        #
        if(len(dups) > 0):
            for dup in dups:
                (i,j)=dup
                stmi=int(stmids[i][0:2])
                stmj=int(stmids[j][0:2])

                # -- select NN over 9X, if both 9X the kill first one
                #
                ikill=i
                if(stmi >= 90 and stmj < 80): ikill=i
                if(stmj >= 90 and stmi < 80): ikill=j
                try:
                    del btcs[stmids[ikill]]
                except:
                    print 'WWW double dups TC.dupChkBtcs: ',i,j,stmi,stmj,stmids[i],stmids[j],ikill,len(btcs),btcs
                    print 'WWW do no del btcs'

            stmids=btcs.keys()

        return(stmids,btcs)


    def getDtg(self,dtg,dupchk=1,gdisttol=60.0,verb=0):

        try:
            btcs=self.stmdtg[dtg]
            stmids=btcs.keys()
        except:
            stmids=[]
            btcs={}

        if(dupchk and len(btcs) > 1):
            (stmids,btcs)=self.dupChkBtcs(stmids,btcs,gdisttol)

        return(stmids,btcs)


    def getDtgByBasin(self,dtg,basin):

        (stmids,btcs)=self.getDtg(dtg)
        
        ostmids=[]
        obtcs={}
            
        if(len(stmids) > 0):

            from TCtrk import getBasinLatLons

            try:
                (lat1,lat2,lon1,lon2)=getBasinLatLons(basin)
                for stmid in stmids:
                    lat=btcs[stmid][0]
                    lon=btcs[stmid][1]
                    inlat=(lat >= lat1 and lat <= lat2)
                    inlon=(lon >= lon1 and lon <= lon2)
                    if(inlat and inlon):
                        ostmids.append(stmid)
                        obtcs[stmid]=btcs[stmid]

            except:
                None

        return(ostmids,obtcs)

    def getStmidDtg(self,dtg,dupchk=1):
        (stmids,btcs)=self.getDtg(dtg,dupchk=dupchk)
        return(stmids)


    def getStmidBtcsDtg(self,dtg,dupchk=1):
        (stmids,btcs)=self.getDtg(dtg,dupchk=dupchk)
        return(stmids,btcs)


    def getBtcsDtg(self,dtg):

        year=dtg[0:4]
        btcs={}
        stmids=self.getStmidDtg(dtg)
        for stmid in stmids:
            md=self.mdDSs.getDataSet(key=year)
            #kk=md.bts[stmid].keys()
            #kk.sort()
            #print kk
            try:
                btcs[stmid]=md.bts[stmid][dtg]
            except:
                btcs[stmid]=None

        return(btcs)



    def getGenDtg(self,dtg,dupchk=1,gdisttol=60.0,verb=0):

        gtcs={}
        stmids=[]
        try:
            gtc=self.gendtg[dtg]
        except:
            return(stmids,gtcs)
        for gt in gtc:
            stmid=gt[0]
            stmids.append(stmid)
            gtcs[stmid]=gt[1:]

        stmids=MF.uniq(stmids)

        if(dupchk and len(gtcs) > 1):
            (stmids,gtcs)=self.dupChkBtcs(stmids,gtcs,gdisttol)


        return(stmids,gtcs)


    def getGenTcsDtg(self,dtg):
        (stmids,gtcs)=self.getGenDtg(dtg)
        return(gtcs)


    def getGenDtgByBasin(self,dtg,basin):
        
        from TCtrk import getBasinLatLons

        gtcs={}
        stmids=[]

        try:
            gtc=self.gendtg[dtg]
        except:
            return(stmids,gtcs)


        for gt in gtc:
            stmid=gt[0]

            try:
                (lat1,lat2,lon1,lon2)=getBasinLatLons(basin)
                lat=gt[1]
                lon=gt[2]
                inlat=(lat >= lat1 and lat <= lat2)
                inlon=(lon >= lon1 and lon <= lon2)
                if(inlat and inlon):
                    stmids.append(stmid)
                    gtcs[stmid]=gt[1:]
            except:
                None

        stmids=MF.uniq(stmids)
        return(stmids,gtcs)


    def getBt(self,stmid):

        self.stmid=stmid.upper()
        self.year=stmid.split('.')[1]

        self.md=self.mdDSs.getDataSet(key=self.year)
        bts=self.md.bts[self.stmid]

        return(bts)


    def getGt(self,stmid):

        self.stmid=stmid.upper()
        self.year=stmid.split('.')[1]
        self.md=self.mdDSs.getDataSet(key=self.year)
        try:
            gts=self.md.gts[stmid]
        except:
            gts={}
        return(gts)


    def getFullBtLatLonVmax(self,stmid):

        bts=self.getBt(stmid)

        dtgs=bts.keys()
        dtgs.sort()

        obts={}

        for dtg in dtgs:
            btc=bts[dtg]
            lat=btc[0][0]
            lon=btc[0][1]
            vmax=btc[0][2]
            obts[dtg]=(lat,lon,vmax)

        return(obts)

    def getBtLatLonVmax(self,stmid):

        bts=self.sbts[stmid.upper()]

        dtgs=bts.keys()
        dtgs.sort()

        obts={}

        for dtg in dtgs:
            btc=bts[dtg]
            lat=btc[0]
            lon=btc[1]
            vmax=btc[2]
            obts[dtg]=(lat,lon,vmax)

        return(obts)


    def getStmDtgs(self,stmid):

        bts=self.sbts[stmid.upper()]
        dtgs=bts.keys()
        dtgs.sort()
        return(dtgs)


    def getBtLatLonVmaxPmin(self,stmid):

        bts=self.sbts[stmid]

        dtgs=bts.keys()
        dtgs.sort()

        obts={}

        for dtg in dtgs:
            btc=bts[dtg]
            lat=btc[0]
            lon=btc[1]
            vmax=btc[2]
            pmin=btc[3]
            obts[dtg]=(lat,lon,vmax,pmin)

        return(lat,lon,vmax,pmin)

    def getBtAge(self,stmid,tdtg):

        bts=self.getBt(stmid)

        dtgs=bts.keys()
        dtgs.sort()

        obts={}

        age=0.0
        for dtg in dtgs:
            btc=bts[dtg]
            dt=mf.dtgdiff(dtg,tdtg)
            tcflg=btc[4][0]
            if(tcflg == 'TC'):
                age=dt
                break

        return(age)

    def getGtLatLonVmax(self,stmid):

        gts=self.getGt(stmid)

        dtgs=gts.keys()
        dtgs.sort()

        ogts={}

        for dtg in dtgs:
            gtc=gts[dtg]
            lat=gtc[0]
            lon=gtc[1]
            vmax=gtc[2]
            ogts[dtg]=(lat,lon,vmax)

        return(ogts)


    def getStmName3id(self,stmid):
        
        stm3id=stmid.split('.')[0].upper()
        stmyear=stmid.split('.')[1]

        tcnames=GetTCnamesHash(stmyear)

        kk=tcnames.keys()

        stmname='unknown'
        stmname=stmname.upper()
        
        for k in kk:
            stm3=k[1]
            if(stm3 == stm3id): stmname=tcnames[k]

        return(stm3id,stmname)

        
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

        
    def getStmidFrom3id(self,snum,dtg):

        stmyear=dtg[0:4]
        if(isShemBasinStm(snum)):
            stmyear=getShemYear(dtg)

        stmid="%s.%s"%(snum.upper(),stmyear)
        
        return(stmid)

        
            
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

        



    def getTcvitals(self,dtg,verb=0):


        def parseTcv(tcvcard,undef=-999.0,verb=0):

            tt=tcvcard.split()
            (centerid,stm3id,stmname,
                       yyyymmdd,hh,
                       clat,clon,
                       vitdir,vitspd,
                       vitpmin,
                       vitpoci,vitroci,
                       vitvmax,vitrmax,
                       vitr34ne,vitr34se,vitr34sw,vitr34nw,
                       vitdepth)=tt

            vitpmin=int(vitpmin)*1.0
            vitdir=int(vitdir)*1.0
            vitspd=int(vitspd)*ms2knots*0.1
            vitspd=int(vitspd+0.5)*1.0
            vitpoci=int(vitpoci)*1.0
            vitroci=int(vitroci)*km2nm

            if(vitroci < 0.0):
                vitroci=undef
            else:
                vitroci=(int(vitroci+0.5)/5.0)*5.0

            vitvmax=int(vitvmax)*ms2knots
            vitvmax=int((vitvmax+1.0)/5.0)*5.0

            vitrmax=int(vitrmax)*km2nm
            if(vitrmax < 0):
                vitrmax=undef
            else:
                vitrmax=(int(vitrmax+0.5)/5.0)*5.0
            
            vitr34ne=int(vitr34ne)*km2nm
            vitr34se=int(vitr34se)*km2nm
            vitr34sw=int(vitr34sw)*km2nm
            vitr34nw=int(vitr34nw)*km2nm

            (vitlat,vitlon,ilat,ilon,hemns,hemew)=Clatlon2Rlatlon(clat,clon)
            
            vitr34=[]
            if(vitr34ne < 0.0):
                vitr34ne=undef
            else:
                vitr34ne=int((vitr34ne+0.5)/5.0)*5.0
            vitr34.append(vitr34ne)
                
            if(vitr34se < 0.0):
                vitr34se=undef
            else:
                vitr34se=int((vitr34se+0.5)/5.0)*5.0
            vitr34.append(vitr34se)
            
            if(vitr34sw < 0.0):
                vitr34sw=undef
            else:
                vitr34sw=int((vitr34sw+0.5)/5.0)*5.0
            vitr34.append(vitr34sw)

            if(vitr34nw < 0.0):
                vitr34nw=undef
            else:
                vitr34nw=int((vitr34nw+0.5)/5.0)*5.0
            vitr34.append(vitr34nw)

            vitr34bar=0.0
            n34=0
            for vr in vitr34:
                if(vr > 0.0):
                    n34=n34+1
                    vitr34bar=vitr34bar+vr

            if(n34 > 0):
                vitr34bar=vitr34bar/n34
            else:
                vitr34bar=undef
                    

            if(verb):
                print 'lat/lon: ',vitlat,vitlon
                print 'dir/spd: ',vitdir,vitspd
                print 'p/roci:  ',vitpoci,vitroci
                print 'vmax:    ',vitvmax,vitrmax
                print 'r34:     ',vitr34,vitr34bar
                print 'deep:    ',vitdepth


            return(vitlat,vitlon,vitdir,vitspd,vitvmax,vitrmax,vitpoci,vitroci,vitr34bar,vitdepth)

            
        tcvitals={}
        
        tcvitalsdtg=self.tcvitalsdtg[dtg]
        stmdtg=self.stmdtg[dtg]
        
        stmids=stmdtg.keys()
        stmids.sort()

        for stmid in stmids:
            rc=stmdtg[stmid]
            tcvcard=tcvitalsdtg[stmid][0]
            rc=parseTcv(tcvcard)
            (vitlat,vitlon,vitdir,vitspd,vitvmax,vitrmax,vitpoci,vitroci,vitr34bar,vitdepth)=rc
            tcvitals[stmid]=rc

        return(tcvitals)


            
            

    def makeTcvitals(self,dtg,basin=None,override=0,verb=0):

        if(basin == None):
            self.tcvpath="%s/tcvitals2.%s.txt"%(TcVitalsDatDir,dtg)
        else:
            self.tcvpath="%s/tcvitals2.%s.%s.txt"%(TcVitalsDatDir,basin,dtg)

        # -- bail if not override and/or path !exist -- takes about 8 s to check!
        #
        if( not(override or not(MF.ChkPath(self.tcvpath))) ): return
        
        if(basin != None):
            from TCtrk import getBasinLatLons
            (lat1,lat2,lon1,lon2)=getBasinLatLons(basin)


        tcvitals=[]
        
        tcvitalsdtg=self.tcvitalsdtg[dtg]
        stmdtg=self.stmdtg[dtg]
        
        stmids=stmdtg.keys()
        stmids.sort()

        for stmid in stmids:

            rc=stmdtg[stmid]
            tcvcard=tcvitalsdtg[stmid]
            
            blat=rc[0]
            blon=rc[1]

            # -- is doing by basin, check blat,blon...
            #
            if(basin != None):
                inlat=(blat >= lat1 and blat <= lat2)
                inlon=(blon >= lon1 and blon <= lon2)
                if(not(inlat and inlon)): continue

            tcvitals.append(tcvcard[0])


        if( override or not(MF.ChkPath(self.tcvpath)) ):
            MF.WriteList2File(tcvitals,self.tcvpath,verb=verb)


class TCutils(TcData):

    # -- reduced version of TcData the only sets up methods
    #
    
    def __init__(self,
             verb=0,
             ):

        self.verb=verb




#uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu
# unbounded methods
#

def getSaffirSimpsonCat(vmax):

    if(vmax < 35.0): cat='TD'
    if(vmax >= 35.0 and vmax < 65.0): cat='TS'
    if(vmax >= 64.0 and vmax <= 82.0): cat='HU1'
    if(vmax >= 83.0 and vmax <= 95.0): cat='HU2'
    if(vmax >= 96.0 and vmax <= 113.0): cat='HU3'
    if(vmax >= 114.0 and vmax <= 135.0): cat='HU4'
    if(vmax > 135.0): cat='HU5'

    return(cat)


def getTyphoonCat(vmax):

    if(vmax < 35.0): cat='td'
    if(vmax >= 35.0 and vmax < 65.0): cat='ts'
    if(vmax >= 64.0 and vmax < 100.0): cat='ty'
    if(vmax >= 100.0 and vmax < 135.0): cat='Mty'
    if(vmax >= 135.0): cat='STY'

    return(cat)

    


def stm1idTostm2id(stm1id):

    b1id=stm1id[2].upper()
    snum=stm1id[0:2]
    b2id=Basin1toBasin2[b1id]
    stm2id=b2id + snum + '.'+stm1id.split('.')[1]
    stm2id=stm2id.lower()
    return(stm2id)


def stm2idTostm1id(stm2id):

    b2id=stm2id[0:2].upper()
    snum=stm2id[2:4]
    b1id=Basin2toBasin1[b2id]
    stm1id=snum + b1id + '.'+stm2id.split('.')[1]
    return(stm1id)



def basin2Chk(b2id):
    """
    convert local b2id to standard atcf b2id
    """
    
    if(b2id == 'SI' or b2id == 'SP' or b2id == 'SL'):
        b2id='SH'

    elif(b2id == 'AA' or b2id == 'BB' or b2id == 'NI' or b2id == 'NA'):
        b2id='IO'

    elif(b2id == 'AT'):
        b2id='AL'
        
    return(b2id)


def getShemYear(dtg):
    """
     convert year in stm dtg to basinyear
    """

    yyyy=int(dtg[0:4])
    mm=int(dtg[4:6])

    if(mm >= 7): yyyy=yyyy+1
    cyyyy=str(yyyy)
    return(cyyyy)


def isShemBasinStm(stmid):

    tt=stmid.split('.')
    stmid=tt[0]

    if(len(stmid) != 3 and len(stmid) != 1 and len(stmid) != 4):
        return(-1)

    if(len(stmid) == 3):
        ustmid=stmid[2].upper()
    elif(len(stmid) == 1):
        ustmid=stmid.upper()
    elif(len(stmid) == 4):
        ustmid=stmid[0:2].upper()

    if(len(ustmid) == 1):
        if(ustmid == 'S' or ustmid == 'P' or ustmid == 'Q'):
            return(1)
        else:
            return(0)
    elif(len(ustmid) == 2):
        if(ustmid == 'SH' or ustmid == 'SP' or ustmid == 'SI' or ustmid == 'SL'):
            return(1)
        else:
            return(0)


def GetTCnamesHash(yyyy,source=''):

    ndir=TcNamesDatDir
    sys.path.append(ndir)
    if(source == 'neumann'):
        impcmd="from TCnamesNeumann%s import tcnames"%(yyyy)
    else:
        impcmd="from TCnames%s import tcnames"%(yyyy)
    exec(impcmd)
    return(tcnames)


def GetTCstatsHash(yyyy,source=''):
    
    ndir=TcNamesDatDir
    sys.path.append(ndir)
    if(source == 'neumann'):
        impcmd="from TCstatsNeumann%s import tcstats"%(yyyy)
    elif(source == 'ops'):
        impcmd="from TCstatsOps%s import tcstats"%(yyyy)
    else:
        impcmd="from TCstats%s import tcstats"%(yyyy)
    exec(impcmd)
    return(tcstats)

def Clatlon2Rlatlon(clat,clon):

    if(len(clat) == 1):
        return(0.0,0.0,0,0,'X','X')
    
    hemns=clat[len(clat)-1:]
    hemew=clon[len(clon)-1:]
    ilat=clat[0:(len(clat)-1)]
    rlat=int(ilat)*0.1
    ilon=clon[0:(len(clon)-1)]
    rlon=int(ilon)*0.1

    if(hemns == 'S'):
        rlat=-rlat
        
    if(hemew == 'W'):
        rlon=360.0-rlon

    return(rlat,rlon,ilat,ilon,hemns,hemew)

def Rlatlon2Clatlon(rlat,rlon,dotens=1):

    hemns='X'
    hemew='X'
    ilat=999
    ilon=9999
    
    if(rlat > -90.0 and rlat < 88.0):

        if(dotens):
            ilat=mf.nint(rlat*10)
        else:
            ilat=mf.nint(rlat)

        hemns='N'
        if(ilat<0):
            ilat=abs(ilat)
            hemns='S'

        if(rlon > 180.0):
            rlon=360.0-rlon
            hemew='W'
        else:
            hemew='E'
            
        if(rlon < 0.0):
            rlon=abs(rlon)
            hemew='W'

        if(dotens):
            ilon=mf.nint(rlon*10)
        else:
            ilon=mf.nint(rlon)

    if(dotens):
        clat="%03d%s"%(ilat,hemns)
        clon="%04d%s"%(ilon,hemew)
        clat="%3d%s"%(ilat,hemns)
        clon="%4d%s"%(ilon,hemew)
    else:
        clat="%2d%s"%(ilat,hemns)
        clon="%3d%s"%(ilon,hemew)
    
    return(clat,clon,ilat,ilon,hemns,hemew)


def CurShemOverlap(curdtg):

    #
    # need to run twice in overlap between shem and nhem seasons
    #

    cy=curdtg[0:4]
    
    
    icym0=int(cy)
    icyp1=icym0+1
    cyp1=str(icyp1)
    
    icymd0=int(curdtg[0:8])

    ccymd0e=str(icym0)+'1231'
    icymd0e=int(ccymd0e)

    ccymdshemb=str(icym0)+'0701'
    icymdshemb=int(ccymdshemb)

    shemoverlap=0
    if(icymd0 >= icymdshemb and icymdshemb <= icymd0e): shemoverlap=1

    return(shemoverlap,cy,cyp1)

def gc_dist(rlat0,rlon0,rlat1,rlon1):

    #
    # based on sherical law of cosines 
    #
    
    dlat=abs(rlat0-rlat1)
    dlon=abs(rlon0-rlon1)
    zerotest=(dlat<epsilon and dlon<epsilon)
    if(zerotest): return(0.0)
    
    f1=deg2rad*rlat0
    f2=deg2rad*rlat1
    rm=deg2rad*(rlon0-rlon1)
    finv=cos(f1)*cos(f2)*cos(rm)+sin(f1)*sin(f2)
    rr=rearth*acos(finv)
    if(tcunits =='english'): rr=rr*km2nm 

    return(rr)


def mercat(rlat,rlon):

    lat=rlat*deg2rad

    if(rlon < 0.0):
        lon=360.0+rlon
    else:
        lon=rlon
        
    x=lon*deg2rad
    y=log(tan(pi4+lat*0.5))

    return(x,y)

def gc_theta(blat1,blon1,flat1,flon1):

    verb=0
    (xa,ya)=mercat(flat1,flon1)
    (xr,yr)=mercat(blat1,blon1)

    difx=xa-xr
    dify=ya-yr

    difx=difx*rad2deg*deglat2nm
    dify=dify*rad2deg*deglat2nm

    if (difx == 0.0):

        if(dify >= 0.0): theta=pi2
        if(dify < 0.0): theta=3*pi/2.0 

    else:

        slope=dify/difx
        if (abs(slope) < 1e-10):
            if(dify >= 0.0): theta=pi2 
            if(dify <= 0.0): theta=pi
        else:
            theta=atan2(dify,difx)
            #if(theta < 0.0):
            #   theta=theta + 2.0*pi
            theta=theta*rad2deg
            return(difx,dify,theta)
        
            if (difx > 0.0):
                if(dify < 0.0): theta=pi-theta
            else:
                if (dify > 0.0):
                    theta=2*pi+theta
                    theta=theta
                else:
                    theta=pi+theta
                    theta=theta

    
    #if(theta < 0.0):
    #    theta=theta + 2.0*pi

    theta=theta*rad2deg
    return(difx,dify,theta)


def dist_err(blat,blon,blat1,blon1,flat,flon):

    verb=0
    (xa,ya)=mercat(flat,flon)
    (xb,yb)=mercat(blat,blon)
    (xr,yr)=mercat(blat1,blon1)

    difx=xb-xr
    dify=yb-yr

    if (difx == 0.0):

      if(dify >= 0.0): theta=0.0
      if(dify < 0.0): theta=pi 

    else:

      slope=dify/difx
      if (abs(slope) < 1e-10):
          if(difx > 0): theta=pi2 
          if(difx < 0): theta=3*pi/2.0
      else:
        theta=atan(1./slope)
        if (difx > 0.0):
          if(dify < 0.0): theta=pi-theta
        else:
           if (dify > 0.):
             theta=2*pi+theta
           else:
             theta=pi+theta

    biasx=cos(theta)*(xa-xb)-sin(theta)*(ya-yb)
    biasy=sin(theta)*(xa-xb)+cos(theta)*(ya-yb)
    factor=cos(deg2rad*(blat+flat)*0.5)
    biasx=biasx*rearth*factor
    biasy=biasy*rearth*factor

    biasew=(xa-xb)*rearth*factor
    biasns=(ya-yb)*rearth*factor
    rr=sqrt(biasx*biasx+biasy*biasy)
    #dist_x=abs(biasx)
    #dist_y=abs(biasy)

    if(tcunits =='english'):
        rr=rr*km2nm
        biasx=biasx*km2nm
        biasy=biasy*km2nm
        biasew=biasew*km2nm
        biasns=biasns*km2nm
        

    if(verb):
        print "mmm ",blat,blon,flat,flon,rr,biasx,biasy

    return(rr,biasx,biasy,biasew,biasns)


def rumltlg(course,speed,dt,rlat0,rlon0):

    ####  print "qqq course,speed,dt,rlat0,rlon0\n"
    #c****	    routine to calculate lat,lon after traveling "dt" time
    #c****	    along a rhumb line specifed by the course and speed
    #c****	    of motion
    #
    #--- assume DEG E!!!!!!!!!!!!!!!!!!!!!!!!
    #
    #  assume speed is in kts and dt is hours
    #
    #      
    distnce=speed*dt
    
    icrse=int(course+0.01)

    if(icrse == 90.0 or icrse == 270.0):

    #      
    #*****		  take care of due east and west motion
    #
        dlon=distnce/(60.0*cos(rlat0*deg2rad))
        if(icrse == 90.0): rlon1=rlon0+dlon
        if(icrse == 270.0): rlon1=rlon0-dlon 
        rlat1=rlat0
    else:
        rlat1=rlat0+distnce*cos(course*deg2rad)/60.0
        d1=(45.0+0.5*rlat1)*deg2rad
        d2=(45.0+0.5*rlat0)*deg2rad
        td1=tan(d1)
        td2=tan(d2)
        #
        # going over the poles!
        #
        if(abs(rlat0) >= 90.0 or abs(rlat1) >= 90.0):
            rlat1=rlon1=None
        else:
            rlogtd1=log(td1)
            rlogtd2=log(td2)
            rdenom=rlogtd1-rlogtd2 
            rlon1=rlon0+(tan(course*deg2rad)*rdenom)*rad2deg

    return(rlat1,rlon1)


def rumhdsp(rlat0,rlon0,rlat1,rlon1,dt,units=tcunits,opt=0):

    verb=0

    if(verb):
        print "***** ",rlat0,rlon0,rlat1,rlon1,dt,units,opt

    if(units == 'metric'):
        distfac=111.19
        spdfac=0.2777
    else:
        distfac=60.0
        spdfac=1.0


    #
    # assumes deg W
    #
    rnumtor=(rlon0-rlon1)*deg2rad

    #
    #--- assume DEG E!!!!!!!!!!!!!!!!!!!!!!!!
    #

    rnumtor=(rlon1-rlon0)*deg2rad
    d1=(45.0+0.5*rlat1)*deg2rad
    d2=(45.0+0.5*rlat0)*deg2rad

    td1=tan(d1)
    td2=tan(d2)
    rlogtd1=log(td1)
    rlogtd2=log(td2)
    rdenom=rlogtd1-rlogtd2
    rmag=rnumtor*rnumtor + rdenom*rdenom

    course=0.0
    if(rmag != 0.0):
        course=atan2(rnumtor,rdenom)*rad2deg

    if(course <= 0.0):  
        course=360.0+course

    #
    #...     now find distance
    #

    icourse=int(course+0.1)
    if(icourse ==  90.0 or icourse == 270.0 ):
        distance=distfac*abs(rlon0-rlon1)*cos(rlat0*deg2rad)
    else:
        distance=distfac*abs(rlat0-rlat1)/abs(cos(course*deg2rad))

    #
    #...     now get speed
    #
    speed=distance/dt

    #
    #...      convert to u and v motion
    #

    spdmtn=speed*spdfac
    ispeed=int(spdmtn*100+0.5)/100
    angle=(90.0-course)*deg2rad
    
    umotion=spdmtn*cos(angle)
    vmotion=spdmtn*sin(angle)
    iumotion=int(umotion*100+0.5)/100
    ivmotion=int(vmotion*100+0.5)/100
    rumotion=float(iumotion)
    rvmotion=float(ivmotion)
    rcourse=float(course)
    rspeed=float(spdmtn)
    if(verb):
        print "%5.2f %4.0f %5.2f %5.2f %5.2f %5.2f\n"%\
              (distance,icourse,spdmtn,angle,umotion,vmotion)
        
    return(rcourse,rspeed,umotion,vmotion)



def VeriTcFlag(tcind,tcwarn):
    vflg=0
    if(tcind == 'TC' or tcwarn == 'WN'):
        vflg=1

    return(vflg)

def getB2idSnumFromPath(dpath,filter=1):
    (dir,file)=os.path.split(dpath)
    b2id=file[1:3]
    snum=file[3:5]
    if(filter):
        if(not(snum.isdigit())):
            snum=-1
        else:
            snum=int(snum)
            if(snum >= 80 and snum <= 89): snum=-1
    return(b2id,snum)
    

def IsJtwcBasin(b1id):
    bid=b1id.lower()
    rc=0
    if(len(bid) == 1  and
       bid == 'w' or bid == 'b' or bid == 'a' or
       bid == 's' or bid == 'p'
       ):
        rc=1
        
    # overlap
    #
    elif(len(bid) == 1  and
       bid == 'e' or bid == 'c'
       ):
        rc=2
        
    elif(len(bid) == 2 and
         b1id == 'wp' or b1id == 'io' or b1id == 'sh'):
        rc=1

    # overlap
    #
    elif(len(bid) == 2 and
         b1id == 'ep' or b1id == 'cp'):
        rc=2
        
    return(rc)

def IsNhcBasin(b1id):
    
    bid=b1id.lower()
    
    if(len(bid) == 1):
        bid=b1id.lower()
    elif(len(bid) >= 3):
        # assume stmid if not 1char
        tt=b1id.split('.')
        bid=tt[0][2].lower()
        
    rc=0
    if(len(bid) == 1 and
        bid == 'l' or bid == 'e' or bid == 'c'
        ):
        rc=1
    elif(len(bid) == 2 and
        bid == 'al' or bid == 'ep' or bid == 'cp'
        ):
        rc=1
        
    return(rc)

    

def IsTc(tcstate):
    #
    # if tc = 1
    # if stc = 2
    # if neither = 0
    #
    if(
        tcstate == 'TD' or
        tcstate == 'TS' or
        tcstate == 'TY' or
        tcstate == 'HU' or
        tcstate == 'ST' or
        tcstate == 'TC'
        ):
        tc=1
    elif(
        tcstate == 'SS' or
        tcstate == 'SD'
        ):
        tc=2
    elif(
        tcstate.lower() == 'xx'
        ):
        tc=-1
    else:
        tc=0

    return(tc)

#
# if tcflag not in bdeck, use find
#

def IsTcWind(vmax):

    tc=0
    if(vmax >= TCvmin): tc=1
    return(tc)


def IsWarn(warnstate):
    #
    # if tc = 1
    # if stc = 2
    # if neither = 0
    #
    if(
        warnstate == 'WN'
        ):
        warn=1
    else:
        warn=0

    return(warn)
    
    

def IsTcList(tt):
  
    try:
        vmax=int(tt[2])
        tcstate=tt[13]
        warnstate=tt[15]
    except:
        try:
            vmax=int(tt[2])
            tcstate=tt[12]
            warnstate=tt[14]
        except:
            vmax=0
            tcstate='xx'
            
    if(vmax >= TCvmin and (tcstate.lower() == 'xx' )): tcstate='TC'
    
    tc=IsTc(tcstate)

    return(tc)
    

def IsWarnList(tt):
  
    try:
        vmax=int(tt[2])
        tcstate=tt[13]
        warnstate=tt[15]
    except:
        try:
            vmax=int(tt[2])
            tcstate=tt[12]
            warnstate=tt[14]
        except:
            tcstate='xx'

    if(vmax >= TCvmin and (tcstate.lower() == 'xx' )): tcstate='TC'
    
    warn=IsWarn(warnstate)

    return(tc)
    

def MakeStmList(stmopt,dofilt9x=0,verb=0):

    def add2000(y):
        if(len(y) == 1):
            yyyy=str(2000+int(y))
        elif(len(y) == 2):
            if(int(y) > 25):
                yyyy=str(1900+int(y))
            else:
                yyyy=str(2000+int(y))

        else:
            yyyy=y
        return(yyyy)


    def getyears(yyy):

        if(yyy == 'cur'):
            curdtg=mf.dtg()
            yyy=curdtg[0:4]
            
        years=[]
        n1=0
        n2=0
        
        tt0=yyy.split('-')
        tt1=yyy.split(',')

        if(len(tt1) > 1):
            for tt in tt1:
                yyyy=add2000(tt)
                years.append(yyyy)
            return(years)
        
        if(len(tt0) > 1):
            y1=tt0[0]
            y2=tt0[1]
            yyyy1=add2000(y1)
            yyyy2=add2000(y2)
            
            if(len(yyyy1) != 4 or len(yyyy2) != 4):
                print 'EEEE getyears tt:',tt
                return(None)

            else:
                n1=int(yyyy1)
                n2=int(yyyy2)
                for n in range(n1,n2+1):
                    years.append(str(n))

        else:
            if(len(yyy) <= 2): yyy=add2000(yyy)
            years=[yyy]

        return(years)
        

    def getstmids(sss,year):
        
        sids=[]
        n1=0
        n2=0
        tt=sss.split('-')

        if(len(tt) > 1):
            if(len(tt[0]) != 2 or len(tt[1]) != 3):
                print 'EEEE getstmids tt:',tt
                return(None)

            else:
                n1=int(tt[0])
                n2=int(tt[1][0:2])
                bid=tt[1][2].upper()

                for n in range(n1,n2+1):
                    sid="%02d%1s.%s"%(n,bid,year)
                    sids.append(sid)
                    
        elif(len(sss) == 1):
            tcnames=GetTCnamesHash(year)
            bchk=sss.upper()
            for tcname in tcnames:
                if(tcname[1][2:3] == bchk):
                    sid="%s.%s"%(tcname[1],tcname[0])
                    sids.append(sid)
                else:
                    sid=None

            
        elif(len(tt) == 1):

            if(len(sss) == 3):

                if(sss[0].upper() == 'M'):
                    nback=int(sss[1])
                    bchk=sss[2].upper()
                    tcnames=GetTCnamesHash(year)
                    for tcname in tcnames:
                        if(tcname[1][2:3] == bchk):
                            sid="%s.%s"%(tcname[1],tcname[0])
                            sids.append(sid)
                        else:
                            sid=None

                    sids.sort()
                    osids=[]
                    
                    nsids=len(sids)
                    for n in range(nsids-nback,nsids):
                        osids.append(sids[n])

                    return(osids)


                else:
                    
                    sid="%s.%s"%(sss.upper(),year)
                    sids.append(sid)
                


        else:
            print 'EEEE getstmids sss:',sss
            return(None)
            

        sids.sort()
        return(sids)

    #
    # start.......................
    #
    
    ttt=stmopt.split('-')
    ttc=stmopt.split(',')
    tt=stmopt.split('.')
    
    curdtg=mf.dtg()
    curyear=curdtg[0:4]


    #
    # single storm
    #

    if(stmopt != None and stmopt != 'all'):
        
        if(len(tt) == 1 and len(ttt) == 1 and len(ttc) == 1):
            if(len(tt[0]) == 3):
                stmid=tt[0][2]
            elif(len(tt[0]) != 1):
                print 'EEEE bad stm3id: ',tt[0],tt
                sys.exit()
            else:
                stmid=tt[0]

            if(isShemBasinStm(stmid)):
                stmyear=getShemYear(curdtg)
            else:
                stmyear=curyear
            stmyear=add2000(stmyear)

            stmopt=stmopt+'.'+stmyear
            tt=stmopt.split('.')

        #
        # stm spanning using current year
        #
        elif(len(ttt) > 1 and len(ttc) == 1 and len(tt) == 1):

            stmids=getstmids(stmopt,curyear)
            return(stmids)


        #
        # list of individual stmid (sss.y)
        #

        if(len(ttc) > 1):

            stmids=[]
            for stmopt in ttc:
                stmids=stmids+MakeStmList(stmopt,dofilt9x,verb)

            return(stmids)


        if(len(ttc) > 1 and len(tt) > 2):

            stmids=[]

            for stmid in ttc:
                ss1=stmid.split('.')
                if(len(ss1) != 2):
                    print 'EEE invalid individual stm: ',stmmid
                    sys.exit()

                sid=ss1[0]
                yid=ss1[1]
                if(len(yid) >= 1): yid=add2000(yid)
                rc=getstmids(sid,yid)
                stmids=stmids+rc

            return(stmids)

        sopt=tt[0]
        yopt=tt[1]
        years=getyears(yopt)

    else:
        
        sopt='w,e,c,l,i,a,b,p,s'
        yopt='cur'
        years=getyears(yopt)


    if(verb):
        print 'ssssssssssss sopt: ',sopt
        print 'yyyyyyyyyyyy yopt: ',yopt,years
    

    stmids=[]

    for year in years:

        ss=sopt.split(',')
        if(len(ss) > 1):
            for sss in ss:
                rc=getstmids(sss,year)
                if(rc != None):
                    stmids=stmids+rc

        else:
            rc=getstmids(sopt,year)
            if(rc != None):
                stmids=stmids+rc

    #
    # filter out 9X
    #
    
    if(dofilt9x):
        nstmids=[]
        for stmid in stmids:
            num=int(stmid[0:2])
            if(num < 80):
                nstmids.append(stmid)

        stmids=nstmids
        

    if(verb):
        for stmid in stmids:
            print 'ssxsssssssss ',stmid

    return(stmids)


def ParseMdeckCard2Btcs(mdcard):
    

#new format for mdeck
#
#  0 2007090800
#  1 09L.2007
#  2 020
#  3 1009
#  4 23.5
#  5 274.5
#  6 -999
#  7 -999
#  8 360.0
#  9 0.0
#  10 0
#  11 FL:
#  12 NT
#  13 DB
#  14 NC
#  15 NC
#  16 NW
#  17 LF:
#  18 0.00
#  19 TDO:
#  20 ___
#  21 C:
#  22 -99.9
#  23 -999.9
#  24 -999
#  25 999.9
#  26 99.9
#  27 ______
#  28 W:
#  29 -99.9
#  30 -999.9
#  31 -999
#  32 999.9
#  33 99.9
#  34 RadSrc:
#  35 none
#  36 r34:
#  37 -999
#  38 -999
#  39 -999
#  40 -999
#  41 r50:
#  42 -999
#  43 -999
#  44 -999
#  45 -999
#  46 CP/Roci:
#  47 9999.0
#  48 999.0
#  49 CRm:
#  50 999.0
#  51 CDi:
#  52 999.0
#  53 Cdpth:
#  54 K

    tt=mdcard.split()
    ntt=len(tt)

    #for n in range(0,ntt):
    #    print 'mmmmmmm ',n,tt[n]

    i=0

    dtg=tt[i] ; i=i+1
    sid=tt[i] ; i=i+1
    bvmax=float(tt[i])  ; i=i+1
    bpmin=float(tt[i]) ; i=i+1
    blat=float(tt[i]) ; i=i+1
    blon=float(tt[i]) ; i=i+1
    r34=float(tt[i]) ; i=i+1
    r50=float(tt[i]) ; i=i+1
    bdir=float(tt[i]) ; i=i+1
    bspd=float(tt[i]) ; i=i+1
    tsnum=int(tt[i]) ; i=i+1
    dum=tt[i] ; i=i+1
    flgtc=tt[i] ; i=i+1
    flgind=tt[i] ; i=i+1
    flgcq=tt[i] ; i=i+1
    flgwn=tt[i] ; i=i+1
    dum=tt[i] ; i=i+1
    lf=float(tt[i]) ; i=i+1
    dum=tt[i] ; i=i+1
    tdo=tt[i] ; i=i+1

    ic=21
    cqlat=float(tt[ic])  ; ic=ic+1
    cqlon=float(tt[ic])  ; ic=ic+1
    cqvmax=float(tt[ic]) ; ic=ic+1
    cqdir=float(tt[ic])  ; ic=ic+1
    cqspd=float(tt[ic])  ; ic=ic+1
    cqpmin=float(tt[ic])  ; ic=ic+1

    iw=29
    wlat=float(tt[iw])  ; iw=iw+1
    wlon=float(tt[iw])  ; iw=iw+1
    wvmax=float(tt[iw]) ; iw=iw+1

    if(ntt == 55):
        ir=37
        r34ne=int(tt[ir]) ; ir=ir+1
        r34se=int(tt[ir]) ; ir=ir+1
        r34sw=int(tt[ir]) ; ir=ir+1
        r34nw=int(tt[ir]) ; ir=ir+2

        r50ne=int(tt[ir]) ; ir=ir+1
        r50se=int(tt[ir]) ; ir=ir+1
        r50sw=int(tt[ir]) ; ir=ir+1
        r50nw=int(tt[ir]) ; ir=ir+2
        
        ir=47
        poci=float(tt[ir]) ; ir=ir+1
        roci=float(tt[ir]) ; ir=ir+2
    
        rmax=float(tt[ir]) ; ir=ir+2
        reye=float(tt[ir]) ; ir=ir+2
        tcdepth=tt[ir]

    else:
        r34ne=r34se=r34sw=r34nw=-999.0
        r50ne=r50se=r50sw=r50nw=-999.0

    r34quad=[r34ne,r34se,r34sw,r34nw]
    r50quad=[r50ne,r50se,r50sw,r50nw]

    if(cqdir > 720.0):
        cqdir=-999.9
        cqspd=-99.9

    btdic=[flgtc,flgind,flgcq,flgwn,tdo,lf,cqlat,cqlon,cqvmax,wlat,wlon,wvmax,tsnum]
    cqdic=[cqlat,cqlon,cqvmax,cqdir,cqspd,cqpmin]
    bwdic=[bvmax,r34,r50,rmax,reye,poci,roci]
    btc=[blat,blon,bvmax,bpmin,bdir,bspd,btdic,cqdic,bwdic,r34quad,r50quad]

    return(btc)



def ParseMdeck2Btcs(dtgs,mdcards):
    
    btcs={}
    
    for dtg in dtgs:
        mdcard=mdcards[dtg]
        btc=ParseMdeckCard2Btcs(mdcard)
        btcs[dtg]=btc

    return(btcs)



def GetMdeckBts(stmid,dofilt9x=1,verb=0):

##    mdcards=findtc(stmid,dofilt9x)
    mdcards=findMdeckTC(stmid,do9x=dofilt9x)
    if(len(mdcards) == 0):
        return(None,None)
    else:
        dtgs=mdcards.keys()
        dtgs.sort()
        bts=ParseMdeck2Btcs(dtgs,mdcards)
        return(dtgs,bts)
        


def findMdeckTC(tstm,do9x=1,verb=0):

    tt=tstm.split('.')

    if(len(tt) != 2):
        print 'EEE invalid tstm in findMdckTC: ',tstm
        sys.exit()

    tstmid=tt[0].upper()
    yyyy=tt[1]

    mddir="%s/%s"%(MdeckBaseDir,yyyy)
    mdmask="%s/mdeck.*.%s.*.txt"%(mddir,tstmid)
    mdpaths=glob.glob(mdmask)

    omdcards={}

    if(len(mdpaths) == 1):
        
        mdpath=mdpaths[0]
        mdcards=open(mdpath).readlines()

        for mdcard in mdcards:
            dtg=mdcard.split()[0]
            omdcards[dtg]=mdcard


    return(omdcards)
    

def GetBtcardsLatLonsFromMdeck(stmid,dtg,nhback=48,nhplus=120,verb=0):

    btcards=[]
    btcardsgt0=[]
    
    lats=[]
    lons=[]
    vmaxs=[]
    pmins=[]

    (btdtgs,btcs)=GetMdeckBts(stmid,dofilt9x=0,verb=verb)

    if(btdtgs == None):
        print 'WWW: no bts for stmid: ',stmid
        return(btcards)

    
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

        (blat,blon,bvmax,bpmin,bdir,bspd,btdic,cqdic,bwdic,r34quad,r50quad)=btcs[dtg]
        (flgtc,flgind,flgcq,flgwn,tdo,lf,cqlat,cqlon,cqvmax,wlat,wlon,wvmax,tsnum)=btdic

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
    dtg0=obtdtgsgt0[0]
    
    for dtg in obtdtgsgt0:
        dt=mf.dtgdiff(dtg0,dtg)
        if(dt%12): continue
        dhplus=mf.dtgdiff(dtg0,dtg)
        if(dhplus > nhplus): continue

        nbt0=nbt0+1

        (blat,blon,bvmax,bpmin,bdir,bspd,btdic,cqdic,bwdic,r34quad,r50quad)=btcs[dtg]
        (flgtc,flgind,flgcq,flgwn,tdo,lf,cqlat,cqlon,cqvmax,wlat,wlon,wvmax,tsnum)=btdic

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

        

def IsWindRadii(code):
    rc=0
    if(code == 'AAA'):
        rc=1
        return(rc)

    if(code == '' or code == '0'): return(rc)
        
        
    if( (code[2] == 'Q' or code[2] == 'S') and
        (
        code[0:2] == 'NN' or
        code[0:2] == 'NE' or
        code[0:2] == 'EE' or
        code[0:2] == 'SE' or
        code[0:2] == 'SS' or
        code[0:2] == 'SW' or
        code[0:2] == 'WW' or
        code[0:2] == 'NW')
        ):
        rc=1

    return(rc)


def WindRadiiCode2Normal(code,radii):

    #
    # convert pre 2004 codes -> ne/se/sw/nw quad standard
    #
    
    #
    # default
    #
    rne=rse=rsw=rnw=-999.
    
    if(radii[0] > 0): rne=float(radii[0])
    if(radii[1] > 0): rne=float(radii[1])
    if(radii[2] > 0): rne=float(radii[2])
    if(radii[3] > 0): rne=float(radii[3])
    
    if(len(code) != 3):
        print 'EEE atcf: invalid wind radii code: ',code
        sys.exit()
    
#AAA - full circle
    if(code == 'AAA'):
        rne=rse=rsw=rnw=radii[0]

#NNS - north semicircle
    elif(code == 'NNS'):
        rne=rnw=radii[0]
        rse=rsw=radii[1]

#NES - northeast semicircle
    elif(code == 'NES'):
        rne=radii[0]
        rse=0.5*radii[0]+0.5*radii[1]
        rsw=radii[1]
        rnw=0.5*radii[0]+0.5*radii[1]

#EES - east semicircle
    elif(code == 'EES'):
        rne=rse=radii[0]
        rnw=rsw=radii[1]

#SES - southeast semicircle
    elif(code == 'SES'):
        rse=radii[0]
        rsw=0.5*radii[0]+0.5*radii[1]
        rnw=radii[1]
        rne=0.5*radii[0]+0.5*radii[1]

#SSS - south semicircle
    elif(code == 'SSS'):
        rsw=rse=radii[0]
        rne=rnw=radii[1]

#SWS - southwest semicircle
    elif(code == 'SWS'):
        rsw=radii[0]
        rnw=0.5*radii[0]+0.5*radii[1]
        rne=radii[1]
        rse=0.5*radii[0]+0.5*radii[1]

#WWS - west semicircle
    elif(code == 'WWS'):
        rnw=rsw=radii[0]
        rne=rse=radii[1]

#NWS - northwest semicircle
    elif(code == 'NWS'):
        rnw=radii[0]
        rne=0.5*radii[0]+0.5*radii[1]
        rse=radii[1]
        rsw=0.5*radii[0]+0.5*radii[1]

#NNQ, NEQ, EEQ, SEQ, SSQ, SWQ, WWQ, NWQ

    elif(code[2] == 'Q'):
        
        if(code[0:2] == 'NN'):
            
            rne=0.5*radii[0] + 0.5*radii[1]
            rse=0.5*radii[1] + 0.5*radii[2]
            rsw=0.5*radii[2] + 0.5*radii[3]
            rnw=0.5*radii[0] + 0.5*radii[3]

        # ----------------- currrent (> 2005) standard
        
        elif(code[0:2] == 'NE'):
            
            rne=radii[0]
            rse=radii[1]
            rsw=radii[2]
            rnw=radii[3]

        elif(code[0:2] == 'EE'):

            rne=0.5*radii[3] + 0.5*radii[0]
            rse=0.5*radii[0] + 0.5*radii[1]
            rsw=0.5*radii[1] + 0.5*radii[2]
            rnw=0.5*radii[2] + 0.5*radii[3]
            
        elif(code[0:2] == 'SE'):
            rne=radii[3]
            rse=radii[0]
            rsw=radii[1]
            rnw=radii[2]
            
        elif(code[0:2] == 'SS'):

            rne=0.5*radii[2] + 0.5*radii[3]
            rse=0.5*radii[3] + 0.5*radii[0]
            rsw=0.5*radii[0] + 0.5*radii[1]
            rnw=0.5*radii[1] + 0.5*radii[2]

        elif(code[0:2] == 'SW'):
            
            rne=radii[2]
            rse=radii[3]
            rsw=radii[0]
            rnw=radii[1]

        elif(code[0:2] == 'WW'):

            rne=0.5*radii[1] + 0.5*radii[2]
            rse=0.5*radii[2] + 0.5*radii[3]
            rsw=0.5*radii[3] + 0.5*radii[0]
            rnw=0.5*radii[0] + 0.5*radii[1]

        elif(code[0:2] == 'NW'):
            
            rne=radii[1]
            rse=radii[2]
            rsw=radii[3]
            rnw=radii[0]

        else:

            print 'EEEEEE atcf: invalid Q wind radii code: ',code
            sys.exit()
            
    #
    # it's not physically possible for all to be zero, if so, then set to undefined
    #

    if(rne == 0.0 and rse == 0.0 and rse == 0.0 and rnw == 0.0):
        rne=rse=rsw=rnw=-999.

    rquad=[rne,rse,rsw,rnw]

    return(rquad)

if (__name__ == "__main__"):

    tD=TcData()
    tD.ls()
    tB=TcBasin('epac')
    tB.ls()
    sys.exit()

