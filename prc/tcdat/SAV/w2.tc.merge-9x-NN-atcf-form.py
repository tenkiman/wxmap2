#!/usr/bin/env python

from tcbase import *
MF=MFutils()

def parseOcardSum(ocardsum):

    tt=ocardsum.split()
    year=tt[0]
    stmidNN="%s.%s"%(tt[1][0:3],year)
    if(mf.find(ocardsum,'9X:')):
        stmid9X="%s.%s"%(tt[-3],year)
    elif(mf.find(ocardsum,'NN:')):
        stmid9X=stmidNN
        stmidNN="%s.%s"%(tt[-1],year)
    else:
        stmid9X=stmidNN
        
    basin='xxxxx'
    b1id=stmidNN[2].lower()
    for basin in TcGenBasin2B1ids.keys():
        if(b1id in TcGenBasin2B1ids[basin]): break
            
    return(stmidNN,stmid9X,basin)


def doRsync2Kishou(sdir,tdir,
                   doupdate=0,dosizeonly=0,dodelete=0,
                   ropt=''):

    pdir=w2.W2BaseDirEtc
    
    rupopt=''
    if(doupdate): rupopt='-u'

    sizonly=''
    if(dosizeonly):  sizonly='--size-only'

    delopt=''
    if(dodelete): delopt='--delete'

    rsyncopt="%s %s %s --timeout=30 --protocol=29 -alv --exclude-from=%s/ex-w21.txt"%(delopt,rupopt,sizonly,pdir)

    MF.sTimer('adc-doRsync2Kishou')
    cmd="rsync %s %s %s"%(rsyncopt,sdir,tdir)
    MF.runcmd(cmd,ropt)
    MF.dTimer('adc-doRsync2Kishou')

def replaceStm2Id(adeck,stmid,NNstmid,acards=None):


    (snum,b1id,year,b2id,stm2id,stm1id)=getStmParams(NNstmid)
    ocards=[]
    
    
    if(acards != None):
        cards=acards
    else:
        cards=MF.ReadFile2List(adeck)
        if(len(cards) == 0):
            print '0 len adeck: ',adeck
            return(ocards)
    
    tt=cards[0].split(',')
    ib2=tt[0].strip()
    inn=tt[1].strip()
    
    ob2=stm2id[0:2].upper()
    onn=stm2id[2:4]
    for card in cards:
        card=card.replace(ib2,ob2,1)
        card=card.replace(inn,onn,1)
        ocards.append(card)
    
    return(ocards)


#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
#
# command line setup
#

class TCVCAdeckCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):
        
        self.sources=['tmtrkN','mftrkN','ecmwf','ecbufr','ukmo','ncep','rtfim','rtfim9','psdRR2']
        self.sourcesActive=['tmtrkN','mftrkN','ecmwf','ecbufr','ukmo','ncep','clip']

        if(argv == None): argv=sys.argv
        
        self.argv=argv
        self.argopts={
            1:['source',  '''source1[,source2,...,sourceN]'''],
            }
            
        self.options={
            'overrideOpt':         ['O:',0,'i','override -O1 :: overrideChkAdeck=1  -O2 :: overrideInv=1   -O3 :: overrideInv/Kill/ChkAdeck=1   '],
            'verb':                ['V',0,1,'verb is verbose'],
            'ropt':                ['N','','norun',' norun is norun'],
            'stmopt':              ['S:',None,'a','relabel CCC0:NNN0 where CCC0 is current name and NNN0 is new'],
            }

        self.defaults={
            'diag':              0,
            }

        self.purpose='''
purpose -- convert tm|mftrnK to ATCF adeck as at JTWC/NHC
sources: %s'''%(self.sourcesActive)
        self.examples='''
%s tmtrkN -d 2014090700.2014090800 -y 2014
'''

#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# -- main
#
CL=TCVCAdeckCmdLine(argv=sys.argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

MF.sTimer('ALL-ADC-MERGE')
(tstmids,tD,tstmids9Xall)=getTstmidsAD2FromStmoptDtgopt(stmopt,dobt=1)

# -- sources
#
if(source == 'all'):
    sources=CL.sourcesActive
else:
    sources=source.split(',')
    source=sources[0]

for source in sources:
    
    for tstmid in tstmids:
        (ocards,ocardsum)=tD.getDSsStmCards(tstmid)
        (stmidNN,stmid9X,basin)=parseOcardSum(ocardsum)
        
        rc=getStmParams(stmid9X)
        s2id9=rc[0]
        rc=getStmParams(stmid9X,convert9x=1)
        snum9=rc[0]
        stmid9=rc[-1]
        
        rc=getStmParams(stmidNN)
        byear=rc[2]
        b2id=rc[3].lower()
        s2idN=rc[0]
        
        tdir="%s/%s/%s"%(TcAdecksAtcfFormDir,byear,source)
        
        adeckNN="%s/a%s%s%s.dat"%(tdir,b2id,s2idN,byear)
        adeckNNsav="%s/a%s%s%s.dat-SAV"%(tdir,b2id,s2idN,byear)
        adeck9X="%s/a%s%s%s.dat"%(tdir,b2id,s2id9,byear)
        
        rcNN=MF.ChkPath(adeckNN)
        rcNNsav=MF.ChkPath(adeckNNsav)
        rc9X=MF.ChkPath(adeck9X)
        
        
        if(verb): print 'rcNN ',rcNN,' rcNNsav',rcNNsav,'rc9X ',rc9X
        
        if(rcNN and not(rcNNsav) and rc9X):

            
            if(ropt == 'norun'):
                print 'DDDD---- would do source: ',source,' stmid: ',tstmid,' stmid9X: ',stmid9X
                continue
            
            print '   NN: ',adeckNN
            print 'NNsav: ',adeckNNsav
            print '   9X: ',adeck9X
            
            acardsN=MF.ReadFile2List(adeckNN)
            cmd="mv %s %s"%(adeckNN,adeckNNsav)
            mf.runcmd(cmd)
            acards9=MF.ReadFile2List(adeck9X)
            ocards9=replaceStm2Id(adeck9X,stmid9,stmidNN,acards=acards9)
            ocards=ocards9+acardsN
            MF.WriteList2File(ocards,adeckNN)
        elif(rcNN and not(rc9X)):
            print 'IIII---- for source: ',source,' stmid: ',tstmid,' NO adeck for stmid9x: ',stmid9X
        else:
            print 'WWWW---- for source: ',source,' stmid: ',tstmid,' already merged in stmid9x: ',stmid9X
            continue
        
        
MF.dTimer('ALL-ADC-MERGE')

sys.exit()
    
