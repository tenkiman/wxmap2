#!/usr/bin/env python

from tcbase import * # makes w2 and MF + all TC stuff

def getPrwArea(area,bail=1,disAreaChk=0):

    oarea=area
    inArea=not(area in w2.W2AreasPrw) and not(area in w2.W2AreasPrwOld)
    if(inArea and not(disAreaChk)):
        print "EEE %s.getPrwArea() invalid area: --> %s <--"%(pyfile,area)
        print '    not in: ',w2.W2AreasPrw
        print '     or in: ',w2.W2AreasPrwOld
        if(bail): sys.exit()
        return(0,None)
    
    elif(disAreaChk):

        try:
            oarea=w2.W2AreasPrws[area]
        except:
            oarea=None

        if(oarea == None):
            print "EEE--disAreaChk %s.getPrwArea() invalid area: --> %s <--"%(pyfile,area)
            print '    not in: ',w2.W2AreasPrw
            if(bail): sys.exit()
            return(0,None)
        else:
            return(1,oarea)
        

    elif(area in w2.W2AreasPrwOld):
        return(1,area)

    elif(area in w2.W2AreasPrw):

        try:
            oarea=w2.W2AreasPrws[area]
        except:
            oarea=None

        if(oarea == None):
            print "EEE %s.getPrwArea() invalid area: --> %s <--"%(pyfile,area)
            print '    not in: ',w2.W2AreasPrw
            if(bail): sys.exit()
            return(0,None)
        else:
            return(1,oarea)
    else:
        print 'EEE big problem with area: ',area,'in getPrwArea()'
        if(bail): sys.exit()
        return(-1,None)



def IsLoopComplete(model,bdtg,nan,nfc,gifpath,chkgif=1):

    npngs=0
    rcan=1
    for n in range(nan,0,-1):
        rc=ChkPrwAnlPltPath(model,bdtg,area,n)
        if(rc): npngs=npngs+1
        if(not(rc)): rcan=0


    rcfc=1
    for n in range(0,nfc+1):
        path="%s/prw.%s.%s.%s.f%03d.png"%(tmpdir,model,bdtg,area,n)
        rc=MF.ChkPath(path)
        if(not(rc)):
            rcfc=0
        if(rc): npngs=npngs+1

    rc=0
    if(rcan and rcfc):  rc=1

    # -- use imagemajick identify to find # of frames in gif...
    if(chkgif):
        if(MF.ChkPath(gifpath)):
            cmd="identify %s"%(gifpath)
            output=MF.runcmdLog(cmd)
            nfiles=0
            for o in output:
                if(mf.find(o,gifpath)): nfiles=nfiles+1

            if(nfiles < npngs): rc=0



    return(rc)


def ChkPrwAnlPltPath(model,bdtg,area,n):

    nn=abs(n)
    ppath="%s/prw.%s.%s.%s.m%03d.png"%(tmpdir,model,bdtg,area,nn)
    if(os.path.exists(ppath)):
        return(1)
    else:
        return(0)

def ChkPrwFcPltPath(model,bdtg,area,tau0,tau1):

    allthere=1
    for tau in range(tau0,tau1+1):
        ppath="%s/prw.%s.%s.%s.f%03d.png"%(tmpdir,model,bdtg,area,tau)
        if(not(os.path.exists(ppath))):  allthere=0

    return(allthere)

def cleanPng(tmpdir,ndaykeep=1):

    paths=glob.glob("%s/prw*png"%(tmpdir))
    for path in paths:
        age=MF.PathModifyTimeCurdiff(path)
        if(age == None): continue
        age=age/24.0
        dtkeep=age+ndaykeep
        if(dtkeep < 0.0):
            try: os.unlink(path)
            except: None


def MkPrwAnimGifLoop(model,bdtg,nan,nfc,loopdone,gifpath):

    # -- sleep for 2 sec to allow files to get to the right places
    #
    sleep(2)

    dtbeg=100
    dtend=100
    dtfc=50
    dtloop=8
    dtpause=24

    gifcmd="convert -loop 0 -delay %d "%(dtbeg)

    # -- loopdone and gifpath are global vars, not a good idea?
    #
    if(loopdone and os.path.exists(gifpath) and not(override)):
        print 'LLL alldone with loop gif for bdtg: ',bdtg,' area: ',area
        return


    for n in range(nan,0,-1):
        pdtg=mf.dtginc(bdtg,-n)
        path="%s/prw.%s.%s.%s.m%03d.png"%(tmpdir,model,bdtg,area,n)
        #print 'aaaaaaaaaaaa ',path,os.path.exists(path)
        if(os.path.exists(path)):
            if(n == nan):
                gifcmd="%s -delay %d %s"%(gifcmd,dtloop,path)
            elif(n == 0):
                gifcmd="%s -delay %d %s"%(gifcmd,dtbeg,path)
            elif(n%dtpause == 0):
                gifcmd="%s -delay %d %s"%(gifcmd,dtfc,path)
            else:
                gifcmd="%s -delay %d %s"%(gifcmd,dtloop,path)

    for n in range(0,nfc+1):
        path="%s/prw.%s.%s.%s.f%03d.png"%(tmpdir,model,bdtg,area,n)
        #print 'ffffffffffffffff ',path,os.path.exists(path)
        if(os.path.exists(path)):
            if(n%dtpause == 0 and n != nfc):
                gifcmd="%s -delay %d %s"%(gifcmd,dtfc,path)
            elif(n == nfc):
                gifcmd="%s -delay %d %s"%(gifcmd,dtend,path)
            else:
                gifcmd="%s -delay %d %s"%(gifcmd,dtloop,path)



    gifcmd="%s %s"%(gifcmd,gifpath)
    mf.runcmd(gifcmd,ropt)


def RsyncPrwLoop(ropt=''):

    # -- rsync to wxmap2.com
    #
    rc=rsync2Wxmap2('wxmap2',ropt)


def getTCgs(dtg,nan,nfc,dtx=1,dupchk=1,verb=0):

    tcsource='tmtrkN'
    if(tcsource == 'tmtrkN'):
        tcaids=['t'+model]
    elif(tcsource == 'mftrkN'):
        tcaids=['m'+model]

    tBG=TcFtBtGsf(tcsource,tstmids=None,tdtg=dtg,taids=tcaids,
                  tD=tD,
                  dtx=dtx,
                  ATtauRange='-12.0',BTtauRange='%d.0'%(-1*nan),ATOtauRange='0.%d'%(nfc),
                  dupchk=dupchk,  # -- disable dupchk for transition of 9X -> NN between tmtrkN and pw2.loop
                  verb=verb)
    tBG.getABs()
    setgsf =tBG.makeSetTcGsf()

    btgsf  =tBG.makeTcFtBtGsf('bt')
    ftgsf  =tBG.makeTcFtBtGsf('ft')
    dbtgsf =tBG.makeDrawBtGsf()
    dftgsf =tBG.makeDrawFtGsf()

    gs=setgsf+btgsf+ftgsf+dbtgsf+dftgsf

    return(gs)

def cpTaus2Loopdir(dtg,sdir,tdir,ropt=''):

    taus2keep=['m048','m024','f000','f024','f048','f072']

    cpopt='-v -p -u'
    if(onKishou): cpopt='-v -p -n'
    if(override): cpopt='-v -p'
    for tau in taus2keep:
        cmd="cp %s %s/*%s*%s* %s/."%(cpopt,sdir,dtg,tau,tdir)
        mf.runcmd(cmd,ropt)



areas=w2.W2AreasPrwOld


#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
#
# command line setup
#

class w2CmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv

        self.argv=argv

        self.argopts={
            1:['dtgopt',   'no default'],
            2:['area',    'all or prwArea: %s'%(str(areas))],
        }


        self.options={

            'verb':                 ['V',0,1,'verb=1 is verbose'],
            'ropt':                 ['N','','norun',' norun is norun'],
            'override':             ['O',0,1,'1 - '],
            'disAreaChk':           ['D',0,1,'Disable area check to test new area'],

            'chkgif':               ['G',1,0,'do NOT chkgif in loop'],
            'tauopt':               ['t:',None,'a','taub.taue'],
            'model':                ['m:','gfs2','a','model to do prw'],

            'doall':                ['A',0,1,'doall prc'],
            'interactive':          ['i',0,1,'run interactively'],
            'doInventoryOnly':      ['I',0,1,'make inventory for prw.htm'],
            'mkloop':               ['L',0,1,'make gif loop'],
            'dorsync':              ['Y',0,1,'rsync to...'],
            'doregen':              ['R',0,1,'write to wxmap2a/'],
            'docpOnly':             ['P',0,1,'only cp tau files over'],

        }

        self.defaults={

        }

        self.purpose='''
create MIMIC-like prw [925 wind] animated .gif
areas: %s'''%(str(areas))

        self.examples='''
%s cur all -A                : standard in w2.nwp2.py
%s cur-18.cur-6 all -A -O    : do all prc and all areas override
%s cur12-12 lant,wpac -A     : do just lant and wpac
%s cur-54.cur-6 wpac -t 0    : analysis plots for wpac'''


#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# cmdline
#

argv=sys.argv

CL=w2CmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr


#---------------------------------------------------------------------------------------
# when running from cron need to change dir...
#

mf.ChangeDir(pydir)

tmpdir=w2.PrwLoopTmpDir
mf.ChkDir(tmpdir,'mk')

nwpdir=w2.Nwp2DataBdirModel(model)

#  -- N hr back (nan) and forward (nfc)
#
nan=48
nfc=48
nfc=72

# -- cycle through bdtgs.
#

dtcycle=6
dtgs=mf.dtg_dtgopt_prc(dtgopt,ddtg=dtcycle)

if(len(dtgs) > 1):

    for dtg in dtgs:
        cmd="%s %s %s"%(pyfile,dtg,area)
        for o,a in CL.opts:
            cmd="%s %s %s"%(cmd,o,a)
        mf.runcmd(cmd,ropt)

    sys.exit()


# -- do all processing
#

dt=1
dtgs=mf.dtg_dtgopt_prc(dtgopt,ddtg=dt)

bdtg=dtgs[0]
# -- set TcData by first analysis dtg vice dtg (years in getMD2years shifts on 011500)
#
bdtgTCd=mf.dtginc(dtgs[0],-nan)

# -- check how old this run -- if 'tooold' force regen
# --- bypass if onKishou
#
howold=mf.dtgdiff(bdtg,curdtg)/24.0
tooold=(howold > w2.W2MaxOldRegen)
if(tooold and not(w2.onKishou)):  doregen=1

if(doregen):
    w2.W2BaseDirWeb=w2.W2RegenBaseDirWeb
    w2.PrwGoesDir="%s/plt_prw_goes"%(w2.W2BaseDirWeb)

loopdir=w2.W2LoopPltDir('prw')
mf.ChkDir(loopdir,'mk')

if(doInventoryOnly):
    rc=makePrwInventory(loopdir,verb=verb)
    sys.exit()

# -- clean off files > ndaykeep old
#
rc=cleanPng(tmpdir,ndaykeep=1)

tD=TcData(dtgopt=bdtgTCd)

if(area == 'all'): doall=1

if(doall and not(docpOnly)):

    if(area == 'all'):
        areas=w2.W2AreasPrwOld
    else:
        areas=area.split(',')
        if(len(areas) <= 1): areas=[area]

    for area in areas:

        oopt=''
        if(override): oopt='-O'
        aopt=''
        if(doregen > 0): aopt='-R'

        dtg=dtgs[0]
        if(disAreaChk):
            disopt='-D'
        else:
            disopt=''

        cmd="%s %s %s %s -t %d.-1 %s -m %s %s"%(pyfile,dtg,area,disopt,nan*-1,oopt,model,aopt)
        mf.runcmd(cmd,ropt)

        taub=0
        taue=nfc
        tauopt="%d.%d"%(taub,taue)

        cmd="%s %s %s %s -t %s %s -m %s %s"%(pyfile,dtg,area,disopt,tauopt,oopt,model,aopt)
        mf.runcmd(cmd,ropt)

        cmd="%s %s %s %s -t %s -L %s -m %s %s"%(pyfile,dtg,area,disopt,tauopt,oopt,model,aopt)
        mf.runcmd(cmd,ropt)


    if(dorsync): rc=RsyncPrwLoop()
    sys.exit()


#sssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssstart ----
#
(rc,area)=getPrwArea(area,disAreaChk=disAreaChk,bail=1)

# -- copy individual tau files to loopdir so Owen can grab them...
#
taupltdir="%s/%s"%(w2.PrwGoesDir,bdtg)
mf.ChkDir(taupltdir,'mk')

MF.sTimer(tag='chkifrunning')
rc=w2.ChkIfRunningNWP(bdtg,pyfile,model)
if(rc > w2.nMaxPidInCron and w2.dochkifrunning):
    if(ropt != 'norun'):
        print 'AAA allready running...sayounara'
        sys.exit()
MF.dTimer(tag='chkifrunning')

if(docpOnly):
    for dtg in dtgs:
        taupltdir="%s/%s"%(w2.PrwGoesDir,dtg)
        mf.ChkDir(taupltdir,'mk')
        cpTaus2Loopdir(dtg,tmpdir,taupltdir)
    sys.exit()

gifpath="%s/prw.%s.%s.%s.loop.gif"%(loopdir,model,bdtg,area)

loopdone=1
if(not(override)):
    loopdone=IsLoopComplete(model,bdtg,nan,nfc,gifpath,chkgif=chkgif)

if(loopdone and not(override) and not(mkloop)):
    print 'DDD alldone bye for bdtg: ',bdtg,' area: ',area
    if(dorsync): rc=RsyncPrwLoop()
    sys.exit()

# -- with -A option (doall) the third call will make the loop, why it's up here and not at the end
#
if(mkloop):
    MkPrwAnimGifLoop(model,bdtg,nan,nfc,loopdone,gifpath)
    rc=makePrwInventory(loopdir,verb=verb)
    if(dorsync): rc=RsyncPrwLoop()
    
    sys.exit()

rc=w2.getW2fldsRtfimCtlpath(model,bdtg,details=0)
if(rc[0] == 0): print 'EEE no w2flds for model: ',model,' bdtg: ',bdtg ; sys.exit()
(rc,nwpdir,ctlpath)=rc

if(tauopt != None):
    tt=tauopt.split('.')
    if(len(tt) == 1):
        taus=[int(tauopt)]
    
    elif(len(tt) >= 2):
        btau=int(tt[0])
        etau=int(tt[1])+1
        taus=range(btau,etau,dt)
    
    elif(len(tt) == 3):
        btau=int(tt[0])
        etau=int(tt[1])+1
        dtau=int(tt[2])
        taus=range(btau,etau,dtau)
else:
    print 'WWW maybe you want to set -A for all option?'
    sys.exit()

gradsopt='-lbc'
if(interactive):
    gradsopt='-lc'

xgrads='grads'
xgrads=setXgrads()

(gradsapp,ext)=os.path.splitext(pyfile)

gsBase='g.prw.base.gs'
gsFinal="%s/t.prw.%s"%(w2.ptmpBaseDir,gsBase)

# -- add tc plotting .gsf to base; check out the 
#
gs=open(gsBase).readlines()
gs=MF.List2String(gs)

gsx=open('prwarea.gsf').readlines()
gsx=MF.List2String(gsx)
gs=gs+gsx

gsf=getTCgs(bdtg,nan=48,nfc=72,dtx=1,dupchk=0)
gs=gs+gsf

MF.WriteString2File(gs,gsFinal,verb=1)

if(len(taus) > 1 and taus[0] >= 0):

    # dotauloop inside grads to speed up plotting... 
    #
    tau0=taus[0]
    tau1=taus[-1]

    if((ChkPrwFcPltPath(model,bdtg,area,tau0,tau1) == 1) and not(override) ):
        print 'WWWW fcpltchk =1 for ',bdtg,' tau= ',tau0,' ',tau1
    else:
        gradsarg="%s %s %d %d %s %s %s"%(area,bdtg,tau0,tau1,model,nwpdir,tmpdir)
        cmd="%s %s \"%s %s\""%(xgrads,gradsopt,gsFinal,gradsarg)
        mf.runcmd(cmd,ropt)

else:

    for tau in taus:

        pdtg=mf.dtginc(bdtg,tau)
        if(not(ChkPrwAnlPltPath(model,bdtg,area,tau)) or override):
            doft=0
            if(tau >= 0): doft=1
            gradsarg="%s %s %d %d %s %s %s"%(area,bdtg,tau,tau,model,nwpdir,tmpdir)
            cmd="%s %s \"%s %s\""%(xgrads,gradsopt,gsFinal,gradsarg)
            mf.runcmd(cmd,ropt)
        else:
            if(verb):
                print 'III: anal plot already done: ',area,bdtg,' tau: ',tau


rc=cpTaus2Loopdir(bdtg,tmpdir,taupltdir)

# -- 20210329 -- add rsync option
#
if(dorsync): RsyncPrwLoop()


# -- do the prw/goes inventory for prw2.htm (will rename later)
#
#### -- not here but after loop gifs made??? rc=makePrwInventory(loopdir,verb=verb)

sys.exit()