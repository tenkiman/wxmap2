#!/usr/bin/env python

from WxMAP2 import *
w2=W2()

from M2 import setModel2

class w2CmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv

        self.argv=argv
        self.argopts={
            1:['dtgopt',    'DTG (YYYYMMDDHH)'],
        }

        self.options={
            'verb':                 ['V',0,1,'verb=1 is verbose'],
            'ropt':                 ['N','','norun',' norun is norun'],
            'JustTCs':              ['J',0,1,'do run TC & plot '],
            'dotest':               ['t',0,1,'only do TCs...no plots'],
            'doDatOnly':            ['D',0,1,'do DAT only'],
            'doNomads':             ['M',1,1,'always use nomads vice get_gfs.pl--after 202209 ncep change'],
            'doGetGfs':             ['G',0,1,'use get_gfs.pl'],
            'doCycle':              ['C',0,1,'cycle b taus in get_gfs.pl'],
            'override':             ['O',0,1,'1 - '],
            'override0':            ['o',0,1,'little override that only bypassed m2 data check'],
            'bypassChkRunning':     ['B',0,1,'1 - bypass ChkIfRunningNWP']
        }


        self.purpose='''
run w2w2.nwp2.py on tenki to kill off nwp2 fields but save w2flds
(c) 2009-%s Michael Fiorino,NOAA ESRL CIRES'''%(w2.curyear)

        self.examples='''
%s cur12 '''



#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# cmdline
#
argv=sys.argv

CL=w2CmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

# -- do data only if in w2switches.py
#
if(w2.W2doDATAonly): doDatOnly=1

model='gfs2'
maxtau=192

m=setModel2(model)
dtgs=mf.dtg_dtgopt_prc(dtgopt)

prcdirFD=w2.PrcDirFlddatW2
prcdirFA=w2.PrcDirFldanalW2
prcdirW2=w2.PrcDirWxmap2W2
prcdirTD=w2.PrcDirTcdiagW2
prcdirTT=w2.PrcDirTctrkW2
prcdirTG=w2.PrcDirTcgenW2
prcdirWB=w2.PrcDirWebW2

if(doGetGfs):
    cmdFD="w2-fld-get_gfs_pl-gfs2.py"
    cycleTaus=0
    if(doCycle): cycleTaus=1
else:
    cmdFD="w2-fld-nomads-curl-gfs0p25.py"
    cycleTaus=-999
    
cmdTT="w2-tc-runTrks.py"
cmdTD="w2-tc-lsdiag.py"
cmdTG="w2-tc-tcgen2.py"
cmdFA="w2-plot.py"
cmdPL="w2-prw-loop.py"
cmdWB="w2-web.py"
cmdRG="w2-w2flds-rsync-gmu.py"


for dtg in dtgs:

    MF.sTimer('ALL-do-gfs2: %s'%(dtg))
    
    # -- check if running and w2flds done already...problem is we kill off the nwp2 fields so will always try to rsync
    #
    if(not(bypassChkRunning)):
        rc=w2.ChkIfRunningNWP(dtg,pyfile,model)
    else:
        rc=-1

    if(rc > 0 and ropt != 'norun'):
        print 'AAA allready running...'
        sys.exit()

    # -- get data status
    #
    fm=m.DataPath(dtg,dtype='w2flds')
    fd=fm.GetDataStatus(dtg)
    doit=(fd.dslastTau == None or (fd.dslastTau < maxtau))
    if(not(doit) and fd.dslastTau == maxtau): doit=0

    if(not(doit) and not(override)): 
        print 'WWW-%s already done for dtg: %s at curtime: %s ...press...'%(CL.pyfile,dtg,CL.curtime)
        if(dotest or override0): 
            None
        elif(JustTCs):
            print 'JJJJJJJJ -- just doing TCs & plots'
        else:
            sys.exit()

    # -- first get the fields
    #
    roptFD=''
    if(ropt == 'norun' or JustTCs): roptFD='norun'
    overoptFD=''
    cmdFDOpt=''
    if(override): overoptFD='-O '
    if(cycleTaus == 1):
        cmdFDOpt='-C'
    cmd="%s/%s %s %s %s"%(prcdirFD,cmdFD,dtg,cmdFDOpt,overoptFD)

    if(not(JustTCs)): 
        
        mf.runcmd(cmd,roptFD)
        
        if(doNomads and not(doGetGfs)):
            # -- run two more times...20210123 server/power/boulder probs
            #
            cmd="%s/%s %s"%(prcdirFD,cmdFD,dtg)
            mf.runcmd(cmd,roptFD)
        
            cmd="%s/%s %s"%(prcdirFD,cmdFD,dtg)
            mf.runcmd(cmd,roptFD)

    # -- DDDDDDDDDDDDDDDDDDDDDDDDDDD Data Only -- bail...
    #
    if(doDatOnly and not(JustTCs)): continue

    # -- check if data there...if not bail on whole thing
    #
    MF.sTimer('w2flds-datachk')
    fm=m.DataPath(dtg,dtype='w2flds')
    fd=fm.GetDataStatus(dtg)
    gotData=not( (fd.dslastTau == None or (fd.dslastTau < maxtau)) )
    if(gotData == 0):
        print 'EEE (do-gfs2.py) GFS data pull failed... fd.dslastTau: ',fd.dslastTau,' sayounara!!'
        sys.exit()
    else:
        print 'III (do-gfs2.py) good data full for dtg: ',dtg
    MF.dTimer('w2flds-datachk')

    # -- TCtrk
    #
    overopt=''
    if(override): overopt='-O '
    cmd="%s/%s %s %s %s"%(prcdirTT,cmdTT,dtg,model,overopt)
    mf.runcmd(cmd,ropt)


    # -- TCdiag
    #
    overopt=''
    if(override): overopt='-O '
    cmd="%s/%s %s %s %s"%(prcdirTD,cmdTD,dtg,model,overopt)
    mf.runcmd(cmd,ropt)

    # -- TCgen -- do before TCdiag because it waits for other processes???
    #
    if(w2.is0012Z(dtg)):
        overopt=''
        if(override): overopt='-O '
        cmd="%s/%s %s %s %s"%(prcdirTG,cmdTG,dtg,model,overopt)
        mf.runcmd(cmd,ropt)
        
    # -- prw loops
    #
    overopt=''
    if(override): overopt='-O '
    cmdprw="%s/%s %s all -A -m %s %s"%(prcdirFA,cmdPL,dtg,model,overopt)
    mf.runcmd(cmdprw,ropt)
    
    # -- if dotest just do data and tracker
    #
    if(dotest): 
        ropt='norun'
        continue

    # -- do plots
    #
    overopt=''
    if(override): overopt='-O '
    cmd="%s/%s %s %s %s"%(prcdirFA,cmdFA,dtg,model,overopt)
    mf.runcmd(cmd,ropt)

    # -- do qmorph plot
    #
    plot='op06'
    tau=0
    cmdplt="%s/%s %s %s -t %d -p %s"%(prcdirFA,cmdFA,dtg,model,tau,plot)
    mf.runcmd(cmdplt,ropt)

    # -- do web
    #
    webopt='-u'
    docleanopt=''
    cmd="%s/%s %s %s %s"%(prcdirWB,cmdWB,dtg,webopt,docleanopt)
    mf.runcmd(cmd,ropt)

    # -- 20210818 -- do just the TCdiag trkplots...
    #
    MF.sTimer('TCDiag-trkplot-redo: %s %s'%(dtg,model))
    overopt='-l -o test-trkplot'
    cmd="%s/%s %s %s %s"%(prcdirTD,cmdTD,dtg,model,overopt)
    mf.runcmd(cmd,ropt)
    MF.dTimer('TCDiag-trkplot-redo: %s %s'%(dtg,model))

    # -- 20221220 -- do inventory and push to wxmap2
    #
    MF.sTimer('TCDiag-inv: %s %s'%(dtg,model))
    overopt='-I'
    cmd="%s/%s %s %s %s"%(prcdirTD,cmdTD,dtg,model,overopt)
    mf.runcmd(cmd,ropt)
    MF.dTimer('TCDiag-inv: %s %s'%(dtg,model))

    # -- rsync to gmu.edu
    #
    if(w2.W2doRsyncPushGmu):
    
        MF.sTimer('R-GMU: %s at: %s'%(model,dtg))
        cmd="%s/%s %s %s"%(prcdirW2,cmdRG,dtg,model)
        mf.runcmd(cmd,ropt)
        MF.dTimer('R-GMU: %s at: %s'%(model,dtg))
        
    MF.dTimer('ALL-do-gfs2: %s'%(dtg))
