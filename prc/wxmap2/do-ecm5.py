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
            'dotest':               ['t',0,1,'only do TCs...no plots'],
            'doDatOnly':            ['D',0,1,'do DAT only'],
            'JustTCs':              ['J',0,1,'do run TCs & plots & Web'],
            'byPassWxmap2Inv':      ['B',1,0,'do NOT byPass the wxmap2.com inv chk, e.g., cron broken'],
            'override':             ['O',0,1,'1 - '],
            'datOverride':          ['o',0,1,'1 - force through data check even if okay... '],
        }


        self.purpose='''
run w2w2.nwp2.py on tenki to kill off nwp2 fields but save w2flds
(c) 2009-%s Michael Fiorino,NOAA ESRL CIRES'''%(w2.curyear)

        self.examples='''
%s cur12 '''



#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# cmdline
#
maxtau=240
argv=sys.argv

CL=w2CmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

# -- do data only if in w2switches.py
#
if(w2.W2doDATAonly): doDatOnly=1

model='ecm5'
m=setModel2(model)
dtgs=mf.dtg_dtgopt_prc(dtgopt)

prcdirFD=w2.PrcDirFlddatW2
prcdirFA=w2.PrcDirFldanalW2

prcdirW2=w2.PrcDirWxmap2W2
prcdirTD=w2.PrcDirTcdiagW2
prcdirTT=w2.PrcDirTctrkW2
prcdirTG=w2.PrcDirTcgenW2
prcdirWB=w2.PrcDirWebW2
prcdirUT=w2.PrcDirUtilW2

cmdFD="w2-fld-rsync-ecm5-wxmap2.py"
cmdTT="w2-tc-runTrks.py"
cmdTD="w2-tc-lsdiag.py"
cmdTG="w2-tc-tcgen2.py"
cmdFA="w2-plot.py"
cmdWB="w2-web.py"
cmdUT="replace.pl"
cmdRG="w2-w2flds-rsync-gmu.py"


for dtg in dtgs:

    MF.sTimer('ALL-do-ecm5: %s'%(dtg))
    # -- check if running and w2flds done already...problem is we kill off the nwp2 fields so will always try to rsync
    #
    rc=w2.ChkIfRunningNWP(dtg,pyfile,model)
    if(rc > 0 and ropt != 'norun'):
        print 'AAA allready running...'
        sys.exit()

    # -- first get the fields
    #
    
    overoptFD=''
    if(override): overoptFD='-O '
    
    rsopt='-X'
    if(byPassWxmap2Inv): rsopt='-B -2 -X'
    if(ropt == 'norun' or dotest): rsopt='-N'
    cmd="%s/%s %s %s %s"%(prcdirFD,cmdFD,dtg,overoptFD,rsopt)
    mf.runcmd(cmd,ropt)

    fm=m.DataPath(dtg,dtype='w2flds')
    fd=fm.GetDataStatus(dtg)
   
    dgrbs=len(fd.dpaths)
    
    # -- 20210922 -- set default doit to -2 .. problem when the rsync fails...
    #
    doit=-2
    fdSfc="%s/ecm5-w2flds-%s-sfc.grb2"%(fd.dstdir,dtg)
    fdUa="%s/ecm5-w2flds-%s-ua.grb2"%(fd.dstdir,dtg)
    fdSfcDt=999.0
    fdSfcOld=-1.5  # path is 1.5 h older than current time
    allreadyDone=0
    
    if(dgrbs == 0 or not(fd.dpathexists) ):
        doit=-1
    elif(dgrbs > 0 and fd.dslastTau < maxtau):
        doit=0
    elif(fd.dslatestCompleteTau == maxtau):
        doit=1
        fdSfcDt=MF.PathCreateTimeCurdiff(fdSfc)
        fdUaDt=MF.PathCreateTimeCurdiff(fdUa)
        # -- 20221112 -- special case for sfc failure on 2022102612 @ ECMWF
        #
        if(fdSfcDt == None): fdSfcDt=-999.
        print 'III---ecm5 fdsfcDt: ',fdSfcDt,' fdUaDt: ',fdUaDt
    
    # -- 20211024 -- new logic to test how old is the sfc.grb2 file, if more than 1 h than assume already done
    #
    if(doit == 1 and fdSfcDt < fdSfcOld):
        allreadyDone=1
        
    # -- 20211024 -- if doit=1 then data pull done and we assume the other processing worked...
    #
    
    if(not(override)):
        
        if(doit < 1):
            print 'WWW---ecm5 NOT READY YET ... bail'
            MF.dTimer('ALL-do-ecm5: %s'%(dtg))
            sys.exit()
                
        elif(doit == 1):
            if(allreadyDone):
                print 'WWW-ecm5 === data pull ALLREADY done...press...'
                print 'WWW-ecm5 === fdSfcDt: %5.1f'%(fdSfcDt),'fdSfcOld: %5.1f'%(fdSfcOld)
                MF.dTimer('ALL-do-ecm5: %s'%(dtg))
                if(datOverride): 
                    print 'WWW-ecm5 === datOverride)...PRESS...'
                else:
                    print 'WWW-ecm5 === not(datOverride)...bail...'
                    sys.exit()
            else:
                print 'WWW-ecm5-111111111111111111-first pass after data for TC wxmap2'
            

            
    # -- because we mislabelled hur as hura at ecmwf...replace var name
    #
    cmd="""%s/%s 'hura ' 'hur  ' %s"""%(prcdirUT,cmdUT,fm.dpath)
    mf.runcmd(cmd,ropt)
                

    # -- DDDDDDDDDDDDDDDDDDDDDDDDDDD Data Only -- bail...
    #
    if(doDatOnly and not(JustTCs)): continue

    # -- TCtrk
    #
    overopt=''
    if(override): overopt='-O '
    cmd="%s/%s %s %s %s"%(prcdirTT,cmdTT,dtg,model,overopt)
    mf.runcmd(cmd,ropt)

    # -- if dotest just do data and tracker
    #
    if(dotest): ropt='norun'

    # -- TCdiag
    #
    overopt=''
    if(override): overopt='-O '
    cmd="%s/%s %s %s %s"%(prcdirTD,cmdTD,dtg,model,overopt)
    mf.runcmd(cmd,ropt)

    # -- TCgen
    #
    overopt=''
    if(override): overopt='-O '
    cmd="%s/%s %s %s %s"%(prcdirTG,cmdTG,dtg,model,overopt)
    mf.runcmd(cmd,ropt)

    if(JustTCs):
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

    MF.dTimer('ALL-do-ecm5: %s'%(dtg))
