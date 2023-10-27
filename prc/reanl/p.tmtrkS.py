#!/usr/bin/env python

from WxMAP2 import *
w2=W2()

from TCtrkS import TmTrkSimple

tbdir='/dat6/dat/reanl/erai/fc/tmtrkN'

abdirStm='%s/adeck-stm'%(tbdir)
MF.ChkDir(abdirStm,'mk')

abdir='%s/adeck-dtg'%(tbdir)
ptable=None

ebdir='/dat6/dat/reanl/erai/fc'

def makeCtlErai(dtg,ropt='',dorm=1,override=0):

    grbs=glob.glob("%s/%s/*.grb"%(ebdir,dtg))
    tgrb="%s/%s/erai.%s.grb"%(ebdir,dtg,dtg)
    ctlpath="%s/%s/erai.%s.ctl"%(ebdir,dtg,dtg)
    gmppath="%s/%s/erai.%s.gmp"%(ebdir,dtg,dtg)
    
    siztgrb=MF.getPathSiz(tgrb)
    siztgmp=MF.getPathSiz(gmppath)

    if(siztgrb <= 0 or override):

        for grb in grbs:
            print grb
            cmd="cat %s >> %s"%(grb,tgrb)
            mf.runcmd(cmd,ropt)
            if(dorm):
                rmcmd="rm %s"%(grb)
                mf.runcmd(rmcmd,ropt)

    if(siztgmp <= 0 or override):
        
        gtime=mf.dtg2gtime(dtg)

        ctl="""dset ^erai.%s.grb
index ^erai.%s.gmp
undef 9.999E+20
title erai.2012102312.ua.an.grb
*  produced by grib2ctl v0.9.12.5p16
dtype grib 255
options yrev
ydef 241 linear -90.0 0.75
xdef 480 linear   0.0 0.75
tdef 21 linear %s 12hr
zdef 9 levels
1000 925 850 700 500 400 300 200 100
vars 11
uas   0 165,1,0  ** 10 metre wind component [m s**-1]
vas   0 166,1,0  ** 10 metre V wind component [m s**-1]
prc   0 143,1,0  ** Convective precipitation [m]
psl   0 151,1,0  ** Mean sea-level pressure [Pa]
prw   0 137,1,0  ** Total column water vapour [kg m**-2]
pr    0 228,1,0  ** Total precipitation [m]
hur   9 157,100,0 ** Relative humidity [%%]
ta    9 130,100,0 ** Temperature [K]
ua    9 131,100,0 ** velocity [m s**-1]
va    9 132,100,0 ** V velocity [m s**-1]
zg    9 129,100,0 ** Geopotential [m**2 s**-2]
ENDVARS"""%(dtg,dtg,gtime)

        MF.WriteString2File(ctl,ctlpath)
        cmd="gribmap -v -i %s"%(ctlpath)
        mf.runcmd(cmd,ropt)

    rc=1
    return(rc)
    

#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# command line setup
#

class TmtrkCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv

        self.argv=argv
        self.argopts={
            1:['dtgopt',    'dtgopt'],
        }

        self.options={
            'override':         ['O',0,1,'override'],
            'verb':             ['V',0,1,'verb=1 is verbose'],
            'ropt':             ['N','','norun',' norun is norun'],
            'doclean':          ['C',1,0,'1 do NOT clean'],            

        }

        self.purpose="""
run TmTrkSimple for the fim7 subseasonal"""

        self.examples='''
%s 2002 '''

#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# main
#

# -----------------------------------  default setting of max taus
#
maxtau=168
mintauTC=132

argv=sys.argv
CL=TmtrkCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr


dtgs=mf.dtg_dtgopt_prc(dtgopt)

override=0
model='erai'
atcfname='erai'

regridTracker=0.5

#regridTracker=1.0
#atcfname='era1'

maxtau=240
dtau=6
max6h=48
max12h=240
taus=range(0,max6h+1,6)+range(max6h+12,max12h+1,12)

for dtg in dtgs:

    grbpath="%s/%s/%s.%s.grb"%(ebdir,dtg,model,dtg)
    ctlpath="%s/%s/%s.%s.ctl"%(ebdir,dtg,model,dtg)
    sizgrb=MF.getPathSiz(grbpath)
    sizctl=MF.getPathSiz(ctlpath)

    print 'qqqq',grbpath,sizgrb

    if((sizgrb <= 0 or sizctl <=0) or override):
        rc=makeCtlErai(dtg,override=override)
        if(rc != 1):
            print 'EEEE in makeCtlErai...'
            sys.exit()


    MF.sTimer("all-%s"%(dtg))

    tdirAdeck='%s/%s'%(abdir,dtg)
    MF.ChkDir(tdirAdeck,'mk')
    
    tdir='%s/%s'%(tbdir,dtg)
    MF.ChkDir(tdir,'mk')

    MF.sTimer('tmtrkN-base-%s-%s'%(model,dtg))
    TT=TmTrkSimple(dtg,
                   model,
                   atcfname,
                   tdir,
                   ctlpath,
                   taus,
                   tdirAdeck=tdirAdeck,
                   tbdirAdeckStm=abdirStm,
                   ptable=ptable,
                   doclean=doclean,
                   regridTracker=regridTracker,
                   verb=verb,
                   )
    MF.dTimer('tmtrkN-base-%s-%s'%(model,dtg))
    

    MF.sTimer('tmtrkN-doTrk-%s-%s'%(model,dtg))
    TT.doTrk(override=override,ropt=ropt)
    MF.dTimer('tmtrkN-doTrk-%s-%s'%(model,dtg))
    
    MF.dTimer("all-%s"%(dtg))

