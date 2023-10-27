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
            1:['dtgopt',    'no default'],
            }

        self.defaults={
            }

        self.options={
            'verb':          ['V',0,1,'verb=1 is verbose'],
            'doInvestDev':   ['I',0,1,'get the Invest_Developers...default is not...'],
            'doStext':       ['s',1,0,'do NOT get the ships and lsdiag...'],
            'ropt':          ['N','','norun',' norun is norun'],
            'doPzal':        ['P',1,1,'make going to pzal the default 20221001'],
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

# -- run on gmu hopper -- rsync over
#
prcdir=w2.PrcDirTcdatW2

if(w2.onTenki and not(w2.onGmu) and not(doPzal)):
    
    cmd="%s/tc-jtwc-rsync.sh"%(prcdir)
    mf.runcmd(cmd,ropt)
    
    sys.exit()

dtg=mf.dtg_command_prc(dtgopt)

# -- switches
#
doshemoverlap=1
doABdecks=1

mm=dtg[4:6]

if(dtgopt == 'cur'):
    do9Xstms=0
    yyyy=curdtg[0:4]

else:
    yyyy=dtg[0:4]


try:
    (yyyy1,yyyy2)=yyyy.split('.')
    years=range(int(yyyy1),int(yyyy2)+1)
    print 'qqqqq ads',years
except:
    if(yyyy == 'all'):
        years=range(2000,2005)
    else:
        years=[yyyy]

# -- set years to two years to cover shem overlap
#
(shemoverlap,yyyy1,yyyy2)=CurShemOverlap(dtg)

if( shemoverlap and doshemoverlap):
    years=[yyyy1,yyyy2]

# -- do previous year to catch overlap of storms crossing year
#
elif( (yyyy == curyear) and (int(mm) == 1)):
    yyyym1=int(yyyy)-1
    yyyym1=str(yyyym1)
    years=[yyyym1,yyyy]


decks=['adeck','bdeck','edeck','fdeck','tdeck']

asj=w2.JtwcService
af=w2.JtwcFtpserver
al=w2.JtwcLogin
ap=w2.JtwcPasswd

sbdir=w2.JtwcDatDir
tbdir=w2.TcDatDir

if(verb):
    print 'ASJ: ',asj
    print ' AF: ',af
    print ' AL: ',al
    print ' AP: ',ap

tdir="%s/%s"%(tbdir,'jtwc')
mf.ChkDir(tdir,'mk')

if(mf.ChkDir(tbdir,diropt='q') != 0): os.chdir(tdir)
print 'CCC: working in: ',os.getcwd()

# -- get the storm tables
#

if(mf.find(af,'pzal')):

    # -- 20190401 -- Angelo put in nrlhhc/
    
    phpurl='php/m2m/index.php'
    phpurl='php/rds/m2m/index.php' # -- 20191026 -- Angelo set this up?
    
    wgeturl='''https://%s/%s/nrlhhc/storm.table'''%(af,phpurl)
    #wgetopt="""--no-check-certificate --mirror -nd -np -T 15 -t 1 --user %s --password '%s'"""%(al,apf)
    wgetmoz='''-U "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0"'''
    wgetoptBase="""--no-check-certificate --mirror -nd -np -T 15 -t 20 %s --http-user=%s --http-password='%s'"""%(wgetmoz,al,ap)
    wgetmask=""
    wgettarget="-P %s"%(tdir)
    cmd="wget %s %s %s %s"%(wgetoptBase,wgetmask,wgettarget,wgeturl)
    mf.runcmd(cmd,ropt)

    if(mf.find(af,'metoc')):
        wgeturl='''"https://%s/%s/atcf_storms/storms.jtwc_atcfp2"'''%(af,phpurl)
        #wgetopt="""--no-check-certificate --mirror -nd -np -T 60 -t 20 %s --http-user %s --http-password '%s'"""%(wgetmoz,al,ap)
        #wgetopt=""" --mirror -nd -np -T 60 -t 1 --user %s --password '%s'"""%(al,apf)
    else:
        wgeturl='''"https://%s@%s/atcf_storms/storms/storms.jtwc_atcfp2"'''%(apf,af)
        wgetopt="--no-check-certificate --mirror -nd -np -T 60 -t 1"
        
    wgetmask=""
    wgettarget="-P %s"%(tdir)
    cmd="wget %s %s %s %s"%(wgetoptBase,wgetmask,wgettarget,wgeturl)
    mf.runcmd(cmd,ropt)

    # -- 20190401 -- long gone
    #wgeturl='''"https://%s@%s/atcf_storms/storms/storms.npmoc_atcfp2"'''%(apf,af)
    #mf.runcmd(cmd,ropt)

else:

    cmd="wget -m -nd  -T 60 -t 1 \"%s://%s:%s@%s/%s/storm.table\""%(asj,al,ap,af,sbdir)
    mf.runcmd(cmd,ropt)

    cmd="wget -m -nd  -T 60 -t 1 \"%s://%s:%s@%s/%s/storms.txt\""%(asj,al,ap,af,sbdir)
    mf.runcmd(cmd,ropt)


# -- ssssssssssssssssssssssssssssssssssssssssssssss -- stext -- ships/lgem output
#
if(mf.find(af,'metoc') and doStext):
    MF.sTimer('jtwc-stext')
    
    for year in years:
        yymmdd=year[2:4]+dtg[4:8]
        
        tdir="%s/%s"%(w2.TcStextJtwcDir,year)
        mf.ChkDir(tdir,'mk')
        wgeturl='''"https://%s/%s/atcf_storms/shipsout/"'''%(af,phpurl)
        wgetmask='''-A "*%s*"'''%(yymmdd)
        wgettarget="-P %s"%(tdir)
        cmd="wget %s %s %s %s"%(wgetoptBase,wgetmask,wgettarget,wgeturl)
        mf.runcmd(cmd,ropt)


    MF.dTimer('jtwc-stext')



for year in years:

    if(doABdecks == 0): continue

    for deck in decks:
        
        if(mf.find(af,'pzal')):
            sdir="%s"%(sbdir)
            tdir="%s/%s/%s/%s"%(tbdir,deck,'jtwc',year)
        else:
            sdir="%s/%s"%(sbdir,year)
            tdir="%s/%s/%s/%s"%(tbdir,deck,'jtwc',year)

            
        if(mf.ChkDir(tdir,diropt='mk') != 0): os.chdir(tdir)
        print 'CCC: working in: ',os.getcwd()

        # -- dtype from deck
        dtype=deck[0:1]
        

        if(mf.find(af,'pzal')):
            
            wgettarget="-P %s"%(tdir)

            if(mf.find(af,'metoc')):
                wgeturl='''https://%s/%s/atcf_storms/'''%(af,phpurl)
            else:
                wgeturl='''https://%s@%s/atcf_storms/storms/'''%(apf,af)
                wgetopt="--no-check-certificate --mirror -nd -np -l1 -T 60 -t 1"
            
            wgetmask="-A \"%s*%s*dat\""%(dtype,year)
            cmd="wget %s %s %s %s"%(wgetoptBase,wgetmask,wgettarget,wgeturl)
            mf.runcmd(cmd,ropt)

            if(mf.find(af,'metoc')):
                wgeturl='''https://%s/%s/nrlhhc/%s/'''%(af,phpurl,year)
            else:
                wgeturl='''https://%s@%s/nrlhhc/%s/'''%(ap,af,year)

            wgetmask="-A \"%s??[A-Z]?%s*dat\""%(dtype,year)
            cmd="wget %s %s %s %s"%(wgetoptBase,wgetmask,wgettarget,wgeturl)
            mf.runcmd(cmd,ropt)

            # -- 20190401 -- no longer on new collab site -- it is ...
            if(doInvestDev):
                if(mf.find(af,'metoc')):
                    wgeturl='''https://%s/%s/nrlhhc/%s/Invest_Developers/'''%(af,phpurl,year)
                else:
                    wgeturl='''https://%s@%s/nrlhhc/%s/Invest_Developers/'''%(ap,af,year)

                wgetmask="-A \"%s??[A-Z]?%s*dat\""%(dtype,year)
                cmd="wget %s %s %s %s"%(wgetoptBase,wgetmask,wgettarget,wgeturl)
                mf.runcmd(cmd,ropt)

            
        else:
            cmd="wget -m -nd -T 180 -t 2 \"%s://%s:%s@%s/%s/%s*dat\""%(asj,al,ap,af,sdir,dtype)
            mf.runcmd(cmd,ropt)

# wget -m -nd "ftp://atcfp1:atcfp112@198.97.80.42//opt/DEVELOPMENT/atcf/archives/2004/[a,b]*dat"

MF.dTimer(tag='all')

sys.exit()

