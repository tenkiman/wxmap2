#!/usr/bin/env python

from WxMAP2 import *
w2=W2()

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
            'model':'gfs2',
        }

        self.options={
            'resopt':     ['L',0,1,'low-res grid resolution'],
            'override':   ['O',0,1,'override'],
            'skipDowget': ['W',0,1,'skip wget just make inventory'],
            'verb':       ['V',0,1,'verb=1 is verbose'],
            'ropt':       ['N','','norun',' norun is norun'],
            'tauopt':     ['t:',None,'a','set taus as tau1,tau2,...'],
            'noRunChk':   ['R',0,1,"""if 1 -- don't if running"""],
        }

        self.purpose='''
purpose -- wget mirror cmc gdps global grids to w2flds
%s cur
'''
        self.examples='''
%s cur
'''

def makeCtl(model,dtg,ropt=''):

    ctlpath="%s.w2flds.%s.ctl"%(model,dtg)

    gtime=mf.dtg2gtime(dtg)
    ntimes=41
    
    grid="""ydef 751 linear   -90.0 0.24
xdef 1500 linear -180.0 0.24"""
    
    # -- 2021092812 new hi res
    #
    grid="""ydef 1201 linear   -90.0 0.15
xdef 2400 linear -180.0 0.15"""

    if(model == 'cgd6'): 
        ntimes=25
        grid="""ydef 301 linear  -90.0 0.6
xdef 601 linear -180.0 0.6"""

    ctl="""dset  ^%s.w2flds.%s.f%%f3.grb2
index ^cgd2.w2flds.%s.gmp2
undef 9.999E+20
title cgd2.w2flds.2013062700.f006.grb2
*  produced by g2ctl v0.0.4m
* griddef=1:0:(601 x 301):grid_template=0:winds(N/S): lat-lon grid:(601 x 301) units 1e-06 input WE:SN output WE:SN res 48 lat -90.000000 to 90.000000 by 0.600000 lon 180.000000 to 180.000000 by 0.600000 #points=180901:winds(N/S)
dtype grib2
%s
tdef %s linear  %s 6hr
* PROFILE hPa
zdef 12 levels 100000 92500 85000 70000 50000 40000 30000 25000 20000 15000 10000 5000
options pascals template
vars 10
prc    0,1,0      0,1,10,1 ** surface Convective Precipitation [kg/m^2]
pr     0,1,0      0,1,8,1 ** surface Total Precipitation [kg/m^2]
uas    0,103,10   0,2,2 ** 10 m above ground U-Component of Wind [m/s]
vas    0,103,10   0,2,3 ** 10 m above ground V-Component of Wind [m/s]
psl    0,101      0,3,1 ** mean sea level Pressure Reduced to MSL [Pa]
zg    12,100      0,3,5 ** (1000 925 850 700 500.. 250 200 150 100 50) Geopotential Height [gpm]
hus   12,100      0,1,0 ** (1000 925 850 700 500.. 250 200 150 100 50) Specific Humidity [kg/kg]
ta    12,100      0,0,0 ** (1000 925 850 700 500.. 250 200 150 100 50) Temperature [K]
ua    12,100      0,2,2 ** (1000 925 850 700 500.. 250 200 150 100 50) U-Component of Wind [m/s]
va    12,100      0,2,3 ** (1000 925 850 700 500.. 250 200 150 100 50) V-Component of Wind [m/s]
ENDVARS"""%(model,dtg,dtg,grid,ntimes,gtime)

    rc=MF.WriteString2File(ctl,ctlpath,verb=1)
    cmd="gribmap -v -i %s"%(ctlpath)
    mf.runcmd(cmd,ropt)




#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
# main
#


MF.sTimer(tag='wget.cmc.gdps')


CL=WgetCmdLine(argv=sys.argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

# -- check if running -- takes a long time these days? slow net?; bigger files?
#
MF.sTimer(tag='chkifrunning')
rc=w2.ChkIfRunningNWP(dtg=None,pyfile=pyfile,model=None,verb=1)

if(rc > 1 and not(noRunChk)):
    print 'AAA allready running...'
    sys.exit()
    
if(resopt):
    gridres='6'
    model='cgd6'
else:
    gridres='24'
    model='cgd2'
    
    # -- 2021092812 -- now 15km!
    #
    gridres='15'

tbdir="%s/nwp2/w2flds/dat/%s"%(w2.W2BaseDirDat,model)

sbdir='https://dd.weather.gc.ca/model_gem_global/66km/grib2/lat_lon'

# 0.6 deg
#
etau=144
dtau=6
taus=range(0,etau+1,dtau)

# 0.24 deg
#
if(gridres == '24'): 
    sbdir='https://dd.weather.gc.ca/model_gem_global/25km/grib2/lat_lon'
    etau=240
    taus=range(0,144+1,6)+range(156,etau+1,12)

# 0.1? deg
#
if(gridres == '15'): 
    sbdir='https://dd.weather.gc.ca/model_gem_global/15km/grib2/lat_lon'
    etau=240
    taus=range(0,144+1,6)+range(156,etau+1,12)
    
if(tauopt != None):
    taus=[]
    itaus=tauopt.split(',')
    for itau in itaus:
        taus.append(int(itau))


print taus

sfcvars=['UGRD_TGL_10','VGRD_TGL_10','ACPCP_SFC_0','APCP_SFC_0','PRMSL_MSL_0']
uavars=['HGT_ISBL','UGRD_ISBL','VGRD_ISBL','TMP_ISBL','SPFH_ISBL']
plevs=[1000,925,850,700,500,400,300,250,200,150,100,50]

dtgs=mf.dtg_dtgopt_prc(dtgopt,ddtg=12)

if(len(dtgs) > 1):
    # cycle by dtgs
    #
    for dtg in dtgs:
        cmd="%s %s"%(pypath,dtg)
        for o,a in CL.opts:
            if(o != '-C'):
                cmd="%s %s %s"%(cmd,o,a)
                
        cmd="%s -R"%(cmd)

        mf.runcmd(cmd,ropt)

    sys.exit()
    
dtg=dtgs[0]
hh=dtg[8:10]

tdir="%s/%s"%(tbdir,dtg)
MF.ChkDir(tdir,'mk')

mf.ChangeDir(tdir)

#mf.makeCtl(model,dtg)
#sys.exit()

invThere={}
invHere={}

allthere=1

alldoneFiles=glob.glob("alldone*")

if(len(alldoneFiles) > 0):
    print 'WWW alldone: ',alldoneFiles[-1],' sayoonara unless override...'
    if(not(override)): sys.exit()

wgetOpt="-nv -m -nd -T 180 -t 10 -l1 --auth-no-challenge"
for tau in taus:

    sdir="%s/%s/%03d"%(sbdir,hh,tau)

    invThere[tau]=[]
    invHere[tau]=[]

    for sfcvar in sfcvars:
        filename="CMC_glb_%s_latlon.%sx.%s_%s_P%03d.grib2"%(sfcvar,gridres,gridres,dtg,tau)
        if(tau == 0 and mf.find(sfcvar,'PCP')): continue

        MF.appendDictList(invThere,tau,filename)
        dowget=1
        if(MF.getPathSiz(filename) > 0): 
            MF.appendDictList(invHere,tau,filename)
            dowget=0

        if(dowget and not(skipDowget) ): 
            cmd="""wget %s %s/%s """%(wgetOpt,sdir,filename)
            mf.runcmd(cmd,ropt)
            MF.appendDictList(invHere,tau,filename)

    for uavar in uavars:
        for plev in plevs:
            filename="CMC_glb_%s_%d_latlon.%sx.%s_%s_P%03d.grib2"%(uavar,plev,gridres,gridres,dtg,tau)  
            MF.appendDictList(invThere,tau,filename)
            dowget=1
            if(MF.getPathSiz(filename) > 0): 
                MF.appendDictList(invHere,tau,filename)
                dowget=0

            if(dowget and not(skipDowget)):                
                cmd="""wget %s %s/%s """%(wgetOpt,sdir,filename)
                mf.runcmd(cmd,ropt)
                MF.appendDictList(invHere,tau,filename)

    lH=len(invHere[tau])
    lT=len(invThere[tau])

    if(lH != lT): 
        print 'WWW allthere = 0 for model: ',model,' dtg: ',dtg,' tau: ',tau
        allthere=0


print 'AAAAAA allthere: ',allthere

if(not(allthere) and not(skipDowget)):
    print 'WWW still need files...'
    sys.exit()

# -- cat individual files to files by tau
#

for tau in taus:

    #tmask="*%sx.%s*P%03d.grib2"%(gridres,gridres,tau)
    otaufile="%s.w2flds.%s.f%03d.grb2"%(model,dtg,tau)
    #taufiles=glob.glob(tmask)

    taufiles=invHere[tau]
    for tfile in taufiles:
        try:
            cmd="cat %s >> %s"%(tfile,otaufile)
            mf.runcmd(cmd,ropt)
            if(ropt != 'norun'): 
                os.unlink(tfile)
            else:
                print 'KKK unlink %s'%(tfile)
        except:
            print 'WWWW unable to cat tfile: ',tfile
            continue

# -- touch file to indicate alldone
#
curtime=mf.dtg('curtime')
curtime=curtime.replace(' ','')
curtime=curtime.replace(',','')
cmd="touch alldone-%s-%s--%s--txt"%(model,dtg,curtime)
mf.runcmd(cmd,ropt)

# -- do the grads .ctl
#
rc=makeCtl(model,dtg)


MF.dTimer(tag='wget.cmc.gdps')
