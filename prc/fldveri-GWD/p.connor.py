#!/usr/bin/env python

from WxMAP2 import *
w2=W2()                               # w2 obj with vars/methods

from cm2 import ClimoFld,ClimoFldWMO  # class pointing to climo data
from ga2 import setGA                 # grads class
from  m2 import *                     # class for ens of model runs and wmostats

modelAn='gfs2'
modelFc='gfs2'
vdtgopt='cur12-12'
wmoClim=1
gaWindow=1
override=0
dtau=24

# -- set verification dtgs, and ensFC dtgs
#
vdtgs=mf.dtg_dtgopt_prc(vdtgopt)
dtgs=vdtgs

# -- make grads object
#
ga=setGA(Window=gaWindow,Quiet=0)

# -- make climo field obj
#

if(wmoClim): 
    bdirClimoWMO='/data/hfip/fiorino/w21/dat/climo'
    C=ClimoFldWMO(bdir=bdirClimoWMO)
else:
    bdirClimo="%s/%s"%(w2.W2BaseDirDat,'climo')
    C=ClimoFld(bdir=bdirClimo)

byearc=C.byear
ga.Climo=C

# -- make EnsModel obj for an and fc, with option to 
#
anoverride=override
fcoverride=override

justinit=1

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
rcl=wmo.makeCoslatWght(ga,'coslat')  

# -- make the cos(lat) weights
#
ga.set.latlon(wmo.gglat1,wmo.gglat2,wmo.gglon1,wmo.gglon2)

areavars={}
areas=['nhem']
areavars['nhem']=[['zg',500]]

#areas=['tropics']
#areavars['tropics']=[['uva',850]]

taus=range(0,240+1,24)
taus=[72]

for vdtg in vdtgs:

    Stats={}
    for area in areas:
        for tau in taus:
            for var in areavars[area]:
                
                vvar=var[0]
                vlev=var[1]
                
                print 'VVVVVVVVVVVVVVVVV vdtg: %s area: %s tau: %d var: %s'%(vdtg,area,tau,str(var))
               

                # -- vector vars
                #
                if(vvar =='uva'):

                    ss=WmoStats(area,vdtg,vvar,vlev,tau,wmo)

                    ssu=WmoStats(area,vdtg,'ua',vlev,tau,wmo)
                    fldsok=ssu.makeFields(ga,wmo,vdtg,'ua',vlev,tau)
                    ssu.makeStats(ga,wmo)
                    ssu.ls()

                    ssv=WmoStats(area,vdtg,'va',vlev,tau,wmo)
                    fldsok=ssu.makeFields(ga,wmo,vdtg,'ua',vlev,tau)
                    ssv.makeStats(ga,wmo)

                    ssv.ls()
                    ss.makeVectorStats(ssu,ssv)

                    fldsok=ss.makeFieldsUV(ga,wmo,vdtg,vvar,vlev,tau)
                    if(fldsok == 0): continue
                    
                    wmo.getAreaLatLon(area)
                    ga.set.latlonA(wmo)
                    
                # -- scalar vars
                #
                else:

                    ss=WmoStats(area,vdtg,vvar,vlev,tau,wmo)
                    fldsok=ss.makeFields(ga,wmo,vdtg,vvar,vlev,tau)
                    if(fldsok == 0): continue
                    ss.makeStats(ga,wmo)
                    
                    wmo.getAreaLatLon(area)
                    ga.set.latlonA(wmo)
                    
                    Stats[modelFc,modelAn,vdtg,area,tau,vvar,vlev]=ss
                        
                    if(ss == None):
                        Stats[modelFc,modelAn,vdtg,area,tau,vvar,vlev]=None

                    print '%-5s %s %8s %3d %4s  rmes: %8.4g  bias: %8.4g  acwmo: %5.3f'%(vvar,vdtg,area,tau,vlev,ss.rmse,ss.meane,ss.acAnFcwmo)
                    


