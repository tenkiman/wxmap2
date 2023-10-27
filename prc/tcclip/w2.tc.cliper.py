#!/usr/bin/env python

from tcbase import *
import TCclip

#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# -- command line setup
#

class Adeck2CmdLine(CmdLine,AdeckSources):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv
        
        self.argv=argv
        self.argopts={
            1:['dtgopt',  '''dtgopt'''],
            }

        self.options={
            'verb':                ['V',0,1,'verb is verbose'],
            'ropt':                ['N','','norun',' norun is norun'],
            'override':            ['O',0,1,'override -- clean out target dir'],
            'dobt':                ['B',0,1,'run with best track'],
            'doMotion':            ['M',0,1,'use CARQ motion vice m12,m24 posits'],
            'stmopt':              ['S:',None,'a','run cliper for these sstorms...'],
            }

        self.defaults={
            }

        self.purpose='''
purpose --  run clipper model for dtgop dtgs
'''
        self.examples='''
%s cur12-12
'''


def errAD(option,opt=None):

    if(option == 'tstmids'):
        print 'EEE # of tstmids = 0 :: no stms to verify...stmopt: ',stmopt,' for errAD option: ',option
    else:
        print 'Stopping in errAD: ',option
    sys.exit()
        

#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
# main
#

CL=Adeck2CmdLine(argv=sys.argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

#
#  defaults
#
ropt=''
stmidset='all'
model='clp3'
if(doMotion): model='clpm'
if(dobt): 
    model='clpb'
    doMotion=0


dtgs=mf.dtg_dtgopt_prc(dtgopt)

tbdir=TcAdecksClipDir

if(stmopt != None):
    tD=TcData(stmopt=stmopt)
    dobyDTG=0
else:
    tD=TcData(dtgopt=dtgopt)
    dobyDTG=1
    
def writeAdecks(allAcards,model,override=0):
    stmids=allAcards.keys()
    tdir=None
    if(len(stmids) > 0):
        tdir="%s/%s/%s"%(tbdir,dtg[0:4],dtg)
        MF.ChkDir(tdir,'mk')

    if(override and tdir != None):
        cmd="rm %s/*%s*"%(tdir,model)
        mf.runcmd(cmd)
        
    for stmid in stmids:
        acards=allAcards[stmid]
        if(len(acards) == 0): 
            print 'no clipper for: ',stmid
            continue
        adpath="%s/tctrk.atcf.%s.%s.%s"%(tdir,dtg,model,stmid)
        print 'path: ',adpath
        MF.WriteList2Path(acards, adpath)

    
if(dobyDTG):
    
    MF.sTimer('clip-byDTG')
    for dtg in dtgs:
        allAcards=TCclip.MakeCliperForecast(tD,dtg,model,doMotion=doMotion,verb=verb)
        rc=writeAdecks(allAcards,model,override=override)
        
    MF.dTimer('clip-byDTG')
                
else:
    
    tstmids=tD.makeStmListMdeck(stmopt)
    for tstmid in tstmids:
        
        mD=tD.getDSsStm(tstmid)
        dtgs=mD.btdtgs

        for dtg in dtgs:
            
            tD=TcData(dtgopt=dtg)
            allAcards=TCclip.MakeCliperForecast(tD,dtg,model,doMotion=doMotion,
                                                tstmid=tstmid,
                                                verb=verb)
            rc=writeAdecks(allAcards,model,override=override)
   

sys.exit()

