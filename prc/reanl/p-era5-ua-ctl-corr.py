#!/usr/bin/env python

from WxMAP2 import *

sbdir='/w21/dat/nwp2/w2flds/dat/era5'

class MdeckCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv

        self.argv=argv

        self.argopts={
            1:['dtgopt', 'no default'],
            }        

        self.options={
            'verb':           ['V',0,1,'verb=1 is verbose'],
            'ropt':           ['N','','norun',' norun is norun'],
            }

        self.purpose='''
correct -ua.ctl files first found in 201806-201910'''
        
        self.examples='''
%s 2018060100'''

def makeCorrCtl(dtg,sctl,ropt='',verb=0):

    gtime=mf.dtg2gtime(dtg)
    
    ctl="""dset ^era5-w2flds-%s-ua.grb2
index ^era5-w2flds-%s-ua.gmp2
undef 9.999E+20
title t-era5-12-si.grb
*  produced by grib2ctl v0.9.12.5p16
dtype grib2
ydef 361 linear -90.0 0.5
xdef 720 linear   0.0 0.5
tdef  41 linear %s 6hr
* PROFILE hPa
zdef 10 levels 100000 92500 85000 70000 50000 40000 30000 25000 20000 5000
options pascals
vars 11
psl    0,101      0,3,0 ** mean sea level Pressure [Pa]
uas    0,103,10   0,2,2 ** 10 m above ground mponent of Wind [m/s]
vas    0,103,10   0,2,3 ** 10 m above ground V-Component of Wind [m/s]
prw    0,1      192,128,137 ** surface desc [unit]
prc    0,1        0,  1, 10   ** surface Convective Precipitation [kg/m^2]
pr     0,1        0,  1, 52,1 ** surface Total Precipitation [kg/m^2]
ua     9,100      0,2,2 ** mponent of Wind [m/s]
va     9,100      0,2,3 ** V-Component of Wind [m/s]
ta     9,100      0,0,0 ** Temperature [K]
hura   9,100      0,1,1 ** Relative Humidity [%%]
zg    10,100      0,3,4 ** Geopotential [m^2/s^2]
ENDVARS"""%(dtg,dtg,gtime)

    if(verb):
        print 'NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN'
        print ctl
        print 'NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN'
    
    MF.WriteCtl(ctl, sctl, verb=verb)
    
    # -- run gribmap
    #
    cmd="gribmap -i %s"%(sctl)
    mf.runcmd(cmd,ropt)
    

#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# -- main
#

MF.sTimer('all')

argv=sys.argv
CL=MdeckCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr


dtgs=mf.dtg_dtgopt_prc(dtgopt)


for dtg in dtgs:
    print '..........................working: ',dtg
    year=dtg[0:4]

    sdir="%s/%s/%s"%(sbdir,year,dtg)
    ctls=glob.glob("%s/*-ua.ctl"%(sdir))
    if(len(ctls) == 1):
        sctl=ctls[0]
        print 'SSSSSSSSSSSSSS',sctl
        rc=makeCorrCtl(dtg,sctl)
    else:
        print 'EEE-noctl for dtg: ',dtg
        sys.exit()
        
   
sys.exit()
