#!/usr/bin/env python

from ptcCL import *
from M2 import setModel2

#MF=MFutils()

tbdir=w2.TcTcanalDatDir
prcdir='/w21/src-SAV/tcdiag'
prcdir='/w21/src/tcdiag'
prcdir=w2.PrcDirTcdiagW2
prcdirIships="%s/tclgem"%(w2.SrcBdirW2)

class MdeckCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv

        self.argv=argv

        self.argopts={
            #1:['dtgopt',    'no default'],
            }

        self.defaults={
            'lsopt':'s',
            'doupdate':0,
            'tcvPath':None,
            }

        self.options={
            'dtgopt':         ['d:',None,'a','year'],
            'verb':           ['V',0,1,'verb=1 is verbose'],
            'ropt':           ['N','','norun',' norun is norun'],
            'stmopt':         ['S:',None,'a','stmopt'],
            'model':          ['m:','ecmt','a','which model analysis to use for tcdiag vars'],
            'dobt':           ['b',0,1,'dobt list bt only'],
            'dols':           ['l',0,1,'do ls of TCs...'],
            'ls9x':           ['9',0,1,'ls9x'],
            'notdoCARQonly':   ['C',0,1,'control on summary plot'],
            'tofile':         ['f',1,0,'do NOT write to file']
            }

        self.purpose='''
check status of tmtrkN/mftrkN/TCdiag/TCgen'''
        
        self.examples='''
%s -S 09w.15
%s '''

    
#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# -- main
#
MF.sTimer('all')

argv=sys.argv
CL=MdeckCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

# -- control output of storm listing by dtg
#
doBT=0
#if(not(dobt)):  doBT=1  # default dobt=0 doBT=1  -- replace all 
if(notdoCARQonly): doBT=1 #Changed the default to doBT=1, and do -C option to   
# ops     dobt=0 doBT=0  -- pure ops  : picks available from CARQ (adeck) first then bdeck (?)
# -- storms
#

label=Labels()

if(stmopt != None):

    MF.sTimer('tcMonitor')
    tD=TcData(stmopt=stmopt)
    tPM=TcPrcMonitor(stmopt, model, dobt, doBT, ls9x,tcD=tD)
    stmids=tPM.stmids
    MF.dTimer('tcMonitor')

    for stmid in stmids:
        print 'NEXT STORM', stmid, 'DEVELOPED?: ',tPM.pTCdev[stmid.upper()] #pTCdev says if the ptc developed into a tc

        dtgs=tPM.dtgsS[stmid]

        status={}
        for dtg in dtgs:
            status[dtg]=tPM.statusS[stmid,dtg]

        storm=stmlife(model,stmid,dtgs,tD,status,tPM.pathsS,tPM.pTCdev[stmid.upper()],verb=verb)

        storm.printCards()
        storm.printPtcMean()

        if (tofile):
            year=stmid[4:]
            tdir='/data/hfip/fiorino/w21/dat/tc/ptcanl/%s'%(year)
            MF.ChkDir(tdir,'mk')
            path="%s/%s.%s.txt"%(tdir,stmid,model)
            storm.toFile(path)

        print 'FINISHED', stmid
        
            
MF.dTimer('all')
