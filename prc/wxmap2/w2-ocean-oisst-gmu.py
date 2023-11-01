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
            'reverse':      ['R',0,1,'reverse direction'],
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

rsyncOpt='-aluv --timeout=120'
if(ropt == 'norun'): rsyncOpt='-aluvn'

sdir='/w21/dat/ocean'
tdir='mfiorino@argo.orc.gmu.edu:/scratch/mfiorino/dat/ocean/oisst'
tdir='mfiorino@hopper1.orc.gmu.edu:/scratch/mfiorino/dat/ocean'

if(reverse):
    MF.sTimer('GMU oisst pull')
    cmd="time rsync %s %s/ %s/"%(rsyncOpt,tdir,sdir)
    mf.runcmd(cmd,ropt)
    MF.dTimer('GMU oisst pull')
    
else:
    
    cmd="time rsync %s %s/ %s/"%(rsyncOpt,sdir,tdir)
    mf.runcmd(cmd,ropt)
