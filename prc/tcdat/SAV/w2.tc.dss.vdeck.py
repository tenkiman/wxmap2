#!/usr/bin/env python

from tcbase import *
from vdCL import *


#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
#
# command line setup
#

class VdeckCmdLine(CmdLine,AdeckSources):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv
        
        self.argv=argv
        self.argopts={
            1:['source',  '''source1[,source2,...,sourceN]'''],
            }
            
        self.options={
            'yearopt':             ['y:',None,'a','year | year1,year2 | year1.yearN = year1,year2,year3...yearN | year1-year2 to setYearMasks=1'],
            'override':            ['O',0,1,'override'],
            'chkoverride':         ['C',0,1,'override source chk'],
            'doclean':             ['K',0,1,'rm the vdeck db file'],
            'verb':                ['v',0,1,'verb=1 is verbose'],
            'verb2':               ['V',0,1,'verb=2 is verbose'],
            'quiet':               ['q',0,1,'1 - turn off all diag messages'],
            'ropt':                ['N','','norun',' norun is norun'],
            'doemean':             ['M',0,1,'1 - make eps mean/spread -> adeck cards -> vdeck'],
            'dovdecks':            ['D',1,0,'1 - adeck cards -> vdeck'],
            'dols':                ['l',0,1,'1 - list'],
            'dolslong':            ['L',0,1,'1 - long list'],
            'dolsfull':            ['F',0,1,'1 - full list'],
            'stmopt':              ['S:',None,'a','stmopt'],
            'aidopt':              ['T:',None,'a','taid'],
            'warn':                ['W',0,1,'warning'],
            'do9xNOT':             ['9',1,0,'if set dofilt9x=0; do9xrelab=1'],
            'qcSpeed':             ['Q',1,0,'turn OFF ad.qcMotion()'],
            'aliasopt':            ['a:',None,'a','aliasopt iname:oname'],
            'dtgopt':              ['d:',None,'a','single dtg'],
            }

        self.defaults={
            'dssverb':           1,
            'unlinkopt':         0,
            'diag':              0,
            }

        self.purpose='''
purpose -- create vdecks from adeck cards
sources: %s'''%(self.sources)
        self.examples='''
%s test
'''


    def ChkSource(self,year=None):

        if(year != None):
            self.getSourcesbyYear(year)
            
        iok=0
        for s in self.sources:
            if(self.source == s): iok=1 ; break

        return(iok)





def errAD(option,opt=None):

    if(option == 'tstmids'):
        print 'EEE # of tstmids = 0 :: no stms to verify...stmopt: ',stmopt,' for errAD option: ',option
    elif(option == 'tstms'):
        print 'EEE # of tstms from stmopt: ',stmopt,' = 0 :: no stms to verify...'
    elif(option == 'omodel'):
        print 'EEE omodel not set in SetMeanSpreadOmodels for source: ',option
    elif(option == 'vdeckitaids'):
        print 'EEE must set -T aidopt when dovdeck=1 (default)'
    else:
        print 'Stopping in errAD: ',option

    sys.exit()
        

def warnAD(option,opt=None):

    if(option == 'taids'):
        print 'WWW # of taids = 0 :: no stms to verify...stmopt: ',stmopt
    else:
        print 'continuing in warnAD: ',option


def getAliasesFromAliasOpt(aliasopt,verb=1):
    
    aliases=[]
    if(aliasopt == None): return(aliases)
        
    aos=aliasopt.split(',')
    for ao in aos:
        tt=ao.split(':')
        if(len(tt) == 2):
            (iname,oname)=(tt[0],tt[1])
        else:
            (iname,oname)=(None,None)
    
        if(iname != None):
            aliases.append([iname,oname])
            
    return(aliases)


#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
# main
#

CL=VdeckCmdLine(argv=sys.argv)
CL.CmdLine()
exec(CL.estr)
if(verb or verb2): print CL.estr

if(verb2): verb=2

aliasesVD=getAliasesFromAliasOpt(aliasopt)

sources=source.split(',')



iyearopt=yearopt
if(yearopt == 'cur' or yearopt == 'ops' or yearopt == None):
    yearopt=curyear
    year=curyear
    years=[year]
    iyearopt=None

if(iyearopt != None):
    
    if(len(iyearopt.split('.')) == 2):
        years=MF.YearRange(iyearopt.split('.')[0],iyearopt.split('.')[1])
        
    elif(len(iyearopt.split('-')) == 2):
        years=MF.YearRange(iyearopt.split('-')[0],iyearopt.split('-')[1])

    elif(len(iyearopt.split(',')) > 1):
        years=iyearopt.split(',')

    elif(len(iyearopt.split(',')) == 1):
        years=iyearopt.split(',')

# -- all storms single year
#
if(stmopt == None and len(years) == 1):
    tstms=MakeStmList(stmopt,yearopt=years[0],verb=verb)

else:
    tstms=MakeStmList(stmopt,verb=verb)
    if(len(tstms) == 0): errAD('tstms')

    if(tstms != None and iyearopt == None):
        years=getYearsFromStmids(tstms)
        
# -- dtg processing -- get stmids and years
#
if(dtgopt != None):
    dtgs=mf.dtg_dtgopt_prc(dtgopt)
    tD=TcData(dtgopt=dtgs[-1])
    tstms=tD.getStmidDtgs(dtgs)
    years=getYearsFromStmids(tstms)

if(len(sources) > 1 or source == 'all' or len(years) > 1):

    for year in years:
        
        if(source == 'all'): sources=CL.getSourcesbyYear(year)
        for source in sources:
            cmd="%s %s -y %s"%(CL.pypath,source,year)
            for o,a in CL.opts:
                if(o != '-y'):
                    cmd="%s %s %s"%(cmd,o,a)
            mf.runcmd(cmd,ropt)
            
    sys.exit()


if(len(years) == 1): year=years[0]

if(not(CL.ChkSource(year)) and not(chkoverride)):
    
    if(diag): print 'WWW not a standard source:',source,""" we'll try using adeck from AD.AdeckSource class..."""

    (ad,aliases)=CL.setAdeckSource(source,year,verb=verb)

    if(ad == None and source != 'e3mn'):
        print """EEE don't know how to make AdeckSource class for: """,source
        sys.exit()



DSss={}
dsbdir="%s/DSs"%(TcDataBdir)

# -- make adeck/vdeck cmp object
#
atC=cmpAdeckVdeck()

# datasets setup -- adeck (input)
#
dbtypes=['adeck','vdeck']
for dbtype in dbtypes:
    dbname="%s_%s_%s"%(dbtype,source,year)
    dbfile="%s.pypdb"%(dbname)
    
    # -- blow away vdeck if docclean
    #
    if(dbtype == 'vdeck' and doclean): unlinkopt=1
    if(dbtype == 'adeck'): doDSsWrite=0
    if(dbtype == 'vdeck'): doDSsWrite=1
    DSss[dbtype]=DataSets(bdir=dsbdir,name=dbfile,dtype=dbtype,verb=dssverb,unlink=unlinkopt,doDSsWrite=doDSsWrite)

# get aids and storms from shelve; setup vdeck dataset
#
aDS=DSss['adeck']
vDS=DSss['vdeck']

        
if(aidopt != None):    itaids=aidopt.split(',')
else:                  itaids=None

if(dols or dolslong or dolsfull):
    lsopt='s'
    if(dolslong): lsopt='l'
    if(dolsfull): lsopt='f'
    (taids,tstmids)=LsAidsStormsDss(vDS,tstms,itaids,dofilt9x=do9xNOT,lsopt=lsopt)

    if(dolsfull):
        for tstmid in tstms:
            try:
                itaids=taids[tstmid]
            except:
                itaids=[]

            if(len(itaids) > 0):
                for taid in itaids:
                    tvD=GetVdsFromDSs(vDS,taid,tstmid,verb=verb,returnlist=1)
                    bdtgs=tvD.BT.dtgs
                    tvD.lsFE(bdtgs)
                    tvD.AT.lsAT(tvD.stmid)
                    
                    #tvD.AT.ls()
                    #tvD.ls()
                    #tvD.ls()
                    #tvD.BT.lsBT()

    sys.exit()



#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm - ensemble means/spread
#
if(doemean):
    makeEnsMeanVdeck(aDS,vDS,tstms,dtau=12,etau=120,doput=0)

#vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv straight vdecks
#
elif(dovdecks):

    vds={}

    (taids,tstmids)=GetAidsStormsFromDss(aDS,itaids,tstms,dofilt9x=do9xNOT)
    
    if(len(tstmids) == 0):  errAD('tstmids')
    if(len(taids) == 0):    warnAD('taids')

    if(ropt == 'norun'):
        print 'will do vdecks for  tstmids: ',tstmids
        print 'will do vdecks for    taids: ',taids
        sys.exit()

    for tstmid in tstmids:

        if(verb): print 'III working tstmid: ',tstmid
        for taid in taids:

            #aaaa -- get adecks
            #
            print 'AAAA getting adeck for: ',taid,tstmid
            (AT,BT,taD)=GetAidBestTrksFromDss(aDS,taid,tstmid,verb=verb)
            if(AT == None): continue
            atC.getADtime(taD)

            BT.dtgs.sort()

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


            vd=MakeVdeckS(BT,AT,etau=168,verb=verb,qcSpeed=qcSpeed)
            vd.stm1id=tstmid
            if(hasattr(tvD,'adtimeVD')): vd.adtimeVD=tvD.adtimeVD
            vd.adtimeAD=taD.adtimeAD
            vd.addtgsVD=taD.dtgs

            # -- aliasesVD
            #
            otaid=taid
            for alias in aliasesVD:
                (iname,oname)=alias
                if(taid == iname): 
                    otaid=oname
                    print 'AAAlias tstmid: ',tstmid,' for taid:',taid,' otaid:',otaid
                    
            vdkey="%s_%s"%(otaid,tstmid)
            
            vds[vdkey]=vd
            vDS.putDataSet(vd,vdkey)


    if(len(vds) > 0):
        PutDsDictKeys2DataSets(vds,vDS)

else:
    print 'WWW neither -m (mean/spread) or dovdeck (default; -D turns off) set...'
    
