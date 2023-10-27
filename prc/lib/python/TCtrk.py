from WxMAP2 import *
w2=W2()

from tcbase import *
from ATCF import *
from ga2 import setGA,GaLatsQ

SetLandFrac=w2.SetLandFrac
GetLandFrac=w2.GetLandFrac

lf=SetLandFrac()

def getLF(lf,lat,lon):
    landfrac=GetLandFrac(lf,lat,lon)
    return(landfrac)

tcgenW3DatDir='/w3/rapb/hfip/tcgen_dat'
tcgenW3DatDir='/w3/rapb/hfip/tcgenDAT'
tcgenW3Dir='/w3/rapb/hfip/tcgen'

tcgenW3DatDir="%s/tcgenDat"%(w2.HfipProducts)
tcgenW3Dir="%s/tcgen"%(w2.HfipProducts)

# -- 20200329 -- reset so goes to root of web dir
#
if(w2.onTenki):
    tcgenW3DatDir=w2.tcgenBaseDirWeb
    # -- 20210124 -- for grads to find bm.????.png
    tcgenW3Dir="%s/tcgen"%(w2.W2BaseDirWebConfigROOT)
    

tcgenModels=['gfs2','fim8','rtfimz','ecm2','ukm2','ngp2','cmc2','ngpc']
tcgenModels=['gfs2','fim8','ecm2','ukm2','cmc2','ngpc','rtfimy']
tcgenModels=['gfs2','rtfimy','fim8','ecm2','ukm2','ngpc']
# 2012 hfip demo
tcgenModels=['gfs2','fim8','ecmn','ukm2','ngpc']
tcgenModels=['gfs2','fim8','ecm2','ukm2','navg','cmc2','rtfim9']
# -- 2017020112 - ecm4 is 0.25 data but plots ecm2
tcgenModels=['gfs2','fim8','ecm4','ukm2','navg','cmc2','rtfim9']
# -- 20180112 - deprecate *fim* add fv3e and g
tcgenModels=['gfs2','ecm4','ukm2','fv3e','fv3g','navg','cmc2']

if(w2.onTenki):
    tcgenModels=['gfs2','ecm5','cgd2','navg','jgsm']      # -- 20190201 -- take out fv3? until we get real-time runs sorted add ecm5
    #tcgenModelsJS=['gfs2','ecm2','fv7e','fv7g']                        # -- 20190326 -- for analyzing fv7 runs on tenki7
    tcgenModelsJS=['gfs2','ecm5','cgd2','navg','jgsm']                        # -- 20200114 -- direct ecmwf hres feed
    
else:
    tcgenModels=['gfs2','ecm4','ukm2','navg','cmc2']  # -- 20190201 -- take out fv3? until we get real-time runs sorted
    tcgenModelsJS=['gfs2','ecm2','ukm2','cmc2','navg']                 # -- 20190201 -- take out fv3? until local runs sorted


tcgenBasins=['lant','epac','wpac','shem','nio']
#tcgenBasins=['lant','epac','wpac','nio']

b1id2tcgenBasin={
    'w':'wpac',
    'e':'epac',
    'c':'epac',
    'l':'lant',
    's':'shem',
    'p':'shem',
    'a':'nio',
    'b':'nio',
    't':'lant',
    }

tcgenModelLabel={
    'gfs2':'NCEP.GFS',
    'gfsk':'ESRL.GFSK',
    'ecm2':'ECMWF.IFS',
    'ecm4':'ECMWF.HRES',
    'ecm5':'ECMWF.HRES-01',
    'jgsm':'JMA GSM',
    'ecmn':'ECMWF.IFS',
    'ecmt':'ECMWF.IFS-05',
    'ngp2':'FNMOC.NGP',
    'ngpc':'FNMOC.NGP',
    'navg':'FNMOC.NAVGEM',
    'ukm2':'UKMO.UM',
    'cmc2':'CMC.GEM',
    'cgd6':'CMC.GDP',
    'cgd2':'CMC.GDPH',
    'fv3e':'ESRL.FV3-NCEP',
    'fv3g':'ESRL.FV3-GF',
    'fv7e':'ESRL.FV3-NCEP',
    'fv7g':'ESRL.FV3-GF',
    'fim8':'ESRL.FIM',
    'rtfim':'ESRL.FIM',
    'rtfim9':'ESRL.FIM9',
    'rtfimy':'ESRL.FIMY',
    'rtfimx':'ESRL.FIMX',
    'rtfimz':'ESRL.FIMZ',
    }


#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# local classes
#

class TmTrk(MFbase):

    def __init__(self,
                 dtg,
                 model,
                 atcfname,
                 tdir,
                 tdirAdeck,
                 taus,
                 maxtauModel,
                 ctlpath,
                 tcD=None,
                 mintauTC=120,
                 maxtauTC=168,
                 verb=0,
                 domdeck=0,
                 trkmode='tracker',
                 domodelpyp=0,
                 dolstcs=0,
                 quiet=0,
                 regridTracker=0.5,
                 #regridGen=1.0,
                 regridGen=0.5, #--  20180109 hi-res grids also changed in TCtrk.py, but effective only here
                 trackerName='tmtrk',
                 trackerAdmask="tc*.txt",
                 xgrads='grads',
                 ):

        self.dtg=dtg
        self.model=model
        self.atcfname=atcfname
        self.tdir=tdir
        self.tdirAdeck=tdirAdeck
        self.taus=taus
        self.maxtauModel=maxtauModel
        self.doga2=0
        #self.trkApp='gettrk_gen.x'
        self.trkApp='gettrk_genN.x'
        self.xgrads=xgrads
        
        MF.ChkDir(tdir,'mk')
        
        self.ctlpath=ctlpath

        self.mintauTC=mintauTC
        self.maxtauTC=maxtauTC

        self.verb=verb
        self.quiet=quiet
        self.dolstcs=dolstcs

        self.prcdir="%s/tctrk"%(os.getenv("W2_PRC_DIR"))
        if(domodelpyp):
            self.pyppath="%s/Pstate.%s.pyp"%(tdir,model)
        else:
            self.pyppath="%s/Pstate.pyp"%(tdir)

        self.initCurState() # from MFbase

        if(not(w2.onWjet)):
            MF.ChkDir(self.tdir,'mk')
            MF.ChkDir(self.tdirAdeck,'mk')

        self.trkmode=trkmode
        self.regridGen=regridGen
        self.regridTracker=regridTracker
        
        if(domdeck):
            self.year=dtg[0:4]
            dsbdir="%s/DSs"%(TcDataBdir)
            dbname='mdecks'
            dbfile="%s.pypdb"%(dbname)
            DSs=DataSets(bdir=dsbdir,name=dbfile,dtype=dbname,verb=self.verb)
            self.mDs=DSs.getDataSet(key=self.year).md


        # -- option to input tcD
        #
        if(tcD == None):
            self.tcD=TcData(dtgopt=self.dtg,verb=verb)
        else:
            self.tcD=tcD

        


    def lstrk(self,nhead=3,ncol=144,lsopt='s',ncprint=100,dupchk=1,selectNN=1):

        if(not(hasattr(self,'tcD'))):
            print 'TTTTTTTTTTTTTTT making tcD...in lstrk'
            sys.exit()

            
        tdir=self.tdirAdeck
        tdir="%s/%s/%s/%s"%(AdeckBaseDir,self.trackerName,self.dtg[0:4],self.dtg)
        
        if(hasattr(self,'dolstcs') and self.dolstcs):
            print "Dtg: %s"%(self.dtg)
            stmids=self.tcD.getStmidDtg(self.dtg,dupchk=dupchk,selectNN=selectNN)
            stmids.sort()
            for stmid in stmids:
                rc=self.tcD.getBtLatLonVmaxPmin(stmid,stmdtg=self.dtg,dupchk=dupchk,selectNN=selectNN)
                if(rc == None):
                    print 'WWW TCtrk.lstrk() no bt for stmid: ',stmid,' dtg: ',self.dtg
                    continue
                
                (lat,lon,vmax,pmin)=rc
                (clat,clon)=self.tcD.rlatLon2clatLon(lat,lon)
                print "%s %s %s %03d %4.0f"%(stmid,clat,clon,int(vmax),float(pmin))


        lasttau=-999
        if(hasattr(self,'taus') and self.taus != None):
            oldtaus=self.taus
            oldtaus.sort()
            if(len(oldtaus) > 0):
                lasttau=oldtaus[-1]
            else:
                lasttau=None

        if(hasattr(self,'trkmodes')):
            nruns=len(self.trkmodes)
            latesttrkmode=self.trkmodes[nruns-1]
        else:
            nruns=1
            latesttrkmode=None

        if(hasattr(self,'dtimes')):
            kk=self.dtimes.keys()
            kk.sort()
            lsline=1
            
            # -- print stats last run kk[:-1] vice all kk  ...
            #
            for k in kk[:-1]:
                if(lsopt == 's' and not(k == 'all')): lsline=0
                if(lsline):
                    for n in range(0,nruns):
                        try:        dtime=self.dtimes[k][n]
                        except:     dtime=0
                        try:     curdtime=self.curdtimes[k][n]
                        except:  curdtime=None
                        try:     curtrkmode=self.trkmodes[n]
                        except:  curtrkmode=None
                        
                        card="time for: %20s t: %s m:s  model: %6s  dtg: %s"%(k,
                                                                              MF.min2minsec(dtime/60.0),
                                                                              self.model,self.dtg
                                                                              )

                        card="%s   curdtime: %s   lasttau: %3d  trkmode: %-12s   n: %d"%(card,
                                                                                     curdtime,
                                                                                     lasttau,
                                                                                     curtrkmode,
                                                                                     n+1)
                        print card
                    

        if(not(lsopt == 's')): print

        omodel=self.model
        if(self.atcfname != None): omodel=self.atcfname.lower()
        
        if(hasattr(self,'tdirAdeck') and lsopt != 's'):
            MF.sTimer('trklslong')
            tmask="%s/tctrk.atcf.%s.%s.txt"%(tdir,self.dtg,omodel)
            trks=glob.glob(tmask)
            for adeck in trks:
                cards=open(adeck).readlines()
                ncprint=min(ncprint,len(cards))
                for n in range(0,ncprint):
                    print cards[n][0:ncol]

            gens=glob.glob("%s/tcgen.atcf.lant.%s.%s.txt"%(self.tdirAdeck,self.dtg,omodel))
            gens=gens+glob.glob("%s/tcgen.atcf.epac.%s.%s.txt"%(self.tdirAdeck,self.dtg,omodel))
            gens=gens+glob.glob("%s/tcgen.atcf.wpac.%s.%s.txt"%(self.tdirAdeck,self.dtg,omodel))
            gens=gens+glob.glob("%s/tcgen.atcf.shem.%s.%s.txt"%(self.tdirAdeck,self.dtg,omodel))
            gens=gens+glob.glob("%s/tcgen.atcf.nio.%s.%s.txt"%(self.tdirAdeck,self.dtg,omodel))
            alltrks=trks+gens
            for trk in alltrks:
                (mtimei,mtime)=MF.PathModifyTimei(trk)
                print 'file: %-100s'%(trk),' siz: %-10d mtime %s'%(MF.GetPathSiz(trk),mtime)
                
            MF.dTimer('trklslong')

        if(hasattr(self,'tdirAdeck') and lsopt == 's'):
            gens=[]
            #MF.sTimer('trkshort')
            tmask="%s/tctrk.atcf.%s.%s.txt"%(self.tdirAdeck,self.dtg,omodel)
            trks=glob.glob(tmask)
            #gens=glob.glob("%s/tcgen.atcf.lant.%s.%s.txt"%(self.tdirAdeck,self.dtg,omodel))
            #gens=gens+glob.glob("%s/tcgen.atcf.epac.%s.%s.txt"%(self.tdirAdeck,self.dtg,omodel))
            #gens=gens+glob.glob("%s/tcgen.atcf.wpac.%s.%s.txt"%(self.tdirAdeck,self.dtg,omodel))
            #gens=gens+glob.glob("%s/tcgen.atcf.shem.%s.%s.txt"%(self.tdirAdeck,self.dtg,omodel))
            #gens=gens+glob.glob("%s/tcgen.atcf.nio.%s.%s.txt"%(self.tdirAdeck,self.dtg,omodel))
            alltrks=trks+gens
            for trk in alltrks:
                (mtimei,mtime)=MF.PathModifyTimei(trk)
                print 'YYYYY %s : %s : %-100s'%(self.dtg,omodel,trk),' siz: %-10d mtime: %s'%(MF.GetPathSiz(trk),mtime)

            #MF.dTimer('trkshort')

            if(len(alltrks) == 0):
                return(0)
            else:
                return(1)




    def chkTrkStatus(self,
                     diag=1,
                     override=0,
                     tcvitalsoverride=1,
                     dupchk=0,  # -- 20181231 -- force using all
                     ):

        # --- get # of TCs
        #
        if(not(hasattr(self,'tcD'))):
            tcD=TcData(dtgopt=self.dtg,verb=verb)

        tcs=self.tcD.getStmidDtg(self.dtg)

        # -- make the tcD object and the tcV object for this dtg
        #

        tcV=self.tcD.getTCvDtg(self.dtg,dupchk=dupchk)
        
        if(tcV == None):
            self.ntcs=0
        else:
            self.ntcs=len(tcV.stmids)

        self.tcV=tcV

        # -- make tcvitals2 file
        #
        if(self.ntcs > 0 and tcvitalsoverride):
            MF.sTimer(tag='tcvitals-override')
            self.tcVcards=self.tcV.makeTCvCards(override=override,filename='tcvitals',verb=1,writefile=1)
            self.tcvpath=self.tcV.tcvpath
            MF.dTimer(tag='tcvitals-override')
        else:
            # -- if no tcs, set to None
            #
            self.tcvpath=None


        if(not(hasattr(self,'mintauTC'))): self.mintauTC=120
        if(not(hasattr(self,'maxtauTC'))): self.maxtauTC=168
           
        if(not(hasattr(self,'pyppath'))): self.pyppath="%s/Pstate.pyp"%(self.tdir)
        if(not(hasattr(self,'maxtauModel'))): self.maxtauModel=-999

        
        prevtaus=None
        curtaus=None

        if(hasattr(self,'taus')): curtaus=self.taus
        if(hasattr(self,'prevtaus')): prevtaus=self.prevtaus

        if(curtaus == None):
            print """EEE no taus, bail with rc=-1, shouldn't have gotten here..."""
            sys.exit()

        curtaus.sort()
        lasttau=curtaus[-1]

        if(prevtaus != None):
            prevtaus.sort()
            prevlasttau=prevtaus[-1]
        else:
            prevlasttau=lasttau

        if(not(hasattr(self,'trkmode'))): self.trkmode=trkmode
        runtrkmode=self.trkmode
        
        if(curtaus != None):  curlasttau=curtaus[-1]
        else:                 curlasttau=lasttau

        if(hasattr(self,'trkmodes')):
            nruns=len(self.trkmodes)
            latesttrkmode=self.trkmodes[nruns-1]
        else:
            nruns=1
            latesttrkmode=None

        # ------------------------- basic return code = 0 or run hasn't been made so do it!
        #
        rc=-999


        # -- check if this mode done
        #
        donetracker=0
        donetrackeronly=0
        
        for n in range(0,nruns):

            if(hasattr(self,'trkmodes')):
                latesttrkmode=self.trkmodes[n]

            curdtime=None
            if(hasattr(self,'curdtimes')):
                try:     curdtime=self.curdtimes['all'][n]
                except:  pass

            #print '0000000 ',latesttrkmode,runtrkmode,curdtime
            if(latesttrkmode != None and latesttrkmode == 'tracker'): donetracker=1
            if(latesttrkmode != None and latesttrkmode == 'trackeronly'): donetrackeronly=0


        # -- now check each run to see what happened...
        #

        trackerstates=[]
        trackeronlystates=[]

        for n in range(0,nruns):

            if(hasattr(self,'trkmodes')):  curtrkmode=self.trkmodes[n]
            else:                          curtrkmode=None

            if(hasattr(self,'otctrkpaths')):
                try:     curtrkpath=self.otctrkpaths[n]
                except:  curtrkpath='/dev/null'

            elif(hasattr(self,'otctrkpath')):  curtrkpath=self.otctrkpath
            else:                              curtrkpath='/dev/null'

            try:     lentrkpath=os.path.getsize(curtrkpath)
            except:  lentrkpath=-999


            if(hasattr(self,'otcgenpaths')):
                try:      curgenpath=self.otcgenpaths[n]
                except:   curgenpath='/dev/null'
            elif(hasattr(self,'otcgenpath')):  curgenpath=self.otcgenpath
            else:                              curgenpath='/dev/null'

            try:     lengenpath=os.path.getsize(curgenpath)
            except:  lengenpath=-999


            if(curtrkmode == 'tracker'):
                trackerstates.append((curtrkpath,lentrkpath,curgenpath,lengenpath))
            elif(curtrkmode == 'trackeronly'):
                trackeronlystates.append((curtrkpath,lentrkpath,curgenpath,lengenpath))
                


        ntrkruns=len(trackerstates)
        ntrkonlyruns=len(trackeronlystates)

        # ----------------------------------- only check tracker mode and only taus...
        #

        if(runtrkmode == 'tracker' and len(trackerstates) > 0):

            (latesttrkpath,latestlentrkpath,latestgenpath,latestlengenpath)=trackerstates[-1]

            for tstate in trackerstates:

                (curtrkpath,curlentrkpath,curgenpath,curlengenpath)=tstate

                # -- case of no tcs
                #
                if(curlasttau >= self.mintauTC and curlasttau >= self.maxtauTC and self.ntcs == 0):
                    rc=1
                    if(diag): print 'III tracker test 111111'

                # -- prevlasttau and curlasttau are the same and <= maxtauTC
                #
                if( (prevlasttau == curlasttau) and (curlasttau <= self.maxtauTC or curlasttau <= self.maxtauModel) ):
                    rc=1
                    if(diag): print 'III tracker test 222222'

                # -- run tracker prevlasttau is < curlasttau and maxtauTC
                #
                if( (prevlasttau < curlasttau) and ( (curlasttau <= self.maxtauTC) or (curlasttau < self.maxtauModel) ) ):
                    rc=0
                    if(diag): print 'III tracker test 333333333333333333333333333 rc=0'



        # !!!!!!!!!!!!!!!!!!!! not doing -T yet in ew2 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #
        
        if(runtrkmode == 'trackeronly' and len(trackeronlystates) > 0):
            
            (latesttrkpath,latestlentrkpath,latestgenpath,latestlengenpath)=trackeronlystates[-1]

            for tstate in trackeronlystates:

                (curtrkpath,curlentrkpath,curgenpath,curlengenpath)=tstate

                # -- case of no tcs
                #
                if(self.ntcs == 0):
                    rc=-999
                    if(diag): print 'IIIOOO tracker test 111111'
                
                # -- prevlasttau and curlasttau are the same and <= maxtauTC
                #
                if( (prevlasttau == curlasttau) and (curlasttau <= self.maxtauTC or curlasttau <= self.maxtauModel) ):
                    rc=1
                    if(diag): print 'IIOOO tracker test 222222'

                # -- run tracker prevlasttau is < curlasttau and maxtauTC
                #
                if( (prevlasttau < curlasttau) and ( (curlasttau <= self.maxtauTC) or (curlasttau < self.maxtauModel) ) ):
                    rc=0
                    if(diag): print 'IIIOOO tracker test 333333333333333333333333333 rc=0'

            if(lentrkpath < 0 or override): rc=0

            print 'rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr ',override,rc




        # NNNNNNNNNNNNNNNNNNNNNNNNNNNN no previous runs
        # check whether we should run...  rc=-999 (no checking)
        #
        if(len(trackerstates) == 0 and runtrkmode == 'tracker'):
            latesttrkpath=None
            lentrkpath=-999
            latestgenpath=None
            lengenpath=-999

            if(lasttau >= self.mintauTC and (lasttau <= self.maxtauTC or lasttau <= self.maxtauModel) ): rc=0
            elif( (self.maxtauModel <= self.mintauTC) and (lasttau == self.maxtauModel) ): rc=0
                
        if(len(trackeronlystates) == 0 and runtrkmode == 'trackeronly'):
            latesttrkpath=None
            lentrkpath=-999
            latestgenpath=None
            lengenpath=-999

            if(lasttau >= self.mintauTC and (lasttau <= self.maxtauTC or lasttau <= self.maxtauModel) and self.ntcs > 0 ): rc=0



        if(diag):
            print 'III  chkTrkStatus:   runtrkmode: ',runtrkmode,' nruns: ',nruns,' ntrkruns: ',ntrkruns,' ntrkonlyruns: ',ntrkonlyruns,' nTTTTcs: ',self.ntcs
            print 'III  chkTrkStatus:   lasttau: ',lasttau,' curlasttau: ',curlasttau,' maxtauModel: ',self.maxtauModel,' mintauTC: ',self.mintauTC,' maxtauTC: ',self.maxtauTC
            print 'III latesttrkpath: ',latesttrkpath,'len: ',lentrkpath
            print 'III latestgenpath: ',latestgenpath,'len: ',lengenpath
            print 'III latesttrkmode: ',latesttrkmode
            print 'III       trkmode: ',self.trkmode
            print 'III            rc: ',rc
            
        if(rc == 1):
            print 'FFF  chkTrkStatus:   rc: ',rc,' if rc==1, already done'

        if(rc == 0):
            print 'III open all rockets, open them ALL the WAY!'


        return(rc)


    def doTrk(self,
              dotrkonly=0,
              dogenonly=0,
              ropt='',
              doClean=1,
              override=0,
              dowindow=0,
              dolsonly=0,
              dupchk=0,  # -- do both NN and 9X version
              gaopt='-g 1024x768',
              do2ga=1,
              TToverride=0,
              GRIBoverride=0,
              GENoverride=0,
              chkGenBasin=1,
              quiet=0,
              ):

        MF.sTimer(tag='trkchk')
        
        self.startga=0

        if(override == 1 and GRIBoverride == 0): self.startga=1


        try:
            TT1=self.getPyp(unlink=0)
        except:
            print 'WWW -- problem in doTrk.getPyp(unlink=0)'
            TT1=None
            
        if(TT1 == None or TToverride):
            if(not(dolsonly)): print '1111111111111111111111111111111111111 making first instance of TmTrk for: ',self.dtg,self.model,self.tdir
            print 'got from instantiation...'
            TT=self
        else:
            print 'got from pyp.............'
            TT=TT1
            if(hasattr(self,'prevtaus')):   TT.prevtaus=self.prevtaus
            if(not(hasattr(TT,'ctlpath'))):   TT.ctlpath=self.ctlpath
            TT.taus=self.taus
            TT.maxtauModel=self.maxtauModel


        # ----------------------- check for remake from TmTrkGen

        if(hasattr(self,'remake')):
            if(self.remake):   TT=self

        trkmode='tracker'
        if(dotrkonly): trkmode='trackeronly'

        TT.trkmode=trkmode

        if(not(hasattr(TT,'tcD'))):
            from tcCL import TcData
            if(self.verb): MF.sTimer(tag='maketcD')
            tcD=TcData(dtgopt=self.dtg,verb=self.verb)
            TT.tcD=tcD
            if(self.verb): MF.dTimer(tag='maketcD')


        # -- get tcV for this dtg
        #
        TT.tcV=TT.tcD.getTCvDtg(self.dtg,dupchk=dupchk)
        
        TT.allreadydone=-1

        # -- now that we've setup the TT object, return if dols
        #
        if(dolsonly):
            if(self.verb): print 'III return TT for dolsonly=1 now that TT is decorated'
            return(TT)
            
        
        # -- make sure there are taus ...
        #
        if(len(TT.taus) == 0):
            print 'WWW(TCtrk) no taus; return TT'
            return(TT)

        #  ***************  make sure .ctl there... before running
        #
        if(MF.ChkPath(TT.ctlpath) ==  0):
            print 'WWW(TCtrk) data file: ',TT.ctlpath,' not there, return'
            return(TT)


        # -- now check trk status cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
        #
        #MF.sTimer(tag='chktrk')
        rc=TT.chkTrkStatus(override=override)
        #MF.dTimer(tag='chktrk')

        #if((rc == 1  or rc == -999) and not(override)):
        # -- 20111028 -- changed for mftrkN
        if((rc == 1) and not(override) and not(dogenonly)):
            TT.allreadydone=1
            return(TT)

        #MF.dTimer(tag='dotrkchk')

        # -- don't seem to need now for tmtrkN
        #if(rc == -999 and dotrkonly):
        #    print 'WWW(TCtrk) trying to run trackeronly with NO tcs, sayooonara'
        #    return(TT)

        try:      TT.trkmodes.append(trkmode)
        except:   TT.trkmodes=[] ; TT.trkmodes.append(trkmode)


        # -- target dirs
        TT.topath="%s/tmtrk"%(TT.tdir)
        
        TT.grbpath="%s.grb"%(TT.topath)
        TT.grbixpath="%s.grb.ix"%(TT.topath)
        TT.grbctlpath="%s.grb.ctl"%(TT.topath)
        TT.grbgmppath="%s.grb.gmp"%(TT.topath)

        TT.grb10path="%s.1p0deg.grb"%(TT.topath)
        TT.grbix10path="%s.grb.1p0deg.ix"%(TT.topath)
        TT.grbctl10path="%s.grb.1p0deg.ctl"%(TT.topath)
        TT.grbgmp10path="%s.grb.1p0deg.gmp"%(TT.topath)

        omodel=TT.model
        if(self.atcfname != None): omodel=self.atcfname
        omodel=omodel.lower()

        otctrkpath="%s/tctrk.atcf.%s.%s.txt"%(TT.tdirAdeck,TT.dtg,omodel)
        otctrksinkpath="%s/tctrk.sink.%s.%s.txt"%(TT.tdirAdeck,TT.dtg,omodel)

        otcgenpath="%s/tcgen.atcf.lant.%s.%s.txt"%(TT.tdirAdeck,TT.dtg,omodel)
        otcgensinkpath="%s/tctrk.sink.lant.%s.%s.txt"%(TT.tdirAdeck,TT.dtg,omodel)

        # -- lists with state of taus/output files
        #
        try:      TT.otctrkpaths.append(otctrkpath)
        except:   TT.otctrkpaths=[] ; TT.otctrkpaths.append(otctrkpath)

        try:      TT.otcgenpaths.append(otcgenpath)
        except:   TT.otcgenpaths=[] ; TT.otcgenpaths.append(otcgenpath)

        TT.prevtaus=TT.taus

        # ----- change to tdir, so can run mulitply instances
        #
        MF.ChangeDir(TT.tdir)

        # -- start timer
        #
        MF.sTimer(tag='all')

        # --- start grads
        #
        genTest=(not(os.path.exists(TT.grb10path)) )
        detTest=(not(os.path.exists(TT.grbpath)) )

        if( ((ropt != 'norun' and self.startga == 0) and detTest) or GRIBoverride):
            print 'sssssssssssssssssssssssssss1111111111111111111111111 '
            ga=setGA(Opts=gaopt,Quiet=quiet,Window=dowindow,Bin=self.xgrads,verb=self.verb)
            ga.fh=ga.open(TT.ctlpath)
            ge=ga.ge

            if(do2ga):
                print 'sssssssssssssssssssssssssss2222222222222222222222222 '
                ga2=setGA(Opts=gaopt,Quiet=quiet,Window=dowindow,Bin=self.xgrads,verb=self.verb)
                ga2.fh=ga2.open(TT.ctlpath)
                ge2=ga2.ge

            self.startga=1

        #--- use gradslats class to make grib input
        # -- 20111030 -- use try;except -- start
        #
        if( (genTest and not(dotrkonly) ) or GRIBoverride):
            
            try:
                ga.fh=ga.open(TT.ctlpath)
            except:
                print 'eeeeeeeeeeeeeeeeeeee11111111111111111111111 '
                ga=setGA(Opts=gaopt,Quiet=quiet,Window=dowindow,Bin=self.xgrads,verb=self.verb)
                ga.fh=ga.open(TT.ctlpath)
                
            ge=ga.ge

            if(do2ga):
                try:
                    ga2.fh=ga2.open(TT.ctlpath)
                except:
                    print 'eeeeeeeeeeeeeeeeeeee22222222222222222222222 '
                    ga2=setGA(Opts=gaopt,Quiet=quiet,Window=dowindow,Bin=self.xgrads,verb=self.verb)
                    ga2.fh=ga2.open(TT.ctlpath)
                ge2=ga2.ge


            else:
                ga2=ga
                ge2=ge

            self.startga=1
            


        # --- set up tcvitals and tracker i/o paths -- cp tcvitals do not ln ...
        #
        
        haveTcs=1

        if(not(hasattr(TT,'tcVcards'))):
            TT.tcVcards=TT.tcV.makeTCvCards(override=override,filename='tcvitals',verb=1,writefile=1)
            TT.tcvpath=TT.tcV.tcvpath

            if(TT.tcvpath != None and os.path.exists(TT.tcvpath)):
                cmd="cp %s fort.12"%(TT.tcvpath)
                MF.runcmd(cmd,ropt)
            else:
                print 'WWW(TCtrk) no tcvitals for ',TT.dtg,' in: ',TT.tcvpath
                haveTcs=0
        else:
            if(len(TT.tcVcards) == 0):
                haveTcs=0
            else:
                haveTcs=1

        TT.haveTcs=haveTcs

        dotracker=0
        if(not(dotrkonly) or dogenonly):
            # --- 1.0 deg data for tcgen
            #
            MF.sTimer('latstcgen')
            if(not(os.path.exists(TT.grb10path)) or GRIBoverride):
                TT.gribArea='areaGen'
                rc=TT.gribInput2TmTrk(ga,ge,TT.dtg,TT.model,TT.taus,TT.grb10path,regrid=TT.regridGen,smth2d=0)
            MF.dTimer('latstcgen')
            dotracker=1

        # --- full res data for tracker mode
        #
        if(haveTcs and not(dogenonly)):
            MF.sTimer('latstctrk')
            if(not(os.path.exists(TT.grbpath)) or GRIBoverride):
                TT.gribArea='area'
                rc=TT.gribInput2TmTrk(ga2,ge2,TT.dtg,TT.model,TT.taus,TT.grbpath,regrid=TT.regridTracker,dotrkonly=dotrkonly)
            MF.dTimer('latstctrk')
            dotracker=1

        # -- correct psl/uas/vas for cgd6 from CMC archivde
        #
        if(self.model == 'cgd6'):
            TT.wgribFilter4Cgd6(override=override,verb=self.verb)

        # -- check if running just trackery...
        #
        if(not(dotracker) and dotrkonly):
            print 'WWW: dotrkonly=1 and haveTcs=0; sayoonara'
            return(TT)


        if( (not(os.path.exists(TT.grbix10path)) or override) and not(dotrkonly) or dogenonly):
            cmd="time %s/grbindex.x %s %s"%(TT.prcdir,TT.grb10path,TT.grbix10path)
            MF.runcmd(cmd,ropt)
            
        if( (not(os.path.exists(TT.grbixpath))  or override) and not(dogenonly) ):
            cmd="time %s/grbindex.x %s %s"%(TT.prcdir,TT.grbpath,TT.grbixpath)
            MF.runcmd(cmd,ropt)
        
        # --- make fcst_minutes for both tracker and tcgen mode
        #
        ifcmin='./fcst_minutes'
        fcmin=TT.makeFcst_minutes()
        MF.WriteCtl(fcmin,ifcmin)
        
        if(os.path.exists(ifcmin)):
            cmd="ln -f -s %s fort.15"%(ifcmin)
            MF.runcmd(cmd,ropt)

        # -- set stdout output file
        #
        ofile='stdout'
        ofile='/dev/null'


        # --- only run tracker if there are TCs...
        #
        if(haveTcs and not(dogenonly) ):

            if(os.path.exists(TT.grbpath)):
                cmd="ln -f -s %s fort.11"%(TT.grbpath)
                MF.runcmd(cmd,ropt)

            if(os.path.exists(TT.grbixpath)):
                cmd="ln -f -s %s fort.31"%(TT.grbixpath)
                MF.runcmd(cmd,ropt)


            # --- make namelist for tracker mode
            #
            nltctrk='namelist.tctrk'
            namelist=self.makeNamelist(trkmode)
            MF.WriteCtl(namelist,nltctrk)

            if(hasattr(TT,'tcVcards')):
                tcvits=TT.tcVcards
                tcvits=tcvits.split('\n')
            else:
                tcvits=open(TT.tcvpath).readlines()
            
            try:     os.unlink(otctrkpath)
            except:  cmd="touch %s"%(otctrkpath); mf.runcmd(cmd,ropt)

            try:     os.unlink(otctrksinkpath)
            except:  cmd="touch %s"%(otctrksinkpath); mf.runcmd(cmd,ropt)

            # -- cycle by storms, in case one fails...
            #
            for tcvit in tcvits:
                if(len(tcvit) == 0): continue
                stm3id=tcvit.split()[1]
                stmpath="fort.12.%s"%(stm3id)
                MF.WriteString2File(tcvit,stmpath)

                omodel=TT.model
                if(self.atcfname != None): omodel=self.atcfname
                omodel=omodel.lower()
                
                otctrkpathSTM="tctrk.atcf.%s.%s.%s.txt"%(TT.dtg,omodel,stm3id.lower())
                otctrksinkpathSTM="tctrk.sink.%s.%s.%s.txt"%(TT.dtg,omodel,stm3id.lower())
                
                ofile="stdout.tctrk.%s.%s.%s.txt"%(TT.dtg,omodel,stm3id.lower())
            
                cmd="ln -f -s %s fort.12"%(stmpath)
                MF.runcmd(cmd,ropt)
                cmd="ln -f -s %s fort.64"%(otctrkpathSTM)
                MF.runcmd(cmd,ropt)
                cmd="ln -f -s %s fort.68"%(otctrksinkpathSTM)
                MF.runcmd(cmd,ropt)
                
                # --- run tracker mode -- use full res data
                #
                tag="tctrk %s"%(stm3id)
                MF.sTimer(tag)
                cmd="time %s/%s < %s > %s"%(TT.prcdir,TT.trkApp,nltctrk,ofile)
                MF.runcmd(cmd,ropt)
                MF.dTimer(tag)

                cmd="cat %s >> %s"%(otctrkpathSTM,otctrkpath)
                mf.runcmd(cmd,ropt)
                
                cmd="cat %s >> %s"%(otctrksinkpathSTM,otctrksinkpath)
                mf.runcmd(cmd,ropt)
                

        # --- run tcgen mode -- always use 1.0 deg data -- by areas
        #
        if(os.path.exists(TT.grb10path)):
            cmd="ln -f -s %s fort.11"%(TT.grb10path)
            MF.runcmd(cmd,ropt)

        if(os.path.exists(TT.grbix10path)):
            cmd="ln -f -s %s fort.31"%(TT.grbix10path)
            MF.runcmd(cmd,ropt)

        if(not(dotrkonly) or dogenonly):

            trkmode='tcgen'
                
            # cycle by basins
            #
            didGenesis=0
            for basin in tcgenBasins:

                # -- make all tcvitals here, in case we want to do tcvitals by basin
                #
                try:     os.unlink('fort.12')
                except:  None

                if(haveTcs):
                    if(hasattr(TT,'tcVcards')):
                        MF.WriteString2File(TT.tcVcards,'fort.12')
                    else:
                        TT.tcV.makeTCvCards(override=override,filename='tcvitals',verb=1,writefile=1)
                        cmd="cp %s fort.12"%(TT.tcV.tcvpath)
                        MF.runcmd(cmd,ropt)

                    
                MF.sTimer(tag=basin)

                omodel=TT.model
                if(self.atcfname != None): omodel=self.atcfname
                omodel=omodel.lower()
                otcgenpath="%s/tcgen.atcf.%s.%s.%s.txt"%(TT.tdirAdeck,basin,TT.dtg,omodel)
                otcgensinkpath="%s/tcgen.sink.%s.%s.%s.txt"%(TT.tdirAdeck,basin,TT.dtg,omodel)
                ofile="%s/stdout.tcgen.%s.%s.%s.txt"%(TT.tdirAdeck,basin,TT.dtg,omodel)
                
                if( (chkGenBasin and not(MF.ChkPath(otcgenpath))) or GENoverride):
                    nltcgen='namelist.tcgen.%s'%(basin)
                    namelist=self.makeNamelist(trkmode,basin)
                    MF.WriteCtl(namelist,nltcgen)

                    # run in tcgen mode
                    #
                    cmd="ln -f -s %s fort.64"%(otcgenpath)
                    MF.runcmd(cmd,ropt)
                    cmd="ln -f -s %s fort.68"%(otcgensinkpath)
                    MF.runcmd(cmd,ropt)

                    cmd="time %s/%s < %s > %s"%(TT.prcdir,TT.trkApp,nltcgen,ofile)
                    MF.runcmd(cmd,ropt)

                    sizgen=MF.GetPathSiz(otcgenpath)
                    if(sizgen > 0): didGenesis=didGenesis+1
                    
                MF.dTimer(tag=basin)

        
        # --- clean up -- blow away grib files...and fort.??
        #
        if(doClean):
            print 'KKKKKKKKKKKKKKKKKKKKKKKKKKKKK cleaning off tracker files...........'
            files=glob.glob("fort.??*") + \
                   ['fcst_minutes',TT.grbpath,TT.grbixpath,TT.grb10path,TT.grbix10path] + glob.glob("*.pgb*") + \
                   glob.glob("namelist.*") + glob.glob("*.grib?") + glob.glob("*.ctl") + glob.glob("*.gm*")
            
            for file in files:
                try:
                    os.unlink(file)
                except:
                    print """WWW(TCtrk) can't unlink file: """,file


        # -- end timer
        #
        
        MF.dTimer(tag='all')
        if(hasattr(TT,'m2')):    del TT.m2
        if(hasattr(TT,'tcD')):   del TT.tcD
        if(hasattr(TT,'tcD2')):   del TT.tcD2
        if(hasattr(TT,'DSs')):   del TT.DSs
        if(hasattr(TT,'dsL')):   del TT.dsL
        
        TT.putPyp(unlink=0)
        
        TT.allreadydone=0

        # -- quit grads; until we know how to keep the process active between calls...
        #
        try:
            ga.__del__()
        except:
            None

        try:
            ga2.__del__()
        except:
            None

        return(TT)


    


    def makeNamelist(self,trkmode='tracker',basin='global'):

        dtg=self.dtg
        atcfname=self.atcfname
        
        cc=dtg[0:2]
        yy=dtg[2:4]
        mm=dtg[4:6]
        dd=dtg[6:8]
        hh=dtg[8:10]

        (lat1,lat2,lon1,lon2)=getBasinLatLons(basin)
        
        print 'NNNNNNNNNNNnamelist: ',dtg,basin,atcfname,trkmode

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

        # ---- turn off tcstruct
        #
        namelist="""&datein
  inp%%bcc=%s,
  inp%%byy=%s,
  inp%%bmm=%s,
  inp%%bdd=%s,
  inp%%bhh=%s,
  inp%%model=17,
  inp%%lt_units='hours'
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
  trkrinfo%%gridtype='global',
  trkrinfo%%contint=100.0,
  trkrinfo%%out_vit='y'
/
&phaseinfo 
  phaseflag='%s',
  phasescheme='both'
/
&structinfo 
  structflag='n',
  ikeflag='n'
/
"""%(cc,yy,mm,dd,hh,atcfname,dtg,lat1,lat2,lon1,lon2,trkmode,pflag)

        return(namelist)


    def makeFcst_minutes(self):

        for n in range(0,len(self.taus)):
            nn=n+1
            if(n == 0):
                fcmin='''%2d %7d'''%(nn,self.taus[n]*60)
            else:
                fcmin='''%s
%2d %7d'''%(fcmin,nn,self.taus[n]*60)

        return(fcmin)


    def gribInput2TmTrk(self,ga,ge,dtg,model,taus,grbpath,regrid=0,dotrkonly=0,smth2d=0):


        areaObj=None
        if(hasattr(self,'gribArea')):
            if(self.gribArea == 'areaGen' and hasattr(self,'areaGen')):
                areaObj=self.areaGen
                self.setReargs(areaObj)

        if(hasattr(self,'gribArea')):
            if(self.gribArea == 'area' and hasattr(self,'area')):
                areaObj=self.area
                self.setReargs(areaObj)
            

        latS=latN=lonW=lonE=None
        if(areaObj != None):
            latS=areaObj.latS
            latN=areaObj.latN
            lonW=areaObj.lonW
            lonE=areaObj.lonE


        (topath,ext)=os.path.splitext(grbpath)

        reargs=None
        if(hasattr(self,'reargs')): reargs=self.reargs


        # -- make galats object
        #
        gl=GaLatsQ(ga,ge,
                   dtg=dtg,model=model,taus=taus,
                   regrid=regrid,
                   reargs=reargs,
                   smth2d=smth2d,
                   )

        gl.create(topath)
        gl.basetime(dtg)
        gl.grid(areaObj)

        uavars=[]
        
        # -- don't really want to do this...latest tracker uses all levels/fields to do phase space even if only tracking
        # -- consistent with TmTrkSimple class
        #
        if(dotrkonly == 999):
            #uavars.append(('ua','instant',[850,700,500]))
            #uavars.append(('va','instant',[850,700,500]))
            #uavars.append(('zg','instant',[850,700]))

            
            uavars.append(('ua','instant',[850,700]))
            uavars.append(('va','instant',[850,700]))
            uavars.append(('zg','instant',[850,700]))

        else:
            uavars.append(('ua','instant',[850,700,500]))
            uavars.append(('va','instant',[850,700,500]))
            if(hasattr(self,'m2') and hasattr(self.m2,'modelZgVar')):
                zgexpr=self.m2.modelZgVar
                uavars.append(('zg','instant',[900,850,800,750,700,650,600,550,500,450,400,350,300],'%s'%(zgexpr)))
            else:
                uavars.append(('zg','instant',[900,850,800,750,700,650,600,550,500,450,400,350,300]))
            uavars.append(('ta','instant',[401]))

        if(len(uavars) > 0):
            gl.plevdim(uavars)

        gl.plevvars(uavars)

        svars=[]
        docgd6sfcvars=1
        # -- expressions for setting psl and uas from 1000 mb fields -- hypsometric for psl and uas = ua(lev=1000)
        #
        if(model == 'cgd6' and docgd6sfcvars):
            svars.append(('psl','instant'))
            svars.append(('uas','instant'))
            svars.append(('vas','instant'))
            svars.append(('pslm','instant','(100000.0*exp((9.80*zg(lev=1000))/(287.04*ta(lev=1000))))'))
            svars.append(('uasm','instant','(ua(lev=1000))'))
            svars.append(('vasm','instant','(va(lev=1000))'))
            print 'CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC cgd6 svars: ',svars
        else:
            svars.append(('psl','instant'))
            svars.append(('uas','instant'))
            svars.append(('vas','instant'))

        gl.sfcvars(svars)

        gl.outvars(svars,uavars)
        gl.close()

        rc=0

        return(rc)

    def cpTrackers2AdeckDir(self):

        if(hasattr(self,'tdirAdeck')):
            sdir=self.tdirAdeck
        else:
            sdir=self.tdir
        tdir="%s/%s/%s/%s"%(AdeckBaseDir,self.trackerName,self.dtg[0:4],self.dtg)
        MF.ChkDir(tdir,'mk')
        cmd="cp -v %s/%s %s/."%(sdir,self.trackerAdmask,tdir)
        mf.runcmd(cmd)

        if(MF.ChkPath("%s/fort.12"%(sdir))):
            cmd="cp -v %s/fort.12 %s/tcvitals.%s.txt"%(sdir,tdir,self.dtg)
            mf.runcmd(cmd)
            
        return
        


class TmTrkChk(TmTrk):

    def __init__(self,
                 dtg,
                 model,
                 tdir,
                 maxtauModel=168,
                 mintauTC=120,
                 maxtauTC=168,
                 verb=0,
                 domdeck=0,
                 ):

        self.dtg=dtg
        self.model=model
        self.tdir=tdir

        self.mintauTC=mintauTC
        self.maxtauTC=maxtauTC
        self.maxtauModel=maxtauModel

        self.verb=0

        self.prcdir="%s/tctrk"%(os.getenv("W2_PRC_DIR"))
        self.pyppath="%s/Pstate.pyp"%(tdir)

        self.initCurState()    # from MFbase

        



    
class TmTrkGen(TmTrk):



    def __init__(self,
                 tcD,
                 dtg,
                 model,
                 basin,
                 gentau=None,
                 maxtauModel=168,
                 mintauTC=120,
                 maxtauTC=168,
                 override=0,
                 trkmode='tracker',
                 verb=0,
                 quiet=1,
                 diag=1,
                 letRemake=0,
                 xgrads='grads',
                 ):


        if(not(w2.onWjet) and w2.onKishou):
            MF.ChkDir(tcgenW3DatDir,'mk')

            
        if(diag): MF.sTimer(tag='TmTrkGenall')
        import FM


        bdtg=dtg
        if(gentau != None):
            self.gentau=gentau
            bdtg=mf.dtginc(dtg,-gentau)


        if(diag):MF.sTimer(tag='TmTrkGen')
        if(model in (FM.wjetmodels + FM.taccmodels) ):
            FR=FM.getFRlocal(model,bdtg)
            ctlpath=FR.ctlpath
            w2rc=0

        else:
            FR=FM.FimRunModel2Short(model,bdtg,verb=verb,override=override)

            # -- reduce # of taus
            #
            rc=w2.getW2fldsRtfimCtlpath(model,bdtg,maxtau=maxtauModel)
            (w2rc,w2ctlpath,w2taus,w2gribtype,w2gribver,datpaths,nfields,tauOffset)=rc

            if(FR.tdatathere == 0 and w2rc == 0):
                ctlpath=None
                maxtauModel=None
            elif(w2rc):
                ctlpath=w2ctlpath
                maxtauModel=FR.m2.setMaxtau(bdtg)
                (tdir,file)=os.path.split(ctlpath)
            elif(FR.tdatathere):
                ctlpath=FR.ctlpathM2
                maxtauModel=FR.m2.setMaxtau(bdtg)
                
        if(diag): MF.dTimer(tag='TmTrkGen')

        year=dtg[0:4]
        atcfname=model.upper()

        if(w2rc == 0):
            if(not(hasattr(FR,'tOutDir'))):
                tdir=FR.tDir
            else:
                tdir=FR.tOutDir
            
        tdir="%s/tctrk"%(tdir)
        tdirAdeck="%s/esrl/%s/w2flds"%(AdeckBaseDir,year)
        MF.ChkDir(tdir,'nomk')
        MF.ChkDir(tdirAdeck,'nomk')

        if(ctlpath != None and w2rc == 0):
            FR.LsGrib(lsopt=0)
            taus=FR.tdattausData
        elif(w2rc):
            taus=w2taus
        else:
            taus=[]

        if(verb):
            print '      w2rc: ',w2rc  
            print '   ctlpath: ',ctlpath
            print '      tdir: ',tdir
            print ' tdirAdeck: ',tdirAdeck
            print '      taus: ',taus

        self.dtg=dtg

        # -- bdtg is the base/beginning dtg from which all +tau calcs are made
        self.bdtg=bdtg
        # -- bdtg is the base/beginning dtg from which all +tau calcs are made

        self.model=model
        self.atcfname=atcfname
        self.tdir=tdir
        self.tdirAdeck=tdirAdeck
        self.taus=taus
        self.quiet=quiet
        
        self.ctlpath=ctlpath

        self.mintauTC=mintauTC
        self.maxtauTC=maxtauTC
        self.maxtauModel=maxtauModel
        self.doga2=0
        self.xgrads=xgrads

        self.verb=0


        self.prcdir="%s/tctrk"%(os.getenv("W2_PRC_DIR"))
        self.pyppathTctrk="%s/Pstate.pyp"%(tdir)
        if(gentau != None):
            self.pyppathTcgen="%s/Pstate.tcgen.%s.t%03d.pyp"%(tdir,basin,gentau)
        else:
            self.pyppathTcgen="%s/Pstate.tcgen.%s.pyp"%(tdir,basin)

        # -- get TT (TmTrk)
        self.TT=self.getPyp(pyppath=self.pyppathTctrk)

        # -- if diff between ctlpath in pyp in ctlpath from W2.getW2fldsRtfimCtlpath()
        # remake TT (TmTrk()) from scratch and set remake=1

        if(not(MF.ChkPath(ctlpath))):
            self.datathere=0
            return

        doremake=0
        if(self.TT == None):
            doremake=1
            TTctlpath=None
        elif(not(hasattr(self.TT,'ctlpath'))):
            TTctlpath=None
            doremake=1
        elif(hasattr(self.TT,'ctlpath') and (self.TT.ctlpath != ctlpath) and letRemake):
            TTctlpath=self.TT.ctlpath
            doremake=1
        elif(ctlpath == None):
            self.datathere=0
            return


        
        # -- if we made it this far, there is data so set it

        self.datathere=1

        if(doremake):
            print 'WWW(TmTrkGen) difference between general ctlpath and one in the pyp; remake'
            print 'WWW(TmTrkGen) self.TT.ctlpath: ',TTctlpath
            print 'WWW(TmTrkGen)         ctlpath: ',ctlpath
                
            self.TT=TmTrk(bdtg,self.model,self.atcfname,self.tdir,self.tdirAdeck,
                     self.taus,self.maxtauModel,self.ctlpath,tcD=tcD)
            self.TT.remake=1

        else:
            self.TT.remake=0
            
        self.initCurState() # from MFbase
        self.trkmode=trkmode
        self.tcD=tcD

        if(diag): MF.dTimer(tag='TmTrkGenall')



    def setw2Plot(self,ga,parea,vdtg,gentau,
                  dobm=1,
                  xsize=None,
                  override=0,
                  ):


        aspect=w2.W2plotAspect
        if(xsize == None):
            self.xsize=w2.W2plotXsize
        else:
            self.xsize=xsize
        self.ysize=int(self.xsize*aspect)

        ge=ga.ge

            
        self.gentau=gentau
        aW2=getW2Area(parea)
        self.aW2=aW2

        ge.timelab='on'
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

        bm=ga.gp.basemap2
        bm.set(xsize=self.xsize,ysize=self.ysize,
               bmdir=tcgenW3DatDir,
               bmname='%s'%(self.basin),
               )
        if(dobm):
            if(self.pngmethod == 'printim'):
                if(not(MF.ChkPath(bm.pngpath)) or override):
                    print 'MMMMMMMMMMMMMMMMM making:',bm.pngpath,override
                    bm.draw()
                    bm.putPng()
                self.bmpngpath=bm.pngpath
            elif(self.pngmethod == 'gxyat'):
                bm.draw()

        ge.setPlotScale()
        ge.setTimebyDtg(vdtg)



    def w2PlotPrp(self):


        prvar=None
        if(hasattr(self.m2,'setprvar')):
            prvar=self.m2.setprvar(self.dtg,self.gentau)
        else:
            prvar=self.m2.modelprvar

        if(prvar != None):
            prvar=prvar.split('=')[1]
            prvar=prvar.replace("'","")

        pslvar=None

        if(hasattr(self.m2,'setpslvar')):
            pslvar=self.m2.setpslvar(self.dtg)
        else:
            pslvar=self.m2.modelpslvar

        gs="""
set clevs   1  2  4  8  16  32 64 128
set gxout shaded
set csmooth on
set cterp on
set rgb 98 185 255 00 50
set ccols 0 39 37 36 98 22 24 26 61
set ccols 0 59 58 57 55 53 75 73 71
set csmooth on
set cterp on
d %s
pm=const(maskout(const(lat,-1),abs(lat)-30),0,-u)
pmt=const(maskout(const(lat,-1),abs(lat)-15),0,-u)
"""%(prvar)

        self.ga(gs)

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


        self.ga(gs)

        cb=self.gp.cbarn
        cb.draw(vert=0,sf=0.75)



    def w2PlotNhc850vort(self):


        pslvar=None

        if(hasattr(self.m2,'setpslvar')):
            pslvar=self.m2.setpslvar(self.dtg)
        else:
            pslvar=self.m2.modelpslvar

        plev1=850
        plev2=200

        self.ge.setColorTable(table='jaecol.gsf')

        gs="""
z5=zg(lev=500)

u8=ua(lev=%d)
v8=va(lev=%d)
rvrt8=hcurl(u8,v8)*1e5

u2=ua(lev=%d)
v2=va(lev=%d)

cf=lat/abs(lat)
cf=const(cf,1,-u)

u8=u8*%f
v8=v8*%f
u2=u2*%f
v2=v2*%f

"""%(plev1,plev1,plev2,plev2,ms2knots,ms2knots,ms2knots,ms2knots)

        uvskip=8
        v2e1='maskout(maskout(u2trop,w2-10),20-w2);skip(v2,%d)'%(uvskip)
        v2em='maskout(maskout(u2trop,w2-20),40-w2);skip(v2,%d)'%(uvskip)
        v2e2='maskout(maskout(u2trop,w2-40),100-w2);skip(v2,%d)'%(uvskip)
        
        gs=gs+"""

set gxout shaded
set csmooth on
set clevs   4   6    8    10    12    14   16  18    20
set ccols 0   39  37   35    22   24    26   27   28   6

d rvrt8
"""

        self.ga(gs)
        self.ge.getShades()

        cb=self.gp.cbarn
        cb.draw(vert=0,sf=0.75)

        gs="""

u2=re(u2,0.5)
v2=re(v2,0.5)

w2=mag(u2,v2)
latr=re(lat,0.5)
u2trop=maskout(u2,30.0-abs(latr))
#u2trop=u2

ds2=0.04

set gxout barb
set cthick 20
set ccolor 0
set digsiz 0.05
d %s

set cthick 5
set ccolor 3
set digsiz 0.04
d %s

set cthick 20
set ccolor 0
set digsiz 0.05
d %s

set cthick 5
set ccolor 1
set digsiz 0.04
d %s

set cthick 20
set ccolor 0
set digsiz 0.05
d %s

set cthick 5
set ccolor 2
set digsiz 0.04
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
d maskout(z5,abs(30)-lat))


"""%(v2e1,v2e1,v2em,v2em,v2e2,v2e2)


        self.ga(gs)




    def lsTcGen(self,
                gentau=72,
                basin=None,
                doland=0,
                lfmax=0.50,
                verb=0,
                ):


        tcgstats=None
        if(hasattr(self,'alltcgencards')):
            tcgcards=self.alltcgencards
            try:      tcgstats=tcgcards[basin,gentau]
            except:   None 
        else:
            print 'WWWW no alltcgencards'

        tcgfastats=None
        if(hasattr(self,'tcgenfldanlcards')):
            tcgfacards=self.tcgenfldanlcards
            try:     tcgfastats=tcgfacards[basin,gentau]
            except:  None  
        else:
            print 'WWWW no tcgenfldanalcards'

        if(tcgstats != None and verb):
            for card in tcgstats:
                print '  tcgstats: ',card
            
        if(tcgfastats != None and verb):
            for card in tcgfastats:
                print 'tcgfaststs: ',card
                
    
        rc=self.getTcGenProps(basin,gentau,verb=verb)

        if(rc == None):
            print 'WWW(lsTcGen): no data for dtg: ',self.dtg,' model: ',self.model,' basin: ',basin,' gentau: ',gentau
            return
        
        (opr,oprc,orc2t,
         actStmids,
         actHitGtcs,genHitGtcs,genGtcs,
         nGenTc,nGenHit,
         pr,prc,rc2t,
         nNo,genNOGtcs,sumStdd,
         cards,
         )=rc

        #for card in cards:
        #    print card

        print "%s %7s %-4s %03d  %s"%(self.dtg,self.model,basin,gentau,opr),'nNo: ',nNo,'genNOGtcs: ',genNOGtcs,'sumStdd: ',sumStdd
        if(nGenTc > 0): print 'nGenTc(OBS): ',nGenTc,genGtcs,' nGenHit(MODEL)wo: ',nGenHit,genHitGtcs

        return


    

    def getTcGenPropsOld(self,basin,gentau,
                         itcgcards=None,
                         warn=0,
                         verb=1):

        prc=pr=rc2t=None
        actHitGtcs=[]
        genHitGtcs={}
        actStmids=[]
        genGtcs={}
        genNOGtcs={}

        sumStdd=0.0
        
        cards=None
        
        if(hasattr(self,'alltcgencards')):
            tcgcards=self.alltcgencards
            try:
                if(verb): print 'got alltcgencards....... from pyp'
                cards=tcgcards[basin,gentau]
            except:
                cards=None
        else:
            cards=None

        if(hasattr(self,'tcgenfldanlcards')):
            tcgfacards=self.tcgenfldanlcards
            try:
                if(verb): print 'got tcgenfldanlcards.... from pyp'
                facards=tcgfacards[basin,gentau]
            except:
                facards=[]
        else:
            facards=[]
            if(warn): print 'WWWW no tcgenfldanalcards'

        if(cards != None):
            cards=cards+facards
        elif(len(facards) > 0):
            cards=facards

        if(itcgcards != None):
            cards=itcgcards

        if(cards == None): return(None)
                   
        if(cards != None):

            for card in cards:
                if(verb): print card
                tt=card.split('|')
                tt0=tt[0].strip()
                if(verb): print 'tt0---------------------------: ',tt0,card
                if(tt0 == 'basinPR'):
                    tt1=tt[1].strip()
                    ttt=tt1.split()
                    prc=float(ttt[1])
                    pr=float(ttt[3])
                    rc2t=float(ttt[5])

                elif(tt0 == 'ACT_HIT'):
                    tt1=tt[1].strip()
                    nActHit=int(tt1)
                    if(nActHit > 0):
                        for n in range(0,nActHit):
                            tt2=tt[2+n].strip()
                            ttt=tt2.split()
                            actHitGtcs.append(ttt[1])

                # -- ssssssssssssssssssssss spuricanes
                #
                elif(tt0 == 'GEN_NO'):
                    tt1=tt[1].strip()
                    nNo=int(tt1)
                    if(nNo > 0):
                        for n in range(0,nNo):
                            tt2=tt[2+n].strip()
                            ttt=tt2.split()
                            std=float(ttt[3])
                            sumStdd=sumStdd+std
                            nofgstmid=ttt[1]
                            nofgstd=ttt[3]
                            nofgage=ttt[5]
                            nofgvmax=ttt[10]
                            genNOGtcs[nofgstmid]=(nofgvmax,nofgage,nofgstd)

                elif(tt0 == 'GEN_HIT'):
                    tt1=tt[1].strip()
                    nGenHit=int(tt1)
                    if(nGenHit > 0):
                        for n in range(0,nGenHit):
                            tt2=tt[2+n].strip()
                            ttt=tt2.split()

#['Gtc:', 'tg0011', 'TC:', '19L.2010', 'D:', '212.8', 'S:', '1.2', 'LL:', '15.9', '275.8', 'V:', '19', 'FgAge:', '6']
                            fgstmid=ttt[1]
                            fgdist=float(ttt[5])
                            fgstd=float(ttt[7])
                            fgvmax=float(ttt[12])
                            fgage=float(ttt[14])
                            genHitGtcs[fgstmid]=(fgvmax,fgage,fgstd,fgdist)


                elif(tt0 == 'GEN_TCs'):
                    tt1=tt[1].strip()
                    nGenTc=int(tt1)
                    if(nGenTc > 0):
                        for n in range(0,nGenTc):
                            tt2=tt[2+n].strip()
                            ttt=tt2.split()
                            gstmid=ttt[1]
                            gvmax=float(ttt[6])
                            gage=float(ttt[8])
                            gstdd=float(ttt[10])

#['TC:', '19L.2010', 'LL:', '16.7', '279.4', 'V:', '35', 'T:', '12', 'S:', '1.2']
                            genGtcs[gstmid]=(gvmax,gage,gstdd)


                elif(tt0 == 'ACT_TCs'):
                    tt1=tt[1].strip()
                    nActTc=int(tt1)
                    if(nActTc > 0):
                        for n in range(0,nActTc):
                            tt2=tt[2+n].strip()
                            ttt=tt2.split()
                            astmid=ttt[1]
                            atcvmax=float(ttt[6])
                            atcage=float(ttt[8])
                            actStmids.append(astmid)


            if(verb): print 'NNNNNNNNNNNNNNN nActTc,nGenTc,nNo,nGenHit,nActHit: ',nActTc,nGenTc,nNo,nGenHit,nActHit




        actStmids=MF.uniq(actStmids)
        
        if(prc != None):  oprc="%4.2f"%(prc)
        else:             oprc='N/A'
            
        if(pr != None):   opr="%4.2f"%(pr)
        else:             opr='N/A'
            
        if(rc2t != None and rc2t > 0.0):  orc2t="%4.2f"%(rc2t)
        else:                             orc2t='N/A'

        if(nNo == 0): sumStdd=-999.
        rc=(opr,oprc,orc2t,
            actStmids,
            actHitGtcs,genHitGtcs,genGtcs,
            nGenTc,nGenHit,
            pr,prc,rc2t,
            nNo,genNOGtcs,sumStdd,
            cards,
            )


        return(rc)



    def getTcGenProps(self,basin,gentau,
                      itcgcards=None,
                      warn=0,
                      verb=1):

        cards=[]
        prc=pr=rc2t=None
        nGenTc=nGenHit=0
        actHitGtcs=[]
        genHitGtcs={}
        actStmids=[]
        genGtcs={}
        genNOGtcs={}

        nNo=0
        sumStdd=0.0
        (rc2t,prc,pr)=self.prList
        
        if(prc != None):  oprc="%4.2f"%(prc)
        else:             oprc='N/A'
            
        if(pr != None):   opr="%4.2f"%(pr)
        else:             opr='N/A'
            
        if(rc2t != None and rc2t > 0.0):  orc2t="%4.2f"%(rc2t)
        else:                             orc2t='N/A'

        if(nNo == 0): sumStdd=-999.

        rc=(opr,oprc,orc2t,
            actStmids,
            actHitGtcs,genHitGtcs,genGtcs,
            nGenTc,nGenHit,
            pr,prc,rc2t,
            nNo,genNOGtcs,sumStdd,
            cards,
            )


        return(rc)


        
    def w2PlotTcGen850(self,parea,gentau=120,
                       dowindow=0,
                       gaopt='-g 1024x768',
                       dostdd=0,
                       doxv=0,
                       pngmethod='printim',
                       fcdtau=24,
                       doland=0,
                       verb=0,
                       diag=0,
                       fcmode='fcst',
                       override=0,
                       xsize=1440,
                       quiet=1,
                       ptype='vrt850',
                       ):


        if(not(gentau in self.taus)):
            print 'WWW tau not available in TCtrk.w2PlotTcGen; sayoonara'
            return

        self.gentau=gentau
        self.verb=verb
        self.doland=doland
        self.pngmethod=pngmethod
        self.diag=diag
        self.fcmode=fcmode
        self.fcdtau=fcdtau
        self.dostdd=dostdd

        # -- setup
        #
        bdtg=self.bdtg
        vdtg=mf.dtginc(bdtg,gentau)
        self.vdtg=vdtg

        model=self.model
        basin=self.basin

        # -- define output
        #
        byear=bdtg[0:4]
        odir='%s/%s/%s'%(tcgenW3DatDir,byear,bdtg)
        MF.ChkDir(odir,'mk')

        opath="%s/%s.%s.%03d.%s.%s.%s.%s.gentracker.png"%(odir,model,vdtg,gentau,basin,parea,ptype,fcmode)
        self.opath=opath

        if( not(override or not(MF.ChkPath(opath))) ):
            print 'III opath: ',opath,' already done...model: ',model,' bdtgs ',bdtg,' vdtg: ',vdtg,' gentau: ',gentau
            return
        elif( override and MF.ChkPath(opath)):
            print 'III override, blow away file if already there -- issue on fat32 drive, not writing if already there and making file 0 size!!!!!!'
            os.unlink(opath)


        # --- open model and set grads env
        #

        if(not(hasattr(self,'ga'))):

            ga=setGA(Opts=gaopt,Quiet=quiet,Window=dowindow,Bin=self.xgrads,verb=verb)
            ga.fh=ga.open(self.ctlpath)
            self.ga=ga
            self.ge=ga.ge

        else:

            ga=self.ga
            ge=self.ge


        self.setw2Plot(ga,parea,vdtg,gentau,xsize=xsize,override=0)


        # -- field plot
        #
        self.w2PlotNhc850vort()

        # -- tracks
        #
        self.w2PlotTcGenTracks()

        # -- title
        #
        self.w2PlotTitle()

        print 'Pnging: ',self.opath

        if(self.doga2):
            ge.makePng(opath,bmpath=self.bmpngpath,xsize=self.xsize,ysize=self.ysize)
        else:
            gs="%s %s -b %s -t 0 x%d y%d png"%(self.pngmethod,opath,self.bmpngpath,self.xsize,self.ysize)
            self.ga(gs)
            

        if(doxv):  os.system("xv %s"%(opath))

        # -- clear if we come back in...
        #

        if(dowindow): ga('q pos')
        ge.clear()

        return


    def w2PlotTcGenPrp(self,tcG,
                       gentau=120,
                       dowindow=0,
                       gaopt='-g 1024x768',
                       dostdd=0,
                       doxv=0,
                       pngmethod='printim',
                       fcdtau=24,
                       doland=0,
                       verb=0,
                       diag=0,
                       fcmode='fcst',
                       override=0,
                       xsize=1440,
                       quiet=1,
                       ptype='prp',
                       ):


        
        self.iV=tcG.iV
        
        self.bdtg=tcG.bdtg
        self.gentau=tcG.gentau
        self.gentype=tcG.gentype
        self.dogendtg=tcG.dogendtg
        self.model=tcG.model
        self.basin=tcG.basin
        self.verb=verb

        vdtg=mf.dtginc(self.bdtg,self.gentau)
        iVdtg=self.bdtg
        if(self.dogendtg):
            iVdtg=vdtg

        self.iVdtg=iVdtg

        self.iVkey=(self.model,iVdtg,self.basin,self.gentau,self.gentype)

        self.iVhash=self.iV.getHash(self.iVkey)

        self.iV.lsHash(self.iVkey,hash=self.iVhash)

        sys.exit()

        self.doland=doland
        self.pngmethod=pngmethod
        self.diag=diag
        self.fcmode=fcmode
        self.fcdtau=fcdtau
        self.dostdd=dostdd

        self.ptype=ptype
        self.fcmode=fcmode
        self.xsize=xsize

        # -- calc vars
        #
        self.vdtg=mf.dtginc(self.bdtg,self.gentau)
        self.parea=TcGenBasin2Area[self.basin]

        # -- define output
        #
        byear=self.bdtg[0:4]
        odir='%s/%s/%s'%(tcgenW3DatDir,byear,self.bdtg)
        MF.ChkDir(odir,'mk')

        opath="%s/%s.%s.%03d.%s.%s.%s.%s.gentracker.png"%(odir,self.model,self.vdtg,self.gentau,self.basin,self.parea,self.ptype,self.fcmode)
        self.opath=opath

        if( not(override or not(MF.ChkPath(opath))) ):
            print 'III opath: ',opath,' already done...model: ',self.model,' bdtgs ',self.bdtg,' vdtg: ',self.vdtg,' gentau: ',self.gentau
            return
        elif( override and MF.ChkPath(opath)):
            print 'III override, blow away file if already there -- issue on fat32 drive, not writing if already there and making file 0 size!!!!!!'
            os.unlink(opath)


        # --- open model and set grads env
        #

        if(not(hasattr(self,'ga'))):
            ga=setGA(Opts=gaopt,Quiet=quiet,Window=dowindow,Bin=self.xgrads,verb=verb)
            ga.fh=ga.open(self.ctlpath)
            ge=ga.ge
            gp=ga.gp
            self.ga=ga
            self.ge=ge
            self.gp=gp

        else:
            ga=self.ga
            ge=self.ga.ge
            gp=self.ga.gp


        self.setw2Plot(ga,self.parea,self.vdtg,self.gentau,xsize=self.xsize,override=0)


        # -- field plot
        #
        self.w2PlotPrp()

        # -- tracks
        #
        self.w2PlotTcGenTracks()

        # -- title
        #
        self.w2PlotTitle()

        print 'Pnging: ',self.opath

        gs="%s %s -b %s -t 0 x%d y%d png"%(self.pngmethod,self.opath,self.bmpngpath,self.xsize,self.ysize)
        print 'gs: ',gs
        self.ga(gs)
            

        if(doxv):  os.system("xv %s"%(self.opath))

        # -- clear if we come back in...
        #

        if(dowindow): ga('q pos')
        ge.clear()

        return



    def w2PlotTitle(self):

        model=self.model
        basin=self.basin
        gentau=self.gentau
        ga=self.ga
        ge=self.ge
        gp=self.gp
        bdtg=self.bdtg
        vdtg=self.vdtg
        dostdd=self.dostdd
    
        rc=self.getTcGenProps(basin,gentau,verb=self.verb)
        if(rc == None):
            print 'III return None from getTcGenProps, bail...model: ',model,' bdtgs ',bdtg,' vdtg: ',vdtg,' gentau: ',gentau
            return
        (opr,oprc,orc2t,
         actStmids,
         actHitGtcs,genHitGtcs,genGtcs,
         nGenTc,nGenHit,
         pr,prc,rc2t,
         nNo,genNOGtcs,sumStdd,
         cards,
         )=rc


        # -- title object
        #
        ttl=gp.title
        ttl.set(scale=1.00)
        
        t1="%s bdtg: %s  `3t`0= %03d [h]  pr: %s [mm/d]  prc2t: %s"%(tcgenModelLabel[model],bdtg,int(gentau),opr,orc2t)
        if(dostdd): t2="valid vdtg: %s :: sTDd [d]"%(vdtg)
        else:       t2="valid vdtg: %s :: Vmax [kt] "%(vdtg)
        t2="%s nGenTc: %1d nGenHit: %1d "%(t2,nGenTc,nGenHit)
        if(nNo > 0):
            t2="%s nNo: %2d stddNo: %4.1f "%(t2,nNo,sumStdd)
        
        ttl.top(t1,t2)



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

        rc=self.getTcGenProps(basin,gentau,verb=verb)
        if(rc == None):
            print 'III return None from getTcGenProps, bail...model: ',model,' bdtgs ',bdtg,' vdtg: ',vdtg,' gentau: ',gentau
            return
        (opr,oprc,orc2t,
         actStmids,
         actHitGtcs,genHitGtcs,genGtcs,
         nGenTc,nGenHit,
         pr,prc,rc2t,
         nNo,genNOGtcs,sumStdd,
         cards,
         )=rc

        if(len(cards) == 0): return

        (fctrks,gctrks,gstds,gtcs,btcs,vbtcs,abtcs)=getFctrkGstdGtcBtcs(self,bdtg,model,basin,gentau,doland=doland)

        if(verb):
            print 'fctrks: ',fctrks.keys(),fctrks
            print 'gctrks: ',gctrks.keys(),gctrks
            print 'gstds:  ',gstds.keys(),gstds
            print 'gtcs:   ',gtcs.keys(),gtcs
            print 'btcs:   ',btcs.keys(),btcs
            print 'vbtcs:  ',vbtcs.keys(),vbtcs
            print 'abtcs:  ',abtcs.keys(),abtcs
            
        # -- get genesis tcs
        #
        
        gbt={}
        gstmids=gtcs.keys()
        gbtstmids=[]
        mcol=2
        for stmid in gstmids:
            gts=self.tcD.getGtLatLonVmax(stmid)
            print gts.keys()
            print gts
            glat=gtcs[stmid][0]
            glon=gtcs[stmid][1]

            if( (glat >= aW2.latS and glat <= aW2.latN) and
                (glon >= aW2.lonW and glon <= aW2.lonE) ):
                gb=GA.plotTcBt(ga,ge,gts,bdtg,nhbak=24,nhfor=gentau,mcol=mcol,ddtg=fcdtau,mcolTD=6)
                gbt[stmid]=gb
                gbtstmids.append(stmid)
                mcol=mcol+1


        # -- plot 24 h of bt:  gentau-24h -> gentau-0h
        #

        pbt={}
        finaly=-999

        gtcol=9

        btmcols=[2,7,3,5]*3
        pbtstmids=[]
        bcol=0
        for stmid in abtcs.keys():

            b1id=stmid[2].lower()
            bts=self.tcD.getBtLatLonVmax(stmid)
            bbb=bts.keys()
            bbb.sort()
            
            try:
                blat=bts[bdtg][0]
                blon=bts[bdtg][1]
            except:
                blat=bts[vdtg][0]
                blon=bts[vdtg][1]

            if( (blat >= self.aW2.latS and blat <= self.aW2.latN) and
                (blon >= self.aW2.lonW and blon <= self.aW2.lonE) ):
                if(self.diag):
                    bbs=bts.keys()
                    bbs.sort()
                    for bt in bbs:
                        print 'bb--',bt,bts[bt]
                        
                pb=GA.plotTcBt(ga,ge,bts,bdtg,nhbak=72,nhfor=gentau,mcol=btmcols[bcol],ddtgfor=fcdtau,ddtgbak=fcdtau,mcolTD=6)
                pbt[stmid]=pb
                pbtstmids.append(stmid)
                bcol=bcol+1


        for stmid in pbtstmids:
            btlgdcol=1
            for gstmid in gstmids:
                if(stmid == gstmid): btlgdcol=gtcol
            otimes=pb.otimesbak[:]+pb.otimesfor[:]
            otimes=MF.uniq(otimes)
            pb=pbt[stmid]
            pb.dline(times=otimes,lcol=7,lthk=10)
            pb.dwxsym(times=otimes)
            if(finaly != -999): pb.finaly=finaly
            pb.legend(ge,times=otimes,bttitle=stmid,btlgdcol=btlgdcol)
            finaly = pb.finaly-pb.dy


        # -- plot the genesis points
        #
        for stmid in gbtstmids:
            gb=gbt[stmid]
            gb.dline(lcol=2,lthk=20)
            gb.dwxsym(times=gb.otimesfor[:],wxcol=1,wxthk=20,wxsiz=0.25)
            gb.dwxsym(times=gb.otimesfor[:],wxcol=gtcol,wxthk=7,wxsiz=0.25)
        

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
            
            mkendcol=fcmkendcol
            mkendcolin=fcmkendcolin
            
            fcs=fctrks[fstmid]
            try:
                fcvmax=fcs[gentau][2]
            except:
                fcvmax=None
            if(fcvmax != None):
                fcdlab="%3.0f"%(float(fcvmax))
            else:
                fcdlab='---'

            # -- for fc doland
            #
            pf=GA.plotTcFt(ga,ge,fcs,dovmaxflg=0,verb=0,doland=1)
            pf.dline(lcol=fclcol)
            pf.dmark(mkcol=mkendcol,mksiz=0.075)
            pf.dmark(mksiz=0.125,mkcol=mkendcol,mksym=3,mkthk=4,times=[gentau])
            pf.dmark(mksiz=0.050,mkcol=mkendcolin,times=[gentau])
            pf.dlabel(times=[gentau],dlab=fcdlab,lbthk=10,lbcol=2)
            #pf.dlabel(times=[gentau],dlab=fcdlab,lbthk=1,lbcol=1)


        # -- plot gcs
        #
        gcs={}

        gstmids=gctrks.keys()
        gstmids.sort()

        for gstmid in gstmids:

            gtype=gstmid[0:2].lower()

            acthit=0
            for actgtc in actHitGtcs:
                if(actgtc == gstmid): acthit=1

            genhit=0
            for gengtc in genHitGtcs:
                if(gengtc == gstmid): genhit=1

            if(gtype != 'tg'):
                mkendcol=fcmkendcol
                mkendcolin=fcmkendcolin
            else:
                mkendcol=gcmkendcol
                mkendcolin=gcmkendcolin

            if(acthit and gtype == 'tg'): mkendcol=3
            if(genhit): mkendcol=9 ; mkendcolin=7
            
            gcs=gctrks[gstmid]
            stdd=gstds[gstmid][0]
            stdd="%4.1f"%(float(stdd))


            pg=GA.plotTcFt(ga,ge,gcs,dovmaxflg=0,verb=0,doland=1)
            pg.dline(lcol=gclcol)
            pg.dmark(mkcol=mkendcol,mksiz=0.075)
            pg.dmark(mksiz=0.125,mkcol=mkendcol,mksym=3,mkthk=4,times=[gentau])
            pg.dmark(mksiz=0.050,mkcol=mkendcolin,times=[gentau])
            pg.dlabel(times=[gentau],dlab=stdd,lbthk=10,lbcol=0)
            pg.dlabel(times=[gentau],dlab=stdd,lbthk=4,lbcol=1)







class TcPrBasin(MFbase):


    def __init__(self,model,basin,bdtg,gentaus=None,prs=None,verb=0):


        self.model=model
        self.bdtg=bdtg
        self.gentaus=gentaus
        self.verb=verb

        year=bdtg[0:4]

        tdir="%s/esrl/%s/w2flds/%s"%(AdeckBaseDir,year,bdtg)
        MF.ChkDir(tdir,'mk')
        
        prpath="%s/prbasin.%s.%s.%s.pyp"%(tdir,basin,bdtg,model)
        self.prpath=prpath

        self.getPrs()


    def putPrs(self):

        if(self.prs != None):
            self.putPyp(self.prs,self.prpath,verb=self.verb)

    def getPrs(self):

        #-- check for case of siz(prpath) = 0...
        #
        if(MF.getPathSiz(self.prpath) > 0):
            prs=self.getPyp(self.prpath,verb=self.verb)
        else:
            prs={}

        self.prs=prs
        
    def getPrsTau(self,tau):

        try:
            pr=self.prs[tau]
        except:
            pr=None
        return(pr)
        





    
#uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu
# unbounded method
#

def getTTpyp(tcD,dtg,model,basin,dogendtg=0,gentau=None,verb=0,quiet=0,diag=0,override=0,
             doga2=0):

    import FM
    
    if(model in (FM.wjetmodels + FM.taccmodels) ):
        FR=FM.getFRlocal(model,dtg)
    elif(model in (FM.m2models + W2.Nwp2ModelsAll) ):
        FR=FM.FimRunModel2Short(model,dtg,verb=verb,override=override)
    else:
        print 'EEE invalid model(getTTpyp): ',model
        sys.exit()


    if(not(dogendtg)): gentau=None
    TT=TmTrkGen(tcD,dtg,model,basin,gentau=gentau,quiet=quiet,diag=diag)
    TT.m2=FR.m2

    datactlpath=TT.ctlpath
    
    bdtg=TT.bdtg

    # make sure data are there...before recovering pyps...
    #
    if(TT.datathere == 0):
        print 'WWW(getTTpyp) no data...ctlpath not there...just return...'
        return(TT)

    
    if(hasattr(TT.TT,'remake')):
        if(TT.TT.remake):
            print 'WWW(getTTpyp) remade TT and TT.TT from scratch...no checking of pyps...and run doTrk()'
            TT.TT.doTrk()
            return(TT)

    if(os.path.exists(TT.pyppathTcgen)):
        if(diag): MF.sTimer(tag='TTallll')
        if(verb): print 'TTTTTTTTTTTTTTTTT there.. ',TT.pyppathTcgen,TT.pyppathTctrk
        if(diag): MF.sTimer(tag='TT1 for TT.pyppathTcgen ')
        TT1=TT.getPyp(pyppath=TT.pyppathTcgen,verb=verb)
        if(diag): MF.dTimer(tag='TT1 for TT.pyppathTcgen ')
        
        # -- check if tcgen bad
        if(TT1 == None):
            TT1=TT

        if(diag): MF.sTimer(tag='TT2 for TT.pyppathTcgen ')
        TT2=TT.getPyp(pyppath=TT.pyppathTctrk)
        if(diag): MF.dTimer(tag='TT2 for TT.pyppathTcgen ')

        TT3=TT1
        TT3.TT=TT2
        TT3.m2=FR.m2
        if(hasattr(TT,'tcD')): TT3.tcD=TT.tcD
        TT=TT3
        # -- bad Tcgen pyp? for rtfimz 2010072100
        try:
            TT.taus=TT2.taus
        except:
            TT.taus=TT1.taus
        TT.quiet=quiet
        if(verb): print 'TTTTTTTTTTTTTTTTT done... ',TT.pyppathTcgen
        if(diag): MF.dTimer(tag='TTallll')

        if(not(hasattr(TT,'bdtg'))): TT.bdtg=bdtg
        

    # -- set the ctlpath with data ...
    #
    TT.ctlpath=datactlpath
    TT.doga2=doga2

    return(TT)


def getTTpyp(tcD,dtg,model,basin,dogendtg=0,gentau=None,verb=0,quiet=0,diag=0,
             override=0,
             doga2=0):

    import FM
    
    if(model in (FM.wjetmodels + FM.taccmodels) ):
        FR=FM.getFRlocal(model,dtg)
    elif(model in (FM.m2models + w2.Nwp2ModelsAll) ):
        FR=FM.FimRunModel2Short(model,dtg,verb=verb,override=override)
    else:
        print 'EEE invalid model(getTTpyp): ',model
        sys.exit()


    if(not(dogendtg)): gentau=None
    TT=TmTrkGen(tcD,dtg,model,basin,gentau=gentau,quiet=quiet,diag=diag)
    TT.m2=FR.m2

    datactlpath=TT.ctlpath
    
    bdtg=TT.bdtg

    # make sure data are there...before recovering pyps...
    #
    if(TT.datathere == 0):
        print 'WWW(getTTpyp) no data...ctlpath not there...just return...'
        return(TT)

    
    if(hasattr(TT.TT,'remake')):
        if(TT.TT.remake):
            print 'WWW(getTTpyp) remade TT and TT.TT from scratch...no checking of pyps...and run doTrk()'
            TT.TT.doTrk()
            return(TT)

    if(os.path.exists(TT.pyppathTcgen)):
        if(diag): MF.sTimer(tag='TTallll')
        if(verb): print 'TTTTTTTTTTTTTTTTT there.. ',TT.pyppathTcgen,TT.pyppathTctrk
        if(diag): MF.sTimer(tag='TT1 for TT.pyppathTcgen ')
        TT1=TT.getPyp(pyppath=TT.pyppathTcgen,verb=verb)
        if(diag): MF.dTimer(tag='TT1 for TT.pyppathTcgen ')
        
        # -- check if tcgen bad
        if(TT1 == None):
            TT1=TT

        if(diag): MF.sTimer(tag='TT2 for TT.pyppathTcgen ')
        TT2=TT.getPyp(pyppath=TT.pyppathTctrk)
        if(diag): MF.dTimer(tag='TT2 for TT.pyppathTcgen ')

        TT3=TT1
        TT3.TT=TT2
        TT3.m2=FR.m2
        if(hasattr(TT,'tcD')): TT3.tcD=TT.tcD
        TT=TT3
        # -- bad Tcgen pyp? for rtfimz 2010072100
        try:
            TT.taus=TT2.taus
        except:
            TT.taus=TT1.taus
        TT.quiet=quiet
        if(verb): print 'TTTTTTTTTTTTTTTTT done... ',TT.pyppathTcgen
        if(diag): MF.dTimer(tag='TTallll')

        if(not(hasattr(TT,'bdtg'))): TT.bdtg=bdtg
        

    # -- set the ctlpath with data ...
    #
    TT.ctlpath=datactlpath
    TT.doga2=doga2

    return(TT)







def getBasinLatLons(basin):

    if(basin == 'global'):
        lat1=-30.0
        lat2=30.0
        lon1=0.0
        lon2=359.0

    elif(basin == 'lant'):

        lat1=0.0
        lat2=30.0
        lon1=360.0-100.0
        lon2=360.0-10.0

    elif(basin == 'epac'):

        lat1=0.0
        lat2=30.0
        lon1=180.0
        lon2=360.0-75.0

    elif(basin == 'wpac'):

        lat1=0.0
        lat2=30.0
        lon1=100.0
        lon2=180.0

    elif(basin == 'shem'):

        lat1=-30.0
        lat2=0.0
        lon1=35.0
        lon2=360.0-150.0

    elif(basin == 'nio'):

        lat1=0.0
        lat2=30.0
        lon1=40.0
        lon2=100.0

    else:
        print 'EEE invalid basin in getBasinLatLon: ',basin
        sys.exit()

    return(lat1,lat2,lon1,lon2)


def getBasinLatLonsPrecise(basin):

    latlons=[]

    if(basin == 'global'):
        lat1=-30.0
        lat2=30.0
        lon1=0.0
        lon2=359.0
        
        latlons.append((lat1,lat2,lon1,lon2))

    elif(basin == 'lant'):

        lat1=0.0
        lat2=30.0
        lon1=360.0-100.
        lon2=359.0

        lat1=0.0
        lat2=10.0
        lon2=360.0-10.0
        lon1=360.0-75.0
        latlons.append((lat1,lat2,lon1,lon2))

        lat1=10.0
        lat2=15.0
        lon2=360.0-10.0
        lon1=360.0-85.0
        latlons.append((lat1,lat2,lon1,lon2))

        lat1=15.0
        lat2=18.0
        lon2=360.0-10.0
        lon1=360.0-89.0
        latlons.append((lat1,lat2,lon1,lon2))

        lat1=18.0
        lat2=30.0
        lon2=360.0-10.0
        lon1=360.0-97.0
        latlons.append((lat1,lat2,lon1,lon2))


    elif(basin == 'epac'):

        lat1=0.0
        lat2=10.0
        lon1=180.0
        lon2=360.0-75.0
        latlons.append((lat1,lat2,lon1,lon2))

        lat1=10.0
        lat2=15.0
        lon1=180.0
        lon2=360.0-85.0
        latlons.append((lat1,lat2,lon1,lon2))

        lat1=15.0
        lat2=18.0
        lon1=180.0
        lon2=360.0-89.0
        latlons.append((lat1,lat2,lon1,lon2))

        lat1=18.0
        lat2=30.0
        lon1=180.0
        lon2=360.0-97.0
        latlons.append((lat1,lat2,lon1,lon2))

    elif(basin == 'wpac'):

        lat1=0.0
        lat2=30.0
        lon1=100.0
        lon2=180.0
        latlons.append((lat1,lat2,lon1,lon2))

    elif(basin == 'shem'):

        lat1=-30.0
        lat2=0.0
        lon1=35.0
        lon2=360.0-150.0
        latlons.append((lat1,lat2,lon1,lon2))

    elif(basin == 'nio'):

        lat1=0.0
        lat2=30.0
        lon1=40.0
        lon2=100.0
        latlons.append((lat1,lat2,lon1,lon2))

    else:
        print 'EEE invalid basin in getBasinLatLon: ',basin
        sys.exit()

    return(latlons)



def getFctrkGstdGtcBtcs(TT,dtg,model,basin,gentau,
                        fcdtau=24,
                        endtau=None,
                        doland=0):


    from TC import TcData,TcBasin

    if(not(hasattr(TT,'tcD'))):
        tcD=TcData(dtgopt=dtg,verb=verb)
    else:
        tcD=TT.tcD

    bP=TcBasin(basin)

    gstds={}
    fctrks={}
    gctrks={}
            
    vdtg=mf.dtginc(dtg,gentau)
    ags=makeAdeckGens(dtg,model,basin)
    afs=makeAdeckGensTctrk(tcD,dtg,model)


    ifctrks=afs.gettrks(dtg,dtau=fcdtau,endtau=gentau)
    
    igctrks=ags.gettrks(basin,dtg,gentau,dtau=fcdtau)

    igstds=ags.getsTDds(basin,dtg,gentau)


    for fstd in ifctrks.keys():

        ftlat=ifctrks[fstd][0][0]
        ftlon=ifctrks[fstd][0][1]

        # --- don't check for initial fc posits overland
        #flf=getLF(lf,ftlat,ftlon)
        #if(not(doland) and flf > 0.5):
        #    continue

        if(bP.isLLin(ftlat,ftlon)):
            fctrks[fstd]=ifctrks[fstd]


    for gstd in igstds.keys():

        gtlat=igstds[gstd][2]
        gtlon=igstds[gstd][3]

        glf=getLF(lf,gtlat,gtlon)
        if(not(doland) and glf > 0.5):
            continue

        if(bP.isLLin(gtlat,gtlon)):
            gstds[gstd]=igstds[gstd]
            gctrks[gstd]=igctrks[gstd]

    (ivstmids,ivbtcs)=tcD.getDtg(vdtg)
    (istmids,ibtcs)=tcD.getDtg(dtg)

    abtcs={}
    btcs={}
    vbtcs={}
    stmids=[]

    for stmid in ivbtcs.keys():
        btlat=ivbtcs[stmid][0]
        btlon=ivbtcs[stmid][1]
        
        if(bP.isLLin(btlat,btlon)):
            vbtcs[stmid]=ivbtcs[stmid]
            abtcs[stmid]=ivbtcs[stmid]


    for stmid in ibtcs.keys():
        btlat=ibtcs[stmid][0]
        btlon=ibtcs[stmid][1]
        if(bP.isLLin(btlat,btlon)):
            btcs[stmid]=ibtcs[stmid]
            abtcs[stmid]=ibtcs[stmid]


    gtcs={}
    igtcs=tcD.getGenTcsDtg(vdtg)

    for gtc in igtcs:
        gtrk=igtcs[gtc]
        gtclat=gtrk[0]
        gtclon=gtrk[1]
        if(bP.isLLin(gtclat,gtclon)):
            gtcs[gtc]=gtrk

    return(fctrks,gctrks,gstds,gtcs,btcs,vbtcs,abtcs)


def getGenDtgsByStorm(stmids,filt00z12z=1,verb=0):

    tcD=TcData(stmopt=stmids,verb=verb)
    gendtgs=[]
    for stmid in stmids:
        try:
            gendtgs=gendtgs+tcD.mdDg.gendtgs[stmid]
            if(verb): print 'GGGendtgs for stmid: ',stmid,' gendtgs: ',gendtgs
        except:
            print "WWW getGenDtgsByStorm(%s) are not available"%(stmid)

    finaldtgs=[]
    for gendtg in gendtgs:
        hh=gendtg[8:10]
        if(filt00z12z and (hh == '00' or  hh == '12')): finaldtgs.append(gendtg)


    finaldtgs=MF.uniq(finaldtgs)

    return(finaldtgs)

def getGenDtgsByStormOld(stmids,filt00z12z=1,verb=0):

    tcD=TcData(verb=verb)
    gendtgs=[]
    for stmid in stmids:
        try:
            gendtgs=gendtgs+tcD.mdDg.gendtgs[stmid]
            if(verb): print 'GGGendtgs for stmid: ',stmid,' gendtgs: ',gendtgs
        except:
            print "WWW getGenDtgsByStormOld(%s) are not available"%(stmid)

    finaldtgs=[]
    for gendtg in gendtgs:
        hh=gendtg[8:10]
        if(filt00z12z and (hh == '00' or  hh == '12')): finaldtgs.append(gendtg)


    finaldtgs=MF.uniq(finaldtgs)

    return(finaldtgs)

    
def getBasinOptFromStmids(tstmids):

    if(not(type(tstmids) is ListType)):
        tstmids=[tstmids]
    basins=[]
    for stmid in tstmids:
        b1id=stmid[2].lower()
        basin=b1id2tcgenBasin[b1id]
        basins.append(basin)

    basins=MF.uniq(basins)

    return(basins)
    
def getGentaus(gentau):

    if(gentau == 'all'):
        gentaus=[0,48,72,96,120,144]
    elif(gentau == 'allgen'):
        gentaus=[72,96,120,144]
    else:
        gentaus=[]
        tt=gentau.split(',')
        for t in tt:
            try:
                gentaus.append(int(t))
            except:
                print 'WWW invalid tau in gentau: ',gentau

        gentaus=MF.uniq(gentaus)

    return(gentaus)


def cleanGenFiles(keepdtg,ropt=''):

    yyyy=keepdtg[0:4]
    MF.ChangeDir(tcgenW3Dir)
    curdtgs=glob.glob("%s/??????????"%(yyyy))
    curdtgs.sort()

    for curdtg in curdtgs:
        cdtg=curdtg.split('/')[1]
        dtime=mf.dtgdiff(keepdtg,cdtg)
        if(dtime < 0.0):
            cmd="rm -r %s/%s"%(tcgenW3Dir,curdtg)
            mf.runcmd(cmd,ropt)




def getGentaus(gentau):

    if(gentau == 'all'):
        gentaus=[0,48,72,96,120,144]
        gentaus=[60,132]
        gentaus=[0,60,132]
        # -- d+2 (60) d+3 (84) d+5 (132)
        gentaus=[0,60,84,108,132]
        gentaus=[0,60,84,108,120,144,168]

    elif(gentau == 'allgen'):
        gentaus=[72,96,120,144]

    elif(gentau == 'all24h'):
        gentaus=[0,24,48,72,96,120]
        gentaus=[0,24,72,120]

    else:
        gentaus=[]
        tt=gentau.split(',')
        for t in tt:
            try:
                gentaus.append(int(t))
            except:
                print 'WWW invalid tau in gentau: ',gentau

        gentaus=MF.uniq(gentaus)

    return(gentaus)

