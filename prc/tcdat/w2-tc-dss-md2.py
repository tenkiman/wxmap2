#!/usr/bin/env python

# -- new tc module with everything needed...
#
from tcbase import *

def getDbname(md2tag,year,doNEWDSsS=1,doBdeck2=0):
    
    if(md2tag != None):
        if(doBdeck2):
            dbname='mdecks2BD2-%s'%(md2tag)
        else:
            dbname='mdecks2-%s'%(md2tag)
    else:
        if(doNEWDSsS):
            if(doBdeck2):
                dbname="mdecksBD2-%s"%(year)
            else:
                dbname="mdecks2-%s"%(year)
        else:
            dbname=Md2Dbname
            
    return(dbname)

def uniqZipTstmids(tstmids,warn=0,verb=0):
    
    for tstmid in tstmids:

        # -- 9999999999999999 -- only for 9x!!!
        #
        if(not(Is9X(tstmid))):
            if(warn): print 'only do uniq for 9X...press...'
            continue
            
        (snum,b2id,byear,abdir,bbdir,
         adarchdir,adarchzippath,aduniqzippath,
         bdarchdir,bdarchzippath,bduniqzippath,
         adcurpath,bdcurpath)=getABsDirsPaths(tstmid,chkNhcJtwcAdeck=chkNhcJtwcAdeck)

        MF.sTimer('zip-%s'%(tstmid))

        if(verb):
            print 'AAAiiiiii ',adarchzippath
            print 'AAAuuuuuu ',aduniqzippath
            print 'AAAcccccc ',adcurpath
            
            print 'BBBiiiiii ',bdarchzippath
            print 'BBBuuuuuu ',bduniqzippath
            print 'BBBcccccc ',bdcurpath


        # -- adeck archive
        #
        try:
            AZ=zipfile.ZipFile(adarchzippath)
        except:
            AZ=None

        if(AZ != None):
            AZu=zipfile.ZipFile(aduniqzippath,'w')
            (uniqfiles,uniqcards)=getuniqdecks(AZ,verb=verb)
            for (ufile,usiz) in uniqfiles:
                ocards=uniqcards[ufile]
                tt=AZ.extract(ufile)
                MF.WriteString2Path(ocards,tt)
                AZu.write(tt,ufile,zipfile.ZIP_DEFLATED)
                
                # -- ufile is a temp file that's put in the archive; rm
                os.unlink(ufile)
            AZu.close()
        
        # -- bdeck archive
        #
        try:
            BZ=zipfile.ZipFile(bdarchzippath)
        except:
            BZ=None
            
        if(BZ != None):
            BZu=zipfile.ZipFile(bduniqzippath,'w')
            (uniqfiles,uniqcards)=getuniqdecks(BZ,verb=verb)
            for (ufile,usiz) in uniqfiles:
                ocards=uniqcards[ufile]
                tt=BZ.extract(ufile)
                
                MF.WriteString2Path(ocards,tt)
                BZu.write(tt,ufile,zipfile.ZIP_DEFLATED)
                # -- ufile is a temp file that's put in the archive; rm
                os.unlink(ufile)
            BZu.close()
        MF.dTimer('zip-%s'%(tstmid))

    return

def updateABdeckZipArchive(tstmids,verb=0):
    
    for tstmid in tstmids:
        (snum,b1id,year,b2id,stm2id,stm1id)=getStmParams(tstmid)
        if(IsNhcBasin(b1id)):
            adsdir="%s/%s"%(w2.TcAdecksNhcDir,year)
            bdsdir="%s/%s"%(w2.TcBdecksNhcDir,year)
            
        else:
            adsdir="%s/%s"%(w2.TcAdecksJtwcDir,year)
            bdsdir="%s/%s"%(w2.TcBdecksJtwcDir,year)
        
        adeckfile="a%s%s%s.dat"%(b2id.lower(),snum,year)    
        adeckpath="%s/%s"%(adsdir,adeckfile)
        
        bdeckfile="b%s%s%s.dat"%(b2id.lower(),snum,year)
        bdeckpath="%s/%s"%(bdsdir,bdeckfile)
        
        asiz=MF.getPathSiz(adeckpath)
        bsiz=MF.getPathSiz(bdeckpath)

        adsdirZip="%s/archive"%(adsdir)
        bdsdirZip="%s/archive"%(bdsdir)
        mf.ChkDir(adsdirZip,'mk')
        mf.ChkDir(bdsdirZip,'mk')
        adeckpathZip="%s/%s.zip"%(adsdirZip,adeckfile)
        bdeckpathZip="%s/%s.zip"%(bdsdirZip,bdeckfile)
        
        asizZip=MF.getPathSiz(adeckpathZip)
        bsizZip=MF.getPathSiz(bdeckpathZip)
        
        # -- 20220528 -- check if asiz is -999
        #
        if(asiz == -999):
            print '!!!!!!!!!!!!!!!!!!!!'
            print 'missing adeck for: ',tstmid
            print '!!!!!!!!!!!!!!!!!!!!'
        else:
            rc=addFile2ZipArchive(adeckpath,adeckpathZip,forceAdd=0,verb=verb)
            
            
        #print 'aaabbb',adeckpath,bdeckpath,'sss',asiz,bsiz
        #print 'aaazzz',adeckpathZip,bdeckpathZip,'sss',asizZip,bsizZip
        
        rc=addFile2ZipArchive(bdeckpath,bdeckpathZip,forceAdd=0,verb=verb)
     
        
        
    


class MdeckCmdLine(CmdLine):

    basins=['l','e','c','w','i','s','q']

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv

        self.argv=argv

        self.argopts={
            #1:['year',    'no default'],
            }

        self.defaults={
            'lsopt':'s',
            'comp9XCC':1,  # turn on comps to CC from NCDC and 9X
            }

        self.options={
            'md2tag':          ['t:',None,'a','postfix tag for pypdb'],
            'override':        ['O',0,1,'override'],
            'doPrevYear':      ['P',1,0,'do NOT check for crossover storms from previous year'],
            'verb':            ['V',0,1,'verb=1 is verbose'],
            'ropt':            ['N','','norun',' norun is norun'],
            'douniq':          ['U',0,1,'0 - uniq the a/bdecks in the archive/*.zip files'],
            'dozip9x':         ['Z',0,1,'0 - use uniq.zip a/bdecks in the archive/*.zip files'],
            'dostmstats':      ['s',1,0,'0 - DO NOT stmstats'],
            'stmopt':          ['S:',None,'a','stmopt'],
            'update':          ['u',0,1,'only update mdeck'],
            'updateYear':      ['Y',0,1,'update entire year (all basins)'],
            'yearopt':         ['y:',None,'a','yearopt yyyy,yyyy'],
            'basinopt':        ['b:',None,'a','basin opt in 1char form,r'],
            'doclean':         ['K',0,1,"""blow away .pypdb file because shelf created with 'c' option """],
            'dokeys':          ['k',0,1,"""set keysin DSs """],
            'doPutDSs':        ['p',1,0,'do NOT put DSs,e.g., testing'],

            'doNEWDSsS':       ['n',1,0,'do NOT make by year for new cache in md2.anl.py'],
            'useNhcArchive':   ['H',0,1,'use NHC archive in /dat/tc/nhc/archive vice real-time year'],
            'doWorkingBT':     ['W',0,1,'using working/b*.dat for bdecks vice ./b*.dat'],
            'chkNhcJtwcAdeck': ['J',0,1,'chk JTWC abdecks if in epac/lant'],

            'doBdeck2':        ['2',0,1,'use bdeck in bdeck2/ vice bdeck/'],
            }

        self.purpose='''

parse mdecks create TC data shelves
special cases:
20220816 -- jt did not clean out previous awp932022.dat
20220611 -- nhc gooned up bep922022
20220528 -- always run adeck check for special cases in getABsDirsPaths
            'AAA---III special case of NHC no adeck and JTWC has the adeck'
20200923 -- 90L.2020? a/bdeck in archive is from 23l 9X really is C8L.2020'''

        self.examples='''
%s -y cur -Y -b s,w
%s -y 2010.2012 -Y -b l
%s -y 2010,2011,2012 -Y -b l # same as above
%s -u
'''



def errMD(option,opt=None):

    if(option == 'tstmids'):
        print 'EEE # of tstmids = 0 :: no stms to md2...stmopt: ',stmopt
    elif(option == 'tstms'):
        print 'EEE # of tstms from stmopt: ',stmopt,' = 0 :: no stms to md2...'
    elif(option == 'stmopt'):
        print 'EEE must specify -y year when doing -S stmopt'
    else:
        print 'Stopping in errAD: ',option

    sys.exit()




    
#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# -- main
#

MF.sTimer('all')

CL=MdeckCmdLine(argv=sys.argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

if(stmopt != None and yearopt == None and basinopt == None and md2tag == None):
    rc=errMD('stmopt')

# -- get verb for DSsPut

verbDSsPut=0

# -- get years

gotcurYear=0
ostmidsYearm1=[]
syearM1=None

if(yearopt == 'cur' or yearopt == 'ops' or yearopt == None):
    year=curyear
    mm=curdtg[4:6]
    shemyear=getShemYear(curdtg)
    if(shemyear != year):
        years=[year,shemyear]
        
    elif(curyear == year and (int(mm) == 1) and doPrevYear):
        syearCur=int(curyear)
        otcs=findtcs(curdtg,verb=verb)
        for otc in otcs:
            ostmid=otc.split()[1]
            rc=getStmParams(ostmid)
            syear=int(rc[2])
            if(syear < syearCur):
                syearM1=syear
                ostmidsYearm1.append(ostmid)
                
        if(len(ostmidsYearm1) > 0):  
            gotcurYear=-1
            years=[syearM1]
        else:
            gotcurYear=1
            years=[year]
    else:
        years=[year]
        gotcurYear=1
    
elif(yearopt != None):
    years=yearopt.split(',')
    
    if(mf.find(yearopt,'.')):
        yy=yearopt.split('.')
        byear=yy[0]
        eyear=yy[-1]
        years=mf.yyyyrange(byear,eyear)
        
    if(curyear in years): gotcurYear=1

# -- set up DSs file
#
md2tagopt=''
if(md2tag != None):   md2tagopt='-t %s'%(md2tag)
elif(doNEWDSsS and len(years) == 1): md2tag=years[0]

dsbdir="%s/DSs"%(TcDataBdir)

if(doWorkingBT and md2tag != None and md2tag[-2:] != '-W'): md2tag="%s-W"%(md2tag)
dbname=getDbname(md2tag,years[0],doNEWDSsS=doNEWDSsS,doBdeck2=doBdeck2)
    
backup=0
dbfile="%s.pypdb"%(dbname)

jtOpt=''
if(chkNhcJtwcAdeck): jtOpt='-J'


# -- update all for years
#
if(updateYear):

    for year in years:
        
        MF.sTimer('UUUpdateYear-%s'%(year))
        
        if(len(year) != 4):
            print 'EEE year not 4 digit...press...'
            continue


        iyear=int(year)

        # -- if year >= 2010 use zip archives for 9x;
        #    otherwise tcVM.get9xABnew will select either NRL or NHC store_invest
        dozip9x=0
        if(iyear >= 2010): dozip9x=1
        
        do9x=0
        if(iyear >= 1998): do9x=1
        
        if(basinopt == None):  ibasins=CL.basins
        else:                  ibasins=basinopt.split(',')

        md2tag=year
        if(doWorkingBT): md2tag="%s-W"%(md2tag)
        md2tagopt="-t %s"%(md2tag)

        wBTopt=''
        if(doWorkingBT): wBTopt='-W'
        
        # -- doclean here, AFTER md2tag set
        #
        if(doclean and not(ropt == 'norun')):

            dbname=getDbname(md2tag,year,doNEWDSsS=doNEWDSsS,doBdeck2=doBdeck2)
            dbfile="%s.pypdb"%(dbname)
            DSsKill=DataSets(bdir=dsbdir,name=dbfile,dtype=dbname,verb=verb,backup=backup,unlink=doclean,doDSsWrite=0)
            DSsKill.closeDataSet()
            del DSsKill
        
        for basin in ibasins:

            donhcarch=''
            idozip9x=dozip9x
            if(IsNhcBasin(basin) and useNhcArchive):
                idozip9x=0
                donhcarch='-H'
            
            bcmd="%s -y %s"%(CL.pypath,iyear)

            dozipopt=''
            if(idozip9x):  dozipopt='-Z'
            dobd2opt=''
            if(doBdeck2): dobd2opt='-2'
            dobd2opt9X=''
            
            if(idozip9x and not(doWorkingBT) and douniq == 0):
                # -- always do uniq if yearly
                cmd="%s -S 9x%s.%d %s -U %s %s "%(bcmd,basin,iyear,md2tagopt,dobd2opt9X,jtOpt)
                mf.runcmd(cmd,ropt)   
                
            if(do9x):
                cmd="%s -S 9x%s.%d %s %s %s %s %s"%(bcmd,basin,iyear,md2tagopt,
                                                 dozipopt,donhcarch,dobd2opt9X,jtOpt)
                mf.runcmd(cmd,ropt)


            cmd="%s -S %s.%d %s %s %s %s %s"%(bcmd,basin,iyear,md2tagopt,
                                              donhcarch,wBTopt,dobd2opt,jtOpt)
            mf.runcmd(cmd,ropt)
            

        MF.dTimer('UUUpdateYear-%s'%(year))

    sys.exit()


# -- since md2 always puts, set this to 1 always
#
doDSsWrite=0
if(doPutDSs): doDSsWrite=1

if(doclean and not(ropt == 'norun')):
    DSsKill=DataSets(bdir=dsbdir,name=dbfile,dtype=dbname,verb=verb,backup=backup,unlink=doclean,doDSsWrite=0)
    DSsKill.closeDataSet()
    del DSsKill
    doclean=0


#-- ooooooooooooooooooooooooooooooo open datasets -- only if years == 1; when update > jul 1
#
if(len(years) == 1 and not(ropt == 'norun') and not(gotcurYear == -1)):
    
    DSs=DataSets(bdir=dsbdir,name=dbfile,dtype=dbname,verb=verb,backup=backup,unlink=doclean,doDSsWrite=doDSsWrite)
    initDSsMD2Keys(DSs,override=override)

    if(dokeys):
        setDSsMD2Keys(DSs)
        sys.exit()
        


tstmids=None
dofilt9x=0

# -- UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU uniq 9X 
#
if(douniq):

    if(stmopt != None and tstmids == None): tstmids=MakeStmList(stmopt,verb=verb,dofilt9x=dofilt9x)
    rc=uniqZipTstmids(tstmids,verb=verb)
    sys.exit()


# -- uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu update
#
if(update):

    # -- how to handle  two season years > 1 jul
    #
        
    overOpt=''
    if(override): overOpt='-O'
    
    if(len(years) > 1):
        if(not(gotcurYear == -1)):
            verbopt=''
            if(verb): verbopt='-V'
            syncOpt=''
            for year in years:
                cmd="%s -u -y %s -t %s %s %s %s %s"%(CL.pypath,year,year,verbopt,
                                                     syncOpt,jtOpt,overOpt)
                mf.runcmd(cmd,ropt)
            sys.exit()

    # -- crossover storms from previous year using mdeck.findtcs()
    #
    if(gotcurYear == -1):

        verbopt=''
        if(verb): verbopt='-V'
        
        rsyncOpt=''

        for ostmid in ostmidsYearm1:
            'III---III--- updating storm: ',ostmid,' from previous year!!!'
            cmd="%s -S %s -y %s %s %s %s -P"%(CL.pypath,ostmid,syearM1,verbopt,rsyncOpt,jtOpt)
            mf.runcmd(cmd,ropt)
            
        cmd="%s -u %s %s %s %s -P"%(CL.pypath,verbopt,rsyncOpt,jtOpt,overOpt)
        mf.runcmd(cmd,ropt)
        sys.exit()
        
        
    if(ropt == 'norun'): sys.exit()
        
    MF.sTimer('abdecks')
    abD=DSs.getDataSet(key='abdecks',verb=verbDSsPut)
    if(abD == None or override):
        print 'abD not there, make...'
        abD=MDpaths(verb=verb)
    abDcur=MDpaths(verb=verb)
    
    (tstmids,ctoffs)=abDcur.getCurStmids(abD,years[0],override=override,verb=verb)
    
    # -- always put the file state 
    if(ropt != 'norun' and doPutDSs): 
        rc=DSs.putDataSet(abDcur,key='abdecks',verb=verbDSsPut)
        if(rc == -1):
            print 'EEEE(md2.putDataSet(abdecks)'
    MF.dTimer('abdecks')

    if(len(tstmids) == 0):
        print 'UUU no stmids to update...'
        DSs.closeDataSet()
        sys.exit()

    print "III will update: "
    for tstmid in tstmids:
        print tstmid,' ctoff: %+5.1f h'%(ctoffs[tstmid])
        
    # -- update Zip Archives
    #
    rc=updateABdeckZipArchive(tstmids,verb=verb)
        
    if(ropt == 'norun'):
        print 'NNN will not update just showing what will happen...'
        sys.exit()

    # -- do uniq to absolutely sure we have the latest in the uniq.zip
    #
    rc=uniqZipTstmids(tstmids,verb=verb)

else:

    # -- get the stmids
    #

    if(stmopt == None):
        if(yearopt != None):
            tstmids=MakeStmListABdecks(stmopt,yearopt=yearopt,verb=verb,dofilt9x=dofilt9x)
        else:
            print 'EEE set either stmopt or yearopt...'; sys.exit()

    else:
        dofilt9x=1
        if(stmopt[0:2] == '9x'):
            stmopt=stmopt.replace('9x','90-99')

        if(mf.find(stmopt.split('.')[0],'9') or (stmopt[0].isalpha()) ):  dofilt9x=0
        
        tstmids=MakeStmListABdecks(stmopt,verb=verb,dofilt9x=dofilt9x)

        if(tstmids == None): 
            print 'WWW(md2) -- tstmids == None -- using MakeStmList vice MakeStmListABdecks'
            tstmids=MakeStmList(stmopt,verb=0,dofilt9x=dofilt9x)
        

if(tstmids == None): 
    print'WWW(md2): tstmids=None'
    pass
elif(len(tstmids) == 0): 
    errMD('tstmids')

if(ropt == 'norun'): 
    print 'bailing because ropt == norun'
    sys.exit()


# -- ssssssssssssssssssssssssssssssssssssssssssssssssss always do the storm tables from jtwc/nhc
#
MF.sTimer('storms')
stmD=StormData(verb=0)
if(doPutDSs and ropt != 'norun'): DSs.putDataSet(stmD,key='storms',verb=verbDSsPut)
MF.dTimer('storms')

def do9X(bdtg,n):

    ostm2id=bd.stm2id.replace('.','%s.'%(chr(icharA+n)))
    ostm2id=bd.stm2id
    newid=chr(icharA+n).upper()
    ostm2id=ostm2id[0:2]+newid+ostm2id[3:]
    ostm2id=ostm2id.lower()

    MF.sTimer('9X-%s'%(ostm2id))

    adtgs=bd.mD.uniqStmdtgs[bdtg]
    adtgb=adtgs[0]
    adtge=adtgs[-1]
    smD=bd.getMDByDtgs(adtgs,ostm2id)
    #smD.ls()
    smD.setMDtrk(verb=verb)
    smD.cleanMD()
    if(verb): smD.lsMDtrk()

    odtgs=smD.trk.keys()
    odtgs.sort()

    ostm2ids.append(ostm2id)
    odtgss[ostm2id]=odtgs
    smDs[ostm2id]=smD
    tstm2ids[ostm2id]=bd.stm2id

    if(doPutDSs): putDssSmdDataSet(DSs,smD,ostm2id,verb=verbDSsPut)

    MF.dTimer('9X-%s'%(ostm2id))


# -- tttttttttttttttttttttttttttttttttttttttttttttttttt main tstmids loop
#

for tstmid in tstmids:

    # -- get paths............................
    #
    (snum,b2id,byear,abdir,bbdir,
     adarchdir,adarchzippath,aduniqzippath,
     bdarchdir,bdarchzippath,bduniqzippath,
     adcurpath,bdcurpath)=getABsDirsPaths(tstmid,
                                          doBdeck2=doBdeck2,
                                          useNhcArchive=useNhcArchive,
                                          chkNhcJtwcAdeck=chkNhcJtwcAdeck,
                                          doWorkingBT=doWorkingBT,verb=verb)
    

    # -- 99999999999999999999999999999999XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    #
    abcardsZip={}
    doABcardsByFile=1
    
    if(int(snum) >= 90):
        # -- !!!!!!!!!!!!! very important
        if(update): dozip9x=1
        if(dozip9x):
            (abcards,abcardsZip)=get9xABuniq(aduniqzippath,bduniqzippath,verb=verb)
        else:
            abcards=get9xABnew(abdir,bbdir,b2id,snum,byear,useNhcArchive=useNhcArchive,verb=verb)

        #print 'b2id,snum,byear',b2id,snum,byear,len(abcardsZip)
        
        # -- 20211220 -- bug in aio942021.dat from JT -- b9i includes cards from a9i
        #
        if(b2id == 'io' and snum == '94' and byear == '2021' and len(abcardsZip) == 2):
            abZcorr=''
            abZ=abcardsZip[1].split('\n')
            for ab in abZ:
                tt=ab.split()
                if(len(tt) > 2 and tt[2][0:6] == '202106'):
                    print 'skipping...',ab
                else:
                    abZcorr=abZcorr+ab+'\n'
                    
            print abZcorr
            abcardsZip[1]=abZcorr
            
        ## -- 20220816 -- bug in awp232022.dat from JT -- includes previous 
        ##
        #if(b2id == 'wp' and snum == '93' and byear == '2022' and len(abcardsZip) == 4):
            #abZcorr=''
            #abZ=abcardsZip[1].split('\n')
            #for ab in abZ:
                #tt=ab.split()
                #if(len(tt) > 2 and tt[2][0:6] == '202207'):
                    #print 'skipping...',ab
                #else:
                    #abZcorr=abZcorr+ab+'\n'
                    
            #print abZcorr
            #abcardsZip[1]=abZcorr
            
            
            
    # -- NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN       
    #
    else:
        
        if(not(useNhcArchive) or not(IsNhcBasin(b2id))):
            abcards=''  
            acards=MF.ReadFile2String(adcurpath)
            bcards=MF.ReadFile2String(bdcurpath)
            abcards=abcards+acards+bcards
            
        elif(useNhcArchive and IsNhcBasin(b2id)):
            abcards=get9xABnew(abdir,bbdir,b2id,snum,byear,useNhcArchive=useNhcArchive,verb=verb)

    if(len(abcards) == 0): 
        print 'WWW for tstmid: ',tstmid,'no abcards...press...'
        continue

    # -- MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM make the mdeck
    #
    ostm2ids=[]
    odtgss={}
    odtgsBTs={}
    smDs={}
    smDBTs={}
    tstm2ids={}

    nZs=abcardsZip.keys()
    nZ=len(nZs)
    
    if(nZ > 0 and doABcardsByFile):
        #print 'do mdeck by individual files'
        for n in range(0,nZ):
            abcards=abcardsZip[n]
            bd=MDdeck(abcards,b2id,snum,byear)
            bd.getDtgRangeNN(bd.mD,nhours=48,verb=verb)
            bdtgs=bd.mD.uniqStmdtgs.keys()
            bdtgs.sort()
            rc=do9X(bdtgs[0],n)
            didByFile=1
        
    else:

        bd=MDdeck(abcards,b2id,snum,byear)
        bd.getDtgRangeNN(bd.mD,nhours=48,verb=verb)
        bdtgs=bd.mD.uniqStmdtgs.keys()
        bdtgs.sort()
        didByFile=0
    
    if(len(bdtgs) >= 1 and int(snum) >= 90 and not(didByFile)):

        for n in range(0,len(bdtgs)):

            bdtg=bdtgs[n]
            ostm2id=bd.stm2id.replace('.','%s.'%(chr(icharA+n)))
            ostm2id=bd.stm2id
            newid=chr(icharA+n).upper()
            ostm2id=ostm2id[0:2]+newid+ostm2id[3:]
            ostm2id=ostm2id.lower()

            MF.sTimer('9X-%s'%(ostm2id))

            adtgs=bd.mD.uniqStmdtgs[bdtg]
            adtgb=adtgs[0]
            adtge=adtgs[-1]
            smD=bd.getMDByDtgs(adtgs,ostm2id)
            #smD.ls()
            smD.setMDtrk(verb=verb)
            smD.cleanMD()
            if(verb): smD.lsMDtrk()

            odtgs=smD.trk.keys()
            odtgs.sort()

            ostm2ids.append(ostm2id)
            odtgss[ostm2id]=odtgs
            smDs[ostm2id]=smD
            tstm2ids[ostm2id]=bd.stm2id

            if(doPutDSs): putDssSmdDataSet(DSs,smD,ostm2id,verb=verbDSsPut)

            MF.dTimer('9X-%s'%(ostm2id))

    elif(len(bdtgs) >= 1 and int(snum) <= maxNNnum):

        ostm2id=bd.stm2id.lower()
        ostm2idBT="%s.bt"%(ostm2id)

        # -- case for dtg breaks in bdeck
        #
        bd.mD.dtgs=bd.mD.uniqStmdtgs[bdtgs[-1]]
        smD=bd.mD
        smDBT=copy.deepcopy(bd.mD)

        smD.setMDtrk(verb=verb)
        if(verb): smD.lsMDtrk()

        odtgs=smD.trk.keys()
        odtgs.sort()
        odtgss[ostm2id]=odtgs

        # -- clean and put to pypdb
        smD.cleanMD()
        if(doPutDSs): putDssSmdDataSet(DSs,smD,ostm2id,verb=verbDSsPut)


        # -- btonly bbbbbbbbbbbbbbbbbbb
        #
        smDBT.setMDtrk(verb=verb,docq00=0,btonly=1)
        if(verb): smDBT.lsMDtrk()

        odtgsBT=smDBT.trk.keys()
        odtgsBT.sort()
        odtgsBTs[ostm2id]=odtgsBT

        ostm2ids.append(ostm2id)
        smDs[ostm2id]=smD
        tstm2ids[ostm2id]=bd.stm2id

        # -- put BT to pypdb
        #
        smDBT.cleanMD()
        if(doPutDSs): putDssSmdDataSet(DSs,smDBT,ostm2idBT,verb=verbDSsPut)
        smDBTs[ostm2id]=smDBT


    # -- dtgs -- carq
    #
    for ostm2id in ostm2ids:
        tstm2id=tstm2ids[ostm2id]
        for odtg in odtgss[ostm2id]:
            smD=smDs[ostm2id]
            dds=DSs.getDataSet(key=odtg,verb=verbDSsPut)
            if(dds == None): 
                dds=MDdtgs(odtg)
            dds.loadDtg(ostm2id,tstm2id,smD,odtg)
            if(doPutDSs): putDssDtgDataSet(DSs,dds,odtg,verb=verbDSsPut)
            if(verb): dds.lsDtgTrk(odtg)
            #dds.lsDtgTrk(odtg)


    # -- dtgs -- bt
    #
    for ostm2id in ostm2ids:
        tstm2id=tstm2ids[ostm2id]

        try:    odtgs=odtgsBTs[ostm2id]
        except: continue

        for odtg in odtgs:
            smDBT=smDBTs[ostm2id]
            keyBT=odtg+'.bt'
            ddsBT=DSs.getDataSet(key=keyBT,verb=verbDSsPut)
            if(ddsBT == None): 
                ddsBT=MDdtgs(odtg)
            ddsBT.loadDtg(ostm2id,tstm2id,smDBT,odtg)
            if(doPutDSs): putDssDtgBTDataSet(DSs,ddsBT,keyBT,verb=verbDSsPut)
            if(verb): ddsBT.lsDtgTrk(odtg)

    # -- analyze for TC properties, including genesis
    #
    for ostm2id in smDBTs.keys():
        smDBT=smDBTs[ostm2id]
        mT=MD2trk(smDBT,DSs,doPutDSs=doPutDSs)
        mT.anlMDtrk(stmD=stmD,verb=verb,comp9XCC=comp9XCC)
        mT.loadMDdtg()
        ostm2idBT="%s.bt"%(ostm2id)
        if(doPutDSs): DSs.putDataSet(smDBT,key=ostm2idBT,verb=verbDSsPut)

    # -- analyze for TC properties, including genesis
    #
    for ostm2id in smDs.keys():

        # -- why do we redo? because we want separate summary stats for .bt and non .bt
        smD=smDs[ostm2id]
        mT=MD2trk(smD,DSs,dobt=0,doPutDSs=doPutDSs)
        mT.anlMDtrk(stmD=stmD,verb=verb,comp9XCC=comp9XCC)
        mT.loadMDdtg()
        if(doPutDSs): DSs.putDataSet(smD,key=ostm2id,verb=verbDSsPut)

# --- put keys dataset to DSs
#
if(doPutDSs): 
    putDSsMD2Keys(DSs,verb=verbDSsPut)
    DSs.closeDataSet(verb=verbDSsPut)

MF.dTimer('all')

    
