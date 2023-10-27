#!/usr/bin/env python
from WxMAP2 import *
w2=W2()
from M import *
MF=MFutils()

def makeGsmapCtl(nt,year,version='',ropt='norun'):
    
    ctlpath="gsmap%s-%s.ctl"%(version,year)
    yearm1=int(year)-1
    ctl="""dset ^final/%%y4/%%y4%%m2%%d2/pr-gsmap-%%y4%%m2%%d2%%h2.grb
title gsmap version: %s pr
undef 9.999E+20
dtype grib
index ^gsmap%s-%s.gmp
options template
xdef 1440 linear   0.125 0.25
ydef  480 linear -59.875 0.25
zdef 1 levels 1013
tdef %d linear 00Z31Dec%d 1hr
vars 1
pr        0   59,  1,  0,  0 gsmap precip. (mm/hr) []
endvars"""%(version,version,year,nt,yearm1)

    rc=MF.WriteCtl(ctl,ctlpath)
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
            #1:['dtgopt',    'no default'],
            }

        self.defaults={
            'prcopt':'all',
            }

        self.options={
            'override':         ['O',0,1,'override'],
            'verb':             ['V',0,1,'verb=1 is verbose'],
            'ropt':             ['N','','norun',' norun is norun'],
            'yearOpt':          ['Y:',None,'a',"""yearOpt"""],
            'makeV6':           ['6',0,1,'make or ln -s V6 only'],
            'doGauge':          ['G',0,1,'only do gribmap'],

            }

        self.purpose='''
make yearly ctl for gsmap 1h grb'''

        self.examples="""
%s -Y cur"""


#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
# -- main
#
argv=sys.argv
CL=WgetCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr


if(yearOpt == None):
    print 'EEE must set -Y byyyy.eyyyy'
    sys.exit()
else:
    tt=yearOpt.split('.')
    if(len(tt) == 1):
        byear=eyear=int(yearOpt)
    elif(len(tt) == 2):
        byear=int(tt[0])
        eyear=int(tt[1])

years=range(byear,eyear+1)
version=''
tbdir='/braid1/mfiorino/w22/dat/pr/gsmap%s'%(version)
tbdirV6='/braid1/mfiorino/w22/dat/pr/gsmapV6'

# -- on mike?
#
tbdir    ="%s/pr/gsmap"%(w2.W2BaseDirDat)
tbdirV6  ="%s/pr/gsmapV6"%(w2.W2BaseDirDat)
tbdirV6G ="%s-Grev"%(tbdirV6)

if(makeV6): 
    if(doGauge):
        tbdir=tbdirV6G
        version='V6-Grev'
    else:
        tbdir=tbdirV6
        version='V6'

MF.ChangeDir(tbdir,verb=1)

MF.sTimer('YYY-CCC-all')
for year in years:
    nt=MF.nDayYear(year)*24
    # -- add 1 d and start in previous year
    nt=nt+24

    MF.sTimer('YYY-CCC-%d'%(year))
    rc=makeGsmapCtl(nt,year,version,ropt)
    MF.dTimer('YYY-CCC-%d'%(year))

MF.dTimer('YYY-CCC-all')
