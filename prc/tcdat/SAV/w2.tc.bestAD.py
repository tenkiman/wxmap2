#!/usr/bin/env python

from tcbase import *
tD=TcData()

class AdeckCmdLine(CmdLine,AdeckSources):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv
        
        self.argv=argv
        self.argopts={
            1:['source',  '''source1[,source2,...,sourceN]'''],
            }

        self.options={
            'yearopt':        ['y:',None,'a','year'],
            'dtgopt':         ['d:',None,'a','year'],
            'aliasopt':       ['a:',None,'a','aliasopt'],
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
            'warn':           ['W:',0,1,'warning'],
            'update':         ['u',0,1,'only update adeck'],
            'doclean':        ['K',0,1,"""blow away .pypdb file because shelf created with 'c' option """],
            'dofilt9x':       ['9',0,1,"""don't process 9X storms"""],
            'phr':            ['h:',None,'i',"""phr -- do 'I' (6) and '2'(12) trackers"""],
            'dojettrack':     ['J',0,1,"""use trackers run on jet vice genesis tracker"""],
            'doVdeck':        ['v',0,1,"""run vdeck after doing adeck"""],
            'md2tag':         ['t:',None,'a','tag for opening mdecks2'],
            'dochkifopen':    ['o',0,1,'do chkifopen in M.DataSets MF.chkIfFileIsOpen'],
            }

        self.purpose='''
parse and create adeck card data shelves
sources: %s'''%(self.sourcesAll)
        self.examples='''
%s -S 12l.11'''


#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# main

CL=AdeckCmdLine(argv=sys.argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

source='best'
model='best'

iyearopt=yearopt
if(yearopt == 'cur' or yearopt == 'ops' or yearopt == None):
    yearopt=curyear
    year=curyear
    years=[year]

dsbdir="%s/DSs"%(TcDataBdir)

if(stmopt != None): tstmids=MakeStmListABdecks(stmopt,verb=1,dofilt9x=1)
#if(stmopt != None): tstmids=MakeStmList(stmopt,verb=verb,dofilt9x=1)
else: tstmids=None

if(tstmids == None): pass
elif(len(tstmids) == 0): errAD('tstmids')

if(tstmids != None and iyearopt == None):
    years=getYearsFromStmids(tstmids)

year=years[0]

dbtype='adeck'
dbname="%s_%s_%s"%(dbtype,source,year)
dbfile="%s.pypdb"%(dbname)
DSs=DataSets(bdir=dsbdir,name=dbfile,dtype=dbtype,verb=verb,doDSsWrite=1)

dbname='mdecks'
dbfile="%s.pypdb"%(dbname)
mDSs=DataSets(bdir=dsbdir,name=dbfile,dtype=dbname,verb=verb)
mD=mDSs.getDataSet(key=year).md


otaus=range(0,120+1,6)

ads={}

for tstmid in tstmids:
    allacards={}
    btcs=tD.getBtcs4Stmid(tstmid,dobt=1)
    dtgs=btcs.keys()
    dtgs.sort()
    for dtg in dtgs:
        trk={}
        for otau in otaus:
            odtg=mf.dtginc(dtg,otau)
            try:
                btc=btcs[odtg]
            except:
                btc=None
                
            if(btc != None):
                (btlat,btlon,btvmax,btpmin,
                 btdir,btspd,
                 tccode,wncode,
                 cqtrkdir,cqtrkspd,cqdirtype,
                 b1id,tdo,ntrk,ndtgs,
                 r34m,r50m,alf,sname,
                 r34,r50,depth)=btc

                trk[otau]=[btlat,btlon,btvmax,btpmin,r34,r50]
                     
                if(verb): print tstmid,otau,odtg,btlat,btlon,r34,r50

        if(len(trk) > 0):
            acards=MakeAdeckCards(model,dtg,trk,tstmid)
            for acard in acards:
                print acard[:-1]
            allacards[dtg]=acards

    adkey="%s_%s"%(model,tstmid)
    ad=makeAdeckByCards(mD,allacards)
    ads[adkey]=ad[0]
    DSs.putDataSet(ad[0],adkey,verb=1)

if(len(ads.keys()) > 0):
    PutDsDictKeys2DataSets(ads,DSs)

                        


