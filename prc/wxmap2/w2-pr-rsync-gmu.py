#!/usr/bin/env python

from WxMAP2 import *
w2=W2()

from M2 import setModel2

#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# command line setup
#
class w2CmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv
        
        self.argv=argv
        self.argopts={
        }

        self.options={
            'verb':         ['V',0,1,'verb=1 is verbose'],
            'ropt':         ['N','','norun',' norun is norun'],
            'doit':         ['X',0,1,'execute'],
            'reverse':      ['R',0,1,' reverse direction'],
            }


        self.purpose='''
rsync from tenki7 to argo.orc.gmu.edu
(c) 2009-2021 Michael Fiorino,wxmap2.com'''

        self.examples='''
%s -X # doit '''

CL=w2CmdLine(argv=sys.argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

rsyncOpt='-aluv --timeout=120 --include="*%s*" '%(curyear)
rsyncOpt='-aluv --timeout=120'
if(ropt == 'norun'): rsyncOpt=rsyncOpt.replace('aluv','aluvn')

sdir='/w21/dat/pr'
tdir='%s:/scratch/mfiorino/dat/pr'%(w2.HopperGmUrl)

if(reverse):
    MF.sTimer('GMU pr pull')
    cmd="time rsync %s %s/ %s/"%(rsyncOpt,tdir,sdir)
    mf.runcmd(cmd,ropt)
    MF.dTimer('GMU pr pull')
    
else:
    
    cmd="time rsync %s %s/ %s/"%(rsyncOpt,sdir,tdir)
    mf.runcmd(cmd,ropt)

