#!/usr/bin/env python

from WxMAP2 import *
w2=W2()

from M2 import setModel2

def anlGmuOutput(output):

    status=-999
    if(len(output) == 0): return(status)
    if(mf.find(output,'receiving incremental file list')): status=1
    if(mf.find(output,'rsync: change_dir')): status=-1
    if(mf.find(output,'rsync error: ')): status=-2
    if(mf.find(output,'speedup is')): status=1
    
    if(status == -999):
        print 'unable to get status in output:'
        print output
        
    return(status)
    

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
rsync web and products from mike3|4|5 -> gmu
(c) 2009-2022 Michael Fiorino, AOES GMU'''

        self.examples='''
%s -X'''

CL=w2CmdLine(argv=sys.argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr


webDirs=['web-config','web']
#webDirs=['web-config']
sdir=w2.HfipProducts
#sdir='/data/w22'
tdir='mfiorino@hopper1.orc.gmu.edu:/scratch/mfiorino'
rsyncOpt='-aluv --delete'
rsyncOptL='-aLuv --delete'
if(reverse):
    rsyncOpt='-aluv'
    rsyncOptL='-aLuv'
else:
    rsyncOpt='-aluv --delete'
    rsyncOptL='-aLuv --delete'
    
if(ropt == 'norun'): 
    rsyncOpt=rsyncOpt.replace('aluv','aluvn')
    rsyncOptL=rsyncOptL.replace('aLuv','aLuvn')
    
if(doit): ropt=''
    
MF.sTimer('GMU-All-products')

for webdir in webDirs:
    
    MF.sTimer('GMU-web-%s'%(webdir))
    if(reverse):
        cmd="time rsync %s %s/%s/ %s/%s/ "%(rsyncOptL,tdir,webdir,sdir,webdir)
    else:
        cmd="time rsync %s %s/%s/ %s/%s/ "%(rsyncOptL,sdir,webdir,tdir,webdir)
    MF.runcmd(cmd,ropt)
    
    MF.dTimer('GMU-web-%s'%(webdir))
    
prodDirs=['tctrkveriDAT','jtdiagDAT','tcactDAT','tcdiagDAT','tcepsDAT','tcgenDAT']

sdir=w2.HfipProducts
tdir='mfiorino@hopper1.orc.gmu.edu:/scratch/mfiorino/hfip/fiorino/products/hfip'


for proddir in prodDirs:
    
    MF.sTimer('GMU-hfip-%s'%(webdir))
    if(reverse):
        cmd="time rsync %s %s/%s/ %s/%s/ "%(rsyncOpt,tdir,proddir,sdir,proddir)
    else:
        cmd="time rsync %s %s/%s/ %s/%s/ "%(rsyncOpt,sdir,proddir,tdir,proddir)
    MF.runcmd(cmd,ropt)

    MF.dTimer('GMU-hfip-%s'%(webdir))

        
MF.dTimer('GMU-All-products')
    
sys.exit()
