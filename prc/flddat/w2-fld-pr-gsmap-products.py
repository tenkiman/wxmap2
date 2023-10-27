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
        if(verb): print line
        if(mf.find(line,'RRRCCC')): print line
        if(mf.find(line,'WWWWWW no data') or mf.find(line,'Open Error')): 
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
        dtg=ffile.split('_')[2][0:10]
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
            
    return(pdtgs)


def MakeProductCtl(pdir,pbase,bdtg,thours,tbdir,ddtg=6,setYear=None):

    if(setYear != None):
        
        bdtg="%s010100"%(setYear)
        edtg="%s123118"%(setYear)
        dtgopt="%s.%s.%d"%(bdtg,edtg,ddtg)
        dtgs=mf.dtg_dtgopt_prc(dtgopt)
        tsteps=len(dtgs)+1
        # -- add 72 h
        #
        tsteps=tsteps+72/ddtg
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
    
    ctl="""dset %s
index %s
undef 9.999E+20
title prq_a06h_2009031812.grb
*  produced by grib2ctl v0.9.12.5p16
dtype grib 255
options template
ydef  480 linear -59.875000 0.25
xdef 1440 linear 0.125000 0.250000
tdef   %d linear %s %dhr
zdef 1 linear 1 1
vars 1
pr  0 59,1,0  ** Precipitation rate [kg/m^2/s]
ENDVARS"""%(dset,index,tsteps,gtime,ddtg)

    C=open(ctlpath,'w')
    C.writelines(ctl)
    C.close()
    return(ctlpath)
    
def makeYearCtl(grbdir,pbase,bdtg,thours,tbdirProd,setYear,ropt=''):
    MF.sTimer('GGGMMM-%s'%(setYear))    
    pctl=MakeProductCtl(grbdir,pbase,bdtg,thours,tbdir=tbdirProd,
                        setYear=setYear)
            
    grbopt=''
    cmd="gribmap %s -i %s"%(grbopt,pctl)
    mf.runcmd(cmd,ropt)
    MF.dTimer('GGGMMM-%s'%(setYear))    
    

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
            }

        self.options={
            'override':         ['O',0,1,'override'],
            'verb':             ['V',0,1,'verb=1 is verbose'],
            'ropt':             ['N','','norun',' norun is norun'],
            'doCtlOnly':        ['g',0,1,"""just make ctl/gribmap"""],
            'doDatOnly':        ['D',0,1,'make or ln -s V6 only'],
            'doYearCtlOnly':    ['Y',0,1,'make or ln -s V6 only'],
            'makeV6':           ['6',0,1,'make or ln -s V6 only'],
            'doGauge':          ['G',0,1,'only do gribmap'],

            }

        self.purpose='''
make cpc qmorph products'''

        self.examples="""
%s cur"""


#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
# -- main
#
argv=sys.argv
CL=WgetCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

dtgs=mf.dtg_dtgopt_prc(dtgopt)

MF.sTimer('all')


#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
# -- main loop
# -- set xgrads
#
xgrads=setXgrads(useStandard=0, useX11=1, returnBoth=0)

pdir=w2.PrcDirFlddatW2

sbdir     =w2.PrGsmapDatRoot
sbdirV6   =w2.PrGsmapV6DatRoot
sbdirV6G  =w2.PrGsmapV6GDatRoot
    
tbdir     =w2.PrGsmapProducts
tbdirV6   =w2.PrGsmapV6Products
tbdirV6G  =w2.PrGsmapV6GProducts

grbdir    =w2.PrGsmapProductsGrib
grbdirV6  =w2.PrGsmapV6ProductsGrib
grbdirV6G =w2.PrGsmapV6GProductsGrib

if(makeV6):
    if(doGauge):
        sbdir=sbdirV6G
        tbdir=tbdirV6G
        grbdir=grbdirV6G
        source='gsmapV6-Grev'
    else:
        sbdir=sbdirV6
        tbdir=tbdirV6
        grbdir=grbdirV6
        source='gsmapV6'
else:
    source    ='gsmap'

prodpre="pr%s"%(source[0])
    
#MF.ChkDir(grbdir,'mk')
    

# -- use yearly .ctl if old...
#
#if(setYear != None and not(doCmorphV10)):
#    if(mf.find(setYear,'cur')): setYear=curdtg[0:4]
#    gadpath="%s/%s-%s.ctl"%(tbdir,source,setYear)

pbases=['prg_a06h','prg_a12h']
pbases=['prg_a06h']
pbase=pbases[0]

curhrdtg=mf.dtg('dtgcurhr')

#gggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggg
# 
# grib

setYear=dtgs[0][0:4]
thours=None

MF.sTimer('AAA-%s'%(setYear))

if(doYearCtlOnly):
    rc=makeYearCtl(grbdir,pbase,dtgs[0],thours,tbdir,setYear,ropt)
    MF.dTimer('AAA-%s'%(setYear))
    sys.exit()
    

pdtgs=GetExistingDtgs(grbdir,dtgs,pbase,thours)

for dtg in dtgs:

    if(dtg in pdtgs):
        print 'already run for dtg: ',dtg
        if(not(override)):
            continue
    
    year=dtg[0:4]
    yymmddhh=dtg[4:10]
    yyyymmdd=dtg[0:8]
    syear=year

    grbdiryy="%s/%s"%(grbdir,syear)
    MF.ChkDir(grbdiryy,'mk')
    
    gadpath="%s/%s-%s.ctl"%(sbdir,source,year)

    os.chdir(pdir)
    (base,ext)=os.path.splitext(pyfile)
    gscmd="%s.gs"%(base)
    cmd="%s -lbc \"%s %s %s %s/%s\""%(xgrads,gscmd,dtg,gadpath,grbdiryy,prodpre)
    #mf.runcmd(cmd,ropt)
    
    lines=MF.runcmdLog(cmd,ropt)
    rc=parseGradsLog(lines,verb=verb)

    if(rc == 0):
        if(rc): rcGrib=0
        print 'WWW-%s -- no data for: %s  dtg: %s'%(pyfile,prodpre,dtg)
        continue
        
if(doDatOnly):
    print 'DDD -- only dat no yearctl...'
    MF.dTimer('AAA-%s'%(setYear))
    sys.exit()

rc=makeYearCtl(grbdir,pbase,dtgs[0],thours,tbdir,setYear,ropt)

MF.dTimer('AAA-%s'%(setYear))

sys.exit()
    

