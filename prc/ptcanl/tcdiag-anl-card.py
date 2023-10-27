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
print 'doBT', doBT
model='gfs2'

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

#    storm=stmlife(stmopt,model)
    tPM=TcPrcMonitor(stmopt, model, dobt, doBT, ls9x)
    stmids=tPM.stmids

    for stmid in stmids:
        dtgs=tPM.dtgsS[stmid]
        for dtg in dtgs:
            #find if the tcdiag was ran at this dtg
            card=tPM.statusS[stmid,dtg]
            tt=card.split()
#            print 'tt',tt
#            print 'length',len(keys)
            if len(keys)==0:
                keys.append(tt[1])
            elif tt[1]!=keys[0]:
                keys.append(tt[1])

                break
#        print keys, 'KEYS**********************************'
        print '\n',label.getLabel()                
        for dtg in dtgs:
            card=tPM.statusS[stmid,dtg]
#            print card
            tt=card.split()
            diag=tt[6].split(':')
            flag=diag[1]

            istmid=tt[1]

            # Parse tcdiag files
            dobail=0
            tD=TcData(stmdtg=dtgs[-1])
            tGa=TcDiagAnl(dtg,model,dols=dols,tbdir=tbdir,dobt=dobt,dobail=dobail,tD=tD,verb=verb)
            tGa.prcdir=prcdir

            # Get card
            id1=keys[0]
            if len(keys)>1:
                id2=keys[1]
            else:
                id2=None
#            print id1,id2
            tG9=TCdiag9X0X(dtg,model,id1,id2,tGa,stmopt,verb,flag)
            print tG9.getCard()

# calculate the mean of the variables while it is a PTC
            card1=tG9.getCard()
            tt=card1.split()
            sid=tt[0]
            sid=getStmParams(sid,convert9x=1)[-1]
            if int(sid[:2])>=90:
#                print sid
                for i in range(9):
                    ptcmean[i]=ptcmean[i]+int(tt[i+2])
                count=count+1

for i in range(9):
    ptcmean[i]=ptcmean[i]/count

print "\nMean Fields: "
print "SYSTEM ID   STARTTIME   DEVELOP/DEATH", label.getLabel()

sys.exit()
            
            
if(verb): MF.dTimer('all')


        
