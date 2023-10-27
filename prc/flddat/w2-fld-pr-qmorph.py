#!/usr/bin/env python

from WxMAP2 import *
w2=W2()

#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
#
# command line setup
#

class WgetCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv
        
        self.argv=argv
        self.argopts={
            1:['dtgopt',    'no default'],
            }

        self.defaults={
            }
        self.options={
            'override':         ['O',0,1,'override'],
            'verb':             ['V',0,1,'verb=1 is verbose'],
            'ropt':             ['N','','norun',' norun is norun'],
            'source':           ['S:',None,'a',' [qmorph]|cmorph'],
            'doevent':          ['E',0,1,' DO event'],
            'dowget':           ['W',1,0,' do NOT do wget'],
            'doallctl':         ['C',1,0,' do NOT do allctl'],
            'doCtlOnly':        ['G',0,1,' do the ctl only...'],
            'doYearCtl':        ['Y',0,1,' make yearly ctl based on curdtg+24...'],
            'dorsync':          ['R',0,1,' do rsync'],
            'ndayback':         ['n:',None,'i',' ndayback to process'],
            'dogribmapupdate':  ['u',0,1,"""do update in gribmap (doesn't work for grads2"""],
            'dorsyncJetZeus':   ['J',0,0,'NEVER rsync products to jet/zeus'],
            'dochkIfRunning':   ['o',1,0,'do NOT chkifrunning in MFutils.chkIfJobIsRunning'],            }

        self.purpose='''
convert cpc qmorph from compressed binary to grib'''

        self.examples="""
%s cur-12
%s cur -R : NOrsync
%s 2008042400 -C -R -W -- don't wget, only process this single dtg and don't make big ctl
%s cur -W -E -- don't do event ... the basis of redoing"""




#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
# main
#


argv=sys.argv
CL=WgetCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

dtgs=mf.dtg_dtgopt_prc(dtgopt)
ddtgFirst=dtgs[0]

model='qmorph'
dtgswitch='2015110800'

#llllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll
#
#  local defs
#

def makeprctl(tmpdir,dtg,source='qmorph'):

    dtgdiff=mf.dtgdiff(dtgswitch,dtg)
    usenew=0
    if(dtgdiff >= 0.0): usenew=1
        
    ctlpath="%s/pr.ctl"%(tmpdir)
    gtime=mf.dtg2gtime(dtg)
    if(source == 'qmorph'):
        
        if(usenew):
            dsetcard="dset ^CMORPH_V0.x_RAW_0.25deg-30min_%s.RT2"%(dtg)
            optioncard='options little_endian'


            dsetcard="dset ^CMORPH_V0.x_RT_8km-30min_%s"%(dtg)
            optioncard='options little_endian'

        else:
            dsetcard="dset ^QMORPH_025deg_%s"%(dtg)
            #dsetcard="dset ^QMORPH_025DEG-30MIN_%s"%(dtg)
            optioncard='options yrev big_endian'
            
    elif(source == 'cmorph'):
        if(usenew):
            dsetcard="dset ^CMORPH_025deg_%s"%(dtg)
            dsetcard="dset ^CMORPH_025DEG-30MIN_%s"%(dtg)
            optioncard='options yrev big_endian'
            
            
            dsetcard="dset ^CMORPH_V0.x_RAW_8km-30min_%s"%(dtg)
            optioncard='options little_endian'
        else:
            dsetcard="dset ^CMORPH_025deg_%s"%(dtg)
            #dsetcard="dset ^CMORPH_025DEG-30MIN_%s"%(dtg)
            optioncard='options yrev big_endian'
            
            
    prctl="""%s
%s
undef  -9999
title  precipitation estimates
xdef 1440 linear    0.125  0.25
ydef  480 linear  -59.875  0.25
zdef  1 levels 1 
tdef  2 linear  %s 30mn
vars 1
pr   1   99 qmorph precip. (mm/hr)
endvars """%(dsetcard,optioncard,gtime)
    
    if(usenew and (source == 'cmorph' or source == 'qmorph') ):
        prctl="""%s
%s
UNDEF  -999.0
TITLE  Precipitation estimates
XDEF 4948 LINEAR   0.036378335 0.072756669
YDEF 1649 LINEAR -59.963614    0.072771377
ZDEF   1 LEVELS 1
TDEF   2 LINEAR  %s 30mn
VARS 1
pr   1  99  hourly cmorph [ mm/hr ]
ENDVARS"""%(dsetcard,optioncard,gtime)

    C=open(ctlpath,'w')
    C.writelines(prctl)
    C.close()
    return(ctlpath)

def makeqmorphctl(tdir,nt,basedtg='2008031418',source='qmorph',doYearCtl=0,
                  tbdir=None,tdirgrib=None,
                  ):

    year=basedtg[0:4]
    gtime=mf.dtg2gtime(basedtg)
    
    if(doYearCtl):
        dset="^%s/%%y4/%s.%%y4%%m2%%d2%%h2.grb"%(tdirgrib,source)
        index="^%s-%s.gmp"%(source,year)
    else:
        dset="^%s/%%y4/%s.%%y4%%m2%%d2%%h2.grb"%(tdirgrib,source)
        index="^%s.gmp"%(source)
    
    ctl="""dset %s
title "c|qmorph pr"
undef 1e+20
dtype grib
index %s
options template
xdef 1440 linear  0.125 0.25
ydef 480 linear -59.875 0.25
zdef 1 levels 1013
tdef %d linear %s 30mn
vars 1
pr        0   59,  1,  0,  0 qmorph precip. (mm/hr) []
endvars"""%(dset,index,nt,gtime)

    if(doYearCtl):
        ctlpath="%s/%s-%s.ctl"%(tbdir,source,year)
    else:
        ctlpath="%s/%s.ctl"%(tbdir,source)
        
    C=open(ctlpath,'w')
    C.writelines(ctl)
    C.close()
    return(ctlpath)
    


#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
#   main loop
#
MF.sTimer(tag='chkifrunning')
rc=w2.ChkIfRunningNWP(curdtg,pyfile)
if(rc > w2.nMaxPidInCron and dochkIfRunning):
    if(ropt != 'norun'):
        print 'AAA allready running...sayounara'
        sys.exit()
MF.dTimer(tag='chkifrunning')

prcdirW2=w2.PrcDirWxmap2W2
cmdRG="w2-pr-rsync-gmu.py"


# -- min size for grb output
#
gzismin=1382568

#llllllllllllllllllllllllllll loop through sources:
#
if(source == None):
    sources=['qmorph','cmorph']
    for source in sources:
        cmd="%s %s"%(pypath,dtgopt)
        for o,a in CL.opts:
            cmd="%s %s %s"%(cmd,o,a)
        cmd="%s -S %s -o"%(cmd,source)
        mf.runcmd(cmd,ropt)

    sys.exit()


#----------------------------------------------------------------------
# -- wget the data...
#

# -- set xgrads
#
xgrads=setXgrads(useStandard=0, useX11=1, returnBoth=0)

MF.sTimer('all')

if(dowget and not(doCtlOnly)):
    MF.sTimer('wget')
    for dtg in dtgs:
        cmd="w2-fld-cpc-wget.py %s -S %s"%(dtg,source)
        mf.runcmd(cmd,ropt)
    MF.dTimer('wget')

curhrdtg=mf.dtg('dtgcurhr')

pdir=w2.PrcDirFlddatW2
if(source == 'qmorph'):
    sbdir=w2.NhcFtpTargetDirQmorph
    tdir=w2.NhcQmorphFinalLocal
    eventtype='qmorph'
    
elif(source == 'cmorph'):
    sbdir=w2.NhcFtpTargetDirCmorph
    tdir=w2.NhcCmorphFinalLocal
    eventtype='cmorph'
    
tbdir="%s/%s"%(w2.PrDatRoot,source)
tdirgrib="30min_025deg/grib"

MF.ChkDir(tdir,'mk')

if(doCtlOnly):

    MF.sTimer('pr.gribmap-only')
    bpdtg=dtgs[0]
    if(len(dtgs) == 1 and not(doYearCtl)):
        print 'EEE to do the ctlonly must set dtgrange in dtgopt'
        sys.exit()
        
    epdtg=dtgs[-1]
    
    if(doYearCtl):
        year=dtgs[0][0:4]
        bpdtg="%s010100"%(year)
        epdtg="%s123123"%(year)
    
    dtimehr=mf.dtgdiff(bpdtg,epdtg)
    nt=(int(dtimehr)+1)*2
    
    if(doYearCtl):
        print 'YYYYYYYY -- ctl for year: ',year
        print

    print 'BBBB bpdtg: ',bpdtg
    print 'EEEE epdtg: ',epdtg
    print '       nt: ',nt

    grbopt=''
    if(dogribmapupdate): grbopt='-u'
    qctlpath=makeqmorphctl(tdir,nt,basedtg=bpdtg,source=source,doYearCtl=doYearCtl,
                           tbdir=tbdir,tdirgrib=tdirgrib)
    cmd="gribmap %s -E -0 -i %s"%(grbopt,qctlpath)
    mf.runcmd(cmd,ropt)
    MF.dTimer('pr.gribmap-only')
    
    if(doYearCtl):
        print 'YYYYYYYYYYYYYYYY -- MMMMMaking --- CCCTTTLLL: source: %s  year: %s ctlpath: %s'%(source,year,qctlpath)
    else:
        print 'MMMMMaking --- CCCTTTLLL: source: %s: ctlpath: %s'%(source,qctlpath)
    
    sys.exit()


tmpdir="%s/tmp"%(tdir)
mf.ChkDir(tmpdir,'mk')

eventmodel='cpc'
eventareaopt='all'

dpaths=[]
pdtgs=[]

MF.sTimer('dpaths')

if(not(mf.find(dtgopt,'cur') or mf.find(dtgopt,'ops'))):
    for dtg in dtgs:
        year=dtg[0:4]
        sdir="%s/%s"%(sbdir,year)
        MF.ChkDir(sdir,'mk')

        dtgdiff=mf.dtgdiff(dtgswitch,dtg)
        usenew=0
        if(dtgdiff >= 0.0): usenew=1
        
        if(source == 'qmorph'):
            if(usenew): 
                mask="CMORPH_V0.x_RAW_0.25deg-30min_%s.RT2.gz"%(dtg)
                mask="CMORPH_V0.x_RT_8km-30min_%s??.gz"%(dtg[0:8])
            else:
                mask="Q*%s*.Z"%(dtg)
                
        elif(source == 'cmorph'):
            if(usenew): 
                mask="CMORPH_V0.x_RAW_8km-30min_%s??.gz"%(dtg[0:8])
            else:
                mask="Q*%s*.Z"%(dtg)
                mask="C*%s*.Z"%(dtg[0:8])
                
        dpaths=dpaths+glob.glob("%s/%s"%(sdir,mask))

else:

    for dtg in dtgs:
        year=dtg[0:4]
        sdir="%s/%s"%(sbdir,year)
        MF.ChkDir(sdir,'mk')
        
        dtgdiff=mf.dtgdiff(dtgswitch,curdtg)
        usenew=0
        if(dtgdiff >= 0.0): usenew=1
    
        if(source == 'qmorph'):
            if(usenew): 
                mask="CMORPH_V0.x_RAW_0.25deg-30min_*.RT2.gz"
                mask="CMORPH_V0.x_RT_8km-30min_%s??.gz"%(dtg[0:8])
            else:
                mask="Q*.Z"
            smask="%s/%s"%(sdir,mask)
            print 'QQQQ smask: ',smask
            dpaths=dpaths+glob.glob("%s"%(smask))
    
        elif(source == 'cmorph'):
            if(usenew): 
                mask="CMORPH_V0.x_RAW_8km-30min_*.gz"
            else:
                mask="Q*.Z"
            dpaths=dpaths+glob.glob("%s/%s"%(sdir,mask))


dpaths=mf.uniq(dpaths)
MF.dTimer('dpaths')

ddtgMin=ddtgFirst
if(ndayback != None): ddtgMin=-24*ndayback

dpaths.sort()

MF.sTimer('getpdtgs')
for dpath in dpaths:

    (ddir,ffile)=os.path.split(dpath)
    tt=ffile.split('_')
    # -- qc check
    #
    qcnewQ=(len(tt) == 5 and not(mf.find(tt[3],'0.25deg')))
    qcnewQ=(len(tt) == 5 and not(mf.find(tt[3],'8km')))
    qcnewC=(len(tt) == 5 and not(mf.find(tt[3],'8km')))
    qcold=(len(tt) != 3 and not(mf.find(tt[1],'025deg')))
    
    if((usenew and qcnewQ and source == 'qmorph') or 
       (usenew and qcnewC and source == 'cmorph')
       ):
        print 'WWW bailing in this dpath: ',dpath
        continue

    # -- get dtg
    #
    if(usenew and (source == 'qmorph' or source == 'cmorph')): 
        dtg=tt[-1].split('.')[0]
    else:
        dtg=tt[2][0:10]
    
    ddtg=mf.dtgdiff(curhrdtg,dtg)

    if(ddtgMin == None or (ndayback != None and ddtg > ddtgMin)):
        if(verb): print 'ddtg,dtg,dpath: ',ddtg,dtg,dpath,ndayback,ddtgMin
        pdtgs.append((dtg,ddtg,dpath))
        
MF.dTimer('getpdtgs')

pdtgs.sort()

if(len(pdtgs) == 0):
    print 'EEE -- no pdtgs -- maybe ndayback == None -- sayounara'
    sys.exit()
    
MF.sTimer('pdtgs')
for pdtg in pdtgs:
    dtg=pdtg[0]
    ddtg=pdtg[1]
    dpath=pdtg[2]
    year=dtg[0:4]
    
    (dir,file)=os.path.split(dpath)


    #------------------- skip 0 size binar files
    #
    #
    if(os.path.getsize(dpath) == 0):
        print 'ZZZZZ 0 size incoming file: ',dpath,' sayoonara ...'
        os.unlink(dpath)
        continue

    

    ## --------------------------- use existence of non 0 size grib file as basis for processing...not events
    ## ecards=w2.GetEvent(eventtype,eventmodel,dtg,eventareaopt)
    ## if(len(ecards) > 0):
    ##     if(verb): print 'WWW already done: ',dtg
    ##     continuef
    
    latsctlpath=makeprctl(tmpdir,dtg,source)

    tbdirq=w2.NhcQmorphFinalLocal
    tdirq="%s/%s"%(tbdirq,year)
    MF.ChkDir(tdirq,'mk')
    
    tbdirc=w2.NhcCmorphFinalLocal
    tdirc="%s/%s"%(tbdirc,year)
    MF.ChkDir(tdirc,'mk')
    
    if(source == 'qmorph'):
        latsgrbpath="%s/qmorph.%s"%(tdirq,dtg)
        grbpath="%s/qmorph.%s.grb"%(tdirq,dtg)
    elif(source == 'cmorph'):
        latsgrbpath="%s/cmorph.%s"%(tdirc,dtg)
        grbpath="%s/cmorph.%s.grb"%(tdirc,dtg)

    allreadydone=0
    if(not(override)):
        gsiz=MF.getPathSiz(grbpath)
        
        if(not(os.path.exists(grbpath))):
            allreadydone=0
        elif(os.path.getsize(grbpath) > 0):
            if(source == 'qmorph' and gsiz >= gzismin):
                allreadydone=1
            elif(source == 'cmorph'):
                allreadydone=1

    if(allreadydone):
        continue

    tpath="%s/%s"%(tmpdir,file)
    (tpathu,ext)=os.path.splitext(tpath)
    
    cmd="cp %s %s"%(dpath,tpath)
    mf.runcmd(cmd,ropt)

    dtgdiff=mf.dtgdiff(dtgswitch,dtg)
    print 'dddd---uuuuu dtg: ',dtg,'dtgdiff: ',dtgdiff
    usenew=0
    if(dtgdiff >= 0.0): usenew=1
    
    if(usenew):
        cmd="%s %s"%('gunzip',tpath)
    else:
        cmd="%s %s"%(w2.CMDuncompress,tpath)
    mf.runcmd(cmd,ropt)

    os.chdir(pdir)
    if(usenew and (source == 'cmorph' or source == 'qmorph') ):
        cmd="%s -lbc \"run w2-fld-pr-cmorph-8km-lats.gs %s %s\""%(xgrads,latsctlpath,latsgrbpath)
    else:
        cmd="%s -lbc \"run w2-fld-pr-qmorph-lats.gs %s %s\""%(xgrads,latsctlpath,latsgrbpath)
    mf.runcmd(cmd,ropt)

    cmd="rm %s/*"%(tmpdir)
    mf.runcmd(cmd,ropt)

    if(doevent):
        eventtag="DONE--- dtg: %s"%(dtg)
        w2.PutEvent(pyfile,eventtype,eventtag,eventmodel,dtg,eventareaopt)

#rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr
#
#

if(dorsync and w2.W2doW3RapbRsync):

    if(source == 'qmorph'):
        cmd="rsync -alv --delete %s %s"%(w2.NhcQmorphFinalLocal,w2.NhcQmorphFinalSnap)
    elif(source == 'cmorph'):
        cmd="rsync -alv --delete %s %s"%(w2.NhcCmorphFinalLocal,w2.NhcCmorphFinalSnap)
    mf.runcmd(cmd,ropt)

#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
#
# set up master .ctl file
# correct way of handling missing data...
#

MF.dTimer('pdtgs')

if(doallctl):

    MF.sTimer('pr.gribmap')
    bpdtg=pdtgs[0][0]
    epdtg=pdtgs[-1][0]
    
    # -- 20180125 - go back 24 h so qmorph.ctl will have enough data points...
    # -- 20190329 -- go back 72 h for qmorph and 24 h for cmorph because it starts 48 h earlier
    #
    if(source == 'qmorph'):
        bpdtg=mf.dtginc(bpdtg, -72)
    else:
        bpdtg=mf.dtginc(bpdtg, -24)
        
    dtimehr=mf.dtgdiff(bpdtg,epdtg)
    nt=(int(dtimehr)+1)*2

    print 'BBBB bpdtg: ',bpdtg
    print 'EEEE epdtg: ',epdtg
    grbopt=''
    if(dogribmapupdate): grbopt='-u'
    qctlpath=makeqmorphctl(tdir,nt,basedtg=bpdtg,source=source,doYearCtl=doYearCtl,
                           tbdir=tbdir,tdirgrib=tdirgrib)
    cmd="gribmap %s -E -0 -i %s"%(grbopt,qctlpath)
    mf.runcmd(cmd,ropt)
    MF.dTimer('pr.gribmap')
    
# -- rsync to gmu.edu
#
if(w2.W2doRsyncPushGmu):

    MF.sTimer('R-GMU: %s at: %s'%(model,dtg))
    cmd="%s/%s -X"%(prcdirW2,cmdRG)
    mf.runcmd(cmd,ropt)
    MF.dTimer('R-GMU: %s at: %s'%(model,dtg))


MF.dTimer('all')
    
sys.exit()

