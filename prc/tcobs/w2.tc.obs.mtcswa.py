#!/usr/bin/env python

from TC import *

MF=MFutils()
        
#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# command line setup
#

class TcObsCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv
        
        self.argv=argv
        self.argopts={
            1:['dtgopt', 'run dtgs'],
            }

        self.defaults={
            'doupdate':0,
            }

        self.options={
            'override':['O',0,1,'override'],
            'verb':['V',0,1,'verb=1 is verbose'],
            'ropt':['N','','norun',' norun is norun'],
            'stmopt':['S:',None,'a','stmopt'],
            }

        self.purpose='''
purpose -- superob the CIRA MTCSWA (multi-platiform TC sfc wind analysis) AMSu and IRWD wind retrievals
for use in EnKF
'''
        self.examples='''
example:
%s 20090900100 -S 13e.9 # process Jimena'''


class Mtcswa(MFbase):

    sbdir=TcObsMtcswaSourceDir
    tbdir=TcObsSatWindsDir

    def lsObs(self,dtg,stm3id):

        year=dtg[0:4]
        sdir="%s/%s/%s"%(self.sbdir,year,stm3id)
        obfiles=glob.glob("%s/*%s*obs"%(sdir,dtg))
        for obfile in obfiles:
            print 'MTCSWA .obs file for dtg: ',dtg,' is: ',obfile
            
        self.obfiles=obfiles
        
#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# main 
argstr="pyfile cur-18 "
argv=argstr.split()
argv=sys.argv
CL=TcObsCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

dtgs=mf.dtg_dtgopt_prc(dtgopt)

mT=Mtcswa()

for dtg in dtgs:

    if(stmopt != None):
        stmids=MakeStmList(stmopt,verb=0)
    else:
        tcD=TcData()
        stmids=tcD.getStmidDtg(dtg)

    for stmid in stmids:
        stm3id=stmid.split('.')[0].lower()
        mT.lsObs(dtg,stm3id)

    
        
