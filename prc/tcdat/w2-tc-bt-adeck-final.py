#!/usr/bin/env python

from WxMAP2 import *
w2=W2()

from tcbase import *
import ATCF

#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# command line setup
#
class RsyncCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv
        
        self.argv=argv
        self.argopts={
            1:['yyyy',    'tyear -- must set '],
            }

        self.defaults={
            'dosizecheck':0,
            'dodupchk':0,
            }

        self.options={
            'popt':             ['p:',None,'a','[clean.all]'],
            'vopt':             ['v:',None,'a','source opt'],
            'do9Xstms':         ['9',0,1,'do9Xstms=1'],
            'verb':             ['V',0,1,'verb=1 is verbose'],
            'ropt':             ['N','','norun',' norun is norun'],
            'writelog':         ['W',0,1,'verb=1 is verbose'],
            'doLn':             ['L',1,0,"""do NOT use 'ln -s' use 'cp' instead for filesystem independence"""],
            }

        self.purpose='''
grep out CARQ/JTWC/OFCL from adeck (no -p) and set local to final AD'''
        self.examples='''
%s  cur                      # just update
%s  cur  -p clean.all        # kill all jtwc.local forms
%s  2005-2011  -p clean.all  # kill all jtwc.local forms'''


#llllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll
#
# local defs
#
def logparse(cards):
    sizes={}
    if(cards == None):
        return(sizes)
    elif(len(cards) == 0):
        return(sizes)
    
    for card in cards:
        tt=card.split()
        sizes[tt[0]]=int(tt[2])
        
    return(sizes)




#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
# main
#

argv=sys.argv
CL=RsyncCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr


#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
# path setup
#
dtTimeCheckMin=-4.5

doarchadeck=0

#
# test if the curdtg is in the shem overlap
#
curyyyy=curdtg[0:4]

(shemoverlap,yyyy1,yyyy2)=CurShemOverlap(curdtg)


#
# do 9X storms if real-time update and ops!!!
#

mm=curdtg[4:6]
if(yyyy == 'ops' or yyyy == 'cur'):
    do9Xstms=1
    if(popt == None): popt=''
    yyyy=curdtg[0:4]
    writelog=1
    doarchadeck=1

try:
    (yyyy1,yyyy2)=yyyy.split('-')
    years=range(int(yyyy1),int(yyyy2)+1)
except:
    if(yyyy == 'all'):
        years=range(2000,2005)
    else:
        years=[yyyy]

if(writelog): dosizecheck=1
if(popt != None and mf.find(popt,'clean')):
    writelog=0
    dosizecheck=0


#
# set years to two years to cover shem overlap
#

if( (yyyy == curyyyy) and shemoverlap):
    years=[yyyy1,yyyy2]

#
# do previous year to catch overlap of storms crossing year
#
elif( (yyyy == curyyyy) and (int(mm) == 1)):
    yyyym1=int(yyyy)-1
    yyyym1=str(yyyym1)
    years=[yyyym1,yyyy]


#yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy
#
# loop by years
#
#yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy

for year in years:

    (shemid,nioid)=TCNum2Stmid(year,verb=verb)

    #1111111111111111111111111111111111111111111111111111111111111111
    #
    # convert jtwc adecks -> my at.local form
    #

    sdir=w2.TcAdecksJtwcDir+"/%s"%(year)
    tdir=w2.TcAdecksFinalDir+"/%s"%(year)
    mf.ChkDir(tdir,'mk')

    #
    # convert nrl/nhc adecks in lant/epac/cpac to my at.local.form
    #
    # for 1999 + use nhc for al/ep/cp
    #
    # 20070717 -- always use nhc adecks
    
    sdiradeckal=w2.TcAdecksNhcDir+"/%s"%(year)
    sdiradecksl=w2.TcAdecksNhcDir+"/%s"%(year)
    sdiradeckep=w2.TcAdecksNhcDir+"/%s"%(year)
    sdiradeckcp=w2.TcAdecksNhcDir+"/%s"%(year)

    maskadeckal="%s/aal??%s.dat"%(sdiradeckal,year)
    maskadecksl="%s/asl??%s.dat"%(sdiradecksl,year)
    maskadeckep="%s/aep??%s.dat"%(sdiradeckep,year)
    #
    # handle case when cp storm -> jtwc aor
    # handle case where ep storm -> cpc -> jtwc updated
    #
    maskadeckcpnhc="%s/acp??%s.dat"%(sdiradeckcp,year)
    maskadeckcpjtwc="%s/acp??%s.dat"%(sdir,year)
    maskadeckepnhc="%s/aep??%s.dat"%(sdiradeckep,year)
    maskadeckepjtwc="%s/aep??%s.dat"%(sdir,year)
    maskadeckwp="%s/awp*%s.dat"%(sdir,year)
    maskadecksh="%s/ash*%s.dat"%(sdir,year)
    maskadeckio="%s/aio*%s.dat"%(sdir,year)

    if(verb):
        print 'MMMMal     ',maskadeckal
        print 'MMMMsl     ',maskadecksl
        print 'MMMMep     ',maskadeckep
        
        print 'MMMMcpnhc  ',maskadeckcpnhc
        print 'MMMMcpjtwc ',maskadeckcpjtwc
        
        print 'MMMMepnhc  ',maskadeckepnhc
        print 'MMMMepjtwc ',maskadeckepjtwc
        
        print 'MMMMwp     ',maskadeckwp
        print 'MMMMsh     ',maskadecksh
        print 'MMMMio     ',maskadeckio

    #
    # always kill off 9X storms if NOT real-time (cur)
    #

    if(do9Xstms == 0):
        mask="%s/AD.???.????.9??.txt"%(tdir)
        killfiles=glob.glob(mask)
        for kfile in killfiles:
            os.unlink(kfile)
        #cmd="rm -f " %s/AD.???.????.9??.txt"%(tdir)
        #mf.runcmd(cmd,ropt)
    
    #
    # clean out existing A* and adeck.local*
    #

    if(popt == 'clean.local'):
        cmd="rm %s/AD.* ; rm %s/AdOps.* "%(tdir)
        mf.runcmd(cmd,ropt)

    if(popt == 'clean.at'):
        cmd="rm %s/adeck.local.*"%(tdir)
        mf.runcmd(cmd,ropt)

    if(popt == 'clean.all'):
        
        MF.sTimer('clean.all')
        ADfiles=glob.glob("%s/AD.*"%(tdir))
        adeckfiles=glob.glob("%s/adeck.local.*"%(tdir))
        AdOpsfiles=glob.glob("%s/AdOps.*"%(tdir))
        
        for kfile in ADfiles+adeckfiles+AdOpsfiles:
            if(verb): print "killing ",kfile
            os.unlink(kfile)
        MF.dTimer('clean.all')
                            
    adecksal=glob.glob(maskadeckal)
    adeckssl=glob.glob(maskadecksl)
    adeckscpnhc=glob.glob(maskadeckcpnhc)
    adeckscpjtwc=glob.glob(maskadeckcpjtwc)

    adecksepnhc=glob.glob(maskadeckepnhc)
    adecksepjtwc=glob.glob(maskadeckepjtwc)

    adeckswp=glob.glob(maskadeckwp)
    adeckssh=glob.glob(maskadecksh)
    adecksio=glob.glob(maskadeckio)

    #
    # order adecks with al first, jt and then override jt with nhc if available
    # 20060829 make jt first for cpac when XXC -> jtwc aor
    #

    adecksep=ATCF.PickBestDeck(adecksepnhc,adecksepjtwc,verb=verb)
    adeckscp=ATCF.PickBestDeck(adeckscpnhc,adeckscpjtwc,verb=verb)

    adecks= adeckswp + adeckssh + adecksio  + adeckscp + adecksal + adeckssl + adecksep

    adecksizes={}
    
    if(writelog):
        logcards=w2.GetLogLatest('adeck',curdtg)
        adecksizes=logparse(logcards)

    #
    # if adecks
    #
    localadecks=[]
    log=[]

    if(writelog):
        logdir="%s/%s"%(w2.TcAdeckLogDir,curdtg)
        mf.ChkDir(logdir,'mk')
        logfile="adeck.%s.txt"%(mf.dtg('dtg_ms'))
        logpath="%s/%s"%(logdir,logfile)

    ######### -- before using just jtwc/nhc adecks: if(len(adecks) != 0) and int(year) >= 2001 ):
    if(len(adecks) != 0):

        for adeck in adecks:

            atCheckArch=0

            (adsdir,adeckfile)=os.path.split(adeck)
            MF.ChkDir(adsdir,'mk')
            curadecksize=mf.GetPathSiz(adeck)
            if(curadecksize == None): curadecksize=0
            
            stmnum=adeckfile[3:5]
            #
            # check for alphanumeric storm id's from jtwc
            #
            if(not(stmnum[0].isdigit())):
                continue

            istmnum=int(stmnum)

            b2id=adeckfile[1:3]
            b2id=b2id.upper()

            b1id=Basin2toBasin1[b2id]
            b3id=Basin1toBasin3[b1id]

            #
            # new logic to us storms.table for shem 1-char basin ids... 
            #
            
            foundb1id=1
            if(b3id == 'shm'):
                try:
                    stmid=shemid[stmnum]
                except:
                    foundb1id=0
            elif(b3id == 'nio'):
                try:
                    stmid=nioid[stmnum]
                except:
                    foundb1id=0
            else:
                stmid=stmnum+b1id

            if(foundb1id == 0):
                try:
                    adcard=open(adeck).readlines(1)[0]
                except:
                    continue

                if(len(adcard.split(',')) <= 1):
                    print 'WWWW(bad adcard): ',adcard
                    continue
                   
                (clat,clon)=adcard.split(',')[6:8]
                clat=clat.strip()
                clon=clon.strip()
                if(len(clat) == 0  or len(clon) ==  0):
                    print 'WWWW(bad adeck): ',adeck
                    continue
                (rlat,rlon)=Clatlon2Rlatlon(clat,clon)
                b1id=tcbasinb1id(rlat,rlon,b3id)
                #print 'BBBBBBBBBBBBBBBBBBB ',rlat,rlon,b1id
                stmid=stmnum+b1id
            

            if(dodupchk):
                #
                # check for multiple b1ids + symbolic links
                #
                maskofileid="%s/adeck.local.jtwc.%s.%s.%2s?.*.txt"%(tdir,b3id,year,stmid[0:2])
                masklnfileid="%s/A*.%s.%s.%2s?.*.txt"%(tdir,b3id,year,stmid[0:2])
                oadecks=glob.glob(maskofileid)
                olnadecks=glob.glob(masklnfileid)
                if(len(oadecks) > 1):
                    print 'WWWWWW(dups) multiple local adecks...use olds stmid...for: ',stmid[0:2]
                    for oadeck in oadecks:
                        print 'WWWWWW(dups) oadeck: ',oadeck

                    oages={}
                    for oadeck in oadecks:
                        timei=os.path.getmtime(oadeck)
                        (dir,file)=os.path.split(oadeck)
                        tt=file.split('.')
                        oages[tt[5]]=timei
                    kk=oages.keys()
                    kk.sort()
                    koldest=kk[0]
                    oldest=oages[koldest]
                    for k in kk:
                        if(oages[k] < oldest):
                            koldest=k
                    stmid=koldest
                    print 'WWWWWW(dups) setting the stmid to: ',stmid
                    print 'WWWWWW(dups) blowoff...to force recalc...'
                    for oadeck in oadecks:
                        os.unlink(oadeck)
                #
                # always blow off ln adecks
                #
                if(len(olnadecks) > 1):
                    for olnadeck in olnadecks:
                        os.unlink(olnadeck)




            maskofile="adeck.local.jtwc.%s.%s.%s.*.txt"%(b3id,year,stmid)
            maskopath="%s/%s"%(tdir,maskofile)
            try:
                adeckopath=glob.glob(maskopath)[0]
            except:
                adeckopath='/tmp/Zy0x1w2!'
                

            print 'Checking adeck: %-80s'%(adeck),'adeckopath:: %-110s'%(adeckopath)
            
            #
            # compare age of real and local adecks
            #

            timei=-999
            dtimei=dtimeo=-999
            if(os.path.exists(adeck)):
                timei=os.path.getctime(adeck)
                ltimei=time.localtime(timei)
                dtimei=time.strftime("%Y%m%d%H:%M%S",ltimei)
                dti=MF.PathModifyTimeCurdiff(adeck)

                # -- doesn't work for NHC...only for bdecks not adecks
                # -- now does by changes in w2.tc.wget.mirror.nhc.abdeck.2.local.py by using gzip -d vice gunzip -- preserves time stamp
                #
                if(dti > dtTimeCheckMin):
                    atCheckArch=1

            timeo=-999
            if(os.path.exists(adeckopath)):
                timeo=os.path.getctime(adeckopath)
                ltimeo=time.localtime(timeo)
                dtimeo=time.strftime("%Y%m%d%H:%M%S",ltimeo)

            dochk=0
            if(atCheckArch):
                dochk=1

            elif( (timei < timeo) and (timeo != -999) ):
                if(verb):
                    print "OOOOOOOOOOO adeck already processed: ",adeck
                    print '     adeck: ',dtimei,adeck
                    print 'adeckopath: ',dtimeo,adeckopath

                continue

            if(verb and dochk):
                print
                print 'CCCCC-checking...'
                print 'adeck:      ',dtimei,adeck
                print 'adeckopath: ',dtimeo,adeckopath
                #print 'WWWWWWWWWWWWWWWWW blow off timei timeo:',timei,timeo,' adeck: ',adeck

            #
            #  filter out 8X storms
            #
            if(istmnum >= 50 and istmnum <= 89):
                if(verb): print 'WWWWWWWWWWWWWWWWW blow off istmnum >=50 and <= 89'
                continue

            #
            # if real-time keep 9X otherwise kill
            #
            if((do9Xstms == 0) and (istmnum >= 50)):
                if(verb): print 'WWWWWWWWWWWWWWWWW blow off do9Xstms == 0 and stmnum >=50'
                continue

            #
            # parse the adeck and create local adeck file cards
            #
            
            (adeckcards,bdtg,edtg)=GrepAdeck(adeck,year)
            adeckofile="adeck.local.jtwc.%s.%s.%s.%s.%s.txt"%(b3id,year,stmid,bdtg,edtg)
            adeckopath="%s/%s"%(tdir,adeckofile)

            #
            # case where adeck does NOT have CARQ OFCL, JTWC .. do a noload
            #
            if(len(adeckcards) == 0 and curadecksize > 0):
                print 'NNNN noload for ',stmid,year,adeck
                adeckcards=['no carq,ofcl, jtwc in this adeck...'] 

            #
            # bail if no cards, bad adeck
            #
            if(not(len(adeckcards))):
                ## -- don't unlink -- just forces rsync to bring over, just continue
                ## print 'WWWWWWWWWWWW no cards in adeck: ',adeck,' SaYOOOnara it...'
                ## cmd="rm %s"%(adeck)
                ## mf.runcmd(cmd,ropt)
                print 'WWWWWWWWWWWWWWWWW blow off len(adeckards): ',len(adeckcards)
                continue
            #
            # check if new adeck size is different
            #
            
            sizechange=1
            if(len(adecksizes) > 0):
                logads=adecksizes.keys()
                for logad in logads:
                    if(adeck == logad):
                        prvsiz=adecksizes[logad]
                        cursiz=os.path.getsize(adeck)
                        if(verb): print 'LLLL comp logadeck: ',logad,' adeck: ',adeck,' prvsiz: ',prvsiz,' cursiz: ',cursiz
                        if(cursiz == prvsiz):
                            sizechange=0
                            print 'LLLL do not update ',adeck,' until the size changes...'
            #
            # make check if adeck there... if not doit
            #
            oadomask="%s/*.%s.%s.%s.*.txt"%(tdir,b3id,year,stmid)
            curaodecks=len(glob.glob(oadomask))

            # -- bad idea for old problem...
            #
            #if(sizechange == 0 and dosizecheck and curaodecks != 0 or mf.find(adeckopath,'12L') or mf.find(adeckopath,'10L')):
            #    print 'WWWWWWWWWWWWWWWWW blow off for 12l and 10L'
            #    continue
            # -- bring back? no because adeck can change with size being the same?
            # -- 20121206 lets try again...
            
            if(sizechange == 0 and dosizecheck and curaodecks != 0 and atCheckArch == 0):
                continue
            
            if(curaodecks == 0):
                print 'WWWW prev adeck for ',oadomask,' not there...DO it'

            print 'AAAAAA working/updating --- ',adeck,' to: ',adeckopath
            
            doarchadeck=1
            if(doarchadeck):

                adarchdir="%s/archive"%(adsdir)
                mf.ChkDir(adarchdir,'mk')
                adarchfile="%s_%s"%(adeckfile,mf.dtg('dtg_hms'))
                adarchpath="%s/%s"%(adarchdir,adarchfile)
                adarchzippath="%s/%s.zip"%(adarchdir,adeckfile)

                # -- use new method in w2methods.py to only add if different from last member of archive
                #
                rc=addFile2ZipArchive(adeck,adarchzippath,forceAdd=0)
                
##                 try:
##                     ADZZ=zipfile.ZipFile(adarchzippath,'a')
##                 except:
##                     ADZZ=zipfile.ZipFile(adarchzippath,'w')
##                 ADZZ.write(adeck,adarchfile,zipfile.ZIP_DEFLATED)
##                 ADZZ.close()
                
            #
            # blow away old adeck.local.jtwc*
            #
            if(curaodecks != 0):
                oadomask="%s/*.%s.%s.%s.*.txt"%(tdir,b3id,year,stmid)
                cmd="rm -f %s"%(oadomask)
                mf.runcmd(cmd,ropt)
                
            localadecks.append(adeckopath)
            siz=mf.GetPathSiz(adeck)
            logcard="%s siz: %8d  dtg: %s time %s  phr: %s"%(adeck,siz,
                                                             curdtg,mf.dtg('dtg_ms'),
                                                             mf.rhh2hhmm(float(mf.dtg('phr'))))

            log.append(logcard)

            MF.WriteList2File(adeckcards,adeckopath)


    if(len(log) > 0 and writelog):
        MF.WriteList2File(log,logpath,verb=1)

        
    #222222222222222222222222222222222222222222222222222222222222222222222
    #
    # ln -s to "final" AD
    #

    for adeck in localadecks:
        
        (idir,ifile)=os.path.split(adeck)
        lf=len(ifile)

        tt=ifile.split('.')
        
        b3id=tt[3]
        year=tt[4]
        stmid=tt[5]
        bdtg=tt[6]
        edtg=tt[7]
        
        stmnum=int(stmid[0:2])

        #
        # always do AdOps; just base on stmnum
        #
        
        if( (stmnum <= 50) ):
            begs=['AD','AdOps']
        elif( (stmnum > 50) ):
            begs=['AdOps']
        else:
            begs=['AD']

        for beg in begs:
            ofile="%s.%s.%s.%s.%s.%s.txt"%(beg,b3id,year,stmid,bdtg,edtg)
            #oadeck="%s/%s"%(tdir,ofile)
            #
            # keep dir out of ln?
            #
            os.chdir(idir)
            if(doLn):
                cmd="ln -f -s %s %s"%(ifile,ofile)
            else:
                cmd="cp %s %s"%(ifile,ofile)
                
            mf.runcmd(cmd,ropt)

sys.exit()
