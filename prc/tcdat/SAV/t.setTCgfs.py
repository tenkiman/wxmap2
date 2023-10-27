#!/usr/bin/env python

from M import MFutils
MFb=MFutils()
MFb.sTimer('all-outer')

MFb.sTimer('w2')
from tcbase import TcData
MFb.dTimer('w2')

MF.sTimer('tc')
tD=TcData()
MF.dTimer('tc')

        

#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
#
# command line setup
#

class AdeckCmdLine(CmdLine,AdeckSources):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv
        
        self.argv=argv
        self.argopts={
            1:['source',           '''source1[,source2,...,sourceN]'''],
            2:['basedtg',          '''base dtg for AT'''],
            }

        self.defaults={
            'dorsync2kaze':0,
            }

        self.options={
            'dtx':            ['d:',6,'i','dt in time interp'],
            'ATtauRange':     ['a:','-24.0','a','''btau.etau to set how far back in dtg for AT'''],
            'BTtauRange':     ['b:','-48.0','a','''btau.etau to set how far back in dtg for BT'''],
            'ATOtauRange':    ['o:','0.72','a','''btau.etau for outputing AT taus'''],
            'override':       ['O',0,1,'override'],
            'verb':           ['V',0,1,'verb=1 is verbose'],
            'ropt':           ['N','','norun',' norun is norun'],
            'doadecks':       ['A',1,0,'0 - no NOT make adecks'],
            'doacardout':     ['D',0,1,'1 - output acards'],
            'doputdss':       ['P',1,0,'0 - do NOT putDSs'],
            'dols':           ['l',0,1,'1 - list'],
            'dolslong':       ['L',0,1,'1 - long list'],
            'dolsfull':       ['F',0,1,'1 - full list'],
            'stmopt':         ['S:',None,'a','stmopt'],
            'aidopt':         ['T:',None,'a','taid'],
            'update':         ['u',0,1,'only update adeck'],
            'doclean':        ['K',0,1,"""blow away .pypdb file because shelf created with 'c' option """],
            'dofilt9x':       ['9',0,1,"""don't process 9X storms"""],
            'phr':            ['h:',None,'i',"""phr -- do 'I' (6) and '2'(12) trackers"""],
            'dojettrack':     ['J',0,1,"""use trackers run on jet vice genesis tracker"""],
            'doVdeck':        ['v',0,1,"""run vdeck after doing adeck"""],
            'md2tag':         ['t:',None,'a','tag for opening mdecks2'],
            }

        self.purpose='''
parse and create adeck card data shelves
sources: %s'''%(self.sourcesAll)
        self.examples='''
%s -u -y cur'''

    def ChkSource(self,year=None):

        if(year != None):
            self.getSourcesbyYear(year)
            
        iok=0
        for s in self.sources:
            if(self.source == s): iok=1 ; break

        return(iok)

#eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
# errors

def errAD(option,opt=None):
    
    if(option == 'tstmids'):
        print 'EEE # of tstmids = 0 :: no stms to verify...stmopt: ',stmopt,' in: ',CL.pyfile
    elif(option == 'taids'):
        print 'EEE # of taids = None :: no aids to pull: ',aidopt,' in: ',CL.pyfile
    else:
        print 'Stopping in errAD: ',option
    sys.exit()


#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# main

MF.sTimer('all-inner')

CL=AdeckCmdLine(argv=sys.argv)
CL.CmdLine()
exec(CL.estr)
if(verb): CL.ls()

sources=source.split(',')

if(stmopt != None): tstmids=MakeStmList(stmopt,verb=0)
else: tstmids=None

if(tstmids == None): pass
elif(len(tstmids) == 0): errAD('tstmids')

if(aidopt != None):  taids=aidopt.split(',')
else:                taids=None ;     errAD('vdeckitaids')

tdtg=mf.dtg_command_prc(basedtg)


tBG=TcFtBtGsf(source,tstmids,tdtg,taids,
            tD=tD,
            dtx=dtx,
            ATtauRange=ATtauRange,BTtauRange=BTtauRange,ATOtauRange=ATOtauRange,
            verb=verb)
tBG.getABs()

if(verb):
    setgsf =tBG.makeSetTcGsf() ; print setgsf
    btgsf  =tBG.makeTcFtBtGsf('bt') ; print btgsf
    ftgsf  =tBG.makeTcFtBtGsf('ft') ; print ftgsf
    dbtgsf =tBG.makeDrawBtGsf() ; print dbtgsf
    dftgsf =tBG.makeDrawFtGsf() ; print dftgsf

#gfs=makeTcBtGsf(ABs,tstmids,taids)
#
#(ABs,tstmids)=getATsBTs(tD,source,tdtg,atdtgs,btdtgs,oattaus,taids,tstmids,dtx=dtx,verb=verb)

for tstmid in tBG.tstmids:
    for taid in taids:
        (satrk,satimes,sbtrk,sbtimes)=tBG.ABs[tstmid,taid]
        if(len(sbtrk) == 0): continue
        print 'OOO------------ tstmid',tstmid,' taid: ',taid,' tdtg: ',tdtg
        print

        kk=sbtrk.keys()
        kk.sort()
        for k in kk:
            print 'BBB:  %10.0f %5.1f %6.1f %3.0f %4.0f'%(k,sbtrk[k][0],sbtrk[k][1],sbtrk[k][2],sbtrk[k][3])
        print
        kk=satrk.keys()
        kk.sort()
        for k in kk:
            print 'AAA:  %10.0f %5.1f %6.1f %3.0f %4.0f'%(k,satrk[k][0],satrk[k][1],satrk[k][2],satrk[k][3])

            

MF.dTimer('all-inner')
MFb.dTimer('all-outer')

