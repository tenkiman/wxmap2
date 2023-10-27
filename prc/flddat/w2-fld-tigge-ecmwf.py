#!/usr/bin/env python

from WxMAP2 import *
w2=W2()

from M2 import setModel2
from tcbase import PrcDirTctrkW2

def getL2Status(m2,dtg,dmodelType='w2flds'):
    
    m2.dmodelType=dmodelType
    m2.dtype=dmodelType
    if(dmodelType == 'w2flds'):
        m2.bddir="%s/%s/dat/%s"%(w2.Nwp2DataBdir,dmodelType,model)
    else:
        m2.bddir="%s/%s"%(w2.Nwp2DataBdir,dmodelType)
        
    if(hasattr(m2,'setxwgribNwp2')): m2.setxwgrib=m.setxwgribNwp2
    fm=m2.DataPath(dtg,dtype=dmodelType,dowgribinv=1,override=override,doDATage=1)
    fd=fm.GetDataStatus(dtg)

    itaus=[]
    ltau=None
    nfCntFlg=-1
    lowTau=-999
    
    if(len(fm.datpaths) > 0):
        itaus=fm.dsitaus
        if(fd.dslatestCompleteTauBackward > 0):
            ltau=fd.dslatestCompleteTauBackward
        else:
            ltau=fd.dslatestCompleteTau

        nfCntFlg=1
        lowTau=-999
        for itau in itaus:
            (age,nf)=fm.statuss[dtg][itau]

            if(nf < fm.nfields):
                nfCntFlg=0
                lowTau=itau
                break
                
    rc=1
    if(nfCntFlg == -1): rc=0
    if(nfCntFlg == 0): rc=-1

    return(rc)
    


#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
#
# command line setup
#

class EcmtCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv
        
        self.argv=argv
        self.argopts={
            1:['dtgopt',    'no default'],
            }

        self.defaults={
            }

        self.options={
            'override':       ['O',0,1,'override'],
            'autoCheck':      ['a',1,0,'do NOT autoCheck l2 status'],
            'verb':           ['V',0,1,'verb=1 is verbose'],
            'dofldinv':       ['I',0,1,'just run M2.DataPath(), GetDataStatus()'],
            'doalltaus':      ['A',1,0,'do NOT do all taus at once v tau by tau - doalltaus=0 deprecated'],
            'doCycle':        ['C',1,0,'do NOT cycle about dtgs'],
            'dotmtrkN':       ['t',1,1,'run tmtrkN (+mftrkN)'],  # -- disable-- always do tmtrkN
            'redo':           ['R',0,1,'redo if data problem'],
            'dols':           ['l',0,1,'do l2 listing'],
            'dolsLong':       ['L',0,1,'get status rc and l2 listing'],
            'ropt':           ['N','','norun',' norun is norun'],
            'doWgrib2Only':   ['W',0,1,' only do wrib2 processing -- old vesion of wgrib2 broke processing...'],
            'doDatOnly':      ['D',0,1,' only do DAT no TCs...'],
            'doTauP6':        ['6',0,1,'run BOTH tau+0 and tau+6'],
            'dochkIfRunning': ['o',0,1,'do chkifrunning using chkRunning() in MFutil'],
            'killPrevJob':    ['K',0,1,'kill first run is'],
            'model':          ['m:','ecmt','a','set model to ecmt or ecmh'],
            }

        self.purpose='''
purpose -- get ops run of ecmwf ifs manage w2flds local and mss
%s cur'''
        self.examples='''
%s cur'''


#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# main
#

MF.sTimer(tag='ecmt-all-outer')
CL=EcmtCmdLine(argv=sys.argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

prcdirW2=w2.PrcDirWxmap2W2
cmdRG="w2-w2flds-rsync-gmu.py"

m2=setModel2(model)
dmodelType='w2flds'

killjobOpt=-1

dtgs=mf.dtg_dtgopt_prc(dtgopt,ddtg=m2.rundtginc)

if(doCycle and len(dtgs) > 1):

    if(not(dochkIfRunning)):
        rc=MF.chkRunning(pyfile,strictChkIfRunning=0,killjob=killjobOpt,nminWait=5)

    for dtg in dtgs:
        cmd="%s %s -o"%(pyfile,dtg)
        for o,a in CL.opts:
            #if(o != '-C'):  -- don't do since default is -C -> 1
            if(o != '-o'):
                cmd="%s %s %s"%(cmd,o,a)
        mf.runcmd(cmd,ropt)    

    sys.exit()

else:
    # -- check if running in MFutils.class
    #
    if(not(dochkIfRunning)):
        rc=MF.chkRunning(pyfile,strictChkIfRunning=0,
                         verb=verb,
                         killjob=killjobOpt,nminWait=5)
    


minDtgAge=48.0
for dtg in dtgs:

    dtgChk=1
    rc=getL2Status(m2,dtg)

    if(autoCheck and not(dols) and not(redo)):
        if(rc == -1): override=1; dotmtrkN=1
        if(rc == 0):  override=1; dotmtrkN=1
        if(rc == 1):
            print 'WWW'
            print 'WWW --- autoCheck shows all is done for: ',dtg,' press...'
            print 'WWW'
            continue
        
    # -- turn off tc if doDatOnly
    #
    if(doDatOnly): dotmtrkN=0
    
    
    if(doalltaus):

        # -- first get status -- real time or older and report from l2.py
        #
        curdtg=mf.dtg()
        cmd="l2.py %s ecmt -W"%(dtg)
        l2log=MF.runcmdLog(cmd, ropt='', quiet=1)
        dtgStatus=l2log[0].split()[1].strip()
        dtgAge=MF.DtgDiff(dtg,curdtg)
        if(len(dtgStatus) != 10 and dtgAge >= minDtgAge): dtgChk=0
        if(dtgAge < minDtgAge): dtgChk=-1
        
        # -- ls or redo
        #
        if(dols or redo):
            
            if(redo and dtgChk == 0):
                print 'WWWW --'
                print 'WWWW -- problem with: ',dtgStatus,'rerun...'
                print 'WWWW --'
                cmd="%s %s -t"%(pyfile,dtg)
                mf.runcmd(cmd,ropt)
                    
            continue    
        
        # -- bail if not override and dtgChk okay
        #
        if(dtgChk and not(override) and not(dols) and not(dolsLong) and not(dotmtrkN)):
            print 'IIII -- already done for dtg: ',dtg
            continue

        MF.sTimer(tag='ecmt-alltaus-%s'%(dtg))
        
        # -- check alltaus file and tau status
        #
        m2.doalltaus=1
        m2.setDtgTdirCtl(dtg)
        m2.filtTaus(curdir,dtgChk,override=1,quiet=0)
        rc=m2.chkTauDat(verb=verb,override=1)
        
        if(dolsLong): 
            print 'LLListing for dtg: ',dtg,'rc: ',rc
            cmd="l2.py %s ecmt -W"%(dtg)
            mf.runcmd(cmd,'quiet')
            continue
        
        if(doWgrib2Only):
            m2.filtTaus(curdir,dtgChk,override=1)
            m2.doalltaus=0
            m2.setDtgTdirCtl(dtg)
            m2.makeCtl()
            rc=m2.chkTauDat(verb=verb,override=1)
            MF.dTimer(tag='ecmt-alltaus-%s'%(dtg))
            continue
        
        # -- we have an alltau -- with just UA -- now go after sf
        #
        if(rc == -1):
            overrideUA=0
            m2.getFieldsTigge(verb=verb,override=overrideUA,ropt=ropt,cleanDir=overrideUA,justSfc=1)
            m2.filtTaus(curdir,dtgChk,override=1)
            m2.doalltaus=0
            rc=m2.chkTauDat(verb=verb,override=1)
            
        if(rc == 1):
            m2.doalltaus=0
            m2.setDtgTdirCtl(dtg)
            m2.makeCtl()
            
        if(rc == 1 and not(override)):
            print 'III already done for dtg: ',dtg,' rc: ',rc,' dotmtrkN: ',dotmtrkN
            if(dotmtrkN):
                MF.sTimer('ecmt-tmtrkN-redo-%s'%(dtg))
                dtgp6=mf.dtginc(dtg,6)
                cmd="%s/w2-tc-runTrks.py %s.%s %s"%(PrcDirTctrkW2,dtg,dtgp6,model) # run current and +6 h since 48-h old
                mf.runcmd(cmd,ropt)
                MF.dTimer('ecmt-tmtrkN-redo-%s'%(dtg))

            continue
        
        if(rc == -2): 
            print 'WWWWWWWWWWw-------------- setting overide = 1 because zero length or incomplete alltaus file...'
            override=1
        
        m2.doalltaus=1
        m2.getFieldsTigge(verb=verb,override=override,ropt=ropt,cleanDir=override)
		
        if(ropt == 'norun'): continue

        m2.filtTaus(curdir,dtgChk,override=1)
        m2.doalltaus=0
        m2.setDtgTdirCtl(dtg)
        m2.makeCtl()
        rc=m2.chkTauDat(verb=verb,override=1)

        MF.sTimer('ecmt-tmtrkN-%s'%(dtg))
        if(dotmtrkN):
            if(doTauP6):
                # -- run both tau+0 and tau+6
                #
                dtgp6=mf.dtginc(dtg,6)
                cmd="%s/w2-tc-runTrks.py %s.%s %s"%(PrcDirTctrkW2,dtg,dtgp6,model)
                mf.runcmd(cmd,ropt)
            else:
                # -- just tau+0
                #
                cmd="%s/w2-tc-runTrks.py %s %s"%(PrcDirTctrkW2,dtg,model) 
                mf.runcmd(cmd,ropt)
                

        MF.dTimer('ecmt-tmtrkN-%s'%(dtg))
        
        MF.dTimer(tag='ecmt-alltaus-%s'%(dtg))
        
    else:
    
        # -- make grib inventory, etc...
        #
        m2.doalltaus=0
        m2.setDtgTdirCtl(dtg)
        m2.makeCtl()
        rc=m2.chkTauDat()
        fm=m2.DataPath(dtg,dtype=m2.dmodelType,dowgribinv=1,override=override,doDATage=1)
        fd=fm.GetDataStatus(dtg)

    # -- rsync to gmu.edu
    #
    if(w2.W2doRsyncPushGmu):
    
        MF.sTimer('R-GMU: %s at: %s'%(model,dtg))
        cmd="%s/%s %s %s"%(prcdirW2,cmdRG,dtg,model)
        mf.runcmd(cmd,ropt)
        MF.dTimer('R-GMU: %s at: %s'%(model,dtg))
    
if(not(dols) and dtgChk == 0): MF.dTimer(tag='ecmt-all-outer')
