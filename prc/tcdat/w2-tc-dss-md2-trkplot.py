#!/usr/bin/env python

from tcbase import *
#import ga2
from ga2 import setGA,gXplotTcBt
from TCtrk import TcPrBasin,getBasinOptFromStmids,tcgenBasins,tcgenModelLabel,getBasinLatLonsPrecise

class TcBtTrkPlot(DataSet):
    
    def __init__(self,stmid,
                 stmopt=None,
                 tD=None,
                 pltdir='%s/tctrk'%(w2.ptmpBaseDir),
                 model='bt',
                 aidtrk=None,
                 aidtaus=None,
                 zoomfact=None,
                 dtgopt=None,
                 otau=48,
                 dobt=1,
                 Quiet=1,
                 Window=0,
                 Bin='grads',
                 doLogger=0,
                 background='black',
                 xsize=1200,
                 #xsize=1600,
                 docp2Dropbox=1,
                 pngmethod='printim',
                 dopbasin=0,
                 verb=0,override=0):

        # -- get TC info and best track
        #
        if(tD == None):
            tD=TcData(stmopt=stmid)
            
        self.tD=tD
            
        btstmid=stmid
        
        # -- first get the BT
        #
        self.BT=tD.makeBestTrk2(btstmid,dobt=dobt,set9xfirst=1)
        self.btrk=self.BT.btrk

        self.stmid=stmid
        (self.stm3id,self.stmname)=tD.getStmName3id(self.stmid)        
        
        stmid=tD.getSubbasinStmid(stmid)
        basin=getBasinOptFromStmids(stmid)[0]
        (snum,b1id,year,b2id,stm2id,stm1id)=getStmParams(stmid)
        if(b1id.lower() == 'c'): basin='cepac'
        #latlons=getBasinLatLonsPrecise(basin)
        
        if(dopbasin):
            pbasin=TcGenBasin2PrwArea[basin]
        else:
            pbasin=None
            
        self.model=model
        self.pltdir=pltdir
        MF.ChkDir(pltdir,'mk')

        self.aidtrk=aidtrk
        self.aidtaus=aidtaus
        self.zoomfact=zoomfact
        self.otau=otau
        self.Bin=Bin
        
        self.xsize=xsize
        self.ysize=xsize*(3.0/4.0)
        self.verb=verb
        self.docp2Dropbox=docp2Dropbox
        
        self.pngmethod=pngmethod
        if(mf.find(background,'w') or mf.find(background,'W')): background='white'
        if(mf.find(background,'b') or mf.find(background,'B')): background='black'
        
        if(background != 'white' and background != 'black'):
            print "EEE background in TcBtTrkPlot must be white or black"
            sys.exit()
            
        self.background=background
        
        self.bgcol=0
        if(background == 'white'): self.bgcol=1
        
        self.override=override
        self.Window=Window
        self.doLogger=doLogger

        self.centerdtg=None
        if(dtgopt != None): self.centerdtg=mf.dtg_command_prc(dtgopt)

        self.setLatLonBox(pbasin=pbasin,reduceLon1=0.0,reduceLon=10.0,reduceLat=5.0)
        
        (clat1,clon1)=Rlatlon2Clatlon(self.lat1,self.lon1,dozero=1,dotens=0)
        (clat2,clon2)=Rlatlon2Clatlon(self.lat2,self.lon2,dozero=1,dotens=0)
        trkstmname=self.stmid
        if(stmopt != None):
            trkstmname=stmopt
        self.pltfile="trkplt.%s.%s.%s-%s.%s-%s.png"%(trkstmname,self.model,clat1,clat2,clon1,clon2)
        self.pltpath="%s/%s"%(self.pltdir,self.pltfile)
        self.trkplotpath=self.pltpath

        self.alreadyDone=0
        if(not(override) and MF.ChkPath(self.trkplotpath)):
            print 'III trkplotpath: ',self.trkplotpath,' already there and override=0...'
            self.alreadyDone=1
            return

        ga=setGA(Quiet=Quiet,Window=Window,doLogger=doLogger,Bin=Bin)

        dumctl="%s/dum.ctl"%(w2.GradsGslibDir)
        ga.fh=ga.open(dumctl)

        self.ga=ga
        self.ge=ga.ge
        
        self.ge.pareaxl=0.50
        self.ge.pareaxr=9.75
        self.ge.pareayb=0.25
        self.ge.pareayt=8.00  # decreased from 8.25
        self.ge.setParea()

        self.curgxout=self.ga.getGxout()
        self.setInitialGA()


    def setLatLonBox(self,pbasin=None,timelab=None,reduceLon1=None,reduceLon=None,reduceLat=None):
        
        if(pbasin != None):
            if(reduceLon == None): reduceLon=0.0
            if(reduceLat == None): reduceLat=0.0
            if(reduceLon1 == None): reduceLon1=reduceLon
            
            aW2=getW2Area(pbasin)
            self.aW2=aW2
            lon1=aW2.lonW
            lon2=aW2.lonE
            lat1=aW2.latS
            lat2=aW2.latN
            
            print 'LLL',lon1,lon2,lat1,lat2
            if(lat1 < 0): lat1=lat1+reduceLat
            else: lat1=lat1-reduceLat

            if(lat2 < 0): lat2=lat2+reduceLat
            else: lat2=lat2-reduceLat
            
            lon1=lon1+reduceLon1
            lon2=lon2-reduceLon

            print 'LLL----',lon1,lon2,lat1,lat2
             
            self.lon1=lon1
            self.lon2=lon2
            self.lat1=lat1
            self.lat2=lat2
            self.xlint=aW2.xlint
            self.ylint=aW2.ylint
            self.pbasin=pbasin
            
            return


        alats=[]
        alons=[]
        avmaxs=[]
        apmins=[]
        
        dtgs=self.btrk.keys()
        dtgs.sort()

        for dtg in dtgs:
            bt=self.btrk[dtg]
            alats.append(bt[0])
            alons.append(bt[1])
            avmaxs.append(bt[2])
            apmins.append(bt[3])
            
        self.alats=alats
        self.alons=alons
        self.avmaxs=avmaxs
        self.apmins=apmins
        
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

            zoom=float(self.zoomfact)

            dlon=(lon2-lon1)/zoom
            dlat=(lat2-lat1)/zoom
            dint=2.5

            if(self.centerdtg == None and zoom < 1.25):
                latOff=0.65
                if(IsNhemBasin(self.stmid)): latOff=0.35
            else:
                latOff=0.50
                
            lonOff=0.50
            
            lat1=rlat-dlat*latOff
            lat1=int(lat1/dint+0.5)*dint
            lat2=lat1+dlat

            lon1=rlon-dlon*lonOff
            lon1=int(lon1/dint+0.5)*dint
            lon2=lon1+dlon


        self.lat1=lat1
        self.lat2=lat2
        self.lon1=lon1
        self.lon2=lon2
        
        
    def setInitialGA(self):

        ga=self.ga
        ge=self.ge

        ge.lat1=self.lat1           
        ge.lat2=self.lat2   
        ge.lon1=self.lon1   
        ge.lon2=self.lon2   
        
        if(hasattr(self,'xlint')): ge.xlint=self.xlint
        if(hasattr(self,'ylint')): ge.ylint=self.ylint
        # -- clear
        #
        ge.clear()
        ge.mapdset='mres'
        ge.mapdset='hires'
        ge.mapthick=4
        ge.mapcol=self.bgcol
        ge.mapcol=45
        ge.setMap()
        ge.grid='off'
        ge.setGrid()
        ge.setLatLon()
        ge.setXylint()
        ge.setParea()
        ge.setPlotScale()
        ge.setXsize(xsize=self.xsize,ysize=self.ysize)
        ge.setColorTable()
        # -- force this?
        ge.timelab='on'


        

    def PlotTrk(self,
                doft=0,dtg0=None,nhbak=None,nhfor=None,
                ddtg=6,dtg0012=1,maxbt=55,
                doalltaus=1,otau=48,etau=120,dtau=12):


        if(self.alreadyDone): return
        
        ga=self.ga
        ge=self.ge

        if(doft):
            self.etau=etau
            self.dtau=dtau
            self.otau=otau

            mktaus=[0,24,48,72,120]
            mkcols={0:1,24:1,48:1,72:2,120:2}
            
            ftlcol=modelTrkPlotProps[self.model][0]
            modeltitle=modelOname[self.model]

            (btau,etau,dtau)=(0,etau,dtau)
            itaus=range(btau,etau+1,dtau)

            taus=[]
            for itau in itaus:
                for ttau in self.aidtaus:
                    if(itau == ttau):
                        taus.append(itau)


        pbt=ga.gp.plotTcBt
        pbt.set(self.btrk,dtg0=dtg0,nhbak=nhbak,nhfor=None,ddtg=ddtg,dtg0012=dtg0012,maxbt=maxbt)
        
        bm=ga.gp.basemap2
        #bm.set(landcol='sienna',oceancol='steelblue')
        # -- try atcf colors
        bm.set(landcol='atcfland',oceancol='atcfocean')
        bm.draw()
        ge.setPlotScale()

        #pbt.dline(times=pbt.otimesbak,lcol=7,lthk=10)
        pbt.dline(times=pbt.otimesbak)
        pbt.dwxsym(times=pbt.otimesbak)
        pbt.legend(ge,times=pbt.otimesbak,ystart=7.9)

        if(doft):

            pft=ga.gp.plotTcFt
            pft.set(self.aidtrk,lcol=ftlcol,doland=1)

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
                pft.dline(times=taus,lsty=3)
                pft.dmark(times=taus,mksiz=0.050)
                for mktau in mktaus:
                    if(mktau in taus):
                        pft.dmark(times=[mktau],mksiz=0.100)
                        pft.dmark(times=[mktau],mkcol=0,mksiz=0.070)
                        pft.dmark(times=[mktau],mkcol=mkcols[mktau],mksiz=0.040)


    

        ttl=ga.gp.title
        ttl.set(scale=0.85)
        
        if(hasattr(self,'pbasin')):
            t1='pTCs for basin: ',self.pbasin.upper()
            t2='md2 BT'
        else:
            btvmax=max(self.avmaxs)
            t1='TC: %s [%s]  V`bmax`n: %3dkt'%(self.stmid,self.stmname,btvmax)
            t2='mdeck2 best track'
        ttl.top(t1,t2)

        if(self.Window): ga('q pos')

        #ge.pngmethod='gxyat'
        ge.makePng(self.pltpath,background=self.background,verb=1)



    def PlotTrkAll(self,stmids,dobt=0,
                dtg0=None,nhbak=None,nhfor=None,
                ddtg=6,dtg0012=1,maxbt=55,
                doalltaus=1,otau=48,etau=120,dtau=12):


        ga=self.ga
        ge=self.ge

        pbt=ga.gp.plotTcBt
        cb=ga.gp.cbarn
        
        nTot=0
        nDev=0
        nNonDev=0
        
        pcolsN=[72,73,74,75,77,79]
        pcolsNReverse=[79,77,75,74,73,72]
        pcolsD=[22,23,35,37,39,29]
 
        devstmids=[]
        
        for stmid in stmids:
            
            BT=self.tD.makeBestTrk2(stmid,dobt=dobt)
            (ocard,ocards)=self.tD.lsDSsStm(stmid,dobt=dobt,sumonly=1,doprintSum=0)
            (ocardBT,ocardsBT)=self.tD.lsDSsStm(stmid,dobt=1,sumonly=1,doprintSum=0)
            tt=ocard.split(':')
            
            totTime=float(ocard.split(':')[2].split(';')[0])
            totTimeBT=float(ocardBT.split(':')[2].split(';')[0])

            totTime9X=float(ocard.split(':')[2].split(';')[1])
            totTime9XBT=float(ocardBT.split(':')[2].split(';')[1])
            
            #print 'TTTTTTTT',stmid,ocard.split(':')[2].split(';'),ocardBT.split(':')[2].split(';')
            print 'TTTTTTTT',stmid,totTime,totTimeBT,totTime9X,totTime9XBT
            
            pbt.set(BT.btrk,dtg0=dtg0,nhbak=nhbak,nhfor=None,ddtg=ddtg,dtg0012=dtg0012,maxbt=maxbt)
            
            nTot=nTot+1
            if(IsNN(stmid)):
                dev=1
                devstmids.append(stmid)
                nDev=nDev+1
            else:    
                nNonDev=nNonDev+1
                dev=0
                
            if(stmid == stmids[0]):
                bm=ga.gp.basemap2
                bm.set(landcol='atcfland',oceancol='atcfocean')
                bm.draw()
                
            ge.setPlotScale()
    
            lcol=15
            lthk=5
            mkcol=0
            mkcolB=1
            mkcolE=0
            mksizB=0.040
            mksizE=0.050
            if(dev): 
                lcol=2
                lthk=6
                mksiz=0.035
                mkcol=9
                mkcolB=1
                mkcolE=9
                mksizE=0.075
            
            if(Is9X(stmid)): totTime=totTime9X
            
            print 'stmid: ',stmid,'totTime: ',totTime,'DevFlag: ',dev
            
            if(totTime <= 1.0):
                lcolD=pcolsD[0]
                lcolN=pcolsN[0]
            elif(totTime > 1.0 and totTime <= 2.5):
                lcolD=pcolsD[1]
                lcolN=pcolsN[1]
            elif(totTime > 2.5 and totTime <= 4.0):
                lcolD=pcolsD[2]
                lcolN=pcolsN[2]
            elif(totTime > 4.0 and totTime <= 5.5):
                lcolD=pcolsD[3]
                lcolN=pcolsN[3]
            elif(totTime > 5.5 and totTime <= 7.0):
                lcolD=pcolsD[4]
                lcolN=pcolsN[4]
            elif(totTime > 7.0):
                lcolD=pcolsD[5]
                lcolN=pcolsN[5]
                
            if(dev): 
                lcol=lcolD
            else:
                lcol=lcolN
                lthk=4
            
            pbt.dline(times=pbt.otimes,lcol=lcol,lsty=1,lthk=lthk)
            if(dev):
                pbt.dmark(times=pbt.otimes[0:1],mksym=3,mksiz=mksizB,mkcol=mkcolB)
                pbt.dmark(times=pbt.otimes[-1:],mksym=3,mksiz=mksizE,mkcol=mkcolE)
            else:
                pbt.dmark(times=pbt.otimes[0:1],mksym=3,mksiz=mksizB,mkcol=mkcolB)
                pbt.dmark(times=pbt.otimes[-1:],mksym=3,mksiz=mksizE,mkcol=mkcolE)
                
        ttl=ga.gp.title
        ttl.set(scale=0.85)
        
        pDev=(float(nDev)/float(nTot))*100.0
        
        devstmids.sort()
        
        print 'SSS: ',nTot,nDev,nNonDev,pDev
        if(hasattr(self,'pbasin')):
            t1='Dev v NonDev pTCs for basin: %s nTot: %d nDev: %d  %% Dev: %3.0f'%(self.pbasin.upper(),nTot,nDev,pDev)
            t2='%s -> %s'%(devstmids[0],devstmids[-1])
        else:
            btvmax=max(self.avmaxs)
            t1='TC: %s [%s]  V`bmax`n: %3dkt'%(self.stmid,self.stmname,btvmax)
            t2='mdeck2 best track'
        ttl.top(t1,t2)

        if(self.Window): ga('q pos')
        
        pcols=[79,   77,  75,   74,  73,   72, 22, 23,  24,  35, 47,   29]
        pcols=pcolsNReverse + pcolsD
        pcuts=[ -7.0, -5.5, -4.0, -2.5, -1.0, 0.0, 1.0, 2.5, 4.0, 5.5, 7.0]
        
        cb.draw(sf=0.75, vert=1, side=None, xmid=None, ymid=None, sfstr=1.0, 
               pcuts=pcuts, pcols=pcols, quiet=0)
        
        #ge.pngmethod='gxyat'
        ge.makePng(self.pltpath,background=self.background,verb=1)
        


    def xvPlot(self,ropt='',zfact=1.25):
        cmd="xv  -geometry %ix%i+50+50 %s"%(self.xsize*zfact,self.ysize*zfact,self.pltpath)
        #cmd="xv %s"%(self.pltpath)
        MF.runcmd(cmd,ropt)

    def cp2Dropbox(self,ropt='',Dropdir='~/Dropbox/TC'):
        cmd="cp %s %s/."%(self.pltpath,Dropdir)
        MF.runcmd(cmd,ropt)


class MdeckCmdLine(CmdLine):

    otags=getMd2DSsTags()
    
    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv

        self.argv=argv

        self.argopts={
            #1:['dtgopt',    'no default'],
            }

        self.defaults={
            'lsopt':'s',
            'doupdate':0,
            }

        self.options={
            'doBTstorms':    ['M',0,1,'do best track opt: 1 only bt; 2 merge bt into full track'],
            'dobt':          ['b:',0,'i','do best track opt: 1 only bt; 2 merge bt into full track'],
            'dtgopt':        ['d:',None,'a','dtgopt'],
            'override':      ['O',0,1,'override'],
            'verb':          ['V',0,1,'verb=1 is verbose'],
            'ropt':          ['N','','norun',' norun is norun'],
            'stmopt':        ['S:',None,'a','stmopt'],
            'background':    ['B:','black','a',"""set background to 'black' or 'white'"""],
            'zoomfact':      ['Z:',None,'f','zoom factor'],
            'dtg0012':       ['2',0,1,'list storm stats only'],
            'dotcvitals':    ['v',0,1,'output tcvitals'],
            'dupchk':        ['R',1,0,'do NOT remove dups from list'],
            'ls9x':          ['9',0,1,'ls stats on 9x'],
            'doanl':         ['a',0,1,'analyze stm liftime histogram'],
            'doCARQonly':    ['C',1,0,'do NOT do ops = use 9X ids always'],
            'doxv':          ['X',0,1,'do NOT do ops = use 9X ids always'],
            'docp2Dropbox':  ['D',0,1,'do cp to dropbox'],
            }

        self.purpose='''
plot trks'''
        
        self.purpose=self.purpose+'''
-t tags: %s'''%(self.otags)
        
        self.examples='''
%s 2009'''


    
#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# -- main
#

MF.sTimer('all')

CL=MdeckCmdLine(argv=sys.argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr
MF.sTimer('md2-plot')
MF.sTimer('tcdata')
tcD=TcData(stmopt=stmopt,verb=verb)
MF.dTimer('tcdata')

ddtg=6
if(dtg0012): ddtg=12

MF.sTimer('stmids')

doBT=0
if(not(dobt)):  doBT=1  # default dobt=0 doBT=1  -- replace all 
if(doCARQonly): doBT=0  # ops     dobt=0 doBT=0  -- pure ops  : picks available from CARQ (adeck) first then bdeck (?)

lstm=len(stmopt.split('.')[0])
ltt1=len(stmopt.split(','))

didold=0
ostmids=[]
dobtStms=0
# -- detect if 9X stmopt
#
if(dobt or doBT and stmopt[0] != '9'): dobtStms=1

if(lstm == 1 or lstm == 3 or mf.find(stmopt,'cc') or ltt1 > 1 ):
    # -- main stmlist
    stmids=tcD.makeStmListMdeck(stmopt,dobt=dobtStms,cnvSubbasin=0,verb=verb)
else:
    didold=1
    stmids=MakeStmList(stmopt)

nstmids=[]
for stmid in stmids:
    nstmids=nstmids+tcD.makeStmListMdeck(stmid,dobt=0)
    stmids=nstmids
MF.dTimer('stmids')

xgrads='grads'
xgrads=setXgrads(useX11=0,useStandard=0)

if(len(stmids) > 1):
    
    #print 'EEE -- multi tracks for %s.TcBtTrkPlot.PlotTrkAll() not work yet...sayounara...'
    #print 'EEE -- for stmids: ',stmids
    #sys.exit()
    
    MF.sTimer('trkplot-all-%s'%(stmopt))
    stmid=stmids[0]
    stmoptName=stmopt
    
    if(doBTstorms): stmoptName='%s-BT'%(stmopt)
    
    tP=TcBtTrkPlot(stmid,stmopt=stmoptName,tD=tcD,dobt=dobt,
                   Window=0,Bin=xgrads,
                   zoomfact=zoomfact,override=override,
                   background=background,dopbasin=1,
                   dtgopt=dtgopt,pltdir='/tmp/tctrk')

    doPlotAll=0
    if(not(tP.alreadyDone)): 
        tP.PlotTrkAll(stmids,dobt=doBTstorms,dtg0012=dtg0012,ddtg=ddtg)
        doPlotAll=1
    if(doxv and not(override)): tP.xvPlot()
    MF.dTimer('trkplot-all-%s'%(stmopt))
    if(tP.alreadyDone): 
        sys.exit()
        
    
else:
    
    MF.sTimer('trkplot')
    stmid=stmids[0]
    tP=TcBtTrkPlot(stmid,tD=tcD,dobt=dobt,
                   Window=0,Bin=xgrads,
                   zoomfact=zoomfact,override=override,
                   background=background,dopbasin=0,
                   dtgopt=dtgopt,pltdir='/tmp/tctrk')

    tP.PlotTrk(dtg0012=dtg0012,ddtg=ddtg)
    MF.dTimer('trkplot')

MF.dTimer('md2-plot')

if(doxv):         tP.xvPlot(zfact=1.0)
if(docp2Dropbox): tP.cp2Dropbox()
