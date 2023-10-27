#!/usr/bin/env python

from tcbase import *
from tcswitches import *

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
            'usearchive':    ['a',0,1,'usearchive'],
            'yearopt':       ['y:',None,'a','yearopt'],
            'doallDecks':    ['A',0,1,'doallDecks'],
            'doBdecksOnly':  ['B',0,1,'doBdecksOnly -- only grab bdecks'],
            'store_invest':  ['s',0,1,'use store_invest dir'],
            'verb':          ['V',0,1,'verb=1 is verbose'],
            'ropt':          ['N','','norun',' norun is norun'],
            }

        self.purpose='''
purpose -- mirror a/b/e/fdecks from nhc to local
%s cur
'''
        self.examples='''
%s cur
'''




#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# main

MF.sTimer(tag='all')

argv=sys.argv
CL=MssCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr
MF.dTimer(tag='all')


dtTimeCheckMin=-4.5

# -- switches
#
dodis=dodisNHC
docom=docomNHC
dostext=dostextNHC

if(usearchive): docom=0 ; dostext=0

(dtg,phr)=mf.dtg_phr_command_prc(dtgopt) 

if(dtgopt == 'cur'):
    do9Xstms=0
    yyyy=curdtg[0:4]
    mm=curdtg[4:6]

elif(dtg[0:4] == curyear):
    yyyy=curyear
    mm=dtg[4:6]

else:
    yyyy=dtg[0:4]
    if(len(dtg) >= 6):
        mm=dtg[4:6]
    else:
        mm=-999

if(len(dtg) >= 8):
    dd=dtg[6:8]
else:
    dd=-9999

try:
    (yyyy1,yyyy2)=yyyy.split('.')
    years=range(int(yyyy1),int(yyyy2)+1)
except:
    if(yyyy == 'all'):
        years=range(2000,2005)
    else:
        years=[yyyy]

###################### bypass for nhc
#
# set years to two years to cover shem overlap
#
#(shemoverlap,yyyy1,yyyy2)=tc2.CurShemOverlap(curdtg)
#
#if( (yyyy == curyear) and shemoverlap):
#    years=[yyyy1,yyyy2]

# -- do previous year to catch overlap of storms crossing year
#
#elif( (yyyy == curyear) and (int(mm) == 1 and int(dd) <= 20) ):
if( (yyyy == curyear) and (int(mm) == 1 and int(dd) <= 20) ):
    yyyym1=int(yyyy)-1
    yyyym1=str(yyyym1)
    years=[yyyym1,yyyy]

if(yearopt != None):
    if(mf.find(yearopt,',')):
        years=yearopt.split(',')
    elif(mf.find(yearopt,'-')):
        byear,eyear=yearopt.split('-')
        years=range(int(byear),int(eyear)+1)

decks=['adeck','bdeck','edeck','fdeck','adeckjtwc']
# 20100204 -- bypass special for jtwc from nhc
decks=['adeck.aid','adeck','bdeck','edeck','fdeck']
decks=['adeck','bdeck','edeck','fdeck']


if(doallDecks):
    decks=['adeck','bdeck','edeck','fdeck']
else:
    decks=['adeck','bdeck','adeck.aid','adeck.pub']
    decks=['adeck.pub','bdeck']
    # -- server is slow just, go after a/bdecks
    decks=['adeck','bdeck']
    decks=['adeck.pub','bdeck','edeck','fdeck']

sbdir=w2.NhcDatDir
tbdir=w2.TcDatDir
wgetopt='-m -nd -T 180 -t 2 -nv'
wgetopt='-m -nd -T 5 -t 1 -v'  # turn off the verbose

print 'NNNHHHCCC doing years: ',years,' decks: ',decks

for year in years:

    if(int(year) <= 2004 and dtgopt != 'cur'): usearchive=1 

    if(usearchive):
        decks=['adeck','bdeck']
        
    if(doBdecksOnly):
        decks=['bdeck']
        
    for deck in decks:

        af=w2.NhcFtpserver
        al=w2.NhcLogin
        ap=w2.NhcPasswd

        if(deck == 'adeck.aid'):  dtype='a'
        if(deck == 'adeck.pub'):  dtype='a'

        if(deck == 'adeck'): dtype='a'
        if(deck == 'bdeck'): dtype='b'
        if(deck == 'edeck'): dtype='e'
        if(deck == 'fdeck'): dtype='f'
        if(deck == 'adeckjtwc'): dtype='a'

        # -- final
        #
        if(usearchive):
            sdir="%s/archive/%s"%(sbdir,year)
            if(deck == 'adeck'):
                if(store_invest and year >= 2012):  sdir="%s/invests"%(sdir)
            elif(deck == 'bdeck'):
                if(store_invest and year >= 2012):  sdir="%s/invests"%(sdir)
            elif(deck == 'fdeck'):
                if(store_invest and year >= 2012):  sdir="%s/invests"%(sdir)
            elif(deck == 'edeck'):
                if(store_invest and year >= 2012):  sdir="%s/invests"%(sdir)

                
        # -- operational
        #
        else:
            if(deck == 'adeck.aid'):
                sdir="%s/aid"%(sbdir)
                if(store_invest and year <= 2010):  sdir="%s/archive/store_invest/aid"%(sbdir)
                if(store_invest and year >= 2011):  sdir="%s//store_invest/aid"%(sbdir)
                
            elif(deck == 'adeck'):
                sdir="%s/aid"%(sbdir)
                if(store_invest and year <= 2010):  sdir="%s/archive/store_invest/aid"%(sbdir)
                if(store_invest and year >= 2011):  sdir="%s//store_invest/aid"%(sbdir)

            elif(deck == 'adeck.pub'):
                sdir="%s/aid_public"%(sbdir)
                if(store_invest and year <= 2010):  sdir="%s/archive/store_invest/aid"%(sbdir)
                if(store_invest and year >= 2011):  sdir="%s/store_invest/aid"%(sbdir)

            elif(deck == 'adeckjtwc'):
                af='moonfish.nhc.noaa.gov'
                al='jtwc'
                sdir="ncep-special"

            elif(deck == 'bdeck'):
                if(curdtg > 2006040100 and year == '2005'):  sdir="%s/btk.final"%(sbdir)
                else:                                        sdir="%s/btk"%(sbdir)
                if(store_invest and year <= 2010):  sdir="%s/archive/store_invest/btk"%(sbdir)
                if(store_invest and year >= 2011):  sdir="%s/store_invest/btk"%(sbdir)

            elif(deck == 'fdeck'):
                sdir="%s/fix"%(sbdir)
                if(store_invest and year <= 2010):  sdir="%s/archive/store_invest/fix"%(sbdir)
                if(store_invest and year >= 2011):  sdir="%s/store_invest/fix"%(sbdir)

            elif(deck == 'edeck'):
                sdir="%s/gpce"%(sbdir)

        if(deck == 'adeck.aid' or deck == 'adeck.pub'):
            tdir="%s/%s/%s/%s"%(tbdir,'adeck','nhc',year)
        else:
            tdir="%s/%s/%s/%s"%(tbdir,deck,'nhc',year)

        # -- from 2009-2012, follow jwtc naming and in YYYY/invests/ dir
        # -- put to normal tdir
        #
        #if(store_invest): tdir="%s/%s/%s/store_invest"%(tbdir,deck,'nhc')

        if(mf.ChkDir(tdir,diropt='mk') != 0): os.chdir(tdir)
        print 'CCC: working in: ',os.getcwd()



        if(deck == 'adeckjtwc'):
            #wget -m -nd -T 180 -t 2 -nv "ftp://jtwc@moonfish.nhc.noaa.gov:/ncep-special/*"
            cmd="wget %s \"ftp://%s@%s:/%s/*\""%(wgetopt,al,af,sdir)
            mf.runcmd(cmd,ropt)

        elif(deck == 'adeck.aid'):

            cmd="wget %s \"ftp://%s/%s/%sal*%s*.dat\""%(wgetopt,af,sdir,dtype,year)
            mf.runcmd(cmd,ropt)
            #
            #cmd="wget %s \"ftp://%s/%s/%ssl*%s*.dat\""%(wgetopt,af,sdir,dtype,year)
            #mf.runcmd(cmd,ropt)

            cmd="wget %s \"ftp://%s/%s/%scp*%s*.dat\""%(wgetopt,af,sdir,dtype,year)
            mf.runcmd(cmd,ropt)

            cmd="wget %s \"ftp://%s/%s/%sep*%s*.dat\""%(wgetopt,af,sdir,dtype,year)
            mf.runcmd(cmd,ropt)
            print

        else:

            cmd="wget %s \"ftp://%s/%s/%sal*%s*.dat*\""%(wgetopt,af,sdir,dtype,year)
            #cmd="wget %s \"ftp://%s/%s/%sal*%s*.dat\""%(wgetopt,af,sdir,dtype,year)
            mf.runcmd(cmd,ropt)

            # -- south lant
            #
            #cmd="wget %s \"ftp://%s/%s/%ssl*%s*.dat*\""%(wgetopt,af,sdir,dtype,year)
            #mf.runcmd(cmd,ropt)

            cmd="wget %s \"ftp://%s/%s/%scp*%s*.dat*\""%(wgetopt,af,sdir,dtype,year)
            #cmd="wget %s \"ftp://%s/%s/%scp*%s*.dat\""%(wgetopt,af,sdir,dtype,year)
            mf.runcmd(cmd,ropt)

            cmd="wget %s \"ftp://%s/%s/%sep*%s*.dat*\""%(wgetopt,af,sdir,dtype,year)
            #cmd="wget %s \"ftp://%s/%s/%sep*%s*.dat\""%(wgetopt,af,sdir,dtype,year)
            mf.runcmd(cmd,ropt)
            print

        # -- uncompress adeck; if not in plain dir aid/
        #
        plain=glob.glob("%s/*.dat"%(tdir))
        gzs=glob.glob("%s/*gz"%(tdir))
        for gz in gzs:
            (gzu,gzext)=os.path.splitext(gz)
            dti=MF.PathModifyTimeCurdiff(gz)
            
            if(not(gzu in plain) or (dti > dtTimeCheckMin) or alwaysGunzip):
                print 'GGGG gunziping .gz in: ',tdir,'and not in aid/:',gzu,' or alwaysGunzip: ',alwaysGunzip
                # -- better way to unzip that preserves time-stamp
                #
                gzuSAV="%s-SAV"%(gz)
                cmd="cp -p %s %s; gzip -f -d %s ; mv %s %s"%(gz,gzuSAV,gz,gzuSAV,gz)
                #mf.runcmd(cmd,'quiet')
                mf.runcmd(cmd,'')


    af=w2.NhcFtpserver
    al=w2.NhcLogin
    ap=w2.NhcPasswd

    tdir="%s/%s"%(tbdir,'nhc')
    mf.ChkDir(tdir,'mk')

    if(mf.ChkDir(tbdir,diropt='q') != 0): os.chdir(tdir)
    print 'CCC: working in: ',os.getcwd()

    # -- always get the storm.table from nhc
    #
    cmd="wget %s \"ftp://%s/%s/archive/storm.table\""%(wgetopt,af,sbdir)
    mf.runcmd(cmd,ropt)

    cmd="wget %s \"ftp://%s/%s/index/storm*\""%(wgetopt,af,sbdir)
    mf.runcmd(cmd,ropt)

    if(docom):
        # com
        #
        tdircom="%s/%s"%(w2.TcComNhcDir,year)
        sdir="%s/com"%(sbdir)
        mf.ChkDir(tdircom,'mk')
        mf.ChangeDir(tdircom)

        cmd="wget %s \"ftp://%s/%s/*%s*.com*\""%(wgetopt,af,sdir,year)
        mf.runcmd(cmd,ropt)

    if(dodis):
        # dis(cussion)
        #
        tdirdis="%s/%s"%(w2.TcDisNhcDir,year)
        sdir="%s/dis"%(sbdir)
        mf.ChkDir(tdirdis,'mk')
        mf.ChangeDir(tdirdis)

        cmd="wget %s \"ftp://%s/%s/*%s*\""%(wgetopt,af,sdir,year)
        mf.runcmd(cmd,ropt)

        cmd="wget %s \"ftp://%s/%s/CPHC/*%s*\""%(wgetopt,af,sdir,year)
        mf.runcmd(cmd,ropt)


    if(dostext):
        # -- stext -- ships/lgem output
        #
        tdir="%s/%s"%(w2.TcStextNhcDir,year)
        sdir="%s/stext"%(sbdir)
        mf.ChkDir(tdir,'mk')
        mf.ChangeDir(tdir)
        
        cmd="wget %s \"ftp://%s/%s/%s*_ships*\""%(wgetopt,af,sdir,year[2:4])
        mf.runcmd(cmd,ropt)


sys.exit()

