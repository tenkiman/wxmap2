#!/usr/bin/env python

from WxMAP2 import *
w2=W2()                               # w2 obj with vars/methods

from cm2 import ClimoFld,ClimoFldWMO  # class pointing to climo data
from ga2 import setGA                 # grads class
from  m2 import *                     # class for ens of model runs and wmostats

#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
#
# -- command line 
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
            'verb':          ['V',0,1,'verb=1 is verbose'],
            'ropt':          ['N','','norun',' norun is norun'],
            'override':      ['O',0,1,'override'],
            'wmoClim':       ['W',1,0,'do NOT use WMO clim from ECMWF'],
            'singleRun':     ['s',0,1,'do single run'],
            'dtgopt':        ['D:',None,'a',"""set dtgopt for making the ensFC .ctl"""],
            'modelAn':       ['A:',None,'a',"""set model verification analaysis"""],
            'vStd':          ['D:','wmo','a',"""set vStd: verification standard = 'wmo'|'testhur'"""],
            'doFwriteAll':   ['F',0,1,"""fwrite out the grids used to calc the stats"""],
            'doPypWriteAll': ['P',0,1,"""write out ss ojb to pypdb"""],
            'doStwrite':     ['S',1,0,"""do NOT output stats to text"""],
            'dtau':          ['d:',24,'i',"""set dtau for making the ensemble in tau"""],
            'tauopt':        ['t:',None,'a',"""set dtau for making the ensemble in tau"""],
            'postfix':       ['p:',None,'a',"""-postfix added to ensFC files"""],
            'qsubrun':       ['q:',0,'i',"""set the qsubrun for FIM gwd exp"""],
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

models=modelFc.split(',')

# -- cycle by model
#
if(len(models) > 1):
    
    for model in models:
        cmd="%s/%s %s %s"%(pydir,pyfile,vdtgopt,model)
        for o,a in CL.opts:
            cmd="%s %s %s"%(cmd,o,a)
        mf.runcmd(cmd,ropt)
    
    sys.exit()
    
    

#modelAn='gfs2'
#modelFc='gfs2'

#wmoClim=1
gaWindow=0
gaQuiet=1


dographics=0
justinit=1

# -- set verification dtgs
#
vdtgs=mf.dtg_dtgopt_prc(vdtgopt)
dtgs=vdtgs

# -- wmo area grids, areas/Vars method
#
wmo=WmoAreaGrid()

# -- get areas/vars/taus
#
(areas,areavars,areaTaus)=wmo.setAreaVars(vStd,modelFc,dtau,dtgs[-1])

# -- default is to verify against own analysis
#
if(modelAn == None):
    modelAn=modelFc

lasttau=168

# -- set verification dtgs, and ensFC dtgs
#
if(modelFc == 'gfs2'):
    taus=range(0,lasttau+1,dtau) # ncep gfs
else:
    taus=range(0,lasttau+1,24)

if(tauopt != None):
    tt=tauopt.split('.')
    if(len(tt) == 1): 
        taus=[int(tauopt)]
    elif(len(tt) == 2):
        taus=range(tt[0],tt[1]+1,dtau)
    else:
        print 'tauopt: ',tauopt," no taus from tauopt.split() taus=[]"
        taus=[]
        

if(areaTaus != None): taus=areaTaus
    
MF.sTimer('ALL')

MF.sTimer('ga')
# -- make grads object
#
ga=setGA(Window=gaWindow,Quiet=gaQuiet)

# -- make climo field obj
#

if(wmoClim): 
    bdirClimoWMO='/data/hfip/fiorino/w21/dat/climo'
    if(w2.onKishou): bdirClimoWMO='/w21/dat/climo'
    C=ClimoFldWMO(bdir=bdirClimoWMO)
else:
    bdirClimo="%s/%s"%(w2.W2BaseDirDat,'climo')
    C=ClimoFld(bdir=bdirClimo)

byearc=C.byear
ga.Climo=C

# -- make EnsModel obj for an and fc, with option to 
#
anoverride=fcoverride=0 # not here

m2An=EnsModel(modelAn,dtgs,justinit=justinit,postfix=postfix)
m2Fc=EnsModel(modelFc,dtgs,justinit=justinit,postfix=postfix)

# -- fim experiments
#
FcExp={}

# -- broken because units of dpsig and ??? in 2011 gwd in mb but in 2012 gwd in Pa
### FcExp[2,'ctl']='/w21/dat/nwp2/rtfim/qsubfim_expt/newgwd/fim8.newgwd.2014050918.ctl'
### FcExp[2,'mod']='fim8-newgwd-AT0'

FcExp[1,'ctl']='/w21/dat/nwp2/rtfim/qsubfim_expt/trunk_4301/fim8.trunk_4301.2014050918.ctl'
FcExp[1,'mod']='fim8-trunk-AT0'

FcExp[2,'ctl']='/w21/dat/nwp2/rtfim/qsubfim_expt/trunk_4301_alttopo_false_no_gwd/fim8.trunk_4301_nogwd.2014050918.ctl'
FcExp[2,'mod']='fim8-trunk-noGWD'

FcExp[3,'ctl']='/w21/dat/nwp2/rtfim/qsubfim_expt/2012phys/fim8.2012phys.2014050918.ctl'
FcExp[3,'mod']='fim8-2012phys-AT0'

FcExp[4,'ctl']='/w21/dat/nwp2/rtfim/qsubfim_expt/newgwd_sigfac_0.1/fim8.newgwd_sigfac_0.1.2014050918.ctl'
FcExp[4,'mod']='fim8-newgwd-sigfac-0.1-AT0'

FcExp[5,'ctl']='/w21/dat/nwp2/rtfim/qsubfim_expt/newgwd_sigfac_4.0/fim8.newgwd_sigfac_4.0.2014050918.ctl'
FcExp[5,'mod']='fim8-newgwd-sigfac-4.0-AT0'

FcExp[6,'ctl']='/w21/dat/nwp2/rtfim/qsubfim_expt/newgwd_sigfac_1.0/fim8.newgwd_sigfac_1.0.2014050918.ctl'
FcExp[6,'mod']='fim8-newgwd-sigfac-1.0-AT0'

FcExp[7,'ctl']='/w21/dat/nwp2/rtfim/qsubfim_expt/newgwd_sigfac_0.1_branch/fim8.newgwd_sigfac_0.1.2014050918.ctl'
FcExp[7,'mod']='fim8-newgwd-branch-sigfac-0.1-AT0'
 
FcExp[8,'dtg']='2014051000'
FcExp[8,'ctl']='/w21/dat/nwp2/rtfim/qsubfim_expt/newgwd_%s/fim8.newgwd.%s.ctl'%(FcExp[8,'dtg'],FcExp[8,'dtg'])
FcExp[8,'mod']='fim8-newgwd-%s'%(FcExp[8,'dtg'])
 
FcExp[9,'dtg']='2013122400'
FcExp[9,'ctl']='/w21/dat/nwp2/rtfim/qsubfim_expt/newgwd_%s/fim8.newgwd.%s.ctl'%(FcExp[9,'dtg'],FcExp[9,'dtg'])
FcExp[9,'mod']='fim8-newgwd-%s'%(FcExp[9,'dtg'])

FcExp[10,'dtg']='2014051000'
FcExp[10,'ctl']='/w21/dat/nwp2/rtfim/qsubfim_expt/trunk_r4301_%s/fim8.trunk_r4301.%s.ctl'%(FcExp[10,'dtg'],FcExp[10,'dtg'])
FcExp[10,'mod']='fim8-trunk-r4301-%s'%(FcExp[10,'dtg'])
 
FcExp[11,'dtg']='2013122400'
FcExp[11,'ctl']='/w21/dat/nwp2/rtfim/qsubfim_expt/trunk_r4301_%s/fim8.trunk_r4301.%s.ctl'%(FcExp[11,'dtg'],FcExp[11,'dtg'])
FcExp[11,'mod']='fim8-trunk-r4301-%s'%(FcExp[11,'dtg'])
 
FcExp[12,'dtg']='2013122400'
FcExp[12,'ctl']='/w21/dat/nwp2/rtfim/qsubfim_expt/newgwd_%s_sigfac_4.0/fim8.newgwd.%s.ctl'%(FcExp[12,'dtg'],FcExp[12,'dtg'])
FcExp[12,'mod']='fim8-newgwd-sigfac-4.0-%s'%(FcExp[12,'dtg'])
 
FcExp[13,'dtg']='2014050918'
FcExp[13,'ctl']='/w21/dat/nwp2/rtfim/qsubfim_expt/bao_2014phystest_2014phys/fim8.bao_2014phystest_2014phys.%s.ctl'%(FcExp[13,'dtg'])
FcExp[13,'mod']='fim8-2014phys-%s'%(FcExp[13,'dtg'])
 
FcExp[14,'dtg']='2014050918'
FcExp[14,'ctl']='/w21/dat/nwp2/rtfim/qsubfim_expt/bao_2014phystest_trunk_r3773/fim8.bao_2014phystest_trunk_r3773.%s.ctl'%(FcExp[14,'dtg'])
FcExp[14,'mod']='fim8-trunk-r3773-%s'%(FcExp[14,'dtg'])
 
FcExp[15,'dtg']='2014050918'
FcExp[15,'ctl']='/w21/dat/nwp2/rtfim/qsubfim_expt/bao_2014phystest_newbranch/fim8.bao_2014phystest_newbranch.%s.ctl'%(FcExp[15,'dtg'])
FcExp[15,'mod']='fim8-2014phys-nb-%s'%(FcExp[15,'dtg'])
 
FcExp[16,'dtg']='2014050918'
FcExp[16,'ctl']='/w21/dat/nwp2/rtfim/qsubfim_expt/trunk_r4567_2014050918/fim8.trunk_4567.%s.ctl'%(FcExp[16,'dtg'])
FcExp[16,'mod']='fim8-trunk-r4567-%s'%(FcExp[16,'dtg'])
 
FcExp[17,'dtg']='2014050918'
FcExp[17,'ctl']='/w21/dat/nwp2/rtfim/qsubfim_expt/gwd2014-efact20_r4567_2014050918/fim8.gwd2014-efact20_4567.%s.ctl'%(FcExp[17,'dtg'])
FcExp[17,'mod']='fim8-gwd2014-efact20-r4567-%s'%(FcExp[17,'dtg'])
 
FcExp[18,'dtg']='2014050918'
FcExp[18,'ctl']='/w21/dat/nwp2/rtfim/qsubfim_expt/gwd2014-efact10_r4567_2014050918/fim8.gwd2014-efact10_4567.%s.ctl'%(FcExp[18,'dtg'])
FcExp[18,'mod']='fim8-gwd2014-efact10-r4567-%s'%(FcExp[18,'dtg'])
 
FcExp[19,'dtg']='2014050918'
FcExp[19,'ctl']='/w21/dat/nwp2/rtfim/qsubfim_expt/gfs1534_%s_G8/grib.%s.ctl'%(FcExp[19,'dtg'],FcExp[19,'dtg'])
FcExp[19,'mod']='fim8-gwd2014-gfs1534-sf40-%s'%(FcExp[19,'dtg'])
 
FcExp[20,'dtg']='2014050918'
FcExp[20,'ctl']='/w21/dat/nwp2/rtfim/qsubfim_expt/gfs574_%s_G8/grib.%s.ctl'%(FcExp[20,'dtg'],FcExp[20,'dtg'])
FcExp[20,'mod']='fim8-gwd2014-gfs574-sf40-%s'%(FcExp[20,'dtg'])
 
FcExp[21,'dtg']='2014050918'
FcExp[21,'ctl']='/w21/dat/nwp2/rtfim/qsubfim_expt/gfs1534-sf01_%s_G8/grib.%s.ctl'%(FcExp[21,'dtg'],FcExp[21,'dtg'])
FcExp[21,'mod']='fim8-gwd2014-gfs1534-sf01-%s'%(FcExp[21,'dtg'])
 
FcExp[22,'dtg']='2014050918'
FcExp[22,'ctl']='/w21/dat/nwp2/rtfim/qsubfim_expt/gfs574-sf01_%s_G8/grib.%s.ctl'%(FcExp[22,'dtg'],FcExp[22,'dtg'])
FcExp[22,'mod']='fim8-gwd2014-gfs574-sf01-%s'%(FcExp[22,'dtg'])
 
 
 
 
###FcExp[4,'ctl']='/w21/dat/nwp2/rtfim/qsubfim_expt/2012phys_alttopo_true/fim8.2012phys_alttopo_true.2014050918.ctl'
###FcExp[4,'mod']='fim8-2012phys-AT1'

# -- broken because units of dpsig and ??? in 2011 gwd in mb but in 2012 gwd in Pa
### FcExp[5,'ctl']='/w21/dat/nwp2/rtfim/qsubfim_expt/newgwd_alttopo_true/fim8.newgwd_alttopo_true.2014050918.ctl'
### FcExp[5,'mod']='fim8-newgwd-AT1'


if(qsubrun > 0):
    fcStartVdtg=dtgs[0]
    bdtg   =fcStartVdtg
    fcCtl  =FcExp[qsubrun,'ctl']
    modelFc=FcExp[qsubrun,'mod']
    singleRun=1
else:
    fcCtl=m2Fc.ensFcCtlpath
    bdtg=None                              # -- if != None, then use we're using a single run dtg
    if(singleRun): fcStartVdtg=dtgs[0]

# --  set the taus by vdtg -- single run then fixed vdtg
#

fctausByVdtg={}

if(singleRun):

    vdtgs=[]
    btaufc=0
    etaufc=192
    etaufc=168
    if(qsubrun > 0): 
        dtaufc=dtau
        fcTaus=range(btaufc,etaufc+1,dtaufc)
        fcTausFwrite=range(dtaufc,etaufc+1,dtaufc)
    else:
        fcTaus=taus
        fcTausFwrite=copy.deepcopy(taus)
        del fcTausFwrite[0]
    
    for fctau in fcTaus:
        fcvdtg=mf.dtginc(fcStartVdtg,fctau)
        fctausByVdtg[fcvdtg]=[fctau]
        vdtgs.append(fcvdtg)
        
    vdtgs.sort()
    dtgs=vdtgs
    
else:
    for vdtg in vdtgs:
        fctausByVdtg[vdtg]=taus

    fcTausFwrite=taus

if(verb):
    print '       fcCtl: ',fcCtl
    print '      fcTaus: ',fcTaus
    print 'fcTausFwrite: ',fcTausFwrite
    print 'fctausByVdtg: ',fctausByVdtg
    print '       vdtgs: ',vdtgs
    

ga.fhAn=ga.open(m2An.ensFcCtlpath)
ga.fhFc=ga.open(fcCtl)

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

MF.dTimer('ga')

# -- make coslat weights
#
rcl=wmo.makeCoslatWght(ga,'coslat')  

# -- pypdb
#
if(doPypWriteAll):
    pypdir=wmo.tdirPYPDB
    MF.ChkDir(pypdir,'mk')

# -- make the cos(lat) weights
#
ga.set.latlon(wmo.gglat1,wmo.gglat2,wmo.gglon1,wmo.gglon2)

ocards=[]

for vdtg in vdtgs:

    MF.sTimer('vdtg-%s'%(vdtg))
    if(doPypWriteAll):
        pyppath="%s/wmo-veri-%s-%s-%s.pyp"%(pypdir,modelFc,modelAn,vdtg)

    doPypWrite=0
    try:
        PF=open(pyppath,'rb')
        (Stats)=pickle.load(PF)
    except:
        doPypWrite=1
        Stats={}
    
    if(override): 
        doPypWrite=1
        Stats={}
    
    if(not(doPypWriteAll)): doPypWrite=0
       
    taus=fctausByVdtg[vdtg]

    for tau in taus:
        
        for area in areas:
 
            for var in areavars[area]:

                vvar=var[0]
                vlev=var[1]
           
                doFwrite=0
                if(doFwriteAll and tau in fcTausFwrite): doFwrite=1
                
                ocard="%-20s %s %s %10s %03d %10s %4d"%(modelFc,modelAn,vdtg,area,tau,vvar,vlev)
                
                print 'Proc: ',ocard,' doFwrite: ',doFwrite 

                # -- vector vars
                #
                if(vvar =='uva'):

                    ocardU="%-20s %s %s %10s %03d %10s %4d"%(modelFc,modelAn,vdtg,area,tau,'ua',vlev)
                    ocardV="%-20s %s %s %10s %03d %10s %4d"%(modelFc,modelAn,vdtg,area,tau,'va',vlev)
                    ocardW="%-20s %s %s %10s %03d %10s %4d"%(modelFc,modelAn,vdtg,area,tau,'wa',vlev)

                    corrUV=corrClUV=rmseTUV=rmsePUV=rmseEUV=biasUV=-999.
                    corrU =corrClU= rmseTU= rmsePU=  rmseEU= biasU=-999.
                    corrV =corrClV= rmseTV= rmsePV=  rmseEV= biasV=-999.
                    corrW =corrClW= rmseTW= rmsePW=  rmseEW= biasW=-999.
                    
                    ssuv=WmoStats(area,vdtg,vvar,vlev,tau,wmo,bdtg=bdtg,verb=verb,
                                  modelAn=modelAn,modelFc=modelFc,doFwrite=doFwrite)

                    ssu=WmoStats(area,vdtg,'ua',vlev,tau,wmo,bdtg=bdtg,verb=verb,
                                 modelAn=modelAn,modelFc=modelFc,doFwrite=doFwrite)
                    
                    fldsoku=ssu.makeFields(ga,wmo,vdtg,'ua',vlev,tau)
                    if(fldsoku):
                        ssu.makeStats(ga,wmo)
                    else:
                        print """EEE can't make fields UUUUU vdtg: %s vlev: %d tau: %d"""%(vdtg,vlev,tau)
                        doFwrite=0
                        
                    ssv=WmoStats(area,vdtg,'va',vlev,tau,wmo,bdtg=bdtg,verb=verb,
                                 modelAn=modelAn,modelFc=modelFc,doFwrite=doFwrite)
                    
                    fldsokv=ssv.makeFields(ga,wmo,vdtg,'va',vlev,tau)
                    
                    if(fldsokv):
                        ssv.makeStats(ga,wmo)
                        ssuv.makeVectorStats(ssu,ssv)
                        
                        corrUV=ssuv.corrUV
                        corrClUV=ssuv.corrClUV
                        rmseTUV=ssuv.rmseTUV
                        rmsePUV=ssuv.rmsePUV
                        rmseEUV=ssuv.rmseEUV

                        corrU=ssu.corrAnFc
                        corrClU=ssu.corrAnFcCl
                        rmseTU=ssu.rmseT
                        rmsePU=ssu.rmseP
                        rmseEU=ssu.rmseE
                        biasU=ssu.MeanErr
    
                        corrV=ssv.corrAnFc
                        corrClV=ssv.corrAnFcCl
                        rmseTV=ssv.rmseT
                        rmsePV=ssv.rmseP
                        rmseEV=ssv.rmseE
                        biasV=ssv.MeanErr
                        
                    else:
                        print """EEE can't make VVVVV fields vdtg: %s vlev: %d tau: %d"""%(vdtg,vlev,tau)
                        doFwrite=0

                    ssw=WmoStats(area,vdtg,'wa',vlev,tau,wmo,bdtg=bdtg,verb=verb,
                                 modelAn=modelAn,modelFc=modelFc,doFwrite=doFwrite)
                    fldsokw=ssw.makeFields(ga,wmo,vdtg,'wa',vlev,tau)

                    if(fldsokw):
                        ssw.makeStats(ga,wmo)

                        corrW=ssw.corrAnFc
                        corrClW=ssw.corrAnFcCl
                        rmseTW=ssw.rmseT
                        rmsePW=ssw.rmseP
                        rmseEW=ssw.rmseE
                        biasW=ssw.MeanErr

                    else:
                        print """EEE can't make WWWWW fields vdtg: %s vlev: %d tau: %d"""%(vdtg,vlev,tau)
                        #continue #sys.exit()
                        doFwrite=0
    
    
                    ocard="%s %8.3f %8.3f %8.3f %8.3f %8.3f %8.3f"%(ocard,corrClUV,corrUV,rmseTUV,rmsePUV,rmseEUV,biasUV)
                    ocards.append(ocard)

                    ocardU="%s %8.3f %8.3f %8.3f %8.3f %8.3f %8.3f"%(ocardU,corrClU,corrU,rmseTU,rmsePU,rmseEU,biasU)
                    ocards.append(ocardU)
                    
                    ocardV="%s %8.3f %8.3f %8.3f %8.3f %8.3f %8.3f"%(ocardV,corrClV,corrV,rmseTV,rmsePV,rmseEV,biasV)
                    ocards.append(ocardV)

                    ocardW="%s %8.3f %8.3f %8.3f %8.3f %8.3f %8.3f"%(ocardW,corrClW,corrW,rmseTW,rmsePW,rmseEW,biasW)
                    ocards.append(ocardW)
                    
                    
                    Stats[modelFc,modelAn,vdtg,area,tau,'ua',vlev]=ssu
                    Stats[modelFc,modelAn,vdtg,area,tau,'va',vlev]=ssv
                    Stats[modelFc,modelAn,vdtg,area,tau,'uva',vlev]=ssuv

                    
                # -- scalar vars
                #
                else:

                    acAnFc=corrAnFc=rmseT=rmseP=rmseE=bias=-999.
                    
                    ss=WmoStats(area,vdtg,vvar,vlev,tau,wmo,bdtg=bdtg,
                                modelAn=modelAn,modelFc=modelFc,doFwrite=doFwrite)
                    
                    fldsok=ss.makeFields(ga,wmo,vdtg,vvar,vlev,tau)
                    
                    if(fldsok):
                        
                        ss.makeStats(ga,wmo)
                        if(ss == None):
                            Stats[modelFc,modelAn,vdtg,area,tau,vvar,vlev]=None
                        else:
                            Stats[modelFc,modelAn,vdtg,area,tau,vvar,vlev]=ss
                            
                        corrAnFc = ss.corrAnFc
                        acAnFc   = ss.corrAnFcCl
                        rmseT    = ss.rmseT
                        rmseP    = ss.rmseP
                        rmseE    = ss.rmseE
                        bias     = ss.MeanErr
                        
                    
                    #print '%-5s %s %8s %3d %4s  rmes: %8.4g  bias: %8.4g  acwmo: %5.3f'%(vvar,vdtg,area,tau,vlev,ss.rmse,ss.meane,ss.acAnFcwmo)
                    ocard="%s %8.3f %8.3f %8.3f %8.3f %8.3f %8.3f"%(ocard,acAnFc,corrAnFc,rmseT,rmseP,rmseE,bias)
                    ocards.append(ocard)
                    
                    
                if(dographics):
                    wmo.getAreaLatLon(area)
                    ga.set.latlonA(wmo)
                    

                    

    if(not(singleRun)):
        
        if(doStwrite):
            odirSt="%s/%s"%(wmo.tdirSTATS,vdtg)
            MF.ChkDir(odirSt,'mk')
            opathSt="%s/%s-%s.%s.txt"%(odirSt,modelFc,modelAn,vdtg)
            MF.WriteList2Path(ocards, opathSt,verb=1)
        else:
            for ocard in ocards:
                print 'St: ',ocard
                
        if(doPypWrite):
                    
            print 'PPPPPPPPPickling: ',pyppath
            PF=open(pyppath,'wb')
            pickle.dump((Stats),PF)
            PF.close()    

            
    MF.dTimer('vdtg-%s'%(vdtg))
    
            
if(singleRun):
    
    if(doStwrite):
        odirSt="%s/%s"%(wmo.tdirSTATS,vdtgs[0])
        MF.ChkDir(odirSt,'mk')
        opathSt="%s/%s_%s_single.%s.txt"%(odirSt,modelFc,modelAn,vdtgs[0])
        MF.WriteList2Path(ocards, opathSt,verb=1)
    else:   
        for ocard in ocards:
            print 'St-Single: ',ocard
        

    if(doPypWrite):
        
        print 'PPPPPPPPPickling-Single: ',pyppath
        PF=open(pyppath,'wb')
        pickle.dump((Stats),PF)
        PF.close()

MF.dTimer('ALL')
