#!/usr/bin/env python

from M import *

import w2

MF=MFutils()

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
            2:['model',    'no default'],
            }

        self.defaults={
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

modelCenter={'avn':'ncep/avn',
             'ukm':'ncep/ukm',
             'ifs':'ecmwf/ifs',
             'ngp':'fnmoc/ngp',
             }

MF.sTimer(tag='wget.nersc')

argv=sys.argv
CL=WgetCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr
dtgs=mf.dtg_dtgopt_prc(dtgopt,ddtg=6)

al='ftp'
ap=""
af='hpss.nersc.gov'



sbdir='/home/f/fiorino/u9508/%s'%(modelCenter[model])
tbdir='/w21/dat/nwp/%s'%(modelCenter[model])


for dtg in dtgs:

    yyyymm=dtg[0:6]
    sdir="%s/%s"%(sbdir,yyyymm)
    tdir="%s/%s"%(tbdir,yyyymm)

    mf.ChkDir(tdir,diropt='mk')
    mf.ChangeDir(tdir)

    cmd="wget -nv -m -nd -T 180 -t 2  \"ftp://%s/%s/*%s*\""%(af,sdir,dtg)
    mf.runcmd(cmd,ropt)


MF.dTimer(tag='wget.nersc')

