#!/usr/bin/env python

from tcbase import *

#llllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll
# local defs
#

def GetNesdisStm2id(stmid,dtg):

    b1id=stmid[2]
    b2id=Basin1toBasin2[b1id]
    stm1id=stmid.split('.')[0].lower()
    year=stmid.split('.')[1]
    yearS=year
    if(isShemBasinStm(stmid)):
        (shemoverlap,cy,cyp1)=CurShemOverlap(dtg)
        yearS=cyp1
        if(not(shemoverlap)): yearS=cy

    stm2id=b2id+stmid[0:2]+yearS

    return(yearS,year,stm1id,stm2id)

#
# bugs in .ctl from nesdis...
#
def FixCtl(ctlpath,verb=1):

    cards=open(ctlpath).readlines()
    if(len(cards) == 0): 
        print 'WWW(w2.tc.wget.mirror.cira.mtcswa.py.FixCtl -- no cards in ctlpath: ',ctlpath,' press...'
        return

    (dir,file)=os.path.split(ctlpath)
    (base,ext)=os.path.splitext(file)

    for n in range(0,len(cards)):
        card=cards[n]
        if(n == 0):
            if(mf.find(card,'grad.bin')):
                card=card.replace('grad.bin',"%s.bin"%(base))
            ictl=card[:-1]
        else:
            ictl="""%s
%s"""%(ictl,card[:-1])
        if(n == 2):
            ictl="""%s
options big_endian"""%(ictl)

    if(verb): print 'fixing: ',ctlpath

    mf.WriteCtl(ictl,ctlpath)
    return




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
            'stmopt':          ['s:',None,'a','stmopt'],
            'dochkIfRunning':  ['o',1,0,'do NOT chkifrunning in MFutils.chkIfJobIsRunning'],
        }

        self.purpose='''
mirror MTCSWA (Multi-platform Tropical Cyclone Surface Wind Analysis) from nesdis.cira to local'''

        self.examples='''
%s cur  -s l,w    : get all current year lant and wpac storms
%s 2004010100     : pull from archive dir for 2004'''


MF.sTimer('all')

argv=sys.argv
CL=TcOpsCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

if(ropt == 'norun'): dochkIfRunning=0
#ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc -- check if job is running and .pypdb may be open...
#
if(dochkIfRunning):
    # -- get command line vars, except -N
    pyfileopt=''
    for s in sys.argv[1:]:
        if(s != '-N'):
            pyfileopt='%s %s'%(pyfileopt,s)

    jobopt=pyfileopt.split()[0]
    killjob=1

    MF.sTimer('tcops-chkIfJobIsRunning pyfile: %s jobopt: %s killjob: %s'%(pyfile,jobopt,killjob))
    rc=MF.chkRunning(pyfile,strictChkIfRunning=0,
                     killjob=killjob,verb=verb,nminWait=1,timesleep=5)
    MF.dTimer('tcops-chkIfJobIsRunning pyfile: %s jobopt: %s killjob: %s'%(pyfile,jobopt,killjob))


#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# main
#
# -- turn off Late since John Knaff stopped in 2016...
#
doLate=0

dtgs=mf.dtg_dtgopt_prc(dtgopt,ddtg=6)

af=w2.TcMtcswaFtpServer
al=w2.TcMtcswaFtpLogin
ap=w2.TcMtcswaFtpPasswd
sbdir=w2.TcMtcswaFtpDatDir
tbdir=w2.TcMtcswaDatDir

afL=w2.TcMtcswaLateFtpServer
alL=w2.TcMtcswaLateFtpLogin
apL=w2.TcMtcswaLateFtpPasswd
sbdirL=w2.TcMtcswaLateFtpDatDir
tbdirL=w2.TcMtcswaLateDatDir

tcD=TcData(dtgopt=dtgopt)

for dtg in dtgs:
    # -- get the hot real time from nesdis
    #

    if(stmopt != None):
        (stmids,stmmeta,oyear,obasin,obid,ohemi)=MakeTcStmidsList(stmopt)
    else:
        stmids=tcD.getStmidDtg(dtg)

    for stmid in stmids:
        (yearS,year,stm1id,stm2id)=GetNesdisStm2id(stmid,dtg)

        sdir="%s/%s/"%(sbdir,stm2id)

        tdir="%s/%s/%s"%(tbdir,year,stm1id)
        mf.ChkDir(tdir,diropt='mk')
        #mf.ChangeDir(tdir)

        # -- output wget (stderr) to logpath
        #
        logpath="%s/db.wget.%s.%s.txt"%(tdir,stmid,dtg)

        cmd="wget -nv -m -nd -T 180 -t 2 -a %s \"ftp://%s:%s@%s/%s/\""%(logpath,al,ap,af,sdir)

        # -- 20180813 -- very different way of setting target dir using http AND using the -np option to not descend down the source dir
        #
        wgetopt="-m -np -nH --cut-dirs=3 -nv -T 60 -t 1 -A %s%s* -R *log* --include-directories=/%s "%(stm2id[-4:],stm2id[0:4],sdir)
        cmd="wget -np -nv -m -nd -T 60 -t 1 -a %s \"http://%s/%s/\" -P %s/"%(logpath,af,sdir,tdir)
        cmd="wget %s  \"http://%s/%s\" -P %s/"%(wgetopt,af,sdir,tdir)
        mf.runcmd(cmd,ropt)

        if(ropt != 'norun'):
            ctls=glob.glob("%s/*.ctl"%(tdir))
            for ctl in ctls:
                FixCtl(ctl)


sys.exit()
