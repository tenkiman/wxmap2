#!/usr/bin/env python

from AD import *


#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
#
# command line setup
#

class FimyCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv
        
        self.argv=argv
        self.argopts={
            1:['dtgopt',    'no default'],
            }

        self.defaults={
            'model':'fimy',
            }

        self.options={
            'override':['O',0,1,'override'],
            'verb':['V',0,1,'verb=1 is verbose'],
            'ropt':['N','','norun',' norun is norun'],
            'dolsonly':['l',0,1,'ls on local/mss'],
            }

        self.purpose='''
purpose -- manage w2flds local and mss
%s cur
'''
        self.examples='''
%s cur
'''


def getTrkpath(dtg,sdirs,mintau=126,
               dotaus=1):

    if(dotaus):
        taus=[]
        for sdir in sdirs:
            (dir,tau)=os.path.split(sdir)
            taus.append(int(tau))

        taus.sort()

        trkDir=None
        trkPath=None

        if(mintau in taus):
            trkDir="%s/%d"%(dir,mintau)
            trkPath=glob.glob("%s/track.%s*"%(trkDir,dtg))[0]
    else:

        if(len(sdirs) == 0):
            trkPath=None
        else:
            (trkDir,file)=os.path.split(sdirs[0])
            trkPath=glob.glob("%s/track.%s*"%(trkDir,dtg))[0]
            if(len(trkPath) == 0): trkPath=None

    return(trkPath)


def getDSs(dtg,trkPath,
           source='fimy',
           abdtype='adeck'):

    dsbdir="%s/DSs"%(TcDataBdir)

    adbtype='adeck'
    year=dtg[0:4]
    adbname="%s_%s_%s"%(adbtype,source,year)
    adbfile="%s.pypdb"%(adbname)
    aDS=DataSets(bdir=dsbdir,name=adbfile,type=adbtype,verb=verb)

    dbname='mdecks'
    dbfile="%s.pypdb"%(dbname)
    DSs=DataSets(bdir=TcDssbdir,name=dbfile,type=dbname,verb=verb)
    
    mD=DSs.getDataSet(key=year).md

    return(aDS,mD)

    




#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
# main
#


argv=sys.argv
CL=FimyCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

dtgs=mf.dtg_dtgopt_prc(dtgopt)


aliases={'f8c':'FIMY'}

# -- make adeck pypdb
#
dsbdir="%s/DSs"%(TcDataBdir)

# -- secondary
sbdir2='/lfs1/projects/fim/fiorino/tmp/adeck/rtfimy'

for dtg in dtgs:
    
    mask="%s/*%s00/tracker_C/*"%(sbdir1,dtg)
    sdirs=glob.glob(mask)
    trkPath=getTrkpath(dtg,sdirs)
    print 'TTT111 ',trkPath,' in: ',mask

    # -- if no trackers in primary, go to secondary
    #
    if(trkPath == None):
        mask="%s/*%s*"%(sbdir2,dtg)
        sdirs=glob.glob(mask)
        trkPath=getTrkpath(dtg,sdirs,dotaus=0)
        print 'TTT222 ',trkPath

    if(trkPath == None):  continue
    
    (aDS,mD)=getDSs(dtg,trkPath)
    aD=Adeck(trkPath,mD,aliases=aliases)
    aD.writeAcards(taids=['fimy'],
                   tdir='/lfs1/projects/tcmt/tier1',
                   tag='FIMY_dv010_%s'%(dtg))

sys.exit()















year='2010'


vdbtype='vdeck'
vdbname="%s_%s_%s"%(vdbtype,source,year)
vdbfile="%s.pypdb"%(vdbname)
vDS=DataSets(bdir=dsbdir,name=vdbfile,type=vdbtype,verb=verb)


bdir='/w21/prj/tc/ncep_3emn_20110412'
ad=AdeckSource(source=source,
               year=year,
               dirname=source,
               bdir=bdir,
               sdir=bdir,
               stype=source,
               )
            
smask="%s/adeck*%s*%s*.txt"%(ad.bdir,source,ad.year)
#smask="%s/adeck*%s*%s*.05.txt"%(ad.bdir,source,ad.year)
                
print 'SSSSSS setAdeckSources.smask: ',smask
ad.admasks=[smask]

aliases={}
aliases['6emn']='6emn'

adecks=ad.getAdecks(source,year)
adps=AtcfAdeckPaths(adecks=adecks)

skipcarq=1
ads=MakeAdecksByYear(adps,year,aliases=aliases,skipcarq=skipcarq,doplusrelabel=0,verb=0)

aDS.verb=1
PutAdecks2DataSets(ads,adps,aDS)


if(len(ads.keys()) > 0):
    PutDsDictKeys2DataSets(ads,aDS)
                           

# -- vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
#

quiet=0
verb=0
override=0
vds={}

itaids=None
tstms=None
(taids,tstmids)=GetAidsStormsFromDss(aDS,itaids,tstms,dofilt9x=1)

# -- make adeck/vdeck cmp object
#
atC=cmpAdeckVdeck()

for tstmid in tstmids:

    print 'III working tstmid: ',tstmid
    for taid in taids:

        #aaaa -- get adecks
        #
        print 'AAAA getting adeck for: ',taid,tstmid
        (AT,BT,taD)=GetAidBestTrksFromDss(aDS,taid,tstmid,verb=verb)
        if(AT == None): continue
        atC.getADtime(taD)


        #vvvv -- get previous vdecks and test for changes in adeck before doing vdeck
        #
        tvD=GetVdsFromDSs(vDS,taid,tstmid,verb=verb,returnlist=1)
        if(tvD != None):
            update=atC.cmp(taid,tstmid,taD,tvD)
            if(update == 0):
                if(not(quiet)): print 'vd for taid:',taid,' tstmid: ',tstmid,' already made ...no change in adeck...bypass...unless...override: ',override
            else:
                if(not(quiet)): print 'vd for taid:',taid,' tstmid: ',tstmid,' NEEDS uPDATING... ',override
            if(not(override) and update == 0):  continue


        vd=MakeVdeckS(BT,AT,verb=verb)
        vd.stm1id=tstmid
        if(hasattr(tvD,'adtimeVD')): vd.adtimeVD=tvD.adtimeVD
        vd.adtimeAD=taD.adtimeAD
        vd.addtgsVD=taD.dtgs


        
        vdkey="%s_%s"%(taid,tstmid)
        vds[vdkey]=vd
        vDS.putDataSet(vd,vdkey)


if(len(vds) > 0):
    PutDsDictKeys2DataSets(vds,vDS)

sys.exit()

# -- make adeck
#
adpaths='/w21/prj/tc/ncep_3emn_20110412/adeck.ncep.3emn2010.txt'
A=Adeck(adpaths,mD,aliases=aliases)

kk=A.aidcards.keys()

for k in kk:
    
    (aid,stm2id)=k

    # by pass carq ---
    #
    if(aid == 'carq' and skipcarq): continue

    acards=A.aidcards[k]

    oads=makeAdeckByCards(mD,acards,aliases=aliases)
    
    for ad in oads:
        # -- skip if ad is None
        #
        if(ad == None):
            print 'WWW None ad for : ',k
            continue

        # -- put ad in ad dict
        #
        adkey="%s_%s"%(ad.aid,ad.stm1id)
        DSs.putDataSet(ad,adkey,verb=1)


