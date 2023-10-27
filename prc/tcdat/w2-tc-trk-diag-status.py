#!/usr/bin/env python

from WxMAP2 import *
w2=W2()

from tcCL import TcPrcMonitor

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
            'model':          ['m:','gfs2','a','model'],
            'dtgopt':         ['d:',None,'a','dtgopt'],
            'doprint':        ['p',1,0,'do NOT print stat card'],
            'dotrk':          ['T',0,1,'redo the tracker'],
            'dodiag':         ['D',0,1,'redo the tcdiag'],
            'verb':           ['V',0,1,'verb=1 is verbose'],
            'ropt':           ['N','','norun',' norun is norun'],
            'stmopt':         ['S:',None,'a','stmopt'],
            'useHfip':        ['H',0,1,'use hfip fs $W2_HFIP vice local'],
            'dobt':           ['b',0,1,'dobt list bt only'],
            'ls9x':           ['9',0,1,'ls9x'],
            'doCARQonly':     ['C',0,1,'control on summary plot'],
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
if(not(dobt)):  doBT=1  # default dobt=0 doBT=1  -- replace all 
if(doCARQonly): doBT=0  # ops     dobt=0 doBT=0  -- pure ops  : picks available from CARQ (adeck) first then bdeck (?)


trkprc="%s/tctrk/w2-tc-runTrks.py"%(os.getenv("W2_PRC_DIR"))
diagprc="%s/tcdiag/w2.tc.lsdiag-tau0.py"%(os.getenv("W2_PRC_DIR"))

# -- storms
#
if(stmopt != None or dtgopt != None):
    
    tPM=TcPrcMonitor(stmopt, model, dobt, doBT, ls9x, 
                     dtgopt=dtgopt,
                     useHfip=useHfip,
                     verb=verb,doprint=0)

    doTMdtgs=[]
    doDGdtgs=[]
    doTMstmids={}
    doDGstmids={}
    
    for stmid in tPM.stmids:
        if(stmopt == None  or (len(tPM.dtgsS[stmid]) > 1) and doprint): print
        for dtg in tPM.dtgsS[stmid]:
            stat=tPM.statusS[stmid,dtg]
            tt=stat.split()
            tttm=tt[5]
            ttdg=tt[6]
            ttgn=tt[7]
            tmtrkdone=tttm.split(':')[-1][1]
            tmgendone=tttm.split(':')[-1][-1]
            dgdone=int(ttdg.split(':')[-1])
            gndone=int(ttgn.split(':')[-1])
            
            print 'qqqqq',tttm,tmtrkdone,tmgendone,ttdg,dgdone,ttgn,gndone
            if(tmtrkdone == '0'): 
                doTMdtgs.append(dtg)
                MF.appendDictList(doTMstmids, dtg, stmid)
            if(dgdone == 0): 
                doDGdtgs.append(dtg)
                MF.appendDictList(doDGstmids, dtg, stmid)
            
            if(doprint): print stat
            
    #if(doprint): print; print
     
    if(dotrk):     
        doTMdtgs=mf.uniq(doTMdtgs)
        for dtg in doTMdtgs:
            cmd="%s %s %s -t -O -M"%(trkprc,dtg,model)
            mf.runcmd(cmd,ropt,postfix=str(doTMstmids[dtg]))
            
    if(dodiag):
        MF.sTimer('run-tcdiag-AAAAAAAAAALLLLLLLLLLLLLL')
        doDGdtgs=mf.uniq(doDGdtgs)
        for dtg in doDGdtgs:
            MF.sTimer('run-tcdiag-%s'%(dtg))
            cmd="%s %s %s -K"%(diagprc,dtg,model)
            mf.runcmd(cmd,ropt,postfix=str(doDGstmids[dtg]))
            MF.dTimer('run-tcdiag-%s'%(dtg))
        MF.sTimer('run-tcdiag-AAAAAAAAAALLLLLLLLLLLLLL')
            
    



    
if(verb): MF.dTimer('all')



        
