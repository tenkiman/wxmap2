#!/usr/bin/env python

from M import *
MF=MFutils()

from WxMAP2 import *
w2=W2()


#llllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll
#
#  local defs
#

def parseGradsLog(lines,verb=0):
    rc=1
    for line in lines:
        if(verb): print line[0:-1]
        if(mf.find(line,'WWWWWW no data')): 
            rc=0
            return(rc)
    return(rc)

            
def GetExistingDtgs(pdir,dtgs,pbase,thours=None):

    pdtgs=[]
    dpaths=[]
    
    for dtg in dtgs:
        year=dtg[0:4]
        yymmdd=dtg[0:8]
        mask="%s/%s/%s_%s??.grb"%(pdir,year,pbase,yymmdd)
        dpaths=dpaths+glob.glob(mask)
        
    dpaths=mf.uniq(dpaths)
    dpaths.sort()

    for dpath in dpaths:
        (ddir,ffile)=os.path.split(dpath)
        dtg=ffile.split('_')[3][0:10]
        pdtgs.append(dtg)

    if(len(pdtgs) == 0):
        pdtgb=curdtg
        thours=0
    else:
        pdtgb=pdtgs[0]
        pdtge=pdtgs[-1]
        if(thours != None):
            pdtgb=mf.dtginc(pdtge,-thours)
        else:
            thours=mf.dtgdiff(pdtgb,pdtge)

    return(pdtgb,thours)


def MakeProductCtl(pdir,pbase,bdtg,thours,tbdir,ddtg=6,
                   nx=720,ny=361,dlon=0.5,dlat=0.5,
                   setYear=None,
                   ):

    if(setYear != None):
        
        bdtg="%s010100"%(setYear)
        edtg="%s122318"%(setYear)
        dtgopt="%s.%s.%d"%(bdtg,edtg,ddtg)
        dtgs=mf.dtg_dtgopt_prc(dtgopt)
        tsteps=len(dtgs)+1
        
        dset="^grib/%%y4/%s_%%y4%%m2%%d2%%h2.grb"%(pbase)
        index="^%s-%s.gmp1"%(pbase,setYear)
        
        ctlpath="%s/%s-%s.ctl"%(tbdir,pbase,setYear)
        gtime=mf.dtg2gtime(bdtg)
        
    else:

        dset="^grib/%%y4/%s_%%y4%%m2%%d2%%h2.grb"%(pbase)
        index="^%s.gmp1"%(pbase)
        ctlpath="%s/%s.ctl"%(tbdir,pbase)
        tsteps=int(thours/ddtg)+1
        gtime=mf.dtg2gtime(bdtg)


    # -- make the ctl
    #
    ctl="""dset %s
index %s
undef 9.999E+20
title prq_a06h_2009031812.grb
*  produced by grib2ctl v0.9.12.5p16
dtype grib 255
options template
xdef %3d linear   0.0 %5.2f
ydef %3d linear -90.0 %5.2f
tdef   %d linear %s %dhr
zdef 1 linear 1 1
vars 1
pr  0 59,1,0  ** Precipitation rate [kg/m^2/s]
ENDVARS"""%(dset,index,
            nx,dlon,
            ny,dlat,
            tsteps,gtime,ddtg)

    C=open(ctlpath,'w')
    C.writelines(ctl)
    C.close()
    return(ctlpath)
    


#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
#
# command line setup
#

class WgetCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv
        
        self.argv=argv
        self.argopts={
            1:['dtgopt',    'no default'],
            }

        self.defaults={
            'prcopt':'all',
            'doHiFreqChk':0,
            'dogribmap':1,
            }

        self.options={
            'override':         ['O',0,1,'override'],
            'verb':             ['V',0,1,'verb=1 is verbose'],
            'ropt':             ['N','','norun',' norun is norun'],
            'doCtlOnly':        ['G',0,1,"""just make ctl/gribmap"""],
            'sourceopt':        ['S:',None,'a',' [qmorph]|cmorph'],
            'ndaybackgribmap':  ['n:',None,'i',' ndayback to process'],
            'doCtlOnly':        ['G',0,1,"""just make ctl/gribmap"""],
            'doScpJet':         ['J',0,0,"""NEVER scp to jet"""],
            'setYear':          ['Y:',None,'a',"""force using yearly files for 30min data"""],
            'dogribmapupdate':  ['u',0,1,"""do update in gribmap (doesn't work for grads2)"""],
            }

        self.purpose='''
make cpc qmorph products'''

        self.examples="""
%s cur"""


argv=sys.argv
CL=WgetCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

dtgs=mf.dtg_dtgopt_prc(dtgopt)


MF.sTimer('all-global')
#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#   main loop

# -- set xgrads
#
xgrads=setXgrads(useStandard=0, useX11=1, returnBoth=0)

wjetlogin=w2.WjetScpServerLogin
wjetserver=w2.WjetScpServer
wjetqdir=w2.WjetQmorphDir

if(mf.find(dtgopt,'ops')):
    #
    # use 'ops6' in mf.py
    #

    doOldOps=0
    if(doOldOps):
        #
        # nhc ops
        #
        ndayback=2
        curdtg12=curdtg[0:8]+'12'
        dtgback=mf.dtginc(curdtg12,-24*ndayback)
        dtgopt="%s.cur+5.1"%(dtgback)
        dtgopt="%s.cur"%(dtgback)

        #
        # gsd ops
        #

        if(float(curphr) > 5.0):
            dtgopt='cur'
        else:
            dtgopt='cur-6'


dtgs=mf.dtg_dtgopt_prc(dtgopt)

#llllllllllllllllllllllllllll loop through sources:
#
# 
#
if(sourceopt == None):
    sources=['qmorph','cmorph']
    for source in sources:
        cmd="%s %s"%(pypath,dtgopt)
        for o,a in CL.opts:
            cmd="%s %s %s"%(cmd,o,a)
        cmd="%s -S %s"%(cmd,source)
        mf.runcmd(cmd,ropt)

    sys.exit()

elif(sourceopt == 'qmorph' or sourceopt == 'cmorph'):
    source=sourceopt

if(source == 'qmorph'):
    pbases=['prq_a06h','prq_a12h']
elif(source == 'cmorph'):
    pbases=['prc_a06h','prc_a12h']
    

curhrdtg=mf.dtg('dtgcurhr')

pdir=w2.PrcDirFlddatW2
tbdir="%s/%s"%(w2.PrDatRoot,source)
tbdirProd="%s/pr_%s"%(w2.PrDatRoot,source)

sdir="%s/%s"%(w2.PrDatRoot,source)

if(source == 'qmorph'):
    grbdir=w2.NhcQmorphProductsGrib
    gadpath="%s%s.ctl"%(sdir,source)
    prodpre="pr%s"%(source[0])
    
elif(source == 'cmorph'):
    grbdir=w2.NhcCmorphProductsGrib
    gadpath="%s%s.ctl"%(sdir,source)
    prodpre="pr%s"%(source[0])


# -- use yearly .ctl if old... new structure on tenki7
#
if(setYear != None):
    if(mf.find(setYear,'cur')): setYear=curdtg[0:4]
    gadpath="%s/%s-%s.ctl"%(tbdirProd,source,setYear)
    
acps=[6,12]

for dtg in dtgs:

    year=dtg[0:4]
    ogrbmask="%s/%s/%s_*_global_%s.grb"%(grbdir,year,prodpre,dtg)
    ogrbpaths=glob.glob(ogrbmask)

    if(verb):
        if(len(ogrbpaths) > 0):
            for ogrbpath in ogrbpaths:
                print 'already processed: ',ogrbpath

    rcGrib=0
    if(len(ogrbpaths) == 0 or override):

        rcGrib=1
        for acp in acps:
            os.chdir(pdir)
            (base,ext)=os.path.splitext(pyfile)
            gscmd="%s.gs"%(base)
            
            ibase="%s/%s"%(tbdirProd,prodpre)
            if(setYear != None):
                prodpre="pr%s"%(source[0])
                ibase="%s/%s"%(tbdirProd,prodpre)

            obase="%s/%s/%s"%(grbdir,year,prodpre)
            cmd="%s -lbc \"%s %s %s %s %s %s\""%(xgrads,gscmd,dtg,ibase,obase,acp,setYear)
            lines=MF.runcmdLog(cmd,ropt)
            rc=parseGradsLog(lines,verb=verb)
            
            if(rc == 0):
                if(rcGrib): rcGrib=0
                print 'WWW-%s -- no data for: %s  dtg: %s'%(pyfile,acp,dtg)
                continue

            # -- 20090731 -- do scp to wjet for jeff whitaker
            #
            if(doScpJet):
                cmd="scp %s %s@%s:%s/."%(ogrbmask,wjetlogin,wjetserver,wjetqdir)
                mf.runcmd(cmd,ropt)

    ogrbpaths=glob.glob(ogrbmask)


if(override): dogribmapupdate=0
if( (dogribmap and rcGrib) or doCtlOnly):
    
    for pbase in pbases:

        pbase="%s_global"%(pbase)

        if(ndaybackgribmap != None): 
            thours=24*ndaybackgribmap
        else:
            thours=None
            
        (bdtg,thours)=GetExistingDtgs(grbdir,dtgs,pbase,thours)

        pctl=MakeProductCtl(grbdir,pbase,bdtg,thours,tbdir=tbdirProd,
                            setYear=setYear)
        
        grbopt=''
        if(dogribmapupdate): grbopt='-u'
        cmd="gribmap %s -E -0 -i %s"%(grbopt,pctl)
        mf.runcmd(cmd,ropt)
        
MF.dTimer('all-global')
sys.exit()
    

