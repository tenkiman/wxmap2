#!/usr/bin/env python

from WxMAP2 import *
w2=W2()                               # w2 obj with vars/methods

from cm2 import ClimoFld,ClimoFldWMO  # class pointing to climo data
from ga2 import setGA                 # grads class
from  m2 import *                     # class for ens of model runs and wmostats

def parseRunCards(cards):
    
    rdict={}
    levsA=[]
    tausA=[]
    areasA=[]
    varsA=[]
    
    for card in cards:
        tt=card.split()
        run=tt[0]
        anl=tt[1]
        area=tt[3]
        tau=int(tt[4])
        var=tt[5]
        lev=int(tt[6])
        
        levsA.append(lev)
        tausA.append(tau)
        areasA.append(area)
        varsA.append(var)
        
        stats=[]

        rdict[area,tau,var,lev]=stats
        for i in range(7,len(tt)):
            stats.append(float(tt[i]))
            #print tt[i]
        #print 'qqq',run,area,tau,var,lev,stats
        
    levsA=mf.uniq(levsA)
    tausA=mf.uniq(tausA)
    areasA=mf.uniq(areasA)
    varsA=mf.uniq(varsA)
    
    return(rdict,run,anl,levsA,tausA,areasA,varsA)


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
            'singleRunOpt':  ['s:',None,'a','veri single run in -s path.ctl'],
            'dtgopt':        ['D:',None,'a',"""set dtgopt for making the ensFC .ctl"""],
            'modelAn':       ['A:',None,'a',"""set model verification analaysis"""],
            'vStd':          ['D:','wmo','a',"""set vStd: verification standard = 'wmo'|'testhur'"""],
            'doFwriteAll':   ['F',0,1,"""fwrite out the grids used to calc the stats"""],
            'doPypWriteAll': ['P',0,1,"""write out ss ojb to pypdb"""],
            'doStwrite':     ['S',1,0,"""do NOT output stats to text"""],
            'dtau':          ['d:',24,'i',"""set dtau for making the ensemble in tau"""],
            'tauopt':        ['t:',None,'a',"""set dtau for making the ensemble in tau"""],
            'postfix':       ['p:',None,'a',"""-%s added to ensFC files"""],
            'qsubrun':       ['q:',0,'i',"""set the qsubrun for FIM gwd exp"""],
            'doGaDat':       ['G',0,1,"""convert single.txt file to .dat file for templating"""],
            }


        self.defaults={
            'verbcd':-1,
            }
        
        self.purpose="""
make wmo verification stats
"""

        self.examples='''
%s 2014011000 fim8 -A gfs2 -p gfs-2014:fim-2014 # verify fim8 v gfs2 anl -p postfixAn:postfixFc
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

if(len(dtgs) == 1 and doGaDat):
    
    bdtg=dtgs[0]
    
    etau=240
    dtau=24
    otaus=range(0,etau+1,dtau) 
    olevs=[850,700,500,250,200,100]
    oareas=['nhem', 'shem', 'tropics']
    ovars=['hur', 'ta', 'ua', 'uva', 'va', 'wa', 'zg']
    
    idirSt="%s/%s"%(wmo.tdirSTATS,bdtg)
    
    runpaths=glob.glob("%s/*txt"%(idirSt))
    
    for runpath in runpaths:
        
        cards=open(runpath).readlines()
        rc=parseRunCards(cards)
        (rdict,orun,oanl,levsA,tausA,areasA,varsA)=rc
        levsA.reverse()

        print 'WWWWWWWWWWWWWWWW runpath: ',runpath,' orun: ',orun,' oanl: ',oanl
        
        if(verb):
            print 'levsA',levsA
            print 'tausA',tausA
            print 'areasA',areasA
            print 'varsA',varsA    

        for tau in otaus:

            vdtg=mf.dtginc(bdtg,tau)
            otauDir="%s/f%03d"%(wmo.tdirSTATS,int(tau))
            MF.ChkDir(otauDir,'mk')

            opath=runpath.replace('.txt','.f%03d.dat'%(int(tau)))
            opath=opath.replace(bdtg,vdtg)
            (odir,ofile)=os.path.split(opath)
            
            opath="%s/%s"%(otauDir,ofile)
        
            oB=open(opath,'wb')
            
            for var in ovars:
                for lev in olevs:
                    for area in oareas:
                        ostats=[-999.0,-999.0,-999.0,-999.0,-999.0,-999.0]
                        try:
                            ostats=rdict[area,tau,var,lev]
                        except:
                            ostats=[-999.0,-999.0,-999.0,-999.0,-999.0,-999.0]
                            
                        
                        stnrec = struct.pack('6f',ostats[0],ostats[1],ostats[2],ostats[3],ostats[4],ostats[5])
                        if(verb): print 'qqqqqqqqqqq',orun,tau,var,lev,area,ostats
                        oB.write(stnrec)
                        
            oB.close()
        
    sys.exit()
    
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

try:
    (postfixAn,postfixFc)=postfix.split(":")
except:
    postfixAn=postfixFc=postfix
    
m2An=EnsModel(modelAn,dtgs,justinit=justinit,postfix=postfixAn)
m2Fc=EnsModel(modelFc,dtgs,justinit=justinit,postfix=postfixFc)

m2An.ls()
m2Fc.ls()

if(singleRunOpt != None):
    try:
        (runctl,runid)=singleRunOpt.split(':')
    except:
        print 'EEE - invalid form of singleRunOpt: ',singleRunOpt
        print 'should be -s ctlpath.ctl:nameofrun'
        sys.exit()
        
    fcStartVdtg=dtgs[0]
    bdtg   =fcStartVdtg
    fcCtl  =runctl
    modelFc=runid
    singleRun=1
else:
    singleRun=1
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
    if(modelFc == 'gfs2'): etaufc=192
    if(modelFc == 'ecm2' or modelFc == 'fim8'): etaufc=240
    
    dtaufc=dtau
    fcTaus=range(btaufc,etaufc+1,dtaufc)
    fcTausFwrite=range(dtaufc,etaufc+1,dtaufc)
    
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
