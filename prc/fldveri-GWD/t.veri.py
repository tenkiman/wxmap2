#!/usr/bin/env python

from M import *
MF=MFutils()

import m2

from CM import ClimoFld
from GA import setGA2
from m2 import EnsModel



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
        
        rmse=sqrt(mse)
        bias=sqrt( (ssu.meanAn-ssu.meanFc)*(ssu.meanAn-ssu.meanFc) + (ssv.meanAn-ssv.meanFc)*(ssv.meanAn-ssv.meanFc) )

        sig2aCL=(ssu.sum2AnCl + ssv.sum2AnCl)/Ninv
        sig2fCL=(ssu.sum2FcCl + ssv.sum2FcCl)/Ninv

        sigaCl=sqrt(sig2aCl)
        sigfCl=sqrt(sig2fCl)

        corr=( (ssu.sum2AnFc + ssv.sum2AnFc)/Ninv ) / (siga*sigf)
        corrCl=( (ssu.sum2AnFcCl + ssv.sum2AnFcCl)/Ninv ) / (sigaCl*sigfCl)

        print 'uu: ',ssu.sigmaAn,ssu.sigmaFc
        print 'vv: ',ssv.sigmaAn,ssv.sigmaFc
        print 'area: ',ssu.area,siga,sigf,'corr: ',corr,' corrCl: ',corrCl,' rmse: ',rmse,' bias: ',bias
        
        self.hashvalue=[siga,sigf,corr,sigaCl,sigfCl,corrCl,rmse,bias]
        self.hashvaluedesc=['sigmaAn','sigmaFc','vectorCorr','sigmaAnCl','sigmaFcCl','vectorCorrCl','rmse','bias']

        


        

    def makeStats(self,ga,wmo):
        """
         strictly by the wmo red book, ii.7-36 - ii.7-38
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
        self.acAnFcwmo=s12ac/(s1ac*s2ac)
        self.rmse=sqrt(s2d/scg)
        self.meane=s1d/scg
        self.acAnFc=ga.get.scorr('vaa','vfa',wmo)

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

        self.hashkey=(self.modelFc,self.vdtg,self.area,self.var,self.tau,self.lev)

        self.hashvalue=[self.acAnFc,self.rmse,self.meane,self.corrAnFc,self.sigmaAn,self.sigmaFc,self.sigmaCl]

        self.hashvaluedesc=['acAnFc','rmse','meane','corrAnFc','sigmaAn','sigmaFc','sigmaCl']


    

class WmoAreaGrid():

    ggdx=2.5
    ggdy=2.5

    globalgrid='pole'
    method='ba'
    
    globalgrid='nopole'
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
    
def makeCoslatWght(ga,ovar,wmo):
    from math import pi
    dyh=wmo.ggdx*0.5
    fh=ga.nfAn
    ggdlat=wmo.ggdlat
    expr="(cos(lat.%d(t=1)*%g/%f))"%(fh,pi,ggdlat)
    ga.dvar.regrid(ovar,expr,wmo.reargs)
    return(1)
    
def makedSinlatWght(ga,wmo):
    from math import pi
    dyh=wmo.ggdx*0.5
    ggdlat=wmo.gglat
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
        print 'EEE no fields found...'
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
        print 'EEE no fields found...'
        return(0)
    else:
        if(doshfilt):
            ga.set.latlon(wmo.gglat1,wmo.gglat2,wmo.gglon1,wmo.gglon2)
            ga.dvar.shfilt(ovar,makeIvar(ivar,tau,1))
            ga.dvar.regrid(ovar,ovar,wmo.reargs)
        return(1)
    
    
def makeCl(ga,ovar,ivar,lev,wmo):
    byear=ga.Climo.byear
    cvdtg="%s%s"%(str(byear),ga.vdtg[4:])
    gtime=mf.dtg2gtime(cvdtg)

    if(lev == 200): lev=250
    expr="%s.%d(time=%s,lev=%d)"%(ivar,ga.nfc,gtime,lev)
    ga.dvar.regrid(ovar,expr,wmo.reargs)
    if(ga.get.stat(ovar).nvalid == 0):
        print 'EEE no verifiying analysis...'
        return(0)
    else:
        return(1)
    
def makeFields(ga,wmo,vdtg,var,lev,tau):

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
            1:['modelFc',    """Forecast model to verify"""],
            2:['dtgopt',     """dtgopt"""],
            }

        self.options={
            'verb':['V',0,1,'verb=1 is verbose'],
            'ropt':['N','','norun',' norun is norun'],
            'override':['O',0,1,'override'],
            'redoStats':['R',0,1,'force redo of the stats objs'],
            'vdtgopt':['v:',None,'a',"""ls source data"""],
            'dtau':['d:',12,'i',"""set dtau for making the ensemble in tau"""],
            }


        self.defaults={
            'verbcd':-1,
            }
        
        self.purpose="""
make wmo verification stats
"""

        self.examples='''
        %s gfs2 2011041500.cur12-12 -v 2011051000.2011051100.12
'''




            
#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# main

argv=sys.argv
CL=MFCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr



modelAn=modelFc

# -- open pickled stats
#

pyppath='/ptmp/wmo.veri.pyp'

try:
    PF=open(pyppath,'rb')
    (Stats)=pickle.load(PF)
except:
    Stats={}


if(override):
    Stats={}
    



# make grads object
ga=setGA2(Window=0,Quiet=1)

C=ClimoFld()
byearc=C.byear
ga.Climo=C

dtgs=mf.dtg_dtgopt_prc(dtgopt)

anoverride=override
fcoverride=override
if(modelAn == modelFc): fcoverride=0

m2An=EnsModel(modelAn,dtgs,dtau=dtau,override=anoverride)
m2Fc=EnsModel(modelFc,dtgs,dtau=dtau,override=fcoverride)

print 'FC: ',m2Fc.ensFcCtlpath

ga.fhAn=ga.open(m2An.ensFcCtlpath)
ga.fhFc=ga.open(m2Fc.ensFcCtlpath)
ga.fhc=ga.open(C.ctlpath)

ga.nfAn=ga.fhAn.fid
ga.nfFc=ga.fhFc.fid
ga.nfc=ga.fhc.fid

ga.modelAn=modelAn
ga.modelFc=modelFc
        
ga.modelAn=m2An
ga.modelFc=m2Fc

if(vdtgopt == None): vdtgopt=dtgopt

vdtgs=mf.dtg_dtgopt_prc(vdtgopt)

# wmo area grids
wmo=WmoAreaGrid()

# make the cos(lat) weights
ga.set.latlon(wmo.gglat1,wmo.gglat2,wmo.gglon1,wmo.gglon2)
rcl=makeCoslatWght(ga,'coslat',wmo)


area='nhem'

areas=['nhem','shem','tropics']

vars=[ ('zg',500),('ua',200),('va',200),('ua',850),('va',850) ]

areas=['nhem']
vars=[['zg',500]]

areas=['nhem','shem','tropics']
areas=['nhem','tropics','shem']
areas=['tropics']
vars=[['zg',500],['ua',850],['va',850],['uva',850],['ua',200],['va',200],['uva',200]]
taus=[72,120,144]
taus=[120]
taus=[72]

didstats=0

for vdtg in vdtgs:
    
    for area in areas:

        for tau in taus:
        
            for var in vars:
                
                vvar=var[0]
                vlev=var[1]
                
                try:
                    ss=Stats[modelFc,modelAn,vdtg,area,tau,vvar,vlev]
                except:
                    ss=None

                if(ss != None and not(redoStats) and not(override)):
                    print 'SS: %s %s %s %10s'%(modelFc,modelAn,vdtg,area),tau,vvar,vlev,ss.acAnFc,ss.acAnFcwmo
                    continue

                if(vvar =='uva'):
                    try:
                        ssu=Stats[modelFc,modelAn,vdtg,area,tau,'ua',vlev]
                        ssv=Stats[modelFc,modelAn,vdtg,area,tau,'va',vlev]
                    except:
                        print 'EEE doing vector stats -- u v stats must exist first'
                        continue

                    ss=WmoStats(area,vdtg,vvar,vlev,tau)
                    ss.makeVectorStats(ssu,ssv)
                    

                else:

                    fldsok=makeFields(ga,wmo,vdtg,vvar,vlev,tau)
                    ss=WmoStats(area,vdtg,vvar,vlev,tau)

                    if(fldsok):
                        didstats=1
                        ss.makeStats(ga,wmo)
                        Stats[modelFc,modelAn,vdtg,area,tau,vvar,vlev]=ss
                    else:
                        Stats[modelFc,modelAn,vdtg,area,tau,vvar,vlev]=None
                    
                    print '%s %8s  ac:    %5.3f acwmo: %5.3f'%(vdtg,area,ss.acAnFc,ss.acAnFcwmo)

if(didstats or redoStats or override):
    print 'PPPPPPPPPickling....'
    PF=open(pyppath,'wb')
    pickle.dump((Stats),PF)
    PF.close()
            





    

