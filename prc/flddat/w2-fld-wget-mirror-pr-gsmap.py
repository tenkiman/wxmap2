#!/usr/bin/env python

from WxMAP2 import *
w2=W2()

from M import *
MF=MFutils()


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
            'model':'gfs2',
            }

        self.options={
            'override':      ['O',0,1,'override'],
            'verb':          ['V',0,1,'verb=1 is verbose'],
            'ropt':          ['N','','norun',' norun is norun'],
            'doWget':        ['W',1,0,' do NOT do wget'],
            'doClean':       ['C',1,0,' do NOT clean off .dat'],
            'makeV6':        ['6',0,1,'make or ln -s V6 only'],
            'doGribmapOnly': ['g',0,1,'only do gribmap'],
            'doGauge'      : ['G',0,1,'only do gribmap'],
            
            }

        self.purpose='''
purpose -- wget mirror gfs stb (sat brightness t) goes images
%s cur
'''
        self.examples='''
%s cur
'''


def makeGsmapDailyCtl(yymmdd):
    
    dfiles=glob.glob("*.%s.*dat"%(yymmdd))
    dfiles.sort()
    ddf=dfiles[0]
    print ddf
    dd=ddf.split('.')
    gsversion=ddf[-13:-4]
    gsversion="%s.%s.%s"%(dd[-4],dd[-3],dd[-2])
    gsname=dd[0]
    print 'gggg',gsversion,ddf
    print 'gsname:',gsname,ddf.split('.')

    ctlpath="pr-gsmap-%s.ctl"%(yymmdd)
    nt=24
    prdtg="%s00"%(yymmdd)
    gtime=mf.dtg2gtime(prdtg)
    
    ctl="""DSET  ^%s.%%y4%%m2%%d2.%%h200.%s.dat
TITLE  GSMaP_MVK 0.1deg Hourly (ver.8)
OPTIONS YREV LITTLE_ENDIAN TEMPLATE
UNDEF  -99.0
XDEF   3600 LINEAR    0.05 0.1
YDEF   1200  LINEAR -59.95 0.1
ZDEF     1 LEVELS 1013
TDEF   %d LINEAR %s 1hr
VARS    1
pr    0  99   hourly averaged rain rate [mm/hr]
ENDVARS"""%(gsname,gsversion,nt,gtime)
    

    C=open(ctlpath,'w')
    C.writelines(ctl)
    C.close()
    return(ctlpath)
    
def makeGsmapDailyGribCtl(yymmdd,ropt='norun'):
    

    ctlpath="pr-gsmap-%s.ctl"%(yymmdd)
    nt=24
    prdtg="%s00"%(yymmdd)
    gtime=mf.dtg2gtime(prdtg)
    
    ctl="""dset ^pr-gsmap-%%y4%%m2%%d2%%h2.grb
index ^pr-gsmap-%s.gmp
undef 9.999E+20
options template
dtype grib
xdef 1440 linear   0.125 0.25
ydef  480 linear -59.875 0.25
zdef    1 linear 1 1
tdef %d linear %s 1hr
vars 1
pr  0 59,1,0  ** Precipitation rate [mm/h]
ENDVARS"""%(yymmdd,nt,gtime)

    C=open(ctlpath,'w')
    C.writelines(ctl)
    C.close()
    cmd="gribmap -v -i %s"%(ctlpath)
    mf.runcmd(cmd,ropt)
    


def make0p25products(ctlpath,opath):
    
    gs="""
open %s
pra06=ave(pr,t+0,t+5)
pra12=ave(pr,t+6,t+11)
pra18=ave(pr,t+12,t+17)
pra24=ave(pr,t+18,t+23)

set fwrite %s
set gxout fwrite
d re(pra06,1440,linear,0.125,0.25,480,linear,-59.875,0.25)
d re(pra12,1440,linear,0.125,0.25,480,linear,-59.875,0.25)
d re(pra18,1440,linear,0.125,0.25,480,linear,-59.875,0.25)
d re(pra24,1440,linear,0.125,0.25,480,linear,-59.875,0.25)
"""%(ctlpath,opath)



#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
# main
#


def getVersionNum(dtg,tbdir,tbdirV6,makeV6=0,doGauge=0,ropt=''):
    
    
    v8start='2021120100'
    v7start='2014030100'
    v6start='2000030100'
    
    yyyy=dtg[0:4]
    yyyymmdd=dtg[0:8]
    
    isV8=isV7=isV6=0
    sbdir=None
    
    diffV8=mf.dtgdiff(v8start,dtg)
    diffV7=mf.dtgdiff(v7start,dtg)
    diffV6=mf.dtgdiff(v6start,dtg)
    
    if((diffV8 >= 0.0) and (diffV8 <= diffV7 and (diffV7 < diffV6))):isV8=1
    if(diffV8 < 0. and (diffV7 >= 0.0) and (diffV7 < diffV6)): isV7=1
    if(diffV8 < 0. and (diffV7 < 0.) and (diffV6 >= 0.0)): isV6=1
    if(diffV8 < 0. and (diffV7 < 0.) and (diffV6 < 0.)): isV6=-1
    
    print 'DDDDD   ',dtg,'v8: ',diffV8,' v7: ',diffV7,' v6:',diffV6
    print 'IIIII V8',isV8,' V7',isV7,' V6',isV6
    if(makeV6):
        if(isV6 and not(doGauge)):
            print 'LLLLL doing ln -s'
            tdir="%s/final/%s/%s"%(tbdir,yyyy,yyyymmdd)
            tdirV6="%s/final/%s/"%(tbdirV6,yyyy)
            MF.ChkDir(tdirV6,'mk')
            cmd="ln -f -s %s %s"%(tdir,tdirV6)
            mf.runcmd(cmd,ropt)
            return(None)
        else:
            isV6=1
            isV7=isV8=0
            print '66666      making v6 pulling vice ln -s'

    if(isV6 < 0):
        print 'WWW -- dtg: ',dtg,' before start of V6: ',v6start
        return(None)
    
    hourDir='hourly'
    if(doGauge):hourDir='hourly_Grev'
    if(isV8):
        sbdir='/standard/v8/%s/'%(hourDir)
    elif(isV7):
        sbdir='/standard/v7/%s/'%(hourDir)
    elif(isV6):
        sbdir='/standard/v6/%s/'%(hourDir)
    elif(isV6 == -1):
        sbdir=None
        
    return(sbdir)
        


MF.sTimer(tag='GSMAP-ALL')

argv=sys.argv
CL=WgetCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

prcdir=w2.PrcDirFlddatW2
cmdRG="w2-w2flds-rsync-gmu.py"

al='rainmap'
ap="""Niskur+1404"""
af='hokusai.eorc.jaxa.jp'

tbdirV6  =w2.PrGsmapV6DatRoot
tbdir    =w2.PrGsmapDatRoot
tbdirV6G ="%s-Grev"%(tbdirV6)

gscmd="w2-fld-pr-gsmap-0p1deg-lats.gs"
gname='pr-gsmap'

dtgs=mf.dtg_dtgopt_prc(dtgopt,ddtg=24)

for dtg in dtgs:

    sbdir=getVersionNum(dtg,tbdir,tbdirV6,makeV6,doGauge)
    if(sbdir != None and makeV6):
        if(doGauge):
            tbdir=tbdirV6G
            print '66666ggggg making V6-Gauge in: ',tbdir,' from: ',sbdir
        else:
            tbdir=tbdirV6
            print '66666_____ making V6       in: ',tbdir,' from: ',sbdir

    MF.sTimer("GSMAP-ALL-%s"%(dtg))
    yyyy=dtg[0:4]
    mm=dtg[4:6]
    dd=dtg[6:8]
    yymmdd=dtg[0:8]

    if(sbdir == None):
        print 'WWW -- just doing ln of VX -> V6'
        continue
    
    sdir="%s/%s/%s/%s"%(sbdir,yyyy,mm,dd)
    tdir="%s/incoming/%s/%s"%(tbdir,yyyy,yymmdd)
    fdir="%s/final/%s/%s"%(tbdir,yyyy,yymmdd)
    mf.ChkDir(fdir,diropt='mk')

    # -- first check if processed already...
    #
    opath1st="%s/%s-%s"%(fdir,gname,dtg)
    gpaths1st=glob.glob("%s.grb"%(opath1st))
    lgpath1st=len(gpaths1st)

    # -- 20221129 -- just do the gribmap...we missed in version 0.1
    #
    if(doGribmapOnly):

        rc=mf.ChangeDir(fdir)
        if(lgpath1st == 0):
            print 'EEE doGribmapOnly, but no grib...sayounara'
            continue
            #sys.exit()
            
        rc=makeGsmapDailyGribCtl(yymmdd,ropt=ropt)
        continue
    
    if(lgpath1st and not(override)):
        print 'III dtg: ',dtg,'already done...press...'
        continue
        
        
    if(doWget and (lgpath1st == 0 or override)):
        
        mf.ChkDir(tdir,diropt='mk')
        mf.ChangeDir(tdir)

        cmd="wget -nv -m -nd -T 180 -t 2  \"ftp://%s/%s/*\""%(af,sdir)
        mf.runcmd(cmd,ropt)

        gzfiles=glob.glob("*.gz")
        gzfiles.sort()
        
        if(len(gzfiles) == 0):
            print 'III -- not ready at jaxa for dtg: ',dtg
            continue
        
        for gzfile in gzfiles:
            datfile=gzfile[0:-3]
            tt=datfile.split('.')
            zdtg="%s%s"%(tt[1],tt[2][0:2])
            grbpath="%s/%s-%s.grb"%(fdir,gname,zdtg)
            
            gsiz=MF.getPathSiz(grbpath)
            dsiz=MF.getPathSiz(datfile)
            
            # -- only do the gunzip if no final grbfile
            #
            if((gsiz < 0 and dsiz < 0) or override):
                cmd="gunzip -c %s > %s/%s"%(gzfile,fdir,datfile)
                mf.runcmd(cmd,ropt)
            else:
                print 'III- %s already processed...press...'%(grbpath)
                

    mf.ChangeDir(fdir)
    fctlfile=makeGsmapDailyCtl(yymmdd)
    
    # -- go back to processing dir
    #
    mf.ChangeDir(prcdir)
    
    for gt in range(0,24):
        
        dpath=None
        gpath=None
        gsiz=dsiz=zsiz=-999

        dpaths=glob.glob("%s/*%s.%02d*.dat"%(fdir,yymmdd,gt))
        if(len(dpaths) == 1):
            dpath=dpaths[0]
        
        gdtg="%s%02d"%(yymmdd,gt)
        gtndx=gt+1

        if(dpath != None):
            dsiz=MF.getPathSiz(dpath)

        opath="%s/%s-%s"%(fdir,gname,gdtg)
        gpaths=glob.glob("%s.grb"%(opath))
        if(len(gpaths) == 1):
            gpath=gpaths[0]
            if(gpath != None): gsiz=MF.getPathSiz(gpath)
            
        if((dsiz > 0 and gsiz < 0) or override):
            ipath="%s/%s"%(fdir,fctlfile)
            MF.sTimer('gsmap-%s'%(gdtg))
            cmd='''grads -lbc "run %s %d %s %s"'''%(gscmd,gtndx,ipath,opath)
            mf.runcmd(cmd,ropt)
            MF.dTimer('gsmap-%s'%(gdtg))

            # -- get the new grib file
            #
            gpaths=glob.glob("%s.grb"%(opath))
            if(len(gpaths) == 1):
                gpath=gpaths[0]
                if(gpath != None): gsiz=MF.getPathSiz(gpath)

        hh=gdtg[8:10]
        zpaths=glob.glob("%s/*.%s.%s00.*gz"%(tdir,yymmdd,hh))
        if(len(zpaths) == 1):
            zpath=zpaths[0]
            zsiz=MF.getPathSiz(zpath)
            #print 'zzzsss',zsiz

            

        #print 'FFFFFFFFFFFFF',dpath,gpath
        print 'SSSSSSSSSSSSS',dsiz,gsiz,zsiz,doClean
        
        if(doClean and dsiz > 0 and gsiz > 0):
            cmd="rm  %s"%(dpath)
            mf.runcmd(cmd,ropt)
        
        if(doClean and gsiz > 0 and zsiz > 0):
            cmd="rm  %s"%(zpath)
            mf.runcmd(cmd,ropt)

    # -- make .ctl for grib
    #
    if(gsiz > 0):
            
        rc=mf.ChangeDir(fdir)
        rc=makeGsmapDailyGribCtl(yymmdd,ropt=ropt)

    
    MF.dTimer("GSMAP-ALL-%s"%(dtg))
    

MF.dTimer(tag='GSMAP-ALL')

