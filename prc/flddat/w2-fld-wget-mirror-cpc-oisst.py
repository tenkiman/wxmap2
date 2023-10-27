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




#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
# main
#

prcdirW2=w2.PrcDirWxmap2W2
cmdRG="w2-ocean-oisst-gmu.py"

MF.sTimer(tag='wget.cpc.oisst')

argstr="pyfile cur"
argv=argstr.split()
#argv=sys.argv
CL=WgetCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

al='ftp'
ap="""-michael.fiorino@noaa.gov"""
af='ftp.emc.ncep.noaa.gov'
sbdir='/cmb/sst/oisst_v2/GRIB/'

prcdirW2=w2.PrcDirWxmap2W2
cmdRG="w2-ocean-oisst-gmu.py"

af='ftp.cpc.ncep.noaa.gov'
#ftp://ftp.cpc.ncep.noaa.gov/precip/PORT/sst/oisst_v2/GRIB/
sbdir='precip/PORT/sst/oisst_v2/GRIB'
tbdir="%s/ocean/oisst"%(w2.W2BaseDirDat)
tdir="%s/weekly/GRIB"%(tbdir)
MF.ChkDir(tdir,'mk')

mf.ChangeDir(tdir)

cmd="wget -nv -m -nd -T 180 -t 2  \"ftp://%s/%s/*\""%(af,sbdir)
mf.runcmd(cmd,ropt)

cmd="gribmap -v -i %s/oiv2.ctl"%(tbdir)
mf.runcmd(cmd,ropt)

# -- rsync to gmu.edu
#
# -- rsync to gmu.edu
#
if(w2.W2doRsyncPushGmu):
    MF.sTimer('R-GMU: %s'%(model))
    cmd="%s/%s -X"%(prcdirW2,cmdRG)
    mf.runcmd(cmd,ropt)
    MF.dTimer('R-GMU: %s'%(model))

MF.dTimer(tag='wget.cpc.oisst')
