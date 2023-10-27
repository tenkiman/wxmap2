#!/usr/bin/env python

from tcbase import *

#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
#
# command line setup
#

def basin2b1id(basin):
    b1id=Basin2toBasin1[basin.upper()]
    if(basin.upper() == 'SH'): b1id='h'
    return(b1id)
    
class MssCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv
        
        self.argv=argv
        self.argopts={
            1:['yearopt',    'no default'],
            }

        self.defaults={
            }

        self.options={
            'override':      ['O',0,1,'verb=1 is verbose'],
            'verb':          ['V',0,1,'verb=1 is verbose'],
            'ropt':          ['N','','norun',' norun is norun'],
            'doBdeck2':      ['2',1,0,'do NOT do bdeck2 -- bdeck2 is a separate archive'],
            
            }

        self.purpose='''
purpose -- mirror a/b/e/fdecks from nhc to local
%s cur
'''
        self.examples='''
%s cur'''

MF.sTimer(tag='all')

argv=sys.argv
CL=MssCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

yy=yearopt.split('.')
if(len(yy) == 2):
    byear=int(yy[0])
    eyear=int(yy[1])
    
else:
    byear=int(yearopt)
    eyear=int(yearopt)
    
years=range(byear,eyear+1)

print 'yyyy',years

if(len(years) > 1):
    
    for year in years:
        cmd="%s %d"%(pypath,year)
        mf.runcmd(cmd,ropt)
        
    sys.exit()


tcD=TcData(years=years)
year=years[0]
iyear=int(year)

deck='bdeck'
if(doBdeck2): deck='bdeck2'

af=w2.NhcFtpserver

#al=w2.NhcLogin
#ap=w2.NhcPasswd

sbdir=w2.NhcDatDir
tbdir=w2.TcDatDir

basins=['cp','ep','al']
#basins=['ep']
#basins=['cp']
#basins=['al']

roptWget=ropt

doCleanDat=0
dowget=1
doDatMv=0
if(not(dowget)): roptWget='norun'

tdir="%s/%s/%s/%s"%(tbdir,deck,'nhc',year)
tdirWorking="%s/working"%(tdir)
tdirFinal="%s/final"%(tdir)
tdirArchive="%s/archive"%(tdir)
tdirInvests="%s/invests"%(tdir)

MF.ChkDir(tdirWorking,'mk')
MF.ChkDir(tdirFinal,'mk')
MF.ChkDir(tdirInvests,'mk')

if(deck == 'adeck'): dtype='a'
if(deck == 'bdeck' or deck == 'bdeck2'): dtype='b'

for basin in basins:

    pfile='%s%s-processed-%s'%(dtype,basin,curdtg)
    if(MF.ChkPath(pfile) and not(override)):
        print 'WWWWWWWWWWW -- basin: ',basin,' already processed.......override = 0'
        sys.exit()
        

    # -- get stmids
    #
    b1id=basin2b1id(basin)
    stmopt="%s.%s"%(b1id.lower(),iyear)
    stmids=tcD.makeStmListMdeck(stmopt,dobt=1)

    wgetmaskDat="%s%s[0-9]?%s.dat"%(dtype,basin,year)
    wgetmaskInvests="%s%s[A-Z]?%s.dat"%(dtype,basin,year)
    wgetmaskTxt="%s%s[0-9]?%s.txt"%(dtype,basin,year)
    
    workingFiles=glob.glob("%s/%s"%(tdirWorking,wgetmaskDat))
    nwFiles=len(workingFiles)

    # -- WWWWWWWWWWWWWWWWWWWWWWWWWW -- mv current .dat to working/
    #
    if(doDatMv and nwFiles == 0):
        cmd="mv -n %s/%s %s/."%(tdir,wgetmaskDat,tdirWorking)
        mf.runcmd(cmd,ropt)
        
    # -- restore NN decks from archive
    #
    for stmid in stmids:

        (snum,b1id,year,b2id,stm2id,stm1id)=getStmParams(stmid)
        zname="%s%s%s%s"%(dtype,b2id.lower(),snum,year)
        zdeck="%s/%s.dat.zip"%(tdirArchive,zname)
        wpath="%s/%s.dat-A"%(tdirWorking,zname)
        wpathC="%s/%s.dat"%(tdirWorking,zname)
        wpathSAV="%s/%s.dat-SAV"%(tdirWorking,zname)

        if(MF.ChkPath(zdeck) and (not(MF.ChkPath(wpath)) or override) ):
            Z=zipfile.ZipFile(zdeck)
            zfiles=Z.namelist()
            if(int(year) <= 2012):
                try:
                    zfile=zfiles[-2]
                except:
                    zfile=zfiles[-1]
            else:
                zfile=zfiles[-1]
            print 'zdeck: ',zdeck
            print 'zfile: ',zfile
            print 'MAKING wpath: ',wpath
            ocards=Z.read(zfile)        
            MF.WriteString2Path(ocards, wpath)
            
        didcpA=0
        if(MF.ChkPath(wpath) and not(MF.ChkPath(wpathC))):
            print 'archive wpath good, but no working...cp over'
            mf.runcmd('cp %s %s'%(wpath,wpathC))
            didcpA=1
        
        if(MF.ChkPath(wpath) and MF.ChkPath(wpathC) and not(MF.ChkPath(wpathSAV))):
            cmd='cmp %s %s'%(wpath,wpathC)
            rc=MF.runcmdLog(cmd,ropt)
            print 'wpath: ',wpath,'rc: ',rc,len(rc)
            if(len(rc) > 1):
                print '!!!!!!!!!!! Archive != Current for: ',stmid,' mv current to save and replace with archive'
                #cmd=" /Applications/xxdiff.app/Contents/MacOS/xxdiff %s %s"%(wpath,wpathC)
                #mf.runcmd(cmd)
                cmd="mv %s %s-SAV"%(wpathC,wpathC)
                mf.runcmd(cmd,ropt)
                cmd="cp %s %s"%(wpath,wpathC)
                mf.runcmd(cmd,ropt)
            else:
                print 'Archive = Current for: ',stmid
                
                
    sdir="%s/archive/%s"%(sbdir,year)
    sdirI="%s/invests"%(sdir)
    
    # -- get decks in archive/YYYY and put to YYYY/final (tdirFinal)
    #
    MF.ChangeDir(tdirFinal)
    print 'CCC: working in tdirFinal: ',os.getcwd()
        
    wgetopt='-m -nd -T 60 -t 1'
    cmd="wget %s \"ftp://%s/%s/%s%s*%s*.dat*\""%(wgetopt,af,sdir,dtype,basin,year)
    mf.runcmd(cmd,roptWget)

    # -- BBBBBBBBBBBBBBBBBBBBBBBBBB -- get decks in archive/YYYY/invests and put to YYYY/invests(tdirFinal)
    #
    MF.ChangeDir(tdirInvests)
    print 'CCC: working in tdirFinal: ',os.getcwd()
        
    wgetopt='-m -nd -T 60 -t 1'
    cmd="wget %s \"ftp://%s/%s/%s%s*%s*.dat*\""%(wgetopt,af,sdirI,dtype,basin,year)
    mf.runcmd(cmd,roptWget)

    # -- IIIIIIIIIIIIIIIIIIIIIIIIII -- get invests bdecks in invests/
    #
    gzs=glob.glob("%s/%s.gz"%(tdirInvests,wgetmaskInvests))

    for gz in gzs:
        (fdir,ffile)=os.path.split(gz)
        (gzu,gzext)=os.path.splitext(ffile)
        gzuSAV="%s.SAV"%(gzu)
        dpath="%s/%s"%(fdir,gzu)
        if(not(MF.ChkPath(dpath))):
            print 'GGGG gunziping .gz in: %s/%s'%(fdir,gzu)
            #cmd="gunzip -c %s > %s/%s"%(gz,fdir,gzu)
            #mf.runcmd(cmd,'quiet')
            cmd="cp -p %s %s; gzip -f -d %s ; mv %s %s"%(gz,gzuSAV,gz,gzuSAV,gz)
            mf.runcmd(cmd,ropt)


    bdecksA=[]
    for gz in gzs:
        (fdir,ffile)=os.path.split(gz)
        bdeck=os.path.splitext(ffile)[0]
        bdecksA.append(bdeck)

    
    # -- get bdecks in final/
    #
    gzs=glob.glob("%s/%s.gz"%(tdirFinal,wgetmaskDat))
    bdecksA=[]
    for gz in gzs:
        (fdir,ffile)=os.path.split(gz)
        bdeck=os.path.splitext(ffile)[0]
        bdecksA.append(bdeck)


    # -- go to base dir ./
    #
    MF.ChangeDir(tdir)

    # -- get plain files in base dir
    #
    plain=glob.glob("%s/%s"%(tdir,wgetmaskDat))
    if(doCleanDat and len(workingFiles) == 0):
        for pfile in plain:
            os.unlink(pfile)
      
    # -- now check in real-time for bdecks not finalized
    #
    sdirRT="%s/btk"%(sbdir)

    wgetopt='-m -nd -T 60 -t 1'
    cmd="wget %s \"ftp://%s/%s/%s\""%(wgetopt,af,sdirRT,wgetmaskDat)
    mf.runcmd(cmd,ropt)

    bdecksRTall=glob.glob("%s/%s"%(tdir,wgetmaskDat))
    bdecksRT=[]
    for bd in bdecksRTall:
        (fdir,ffile)=os.path.split(bd)
        bdecksRT.append(ffile)
    
    bdecksBoth=[]
    
    for bdeckA in bdecksA:
        if(bdeckA in bdecksRT):
            bdecksBoth.append(bdeckA)
            
    print 'AAAAAAAAAA',bdecksA
    print 'RRRRRRRRRR',bdecksRT
    print 'BBBBBBBBBB',bdecksBoth

    for gz in gzs:
        (fdir,ffile)=os.path.split(gz)
        (gzu,gzext)=os.path.splitext(ffile)
        if(not(gzu in bdecksRT)):
            print 'GGGG gunziping .gz in: ',fdir,'and not in aid/:',gzu
            # -- better way to gunzip that preserves file time-stamp
            #
            gzuSAV="%s-SAV"%(gz)
            cmd="cp -p %s %s; gzip -f -d %s ; mv %s %s"%(gz,gzuSAV,gz,gzuSAV,gz)
            #cmd="gunzip -c %s > %s/%s"%(gz,fdir,gzu)
            #mf.runcmd(cmd,'quiet')
            mf.runcmd(cmd,ropt)
        else:
            print 'GGGG gunziping .gz in: ',fdir,'for FINAL bdeck :',gzu
            cmd="gunzip -c %s > %s/%s"%(gz,fdir,gzu)
            mf.runcmd(cmd,ropt)

    bdecks=glob.glob("%s/%s"%(tdirFinal,wgetmaskDat))

    for bdeck in bdecks:
        cmd="cp %s %s/."%(bdeck,tdir)
        mf.runcmd(cmd,ropt)
        
    # -- print file that processing has been done
    #
    cmd='touch %s/%s'%(tdir,pfile)
    mf.runcmd(cmd,ropt)
        
        

MF.dTimer(tag='all')

sys.exit()

