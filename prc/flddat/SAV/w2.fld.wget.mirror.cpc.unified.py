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

def makeCtl(tbdir,ntime,gtime):
    
    ctlpath="%s/pr.cpc.unified.ctl"%(tbdir)
    
    ctl="""dset ^%%y4/PRCP_CU_GAUGE_V1.0CONUS_0.25deg.lnx.%%y4%%m2%%d2.RT
options  little_endian template
title  Daily Precipitation Analysis over CONUS  
undef -999.0
#xdef 300 linear  230.125 0.250
xdef 300 linear -129.875 0.250
ydef 120  linear  20.125  0.250
zdef 1 linear 1 1
tdef %d linear %s 1dy
vars 2
rain     1  00 the grid analysis (0.1mm/day)
nstn     1  00 the number gauges 
endvars"""%(ntime,gtime)
    
    MF.WriteString2Path(ctl,ctlpath)



#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
# main
#

#ftp://ftp.cpc.ncep.noaa.gov/precip/CPC_UNI_PRCP/GAUGE_CONUS/RT/2013/
#ftp://ftp.cpc.ncep.noaa.gov/precip/CPC_UNI_PRCP/GAUGE_CONUS/RT/2013/PRCP_CU_GAUGE_V1.0CONUS_0.25deg.lnx.20130906.RT
MF.sTimer(tag='wget.cpc.pr.unified')

CL=WgetCmdLine(argv=sys.argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

al='ftp'
ap="""-michael.fiorino@noaa.gov"""
af='ftp.cpc.ncep.noaa.gov'
tbdir="%s/pr/cpc_unified"%(w2.W2BaseDirDat)

dtgs=mf.dtg_dtgopt_prc(dtgopt)

for dtg in dtgs:
    year=dtg[0:4]

    sbdir='precip/CPC_UNI_PRCP/GAUGE_CONUS/RT/%s'%(year)
    tdir="%s/%s"%(tbdir,year)
    MF.ChkDir(tdir,'mk')
    mf.ChangeDir(tdir)

    cmd="wget -nv -m -nd -T 180 -t 2  \"ftp://%s/%s/*%s*\""%(af,sbdir,dtg[0:8])
    mf.runcmd(cmd,ropt)
    

uniprs=glob.glob("%s/????/*.RT"%(tbdir))

uniprs.sort()

bdtg=uniprs[0].split('.')[-2] + '00'
edtg=uniprs[-1].split('.')[-2] + '00'

dtgs=mf.dtgrange(bdtg,edtg,24)
ntimes=len(dtgs)

gtime=mf.dtg2gtime(bdtg)
gtime=gtime[3:]

print 'gggg ',gtime

makeCtl(tbdir,ntimes,gtime)

MF.dTimer(tag='wget.cpc.pr.unified')