import os
import sys
import mf
import copy
import glob
import time

gsdGribSrcDir='/model/gsd/GRIB'
gsdGribSrcDir='/tmp/gsd/data/model/gsd/GRIB'
gsdGribTargetDir='/wxmap2/dat/nwp/gsd'


modelres={
    'fim8':'05',
    'fim9':'05'
    }


def gribmap(tpath,ropt=''):

    (dir,file)=os.path.split(tpath)

    tt=file.split('.')

    dtg=tt[2]

    (base,ext)=os.path.splitext(file)

    gmpfile="%s.gmp"%(base)
    ctlfile="%s.ctl"%(base)
    grbfile=file

    ctlpath="%s/%s"%(dir,ctlfile)
    gmppath="%s/%s"%(dir,gmpfile)

    gtime=mf.dtg2gtime(dtg)

    levs=[850,700,500,200]
    
    nl=len(levs)

    zlevcard="zdef %d levels"%(nl)

    for lev in levs:
        zlevcard=zlevcard+" %d"%(lev)

    ctl="""dset ^%s
index ^%s
undef 9.999E+20
title gsd fim
options yrev
dtype grib 
xdef 720 linear   0.0 0.5
ydef 361 linear -90.0 0.5
tdef  81 linear %s 3hr
%s
vars 9
prc  0  63,1,1  ** Convective precipitation [kg/m^2]
zg   %d   7,100,0  ** Geopotential height [gpm]
psl  0 129,102,1  ** Mean sea level pressure (MAPS) [Pa]
prl  0  62,1,1  ** Large scale precipitation [kg/m^2]
ta   %d  11,100,0  ** Temp. [K]
ua   %d  33,100,0 ** u wind [m/s]
uas  0  33,109,1  ** u wind [m/s]
va   %d  34,100,0 ** v wind [m/s]
vas  0  34,109,1  ** v wind [m/s]
endvars
"""%(grbfile,gmpfile,gtime,zlevcard,nl,nl,nl,nl)

    mf.WriteCtl(ctl,ctlpath)

    dogribmap=1
    if(not(os.path.exists(gmppath))):  dogribmap=1
        
    if(dogribmap):
        cmd="gribmap -v -i %s"%(ctlpath)
        mf.runcmd(cmd,ropt)




    


