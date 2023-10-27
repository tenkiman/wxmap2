#!/usr/bin/env python

diag=1
if(diag):
    from M import MFutils
    mf2=MFutils()
    mf2.sTimer('w2')

from tcbase import *
from ATCF import AidProp
#from VT import AidProp
if(diag): mf2.dTimer('w2')

#llllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll
# local unbounded methods

def doRsyncDSS2Kaze(doupdate=0,reverse=0,dodelete=1,
                    ropt=''):

    sdir=w2.TcDatDirDSs
    tdir="%s/%s"%(DATLocalBaseDir,sdir)
    tdir=tdir.replace('//','/')
    sdir=sdir.replace('//','/')

    pdir=w2.W2BaseDirEtc
    
    rupopt=''
    if(doupdate): rupopt='-u'

    sizonly=''
    if(reverse):  sizonly='--size-only'

    delopt=''
    if(dodelete): delopt='--delete'

    rsyncopt="%s %s %s -alv --exclude-from=%s/ex-w21.txt"%(delopt,rupopt,sizonly,pdir)

    MF.sTimer('adk-doRsyncDSS2Kaze')
    cmd="rsync %s %s/ %s/"%(rsyncopt,sdir,tdir)
    MF.runcmd(cmd,ropt)
    MF.dTimer('adk-doRsyncDSS2Kaze')
    
    
def doRsyncK2K(sdir,ropt='',doupdate=0,dodelete=0,reverse=0,sizeonly=0,rsyncXopts=None):

    tdir="%s/%s"%(DATKazeBaseDir,sdir)
    if(mf.find(W2Host,'taifuu')):   tdir=sdir

    tdir=tdir.replace('//','/')
    sdir=sdir.replace('//','/')
        
    if(mf.find(tdir,'-BAK')): tdir=tdir.replace('-BAK','')

    if(ropt == '' and not(mf.find(tdir,'pypdb'))): MF.ChkDir(tdir,'mk')
    
    if(reverse):
        sdirin=sdir
        sdir=tdir
        tdir=sdirin

    if(w2.onKaze or mf.find(W2Host,'taifuu') ):

        if(reverse):
            tdir="fiorino@kishou.fsl.noaa.gov:/%s"%(tdir)
        else:
            sdir="fiorino@kishou.fsl.noaa.gov:/%s"%(sdir)
        
    tdir=tdir.replace('//','/')
    sdir=sdir.replace('//','/')
    pdir=LocalBaseDirEtc
    if(mf.find(W2Host,'taifuu')):  pdir=w2.W2BaseDirEtc

    rupopt=''
    if(doupdate): rupopt='-u'

    sizonly=''
    if(sizeonly):  sizonly='--size-only'

    delopt=''
    if(dodelete): delopt='--delete'

    rsyncopt="--timeout=100 %s %s %s -alv --exclude-from=%s/ex-w21.txt"%(delopt,rupopt,sizonly,pdir)

    if(rsyncXopts != None):
        rsyncopt="%s %s"%(rsyncopt,rsyncXopts)

    if(reverse):
        if(not(mf.find(sdir,'pypdb'))):
            cmd="rsync %s %s/ %s/"%(rsyncopt,sdir,tdir)
        else:
            cmd="rsync %s %s %s"%(rsyncopt,sdir,tdir)
    else:
        if(not(mf.find(sdir,'pypdb'))):
            MF.ChkDir(tdir,'mk')
            cmd="rsync %s %s/ %s/"%(rsyncopt,sdir,tdir)
        else:
            cmd="rsync %s %s %s"%(rsyncopt,sdir,tdir)
        
    mf.runcmd(cmd,ropt)


         
#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
#
# command line setup
#

class AdeckCmdLine(CmdLine,AdeckSources):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv
        
        self.argv=argv
        self.argopts={
            1:['source',  '''source1[,source2,...,sourceN]'''],
            }

        self.defaults={
            'dorsync2kaze':0,
            'setYearMask':0,
            'yearMasks':None,
            }

        self.options={
            'test':                ['x',0,1,'test switch'],
            'yearopt':             ['y:',None,'a','year'],
            'dtgopt':              ['d:',None,'a','year'],
            'aliasopt':            ['a:',None,'a','aliasopt iname:oname only for -D (doacardout=1)'],
            'override':            ['O',0,1,'override'],
            'verb':                ['V',0,1,'verb=1 is verbose'],
            'ropt':                ['N','','norun',' norun is norun'],
            'doadecks':            ['A',1,0,'0 - no NOT make adecks'],
            'useAdeckDir':         ['E',0,1,'for tmtrkN and mftrkN, use dat/tc/adeck vice dat/tc/tmtrkN'],
            'doacardout':          ['D',0,1,'1 - output acards'],
            'doputdss':            ['P',1,0,'0 - do NOT putDSs'],
            'dols':                ['l',0,1,'1 - list'],
            'dolslong':            ['L',0,1,'1 - long list'],
            'dolsfull':            ['F',0,1,'1 - full list'],
            'dolooper':            ['r',1,0,'do NOT use loop logic'],
            'doYearLooper':        ['e',1,0,'do NOT use year loop logic'],
            'stmopt':              ['S:',None,'a','stmopt'],
            'aidopt':              ['T:',None,'a','taid'],
            'warn':                ['W:',0,1,'warning'],
            'update':              ['u',0,1,'only update adeck'],
            'doclean':             ['K',0,1,"""blow away .pypdb file because shelf created with 'c' option """],
            'dofilt9x':            ['9',0,1,"""don't process 9X storms"""],
            'phr':                 ['h:',None,'i',"""phr -- do 'I' (6) and '2'(12) trackers"""],
            'dojettrack':          ['J',0,1,"""use trackers run on jet vice genesis tracker"""],
            'doVdeck':             ['v',0,1,"""run vdeck after doing adeck"""],
            'dochkIfRunning':      ['o',0,1,'do chkifrunning in M.DataSets MF.chkIfFileIsOpen'],
            'chkoverride':         ['C',0,1,'override source chk'],
            'ZIPoverride':         ['Z',0,1,'ZIP override'],
            'useZipArchive':       ['z',0,1,"""USE the ZipArchive -- it's broken and putDataSet is fast enough..."""],
            'doRsync2Kishou':      ['R',1,0,'do NOT rysnc dss to kishou'],
            'strictChkIfRunning' : ['s',0,1,'strict check if running -- any instance'],
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
    else:
        print 'Stopping in errAD: ',option

    sys.exit()
        
#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# main

MF.sTimer('all')
CL=AdeckCmdLine(argv=sys.argv)
CL.CmdLine()
exec(CL.estr)

sources=source.split(',')

# -- get command line vars, except -N
pyfileopt=''
for s in sys.argv[1:]:
    if(s != '-N'):
        pyfileopt='%s %s'%(pyfileopt,s)

# -- determine if we need to span multiple years for this source
#
Asources=set(sources)
Bsources=set(CL.sourcesDtg)
stestDtg=Asources.intersection(Bsources)
stestDtg=len(stestDtg)

# -- listing and opts
#
doListingOpt=''
doListing=(dols or dolslong or dolsfull)
if(doListing):
    if(dols):     doListingOpt='-l'
    if(dolslong): doListingOpt='-L'
    if(dolsfull): doListingOpt='-F'
    

dtgs=[]
if(dtgopt != None):
    dtgs=mf.dtg_dtgopt_prc(dtgopt)

#ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc -- check if job is running and .pypdb may be open...
# -- add check if running, if so then cycle until it's stopped; 
#    more precise check of job by including cmd line string
#
if(dochkIfRunning == 0 and len(sources) == 1 or strictChkIfRunning):

    # -- still getting conflicts when doing updating -- corrupts either zipfile or pypdb
    #    current config
    #jobopt=pyfileopt
    #killjob=1
    #    new config -- wait five minutes before bailing -- don't depend on jobopt
    # -- go back to old settings?
    jobopt=pyfileopt.split()[0]
    # -- this causes a big problem when more than one adk is running -- from fp2 -T
    #killjob=0
    killjob=1
    
    MF.sTimer('adk-chkIfJobIsRunning pyfile: %s jobopt: %s killjob: %s'%(pyfile,jobopt,killjob))
    rc=MF.chkRunning(pyfile,strictChkIfRunning=strictChkIfRunning,
                     killjob=killjob,verb=verb,nminWait=1,timesleep=5)
    MF.dTimer('adk-chkIfJobIsRunning pyfile: %s jobopt: %s killjob: %s'%(pyfile,jobopt,killjob))

#yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy -- yearopt == None or cur|ops
#
yearsAll=[]
years=[]
iyearopt=yearopt
if(yearopt == 'cur' or yearopt == 'ops' or yearopt == None):
    yearopt=curyear
    year=curyear
    years=[year]
    yearsAll=years
    iyearopt=None

    (shemoverlap,yyyy1,yyyy2)=CurShemOverlap(curdtg)

    # -- use set to make an intersection of lists
    #
    if(shemoverlap):
        yearsAll=[yyyy1,yyyy2]
        if( (stestDtg == 0) or doListing ):
            years=[yyyy1,yyyy2]

if(verb): print 'yyyy111111 ',years,yearsAll
#yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy -- yearopt
#
if(iyearopt != None):

    if(len(iyearopt.split('.')) == 2):
        years=MF.YearRange(iyearopt.split('.')[0],iyearopt.split('.')[1])

    elif(len(iyearopt.split(',')) > 1):
        years=iyearopt.split(',')

    # -- special case for setting years specifically, used for mftrkN
    # -- turn off looping and set the mask...
    #
    elif(len(iyearopt.split('-')) == 2):
        years=iyearopt.split('-')
        dolooper=0
        setYearMask=1
        yearMasks=years
        
    elif(len(iyearopt.split(',')) == 1):
        years=iyearopt.split(',')
        
    yearsAll=years
    
if(verb): print 'yyyy222222 ',years,yearsAll,iyearopt

#sssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss -- stormopt
#
stmopts=[]
if(stmopt != None):
    tstmids=MakeStmList(stmopt,verb=verb)
    stmopts=stmopt.split(',')
else: tstmids=None


if(tstmids == None): 
    if(stmopt != None): print 'WWW stmopt:',stmopt,'tstmids = None, pass...'
    pass
elif(len(tstmids) == 0): errAD('tstmids')

#ddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd -- single dtg
# -- if one dtg, get stmids to set year(s)
#
gotyears1dtg=0
#if(len(dtgs) == 1 and len(years) == 0):
if(len(dtgs) == 1 and iyearopt == None):
    tD=TcData(dtgopt=dtgs[-1])
    dtstmids=tD.getStmidDtgs(dtgs)
    otstmids=[]
    if(tstmids != None): 
        for tstmid in tstmids:
            if(tstmid in dtstmids): otstmids.append(tstmid)
    if(len(otstmids) > 0): tstmids=otstmids
    else:                  tstmids=dtstmids
    
    yearsAll=getYearsFromStmids(tstmids)
    years=yearsAll
    gotyears1dtg=1

    if(verb): print 'yyyy333333 ',years,yearsAll,tstmids

#ttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt -- years based on tstmid
#
if((tstmids != None and iyearopt == None and (stestDtg == 0)) or
   (doListing and iyearopt == None and len(dtgs) < 1 and not(gotyears1dtg)) or 
   (doacardout and iyearopt == None and tstmids != None) or   # logic for acards out
   (phr != None) and
   dolooper
   ):
    
    years=getYearsFromStmids(tstmids)
    if(verb): print 'yyyy333YYY ',years,yearsAll,tstmids
    
# -- add looping by stmid for multi year in a basin do phr
#
if(aidopt != None):  taids=aidopt.split(',')
else:                taids=[] ;     #errAD('vdeckitaids')

#yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy -- yearsAll
#
yearsAll=years+yearsAll
yearsAll=mf.uniq(yearsAll)

if(verb): print 'yyyy444444 ',years,yearsAll,doListing,doListingOpt

#CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC -- cycle by source,years,dtgs,taids
#
if((len(sources) > 1 or source == 'all' or len(years) > 1 or len(dtgs) > 1 or len(taids) > 1) and dolooper ):

    dostmopt=0
    doyear=0
    dostmids=0
    dodtgopt=0
    dotaids=0

    if(tstmids != None and len(tstmids) > 1 and phr != None):
        tloops=tstmids
        dostmids=1
        
    elif(len(stmopts) > 1):
        tloops=stmopts
        dostmopt=1

    elif(len(dtgs) > 1):
        tloops=dtgs
        dodtgopt=1

    elif(len(taids) > 1):
        tloops=taids
        dotaids=1

    else:
        tloops=years
        doyear=1
        
    #if(dostmopt and len(taids) > 1):
        

    print 'dostmops',dostmopt,'dotaids',taids
    
    for tloop in tloops:
        for source in sources:

            if(source == 'all'): sources=CL.getSourcesbyYear(tloop)
            
            # -- disable chkIfJobIsRunning for cycling...using -o?  not sure this is a good idea...
            #
            chkRunOpt=''
            if(dochkIfRunning or dodtgopt): chkRunOpt='-o'
            chkRunOpt='-o'

            if(doyear):
                yearloopropt=''
                yearlistopt=''
                if(not(doYearLooper)): yearloopropt='-r'
                if(doListing):   yearlistopt=doListingOpt
                cmd="%s %s -y %s %s %s %s"%(CL.pypath,source,tloop,chkRunOpt,yearloopropt,yearlistopt)
                for o,a in CL.opts:
                    if(o != '-y' and o != '-r' and o != '-l' and o != '-L' and o != '-F'):
                        cmd="%s %s %s"%(cmd,o,a)
                mf.runcmd(cmd,ropt)

            if(dostmopt or dostmids):
                cmd="%s %s -S %s %s"%(CL.pypath,source,tloop,chkRunOpt)
                for o,a in CL.opts:
                    if(o != '-S' and (len(taids) > 1 and o != '-T' )):
                        cmd="%s %s %s"%(cmd,o,a)

                if(len(taids) > 1):
                    cmdS=cmd
                    for taid in taids:
                        cmd="%s -T %s"%(cmdS,taid)
                        mf.runcmd(cmd,ropt) 
                else:
                    mf.runcmd(cmd,ropt) 
                
            if(dotaids):
                cmd="%s %s -T %s %s"%(CL.pypath,source,tloop,chkRunOpt)
                for o,a in CL.opts:
                    if(o != '-T'):
                        cmd="%s %s %s"%(cmd,o,a)
                mf.runcmd(cmd,ropt)


            if(dodtgopt):
                cmd="%s %s -d %s %s"%(CL.pypath,source,tloop,chkRunOpt)
                for o,a in CL.opts:
                    if(o != '-d'):
                        cmd="%s %s %s"%(cmd,o,a)
                mf.runcmd(cmd,ropt)
                

    sys.exit()


# -- dochk for fimens2012
#
dochk=0
if(source == 'fimens2012' and doListing): dochk=1

# -- special case for setting year when not cycling
#
if(len(years) == 1 or (len(years) == 2 and setYearMask) ): year=years[0]
if(verb): print 'YYYYY55555',years,year,CL.ChkSource(year),chkoverride

#SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS -- make ad source object
#
if(not(CL.ChkSource(year)) and not(chkoverride)):

    # -- aliases come from here
    #
    # -- if cleaning pypdb -- use ptmp/source for adecks (usePtmpDir=doclean)
    #
    ttag='ad2.setAdeckSource: %s year: %s'%(source,year)
    MF.sTimer(ttag)
    
    (ad,aliases)=CL.setAdeckSource(source,year,dojettrack=dojettrack,dtgopt=dtgopt,dochk=dochk,
                                   useAdeckDir=useAdeckDir,
                                   ZIPoverride=ZIPoverride,
                                   usePtmpDir=doclean,
                                   yearMasks=yearMasks,
                                   useZipArchive=useZipArchive,
                                   verb=verb)

    if(ad == None):
        print """EEE don't know how to make AdeckSource class for: """,source
        sys.exit()
        
    getadecks=ad.getAdecks
    MF.dTimer(ttag)
    
    
else:
    # -- older style from AD vice ad2
    MF.sTimer('tcabse.GetAdmaskAdecks -- oldstyle source: %s year: %s'%(source,year))
    ad=None
    getadecks=GetAdmaskAdecks
    aliases=GetAdeckAliases(source)
    MF.dTimer('tcbase.GetAdmaskAdecks -- oldstyle source: %s year: %s'%(source,year))
    
#OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO -- set processing options
#
if(doclean):
    doadecks=1
    doputdss=1

if(phr != None or doListing or doacardout):
    doadecks=0
    doputdss=0
    update=0

if(phr != None and source != 'carq'):
    doVdeck=1

if(aidopt != None):  taids=aidopt.split(',')
else:                taids=None ;     #errAD('vdeckitaids')

if(ropt == 'norun'):
    print 'III will run: %s %s'%(CL.pypath,pyfileopt)
    sys.exit()

# -- set the source of pypdb files
#

dsbdir="%s/DSs"%(TcDataBdir)
dbtype='adeck'
    
# -- LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL -- ls
#
if(doListing or doacardout):

    # -- OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO - open DSs file
    #
    MF.sTimer('adk-openDss-dolisting-doacardout-year:%s'%(year))
    dbname="%s_%s_%s"%(dbtype,source,year)
    dbfile="%s.pypdb"%(dbname)
    backup=0
    chkifopen=0
    docleanOpen=0
    DSs=DataSets(bdir=dsbdir,name=dbfile,dtype=dbtype,verb=verb,backup=backup,unlink=docleanOpen,chkifopen=chkifopen)
    MF.dTimer('adk-openDss-dolisting-doacardout-year:%s'%(year))

if(doListing):

    lsopt='s'
    if(dolslong): lsopt='l'
    if(dolsfull): lsopt='f'

    (otaids,ostmids)=LsAidsStormsDss(DSs,tstmids,taids,dofilt9x=dofilt9x,lsopt=lsopt,dtgopt=dtgopt)

    if(dolsfull):
        lsBT=1
        BTs={}
        for tstmid in ostmids:
            try:
                taids=otaids[tstmid]
                print 'WWW(w2-tc-dss-adeck.py) no otaids for tstmid: ',tstmid
            except:
                continue
            for taid in taids:
                (AT,BT,aD)=GetAidBestTrksFromDss(DSs,taid,tstmid,verb=verb,warn=0)
                BTs[tstmid]=BT
                
        if(lsBT):
            btstmids=BTs.keys()
            btstmids.sort()

            for btstmid in btstmids:
                BT=BTs[btstmid]
                if(BT != None):
                    print
                    print 'BT for: ',btstmid
                    BT.lsBT()
                    
    MF.dTimer('all')
    sys.exit()

# -- CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC -- output adeck cards
#
elif(doacardout):
    
    tdir='/w3/rapb/fiorino/tc/tceps/%s'%(year)
    tdir='/lfs2/projects/fim/fiorino/w21/dat/tc/hfip/tier1/stream1.5/2012'
    tdir='/lfs2/projects/tcmt/tier1'
    # -- on kishou
    tdir='/w3/rapb/hfip/fim_tier1'
    tdir='/ptmp/fim9'

    if(aliasopt != None):
        tt=aliasopt.split(':')
        if(len(tt) == 2):
            (iname,oname)=(tt[0],tt[1])
        else:
            (iname,oname)=(None,None)

        if(iname != None):
            aliases=[(iname,oname)]
        else:
            aliases=None
    else:
        aliases=None

    # -- hfip processing -- make function of source
    dohfip=0
    dohfip2013=0
    dohfip2014=0
    
    if(source == 'rtfim_r4109'): dohfip2014=1
    if(source == 'rtfim_r3162_g9' or source == 'rtfim_r3162_g9hyb'): dohfip2013=1

    if(dohfip2013):
        tdir='/ptmp/hfip2013'
        aliases=[('fr3162g9hyb','fim9')]
        aliases=[('fr3162g9','fim9'),('fr3162g9hyb','fim9')]
        if(int(year) == 2013 and taids[0] == 'tfim9'):  aliases=[('tfim9','fim9')]
        hfipver='3162'
        dohfip=1
        
    if(dohfip2014):
        tdir='/ptmp/hfip2014'
        #aliases=[('tfim9','fim9')] - shouldn't be needed
        hfipver='4109'
        dohfip=1
        
    MF.ChkDir(tdir,'mk')
    
    AcardsFromAds(DSs,taids,tstmids,dtgopt=dtgopt,tdir=tdir,hfipver=hfipver,
                  aliases=aliases,dowrite=1,verb=verb,dohfip=dohfip,dofilt9x=dofilt9x,
                  override=override)


    MF.dTimer('all')
    sys.exit()

# -- zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz if using zip file the get adecks and put
#    scan the source dir for adecks and add/update to zip archive
#
doZipArchive=1
if(override): doZipArchive=0

if(ad != None and ad.dozip and doZipArchive and not(doclean) and not(setYearMask) ):
    ad.dozip=0
    ad.verb=verb
    MF.sTimer('adk-doZipArchiveOnly-ad.getAdecks')
    adecks=ad.getAdecks(override=override,dtgopt=dtgopt)
    ad.putAdecks(adecks,override=ZIPoverride)
    ad.dozip=1
    MF.dTimer('adk-doZipArchiveOnly-ad.getAdecks')

# -- if doing specific dtgs; always update, unless override
#

if(dtgopt != None):
    if(not(doListing or doacardout)):
        update=1
    if(override):
        update=0
    
# -- uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu update
#
if(update):

    # -- OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO - open DSs file

    MF.sTimer('update-curadps')
    if(ad != None and ad.dozip):
        adecks=ad.getAdecks(override=override,dtgopt=None)
    else:
        adecks=getadecks(source,year,dtgopt=dtgopt)

    curadps=AtcfAdeckPaths(adecks=adecks,dtgopt=None)
    MF.dTimer('update-curadps')

    # -- open DSs to get oldadps
    #
    MF.sTimer('adk-openDss-update-year: %s'%(year))
    dbname="%s_%s_%s"%(dbtype,source,year)
    dbfile="%s.pypdb"%(dbname)
    backup=0
    chkifopen=0
    docleanOpen=doclean
    if(doListing): docleanOpen=0
    DSs=DataSets(bdir=dsbdir,name=dbfile,dtype=dbtype,verb=verb,backup=backup,unlink=docleanOpen,chkifopen=chkifopen)
    MF.dTimer('adk-openDss-update-year: %s'%(year))

    # -- get old adps -- what is in the DSs
    #
    MF.sTimer('adk-oldadps')
    try:
        oldadps=DSs.getDataSet('adps').data
        oldkeys=DSs.getDataSet('keys').data
    except:
        print 'WWW(adk) -- no adps,keys in DSs'
        oldadps=None
        oldkeys=[]
    MF.dTimer('adk-oldadps')
    
    # -- close the DSs because it will be opened again in updateAds
    #
    DSs.closeDataSet()
    
    oldkeys.sort()
    

    # -- for nhc only check size -- wget mirror is dumb about getting time; 
    # -- nhc always resets the time in the file on their public ftp server
    # -- also use size only for ad2.sourcesDtg
    #
    MF.sTimer('update-newadps')
    sizeonly=0
    if(source == 'nhc' or source == 'ncep' or source == 'jtwc' or source == 'carq' or (source in CL.sourcesDtg)
       or source == 'fimens2012' or source == 'fim9hfip'): sizeonly=1

    # -- get new adecks
    #
    newadecks=getNewadecks(curadps,oldadps,sizeonly=sizeonly)

    skipcarq=1
    if(source == 'carq'): skipcarq=0

    # -- make new Adeck objects
    #
    (nads,stmids)=makeNewAdecksStmids(newadecks,year,aliases,skipcarq=skipcarq)

    # -- update Adecks
    #
    (oads,nads,DSsS)=updateAds(nads,source,verb=verb,docp1st=0)
    
    if(ropt != 'norun' and len(DSsS.keys()) > 0):
        updateDSs(nads,oldkeys,curadps,stmids,DSsS,DSsAdpsKeys=None,verb=1)
        
    # -- close the DSs...
    #
    for k in DSsS.keys():
        DSsS[k].closeDataSet()
        
    MF.dTimer('update-newadps')

    if(w2.onWjet):
        print 'FFF onWjet stop adeck update'
        sys.exit()

    # -- this can hang...only do if set on command line
    #
    if(doVdeck):

        if(dtgopt != None and len(stmids) == 0):
            tD=TcData(dtgopt=dtgs[-1])
            tstmids=tD.getStmidDtgs(dtgs)

        for stmid in stmids:
            if(taids == None or len(taids) == 0):
                print 'III(%s--doing vdeck: source: %s stmid: %s'%(pyfile,source,stmid) 
                cmd="w2.tc.dss.vdeck.py %s -S %s"%(source,stmid)
                MF.runcmd(cmd,ropt)
            else:
                for taid in taids:
                    print 'III(%s--doing vdeck: source: %s stmid: %s taid: %s'%(pyfile,source,stmid,taid) 
                    cmd="w2.tc.dss.vdeck.py %s -S %s -T %s"%(source,stmid,taid)
                    MF.runcmd(cmd,ropt)
                    

    # -- rsync under update
    #
    if(dorsync2kaze and not(w2.onKaze) and len(nads)> 0):
        rc=doRsyncDSS2Kaze()

    if(w2.onKaze and doRsync2Kishou and len(nads) > 0):
        
        sfile="%s/%s"%('w21/dat/tc/DSs',dbfile)
        doRsyncK2K(sfile,ropt=ropt,reverse=1)
        
        for year in yearsAll:
            dbname="%s_%s_%s"%(dbtype,source,year)
            dbfile="%s.pypdb"%(dbname)
            sfile="%s/%s"%('w21/dat/tc/DSs',dbfile)
            MF.sTimer('adk-doRsyncK2K-%s'%(year))
            doRsyncK2K(sfile,ropt=ropt,reverse=1)
            MF.dTimer('adk-doRsyncK2K-%s'%(year))
                
    sys.exit()


            
# -- +++++++++++++++++++++++++++++++++ phr bias corr -- make 'I' and '2' trackers
#
if(phr != None):

    # -- OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO - open DSs file
    MF.sTimer('adk-openDss-phr')
    dbname="%s_%s_%s"%(dbtype,source,year)
    dbfile="%s.pypdb"%(dbname)
    backup=0
    chkifopen=0
    docleanOpen=0
    DSs=DataSets(bdir=dsbdir,name=dbfile,dtype=dbtype,verb=verb,backup=backup,unlink=docleanOpen,chkifopen=chkifopen,doDSsWrite=1)
    MF.dTimer('adk-openDss-phr')

    dbname='mdecks'
    dbfile="%s.pypdb"%(dbname)
    mDSs=DataSets(bdir=dsbdir,name=dbfile,dtype=dbname,verb=verb)
    mD=mDSs.getDataSet(key=year).md

    ads={}
    adps=None
    for taid in taids:
        for tstmid in tstmids:

            acards={}
 
            dtx=3
            model=taid
            stm3id=tstmid.split('.')[0]
            aP=AidProp(model)
            
            omodel="%s%02d"%(model,phr)
            otaids=[omodel]

            (AT,BT,aD)=GetAidBestTrksFromDss(DSs,taid,tstmid,verb=verb,warn=1)
            if( not(hasattr(AT,'dtgs')) or len(AT.dtgs) == 0 ): 
                print 'WWW phr != None, do AT from GetAidBestTrksFromDss for tstmid: ',tstmid,' taid: ',taid
                continue
            dtgs=AT.dtgs

            for dtg in dtgs:
                btdtg=mf.dtginc(dtg,phr)
                (btlat,btlon,btdir,btspd,bvmax)=BT.selectBestBtCqTau0(btdtg,verb=verb)
                if(btlat == None): continue
                itrk=AT.atrks[dtg]
                (jtrk,jtaus)=aD.FcTrackInterpFill(itrk,npass=10,dovmaxSmth=0)
                otrk=aD.BiasCorrFcTrackInterpFill(jtrk,itrk,jtaus,phr,dtx,
                                                  btlat,btlon,btdir,btspd,bvmax,
                                                  model,dtg,stm3id,
                                                  vmaxCorrScheme=aP.vmaxCorrScheme,
                                                  dopc=1,vmaxmin=20.0,verb=verb)

                
                acards[btdtg]=MakeAdeckCards(omodel,btdtg,otrk,tstmid,verb=verb)

            if(len(acards) > 0):
                adkey="%s_%s"%(omodel,tstmid)
                ad=makeAdeckByCards(mD,acards,dofilt9x=dofilt9x)
                ads[adkey]=ad[0]
                DSs.putDataSet(ad[0],adkey,verb=1)
            

    if(len(ads.keys()) > 0):
        PutDsDictKeys2DataSets(ads,DSs)

    doadecks=0
    doputdss=0

# -- AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA make adecks
#
if(doadecks):

    MF.sTimer('adk-doadecks-ALL')
    gotzipadecks=0
    if(ad != None and ad.dozip):
        #ad.verb=1
        MF.sTimer('adk-doadecks-getadecks')
        adecks=ad.getAdecks(override=override,dtgopt=dtgopt)
        MF.dTimer('adk-doadecks-getadecks')
        gotzipadecks=1
    else:
        adecks=getadecks(source,year,tstmids=tstmids,dtgopt=dtgopt)


    if(len(adecks) == 0):
        if(gotzipadecks):
            print 'EEE(dozip=1) no adecks for source: ',source,' year: ',year
        else:
            print 'EEE no adecks for source: ',source,' year: ',year,'tstmids: ',tstmids
            print 'maybe need -J option for jetsource?'

    MF.sTimer('adk-AtcfAdeckPath')
    adps=AtcfAdeckPaths(adecks=adecks)
    MF.dTimer('adk-AtcfAdeckPath')

    MF.sTimer('adk-MakeAdecksByYear')

    skipcarq=1
    if(source == 'carq'): skipcarq=0
    if(mf.find(source,'cfsrr')):
        ads=MakeAdecksByYear(adps,year,aliases=aliases,skipcarq=skipcarq,fixmd2=1)
    else:
        ads=MakeAdecksByYear(adps,year,aliases=aliases,skipcarq=skipcarq,
                             yearMasks=yearMasks,
                             dofilt9x=dofilt9x,
                             verb=verb)
    
    MF.dTimer('adk-MakeAdecksByYear')

    MF.dTimer('adk-doadecks-ALL')

# -- PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP put to pyp
#
if(doputdss):

    MF.sTimer('adk-putdss')
    DSsS=PutAdecks2DataSets(ads,adps,source,doclean=doclean,verb=1)
    tstmids=None
    taids=None
    (aids,stmids)=GetAidsStormsFromDsss(DSsS,taids,tstmids)

    for aid in aids:
        for stmid in stmids:
            print 'aid: ',aid,' stmid: ',stmid

    MF.dTimer('adk-putdss')


# -- VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV  do vdeck
#
if(doVdeck):

    overopt=''
    modelopt=''
    if(override): overopt='-O'
    if('omodel' in locals().keys()):
        modelopt='-T %s'%(omodel)

    if(dtgopt != None):
        tD=TcData(dtgopt=dtgs[-1])
        tstmids=tD.getStmidDtgs(dtgs)
        
    print 'III(%s--doing vdeck: %s %s'%(pyfile,source,modelopt)
    if(tstmids == None): tstmids=[]
    
    for stmid in tstmids:
        cmd="w2.tc.dss.vdeck.py %s -S %s %s %s"%(source,stmid,modelopt,overopt)
        MF.runcmd(cmd,ropt)



# -- rsyncs after doing adecks
#
if(dorsync2kaze and not(w2.onKaze)):
    rc=doRsyncDSS2Kaze()

if(w2.onKaze and doRsync2Kishou):

    for year in yearsAll:
        dbname="%s_%s_%s"%(dbtype,source,year)
        dbfile="%s.pypdb"%(dbname)
        sfile="%s/%s"%('w21/dat/tc/DSs',dbfile)
        MF.sTimer('adk-doRsyncK2K-%s'%(year))
        doRsyncK2K(sfile,ropt=ropt,reverse=1)
        MF.dTimer('adk-doRsyncK2K-%s'%(year))


MF.dTimer('all')

sys.exit()
