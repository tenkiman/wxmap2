from WxMAP2 import *
w2=W2()

from GRIB import Grib1,Grib2

from tcbase import AdeckBaseDir


#VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV
# top most variables

m2models=['fim8']
taccmodels=['fim9','f8em','f9em','f0em']
wjetmodels=['rtfim','rtfimx','rtfimy','rtfimz','rtfim7','rtfimR925']

models=['rtfim','rtfimx','rtfimy','rtfimz','rtfim7']
#-- 20110813 -- fimz if off
models=['rtfim','rtfimx','rtfimy','rtfim7']
models=['rtfim','rtfimx','rtfim9','rtfim7']
taumax=168
taumax=240

mssBaseCleanDir='/mss/jet/projects/fim/rtfim'


trootWjet='%s/rtfim'%(w2.WjetW2base)
trootZeus='%s/rtfim'%(w2.ZeusW2base)

if(w2.onWjet):
    lrootWjet="%s/rtfim"%(w2.Nwp2DataBdir)
elif(w2.onZeus):
    lrootWjet=trootZeus
else:
    lrootWjet="%s/%s/rtfim"%(sbaseWjet,w2.Nwp2DataBdir)

lrootLocal="%s/rtfim"%(w2.Nwp2DataBdir)

rsyncServerJet='%s@%s'%(w2.WjetScpServerLogin,w2.WjetScpServer)
rsyncServerZeus='%s@%s'%(w2.ZeusScpServerLogin,w2.ZeusScpServer)
rsyncServerKishou='fiorino@kishou.fsl.noaa.gov'
rsyncOpt='--protocol=29 --timeout=60 -alv -u'


# -- climo and verif dirs
#
cmeandir='/lfs2/projects/rtfim/cmean'
gfsverifdir='/lfs2/projects/rtfim/verif/GFS'


class rtfimRuns(MFbase):

    runs={
        'rtfim':                    'FIM',
        'rtfimx':                   'FIMX',
        'rtfimy':                   'FIMY',
        'rtfimz':                   'FIMZ',
        'rtfim7':                   'FIM7',
        'rtfim9':                   'FIM9',
        'rtfimz9':                  'FIMZ9',
        'rtfimz_r1163':             'FIMZRETRO1163',
        'rtfimz_retro':             'FIMZretro',
        'rtfim_r1174':              'FIMRETRO1174',
        'rtfim_r1216':              'FIMRETRO1216',
        'rtfim_r1196':              'FIMRETRO1196',
        'rtfim_r1216a':             'FIMRETRO1216A',
        'rtfimz_r1094a':            'FIMZRETRO1094A',
        'portal_r1216a':            'FIMR1216',
        'rtfim_r925':               'FIM_retro_r925',
        'rtfim_r1226':              'FIMRETROPHYS1226',
        'rtfim_r1231':              'FIMRETROPHYS1231',
        'rtfim_r1094b':             'FIMretro2009NewPhys1094b',
        'rtfim_r1272':              'FIMRETRO1272',
        'rtfim_r1273':              'FIMRETRO1273',
        'rtfim_r1273a':             'FIMRETRO1273_INFC_SM_0',
        'rtfim_r1273enkf':          'FIMRETRO1273_ENKF',
        'rtfim_r1291g7':            'FIMRETRO1291_G7',
        'rtfim_r1359enkf':          'FIMRETRO1359_ENKF',
        'rtfim_r1411enkf':          'FIMRETRO1411_ENKF',
        'rtfim_r1422enkf':          'FIMRETRO1422_ENKF',
        'rtfim_r1422gfs':           'FIMRETRO1422_GFS',
        'rtfim_r1422gfsG7':         'FIMRETRO1422_GFS_G7',
        'rtfimy_enkf':              'FIMY_ENKF',
        'rtfim_r1422gfsG7L38':      'FIMRETRO1422_GFS_G7_L38',
        'rtfim_r1607gfsG7':         'FIMRETRO1607_GFS_G7',
        'rtfim_r1633gfsG7L38':      'FIMRETRO1633_GFS_G7_L38',
        'rtfim_r1607gfsG7cugd':     'FIMRETRO1607_GFS_G7_CUGD_CNT',
        'rtfim_r1607gfsG7cutneg':   'FIMRETRO1607_GFS_G7_CUGD_T_NEG',
        'rtfim_r1607gfsG7cutneg':   'FIMRETRO1607_GFS_G7_CUGD_T_NEG',
        'rtfim_r1422gfsdpsig20':    'FIMRETRO1422_GFS_DPSIG20',
        'rtfim_r1422gfspi0':        'FIMRETRO1422_GFS_PI_0',
        'rtfimz_r1163':             'FIMZretro_r1163',
        'rtfim_r1831pcmadv':        'FIMRETRO1831_PCMADV',
        'rtfim_r1831gfsg8':         'FIMRETRO1831_GFS_G8',
        'rtfim_r1831plm1':          'FIMRETRO1831_PLM1',
        'rtfim_r1831plm1vdif05':    'FIMRETRO1831_PLM1_VDIF05',
        'rtfim_r1831plm1vdif10':    'FIMRETRO1831_PLM1_VDIF1',
        'rtfim_r1926':              'FIMRETRO1926',
        'rtfim_r1868gfsG7cugd':     'FIMRETRO1878_GFS_G7_CD_CNT',

        'rtfim_r1926phys1d':        'FIMRETRO1926_PHYS1DT',
        'rtfim_r2159intfc500':      'FIMRETRO2159_INTFC200',
        'rtfim_r2176sigma':         'FIMRETRO2176_SIGMA',
        'rtfim_r2093phys1dsig':     'FIMRETRO2093_PHYSTEND_SIGMA',
        'rtfim_r2220intfc150':      'FIMRETRO2220_INTFC150',

        'rtfim_r2371hyb':           'FIMRETRO2371_HYB',
        'rtfim_r2371vdiff':         'FIMRETRO2371_VDIFF',
        'rtfim_r2608g9zeus':        'FIM9RETRO',
        'rtfim_r2710isaac':         'FIMRETRO_ISAAC',
        'rtfim_r2710isaacZ':	    'FIMRETRO_ISAAC_ZEUS',
        'rtfim_r2647jpgf':          'FIMRETRO_janjic_pgf',
        'rtfim_r2796isaacjpgf':     'FIMRETRO_ISAAC_ZEUS_jpgf',
        'rtfim_r2799isaacnojpgf':       'FIMRETRO_ISAAC_ZEUS_nojpgf',
        'rtfim_r2799isaacnojpgf_plm':   'FIMRETRO_ISAAC_ZEUS_nojpgf_plm',
        'rtfim_r4370_2012gwd':           'FIMRETRO_2012gwd',
        
    }





    def __init__(self,
                 name='rtfim',
                 npe='240',
                 g='8',
                 nlvl='64',
                 fimrun=None,
                 expname='',
                 ):

        self.name=name
        self.npe=npe
        self.g=g
        self.nlvl=nlvl
        self.expname=expname

        if(fimrun != None):
            self.getRun(fimrun)
            if(self.fimrun == None):
                print 'EEE in rtfimRuns.getRun() for fimrun: ',fimrun,' not there...'
                sys.exit()
        else:
            self.fimrun=None


    def getRun(self,run):

        self.name=None
        self.fimrun=None
        self.whereRun='jet'
        self.lrootLocal=lrootLocal
        
        self.useDtgDirName=0

        # -- real-time runs on jet
        #
        if(run == 'rtfim'):
            self.name=run;self.g='8';self.npe='240';self.fimrun=self.runs[run]
            self.useDtgDirName=1
            
        elif(run == 'rtfimx'):
            self.name=run;self.g='7';self.npe='120';self.fimrun=self.runs[run]
            self.name=run;self.g='7';self.npe='240';self.fimrun=self.runs[run]
            self.useDtgDirName=1
            self.taumax=168

            
        elif(run == 'rtfim7'):
            self.name=run;self.g='7';self.npe='120';self.fimrun=self.runs[run]
            self.useDtgDirName=1

        elif(run == 'rtfim9'):
            self.name=run;self.g='9';self.npe='800';self.fimrun=self.runs[run]
            self.name=run;self.g='9';self.npe='1200';self.fimrun=self.runs[run]
            self.name=run;self.g='9';self.npe='1600';self.fimrun=self.runs[run]
            self.useDtgDirName=1

        # -- less/occasional real-time on jet
        #
        elif(run == 'rtfimy'):
            self.name=run;self.g='8';self.npe='240';self.fimrun=self.runs[run]
            # -- from jeff's reservation
            self.name=run;self.g='8';self.npe='600';self.fimrun=self.runs[run]

        elif(run == 'rtfimz'):
            self.name=run;self.g='8';self.npe='120';self.fimrun=self.runs[run]
            self.name=run;self.g='8';self.npe='240';self.fimrun=self.runs[run]
            self.useDtgDirName=1

        elif(run == 'rtfimz9'):
            self.name=run;self.g='9';self.npe='800';self.fimrun=self.runs[run]

        # -- experiments
        #
        elif(run == 'rtfimz_r1163'):
            self.name=run;self.g='8';self.npe='120';self.fimrun=self.runs[run]

        elif(run == 'rtfim_r1174'):
            self.name=run;self.g='8';self.npe='120';self.fimrun=self.runs[run]

        elif(run == 'rtfim_r1216' or run == 'rtfim_r1216a' ):
            self.name=run;self.g='8';self.npe='120';self.fimrun=self.runs[run]
            self.srootWjet='/lfs2/projects/rtfim/%s'%(self.fimrun)

        elif(run == 'portal_r1216a'):
            self.name=run;self.g='8';self.npe='120';self.fimrun=self.runs[run]
            self.srootWjet='/lfs2/projects/fim/fiorino/portal/%s'%(self.fimrun)

        elif(run == 'rtfim_r1196'):
            self.name=run;self.g='8';self.npe='120';self.fimrun=self.runs[run]
            self.srootWjet='/lfs2/projects/rtfim/%s'%(self.fimrun)

        elif(run == 'rtfimz_retro'):
            self.name=run;self.g='8';self.npe='120';self.fimrun=self.runs[run]


        elif(run == 'rtfim_r925' or
             run == 'rtfimz_r1094a' or
             run == 'rtfim_r1094b' or
             run == 'rtfim_r1226' or
             run == 'rtfim_r1231' or
             run == 'rtfim_r1272' or
             run == 'rtfim_r1273' or
             run == 'rtfim_r1273a' or
             run == 'rtfim_r1273enkf' or
             run == 'rtfim_r1359enkf'
             ):
            self.name=run;self.g='8';self.npe='120';self.fimrun=self.runs[run]
            self.srootWjet='/lfs2/projects/rtfim/%s'%(self.fimrun)

        elif(run == 'rtfim_r1411enkf' or
             run == 'rtfim_r1422enkf' or
             run == 'rtfim_r1422gfs'
             ):
            self.name=run;self.g='8';self.npe='240';self.fimrun=self.runs[run]
            self.srootWjet='/lfs0/projects/rtfim/%s'%(self.fimrun)


        elif(run == 'rtfim_r1291g7'
             ):
            self.name=run;self.g='7';self.npe='120';self.fimrun=self.runs[run]
            self.srootWjet='/lfs2/projects/rtfim/%s'%(self.fimrun)



        elif(run == 'rtfim_r1422gfsG7'
             ):
            self.name=run;self.g='7';self.npe='120';self.fimrun=self.runs[run]
            self.srootWjet='/lfs0/projects/rtfim/%s'%(self.fimrun)

        elif(run == 'rtfim_r1422gfsG7L38'
             ):
            self.name=run;self.g='7';self.npe='120';self.nlvl='38';self.fimrun=self.runs[run]
            self.srootWjet='/lfs0/projects/rtfim/%s'%(self.fimrun)

        elif(run == 'rtfim_r1607gfsG7'
             ):
            self.name=run;self.g='7';self.npe='120';self.nlvl='64';self.fimrun=self.runs[run]
            self.srootWjet='/lfs0/projects/rtfim/%s'%(self.fimrun)

        elif(run == 'rtfimy_enkf'
             ):
            self.name=run;self.g='8';self.npe='600';self.fimrun=self.runs[run]
            self.srootWjet='/lfs0/projects/rtfim/%s'%(self.fimrun)

        elif(run == 'rtfim_r1633gfsG7L38'
             ):
            self.name=run;self.g='7';self.npe='120';self.nlvl='38';self.fimrun=self.runs[run]
            self.srootWjet='/lfs0/projects/rtfim/%s'%(self.fimrun)

        elif(run == 'rtfim_r1607gfsG7cugd'
             ):
            self.name=run;self.g='7';self.npe='120';self.nlvl='64';self.fimrun=self.runs[run]
            self.srootWjet='/lfs2/projects/rtfim/%s'%(self.fimrun)

        elif(run == 'rtfim_r1607gfsG7cutneg'
             ):
            self.name=run;self.g='7';self.npe='120';self.nlvl='64';self.fimrun=self.runs[run]
            self.srootWjet='/lfs2/projects/rtfim/%s'%(self.fimrun)

        elif(run == 'rtfim_r1422gfsdpsig20'
             ):
            self.name=run;self.g='8';self.npe='120';self.nlvl='64';self.fimrun=self.runs[run]
            self.srootWjet='/lfs0/projects/rtfim/%s'%(self.fimrun)

        elif(run == 'rtfim_r1422gfspi0'
             ):
            self.name=run;self.g='8';self.npe='120';self.nlvl='64';self.fimrun=self.runs[run]
            self.srootWjet='/lfs0/projects/rtfim/%s'%(self.fimrun)

        elif(run == 'rtfimz_r1163'
             ):
            self.name=run;self.g='8';self.npe='120';self.nlvl='64';self.fimrun=self.runs[run]
            self.srootWjet='/lfs0/projects/rtfim/%s'%(self.fimrun)

        elif(run == 'rtfim_r1831pcmadv'
             ):
            self.name=run;self.g='8';self.npe='240';self.nlvl='64';self.fimrun=self.runs[run]
            self.srootWjet='/lfs2/projects/rtfim/%s'%(self.fimrun)

        elif(run == 'rtfim_r1831gfsg8'
             ):
            self.name=run;self.g='8';self.npe='240';self.nlvl='64';self.fimrun=self.runs[run]
            self.srootWjet='/lfs2/projects/rtfim/%s'%(self.fimrun)

        elif(run == 'rtfim_r1831plm1'
             ):
            self.name=run;self.g='8';self.npe='240';self.nlvl='64';self.fimrun=self.runs[run]
            self.srootWjet='/lfs2/projects/rtfim/%s'%(self.fimrun)

        elif(run == 'rtfim_r1831plm1vdif05'
             ):
            self.name=run;self.g='8';self.npe='240';self.nlvl='64';self.fimrun=self.runs[run]
            self.srootWjet='/lfs2/projects/rtfim/%s'%(self.fimrun)

            print 'sssss ',self.srootWjet

        elif(run == 'rtfim_r1831plm1vdif10'
             ):
            self.name=run;self.g='8';self.npe='240';self.nlvl='64';self.fimrun=self.runs[run]
            self.srootWjet='/pan2/projects/fim-njet/%s'%(self.fimrun)

        elif(run == 'rtfim_r1926'
             ):
            self.name=run;self.g='8';self.npe='240';self.nlvl='64';self.fimrun=self.runs[run]
            self.srootWjet='/pan2/projects/fim-njet/%s'%(self.fimrun)

        elif(run == 'rtfim_r1926phys1d'
             ):
            self.name=run;self.g='8';self.npe='240';self.nlvl='64';self.fimrun=self.runs[run]
            self.srootWjet='/pan2/projects/fim-njet/%s'%(self.fimrun)

        elif(run == 'rtfim_r2159intfc500'
             ):
            self.name=run;self.g='8';self.npe='240';self.nlvl='64';self.fimrun=self.runs[run]
            self.srootWjet='/lfs2/projects/rtfim/%s'%(self.fimrun)

        elif(run == 'rtfim_r2176sigma'
             ):
            self.name=run;self.g='8';self.npe='240';self.nlvl='64';self.fimrun=self.runs[run]
            self.srootWjet='/lfs2/projects/rtfim/%s'%(self.fimrun)

        elif(run == 'rtfim_r2093phys1dsig'
             ):
            self.name=run;self.g='8';self.npe='240';self.nlvl='64';self.fimrun=self.runs[run]
            self.srootWjet='/lfs2/projects/rtfim/%s'%(self.fimrun)

        elif(run == 'rtfim_r2220intfc150'
             ):
            self.name=run;self.g='8';self.npe='240';self.nlvl='64';self.fimrun=self.runs[run]
            self.srootWjet='/pan2/projects/fim-njet/%s'%(self.fimrun)

        elif(run == 'rtfim_r2608g9zeus'
             ):
            self.name=run;self.g='9';self.npe='800';self.nlvl='64';self.fimrun=self.runs[run]
            self.srootWjet='/scratch1/portfolios/BMC/fim/%s'%(self.fimrun)

        elif(run == 'rtfim_r2710isaac'
             ):
            self.dtgopt='2012081700.2012082900.24'
            self.name=run;self.g='8';self.npe='240';self.nlvl='64';self.fimrun=self.runs[run]
            self.srootWjet='/lfs2/projects/fim-njet/%s'%(self.fimrun)

        elif(run == 'rtfim_r2710isaacZ'
             ):
            self.dtgopt='2012081700.2012082912.12'
            self.name=run;self.g='8';self.npe='240';self.nlvl='64';self.fimrun=self.runs[run]
            self.srootWjet='/scratch2/portfolios/BMC/fim/%s'%(self.fimrun)
            self.whereRun='zeus'

        elif(run == 'rtfim_r2647jpgf'
             ):
            self.name=run;self.g='8';self.npe='240';self.nlvl='64';self.fimrun=self.runs[run]
            self.srootWjet='/scratch2/portfolios/BMC/rtfim/%s'%(self.fimrun)

        elif(run == 'rtfim_r2796isaacjpgf'
             ):
            self.dtgopt='2012081700.2012082912.12'
            self.name=run;self.g='8';self.npe='240';self.nlvl='64';self.fimrun=self.runs[run]
            self.srootWjet='/scratch2/portfolios/BMC/rtfim/%s'%(self.fimrun)
            self.whereRun='zeus'

        elif(run == 'rtfim_r2799isaacnojpgf'
             ):
            self.dtgopt='2012081700.2012082912.12'
            self.name=run;self.g='8';self.npe='240';self.nlvl='64';self.fimrun=self.runs[run]
            self.srootWjet='/scratch2/portfolios/BMC/rtfim/%s'%(self.fimrun)
            self.whereRun='zeus'
            if(not(w2.onWjet or w2.onZeus)): self.troot=self.lrootLocal

        elif(run == 'rtfim_r2799isaacnojpgf_plm'
             ):
            self.dtgopt='2012081700.2012082912.12'
            self.name=run;self.g='8';self.npe='240';self.nlvl='64';self.fimrun=self.runs[run]
            self.srootWjet='/scratch2/portfolios/BMC/rtfim/%s'%(self.fimrun)
            self.lrootLocal='/w21/dat/nwp2/rtfim'
            self.whereRun='zeus'
            if(not(w2.onWjet or w2.onZeus)): self.troot=self.lrootLocal

        elif(run == 'rtfim_r4370_2012gwd'
             ):
            #self.dtgopt='2013120100.2014022800.24'
            self.name=run;self.g='8';self.npe='240';self.nlvl='64';self.fimrun=self.runs[run]
            self.srootWjet='/scratch2/portfolios/BMC/fim/%s'%(self.fimrun)
            #self.lrootLocal='/w21/dat/nwp2/rtfim'
            self.whereRun='zeus'
            if(not(w2.onWjet or w2.onZeus)): self.troot=self.lrootLocal

        if(hasattr(self,'dtgopt')): self.dtgs=mf.dtg_dtgopt_prc(self.dtgopt)

        if(not(w2.onWjet or w2.onZeus)): self.troot=self.lrootLocal

        if(hasattr(self,'dtgopt')): self.dtgs=mf.dtg_dtgopt_prc(self.dtgopt)

        if(hasattr(self,'srootWjet')):
            self.srootWjet=os.path.realpath('%s'%(self.srootWjet))
        else:
            self.srootWjet=os.path.realpath('%s/%s'%(srootWjet,self.fimrun))
            
        if(w2.onZeus): self.troot=self.lrootLocal

        return(self)

    def getRunlist(self,nbreak=5):

        runkeys=self.runs.keys()
        runlist=''
        nr=len(runkeys)
        for n in range(0,nr):
            run=runkeys[n]
            if(n == 0):
                if(nr > 1):
                    runlist="%s"%(run)
                else:
                    runlist="%s"%(run)
            elif(n <= nr-1):
                if(n%nbreak != 0):
                    runlist="%s, %s"%(runlist,run)
                else:
                    runlist="%s,\n%s"%(runlist,run)

        return(runlist)

    def getRmodel(self,model):

        try:
            self.fimrun=self.runs[model]
        except:
            self.fimrun='Rmodel=unknown'

        return(self.fimrun)


    def getMyRun(self,val,verb=0):
        """return the key of dictionary dic given the value"""
        try:
            rc=[k for k, v in self.runs.iteritems() if v == val][0]
        except:
            if(verb): print 'RRRRRRRRRRRRRRRRR return .lower() of val: ',val.lower()
            rc=val.lower()
        return (rc)


def getDSslocal(dblocal,model,dtg,verb=1):

    dskey="%s.%s"%(model,dtg)

    bd1="%s/rtfim"%(w2.Nwp2DataBdir)
    bd2="%s/rtfim"%(w2.Nwp2DataBdirArch1)
    bd3="%s/rtfim"%(w2.Nwp2DataBdirArch2)

    lr1="%s/DSs"%(bd1)
    lr2="%s/DSs"%(bd2)
    lr3="%s/DSs"%(bd3)

    DSsl1=DataSets(bdir=lr1,name=dblocal,dtype='model',verb=verb)
    DSsl2=DataSets(bdir=lr2,name=dblocal,dtype='model',verb=verb)
    DSsl3=None

    if(MF.ChkDir(lr3)):
        DSsl3=DataSets(bdir=lr3,name=dblocal,dtype='model',verb=verb)

    try:     ctl1=DSsl1.getDataSet(dskey).FR.ctlpath
    except:  ctl1=None

    try:     ctl2=DSsl2.getDataSet(dskey).FR.ctlpath
    except:  ctl2=None

    if(ctl2 != None):
        (dir,file)=os.path.split(ctl2)
        dd=dir.split('/')
        datdir=bd2
        for d in dd[len(dd)-3:]:
            datdir="%s/%s"%(datdir,d)
        ctl2="%s/%s"%(datdir,file)

    print '11111111111',ctl1,MF.ChkPath(ctl1)
    print '22222222222',ctl2,MF.ChkPath(ctl2)


    sys.exit()


class Qsub(MFbase):

    def __init__(self,
                 argv=None,
                 project='fim-njet',
                 vmem='1.0G',
                 qname='tctrk',
                 partition='xjet:sjet:vjet:ujet:vjet',
                 runcmd='/lfs2/projects/fim/fiorino/w21/run.cron.tcsh',
                 logdir='/lfs2/projects/fim/fiorino/tmp',
                 doqsub=1,
                 queue='batch',
                 ropt='',
                 min4dtg=40,
                 dtgopt=None,
                 modelopt=None,
                 qsubcmd=None,
                 doKshUnlink=1,
                 procs=2,
                 ):

        if(w2.onZeus): 
            project='fim'
            partition='zeus'
            runcmd='/scratch1/portfolios/BMC/fim/fiorino/w21/run.cron.tcsh'
            logdir='/scratch1/portfolios/BMC/fim/fiorino/tmp'

        if(w2.onTheia): 
            project='fim'
            partition='theia'
            runcmd='/scratch3/BMC/fim/fiorino/w21/run.cron.tcsh'
            logdir='/scratch3/BMC/fim/fiorino/tmp'

        self.argv=argv
        self.qsubcmd=qsubcmd

        if(self.argv != None):  (pydir,pycmd)=os.path.split(self.argv[0])
        
        if(self.qsubcmd != None):
            (pydir,pycmd)=os.path.split(self.qsubcmd)

        self.pydir=pydir
        self.pycmd=pycmd

        self.project=project
        self.vmem=vmem
        self.qname=qname
        self.queue=queue
        self.procs=procs
        self.partition=partition
        self.runcmd=runcmd

        self.logdir=logdir
        self.doqsub=doqsub
        self.ropt=ropt
        self.min4dtg=min4dtg
        self.dtgopt=dtgopt
        self.modelopt=modelopt
        self.doKshUnlink=doKshUnlink

        self.initQsub()



    def initQsub(self):

        if(self.argv != None and self.dtgopt == None): 
            self.dtgopt=self.argv[1]
            
        if(self.dtgopt != None): 
            dtgs=mf.dtg_dtgopt_prc(self.dtgopt)
        else:
            print 'EEE Qsub.initQsub: both self.argv and self.dtgopt == None, sayoonara...'
            sys.exit()

        if(self.argv != None and len(self.argv) > 2 and self.modelopt == None): 
            self.modelopt=self.argv[2]
            
        if(self.modelopt != None):
            modelopt=self.modelopt
        else:
            print 'EEE Qsub.initQsub: both self.argv and self.modelopt == None, sayoonara...'
            sys.exit()


        ndtgs=len(dtgs)

        totmin=self.min4dtg*ndtgs
        nmin=totmin%60
        nhour=totmin/60
        
        rttime="%02d:%02d:00"%(nhour,nmin)

        if(ndtgs == 1):
            dtg=dtgs[0]
            pyopt=dtg
            nargstart=2
        else:
            pyopt=self.dtgopt
            nargstart=2

        pytag="%s_%s"%(self.qname,modelopt[2:])
        for arg in self.argv[nargstart:]:
            if(arg != '-Q' and arg != '-V' and arg != '-N'):
                arg=arg.strip()
                pyopt="%s %s"%(pyopt,arg)
            elif(arg == '-N'):
                self.ropt='norun'

        curdtg=mf.dtg('dtg_mn')
        outpath="%s/out_%s_%s_%s.txt"%(self.logdir,pytag,self.dtgopt,curdtg)
        logpath="%s/log_%s_%s_%s.txt"%(self.logdir,pytag,self.dtgopt,curdtg)

        self.qname=pytag


        # -- new qsub system on both jet and zeus
        #

        qsubshHead='''
#!/bin/sh --login
#PBS -d .
#PBS -N %s
#PBS -A %s 
#PBS -l procs=%d
#PBS -l partition=%s
#PBS -q %s
#PBS -l walltime=%s
#PBS -j oe
#PBS -o %s
'''%(self.qname,
     self.project,
     self.procs,
     self.partition,
     self.queue,
     rttime,logpath)


        qsubshuNix='''
# Set up paths to unix commands
RM=/bin/rm
CP=/bin/cp
MV=/bin/mv
LN=/bin/ln
MKDIR=/bin/mkdir
CAT=/bin/cat
ECHO=/bin/echo
CUT=/bin/cut
WC=/usr/bin/wc
DATE=/bin/date
AWK="/bin/awk --posix"
SED=/bin/sed
TAIL=/usr/bin/tail
'''

        qsubshMain='''
# Executable script and path
RUNCMD='%s'
PYDIR="%s"
PYCMD="%s"

# Set CWD to script location and execute redirecting stdout/stderr
cd $PYDIR
$RUNCMD "$PYDIR/$PYCMD %s" >> %s 2>&1

# Check for exit status of script
error=$?
if [ ${error} -ne 0 ]; then
  ${ECHO} "ERROR: ${PYCMD} crashed  Exit status=${error}"
  exit ${error}
fi

# Sucessful exit
exit 0'''%(self.runcmd,
           self.pydir,
           self.pycmd,
           pyopt,outpath)


        qsubsh=qsubshHead+qsubshuNix+qsubshMain
        qpath="%s/p.qsub.%s.ksh"%(self.pydir,pytag)
        rc=MF.WriteString2File(qsubsh,qpath)

        print 'QQQ  qpath: ',qpath

        if(self.doqsub and self.ropt != 'norun'):

            cmd="qsub %s"%(qpath)
            MF.runcmd(cmd,self.ropt)

            if(self.doKshUnlink):
                try:     os.unlink(qpath)
                except:  None

        else:

            print
            print qsubsh
            print




def getFRlocal(model,dtg,verb=0):

    dskey="%s.%s"%(model,dtg)

    dbname=SetDBname(model)

    if(mf.find(w2.remoteHost,'zeus')):  dbwjet="%s_zeus_%s.pypdb"%(dbname,dtg)
    else:                               dbwjet="%s_wjet_%s.pypdb"%(dbname,dtg)

    dblocal="%s_local_%s.pypdb"%(dbname,dtg)

    dsbdirlocal="%s/DSs"%(lrootLocal)

    DSswjet=DataSets(bdir=dsbdirlocal,name=dbwjet,dtype='model',verb=verb)
    DSslocal=DataSets(bdir=dsbdirlocal,name=dblocal,dtype='model',verb=verb)

    dslocal=DSslocal.getDataSet(dskey)
    dswjet=DSswjet.getDataSet(dskey)


    (FE,FR)=getDswjet(dswjet,dtg,model)
    FRlocal=getDslocal(FE,FR,dslocal,dtg,model)

    return(FRlocal)



def getDswjet(dswjet,dtg,model,fmodel=None,expopt=None,DSoverride=0,warn=0):

    FE=FR=None

    if(dswjet == None):
        if(DSoverride):
            print 'DSoverride on local -- database problem with DSswjet for model: ',model,' fmodel: ',fmodel,' expopt: ',expopt,' made on wjet...'
            FE=setFE(dtg,model,fmodel=fmodel,expopt=expopt)
            FR=FimRun(FE,gribver=2,override=DSoverride)
        else:
            if(warn): print 'WWW no data for model: ',model,' fmodel: ',fmodel,' expopt: ',expopt,' made on wjet...'
            return(FE,FR)
    else:
        FR=dswjet.FR
        FE=FR.FE

    if(not(hasattr(FE,'fmodel'))): FE.fmodel=FE.sroot.split('/')[-1]

    return(FE,FR)


def getDslocal(FE,FR,dslocal,dtg,model,override=0):

    FRlocal=None

    if((dslocal == None or override > 0) and FE != None):
        if(not(hasattr(FE,'fmodel'))): FE.fmodel=FE.sroot.split('/')[-1]
        print 'FM.getDslocal: making new FRlocal ',FE.fmodel,FE.expopt,lrootLocal
        FElocal=setFE(dtg,model,fmodel=FE.fmodel,expopt=FE.expopt,sroot=trootWjet,troot=lrootLocal,npes=FE.npes,glvl=FE.glvl)
        FRlocal=FimRun(FElocal,gribver=2)
        if(FR != None):
            if(hasattr(FR,'comment')):  FRlocal.comment=FR.comment

    elif(dslocal != None):
        FRlocal=dslocal.FR

    # --- use fim8 model2 settings for rtfim runs...
    #
    from M2 import setModel2
    FRlocal.m2=setModel2('rtfim')



    return(FRlocal)



def Rsync2Local(sdir,tdir,rs=rsyncServerJet,ro=rsyncOpt,override=0,ropt=''):
    """
    rsync model data to local
    """
    mf.ChkDir(tdir,'mk')

    if(not(w2.onWjet or w2.onZeus)):
        cmd="rsync %s %s:%s/ %s/"%(ro,rs,sdir,tdir)
        mf.runcmd(cmd,ropt)

def SetDBname(model):

    dbname='rtfim'
    for m in taccmodels:
        if(model == m): dbname='tacc2009'

    for m in m2models:
        if(model == m): dbname='w2flds'

    return(dbname)

def setAtcfname(model):

    if(model == 'rtfim'):        atcfname='f8c'
    elif(model == 'rtfimx'):     atcfname='f8cx'
    elif(model == 'rtfimy'):     atcfname='f8cy'
    elif(model == 'rtfim7'):     atcfname='f7c'
    elif(model == 'rtfimz'):     atcfname='f8cz'
    elif(model == 'rtfimchem'):  atcfname='fchm'
    else:                        atcfname=model.upper()
    return(atcfname)


def setFmodel(model):

    if(model == 'rtfim'):
        fmodel='FIM'
    elif(model == 'rtfimx'):
        fmodel='FIMX'
    elif(model == 'rtfimy'):
        fmodel='FIMY'
    elif(model == 'rtfimz'):
        fmodel='FIMZ'
    elif(model == 'rtfim7'):
        fmodel='FIM7'
    elif(model == 'rtfimz9'):
        fmodel='FIMZ9'
    else:
        print 'EEE invalid model: ',model,' in setFmodel'
        sys.exit()

    return(fmodel)



def rsync2Kishou(tdir,tdirKishou,ropt):

    prcdir=w2.PrcDirFlddatW2
    expath="%s/ex-kaze2kishou.txt"%(prcdir)

    rsyncoptDry='-alvn  --protocol=29 --exclude-from=%s '%(expath)
    rsyncoptDo='-alv  --protocol=29 --exclude-from=%s '%(expath)
    rsyncopt=rsyncoptDo
    if(ropt == 'norun'):
        rsyncopt=rsyncoptDry
        ropt=''

    cmd='rsync %s %s %s'%(rsyncopt,tdir,tdirKishou)
    mf.runcmd(cmd,ropt)


def setFE(dtg,
          model,
          fmodel=None,
          expopt=None,
          sroot=None,
          troot=trootWjet,
          lroot=lrootLocal,
          npes=None,
          glvl=None,
          nlvl=None,
          taumax=taumax,
          comment=None):

    mr=rtfimRuns()
    mr.getRun(model)
    
    if(hasattr(mr,'srootWjet')): sroot=mr.srootWjet
    if(hasattr(mr,'troot')): troot=mr.troot
    if(hasattr(mr,'lrootLocal')): lroot=mr.lrootLocal
    if(hasattr(mr,'nlvl')): nlvl=mr.nlvl


    if(fmodel == None and not(hasattr(mr,'fimrun'))):
        (fmodel)=setFmodel(model)
    else:
        fmodel=mr.fimrun

    if(expopt == None and not(hasattr(mr,'fimrun'))):
        expopt=fmodel
    else:
        expopt=mr.fimrun

    if(sroot == None): sroot="%s/%s"%(srootWjet,fmodel)

    if(npes == None and not(hasattr(mr,'npe'))):
        npes='240'
    else:
        npes=mr.npe


    if(glvl == None and not(hasattr(mr,'g'))):
        glvl='8'
    else:
        glvl=mr.g

    if(nlvl == None):
        nlvl='64'

    if(hasattr(mr,'taumax')): taumax=mr.taumax
    fimsuffix=None
    if(w2.onWjet): fimsuffix='_jet_p'

    fe=FimExp(
        sroot=sroot,
        troot=troot,
        lroot=lroot,
        fmodel=fmodel,
        model=model,
        expopt=expopt,
        fimver=None,
        fimtype='C',
        dtg=dtg,
        npes=npes,
        glvl=glvl,
        nlvl=nlvl,
        lasttau=taumax,
        fimsuffix=fimsuffix,
        comment=comment,
    )


    # dangle useDtgDirName to fe
    #
    
    if(hasattr(mr,'useDtgDirName')): fe.useDtgDirName=mr.useDtgDirName
        
    return(fe)

#CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
# base class with methods
#

class FIM(Model,MFutils):


    def getStdOut(self,override=0,verb=0):

        if(os.path.exists(self.std_pyppath) and not(override)):
            if(verb): print 'uuuuuuupppppppppppppp ',self.std_pyppath
            self.stdout=self.GetPyp(pyppath=self.std_pyppath)
            return


    def ParseStdOut(self,override=0,verb=0):

        # precip - total/nonconv/conv=  0.0000000E+00  0.0000000E+00  0.0000000E+00
        # Global 3D mass          =  5.1274939E+18  at time step=           1
        # Global 3D water vapor   =  1.3496351E+16  at time step=           1
        # Global 3D cloud water   =  3.5297962E+13  at time step=           1
        # Global integ acc precip =  6.9420607E+12  at time step=           1
        # Global integ evaporation=  6.7022252E+12  at time step=           1


        if(os.path.exists(self.std_pyppath) and not(override)):
            if(verb): print 'uuuuuuupppppppppppppp ',self.std_pyppath
            self.stdout=self.GetPyp(pyppath=self.std_pyppath)
            return


        rundate=None
        rundtg=None

        modtimers=[]

        gwnoise={}
        gpr={}
        gprc={}
        gprl={}
        gmass={}
        gh2o={}
        gclh2o={}
        gpraccum={}
        gevap={}

        cards=[]
        path=self.tStdOutPath
        if(os.path.exists(path)):
            cards=open(path).readlines()

        if(len(cards) == 0):
            self.stdout=None
            del self.tStdOutPath
            return

        ntimer=0
        for n in range(0,len(cards)):

            card=cards[n][:-1]

            if(mf.find(card,'DATE-TIME: ')):
                rundate=card[12:-1].strip()
                if(verb): print 'TTTTT rundate',rundate,'ddd'

                #Default time step:                         101 seconds
                #Time step reduced to                        90 seconds


            if(mf.find(card,'Length of time step:')):

                tt=card.split(':')
                ltt=len(tt)
                tt=tt[ltt-1].split()
                timestep=float(tt[0])
                timestepunits=tt[1]
                if(verb): print 'TTTTTTTTT ',timestep,timestepunits

            if(mf.find(card,'Time step reduced to')):

                tt=card.split()
                timestep=float(tt[-2])
                timestepunits=tt[-1]
                if(verb): print 'TTTTTTTTT ',timestep,timestepunits

            if(mf.find(card,'Number of time steps')):

                #Number of time steps:                    6000 timesteps
                tt=card.split()
                Ntimesteps=tt[-2]
                if(verb): print 'TTTTTTTTT Ntimesteps: ',Ntimesteps

            if(mf.find(card,'Forecast initial time')):

                tt=card.split()
                rundtg=tt[3][0:10]
                if(verb): print 'TTTTTTTTT ',rundtg

            if(mf.find(card,'Output every  ')):
                tt=card.split()
                dtau=tt[2]
                dtauunits=tt[3]
                if(verb): print 'TTTTTTTTT ',dtau,dtauunits

            #
            # time series
            #
            bd=28
            if(mf.find(card,' rms-d(psfc)**2/d**2t) = ')):

                # rms-d(psfc)**2/d**2t) =          10   23.05441    
                tt=card.split()
                its=int(tt[2])
                val=float(tt[3])
                #print 'mmmmmmmmmmmmmmmmmmmmmmmmmmm noise',tt,its,val
                if(verb): print 'noise ',its,val
                gwnoise[its]=val

            if(mf.find(card,'precip - total/nonconv/conv=')):

                #precip - total/nonconv/conv=  0.0000000E+00  0.0000000E+00  0.0000000E+00
                # -- go back for its

                tt2=cards[n-1]
                if(not(mf.find(cards[n-1],'MAXMIN'))):  tt2=cards[n-2]

                tt2=tt2.split()
                its=int(tt2[1])

                tt=card.split()

                pr=float(tt[3])
                prl=float(tt[4])
                prc=float(tt[5])
                #print 'mmmmmmmmmmmmmmmmmmmmmmmmmmm gmass',tt,its,pr,prl,prc
                if(verb): print 'pr     ',its,pr,prl,prc
                gpr[its]=pr
                gprl[its]=prl
                gprc[its]=prc

            if(mf.find(card,'Global 3D mass          =')):

                #Global 3D mass          = 5.1249919E+18 at   0.1 hr, time step=       1
                tt=card[bd:].split()
                tt=card.split()
                its=int(tt[-1])
                val=float(tt[4])
                #print 'mmmmmmmmmmmmmmmmmmmmmmmmmmm gmass',tt,its,val
                if(verb): print 'gmass  ',its,val
                gmass[its]=val

            if(mf.find(card,'Global 3D water vapor   =')):

                #Global 3D water vapor   = 1.3939858E+16 at   0.1 hr, time step=       1
                tt=card.split()
                its=int(tt[-1])
                val=float(tt[5])
                #print 'mmmmmmmmmmmmmmmmmmmmmmmmmmm   h2o',tt,its,val
                if(verb): print 'gh2o     ',its,val
                gh2o[its]=val

            if(mf.find(card,'Global 3D cloud water   =')):

                #Global 3D cloud water   = 3.6389756E+13 at   0.1 hr, time step=       1
                tt=card.split()
                its=int(tt[-1])
                val=float(tt[5])
                #print 'mmmmmmmmmmmmmmmmmmmmmmmmmmm clh2o ',tt,its,val
                if(verb): print 'gclh2o    ',its,val
                gclh2o[its]=val

            if(mf.find(card,'Global integ acc precip =')):

                #Global integ acc precip = 1.9118372E+13 at   0.1 hr, time step=       1
                tt=card.split()
                val=float(tt[5])
                #print 'mmmmmmmmmmmmmmmmmmmmmmmmmmm praccum ',tt,its,val
                if(verb): print 'gpraccum ',its,val
                gpraccum[its]=val

            if(mf.find(card,'Global integ evaporation=')):

                # Global integ evaporation=  6.1587870E+12  at time step=           1
                tt=card.split()
                val=float(tt[3])
                #print 'mmmmmmmmmmmmmmmmmmmmmmmmmmm evap ',tt,its,val
                if(verb): print 'gevap   ',its,val
                gevap[its]=val

            if(mf.find(card,'MODULE TIME (sec)')):

                ntimer=ntimer+1

                if(ntimer == 2):
                    nstart=n+2
                    nend=nstart+11
                    for nn in range(nstart,nend+1):
                        card=cards[nn][:-1]
                        tt=card.split()

                        try:
                            prcname=tt[0]
                        except:
                            continue
                        bd=1
                        if(prcname == 'Main'):  bd=2

                        try:
                            prcmin=float(tt[bd])
                            prcmax=float(tt[bd+1])

                            modtimers.append((prcname,prcmin,prcmax))
                            if(verb): print 'modtimers: ',prcname,prcmin,prcmax
                        except:
                            continue


        rec=(
            rundate,
            rundtg,
            timestep,
            timestepunits,
            Ntimesteps,
            dtau,
            dtauunits,
            gwnoise,
            gpr,
            gprl,
            gprc,
            gmass,
            gh2o,
            gclh2o,
            gpraccum,
            gevap,
            modtimers,
        )


        stdout=FimStdOut(rec)

        stdpyp=(stdout)
        self.PutPyp(pyp=stdpyp,pyppath=self.std_pyppath)

        self.stdout=stdout

    def lsStdOut(self,override=0,verb=0):

        if(self.docpalways == -1):
            return


        self.ParseStdOut(override=override,verb=verb)

        print
        print 'rundate:       ',self.stdout.rundate
        print 'rundtg:        ',self.stdout.rundtg
        print 'timestep:      ',self.stdout.timestep
        print 'Ntimesteps:    ',self.stdout.Ntimesteps
        print 'timestepunits: ',self.stdout.timestepunits
        print 'dtau:          ',self.stdout.dtau
        print 'dtauunits:     ',self.stdout.dtauunits
        print

        if(hasattr(self.stdout,'modtimers')):

            print 'Module timer:'
            for modtimer in self.stdout.modtimers:
                print '%-12s: min: %6.2f  max: %6.2f'%(modtimer[0],modtimer[1],modtimer[2])
            print


        kk=self.stdout.TS.keys()
        print 'TimeSeries vars:'
        for k  in kk:
            print k

        print


    def GetPyp(self,pyppath=None):

        if(pyppath != None):
            ppath=pyppath
        else:
            ppath=self.pyppath

        if(os.path.exists(ppath)):
            PS=open(ppath)
            FR=pickle.load(PS)
            PS.close()
            return(FR)

        else:
            return(None)


    def PutPyp(self,pyp=None,pyppath=None):

        if(pyppath != None):
            ppath=pyppath
        else:
            ppath=self.pyppath

        if(pyp != None):
            pyppckle=pyp
        else:
            pyppckle=self

        try:
            PS=open(ppath,'w')
            pickle.dump(pyppckle,PS)
            PS.close()
        except:
            print 'EEEEE unable to pickle.dump: ',self.pyppath
            sys.exit()



class FimExp(MFbase):

    def __init__(self,
                 sroot=None,
                 troot=trootWjet,
                 lroot=lrootLocal,
                 fmodel='myfmodel',
                 model='mymodel',
                 expopt='myfimrun',
                 fimver=None,
                 fimtype='C',
                 dtg=None,
                 glvl='8',
                 nlvl='64',
                 npes='240',
                 btau=0,
                 etau=taumax,
                 dtau=6,
                 lasttau=taumax,
                 fimsuffix=None,
                 comment=None,
                 ):

        if(sroot == None): sroot="%s/%s"%(srootWjet,'FIM')
        self.sroot=sroot
        self.troot=troot
        self.lroot=lroot

        self.model=model
        self.expopt=expopt


        self.fimver=fimver
        self.fmodel=fmodel

        self.glvl=glvl
        self.nlvl=nlvl
        self.npes=npes

        self.fimtype=fimtype

        self.dtg=dtg
        self.btau=btau
        self.etau=etau
        self.dtau=dtau
        self.lasttau=lasttau

        didparams=0
        if(dtg == None):
            didparams=self.setExpParams()

        self.fimsuffix=fimsuffix
        self.comment=comment
        self.initComment()

        if(didparams): return



    def getTauFimOut(self,fimout,tunit):

        tt=fimout.split('_')
        t1=tt[-1]

        var=t1[0:4]
        tau=None
        if(tunit == 'hr'):
            tau=int(t1[-8:-2])

        return(var,tau)




    def setExpParams(self):

        curdir=os.getcwd()

        if(MF.ChangeDir(self.sroot) == 0):
            print 'EEE unable to cd to: ',self.sroot
            return(0)


        tt=self.sroot.split('/')

        sroot=tt[0]
        for n in range(1,len(tt)-1):
            sroot="%s/%s"%(sroot,tt[n])

        if(mf.find(self.sroot,'qsub')):
            tt=self.sroot.split('/')[-1]
            tt=tt.split('_')
            self.npes=tt[-1]
            self.nlvl=tt[-2]
            self.glvl=tt[-3][-1]
            self.fimver='qsub'
            self.fimtype=''


        dirs=os.listdir('.')
        if('fim' in dirs):
            MF.ChangeDir('fim')
            from fm2 import FIM
            fS=FIM("%s/fim/stdout"%(self.sroot))

            self.dtg=fS.rundtg
            fS.lsStdOut()

            cmd="ls -l fim_out*"
            fimouts=MF.runcmdLog(cmd)

            vars=[]
            taus=[]

            for fimout in fimouts:
                if(len(fimout) > 1):
                    tunit=fimout[-2:]
                    (var,tau)=self.getTauFimOut(fimout,tunit)
                    taus.append(tau)
                    vars.append(var)


            taus=MF.uniq(taus)
            vars=MF.uniq(vars)

        # -- reset sroot
        #
        self.sroot=sroot
        self.btau=taus[0]
        self.etau=taus[-1]

        if(len(taus) > 1):
            dtau=taus[1]-taus[0]
        else:
            dtau=0

        self.dtau=dtau

        self.lasttau=taus[-1]

        self.taus=taus
        self.vars=vars

        MF.ChangeDir(curdir)

        return(1)





    def initComment(self):

        if(self.comment != None): return

        if(self.model == 'rtfim'):

            dtg1='2010021200'
            diff1=mf.dtgdiff(dtg1,self.dtg)

            if(diff1 >= 0.0):
                comment='GSI + r916 - intfc_smooth=50, slak=0.50, dpsig=15, bao plev xkt2'
            else:
                comment='r901 trunk sig-theta'

        elif(self.model == 'rtfimx'):

            dtg1='2010021200'
            diff1=mf.dtgdiff(dtg1,self.dtg)

            if(diff1 >= 0):
                comment='GSI + r916 - intfc_smooth=50, slak=0.50, dpsig=10, bao plev xkt2'
            else:
                comment='r872 sig-p hybgen.F90.sig'

        elif(self.model == 'rtfimy'):
            dtg1='2010021112'
            diff1=mf.dtgdiff(dtg1,self.dtg)

            if(diff1 >= 0):
                comment='ENKF + FIM(r916 - intfc_smooth=50, slak=0.50, dpsig=15, bao plev xkt2)'
            else:
                comment='ENKF + r901 trunk sig-theta'

        elif(self.model == 'rtfimR925'):
            dtg1='2010021112'
            diff1=mf.dtgdiff(dtg1,self.dtg)

            if(diff1 >= 0):
                comment='FIM(r925 - intfc_smooth=50, slak=0.50, dpsig=15) retro for 200908-09 every 00z)'
            else:
                comment='None'
        else:
            comment='mycomment'

        self.comment=comment



class FimAllCtl(FIM):


    ctltype='prs'
    gribtype='grb1'
    gmaptype="%s.gmp"%(gribtype)


    levs="""zdef 43 levels
1000 975 950 925 900 875 850 825 800 775 750 725 700
     675 650 625 600 575 550 525 500 475 450 425 400
     375 350 325 300 275 250 225 200 175 150 125 100
      75  50  25 20 10 5"""

    vars="""vars 19
hfls  0 121,1,1   ** Latent heat flux [W/m^2]
hfss  0 122,1,1   ** Sensible heat flux [W/m^2]
pr    0  61,1,1   ** Total precipitation [kg/m^2]
prc   0  63,1,1   ** Convective precipitation [kg/m^2]
prl   0  62,1,1   ** Large scale precipitation [kg/m^2]
prw   0  54,1,1   ** Precipitable water [kg/m^2]
psl   0 129,102,1 ** Mean sea level pressure (MAPS) [Pa]
rls   0 112,1,1   ** Net long wave (surface) [W/m^2]
rss   0 111,1,1   ** Net short wave (surface) [W/m^2]
sno   0  65,1,1   ** Accum. snow [kg/m^2]
ts    0  11,1,1   ** Temp. [K]
ustar 0 253,1,1   ** Friction velocity [m/s]
zgclb 0  7,2,1    ** Geopotential height [gpm]
zgclt 0  7,3,1    ** Geopotential height [gpm]
ta   43  11,100,0 ** Temp. [K]
ua   43  33,100,0 ** u wind [m/s]
hur  43  52,100,0 ** Relative humidity [%%]
va   43 34,100,0  ** v wind [m/s]
zg   43  7,100,0  ** Geopotential height [gpm]
endvars"""


    undef='9.999E+20'
    title='/lfs2/projects/fim/fiorino/FIM/FIMrun/fim_9_64_240_200910131200/post_C/fim/NAT/grib1/0928612000024'


    def __init__(self,dtg=None,tdir=None,lasttau=taumax,taus=[0,6],dtau=6,glvl=8,
                 dset=None,
                 mset=None,
                 gridRes=None,
                 ):


        self.dtg=dtg
        self.tdir=tdir
        self.lasttau=lasttau
        self.taus=taus
        self.dtau=dtau
        self.glvl=glvl
        self.dset=dset
        self.mset=mset
        self.gridRes=gridRes

        self.setGrid()
        self.setCtl()



    def setCtl(self):

        gtime=mf.dtg2gtime(self.dtg)

        nt=len(self.taus)

        if(len(self.taus) > 1):
            dtau=int(self.taus[1])-int(self.taus[0])
            dtau="%dhr"%(dtau)
        else:
            dtau='1mo'

        if(self.dset == None):
            self.dset="^fim.%s.f%%f3.%s"%(self.dtg,self.gribtype)

        if(self.mset == None):
            self.mset="^fim.%s.%s.%s"%(self.dtg,self.ctltype,self.gmaptype)

        self.cfile="fim.%s.%s.ctl"%(self.ctltype,self.dtg)
        self.tdef="tdef %d  linear %s %s"%(nt,gtime,dtau)

        if(self.tdir != None):
            self.ctlpath="%s/%s"%(self.tdir,self.cfile)
            self.gmppath="%s/%s"%(self.tdir,self.mset)
            self.pyppath="%s/FimAllCtl.%s.pyp"%(self.tdir,self.ctltype)

        self.ctl="""dset %s
index %s
undef %s
title %s
options yrev template
dtype grib 255
%s
%s
%s
%s"""%(self.dset,self.mset,
       self.undef,self.title,
       self.grid,self.levs,self.tdef,
       self.vars)

        self.nt=nt
        self.dtau=dtau


    def setGrid(self):

        if(int(self.glvl) <= 5 or (self.gridRes != None and self.gridRes == 2.5) ):
            self.grid="""xdef 144 linear 0 2.5
ydef  73 linear -90.0 2.5"""
        else:
            self.grid="""xdef 720 linear 0 0.5
ydef 361 linear -90.0 0.5"""




    def WriteCtl(self,verb=0):

        try:
            c=open(self.ctlpath,'w')
        except:
            print "EEE unable to open: %s"%(self.ctlpath)
            sys.exit()

        if(verb): print "CCCC creating .ctl: %s"%(self.ctlpath)
        c.writelines(self.ctl)
        c.close()
        return


class PrsCtl(FimAllCtl):


    def __init__(self,dtg=None,tdir=None,lasttau=taumax,taus=[0,6],dtau=6,glvl=8,
                 dset=None,
                 mset=None,
                 gridRes=None,
                 ):


        self.dtg=dtg
        self.tdir=tdir
        self.lasttau=lasttau
        self.taus=taus
        self.dtau=dtau
        self.glvl=glvl
        self.ctltpye='prs'
        self.dset=dset
        self.mset=mset
        self.gridRes=gridRes

        self.vars="""vars 21
uas   0  33,105,10  ** u sfc wind [m/s]
vas   0  34,105,10  ** v sfc wind [m/s]
hfls  0 121,1,1   ** Latent heat flux [W/m^2]
hfss  0 122,1,1   ** Sensible heat flux [W/m^2]
pr    0  61,1,1   ** Total precipitation [kg/m^2]
prc   0  63,1,1   ** Convective precipitation [kg/m^2]
prl   0  62,1,1   ** Large scale precipitation [kg/m^2]
prw   0  54,1,1   ** Precipitable water [kg/m^2]
psl   0 129,102,1 ** Mean sea level pressure (MAPS) [Pa]
rls   0 112,1,1   ** Net long wave (surface) [W/m^2]
rss   0 111,1,1   ** Net short wave (surface) [W/m^2]
sno   0  65,1,1   ** Accum. snow [kg/m^2]
ts    0  11,1,1   ** Temp. [K]
ustar 0 253,1,1   ** Friction velocity [m/s]
zgclb 0  7,2,1    ** Geopotential height [gpm]
zgclt 0  7,3,1    ** Geopotential height [gpm]
ta   43  11,100,0 ** Temp. [K]
ua   43  33,100,0 ** u wind [m/s]
hur  43  52,100,0 ** Relative humidity [%%]
va   43  34,100,0  ** v wind [m/s]
zg   43  7,100,0  ** Geopotential height [gpm]
endvars"""

        self.setGrid()
        self.setCtl()



class PrsFimXCtl(FimAllCtl):


    def __init__(self,dtg=None,tdir=None,lasttau=taumax,taus=[0,6],dtau=6,glvl=7,
                 dset=None,
                 mset=None,
                 gridRes=None,
                 ):


        self.dtg=dtg
        self.tdir=tdir
        self.lasttau=lasttau
        self.taus=taus
        self.dtau=dtau
        self.glvl=glvl
        self.ctltpye='prs'

        self.dset=dset
        self.mset=mset
        self.gridRes=gridRes

        self.vars="""vars 45
uas       0  33,105,10  ** u sfc wind [m/s]
vas       0  34,105,10  ** v sfc wind [m/s]
ia2d      0 130,1,1  ** Integrated PM25 [ug/m3]                                     
ib2d      0 132,1,1  ** Integrated black carbon [ug/kg]                             
id2d      0 134,1,1  ** Integrated fine dust [ug/kg]                                
io2d      0 131,1,1  ** Integrated organic carbon [ug/kg]                           
is2d      0 133,1,1  ** Integrated sulf [ppm]                                       
pr        0 61,1,1  ** Total precipitation [kg/m^2]
prc       0 63,1,1  ** Convective precipitation [kg/m^2]
prl       0 62,1,1  ** Large scale precipitation [kg/m^2]
prw       0 54,1,1  ** Precipitable water [kg/m^2]
psl       0 129,102,1  ** Mean sea level pressure (MAPS) [Pa]
rls       0 112,1,1  ** Net long wave (surface) [W/m^2]
rss       0 111,1,1  ** Net short wave (surface) [W/m^2]
sno       0 65,1,1  ** Accum. snow [kg/m^2]
tas       0 11,1,1  ** Temp. [K]
us2d      0 253,1,1  ** Friction velocity [m/s]                                     
zgclb     0  7,2,1    ** Geopotential height [gpm]
zgclt     0  7,3,1    ** Geopotential height [gpm]
ao2d      0 135,1,1  ** Aerosol Optical Depth [ug/kg]                               
hfls      0 121,1,1  ** Latent heat flux [W/m^2]
hfss      0 122,1,1  ** Sensible heat flux [W/m^2]
hur      40 52,100,0 ** Relative humidity [%%]
bc1p     40 235,100,0 ** hydrophobic black carbon - p [ug/kg]                        
bc2p     40 236,100,0 ** hydrophobic black carbon - p [ug/kg]                        
d1sp     40 239,100,0 ** dust1 - p [ppm]                                             
d2sp     40 240,100,0 ** dust2 - p [ppm]                                             
d3sp     40 241,100,0 ** dust3 - p [ppm]                                             
d4sp     40 242,100,0 ** dust4 - p [ppm]                                             
d5sp     40 244,100,0 ** dust5 - p [ppm]                                             
dmsp     40 252,100,0 ** dms - p [ppm]                                               
msap     40 254,100,0 ** msa - p [ppm]                                               
oc1p     40 233,100,0 ** hydrophillic organic carbon - p [ug/kg]                     
oc2p     40 234,100,0 ** hydrophillic organic carbon - p [ug/kg]                     
p25p     40 155,100,0 ** prmary pm25 - p [ug/kg]                                     
s1sp     40 248,100,0 ** seasalt1 - p [ppm]                                          
s2sp     40 249,100,0 ** seasalt2 - p [ppm]                                          
s3sp     40 250,100,0 ** seasalt3 - p [ppm]                                          
s4sp     40 251,100,0 ** seasalt4 - p [ppm]                                          
slfp     40 238,100,0 ** sulfate - p [ppm]                                           
so2p     40 237,100,0 ** so2 - p [ppm]                                               
ta       40 11,100,0 ** Temp. [K]
ua       40 33,100,0 ** u wind [m/s]
va       40 34,100,0 ** v wind [m/s]
zg       40   7,100,0 ** Geopotential height [gpm]
endvars"""


        self.setGrid()
        self.setCtl()



class HblCtl(FimAllCtl):

    def __init__(self,dtg=None,tdir=None,lasttau=taumax,taus=[0,6],dtau=6,glvl=8,nlvl=64,
                 dset=None,
                 mset=None,
                 gridRes=None,
                 ):


        self.dtg=dtg
        self.tdir=tdir
        self.lasttau=lasttau
        self.taus=taus
        self.dtau=dtau
        self.glvl=glvl
        self.dset=dset
        self.mset=mset
        self.gridRes=gridRes

        self.ctltype='hbl'

        self.levs="""zdef 65 levels
65 64 63 62 61 60 59 58 57 56 55 54 53 52 51 50 49 48 47 46 45 44 43 42 41 40 39 38 37 36 35 34 33 32 31 30 29 28 27 26 25 24 23 22 21
20 19 18 17 16 15 14 13 12 11 10 9 8 7 6 5 4 3 2 1"""


        nlvl=int(nlvl)

        self.levs="""zdef %d linear 1 1"""%(nlvl+1)

        self.vars="""vars 25
uas   0  33,105,10  ** u sfc wind [m/s]
vas   0  34,105,10  ** v sfc wind [m/s]
hfls  0 121,1,1   ** Latent heat flux [W/m^2]
hfss  0 122,1,1   ** Sensible heat flux [W/m^2]
pr    0  61,1,1   ** Total precipitation [kg/m^2]
prc   0  63,1,1   ** Convective precipitation [kg/m^2]
prl   0  62,1,1   ** Large scale precipitation [kg/m^2]
prw   0  54,1,1   ** Precipitable water [kg/m^2]
psl   0 129,102,1 ** Mean sea level pressure (MAPS) [Pa]
rls   0 112,1,1   ** Net long wave (surface) [W/m^2]
rss   0 111,1,1   ** Net short wave (surface) [W/m^2]
sno   0  65,1,1   ** Accum. snow [kg/m^2]
ts    0  11,1,1   ** Temp. [K]
ustar 0 253,1,1   ** Friction velocity [m/s]
zgclb 0   7,2,1   ** Geopotential height [gpm]
zgclt 0   7,3,1   ** Geopotential height [gpm]
ta   %d  11,109,0 ** Temp. [K]
td   %d  17,109,0 ** Dew point temp. [K]
ua   %d  33,109,0 ** u wind [m/s]
hur  %d  52,109,0 ** Relative humidity [%%]
va   %d  34,109,0 ** v wind [m/s]
wap  %d  39,109,0 ** Pressure vertical velocity [Pa/s]
o3   %d 154,109,0 ** Ozone mixing ratio [kg/kg]
zg   %d   7,109,0 ** Geopotential height [gpm]
pa   %d   1,109,0 ** Pressure [Pa]
endvars"""%(nlvl,nlvl,nlvl,nlvl,nlvl,nlvl,nlvl,
            nlvl+1,nlvl+1)

        self.setGrid()
        self.setCtl()



class FimVerif(MFbase):


    def __init__(self,tdir='/tmp',sdir=None):

        self.tdir=tdir
        self.pyppath="%s/FimVerif.pyp"%(tdir)

        curPyp=self.getPyp(verb=1)

        if(curPyp == None):
            self.stats={}

        else:
            self.stats=curPyp.stats

        self.area2key={
            10:'nhem',
            9:'shem',
            7:'global',
            11:'npole',
            12:'spole',
            7:'nhem',
        }



    def setArea(self,lat1,lat2):

        area=None
        if(lat1 >= 20.0  and lat2 <=  80.0): area='nhem'
        if(lat1 >= -80.0 and lat2 <= -20.0): area='shem'
        if(lat1 >= -90.0 and lat2 <= -90.0): area='global'
        if(lat1 >= 70.0  and lat2 <=  90.0): area='npole'
        if(lat1 >= -90.0 and lat2 <= -70.0): area='spole'
        if(lat1 >= -20.0 and lat2 <=  20.0): area='tropics'

        return(area)

    def areaKey(self,key):

        #PPPP(str):  554 str: 20090802:00:FIMretro2009NewPhys1094b:GFS:850:VGRD:24:10:9513 20.0 80.0 144 25 -2.5
        #PPPP(str):  558 str: 20090802:00:FIMretro2009NewPhys1094b:GFS:850:VGRD:24:9:9667 -80.0 -20.0 144 25 -2.5
        #PPPP(str):  562 str: 20090802:00:FIMretro2009NewPhys1094b:GFS:850:VGRD:24:8:9050 -20.0 20.0 144 17 -2.5
        #PPPP(str):  566 str: 20090802:00:FIMretro2009NewPhys1094b:GFS:850:VGRD:24:7:9554 -90.0 90.0 720 361 -0.5
        #PPPP(str):  570 str: 20090802:00:FIMretro2009NewPhys1094b:GFS:850:VGRD:24:11:9473 70.0 90.0 144 9 -2.5
        #PPPP(str):  574 str: 20090802:00:FIMretro2009NewPhys1094b:GFS:850:VGRD:24:12:9357 -70.0 -90.0 144 9 -2.5

        area=None
        if(key == 10): area='nhem'
        if(key ==  9): area='shem'
        if(key ==  7): area='global'
        if(key == 11): area='npole'
        if(key == 12): area='spole'
        if(key ==  8): area='tropics'

        return(area)


    def getGridParams(self,area):


        gridparams=None
        if(area == 'nhem'):     gridparams='''-g"255,0,144,25,+20000,0,0,+80000,-2500,0,0,64,0,0,0,0,0,0,0,0,255"'''
        if(area == 'shem'):     gridparams='''-g"255,0,144,25,-80000,0,0,-20000,-2500,0,0,64,0,0,0,0,0,0,0,0,255"'''
        if(area == 'global'):   gridparams='''-g"255,0,720,361,-90000,0,0,+90000,-500,0,0,64,0,0,0,0,0,0,0,0,255"'''
        if(area == 'npole'):    gridparams='''-g"255,0,144,9,+70000,0,0,+90000,-2500,0,0,64,0,0,0,0,0,0,0,0,255"'''
        if(area == 'spole'):    gridparams='''-g"255,0,144,9,-70000,0,0,-90000,-2500,0,0,64,0,0,0,0,0,0,0,0,255"'''
        if(area == 'tropics'):  gridparams='''-g"255,0,144,17,-20000,0,0,+20000,-2500,0,0,64,0,0,0,0,0,0,0,0,255"'''

        return(gridparams)



    def getLatLon(self,card):
        tt=card.split()
        for ttt in tt:
            if(mf.find(ttt,'-g')):
                ll=ttt.split(',')
                nx=int(ll[2])
                ny=int(ll[3])
                lat1=float(ll[4])*0.001
                lat2=float(ll[7])*0.001
                dlat=float(ll[8])*0.001

        return(lat1,lat2,nx,ny,dlat)

    def getVname(self,vvar):

        ovar=None
        if(vvar == 'hgt'):  ovar='zg'
        if(vvar == 'ugrd'): ovar='ua'
        if(vvar == 'vgrd'): ovar='va'
        return(ovar)


    def getVarPdsLevel(self,vvar,level):

        opds=None
        if(vvar == 'hgt'):  opds="""-k '4*-1  7 100  %d '"""%(level)
        if(vvar == 'ugrd'): opds="""-k '4*-1 33 100  %d '"""%(level)
        if(vvar == 'vgrd'): opds="""-k '4*-1 34 100  %d '"""%(level)
        return(opds)



    def getStat4Str(self,strCard):

        tt=strCard.split(':')
        vdtg="%s%s"%(tt[0],tt[1])
        expname=tt[2]
        veriModel=tt[3]
        plev=int(tt[4])
        vvar=tt[5].lower()
        ovar=self.getVname(vvar)
        tau=int(tt[6])
        akey=int(tt[7])
        area=self.areaKey(akey)
        stat=float(tt[8])*0.0001
        return(ovar,plev,tau,area,stat)







class FimStdOut(MFutils):


    def __init__(self,rec):

        TS={}
        vardesc={}

        (
            rundate,
            rundtg,
            timestep,
            timestepunits,
            Ntimesteps,
            dtau,
            dtauunits,
            gwnoise,
            gpr,
            gprl,
            gprc,
            gmass,
            gh2o,
            gclh2o,
            gpraccum,
            gevap,
            modtimers,
            )=rec


        self.rundate=rundate
        self.rundtg=rundtg
        self.timestep=timestep
        self.timestepunits=timestepunits
        self.Ntimesteps=Ntimesteps
        self.dtau=dtau
        self.dtauunits=dtauunits
        self.modtimers=modtimers

        TS['gwnoise']=gwnoise
        TS['gpr']=gpr
        TS['gprl']=gprl
        TS['gprc']=gprc
        TS['gmass']=gmass
        TS['gh2o']=gh2o
        TS['gclh2o']=gclh2o
        TS['gpraccum']=gpraccum
        TS['gevap']=gevap

        self.TS=TS

        vardesc['gwnoise']='Gravity Wave Noise rms(dp*2/dt*2)'
        vardesc['gpr']='Global Total Precip'
        vardesc['gprl']='Global Large-Scale Precip'
        vardesc['gprc']='Global Convective Precip'
        vardesc['gmass']='Global 3D mass'
        vardesc['gh2o']='Global 3D water vapor'
        vardesc['gclh2o']='Global 3D cloud water'
        vardesc['gpraccum']='Global integ acc precip'
        vardesc['gevap']='Global integ evaporation'

        self.vardesc=vardesc


class FieldRequest(MFutils):

    mplevs=[1000,925,850,700,500,400,300,250,200,150,100]

    def I2Osfcvar(self,ivar,ilevcode,unitscode=None):

        ovar=ivar
        for s in self.sfcvars.keys():

            ilevchk=ilevcode.replace(',','.')

            vcomp=(ivar == self.sfcvars[s][0])
            lcomp=(ilevchk == self.sfcvars[s][1])

            ucomp=1
            if(vcomp and lcomp and ucomp):
                return(s)

        return(ovar)


    def I2Ouavar(self,ivar):

        ovar=ivar

        for u in self.uavars.keys():
            if(ivar == self.uavars[u][0]):
                return(u)

        return(ovar)




class FieldRequest1(FieldRequest):


    def __init__(self,ftype='std',etau=240):


##         sfcvars={}
##         uavars={}

##         sfcvars['uas']=['ua','109.1']
##         sfcvars['vas']=['va','109.1']
##         sfcvars['tas']=['ta','109.1']
##         sfcvars['psl']=['psl','102.1'] 
##         sfcvars['pr']=['pr','1.1']
##         sfcvars['prc']=['prc','1.1']
##         sfcvars['prw']=['prw','1.1']

##         uavars['ua']  = ['ua', ['100.1000','100.925','100.850','100.700','100.500','100.300','100.200']]
##         uavars['va']  = ['va', ['100.1000','100.925','100.850','100.700','100.500','100.300','100.200']]
##         uavars['zg']  = ['zg', ['100.1000','100.850','100.700','100.500','100.200']]
##         uavars['hur'] = ['hur',['100.1000','100.925','100.850','100.700','100.500','100.300','100.200']]
##         uavars['ta']  = ['ta', ['100.1000','100.925','100.850','100.700','100.500','100.300','100.200']]


        sfcvars={}
        uavars={}

        uarequest={}

        uvplevs=self.mplevs
        zplevs=self.mplevs
        tplevs=self.mplevs
        rhplevs=self.mplevs

        uarequest['ua']=[]
        uarequest['va']=[]
        uarequest['zg']=[]
        uarequest['ta']=[]
        uarequest['hur']=[]


        for plev in uvplevs:
            uarequest['ua']=uarequest['ua']+ ['100.%d'%(plev)]
            uarequest['va']=uarequest['va']+ ['100.%d'%(plev)]

        for plev in zplevs:
            uarequest['zg']=uarequest['zg']+ ['100.%d'%(plev)]

        for plev in tplevs:
            uarequest['ta']=uarequest['ta']+ ['100.%d'%(plev)]

        if(len(rhplevs) > 0):
            for plev in rhplevs:
                uarequest['hur']=uarequest['hur']+ ['100.%d'%(plev)]


# stan added real 10 m on 20110915     ...
#746:266545560:d=11110700:ua:kpds5=33:kpds6=105:kpds7=10:TR=0:P1=72:P2=0:Time1:10 m above gnd:72hr fcst:NAve=0
#747:266870544:d=11110700:va:kpds5=34:kpds6=105:kpds7=10:TR=0:P1=72:P2=0:Time1:10 m above gnd:72hr fcst:NAve=0

#        sfcvars['uas']=['ua','109.1']
#        sfcvars['vas']=['va','109.1']
# -- 20111107 use real sfc winds
        sfcvars['uas']=['ua','105.10']
        sfcvars['vas']=['va','105.10']

        sfcvars['tas']=['ta','109.1']
        sfcvars['hurs']=['hur','109.1']

        sfcvars['ts']=['ta','1.1']

        sfcvars['psl']=['psl','102.1'] 
        sfcvars['pr']=['pr','1.1']
        sfcvars['prc']=['prc','1.1']
        sfcvars['prw']=['prw','1.1']

        sfcvars['ao2d']=['ao2d','1.1']
        sfcvars['hfls']=['hfls','1,1']
        sfcvars['hfss']=['hfss','1,1']
        sfcvars['ia2d']=['ia2d','1,1']
        sfcvars['ib2d']=['ib2d','1,1']
        sfcvars['id2d']=['id2d','1,1']
        sfcvars['io2d']=['io2d','1.1']
        sfcvars['is2d']=['is2d','1,1']
        sfcvars['rls'] =['rls','1.1']
        sfcvars['rss'] =['rss','1.1']
        sfcvars['sno'] =['sno','1.1']


        uavars['ua']  = ['ua',  uarequest['ua'] ]
        uavars['va']  = ['va',  uarequest['va'] ]
        uavars['zg']  = ['zg',  uarequest['zg']  ]
        uavars['hur'] = ['hur', uarequest['hur']   ]
        uavars['ta']  = ['ta',  uarequest['ta']  ]



        btau=0
        dtau=6
        ttaus=range(btau,etau+1,dtau)

        self.sfcvars=sfcvars
        self.uavars=uavars
        self.ttaus=ttaus
        self.ftype=ftype




class FieldRequest2(FieldRequest):


    def __init__(self,ftype='std',etau=240):

        sfcvars={}
        uavars={}

        uarequest={}

        uvplevs=self.mplevs
        zplevs=self.mplevs
        tplevs=self.mplevs
        rhplevs=self.mplevs

        uarequest['ugrd']=[]
        uarequest['vgrd']=[]
        uarequest['hgt']=[]
        uarequest['tmp']=[]
        uarequest['rh']=[]


        for plev in uvplevs:
            uarequest['ugrd']=uarequest['ugrd']+ ['100.%d'%(plev)]
            uarequest['vgrd']=uarequest['vgrd']+ ['100.%d'%(plev)]

        for plev in zplevs:
            uarequest['hgt']=uarequest['hgt']+ ['100.%d'%(plev)]

        for plev in tplevs:
            uarequest['tmp']=uarequest['tmp']+ ['100.%d'%(plev)]

        if(len(rhplevs) > 0):
            for plev in rhplevs:
                uarequest['rh']=uarequest['rh']+ ['100.%d'%(plev)]



        #sfcvars['uas']=['ugrd','105.1']
        #sfcvars['vas']=['vgrd','105.1']

        # -- real sfc wind in grib2 --
        #
        sfcvars['uas']=['ugrd','103.10']
        sfcvars['vas']=['vgrd','103.10']

        sfcvars['tas']=['tmp','105.1']
        sfcvars['hurs']=['rh','105.1']
        sfcvars['ts']=['tmp','1.0','0,0,0']
        sfcvars['psl']=['var','101.0']
        # -- 20150113 -- added ,1 to 0,1,8|10 units var
        sfcvars['pr']=['apcp','1.0','0,1,8,1']
        sfcvars['prc']=['acpcp','1.0','0,1,10,1']
        sfcvars['prw']=['pwat','1.0']

        uavars['ua']  = ['ugrd', uarequest['ugrd'] ]
        uavars['va']  = ['vgrd', uarequest['vgrd'] ]
        uavars['zg']  = ['hgt',  uarequest['hgt']  ]
        uavars['hur'] = ['rh',   uarequest['rh']   ]
        uavars['ta']  = ['tmp',  uarequest['tmp']  ]

        btau=0
        dtau=6
        ttaus=range(btau,etau+1,dtau)

        self.sfcvars=sfcvars
        self.uavars=uavars
        self.ttaus=ttaus
        self.ftype=ftype





class FimRun(FIM,Grib1,Grib2):


    def __init__(self,FE,gribver=2,override=0,verb=0,docpalways=1,dobail=1,
                 doverif=0,
                 dofimx=0,
                 usedataTaus=0,
                 doTT=0,
                 gridRes=None,
                 ):

        if(FE == None):
            print 'must initialize with a FimExp object...'
            sys.exit()


        if(not(w2.onWjet or w2.onZeus)): docpalways=0

        self.curdtg=mf.dtg()
        self.verb=verb
        self.override=override
        self.gribver=gribver
        self.docpalways=docpalways
        self.dofimx=dofimx
        self.usedataTaus=usedataTaus
        self.doverif=doverif
        self.gridRes=gridRes

        self.initVars(FE)
        self.initGribPrc()
        self.initSourceTarget()
        if(self.initDataThere() == 0 and dobail): self.FimRunOK=0 ; return
        if(self.initTargetDirs() == 0 and dobail): self.FimRunOK=0 ; return
        self.initGribs()
        self.initTrackers()
        self.initStdOut()
        self.initPyp()
        self.initSvnInfo()

        if(not(w2.onWjet or w2.onZeus) and doTT):   self.initTT()  # make TmTrk (TT) object

        self.FimRunOK=1


    def lsSdir(self,verb=0):

        if(w2.onWjet or w2.onZeus):
            ff=glob.glob("%s/fim_C*/stdout"%(self.sDir))
        else:
            stdmask="%s/fim.stdout.txt"%(self.tDirNotag)
            ff=glob.glob(stdmask)


        nruns=len(ff)
        nNaNs=[]
        sumNaNs=0
        for f in ff:
            cmd="grep NaN %s"%(f)
            tt=os.popen(cmd).readlines()
            sumNaNs=sumNaNs+len(tt)
            nNaNs.append(len(tt))

        if(verb):
            for n in range(0,nruns):
                print 'Nrun: ',n,' for: ',self.dtg,self.FE.fmodel,' #Nan: ',nNaNs[n],' path: ',ff[n]

        self.nfimruns=nruns
        self.fimnNaNs=nNaNs
        self.sumNaNs=sumNaNs
        self.fimpaths=ff


    #iiiiiiiiiiiiiiiiiiiiiiiiiiiiiii init methods
    #
    def initVars(self,FE):

        self.FE=FE

        self.dtg=FE.dtg
        self.expopt=FE.expopt
        self.fimtype=FE.fimtype
        self.comment=FE.comment

        self.sRoot=FE.sroot
        self.tRoot=FE.troot
        self.lRoot=FE.lroot
        self.fimsuffix=FE.fimsuffix

        self.fimver=FE.fimver
        self.glvl=FE.glvl
        self.nlvl=FE.nlvl
        self.npes=FE.npes

        self.fimtype=FE.fimtype
        self.lasttau=FE.lasttau

        self.reqtaus=range(FE.btau,FE.etau+1,FE.dtau)
        self.iokreqtaus={}
        for tau in self.reqtaus:
            self.iokreqtaus[tau]=0

        self.trackerTau=self.lasttau

        # set gribver -- if qsub, always set as 1
        #
        if(self.fimver == 'qsub'): self.gribver=1

        self.fimtag="fim%s_%s_%s"%(self.glvl,self.nlvl,self.npes)

        if(self.fimver == None):
            self.fimtag="fim_%s_%s_%s"%(self.glvl,self.nlvl,self.npes)

        self.jday=mf.Dtg2JulianDay(self.dtg)
        self.yy=self.dtg[2:4]

        self.maxtauModel=self.lasttau

        # -- put the anom stats here...
        #
        self.verifStats={}


    def initGribPrc(self):

        # environment may set path to non grads1.10 gribmap and grads -- so force here to '1'
        # after symbolic links -- also add grads1 path, must come from environment
        #

        if(self.gribver == 1):

            # -- mf 20110110 :: force use of grads2
            #grads1BinDir="%s/bin"%(os.getenv('W2_GRADS1_BDIR'))
            grads1BinDir="%s/bin"%(os.getenv('W2_GRADS2_BDIR'))
            self.xwgrib="%s/wgrib"%(grads1BinDir)
            self.xgribmap="%s/gribmap"%(grads1BinDir)
            self.gribtype='grb1'

        elif(self.gribver == 2):
            grads2BinDir="%s/bin"%(os.getenv('W2_GRADS2_BDIR'))
            wgrib2BinDir="%s"%(os.getenv('W2_BDIRBIN'))
            wgrib2BinDir=os.getenv('W2_BDIRBIN')
            self.xwgrib="%s/wgrib2"%(wgrib2BinDir)
            self.xgribmap="%s/gribmap"%(grads2BinDir)
            self.gribtype='grb2'

    def initSourceTarget(self,doqsubchk=0):


        #ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss
        # set up source
        #
        if(self.sRoot != None):

            # set base sourse dir -- where the model is run
            #
            print '000000',self.fimver,self.fimsuffix
            if(self.fimver == None or self.fimver == 'wfm'):
                if(self.fimsuffix != None):
                    self.sDir="%s/FIMrun%s/%s_%s00"%(self.sRoot,self.fimsuffix,self.fimtag,self.dtg)
                else:
                    self.sDir="%s/FIMrun/%s_%s00"%(self.sRoot,self.fimtag,self.dtg)

                # -- new option to set whether using dtg vice fimtag in the dir name
                #    dtg is now used on all real-time on jet/zeus avoids issue of npe in dir name
                #
                if(self.FE.useDtgDirName):  
                    if(self.fimsuffix != None):
                        self.sDir="%s/FIMrun%s/%s"%(self.sRoot,self.fimsuffix,self.dtg)
                    else:
                        self.sDir="%s/FIMrun/%s"%(self.sRoot,self.dtg)
                        
                    
            elif(self.fimver == 'qsub'):
                if(doqsubchk):
                    mask0="%s/%s_*"%(self.sRoot,self.fimtag)
                    mask1="%s/%s*/"%(self.sRoot,self.fimtag)

                    dirs0=glob.glob(mask0)
                    dirs1=glob.glob(mask1)

                    if(len(dirs0) == 1):
                        self.sDir=dirs0[0]

                    elif(len(dirs1) == 1):
                        self.sDir=dirs1[0]
                    else:
                        # mf 20110201 -- allow fall through when sRoot does not exists/cleaned,
                        # but target still there for followon analysis
                        #
                        print 'WWW(initSourceTarget) no data in mask0: ',mask0,' or mask1: ',mask1,' setting sDir to None'
                        self.sDir=None
                        #sys.exit()
                else:
                    self.sDir="%s/%s"%(self.sRoot,self.fimtag)


            else:
                print 'qqqqqqqqqqqqqqqqqqqqqqqq'
                if(self.fimsuffix != None):
                    self.sDir="%s/%s/FIMrun%s/%s_%s00_%s"%(self.sRoot,self.fimver,self.fimsuffix,self.fimtag,self.dtg,self.expopt)
                else:
                    self.sDir="%s/%s/FIMrun/%s_%s00_%s"%(self.sRoot,self.fimver,self.fimtag,self.dtg,self.expopt)
                    

            # -- set wfm dir
            #
            self.wfmDir="%s/FIMwfm"%(self.sRoot)
            self.veriFtDir=None
            if(self.doverif):  self.veriFtDir="%s/%s/verif"%(self.tRoot,self.expopt)


            # set base source dir with output
            #
            if(self.fimver == 'qsub' and self.sDir != None):
                self.sGribDir="%s/post/"%(self.sDir)
                self.sTrackerDir="%s/tracker/%s"%(self.sDir,self.trackerTau)
                self.sOutDir="%s/fim"%(self.sDir)
            else:
                self.sGribDir="%s/post_%s/fim/NAT/grib%1d"%(self.sDir,self.fimtype,self.gribver)
                self.sTrackerDir="%s/tracker_%s/%s"%(self.sDir,self.fimtype,self.trackerTau)
                self.sOutDir="%s/fim_%s"%(self.sDir,self.fimtype)


            try:
                self.sAdeckPath=glob.glob("%s/track.*"%(self.sTrackerDir))[0]
                self.sTrackerGribPath=glob.glob("%s/track.*"%(self.sTrackerDir))[0]
            except:
                self.sAdeckPath=None
                self.sTrackerGribPath=None

            self.gmask="%s/%s%s????????"%(self.sGribDir,self.yy,self.jday)
            self.sStdOutPath="%s/stdout"%(self.sOutDir)
            self.sFIMnamelist="%s/../FIMnamelist"%(self.sDir)

            # -- this is always true?
            self.sFIMnamelist="%s/FIMnamelist"%(self.sOutDir)


        if(self.fimver == None or self.fimver == 'wfm'):
            self.tDir="%s/dat/%s/%s/%s"%(self.tRoot,self.expopt,self.dtg,self.fimtag)
            self.tDirNotag="%s/dat/%s/%s"%(self.tRoot,self.expopt,self.dtg)
        elif(self.fimver == 'qsub'):
            self.tDir="%s/dat/%s/%s/%s"%(self.tRoot,self.fimtag,self.expopt,self.dtg)
            self.tDirNotag="%s/dat/%s/%s"%(self.tRoot,self.expopt,self.dtg)
        else:
            self.tDir="%s/dat/%s/%s/%s/%s"%(self.tRoot,self.fimver,self.fimtag,self.expopt,self.dtg)
            self.tDirNotag="%s/dat/%s/%s"%(self.tRoot,self.expopt,self.dtg)

        # -- 20121206 -- force the target dir to be the same on jet/zeus as locally...
        #
        if(w2.onWjet or w2.onZeus):
            self.tDir=self.tDirNotag
            

    def initDataThere(self):

        #eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
        # check if source and target dir...
        #
        self.sdatathere=self.tdatathere=self.datathere=1
        if(not(mf.ChkDir(self.sDir,diropt='quiet'))): self.sdatathere=0
        if(not(mf.ChkDir(self.tDir,diropt='quiet'))): self.tdatathere=0

        # bail if source processing not there...and onWjet
        #
        if( not(self.sdatathere) and (w2.onWjet or w2.onZeus)):
            print "WWW(FimRun) initDataThere -- sdatathere = 0 and onWjet"
            return(0)

        if(self.verb): print 'GGGG gmask: ',self.gmask,'lllllllllllllllllllllll ',len(glob.glob(self.gmask))
        # now check if any data there
        if(len(glob.glob(self.gmask)) == 0): self.sdatathere=0


        # check if both s and t data dirs there ... always do gribver=1 if on wjet, so by the time
        # we want to do the grib, the t dir should be there...
        #
        if( self.sdatathere == 0 and self.tdatathere == 0 ):
            self.datathere=0
            if(w2.onWjet or w2.onZeus):
                if(self.verb): print 'EEE source dir: ',self.sDir,' and tdir: ',self.tDir,' not there, sayoonara'
                return(0)

        # -- check if source gone but target there -- was redone and need to redo?
        #
        if( self.sdatathere == 0 and self.tdatathere == 1 ):
            self.datathere=0
            if(w2.onWjet):
                print 'WWW source dir: ',self.sDir,' gone, but tdir: ',self.tDir,' there -- redo? use -O option'
                return(0)


    def initTargetDirs(self,domkdir=1):

        #pppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp
        # set up paths
        #

        if(hasattr(self,'veriFtDir') and self.veriFtDir != None):
            if(domkdir): mf.ChkDir(self.veriFtDir,'mk')

        if(self.tRoot != None and self.sdatathere):
            if(domkdir): mf.ChkDir(self.tDir,'mk')

        #tttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt
        # check tdir
        #

        self.tOutDir=None
        if(domkdir):
            if(mf.ChkDir(self.tDir,diropt='quiet')): self.tOutDir="%s"%(self.tDir)
        else:
            self.tOutDir="%s"%(self.tDir)

        # if local, chk both tDir and tDirNotag
        #

        if(not(w2.onWjet or w2.onZeus)):
            if(self.tDirNotag != None):
                if(domkdir and self.tdatathere): mf.ChkDir(self.tDirNotag,diropt='mk')
                self.tOutDir="%s"%(self.tDirNotag)
            elif(self.tDir != None):
                if(domkdir and self.tdatathere): mf.ChkDir(self.tDir,diropt='mk')
                self.tOutDir="%s"%(self.tDir)

        if(self.tOutDir == None):
            print 'WWW tdir and tDirNotag do not exists; gribver',self.gribver,' returning...'
            return(0)

        if(w2.onWjet or w2.onZeus):
            self.pyppath="%s/FRwjet.pyp"%(self.tOutDir)
        else:
            self.pyppath="%s/FR.pyp"%(self.tOutDir)

        self.tbase="fim%s.%s"%(self.glvl,self.expopt)
        self.tdatbase="%s/%s"%(self.tOutDir,self.tbase)
        self.tdatbase="%s/fim%s.%s"%(self.tOutDir,self.glvl,self.expopt)
        self.ctlpath="%s.%s.ctl"%(self.tdatbase,self.gribtype)
        self.gmppath="%s.%s.gmp"%(self.tdatbase,self.gribtype)
        self.gmpfile="%s.%s.gmp"%(self.tbase,self.gribtype)
        self.gtime=mf.dtg2gtime(self.dtg)



    def initGribs(self):

        self.grbtaus=None

        #gggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggg
        # grib files
        #
        if(self.sRoot != None):
            gpaths=glob.glob(self.gmask)

            taus=[]
            for gpath in gpaths:

                (dir,file)=os.path.split(gpath)
                tau=int(file[-4:])
                taus.append(tau)

                tpath="%s/fim.%s.f%03d.%s"%(self.tOutDir,self.dtg,tau,self.gribtype)
                
                if(not(os.path.exists(tpath)) or self.override > 0 and self.override != 3):
                    cmd="ln -f -s %s %s"%(gpath,tpath)
                    mf.runcmd(cmd)

                if(tau in self.reqtaus):
                    self.iokreqtaus[tau]=1


            taus=mf.uniq(taus)
            taus.sort()

            self.gribtaus=taus

    def initTrackers(self):

        #tttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt
        # cp over trackers tcvitals...for last tau or last tau-12
        #
        self.GetLatestTrackers(override=self.override)


        #cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
        #  prs and hbl .ctl for all fields out of post
        #
        if(self.lasttau in self.gribtaus or self.override == 3): self.DoAllCtl(override=self.override)


    def initStdOut(self):

        from fm2 import FIM

        #ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss
        # do a little work here...put stdout from fim in the target dir,
        # parse and the make stdout pickle
        #
        self.tStdOutPath="%s/fim.stdout.txt"%(self.tOutDir)
        self.tFIMnamelist="%s/FIMnamelist"%(self.tOutDir)
        self.std_pyppath="%s/fim.stdout.pyp"%(self.tOutDir)

        if( (
            ( (not(os.path.exists(self.tStdOutPath)) and os.path.exists(self.sStdOutPath) ) and
              (self.usedataTaus == 0 and self.lasttau in self.gribtaus) and
              self.sRoot != None) or
            ( self.fimver == 'qsub') or
            self.docpalways == 1
            ) and self.docpalways != -1

            ):

            # -- check pathological case of no stdout ...
            #
            if(MF.ChkPath(self.sStdOutPath)):
                cmd="cp -p %s %s"%(self.sStdOutPath,self.tStdOutPath)
                mf.runcmd(cmd,'')

                self.fS=FIM(self.sStdOutPath)
            #self.ParseStdOut(override=1)

        # get FIMnamelist...to document the run
        #
        if( ((not(os.path.exists(self.tFIMnamelist)) and os.path.exists(self.sFIMnamelist))
             or self.docpalways
             ) and self.docpalways != -1
            ):
            cmd="cp -p %s %s"%(self.sFIMnamelist,self.tFIMnamelist)
            mf.runcmd(cmd,'')


    def initPyp(self):

        #pppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp
        #  pickle object
        #

        self.curdtghms=mf.dtg('dtg.hms')

        if(hasattr(self,'pyppath') and curuSer == 'fiorino' and self.tdatathere):
            if(self.verb): print 'pppppppppppppppppppppppppp pickling: ',self.pyppath,' in FimRun at: ',self.curdtghms
            self.PutPyp()


    def initTT(self):

        from TCtrk import TmTrk

        self.LsGrib(lsopt=0)

        if(self.FE != None):
            if(not(hasattr(self.FE,'model'))):
                return(-1)
            else:
                model=self.FE.model
        else:
            model=self.model

        atcfname=setAtcfname(model)
        year=self.dtg[0:4]
        tdir=self.tOutDir
        tdirTT="%s/tctrk"%(tdir)
        tdirAdeck="%s/esrl/%s/w2flds"%(AdeckBaseDir,year)
        taus=self.tdattausData
        if(len(taus) > 0):
            maxtau=taus[-1]
            if(hasattr(self,'ctlpathM2')):
                ctlpath=self.ctlpathM2
            else:
                ctlpath=self.ctlpath

            TT=TmTrk(self.dtg,model,atcfname,tdirTT,tdirAdeck,taus,maxtau,ctlpath,verb=self.verb)
            TT1=TT.getPyp(unlink=0)
            if(TT1 != None):
                TT=TT1
                TT.taus=taus
                if(hasattr(self,'maxtauModel')):
                    TT.maxtauModel=self.maxtauModel
                else:
                    TT.maxtauModel=self.lasttau

            self.TT=TT
            self.TT.verb=self.verb

        else:
            self.TT=None


    def initSvnInfo(self):

        if(w2.onWjet or w2.onZeus):

            self.svnuRl=None
            self.svnRevision=None
            self.svnChangeRevAuthor=None
            self.svnChangeRev=None
            self.svnChangeDate=None
            self.svnChangeTime=None
            self.svnChangeDtg=None
            self.svncomment=None


            svnDir=self.sRoot
            if(self.fimver == 'qsub'): svnDir="%s/.."%(self.sRoot)

            cmd="svn info %s"%(svnDir)
            cards=os.popen(cmd).readlines()
            if(len(cards) == 0): return

            for card in cards:
                card=card[:-1]
                tt=card.split()
                if(self.verb): print 'svn info: ',card
                if(mf.find(card,'RL:')):
                    self.svnuRl=tt[1]
                if(mf.find(card,'Revision:')):
                    self.svnRevision=tt[1]
                if(mf.find(card,'Changed Author:')):
                    self.svnChangeRevAuthor=tt[3]
                if(mf.find(card,'Changed Rev:')):
                    self.svnChangeRev=tt[3]
                if(mf.find(card,'Changed Date:')):
                    self.svnChangeDate=tt[3]
                    self.svnChangeTime=tt[4]

            if(self.svnChangeDate != None and self.svnChangeTime != None):
                dd=self.svnChangeDate.split('-')
                hh=self.svnChangeTime.split(':')
                dtg=dd[0]+dd[1]+dd[2]+hh[0]
                self.svnChangeDtg=dtg


            if(self.svnChangeDtg != None):
                if(mf.dtgdiff(self.svnChangeDtg,self.dtg) >= 0.0):
                    self.svncomment="svn rev: %s dtg: %s url: %s author: %s"%(
                        self.svnRevision,
                        self.svnChangeDtg,
                        self.svnuRl,
                        self.svnChangeRevAuthor,
                    )


    def GetLatestTrackers(self,override=0,ropt='',verb=0):
        """
        get trackers for latest tau counting down from lasttau (168)
        """
        testtaus=[self.lasttau,self.lasttau-12,self.lasttau-24,120]
        gottau=None
        if(verb):
            print 'gribtaus: ',self.gribtaus
        for ttau in testtaus:
            for n in range(len(self.gribtaus)-1,-1,-1):
                gtau=self.gribtaus[n]
                if(gtau == ttau):
                    gottau=ttau
                    break
            if(gottau != None): break


        if(verb): print 'dtg: ',self.dtg,' testtaus: ',testtaus,' gottau: ',gottau
        if(gottau == None):
            return
        else:

            sfiles=glob.glob("%s/*vital*"%(self.sTrackerDir))
            tfiles=glob.glob("%s/track.*"%(self.sTrackerDir))
            ofiles=glob.glob("%s/track.*"%(self.tOutDir))

            if(verb):
                print 'sfiles: ',len(sfiles)
                print 'tfiles: ',len(tfiles)
                print 'ofiles: ',len(ofiles)
                print 'tOutDir: ',self.tOutDir

            if( (len(sfiles) == 1) and (len(ofiles) == 0 or override >= 1) ):
                cmd="cp -p %s %s/."%(sfiles[0],self.tOutDir)
                mf.runcmd(cmd,ropt)

                cmd="cp -p %s %s/."%(tfiles[0],self.tOutDir)
                mf.runcmd(cmd,ropt)


    def getTCtrkStatus(self,verb=0):


        if(not(w2.onKishou) and not(w2.onKaze)): return(-1)

        if(not(hasattr(self,'TT'))):  self.initTT()
        rc=self.TT.chkTrkStatus()

        return(rc)


    def runTCtrk(self,dolsonly=0,verb=0,override=0,dotrkonly=0):

        self.initTT()
        if(self.TT != None):
            self.TT.doTrk(ropt='',dolsonly=dolsonly,override=override,dotrkonly=dotrkonly)
        TT=self.TT
        return(TT)



    def LnFc(self,dtau=12,override=0,ropt='',verb=0):
        """
        make sybmolic links to do ensembles by forecast (FC)
        """
        sdir=self.tOutDir
        tdir=os.path.normpath("%s/.."%(sdir))
        if(not(mf.ChkDir(sdir,''))): return
        for n in range(0,len(self.tdattaus)):
            tau=self.tdattaus[n]
            ftau="f%03d"%(tau)
            vdtg=mf.dtginc(self.dtg,tau)
            if(tau%dtau == 0):
                spath=self.tdatpaths[tau]
                ldir="%s/%s"%(tdir,ftau)
                mf.ChkDir(ldir,'mk')
                lpath="%s/%s.%s.%s"%(ldir,self.tbase,vdtg,self.gribtype)
                if(not(os.path.exists(lpath)) or override):
                    cmd="ln -s -f %s %s"%(spath,lpath)
                    mf.runcmd(cmd,ropt)
                else:
                    if(verb): print '  did:  ln -s ',spath,lpath
                    continue


        self.dtauLnFc=dtau




    def EnsFcCtl(self,bdtg=None,edtg=None,ddtg=12,
                 taumax=taumax,
                 override=0,chkonly=0,ropt='',verb=0):
        """
        make .ctl for model runs as an ensemble of forecasts f000, f012, ... ,fLLL
        """


        (bdtg,edtg)=setEnsFcBdtgEdtg(bdtg,edtg,taumax)

        self.dtgopt="%s.%s.%d"%(bdtg,edtg,ddtg)
        fcdtgs=mf.dtg_dtgopt_prc(self.dtgopt)
        nt=len(fcdtgs)

        print 'lllllllllllllllll ',nt,bdtg,edtg,ddtg

        if(hasattr(self,'sdirbase')): self.tOutDir="%s/%s"%(self.sdirbase,bdtg)
        if(not(hasattr(self,'dtg'))): self.dtg=bdtg
        if(not(hasattr(self,'gribver'))): self.gribver=self.gribtype[-1]
        if(not(hasattr(self,'tdatbase'))): self.tdatbase="%s/%s.%s"%(self.tOutDir,self.tbase,self.dtg)
        if(not(hasattr(self,'ctlpath'))): self.ctlpath="%s.ctl"%(self.tdatbase)

        sdir=self.tOutDir
        tdirc=os.path.normpath("%s/../../ensFC"%(sdir))
        if(not(mf.ChkDir(sdir,''))): return
        mf.ChkDir(tdirc,'mk')


        octlpath="%s/%s.%s.ctl"%(tdirc,self.tbase,self.gribtype)
        ogmppath="%s/%s.%s.gmp"%(tdirc,self.tbase,self.gribtype)
        self.ensFcCtlpath=octlpath
        self.ensFcGmppath=ogmppath

        #
        # just get paths...
        #

        if(chkonly and os.path.exists(self.ensFcCtlpath) and os.path.exists(self.ensFcCtlpath)):
            return



        #
        # run lsgrib and do lnfc
        #

        for fcdtg in fcdtgs:
            self.tdatbase=self.tdatbase.replace(self.dtg,fcdtg)
            self.dtg=fcdtg
            self.LsGrib(lsopt=0)
            if(len(self.tdattaus) > 0):
                self.LnFc(verb=verb,override=override)
            else:
                print 'WWW no taus for dtg: ',self.dtg,' model: ',self.model


        if(not(os.path.exists(self.ctlpath))):
            print 'WWW ctlpath for model: ',self.model,' bdtg: ',bdtg,' gribver: ',self.gribver,' is not there try other dtg/gribver'
            for fcdtg in fcdtgs:
                tctlpath=self.ctlpath.replace(bdtg,fcdtg)
                if(os.path.exists(tctlpath)):
                    self.tdatbase=self.tdatbase.replace(self.dtg,fcdtg)
                    self.dtg=fcdtg
                    self.LsGrib(lsopt='0')
                    break

        else:
            tctlpath=self.ctlpath
            self.tdatbase=self.tdatbase.replace(self.dtg,bdtg)
            self.dtg=bdtg
            self.LsGrib(lsopt=0)

        self.tctlpath=tctlpath

        #
        # make the fc taus that will be the ensemble dimentions
        #
        fctaus=[]
        for fctau in self.tdattaus:
            if(fctau%self.dtauLnFc == 0):
                fctaus.append(fctau)

        #
        # make the 5-d .ctl
        #
        cards=open(tctlpath).readlines()

        (dir,file)=os.path.split(tctlpath)
        (base,ext)=os.path.splitext(file)

        ntaus=len(fctaus)

        edefcard="edef %d names "%(ntaus)
        for fctau in fctaus:
            edefcard="%s f%03d"%(edefcard,fctau)

        octl=''
        for n in range(0,len(cards)):
            card=cards[n]
            if(mf.find(card,'dset')):
                card="dset ^../%s/%%e/%s.%%y4%%m2%%d2%%h2.%s"%(self.model,self.tbase,self.gribtype)
                octl=card
            elif(mf.find(card,'index')):
                gmpfile="%s.%s.gmp"%(self.tbase,self.gribtype)
                gmppath="%s/%s"%(tdirc,gmpfile)
                gmpcard="index ^%s"%(gmpfile)
                octl="""%s
%s"""%(octl,gmpcard)

            elif(mf.find(card,'tdef')):
                gtime=mf.dtg2gtime(bdtg)
                tdefcard="tdef %d linear %s %dhr"%(nt,gtime,self.dtauLnFc)
                octl="""%s
%s
%s"""%(octl,tdefcard,edefcard)

            else:
                octl="""%s
%s"""%(octl,card.strip())

        self.WriteCtl(octl,octlpath)

        #
        # force use of gribmap2 since we're unsing the ensemble dimension
        #
        dogribmap=1
        if(dogribmap):
            self.ctlpath=octlpath
            self.gribtype='grb2'
            self.DoGribmap(gmpverb=verb)
        return

    def CnvGrib1to2(self,ropt='',override=0,verb=0):
        """
        lopt = 0 -- turns off inventory
        """

        # set up the variables for GRIB.MakeCtl

        self.tdatpaths={}
        self.taus=[]
        self.ttaus=[]
        self.tdatmask="%s.f%%f3.%s"%(self.tbase,self.gribtype)


        # get the gribs and convert

        grib1mask="%s.f???.grb1"%(self.tdatbase)
        gribs=glob.glob(grib1mask)
        gribs.sort()

        for grib1 in gribs:
            grib2=grib1.replace('grb1','grb2')
            if(not(os.path.exists(grib2))):
                cmd="cnvgrib -g12 %s %s"%(grib1,grib2)
                mf.runcmd(cmd,ropt)

            # fill in MakeCtl vars
            (dir,file)=os.path.split(grib2)
            tau=int(file.split('.')[2][1:])
            self.taus.append(tau)
            self.ttaus.append(tau)
            self.tdatpaths[tau]=grib2

        if(len(self.taus) > 0):
            # make the .ctl
            self.MakeCtl(verb=0)



    def LsGrib(self,dowgribinv=1,override=0,lsopt='s',verb=0,
               doCurAge=0,doSdatCurAge=onWjet,doStdOutCurAge=onWjet):
        """
        lsopt = 0 -- turns off inventory
        set doSdatCurAge based on being on wjet
        """

        ocards=[]

        self.tdatpaths={}
        self.tdattaus=[]
        self.tdattausData=[]
        self.tdatstatus={}

        ocard='%12s  %s'%(self.expopt,self.dtg)
        ocard=ocard+'''   ***>>> NO DATA <<<***'''

        try:
            tpathmask="%s.f???.%s"%(self.tdatbase,self.gribtype)
        except:
            return(0,ocard)

        gribs=glob.glob(tpathmask)
        gribs.sort()

        curdtg=mf.dtg()


        for datpath in gribs:
            (dir,file)=os.path.split(datpath)
            tt=file.split('.')
            ltt=len(tt)
            tau=int(tt[ltt-2][1:])

            try:
                sdatpath=self.sdatpaths[tau]
            except:
                sdatpath=None
                pass

            try:
                sdatcurage=self.sdatpathAges[tau]
            except:
                sdatcurage=-999.
                pass

            # find taus with non-zero file length and add to new list tdattausData
            #
            filesize=os.path.getsize(datpath)
            if(filesize != 0): self.tdattausData.append(tau)

            self.tdattaus.append(tau)

            if(doSdatCurAge): agecur=sdatcurage

            agedatpath=datpath
            if(sdatpath != None and doSdatCurAge): agedatpath=sdatpath

            self.tdatpaths[tau]=datpath

            wgribpath="%s.f%03d.wgrib%1d.txt"%(self.tdatbase,tau,self.gribver)
            if(dowgribinv):
                if(not(os.path.exists(wgribpath)) or (os.path.getsize(wgribpath) == 0 and
                                                      os.path.getsize(datpath) != 0)
                   or override >= 1):

                    cmd="%s %s > %s"%(self.xwgrib,datpath,wgribpath)
                    mf.runcmd(cmd)

            if(os.path.exists(wgribpath)):

                # check if agedatpath is there...if not use output datfile; problem on wjet
                #
                if(not(os.path.exists(agedatpath))): agedatpath=datpath

                # -- check if stdout there, might not be if rerun
                #

                if(doStdOutCurAge and hasattr(self,'tStdOutPath')):
                    age=self.PathCreateTimeDtgdiff(self.dtg,self.sStdOutPath)
                    if(age == None): age=self.PathCreateTimeDtgdiff(self.dtg,self.tStdOutPath)
                    agecur=self.PathCreateTimeDtgdiff(curdtg,self.sStdOutPath)
                    if(agecur == None): agecur=self.PathCreateTimeDtgdiff(curdtg,self.tStdOutPath)

                else:
                    age=self.PathCreateTimeDtgdiff(self.dtg,agedatpath)
                    agecur=self.PathCreateTimeDtgdiff(curdtg,agedatpath)

                # -- in case there is no stdout in source or on target -- when fs problems
                #
                if(age == None and agecur == None):
                    age=self.PathCreateTimeDtgdiff(self.dtg,agedatpath)
                    agecur=self.PathCreateTimeDtgdiff(curdtg,agedatpath)



                nf=len(open(wgribpath).readlines())
                self.tdatstatus[tau]=(age,nf,agecur)


        if(len(gribs) == 0):
            self.tdatathere=0
            if(verb):
                print 'WWW no output grib for ',self.dtg,' for gribver: ',self.gribver
            return(0,ocard)

        # -- if gribs set tdatathere to 1, for lsfim.py
        #
        self.tdatathere=1
        if(lsopt == 0): return(1,None)

        nb=0
        ne=1
        nbe=-2


        if(not(hasattr(self,'comment'))):  self.comment=None
        if(verb):
            print
            print 'tOutdir: ',self.tOutDir,' comment: ',self.comment
            print 'grib %s filter output: %s'%(10*str(self.gribver),self.dtg)
        if(lsopt == 'l'):
            ne=len(self.tdattaus)

        otbase=self.tbase.split()
        if(lsopt == 's' or lsopt == 'l'):
            if(verb): print
            for tau in self.tdattaus[nb:ne]:
                (age,nf,agecur)=self.tdatstatus[tau]
                oage=age
                if(doCurAge or doSdatCurAge): oage=agecur
                if(oage != None):
                    ocard="%12s  %s   %03d   %9.4f  %4d"%(otbase[0],self.dtg,tau,oage,nf)
                    ocards.append(ocard)
                    print ocard
            else:
                if(verb):print 'WWWWWWWWWWWWWWWW oage = None in LsGrib'

        if(lsopt == 'Last'):
            tau=self.tdattaus[-1]
            (age,nf,agecur)=self.tdatstatus[tau]
            oage=age
            if(oage != None):
                if(doCurAge or doSdatCurAge): oage=agecur
                nfstat=''
                if(tau < self.lasttau): nfstat='<<<<*** short '
                ocard="%12s  %s   %03d   %9.4f  %4d %s "%(otbase[0],self.dtg,tau,oage,nf,nfstat)
                ocards.append(ocard)
            else:
                if(verb): print 'WWWWWWWWWWWWWWWW oage = None in LsGrib'


        return(1,ocard)





    def SetFieldRequest(self,sfcvars,uavars,tau):

        request={}
        sfckeys=sfcvars.keys()
        for sfckey in sfckeys:
            tt=sfcvars[sfckey]
            rvar=tt[0]
            rlev=tt[1]
            try:
                runits=tt[2]
            except:
                runits=None

            try:
                request[rvar].append(rlev)
            except:
                request[rvar]=[]
                request[rvar].append(rlev)

            request[rvar,'units']=runits


        uakeys=uavars.keys()

        for uakey in uakeys:
            tt=uavars[uakey]
            rvar=tt[0]
            rlevs=tt[1]

            try:
                runits=tt[2]
            except:
                runits=None
            request[rvar,'units']=runits

            for rlev in rlevs:
                try:
                    request[rvar].append(rlev)
                except:
                    request[rvar]=[]
                    request[rvar].append(rlev)


        request['taus']=[tau]

        return(request)


    def DoGrib(self,FQ,override=0,verb=0,alwaysDoCtl=0):
        """
        FQ is the FieldRequest1/2 object
        """

        # -- first get the output grib inventory
        #
        
        rc=self.LsGrib(lsopt=0,verb=verb,override=override)
        
        if(len(rc) == 2 and rc[0] == 0):
            print "WWW(FM.DoGrib) -- no gribs out of LsGrib() --- press..."
            #return

        self.FQ=FQ
        self.fldrequest={}

        if(self.gribtype == 'grb1'): self.MakeFdb1(override=override)
        if(self.gribtype == 'grb2'):
            if(self.MakeFdb2(override=override) == 0): return

        if(not(hasattr(FQ,'ttaus'))):
            self.ttaus=self.taus
        else:
            self.ttaus=FQ.ttaus

        self.ioktaus={}

        nfmax=-999
        for ttau in self.ttaus:
            try:
                nf=self.tdatstatus[ttau][1]
            except:
                continue

            if(nf > nfmax): nfmax=nf

        for ttau in self.ttaus:
            try:
                nf=self.tdatstatus[ttau][1]
            except:
                continue

            if(nf < nfmax):
                if(verb): print 'RRRR need to redo fdb...for ttau: ',ttau
                if(self.gribtype == 'grb1'): self.MakeFdb1(ttau=ttau)
                if(self.gribtype == 'grb2'): self.MakeFdb2(ttau=ttau)



        shortDone=0

        for ttau in self.ttaus:


            try:
                ipath=self.sdatpaths[ttau]
                opath=self.tdatpaths[ttau]
                self.ioktaus[ttau]=1
                filethere=1
            except:
                filethere=0
                self.ioktaus[ttau]=0

            request=self.SetFieldRequest(FQ.sfcvars,FQ.uavars,ttau)

            self.fldrequest[ttau]=request

            try:
                nf=self.tdatstatus[ttau][1]
                isshort=(nf < nfmax)
                if(verb): print 'CCCC: check if nf is >= nfmax',ttau,nf,nfmax,isshort,shortDone
            except:
                nf=0
                isshort=0


            if(isshort and shortDone == 0): shortDone=1
            #isshort=0

            if( (filethere and not(os.path.exists(opath))) or isshort or override >= 1):

                if(self.gribtype == 'grb1'):
                    (records,recsiz,nrectot)=self.ParseFdb1(ttau=ttau)
                    orecs=self.Wgrib1VarFilter(records,request,verb=verb)
                if(self.gribtype == 'grb2'):
                    (records,recsiz,nrectot)=self.ParseFdb2(ttau=ttau)
                    orecs=self.Wgrib2VarFilter(records,request,ttau,verb=verb)

                if(len(orecs) > 0):
                    if(self.gribtype == 'grb1'): self.Wgrib1Filter(orecs,ipath,opath)
                    if(self.gribtype == 'grb2'): self.Wgrib2Filter(orecs,ipath,opath)
                    self.ioktaus[ttau]=1
                else:
                    self.ioktaus[ttau]=0


        # check if the .ctl and .gmp are there...and all the requested taus...or fixed short taus...
        #

        if(
            ( not(0 in self.iokreqtaus.values()) and not(os.path.exists(self.gmppath)) ) or
            override >= 1 or
            shortDone or
            alwaysDoCtl
            ):

            self.MakeCtl(verb=verb,override=override)
            self.gribdtghms=mf.dtg('dtg.hms')
            (odtg,phr)=mf.dtg_phr_command_prc(self.dtg)
            self.gribphr=float(phr)

            if(verb): print 'pppppppppppppppppppppppppp pickling: ',self.pyppath,' in DoGrib at: ',self.curdtghms
            self.PutPyp()


        else:
            for ttau in self.ttaus:
                if(self.ioktaus[ttau] == 0):
                    print "III need tau: %d for %s"%(ttau,self.dtg)


        if(shortDone or override >= 2):
            self.LsGrib(override=override)




    def DoAllCtl(self,override=0):

        try:
            if(self.dofimx):
                p1lt=PrsFimXCtl(dtg=self.dtg,taus=self.gribtaus,tdir=self.tDir,gridRes=self.gridRes).GetPyp().lasttau
            else:
                p1lt=PrsCtl(dtg=self.dtg,taus=self.gribtaus,tdir=self.tDir,gridRes=self.gridRes).GetPyp().lasttau
        except:
            p1lt=None


        if(p1lt == None or override == 3 or p1lt != self.lasttau):

            if(self.dofimx):
                p1=PrsFimXCtl(dtg=self.dtg,lasttau=self.lasttau,taus=self.gribtaus,tdir=self.tDir,
                              glvl=self.glvl,gridRes=self.gridRes)
            else:
                p1=PrsCtl(dtg=self.dtg,lasttau=self.lasttau,taus=self.gribtaus,tdir=self.tDir,
                          glvl=self.glvl,gridRes=self.gridRes)

            h1=HblCtl(dtg=self.dtg,lasttau=self.lasttau,taus=self.gribtaus,tdir=self.tDir,
                      glvl=self.glvl,nlvl=self.nlvl,gridRes=self.gridRes)

            p1.WriteCtl()
            h1.WriteCtl()

            if(not(os.path.exists(p1.gmppath)) or override == 3):  p1.DoGribmap()
            if(not(os.path.exists(h1.gmppath)) or override == 3):  h1.DoGribmap()

            h1.PutPyp()
            p1.PutPyp()

            self.allhblctl=h1.ctlpath
            self.allprsctl=p1.ctlpath

            self.h1=h1
            self.p1=p1

        elif(override == 2):

            if(self.dofimx):
                p1=PrsFimXCtl(dtg=self.dtg,lasttau=self.lasttau,taus=self.gribtaus,tdir=self.tDir)
            else:
                p1=PrsCtl(dtg=self.dtg,lasttau=self.lasttau,taus=self.gribtaus,tdir=self.tDir)
            h1=HblCtl(dtg=self.dtg,lasttau=self.lasttau,taus=self.gribtaus,tdir=self.tDir)

            self.allhblctl=h1.ctlpath
            self.allprsctl=p1.ctlpath

    def getAllCtl(self):

        if(self.dofimx):
            p1=PrsFimXCtl(dtg=self.dtg,lasttau=self.lasttau,taus=self.gribtaus,tdir=self.tDir)
        else:
            p1=PrsCtl(dtg=self.dtg,lasttau=self.lasttau,taus=self.gribtaus,tdir=self.tDir)
        h1=HblCtl(dtg=self.dtg,lasttau=self.lasttau,taus=self.gribtaus,tdir=self.tDir)

        self.allhblctl=h1.ctlpath
        self.allprsctl=p1.ctlpath


    def runVerif(self,vtaus,vvars,vplevs,vareas,ropt='',verb=0,dozave=1):

        fV=FimVerif()

        def rundiffgb(vtau,vvar,plev,area):
            vdtg=mf.dtginc(self.dtg,vtau)

            grbpath="%s.f%03d.grb1"%(self.tdatbase,vtau)
            grbsiz=MF.GetPathSiz(grbpath)
            if(grbsiz == None or grbsiz == 0):
                grb2path="%s.f%03d.grb2"%(self.tdatbase,vtau)
                cmd="cnvgrib -g21 %s %s"%(grb2path,grbpath)
                MF.runcmd(cmd,ropt)


            ndxpath="%s.ndx"%(grbpath)
            ndxsiz=MF.GetPathSiz(ndxpath)
            if(ndxsiz == None or ndxsiz == 0):
                cmd="/whome/rtfim/diffgb/grbindex.x %s %s"%(grbpath,ndxpath)
                MF.runcmd(cmd,ropt)
            else:
                if(verb): print 'III ndxpath: ',ndxpath,' already done...'


            diffgbcmd="/whome/rtfim/diffgb/diffgb -h -t 'ano'"
            if(dozave):
                zave=""" -z '1 20'"""
            else:
                zave=''

            mgrb=grbpath
            mndx=ndxpath

            mmdd=vdtg[4:8]
            cgrb="%s/cmean_1d.1959%s"%(cmeandir,mmdd)
            cndx="%s.ndx"%(cgrb)

            jday=mf.Dtg2JulianDay(vdtg)
            vyy=vdtg[2:4]
            vhh=vdtg[8:10]

            vgrb="%s/%s/%s%s%s000000.grib1"%(gfsverifdir,vdtg,vyy,jday,vhh)
            vndx="%s/%s/%s%s%s000000.ndx"%(gfsverifdir,vdtg,vyy,jday,vhh)

            gridparams=fV.getGridParams(area)
            opds=fV.getVarPdsLevel(vvar,plev)

            if(verb):

                print 'grbpath: ',grbpath
                print 'jday:   ',jday
                print 'climo:  ',cgrb,cndx
                print 'gfsanl: ',vgrb,vndx
                print 'model:  ',mgrb,mndx

                print 'opds:       ',opds
                print 'gridparams: ',gridparams



            #time /whome/rtfim/diffgb/diffgb -h -t 'ano' -k '4*-1 7 100  500 '
            # -g"255,0,144,25,+20000,0,0,+80000,-2500,0,0,64,0,0,0,0,0,0,0,0,255"
            # -C /lfs2/projects/rtfim/cmean//cmean_1d.19591002
            # -c /lfs2/projects/rtfim/cmean//cmean_1d.19591002.ndx
            # -z '1 20'
            # /lfs2/projects/rtfim/FIMretro2009NewPhys1094b/FIMrun/fim_8_64_120_200910020000/verif/GFS//0927500000000.grib1
            # /lfs2/projects/rtfim/FIMretro2009NewPhys1094b/FIMrun/fim_8_64_120_200910020000/verif/GFS//0927500000000.grib1.ndx
            # fim8_64_120/RUN2/2009092700/fim.2009092700.f120.grb1
            # fim8_64_120/RUN2/2009092700/fim.2009092700.f120.grb1.ndx

            cmd="""%s %s %s %s -C %s -c %s %s %s %s %s"""%(diffgbcmd,opds,zave,gridparams,cgrb,cndx,vgrb,vndx,mgrb,mndx)
            rc=os.popen(cmd).readlines()
            tt=rc[0].split()
            stat=float(tt[len(tt)-2])

            #print 'rc: ',rc,stat
            return(stat)


        if(hasattr(self.FE,'omodel')):
            vmodel=self.FE.omodel
        else:
            vmodel=self.FE.model

        for vtau in vtaus:
            for vvar in vvars:
                for vplev in vplevs:
                    for varea in vareas:
                        stat=rundiffgb(vtau,vvar,vplev,varea)
                        self.verifStats[vmodel,self.dtg,vvar,vplev,varea,vtau]=stat

        kk=self.verifStats.keys()

        for k in kk:
            print 'key: %64s'%(str(k)),'stat: ',self.verifStats[k]



    def parseVerifLog(self,ropt='norun',verb=0):




        # -- instantiate the pyp with the stats
        #

        sV=FimVerif(self.veriFtDir)

        bdir="%s/log/verif"%(self.wfmDir)
        print "bdir: %s"%(bdir)

        nchunks=6
        nper=4
        nhead=1

        logfiles=glob.glob("%s/*%s*log"%(bdir,self.dtg))

        for logfile in logfiles:
            print 'BBB: ',logfile
            if(os.path.exists(logfile)):
                cards=open(logfile).readlines()

            n=0
            curlev=None
            curvar=None
            curfcst=None
            curstr=None
            dostats=1

            while(n < len(cards)):

                card=cards[n][:-1]

                if(verb > 1): print 'CCC: ',n,card
                # -- just yank out what goes into the database
                #

                if(mf.find(card,'str: ')): curstr=card.split()[1]

                if(curstr != None):
                    rc=sV.getStat4Str(curstr)
                    (ovar,plev,tau,area,stat)=rc
                    sV.stats[self.dtg,ovar,plev,area,tau]=stat
                    if(verb): print rc
                    curstr=None

                n=n+1

        sV.putPyp()


## -- original code to parse out lat/lon etc from the output of diffgb

##                 #if(mf.find(card,'var: ')): curvar=card.split()[1]
##                 #if(mf.find(card,'lev: ')): curlev=card.split()[1]
##                 #yyyyif(mf.find(card,'FOUND fcst:')): curfcst=card.split()[2]

##                 if(curvar != None and curfcst != None):
##                     print 'PPPP: ',n,curvar,curfcst,curlev,card

##                     if(dostats):

##                         nb=n+nhead+nper

##                         for k in range(0,nchunks):

##                             #for j in range(0,30):
##                             #    nn=n+k*nper+j
##                             #    card=cards[nn][:-1]
##                             #    print 'KKKK ',k,j,nn,card

##                             ns=nb+k*nper
##                             card=cards[ns][:-1]
##                             strchk=card.split()[0]
##                             #print 'SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS: ',strchk
##                             #if(strchk != 'str:'):
##                             #    curfcst=None
##                             #    n=n+1
##                             #    break
##                             llcard=cards[ns-3]
##                             (lat1,lat2,nx,ny,dlat)=getLatLon(llcard)
##                             print 'PPPP(str): ',ns,card,lat1,lat2,nx,ny,dlat

##                         n=ns-1

##                     else:
##                         n=n+1

##                     #curvar=None
##                     curfcst=None

##                 else:
##                     n=n+1







    def cleanRun(self,doCleanRun=1,ropt='norun'):

        if(doCleanRun <= 2):

            rmFRdirs=['ensics','prep_C','tracker_C','soundings','verif','ncl_C']
            fimKeep=['stdout']
            postKeep=['fim']
            # -- keep grib1 for diffgb verification
            #
            fimgribKeep=['grib2']
            keepdirs=[]

            killpaths=[]

            dirs=glob.glob("%s/*"%(self.sDir))
            for dir in dirs:
                odir=dir.split('/')[-1]
                if(odir in rmFRdirs):
                    killpaths.append(dir)
                else:
                    keepdirs.append(dir)
                    print 'keep: ',dir,odir

            for dir in keepdirs:

                if(mf.find(dir.split('/')[-1],'fim')):
                    fdirs=glob.glob("%s/*"%(dir))
                    for fdir in fdirs:
                        (bdir,base)=os.path.split(fdir)
                        if(base in fimKeep):
                            print 'fffkeep: ',fdir
                        else:
                            killpaths.append(fdir)


                elif(mf.find(dir.split('/')[-1],'post')):
                    pdirs=glob.glob("%s/*"%(dir))
                    for pdir in pdirs:
                        (bdir,base)=os.path.split(pdir)
                        if(base in postKeep):
                            gdirs=glob.glob("%s/*/*"%(pdir))
                            for gdir in gdirs:
                                if(gdir.split('/')[-1] in fimgribKeep):
                                    print 'gggkeep: ',gdir
                                else:
                                    killpaths.append(gdir)
                        else:
                            killpaths.append(pdir)


            for kpath in killpaths:

                if(os.path.isdir(kpath)):
                    cmd="rm -f -r %s"%(kpath)
                else:
                    cmd="rm -f %s"%(kpath)

                mf.runcmd(cmd,ropt)


        # -- tar and rm
        #
        if(doCleanRun >= 2):

            MF.ChangeDir(self.sRoot)
            MF.ChangeDir('../.')
            mf.runcmd('pwd')
            mf.runcmd('ls -l %s'%(self.expopt))

            ropt='norun'
            ropt=''
            cmd="tar -cvf %s/%s.tar %s"%(mssBaseCleanDir,self.expopt,self.expopt)
            mf.runcmd(cmd,ropt)

            cmd="rm -f -r  %s"%(self.expopt)
            mf.runcmd(cmd,ropt)

            sys.exit()







class FimRunModel2(FimRun):


    def __init__(self,model,dtg,override=0,verb=0,doTT=0):

        from M2 import setModel2

        self.model=model
        self.dtg=dtg
        self.m2=setModel2(model)

        self.curdtg=mf.dtg()
        self.verb=verb
        self.override=override

        self.FE=None

        self.expopt='w2flds'
        self.fimtype=None
        self.comment='FIM g8 (30 km) with GSI'

        self.gribver=self.m2.gribver
        self.sRoot=self.m2.bddir
        self.tRoot=self.m2.bdir2
        self.lRoot=None

        self.fimver=None
        self.glvl=None
        self.nlvl=None
        self.npes=None

        self.fimtype=None

        self.initVars()
        self.initGribPrc()
        self.initSourceTarget()
        if(self.initDataThere() == 0):
            if(verb): print 'NOT FM.initDataThere nnnnnnnnnnnnnnnnnnnnnnn  model: %6s  dtg: %s'%(self.model,self.dtg)
            return
        if(self.initTargetDirs(domkdir=0) == 0):
            if(verb): print 'NOT FM.initTarget    nnnnnnnnnnnnnnnnnnnnnnn  model: %6s  dtg: %s'%(self.model,self.dtg)
            return

        self.tbase="%s.%s.%s"%(self.model,self.expopt,self.dtg)
        self.tdatbase="%s/%s"%(self.tOutDir,self.tbase)
        self.ctlpath="%s.%s.ctl"%(self.tdatbase,self.gribtype)
        self.ctlpathM2="%s.ctl"%(self.tdatbase)
        self.gmppath="%s.%s.gmp"%(self.tdatbase,self.gribtype)
        self.gmpfile="%s.%s.gmp"%(self.tbase,self.gribtype)

        self.initGribs()

        # -- set maxtau
        self.m2.setMaxtau(dtg)
        self.maxtau=self.m2.maxtau

        # -- init TcTrk class as TT

        if(doTT):
            self.initTT()

        #self.initTrackers()
        #self.initStdOut()
        #self.initPyp()


    def initVars(self):


        self.lasttau=168
        self.btau=0
        self.etau=self.lasttau
        self.dtau=6

        self.reqtaus=range(self.btau,self.etau+1,self.dtau)
        self.iokreqtaus={}
        for tau in self.reqtaus:
            self.iokreqtaus[tau]=0

        self.jday=mf.Dtg2JulianDay(self.dtg)


    def initSourceTarget(self):

        # set up source
        #
        if(self.sRoot != None):

            self.sDir="%s"%(self.sRoot)
            self.sGribDir="%s/%s"%(self.sDir,self.dtg)
            self.sTrackerDir=None
            self.sOutDir=None

            self.sAdeckPath=None
            self.sTrackerGribPath=None
            hh=self.dtg[8:10]

            self.gmask="%s/%s.%s.f???.%s"%(self.sGribDir,self.model,self.dtg,self.m2.gribtype)

            # for consistency with rtfim runs set tDirNotag and tDir to tDirNotag -> tOutDir
            #
            self.tDirNotag="%s/%s/dat/%s/%s"%(self.tRoot,self.expopt,self.model,self.dtg)
            self.tDir=self.tDirNotag


    def initDataThere(self):

        #eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
        # check if source and targt dir...
        #
        self.sdatathere=self.tdatathere=self.datathere=1
        if(not(mf.ChkDir(self.sDir,diropt='quiet'))): self.sdatathere=0
        if(not(mf.ChkDir(self.tDir,diropt='quiet'))): self.tdatathere=0

        # bail if source processing not there...for w2flds...
        #
        sdirchk="%s/%s"%(self.sDir,self.dtg)
        self.sdatathere=mf.ChkDir(sdirchk,diropt='quiet')

        if( not(self.sdatathere) and not(self.tdatathere) ):
            return(0)

        # now check if any data there
        if(len(glob.glob(self.gmask)) == 0): self.sdatathere=0


        # check if both s and t data dirs there ... always do gribver=1 if on wjet, so by the time
        # we want to do the grib, the t dir should be there...
        #
        if( self.sdatathere == 0 and self.tdatathere == 0 ):
            self.datathere=0
            if(w2.onWjet or w2.onZeus):
                if(self.verb): print 'EEE source dir: ',self.sDir,' and tdir: ',self.tDir,' not there, sayoonara'
                return(0)



    def initGribs(self):

        self.grbtaus=None

        #gggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggg
        # grib files
        #
        if(self.sRoot != None):
            gpaths=glob.glob(self.gmask)

            taus=[]
            for gpath in gpaths:

                (dir,file)=os.path.split(gpath)
                tau=self.GetTauGrib1File(file)
                taus.append(tau)

                tpath="%s/%s.%s.f%03d.%s"%(self.tOutDir,self.model,self.dtg,tau,self.gribtype)
                if(not( os.path.exists(tpath) or os.path.islink(tpath) ) or self.override > 1 and self.override != 3):
                    cmd="ln -f -s %s %s"%(gpath,tpath)
                    mf.runcmd(cmd)

                if(tau in self.reqtaus):
                    self.iokreqtaus[tau]=1


            taus=mf.uniq(taus)
            taus.sort()

            self.gribtaus=taus



    def GetTauGrib1File(self,file):
        tau=file.split('.')[-2][1:]
        tau=int(tau)
        return(tau)


class FimRunModel2Short(FimRunModel2):


    def __init__(self,model,dtg,override=0,verb=0):

        from M2 import setModel2

        self.model=model
        self.dtg=dtg
        self.m2=setModel2(model)

        self.curdtg=mf.dtg()
        self.verb=verb
        self.override=override

        self.FE=None

        self.expopt='w2flds'
        self.fimtype=None
        self.comment='FIM g8 (30 km) with GSI'

        self.gribver=self.m2.gribver
        self.sRoot=self.m2.bddir
        self.tRoot=self.m2.bdir2
        self.lRoot=None

        self.fimver=None
        self.glvl=None
        self.nlvl=None
        self.npes=None

        self.fimtype=None

        self.initVars()
        self.initGribPrc()
        self.initSourceTarget()
        if(self.initDataThere() == 0):
            if(verb): print 'NOT FM.initDataThere nnnnnnnnnnnnnnnnnnnnnnn  model: %6s  dtg: %s'%(self.model,self.dtg)
            return
        if(self.initTargetDirs(domkdir=0) == 0):
            if(verb): print 'NOT FM.initTarget    nnnnnnnnnnnnnnnnnnnnnnn  model: %6s  dtg: %s'%(self.model,self.dtg)
            return

        self.tbase="%s.%s.%s"%(self.model,self.expopt,self.dtg)
        self.tdatbase="%s/%s"%(self.tOutDir,self.tbase)
        self.ctlpath="%s.%s.ctl"%(self.tdatbase,self.gribtype)
        self.ctlpathM2="%s.ctl"%(self.tdatbase)
        self.gmppath="%s.%s.gmp"%(self.tdatbase,self.gribtype)
        self.gmpfile="%s.%s.gmp"%(self.tbase,self.gribtype)
        self.m2.setMaxtau(dtg)
        self.maxtau=self.m2.maxtau

        self.LsGrib(lsopt=0)




class SetPlotXY(MFbase):


    def hash2xy(self,hash):

        import numpy

        xl=[]
        yl=[]
        kk=hash.keys()
        kk.sort()
        for k in kk:
            xl.append(k)
            yl.append(hash[k])

        x=numpy.array(xl)
        y=numpy.array(yl)

        return(x,y)


    def __init__(self,F,gvar):

        #
        # get data/info from FimRun (F) object
        #

        if(hasattr(F,'stdout')):
            hash=F.stdout.TS[gvar]
            dx=F.stdout.timestep
            ixunits=F.stdout.timestepunits

        else:
            hash=F.TS[gvar]
            dx=F.timestep
            ixunits=F.timestepunits

        if(mf.find(ixunits,'sec')):
            xfact=dx/3600.0
            self.xunits='h'
        else:
            xfact=1.0


        (x,y)=self.hash2xy(hash)

        x=x*xfact

        self.x=x
        self.y=y
        self.np=len(x)
        self.dx=dx




class PlotXYs(MFbase):

    import w2colors as W2C

    cols=[]
    namecols=['red','navy','gold','black','green','purple']

    for ncol in namecols:
        cols.append(W2C.Color2Hex[ncol])

    lstys=[]
    lstys.append('-')
    lstys.append('-')
    lstys.append('--')
    lstys.append(':')
    lstys.append('-.')
    lstys.append('-')

    lwids=[]

    lwids.append(2.0)
    lwids.append(1.0)
    lwids.append(2.0)
    lwids.append(1.0)
    lwids.append(2.0)
    lwids.append(1.0)

    def __init__(self,XYs):


        import numpy
        yss=[]
        xss=[]
        zeros=[]

        for XY in XYs:

            xss.append(XY.x)
            yss.append(XY.y)
            zeros.append(numpy.zeros(XY.np))

        self.yss=yss
        self.xss=xss
        self.zeros=zeros
        self.xunits=XYs[0].xunits


    def pdiff(self):

        oyss=[]
        oxss=[]
        ny=len(self.yss)
        if(ny>1):

            ymean=self.zeros
            for n in range(0,ny):
                ymean=ymean+self.yss[n]

            ymean=ymean/ny

            for n in range(1,ny):
                ydiff=self.yss[n] - self.yss[n-1]
                ymean=(self.yss[n] + self.yss[n-1])*0.5
                pdiff=(ydiff/ymean)*100.0
                oyss.append(pdiff)
                oxss.append(self.xss[n-1])

                for i in range(0,len(pdiff)):
                    print 'i ',i,pdiff[i]

            self.yss=oyss
            self.xss=oxss
            self.t2='Percent Difference from Mean of'






    def plot(self,pngpath=None,doshow=0,
             yb=None,
             ye=None,
             ):

        def setxlab(xunits):
            if(xunits == 'h'):
                xlab="time [%s]"%(xunits)
            else:
                xlab=''
            return(xlab)


        MF.sTimer('pylab')
        from matplotlib import pylab
        import pylab as P
        from numpy import arange
        MF.dTimer('pylab')

        Params = {
            'axes.labelsize': 12,
            'text.fontsize': 12,
            'legend.fontsize': 14,
            'xtick.labelsize': 12,
            'ytick.labelsize': 12,
        }



        try:
            t1=self.t1
        except:
            t1=''

        try:
            t2=self.t2
        except:
            t2=''

        P.rcParams.update(Params)

        xydim=(10.5,8.25)
        F=P.figure(figsize=xydim)

        leftsubplot=0.10
        bottomsubplot=0.15

        F.subplots_adjust(top=0.9,bottom=bottomsubplot,left=leftsubplot,right=0.95,wspace=0.0,hspace=0.0)

        FP=F.add_subplot(111)

        xmaxA=-1e20
        xminA=1e20

        for n in range(0,len(self.yss)):
            ys=self.yss[n]
            xs=self.xss[n]
            ymax=ys.max()
            ymin=ys.min()
            xmax=xs.max()
            xmin=xs.min()
            xmaxA=max(xmax,xmaxA)
            xminA=min(ymin,xminA)

        dx=24.0
        xb=0.0
        xe=xmaxA
        xts=arange(xb,xe,dx)

        nyss=len(self.yss)

        ys1=None
        if(nyss == 3):
            ys0=self.yss[1]
            ys1=self.yss[2]

        self.lwids[2]=0
        self.lwids[1]=2.0

        for n in range(0,len(self.yss)):

            ys=self.yss[n]
            xs=self.xss[n]

            rc=FP.plot(xs,ys,
                       color=self.cols[n],
                       linestyle=self.lstys[n],
                       marker='',
                       linewidth=self.lwids[n],
                       alpha=1.0,
                       )

        if(yb != None and ye != None):
            P.ylim(yb,ye)

        if(ys1 != None):
            P.fill_between(xs, ys0, ys1, where=ys1>=ys0,  facecolor='red', alpha=0.5,linewidth=0)
            P.fill_between(xs, ys0, ys1, where=ys1<=ys0,  facecolor='blue', alpha=0.5,linewidth=0)

        P.xlim(xb,xe)
        P.xticks(xts)

        xlab=setxlab(self.xunits)
        P.xlabel(xlab)

        if(len(t1)>0):
            P.suptitle(t1,fontsize=14)
        if(len(t2)>0):
            P.title(t2,size=11)

        P.grid(True)



        if(pngpath != None):
            P.savefig(pngpath)
            print 'PlotXYs pngpath: ',pngpath

        if(doshow):
            P.show()
            print 'PlotXYs do show'



class PlotMaps():

    def __init__(self,F1,F2=None,xgrads='grads',window=0,opt=None):

        self.F1=F1
        self.F2=F2

        import grads
        if(opt != None):
            ga=grads.GaNum(Bin=xgrads,Opts=opt,Window=window)
        else:
            ga.grads.GaNum(Bin=xgrads,Window=window)

        print F1.ctlpath
        ga.open(F1.ctlpath)
        if(F2 != None):
            print F2.ctlpath
            ga.open(F2.ctlpath)


        self.ga=ga


    #    ga('q files')
    #    ga('set xsize 1600 1200')
    #    ga('set x 1')
    #    ga('set y 1')
    #    ga('set t 1 last')
    #    ga('p1=aave(prc.1-prc.2,lon=0,lon=360,lat=-20,lat=20)')
    #    ga('d p1')
    #    ga('q pos')



if (__name__ == "__main__"):

    rt=rtfimRuns()
    rt.ls()
    sys.exit()



