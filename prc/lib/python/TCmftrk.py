from WxMAP2 import *
w2=W2()

from tcbase import Adeck
from vdVM import MakeVdeckSDtg

from tcbase import TcData,TcAdecksLocalDir,getHemis,Basin1toBasin2,Rlatlon2ClatlonFull,Clatlon2Rlatlon,isShemBasinStm,gc_dist,chklat,vmaxMS2KT,GetMdeckBts,BestTrk,Adeck

class MfTrkAreaNhem(W2areas):


    def __init__(self,
                 lonW=0.0,
                 lonE=360.0,
                 latS=0.0,
                 latN=80.0,
                 dx=0.5,
                 dy=0.5,
                 ):

        self.setLons(lonW,lonE)
        self.setLats(latS,latN)

        self.setGrid(dx,dy)


class MfTrkAreaShem(W2areas):


    def __init__(self,
                 lonW=0.0,
                 lonE=360.0,
                 latS=-60.0,
                 latN=0.0,
                 dx=0.5,
                 dy=0.5,
                 ):

        self.setLons(lonW,lonE)
        self.setLats(latS,latN)

        self.setGrid(dx,dy)


class MfTrkAreaGlobal(W2areas):


    def __init__(self,
                 lonW=0.0,
                 lonE=360.0,
                 latS=-60.0,
                 latN=60.0,
                 dx=0.5,
                 dy=0.5,
                 ):

        self.setLons(lonW,lonE)
        self.setLats(latS,latN)

        self.setGrid(dx,dy)




class mfTracker(f77GridOutput):


    remethod='ba'
    remethod='bl'
    remethod='' # use re default for change in res  'ba' for fine->coarse and 'bl' for coarse->fine

    rexopt='linear'
    reyopt='linear'

    def __init__(self,model,dtg,
                 area=None,
                 taus=None,
                 vars=None,
                 doregrid=1,
                 tdir=None,
                 tbdir=None,
                 mintauTC=120,
                 maxtauTC=168,
                 doLogger=0,
                 Quiet=1,
                 verb=0,
                 doByTau=1,
                 # -- 20130401 -- updated src with new settings for speed check, etc....
                 version=1.1,
                 adecksource='wxmap2',
                 dbname='invMftrkN',
                 doInvOnly=0,
                 diag=1,
                 trackerName='mmtrkN',
                 trackerAdmask="wxmap2*",
                 f77dir='/tmp',
                 ):

        import TCw2 as TC
        from M2 import setModel2


        tbdir=w2.TcDatDirMFtrk


        # -- inventory
        #
        self.dbname=dbname
        self.dbfile="%s.pypdb"%(dbname)
        self.dsbdir="%s/DSs"%(tbdir)
        MF.ChkDir(self.dsbdir,'mk')

        if(diag): MF.sTimer('setDSs')
        self.DSs=DataSets(bdir=self.dsbdir,name=self.dbfile,dtype=self.dbname,verb=verb,doDSsWrite=1)
        self.dbkeyLocal='local'

        try:
            self.dsL=self.DSs.getDataSet(key=self.dbkeyLocal,verb=verb)
            self.invN=self.dsL.data
        except:
            self.dsL=DataSet(name=self.dbkeyLocal,dtype='hash')
            self.invN={}

        if(doInvOnly): return 
        if(diag): MF.dTimer('setDSs')

        # -- m2 object
        #
        self.m2=setModel2(model)

        # -- now check if tau complete
        #
        nfieldfact=-3
        nfieldmin=self.m2.nfields
        if(hasattr(self.m2,'nfieldsW2flds')): nfieldmin=self.m2.nfieldsW2flds
        nfieldmin=nfieldmin + nfieldfact

        if(not(mintauTC in self.taus)):
            print 'WWW insufficient taus...latest: ',self.taus[-1]
            self.enoughTaus=0
        else:
            self.enoughTaus=1

        if(self.enoughTaus and (nfields[mintauTC] < nfieldmin) ):
            print 'WWW enough taus, but incomplete...mintauTC: ',mintauTC,\
                  ' nfields: ',nfields[mintauTC],'nfieldmin:',nfieldmin,self.m2.nfieldsW2flds
            self.enoughTaus=0

        self.model=model
        self.dtg=dtg
        self.area=area
        self.taus=taus
        self.vars=vars
        self.doregrid=doregrid
        self.GAdoLogger=doLogger
        self.GAQuiet=Quiet
        self.dpaths={}
        self.sstdpath=None
        self.areaname=None
        self.verb=verb
        self.doByTau=doByTau
        self.version=version
        self.adecksource=adecksource
        self.prcdir="%s/tctrk"%(os.getenv("W2_PRC_DIR"))
        self.f77dir=f77dir

        # -- get m2 object with model details
        #
        self.m2=setModel2(model)
        
        # -- set grid before setting vars...
        #
        if(area == None): self.setGridMFtracker()

        # -- abspath tdir set here
        #
        self.setCtl(tbdir=tbdir)
        self.initVars()
        self.initNgtrkVars()

        self.setTCs()

        self.setNgtrkOutput(verb=verb)
        self.setNgtrp(verb=verb)

        filename="%s.%s"%(self.model,self.dtg)
        self.setOutput(filename=filename)
        self.setNgtrkNl()

    def setTCs(self,ropt='',override=0):

        self.tD=TcData(dtgopt=self.dtg,verb=self.verb)

        (self.istmids,self.btcs)=self.tD.getDtg(self.dtg)

        tcV=self.tD.getTCvDtg(self.dtg)
        self.tcVcards=tcV.makeTCvCards()
        self.istmids=tcV.stmids


    def setGridMFtracker(self,ropt='',override=0):

        if(len(self.istmids) == 0):
            print 'EEE no storms to run mftrkN in mfTracker.setGridMFtracker()...sayoonara'
            sys.exit()

        self.hemigrid=getHemis(self.istmids)
        if(self.hemigrid == 'nhem'):  aa=MfTrkAreaNhem()
        if(self.hemigrid == 'shem'):  aa=MfTrkAreaShem()
        if(self.hemigrid == 'global'):  aa=MfTrkAreaGlobal()

        self.area=aa
        
        # override to test with more general code
        #
        #self.area=W2areaGlobal()



    def initVars(self,undef=1e20):

        if(self.area == None): self.area=W2areaGlobal()

        pslvar='1.0'
        if(hasattr(self.m2,'modelpslvar')): pslvar=self.m2.modelpslvar

        pslfact=pslvar.replace('psl*','')

        #-- added 7th field for array name in f77Output.f module
        #
        ua850='ua(lev=850)'
        va850='va(lev=850)'
        ua850t='(ua(t-TM1,lev=850)*TFM1 + ua(t+TP1,lev=850)*TFP1)'
        va850t='(va(t-TM1,lev=850)*TFM1 + va(t+TP1,lev=850)*TFP1)'

        if(self.vars == None): self.vars=['uas:uas:(uas(t-TM1)*TFM1 + uas(t+TP1)*TFP1):0:-999:-999:uas [m/s]:ddfld',
                                          'vas:vas:(vas(t-TM1)*TFM1 + vas(t+TP1)*TFP1):0:-999:-999:vas [m/s]:fffld',
                                          # vrt850 is recalculated for time interp, but need unambiguous expression here for
                                          # testing in WxMAP2.f77Oputput.getValidTaus
                                          'vrt850:(hcurl(%s,%s)*1e5):(hcurl(%s,%s)*1e5):850:-999:-999:rel vort 850 [*1e5 /s]:vvfld'%(ua850,va850,ua850t,va850t),
                                          'psl:(psl*%s):((psl(t-TM1)*TFM1)*%s + (psl(t+TP1)*TFP1)*%s):0:-999:-999:psl [mb]:pslfld'%(pslfact,pslfact,pslfact),
                                          ]


        self.undef=undef

        if(self.taus == None):
            self.btau=0
            self.etau=144
            if(hasattr(self,'maxtauTC')): self.etau=self.maxtauTC
            self.dtau=6
            self.tunits='hr'
            self.taus=range(self.btau,self.etau+1,self.dtau)

        aa=self.area

        
        if(self.remethod == ''):
            self.reargs="%d,%s,%f,%f,%d,%s,%f,%f"%(aa.ni,self.rexopt,aa.lonW,aa.dx,aa.nj,self.reyopt,aa.latS,aa.dy)
        else:
            self.reargs="%d,%s,%f,%f,%d,%s,%f,%f,%s"%(aa.ni,self.rexopt,aa.lonW,aa.dx,aa.nj,self.reyopt,aa.latS,aa.dy,self.remethod)

        if(not(self.doregrid)): self.reargs=None
        


    def initNgtrkVars(self):

        self.oadir=self.tdir

        self.localadirs={}

        # -- trackers paths
        self.ngpath="%s/ngtrk.ngtrp.txt"%(self.tdir)
        self.ndpath="%s/ngtrk.diag.txt"%(self.tdir)
        self.nfpath="%s/ngtrk.mfdiag.txt"%(self.tdir)
        self.nopath="%s/ngtrk.out.txt"%(self.tdir)
        self.nlpath="%s/ngtrk.nl"%(self.tdir)

        # -- tracker app
        #
        self.tracker='%s/ngtrkN.x'%(self.prcdir)

        # -- atcf

        amodel=self.model
        #if(w2.IsModel2(model)): amodel=model[0:3]

        if(amodel == 'rtfimy'):
            adeckname='FIMY'
            adecknum=99

        elif(amodel == 'rtfim'):
            adeckname='FIM8'
            adecknum=99
        elif(amodel == 'rtfim7'):
            adeckname='FIM7'
            adecknum=99
        elif(amodel == 'rtfimx'):
            adeckname='FIMX'
            adecknum=99
        elif(amodel == 'rtfim9'):
            adeckname='FIM9'
            adecknum=99
        else:
            try:
                adeckname=ModelNametoAdeckName[amodel]
                adecknum=ModelNametoAdeckNum[amodel]
            except:
                adeckname=amodel.upper()
                adecknum=99
                print 'WWW atcf.ModelNametoAdeckName failed for amodel: ',amodel,'using upper(): ',adeckname

        self.amodel=amodel
        self.adeckname=adeckname
        self.adecknum=adecknum

        # -- .gsf for w2-plot.py (and g.wxmap*gs)
        #
        self.ngtrktcbtftgsfpath="%s/ngtrk.tcbtft.%s.%s.gsf"%(self.tdir,self.amodel,self.dtg)
        self.ngtrktcbtofgsfpath="%s/ngtrk.tcbtof.%s.%s.gsf"%(self.tdir,self.amodel,self.dtg)



    def setNgtrkNl(self):

        nl="""&trkParamsNL
  vortcrit=7.5,
  vmaxweak=45.0,
  vortadjfact=0.60,
  doGdatCon=.true.,
  vortcritadjust=.true.,
! -- a bug in the speed brake?  for 01e.2012? 2012051512
!  doSpeedBrake=.false.,
! -- from 09w.2012 2012071712 test in src/tcnavygrk/unittest/09w.2012

  doSpeedBrake=.true.,
  doAccelBrake=.true.,

! -- mods based on 08w.2012 -- raise max speed and lower speed check for ET to 35 (wpac)

  forspdMax=35.0,
  accelMax=30.0,

  forspdLatET=35.0,
  forspdMaxET=45.0,

  forspdAdjfact=1.25,
  forspdMaxTau0=12,

!  rfindPsl=1.0,
!  rfindVrt850=1.0,
  rfindPsl=0.5,
  rfindVrt850=0.5,
  rfindGen=0.5,

! set the scale and min slp deficit for turning off the tracker
!
  sdistpsl=120,
  rminPsldef=-0.5,

  rlatmax=60.0,
  rmaxConSep=180.0,
  undef=1e20,

! time period to set the motion to the input/obs for making the first guess
!
  ktauMaxInitialMotion=12,

! smooth the motion from previous smthMotionTauPeriod motions
!
  dosmthMotion=.true.,
!  dosmthMotion=.false.,
  smthMotionTauPeriod=18.0,

/

&verbOse
!  verbConGdat=.true.,
!  verbMfTrackem=.true.,
!  verbGrhiloPsl=.true.,	
!  verbGrhiloVrt850=.true.,
!  verbMftrack=.true.
!  verbTrackem=.true.
/
        """

        MF.WriteString2File(nl,self.nlpath)


    def setNgtrp(self,verb=2):

        self.ngtrp=self.tD.Carq2Ngtrp(self.dtg)
        MF.WriteList2File(self.ngtrp,self.ngpath,verb=verb)

    def setNgtrkOutput(self,verb=0):

        self.adeckatcfpaths={}
        self.adeckatcfpathLocals={}

        for stmid in self.istmids:
            if(verb): print 'setNgtrkOutput.stmid: ',stmid
            year=self.dtg[0:4]
            self.localadirs[stmid]="%s/%s/%s"%(TcAdecksLocalDir,year,self.dtg)
            mf.ChkDir(self.localadirs[stmid],'mk')

            versionId="v%03.0f"%(self.version*10.0)
            adeckatcfpath="%s/%s.%s.%s.%s.%s"%(self.oadir,self.adecksource,versionId,self.amodel,self.dtg,stmid)
            adeckatcfpathLocal="%s/%s.%s.%s.%s.%s"%(self.localadirs[stmid],self.adecksource,versionId,self.amodel,self.dtg,stmid)
            #
            # --- create symbolic link between local ngp2 and ngp wxmap adeck ... nhc feed missing tau0
            #
            if(self.amodel == 'ngp2'):
                adeckatcfpathalias="%s/wxmap.%s.%s.%s"%(self.oadir,self.amodel[0:3],self.dtg,stmid)
                adeckatcfpathalias=''
            else:
                adeckatcfpathalias=''

            if(adeckatcfpathalias != ''):
                cmd="ln -s %s %s"%(adeckatcfpath,adeckatcfpathalias)
                mf.runcmd(cmd,'')

            if(verb):
                print 'setNgtrkOutput.AAAA:      adeckatcfpath: ',adeckatcfpath
                print 'setNgtrkOutput.AAAA: adeckatcfpathLocal: ',adeckatcfpathLocal

            self.adeckatcfpaths[stmid]=adeckatcfpath
            self.adeckatcfpathLocals[stmid]=adeckatcfpathLocal



    def runTracker(self,ropt='',override=0):

        copt=''
        if(not(MF.ChkPath(self.nopath)) or not(self.chkAdecks(dolocal=0)) or override):
            cmd1="%s %s %s %s %s %s %s %s"%(self.tracker,self.nlpath,self.ngpath,self.mpath,self.nopath,self.ndpath,self.nfpath,copt)
            print cmd1
            mf.runcmd(cmd1,ropt)



    def chkAdecks(self,dolocal=1):

        nstmsdone=0
        nstmsdoneL=0
        totstms=len(self.istmids)

        if(dolocal):
            for stmid in self.istmids:
                siz=MF.GetPathSiz(self.adeckatcfpathLocals[stmid])
                if(siz != None and siz > 0):
                    nstmsdoneL=nstmsdoneL+1

        for stmid in self.istmids:
            siz=MF.GetPathSiz(self.adeckatcfpaths[stmid])
            if(siz != None and siz > 0):
                nstmsdone=nstmsdone+1

        if(nstmsdone == totstms or (dolocal and nstmsdoneL == totstms) ):
            print 'IIIII----- adecks for model: ',self.model,' dtg: ',self.dtg,' nstmsdone: ',nstmsdone,' IIIIIIIIIIIIIIIIIIIIIIII'
            return(1)
        else:
            return(0)


    def lsAdecks(self,lsopt='s',ncprint=100):

        for stmid in self.istmids:

            siz=MF.GetPathSiz(self.adeckatcfpaths[stmid])
            if(siz != None):
                print
                print 'sss ',siz,self.adeckatcfpaths[stmid],lsopt
                if(lsopt == 'l'):
                    MF.listTxtPath(self.adeckatcfpaths[stmid],ncprint=ncprint)




    def invTrk(self,quiet=0,override=0,verb=1):


        def chkAtcf(siz,path):
            if(siz == None):
                ncards=-1
                taus=None
                return(ncards,taus)

            cards=open(path).readlines()
            ncards=len(cards)
            taus=[]
            for card in cards:
                tt=card.split(',')
                for n in range(0,len(tt)):
                    t1=tt[n].strip()
                    if(n == 5): taus.append(int(t1))

            taus=mf.uniq(taus)

            return(ncards,taus)


        #ssssssssssssssssssssssssssssssssssssssssssssssssss start
        # -- tcs
        #

        didinv=0

        try:
            stm3ids=self.invN[self.dtg,self.model,'stm3ids']
        except:
            stm3ids=None

        if(stm3ids == None or override):

            stm3ids={}
            tcs=self.tcVcards.split('\n')
            for tc in tcs:
                if(len(tc) > 0):
                    tt=tc.split()
                    stm3id=tt[1]
                    stmname=tt[2]
                    stmlat=tt[5]
                    stmlon=tt[6]
                    stmvmax=vmaxMS2KT(tt[12])

                    stm3ids[stm3id]=(stmlat,stmlon,stmvmax,stmname)
            self.invN[self.dtg,self.model,'stm3ids']=stm3ids
            didinv=1

        if(len(stm3ids) > 0 and verb):
            kk=stm3ids.keys()
            kk.sort()
            for k in kk:
                print k,stm3ids[k]


        # -- get data tau inventory
        #

        try:
            otaus=self.invN[self.dtg,self.model,'taus']
        except:
            otaus=None


        if(otaus == None or override):

            cmd="/w21/prc/flddat/t.nwp.w2flds.py %s %s -l -F"%(self.dtg,self.model)
            fldtauInv=MF.runcmdLog(cmd)
            nada=0
            for card in fldtauInv:
                if(mf.find(card,'LLL')):
                    tt=card.split()
                    if(mf.find(tt[0],'NNN')):
                        taus=[-999]
                        break
                    else:
                        for n in range(0,len(tt)):
                            if(mf.find(tt[n],'Ntaus:')):
                                nt=n
                                break

                    if(not(nada)):
                        ntaus=tt[nt+1]
                        taus=tt[nt+3:]

            otaus=[]
            for tau in taus:
                otaus.append(int(tau))

            self.invN[self.dtg,self.model,'taus']=otaus
            didinv=1

        if(verb):
            print 'TTT model: ',self.model,' data taus: ',otaus


        # -- adecks
        #

        try:
            adeckStatus=self.invN[self.dtg,self.model,'adeck']
        except:
            adeckStatus=None

        if(adeckStatus == None or override):

            adeckStatus={}

            nstmsdone=0
            for stm3id in stm3ids:
                print 'CCC checking: ',stm3id
                for stmid in self.istmids:
                    if(mf.find(stmid,stm3id)):
                        taid=self.adeckname.lower()
                        tstmid=stmid
                        apath=self.adeckatcfpaths[stmid]

                        # ---------------------- make vdeck from adeck for checking...
                        #
                        makeVdeck4Apath=0
                        if(makeVdeck4Apath):
                            aD=Adeck(apath,verb=verb)
                            aD.taid=taid
                            aD.tstmid=tstmid
                            AT=aD.GetAidTrks(aid=taid,stm1id=tstmid)

                            # -- new md2 -- problem is need to mod tc2.MDdataset
                            #dss=self.tD.getDSsFullStm(stmid)
                            #btrk=dss.trk
                            #bdtgs=btrk.keys()
                            #bdtgs.sort()
                            #for bdtg in bdtgs:
                            #    btrk[bdtg].ls()

                            (btdtgs,btcs)=GetMdeckBts(stmid,dofilt9x=0,verb=0)
                            BT=BestTrk2(btdtgs,btcs)
                            BT.stmid=stmid
                            vd=MakeVdeckSDtg(BT,AT,self.dtg,verb=verb,qcSpeed=1)
                            vd.ls()
                            return

                        siz=MF.GetPathSiz(apath)
                        if(siz != None and siz > 0):
                            (ncards,taus)=chkAtcf(siz,apath)
                            (dtimei,ldtg,gdtgS)=MF.PathModifyTime(apath)
                            adeckStatus[stm3id]=(stmid,ncards,taus,siz,dtimei)
                            nstmsdone=nstmsdone+1


            self.invN[self.dtg,self.model,'adeck']=adeckStatus
            didinv=1


        if(verb):
            stm3ids=adeckStatus.keys()
            stm3ids.sort()

            for stm3id in stm3ids:
                print 'AAAAAAAAAA ',stm3id,adeckStatus[stm3id]


        if(hasattr(self,'dsL') and didinv):
            self.dsL.data=self.invN
            self.DSs.putDataSet(self.dsL,key=self.dbkeyLocal,verb=1)


        return


    def chkInv(self,verb=0):

        try:
            self.invN[self.dtg,self.model,'sumGen']
        except:
            self.invTrk(quiet=1)   

        gen=self.invN[self.dtg,self.model,'sumGen']
        trk=self.invN[self.dtg,self.model,'sumStm']
        tt=gen.split()
        (ngood,nall)=tt[2].split('/')
        pdonegen=0
        if(int(nall) > 0):
            pdonegen=float(ngood)/float(nall)
        if(verb): print 'TTTT: ',self.model,self.dtg,ngood,nall,pdonegen

        tt=trk.split()
        (ngood,nall)=tt[2].split('/')
        pdonetrk=0
        if(int(nall) > 0):
            pdonetrk=float(ngood)/float(nall)
        if(verb): print 'GGGG: ',self.model,self.dtg,ngood,nall,pdonetrk

        rc=1
        if(pdonegen == 1.0 and pdonetrk == 1.0): rc=0
        return(rc)








    def ngtrk2Adeck(self,
                    verb=0,
                    biascorrvmax=0,
                    docpLocal=1):


        ntcfs={}

        otdir=self.tdir

        ngtrktrackpath=self.nopath
        ngtrkdiagmfpath=self.nfpath
        ngtrkngtrppath=self.ngpath

        #----------------------------------------------------------------------
        # read in ngtrk ngtrp and diag 
        #----------------------------------------------------------------------

        (stmdatang,stmidsng,stmvmaxmf,stmidsmf)=self.ParseNgtrkNgtrpDiagCards(ngtrkngtrppath,ngtrkdiagmfpath)

        #----------------------------------------------------------------------
        # read in ngtrk track
        #----------------------------------------------------------------------

        (stmids,stmdata,stmtaus)=self.ParseNgtrkTrackCards(ngtrktrackpath)

        pmin=0
        r34ne=0
        r34se=0
        r34sw=0
        r34nw=0

        for stmid in stmids:

            if(len(stmid) <= 3): 
                stmidFull=None
                continue
            for istmid in self.istmids:

                if(verb): print 'iiiiiiiiiiiiiiiiiiii ',istmid,stmid,istmid[2],stmid.upper()[2],int(istmid[0:2]),int(stmid[0:2])
                if(stmid.upper() == istmid.split('.')[0].upper()):
                    stmidFull=istmid
                    if(verb): print '0000000000000000000 ',stmid.upper(),istmid.split('.')[0].upper(),stmidFull
                    break

                # -- problem with ??I in md2 v ??A|??B in mdeck
                elif(istmid[2] == 'I' and (stmid.upper()[2] == 'A' or stmid.upper()[2] == 'B') and (int(istmid[0:2]) == int(stmid[0:2])) ):
                    stmidFull=istmid
                    if(verb): print '1111111111111111111 ',istmid[2].stmid.upper()[2],int(istmid[0:2]),int(stmid[0:2])
                    break

                # -- shem storms ?? why'd i though i needed??
                elif(istmid[2] == 'S' and (stmid.upper()[2] == 'P' or stmid.upper()[2] == 'S') and (int(istmid[0:2]) == int(stmid[0:2])) ):
                    stmidFull=istmid
                    if(verb): print '2222222222222222222 ',istmid[2].stmid.upper()[2],int(istmid[0:2]),int(stmid[0:2])
                    break

                else:
                    stmidFull=istmid


            # -- open adeck file
            #

            if(stmidFull == None): 
                continue
            
            print 'AAAA adeckatcfpath: ',self.adeckatcfpaths[stmidFull]

            aatcf=open(self.adeckatcfpaths[stmidFull],'w')

            stmnum=stmid[0:2]
            basin1=stmid[2:]
            basin2=Basin1toBasin2[basin1]

            if(verb): print 'SSS ',stmid,basin1,basin2,self.adeckname,self.adecknum

            # -- for no forecasts
            #
            try:
                vmaxbias=int(stmdatang[stmid,'tcvmax']) - int(stmvmaxmf[stmid,0,'vmax'])
            except:
                continue

            vmax0=stmvmaxmf[stmid,0,'vmax']

            ntcfcst=0


            if(len(stmtaus[stmid]) == 0):
                ntcfs[stmid]=0
                continue

            print

            for itau in stmtaus[stmid]:

                try:
                    (rlatfc,rlonfc,rdirfc,rspdfc,rcnf)=stmdata[stmid,itau,'fcst']
                    (clat,clon,ilat,ilon,hemns,hemew)=Rlatlon2ClatlonFull(rlatfc,rlonfc)
                    vmax=stmvmaxmf[stmid,itau,'vmax']
                    dvmax=stmvmaxmf[stmid,itau,'dvmax']
                    ntcfcst=ntcfcst+1

                except:
                    continue

                try:
                    pmin=stmvmaxmf[stmid,itau,'pmin']
                    if(pmin > 1050.0): pmin=0.
                except:
                    continue


                if(biascorrvmax):
                    #
                    # bias correct vmax forecast
                    #

                    vmaxadd=vmax
                    if(dvmax != -999):
                        vmaxadd=vmax0 + vmax0*dvmax

                        vmaxcorr=vmaxadd+vmaxbias

                    #
                    # round to nearest 5 kt
                    #

                    vmaxcorr=int(float(vmaxcorr)/5.0 + 0.5)*5

                else:
                    vmaxadd=0.0
                    vmaxcorr=vmax

                if(verb):
                    print "VVV %6.1f %7.3f %6.1f %3d"%(vmax0,dvmax,vmaxadd,vmaxcorr)
                    print 'FFF %03d  %6.1f  %7.1f :: %6.1f %6.1f'%(itau,rlatfc,rlonfc,rdirfc,rspdfc)
                    print "FFF %03d %03d%1s %04d%1s"%(itau,ilat,hemns,ilon,hemew)

                acard0="%2s, %2s, %10s, %2s, %4s, %3d,"%(basin2,stmnum,self.dtg,self.adecknum,self.adeckname,itau)
                # 20030428 -- make more atcf friendly
                adum=0 
                acard1=" %3d%1s, %4d%1s, %3d, %4.0f,   ,  34, NEQ, %4d, %4d, %4d, %4d, %4d, %4d, %3d, %3d, %3d,"%\
                    (ilat,hemns,ilon,hemew,vmaxcorr,pmin,r34ne,r34se,r34sw,r34nw,adum,adum,adum,adum,adum)

                acard=acard0+acard1
                print 'AAA %s'%(acard)
                acard=acard+'\n'

                aatcf.writelines(acard)

            aatcf.close()

            if(docpLocal):
                cmd="cp %s %s"%(self.adeckatcfpaths[stmidFull],self.adeckatcfpathLocals[stmidFull])
                mf.runcmd(cmd)

            ntcfs[stmid]=ntcfcst

        #
        # add lower case stmid to ntcfs
        #

        for stmid in stmids:
            stmlow=stmid

            # -- for no forecasts
            #
            try:
                ntcfs[stmlow]=ntcfs[stmid]
                print 'NNNNNNNNNNNNNN ntcfs: ',stmlow,' ',ntcfs[stmid]
            except:
                None


        self.stmids=stmids
        self.stmdata=stmdata
        self.stmidsng=stmidsng
        self.stmdatang=stmdatang

        return(ntcfs,stmids,stmdata,stmidsng,stmdatang)



    def ParseHeadMFdiag(self,n,cards,verb=0):

        tt=cards[n].split()
        type=tt[0]
        rtau=float(tt[2])
        stm=tt[4]
        rlon0=float(tt[5])
        rlat0=float(tt[6])
        if(verb): print 'mm1 ',cards[n],len(cards),type,rtau,stm,rlat0,rlon0

        n=n+1
        tt=cards[n].split()

        npts=int(tt[0])+int(tt[1])

        if(verb): print 'mm2 ',npts

        return(n,stm,rtau,rlat0,rlon0,type,npts)


    def ParseExtremaMFdiag(self,n,cards,rlat0,rlon0,npts,getmax=1,verb=0):

        # mf 20090401 -- changed format of the mf diag output from ngtrk.x
        #

        disttau=-999.0

        if(getmax):
            maxtau=-999.0
        else:
            maxtau=1e20

        for nn in range(0,npts):
            n=n+1
            try:
                tt=cards[n].split()
                doparse=1
            except:
                doparse=0

            if(doparse):
                dist=float(tt[1])
                rlon=float(tt[2])
                rlat=float(tt[3])
                rmax=float(tt[4])

                if(getmax and rmax>maxtau):
                    maxtau=rmax
                    disttau=dist
                if(not(getmax) and rmax<maxtau):
                    maxtau=rmax
                    disttau=dist

            if(verb):
                print cards[n][:-1]
                print "%s :: %6.2f %6.2f %6.2f %6.2f"%('mm3 ',rlat,rlon,rmax,dist)

        n=n+1

        return(n,maxtau,disttau)


    def ParseNgtrkTrackCards(self,ngtrkpath,verb=0):

        stmids=[]
        stmdata={}
        stmtaus={}

        o=open(ngtrkpath)
        cards=o.readlines()
        o.close()

        ncards=len(cards)

        if(ncards <= 1):
            print 'WWWW----- mfTracker.ParseNgtrkTrackCards() ncards <= 1 no trackers; bail...'
            return(stmids,stmdata,stmtaus)

        n=0
        tt=cards[n].split()
        nstm=int(tt[0])

        n=n+1

        for i in range(0,nstm):
            tt=cards[n].split()
            stmid=tt[0]
            stmtaus[stmid]=[]
            stmids.append(stmid)
            n=n+1

        # next card is blank, skip 2 because we started at 1 vice 0

        n=n+2

        while(n < ncards):

            tt=cards[n].split()
            tau=tt[0]

            if(tau == '***'):
                stm=tt[1]
                rlatcarq=float(tt[2])
                rloncarq=float(tt[3])
                itau=0

                stmdata[stm,itau,'carq']=(rlatcarq,rloncarq)

            elif(tau.find('FIN') >= 0 or tau.find('LOS') >= 0):
                print 'done/lost'

            else:
                stm=tt[1]
                rlat=tt[2]
                rlon=tt[3]
                rdir=tt[4]
                rspd=tt[5]
                rcnf="%s %s %s"%(tt[6],tt[7],tt[8])
                itau=int(tau)
                rlatfc=float(rlat)
                rlonfc=float(rlon)

                if(verb): print 'nnn ',itau,stm,rlat,rlon,rdir,rspd,rcnf
                if(rlatfc > 90.0):
                    n=n+1
                    continue            

                try:
                    rdirfc=float(rdir)
                except:
                    rdirfc=-999.

                try:
                    rspdfc=float(rspd)
                except:
                    rspdfc=-999.

                stmdata[stm,itau,'fcst']=(rlatfc,rlonfc,rdirfc,rspdfc,rcnf)


                try:
                    stmtaus[stm].append(itau)
                except:
                    stmtaus[stm]=[]
                    stmtaus[stm].append(itau)

            n=n+1

        return(stmids,stmdata,stmtaus)



    def ParseNgtrkNgtrpDiagCards(self,ngtrkngtrppath,ngtrkdiagmfpath,verb=0):


        #----------------------------------------------------------------------
        # parse the ngtrp file
        #----------------------------------------------------------------------

        stmdatang={}
        stmidsng=[]
        stmvmaxmf={}
        stmidsmf=[]

        o=open(ngtrkngtrppath)
        cards=o.readlines()
        o.close()

        ncards=len(cards)

        n=1
        while(n < ncards):

            tt=cards[n].split()

            (tcrlat,tcrlon)=Clatlon2Rlatlon(tt[0],tt[1])

            stmid=tt[3]+tt[4]
            tcvmax=int(tt[2])
            tcdir=float(tt[7])*0.1
            tcspd=float(tt[8])*0.1
            tcr34=float(tt[5])
            tcr50=float(tt[6])

            stmidsng.append(stmid)

            stmdatang[stmid,'tcvmax']=tcvmax
            stmdatang[stmid,'tcdir']=tcdir
            stmdatang[stmid,'tcspd']=tcspd
            stmdatang[stmid,'tcr34']=tcr34
            stmdatang[stmid,'tcr50']=tcr50
            stmdatang[stmid,'tcrlat']=tcrlat
            stmdatang[stmid,'tcrlon']=tcrlon

            n=n+1

        #----------------------------------------------------------------------
        # parse the mf diag file from ngtrk.x
        #----------------------------------------------------------------------

        try:
            o=open(ngtrkdiagmfpath)
            cards=o.readlines()
            o.close()
        except:
            print 'WWW(ParseNgtrkNgtrpDiagCards), no ngtrkdiagmfpath: ',ngtrkdiagmfpath,' bail...'
            rc=(stmdatang,stmidsng,stmvmaxmf,stmidsmf)
            return(rc)


        ncards=len(cards)
        if(verb): print 'NNN ncards ',ncards,ngtrkdiagmfpath

        n=0
        while(n < ncards):

            (n,stm,rtau,rlat0,rlon0,type,npts)=self.ParseHeadMFdiag(n,cards,verb=0)
            stmidsmf.append(stm)
            if(verb): print 'EXTRMA n: ',n,maxtau,disttau,type,stm,rlat0,rlon0

            if(type == 'PSL'):
                (n,maxtau,disttau)=self.ParseExtremaMFdiag(n,cards,rlat0,rlon0,npts,getmax=0,verb=0)
                tau=int(rtau)
                stmvmaxmf[stm,tau,'pmin']=maxtau
                stmvmaxmf[stm,tau,'pmindist']=disttau

            elif(type == 'SPD'):
                (n,maxtau,disttau)=self.ParseExtremaMFdiag(n,cards,rlat0,rlon0,npts,getmax=1)
                tau=int(rtau)
                stmvmaxmf[stm,tau,'vmax']=maxtau
                stmvmaxmf[stm,tau,'dist']=disttau

            else:
                (n,maxtau,disttau)=self.ParseExtremaMFdiag(n,cards,rlat0,rlon0,npts,getmax=1)




        if(len(stmidsmf) == 0):
            rc=(stmdatang,stmidsng,stmvmaxmf,stmidsmf)

        stmidsmf=mf.uniq(stmidsmf)

        dtau=self.dtau
        etau=self.etau
        btau=self.btau

        for stm in stmidsmf:

            for tau in range(btau,etau+1,dtau):

                try:
                    vmax=stmvmaxmf[stm,tau,'vmax']
                    dist=stmvmaxmf[stm,tau,'dist']
                    if(tau >= dtau):
                        taumdtau=tau-dtau
                        dvmax=stmvmaxmf[stm,tau,'vmax']-stmvmaxmf[stm,0,'vmax']
                        dvmax=dvmax/stmvmaxmf[stm,0,'vmax']
                    elif(tau == 0):
                        dvmax=0.0
                    stmvmaxmf[stm,tau,'dvmax']=dvmax

                    if(verb): print 'TTTT %s :: %03d  %6.1f  %7.1f  %7.3f'%(stm,tau,vmax,dist,dvmax)

                except:

                    stmvmaxmf[stm,tau,'vmax']=-999
                    stmvmaxmf[stm,tau,'dist']=-999
                    stmvmaxmf[stm,tau,'dvmax']=-999
                    if(verb): print 'TTTT(except) %s :: %03d  %6.1f  %7.1f  %7.3f'%(stm,tau,vmax,dist,dvmax)

                    test=1

        rc=(stmdatang,stmidsng,stmvmaxmf,stmidsmf)
        return(rc)


    def SetBestNgtrkTrack(self,dtg,model,
                          stmids1,stmdata1,stmtaus1,stmdatang1,stmidsng1,stmvmaxmf1,stmidsmf1,
                          stmids2,stmdata2,stmtaus2,stmdatang2,stmidsng2,stmvmaxmf2,stmidsmf2,
                          ipemax=200.0,ipeclose=60.0,tdratiomin=70.0,sqrlmax=40.0,fnldistratiomax=30.0,
                          ):

        """ made redundant by ngtrkN.x which is more fault tolerant and stable by using the mass field (psl) as part of a three fix consensus 

        """

        def bestrule(model):
            #
            # 0 -- use algorithm
            # 1 -- always select sfc wind
            # 2 -- always select 850 vort

            rule=0
            if(model == 'fim8'):
                rule=2
                rule=0
            return(rule)


        def xequator(stmdata,stmid,taus):

            isshem=isShemBasinStm(stmid)
            isxeq=0
            for tau in taus:
                flat=stmdata[stmid,tau,'fcst'][0]
                if(flat > -88.0 and flat < 88.0):
                    if(isshem and flat > 0.0): isxeq=1
                    if(not(isshem) and flat < 0.0): isxeq=1

            return(isxeq)



        stmids=[]
        stmdata={}
        stmtaus={}

        stmdatang={}
        stmidsng=[]
        stmvmaxmf={}
        stmidsmf=[]

        for stmid in stmids1:

            tcvmax=stmdatang1[stmid,'tcvmax']
            tcdir=stmdatang1[stmid,'tcdir']
            tcspd=stmdatang1[stmid,'tcspd']

            try:
                taus1=stmtaus1[stmid]
            except:
                taus1=[]

            try:
                taus2=stmtaus2[stmid]
            except:
                taus2=[]


            nt1=len(taus1)
            nt2=len(taus2)

            print
            print 'BBBB',dtg,' Best trker: ',stmid,' tcdir/tcspd: ',tcdir,tcspd

            ntest=0

            if( nt1 > 0 and nt2 == 0 ):
                best=1
                if(xequator(stmdata1,stmid,taus1)): best=0

            elif(nt1 == 0 and nt2 > 0):
                best=2
                if(xequator(stmdata2,stmid,taus2)): best=0

            elif( nt1 > 0 and nt2 > 0 ):

                if(nt2 > nt1):
                    ataus=taus2
                else:
                    ataus=taus1

                totdist1=0.0
                totdist2=0.0

                for k in range(0,len(ataus)):

                    tau=ataus[k]
                    taup=ataus[k-1]

                    if(tau == 0):

                        clat1=stmdata1[stmid,tau,'carq'][0]
                        clon1=stmdata1[stmid,tau,'carq'][1]

                        try:
                            flat10=stmdata1[stmid,tau,'fcst'][0]
                            flon10=stmdata1[stmid,tau,'fcst'][1]
                            ipe1=gc_dist(clat1,clon1,flat10,flon10)
                        except:
                            flon10=999.
                            flat10=99.
                            ipe1=999.

                        try:
                            flat20=stmdata2[stmid,tau,'fcst'][0]
                            flon20=stmdata2[stmid,tau,'fcst'][1]
                            ipe2=gc_dist(clat1,clon1,flat20,flon20)
                        except:
                            flat20=99.
                            flon20=999.
                            ipe2=999.

                        fdist12=gc_dist(flat10,flon10,flat20,flon20)
                        print 'BBBB',dtg,' ipe CARQ: ',clat1,clon1,' 1: %5.1f %6.1f ipe: %4.1f '%(flat10,flon10,ipe1),\
                              ' 2: %5.1f %6.1f ipe: %4.1f '%(flat20,flon20,ipe2),' fdist12: %4.1f'%(fdist12)


                    try:
                        flat1f=stmdata1[stmid,tau,'fcst'][0]
                        flon1f=stmdata1[stmid,tau,'fcst'][1]

                        if(k > 0):
                            flat1fp=stmdata1[stmid,taup,'fcst'][0]
                            flon1fp=stmdata1[stmid,taup,'fcst'][1]
                            totdist1=totdist1+gc_dist(flat1f,flon1f,flat1fp,flon1fp)

                        spd1f=stmdata1[stmid,tau,'fcst'][3]

                    except:
                        flat1f=-99.
                        flon1f=-999.
                        spd1f=-99.

                    try:
                        flat2f=stmdata2[stmid,tau,'fcst'][0]
                        flon2f=stmdata2[stmid,tau,'fcst'][1]

                        if(k > 0):
                            flat2fp=stmdata2[stmid,taup,'fcst'][0]
                            flon2fp=stmdata2[stmid,taup,'fcst'][1]
                            totdist2=totdist2+gc_dist(flat2f,flon2f,flat2fp,flon2fp)
                        spd2f=stmdata2[stmid,tau,'fcst'][3]

                    except:
                        flat2f=-99.
                        flon2f=-999.
                        spd2f=-99.



                    fdist12=-999.
                    if(chklat(flat1f) and chklat(flat2f)):
                        fdist12=gc_dist(flat1f,flon1f,flat2f,flon2f)
                    print 'ffff: %03d'%(tau),' 1: %5.1f %6.1f %4.1f '%(flat1f,flon1f,spd1f),' 2: %5.1f %6.1f %4.1f '%(flat2f,flon2f,spd2f),\
                          ' fdist12: %5.1f'%(fdist12)

                #
                # find distance from initial postion to final positions
                #

                flat1fnl=stmdata1[stmid,taus1[-1],'fcst'][0]
                flon1fnl=stmdata1[stmid,taus1[-1],'fcst'][1]
                i2fdist1=gc_dist(flat10,flon10,flat1fnl,flon1fnl)

                #
                # persistence forecast
                #
                (flat1pers,flon1pers)=rumltlg(tcdir,tcspd,taus1[-1],flat10,flon10)

                flat2fnl=stmdata2[stmid,taus2[-1],'fcst'][0]
                flon2fnl=stmdata2[stmid,taus2[-1],'fcst'][1]
                i2fdist2=gc_dist(flat20,flon20,flat2fnl,flon2fnl)
                (flat2pers,flon2pers)=rumltlg(tcdir,tcspd,taus2[-1],flat20,flon20)

                if(flat2pers == None or flat1pers == None):
                    #
                    # case where TC goes over the poles...
                    #
                    f2f2perdist=None
                    f12f2dist=None
                    f1f2perdist=None
                else:

                    #
                    # distance from final 1 and 2 points
                    #
                    f2f2perdist=gc_dist(flat2fnl,flon2fnl,flat2pers,flon2pers)
                    f12f2dist=gc_dist(flat1fnl,flon1fnl,flat2fnl,flon2fnl)

                    #
                    # distance between final and persistence points
                    #
                    f1f2perdist=gc_dist(flat1fnl,flon1fnl,flat1pers,flon1pers)

                #
                # normalize all distacnce to per time step 12 h
                #
                #if(nt1 >= 2):
                #   totdist1=totdist1/(nt1-1)
                #   i2fdist1=i2fdist1/(nt1-1)
                #if(nt2 >= 2):
                #   totdist2=totdist2/(nt2-1)
                #   i2fdist2=i2fdist2/(nt2-1)

                #
                # squirely ratio =  distance from tau=0 to tau=final / total distance, if small the the storm did a lot of motion to go nowhere
                #
                sqrly1=sqrly2=-999.

                if(totdist1 > 0.0):
                    sqrly1=(i2fdist1/totdist1)*100.0

                if(totdist2 > 0.0):
                    sqrly2=(i2fdist2/totdist2)*100.0

                print 'BBBB',dtg,' select nt1/ipe1: %d %3.0f'%(nt1,ipe1),' nt2/ipe2: %d %3.0f'%(nt2,ipe2),' ipemax: ',ipemax,' ipeclose: ',ipeclose
                print 'BBBB',dtg,'    totdist1: %6.0f'%(totdist1),'  totdist2: %6.0f'%(totdist2)
                print 'BBBB',dtg,'    i2fdist1: %6.0f'%(i2fdist1),'  i2fdist2: %6.0f'%(i2fdist2)
                print 'BBBB',dtg,'    sqrly1/2: %3.0f  %3.0f'%(sqrly1,sqrly2)

                #print 'BBBB',dtg,' f1f2perdist: %6.0f'%(f1f2perdist),flat10,flon10,flat1pers,flon1pers
                #print 'BBBB',dtg,' f2f2perdist: %6.0f'%(f2f2perdist)

                #ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss
                #
                # selection rules:
                #
                # 1) take longest (tau) track if ipe <= ipemax
                #

                ipe1test=(ipe1 <= ipemax)
                ipe2test=(ipe2 <= ipemax)

                ipe1closetest=(ipe1 <= ipeclose)
                ipe2closetest=(ipe2 <= ipeclose)

                ipetest=0
                if(nt1 > nt2 and ipe1test):
                    best=1
                    ntest=1

                elif(nt2 > nt1 and ipe2test):
                    best=2
                    ntest=1

                #
                # if one track fails the ipemax test, just go with the one that passes
                #
                elif(ipe2test and not(ipe1test)):
                    best=2
                    ntest=22

                elif(not(ipe2test) and ipe1test):
                    best=1
                    ntest=11

                #
                # both failed...
                #
                elif(not(ipe2test) and not(ipe1test)):
                    best=0
                    ntest=99

                #ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss
                #
                # 2) if lengths =, go for lower ipe
                #
                elif(nt1 == nt2):

                    if(ipe1 <= ipe2):
                        best=1
                    else:
                        best=2

                    ipetest=1

                    #
                    # go with the sfc if both are less than ipeclose (60 nm)
                    #

                    if(best == 2 and ipe1 < ipeclose):
                        ipetest=3
                        best=1

                    ntest=2
                    print 'BBBB',dtg,' nt1=nt2 ipetest: %d  best: %d'%(ipetest,best)

                #ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss
                #
                # 3) check length of track...if one track much shorter/longer than the other
                #    then use longer, unless ipe is very good
                #

                disttest=0
                tdratio=-999.0
                if(totdist1 <= totdist2 and totdist2 > 0.0):
                    tdratio=(totdist1/totdist2)*100.0
                    if(tdratio < tdratiomin and not(ipe1closetest)):
                        best=2
                        disttest=2
                        ntest=3
                elif(totdist1 > 0.0):
                    tdratio=(totdist2/totdist1)*100.0
                    if(tdratio < tdratiomin and not(ipe2closetest) ):
                        best=1
                        disttest=1
                        ntest=3
                else:
                    distest=-1
                    best=1
                    ntest=3

                fnldisttest=0
                fnldstratio=-999.0


                #ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss
                #
                # 4) now check squirlyness -- tracks that are long but go near initial position -- go for the less squirly
                #

                sqrltest=0
                dsqrl=sqrly1-sqrly2

                print 'BBBB',dtg,'      dsqrl: %4.0f'%(dsqrl)

                if(abs(dsqrl) > sqrlmax):
                    if(dsqrl > 0.0):
                        sqrltest=2
                        best=1
                        ntest=4
                    elif(dsqrl < 0.0):
                        sqrltest=1
                        best=2
                        ntest=4

                    print 'BBBBSSSQQQRRRLLLYYY setting best by squirelyness: disttest: ',disttest,' dsqrl: %4.0f'%(dsqrl),' best: ',best

                print 'BBBB',dtg,'       ntest: ',ntest,' ipetest: ',ipetest,' best= ',best
                print 'BBBB',dtg,'    disttest: ',disttest," tdratio: %3.0f"%(tdratio),' best= ',best


                #ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss
                #
                # 5) check a big difference between the trackers, go with sfc
                #

                totdist12=totdist1+totdist2
                if(totdist12 > 0.0 and f12f2dist != None):
                    fnldistratio=(f12f2dist/totdist12*0.5)*100.0
                else:
                    fnldistratio=0.0
                    f12f2dist=-999.

                print 'BBBB',dtg,'   f12f2dist: %6.0f  fnldistratio: %3.0f fnldistratiomax: %3.0f'%(f12f2dist,fnldistratio,fnldistratiomax),\
                      ' disttest: ',disttest,' sqrltest: ',sqrltest
                if(totdist2 > 0.0 and totdist1 > 0.0 and disttest == 0 and sqrltest == 0 and fnldistratio > fnldistratiomax):
                    best=1
                    fnldisttest=0
                    ntest=5
                    print 'BBBBFFFNNNLLDDDRATIO   f12f2dist: %6.0f  fnldistratio: %3.0f  fnldisttest: %d'%(f12f2dist,fnldistratio,fnldisttest)

                #ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss
                #
                # 6) cross equator
                #

                if(best == 1 and xequator(stmdata1,stmid,taus1)):
                    best=2
                    ntest=6
                    print 'BBBBB',dtg,' XXXXXXXXXEEEEEEEEEEEEEQQQQQQQQQQQQQQQ track 1, set best=2'
                if(best == 2 and xequator(stmdata2,stmid,taus2)):
                    best=1
                    ntest=6
                    print 'BBBBB',dtg,' XXXXXXXXXEEEEEEEEEEEEEQQQQQQQQQQQQQQQ track 2, set best=1'


            else:

                #
                # no positions -- total failure of tracker
                #

                best=0
                ntest=0

            if(bestrule(model) > 0):
                best=bestrule(model)
                ntest="override by model: %s"%(model)

            print 'BBBB %s%s'%(dtg,'BBBBBBBBBBBBBBBBBBBB---> '),stmid,' best: ',best,' ntest: ',ntest

            if(best > 0):
                stmids.append(stmid)
                stmidsng.append(stmid)
                stmidsmf.append(stmid)

            if(best == 0):


                stmidsng.append(stmid)
                stmdatang[stmid,'tcvmax']=stmdatang1[stmid,'tcvmax']
                stmdatang[stmid,'tcdir']=stmdatang1[stmid,'tcdir']
                stmdatang[stmid,'tcspd']=stmdatang1[stmid,'tcspd']
                stmdatang[stmid,'tcr34']=stmdatang1[stmid,'tcr34']
                stmdatang[stmid,'tcr50']=stmdatang1[stmid,'tcr50']
                stmdatang[stmid,'tcrlat']=stmdatang1[stmid,'tcrlat']
                stmdatang[stmid,'tcrlon']=stmdatang1[stmid,'tcrlon']

            elif(best == 1):

                stmdata[stmid,0,'carq']=stmdata1[stmid,0,'carq']

                for tau in taus1:
                    stmdata[stmid,tau,'fcst']=stmdata1[stmid,tau,'fcst']
                    stmvmaxmf[stmid,tau,'vmax']=stmvmaxmf1[stmid,tau,'vmax']
                    stmvmaxmf[stmid,tau,'dist']=stmvmaxmf1[stmid,tau,'dist']
                    stmvmaxmf[stmid,tau,'dvmax']=stmvmaxmf1[stmid,tau,'dvmax']

                stmtaus[stmid]=taus1

                stmdatang[stmid,'tcvmax']=stmdatang1[stmid,'tcvmax']
                stmdatang[stmid,'tcdir']=stmdatang1[stmid,'tcdir']
                stmdatang[stmid,'tcspd']=stmdatang1[stmid,'tcspd']
                stmdatang[stmid,'tcr34']=stmdatang1[stmid,'tcr34']
                stmdatang[stmid,'tcr50']=stmdatang1[stmid,'tcr50']
                stmdatang[stmid,'tcrlat']=stmdatang1[stmid,'tcrlat']
                stmdatang[stmid,'tcrlon']=stmdatang1[stmid,'tcrlon']


            elif(best == 2):

                stmdata[stmid,0,'carq']=stmdata2[stmid,0,'carq']
                for tau in taus2:
                    stmdata[stmid,tau,'fcst']=stmdata2[stmid,tau,'fcst']
                    stmvmaxmf[stmid,tau,'vmax']=stmvmaxmf2[stmid,tau,'vmax']
                    stmvmaxmf[stmid,tau,'dist']=stmvmaxmf2[stmid,tau,'dist']
                    stmvmaxmf[stmid,tau,'dvmax']=stmvmaxmf2[stmid,tau,'dvmax']

                stmtaus[stmid]=taus2

                stmdatang[stmid,'tcvmax']=stmdatang2[stmid,'tcvmax']
                stmdatang[stmid,'tcdir']=stmdatang2[stmid,'tcdir']
                stmdatang[stmid,'tcspd']=stmdatang2[stmid,'tcspd']
                stmdatang[stmid,'tcr34']=stmdatang2[stmid,'tcr34']
                stmdatang[stmid,'tcr50']=stmdatang2[stmid,'tcr50']
                stmdatang[stmid,'tcrlat']=stmdatang2[stmid,'tcrlat']
                stmdatang[stmid,'tcrlon']=stmdatang2[stmid,'tcrlon']


        rc=(stmids,stmdata,stmtaus,stmdatang,stmidsng,stmvmaxmf,stmidsmf)

        return(rc)



    def TcStruct2BtFtGs(self,
                        override=0):



        dtg=self.dtg
        model=self.model
        stmids=self.istmids
        stmdata=self.stmdata
        stmidsng=self.stmidsng
        stmdatang=self.stmdatang
        ngtrktcbtftgsfpath=self.ngtrktcbtftgsfpath

        amodel=model
        #if(w2.IsModel2(model)): amodel=model[0:3]

        verb=0

        cards=[]

        cards.append('function tcbtft()\n')

        etau6=48
        btau12=60
        etauall=120

        taus6=range(0,etau6+1,6)
        taus=range(btau12,etauall+1,12)

        tausall=taus6+taus

        for tau in tausall:

            nt=1
            itau=int(tau)

            if( itau%12 == 6 and itau < 48 and itau > 0):

                itau0=int(tau-6)
                itau12=int(tau+6)

                for stmid in stmids:
                    try:
                        (rlat0,rlon0,rdir0,rspd0,rcnf0)=stmdata[stmid,itau0,'fcst']
                        (rlat1,rlon1,rdir1,rspd1,rcnf1)=stmdata[stmid,itau12,'fcst']
                        rlat=(rlat1+rlat0)*0.5
                        rlon=(rlon1+rlon0)*0.5

                        gsfcard="_tcft.%d.%d='%5.2f %6.2f %s'"%(itau,nt,rlat,rlon,rcnf0.split()[0])
                        cards.append(gsfcard)
                        nt=nt+1
                    except:
                        print 'no data for ',stmid,itau
                        continue

            else:

                for stmid in stmids:
                    try:
                        (rlat,rlon,rdir,rspd,rcnf)=stmdata[stmid,itau,'fcst']
                        gsfcard="_tcft.%d.%d='%5.2f %6.2f %s'"%(itau,nt,rlat,rlon,rcnf.split()[0])
                        cards.append(gsfcard)
                        nt=nt+1
                    except:
                        print 'no data for ',stmid,itau
                        continue


            if(nt == 1):
                gsfcard="_ntcft.%s=0"%(itau)
            else:
                nt=nt-1
                gsfcard="_ntcft.%s=%d"%(itau,nt)
            cards.append(gsfcard)
            cards.append(' ')



            if(nt == 1):
                gsfcard="_ntcft.%s=0"%(itau)
            else:
                nt=nt-1
                gsfcard="_ntcft.%s=%d"%(itau,nt)


        #
        # 20080507 -- case where only one storm and model completely failed to track -> no stmids which are calculated
        # from tracked storms... this causes the except: and added code to put a _tcbt.1 card so the drawtcbt.gsf doesn't fail
        #

        nbt=1
        for stmid in stmidsng:
            try:
                tcrlat=stmdatang[stmid,'tcrlat']
                tcrlon=stmdatang[stmid,'tcrlon']
                tcvmax=stmdatang[stmid,'tcvmax']
                gsfcard="_tcbt.%d='%5.2f %6.2f %d %s'"%(nbt,tcrlat,tcrlon,tcvmax,stmid)
                cards.append(gsfcard)
                nbt=nbt+1
            except:
                gsfcard="_tcbt.%d='%5.2f %6.2f %d %s'"%(nbt,-99.,-999.,-99,stmid)
                cards.append(gsfcard)
                gsfcard="_ntcbt=0"
                cards.append(gsfcard)
                continue

            #print 'no data for ',stmid,itau

        if(nbt == 1):
            gsfcard="_tcbt.%d='%5.2f %6.2f %d exception'"%(nbt,-99.,-999.,-99)
            cards.append(gsfcard)
            gsfcard="_ntcbt=0"
            cards.append(gsfcard)
        else:
            nbt=nbt-1
            gsfcard="_ntcbt=%d"%(nbt)
            cards.append(gsfcard)
            cards.append(' ')

        cards.append('return')

        print 'OOOOO - gfs tracker: ',model,' path: ',ngtrktcbtftgsfpath
        GS=open(ngtrktcbtftgsfpath,'w')
        for card in cards:
            GS.writelines(card+'\n')
            ###print card

        GS.close()

        return



    def TcStruct2BtOfGs(self,dtg,model,otdir,
                        ngtrktcbtofgsfpath,verb=0,ropt=''):


        amodel=model
        #if(w2.IsModel2(model)): amodel=model[0:3]

        dtautracker=atcf.DtauModelTracker[amodel]

        #
        #  cp from nhc/jtwc adeck dirs, wxmap.ofc? forms of ofcl/ofci tracks for overlay on model track
        #

        year=dtg[0:4]
        ofcljtwcdir="%s/%s/wxmap"%(w2.TcAdecksJtwcDir,year)
        cmd="cp %s/wxmap.ofc?.%s.??? %s/."%(ofcljtwcdir,dtg,otdir)
        mf.runcmd(cmd,ropt)

        ofclnhcdir="%s/%s/wxmap"%(w2.TcAdecksNhcDir,year)
        cmd="cp %s/wxmap.ofc?.%s.??? %s/."%(ofclnhcdir,dtg,otdir)
        mf.runcmd(cmd,ropt)

        #
        # go for both ofc and ofi
        #
        amask="%s/wxmap.ofc?.%s.???"%(otdir,dtg)
        adecks=glob.glob(amask)

        #
        # pick ofc over ofi
        #

        stms=[]
        for adeck in adecks:
            (dir,file)=os.path.split(adeck)
            (ofile,stm)=os.path.splitext(file)
            stms.append(stm[1:])

        #
        # if no ofc? forecasts...
        #
        if(len(stms) == 0):
            return

        ustms=mf.uniq(stms)

        uadecks=[]

        for stm in ustms:
            ofcadeck="%s/wxmap.ofcl.%s.%s"%(otdir,dtg,stm)
            ofiadeck="%s/wxmap.ofci.%s.%s"%(otdir,dtg,stm)
            ofcthere=os.path.exists(ofcadeck)
            ofithere=os.path.exists(ofiadeck)

            if(ofcthere and ofithere):
                uadecks.append(ofcadeck)

            elif(not(ofcthere) and ofithere):
                uadecks.append(ofiadeck)

            elif(ofcthere and not(ofithere)):
                uadecks.append(ofcadeck)


        adecks=copy.deepcopy(uadecks)

        if(verb):
            print 'aaaa ',amask
            print adecks

        gscards=[]

        if(len(adecks) == 0):
            ftcs=None
            ftcstruct=None
            return(ftcs,ftcstruct)

        else:

            oflatlons={}
            for adeck in adecks:
                try:
                    cards=open(adeck).readlines()
                except:
                    cards=None

                if(cards != None):
                    (ftcs,ftcs2,ftcstruct)=TCveri.ParseAdeckCards(dtg,cards,dtautracker)

                    stms=ftcs.keys()
                    for stm in stms:
                        ftc=ftcs[stm]

                        for i in range(0,len(ftc)):
                            tt=ftc[i]
                            if(i==0):
                                btlat=tt[0]
                                btlon=tt[1]
                                if(verb): print 'bttttttt ',btlat,btlon
                            else:
                                fttau=tt[0]
                                ftlat=tt[4]
                                ftlon=tt[5]
                                if(ftlat < 89.0):

                                    if(fttau == 48):
                                        lat48=ftlat
                                        lon48=ftlon
                                    elif(fttau == 72):
                                        lat72=ftlat
                                        lon72=ftlon
                                    elif(fttau == 96):
                                        lat96=ftlat
                                        lon96=ftlon
                                    elif(fttau == 120):
                                        lat120=ftlat
                                        lon120=ftlon

                                    if(verb): print 'fttttt ',fttau,ftlat,ftlon

                                    try:
                                        oflatlons[fttau].append([ftlat,ftlon])
                                    except:
                                        oflatlons[fttau]=[]
                                        oflatlons[fttau].append([ftlat,ftlon])

                                    #
                                    # interp for tau 60
                                    #
                                    if(fttau == 72):

                                        lat60=(ftlat+lat48)*0.5
                                        lon60=(ftlon+lon48)*0.5

                                        try:
                                            oflatlons[60].append([lat60,lon60])
                                        except:
                                            oflatlons[60]=[]
                                            oflatlons[60].append([lat60,lon60])



                                    #
                                    # interp for tau 84
                                    #
                                    if(fttau == 96):

                                        lat84=(ftlat+lat72)*0.5
                                        lon84=(ftlon+lon72)*0.5

                                        try:
                                            oflatlons[84].append([lat84,lon84])
                                        except:
                                            oflatlons[84]=[]
                                            oflatlons[84].append([lat84,lon84])


                                    #
                                    # interp for tau 108
                                    #
                                    if(fttau == 120):

                                        lat108=(ftlat+lat96)*0.5
                                        lon108=(ftlon+lon96)*0.5

                                        try:
                                            oflatlons[108].append([lat108,lon108])
                                        except:
                                            oflatlons[108]=[]
                                            oflatlons[108].append([lat108,lon108])




            taus=oflatlons.keys()
            taus.sort()

            card='function tcftof()'
            gscards.append(card)

            card=''
            gscards.append(card)

            for tau in taus:
                npts=len(oflatlons[tau])

                for i in range(0,npts):
                    lat=0
                    lon=0
                    (lat,lon)=oflatlons[tau][i]
                    card="_tcof.%d.%d='%5.1f %6.1f 1'"%(tau,i+1,lat,lon)
                    gscards.append(card)

                card="_ntcof.%d=%s"%(tau,npts)
                gscards.append(card)

                card=''
                gscards.append(card)


            card='return'
            gscards.append(card)


            if(verb):
                for gscard in gscards:
                    print gscard

            print 'OOOOO - ofcl tracker .gsf: ',amodel,' path: ',ngtrktcbtofgsfpath
            GS=open(ngtrktcbtofgsfpath,'w')
            for gscard in gscards:
                GS.writelines(gscard+'\n')

            GS.close()


        return