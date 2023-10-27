#!/usr/bin/env python

from M import *

from M2 import setModel2

from tcCL import TcPrcMonitor

from diagcard import *

MF=MFutils()

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
            'dobt':           ['b',0,1,'dobt list bt only'],
            'dols':           ['l',0,1,'do ls of TCs...'],
            'ls9x':           ['9',0,1,'ls9x'],
            'notdoCARQonly':     ['C',0,1,'control on summary plot'],
            'tofile':           ['f',0,1,'print to file']
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
if(notdoCARQonly): doBT=1 #Changed the default to doBT=1, and do -C option to   
# ops     dobt=0 doBT=0  -- pure ops  : picks available from CARQ (adeck) first then bdeck (?)
# -- storms
#
print 'doBT', doBT
model='gfs2'
model='ecmt'

label=Labels()


#(dtgs,modelsDiag)=getDtgsModels(CL,dtgopt,modelopt)
MF.sTimer('TcData')
MF.dTimer('TcData')
MF.ChangeDir(prcdir)

keys=[]

ptcmean=[]
for i in range(9):
    ptcmean.append(0)
count=0


if(stmopt != None):
#    print 'aslkdfj;aklsjdf;akljdf'
#   print stmopt, model, dobt, doBT, ls9x

    tPM=TcPrcMonitor(stmopt, model, dobt, doBT, ls9x)
    stmids=tPM.stmids
    tPM.ls()
    print stmids

    for stmid in stmids:
        print 'NEXT ROUND', stmid
        dtgs=tPM.dtgsS[stmid]
        cardDic={}
        for dtg in dtgs:
            cardDic[dtg]=tPM.statusS[stmid,dtg]
        storm=stmlife(model,stmid,dtgs,cardDic)
        tD=TcData(stmdtg=dtgs[-1])

        storm.printCards(tbdir,prcdir,tD,verb=verb)

        storm.ptcMean()
        if (tofile):
            path='/home/amb/michael.natoli/lsdiag/data/'+stmid+'.dat'
            storm.toFile(path)

        print 'FINISHED', stmid
sys.exit()
            
if(verb): MF.dTimer('all')
