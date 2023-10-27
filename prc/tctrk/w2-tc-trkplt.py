#!/usr/bin/env python

diag=0
if(diag):
    from M import MFutils
    mf2=MFutils()
    mf2.sTimer('w2')

from tcbase import *

from ga2 import setGA
from M2 import setModel2
from ATCF import AidProp
from vdVM import getVdDss
if(diag): mf2.dTimer('w2')

class TcIntensityPlot(MFbase):
    
    modelDtgs={}
    modelColor={}
    
    def __init__(self,
                 models,
                 verb=0,
                 ):

        nmodels=[]
        for model in models:
            nmodel=model.split('.')[0]
            nmodels.append(nmodel)
            self.modelDtgs[nmodel]=[]
            
        self.models=nmodels
        self.verb=verb
        
    def addModel(self,model,dtg,btcolor,ftcolor):
        
        MF.appendDictList(self.modelDtgs,model,dtg)
        self.modelColor[model,dtg]=(btcolor,ftcolor)
        
    def makeTcIntensityPlotOfileGs(self,
                                   ):
        
        gs=''
        
        nmodel=0
        for model in self.models:
            for dtg in self.modelDtgs[model]:
                gs=gs+"""
mfile=vmdir'fcvmax.'%s'.'stmid'.'%s'.ctl'
f%d=ofile(mfile)
"""%(model,dtg,nmodel)
                nmodel=nmodel+1            
                
        return(gs)

        
    def makeTcIntensityPlotGs(self,
                              digsiz=0.03,
                              cmark=3,
                              ):
        
        gs=''
        nmodel=0
        for model in self.models:
            for dtg in self.modelDtgs[model]:
                (btcol,ftcol)=self.modelColor[model,dtg]
                gs=gs+"""

# -- first check if there are intensity forecasts
#

'fm=fvm.'f%d
rc=datachk(fm)

if(rc != -999)

'set ccolor %d'
'set cstyle 1'
'set cthick 4'
'set cmark %d'
'set digsiz 0'
'd fm'

'set ccolor %d'
'set cstyle 0'
'set cthick 0'
'set cmark 3'
'set digsiz %5.3f'
'd fm'

endif

"""%(nmodel,ftcol,cmark,btcol,digsiz)
                        
                nmodel=nmodel+1
    
        return(gs)
        
    

class AidPropLocal(MFbase):

    def __init__(self,
                 aid,
                 label=None,
                 color=None,
                 year=2011,
                 doMFTMlabels=0,
                 ):

        oname=aid
        mark='d'
        color=None
        label=None

        if(doMFTMlabels):
            
            if(len(aid) == 5 and aid[0] == 'm'):
                aP=AidProp(aid[1:])
                if(aP.label != None):
                    label="%s ; MF tracker V1.1"%(aP.label)
                    color=aP.color
                    color='purple'
    
                else:
                    label="MF tracker V1.1"
                    color='purple'
    
            elif(len(aid) == 5 and aid[0] == 't'):
                aP=AidProp(aid[1:])
                if(aP.label != None):
                    label="%s ; TM tracker"%(aP.label)
                    color=aP.color
                    color='navy'
                else:
                    label="TM tracker"
                    color='navy'
            
        aPbase=AidProp(aid)
        gotbase=aPbase.gotbase
        gotpost=aPbase.gotpost
 
        # -- see if the root aid has a specific setting
        if(gotbase):
            label=aPbase.label
            color=aPbase.color

        self.label=label
        self.color=color
        self.oname=oname
        self.mark=mark



class TcBtFtTrkPlot(DataSet,TcAidTrk):

    from w2base import w2Colors
    wC=w2Colors()

    def __init__(self,stmid,finalstmid,models,dtgs,
                 tD=None,
                 dbtype=None,
                 dsbdir=None,
                 pltdir=None,
                 aidtrk=None,
                 aidtaus=None,
                 zoomfact=None,
                 centerdtg=None,
                 useReftrk=0,
                 dtgopt=None,
                 ttaus=None,
                 otau=48,
                 Quiet=1,
                 Window=0,
                 doLogger=0,
                 Bin='grads',
                 dobt=2,  # combines BT + 9X in getDSsFullStm
                 dols=0,
                 doft=0,
                 doerr=0,
                 pcolMaxChar=8,
                 #landcol='sienna',
                 #oceancol='steelblue',
                 landcol='tan',
                 oceancol='lightblue',
                 background='black',
                 backgroundColor=0,
                 mktaus=None,
                 maxtau=168,
                 xsize=1024,
                 ysize=None,
                 verb=0,
                 labeltag=None,
                 doland=0,
                 dolandFC=0,
                 docycle=0,
                 maxlandFrac=0.8,
                 cur12dtg=None,
                 doFOF=0,
                 override=0):

        MF.sTimer('TcBtFtTrkPlot-INIT')
        # -- get TC info and best track
        #
        if(tD == None):
            tD=TcData(stmopt=stmid)

        #if(model != 'bt' and w2.IsModel2(model)): m2=setModel2(model)
        #self.m2=m2

        # -- get the cur12-12 dtg for labeling plots
        #
        if(cur12dtg == None):
            cur12dtgs=mf.dtg_dtgopt_prc('cur12-12')
            cur12dtg=cur12dtgs[0]
            
        self.cur12dtg=cur12dtg
        self.doFOF=doFOF
        
        self.tD=tD

        self.models=models
        self.dtgs=dtgs
        self.dbtype=dbtype
        self.dsbdir=dsbdir
        
        rc=getStmParams(stmid)
        stmyear=rc[2]
        stmdir=rc[0]+rc[1].upper()
        
        if(pltdir == None):
            pltdir="%s/tctrkveriDAT/%s/%s/%s"%(w2.HfipProducts,stmyear,stmdir,self.cur12dtg)
        
        self.doft=1
        if(len(models) == 1 and models[0] == 'bt'): self.doft=0

        self.doerr=doerr
        self.pcolMaxChar=pcolMaxChar
        
        self.stmid=stmid
        self.finalstmid=finalstmid
        self.stmdtg=dtgs[0]
        MF.ChkDir(pltdir,'mk')
        self.pltdir=pltdir
        
        # -- internal fof dir
        #
        if(self.doFOF):
            pltFOFdir="%s/%s"%(stmdir,self.cur12dtg)
            self.pltFOFdir=pltFOFdir

        self.aidtrk=aidtrk
        self.aidtaus=aidtaus
        self.zoomfact=zoomfact
        self.otau=otau
        
        self.useReftrk=useReftrk
        
        if(ttaus == None):
            self.targetTaus=range(0,120+1,6)+range(132,maxtau+1,12)
        else:
            self.targetTaus=ttaus

        self.doft=doft
        
        self.verb=verb
        self.override=override
        self.labeltag=labeltag
        
        self.landcol=landcol
        self.oceancol=oceancol
        self.backgroundColor=backgroundColor
        
        self.maxtau=maxtau
        
        self.doland=doland
        self.dolandFC=dolandFC
        self.docycle=docycle
        self.maxlandFrac=maxlandFrac
        
        self.xsize=xsize
        if(ysize != None):
            self.ysize=ysize
        else:
            self.ysize=self.xsize*(3.0/4.0)

        self.Quiet=Quiet
        self.Window=Window
        self.doLogger=doLogger
        self.Bin=Bin

        self.plotDone=0

        # -- set the AD2ss and VD2 to only call once
        #
        self.AD2ss=None
        self.vD2=None
        self.ga=None
        self.ge=None
        
        if(dtgopt != None):
            self.dtgs=mf.dtg_dtgopt_prc(dtgopt)

        # -- new logic for center dtg
        #
        self.centerdtg=centerdtg
        
        # -- not sure we want to do this: if(centerdtg == None): self.centerdtg=mf.dtg_dtgopt_prc(dtgopt)[0]


        try:
            self.BT=tD.makeBestTrk2(stmid,dobt=dobt)
            self.btrk=self.BT.btrk
        except:
            print 'WWWWWWWWWWW no bt for stmid: ',stmid
            return

        
        (self.stm3id,self.stmname)=tD.getStmName3id(self.finalstmid)
        self.stmname=tD.getStmNameMD2(self.finalstmid)
        
        # -- if ls return
        #
        if(dols):
            return

        self.setLatLonBounds()

        (clat1,clon1)=Rlatlon2Clatlon(self.lat1,self.lon1,dozero=1,dotens=0)
        (clat2,clon2)=Rlatlon2Clatlon(self.lat2,self.lon2,dozero=1,dotens=0)

        # -- calc title and file labels
        #
        
        psources=[]
        pmodels=[]
        nmodels=len(models)

        for model in models:
            mm=model.split('.')
            if(len(mm) > 1):
                pmodel=mm[0]
                pmodels.append(pmodel)
                psource=mm[1]
                psources.append(psource)
            else:
                pmodel=mm[0]
                pmodels.append(pmodel)
                psource='ad2'
                psources.append(psource)

        if(nmodels > 1):

            for pmodel in pmodels:
                
                (pcolor,plabel)=self.getAidColorLabel(pmodel)
                # -- limit color name to 10 char
                tpcolor=pcolor[0:self.pcolMaxChar]

                if(pmodels.index(pmodel) == 0):
                    modTitle="%s(%s)"%(pmodel.upper(),tpcolor)
                    #modKey="%s=%s"%(pmodel.upper(),plabel.split('-')[1].strip())
                    modKey="%s={%s}"%(pmodel.upper(),plabel)
                    modLabel=pmodel
                else:
                    modTitle="%s, %s(%s)"%(modTitle,pmodel.upper(),tpcolor)
                    modLabel="%s-%s"%(modLabel,pmodel)
                    #modKey="%s ; %s=%s"%(modKey,pmodel.upper(),plabel.split('-')[1].strip())
                    modKey="%s ; %s={%s}"%(modKey,pmodel.upper(),plabel)

            for psource in psources:
                if(psources.index(psource) == 0):
                    #srcTitle="%s(%s)"%(psource,pcolor)
                    srcTitle=psource
                    srcLabel=psource
                else:
                    #srcTitle="%s, %s(%s)"%(srcTitle,psource,pcolor)
                    srcTitle="%s, %s"%(srcTitle,psource)
                    srcLabel="%s-%s"%(srcLabel,psource)
                

        else:

            
            (pcolor,plabel)=self.getAidColorLabel(pmodels[0])

            # -- limit color name to 10 char
            tpcolor=pcolor[0:self.pcolMaxChar]

            modTitle="%s(%s)"%(pmodel.upper(),tpcolor)
            modKey="%s={ %s }"%(pmodel.upper(),plabel.split('-')[-1].strip())
            modLabel=pmodel
            srcTitle=psource
            srcLabel=psource
            
        self.modTitle=modTitle
        self.srcTitle=srcTitle
        self.modKey=modKey

        self.modLabel=modLabel
        self.srcLabel=srcLabel

        if(len(dtgs) > 1):
            self.dtgLabel="%s-%s"%(dtgs[0],dtgs[-1])
        else:
            self.dtgLabel=dtgs[0]
            
        # file of files for hanis
        #
        if(self.docycle and self.doFOF):
            self.FOFfile="fof-%s.txt"%(self.modLabel)
            self.FOFpath="%s/%s"%(self.pltdir,self.FOFfile)
            FF=open(self.FOFpath, mode='a')
            #else:
            #    print 'III-FOF:          %s already exists...press...'%(self.FOFpath)
                
        
        clatLabel="%s.%s-%s.%s"%(clat1,clat2,clon1,clon2)
        if(self.zoomfact == None): clatLabel='UNZOOM'
        
        if(self.doft):
            self.pltfile="trkplt-%s-%s-%s-%s-M%03d.png"%(self.dtgLabel,self.modLabel,
                                                         self.srcLabel,self.dtgLabel,clatLabel,maxtau)
        else:
            self.pltfile="trkplt-%s-%s-%s-M%03d.png"%(self.dtgLabel,self.modLabel,
                                                      clatLabel,maxtau)

        if(self.doerr != -999):
            
            if(self.doerr > 0):
                self.pltfile="err-%03d.%s"%(self.doerr,self.pltfile)
            else:
                self.pltfile="err-%03d.%s"%(-1* self.doerr,self.pltfile)
                

        self.pltpath="%s/%s"%(self.pltdir,self.pltfile)
        print 'PPPPP: ',self.pltpath
        self.trkplotpath=self.pltpath
        
        if(self.doFOF):
            odtg=mf.dtg2gtime(dtgs[0])
            odtg=odtg[0:3]+ ' ' + odtg[3:-4]+ ' ' + odtg[-4:]
            FF.writelines('''%s/%s "%s"\n'''%(self.pltFOFdir,self.pltfile,odtg))
            FF.close()
        
        if(not(override) and MF.ChkPath(self.trkplotpath)):
            print 'III-trkplotpath: ',self.trkplotpath,' already there and override=0...'
            self.plotDone=1
            #MF.dTimer('TcBtFtTrkPlot-INIT')
            return

        if(mktaus == None):
            self.mktaus=[0,24,48,72,120,144,168,192,216,240]
            self.mkcols={0:1,24:1,48:1,72:2,96:2,120:2,144:3,168:4,192:3,216:4,240:5}
        else:
            self.mktaus=mktaus
            
        MF.dTimer('TcBtFtTrkPlot-INIT')


    def getAidColorLabel(self,model):

        apl=AidPropLocal(model)

        if(apl.color != None):
            pcolor=apl.color
        else:
            ap=AidProp(model)
            pcolor=ap.color

        if(apl.label != None):
            plabel=apl.label
        else:
            plabel=ap.label

        return(pcolor,plabel)


    def setLatLonBounds(self,ndayBack=2):

        alats=[]
        alons=[]
        avmaxs=[]
        apmins=[]
        
        dtgs=self.btrk.keys()
        dtgs.sort()

        backdtg=mf.dtginc(self.stmdtg,-ndayBack*24)

        for dtg in dtgs:
            bt=self.btrk[dtg]
            bddtg=mf.dtgdiff(backdtg,dtg)
            
            # -- skip dtgs <= ndayBack
            #
            if(bddtg <= 0.0): continue
            
            alats.append(bt[0])
            alons.append(bt[1])
            avmaxs.append(bt[2])
            apmins.append(bt[3])

        self.alats=alats
        self.alons=alons
        self.avmaxs=avmaxs
        self.apmins=apmins

        if(len(alats) == 0):
            
            print 'EEE-no BT for stmid: ',self.stmid,' dtgs: ',self.dtgs,' sayounara'
            if(Is9X(self.stmid)):
                print 'EEE -- maybe wrong 9X?'
            sys.exit()
        
        if(self.useReftrk):
            MF.sTimer('reftrk')
            rc=GetOpsRefTrk(self.stmdtg,self.finalstmid,verb=verb)
            alats=rc[0]
            alons=rc[1]
            MF.dTimer('reftrk')
            
        (lat1,lat2,lon1,lon2)=LatLonOpsPlotBounds(alats,alons,verb=verb)

        if(self.centerdtg != None and (self.centerdtg in dtgs) ):
            bt=self.btrk[self.centerdtg]
            rlat=bt[0]
            rlon=bt[1]
        else:
            rlat=(lat1+lat2)*0.5
            rlon=(lon1+lon2)*0.5

            from numpy import mean
            rlat=mean(alats)
            rlon=mean(alons)


        if(self.zoomfact != None):

            tt=self.zoomfact.split(',')
            
            if(len(tt) == 4):
                # -- set lat/lon box explicitly
                #
                lat1=float(tt[0])
                lon1=float(tt[1])
                lat2=float(tt[2])
                lon2=float(tt[3])
                # -- check cross of prime meridian -- 18L.2019
                #
                cross0W=0
                isShem=0
                if(lat1 < 0.0 and lat2 < 0.0): isShem=1
                if(lon1 < 0.0 and lon2 > 0.0): cross0W=1
                
                # -- check of converting to degree E
                #
                cnv1=0
                cnv2=0
                if(lon1 < 0.): 
                    cnv1=1
                    lon1=360.0+lon1
                if(lon2 <= 0.): 
                    cnv2=1
                    lon2=360.0+lon2
                
                # -- case of crossing...put all in deg E
                #
                if(cross0W and cnv1):
                    lon2=360.0+lon2

                # -- check if lon1|2 are increasing (positive definite?)
                #
                if(lon1 > lon2):
                    print 'EEE-ZZZ lon1 > lon2 for zoomfact: ',self.zoomfact,'lon1: ',lon1,'lon2: ',lon2
                    sys.exit()
                    
            else:

                # -- set lat/lon box
                #
                zoom=float(self.zoomfact)
    
                dlon=(lon2-lon1)/zoom
                dlat=(lat2-lat1)/zoom
                dint=2.5
    
                
                if(self.centerdtg == None and zoom < 1.25):
                    latOff=0.65
                    if(IsNhemBasin(self.finalstmid)): latOff=0.35
                else:
                    latOff=0.50
                    
                lonOff=0.50
                
                lat1=int(lat1/dint+0.5)*dint
                lat2=lat1+dlat
    
                lon1=rlon-dlon*lonOff
                lon1=int(lon1/dint+0.5)*dint
                lon2=lon1+dlon
                #sys.exit()

        aspect=(lat2-lat1)/(lon2-lon1)
    
        self.lat1=lat1
        self.lat2=lat2
        self.lon1=lon1
        self.lon2=lon2
        
        

    def setTrkPltGA(self):
        
        # -- grads
        #
        if(self.ga == None):
            
            ga=setGA(Quiet=self.Quiet,Window=self.Window,doLogger=self.doLogger,Bin=self.Bin)
            
            dumctl="%s/dum.ctl"%(w2.GradsGslibDir)
            ga.fh=ga.open(dumctl)
        
            self.ga=ga
            self.ge=ga.ge
            
            self.ge.pareaxl=0.50
            self.ge.pareaxr=9.75
            self.ge.pareayb=0.25
            self.ge.pareayt=7.75
            self.ge.setParea()
        
            self.ge.xsize=self.xsize
            self.ge.ysize=self.ysize
            
            self.curgxout=self.ga.getGxout()
            self.setInitialGA()
        


    def setInitialGA(self):

        ga=self.ga
        ge=self.ge

        ge.lat1=self.lat1
        ge.lat2=self.lat2
        ge.lon1=self.lon1
        ge.lon2=self.lon2

        ge.backgroundColor=self.backgroundColor
        
        ge.mapdset='hires'
        #ge.xlint=xlint
        #ge.ylint=ylint
        ge.clear()
        ge.mapcol=0
        ge.setMap()
        ge.grid='off'
        ge.setGrid()
        ge.setLatLon()
        ge.setXylint()
        ge.setParea()
        ge.setPlotScale()
        
    
    def PlotTrkBT(self,tIP,
                dtg0=None,nhbakBT=None,nhforBT=None,doerr=-999,
                ddtg=12,dtg0012=0,maxbt=55,dtau=12):

        MF.sTimer('pbt')
        if(self.ga == None): self.setTrkPltGA()
        
        self.dtg0=dtg0
        
        # -- set vdtg if doerr
        #
        vdtg=None
        if(doerr != -999):
            if(doerr < 0): 
                vdtg=mf.dtginc(dtg0,-doerr)
            else:
                vdtg=mf.dtginc(dtg0,doerr)
                
        
        ga=self.ga
        ge=self.ge
        
        if(dtg0 != None and ddtg == 12 and w2.is0012Z(dtg0)):
            dtg0012=1
        
        #if(dtg0 != None and w2.is0618Z(dtg0) and ddtg == 12):
        #    dtg0012=0
        
        pbt=ga.gp.plotTcBt
        pbt.btcols=[2,1,3,4]*20      # default in ga2.py
        btcols12=[2,1,4,3,12,14]*20  # try something different
        btcols06=[1,2,4,1,3,4,12,3,14,12,2,14,1,2]*20
        
        pbt.btcols=btcols12 
        
        # -- first set for all dtgs
        #
        ddtgAll=6
        dtg0012All=0
        pbt.set(self.btrk,
                dtg0=dtg0,
                nhbak=None,
                nhfor=None,
                ddtg=ddtgAll,
                ddtgbak=ddtgAll,
                ddtgfor=ddtgAll,
                dtg0012=dtg0012All,
                doland=self.doland,
                maxlandFrac=self.maxlandFrac,
                maxbt=999)  # signal to use all bt dtgs
        
        # -- now save the markprop
        #
        #mks=pbt.markprop.keys()
        #mks.sort()
        markPropAll=pbt.markprop
        
        pbt.set(self.btrk,
                dtg0=dtg0,
                nhbak=nhbakBT,
                nhfor=nhforBT,
                ddtg=ddtg,
                ddtgbak=ddtg,
                ddtgfor=ddtg,
                dtg0012=dtg0012,
                doland=self.doland,
                maxlandFrac=self.maxlandFrac,
                maxbt=maxbt)
        

        mks=markPropAll.keys()

        # -- save nhbakBT for plot fc
        #
        self.nhbakBT=nhbakBT

        #mks=pbt.markprop.keys()
        #mks.sort()
        #print 'mmmm-----',dtg0,mks
        pbt.markprop=markPropAll
        
        # -- make grads data file with best track vmax
        #
        pbt.setGradsData(dtg0,tname="btvmax.%s"%(self.stmid))

        bm=ga.gp.basemap2
        bm.set(landcol=self.landcol,oceancol=self.oceancol)
        bm.draw()
        ge.setPlotScale()

        #pbt.dline(times=pbt.owptimesbak,lcol=7,lthk=10)

        btotimes=pbt.otimesbak
        
        
        if(nhforBT != None and nhforBT > 0):
            btotimes=pbt.otimesbak+pbt.otimesfor
            btotimes=mf.uniq(btotimes)

        if(nhforBT == None and vdtg == None):
            btotimes=pbt.otimes

        if(vdtg != None):    
            pbt.otimesfor=[vdtg]
            btotimes=pbt.otimesbak+pbt.otimesfor
            btotimes=mf.uniq(btotimes)
            print '3333',btotimes


        if(vdtg == None):
            pbt.dline(times=btotimes,lcol=0,lsty=1,lthk=6)
            pbt.dwxsym(times=btotimes)
            pbt.legend(ge,times=btotimes,hiTime=dtg0,ystart=7.75)
        else:
            pbt.dline(times=pbt.otimesbak,lcol=0,lsty=1,lthk=6)
            pbt.dwxsym(times=btotimes)
            pbt.legend(ge,times=pbt.otimes,hiTime=dtg0,ystart=7.75)
            
        self.lastdtgBT=btotimes[-1]
        
        for btotime in btotimes:
            try:
                (obtsym,obtsiz,obtcol,obtthk)=pbt.markprop[btotime]
            except:
                continue

        tIP.markprop=pbt.markprop

        self.pbt=pbt
        MF.dTimer('pbt')


    def PlotTrkFC(self,tIP,model,ftdtg=None,
                  otau=48,etau=120,dtau=6,
                  mktaus=None,
                  plotFTwithBT=1,
                  doerr=0):
        """ plot fc track
        """

        oftdtg=ftdtg
        if(ftdtg == None):
            oftdtg='9999999999'
            
        MF.sTimer('pft-%s-%s'%(model,oftdtg))
        (pcolor,plabel)=self.getAidColorLabel(model)

        if(self.ga == None): self.setTrkPltGA()
        ga=self.ga
        ge=self.ge

        self.ftdtg=ftdtg
        
        if(hasattr(self,'lastdtgBT') and ftdtg != None and plotFTwithBT):
            etau=mf.dtgdiff(ftdtg,self.lastdtgBT)
            etau=int(etau)
            if(etau > self.maxtau): etau=self.maxtau
            
        self.etau=etau
        self.dtau=dtau
        self.otau=otau
        
        if(mktaus == None):
            mktaus=self.mktaus
        else:
            mktaus=mktaus

        # -- set the color by the colin in VT.AidProp
        #
        if(hasattr(self,'ftlcol')):
            ftlcol=self.ftlcol+1
        else:
            ftlcol=101
            
        self.ftlcol=ftlcol

        rc=tIP.markprop[ftdtg]
        btlcol=rc[2]
        
        tIP.addModel(model,ftdtg,btlcol,ftlcol)
        
        hex=self.wC.W2Colors[pcolor]
        (r,g,b)=self.wC.hex2rgb(hex)
        lcolrgb='set rgb %d %d %d %d'%(ftlcol,r,g,b)
        ga(lcolrgb)

        (btau,etau,dtau)=(0,etau,dtau)
        itaus=range(btau,etau+1,dtau)

        taus=[]
        for itau in itaus:
            for ttau in self.aidtaus:
                if(itau == ttau):
                    taus.append(itau)

        pft=ga.gp.plotTcFt
        pft.maxlandFrac=self.maxlandFrac
        pft.set(self.aidtrk,lcol=ftlcol,doland=self.dolandFC)

        # -- make grads data file with vmax
        #
        if(hasattr(self.pbt,'platlons0')): platlons0=self.pbt.platlons0
        else:                              platlons0=self.pbt.platlons[self.pbt.otimes[0]]

        if(hasattr(self,'lastdtgBT') and ftdtg != None and plotFTwithBT): 
            self.maxtau=etau
        
        gdftdtg=dtg0
        if(ftdtg != None): gdftdtg=ftdtg
        pft.setGradsData(tdtg=gdftdtg,
                         platlons=platlons0,
                         dttime=self.pbt.dttime,
                         tname="fcvmax.%s.%s"%(model,self.stmid),
                         maxtau=self.maxtau,
                         )
        
        if(ftlcol == -2):
            pft.dline(lcol=15)
            try:     vmcol=pft.lineprop[otau][0]
            except:  None

            if(vmcol != 75):
                pft.dmark(times=[otau],mkcol=vmcol,mksiz=0.20)
                pft.dmark(times=[otau],mksiz=0.05)
            else:
                pft.dmark(times=[otau])
        else:
            ftmkcol=ftlcol
            if(ftdtg != None and (doerr < 0)):
                ftmkcol=self.pbt.markprop[ftdtg][2]

            if(doerr < 0):
                pft.dline(times=taus,lsty=3,lthk=6)
                pft.dmark(times=taus,mksiz=0.040,mkcol=ftmkcol)
                
                # -- special handling of special taus
                #
                for mktau in mktaus:
                    if(mktau in taus):
                        vdtg=mf.dtginc(ftdtg,mktau)
                        
                        try:
                            ftmkcolM=self.pbt.markprop[vdtg][2]
                        except:
                            ftmkcolM=15
                            
                        # -- make tau 72 bigger
                        #
                        if(mktau == 72):
                            pft.dmark(times=[mktau],mkcol=ftmkcolM,mksiz=0.150)
                            pft.dmark(times=[mktau],mkcol=0,mksiz=0.090)
                            pft.dmark(times=[mktau],mkcol=self.mkcols[mktau],mksiz=0.070)
                            
                        else:
                            pft.dmark(times=[mktau],mkcol=ftmkcolM,mksiz=0.100)
                            pft.dmark(times=[mktau],mkcol=0,mksiz=0.060)
                            pft.dmark(times=[mktau],mkcol=self.mkcols[mktau],mksiz=0.040)

        MF.dTimer('pft-%s-%s'%(model,oftdtg))


    def PlotTrkError(self,model,ftdtg=None,
                     otau=48,etau=120,dtau=6,
                     ):

        """ plot fc error for etau
        """


        ga=self.ga
        ge=self.ge

        if(etau != -999 and etau < 0): 
            self.etau=-1*etau
        else:
            self.etau=etau
        
        if(dtau != -999 and dtau > 0):
            self.dtau=-1*dtau
        else:
            self.dtau=dtau
            
        self.otau=self.etau

        mktaus=[self.etau]
        
        (pcolor,plabel)=self.getAidColorLabel(model)


        # -- set the color by the colin in VT.AidProp
        #
        if(hasattr(self,'ftlcol')):
            ftlcol=self.ftlcol
        else:
            ftlcol=101
            
        self.ftlcol=ftlcol

        hex=self.wC.W2Colors[pcolor]
        (r,g,b)=self.wC.hex2rgb(hex)
        lcolrgb='set rgb %d %d %d %d'%(ftlcol,r,g,b)
        ga(lcolrgb)

        (ibtau,ietau,idtau)=(0,self.etau,self.dtau)
        itaus=range(ibtau,ietau+1,idtau)
        
        taus=[]
        for itau in itaus:
            for ttau in self.aidtaus:
                if(itau == ttau):
                    taus.append(itau)

        pft=ga.gp.plotTcFt
        vdtg=mf.dtginc(ftdtg,ietau)
        
        if(self.aidFEs[ietau] < 0):
            print 'WWW(TcBtFtTrkPlot.PlotTrkError): veri BT not at TC...press'
            return
        
        try:
            aidposit=self.aidtrk[ietau][0:4]
        except:
            print 'WWW no aid for etau: ',ietau
            return
        
        try:
            veriposit=self.btrk[vdtg][0:4]
        except:
            print 'WWW no bt for vdtg: ',vdtg
            return
        
        taus=[ietau-idtau,ietau]

        self.errtrk={
            ietau:aidposit,
            ietau-idtau:veriposit
            }

        pft.set(self.errtrk,lcol=ftlcol,doland=self.dolandFC)
        pft.dline(times=taus,lsty=3)

        ftmkcol=ftlcol
        if(ftdtg != None): ftmkcol=self.pbt.markprop[ftdtg][2]
        
        for mktau in mktaus:
            if(mktau in taus):
                pft.dmark(times=[mktau],mkcol=ftmkcol,mksiz=0.100)
                pft.dmark(times=[mktau],mkcol=0,mksiz=0.070)
                pft.dmark(times=[mktau],mkcol=self.mkcols[mktau],mksiz=0.040)


    

    def PlotTrkTitle(self,models=None,dtgs=None):

        if(models == None):  models=self.models
        if(dtgs == None):    dtgs=self.dtgs
        
        ga=self.ga
        ge=self.ge

        ttl=ga.gp.title
        ttl.set(scale=0.60,t3scale=0.45,t1thk=4,t2thk=4,t3thk=4)
        btvmax=max(self.avmaxs)
        
        ftpostfix=''
        if(self.doft): ftpostfix=self.ftlabel

        if(self.stmdtg != None):
            btvmax=self.btrk[self.stmdtg][2]
        else:
            btvmax=self.stmdss.vmax

        if(self.doerr != -999):
            if(self.doerr > 0): 
                errtau=self.doerr
            else:
                errtau=-1*self.doerr
                
            self.toptitle1='%s %-3d-h Error for TC: %s [%s]  V`bmax`n: %3dkt'%(self.modTitle,errtau,self.finalstmid,self.stmname,btvmax)
        else:
            self.toptitle1='%s %-3d-h Fcst for TC: %s [%s]  V`bmax`n: %3dkt'%(self.modTitle,self.etau,self.finalstmid,self.stmname,btvmax)
        self.toptitle2=''
        if(len(dtgs) > 1):
            self.toptitle2="run dtgs: %s-%s  tracker sources: %s"%(dtgs[0],dtgs[-1],self.srcTitle)
        else:
            veridtg=mf.dtginc(self.stmdtg,self.maxtau)
            self.toptitle2="runDtg: %s %d-h veriDtg: %s tracker source: %s"%(self.stmdtg,self.maxtau,veridtg,self.srcTitle)

        t1=self.toptitle1
        t2=self.toptitle2
        t3=self.modKey
        if(self.labeltag != None): t1="%s `2%s`0"%(t1,self.labeltag)

        ttl.top(t1,t2,t3)

        if(self.Window): ga('q pos')

    def pngPath(self):
        #self.ge.pngmethod='gxyat'
        self.ge.makePng(self.pltpath,background='black',verb=1)


    def xvPlot(self,ropt='',zfact=1.25):

        if(hasattr(self,'ge') and self.ge != None):
            xs=self.ge.xsize
            ys=self.ge.ysize
        else:
            xs=self.xsize
            ys=self.ysize
            
        cmd="xv  -geometry %ix%i+50+50 %s"%(xs*zfact,ys*zfact,self.pltpath)
        #cmd="xv %s"%(self.pltpath)
        MF.runcmd(cmd,ropt)
        
    def pngquantPlot(self,ropt='',nbits=24):
        cmd="pngquant %d --force --output %s %s"%(nbits,self.pltpath,self.pltpath)
        MF.runcmd(cmd,ropt)

    def cpDropbox(self,tdir='~/Dropbox/TC',ropt=''):
        cmd="cp %s %s/."%(self.pltpath,tdir)
        print 'cccccccc ',cmd
        mf.runcmd(cmd,ropt)



    def setTCtracker(self,stmid,dtg,taid=None,adeck=None,source='ad2',aidSource=None,
                     maxtau=168,quiet=0,verb=0,dols=0):

        dsbdir=self.dsbdir
        
        if(adeck != None):
            aD=Adeck(adeck)

            # first aid
            if(not(quiet)): print 'stmid: ',stmid
            try:
                ndx=aD.stm1ids.index(stmid)
                stm2id=aD.stm2ids[ndx]
            except:
                if(not(quiet)): print 'WWW no aidtrk for : ',stmid
                return(0)

            aid=aD.aids[0]
            self.aid=aid
            try:
                self.aidtrk=aD.aidtrks[aid,stm2id][dtg]
            except:
                if(not(quiet)): print """can't find aidtrk for aid,stm2id,dtg: """,aid,stm2id,dtg
                return(0)

            self.aidtaus=aD.aidtaus[aid,stm2id,dtg]
            self.aidtaus=mf.uniq(self.aidtaus)
            self.aidsource=source
            self.aidname=aid

        # -- AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD22222222222222222222222222222222222222
        #
        elif(source == 'ad2'):

            if(taid == None):
                print 'EEE[TcBtFtTrkPlot.setTCtracker()] -- source = adeck2, must set taid=aid in call...sayoonara'
                sys.exit()
                
            tstmids=[stmid]
            stmyear=stmid.split('.')[-1]
            
            if(self.AD2ss == None):
                (AD2ss,bd2s,dbnames,basins,ybears)=getAdeck2Bdeck2DSs(tstmids,dsbdir=dsbdir,verb=0)
                self.AD2ss=AD2ss
                self.bd2s=bd2s
                self.basins=basins
            else:
                AD2ss=self.AD2ss
                bd2s=self.bd2s
                basins=self.basins
            
            key="%s_%s"%(taid,stmid.upper())
            
            aD2ds=AD2ss[basins[0],stmyear]
            try:
                aD2=aD2ds.getDataSet(key)
            except:
                aD2=None

            if(aD2 != None):

                aD2dtgs=aD2.dtgs
                aD2dtgs.sort()
                
                if(dtg in aD2dtgs):
                    aidtrk=aD2.AT.atrks[dtg]
                    self.aid=taid
                    self.aidtrk=aidtrk
                    self.aidtaus=aidtrk.keys()
                    self.aidtaus.sort()
                    self.aidsource=source
                    self.aidname=taid
                    self.stmid=stmid
                    gotaid=1
                else:
                    gotaid=0
            else:
                gotaid=0
                    
            if(not(gotaid)):
                noaidtaus=[]
                lasttau=-999
                print 'NONONONO no tracker from aidsource: %-10s'%(source),' taid: %-6s'%(taid),' stmid: ',stmid,' ntaus: %3d'%(len(noaidtaus)),\
                      ' lasttau: %3d'%(lasttau),' finalstmid: ',stmid,' dtg: ',dtg,' <<<<<------'
                return(0)


            # -- get second adeck and merge position/intensity
            #
            if(taid == 'tvcn'):
                taid2='ivcn'
                key2="%s_%s"%(taid2,stmid.upper())
                try:
                    aD2=aD2ds.getDataSet(key2)
                except:
                    aD2=None
                
                if(dtg in aD2dtgs):
                    aidtrk2=aD2.AT.atrks[dtg]
                    gotaid2=1
                else:
                    gotaid2=0
                    
                aid2taus=aidtrk2.keys()
                aid2taus.sort()
                
                for tau2 in aid2taus:
                    if(tau2 in self.aidtaus):
                        self.aidtrk[tau2][2]=aidtrk2[tau2][2]
                
                if(verb):
                    print 'MMM --- merging ivcn into tvcn'
                    for tau2 in aid2taus:
                        print 'IVCN tau2: ',tau2,' aidtrk2: ',aidtrk2[tau2][2]
                    
                    for tau in self.aidtaus:
                        print 'TVCN tau:  ',tau,' aidtrk: ',self.aidtrk[tau][0:2]
                    

            # -- get the vdeck
            #
            if(self.vD2 == None):
                VD2ss=getVdeck2DSs(tstmids,verb=1)
                try:
                    vD2=VD2ss[stmyear].getDataSet(key)
                except:
                    vD2=None
                self.vD2=vD2
            else:
                vD2=self.vD2    
                
            self.vd=vD2

            do6hinterp=1
            if(do6hinterp):
                aDu=ADutils()
                (iatrk,itaus)=aDu.FcTrackInterpFill(self.aidtrk,dtx=6)
                itaus=iatrk.keys()
                itaus.sort()
                self.aidtrk=iatrk
                self.aidtaus=itaus

            self.aidFEs={}
            
            for tau in self.aidtaus:
                self.aidFEs[tau]=-999
                
            if(self.vd != None):

                for tau in self.aidtaus:
    
                    if(self.maxtau != None and tau > self.maxtau): continue
                    fe=-999.
                    try:
                        vdtgs=self.vd.bdtg[tau]
                        ndx=vdtgs.index(dtg)
                        fe=self.vd.fe[tau][ndx]
                    except: 
                        None
    
                    if(fe == self.vd.undef): fe=-999.
                    self.aidFEs[tau]=fe
                    


        else:
            if(not(quiet)): print 'WWW setTCtracker no aD for source: ',source,' aid: ',aid,' dtg: ',dtg
            return(0)

        if(dols and hasattr(self,'aidtaus')):

            print 'Aid: ',self.aidname,' Stmid: ',self.stmid,'dtg: ',dtg
            print 'tau  lat   lon   vmax    pmin'
            
            for tau in self.aidtaus:

                if(self.maxtau != None and tau > self.maxtau): continue
                fe=-999.
                if(self.vd != None):
                    
                    try:
                        vdtgs=self.vd.bdtg[tau]
                        ndx=vdtgs.index(dtg)
                        fe=self.vd.fe[tau][ndx]
                    except:
                        None

                    if(fe == self.vd.undef): fe=-999.
                
                tt=self.aidtrk[tau]

                fclat=tt[0]
                fclon=tt[1]
                fcvmax=tt[2]
                fcpmin=tt[3]

                btdtg=mf.dtginc(dtg,tau)
                btlat=-99.
                btvmax=-99.
                btlon=-999.
                wnflg='  '
                tcflg='  '
                try:
                    bt=self.btrk[btdtg]
                    btlat=bt[0]
                    btlon=bt[1]
                    btvmax=bt[2]
                    wnflg=bt[-1]
                    tcflg=bt[-2]
                except:
                    None
                    

                if(fcvmax == -99.):  cfcvmax='   '
                else:               cfcvmax="%3.0f"%(fcvmax)
                
                if(fclat == -99.):  cfclat='     '
                else:               cfclat="%5.1f"%(fclat)
                
                if(fclon == -999.): cfclon='      '
                else:               cfclon="%6.1f"%(fclon)

                if(fcpmin == -9999.): cfcpmin='    '
                else:                 cfcpmin="%4.0f"%(fcpmin)


                if(btvmax == -99.):  cbtvmax='    '
                else:               cbtvmax="%4.0f"%(btvmax)
                
                if(btlat == -99.):  cbtlat='     '
                else:               cbtlat="%5.1f"%(btlat)
                
                if(btlon == -999.): cbtlon='      '
                else:               cbtlon="%6.1f"%(btlon)
                
                if(fe == -999.):    cfe='      '
                else:               cfe="%6.1f"%(fe)
                
                
                print "%03d %s %s  %s  %s  BT: %s %s %s %s %s  FE: %s"%(tau,
                                                                        cfclat,cfclon,cfcvmax,cfcpmin,
                                                                        cbtlat,cbtlon,cbtvmax,
                                                                        tcflg,wnflg,cfe)
            return


        ataus=[]
        if(maxtau != None):
            for atau in self.aidtaus:
                if(atau in self.targetTaus):
                    ataus.append(atau)
            self.aidtaus=ataus

        if(self.aidtrk != None):
            print 'TCTCTCTC got tracker from aidsource: %-10s'%(self.aidsource),' aid: %-6s'%(self.aid),' stmid: ',stmid,' ntaus: %3d'%(len(self.aidtaus)),\
                  ' lasttau: %3d'%(self.aidtaus[-1]),' finalstmid: ',self.stmid,' dtg: ',dtg
            

        

        self.aidMotion={}
        
        

        # -- get the motion based on the next tau
        #
        ntaus=len(self.aidtaus)

        for tau in self.aidtaus:
            
            # -- get track for spd/dir calc
            taup0=tau
            rc=self.aidtrk[taup0]
            (latcp0,loncp0,vmaxcp0,pmincp0)=rc[0:4]

            np=self.aidtaus.index(tau)

            # -- check if at end of tau...
            #
            if(np == ntaus-1):
                np=np-1
                taup0=self.aidtaus[np]
                rc=self.aidtrk[taup0]
                (latcp0,loncp0,vmaxcp0,pmincp0)=rc[0:4]

            # -- get track at next tau
            #
            np1=np+1
            taup1=self.aidtaus[np1]
            rc=self.aidtrk[taup1]
            (latcp1,loncp1,vmaxcp1,pmincp1)=rc[0:4]

            dt=taup1-taup0
            if(dt == 0):
                dir=9999.
                spd=9999.
            else:
                (dir,spd,umot,vmot)=rumhdsp(latcp0,loncp0,latcp1,loncp1,taup1-taup0)
                if(dir == 360.0): dir=0.0

            # -- bug in setting the endpoint, bandaid for now...
            #
            if(spd < 0.0):
                spd=9999.
                dir=9999.

            self.aidMotion[tau]=(dir,spd)
            if(verb): print 'ttttttttttt ',tau,'latlon0:',latcp0,loncp0,'latlon1: ',latcp1,loncp1,'dirspd: ',dir,spd

        return(1)


    def makeIntensityGs(self,
                        intensityScale=0.55,
                        corner=22,
                        ):
        
        self.ge.getGxinfo()
        
        stmid=self.stmid
        dtgs=self.dtgs
        
        dtgb=dtgs[0]
        dtge=dtgs[-1]
        dtgb=mf.dtginc(dtgb,-self.nhbakBT)
        dtge=mf.dtginc(dtge,self.maxtau+24)
        
        gtimeb=mf.dtg2gtime(dtgb)
        gtimee=mf.dtg2gtime(dtge)
        
        gs="""function main(args)

rc=gsfallow('on')
rc=const()

dtg='%s'
stmid='%s'
vmdir='/tmp/'

bfile=vmdir'btvmax.'stmid'.'dtg'.ctl'
b0=ofile(bfile)

"""%(dtg0,stmid)

        gs=gs+tIP.makeTcIntensityPlotOfileGs()

        self.ge.getGxinfo()
        
        plotxl=self.ge.plotxl
        plotxr=self.ge.plotxr
        plotyb=self.ge.plotyb
        plotyt=self.ge.plotyt
        
        # -- lower left 11
        #
        if(corner == 11):
            gsCorner="""
yvb=%f+gut
yvt=yvb+dvy
xvl=%f+gut
xvr=xvl+dvx
        
"""%(plotyb,plotxl)

        # -- upper left 21
        #
        elif(corner == 21):
            gsCorner="""
yvb=%f-dvy-gut
yvt=%f-gut
xvr=%f+dvx+gut
xvl=%f+gut
                    
"""%(plotyt,plotyt,plotxl,plotxl)
          
        # -- upper right 22
        #
        elif(corner == 22):
            gsCorner="""
yvb=%f-dvy-gut
yvt=%f-gut
xvl=%f-dvx-gut
xvr=%f-gut
                    
"""%(plotyt,plotyt,plotxr,plotxr)
            
        # -- lower right 12
        #
        elif(corner == 12):
            gsCorner="""
yvb=%f+gut
yvt=yvb+dvy
xvl=%f-dvx-gut
xvr=%f-gut
                    
"""%(plotyb,plotxr,plotxr)
            
        
        gs=gs+"""

scale=1.0
scale=0.75
#scale=1.25
scale=%4.1f
aspect=4/3
aspect=16/9

dvx=4
dvy=dvx/aspect
gut=0.35

slab=0.085
smrk=0.03

dvx=dvx*scale
dvy=dvy*scale
gut=gut*scale
slab=slab*scale
smrk=smrk*scale

%s

#print 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX 'xvl' 'xvr' YYYY 'yvb' 'yvt

x1=xvl-gut
x2=xvr+gut
y1=yvb-gut
y2=yvt+gut

'set rgb 122 150 150 150'
'set line 122'
#'set background 122'

'draw polyf 'x1' 'y1' 'x2' 'y1' 'x2' 'y2' 'x1' 'y2' 'x1' 'y1

'set dfile 'b0
'set x 1'
'set y 1'
'set t 1 last'

'set time %s %s'

'set parea 'xvl' 'xvr' 'yvb' 'yvt
'set grads off'

'set vrange 0 170'
'set ylint 20'
'set xlopts 1 3 'slab
'set ylopts 1 3 'slab
'set grid on 3 15 3'

'set ccolor 0'
'set digsiz 0.03'
'set cmark 3'
'd bvm'"""%(intensityScale,
            gsCorner,
            gtimeb,gtimee)

        gs=gs+tIP.makeTcIntensityPlotGs()
                
        gs=gs+"""

'set grid off'
'set ccolor 0'
'set digsiz 0.05'
'set cmark 3'
'd bvm'

t1='V`bmax`n[kt] Best Track - black'
scl=0.5
dorecf=0
rc=stitle(t1,scl,dorecf)
return
"""%(    )
        
        MF.WriteString2Path(gs,'/tmp/g.gs')
        

def getModelAdeck(model,ftdtg,source):

    adeck=None
    sdir="%s/tmtrkN/%s"%(w2.TcDatDir,ftdtg)
    if(source == 'tmtrkN'):
        # -- tmtrkN
        adeck="%s/%s/tctrk.atcf.%s.%s.txt"%(sdir,model,ftdtg,model)
        ftlabel='tmtrkN'
    elif(source == 'mftrkN'):
        # -- mftrkN
        adeck='%s/%s/wxmap2.v010.%s.%s.%s'%(sdir,model,model,ftdtg,finalstmid)
        ftlabel='mftrkN'

    if(not(MF.ChkPath(adeck))):
        print 'EEE no adeck for: ',adeck
        sys.exit()

    return(adeck,ftlabel)



class MdeckCmdLine(CmdLine):

    otags=getMd2DSsTags()
    
    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv

        self.argv=argv

        self.argopts={
            1:['dtgopt',    'dtgs'],
            2:['modelopt',  """models: MMM1 | MMM1,MMM2,...,MMMn | 'all'"""],
            }

        self.defaults={
            'lsopt':         's',
            'doupdate':        0,
            'cnvSubbasin':     0,
            }

        self.options={
            'centerdtg':       ['G:',None,'a','dtg to center plots to center +- taus'],
            'dssDir':          ['D:',None,'a','set base dir for DSs'],
            'dtg0':            ['0:',None,'a','dtg0 - start dtg'],
            'doxv':            ['X',0,1,'run xv on plot'],
            'doBT':            ['b',2,0,"""for case when can't find gen with bt=1"""],
            'maxtau':          ['M:',168,'i','max forward tau'],
            'maxlandFrac':     ['m:',0.8,'f','maxlandFrac to be land'],
            'doerr':           ['E:',-999,'i','set the tau to plot PE'],
            'override':        ['O',0,1,'override'],
            'cycle':           ['C',0,1,'cycle models/dtgs'],
            'dols':            ['l',0,1,'dols only'],
            'verb':            ['V',0,1,'verb=1 is verbose'],
            'doland':          ['L',1,0,'exclude land points from bt'],
            'dolandFC':        ['f',1,0,'exclude land points from fc'],
            'ropt':            ['N','','norun',' norun is norun'],
            'stmopt':          ['S:',None,'a','stmopt'],
            'labeltag':        ['t:',None,'a','labeltag - extra labeling'],
            'zoomfact':        ['Z:',None,'a','zoom factor | corner pts lat1,lon1,lat2,lon2'],
            'dtg0012':         ['2',0,1,'list storm stats only'],
            'useReftrk':       ['R',0,1,'use the ops reftrk'],
            'quiet':           ['q',1,0,'turn off quiet'],
            'doDropbox':       ['d',0,1,'do cp plot to dropbox'],
            'plotFTwithBT':    ['F',0,1,'plot FT only with verifying BT'],
            'doPngQ':          ['Q',1,0,'do NOT reduce plot file size using pngquant - 24bit'],
            'cur12dtg':        ['1:',None,'a','set cur12dtg used in setting the pltdir and labeling'],
            'intensityScale':  ['I:',0.60,'f','how big to make intensity plot'],
            }

        self.purpose='''
plot trks'''
        
        self.purpose=self.purpose+'''
-t tags: %s'''%(self.otags)
        
        self.examples='''
%s 2012102300 edet,avno -S 01p -X'''

def errM2(option,opt=None):

    if(option == 'model'):
        print """EEE(errM2): can't make m2 for model: %s"""%(opt)
    else:
        print 'Stopping in errAD: ',option

    sys.exit()
        

    
#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# -- main
#

# -- change to dir
#

prcdir=w2.PrcDirTctrkW2
#MF.ChangeDir(prcdir)

MF.sTimer('all')

CL=MdeckCmdLine(argv=sys.argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

dtgs=mf.dtg_dtgopt_prc(dtgopt)
models=modelopt.split(',')

if(cycle and (len(dtgs) > 1)):

    # cycle by dtgs
    #
    MF.sTimer('TrkPlot-Cycle-ALL')
    for dtg in dtgs:
        cmd="%s %s %s"%(pypath,dtg,modelopt)
        for o,a in CL.opts:
            if(o != '-C'): #-- let this pass to save if cycling
                cmd="%s %s %s"%(cmd,o,a)
            #cmd="%s %s %s"%(cmd,o,a)

        mf.runcmd(cmd,ropt)
    MF.dTimer('TrkPlot-Cycle-ALL')
    sys.exit()

if(verb): MF.sTimer('tcdata')
tcD=TcData(dtgopt=dtgs[0],verb=verb)
if(verb): MF.dTimer('tcdata')

# -- set grads
#
xgrads=setXgrads(useX11=0)

ddtg=12
if(dtg0012): ddtg=12

#if(stmopt != None):  stmids=MakeStmList(stmopt)
#else:                stmids=[]

didold=0

if(stmopt != None):
    lstm=len(stmopt.split('.')[0])
    if(lstm == 1 or lstm == 3 or mf.find(stmopt,'cc') ):
        stmids=tcD.makeStmListMdeck(stmopt,dobt=0,cnvSubbasin=cnvSubbasin)
    else:
        didold=1
        ostmids=MakeStmList(stmopt)
else:
    stmids=[]

# -- if used old stm lister, put through new one that uses the stmids keys; 
# -- needed for 9X=> [a-z][0-9]

if(didold):
    stmids=[]
    for ostmid in ostmids:
        stmids=stmids+tcD.makeStmListMdeck(ostmid,dobt=dobt,cnvSubbasin=cnvSubbasin)

for stmid in stmids:
    ostmid=tcD.getSubbasinStmid(stmid)

if(dtg0 != None and dtg0 in dtgs):
    dtg0=dtg0
else:
    dtg0=dtgs[0]

ftdtg=dtg0
if(dtg0 != None and stmopt == None):
    stmids=tcD.getStmidDtg(ftdtg)

# -- setup dat dir
#
if(dssDir != None):
    dsbdir=dssDir
    dsbdirVD2=dssDir
else:
    dsbdir="%s/DSs"%(TcDataBdir)
    dsbdirVD2="%s/DSs-VD2"%(TcDataBdir)
    
    # -- local for DSs or DSs-local in .
    #
    dsbdir="%s/DSs"%(TcDataBdir)
    localDSs=os.path.abspath('./DSs')
    localDSsLocal=os.path.abspath('./DSs-local')
    
    if(os.path.exists(localDSs)):
        dsbdir=localDSs
        dsbdirVD2=dsbdir
        
    elif(os.path.exists(localDSsLocal)):
        dsbdir=localDSsLocal
        dsbdirVD2=dsbdir


# -- class handling tc intensity plot
#
tIP=TcIntensityPlot(models,verb=verb)

# -- get full set if stmids
#
fstmids=[]
for stmid in stmids:

    allstmids=tcD.makeStmListMdeck(stmid,dobt=0,cnvSubbasin=cnvSubbasin)
    
    if(len(allstmids) > 1):

        if(dtg0 != None):
            for allstmid in allstmids:
                odds=tcD.getDSsFullStm(allstmid)
                if(dtg0 in odds.dtgs):
                    fstmids.append(allstmid)
        else:
            fstmids.append(allstmid)

    else:
        fstmids.append(stmid)


allTrkPlots={}

for stmid in fstmids:

    NgotATs=0
    didBTplot=0

    # -- convert 2-char basin stm1id to subbasin using Tcnames
    #
    finalstmid=tcD.getSubbasinStmid(stmid)

    tP=TcBtFtTrkPlot(stmid,finalstmid,models,dtgs,
                     tD=tcD,
                     dsbdir=dsbdir,
                     Window=0,zoomfact=zoomfact,centerdtg=centerdtg,
                     override=override,dtgopt=dtgopt,
                     useReftrk=useReftrk,
                     Quiet=quiet,
                     Bin=xgrads,
                     #mktaus=[maxtau],
                     mktaus=None,
                     maxtau=maxtau,
                     doerr=doerr,
                     xsize=xsizeTcTrk,
                     dols=dols,
                     verb=verb,
                     dobt=doBT,  # for 01W.2019 have to use doBt=0
                     labeltag=labeltag,
                     doland=doland,
                     dolandFC=dolandFC,
                     docycle=cycle,
                     cur12dtg=cur12dtg,
                     maxlandFrac=maxlandFrac,
                     )

    MF.sTimer('trkplot-ALL: %s'%(stmid))
    
    
    #tP.ls()
    #tP.BT.ls()
    #dtgs=tP.BT.dtgs
    #for dtg in dtgs:
        #print 'ddd',dtg,tP.BT.btcs[dtg]
    #sys.exit()
    if(not(override) and tP.plotDone):
        print 'III-tP.plotDone:   and not override...press...'
        MF.dTimer('trkplot-ALL: %s'%(stmid))
        continue


    # -- find corner with fewest points
    #
    MF.sTimer('III-get-corner-intensity: %s'%(stmid))

    alats=[]
    alons=[]

    for model in models:

        for ftdtg in dtgs:
            gotTrks=tP.setTCtracker(finalstmid,ftdtg,taid=model,maxtau=maxtau,quiet=quiet,dols=dols)
            if(gotTrks):
                for atau in tP.aidtaus:
                    alat=tP.aidtrk[atau][0]
                    alon=tP.aidtrk[atau][1]
                    alats.append(alat)
                    alons.append(alon)
                
    corner=getCornerFewestLatLon(alats,alons,
                             tP.lat1,tP.lat2,tP.lon1,tP.lon2,
                             verb=verb)
    
    MF.dTimer('III-get-corner-intensity: %s'%(stmid))
    
    # -- now cycle through models and plot
    #
    
    for model in models:

        aidSource=model
        mss=model.split('.')
        if(len(mss) == 2):
            model=mss[0]
            source=mss[1]
            adeck=None
        elif(len(mss) == 1):
            aidSource=None
            source='ad2'

        MF.sTimer('trkplot: %s %s'%(stmid,model))


        for ftdtg in dtgs:
            if(tP.setTCtracker(finalstmid,ftdtg,taid=model,maxtau=maxtau,quiet=quiet,dols=dols)):
                NgotATs=NgotATs+1

        if(NgotATs == 0):
            print 'EEE(%s) no tracker for any dtgs: '%(pyfile),dtgs,' and model: ',model
            # -- continue vice sys.exit() to look for trackers of other models...
            if(len(models) == 1): 
                print 'III sayoonara--only one model :( and no trackers'
                sys.exit()
            

        if(not(tP.plotDone)):

            # -- do BT on first tracker
            #
            if( ((NgotATs == 1) or (not(cycle) and NgotATs >= 1)) and didBTplot == 0):

                tP.PlotTrkBT(tIP,dtg0012=dtg0012,ddtg=ddtg,dtg0=dtg0,
                             nhbakBT=48,
                             nhforBT=None,
                             dtau=12,
                             doerr=doerr,
                             )
                didBTplot=1

            # -- plot each FC track
            #
            for ftdtg in dtgs:

                gotTrks=tP.setTCtracker(finalstmid,ftdtg,taid=model,maxtau=maxtau,quiet=quiet,dols=dols)
                if(gotTrks == 0):
                    print 'NNNN no tracker for finalstmid: ',finalstmid,'ftdtg: ',ftdtg

                else:
                    #mks=tP.pbt.markprop.keys()
                    #mks.sort()
                    #for mk in mks:
                    #    print 'mmm',mk,tP.pbt.markprop[mk]
                        
                    tP.PlotTrkFC(tIP,model,ftdtg,
                                 etau=maxtau,
                                 dtau=12,
                                 doerr=doerr,
                                 plotFTwithBT=plotFTwithBT,
                                 )
                    continue
                
                    if(doerr != -999):
                        tP.PlotTrkError(model,ftdtg,
                                        etau=doerr,
                                        dtau=doerr,
                                        )

                    MF.appendDictList(allTrkPlots,stmid,tP.pltpath)
                        
    if((not(dols) and not(tP.plotDone) or override) and NgotATs > 0):
        tP.makeIntensityGs(intensityScale=intensityScale,corner=corner)
        tP.PlotTrkTitle()
        tP.ga('run /tmp/g.gs')
        tP.pngPath()
        if(doPngQ): tP.pngquantPlot()
        
            
    pstmids=allTrkPlots.keys()
        
    MF.dTimer('trkplot: %s %s'%(stmid,model))
    MF.dTimer('trkplot-ALL: %s'%(stmid))

    if(tP.plotDone != -1 and not(dols) and NgotATs > 0): 
        if(doDropbox): tP.cpDropbox()
        if(doxv): tP.xvPlot(zfact=1.0)
        

