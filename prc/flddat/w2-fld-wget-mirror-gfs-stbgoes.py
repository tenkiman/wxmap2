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
            'model':'gfs2',
            }

        self.options={
            'override':['O',0,1,'override'],
            'verb':['V',0,1,'verb=1 is verbose'],
            'ropt':['N','','norun',' norun is norun'],
            }

        self.purpose='''
purpose -- wget mirror gfs stb (sat brightness t) goes images
%s cur
'''
        self.examples='''
%s cur
'''



def MakeCtl(dtg,ntaus,ropt='',verb=0,doLn=1):

    hh=int(dtg[8:])

    gtime=mf.dtg2gtime(dtg)

    ctlpath="gfs.t%02dz.goessimpgrb2.1p00.grib2.ctl"%(hh)
    gmppath="gfs.t%02dz.goessimpgrb2.1p00.grib2.gmp"%(hh)
    ctlpath="gfs.t%02dz.goessimpgrb2.0p25.grib2.ctl"%(hh)
    gmppath="gfs.t%02dz.goessimpgrb2.0p25.grib2.gmp"%(hh)
    if(doLn):
        dset="dset ^gfs.t%02dz.goessimpgrb2.f%%f3.1p00.grib2"%(hh)
    else:
        dset="dset ^gfs.t%02dz.goessimpgrb2.1p00.f%%f3"%(hh)
        dset="dset ^gfs.t%02dz.goessimpgrb2.0p25.f%%f3"%(hh)
    
    ctl="""%s
title gfs 1deg goes images
undef 1e20
options template
*  produced by g2ctl v0.0.4m
* griddef=1:0:(360 x 181):grid_template=0: lat-lon grid:(360 x 181) units 1e-06 input WE:NS output WE:SN res 48 lat 90.000000 to -90.000000 by 1.000000 lon 0.000000 to 359.000000 by 1.000000 #points=65160:winds(N/S)
index ^%s
dtype grib2
ydef  721 linear  -90.0 0.25
xdef 1440 linear    0.0 0.25
tdef %d linear %s 3hr
zdef 1 linear 1 1
vars 4
sbtch2   0,  8,0       3,192,53 ** top of atmosphere desc [unit]
sbtch3   0,  8,0       3,192,54 ** top of atmosphere desc [unit]
sbtch4   0,  8,0       3,192,55 ** top of atmosphere desc [unit]
sbtch5   0,  8,0       3,192,58 ** top of atmosphere desc [unit]
endvars
# -- before gfs 16 2021032212
#sbtch2   0,  8,0       3,192,0 ** top of atmosphere Simulated Brightness Temperature for GOES 12, Channel 2 [K]
#sbtch3   0,  8,0       3,192,1 ** top of atmosphere Simulated Brightness Temperature for GOES 12, Channel 3 [K]
#sbtch4   0,  8,0       3,192,2 ** top of atmosphere Simulated Brightness Temperature for GOES 12, Channel 4 [K]
#sbtch5   0,  8,0       3,192,3 ** top of atmosphere Simulated Brightness Temperature for GOES 12, Channel 5 [K]
"""%(dset,gmppath,ntaus,gtime)

    MF.WriteString2File(ctl,ctlpath,verb=verb)

    cmd="gribmap -v -i %s"%(ctlpath)
    mf.runcmd(cmd,ropt)

    

    


#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
# main
#


MF.sTimer(tag='wget.gfs.stb')

argstr="pyfile -y 2010 -S w.10 -P"
argv=argstr.split()
argv=sys.argv
CL=WgetCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

prcdirW2=w2.PrcDirWxmap2W2
cmdRG="w2-w2flds-rsync-gmu.py"

al='ftp'
ap="""-michael.fiorino@noaa.gov"""
af='ftpprd.ncep.noaa.gov'

sbdir='/pub/data/nccf/com/gfs/prod'
tbdir="%s/%s"%(w2.Nwp2DataBdir,w2.Model2CenterModel(model))

dtgs=mf.dtg_dtgopt_prc(dtgopt,ddtg=6)

model='goes'
m=setModel2(model)
m.doLn=0

minTauGoes=120

for dtg in dtgs:

    yyyymmdd=dtg[0:8]
    hh=dtg[8:10]
    sdir="%s/gfs.%s/%s/atmos"%(sbdir,yyyymmdd,hh)
    tdir="%s/%s"%(tbdir,dtg)

    mf.ChkDir(tdir,diropt='mk')
    mf.ChangeDir(tdir)

    cmd="wget -nv -m -nd -T 180 -t 2  \"ftp://%s/%s/*goes*1p00.f???\""%(af,sdir)
    cmd="wget -nv -m -nd -T 180 -t 2  \"ftp://%s/%s/*goes*0p25.f???\""%(af,sdir)
    mf.runcmd(cmd,ropt)

    files=glob.glob("*goes*1p00.f???")
    files=glob.glob("*goes*0p25.f???")

    ntaus=len(files)
    print 'nnnnnnnnnnnnnnnnnnnnnnnnnnnnn ',ntaus
    for ifile in files:
        (base,ext)=os.path.splitext(ifile)
        
        #gfs.t00z.goessimpgrb2f00.1p0deg
        #01234567890123456789012345678901
        #gfs.t18z.goessimpgrb2.1p00.f180
        tau=int(ext[-3:])
        ofile=base[0:21]+".f%03d.1p00.grib2"%(tau)
        ofile=base[0:21]+".f%03d.0p25.grib2"%(tau)
        if(verb): print ifile,ofile
        if(not(os.path.exists(ofile)) and m.doLn):
            cmd="ln -s -f %s %s"%(ifile,ofile)
            mf.runcmd(cmd,ropt)


    # -- really need to do this check in w2.gfs.goes.py -- basic check is for existance of .ctl file
    #    which for data sets like these (constant update) is always there
    # -- but no harm
    fm=m.DataPath(dtg,dowgribinv=1,override=override)
    fd=fm.GetDataStatus(dtg)

    print 'III minTauGoes in fd.dsitaus: ',minTauGoes,fd.dsitaus,dtg,dtgs[-1],mf.dtgdiff(dtg,curdtg)
    if((minTauGoes in fd.dsitaus) and (dtg == dtgs[-1] or mf.dtgdiff(dtg,curdtg) > 0)):
        print 'CCCCCCCCCCCCCC making goes .ctl for: ',dtg
        MakeCtl(dtg,ntaus,doLn=m.doLn)    

    # -- rsync to gmu.edu
    #
    if(w2.W2doRsyncPushGmu):
    
        MF.sTimer('R-GMU: %s at: %s'%(model,dtg))
        cmd="%s/%s %s %s"%(prcdirW2,cmdRG,dtg,model)
        mf.runcmd(cmd,ropt)
        MF.dTimer('R-GMU: %s at: %s'%(model,dtg))


MF.dTimer(tag='wget.gfs.stb')

