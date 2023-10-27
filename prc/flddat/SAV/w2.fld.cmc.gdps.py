#!/usr/bin/env python

from WxMAP2 import *
w2=W2()

from M2 import setModel2

def makeCtl(model,dtg,override=0,ropt=''):

    ctlpath="%s.w2flds.%s.ctl"%(model,dtg)

    gtime=mf.dtg2gtime(dtg)
    ntimes=41
    dogribmap=1

    ndxfile="%s.w2flds.%s.gmp2"%(model,dtg)
    print 'qqq ',MF.getPathSiz(ndxfile)
    if(MF.getPathSiz(ndxfile) > 0 and not(override)): dogribmap=0
    
    if(model == 'cgd6'): 
        ntimes=41
        grid="""ydef 301 linear  -90.0 0.6
xdef 600 linear -180.0 0.6"""

    ctl="""dset  ^%s.w2flds.%s.f%%f3.grb2
index ^%s
undef 9.999E+20
title cgd2.w2flds.2013062700.f006.grb2
*  produced by g2ctl v0.0.4m
* griddef=1:0:(600 x 301):grid_template=0:winds(N/S): lat-lon grid:(601 x 301) units 1e-06 input WE:SN output WE:SN res 48 lat -90.000000 to 90.000000 by 0.600000 lon 180.000000 to 180.000000 by 0.600000 #points=180901:winds(N/S)
dtype grib2
%s
tdef %s linear  %s 6hr
* PROFILE hPa
zdef 12 levels 100000 92500 85000 70000 50000 40000 30000 25000 20000 15000 10000 5000
options pascals template
vars 12
prc    0,1,0      0,1,10,1 ** surface Convective Precipitation [kg/m^2]
pr     0,1,0      0,1,8,1 ** surface Total Precipitation [kg/m^2]
uas    0,103,10   0,2,2 ** 10 m above ground U-Component of Wind [m/s]
vas    0,103,10   0,2,3 ** 10 m above ground V-Component of Wind [m/s]
psl    0,101      0,3,1 ** mean sea level Pressure Reduced to MSL [Pa]
hdpt  12,100      0,0,7 ** (1000 925 850 700 500.. 250 200 150 100 50) Dew Point Depression (or Deficit) [K]
zg    12,100      0,3,5 ** (1000 925 850 700 500.. 250 200 150 100 50) Geopotential Height [gpm]
hus   12,100      0,1,0 ** (1000 925 850 700 500.. 250 200 150 100 50) Specific Humidity [kg/kg]
hur   12,100      0,1,1 ** (1000 925 850 700 500.. 250 200 150 100 50) Specific Humidity [kg/kg]
ta    12,100      0,0,0 ** (1000 925 850 700 500.. 250 200 150 100 50) Temperature [K]
ua    12,100      0,2,2 ** (1000 925 850 700 500.. 250 200 150 100 50) U-Component of Wind [m/s]
va    12,100      0,2,3 ** (1000 925 850 700 500.. 250 200 150 100 50) V-Component of Wind [m/s]
ENDVARS"""%(model,dtg,ndxfile,grid,ntimes,gtime)

    rc=MF.WriteString2File(ctl,ctlpath,verb=1)
    
    if(dogribmap):
        cmd="gribmap -i %s"%(ctlpath)
        mf.runcmd(cmd,ropt)



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
            'resopt':     ['L',1,0,'low-res grid resolution -- cgd6 is model from archive'],
            'override':   ['O',0,1,'override'],
            'verb':       ['V',0,1,'verb=1 is verbose'],
            'ropt':       ['N','','norun',' norun is norun'],
            'tauopt':     ['t:',None,'a','set taus as tau1,tau2,...'],
            'dowget':     ['W',0,1,'do wget to get .tar from cmc'],
            'dols':       ['l',0,1,'do ls like l2.py'],
            
        }

        self.purpose='''
purpose -- dearchive & process cmc gdps global grids to w2flds'''
        self.examples='''
%s 2009050100
'''


#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
# main
#

MF.sTimer(tag='cmc.gdps')
CL=WgetCmdLine(argv=sys.argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

if(resopt):
    gridres='6'
    model='cgd6'
else:
    gridres='24'
    model='cgd2'
    
# -- M2 object
#
dmodelType='w2flds'
m=setModel2(model)

srcurl="ftp://ftp.cmc.ec.gc.ca/ftp/cmos/noaa/"                         # - for one-off files
srcurl="http://collaboration.cmc.ec.gc.ca/cmc/cmoi/noaa/"
sbdir='/w21/dat/nwp2/w2flds/dat/cgd6/cnfs/ops/dpssops/afssmit/noaa/final'
sbdir1='/w21/dat/nwp2/w2flds/dat/cgd6/final'
tbdir="%s/nwp2/w2flds/dat/%s"%(w2.W2BaseDirDat,model)

dtgs=mf.dtg_dtgopt_prc(dtgopt,ddtg=12)

for dtg in dtgs:

    fm=m.DataPath(dtg,dtype=dmodelType,dowgribinv=1,override=override,doDATage=1)
    fd=fm.GetDataStatus(dtg)
    fd.getEtau(dtg)
    
    endtau=fd.etau
    cmptau=fd.dslatestCompleteTauBackward 
    isdone=(endtau == cmptau and dtg[8:10] == '00')
    
    if(dols):
        print ' dtg:  ',dtg,' isdone:  ',isdone,' Maxtau: %5d'%(endtau),' Completed tau: %5d'%(cmptau)
        continue

    didwget=0
    tarball="%s.tar"%(dtg[0:8])
    
    if(not(isdone) and dowget or override):
        cmd="""wget -m -nd -T 180 -t 2 -l1 -P %s %s/%s"""%(tbdir,srcurl,tarball)
        mf.runcmd(cmd,ropt)
        MF.ChangeDir(tbdir)
        cmd="tar -xvf %s.tar"%(dtg[0:8])
        mf.runcmd(cmd,ropt)
        didwget=1
        
    spaths=glob.glob("%s/*%s*"%(sbdir,dtg))
    spaths=spaths+glob.glob("%s/*%s*"%(sbdir1,dtg))
  
    tdir="%s/%s"%(tbdir,dtg)
    MF.ChkDir(tdir,'mk')
    MF.ChangeDir(tdir)    

    if(len(spaths) > 0):
        # -- mv the files to the target dir with standard w2flds names
        #
        for spath in spaths:
            (ddir,dfile)=os.path.split(spath)
            tau=dfile.split('.')[0][-3:]
            ofile="%s.w2flds.%s.f%s.grb2"%(model,dtg,tau)
            cmd="mv %s %s/%s"%(spath,tdir,ofile)
            mf.runcmd(cmd,ropt)
    
    # -- do the grads .ctl
    #
    rc=makeCtl(model,dtg,override=override)
    
    # -- if we did the wget, do 12 z
    if(didwget):
        cmd="%s %s"%(CL.pypath,dtg[0:8]+'12')
        mf.runcmd(cmd,ropt)
        
        # -- kill tarball
        # 
        cmd="rm %s/%s"%(tbdir,tarball)
        mf.runcmd(cmd,ropt)


MF.dTimer(tag='cmc.gdps')
