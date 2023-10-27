#!/usr/bin/env python

from tcbase import *

#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
#
# command line setup
#

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
            'verb':          ['V',0,1,'verb=1 is verbose'],
            'ropt':          ['N','','norun',' norun is norun'],
            'doDatMv':       ['M',0,1,'mv existing into the working dir'],
            'doBdeck2':      ['2',1,0,'do NOT do bdeck2 -- bdeck2 is a separate archive'],
            }

        self.purpose='''
purpose -- mirror a/b/e/fdecks from jtwc to local
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

tt=yearopt.split('.')

if(len(tt) == 2):
    byear=tt[0]
    eyear=tt[1]
    years=mf.yyyyrange(byear, eyear)
    oyearOpt="%s-%s"%(byear,eyear)

elif(len(tt) == 1):

    years=[yearopt]
    oyearOpt=yearopt

else:
    print 'EEE -- invalid yearopt: ',yearopt



doBdeck2=1

deck='bdeck'
if(doBdeck2):
    deck='bdeck2'

asj=w2.JtwcService
af=w2.JtwcFtpserver
al=w2.JtwcLogin
ap=w2.JtwcPasswd


sbdir=w2.JtwcDatDir
tbdir=w2.TcDatDir

tdir="%s/%s"%(tbdir,'jtwc')
mf.ChkDir(tdir,'mk')


basins=['sh','io','wp']
#basins=['wp']

roptWget=ropt

dowget=1
useZipArchive=1

if(not(dowget)): roptWget='norun'

for year in years:
    
    for basin in basins:
            
        if(mf.find(af,'pzal')):
            sdir="%s"%(sbdir)
            tdir="%s/%s/%s/%s"%(tbdir,deck,'jtwc',year)
            tdirWorking="%s/working"%(tdir)
            tdirFinal="%s/final"%(tdir)
            print 'qqq',tdir
            if(not(doBdeck2)):
                MF.ChkDir(tdirWorking,'mk')
                MF.ChkDir(tdirFinal,'mk')
            
        else:
            sdir="%s/%s"%(sbdir,year)
            tdir="%s/%s/%s/%s"%(tbdir,deck,'jtwc',year)
    
    
        if(mf.ChkDir(tdir,diropt='mk') != 0): os.chdir(tdir)
        print 'CCC: working in: ',os.getcwd()
    
        if(deck == 'adeck'): dtype='a'
        if(deck == 'bdeck' or deck == 'bdeck2'): dtype='b'
    
        wgetmaskDat="%s%s[0-9]?%s.dat"%(dtype,basin,year)
        wgetmaskDatAll="%s%s??%s.dat"%(dtype,basin,year)
        wgetmaskTxt="%s%s[0-9]?%s.txt"%(dtype,basin,year)
    
        # -- mv current .dat to working/
        #
        if(doDatMv):
            cmd="mv -n %s/%s %s/."%(tdir,wgetmaskDatAll,tdirWorking)
            mf.runcmd(cmd,ropt)
    
        wgetopt="--no-check-certificate --mirror -nd -np -l1 -T 60 -t 1"
    
        # -- older method
        #
        wgettarget="-P %s"%(tdir)
        wgeturl='''http://www.usno.navy.mil/NOOC/nmfc-ph/RSS/jtwc/best_tracks/%s/%ss-b%s/'''%(year,year,basin)
        if(int(year) <= 2010):
            wgetmask="-A \"%s\""%(wgetmaskTxt)
        else:
            wgetmask="-A \"%s\""%(wgetmaskDat)
    
        # -- new server 20160615
        #
        if(useZipArchive):
            if(doBdeck2):
                wgettarget="-P %s"%(tdir)
            else:
                wgettarget="-P %s"%(tdirFinal)
            wgeturl='''https://metoc.ndbc.noaa.gov/ProductFeeds-portlet/img/jtwc/best_tracks/%s/%ss-b%s/b%s%s.zip'''%(year,year,basin,basin,year)
            wgeturl='''https://www.metoc.navy.mil/jtwc/products/best-tracks/%s/%ss-b%s/b%s%s.zip'''%(year,year,basin,basin,year)
            wgetmask=''
            
        cmd="wget %s %s %s %s"%(wgetopt,wgetmask,wgettarget,wgeturl)
        mf.runcmd(cmd,roptWget)
    
        if(useZipArchive):
            #and not(doDatMv)):
        
            if(doBdeck2):
                cmd="unzip -n -d . b%s%s.zip"%(basin,year)
            else:
                cmd="unzip -n -d . final/b%s%s.zip"%(basin,year)
            mf.runcmd(cmd,ropt)
           
            if(int(year) <= 2010):
                bdecks=glob.glob("%s/%s"%(tdir,wgetmaskTxt))
            else:
                bdecks=glob.glob("%s/%s"%(tdir,wgetmaskDat))
                
            for bdeck in bdecks:
                
                if(int(year) <= 2010):
                    (bdir,bfile)=os.path.split(bdeck)
                    (bbase,bext)=os.path.splitext(bfile)
                    bdeckDat="%s/%s.dat"%(bdir,bbase)
                
                    cmd="mv %s %s"%(bdeck,bdeckDat)
                    mf.runcmd(cmd,ropt)
                else:
                    bdeckDat=bdeck  
            
            
        else:
            
            #  relabel .txt to .dat if <= 2010; otherwise fill final/ with these bdecks
            #
            if(int(year) <= 2010):
                bdecks=glob.glob("%s/%s"%(tdir,wgetmaskTxt))
            else:
                bdecks=glob.glob("%s/%s"%(tdir,wgetmaskDat))
                
            for bdeck in bdecks:
                
                if(int(year) <= 2010):
                    (bdir,bfile)=os.path.split(bdeck)
                    (bbase,bext)=os.path.splitext(bfile)
                    bdeckDat="%s/%s.dat"%(bdir,bbase)
                
                    cmd="mv %s %s"%(bdeck,bdeckDat)
                    mf.runcmd(cmd,ropt)
                else:
                    bdeckDat=bdeck  
    
                cmd="cp %s %s/."%(bdeckDat,tdirFinal)
                mf.runcmd(cmd,ropt)
    
        

MF.dTimer(tag='all')

sys.exit()

