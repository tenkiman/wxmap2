#!/usr/bin/env python

from tcbase import *

def getDtgFiltOpts(filterOpts):
    
    filt0012=0
    filt0618=0
    filt00=0
    filt12=0
    
    if(filterOpts != None):
        
        for filterOpt in filterOpts:
            if(filterOpt.upper() == 'Z0012'): filt0012=1
            if(filterOpt.upper() == 'Z0618'): filt0618=1
            if(filterOpt.upper() == 'Z00'):   filt00=1
            if(filterOpt.upper() == 'Z12'):   filt12=1
            
    return(filt0012,filt0618,filt00,filt12)
        


#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# -- command line setup
#

class Adeck2CmdLine(CmdLine,AdeckSources):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv
        
        self.argv=argv
        self.argopts={
            1:['source',  '''source1[,source2,...,sourceN]'''],
            }

        self.defaults={
            }
            
        self.options={
            'dssDir':              ['D:',None,'a','set base dir for DSs'],
            'opath':               ['o:','/tmp/adeck.dat','a',"""
opath -- where to output
"""
                                    ],
            'verb':                ['V',0,1,'verb is verbose'],
            'quiet':               ['q',0,1,'1 - turn off all diag messages'],
            'ropt':                ['N','','norun',' norun is norun'],
            'stmopt':              ['S:',None,'a','stmopt'],
            'dtgopt':              ['d:',None,'a','dtgopt to get tstmids'],
            'aidopt':              ['T:',None,'a','taid'],
            'doput':               ['P',1,0,'do NOT put a|vdeck2'],
            'doAppend':            ['A',0,1,'append cards to opath'],
            'filterOpts':          ['f:',None,'a',"""filterOpt:
       synop time only:    'z0012'|'z00'|'z12' | 'z0618'
       use comma delimited for multiple filterOpt, e.g., z0012,tau072
"""],
            
            }

        self.defaults={
            'diag':              0,
            }

        self.purpose='''
purpose -- filter out adeck cards from source by taid
sources: %s'''%(self.sources)
        self.examples='''
%s -S 01a.12 -T avno,clip    # relabel and add c120 -> clip5
'''


def errAD(option,opt=None):

    if(option == 'tstmids'):
        print 'EEE # of tstmids = 0 :: no stms to verify...stmopt: ',stmopt,' for errAD option: ',option
    elif(option == 'stmopt'):
        print 'EEE must set -S stmopt OR -d dtgopt'
    elif(option == 'source'):
        print 'EEE must set source for no plain args and NOT doing -l -L'
    elif(option == 'taids'):
        print 'EEE must set taids'
    else:
        print 'Stopping in errAD: ',option
    sys.exit()
        

def warnAD(option,opt=None):

    if(option == 'taids'):
        print 'WWW # of taids = 0 :: no stms to verify...stmopt: ',stmopt
    else:
        print 'continuing in warnAD: ',option



#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
# main
#

CL=Adeck2CmdLine(argv=sys.argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr
    
#
isources=source.split(',')

sources=[]
for isource in isources:
    source=isource
    if( (mf.find(source,'jt') or mf.find(source,'nh') ) ): source='jt-nhc'
    sources.append(source)
    

# -- stmids
#
if(stmopt == None and dtgopt == None): errAD('stmopt')

if(stmopt != None and (mf.find(stmopt,'all'))):
    stmopt=getAllStmopt(stmopt)

    
# -- loop
#

if(len(sources) > 1):
    for source in sources:
        cmd="%s %s -o"%(CL.pypath,source)
        for o,a in CL.opts:
            cmd="%s %s %s"%(cmd,o,a)
        mf.runcmd(cmd,ropt)
        
    sys.exit()

# -- taids
#
taids=None

if(aidopt != None):
    taids=aidopt.split(',')
else:
    errAD('taids')

# -- test if stmopt 9X
#
do9Xonly=0
if(stmopt != None and Is9Xstmopt(stmopt)): do9Xonly=1

# -- get tstmids
#
dobt=1
(tstmids,tD,tstmids9Xall)=getTstmidsAD2FromStmoptDtgopt(stmopt,dtgopt,do9Xonly,dobt,source)

if(ropt == 'norun'):
    print 'NNN will do tstmids:',tstmids
    sys.exit()

# -- YYYYYYYYYYYYYYYYYYYYYYYYYYYY years
#
syears=getYearsFromStmids(tstmids)

# -- mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm -- main processing section
#
MF.sTimer('ads-all')

# -- inventory of acards
#
ad2Is={}
if(ropt != 'norun'):
    for syear in syears:
        ad2Is[syear]=AdToAtcfInvHash(source,byear=syear,bnameBase='Inv-AD2',
                                      verb=1,
                                      )
# -- FFFFFF -- tau filter 
#
if(filterOpts != None): filterOpts=filterOpts.split(',')
(filt0012,filt0618,filt00,filt12)=getDtgFiltOpts(filterOpts)


allCards=[]
for tstmid in tstmids:
    (cards,byear,prependAid)=getAcards(source,tstmid,ad2Is,taids=taids,dtgopt=dtgopt,
                                       filt0012=filt0012,filt0618=filt0618,
                                       filt00=filt00,filt12=filt12)
    cards=cards.split('\n')
    allCards=allCards+cards
    
    if(verb):
        for card in cards:
            print card
    
    
MF.WriteList2Path(allCards,opath,append=doAppend)
    
MF.dTimer('ads-all')

sys.exit()
    
