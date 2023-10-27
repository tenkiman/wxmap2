from tcbase import *

from M2 import setModel2
from FM import FimRunModel2Short,onWjet
from TCtrk import TmTrk,getBasinLatLons,tcgenBasins,TmTrkGen

from GRIB import Grib1,Grib2

class TmTrkN(TmTrk,TmTrkGen,Grib1):

    remethod='ba'
    remethod='bl'
    remethod='' # use re default for change in res  'ba' for fine->coarse and 'bl' for coarse->fine

    rexopt='linear'
    reyopt='linear'


    def __init__(self,
                 dtg,
                 model,
                 ctlpath=None,
                 taus=None,
                 maxtauModel=168,
                 nfields=None,
                 atcfname=None,
                 tdir=None,
                 tbdir=None,
                 tdirAdeck=None,
                 tcD=None,
                 # increase to 132 for tcgen vice 120
                 mintauTC=132,
                 maxtauTC=168,
                 verb=0,
                 domdeck=0,
                 trkmode='tracker',
                 domodelpyp=0,
                 dols=0,
                 dolstcs=1,
                 quiet=0,
                 doregrid=1,
                 regridTracker=0.5,
                 #regridGen=1.0,
                 regridGen=0.5,   # -- 20180912 higher res models
                 override=0,
                 dbname='invTmtrkN',
                 doInvOnly=0,
                 diag=1,
                 trackerName='tmtrkN',
                 trackerAdmask="tc*.txt",
                 doCleanonly=0,
                 doInventory=0,
                 xgrads='grads',
                 ):



        # -- m2 object
        #
        self.m2=setModel2(model)
        m2model=self.m2.model

        if(hasattr(self.m2,'regridTracker')): 
            regridTracker=self.m2.regridTracker
        
        
        grads1BinDir="%s/bin"%(os.getenv('W2_GRADS2_BDIR'))
        self.xwgrib="%s/wgrib"%(grads1BinDir)
        self.xgribmap="%s/gribmap"%(grads1BinDir)
        self.gribtype='grb1'
        
        tbdir=w2.TcDatDirTMtrkN

        if(dtg == None):
            self.tbdir=tbdir
            return
        if(atcfname != None): trackerAdmask="tc*%s*txt"%(atcfname.lower())
        
        self.trackerName=trackerName
        self.trackerAdmask=trackerAdmask
        self.enoughTaus=0
        self.datataus=0
        self.override=override

        # -- inventory
        #
        if(doInventory):

            if(diag): MF.sTimer('setDSs-TmTrkN-Inv')

            self.dbname=dbname
            self.dbfile="%s.pypdb"%(dbname)
            self.dsbdir="%s/DSs"%(tbdir)
            MF.ChkDir(self.dsbdir,'mk')

            self.DSs=DataSets(bdir=self.dsbdir,name=self.dbfile,dtype=self.dbname,verb=verb,dowriteback=0,doDSsWrite=1)
            self.dbkeyLocal='local'

            try:
                self.dsL=self.DSs.getDataSet(key=self.dbkeyLocal,verb=verb)
                self.invTmtrkN=self.dsL.data
            except:
                print 'MMMMMMMMMMMMM making new dataset'
                self.dsL=DataSet(name=self.dbkeyLocal,dtype='hash')
                self.invTmtrkN={}

            if(diag): MF.dTimer('setDSs-TmTrkN-Inv')

        if(doInvOnly): return 

        self.dtg=dtg
        self.model=model
        
        # -- make tcdata
        #
        tcD=TcData(dtgopt=dtg,verb=verb)
        self.tcD=tcD

        if(ctlpath == None or taus == None or nfields == None):
            (ctlpath,taus,nfields,tauOffset)=getCtlpathTaus(model,dtg)

        self.ctlpath=ctlpath
        self.taus=taus


        # -- check if enough taus are available
        #
        if(hasattr(self.m2,'dattaus')): 
            dattaus=self.m2.dattaus
        else:
            dattaus=w2.Model2DataTaus(m2model,dtg)

        if(len(dattaus) > 0):
            maxDataTauModel=dattaus[-1]
            self.datataus=1
        else:
            print 'WWW not taus for m2model: ',m2model,' dtg: ',dtg
            return

        mintauChk=min(mintauTC,maxDataTauModel)
        mintauTC=mintauChk

        # -- now check if tau complete
        #
        nfieldfact=-3
        nfieldmin=self.m2.nfields
        if(hasattr(self.m2,'nfieldsW2flds')): nfieldmin=self.m2.nfieldsW2flds
        nfieldmin=nfieldmin + nfieldfact
        
        if(self.taus != None and not(mintauTC in self.taus) ):
            if(len(self.taus) == 0): lastTau=None
            else: lastTau=self.taus[-1]
            print 'WWW insufficient taus...latest: ',lastTau
        else:
            self.enoughTaus=1

        nfieldChk=0
        if(nfields != None and mintauTC in nfields.keys() and nfields[mintauTC] >= nfieldmin): nfieldChk=1
        
        if(self.enoughTaus and nfieldChk == 0):
            
            nfieldsTau=None
            if(nfields != None):
                latestTau=nfields.keys()
                latestTau.sort()
                latestTau=latestTau[-1]
                nfieldsTau=nfields[latestTau]
                
            print 'WWW enough taus, but incomplete...mintauTC: ',mintauTC,'latestTau: ',latestTau,\
                  ' nfields[latestTau]: ',nfieldsTau,'nfieldmin:',nfieldmin,self.m2.nfieldsW2flds
            self.enoughTaus=0


        self.maxtauModel=maxtauModel
        self.tbdir=tbdir

        if(atcfname == None):   self.atcfname=model.upper()
        else:                   self.atcfname=atcfname

        if(tdir == None):       self.tdir="%s/%s/%s"%(tbdir,dtg,model)
        else:                   self.tdir=tdir

        if(tdirAdeck == None):  self.tdirAdeck=self.tdir
        else:                   self.tdirAdeck=tdirAdeck


        self.trkApp='gettrk_genN.x'
        self.xgrads=xgrads

        self.doga2=0

        self.mintauTC=mintauTC
        self.maxtauTC=maxtauTC

        self.verb=verb
        self.quiet=quiet
        self.dols=dols
        self.dolstcs=dolstcs

        self.prcdir="%s/tctrk"%(os.getenv("W2_PRC_DIR"))
        if(domodelpyp):
            self.pyppath="%s/Pstate.%s.pyp"%(self.tdir,model)
        else:
            self.pyppath="%s/Pstate.pyp"%(self.tdir)


        self.initCurState() # from MFbase

        # -- why? -- trying to run now...
        #if(not(onWjet) and ctlpath != None):
        if(ctlpath != None):
            MF.ChkDir(self.tdir,'mk')
            MF.ChkDir(self.tdirAdeck,'mk')

        self.trkmode=trkmode

        self.doregrid=doregrid
        self.regridGen=regridGen
        self.regridTracker=regridTracker

        # -- make tcD
        #
        tcV=self.tcD.getTCvDtg(self.dtg)
        #if(not(self.dols)):
        self.tcVcards=tcV.makeTCvCards(verb=verb,override=override)

        self.setTCs(override=override)
        self.setFldGrid(override=override)

        self.topath="%s/tmtrk"%(self.tdir)

        self.grbpath="%s.grb"%(self.topath)
        self.grbixpath="%s.grb.ix"%(self.topath)
        self.grbctlpath="%s.grb.ctl"%(self.topath)
        self.grbgmppath="%s.grb.gmp"%(self.topath)
        self.fdbpath="%s.wgrib1.txt"%(self.grbpath)
        
        self.grb10path="%s.1p0deg.grb"%(self.topath)
        self.grbix10path="%s.grb.1p0deg.ix"%(self.topath)
        self.grbctl10path="%s.grb.1p0deg.ctl"%(self.topath)
        self.grbgmp10path="%s.grb.1p0deg.gmp"%(self.topath)
        
        self.fdb10path="%s.wgrib1.txt"%(self.grb10path)

    def wgribFilter4Cgd6(self,override=1,verb=0):

        def doWgribFilter(grbpath):

            fdbpath="%s.wgrib1.txt"%(grbpath)
            
            MF.sTimer('tmtrkN.wgribFilter4Cgd6-grib1Inv')
    
            print 'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW',grbpath,fdbpath
            if( (override or not(MF.ChkPath(fdbpath))) and MF.ChkPath(grbpath) ):
                F=open(fdbpath,'w')
                F.writelines(grbpath+'\n')
                F.close()
                cmd="%s -V %s >> %s"%(self.xwgrib,grbpath,fdbpath)
                mf.runcmd(cmd,'')
            MF.dTimer('tmtrkN.wgribFilter4Cgd6-grib1Inv')
            
            (recs,recsiz,nrectot)=self.ParseFdb1(open(fdbpath).readlines())
            
            orecs=[]
            kk=recs.keys()
            kk.sort()
            nrec=1
            while(nrec <= kk[-1]):
                
                W=recs[nrec]
                #print '00000',nrec,W.var,W.tau,W.lev,W.gridvalmin
    
                # --  use order of variable output in TCtrk.TmTrk.gribInput2TmTrk
                #
                if(W.var == 'PRMSL' ):
                    
                    WP1=W          ; nrecp1=nrec ; nrec=nrec+1
                    WU1=recs[nrec] ; nrecu1=nrec ; nrec=nrec+1
                    WV1=recs[nrec] ; nrecv1=nrec ; nrec=nrec+1
                    WP2=recs[nrec] ; nrecp2=nrec ; nrec=nrec+1
                    # -- check if 4th var in 6-var sequence is psl
                    #
                    if(WP2.var != 'PRMSL'):
                        print 'WWW(TmTrkN.wgribFilter4Cgd6()) this grbpath has already been processed...'
                        return
                    
                    WU2=recs[nrec] ; nrecu2=nrec ; nrec=nrec+1
                    WV2=recs[nrec] ; nrecv2=nrec ; nrec=nrec+1
                    
                    if(WP1.nundef == 0):
                        ocardP="%d:%d:%03d:%s:%d:%d:%d:%f"%(nrecp1,WP1.sizrecp1,WP1.tau,WP1.var,WP1.lev,WP1.ndef,WP1.nundef,WP1.gridvalmin)
                        ocardP=ocardP+'\n'
                        nrecp=nrecp1
                    else:
                        ocardP="%d:%d:%03d:%s:%d:%d:%d:%f"%(nrecp2,WP2.sizrecp1,WP2.tau,WP2.var,WP2.lev,WP2.ndef,WP2.nundef,WP2.gridvalmin)
                        ocardP=ocardP+'\n'
                        nrecp=nrecp2
    
                    
                    if(WU1.nundef == 0):
                        ocardU="%d:%d:%03d:%s:%d:%d:%d:%f"%(nrecu1,WU1.sizrecp1,WU1.tau,WU1.var,WU1.lev,WU1.ndef,WU1.nundef,WU1.gridvalmin)
                        ocardU=ocardU+'\n'
                        nrecu=nrecu1
                    else:
                        ocardU="%d:%d:%03d:%s:%d:%d:%d:%f"%(nrecu2,WU2.sizrecp1,WU2.tau,WU2.var,WU2.lev,WU2.ndef,WU2.nundef,WU2.gridvalmin)
                        ocardU=ocardU+'\n'
                        nrecu=nrecu1
    
                    if(WV1.nundef == 0):
                        ocardV="%d:%d:%03d:%s:%d:%d:%d:%f"%(nrecv1,WV1.sizrecp1,WV1.tau,WV1.var,WV1.lev,WV1.ndef,WV1.nundef,WV1.gridvalmin)
                        ocardV=ocardV+'\n'
                        nrecv=nrecv1
                    else:
                        ocardV="%d:%d:%03d:%s:%d:%d:%d:%f"%(nrecv2,WV2.sizrecp1,WV2.tau,WV2.var,WV2.lev,WV2.ndef,WV2.nundef,WV2.gridvalmin)
                        ocardV=ocardV+'\n'
                        nrecv=nrecv2
                        
                    if(verb): print 'ccc',nrecp,ocardP[:-1]
                    orecs.append(ocardP)
                    if(verb): print 'ccc',nrecu,ocardU[:-1]
                    orecs.append(ocardU)
                    if(verb): print 'ccc',nrecv,ocardV[:-1]
                    orecs.append(ocardV)
    
                    # -- end of recs
                    #
                    if(nrec >= kk[-1]): continue
                    
                    # -- go to next one after this 6-rec sequence
                    #
                    W=recs[nrec]
                    
                ocard="%d:%d:%03d:%s:%d:%d:%d:%f"%(nrec,W.sizrecp1,W.tau,W.var,W.lev,W.ndef,W.nundef,W.gridvalmin)
                ocard=ocard+'\n'
                orecs.append(ocard)            
                
                if(verb): print 'ccc',nrec,ocard[:-1]
                nrec=nrec+1
                
            (dir,ogrbfile)=os.path.split(grbpath)
            ogrbpath="/tmp/%s"%(ogrbfile)
            self.Wgrib1Filter(orecs, grbpath,
                              "%s"%(ogrbpath))
            
            # -- now cp over
            #
            cmd="cp %s %s"%(ogrbpath,grbpath)
            mf.runcmd(cmd)
            
            return

        rc1=doWgribFilter(self.grbpath)
        rc2=doWgribFilter(self.grb10path)
            
        return


    def cleanAllFiles(self,dtgopt=None):

        
        def getfiles():
            # -- 20170214 -- kill off Pstate and stdout which are not really important to save
            files=glob.glob("fort.??*") + glob.glob("namelist*") + \
                glob.glob('fcst_minutes') + \
                glob.glob("tmtrk*.*") + glob.glob("stdout.*") + \
                glob.glob("*.dat") + glob.glob("Pstate*") 

            for file in files:
                try:
                    print 'KKilling: ',file
                    os.unlink(file)
                except:
                    print """WWW(TCtrk) can't unlink file: """,file


        if(MF.ChangeDir(self.tbdir) == 0):
            print 'EEE self.tdir not there in cleanFiles...'
            sys.exit()

        bddtg=None
        if(dtgopt != None):
            basedtgs=mf.dtg_dtgopt_prc(dtgopt)
            bddtg=basedtgs[-1]
            dtgs=basedtgs
        else:
            dtgs=glob.glob('??????????')


        for dtg in dtgs:

            if(bddtg != None):
                testdiff=mf.dtgdiff(bddtg,dtg)
                print dtg,bddtg,testdiff
                if(testdiff > 0.0): continue

            MF.ChangeDir(dtg)
            models=glob.glob('*')

            for model in models:
                MF.ChangeDir(model)

                print 'KKKKKKKKKKKKKKKKKKKK dtg: ',dtg,' model: ',model
                getfiles()

                MF.ChangeDir('../.')

            MF.ChangeDir('../.')

        return



    def cleanFiles(self):

        if(MF.ChangeDir(self.tdir) == 0):
            print 'EEE self.tdir not there in cleanFiles...'
            sys.exit()

        files=glob.glob("fort.??*") + glob.glob("namelist*") + \
            ['fcst_minutes',self.grbpath,self.grbctlpath,self.grbgmppath,self.grbixpath] + \
            [self.grb10path,self.grbctl10path,self.grbix10path,self.grbgmp10path] + glob.glob("%.wgrib?.txt") + \
            glob.glob("%s.*.*"%(self.model)) + glob.glob("ngtrk.*")  # add mftrkN data files and ngtrk files

        for file in files:
            try:
                os.unlink(file)
                print 'KKilling: ',file
            except:
                print """WWW(TCtrk) can't unlink file: """,file


    def setGrads(self,type='trk',override=0):

        if(type == 'trk'):
            aa=self.area
            (dir,gmp)=os.path.split(self.grbgmppath)
            (dir,grb)=os.path.split(self.grbpath)
            gmppath=self.grbgmppath
            ctlpath=self.grbctlpath
        elif(type == 'gen'):
            aa=self.areaGen
            (dir,gmp)=os.path.split(self.grbgmp10path)
            (dir,grb)=os.path.split(self.grb10path)
            gmppath=self.grbgmp10path
            ctlpath=self.grbctl10path
        else:
            print 'EEE invalid type in setGrads: ',type
            sys.exit()

        if(aa == None):
            print 'WWW(TCtmtrkN.setGrads) no TCs because self.area == None'
            return


        btau=self.taus[0]
        etau=self.taus[-1]
        dtau=self.taus[1]-self.taus[0]
        nt=int((etau-btau)/dtau) + 1

        dtype= "dtype grib 255"
        title= "title tmtrkN for model: %s dtg: %s"%(self.model,self.dtg)
        undef= "undef 9.999E+20"
        index= "index ^%s"%(gmp)
        dset=  "dset ^%s"%(grb)

        xdef="xdef %3d linear %5.2f %5.2f"%(aa.ni,aa.lonW,aa.dx)
        ydef="ydef %3d linear %5.2f %5.2f"%(aa.nj,aa.latS,aa.dy)
        zdef="zdef 13 levels 900 850 800 750 700 650 600 550 500 450 400 350 300"
        tdef="tdef  %s linear %s %dhr"%(nt,mf.dtg2gtime(self.dtg),dtau)
        vars="""vars 7
zg    13  7,100,  0 ** Geopotential height [gpm]
psl    0  2,102,  0 ** Pressure reduced to MSL [Pa]
ta401  0 11,100,401 ** Temp. [K]
ua    13 33,100,  0 ** u wind [m/s]
uas    0 33,105, 10 ** u wind [m/s]
va    13 34,100,  0 ** v wind [m/s]
vas    0 34,105, 10 ** v wind [m/s]
endvars"""

        ctl="""%s
%s
%s
%s
%s
%s
%s
%s
%s
%s"""%(dset,dtype,title,index,undef,xdef,ydef,zdef,tdef,vars)


        MF.WriteString2File(ctl,ctlpath,verb=1)

        # -- do gribmap
        #
        if(not(MF.ChkPath(gmppath)) or override):
            cmd="gribmap -i %s"%(ctlpath)
            mf.runcmd(cmd)


    def setTCs(self,ropt='',override=0):
        (self.istmids,self.btcs)=self.tcD.getDtg(self.dtg)
        

    def setFldGrid(self,ropt='',override=0):

        if(len(self.istmids) == 0):
            aa=TmTrkAreaGlobal()
            aa=None
        else:
            dx=dy=0.5
            if(self.regridTracker != 0): dx=dy=self.regridTracker
            self.hemigrid=getHemis(self.istmids)

            if(self.hemigrid == 'nhem'):   aa=TmTrkAreaNhem(dx=dx,dy=dy)
            if(self.hemigrid == 'shem'):   aa=TmTrkAreaShem(dx=dx,dy=dy)
            if(self.hemigrid == 'global'): aa=TmTrkAreaGlobal(dx=dx,dy=dy)

        self.area=aa
        dx=dy=1.0
        if(self.regridGen != 0): dx=dy=self.regridGen
        self.areaGen=TmTrkAreaTropics(dx=dx,dy=dy)

        # override to test with more general code
        #
        #self.area=W2areaGlobal()

    def setReargs(self,area):

        aa=area

        if(aa == None):
            print 'WWW(TmTrkN.setReargs) - doing -t?  need -t -O to regen the .pyp...if this fails...'
            
        if(self.remethod == ''):
            self.reargs="%d,%s,%f,%f,%d,%s,%f,%f"%(aa.ni,self.rexopt,aa.lonW,aa.dx,aa.nj,self.reyopt,aa.latS,aa.dy)
        else:
            self.reargs="%d,%s,%f,%f,%d,%s,%f,%f,%s"%(aa.ni,self.rexopt,aa.lonW,aa.dx,aa.nj,self.reyopt,aa.latS,aa.dy,self.remethod)

        if(not(self.doregrid)): self.reargs=None




    def makeNamelist(self,trkmode='tracker',basin='global'):

        dtg=self.dtg
        atcfname=self.atcfname

        cc=dtg[0:2]
        yy=dtg[2:4]
        mm=dtg[4:6]
        dd=dtg[6:8]
        hh=dtg[8:10]

        modtyp='global'
        gridtype='global'

        if(hasattr(self,'area') and mf.find(trkmode,'tracker') ):
            lat1=self.area.latS
            lat2=self.area.latN
            lon1=self.area.lonW
            lon2=self.area.lonE
            modtyp='regional'
            gridtype='regional'

        elif(hasattr(self,'areaGen') and mf.find(trkmode,'tcgen') ):
            lat1=self.areaGen.latS
            lat2=self.areaGen.latN
            lon1=self.areaGen.lonW
            lon2=self.areaGen.lonE
            modtyp='regional'
            gridtype='regional'

        # -- get search lat/lon based on basin
        #
        (lat1,lat2,lon1,lon2)=getBasinLatLons(basin)

        if(trkmode == 'trackeronly'):
            trkmode='tracker'
            pflag='n'
        elif(trkmode == 'tracker'):
            pflag='y'
        elif(trkmode == 'tcgen'):
            pflag='y'
        else:
            print 'EEE invalid trkmode: ',trkmode
            sys.exit()


        if(hasattr(self,'searchLatS')): lat1=self.searchLatS
        if(hasattr(self,'searchLatN')): lat2=self.searchLatN

        # -- pull last 4 char from name -- limitation of gettrk_genN.x application
        #
        atcfnameNL=atcfname[-4:]

        # ---- turn off tcstruct
        #
        namelist="""&datein
  inp%%bcc=%s,
  inp%%byy=%s,
  inp%%bmm=%s,
  inp%%bdd=%s,
  inp%%bhh=%s,
  inp%%model=17,
  inp%%modtyp='%s',
  inp%%lt_units='hours'
  inp%%file_seq='onebig',
  inp%%nesttyp='',
/
&atcfinfo
  atcfnum=83,
  atcfname='%s',
  atcfymdh=%s
/
&trackerinfo
  trkrinfo%%southbd=%5.1f,
  trkrinfo%%northbd=%5.1f,
  trkrinfo%%westbd=%5.1f,
  trkrinfo%%eastbd=%5.1f,
  trkrinfo%%type='%s',
  trkrinfo%%mslpthresh=0.0015,
  trkrinfo%%v850thresh=1.5000,
  trkrinfo%%gridtype='%s',
  trkrinfo%%contint=100.0,
  trkrinfo%%out_vit='y'
/
&phaseinfo 
  phaseflag='%s',
  phasescheme='both',
  wcore_depth=1.0
/
&structinfo 
  structflag='n',
  ikeflag='n'
/
&fnameinfo
  gmodname='gfso',
  rundescr='xxxx',
  atcfdescr='xxxx'
/
&verbose
  verb=2
/
"""%(cc,yy,mm,dd,hh,modtyp,atcfnameNL,dtg,lat1,lat2,lon1,lon2,trkmode,gridtype,pflag)

        return(namelist)

    def invTrk(self,quiet=0):


        def chkStdout(path):
            nstop=0
            nerr=0
            cards=open(path).readlines()
            for card in cards:
                if(MF.find(card,'STOP')): nstop=nstop+1
                if(MF.find(card,'ERROR')): nerr=nerr+1

            return(nerr,nstop)


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

        def vmaxMS2KT(vmax):

            if(vmax%5 < 2.5):
                vmax=5*int(vmax/5)
            elif(vmax%5 >= 2.5):
                vmax=5*(int(vmax/5)+1)
            return(vmax)

        def setOtaus(stm3id,otaus):

            tag='C'
            if(otaus[0] == 999):
                otausC=" T:***-***"
                tag='m'
            elif(otaus[0] == 888):
                otausC=" T:SSS-SSS"
                tag='S'
            elif(otaus[0] == 777):
                otausC=" T:FFF-FFF"
                tag='F'
            elif(otaus[0] == 666):
                otausC=" T:EEE-EEE"
                tag='E'
            else:
                otausC=" T:%03d-%03d"%(otaus[0],otaus[1])
                if(otaus[0] == otaus[1]):
                    tag='s'
                elif(otaus[1] < self.maxtauModel):
                    tag='i'

            otausC=otausC+' '+tag

            tauStatus[stm3id]=tag
            return(otausC)


        def setStatus(osizS,nerr,nstop,nfail,type='trk',
                      nerrminTrk=5,
                      nerrminGen=10,
                      ):

            status=''' OK..  '''
            if(osizS == None): status=''' FAIL!!'''
            if(nstop == 1):    status=''' STOP!!'''
            if(nstop == -1):   status=''' ToDo..'''
            if(type == 'trk' and nerr > nerrminTrk):      status=''' ERR...'''
            if(type == 'gen' and nerr > nerrminGen):      status=''' ERR...'''
            status="%s %3d %1d %1d"%(status,nerr,nstop,nfail)
            return(status)


        def chkTcgen(siz,path):
            if(siz == None):
                ncards=-1
                taus=None
                return(ncards,taus)

            cards=open(path).readlines()
            ncards=len(cards)
            genstms=[]
            for card in cards:
                tt=card.split(',')
                for n in range(0,len(tt)):
                    t1=tt[n].strip()
                    if(n == 1 and tt[0] == 'TG'): genstms.append(t1)

            genstms=mf.uniq(genstms)

            return(ncards,genstms)

        #ssssssssssssssssssssssssssssssssssssssssssssssssss start
        #
        nerrminTrk=15
        nerrminGen=30

        stmCards=[]
        genCards=[]

        stm3ids=[]
        tauStatus={}

        tcs=self.tcVcards.split('\n')
        for tc in tcs:
            if(len(tc) > 0):
                tt=tc.split()
                stm3ids.append((tt[1],tt[5],tt[6],int(tt[12])*1.94+0.5))

        stm3ids.sort()

        for (stm3id,lat,lon,vmax) in stm3ids:
            nerr=nstop=-1
            lstm3id=stm3id.lower()

            tctrkAtcf="%s/tctrk.atcf.%s.%s.%s.txt"%(self.tdir,self.dtg,self.model,lstm3id)
            sizA=MF.GetPathSiz(tctrkAtcf)
            stdout="%s/stdout.tctrk.%s.%s.%s.txt"%(self.tdir,self.dtg,self.model,lstm3id)
            sizS=MF.GetPathSiz(stdout)
            (dtimei,ldtg,gdtgS)=MF.PathModifyTime(stdout)

            nfail=0
            if(sizS != None): (nerr,nstop)=chkStdout(stdout)
            else:              nfail=nfail+1

            (ncards,taus)=chkAtcf(sizA,tctrkAtcf)
            if(taus == None and nerr == 0):
                otaus=(999,999)
            elif(nstop > 0):
                otaus=(888,888)
            elif(nfail > 0):
                otaus=(777,777)
            elif(nerr  > nerrminTrk):
                otaus=(666,666)
            elif(taus == None):
                otaus=(555,555)
            else:
                otaus=(taus[0],taus[-1])

            if(sizA == None): osizA=-999
            else:             osizA=int(sizA)
            if(sizS == None): osizS=-999
            else:             osizS=int(sizS)


            stat=setStatus(osizS,nerr,nstop,nfail,type='trk',nerrminTrk=nerrminTrk,nerrminGen=nerrminGen)
            ocardAtcf="%5s %s  V:%03d"%(stm3id,stat,vmaxMS2KT(vmax))
            ocard=ocardAtcf + setOtaus(stm3id,otaus) + "%7d %7d  %s"%(osizA,osizS,gdtgS) + "  %4s %5s  "%(lat,lon) + tctrkAtcf
            stmCards.append(ocard)
            if(not(quiet)): print ocard


        basinStatus={}

        tcgenDone=1
        for basin in tcgenBasins:

            tcgenAtcf="%s/tcgen.atcf.%s.%s.%s.txt"%(self.tdir,basin,self.dtg,self.model)
            sizA=MF.GetPathSiz(tcgenAtcf)
            (ncards,genstms)=chkTcgen(sizA,tcgenAtcf)
            stdout="%s/stdout.tcgen.%s.%s.%s.txt"%(self.tdir,basin,self.dtg,self.model)
            sizS=MF.GetPathSiz(stdout)
            (dtimei,ldtg,gdtgS)=MF.PathModifyTime(stdout)

            if(genstms == None):
                tcgenDone=0
                break

            nfail=0
            if(sizS != None): (nerr,nstop)=chkStdout(stdout)
            else:             nfail=1

            basinStatus[basin]=(nstop,nfail)

            if(sizA == None): osizA=-999
            else:             osizA=int(sizA)
            if(sizS == None): osizS=-999
            else:             osizS=int(sizS)

            ngenstms=len(genstms)
            stat=setStatus(osizS,nerr,nstop,nfail,type='gen',nerrminTrk=nerrminTrk,nerrminGen=nerrminGen)
            ocard="%5s %s  Ntcg: %2d  %7d %7d %s"%(basin,stat,ngenstms,osizA,osizS,tcgenAtcf)
            if(not(quiet)): print ocard
            genCards.append(ocard)


        nTC=len(stm3ids)
        nFail=0
        nStop=0
        nComplete=0
        nMiss=0
        nIncomplete=0
        nSingle=0
        nErr=0

        for (stm3id,lat,lon,vmax) in stm3ids:
            tag=tauStatus[stm3id]
            if(tag == 'C'): nComplete=nComplete+1
            if(tag == 'm'): nMiss=nMiss+1
            if(tag == 'i'): nIncomplete=nIncomplete+1
            if(tag == 's'): nSingle=nSingle+1
            if(tag == 'F'): nFail=nFail+1
            if(tag == 'S'): nStop=nStop+1
            if(tag == 'E'): nErr=nErr+1

        if(nMiss == nTC):
            nGood=0
        else:
            nGood=nTC-nFail-nStop
        ocardSumStm="stmSum: nGood: %2d/%-2d  nErr: %2d/%-2d  nFail: %2d  nStop: %2d  nComplete: %2d  nMiss: %2d  nIncomplete: %2d  nSingle: %2d nTC: %2d "%(nGood,nTC,nErr,nTC,nFail,nStop,nComplete,nMiss,nIncomplete,nSingle,nTC)
        if(not(quiet)): print ocardSumStm
        self.invTmtrkN[self.dtg,self.model,'sumStm']=ocardSumStm

        nFail=0
        nStop=0
        nComplete=0
        nBasin=len(tcgenBasins)
        nGood=nBasin
        nErr=0

        for basin in tcgenBasins:
            if(not(tcgenDone)):
                nGood=0
                continue
            (nstop,nfail)=basinStatus[basin]

            if(nstop == 0 and nfail == 0): nComplete=nComplete+1
            if(nstop == 1):
                nStop=nStop+1
                nGood=nGood-1
            if(nfail == 1):
                nFail=nFail+1
                nGood=nGood-1

            tag=tauStatus[stm3id]
            if(tag == 'C'): nComplete=nComplete+1
            if(tag == 'm'): nMiss=nMiss+1
            if(tag == 'i'): nIncomplete=nIncomplete+1
            if(tag == 's'): nSingle=nSingle+1
            if(tag == 'F'): nFail=nFail+1
            if(tag == 'E'): nErr=nErr+1

        ocardSumGen="stmGen: nGood: %2d/%-2d  nErr: %2d/%-2d  nFail: %2d  nStop: %2d"%(nGood,nBasin,nErr,nBasin,nFail,nStop)
        if(not(quiet)): print ocardSumGen

        self.invTmtrkN[self.dtg,self.model,'sumGen']=ocardSumGen
        self.invTmtrkN[self.dtg,self.model,'stm']=stmCards
        self.invTmtrkN[self.dtg,self.model,'gen']=genCards

        if(hasattr(self,'dsL')):
            self.dsL.data=self.invTmtrkN
            self.DSs.putDataSet(self.dsL,key=self.dbkeyLocal)
            self.DSs.closeDataSet()


        return

    def chkInv(self,verb=0):

        try:
            self.invTmtrkN[self.dtg,self.model,'sumGen']
        except:
            try:
                self.invTrk(quiet=1)   
            except:
                print 'WWW TCtmtrkN.chkInv no invTmtrkN or invTrk failed...rc=0 and return'
                rc=0
                return(rc)

        gen=self.invTmtrkN[self.dtg,self.model,'sumGen']
        trk=self.invTmtrkN[self.dtg,self.model,'sumStm']
        tt=gen.split()
        pdonegen=0
        (ngood,nall)=tt[2].split('/')
        if(nall > 0):
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

    def relabelAdeckDirTrackers(self,verb=0):

        if(hasattr(self,'tdirAdeck')):
            sdir=self.tdirAdeck
        else:
            sdir=self.tdir
        tdir="%s/%s/%s/%s"%(AdeckBaseDir,self.trackerName,self.dtg[0:4],self.dtg)
        
        trackers=glob.glob("%s/%s"%(tdir,self.trackerAdmask))
        curtrackers=glob.glob("%s/*.???.????"%(tdir))

        stmids=self.istmids
        
        atcfTrks=[]
        tcvstm3s=[]
        relabelStmids={}
        
        gotTCvitals=0
        for tracker in trackers:
            if(mf.find(tracker,'tctrk')):
                atcfTrks.append(tracker)

            
            if(mf.find(tracker,'tcvital')):
                cards=open(tracker).readlines()
                for card in cards:
                    tcvstm3s.append(card.split()[1])
                gotTCvitals=1

        # -- see if object has tcvcards
        #
        if(hasattr(self,'tcVcards')):
            cards=self.tcVcards
            cards=cards.split('\n')
            for card in cards:
                if(len(card) > 0):
                    tcvstm3s.append(card.split()[1])
                
            gotTCvitals=1
        

        # -- rm new form if override
        #
        if(self.override):
            if(len(curtrackers) > 0):
                if(self.atcfname != None):
                    cmd="rm -f %s/tc???.*.%s.???.????"%(tdir,self.atcfname.lower())
                else:
                    cmd="rm -f %s/*.???.????"%(tdir)
                mf.runcmd(cmd,'')
            curtrackers=glob.glob("%s/*.???.????"%(tdir))
            
        if(gotTCvitals == 0):

            for atcfTrk in atcfTrks:
                (dir,file)=os.path.split(atcfTrk)
                tt=file.split('.')
                if(len(tt) == 6): tcvstm3s.append(tt[-2].upper())

            tcvstm3s=mf.uniq(tcvstm3s)

        for tcvstm3 in tcvstm3s:
            for stmid in stmids:
                stm3=stmid.split('.')[0]

                # -- direct matches
                #
                if(tcvstm3 == stm3):
                    relabelStmids[tcvstm3]=stmid
                    relabeltype=0
                    

        if(verb): print 'stmids: ',stmids,'tcvstm3s: ',tcvstm3s

        relabeltype=0
        for tcvstm3 in tcvstm3s:
            try:
                relabelStmids[tcvstm3]
            except:
                relabeltype=-999
                print 'no dirrect match for:',tcvstm3,'... look for 9x...tcvstm3s: ',tcvstm3s
                for stmid in stmids:
                    stm3=stmid.split('.')[0]
                    if(  ( tcvstm3[0] == '9') and 
                         ( (tcvstm3[2] == stm3[2]) or
                           ( (tcvstm3[2] == 'A' or tcvstm3[2] == 'B') and stm3[2] == 'I') or
                           ( (tcvstm3[2] == 'S' or tcvstm3[2] == 'P') and stm3[2] == 'S')
                           )
                         ):
                        relabeltype=1
                        relabelStmids[tcvstm3]="%s.%s"%(tcvstm3,stmid.split('.')[1])

                    # -- misslabel of S/P or A/B
                    #
                    if(  ( int(tcvstm3[0:2]) == int(stm3[0:2]) ) and
                         ( 
                           ( (stm3[2] == 'A' or stm3[2] == 'B') and tcvstm3[2] == 'I' ) or
                           ( (stm3[2] == 'S' or stm3[2] == 'P') and tcvstm3[2] == 'S')
                           )
                         ):
                        relabeltype=2
                        relabelStmids[tcvstm3]=stmid

                    if(  ( int(tcvstm3[0:2]) == int(stm3[0:2]) ) and
                         ( (tcvstm3[2] == stm3[2]) or
                           ( (tcvstm3[2] == 'A' or tcvstm3[2] == 'B') ) or
                           ( (tcvstm3[2] == 'S' or tcvstm3[2] == 'P') )
                           )
                         ):
                        relabeltype=3
                        relabelStmids[tcvstm3]="%s.%s"%(tcvstm3.upper(),stmid.split('.')[1])

        if(relabeltype != -999):
            print 'TTTTT dtg: ',self.dtg,'gotTCvitals: ',gotTCvitals,' relabeltype: ',relabeltype,' stmids: ',stmids,' #atcfGtrks: ',len(atcfTrks)
        else:
            print '00000 dtg: ',self.dtg,'stmids: ',stmids,' = NADA or #atcfTrks: ',len(atcfTrks)
                
        tcvok=1
        for tcvstm3 in tcvstm3s:
            try:
                relabelStmids[tcvstm3]
            except:
                print '2nd pass no dirrect match for:',tcvstm3,'... look for 9x...'
                #sys.exit()
                tcvok=1
                
        if(tcvok):

            cpopt='-n -p'
            if(self.override): cpopt='-p'
            for atcfTrk in atcfTrks:
                oldTrkr=atcfTrk
                for tcvstm3 in tcvstm3s:
                    try:
                        newTrkr=atcfTrk.replace("%s.txt"%(tcvstm3.lower()),relabelStmids[tcvstm3])
                    except:
                        continue
                    if(newTrkr != atcfTrk):
                        if(verb): 
                            print
                            print 'oooo:',oldTrkr
                            print 'nnnn:',newTrkr
                        
                        cmd="cp %s %s %s"%(cpopt,oldTrkr,newTrkr)
                        mf.runcmd(cmd,'')
        






