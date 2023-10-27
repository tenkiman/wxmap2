#!/usr/bin/env python

from tcbase import *
from tcswitches import *

rsyncopt29='--timeout=30 --protocol=29'

class TcOpsCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv

        self.argv=argv

        self.argopts={
            1:['dtgopt',    'no default'],
        }

        self.defaults={
        }

        self.options={
            'ropt':            ['N','','norun',' norun is norun'],
            'verb':            ['V',0,1,'verb=1 is verbose'],
            'override':        ['O',0,1,'override'],
            'domirror':        ['M',1,0,'doNOT mirror'],
            'chkNhcJtwcAdeck': ['J',0,1,'do chk NHC/JTWC a|bdecks in epac'],
            'doforecall':      ['F',0,1,'doforecall'],
            'dotcvitalsonly':  ['v',0,1,'dotcvitalsonly'],
            'dobdecksonly':    ['B',0,1,'dobdecksonly'],
            'doreftrkonly':    ['R',0,1,'doreftrkonly'],
            'dogrepnceponly':  ['n',0,1,''],
            'domtcswa':        ['C',1,0,'doNOT mirror over cira mtcswa'],
            'doeps':           ['E',0,1,'DO tigge eps'],
            'doepsAdeck':      ['A',0,1,'use Adeck (-A) for ncep & cmc'],
            'doAd2':           ['2',1,0,'do NOT run ad2 in otc'],
            'doATCFonly':      ['a',0,1,'only do ATCF processsing...'],
            'doEpsOnly':       ['e',0,1,'do tigge eps ONLY...'],
            'dochkIfRunning':  ['o',1,0,'do NOT chkifrunning in M.DataSets MF.chkIfFileIsOpen'],

        }

        self.purpose='''
master script to do all ops tc processing...
'''
        self.examples='''
%s ops
'''


MF.sTimer('all')

argv=sys.argv
CL=TcOpsCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

# -- get command line vars, except -N
pyfileopt=''
for s in sys.argv[1:]:
    if(s != '-N'):
        pyfileopt='%s %s'%(pyfileopt,s)

if(ropt == 'norun'): dochkIfRunning=0
#ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc -- check if job is running and .pypdb may be open...
#
if(dochkIfRunning):

    # -- still getting conflicts when doing updating -- corrupts either zipfile or pypdb
    #    current config
    #jobopt=pyfileoptc
    #killjob=1
    #    new config -- wait five minutes before bailing -- don't depend on jobopt
    # -- go back to old settings?
    jobopt=pyfileopt.split()[0]
    # -- this causes a big problem when more than one adk is running -- from fp2 -T
    #killjob=0
    killjob=1

    MF.sTimer('tcops-chkIfJobIsRunning pyfile: %s jobopt: %s killjob: %s'%(pyfile,jobopt,killjob))
    rc=MF.chkRunning(pyfile,strictChkIfRunning=1,
                     killjob=killjob,verb=verb,nminWait=1,timesleep=5)
    MF.dTimer('tcops-chkIfJobIsRunning pyfile: %s jobopt: %s killjob: %s'%(pyfile,jobopt,killjob))



idtgopt=dtgopt
if(dtgopt == 'ops'): idtgopt='cur'
dtgs=mf.dtg_dtgopt_prc(idtgopt)

doOps=(dtgopt == 'ops')

if(dtgopt != 'ops'):
    docuradeck=0

# -- defaults mirrormit was 1 if not set!
#
domirrormit=0
domirrorwjetNcep=0

# -- 20211013 -- turn off after hopper came back from big network down time
# -- 20211014 -- back on...pzal back
#
domirrorjtwc=1

if(domirror == 0):
    domirrornhc=0
    domirrorjtwc=0
    domirrorwjet=0
    domirrortacc=0
    domirrormit=0
    doAd2=0

if(doEpsOnly):
    domirrornhc=0
    domirrorjtwc=0
    domirrorwjet=0
    w2.W2doW3RapbNcepCmcAdecks=0    
    w2.W2doW3RapbRtfimAdecks=0
    dopostmdeck=0
    domtcswa=0
    doeps=1
    doOps=1
    doAd2=1

# -- do here because don't want to override settings from tcswitches.py and w2switches.py
#
if(w2.onTenki or w2.onGmu):
    domirror=0

domirrorwjet=0

scpserver='jetscp.rdhpcs.noaa.gov'
w3tdir=w2.TcvitalsDirW3
datprcdir=w2.PrcDirTcdatW2
prctcbogdir=w2.PrcDirTcbogW2
datww3dir=w2.PrcDirTcww3W2


#
# mech to run sequence of dtgs...
#
if(len(dtgs) > 1):

    for dtg in dtgs:
        cmd="%s %s"%(pyfile,dtg)
        for o,a in CL.opts:
            cmd="%s %s %s"%(cmd,o,a)
        mf.runcmd(cmd,ropt)


    sys.exit()

curdtgms=mf.dtg('dtg_ms')

# cd to prc dir to pick up ex- files that exclude data from rsync
#
mf.ChangeDir(datprcdir)

#vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv -- vitals
#
if(dotcvitalsonly):

    for dtg in dtgs:
        md2aOpt=''
        cmd="w2-tc-dss-md2-anl.py -d %s -v %s"%(dtg,md2aOpt)
        mf.runcmd(cmd,ropt)

    sys.exit()

if(doOps):

    #mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm------------------ mirroring
    #
    # -- first the operational abdecks... and storm files

    if(domirrornhc):

        MF.sTimer('TCOPS:mirrornhc ')

        # -- get main decks
        #
        cmd="w2-tc-wget-mirror-nhc-abdeck-2-local.py cur"
        mf.runcmd(cmd,ropt)

        # -- now do -s to get 9X in store_invest dir
        #
        cmd="w2-tc-wget-mirror-nhc-abdeck-2-local.py cur -s"
        mf.runcmd(cmd,ropt)

        if(ropt == ''): MF.dTimer('TCOPS:mirrornhc ')

    if(domirrorjtwc):

        MF.sTimer('TCOPS:mirrortwc ')

        cmd="w2-tc-wget-mirror-jtwc-abdeck-2-local.py cur "  # -- 20221001 -- make pzal the default :: 22020406 -- mirroring directly from pzal working now...
        mf.runcmd(cmd,ropt)

        if(ropt == ''): MF.dTimer('TCOPS:mirrortwc ')


    MF.sTimer('TCOPS:mirrorALL ')

    #nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn
    #
    # update names
    #

    if(not(doEpsOnly)): 

        cmd="w2-tc-names.py  cur"
        mf.runcmd(cmd,ropt)

        #dddddddddddddddddddddddddddddddddddddddddddddddddd
        #
        # create final local BT and AD and MD
        #

        MF.sTimer('TCOPS:a,b,mdeck final ')
        dtgoptfinal='ops'
        if(dtgopt == 'cur' or dtgopt == 'ops'): dtgoptfinal='ops'

        cmd="w2-tc-bt-adeck-final.py %s"%(dtgoptfinal)
        mf.runcmd(cmd,ropt)

        cmd="w2-tc-bt-bdeck-final.py %s"%(dtgoptfinal)
        mf.runcmd(cmd,ropt)

        cmd="w2-tc-bt-mdeck-final.py %s"%(dtgoptfinal)
        mf.runcmd(cmd,ropt)
        if(ropt == ''): MF.dTimer('TCOPS:a,b,mdeck final ')



if(ropt == 'norun' and not(doEpsOnly)): dopostmdeck=1

if(dopostmdeck):

    shemyear=getShemYear(curdtg)

    #ddddddddddddddddddddddddddddddddddddddddddddddd -- old mdeck as .pypdb
    #
    mdkOpt=''
    cmd="%s/w2-tc-dss-mdeck.py -y cur %s"%(datprcdir,mdkOpt)
    mf.runcmd(cmd,ropt)

    #ddddddddddddddddddddddddddddddddddddddddddddddd -- new mdeck2 as .pypdb
    #
    md2Opt=''
    if(chkNhcJtwcAdeck): md2Opt='-J'
    cmd="%s/w2-tc-dss-md2.py -u %s"%(datprcdir,md2Opt)
    mf.runcmd(cmd,ropt)

    #pppppppppppppppppppppppppppppppppppppppppppppppppp
    #
    # do posits for trackers...
    # create btops and map9x (9X->XX) cards in carq dir 
    #
    MF.sTimer('TCOPS:posits ')
    for dtg in dtgs:

        dtgm6=mf.dtginc(dtg,-6)
        dtgm12=mf.dtginc(dtg,-12)

        # -- do tc posits
        #
        cmd="w2-tc-posit.py %s -C"%(dtg)
        mf.runcmd(cmd,ropt)

        cmd="w2-tc-posit.py %s -C"%(dtgm6)
        mf.runcmd(cmd,ropt)

        # -- make tcvitals using new mdeck2 -- does scp and cp 
        #
        md2aOpt=''
        cmd="w2-tc-dss-md2-anl.py -d %s -v %s"%(dtgm6,md2aOpt)
        mf.runcmd(cmd,ropt)

        cmd="w2-tc-dss-md2-anl.py -d %s -v %s"%(dtg,md2aOpt)
        mf.runcmd(cmd,ropt)

        if(ropt == ''): MF.dTimer('TCOPS:posits ')


    #aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa -- do carq adeck
    #
    cmd="w2-tc-dss-adeck.py carq -y %s -u"%(curyear)
    mf.runcmd(cmd,ropt)

    if(shemyear != curyear):
        cmd="w2-tc-dss-adeck.py carq -y %s -u"%(shemyear)
    mf.runcmd(cmd,ropt)

    if(doATCFonly):
        print 'III--- stop doATCFonly...'
        MF.dTimer('all')
        sys.exit()


#eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
#
# get eps plots...and tigge trackers...convert to wxmmap...only if ops
# and after bdecks
#

doingOps=0

if(doOps):
    doingOps=1
    if(doEpsOnly): doingOps=0

    # -- always make tcvitals using new mdeck2 -- does scp and cp as well,
    #    to keep the vitals hot; redundant if dopostmdeck
    #
    if(not(doEpsOnly) and not(dopostmdeck)):
        md2aOpt=''
        cmd="w2-tc-dss-md2-anl.py -d %s -v %s"%(dtgs[0],md2aOpt)
        mf.runcmd(cmd,ropt)



    #MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
    # MTCSWA -- cira multi-platform TC sfc wind analysis
    #
    # -- 20181112 -- turnoff -- bugs? -- fixed
    #domtcswa=0
    if(domtcswa):

        MF.sTimer('TCOPS:wget.mtcswa ')
        curopt='cur'
        fphr=mf.dtg('fphr')
        if(fphr < 1.5): curopt='cur-6'

        # -- this only pull the .png
        #
        cmd="w2-tc-wget-http-mirror-cira-mtcswa.py %s"%(curopt)
        mf.runcmd(cmd,ropt)

        # -- 20230605 -- pull .nc files with data
        #
        cmd="w2-tc-wget-http-mirror-cira-mtcswa2.py %s"%(curopt)
        mf.runcmd(cmd,ropt)
        if(ropt == ''): MF.dTimer('TCOPS:wget.mtcswa ')
    
    # -- 20230607 -- keeps failing in .crontab -- do here
    #
    if(doAd2):

        ad2Opt=''
        if(chkNhcJtwcAdeck): ad2Opt='-J'
        cmd="w2-tc-dss-ad2.py jt -d cur-24.cur %s"%(ad2Opt)
        mf.runcmd(cmd,ropt)
        
        cmd="w2-tc-dss-ad2.py jt,gefs,ukmo -d cur-24.cur -9 %s"%(ad2Opt)
        mf.runcmd(cmd,ropt)


    if(doeps):

        #eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
        # get ecmwf eps plots
        #

        # -- 20150717 -- problem with ecmwf network?
        # -- 20181030 -- use wmo-essential bufr vice tigge
        #
        doECMWFeps=0

        #tttttttttttttttttttttttttttttttttttttttttttttttttt
        # tigge xml -> adeck -- has built in check if already cracked
        # runs w2-tc-g-epsanal.py and w2-tc-inventory-epsanal.py after cracked and for the 'all' options
        #
        xml2adeckopt='-G'
        if(w2.W2doTcepsAnl): xml2adeckopt=''

        if(doECMWFeps):
            cmd="%s/w2-tc-tigge-xml-2-wxmap-adecks.py cur12-24 ecmwf ecmt %s"%(datprcdir,xml2adeckopt)
            mf.runcmd(cmd,ropt)
            cmd="%s/w2-tc-tigge-xml-2-wxmap-adecks.py cur12-24 ecmwf all %s"%(datprcdir,xml2adeckopt)
            mf.runcmd(cmd,ropt)

            cmd="%s/w2-tc-tigge-xml-2-wxmap-adecks.py cur12-12 ecmwf ecmt %s"%(datprcdir,xml2adeckopt)
            mf.runcmd(cmd,ropt)
            cmd="%s/w2-tc-tigge-xml-2-wxmap-adecks.py cur12-12 ecmwf all %s"%(datprcdir,xml2adeckopt)
            mf.runcmd(cmd,ropt)

            cmd="%s/w2-tc-tigge-xml-2-wxmap-adecks.py ops12 ecmwf ecmt %s"%(datprcdir,xml2adeckopt)
            mf.runcmd(cmd,ropt)
            cmd="%s/w2-tc-tigge-xml-2-wxmap-adecks.py ops12 ecmwf all %s"%(datprcdir,xml2adeckopt)
            mf.runcmd(cmd,ropt)

        # ncep xml tigge is down... use standard adecks form nhc
        # 20100711 -- ncep xml tigge is back; set TcTcepsNcepSource='tigge' in w2switches
        #
        if(mf.find(w2.TcTcepsNcepSource,'tigge')):
            adeckOpt=''
            if(doepsAdeck): adeckOpt='-A'
            cmd="%s/w2-tc-tigge-xml-2-wxmap-adecks.py ops6 ncep gfst %s"%(datprcdir,xml2adeckopt)
            mf.runcmd(cmd,ropt)
            cmd="%s/w2-tc-tigge-xml-2-wxmap-adecks.py ops6 ncep all %s %s"%(datprcdir,xml2adeckopt,adeckOpt)
            mf.runcmd(cmd,ropt)
            cmd="%s/w2-tc-tigge-xml-2-wxmap-adecks.py ops12 cmc cmct %s"%(datprcdir,xml2adeckopt)
            mf.runcmd(cmd,ropt)
            cmd="%s/w2-tc-tigge-xml-2-wxmap-adecks.py ops12 cmc all %s %s"%(datprcdir,xml2adeckopt,adeckOpt)
            mf.runcmd(cmd,ropt)

        elif(w2.TcTcepsNcepSource == 'adeck'):
            cmd="%s/w2-tc-g-epsanal.py ops6 ncep"%(datprcdir)
            mf.runcmd(cmd,ropt)

            cmd="%s/w2-tc-g-epsanal.py ops12 cmc"%(datprcdir)
            mf.runcmd(cmd,ropt)

        elif(w2.TcTcepsNcepSource == 'adeckonly'):
            cmd="%s/w2-tc-g-epsanal.py ops6 ncep -A"%(datprcdir)
            mf.runcmd(cmd,ropt)

            cmd="%s/w2-tc-g-epsanal.py ops12 cmc -A"%(datprcdir)
            mf.runcmd(cmd,ropt)

        elif(w2.TcTcepsNcepSource == 'ad2'):

            dtgoptN='ops6'
            dtgoptC='ops12'
            dtgoptE='ops12'

            if(idtgopt != 'ops' and idtgopt != 'cur'): dtgoptN=dtgoptC=dtgoptE=idtgopt
            cmd="%s/w2-tc-g-epsanal-dss-ad2.py %s ncep "%(datprcdir,dtgoptN)
            mf.runcmd(cmd,ropt)

            cmd="%s/w2-tc-g-epsanal-dss-ad2.py %s cmc "%(datprcdir,dtgoptC)
            mf.runcmd(cmd,ropt)

            if(doECMWFeps == 0):
                cmd="%s/w2-tc-g-epsanal-dss-ad2.py %s ecmb "%(datprcdir,dtgoptE)
                mf.runcmd(cmd,ropt)

        # -- 20180825 -- use ad2 for mogreps
        #
        if(w2.TcTcepsNcepSource != 'ad2'):
            cmd="%s/w2-tc-g-epsanal-dss-ad2.py ops12 ukmo "%(datprcdir)
            mf.runcmd(cmd,ropt)
        else:
            # -- 20150707
            dtgoptU='ops12'
            if(idtgopt != 'ops' and idtgopt != 'cur'): dtgoptU=idtgopt
            cmd="%s/w2-tc-wget-mirror-tigge-2-local.py %s ukmo"%(datprcdir,dtgoptU)
            mf.runcmd(cmd,ropt)

            cmd="%s/w2-tc-tigge-xml-2-wxmap-adecks.py %s ukmo all"%(datprcdir,dtgoptU)
            mf.runcmd(cmd,ropt)


MF.dTimer('all')
