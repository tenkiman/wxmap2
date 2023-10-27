#!/usr/bin/env python

from tcbase import *

#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
#
# command line setup
#
class AdeckCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv
        
        self.argv=argv
        self.argopts={
            1:['emean',  '''name of ensemble mean
            
  psdr2  :: RR2  1-10 PSD                 atcf name: rr2em (mean); rr2es (spread)
  ngeps  :: GEFS 1-20 NCEP                atcf name: faemn (mean); faesp (spread)
  eeps   :: EPS  1-50 ECMWF               atcf name: feemn (mean); feesp (spread)
  neeps  :: EPS  1-50 from NCEP trackers  atcf name: neemn (mean); neesp (spread)
  fgeps  :: FIMENS 01-10 + GEFS 11-20     atcf name: ffgmn (mean); ffgsp (spread)
  fgops  :: FIMENS 01-05                  atcf name: fgomn (mean); fgosp (spread)
  fgfps  :: FIMENS 06-10                  atcf name: fgfmn (mean); fgfsp (spread)'''],
            }

        self.defaults={
            'doupdate':0,
            }

        self.options={
            'override':       ['O',0,1,'override'],
            'verb':           ['V',0,1,'verb=1 is verbose'],
            'ropt':           ['N','','norun',' norun is norun'],
            'doput':          ['P',1,0,'do NOT put ensemble adecks to ad2-BB-YYYY.pypdb'],
            'stmopt':         ['S:',None,'a','stmopt'],
            'dtgopt':         ['d:',None,'a','dtgopt'],
            'dobt':           ['b',1,0,'dobt=1 UNLESS set...do ALL TCs and pTCs'],
            'do9Xonly':       ['9',0,1,'just do 9X'],
            'dssDir':         ['D:',None,'a','set base dir for DSs'],
            
            }

        self.purpose='''
purpose -- parse and create ensemble mean adeck2
'''
        self.examples='''
%s test
'''
    def errAD(option,opt=None):
        
        if(option == 'stmopt'):
            print 'EEE must set -S stmopt'
        else:
            print 'Stopping in errAD: ',option
            sys.exit()
                
#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
# main
#

aliases={}

argv=sys.argv
CL=AdeckCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)

# -- DSs dir
#
if(dssDir != None):
    dsbdir=dssDir
else:
    dsbdir="%s/DSs"%(TcDataBdir)

(tstmids,tD,tstmids9Xall)=getTstmidsAD2FromStmoptDtgopt(stmopt,dtgopt,dobt=dobt)

if(tstmids == None): pass
elif(len(tstmids) == 0): errAD('tstmids')

(A2DSs,B2DS,dbnames,basins,byears)=getAdeck2Bdeck2DSs(tstmids,dsbdir=dsbdir)
MF.sTimer("adE-all")
adE=AdeckEnsemble(tD,tstmids,A2DSs,B2DS,dbnames,basins,byears,emean,tdir=dsbdir,corrTauInc=12,verb=verb)
MF.dTimer("adE-all")

if(doput and len(adE.ad2s) > 0):
    MF.sTimer("adE-put")
    adE.putAd2s()
    MF.dTimer("adE-put")
    

sys.exit()

