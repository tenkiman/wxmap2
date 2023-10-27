#!/usr/bin/env python

from WxMAP2 import *
w2=W2()


#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
#
# command line setup
#

class w2CmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv
        
        self.argv=argv
        self.argopts={
            1:['dtgopt',    'DTG (YYYYMMDDHH)'],
            }
            
        self.options={
            'verb':['V',0,1,'verb=1 is verbose'],
            'ropt':['N','','norun',' norun is norun'],
            }

        self.defaults={
            }

        self.purpose='''
main control script for nwp2 models (gfs2,ecm2,ukm2,fim8,ngp2,cmc2,fimx)
using /public/data/grids/ and from wjet
(c) 2009-2012 Michael Fiorino,NOAA ESRL'''
        
        self.examples='''
%s ops6 gfs2 (sets incrontab=1)'''


        
#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# cmdline
#

argv=sys.argv

CL=w2CmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

dtgs=mf.dtg_dtgopt_prc(dtgopt)
cmd="""grep min /ptmp/log.load.py.%s.LOAD | tail -150 | grep -v "_05_??" | grep -v "_15_??" | grep -v _25_ | grep -v _35_  | grep -v _45_ | grep -v _55_ | grep %s"""%(w2.W2Host,dtgs[0][0:8])

mf.runcmd(cmd,ropt)



