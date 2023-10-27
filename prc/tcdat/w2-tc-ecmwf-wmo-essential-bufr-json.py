#!/usr/bin/env python

#from __future__ import print_function

import collections
from eccodes import *
from tcbase import *
from tcbufr import *
w2=W2()

    
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
            'override':        ['O',0,1,'override adc conversion using -O1 option'],
            'doBufr':          ['B',1,0,'do NOT crack the bufr'],
            'doAD2':           ['A',1,0,'do NOT do adc and ad2'],
            'doWget':          ['W',1,0,'do NOT wget'],
            'doEpsPlots':      ['E',1,0,'do NOT run w2-tc-g-epsanal-dss-ad2.py...'] 
            }

        self.purpose='''
mirror ecmwf wmo essential of tcbufr'''

        self.examples='''
%s 2004010100     : pull from archive dir for 2004'''


MF.sTimer('all')

argv=sys.argv
CL=TcOpsCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# main
#

dtgs=mf.dtg_dtgopt_prc(dtgopt,ddtg=6)

tbdir=w2.TcpsdRR2DatDir

af=w2.EcmwfWmoFtpserver
al=w2.EcmwfWmoLogin
ap=w2.EcmwfWmoPasswd

tbdir=EcmwfWmoBufrLocalDir
obdir=TcAdecksEcmwfDir

#tbdir='/tmp'
#obdir='/tmp'

MF.sTimer('all')
        
tD=TcData(dtgopt=dtgopt)

for dtg in dtgs:

    MF.sTimer('CRACK-wmo-tc: %s'%(dtg))
    rcS=CurShemOverlap(dtg)
    (isShemOver,curyear,curyearp1)=rcS
    sdir="%s0000"%(dtg)
    tdir="%s/%s/%s"%(tbdir,curyear,dtg)
    odir="%s/%s/wmo"%(obdir,curyear)
    
    print 'Processing: ',dtg,'WWW--remove'
    if(ropt == 'norun'):
        print 'process dtg: ',dtg
        continue
    
    if(verb):
        print 'SSS',isShemOver

    mf.ChkDir(tdir,diropt='mk')
    mf.ChkDir(odir,diropt='mk')
    
    odirS=None
    if(isShemOver):
        odirS="%s/%s/wmo"%(obdir,curyearp1)
        mf.ChkDir(odirS,diropt='mk')

    if(doWget):
        MF.sTimer('get-wmo-tc: %s'%(dtg))
        mf.ChangeDir(tdir)
        logpath="%s/db.wget.%s.txt"%(tdir,dtg)
        cmd="wget -nv -m -nd -T 180 -t 2 \"ftp://%s:%s@%s/%s/*tropical_cyclone*\""%(al,ap,af,sdir)
        mf.runcmd(cmd,ropt)
        MF.dTimer('get-wmo-tc: %s'%(dtg))
        
    if(doBufr):
        
        acards={}
        btlatlons=getBTlatlons(dtg, tD)
        
        dfiles=glob.glob("%s/*ECMF*"%(tdir))
        gfiles=glob.glob("%s/*ECEP*"%(tdir))
        bpaths=dfiles+gfiles
        
        # -- test 20200705 to do R50...
        #bdir='/dat1/tc/ecmwf/wmo-essential/2020/2020070500'
        #bfile='A_JSXX19ECEP050000_C_ECMP_20200705000000_tropical_cyclone_track_71L_-89p5degW_30degN_bufr4.bin'
        #bpaths=['%s/%s'%(bdir,bfile)]
        
        # -- debug 20200708
        #--failed
        #bpaths=['/dat1/w21/dat/tc/ecmwf/wmo-essential/2020/2020070800/A_JSXX01ECEP080000_C_ECMP_20200708000000_tropical_cyclone_track_CRISTINA_-104p7degW_13p5degN_bufr4.bin']
        #--works: 
        #bpaths=['/dat1/w21/dat/tc/ecmwf/wmo-essential/2020/2020070800/A_JSXX19ECEP080000_C_ECMP_20200708000000_tropical_cyclone_track_70L_-82p6degW_32p9degN_bufr4.bin']
        # 20200709 -- new bug
        #bpaths=['/dat1/w21/dat/tc/ecmwf/wmo-essential/2020/2020070900/A_JSXX34ECEP090000_C_ECMP_20200709000000_tropical_cyclone_track_70B_94p3degE_27p2degN_bufr4.bin']
        # 20200725 -- new bug with big storm?
        #bpaths=['/dat1/w21/dat/tc/ecmwf/wmo-essential/2020/2020072412/A_JSXX02ECEP241200_C_ECMP_20200724120000_tropical_cyclone_track_DOUGLAS_-141p1degW_16p1degN_bufr4.bin']
        #bpaths=['/dat1/w21/dat/tc/ecmwf/wmo-essential/2020/2020051512/A_JSXX28ECEP151200_C_ECMP_20200515120000_tropical_cyclone_track_70A_63p8degE_3p4degN_bufr4.bin']
        # 20210611 -- bug in this one...fixed in tcbufr.py
        #bpaths=['/data/w22/dat/tc/ecmwf/wmo-essential/2021/2021061018/A_JSXX26ECEP101800_C_ECMP_20210610180000_tropical_cyclone_track_70B_88degE_22p1degN_bufr4.bin']
        for bpath in bpaths:
            print 'BBB: ',bpath,'siz: ',MF.getPathSiz(bpath)
            (bdir,bfile)=os.path.split(bpath)
            MF.sTimer('json-crack-dtg: %s -- Crack: %s'%(dtg,bfile))
            rc=crackJson(bpath, btlatlons, dtg, acards, verb=verb)
            MF.dTimer('json-crack-dtg: %s -- Crack: %s'%(dtg,bfile))

        # -- uniq the acards lisr
        #
        MF.uniqDict2List(acards)
        
        acards=removeDups(acards)
        
        
        if(verb):
            for kk in acards.keys():
                print kk
                ss=acards[kk].keys()
                if('EMDT' in ss):
                    ocards=acards[kk]['EMDT']
                    for ocard in ocards:
                        print ocard.strip()
                    print
                    print
                    
        # -- output
        #
        
        kk1=acards.keys()
        
        gotShem=0
        for k1 in kk1:
            allcards=[]
            kk2=acards[k1].keys()
            for k2 in kk2:
                ocards=acards[k1][k2]
                allcards=allcards+ocards
                
            odirCur=odir
            tt=k1.split('.')
            stmyear=tt[-1]
            if(stmyear == curyearp1):
                opath="%s/adeck-ecmwf-wmo.%s.%s"%(odirS,dtg,k1)
                gotShem=1
            else:
                opath="%s/adeck-ecmwf-wmo.%s.%s"%(odir,dtg,k1)
            print 'OOO: ',opath
            MF.WriteList2Path(allcards, opath)
    
        MF.dTimer('CRACK-wmo-tc: %s'%(dtg))
        
if(ropt == 'norun'):
    sys.exit()
    
# -- do adc and ad2
#
if(doAD2):
    oOpt=''
    if(override): oOpt='-O1'
    MF.sTimer('adc-ad2-update')
    cmd="%s/w2-tc-convert-tm-mftrkN-to-atcf-adeck.py %s -d %s -A %s"%(w2.PrcDirTcdatW2,'ec-wmo',dtgopt,oOpt)
    mf.runcmd(cmd,ropt)
    MF.dTimer('adc-ad2-update')

    MF.sTimer('ad2-9X-update')
    cmd="%s/w2-tc-dss-ad2.py %s -d %s -9"%(w2.PrcDirTcdatW2,'ec-wmo',dtgopt)
    mf.runcmd(cmd,ropt)
    MF.dTimer('ad2-9X-update')

# -- do eps plots
#
if(doEpsPlots):
    MF.sTimer('g.eps-plots')
    cmd="%s/w2-tc-g-epsanal-dss-ad2.py %s ecmb"%(w2.PrcDirTcdatW2,dtgopt)
    mf.runcmd(cmd,ropt)
    MF.dTimer('g.eps-plots')

    # -- rsync to wxmap2.com
    #
    rc=rsync2Wxmap2('tceps',ropt)
    
    
MF.dTimer('all')
sys.exit()




