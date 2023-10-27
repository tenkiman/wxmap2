#!/usr/bin/env python

import os,sys,glob,time,getopt

import mf
import w2
import M2
import FM

from WxMAP2 import W2
from W2Plot import PlotControl,Model2PlotControl,CmdLine



test=0

if(test == 1):
    model='gfs2'
    dtg='2009121500'
    plotopt='500'
    tauopt='0'
    areaopt='conus'
    MP=Model2PlotControl(model,dtg)
    MP.setAreas(areaopt)
    MP.setPlots(plotopt,tauopt)
    MP.setGsf()
    sys.exit()
    
elif(test == 2):
    model='rtfim'
    dtg='2009121500'
    plotopt='prp'
    tauopt='all'
    areaopt='conus'
    mp=PlotControl(model,dtg)
    mp.setAreas(areaopt)
    mp.setPlots(plotopt,tauopt)
    mp.setGsf()
    sys.exit()
else:
    rc=CmdLine()


(
    opts,curdtg,curphr,curyear,curtime,curdir,pypath,pydir,pyfile,ropt,verb,override,
    dtgopt,modelopt,
    plotopt,tauopt, areaopt,interact,dotest,dow2flds,
    ctltype,docleanplt,doarchive,
    )=rc

models=modelopt.split('.')
dtgs=mf.dtg_dtgopt_prc(dtgopt)

# cccccccccccccccc cycling
#

if(len(dtgs) > 1 or len(models) > 1):

    for model in models:
        for dtg in dtgs:
            cmd="%s %s %s"%(pyfile,dtg,model)
            for o,a in opts:
                cmd="%s %s %s"%(cmd,o,a)
            mf.runcmd(cmd,ropt)

    sys.exit()


dtg=dtgs[0]
model=models[0]

if(ropt == 'norun'):
    print 'RRR will run: ',model,dtg,' areaopt: ',areaopt
    sys.exit()
    

if(w2.IsModel2(model)):
    MP=Model2PlotControl(model,dtg)
else:
    MP=PlotControl(model,dtg)

if(not(MP.datathere)):
    print 'EEE no data for model: ',model,' dtg: ',dtg
    sys.exit()

MP.setAreas(areaopt)
MP.setPlots(plotopt,tauopt)
MP.setGsf()

curpid=os.getpid()

mf.ChangeDir(MP.prcdir)

# iiiiiiiiiiiiiiiiiii interaction
#
if(interact):  gmode='-lc'
else:          gmode='-lbc'

gradscmd='grads2'

grfprc='printim'
gsbase="g.wxmap.base.gs"
gsfinal="g.w1.%s.%s.gs"%(MP.dtg,MP.model)
gcmd="run %s"%(gsfinal)

gdir=MP.plotdir
if(mf.ChkDir(gdir,'mk') == 0):
    print 'EEE unable to make plotdir: ',gdir
    sys.exit()


for area in MP.areas:

    if(docleanplt):
        cmd="rm %s/*.%s.png"%(gdir,area)
        mf.runcmd(cmd,ropt)
        

    gradsruns=[]
    
    for tau in MP.taus:
            
        for plot in MP.plots:

            gname="%s/%s.%s.%03d.%s.png"%(gdir,MP.model,plot,tau,area)

            try:
                mopt1=w2env.plot_control[area,plot,'units']
            except:
                mopt1=''

            gtypeout=gname
            if(plot == 'clm'):
                gtypeout=gdir
                mopt1=pmodel

            gradsrun="%s %s %s %s %s y %s %s %d %d %s"%(MP.dtg,MP.model,tau,area,
                                                        MP.pnum[plot],
                                                        gtypeout,grfprc,
                                                        MP.plotXsize,MP.plotYsize,mopt1)
            
            taschk=1
            if((plot == 'tmx' or plot == 'tmn') and tau < 24): taschk=0

            if((not(os.path.exists(gname)) and taschk) or override):
                gradsruns.append(gradsrun)
            elif(taschk == 0):
                continue
            else:
                siz=os.path.getsize(gname)
                if(siz == 0):
                    gradsruns.append(gradsrun)
                else:
                    if(verb):
                        print 'WWWW already did plot for: ',plot,tau,area


    
    nrun=len(gradsruns)
    
    if(nrun > 0):
        
        cmd="cat %s > %s"%(gsbase,gsfinal)
        mf.runcmd(cmd,ropt)
        
        cfg="""
function loadcfg()

_geodir=\'%s\'
_climosstdir=\'%s\'
_climodatdir=\'%s\'
_prcdir=\'%s\'
_cfgdir=\'%s\'
_basemapdir=\'%s\'
_tack1=\'%s\'
_tack2=\'%s\'
_fullmod=\'%s\'
_t1col=1
_t2col=1

_nrun=%d
_interact=%d

model=%s
model2=%s

_bdtg=%s
_dtgp=incdtgh(_bdtg,%d)

"""%(
            MP.geodir,
            MP.climosstdir,
            MP.climodatdir,
            MP.prcdir,
            MP.cfgdir,
            MP.basemapdir,
            MP.modeltitleAck1,
            MP.modeltitleAck2,
            MP.modeltitleFullmod,
            nrun,
            interact,
            MP.model,
            MP.model,
            MP.dtg,
            MP.modeldtau,
            
            )
    

        cfg=cfg+"""
dpath='%s'
dpathm='%s'
dpath2='%s'

_fnf=ofile(dpath)
_fnfp=ofile(dpathm)
_fnfmod2=ofile(dpath2)

print 'qqqqqqqqqq 11111111 'dpath'   _fnf: '_fnf
print 'qqqqqqqqqq 22222222 'dpathm'  _fnfp: '_fnfp
print 'qqqqqqqqqq 22222222 'dpath2' _fnfmod2: '_fnfmod2

# from the modelvar.gsf, pslvar.gfs, precipvar.gsf prwvar.gsf...

_dotc=0


"""%(MP.ctlpathCur,MP.ctlpathPrv,MP.ctlpathCur)

        #
        # regrid?
        #
        
        doregrid=0
        if(plotopt == 'clm'):
            doregrid=1
            
        cfg=cfg+"""
_regrid=%d
    """%(doregrid)


        args=''

        i=1
        for gradsrun in gradsruns:
            arg="_args.%d=\'%s\'\n"%(i,gradsrun)
            args=args+arg
            i=i+1

        cfg=cfg+args+"""
return

%s

"""%(MP.modtitlegsf)

        cfg=cfg+"""
%s
"""%(MP.localvargsf)

        if(dotest == 0):
            tmpprcdir="%s.%s.%s.%s"%(w2.W2TmpPrcDirPrefix,MP.model,MP.dtg,curpid)
            mf.ChkDir(tmpprcdir,'mk')
            gscfgpath="/%s/g.wxmap.cfg.gsf"%(tmpprcdir)
        else:
            gscfgpath="/tmp/g.wxmap.cfg.gsf"

        print 'TTTTTTTTTTTTTTT ',dotest,gscfgpath
        O=open(gscfgpath,'w')
        O.writelines(cfg)
        O.close()

        if(dotest == 0):
            cmd="cp %s/*.gsf %s/."%(MP.prcdir,tmpprcdir)
            mf.runcmd(cmd,ropt)
            
            cmd="mv %s/%s %s"%(MP.prcdir,gsfinal,tmpprcdir)
            mf.runcmd(cmd,ropt)
            
            mf.ChangeDir(tmpprcdir)

            
        cmd="cat %s >> %s"%(gscfgpath,gsfinal)
        mf.runcmd(cmd,ropt)
        
        cmd="%s %s \"%s \" -g %dx%d"%(gradscmd,gmode,gcmd,MP.plotXsize,MP.plotYsize)
        mf.runcmd(cmd,ropt)

        if(dotest == 0):
            
            mf.ChangeDir(MP.prcdir)
            cmd="rm -r %s"%(tmpprcdir)
            mf.runcmd(cmd,ropt)


            
            
