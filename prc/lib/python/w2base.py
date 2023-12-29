from M import *
MF=MFutils()

from w2switches import *
from w2localvars import *
from w2methods import *

from w2env import W2env
from w2nwp2 import W2Nwp2

from mfbase import ptmpBaseDir

class Model(MFbase):

    def DoGribmap(self,gmpverb=0):

        if(self.gribtype == 'grb1'): xgribmap='gribmap'
        if(self.gribtype == 'grb2'): xgribmap='gribmap'
        xgopt='-i'
        if(gmpverb):
            xgopt='-v -i'

        cmd="%s %s %s"%(xgribmap,xgopt,self.ctlpath)
        mf.runcmd(cmd)


class InvHash(MFbase):

    def __init__(self,
                 dbname,
                 tbdir=None,
                 dbkeyLocal='inventory',
                 diag=0,
                 verb=0,
                 override=0,
                 unlink=0):

        MF=MFutils()
        self.dbname=dbname
        self.tbdir=tbdir

        self.dbname=dbname
        self.dbfile="%s.pypdb"%(dbname)
        if(tbdir == None):
            tbdir='/tmp'
            self.dsbdir="%s/DSs"%(tbdir)
        else:
            self.dsbdir=tbdir

        MF.ChkDir(self.dsbdir,'mk')

        self.DSs=DataSets(bdir=self.dsbdir,name=self.dbfile,dtype=self.dbname,verb=verb,unlink=unlink,doDSsWrite=1)
        self.dbkeyLocal=dbkeyLocal

        if(diag): MF.sTimer('setDSs')
        try:
            self.dsL=self.DSs.getDataSet(key=self.dbkeyLocal,verb=verb)
            self.hash=self.dsL.data
        except:
            self.dsL=DataSet(name=self.dbkeyLocal,dtype='hash')
            self.hash={}

        if(override): self.hash={}

        if(diag): MF.dTimer('setDSs')

    def put(self,verb=0):

        self.dsL.data=self.hash
        self.DSs.putDataSet(self.dsL,key=self.dbkeyLocal,verb=verb)

    def close(self,verb=1):
        self.DSs.closeDataSet(verb=verb, warn=1)

    def lsInv(self,
              models,
              dtgs,
              basins=None,
              gentaus=None,
              dogendtg=None,
              ):

        #type='fcst'
        #if(dogendtg): type='veri'


        kk=self.hash.keys()
        for k in kk:
            print 'key: ',k
            vals=self.hash[k]
            print vals
            #for val in self.hash[k]:
            #    print val


class W2Base(W2env,W2Nwp2,W2GlobalVars):

    __doc__="""
#bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb
# base
#bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb
"""

    #iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii -- initialize

    def __init__(self,
                 W2BaseDirDat=None,
                 ):


        self.W2BaseDirDat=W2BaseDirDat

        self.initW2GlobalVars()
        self.initW2LocalVars()
        self.initW2VarsSwitches()
        self.initW2VarsModule()
        self.initW2VarsEnv()
        self.initW2VarsAll()
        self.initW2VarsNwp2()
        self.initW2VarsClimo()



    def initW2LocalVars(self):

        # -- from w2localvars.py
        #
        
        if('onZeus' in globals()):   self.onZeus=onZeus
        else:                        self.onZeus=onWjet
        
        if('onTheia' in globals()):   self.onTheia=onTheia
        else:                         self.onTheia=onWjet

        if('onHera' in globals()):   self.onHera=onHera
        else:                         self.onHera=onWjet
        
        if('onTaifuu' in globals()): self.onTaifuu=onTaifuu
        else:                        self.onTaifuu=0

        if('onTenki' in globals()): self.onTenki=onTenki
        else:                        self.onTenki=0

        if('onKaze' in globals()):   self.onKaze=onKaze
        else:                        self.onKaze=0

        if('onKishou' in globals()): self.onKishou=onKishou
        else:                        self.onKishou=0
        
        if('onWjet' in globals()):   self.onWjet=onWjet
        else:                        self.onWjet=0
        
        if('onGmu' in globals()):    self.onGmu=onGmu
        else:                        self.onGmu=0
        # -- 20210622 -- add location ptmp to remove dependence on /ptmp
        #
        self.ptmpBaseDir=ptmpBaseDir
        
        self.remoteHost=remoteHost
        self.W2Host=W2Host
        self.curuSer=curuSer
        self.W2plotAspect=W2plotAspect
        self.W2plotXsize=W2plotXsize
        
        self.HfipWebBdir=HfipWebBdir
        self.LocalBaseDirLog=LocalBaseDirLog
        self.W2LocalBaseDir=W2LocalBaseDir

        self.CagipsDatBdir=CagipsDatBdir
        self.CagipsSdirNgpc=CagipsSdirNgpc
        if('CagipsSdirNavg' in globals()):      self.CagipsSdirNavg=CagipsSdirNavg
        self.CagipsSdirNgpj=CagipsSdirNgpj
        self.CagipsSdirGfsc=CagipsSdirGfsc
        self.CagipsSdiruKmc=CagipsSdiruKmc
        self.CagipsSdirJmac=CagipsSdirJmac
        self.CagipsSdirOcn=CagipsSdirOcn
        self.CagipsSdirOhc=CagipsSdirOhc
        self.CagipsSdirWw3=CagipsSdirWw3
        if('CagipsPrcDir' in globals()):      self.CagipsPrcDir=CagipsPrcDir
        if('CagipsPrcDirBeta' in globals()):  self.CagipsPrcDirBeta=CagipsPrcDirBeta
        self.nMaxPidInCron=nMaxPidInCron
        self.dochkifrunning=dochkifrunning

        self.W2AreasPrw=W2AreasPrw
        self.W2AreasPrwOld=W2AreasPrwOld
        self.W2AreasPrws=W2AreasPrws
        self.W2MaxOldRegen=W2MaxOldRegen

        self.Nwp2ModelsAll=Nwp2ModelsAll
        self.Nwp2ModelsNwp=Nwp2ModelsNwp
        self.Nwp2ModelsActive=Nwp2ModelsActive
        self.Nwp2ModelsActiveW2flds=Nwp2ModelsActiveW2flds
        if(Nwp2ModelsActW20012 != None): self.Nwp2ModelsActW20012=Nwp2ModelsActW20012
        if(Nwp2ModelsActW20618 != None): self.Nwp2ModelsActW20618=Nwp2ModelsActW20618
        
        if(TCsourcesActive != None): self.TCsourcesActive=TCsourcesActive


    def initW2VarsModule(self):

        # -- module vars -> object
        #
        self.W2adminuSer=W2adminuSer
        self.W2currentuSer=W2currentuSer
        self.TcTcepsNcepSource=TcTcepsNcepSource
        self.W2rawECHiRes=W2rawECHiRes
        self.EcNogapsCssFeed=EcNogapsCssFeed
        self.W2BaseDirDat2=LocalBaseDirDat


    def initW2VarsSwitches(self):

        # -- pull vars from w2switches
        #
        self.wxModels=wxModels
        if(W2doDATAonly != None): 
            self.W2doDATAonly=W2doDATAonly
        else:
            self.W2doDATAonly=0
            
        if(W2doRsyncPushGmu != None): 
            self.W2doRsyncPushGmu=W2doRsyncPushGmu
        else:
            self.W2doRsyncPushGmu=0
            
        # -- 20231215 -- switch to turn on rsync to wxmap2
        #
        if(W2doRsync2Wxmap2 != None): 
            self.W2doRsync2Wxmap2=W2doRsync2Wxmap2
        else:
            self.W2doRsync2Wxmap2=0
            
        self.W2doM2Tryarch=W2doM2Tryarch
        self.W2Nwp2DataOnly=W2Nwp2DataOnly
        self.W2doTCdiag=W2doTCdiag
        self.W2doTCfilt=W2doTCfilt
        self.W2mintauTCfilt=mintauTCfilt
        self.W2doTCgen=W2doTCgen
        self.W2doFimPost2DataOnly=W2doFimPost2DataOnly

        self.W2doMirrorWjet=W2doMirrorWjet
        self.W2doNcepEnsTrackers=W2doNcepEnsTrackers
        self.W2doW3Rapb=W2doW3Rapb

        self.W2doW3RapbFimAdecks=W2doW3RapbFimAdecks
        self.W2doW3RapbEpsInv=W2doW3RapbEpsInv
        self.W2doW3RapbRefTrk=W2doW3RapbRefTrk

        self.W2isHfipDemo=W2isHfipDemo
        self.W2doW3RapbBdecks=W2doW3RapbBdecks
        self.W2doW3RapbRsync=W2doW3RapbRsync
        self.W2doW3RapbXmlAdecks=W2doW3RapbXmlAdecks
        self.W2doW3RapbWjetAdecks=W2doW3RapbWjetAdecks

        self.W2doW3RapbNcepCmcAdecks=W2doW3RapbNcepCmcAdecks
        self.W2doW3RapbRtfimAdecks=W2doW3RapbRtfimAdecks
        self.W2doTcepsAnl=W2doTcepsAnl
        self.W2doPublicAdecks=W2doPublicAdecks
        self.W2doGfsEnkf=W2doGfsEnkf
        self.W2doGfsEnkfOnly=W2doGfsEnkfOnly
        self.wjetsources=wjetsources

        self.W2doTcepsAnl=W2doTcepsAnl

        self.W2doWjet=W2doWjet
        self.W2Nwp2DataOnly=W2Nwp2DataOnly
        self.W2Model2PlotWeb=W2Model2PlotWeb
        self.W2NdayClean=W2NdayClean
        self.W2NdayCleanPrwLoop=W2NdayCleanPrwLoop
        self.W2NdayCleanTcanal=W2NdayCleanTcanal
        self.W2NdayCleanTcfilt=W2NdayCleanTcfilt
        self.W2doKaze2KishouTCdat=W2doKaze2KishouTCdat

    def initW2VarsEnv(self):

        self.W2Center=os.getenv('W2CENTER')
        self.W2Version=os.getenv('W2_VERSION')
        self.W2CenterFullName=self.W2Center

        self.W2Dir=os.getenv('W2')
        self.W2BaseDir=os.getenv('W2_BDIR')
        self.W2BaseDirEtc="%s/etc"%(self.W2BaseDir)

        if(self.W2BaseDirDat == None):   self.W2BaseDirDat=os.getenv('W2_BDIRDAT')
        else:                            self.W2BaseDirDat=self.W2BaseDirDat

        self.ptmpBaseDir=os.getenv('PTMP')

        self.W2BaseDirApp=os.getenv('W2_BDIRAPP')
        self.W2BaseDirBin=os.getenv('W2_BDIRBIN')
        self.W2BaseDirPlt=os.getenv('W2_BDIRPLT')
        self.W2BaseDirWeb=os.getenv('W2_BDIRWEB')
        self.W2BaseDirEvt=os.getenv('W2_BDIREVT')
        self.W2BaseDirLog=os.getenv('W2_BDIRLOG')
        self.W2BaseDirPrc=os.getenv('W2_PRC_DIR')


        os.getenv('W2_VERSION')
        os.getenv('W2_GRADS_BDIR')
        os.getenv('W2_OPENGRADS2_BDIR')
        os.getenv('W2_GRADS2_BDIR')
        os.getenv('W2_BDIRAPPLIB')
        os.getenv('W2_BDIRDAT')
        os.getenv('W2_SRC_DIR')
        os.getenv('W2_BDIRWEB')
        os.getenv('W2_BDIRPLT')
        os.getenv('W2_BDIRLIB')
        os.getenv('W2_PERL_DIR')
        os.getenv('W2_BDIRWEBCONFIG')
        os.getenv('W2_BDIRMSSBIN')
        os.getenv('W2_PY_DIR')
        os.getenv('W2_BDIRDB3LIB')
        os.getenv('W2_BDIRLOG')
        os.getenv('W2_BDIRAPP')
        os.getenv('W2_GRADS_VERSION')
        os.getenv('W2_BDIREVT')
        os.getenv('W2_BDIRBIN')
        os.getenv('W2_BDIR')
        os.getenv('W2_PRC_DIR')
        os.getenv('BUFR_TABLES')
        os.getenv('PERL5LIB')
        os.getenv('GALIBD')
        os.getenv('LD_LIBRARY_PATH')
        os.getenv('GASCRP')
        os.getenv('GRIBTAB')
        
        os.getenv('ECCODES_DEFINITION_PATH')
        os.getenv('PYTHONSTARTUP')
        os.getenv('W2CENTER')
        os.getenv('GA2UDXT')
        os.getenv('PYTHONPATH')
        os.getenv('VISUAL')
        os.getenv('EDITOR')
        os.getenv('GADDIR')

        self.W2EnvVarPtmp=os.getenv('PTMP')
        self.W2EnvVarWeb=os.getenv('W2_BDIRWEB')
        self.W2EnvVarHfipDat=os.getenv('W2_HFIPDAT')
        self.W2EnvVarHfip=os.getenv('W2_HFIP')
        self.HfipProducts=self.W2EnvVarHfip
        


    def initW2VarsNwp2(self):

        self.prodcenter=self.W2Center
        self.geodir=self.W2BaseDirDat+'/geog'

        self.Nwp2DataBdir="%s/nwp2"%(self.W2BaseDirDat)
        self.Nwp2DataDSsBdir="%s/DSs"%(self.Nwp2DataBdir)
        self.Nwp2DataBdirArch1="/dat5/dat/nwp2"
        self.Nwp2DataBdirArch2="/dat6/dat/nwp2"
        self.Nwp2DataBdirArch3="/dat5/dat/nwp2"
        
        # -- move Nwp2Models... to pull from w2localvar.py in initW2VarsLocal
        
        self.allBdirs=[self.Nwp2DataBdir,self.Nwp2DataBdirArch1,self.Nwp2DataBdirArch2]

        self.maxfphrWeb=maxfphrWeb

    def initW2VarsClimo(self):

        self.climosstdir=self.W2BaseDirDat+'/climo/sst'
        self.climodatdir=self.W2BaseDirDat+'/climo'

        #self.climosstdir=None
        #self.climodatdir=None

        # -- 20120910 -- R1 wind climo

        self.R1ClimoDatDir='%s/ncepr1_daily_wind/ac'%(self.climodatdir)
        self.R1ClimoByear=1970
        self.R1ClimoEyear=2000
        self.R1ClimoNday=6


    def initW2VarsAll(self):

        self.W2TmpPrcDirPrefix='/tmp/PRC.W2PLOT'

        self.AppBdirW2=self.W2BaseDirApp
        self.BinBdirW2=self.W2BaseDirBin
        self.SrcBdirW2=self.W2BaseDir+'/src'
        self.PrcBdirW2=self.W2BaseDir+'/prc'
        self.PrcCfgBdirW2=self.PrcBdirW2+'/cfg'
        self.DatBdirW2=self.W2BaseDirDat
        self.EvtBdirW2=self.W2BaseDirEvt

        self.W2BaseDirDat2='/data/wxmap2/dat'
        self.W2BaseDirDat2='/storage2/kishou/wxmap2/dat'
        self.W2BaseDirDat2='/storage4/kishou/wxmap2/dat'
        self.W2BaseDirDat2='/wxmap2/dat2'
        self.W2BaseDirDat2='/dat2'
        self.W2BaseDirDat2=self.W2BaseDirDat


        self.DatBdirW2data=self.W2BaseDirDat2

        if(self.onWjet):
####            self.LogBdirW2='/lfs2/projects/fim/fiorino/tmp'
            self.LogBdirW2='/lfs1/projects/fim/fiorino/tmp'
            self.PrwLoopTmpDir='%s/prw'%(self.LogBdirW2)
        else:
            self.LogBdirW2=self.ptmpBaseDir
            self.PrwLoopTmpDir='%s/prw'%(self.ptmpBaseDir)
        
        if('LogBdirW2' in globals()):      self.LogBdirW2=LogBdirW2
        if('PrwLoopTmpDir' in globals()):  self.PrwLoopTmpDir=PrwLoopTmpDir

        self.PrwGoesDir="%s/plt_prw_goes"%(self.W2BaseDirWeb)
        
        self.W2BaseDirWebConfig="%s/web-config"%(self.W2BaseDir)
        # -- 202for grads that can't handle uppercase dirs
        self.W2BaseDirWebConfigROOT="/w%s/web-config"%(self.W2Version)
        
        self.tcgenBaseDirWeb="%s/tcgen"%(self.W2BaseDirWebConfig)
        self.jtdiagBaseDirWeb="%s/jtdiag"%(self.W2BaseDirWebConfig)
        self.tcdiagBaseDirWeb="%s/tcdiag"%(self.W2BaseDirWebConfig)
        self.tcepsBaseDirWeb="%s/tceps"%(self.W2BaseDirWebConfig)
        self.tcgenBaseDirWeb="%s/tcgen"%(self.W2BaseDirWebConfig)
        self.tcactBaseDirWeb="%s/tcact"%(self.W2BaseDirWebConfig)
        

        #self.LogBdirW2='/tmp'
        #self.PrwLoopTmpDir='/tmp/prw'

        self.GradsBdirW2=self.AppBdirW2+'/grads'
        self.GradsGslibDir=self.GradsBdirW2+'/gslib'

        self.NwpDataBdirW2=self.DatBdirW2
        self.CMDuncompress='uncompress'
        self.CMDuncompress='gunzip'



#pppppppppppppppppppppppppppppppppppppppppppp
# /public/ - esrl

        self.EsrlPublicDirFim='/public/data/fsl/fim/tracker'
        self.EsrlPublicDirFim9='/public/data/fsl/fim/tracker'

        self.DATKazeBaseDir=DATKazeBaseDir

#wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww
# kishou

        self.KishouScpServer='kishou.fsl.noaa.gov'
        self.KishouTcDatDir="/w21/dat/tc"
        
#wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww
# kishou
        
        self.KazeScpServer='tcops.fsl.noaa.gov'
        self.KazeScpServer='wxmap2.fsl.noaa.gov'
        self.KazeTcDatDir=HfipTcDatDir


# hfip
        self.HfipTcDatDir=HfipTcDatDir

#wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww
# wjet

        self.WjetScpServer='jetscp.rdhpcs.noaa.gov'
        self.WjetScpServer='dtn-jet.rdhpcs.noaa.gov'
        self.WjetScpServerLogin='fiorino'
        self.WjetScpServerLogin='Michael.Fiorino'

####        self.WjetQmorphDir='/lfs2/projects/fim/fiorino/dat/qmorph'
####        self.WjetFimProject='/lfs2/projects/fim/fiorino'
####        self.WjetRtfim='/lfs2/projects/rtfim'

        self.WjetQmorphDir='/lfs1/projects/fim/fiorino/dat/qmorph'
        self.WjetFimProject='/lfs1/projects/fim/fiorino'
        self.WjetRtfim='/lfs1/projects/rtfim'

        self.WjetW2base=sbaseWjet
        self.ZeusW2base=sbaseZeus
        self.W2WjetW2base="%s/w21"%(sbaseWjet)
        self.W2ZeusW2base="%s/w21"%(sbaseZeus)
        self.WjetTcDatDir="%s/dat/tc"%(self.W2WjetW2base)
        self.WjetTcvitals='/pan2/projects/fim-njet/tcvitals'
        self.WjetTcvitals='/lfs1/projects/fim/tcvitals'
        self.WjetTcvitals='/lfs3/projects/gsd-fv3-hfip/tcvitals'

#wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww
# zeus

        self.ZeusScpServer='dtn-zeus.rdhpcs.noaa.gov'
        self.ZeusScpServerLogin='Michael.Fiorino'
        self.ZeusTcvitals='/scratch1/portfolios/BMC/fim/tcvitals'
        self.ZeusW2base=sbaseZeus
        self.W2ZeusW2base="%s/w21"%(sbaseZeus)
        self.ZeusTcDatDir="%s/dat/tc"%(self.W2ZeusW2base)
#wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww
# theia

        self.TheiaScpServer='dtn-theia.fairmont.rdhpcs.noaa.gov'
        self.TheiaScpServer='dtn-theia.rdhpcs.noaa.gov'
        self.TheiaScpServerLogin='Michael.Fiorino'
        self.TheiaTcvitals='/scratch4/BMC/fim/tcvitals'
        self.TheiaW2base=sbaseTheia
        self.W2TheiaW2base="%s/w21"%(sbaseTheia)
        self.TheiaTcDatDir="%s/dat/tc"%(self.W2TheiaW2base)

#wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww
# hera

        self.HeraScpServer='dtn-hera.fairmont.rdhpcs.noaa.gov'
        self.HeraScpServer='dtn-hera.rdhpcs.noaa.gov'
        self.HeraScpServerLogin='Michael.Fiorino'
        self.HeraTcvitals='/scratch2/BMC/gsd-fv3-dev/tcvitals'
        self.HeraW2base=sbaseHera
        self.W2HeraW2base="%s/w21"%(sbaseHera)
        self.HeraTcDatDir="%s/dat/tc"%(self.W2HeraW2base)


#rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr
# ranger.tacc.utexas.edu

        self.TaccUser='mfiorino'
        self.TaccServer='ranger.tacc.utexas.edu'
        self.TaccFim9Gfs='/scratch/01033/harrop/FIM/FIMrun'
        self.TaccFim9EnKF='/scratch/01033/harrop/FIM_ens/FIMrun'
        self.TaccFim8EnKF='/scratch/01033/harrop/FIM_ens/FIMrun'
        self.TaccFim10kmEnKF='/scratch/01033/harrop/FIM_10km/FIMrun'
        self.TaccTcvitals='/work/01233/mfiorino/w21/dat/tc/tcvitals'
        self.TaccMfAdecks='/work/01233/mfiorino/w21/dat/tc/adeck/tacc/2009'


        self.Nwp2DataBdir='/storage2/nwp2'
        self.Nwp2DataBdir='/storage3/nwp2'
        self.Nwp2DataBdir="%s/nwp2"%(self.W2BaseDirDat)

        self.Nwp2DataArchiveBdirLocal='/storage0/nwp2'
        self.Nwp2DataArchiveBdirLocal10='/storage10/nwp2'
        self.Nwp2DataArchiveBdirLocal11='/storage11/nwp2'
        self.Nwp2DataArchiveBdirSnap='/storage4/nwp2'

        self.Nwp2DataMassStore='/mss/jet/projects/fim/fiorino/nwp2'
        self.NwpDataMassStore='/mss/jet/projects/fim/fiorino/nwp'
        self.RtfimDataMassStore='/mss/jet/projects/fim/fiorino/rtfim'

        self.GeogDatDirW2="%s/geog"%(self.DatBdirW2)

        self.PrcDirTcdatW2="%s/tcdat"%(self.PrcBdirW2)
        self.PrcDirTcdiagW2="%s/tcdiag"%(self.PrcBdirW2)
        self.PrcDirTcbogW2="%s/tcbog"%(self.PrcBdirW2)
        self.PrcDirTcpltW2="%s/tcplt"%(self.PrcBdirW2)
        self.PrcDirTcww3W2="%s/tcww3"%(self.PrcBdirW2)
        self.PrcDirWebW2="%s/web"%(self.PrcBdirW2)
        self.PrcDirUtilW2="%s/util"%(self.PrcBdirW2)
        self.PrcDirWxmap2W2="%s/wxmap2"%(self.PrcBdirW2)
        self.PrcDirTcanalW2="%s/tcanal"%(self.PrcBdirW2)
        self.PrcDirTctrkW2="%s/tctrk"%(self.PrcBdirW2)
        self.PrcDirTcgenW2="%s/tcgen"%(self.PrcBdirW2)
        self.PrcDirTcepsW2="%s/tcdat"%(self.PrcBdirW2)
        self.PrcDirTcfiltW2="%s/tcfilt"%(self.PrcBdirW2)
        self.PrcDirTcclimoW2="%s/tcclimo"%(self.PrcBdirW2)

        self.PrcDirFlddatW2="%s/flddat"%(self.PrcBdirW2)
        self.PrcDirFlddatHwrfW2="%s/hwrf"%(self.PrcBdirW2)
        self.PrcDirFldanalW2="%s/fldanal"%(self.PrcBdirW2)

        self.FtpIncomingDir='/pcmdi/ftp_incoming/fiorino'

        self.AtcfFtpserver='198.97.80.42'
        self.AtcfLogin='atcfp1'
        self.AtcfPasswd='atcfp112'
        self.AtcfArchiveDir='/opt/DEVELOPMENT/atcf/archives'
        self.AtcfStormDir='/opt/DEVELOPMENT/atcf/storms'


        self.TcDatDir="%s/tc"%(self.W2BaseDirDat)
        self.TcDatDirMFtrk="%s/tc/mftrk"%(self.W2BaseDirDat)
        self.TcDatDirTMtrkN="%s/tc/tmtrkN"%(self.W2BaseDirDat)
        self.TcDatDirDSs="%s/tc/DSs"%(self.W2BaseDirDat)
        self.TcDatDir2="%s/tc"%(self.W2BaseDirDat2)


        self.WdriveFtpBaseDir='/wdrive/FTP/users/fiorino'

        self.TcAdecksXfr2AtcfDir="%s/adeck/xfr2atcf"%(self.TcDatDir)

        self.eBdeckDir="%s/ebt"%(self.TcDatDir)

        self.TcRefTrkDatDir="%s/reftrk"%(self.TcDatDir)

        self.TcAdecksNhcDir="%s/adeck/nhc"%(self.TcDatDir)
        self.TcAdecksJtwcNhcDir="%s/adeckjtwc/nhc"%(self.TcDatDir)
        self.TcBdecksNhcDir="%s/bdeck/nhc"%(self.TcDatDir)
        self.TcBdecksNhcDir2="%s/bdeck2/nhc"%(self.TcDatDir)
        self.TcStormsNhcDir="%s/nhc"%(self.TcDatDir)
        self.TcDatDirNhc="%s/nhc"%(self.TcDatDir)
        self.TcComNhcDir="%s/com/nhc"%(self.TcDatDir)
        self.TcDisNhcDir="%s/dis/nhc"%(self.TcDatDir)
        self.TcStextNhcDir="%s/stext/nhc"%(self.TcDatDir)
        self.TcStextJtwcDir="%s/stext/jtwc"%(self.TcDatDir)

        self.TcABdecksJtwcDir="%s/jtwc"%(self.TcDatDir)
        self.TcAdecksJtwcDir="%s/adeck/jtwc"%(self.TcDatDir)
        self.TcBdecksJtwcDir="%s/bdeck/jtwc"%(self.TcDatDir)
        self.TcBdecksJtwcDir2="%s/bdeck2/jtwc"%(self.TcDatDir)
        self.TcStormsJtwcDir="%s/jtwc"%(self.TcDatDir)
        self.TcComJtwcDir="%s/com/jtwc"%(self.TcDatDir)

        self.TcBdecksNeumannDir="%s/bdeck/neumann"%(self.TcDatDir)
        self.TcStormsNeumannDir="%s/neumann"%(self.TcDatDir)

        self.TcBdecksHurdatDir="%s/bdeck/hurdat"%(self.TcDatDir)
        self.TcStormsHurdatDir="%s/hurdat"%(self.TcDatDir)
        self.TcEcmwfEcbufr="%s/ecmwf/ecbufr"%(self.TcDatDir)

        self.TcAdecksLocalDir="%s/adeck/local"%(self.TcDatDir)
        self.TcAdecksEcmwfDir="%s/adeck/ecmwf"%(self.TcDatDir)
        self.TcAdecksMitDir="%s/adeck/mit"%(self.TcDatDir)
        self.TcAdecksTcepsDir="%s/adeck/tceps"%(self.TcDatDir)
        self.TcAdecksuKmoDir="%s/adeck/ukmo"%(self.TcDatDir)
        self.TcAdecksNcepDir="%s/adeck/ncep"%(self.TcDatDir)
        self.TcAdecksCmcDir="%s/adeck/cmc"%(self.TcDatDir)
        self.TcAdecksEsrlDir="%s/adeck/esrl"%(self.TcDatDir)
        self.TcAdecksLocalDir="%s/adeck/local"%(self.TcDatDir)
        self.TcAdecksGfsenkfDir="%s/adeck/esrl"%(self.TcDatDir)
        self.TcAdecksTaccDir="%s/adeck/tacc"%(self.TcDatDir)
        self.TcAdecksJmaDir="%s/adeck/jma"%(self.TcDatDir)
        self.TcAdecksFnmocDir="%s/adeck/jtwc"%(self.TcDatDir)
        self.TcAdecksTmtrkNDir="%s/adeck/tmtrkN"%(self.TcDatDir)

        self.HfipBaseDir="/dat2/hfip/web"
        self.HfipHttpInternetDocRoot='/w3/rapb/hfip'

#tttttttccccccc
# tceps
#


        self.TcBaseDirPltTc=self.W2BaseDirPlt+"/tc"
        self.TcPltEcmwfDir=self.TcBaseDirPltTc+"/ecmwf"
        self.TcPltEcmwfEpsDir=self.TcBaseDirPltTc+"/ecmwf_eps"

        self.TcTcepsEcmwfDir="%s/tceps/ecmwf"%(self.TcDatDir)
        self.TcTcepsuKmoDir="%s/tceps/ukmo"%(self.TcDatDir)
        self.TcTcepsNcepDir="%s/tceps/ncep"%(self.TcDatDir)
        self.TcTcepsCmcDir="%s/tceps/cmc"%(self.TcDatDir)
        self.TcTcepsEsrlDir="%s/tceps/esrl"%(self.TcDatDir)
        self.TcTcepsGfsenkfDir="%s/tceps/gfsenkf"%(self.TcDatDir)
        self.TcTcepsFimensDir="%s/tceps/fimens"%(self.TcDatDir)
        self.TcTcepsFnmocDir="%s/tceps/fnmoc"%(self.TcDatDir)

        self.TcTcepsEcmwfNmembers=51
        self.TcTcepsEcmwfNmembers=50
        self.TcTcepsuKmoNmembers=24
        self.TcTcepsuKmoNmembers=35
        self.TcTcepsNcepNmembers=31
        self.TcTcepsCmcNmembers=21
        self.TcTcepsEsrlNmembers=21
        self.TcTcepsGfsenkfNmembers=20
        self.TcTcepsFimensNmembers=20
        self.TcTcepsFnmocNmembers=20

        self.TcTcepsDatDirRT="%s/tceps"%(self.TcDatDir)
        self.TcTcepsDatDir="%s/tceps"%(self.TcDatDir2)
        self.TcTcepsDatDirTail="dat/tc/tceps"
        self.TcTcepsWebDir="%s/tceps"%(self.HfipBaseDir)


        # -- tcclimo
        #
        BaseDirPltTc=self.TcBaseDirPltTc
        self.PltTcOpsDir="%s/ops"%(BaseDirPltTc)
        self.PltTcOpsClimoDir="%s/climo"%(self.PltTcOpsDir)

# direct write to webserver dir
        if(W2doW3RapbRsync == 0): self.TcTcepsWebDir="%s/tceps"%(self.HfipProducts)

        self.TcTcepsWebDirKishou="%s/tceps"%(self.HfipBaseDir)

        self.TcTcanalDatDirRT="%s/tcanal"%(self.TcDatDir)
        self.TcTcanalDatDir="%s/tcanal"%(self.TcDatDir2)
        self.TcTcanalDatDir0="%s/tcanal0"%(self.TcDatDir2)
        self.TcTcanalDatDirTail="dat/tc/tcanal"
        self.TcTcanalWebDir="%s/tc/tcanal"%(self.W2BaseDirWeb)

        self.TcTcdiagDatDir="%s/tcdiag"%(self.TcDatDir2)

        self.TcAtcfDatDir="%s/atcf"%(self.TcDatDir)
                
        self.TcBtNeumannDatDir="%s/btn"%(self.TcDatDir)
        self.TcBtHurdatDatDir="%s/bth"%(self.TcDatDir)
        self.TcBtOpsDatDir="%s/bto"%(self.TcDatDir)

        self.TcTcfiltDatDirRT="%s/tcfilt"%(self.TcDatDir)
        self.TcTcfiltDatDir="%s/tcfilt"%(self.TcDatDir2)
        self.TcTcfiltDatDirTail="dat/tc/tcfilt"
        self.TcTcfiltWebDir="%s/tc/tcfilt"%(self.W2BaseDirWeb)
        self.TcTcfiltWdriveWebDir="%s/tc/tcfilt"%(self.W2BaseDirWeb)

        self.TcTcWW3WebDir="%s/tc/tcww3"%(self.W2BaseDirWeb)

        self.TceBtCsuDatDir="%s/ebt"%(self.TcDatDir)

        self.TcCimssWindRadiiDir="%s/cimss"%(self.TcDatDir)
        self.TccBtCimssDatDir="%s/cbt"%(self.TcDatDir)

        self.TcClimoDatDir="%s/climo"%(self.TcDatDir)
        self.TcCarqDatDir="%s/carq"%(self.TcDatDir)
        self.TcNamesDatDir="%s/names"%(self.TcDatDir)

        # -- dirs for mdecks.pypdb (old style used by a/vdecks) using w2-tc-dss-mdeck.py
        #
        self.TcDatFinalDir=self.TcDatDir
        
        self.TcBtDatDir="%s/bt"%(self.TcDatFinalDir)
        self.TcAdecksFinalDir="%s/adeck"%(self.TcDatFinalDir)
        self.TcBdecksFinalDir="%s/bdeck"%(self.TcDatFinalDir)
        self.TcMdecksFinalDir="%s/mdeck"%(self.TcDatFinalDir)

        #self.TcStatusLogDir="%s/tcstatus"%(self.W2BaseDirLog)
        # -- use new fs for logs...
        self.TcStatusLogDir="%s/tcstatus"%(self.LocalBaseDirLog)

        self.TcAdeckLogDir="%s/adeck"%(self.W2BaseDirLog)
        self.TcBdeckLogDir="%s/bdeck"%(self.W2BaseDirLog)
        self.TcMdeckLogDir="%s/mdeck"%(self.W2BaseDirLog)

        self.TcTcbogDatDir="%s/tcbog"%(self.TcDatDir)

        self.TcTiggeDatDir="%s"%(self.TcDatDir)

#cccccccccccccccccccccccccccccccccccccccccccccccccc
# cira MTCSWA -- multi-platform tropical cyclone surface wind analysis
#
        self.TcMtcswaFtpServer='satepsanone.nesdis.noaa.gov'
        self.TcMtcswaFtpDatDir='MTCSWA'
        self.TcMtcswaFtpDatDir='pub/MTCSWA'
        self.TcMtcswaFtpLogin='ftp'
        self.TcMtcswaFtpPasswd="michael.fiorino"
        self.TcMtcswaDatDir="%s/cira/mtcswa"%(self.TcDatDir)

        self.TcMtcswa2FtpServer='satepsanone.nesdis.noaa.gov'
        self.TcMtcswa2FtpDatDir='pub/7day/MTCSWA/NC'
        self.TcMtcswa2FtpLogin='ftp'
        self.TcMtcswa2FtpPasswd="mfiorino@gmu.edu"
        self.TcMtcswa2DatDir="%s/cira/mtcswa2"%(self.TcDatDir)

        self.TcMtcswaLateFtpServer='rammftp.cira.colostate.edu'
        self.TcMtcswaLateFtpDatDir='knaff/MPSW_LATE'
        self.TcMtcswaLateFtpLogin='ftp'
        self.TcMtcswaLateFtpPasswd="michael.fiorino"
        self.TcMtcswaLateDatDir="%s/cira/mtcswa_Late"%(self.TcDatDir)

        self.TcDiagHttpServer='ruc.noaa.gov'
        self.TcDiagHttpDatDir='hfip/tcdiag'
        self.TcDiagHttpLocalDatDir="%s/tcdiag"%(self.TcDatDir)

        self.JtDiagHttpServer='ruc.noaa.gov'
        self.JtDiagHttpDatDir='hfip/jtdiag'
        self.JtDiagHttpLocalDatDir="%s/jtdiagDAT"%(self.TcDatDir)

        self.TcGenHttpServer='ruc.noaa.gov'
        self.TcGenHttpDatDir='hfip/tcgen'
        self.TcGenHttpLocalDatDir="%s/tcgen"%(self.TcDatDir)
# -- psd RR2 
#
        self.TcpsdRR2FtpServer='ftp.cdc.noaa.gov'
        self.TcpsdRR2FtpDatDir='/Projects/Reforecast2/TropicalCyclone2'
        self.TcpsdRR2FtpLogin='ftp'
        self.TcpsdRR2FtpPasswd="michael.fiorino"
        self.TcpsdRR2DatDir="%s/adeck/psdRR2"%(self.TcDatDir)
        

#
#  nhc web
#

        self.NhcHttpIntranetServerSkate='skate.nhc.noaa.gov'
        self.NhcHttpIntranetDocRootSkate='/www/mfiorino/public_html'
        self.NhcHttpuserSkate='mfiorino'

        self.DoDogfishRsync=1
        self.NhcHttpIntranetServerDogfish='dogfish.nhc.noaa.gov'
        self.NhcHttpIntranetDocRootDogfish='/data/www/html/mfiorino'
        self.NhcHttpuserDogfish='mfiorino'

#
#  jtwc web
#

        self.JtwcHttpIntranetServer='138.163.146.36'
        self.JtwcHttpIntranetDocRoot='/dat/nwp'
        self.JtwcHttpuser='fiorino'

        self.LocalHttpDocRoot='/Library/WebServer/Documents/'
        
        self.EsrlHttpIntranetDocRoot='%s/wxmap2/'%(self.HfipProducts)
        self.EsrlHttpIntranetDocRootFiorino='%s/hfip/fiorino'%(self.HfipProducts)
        

        self.TcAdecksEcmwfDirW3="%s/tc/tceps/ecmwf"%(self.EsrlHttpIntranetDocRootFiorino)
        self.TcAdecksuKmoDirW3="%s/tc/tceps/ukmo"%(self.EsrlHttpIntranetDocRootFiorino)
        self.TcAdecksNcepDirW3="%s/tc/tceps/ncep"%(self.EsrlHttpIntranetDocRootFiorino)
        self.TcAdecksJmaDirW3="%s/tc/tceps/jma"%(self.EsrlHttpIntranetDocRootFiorino)
        self.TcAdecksCmcDirW3="%s/tc/tceps/cmc"%(self.EsrlHttpIntranetDocRootFiorino)
        self.TcbogDirW3="%s/tc/tcvitals"%(self.EsrlHttpIntranetDocRootFiorino)
        self.TcbogMoDirW3="%s/tcbog"%(self.EsrlHttpIntranetDocRootFiorino)
        self.TcvitalsDirW3="%s/tc/tcvitals"%(self.EsrlHttpIntranetDocRootFiorino)
        self.TcBdecksDirW3="%s/tc/bdecks"%(self.EsrlHttpIntranetDocRootFiorino)
        self.TcAdecksDirW3="%s/tc/adecks"%(self.EsrlHttpIntranetDocRootFiorino)

        self.wxhWeb="%s/web"%(self.W2BaseDir)

        self.wxhWebPub="%s/wxmap2"%(self.HfipProducts)
        self.wxhWeba="/data/amb/projects/wxmap2a"
        self.wxhWebClm="%s/web_clm"%(self.W2BaseDirWeb)


# llnl
#
        self.LlnlFtpServer='tenki.llnl.gov'

# jtwc
#
        self.JtwcFtpserver='198.97.80.64'

# 20050126 - .64 turned off (wxamp0) on 20050124; change the new wxmap machine .60 (wxmap2)
#
        self.JtwcFtpserver='198.97.80.60'

# 200604 - use atcfarch@ftp://pzal  vice wxmap2
#
        self.JtwcPzalAtcfServer='205.85.40.24'
        self.JtwcPzalAtcfLogin='nhc'
        self.JtwcPzalAtcfPasswd="Hurricane2**4"

#JtwcPzalAtcfServer='pzal.npmoc.navy.mil'
#JtwcPzalAtcfLogin='fnmoc'
#JtwcPzalatcfPasswd='8tcf5t0rmZ'

#
# 20060215 -- reconfig firewall
# 20060411 -- go with wxmap2 until pzal sorted
#
        self.jtserv='https'
        
#jtserv='ftp'

        if(self.jtserv == 'ftp'):

            self.JtwcFtpserver='pzal.npmoc.navy.mil'
            self.JtwcLogin='atcfarch'
            self.JtwcPasswd='HAwA1150'
            self.JtwcDatDir='/storms'

            self.JtwcService='ftp'
            self.JtwcFtpserver='199.10.200.62'
            self.JtwcLogin='fiorino'
            self.JtwcPasswd='tcad94'
            self.JtwcDatDir='/dat/nwp/dat/tc/jtwc'

        else:

            self.JtwcService='https'

            self.JtwcFtpserver='pzal.nmci.navy.mil'
            self.JtwcFtpserver='pzal.ndbc.noaa.gov'
            self.JtwcLogin='atcfarch'
            self.JtwcPasswd='HAwA1150'
            self.JtwcPasswd='fiorino:[TcaD94]{2011}'
            self.JtwcPasswdFnmoc='fnmoc:8tcf5t0rm'
            self.JtwcDatDir='/storms'

            # -- 20190401 -- new collab server
            self.JtwcFtpserver='pzal.metoc.navy.mil'

            self.JtwcLogin='fnmoc'
            self.JtwcPasswdFnmoc='&XVp4mndcb+dMmT' # latest one I tried
            self.JtwcPasswdFnmoc='l~Kst35(gqxA*6d' # changed 20190716
            self.JtwcPasswdFnmoc='9i9S@XU^kqoFj5' # changed 20201106

            self.JtwcLogin='tenkiman' # my own login approved 20201110
            self.JtwcPasswdFnmoc='s9a!LvtJjHPZ~Zr' # set 20201110
            self.JtwcPasswdFnmoc='gZ1*3n2$52M9go'
            self.JtwcPasswdFnmoc='qIpy28zMYOmFx!'
            self.JtwcPasswdFnmoc='C6v2jt(9wIJOSb'

            self.JtwcLogin='tenkiman' # my own login approved 20201110
            self.JtwcPasswd='6Da283305(dquX'  # 20210902 -- new passwd after jtwc using -U 'moz'
            self.JtwcPasswd='8dc)E!IG#clxJL4'  # 20210913 -- new passwd  annual'
            
            self.JtwcDatDir='/php/m2m/index.php/atcf_storms'
            self.JtwcDatDir='/php/rds/m2m/index.php/atcf_storms'


        self.PushTcstruct2Pzal=0

# -- kerry emanuel chips model

        self.MitFtpserver='texmex.mit.edu'
        self.MitLogin='ftp'
        self.MitPasswd='michael.fiorino@noaa.gov'
        self.MitDatDir='/pub/emanuel/JTWC'

# -- nhc
#

        self.NhcService='ftp'
        self.NhcFtpserver='ftp.tpc.ncep.noaa.gov'
        self.NhcFtpserver='ftp.nhc.noaa.gov'

# -- shifted back to this on 20120322
#        self.NhcFtpserver='ftp.nhc.noaa.gov'

        self.NhcLogin='ftp'
        self.NhcPasswd='michael.fiorino@noaa.gov'
        self.NhcDatDir='/pub/atcf'
        self.NhcDatDir='/atcf'
        self.NhcLocalAtcfDatDir='/mnt/users/atcf'

#-- ucar
#

        self.HfipFtpserver='ftp.rap.ucar.edu'
        self.HfipLogin='ftp'
        self.HfipPasswd='michael.fiorino@noaa.gov'
        self.HfipLogin='hfipteam'
        self.HfipPasswd='hfipteam'
        self.HfipDatDir='/incoming/irap/hfip'

        self.HfipLocalAtcfDatDir='/mnt/users/atcf'

        self.HrdFtpserver='ftp.aoml.noaa.gov'
        self.HrdLogin='ftp'
        self.HrdPasswd='fiorino@llnl.gov'
        self.HrdDatDir='/pub/hrd/gopal/tracks'
        self.HrdHwindDatDir='/pub/hrd/hwind/carq/Operational'

        self.EcmwfTiggeFtpserver='tigge-ldm.ecmwf.int'
        self.EcmwfTiggeLogin='tigge'
        self.EcmwfTiggePasswd='tigge'
        self.EcmwfTiggeDatDir='/cxml'

        self.EcmwfWmoFtpserver='dissemination.ecmwf.int'
        # -- 20221018 -- because of data move to bologna
        self.EcmwfWmoFtpserver='diss.ecmwf.int'
        self.EcmwfWmoLogin='wmo'
        self.EcmwfWmoPasswd='essential'

        self.uKmoTiggeFtpserver='ftp.metoffice.gov.uk'
        # -- 20180505 -- ukmo login/passwd moved to .netrc -- using new long mf_tropc
        self.uKmoTiggeDatDir='.'

        useJpeng=1
        useJpeng=0
        self.useJpeng=useJpeng
        
        if(useJpeng):
            
            self.NcepTiggeFtpserver='ftp.emc.ncep.noaa.gov'
            self.NcepTiggeLogin='ftp'
            self.NcepTiggePasswd='michael.fiorino@noaa.gov'
            self.NcepTiggePasswd='mike'
        
            #self.NcepTiggeDatDir='/gmb/rwobus/tigge/beta/cxml' -- deprecated at ncep 2013073100
            self.NcepTiggeDatDir='/gc_wmb/jpeng/cxml'
            # -- changed 20130807 above stopped on 2013073118
            self.NcepTiggeDatDir='/gc_wmb/jpeng/cxml'
        
        else:
            
            self.NcepTiggeFtpserver='ftp.ncep.noaa.gov'
            self.NcepTiggeLogin='ftp'
            self.NcepTiggePasswd='michael.fiorino@noaa.gov'
            self.NcepTiggePasswd='mike'
            self.NcepTiggeDatDir='/pub/data/nccf/com/ens_tracker/prod'
            

        self.CmcTiggeFtpserver=self.NcepTiggeFtpserver
        self.CmcTiggeLogin=self.NcepTiggeLogin
        self.CmcTiggePasswd=self.NcepTiggePasswd
        self.CmcTiggeDatDir=self.NcepTiggeDatDir

# set on kishou by su
#
        self.NhcLocalAtcfDatDir='/atcf'

        self.NhcLocalAtcfOpsDatDir='/home/mfiorino/databases/atcf/storms'
        self.NhcLocalAtcfOpsDatabaseDir='/home/mfiorino/databases/atcf/atcfdatabase'
        self.NhcLocalAtcfOpsDatArchiveDir='/home/mfiorino/databases/atcf/archive'

# jtwc -- rsync mech to do a/b decks vice wget to pzal.nmci.navy.mil
#

        self.JtwcWxmap2AtcfDatDir='/dat/nwp/dat/tc/jtwc'

# 20110713 -- nfs from wxmap1 -> 2 machine
#
        self.JtwcWxmap2AtcfDatDir='/dat/rdata/tc/jtwc'
        self.JtwcWxmap2AtcfEcmwfDatDir='/dat/nwp/dat/tc/ecmwf'

# -- jma
#
        self.JmaFtpserver='ddb.kishou.go.jp'
        self.JmaIdir='/dat/nwp/dat'


# -- fnmoc
#
        self.FnmocCagipsGridCacheDir='/gpfs6/cagips/cache/fnmoc/grid'
        self.FnmocCagipsGridLocalDir='/home/dlaws/cagips_data'

#  nhc - cagips
#
        self.NhcCagipsGridCacheDir='/gpfs6/cagips/cache/fnmoc/grid'
        self.NhcCagipsGridLocalDir='/home/mfiorino/dat/cagips'

#  nhc - nawips
#
        self.NhcNawipsGridCacheDir='/gpfs6/cagips/cache/fnmoc/grid'
        self.NhcNawipsGridLocalDir='/mnt/model'
        self.NhcNawipsGridLocalDir='/model'
        self.NhcNawipsGridArchDir='/mnt/data_arch'
        self.NhcNawipsGridArchTmpDir='/storage/data_arch'

# nhc -- model flds
#
        self.NhcFldArchiveBase='/storage/dat/nwp'

# 20081202 -- shift to snap drives to disconnect local usb2 drives...
#
        self.NhcFldArchiveBase='/storage3/dat/nwp'
        self.NhcFldLiveBase='/storage2/nwp2'
#--------- 20070823 -- cut over to new snap drive
        self.NhcFldLiveBase="%s/nwp2"%(self.W2BaseDirDat)

# nhc - ftp dirs
# nhc - nco
#
        self.NcoDcomDir='/dcom/us007003'
        self.NcoGridLocalDir='/mnt/model'
        self.NcoGridArchDir='/mnt/data_arch'

#  nhc - ukmo 
#
        self.NhcFtpIncominguKmo='/users/naprod/model/ukmet_hr/downloads'
        self.NhcFtpIncominguKmo='mfiorino@compute1:/home/naprod/model/ukmet_hr/downloads'
        self.NhcTargetuKmo=self.NhcFldLiveBase+'/ukmo/ukm'

#  nhc - cpc qmorph rain 
#
        self.PrDatRoot="%s/pr"%(self.W2BaseDirDat)
        self.PrCV10DatRoot="%s/pr/cmorph-v10"%(self.W2BaseDirDat)

        
        self.CpcFtpQmorphServer='ftp.cpc.ncep.noaa.gov'
        self.CpcFtpSourceDirQmorph='/precip/qmorph/30min_025deg/'
        #self.CpcFtpSourceDirQmorph='/precip/CMORPH_V0.x_RT/RAW/0.25deg-30min/'

        self.NhcFtpTargetDirQmorph='%s/qmorph/30min_025deg/incoming'%(self.PrDatRoot)
        self.NhcQmorphFinalLocal='%s/qmorph/30min_025deg/grib'%(self.PrDatRoot)
        self.NhcQmorphProductsGrib='%s/model/pr_qmorph/grib'%(self.PrDatRoot)

        self.NhcQmorphFinalSnap='/storage3/dat/qmorph/30min_025deg/grib/'
        self.NhcQmorphProductsGempak='/dat1/model/pr_qmorph/'
        self.NhcQmorphProductsGempakNawips='/model/pr_qmorph/'

        self.CpcFtpCmorphServer=self.CpcFtpQmorphServer
        self.CpcFtpSourceDirCmorph='/precip/global_CMORPH/30min_025deg/'
        #self.CpcFtpSourceDirCmorph='/precip/CMORPH_V0.x/RAW/30min_025deg/'




# 20090605 -- tmp location for recovered cmorph gap 200905007-20090521
#
#CpcFtpSourceDirCmorph='/precip/qmorph/30min_025deg/'

        self.NhcFtpTargetDirCmorph='%s/cmorph/30min_025deg/incoming'%(self.PrDatRoot)
        self.NhcCmorphFinalLocal='%s/cmorph/30min_025deg/grib'%(self.PrDatRoot)
        self.NhcCmorphProductsGrib='%s/model/pr_cmorph/grib'%(self.PrDatRoot)

        self.NhcCmorphFinalSnap='/storage3/dat/cmorph/30min_025deg/grib/'
        self.NhcCmorphProductsGempak='/dat1/model/pr_cmorph/'

        # -- 20221129 gsmap dirs
        #
        self.PrGsmapDatRoot="%s/pr/gsmap"%(self.W2BaseDirDat)
        self.PrGsmapV6DatRoot="%s/pr/gsmapV6"%(self.W2BaseDirDat)
        self.PrGsmapV6GDatRoot="%s/pr/gsmapV6-Grev"%(self.W2BaseDirDat)
        
        self.PrGsmapProducts='%s/pr/model/pr_gsmap'%(self.W2BaseDirDat)
        self.PrGsmapV6Products='%s/pr/model/pr_gsmapV6'%(self.W2BaseDirDat)
        self.PrGsmapV6GProducts='%s/pr/model/pr_gsmapV6-Grev'%(self.W2BaseDirDat)

        self.PrGsmapProductsGrib='%s/grib'%(self.PrGsmapProducts)
        self.PrGsmapV6ProductsGrib='%s/grib'%(self.PrGsmapV6Products)
        self.PrGsmapV6GProductsGrib='%s/grib'%(self.PrGsmapV6GProducts)

        # -- 20230214 -- product for superBT

        self.PrGsmapV6GProducts='%s/pr/pr_gsmapV6-Grev'%(self.W2BaseDirDat)
        self.PrCmorphV10Products='%s/pr/pr_cmorph-v10'%(self.W2BaseDirDat)
        self.PrCmorphVX0Products='%s/pr/pr_cmorph'%(self.W2BaseDirDat)
        self.PrImergV06Products='%s/pr/pr_imerg'%(self.W2BaseDirDat)


    def setNcepTCepsSource(self,useJpeng=0):
        
        self.useJpeng=useJpeng
        
        if(useJpeng):
            
            self.NcepTiggeFtpserver='ftp.emc.ncep.noaa.gov'
            self.NcepTiggeLogin='ftp'
            self.NcepTiggePasswd='michael.fiorino@noaa.gov'
            self.NcepTiggePasswd='mike'
        
            #self.NcepTiggeDatDir='/gmb/rwobus/tigge/beta/cxml' -- deprecated at ncep 2013073100
            self.NcepTiggeDatDir='/gc_wmb/jpeng/cxml'
            # -- changed 20130807 above stopped on 2013073118
            self.NcepTiggeDatDir='/gc_wmb/jpeng/cxml'
        
        else:
            
            self.NcepTiggeFtpserver='ftp.ncep.noaa.gov'
            self.NcepTiggeLogin='ftp'
            self.NcepTiggePasswd='michael.fiorino@noaa.gov'
            self.NcepTiggePasswd='mike'
            self.NcepTiggeDatDir='/pub/data/nccf/com/ens_tracker/prod'
            

        self.CmcTiggeFtpserver=self.NcepTiggeFtpserver
        self.CmcTiggeLogin=self.NcepTiggeLogin
        self.CmcTiggePasswd=self.NcepTiggePasswd
        self.CmcTiggeDatDir=self.NcepTiggeDatDir
        


    def getTausFromTauopt(self,tauopt,taui=6):
        
        taus=[]
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
    
            for tau in range(taub,taue+1,taui):
                taus.append(tau)
    
        return(taus)
    
    def getL2ModelStatus(self,model,l2opt,dtg,bdir2=None,verb=0,override=0):
        
        from M2 import setModel2
        
        lsext=''
        doarchive=0
        m=setModel2(model,bdir2=bdir2)
        dmodelType=None
        if(l2opt == '-W'): dmodelType='w2flds'
        m.dtype=dmodelType
        
        if(dmodelType != None):         m.bddir="%s/%s/dat/%s"%(m.bdir2,'w2flds',model)
        if(hasattr(m,'setxwgribNwp2')): m.setxwgrib=m.setxwgribNwp2
        fm=m.DataPath(dtg,dtype=dmodelType,dowgribinv=1,override=override,doDATage=1)
        fd=fm.GetDataStatus(dtg)

        # -- get the ddtg which might not be the same as the dtg path because we allow return +6 h for 00/12Z models
        #
        ddtg=fd.ddtgs[0]
        # -- always show the data dir
        #
        lsext="%s/%s"%(m.bddir,dtg)
        longls=0
        badage=0
        didprint=0
        
        if(len(fm.datpaths) > 0):
            itaus=fm.dsitaus
    
            if(fd.dslatestCompleteTauBackward > 0):
                tau=fd.dslatestCompleteTauBackward
            else:
                tau=fd.dslatestCompleteTau
    
            taus=[tau]
            if(longls == 1):
                taus=itaus
    
            # -- logic for handling 'alltau' models, e.g., ukm2
            #
            statussTaus=fm.statuss[dtg].keys()
    
            otau=tau
            itaus=taus
    
            if(len(statussTaus) == 1):  itaus=[statussTaus[0]]
            if(len(statussTaus) == 0):  
                itaus=[]                        
                tau=999
                age=999.9
                nf=0
                prefix='Z-'
                card="%-6s %s%s  %03d   %7.2f  %4d <--- NO/ZERO DATA localdir: %s"%(model,prefix,ddtg,tau,age,nf,fd.dstdir)
                if(verb): print card
                
                didprint=1
    
            ostat=statussTaus
            ostat.sort()
            for itau in itaus:
                prefix='  '
    
                (age,nf)=fm.statuss[dtg][itau]
                if(age == None):
    
                    tau=999
                    age=999.9
                    nf=0
                    if(not(doarchive)):
                        prefix='N-'
                        card="%-6s %s%s   %03d   %7.2f  %4d <--- NOOOO DATA because data are ln -s localdir: %s"%\
                              (model,prefix,ddtg,tau,age,nf,fd.dstdir)
                        if(verb): print card
                        didprint=1
                        continue
                    
                # -- use the tau from above unless more than 1 tau
                #
                if(len(itaus) > 1): otau=itau
                olsext=lsext
                if(nf < fm.nfields or itau < m.etau): 
                    prefix='L-'
                    olsext="%s <--- low data count nfields: %d"%(lsext,fm.nfields)
                card="%-6s %s%s  %03d   %7.2f  %4d %s"%(model,prefix,ddtg,otau,age,nf,olsext)
                # -- case of 0 taus -- not enougth
                if(itau == 0): 
                    prefix='0-'
                    olsext="%s <--- 000 -- incomplete run insufficent taus"%(lsext)
                card="%-6s %s%s  %03d   %7.2f  %4d %s"%(model,prefix,ddtg,otau,age,nf,olsext)
                if(verb): print 'cccc---',card
                didprint=1
    
        else:
            tau=999
            age=999.9
            nf=0
    
        if((not(doarchive) and nf == 0 and not(didprint)) or badage):
            if(badage): age=-888.8
            card="%-6s N-%s  %03d   %7.2f  %4d <--- NO DATA localdir: %s"%(model,dtg,tau,age,nf,fd.dstdir)
            if(verb): print card
            
        return(card)





#wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww22222222222222222222222222222222222
# from w2.py methods



    def is0012Z(self,dtg):
        rc=0
        if(dtg[8:10] == '00' or dtg[8:10] == '12'): rc=1
        return(rc)


    def is0618Z(self,dtg):
        rc=0
        if(dtg[8:10] == '06' or dtg[8:10] == '18'): rc=1
        return(rc)
    
    def IsOffTime(self,dtg):
        dtghh=int(dtg[8:10])
        if(dtghh == 6 or dtghh == 18):
            return(1)
        else:
            return(0)


    def getModelBaseName(self,imodel):

        ttp=imodel.split('.')
        ttd=imodel.split('_')
        if(len(ttp) > 1):
            model=ttp[0]
        elif(len(ttd) > 1):
            model=ttd[0]
        else:
            model=imodel

        lm=len(model)
        try:
            nm=int(model[lm-2:lm])
        except:
            nm=-999

        if(model[-1] == 'j' or model[-1] == 'k'):
            mbase=model[0:-1]
        elif(lm == 5 and nm >= 0):
            mbase=model[0:3]
        elif(lm == 4):
            mbase=model[0:4]
        elif(lm >= 5 and nm != -999):
            mbase=model[0:4]
        elif(lm >= 5 and nm == -999):
            mbase=model
        else:
            mbase=model[0:3]

        return(mbase)


    def GetModelsFromModopt(self,modopt):

        tt=modopt.split('.')
        if(len(tt) >= 2):
            models=tt
            nmodels=len(tt)
        elif(len(tt) == 1):
            models=[modopt]
            nmodels=1
        else:
            print 'EEEE w2.GetModelsFromModopt :: invalid modopt: ',modopt
            sys.exit()

        return(models)


    def GetLogLatest(self,type,dtg):

        masktype=type
        if(type == 'tcstatus'):
            masktype='tc'

        logdir="%s/%s/%s"%(self.W2BaseDirLog,type,dtg)
        logs=glob.glob("%s/%s.*"%(logdir,masktype))
        ocards={}
        cards=[]

        if(len(logs) == 0):
            #
            # go back -6 h
            #
            dtgm6=mf.dtginc(dtg,-6)
            print 'LLLLL going back -6 h from: ',dtg,' to ',dtgm6
            logdir="%s/%s/%s"%(self.W2BaseDirLog,type,dtgm6)
            logs=glob.glob("%s/%s.*"%(logdir,masktype))

        if(len(logs) > 0):
            logs.sort()
            for log in logs:
                cards=open(log).readlines()
                for card in cards:
                    file=card.split()[0]
                    ocards[file]=card

            files=ocards.keys()
            files.sort()

            for file in files:
                cards.append(ocards[file])

        else:
            cards=None

        return(cards)


    def GetLatestTcStatusLog(self,dtg):

        type='tcstatus'
        masktype='tc'

        logdir="%s/%s/%s"%(self.W2BaseDirLog,type,dtg)
        logs=glob.glob("%s/%s.*"%(logdir,masktype))
        ocards={}
        cards=[]

        if(len(logs) == 0):
            #
            # go back -6 h
            #
            dtgm6=mf.dtginc(dtg,-6)
            print 'LLLLL going back -6 h from: ',dtg,' to ',dtgm6
            logdir="%s/%s/%s"%(self.W2BaseDirLog,type,dtgm6)
            logs=glob.glob("%s/%s.*"%(logdir,masktype))

        if(len(logs) > 0):
            logs.sort()
            logfile=logs[-1]
            print 'lllll ',logfile
            cards=open(logfile).readlines()

        else:
            cards=None

        return(cards)


    def GetSynHour(self,dtg):
        hh=synhour=dtg[8:]
        ihh=int(hh)
        return(hh,ihh)


    def cpTcvitals(self,dtgs,ropt='',verb=0):

        if(ropt == 'norun'):
            print 'CCC:--- running w2.cpTcvitals()'
            return

        from types import ListType

        tvdir="%s/tc/tcvitals"%(self.W2BaseDirDat)
        tdssdir="%s/tc/DSs"%(self.W2BaseDirDat)

        w3tdir=self.TcvitalsDirW3

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
                cmd="scp %s %s@%s:%s/."%(tvpath,self.WjetScpServerLogin,self.WjetScpServer,self.WjetTcvitals)
                mf.runcmd(cmd,ropt)

            if(W2doW3Rapb):
                cmd="cp %s  %s/."%(tvpath,w3tdir)
                mf.runcmd(cmd,ropt)


        return

    def cpReftrk2W3(self,dtgs,ropt='',verb=0):

        if(ropt == 'norun'):
            print 'CCC:--- running w2.cpReftrkW3()'
            return

        from types import ListType

        w3tdir=self.TcvitalsDirW3
        if( not(type(dtgs) is ListType) ):
            dtgs=[dtgs]

        for dtg in dtgs:
            year=dtg[0:4]
            sdir="%s/%s"%(self.TcRefTrkDatDir,year)
            if(self.W2doW3Rapb):
                cmd="cp -p %s/*%s* %s/."%(sdir,dtg,w3tdir)
                mf.runcmd(cmd,ropt)
            if(self.W2doWjet):
                cmd="scp %s/*%s* %s@%s:/lfs1/projects/rtfim/tcvitals/."%(sdir,dtg,self.WjetScpServerLogin,self.WjetScpServer)
                mf.runcmd(cmd,ropt)

        return


    def cpNcepAdecks2Jet(self,dtg,ropt='',verb=0):

        if(ropt == 'norun'):
            print 'CCC:--- running w2.cpNcepAdecks2Jet()'
            return

        year=dtg[0:4]
        spath="%s/%s/tracks.atcfunix.%s"%(self.TcAdecksNcepDir,year,year[2:4])
        cmd="scp %s %s@%s:%s/adeck/ncep/."%(spath,self.WjetScpServerLogin,self.WjetScpServer,self.WjetTcDatDir)
        mf.runcmd(cmd,ropt)

        return


    def cpBdecks2W3(self,dtgopt,ropt='',verb=0):

        if(ropt == 'norun'):
            print 'CCC:--- running w2.cpBdecks2W3()'
            return

        from tcCL import Bdeck

        b=Bdeck(dtgopt=dtgopt,verb=verb)
        w3tdir=self.TcBdecksDirW3

        bdtgs=b.dtgs
        stmids=b.curbdecks.keys()

        bdtgs.sort()
        stmids.sort()

        for bdtg in bdtgs:
            for stmid in stmids:
                bdeck=b.curbdecks[stmid]
                (dir,file)=os.path.split(bdeck)
                tpath="%s/%s.%s"%(w3tdir,bdtg,file)

                cmd="cp -p %s %s"%(bdeck,tpath)
                mf.runcmd(cmd,ropt)

                cmd="cp -p %s %s/."%(bdeck,w3tdir)
                mf.runcmd(cmd,ropt)

        return



    # --- mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm model2 metods

    def Model2DdtgData(self,model,dtghh=''):

        ddtg=None

        if(model == 'gfs2' or model == 'goes'): ddtg=6
        if(model == 'fim8' or model == 'fv3e' or model == 'fv3g'): ddtg=12
        if(model == 'fimx'): ddtg=12
        if(model == 'ngp2'): ddtg=12

        if(model == 'ngpc' or model == 'ngpj'): ddtg=12
        if(model == 'navg'): ddtg=12
        if(model == 'gfsc'): ddtg=6
        if(model == 'ukmc'): ddtg=12
        if(model == 'jmac'): ddtg=12
        if(model == 'gfsn'): ddtg=6

        if(model == 'ecm2'): ddtg=12
        if(model == 'ecm4'): ddtg=12
        if(model == 'ecm5' or model == 'era5' or model == 'cgd2'): ddtg=12
        if(model == 'jgsm'): ddtg=6
        if(model == 'gfsk'): ddtg=6
        if(model == 'ecmn'): ddtg=12
        if(model == 'ecmg'): ddtg=12
        if(model == 'ukm2'): ddtg=6
        if(model == 'cmc2'): ddtg=12

        if(model == 'ocn'):  dtau=24
        if(model == 'ohc'):  dtau=12
        if(model == 'ww3'):  dtau=12


        return(ddtg)



    def Model2EtauData(self,model,dtghh=999):

        etau=None

        dtghh=int(dtghh)

        if(model == 'gfs' or model == 'goes'): etau=144
        if(model == 'ngp'): etau=144
        if(model == 'ngp05'): etau=144

        if(model == 'ecm'): etau=144
        if(model == 'cmc'): etau=144
        if(model == 'ocn'): etau=0
        if(model == 'ohc'): etau=0
        if(model == 'ww3'): etau=180

        if(model == 'gfs2'): etau=180
        if(model == 'ngp2'): etau=144

        if(model == 'ngpc' or model == 'ngpj'): etau=180
        if(model == 'navg'): etau=180

        if(model == 'gfsc'): etau=180
        if(model == 'gfsn'): etau=180

        if(model == 'ukmc'):
            if(dtghh == 0 or dtghh == 12):
                etau=120
            elif(dtghh == 6 or dtghh == 18):
                etau=0

        if(model == 'jmac'):
            if(dtghh == 12):
                etau=168
            elif(dtghh == 0):
                etau=84

        if(model == 'ecm2'): etau=240
        if(model == 'ecm4'): etau=240
        if(model == 'ecm5' or model == 'era5' or model == 'cgd2'): etau=240
        
        if(model == 'jgsm'): etau=132
        
        if(model == 'gfsk'): etau=168
        if(model == 'gfsr' or model == 'gfr1'): etau=168
        if(model == 'ecmn'): etau=240
        if(model == 'ecmg'): etau=240

        if(model == 'ukm2' or model == 'ukm'):
            if(dtghh == 0 or dtghh == 12):
                etau=144
            elif(dtghh == 6 or dtghh == 18):
                etau=60

        if(model == 'cmc2'):
            if(dtghh == 0):
                etau=180
            elif(dtghh == 12):
                etau=144
            else:
                etau=None

        if(model == 'cgd6'):
            if(dtghh == 0):
                etau=240
            elif(dtghh == 12):
                etau=144
            else:
                etau=None

        if(model == 'cgd2'):
            if(dtghh == 0):
                etau=240
            elif(dtghh == 12):
                etau=144
            else:
                etau=None


        if(model == 'fim8' or model == 'fim9' or model == 'fimx' or
           model == 'fv3e' or model == 'fv3g'):
            etau=168

        return(etau)



    def Model2DtauData(self,model,dtghh=''):

        if(model == 'gfs2' or model == 'goes'): dtau=6
        if(model == 'gfsr' or model == 'gfr1'): dtau=6
        if(model == 'fim8' or model == 'fv3e' or model == 'fv3g'): dtau=6
        if(model == 'fimx'): dtau=6
        if(model == 'ngp2'): dtau=6

        if(model == 'ngpc' or model == 'ngpj'): dtau=6
        if(model == 'navg'): dtau=6
        if(model == 'ukmc'): dtau=6
        if(model == 'gfsc'): dtau=6
        if(model == 'jmac'): dtau=6
        if(model == 'gfsn'): dtau=6

        if(model == 'ocn'):  dtau=6
        if(model == 'ohc'):  dtau=6
        if(model == 'ww3'):  dtau=6
        if(model == 'ecm2'): dtau=6
        if(model == 'ecm4'): dtau=6
        if(model == 'ecm5' or model == 'era5' or model == 'cgd2'): dtau=6
        if(model == 'jgsm'): dtau=6
        if(model == 'gfsk'): dtau=6
        if(model == 'ecmn'): dtau=6
        if(model == 'ecmg'): dtau=24
        if(model == 'ukm2'): dtau=6
        if(model == 'cmc2'): dtau=6

        return(dtau)


    def Model2DataTaus(self,model,dtg):

        dtghh=int(dtg[8:10])
        
        from M2 import setModel2
        m=setModel2(model)

        etau=None
        dtau=None

        # -- more agressive use of M2
        #
        if(m != None):
            
            # -- ukm2 and navg have a getDataTaus methods
            #
            if(hasattr(m,'getDataTaus')): 
                taus=m.getDataTaus(dtg)
                
            elif(hasattr(m,'dattaus')): 
                taus=m.dattaus
            else:
                etau=m.getEtau(dtg=dtg)
                dtau=m.getDtau(dtg=dtg)
                taus=range(0,etau+1,dtau)
            return(taus)

        taus=[]

        if(model == 'gfs2' or model == 'fim8' or model == 'fimx' or 
           model == 'gfsr' or model == 'gfr1' or model == 'gfsk' or
           model == 'ecm2' or model == 'ecm4' or 
           model == 'cmc2' or model == 'cgd6' or model == 'cgd2' or
           model == 'ocn' or model == 'ohc' or model == 'ww3' or
           model == 'ecmg' or
           model == 'ngpc' or model == 'ngpj' or
           model == 'navg' or
           model == 'jgsm' or
           model == 'gfsc' or model == 'goes' 
           ):
            if(etau == None):
                etau=self.Model2EtauData(model,dtghh)
                dtau=self.Model2DtauData(model,dtghh)

            if(etau != None):
                taus=range(0,etau+1,dtau)
            else:
                taus=[]

        # -- special cases
        #
        elif(model == 'ukm2' or model == 'ngp2' ):
            if(dtghh == 0 or dtghh == 12):
                taus=range(0,72+1,6)+range(84,144+1,12)
            elif(dtghh == 6 or dtghh == 18):
                taus=range(0,60+1,6)

        elif(model == 'ukmc'):
            if(dtghh == 12):
                taus=range(0,72+1,6)+range(84,120+1,12)
            elif(dtghh == 0):
                taus=range(0,72+1,6)+range(84,120+1,12)
            else:
                taus=[]


        # -- nws ecmwf
        #
        elif(model == 'ecmn'):
            taus=range(0,48+1,6)+range(48,240+1,12)

        elif(model == 'jmac'):
            if(dtghh == 12):
                taus=range(0,72+1,6)+range(84,168+1,12)
            elif(dtghh == 0):
                taus=range(0,72+1,6)+range(84,84+1,12)
            else:
                taus=[]

        elif(model == 'gfsn'):
            etau=Model2EtauData(model,dtghh)
            dtau=Model2DtauData(model,dtghh)
            if(etau != None):
                taus=range(0,etau+1,dtau)
            else:
                taus=[]



        else:
            print 'EEE invalid model w2.Model2DataTaus: ',model
            sys.exit()


        return(taus)

    
    def Model2CtlPath(self,model,dtg,ctltype=0,doarchive=0):

        if(doarchive == 1):
            ctldir="%s/w2flds/dat/%s/%s"%(self.Nwp2DataBdir,model,dtg)
            if(model == 'ecm5' or model == 'jgsm'):
                ctldir="%s/w2flds/dat/%s/%s/%s"%(self.Nwp2DataBdir,model,dtg[0:4],dtg)
                
        else:
            ctldir="%s/%s"%(self.Nwp2DataBdirModel(model),dtg)

        if(ctltype != 0 and doarchive != 1):
            ctlmask="%s/*.%s.%s.ctl"%(ctldir,dtg,ctltype)
        else:
            ctlmask="%s/*.%s.ctl"%(ctldir,dtg)
            if(model == 'ecm5'):
                ctlmask="%s/*%s*ua.ctl"%(ctldir,dtg)
            if(model == 'jgsm'):
                ctlmask="%s/*%s*.ctl"%(ctldir,dtg)

        if( (doarchive > 0) and (model == 'fim8' or model == 'gfs2') ):
            ctlmask="%s/*%s*.%s.ctl"%(ctldir,model,dtg)

        if(model == 'fimx' ):
            ctldir='/w21/dat/nwp2/rtfim/dat/FIMX/%s'%(dtg)
            ctlmask="%s/fim8.FIMX.grb2.ctl"%(ctldir)

        ctlpaths=glob.glob(ctlmask)


        if(len(ctlpaths) == 0):
            ctlpath=None
        else:
            ctlpath=ctlpaths[0]

        return(ctlpath)


    def Model2LocalArchivePaths(self,model,dtg):

        yyyymm=dtg[0:6]

        localpaths=[]
        localarchpaths=[]

        if(model == 'gfs2'):
            ctlfile="gfs2.%s.ctl"%(dtg)

        elif(model == 'fim8'):
            ctlfile="fim8.*%s.ctl"%(dtg)

        elif(model == 'fimx'):
            ctlfile="%s/fim8.FIMX.grb2.ctl"%(dtg)

        elif(model == 'ngp2'):
            ctlfile="ngp.*%s.ctl"%(dtg)

        elif(model == 'ngpc'):
            ctlfile="ngpc.*%s.ctl"%(dtg)

        elif(model == 'navg'):
            ctlfile="navg.*%s.ctl"%(dtg)

        elif(model == 'ngpj'):
            ctlfile="ngpj.*%s.ctl"%(dtg)

        elif(model == 'gfsc'):
            ctlfile="gfsc.%s.*"%(dtg)

        elif(model == 'ukmc'):
            ctlfile="cmc.%s.*"%(dtg)

        elif(model == 'jmac'):
            ctlfile="jmac.%s.*"%(dtg)

        elif(model == 'ukm2'):
            ctlfile="ukm.%s.ctl"%(dtg)

        elif(model == 'ecm2'):
            ctlfile="ecmo.%s.*"%(dtg)

        elif(model == 'ecm4'):
            ctlfile="%s.%s.*"%(model,dtg)

        elif(model == 'ecm5' or model == 'era5'):
            ctlfile="%s-w2flds-%s-ua.*"%(model,dtg)

        elif(model == 'jgsm'):
            ctlfile="%s.w2flds.%s.*"%(model,dtg)

        elif(model == 'cgd2'):
            ctlfile="%s.%s.*"%(model,dtg)

        elif(model == 'gfsk'):
            ctlfile="gfsk.%s.*"%(dtg)

        elif(model == 'ecmn'):
            ctlfile="ecmn.%s.*"%(dtg)

        elif(model == 'ecmg'):
            ctlfile="ecmg.%s.*"%(dtg)

        elif(model == 'cmc2'):
            ctlfile="cmc.%s.*"%(dtg)


        localdir=self.Nwp2DataBdirModel(model)
        localpath="%s/%s/%s"%(localdir,dtg,ctlfile)
        print 'llll ',localpath
        localpaths.append(localpath)

        archsources=['local','local10','snap']
        for archsource in archsources:
            localarchbase=self.Model2ArchiveDir(yyyymm,source=archsource)
            localarchdir=self.Nwp2DataBdirModel(model,bdir2=localarchbase)
            localarchpath="%s/%s/%s"%(localarchdir,dtg,ctlfile)
            localarchpaths.append(localarchpath)

        return(localpaths,localarchpaths)


    def Model2ArchiveDir(self,yyyymm,source='local',dtg=None):

        if(source == 'local'):
            archdir=self.Nwp2DataArchiveBdirLocal
        elif(source == 'local10'):
            archdir=self.Nwp2DataArchiveBdirLocal10
        elif(source == 'snap'):
            archdir=self.Nwp2DataArchiveBdirSnap
        else:
            print 'EEE invalid (w2.py) model2 archive source: ',source
            sys.exit()

        archdir="%s/%s"%(archdir,yyyymm)

        return(archdir)


    def Model2Model2TcModel(self,model):

        if(model == 'gfs2'):
            tcmodel='gfs2'
            
        elif(model == 'fim8'):
            tcmodel='fim8'

        elif(model == 'fimx'):
            tcmodel='fimx'

        elif(model == 'ngp2'):
            tcmodel='ngp2'

        elif(model == 'ngpc'):
            tcmodel='ngpc'

        elif(model == 'navg'):
            tcmodel='navg'

        elif(model == 'ngpj'):
            tcmodel='ngpj'

        elif(model == 'gfsc'):
            tcmodel=model

        elif(model == 'ukmc'):
            tcmodel=model

        elif(model == 'jmac'):
            tcmodel=model

        elif(model == 'ecm2'):
            tcmodel=model

        elif(model == 'ecm4'):
            tcmodel=model

        elif(model == 'ecm5' or model == 'era5' or model == 'cgd2'):
            tcmodel=model

        elif(model == 'jgsm'):
            tcmodel=model

        elif(model == 'gfsk'):
            tcmodel='gfsk'

        elif(model == 'ecmn'):
            tcmodel='ecmn'
        elif(model == 'ecmg'):
            tcmodel='ecmg'

        elif(model == 'ukm2'):
            tcmodel='ukm2'
            
        elif(model == 'cmc2'):
            tcmodel='cmc'

        else:
            tcmodel=model

        return(tcmodel)


    def Model2Model2PlotModel(self,model):

        if(model == 'gfs2'):
            pmodel='gfs'
        elif(model == 'fim8'):
            pmodel='fim'
        elif(model == 'fimx'):
            pmodel='fimx'
        elif(model == 'ngp2'):
            pmodel='ngp2'

        elif(model == 'ngpc'):
            pmodel='ngpc'
        elif(model == 'navg'):
            pmodel='navg'
        elif(model == 'ngpj'):
            pmodel='ngpj'
        elif(model == 'gfsc'):
            pmodel='gfsc'
        elif(model == 'ukmc'):
            pmodel='ukmc'
        elif(model == 'jmac'):
            pmodel='jmac'

        elif(model == 'ecm2'):
            pmodel='ecm'

        elif(model == 'ecm4'):
            pmodel='ecm'

        elif(model == 'ecm5'):
            pmodel='ecm'

        elif(model == 'jgsm'):
            pmodel='gsm'

        elif(model == 'era5'):
            pmodel='er5'

        elif(model == 'cgd2'):
            pmodel='cmc'

        elif(model == 'gfsk'):
            pmodel='gfsk'

        elif(model == 'ecmn'):
            pmodel='ecmn'
            
        elif(model == 'ecmg'):
            pmodel='ecmg'

        elif(model == 'ukm2'):
            pmodel='ukm'
        elif(model == 'cmc2'):
            pmodel='cmc'

        else:
            pmodel=model

        return(pmodel)


    def ModeltoGrfModel(self,model):

        if(model == 'gfs2'):
            gmodname='gfs05'
        elif(model == 'fim8'):
            gmodname='fim05'
        elif(model == 'fimx'):
            gmodname='fimx05'
        elif(model == 'ngp2'):
            gmodname='ngp10'
        elif(model == 'ngpc'):
            gmodname='ngp05'
        elif(model == 'navg'):
            gmodname='nav05'
        elif(model == 'ngpj'):
            gmodname='ngp05'
        elif(model == 'gfsc'):
            gmodname='gfs05'
        elif(model == 'ukmc'):
            gmodname='ukm10'
        elif(model == 'jmac'):
            gmodname='jma10'
        elif(model == 'ecmn'):
            gmodname='ecmn10'
        elif(model == 'ecmg'):
            gmodname='ecmg05'

        elif(model == 'ecm2'):
            gmodname='ecm10'

        elif(model == 'ecm4' or model == 'ecm5'):
            gmodname='ecm025'

        elif(model == 'jgsm'):
            gmodname='gsm125'

        elif(model == 'era5'):
            gmodname='er505'

        elif(model == 'cgd2'):
            gmodname='cmc025'

        elif(model == 'gfsk'):
            gmodname='gfs05'

        elif(model == 'ukm2'):
            gmodname='ukm07'
        elif(model == 'cmc2'):
            gmodname='cmc10'
            
        elif(model == 'fv3e'):
            gmodname='fv3e05'
        elif(model == 'fv3g'):
            gmodname='fv3g05'
            
        else:
            gmodname="%s%s"%(model,W2_MODELS_GRF_EXT)

        #ffffffffffffffffffffffffffffffffffffff
        #
        # force standard extenion -- disable
        #
        #gmodname="%s%s"%(model[0:3],W2_MODELS_GRF_EXT)

        return(gmodname)




    def Model2CenterModel(self,model):

        centermodel=None

        if(model == 'gfs2'): centermodel='ncep/gfs2'
        if(model == 'goes'): centermodel='ncep/gfs2'
        if(model == 'fim8'): centermodel='esrl/fim8'
        if(model == 'fv3e'): centermodel='esrl/fv3e'
        if(model == 'fv3g'): centermodel='esrl/fv3g'
        if(model == 'fimx'): centermodel='esrl/fimx'
        if(model == 'ngp2'): centermodel='fnmoc/nogaps'

        if(model == 'ngpc'): centermodel='fnmoc/ngp05cagips'
        if(model == 'navg'): centermodel='fnmoc/nav05cagips'
        if(model == 'ngpj'): centermodel='fnmoc/ngp05jtwc'
        if(model == 'ukmc'): centermodel='ukmo/ukmc'
        if(model == 'gfsc'): centermodel='ncep/gfsc'
        if(model == 'gfsn'): centermodel='ncep/gfsn'
        if(model == 'jmac'): centermodel='jma/jmac'

        if(model == 'ocn'): centermodel='fnmoc/ocean/sst'
        if(model == 'ohc'): centermodel='fnmoc/ocean/ohc'
        if(model == 'ww3'): centermodel='fnmoc/ocean/ww3'
        if(model == 'ukm2'): centermodel='ukmo/ukm2'
        if(model == 'ecm1'): centermodel='ecmwf/ecm1'
        if(model == 'ecm2'): centermodel='ecmwf/ecmo'
        if(model == 'ecm4'): centermodel='ecmwf/ecm4'
        if(model == 'ecm5'): centermodel='ecmwf/ecm5'
        if(model == 'jgsm'): centermodel='jma/jgsm'
        if(model == 'era5'): centermodel='ecmwf/era5'
        if(model == 'cgd2'): centermodel='cmc/cgd2'
        if(model == 'gfsk'): centermodel='esrl/gfsk'
        if(model == 'gfsk'): centermodel='esrl/gfsk'
        if(model == 'ecmn'): centermodel='ecmwf/ecmo_nws'
        if(model == 'ecmg'): centermodel='ecmwf/ecmg'
        if(model == 'cmc2'): centermodel='cmc/cmc'
        if(model == 'gfdl'): centermodel='ncep/gfdl'
        if(model == 'hwrf'): centermodel='ncep/gfdl'
        if(model == 'tctrk'): centermodel='tctrk'

        return(centermodel)




    def Model2DtauPlot(self,model,dtghh=''):

        dtau=None

        if(model == 'gfs'): dtau=6
        if(model == 'ngp'): dtau=6
        if(model == 'ngp05'): dtau=6
        if(model == 'ukm'): dtau=6
        if(model == 'ecm'): dtau=12
        if(model == 'cmc'): dtau=12
        if(model == 'ocn'): dtau=12
        if(model == 'ohc'): dtau=12
        if(model == 'ww3'): dtau=6

        if(model == 'gfs2'): dtau=12
        if(model == 'fim8' or model == 'fv3e' or model == 'fv3g'): dtau=12
        if(model == 'fimx'): dtau=12
        if(model == 'ngp2'): dtau=12

        if(model == 'ngpc' or model == 'ngpj'): dtau=6
        if(model == 'navg'): dtau=6
        if(model == 'ukmc'): dtau=6
        if(model == 'gfsc'): dtau=6
        if(model == 'gfsn'): dtau=6
        if(model == 'jmac'): dtau=6

        if(model == 'ecm2'): dtau=12
        if(model == 'ecm4'): dtau=12
        if(model == 'ecm5' or model == 'era5' or model == 'cgd2'): dtau=12
        if(model == 'jgsm'): dtau=6
        if(model == 'gfsk'): dtau=6
        if(model == 'ecmn'): dtau=12
        if(model == 'ecmg'): dtau=24
        if(model == 'ukm2'): dtau=6
        if(model == 'cmc2'): dtau=12

        return(dtau)



    def Model2PlotMinTau(self,model,dtg):

        dtghh=int(dtg[8:10])

        if(model == 'gfs2' or model == 'fv3e' or model == 'fv3g'):
            taumin=144

        elif(mf.find(model,'fim8')):
            taumin=144

        elif(mf.find(model,'ocn')):
            taumin=0

        elif(mf.find(model,'ohc')):
            taumin=0

        elif(mf.find(model,'ww3')):
            taumin=0

        elif(mf.find(model,'fimx')):
            taumin=144

        elif(model == 'ngp2'):
            taumin=144

        elif(model == 'ngpc' or model == 'ngpj'):
            taumin=144

        elif(model == 'navg'):
            taumin=144

        elif(model == 'gfsc'):
            taumin=144

        elif(model == 'ukmc'):
            taumin=120

        elif(model == 'jmac'):
            taumin=120

        elif(model == 'ecm2'):
            taumin=144

        elif(model == 'ecm4'):
            taumin=144

        elif(model == 'ecm5' or model == 'era5' or model == 'cgd2'):
            taumin=144
            
        elif(model == 'jgsm'):
            taumin=132

        elif(model == 'gfsk'):
            taumin=144

        elif(model == 'ecmn'):
            taumin=144

        elif(model == 'ecmg'):
            taumin=144

        elif(model == 'ukm2'):
            #
            # taumin and tau forced to be the same because grib from ukmo is in one file...
            #
            if(dtghh == 0 or dtghh == 12):
                taumin=144
            elif(dtghh == 6 or dtghh == 18):
                taumin=60

        elif(model == 'cmc2'):
            taumin=144

        else:
            print 'EEE invalid model Model2PlotMinTau: ',model
            sys.exit()

        tauend=self.Model2EtauData(model,dtghh)
        dtau=self.Model2DtauPlot(model)


        if(tauend != None and dtau != None):
            alltaus=range(0,tauend+1,dtau)
        else:
            print 'EEE.w2base.Model2PlotMinTau invalid model in plotmintau',model,dtg
            sys.exit()

        return(taumin,alltaus)



    def Model2DataPathsStatus(self,model,dtg,doreport=0,center='esrl',cagips=0,dowgribinv=1):


        printall=0
        if(doreport == 2): printall=1


        yyyy=dtg[0:4]
        mm=dtg[4:6]
        yyyymm=dtg[0:6]
        mmddhh=dtg[4:10]

        renmask=None
        modelrename=None

        localdir="%s/%s"%(self.Nwp2DataBdirModel(model),dtg)

        xwgrib='wgrib'

        if(model == 'gfs2' or model == 'fv3e' or model == 'fv3g'):

            xwgrib='wgrib2'
            dmask="*%s.%s.f???.grb2"%(model,dtg)
            ldmask="%s/%s"%(localdir,dmask)

            def name2tau(file):
                tau=file.split('.')[2][1:]
                tau=int(tau)

                return(tau)


        elif(model == 'ngp2'):

            dmask="*%s.%s.f???.grb2"%(model,dtg)
            ldmask="%s/%s"%(localdir,dmask)

            def name2tau(file):
                tau=file.split('.')[2][1:]
                tau=int(tau)

                return(tau)


        elif(model == 'ngpc' or model == 'ngpj'):

            dmask="*%s.%s.f???.grb1"%(model,dtg)
            ldmask="%s/%s"%(localdir,dmask)

            def name2tau(file):
                tau=file.split('.')[2][1:]
                tau=int(tau)

                return(tau)

        elif(model == 'navg'):

            dmask="*%s.%s.f???.grb1"%(model,dtg)
            ldmask="%s/%s"%(localdir,dmask)

            def name2tau(file):
                tau=file.split('.')[2][1:]
                tau=int(tau)

                return(tau)

        elif(model == 'gfsc'):

            dmask="*%s.%s.f???.grb1"%(model,dtg)
            ldmask="%s/%s"%(localdir,dmask)

            def name2tau(file):
                tau=file.split('.')[2][1:]
                tau=int(tau)

                return(tau)

        elif(model == 'ukmc'):

            dmask="*%s.%s.f???.grb1"%(model,dtg)
            ldmask="%s/%s"%(localdir,dmask)

            def name2tau(file):
                tau=file.split('.')[2][1:]
                tau=int(tau)

                return(tau)

        elif(model == 'jmac'):

            dmask="*%s.%s.f???.grb1"%(model,dtg)
            ldmask="%s/%s"%(localdir,dmask)

            def name2tau(file):
                tau=file.split('.')[2][1:]
                tau=int(tau)

                return(tau)


        elif(model == 'fim8'):

            remotedir="%s/%s"%(self.Model2CenterModel(model),yyyymm)
            dmask="fim8.%s.f???.grb1"%(dtg)
            ldmask="%s/%s"%(localdir,dmask)

            def name2tau(file):
                (base,ext)=os.path.splitext(file)
                lf=len(base)
                lfe=lf
                lfb=lfe-3
                tau=base[lfb:lfe]
                tau=int(tau)

                return(tau)


        elif(model == 'fimx'):

            localdir='/w21/dat/nwp2/rtfim/dat/FIMX/%s'%(dtg)
            remotedir="%s/%s"%(self.Model2CenterModel(model),yyyymm)
            dmask="*fim8.FIMX.f???.grb2"
            ldmask="%s/%s"%(localdir,dmask)

            def name2tau(file):
                (base,ext)=os.path.splitext(file)
                lf=len(base)
                lfe=lf
                lfb=lfe-3
                tau=base[lfb:lfe]
                tau=int(tau)

                return(tau)



        elif(model == 'ukm2'):

            dmask="ukm2.%s.grb1"%(dtg)
            ldmask="%s/%s"%(localdir,dmask)
            hh=dtg[8:10]
            def name2tau(file):
                hh=dtg[8:10]
                if(hh == '00' or hh == '12'):
                    tau=144
                else:
                    tau=60

                return(tau)


        elif(model == 'ecm2'):

            dmask="ecmo.%s.f???.grb1"%(dtg)
            ldmask="%s/%s"%(localdir,dmask)

            def name2tau(file):

                lf=len(file)
                lfe=lf-3
                lfb=lfe-6
                vmmddhh=file[lfb:lfe]
                vmm=vmmddhh[0:2]
                if(vmm == '01' and mm == '12'):
                    vdtg=str(int(yyyy+1))+vmmddhh
                else:
                    vdtg=yyyy+vmmddhh
                tau=mf.dtgdiff(dtg,vdtg)
                tau=int(tau)

                return(tau)

            def name2tau(file):
                (base,ext)=os.path.splitext(file)
                lf=len(base)
                lfe=lf
                lfb=lfe-3
                tau=base[lfb:lfe]
                tau=int(tau)

                return(tau)

        elif(model == 'ecm4'):

            dmask="%s.%s.f???.grb1"%(model,dtg)
            ldmask="%s/%s"%(localdir,dmask)

            def name2tau(file):

                lf=len(file)
                lfe=lf-3
                lfb=lfe-6
                vmmddhh=file[lfb:lfe]
                vmm=vmmddhh[0:2]
                if(vmm == '01' and mm == '12'):
                    vdtg=str(int(yyyy+1))+vmmddhh
                else:
                    vdtg=yyyy+vmmddhh
                tau=mf.dtgdiff(dtg,vdtg)
                tau=int(tau)

                return(tau)

            def name2tau(file):
                (base,ext)=os.path.splitext(file)
                lf=len(base)
                lfe=lf
                lfb=lfe-3
                tau=base[lfb:lfe]
                tau=int(tau)

                return(tau)


        elif(model == 'gfsk'):

            dmask="gfsk.%s.f???.grb1"%(dtg)
            ldmask="%s/%s"%(localdir,dmask)


            def name2tau(file):
                (base,ext)=os.path.splitext(file)
                lf=len(base)
                lfe=lf
                lfb=lfe-3
                tau=base[lfb:lfe]
                tau=int(tau)

                return(tau)

        elif(model == 'era5' or model == 'ecm5' ):

            dmask="%s-w2flds-%s-ua.grb2"%(model,dtg)
            ldmask="%s/%s"%(localdir,dmask)
            hh=dtg[8:10]
            
            def name2tau(file):
                hh=dtg[8:10]
                if(hh == '00' or hh == '12'):
                    tau=240
                else:
                    tau=240

                return(tau)

        elif(model == 'jgsm'):
            
            dmask="%s.w2flds.%s.grb2"%(model,dtg)
            ldmask="%s/%s"%(localdir,dmask)
            hh=dtg[8:10]
                    
            def name2tau(file):
                hh=dtg[8:10]
                if(hh == '00' or hh == '12'):
                    tau=132
                else:
                    tau=132
        
                return(tau)

        elif(model == 'cgd2'):

            dmask="%s.w2flds.%s.f???.grb2"%(model,dtg)
            ldmask="%s/%s"%(localdir,dmask)
            hh=dtg[8:10]
            def name2tau(file):
                hh=dtg[8:10]
                if(hh == '00' or hh == '12'):
                    tau=240
                else:
                    tau=240

                return(tau)

        elif(model == 'ecmn'):

            dmask="*%s.%s.f???.grb2"%(model,dtg)
            ldmask="%s/%s"%(localdir,dmask)

            def name2tau(file):
                tau=file.split('.')[2][1:]
                tau=int(tau)

                return(tau)


        elif(model == 'ecmg'):

            dmask="*%s.%s.f???.grb2"%(model,dtg)
            ldmask="%s/%s"%(localdir,dmask)

            def name2tau(file):
                tau=file.split('.')[2][1:]
                tau=int(tau)

                return(tau)



        elif(model == 'cmc2'):

            dmask="*%s.%s.f???.grb1"%(model,dtg)
            ldmask="%s/%s"%(localdir,dmask)

            def name2tau(file):
                tau=file.split('.')[2][1:]
                tau=int(tau)

                return(tau)


        else:
            print 'EEEE invalid model in w2.ModelArchiveDir: ',model
            sys.exit()


        status={}

        override=0

        dpaths=glob.glob("%s"%(ldmask))
        dpaths.sort()
        
        report=[]

        if(doreport != 2):
            report.append("model: %s dtg: %s "%(model,dtg))

        np=len(dpaths)

        if(np == 0):
            rc=-1
            print 'WWW:  NO DATA model: ',model,dtg,' localdir: ',localdir
            return(rc,-999)


        report.append(" ")
        report.append("model   dtg       tau(h)  age(h)  nf")
        report.append("===== ==========  ======  ======  ==")
        report.append(" ")

        for dpath in dpaths:

            (dir,file)=os.path.split(dpath)
            (base,ext)=os.path.splitext(dpath)
            gribver=int(ext[-1])

            if(model == 'ukm2'):
                hh=dtg[8:10]
                if(hh == '00' or hh == '12'):
                    tau=144
                else:
                    tau=60
                wgribpath="%s.wgrib%1d.txt"%(base,gribver)

            else:
                tau=name2tau(file)
                wgribpath="%s.wgrib%1d.txt"%(base,gribver)

            if(dowgribinv):
                if(not(os.path.exists(wgribpath)) or (os.path.getsize(wgribpath) == 0) or override):
                    cmd="%s %s > %s"%(xwgrib,dpath,wgribpath)
                    mf.runcmd(cmd)

            if(os.path.exists(wgribpath)):
                (dir,file)=os.path.split(wgribpath)
                age=MF.PathCreateTimeDtgdiff(dtg,wgribpath)
                nf=len(open(wgribpath).readlines())
                report.append("%s  %s   %03d   %5.2f  %4d"%(model,dtg,tau,age,nf))
                status[tau]=(age,nf)



        nmiss=-999
        curtaus=status.keys()
        curtaus.sort()

        (taumin,alltaus)=self.Model2PlotMinTau(model,dtg)

        if(len(curtaus) > 0):
            latesttau=curtaus[-1]
        else:
            latesttau=-999


        #
        # see if minimum taus is available
        #
        try:
            (agedone,nfdone)=status[taumin]
            iok=1
        except:
            (agedone,nfdone)=(-999.9,-99)
            iok=0


        if(iok):

            #
            # test for completeness
            #

            cmask={}

            for atau in alltaus:

                if(atau <= taumin):
                    cmask[atau]=0
                    for ctau in curtaus:
                        if(ctau == atau):
                            cmask[ctau]=1

            mtaus=cmask.keys()
            mtaus.sort()
            nmiss=0
            for mtau in mtaus:
                if(cmask[mtau] == 0): nmiss=nmiss+1


            rc=1

        else:

            #print 'WWW2: ',report[0],' insufficient DATA...'
            rc=0


        if(doreport):
            if(printall):
                for line in report:
                    print line
            else:
                print report[-1]

        return(rc,latesttau)



    def Model2IsReady2Plot(self,model,dtg,dow2flds=1):
        
        minfracreq=0.0
        if(dow2flds):
            from M2 import setModel2
            m2=setModel2(model)
            fm=m2.DataPath(dtg,dtype='w2flds',dowgribinv=1)
            fd=fm.GetDataStatus(dtg)
            (taumin,alltaus)=self.Model2PlotMinTau(model,dtg)
            
            latesttau=fd.dslatestCompleteTau
            latesttauB=fd.dslatestCompleteTauBackward
            rc=0
            if((latesttau >= taumin) or
               (latesttau > 0 and latesttauB > taumin)
               ): rc=1
            
            
        else:
            if(model == 'ecmn' or model == 'ecmg'):
                rc=1
            else:
                (rc,latesttau)=self.Model2DataPathsStatus(model,dtg)

        return(rc,minfracreq)




    def SetLandFrac(self,lfres='1deg',ni=720,nj=361):

        lf=array.array('f')
        gdir=self.GeogDatDirW2
        lfres='1deg'
        lfpath="%s/lf.%s.dat"%(gdir,lfres)
        LF=open(lfpath,'rb')
        nij=ni*nj
        lf.fromfile(LF,nij)
        return(lf)

    #  return land frac given lat/lon; note defaults; same as used by .gs
    #

    def GetLandFrac(self,lf,tlat,tlon,ni=720,nj=361,blat=-90.0,blon=0.0,dlat=0.5,dlon=0.5):


        def w2ij(wi,wj,ni,nj,wi0,wj0,dwi,dwj):

            i=(wi-wi0)/dwi + 0.5
            j=(wj-wj0)/dwj + 0.5

            #
            # cyclic continuity in x
            #
            if(i <  0.0): i=float(ni)+i
            if(i >   ni): i=i-float(ni)

            i=int(i+1.0)
            j=int(j+1.0)

            return(i,j)


        (i,j)=w2ij(tlon,tlat,ni,nj,blon,blat,dlon,dlat)
        ij=(j-1)*ni+i-1
        return(lf[ij])


    def IsModel2(self,model):

        for m2 in self.Nwp2ModelsAll:
            if(m2 == model):
                return(1)
        return(0)

    def IsModel2PlotRunning(self,model,dtg):
        prcs="%s.%s.%s.*"%(self.W2TmpPrcDirPrefix,model,dtg)
        prcs=glob.glob(prcs)
        return(len(prcs))


    def Nwp2DataBdirModel(self,model,bdir2=None):

        ddir=None
        if(bdir2 == ''):
            ddir=ddir[1:]

        if(bdir2 == None): bdir2=self.Nwp2DataBdir
        centermodel=self.Model2CenterModel(model)
        ddir="%s/%s"%(bdir2,centermodel)

        if(model == 'fimx'):
            ddir='/w21/dat/nwp2/rtfim/dat/FIMX'


        if(model == 'all2'):
            ddir="%s/*/*"%(bdir2)

        return(ddir)


    def getW2fldsRtfimCtlpath(self,model,dtg,maxtau=None,dtau=6,details=1,override=0,verb=0,doSfc=0):

        from M2 import setModel2,FimModel,Model2

        def getNfields(wgribs,verb=1):

            nfields={}

            for wgrib in wgribs:
                (dir,file)=os.path.split(wgrib)
                tt=file.split('.')
                tau=tt[len(tt)-3][1:]
                nf=len(open(wgrib).readlines())
                nfields[int(tau)]=nf

            return(nfields)


        def gettaus(gribs,verb=0):

            datpaths={}
            taus=[]
            gribver=None
            gribtype=None

            for grib in gribs:
                (dir,file)=os.path.split(grib)
                tt=file.split('.')
                tau=tt[len(tt)-2][1:]
                gribtype=tt[len(tt)-1]
                gribver=gribtype[-1:]
                siz=MF.GetPathSiz(grib)

                if(siz > 0):
                    tau=int(tau)
                    taus.append(tau)
                    datpaths[tau]=grib
                    if(verb): print file,tau,gribtype,gribver

            taus=MF.uniq(taus)

            return(taus,gribtype,gribver,datpaths)


        # -- default is to get 'all' taus, called only if maxtau is set...in
        #    getCtlpathTaus(self,model,dtg,maxtau=168)
        #
        def reducetaus(taus,maxtau='all',dtau=6):

            taus.sort()
            ftaus=[]
            if(maxtau == 'all'): maxtau=taus[-1]
            rtaus=range(0,maxtau+1,dtau)
            for tau in taus:
                if(not(tau in rtaus)): continue
                ftaus.append(tau)

            ftaus=MF.uniq(ftaus)

            return(ftaus)

        def dofail(details):
            if(not(details)):
                return(0,None,None)
            else:
                return(0,None,None,None,None,None,None,None)


        from FM import rtfimRuns
        fR=rtfimRuns()

        dtype=None
        if(model in self.Nwp2ModelsAll):
            dtype='w2flds'
            imodel=model
        elif(model in fR.runs.keys()):
            dtype='rtfim'
            imodel=fR.runs[model]
        else:
            print 'EEE invalid model in W2.getW2fldsRtfimCtlpath model: ',model
            return(0,None,None,None,None,None,None,None)

        m2=setModel2(imodel)  
        m2.setDbase(dtg)

        dataDtg=dtg
        tauOffset=0
        
        if(self.is0618Z(dtg) and m2.modelDdtg == 12):
            tauOffset=6
            dataDtg=mf.dtginc(dtg, -6)

        nfields={}

        bdirs=copy.copy(self.allBdirs)
        if(onWjet):
            bdirs.append(self.W2LocalBaseDir)

        # -- check m2 for use obj bddir
        #
        useBddir=0
        if(hasattr(m2,'useBddir')): useBddir=m2.useBddir
        if(useBddir):
            bdirs=[m2.bddir]
            
            
        for bdir in bdirs:
            
            if(bdir == '/Volumes' and dtype == 'w2flds'):
                rootdir="%s/%s/%s"%(bdir,dtype,imodel)
            elif(useBddir):
                rootdir=bdir
            else:
                rootdir="%s/%s/dat/%s"%(bdir,dtype,imodel)
                
            maskdir="%s/%s"%(rootdir,dataDtg)

            # -- original, changed to be consistent between local and remote (wjet)
            #
            #if(onWjet and dtype == 'rtfim'): maskdir="%s/%s/fim*"%(rootdir,dtg)
            if(onWjet and dtype == 'rtfim'):
                from FM import trootWjet
                rootdir="%s/dat/%s"%(trootWjet,imodel)
                maskdir="%s/%s"%(rootdir,dataDtg)

            mask="%s/*%s*.ctl"%(maskdir,imodel)

            if(verb): print "W2.getW2fldsRtfimCtlpath: ",mask
            ctlpaths=glob.glob(mask)
            
            # -- special case for era5 where we have ua and sfc .ctl
            #
            if(len(ctlpaths) == 2 and (imodel == 'era5' or imodel == 'ecm5') ):
                for ctl in ctlpaths:
                    if(doSfc and mf.find(ctl,'sfc')): 
                        ctlpaths=[ctl]
                        
                    elif(not(doSfc) and mf.find(ctl,'ua')): 
                        ctlpaths=[ctl]
                    
            if(len(ctlpaths) == 1):
                ctlpath=ctlpaths[0]
                
                # -- use M2 for w2flds -- cgd6 does not have a wgrib?.txt inventory...this makes it...
                #
                if(dtype == 'w2flds'):
                    fm=m2.DataPath(dataDtg,dtype=dtype,dowgribinv=1,override=override,doDATage=1) 
                    fd=fm.GetDataStatus(dataDtg)
                    
                if(details):
                    
                    # -- handle situation where taus in w2flds != taus in nwp2 fields
                    # -- tossed tau78 in ngp2
                    #
                    gmask="%s/*%s*.grb?"%(maskdir,imodel)
                    if(dtype == 'w2flds'): gmask="%s/*%s*%s*.grb?"%(maskdir,imodel,dtype)
                    
                    # -- use fd object first...
                    #
                    if(hasattr(fd,'statuss')):
                        
                        try:
                            fds=fd.statuss[dataDtg]
                        except:
                            dofail(details)
                        
                        taus=fds.keys()
                        datpaths=fd.datpaths
                        gribtype=fd.gribtype
                        gribver=fd.gribver
                        
                        # get nfields hash
                        #
                        nfields={}
                        for n in range(0,len(fds)):
                            ntau=taus[n]
                            nf=fds[ntau][-1]
                            nfields[ntau]=nf
                            
                        taus.sort()

                    else:
                        gribs=glob.glob(gmask)
                        (taus,gribtype,gribver,datpaths)=gettaus(gribs)
                    
                        wmask="%s/*%s*.f???.wgrib?.txt"%(maskdir,imodel)
                        wgribs=glob.glob(wmask)
                        nfields=getNfields(wgribs)
                    
                    # -- cull taus
                    if(maxtau != None): taus=reducetaus(taus,maxtau,dtau)

                else:
                    taus=gribtype=gribver=datpaths=None

                if(not(details)):
                    return(1,rootdir,ctlpath)
                else:
                    return(1,ctlpath,taus,gribtype,gribver,datpaths,nfields,tauOffset)


        if(len(ctlpaths) == 0 or len(ctlpaths) > 1):
            if(verb): print 'WWW ctlpaths: ',ctlpaths

        dofail(details)



    def getCtlpathTaus(self,model,dtg,maxtau=168):

        ctlpath=taus=nfields=tauOffset=None
        rc=self.getW2fldsRtfimCtlpath(model,dtg,maxtau=maxtau)
        if(rc == None):
            ctlpath=taus=nfields=tauOffset=None
        else:
            ctlpath=rc[1]
            taus=rc[2]
            nfields=rc[-2]
            tauOffset=rc[-1]
            
        return(ctlpath,taus,nfields,tauOffset)



    #
    # event logging
    #

    def EventPath(self,evtType,model,dtg,areaopt):
        bdir="%s/%s"%(self.EvtBdirW2,dtg[0:6])
        mf.ChkDir(bdir,'mk')
        epath="%s/%s.%s.%s.%s.txt"%(bdir,evtType,model,dtg,areaopt)
        return(epath)


    def PutEvent(self,pyfile,evtType,tag,model,dtg,areaopt,area=None):

        dtgmn=dtg+'00'
        cdtgmn=mf.dtg('dtgmn')
        phr=mf.dtgmndiff(dtgmn,cdtgmn)
        eventtime=mf.dtg('dtg.hms')
        epath=self.EventPath(evtType,model,dtg,areaopt)

        oareaopt=areaopt
        if(area != None): oareaopt=area

        eventcard="%s %-15s dtg: %s model: %-5s areaopt: %-10s  time: %s phr: %6.2f"%(pyfile,tag,dtg,model,oareaopt,eventtime,phr)

        E=open(epath,'a')
        E.writelines(eventcard+'\n')
        E.close()


    def GetEvent(self,evtType,model,dtg,areaopt):
        epath=self.EventPath(evtType,model,dtg,areaopt)
        try:
            cards=open(epath).readlines()
        except:
            cards=[]
        return(cards)


    def ModelPlotTaus(self,model,dtg,center=None):

        if(center == None):
            center=self.W2Center.lower()

        dtghh=int(dtg[8:10])

        taus=None
        if(center == 'esrl' or mf.find(center,'wxmap')):

            if(model == 'gfs2' or model == 'gfs' or 
               model == 'ecm2' or model == 'ecm4' or model == 'era5' or model == 'ecm5' or model == 'cgd2' or
               model == 'fv3e' or model == 'fv3g' or
               model == 'gfsk'):
                etau=144
                dtau=12
                etau=None
                taus=[0,6,12,18,24,30,36,42,48,60,72,84,96,108,120,132,144,156,168]

            elif(model == 'jgsm'):
                etau=132
                dtau=6
                etau=None
                taus=[0,6,12,18,24,30,36,42,48,60,72,84,96,108,120,132]

            elif(model == 'ngp2' or model == 'ngp'):
                dtau=6
                etau=None
                taus=[0,6,12,18,24,30,36,42,48,60,72,84,96,108,120,132,144]

            elif(model == 'ngpc' or model == 'ngpj'):
                dtau=6
                etau=None
                taus=[0,6,12,18,24,30,36,42,48,60,72,84,96,108,120,132,144,156,168]

            elif(model == 'navg'):
                dtau=6
                etau=None
                taus=[0,6,12,18,24,30,36,42,48,60,72,84,96,108,120,132,144,156,168]

            # -- jtwc cagips models
            #
            elif(model == 'gfsc' or model == 'jmac'):
                dtau=6
                etau=None
                taus=[0,6,12,18,24,30,36,42,48,60,72,84,96,108,120,132,144,156,168]

            elif(model == 'ukmc'):
                dtau=12
                etau=None
                if(dtghh == 0 or dtghh == 12):
                    taus=[0,6,12,18,24,30,36,42,48,60,72,84,96,108,120]
                elif(dtghh == 6 or dtghh == 18):
                    taus=[0]

            elif(model == 'ecm' or model == 'ecmn'):
                etau=168
                dtau=12
                etau=None
                taus=[0,6,12,18,24,30,36,42,48,60,72,84,96,108,120,132,144,156,168]

            elif(model == 'ecmg'):
                etau=168
                dtau=24
                etau=None
                taus=[0,24,48,72,96,120,144,168]


            elif(model == 'ukm2' or model == 'ukm'):

                dtau=12
                etau=None
                if(dtghh == 0 or dtghh == 12):
                    taus=[0,6,12,18,24,30,36,42,48,60,72,84,96,108,120,132,144,156,168]
                elif(dtghh == 6 or dtghh == 18):
                    taus=[0,6,12,18,24,30,36,42,48,60]

            elif(model == 'cmc2' or model == 'cmc'):
                etau=144
                dtau=12

            else:
                print 'EEE invalid model ModelPlotTaus: ',model
                sys.exit()

        else:

            print 'EEEEEEEEEEEEEEEEEEE invalid center: ',center
            sys.exit()

        if(etau != None):
            taus=range(0,etau+1,dtau)

        return(taus)




    def setAreas(self,areaopt):

        w2areas= [
            'asia',
            'wconus',
            'conus',
            'europe',
            'tropwpac',
            'tropnio',
            'tropepac',
            'troplant',
            'tropsio',
            'tropoz',
            'tropswpac',
        ]

        self.areaRegion={

            'asia':'midlat',
            'wconus':'midlat',
            'conus':'midlat',
            'europe':'midlat',

            'troplant':'tropics',
            'tropepac':'tropics',
            'tropwpac':'tropics',
            'tropswpac':'tropics',
            'tropnio':'tropics',
            'tropsio':'tropics',
            'tropoz':'tropics',

        }

        self.areaOtherAreas={

            'asia':['wconus','conus','tropwpac','tropnio'],
            'europ':['conus','wconus','troplant','asia'],
            'conus':['troplant','wconus','europe','tropepac'],
            'wconus':['tropepac','conus','europe','troplant'],

            'troplant':['tropepac','tropwpac','tropnio','europe'],
            'tropepac':['troplant','tropwpac','tropnio','conus'],
            'tropwpac':['troplant','tropepac','tropnio','asia'],
            'tropswpac':['tropsio','tropoz','tropnio','tropepac'],
            'tropnio':['tropwpac','tropsio','tropswpac','tropepac'],
            'tropsio':['tropswpac','tropoz','tropnio','tropepac'],
            'tropoz':['tropsio','tropswpac','tropwpac','tropepac'],

        }


        if(areaopt != 'all'):
            self.areas=[areaopt]
        elif(len(areaopt.split('.')) > 1):
            self.areas=areaopt.split('.')
        else:
            self.areas=w2areas


    def IsModel2PlotRunning(self,model,dtg,verb=1):
        prcs="%s.%s.%s.*"%(self.W2TmpPrcDirPrefix,model,dtg)
        if(verb): print 'IsModel2PlotRunning: mask: ',prcs
        prcs=glob.glob(prcs)
        if(verb):
            for prc in prcs:
                print 'prc: ',prc
            print 'len(prcs): ',len(prcs)
        return(len(prcs))


    def NwpDataBdir(self,model):

        # do not put in argument list, set bdir by
        # setting in the w2 object, e.g.,
        # w2.W2BaseDirDat=w2.W2RegenBaseDirDat
        #
        bdir=self.W2BaseDirDat

        if(model == 'ngp'):
            ddir="%s/nwp/fnmoc"%(bdir)
        elif(model == 'ngp05'):
            ddir="%s/nwp/fnmoc"%(bdir)
        elif(model == 'ocn'):
            ddir="%s/nwp/fnmoc"%(bdir)
        elif(model == 'ww3'):
            ddir="%s/nwp/fnmoc"%(bdir)
        elif(model == 'gfs' or model == 'gfs.jtwc' or model == 'avn'):
            ddir="%s/nwp/ncep"%(bdir)
        elif(model == 'ukm' or model == 'ukm.jtwc'):
            ddir="%s/nwp/ukmo"%(bdir)
        elif(model == 'gsm'):
            ddir="%s/nwp/jma"%(bdir)
        elif(model == 'ecm'):
            ddir="%s/nwp/ecmwf"%(bdir)
        elif(model == 'cmc'):
            ddir="%s/nwp/cmc"%(bdir)
        elif(model == 'fim8' or model == 'fim9' or model == 'fimx'):
            ddir="%s/nwp/gsd/%s"%(bdir,model)
        elif(model == 'all'):
            ddir="%s/nwp/*"%(bdir)

        elif(model == 'cqpr'):
            ddir=self.NhcQmorphProductsGrib
        else:
            ddir=0

        if(bdir == ''):
            ddir=ddir[1:]

        return(ddir)

    def W2LoopPltDir(self,ltype,dtype='full',doarchive=0):

        gdir='plt_loop'
        if(ltype == 'prw'): gdir='plt_loop'

        if(dtype == 'full'):

            if(doarchive == 3):
                gdir="%s/%s"%(self.EsrlHttpIntranetDocRoot,gdir)
            elif(doarchive > 0 and doarchive != 3):
                gdir="%sa/%s"%(self.W2BaseDirWeb,gdir)
            else:
                gdir="%s/%s"%(self.W2BaseDirWeb,gdir)

        return(gdir)


    def ModelHtmDir(self,model,dtg):
        hdir="%s/web_%s/%s"%(self.wxhWeb,model,dtg)
        return(hdir)


    def ModelGrfDir(self,model,dtg):
        if(model == 'ngp'):
            gdir="%s/plt_fnmoc_ngp/%s"%(self.wxhWeb,dtg)
        elif(model == 'ocn'):
            gdir="%s/plt_fnmoc_ocn/%s"%(self.wxhWeb,dtg)
            gdir="%s/ocn10.sst.000.tropwpac.png"%(gdir)
        elif(model == 'gfs'):
            gdir="%s/plt_ncep_gfs/%s"%(self.wxhWeb,dtg)
        elif(model == 'fim'):
            gdir="%s/plt_esrl_fim/%s"%(self.wxhWeb,dtg)

        elif(model == 'fv3e'):
            gdir="%s/plt_esrl_fv3e/%s"%(self.wxhWeb,dtg)
        elif(model == 'fv3g'):
            gdir="%s/plt_esrl_fv3g/%s"%(self.wxhWeb,dtg)

        elif(model == 'fimx'):
            gdir="%s/plt_esrl_fimx/%s"%(self.wxhWeb,dtg)
        elif(model == 'ngpc'):
            gdir="%s/plt_fnmoc_ngpc/%s"%(self.wxhWeb,dtg)
        elif(model == 'navg'):
            gdir="%s/plt_fnmoc_navg/%s"%(self.wxhWeb,dtg)
        elif(model == 'gdl'):
            gdir="%s/plt_gfdl_gfl/%s"%(self.wxhWeb,dtg)
        elif(model == 'ukm'):
            gdir="%s/plt_ukmo_ukm/%s"%(self.wxhWeb,dtg)
        elif(model == 'ecm'):
            gdir="%s/plt_ecmwf_ecm/%s"%(self.wxhWeb,dtg)
        elif(model == 'ecmn'):
            gdir="%s/plt_ecmwf_ecm/%s"%(self.wxhWeb,dtg)
        elif(model == 'ecmt'):
            gdir="%s/plt_ecmwf_ecmt/%s"%(self.wxhWeb,dtg)
        elif(model == 'ecmg'):
            gdir="%s/plt_ecmwf_ecmg/%s"%(self.wxhWeb,dtg)
        elif(model == 'cmc' or model == 'cgd2'):
            gdir="%s/plt_cmc_cmc/%s"%(self.wxhWeb,dtg)
        elif(model == 'gsm'):
            gdir="%s/plt_jma_gsm/%s"%(self.wxhWeb,dtg)
        else:
            print 'EEEE invalid model: ',model
            sys.exit()

        return(gdir)

    def GetWxmapDtgs(self,curdtg,verb=0):

        dtgs={}
        models=self.wxModels

        for model in models:

            tdtg=curdtg
            ok=0
            n=0
            nmax=8
            while(ok == 0 and n < nmax):
                tdir=self.ModelHtmDir(model,tdtg)
                tdir=self.ModelGrfDir(model,tdtg)
                chkmethod=os.path.isdir
                if(model == 'ocn'): chkmethod=os.path.exists

                if(verb): print 'w2base.GetWxmapDtgs doing: ',model,tdir,tdtg
                if(chkmethod(tdir)):
                    if(verb): print 'w2base.GetWxmapDtgs RRRRR: ',tdir,tdtg,n
                    dtgs[model]=tdtg
                    ok=1
                else:
                    tdtg=mf.dtginc(tdtg,-6)
                    n=n+1

                if(n >= nmax):
                    dtgs[model]='----------'


        return(dtgs)



    def HtmlWxmapMainFull(self,tdtg,curdtg,curphr,template,verb=0,dopublic=0,setEcmModel=None,setNavModel=None):

        from tcbase import TcData
        tD=TcData(dtgopt=tdtg)
        (stmids,btcs)=tD.getDtg(tdtg)

        stmids.sort()

        nstm=len(stmids)
        tctitle=''
        for n in range(0,nstm):
            ostmid=stmids[n]
            vmax=btcs[ostmid][2]
            tt=ostmid.split('.')
            ostmid="%s.%s(%d)"%(tt[0],tt[1][-2:],vmax)
            if(n < nstm-1):
                tctitle=tctitle+"%s | "%(ostmid)
            else:
                tctitle=tctitle+"%s"%(ostmid)

        try:
            htm2=open(template,'r').read()
        except:
            print "EEEE unable to open template: %s"%(template)
            sys.exit()


        iEcmModel=EcmModel
        if(setEcmModel != None): iEcmModel=setEcmModel

        # -- set wxmodel if 'ecmt'
        #
        if(iEcmModel == 'ecmt'):
            self.wxModels=['gfs','fim','ngpc','ecmt','ukm']

        wxdtgs=self.GetWxmapDtgs(tdtg,verb=verb)

        if(iEcmModel == 'ecmn'):
            dtgecm=wxdtgs['ecmn']
        elif(iEcmModel == 'ecmg'):
            dtgecm=wxdtgs['ecmg']
        elif(iEcmModel == 'ecmt'):
            dtgecm=wxdtgs['ecmt']
        else:
            dtgecm=wxdtgs['ecm']

        iNavModel='navg'
        if(setNavModel != None): iNavModel=setNavModel

        iNavModel='navg'
        if(setNavModel != None): iNavModel=setNavModel

        dtgnavy=wxdtgs[iNavModel]

        if(verb):
            for d in wxdtgs.keys():
                print d,wxdtgs[d]




    ##     dtggfs=wxdtgs['gfs']
    ##     dtgngp=wxdtgs['ngp']
    ##     dtgukm=wxdtgs['ukm']
    ##     dtgecm=wxdtgs['ecm']
    ##     dtgcmc=wxdtgs['cmc']
    ##     dtgocn=wxdtgs['ocn']
    ##     dtggsm=wxdtgs['gsm']

    ##     createTxt="<b>Created: %s %s h</b>  GFS:%s  NGP:%s  UKM:%s  ECM:%s  CMC:%s  OCN:%s  "%(curdtg,curphr,
    ##                                                                                            dtggfs[6:],
    ##                                                                                            dtgngp[6:],
    ##                                                                                            dtgukm[6:],
    ##                                                                                            dtgecm[6:],
    ##                                                                                            dtgcmc[6:],
    ##                                                                                            dtgocn[6:])

        dtggfs=wxdtgs['gfs']
        #dtgfim=wxdtgs['fv3e']
        #dtgfv3e=wxdtgs['fv3e']
        #dtgfimx=wxdtgs['fimx']

        if(onKaze):
            dtgukm=wxdtgs['ukm']
        if(onTenki):
            dtgcmc=wxdtgs['cmc']


        #createTxt="<b>Created: %s %s h</b>  GFS:%s  FIM:%s   FIMX:%s  %s:%s UKM:%s "%(curdtg,curphr,
        #                                                                            dtggfs[6:],
        #                                                                            dtgfim[6:],
        #                                                                            dtgfimx[6:],
        #                                                                            EcmModel.upper(),
        #                                                                            dtgecm[6:],
        #                                                                            dtgukm[6:],
        #                                                       )

        if(dopublic):
            createTxt="<b>Created: %s %s h</b>  GFS:%s  FIM:%s  NAVY:%s "%(curdtg,curphr,
                                                                         dtggfs[6:],
                                                                         dtgfim[6:],
                                                                         dtgnavy[6:],
                                                                         )

        else:
            if(onTenki):
                createTxt="<b>Created: %s %s h</b>&nbsp;&nbsp;&nbsp;  GFS:%s  %s:%s  CMC:%s  NAVY:%s"%(curdtg,curphr,
                                                                                                       dtggfs[6:],
                                                                                                       EcmModel.upper(),dtgecm[6:],
                                                                                                       dtgcmc[6:],
                                                                                                       dtgnavy[6:],
                                                                                                       )

                htmlHead=(self.WxmapCenter,tdtg,dtggfs,dtgecm,dtgecm,dtgecm,dtgcmc,dtgnavy,self.WxmapCenter,tdtg,createTxt,
                          nstm,tctitle)

            if(onKaze):
                createTxt="<b>Created: %s %s h</b>&nbsp;&nbsp;&nbsp;  GFS:%s  %s:%s  UKM:%s  NAVY:%s"%(curdtg,curphr,
                                                                                                       dtggfs[6:],
                                                                                                       EcmModel.upper(),dtgecm[6:],
                                                                                                       dtgukm[6:],
                                                                                                       dtgnavy[6:],
                                                                                                       )
                htmlHead=(self.WxmapCenter,tdtg,dtggfs,dtgecm,dtgecm,dtgecm,dtgukm,dtgnavy,self.WxmapCenter,tdtg,createTxt,
                          nstm,tctitle)


        htm1=''' <html> <head> 
        
<!-- Global site tag (gtag.js) - Google Analytics -->
<script async src=\"https://www.googletagmanager.com/gtag/js?id=G-VG0RC3XML9\"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-VG0RC3XML9');
</script>
        
<title> %s WxMAP2 </title>
<link rel="shortcut icon" href="favicon.ico">
<link rel="stylesheet" type="text/css" href="css/wxmain.css">
<link rel="stylesheet" type="text/css" href="css/dropdown.css">

</head>

<body background="icon/wxmap.bkg.2.gif" TEXT="#000000" LINK="#0000FF" VLINK="#006030">


<script type=\"text/javascript\">
//Contents for menu 1
var menuusnsat=new Array()

menuusnsat[0]='<a href="javascript:cvalue=getW2Url(\\'nrl.sat.troplant\\'),loadW2Html(cvalue,\\'window\\');">nrl-troplant</a>'
menuusnsat[1]='<a href="javascript:cvalue=getW2Url(\\'nrl.sat.tropepac\\'),loadW2Html(cvalue,\\'window\\');">nrl-tropepac</a>'
menuusnsat[2]='<a href="javascript:cvalue=getW2Url(\\'nrl.sat.tropwpac\\'),loadW2Html(cvalue,\\'window\\');">nrl-tropwpac</a>'
menuusnsat[3]='<a href="javascript:cvalue=getW2Url(\\'usn.sat.nfmc-jtwc\\'),loadW2Html(cvalue,\\'window\\');">nmfc-jtwc</a>'

//menuusnsat[2]='<a href="">tropwpac</a>'

var menucira=new Array()
menucira[0]='<a href="javascript:cvalue=getW2Url(\\'cira.tc\\'),loadW2Html(cvalue,\\'window\\');">tc-rammb</a>'
menucira[1]='<a href="javascript:cvalue=getW2Url(\\'cira.ramsdis\\'),loadW2Html(cvalue,\\'window\\');">sat-ramsdis</a>'
menucira[2]='<a href="javascript:cvalue=getW2Url(\\'cira.tcfa\\'),loadW2Html(cvalue,\\'window\\');">tc-genesis</a>'
menucira[3]='<a href="javascript:cvalue=getW2Url(\\'cira.prw\\'),loadW2Html(cvalue,\\'window\\');">sat-prw</a>'

var menussd=new Array()
menussd[0]='<a href="javascript:cvalue=getW2Url(\\'ssd.troplant.vis\\'),loadW2Html(cvalue,\\'window\\');">troplant vis</a>'
menussd[1]='<a href="javascript:cvalue=getW2Url(\\'ssd.troplant.ir\\'),loadW2Html(cvalue,\\'window\\');">troplant ir</a>'
menussd[2]='<a href="javascript:cvalue=getW2Url(\\'ssd.tropepac.vis\\'),loadW2Html(cvalue,\\'window\\');">tropepac vis</a>'
menussd[3]='<a href="javascript:cvalue=getW2Url(\\'ssd.tropepac.ir\\'),loadW2Html(cvalue,\\'window\\');">tropepac ir</a>'

var menucimss=new Array()

//menucimss[0]='<a href="http://cimss.ssec.wisc.edu/tropic/real-time/tpw2/global2/main.html">global prw</a>'
menucimss[0]='<a href="http://tropic.ssec.wisc.edu/real-time/mimic-tpw/global2/main.html">global prw</a>'
menucimss[1]='<a href="http://cimss.ssec.wisc.edu/tropic2/real-time/imagemain.php?&basin=atlantic&prod=irn&sat=g8">images</a>'
menucimss[2]='<a href="http://cimss.ssec.wisc.edu/tropic2/real-time/windmain.php?&basin=atlantic&sat=wg8&prod=wvir&zoom=&time=">winds - lant</a>'
//menucimss[0]='<a href="">troplant vis</a>'

var menucpc=new Array()
menucpc[0]='<a href="http://www.cpc.ncep.noaa.gov/products/precip/CWlink/MJO/enso.shtml">enso</a>'
menucpc[1]='<a href="http://www.cpc.ncep.noaa.gov/products/precip/CWlink/MJO/mjo.shtml">mjo</a>'
menucpc[2]='<a href="http://www.cpc.ncep.noaa.gov/products/hurricane/">hurricanes</a>'
menucpc[3]='<a href="http://www.cpc.ncep.noaa.gov/products/Global_Monsoons/Global-Monsoon.shtml">monsoons</a>'

var menufim=new Array()
menufim[0]='<a href="javascript:cvalue=getW2Url(\\'gsd.fim8.wxmap\\'),loadW2Html(cvalue,\\'window\\');">FIM8 30km (gsd)</a>'
menufim[1]='<a href="javascript:cvalue=getW2Url(\\'gsd.fim9.wxmap\\'),loadW2Html(cvalue,\\'window\\');">FIM9 15km (tacc)</a>'

//menucpc[0]='<a href="">troplant vis</a>'


</script>


<script language="javascript" src="js/dropdown.js" type="text/javascript"></script>
<script language="javascript" src="js/wxmain.js" type="text/javascript"></script>

<script language="javascript">
dtgcur='%s';
dtggfs='%s';
dtgecm='%s';
dtgecmn='%s';
dtgecmg='%s';
dtgukm='%s';
dtgnavy='%s';
dtggsm='%s';

</script>


<table class="main" cellspacing=1 cellpadding=1 border=0>
<tr>
<td class='title'>
%s WxMAP2 - %s
</td>
</tr>

<tr>
<td class='status'>
%s
</td>
</tr>

<tr>
<td class='status9pt'>
TCs(%d): %s
</td>
</tr>

'''%(htmlHead)

        htm=htm1+htm2
        return(htm)

    def HtmlWxmapMain(self,tdtg,curdtg,curphr,template,verb=0,dopublic=0,setEcmModel=None,setNavModel=None):

        from tcbase import TcData
        tD=TcData(dtgopt=tdtg)
        (stmids,btcs)=tD.getDtg(tdtg)

        stmids.sort()

        nstm=len(stmids)
        tctitle=''
        for n in range(0,nstm):
            ostmid=stmids[n]
            vmax=btcs[ostmid][2]
            tt=ostmid.split('.')
            ostmid="%s.%s(%d)"%(tt[0],tt[1][-2:],vmax)
            if(n < nstm-1):
                tctitle=tctitle+"%s | "%(ostmid)
            else:
                tctitle=tctitle+"%s"%(ostmid)

        try:
            htm2=open(template,'r').read()
        except:
            print "EEEE unable to open template: %s"%(template)
            sys.exit()

        iEcmModel=EcmModel
        if(setEcmModel != None): iEcmModel=setEcmModel

        # -- set wxmodel if 'ecmt'
        #
        if(iEcmModel == 'ecmt'):
            self.wxModels=['gfs','fim','ngpc','ecmt','ukm']

        wxdtgs=self.GetWxmapDtgs(tdtg,verb=verb)

        if(iEcmModel == 'ecmn'):
            dtgecm=wxdtgs['ecmn']
        elif(iEcmModel == 'ecmg'):
            dtgecm=wxdtgs['ecmg']
        elif(iEcmModel == 'ecmt'):
            dtgecm=wxdtgs['ecmt']
        else:
            dtgecm=wxdtgs['ecm']

        iNavModel='navg'
        if(setNavModel != None): iNavModel=setNavModel

        iNavModel='navg'
        if(setNavModel != None): iNavModel=setNavModel

        dtgnavy=wxdtgs[iNavModel]

        if(verb):
            for d in wxdtgs.keys():
                print d,wxdtgs[d]



        dtggfs=wxdtgs['gfs']
        dtgcmc=wxdtgs['cmc']
        dtggsm=wxdtgs['gsm']

        createTxt="<b>Created: %s %s h</b>&nbsp;&nbsp;&nbsp;  GFS:%s  %s:%s  CMC:%s  NAVY:%s  GSM:%s"%(curdtg,curphr,
                                                                                               dtggfs[6:],
                                                                                               EcmModel.upper(),dtgecm[6:],
                                                                                               dtgcmc[6:],
                                                                                               dtgnavy[6:],
                                                                                               dtggsm[6:],
                                                                                               )
        
        
        htmlHead=(self.WxmapCenter,tdtg,dtggfs,dtgecm,dtgecm,dtgecm,dtgcmc,dtgnavy,dtggsm,self.WxmapCenter,tdtg,createTxt,
                  nstm,tctitle)


        htm1=''' <html> <head> 

<!-- Global site tag (gtag.js) - Google Analytics -->
<script async src=\"https://www.googletagmanager.com/gtag/js?id=G-VG0RC3XML9\"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-VG0RC3XML9');
</script>

        
<title> %s WxMAP2 </title>
<link rel="shortcut icon" href="favicon.ico">
<link rel="stylesheet" type="text/css" href="css/wxmain.css">
<link rel="stylesheet" type="text/css" href="css/dropdown.css">

</head>

<body background="icon/wxmap.bkg.2.gif" TEXT="#000000" LINK="#0000FF" VLINK="#006030">

<script type=\"text/javascript\">
//Contents for menu 1
var menuusnsat=new Array()

menuusnsat[0]='<a href="javascript:cvalue=getW2Url(\\'nrl.sat.troplant\\'),loadW2Html(cvalue,\\'window\\');">nrl-troplant</a>'
menuusnsat[1]='<a href="javascript:cvalue=getW2Url(\\'nrl.sat.tropepac\\'),loadW2Html(cvalue,\\'window\\');">nrl-tropepac</a>'
menuusnsat[2]='<a href="javascript:cvalue=getW2Url(\\'nrl.sat.tropwpac\\'),loadW2Html(cvalue,\\'window\\');">nrl-tropwpac</a>'
menuusnsat[3]='<a href="javascript:cvalue=getW2Url(\\'usn.sat.nfmc-jtwc\\'),loadW2Html(cvalue,\\'window\\');">nmfc-jtwc</a>'

//menuusnsat[2]='<a href="">tropwpac</a>'

var menucira=new Array()
menucira[0]='<a href="javascript:cvalue=getW2Url(\\'cira.tc\\'),loadW2Html(cvalue,\\'window\\');">tc-rammb</a>'
menucira[1]='<a href="javascript:cvalue=getW2Url(\\'cira.ramsdis\\'),loadW2Html(cvalue,\\'window\\');">sat-ramsdis</a>'
menucira[2]='<a href="javascript:cvalue=getW2Url(\\'cira.tcfa\\'),loadW2Html(cvalue,\\'window\\');">tc-genesis</a>'
menucira[3]='<a href="javascript:cvalue=getW2Url(\\'cira.prw\\'),loadW2Html(cvalue,\\'window\\');">sat-prw</a>'

var menussd=new Array()
menussd[0]='<a href="javascript:cvalue=getW2Url(\\'ssd.troplant.vis\\'),loadW2Html(cvalue,\\'window\\');">troplant vis</a>'
menussd[1]='<a href="javascript:cvalue=getW2Url(\\'ssd.troplant.ir\\'),loadW2Html(cvalue,\\'window\\');">troplant ir</a>'
menussd[2]='<a href="javascript:cvalue=getW2Url(\\'ssd.tropepac.vis\\'),loadW2Html(cvalue,\\'window\\');">tropepac vis</a>'
menussd[3]='<a href="javascript:cvalue=getW2Url(\\'ssd.tropepac.ir\\'),loadW2Html(cvalue,\\'window\\');">tropepac ir</a>'

var menucimss=new Array()

//menucimss[0]='<a href="http://cimss.ssec.wisc.edu/tropic/real-time/tpw2/global2/main.html">global prw</a>'
menucimss[0]='<a href="http://tropic.ssec.wisc.edu/real-time/mimic-tpw/global2/main.html">global prw</a>'
menucimss[1]='<a href="http://cimss.ssec.wisc.edu/tropic2/real-time/imagemain.php?&basin=atlantic&prod=irn&sat=g8">images</a>'
menucimss[2]='<a href="http://cimss.ssec.wisc.edu/tropic2/real-time/windmain.php?&basin=atlantic&sat=wg8&prod=wvir&zoom=&time=">winds - lant</a>'
//menucimss[0]='<a href="">troplant vis</a>'

var menucpc=new Array()
menucpc[0]='<a href="http://www.cpc.ncep.noaa.gov/products/precip/CWlink/MJO/enso.shtml">enso</a>'
menucpc[1]='<a href="http://www.cpc.ncep.noaa.gov/products/precip/CWlink/MJO/mjo.shtml">mjo</a>'
menucpc[2]='<a href="http://www.cpc.ncep.noaa.gov/products/hurricane/">hurricanes</a>'
menucpc[3]='<a href="http://www.cpc.ncep.noaa.gov/products/Global_Monsoons/Global-Monsoon.shtml">monsoons</a>'

var menufim=new Array()
menufim[0]='<a href="javascript:cvalue=getW2Url(\\'gsd.fim8.wxmap\\'),loadW2Html(cvalue,\\'window\\');">FIM8 30km (gsd)</a>'
menufim[1]='<a href="javascript:cvalue=getW2Url(\\'gsd.fim9.wxmap\\'),loadW2Html(cvalue,\\'window\\');">FIM9 15km (tacc)</a>'

//menucpc[0]='<a href="">troplant vis</a>'


</script>


<script language="javascript" src="js/dropdown.js" type="text/javascript"></script>
<script language="javascript" src="js/wxmain.js" type="text/javascript"></script>

<script language="javascript">
dtgcur='%s';
dtggfs='%s';
dtgecm='%s';
dtgecmn='%s';
dtgecmg='%s';
dtgcmc='%s';
dtgnavy='%s';
dtggsm='%s';

</script>


<table class="main" cellspacing=1 cellpadding=1 border=0>
<tr>
<td class='title'>
%s WxMAP2 - %s
</td>
</tr>

<tr>
<td class='status'>
%s
</td>
</tr>

<tr>
<td class='status9pt'>
TCs(%d): %s
</td>
</tr>

'''%(htmlHead)

        htm=htm1+htm2
        return(htm)

class w2Colors(MFbase):

    def __init__(self,verb=0):
        import webcolors
        #Color2Hex={}
        #Color2Hex['black']='#000000'
        #Color2Hex['white']='#FFFFFF'

        #Color2Hex['navy']='#000080'
        #Color2Hex['blue']='#0000FF'
        #Color2Hex['royalblue']='#4169E1'
        #Color2Hex['steelblue']='#4682B4'
        #Color2Hex['usafblue']='#CCCCFF'
        #Color2Hex['mediumslateblue']='#7B68EE'
        #Color2Hex['mediumblue']='#0000CD'
        #Color2Hex['powderblue']='#B0E0E6'
        #Color2Hex['skyblue']='#87CEEB'
        #Color2Hex['lightblue']='#ADD8E6'
        #Color2Hex['deepskyblue']='#00BFFF'
        #Color2Hex['dodgerblue']='#1E90FF'

        #Color2Hex['yellow']='#FFFF00'
        #Color2Hex['gold']='#FFD700'
        #Color2Hex['yellowgreen']='#9ACD32'
        #Color2Hex['khaki']='#F0E68C'
        #Color2Hex['goldenrod']='#DAA520'
        #Color2Hex['lightgoldenrodyellow']='#FAFAD2'
        #Color2Hex['tan']='#D2B48C'
        #Color2Hex['peru']='#CD853F'
        #Color2Hex['sienna']='#A0522D'
        #Color2Hex['chocolate']='#D2691E'


        #Color2Hex['wheat']='#F5DEB3'
        #Color2Hex['usafgrey']='#51588E'
        #Color2Hex['grey']='#808080'

        #Color2Hex['garnet']='#990000'
        #Color2Hex['magenta']='#FF00FF'
        #Color2Hex['maroon']='#800000'

        #Color2Hex['lightgreen']='#90EE00'
        #Color2Hex['green']='#008000'
        #Color2Hex['greenyellow']='#ADFF2F'
        #Color2Hex['olive']='#808000'
        #Color2Hex['olivedrab']='#6B8E23'
        #Color2Hex['mediumturquoise']='#48D1CC'
        
        #Color2Hex['mediumseagreen']='#3CB371'
        #Color2Hex['darkgreen']='#006400'

        #Color2Hex['red']='#FF0000'
        #Color2Hex['tomato']='#FF4637'
        #Color2Hex['indianred']='#CD5C5C'
        #Color2Hex['darkred']='#8B0000'
        #Color2Hex['lightcoral']='#F08080'
        #Color2Hex['orange']='#FFA500'

        #Color2Hex['orchid']='#DA70D6'
        #Color2Hex['violet']='#EE82EE'
        #Color2Hex['fuchsia']='#FF00FF'

        #Color2Hex['purple']='#800080'
        #Color2Hex['indigo']='#4B0082'
        #Color2Hex['plum']='#DDA0DD'
        #Color2Hex['violetred']='#D02090'
        #Color2Hex['teal']='#008080'
        #Color2Hex['atcfland']='#FEDE85'
        #Color2Hex['atcfocean']='#B4FEFE'        

        colors=webcolors.CSS3_NAMES_TO_HEX.keys()
        Color2Hex=webcolors.CSS3_NAMES_TO_HEX
        Color2Hex['grey1']='#CCCCCC'
        Color2Hex['grey2']='#999999'
        Color2Hex['grey3']='#666666'
        Color2Hex['grey4']='#333333'
        Color2Hex['atcfland']='#FEDE85'
        Color2Hex['atcfocean']='#B4FEFE'        
        Color2Hex['violetred']='#D02090'
        
        if(verb):
            colors.sort()
            for color in colors:
                print color,Color2Hex[color]
        
        
        GaColorRgb={}

        GaColorRgb[0] =[0,0,0]
        GaColorRgb[1] =[255,255,255]
        GaColorRgb[2] =[250,60,60]
        GaColorRgb[3] =[0,220,0]
        GaColorRgb[4] =[30,60,255]
        GaColorRgb[5] =[0,200,200]
        GaColorRgb[6] =[240,0,130]
        GaColorRgb[7] =[230,220,50]
        GaColorRgb[8] =[240,130,40]
        GaColorRgb[9] =[160,0,200]
        GaColorRgb[10]=[160,230,50]
        GaColorRgb[11]=[0,160,255]
        GaColorRgb[12]=[230,175,45]
        GaColorRgb[13]=[0,210,140]
        GaColorRgb[14]=[130,0,220]
        GaColorRgb[15]=[170,170,170]

        GaColorName2Rgb={}
        GaColorName2Rgb['black']=GaColorRgb[0] 
        GaColorName2Rgb['white']=GaColorRgb[1] 
        GaColorName2Rgb['red']=GaColorRgb[2] 
        GaColorName2Rgb['green']=GaColorRgb[3] 
        GaColorName2Rgb['blue']=GaColorRgb[4] 
        GaColorName2Rgb['lightblue']=GaColorRgb[5] 
        GaColorName2Rgb['magenta']=GaColorRgb[6] 
        GaColorName2Rgb['yellow']=GaColorRgb[7] 
        GaColorName2Rgb['orange']=GaColorRgb[8] 
        GaColorName2Rgb['purple']=GaColorRgb[9] 
        GaColorName2Rgb['yellowgreen']=GaColorRgb[10]
        GaColorName2Rgb['mediumblue']=GaColorRgb[11]
        GaColorName2Rgb['darkyellow']=GaColorRgb[12]
        GaColorName2Rgb['aqua']=GaColorRgb[13]
        GaColorName2Rgb['darkpurple']=GaColorRgb[14]
        GaColorName2Rgb['gray']=GaColorRgb[15]

        #  0   background       0   0   0 (black by default)
        #  1   foreground     255 255 255 (white by default)
        #  2   red            250  60  60 
        #  3   green            0 220   0 
        #  4   dark blue       30  60 255 
        #  5   light blue       0 200 200 
        #  6   magenta        240   0 130 
        #  7   yellow         230 220  50 
        #  8   orange         240 130  40 
        #  9   purple         160   0 200 
        # 10   yellow/green   160 230  50 
        # 11   medium blue      0 160 255 
        # 12   dark yellow    230 175  45 
        # 13   aqua             0 210 140 
        # 14   dark purple    130   0 220 
        # 15   gray           170 170 170

        self.chex=Color2Hex
        self.W2Colors=Color2Hex
        self.cga=GaColorName2Rgb

        JaeCols={
            #light yellow to dark red
            21:'#FFFAAA',  # 255 250 170
            22:'#FFE878',  # 255 232 120
            23:'#FFC03C',  # 255 192 060
            24:'#FFA000',  # 255 160 000
            25:'#FF6000',  # 255 096 000
            26:'#FF3200',  # 255 050 000
            27:'#E11400',  # 225 020 000
            28:'#C00000',  # 192 000 000
            29:'#A50000',  # 165 000 000


            #light green to dark green
            31:'#E6FFE1',  # 230 255 225
            32:'#C8FFBE',  # 200 255 190
            33:'#B4FAAA',  # 180 250 170
            34:'#96F58C',  # 150 245 140
            35:'#78F573',  # 120 245 115
            36:'#50F050',  # 080 240 080
            37:'#37D23C',  # 055 210 060
            38:'#1EB41E',  # 030 180 030
            39:'#0FA00F',  # 015 160 015

            #light blue to dark blue
            41:'#C8FFFF',  # 200 255 255
            42:'#AFF0FF',  # 175 240 255
            43:'#82D2FF',  # 130 210 255
            44:'#5FBEFA',  # 095 190 250
            45:'#4BB4F0',  # 075 180 240
            46:'#3CAAE6',  # 060 170 230
            47:'#2896D2',  # 040 150 210
            48:'#1E8CC8',  # 030 140 200
            49:'#1482BE',  # 020 130 190

            #light purple to dark purple
            51:'#DCDCFF',  # 220 220 255
            52:'#C0B4FF',  # 192 180 255
            53:'#A08CFF',  # 160 140 255
            54:'#8070EB',  # 128 112 235
            55:'#7060DC',  # 112 096 220
            56:'#483CC8',  # 072 060 200
            57:'#3C28B4',  # 060 040 180
            58:'#2D1EA5',  # 045 030 165
            59:'#2800A0',  # 040 000 160

            #light pink to dark rose  
            61:'#FFE6E6',  # 255 230 230
            62:'#FFC8C8',  # 255 200 200
            63:'#F8A0A0',  # 248 160 160
            64:'#E68C8C',  # 230 140 140
            65:'#E67070',  # 230 112 112
            66:'#E65050',  # 230 080 080
            67:'#C83C3C',  # 200 060 060
            68:'#B42828',  # 180 040 040
            69:'#A42020',  # 164 032 032


            #light grey to dark grey
            71:'#FAFAFA',  # 250 250 250
            72:'#C8C8C8',  # 200 200 200
            73:'#A0A0A0',  # 160 160 160
            74:'#8C8C8C',  # 140 140 140
            75:'#707070',  # 112 112 112
            76:'#505050',  # 080 080 080
            77:'#3C3C3C',  # 060 060 060
            78:'#282828',  # 040 040 040
            79:'#202020',  # 032 032 032
        }

        self.JaeCols=JaeCols


    def hex2dec(self,s):
        return int(s, 16)

    def dec2hex(self,n):
        """return the hexadecimal string representation of integer n"""
        return "%X" % n

    def hex2rgb(self,scolor):

        r=self.hex2dec(scolor[1:3])
        g=self.hex2dec(scolor[3:5])
        b=self.hex2dec(scolor[5:7])
        return(r,g,b)



class GaProc(MFbase):
    """ object to hang a 'ga' to pass between processing objects"""

    def __init__(self,ga=None,
                 verb=0,
                 ctlpath=None,
                 Quiet=1,
                 Window=0,
                 Opts='',
                 doLogger=0,
                 Bin='grads',
                 ):

        self.ga=ga
        self.verb=verb
        self.ctlpath=ctlpath
        self.Quiet=Quiet
        self.Window=Window
        self.Opts=Opts
        self.doLogger=doLogger
        self.Bin=Bin

    def initGA(self,ctlpath=None,doreinit=0):

        # -- do grads: 1) open files; 2) get field data
        # -- decorate the GaProc (gaP) object
        #
        if(self.ga == None):
            print 'w2.GaProc MMMMMM -- making self.ga'
            from ga2 import setGA
            ga=setGA(Opts=self.Opts,Quiet=self.Quiet,Window=self.Window,doLogger=self.doLogger,verb=self.verb,Bin=self.Bin)
            self.ga=ga
            self.ge=ga.ge
            
        else:
            ga=self.ga
            ge=self.ge

        if(doreinit): ga('reinit')

        if(self.ctlpath != None or ctlpath != None):
            if(self.ctlpath != None):
                print 'w2.GaProc OOOOO -- open self.ctlpath: ',self.ctlpath
                ga.fh=ga.open(self.ctlpath)
            if(ctlpath != None):
                print 'w2.GaProc OOOOO -- open ctlpath: ',ctlpath
                ga.fh=ga.open(ctlpath)

            ge=ga.ge
            ge.fh=ga.fh
            ge.getFileMeta()
            self.ga=ga
            self.ge=ga.ge

        self.gp=self.ga.gp



class procGA(MFbase):

    w2=W2Base()
    
    def __init__(self,
                 ctlpath,
                 gaQuiet=1,
                 gaWindow=0,
                 gadoLogger=0,
                 gaOpts='',
                 xsize=1440,
                 ):


        # --set put gaP objects...
        """

"""
        self.xsize=xsize
        aspect=self.w2.W2plotAspect
        self.ysize=int(self.xsize*aspect) 
        self.ctlpath=ctlpath
        
        self.gaopt='-g 20+20+%dx%d'%(self.xsize,self.ysize)
        self.gaopt=''
        self.gaQuiet=gaQuiet
        self.gaWindow=gaWindow
        self.gadoLogger=gadoLogger
        self.gaOpts=gaOpts
       

        self.gaP=GaProc(
            Quiet=self.gaQuiet,
            Window=self.gaWindow,
            Opts=self.gaOpts,
            doLogger=self.gadoLogger,
        )

    def getGAfromGaProc(self,
                        ):

        # -- force ga options from self -- now done by passing TcgenGP() to Tcgen
        #
        #if(not(hasattr(self,'gaP'))):
        #    self.gaP=GaProc(Quiet=self.gaQuiet,Opts=self.gaOpts)

        if(not(hasattr(self,'ga'))):

            # -- doreinit reinits the grads obj
            #
            self.gaP.initGA(ctlpath=self.ctlpath,doreinit=1)
            ga=self.gaP.ga
            
            lsctl="%s/ls.1deg.ctl"%(self.w2.geodir)
            ga("open %s"%(lsctl))
            ge=ga.ge
            gp=ga.gp

            self.ga=ga
            self.ge=ge
            self.gp=gp

        else:
            self.ga('q files')
            self.ga('close 1')
            self.ga('close 2')
            self.ga('open %s'%(self.ctlpath))
            lsctl="%s/ls.1deg.ctl"%(self.w2.geodir)
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

def setXgrads(useStandard=0,useX11=1,returnBoth=0):
    
    if(useStandard):
        xgrads='grads'
        rc=xgrads
        if(returnBoth): rc=(xgrads,xgrads)
        return(rc)
    
    bdirApp=os.getenv('W2_BDIRAPP')
    gradsVersion='opengrads-2.2.1.oga.1'

    xgradsX='%s/%s/Contents/gradsX11'%(bdirApp,gradsVersion)
    xgrads='%s/%s/Contents/grads'%(bdirApp,gradsVersion)

    if(xgrads == None):
        print 'EEEE----XXXGGGRRRAAADDDSSS - xgrads not set!!!'
        sys.exit()
    
    if(useX11):     rc=xgradsX
    else:           rc=xgrads
    if(returnBoth): rc=(xgradsX,xgrads)
    return(rc)

def setPngquant():
    
    xpngquant='/usr/bin/pngquant'
    if(onTenki):
        xpngquant='/usr/bin/pngquant'
        
    return(xpngquant)

def getTausFromTauopt(tauopt,taui=6):
    
    taus=[]
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

        for tau in range(taub,taue+1,taui):
            taus.append(tau)

    return(taus)


def rsync2Wxmap2(localweb='all',stmid=None,ropt='',doCommand2=0,
                 doBail=1,noRsync=0):
    
    sdir=W2BaseDirWebConfig  # from w2globalvars.py
    lbdir=HfipWebBdir        # from w2localvars.py -- not consistent but...
    noRsync=not(W2doRsync2Wxmap2)

    tdir='''mfiorino@wxmap2.com:/home3/mfiorino'''
    rsyncopt='''rsync -alv --rsh="ssh -p2222" --timeout=300'''
    if(localweb == 'all'):
        webs=['tcact','tcgen','jtdiag','wxmap2','tceps']
    else:
        webs=[localweb]
        
    if(noRsync):
        print 'wxmap2.com down -- no rsync for webs: ',str(webs)
        return

    for web in webs:

        # -- first rsync to local drive because the data dirs to be rsync will be cleaned
        #    by w2-clean-hfip.py
        # -- the long term store is in 
        #
        # W2EnvVarHfipDat/
        #                 jtdiagDAT
        #                 tcepsDAT
        #                 tcgenDAT
        #                 tcdiagDAT
        
        if(web != 'tcact' and web != 'wxmap2' and
           web != 'tctrkveri'
#           web != 'tctrkveri' and web != 'tcgen' and
#           web != 'tctrkveri' and
#           web != 'tceps'
           ):
            curyear=mf.dtg()[0:4]
            lsdir="%s/%s/%s"%(sdir,web,curyear)
            ltdir="%s/%sDAT/%s"%(lbdir,web,curyear)
            cmd="rsync -alv %s/ %s/"%(lsdir,ltdir)
            mf.runcmd(cmd,ropt)
            
            
        tweb=web
        if(web == 'wxmap2'):
            #sdir="%s/.."%(os.getenv('W2_HFIP'))
            #sdir="%s"%(os.getenv('W2_HFIP'))
            sdir=HfipProducts
            tdir='''mfiorino@wxmap2.com:/home3/mfiorino'''
            rsyncopt='''rsync -alv --copy-links --rsh="ssh -p2222" --timeout=300'''
            tweb='maps'

        elif(web == 'tceps'):
            tdir='''mfiorino@wxmap2.com:/home3/mfiorino'''
            rsyncopt='''rsync -alv --copy-links --rsh="ssh -p2222"'''
            tweb=web

        elif(web == 'tcgen'):
            tdir='''mfiorino@wxmap2.com:/home3/mfiorino'''
            rsyncopt='''rsync -alv --copy-links --rsh="ssh -p2222"'''
            tweb=web

        elif(web == 'tcact'):
            tdir='''mfiorino@wxmap2.com:/home3/mfiorino'''
            rsyncopt='''rsync -alv --exclude "cur" --copy-links --delete --rsh="ssh -p2222"'''
            tweb=web

        elif(web == 'tctrkveri'):
            tdir='''mfiorino@wxmap2.com:/home3/mfiorino'''
            rsyncopt='''rsync -aLv --delete-after --rsh="ssh -p2222"'''
            tweb=web

        cmd='''%s %s/%s/ "%s/%s/"'''%(rsyncopt,sdir,web,tdir,tweb)
        
        if(doCommand2):
            # -- 20211122 -- better handling of error from rsync
            #
            rc=MF.loopCmd2(cmd,nLoop=0)
            orc=rc
            if(len(rc) > 0): orc=rc[0] ; rc=orc
        
            if(rc == 0):
                print '1111-rc: ',rc,"""ropt is 'norun'"""
            elif(rc == 1):
                print 'FFF-good to go...press'
            elif(rc != 1): 
                print 'eee',doBail
                print 'EEEE rsync error DATA...' 
                if(doBail): 
                    print '...BAILing...'
                    sys.exit()
            else:
                print 'EEEEE-rc: ',rc
                if(doBail): 
                    print '...BAILing...'
                    sys.exit()
        
        else:
            MF.sTimer('RRRSSSYYYNNNCCC-CMD')
            mf.runcmd(cmd,ropt)
            MF.dTimer('RRRSSSYYYNNNCCC-CMD')
    


if (__name__ == "__main__"):

    #rc=rsync2Wxmap2('wxmap2',ropt='norun')
    ropt='norun'
    ropt=''
    web='wxmap2'
    #web='tctrkveri'
    # -- 20210122 -- reorg to be consistent with mike2
    #web='jtdiag'
    #web='tcgen'
    #web='tceps'
    #web='tctrkveri'
    #web='tcact'
    #web='tceps'
    #rc=rsync2Wxmap2(web,ropt=ropt)

    web='tctrkveri'
    web='wxmap2'
    web='jtdiag'
    web='tcdiag'
    web='tcgen'
    web='tcact'
    web='tceps'
    web='tctrkveri'
    
    rc=rsync2Wxmap2(web,ropt=ropt,doBail=0)

    sys.exit()
    w2=W2env()
    w2=W2Base()
    w2.ls()
    sys.exit()

