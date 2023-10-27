#!/usr/bin/env python

from WxMAP2 import *
w2=W2()

wxModels2=Nwp2ModelsActiveW2flds
wxModels2offtimes=Nwp2ModelsActW20618

from tcbase import TcData,TcFtBtGsf

# -- local def for making gtime
#
def makeLocalGtimeGs(bdtg,btau=-48,etau=240,dtau=6,verb=0):
    gs="""
function setgtime()
"""
    for tau in taus:
        cdtg=mf.dtginc(bdtg,tau)
        lgtime=MF.getGtime4DTG(cdtg,local=1,verb=verb)    
        ugtime=MF.getGtime4DTG(cdtg,local=0,verb=verb)    

        ugs='''_ugtime.%s='%s'
'''%(tau,ugtime)
        gs=gs+ugs
        
        lgs='''_lgtime.%s='%s'
'''%(tau,lgtime)
        gs=gs+lgs
        if(verb):
            print 'll: ',dtg,lgtime
            print 'uu: ',dtg,ugtime
        
    gs=gs+'''return
'''
    return(gs)

# -- by dtg...varname > 16 chars...grads barfs...
#
    edtg=mf.dtginc(bdtg,etau)
    mdtg=mf.dtginc(bdtg,btau)
    dtgopt="%s.%s.%i"%(mdtg,edtg,dtau)
    dtgs=mf.dtg_dtgopt_prc(dtgopt)
        
    for dtg in dtgs:
        lgtime=MF.getGtime4DTG(dtg,local=1,verb=verb)    
        ugtime=MF.getGtime4DTG(dtg,local=0,verb=verb)    
        
        ugs='''_ugtime.%s='%s'
'''%(dtg,ugtime)
        gs=gs+ugs
        
        lgs='''_lgtime.%s='%s'
'''%(dtg,lgtime)
        gs=gs+lgs
        if(verb):
            print 'll: ',dtg,lgtime
            print 'uu: ',dtg,ugtime
        
    gs=gs+'''return
'''

    return(gs)


#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
#
# command line setup
#

class w2CmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv
        
        self.argv=argv

        self.argopts={
            1:['dtgopt',    'DTG (YYYYMMDDHH)'],
            2:['modelopt',  '''modelopt - all | gfs2,ecm2,fim8,fimx,ukm2,ngp2,cgd2'''],
            }
            
        self.defaults={
            'incrontab':0,
            'dow2flds':1,
            'docleanPlotsHtms':0,
            }

        self.options={
            'ropt':              ['N','','norun',' norun is norun'],
            'verb':              ['V',0,1,'verb=1 is verbose'],
            'override':          ['O',0,1,'1 - '],

            'areaopt':           ['a:','all','a','area: troplant...'],
            'plotopt':           ['p:','all','a','plotopt: all|...'],
            'tauopt':            ['t:','all','a','tauopt: all|...'],
            'ctltype':           ['c:','mand','a','tauopt: all|...'],
            'doarchive':         ['A:',0,'i','doarchive =0|1|2; 1 -- use /dat/nwp2/w2flds (i.e., for gfs2 and fim8 if data not on /public); 2 -- use /dat/nwp2'],
            'modelopt2':         ['2:',None,'a','second model .ctl? -- deprecated '],

            'dow2flds':          ['F',0,1,'use w2flds'],
            'dogribmap':         ['G',0,1,'otherwise -u in gribmap1'],
            'interact':          ['I',0,1,'q pos interactive'],
            'dotest':            ['T',0,1,'test mode'],
            'donocagips':        ['k',0,1,'no cagips data'],
            'doregen':           ['R',0,1,'regen to different dir'],
            'docleanplt':        ['C',0,1,'doclenplt'],
            }


        ptypes=w2.pnum.keys()
        ptypes.sort()
        pstring=MF.setList2String(ptypes)
        self.purpose='''
drive g.wxmap.base.gs grads plotting script for -p ptypes: 
%s'''%(pstring)
        
        self.examples="""
  %s bdtg[.edtg[.ddtg]] model -p 'all'|plot -t 'all'|tau -O
  %s cur-24.cur-6 all -O   -- redo all plots for a dtgrange, overwrite
  %s cur-6 gfs -a europe -p basemap       :: make basemap for europe
  %s cur-6 gfs -a europe -p basemap.topo  :: make basemap for europe with topo shading"""


#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# cmdline
#

argv=sys.argv

CL=w2CmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr


curpid=os.getpid()

#
# environment
#
prodcenter=w2.W2_PROD_CENTER
geodir=w2.W2_GEODIR
climosstdir=w2.W2_CLIMOSST
climodatdir=w2.W2_CLIMODAT
prcdir=w2.PrcDirFldanalW2
cfgdir=w2.PrcCfgBdirW2

basemapdir=w2.W2_BASEMAP_GDIR

if(doarchive > 0):
    w2.W2_BDIRWEB=w2.W2_BDIRWEBA


#
#  change dir to prc dir to setup cp to /tmp/prc dir
#
mf.ChangeDir(prcdir)

if(dtgopt == None):
    print 'EEE must set the dtg opt ...'
    sys.exit()

if(doregen):
    w2.W2BaseDirDat=w2.W2RegenBaseDirDat
    w2.W2_BDIRWEB=w2.W2RegenBaseDirWeb
    w2.W2_WEB_DIR=w2.W2RegenBaseDirWeb
    w2.W2_BDIRPLT=w2.W2RegenBaseDirPlt

minfracocn=0.5
minfracatm=0.85
if(modelopt == 'cgd2'): minfracatm=0.82

dtgs=mf.dtg_dtgopt_prc(dtgopt)

#
#mmmmmmmmmm model setup sssssssssssssssssssssssssssssssssssssssssss
#
model=modelopt

tt=modelopt.split('.')
jtwcopt=0
if(len(tt) == 2 and tt[1] == 'jtwc'):
    model=tt[0]
    jtwcopt=1
#
#cccccccccccccccccccccccccccccccccccccccccccccccccccc cycle by dtgs/models ccccccccccccccccccccccccccccccccccccc
#

if(len(dtgs) > 1 or modelopt == 'all' or len(modelopt.split(',')) > 1 ):
    
    #
    # more general dtg cycling
    #
    for dtg in dtgs:
        if(modelopt == 'all'):
            models=wxModels2
            if(w2.IsOffTime(dtg)): models=wxModels2offtimes
        elif(len(modelopt.split(',')) > 1):
            models=modelopt.split(',')
        else:
            models=[modelopt]

        for model in models:
            cmd="%s %s %s"%(pyfile,dtg,model)
            for o,a in CL.opts:
                cmd="%s %s %s"%(cmd,o,a)

            mf.runcmd(cmd,ropt)

    sys.exit()

else:
    dtg=dtgs[0]

MF.sTimer('w2plot-%s-%s'%(model,dtg))

# -- TcData setup based on dtg
#
tD=TcData(dtgopt=dtg)


#aaaaaaaaaa area setup asssssssssssssssssssssssssssssssssssssssssss
#
areas=[]
if(areaopt == 'all'):
    if(plotopt == 'clm'):
        areas=w2.W2_AREAS_CLIMO
    elif(plotopt == 'basemap' or plotopt == 'basemap.topo'):
        areas=w2.W2_AREAS_ALL
    else:
        areas=w2.W2_AREAS
        
elif(len(areaopt.split('.')) > 1):
    areas=areaopt.split('.')
elif(len(areaopt.split(',')) > 1):
    areas=areaopt.split(',')
else:
    areas=[areaopt]

#sssssssssssssssssssssssssssssssssssss single dtg sssssssssssssssssssssssssssssssssssssss
# -- model2?
#

#ttttttttttttttttttttttttttttttttttttccccccccccccccccccccccccccccccccc run the adeck to get all trackers
#

donwp2=w2.IsModel2(model)

ioklocal=1
dongpcagips=0

if(donwp2 and doarchive == 0):
    (ioklocal,minfracreq)=w2.Model2IsReady2Plot(model,dtg)


#
# bail if no data
#
if(ioklocal == -1):
    print "EEEEE4 no data for: %s at: %s"%(model,dtg)
    sys.exit()

elif(ioklocal == 0 and override == 0):
    print "EEEEE5 insufficient data for: %s at: %s minfrac: %3.2f"%(model,dtg,minfracreq)
    sys.exit()


# iiiiiiiiiiiiiiiiiii interaction
#
if(interact):
    gmode='-lc'
else:
    gmode='-lbc'

#pppppppp plot setup sssssssssssssssssssssssssssssssssssssssssssssss
#
if(plotopt == 'basemap' or plotopt == 'basemap.topo'):
    gdir=w2.W2_BASEMAP_GDIR
    gcdir=gdir

elif(modelopt == 'nr1'):
    gdir=w2.W2_WEB_DIR+'/clm/monthly'
    gcdir=gdir

elif(modelopt != 'all'):
    gcdir=w2.getW2_MODELS_CURRENT_GRFDIR(model)
    gdir=gcdir+'/%s'%(dtg)
    rc=mf.ChkDir(gdir,'mk')

#bbbbbbbbbbb basemap setup ssssssssssssssssssssssssssssssssssssssss
#
if(plotopt == 'basemap'):
    interact=1
    tauopt='000'
    override=1


#grfprc='gxyat'
grfprc='printim'
gsbase="g.wxmap.base.gs"
gsFinal="g.w1.%s.%s.gs"%(dtg,model)
gcmd="run %s"%(gsFinal)

# define the model for tc trackers (tcmodel) and plotting (pmodel)
#
if(donwp2):
    tcmodel=w2.Model2Model2TcModel(model)
    pmodel=w2.Model2Model2PlotModel(model)
else:
    tcmodel=model
    pmodel=model

datdir=w2.NwpDataBdir(model)
datdir2=w2.NwpDataBdir('ngp2')

rcG=setXgrads(returnBoth=1)
xpngquant=setPngquant()

for area in areas:

    MF.sTimer('w2plot-%s-%s-AREA-%s'%(model,dtg,area.upper()))
    
    xgradsX=rcG[0]
    xgrads=rcG[1]
    
    xgradsCmd=xgradsX
    #xgradsCmd='grads'
    dopngquant=0
    
    # -- 20200321 -- for reduced aeras do hi-qual grads
    #
    if(
        area == 'tropwpac' or 
        area == 'troplant' or 
        area == 'tropepac' or
        area == 'conus'
        ): 
        xgradsCmd=xgrads
        dopngquant=1

    # -- make basemap with topo shading
    #
    if(plotopt == 'basemap.topo'):
        cmd='''%s -lbc "makebg.gs %s"'''%(xgradsCmd,area)
        mf.runcmd(cmd,ropt)
        sys.exit()


    if(docleanplt):
        cmd="rm %s/*.%s.png"%(gdir,area)
        mf.runcmd(cmd,ropt)
        
    (xs,ys)=w2.PlotXsYs(model,area)
    
    if(plotopt == 'all'):
        try:
            plots=w2.plot_control[pmodel,area,'plots']
        except:
            print 'EEE PPPPPPPPPPP no plots in w2.plot_control for model',pmodel,' area: ',area
            plots=''
            
        plots=plots.split()
    else:
        plots=[plotopt]

    bmapdir=w2.W2_BASEMAP_GDIR
    bmapgif="%s/basemap.%s.gif"%(bmapdir,area)

    if(plotopt == 'basemap'):
        gname="%s/basemap.%s.png"%(gdir,area)
        print 'BBBBBBBBBBBBBBBBBB ',gname

    gradsruns=[]

    #--------------------------------------------------------------
    # use tau as the outer loop to try keeping decoded grib fields in memory cache
    # vice cycling by plots 
    #

    if(tauopt == 'all'):
        taus=w2.ModelPlotTaus(model,dtg)
    else:
        taus=[int(tauopt)]

    # -- go for day 5 tau since clm is tau=0-120 mean
    #
    if(plotopt == 'clm'):
        taus=[120]

    for tau in taus:
        for plot in plots:

            gmodname=w2.ModeltoGrfModel(model)
            if(plot != 'basemap'):
                gname="%s/%s.%s.%03d.%s.png"%(gdir,gmodname,plot,tau,area)
            try:
                mopt1=w2.plot_control[area,plot,'units']
            except:
                mopt1=''

            gtypeout=gname
             
            # -- climo params
            #
            if(plot == 'clm'):
                gtypeout=gdir
                mopt1=pmodel
                obttimes=range(-72,1,24)
                obttimes=[0]
            else:
                obttimes=[0]


            gradsrun="%s %s %s %s %s y %s %s %d %d %s"%(dtg,model,tau,area,
                                                        w2.pnum[plot],
                                                        gtypeout,grfprc,
                                                        xs,ys,mopt1)
            
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
        
        (myname,tack1,tack2,fullmod)=w2.TitleAck(model)

        #
        # record the plot event only if plots need to be made...
        #
        eventtype='plot'
        eventtag="START--- nrun: %4d"%(nrun)
        
        # -- get event cards to turn on adeck update
        #
        evtcards=w2.GetEvent(eventtype,model,dtg,areaopt)
        
        # -- put event card
        #
        w2.PutEvent(pyfile,eventtype,eventtag,model,dtg,areaopt,area)

        
        cmd="cat %s > %s"%(gsbase,gsFinal)
        mf.runcmd(cmd,ropt)

        if(model == 'ocn'): tcmodel='ngp2'

        tcsource='tmtrkN'
        if(tcsource == 'tmtrkN'):
            tcaids=['t'+model]
        elif(tcsource == 'mftrkN'):
            tcaids=['t'+model]
            
        MF.sTimer('TCs-%s'%dtg)
        dtxTC=6
        tBG=TcFtBtGsf(tcsource,tstmids=None,tdtg=dtg,taids=tcaids,
                      tD=tD,
                      dtx=dtxTC,
                      #ATtauRange='-12.0',BTtauRange='0',ATOtauRange=None,
                      ATtauRange='0',BTtauRange='0',ATOtauRange=None,
                      verb=verb)
        
        tBG.getABs()

            
        setgsf =tBG.makeSetTcGsf(obttimes=obttimes)
        btgsf  =tBG.makeTcFtBtGsf('bt')
        ftgsf  =tBG.makeTcFtBtGsf('ft')
        dbtgsf =tBG.makeDrawBtGsf()
        dftgsf =tBG.makeDrawFtGsf()

        btthere=1
        ftthere=1
        dotc=1
        
        if(len(tBG.tstmids) == 0): btthere=0 ; ftthere=0 ; dotc=0

        tcgsf=setgsf+btgsf+ftgsf+dbtgsf+dftgsf

        gsTcPath='%s/tc.gsf.%s.gs'%(w2.ptmpBaseDir,curpid)
        MF.WriteString2File(tcgsf,gsTcPath,verb=1)
        
        # cat tcposit .gsf to g.wxmap base to create driving script
        #
        cmd="cat %s >> %s"%(gsTcPath,gsFinal)
        mf.runcmd(cmd,ropt)
        os.unlink(gsTcPath)
        MF.dTimer('TCs-%s'%dtg)

        # -- gtime gs to set day of week and local time
        #
        btau=taus[0]
        etau=taus[-1]

        gsGtimePath='%s/gtime.%s.gs'%(w2.ptmpBaseDir,curpid)
        gsGtime=makeLocalGtimeGs(bdtg=dtg,btau=btau,etau=etau,verb=0)
        MF.WriteString2File(gsGtime,gsGtimePath,verb=1)
        cmd="cat %s >> %s"%(gsGtimePath,gsFinal)
        mf.runcmd(cmd,ropt)
        

        if(dongpcagips):
            specopt='cagips'
        elif(plotopt == 'basemap'):
            specopt=plotopt
        elif(dotest):
            specopt='test'
        else:
            specopt=''

        #
        # check if climo dat available
        #
        clmpath="%s/clm.25.%s.ctl"%(climodatdir,dtg)
        if(not(os.path.exists(clmpath))):  climodatdir='None'

        sstpath="%s/climobs_sst_clim.ctl"%(climosstdir)
        if(not(os.path.exists(sstpath))):  climosstdir='None'

        # -- donwp2 = w2flds
        #
        if(donwp2):

            modelres=0
            # -- 2nd model? haven't used in a long time
            #
            model2=model
            if(modelopt2 != None): model2=modelopt2
            modelres=w2.W2_MODELS_RES[modelopt]
            
            dtau=w2.Model2DdtgData(model,dtg)
            dtau=-dtau
            dtgm=mf.dtginc(dtg,dtau)

            if(model == 'ecmn'): ctltype=0
            if(model == 'ecmg'): ctltype=0
            if(model == 'fimx'): ctltype=0
            if(model == 'ngp2'): ctltype=0
            if(model == 'ngpc'): ctltype=0
            if(model == 'navg'): ctltype=0
            if(model == 'ecm2'): ctltype=0
            if(model == 'ecm4'): ctltype=0
            if(model == 'fv3e' or model == 'fv3g'): ctltype=0
            if(model == 'ukm2'): ctltype=0

            if(model == 'fimx'): dow2flds=0
            
            doarchiveflds=doarchive
            if(dow2flds):  doarchiveflds=1

            dpath=w2.Model2CtlPath(model,dtg,ctltype,doarchive=doarchiveflds)
            dpathm=w2.Model2CtlPath(model,dtgm,ctltype,doarchive=doarchiveflds)
            
            if(dpathm == None): dpathm=dpath
            dpath2=w2.Model2CtlPath(model2,dtg,ctltype,doarchive=doarchiveflds)
            rc=w2.getW2fldsRtfimCtlpath(model,dtg,details=0)

            if(dpath == None):
                print 'EEEEEEEEE no data for model: ',model,' at: ',dtg,' dpath: ',dpath,w2.Nwp2DataBdirModel(model)
                sys.exit()

        else:
            
            modelres=w2.W2_MODELS_RES[modelopt]
            model2=modelopt2
            dtau=w2.W2_MODELS_TauInc[modelopt]
            dtau=-dtau
            dtgm=mf.dtginc(dtg,dtau)
            ddir=w2.NwpDataBdir(model)
            dpath="%s/%s"%(ddir,w2.NwpDataFile(model,dtg)[0])
            dpathm="%s/%s"%(ddir,w2.NwpDataFile(model,dtgm)[0])
            dpath2="%s/%s"%(ddir,w2.NwpDataFile(model2,dtg)[0])
            

        prsource='qmorph'
        prdatdir="%s/pr_%s"%(w2.PrDatRoot,prsource)
        
        curtime=mf.dtg('cur.hm')
        cfg="""
function loadcfg()

_prdatdir=\'%s\'
_datdir=\'%s\'
_datdir2=\'%s\'
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
_res=%s

_bdtg=%s
_dtgp=incdtgh(_bdtg,%d)

_specopt='%s'

_btthere=%d
_ftthere=%d
_dotc=%d

_curtime=\'%s\'
_dopngquant=%d
_xpngquant=\'%s\'

# -- get global gtime var
#
rc=setgtime()

"""%(
            prdatdir,
            datdir,
            datdir2,
            geodir,
            climosstdir,
            climodatdir,
            prcdir,
            cfgdir,
            basemapdir,
            tack1,
            tack2,
            fullmod,
            nrun,
            interact,
            modelopt,
            modelopt2,
            modelres,
            dtg,
            dtau,
            specopt,
            btthere,
            ftthere,
            dotc,
            curtime,
            dopngquant,
            xpngquant,
            )
    

        cfg=cfg+"""
dpath='%s'
dpathm='%s'
dpath2='%s'

_fnf=ofile(dpath)
_fnfp=ofile(dpathm)
_fnfmod2=ofile(dpath2)

"""%(dpath,dpathm,dpath2)

        #
        # regrid?
        #
        
        doregrid=0
        if(plotopt == 'clm'): doregrid=1
            
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
# -- setup the tcs
return

#--- dummy localvar
function localvar()
return

#--- dummy prvar
function prvar()
return

"""

        if(dotest == 0):
            tmpprcdir="%s.%s.%s.%s"%(w2.W2TmpPrcDirPrefix,model,dtg,curpid)
            mf.ChkDir(tmpprcdir,'mk')
            gscfgpath="/%s/g.wxmap.cfg.gsf"%(tmpprcdir)
        else:
            gscfgpath="/tmp/g.wxmap.cfg.gsf"

        print 'TTTTTTTTTTTTTTT ',dotest,gscfgpath
        O=open(gscfgpath,'w')
        O.writelines(cfg)
        O.close()

        if(dotest == 0):
            cmd="cp %s/*.gsf %s/."%(prcdir,tmpprcdir)
            mf.runcmd(cmd,ropt)
            
            cmd="mv %s/%s %s"%(prcdir,gsFinal,tmpprcdir)
            mf.runcmd(cmd,ropt)
            
            mf.ChangeDir(tmpprcdir)

            
        cmd="cat %s >> %s"%(gscfgpath,gsFinal)
        mf.runcmd(cmd,ropt)
        
        cmd="%s %s \"%s \" -g %dx%d"%(xgradsCmd,gmode,gcmd,xs,ys)
        mf.runcmd(cmd,ropt)

        if(dotest == 0):
            
            eventtag="  END--- nrun: %4d"%(nrun)
            w2.PutEvent(pyfile,eventtype,eventtag,model,dtg,areaopt,area)

            mf.ChangeDir(prcdir)

            cmd="rm -r %s"%(tmpprcdir)
            mf.runcmd(cmd,ropt)

    MF.dTimer('w2plot-%s-%s-AREA-%s'%(model,dtg,area.upper()))

            
MF.dTimer('w2plot-%s-%s'%(model,dtg))            
