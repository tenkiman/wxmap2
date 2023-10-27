import os,sys,glob,time,getopt

import mf
import w2
import M2
import FM

from WxMAP2 import W2


class PlotControl(W2):
    
    prcdir=w2.PrcDirFldanalW2
    cfgdir=w2.PrcCfgBdirW2
    basemapdir=w2.W2BaseDirPlt+'/basemap'

    plotXsize=900
    plotYsize=(3.0/4.0)*plotXsize

    pnam={}

    pnam={
        '1':'500',
        '2':'psl',
        '3':'prp',
        '4':'850',
        '5':'tas',
        '6':'uas',
        '7':'u50',
        '8':'shr',
        '9':'u70',
        '10':'sst',
        '11':'wav',
        '12':'w20',
        '13':'wdl',
        '14':'lmq',
        '15':'mhq',
        '16':'hhq',
        '20':'tmx',
        '21':'tmn',
        '22':'thk',
        '23':'w70',
        '30':'basemap',
        '50':'clm',
        '60':'stg',
        '61':'st2',

        '101':'n850',
        '102':'op06',
        '103':'op12',

        }

    pns=pnam.keys()

    pnum={}

    for pn in pns:
        pnum[pnam[pn]]=pn


    # --- defaults
    
    myname="Dr. Mike Fiorino (michael.fiorino@noaa.gov) ESRL/GSD/AMB, Boulder, CO"

    modelpslsmth=1
    modelukfill=0
    modelbskip=12
    modelvskip=6
    modelvskip2=8
    modelvskipuas=5
    modelstrmdenuas=4
    modelstrmdenua=4
    modelstrmdenua2=5
    modelregridshr=1
    modelregriduas=1
    modelprwsden=4
    modelprwbskip=10
    modelregridprw=1
    modeltitleMyname=myname
    modeltitleAck2="Diagnostics/graphics by " + myname

    ddtgmodel=12


    def __init__(self,model,dtg):

        self.model=model
        self.dtg=dtg

        self.dtgm=mf.dtginc(self.dtg,-self.ddtgmodel)

        # data-------------------------------------
        #
        FE=FM.setFE(self.dtg,self.model)
        FEl=FM.setFE(self.dtg,self.model,troot=FE.lroot)
        FRl=FM.FimRun(FEl)
        self.ctlpathCur=FRl.ctlpath

        FEl.dtg=self.dtgm
        FRl=FM.FimRun(FEl)
        self.ctlpathPrv=FRl.ctlpath

        self.plotdir="%s/plt_%s_%s/%s"%(self.basedir,self.center,self.model,self.dtg)
        self.FRl=FRl

        self.modelrestitle='G8|dx~30km L64'
        self.modeldtau=6
        self.modelgridres='0.5'
        self.modelprvar="""_prvar='pr*4'"""

        self.modelpslvar='psl*0.01'

        self.modeltitleAck1="ESRL FIM courtesy ESRL/GSD/AMB"
        self.modeltitleFullmod="rtfim(%s)"%(FRl.expopt)

        self.datathere=0
        if(self.ctlpathCur != None): self.datathere=1

    

    def setPlots(self,plotopt,tauopt,area='conus',region='midlats',regtype='full'):

        taus=[0,6,12,18,24,30,36,42,48,60,72,84,96,108,120,132,144,156,168]
            
        PlotsMidLatFull="500 prp w20 850 uas psl"
        PlotsMidLatFullTmaxTmin="500 prp w20 850 uas psl tmx tmn"
        PlotsMidLat="500 prp w20"
        PlotsMidLatTmaxTmin="500 prp w20 tmx tmn"
     
        PlotsNhemTropfull="n850 uas shr prp w20 mhq wdl hhq lmq 500 u50 u70 w70 850 psl"
        PlotsShemTropfull="n850 uas shr prp w20 mhq wdl 850"
        PlotsTropMonitor="uas prp shr n850 w20 mhq psl"

        region=self.areaRegion[area]
        
        
        if(plotopt != 'all'):
            self.plots=[plotopt]

        elif(region == 'midlat'):

            if(regtype == 'full'):
                self.plots=PlotsMidLatFull.split()

            elif(regtype == 'full.tmax'):
                self.plots=PlotsMidLatFullTmaxTmin.split()

        elif(region == 'tropics'):
            
            if(regtype == 'nhem'):
                self.plots=PlotsNhemTropfull.split()

            elif(regtype == 'shem'):
                self.plots=PlotsShemTropfull.split()

            elif(regtype == 'monitor'):
                self.plots=PlotsTropMonitor.split()
                
        if(tauopt != 'all'):
            self.taus=[int(tauopt)]
        else:
            self.taus=taus




    def setGsf(self):
        
        self.localvargsf="""
function prvar()
%s
return

function localvar()
_pslvar=\'%s\'
_pslsmth=%d
_ukfill=%d
_bskip=%d
_vskip=%d
_vskip2=%d
_vskipuas=%d
_strmdenuas=%d
_strmdenua=%d
_strmdenua2=%d
_regridshr=%d
_regriduas=%d
_prwsden=%d
_prwbskip=%d
_regridprw=%d
return

"""%(
            self.modelprvar,
            self.modelpslvar,
            self.modelpslsmth,
            self.modelukfill,
            self.modelbskip,
            self.modelvskip,
            self.modelvskip2,
            self.modelvskipuas,
            self.modelstrmdenuas,
            self.modelstrmdenua,
            self.modelstrmdenua2,
            self.modelregridshr,
            self.modelregriduas,
            self.modelprwsden,
            self.modelprwbskip,
            self.modelregridprw,
            )    
        self.modtitlegsf="""
function modtitle()
ttau=_tau*1.0
tres='`2%s`3.`0 Fields`0'
'set strsiz 0.14'
'draw string 0.2 8.30 %s (%s)  '_bdtg' run 'tres' `3t`0 = 'ttau' h'
return"""%(self.modelgridres,self.modeltitleFullmod,self.modelrestitle)



class Model2PlotControl(PlotControl):

    def __init__(self,model,dtg,ddtgmodel=12,dmodelType='w2flds'):

        m=M2.setModel2(model)
        
        self.model=model
        self.dtg=dtg
        self.ddtgmodel=ddtgmodel

        dtgm=mf.dtginc(dtg,-self.ddtgmodel)

        self.center=m.center

        if(dmodelType == 'w2flds'):
            m.bddir="%s/%s/dat/%s"%(w2.Nwp2DataBdir,dmodelType,model)
            m.dmodel="%s.%s"%(model,dmodelType)
                
        m.DataPath(dtg)
        if(len(m.dpaths) > 0):
            self.ctlpathCur=m.dpaths[0]
        else:
            self.ctlpathCur=None

        m.DataPath(dtgm)
        if(len(m.dpaths) > 0):
            self.ctlpathPrv=m.dpaths[0]
        else:
            self.ctlpathPrv=self.ctlpathCur

        self.plotdir="%s/plt_%s_%s/%s"%(self.basedir,self.center,self.model,self.dtg)

        self.modelrestitle=m.modelrestitle
        self.modeldtau=m.modeldtau
        self.modelgridres=m.modelgridres

        if(self.ddtgmodel == 12 and hasattr(m,'modelprvar12')):
            self.modelprvar=m.modelprvar12
        else:
            self.modelprvar=m.modelprvar
        self.modelpslvar=m.modelpslvar
        
        self.modeltitleAck1=m.modeltitleAck1
        self.modeltitleFullmod=m.modeltitleFullmod

        self.datathere=0
        if(self.ctlpathCur != None): self.datathere=1
    

def CmdLine():

    __doc__="""%s

purpose:

usages:

  %s bdtg[.edtg[.ddtg]] model -p 'all'|plot -t 'all'|tau -O
  %s cur-24.cur-6 all -O   -- redo all plots for a dtgrange, overwrite
  %s cur-6 gfs -a europe -p basemap  :: make basemap for europe
models:
  ecm | ngp | gfs | ukm | cmc | all

-N  -- norun
-O  -- override=1 (force plot)
-I  -- interact
-T  -- test (no rm of .gs)
-A  0|1|2 doarchive=int(a) ; make plots in /w21/weba
    1 -- use /dat/nwp2/w2flds (i.e., for gfs2 and fim8 if data not on /public)
    2 -- use /dat/nwp2

-F :: dow2flds=1 :: use wgrib filtered fields

-c ctltype  :: ctltype = 'mand' | 'pr' | 'hl'

examples:

 %s cur-12 ngp -t 0 -a tropsio -p prp -O -I  | interactively create tau0 prp plot for tropsio and overwrite (-O disable exist check)
 
(c) 2006-2010 Michael Fiorino, NOAA ESRL
"""

    curdtg=mf.dtg()
    curphr=mf.dtg('phr')
    curyear=curdtg[0:4]
    curtime=mf.dtg('curtime')
    curdir=os.getcwd()
    pypath=sys.argv[0]
    (pydir,pyfile)=os.path.split(pypath)

    #
    #  defaults
    #
    ropt=''
    verb=0

    plotopt='all'
    tauopt='all'
    areaopt='all'

    override=0
    interact=0
    dotest=0
    dow2flds=0
    #
    # use the mandatory level version
    #
    ctltype='mand'
    docleanplt=0
    doarchive=0

    narg=len(sys.argv)-1

    if(narg >= 2):

        dtgopt=sys.argv[1]
        modelopt=sys.argv[2]

        try:
            (opts, args) = getopt.getopt(sys.argv[3:], "m:a:p:t:DNVGOITFkRc:CA:")

        except getopt.GetoptError:
            mf.usage(__doc__,pyfile,curdtg,curtime,curphr)
            sys.exit(2)

        for o, a in opts:
            if o in ("-a",""): areaopt=a
            if o in ("-p",""): plotopt=a
            if o in ("-t",""): tauopt=a
            if o in ("-N",""): ropt='norun'
            if o in ("-F",""): dow2flds=1
            if o in ("-V",""): verb=1
            if o in ("-O",""): override=1
            if o in ("-G",""): dogribmap=1
            if o in ("-I",""): interact=1
            if o in ("-T",""): dotest=1
            if o in ("-c",""): ctltype=a
            if o in ("-C",""): docleanplt=1
            if o in ("-A",""): doarchive=int(a)

    else:
        mf.usage(__doc__,pyfile,curdtg,curtime,curphr)
        sys.exit(1)

    rc={}
    for d in dir():
        if(not(mf.find(d,'__'))):
            rc[d]=eval(d)

    rc=(
        opts,curdtg,curphr,curyear,curtime,curdir,pypath,pydir,pyfile,ropt,verb,override,
        dtgopt,modelopt,
        plotopt,tauopt, areaopt,interact,dotest,dow2flds,
        ctltype,docleanplt,doarchive,
        )

    return(rc)

    


