#!/usr/bin/env python

from TCdiag import *  # imports tcbase

class Ecm5CmdLine(CmdLine):

    def __init__(self,argv=sys.argv):


        if(argv == None): argv=sys.argv
        
        self.argv=argv
        self.argopts={
            1:['dtgopt',  '''pull ecm5 from wxmap2 '''],
            }

        self.defaults={
            }
            
        self.options={
            'override':            ['O',0,1,"""override"""],
            'verb':                ['V',0,1,'verb is verbose'],
            'ropt':                ['N','norun','norun','must use -X to run'],
            'doIt':                ['X',0,1,'run it norun is norun'],
            'doTCs':               ['t',1,0,'do NOT do the TC tracker'],
            'modOpt':              ['m:',None,'a','model opt'],
            }

        self.purpose='''
rsync ecm5 from wxmap2.com to tenki7'''
        
        self.examples='''
%s -N'''

#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
# main
#

CL=Ecm5CmdLine(argv=sys.argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr


if(doIt): ropt=''

models=['ecm5']
if(modOpt != None):
    models=modOpt.split(',')

dtgs=mf.dtg_dtgopt_prc(dtgopt)

prcdirW2=os.getenv('W2_PRC_DIR')
prcdir="%s/tcdiag"%(prcdirW2)

overOpt=''
if(override): overOpt='-O'

for dtg in dtgs:

    MF.sTimer('lsdiag-ALL-%s'%(dtg))
    if(mf.find(modOpt,'all') and MF.is0012Z(dtg)): models=tcdiagModels
    if(mf.find(modOpt,'all') and MF.is0618Z(dtg)): models=tcdiagModels0618
    
    for model in models:
        cmd="%s/w2-tc-lsdiag.py %s %s %s"%(prcdir,dtg,model,overOpt)
        mf.runcmd(cmd,ropt)
        
    MF.dTimer('lsdiag-ALL-%s'%(dtg))
