#!/usr/bin/env python

from WxMAP2 import *
w2=W2()

from tcbase import *
import ATCF

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
            'popt':             ['p:',None,'a',' [clean.BT | clean.bt | clean.all]'],
            'vopt':             ['v:',None,'a','source opt'],
            'source':           ['s:',None,'a','source opt'],
            'do9Xstms':         ['9',0,1,'do9Xstms=1'],
            'verb':             ['V',0,1,'verb=1 is verbose'],
            'ropt':             ['N','','norun',' norun is norun'],
            'writelog':         ['W',0,1,'verb=1 is verbose'],
            'doLn':             ['L',1,0,"""do NOT use 'ln -s' use 'cp' instead for filesystem independence"""],
            }

        self.purpose='''
calc bt from at jtwc to adeck (no -p) and set local to final BT'''
        self.examples='''
%s  cur                      # just update
%s  cur  -p clean.all        # kill all ln jtwc.local forms
%s  2005-2011  -p clean.all  # kill all ln jtwc.local forms'''



#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
# main
#

argv=sys.argv
CL=RsyncCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr
dtTimeCheckMin=-4.5

#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
# test if the curdtg is in the shem overlap
#

doarchadeck=0

curyyyy=curdtg[0:4]
(shemoverlap,yyyy1,yyyy2)=CurShemOverlap(curdtg)

#
# do 9X storms if real-time update and ops!!!
#

mm=curdtg[4:6]

if(yyyy == 'cur' or yyyy == 'ops'):
    do9Xstms=1
    if(popt == None): popt=''
    yyyy=curdtg[0:4]
    mm=curdtg[4:6]
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

#  set the year to cut away from neumann....
#

yearneumann=YearTcBtNeumann

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

# -- hard wire to hfip dir

for year in years:

    (shemid,nioid)=TCNum2Stmid(year)

    #
    # neumann data...just ln
    #
    if(int(year) <= yearneumann):
        
        btdir=w2.TcBtDatDir+"/%s"%(year)
        os.chdir(btdir)
        btsmask="bt.neumann.*.txt"
        btslocal=glob.glob(btsmask)
        print 'neumann data: bt.neumann.BBB.YYYY.SSS.txt ; just do ln .......'
        for bt in btslocal:
            b3id=bt.split('.')[2]
            stmid=bt.split('.')[4]
            ofile="BT.%s.%s.%s.txt"%(b3id,year,stmid)
            obdeck="%s"%(ofile)
            if(doLn):
                cmd="ln -f -s %s %s"%(bt,obdeck)
            else:
                cmd="cp %s %s"%(bt,obdeck)
                
            mf.runcmd(cmd,ropt)

        continue
    
    else:
        
        btdir=w2.TcBtDatDir+"/%s"%(year)
        mf.ChkDir(btdir,diropt='mk')
        

    #1111111111111111111111111111111111111111111111111111111111111111
    #
    # convert jtwc bdecks -> my bt.local form
    #

    bdir=w2.TcBdecksJtwcDir+"/%s"%(year)
    tdir=w2.TcBtDatDir+"/%s"%(year)
    mf.ChkDir(tdir,'mk')
    
    # -- convert nrl/nhc bdecks in lant/epac/cpac to my bt.local.form
    #
    # for 1999 + use nhc for al/ep/cp


    if(int(year) >= yearneumann):
        bdirbdeckal=w2.TcBdecksNhcDir+"/%s"%(year)
        bdirbdeckep=w2.TcBdecksNhcDir+"/%s"%(year)
        bdirbdeckcp=w2.TcBdecksNhcDir+"/%s"%(year)

    maskbdeckal="%s/bal??%s.dat"%(bdirbdeckal,year)
    maskbdecksl="%s/bsl??%s.dat"%(bdirbdeckal,year)
    maskbdeckep="%s/bep??%s.dat"%(bdirbdeckep,year)

    # -- handle case when cp storm -> jtwc aor
    # -- handle case where ep storm -> cpc -> jtwc updated
    #
    maskbdeckcpnhc="%s/bcp??%s.dat"%(bdirbdeckcp,year)
    maskbdeckcpjtwc="%s/bcp??%s.dat"%(bdir,year)
    maskbdeckepnhc="%s/bep??%s.dat"%(bdirbdeckep,year)
    maskbdeckepjtwc="%s/bep??%s.dat"%(bdir,year)
    maskbdeckwp="%s/bwp??%s.dat"%(bdir,year)
    maskbdeckio="%s/bio??%s.dat"%(bdir,year)
    maskbdecksh="%s/bsh??%s.dat"%(bdir,year)

    if(verb):
        print 'MMMMal     ',maskbdeckal
        print 'MMMMsl     ',maskbdecksl
        print 'MMMMep     ',maskbdeckep
        print 'MMMMcpnhc  ',maskbdeckcpnhc
        print 'MMMMcpjtwc ',maskbdeckcpnhc
        print 'MMMMepnhc  ',maskbdeckepnhc
        print 'MMMMepjtwc ',maskbdeckepnhc
        print 'MMMMwp     ',maskbdeckwp
        print 'MMMMio     ',maskbdeckio
        print 'MMMMsh     ',maskbdecksh
    

    #
    # always kill off 9X storms if NOT real-time (cur)
    #

    if(do9Xstms == 0):
        cmd="rm -f %s/BT.???.????.9??.txt"%(tdir)
        mf.runcmd(cmd,ropt)
    
    #
    # clean out existing B* and bt.local*
    #

    if(popt == 'clean.local'):
        cmd="rm %s/BT.* ; rm %s/BtOps.* "%(tdir)
        mf.runcmd(cmd,ropt)

    if(popt == 'clean.bt'):
        cmd="rm %s/bt.local.*"%(tdir)
        mf.runcmd(cmd,ropt)

    if(popt == 'clean.all'):
        
        MF.sTimer('clean.all')
        BTfiles=glob.glob("%s/BT.*"%(tdir))
        btlocalfiles=glob.glob("%s/bt.local.*"%(tdir))
        BtOpsfiles=glob.glob("%s/BtOps.*"%(tdir))
        
        for kfile in BTfiles+btlocalfiles+BtOpsfiles:
            if(verb): print "killing ",kfile
            os.unlink(kfile)
        MF.dTimer('clean.all')
         
        #cmd="rm %s/BT.* ; rm %s/bt.local.* ; rm %s/BtOps.*"%(tdir,tdir,tdir)
        #mf.runcmd(cmd,ropt)


    bdeckswp=glob.glob(maskbdeckwp)
    bdecksio=glob.glob(maskbdeckio)
    bdeckssh=glob.glob(maskbdecksh)

    bdecksal=glob.glob(maskbdeckal)
    bdeckssl=glob.glob(maskbdecksl)

    bdeckscpnhc=glob.glob(maskbdeckcpnhc)
    bdeckscpjtwc=glob.glob(maskbdeckcpjtwc)

    bdecksepnhc=glob.glob(maskbdeckepnhc)
    bdecksepjtwc=glob.glob(maskbdeckepjtwc)

    #
    # def to pick "correct" deck
    #

    bdecksep=ATCF.PickBestDeck(bdecksepnhc,bdecksepjtwc,verb=verb)
    bdeckscp=ATCF.PickBestDeck(bdeckscpnhc,bdeckscpjtwc,verb=verb)

    # -- force nhc for bdecks
    bdecksep=bdecksepnhc
    bdeckscp=bdeckscpnhc
    
    bdecks= bdeckswp + bdecksio + bdeckssh + bdeckscp + bdecksal + bdeckssl + bdecksep
    bdecks.sort()
    
    bdecksizes={}
    if(writelog):
        logcards=w2.GetLogLatest('bdeck',curdtg)
        bdecksizes=logparse(logcards)
    
    #
    # if bdecks
    #
    
    localbdecks=[]
    log=[]
    
    if(writelog):
        logdir="%s/%s"%(w2.TcBdeckLogDir,curdtg)
        mf.ChkDir(logdir,'mk')
        logfile="bdeck.%s.txt"%(mf.dtg('dtg_ms'))
        logpath="%s/%s"%(logdir,logfile)

        
    if(len(bdecks) != 0 and int(year) >= yearneumann ):

        for bdeck in bdecks:

            btCheckArch=0
            (bdsdir,bdeckfile)=os.path.split(bdeck)
            curbdecksize=mf.GetPathSiz(bdeck)
            if(curbdecksize == None): curbdecksize=0

            stmnum=bdeckfile[3:5]
            #
            # check for alphanumeric storm id's from jtwc
            #
            if(not(stmnum[0].isdigit())):
                continue
            
            istmnum=int(stmnum)
            
            b2id=bdeckfile[1:3]
            b2id=b2id.upper()

            b1id=Basin2toBasin1[b2id]
            b3id=Basin1toBasin3[b1id]

            #
            # new logic to use storms.table for shem/nio 1-char basin ids... 
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
                    bdcard=open(bdeck).readlines()[0]
                except:
                    continue
                
                (clat,clon)=bdcard.split(',')[6:8]
                clat.strip()
                clon.strip()
                (rlat,rlon)=Clatlon2Rlatlon(clat,clon)
                b1id=tcbasinb1id(rlat,rlon,b3id)
                ###print 'BBBBB ',rlat,rlon,b1id
                stmid=stmnum+b1id

            
            #
            #  filter out 8X storms
            #

            if(istmnum >= 50 and istmnum <= 89): continue

            #
            # if real-time keep 9X otherwise kill
            #

            if((do9Xstms == 0) and (istmnum >= 50)): continue

            if(dodupchk):
                #
                # check for multiple b1ids
                #
                maskofileid="%s/bt.local.jtwc.%s.%s.%2s?.*.txt"%(tdir,b3id,year,stmid[0:2])
                masklnfileid="%s/B*.%s.%s.%2s?.*.txt"%(tdir,b3id,year,stmid[0:2])
                obdecks=glob.glob(maskofileid)
                olnbdecks=glob.glob(masklnfileid)
                if(len(obdecks) > 1):
                    print 'WWWWWW(dups) multiple local bdecks...use olds stmid...for: ',stmid[0:2]
                    for obdeck in obdecks:
                        print 'WWWWWW(dups) obdeck: ',obdeck

                    oages={}
                    for obdeck in obdecks:
                        timei=os.path.getmtime(obdeck)
                        (dir,file)=os.path.split(obdeck)
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
                    for obdeck in obdecks:
                        os.unlink(obdeck)
                #
                # always blow off ln adecks
                #
                if(len(olnbdecks) > 1):
                    for olnbdeck in olnbdecks:
                        os.unlink(olnbdeck)
            
            maskofile="bt.local.jtwc.%s.%s.%s.*.txt"%(b3id,year,stmid)
            maskopath="%s/%s"%(tdir,maskofile)
            try:
                bdeckopath=glob.glob(maskopath)[0]
            except:
                bdeckopath='/tmp/Zy0x1w2!'
            #
            # compare age of real and local adecks
            #

            timei=-999
            dtimei=-999
            if(os.path.exists(bdeck)):
                timei=os.path.getctime(bdeck)
                ltimei=time.localtime(timei)
                dtimei=time.strftime("%Y%m%d%H:%M%S",ltimei)
                dti=MF.PathModifyTimeCurdiff(bdeck)
                
                if(dti > dtTimeCheckMin):
                    btCheckArch=1

            timeo=-999
            dtimeo=-999
            if(os.path.exists(bdeckopath)):
                timeo=os.path.getctime(bdeckopath)
                ltimeo=time.localtime(timeo)
                dtimeo=time.strftime("%Y%m%d%H:%M%S",ltimeo)


            dochk=0
            if(btCheckArch):
                dochk=1

            elif( (timei < timeo) and (timeo != -999)):
                dochk=0
                if(verb):
                    print "OOOOOOOOOOO bdeck already processed: ",bdeck
                    print 'bdeck:      ',dtimei,bdeck
                    print 'bdeckopath: ',dtimeo,bdeckopath

                continue

            if(verb and dochk):
                print
                print 'CCCCC-checking...'
                print 'bdeck:      ',dtimei,bdeck
                print 'bdeckopath: ',dtimeo,bdeckopath
                
            (btcards,bdtg,edtg)=ParseBdeck(bdeck,year)
            bdeckofile="bt.local.jtwc.%s.%s.%s.%s.%s.txt"%(b3id,year,stmid,bdtg,edtg)
            bdeckopath="%s/%s"%(tdir,bdeckofile)

            #
            # bail if no cards, bad bdeck
            #
            
            if(not(btcards)):
                ## -- don't unlink -- just forces rsync to bring over, just continue
                ## print 'WWWWWWWWWWW no cards in bdeck: ',bdeck,' SaYOOOnara it...'
                ## cmd="rm %s"%(bdeck)
                ## mf.runcmd(cmd,ropt)
                continue

            #
            # check if new adeck size is different
            #
            
            sizechange=1
            if(len(bdecksizes) > 0):
                logbdecks=bdecksizes.keys()
                for logbdeck in logbdecks:
                    if(bdeck == logbdeck):
                        prvsiz=bdecksizes[logbdeck]
                        cursiz=os.path.getsize(bdeck)
                        if(verb): print 'LLLL comp logbdeck: ',logbdeck,' bdeck: ',bdeck,' prvsiz: ',prvsiz,' cursiz: ',cursiz
                        if(cursiz == prvsiz):
                            sizechange=0
                            print 'LLLL do not update ',bdeck,' until the size changes...'; print

            #
            # make sure bdeck there, if not ... do it
            #
            obdeckomask="%s/*.%s.%s.%s.*.txt"%(tdir,b3id,year,stmid)
            curbodecks=len(glob.glob(obdeckomask))
            if(sizechange == 0 and dosizecheck and curbodecks != 0 and btCheckArch == 0):
                continue

            if(curbodecks == 0):
                print 'WWWW prev bdeck for ',obdeckomask,' not there...DO it'
        
            print 'BBBBBB working/updating --- ',bdeck

            doarchbdeck=1
            if(doarchbdeck):

                bdarchdir="%s/archive"%(bdsdir)
                mf.ChkDir(bdarchdir,'mk')
                bdarchfile="%s_%s"%(bdeckfile,mf.dtg('dtg_hms'))
                bdarchpath="%s/%s"%(bdarchdir,bdarchfile)
                bdarchzippath="%s/%s.zip"%(bdarchdir,bdeckfile)
                
                # -- use new method in w2methods.py to only add if different from last member of archive
                #
                rc=addFile2ZipArchive(bdeck,bdarchzippath,forceAdd=0)

##                 try:
##                     BDZZ=zipfile.ZipFile(bdarchzippath,'a')
##                 except:
##                     BDZZ=zipfile.ZipFile(bdarchzippath,'w')
##                 BDZZ.write(bdeck,bdarchfile,zipfile.ZIP_DEFLATED)
##                 BDZZ.close()

            #
            # blow away old bt.local.jtwc*
            #
            if(curbodecks != 0):
                obdeckomask="%s/*.%s.%s.%s.*.txt"%(tdir,b3id,year,stmid)
                cmd="rm %s"%(obdeckomask)
                mf.runcmd(cmd,ropt)

            localbdecks.append(bdeckopath)
            siz=mf.GetPathSiz(bdeck)
            logcard="%s siz: %8d  dtg: %s time %s  phr: %s"%(bdeck,siz,
                                                             curdtg,mf.dtg('dtg_ms'),
                                                             mf.rhh2hhmm(float(mf.dtg('phr'))))
            log.append(logcard)

            MF.WriteList2File(btcards,bdeckopath)


    if(len(log) > 0 and writelog):
        MF.WriteList2File(log,logpath,verb=1)

    #222222222222222222222222222222222222222222222222222222222222222222222
    #
    # ln -s to "final" BT
    #
    for bdeck in localbdecks:
    
        (idir,ifile)=os.path.split(bdeck)
        lf=len(ifile)

        tt=ifile.split('.')

        b3id=tt[3]
        year=tt[4]
        stmid=tt[5]
        bdtg=tt[6]
        edtg=tt[7]
        
        stmnum=int(stmid[0:2])

        #
        # always do BtOps; just base on stmnum
        #
        
        if( (stmnum <= 50) ):
            begs=['BT','BtOps']
        elif( (stmnum > 50) ):
            begs=['BtOps']
        else:
            begs=['BT']

        for beg in begs:
            ofile="%s.%s.%s.%s.%s.%s.txt"%(beg,b3id,year,stmid,bdtg,edtg)
            
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
