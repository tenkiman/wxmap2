#!/usr/bin/env python

from WxMAP2 import *

sbdir='/braid1/mfiorino/w22/dat/nwp2/w2flds/dat/era5'
sbdir='/dat13/nwp2/w2flds/dat/era5'
sbdir='/dat9/dat/nwp2/w2flds/dat/era5'

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
    
    ctl="""dset  ^era5-w2flds-%s-sfc.grb
index ^era5-w2flds-%s-sfc.gmp
undef 9.999E+20
title era5-w2flds-2017083112-sfc.grb
*  produced by grib2ctl v0.9.12.5p16
dtype grib 255
options yrev
ydef 721 linear -90.0 0.25
xdef 1440 linear  0.0 0.25
tdef 41 linear %s 6hr
zdef 1 linear 1 1
vars 5
uas  0 165,1,0  ** 10 metre U wind component [m s**-1]
vas  0 166,1,0  ** 10 metre V wind component [m s**-1]
prc  0 143,1,0  ** Convective precipitation [m]
prl  0 142,1,0  ** Stratiform precipitation (Large-scale precipitation) [m]
psl  0 151,1,0  ** Mean sea level pressure [Pa]
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
    ctls=glob.glob("%s/*-sfc.ctl"%(sdir))
    if(len(ctls) == 1):
        sctl=ctls[0]
        print 'SSSSSSSSSSSSSS',sctl
        if(ropt == ''): rc=makeCorrCtl(dtg,sctl)
    else:
        print 'EEE-noctl for dtg: ',dtg,' press...'
        
   
sys.exit()
