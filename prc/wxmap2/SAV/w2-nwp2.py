#!/usr/bin/env python

from M import *
MFs=MFutils()

MFs.sTimer('startup')
from tcbase import *

import M2
import FM
MFs.dTimer('startup')

from TCtrk import tcgenModels
from TCdiag import tcdiagModels,tcdiagModels0618,jtdiagModels

#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
#
# command line setup
#

class w2CmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv

        self.argv=argv
        self.argopts={
            1:['dtgopt',    'DTG (YYYYMMDDHH)'],
            2:['modelopt',  '''modelopt - all | gfs2,ecm2,ecm4,fim8,fimx,ukm2,ngp2,cmc2'''],
        }

        self.options={
            'verb':              ['V',0,1,'verb=1 is verbose'],
            'ropt':              ['N','','norun',' norun is norun'],
            'mintauTC':          ['n:',None,'i',' set mintauTC for running tmtrkN'],
            'doDataOnly':        ['D',0,1,'only do data processing'],
            'forceGribmap':      ['G',0,1,'otherwise -u in gribmap1'],
            'forcePlot1':        ['P',0,1,'1 -  overwrite -O in w2-plot.py'],
            'forcePlot2':        ['p',0,2,'1 -'],
            'forceWeb1':         ['W',0,1,'1 -'],
            'forceWeb2':         ['w',0,1,'1 - '],
            'forceWeb3':         ['H',0,1,'1 - '],
            'dotest':            ['t',0,1,'1 - '],
            'forceTC':           ['T',0,1,'1 - '],
            'JustTCs':           ['J',0,1,'do run TC & plot '],
            'override':          ['O',0,1,'1 - '],
            'overrideSwitches':  ['r',0,1,'1 - by base w2dnwp2* switch'],
            'fldoverride':       ['o',0,1,'1 - '],
            'doRsyncWjetOnly':   ['R',0,1,'1 - '],
            'doRsyncW2flds':     ['2',0,1,'1 - run RsyncWjetW2flds2Local() to rsync w2flds from jet to local'],
            'noRsyncRapb':       ['r',0,1,'1 - '],
            'dormdata':          ['K',0,1,'1 - '],
            'docheck':           ['k',0,1,'bail point for testing'],
            'dow2fldsonly':      ['f',0,1,'1 - '],
            'doNomads':          ['M',0,1,'1 - get from NCDC.Nomads '],
            'doNcepNomads':      ['a',0,1,'1 - get from NCEP.Nomads '],
            'mssGetDir':         ['m:',None,'a','get off mss and put to -m tmp2 model/tmp2'],
            'doarchive':         ['A:',0,'i','doarchive =0|1|2'],
            'dovdeck':           ['v',0,1,'dovdeck=0'],
            'bypassW2flds':      ['b',0,1,"""don't do w2.fld.wgrib.filter.py"""],
            'bypassNWP2flds':    ['B',0,1,"""don't do nwp2 flds"""],
            'bypassPublicWeb':   ['X',1,1,"""don't do public web at all"""],
        }

        self.defaults={
            'incrontab':0,
            'dow2flds':1,
            'docleanPlotsHtms':0,

        }

        self.purpose='''
main control script for nwp2 models (gfs2,ecm2,ecm4,ukm2,fim8,ngp2,cmc2,fimx)
using /public/data/grids/ and from wjet
(c) 2009-%s Michael Fiorino,NOAA ESRL'''%(w2.curyear)

        self.examples='''
%s ops6 gfs2 (sets incrontab=1)'''



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

if(not(forcePlot1 and forcePlot2)): forcePlot=0
if(forcePlot1): forcePlot=1
if(forcePlot2): forcePlot=2

if(not(forceWeb1 and forceWeb2 and forceWeb3)): forceWeb=0
if(forceWeb1): forceWeb=1
if(forceWeb2): forceWeb=2
if(forceWeb3): forceWeb=-1


#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#  main setion ; loop models
#

MF.sTimer('all-%s'%(pyfile))
models=modelopt.split(',')

if(len(models) > 1 or modelopt == 'all'):

    if(modelopt == 'all'):
        #models=w2.wxModels2
        models=M2.Model2.models

        if(dow2flds):
            models.append('cmc2')

    for model in models:
        cmd="%s %s %s"%(CL.pypath,dtgopt,model)
        for o,a in CL.opts:
            cmd="%s %s %s"%(cmd,o,a)
        mf.runcmd(cmd,ropt)
    sys.exit()

else:

    model=modelopt

#--------------------------------------------------
# setup
#

if(dtgopt == 'ops6' or dtgopt == 'ops12'): incrontab=1

dtgs=w2.getOpsDtg(dtgopt,model)

if(ropt == 'norun' and len(dtgs) >= 1):
    for dtg in dtgs:
        print "Process: %s"%(dtg)

    sys.exit()

if(not(w2.IsModel2(model) or model == 'fimx')):
    print 'EEE invalid model w2.IsModel2(model) :: sayoonara:',model
    sys.exit()


if(docleanPlotsHtms):
    docleanopt='-C'
else:
    docleanopt=''

doctl=1
dorunchk=0



# -- switches
# -- turn off doing tctrkflds -- use w2flds instead in w2.fld.wgrib.filter.py

doTCfilt=w2.W2doTCfilt


if(doarchive > 0): w2.W2_BDIRWEB=w2.W2_BDIRWEBA

# -- switches from w2switches
#
if(w2.W2doDATAonly and not(overrideSwitches)): doDataOnly=1


#----------------------------------------------------------------------
# cycle by dtgs
#

for dtg in dtgs:


    # -- make m2 object
    #
    m=M2.setModel2(model)

    # -- get min taus to plot do tc == same as plot
    #
    (mintauPLOT,alltaus)=w2.Model2PlotMinTau(model,dtg)
    if(mintauTC == None):
        mintauTC=mintauPLOT

    MF.sTimer(tag='chkifrunning-w2.nwp2.py')
    

    # -- 20130219 -- look for both dtgopt and dtg runs
    #
    rc1=w2.ChkIfRunningNWP(dtgopt,pyfile,model)
    rc2=w2.ChkIfRunningNWP(dtg,pyfile,model)
    
    # -- if doing dtgopt rc1 = 1 and rc2 = 0 so bump not really
    #if(rc1 == 1): rc1=2    
    #if(rc1 == 0 and rc2 == 1): rc2=2

    rc=max(rc1,rc2)

    print 'CCCIIIRRR11111     rc1: ',rc1,' dtgopt: ',dtgopt,' pyfile: ',pyfile,' model: ',model
    print 'CCCIIIRRR22222     rc2: ',rc2,'   dtg: ',dtg
    print 'CCCIIIRRR MAX(rc1,rc2): ',rc,' nMaxPidInCron: ',w2.nMaxPidInCron

    if(rc > w2.nMaxPidInCron and w2.dochkifrunning):
        if(ropt != 'norun'):
            print 'AAA allready running...'
            continue
    MF.dTimer(tag='chkifrunning-w2.nwp2.py')


    # -- ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
    #    process complete fields and do w2flds, except if pulling over from wjet
    #

    doFullFlds=1
    if(not(w2.onWjet) and doRsyncW2flds): doFullFlds=0
    if(w2.onWjet and fldoverride): override=1

    doNwp2Fields=1

    # -- if using nomads.ncep to directly pull gfs2 fields...
    #
    if(model == 'gfs2' or model == 'ukm2' or model == 'navg'): doNwp2Fields=0

    dtg0p50Gfs='2015050100'
    dtg0p25Gfs='2017021000'
    ddtg0p25=mf.dtgdiff(dtg0p25Gfs,dtg)
    ddtg0p50=mf.dtgdiff(dtg0p50Gfs,dtg)

    if(model == 'gfs2' and ddtg0p25 >= 0.): doNwp2Fields=0

    if(model == 'gfs2' and ddtg0p50 <= 0.0):
        print 'cannot use current nomads methods to recover GFS 0.5deg fields from NCDC for dtg: ',dtg,' press...'
        sys.exit()

    if(doFullFlds):

        # -- w2overide forces making of the controls doing the wgrib inventory
        #    needed for navg because the tau controls are based on the nwp2 vice w2flds state?
        #
        FMoverride=override

        if(doNwp2Fields):

            (sdir,tdir,smask,ctlpath,source,deltaSiz,dtg)=w2.DComNcepDirNRsync(dtg,model,override=override,
                                                                               doNomads=doNomads,doNcepNomads=doNcepNomads,
                                                                               mssGetDir=mssGetDir,
                                                                               dormdata=dormdata,verb=verb,ropt=ropt)

            # -- check if we got some data
            #
            if(sdir == None): continue

            if(dormdata): continue

            if(doRsyncWjetOnly and forceGribmap == 0):
                w2.RsyncWjetDcomNcep2Local(dtg,model)
                sys.exit()

            elif((model == 'ngp2' or model == 'ecm2' or model == 'ecm4' or
                  model == 'gfsk' or model == 'cmc2') and not(w2.onWjet) and not(dow2fldsonly)):
                # --protocol=29 makes rsync version 3.* on kaze work on jetscp which is at version 2.*
                #ScpWjetDcomNcep2Local(dtg,model)
                #else:
                if(not(bypassNWP2flds)):
                    MF.sTimer('rsync-local-%s-%s'%(model,dtg))
                    w2.RsyncWjetDcomNcep2Local(dtg,model)
                    MF.dTimer('rsync-local-%s-%s'%(model,dtg))


            modelmask="%s/%s"%(sdir,smask)
            modelfiles=glob.glob(modelmask)
            modelfiles=w2.FilterNwp2SmaskTaus(modelfiles,model)
            if(verb):
                print 'SSSSSSSSSSSSSS modelfiles     into w2.FilterNwp2SmaskTaus modelmask: ',modelmask
                for mfile in modelfiles:
                    print mfile

            modelfilestdir=glob.glob("%s/%s"%(tdir,smask))
            modelfilestdir=w2.FilterNwp2SmaskTaus(modelfilestdir,model)

            if(verb):
                print 'TTTTTTTTTTTTTT modelfilestdir into w2.FilterNwp2SmaskTaus'
                for mfile in modelfilestdir:
                    print mfile


            if(len(modelfilestdir) > 0 and not(override)):
                modelfiles=modelfilestdir

            modelfiles.sort()

            # -- check for 0 len files
            #
            omodelfiles=[]
            for mfile in modelfiles:
                siz=MF.GetPathSiz(mfile)
                if(siz > 0): omodelfiles.append(mfile)

            modelfiles=omodelfiles

            modelfiles.sort()
            nfiles=len(modelfiles)

            status={}
            dstatus=None
            dogribmap=0

            localmodelfiles=[]
            # -- make localmodelfiles and process
            #
            if(nfiles > 0):
                localmodelfiles=w2.Model2SymbolicLinks(modelfiles,dtg,model,tdir,source,ropt,override)
            else:
                print 'WWW(w2.nwp2.py): no %s model data for %s'%(model,dtg)


            # -- special for ldm data feeds where i blow off input files: ecmn and ecmg
            #
            if(model == 'ecmn'):
                (omodel,grbtype,tautype,doLn)=w2.Model2ModelProp(model)
                localmodelfiles=glob.glob("%s/%s.%s.f???.%s"%(tdir,omodel,dtg,grbtype))

            # -- don't need anymore use M2
            #if((doinv and len(localmodelfiles) > 0) or override):
            #    status=w2.MakeEsrlDataInventory(localmodelfiles,dtg,model,pyfile,incrontab,override)
            #    dstatus=w2.GetDataStatus(status,dtg,model,tdir)


            # -- if doNomads == 1 set options; 20140312 -- really?
            #  
            #if(doNomads or domssGet): forceGribmap=1

            # -- 20121213 -- move to before data check ****************************
            #    wgrib filter the fields for making all wxmap2 products
            #
            dowjet=(w2.onWjet and model == 'gfsk')

            if( ((not(w2.onWjet) and model != 'fimx') or dowjet) and not(bypassW2flds) ):
                prcdir=w2.PrcDirFlddatW2
                mf.ChangeDir(prcdir)
                oopt=''
                #if(override): oopt='-O

                # -- special handling for models with partials...hard override -- redo fdb
                #
                if(override or \
                   #(model == 'ukm2') or (model == 'ngpc') or (model == 'navg') or (model == 'ecmn') or (model == 'ngpj') \
                   (model == 'ukm2') or (model == 'ecmn') or (model == 'navg') \
                   ):
                    oopt='-o'
                    #FMoverride=1

                #oopt=''
                # 20130905 -- use the command line options vice direct setting
                #docheck=1

                # -- must have some localmodelfiles to do w2.fld.wgrib.filter.py
                #
                if( (len(localmodelfiles) > 0 and not(docheck)) or override):
                    cmd="w2.fld.wgrib.filter.py %s %s %s"%(dtg,model,oopt)
                    mf.runcmd(cmd,ropt)
                else:
                    print 'III(%s) no localmodelfiles, bypass w2.fld.wgrib.filter.py ...'%(pyfile)

            # --- if doNomads run wgrib filter
            #
            if(doNomads or doNcepNomads or mssGetDir != None):
                prcdir=w2.PrcDirFlddatW2
                MF.ChangeDir(prcdir)
                cmd="w2.fld.wgrib.filter.py %s %s -o"%(dtg,model)
                mf.runcmd(cmd,ropt)
                if(not(dotest) and not(w2.onKaze) ): doDataOnly=1

        else:
            # -- special for pull w2flds directly from nomads.ncep.noaa.gov
            # -- this curls over gfs2.w2flds.dtg.f???.grb2
            #
            if(model == 'gfs2'):
                overOpt=''
                if(override): overOpt='-O'
                cmd="w2.fld.nomads.curl.gfs0p25.py %s %s"%(dtg,overOpt)
                mf.runcmd(cmd,ropt)

                # -- redo to check if missing taus -- even if override?
                #
                if(not(override)):
                    cmd="w2.fld.nomads.curl.gfs0p25.py %s"%(dtg)
                    mf.runcmd(cmd,ropt)


            elif(model == 'ukm2'):

                overOpt=''
                if(override): overOpt='-O'
                cmd="w2.fld.ukm2-native.py %s %s"%(dtg,overOpt)
                mf.runcmd(cmd,ropt)

                # -- redo to check if missing taus
                #
                if(not(override)):
                    cmd="w2.fld.ukm2-native.py %s"%(dtg)
                    mf.runcmd(cmd,ropt)

            # -- 20160625 -- use ncep to pull navg vice cagips which has been broken since 201605????
            #
            elif(model == 'navg'):

                overOpt=''
                if(override): overOpt='-O'
                cmd="w2.fld.wget-ncep-navgem.py %s %s"%(dtg,overOpt)
                mf.runcmd(cmd,ropt)


            nfiles=-888  # signal to use fd object
            doctl=0


        # --- set/chk data status -- assumes w2.fld.wgrib.filter.py has been called!!! it does not depend on the nwp2 .ctl
        #
        latestCompleteTau=-999

        # -- use M2 data status
        #
        # -- use nwp2 state?
        #fm=m.DataPath(dtg,dowgribinv=1,override=FMoverride)
        # -- w2flds because follow on depends on these fields
        fm=m.DataPath(dtg,dtype='w2flds',dowgribinv=1,override=FMoverride)

        # -- if ngp2 (navgem from ncep) -- don't check # fields because tau78 is low
        # -- done in getDataTaus in Ngp2()
        #if(model == 'ngp2'): checkNF=0
        checkNF=1
        fd=fm.GetDataStatus(dtg,checkNF=checkNF)
        if(nfiles == -888): nfiles=len(fd.datpaths)


        lastTau=-999
        latestTau=-999
        if(fd.dslastTau != None):

            (odtg,curfphr)=mf.dtg_phr_command_prc(dtg)
            curfphr=float(curfphr)

            lastTau=fd.dslastTau
            gmpAge=fd.dsgmpAge
            oldestTauAge=fd.dsoldestTauAge
            latestTau=fd.dslatestTau
            gmplastdogribmap=fd.dsgmplastdogribmap
            gmplatestTau=fd.dsgmplatestTau
            gmplastTau=fd.dsgmplastTau
            latestCompleteTau=fd.dslatestCompleteTau

#         if(dstatus != None):
#             (odtg,curfphr)=mf.dtg_phr_command_prc(dtg)
#             curfphr=float(curfphr)
#             lastTau=dstatus[0]
#             gmpAge=dstatus[1]
#             oldestTauAge=dstatus[2]
#             latestTau=dstatus[3]
#             gmplastdogribmap=dstatus[6]
#             gmplatestTau=int(dstatus[7])
#             gmplastTau=int(dstatus[8])
#             latestCompleteTau=int(dstatus[9])

            if( ((gmpAge-oldestTauAge) < -0.05) or forceGribmap): dogribmap=1

            if(
                (latestTau < lastTau) and

                (gmplatestTau != latestTau and
                 gmplastTau != lastTau and
                 gmplastdogribmap != 2) or

                override

                ): dogribmap=2


            if( ((gmpAge-oldestTauAge) < -0.05) or forceGribmap): dogribmap=1

            if(
                (latestTau < lastTau) and

                (gmplatestTau != latestTau and
                 gmplastTau != lastTau and
                 gmplastdogribmap != 2) or

                override

                ): dogribmap=2

            #eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
            # ecm2 -- always do gribmap if on wjet
            # 20091219 -- turn off fixed localmodelfiles so update should work...
            #if(model == 'ecm2' and FM.onWjet):
            #    dogribmap=3

            print '            onWjet:  %-d '%(w2.onWjet)
            print '            nfiles:  %-d '%(nfiles)
            print '           curfphr:  %-5.2f '%(curfphr)
            print '            gmpAge:  %-5.2f '%(gmpAge)
            print '      oldestTauAge:  %-5.2f '%(oldestTauAge)
            print '         latestTau:  %-5.0f '%(latestTau)
            print '           lastTau:  %-5.0f '%(lastTau)
            print '  gmplastdogribmap: ',gmplastdogribmap
            print '      gmplatestTau: ',gmplatestTau
            print '        gmplastTau: ',gmplastTau
            print ' latestCompleteTau: ',latestCompleteTau
            print
            print '          doNomads: ',doNomads
            print '      doNcepNomads: ',doNcepNomads
            print '         mssGetDir: ',mssGetDir
            print '      forceGribmap: ',forceGribmap
            print 'Final    dogribmap: ',dogribmap

            if(docheck):
                fd.ls('ds')
                #sys.exit()


        # -- add check if lastTau = -999 i.e., fd=fm.GetDataStatus(dtg,checkNF=1) didn't work -- because first time through?
        #
        if(doctl and nfiles > 0 and dogribmap >= 0 or (override and doNwp2Fields) or
           forceGribmap and lastTau != -999):
            w2.MakeEsrlDataCtl(dtg,ctlpath,model,pyfile,lastTau,latestTau,dogribmap,forceGribmap,override,incrontab,ropt=ropt)
            if(forceGribmap): continue

        # -- if getting from hpss, clean and then
        #
        if(mssGetDir != None):
            w2.cleanMssGet(sdir)
            continue

        # -- WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW2222222222222222222222222222222222
        # go to next dtg
        if(dow2fldsonly):
            continue

        if(doDataOnly and mssGetDir == None and not(JustTCs)): 
            print "III(%s) doDataOnly for dtg: %s cycle to next dtg..."%(pyfile,dtg)
            continue

        # ---------------- make model2 object
        #
        if(model == 'fimx'):
            rtmodel='rtfimx'
            FR=FM.getFRlocal(rtmodel,dtg)
        else:
            FR=FM.FimRunModel2(model,dtg,verb=verb,override=override)



    # -- ttttttttttttttttttttttttttttttttttttttttttttttttttcccccccccccccccccccccccccccccccccccccccccccccccccc
    #    TCs

    tcs=findtcs(dtg)
    ntcs=len(tcs)

    iokTCstruct=w2.GetTCstructStatus(dtg,model)
    iokTCtrk=w2.GetTCtrkStatus(dtg,model)


    # -- 2222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222
    # bring over w2flds

    if(doRsyncW2flds):

        # -- set doKishou=1 to rsync from Kishou to local
        #
        doKishou=0
        (tdir,localmodelfiles)=w2.RsyncWjetW2flds2Local(dtg,model,doKishou=doKishou)

        #status=w2.MakeEsrlDataInventory(localmodelfiles,dtg,model,pyfile,incrontab,override)
        #dstatus=w2.GetDataStatus(status,dtg,model,tdir)

        #latestCompleteTau=int(dstatus[9])
        iokTCtrk=1
        iokTCstruct=1
        dogribmap=0

        # -- bring from wjet adecks and put to wjet cira wind data -- do this at end
        #
        #rc=RsyncWjetEsrlAdecks2Local(dtg)
        #rc=RsyncWjetLocal2Cira(dtg)

        continue


    print
    print '             ntcs: ',ntcs
    print '         mintauTC: ',mintauTC
    print '      iokTCstruct: ',iokTCstruct,' BEFORE tcstruct'
    print '         iokTCtrk: ',iokTCtrk,' BEFORE tctrk'

    # -- ttttttttttttttttttcccccccccccccccccccccccc trackers
    #
    if((latestCompleteTau >= mintauTC and
        (iokTCtrk == 0 or dogribmap > 0)) or
       forceTC or (override or fldoverride) ):

        prcdir=w2.PrcDirTctrkW2
        mf.ChangeDir(prcdir)

        overOpt=''
        if(forceTC or override or fldoverride): overOpt='-O'

        # -- run both TM and MF (-M) tracker here
        #
        # -- 20191201 -- -M is redundant -- always run
        cmd="w2-tc-runTrks.py %s %s %s"%(dtg,model,overOpt)
        mf.runcmd(cmd,ropt)

        # -- TTTTTCCCCCDDDDDIIIIIAAAAAGGGGG ----------------------------------------------------
        # -- 20181011 -- do tcdiag here...
        #
        prcdir=w2.PrcDirTcdiagW2
        mf.ChangeDir(prcdir)

        # -- -C :: signal to ldtc that it's being run in cron to force inv at end
        #
        if( (MF.is0012Z(dtg) and (model in tcdiagModels)) or
            (MF.is0618Z(dtg) and (model in tcdiagModels0618))
            ):
            cmd="w2-tc-lsdiag.py %s %s -C"%(dtg,model)
            mf.runcmd(cmd,ropt)


        # -- TTTTTCCCCCGGGGGEEEEENNNNN -----------------------------------------------------------
        # -- 20181012 -- do tcgen now...
        #
        prcdir=w2.PrcDirTcgenW2
        mf.ChangeDir(prcdir)

        if(MF.is0012Z(dtg) and (model in tcgenModels)):
            cmd="w2-tc-tcgen2.py %s %s -C"%(dtg,model)
            mf.runcmd(cmd,ropt)



    # -- tttttttttttttttttccccccccccccccccc struct old mftracker -- disabled
    #
    disable=1
    if( (
        ntcs > 0 and
        latestCompleteTau >= mintauTC and
        (iokTCstruct == 0 or dogribmap > 0) or
        forceTC or (override and not(fldoverride))
    )
        and not(disable)
        ):

        # -- force postprocess after tcstruct to do vdeck for tcfilt
        #
        prcdir=w2.PrcDirTcanalW2
        mf.ChangeDir(prcdir)
        tccopt=''
        if(dovdeck):  tccopt='-P'
        if(forceTC or override): tccopt="%s -O"%(tccopt)

        cmd="w2.tc.tcstruct.py %s %s %s"%(dtg,model,tccopt)
        mf.runcmd(cmd,ropt)

        # -- run my tracker

        prcdir=w2.PrcDirTctrkW2
        mf.ChangeDir(prcdir)

        tccopt=''
        if(forceTC or override): tccopt="%s -O"%(tccopt)
        cmd="w2.tc.mftrk.py %s %s %s"%(dtg,model,tccopt)
        mf.runcmd(cmd,ropt)



    iokTCstruct=w2.GetTCstructStatus(dtg,model)
    iokTCtrk=w2.GetTCtrkStatus(dtg,model)

    #tttttttttttttttttttttttccccccccccccccccccccccffffffffffffffffffffffffffffff
    # TC filt   
    #

    iokTCfilt=w2.GetTCfiltStatus(dtg,model)

    print '      iokTCstruct: ',iokTCstruct,' AFTER tcstruct'
    print '         iokTCtrk: ',iokTCtrk,' AFTER tctrk'
    print '        iokTCfilt: ',iokTCfilt,' BEFORE tcfilt'


    if((
        ntcs > 0 and
        latestCompleteTau >= mintauTCfilt and
        iokTCstruct == 1 and
        iokTCfilt == 0 or forceTC or override
        ) and
       doTCfilt):

        if(incrontab):
            eventtype='nwp2.tcfilt'
            areaopt='ALL'
            eventtag="START--- nwp2.tcfilt  model: %s dtg: %s"%(model,dtg)
            w2.PutEvent(pyfile,eventtype,eventtag,model,dtg,areaopt)

        prcdir=w2.PrcDirTcfiltW2
        mf.ChangeDir(prcdir)
        tcfiltopt=''
        if(forceTC or override): tcfiltopt="%s -F"%(tcfiltopt)
        cmd="w2.tc.tcfilt.py %s %s %s"%(dtg,model,tcfiltopt)
        mf.runcmd(cmd,ropt)

        #
        # do inventory relative to current dtg
        #
        cmd="w2.tc.tcfilt.py %s -I"%(curdtg)
        mf.runcmd(cmd,ropt)

        if(incrontab):
            eventtag="EEEND--- nwp2.tcfilt  model: %s dtg: %s"%(model,dtg)
            w2.PutEvent(pyfile,eventtype,eventtag,model,dtg,areaopt)


    # --- if forceTc bail
    #
    if(forceTC and (forcePlot == 0)): continue

    iokrunning=w2.IsModel2PlotRunning(model,dtg)


    #pppppppppppppppppppppppppwwwwwwwwwwwwwwwwwwwwwwwww
    # do the plots and web

    nplots2do=w2.GetPlotStatus(dtg,model)
    doplot=0
    if(w2.W2Model2PlotWeb and
       (latestCompleteTau >= mintauPLOT and nplots2do > 0 ) or
       (model == 'gfs2' and lastTau >= mintauPLOT) or # special case for gfs2 because of incomplete pulls from ITS :( 
       (forcePlot > 0)
       ): doplot=1

    if(forceWeb > 0): doplot=0

    print '       mintauPLOT: ',mintauPLOT
    print '           doplot: ',doplot
    print '        nplots2do: ',nplots2do

    # -- ttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt dotest endpoint if only doing TCs
    # -- 20190124 -- add prw plots
    if(dotest):

        # -- prw...use full .ctls
        #
        if(model == 'gfs2' or model == 'fim8'):
            prwopt=''
            if(doarchive > 0): prwopt='-C'
            cmdprw="%s/w2.prw.loop.py %s all -A -m %s %s"%(w2.PrcDirFldanalW2,dtg,model,prwopt)
            mf.runcmd(cmdprw,ropt)

        # -- now bail instead of plotting
        #
        continue


    if(doplot):

        if( dorunchk and iokrunning == 0 ): continue

        if(incrontab):
            eventtype='plot-prw'
            areaopt='ALL'
            eventtag="START--- lastTau: %04d"%(lastTau)
            w2.PutEvent(pyfile,eventtype,eventtag,model,dtg,areaopt)

        plotopt=''
        if(forcePlot == 1): plotopt='-O'
        prcdir=w2.PrcDirFldanalW2
        os.chdir(prcdir)
        archopt=''
        if(doarchive > 1): archopt='-A %d'%(doarchive)

        cmdplt="w2-plot.py %s %s %s %s %s"%(dtg,model,docleanopt,plotopt,archopt)
        mf.runcmd(cmdplt,ropt)

        plot='op06'
        tau=0
        cmdplt="w2-plot.py %s %s -t %d -p %s"%(dtg,model,tau,plot)
        mf.runcmd(cmdplt,ropt)

        # -- prw...use full .ctls
        #
        if(model == 'gfs2' or model == 'fim8'):
            prwopt=''
            if(doarchive > 0): prwopt='-C'

            # -- update the adeck at by doing the -u option
            # -- 20170802 -- turn off since adCL.TcFtBtGsf.getABs.getATsBTs() uses ad2(V2) vice adeck(V1)
            #
            #prwopt="%s -u"%(prwopt)

            cmdprw="%s/w2.prw.loop.py %s all -A -m %s %s"%(w2.PrcDirFldanalW2,dtg,model,prwopt)
            mf.runcmd(cmdprw,ropt)

        # -- do goes image loop
        # 20110714 -- move to crontab tab because data not syncing with gfs2
        #
        ##if(model == 'gfs2'):
        ##    cmdgoes="w2.gfs.goes.loop.py %s all -A"%(dtg)
        ##    mf.runcmd(cmdgoes,ropt)

        if(incrontab):
            eventtag="EEEND--- lastTau: %04d"%(lastTau)
            w2.PutEvent(pyfile,eventtype,eventtag,model,dtg,areaopt)

    #wwwwwwwwwwwwwwwwwwwwwwwwwrrrrrrrrrrrrrrrrrrrrrrrrr
    #  web and rsync to brain
    #

    doweb=0
    if(doplot or forceWeb): doweb=1
    if(forceWeb == -1): doweb=0


    if(doweb):

        webopt='-u'
        if(forcePlot): webopt=''
        if(forceWeb == 2): webopt=''
        if(curfphr > w2.maxfphrWeb): webopt=''
        if(forceWeb == 1): webopt='-u'
        prcdir=w2.PrcDirWebW2
        os.chdir(prcdir)
        if(doarchive > 0): webopt="%s -A %d"%(webopt,doarchive)

        cmdplt="w2-web.py %s %s %s"%(dtg,webopt,docleanopt)
        mf.runcmd(cmdplt,ropt)

        # -- do public web
        #
        if(not(bypassPublicWeb)):
            cmdplt="w2-web.py %s %s %s -P"%(dtg,webopt,docleanopt)
            cmdplt="w2-web.py %s %s -P"%(dtg,webopt)
            mf.runcmd(cmdplt,ropt)

        #
        # if no plots done -- don't do rsync
        #

        nplots2doNe=w2.GetPlotStatus(dtg,model)
        print 'WWWWW w2.esrl.nwp2.py: nplots2do',nplots2do,' nplots2doNe: ',nplots2doNe
        if((nplots2do != nplots2doNe or forceWeb) and w2.W2doW3RapbRsync and not(noRsyncRapb)):
            mf.ChangeDir(curdir)
            RsyncWeb(dtg,ropt)


# -- 2222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222
# bring over w2flds

#if(doRsyncW2flds):
    #rc=w2.RsyncWjetEsrlAdecks2Local(dtg)
    #rc=RsyncWjetLocal2Cira(dtg)

MF.dTimer('all-%s'%(pyfile))

sys.exit()
