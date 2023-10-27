#!/usr/bin/env python

from WxMAP2 import *
w2=W2()

from MD import *
MdDbname='mdeck'

def LsAidsStormsDss(DSs,tstms=None,taids=None,dofilt9x=0,lsopt='s',
                    dtgopt=None,printZeros=1,
                    verb=1):

    if(dtgopt != None and tstms == None):
        dtgs=mf.dtg_dtgopt_prc(dtgopt)
        dtg=dtgs[-1]
        tD=TcData(dtgopt=dtg)
        # -- use same method as in TCvitals
        #
        tstms=tD.getDSsDtg(dtg)

        ## -- don't need this if using getDSsDtg
        ## -- convert 2-char basin id to subbasin
        ##
        #tstmids=[]
        #for tstm in tstms:
            #stmid=tD.getSubbasinStmid(tstm)
            #tstmids.append(stmid)

        #tstms=tstmids

    aids={}
    stms=[]

    try:
        dskeys=DSs.db['keys'].getData()
        dskeys.sort()
    except:
        return(aids,stms)

    for dskey in dskeys:

        aid=dskey.split('_')[0]
        stm=dskey.split('_')[1]

        snum=int(stm[0:2])
        if(dofilt9x and (snum >= 90 and snum <= 99) ): continue

        doaid=1
        dostm=1
        stmnum=int(stm[0:2])
        if(dofilt9x and (stmnum >= 90 and stmnum <= 99)): dostm=0

        if(tstms != None):
            dostm=0
            if(type(tstms) != ListType): tstms=[tstms]
            for tstm in tstms:
                stmnum=int(stm[0:2])
                if(mf.find(stm,tstm.upper())): dostm=1
                if(dofilt9x and (stmnum >= 90 and stmnum <= 99)): dostm=0

        if(taids != None):
            doaid=0
            if(type(taids) != ListType): taids=[taids]
            for taid in taids:
                if(mf.find(aid,taid.lower())): doaid=1

        if(doaid): MF.loadDictList(aids,stm,aid)
        if(dostm): stms.append(stm)

    stms=MF.uniq(stms)

    if(len(stms) == 0):
        print 'WWW(AD.LsAidsStormsDss) no storms for tstms: ',tstms
        return(aids,stms)

    kk=aids.keys()
    kk.sort()

    for stm in stms:
        try:       aa=aids[stm]
        except:    continue

        aa.sort()
        lsext=''

        if(lsopt == 's'):
            nstrlen=128
            if(len(str(aa)) > nstrlen): lsext='...'
            card='stmid: %s'%(stm)+' aids: %s %s'%(str(aa)[0:nstrlen],lsext)
            print card

        if(lsopt == 'l'):
            nstrlen=-1
            lsext=''
            card='stmid: %s'%(stm)+' aids:'
            for n in range(0,len(aa)):
                card="%s %5s"%(card,aa[n])
                if(n%20 == 0 and n > 0): card="%s %s"%(card,aa[n])+'\n'
            if(dtgopt == None): print card


    if(lsopt != 'f' and lsopt != 'l' and dtgopt == None):
        return(aids,stms)


    if(dtgopt != None):
        idtgs=mf.dtg_dtgopt_prc(dtgopt)
        print 'Searching for dtgs: ',idtgs
        printZeros=0


    # -- new form of output, aid,stm,dtgs
    #
    for stm in stms:
        try:       oaids=aids[stm]
        except:    continue
        for aid in oaids:
            #aP=Aid(aid)
            dskey="%s_%s"%(aid,stm)
            DSs.verb=0
            aD=DSs.getDataSet(dskey)

            if(aD == None): continue

            if(aD.__module__ == 'VD'):

                bdtgs=aD.bdtg[0]
                vflags=aD.vflag[0]

                gotlong=0
                if(hasattr(aD,'vdecktype')):
                    if(aD.vdecktype == 'long'):
                        warns=aD.warnYN[0]
                        fcruns=aD.fcrunYN[0]
                        tflags=aD.tcYN[0]
                        gotlong=1

                for n in range(0,len(bdtgs)):
                    bdtg=bdtgs[n]
                    hh=bdtg[8:10]
                    if(gotlong):
                        warn=warns[n]
                        vflag=vflags[n]
                        fcrun=fcruns[n]
                        tcflg=tflags[n]
                        print bdtg,hh,warn,vflag,fcrun,tcflg
                dtgs=bdtgs
                odtgs=dtgs

            else:

                # -- find dtgs with longest, because of bug in updateAds of not setting nad.dtgs=
                #
                dtgs1=aD.dtgs
                dtgs2=aD.ats.keys()
                dtgs=dtgs1
                if(len(dtgs2) >= len(dtgs1)): dtgs=dtgs2

                if(dtgopt != None):
                    odtgs=[]
                    for dtg in dtgs:
                        if(dtg in idtgs): odtgs.append(dtg)
                else:
                    odtgs=dtgs

                # -- print the adeck cards
                #
                if(lsopt == 'f'):
                    aD.lsAidcards(dtgopt=dtgopt)

            odtgs.sort()

            doprint=1
            if(not(printZeros) and len(odtgs) == 0): doprint=0
            if(printZeros): doprint=1

            if(doprint):  print 'aid: %7s'%(aid),' stm:',stm,'N: %3d'%(len(odtgs)),' dtgs:',MF.makeDtgsString(odtgs)



    return(aids,stms)






def ScpTcDss2Kishou(ropt=''):

    fname="%s.pypdb"%(MdDbname)
    sdir=w2.TcDatDirDSs

    if(w2.onKaze):
        
        tdir='fiorino@%s:%s/DSs'%(w2.KishouScpServer,w2.KishouTcDatDir)
        cmd='''scp %s/%s  "%s/."'''%(sdir,fname,tdir)
        mf.runcmd(cmd,ropt)

    elif(w2.onKishou):

        tdir="%s/%s"%(w2.DATKazeBaseDir,sdir)
        cmd="cp %s/%s  %s/."%(sdir,fname,tdir)
        mf.runcmd(cmd,ropt)

    

#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
#
# command line setup
#

class MdeckCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):
        if(argv == None): argv=sys.argv
        
        self.argv=argv
        self.argopts={
#            1:['year',    'no default'],
            }

        self.defaults={
            'lsopt':'s',
            'doupdate':0,
            }

        self.options={
            'year':           ['y:',None,'a','year'],
            'dop1year':       ['1',0,1,'do p1year in MD.Mdeck()'],
            'override':       ['O',0,1,'override'],
            'verb':           ['V',0,1,'verb=1 is verbose'],
            'ropt':           ['N','','norun',' norun is norun'],
            'domdecks':       ['M',1,0,'0 - DO NOT make mdeck cards'],
            'doputdss':       ['P',1,0,'0 - DO NOT putDSs'],
            'dostmstats':     ['s',1,0,'0 - DO NOT stmstats'],
            'dols':           ['l',0,1,'1 - list'],
            'lstype':         ['y:','r','a','type r - reg ; g - genesis'],
            'dolslong':       ['L',0,1,'1 - long list'],
            'dolsgen':        ['G',0,1,'1 - ls genesis dtgs only'],
            'stmopt':         ['S:',None,'a','stmopt'],
            'warn':           ['W:',0,1,'warning'],
            'mdtag':          ['t:',None,'a','tag for mdecks-tag name'],
            'update':         ['u',0,1,'only update mdeck'],
            'doclean':        ['K',0,1,"""blow away .pypdb file because shelf created with 'c' option """],
            'doScpMdecks':    ['C',0,0,"""deprecate"""],
            }

        self.purpose='''
purpose -- parse mdecks create TC data shelves
%s 2009
'''
        self.examples='''
%s -y 2009
%s -y 2000-2005  # cycle through years 2000-2005'''

    def ChkSource(self):

        iok=0
        for s in self.sources:
            if(self.source == s): iok=1 ; break

        return(iok)

#eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
# errors

def errAD(option,opt=None):

    if(option == 'tstmids'):
        print 'EEE # of tstmids = 0 :: no stms to verify...stmopt: ',stmopt
    elif(option == 'tstms'):
        print 'EEE # of tstms from stmopt: ',stmopt,' = 0 :: no stms to verify...'
    else:
        print 'Stopping in errAD: ',option

    sys.exit()
        


#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
# main
#

MF.sTimer(tag='mdeck')

CL=MdeckCmdLine(argv=sys.argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

if(year == None):
    print 'EEE must use -y opt to set the year'
    sys.exit()

elif(year == 'cur' or year == 'ops' or year == None):
    (shemoverlap,yyyy1,yyyy2)=CurShemOverlap(curdtg)
    if(shemoverlap): dop1year=1

    year=curyear
    shemyear=getShemYear(curdtg)
    
    if(shemyear != year):
        # - do next year first to avoid messing up current year hashes
        # -- causing a hang?  or writeback=1?
        # -- no - needed to do cur for tcgen2, go back until we remove all mdeck dependencies
        #
        years=[shemyear,year]
        for year in years:
            scpopt=''
            if(year != years[-1]): scpopt='-C'
            cmd="%s -y %s %s"%(CL.pypath,year,scpopt)
            for o,a in CL.opts:
                if(o != '-y'):
                    cmd="%s %s %s"%(cmd,o,a)
            mf.runcmd(cmd,ropt)
        sys.exit()

elif(len(year.split('-')) == 2):
    year0=year.split('-')[0]
    year1=year.split('-')[1]
    print 'yyy',year0,year1
    if(year1 == 'cur'):
        (shemoverlap,yyyy1,yyyy2)=CurShemOverlap(curdtg)
        year1=yyyy1
        if(shemoverlap): year1=yyyy2
        
    years=MF.YearRange(year0,year1)
    for year in years:
        scpopt=''
        if(year != years[-1]): scpopt='-C'
        cmd="%s -y %s %s"%(CL.pypath,year,scpopt)
        killopt=None
        if(year == years[0] and doclean): killopt='-K'
        for o,a in CL.opts:
            if(o != '-y' and o != '-K'):
                cmd="%s %s %s"%(cmd,o,a)
        if(killopt != None): cmd="%s %s"%(cmd,killopt)
        mf.runcmd(cmd,ropt)
    sys.exit()
    
if(stmopt != None): domdecks=0; doputdss=0; dolslong=1
  
  
dowriteback=0
dsbdir="%s/DSs"%(TcDataBdir)
if(mdtag != None):
    dbname="mdecks-%s"%(mdtag)
else:
    dbname='mdecks'

backup=0
dbfile="%s.pypdb"%(dbname)
mdDSs=DataSets(bdir=dsbdir,name=dbfile,dtype=dbname,verb=verb,backup=backup,unlink=doclean,dowriteback=dowriteback,doDSsWrite=1)

if(stmopt != None): tstmids=MakeStmList(stmopt,verb=0)
else: tstmids=None

if(tstmids == None): pass
elif(len(tstmids) == 0): errAD('tstmids')


if(dols or dolslong or lstype == 'g' or dolsgen):
    if(dolslong): lsopt='l'
    if(dols): lsopt='s'
    if(dolsgen): lstype='g'
    stms=LsStormsDss(mdDSs,year,tstmids,lsopt=lsopt,lstype=lstype)
    sys.exit()


# -- force regen by setting all datasets to None
#

if(domdecks):
    print 'MMMMMMMMMMMMMMMMMM doing mdeck for year: ',year
    if(ropt != 'norun'): 
        MF.sTimer('mdeck')
        #mdD=DSs.getDataSet(key='mdeck_dtg')
        #mdDg=DSs.getDataSet(key='mdeck_dtg_gen')
        #mdDs=DSs.getDataSet(key='mdeck_stmid')
        mdD=mdDg=mdDs=None
        md=Mdeck(year,mdD,mdDg,mdDs,dop1year=dop1year)
        MF.dTimer('mdeck')

if(dostmstats):
    print 'SSSSSSSSSSSSSSSSSS dostmstats...',year
    if(ropt != 'norun'):
        MF.sTimer('stats')
        dsname='mdeck_stmstats'
        #mdSS=DSs.getDataSet(key=dsname)
        mdSS=None
        ms=MdeckSimple(year,mdSS,verb=verb)
        ms.analyzeBt(mdDSs,mdD=md.mdD,mdDs=md.mdDs,mdDg=md.mdDg,
                     verb=verb)
        rc=mdDSs.putDataSet(ms,key=dsname)
        if(rc == -1):
            print 'EEE big problem in w2-tc-dss-mdeck.py...putting: ',dsname
            sys.exit()

        MF.dTimer('stats')
        
if(doputdss):
    print 'PPPPPPPPPPPPPPPPPP putting dataset md...',year
    if(ropt != 'norun'):
        MF.sTimer('put')
        rc=mdDSs.putDataSet(md.ds,key=year,unlinkException=0)
        if(rc == -1):
            print 'EEE big problem in w2-tc-dss-mdeck.py...putting mdeck for year: ',year
            sys.exit()
            
        mdDSs.putDataSet(md.mdD,key='mdeck_dtg')
        mdDSs.putDataSet(md.mdDg,key='mdeck_dtg_gen')
        mdDSs.putDataSet(md.mdDs,key='mdeck_stmid')
        #if(dowriteback == 0): DSs.syncDataSet()  #-- sync so available to analyzeBt and dowriteback=0
        
        MF.dTimer('put')


if(doputdss or dostmstats):
    mdDSs.closeDataSet()  #-- close syncs the writeback cache
    
if(mdtag == None and doScpMdecks):
    
    MF.sTimer('scp')
    rc=ScpTcDss2Kishou(ropt=ropt)
    MF.dTimer('scp')

    # -- Theia too
    MF.sTimer('RsyncTCmdecks2Theia')
    sdir=w2.TcDatDirDSs
    tdir='%s@%s:%s/DSs'%(w2.TheiaScpServerLogin,w2.TheiaScpServer,w2.TheiaTcDatDir)
    cmd='''rsync --timeout=30 --protocol=29 -alv --delete %s/mdecks.pypdb  "%s/"'''%(sdir,tdir)
    mf.runcmd(cmd,ropt)
    if(ropt == ''): MF.dTimer('RsyncTCmdecks2Theia')
    
    # -- Hera too
    MF.sTimer('RsyncTCmdecks2Hera')
    sdir=w2.TcDatDirDSs
    tdir='%s@%s:%s/DSs'%(w2.HeraScpServerLogin,w2.HeraScpServer,w2.HeraTcDatDir)
    cmd='''rsync --timeout=30 --protocol=29 -alv --delete %s/mdecks.pypdb  "%s/"'''%(sdir,tdir)
    mf.runcmd(cmd,ropt)
    if(ropt == ''): MF.dTimer('RsyncTCmdecks2Hera')
    

MF.dTimer(tag='mdeck')

sys.exit()


        


