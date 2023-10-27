"""
config for TC processing

"""

# -- need to clean up-- but old
import os
import sys
import string
import posixpath
import glob
import copy

import math
from math import atan2
from math import atan
from math import pi
from math import fabs
from math import cos
from math import sin
from math import log
from math import tan
from math import acos
from math import sqrt

import time

import w2
import mf
import ATCF
import TCtdos
#import ADr1708 as AD
from tcbase import MakeStmList

from const import  *

StdOutReport=0
PrintReport=1

tcunits='english'
femax=1500.0
cunito='nm'
epsilon=1e-10

def SetTCunits(units):
    global femax,cunito,tcunits
    tcunits=units
    if(tcunits == 'metric'):
        cunito='km'
        femax=femax*nm2km


bdirw2=w2.W2Dir
bdir=w2.W2BaseDir
MfLibrary=bdir+'/lib/python'

BaseDirDataTcCur=w2.TcDatDir
FcCurDir=BaseDirDataTcCur + "/ft_ops"


BaseDirWWW=w2.W2BaseDirWeb
BaseDirWWWTcSitrep=BaseDirWWW+'/tc/sitrep'
BaseDirWWWTcSitrep='/w3/rapb/hfip/tcact'
BaseDirWWWTcSitrep='%s/tcact'%(os.getenv('W2_HFIP'))

BaseDirDataTc=bdirw2+"/dat/tc"
BaseDirPrc=bdir+"/prc"
BaseDirPrcTc=bdir+"/prc/tc"
BaseDirPrcTcDat=bdir+"/prc/tcdat"
BaseDirPrcTcVeri=bdir+"/prc/tcveri"
BaseDirPrcTcClimo=bdir+"/prc/tcclimio"

BaseDirPltTc=w2.TcBaseDirPltTc
PltTcOpsDir="%s/ops"%(BaseDirPltTc)
PltTcOpsTrackDir="%s/track"%(PltTcOpsDir)
PltTcOpsVeriDir="%s/veri"%(PltTcOpsDir)
PltTcOpsClimoDir="%s/climo"%(PltTcOpsDir)
PltTcOpsVitalsDir="%s/vitals"%(PltTcOpsDir)

PltTcClimoDir=BaseDirPltTc+"/climo"
PltTcActivityDir=BaseDirPltTc+"/activity"

FcDir=BaseDirDataTc + "/fc"
FcOpsDir=BaseDirDataTc + "/fc/ops"

EcmwfFcDir=BaseDirDataTc + "/fc/ecmwf/eps"
EcmwfFcTxtDir=BaseDirDataTc + "/ecmwf/txt_trackers"
EcmwfFcMslDir=BaseDirDataTc + "/ecmwf/pcmdi/ecmwf/eps_msl_2002_2003"

EcmwfBufrLocalDir=BaseDirDataTc + '/ecmwf/bufr'
EcmwfBufrNCOLocalDir='/mnt/model/ecmwf/tracker'

JmaLocalDir=BaseDirDataTc + '/jma'

JtwcAtcfArchiveDir=BaseDirDataTc + '/jtwc/archive'

Nhc2JtwcFtpServer='moonfish.nhc.noaa.gov'

FiltDir=BaseDirDataTc + "/filt"
VeriDir=BaseDirDataTc + "/veri"


RptDir=bdir + "/rpt"
RptTcDir=bdir + "/rpt/tc"
RptTcOpsDir=bdir + "/rpt/tc/ops"
RptTcOpsVeriDir="%s/veri"%(RptTcOpsDir)

BtOpsDir="/pcmdi/tenki_dat/nwp/dat/tc"

BdeckDir=BaseDirDataTc + "/bdeck"
BdeckDirNrl=BdeckDir + '/nrl'
BdeckDirNhc=BdeckDir + '/nhc'
BdeckDirJtwc=BdeckDir + '/jtwc'
BdeckDirNeumann=BdeckDir + '/neumann'
BdeckDirHurdat=BdeckDir + '/hurdat'

AdeckDir=BaseDirDataTc + '/adeck'
AdeckDirEcmwf=AdeckDir + '/ecmwf'
AdeckDirJtwc=AdeckDir + '/jtwc'
AdeckDirJma=AdeckDir + '/jma'
AdeckDirNhc=AdeckDir + '/nhc'
AdeckDirNcep=AdeckDir + '/ncep'
AdeckDirTpc=AdeckDir + '/tpc'
AdeckDirNhcOps=AdeckDir + '/nhc/moonfish'
AdeckDirNrl=AdeckDir + '/nrl'
AdeckDirNasa=AdeckDir + '/nasa'
AdeckDirJma=AdeckDir + '/jma'
AdeckDirGsd=AdeckDir + '/gsd'
AdeckDirHrd=AdeckDir + '/hrd'
AdeckDirW2=AdeckDir + '/wxmap2'

AdeckDirJtwcEcmwf=AdeckDir + '/jtwc/ecmwf'

AdeckDirLocal=AdeckDir + '/local'

AdeckSourceDirTpc=BaseDirDataTc + '/ncep/tpc'
AdeckSourceDirGsd='/model/gsd/ATCF'
AdeckSourceDirHrd=AdeckDirHrd

eBdeckDir=BaseDirDataTc + "/ebt"


VdeckDir=BaseDirDataTc + '/vdeck'
MdeckDir=BaseDirDataTc + '/mdeck'

BaseDirDatTcusb2='/media/NO_NAME1/kishou/work/wxmap2/dat/tc'
BaseDirDatTcusb2='/media/usbdisk/kishou/work/wxmap2/dat/tc'
BaseDirDatTcusb2='/storage2/kishou/work/wxmap2/dat/tc'
##### 20080825 - shift to storage4, storage2 usb2 disk overheated
BaseDirDatTcusb2='/storage4/kishou/wxmap2/dat/tc'

TcanalDatDir=BaseDirDataTc + '/tcanal'
TcanalDatDirusb2=BaseDirDatTcusb2 + '/tcanal'


StormsDirArchiveNhc="/home/mfiorino/databases/atcf/archives"
StormsDirArchiveFinalNhc="/home/mfiorino/databases/atcfdatabase/archive"
StormsDirNhc="/home/mfiorino/databases/atcf/storms"
StormsDirAdeckNhc="/home/mfiorino/databases/atcfdatabase/aid_nws"
StormsDirBdeckNhc="/home/mfiorino/databases/atcfdatabase/btk"


YearsBackClimo=32
YearsBackClimoTss=[4,8,16,32]
YearTcBtNeumann=1945

MITtdir='fiorino'
MITserver='wind.mit.edu'

#
# basin parameters
#
primeMeridianChk=60.0

#
# tc parameters/limits
#
TCvmin=25

vmaxTS=35.0
vmaxTY=65.0

#
# vdeck hit and dup distances -> w2.tc.vdeck.py
#
vdeckHitDist=250.0
vdeckDupDist=120.0


VdeckModels=['gfs','ngp','ukm','clp','fv4','fv5','eco','ece','ofc','con','fg4','fd5',
             'egr','ofi','cn3','cn4','cne','cnf','pne','avo','avi',
             'gfd','gfi','fss',
             'uko','ngn']

VdeckModels=['gfs','ngp','ukm','clp','eco','ece','ofc','con',
             'egr','ofi','cn3','cn4','cne','pne','avo','avi',
             'gfd','gfi',
             'fss',
             'uko','uki',
             'ngn']

VdeckModels=[
    'clp','gfs','ngp','ukm','ecm','cmc',
    ]

VeriRules=['jtwc','jtwc.pure','jtwc.mod','nhc.pure','nhc.wind','td30']

Vtaus=range(0,120+1,12)

ClimoBasinsHemi = {
    'NHS':['nhem','wpac','epac','lant','nio','shem','global'],
    'SHS':['shem','sio','swpac','nhem','global'],
    }

Basin2toBasin1 = {
    'IO':'I',
    'SH':'P',
    'SH':'S',
    'SI':'S',
    'SP':'P',
    'WP':'W',
    'CP':'C',
    'EP':'E',
    'AT':'L',
    'AL':'L',
    'NA':'L',
    'SL':'Q',
    'SA':'T',
    'BB':'B',
    'AS':'A',
    'XX':'X',
    }

Basin2toBasin1Tpc = {
    'IO':'I',
    'SP':'P',
    'SL':'Q',
    'SI':'S',
    'WP':'W',
    'CP':'C',
    'EP':'E',
    'AL':'L',
    'NA':'A',
    'BB':'B',
    }


Basin1toBasin2 = {
    'A':'IO',
    'B':'IO',
    'L':'AT',
    'L':'AL',
    'I':'IO',
    'S':'SH',
    'P':'SH',
    'W':'WP',
    'C':'CP',
    'E':'EP',
    'Q':'SL',
    'X':'XX',
    }

Basin1toForecastCenter = {
    'A':'JTWC',
    'B':'JTWC',
    'L':'NHC',
    'I':'JTWC',
    'S':'JTWC',
    'P':'JTWC',
    'W':'JTWC',
    'C':'CPHC',
    'E':'NHC',
    'Q':'NHC',
    'X':'XHC',
    }

Basin1toButtonStyle = {
    'A':'bnio',
    'B':'bnio',
    'L':'blant',
    'I':'bnio',
    'S':'bsio',
    'P':'bspac',
    'W':'bwpac',
    'C':'bcpac',
    'E':'bepac',
    'Q':'blant',
    }

Basin1toButtonColor = {
    'A':'wheat',
    'B':'wheat',
    'L':'pink',
    'I':'wheat',
    'S':'#ADD8E6',
    'P':'#EE82EE',
    'W':'#EE82EE',
    'C':'lightgreen',
    'E':'lightgrey',
    'Q':'pink',
    }

Basin1toBasinNumber = {
    'L':'1',
    'E':'2',
    'W':'3',
    'C':'4',
    'A':'5',
    'B':'6',
    'I':'7',
    'S':'8',
    'P':'9',
    'Q':'10',
    }

Basin1toBasinName = {
    'A':'   ASEA - Arabian Sea',
    'B':'   BAYB - Bay of Bengal',
    'L':'   LANT - north Atlantic',
    'I':'    NIO - north Indian Ocean',
    'S':'    SIO - south Indian Ocean',
    'P':'  SPWAC - southwest Pacific',
    'W':'WESTPAC - western North Pacific',
    'C':'CENTPAC - central North Pacific',
    'E':'EASTPAC - eastern North Pacific',
    'Q':'  SLANT - south Atlantic'
    }

Basin1toBasinNameShort = {
    'A':'ASEA',
    'B':'BAYB',
    'L':'LANT',
    'I':'NIO',
    'S':'SIO',
    'P':'SPWAC',
    'W':'WESTPAC',
    'C':'CENTPAC',
    'E':'EASTPAC',
    'Q':'SLANT'
    }

Basin1toHemi = {
    'A':'N',
    'B':'N',
    'L':'N',
    'I':'N',
    'S':'S',
    'P':'S',
    'W':'N',
    'C':'N',
    'E':'N',
    'Q':'S',
    }

Basin1toHemi3 = {
    'A':'NHS',
    'B':'NHS',
    'L':'NHS',
    'I':'NHS',
    'S':'SHS',
    'P':'SHS',
    'W':'NHS',
    'C':'NHS',
    'E':'NHS',
    'Q':'SHS',
    }

Basin1toHemi4 = {
    'A':'nhem',
    'B':'nhem',
    'L':'nhem',
    'I':'nhem',
    'S':'shem',
    'P':'shem',
    'W':'nhem',
    'C':'nhem',
    'E':'nhem',
    'Q':'shem',
    }

Basin1toBasin3 = {
    'A':'nio',
    'B':'nio',
    'I':'nio',
    'L':'atl',
    'S':'shm',
    'P':'shm',
    'W':'wpc',
    'C':'epc',
    'E':'epc',
    'Q':'slt',
    }

SuperBasins=['NHS','SHS','LTS','WPS','EPS','NIS']

Hemi1toHemiName = {
    'NHS':'NHEM Super Basin',
    'SHS':'SHEM Super Basin',
    'LTS':'LANT Super Basin',
    'WPS':'WPAC Super Basin',
    'EPS':'EPAC Super Basin',
    'NIS':'NIO  Super Basin',
    }

Hemi3toHemiName = {
    'NHS':'NHEM Super Basin',
    'SHS':'SHEM Super Basin',
    'LTS':'LANT Super Basin',
    'WPS':'WPAC Super Basin',
    'EPS':'EPAC Super Basin',
    'NIS':'NIO  Super Basin',
    }

Hemi3toHemiNameShort = {
    'NHS':'NHEM',
    'SHS':'SHEM',
    'LTS':'LANT SB',
    'WPS':'WPAC SB',
    'EPS':'EPAC SB',
    'NIS':'NIO  SB',
    }

Hemi1toHemiVeriName = {
    'NHS':'nhem',
    'SHS':'shem',
    'LTS':'lant',
    'WPS':'wpac',
    'EPS':'epac',
    'NIS':'nio',
    }

Hemi1toBasins = {
    'NHS':('A','B','I','W','C','E','L'),
    'SHS':('S','P','Q'),
    'LTS':('L'),
    'WPS':('W'),
    'EPS':('C','E'),
    'NIS':('A','B','I'),
    }

Hemi3toBasins = {
    'NHS':('A','B','I','W','C','E','L'),
    'SHS':('S','P','Q'),
    'LTS':('L'),
    'WPS':('W'),
    'EPS':('C','E'),
    'NIS':('A','B','I'),
    }

Hemi3toSuperBasins = {
    'NHS':('NHS','NIS','WPS','EPS','LTS'),
    'SHS':('SHS','S','P','Q'),
    }

BasinsAll=['L','E','C','W','A','B','I','S','P','Q']

TrkModels=['ofc','clp','gfs','ngp','ukm','eco','ece','btk','fv4','fv5','con','fg4','fd5',
           'egr','ofi','cn3','cn4','cne','cnf','pne','gfd']

TcanalModelsoff=['gfs','ngp','ukm']

TcanalModels2005=['gfs','ngp','ukm','fg4']

TcanalModels=['gfs2','fim8','ecm2','ngp2','ukm2']
TcanalModelsoff=['gfs2','ukm2']

def VeriTcFlag(tcind,tcwarn):
    vflg=0
    if(tcind == 'TC' or tcwarn == 'WN'):
        vflg=1

    return(vflg)


def IsJtwcBasin(b1id):
    bid=b1id.lower()
    rc=0
    if(
        bid == 'w' or bid == 'b' or bid == 'a' or
        bid == 's' or bid == 'p'
        ):
        rc=1
        
    return(rc)

def IsNhcBasin(b1id):
    bid=b1id.lower()
    rc=0
    if(
        bid == 'l' or bid == 'e' or bid == 'c'
        ):
        rc=1
        
    return(rc)

    

def IsTc(tcstate):
    #
    # if tc = 1
    # if stc = 2
    # if neither = 0
    #
    if(
        tcstate == 'TD' or
        tcstate == 'TS' or
        tcstate == 'TY' or
        tcstate == 'HU' or
        tcstate == 'ST' or
        tcstate == 'TC'
        ):
        tc=1
    elif(
        tcstate == 'SS' or
        tcstate == 'SD'
        ):
        tc=2
    elif(
        tcstate.lower() == 'xx'
        ):
        tc=-1
    else:
        tc=0

    return(tc)

#
# if tcflag not in bdeck, use find
#

def IsTcWind(vmax):

    tc=0
    if(vmax >= TCvmin): tc=1
    return(tc)


def IsWarn(warnstate):
    #
    # if tc = 1
    # if stc = 2
    # if neither = 0
    #
    if(
        warnstate == 'WN'
        ):
        warn=1
    else:
        warn=0

    return(warn)
    
    

def IsTcList(tt):
  
    try:
        vmax=int(tt[2])
        tcstate=tt[13]
        warnstate=tt[15]
    except:
        try:
            vmax=int(tt[2])
            tcstate=tt[12]
            warnstate=tt[14]
        except:
            vmax=0
            tcstate='xx'
            
    if(vmax >= TCvmin and (tcstate.lower() == 'xx' )): tcstate='TC'
    
    tc=IsTc(tcstate)

    return(tc)
    

def IsWarnList(tt):
  
    try:
        vmax=int(tt[2])
        tcstate=tt[13]
        warnstate=tt[15]
    except:
        try:
            vmax=int(tt[2])
            tcstate=tt[12]
            warnstate=tt[14]
        except:
            tcstate='xx'

    if(vmax >= TCvmin and (tcstate.lower() == 'xx' )): tcstate='TC'
    
    warn=IsWarn(warnstate)

    return(tc)
    



def GetTCnamesHash(yyyy,source=''):

    ndir=w2.TcNamesDatDir
    sys.path.append(ndir)
    if(source == 'neumann'):
        impcmd="from TCnamesNeumann%s import tcnames"%(yyyy)
    elif(source == 'ops'):
        impcmd="from TCnamesOps%s import tcnames"%(yyyy)
    else:
        impcmd="from TCnames%s import tcnames"%(yyyy)
    exec(impcmd)
    return(tcnames)


def GetTCstatsHash(yyyy,source=''):
    
    ndir=w2.TcNamesDatDir
    sys.path.append(ndir)
    if(source == 'neumann'):
        impcmd="from TCstatsNeumann%s import tcstats"%(yyyy)
    elif(source == 'ops'):
        impcmd="from TCstatsOps%s import tcstats"%(yyyy)
    else:
        impcmd="from TCstats%s import tcstats"%(yyyy)
    exec(impcmd)
    return(tcstats)



def HolidayAtkinsonPsl2Vmax(psl):

    vmax=0.0
    if(psl < 880.0):
        vmax=154.0
    elif(psl >= 880.0 and psl < 885.0):
        vmax=150.0
    elif(psl >= 850.0 and psl < 890.0):
        vmax=146.0
    elif(psl >= 890.0 and psl < 895.0):
        vmax=142.0
    elif(psl >= 895.0 and psl < 900.0):
        vmax=138.0
    elif(psl >= 900.0 and psl < 905.0):
        vmax=134.0
    elif(psl >= 905.0 and psl < 910.0):
        vmax=130.0
    elif(psl >= 910.0 and psl < 915.0):
        vmax=126.0
    elif(psl >= 915.0 and psl < 920.0):
        vmax=122.0
    elif(psl >= 920.0 and psl < 925.0):
        vmax=117.0
    elif(psl >= 925.0 and psl < 930.0):
        vmax=113.0
    elif(psl >= 930.0 and psl < 935.0):
        vmax=108.0
    elif(psl >= 935.0 and psl < 940.0):
        vmax=103.0
    elif(psl >= 940.0 and psl < 945.0):
        vmax=99.0
    elif(psl >= 945.0 and psl < 950.0):
        vmax=94.0
    elif(psl >= 950.0 and psl < 955.0):
        vmax=88.0
    elif(psl >= 955.0 and psl < 960.0):
        vmax=83.0
    elif(psl >= 960.0 and psl < 965.0):
        vmax=78.0
    elif(psl >= 965.0 and psl < 970.0):
        vmax=72.0
    elif(psl >= 970.0 and psl < 975.0):
        vmax=66.0
    elif(psl >= 975.0 and psl < 980.0):
        vmax=60.0
    elif(psl >= 980.0 and psl < 985.0):
        vmax=53.0
    elif(psl >= 985.0 and psl < 990.0):
        vmax=46.0
    elif(psl >= 990.0 and psl < 995.0):
        vmax=38.0
    elif(psl >= 995.0 and psl < 1000.0):
        vmax=30.0
    elif(psl >= 1000.0 and psl < 1005.0):
        vmax=22.0
    elif(psl >= 1005.0):
        vmax=20.0

    return(vmax)


def GetTCName(s,quiet=1):

    warn=1

    sid=s.split('.')[0]
    yyyy=s.split('.')[1]

    tcnames=GetTCnamesHash(yyyy)

    try:
        sname=tcnames[yyyy,sid]
    except:
        yyyym1=mf.yyyyinc(yyyy,-1)
        try:
            tcnamesm1=GetTCnamesHash(yyyym1)
            sname=tcnamesm1[str(yyyym1),sid]
            if(warn): print 'wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww'
            if(warn): print 'WWWW looking for name from previous year'
            if(warn): print 'WWWW ',yyyym1,s,sname
            if(warn): print 'wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww'
        except:
            sname='UNKNOWN'
            if(not(quiet)):
                print "WWW unable to find storm name for: %s :: %s setting to %s"%(yyyy,sid,sname)
            #sys.exit()
                                                                  
            
    return(sname)
                

def GetTCStats(s):

    warn=1

    sid=s.split('.')[0]
    yyyy=s.split('.')[1]

    tcstats=GetTCstatsHash(yyyy)

    try:
        stats=tcstats[yyyy,sid]
    except:
        yyyym1=mf.yyyyinc(yyyy,-1)
        try:
            tcstatsm1=GetTCstatsHash(yyyym1)
            stats=tcstatsm1[str(yyyym1),sid]
            if(warn): print 'wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww'
            if(warn): print 'WWWW looking for name from previous year'
            if(warn): print 'WWWW ',yyyym1,s,sname
            if(warn): print 'wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww'
        except:
            stats=None
            print "WWWW unable to find storm stats for: %s :: %s"%(yyyy,sid)
                                                                  
            
    return(stats)
                


def Track2Adeck(model,track):

    adeck=[]
    a=open(adeckpath,'w')
    return(adeck)

def WriteAdeck(adeck,path):

    adeck=[]
    adeckpath="%s/wxmap.%s.%s.%s.txt"%(otdir,model,dtg,stmlow)
    

def Clatlon2Rlatlon(clat,clon):

    if(len(clat) == 1):
        return(0.0,0.0,0,0,'X','X')
    
    hemns=clat[len(clat)-1:]
    hemew=clon[len(clon)-1:]
    ilat=clat[0:(len(clat)-1)]
    rlat=int(ilat)*0.1
    ilon=clon[0:(len(clon)-1)]
    rlon=int(ilon)*0.1

    if(hemns == 'S'):
        rlat=-rlat
        
    if(hemew == 'W'):
        rlon=360.0-rlon

    return(rlat,rlon,ilat,ilon,hemns,hemew)

def Rlatlon2Clatlon(rlat,rlon,dotens=1):

    hemns='X'
    hemew='X'
    ilat=999
    ilon=9999
    
    if(rlat > -90.0 and rlat < 88.0):

        if(dotens):
            ilat=mf.nint(rlat*10)
        else:
            ilat=mf.nint(rlat)

        hemns='N'
        if(ilat<0):
            ilat=abs(ilat)
            hemns='S'

        if(rlon > 180.0):
            rlon=360.0-rlon
            hemew='W'
        else:
            hemew='E'
            
        if(rlon < 0.0):
            rlon=abs(rlon)
            hemew='W'

        if(dotens):
            ilon=mf.nint(rlon*10)
        else:
            ilon=mf.nint(rlon)

    if(dotens):
        clat="%03d%s"%(ilat,hemns)
        clon="%04d%s"%(ilon,hemew)
        clat="%3d%s"%(ilat,hemns)
        clon="%4d%s"%(ilon,hemew)
    else:
        clat="%2d%s"%(ilat,hemns)
        clon="%3d%s"%(ilon,hemew)
    
    return(clat,clon,ilat,ilon,hemns,hemew)




def VeriModelOmodel(model,phr=None):

    omodel=model
    vomodel=model
    if(model == 'era40.256.fc'): omodel='e40'
    if(model == 'era40'): omodel='e40'
    if(phr != None):
        vomodel="%s%02d"%(model,int(phr))
    else:
        vomodel="%s%2s"%(model,'  ')   # really want to do this?
        vomodel=model
    
    return(omodel,vomodel)

def VeriModelOmodelOld(model,phr=None):

    omodel=model
    if(model == 'era40.256.fc'): omodel='e40'
    if(model == 'era40'): omodel='e40'
    if(phr != None):
        vomodel="%s%02d"%(model,int(phr))
    else:
        vomodel="%s%2s"%(model,'  ')   # really want to do this?
        vomodel=model
    
    return(omodel)


def ModelDataBdir(model):

    if(model == 'era40'):
        ddir='/pcmdi/reanal/ecmwf/era40/fc/tcanal'
    elif(model == 'gfs' or model == 'ukm' or model == 'ngp'):
        ddir=w2.NwpDataBdir(model)
        
    return(ddir)

#
# new version
#

def ModelFcDir(model,mopt=None):

    if(len(model.split('.')) == 2):
        model=model.split('.')[0]
        mopt=model.split('.')[1]

    if(mopt == 'ops'):
        ftdir="%s/%s"%(FcDir,mopt)
        return(ftdir)
              
    if(model == 'era40' or model == 'eclp'):
        ftdir="%s/era40"%(FcDir)
    elif(model == 'ecm'):
        ftdir="%s/ecmwf/ifs"%(FcDir)
    elif(model == 'ngp'):
        ftdir="%s/fnmoc/ngp"%(FcDir)
    elif(model == 'gfs'):
        ftdir="%s/ncep/gfs"%(FcDir)
    elif(model == 'mrf'):
        ftdir="%s/ncep/mrf"%(FcDir)
    elif(model == 'ukm'):
        ftdir="%s/ncep/ukm"%(FcDir)
    elif(model == 'clp'):
        ftdir="%s/clp"%(FcDir)
    #
    # adecks generated from ecmwf ftp push go to ops dir, since 20030801
    #
    elif(model == 'ofc'):
        ftdir="%s/ops"%(FcDir)
    elif(model == 'eco'):
        ftdir="%s/ops"%(FcDir)
    elif(model == 'ece'):
        ftdir="%s/ops"%(FcDir)
    else:
        ftdir=FcDir

    return(ftdir)

    


def NgtrkParms(model):

    dlonmax=6.0
    vortcrit=3.5

    return(dlonmax,vortcrit)

def ModelRes(model):
    res='10'
    if(model == 'ukm'): res='12'
    if(model == 'era40'): res='10'
    if(model == 'gfs'): res='10'
    if(model == 'ngp'): res='10'

    return(res)

def ModelDataCtlPath(model,dtg):

    if(model == 'era40'):
        yyyy=dtg[0:4]
        ddir="%s/%s"%(ModelDataBdir(model),yyyy)
        mask="%s/*%s*ctl"%(ddir,dtg)
    elif(model == 'gfs' or model == 'ukm' or model == 'ngp'):
        ddir=ModelDataBdir(model)
        mask="%s/*%s*%s*ctl"%(ddir,model,dtg)
    elif(model == 'clp'):
        return(None,None)
        
    
    ls=glob.glob(mask)
    if(len(ls) == 1):
        path=ls[0]
        (dir,file)=posixpath.split(path)
        return(dir,file)
    else:
        return(0,0)
        
    return(dctlfile)

def vcparseNoCtAtOld(card):
    tt=string.split(card)
    f=string.atof
    ttt=(tt[0],tt[1],tt[2],tt[2][0:2],tt[2][2:3],tt[3],tt[4],
         f(tt[6]),f(tt[7]),f(tt[9]),f(tt[10]),
         f(tt[12]),f(tt[14]),f(tt[16]))
#    (model,tau,sid,snum,sbasin,bdtg,vdtg,
#     flat,flon,blat,blon,
#     fe,bvmax,fvmax)
    
    return(ttt)

    
def vcparseOld(card):

    f=string.atof
    tt=string.split(card)
    #
    # add year to 3-char storm id
    #
    #    (model,tau,sid,snum,sbasin,bdtg,vdtg,flat,flon,blat,blon,
    #     fe,bvmax,fvmax,cte,ate)=TC.vcparse(c)

    fe=f(tt[12])
    cte=f(tt[25])
    ate=f(tt[26])
    fve=f(tt[34])
    fveu=f(tt[35])

    if(tcunits == 'metric' and fe >= 0.0):
        fe=fe*nm2km
        cte=cte*nm2km
        ate=ate*nm2km
        fve=fve*knots2ms
        fveu=fveu*knots2ms


    if(len(tt[2].split('.')) == 1):
        sid="%s.%s"%(tt[2],tt[3][0:4])
    else:
        sid=tt[2]

    ttt=(tt[0],tt[1],sid,tt[2][0:2],tt[2][2:3],tt[3],tt[4],
         f(tt[6]),f(tt[7]),f(tt[9]),f(tt[10]),fe,f(tt[14]),f(tt[16]),
         cte,ate,fve,fveu)
    return(ttt)



def vcparseNoCtAt(card):
    tt=string.split(card)
    f=string.atof
    ttt=(tt[0],tt[1],tt[2],tt[2][0:2],tt[2][2:3],tt[3],tt[4],
         f(tt[6]),f(tt[7]),f(tt[9]),f(tt[10]),
         f(tt[12]),f(tt[14]),f(tt[16]))
#    (model,tau,sid,snum,sbasin,bdtg,vdtg,
#     flat,flon,blat,blon,
#     fe,bvmax,fvmax)

    return(ttt)


def vcparse(card):

# 0   1     2         3          4        5     6     7  8  9 10 11 12   13  14  15     16   17    18    19 
#ofc 000 12L.2005 2005082318 2005082318 FLG: BTC_Fee TC TD CQ WN CQ WN  TDO: SRS FE:    8.2  LF:  0.03  0.03
#
# 20     21     22  23    24     25  26    27     28  29    30    31   32    33    34   35    36  37    38 
#Bmot:   75.4  11.9 BP:  28.3  317.8 CP: -99.9 -999.9 WP: -99.9 -999.9 FP:  91.9  911.9 BW:  35.0 FW: -88.8
#
#39     40  41    42   43    44      45    46     47     48    49  50   51          52      53
#CW: -999.0 WW: -999.0 FS: -888.8  -88.8 -888.8  -88.8 -888.8  CT: CC CT_AT(nm):  9999.9  9999.9
#
# 54    55  56    57   58   59   60   61   62
#BVd: -999 FVd: -999 -999 -999 -999 -999 -999

#   (model,tau,sid,snum,sbasin,bdtg,vdtg,flat,flon,blat,blon,
#     fe,bvmax,fvmax,cte,ate,fve,fveu)=vcparse(c)
     
    f=float
    tt=card.split()
    
    #
    # add year to 3-char storm id
    #
    #    (model,tau,sid,snum,sbasin,bdtg,vdtg,flat,flon,blat,blon,
    #     fe,bvmax,fvmax,cte,ate)=TC.vcparse(c)

    model=tt[0]
    tau=tt[1]
    
    fe=f(tt[16])
    cte=f(tt[52])
    ate=f(tt[53])
    fve=f(tt[61])
    fveu=f(tt[62])

    if(len(tt[2].split('.')) == 1):
        sid="%s.%s"%(tt[2],tt[3][0:4])
    else:
        sid=tt[2]
        
    snum=tt[2][0:2]
    sbasin=tt[2][2:3]
    bdtg=tt[3]
    vdtg=tt[4]

    flat=f(tt[33])
    flon=f(tt[34])
    blat=f(tt[24])
    blon=f(tt[25])
    
    bvmax=f(tt[36])
    fvmax=f(tt[38])
    
    if(tcunits == 'metric' and fe >= 0.0):
        fe=fe*nm2km
        cte=cte*nm2km
        ate=ate*nm2km
        fve=fve*knots2ms
        fveu=fveu*knots2ms
        
    ttt=(model,tau,sid,snum,sbasin,bdtg,vdtg,flat,flon,blat,blon,
         fe,bvmax,fvmax,cte,ate,fve,fveu)

    return(ttt)



def gc_dist(rlat0,rlon0,rlat1,rlon1):

    #
    # based on sherical law of cosines 
    #
    
    dlat=abs(rlat0-rlat1)
    dlon=abs(rlon0-rlon1)
    zerotest=(dlat<epsilon and dlon<epsilon)
    if(zerotest): return(0.0)
    
    f1=deg2rad*rlat0
    f2=deg2rad*rlat1
    rm=deg2rad*(rlon0-rlon1)
    finv=cos(f1)*cos(f2)*cos(rm)+sin(f1)*sin(f2)
    rr=rearth*acos(finv)
    if(tcunits =='english'): rr=rr*km2nm 

    return(rr)


def mercat(rlat,rlon):

    lat=rlat*deg2rad

    if(rlon < 0.0):
        lon=360.0+rlon
    else:
        lon=rlon
        
    x=lon*deg2rad
    y=log(tan(pi4+lat*0.5))

    return(x,y)

def gc_theta(blat1,blon1,flat1,flon1):

    verb=0
    (xa,ya)=mercat(flat1,flon1)
    (xr,yr)=mercat(blat1,blon1)

    difx=xa-xr
    dify=ya-yr

    difx=difx*rad2deg*deglat2nm
    dify=dify*rad2deg*deglat2nm

    if (difx == 0.0):

        if(dify >= 0.0): theta=pi2
        if(dify < 0.0): theta=3*pi/2.0 

    else:

        slope=dify/difx
        if (abs(slope) < 1e-10):
            if(dify >= 0.0): theta=pi2 
            if(dify <= 0.0): theta=pi
        else:
            theta=atan2(dify,difx)
            #if(theta < 0.0):
            #   theta=theta + 2.0*pi
            theta=theta*rad2deg
            return(difx,dify,theta)
        
            if (difx > 0.0):
                if(dify < 0.0): theta=pi-theta
            else:
                if (dify > 0.0):
                    theta=2*pi+theta
                    theta=theta
                else:
                    theta=pi+theta
                    theta=theta

    
    #if(theta < 0.0):
    #    theta=theta + 2.0*pi

    theta=theta*rad2deg
    return(difx,dify,theta)


def dist_err(blat,blon,blat1,blon1,flat,flon):

    verb=0
    (xa,ya)=mercat(flat,flon)
    (xb,yb)=mercat(blat,blon)
    (xr,yr)=mercat(blat1,blon1)

    difx=xb-xr
    dify=yb-yr

    if (difx == 0.0):

      if(dify >= 0.0): theta=0.0
      if(dify < 0.0): theta=pi 

    else:

      slope=dify/difx
      if (abs(slope) < 1e-10):
          if(difx > 0): theta=pi2 
          if(difx < 0): theta=3*pi/2.0
      else:
        theta=atan(1./slope)
        if (difx > 0.0):
          if(dify < 0.0): theta=pi-theta
        else:
           if (dify > 0.):
             theta=2*pi+theta
           else:
             theta=pi+theta

    biasx=cos(theta)*(xa-xb)-sin(theta)*(ya-yb)
    biasy=sin(theta)*(xa-xb)+cos(theta)*(ya-yb)
    factor=cos(deg2rad*(blat+flat)*0.5)
    biasx=biasx*rearth*factor
    biasy=biasy*rearth*factor

    biasew=(xa-xb)*rearth*factor
    biasns=(ya-yb)*rearth*factor
    rr=sqrt(biasx*biasx+biasy*biasy)
    #dist_x=abs(biasx)
    #dist_y=abs(biasy)

    if(tcunits =='english'):
        rr=rr*km2nm
        biasx=biasx*km2nm
        biasy=biasy*km2nm
        biasew=biasew*km2nm
        biasns=biasns*km2nm
        

    if(verb):
        print "mmm ",blat,blon,flat,flon,rr,biasx,biasy

    return(rr,biasx,biasy,biasew,biasns)


def rumltlg(course,speed,dt,rlat0,rlon0):

    ####  print "qqq course,speed,dt,rlat0,rlon0\n"
    #c****	    routine to calculate lat,lon after traveling "dt" time
    #c****	    along a rhumb line specifed by the course and speed
    #c****	    of motion
    #
    #--- assume DEG E!!!!!!!!!!!!!!!!!!!!!!!!
    #
    #  assume speed is in kts and dt is hours
    #
    #      
    distnce=speed*dt
    
    icrse=int(course+0.01)

    if(icrse == 90.0 or icrse == 270.0):

    #      
    #*****		  take care of due east and west motion
    #
        dlon=distnce/(60.0*cos(rlat0*deg2rad))
        if(icrse == 90.0): rlon1=rlon0+dlon
        if(icrse == 270.0): rlon1=rlon0-dlon 
        rlat1=rlat0
    else:
        rlat1=rlat0+distnce*cos(course*deg2rad)/60.0
        d1=(45.0+0.5*rlat1)*deg2rad
        d2=(45.0+0.5*rlat0)*deg2rad
        td1=tan(d1)
        td2=tan(d2)
        #
        # going over the poles!
        #
        if(abs(rlat0) >= 90.0 or abs(rlat1) >= 90.0):
            rlat1=rlon1=None
        else:
            rlogtd1=log(td1)
            rlogtd2=log(td2)
            rdenom=rlogtd1-rlogtd2 
            rlon1=rlon0+(tan(course*deg2rad)*rdenom)*rad2deg

    return(rlat1,rlon1)


def rumhdsp(rlat0,rlon0,rlat1,rlon1,dt,units=tcunits,opt=0):

    verb=0

    if(verb):
        print "***** ",rlat0,rlon0,rlat1,rlon1,dt,units,opt

    if(units == 'metric'):
        distfac=111.19
        spdfac=0.2777
    else:
        distfac=60.0
        spdfac=1.0


    #
    # assumes deg W
    #
    rnumtor=(rlon0-rlon1)*deg2rad

    #
    #--- assume DEG E!!!!!!!!!!!!!!!!!!!!!!!!
    #

    rnumtor=(rlon1-rlon0)*deg2rad
    d1=(45.0+0.5*rlat1)*deg2rad
    d2=(45.0+0.5*rlat0)*deg2rad

    td1=tan(d1)
    td2=tan(d2)
    rlogtd1=log(td1)
    rlogtd2=log(td2)
    rdenom=rlogtd1-rlogtd2
    rmag=rnumtor*rnumtor + rdenom*rdenom

    course=0.0
    if(rmag != 0.0):
        course=atan2(rnumtor,rdenom)*rad2deg

    if(course <= 0.0):  
        course=360.0+course

    #
    #...     now find distance
    #

    icourse=int(course+0.1)
    if(icourse ==  90.0 or icourse == 270.0 ):
        distance=distfac*abs(rlon0-rlon1)*cos(rlat0*deg2rad)
    else:
        distance=distfac*abs(rlat0-rlat1)/abs(cos(course*deg2rad))

    #
    #...     now get speed
    #
    speed=distance/dt

    #
    #...      convert to u and v motion
    #

    spdmtn=speed*spdfac
    ispeed=int(spdmtn*100+0.5)/100
    angle=(90.0-course)*deg2rad
    
    umotion=spdmtn*cos(angle)
    vmotion=spdmtn*sin(angle)
    iumotion=int(umotion*100+0.5)/100
    ivmotion=int(vmotion*100+0.5)/100
    rumotion=float(iumotion)
    rvmotion=float(ivmotion)
    rcourse=float(course)
    rspeed=float(spdmtn)
    if(verb):
        print "%5.2f %4.0f %5.2f %5.2f %5.2f %5.2f\n"%\
              (distance,icourse,spdmtn,angle,umotion,vmotion)
        
##    return(icourse,ispeed,iumotion,ivmotion)
    return(rcourse,rspeed,umotion,vmotion)

#
#  service routines for findtc?
#

def GrepCdtgABdecks(tcs,cdtg,btps):

    paths=[]
    for btp in btps:
        tt=btp.split('.')
        ltt=len(tt)
        bdtg=tt[ltt-3]
        edtg=tt[ltt-2]
        edtgp12=mf.dtginc(edtg,12)
        if(cdtg >= bdtg and cdtg <= edtgp12):
            paths.append(btp)

    for path in paths:
        cmd="( grep %s %s | grep -s -v lonbnd )"%(cdtg,path)
        (dir,file)=os.path.split(path)
        tt=file.split('.')
        dyear=tt[2]
        dbid=tt[3]
        ttt=os.popen(cmd).readlines()
        for tt in ttt:
            tt="%s %s %s"%(dyear,dbid,tt)
            tcs.append(tt)

    return

def GrepCdtgMdecks(tcs,cdtg,btps):

    paths=[]
    for btp in btps:
        tt=btp.split('.')
        ltt=len(tt)
        bdtg=tt[ltt-3]
        edtg=tt[ltt-2]
        edtgp12=mf.dtginc(edtg,12)
        if(cdtg >= bdtg and cdtg <= edtgp12):
            paths.append(btp)

    for path in paths:
        cmd="( grep %s %s | grep -s -v lonbnd )"%(cdtg,path)
        (dir,file)=os.path.split(path)
        tt=file.split('.')
        dyear=tt[2]
        dbid=tt[3]
        ttt=os.popen(cmd).readlines()
        for tt in ttt:
            tcs.append(tt[:-1])

    return


def SC(str):
    ostr=str[0:-1]
    return(ostr)

def chkradii(crad):
    irad=-999
    if(crad == ''):
        irad=-999
    else:
        try:
            irad=int(crad)
        except:
            irad=-999
    if(irad < 0 or irad > 999):
        irad=-999
    elif(irad == 0):
        irad=0
    return(irad)




def ParseAdeckCard(addata,adstm,adcard,verb=0):

    tt=adcard.split()
    ntt=len(tt)

    if(verb):
        print '   ntt: ',ntt
        print 'adcard: ',adcard[:-1]
        for i in range(0,ntt):
            print 'adflds: ',i,tt[i]

    ctype=SC(tt[6])
    ctau=SC(tt[7])
    clat=SC(tt[8])
    clon=SC(tt[9])
    cvmax=SC(tt[10])
    if(ntt > 11):
        cpmin=SC(tt[11])
    else:
        cpmin=-999

    #
    # initialize rlat/rlon for case of all CARQ noloads
    #
    
    rlat=-99.9
    rlon=-999.9
    
    ctdo='___'
    ind='__'
    cdir='___'
    cspd='__'

    #
    # 25W.1986 has a blank JTWC 12 h lat/lon card, if '' then return
    #
    noload=0
    if(clat == '' and verb):
        print 'WWWWWWW noload making mdeck from adeck card: ',adcard[:-1]
        noload=1

    if(not(noload) and clat != ''):
        (rlat,rlon,ilat,ilon,hemns,hemew)=Clatlon2Rlatlon(clat,clon)

        
    if(verb):
        print 'CCCCCCCCCC ctype: ',ctype,ntt

       
    if(ctype == 'JTWC' or ctype == 'OFCL'):
        ctdo=SC(tt[ntt-3])
        wndir=SC(tt[ntt-2])
        wnspd=SC(tt[ntt-1])
        wnclat=SC(tt[8])
        wnclon=SC(tt[9])
        wnvmax=SC(tt[10])
        if(ntt > 11):
            wnpmin=SC(tt[11])
        else:
            wnpmin=-999
        if(not(ctdo.isalpha())): ctdo='___'
        if(not(noload)):
            (rlat,rlon,ilat,ilon,hemns,hemew)=Clatlon2Rlatlon(wnclat,wnclon)
        if(ctau == '0'):
            addata[adstm,'warn']=[rlat,rlon,wnvmax,ctdo,wndir,wnspd,wnpmin]

        if(verb): print 'www ',wnclat,wnclon,wnvmax,ctdo,wnpmin

    if(ctype == 'OFCL' or ctype == 'JTWC' or ctype == 'WRNG'):
        if(ntt == 27):
            ctdo=tt[ntt-1]
        else:
            ctdo=SC(tt[ntt-3])
        if(not(ctdo.isalpha()) or ctdo == ''): ctdo='___'
        addata[adstm,'tdo']=ctdo
        addata[adstm,'warnflg']=1


    #
    # go after radii
    #
    if((ctype == 'CNTR' or
       ctype == 'COMS' or
       ctype == 'CARQ' or
       ctype == 'JTWC' or ctype == 'OFCL') and
       (ntt > 18)
        
       ):

        rcode=SC(tt[14])

        if(atcf.IsWindRadii(rcode)):
            rwind=int(SC(tt[13]))

            if(rwind == 35 or rwind == 34): crcode='r34'
            if(rwind == 50): crcode='r50'
            if(rwind == 100): crcode='r100'
            if(rwind == 64 or rwind == 65): crcode='r64'

            if(verb):
                print 'GGGG----- ',adcard
                print 'GGGG----- ',rwind,rcode,crcode
            
            irne=chkradii(SC(tt[15]))
            irse=chkradii(SC(tt[16]))
            irsw=chkradii(SC(tt[17]))
            if(ctype == 'CNTR'):
                irnw=chkradii(tt[18])
            else:
                irnw=chkradii(SC(tt[18]))

            radii=[irne,irse,irsw,irnw]
            
            if(verb):
                print 'GGGGG----- ',radii

            if(
                (ctype == 'JTWC' and ctau == '12') or
                (ctype == 'OFCL' and ctau == '12') or
                (ctype == 'JTWC' and ctau == '-12') or
                (ctype == 'OFCL' and ctau == '-12') or
                (ctype == 'CARQ' and ctau == '-12')
                ):
                pass
            else:
                rquad=atcf.WindRadiiCode2Normal(rcode,radii)
                addata[adstm,ctype,crcode]=rquad

                if(verb):
                    print 'GGGGFFFFFF----- ',adstm,ctau,crcode,ctype,' AAA ',addata[adstm,ctype,crcode]
    #
    # misc -- roci/poci rmax, deye,depth
    #

    if(ctype == 'CARQ' or ctype == 'WRNG'):

        try:
            ind=SC(tt[12])
        except:
            ind='XX'

        if(ctau == '0'):

            cpoci=9999
            croci=999
            crmax=999
            cdeye=999
            cdepth='K'
            cdir=999
            cspd=99
            cqname='______'
            #
            # handle cases without depth code
            #
            if(ntt == 31 or ntt == 32 or ntt == 29):
                cpoci=int(SC(tt[19]))
                croci=int(SC(tt[20]))
                crmax=int(SC(tt[21]))
                if(SC(tt[22]) != ''):
                    cdeye=int(SC(tt[22]))
                else:
                    cdeye=-99
                cdir=int(SC(tt[27]))
                cspd=int(SC(tt[28]))

            if(ntt == 31):
                cqname=SC(tt[29])
                cdepth=SC(tt[30])

            if(ntt == 32):
                cqname=SC(tt[29])
                cdepth=SC(tt[31])


        if(ctau == '-12'):
            cqname='______'
            if(ntt == 29):
                cdir=int(SC(tt[27]))
                cspd=int(SC(tt[28]))
            else:
                cdir=999
                cspd=99

        #
        # dump tau 0 into carq and tau-12 int carq12....
        #
        
        if(ntt == 11):
            vmax=int(tt[10])
        else:
            vmax=int(cvmax)
            
        if(ctau == '0' and ctype == 'CARQ'):
            addata[adstm,'carq']=[rlat,rlon,vmax,ind,cdir,cspd,cpmin,cqname,
                                  cpoci,croci,crmax,cdeye,cdepth]

        if(ctau == '-12' and ctype == 'CARQ'):
            addata[adstm,'carq12']=[rlat,rlon,vmax,ind,cdir,cspd,cpmin,cqname]

        if(ctau == '0' and ctype == 'WRNG'):
            addata[adstm,'wrng']=[rlat,rlon,vmax,ind,cdir,cspd,cpmin,cqname,
                                  cpoci,croci,crmax,cdeye,cdepth]
        
        if(ctau == '-12' and ctype == 'WRNG'):
            addata[adstm,'wrng12']=[rlat,rlon,vmax,ind,cdir,cspd,cpmin,cqname]
            
        if(verb): print 'ccc ',ntt,ctype,clat,clon,cvmax,ind,cdir,cspd,cpmin,cqname

    return

def ParseTCcard(scard):

    #2007 04W 2007071306 04W 130  926  27.3 127.4  196  128  +6h   6.3 12.1  12h 360.0 12.0  23 ST r34: 235 220 135 195 r50: 165 165  80 100
    # 0   1        2      3   4    5    6     7     8    9   10     11  12    13  14    15   16 17
    tt=scard.split()
    ntt=len(tt)
    #
    # neumann bt include x/y motion and no TS counter so ntt = 12
    # real bt does not include x/y, but has TS counter so ntt = 11
    #
    i=4
    vmax=float(tt[i])  ; i=i+1
    pmin=float(tt[i])  ; i=i+1
    lat=float(tt[i])   ; i=i+1
    lon=float(tt[i])   ; i=i+1
    r34=float(tt[i])   ; i=i+1
    r50=float(tt[i])   ; i=i+2
    dir=float(tt[i])   ; i=i+1
    spd=float(tt[i])  ; i=i+2
    odir=float(tt[i]) ; i=i+1
    ospd=float(tt[i]) ; i=i+1
    nts=int(tt[i])    ; i=i+1
    tcind=tt[i]       ; i=i+2

    try:
        r34ne=int(tt[i])       ; i=i+1
        r34se=int(tt[i])       ; i=i+1
        r34sw=int(tt[i])      ; i=i+1
        r34nw=int(tt[i])      ; i=i+2

        r50ne=int(tt[i])      ; i=i+1
        r50se=int(tt[i])      ; i=i+1
        r50sw=int(tt[i])      ; i=i+1
        r50nw=int(tt[i])      ; i=i+1

    except:
        r34ne=r34se=r34sw=r34nw=0
        r50ne=r50se=r50sw=r50nw=0

    if(pmin == 0): pmin=-999
    r34quad=[r34ne,r34se,r34sw,r34nw]
    r50quad=[r50ne,r50se,r50sw,r50nw]
    
    return(vmax,pmin,lat,lon,r34,r50,dir,spd,odir,ospd,nts,tcind,r34quad,r50quad)





def ParseEbtTCcard(scard):

    #1988101812 11L 075  984  11.5 284.2   62   30  +6h 254.8  7.6  12h 260.3  8.9  30 TY r34:  75  50  50  75 r50:  40  20  20  40
    #r64:  20   0   0  20 CP/Roci: 1008.0 180.0  CRm:  15.0  CDi: -99.0
    

    #2007 04W 2007071306 04W 130  926  27.3 127.4  196  128  +6h   6.3 12.1  12h 360.0 12.0  23 ST r34: 235 220 135 195 r50: 165 165  80 100
    # 0   1        2      3   4    5    6     7     8    9   10     11  12    13  14    15   16 17
    tt=scard.split()
    ntt=len(tt)
    #
    # neumann bt include x/y motion and no TS counter so ntt = 12
    # real bt does not include x/y, but has TS counter so ntt = 11
    #
    i=4
    vmax=float(tt[i])  ; i=i+1
    pmin=float(tt[i])  ; i=i+1
    lat=float(tt[i])   ; i=i+1
    lon=float(tt[i])   ; i=i+1
    r34=float(tt[i])   ; i=i+1
    r50=float(tt[i])   ; i=i+2
    dir=float(tt[i])   ; i=i+1
    spd=float(tt[i])  ; i=i+2
    odir=float(tt[i]) ; i=i+1
    ospd=float(tt[i]) ; i=i+1
    nts=int(tt[i])    ; i=i+1
    tcind=tt[i]       ; i=i+2

    try:
        r34ne=int(tt[i])       ; i=i+1
        r34se=int(tt[i])       ; i=i+1
        r34sw=int(tt[i])      ; i=i+1
        r34nw=int(tt[i])      ; i=i+2

        r50ne=int(tt[i])      ; i=i+1
        r50se=int(tt[i])      ; i=i+1
        r50sw=int(tt[i])      ; i=i+1
        r50nw=int(tt[i])      ; i=i+2

        r64ne=int(tt[i])      ; i=i+1
        r64se=int(tt[i])      ; i=i+1
        r64sw=int(tt[i])      ; i=i+1
        r64nw=int(tt[i])      ; i=i+2

    except:
        r34ne=r34se=r34sw=r34nw=-999
        r50ne=r50se=r50sw=r50nw=-999
        r64ne=r64se=r64sw=r64nw=-999

    try:
        poci=float(tt[i])      ; i=i+1
        roci=float(tt[i])      ; i=i+2

        rmax=float(tt[i])      ; i=i+2
        deye=float(tt[i])      ; i=i+1

    except:
        poci=9999
        roci=9999
        rmax=999
        deye=999

    if(poci < 0.0): poci=-999.0
    if(roci < 0.0): poci=-999.0
        

    if(pmin == 0): pmin=-999
    r34quad=[r34ne,r34se,r34sw,r34nw]
    r50quad=[r50ne,r50se,r50sw,r50nw]
    r64quad=[r64ne,r64se,r64sw,r64nw]
    
    return(vmax,pmin,lat,lon,r34,r50,dir,spd,odir,ospd,nts,tcind,
           r34quad,r50quad,r64quad,
           poci,roci,rmax,deye)


def GrepTcABdecks(tcs,tstmid,btps,dtype='bdeck'):

    def loaddic(dic,key,card):
        try:
            dic[key].append(card)
        except:
            dic[key]=[]
            dic[key].append(card)

        return
    
    paths=[]
    for btp in btps:
        tt=btp.split('.')
        ltt=len(tt)
        stmid=tt[ltt-4]
        if(tstmid == stmid):
            paths.append(btp)


    for path in paths:

        (dir,file)=os.path.split(path)
        tt=file.split('.')

        if(dtype == 'ebdeck'):
            # ['ebt', 'local', 'nhc', 'atl', '2001', '12L', '2001100612', '2001100818', 'txt']
            dyear=tt[4]
            dbid=tt[5]

        else:
            dyear=tt[2]
            dbid=tt[3]

        if(dtype == 'bdeck' or dtype == 'ebdeck'):
            tstmidgrep=tstmid

            #
            # if invest 'I' storms might be 'A' or 'B' inside the bdeck
            #
            if( (tstmid[2] == 'I' or tstmid[2] == 'S')
                and (int(tstmid[0:2]) >= 90 )):
                tstmidgrep="\"%s\\?\""%(tstmid[0:2])
                
            cmd="( grep -h %s %s | grep -s -v lonbnd )"%(tstmidgrep,path)
            ttt=os.popen(cmd).readlines()
        else:
            ttt=open(path,'r').readlines()

        for tt in ttt:
            if(dtype == 'bdeck' or dtype == 'ebdeck'):
                dtg=tt.split()[0]
                tt="%s %s %s"%(dyear,dbid,tt)
                tcs[dtg]=tt
            else:

                tttt=tt.split()
                dtg=SC(tttt[2])
                asrc=SC(tttt[4])
                atau=SC(tttt[5])

                ltt=len(tttt)
                
                tt="%s %s %s"%(dyear,dbid,tt)
                try:
                    tcs[dtg,asrc].append(tt)
                except:
                    tcs[dtg,asrc]=[]
                    tcs[dtg,asrc].append(tt)


    return


def SelectBestWindRadii(ar34quad,ar50quad,artype,
                        br34quad,br50quad,bfrtype='BEST'):

    r34quad=r50quad=[-999,-999,-999,-999]
    r34=r50=-999
    frtype='none'

    if(ar34quad  == None and
       (
        br34quad[0] == 0 and
        br34quad[1] == 0 and
        br34quad[2] == 0 and
        br34quad[3] == 0
        )
       ):
        r34quad=[-999,-999,-999,-999]
        r34=-999
        
    elif(
        br34quad[0] > 0.0 or
        br34quad[1] > 0.0 or
        br34quad[2] > 0.0 or
        br34quad[3] > 0.0
        ):
        r34quad=br34quad
        r34=(br34quad[0]+br34quad[1]+br34quad[2]+br34quad[3])*0.25
        frtype=bfrtype
        
    elif(ar34quad != None):
        r34quad=ar34quad
        r34=(ar34quad[0]+ar34quad[1]+ar34quad[2]+ar34quad[3])*0.25
        frtype=artype

    if(r34 == 0): r34=-999

    if(
        r34quad[0] == 0 and
        r34quad[1] == 0 and
        r34quad[2] == 0 and
        r34quad[3] == 0
        ):
        r34quad=[-999,-999,-999,-999]
        r34=-999
        
    ###print 'SSSSSSSFFFFFFFFFFFFFFFFFFf ',r34quad,r34

    if(ar50quad  == None and
       (
        br50quad[0] == 0 and
        br50quad[1] == 0 and
        br50quad[2] == 0 and
        br50quad[3] == 0
        )
       ):
        r50quad=[-999,-999,-999,-999]
        r50=-999
        
    elif(
        br50quad[0] > 0.0 or
        br50quad[1] > 0.0 or
        br50quad[2] > 0.0 or
        br50quad[3] > 0.0
        ):
        r50quad=br50quad
        r50=(br50quad[0]+br50quad[1]+br50quad[2]+br50quad[3])*0.25
        
    elif(ar50quad != None):
        r50quad=ar50quad
        r50=(ar50quad[0]+ar50quad[1]+ar50quad[2]+ar50quad[3])*0.25
        
    if(r50 == 0): r50=-999

    if(
        r50quad[0] == 0 and
        r50quad[1] == 0 and
        r50quad[2] == 0 and
        r50quad[3] == 0
        ): r50quad=[-999,-999,-999,-999]
        

        
    ####print 'SSSSSSSFFFFFFFFFFFFFF5555555 ',r50quad,r50

    return(r34quad,r50quad,frtype,r34,r50)
    



def GetAdeckWindRadii(addata,dtg,verb=0):

    type='none'
    r34quad=None
    r50quad=None


    def chkrquad(quad,type):
        otype='none'
        good=1
        if(quad[0] == -999. and
           quad[1] == -999. and
           quad[2] == -999. and
           quad[3] == -999.
           ): good=0

        if(good):
            return(type)
        else:
            return(otype)
    
        

    #
    #333333333333333333333333333333333333333333
    #

    type='none'
    
    try:
        r34quad=addata[dtg,'CARQ','r34']
        type=chkrquad(r34quad,'carq')
    except:
        pass

        

    if(type == 'none'):
        try:
            r34quad=addata[dtg,'CNTR','r34']
            type=chkrquad(r34quad,'cntr')
        except:
            pass

    if(type == 'none'):
        try:
            r34quad=addata[dtg,'COMS','r34']
            type=chkrquad(r34quad,'coms')
        except:
            pass
        
    if(type == 'none'):
        try:
            r34quad=addata[dtg,'JTWC','r34']
            type=chkrquad(r34quad,'jtwc')
        except:
            pass

    if(type == 'none'):
        try:
            r34quad=addata[dtg,'OFCL','r34']
            type=chkrquad(r34quad,'ofcl')
        except:
            pass

    #
    # 55555555555555555555555555555555555555555555555
    #
    type50='none'
    
    try:
        r50quad=addata[dtg,'CARQ','r50']
        type50=chkrquad(r50qaud,'carq')
    except:
        pass

    if(type50 == 'none'):
        
        try:
            r50quad=addata[dtg,'CNTR','r50']
            type50=chkrquad(r50qaud,'cntr')
        except:
            pass

    if(type50 == 'none'):
        
        try:
            r50quad=addata[dtg,'COMS','r50']
            type50=chkrquad(r50qaud,'coms')
        except:
            pass

    if(type50 == 'none'):

        try:
            r50quad=addata[dtg,'JTWC','r50']
            type50=chkrquad(r50qaud,'jtwc')
        except:
            pass

    if(type50 == 'none'):

        try:
            r50quad=addata[dtg,'OFCL','r50']
            type50=chkrquad(r50qaud,'jtwc')
        except:
            pass

    if(verb):
        print
        print 'RRRRRRRRRR33333333 ',dtg,type,r34quad
        print 'RRRRRRRRRR55555555 ',dtg,type50,r50quad
        
    return(r34quad,r50quad,type)

#--------------------------------------------------------------------------
# 20070911 -- loadmdeck rips the adeck and bdeck and ebt (extended bt)  hashes to
# construct the final mdeck card with all storm data that will
# be used in tcanal, etc. including r34/r50 poci/roci rmax/deye/depth code
#
#--------------------------------------------------------------------------

def LoadMdeckCard(tstm,addata,adkey,abdcard,bdcard,ebdcard,dtg,lf,doLF=1):

    (ar34quad,ar50quad,artype)=GetAdeckWindRadii(addata,adkey)

    if(bdcard != ''):
        (vmax,pmin,lat,lon,r34,r50,dir,spd,odir,ospd,nts,tcind,br34quad,br50quad)=ParseTCcard(bdcard)
    else:

        try:
            cq=addata[adkey,'carq']
            carqthere=1
        except:
            carqthere=0
            pass

        if(carqthere):

            #
            # try both tau=0 and tau=12 for carq motion
            #
            try:
                cn0=addata[adkey,'carq']
                cn12=addata[adkey,'carq12']
                clat0=cn0[0]
                clon0=cn0[1]
                cvmax0=cn0[2]
                clat12=cn12[0]
                clon12=cn12[1]
                (carqcourse12,carqspeed12,cumotion,cvmotion)=rumhdsp(clat12,clon12,clat0,clon0,12.0)

            except:
                carqcourse12=999.0
                carqspeed12=99.0

            
            lat=float(cq[0])
            lon=float(cq[1])
            vmax=int(cq[2])
            dir=odir=float(cq[4])
            spd=ospd=float(cq[5])

            if(dir == 999.0 or carqcourse12 == 999.0):
                dir=odir=-99.9
            if(spd == 99.0 or carqspeed12 == 99.0):
                spd=ospd=-99.9

            if(carqcourse12 != 999.0):
                dir=odir=carqcourse12


            if(carqspeed12 != 99.0):
                spd=ospd=carqspeed12
                
            carqname=cq[7]
            if(len(str(cq[6])) == 0):
                pmin=-999
            else:
                pmin=float(cq[6])

            if(pmin == 0):
                pmin=-999

            #
            # use carq indicator
            #
            tcind=cq[3]
            if(tcind == ''):
                tcind='--'

            #
            # set number of TS posits to -1 as an not-real-bt indicator 
            #
            nts=-1
            r34=r50=-999.
            br34quad=br50quad=(-999.,-999.,-999.,-999.)

        else:

            #
            # if no bt and no carq return None so the dtg is skipped in findtc()
            #
            return(None)
        

    epoci=None

    if(len(ebdcard) > 0):

           (evmax,epmin,elat,elon,er34,er50,edir,espd,eodir,eospd,ents,etcind,
            ebr34quad,ebr50quad,ebr65quad,
            epoci,eroci,ermax,edeye)=ParseEbtTCcard(ebdcard)
        

    (fr34quad,fr50quad,frtype,fr34,fr50)=SelectBestWindRadii(ar34quad,ar50quad,artype,
                                                             br34quad,br50quad,bfrtype='BEST')
    if(len(ebdcard) > 0):
        (fr34quad,fr50quad,frtype,fr34,fr50)=SelectBestWindRadii(ar34quad,ar50quad,artype,
                                                                 ebr34quad,ebr50quad,bfrtype='EXBT')

    if(pmin > 0.0):
        gotpmin=1
        (fvmax,fpmin,flat,flon,fdir,fspd,fnts)=(vmax,pmin,lat,lon,odir,ospd,nts)
    else:
        (fvmax,fpmin,flat,flon,fdir,fspd,fnts)=(vmax,pmin,lat,lon,odir,ospd,nts)



    #
    # bt section
    #

    ucard="%s %s %03d %4d %5.1f %6.1f %4d %4d %5.1f %5.1f  %2d"%\
           (dtg,tstm,int(fvmax),int(fpmin),flat,flon,int(fr34),int(fr50),fdir,fspd,int(fnts))

    if(doLF):
        lfrac=w2.GetLandFrac(lf,flat,flon)
        lfucard="  LF: %4.2f"%(lfrac)
    else:
        lfucard="  LF: *.**"

    #
    # 20080108 -- test if operational TC 
    #
    tcstat='TC'
    if((IsTc(tcind) == 0) or fvmax < TCvmin): tcstat='NT'
    if((IsTc(tcind) == -1) and fvmax >= TCvmin ): tcstat='TC'

    flucard="  FL: %s %s"%(tcstat,tcind)

    #
    # try both tau=0 and tau=12 for carq motion
    #
    try:
        cn0=addata[adkey,'carq']
        cn12=addata[adkey,'carq12']
        clat0=cn0[0]
        clon0=cn0[1]
        cvmax0=cn0[2]
        clat12=cn12[0]
        clon12=cn12[1]
        (carqcourse12,carqspeed12,cumotion,cvmotion)=rumhdsp(clat12,clon12,clat0,clon0,12.0)

    except:
        carqcourse12=999.0
        carqspeed12=99.0



    try:
        cq=addata[adkey,'carq']
        carqthere=1
    except:
        carqthere=0
        pass
    
    if(carqthere):
        carqrlat=float(cq[0])
        carqrlon=float(cq[1])
        carqvmax=int(cq[2])
        carqcourse=float(cq[4])
        carqspeed=float(cq[5])
        carqname=cq[7]
        if(len(str(cq[6])) == 0):
            carqpmin=-999
        else:
            carqpmin=float(cq[6])
            
        if(len(carqname) == 0): carqname='_________'
        #
        # if motion on carq tau=0 undef, and -12 h carq posit available, use that motion
        #
        if(carqcourse > 360.0 and carqcourse12 <= 360.0):
            carqcourse=carqcourse12
            carqspeed=carqspeed12

        cqucard="  C: %5.1f %6.1f %4d %5.1f %4.1f %4.0f %-9s"%(carqrlat,carqrlon,carqvmax,carqcourse,carqspeed,carqpmin,carqname[0:9])
        flucard="%s CQ"%(flucard)
    else:
        carqpmin=-999
        carqname='_________'
        cqucard="  C: %5.1f %6.1f %4d %5.1f %4.1f %4.0f %-9s"%(-99.9,-999.9,-999,999.9,99.9,carqpmin,carqname)
        flucard="%s NC"%(flucard)

    
    try:
        wn=addata[adkey,'warn']
        wndir=int(wn[len(wn)-3])
        wnspd=int(wn[len(wn)-2])
        
        if(wndir == 0 and wnspd == 0):
            wndir=999.9
            wnspd=99.9
                  
        wnucardofcl="  W: %5.1f %6.1f %4d %5.1f %4.1f"%(wn[0],wn[1],int(wn[2]),wndir,wnspd)
        downofcl=1
    except:
        downofcl=0

    try:
        wn0=addata[adkey,'wrng']
        wn12=addata[adkey,'wrng12']
        wlat0=wn0[0]
        wlon0=wn0[1]
        wvmax0=wn0[2]
        wlat12=wn12[0]
        wlon12=wn12[1]
        (wcourse,wspeed,wumotion,wvmotion)=rumhdsp(wlat12,wlon12,wlat0,wlon0,12.0)
        wnucardwarn="  W: %5.1f %6.1f %4d %5.1f %4.1f"%(wlat0,wlon0,wvmax0,wcourse,wspeed)
        downwarn=1

    except:
        downwarn=0


    if(downofcl == 0 and downwarn == 0):
        wnucard="  W: %5.1f %6.1f %4d %5.1f %4.1f"%(-99.9,-999.9,-999,999.9,99.9)
       
    elif(downwarn):
        wnucard=wnucardwarn

    elif(downofcl):
        wnucard=wnucardofcl

    try:
        wn=addata[adkey,'warnflg']
        flucard="%s WN"%(flucard)

    except:
        flucard="%s NW"%(flucard)


    try:
        tdo=addata[adkey,'tdo']
        tdoucard="  TDO: %3s"%(tdo)
    except:
        tdoucard="  TDO: %3s"%('___')


    (r34ne,r34se,r34sw,r34nw)=fr34quad
    (r50ne,r50se,r50sw,r50nw)=fr50quad

    r34card=" r34: %4d %4d %4d %4d "%(r34ne,r34se,r34sw,r34nw)
    r50card="r50: %4d %4d %4d %4d "%(r50ne,r50se,r50sw,r50nw)

    rtypecard=" RadSrc: %s"%(frtype)

    #
    # misc carq -- poci,roci, rmax, deye
    #[26.3, 128.6, 20, 'DB', 35, 6, 'INVEST', 1008, 150, 45, 0, 'S']
    #   0    1      2    3    4  5     6       7    8    9   10  11

    try:
        cq=addata[adkey,'carq']
        cpoci=float(cq[8])
        croci=float(cq[9])
        crmax=float(cq[10])
        cdeye=float(cq[11])
        if(cdeye == 0.0): cdeye=-99.
        cdepth=cq[12]
        if(len(cdepth) == 0): cdepth='X'
        gotstruct=1

    except:
        cq='---------------------------------------'
        cpoci=9999.0
        croci=999.0
        crmax=999.0
        cdeye=999.0
        cdepth='K'
        gotstruct=0

    if( (gotstruct == 0 or
        (gotstruct and cpoci > 1050.0))
        and epoci != None):
        cpoci=epoci
        croci=eroci
        crmax=ermax
        cdeye=edeye
        cdepth='K'
        gotstruct=1

    #
    # final check
    #
    if(gotstruct):
        if(cpoci < 0.0):
            cpoci=9999.0
        if(croci < 0.0):
            croci=999.0
        if(crmax < 0.0):
            crmax=999.0
        if(cdeye < 0.0):
           cdeye=999.0
    

    cqxcard=" CP/Roci: %6.1f %5.1f  CRm: %5.1f  CDi: %5.1f  Cdpth: %s"%(cpoci,croci,crmax,cdeye,cdepth)

    ucard=ucard + flucard + lfucard + tdoucard + cqucard + wnucard + rtypecard + r34card + r50card + cqxcard

    return(ucard)

def findMdeckTC(tstm,do9x=1,verb=0):

    tt=tstm.split('.')

    if(len(tt) != 2):
        print 'EEE invalid tstm in findMdckTC: ',tstm
        sys.exit()

    tstmid=tt[0].upper()
    yyyy=tt[1]

    mddir="%s/%s"%(MdeckDir,yyyy)
    mdmask="%s/mdeck.*.%s.*.txt"%(mddir,tstmid)
    mdpaths=glob.glob(mdmask)

    omdcards={}

    if(len(mdpaths) >= 1):
        
        mdpath=mdpaths[-1]
        mdcards=open(mdpath).readlines()

        for mdcard in mdcards:
            dtg=mdcard.split()[0]
            omdcards[dtg]=mdcard


    return(omdcards)
    



#--------------------------------------------------------------------------
# 20070911 -- findtc greps adeck cards and creates addata{} where the key is the DTG
# and generates mdeck cards
#
#--------------------------------------------------------------------------

def findtc(tstm,dofilt9x=1,srcopt='bt',doLF=1,verb=0):

    #
    # setup land-sea fraction
    #
    tt=tstm.split('.')

    if(len(tt) != 2):
        print 'EEE invalid tstm in findtc: ',tstm
        sys.exit()

    tstmid=tt[0]
    yyyy=tt[1]
    #
    #  turn off 9x filter if stmid 9X
    #
    if(int(tstmid[0:2]) >= 90 and int(tstmid[0:2]) <= 99):
        dofilt9x=0
    
    if(doLF):
        lf=w2.SetLandFrac()

    if(srcopt == 'bt' or dofilt9x == 1):
        
        ddir=w2.TcBtDatDir
        btprefix='BT'
        addir=w2.TcAdecksFinalDir
        adprefix='AD'
        if(verb): print 'BBBBBBBB bt source is real (BT.)'

    if(srcopt == 'btops' or dofilt9x == 0):
        ddir=w2.TcBtDatDir
        btprefix='BtOps'
        addir=w2.TcAdecksFinalDir
        adprefix='AdOps'
        if(verb): print 'BBBBBBBB bt source is  OPS (BtOps.)'
        

    bdmkyyyy="%s/%s/%s.???.%s.%s.*"%(ddir,yyyy,btprefix,yyyy,tstmid)
    admkyyyy="%s/%s/%s.???.%s.%s.*"%(addir,yyyy,adprefix,yyyy,tstmid)

    bdp=glob.glob(bdmkyyyy)
    adp=glob.glob(admkyyyy)

    bdtcs={}
    adtcs={}
    addata={}
    mcards={}

    GrepTcABdecks(bdtcs,tstmid,bdp,'bdeck')
    GrepTcABdecks(adtcs,tstmid,adp,'adeck')

    adtgs=adtcs.keys()
    adtgs.sort()

    bdtgs=bdtcs.keys()
    bdtgs.sort()

    #
    # check if the local adeck is old..typically 9x
    #
    maxabdtgdiff=5.0
    try:
        lastadtg=adtgs[-1][0]
        lastbdtg=bdtgs[-1]
        abdtgdiff=mf.dtgdiff(lastadtg,lastbdtg)/24.0
    except:
        abdtgdiff=-99999

    if(len(adtgs) > 0 and abdtgdiff < maxabdtgdiff):
        for adtg in adtgs:
            bdtgs.append(adtg[0])

        bdtgs.sort()

    dtgs=mf.uniq(bdtgs)

    if(verb):
        print 'BBBB ',bdtgs
        print 'AAAA ',bdtgs


#
# extend best tracks
#

    eddir=eBdeckDir
    ebtprefix='ebt.local.nhc'
    emkyyyy="%s/%s/%s.???.%s.%s.*"%(eddir,yyyy,ebtprefix,yyyy,tstmid)
    ebdp=glob.glob(emkyyyy)
    ebdtcs={}

    if(len(ebdp) > 0):
        GrepTcABdecks(ebdtcs,tstmid,ebdp,'ebdeck')
        edtgs=ebdtcs.keys()
        edtgs.sort()


    for dtg in dtgs:

        try:
            bdcard=bdtcs[dtg]
        except:
            bdcard=''

        try:
            cntrcards=adtcs[dtg,'CNTR']
            for cntrcard in cntrcards:
                ParseAdeckCard(addata,dtg,cntrcard,verb=verb)
        except:
            cntrcards=None

        
        try:
            comscards=adtcs[dtg,'COMS']
            for comscard in comscards:
                ParseAdeckCard(addata,dtg,comscard,verb=verb)
        except:
            comsrcards=None


        try:
            carqcards=adtcs[dtg,'CARQ']
            for n in range(0,len(carqcards)):
                carqcard=carqcards[n]
                ParseAdeckCard(addata,dtg,carqcard,verb=verb)
        except:
            carqcards=None

        
        try:
            jtwccards=adtcs[dtg,'JTWC']
            for jtwccard in jtwccards:
                ParseAdeckCard(addata,dtg,jtwccard,verb=verb)
        except:
            jtwcrcards=None

        
        try:
            ofclcards=adtcs[dtg,'OFCL']
            for ofclcard in ofclcards:
                ParseAdeckCard(addata,dtg,ofclcard,verb=verb)
        except:
            ofclrcards=None


        try:
            wrngcards=adtcs[dtg,'WRNG']
            for wrngcard in wrngcards:
                ParseAdeckCard(addata,dtg,wrngcard,verb=verb)
        except:
            wrngrcards=None

        try:
            ebdcard=ebdtcs[dtg]
        except:
            ebdcard=''

        
        ucard=LoadMdeckCard(tstm,addata,dtg,bdcard,bdcard,ebdcard,dtg,lf)
        
        if(ucard != None):
            mcards[dtg]=ucard


    return(mcards)


def DupChkTcs(tcs,drmin=0.5,verb=0):

    nstm=len(tcs)

    stms=[]
    stmlats=[]
    stmlons=[]
    
    utcs=[]

    itcu={}

    for tc in tcs:
        tt=tc.split()
        rlat=float(tt[4])
        rlon=float(tt[5])
        stms.append(tt[1])
        stmlats.append(rlat)
        stmlons.append(rlon)

    #
    # calc distance between TCs and find uniq stms
    #


    for i in range(0,nstm):
        itcu[i]=1

    for i in range(0,nstm):
        ii=i+1
        istmu=1
        for ii in range(ii,nstm):
            dlat=stmlats[i]-stmlats[ii]
            dlon=stmlons[i]-stmlons[ii]
            dr=sqrt(dlat*dlat+dlon*dlon)

            if(dr <= drmin):
                #
                # if choosing between 9X and storm in warning us non-9X
                #
                if(int(stms[i][0:2]) < 90):
                    itcu[ii]=0
                else:
                    itcu[i]=0
            if(verb and (itcu[ii]==0 or itcu[i]) ):
                print 'qqq ii ',i,ii,dr,drmin,' dlat lon: ',dlat,dlon,stms[i],stms[ii]

    #
    # create new storm list
    #

    for i in range(0,nstm):
        if(itcu[i] == 1): utcs.append(tcs[i])

    return(utcs)


                    
#--------------------------------------------------------------------------
# 20070911 -- findtcs greps adeck cards and creates addata{} where the key is the STM
#
#
#--------------------------------------------------------------------------

def getmdecktcs(ddir,cdtg,dofilt9x=0,verb=0):
    
    bdmdeckpath="%s/btops.%s.txt"%(ddir,cdtg)
    try:
        tcs=open(bdmdeckpath).readlines()
    except:
        tcs=[]

    otcs=[]
    if(len(tcs) > 0):
        for tc in tcs:
            stm=tc.split()[1]
            stm3id=stm.split('.')[0]
            if(not(dofilt9x and int(stm3id[0:2]) >= 90)):
                otcs.append(tc)
                
    
    return(otcs)
        
def findtcsOLD(cdtg,dofilt9x=0,srcopt='mdeck',doLF=1,verb=0):

    def getstmid(dtg,stmnum,b2id):

        stmyear=dtg[0:4]

        if(b2id == 'SH'):
            stmyear=GetShemYear(dtg)

        if(b2id == 'SH' or b2id == 'IO'):
            (shemid,nioid)=TCNum2Stmid(stmyear)
            if(b2id == 'SH'):
                try:
                    b1id=shemid[stmnum]
                except:
                    b1id=stmnum+b1id
            if(b2id == 'IO'):
                try:
                    b1id=shemid[stmnum]
                except:
                    b1id=stmnum+b1id

        else:
            
            b1id=Basin2toBasin1[b2id]

        stmid=stmnum+b1id

        return(stmyear,stmid)
        



    #
    # setup land-sea fraction
    #

    if(doLF):
        lf=w2.SetLandFrac()

    drmin=0.5   # min distance (deg) to consider TC uniq in the bunch
        
    stms=[]
    stmcards={}
    ustmcards={}
    
    adstms=[]
    adstmcards={}
    adustmcards={}
    
    yyyy=cdtg[0:4]
    mm=cdtg[4:6]

    yyyym1=string.atoi(yyyy)-1
    yyyym1=str(yyyym1)
    yyyyp1=string.atoi(yyyy)+1
    yyyyp1=str(yyyyp1)

    (shemoverlap,shyyyy,shyyyyp1)=CurShemOverlap(cdtg)

    if(srcopt == 'bt'):
        ddir=w2.TcBtDatDir
        btprefix='BT'
        addir=w2.TcAdecksFinalDir
        adprefix='AD'
        if(verb): print 'BBBBBBBB bt source is real (BT.) ddir: ',ddir

    elif(srcopt == 'bt.ops'):
        ddir=w2.TcBtDatDir
        btprefix='BtOps'
        addir=w2.TcAdecksFinalDir
        adprefix='AdOps'
        if(verb): print 'BBBBBBBB bt source is  OPS (BtOps.)'
        
    elif(srcopt == 'mdeck'):
        yyyy=cdtg[0:4]
        ddir="%s/%s"%(w2.TcCarqDatDir,yyyy)
        (tcs)=getmdecktcs(ddir,cdtg)
        return(tcs)


    if(srcopt == 'bt' or srcopt == 'bt.ops'):
        
        tcs=[]
        adtcs=[]
        mdtcs=[]

        doprevyear=0
        if(mm == '01' or mm == '02'): doprevyear=1

        #
        #  look in past and future year for posits becaus of different treatment of shem by jtwc (060100-070100)
        #  and my version of neumann (010100 - 123118)
        #
        # 20040902 -H forces output of file, need for case with ONE file in the bt dir (beginning of shem season)
        #

        bdmkyyyy="%s/%s/%s.???.*"%(ddir,yyyy,btprefix)
        admkyyyy="%s/%s/%s.???.*"%(addir,yyyy,adprefix)

        bdmkyyyym1="%s/%s/%s.???.*"%(ddir,yyyym1,btprefix)
        bdmkyyyyp1="%s/%s/%s.???.*"%(ddir,yyyyp1,btprefix)

        admkyyyym1="%s/%s/%s.???.*"%(addir,yyyym1,adprefix)
        admkyyyyp1="%s/%s/%s.???.*"%(addir,yyyyp1,adprefix)

        mddir=MdeckDir
        mdprefix='MD'

        mdmkyyyy="%s/%s/%s.???.*"%(mddir,yyyy,mdprefix)
        mdmkyyyym1="%s/%s/%s.???.*"%(mddir,yyyym1,mdprefix)
        mdmkyyyyp1="%s/%s/%s.???.*"%(mddir,yyyyp1,mdprefix)

        
        btp=glob.glob(bdmkyyyy)
        adp=glob.glob(admkyyyy)

        btpm1=glob.glob(bdmkyyyym1)
        adpm1=glob.glob(admkyyyym1)

        btpp1=glob.glob(bdmkyyyyp1)
        adpp1=glob.glob(admkyyyyp1)

        mdp=glob.glob(mdmkyyyy)
        mdpm1=glob.glob(mdmkyyyym1)
        mdpp1=glob.glob(mdmkyyyyp1)

        if(verb): print 'PPPPPPPPPPP doprevyear: ',doprevyear,' shemoverlap ',shemoverlap

        if(doprevyear):

            GrepCdtgABdecks(tcs,cdtg,btpm1)

            if(shemoverlap):
                GrepCdtgABdecks(tcs,cdtg,btpp1)
            GrepCdtgABdecks(tcs,cdtg,btp)

            GrepCdtgABdecks(adtcs,cdtg,adpm1)
            if(shemoverlap):
                GrepCdtgABdecks(adtcs,cdtg,adpp1)
            GrepCdtgABdecks(adtcs,cdtg,adp)

        else:

            if(shemoverlap):
                GrepCdtgABdecks(tcs,cdtg,btpp1)
                GrepCdtgABdecks(adtcs,cdtg,adpp1)
                GrepCdtgABdecks(mdtcs,cdtg,mdpp1)

            GrepCdtgABdecks(tcs,cdtg,btp)
            GrepCdtgABdecks(adtcs,cdtg,adp)

            if(shemoverlap):
                GrepCdtgABdecks(mdtcs,cdtg,mdpp1)

            GrepCdtgABdecks(mdtcs,cdtg,mdp)

    
    if(verb):
        for tc in tcs:
            print 'tcccccccccccccccccccccccccccccc',tc[:-1]


    ntcs=len(tcs)
    adntcs=len(adtcs)

    ntcs=len(mdtcs)
    print 'nnnnnnnnnnnnn ',ntcs
    for mdtc in mdtcs:
        print mdtc

    if(ntcs != 0):

        ntcok=0
        for tc in tcs:
            tt=tc.split()

            btyear=tt[0]
            btid=tt[1]
            
            dtg=tt[2]
            stmid="%s.%s"%(btid,btyear)

            vmax=tt[4]
            pmin=tt[5]
            stmnum=int(stmid[0:2])

            doit=1
            if(dofilt9x and stmnum >= 50): doit=0

            if(doit):
                stms.append(stmid)
                try:
                    stmcards[stmid].append(tc)
                except:
                    stmcards[stmid]=[tc]
                    
                ntcok=ntcok+1

        if(ntcok == 0):
            tcs=[]
            return(tcs)
        
        stms=mf.uniq(stms)

        #aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
        # 
        # parse adeck for flags posits ...
        #
        #aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa

        addata={}

        if(adntcs != 0):

            for adtc in adtcs:

                tt=adtc.split()
                adyear=tt[0]
                adid=tt[1]
                stmid="%s.%s"%(adid,adyear)
                stmnum=int(adid[0:2])
                
                doit=1

                if(dofilt9x and stmnum >= 50): doit=0

                if(doit):
                    adstms.append(stmid)
                    try:
                        adstmcards[stmid].append(adtc)
                    except:
                        adstmcards[stmid]=[adtc]

                    ntcok=ntcok+1

            adstms=mf.uniq(adstms)
            adstms.reverse()
            adstms.sort()

            def SC(str):
                ostr=str[0:-1]
                return(ostr)


            for adstm in adstms:
                for adcard in adstmcards[adstm]:
                    ParseAdeckCard(addata,adstm,adcard,verb=verb)



        
        #
        # reverse so the non 9X storms are on the bottom
        #

        stms.reverse()
        stms.sort()

        for stm in stms:

            bdcard=stmcards[stm][0]
            ucard=LoadMdeckCard(stm,addata,stm,bdcard,bdcard,dtg,lf)
            ustmcards[stm]=ucard
            
        #
        # dup check
        #

        nstm=len(stms)

        stmlats=[]
        stmlons=[]
        istmsu={}

        stmsu=[]

        for stm in stms:
            tt=ustmcards[stm].split()
            rlat=float(tt[4])
            rlon=float(tt[5])
            stmlats.append(rlat)
            stmlons.append(rlon)

        #
        # calc distance between TCs and find uniq stms
        #


        for i in range(0,nstm):
            istmsu[i]=1
            
        for i in range(0,nstm):
            ii=i+1
            istmu=1
            for ii in range(ii,nstm):
                dlat=stmlats[i]-stmlats[ii]
                dlon=stmlons[i]-stmlons[ii]
                dr=sqrt(dlat*dlat+dlon*dlon)
                
                if(dr <= drmin):
                    #
                    # if choosing between 9X and storm in warning us non-9X
                    #
                    if(int(stms[i][0:2]) < 90):
                        istmsu[ii]=0
                    else:
                        istmsu[i]=0
                if(verb and (istmsu[ii]==0 or istmsu[i]) ):
                    print 'qqq ii ',i,ii,dr,drmin,' dlat lon: ',dlat,dlon,stms[i],stms[ii]
                
        #
        # create new storm list
        #
        
        for i in range(0,nstm):
            if(istmsu[i] == 1): stmsu.append(stms[i])

        #
        # use uniq'd storm list for make cards
        #

        tcs=[]
        for stm in stmsu:
            tcs.append(ustmcards[stm])

    
    return(tcs)



#--------------------------------------------------------------------------
# 20071128 -- findtcs greps mdeck cards -- the key is to get the mdecks right first
#
#
#--------------------------------------------------------------------------

def findtcs(cdtg,dofilt9x=0,srcopt='btops',doLF=1,verb=0):

    if(srcopt == 'btops'):
        yyyy=cdtg[0:4]
        ddir="%s/%s"%(w2.TcCarqDatDir,yyyy)
        tcs=getmdecktcs(ddir,cdtg,dofilt9x)
        return(tcs)


    #-----------------------------------------------------------------
    #
    # if srcopt != btops, then go for dtg in mdecks directly
    #
    #-----------------------------------------------------------------

    #
    # setup land-sea fraction
    #

    if(doLF):
        lf=w2.SetLandFrac()
        
    stms=[]
    stmcards={}

    yyyy=cdtg[0:4]
    mm=cdtg[4:6]

    yyyym1=string.atoi(yyyy)-1
    yyyym1=str(yyyym1)
    yyyyp1=string.atoi(yyyy)+1
    yyyyp1=str(yyyyp1)

    (shemoverlap,shyyyy,shyyyyp1)=CurShemOverlap(cdtg)
        
    tcs=[]
    mdtcs=[]

    doprevyear=0
    if(mm == '01' or mm == '02'): doprevyear=1

    mddir=MdeckDir
    mdprefix='MdOps'

    mdmkyyyy="%s/%s/%s.???.*"%(mddir,yyyy,mdprefix)
    mdmkyyyym1="%s/%s/%s.???.*"%(mddir,yyyym1,mdprefix)
    mdmkyyyyp1="%s/%s/%s.???.*"%(mddir,yyyyp1,mdprefix)

    mdp=glob.glob(mdmkyyyy)
    mdpm1=glob.glob(mdmkyyyym1)
    mdpp1=glob.glob(mdmkyyyyp1)

    if(verb): print 'PPPPPPPPPPP doprevyear: ',doprevyear,' shemoverlap ',shemoverlap

    if(doprevyear):

        GrepCdtgMdecks(mdtcs,cdtg,mdpm1)

        if(shemoverlap):
            GrepCdtgMdecks(mdtcs,cdtg,mdpp1)

        GrepCdtgMdecks(mdtcs,cdtg,mdp)

    else:

        if(shemoverlap):
            GrepCdtgMdecks(mdtcs,cdtg,mdpp1)

        GrepCdtgMdecks(mdtcs,cdtg,mdp)

    if(verb):
        for tc in mdtcs:
            print 'tcccccccccccccccccccccccccccccc',tc[:-1]

    ntcs=len(mdtcs)

    if(ntcs != 0):

        ntcok=0
        for tc in mdtcs:
            
            tt=tc.split()

            btyear=tt[0]
            btid=tt[1]
            
            dtg=tt[2]
            stmid="%s.%s"%(btid,btyear)

            vmax=tt[4]
            pmin=tt[5]
            stmnum=int(stmid[0:2])

            doit=1
            if(dofilt9x and stmnum >= 90): doit=0
            
            if(doit):
                stms.append(stmid)
                stmcards[stmid]=tc
                ntcok=ntcok+1

        if(ntcok == 0):
            tcs=[]
            return(tcs)
        
        stms=mf.uniq(stms)

        for stm in stms:
            tcs.append(stmcards[stm])


            

    return(tcs)





def tcsource(dtg):
    source='neumann'
    
    if(int(dtg) > 2001010100 ): source='ops'
    
    return(source)
    

def tcbasin(lat,lon):

    basin='00'

    if(lat > 0.0 and lon >= 40.0 and lon < 75.0 ):
        basin='NIA'
        
    if(lat > 0.0 and lon >= 75.0 and lon < 100.0 ):
        basin='NIB'


    if(lat > 0.0 and lon >= 100.0 and lon < 180.0):
        basin='WPC'

    # 20011029
    # Jim Gross says that for cliper purposes CPC=EPC
    #

    if( (lat > 0.0 and lat <= 90.0 ) and (lon >= 180.0 and lon < 258.0) ):
        basin='EPC'

    if( (lat > 0.0 and lat <= 17.0 ) and (lon >= 258.0 and lon < 270.0) ):
        basin='EPC'
    elif( (lat > 17.0) and (lon >= 258.0 and lon < 270.0) ):
        basin='ATL'
    
    if( (lat > 0 and lat <= 14.0 ) and (lon >= 270 and lon < 275) ):
        basin='EPC'
    elif( (lat > 14) and (lon >= 270 and lon < 275) ):
        basin='ATL'
        
    if( (lat > 0 and lat <= 9 ) and (lon >= 275 and lon < 285) ):
        basin='EPC'
    elif( (lat > 9) and (lon >= 275 and lon < 285) ):
        basin='ATL'


    if( lat > 0 and lon >= 285):
        basin='ATL'


    if( lat < 0 and lon >= 135):
        basin='SEP'

    if( lat < 0 and ( lon > 40 and lon < 135) ):
        basin='SIO'
        
    return(basin)

def tcbasinb1id(lat,lon,b3id):

    b1id='X'

    if(lat > 0.0 and lon >= 40.0 and lon < 75.0 ):
        b1id='A'
        
    if(lat > 0.0 and lon >= 75.0 and lon < 100.0 ):
        b1id='B'


    if(lat > 0.0 and lon >= 100.0 and lon < 180.0):
        b1id='W'

    # 20011029
    # Jim Gross says that for cliper purposes CPC=EPC
    #

    if( (lat > 0.0 and lat <= 90.0 ) and (lon >= 180.0 and lon < 258.0) ):
        b1id='E'

    if( (lat > 0.0 and lat <= 17.0 ) and (lon >= 258.0 and lon < 270.0) ):
        b1id='E'
        
    elif( (lat > 17.0) and (lon >= 258.0 and lon < 270.0) ):
        b1id='L'
    
    if( (lat > 0 and lat <= 14.0 ) and (lon >= 270 and lon < 275) ):
        b1id='E'
    elif( (lat > 14) and (lon >= 270 and lon < 275) ):
        b1id='L'
        
    if( (lat > 0 and lat <= 9 ) and (lon >= 275 and lon < 285) ):
        b1id='E'
    elif( (lat > 9) and (lon >= 275 and lon < 285) ):
        b1id='L'


    if( lat > 0 and lon >= 285):
        b1id='L'


    if( lat < 0 and lon >= 135):
        b1id='P'

    if( lat < 0 and ( lon > 30 and lon < 135) ):
        b1id='S'

    #
    # sanity check
    #
    if(b3id == 'nio' and b1id != 'A' and b1id != 'B'):
        if(b1id == 'W'): b1id='B'
        
    return(b1id)

    
def cliperinput(dtg,source='neumann'):

    verb=0
    
    tcs=findtcs(dtg)
    if(verb): print tcs

    f=string.atof
    
    o=open('/tmp/clip.input.txt','w')

    for tc in tcs:
        if(verb): print tc
        tt=string.split(tc)
        sname=tt[1]
        vmax=f(tt[2])
        lat0=f(tt[4])
        lon0=f(tt[5])
        dir=f(tt[8])
        spd=f(tt[9])

        (latm12,lonm12)=rumltlg(dir,spd,-12,lat0,lon0)
        (latm24,lonm24)=rumltlg(dir,spd,-24,lat0,lon0)

        basin=tcbasin(lat0,lon0)
        if(verb): print "ssss ",sname,vmax,lat0,lon0,dir,spd
        if(verb): print "mmmm ",latm12,lonm12,latm24,lonm24
        part1="%10s %3s %3s  vmax: %03d "%(dtg,sname,basin,vmax)
        part2="motion: %6.2f %5.2f  tau0: %5.1f %6.1f "%(dir,spd,lat0,lon0)
        part3="taum12: %5.1f %6.1f  taum24: %5.1f %6.1f"%(latm12,lonm12,latm24,lonm24)
        clipcard=part1+part2+part3+'\n'

        print part1,part2,part3

        o.writelines(clipcard)
        
    o.close()
        

##         i=0
##         for ttt in tt:
##             print "i,ttt ",i,ttt
##             i=i+1
##         ttt=string.split(tt[0],':')
##         btpath=ttt[0]
##         print "btpath ",btpath
##         fbt=open(btpath)
##         bt=fbt.readlines()
##         for b in bt:
##             print b

#-13.8 192.3  -99  -99 230.0 06.29     
#-14.2 191.8 


def StormReport(basins,basinstorms,storms,storm,metadata):

    verb=0
    
    (veriname,verirule,dohomo,hm1,hm2,OPATH,RPATH,PPATH)=metadata

    ocards=[]
    rcards=[]
    
    for bb in BasinsAll:
        
        for b in basins:
            
            if(bb == b):
                
                if(StdOutReport): print "basins: %s"%(b)
                rcards.append("basins: %s"%(b))

                ss=basinstorms[b]
                ss=mf.uniq(ss)

                for s in ss:
                    ss1=storm[s]
                    sdtgs=[]
                    svmax=0.0
                    svmean=0.0
                    nvmean=0
                    for s1 in ss1:
                        if(s1[1] != 999.0):
                            vmax=float(s1[1])
                            svmean=svmean+vmax
                            nvmean=nvmean+1
                            if(vmax >= svmax): svmax=vmax
                        sdtgs.append(s1[0])

                    if(nvmean != 0):
                        svmean=svmean/float(nvmean)
                    else:
                        svmean=999
                        svmax=999

                    bdtg=sdtgs[0]
                    edtg=sdtgs[-1]
                    nday=mf.dtgdiff(bdtg,edtg)/24.0

                    sdtgs.sort()

                    sname=GetTCName(s)

                    rcard="%s %12s :: %5.1f : %s :: %s :: %5.1f : %5.1f"%(s,sname,nday,bdtg,edtg,svmax,svmean)
                    if(StdOutReport): print rcard
                    rcards.append(rcard)

    if(PrintReport):
        for rcard in rcards:
            if(verb): print 'RRRBBB: ',rcard
            RPATH.writelines(rcard+'\n')

    return


def VeriRuleCheck(verirule):
    ok=0
    for v in VeriRules:
        if(verirule == v): ok=1

    return(ok)
    

def VeriRule2Rtitle(verirule):
    if(verirule == 'jtwc'):
        rtitle='JTWC      (CARQ filt) rules'
    elif(verirule == 'jtwc.pure'):
        rtitle='JTWC.pure ( FE0 filt) rules'
    elif(verirule == 'jtwc.mod'):
        rtitle='JTWC.mod  ( TD  filt) rules'
    elif(verirule == 'nhc.pure'):
        rtitle='NHC.pure  (35kt filt) rules'
    elif(verirule == 'nhc.wind'):
        rtitle='NHC.wind  ( TS  filt) rules'
    elif(verirule == 'td30'):
        rtitle='TD only rules'
    return(rtitle)


def StormStatReport(stms,models,taus,stmstats,metadata):

    (veriname,verirule,dohomo,hm1,hm2,OPATH,RPATH,PPATH)=metadata

    verb=0

    global pystatvars

    tcfcname='tcfc'
    try:
        pystatvars.append(tcfcname)
    except:
        pystatvars=[]
        pystatvars.append(tcfcname)


    rcards=[]
    pcards=[]

    dopyvar=1

    if(dopyvar):  pcards.append('%s={\n'%(tcfcname))
    
    #
    # report by basin; brute force
    #
    
    for b in BasinsAll:
        
        for stm in stms:

            sbasin=stm[2:3]

            if(sbasin == b):

                sname=GetTCName(stm)
                
                rtitle=VeriRule2Rtitle(verirule)

                btitle="%s %-12s (%s) veriname: \'%s\'"%(stm,sname,rtitle,veriname)
                bbbb='='*len(btitle)

                if(StdOutReport): print
                rcards.append(' ')
                
                if(StdOutReport): print btitle
                rcards.append(btitle)
                
                if(StdOutReport): print bbbb
                rcards.append(bbbb)
                
                if(StdOutReport): print
                rcards.append(' ')
                
                if(dohomo):
                    htitle="**** NB: HOMOGENEOUS between: %s & %s ****"%(hm1,hm2)
                    hhhh='*'*len(htitle)
                    if(StdOutReport): print htitle
                    rcards.append(htitle)
                    if(StdOutReport): print hhhh
                    rcards.append(hhhh)
                    if(StdOutReport): print
                    rcards.append(' ')
                    
                rcard="mod tau     Nbt  Nfc    POD       %%imp   FE(%s)  CTE(%s)  ATE(%s)"%(cunito,cunito,cunito)
                rcard=rcard+"     Nfv   FV(kt)  BV(kt)   FVe(kt) FVeu(kt)"

                if(StdOutReport): print rcard
                rcards.append(rcard)

                rcard='--- ---    ---- ----    ---       ----    -----  -------  -------'
                rcard=rcard+'    ----    -----   -----   ------- --------'

                if(StdOutReport): print rcard
                rcards.append(rcard)

                pycard="\n('%s','%s'): \n{\n"%(stm.split('.')[1],stm.split('.')[0])
                
                for tau in taus:

                    itau=int(tau)

                    for model in models:

                        try:
                            cc=stmstats[stm,'clp',tau]
                            ccc=cc[0]
                            (clpntcb,clpntcf,clpntcfv,clppod,clpmeanfe,clpmeanfv,clpmeanbv,clpmeancte,clpmeanate)=\
                            (ccc[0],ccc[1],ccc[2],ccc[3],ccc[4],ccc[5],ccc[6],ccc[7],ccc[8])
                        except:
                            clpmeanfe=-999.0

                        tt=stmstats[stm,model,tau]
                        ttt=tt[0]
                        
                        (bntcb,bntcf,bntcfv,bpod,bmeanfe,bmeanfv,bmeanbv,bmeancte,bmeanate,bmeanfve,bmeanfveu)=\
                        (ttt[0],ttt[1],ttt[2],ttt[3],ttt[4],ttt[5],ttt[6],ttt[7],ttt[8],ttt[9],ttt[10])

                        if(clpmeanfe > 0.0 and itau>0 ):
                            clpimprov=((clpmeanfe-bmeanfe)/clpmeanfe)*100.0
                        else:
                            clpimprov=0.0

                        rformat="%s %s :: %4d %4d :: %3.0f :: %7.1f  %7.1f  %7.1f  %7.1f :: %4d :: %5.1f   %5.1f ::  %5.1f    %5.1f"
                        rcard=(rformat)%\
                               (model,tau,bntcb,bntcf,bpod,clpimprov,bmeanfe,bmeancte,bmeanate,bntcf,
                                bmeanfv,bmeanbv,bmeanfve,bmeanfveu)
                        if(StdOutReport): print rcard
                        rcards.append(rcard)

                        if(itau == 0):
                            
                            pyhash="'%s.%03d': (%4d, %4d, %3.0f, %7.1f, %4d, %7.1f, %7.1f, %5.1f, %5.1f),\n"%\
                                    (model,itau,bntcb,bntcf,bpod,bmeanfe,bntcfv,
                                     bmeanfv,bmeanbv,bmeanfve,bmeanfveu)
                            pycard="%s %s"%(pycard,pyhash)


                        elif(itau == 48 or itau == 72):
                            pyhash="'%s.%03d': (%4d, %4d, %3.0f, %4.0f, %7.1f, %7.1f, %7.1f, %4d, %7.1f, %7.1f, %5.1f, %5.1f),\n"%\
                                    (model,itau,bntcb,bntcf,bpod,clpimprov,bmeanfe,bmeancte,bmeanate,bntcfv,
                                     bmeanfv,bmeanbv,bmeanfve,bmeanfveu)
                            pycard="%s %s"%(pycard,pyhash)

                        
                    if(StdOutReport): print
                    rcards.append(' ')

                pycard=pycard+'},'
                pcards.append(pycard)
                #print 'TTTTTTTTTTTTTTTTTTTTTTT ',pycard

    if(PrintReport):
        for rcard in rcards:
            if(verb): print 'RRRBBB: ',rcard
            RPATH.writelines(rcard+'\n')


    if(dopyvar): pcards.append('\n}\n')
    for pcard in pcards:
        if(verb): print 'RRRPPP: ',pcard
        PPATH.writelines(pcard+'\n')
        
    return


def StatReportKey(models,taus,verb=1):

    kcards=[]
    kcards.append('Key:')
    kcards.append(' ')
    kcards.append('mod       - model')
    kcards.append('tau       - forecast hour')
    kcards.append('Nbt       - # verifying BT (best track) posits')
    kcards.append('Nfc       - # forecast posits')
    kcards.append('POD       - Probability of Detection (Nfc/Nbt)')
    kcards.append('%imp      - % improvement over CLIPER')
    kcards.append('FE        - Forecast Error')
    kcards.append('CTE       - Cross Track Error (path)')
    kcards.append('ATE       - Along Track Error (speed)')
    kcards.append('ATE       - Along Track Error (speed)')
    kcards.append('Nfv       - # forecast posits with max wind')
    kcards.append('FV        - Mean forecast max wind')
    kcards.append('BV        - Mean BT max wind')
    kcards.append('FVe       - Mean abs intensity forecast error max (kt)')
    kcards.append('BVeu      - Intensity forecast error bias (mean error)')
    kcards.append(' ')
    kcards.append('Models:')
    kcards.append(' ')

    for model in models:

        try:
            desc=ModelNametoModelDesc[model]
        except:
            desc="unknown"

        kcards.append("%s       - %s"%(model,desc))


    if(verb):

        for kcard in kcards:
            print kcard
            
    return(kcards)
        

def BasinStatReport(basins,models,taus,basinstats,metadata):

    verb=0

    global pystatvars
    tcfcname='tcfcbasin'
    try:
        pystatvars.append(tcfcname)
    except:
        pystatvars=[]
        pystatvars.append(tcfcname)
            

    (veriname,verirule,dohomo,hm1,hm2,OPATH,RPATH,PPATH)=metadata

    ocards=[]
    rcards=[]
    pcards=[]

    dopyvar=1
    if(dopyvar): pcards.append('%s={\n'%(tcfcname))

    for basin in basins:

        rtitle=VeriRule2Rtitle(verirule)

        btitle="%s (%s) veriname: \'%s\'"%(Basin1toBasinName[basin],rtitle,veriname)
        bbbb='='*len(btitle)
        
        if(StdOutReport): print
        rcards.append(' ')
        
        if(StdOutReport): print btitle
        rcards.append(btitle)
        
        if(StdOutReport): print bbbb
        rcards.append(bbbb)

        if(dohomo):
            htitle="**** NB: HOMOGENEOUS between: %s & %s ****"%(hm1,hm2)
            hhhh='*'*len(htitle)

            if(StdOutReport): print htitle
            rcards.append(htitle)

            if(StdOutReport): print hhhh
            rcards.append(hhhh)

        
        if(StdOutReport): print
        rcards.append(' ')

        rcard="mod tau     Nbt  Nfc    POD       %%imp   FE(%s)  CTE(%s)  ATE(%s)"%(cunito,cunito,cunito)
        rcard=rcard+"     Nfv   FV(kt)  BV(kt)   FVe(kt) FVeu(kt)"

        if(StdOutReport): print rcard
        rcards.append(rcard)

        rcard='--- ---    ---- ----    ---       ----    -----  -------  -------'
        rcard=rcard+'    ----    -----   -----   ------- --------'

        if(StdOutReport): print rcard
        rcards.append(rcard)

        pycard="\n('%s'): \n{\n"%(basin)

        ocardhead='%s, %8s,  basin, %2s, '%(veriname,verirule,basin)

        for tau in taus:

            itau=int(tau)

            for model in models:

                try:
                    cc=basinstats[basin,'clp',tau]
                    ccc=cc[0]
                    (clpntcb,clpntcf,clpntcfv,clppod,clpmeanfe,clpmeanfv,clpmeanbv,clpmeancte,clpmeanate)=\
                    (ccc[0],ccc[1],ccc[2],ccc[3],ccc[4],ccc[5],ccc[6],ccc[7],ccc[8])
                except:
                    clpmeanfe=-999.0
                    
                tt=basinstats[basin,model,tau]
                ttt=tt[0]

                (bntcb,bntcf,bntcfv,bpod,bmeanfe,bmeanfv,bmeanbv,bmeancte,bmeanate,bmeanfve,bmeanfveu)=\
                (ttt[0],ttt[1],ttt[2],ttt[3],ttt[4],ttt[5],ttt[6],ttt[7],ttt[8],ttt[9],ttt[10])

                if(clpmeanfe > 0.0 and itau>0 ):
                    clpimprov=((clpmeanfe-bmeanfe)/clpmeanfe)*100.0

                else:
                    clpimprov=0.0

                rformat="%s %s :: %4d %4d :: %3.0f :: %7.1f  %7.1f  %7.1f  %7.1f :: %4d :: %5.1f   %5.1f ::  %5.1f    %5.1f"
                rcard=(rformat)%\
                       (model,tau,bntcb,bntcf,bpod,clpimprov,bmeanfe,bmeancte,bmeanate,bntcf,
                        bmeanfv,bmeanbv,bmeanfve,bmeanfveu)
                if(StdOutReport): print rcard
                rcards.append(rcard)

                if(itau >= 0 and itau <= 120):
                    ocard=ocardhead+"%s, %03d, %4d, %4d, %3.0f, %5.1f, %5.1f, %5.1f, %5.0f, %6.1f, %6.1f, %5.1f, %5.1f,"%\
                           (model,itau,bntcb,bntcf,bpod,bmeanfe,bmeanfv,bmeanbv,clpimprov
                            ,bmeancte,bmeanate,bmeanfve,bmeanfveu)
                    ocards.append(ocard)
                    
                if(itau == 0):
                    pyhash="'%s.%03d': (%4d, %4d, %3.0f, %7.1f, %4d, %7.1f, %7.1f, %5.1f, %5.1f),\n"%\
                            (model,itau,bntcb,bntcf,bpod,bmeanfe,bntcfv,
                             bmeanfv,bmeanbv,bmeanfve,bmeanfveu)
                    pycard="%s %s"%(pycard,pyhash)
                        
                else:
                    pyhash="'%s.%03d': (%4d, %4d, %3.0f, %4.0f, %7.1f, %7.1f, %7.1f, %4d, %7.1f, %7.1f, %5.1f, %5.1f),\n"%\
                            (model,itau,bntcb,bntcf,bpod,clpimprov,bmeanfe,bmeancte,bmeanate,bntcfv,
                             bmeanfv,bmeanbv,bmeanfve,bmeanfveu)
                    pycard="%s %s"%(pycard,pyhash)
                
            if(StdOutReport): print
            rcards.append(' ')
            
        pycard=pycard+'},'
        pcards.append(pycard)

    for ocard in ocards:
        if(verb): print 'OOOBBB: ',ocard
        OPATH.writelines(ocard+'\n')

    if(PrintReport):
        for rcard in rcards:
            if(verb): print 'RRRBBB: ',rcard
            RPATH.writelines(rcard+'\n')


    if(dopyvar): pcards.append('\n}\n')
    for pcard in pcards:
        if(verb): print 'RRRPPP: ',pcard
        PPATH.writelines(pcard+'\n')

    return

def HemiStatReport(basins,models,taus,basinstats,hemi,metadata):
    
    verb=0
    global pystatvars

    (veriname,verirule,dohomo,hm1,hm2,OPATH,RPATH,PPATH)=metadata

    rtitle=VeriRule2Rtitle(verirule)

    htitle="%s (%s) :: verifile: \'%s\'"%(Hemi1toHemiName[hemi],rtitle,veriname)
    hhhh='='*len(htitle)

    rcards=[]
    pcards=[]

    tcfcname='tcfc%s'%(hemi)
    try:
        pystatvars.append(tcfcname)
    except:
        pystatvars=[]
        pystatvars.append(tcfcname)
            
    pycard=('%s={\n'%(tcfcname))

    if(StdOutReport): print
    rcards.append(' ')
    
    if(StdOutReport): print htitle
    rcards.append(htitle)
    
    if(StdOutReport): print hhhh
    rcards.append(hhhh)
    
    if(dohomo):
        htitle="**** NB: HOMOGENEOUS between: %s & %s ****"%(hm1,hm2)
        hhhh='*'*len(htitle)
        if(StdOutReport): print htitle
        rcards.append(htitle)
        if(StdOutReport): print hhhh
        rcards.append(hhhh)
        
    if(StdOutReport): print
    rcards.append(' ')

    rcard="mod tau     Nbt  Nfc    POD       %%imp   FE(%s)  CTE(%s)  ATE(%s)"%(cunito,cunito,cunito)
    rcard=rcard+"     Nfv   FV(kt)  BV(kt)   FVe(kt) FVeu(kt)"

    if(StdOutReport): print rcard
    rcards.append(rcard)

    rcard='--- ---    ---- ----    ---       ----    -----  -------  -------'
    rcard=rcard+'    ----    -----   -----   ------- --------'

    if(StdOutReport): print rcard
    rcards.append(rcard)
    
    ocards=[]
    
    ocardhead='%s, %8s,   hemi, %2s, '%(veriname,verirule,hemi)
    

    for tau in taus:
        
        itau=int(tau)
        for model in models:
            
            (hntcb,hntcf,hntcfv,hpod,hmeanfe,hmeanfv,hmeanbv,
             hmeancte,hmeanate,hmeanfve,hmeanfveu)=\
            (0,0,0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0)
            
            hclpmeanfe=0.0
            hclpntcf=0
            hclpntcfv=0
            
            for basin in Hemi3toBasins[hemi]:

                try:
                    cc=basinstats[basin,'clp',tau]
                    ccc=cc[0]
                    (clpntcb,clpntcf,clpntcfv,clppod,clpmeanfe,clpmeanfv,clpmeanbv,clpmeancte,clpmeanate)=\
                    (ccc[0],ccc[1],ccc[2],ccc[3],ccc[4],ccc[5],ccc[6],ccc[7],ccc[8])
                    hclpmeanfe=hclpmeanfe+clpmeanfe*clpntcf
                    hclpntcf=hclpntcf+clpntcf
                    hclpntcfv=hclpntcfv+clpntcfv
                except:
                    clpmeanfe=-999.0
                    

                try:
                    
                    tt=basinstats[basin,model,tau]
                    ttt=tt[0]
                    
                    (bntcb,bntcf,bntcfv,bpod,bmeanfe,bmeanfv,bmeanbv,bmeancte,bmeanate,bmeanfve,bmeanfveu)=\
                    (ttt[0],ttt[1],ttt[2],ttt[3],ttt[4],ttt[5],ttt[6],ttt[7],ttt[8],ttt[9],ttt[10])

                    hntcb=hntcb+bntcb
                    hntcf=hntcf+bntcf
                    hntcfv=hntcfv+bntcfv
                    hpod=hpod+bpod*bntcf

                    hmeanfe=hmeanfe+bmeanfe*bntcf
                    hmeanfv=hmeanfv+bmeanfv*bntcfv
                    hmeanbv=hmeanbv+bmeanbv*bntcf
                    hmeancte=hmeancte+bmeancte*bntcf
                    hmeanate=hmeanate+bmeanate*bntcf
                    hmeanfve=hmeanfve+bmeanfve*bntcfv
                    hmeanfveu=hmeanfveu+bmeanfveu*bntcfv

                    hemithere=1
                    
                except:

                    hemithere=0

                    
            if(hclpntcf > 0):
                 
                hclpmeanfe=hclpmeanfe/hclpntcf

            if(hntcf > 0):
                
                hpod=hpod/hntcf
                hmeanfe=hmeanfe/hntcf
                hmeanbv=hmeanbv/hntcf
                hmeancte=hmeancte/hntcf
                hmeanate=hmeanate/hntcf

            if(hntcfv > 0):
                hmeanfv=hmeanfv/hntcfv
                hmeanfve=hmeanfve/hntcfv
                hmeanfveu=hmeanfveu/hntcfv


            if(itau>0 and hclpntcf > 0):
                hclpimprov=((hclpmeanfe-hmeanfe)/hclpmeanfe)*100.0
            else:
                hclpimprov=0.0

            rformat="%s %s :: %4d %4d :: %3.0f :: %7.1f  %7.1f  %7.1f  %7.1f :: %4d :: %5.1f   %5.1f ::  %5.1f    %5.1f"
            rcard=(rformat)%\
                   (model,tau,hntcb,hntcf,hpod,hclpimprov,hmeanfe,hmeancte,hmeanate,hntcf,
                    hmeanfv,hmeanbv,hmeanfve,hmeanfveu)

            if(StdOutReport): print rcard
            rcards.append(rcard)

            if(itau >= 0 and itau <= 120):
                oformat="%s, %03d, %4d, %4d, %3.0f, %5.1f, %6.1f, %6.1f, %5.0f, %6.1f, %6.1f, %5.1f, %5.1f,"
                ocard=ocardhead+oformat%\
                       (model,itau,hntcb,hntcf,hpod,hmeanfe,hmeanfv,hmeanbv,hclpimprov,
                        hmeancte,hmeanate,hmeanfve,hmeanfveu)
                ocards.append(ocard)


            if(itau == 0):
                pformat="'%s.%03d': (%4d, %4d, %3.0f, %7.1f, %4d, %7.1f, %7.1f, %5.1f, %5.1f),\n"
                pyhash=pformat%\
                        (model,itau,hntcb,hntcf,hpod,hmeanfe,hntcfv,
                         hmeanfv,hmeanbv,hmeanfve,hmeanfveu)
                pycard="%s %s"%(pycard,pyhash)
            else:
                pformat="'%s.%03d': (%4d, %4d, %3.0f, %4.0f, %7.1f, %7.1f, %7.1f, %4d, %7.1f, %7.1f, %5.1f, %5.1f),\n"
                pyhash=pformat%\
                        (model,itau,hntcb,hntcf,hpod,hclpimprov,hmeanfe,hmeancte,hmeanate,hntcfv,
                         hmeanfv,hmeanbv,hmeanfve,hmeanfveu)
                pycard="%s %s"%(pycard,pyhash)
                
        if(StdOutReport): print
        rcards.append(' ')

                
    pcards.append(pycard)

    for ocard in ocards:
        if(verb): print 'OOOHHH: ',ocard
        OPATH.writelines(ocard+'\n')


    if(PrintReport):
        for rcard in rcards:
            if(verb): print 'RRRBBB: ',rcard
            RPATH.writelines(rcard+'\n')

    pcards.append('}\n')
    for pcard in pcards:
        if(verb): print 'RRRPPP: ',pcard
        PPATH.writelines(pcard+'\n')

    return

def ftcards(stmid,vpath,ftopath):

    verb=0
    grepcmd="grep -h \'%s \' %s"%(stmid,vpath)
    fts=os.popen(grepcmd).readlines()

    FO=open(ftopath,'w')

    models=[]
    bdtgs=[]

    tcft={}

    for ft in fts:

        #e40 048 07L 1989090912 1989091112 FP: 40.4 297.6 BP: 39.4 298.0 FE: 62.8 BW: 40.0 FS: 22.3 159.2 2.8 -888.8 9.2 17.9 \
        #CT: CC CT_AT(nm): 30.4 54.9

        tt=ft.split()
        
        model=tt[0]
        tau=tt[1]
        bdtg=tt[3]
        lat=tt[6]
        lon=tt[7]
        btvmax=tt[14]

        if(verb): print model,tau,bdtg,lat,lon,btvmax

        models.append(model)
        bdtgs.append(bdtg)

        if(float(lat) > -80.0):

            try:
                if(tau == '000'):
                    tcft[model,bdtg]="%s %s %s %s"%(tau,lat,lon,btvmax)
                else:
                    tcft[model,bdtg]="%s : %s %s %s %s"%(tcft[model,bdtg],tau,lat,lon,btvmax)
                iok=1
            except:
                iok=2
                tcft[model,bdtg]=''

            if(iok == 2):
                if(tau == '000'):
                    tcft[model,bdtg]="%s %s %s %s"%(tau,lat,lon,btvmax)
                else:
                    tcft[model,bdtg]="%s : %s %s %s %s"%(tcft[model,bdtg],tau,lat,lon,btvmax)


    models=mf.uniq(models)
    bdtgs=mf.uniq(bdtgs)

    for model in models:
        for bdtg in bdtgs:
            try:
                ocard="%s %s :: %s"%(model,bdtg,tcft[model,bdtg])
                if(verb): print ocard
                ocard=ocard+'\n'
                FO.writelines(ocard)
            except:
                continue

    FO.close()

    return

    


def FnmocTrackerPosits(tpath):

    verb=0
    
    posits={}
    tcs=[]
    
    try:
        cards=open(tpath).readlines()
    except:
        return(-999,-999,-999)

    ncards=len(cards)
    card1=cards[0]
    ntc=int(card1.split()[0])
    if(verb): print card1,ncards,ntc

    ib=ntc+2
    ie=ncards
    i=ib
    while(i<ie):
        card=cards[i][:-1]
        tt=card.split()
        if (tt[0] == '***'):
            stmid=tt[1]
            stmlat=float(tt[2])
            stmlon=float(tt[3])
            tcs.append(tt[1])
            posits[stmid,'ob']=[stmlat,stmlon]
            if(verb): print 'stm lat/lon ',stmlat,stmlon
            i=i+1
            card=cards[i][:-1]
            tau=card.split()[0]
            while(tau != 'LOST' and tau != '***' and tau != 'FINISHED'):
                card=cards[i][:-1]
                tt=card.split()
                tau=tt[0]
                
                if(tau == '***'):
                    i=i-1

                elif(tau == 'FINISHED'):
                    i=i-1

                elif(not(tau == 'LOST' or tau == 'FINISHED')):
                    tau=int(tau)
                    rlat=float(tt[2])
                    rlon=float(tt[3])
                    if(verb): print stmid,i,card,tau,rlat,rlon
                    posits[stmid,tau]=[rlat,rlon]

                    i=i+1
                    

        else:
            i=i+1

    taus=range(0,121,12)
    for tc in tcs:

        if(posits[tc,0][0] == 99.9):
            posits[tc,0]=posits[tc,'ob']

        for tau in taus:
            try:
                rlat=posits[tc,tau][0]
                rlon=posits[tc,tau][1]
                if(verb): print 'tc ',tc,rlat,rlon
            except:
                if(verb): print 'tc ',tc,' no data for tau = ',tau
                posits[tc,tau]=[99.9,999.9]

    return(tcs,taus,posits)
        


    

def TcGfdlDiag (modtype,
                geopath,fldpath,prppath,
                gfdldpath,gfdlopath,gfdltpath,
                dtaudt):

    verb=0
    
    gs=[]
    gspath="p.tc.gfdl.TMP.%s.gs"%(modtype)
    gsfile=open(gspath,'w')

    g=gs.append

    g("""

function main(args)

rc=gsfallow('on')
rc=const()

modtype='%s'

geopath='%s'
fldpath='%s'
prppath='%s'

dpath='%s'
opath='%s'
tpath='%s'


_ff=ofile(fldpath)
_fp=ofile(prppath)
_fg=ofile(geopath)


#
# get metadata using first file
#
rc=metadata1('n','y','n')

tb=1
te=_nt
dt=%s
rc=gfdlanal(odir,modtype,tb,te,dt,dpath,opath,tpath)

'quit'
return

"""%(modtype,
     geopath,fldpath,prppath,
     gfdldpath,gfdlopath,gfdltpath,
     dtaudt))

    for g in gs:
        g=g+'\n'
        if(verb): print 'gggg ',g
        gsfile.writelines(g)

    gsfile.close()

    doit=''
    cmd="grads -lbc \"run %s\""%(gspath)
    mf.runcmd(cmd,doit)
    

def TCType(vmax):

    if(vmax <= 34): tctype='TD'
    if(vmax >= 35 and vmax <= 63): tctype='TS'
    if(vmax >= 64 and vmax <= 129): tctype='TY'
    if(vmax >= 130): tctype='STY'

    return(tctype)


def TCNum2Stmid(year,source=''):
    """
convert stm number -> basin ID using storms.table*
tc/p.tc.names.py year converts this to 

    """
    verb=0

    tcnames=GetTCnamesHash(year,source)

    tcs=tcnames.keys()
    shemid={}
    nioid={}
    stmids=[]
    for tc in tcs:
        stmid=tc[1]
        b1=stmid[2]
        sn=stmid[0:2]
        h1=Basin1toHemi[b1]
        if(verb): print sn,b1,h1
        stmids.append(stmid)

        #
        # logic for SLANT
        #
        
        if(h1 == 'S' and b1 != 'Q'):
            shemid[sn]=stmid

        if(b1 == 'A' or b1 == 'B'):
            nioid[sn]=stmid

    stmids.sort()

    if(verb):
        for stmid in stmids:
            print stmid

        sns=shemid.keys()
        sns.sort()

        for sn in sns:
            print 'sSSS',sn,shemid[sn]
        
        nins=nioid.keys()
        nins.sort()
        for sn in nins:
            print 'IIII',sn,nioid[sn]

    return(shemid,nioid)
        


def TCsByBasin(yyyy,basinopt,pycards,rptopt=0,tchash='null',bstmid='null',source='null'):

    curdtg=mf.dtg()
    curdtgm6=mf.dtginc(curdtg,-6)
    
    def stmhtmljs(obasin,yyyy,stm,tctype,tn,vmax,tclife,latb,lonb,bdtg,edtg,lat1,lat2,lon1,lon2,checked=''):

        bdesc=Basin1toBasinNameShort[obasin]

        bstyle=Basin1toButtonStyle[obasin]
        bcol=Basin1toButtonColor[obasin]
        
        html1="""<tr><td class="%s" onMouseOver='stm(TC["%s"],Style[20])' onMouseOut='htm()'>
<input type='radio' name="tctrk" %s onClick="stid='%s';stname='%s';stclass='%s',swap();">%s
</td></tr>"""%(bstyle,stm,checked,stm,tn,tctype,stm)

        bstyle='btnstm'
        html2="""
<tr><td
onMouseOver="this.T_STATIC=true;this.T_TITLE=TC['%s'][0];this.T_TEMP=2500;this.T_WIDTH=200;
return escape(TC['%s'][1])" >
<input type='button' class='%s' style="background-color: %s"
value='%s' name="tctrk" %s onClick="stid='%s';stname='%s';stclass='%s',swap();">
</td></tr>
"""%(stm,stm,bstyle,bcol,stm,checked,stm,tn,tctype)

        html=html2

        js="""TC['%s']=["%s - %s %s",
"\\
<b>Basin</b>: %s<br>\\
<b>V<sub>max</sub></b>:  %s kt<hr>\\
<b>Dtg range</b>: %s %s<br>\\
<b>Lifetime</b>:  %5.2f d<br>\\
<b>Lat range</b>:  %6.1f <-> %-6.1f<br>\\
<b>Lon range</b>:  %6.1f <-> %-6.1f<br>\\
"]"""%(stm,stm,tctype,tn,bdesc,vmax,bdtg,edtg,tclife,lat1,lat2,lon1,lon2)


        return(js,html)


    allhtml={}
    alljs={}
        
    #
    # set tc hash from input ...
    #

    if(tchash != 'null'):
        tn=tchash
    else:
        tn=GetTCnamesHash(yyyy,source)

    keys=tn.keys()
    keys.sort()

    stms={}
    basins=[]

    tcstats={}
    tcs=[]

    for key in keys:

        (tcyyyy,tcid)=key
        if(yyyy == tcyyyy):
            bid=tcid[2:3]
            basins.append(bid)
            try:
                stms[bid].append(tcid)
            except:
                stms[bid]=[]
                stms[bid].append(tcid)
            

    try:
        basins=mf.uniq(basins)
    except:
        print 'WWWWW nobasins in TCsbyBasins for ',basins

    obasins=basins

    if(basinopt != None):
        if(basinopt == 'GLB' or basinopt == 'G'):
            obasins=BasinsAll
        elif(len(basinopt) == 3 and mf.find(basinopt,'.') != 1):
            obasins=Hemi3toBasins[basinopt]
        else:
            obasins=basinopt.split('.')
        


    #
    # get the last storm for bstmid
    #
    
    astms=[]
    for obasin in obasins:
        try:
            for stm in stms[obasin]:
                astms.append(stm)
        except:
            pass

    astms.sort()

    #
    # case of beginning of SHEM season and no storms in nhem, bail
    #
    
    if(len(astms) == 0):
        return(tcs,tcstats,allhtml,alljs,bstmid)
        
    
    if(bstmid=='null'): bstmid=astms[-1]
    
    if(len(obasins) > 1 and rptopt == 1):
        print
        print "TC Summary by Basin for: %s"%(yyyy)
        print
        ntot=0
        for obasin in obasins:

            try:
                ntcs=len(stms[obasin])
            except:
                ntcs=0

            btitle=Basin1toBasinName[obasin]
            print "Basin: %s: %32s: %3d TCs"%(obasin,btitle,ntcs)
            ntot=ntot+ntcs

        btitle='                    Total (%s)'%(yyyy)
        print
        obasin='G'
        print "Total: %s: %32s: %3d TCs"%(obasin,btitle,ntot)
        print


    for obasin in obasins:
        
        try:
            ntcs=len(stms[obasin])
        except:
            ntcs=0
            
        if(rptopt == 1):
            btitle=Basin1toBasinName[obasin]
            print
            print "Basin: %s %32s: %2d TCs"%(obasin,btitle,ntcs)
            print

        if(ntcs == 0): continue
        
        for stm in stms[obasin]:

            if(source == 'neumann'):
                bdir=w2.TcBtNeumannDatDir
            elif(source == 'ops'):
                bdir=w2.TcBtOpsDatDir
            else:
                bdir=w2.TcBtDatDir
            
            ostm=stm
            
            btmask="%s/%s/BT.*.%s.%s.*txt"%(bdir,yyyy,yyyy,ostm)

            btpath=glob.glob(btmask)
            if(btpath):
                head=open(btpath[0]).readline()
            else:
                if(ostm[0] != '9'):
                    print "WWWWWWWWWWWWWWWWWWWWWWWW missing bt file for: %s %s %s"%(ostm,yyyy,btpath)
                continue
            
            tt=head.split()

            #for n in range(0,len(tt)):
            #    print 'tttttt ',n,tt[n]
            #  0 09E
            #  1 epc
            #  2 53
            #  3 2007080312
            #  4 2007081612
            #  5 lonbnd:
            #  6 198.5
            #  7 257.0
            #  8 latbnd:
            #  9 9.1
            #  10 17.4
            #  11 maxspd:
            #  12 120
            #  13 stcd:
            #  14 10.5
            #  15 d:
            #  16 12.25
            #  17 ace:
            #  18 22.98
            #  19 d:
            #  20 7.25
            #  21 nri:
            #  22 0
            #  23 ned:
            #  24 0
            #  25 nri:
            #  26 0
            

            bdtg=tt[3][0:11]
            edtg=tt[4][0:11]
            lon1=float(tt[6])
            lon2=float(tt[7])
            lat1=float(tt[9])
            lat2=float(tt[10])
            vmax=int(tt[12][0:3])

            if(len(tt) >= 20):
                stcd=float(tt[14])
                tcdstc=float(tt[16])
                ace=float(tt[18])
                tcdace=float(tt[20])
            else:
                stcd=-99.9
                tcdstc=0.0
                ace=-99.9
                tcdace=0
                

            if(len(tt) >= 26):
                nri=int(tt[22])
                ned=int(tt[24])
                nrw=int(tt[26])
            else:
                nri=-1
                ned=-1
                nrw=-1
                

            latb=(lat1+lat2)*0.5
            lonb=(lon1+lon2)*0.5

            tctype=TCType(vmax)

            tclife=(float(int(tt[2])-1)*6.0)/24.0

            #print head

            tcstats[stm]=(tctype,tn[yyyy,stm],vmax,tclife,latb,lonb,bdtg,edtg)
            tcs.append(stm)
            #
            # generate py card
            #
            pycard="('%s','%s'): ('%3s','%-12s', %3d, %4.1f, %5.1f, %6.1f, '%s', '%s', %5.1f, %5.2f, %5.1f, %5.2f),"%\
                    (yyyy,stm,tctype,tn[yyyy,stm],vmax,tclife,latb,lonb,bdtg,edtg,
                     stcd,tcdstc,ace,tcdace)
            pycards.append(pycard)

            if(rptopt == 1):

                livestatus='  '
                if(edtg == curdtg or edtg == curdtgm6): livestatus='--'
                RIstatus=''
                if(nri > 0): RIstatus='rrRI'
                if(ned > 0): RIstatus='rrED'
                ocard="%s %s%2s %3s %-12s : %3d : %4.1f : %5.1f %6.1f dtg: %s %s : %5.1f <-> %-5.1f : %5.1f <-> %-5.1f : %4.1f : %4.1f : %2d : %1d : %2d : %s"%\
                (yyyy,stm,livestatus,tctype,tn[yyyy,stm],vmax,tclife,latb,lonb,bdtg,edtg,
                 lat1,lat2,lon1,lon2,
                 stcd,ace,
                 nri,ned,nrw,
                 RIstatus)
                print ocard

            if(bstmid == 'null'):
                bstmid=stm
                
            if(bstmid != 'null' and stm == bstmid):
                checked='checked'
            else:
                checked=''
            (js,html)=stmhtmljs(obasin,yyyy,stm,tctype,tn[yyyy,stm],
                                vmax,tclife,latb,lonb,bdtg,edtg,lat1,lat2,lon1,lon2,checked)
            allhtml[stm]=html+"\n"
            alljs[stm]=js+"\n"

        

        
    return(tcs,tcstats,allhtml,alljs,bstmid)

    
    

def SetBidBdCard(card,syyyy,source=''):

    tcnames=GetTCnamesHash(syyyy,source)

    tt=card.split(',')
    t2=[]
    for ttt in tt:
        ttt=ttt.strip()
        t2.append(ttt)

    b2id=t2[0]
    bid=Basin2toBasin1[b2id]
    jtbid='X'
        
    #
    # parse out basics
    # 

    dtg=t2[2]
    clat=t2[6]
    clon=t2[7]
    try:
        vmax=int(t2[8])
    except:
        vmax=-99
    try:
        pmin=int(t2[9])
    except:
        pmin=-999

    (rlat,rlon,ilat,ilon,hemns,hemew)=Clatlon2Rlatlon(clat,clon)

    if(b2id == 'SH'):
        if(rlon <= 135.0):
            bid='S'
        else:
            bid='P'

        try:
            jtname=tcnames[syyyy,t2[1]+'S']
            jtbid='S'

        except:

            try:
                jtname=tcnames[syyyy,t2[1]+'P']
                jtbid='P'
            except:
                jtbid='X'
        

    if(b2id == 'IO'):
        if(rlon >= 75.0 and rlon <= 100.0):
            bid='B'
        else:
            bid='A'

    stmid=t2[1]+bid

    return(stmid,bid,jtbid)

def GrepAdeck(adpath,yyyy):

    comscardsp00=[]
    cmd="grep \'COMS,   0,\' %s"%(adpath)
    comscardsp00=os.popen(cmd).readlines()

    cmd="grep \'COMS, -12,\' %s"%(adpath)
    comscardsm12=os.popen(cmd).readlines()
    
    cmd="grep \'CNTR,   0,\' %s"%(adpath)
    cntrcardsp00=os.popen(cmd).readlines()

    #
    # 1991-1993
    #
    cmd="grep \'CNTR,   1,\' %s"%(adpath)
    cntrcardsp01=os.popen(cmd).readlines()

    cmd="grep \'WRNG,   0,\' %s"%(adpath)
    wrngcardsp00=os.popen(cmd).readlines()

    cmd="grep \'WRNG, -12,\' %s"%(adpath)
    wrngcardsm12=os.popen(cmd).readlines()

    cmd="grep \'CARQ,   0,\' %s"%(adpath)
    carqcardsp00=os.popen(cmd).readlines()

    cmd="grep \'CARQ, -12,\' %s"%(adpath)
    carqcardsm12=os.popen(cmd).readlines()

#
# no tau 0 in OFCL <= 2000 so use + 12 for tdo...
#

    cmd="grep \'JTWC,   0,\' %s"%(adpath)
    jtwccards=os.popen(cmd).readlines()
    cmd="grep \'OFCL,   0,\' %s"%(adpath)
    nhccards=os.popen(cmd).readlines()

    cmd="grep \'JTWC,  12,\' %s"%(adpath)
    jtwccardsp12=os.popen(cmd).readlines()
    cmd="grep \'OFCL,  12,\' %s"%(adpath)
    nhccardsp12=os.popen(cmd).readlines()

    adeckcards=comscardsp00+comscardsm12+\
                cntrcardsp00+cntrcardsp01+\
                wrngcardsp00+wrngcardsm12+\
                carqcardsp00+carqcardsm12+\
                jtwccards+jtwccardsp12+\
                nhccards+nhccardsp12

    cards=[]
    dtgs=[]
    if(len(adeckcards) == 0):
        bdtg='0000000000'
        edtg=bdtg
        return(cards,bdtg,edtg)
    

    for ad in adeckcards:
        dtg=ad.split()[2]
        dtg=dtg.split(',')[0]
        dtg.strip()
        dtgs.append(dtg)
        cards.append(ad[:-1])

    dtgs=mf.uniq(dtgs)
    bdtg=dtgs[0]
    edtg=dtgs[-1]
    
    return(cards,bdtg,edtg)

def scaledTC(vmax):

    tdmin=25.0
    tsmin=35.0
    tymin=65.0
    stymin=130.0

    stc=0.0
    if(vmax >= tdmin and vmax < tsmin):
        stc=0.25
        
    elif(vmax >= tsmin and vmax < tymin):
        dvmax=(vmax-tsmin)/(tymin-tsmin)
        stc=0.5+dvmax*0.5

    elif(vmax >= tymin and vmax < stymin):
        dvmax=(vmax-tymin)/(stymin-tymin)
        stc=1.0+dvmax*1.0

    elif(vmax >= stymin):
        stc=2.0
        
    return(stc)

def aceTC(vmax):
    tsmin=35.0
    if(vmax >= tsmin):
        ace=vmax*vmax
    else:
        ace=0.0
    return(ace)

    

def ParseBdeck(bdpath,yyyy,source=''):

    btcards=[]

    verb=0

    try:
        bdcards=open(bdpath).readlines()
    except:
        bdcards=None

    if(not(bdcards)):
        bdtg='0000000000'
        edtg=bdtg
        return(btcards,bdtg,edtg)
    else:
        tt=bdcards[0]
        bdtg=tt.split()[2]
        bdtg=bdtg.split(',')[0]

    bdfirstcard=bdcards[0]
    bdlastcard=bdcards[len(bdcards)-1]

    tt=bdlastcard
    edtg=tt.split()[2]
    edtg=edtg.split(',')[0]
    
    b2id=bdfirstcard.split(',')[0]
    b2id=b2id.strip()

    #
    # if shem use last card
    #

    if(b2id == 'SH'):

        (stmid,bidl,jtbid)=SetBidBdCard(bdlastcard,yyyy,source)
        (stmid,bidf,jtbid)=SetBidBdCard(bdfirstcard,yyyy,source)
        if(bidl == bidf):
            bid=bidl
        elif(bidl == 'P' and bidf == 'S'):
            bid='P'
        elif(bidl == 'S' and bidf == 'P'):
            bid='S'
        else:
            print 'EEE in ParseBdeck in sorting out the basin id'
            sys.exit()
        #
        # first posit rule works best compared to jt names
        #
        bid=bidf

        #
        # use the jtwc bid if available
        #
        
        if(jtbid != 'X'): bid=jtbid
        stmid=stmid[0:2]+bid
        
    else:
        (stmid,bid,jtbid)=SetBidBdCard(bdfirstcard,yyyy,source)

    
    stmdata={}

    dtgs=[]

    idflg=1

    for bdcard in bdcards:

        tt=bdcard.split(',')
        t2=[]
        for ttt in tt:
            ttt=ttt.strip()
            t2.append(ttt)

        #
        # parse out basics
        # 

        dtg=t2[2]

        #
        # look for non 6-h times
        #
        hh=int(dtg[8:10])

        if(hh != 0 and hh != 6 and hh != 12 and hh != 18):
            continue
        
        clat=t2[6]
        clon=t2[7]
        try:
            vmax=int(t2[8])
        except:
            vmax=-99
            
        (rlat,rlon,ilat,ilon,hemns,hemew)=Clatlon2Rlatlon(clat,clon)
        #
        # check for storms crossing the prime meridian...for nhc
        #
        if(bid == 'L' and rlon < 60.0):
            rlon=rlon+360.0
            print 'XXXXXXX crossing prime meridian',rlon
            
        
        if(len(t2) > 10):
            if(t2[9] != ''):
                pmin=int(t2[9])
            else:
                pmin=-999
            tcind=t2[10]
            if(tcind == ''): tcind='xx'
        else:
            pmin=-999
            tcind='XX'

        if(pmin == 0): pmin=-999
            
        stmdata[dtg,'tcind']=tcind
        stmdata[dtg,'stcd']=scaledTC(vmax)
        stmdata[dtg,'ace']=aceTC(vmax)


        
#SH, 23, 2005031000,   , BEST,   0, 142S, 1164E,  45,  991, TS,  34, NEQ,  120,  120,  120,  120, 1008,  160,  25,   0,   0
        dtgs.append(dtg)
        
        
        #
        # R34
        #

        r34=0.0
        r50=0.0
        if(len(t2) > 12 and t2[11] == '34'):
            if(t2[12] == 'NEQ'):
                r34ne=float(t2[13])
                r34se=float(t2[14])
                r34sw=float(t2[15])
                r34nw=float(t2[16])
                r34=r34ne+r34se+r34sw+r34nw
                r34=r34*0.25
            elif(t2[12] == 'AAA'):
                r34ne=float(t2[13])
                r34se=r34ne
                r34sw=r34ne
                r34nw=r34ne
                r34=r34ne
            else:
                r34=0.0
                r34ne=r34
                r34se=r34
                r34sw=r34
                r34nw=r34

            r34=mf.nint(r34)
            stmdata[dtg,'r34']=r34
            stmdata[dtg,'r34quad']=[r34ne,r34se,r34sw,r34nw]
            cr34="r34: %3d %3d %3d %3d"%(mf.nint(r34ne),mf.nint(r34se),mf.nint(r34sw),mf.nint(r34nw))
            stmdata[dtg,'cr34quad']=cr34
            
        #
        # R50
        #

        if(len(t2) > 12 and t2[11] == '50'):
            if(t2[12] == 'NEQ'):
                r50ne=float(t2[13])
                r50se=float(t2[14])
                r50sw=float(t2[15])
                r50nw=float(t2[16])
                r50=r50ne+r50se+r50sw+r50nw
                r50=r50*0.25
            elif(t2[12] == 'AAA'):
                r50ne=float(t2[13])
                r50se=r50ne
                r50sw=r50ne
                r50nw=r50ne
                r50=r50ne
            else:
                r50=0.0
                r50ne=r50
                r50se=r50
                r50sw=r50
                r50nw=r50
            r50=mf.nint(r50)
            stmdata[dtg,'r50']=r50
            stmdata[dtg,'r50qaud']=[r50ne,r50se,r50sw,r50nw]
            cr50="r50: %3d %3d %3d %3d"%(mf.nint(r50ne),mf.nint(r50se),mf.nint(r50sw),mf.nint(r50nw))
            stmdata[dtg,'cr50quad']=cr50
            
        #
        # load dic
        #
            
        stmdata[dtg,'rlat']=rlat
        stmdata[dtg,'rlon']=rlon
        stmdata[dtg,'vmax']=vmax
        stmdata[dtg,'pmin']=pmin

        #2004012512 10S 015 1006 -11.9  62.9 -999 -999  90.0   2.0    0
        if(verb): print bdcard[:-1]
        if(verb): print "%s %s %03i %4i %5.1f %5.1f %4i %4i"%(dtg,stmid,vmax,pmin,rlat,rlon,r34,r50)
            

    dtgs=mf.uniq(dtgs)
    np=len(dtgs)
    if(verb): print 'nnnnnnnnnnnnnnn ',np

    #
    # find bounds, 12-h motion +- 6 h around posit and -12->+0 for driving trackers/bias corr
    # also count/order TS positions
    #

    nts=0

    rlatmin=999.9
    rlatmax=-999.9
    rlonmin=999.9
    rlonmax=-999.9
    vmaxmax=-999.9
    
    tcdsumstc=0.0
    tcdsumace=0.0
    stcdsum=0.0
    acesum=0.0

    nri=0
    nrw=0
    ned=0
    
    n=0
    for dtg in dtgs:

        # -- find # of RI, RW and EDs
        #
        n24=n+4
        try:
            dtg24=dtgs[n24]
            dtg00=dtg
        except:
            dtg24=None
            dtg00=None

        if(dtg24 != None):
            tc24=IsTc(stmdata[dtg24,'tcind'])
            tc00=IsTc(stmdata[dtg00,'tcind'])
            
            if(tc00 and tc24):
                vmax00=stmdata[dtg00,'vmax']
                vmax24=stmdata[dtg24,'vmax']
                dvmax=vmax24-vmax00
                #print 'qqqqq 000 ',dtg00,dtg24,vmax00,vmax24,' dvmax: ',dvmax
                if(dvmax <= -30): nrw=nrw+1
                if(dvmax >= 30): nri=nri+1
                if(dvmax >= 50): ned=ned+1
                
        
        if(stmdata[dtg,'rlat'] <= rlatmin): rlatmin=stmdata[dtg,'rlat']
        if(stmdata[dtg,'rlat'] >= rlatmax): rlatmax=stmdata[dtg,'rlat']

        if(stmdata[dtg,'rlon'] <= rlonmin): rlonmin=stmdata[dtg,'rlon']
        if(stmdata[dtg,'rlon'] >= rlonmax): rlonmax=stmdata[dtg,'rlon']

        if(stmdata[dtg,'vmax'] >= vmaxmax): vmaxmax=stmdata[dtg,'vmax']

        n=n+1


        if(n == 1):
            dt=6.0
            odt=6.0
            rlat0=stmdata[dtg,'rlat']
            rlon0=stmdata[dtg,'rlon']
            dtgp1=mf.dtginc(dtg,+6)
            if(np>=2):
                try:
                    rlat1=stmdata[dtgp1,'rlat']
                    rlon1=stmdata[dtgp1,'rlon']
                except:
                    rlat1=rlat0
                    rlon1=rlon0
            else:
                rlat1=rlat0
                rlon1=rlon0

            orlat0=rlat0
            orlon0=rlon0
            orlat1=rlat1
            orlon1=rlon1

        elif(n == np):
            dt=6.0
            dtgm1=mf.dtginc(dtg,-6)
            rlat1=stmdata[dtg,'rlat']
            rlon1=stmdata[dtg,'rlon']

            odt=12.0
            odtgm1=mf.dtginc(dtg,-12)
            orlat1=stmdata[dtg,'rlat']
            orlon1=stmdata[dtg,'rlon']

            if(np == 2):
                odt=6.0
                try:
                    rlat0=stmdata[dtgm1,'rlat']
                    rlon0=stmdata[dtgm1,'rlon']
                    orlat0=stmdata[dtgm1,'rlat']
                    orlon0=stmdata[dtgm1,'rlon']
                except:
                    rlat0=rlat1
                    rlon0=rlon1
                    orlat0=rlat1
                    orlon0=rlon1
                    
            elif(np>=3):
                try:
                    rlat0=stmdata[dtgm1,'rlat']
                    rlon0=stmdata[dtgm1,'rlon']
                    orlat0=stmdata[odtgm1,'rlat']
                    orlon0=stmdata[odtgm1,'rlon']
                except:
                    rlat0=rlat1
                    rlon0=rlon1
                    orlat0=rlat1
                    orlon0=rlon1

                    
            else:
                rlat0=rlat1
                rlon0=rlon1
                
        elif(np >= 3):
            dt=12.0
            odt=12.0
            dtgm1=mf.dtginc(dtg,-6)
            dtgp1=mf.dtginc(dtg,+6)
            
            odtgm1=mf.dtginc(dtg,-12)
            odtgp1=mf.dtginc(dtg,+0)
            if(n == 2):
                odt=6.0
                odtgm1=mf.dtginc(dtg,-6)
                    
            try:
                rlat0=stmdata[dtgm1,'rlat']
                rlon0=stmdata[dtgm1,'rlon']
                rlat1=stmdata[dtgp1,'rlat']
                rlon1=stmdata[dtgp1,'rlon']
            except:
                rlat1=stmdata[dtg,'rlat']
                rlon1=stmdata[dtg,'rlon']
                rlat0=rlat1
                rlon0=rlon1

            try:
                orlat0=stmdata[odtgm1,'rlat']
                orlon0=stmdata[odtgm1,'rlon']
                orlat1=stmdata[odtgp1,'rlat']
                orlon1=stmdata[odtgp1,'rlon']
            except:
                orlat1=stmdata[dtg,'rlat']
                orlon1=stmdata[dtg,'rlon']
                orlat0=rlat1
                orlon0=rlon1
                
        
        vmax=stmdata[dtg,'vmax']

        if(vmax >= 35 or nts > 0): nts=nts+1

        if(n==1):
            ddtg=6.0
            
        elif(n>=2):
            dtg0=dtgs[n-2]
            dtg1=dtgs[n-1]
            ddtg=mf.dtgdiff(dtg0,dtg1)

        dtday=ddtg/24.0


        #
        # tcdays for stcd and ace
        #
        
        if(stmdata[dtg,'stcd'] > 0.0):
            tcdsumstc=tcdsumstc + dtday*1.0

        if(stmdata[dtg,'ace'] > 0.0):
            tcdsumace=tcdsumace + dtday*1.0

        stcdsum=stcdsum + dtday*stmdata[dtg,'stcd']
        acesum=acesum + stmdata[dtg,'ace']

        (course,speed,iumotion,ivmotion)=rumhdspi(rlat0,rlon0,rlat1,rlon1,dt)
        (ocourse,ospeed,oiumotion,oivmotion)=rumhdspi(orlat0,orlon0,orlat1,orlon1,odt)
        stmdata[dtg,'course']=course
        stmdata[dtg,'speed']=speed
        stmdata[dtg,'ocourse']=ocourse
        stmdata[dtg,'ospeed']=ospeed
        stmdata[dtg,'nts']=nts


    #
    #  output
    #

    #21W wpc 54 2003101806 2003103112 lonbnd: 142.8 169.4 latbnd: 016.7 032.3 maxspd: 130


    #
    # scale ace by 1/(4*65*65) to make like sTCd
    #

    
    acesum=acesum/(4.0*65.0*65.0)
    
    b3id=Basin1toBasin3[bid]
    headcard="%s %s %2i %s %s lonbnd: %5.1f %5.1f latbnd: %5.1f %5.1f maxspd: %3i  stcd: %5.1f d: %5.2f  ace: %7.2f d: %5.2f nri: %d  ned: %d  nrw: %d"%\
              (stmid,b3id,np,dtgs[0],dtgs[len(dtgs)-1],
               rlonmin,rlonmax,rlatmin,rlatmax,vmaxmax,
               stcdsum,tcdsumstc,acesum,tcdsumace,
               nri,ned,nrw)

    if(verb):
        print 'hhhhhhhhhhhhh '
        print headcard

    btcards.append(headcard)

    for dtg in dtgs:
        
        vmax=stmdata[dtg,'vmax']
        pmin=stmdata[dtg,'pmin']
        rlat=stmdata[dtg,'rlat']
        rlon=stmdata[dtg,'rlon']
        try:
            r34=stmdata[dtg,'r34']
        except:
            r34=-999
        try:
            r50=stmdata[dtg,'r50']
        except:
            r50=-999

        if(r34 == 0): r34=-999
        if(r50 == 0): r50=-999
        
        course=stmdata[dtg,'course']
        speed=stmdata[dtg,'speed']
        ocourse=stmdata[dtg,'ocourse']
        ospeed=stmdata[dtg,'ospeed']
        nts=stmdata[dtg,'nts']
        tcind=stmdata[dtg,'tcind']

        try:
            cr34=stmdata[dtg,'cr34quad']
        except:
            cr34="r34: %3d %3d %3d %3d"%(0,0,0,0)

        try:
            cr50=stmdata[dtg,'cr50quad']
        except:
            cr50="r50: %3d %3d %3d %3d"%(0,0,0,0)
            
        stmcard="%s %s %03i %4i %5.1f %5.1f %4i %4i  +6h %5.1f %4.1f  12h %5.1f %4.1f %3i %s"%\
                 (dtg,stmid,vmax,pmin,rlat,rlon,r34,r50,course,speed,ocourse,ospeed,nts,tcind)

        stmcard="%s %s %s"%(stmcard,cr34,cr50)
        
        btcards.append(stmcard)

        if(verb): print stmcard

    return(btcards,bdtg,edtg)



#
# integer iumotion, ivmotion
#
    
def rumhdspi(rlat0,rlon0,rlat1,rlon1,dt):

    verb=0

    if(verb):
        print rlat0,rlon0,rlat1,rlon1,dt,units
        
    if(tcunits == 'metric'):
        distfac=111.19
        spdfac=0.2777
    else:
        distfac=60
        spdfac=1.0
    
    rnumtor=(rlon0-rlon1)*deg2rad
    rnumtor=(rlon1-rlon0)*deg2rad
    
    d1=(45.0+0.5*rlat1)*deg2rad
    d2=(45.0+0.5*rlat0)*deg2rad

    td1=tan(d1)
    td2=tan(d2)
    rlogtd1=log(td1)
    rlogtd2=log(td2)
    rdenom=rlogtd1-rlogtd2
    rmag=rnumtor*rnumtor + rdenom*rdenom
    course=0.0
    
    if(rmag != 0.0):
        course=atan2(rnumtor,rdenom)*rad2deg

    if(course <= 0.0):
        course=360.0+course

    icourse=int(course+0.1)
    
    if(icourse ==  90.0 or icourse == 270.0 ):
        distance=distfac*abs(rlon0-rlon1)*cos(rlat0*deg2rad)
    else:
        distance=distfac*abs(rlat0-rlat1)/abs(cos(course*deg2rad))
        
    speed=distance/dt

    spdmtn=speed*spdfac
    ispeed=int(spdmtn*100+0.5)/100
    angle=(90.0-course)*deg2rad
    umotion=spdmtn*cos(angle)
    vmotion=spdmtn*sin(angle)
    iumotion=int(umotion*100+0.5)/100
    ivmotion=int(vmotion*100+0.5)/100
    if(verb): print "%5.2f %4.0f %5.2f %5.2f %5.2f %5.2f"%(distance,icourse,spdmtn,angle,umotion,vmotion)
####    print "%5.2f %5.2f"%(icourse,spdmtn)

    return(course,speed,iumotion,ivmotion)



def TcFcStatLegend(tcfcstat,tmodel,bid,taufcveristat,verb=0):

    gsname='lgndstat'
    gs=[]


    g=gs.append

    x0=0.10
    y0=0.02
    dx=1.55
    dy=0.40
    
    lgndmodels=['ofc','clp','gfs','ngp','ukm','eco']
    nmodels=len(lgndmodels)

    xst=(x0+dx*nmodels)*0.5
    xst=(x0+0.1)
    yst=y0+dy+0.125
    ssizt=0.08
    titlet="`0%s-h FE [nm] + (N cases) + %% Improve over Cliper [MeanAbs Intensity Error (kt), Bias (F-O) kt)]`0"%(taufcveristat)
    
    
    g("function %s"%(gsname))

    
    g('x0=%f'%(x0))
    g('y0=%f'%(y0))
    g('dx=%f'%(dx))
    g('dy=%f'%(dy))

    g('lcol=81')
    g('bcolact=21')
    g('bcolinact=31')

    g("'set line 1 0 4'")
    g("'set string 4 ' l ' 4'")
    g("'set strsiz %s'"%(ssizt))
    g("'draw string %f %f %s'"%(xst,yst,titlet))
    
    tcmodels=[]
    tcmodelstats={}
    if(tcfcstat):
        tcs=tcfcstat.keys()
        tcs.sort()
        if(verb): print tcs
        for tc in tcs:
            if(mf.find(tc,taufcveristat)):
                model=tc.split('.')[0]
                ttt=tcfcstat[tc]
                n72bt=ttt[0]
                modeln=ttt[1]
                modelpod=mf.nint(ttt[2])
                modelimpclp=mf.nint(ttt[3])
                modelfe=mf.nint(ttt[4])
                try:
                    modelfve=mf.nint(ttt[10])
                    modelfveu=mf.nint(ttt[11])
                except:
                    modelfve='--'
                    modelfveu='--'
                    

                tcmodels.append(model)
                tcmodelstats[model]=(modeln,modelpod,modelimpclp,modelfe,modelfve,modelfveu)

                if(verb):
                    print 'mmmm ',ttt
                    print 'mmmm ',model,modeln,modelpod,modelimpclp,modelfe,
                    print 'mmmmiiii ',modelfve,modelfveu


    n=0
    for lgndmodel in lgndmodels:

        try:
            (modeln,modelpod,modelimpclp,modelfe,modelfve,modelfveu)=tcmodelstats[lgndmodel]

            lmodel=lgndmodel.upper()
            if(lmodel == 'ECO'): lmodel='ECMWF(ops)'
            if(lmodel == 'ECE'): lmodel='ECMWF(EPS)'

            if(modeln == 0):
                cell1="_title.1.1=\'%s (%s) '"%(lmodel,n72bt)
                cell2="_title.2.1=\'---\'"
                cell3="_title.2.2=\'---\'"

            else:
                cell1="_title.1.1=\'%s (%s) '"%(lmodel,n72bt)
                cell2="_title.2.1=\'`4%s`0 (%s)\'"%(modelfe,modeln)
                cell3="_title.2.2=\'%s[%s,%s]\'"%(modelimpclp,modelfve,modelfveu)

        except:
            cell1="_title.1.1=\'---\'"
            cell2="_title.2.1=\'---\'"
            cell3="_title.2.2=\'---\'"

        card="%s ; %s ; %s"%(cell1,cell2,cell3)

        bcol='bcolinact'
        if(lgndmodel == tmodel): bcol='bcolact'
        
        if(n==0):
            g('_title.1.1=\'Model (N bt)\'    ;    _title.2.1=\'FE (N fc)\'   ;   _title.2.2=\'%clp[IE,IB]\'')
            g('rc=prntstat(x0,y0,dx,dy,lcol)')
            g(card)
            g('x0=x0+dx')
            g("rc=prntstat(x0,y0,dx,dy,%s)"%(bcol))
            
        else:
            g(card)
            g('x0=x0+dx')
            g("rc=prntstat(x0,y0,dx,dy,%s)"%(bcol))

        n=n+1



    g('return')
    
    gspath="%s.gsf"%(gsname)
    gsfile=open(gspath,'w')

    for gg in gs:
        gg=gg+'\n'
        if(verb): print gg[:-1]
        gsfile.write(gg)
        
    gsfile.close()

    return


def TcVeriStatModelLegend(model):

    if(model == 'gfs'):
        mtcen='NCEP'
        mtmod='GFS (T254L64)'
        mtup='GFS'
        
    elif(model == 'ecm'):
        mtcen='ECMWF'
        mtmod='IFS Cy28r1 (T`bL`n799L90)'
        mtup='IFS(ops)'

    elif(model == 'eco'):
        mtcen='ECMWF'
        mtmod='IFS Cy28r1 (T`bL`n511L60)'
        mtup='IFS(ops)'

    elif(model == 'ofc'):
        mtcen='JTWC/NHC'
        mtmod='Official Forecast'
        mtup='OFC'
        
    elif(model == 'ece'):
        mtcen='ECMWF'
        mtmod='EPS(T`bL`n255L40)'
        mtup='IFS(eps)'

    elif(model == 'ngp'):
        mtcen='FNMOC'
        mtmod='NOGAPS 4.0 (T239L30)'
        mtup='NGP'

    elif(model == 'ukm'):
        mtcen='UKMO'
        mtmod='UM (0.83x0.55 L38)'
        mtup='UKM'
        
    elif(model == 'clp'):
        mtcen='NRL/ATCF'
        mtmod='CLIPER'
        mtup='CLP'

    elif(model == 'fv4'):
        mtcen='NASA/SIVO'
        mtmod='GEOS4'
        mtup='FV4'

    elif(model == 'fv5'):
        mtcen='NASA/SIVO'
        mtmod='GEOS5'
        mtup='FV5'

    elif(model == 'fd5'):
        mtcen='NASA/SIVO'
        mtmod='GEOS5+DAS'
        mtup='FD5'

    elif(model == 'con'):
        mtcen='MODCON'
        mtmod='CON_'
        mtup='CON'

    elif(model == 'cn3'):
        mtcen='CON3'
        mtmod='CON3'
        mtup='CON3'

    elif(model == 'cn4'):
        mtcen='CON4'
        mtmod='CON4'
        mtup='CON4'

    elif(model == 'cne'):
        mtcen='CONE'
        mtmod='CONE'
        mtup='CONE'

    elif(model == 'cnf'):
        mtcen='CONF'
        mtmod='CONF'
        mtup='CONF'

    elif(model == 'cne'):
        mtcen='PONE'
        mtmod='PONE'
        mtup='PONE'

    elif(model == 'gfd'):
        mtcen='GFDL'
        mtmod='GFDL'
        mtup='GFDL'


    else:
        print 'EEE invalid model in TcVeriStatModelLegend'
        sys.exit()

    return(mtcen,mtmod,mtup)

def GetShemYear(dtg):
    #
    # convert year in stm dtg to basinyear
    #

    yyyy=int(dtg[0:4])
    mm=int(dtg[4:6])

    if(mm >= 7): yyyy=yyyy+1

    cyyyy=str(yyyy)

    return(cyyyy)
    
    

def CurShemOverlap(curdtg):

    #
    # need to run twice in overlap between shem and nhem seasons
    #

    cy=curdtg[0:4]
    
    
    icym0=int(cy)
    icyp1=icym0+1
    cyp1=str(icyp1)
    
    icymd0=int(curdtg[0:8])

    ccymd0e=str(icym0)+'1231'
    icymd0e=int(ccymd0e)

    ccymdshemb=str(icym0)+'0701'
    icymdshemb=int(ccymdshemb)

    shemoverlap=0
    if(icymd0 >= icymdshemb and icymdshemb <= icymd0e): shemoverlap=1

    return(shemoverlap,cy,cyp1)


def IsShemBasinStm(stmid):

    if(len(stmid) != 3 and len(stmid) != 1):
        return(-1)

    if(len(stmid) == 3):
        ustmid=stmid[2].upper()
    else:
        ustmid=stmid.upper()

    if(ustmid == 'S' or ustmid == 'P' or ustmid == 'Q'):
        return(1)
    else:
        return(0)
    
def IsModelPhr(model):
    lm=len(model)
    mext=model[lm-2:lm]
    mbase=model[0:lm-2]
    modelopt=model
    rc=0
    if(mext == '00' or mext == '06' or mext == '12'):
        modelopt=mbase
        rc=1

    return(rc,modelopt)
        
def w2ij(wi,wj,ni,nj,wi0,wj0,dwi,dwj):
    
    i=(wi-wi0)/dwi + 0.5
    j=(wj-wj0)/dwj + 0.5

    #
    # cyclic continuity in x
    #
    
    if(i <  0.0): i=float(ni)+i
    if(i >   ni): i=i-float(ni)

    i=int(i+1.0)
    j=int(j+1.0)

    return(i,j)

import copy

dLatLonEcmwfEPSAnalysis=1.0

dTau=12


def SetFtpServer(pushcenter):
    
    if(pushcenter == 'llnl'):
        server='sprite.llnl.gov'
        ftpdirput='/var/ftp/pub/fiorino/npmoc'
    
    elif(pushcenter == 'npmoc'):
        server='blackgbs.npmoc.navy.mil'
        server='199.10.200.38'
        ftpdirput='/comms_dir/llnl/ecmwf'

    return(server,ftpdirput)



def PingFtpServer(server):

    tt=server.split('.')
    if(len(tt) == 3):
        servercheck=tt[0]
    elif(len(tt) == 4 and tt[0].isdigit()):
        servercheck=server
    else:
        servercheck=server

    dsec=5
    nsec=1
    nsecmax=nsec+2*dsec

    verb=0
    while(nsec<=nsecmax):
        cmd='ping -w %s %s'%(nsec,server)
        #
        # uset popen4 because stdout and stderr go to O
        #
        (I,O)=os.popen4(cmd)
        try:
            cards=O.readlines()
        except:
            cards=[]

        status=1
        for card in cards:
            if(verb): print server,'ccc',card
            if(mf.find(card,'0 received')):
                status=0
            elif(mf.find(card,'unknown host')):
                status=-1

        if(status==1):
            break

        elif(status == -1):
            print "unknown host: %s; bail"%(server)
            status=0
            break
            
        else:
            nsec=nsec+5
            print "bump ping wait to: %d ; try again"%(nsec)
        
        
    return(status)

def CheckFtpServer(server):

    tt=server.split('.')
    if(len(tt) == 3):
        servercheck=tt[0]
    elif(len(tt) == 4):
        servercheck=server
        
    verb=1
    cmd='traceroute %s'%(server)
    cards=os.popen(cmd).readlines()
    status=0
    for card in cards:
        if(verb): print server,card
        if(card.find(servercheck) != -1): status=1
    return(status)

def RegionalCtl(dtg,ni,nj,blat,dlat,blon,dlon,undef,taus):

    nt=len(taus)
    dt=12
    gtime=mf.dtg2gtime(dtg)
    
    ctl="""dset ^t.dat
title test
undef %s
xdef %3d linear %5.1f  %5.1f
ydef %3d linear %5.1f  %5.1f
zdef   1 levels 1013
tdef %3d linear %s %dhr
vars 1
n 0 0 # of ensembles per grid box and tau [nd] 
endvars"""%(str(undef),
            ni,blon,dlon,
            nj,blat,dlat,
            nt,gtime,dt)

    #print ctl

    cpath='/tmp/t.ctl'
    c=open(cpath,'w')
    c.writelines(ctl)
    c.close()

    return(cpath)
                          
    
def ParseEcmwfTracksMsl(cards,stmid,trktype):

    """
    parse psl ecmwf tracks (msl in ec terms)

    """

    verb=0
    members=[]
    increments={}
    etrk={}

    if(trktype == 'eco'):
        dtaumsl=6.0
    elif(trktype == 'ece'):
        dtaumsl=12.0

    ib=4
    n=len(cards)
    if(verb): print 'MSL ',n

    i=ib
    while(i<n):
        
        tt=cards[i].split()

        lat=float(tt[0])
        lon=float(tt[1])
        #
        # convert to deg E
        #
        if(lon < 0.0): lon=360.0+lon
        member=int(tt[2])
        
        if(trktype == 'msl'):
            if(member == 52):
                dtaumsl=6.0
            else:
                dtaumsl=12.0
        
        members.append(member)
        yyyymmdd=tt[3]
        hh=int(tt[4])/100
        pmin=float(tt[5])
        vmax=HolidayAtkinsonPsl2Vmax(pmin)
        #
        # boost max wind and round to nearest 5
        #
        EcmwfVmaxAliasFactor=1.25
        vmax=vmax*EcmwfVmaxAliasFactor
        vmax=int((vmax/5.0)+0.5)*5.0

        
        tcparms=(lat,lon,pmin,vmax)
        try:
            etrk[member].append(tcparms)
        except:
            etrk[member]=[]
            etrk[member].append(tcparms)
            
        increments[member]=dtaumsl

        i=i+1


    nmembers=mf.uniq(members)
    
    return(nmembers,increments,etrk)

def ParseEcmwfTracks(cards,obsflg):

    verb=0
    members=[]
    increments={}
    etrk={}
    
    stmid=cards[1].split()[2]
    stmname=cards[2].split()[2]

    print stmid
    print stmname

    ib=4
    if(obsflg): ib=6
    n=len(cards)

    if(verb):
        i=ib
        while(i<n):
            print 'ccc ',i,cards[i][:-1]
            i=i+1

    i=ib
    while(i<n):
        if(verb): print 'ccc ',i,cards[i][:-1]
        member=int(float(cards[i].split()[1]))
        members.append(member)
        i=i+1
        increment=float(cards[i].split()[1])
        i=i+1
        nsteps=int(float(cards[i].split()[3]))
        if(verb): print 'nnn ',member,nsteps,increment

        increments[member]=increment
        i=i+1
        trk=[]
        for j in range(0,nsteps):
            tt=cards[i].split()
            lat=float(tt[0])
            lon=float(tt[1])
            #
            # convert to deg E
            #
            if(lon < 0.0): lon=360.0+lon
            pmin=float(tt[2])
            vmax=float(tt[3])*ms2knots
            if(verb): print i,j,i,lat,lon,pmin,vmax
            tcparms=(lat,lon,pmin,vmax)
            trk.append(tcparms)
            i=i+1
        etrk[member]=trk
            

    return(members,increments,etrk)


#
#  move ecmwf files to data dir
#

def RegionalGrid(blat,elat,dlat,blon,elon,dlon,undef,taus):

    InitialValue=0.0

    latsiz=elat-blat
    lonsiz=elon-blon
    
    grid={}
    ni=int(lonsiz/dlon)+1
    nj=int(latsiz/dlat)+1
    nij=ni*nj

    Initial=0.0

    for tau in taus:
        for i in range(0,ni):
            for j in range(0,nj):
                ii=j*ni + i
                grid[ii,tau]=InitialValue
    
            
    return(ni,nj,nij,grid)

def GlobalGrid(dlon,dlat,undef,taus):

    grid={}
    ni=int(360.0/dlon)
    nj=int(180.0/dlat)+1
    nij=ni*nj

    InitialGrid=0.0

    for tau in taus:
        for i in range(0,ni):
            for j in range(0,nj):
                ii=j*ni + i
                grid[ii,tau]=InitialGrid
    
            
    return(ni,nj,nij,grid)


def ll2i(lon,lat,dlon,dlat,lon0,lat0,ni,nj):

    i=(lon - lon0)/dlon + 0.5 
    j=(lat - lat0)/dlon + 0.5 

    if(i<=0): i=ni+i
    if(i>=ni): i=i-ni

    i=int(i+1.0)
    j=int(j+1.0)

    ii=(j-1)*ni + i

    return(ii)

def LatLonBounds(lats,lons,
                 latbuff=10.0,lonbuff=15.0):

    latinc=loninc=5.0
    
    latmaxplot=50.0
    lonmaxplot=80.0

    maxlat=maxlon=-999.9
    minlat=minlon=999.9

    for lat in lats:
        if(lat < minlat): minlat=lat
        if(lat > maxlat): maxlat=lat

    for lon in lons:
        if(lon < minlon): minlon=lon
        if(lon > maxlon): maxlon=lon

    latbar=(minlat+maxlat)*0.5
    lonbar=(minlon+maxlon)*0.5

    nj1=int( minlat/latinc+0.5 )
    nj2=int( maxlat/latinc+0.5 )
    nj3=int( minlon/loninc+0.5 )
    nj4=int( maxlon/loninc+0.5 )

    j1=nj1*latinc
    j2=nj2*latinc
    j3=nj3*loninc
    j4=nj4*loninc

    latplotmin=j1-latbuff
    latplotmax=j2+latbuff
    lonplotmin=j3-lonbuff
    lonplotmax=j4+lonbuff
    
    return(latplotmin,latplotmax,lonplotmin,lonplotmax)
                                
    latplotmin=int( (latbar - (latmaxplot/2) )/latinc + 0.5)*latinc
    latplotmax=latplotmin + latmaxplot

    lonplotmin=int( (lonbar - (latmaxplot/2) )/loninc + 0.5)*loninc
    lonplotmax=lonplotmin + lonmaxplot
    
    return(latplotmin,latplotmax,lonplotmin,lonplotmax)


def MakeTauTrack(ectrack,taus,inctau):
    
    track={}
    ttau=0
    for e in ectrack:
        for tau in taus:
            if(ttau == tau):
                track[ttau]=e
        ttau=ttau+inctau

    return(track)

    
def MakeAdeck(model,ostmid,dtg,adeckdir,ectrack,server,ftpdirput,
              trktype='all',doftp=1,verb=0):

    taus=ectrack.keys()
    taus.sort()
    
    stmnum=ostmid[0:2]
    basin1=ostmid[2:3]
    basin2=Basin1toBasin2[basin1]
    adeckname=ModelNametoAdeckName[model]
    adecknum=ModelNametoAdeckNum[model]
    r34ne=r34se=r34sw=r34nw=0
    adum=0

    if(trktype == 'all'):
        adeckfile="wxmap.%s.%s.%s"%(model,dtg,ostmid)
    else:
        adeckfile="wxmap.MSL.%s.%s.%s"%(model,dtg,ostmid)

    apath="%s/%s"%(adeckdir,adeckfile)

    if(verb):
        print 'AAAAA making adeck to: ',apath
    a=open(apath,'w')

    for tau in taus:

        itau=int(tau)
        (lat,lon,pmin,vmax)=ectrack[tau]

        ivmax=int(vmax)
        ipmin=int(pmin)

        (ilat,ilon,hemns,hemew)=Rlatlon2Clatlon(lat,lon)

        acard0="%2s, %2s, %10s, %2s, %4s, %3d,"%(basin2,stmnum,dtg,adecknum,adeckname,itau)

        acard1=" %3d%1s, %4d%1s, %3d, %4d, XX,  34, NEQ, %4d, %4d, %4d, %4d, %4d, %4d, %3d, %3d, %3d,"%\
                (ilat,hemns,ilon,hemew,ivmax,ipmin,r34ne,r34se,r34sw,r34nw,adum,adum,adum,adum,adum)

        acard=acard0+acard1
        if(verb): print acard
        a.writelines(acard+'\n')

    a.close()

    if(doftp):
        
        #
        # ftp put adeck
        #
        mf.doFTPsimple(server,adeckdir,ftpdirput,adeckfile)

    return(apath)

def AnalyzeMembers2Grid(members,increments,etrk,dlat,dlon,undef,taus,dtg):

    verb=0
    
    lats=[]
    lons=[]

    for member in members:
        trk=etrk[member]
        for t in trk:
            (lat,lon,pmin,vmax)=t
            lats.append(lat)
            lons.append(lon)

    (blat,elat,blon,elon)=LatLonBounds(lats,lons)
    (ni,nj,nij,grid)=RegionalGrid(blat,elat,dlat,blon,elon,dlon,undef,taus)

    cpath=RegionalCtl(dtg,ni,nj,blat,dlat,blon,dlon,undef,taus)

    ntau={}
    for tau in taus:
        ntau[tau]=0.0

    for member in members:
        dt=increments[member]
        trk=etrk[member]
        rtau=0.0

        for t in trk:
            (lat,lon,pmin,vmax)=t
            itau=int(rtau)

            ii=ll2i(lon,lat,dlon,dlat,blon,blat,ni,nj)
            for tau in taus:
                if(itau == tau):
                    ##print 'iiiii increment ',tau,ii
                    grid[ii-1,tau]=grid[ii-1,tau]+1.0
                    ntau[tau]=ntau[tau]+1.0

            rtau=rtau+dt


    if(verb):
        for tau in taus:
            print 'tau = ',tau,ntau[tau]
    
    import array

    g=array.array('f')

    (dir,file)=os.path.split(cpath)
    (base,ext)=os.path.splitext(file)

    dpath="%s/%s.dat"%(dir,base)

    o=open(dpath,'wb')

    ngrid=[]

    for tau in taus:

        if(tau == 0):
            for i in range(0,ni):
                for j in range(0,nj):
                    ii=j*ni + i
                    ngrid.append(0.0)


        for i in range(0,ni):
            for j in range(0,nj):
                ii=j*ni + i
                if(grid[ii,tau] > 0.0):
                    ngrid[ii]=grid[ii,tau]
                    if(verb): print 'BBBBBBBBB ',ii,tau,ngrid[ii]
                if(grid[ii,tau] == 0.0):
                    ngrid[ii]=undef


        #print 'writing tau = ',tau
        g.fromlist(ngrid)

    g.tofile(o)

    o.close()

    return(cpath)


def GetEcmwfEpsTcs(paths,verb=0):

    paths.sort()

#    paths=[
#        '/pcmdi/ftp_incoming/fiorino/tracks_06L_2004082600.fm',
#        '/pcmdi/chico_dat/wxmap2/dat/tc/fc/ecmwf/eps/tracks_22W_2004082400.fm',
#        '/pcmdi/ftp_incoming/fiorino/tracks_06L_2004082512.fm',
#        ]

    etcs=[]
    for path in paths:
        if(verb): print 'ECTC path       : ',path
        (dir,filePext)=os.path.split(path)
        (file,ext)=os.path.splitext(filePext)

        trktype='all'
        
        tt=file.split('_')

        if(len(tt) == 5):
            if(tt[1] == 'det'): trktype='eco'
            if(tt[1] == 'eps'): trktype='ece'
            dtg=tt[4]
            istmid=tt[3]
        elif(len(tt) == 3 and tt[0] != 'msl'):
            dtg=tt[2]
            istmid=[1]
        elif(len(tt) == 3 and tt[0] == 'msl'):
            trktype='msl'
            dtg=tt[2]
            istmid=[1]

        #
        # check for case with no tracks
        #
        if(trktype == 'eco'):
            mincards=4
        elif(trktype == 'ece'):
            mincards=100
        elif(trktype == 'all' or trktype == 'msl'):
            mincards=200

        tcs=findtc(dtg)

        ecards=open(path).readlines()
        necards=len(ecards)

        if(verb):
            for tc in tcs:
                print 'ECTC obs tc: ',tc
            print 'ECTC file,istmid,dtg : ',file,istmid,dtg
            print 'ECTD necards,trktype : ',necards,trktype
            
            for ecard in ecards:
                print ecard[:-1]
        
        
        if(necards > mincards):

            if(trktype == 'all'):
                
                istmid=ecards[1].split()[2]
                istmname=ecards[2].split()[2]

                #
                # search for a member with initial position -- the first one might not have one...
                #
                #
                # 20040902 new format may have obs lat/lon
                #

                ichk=6

                obslat=obslon=None
                obsflg=0
                
                testlat=ecards[3].split()
                testlon=ecards[4].split()

                if(testlat[1] == 'lat:'):
                    obslat=float(testlat[2])
                    
                if(testlon[1] == 'lon:'):
                    obslon=float(testlon[2])

                if(obslat and obslon):
                    print "OOOOOOOOOOOOO obslat: %5.1f %6.1f"%(obslat,obslon)
                    ichk=8
                    obsflg=1

                
                #for i in range(0,len(ecards)):
                #    if(i < 20):
                #        print i,ecards[i][:-1]
                
                nmember=int(float(ecards[ichk].split()[3]))

                if(nmember != 0):
                    ilatlon=ichk+1
                else:
                    while(nmember == 0):
                        ichk=ichk+3
                        nmember=int(float(ecards[ichk].split()[3]))
                        if(verb): print '000000 ',ichk,nmember

                    ilatlon=ichk+1

            elif(trktype == 'eco'):
                ilatlon=4
                nmember=52
                
            elif(trktype == 'ece'):
                ilatlon=4
                nmember=51

            elif(trktype == 'msl'):
                ilatlon=3
                nmember=52

            ee=ecards[ilatlon].split()
            
            if(verb): print 'nnnn ',nmember,ilatlon
            istmlat=float(ee[0])
            istmlon=float(ee[1])

            distmin=1e20
            distmin=250.0
            i=0
            imin=-999
            for tc in tcs:
                tcid=tc.split()[1]
                tclat=float(tc.split()[4])
                tclon=float(tc.split()[5])
                dist=gc_dist(tclat,tclon,istmlat,istmlon)
                if(dist < distmin):
                    distmin=dist
                    imin=i
                #print '11 ',dist,' 222 ',tcid,tclon,istmlat,istmlon
                i=i+1

            #
            # no match
            #
            if(imin<0):
                tcard=(None,path,dtg,None,None)
            else:
                ostmid=tcs[imin].split()[1]
                tcard=(ostmid,path,dtg,trktype,obsflg)
                
            etcs.append(tcard)

    return(etcs)

#
# verification TCs by dtg, Must BE >= 20 kts!!!!!
#

def FindTcsBtMoFinal(dtg,verb=0):

    vmaxmin=20.0
    
    yyyy=dtg[0:4]
    yyyymm=dtg[0:6]
    yyyymmp1=mf.yyyymminc(yyyymm,1)

    btmopath="%s/%s/bt.%s.final.txt"%(BtDir,yyyy,yyyymm)

    if(verb):
        print 'btmopath: ',btmopath

    try:
        b=open(btmopath)
    except:
        print 'EEEE unable to open ',btmopath
        sys.exit()

    cmd="grep -s -h %s %s"%(dtg,btmopath)
    cards=os.popen(cmd).readlines()

    tcs=[]
    for card in cards:
        tt=card.split()
        vmax=float(tt[2])

        if(vmax >= vmaxmin):
            tcs.append(card[:-1])
        
    return(tcs)


def ReadBtMoFinal(dtg):

    yyyy=dtg[0:4]
    yyyymm=dtg[0:6]
    yyyymmp1=mf.yyyymminc(yyyymm,1)

    btmopath="%s/%s/bt.%s.final.txt"%(BtDir,yyyy,yyyymm)

    try:
        b=open(btmopath)
    except:
        print 'EEEE unable to open ',btmopath
        sys.exit()


    cards=b.readlines()
    b.close()

    btcs={}
    btstmids={}
    btcstms={}
    
    for card in cards:
        tt=card.split()
        dtg=tt[0]
        stmid=tt[1]
        vmax=int(tt[2])
        pmin=int(tt[3])
        lat=float(tt[4])
        lon=float(tt[5])
        dir=float(tt[8])
        spd=float(tt[9])
        btdata=(lat,lon,vmax,pmin,dir,spd)
        btdatadtg=(dtg,lat,lon,vmax,pmin,dir,spd)
        btcs[dtg,stmid]=btdata
        try:
            btstmids[dtg].append(stmid)
        except:
            btstmids[dtg]=[stmid]

        try:
            btcstms[stmid].append(btdatadtg)
        except:
            btcstms[stmid]=[btdatadtg]
            

    return(btcs,btstmids,btcstms)

def MakeBtMoFinal(dtg,verb=0):

    yyyy=dtg[0:4]
    yyyymm=dtg[0:6]
    yyyymmp1=mf.yyyymminc(yyyymm,1)

    btmopath="%s/%s/bt.%s.final.txt"%(BtDir,yyyy,yyyymm)

    print 'btmopath ',btmopath

    b=open(btmopath,'w')

    ddtg=6
    bdtg=yyyymm+'0100'
    edtg=yyyymmp1+'2100'

    vdtgs=mf.dtgrange(bdtg,edtg,ddtg)

    for vdtg in vdtgs:
        if(verb): print 
        tcs=findtc(vdtg)
        for tc in tcs:
            b.writelines(tc+'\n')
            if(verb): print tc

    b.close()


    return()



def ParseFtCards(dtg,cards):

    verb=0
    
    stms=[]
    ftcs={}

    #
    # for older tracking files check if cyclones
    #
    if(cards[0].find('NO CY') != -1):
        print 'WWWW \'NO CYCLONES TO TRACK\' message in track file...'
        return(ftcs)

    
    nstms=int(cards[0].split()[0])

    if(verb):
        print 'nnnn ',nstms,cards[nstms+2]

    n=-1
    for card in cards:
        
        n=n+1
        if(n < nstms+2): continue
        if(verb): print card[:-1]
        tt=card.split()

        if( ( tt[0] == '***') or ( tt[0] != 'LOST' and tt[0] != 'FINISHED') ):

            #
            # new style storm from tracker SSS.YYYY
            #

            try:
                ss=tt[1].split('.')
                stm=ss[0]
            except:
                stm=tt[1]
            
            stms.append(stm)
            
            if( tt[0] == '***'):
                latwarn=float(tt[2])
                lonwarn=float(tt[3])
                ftcs[stm]=[(latwarn,lonwarn)]
            
            else:
                tau=int(tt[0])
                sdtgm12=mf.dtginc(dtg,tau-12);
                sdtgp12=mf.dtginc(dtg,tau+12);
                sdtg=mf.dtginc(dtg,tau);
                lat=float(tt[2])
                lon=float(tt[3])
                ccirc='CC'
                if(float(tt[6]) < 0): ccirc='VM'

                ft=(tau,sdtg,sdtgm12,sdtgp12,lat,lon,ccirc)

                try:
                    ftcs[stm].append(ft)
                except:
                    print 'EEEEEEEEE no warning posit for: ',stm
                    sys.exit()

   
    #
    # extend fc track to taumax (120) with 999 to for force detection of
    # bt for POD purposes
    #

    taumax=120
    
    stms=mf.uniq(stms)
    #
    # check for an fc with no posits
    # add a noload
    #
    donoload=0
    for stm in stms:
        
        np=len(ftcs[stm])
        if(np == 1):
            ft=(0,dtg,dtg,dtg,99.9,999.9,'CC')
            ftcs[stm].append(ft)
            
        if(donoload):
            (latwarn,lonwarn)=ftcs[stm][0]
            ftcs[stm]=[(latwarn,lonwarn)]
            ft=(0,dtg,dtg,dtg,99.9,999.9,'CC')
            ftcs[stm].append(ft)

    
    for stm in stms:
        np=len(ftcs[stm])-1
        (ftau,fsdtg,sdtgm12,sdtgp12,lat,lon,ccirc)=ftcs[stm][np]

        if(ftau < taumax):
            npall=taumax/dTau+1
            sdtg=fsdtg
            tau=ftau+dTau
            for i in range(np+1,npall+1):
                sdtg=mf.dtginc(sdtg,dTau)
                sdtgm12=mf.dtginc(sdtg,-dTau)
                sdtgp12=mf.dtginc(sdtg,+dTau)
                alat=99.9
                alon=999.9
                accirc='CC'
                ftadd=(tau,sdtg,sdtgm12,sdtgp12,alat,alon,accirc)
                ftcs[stm].append(ftadd)
                tau=tau+dTau
                

    return(ftcs)

def TcClass(vmax):

    if(vmax < 30): tcclass='nt'
    if(vmax >=30 and vmax < 35): tcclass='td'
    if(vmax >=35 and vmax < 65): tcclass='ts'
    if(vmax >=65 and vmax < 130): tcclass='ty'
    if(vmax >=130): tcclass='st'
    #
    # case where vmax missing...
    #
    if(vmax == 999): tcclass='nt'

    return(tcclass)
    

def AnalyzeBtCards(cards,stmname):

    verb=0
    btsummary=''
    gdtg35='1776070400'
    glat35=-99.9
    glon35=-999.9

    nnt=0
    ntd=0
    nts=0
    nty=0
    nst=0
    nt=0
    ng=0

    ng35=0
    gflg=0
    gflg35=0
    eflg=0

    tcvmax=0.0

    tccs=[]
    dtgs=[]

    for card in cards[1:]:
        #print card.strip()
        tt=card.split()
        dtg=tt[0]
        stmid=tt[1]
        vmax=int(tt[2])
        rlat=float(tt[4])
        rlon=float(tt[5])

        if(vmax > tcvmax): tcvmax=vmax

        tcc=TcClass(vmax)

        tccs.append(tcc)
        dtgs.append(dtg)
        
        if(tcc == 'nt'): nnt=nnt+1
        if(tcc == 'td'): ntd=ntd+1
        if(tcc == 'ts'): nts=nts+1
        if(tcc == 'ty'): nty=nty+1
        if(tcc == 'st'): nst=nst+1
        
        #
        # genesis point
        #
        
        if(ntd == 1 and nts == 0 and nty == 0 and nst == 0):
            if(verb): print 'GGGG at TD'
            ng=1
        if(ntd == 0 and nts == 1 and nty == 0 and nst == 0):
            if(verb): print 'GGGGSSSS at TS'
            ng=2
        if(ntd == 0 and nts == 0 and nty == 1 and nst == 0):
            if(verb): print 'GGGGTTTTTTTTT at TY!!!!'
            ng=3
        if(ntd == 0 and nts == 0 and nty == 0 and nst == 1):
            if(verb): print 'GGGGTTTTTTTTTSSSSSSSSSSSSSS  at STY!!!!'
            ng=4
        

        #
        # 35 kt genesis point
        #
        
        if(nts == 1):
            if(verb): print 'GGGG at TD'
            ng35=1
            
        if(ng > 0 and gflg == 0):
            gdtg=dtg
            glat=rlat
            glon=rlon
            if(verb): print 'GGGGGG at: ',gdtg
            gflg=1
            
        if(ng35 > 0 and gflg35 == 0):
            gdtg35=dtg
            glat35=rlat
            glon35=rlon
            if(verb): print 'GGGGGG33333555555 at: ',gdtg35
            gflg35=1
            
            
        if(verb): print "%s %s %3d %5.1f %6.1f :: %s"%(dtg,stmid,vmax,rlat,rlon,tcc)

        nt=nt+1


    #
    # work backword for endpoint
    #

    nc=len(tccs)

    edtg=dtgs[nt-1]
    for n in range(nc-1,0,-1):
        if(eflg == 0 and tccs[n] != 'nt'):
            eflg=1
            edtg=dtgs[n]

    #
    # case of NO posit >= 30 kt
    #

    if(nt > 0 and gflg == 0):
        gdtg='9999999999'
        edtg=gdtg
        tclifetime=-99.99
        glat=-99.9
        glon=-99.9
    else:
        tclifetime=(mf.dtgdiff(gdtg,edtg)+6.0)/24.0

    
    sumcard="%s %s :: %12s :: %s %s %6.2f :: %5.1f %6.1f :: %5.1f"%\
             (gdtg[0:4],stmid,stmname,gdtg,edtg,tclifetime,glat,glon,tcvmax)
    #sumcard="%s ::  nt:  %3d  :: nnt: %2d  ntd: %2d  nts: %2d  nty: %2d  nst: %2d"%\
    sumcard="%s ::  %3d  :: %2d  %2d  %2d  %2d %2d"%\
             (sumcard,nt,nnt,ntd,nts,nty,nst)

    sumcard="%s ::  gdtg35: %s :: %5.1f %6.1f"%\
             (sumcard,gdtg35,glat35,glon35)

    print sumcard
    return(sumcard)
    

def StripList(list):
    nlist=[]
    for tt in list:
        ttt=tt.strip()
        nlist.append(ttt)
    return(nlist)
    

def GrepTcVeriSum(veridir,veritype,verirule,model,tau,area,areaid,undef,years,verb=0):

    sumdata={}

    noload=[]
    
    ns=7
    for i in range(0,ns):
        noload.append(undef)
        
    noload=tuple(noload)
    
    for year in years:
        sumdata[year]=(noload)

    vmask="%s/tc.veri.sum.%s.????.%s.txt"%(veridir,veritype,verirule)

    cmd="grep -s -h \' %s, \' %s | grep -s  \' %s, \' | grep -s \' %s, \' | grep -s \' %s, \' "%\
         (model,vmask,tau,area,areaid)

    cards=os.popen(cmd).readlines()

    if(verb): print 'vvvvvvvvvv model,verirule,tau,area: ',model,verirule,tau,area
    
    for card in cards:
        
        tt=card.split(',')
        ttt=StripList(tt)
        yyyy=int(ttt[0].split('.')[1])
        tt=tuple(ttt[6:13])
        (nbt,nfc,pod,fe,impclp,ate,cte)=tt
        #print yyyy,model,nbt,nfc,pod,fe,impclp,ate,cte
        sumdata[yyyy]=(tt)

    print

    return(sumdata)
        

def VarTcVeriSum(varopt,sumdata,undef,years):

    ovar=[]

    for year in years:
        (nbt,nfc,pod,fe,impclp,ate,cte)=sumdata[year]
        if(float(pod) == 0.0):
            pod=undef
            fe=undef
            impclp=undef
            
        if(varopt == 'pod'):
            print 'ssss ',year,nbt,nfc,pod,varopt
            ovar.append(float(pod))
        elif(varopt == 'fe'):
            print 'ssss ',year,fe,varopt
            ovar.append(float(fe))
        elif(varopt == 'impclp'):
            print 'ssss ',year,impclp,varopt
            ovar.append(float(impclp))
        elif(varopt == 'nbt'):
            print 'ssss ',year,impclp,varopt
            ovar.append(float(nbt))
        elif(varopt == 'nfc'):
            print 'ssss ',year,impclp,varopt
            ovar.append(float(nfc))
        else:
            print 'EEE invalid varopt in VarTcVerSum: %s'%(varopt)

    return(ovar)

def AreaName(area,areaid):
    
    varaeid='99'
    if(area == 'hemi'):
        if(areaid == 'W'): vareaid='WESTPAC'
        if(areaid == 'EP'): vareaid='EASTPAC'
        if(areaid == 'N'): vareaid='NHEM'
        if(areaid == 'S'): vareaid='SHEM'
    
    if(area == 'basin'):
        if(areaid == 'W'): vareaid='WESTPAC'
        if(areaid == 'E'): vareaid='EASTPAC'
        if(areaid == 'L'): vareaid='LANT'
        if(areaid == 'S'): vareaid='SHEM'

    return(vareaid)


def VarOptName(varopt):

    if(varopt == 'impclp'):
        tvaropt='% improve over CLP'
    elif(varopt == 'fe'):
        tvaropt='FE (nm)'
    elif(varopt == 'pod'):
        tvaropt='POD [%]'
    elif(varopt == 'nbt'):
        tvaropt='N (BT) [#]'
    elif(varopt == 'nfc'):
        tvaropt='N (fc) [#]'

    return(tvaropt)


def VeriRuleName(vr):
    
    tt=vr.split('.')

    if(tt[1] == 'hetero'): vtype="Hetero"
    if(len(tt) >= 3):
        if(tt[2] == 'hetero'): vtype="Hetero"

    if(tt[1] == 'homo'): vtype="Homogeneous %s:%s"%(tt[2],tt[3])

    if(len(tt) >= 3):
        if(tt[2] == 'homo'): vtype="Homogeneous %s:%s"%(tt[3],tt[4])

    if(vr.find('nhc.pure') != -1): veriname="%s %s"%(vtype,'NHC')
    if(vr.find('jtwc') != -1): veriname="%s %s"%(vtype,'JTWC')
    if(vr.find('jtwc.mod') != -1): veriname="%s %s"%(vtype,'JTWC(mod)')
    if(vr.find('td30') != -1): veriname="%s %s"%(vtype,'>= TD')
    if(vr.find('nhc.wind') != -1): veriname="%s %s"%(vtype,'>= TS')
    
    return(veriname)



def ModelName(model):
    
    if(model == 'e40'): modelname="ERA-40"
    elif(model == 'ecm'): modelname="ECMWF IFS"
    elif(model == 'clp'): modelname="CLIPER"
    elif(model == 'clp'): modelname="CLIPER"
    elif(model == 'ngp'): modelname="NOGAPS"
    
    return(modelname)




def VarCardTcVeriSum(varopt,verirule,model,tau,area,areaid,nv,nt):

    vtau="%03d"%(int(tau))
    vtau="%d"%(int(tau))

    tvaropt=VarOptName(varopt)
    vareaid=AreaName(area,areaid)
    veriname=VeriRuleName(verirule)
    modelname=ModelName(model)
    
    vardesc="%s(%s) : `3t`0=%s : %s : %s : %s"%(modelname,model,vtau,tvaropt,veriname,vareaid)
    varname="v%s"%(nv)
    varcard="%s 0 -1,20,%s   %s"%(varname,nt,vardesc)

    return(varname,vardesc,varcard)

#--------------------------------------------------
#
# title - veri rules
#
#--------------------------------------------------

def TitleVeriRules(verirules):

    title='Veri Rules: '
    nvr=len(verirules)

    if(nvr>1): title=title+' 1) '

    for i in range(0,nvr):

        vr=verirules[i]
        
        veriname=VeriRuleName(vr)

        title=title+veriname

        if(i>=0 and i<nvr-1 and nvr>1): title=title+"; %d) "%(i+2)

    return(title)
        

def TitleModels(models):

    title='Models: '
    nvr=len(models)

    if(nvr>1): title=title+'1) '
    
    for i in range(0,nvr):
        model=models[i]
        modelname=ModelName(model)
        title=title+"%s(%s)"%(modelname,model)

        if(i>=0 and i<nvr-1 and nvr>1): title=title+"; %d) "%(i+2)

    return(title)
        

def TitleTaus(taus):

    title='Taus: '

    nvr=len(taus)
    if(nvr>1): title=title+' 1) '
    
    for i in range(0,nvr):
        tau=int(taus[i])
        title=title+"%d"%(tau)
        
        if(i>=0 and i<nvr-1 and nvr>1): title=title+"; %d) "%(i+2)

    return(title)
        

def TitleAreas(areas):

    title='Basins: '

    nvr=len(areas)
    if(nvr>1): title=title+' 1) '
    
    for i in range(0,nvr):
        vr=areas[i]
        tt=vr.split('.')
        area=tt[0]
        areaid=tt[1]
        areaname=AreaName(area,areaid)
        title=title+"%s"%(areaname)
        if(i>=0 and i<nvr-1 and nvr>1): title=title+"; %d) "%(i+2)

    return(title)
        
def TitleVarOpts(varopts):

    title=''

    nvr=len(varopts)
    if(nvr>1): title=title+' 1) '
    
    for i in range(0,nvr):
        vr=varopts[i]
        varoptname=VarOptName(vr)
        title=title+"%s"%(varoptname)
        if(i>=0 and i<nvr-1 and nvr>1): title=title+"; %d) "%(i+2)

    return(title)
        

def OrderTcPlotVars(verirules,models,areas,taus,varopts,igvars):

    nvr=len(verirules)
    nvo=len(varopts)
    na=len(areas)
    nm=len(models)
    nt=len(taus)

    verirules=verirules
    models=models
    areas=areas
    taus=taus
    varopts=varopts
    
    ogvars=[]

    fastest='models'
    if(nvr > 1 and nvr >= nm): fastest='verirules'
    if(nm > 1 and nm >=nvr): fastest='models'
    if(nm == 3 and nm >= nvr): fastest='verirules'

    altcol=1

    if(fastest=='verirules'):
        
        altcol=nvr
        for varopt in varopts:
            for model in models:
                for area  in areas:
                    for tau in taus:
                        for v1 in verirules:
                            (vn,vd)=igvars[varopt,tau,area,model,v1]
                            ogvars.append([vn,vd])

    elif(fastest=='models'):
        
        altcol=nm
        for varopt in varopts:
            for area  in areas:
                for tau in taus:
                    for v1 in verirules:
                        for model in models:
                            (vn,vd)=igvars[varopt,tau,area,model,v1]
                            ogvars.append([vn,vd])

    else:
        for v1 in verirules:
            for model in models:
                for area  in areas:
                    for tau in taus:
                        for varopt in varopts:
                            (vn,vd)=igvars[varopt,tau,area,model,v1]
                            ogvars.append([vn,vd])
            

    return(altcol,ogvars)



def SetHomoRule(hiopt):
    
    #
    # homo opts
    #

    homorule='hetero'
    homomodel1=''
    homomodel2=''
    dohomo=0

    if(hiopt != 'null' and hiopt != 'hetero'):

        hh=hiopt.split('.')
        if(len(hh) == 2):
            dohomo=1
            homomodel1=hh[0]
            homomodel2=hh[1]
            homorule='homo.%s.%s'%(homomodel1,homomodel2)
        else:
            print "EEE invalid homo compare options: %s"%(hiopt)
            sys.exit()
            
    return(homorule,homomodel1,homomodel2,dohomo)


def GetTcStatsDic(TCS,basinopt,modelopt):

    if(basinopt == 'NHS'):
        try:
            statsdic=TCS.tcfcNHS
        except:
            statsdic=None

    elif(basinopt == 'SHS'):
        try:
            statsdic=TCS.tcfcSHS
        except:
            statsdic=None
    
    elif(basinopt == 'LTS'):
        try:
            statsdic=TCS.tcfcLTS
        except:
            statsdic=None

    elif(basinopt == 'WPS'):
        try:
            statsdic=TCS.tcfcWPS
        except:
            statsdic=None

    elif(basinopt == 'EPS'):
        try:
            statsdic=TCS.tcfcEPS
        except:
            statsdic=None

    elif(basinopt == 'NIS'):
        try:
            statsdic=TCS.tcfcNIS
        except:
            statsdic=None

    elif(len(basinopt) == 1):
        try:
            statsdic=TCS.tcfcbasin[basinopt]
        except:
            statsdic=None

    models=modelopt.split('.')

    if(statsdic):
        sk=statsdic.keys()
        sk.sort()
    else:
        return(None,None,None)


    stats={}
    taus=[]
    
    for model in models:

        for k in sk:

            tmodel=k.split('.')[0]
            tau=k.split('.')[1]
            taus.append(tau)
            if(tmodel == model):
                try:
                    stats[model,tau].append(statsdic[k])
                except:
                    stats[model,tau]=[]
                    stats[model,tau].append(statsdic[k])
    taus=mf.uniq(taus)
    taus.sort()

    return(models,taus,stats)


    
def ParseFtMfCards(dtg,cards):


    #
    # 20041007: handle bad data
    #
    
    def splitfc(cards,i,undef):

        try:
            scard=cards[i]
        except:
            scard='undef '

        try:
            tt=scard.split()
            tlon=float(tt[1])
            tlat=float(tt[2])
            tval=float(tt[3])
            tdist=gc_dist(flat,flon,tlat,tlon)
        except:
            tdist=tval=tlon=tlat=undef
            
        return(tdist,tval,tlon,tlat)

    def splittau(cards,i):
        tt=cards[i].split()
        type=tt[0]
        tau=int(float(tt[2]))
        stmid=tt[4]
        flon=float(tt[5])
        flat=float(tt[6])
        #print type,tau,stmid,flon,flat
        i=i+1

        tt=cards[i].split()
        #print i,tt
        nhi=int(tt[0])
        nlo=int(tt[1])
        i=i+1

        return(type,tau,stmid,flon,flat,nhi,nlo,i)


    verb=0

    undef=1e20
    
    dcrit={}
    dcrit['SPD','H']=400.0
    dcrit['SPD','L']=200.0
    dcrit['VRT','H']=400.0
    dcrit['VRT','L']=200.0

    ftcstruct={}

    stms=[]
    ftcs={}

    ncards=len(cards)

    for i in range(0,ncards):

        if(mf.find(cards[i],'tau:')):
           
           (type,tau,stmid,flon,flat,nhi,nlo,i)=splittau(cards,i)

           tdcrit=dcrit[type,'H']
           tdmin=undef
           for j in range(0,nhi):
               (tdist,tval,tlon,tlat)=splitfc(cards,i,undef)
               if(tdist < tdcrit and tdist < tdmin):
                   tdmin=tdist
                   tvalcrit=tval
               if(verb): print 'hi ',i,tdcrit,tdist,tlon,tlat,tval,ncards
               i=i+1

           if(type == 'SPD'): typeout='spdmax'
           if(type == 'VRT'): typeout='vrtmax'
           if(tdmin == undef):
               tdmin=-888.8
               tvalcrit=-88.8
           ftcstruct[stmid,tau,typeout,'dist']=tdmin
           ftcstruct[stmid,tau,typeout,'val']=tvalcrit
         
           if(verb):
               print "hhhhhhhhhhh stm: %s tau: %03d type: %s ::  %7.1f  %7.2f"%\
                     (stmid,tau,type,tdmin,tvalcrit)


           tdcrit=dcrit[type,'L']
           tdmin=undef
           for j in range(0,nlo):
               (tdist,tval,tlon,tlat)=splitfc(cards,i,undef)
               if(tdist < tdcrit and tdist < tdmin):
                   tdmin=tdist
                   tvalcrit=tval
               if(verb): print 'lo ',i,tdist,tlon,tlat,tval
               i=i+1
               
           if(type == 'SPD'): typeout='spdmin'
           if(type == 'VRT'): typeout='vrtmin'
           if(tdmin == undef):
               tdmin=-888.8
               tvalcrit=-88.8
           ftcstruct[stmid,tau,typeout,'dist']=tdmin
           ftcstruct[stmid,tau,typeout,'val']=tvalcrit
         

           if(verb):
               print "lllllllllll stm: %s tau: %03d type: %s ::  %7.1f  %7.2f"%\
                     (stmid,tau,type,tdmin,tvalcrit)

           #print 'eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee ',i

            


    return(ftcstruct)
        

def GetftcstrucParms(ftcstruct,fcid,tau):
    
    try:
        fmaxspd=ftcstruct[fcid,tau,'spdmax','val']
    except:
        fmaxspd=-88.8

    try:
        fminspd=ftcstruct[fcid,tau,'spdmin','val']
    except:
        fminspd=-88.8

    try:
        fmaxvrt=ftcstruct[fcid,tau,'vrtmax','val']
    except:
        fmaxvrt=-88.8

    try:
        fminvrt=ftcstruct[fcid,tau,'vrtmin','val']
    except:
        fminvrt=-88.8

    try:
        fmaxspddist=ftcstruct[fcid,tau,'spdmax','dist']
    except:
        fmaxspddist=-888.8

    try:
        fminspddist=ftcstruct[fcid,tau,'spdmin','dist']
    except:
        fminspddist=-888.8

    try:
        fmaxvrtdist=ftcstruct[fcid,tau,'vrtmax','dist']
    except:
        fmaxvrtdist=-888.8

    try:
        fminvrtdist=ftcstruct[fcid,tau,'vrtmin','dist']
    except:
        fminvrtdist=-888.8

    return(fmaxspddist,fminspd,fminspddist,fmaxvrt,fmaxvrtdist,fmaxspd)

def FilterHemiTcs(tcs,hemi):
    btcs=[]
    for tc in tcs:
        tt=tc.split()
        tcbasin=tt[1].split('.')[0][2:3]
        tchemi=Basin1toHemi3[tcbasin]
        if(tchemi == hemi):
            btcs.append(tc)
            
    tcs=btcs
    return(tcs)
    

def FilterBasinTcs(tcs,basin):
    btcs=[]
    for tc in tcs:
        tt=tc.split()
        tcbasin=tt[1].split('.')[0][2:3]
        if(tcbasin == basin):
            btcs.append(tc)
            
    tcs=btcs
    return(tcs)
    
#--------------------------------------------------
#
#  load w2 adecks into dic
#
#--------------------------------------------------

def LoadW2TcFcCards(stmopt,year,phr,imodel,amodel,verb=0):

    ftmfcards=None
    ftcards=None
    
    ftdir=AdeckDirW2
    ftype='adeck'

    ftmask='%s/%s/w2.adeck.%s.%s.*'%(ftdir,year,imodel,stmopt)
    if(verb): print 'W2 ADECK ftmask: ',ftmask
    ftpaths=glob.glob(ftmask)
    
    if(verb):
        print 'adeck data for : ',imodel,' ftpaths: ',ftpaths

    ftcards=[]    
    for ftpath in ftpaths:
        (d,f)=os.path.split(ftpath)
        cards=open(ftpath).readlines()
        for card in cards:
            ftcards.append(card)

    aftcards={}

    if(phr != None):
        tamodel="%s%02d"%(amodel,int(phr))
    else:
        tamodel=amodel
        
    for ftcard in ftcards:
        tt=ftcard.split(',')
        dtg=tt[2].strip()
        iamodel=tt[4].strip()
        if(iamodel == tamodel):
            try:
                aftcards[dtg].append(ftcard)
            except:
                aftcards[dtg]=[]
                aftcards[dtg].append(ftcard)

    return(aftcards)

#--------------------------------------------------
#
#  get w2 ftcards from adecks dic by dtg
#
#--------------------------------------------------

def GetTcFcCardsW2(dtg,amodel,phr,aftcards,verb=0):

    ftmfcards=None
    ftype='adeck'

    try:
        ftcards=aftcards[dtg]
    except:
        ftcards=None

    if(ftcards != None and verb):
        for ftcard in ftcards:
            print 'qqq ',ftcard[:-1]

    return(ftcards,ftmfcards,ftype)


        
def ParseVdeck2Fcs(cards):

    #  0 gfsn
    #  1 018
    #  2 16L.2007
    #  3 2007102400
    #  4 2007102418
    #  5 FLG:
    #  6 BNT_FMR
    #  7 TC
    #  8 LO
    #  9 NC
    #  10 NW
    #  11 NC
    #  12 NW
    #  13 TDO:
    #  30 17.7
    #  31 287.8
    #  32 WP:
    #  33 20.5
    #  34 286.2
    #  35 FP:
    #  36 19.4
    #  37 288.8
    #  38 BW:
    #  39 45.0
    #  40 FW:
    #  41 32.0
    #  42 CW:
    #  43 45.0
    #  44 WW:
    #  45 45.0
    #  46 FS:
    #  47 -888.8
    #  48 -88.8
    #  49 -888.8
    #  50 -88.8
    #  51 -888.8
    #  52 CT:
    #  53 CC
    #  54 CT_AT(nm):
    #  55 98.4
    #  56 -104.8
    #  57 -91.1
    #  58 111.2
    #  59 135.5
    #  60 -48.0
    #  61 BVd:
    #  62 0
    #  63 FVd:
    #  64 35
    #  65 23
    #  66 FV:
    #  67 60
    #  68 51
    #  69 32
    #  70 FVe:
    #  71 15
    #  72 6
    #  73 -13
    #  74 fcR34:
    #  75 173
    #  76 0
    #  77 0
    #  78 0
    #  79 fcR50:
    #  80 -999
    #  81 -999
    #  82 -999
    #  83 -999

    fcs={}
    dtgs=[]
    
    for card in cards:
        tt=card.split()

        #for i in range(0,len(tt)):
        #    print 'vvvv ',i,tt[i]

        tau=int(tt[1])
        bdtg=tt[3]
        vdtg=tt[4]

        tdo=tt[14]
        
        bdir=float(tt[21])
        bspd=float(tt[22])
        
        cqdir=float(tt[24])
        cqspd=float(tt[25])
        
        blat=float(tt[27])
        blon=float(tt[28])
        bvmax=float(tt[39])
        cqvmax=float(tt[43])

        bflgtc=tt[7]
        bflgind=tt[8]
        bflgcq=tt[9]
        bflgwn=tt[10]

        ffe=float(tt[16])

        blf=float(tt[18])
        flf=float(tt[19])
        
        cqlat=float(tt[30])
        cqlon=float(tt[31])

        flat=float(tt[36])
        flon=float(tt[37])
        fvmax=float(tt[41])

        fcte=float(tt[55])
        fate=float(tt[56])
        ffcte=float(tt[57])
        ffate=float(tt[58])
        fewe=float(tt[59])
        fnse=float(tt[60])

        fve=float(tt[71])
        fveu=float(tt[72])
        fver=float(tt[73])
        
        if(len(tt) >= 84):

            ir=75
            r34ne=int(tt[ir]) ; ir=ir+1
            r34se=int(tt[ir]) ; ir=ir+1
            r34sw=int(tt[ir]) ; ir=ir+1
            r34nw=int(tt[ir]) ; ir=ir+2

            r50ne=int(tt[ir]) ; ir=ir+1
            r50se=int(tt[ir]) ; ir=ir+1
            r50sw=int(tt[ir]) ; ir=ir+1
            r50nw=int(tt[ir]) ; ir=ir+1
            
        else:
            
            r34ne=r34se=r34sw=r34nw=-992
            r50ne=r50se=r50sw=r50nw=-992


        r34quad=[r34ne,r34se,r34sw,r34nw]
        r50quad=[r50ne,r50se,r50sw,r50nw]

        if(tau == 0):
            fcs[bdtg,'mot']=[bdir,bspd]
            fcs[bdtg,'btflg']=[bflgtc,bflgind,bflgcq,bflgwn]
            fcs[bdtg,'bt']=[blat,blon,bvmax,blf]
            fcs[bdtg,'cq']=[cqlat,cqlon,cqvmax,cqdir,cqspd]
            
        fcs[bdtg,tau]=[vdtg,flat,flon,fvmax,flf,ffe,fcte,fate,ffcte,ffate,fewe,fnse,r34quad,r50quad]
        fcs[bdtg,tau,'vmax']=[bvmax,fvmax,fve,fveu,fver]
        fcs[bdtg,tau,'tdo']=tdo
        fcs[bdtg,tau,'bt']=[blat,blon,bvmax,blf]
        fcs[bdtg,tau,'btflg']=[bflgtc,bflgind,bflgcq,bflgwn]
        
        ####print '33334444: ',len(tt),fcs[bdtg,tau,'r34'],fcs[bdtg,tau,'r50']

        dtgs.append(bdtg)

    dtgs=mf.uniq(dtgs)

    return(dtgs,fcs)



#--------------------------------------------------
#
#  track extrap using motion
#
#--------------------------------------------------

def TrackBtCqExtrap(itrk,taus,blat,blon,cqlat,cqlon,verb=1):

    otrk=copy.deepcopy(itrk)
                   
    #
    # find fc taus
    #
    
    ftaus=[]

    for tau in taus:
        flat=otrk[tau][1]
        if(flat > -90.0 and flat < 88.0 ):
            ftaus.append(tau)

    #
    # check for noshow/noload
    #
    ntaus=len(ftaus)
    if(ntaus == 0): return(otrk)

    #
    # save target taus and replace input taus with forecast taus
    #
    
    taus=ftaus
    
    ntau=len(taus)
    etau=taus[ntau-1]

    
    i=0
    while(i< ntau):

        #
        # case of only initial position and no fc posits
        #
        
        if(ntau > 1):
            tau0=taus[i]
            tau1=taus[i+1]
        else:
            tau0=taus[i]
            tau1=tau0

        if(tau0 == etau):
            tau0=taus[i-1]
            tau1=taus[i]

            
        dtau=tau1-tau0
        
        flat0=itrk[tau0][1]
        flon0=itrk[tau0][2]
        fvmax0=itrk[tau0][3]

        flat1=itrk[tau1][1]
        flon1=itrk[tau1][2]
        fvmax1=itrk[tau1][3]

        if(tau0 != tau1):
            (fdir,fspd,fiumot,fivmot)=rumhdsp(flat0,flon0,flat1,flon1,dtau)

        if(tau0 == 0):
            
            if(cqlat > -90.0 and cqlat < 88.0):
                otrk[tau0][1]=cqlat
                otrk[tau0][2]=cqlon
            else:
                otrk[tau0][1]=blat
                otrk[tau0][2]=blon
                
            otrk[tau0][3]=fvmax0

            #
            # bail of only one tau
            #
            if(ntaus == 1): break
                
            
        eflat0=otrk[tau0][1]
        eflon0=otrk[tau0][2]

        (eflat1,eflon1)=rumltlg(fdir,fspd,dtau,eflat0,eflon0)
                
        otrk[tau1][1]=eflat1
        otrk[tau1][2]=eflon1
        
        if(verb):
            print
            print '--- ',i,tau0,tau1,dtau
            print '000 ',flat0,flon0
            print '111 ',eflat1,eflon1
            print 'fc: ',fdir,fspd,fiumot,fivmot

        i=i+1

        if(i == ntau-1): break

    if(verb):
        i=0
        while(i< ntau):
            tau0=taus[i]
            olat0=otrk[tau0][1]
            olon0=otrk[tau0][2]
            ilat0=itrk[tau0][1]
            ilon0=itrk[tau0][2]
            print "AAA---XXXXX %03i in: %5.1f %6.1f  out: %5.1f %6.1f"%(tau0,ilat0,ilon0,olat0,olon0)
            i=i+1
            if(i == ntau): break


    return(otrk)



def MakeAdeckCards(model,ostmid,dtg,fctrk,phr='',verb=0):

    taus=fctrk.keys()
    taus.sort()
    
    stmnum=ostmid[0:2]
    basin1=ostmid[2:3]
    basin2=Basin1toBasin2[basin1]
    adeckname=atcf.ModelNametoAdeckName[model]
    adecknum=atcf.ModelNametoAdeckNum[model]

    if(phr != ''):
        adeckname=adeckname+phr
    elif(phr == 'O'):
        adeckname=adeckname+phr
    
    r34ne=r34se=r34sw=r34nw=0
    adum=0

    acards=[]
    
    for tau in taus:

        itau=int(tau)
        (vdtg,lat,lon,vmax,flf,ffe,fcte,fate,ffcte,ffate,fewe,fnse,r34quad,r50quad)=fctrk[tau]

        if(lat < -90.0 or lat > 88.0): continue

        ivmax=int(vmax)
        ipmin=0

        (clat,clon,ilat,ilon,hemns,hemew)=Rlatlon2Clatlon(lat,lon)

        try:
            (r34ne,r34se,r34sw,r34nw)=r34quad
        except:
            r34ne=r34se=r34sw=r34nw=-999
                
        try:
            (r50ne,r50se,r50sw,r50nw)=r50quad
        except:
            r50ne=r50se=r50sw=r50nw=-999

        adextra=''
        if(len(adeckname) == 4): adextra='  '
        if(len(adeckname) == 5): adextra=' '
        acard0="%2s, %2s, %10s, %2s, %4s, %s%3d,"%(basin2,stmnum,dtg,adecknum,adeckname,adextra,itau)

        acard1=" %3d%1s, %4d%1s, %3d, %4d,   ,  34, NEQ, %4d, %4d, %4d, %4d, %4d, %4d, %3d, %3d, %3d,"%\
                (ilat,hemns,ilon,hemew,ivmax,ipmin,r34ne,r34se,r34sw,r34nw,adum,adum,adum,adum,adum)

        acard1=" %3d%1s, %4d%1s, %3d, %4d,   ,  34, NEQ, %4d, %4d, %4d, %4d,   50, NEQ, %4d, %4d, %4d, %4d,"%\
                (ilat,hemns,ilon,hemew,ivmax,ipmin,r34ne,r34se,r34sw,r34nw,r50ne,r50se,r50sw,r50nw)


        acard=acard0+acard1
        if(verb): print acard
        acards.append(acard)

    return(acards)


def PrintInOutTrk(taus,itrk,otrk):
    ntaus=len(taus)
    i=0
    while(i< ntaus):
        tau0=taus[i]
        olat0=otrk[tau0][1]
        olon0=otrk[tau0][2]
        ilat0=itrk[tau0][1]
        ilon0=itrk[tau0][2]
        print "AAA----PPPP %03i in: %5.1f %6.1f  out: %5.1f %6.1f"%(tau0,ilat0,ilon0,olat0,olon0)
        i=i+1
        if(i == ntaus): break

    return


#
# set BT verification flags
#

def SetBtVdeck(stmid,model,dtgs,fcs,ruleopt=None,filtsynhh=None,verb=0):

    if(ruleopt == None):
        oruleopt='ops'
    else:
        oruleopt=ruleopt
        
    idtgs=copy.deepcopy(dtgs)

    b1id=stmid[2:3]
    b3id=Basin1toBasin3[b1id]

    chk12hrops=0
    if(b3id == 'nio' or b3id == 'shm' or b3id == 'slt'): chk12hrops=1

    docarqchk=((ruleopt != None) and (ruleopt == 'carq'))
    dowarnchk=((ruleopt != None) and (ruleopt == 'warn'))

    oruleaddopt=''
    if(docarqchk or dowarnchk): oruleaddopt=ruleopt
    
    #
    # set up fc taus
    #
    
    btau=0
    etau=120
    dtau=12
    taus=range(btau,etau+1,dtau)
    ntaus=len(taus)

    lfmax=0.95

    #
    # set up veriflag
    #
    
    btvflgjtwc={}
    btvflgnhc={}

    btgcards=[]

    if(filtsynhh == '0012Z'):
        dtgs=[]
        for idtg in idtgs:
            hh=idtg[8:10]
            if(hh == '00' or hh == '12'): dtgs.append(idtg)
    elif(filtsynhh == '0012Z'):
        dtgs=[]
        for idtg in idtgs:
            hh=idtg[8:10]
            if(hh == '06' or hh == '18'): dtgs.append(idtg)



    btgcard="N bt: %d"%(len(dtgs))
    btgcards.append(btgcard)

    blatmax=-99.0
    blatmin=99.0
    blonmin=999.9
    blonmax=-999.9

    blatmaxall=-99.0
    blatminall=99.0
    blonminall=999.9
    blonmaxall=-999.9


    #
    # bt analysis
    #
    
    bttime2warn=0.0
    bttime2carq=0.0
    bttime2end=0.0

    bttimeflgwarn=0
    bttimeflgcarq=0
    bttimeflgend=0
    
    dtg0=dtgs[0]
    curtime0=0.0
    ndtg=0

    dtimebt=6.0

    for dtg in dtgs:

        curtime=mf.dtgdiff(dtg0,dtg)
        dcurtime=curtime-curtime0
        
        [bflgtc,bflgind,bflgcq,bflgwn]=fcs[dtg,'btflg']
        [blat,blon,bvmax,blf]=fcs[dtg,'bt']

        if(bttimeflgcarq == 0 and bflgcq != 'CQ'):
            bttime2carq=bttime2carq+dtimebt
        else:
            bttimeflgcarq=1
            
        if(bttimeflgwarn == 0 and bflgwn != 'WN'):
            bttime2warn=bttime2warn+dtimebt
        else:
            bttimeflgwarn=1

        if(verb):
            print 'tttt ',ndtg,curtime,dcurtime
            print '  cq ',bflgcq,bttimeflgcarq,bttime2carq
            print '  wn ',bflgwn,bttimeflgwarn,bttime2warn

        if(bttimeflgcarq == 1 and bttimeflgwarn == 1): break

        curtime0=curtime
        ndtg=ndtg+1

    bttime2end=0.0
    bttimeflgend=0

    rdtgs=copy.deepcopy(dtgs)
    rdtgs.reverse()

    dtgend=dtgs[0]

    ndtg=0

    for dtg in rdtgs:

        curtime=mf.dtgdiff(dtgend,dtg)
        dcurtime=curtime-curtime0
        
        [bflgtc,bflgind,bflgcq,bflgwn]=fcs[dtg,'btflg']
        [blat,blon,bvmax,blf]=fcs[dtg,'bt']

        curtime0=curtime

        if(bttimeflgend == 0 and bflgwn != 'WN'):
            bttime2end=bttime2end+dtimebt
        else:
            bttimeflgend=1
            break

        if(verb):
            print 'eee ',ndtg,dtg,curtime,dcurtime,
            print 'end ',bflgwn,bttimeflgend,bttime2end,blat,blon,bvmax,blf
        
        ndtg=ndtg+1
    

    
    #
    #  set verification flag
    #

    edtg=1776070412
    
    for dtg in dtgs:
        
        dtgp6=mf.dtginc(dtg,6)
        dtgm6=mf.dtginc(dtg,-6)
        try:
            [blat,blon,bvmax,blf]=fcs[dtgp6,'bt']
            blfp6=blf
        except:
            blfp6=None

        try:
            [blat,blon,bvmax,blf]=fcs[dtgm6,'bt']
            blfm6=blf
        except:
            blfm6=None

        
        [bflgtc,bflgind,bflgcq,bflgwn]=fcs[dtg,'btflg']
        [blat,blon,bvmax,blf]=fcs[dtg,'bt']

        isnotcarq = not((bflgcq == 'CQ'))
        isnotwarn = not((bflgwn == 'WN'))

        #
        # logic for 12-h warning cycle
        #
        if(chk12hrops):
            try:
                [bflgtc99,bflgind99,bflgcqm6,bflgwnm6]=fcs[dtgm6,'btflg']
            except:
                [bflgtc99,bflgind99,bflgcqm6,bflgwnm6]=fcs[dtg,'btflg']
            
            try:
                [bflgtc99,bflgind99,bflgcqp6,bflgwnp6]=fcs[dtgp6,'btflg']
            except:
                [bflgtc99,bflgind99,bflgcqp6,bflgwnp6]=fcs[dtg,'btflg']

            ischkwn=(bflgwnm6 == 'WN') and (bflgwn == 'NW') and (bflgwnp6 == 'WN') 
            ischkcq=(bflgcqm6 == 'CQ') and (bflgcq == 'NW') and (bflgcqp6 == 'CQ') 

            isnotcarq = not( (bflgcq == 'CQ') or ( (bflgcqm6 == 'CQ') and (bflgcq == 'NC') and (bflgcqp6 == 'CQ') ) )
            isnotwarn = not( (bflgwn == 'WN') or ( (bflgwnm6 == 'WN') and (bflgwn == 'NW') and (bflgwnp6 == 'WN') ) )
            

        #
        # jtwc flag
        #
        if(
            (bflgtc == 'TC') and
            ( (bflgcq == 'CQ') or (bflgwn == 'WN') ) and
            (bflgind != 'EX') and (bflgind != 'LO') 
            ):

            #
            # + land flag (require +- 6 h posit bt land
            #
            btvflgjtwc[dtg]=1
            if(blf >= lfmax):
                if( (blfm6 >= lfmax) or (blfp6 >= lfmax) ):  
                    btvflgjtwc[dtg]=-1
                else:
                    btvflgjtwc[dtg]=2


        else:
            btvflgjtwc[dtg]=0


        if(docarqchk and isnotcarq and btvflgjtwc[dtg] != 0):
            btvflgjtwc[dtg]=0
            ###print 'tttttttttttt jjjjjjjjj CCCCCCCCCCC turning off jtwc for docarq ',dtg
            
        if(dowarnchk and isnotwarn and btvflgjtwc[dtg] != 0):
            btvflgjtwc[dtg]=0
            ###print 'tttttttttttt jjjjjjjjj WWWWWWWWWWW turning off jtwc for dowarn ',dtg
            


        #
        # nhc flag
        #
        if(		
            (bflgind == 'TD') or (bflgind == 'TS') or (bflgind == 'HU') or
            (bflgind == 'TY') or (bflgind == 'ST') and (bflgind != 'EX')
            ):
            btvflgnhc[dtg]=1

        else:
            btvflgnhc[dtg]=0


        if(docarqchk and isnotcarq and btvflgnhc[dtg] != 0):
            btvflgnhc[dtg]=0
            ###print 'tttttttttttt nnnnnnnnn CCCCCCCCCCC turning off nhc for docarq ',dtg
            
        if(dowarnchk and isnotwarn and btvflgnhc[dtg] != 0):
            btvflgnhc[dtg]=0
            ###print 'tttttttttttt nnnnnnnnn WWWWWWWWWWW turning off nhc for dowarn ',dtg

            
        if(verb):
            (clat,clon,ilat,ilon,hemns,hemew)=Rlatlon2Clatlon(blat,blon)
            print 'bt     ',dtg,clat,clon,("%5.1f"%(bvmax)),("%4.2f"%(blf)),\
                  bflgtc,bflgind,bflgcq,bflgwn,\
                  ' vjtwc: ',("%2d"%(btvflgjtwc[dtg])),\
                  ' vnhc:',("%2d"%(btvflgnhc[dtg]))

        if(b1id == 'L' or b1id == 'E' or b1id == 'C'):
            btvf=btvflgnhc[dtg]
            btvflg=btvflgnhc
            ruleflg='NhcOps'+oruleaddopt
        else:
            btvf=btvflgjtwc[dtg]
            btvflg=btvflgjtwc
            ruleflg='JtwcOps'+oruleaddopt

        if(btvf == 1): edtg=dtg

        #
        # check for crossing the date line...
        #

        if(blon >= 0.0 and blon <= 60.0):
            blon=blon+360.0

        if(btvf == 1):
            if(blat < blatmin): blatmin=blat
            if(blat > blatmax): blatmax=blat
            if(blon < blonmin): blonmin=blon
            if(blon > blonmax): blonmax=blon

        if(blat < blatminall): blatminall=blat
        if(blat > blatmaxall): blatmaxall=blat
        if(blon < blonminall): blonminall=blon
        if(blon > blonmaxall): blonmaxall=blon

        btgcard="%s %6.1f %6.1f %3d %2d"%(dtg,blat,blon,int(bvmax),btvf)
        btgcards.append(btgcard)

        ######print btgcard

    try:
        edtgplot=mf.dtginc(edtg,24)
    except:
        print 'EEE do dtgs found in calc of last plot dtg; return None ...'
        return(None)

    rclist=[taus,dtgs,btvflg,btgcards,edtgplot,blatmin,blatmax,blonmin,blonmax,ruleflg,
            bttime2carq,bttime2warn,bttime2end,blatminall,blatmaxall,blonminall,blonmaxall]

    return(rclist)
    

#---------------------------------------------------------------------
#
# from g.tc.gs
#
#---------------------------------------------------------------------

def SetBlatLonBoundsTcPlot(b1id,blatmin,blatmax,blonmin,blonmax,docalc=1):

    b1id=b1id.lower()

    dltln=5.0
    
    dlatbase=5.0
    dlonbase=10.0
    
    ltmn=blatmin
    ltmx=blatmax
    lnmn=blonmin
    lnmx=blonmax

    ltmxtl=60
    ltmntl=-60

    lttol=5.0
    lntol=5.0

    lttol=10.0
    lntol=13.5

    lttol=8.5
    lntol=11.5

    lnadd=0
    ltadd=0
    if(lntol < dlonbase):
        lnadd=1
    if(lttol < dlatbase):
        ltadd=1

        
    lnint=(int(lntol/dlonbase)+lnadd)*(int(dlonbase))
    ltint=(int(lttol/dlatbase)+ltadd)*(int(dlatbase))

    if(docalc == 0):
        return(lnmn,lnmx,ltmn,ltmx,lnint,ltint)


    ltdist=blatmax-blatmin

    if(b1id == 's' and ltdist < 5.0):
        lttol=11.0
        lntol=lttol*1.33
        lnint=10
        ltint=10


    ltmn=int(ltmn)
    ltmx=int(ltmx)
    lnmn=int(lnmn)
    lnmx=int(lnmx)

    if(ltmn < 0 and ltmx > 0):
        ltmn=mf.nint(ltmn/lttol)-1
        ltmx=mf.nint(ltmx/lttol)-1
    else:
        ltmn=mf.nint(ltmn/lttol)
        ltmx=mf.nint(ltmx/lttol)

    lnmn=mf.nint(lnmn/lttol)
    lnmx=mf.nint(lnmx/lttol)

    
    ltmn=ltmn*lttol-lttol
    ltmx=ltmx*lttol+lttol

    lnmn=lnmn*lttol-lntol
    lnmx=lnmx*lttol+lntol

    aspect=(ltmx-ltmn)/(lnmx-lnmn)

    maxiter=10
    iter=1
    while(aspect < 0.5 and iter <= maxiter):
        
        ltmx=ltmx+lttol
        ltmn=ltmn-lttol
            
        aspect=(ltmx-ltmn)/(lnmx-lnmn)
        iter=iter+1

    
    iter=1
    while(aspect > 0.9 and iter <= maxiter):
        lnmx=lnmx+lntol
        lnmn=lnmn-lntol
        aspect=(ltmx-ltmn)/(lnmx-lnmn)
        iter=iter+1


    ltmn=mf.nint(ltmn/dltln)*dltln
    ltmx=mf.nint(ltmx/dltln)*dltln

    lnmn=mf.nint(lnmn/dltln)*dltln
    lnmx=mf.nint(lnmx/dltln)*dltln

    #
    # bias to se corner if nhem
    #
    if(b1id == 's' or b1id == 'p'):
        ltmx=ltmx+dltln*0.0
        lnmn=lnmn-dltln*0.0
    else:
        ltmx=ltmx+dltln
        lnmn=lnmn-dltln

    if(iter >= maxiter):
        print 'EEEEE in TCw2.SetBlat ... ',iter,' > maxiter ',maxiter
        sys.exit()


    return(lnmn,lnmx,ltmn,ltmx,lnint,ltint)

#gggggggggggggggggggggggggggggggggggggggggggggggggg
#
# gsf for track plotter...
#
#gggggggggggggggggggggggggggggggggggggggggggggggggg

def TcTrkGsf(year,stmid,vdmodel,
             imodel,phr,dtgs,
             blatmin,blatmax,
             blonmin,blonmax,
             blatminall,blatmaxall,
             blonminall,blonmaxall,
             ruleflg,verb=0):

    gsfcards=[]
    G=gsfcards.append

    G("function tctrkp()")
    
    b1id=stmid[2:3]
    b3id=Basin1toBasin3[b1id]
    
    tcnames=GetTCnamesHash(year)
    tcstats=GetTCstatsHash(year)
    
    try:
        tstmname=tcnames[year,stmid]
    except:
        tstmname='NoName'

    try:
        tstmstat=tcstats[year,stmid]
        tstmtype=tstmstat[0]
    except:
        tstmtype='TC'


    mname=atcf.ModelNametoModelDesc[imodel]
    bdtg=dtgs[0]
    edtg=dtgs[len(dtgs)-1]
    
    mtitle1="_mtitle1='`4%s`0 :: %s Forecasts for `4%s %s `0%s `2%s'"%(vdmodel,mname,year,stmid,tstmtype,tstmname)
    if(phr == None):
        mphr="Raw Output"
    else:
        mphr="`4%02d`0 :: BIAS-CORR 0-24 h motion & EXTRAP forward %d h"%(phr,phr) 
    mtitle2="_mtitle2='%s -- period %s to %s'"%(mphr,bdtg,edtg)

    if(verb):
        print '    mname: ',mname
        print '  mtitle1: ',mtitle1
        print '  mtitle2: ',mtitle2

    (lnmn,lnmx,ltmn,ltmx,lnint,ltint)=SetBlatLonBoundsTcPlot(b3id,blatmin,blatmax,blonmin,blonmax)
    
    (lnmnall,lnmxall,ltmnall,ltmxall,lnintall,ltintall)=\
         SetBlatLonBoundsTcPlot(b3id,blatminall,blatmaxall,blonminall,blonmaxall)


    G("%s"%(mtitle1))
    G("%s"%(mtitle2))
    
    G("_lnmn=%5.1f"%(lnmn))
    G("_lnmx=%-5.1f"%(lnmx))
    G("_ltmn=%-5.1f"%(ltmn))
    G("_ltmx=%-5.1f"%(ltmx))
    G("_lnint=%-5.1f"%(lnint))
    G("_ltint=%-5.1f"%(lnint))
    
    G("_lnmnall=%5.1f"%(lnmnall))
    G("_lnmxall=%-5.1f"%(lnmxall))
    G("_ltmnall=%-5.1f"%(ltmnall))
    G("_ltmxall=%-5.1f"%(ltmxall))
    G("_lnintall=%-5.1f"%(lnintall))
    G("_ltintall=%-5.1f"%(lnintall))
    
    G("_ruleflg='%s'"%(ruleflg))
    G("return")

    gsfall=''
    for gsf in gsfcards:
        gsfall=gsfall+gsf+'\n'

    return(gsfall)

#vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
#
# main vdeck analysis 
#
#vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

def mercat_theta(x0,x1,y0,y1):
    
    dx=x1-x0
    dy=y1-y0

    if (dx == 0.0):
        if(dy >= 0.0): dthd=0.0
        if(dy < 0.0): dthd=pi 
    else:
        slope=dy/dx
        if (abs(slope) < 1e-10):
            if(dx > 0.0): dthd=pi2 
            if(dx < 0.0): dthd=3*pi/2.0
        else:
            dthd=atan2(dy,dx)
            if(dthd < 0.0):
                dthd=dthd + 2.0*pi
                
    dthd=dthd*rad2deg
    return(dthd)


def ConsistAnal(rc0,rc1,i,tau,dtgs,dtrun=6.0):
    
    fe0=rc0[0]
    fe1=rc1[0]
    dfe=fabs(fe1-fe0)

    #
    # mean fe of conseqitive runs and change in error direction (in rose)
    #
    febar=(fe0+fe1)*0.5
                
    thfe0=rc0[1]
    thfe1=rc1[1]
    dthfe=fabs(thfe1-thfe0)
    if(dthfe > 180.0): dthfe=360.0-dthfe
    
    #
    # length of forecast and angle change
    #
    gc0=rc0[4]
    gc1=rc1[4]
    dgc=fabs(gc1-gc0)


    #
    # angle between bt and fc at the forecast time
    #
                    
    thgc0=rc0[5]
    thgc1=rc1[5]
    xgc0=rc0[6]
    xgc1=rc1[6]
    
    dxgc=xgc1-xgc0
    ygc0=rc0[7]
    ygc1=rc1[7]
    dygc=ygc1-ygc0

    bgc0=rc0[8]
    bgc1=rc1[8]
    dbgc=fabs(bgc1-bgc0)
    xbgc0=rc0[10]
    xbgc1=rc1[10]
    dxbgc=xbgc1-xbgc0
    ybgc0=rc0[11]
    ybgc1=rc1[11]
    dybgc=ybgc1-ybgc0

    #
    # angle change between runs of:
    #
    #   bt and fc (dthgc)
    #   fc from tau=0 (dthdgc)
    #   bt from tau=0 (dthdbgc)
    #
    
    dthgc=fabs(thgc1-thgc0)
    if(dthgc > 180.0): dthgc=360.0-dthgc

    dthdgc=mercat_theta(xgc0,xgc1,ygc0,ygc1)
    if(dthdgc > 180.0): dthdgc=360.0-dthdgc

    dthdbgc=mercat_theta(xbgc0,xbgc1,ybgc0,ybgc1)
    if(dthdbgc > 180.0): dthdbgc=360.0-dthdbgc

    #
    # change in distance and angle between runs for fc and bt  
    #

    flat0=rc0[12]
    flon0=rc0[13]
    flat1=rc1[12]
    flon1=rc1[13]

    blat0=rc0[14]
    blon0=rc0[15]
    blat1=rc1[14]
    blon1=rc1[15]
    
    (fcdx,fcdy,fctheta)=gc_theta(flat0,flon0,flat1,flon1)
    fcgc=gc_dist(flat0,flon0,flat1,flon1)
    if(fctheta > 180.0): fctheta=360.0-fctheta

    (btdx,btdy,bttheta)=gc_theta(blat0,blon0,blat1,blon1)
    btgc=gc_dist(blat0,blon0,blat1,blon1)
    #if(bttheta > 180.0): bttheta=360.0-bttheta
    
    #
    # change in course between runs, bt and fc
    #
    
    fccrs0=rc0[16]
    fcspd0=rc0[17]
    btcrs0=rc0[18]
    btspd0=rc0[19]
    
    fccrs1=rc1[16]
    fcspd1=rc1[17]
    btcrs1=rc1[18]
    btspd1=rc1[19]

    dtspd=12.0
    dbtdst=(btspd1-btspd0)*dtspd
    dfcdst=(fcspd1-fcspd0)*dtspd
    
    dbtcrs=fabs(btcrs1-btcrs0)
    if(dbtcrs > 180.0): dbtcrs=360.0-dbtcrs
    dbtcrs=btcrs1-btcrs0
    if(dbtcrs > 180.0): dbtcrs=360.0-dbtcrs
    if(dbtcrs < -180.0): dbtcrs=360.0+dbtcrs

    dfccrs=fabs(fccrs1-fccrs0)
    if(dfccrs > 180.0): dfccrs=360.0-dfccrs
    dfccrs=fccrs1-fccrs0
    if(dfccrs > 180.0): dfccrs=360.0-dfccrs
    if(dfccrs < -180.0): dfccrs=360.0+dfccrs


    card="yyy111: i: %2d t: %03d %s dfe: %4.0f %4.0f %4.0f"%(i,tau,dtgs[i],fe0,fe1,dfe)
    card="%s thfes: %4.0f %4.0f %4.0f"%(card,thfe0,thfe1,dthfe)
    card="%s gcs: %4.0f %4.0f %4.0f"%(card,gc0,gc1,dgc)
    card="%s thgcs: %4.0f %4.0f %4.0f"%(card,dxgc,dygc,dthdgc)
    card="%s bgcs: %4.0f %4.0f %4.0f"%(card,dxbgc,dybgc,dthdbgc)
    #print card

    pref='yyy111:'
    if(dtrun == 12.0):
        pref='yyy222:'
    elif(dtrun == 18.0):
        pref='yyy333:'
    card1="%s i: %2d t: %03d %s fe: %4.0f febar: %4.0f"%(pref,i,tau,dtgs[i],fe0,febar)
    card1="%s dfe: %4.0f %4.0f"%(card1,dfe,dthfe)
    #ard1="%s thfes: %4.0f"%(card1)
    #card1="%s   dgc: %4.0f %4.0f"%(card1,dgc,dthdgc)
    #card1="%s  dbgc: %4.0f %4.0f"%(card1,dbgc,dthdbgc)
    card1="%s  fcgc: %5.0f %4.0f"%(card1,fcgc,fctheta)
    card1="%s  btgc: %4.0f %4.0f"%(card1,btgc,bttheta)
    card1="%s  btcs: %4.0f %4.0f"%(card1,dbtdst,dbtcrs)
    card1="%s  fccs: %4.0f %4.0f"%(card1,dfcdst,dfccrs)
    #print card1

    return
                

def GetVdeckcFcs(stmid,model,verb=0,dotimer=0):

    from time import time as timer
    import cPickle as pickle

    (stm3id,year)=stmid.split('.')
    
    vddir=BaseDirDataTc+"/vdeck/%s/%s"%(year,model)

    cfcspypofile="cfcs.%s.%s.pyp"%(stmid,model)
    cfcspypopath="%s/%s"%(vddir,cfcspypofile)
    #
    # run if not available
    #
    if(not(os.path.exists(cfcspypopath))):
        if(dotimer): stime=timer()
        print 'DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD running dqc for ',stmid,model
        cmd="%s/w2.tc.vdeck.dqc.py %s %s"%(BaseDirPrcTcDat,stmid,model)
        mf.runcmd(cmd,'')

    if(os.path.exists(cfcspypopath)):

        if(dotimer): stime=timer()
        PC=open(cfcspypopath)
        try:
            (dtgs,cfcs)=pickle.load(PC)
            if(dotimer): mf.Timer('load fcs pickle',stime)
            return(dtgs,cfcs)
        except:
            return(None,None)

    else:
        if(verb): print 'WWW TCw2.py:  no vdecks cfcs for: ',stmid,' model: ',model
        return(None,None)
        
def GetVdeckFcs(stmid,model,verb=0,dotimer=0):

    from time import time as timer
    import cPickle as pickle

    (stm3id,year)=stmid.split('.')
    
    vddir=BaseDirDataTc+"/vdeck/%s/%s"%(year,model)

    fcspypofile="fcs.%s.%s.pyp"%(stmid,model)
    fcspypopath="%s/%s"%(vddir,fcspypofile)

    if(os.path.exists(fcspypopath)):

        if(dotimer): stime=timer()
        PF=open(fcspypopath)
        (dtgs,fcs)=pickle.load(PF)
        if(dotimer): mf.Timer('load fcs pickle',stime)
        return(dtgs,fcs)

    else:
        if(verb): print 'WWW TCw2.py:  no vdecks fcs for: ',stmid,' model: ',model
        return(None,None)
        
def GetMdeckBts(stmid,dofilt9x=1,verb=0):

##    mdcards=findtc(stmid,dofilt9x)

    mdcards=findMdeckTC(stmid,do9x=dofilt9x)
    if(len(mdcards) == 0):
        return(None,None)
    else:
        dtgs=mdcards.keys()
        dtgs.sort()
        bts=ParseMdeck2Btcs(dtgs,mdcards)
        return(dtgs,bts)
        


def VdeckVitals(stmid,modopt,tdoopt,ruleopt,phr,verb):

    year=stmid.split('.')[1]
    stm3id=stmid.split('.')[0]
    b1id=stm3id[2:3]
    b3id=Basin1toBasin3[b1id]

    if(ruleopt == None):
        oruleopt='ops'
    else:
        oruleopt=ruleopt

    printall=1

    tt=modopt.split('.')
    if(len(tt) == 2):
        imodels=tt
        nmodels=2
    elif(len(tt) == 1):
        imodels=[modopt]
        nmodels=1
    else:
        print 'EEEE invalid modopt: ',modopt
        sys.exit()


    vddir=BaseDirDataTc+"/vdeck/%s"%(year)

    #
    # cycle through 1-2 models
    #

    filt0012=filt0618=0

    nmodel=1
    for imodel in imodels:

        vdmodel=imodel

        limod=len(imodel)
        cphr=imodel[limod-2:limod]

        if(cphr == '00' or cphr == '06' or cphr == '12'):
            phr=int(cphr)
            imodel=imodel[0:limod-2]
        else:
            phr=None

        if(verb): print 'mmmmmmmmmmm imodel,vdmodel,phr: ',imodel,vdmodel,phr

        if(atcf.DtauModel[imodel] == 12):
            
            if(phr == None and atcf.StartSynHourModel[imodel] == 6):
                filt0012=0
                filt0618=1
            elif(phr != None and int(phr) == 6 and atcf.StartSynHourModel[imodel] == 6):
                filt0012=1
                filt0618=0
            elif(phr != None and int(phr) == 0 and atcf.StartSynHourModel[imodel] == 6):
                filt0012=0
                filt0618=1
            elif(phr != None and int(phr) == 6):
                filt0012=0
                filt0618=1
            else:
                filt0012=1
                filt0618=0


        if(nmodel == 1):
            vdmodel1=vdmodel
            (idtgs,fcs1)=GetVdeckFcs(stmid,imodel)
            rclist=SetBtVdeck(stm3id,imodel,idtgs,fcs1,ruleopt,verb=verb)
        elif(nmodel == 2):
            vdmodel2=vdmodel
            (idtgs,fcs2)=GetVdeckFcs(stmid,imodel)
            rclist=SetBtVdeck(stm3id,imodel,idtgs,fcs2,ruleopt,verb=verb)

        taus=rclist[0]
        dtgs=rclist[1]
        btvflg=rclist[2]
        btgcards=rclist[3]
        edtgplot=rclist[4]
        blatmin=rclist[5]
        blatmax=rclist[6]
        blonmin=rclist[7]
        blonmax=rclist[8]
        ruleflg=rclist[9]
        bttime2carq=rclist[10]
        bttime2warn=rclist[11]
        bttime2end=rclist[12]
        blatminall=rclist[13]
        blatmaxall=rclist[14]
        blonminall=rclist[15]
        blonmaxall=rclist[16]

        gsf1=TcTrkGsf(year,stm3id,vdmodel,
                      imodel,phr,dtgs,
                      blatmin,blatmax,
                      blonmin,blonmax,
                      blatminall,blatmaxall,
                      blonminall,blonmaxall,
                      ruleflg)


        nmodel=nmodel+1

    if(nmodels == 1):
        fcs2=copy.deepcopy(fcs1)
        vdmodel2=vdmodel1



    btpycards=[]
    dfepycards=[]
    pycards=[]
    scards=[]

    #
    #
    #

    cntbt={}
    cntfc={}
    cnthit={}  
    cntmiss={}  
    cntmissfc={}  
    cntover={}  
    cntoverfc={}  


    def SimpleTauStat(stat,var,varname,tau):

        var2=var*var
        
        try:
            stat[varname,tau,'n']=stat[varname,tau,'n']+1
        except:
            stat[varname,tau,'n']=1

        try:
            stat[varname,tau,'sum']=stat[varname,tau,'sum']+var
        except:
            stat[varname,tau,'sum']=var

        try:
            stat[varname,tau,'abssum']=stat[varname,tau,'abssum']+math.fabs(var)
        except:
            stat[varname,tau,'abssum']=math.fabs(var)

        try:
            stat[varname,tau,'sum2']=stat[varname,tau,'sum2']+var2
        except:
            stat[varname,tau,'sum2']=var2
            


    def FinalizeStat(TauStats,ic):

        (vfe,
        vcte,vate,vctef,vatef,veweb,vnseb,
        vfve,vfveu,vfver,
        vbv,vfv)=ic

        try:
            mfe=TauStats[vfe,tau,'sum']/TauStats[vfe,tau,'n']
        except:
            mfe=-999.0

        try:
            mcte=TauStats[vcte,tau,'sum']/TauStats[vcte,tau,'n']
            mate=TauStats[vate,tau,'sum']/TauStats[vate,tau,'n']
        except:
            mcte=-999.0
            mate=-999.0

        try:
            mctef=TauStats[vctef,tau,'sum']/TauStats[vctef,tau,'n']
            matef=TauStats[vatef,tau,'sum']/TauStats[vatef,tau,'n']
        except:
            mctef=-999.0
            matef=-999.0

        try:
            meweb=TauStats[veweb,tau,'sum']/TauStats[veweb,tau,'n']
            mnseb=TauStats[vnseb,tau,'sum']/TauStats[vnseb,tau,'n']
        except:
            meweb=-999.0
            mnseb=-999.0

        try:
            mave=TauStats[vfve,tau,'abssum']/TauStats[vfve,tau,'n']
            mbve=TauStats[vfve,tau,'sum']/TauStats[vfve,tau,'n']
        except:
            mave=-999.0
            mbve=-999.0

        try:
            maveu=TauStats[vfveu,tau,'abssum']/TauStats[vfveu,tau,'n']
            mbveu=TauStats[vfveu,tau,'sum']/TauStats[vfveu,tau,'n']
        except:
            maveu=-999.0
            mbveu=-999.0

        try:
            maver=TauStats[vfver,tau,'abssum']/TauStats[vfver,tau,'n']
            mbver=TauStats[vfver,tau,'sum']/TauStats[vfver,tau,'n']
        except:
            maver=-999.0
            mbver=-999.0

        try:
            mbv=TauStats[vbv,tau,'abssum']/TauStats[vbv,tau,'n']
            mfv=TauStats[vfv,tau,'sum']/TauStats[vfv,tau,'n']
        except:
            mbv=-999.0
            mfv=-999.0


        rc=(mfe,mcte,mate,mctef,matef,meweb,mnseb,
            mave,mbve,maveu,mbveu,maver,mbver,
            mbv,mfv)

        return(rc)




    TauStats={}

    for tau in taus:

        cntbt[tau]=0
        cntfc[tau]=0
        cnthit[tau]=0
        cntmiss[tau]=0
        cntover[tau]=0
        cntmissfc[tau]=0
        cntoverfc[tau]=0


    #
    # run-to-run forecast consistency check
    #

    mod1consist={}
    
    for dtg in dtgs:

        if(btvflg[dtg] == 1):

            i=0
            for tau in taus:

                try:
                    [vdtg,flat1,flon1,fvmax,flf,ffe,fcte,fate,ffcte,ffate,fewe,fnse,r34quad,r50quad]=fcs1[dtg,tau]
                    [blat1,blon1,bvmax1,blf1]=fcs1[dtg,tau,'bt']

                    [vdtg2,flat2,flon2,fvmax2,flf2,ffe2,fcte2,fate2,ffcte2,ffate2,fewe2,fnse2,r34quad2,r50quad2]=fcs2[dtg,tau]
                    [bvmax2,fvmax2,fve2,fveu2,fver2]=fcs2[dtg,tau,'vmax']
                    [blat2,blon2,bvmax2,blf2]=fcs1[dtg,tau,'bt']

                except:
                    if(verb): print 'fail1111 ',tau
                    mod1consist[dtg,tau]=[-999.0]
                    i=i+1
                    continue

                if(tau == 0):
                    blat0=blat1
                    blon0=blon1
                    flat0=flat1
                    flon0=flon1
                    blat1m1=blat1
                    blon1m1=blon1
                    flat1m1=flat1
                    flon1m1=flon1
                    taum1=0
                    dtau=0

                
                elif(i> 0):

                    taum1=taus[i-1]
                    dtau=tau-taum1

                    try:
                        [vdtg,flat1m1,flon1m1,fvmaxm1,flfm1,ffem1,fctem1,fatem1,ffctem1,ffatem1,fewem1,fnsem1,r34quad1,r50quad1]=fcs1[dtg,taum1]
                        [blat1m1,blon1m1,bvmax1m1,blf1m1]=fcs1[dtg,taum1,'bt']
                    except:
                        #
                        # go back to early tau for ofc (no 60, 84, ...) 
                        #
                        taum1=taus[i-2]
                        dtau=tau-taum1
                        try:
                            [vdtg,flat1m1,flon1m1,fvmaxm1,flfm1,ffem1,fctem1,fatem1,ffctem1,ffatem1,fewem1,fnsem1,r34quad1,r50quad1]=fcs1[dtg,taum1]
                            [blat1m1,blon1m1,bvmax1m1,blf1m1]=fcs1[dtg,taum1,'bt']
                        except:
                            print 'EEEEEEEEE no tau-2 fc ........',dtg,tau,i,taum1,taus
                            #sys.exit()



                if( blat1 > -90.0 and blat1 < 88.0 and flat1 > -90.0 and flat1 < 88.0 ):

                    #print 
                    #print '0000000000000bbbbbb %s tau %03d'%(dtg,tau),blat0,blon0
                    #print '1111111111111bbbbbb %s tau %03d'%(dtg,tau),blat1,blon1
                    #print 'm1m1m1m1m1m1mbbbbbb %s tau %03d'%(dtg,tau),blat1m1,blon1m1
                    #print 
                    #print '0000000000000ffffff %s tau %03d'%(dtg,tau),flat0,flon0
                    #print '1111111111111ffffff %s tau %03d'%(dtg,tau),flat1,flon1
                    #print 'm1m1m1m1m1m1mffffff %s tau %03d'%(dtg,tau),flat1m1,flon1m1

                    if(dtau == 0):
                        (fccourse,fcspeed,fciumotion,fcivmotion)=(0.0,0.0,0.0,0.0)
                        (btcourse,btspeed,btiumotion,btivmotion)=(0.0,0.0,0.0,0.0)
                    else:
                        (fccourse,fcspeed,fciumotion,fcivmotion)=rumhdsp(flat1m1,flon1m1,flat1,flon1,dtau)
                        (btcourse,btspeed,btiumotion,btivmotion)=rumhdsp(blat1m1,blon1m1,blat1,blon1,dtau)

                    #print 'bbbbbbbbbbbbbffffff %s tau %03d'%(dtg,tau),btcourse,btspeed
                    #print 'rrrrrrrrrrrrrffffff %s tau %03d'%(dtg,tau),fccourse,fcspeed
                    
                    fe=gc_dist(blat1,blon1,flat1,flon1)
                    gc0=gc_dist(blat0,blon0,flat1,flon1)
                    bgc0=gc_dist(blat0,blon0,blat1,blon1)

                    (difx,dify,theta)=gc_theta(blat1,blon1,flat1,flon1)
                    (difx0,dify0,theta0)=gc_theta(blat0,blon0,flat1,flon1)
                    (bdifx0,bdify0,btheta0)=gc_theta(blat0,blon0,blat1,blon1)
                    
                    #print '1111111111111 tau %03d'%(tau),blat0,blon0,blat1,blon1,flat1,flon1
                    #print '111 tau %03d %s fe: %6.1f Th: %5.1f x,y: %5.0f %5.0f'%(tau,dtg,fe,theta,difx,dify)
                    #print '111 tau %03d %s gc0: %6.1f Th: %5.1f x,y: %5.0f %5.0f'%(tau,dtg,gc0,theta0,difx0,dify0)
                    #print '111 tau %03d %s gc0: %6.1f Th: %5.1f x,y: %5.0f %5.0f'%(tau,dtg,bgc0,btheta0,bdifx0,bdify0)
                    
                    mod1consist[dtg,tau]=[fe,theta,difx,dify,gc0,theta0,difx0,dify0,bgc0,btheta0,bdifx0,bdify0,
                                          flat1,flon1,blat1,blon1,fccourse,fcspeed,btcourse,btspeed]
                else:
                    mod1consist[dtg,tau]=[-888.0]

                i=i+1


        else:
            
            for tau in taus:
                mod1consist[dtg,tau]=[-789.0]

            


    for tau in taus:

        if(verb): print
        ndtgs=len(dtgs)
        for i in range(0,ndtgs):

            rcp0=mod1consist[dtgs[i],tau]
            if(i<ndtgs-1):
                try:
                    rcp1=mod1consist[dtgs[i+1],tau]
                except:
                    rcp1=rcp0
            else:
                rcp1=rcp0
                
            if(i<ndtgs-2):
                try:
                    rcp2=mod1consist[dtgs[i+2],tau]
                except:
                    rcp2=rcp0
            else:
                rcp2=rcp0
                
            if(i<ndtgs-3):
                try:
                    rcp3=mod1consist[dtgs[i+3],tau]
                except:
                    rcp3=rcp0
            else:
                rcp3=rcp0
                
            fep0=rcp0[0]
            fep1=rcp1[0]
            fep2=rcp2[0]
            fep3=rcp3[0]

            if(fep0 >= 0.0 and fep1 >= 0.0):
                ConsistAnal(rcp0,rcp1,i,tau,dtgs,dtrun=6.0)
            elif(fep0 >= 0.0 and fep2 >= 0.0):
                ConsistAnal(rcp0,rcp2,i,tau,dtgs,dtrun=12.0)
                #print "yyy222: i: %2d t: %03d %s fes: %5.0f %5.0f"%(i,tau,dtgs[i],fep0,fep2)
            elif(fep0 >= 0.0 and fep3 >= 0.0):
                ConsistAnal(rcp0,rcp3,i,tau,dtgs,dtrun=18.0)
                #print "yyy222: i: %2d t: %03d %s fes: %5.0f %5.0f"%(i,tau,dtgs[i],fep0,fep2)
            else:
                continue
                #print "nnn: i: %2d t: %03d %s"%(i,tau,dtgs[i])



    tdos=[]
    fcgcards=[]
    for dtg in dtgs:

        hh=dtg[8:10]

        if(filt0012 and (hh == '06' or hh == '18')):
            continue
        elif(filt0618 and (hh == '00' or hh == '12')):
            continue

        if(btvflg[dtg] == 1):

            fcgcard="%s %s :: "%(imodel,dtg)

            ihitbt00=0
            ihitfc00=0

            for tau in taus:

                if(tau == 0): ihitbt00=1

                try:
                    [vdtg,flat,flon,fvmax,flf,ffe,fcte,fate,fctef,fatef,feweb,fnseb,r34quad,r50quad]=fcs1[dtg,tau]
                    [bvmax,fvmax,fve,fveu,fver]=fcs1[dtg,tau,'vmax']
                    tdo=fcs1[dtg,tau,'tdo']

                    [vdtg2,flat2,flon2,fvmax2,flf2,ffe2,fcte2,fate2,fctef2,fatef2,feweb2,fnseb2,r34quad2,r50quad2]=fcs2[dtg,tau]
                    [bvmax2,fvmax2,fve2,fveu2,fver2]=fcs2[dtg,tau,'vmax']
                    tdo2=fcs2[dtg,tau,'tdo']
                except:
                    if(verb): print 'fail2222',tau
                    continue

                tdos.append(tdo)

                if(tdoopt != None and tdo != tdoopt): continue 

                ihitbt=0
                try:
                    if(btvflg[vdtg] == 1):
                        ihitbt=1
                        cntbt[tau]=cntbt[tau]+1
                except:
                    continue

                #
                # forecast made
                #
                fctest1=( (flat > -90.0 and flat < 88.0) or (flat == 97.9 and fvmax > 0.0) )
                fctest2=( (flat2 > -90.0 and flat2 < 88.0) or (flat2 == 97.9 and fvmax2 > 0.0) )
                
                fctest=( fctest1 and fctest2 )

                if(fctest):
                    try:
                        if(btvflg[vdtg] == 1):
                            ihitfc=1
                            cntfc[tau]=cntfc[tau]+1
                            if(tau == 0): ihitfc00=1
                    except:
                        ihitfc=-999

                #
                # no forecast ........
                #
                else:
                    try:
                        if(btvflg[vdtg] == 1):
                            ihitfc=-1
                        else:
                            ihitfc=0
                    except:
                        continue


                if(verb): print 'fffffffff ',"%03d %2d %2d %2d %2d"%(tau,ihitbt,ihitfc,ihitbt00,ihitfc00),dtg,vdtg,flat,tdo,fctest


                if(ihitbt == 1 and ihitfc == 1): cnthit[tau]=cnthit[tau]+1
                if(ihitbt == 1 and ihitfc == -1):
                    cntmiss[tau]=cntmiss[tau]+1
                    if(ihitfc00 == 1): cntmissfc[tau]=cntmissfc[tau]+1

                if(ihitbt == 0 and ihitfc == 1):
                    cntover[tau]=cntover[tau]+1
                    if(ihitfc00 ==1): cntoverfc[tau]=cntoverfc[tau]+1


                if(vdtg <= edtgplot and fctest):

                    offe=-999
#                    try:
                    if(btvflg[vdtg] == 1):
                        
                        offe=ffe

                        SimpleTauStat(TauStats,ffe,'ffe',tau)
                        SimpleTauStat(TauStats,fcte,'fcte',tau)
                        SimpleTauStat(TauStats,fate,'fate',tau)
                        SimpleTauStat(TauStats,fctef,'fctef',tau)
                        SimpleTauStat(TauStats,fatef,'fatef',tau)
                        SimpleTauStat(TauStats,feweb,'feweb',tau)
                        SimpleTauStat(TauStats,fnseb,'fnseb',tau)
                       
                        if(fve != -999.0):
                            SimpleTauStat(TauStats,fve,'fve',tau)
                            SimpleTauStat(TauStats,bvmax,'bvm',tau)
                            SimpleTauStat(TauStats,fvmax,'fvm',tau)

                        if(fveu != -999.0):
                            SimpleTauStat(TauStats,fveu,'fveu',tau)

                        if(fver != -999.0):
                            SimpleTauStat(TauStats,fver,'fver',tau)

#
# 2nd aid
#
                        SimpleTauStat(TauStats,ffe2,'ffe2',tau)
                        SimpleTauStat(TauStats,fcte2,'fcte2',tau)
                        SimpleTauStat(TauStats,fate2,'fate2',tau)
                        SimpleTauStat(TauStats,fctef2,'fctef2',tau)
                        SimpleTauStat(TauStats,fatef2,'fatef2',tau)
                        SimpleTauStat(TauStats,feweb2,'feweb2',tau)
                        SimpleTauStat(TauStats,fnseb2,'fnseb2',tau)
                       
                        if(fve2 != -999.0):
                            SimpleTauStat(TauStats,fve2,'fve2',tau)
                            SimpleTauStat(TauStats,bvmax2,'bvm2',tau)
                            SimpleTauStat(TauStats,fvmax2,'fvm2',tau)

                        if(fveu != -999.0):
                            SimpleTauStat(TauStats,fveu2,'fveu2',tau)

                        if(fver != -999.0):
                            SimpleTauStat(TauStats,fver2,'fver2',tau)



                        if(tau == 36 or tau == 72):
                            dfe=ffe2-ffe
                            if(tau == 36): fenorm=75.0
                            if(tau == 72): fenorm=150.0

                            if(ffe2 == 0.0):
                                dfep=-999.9
                                dfeppacflt=-999.9
                            else:
                                dfep=(dfe/ffe2)*100.0
                                dfeppacflt=(dfe/fenorm)*100.0


                            dfepycard="""DfeVitals['%s','%s','%s','%s',%d] = [%6.1f,%6.1f,%6.1f,%4.0f,%4.0f,'%s']"""%\
                                      (stmid,vdtg,modopt,oruleopt,tau,ffe,ffe2,dfe,dfep,dfeppacflt,tdo)
                            if(verb): print 'dfe: ',dfepycard
                            dfepycards.append(dfepycard)


#                    except:
#                        if(verb): print 'fail2: ',tau,vdtg
#                        continue

                    #print 'fcs1 ',tau,dtg,vdtg,flat,offe,flf
                    fcgcard="%s %03d %5.1f %5.1f %3d %4d :"%(fcgcard,tau,flat,flon,int(fvmax),int(offe))

                #except:
                #    print 'NNNNNNNNNNNNNN' 
                #    continue

            fcgcards.append(fcgcard)


    for tau in taus:

#
# 11111111111 aid 1
#

        vfe='ffe'; vcte='fcte'; vate='fate'; vctef='fctef'; vatef='fatef'
        veweb='feweb'; vnseb='fnseb'; vfve='fve'; vfveu='fveu'; vfver='fver'; vbv='bvm'; vfv='fvm'

        ic1=(vfe,
            vcte,vate,vctef,vatef,veweb,vnseb,
            vfve,vfveu,vfver,
            vbv,vfv)

        (mfe1,
         mcte1,mate1,mctef1,matef1,meweb1,mnseb1,
         mave1,mbve1,maveu1,mbveu1,maver1,mbver1,
         mbv1,mfv1)=FinalizeStat(TauStats,ic1)

#
# 2222222222 aid 2
#

        vfe2='ffe2'; vcte2='fcte2'; vate2='fate2'; vctef2='fctef2'; vatef2='fatef2'
        veweb2='feweb2'; vnseb2='fnseb2'; vfve2='fve2'; vfveu2='fveu2'; vfver2='fver2'; vbv2='bvm2'; vfv2='fvm2'
                      
        ic2=(vfe2,
            vcte2,vate2,vctef2,vatef2,veweb2,vnseb2,
            vfve2,vfveu2,vfver2,
            vbv2,vfv2)
        
        (mfe2,
         mcte2,mate2,mctef2,matef2,meweb2,mnseb2,
         mave2,mbve2,maveu2,mbveu2,maver2,mbver2,
         mbv2,mfv2)=FinalizeStat(TauStats,ic2)


        if(verb and cntfc > 0):
            print
            print "      cntbt : %03d %3d"%(tau,cntbt[tau])
            print "      cntfc : %03d %3d"%(tau,cntfc[tau])
            print "     cnthit : %03d %3d"%(tau,cnthit[tau])
            print "    cntmiss : %03d %3d"%(tau,cntmiss[tau])
            print "    cntover : %03d %3d"%(tau,cntover[tau])
            print "  cntmissfc : %03d %3d"%(tau,cntmissfc[tau])
            print "  cntoverfc : %03d %3d"%(tau,cntoverfc[tau])
            print "       mfe1 : %03d %4.0f %2d"%(tau,mfe1,mfe1)
            print "      mcte1 : %03d %4.0f %2d"%(tau,mcte1,mcte1)
            print "      mate1 : %03d %4.0f %2d"%(tau,mate1,mate1)

            print "      mave1 : %03d %4.0f %2d"%(tau,mave1,mave1)
            print "      mbve1 : %03d %4.0f %2d"%(tau,mbve1,mbve1)
            print "     maveu1 : %03d %4.0f %2d"%(tau,maveu1,maveu1)
            print "     mbveu1 : %03d %4.0f %2d"%(tau,mbveu1,mbveu1)
            print "     maver1 : %03d %4.0f %2d"%(tau,maver1,maver1)
            print "     mbver1 : %03d %4.0f %2d"%(tau,mbver1,mbver1)
            print "       mbv1 : %03d %4.0f %2d"%(tau,mbv1,mbv1)
            print "       mfv1 : %03d %4.0f %2d"%(tau,mfv1,mfv1)


        scard1="%03d C %2d %2d %2d %2d fc %2d %2d"%(tau,cntbt[tau],cntfc[tau],
                                              cntmiss[tau],cntover[tau],
                                              cntmissfc[tau],cntoverfc[tau]
                                              )

        pycard1="C %2d %2d %2d %2d fc %2d %2d"%(cntbt[tau],cntfc[tau],
                                              cntmiss[tau],cntover[tau],
                                              cntmissfc[tau],cntoverfc[tau]
                                              )
        pycard1=pycard1

        ovdmodel1=vdmodel1
        if(tdoopt != None):
            ovdmodel1=vdmodel1+tdoopt

        ovdmodel2=vdmodel2
        if(tdoopt != None):
            ovdmodel2=vdmodel2+tdoopt

        def scardout(ovdmodel1,
                     mfe1,mcte1,mate1,
                     mctef1,matef1,
                     meweb1,mnseb1,
                     mbv1,mfv1,mave1,mbve1,
                     maveu1,mbveu1,maver1,mbver1):
        

            scard="%9s FE %4.0f  CT/Ab: %4.0f %4.0f CT/Av: %4.0f %4.0f CT/AeN: %4.0f %4.0f"%\
                    (ovdmodel1,mfe1,mcte1,mate1,
                     mctef1,matef1,
                     meweb1,mnseb1)

            scard="%s VmB/Fc: %3.0f %3.0f VeCA/b: %3.0f %3.0f"%\
                    (scard,mbv1,mfv1,mave1,mbve1)
            
            scard="%s  VeUA/b: %5.1f %5.1f VeRA/b: %5.1f %5.1f"%\
                    (scard,maveu1,mbveu1,maver1,mbver1)

            return(scard)



        scard2=scardout(ovdmodel1,
                        mfe1,mcte1,mate1,
                        mctef1,matef1,
                        meweb1,mnseb1,
                        mbv1,mfv1,mave1,mbve1,
                        maveu1,mbveu1,maver1,mbver1)
        

        scard3=scardout(ovdmodel2,
                        mfe2,mcte2,mate2,
                        mctef2,matef2,
                        meweb2,mnseb2,
                        mbv2,mfv2,mave2,mbve2,
                        maveu2,mbveu2,maver2,mbver2)
        

        scard="%s %s %s"%(scard1,scard2,scard3)




        if(mfe1 != -999.0 or printall):
            scards.append(scard)


        if(tdoopt != None):
            otdoopt=tdoopt
        else:
            otdoopt='ALL'

        pycard="""Vitals['%s','%s','%s','%s',%d] = [
    '%s',
    '%s',
    '%s',
    ]"""%(stmid,modopt,ruleflg,otdoopt,tau,
          pycard1,scard2,scard3)

        pycards.append(pycard)

    #
    # bt vitals
    #
    btpycard="""
BtVitals['%s','%s'] = [%5.1f,%5.1f,%5.1f]"""%\
    (stmid,modopt,
     bttime2carq,bttime2warn,bttime2end)

    btpycards.append(btpycard)

    if(tdoopt != None and len(tdos) > 0):
        tdos=mf.uniq(tdos)
        #for tdo in tdos:
        #    print 'ttt ',tdo
    else:
        tdos=None

    if(verb):
        for btgcard in btgcards:
            print 'bbb ',btgcard

        print
        for fcgcard in fcgcards:
            print 'fff ',fcgcard

        print
        for pycard in pycards:
            print 'ppp ',pycard

        print
        for scard in scards:
            print 'sss ',scard



    return(btgcards,fcgcards,pycards,scards,gsf1,dfepycards,btpycards)

#----------------------------------------------------------------------
#
#  define the runs of vitals
#
#----------------------------------------------------------------------

def SetVdeckVitalsOpts(stmopt,modopt,tdoopt,dfeonly,vdms=VdeckModels,dohomo=0):

    mm=modopt.split('.')
    if(len(mm) == 2):
        mod1=mm[0]
        mod2=mm[1]
    else:
        mod1=None
        mod2=None
    
    if(modopt == 'all'):
        votype=1
    elif(modopt == 'ALL'):
        votype=1
    elif(modopt == 'top5'):
        votype=1
    elif(modopt == 'all0'):
        votype=0
    elif(modopt == 'cyclemodels'):
        votype=3
    elif(not(dohomo)):
        votype=-1
        vdms=[modopt]
    elif(dohomo):
        votype=-2
    else:
        votype=2

    if(mod1 == None and mod2 == None and votype == -1):
        print 'EEEE to do single model use -m all.MMM modopt: ',modopt,' votype: ',votype
        sys.exit()
    

    if(len(mm) == 2 and mod1 == 'all'):
        vdmsa=VdeckModels
        vdmsb=[mod2]

    elif(len(mm) == 2 and (mod1 != None and mod2 != None)):
        vdmsa=[mod1]
        vdmsb=[mod2]

    elif(dohomo):
        vdmsa=vdms
        vdmsb=[modopt]
        
    else:
        vdmsa=vdms
        vdmsb=vdms


    b1id=stmopt[2:3]

    #
    # nhc tdo veri
    #
    optsadd=None

    tdos=TCtdos.GetTdos(b1id)
    
    if(b1id == 'L' or b1id == 'E'):
        tdos=['SRS','LAA','JLB','JLF','RDK','RJP','___',
              'DPB','ESB','HSM','JRR','MMM']

    #
    # jtwc tdo veri
    #
    if(b1id == 'W' or b1id == 'I' or b1id == 'B' or b1id == 'S' or b1id == 'P'):
        tdos=['CAB','JMM','JSB','JSD','RMK','JWL','YOP','___',
              'ADL','BGH','JWF','KAP','MBS','MEK','SGB']
        
    if(tdos):
        optsadd=[]
        tdocmps=['ofc.ofc06','ofc.con']

        for tdocmp in tdocmps:
            for tdo in tdos:
                optsadd.append([tdocmp,tdo])


    opts=[]

    if(dfeonly):
        
        optsadd=None
        for vdm in vdms:
            ounofc06="%s.ofc06"%(vdm)
            o06ofc06="%s06.ofc06"%(vdm)
            if(vdm != 'ofc' and vdm != 'clp' and vdm != 'con' ):
                opts.append([o06ofc06,None])
            else:
                opts.append([ounofc06,None])


    elif(votype == 3):
        

        #
        #  do hetero for the model
        #

        for imodel in vdms:

            if(len(imodel) <= 4):
                opts.append(["%s"%(imodel),None])
                opts.append(["%s00"%(imodel),None])
                opts.append(["%s06"%(imodel),None])
                opts.append(["%s12"%(imodel),None])
            else:
                opts.append(["%s"%(imodel),None])


    elif(dohomo):
        
        for vdm in vdmsa:
            moda=vdm
            oas=[]
            ouna="%s"%(vdm)
            o00a="%s00"%(vdm)
            o06a="%s06"%(vdm)
            o12a="%s12"%(vdm)

            oas.append(ouna)
            oas.append(o00a)
            oas.append(o06a)
            oas.append(o12a)

            for vdm in vdmsb:
                obs=[]
                modb=vdm
                ounb="%s"%(vdm)
                o00b="%s00"%(vdm)
                o06b="%s06"%(vdm)
                o12b="%s12"%(vdm)
                    
                obs.append(ounb)
                obs.append(o00b)
                obs.append(o06b)
                obs.append(o12b)

                for oa in oas:
                    for ob in obs:
                        if(oa != ob):
                            opts.append(["%s.%s"%(oa,ob),None])




    elif(mod1 != None and mod2 != None and mf.find(modopt,'all')):
        
        votype=mod2

        #
        #  do hetero for the model
        #
        
        opts.append(["%s"%(mod2),None])
        opts.append(["%s00"%(mod2),None])
        opts.append(["%s06"%(mod2),None])
        opts.append(["%s12"%(mod2),None])

        for vdm in vdmsa:
            moda=vdm
            oas=[]
            ouna="%s"%(vdm)
            o00a="%s00"%(vdm)
            o06a="%s06"%(vdm)
            o12a="%s12"%(vdm)

            oas.append(ouna)
            oas.append(o00a)
            oas.append(o06a)
            oas.append(o12a)

            for vdm in vdmsb:
                obs=[]
                modb=vdm
                ounb="%s"%(vdm)
                o00b="%s00"%(vdm)
                o06b="%s06"%(vdm)
                o12b="%s12"%(vdm)
                    
                obs.append(ounb)
                obs.append(o00b)
                obs.append(o06b)
                obs.append(o12b)



                for oa in oas:
                    for ob in obs:
                        atau=None
                        btau=None
                        if(len(oa) == 5): atau=int(oa[3:5])
                        if(len(ob) == 5): btau=int(ob[3:5])
                        if(moda == modb):
                            ###print 'ooooaaaa ',moda,modb,oa,ob,atau,btau
                            if(moda == 'con' or moda == 'clp' or moda == 'ofc' ):
                                if(
                                    (atau == None and btau == 6) or
                                    (atau == None and btau == 0) or
                                    (atau == 6 and btau == 0) or
                                    (atau == 0 and btau == 6) or
                                    (atau == 6 and btau == 6) or
                                    (atau == 0 and btau == 0) or
                                    (atau == 0 and btau == None)
                                    ):
                                    ###print 'dddddddddhhhhhhhhhhhh ',oa,ob
                                    opts.append(["%s.%s"%(oa,ob),None])

                            elif( (atau < btau) or
                                  (atau == None and btau == 6) or
                                  (atau == 0 and btau == 6) or
                                  (atau == 0 and btau == 0) or
                                  (atau == 6 and btau == 0) or
                                  (atau == 6 and btau == 6) or
                                  (atau == 0 and btau == 12)
                                  ):
                                ###print 'eeeeeeeeehhhhhhhhhhhh ',oa,ob
                                opts.append(["%s.%s"%(oa,ob),None])
                        else:
                            ##print 'dddddddd ',moda,modb,oa,ob,atau,btau
                            
                            if(modb == 'con' or modb == 'ofc'  or modb == 'ofi' ):
                                
                                if( (atau == 0 and btau == 0) or
                                    (atau == 6 and btau == None) or
                                    (atau == 6 and btau == 0) or
                                    (atau == 0 and btau == 6) or
                                    (atau == None and btau == 6) or
                                    (atau == None and btau == None) or
                                    (atau == 6 and btau == 6) or
                                    (atau == 0 and btau == None) or
                                    (atau == None and btau == 0)
                                    ):
                                    ###print 'dddddddddhhhhhhhhhhhh ',oa,ob
                                    opts.append(["%s.%s"%(oa,ob),None])


                            elif(moda == 'con' or moda == 'clp' or moda == 'ofc' ):
                                if( (atau == 0 and btau == 0) or
                                    (atau == None and btau == 6) or
                                    (atau == None and btau == 0) or
                                    (atau == 0 and btau == 6) or
                                    (atau == 6 and btau == 6) or
                                    (atau == 0 and btau == None) or
                                    (atau == 6 and btau == 0) or
                                    (atau == None and btau == None)
                                    ):
                                    ###print 'dddddddddhhhhhhhhhhhh ',oa,ob
                                    opts.append(["%s.%s"%(oa,ob),None])
                                    
                            elif(modb == 'con' or modb == 'ofc'  or modb == 'ofi' ):
                                
                                if( (atau == 0 and btau == 0) or
                                    (atau == 6 and btau == None) or
                                    (atau == 6 and btau == 0) or
                                    (atau == None and btau == 6) or
                                    (atau == None and btau == None) or
                                    (atau == 6 and btau == 6) or
                                    (atau == 0 and btau == None) or
                                    (atau == None and btau == 0)
                                    ):
                                    ###print 'dddddddddhhhhhhhhhhhh ',oa,ob
                                    opts.append(["%s.%s"%(oa,ob),None])

                            elif( modb == 'clp' ):
                                
                                if( (atau == 0 and btau == 0) or
                                    (atau == 6 and btau == None) or
                                    (atau == 6 and btau == 0) or
                                    (atau == 0 and btau == None) or
                                    (atau == 6 and btau == 6) or
                                    (atau == None and btau == 0)
                                    ):
                                    ###print 'dddddddddhhhhhhhhhhhh ',oa,ob
                                    opts.append(["%s.%s"%(oa,ob),None])

                            elif(
                                (atau == 0 and btau == 0) or
                                (atau == 6 and btau == 6) or
                                (atau == 0 and btau == None) or
                                (atau == 6 and btau == 0) or
                                (atau == None and btau == None)
                                ):
                                ###print 'dddddddddhhhhhhhhhhhh ',oa,ob
                                opts.append(["%s.%s"%(oa,ob),None])


        
    else:

        if(votype >= 1):
            
            for vdm in vdms:
                oas=[]
                ouna="%s"%(vdm)
                o00a="%s00"%(vdm)
                o06a="%s06"%(vdm)
                o12a="%s12"%(vdm)
                
                oas.append(ouna)
                oas.append(o00a)
                oas.append(o06a)
                oas.append(o12a)

                if(vdm != 'clip'):
                    ounaclp="%s.%s"%(ouna,'clip')
                    o00aclp="%s.%s"%(o00a,'clip00')
                    o06aclp="%s.%s"%(o06a,'clip06')
                    o06aclp="%s.%s"%(o06a,'clip')
                    oas.append(ounaclp)
                    oas.append(o00aclp)
                    oas.append(o06aclp)
                    
                for oa in oas:
                    opts.append(["%s"%(oa),None])

        else:
        
            for vdm in vdms:
                oun="%s"%(vdm)
                o00="%s00"%(vdm)
                o06="%s06"%(vdm)
                o12="%s12"%(vdm)
                oun00="%s.%s00"%(vdm,vdm)
                oun06="%s.%s06"%(vdm,vdm)

                oofcun00="ofc.%s00"%(vdm)
                oofcun06="ofc.%s06"%(vdm)
                opts.append([oofcun00,None])
                opts.append([oofcun06,None])

                o0006="%s00.%s06"%(vdm,vdm)
                o0606="%s06.%s06"%(vdm,vdm)
                o0012="%s00.%s12"%(vdm,vdm)

                o00ofc06="%s00.ofc06"%(vdm)
                o00ofc00="%s00.ofc00"%(vdm)
                o06ofc06="%s06.ofc06"%(vdm)

                ounclp00="%s.clp00"%(oun)
                o06clp00="%s.clp00"%(o06)


                opts.append([oun,None])
                opts.append([o00,None])


                opts.append([o06,None])
                opts.append([o12,None])
                if(atcf.DtauModel[vdm] == 6):
                    opts.append([o0006,None])
                opts.append([o0012,None])
                opts.append([o0606,None])
                opts.append([oun00,None])
                opts.append([oun06,None])
                opts.append([o06ofc06,None])
                opts.append([o00ofc00,None])
                opts.append([o06clp00,None])
                opts.append([ounclp00,None])


                #
                # always comp to avn00
                #
                if(vdm != 'gfs'):
                    om1m2="%s06.%s"%('gfs',o06)
                    opts.append([om1m2,None])
                    om1m2="%s00.%s"%('gfs',o00)
                    opts.append([om1m2,None])

                if(vdm != 'ukm'):
                    om1m2="%s06.%s"%('ukm',o06)
                    opts.append([om1m2,None])
                    om1m2="%s00.%s"%('ukm',o00)
                    opts.append([om1m2,None])

                if(vdm != 'ngp'):
                    om1m2="%s06.%s"%('ngp',o06)
                    opts.append([om1m2,None])
                    om1m2="%s00.%s"%('ngp',o00)
                    opts.append([om1m2,None])

                if(vdm != 'eco'):
                    om1m2="%s06.%s"%('eco',o06)
                    opts.append([om1m2,None])
                    om1m2="%s00.%s"%('eco',o00)
                    opts.append([om1m2,None])

                if(vdm != 'fv4'):
                    om1m2="%s06.%s"%('fv4',o06)
                    opts.append([om1m2,None])
                    om1m2="%s00.%s"%('fv4',o00)
                    opts.append([om1m2,None])

                if(vdm != 'fg4'):
                    om1m2="%s06.%s"%('fg4',o06)
                    opts.append([om1m2,None])
                    om1m2="%s00.%s"%('fg4',o00)
                    opts.append([om1m2,None])

                if(vdm != 'con'):
                    om1m2="%s00.%s"%('con',o06)
                    opts.append([om1m2,None])
                    om1m2="%s00.%s"%('con',o00)
                    opts.append([om1m2,None])
                    om1m2="%s06.%s"%('con',o06)
                    opts.append([om1m2,None])
                    om1m2="%s.%s"%('con',o06)
                    opts.append([om1m2,None])

                if(vdm != 'clp'):
                    om1m2="%s.%s"%(o06,'clp00')
                    opts.append([om1m2,None])

                if(vdm == 'ofc'):
                    om1m2="%s.%s"%(oun,'clp00')
                    opts.append([om1m2,None])


    dooptsadd=0
    if(optsadd and dooptsadd):
        opts=opts+optsadd
        
    return(opts,votype)


#----------------------------------------------------------------------
#
#  define the runs of vitals
#
#----------------------------------------------------------------------

def ParseMdeck2Btcs(dtgs,mdcards):
    
    btcs={}
    
    for dtg in dtgs:
        mdcard=mdcards[dtg]
        btc=ParseMdeckCard2Btcs(mdcard)
        btcs[dtg]=btc

    return(btcs)


def GetGcardsTcVitalsHash(stmopt,model,bts,fcs,gsfs):

    try:
        btcards=bts[stmopt,model]
    except:
        btcards=None

    try:
        fccards=fcs[stmopt,model,'ALL']
    except:
        fccards=None

    try:
        gsfcards=gsfs[stmopt,model]
    except:
        gsfcards=None

    return(btcards,fccards,gsfcards)



def FiltBtFcGcards(btcards,fccards,ebtdtg,fcmode):

    ebtdtgm6=mf.dtginc(ebtdtg,-6)
    bbtdtgm6=mf.dtginc(ebtdtg,-72)
    bbtdtgm6=mf.dtginc(ebtdtg,-36)

    nfccards=[]
    nbtcards=[]
    
    nbtcards.append('N bt:')

    if(fcmode == 3 or fcmode == 4):
        nbtcards=copy.deepcopy(btcards)
    else:
        nnbt=0
        for btcard in btcards[1:]:
            btdtg=btcard.split()[0]
            if(int(btdtg) <= int(ebtdtg)):
                nnbt=nnbt+1
                nbtcards.append(btcard)
                
        nbtcards[0]="%s %d"%(nbtcards[0],nnbt)

    nnfc=0
    for fccard in fccards:
        fcdtg=fccard.split()[1]

        if(fcmode == 1 or fcmode == 4):
            dtgtest= ( (int(fcdtg) <= int(ebtdtgm6)) and (int(fcdtg) >= int(bbtdtgm6)) )
        elif(fcmode == 2 or fcmode == 3):
            dtgtest=(int(fcdtg) == int(ebtdtg))
        else:
            print 'EEE invalid fcmode in TC.FiltBtFcGcards ',fcmode
            sys.exit()
            
        if(dtgtest):
            nnfc=nnfc+1
            nfccards.append(fccard)
            
    
    return(nbtcards,nfccards)
    

def FiltGsfGcards(gsfcards,ebtdtg=None,fcmode=None,pltopt=None,dohomo=None):

    ngsfcards=[]

    gsfcards=gsfcards.split('\n')

    ngsfcards=''

    nngsf=0
    
    for gsfcard in gsfcards:

        if(pltopt == 'plus5'):
            if( mf.find(gsfcard,'_ltmn') or mf.find(gsfcard,'_lnmn')):
                tt=gsfcard.split('=')
                ltln=float(tt[1])-5.0
                gsfcard="%s=%-6.1f"%(tt[0],ltln)
           
            elif( mf.find(gsfcard,'_ltmx') or mf.find(gsfcard,'_lnmx')):
                tt=gsfcard.split('=')
                ltln=float(tt[1])+5.0
                gsfcard="%s=%-6.1f"%(tt[0],ltln)

        if( mf.find(gsfcard,'_mtitle2') and ebtdtg != None ):
           tt=gsfcard.split('=')

           ltt=len(tt[1])

           nmadd=''
           if(fcmode == 1):
               nmadd="`4history thru: %s`0'"%(ebtdtg)
           
           elif(fcmode == 2):
               nmadd="`4Make Forecast: %s`0'"%(ebtdtg)
           
           elif(fcmode == 3):
               nmadd="`4Make FC + BT: %s`0'"%(ebtdtg)
           
           elif(fcmode == 4):
               nmadd="`4History + BT: %s`0'"%(ebtdtg)

           if(dohomo):
               nmadd="%s `4HOMO model stats`0'"%(nmadd)
               nmtitle2=tt[1][0:ltt-32]+nmadd
           else:
               nmtitle2=tt[1][0:ltt-25]+nmadd
               
           gsfcard="%s=%s"%(tt[0],nmtitle2)
           print 'filtgsf mtitle2',gsfcard

        ngsfcards="%s%s\n"%(ngsfcards,gsfcard)

    return(ngsfcards)
    

    
def TcFcStatLegend2(tcfcstat,tmodel,taufcveristat,legendmodels=None,verb=0):

    gsname='lgndstat2'
    gs=[]

    g=gs.append

    x0=0.10
    y0=0.02
    dx=1.35
    dy=0.40

    
    if(legendmodels == None):
        lgndmodels=['ofc','con','fg4','gfs','ngp','ukm','eco']
        if(tmodel == 'fv4' or tmodel == 'fg4' or tmodel == 'fv5' or tmodel == 'fd5' or
           tmodel == 'cn3' or tmodel == 'cn4' or tmodel == 'cne' or tmodel == 'cnf' or tmodel == 'pne' or
           tmodel == 'avo' or tmodel == 'avi' or tmodel == 'gfd' or tmodel == 'gfi' or
           tmodel == 'uko' or tmodel == 'uki' or tmodel == 'ngn' or tmodel == 'fss'
           ):
        
            lgndmodels=['ofc','con',tmodel,'gfs','ngp','ukm','eco']
            
    else:
        lgndmodels=legendmodels
    

    nmodels=len(lgndmodels)

    xst=(x0+dx*nmodels)*0.5
    xst=(x0+0.1)
    yst=y0+dy+0.125
    ssizt=0.08
    titlet="`0%s-h FE [nm] + (N cases) + %% Improve over ofc06 and [clp]`0"%(taufcveristat)
    
    g("function %s"%(gsname))

    g('x0=%f'%(x0))
    g('y0=%f'%(y0))
    g('dx=%f'%(dx))
    g('dy=%f'%(dy))

    g('lcol=81')
    g('bcolact=21')
    g('bcolinact=31')

    g("'set line 1 0 4'")
    g("'set string 4 ' l ' 4'")
    g("'set strsiz %s'"%(ssizt))
    g("'draw string %f %f %s'"%(xst,yst,titlet))
    
    tcmodels=[]
    tcmodelstats={}
    if(tcfcstat == None): return

    n=0
    for lgndmodel in lgndmodels:

        try:
            (nbt,nfc,femod1,idfe,idfeclp)=tcfcstat[lgndmodel,taufcveristat]
        except:
            continue
        
        modeln=int(nfc)
        if(nbt > 0 and modeln > 0):
            modelpod = ( (float(nbt)-float(nfc))/float(nbt) )*100.0
        else:
            modelpod =-999
            
        modelimp=idfe
        modelimpclp=idfeclp
        modelfe="%3.0f"%(femod1)
        
        modelfve='-'
        modelfveu='-'

        lmodel=lgndmodel.upper()

        if(lmodel == 'ECO'): lmodel='ECMWF(ops)'
        if(lmodel == 'ECE'): lmodel='ECMWF(EPS)'

        if(modeln == 0):
            cell1="_title.1.1=\'%s (%s) '"%(lmodel,nbt)
            cell2="_title.2.1=\'---\'"
            cell3="_title.2.2=\'---\'"
        else:
            cell1="_title.1.1=\'%s (%s) '"%(lmodel,nbt)
            cell2="_title.2.1=\'`4%s`0 (%s)\'"%(modelfe,modeln)
            cell3="_title.2.2=\'%s [%s]\'"%(modelimp,modelimpclp.strip())
            

        card="%s ; %s ; %s"%(cell1,cell2,cell3)

        bcol='bcolinact'
        if(lgndmodel == tmodel): bcol='bcolact'
        
        if(n==0):
            g('_title.1.1=\'Model (N bt)\'    ;    _title.2.1=\'FE (N fc)\'   ;   _title.2.2=\'%O06[CLP]\'')
            g('rc=prntstat(x0,y0,dx,dy,lcol)')
            g(card)
            g('x0=x0+dx')
            g("rc=prntstat(x0,y0,dx,dy,%s)"%(bcol))
            
        else:
            g(card)
            g('x0=x0+dx')
            g("rc=prntstat(x0,y0,dx,dy,%s)"%(bcol))

        n=n+1


    g('return')
    
    gspath="%s.gsf"%(gsname)
    gsfile=open(gspath,'w')

    for gg in gs:
        gg=gg+'\n'
        if(verb): print gg[:-1]
        gsfile.write(gg)
        
    gsfile.close()

    return



def MakeVitalsAllPy(allpy,iecard,stmopt,modopt,tdoopt,
                    vpycards,dfepycards,btpycards,scards,
                    btgcards,fcgcards,gsf1,dohomo,verb=0):

    for pycard in vpycards:
        allpy.append(pycard)

    for dfepycard in dfepycards:
        allpy.append(dfepycard)

    if(dohomo == 0):
        for btpycard in btpycards:
            allpy.append(btpycard)

    if(verb):
        for scard in scards:
            chk=scard.split()[11]
            if(chk != '-999'): print scard[0:iecard]

    if(dohomo == 0):
        #
        #  BtGcards
        #
        pycard="""
BtGcards['%s','%s'] = [ """%(stmopt,modopt)
        allpy.append(pycard)

        for bt in btgcards:
            pycard="'%s',"%(bt)
            allpy.append(pycard)

        pycard="""]
        """
        allpy.append(pycard)



        #
        #  FcGcards
        #
        if(tdoopt != None):
            otdoopt=tdoopt
        else:
            otdoopt='ALL'

        pycard="""
FcGcards['%s','%s','%s'] = [ """%(stmopt,modopt,otdoopt)
        allpy.append(pycard)

        for fc in fcgcards:
            pycard="'%s',"%(fc)
            allpy.append(pycard)

        pycard="""]
        """
        allpy.append(pycard)


        #
        #  gsfcards
        #
        pycard="""
GsfGcards['%s','%s'] = \"\"\" """%(stmopt,modopt)
        allpy.append(pycard)

        pycard=gsf1
        allpy.append(pycard)

        pycard="""\"\"\"
        """
        allpy.append(pycard)

    return



def MakeTcStmidsList(stmopt,dofilt9x=1,quiet=1):

    obasin=None
    obid=None
    oyear=None
    ohemi=None

    vstmids=[]
    stmmeta={}

    stmids=MakeStmList(stmopt)

    for stmid in stmids:

        (stm,year)=stmid.split('.')
        b1id=stm[2]
        chk9x=(int(stm[0]) == 9)
        if(dofilt9x and chk9x):
            continue
        
        tcnames=GetTCnamesHash(year)
        tcstats=GetTCstatsHash(year)

        vstmids.append(stmid)

        try:
            tstmname=tcnames[year,stm]
        except:
            tstmname='NoName'

        try:
            tstmstat=tcstats[year,stm]
            tstmtype=tstmstat[0]
        except:
            tstmtype='TC'
            if( int(stmid[0]) == 9 ):
                if(not(quiet)):
                   print "WWWWWWWWWW problem with tcstats: %s %s ...continue"%(year,stmid)
                continue
            else:
                print "EEEEEEEEEE problem with tcstats: %s %s ...STOP"%(year,stmid[0])
                sys.exit()
            
        tstmtype=tstmtype.strip()

        tstmname=tcnames[year,stm]
        stmmeta[stmid]=[tstmname,tstmtype]


    if(obasin == None): obasin=b1id
    if(obid == None): obid=b1id
    if(oyear == None): oyear=year
    if(ohemi == None and obasin != None): ohemi=Basin1toHemi4[obasin]
        
    return(stmids,stmmeta,oyear,obasin,obid,ohemi)




def ModelTcFcTracksLocation(dtg,imodel):

    yyyymm=dtg[0:6]
    yyyymm=int(yyyymm)

    dotcanaltrackers=0
    ftype='adeck'
    imodelalias=imodel

    #
    # 20060613 -- allow for alias
    #
    if(imodel == 'gfs' or imodel == 'cmc'):
        dotcanaltrackers=1
        ftype='mf'
        ftype='adeck'
        
    elif(yyyymm >= 200512):
        if(imodel == 'ngp' or imodel == 'ukm' or imodel == 'ecm' ):
            dotcanaltrackers=0
            ftype='mf'
            ftype='adeck'
            
    elif(yyyymm >= 200506):

        if(imodel == 'clp'):
            dotcanaltrackers=1
            ftype='mf'

    elif(imodel == 'fg4' or imodel == 'fg5'):
        dotcanaltrackers=1


    return(dotcanaltrackers,ftype,imodelalias)
        
def FcGlobYearRange(dtg,stm3id):
    
    hemi=Basin1toHemi[stm3id[-1]]
    iyear=int(dtg[0:4])
    imo=int(dtg[4:6])
    if(hemi == 'N'):
        if(imo == 1):
            iyears=[iyear-1,iyear]
        else:
            iyears=[iyear]
    else:
        if(imo == 7):
            iyears=[iyear,iyear+1]
        elif(imo > 7):
            iyears=[iyear+1]
        else:
            iyears=[iyear]

    return(iyears)
    

def GetTcFcCards(dtg,imodel,ifctype,stm3id,prcopt='ops',useallstms=0,verb=0,quiet=1):

    ftmfcards=None
    ftcards=None

    (dotcanaltrackers,tcanalftype,imodelalias)=ModelTcFcTracksLocation(dtg,imodel)

    if(imodel == 'eco' or imodel == 'ece'):

        ftdir=AdeckDirEcmwf
        ftype='adeck'

        ftmaskops='%s/wxmap.%s.%s.*'%(ftdir,imodel,dtg)
        ftpathsops=glob.glob(ftmaskops)

        ftmaskmsl='%s/wxmap.MSL.%s.%s.*'%(ftdir,imodel,dtg)
        ftpathsmsl=glob.glob(ftmaskmsl)

        if(len(ftpathsmsl) == 0 and len(ftpathsops) != 0):
            ftpaths=ftpathsops
            if(verb): print 'FFFFFFFFF ecmwf: using OPS paths only ',ftpaths

        elif(len(ftpathsmsl) != 0 and len(ftpathsops) == 0):
            ftpaths=ftpathsmsl
            if(verb): print 'FFFFFFFFF ecmwf: using MSL paths only'

        else:
            ftpaths=ftpathsmsl+ftpathsops


        if(verb): print ftpaths

        ftcards=[]    
        for ftpath in ftpaths:
            cards=open(ftpath).readlines()
            for card in cards:
                ftcards.append(card)

    elif(imodel == 'fv4' or imodel == 'fv5' or imodel == 'fd5'):

        ftdir1=AdeckDirNasa
        ftype='adeck'

        ftmask1='%s/????/wxmap/wxmap.%s.%s.*'%(ftdir1,imodel,dtg)
        if(verb): print 'ADECK ftmask1: ',ftmask1
        ftpaths1=glob.glob(ftmask1)

        ftpaths=ftpaths1

        if(verb):
            print 'adeck data for : ',imodel,' ftpaths: ',ftpaths

        ftcards=[]    
        for ftpath in ftpaths:
            (d,f)=os.path.split(ftpath)
            cards=open(ftpath).readlines()
            for card in cards:
                ftcards.append(card)


    #w2w2w2w2w2w2w2w2w2w2w2w2w2w2w2
    #
    # tcanal trackers in w2 
    #
    #w2w2w2w2w2w2w2w2w2w2w2w2w2w2w2
    
    elif(ifctype == 0):

        ftdir1=TcanalDatDir
        ftdir1offline=TcanalDatDirusb2
        ftype=tcanalftype

        if(ftype == 'adeck'):
            ftmask1="%s/%s/trk/wxmap.%s.%s.*"%(ftdir1,dtg,imodelalias,dtg)
            if(verb): print 'ADECK ftmask1: ',ftmask1
            ftpaths1=glob.glob(ftmask1)
            if(verb):
                print 'adeck data for : ',imodelalias,' ftpaths: ',ftpaths
                
            ftpaths=ftpaths1

            ftcards=[]    
            for ftpath in ftpaths:
                (d,f)=os.path.split(ftpath)
                cards=open(ftpath).readlines()
                for card in cards:
                    ftcards.append(card)


        elif(ftype == 'mf'):

            yyyy=dtg[0:4]
            ftfile="ngtrk.track.%s.%s.txt"%(imodelalias,dtg)
            ftfilemf="ngtrk.track.diag.mf.%s.%s.txt"%(imodelalias,dtg)

            
            ftdpath="%s/%s/%s/trk/%s"%(ftdir1,yyyy,dtg,ftfile)
            ftdpathmf="%s/%s/%s/trk/%s"%(ftdir1,yyyy,dtg,ftfilemf)


            if(verb):
                print 'FFFF paths ',ftdpath,ftdpathmf

            try:
                ftcards=open(ftdpath).readlines()
            except:
                #
                # try offline
                #
                ftdpath="%s/%s/%s/trk/%s"%(ftdir1offline,yyyy,dtg,ftfile)
                ftdpathmf="%s/%s/%s/trk/%s"%(ftdir1offline,yyyy,dtg,ftfilemf)
                if(verb >= 1):
                    print 'WWWWW: try OFFLINE tcanal: ',ftdpath


            try:
                ftcards=open(ftdpath).readlines()
            except:
                if(verb): print "EEE unable to read/open: %s"%(ftdpath)
                #
                # close to make 0 length
                #
                ftcards=None

            try:
                ftmfcards=open(ftdpathmf).readlines()
            except:
                ftmfcards=None

            #print 'qqq ',verb
            #sys.exit()

    #w2w2w2w2w2w2w2w2w2w2w2w2w2w2w2
    #
    # ops adecks converted to w2 adeck file struct
    #
    #w2w2w2w2w2w2w2w2w2w2w2w2w2w2w2

    elif(ifctype == 1):

        #
        # for speed calc years to glob
        #
        yearmasks=FcGlobYearRange(dtg,stm3id)

        b1id=stm3id[2]
        ftdir1=AdeckDirJtwc
        ftdir2=AdeckDirNhc
        ftdir3=AdeckDirEcmwf
        ftdir4=AdeckDirNcep
        ftdir5=AdeckDirJma
        ftdir6=AdeckDirLocal
        ftdir7=AdeckDirTpc
        ftdir8=AdeckDirGsd
        ftdir9=AdeckDirHrd


        dojtwctrk=0
        donhctrk=0
        doecmwftrk=0
        donceptrk=0
        dojmatrk=0
        dolocaltrk=0
        dotpctrk=1
        dogsdtrk=0
        dohrdtrk=0
        
        if(IsJtwcBasin(b1id)):
            dojtwctrk=1
            dojmatrk=0
            
        if(IsNhcBasin(b1id)):
            donhctrk=1
            dojmatrk=1

        if(atcf.IsLocalTrackModel(imodel)):
            dojtwctrk=0
            donhctrk=0
            doecmwftrk=0
            dojmatrk=0
            dolocaltrk=1
            dotpctrk=0

        if(atcf.IsEcmwfTrackModel(imodel)):
            doecmwftrk=1
            dotpctrk=0
            dojtwctrk=1
            donhctrk=0
            dojmatrk=0

        if(atcf.IsNcepTrackModel(imodel)):
            dojtwctrk=0
            donhctrk=0
            doecmwftrk=0
            donceptrk=1
            dojmatrk=0
            dotpctrk=0
            dolocaltrk=0

        if(atcf.IsGsdTrackModel(imodel)):
            dojtwctrk=0
            donhctrk=1
            doecmwftrk=0
            donceptrk=0
            dojmatrk=0
            dotpctrk=0
            dolocaltrk=0
            dogsdtrk=1

        if(atcf.IsHrdTrackModel(imodel)):
            dojtwctrk=0
            donhctrk=0
            doecmwftrk=0
            donceptrk=0
            dojmatrk=0
            dotpctrk=0
            dolocaltrk=0
            dogsdtrk=0
            dohrdtrk=1

        if(dojmatrk):
            dotpctrk=0


        dojtwctrk=donhctrk=1
        
        ftype='adeck'
        ftpaths1=ftpaths2=ftpaths3=ftpaths4=ftpaths5=ftpaths6=ftpaths7=ftpaths8=ftpaths9=[]

        #print 'VD dotrk: ',imodel,dojtwctrk,donhctrk,doecmwftrk,donceptrk,dojmatrk,dolocaltrk,dotpctrk,dogsdtrk,dohrdtrk,' useallstms ',useallstms
        
        for yearmask in yearmasks:

            if(dojtwctrk):
                ftmask1='%s/%s/wxmap/wxmap.%s.%s.%s'%(ftdir1,yearmask,imodel,dtg,stm3id)
                if(useallstms):
                    ftmask1='%s/%s/wxmap/wxmap.%s.%s.*'%(ftdir1,yearmask,imodel,dtg)
                if(verb): print 'ADECK (jtwc) ftmask1: ',ftmask1
                ftpaths1=ftpaths1+glob.glob(ftmask1)

            if(donhctrk):
                ftmask2='%s/%s/wxmap/wxmap.%s.%s.%s'%(ftdir2,yearmask,imodel,dtg,stm3id)
                if(useallstms):
                    ftmask2='%s/%s/wxmap/wxmap.%s.%s.*'%(ftdir2,yearmask,imodel,dtg)
                if(verb): print 'ADECK ftmask2: ',ftmask2
                ftpaths2=ftpaths2+glob.glob(ftmask2)

            #
            # for ecmwf grep all storms because of post-season renumber hard to do with non-nhc adecks
            #
            if(doecmwftrk):
                imodelmask=imodel
                if(imodel == 'ecmo' or imodel == 'ecmt' and yearmask <= 2001):
                    imodelmask='eco'
                ftmask3='%s/%s/wxmap/wxmap.%s.%s.*'%(ftdir3,yearmask,imodelmask,dtg)
                if(verb): print 'ADECK (ecmwf) ftmask3: ',ftmask3
                ftpaths3=ftpaths3+glob.glob(ftmask3)

            #
            # ncep -- where experimental adecks from emc/gfdl are located, they tend to mess up storm numbering, so useallstms
            #
            # 20080423 -- change ftmask4='%s/%s/wxmap/wxmap.%s.%s.%s'%(ftdir4,yearmask,imodel,dtg,stm3id)
            if(donceptrk):
                ftmask4='%s/%s/wxmap/wxmap.%s.%s.*'%(ftdir4,yearmask,imodel,dtg)
                if(useallstms):
                    ftmask4='%s/%s/wxmap/wxmap.%s.%s.*'%(ftdir4,yearmask,imodel,dtg)
                if(verb): print 'ADECK ftmask4: ',ftmask4
                ftpaths4=ftpaths4+glob.glob(ftmask4)
            
            #
            # look in jma adeck dir
            #
            if(dojmatrk):
                ftmask5='%s/%s/wxmap/wxmap.%s.%s.%s'%(ftdir5,yearmask,imodel,dtg,stm3id)
                if(useallstms):
                    ftmask5='%s/%s/wxmap/wxmap.%s.%s.*'%(ftdir5,yearmask,imodel,dtg)
                if(verb): print 'ADECK ftmask5: ',ftmask5
                ftpaths5=ftpaths5+glob.glob(ftmask5)

            #
            # look in local adeck dir -- force to use all stms  -- problem is the local adecks file names are not renumbered
            # 20080703 -- changed to renumber the wxmap adecks
            # 
            if(dolocaltrk):
                ftmask6='%s/%s/wxmap/wxmap.%s.%s.%s'%(ftdir6,yearmask,imodel,dtg,stm3id)
                if(useallstms):
                    ftmask6='%s/%s/wxmap/wxmap.%s.%s.*'%(ftdir6,yearmask,imodel,dtg)
                stm3id=stm3id.lower()
                ftdir6='/w21/dat/tc/adeck/tmtrkN'
                ftmask6='%s/%s/%s/tctrk.atcf.%s.%s.%s.txt'%(ftdir6,dtg[0:4],dtg,dtg,imodel,stm3id)
                if(verb): print 'ADECK ftmask6: ',ftmask6
                if(useallstms):
                    ftmask6='%s/%s/wxmap/wxmap.%s.%s.*'%(ftdir6,yearmask,imodel,dtg)
                if(verb): print 'ADECK ftmask6: ',ftmask6
                ftpaths6=ftpaths6+glob.glob(ftmask6)

            #
            # look in tcp adeck dir
            #
            if(dotpctrk):
                ftmask7='%s/%s/wxmap/wxmap.%s.%s.*'%(ftdir7,yearmask,imodel,dtg)
                if(useallstms):
                    ftmask7='%s/%s/wxmap/wxmap.%s.%s.*'%(ftdir7,yearmask,imodel,dtg)
                if(verb): print 'ADECK ftmask7: ',ftmask7
                ftpaths7=ftpaths7+glob.glob(ftmask7)

            #
            # look in gsd adeck dir
            #
            if(dogsdtrk):
                ftmask8='%s/%s/wxmap/wxmap.%s.%s.*'%(ftdir8,yearmask,imodel,dtg)
                if(useallstms):
                    ftmask8='%s/%s/wxmap/wxmap.%s.%s.*'%(ftdir8,yearmask,imodel,dtg)
                if(verb): print 'ADECK ftmask8: ',ftmask8
                ftpaths8=ftpaths8+glob.glob(ftmask8)

            #
            # look in hrd adeck dir
            #
            if(dohrdtrk):
                ftmask9='%s/%s/wxmap/wxmap.%s.%s.*'%(ftdir9,yearmask,imodel,dtg)
                if(useallstms):
                    ftmask9='%s/%s/wxmap/wxmap.%s.%s.*'%(ftdir9,yearmask,imodel,dtg)
                if(verb): print 'ADECK ftmask9: ',ftmask9
                ftpaths9=ftpaths9+glob.glob(ftmask9)

        ftpaths=ftpaths1+ftpaths2+ftpaths3+ftpaths4+ftpaths5+ftpaths6+ftpaths7+ftpaths8+ftpaths9

        #
        # check for dups in the ftpaths for wxmap adecks
        #
        def dupftpaths(ftpaths):
            fts={}
            oftpaths=[]
            for ftpath in ftpaths:
                (d,f)=os.path.splitext(ftpath)
                siz=mf.GetPathSiz(ftpath)
                age=mf.PathDmtime(ftpath)
                stmid=f.split('.')[1]
                fts[stmid]=ftpath
                
            kk=fts.keys()

            for k in kk:
                oftpaths.append(fts[k])

            return(oftpaths)

        nftpaths=len(ftpaths)
        ftpaths=dupftpaths(ftpaths)
        nftpathsuniq=len(ftpaths)

        if(nftpaths != nftpathsuniq):
            #print 'EEEEEEEEE TCw2.GetTcFcCards: multiply wxmap.adeck paths for: ',imodel
            #sys.exit()
            print 'WWWWWWWWWWW TC.GetTcFcCards: multiply wxmap.adeck paths for: ',imodel
            for ftpath in ftpaths:
                print 'ftpath useds: ',ftpath
                
            

        ftcards=[]    
        for ftpath in ftpaths:
            (d,f)=os.path.split(ftpath)
            cards=open(ftpath).readlines()
            
            if(len(cards) > 0 and not(quiet) ):
                print 'adeck data FOuND for : ',imodel,' ftpath: ',ftpath,' ntot: ',nftpaths,' nuniq: ',nftpathsuniq

            for card in cards:
                ftcards.append(card)

    else:

        #ffffffffffffffffffffffffffffffffffffffffffffff
        #
        # mf/fnmoc trackers
        #
        #ffffffffffffffffffffffffffffffffffffffffffffff

        ftype='mf'

        if(prcopt == 'ops'):
            ftdir=ModelFcDir(imodel,mopt='ops')
        else:
            ftdir=ModelFcDir(imodel)

        if(imodel == 'eclp'): imodel='clp'

        ftfile="tc.%s.%s.tracks.txt"%(imodel,dtg)
        ftfilemf="tc.%s.%s.tracks.mf.txt"%(imodel,dtg)

        ftdpath="%s/%s"%(ftdir,ftfile)
        ftdpathmf="%s/%s"%(ftdir,ftfilemf)

        if(verb):
            print 'FFFF paths ',ftdpath,ftdpathmf

        try:
            ftcards=open(ftdpath).readlines()
        except:
            if(verb): print "EEE unable to read/open: %s"%(ftdpath)
            #
            # close to make 0 length
            #
            ftcards=None

        try:
            ftmfcards=open(ftdpathmf).readlines()
        except:
            ftmfcards=None

    return(ftcards,ftmfcards,ftype)

#--------------------------------------------------
#
#  get w2 ftcards from adecks dic by dtg
#
#--------------------------------------------------

def GetTcFcCardsW2(dtg,amodel,phr,aftcards,verb=0):

    ftmfcards=None
    ftype='adeck'

    try:
        ftcards=aftcards[dtg]
    except:
        ftcards=None

    if(ftcards != None and verb):
        for ftcard in ftcards:
            print 'qqq ',ftcard[:-1]

    return(ftcards,ftmfcards,ftype)


def MfePerishibility(allstats,dohomo,taus):

    if(len(allstats) != 3 and dohomo == 0):
        print 'EEE in MfePerishibility must have 3 sets of stats'
        return
    elif(dohomo == 1 and len(allstats) != 2):
        print 'WWW in MfePerishibility must have 3 sets of stats'
        return

    (mod1,mfe1s,mfe2s,mcte1s,mcte2s,
     mate1s,mate2s,
     mvear1s,mvear2s,mvebr1s,mvebr2s,
     gainxys,gaine6xs,nfe1s,
     mfe2m1s,pof1s,pod1s,nrun1s,
     nrunmiss1s,nbt1s,nfc1s,
     nfcmiss1s,nfcover1s)=allstats[0]

    if(dohomo):
        mfe0=mfe1s
        gain6h=gaine6xs
        mfe12=mfe2s
    else:
        mfe0=mfe1s
        gain6h=gaine6xs

    (mod1,mfe1s,mfe2s,mcte1s,mcte2s,
     mate1s,mate2s,
     gainxys,gaine6xs,nfe1s,
     mfe2m1s,pof1s,pod1s,nrun1s,
     nrunmiss1s,nbt1s,nfc1s,
     nfcmiss1s,nfcover1s)=allstats[1]

    if(dohomo):
        mfe06=mfe1s
    else:
        mfe06=mfe1s

    if(dohomo == 0):
        (mod1,mfe1s,mfe2s,mcte1s,mcte2s,
         mate1s,mate2s,
         gainxys,gaine6xs,nfe1s,
         mfe2m1s,pof1s,pod1s,nrun1s,
         nrunmiss1s,nbt1s,nfc1s,
         nfcmiss1s,nfcover1s)=allstats[2]
        mfe12=mfe1s

    for tau in taus:

        fe0=mfe0[tau]
        fe6=mfe06[tau]
        fe12=mfe12[tau]
        g6h=gain6h[tau]
        g12h=g6h*2.0
        
        df6m0=(fe6-fe0)
        df12m0=(fe12-fe0)

        if(g6h > 0.0):
            pi6m0=df6m0/g6h
            pi12m0=df12m0/g12h
        else:
            pi6m0=-999
            pi12m0=-999
        
        card1="pppp tau: %3d  fe0,6,12: %5.1f %5.1f %5.1f : g6,12h: %5.1f %5.1f"%(tau,fe0,fe6,fe12,g6h,g12h)
        card2=" dfe6m0: %5.1f df12m0: %5.1f : pi6m0: %5.2f pi12m0: %5.2f"%(df6m0,df12m0,pi6m0,pi12m0)

        card=card1+card2
        print card


    return





#vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
#
#  vdeck qc
#
#vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv


def VdeckQc(stmopt,modopt,verb=0,ruleopt=None):

    year=stmopt.split('.')[1]
    stm3id=stmopt.split('.')[0]
    b1id=stm3id[2:3]
    b3id=Basin1toBasin3[b1id]

    tt=modopt.split('.')
    if(len(tt) == 2):
        imodels=tt
        nmodels=2
    elif(len(tt) == 1):
        imodels=[modopt]
        nmodels=1
    else:
        print 'EEEE invalid modopt: ',modopt
        sys.exit()

    if(ruleopt == None):
        oruleopt='ops'
    else:
        oruleopt=ruleopt

    vddir=BaseDirDataTc+"/vdeck/%s"%(year)

    nmodel=1
    for imodel in imodels:

        vdmodel=imodel

        limod=len(imodel)

        if(atcf.DtauModel[imodel] == 12):
            
            if(phr == None and atcf.StartSynHourModel[imodel] == 6):
                filt0012=0
                filt0618=1
            elif(phr != None and int(phr) == 6 and atcf.StartSynHourModel[imodel] == 6):
                filt0012=1
                filt0618=0
            elif(phr != None and int(phr) == 0 and atcf.StartSynHourModel[imodel] == 6):
                filt0012=0
                filt0618=1
            elif(phr != None and int(phr) == 6):
                filt0012=0
                filt0618=1
            else:
                filt0012=1
                filt0618=0

        vdmask="%s/vdeck.%s.%s.%s.%s.*.txt"%(vddir,b3id,year,stm3id,vdmodel)
        ls=glob.glob(vdmask)
        if(len(ls) == 1):
            vdpath=ls[0]
        else:
            print 'EEE no vdecks for: ',stmopt,' and vdmask: ',vdmask
            return(None,None,None,None,None,None,None)

        if(verb): print 'vdmask ',vdmask,ls,vdmodel
        tt=vdpath.split('.')
        b3id=tt[1]
        year=tt[2]
        stm3id=tt[3]
        b1id=stm3id[2:3]
        bdtg=tt[5]
        edtg=tt[6]

        vdcards=open(vdpath,'r').readlines()

        if(nmodel == 1):
            vdmodel1=vdmodel
            (idtgs,fcs1)=ParseVdeck2Fcs(vdcards)
            rclist=SetBtVdeck(stm3id,imodel,idtgs,fcs1,ruleopt,verb=verb)
        elif(nmodel == 2):
            vdmodel2=vdmodel
            (idtgs,fcs2)=ParseVdeck2Fcs(vdcards)
            rclist=SetBtVdeck(stm3id,imodel,idtgs,fcs2,ruleopt,verb=verb)


    unsignedwarn=[]
    report=None


    n=0
    for idtg in idtgs:
        tdo=fcs1[idtg,0,'tdo']
        warnstatus=fcs1[idtg,'btflg'][3]
        if( (tdo == None or tdo == '___') and
            (warnstatus == 'WN')
            and
            (TCtdos.FcTdoSign(idtg,stmopt) == None) ):
            
            if(n==0):
                print
                print 'unsigned advisory STM: ',stmopt
                unsignedwarn.append([idtg,stmopt])
                
            print 'unsigned advisory DTG:: ', idtg
            n=n+1


    return(unsignedwarn)



def ParseMdeckCard2Btcs(mdcard):
    

#new format for mdeck
#
#  0 2007090800
#  1 09L.2007
#  2 020
#  3 1009
#  4 23.5
#  5 274.5
#  6 -999
#  7 -999
#  8 360.0
#  9 0.0
#  10 0
#  11 FL:
#  12 NT
#  13 DB
#  14 NC
#  15 NC
#  16 NW
#  17 LF:
#  18 0.00
#  19 TDO:
#  20 ___
#  21 C:
#  22 -99.9
#  23 -999.9
#  24 -999
#  25 999.9
#  26 99.9
#  27 ______
#  28 W:
#  29 -99.9
#  30 -999.9
#  31 -999
#  32 999.9
#  33 99.9
#  34 RadSrc:
#  35 none
#  36 r34:
#  37 -999
#  38 -999
#  39 -999
#  40 -999
#  41 r50:
#  42 -999
#  43 -999
#  44 -999
#  45 -999
#  46 CP/Roci:
#  47 9999.0
#  48 999.0
#  49 CRm:
#  50 999.0
#  51 CDi:
#  52 999.0
#  53 Cdpth:
#  54 K

    tt=mdcard.split()
    ntt=len(tt)

    #for n in range(0,ntt):
    #    print 'mmmmmmm ',n,tt[n]

    i=0

    dtg=tt[i] ; i=i+1
    sid=tt[i] ; i=i+1
    bvmax=float(tt[i])  ; i=i+1
    bpmin=float(tt[i]) ; i=i+1
    blat=float(tt[i]) ; i=i+1
    blon=float(tt[i]) ; i=i+1
    r34=float(tt[i]) ; i=i+1
    r50=float(tt[i]) ; i=i+1
    bdir=float(tt[i]) ; i=i+1
    bspd=float(tt[i]) ; i=i+1
    tsnum=int(tt[i]) ; i=i+1
    dum=tt[i] ; i=i+1
    flgtc=tt[i] ; i=i+1
    flgind=tt[i] ; i=i+1
    flgcq=tt[i] ; i=i+1
    flgwn=tt[i] ; i=i+1
    dum=tt[i] ; i=i+1
    lf=float(tt[i]) ; i=i+1
    dum=tt[i] ; i=i+1
    tdo=tt[i] ; i=i+1

    ic=21
    cqlat=float(tt[ic])  ; ic=ic+1
    cqlon=float(tt[ic])  ; ic=ic+1
    cqvmax=float(tt[ic]) ; ic=ic+1
    cqdir=float(tt[ic])  ; ic=ic+1
    cqspd=float(tt[ic])  ; ic=ic+1
    cqpmin=float(tt[ic])  ; ic=ic+1

    iw=29
    wlat=float(tt[iw])  ; iw=iw+1
    wlon=float(tt[iw])  ; iw=iw+1
    wvmax=float(tt[iw]) ; iw=iw+1

    if(ntt == 55):
        ir=37
        r34ne=int(tt[ir]) ; ir=ir+1
        r34se=int(tt[ir]) ; ir=ir+1
        r34sw=int(tt[ir]) ; ir=ir+1
        r34nw=int(tt[ir]) ; ir=ir+2

        r50ne=int(tt[ir]) ; ir=ir+1
        r50se=int(tt[ir]) ; ir=ir+1
        r50sw=int(tt[ir]) ; ir=ir+1
        r50nw=int(tt[ir]) ; ir=ir+2
        
        ir=47
        poci=float(tt[ir]) ; ir=ir+1
        roci=float(tt[ir]) ; ir=ir+2
    
        rmax=float(tt[ir]) ; ir=ir+2
        reye=float(tt[ir]) ; ir=ir+2
        tcdepth=tt[ir]

    else:
        r34ne=r34se=r34sw=r34nw=-999.0
        r50ne=r50se=r50sw=r50nw=-999.0

    r34quad=[r34ne,r34se,r34sw,r34nw]
    r50quad=[r50ne,r50se,r50sw,r50nw]

    if(cqdir > 720.0):
        cqdir=-999.9
        cqspd=-99.9

    btdic=[flgtc,flgind,flgcq,flgwn,tdo,lf,cqlat,cqlon,cqvmax,wlat,wlon,wvmax,tsnum]
    cqdic=[cqlat,cqlon,cqvmax,cqdir,cqspd,cqpmin]
    bwdic=[bvmax,r34,r50,rmax,reye,poci,roci]
    btc=[blat,blon,bvmax,bpmin,bdir,bspd,btdic,cqdic,bwdic,r34quad,r50quad]

    return(btc)


def GetMap9x(dtg,verb=0):

    year=dtg[0:4]
    
    mddir=w2.TcMdecksFinalDir+"/%s"%(year)

    md9s=glob.glob("%s/MdOps.*.9??.*"%(mddir))
    md1s=glob.glob("%s/MD.*.???.*"%(mddir))

    m9s={}
    m1s={}

    m9lls={}
    m1lls={}

    m9xdtg={}
    m1xdtg={}

    for md9 in md9s:
        (dir,file)=os.path.split(md9)

        tt=file.split('.')
        basin=tt[1]
        m9x=tt[3]
        bdtg=tt[4]
        edtg=tt[5]
        m9xdtg[basin,m9x]=(bdtg,edtg)
        m9s[basin,m9x]=md9

        card=open(md9).readline()
        tt=card.split()
        m9lls[basin,m9x]=(float(tt[4]),float(tt[5]))


    for md1 in md1s:
        (dir,file)=os.path.split(md1)
        tt=file.split('.')
        basin=tt[1]
        m1x=tt[3]
        bdtg=tt[4]
        edtg=tt[5]
        m1xdtg[basin,m1x]=(bdtg,edtg)
        m1s[basin,m1x]=md1

        card=open(md1).readline()
        tt=card.split()
        m1lls[basin,m1x]=(float(tt[4]),float(tt[5]))


    def Dll(ll1,ll2):
        d=sqrt( (ll1[0]-ll2[0])*(ll1[0]-ll2[0]) + (ll1[1]-ll2[1])*(ll1[1]-ll2[1]))
        return(d)


    dllmin=0.5
    k9=m9xdtg.keys()
    k1=m1xdtg.keys()

    map9x={}

    for k in k9:
        b9=k[0]
        s9=k[1]
        b9dtg=m9xdtg[k][0]
        ll9=m9lls[k]

        for k in k1:
            b1=k[0]
            s1=k[1]
            b1dtg=m1xdtg[k][1]
            ll1=m1lls[k]
            ddtg=mf.dtgdiff(b9dtg,b1dtg)/24.0
            dll=Dll(ll9,ll1)
            if(b9 == b1 and ddtg >= -4.0 and dll <= dllmin):
                if(verb):
                    print 'kk11 ',' ss ',s9,s1,' bbb ',ddtg,' b9: ',b9dtg,'  b1: ',b1dtg," %5.1f "%dll,ll9,ll1
                map9x[s9]=s1


    return(map9x)

def GetMap9xDtg(dtg,verb=0):

    def Dll(ll1,ll2):
        d=sqrt( (ll1[0]-ll2[0])*(ll1[0]-ll2[0]) + (ll1[1]-ll2[1])*(ll1[1]-ll2[1]))
        return(d)

    tcs=findtcs(dtg)
    ntcs=len(tcs)
    stmids=[]
    posits={}
    
    dllmin=1.0

    map9x={}

    mdll={}

    for tc in tcs:
        tt=tc.split()
        stmid=tt[1]
        lat=float(tt[4])
        lon=float(tt[5])
        stmids.append(stmid)
        posits[stmid]=(lat,lon)

    for stmid in stmids:
        
        if(stmid[0] == '9'):
            ll9x=posits[stmid]
            stmid9x=stmid
            
            for stmid in stmids:
                if(stmid[0] != '9'):
                    ll1x=posits[stmid]
                    dll=Dll(ll9x,ll1x)
                    if(dll < dllmin):
                        map9x[stmid9x]=stmid


    return(map9x)

def FormatLon(flon):

    from math import fabs
    if(flon >= 180.0):
        flon=flon-360.0

    if(flon <= -100.0):
        oflon="%5.1fW"%(fabs(flon))
    elif(flon <= -10.0):
        oflon=" %4.1fW"%(fabs(flon))
    elif(flon <= -0.0):
        oflon="  %3.1fW"%(fabs(flon))
    elif(flon >= 0.0 and flon < 10.0):
        oflon="  %3.1fE"%(fabs(flon))
    elif(flon >= 10.0 and flon < 100.0):
        oflon=" %4.1fE"%(fabs(flon))
    else:
        oflon="%5.1fE"%(fabs(flon))

    return(oflon)

def FormatLat(flat):

    from math import fabs
    if(flat <= 0.0):
        flat=fabs(flat)
        ihemns='S'
    else:
        ihemns='N'

    oflat="%4.1f%s"%(flat,ihemns)
    return(oflat)

#
#  20080507 -- new function to get stmids by dtg for vdeck.py
#
def GetStmidsByDtg(dtg,srcopt='btops'):

    tcs=findtcs(dtg,srcopt=srcopt)
    ntcs=len(tcs)
    stmids=[]
    stmopt=''

    if(ntcs == 1):
        stmid=tcs[0].split()[1]
        stmids.append(stmid)
        stmopt=stmid

    else:
        for n in range(0,ntcs):
            stmid=tcs[n].split()[1]
            stmids.append(stmid)
            if(n == 0):
                stmopt=stmid
            else:
                stmopt="%s,%s"%(stmopt,stmid)

    return(stmids,stmopt)

def chklat(lat):
    rc=0
    if(lat > -88.0 and lat < 88.0):
        rc=1
    return(rc)



def GetBtLatLonVmax(stmid,verb=0):

    bts={}

    stmid=stmid.upper()
    mdcards=findtc(stmid)
    dtgs=mdcards.keys()
    dtgs.sort()
    lastdtg = dtgs[-1]
    btcs=ParseMdeck2Btcs(dtgs,mdcards)

    n=0
    for dtg in dtgs:
        rc=btcs[dtg]
        
        #(blat,blon,bvmax,bpmin,bdir,bspd,btdic,cqdic,bwdic,btr34quad,btr50quad)=

        blat=rc[0]
        blon=rc[1]
        bvmax=rc[2]
        bpmin=rc[3]
        bdir=rc[4]
        bspd=rc[5]
        btdic=rc[6]
        cqdic=rc[7]
        tcflg=btdic[0]
        stflg=btdic[1]
        cqflg=btdic[2]
        wnflg=btdic[3]
        bttype=btdic[len(btdic)-1]
        if(bttype == -1):
            btflg=0
        else:
            btflg=1
            

        if(verb):
            print 'ddddddd ',n,dtg,blat,blon,bvmax,tcflg,stflg,cqflg,wnflg,btflg

        bts[dtg]=[blat,blon,bvmax,bpmin,bdir,bspd,tcflg,stflg,cqflg,wnflg,btflg]
        n=n+1

    return(bts)

def GetBtRadii(stmid,Rs,verb=1):

    bts={}

    mdcards=findtc(stmid)
    dtgs=mdcards.keys()
    dtgs.sort()
    lastdtg = dtgs[-1]
    btcs=ParseMdeck2Btcs(dtgs,mdcards)

    n=0
    for dtg in dtgs:
        
        rc=btcs[dtg]
        
        #(blat,blon,bvmax,bpmin,bdir,bspd,btdic,cqdic,bwdic,btr34quad,btr50quad)
        #btdic=[flgtc,flgind,flgcq,flgwn,tdo,lf,cqlat,cqlon,cqvmax,wlat,wlon,wvmax,tsnum]
        #cqdic=[cqlat,cqlon,cqvmax,cqdir,cqspd,cqpmin]
        #bwdic=[bvmax,r34,r50,rmax,reye,poci,roci]
        #btc=[blat,blon,bvmax,bpmin,bdir,bspd,btdic,cqdic,bwdic,r34quad,r50quad]
        #       0    1     2     3     4   5   6      7     8      9      10
        blat=rc[0]
        blon=rc[1]
        bvmax=rc[2]

        btdic=rc[6]
        flgtc=btdic[0]
        flgind=btdic[1]

        istc=IsTc(flgind)
        
        bwdic=rc[8]
        r34quad=rc[9]
        r50quad=rc[10]

        rmax=bwdic[3]
        reye=bwdic[4]
        
        poci=bwdic[5]
        roci=bwdic[6]
        
        cblon=FormatLon(float(blon))
        lblon=len(str(blon))
        lcblon=len(cblon)

        for r in r34quad:
            if(r > 0 and istc > 0):
                Rs.r34.append(r)

        for r in r50quad:
            if(r > 0 and istc > 0):
                Rs.r50.append(r)

        if(rmax != 999 and istc > 0):
            Rs.rmax.append(rmax)

        btcard="%s  %s  Flgs: %d  Bt: %6.1f %s  Vm: %3.0f"%(stmid,dtg,istc,blat,cblon,bvmax)
        r34card="  R34: % 4d % 4d % 4d % 4d"%(r34quad[0],r34quad[1],r34quad[2],r34quad[3])
        r50card="  R50: % 4d % 4d % 4d % 4d"%(r50quad[0],r50quad[1],r50quad[2],r50quad[3])
        rmaxcard="  Rm: %4.0f Reye: %4.0f"%(rmax,reye)
        pocicard="  P/Roci: %5.0f %5.0f"%(poci,roci)

        r34card=r34card.replace('-999','  - ')
        r50card=r50card.replace('-999','  - ')
        rmaxcard=rmaxcard.replace('999',' - ')
        pocicard=pocicard.replace('9999','  - ')
        pocicard=pocicard.replace('999',' - ')
        
        
        if(verb):
            radcard=btcard+r34card+r50card+rmaxcard+pocicard
            print radcard
            #print 'ddddddd ',n,dtg,blat,blon,bvmax,bwdic,r34quad,r50quad

        bts[dtg]=radcard
        n=n+1

    return(bts)

def ConvertB1Stmid2B2Stmid(b1stmid):

    snum=b1stmid[0:2]
    b1id=b1stmid[2]
    year=b1stmid.split('.')[1]

    b2id=Basin1toBasin2[b1id]

    b2stmid="%s%s%s"%(b2id,snum,year)

    return(b2stmid)


def GetBtcardsLatLonsFromMdeck(stmid,dtg,nhback=48,nhplus=120,verb=0):

    btcards=[]
    btcardsgt0=[]
    
    lats=[]
    lons=[]
    vmaxs=[]
    pmins=[]

    (btdtgs,btcs)=GetMdeckBts(stmid,dofilt9x=0,verb=verb)

    if(btdtgs == None):
        print 'WWW(GetBtcardsLatLonsFromMdeck): no bts for stmid: ',stmid
        return(btcards,None,None,None,None,None)

    
    btdtgs.sort()

    obtdtgs=[]
    obtdtgsgt0=[]
    for btdtg in btdtgs:
        dt=mf.dtgdiff(dtg,btdtg)
        if(dt <= 0 and dt >= -nhback):
            obtdtgs.append(btdtg)
        if(dt >= 0):
            obtdtgsgt0.append(btdtg)
            
            
    btcard="N bt: %d"%(len(obtdtgs))
    btcards.append(btcard)

    for dtg in obtdtgs:

        (blat,blon,bvmax,bpmin,bdir,bspd,btdic,cqdic,bwdic,r34quad,r50quad)=btcs[dtg]
        (flgtc,flgind,flgcq,flgwn,tdo,lf,cqlat,cqlon,cqvmax,wlat,wlon,wvmax,tsnum)=btdic

        flgveri=VeriTcFlag(flgtc,flgwn)

        btcard="%s %6.1f %6.1f %3d %2d %6.0f"%(dtg,blat,blon,int(bvmax),flgveri,bpmin)
        btcards.append(btcard)
        lats.append(blat)
        lons.append(blon)
        vmaxs.append(bvmax)
        pmins.append(bpmin)

    btcardgt0="N bt: %d"%(len(obtdtgsgt0))
    btcardsgt0.append(btcardgt0)

    nbt0=0
    dtg0=obtdtgsgt0[0]
    
    for dtg in obtdtgsgt0:
        dt=mf.dtgdiff(dtg0,dtg)
        if(dt%12): continue
        dhplus=mf.dtgdiff(dtg0,dtg)
        if(dhplus > nhplus): continue

        nbt0=nbt0+1

        (blat,blon,bvmax,bpmin,bdir,bspd,btdic,cqdic,bwdic,r34quad,r50quad)=btcs[dtg]
        (flgtc,flgind,flgcq,flgwn,tdo,lf,cqlat,cqlon,cqvmax,wlat,wlon,wvmax,tsnum)=btdic

        flgveri=VeriTcFlag(flgtc,flgwn)

        btcard="%s %6.1f %6.1f %3d %2d %6.0f"%(dtg,blat,blon,int(bvmax),flgveri,bpmin)
        btcardsgt0.append(btcard)
        lats.append(blat)
        lons.append(blon)
        vmaxs.append(bvmax)
        pmins.append(bpmin)

    # replace nbt with count from culling out tau12 increment
    
    btcardsgt0[0]="N bt: %d"%(nbt0)
    return(btcards,btcardsgt0,lats,lons,vmaxs,pmins)



def stm1to2id(stmid): 
    b1id=stmid[2]
    bnum=stmid[0:2]
    b1year=stmid.split('.')[1]
    
    stm2id="%s%s.%s"%(Basin1toBasin2[b1id].lower(),bnum,b1year)
    return(stm2id)




