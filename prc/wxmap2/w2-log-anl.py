#!/usr/bin/env python
from WxMAP2 import *
w2=W2()

def getYMD(logline,ldtginc=6,eps=0.001):
    
    # -- 20230508 -- handle date format on openSuse Mike5
    #
    from mf import cname3
    tt=logline.split()

    ampmflg=tt[-4]
    
    add12=0
    if(ampmflg == 'AM' or ampmflg == 'PM'): apflg=1
    else: apflg=0
    
    if(apflg == 0):
        time=tt[-5]
        year=tt[-3]
        dd=int(tt[-6])
        mm=cname3[tt[-7].upper()]
    else:
        #['05', 'Apr', '2023', '02:37:01', 'PM', 'UTC', 'on', 'tenkiS.wxmap2.com']

        if(ampmflg == 'PM'): add12=12
        time=tt[-5]
        year=tt[-6]
        dd=int(tt[-8])
        mm=cname3[tt[-7].upper()]

    itime=time.split(':')
    hh=int(itime[0])+add12
    ftime=float(hh) + (float(itime[1])/60.0) + (float(itime[2])/(60.0*60.0))
    ihh=int(ftime-eps)
    dhh=ihh/ldtginc
    dhh=dhh*ldtginc
    dtgymd="%s%s%02d"%(year,mm,dd)
    dtg="%s%02d"%(dtgymd,dhh)
    return(time,dtgymd,ftime,dtg)


logsTenki={
    
'load':'log.load.py.tenki.LOAD',

'cln-w':'log-w2-clean-web.py.WEBCLEAN',
'cln-h':'log-w2-clean-hfip.py.HFIPCLEAN',
'ecmt':'log-w2.fld.tigge.ecmwf.py.ECMT',
'ecmt-late':'log-w2.fld.tigge.ecmwf.py.ECMT-LATE',
'oisst':'log-w2-fld-wget-mirror-cpc-oisst.py.CPC.OISST',
'goes':'log-w2-fld-wget-mirror-gfs-stbgoes.py.GFS2',
'goes-loop':'log-w2-gfs-goes-loop-py.GOES',

'cgd2':'log-w2-do-cgd2.py.CGD2',
'ecm4':'log-w2-nwp2.py.ECM4',
'ecm4-12':'log-w2-nwp2.py.ECM4-cur12-12',

'ecm5-late':'log-w2-do-ecm5.py.ECM5-LATE',
'ecm5-very':'log-w2-do-ecm5.py.ECM5-VERYLATE',
'ecm5-miss':'log-w2-do-ecm5.py.ECM5-MISS',
'ecm5':'log-w2-do-ecm5.py.ECM5',

'jgsm':'log-w2-do-jgsm.py.JGSM',

'gfs2-5':'log.do-gfs2.py.GFS2_p505',
'gfs2-6':'log.do-gfs2.py.GFS2_p600',
'gfs2-7':'log.do-gfs2.py.GFS2_p700',
'navg-6':'log.do-navg.py.NAVG_p605',
'navg-7':'log.do-navg.py.NAVG_p731',
'navg-8':'log.do-navg.py.NAVG_p831',
'navg-late':'log.do-navg.py.NAVG_LATE',

'psma-kill':'log-w2-ps-monitor-anl.py.tenki.PS-MONITOR-KILL-LONG-PS',
'psma':'log-w2-ps-monitor.py.tenki.PS-MONITOR',
'eps-all':'log-w2-tc-all-eps.py.EPSPLOTTIGGENCEP',
'eps-allm12':'log-w2-tc-all-eps.py.EPSPLOTTIGGENCEP-M12',
'eps-ncep':'log-w2-tc-all-eps.py.TIGGE-NCEP',
'eps-cmc':'log-w2-tc-all-eps.py.TIGGE-CMC',
#'adc':'log-w2-tc-convert-tm-mftrkN-to-atcf-adeck.py.wxmap2.ADC-all-hourly-AD2',

#'ad2-ecmt':'log-w2-tc-convert-tm-mftrkN-to-atcf-adeck.py.wxmap2.ADC-tmtrkN-AD2-ECMT',
'ad2-jt':'log-w2.tc.dss.ad2.py.wxmap2.AD2-jt-nhc-hourly-AD2',
'ad2-9x':'log-w2.tc.dss.ad2.py.wxmap2.AD2-jt-nhc-tm-mftrkN-hourly-AD2-9X',
'otc':'log-w2-tc-ops-dat.py.TENKILF',
'wmo-det':'log-w2-tc-ecmwf-wmo-essential-bufr-json.py-DET',
'wmo-eps':'log-w2-tc-ecmwf-wmo-essential-bufr-json.py-EPS',
'wmo-epsm12':'log-w2-tc-ecmwf-wmo-essential-bufr-json.py-EPSM12',

'jtd-2':'log-w2-tc-jtdiag.py-JTdiag-ph2-3',
'jtd-op':'log-w2-tc-jtdiag.py-JTdiag-ph2p5',
'jtd-l8':'log-w2-tc-jtdiag.py-JTdiag-LATE',

'pr-q':'log-w2-fld-qmorph.py.CPC-QMORPH',
'pr-c':'log-w2-fld-qmorph.py.CPC-CMORPH',
'pr-qp':'log-w2-fld-qmorph-products.py.qmorph.CPC',
'pr-cp':'log-w2-fld-qmorph-products.py.cmorph.CPC',
'pr-qpg':'log-w2-fld-qmorph-global-products.py.qmorph.CPC',
'pr-cpg':'log-w2-fld-qmorph-global-products.py.cmorph.CPC',

'trk-mod':'log-w2-tc-stm-trkplt.py.TCTRKPLTMOD',
'trk-ops':'log-w2-tc-stm-trkplt.py.TCTRKPLTOPS',

# -- clean .dat in tcanal
#
'tcd-k':'log-w2-tc-lsdiag.py.TCDIAG-CLEAN',

# -- season
#
'tcs-s':'log-w2.cur.clm.py.TC.CLM-SHEM',
'tcs-n':'log-w2.cur.clm.py.TC.CLM-NHEM',

# -- push to wxmap2.com
#
'wx2-p1':'log-w2-tc-active-rsync-wxmap2.py.TCACT2WXMAP2-P1',
'wx2-p2':'log-w2-tc-active-rsync-wxmap2.py.TCACT2WXMAP2-P2',
'wx2-p3':'log-w2-tc-active-rsync-wxmap2.py.TCACT2WXMAP2-P3',
'wx2-p4':'log-w2-tc-active-rsync-wxmap2.py.TCACT2WXMAP2-P4',

'wx2':'log-w2-tc-rsync-mirror-TC-names-DSs-tcvitals-wxmap2.py.TC2WXMAP2',

# -- gmu pulls to mike4
#
'g-o':'log-w2-ocean-oisst-gmu',
'g-r':'log-w2-pr-rsync-gmu.py',
'g-t':'log-w2-tc-rsync-gmu.py',
'g-w2':'log-w2-w2flds-rsync-gm',
'g-we':'log-w2-w2flds-rsync-gm',

# -- gmu push from mike3
#
'gmu-w2':'log-w2-w2flds-rsync-gmu.py.W2FLD-GMU',
'gmu-tc':'log-w2-tc-rsync-gmu.py.TCDAT2GMU',
'gmu-pr':'log-w2-pr-rsync-gmu.py.PR-GMU',
'gmu-o':'log-w2-ocean-oisst-gmu.py.OISST-GMU',
'gmu-p':'log-w2-products-sync-gmu.py.PRODUCTS-GMU',

# -- gmu touch on hopper
#
'gmu-t':'log-w2-touch-gmu.py.tenki.GMU-TOUCH',

}




logdtgincs={
    'cmc2':12,
    
    'ecmt':12,
    
    'ecm2':12,
    'ecm2-12':12,

    'ecm4':12,
    'ecm4-12':12,

    'ecm5':12,
    'ecm5-late':12,
    'ecm5-very':12,
    'ecm5-miss':12,
    
    'cgd2':12,
    
    'gfs2-4':6,
    'gfs2-5':6,
    'gfs2-6':6,
    'gfs2-7':6,

    'navg-6':6,
    'navg-7':6,
    'navg-8':6,
    
    'ngpj-6':6,
    'ngpj-12':6,
    'ukmc':12,
    
    'ukm2-6':6,
    'ukm2-12':6,
    
    'jmac':12,
    
    'ocn':24,
    'ww3':24,
    'ohc':24,
    
}

logDtmin={
    
    'ad2-9x': 0.02,
    'ad2-jt': 0.05,
    
    'cln-w':  0.01,
    'cln-h':  0.01,
    
    'oisst':0.25,
    
    'wmo-eps':0.25,
    'wmo-epsm12':0.15,
    'wmo-det':0.10,
    
    'eps-all':0.10,
    'eps-allm12':0.10,
    'eps-tigge':0.10,
    'eps-cmc':0.10,
    
    'pr-q':0.025,
    'pr-qp':0.025,
    'pr-qpg':0.015,
    'pr-c':0.025,
    'pr-cp':0.025,
    'pr-cpg':0.015,
    
    'gfs2-5':0.01,
    'gfs2-6':0.01,
    'gfs2-7':0.01,
    
    'navg':0.01,
    'navg-6':0.01,
    'navg-7':0.01,
    'navg-8':0.01,
    
    'goes':0.10,

    'jtd-2':0.25,
    'jtd-op':0.25,
    
    'ecm4':0.25,
    'ecm4-12':0.15,
    'ecm5':0.07,
    'ecm5-miss':0.07,
    'ecm5-very':0.07,
    'ecm5-late':0.07,
 
    'psma-kill':0.01,
    'wmo-det':0.04,
    'wmo-eps':0.00,
    'wmo-epsm12':0.04,
    
    'trk-mod':0.01,
    'trk-ops':0.01,
    
    'wx2':0.07,
    'wx2-p1':0.07,
    'wx2-p2':0.07,
    'wx2-p3':0.07,
    'wx2-p4':0.07,
    
    'g-o':0.01,
    'g-t':0.01,
    'g-p':0.01,
    'g-w2':0.01,
    'g-we':0.01,
    
    'gmu-w2':0.01,
    'gmu-tc':0.01,
    'gmu-pr':0.01,
    'gmu-o':0.01,
    
    'oisst':0.1,
    
    
    
    
}

if(w2.onTenki or w2.onGmu):  logs=logsTenki

plogs=logs.keys()
plogs.sort()

logstr='%s'%plogs[0]
for plog in plogs[1:]:
    nn=plogs.index(plog)
    
    if(nn%8 == 0): 
        logstr='%s, \n%s'%(logstr,plog)
    else:
        logstr='%s, %s'%(logstr,plog)
    
class w2CmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv

        self.argv=argv
        self.argopts={
            1:['log',    '%s log file'%(w2.ptmpBaseDir)],
        }

        self.options={
            'showEvent':            ['e:',-999,'i','display event #'],
            'verb':                 ['V',0,1,'verbose'],
            'showAll':              ['A',0,1,'show all events'],
            'timerOnly':            ['T',0,1,'only save timer---- cards'],
            'printfullecard':       ['F',0,1,'printout full ecard'],
        }


        self.purpose='''
parse log files for specific events in: 

%s

(c) 2009-%s Michael Fiorino,NOAA ESRL CIRES'''%(logstr,w2.curyear)

        self.examples='''
%s ecm4       # list events and dtgs
%s ecm4 -e 4  # print event #4 '''



#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# cmdline
#
maxtau=240
argv=sys.argv

CL=w2CmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr


logpdir=w2.ptmpBaseDir

try:
    logfile=logs[log]
except:
    print 'WWW -- for log: ',log,' arimasen...'
    sys.exit()
    
logpath="%s/%s"%(logpdir,logfile)

ldtginc=6
if(log in logdtgincs.keys()): ldtginc=logdtgincs[log]


if(log == 'psma-kill'):
    cmd='grep -i KKKil %s | grep -i utc | grep -i time'%(logpath)
    mf.runcmd(cmd)
    sys.exit()
else:
    loglines=MF.ReadFile2List(logpath)
    


nbegs={}
nends={}

ne=0
gotstart=0
prevlogstart=''
prevtimestart='XX:XX:XX'
if(loglines == None or len(loglines) <= 0):
    print 'III log: ',log,' logpath: ',logpath,' not availalble...bye...'
    sys.exit()

print 'LLL: ',logpath
print '  E#   BBBBBB              EEEEEE               TotTime      Bline    Eline'

for logline in loglines:
    if(verb > 1): print logline[0:-1]
    if(mf.find(logline,'QQQQQ: START')): 
        ne=ne+1
        logstart=logline[0:-1]
        (timestart,dtgymd,ftimestart,dtgstart)=getYMD(logstart,ldtginc)
        nbeg=loglines.index(logline)
        if(verb): print 'BBBBBBB %3d %8d %s %s %7.4f'%(ne,nbeg,dtgymd,timestart,ftimestart)
        nbegs[ne]=(nbeg,dtgymd,ftimestart,dtgstart)
        
    if(mf.find(logline,'QQQQQ:  END')): 
        nend=loglines.index(logline)
        logend=logline[0:-1]
        (timeend,dtgymd,ftimeend,dtgend)=getYMD(logend)
        if(verb): print 'EEEEEEE %3d %8d %s %s %7.4f'%(ne,nend,dtgymd,timeend,ftimeend)
        MF.appendDictList(nends,ne,(nend,dtgymd,ftimeend,dtgstart))

dtimemin=1.0
if(log in logDtmin.keys()):  dtimemin=logDtmin[log]

nes=nends.keys()
nes.sort()
ls=len(nes)

events=[]

ke=nes[0]
e=nends[ke][-1]
kb=1
b=nbegs[kb]

events.append([kb,b,ke,e])

for l in range(1,ls):
    ke=nes[l]
    kb=nes[l-1]+1

    e=nends[ke][-1]
    b=nbegs[kb]
    ne=l+1
    #print 'EEE: ',ne,l,'bb',kb,b,'ee',ke,e
    events.append([kb,b,ke,e])
    
doLess=0
nevents=len(events)
for k in range(0,nevents):
    (kb,b,ke,e)=events[k]
    (nlb,dtgymdb,ftimeb,dtgb)=b
    (nle,dtgymde,ftimee,dtge)=e
    fftimee=float(dtgymde[-2:])*24.0 + ftimee
    fftimeb=float(dtgymdb[-2:])*24.0 + ftimeb
    
    dtime=fftimee-fftimeb
    dtime=dtime*60.0
    if(printfullecard):
        ecard="%7d %s %s %6.2fh %7d %s %s %6.2fh  dt: %6.2f min"%(nlb,dtgymdb,dtgb,ftimeb,nle,dtgymde,dtge,ftimee,dtime)
    else:
        ecard="  %s %6.2fh  %s %6.2fh  %6.2f min"%(dtgb,ftimeb,dtge,ftimee,dtime)
        
    if(dtime > dtimemin or showAll):
        print ' %3d %s  %7d  %7d'%(k,ecard,nlb,nle)
        if(showEvent >= 0 and (showEvent <= nevents and showEvent == k)):
            cards=[]
            timerCards=[]
            doLess=1
            epath='/tmp/log-output.txt'
            try:       os.unlink(epath)
            except:    None
            for i in range(nlb,nle):
                card=loglines[i]
                if(mf.find(card,'----------timer:')):
                    timerCards.append(card)
                #print card[0:-1]
                cards.append(card)
            if(timerOnly):
                MF.WriteList2Path(timerCards, epath)
            else:
                MF.WriteList2Path(cards, epath)
            break
            
    else:
        if(verb): print 'SSSMMMAAALLLLL--- %3d %s'%(k,ecard)
        
if(doLess):
    cmd="less %s"%(epath)
    mf.runcmd(cmd)
    
sys.exit()

