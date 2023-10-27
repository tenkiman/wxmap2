#!/usr/bin/env python

from WxMAP2 import *
w2=W2()

from tc2 import TcData,TcBasin,getHemis,rumhdsp
from TCdiag import TcDiag,Oisst,getStmids,getDtgsModels,MfTrkAreaNhem,MfTrkAreaShem,MfTrkAreaGlobal
from M2 import setModel2
import AD

# -- top level vars
#
tbdir='/dat3/tc/tcanal'
prcdir='/w21/src-SAV/tcdiag'


class GaProc(MFbase):
    """ object to hang a 'ga' to pass between processing objects"""

    def __init__(self,ga=None):
        self.ga=ga


class InvHash(InvHash):

        
    def lsInv(self,
              models,
              dtgs,
              ):

            
        kk=self.hash.keys()
        for k in kk:
           imodel=k[0]
           idtg=k[1]
           if((idtg in dtgs) and
              (imodel in models)
              ):
               print k,imodel,idtg,self.hash[k]
        



        


class TcDiag(TcDiag):


    aidAliases={
        'ngf2':'gfs2',
        'nuk2':'ukm2',
        'nec2':'ecm2',
        'nng2':'ngp2',
        'ncm2':'cmc2',
        'nngc':'ngpc',
        }

    def initAD(self,dtg,model,verb=0):

        sdir='/dat3/tc/tmtrkN'

        if(self.trkSource == 'tmtrk'):
            apath="%s/%s/%s/tctrk.atcf.%s.%s.txt"%(sdir,dtg,model,dtg,model)
            spath="%s/%s/%s/tctrk.sink.%s.%s.txt"%(sdir,dtg,model,dtg,model)
        elif(self.trkSource == 'mftrk'):
            apath="%s/%s/%s/wxmap2.v010.%s.%s.*"%(sdir,dtg,model,model,dtg)
            spath=''
        else:
            print 'EEE invalid trkSource: ',trkSource
            sys.exit()

        self.aid=self.adeckaid
        if(not(mf.find(model,'rtfim'))): self.aid=model

        self.aD=AD.Adeck(apath,verb=verb,aliases=self.aidAliases)
        self.apath=apath
        
        # -- since we're only doing one aid, pull first aid in aids
        #
        if(len(self.aD.aids) > 0): self.aidname=self.aD.aids[0]

        self.aDS=AD.AdeckSink(spath,verb=self.verb)
        if(self.verb or verb):
            print 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA apath: ',apath,' self.aid: ',self.aid,' self.adeckaid ',self.adeckaid,' model: ',model
            print 'SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS spath: ',spath

        self.adstm2ids=self.aD.stm2ids


    def setTCtracker(self,stmid,aidSource=None,maxtau=168,quiet=0):

        if(aidSource != None):
            tt=aidSource.split('.')
            if(len(tt) != 2):
                print 'EEE TCdiag.setTCtracker.aidSource not well formed, should be AAAA.SSSSS but is: ',aidSource
                return(0)

            aid=tt[0]
            source=tt[1]

            self.getAidtrkFromAdss(self.dtg,stmid,sources=source,adeckaid=aid)

            if(self.ADaidtaus != None):
                self.aid=aid
                self.aidtrk=self.ADaidtrk
                self.aidtaus=self.ADaidtaus
                self.aidsource=source
                self.aidname=aid
                self.stmid=stmid

            else:
                print 'WWW TCdiag.setTCtracker no aD for source: ',source,' aid: ',aid
                return(0)
            
        else:

            # -- first source is adecks from TMtrker from w2flds...
            #
            if(self.aD != None):

                self.stmid=stmid
                self.getAidtrk(self.dtg,self.stmid)
                self.getAidcards(self.dtg,self.stmid)
                ntaus1=0
                lasttau1=0

                if(self.aidtaus != None):
                    aidtrks1=self.aidtrk
                    aidtaus1=self.aidtaus
                    ntaus1=len(self.aidtaus)
                    lasttau1=aidtaus1[-1]
                else:
                    # -- bail point 0 -- no tracker taus for aid
                    #
                    #print 'WWW bail point #0'
                    return(0)

            else:
                # -- bail point 1 -- no tracker taus for aid
                #
                print 'WWWWW forcing use of tmTrkN...'
                return(0)

            self.aidtrk=aidtrks1
            self.aidtaus=aidtaus1
            self.aidsource='tmTrkN'

            # -- bail point 2 -- no tracker taus for aid
            #
            if(len(self.aidtaus) == 0):
                print 'WWW(%s)'%(self.basename),'no final  tracker taus for dtg: ',self.dtg,' model: ',self.model,' stmid: ',self.stmid,' bailing...'
                return(0)

            # -- bail point 3 -- singleton -- rlat 0/0
            #
            if(len(self.aidtaus) == 1):
                trk0=self.aidtrk[self.aidtaus[0]]
                if( len(trk0) >= 2 and trk0[0] == 0.0 or trk0[1] == 0.0):
                    print 'WWW(%s)'%(self.basename),'singleton trk = 0,0 taus for dtg: ',self.dtg,' model: ',self.model,' stmid: ',self.stmid,' bailing...'
                return(0)


            self.diagpath="%s/diag.%s.%s.txt"%(self.pltdir,self.stmid,self.model)

            self.pyppathDiag="%s/diag.%s.pyp"%(self.pltdir,self.stmid)
            self.pyppathHtml="%s/html.%s.pyp"%(self.pltdir,self.stmid)
            self.pyppathData="%s/data.%s.pyp"%(self.pltdir,self.stmid)
            self.diagpathALL="%s/diag.all.%s.%s.txt"%(self.pltdir,self.stmid,self.model)
            self.diagpathWebALL="%s/diag.all.%s.%s.txt"%(self.webdiagdir,self.stmid,self.model)

            self.pyppathDataALL="%s/data.all.%s.pyp"%(self.pltdir,self.stmid)
            if(self.doDiagOnly):
                self.diagpath=self.diagpathALL
                self.pyppathData=self.pyppathDataALL


        # -- limit taus
        ataus=[]
        if(maxtau != None):
            for atau in self.aidtaus:
                if(atau in self.targetTaus):
                    ataus.append(atau)
            self.aidtaus=ataus

        if(self.aidtrk != None and not(quiet)):
            print 'TCTCTCTC got tracker from aidsource: %-10s'%(self.aidsource),' model: %-6s'%(self.model),' stmid: ',self.stmid,' ntaus: %3d'%(len(self.aidtaus)),' lasttau: %3d'%(self.aidtaus[-1])

        self.aidMotion={}

        # -- get the motion based on the next tau
        #
        ntaus=len(self.aidtaus)

        for tau in self.aidtaus:
            
            # -- get track for spd/dir calc
            taup0=tau
            (latcp0,loncp0,vmaxcp0,pmincp0)=self.aidtrk[taup0]

            np=self.aidtaus.index(tau)

            # -- check if at end of tau...
            #
            if(np == ntaus-1):
                np=np-1
                taup0=self.aidtaus[np]
                (latcp0,loncp0,vmaxcp0,pmincp0)=self.aidtrk[taup0]

            # -- get track at next tau
            #
            np1=np+1
            taup1=self.aidtaus[np1]
            (latcp1,loncp1,vmaxcp1,pmincp1)=self.aidtrk[taup1]

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

        return(1)


    def chKOutput(self,iV,dstmids=None,aidSource=None,rc=None,quiet=0):


        inv={}

        if(dstmids == None):
            inv='dstmids=None'
            if(rc != None): inv=inv+rc
            iV.hash[self.model,self.dtg]=inv
            iV.put()
            return(-2)

        if(aidSource != None and len(aidSource.split('.')) == 2):
            self.aidsource=aidSource.split('.')[1]
            self.aid=aidSource.split('.')[0]
            
        sizStmid=[]
        for stmid in dstmids:
            (rc,dtime,dpath)=self.setDiagPath(stmid,tbdir=tbdir)
            sizStmid.append(rc)
            if(rc == -999):
                rc=('notrun yet')
                
            inv[stmid]=rc

        if(len(dstmids) == 0):
            inv=('no tcs or no tcs in TCdiag.tcdiagBasins')
            print 'WWW(chKoutput): ',inv
            status=-2

        status=0
        if(max(sizStmid) <= 0): status=-1

        if(status == -1):
            print """WWW TCdiagN.setDiagPath: hasn't been run yet..."""
        else:
            if(not(quiet)):
                print
                print """IIIIIIIIIIII -- already run; use -O(override=1)  or -o(TDoverride=1) to override"""
                print

        iV.hash[self.model,self.dtg]=inv
        iV.put()

        return(status)
            


    def thinOutputByTaus(self):

        tdir="%s/%s/%s"%(tbdir,self.dtg,self.model)

        datpaths=glob.glob("%s/*dat"%(tdir))

        taus=[]
        dpaths={}
        for dat in datpaths:
            tau=dat.split('.')[-2][1:]
            tau=int(tau)
            taus.append(tau)
            dpaths[tau]=dat
            
            
        thinTaus=range(6,126+1,12)

        nkill=0
        for thintau in thinTaus:
            if(thintau in taus):
                dpath=dpaths[thintau]
                cmd="rm %s"%(dpath)
                mf.runcmd(cmd,ropt)
                nkill=nkill+1
                                
        
        print 'III(TcDiag.thinOutputByTaus) nkill: ',nkill
        return(nkill)
            




class TcFldsDiag(f77GridOutput,W2areas):

    def __init__(self,
                 dtg,
                 model,
                 ctlpath,
                 dstmids,
                 area=None,
                 dlon=None,dlat=None,
                 taus=None,
                 tunits='hr',
                 vars=None,
                 doregrid=1,
                 tbdir=tbdir,
                 doLogger=0,
                 Quiet=0,
                 verb=0,
                 doByTau=1,
                 setDxDyPrec=1,
                 dols=0,
                 ):


        self.m2=setModel2(model)

        self.dstmids=dstmids
        self.doregrid=doregrid

        self.GAdoLogger=doLogger
        self.GAQuiet=Quiet
        self.verb=verb
        self.doByTau=doByTau
        self.setDxDyPrec=setDxDyPrec
        
        cP=ctlProps(ctlpath)

        if(dlon == None):
            dx=cP.dlon
        else:
            dx=dlon
            
        if(dlat == None):
            dy=cP.dlat
        else:
            dy=dlat

        
        self.tcB=TcBasin()

        if(area == None): self.setFldGridArea()

        if(self.area == None): print "EEE error in getW2Area for area: ",area ; sys.exit()

        lonW=self.area.lonW
        lonE=self.area.lonE
        latS=self.area.latS
        latN=self.area.latN

        if(taus == None):
            self.btau=0
            self.etau=120
            self.dtau=6
            self.extaus=[132,144,156,168]
            taus=range(self.btau,self.etau+1,self.dtau)+self.extaus
            #taus=[0,6]
            
        else:
            self.btau=taus[0]
            self.etau=taus[-1]
            if(len(taus) > 1):
                self.dtau=taus[1]-taus[0]
            else:
                self.dtau=6
                
        self.tunits=tunits
        self.taus=taus
            
        self.dtg=dtg
        self.model=model
        self.ctlpath=ctlpath
        self.tbdir=tbdir

        self.setCtl(ctlpath=ctlpath,tbdir=tbdir,dols=dols)
        if(self.status == 0): return
        
        self.tdirsst="%s/%s/oisst"%(tbdir,self.dtg)
        if(not(dols)): MF.ChkDir(self.tdirsst,'mk')

        sstfile='oisst.%s.%s.dat'%(self.dtg,self.areaname)
        self.sstdpath="%s/%s"%(self.tdirsst,sstfile)

        self.initVars()

        filename="%s.%s.%s"%(self.model,self.dtg,self.areaname)
                
        self.setOutput(name=filename)

        sstfile='oisst.%s.%s.dat'%(self.dtg,self.areaname)
        self.sstdpath="%s/%s"%(self.tdirsst,sstfile)

        self.getDpaths(verb=verb)


    def initVars(self,
                 varSsfc=None,
                 varSua=None,
                 undef=-1e20):
        
        if(self.area == None): self.area=W2areaGlobal()

        if(varSsfc == None):
            
            self.varSsfc=['uas:uas:(uas(t-TM1)*TFM1 + uas(t+TP1)*TFP1):0:-999:-999:uas [m/s]',
                          'vas:vas:(vas(t-TM1)*TFM1 + vas(t+TP1)*TFP1):0:-999:-999:vas [m/s]',
                          'psl:(psl*1.00):(psl(t-TM1)*TFM1 + psl(t+TP1)*TFP1):0:-999:-999:psl [mb]',
                          'prw:(prw*1.00):(prw(t-TM1)*TFM1 + prw(t+TP1)*TFP1):0:-999:-999:psl [mb]',
                          'pr:getprvar:0:-999:-999:pr 6-h rate [mm/day]',
                          'vrt925:(hcurl(ua,va)*1e5):925:-999:-999:rel vort 925 [*1e5 /s]',
                          'vrt850:(hcurl(ua,va)*1e5):850:-999:-999:rel vort 850 [*1e5 /s]',
                          'vrt700:(hcurl(ua,va)*1e5):700:-999:-999:rel vort 700 [*1e5 /s]',
                          'zthklo:getexpr:0:-999:-999:600-900 thick [m]',
                          'zthkup:getexpr:0:-999:-999:300-600 thick [m]',
                          'z900:getexpr:0:-999:-999:900 [m]',
                          'z850:getexpr:0:-999:-999:850 [m]',
                          'z800:getexpr:0:-999:-999:800 [m]',
                          'z750:getexpr:0:-999:-999:750 [m]',
                          'z700:getexpr:0:-999:-999:700 [m]',
                          'z650:getexpr:0:-999:-999:650 [m]',
                          'z600:getexpr:0:-999:-999:600 [m]',
                          'z550:getexpr:0:-999:-999:550 [m]',
                          'z500:getexpr:0:-999:-999:500 [m]',
                          'z450:getexpr:0:-999:-999:450 [m]',
                          'z400:getexpr:0:-999:-999:400 [m]',
                          'z350:getexpr:0:-999:-999:350 [m]',
                          'z300:getexpr:0:-999:-999:300 [m]',
                          ]

        if(varSua == None):
            
            self.varSua=[]

            self.varSuavar=['ua','va']
            self.varSl=[850,200]

            self.varSuavar=['ua','va','hur','ta','zg']
            self.varSl=[1000,850,700,500,400,300,250,200,150,100]
            
            self.varSu={
                'ua':('ua','ua [m/s]'),
                'va':('va','va [m/s]'),
                'hur':('hur','''hur [%]'''),
                'ta':('ta','ta [K]'),
                'zg':('zg','zg [m]'),
                }
            

            for var in self.varSuavar:
                for lev in self.varSl:
                    expr=self.varSu[var][0]
                    desc=self.varSu[var][1]
                    vtexpr="(%s(t-TM1)*TFM1 + %s(t+TP1)*TFP1)"%(var,var)
                    self.varSua.append('%s:%s:%s:%d:-999:-999:%s'%(var,expr,vtexpr,lev,desc))


        self.dpaths={}
        self.vars=[]
        
        for var in self.varSsfc:
            self.vars.append(var)

        for var in self.varSua:
            self.vars.append(var)
            

        self.undef=undef
        
        if(self.taus == None):
            self.btau=0
            self.etau=120
            self.dtau=6
            self.tunits='hr'
            self.taus=range(self.btau,self.etau+1,self.dtau)

        aa=self.area

        cdx="%f"%(aa.dx)
        cdy="%f"%(aa.dy)
        if(self.setDxDyPrec):
            cdx="%7.3f"%(aa.dx)
            cdy="%7.3f"%(aa.dy)
            
        
        if(self.remethod == ''):
            self.reargs="%d,%s,%f,%s,%d,%s,%f,%s"%(aa.ni,self.rexopt,aa.lonW,cdx,aa.nj,self.reyopt,aa.latS,cdy)
        else:
            self.reargs="%d,%s,%f,%s,%d,%s,%f,%s,%s"%(aa.ni,self.rexopt,aa.lonW,cdx,aa.nj,self.reyopt,aa.latS,cdy,self.remethod)


        if(not(self.doregrid)): self.reargs=None


    def makeOisst(self,override=0):

        if(not(hasattr(self,'ga')) or not(hasattr(self,'ge')) or not(hasattr(self,'dtg')) ):
            print 'EEE makeOisst, need to run makeFldInput first...'
            sys.exit()

        self.ga.oisstOpened=0

        if(MF.ChkPath(self.sstdpath,verb=1) and not(override)): return

        MF.sTimer(tag='sst')
        ssT=Oisst(self.ga,self.ge,self.dtg,verb=self.verb,area=self.area,dpath=self.sstdpath,reargs=self.reargs,override=override)
        MF.dTimer(tag='sst')

        self.ssT=ssT

        # -- the first file open is the met fields, make it the default
        #
        self.ga('set dfile 1')
        self.ga('set z 1')

    def setFldGridArea(self,ropt='',override=0):

        self.hemigrid=getHemis(self.dstmids)
        if(self.hemigrid == 'nhem'):  aa=MfTrkAreaNhem()
        if(self.hemigrid == 'shem'):  aa=MfTrkAreaShem()
        if(self.hemigrid == 'global'):  aa=MfTrkAreaGlobal()

        self.areaname=self.hemigrid

        self.area=aa

        # override to test with more general code
        #
        #self.area=W2areaGlobal()
        
        aa=self.area

        if(self.remethod == ''):
            self.reargs="%d,%s,%f,%f,%d,%s,%f,%f"%(aa.ni,self.rexopt,aa.lonW,aa.dx,aa.nj,self.reyopt,aa.latS,aa.dy)
        else:
            self.reargs="%d,%s,%f,%f,%d,%s,%f,%f,%s"%(aa.ni,self.rexopt,aa.lonW,aa.dx,aa.nj,self.reyopt,aa.latS,aa.dy,self.remethod)

        if(not(self.doregrid)): self.reargs=None


    def makeFldInputGA(self,gaP):

        # -- do grads: 1) open files; 2) get field data
        #
        xgrads='grads2'

        # -- decorate the GaProc (gaP) object
        #
        if(gaP.ga == None):
            print 'MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM -- making gaP.ga'
            #from ga2 import setGA
            #ga=setGA(Bin=xgrads,doLogger=self.GAdoLogger,Quiet=self.GAQuiet)

            import GA
            ga=GA.setGA2(Bin=xgrads,doLogger=self.GAdoLogger,Quiet=self.GAQuiet)
            gaP.ga=ga
            
        
        self.ga                      =gaP.ga
        
        # -- do file open via ge so getFileMeta works...
        print 'OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO -- open: ',self.ctlpath

        self.ga.ge.fh                =self.ga.open(self.ctlpath)
        self.ga.ge.getFileMeta()
        self.ge                      =self.ga.ge
        gaP.ge                       =self.ga.ge
        

    def reinitGA(self,gaP):
        gaP.ge.reinit()
            

    def destructGA(self):
        if(hasattr(self,'ga')):
            print 'QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ ga'
            self.ga.__del__()
            
        if(hasattr(self,'ga2')):
            print 'QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ ga2'
            self.ga2.__del__()
        

    def thinDpathsByTaus(self,verb=0,ropt=''):

        thinTaus=range(6,126+1,12)
        
        for thintau in thinTaus:
            if(thintau in self.taus):
                (rc,path)=self.dpaths[thintau]
                cmd="rm %s"%(path)
                mf.runcmd(cmd,ropt)
                                

    def fldDiagTcGen(self,basin,
                     gentau=120,
                     dogendtg=0,
                     dowindow=0,
                     gaopt='-g 1024x768',
                     doxv=0,
                     pngmethod='printim',
                     verb=0,
                     prOB=15.0,
                     undef=-999.,
                     quiet=0,
                     ):

        from TCtrk import getBasinLatLons
        

        ge=ga.ge
        (ge.lat1,ge.lat2,ge.lon1,ge.lon2)=getBasinLatLons(basin)
        ge.setLatLon()

        if(hasattr(self,'bdtg')):
            bdtg=self.bdtg
        else:
            if(dogendtg):
                bdtg=mf.dtginc(self.dtg,-gentau)
            else:
                bdtg=self.dtg
            
        
        ge.setTimebyDtgTau(bdtg,gentau)
	
        # -- get meta data to check if there's a prc...decorate both ge and ga
        #
        
        ge.getFileMeta(ga)

        if(verb):
            ga('q file')
            ga('q dims')
            print 'vars: ',ge.vars


        # --- get model specific expr for pr in mm/day
        #

        if(hasattr(self.m2,'setprvar')):
            prvar=self.m2.setprvar(self.dtg,gentau)
        else:
            prvar=self.m2.modelprvar

        if(gentau == 0 and hasattr(self.m2,'modelprvar00')): prvar=self.m2.modelprvar00
        if(gentau == 6 and hasattr(self.m2,'modelprvar06')): prvar=self.m2.modelprvar06

        prvar=prvar.split('=')[1]


        # -- check if there's a prc ...
        #

        if('prc' in ge.vars):
            prvarc=prvar.replace('pr','prc')
        else:
            prvarc="(const(pr,-999.0,-a))"

        
        prvar=prvar.replace("'","")
        prvarc=prvarc.replace("'","")

        ga.dvar.re2('pc',prvarc,1.0,1.0)
        ga.dvar.re2('p',prvar,1.0,1.0)

        pca=ga.get.aave('pc',ge)
        pa=ga.get.aave('p',ge)

        pcao=ga.get.aave('maskout(pc,-ls.2(t=1))',ge)
        pao=ga.get.aave('maskout(p,-ls.2(t=1))',ge)

        if(verb):
            print 'pppppppppppppp pcao: ',pcao
            print 'pppppppppppppp  pao: ',pao

        # -- bad pr for fim8 2009080412...
        #
        if(pao  > prOB or pao  == 0): pao=undef
        if(pcao > prOB or pcao == 0): pcao=undef
        
        if(pcao > 0.0 and pao > 0.0):
            ratioC2T=pcao/pao
        else:
            ratioC2T=undef
            if(pcao < 0.0): pcao=undef

        if(pao < 0.0): pao=undef

        if(verb):
            print 'RRRRRRRRRRRRRRRRRRRRRRRRR ',ratioC2T,pcao,pao

        rc=(ratioC2T,pcao,pao)
        return(rc)
        
        #ga.ls()

        

        
        
        
#----------------------------------------------------------------------------------------------------
#

class MyCmdLine(CmdLine):

    # -- set up here to put in an object
    #
    
    btau06=0
    etau06=120
    dtau06=6
    
    btau12=etau06+12
    etau12=168
    dtau12=12

    ttaus=range(btau06,etau06+1,dtau06)+range(btau12,etau12+1,dtau12)
    
    gaopt='-g 1024x768'

    def __init__(self,argv=sys.argv):



        if(argv == None): argv=sys.argv
        
        self.argv=argv
        self.argopts={
            1:['dtgopt',  'run dtgs'],
            2:['modelopt',    'model|model1,model2|all|allgen'],
            }

        self.defaults={
            'doupdate':0,
            'doga':1,
            }

        self.options={
            'override':         ['O',0,1,'override'],
            'TDoverride':       ['o',0,1,'override just running the '],
            'verb':             ['V',0,1,'verb=1 is verbose'],
            'quiet':            ['q',1,0,' turn OFF running GA in quiet mode'],
            'ropt':             ['N','','norun',' norun is norun'],
            'doTcFlds':         ['F',0,1,'''doTcFlds -- make f77 input files for lsdiags.x only'''],
            'dowindow':         ['w',0,1,'1 - dowindow in GA.setGA()'],
            'dowebserver':      ['W',0,1,'1 - dowebserver=1 write to webserver for plotonly '],
            'doxv':             ['X',0,1,'1 - xv the plot'],
            'doplot':           ['P',0,1,'1 - make diag plots'],
            'aidSource':        ['T:',None,'a','aid.source to pull adeck from the adeck_source_year_pypdb'],
            'domandonly':       ['m',0,1,'DO        reduced levels only (sfc,850,500,200)'],
            'doStndOnly':       ['s',1,0,'do NOT do SHIPS levels (1000,850,700,500,400,300,250,200,150,100)'],
            'stmopt':           ['S:',None,'a','stmopt'],
            'getpYp':           ['Y',0,1,'1 - get from pyp'],
            'doclean':          ['K',0,1,'clean off files < dtgopt'],
            'dohtmlvars':       ['H',0,1,'do html for individual models'],
            'dothin':           ['t',0,1,'dothin -- reduce # of taus .dat files to reduce storage'],
            'lsInv':            ['I',0,1,'do html for individual models'],
            'dols':             ['l',0,1,'do ls of TCs...'],
            'ndayback':         ['n:',25,'i','ndays back to do inventory from current dtg...'],
            'doTrkPlot':        ['R',0,1,'doTrkPlot...'],
            'zoomfact':         ['Z:',None,'a','zoomfact'],
            'doALL':            ['A',0,1,'do all processing for a dtg'],
            'doDiagOnly':       ['D',0,1,'do only diagfile processing'],
            'trkSource':        ['M','tmtrk','mftrk','tm|mftrk for trkSource'],
            'doPr':             ['p',0,1,'calc tcgen precip status'],
            }

        self.purpose='''
purpose -- generate TC large-scale 'diag' file for lgem/ships/stips intensity models
 '''
        self.examples='''
%s 2010052500 gfs2
'''


def errAD(option,opt=None):

    if(option == 'tstmids'):
        print 'EEE # of tstmids = 0 :: no stms to verify...stmopt: ',stmopt
    elif(option == 'tstms'):
        print 'EEE # of tstms from stmopt: ',stmopt,' = 0 :: no stms to verify...'
    else:
        print 'Stopping in errAD: ',option

    sys.exit()


def runLsDiag(mfT,tG,ropt='',override=0):
    """ run the fortran using the TcFldsDiag and TcDiag objects
    """
    if(not(mfT.sstDone and mfT.meteoDone)):
        print '''EEE(runLsDiag):  mfT.sstDone and mfT.meteoDone != 1'''
        return(0)

    sstpath=mfT.sstdpath
    metapath=mfT.mpath
    tcmetapath=tG.mpath
    outpath=tG.finalDiagPath
    prcdir=tG.prcdir
    cmd="%s/lsdiag.x %s %s %s %s"%(prcdir,metapath,tcmetapath,sstpath,outpath)
    MF.runcmd(cmd,ropt)

    




#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
# main
#

MF.sTimer(tag='all')

argv=sys.argv
CL=MyCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

#if(doALL): doAllPrc(CL)

(dtgs,models)=getDtgsModels(CL,dtgopt,modelopt)

tcB=TcBasin()

# -- grads processing object
#
gaP=GaProc()

# -- inventory object
#
if(not(dothin)):
    iV=InvHash(dbname='invTcdiag',
               tbdir=tbdir,
               override=doclean)

    if(lsInv):
        iV.lsInv(models,dtgs)
        sys.exit()



for dtg in dtgs:

    for model in models:

        # -- first run mf|tmtrkN to get trackers
        #
        dotrkSource=0
        if(dotrkSource):
            if(trkSource == 'tmtrk'):    cmd="/w21/prc/tctrk/w2.tc.tmtrkN.py %s %s"%(dtg,model)
            elif(trkSource == 'mftrk'):  cmd="/w21/prc/tctrk/w2.tc.mftrkN.py %s %s"%(dtg,model)
            if(not(dols) and not(dothin) and not(doPr)):
                mf.runcmd(cmd,ropt)
            

        dobail=0
        if(ropt == 'norun'): dobail=0
        MF.sTimer('tcdiag')
        tG=TcDiag(dtg,model,
                  ttaus=CL.ttaus,
                  doplot=doplot,
                  gaopt=CL.gaopt,
                  domandonly=domandonly,
                  doStndOnly=doStndOnly,
                  doDiagOnly=doDiagOnly,
                  dols=dols,
                  dowebserver=dowebserver,
                  trkSource=trkSource,
                  dobail=dobail,
                  doga=0,verb=verb)

        tG.prcdir=prcdir

        MF.dTimer('tcdiag')

        if(dothin):
            tG.thinOutputByTaus()
            continue

        # -- tcs
        #
        tG.setTCs()
        tstmids=getStmids(dtg,tG.stmids,tG.adstm2ids,stmopt=stmopt,dols=0)

        # -- if no TCs or no trackers...continue
        #
        if(len(tG.adstm2ids) == 0 or len(tG.stmids) == 0):
            print 'WWW tmtrkN not run yet...or no TCs...continue...'
            rc=tG.chKOutput(iV,dstmids=None,aidSource=aidSource,rc="noTCs or %s not run yet"%(trkSource))
            continue

        # -- get storms and make sure ctlpath there...
        #
        dstmids=tG.getTCdiagStorms(tstmids)

        ctlpath=tG.ctlpath

        # -- check if done
        #
        rc=tG.chKOutput(iV,dstmids,aidSource=aidSource)

        if(rc == -2):
            print '0000: no tcs or no tcs in TCdiag.tcdiagBasins'
            continue
        elif( (rc == 0 or dols) and not(override) and not(TDoverride) ):
            continue

        if(ropt == 'norun'):  continue

        # -- check if a data tau 0
        #
        if(not(0 in tG.targetTaus)):
            print 'EEE no data tau0...continue...',ctlpath
            continue

        if(ctlpath != None and not(dothin)):
            print 'PPPPPPPPPPPPPPPPP process  dtg: ',dtg," model:  %-10s"%(model)," targetTaus: %3d-%-3d"%(tG.targetTaus[0],tG.targetTaus[-1]),' ctlpath: ',ctlpath


        # -- input fields
        #
        MF.sTimer('tcfldsdiag:%s:%s'%(dtg,model))

        # -- set taus based on available data, not ttaus
        #
        mfT=TcFldsDiag(dtg,model,ctlpath,
                       taus=tG.targetTaus,
                       dstmids=dstmids,
                       dlat=0.5,
                       dlon=0.5,
                       Quiet=quiet,
                       dols=dols,
                       )


        if(mfT.status == 0):
            print 'mfT.status = 0'
            continue

        if(dols):
            for stmid in dstmids:
                (rc,dtime,dpath)=tG.setDiagPath(stmid,tdir=mfT.tdir)
                tG.lsDiag(stmid,dobail=0)
            continue

        if(not(mfT.sstDone and mfT.meteoDone) or override):

            MF.sTimer('fldinput:%s:%s'%(dtg,model))
            # -- start grads; decoreate the tG object (TcDiag()); open fld ctlpath
            mfT.makeFldInputGA(gaP)
            # -- SST
            mfT.makeOisst(override=override)
            # -- meteo
            mfT.makeFldInput(override=override,verb=verb,doconst0=0)
            # -- get the data status
            mfT.getDpaths(verb=1)
            # -- reinit ga
            mfT.reinitGA(gaP)
            MF.dTimer('fldinput:%s:%s'%(dtg,model))

        MF.dTimer('tcfldsdiag:%s:%s'%(dtg,model))

        for stmid in dstmids:

            # -- get tctracker and make tc meta file -- this sets the aid and source for setDiagPath
            #
            if(tG.setTCtracker(stmid,aidSource,quiet=0) == 0): continue
            rc=tG.makeTCmeta(tdir=mfT.tdir)

            # -- set diagfile output path
            #
            (rc,dtime,dpath)=tG.setDiagPath(stmid,tdir=mfT.tdir)

            # -- run fortran
            #
            MF.sTimer('lsdiag.x:%s:%s:%s'%(dtg,model,stmid))
            runLsDiag(mfT,tG)
            MF.dTimer('lsdiag.x:%s:%s:%s'%(dtg,model,stmid))

        # -- load inventory
        #
        rc=tG.chKOutput(iV,dstmids,aidSource=aidSource,quiet=1)
        
MF.dTimer(tag='all')
