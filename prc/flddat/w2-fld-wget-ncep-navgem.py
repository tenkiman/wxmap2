#!/usr/bin/env python

from WxMAP2 import *
w2=W2()

from M2 import setModel2

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
            'model':'navg',
            }

        self.options={
            'override':['O',0,1,'override'],
            'verb':['V',0,1,'verb=1 is verbose'],
            'ropt':['N','','norun',' norun is norun'],
            }

        self.purpose='''
purpose -- wget mirror navgem from ncep ftp 
%s cur
'''
        self.examples='''
%s cur
'''



def MakeCtl(dtg,ntaus,ropt='',verb=0):

    gtime=mf.dtg2gtime(dtg)
    ctlpath="navg.w2flds.%s.ctl"%(dtg)

    ctl="""dset ^navgem_%sf%%f3.grib2
index ^navgem_%s.gmp2
undef 9.999E+20
title navgem_2019062400f072.grib2
*  produced by g2ctl v0.0.4m                                                                                                                                                                                                                 
* griddef=1:421:(720 x 361):grid_template=0:winds(N/S): lat-lon grid:(720 x 361) units 1e-06 input WE:SN output WE:SN res 48 lat -90.000000 to 90.000000 by 0.500000 lon 0.000000 to 359.500000 by 0.500000 #points=259920:winds(N/S)
dtype grib2
ydef 361 linear -90.0 0.5
xdef 720 linear   0.0 0.5
tdef  %d linear %s 6hr
* PROFILE hPa                                                                                                                                                                                                                                
zdef 13 levels 100000 92500 85000 70000 50000 40000 30000 25000 20000 15000 10000 7000 5000
options pascals template
vars 11
prc         0,  1,0       0,1,10,1   ** surface Convective Precipitation [kg/m^2]
pr          0,  1,0       0,1, 8,1   ** surface Total Precipitation [kg/m^2]
zg         15,100         0,3, 5     ** (1000 925 850 700 500.. 250 200 150 100 70) Geopotential Height [gpm]
psl         0,101,0       0,3, 1     ** mean sea level Pressure Reduced to MSL [Pa]
hur        15,100         0,1, 1     ** (1000 950 900 850 800.. 500 450 400 350 300) Relative Humidity [%%]
ta         15,100         0, 0,0     ** (1000 925 850 700 500.. 250 200 150 100 70) Temperature [K]
tas         0,103,2       0, 0,0     ** 2 m above ground Temperature [K]
ua         15,100         0, 2,2     ** (1000 925 850 700 500.. 250 200 150 100 70) U-Component of Wind [m/s]
uas         0,103,10      0, 2,2     ** 10 m above ground U-Component of Wind [m/s]
va         15,100         0, 2,3     ** (1000 925 850 700 500.. 250 200 150 100 70) V-Component of Wind [m/s]
vas         0,103,10      0, 2,3     ** 10 m above ground V-Component of Wind [m/s]
ENDVARS
#zgwm        0, 6,0        0,3, 5     ** max wind Geopotential Height [gpm]
#pawm        0, 6,0        0,3,0      ** max wind Pressure [Pa]
#PREStrop   0,7,0   0,3,0 ** tropopause Pressure [Pa]
#vrta500     0,100,50000   0,2,10     ** 500 mb Absolute Vorticity [1/s]
#TMPmwl   0,6,0   0,0,0 ** max wind Temperature [K]
#TMPtrop   0,7,0   0,0,0 ** tropopause Temperature [K]
#UGRD20m   0,103,19.5   0,2,2 ** 19.5 m above ground U-Component of Wind [m/s]
#UGRDmwl   0,6,0   0,2,2 ** max wind U-Component of Wind [m/s]
#VGRD20m   0,103,19.5   0,2,3 ** 19.5 m above ground V-Component of Wind [m/s]
#VGRDmwl   0,6,0   0,2,3 ** max wind V-Component of Wind [m/s]
#VVELprs    15,100  0,2,8 ** (1000 925 850 700 500.. 300 250 200 150 100) Vertical Velocity (Pressure) [Pa/s]
#var0224320m   0,103,19.5   0,2,243 ** 19.5 m above ground desc [unit]
"""%(dtg,dtg,ntaus,gtime)
    
    
    MF.WriteString2File(ctl,ctlpath,verb=verb)

    cmd="gribmap -v -i %s"%(ctlpath)
    mf.runcmd(cmd,ropt)

    


#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
# main
#


MF.sTimer(tag='wget-navgem')

argstr="pyfile -y 2010 -S w.10 -P"
argv=argstr.split()
argv=sys.argv
CL=WgetCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

al='ftp'
ap="""-michael.fiorino@noaa.gov"""
af='ftpprd.ncep.noaa.gov'

#ftp://ftpprd.ncep.noaa.gov/pub/data/nccf/com/fnmoc/prod/navgem.20190624/
sbdir='/pub/data/nccf/com/fnmoc/prod'
tbdir="%s/%s"%(w2.Nwp2DataBdir,w2.Model2CenterModel(model))

dtgs=mf.dtg_dtgopt_prc(dtgopt,ddtg=6)

m2=setModel2(model)

for dtg in dtgs:

    yyyymmdd=dtg[0:8]

    sdir="%s/navgem.%s"%(sbdir,yyyymmdd)
    tdir="%s/%s"%(tbdir,dtg)
    tdir="%s/%s"%(m2.w2fldsSrcDir,dtg)
    
    mf.ChkDir(tdir,diropt='mk')
    mf.ChangeDir(tdir)

    cmd="wget -nv -m -nd -T 180 -t 2  \"ftp://%s/%s/*%s*\""%(af,sdir,dtg)
    mf.runcmd(cmd,ropt)

    # -- really need to do this check in w2.gfs.goes.py -- basic check is for existance of .ctl file
    #    which for data sets like these (constant update) is always there
    # -- but no harm

    fm=m2.DataPath(dtg,dtype='w2flds',dowgribinv=1,override=override)
    fd=fm.GetDataStatus(dtg)

    ntaus=None
    if(fd.dslastTau != None):
        ntaus=fd.dslastTau/fd.dtau + 1
        MakeCtl(dtg,ntaus)    
    else:
        print 'WWW---NNNOOO---data for dtg: ',dtg,' press...'

MF.dTimer(tag='wget-navgem')
