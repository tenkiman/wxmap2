#!/usr/bin/env python

from WxMAP2 import *
w2=W2()                               # w2 obj with vars/methods

from cm2 import ClimoFld,ClimoFldWMO  # class pointing to climo data
from ga2 import setGA                 # grads class
from m2 import EnsModel               # class for ens of model runs


class WmoStats(MFbase):

    wmoversion='0.1 -- comp to ncep vsdb'

    def __init__(self,area,vdtg,var,lev,tau,
                 doAnom=1):

        self.ggdx=wmo.ggdx
        self.ggmethod=wmo.method
        self.ggshfilt=wmo.ggshfilt
        self.ggshfiltNwaves=wmo.ggshfiltNwaves

        self.curdtg=mf.dtg('dtg.phm')
        self.wmoversion=self.wmoversion

        self.area=area
        self.vdtg=vdtg
        self.var=var
        self.lev=lev
        self.tau=tau
        self.doAnom=doAnom

        self.rmse=None
        self.rmseT=None
        self.rmseE=None
        self.rmseP=None
        
        self.meane=None
        
        self.acAnFc=None
        self.acAnFcwmo=None

        self.corrAnFc=None

        self.meanAn=None
        self.meanFc=None
        self.meanCl=None
        
        self.sigmaAn=None
        self.sigmaFc=None
        self.sigmaCl=None

        self.sigmaAnAnom=None
        self.sigmaFcAnom=None

    def makeVectorStats(self,ssu,ssv):

        #ssu.ls()
        #ssv.ls()

        Ninv=ssu.sumCoslat

        mse=(ssu.sum2Df + ssv.sum2Df)/Ninv
        
        sig2a=(ssu.sum2An + ssv.sum2An)/Ninv
        sig2f=(ssu.sum2Fc + ssv.sum2Fc)/Ninv

        sig2aCl=(ssu.sum2AnCl + ssv.sum2AnCl)/Ninv
        sig2fCl=(ssu.sum2FcCl + ssv.sum2FcCl)/Ninv

        siga=sqrt(sig2a)
        sigf=sqrt(sig2f)
        
        self.rmse=sqrt(mse)
        self.bias=sqrt( (ssu.meanAn-ssu.meanFc)*(ssu.meanAn-ssu.meanFc) + (ssv.meanAn-ssv.meanFc)*(ssv.meanAn-ssv.meanFc) )

        sig2aCL=(ssu.sum2AnCl + ssv.sum2AnCl)/Ninv
        sig2fCL=(ssu.sum2FcCl + ssv.sum2FcCl)/Ninv

        sigaCl=sqrt(sig2aCl)
        sigfCl=sqrt(sig2fCl)

        # -- wmo corr
        #
        corr=( (ssu.sum2AnFc + ssv.sum2AnFc)/Ninv ) / (siga*sigf)
        corrCl=( (ssu.sum2AnFcCl + ssv.sum2AnFcCl)/Ninv ) / (sigaCl*sigfCl)


        mseP= sig2f+sig2a - 2.0*sigf*siga*corr
        mseE= (ssu.meanFc - ssu.meanAn)*(ssu.meanFc - ssu.meanAn) +  (ssv.meanFc - ssv.meanAn)*(ssv.meanFc - ssv.meanAn) 

        mseT=mseP+mseE
        
        self.rmseT=sqrt(mseT)
        self.rmseE=sqrt(mseE)
        self.rmseP=sqrt(mseP)

        print
        print 'VVVV  area: %8s'%(ssu.area),' vdtg: ',ssu.vdtg,' tau: ',ssu.tau
        print 'VVuu UsigA: %8.4g   UsigF: %8.4g '%(ssu.sigmaAn,ssu.sigmaFc)
        print 'VVvv VsigA: %8.4g   VsigF: %8.4g '%(ssv.sigmaAn,ssv.sigmaFc)
        print 'VVVV  siga: %8.4g    sigf: %8.4g   rmse: %8.4g  bias: %8.4g'%(siga,sigf,self.rmse,self.bias)
        print 'VVVV  corr: %8.4g  corrCL: %8.4g'%(corr,corrCl)
        print 'VVVV rmseT: %8.4g   rmseP: %8.4g  rmseE: %8.4g'%(self.rmseT,self.rmseP,self.rmseE)
        print

        
        #self.hashvalue=[siga,sigf,corr,sigaCl,sigfCl,corrCl,self.rmse,self.bias]
        #self.hashvaluedesc=['sigmaAn','sigmaFc','vectorCorr','sigmaAnCl','sigmaFcCl','vectorCorrCl','rmse','bias']

        

    def makeStats(self,ga,wmo):
        """
         strictly by the wmo red book, ii.7-36 - ii.7-38
         and grads using scorr
        """
        from math import sqrt
        
        wmo.getAreaLatLon(self.area)

        scg=ga.get.asumg('coslat',wmo)

        s1d=ga.get.asumg('vd*coslat',wmo)
        s2d=ga.get.asumg('vd*vd*coslat',wmo)

        s1aa=ga.get.asumg('vaa*coslat',wmo)
        s2aa=ga.get.asumg('vaa*vaa*coslat',wmo)

        s1af=ga.get.asumg('vfa*coslat',wmo)
        s2af=ga.get.asumg('vfa*vfa*coslat',wmo)

        s1a=ga.get.asumg('va*coslat',wmo)
        s2a=ga.get.asumg('va*va*coslat',wmo)

        s1f=ga.get.asumg('vf*coslat',wmo)
        s2f=ga.get.asumg('vf*vf*coslat',wmo)

        s1c=ga.get.asumg('vc*coslat',wmo)
        s2c=ga.get.asumg('vc*vc*coslat',wmo)

        maf=s1af/scg
        maa=s1aa/scg

        mf=s1f/scg
        ma=s1a/scg
        mc=s1c/scg

        try:
            sigf=sqrt(s2f/scg - mf*mf)
        except:
            sigf=None

        try:
            siga=sqrt(s2a/scg - ma*ma)
        except:
            siga=None

        try:
            sigc=sqrt(s2c/scg - mc*mc)
        except:
            sigc=None

        try:
            sigaf=sqrt(s2af/scg - maf*maf)
        except:
            sigaf=None

        try:
            sigaa=sqrt(s2aa/scg - maa*maa)
        except:
            sigaa=None

        
        s12ac=ga.get.asumg("(vfa-%g)*(vaa-%g)*coslat"%(maf,maa),wmo)
        s1ac=sqrt(ga.get.asumg("(vfa-%g)*(vfa-%g)*coslat"%(maf,maf),wmo))
        s2ac=sqrt(ga.get.asumg("(vaa-%g)*(vaa-%g)*coslat"%(maa,maa),wmo))

        self.sumCoslat=scg

        # -- sums for vector calcs
        #
        self.sum2An=ga.get.asumg('(((va-%g)*(va-%g))*coslat)'%(ma,ma),wmo)
        self.sum2Fc=ga.get.asumg('(((vf-%g)*(vf-%g))*coslat)'%(mf,mf),wmo)
        self.sum2AnFc=ga.get.asumg('(((va-%g)*(vf-%g))*coslat)'%(ma,mf),wmo)
        
        self.sum2AnCl=ga.get.asumg('(((vaa-%g)*(vaa-%g))*coslat)'%(maa,maa),wmo)
        self.sum2FcCl=ga.get.asumg('(((vfa-%g)*(vfa-%g))*coslat)'%(maf,maf),wmo)
        self.sum2AnFcCl=ga.get.asumg('(((vaa-%g)*(vfa-%g))*coslat)'%(maa,maf),wmo)
        
        self.corrAnFc=ga.get.scorr('va-%g'%(ma),'vf-%g'%(mf),wmo)
        self.corrAnFcwmo=( self.sum2AnFc/scg ) / (siga*sigf)

        self.acAnFc=ga.get.scorr('vaa','vfa',wmo)
        self.acAnFcwmo=s12ac/(s1ac*s2ac)

        self.rmse=sqrt(s2d/scg)
        self.meane=s1d/scg

        self.sum2Df=s2d
        
        self.meanAn=ma
        self.meanFc=mf
        self.meanCl=mc

        self.sigmaAn=siga
        self.sigmaFc=sigf
        self.sigmaCl=sigc

        self.sigmaAnAnom=sigaa
        self.sigmaFcAnom=sigaf

        self.modelAn=ga.modelAn.model
        self.modelFc=ga.modelFc.model

        sig2a=(self.sum2An)/scg
        sig2f=(self.sum2Fc)/scg

        # -- vsdb breakdown of mse into P (pattern) and E (mean)
        #
        mseP= sig2f+sig2a - 2.0*sigf*siga*self.corrAnFcwmo
        mseE= (self.meanFc - self.meanAn)*(self.meanFc - self.meanAn)
        mseT=mseP+mseE

        if(mseT < 0.001): mseT=0.0
        if(mseE < 0.001): mseE=0.0
        if(mseP < 0.001): mseP=0.0
        
        self.rmseT=sqrt(mseT)
        self.rmseE=sqrt(mseE)
        self.rmseP=sqrt(mseP)

        #- output hashes...
        #
        self.hashkey=(self.modelFc,self.vdtg,self.area,self.var,self.tau,self.lev)
        self.hashvalue=[self.acAnFc,self.rmse,self.meane,self.corrAnFc,self.sigmaAn,self.sigmaFc,self.sigmaCl]
        self.hashvaluedesc=['acAnFc','rmse','meane','corrAnFc','sigmaAn','sigmaFc','sigmaCl']


    

class WmoAreaGrid():

    ggdx=2.5
    ggdy=2.5

    # -- new standard
    
    ggdx=1.5
    ggdy=1.5

    globalgrid='pole'
    
    # -- new standard has a pole point
    #globalgrid='nopole'
    #method='bl' # 0.867263
    # --use box averaging because wmo grid coarser than models circa 2000-2010
    #
    method='ba' # 0.869863
    
    xlinear=1
    ylinear=1

    # global grid (gg) properties
    
    ggdlat=180.0
    ggdlon=360.0
    
    gglat1=-90.0
    gglat2=gglat1+ggdlat
    gglon1=0.0
    gglon2=gglon1+ggdlon

    areas={
        'nhem':[20,90,0,360],
        'shem':[-90,-20,0,360],
        'tropics':[-20,20,0,360],
        }

    ggshfilt=0
    ggshfiltNwaves=20
    
    def __init__(self,globalgrid=globalgrid,method=method):


        if(self.globalgrid == 'nopole'):
            self.ni=int(self.ggdlon/self.ggdx + 0.5)
            self.nj=int(self.ggdlat/self.ggdy + 0.5)
            self.gglat11=self.gglat1+self.ggdy*0.5
            self.gglon11=self.gglon1+self.ggdx*0.5
        else:
            self.ni=int(self.ggdlon/self.ggdx + 0.5)
            self.nj=int(self.ggdlat/self.ggdy + 0.5)+1
            self.gglat11=self.gglat1
            self.gglon11=self.gglon1

        rexopt='linear'
        reyopt='linear'

        self.method=method
        self.reargs="%d,%s,%f,%f,%d,%s,%f,%f,%s"%(self.ni,rexopt,self.gglon11,self.ggdx,self.nj,reyopt,self.gglat11,self.ggdy,self.method)


    def getAreaLatLon(self,area='nhem'):
            
        self.lat1=self.areas[area][0]
        self.lat2=self.areas[area][1]
        self.lon1=self.areas[area][2]
        self.lon2=self.areas[area][3]



def makeIvar(ivar,tau,fh=1):
    expr="%s.%d(ens=f%03d)"%(ivar,fh,tau)
    return(expr)
    
    
def makeCoslatWght(ga,ovar,wmo,fh=1):
    from math import pi
    expr="(cos(lat.%d(t=1)*%g/%f))"%(fh,pi,wmo.ggdlat)
    ga.dvar.regrid(ovar,expr,wmo.reargs)
    return(1)

    
def makedSinlatWght(ga,wmo,fh=1):
    from math import pi
    dyh=wmo.ggdx*0.5
    ggdlat=wmo.ggdlat
    fh=ga.nfAn
    exprhi="(sin((lat.%d(t=1)+%g)*%g/%f))"%(fh,dyh,pi,ggdlat)
    exprlo="(sin((lat.%d(t=1)-%g)*%g/%f))"%(fh,dyh,pi,ggdlat)
    ga.dvar.regrid('sinhi',exprhi,wmo.reargs)
    ga.dvar.regrid('sinlo',exprlo,wmo.reargs)
    ga.dvar.var('dsinlat','abs(sinhi-sinlo)*%g'%(wmo.ggdy))
    return(1)

    
def makeAnfld(ga,ovar,ivar,tau,wmo,doshfilt=0):
    
    ga.dvar.regrid(ovar,makeIvar(ivar,tau,ga.nfAn),wmo.reargs)
    if(ga.get.stat(ovar).nvalid == 0):
        print 'EEEaaaaaaaaaaaaa no fields found Anfld...',ga.modelAn,ga.vdtg,'var: ',ivar,' tau: ',tau
        return(0)
    else:
        if(doshfilt):
            ga.set.latlon(wmo.gglat1,wmo.gglat2,wmo.gglon1,wmo.gglon2)
            ga.dvar.shfilt(ovar,makeIvar(ivar,tau,1))
            ga.dvar.regrid(ovar,ovar,wmo.reargs)
        return(1)
    
def makeFcfld(ga,ovar,ivar,tau,wmo,doshfilt=0):
    
    ga.dvar.regrid(ovar,makeIvar(ivar,tau,ga.nfFc),wmo.reargs)
    if(ga.get.stat(ovar).nvalid == 0):
        print 'EEEfffffffffff no fields found Fcfld...',ga.modelAn,ga.vdtg,'var: ',ivar,' tau: ',tau
        return(0)
    else:
        if(doshfilt):
            ga.set.latlon(wmo.gglat1,wmo.gglat2,wmo.gglon1,wmo.gglon2)
            ga.dvar.shfilt(ovar,makeIvar(ivar,tau,1))
            ga.dvar.regrid(ovar,ovar,wmo.reargs)
        return(1)
    
def getClgaC(ga,ivar):
    
    if(ivar == 'ua' or ivar == 'va' or ivar == 'uva'):
        gaC=ga.nfcUV
    elif(ivar == 'zg'):
        gaC=ga.nfcMS
    else:
        print 'EEE invalid ivar: ',ivar,'in getClgaC'
        sys.exit()
    
    return(gaC)
    
def makeCl(ga,ovar,ivar,lev,wmo):

    byear=ga.Climo.byear
    cvdtg="%s%s"%(str(byear),ga.vdtg[4:])
    gtime=mf.dtg2gtime(cvdtg)

    gaC=getClgaC(ga,ivar)
    
    if(lev == 200 and ga.Climo.ctype == 'cmean'): lev=250
    
    expr="%s.%d(time=%s,lev=%d)"%(ivar,gaC,gtime,lev)
    
    if(ivar == 'zg' and ga.Climo.ctype == 'era-dailyclim'):
        expr="zgg.%d(time=%s,lev=%d)"%(gaC,gtime,lev)
        expr="(%s/%f)"%(expr,ga.Climo.gravity)
        
    ga.dvar.regrid(ovar,expr,wmo.reargs)
    if(ga.get.stat(ovar).nvalid == 0):
        print 'EEE no verifiying analysis...'
        return(0)
    else:
        return(1)
    
def makeFields(ga,wmo,vdtg,var,lev,tau):
    
    """ makes defined variables:
    
    vc = var climo
    va = var analysis (an)
    vf = var forecast (fc)
    vaa = va-vc = anom an from climo
    vfa = vf-vc = anom fc from climo
    vd  = vf-va = fc - an 
    coslat = cosine weights from makeCoslatWhgt()
    
    """

    ga.vdtg=vdtg
    ga.set.dtg(vdtg)
    ga.set.lev(lev)

    ga.set.latlon(wmo.gglat1,wmo.gglat2,wmo.gglon1,wmo.gglon2)

    rcc=makeCl(ga,'vc',var,lev,wmo)
    rca=makeAnfld(ga,'va',var,0,wmo)
    rcf=makeFcfld(ga,'vf',var,tau,wmo)

    if(rcc and rca and rcf):
        ga.dvar.var('vaa','va-vc')
        ga.dvar.var('vfa','vf-vc')
        ga.dvar.var('vd','vf-va')
        return(1)
    else:
        return(0)

    

#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
#
# command line setupdset ^pgrbfg_2010061700_fhr%f2_mem001
#

class MFCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv
        
        self.argv=argv
        self.argopts={
            1:['vdtgopt',    """vdtgopt"""],
            2:['modelFc',    """Forecast model to verify"""],
            }

        self.options={
            'verb':       ['V',0,1,'verb=1 is verbose'],
            'ropt':       ['N','','norun',' norun is norun'],
            'override':   ['O',0,1,'override'],
            'doStats':    ['S',1,0,'do NOT redo of the stats objs'],
            'wmoClim':    ['W',0,1,'use WMO clim from ECMWF'],
            'dtgopt':     ['D:',None,'a',"""set dtgopt for making the ensFC .ctl"""],
            'modelAn':    ['A:',None,'a',"""set model verification analaysis"""],
            'dtau':       ['d:',12,'i',"""set dtau for making the ensemble in tau"""],
            'tauopt':     ['t:',None,'a',"""set dtau for making the ensemble in tau"""],
            }


        self.defaults={
            'verbcd':-1,
            }
        
        self.purpose="""
make wmo verification stats
"""

        self.examples='''
        %s cur12-d5.cur12-12 gfs2 -A ecm2 -W # use WMO clim verify against ECMWF analyses
'''




            
#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# main

argv=sys.argv
CL=MFCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

pypdir="%s/veriWMO"%(w2.Nwp2DataBdir)
MF.ChkDir(pypdir,'mk')

# -- verify against own analysis
#
if(modelAn == None):
    modelAn=modelFc

# -- set verification dtgs, and ensFC dtgs
#
vdtgs=mf.dtg_dtgopt_prc(vdtgopt)
dtgs=vdtgs
if(dtgopt != None): dtgs=mf.dtg_dtgopt_prc(dtgopt)

if(doStats):
    
    # -- make grads object
    #
    ga=setGA(Window=0,Quiet=1)
    
    # -- make climo field obj
    #
    bdirClimo="%s/%s"%(w2.W2BaseDirDat,'climo')
    C=ClimoFld(bdir=bdirClimo)
    
    if(wmoClim): 
        bdirClimoWMO='/data/hfip/fiorino/w21/dat/climo'
        C=ClimoFldWMO(bdir=bdirClimoWMO)
    
    byearc=C.byear
    ga.Climo=C
    
    # -- make EnsModel obj for an and fc, with option to 
    #
    anoverride=override
    fcoverride=override
    if(modelAn == modelFc): fcoverride=0
    
    justinit=1
    if(override): justinit=0

    m2An=EnsModel(modelAn,dtgs,dtau=dtau,overrideLN=anoverride,overrideGM=anoverride,justinit=justinit)
    m2Fc=EnsModel(modelFc,dtgs,dtau=dtau,overrideLN=fcoverride,overrideGM=fcoverride,justinit=justinit)
    
    print 'FC: ',m2Fc.ensFcCtlpath
    
    ga.fhAn=ga.open(m2An.ensFcCtlpath)
    ga.fhFc=ga.open(m2Fc.ensFcCtlpath)
    
    if(hasattr(C,'ctlpathUV')):
        ga.fhcUV=ga.open(C.ctlpathUV)
    else:
        ga.fhcUV=ga.open(C.ctlpath)
    
    if(hasattr(C,'ctlpathWS')):
        ga.fhcWS=ga.open(C.ctlpathWS)
    else:
        ga.fhcWS=ga.open(C.ctlpath)
        
    if(hasattr(C,'ctlpathMS')):
        ga.fhcMS=ga.open(C.ctlpathMS)
    else:
        ga.fhcMS=ga.open(C.ctlpath)
            
    
    ga.nfAn=ga.fhAn.fid
    ga.nfFc=ga.fhFc.fid
    
    ga.nfcUV=ga.fhcUV.fid
    ga.nfcWS=ga.fhcWS.fid
    ga.nfcMS=ga.fhcMS.fid
    
    ga.modelAn=modelAn
    ga.modelFc=modelFc
            
    ga.modelAn=m2An
    ga.modelFc=m2Fc


# -- wmo area grids
#
wmo=WmoAreaGrid()

# -- make the cos(lat) weights
#
if(doStats):
    ga.set.latlon(wmo.gglat1,wmo.gglat2,wmo.gglon1,wmo.gglon2)
    rcl=makeCoslatWght(ga,'coslat',wmo)

area='nhem'
areas=['nhem','shem','tropics']
vars=[ ('zg',500),('ua',200),('va',200),('ua',850),('va',850) ]

areas=['nhem','shem','tropics']
#areas=['nhem','shem']

areavars={}

areavars['tropics']=[
    ['ua',925],['va',925],['uva',925],
    ['ua',850],['va',850],['uva',850],
    ['ua',700],['va',700],['uva',700],
    ['ua',500],['va',500],['uva',500],
    ['ua',250],['va',250],['uva',250],
    ['ua',200],['va',200],['uva',200],
    ['ua',100],['va',100],['uva',100],
]

areavars['nhem']=[['zg',500]]
areavars['shem']=[['zg',500]]

taus=[120,144,168]
taus=range(0,240+1,12)

if(tauopt != None):
    tt=tauopt.split('.')
    if(len(tt) == 1): 
        taus=[int(tauopt)]
    elif(len(tt) == 2):
        taus=range(tt[0],tt[1]+1,dtau)
    else:
        print 'tauopt: ',tauopt," no taus from tauopt.split() taus=[]"
        taus=[]

didstats=0
fldsok=-1

for vdtg in vdtgs:

    pyppath="%s/wmo-veri-%s-%s-%s.pyp"%(pypdir,modelFc,modelAn,vdtg)
    
    try:
        PF=open(pyppath,'rb')
        (Stats)=pickle.load(PF)
    except:
        Stats={}
    
    if(override): Stats={}
    
    for area in areas:

        for tau in taus:
        
            for var in areavars[area]:
                
                vvar=var[0]
                vlev=var[1]
                
                print 'VVVVVVVVVVVVVVVVV vdtg: %s area: %s tau: %d var: %s'%(vdtg,area,tau,str(var))
               
                if(doStats):
                    fldsok=makeFields(ga,wmo,vdtg,vvar,vlev,tau)
                    if(fldsok == 0): continue

                try:
                    ss=Stats[modelFc,modelAn,vdtg,area,tau,vvar,vlev]
                except:
                    ss=None
                
                # -- got from pickle
                #
                if( not(doStats) and not(override) ):
                    if(ss == None):
                        print "NN: %s %s %s %10s"%(modelFc,modelAn,vdtg,area),tau,vvar,vlev,' no pickled stats...'
                    else:
                        print 'SS: fc: %s an: %s %s %10s'%(modelFc,modelAn,vdtg,area),tau,vvar,vlev
                        print "rmse: %8.4g bias: %8.4g AC: %8.4g"%(ss.rmse,ss.meane,ss.acAnFcwmo)
                        continue    

                # -- vector vars
                #
                if(vvar =='uva'):
                    if(fldsok == 0): break

                    try:
                        ssu=Stats[modelFc,modelAn,vdtg,area,tau,'ua',vlev]
                        ssv=Stats[modelFc,modelAn,vdtg,area,tau,'va',vlev]
                    except:
                        print 'EEE doing vector stats -- u v stats must exist first'
                        continue

                    ss=WmoStats(area,vdtg,vvar,vlev,tau)
                    ss.makeVectorStats(ssu,ssv)
                    
                # -- scalar vars
                #
                else:

                    ss=WmoStats(area,vdtg,vvar,vlev,tau)

                    if(doStats):
                        didstats=1
                        ss.makeStats(ga,wmo)
                        Stats[modelFc,modelAn,vdtg,area,tau,vvar,vlev]=ss
                        
                    if(ss == None):
                        Stats[modelFc,modelAn,vdtg,area,tau,vvar,vlev]=None

                    if(didstats):
                        print '%-5s %s %8s %3d %4s  rmes: %8.4g  bias: %8.4g  acwmo: %5.3f'%(vvar,vdtg,area,tau,vlev,ss.rmse,ss.meane,ss.acAnFcwmo)


    if(doStats or override):
        
        print 'PPPPPPPPPickling....'
        PF=open(pyppath,'wb')
        pickle.dump((Stats),PF)
        PF.close()
            





    

