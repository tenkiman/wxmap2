#!/usr/bin/env python

from WxMAP2 import *
w2=W2()
from m2 import EnsModel

import FM

#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
#
# command line setup
#

class MFCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv
        
        self.argv=argv
        self.argopts={
            1:['dtgopt',            """set the basedtg to mssTar and rm -r all earlier data sets"""],
            2:['modelopt',          """models: MMM1 | MMM1,MMM2,...,MMMn | 'all'"""],
            }

        self.options={
            'verb':                    ['V',0,1,'verb=1 is verbose'],
            'ropt':                    ['N','','norun',' norun is norun'],
            'override':                ['O',0,1,'override'],
            'overrideGM':              ['G',0,1,'overrideGM -- override gribmap making'],
            'dtauopt':                 ['d:','12.12','a',"""dtau.ddtg """],
            'dolsctl':                 ['L',0,1,"""only list the .ctl"""],
            'doarchive':               ['a',0,1,"""use archive dir"""],
            'postfix':                 ['p:',None,'a',"""-postfix added to output files"""],
            }


        self.rt=FM.rtfimRuns()

        self.defaults={
            'verbcd':-1,
            }
        
        self.purpose="""
make ensemble FC objects for using grads ensemble dimension

rtfim runs:
%s"""%(self.rt.getRunlist())
        
        self.examples='''
%s cur12-d30.cur12-12 gfs2 -d 12.12'''


    def chkFimRun(self,model):

        rtmodels=self.rt.runs.keys()

        if(not(model in rtmodels)):
            print 'EEE model: ',model,' not in FM.rtfimRuns.runs...sayoonara'
            sys.exit()

        return(1)


#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
# main
#
argv=sys.argv
CL=MFCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

overrideLN=0
if(override):
    overrideLN=overrideGM=1
    
dtgs=mf.dtg_dtgopt_prc(dtgopt)
models=modelopt.split(',')

(dtau,ddtg)=dtauopt.split('.')

for model in models:

    MF.sTimer('EnsModel: %s'%(model))
    mFc=EnsModel(model,dtgs,dtau=dtau,ddtg=ddtg,
                 overrideLN=overrideLN,overrideGM=overrideGM,
                 postfix=postfix,
                 justinit=dolsctl,
                 do12hr=0,
                 verb=verb)
    if(dolsctl):
        print mFc.ensFcCtlpath
        cmd="cat %s"%(mFc.ensFcCtlpath)
        mf.runcmd(cmd,ropt)
    MF.dTimer('EnsModel: %s'%(model))
    

