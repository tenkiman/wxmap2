from M import *
MF=MFutils()

from tcbase import TcBtNeumannDatDir,TcBtOpsDatDir,TcBtDatDir,TcAdecksFinalDir,eBdeckDir,TcNamesDatDir
from tcbase import AD2dbname,BD2dbname,VD2dbname,MD2dbname
from TCtrk import tcgenModelsJS

YearsBackClimo=32
YearsBackClimoTss=[4,8,16,32]

YearsBackClimo=48
YearsBackClimoTss=[4,8,16,32,48]
byearClimo=1970
eyearClimo=2000

byearClimo=1981
eyearClimo=2010

YearTcBtNeumann=1944

icharA=97
undef=-999
maxNNnum=60
maxNNnum=49 # -- 20140515 -- NHC fooling with these numbers

# tc parameters/limits
#
TCvmin=25.0
#TCvmin=30.0

vmaxTS=35.0
vmaxTY=65.0

IPerror=15.0 # nmi

ddtgTrack=6

Basin1toBasin2 = {
    'A':'IO',
    'B':'IO',
    'L':'AL',
    'I':'IO',
    'S':'SH',
    'P':'SH',
    'H':'SH', # -- to handle both s and p for shem
    'W':'WP',
    'C':'CP',
    'E':'EP',
    'Q':'SL',
    'T':'SA',
    'X':'XX',
}

Basin1toHemi = {
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
    'T':'shem',
    'H':'shem',
    'X':'XXXX',
}

Basin1toFullBasin = {
    'A':'nio',
    'B':'nio',
    'L':'lant',
    'I':'nio',
    'S':'shem',
    'H':'shem',
    'P':'shem',
    'W':'wpac',
    'C':'cpac',
    'E':'epac',
    'Q':'slant',
    'T':'slant',
    'X':'XXXXX',
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
    'AA':'A',
    'XX':'X',
    # -- default in gettrk_gen.x  how he handles 'I' storms...
    'HC':'I',
}


ClimoBasinsHemi = {
    'NHS':['nhem','wpac','epac','lant','nio','shem','global'],
    'SHS':['shem','sio','swpac','nhem','global'],
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
    'H':'SH',
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

Basin1toHemi1 = {
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
    'T':'slt',
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


TcGenBasin2Area={
    'lant':'troplant',
    'epac':'tropepac',
    'wpac':'tropwpac',
    'shem':'tropshem',
    'nio':'tropnio',
}

TcGenBasin2PrwArea={
    'lant':'prwLant',
    'epac':'prwEpac',
    'cepac':'prwCEpac',
    'wpac':'prwWpac',
    'shem':'prwSpac',
    'nio':'prwIo',
}

TcGenBasin2B1ids={
    'lant':['l'],
    'epac':['c','e'],
    'wpac':['w'],
    'shem':['s','p'],
     'nio':['a','b'],
}


tdmin=25.0
tsmin=35.0
tymin=65.0
stymin=130.0

peakNhemMMDDHH='090100'
peakShemMMDDHH='021500'

#primeMeridianChk=60.0 -- too big for AS, e.g., 01A.12
primeMeridianChk=30.0

centerid='MFTC'
tcVcenterid='M2TC'


opsaids={}

opsaids['jtwc']=['jtwc','jtwi','c120','clip','clim','conw','mbam','wbar','xtrp']
opsaids['nhc']=['ofcl','ofci','clp5','clip','clim','xtrp','tvcn']




#uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu
# new unbounded methods


def scaledTC(vmax):


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
    if(vmax >= tsmin):
        ace=vmax*vmax
    else:
        ace=0.0
    return(ace)


def TCType(vmax):

    if(vmax <= 34): tctype='TD'
    if(vmax >= 35 and vmax <= 63): tctype='TS'
    if(vmax >= 64 and vmax <= 129): tctype='TY'
    if(vmax >= 130): tctype='STY'
    return(tctype)


def getSaffirSimpsonCat(vmax):

    if(vmax < 35.0): cat='TD'
    if(vmax >= 35.0 and vmax < 65.0): cat='TS'
    if(vmax >= 64.0 and vmax <= 82.0): cat='HU1'
    if(vmax >= 83.0 and vmax <= 95.0): cat='HU2'
    if(vmax >= 96.0 and vmax <= 113.0): cat='HU3'
    if(vmax >= 114.0 and vmax <= 135.0): cat='HU4'
    if(vmax > 135.0): cat='HU5'
    return(cat)


def getTyphoonCat(vmax):

    if(vmax < 35.0): cat='td'
    if(vmax >= 35.0 and vmax < 65.0): cat='ts'
    if(vmax >= 64.0 and vmax < 100.0): cat='ty'
    if(vmax >= 100.0 and vmax < 135.0): cat='Mty'
    if(vmax >= 135.0): cat='STY'
    return(cat)


def b1idTob2id(b1id):
    b2id=Basin1toBasin2[b1id.upper()].lower()
    b2id=b2id.lower()
    return(b2id)


def b2idTob1id(b2id):
    b1id=Basin2toBasin1[b2id.upper()].lower()
    b1id=b1id.lower()
    return(b1id)


def stm1idTostm2id(stm1id):

    b1id=stm1id[2].upper()
    snum=stm1id[0:2]
    b2id=Basin1toBasin2[b1id]
    stm2id=b2id + snum + '.'+stm1id.split('.')[1]
    stm2id=stm2id.lower()
    return(stm2id)


def stm2idTostm1id(stm2id):

    ss=stm2id.split('.')
    sid=ss[0]
    syear=ss[1]

    b2id=sid[0:2].upper()
    if(mf.find(sid,'cc')):
        snum='CC'+sid[-3:]
    else:
        snum=sid[2:4]

    b1id=Basin2toBasin1[b2id]
    stm1id=snum + b1id + '.'+syear
    return(stm1id)



def basin2Chk(b2id):
    """
    convert local b2id to standard atcf b2id
    """

    if(b2id == 'SI' or b2id == 'SP' or b2id == 'SL'):
        b2id='SH'

    elif(b2id == 'AA' or b2id == 'BB' or b2id == 'NI' or b2id == 'NA'):
        b2id='IO'

    elif(b2id == 'AT'):
        b2id='AL'

    return(b2id)


def getShemYear(dtg):
    """
     convert year in stm dtg to basinyear
    """

    yyyy=int(dtg[0:4])
    mm=int(dtg[4:6])

    if(mm >= 7): yyyy=yyyy+1
    cyyyy=str(yyyy)
    return(cyyyy)

def getNhemYears(dtg):
    """
     get nhem years for case of storm crossing new year
    """

    year1=dtg[0:4]
    dtgnhemMax=year1+'011500'
    dtnhem=mf.dtgdiff(dtg,dtgnhemMax)
    year2=year1
    if(dtnhem >= 0.0): year2=str(int(year1)-1)
    years=[year2,year1]
    return(years)

def getNhemYearsInt(dtg,mmddhh='011500'):
    """
     get nhem years for case of storm crossing new year as Int
    """

    year1=dtg[0:4]
    dtgnhemMax=year1+mmddhh
    dtnhem=mf.dtgdiff(dtg,dtgnhemMax)
    year1=int(year1)
    year2=year1
    if(dtnhem >= 0.0): year2=year2-1
    rc=0
    if(year2 != year1):rc=1
    years=[year2,year1]
    return(rc,years)

def getNhemShemYearsFromDtg(dtg):
    """
get years for a dtg to handle two situations nhem storms crossing new year
shem storms 070100-123118
"""
    (rcnhem,nhemyears)=getNhemYearsInt(dtg)
    shemyear=int(getShemYear(dtg))
    
    if(rcnhem):
        rc=1
        year=nhemyears[0]
        shemyear=nhemyears[1]
    else:
        rc=2
        year=nhemyears[0]
        if(year == shemyear): rc=0
        
    return(rc,year,shemyear)
    


def getIoShemB1idFromRlon(b2id,rlon):

    b1id='X'

    if(b2id.upper() == 'SH'):
        if(rlon <= 135.0):
            b1id='S'
        else:
            b1id='P'


    if(b2id.upper() == 'IO'):
        if(rlon >= 76.0 and rlon <= 110.0):
            b1id='B'
        else:
            b1id='A'

    if(b1id == 'X'):
        print 'EEE in tc2.getIoShemB1idFromRlon(b2id,rlon) ',b2id,rlon
        sys.exit()


    return(b1id)



def isShemBasinStm(stmid):

    tt=stmid.split('.')
    stmid=tt[0]

    if(len(stmid) > 4):
        return(-1)

    if(len(stmid) == 1):
        ustmid=stmid.upper()
    elif(len(stmid) == 2):
        ustmid=stmid.upper()
    elif(len(stmid) == 3):
        ustmid=stmid[2].upper()
    elif(len(stmid) == 4):
        ustmid=stmid[0:2].upper()

    if(len(ustmid) == 1):
        if(ustmid == 'S' or ustmid == 'P' or ustmid == 'Q' or ustmid == 'H'):
            return(1)
        else:
            return(0)
    elif(len(ustmid) == 2):
        if(ustmid == 'SH' or ustmid == 'SP' or ustmid == 'SI' or ustmid == 'SL'):
            return(1)
        else:
            return(0)

def isIOBasinStm(stmid):

    tt=stmid.split('.')
    stmid=tt[0]

    if(len(stmid) > 4):
        return(-1)

    if(len(stmid) == 1):
        ustmid=stmid.upper()
    elif(len(stmid) == 2):
        ustmid=stmid.upper()
    elif(len(stmid) == 3):
        ustmid=stmid[2].upper()
    elif(len(stmid) == 4):
        ustmid=stmid[0:2].upper()

    if(len(ustmid) == 1):
        if(ustmid == 'I' or ustmid == 'A' or ustmid == 'B'):
            return(1)
        else:
            return(0)
    elif(len(ustmid) == 2):
        if(ustmid == 'IO' or ustmid == 'BB' or ustmid == 'AA'):
            return(1)
        else:
            return(0)


def GetTCnamesHash(yyyy,source=''):
    
    from tcbase import TcNamesDatDir
    ndir=TcNamesDatDir
    sys.path.append(ndir)
    if(source == 'neumann'):
        impcmd="from TCnamesNeumann%s import tcnames"%(yyyy)
    else:
        impcmd="from TCnames%s import tcnames"%(yyyy)
    exec(impcmd)
    return(tcnames)

def isIoShemSubbasin(stm1id,stm2id,convertAlpha=0):

    # -- if [A-Z][0-9] 9x comes in, convert
    #
    chkstm1id=stm1id

    # -- really want to do this?
    #
    if(stm1id[0].isalpha() and convertAlpha):
        chkstm1id='9'+stm1id[1:]
        chkstm1id=chkstm1id.upper()

    rc=0
    bnum=(chkstm1id[0:2] == stm2id[0:2])
    b1id=(
        (chkstm1id[2] == 'S' and (stm2id[2] == 'S' or stm2id[2] == 'P')) or
        (chkstm1id[2] == 'I' and (stm2id[2] == 'A' or stm2id[2] == 'B'))
    )

    if(bnum and b1id): rc=1

    return(rc)

def isIoShemSubbasinStm1id(stm1id):
    """ only look for uniq b1id
"""
    rc=0
    b1id=stm1id[2].upper()
    btest=( (b1id == 'A' or b1id == 'B' or b1id == 'P') )
    if(btest): rc=1

    return(rc)

def isIoShemSubbasinB1id(b1id):

    rc=0
    goodb1id=(
        (b1id == 'A' or b1id == 'B' or b1id == 'P')
    )
    if(goodb1id): rc=1

    return(rc)

def getFinalStm1idFromStmids(tstmid,stmids):
    """ handle stmids from adecks with 2-char basins -> 1-char basin by comp of 1-char subbasin in io/shem"""
    
    ostmid=tstmid
    for stmid in stmids:
        if(isIoShemSubbasin(tstmid,stmid)):
            ostmid=stmid
            continue
    return(ostmid)


def GetTCstatsHash(yyyy,source=''):

    ndir=TcNamesDatDir
    sys.path.append(ndir)
    if(source == 'neumann'):
        impcmd="from TCstatsNeumann%s import tcstats"%(yyyy)
    elif(source == 'ops'):
        impcmd="from TCstatsOps%s import tcstats"%(yyyy)
    else:
        impcmd="from TCstats%s import tcstats"%(yyyy)
    exec(impcmd)
    return(tcstats)

def basin2Chk(b2id):
    """
    convert local b2id to standard atcf b2id
    """

    if(b2id == 'SI' or b2id == 'SP' or b2id == 'SL'):
        b2id='SH'

    elif(b2id == 'AA' or b2id == 'BB' or b2id == 'NI' or b2id == 'NA'):
        b2id='IO'

    elif(b2id == 'AT'):
        b2id='AL'

    return(b2id)




def Clatlon2Rlatlon(clat,clon):

    if(len(clat) == 1):
        return(0.0,0.0)

    hemns=clat[len(clat)-1:]
    hemew=clon[len(clon)-1:]
    if(mf.find(clat,'.')):
        rlat=float(clat[0:(len(clat)-1)])
    else:
        ilat=clat[0:(len(clat)-1)]
        rlat=int(ilat)*0.1
        
    if(mf.find(clon,'.')):
        rlon=float(clon[0:(len(clon)-1)])
    else:
        ilon=clon[0:(len(clon)-1)]
        rlon=int(ilon)*0.1

    if(hemns == 'S'):
        rlat=-rlat

    if(hemew == 'W'):
        rlon=360.0-rlon

    return(rlat,rlon)

def Clatlon2RlatlonFull(clat,clon):

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



def Rlatlon2ClatlonFull(rlat,rlon,dotens=1):

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



def Rlatlon2Clatlon(rlat,rlon,dotens=1,dodec=0,dozero=0):

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
            rlat=abs(rlat)

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
        clat="%3d%s"%(ilat,hemns)
        clon="%4d%s"%(ilon,hemew)
        if(dozero):
            clat="%03d%s"%(ilat,hemns)
            clon="%04d%s"%(ilon,hemew)
    else:
        if(dozero):
            clat="%02d%s"%(ilat,hemns)
            clon="%03d%s"%(ilon,hemew)
        else:
            clat="%02d%s"%(ilat,hemns)
            clon="%03d%s"%(ilon,hemew)

    if(dodec):
        clat="%5.1f%s"%(rlat,hemns)
        clon="%5.1f%s"%(rlon,hemew)

    return(clat,clon)


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

def gc_dist(rlat0,rlon0,rlat1,rlon1,tcunits=tcunits):

    # -- based on the spherical law of cosines 
    #

    dlat=abs(rlat0-rlat1)
    dlon=abs(rlon0-rlon1)
    if(dlon == 360.0): dlon=0.0
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


def dist_err(blat,blon,blat1,blon1,flat,flon,tcunits=tcunits):

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



def VeriTcFlag(tcind,tcwarn):
    vflg=0
    if(tcind == 'TC' or tcwarn == 'WN'):
        vflg=1

    return(vflg)


def getB2idSnumFromPath(dpath,filter=1):
    (dir,file)=os.path.split(dpath)
    b2id=file[1:3]
    snum=file[3:5]
    year=file[5:9]
    if(filter):
        if(snum[0].isalpha()):
            snum1=int(snum[1])
            snum=90+snum1
        else:
            snum=int(snum)
            if(snum >= 80 and snum <= 89): snum=-1


    stm2id="%s%02d.%s"%(b2id,snum,year)
    (snum,sb1id,syear,sb2id,stm2id,stm1id)=getStmParams(stm2id)
    snum=int(snum)
    return(b2id,snum,stm1id,stm2id)


def IsJtwcBasin(b1id):

    bid=b1id.lower()
    if(len(bid) == 1):
        bid=b1id.lower()
    elif(len(bid) >= 3):
        # assume stmid if not 1char
        tt=b1id.split('.')
        bid=tt[0][2].lower()

    rc=0
    if(len(bid) == 1  and
       bid == 'w' or bid == 'b' or bid == 'a' or  bid == 'i' or
       bid == 's' or bid == 'p'
       ):
        rc=1

    # overlap
    #
    elif(len(bid) == 1  and
         bid == 'e' or bid == 'c'
         ):
        rc=2

    elif(len(bid) == 2 and
         bid == 'wp' or bid == 'io' or bid == 'sh'):
        rc=1

    # overlap
    #
    elif(len(bid) == 2 and
         bid == 'ep' or bid == 'cp'):
        rc=2

    return(rc)

def IsNhcBasin(b1id):

    bid=b1id.lower()

    if(len(bid) == 1):
        bid=b1id.lower()
    elif(len(bid) >= 3):
        # assume stmid if not 1char
        tt=b1id.split('.')
        bid=tt[0][2].lower()

    rc=0
    if(len(bid) == 1 and
       bid == 'l' or bid == 'e' or bid == 'c' or bid == 'q'
       ):
        rc=1
    elif(len(bid) == 2 and
         bid == 'al' or bid == 'ep' or bid == 'cp' or bid == 'sl'
         ):
        rc=1

    return(rc)

def IsIoShemBasin(b1id):

    bid=b1id.lower()

    if(len(bid) == 1):
        bid=b1id.lower()
    elif(len(bid) >= 3):
        # assume stmid if not 1char
        tt=b1id.split('.')
        bid=tt[0][2].lower()

    rc=0
    if(len(bid) == 1 and
       bid == 'i' or bid == 'a' or bid == 'b' or bid == 's' or bid == 'p'
       ):
        rc=1
    elif(len(bid) == 2 and
         bid == 'io' or bid == 'aa' or bid == 'bb' or bid == 'sh' or bid == 'si' or bid == 'sp'
         ):
        rc=1

    return(rc)

def IsIoSubBasin(b1id):

    bid=b1id.lower()

    if(len(bid) == 1):
        bid=b1id.lower()
    elif(len(bid) >= 3):
        # assume stmid if not 1char
        tt=b1id.split('.')
        bid=tt[0][2].lower()

    rc=0
    if(len(bid) == 1 and
       bid == 'i' or bid == 'a' or bid == 'b'
       ):
        rc=1
    elif(len(bid) == 2 and
         bid == 'io' or bid == 'aa' or bid == 'bb' 
         ):
        rc=1

    return(rc)

def IsShemSubBasin(b1id):

    bid=b1id.lower()

    if(len(bid) == 1):
        bid=b1id.lower()
    elif(len(bid) >= 3):
        # assume stmid if not 1char
        tt=b1id.split('.')
        bid=tt[0][2].lower()

    rc=0
    if(len(bid) == 1 and
       bid == 's' or bid == 'p'
       ):
        rc=1
    elif(len(bid) == 2 and
         bid == 'si' or bid == 'sp'
         ):
        rc=1

    return(rc)

def IsNhemBasin(b1id):

    bid=b1id.lower()

    if(len(bid) == 1):
        bid=b1id.lower()
    elif(len(bid) >= 3):
        # assume stmid if not 1char
        tt=b1id.split('.')
        bid=tt[0][2].lower()

    rc=0
    if(len(bid) == 1 and
       bid == 'i' or bid == 'a' or bid == 'b' or bid == 'w' or bid == 'e' or bid == 'l'  or bid == 'c'
       ):
        rc=1
    elif(len(bid) == 2 and
         bid == 'io' or bid == 'aa' or bid == 'bb' or bid == 'wp' or bid == 'ep' or bid == 'al' or bid == 'cp'
         ):
        rc=1

    return(rc)


def get9XstmidFromNewForm(stmid9x):
    (snum,b1id,year,b2id,stm2id,stm1id)=getStmParams(stmid9x)
    if(snum[0:2].upper() == 'XX'):
        stmid9x='XXX'+'.XXXX'
        stmid9x='___.____'
        stmid9x='XX%s.%s'%(b1id,year)
    elif(snum[0].isalpha()):
        stmid9x='9'+snum[1:]+b1id+'.'+year
    return(stmid9x)

def getStmSiz(stmSiz,stmSizMin=257):
    
    rc=0
    ntrk=len(stmSiz)
    nsiz=0
    for sstm in stmSiz:
        ss=sstm.split('.')
        sz=int(ss[-1])
        st=0
        if(sz > stmSizMin): nsiz=nsiz+sz

    if(ntrk > 0 and nsiz > 0):rc=1
    if(ntrk > 0 and nsiz == 0): rc=-2
    
    ostmSiz=stmSiz
    if(rc == -2):
        ostmSiz=[]
        for ss in stmSiz:
            ss=ss.strip()
            ss=ss+'-NOOOOOOOLOAD'
            ostmSiz.append(ss)
        
    return(rc,ostmSiz)


def getStmParams(stmid,convert9x=0):

    istmid=stmid
    if(convert9x): istmid=get9XstmidFromNewForm(stmid)

    tt=istmid.split('.')

    # -- case of genesis stmid tgNNNNN
    #
    if(len(tt) == 1):
        year=-9999
        snum='-99'
        b1id='X'
        b2id='XX'
        stm2id='NNXX.YYYY'
        stm1id='NNX.YYYY'
        if(istmid[0:2] == 'tg'):     snum='-1'
        
        return(snum,b1id,year,b2id,stm2id,stm1id)

    else:
        year=tt[1]

    if(len(tt[0]) == 4):
        snum=istmid[2:4]
        b2id=istmid[0:2]
        b1id=Basin2toBasin1[b2id.upper()]
        stm2id=istmid
    elif(len(tt[0]) == 7):
        snum=istmid[4:7]
        b2id=istmid[0:2].lower()
        b1id=Basin2toBasin1[b2id.upper()]
        stm2id=b2id+'cc'+snum+'.'+year
    elif(len(tt[0]) == 6):
        snum=istmid[2:5]
        b1id=istmid.split('.')[0][-1]
        b2id=Basin1toBasin2[b1id.upper()]
        stm2id=b2id+'cc'+snum+'.'+year
        stm2id=stm2id.lower()
    else:
        snum=istmid[0:2]
        b1id=istmid[2]
        b2id=Basin1toBasin2[b1id.upper()]
        stm2id=b2id+snum+'.'+year
        stm2id=stm2id.lower()

    stm1id=snum+b1id+'.'+year

    return(snum,b1id,year,b2id,stm2id,stm1id)



def Is9X(stmid):
    rc=0
    (snum,b1id,year,b2id,stm2id,stm1id)=getStmParams(stmid)
    if((snum[0].isalpha() and int(snum[1]) >=0 and int(snum[1]) <= 9) or
       (snum.isdigit() and (int(snum) >= 90 and int(snum) <= 99) )
       ):
        rc=1

    return(rc)

def areStmids9X(stmids):
    rc=1
    for stmid in stmids:
        if(IsNN(stmid)): 
            rc=0
            return(rc)

    return(rc)

def Is9Xstmopt(stmopt):
    
    tt=stmopt.split(',')
    if(len(tt) > 1):
        frc=0
        for t in tt:
            if(len(t) == 1):
                rc=0
                return(rc)
            else:
                trc=Is9Xstmopt(t)
            frc=frc+trc
            
        if(frc == len(tt)): 
            rc=1
        else:
            rc=0
            
        return(rc)
        
    rc=0
    snum=stmopt.split('.')[0]
    if(len(snum) != 3): return(rc)
    
    snum=snum[0:2]
    if((snum[0].isalpha() and int(snum[1]) >=0 and int(snum[1]) <= 9) or
       (snum.isdigit() and (int(snum) >= 90 and int(snum) <= 99) ) or
       (snum[0] == '9' and snum[1] == 'x')
       ):
        rc=1

    return(rc)


def Is9XSnum(snum):
    rc=0
    if(snum.isdigit() and (int(snum) >= 90 and int(snum) <= 99) ): rc=1
    return(rc)


def IsNN(stmid):
    rc=0
    (snum,b1id,year,b2id,stm2id,stm1id)=getStmParams(stmid)
    if(
        (snum.isdigit() and (int(snum) >= 1 and int(snum) <= maxNNnum) )
        ):
        rc=1
    return(rc)

def IsValidStmid(stmid):
    rc=0
    (snum,b1id,year,b2id,stm2id,stm1id)=getStmParams(stmid)
    rc=(IsNN(stmid) or Is9X(stmid) or int(snum) == -1)
    return(rc)

def IsTc(tcstate):
    #
    # if tc = 1
    # if stc = 2
    # if neither = 0
    # if undefined = -1
    #
    tcstate=tcstate.upper()

    if(
        tcstate == 'TD' or
        tcstate == 'TS' or
        tcstate == 'TY' or
        tcstate == 'HU' or
        tcstate == 'ST' or
        tcstate == 'TC' 
        #or tcstate == 'TW' no -- this is a Tropical Wave
        ):
        tc=1
    elif(
        tcstate == 'SS' or
        tcstate == 'SD'
        ):
        tc=2
    elif(
        tcstate == 'EX'
        ):
        tc=3
    elif(
        tcstate.lower() == 'xx' or
        tcstate == '  ' or
        len(tcstate) == 0
        ):
        tc=-1
    else:
        tc=0

    return(tc)

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
        dtg=tt[0]
        stmid=tt[1]
        vmax=int(tt[2])
        tcstate=tt[13]
        warnstate=tt[15]
    except:
        try:
            dtg=tt[0]
            stmid=tt[1]
            vmax=int(tt[2])
            tcstate=tt[12]
            warnstate=tt[14]
        except:
            dtg=stmid=b1id=None
            vmax=0
            tcstate='xx'

    if(vmax >= TCvmin and (tcstate.lower() == 'xx' )): tcstate='TC'

    tc=IsTc(tcstate)
    # -- if warnings and still not a TC call it a TC
    #
    if(stmid != None): 
        b1id=stmid[2]
        shemio=isIoShemSubbasinB1id(b1id)
    
    if(not(tc) and IsWarn(warnstate) and not(shemio)):
        print 'WWWTTTCCC stm: ',stmid,'is NOT a TC but warnings...call it a TC on',dtg,b1id,shemio
        tc=1
    

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


def add2000(y):
    if(len(y) == 1):
        yyyy=str(2000+int(y))
    elif(len(y) == 2):
        if(int(y) > 25):
            yyyy=str(1900+int(y))
        else:
            yyyy=str(2000+int(y))
    else:
        yyyy=y
    return(yyyy)


def getyears(yyy):

    if(yyy == 'cur'):
        curdtg=mf.dtg()
        yyy=curdtg[0:4]

    years=[]
    n1=0
    n2=0

    tt0=yyy.split('-')
    tt1=yyy.split(',')

    if(len(tt1) > 1):
        for tt in tt1:
            yyyy=add2000(tt)
            years.append(yyyy)
        return(years)

    if(len(tt0) > 1):
        y1=tt0[0]
        y2=tt0[1]
        yyyy1=add2000(y1)
        yyyy2=add2000(y2)

        if(len(yyyy1) != 4 or len(yyyy2) != 4):
            print 'EEEE getyears tt:',tt
            return(None)

        else:
            n1=int(yyyy1)
            n2=int(yyyy2)
            for n in range(n1,n2+1):
                years.append(str(n))

    else:
        if(len(yyy) <= 2): yyy=add2000(yyy)
        years=[yyy]

    return(years)

def getAdeckYearBasinFromPath(adeckpath):
    import os
    """recover 2-char basin id and year from adeck path"""
    adyear=None
    adbasin=None
    (dir,file)=os.path.split(adeckpath)
    (base,ext)=os.path.splitext(file)
    # -- check if standard adeck file name a??NNYYYY.dat
    #
    if( (ext.lower() == '.dat') and (len(base) == 9) ):
        adyear=base[-4:]
        adbasin=base[1:3]
    return(adyear,adbasin)
    
    
    

def Relabel9xAcards(ac,stmid):

    oacards={}

    stmnum=stmid[0:2]
    for dtg in ac.dtgs:
        ocards=[]
        for card in ac.acards[dtg]:
            snum=card[4:6]
            ocard=card
            if(snum != stmnum):
                ocard=ocard[0:4]+stmnum+ocard[6:]
            ocards.append(ocard)

        oacards[dtg]=ocards

    ac.acards=oacards
    return(ac)


def MakeStmListABdecks(stmopt,yearopt=None,dofilt9x=0,verb=1):

    from w2local import W2
    w2=W2()

    def getabstmids(b2id,byear):

        stmids=[]

        # == 2 if overlap
        #
        if(IsJtwcBasin(b2id) == 1):
            abdir=w2.TcAdecksJtwcDir
            bbdir=w2.TcBdecksJtwcDir

        elif(IsNhcBasin(b2id)):
            abdir=w2.TcAdecksNhcDir
            bbdir=w2.TcBdecksNhcDir

        amask9="%s/%s/a%s[a-z][0-9]%s.dat"%(abdir,byear,b2id,byear)
        bmask9="%s/%s/b%s[a-z][0-9]%s.dat"%(bbdir,byear,b2id,byear)

        if(dofilt9x == 1):
            amask="%s/%s/a%s[0-5][0-9]%s.dat"%(abdir,byear,b2id,byear)
            bmask="%s/%s/b%s[0-5][0-9]%s.dat"%(bbdir,byear,b2id,byear)
            amask9=bmask9=None
        else:
            amask="%s/%s/a%s??%s.dat"%(abdir,byear,b2id,byear)
            bmask="%s/%s/b%s??%s.dat"%(bbdir,byear,b2id,byear)


        if(verb):
            print 'AAAAAAAAAAAAAAAAAAAA MakeStmListABdecks: ',amask
            print 'BBBBBBBBBBBBBBBBBBBB MakeStmListABdecks: ',bmask

            print 'AAAAAAAAAA9999999999 MakeStmListABdecks: ',amask9
            print 'BBBBBBBBBB9999999999 MakeStmListABdecks: ',bmask9


        apaths=glob.glob(amask)

        if(amask9 != None):
            apaths=apaths+glob.glob(amask9)


        apaths.sort()

        bpaths=glob.glob(bmask)
        if(bmask9 != None):
            bpaths=bpaths+glob.glob(bmask9)

        bpaths.sort()

        for bpath in bpaths:
            if(verb): print 'tcVM.MakeStmListABdecks-bpath: ',bpath
            (dir,file)=os.path.split(bpath)
            snum=file[3:5]

            if(snum[0].isalpha()):
                inum=90+int(snum[1])
                print 'AAAAAAAAAAAAAAAAAA bypass [A-Z][0-9] bpath: ',bpath
                continue
            try:
                inum=int(snum)
            except:
                inum=999
            if(inum >= 80 and inum <= 89):
                print '8888888888888 bypass 8X storm file: ',file
                continue
            byear=file[5:9]
            #stmid=snum+b1id.lower()+'.'+byear
            stmid=snum+b1id.upper()+'.'+byear
            stmids.append(stmid)

            stmids=mf.uniq(stmids)
            stmids.reverse()

        return(stmids)


    if(stmopt != None):
        ss=stmopt.split(',')
        tt=stmopt.split('.')

    elif(stmopt == None):
        tt=[]
        sopt='w,e,c,l,i,a,b,p,s'
        if(yearopt == None):
            byear=mf.dtg()[0:4]
        else:
            byear=yearopt
        ss=sopt.split(',')
        
    if(len(ss) > 1):
        stmids=[]
        for s in ss:
            b1id=s.upper()
            b2id=Basin1toBasin2[b1id].lower()
            stmids=stmids+getabstmids(b2id,byear)
        return(stmids)


    if(len(tt) == 2 or len(tt) == 1):

        if(len(tt) == 1):
            ss=tt[0]
            byear=mf.dtg()[0:4]
        else:
            ss=tt[0]
            byear=tt[1]
            
        if(len(byear) <= 2): byear=add2000(byear)

        if(len(ss) == 1):
            b1id=ss.upper()
            b2id=Basin1toBasin2[b1id].lower()
            stmids=getabstmids(b2id,byear)
        elif(len(ss) == 3):
            b1id=ss[-1].upper()
            b2id=Basin1toBasin2[b1id].lower()
            stmids=getabstmids(b2id,byear)
            tstmid="%s.%s"%(stmopt.split('.')[0].upper(),byear)
            if(tstmid in stmids):
                stmids=[tstmid]
        else:
            stmids=None

        return(stmids)









def MakeStmList(stmopt,yearopt=None,dofilt9x=0,verb=0):

    def getyears(yyy):

        if(yyy == 'cur'):
            curdtg=mf.dtg()
            yyy=curdtg[0:4]

        years=[]
        n1=0
        n2=0

        tt0=yyy.split('-')
        tt1=yyy.split(',')

        if(len(tt1) > 1):
            for tt in tt1:
                yyyy=add2000(tt)
                years.append(yyyy)
            return(years)

        if(len(tt0) > 1):
            y1=tt0[0]
            y2=tt0[1]
            yyyy1=add2000(y1)
            yyyy2=add2000(y2)

            if(len(yyyy1) != 4 or len(yyyy2) != 4):
                print 'EEEE getyears tt:',tt
                return(None)

            else:
                n1=int(yyyy1)
                n2=int(yyyy2)
                for n in range(n1,n2+1):
                    years.append(str(n))

        else:
            if(len(yyy) <= 2): yyy=add2000(yyy)
            years=[yyy]

        return(years)


    def getstmids(sss,year,dofilt9x=dofilt9x):

        sids=[]
        n1=0
        n2=0
        tt=sss.split('-')

        if(len(tt) > 1):
            if(len(tt[0]) != 2 or len(tt[1]) != 3):
                print 'EEEE getstmids tt:',tt
                return(None)

            else:
                n1=int(tt[0])
                n2=int(tt[1][0:2])
                bid=tt[1][2].upper()

                for n in range(n1,n2+1):
                    sid="%02d%1s.%s"%(n,bid,year)
                    sids.append(sid)

        elif(len(sss) == 1):

            tcnames=GetTCnamesHash(year)
            bchk=sss.upper()

            for tcname in tcnames:
                # -- improved subbasin checking...
                #
                tcsubbasin=tcname[1][2:3]
                chk1=(tcsubbasin == bchk)
                chk2=(isIOBasinStm(tcsubbasin) and isIOBasinStm(bchk))
                chk3=(isShemBasinStm(tcsubbasin) and isShemBasinStm(bchk))
                if(chk1 or chk2 or chk3):
                    sid="%s.%s"%(tcname[1],tcname[0])
                    sids.append(sid)
                else:
                    sid=None
                    
        elif(len(tt) == 1):

            if(len(sss) == 3):
                if(sss[0].upper() == 'M'):
                    nback=int(sss[1])
                    bchk=sss[2].upper()
                    tcnames=GetTCnamesHash(year)
                    for tcname in tcnames:
                        if(tcname[1][2:3] == bchk):
                            sid="%s.%s"%(tcname[1],tcname[0])
                            sids.append(sid)
                        else:
                            sid=None

                    sids.sort()
                    osids=[]

                    nsids=len(sids)
                    for n in range(nsids-nback,nsids):
                        osids.append(sids[n])

                    return(osids)

                elif(mf.find(sss[0:2].lower(),'9x')):

                    # -- turn off dofilt9x if here...
                    if(dofilt9x): print 'WWW(tcVM.MakeStmList) -- dofilt9x=1 but you want 9X stmids...set dofilt9x=0'
                    for n in range(90,100):
                        sid="%2d"%(n) + sss[2].upper() + '.'+year
                        sids.append(sid)
                    

                else:

                    sid="%s.%s"%(sss.upper(),year)
                    sids.append(sid)



        else:
            print 'EEEE getstmids sss:',sss
            return(None)


        sids.sort()
        return(sids)

    #
    # start.......................
    #

    curdtg=mf.dtg()
    curyear=curdtg[0:4]

    #
    # single storm
    #

    if(stmopt == None):

        sopt='w,e,c,l,i,a,b,p,s'
        if(yearopt == None):
            yopt='cur'
        else:
            yopt=yearopt
        years=getyears(yopt)

    elif(stmopt != None and stmopt != 'all'):

        ttt=stmopt.split('-')
        ttc=stmopt.split(',')
        tt=stmopt.split('.')
        
        if(len(tt) == 1 and len(ttt) == 1 and len(ttc) == 1):
            if(len(tt[0]) == 3):
                stmid=tt[0][2]
            elif(len(tt[0]) != 1):
                print 'tcVM.MakeStmList() EEEE bad stm3id: tt:',tt,'ttt: ',ttt,'ttc: ',ttc,'stmopt: ',stmopt
                sys.exit()
            else:
                stmid=tt[0]

            if(isShemBasinStm(stmid)):
                stmyear=getShemYear(curdtg)
            else:
                stmyear=curyear

            if(isIOBasinStm(stmid)):
                stmyear=curyear
                
            stmyear=add2000(stmyear)

            stmopt=stmopt+'.'+stmyear
            tt=stmopt.split('.')
            
        #
        # stm spanning using current year
        #

        elif(len(ttt) > 1 and len(ttc) == 1 and len(tt) == 1):

            stmids=getstmids(stmopt,curyear,dofilt9x)
            return(stmids)

        #
        # list of individual stmid (sss.y)
        #

        if(len(ttc) > 1):

            stmids=[]
            for stmopt in ttc:
                stmids=stmids+MakeStmList(stmopt,dofilt9x=dofilt9x,
                                          verb=verb)

            return(stmids)


        if(len(ttc) > 1 and len(tt) > 2):

            stmids=[]

            for stmid in ttc:
                ss1=stmid.split('.')
                if(len(ss1) != 2):
                    print 'EEE invalid individual stm: ',stmmid
                    sys.exit()

                sid=ss1[0]
                yid=ss1[1]
                if(len(yid) >= 1): yid=add2000(yid)
                rc=getstmids(sid,yid,dofilt9x)
                stmids=stmids+rc

            return(stmids)

        sopt=tt[0]
        yopt=tt[1]
        years=getyears(yopt)

    else:

        sopt='w,e,c,l,i,a,b,p,s'
        if(yearopt == None):
            yopt='cur'
        else:
            yopt=yearopt
        years=getyears(yopt)


    if(verb):
        print '(tcbase.makeStmList) sopt: ',sopt
        print '(tcbase.makeStmList) yopt: ',yopt,years


    stmids=[]

    for year in years:

        ss=sopt.split(',')
        if(len(ss) > 1):
            for sss in ss:
                rc=getstmids(sss,year,dofilt9x=dofilt9x)
                if(rc != None):
                    stmids=stmids+rc

        else:
            stmopt="%s.%s"%(sopt,year)
            rc=getstmids(sopt,year,dofilt9x=dofilt9x)
            if(rc != None):
                stmids=stmids+rc

    #
    # filter out 9X
    #
    if(dofilt9x):
        nstmids=[]
        for stmid in stmids:
            num=int(stmid[0:2])
            if(num < 80):
                nstmids.append(stmid)

        stmids=nstmids


    if(verb):
        for stmid in stmids:
            print '(tcbase.makeStmList) stmid: ',stmid

    # -- case 
    return(stmids)


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
        poci=roci=rmax=reye=-999.0
        tcdepth='X'

    r34quad=[r34ne,r34se,r34sw,r34nw]
    r50quad=[r50ne,r50se,r50sw,r50nw]

    if(cqdir > 720.0):
        cqdir=-999.9
        cqspd=-99.9

    btdic=[flgtc,flgind,flgcq,flgwn,tdo,lf,cqlat,cqlon,cqvmax,wlat,wlon,wvmax,tsnum]
    cqdic=[cqlat,cqlon,cqvmax,cqdir,cqspd,cqpmin]
    bwdic=[bvmax,r34,r50,rmax,reye,poci,roci,tcdepth]
    btc=[blat,blon,bvmax,bpmin,bdir,bspd,btdic,cqdic,bwdic,r34quad,r50quad]

    return(btc)



def ParseMdeck2Btcs(dtgs,mdcards):

    btcs={}

    for dtg in dtgs:
        mdcard=mdcards[dtg]
        btc=ParseMdeckCard2Btcs(mdcard)
        btcs[dtg]=btc

    return(btcs)



def GetMdeckBts(stmid,dofilt9x=1,verb=0):

##    mdcards=findtc(stmid,dofilt9x)
    mdcards=findMdeckTC(stmid,do9x=dofilt9x)
    if(len(mdcards) == 0):
        print 'WWW(GetMdeckBts): mdcards = []'
        return(None,None)
    else:
        dtgs=mdcards.keys()
        dtgs.sort()
        bts=ParseMdeck2Btcs(dtgs,mdcards)
        return(dtgs,bts)



def GetBtcardsLatLonsFromMdeck(stmid,dtg,nhback=48,nhplus=120,verb=0):

    btcards=[]
    btcardsgt0=[]

    lats=[]
    lons=[]
    vmaxs=[]
    pmins=[]

    (btdtgs,btcs)=GetMdeckBts(stmid,dofilt9x=0,verb=verb)

    if(btdtgs == None):
        print 'WWW(tcbase.GetBtcardsLatLonsFromMdeck): no bts for stmid: ',stmid
        return(btcards,btcardsgt0,lats,lons,vmaxs,pmins)


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
    # -- 20130703 -- caused gfs2 to crash on plotting in lsdiag
    if(len(obtdtgsgt0) > 0):
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


def GetOpsRefTrk(dtg,stmid,rtaus=None,override=0,verb=0,btc=None,inputAD=None):


    from w2local import W2
    w2=W2()


    rc=getStmParams(stmid, convert9x=1)
    stm1id=rc[-1]
    astm2id=rc[-2]
    
    stmid=stm1id
    if(rtaus != None):
        taus=rtaus
    else:
        taus=[0,12,24,36,48,60,72,84,96,108,120]
    year=dtg[0:4]

    # --- set up the reftrk path
    #

    refbdir=w2.TcRefTrkDatDir
    refdir="%s/%s"%(refbdir,year)
    mf.ChkDir(refdir,'mk')
    refpath="%s/reftrk.%s.%s.txt"%(refdir,stmid,dtg)

    if(verb): print 'RRR in GetOpsRefTrk refpath: ',refpath,MF.GetPathSiz(refpath)


    #rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr
    # -- set up the reftrk path and open if there

    # -- always get storm ops adecks and make ad Adeck obj
    #
    snum=stmid[0:2]
    b1id=stmid[2]
    b2id=Basin1toBasin2[b1id].lower()

    if(IsJtwcBasin(b1id)):
        sdir="%s/%s"%(w2.TcAdecksJtwcDir,year)
        (shemoverlap,cy,cyp1)=CurShemOverlap(dtg)
        if(shemoverlap):
            mask=[]
            sdir="%s/%s"%(w2.TcAdecksJtwcDir,cy)
            sdirp1="%s/%s"%(w2.TcAdecksJtwcDir,cyp1)
            mask.append("%s/a%s%s%s.dat"%(sdir,b2id,snum,cy))
            mask.append("%s/a%s%s%s.dat"%(sdirp1,b2id,snum,cyp1))
        else:
            mask="%s/a%s%s%s.dat"%(sdir,b2id,snum,year)

        oaids=opsaids['jtwc']

    elif(IsNhcBasin(b1id)):
        sdir="%s/%s"%(w2.TcAdecksNhcDir,year)
        mask="%s/a%s%s%s.dat"%(sdir,b2id,snum,year)
        oaids=opsaids['nhc']

    else:
        print 'EEE(tcbase.GetOpsRefTrk): invalid b1id: ',b1id,'is not jt|nhc'
        sys.exit()

    #from adCL import Adeck
    #from adVM import GetStm2idFromAdeck
    #ad=Adeck(mask)


    # -- if not there get the adecks and make
    #
    if(MF.GetPathSiz(refpath) <= 0 or override):

        # get storm ops adecks and make the ad Adeck obj
        #
        snum=stmid[0:2]
        b1id=stmid[2]
        b2id=Basin1toBasin2[b1id].lower()
        if(IsJtwcBasin(b1id)):
            sdir="%s/%s"%(w2.TcAdecksJtwcDir,year)
            (shemoverlap,cy,cyp1)=CurShemOverlap(dtg)
            if(shemoverlap):
                mask=[]
                sdir="%s/%s"%(w2.TcAdecksJtwcDir,cy)
                sdirp1="%s/%s"%(w2.TcAdecksJtwcDir,cyp1)
                mask.append("%s/a%s%s%s.dat"%(sdir,b2id,snum,cy))
                mask.append("%s/a%s%s%s.dat"%(sdirp1,b2id,snum,cyp1))
            else:
                mask="%s/a%s%s%s.dat"%(sdir,b2id,snum,year)

            oaids=opsaids['jtwc']

        elif(IsNhcBasin(b1id)):
            sdir="%s/%s"%(w2.TcAdecksNhcDir,year)
            mask="%s/a%s%s%s.dat"%(sdir,b2id,snum,year)
            oaids=opsaids['nhc']

        from tcbase import Adeck,GetStm2idFromAdeck
        ad=Adeck(mask)

        try:
            REF=open(refpath,'w')
        except:
            print 'EEE unable to open reftrk output: ',refpath
            sys.exit()

        # -- check if refcards sufficent...if not, try to regen...
        #
        if(REF != None):
            refcards=open(refpath).readlines()
            if(len(refcards) <= 1):
                REF=None

        refcards=None

    else:
        
        # -- get the reftrk...
        #
        REF=None
        refcards=open(refpath).readlines()


    #rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr
    # -- parse reftrk if already done
    #

    reflats=[]
    reflons=[]

    if(REF == None and refcards != None):

        reftrk={}

        nr=len(refcards)
        tt=refcards[0].split()

        refdtg=tt[1]
        refstmid=tt[3]
        refaid=tt[5]
        reftau=tt[7]

        if(verb):
            print 'RRR reftrk: ',refpath
            print 'RRR reftrk: ',refdtg,refstmid,refaid,reftau,nr

        for n in range(1,nr):
            tt=refcards[n].split()
            tau=int(tt[0])
            lat=float(tt[1])
            lon=float(tt[2])
            vmax=float(tt[3])
            pmin=float(tt[4])
            reftrk[tau]=(lat,lon,vmax,pmin)
            reflats.append(lat)
            reflons.append(lon)
            if(verb): print 'RRR lat,lon: ',lat,lon

        return(reflats,reflons,refaid,reftau,reftrk)


    #rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr
    # -- otherwise make  it
    #

    try:
        REF=open(refpath,'w')
    except:
        print 'EEE unable to open reftrk output: ',refpath
        sys.exit()


    dd=ad.dtgs
    dd.sort()

    nposits=0

    gottau={}
    for tau in taus:
        gottau[tau]=0

    #
    # define a target tau
    #

    ttaus=[72,48,24]
    refaid=None
    reftau=None

    for ttau in ttaus:
        gottau[tau]=0

        for oaid in oaids:
            if(gottau[tau] == 0):
                try:
                    rc=ad.aidtrks[oaid,astm2id][dtg][ttau]
                    if(len(rc) >= 4): 
                        (lat,lon,pmin,vmax)=rc[0:4]
                    
                    #
                    # get the first posit...
                    #
                    gottau[ttau]=1
                    refaid=oaid
                    reftau=ttau
                    if(verb): print 'HHHHH ',ttau,oaid,gottau[ttau]
                    break

                except:
                    if(gottau[tau] == 0):
                        if(verb): print 'NNNN111 no tracks for ',oaid,astm2id,dtg,ttau

        if(gottau[ttau]):
            break

    # -- after loop see what aid is the ref and at what tau
    #

    b1id=stmid[2].lower()

    print 'RRR (refpath):',refpath
    print 'RRR  (reftrk):',dtg,stmid,b1id,refaid,reftau

    #---------------------------------------------------
    # get btcards
    # nhback=48 as the default or only consider previous 48 h of BT

    (btcards,btcardsgt0,btlats,btlons,btvmaxs,btpmins)=GetBtcardsLatLonsFromMdeck(stmid,dtg,verb=0)

    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # 
    # for 9X storms, mdeck might not be there...findtcs and the pull out from btops.dtg.txt
    #

    if(len(btcards) == 0 or int(btcards[0].split()[2]) == 0):
        otcs=findtcs(dtg)
        print 'otcs ',otcs
        for tc in otcs:
            tt=tc.split()
            tstmid=tt[1]
            print 'otc: ',tc,tstmid
            if(stmid == tstmid):
                tvmax=tt[2]
                tpmin=tt[3]
                trlat=float(tt[4])
                trlon=float(tt[5])
                #
                # crossing the prime meridian -- for lant only
                #
                if(trlon <= primeMeridianChk and b1id == 'l'):
                    trlon=trlon+360.0

                reflats.append(trlat)
                reflons.append(trlon)

        print 'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW -- no mdeck for: ',stmid,' dtg: ',dtg,' using btops.DTG.txt',reflons,reflats

    #
    # write the reftrk data to REF
    #

    rcard="dtg: %s stmid: %s refaid: %s reftau: %s"%(dtg,stmid,refaid,reftau)
    REF.writelines(rcard+'\n')

    reftrk={}

    for btcard in btcards[1:]:
        tt=btcard.split()
        bdtg=tt[0]
        blat=float(tt[1])
        blon=float(tt[2])

        reflats.append(blat)
        reflons.append(blon)

        bvmax=float(tt[3])
        bvflg=tt[4]
        bpmin=float(tt[5])
        btau=mf.dtgdiff(dtg,bdtg)
        if(btau == 0): btau=-1
        reftrk[btau]=(blat,blon,bvmax,bpmin)
        rcard="%4i  %5.1f  %6.1f  %3.0f  %6.0f BT"%(btau,blat,blon,bvmax,bpmin)
        if(verb): print 'RRR rcard: ',rcard
        REF.writelines(rcard+'\n')


    nojoy=1
    for tau in taus:
        try:
            rc=ad.aidtrks[oaid,astm2id][dtg][tau]
            if(len(rc) >= 4):
                (lat,lon,vmax,pmin)=rc[0:4]

            #
            # crossing the prime meridian; mod to get madagacar
            #
            if(lon <= primeMeridianChk and b1id == 'l'):
                lon=lon+360.0

            reflats.append(lat)
            reflons.append(lon)
            reftrk[tau]=(lat,lon,vmax,pmin)
            rcard="%4i  %5.1f  %6.1f  %3.0f  %6.0f %s"%(tau,lat,lon,vmax,pmin,refaid)
            if(verb): print 'RRR rcard: ',rcard
            REF.writelines(rcard+'\n')
            nojoy=0

        except:
            None

    # -- no aids use climo motion 285 ; 12 kt
    #
    if(nojoy):

        btaus=reftrk.keys()
        btaus.sort()

        if(btc != None):
            (blat0,blon0,bvmax0,bpmin0)=btc[0:4]
        else:
            if(len(btaus) > 0 and btaus[-1] >= -6):
                (blat0,blon0,bvmax0,bpmin0)=reftrk[btaus[-1]]
            else:
                print 'EEEEEEEEEEEEEEE no bt or forecast track in tcbase.GetOpsRefTrk()'
                sys.exit()

        if(blat0 > 0.0):

            if(abs(blat0) < 25.0):
                clmdir=285
                clmspd=12
            else:
                clmdir=315
                clmspd=6

        else:

            if(abs(blat0) < 25.0):
                clmdir=265
                clmspd=12
            else:
                clmdir=225
                clmspd=6


        nt=len(taus)
        dtau=taus[1]-taus[0]
        refaid='MFCLM'
        for n in range(1,nt):
            if(n == 1):
                reflats.append(blat0)
                reflons.append(blon0)
                tau=taus[0]
                if(bvmax0 == None): bvmax0=-99.
                if(bpmin0 == None): bpmin0=-999.
                reftrk[tau]=(blat0,blon0,bvmax0,bpmin0)
                rcard="%4i  %5.1f  %6.1f  %3.0f  %6.0f %s"%(tau,blat0,blon0,bvmax0,bpmin0,refaid)
                if(verb): print 'RRR rcard: ',rcard,' CCCCCCCCCClimo'
                REF.writelines(rcard+'\n')

                (rlat,rlon)=rumltlg(clmdir,clmspd,dtau,blat0,blon0)

                reflats.append(rlat)
                reflons.append(rlon)
                tau=taus[1]
                reftrk[tau]=(rlat,rlon,bvmax0,bpmin0)
                rcard="%4i  %5.1f  %6.1f  %3.0f  %6.0f %s"%(tau,rlat,rlon,bvmax0,bpmin0,refaid)
                if(verb): print 'RRR rcard: ',rcard,' CCCCCCCCCClimo'
                REF.writelines(rcard+'\n')

            else:

                (blat0,blon0,bvmax0,bpmin0)=reftrk[taus[n-1]]
                (rlat,rlon)=rumltlg(clmdir,clmspd,dtau,blat0,blon0)

                reflats.append(rlat)
                reflons.append(rlon)
                tau=taus[n]
                reftrk[tau]=(rlat,rlon,bvmax0,bpmin0)
                rcard="%4i  %5.1f  %6.1f  %3.0f  %6.0f %s"%(tau,rlat,rlon,bvmax0,bpmin0,refaid)
                if(verb): print 'RRR rcard: ',rcard,' CCCCCCCCCClimo'
                REF.writelines(rcard+'\n')




    if(verb): print 'RRR(refpath): ',refpath
    REF.close()

    return(reflats,reflons,refaid,reftau,reftrk)

def getCornerFewestLatLon(alats,alons,
                          lat1,lat2,lon1,lon2,
                          verb=0,
                        ):
    
    
    rlatm=(lat1+lat2)*0.5
    rlonm=(lon1+lon2)*0.5
    
    corners={11:0,
             22:0,
             12:0,
             21:0,
             }
    
    def whichCorner(lat,lon,rlatm,rlonm,corners):
        
        if(lat >= rlatm and lon >= rlonm):
            corners[22]=corners[22]+1
            return(22)
            
        elif(lat <= rlatm and lon <= rlonm):
            corners[11]=corners[11]+1
            return(11)
            
        elif(lat >= rlatm and lon <= rlonm):
            corners[21]=corners[21]+1
            return(21)
            
        elif(lat <= rlatm and lon >= rlonm):
            corners[12]=corners[12]+1
            return(12)
            
            
        
    for n in range(0,len(alats)):
        lat=alats[n]
        lon=alons[n]
        
        cc=whichCorner(lat, lon, rlatm, rlonm, corners)


    ccmin=99999
    for cc in corners.keys():
        ccval=corners[cc]
        if(ccval < ccmin): ccmin=ccval
        
    ccmins=[]
    for cc in corners.keys():
        ccval=corners[cc]
        if(ccval == ccmin): ccmins.append(cc)
        
    if(len(ccmins) > 1):
        ccminFinal=ccmins[0]
        for ccs in ccmins:
            if(ccs == 12): ccminFinal=ccs
            if(ccs == 22): ccminFinal=ccs
    else:
        ccminFinal=ccmins[0]
        
    return (ccminFinal)
    




def LatLonOpsPlotBounds(alats,alons,
                        latbuffPoleward=10.0,
                        latbuffEq=7.5,
                        lonbuff=10.0,
                        latinc=5.0,
                        loninc=5.0,
                        aspectmin=0.75,
                        dlonplotmax=80.0,
                        verb=0,
                        ):

    #
    # no lat/lons
    #
    if(len(alats) == 0):
        latplotmin=None
        latplotmax=None
        lonplotmin=None
        lonplotmax=None


    latmin=min(alats)
    latmax=max(alats)
    lonmin=min(alons)
    lonmax=max(alons)

    if(latmax < 0.0):
        latbuffS=latbuffPoleward
        latbuffN=latbuffEq
    else:
        latbuffN=latbuffPoleward
        latbuffS=latbuffEq

    latbar=(latmin+latmax)*0.5
    lonbar=(lonmin+lonmax)*0.5

    if(latmin < 0):
        nj1=int( (latmin/latinc)-0.5 )
        nj2=int( (latmax/latinc)-0.5 )
    else:
        nj1=int( (latmin/latinc)+0.5 )
        nj2=int( (latmax/latinc)+0.5 )

    nj3=int( (lonmin/loninc)+0.5 )
    nj4=int( (lonmax/loninc)+0.5 )

    j1=nj1*latinc
    j2=nj2*latinc
    j3=nj3*loninc
    j4=nj4*loninc

    latplotmin=j1-latbuffS
    latplotmax=j2+latbuffN
    lonplotmin=j3-lonbuff
    lonplotmax=j4+lonbuff

    dlonplot=lonplotmax-lonplotmin
    dlatplot=latplotmax-latplotmin

    aspect=dlatplot/dlonplot

    if(verb):
        print 'BBB (iter000) reftrk min,max: ',latmin,latmax,lonmin,lonmax
        print 'BBB (iter000) dlatplot,dlonplot: ',dlatplot,dlonplot,' aspect: ',aspect

    if(dlonplot > dlonplotmax):
        dlonplot=dlonplotmax
        print 'WWW (bounds): dlonplot > dlonplotmax: ',dlonplotmax,' set to dloplotmax'

    #
    # make initial adjustment
    #

    if(aspect < aspectmin):
        #dlatplot=dlonplot*aspectmin
        dlonplot=dlatplot/aspectmin
        dlatplot=int((dlatplot/latinc)+0.5)*latinc
        aspect=dlatplot/dlonplot
        if(verb):
            print 'BBB (iter---) 0000: dlatplot,dlonplot: ',dlatplot,dlonplot,' aspect: ',aspect

    elif(aspect > aspectmin):

        #dlatplot=dlonplot*aspectmin
        dlonplot=dlatplot/aspectmin
        dlatplot=int((dlatplot/latinc)+0.5)*latinc
        aspect=dlatplot/dlonplot
        if(verb):
            print 'BBB (iter+++) 0000: dlatplot,dlonplot: ',dlatplot,dlonplot,' aspect: ',aspect,aspectmin


    #
    # iterate
    #

    if(aspect > aspectmin):

        while(aspect > aspectmin):
            dlonplot=dlonplot+loninc*0.5
            aspect=dlatplot/dlonplot
            if(verb):
                print 'BBB (iter+++) 1111: dlatplot,dlonplot: ',dlatplot,dlonplot,' aspect: ',aspect

        if(latmax < 0.0):
            latplotmin=latplotmax-dlatplot
        else:
            latplotmax=latplotmin+dlatplot

    elif(aspect < aspectmin):

        while(aspect < aspectmin):
            dlatplot=dlatplot-latinc*0.5
            aspect=dlatplot/dlonplot
            if(verb):
                print 'BBB (iter---) 1111: dlatplot,dlonplot: ',dlatplot,dlonplot,' aspect: ',aspect

        if(latmax < 0.0):
            latplotmin=latplotmax-dlatplot
        else:
            latplotmax=latplotmin+dlatplot



    #
    # recenter in longitude
    #
    lonplotmin=j3-dlonplot*0.5
    lonplotmax=j4+dlonplot*0.5

    if(verb):
        print 'BBB (bounds): ','  latplotmin,latplotmax: ',latplotmin,latplotmax,'  lonplotmin,lonplotmax: ',lonplotmin,lonplotmax
        print 'BBB (bounds): ','           dlat/lonplot: ',dlatplot,dlonplot,'            aspect: ',aspect


    return(latplotmin,latplotmax,lonplotmin,lonplotmax)


def IsWindRadii(code):
    rc=0
    if(code == 'AAA'):
        rc=1
        return(rc)

    if(code == '' or code == '0'): return(rc)


    if( (code[2] == 'Q' or code[2] == 'S') and
        (
            code[0:2] == 'NN' or
            code[0:2] == 'NE' or
            code[0:2] == 'EE' or
            code[0:2] == 'SE' or
            code[0:2] == 'SS' or
            code[0:2] == 'SW' or
            code[0:2] == 'WW' or
            code[0:2] == 'NW')
        ):
        rc=1

    return(rc)


def WindRadiiCode2Normal(code,radii):

    #
    # convert pre 2004 codes -> ne/se/sw/nw quad standard
    #

    #
    # default
    #
    rne=rse=rsw=rnw=-999.

    if(radii[0] > 0): rne=float(radii[0])
    if(radii[1] > 0): rne=float(radii[1])
    if(radii[2] > 0): rne=float(radii[2])
    if(radii[3] > 0): rne=float(radii[3])

    if(len(code) != 3):
        print 'EEE atcf: invalid wind radii code: ',code
        sys.exit()

#AAA - full circle
    if(code == 'AAA'):
        rne=rse=rsw=rnw=radii[0]

#NNS - north semicircle
    elif(code == 'NNS'):
        rne=rnw=radii[0]
        rse=rsw=radii[1]

#NES - northeast semicircle
    elif(code == 'NES'):
        rne=radii[0]
        rse=0.5*radii[0]+0.5*radii[1]
        rsw=radii[1]
        rnw=0.5*radii[0]+0.5*radii[1]

#EES - east semicircle
    elif(code == 'EES'):
        rne=rse=radii[0]
        rnw=rsw=radii[1]

#SES - southeast semicircle
    elif(code == 'SES'):
        rse=radii[0]
        rsw=0.5*radii[0]+0.5*radii[1]
        rnw=radii[1]
        rne=0.5*radii[0]+0.5*radii[1]

#SSS - south semicircle
    elif(code == 'SSS'):
        rsw=rse=radii[0]
        rne=rnw=radii[1]

#SWS - southwest semicircle
    elif(code == 'SWS'):
        rsw=radii[0]
        rnw=0.5*radii[0]+0.5*radii[1]
        rne=radii[1]
        rse=0.5*radii[0]+0.5*radii[1]

#WWS - west semicircle
    elif(code == 'WWS'):
        rnw=rsw=radii[0]
        rne=rse=radii[1]

#NWS - northwest semicircle
    elif(code == 'NWS'):
        rnw=radii[0]
        rne=0.5*radii[0]+0.5*radii[1]
        rse=radii[1]
        rsw=0.5*radii[0]+0.5*radii[1]

#NNQ, NEQ, EEQ, SEQ, SSQ, SWQ, WWQ, NWQ

    elif(code[2] == 'Q'):

        if(code[0:2] == 'NN'):

            rne=0.5*radii[0] + 0.5*radii[1]
            rse=0.5*radii[1] + 0.5*radii[2]
            rsw=0.5*radii[2] + 0.5*radii[3]
            rnw=0.5*radii[0] + 0.5*radii[3]

        # ----------------- currrent (> 2005) standard

        elif(code[0:2] == 'NE'):

            rne=radii[0]
            rse=radii[1]
            rsw=radii[2]
            rnw=radii[3]

        elif(code[0:2] == 'EE'):

            rne=0.5*radii[3] + 0.5*radii[0]
            rse=0.5*radii[0] + 0.5*radii[1]
            rsw=0.5*radii[1] + 0.5*radii[2]
            rnw=0.5*radii[2] + 0.5*radii[3]

        elif(code[0:2] == 'SE'):
            rne=radii[3]
            rse=radii[0]
            rsw=radii[1]
            rnw=radii[2]

        elif(code[0:2] == 'SS'):

            rne=0.5*radii[2] + 0.5*radii[3]
            rse=0.5*radii[3] + 0.5*radii[0]
            rsw=0.5*radii[0] + 0.5*radii[1]
            rnw=0.5*radii[1] + 0.5*radii[2]

        elif(code[0:2] == 'SW'):

            rne=radii[2]
            rse=radii[3]
            rsw=radii[0]
            rnw=radii[1]

        elif(code[0:2] == 'WW'):

            rne=0.5*radii[1] + 0.5*radii[2]
            rse=0.5*radii[2] + 0.5*radii[3]
            rsw=0.5*radii[3] + 0.5*radii[0]
            rnw=0.5*radii[0] + 0.5*radii[1]

        elif(code[0:2] == 'NW'):

            rne=radii[1]
            rse=radii[2]
            rsw=radii[3]
            rnw=radii[0]

        else:

            print 'EEEEEE atcf: invalid Q wind radii code: ',code
            sys.exit()

    #
    # it's not physically possible for all to be zero, if so, then set to undefined
    #

    if(rne == 0.0 and rse == 0.0 and rse == 0.0 and rnw == 0.0):
        rne=rse=rsw=rnw=-999.

    rquad=[rne,rse,rsw,rnw]

    return(rquad)


#uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu
# old unbounded methods
def ufile2dtghms(ufile):
    tt=ufile.split('.')
    tt=tt[1].split('_')
    dtghms="%s %02d:%02d:%02d"%(tt[1],int(tt[2]),int(tt[3]),int(tt[4]))
    return(dtghms)


def getuniqdecks(AZ,diffhr=48.0,verb=0,lenGoodFile=31,doMerge=1):


    def parseABdeck(cards):
        deck={}
        dtgs=[]
        aids=[]
        taus=[]
        allcards=cards.split('\n')
        for card in allcards:
            tt=card.split(',')
            if(len(tt) > 1):
                try:
                    dtg=tt[2].strip()
                    aid=tt[4].strip()
                    tau=int(tt[5].strip())
                    MF.append3TupleKeyDictList(deck, dtg, aid, tau, card)
                    dtgs.append(dtg)
                    aids.append(aid)
                    taus.append(tau)
                except:
                    print 'WWW--tcVM.getuniqdecks.parseABdeck(): bad card: ',card
                
        dtgs=mf.uniq(dtgs)
        aids=mf.uniq(aids)
        taus=mf.uniq(taus)
        
        return(deck,dtgs,aids,taus)
    
    def uniqDecks(ufiles,cards,nb,ne):
        
        alldecks={}
        alldtgs=[]
        allaids=[]
        alltaus=[]
        
        allcards=''
        
        for n in range(nb,ne+1):
            ufile=ufiles[n]
            abcards=cards[ufile]
            (deck,dtgs,aids,taus)=parseABdeck(abcards)
            alldecks.update(deck)
            alldtgs=alldtgs+dtgs
            allaids=allaids+aids
            alltaus=alltaus+taus
            
        allaids=mf.uniq(allaids)
        alldtgs=mf.uniq(alldtgs)
        alltaus=mf.uniq(alltaus)
            
        alldtgs.sort()
        
        for dtg in alldtgs:
            for aid in allaids:
                for tau in alltaus:
                    try:
                        rc=alldecks[dtg,aid,tau]
                    except:
                        rc=None
                    if(rc != None):
                        for r in rc:
                            allcards=allcards+r+'\n'
                        
        return(allcards,allaids,alldtgs,alltaus)
    
                        
    def printUcards(ucards):
        
        for card in ucards.split('\n'):
            print card

        
    MF.sTimer('ufiles')

    zfiles=AZ.namelist()

    uniqfiles=[]
    uniqcards={}

    sizes=[]
    sizfiles={}
    filesizs={}
    cards={}

    n=0

    ufiles=[]
    for zfile in zfiles:

        if(len(zfile) <= lenGoodFile):

            try:
                cards[zfile]=AZ.read(zfile)
                tt=AZ.getinfo(zfile)
                siz=tt.file_size
                tsiz=siz
                
                # -- 20220816 -- special case where jt did not clean out previous awp932022.dat
                #
                if(mf.find(zfile,'awp932022.dat_202208')):
                    acards=cards[zfile].split('\n')
                    ncards=''
                    for acard in acards:
                        asiz=len(acard)
                        if(asiz > 0):
                            aa=acard.split(',')
                            dtg=aa[2].strip()
                            if(dtg[0:6] == '202208'):
                                ncards=ncards+acard+'\n'
                            
                    cards[zfile]=ncards
                    siz=len(cards[zfile])
                    print 'SSS-20220816 for zfile: ',zfile,'siz: ',siz,tsiz
    
                sizfiles[siz]=zfile
                sizes.append(siz)
                filesizs[zfile]=siz
                
    
                if(verb): print 'GGGGGGGGGoodfile: ',n,zfile,len(cards[zfile]),siz
                ufiles.append(zfile)
                n=n+1
            
            except:
                if(verb): print 'BBBBBBBBBBadfile: ',zfile,len(zfile),' BBBBBBBBBBBBBBBBBBBBBBBBBBBBBaaaaaaaaaaaaaaaaaaaDDDDDDDDDDDDDDDDDDDDD'
            


    ufiles.sort()
    nuf=len(ufiles)
    
    nb=0
    nuend=nuf-1
    nuend=nuf
    if(nuend == 0): nuend=1
    
    ustmid=ufiles[-1][1:9]

    for n in range(0,nuend):
        
        ufile=ufiles[n]
        #if((n+1) > nuend):   # -- 20160727 -- bug for case with 1 good file in zip archive
        if((n+1) >= nuend):
            ufilep1=ufiles[n]
        else:
            ufilep1=ufiles[n+1]

        usiz=filesizs[ufile]
        usizp1=filesizs[ufilep1]
        
        dtghms=ufile2dtghms(ufile)
        dtghms1=ufile2dtghms(ufilep1)
        udiff=MF.DiffDtgHms(dtghms,dtghms1)

        if(verb):
            print ' 0000: ',n,ufile,usiz,dtghms
            print ' 1111: ',n+1,ufilep1,usizp1,dtghms1
            print ' 2222: ',ustmid,udiff,diffhr,n,nuf-1
        

        # -- test if last file is bigger than penultimate at end of ufile list
        # -- the assumption is the last uniq file should be bigger if last one...
        # -- otherwise you have a new storm so don't use the last one before a big change
        # -- in time...except...
        # -- 20200923 -- maybe not... nhc did a quick turnaround for 90L in 2020...
        #
        # -- special case???? for 90L.2020? YYEESS!  last a/bdeck in archive is from 23l 9X really is C8L.2020
        #
        
        
        if(usizp1 > usiz and n == nuf-2 and ustmid == 'al902020'):
            
            # -- case where penultimate differs from last
            #
            ne=n
            
            print ' 5555: ',n,nb,ne,ufile,ufilep1,nuf
            if(doMerge):
                MF.sTimer('uniqDeck-%s-%d-%d-merge-PenUlt-END'%(ustmid,nb,ne))
                (ucards,allaids,alldtgs,alltaus)=uniqDecks(ufiles,cards,nb,ne)
                MF.dTimer('uniqDeck-%s-%d-%d-merge-PenUlt-END'%(ustmid,nb,ne))
                
            uniqfiles.append((ufile,usiz))
            uniqcards[ufile]=ucards
            break
         
            ## -- set last one as uniq
            ##
            #uniqfiles.append((ufilep1,usizp1))
            #uniqcards[ufilep1]=cards[ufilep1]
            
            ## -- break out of loop
            ##
            #break
            
        
        
        if(udiff > diffhr or n == nuf-1 or nuf == 1):

            if(verb):
                print 'udiff: %6.1f p0: %40s %10d  p1:  %40s %10d '%(udiff,ufile,usiz,ufilep1,usizp1)

            # -- test if last file is bigger than penultimate at end of ufile list
            # -- the assumption is the last uniq file should be bigger if last one...
            # -- otherwise you have a new storm so don't use the last one before a big change
            # -- in time...except...
            # -- 20200923 -- maybe not... nhc did a quick turnaround for 90L in 2020...
            #
            # -- special case???? for 90L.2020?
            #
            
            if(usizp1 > usiz and n == nuf-1 ):
                # -- bug should be n+1 vice n as below
                #
                ne=n+1
                uniqfiles.append((ufilep1,usizp1))
                ucards=cards[ufilep1]
                
                if(verb): print ' 4444: ',nb,ne,ufilep1,nuf
                if(doMerge):
                    MF.sTimer('uniqDeck-%d-%d-merge-END'%(nb,ne))
                    (ucards,allaids,alldtgs,alltaus)=uniqDecks(ufiles,cards,nb,ne)
                    MF.dTimer('uniqDeck-%d-%d-merge-END'%(nb,ne))
                uniqcards[ufilep1]=ucards
                
            else:
                
                ne=n
                uniqfiles.append((ufile,usiz))

                if(verb): print ' 3333: ',nb,ne,ufile
                if(doMerge):
                    MF.sTimer('uniqDeck-%s-%d-%d-merge'%(ustmid,nb,ne))
                    (ucards,allaids,alldtgs,alltaus)=uniqDecks(ufiles,cards,nb,ne)
                    MF.dTimer('uniqDeck-%s-%d-%d-merge'%(ustmid,nb,ne))
                else:
                    ucards=cards[ufile]
                    
                uniqcards[ufile]=ucards
                
                nb=ne+1
                

    MF.dTimer('ufiles')

    return(uniqfiles,uniqcards)



def get9xABuniq(aduniqzippath,bduniqzippath,verb=0):

    abcards=''
    abcardsZip={}
    
    if(verb):
        print 'AAAUUUZZZPPP: ',aduniqzippath
        print 'BBBUUUZZZPPP: ',bduniqzippath

    try:
        AZ=zipfile.ZipFile(aduniqzippath)
        afiles=AZ.namelist()
    except:
        print 'WWW tcVM.get9xABuniq -- failed to open|read aduniqzippath: ',aduniqzippath,' afiles=[]'
        afiles=[]

    try:
        BZ=zipfile.ZipFile(bduniqzippath)
        bfiles=BZ.namelist()
    except:
        print 'WWW tcVM.get9xABuniq -- failed to open|read bduniqzippath: ',bduniqzippath,' bfiles=[]'
        bfiles=[]

    nA=len(afiles)
    nB=len(bfiles)
    if(verb): print '#Afiles: ',nA,' #Bfiles: ',nB
    
    doByFile=0
    if(nA == nB): doByFile=1
    
    n=0
    for afile in afiles:
        akey=afile[-17:-6]
        if(verb): print 'AAAAAAAA-afile:',afile,akey
        ocards=AZ.read(afile)
        if(doByFile):
            abcardsZip[n]=ocards
        #print 'OOOOOOOOOO',ocards
        abcards=abcards+ocards
        n=n+1

    n=0
    for bfile in bfiles:
        bkey=bfile[-17:-6]
        if(verb): print 'BBBBBBBB-bfile:',bfile,bkey
        ocards=BZ.read(bfile)
        # -- 20220611 -- very special case 
        bstrm=bfile[0:9]
        if(bstrm == 'bep922022'):
            ocards='9999'+ocards
            print 'SSS -- special case of bdeck with initial old card -- goon it up so Adeck fails...'
            print ocards
        if(doByFile):
            abcardsZip[n]=abcardsZip[n]+ocards
        n=n+1
            
        #print 'OOOOOOOO',ocards
        abcards=abcards+ocards

    return(abcards,abcardsZip)

def get9xAuniq(aduniqzippath,tstmid):

    acards=''
    icharId=tstmid[0].lower()

    try:
        AZ=zipfile.ZipFile(aduniqzippath)
        afiles=AZ.namelist()
    except:
        afiles=[]


    for n in range(0,len(afiles)):
        afile=afiles[n]
        ocharId=chr(icharA+n)
        if(icharId == ocharId):
            ocards=AZ.read(afile)
            acards=acards+ocards
            break

    return(acards)



def getHemis(stmids):

    rc=None
    hemis=[]
    for stmid in stmids:
        (snum,b1id,year,b2id,stm2id,stm1id)=getStmParams(stmid)
        hemis.append(Basin1toHemi[b1id.upper()])

    if('nhem' in hemis and 'shem' in hemis): rc='global'
    if('nhem' in hemis and not('shem' in hemis)): rc='nhem'
    if('shem' in hemis and not('nhem' in hemis)): rc='shem'

    return(rc)

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


def vmaxMS2KT(vmax):

    vmax=int(vmax)
    if(vmax%5 < 2.5):
        vmax=5*int(vmax/5)
    elif(vmax%5 >= 2.5):
        vmax=5*(int(vmax/5)+1)
    return(vmax)


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
                bdir=TcBtNeumannDatDir
            elif(source == 'ops'):
                bdir=TcBtOpsDatDir
            else:
                bdir=TcBtDatDir

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


def TCType(vmax):

    if(vmax <= 34): tctype='TD'
    if(vmax >= 35 and vmax <= 63): tctype='TS'
    if(vmax >= 64 and vmax <= 129): tctype='TY'
    if(vmax >= 130): tctype='STY'

    return(tctype)


def TCNum2Stmid(year,source='',verb=0):
    """
convert stm number -> basin ID using storms.table*
tc/p.tc.names.py year converts this to 

    """


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
        if(verb): print 'sn,b1,h1(TCNum2Stmid):',sn,b1,h1
        stmids.append(stmid)

        #
        # logic for SLANT
        #

        if( (b1 == 'S' or b1 == 'P') and b1 != 'Q'):
            shemid[sn]=stmid

        if(b1 == 'A' or b1 == 'B'):
            nioid[sn]=stmid

    stmids.sort()

    if(verb):
        for stmid in stmids:
            print 'stmid(TCNum2Stmid):',stmid

        sns=shemid.keys()
        sns.sort()

        for sn in sns:
            print 'SSS',sn,shemid[sn]

        nins=nioid.keys()
        nins.sort()
        for sn in nins:
            print 'IIII',sn,nioid[sn]

    return(shemid,nioid)

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

        if(mf.find(bdcard,'GENESIS')):
            print 'WWW NHC genesis posit...bybass...'
            continue
        
        tt=bdcard.split(',')
        t2=[]
        for ttt in tt:
            ttt=ttt.strip()
            t2.append(ttt)

        #
        # parse out basics
        # 

        dtg=t2[2]

        # look for non 6-h times
        #
        hh=int(dtg[8:10])

        # -- nhc puts land fall point, an issue of on synoptic hour and min != ''
        #
        try:
            min=int(tt[3])
        except:
            min=-999

        if((hh != 0 and hh != 6 and hh != 12 and hh != 18) or min != -999):
            continue

        clat=t2[6]
        clon=t2[7]
        try:
            vmax=int(t2[8])
        except:
            vmax=-99

        (rlat,rlon)=Clatlon2Rlatlon(clat,clon)
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

    (rlat,rlon)=Clatlon2Rlatlon(clat,clon)

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


def rumhdspi(rlat0,rlon0,rlat1,rlon1,dt,tcunits=tcunits):

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


def findtcs(cdtg,dofilt9x=0,srcopt='btops',doLF=1,verb=0):

    from w2local import W2
    w2=W2()
    
    from tcbase import TcCarqDatDir
    if(srcopt == 'btops'):
        yyyy=cdtg[0:4]
        ddir="%s/%s"%(TcCarqDatDir,yyyy)
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

    yyyym1=int(yyyy)-1
    yyyym1=str(yyyym1)
    yyyyp1=int(yyyy)+1
    yyyyp1=str(yyyyp1)

    (shemoverlap,shyyyy,shyyyyp1)=CurShemOverlap(cdtg)

    tcs=[]
    mdtcs=[]

    doprevyear=0
    if(mm == '01' or mm == '02'): doprevyear=1

    mddir=w2.TcMdecksFinalDir
    mdprefix='MdOps'

    mdmkyyyy="%s/%s/%s.???.*"%(mddir,yyyy,mdprefix)
    mdmkyyyym1="%s/%s/%s.???.*"%(mddir,yyyym1,mdprefix)
    mdmkyyyyp1="%s/%s/%s.???.*"%(mddir,yyyyp1,mdprefix)

    mdp=glob.glob(mdmkyyyy)
    mdpm1=glob.glob(mdmkyyyym1)
    mdpp1=glob.glob(mdmkyyyyp1)

    if(verb):
        print 'MMM mdmkyyyy:   ',mdmkyyyy
        print 'MMM mdmkyyyym1: ',mdmkyyyym1
        print 'MMM mdmkyyyyp1: ',mdmkyyyyp1

        print 'PPPPPPPPPPP doprevyear: ',doprevyear,' shemoverlap ',shemoverlap

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

    # -- remove dups, increas drmin for 9X
    #
    mdtcs=DupChkTcs(mdtcs,drmin=1.5,verb=verb)

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



    return(r34quad,r50quad,frtype,r34,r50)


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

    return(rcourse,rspeed,umotion,vmotion)




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
        (rlat,rlon)=Clatlon2Rlatlon(clat,clon)


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
            (rlat,rlon)=Clatlon2Rlatlon(wnclat,wnclon)
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

        if(IsWindRadii(rcode)):
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
                rquad=WindRadiiCode2Normal(rcode,radii)
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
            try:
                vmax=int(tt[10])
            except:
                vmax=0
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
            try:
                ttt=open(path,'r').readlines()
            except:
                print 'WWW unable to open: ',path
                ttt=[]

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

def LoadMdeckCard(tstm,addata,adkey,abdcard,bdcard,ebdcard,dtg,lf,doLF=1):
    #--------------------------------------------------------------------------
    # 20070911 -- loadmdeck rips the adeck and bdeck and ebt (extended bt)  hashes to
    # construct the final mdeck card with all storm data that will
    # be used in tcanal, etc. including r34/r50 poci/roci rmax/deye/depth code
    #
    #--------------------------------------------------------------------------

    from w2local import W2
    w2=W2()
    
    (ar34quad,ar50quad,artype)=GetAdeckWindRadii(addata,adkey)

    tcindBT=''
    tcindCQ=''

    if(bdcard != ''):
        (vmax,pmin,lat,lon,r34,r50,dir,spd,odir,ospd,nts,tcindBT,br34quad,br50quad)=ParseTCcard(bdcard)
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

            # CQ tc indicator 
            #
            tcindCQ=cq[3]

            # -- set number of TS posits to -1 as an not-real-bt indicator 
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

    # -- 20120201 -- select the BT indicator first
    #
    if(IsTc(tcindBT) >= 0):
        tcind=tcindBT
    elif(IsTc(tcindCQ) >= 0):
        tcind=tcindCQ
    else:
        tcind='XX'

    # -- set by max wind if not available
    if(IsTc(tcind) <  0 and IsTcWind(fvmax)): tcind='TC'


    #
    # 20080108 -- test if operational TC 
    #
    tcstat='TC'
    if(IsTc(tcind) <= 0): tcstat='NT'

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

    from tcbase import MdeckDir
    
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

    if(len(mdpaths) > 0):

        mdpath=mdpaths[-1]
        mdcards=open(mdpath).readlines()

        for mdcard in mdcards:
            dtg=mdcard.split()[0]
            omdcards[dtg]=mdcard


    return(omdcards)




def findtc(tstm,dofilt9x=1,srcopt='bt',doLF=1,verb=0,btonly=0):
    #--------------------------------------------------------------------------
    # 20070911 -- findtc greps adeck cards and creates addata{} where the key is the DTG
    # and generates mdeck cards
    #
    #--------------------------------------------------------------------------

    from w2local import W2
    w2=W2()
    
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

        ddir=TcBtDatDir
        btprefix='BT'
        addir=TcAdecksFinalDir
        adprefix='AD'
        if(verb): print 'BBBBBBBB bt source is real (BT.)'

    if(srcopt == 'btops' or dofilt9x == 0):
        ddir=TcBtDatDir
        btprefix='BtOps'
        addir=TcAdecksFinalDir
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

    # --check if the  local adeck is old..typically 9x
    #

    if(not(btonly)):
        # --check if the  local adeck is old..typically 9x
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
        print 'BBBB---- ',bdtgs
        print 'AAAA---- ',bdtgs


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
        except:
            carqcards=None

        if(carqcards != None):
            for n in range(0,len(carqcards)):
                carqcard=carqcards[n]
                ParseAdeckCard(addata,dtg,carqcard,verb=verb)


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


def getTcFcPosits(ftpath,dtft=1,verb=0):

    """ use get AD.Adeck to get single aid/dtg from an adeck path
    """
    from adCL import Adeck

    ad=Adeck(ftpath)
    aid=ad.aids[0]
    dtg=ad.dtgs[0]

    ftposits={}

    for stm2id in ad.stm2ids:
        fts=ad.aidtrks[aid,stm2id][dtg]
        taus=fts.keys()
        taus.sort()
        ntaus=len(taus)

        dtau=6
        if(ntaus > 1): dtau=taus[1]-taus[0]

        for n in range(0,len(taus)):

            if(n == 0 and ntaus == 1):
                tau0=taus[n]
                tau1=taus[n]
            else:
                tau0=taus[n-1]
                tau1=taus[n]

            (rlat0,rlon0,rvmax0,rpmin0)=fts[tau0][0:4]
            (rlat1,rlon1,rvmax1,rpmin1)=fts[tau1][0:4]

            if(tau0 == 0):
                stau=tau0
            else:
                stau=tau0+dtft

            for fttau in range(stau,tau1+dtft,dtft):
                rfact1=(fttau-tau0)*1.0/dtau
                rfact0=(1.0-rfact1)
                rlat=rfact0*rlat0+rfact1*rlat1
                rlon=rfact0*rlon0+rfact1*rlon1
                rvmax=rfact0*rvmax0+rfact1*rvmax1
                if(verb): print 'getTcFcPosits ',fttau,rlat,rlon,rvmax
                MF.appendDictList(ftposits,fttau,(rlat,rlon,rvmax))

    return(ftposits)


def getMd2DSsTags(sdir='/w21/dat/tc/DSs'):

    otags=[]
    tags=glob.glob("%s/mdecks2-*"%(sdir))

    for tag in tags:
        (dir,file)=os.path.split(tag)
        (base,ext)=os.path.splitext(file)

        tt=base.split('mdecks2-')
        otags.append(tt[1])

    return(otags)


# -- TCw2.py -- old
def DupChkTcs(tcs,drmin=0.5,verb=0):

    nstm=len(tcs)

    stms=[]
    stmlats=[]
    stmlons=[]

    utcs=[]

    itcu={}

    for tc in tcs:
        tt=tc.split()
        dtg=tt[0]
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

                stmnum1=int(stms[i][0:2])
                b1id1=stms[i][2]
                stmnum2=int(stms[ii][0:2])
                b1id2=stms[ii][2]

                # -- case of lant -> epac
                #
                if((b1id1 == 'E' and b1id2 == 'L') or (b1id1 == 'E' and b1id2 == 'L')):
                    print 'TTT transition storm from lant <-> epac',dtg,stms[i],stms[ii]
                    itcu[ii]=1
                    itcu[i]=1

                if(verb): print 'uuuu ',stms[i],stms[ii],stmnum1,stmnum2,b1id1,b1id2

                # -- select stm with correct subbasin id if basin is IO or SH
                #
                if(stmnum1 == stmnum2):

                    if(b1id1 == 'S' and b1id2 == 'P'):
                        itcu[ii]=1
                        itcu[i]=0
                    elif(b1id1 == 'P' and b1id2 == 'S'):
                        itcu[ii]=0
                        itcu[i]=1

                    elif(b1id1 == 'I' and (b1id2 == 'A' or b1id2 == 'B') ):
                        itcu[ii]=1
                        itcu[i]=0
                    elif((b1id2 == 'A' or b1id2 == 'B') and b1id2 == 'I'):
                        itcu[ii]=0
                        itcu[i]=1


            if(verb and (itcu[ii]==0 or itcu[i]) ):
                print 'qqq ii ',i,ii,dr,drmin,' dlat lon: ',dlat,dlon,stms[i],stms[ii]

    #
    # create new storm list
    #

    for i in range(0,nstm):
        if(itcu[i] == 1): utcs.append(tcs[i])

    return(utcs)


def ConvertB1Stmid2B2Stmid(b1stmid):

    snum=b1stmid[0:2]
    b1id=b1stmid[2]
    year=b1stmid.split('.')[1]

    b2id=Basin1toBasin2[b1id]

    b2stmid="%s%s%s"%(b2id,snum,year)

    return(b2stmid)


def sortStmids(stm1ids):

    basinorder=['l','e','c','w','i','a','b','s','p','q']
    ostm1ids=[]

    for bo in basinorder:
        for stm1id in stm1ids:
            b1id=stm1id.split('.')[0][-1]
            if(bo.upper() == b1id): ostm1ids.append(stm1id)

    return(ostm1ids)


def printTrk(stmid,dtg,rlat,rlon,vmax,pmin,
             dir=-999,spd=-999,dirtype='X',
             tdo='---',
             tccode='XX',
             wncode='XX',
             ntrk=0,
             ndtgs=0,
             r34m=None,
             r50m=None,
             alf=None,
             sname='---------',
             gentrk=0,
             doprint=1):

    (clat,clon)=Rlatlon2Clatlon(rlat,rlon,dodec=1)

    if(vmax == None or vmax == undef or vmax == 0):  cvmax='---'
    else:              cvmax="%03d"%(vmax)
    if(pmin == None):  cpmin='----'
    else:              cpmin="%4d"%(pmin)

    if(r34m == None or r34m == undef):
        cr34m='---'
    else:
        cr34m="%3.0f"%(float(r34m))

    if(r50m == None or r34m == undef):
        cr50m='---'
    else:
        cr50m="%3.0f"%(r50m)

    # -- if first posit set to 360.0 and -0 spd
    #
    if(dir == -999.): dir=360.0
    if(spd == -999.): spd=-0.0

    cdir="%5.1f"%(dir)
    cspd="%4.1f"%(spd)

    if(alf == None or alf == undef):
        clf='----'
    else:
        clf="%4.2f"%(alf)

    if(gentrk):
        card="%s* %12s "%(dtg,stmid.upper())
    else:
        card="%s  %12s "%(dtg,stmid.upper())

    card=card+"%s %s %s  %s  %s %s"%(cvmax,cpmin,clat,clon,cr34m,cr50m)
    card=card+"  %s %s %s  %s %s  %s"%(cdir,cspd,dirtype,tccode,wncode,tdo)
    card=card+" %3d/%-3d lf: %s %-9s"%(ntrk,ndtgs,clf,sname[0:9])
    if(gentrk): card=card+" <**Genesis"
    if(doprint): print card
    return(card)



def printTCV(stmid,dtg,rlat,rlon,vmax,pmin,
             dir=-999,spd=-999,
             r34m=None,
             r50m=None,
             sname='---------',
             gentrk=0,
             doprint=1):



    (clat,clon)=Rlatlon2Clatlon(rlat,rlon,dodec=1)
    if(vmax == None):  cvmax='---'
    else:              cvmax="%03d"%(vmax)
    if(pmin == None):  cpmin='----'
    else:              cpmin="%4d"%(pmin)

    if(r34m == None):
        cr34m='---'
    else:
        cr34m="%3.0f"%(float(r34m))

    if(r50m == None):
        cr50m='---'
    else:
        cr50m="%3.0f"%(r50m)

    cdir="%5.1f"%(dir)
    cspd="%4.1f"%(spd)

    if(alf == None):
        clf='----'
    else:
        clf="%4.2f"%(alf)


    tcvitalscard="%4s %3s %-9s %8s %04d %s %s %s %s %s %s %s %s %s %s %s %s %s %s"%\
        (tcVcenterid,stm3id,stmname,
         dtg[0:8],int(dtg[8:10])*100,
         clat,clon,
         vitdir,vitspd,
         vitpmin,
         vitpoci,vitroci,
         vitvmax,vitrmax,
         vitr34ne,vitr34se,vitr34sw,vitr34nw,
         vitdepth)



    card="%s %s "%(dtg,stmid.upper())
    card=card+"%s %s %s  %s  %s %s"%(cvmax,cpmin,clat,clon,cr34m,cr50m)
    card=card+"  %s %s %s  %s %s  %s"%(cdir,cspd,dirtype,tccode,wncode,tdo)
    card=card+" %3d/%-3d lf: %s %-9s"%(ntrk,ndtgs,clf,sname[0:9])
    if(gentrk): card=card+" <---Genesis"
    if(doprint): print card
    return(card)


def getMd2Years(stmopt=None,dtgopt=None):

    curdtg=mf.dtg()
    
    years=[int(curdtg[0:4])]
    
    if(dtgopt != None):
        dtgs=mf.dtg_dtgopt_prc(dtgopt,ddtg=6)

        years=[]
        for dtg in dtgs:
            (rc,nhemyears)=getNhemYearsInt(dtg)
            years=years+nhemyears

            curyear=int(dtg[0:4])
            shemyear=int(getShemYear(dtg))
            if(curyear != shemyear):
                years.append(shemyear)
                
        years=mf.uniq(years)

    if(stmopt != None):

        if(type(stmopt) is ListType):
            stmids=stmopt
        else:
            # -- use this one because makeStmListMdeck is a method on TcData() -- this is stand-alone
            stmids=MakeStmList(stmopt)

        if(len(stmids) > 0):
            years=[]
            for stmid in stmids:
                year=int(stmid.split('.')[1])
                years.append(year)
            years=mf.uniq(years)
        
        
    return(years)


def getMd2tag(stmopt=None,dtgopt=None,years=None,dobail=1):

    def setmd2tags(years):

        md2tag=None
        md2tags=[]
        for year in years:
            if(year >= 2010 and year <= 2013): md2tags.append('10-13')
            if(year >= 2000 and year <= 2009): md2tags.append('00-09')
            if(year >= 1990 and year <= 1999): md2tags.append('90-99')
            if(year >= 1980 and year <= 1989): md2tags.append('80-89')
            if(year >= 1970 and year <= 1979): md2tags.append('70-79')
            if(year >= 1960 and year <= 1969): md2tags.append('60-69')
            if(year >= 1948 and year < 1959):  md2tags.append('48-59')           
            
            #if(year >= 2010 and year <= 2011): md2tags.append('10-12')
            #if(year >= 2000 and year <= 2009): md2tags.append('00-10')
            #if(year >= 1979 and year <= 1999): md2tags.append('79-99')
            #if(year >= 1969 and year < 1979):  md2tags.append('69-79')
            #if(year >= 1949 and year < 1969):  md2tags.append('49-70')
            
            if(year < 1948):                   md2tags=['tooyoung']

        md2tags=mf.uniq(md2tags)

        if(len(md2tags) > 1):
            print 'EEE getMd2tag.dtgopt: ',dtgopt,' crosses a boundary in the mdecks2*.pypdb, sayoonara...'
            if(dobail): sys.exit()

        elif(len(md2tags) == 1 and md2tags[0] != 'tooyoung'):
            md2tag=md2tags[0]

        return(md2tag)



    md2tag=None
    if(dtgopt != None):
        dtgs=mf.dtg_dtgopt_prc(dtgopt,ddtg=6)

        years=[]
        for dtg in dtgs:
            years.append(int(dtg[0:4]))

        years=mf.uniq(years)
        md2tag=setmd2tags(years)


    if(stmopt != None):

        if(type(stmopt) is ListType):
            stmids=stmopt
        else:
            stmids=MakeStmList(stmopt)

        years=[]
        for stmid in stmids:
            year=int(stmid.split('.')[1])
            years.append(year)

        years=mf.uniq(years)
        md2tag=setmd2tags(years)

    if(years != None):
        md2tag=setmd2tags(years)

    return(md2tag)

def GetMap9x(dtg,verb=0):

    from w2local import W2
    w2=W2()

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


def GetTCName(s,quiet=1,doprevyear=0):

    warn=1

    sid=s.split('.')[0]
    yyyy=s.split('.')[1]

    tcnames=GetTCnamesHash(yyyy)

    try:
        sname=tcnames[yyyy,sid]
    except:
        if(doprevyear):
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
        else:
            sname='unknown'


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

def makeTcgenPhpInventory(dtgopt,gendtgs,invopt,tstmids,basins,ndayback=5,verb=0):

    from TCtrk import tcgenW3Dir as webdir

    # -- use older mdeck for Tcdata because it has mdDg object with gen1dtg
    #
    from TC import TcData
    tcD=TcData(dtgopt=dtgopt)

    MF.sTimer(tag='inv.tcgen')

    if(len(dtgopt.split('.')) > 1):
        tdtgs=mf.dtg_dtgopt_prc(dtgopt)

    elif(not(mf.find(dtgopt,'cur'))):
        edtg=mf.dtg_command_prc(dtgopt)
        bdtg=mf.dtginc(edtg,-24*ndayback)
        tdtgopt="%s.%s"%(bdtg,edtg)
        tdtgs=mf.dtg_dtgopt_prc(tdtgopt)

    else:
        bdtg="cur12-d%d"%(ndayback)
        tdtgopt="%s.cur12"%(bdtg)
        tdtgs=mf.dtg_dtgopt_prc(tdtgopt)

    invpath="%s/inv.tcgen.txt"%(webdir)

    if(gendtgs != None):
        tdtgs=gendtgs
        invpath="%s/inv.tcgen.%s.txt"%(webdir,invopt)

    MF.ChangeDir(webdir)


    #ttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt
    # tc hashes
    #
    namesStm={}
    stmsDtg={}
    dtgsStm={}
    genstms=tcD.mdDg.gen1dtg
    gendtgs=genstms.keys()
    gendtgs.sort()

    allgenstms=[]
    for dtg in tdtgs:
        try:
            stms=genstms[dtg]
            for stm in stms:
                stm3=stm[0]
                if(invopt != 'all' and not(stm3 in tstmids)): continue
                (stm3id,stmname)=tcD.getStmName3id(stm3)
                MF.appendDictList(namesStm,stm3,stmname)
                # -- stm <- dtg
                MF.appendDictList(stmsDtg,dtg,stm3)
                # -- dtg <- stm
                MF.appendDictList(dtgsStm,stm3,dtg)
        except:
            None



    stmsDtg=MF.uniqDict(stmsDtg)
    dtgsStm=MF.uniqDict(dtgsStm)
    namesStm=MF.uniqDict(namesStm)


    cards=[]
    cards=cards+MF.PrintDict(stmsDtg,name='hash')
    cards=cards+MF.PrintDict(dtgsStm,name='hash')
    cards=cards+MF.PrintDict(namesStm,name='hash')


    #ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
    # fcst mode hashes
    #

    fdtgsModel={}
    basinsFdtg={}
    fdtgsBasin={}

    modelsFdtgBasin={}
    tausFdtgBasinModel={}

    for dtg in tdtgs:
        year=dtg[0:4]
        maskpng="%s/%s/*.png"%(year,dtg)
        plts=glob.glob(maskpng)

        for plt in plts:
            (dir,file)=os.path.split(plt)
            (base,ext)=os.path.splitext(file)
            tt=file.split('.')
            model=tt[0]
            vdtg=tt[1]
            tau=tt[2]
            basin=tt[3]
            if(invopt != 'all' and not(basin in basins)): continue
            if(verb): print 'FFF model: ',model,dtg,basin,tau,'vvv: ',vdtg

            # -- dtg <- model
            MF.appendDictList(fdtgsModel,model,dtg)
            # -- basins <- fdtg
            MF.appendDictList(basinsFdtg,dtg,basin)
            # -- fdtgs <- basin
            MF.appendDictList(fdtgsBasin,basin,dtg)
            # -- models <- fdtg,basin
            MF.append2TupleKeyDictList(modelsFdtgBasin,dtg,basin,model)
            # -- taus <- fdtg,basin,model
            MF.append3TupleKeyDictList(tausFdtgBasinModel,dtg,basin,model,tau)


    fdtgsBasin=MF.uniqDict(fdtgsBasin)
    basinsFdtg=MF.uniqDict(basinsFdtg)
    fdtgsModel=MF.uniqDict(fdtgsModel)

    modelsFdtgBasin=MF.uniqDict(modelsFdtgBasin)
    tausFdtgBasinModel=MF.uniqDict(tausFdtgBasinModel)

    cards=cards+MF.PrintDict(fdtgsBasin,name='hash')
    cards=cards+MF.PrintDict(basinsFdtg,name='hash')
    cards=cards+MF.PrintDict(fdtgsModel,name='hash')
    cards=cards+MF.PrintDict(modelsFdtgBasin,name='hash')
    cards=cards+MF.PrintDict(tausFdtgBasinModel,name='hash')


    #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
    # veri hashes
    #

    vdtgsModel={}
    basinsVdtg={}
    vdtgsBasin={}

    modelsVdtgBasin={}
    tausVdtgBasinModel={}

    for dtg in tdtgs:
        year=dtg[0:4]
        maskpng="%s/*/*.%s.*png"%(year,dtg)
        plts=glob.glob(maskpng)

        print 'III makeTCgenPhpInventory working dtg: ',dtg

        for plt in plts:
            (dir,file)=os.path.split(plt)
            tt=dir.split('/')
            bdtg=tt[-1]
            (base,ext)=os.path.splitext(file)
            tt=file.split('.')
            model=tt[0]
            vdtg=tt[1]
            tau=tt[2]
            basin=tt[3]
            if(invopt != 'all' and not(basin in basins)): continue
            if(verb): print 'VVV model: ',model,bdtg,basin,tau,'vvv: ',vdtg

            # -- dtg <- model
            MF.appendDictList(vdtgsModel,model,dtg)
            # -- basins <- vdtg
            MF.appendDictList(basinsVdtg,dtg,basin)
            # -- vdtgs <- basin
            MF.appendDictList(vdtgsBasin,basin,dtg)
            # -- models <- vdtg,basin
            MF.append2TupleKeyDictList(modelsVdtgBasin,dtg,basin,model)
            # -- taus <- vdtg,basin,model
            MF.append3TupleKeyDictList(tausVdtgBasinModel,dtg,basin,model,tau)

    vdtgsBasin=MF.uniqDict(vdtgsBasin)
    basinsVdtg=MF.uniqDict(basinsVdtg)
    vdtgsModel=MF.uniqDict(vdtgsModel)

    modelsVdtgBasin=MF.uniqDict(modelsVdtgBasin)
    tausVdtgBasinModel=MF.uniqDict(tausVdtgBasinModel)

    cards=cards+MF.PrintDict(vdtgsBasin,name='hash')
    cards=cards+MF.PrintDict(basinsVdtg,name='hash')
    cards=cards+MF.PrintDict(vdtgsModel,name='hash')
    cards=cards+MF.PrintDict(modelsVdtgBasin,name='hash')
    cards=cards+MF.PrintDict(tausVdtgBasinModel,name='hash')

    rc=MF.WriteList2File(cards,invpath,verb=verb)

    MF.dTimer(tag='inv.tcgen')

    return(1)


def makeTcgenJsInventory(dtgopt,gendtgs,tstmids,basins,invopt='all',
                         gentaus=None,
                         ndayback=5,bdtg=None,verb=0):

    def getGenStmDtg(dtgs):
        ndtg=len(dtgs)
        mdtg=ndtg/2
        hh=dtgs[mdtg][8:]
        if(hh != '00' and hh != '12'): mdtg=mdtg-1
        stmdtg=dtgs[mdtg]
        return(stmdtg)

    from TCtrk import tcgenW3Dir as webdir

    # -- old TcData object -- but has convenient gen1dtg to get gen storms by dtg
    #from TC import TcData as TcDataOld

    # -- 20151019 -- removed
    from tcCL import TcData

    tD=TcData(dtgopt=dtgopt)

    MF.sTimer(tag='inv.tcgen')

    if(len(dtgopt.split('.')) > 1):
        tdtgs=mf.dtg_dtgopt_prc(dtgopt)

    elif(bdtg != None):
        edtg=mf.dtg_command_prc(dtgopt)
        tdtgopt="%s.%s.12"%(bdtg,edtg)
        tdtgs=mf.dtg_dtgopt_prc(tdtgopt)

    elif(mf.find(dtgopt,'ops')):
        edtg=mf.dtg_command_prc(dtgopt)
        bdtg=edtg[0:4]+'010100'
        tdtgopt="%s.%s.12"%(bdtg,edtg)
        tdtgs=mf.dtg_dtgopt_prc(tdtgopt)

    elif(not(mf.find(dtgopt,'cur'))):
        edtg=mf.dtg_command_prc(dtgopt)
        bdtg=mf.dtginc(edtg,-24*ndayback)
        tdtgopt="%s.%s.12"%(bdtg,edtg)
        tdtgs=mf.dtg_dtgopt_prc(tdtgopt)

    else:
        bdtg="cur12-d%d"%(ndayback)
        tdtgopt="%s.cur12"%(bdtg)
        tdtgs=mf.dtg_dtgopt_prc(tdtgopt)

    if(invopt== 'all'):
        invpath="%s/inv.tcgen.js"%(webdir)
    else:
        invpath="%s/inv.tcgen.%s.js"%(webdir,invopt)
        
    tdtgs.sort()

    #print 'qqqqqqqq',dtgopt,gendtgs,' webdir: ',webdir
    #for tdtg in tdtgs:
        #print tdtg

    if(gendtgs != None):
        tdtgs=gendtgs
    
    MF.ChangeDir(webdir)


    allModels=    ['gfs2','fim8','rtfim9','ecm2','ukm2','cmc2','navg']
    allModels=    ['gfs2','ecm2','ukm2','cmc2','navg','fim8','rtfim9']
    allModels=    ['gfs2','ecm2','ukm2','cmc2','navg','fim8'] # 20171030 - fim* is being deprecated
    allModels=    ['gfs2','fv3e','fv3g','ecm2','ukm2','cmc2','navg']   # -- 201801121030 - fim* is being deprecated
    allModels=    ['gfs2','ecm2','ukm2','cmc2','navg']                 # -- 20190201 -- take out fv3? until local runs sorted
    allModels=    ['gfs2','ecm2','fv7e','fv7g']                        # -- 20190326 -- for analyzing fv7 runs on tenki7

    allModels= tcgenModelsJS
    
    allModelButtons={
        'gfs2':'GFS',
        'fim8':'FIM8',
        'rtfim9':'FIM9',
        'ecm2':'ECM',
        'ecm4':'ECM',
        'ecm5':'ECM5',
        'jgsm':'JGSM',
        'era5':'ERA5',
        'ukm2':'UKM',
        'cmc2':'CMC',
        'cgd2':'CMCG',
        'navg':'NAVG',
        'fv3e':'FV3N',
        'fv3g':'FV3G',
        'fv7e':'FV7N',
        'fv7g':'FV7G',
    }

    allModelLabels={
        'gfs2':'ncep GFS',
        'fim8':'esrl FIM8',
        'rtfim9':'esrl FIM9',
        'ecm2':'ecmwf HRES',
        'ecm4':'ecmwf HRES',
        'ecm5':'ecmwf HRES',
        'jgsm':'JMA GSM',
        'ukm2':'ukmo UM',
        'cmc2':'cmc GEM',
        'cgd2':'cmc GDPS',
        'navg':'fnmoc NAVGEM',
        'fv3e':'esrl FV3-NCEP',
        'fv3g':'esrl FV3-GF',
        'fv7e':'esrl FV7-NCEP',
        'fv7g':'esrl FV7-GF',
        
    }


    allModelsData=allModels
    allDomainsALL=['WPAC','EPAC','LANT','NIO','SHEM']
    
    allDomains=[]
    for basin in basins:
        allDomains.append(basin.upper())
    
    allProducts=['prp','v85','uas']
    
    # get stmids


    #ttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt
    # tc hashes
    #
    namesStm={}
    stmsDtg={}
    dtgsStm={}

    allgenstms=[]
    for dtg in tdtgs:

        try:
            igenstms=tD.getGenStmidsByDtg(dtg)
        except:
            None
            
        try:
            stms=igenstms
            for stm in stms:
                if(invopt != 'all' and (tstmids != None and not(stm in tstmids))):  continue
                (stm3id,stmname)=tD.getStmName3id(stm)
                MF.appendDictList(namesStm,stm3id,stmname)
                # -- stm <- dtg
                MF.appendDictList(stmsDtg,dtg,stm3id)
                # -- dtg <- stm
                MF.appendDictList(dtgsStm,stm3id,dtg)
                allgenstms.append(stm3id)
                if(verb): print 'tbase.makeTcgenJsInventory() adding stm3:',stm3id,' to tc hashes for dtg: ',dtg
        except:
            None

    stmsDtg=MF.uniqDict(stmsDtg)
    dtgsStm=MF.uniqDict(dtgsStm)
    namesStm=MF.uniqDict(namesStm)

    allgenstms=mf.uniq(allgenstms)

    #ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
    # fcst mode hashes
    #

    fcdtgs=[]

    fdtgsModel={}
    basinsFdtg={}
    fdtgsBasin={}

    modelsFdtgBasin={}
    tausFdtgBasinModel={}

    for dtg in tdtgs:
        year=dtg[0:4]
        maskpng="%s/%s/*.png"%(year,dtg)
        plts=glob.glob(maskpng)

        if(verb): print 'III-FFF makeTCgenInventory working dtg: ',dtg,'maskpng: ',maskpng

        for plt in plts:
            (dir,file)=os.path.split(plt)
            (base,ext)=os.path.splitext(file)
            tt=file.split('.')
            model=tt[0]
            vdtg=tt[1]
            tau=tt[2]
            basin=tt[3]
            if(gentaus != None and (not(int(tau) in gentaus))): 
                print 'makeTcgenJSInventory-tau-not-in-gentaus',gentaus,int(tau)
                continue
            
            bdtg=mf.dtginc(vdtg,-int(tau))
            fcdtgs.append(bdtg)
            if(invopt != 'all' and not(basin in basins)): continue
            if(verb): print 'FFF model: ',model,dtg,basin,tau,'vvv: ',vdtg

            # -- dtg <- model
            MF.appendDictList(fdtgsModel,model,dtg)
            # -- basins <- fdtg
            MF.appendDictList(basinsFdtg,dtg,basin)
            # -- fdtgs <- basin
            MF.appendDictList(fdtgsBasin,basin,dtg)
            # -- models <- fdtg,basin
            MF.append2TupleKeyDictList(modelsFdtgBasin,dtg,basin,model)
            # -- taus <- fdtg,basin,model
            MF.append3TupleKeyDictList(tausFdtgBasinModel,dtg,basin,model,tau)

    fcdtgs=mf.uniq(fcdtgs)
    
    #print 'FFFFFFFFFFFFFF'
    #kks=tausFdtgBasinModel.keys()
    #kks.sort()
    #for kk in kks:
        #print kk
        
    #sys.exit()

    fdtgsBasin=MF.uniqDict(fdtgsBasin)
    basinsFdtg=MF.uniqDict(basinsFdtg)
    fdtgsModel=MF.uniqDict(fdtgsModel)

    modelsFdtgBasin=MF.uniqDict(modelsFdtgBasin)
    tausFdtgBasinModel=MF.uniqDict(tausFdtgBasinModel)

    #print 'AAAAAAAAAAAAAAAAAAAAA'
    #kks=tausFdtgBasinModel.keys()
    #kks.sort()
    #for kk in kks:
        #print kk,'taus: ',tausFdtgBasinModel[kk]
    #sys.exit()



    #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
    # veri hashes
    #

    vcdtgs=[]

    vdtgsModel={}
    basinsVdtg={}
    vdtgsBasin={}

    modelsVdtgBasin={}
    tausVdtgBasinModel={}

    for dtg in tdtgs:
        year=dtg[0:4]
        maskpng="%s/%s/*.veri.*png"%(year,dtg)
        plts=glob.glob(maskpng)

        if(verb): print 'III-VVV makeTCgenInventory working dtg: ',dtg

        for plt in plts:
            (dir,file)=os.path.split(plt)
            tt=dir.split('/')
            bdtg=tt[-1]
            (base,ext)=os.path.splitext(file)
            tt=file.split('.')
            model=tt[0]
            vdtg=tt[1]
            
            # -- skip verifying dtgs outside range
            #
            if(not(vdtg in tdtgs)): continue
            
            vcdtgs.append(vdtg)
            tau=tt[2]
            if(gentaus != None and (not(int(tau) in gentaus))): continue
            basin=tt[3]
            if(invopt != 'all' and not(basin in basins)): continue
            if(verb): print 'VVV model: ',model,bdtg,basin,tau,'vvv: ',vdtg,'tdtg: ',dtg

            # -- dtg <- model
            MF.appendDictList(vdtgsModel,model,dtg)
            # -- basins <- vdtg
            MF.appendDictList(basinsVdtg,dtg,basin)
            # -- vdtgs <- basin
            MF.appendDictList(vdtgsBasin,basin,dtg)
            # -- models <- vdtg,basin
            MF.append2TupleKeyDictList(modelsVdtgBasin,dtg,basin,model)
            # -- taus <- vdtg,basin,model
            MF.append3TupleKeyDictList(tausVdtgBasinModel,vdtg,basin,model,tau)


    vcdtgs=mf.uniq(vcdtgs)

    vdtgsBasin=MF.uniqDict(vdtgsBasin)
    basinsVdtg=MF.uniqDict(basinsVdtg)
    vdtgsModel=MF.uniqDict(vdtgsModel)

    modelsVdtgBasin=MF.uniqDict(modelsVdtgBasin)
    tausVdtgBasinModel=MF.uniqDict(tausVdtgBasinModel)

    #jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj

    allDtgs=mf.uniq(fcdtgs+vcdtgs)

    invt="""	allTaus = [	

"""
    for tau in gentaus:
        invt=invt+"""    '%d',
"""%(tau)
   
    invt=invt+"""
    ]
"""
    
    inv="""
    // fixed vars

    var allModels = [
"""

    for model in allModels:
        inv=inv+"""    '%s',
"""%(model)

    inv=inv+"""
     ];

    var modelLabels =  [
"""
    
    for model in allModels:
        inv=inv+"""    '%s',
"""%(allModelLabels[model])
        
    inv=inv+'''
      ];

    var allDomains = %s;
	var allProducts = %s;

%s

'''%(str(allDomainsALL),str(allProducts),invt)

    stormDict={}
    dtgDict={}
    domainDict={}

    inv=inv+'''
    var allDtgs = [
'''

    allDtgs.reverse()

    n=0
    for dtg in allDtgs:
        n=n+1
        inv=inv+"""   '%s',"""%(dtg)
        if(n%10 == 0): inv=inv+'\n'

    inv=inv+"""
        ]

    var modelButton2Model = new Array()
    var modelModel2Button = new Array()
    """

    for key,val in allModelButtons.items():
        inv=inv+"""
	modelModel2Button['%s']='%s'
    modelButton2Model['%s']='%s'
"""%(key,val,val,key)


    inv=inv+"""

    var stormDict= new Array()

"""



    allStorms=[]

    for stm in allgenstms:
        
        basin=Basin1toFullBasin[stm[-1].upper()].upper()
        allstorm="%s [%s]"%(stm,namesStm[stm][0])
        if(Is9X(stm)): continue
        stmdtg=getGenStmDtg(dtgsStm[stm])

        inv=inv+"""    stormDict['%s'] = ['%s','%s']
"""%(allstorm,basin,stmdtg)
        allStorms.append(allstorm)

    inv=inv+"""
    var allStorms = [
"""
    for astm in allStorms:
        inv=inv+"""   '%s',
"""%(astm)

    inv=inv+"""    ]

	domainDict = new Array()

"""

    for basin in fdtgsBasin.keys():

        basdtgs=fdtgsBasin[basin]
        basdtgs.reverse()
        bname=basin.upper()
        inv=inv+"""    
     domainDict['%s'] = [
"""%(bname)
        n=0
        for basdtg in basdtgs:
            n=n+1
            inv=inv+"""  '%s',"""%(basdtg)
            if(n%10 == 0): inv=inv+"\n"

        inv=inv+"""    ]
"""

    inv=inv+"""
     dtgDict=new Array()
"""

    for dtg in allDtgs:

        
        inv=inv+"""

     dtgDict['%s'] = {"""%(dtg)

        for model in allModelsData:
            fctaus=[]
            ifctaus=[]
            vrtaus=[]
            ivrtaus=[]

                
            # -- got after lant...but if this failed...
            failed=0
            try:
                obasin=allDomains[0].lower()
                fctaus=tausFdtgBasinModel[dtg,obasin,model]
            except:
                fctaus=[]
                failed=1
                
            # -- failed so try epac
            if(failed):
                failed=0
                try:
                    obasin=allDomains[1].lower()
                    fctaus=tausFdtgBasinModel[dtg,obasin,model]
                except:
                    fctaus=[]
                    failed=1
                
                
            if(verb): print 'FFF-DDD ',dtg,obasin,model,'fctaus: ',fctaus


            try:
                vrtaus=tausVdtgBasinModel[dtg,allDomains[0].lower(),model]
            except:
                vrtaus=[]

            for fctau in fctaus:
                itau=int(fctau)
                ifctaus.append('%d'%(itau))

            for vrtau in vrtaus:
                itau=int(vrtau)
                ivrtaus.append('%d'%(itau))


            #fcst=""" '%sfcst':[ %s,%s ] """%(allModels[allModelsData.index(model)],str(allProducts),str(ifctaus))   
            #veri=""" '%sveri':[ %s,%s ] """%(allModels[allModelsData.index(model)],str(allProducts),str(ivrtaus))
            #use model data name for plot files...
            # mod tcGenJqery.js to convert label model to data model...

            fcst=""" '%sfcst':[ %s,%s ] """%(model,str(allProducts),str(ifctaus))   
            veri=""" '%sveri':[ %s,%s ] """%(model,str(allProducts),str(ivrtaus))   

            ostr="%s , %s, "%(fcst,veri)
            inv=inv+"""
     %s"""%(ostr)

        inv=inv+"""
     }"""

    if(verb):
        print
        print inv
        print

    rc=MF.WriteString2File(inv,invpath,verb=verb)


def makePrwInventory(loopdir,nDtgButtons=5,verb=0):

    from w2local import W2
    w2=W2()

    allModelsAll=['GFS2','FIM8','GOES']
    allModelsAll=['GFS2','FV3G','GOES'] # -- 20180115 deprecate fim*
    allModelsAll=['GFS2','GOES']        # -- 20200303 FV3 before GSL shutdown*
    #allDomainsAll=['WPAC','EPAC','LANT','ENSO','IO','SPAC']
    allDomainsAll=['WPAC','CPAC','EPAC','LANT','IO','SPAC']

    allDtgs=[]
    allModels=[]
    allDomains=[]

    dtgDictModels={}
    dtgDictDomains={}

    plots=glob.glob("%s/*.gif"%(loopdir))
    for plot in plots:
        (dir,file)=os.path.split(plot)
        tt=file.split('.')
        prod=tt[0]
        model=tt[1]
        if(prod == 'gfs'):
            dtg=tt[4]
            area=tt[3]
        elif(prod == 'w2loop'):
            continue
        else:
            dtg=tt[2]
            area=tt[3]
        if(area[0:3] == 'prw'): area=area[3:].lower()
        ##print file
        ##print 'ppp',prod,model,dtg,area
        allDtgs.append(dtg)
        model=model.upper()
        area=area.upper()

        allModels.append(model)
        allDomains.append(area)
        MF.appendDictList(dtgDictModels,dtg,model)
        MF.appendDictList(dtgDictDomains,dtg,area)


    MF.uniqDictList(dtgDictDomains)
    MF.uniqDictList(dtgDictModels)

    allDomains=mf.uniq(allDomains)
    allModels=mf.uniq(allModels)
    allDtgs=mf.uniq(allDtgs)

    inv='''

    var allModels = %s
    var allDomains = %s

    var allDtgs = [

'''%(str(allModelsAll),str(allDomainsAll))

    allDtgs.reverse()

    for dtg in allDtgs:
        inv=inv+"""   '%s',
"""%(dtg)


    inv=inv+"""
    ]

    var dtgDict= new Array()

"""

    def sortModels(models,allmodels):
        omodels=[]
        for amodel in allmodels:
            for model in models:
                if(model == amodel): 
                    omodels.append(model)

        return(omodels)

    def sortDomains(domains,alldomains):
        odomains=[]
        for adomain in alldomains:
            for domain in domains:
                if(domain == adomain): odomains.append(domain)

        return(odomains)

    for dtg in allDtgs:

        odom=dtgDictDomains[dtg]
        odom=sortDomains(odom,allDomainsAll)
        odomlist=str(odom)

        omod=dtgDictModels[dtg]
        omod=sortModels(omod,allModelsAll)
        omodlist=str(omod)

        card="""    dtgDict['%s'] = [ %-30s , %-s ]"""%(dtg,omodlist,odomlist)

        inv=inv+card+'\n'
        #print 'CCC: ',card
        #print dtg,dtgDictModels[dtg],dtgDictDomains[dtg],cc

    inv=inv+'''
    var numDTGweb = %i;

    allFrames = [   
    '-48',
    '-24',
    '+0' ,
    '+24',
    '+48',
    '+72'
    ]
    '''%(nDtgButtons)

    if(verb):
        print
        print 'prwInv.js:'
        print inv
        print

    invpath="%s/prwInv.js"%(w2.W2BaseDirWeb)
    rc=MF.WriteString2File(inv,invpath,verb=verb)


def sortStmidsMD2update(stm1ids):

    stm1ids.sort()
    basinorder=['l','e','c','w','i','a','b','s','p','q']
    ostm1ids=[]

    for bo in basinorder:
        for stm1id in stm1ids:
            b1id=stm1id.split('.')[0][-1]
            if(bo.upper() == b1id): ostm1ids.append(stm1id)

    stm1ids=ostm1ids
    ostm1ids=[]
    for bo in basinorder:
        stm9x=[]
        stmNN=[]
        for stm1id in stm1ids:
            b1id=stm1id.split('.')[0][-1]
            snum=int(stm1id.split('.')[0][0:2])
            if(snum >= 90 and (bo.upper() == b1id) ): stm9x.append(stm1id)
            if(snum <= 79 and (bo.upper() == b1id) ): stmNN.append(stm1id)
        ostm1ids=ostm1ids+stm9x+stmNN

    return(ostm1ids)

    
#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# unbounded methods for the classes
#
        
def initDSsMD2Keys(DSs,override=0,md2key='md2keys'):

    try:
        md2=DSs.getDataSet(key=md2key)
    except:
        md2=None

    if(md2 == None or override):
        DSs.mddtgs=[]
        DSs.mddtgsBT=[]
        DSs.mdstmids=[]
        DSs.mdstmidsCC=[]
    else:
        DSs.mddtgs=md2.mddtgs
        DSs.mddtgsBT=md2.mddtgsBT
        DSs.mdstmids=md2.mdstmids
        DSs.mdstmidsCC=md2.mdstmidsCC
    return

# -- dss put methods for stms and dtgs
#
def putDssSmdDataSet(DSs,smD,stmid,verb=0):

    DSs.putDataSet(smD,key=stmid,verb=verb)
    if(not(stmid in DSs.mdstmids)):
        DSs.mdstmids.append(stmid)
        if(verb): print 'PPP putting stmid: ',stmid,' to DSs.mdstmids'


def putDssSmdCCDataSet(DSs,smD,stmid,verb=0):

    DSs.putDataSet(smD,key=stmid,verb=verb)
    if(not(stmid in DSs.mdstmidsCC)):
        DSs.mdstmidsCC.append(stmid)
        if(verb): print 'PPP putting CC stmid: ',stmid,' to DSs.mdstmidsCC'



def putDssDtgDataSet(DSs,dds,dtg,verb=0):

    DSs.putDataSet(dds,key=dtg,verb=verb)
    if(not(dtg in DSs.mddtgs)):
        DSs.mddtgs.append(dtg)



def putDssDtgBTDataSet(DSs,dds,dtg,verb=0):

    DSs.putDataSet(dds,key=dtg,verb=verb)
    if(not(dtg in DSs.mddtgsBT)):
        DSs.mddtgsBT.append(dtg)

    

def putDSsMD2Keys(DSs,override=0,md2key='md2keys',verb=0):

    from tcCL import MD2Keys
    md2=MD2Keys(DSs.mddtgs,DSs.mddtgsBT,DSs.mdstmids,DSs.mdstmidsCC)
    DSs.putDataSet(md2,key=md2key,verb=verb)

        

def setDSsMD2Keys(DSs,override=1,md2key='md2keys'):

    from tcCL import MD2Keys

    MF.sTimer('keys')
    md2=DSs.getDataSet(key=md2key)

    if(md2 == None or override):
        mddtgs=[]
        mddtgsBT=[]
        mdstmids=[]
        mdstmidsCC=[]
        kk=DSs.getKeys()

    else:
        return
    
    for k in kk:
        if(mf.find(k,'.')):
            tt=k.split('.')
            if(tt[0].isdigit() and tt[1] == 'bt'):
                mddtgsBT.append(k.lower())
            else:
                mdstmids.append(k.lower())
        else:
            mddtgs.append(k)

    md2=MD2Keys(mddtgs,mddtgsBT,mdstmids)
    DSs.putDataSet(md2,key=md2key)
    
    MF.dTimer('keys')

        
def getCtlpathTaus(model,dtg,maxtau=168,verb=0,doSfc=0):
    
    from w2local import W2
    w2=W2()
    taus=[]
    ctlpath=taus=nfields=tauOffset=None
    rc=w2.getW2fldsRtfimCtlpath(model,dtg,maxtau=maxtau,verb=verb,doSfc=doSfc)
    if(rc == None):
        print 'EEEE---tcVM-getCtlpathTaus-w2base.getW2fldsRtfimCtlpath...sayounara...for model: ',model,' dtg: ',dtg
        sys.exit()
    if(rc[0]):
        ctlpath=rc[1]
        taus=rc[2]
        nfields=rc[-2]
        tauOffset=rc[-1]

    return(ctlpath,taus,nfields,tauOffset)

def getABsDirsPaths(tstmid,useNhcArchive=0,doWorkingBT=0,
                    chkNhcJtwcAdeck=0,doBdeck2=0,
                    verb=0):

    from w2local import W2
    w2=W2()
    
    stm2id=stm1idTostm2id(tstmid)
    
    # -- get the current N/SHEM year
    #
    curdtg=mf.dtg()
    curyearNHEM=curdtg[0:4]
    curyearSHEM=getShemYear(curdtg)
    
    b2id=stm2id[0:2]
    snum=stm2id[2:4]
    byear=stm2id.split('.')[1]

    # -- when cp -> wp IsJtwcBasin = 2
    #
    rcJ=IsJtwcBasin(b2id)
    rcN=IsNhcBasin(b2id)
 
    if(rcJ >= 1):
        abdir=w2.TcAdecksJtwcDir
        if(doBdeck2):
            bbdir=w2.TcBdecksJtwcDir2
        else:
            bbdir=w2.TcBdecksJtwcDir
        
    if(rcJ == 2):
        abdirJ=abdir
        bbdirJ=bbdir

    # -- set nhc if cross basin
    #
    if(rcN):
        abdir=w2.TcAdecksNhcDir
        if(doBdeck2):
            bbdir=w2.TcBdecksNhcDir2
        else:
            bbdir=w2.TcBdecksNhcDir
        
    adeckfile='a%s%s%s.dat'%(b2id,snum,byear)
    bdeckfile='b%s%s%s.dat'%(b2id,snum,byear)
    
    if(rcN and useNhcArchive):
        
        sbdir=w2.NhcDatDir
        sdir="%s/archive/%s"%(sbdir,byear)
        
        adsdir=sdir
        bdsdir=sdir

    else:
        adsdir="%s/%s"%(abdir,byear)
        bdsdir="%s/%s"%(bbdir,byear)
        
    if(doWorkingBT):
        bdsdir="%s/working"%(bdsdir)
        print "tcVM.getABsDirsPaths().doWorkingBT=1 bdsdir: ",bdsdir
        

    # -- 20220528 -- always check...
    #
    # -- a/bdeck in both JTWC and NHC find biggest/youngest 
    # -- only if current year; otherwise strictly follow the a/bdeck source
    #
    
    if(rcJ == 2 and ( (int(byear) == int(curyearNHEM)) ) ):

        print
        print 'III(multiple a/bdecks between JTWC/NHC for tstmid: ',tstmid
        
        adsdir1=adsdir
        adsdir2="%s/%s"%(abdirJ,byear)

        bdsdir1=bdsdir
        bdsdir2="%s/%s"%(bbdirJ,byear)
        
        adcurpath1="%s/%s"%(adsdir1,adeckfile)
        bdcurpath1="%s/%s"%(bdsdir1,bdeckfile)        

        adcurpath2="%s/%s"%(adsdir2,adeckfile)
        bdcurpath2="%s/%s"%(bdsdir2,bdeckfile)
        
        asiz1=MF.getPathSiz(adcurpath1)
        asiz2=MF.getPathSiz(adcurpath2)
        bsiz1=MF.getPathSiz(bdcurpath1)
        bsiz2=MF.getPathSiz(bdcurpath2)
        
        
        undef2=1e20
        ctimei=MF.getCurTimei()
        aage1=aage2=bage1=bage2=undef2
        
        if(asiz1 > 0): (aage1,aa)=MF.PathModifyTimei(adcurpath1) ; aage1=MF.DeltaTimei(ctimei,aage1)
        if(asiz2 > 0): (aage2,aa)=MF.PathModifyTimei(adcurpath2) ; aage2=MF.DeltaTimei(ctimei,aage2)
        if(bsiz1 > 0): (bage1,aa)=MF.PathModifyTimei(bdcurpath1) ; bage1=MF.DeltaTimei(ctimei,bage1)
        if(bsiz2 > 0): (bage2,aa)=MF.PathModifyTimei(bdcurpath2) ; bage2=MF.DeltaTimei(ctimei,bage2)

        is9x=Is9X(tstmid)

        if(verb):
            print 'SSS ',tstmid,is9x
            print 'AAA 1',adcurpath1
            print 'aaa 2',adcurpath2
            print 'BBB 1',bdcurpath1
            print 'bbb 2',bdcurpath2
            
            print 'SSSS ',asiz1,asiz2,bsiz1,bsiz2
            print 'AAAA ',aage1,aage2,bage1,bage2

        # -- 20220528 -- always run check for special cases...
        #
        asizChk=(asiz1 == -999 and asiz2 > 0)

        selectJ=0
        if(chkNhcJtwcAdeck or asizChk):
            
            if(asizChk):
                print 'AAA---III special case of NHC no adeck and JTWC has the adeck'
            
            # -- select newest if 9X
            #
            if(is9x):
                # -- select NHC -- select based on adeck undefined (case where there are old 9x in jtwc)
                #
                if(aage1 < aage2 or (aage1 == undef2 and aage2 == undef2) or (bage1 < bage2) ): 
                    adsdir=adsdir1
                    bdsdir=bdsdir1
                else:
                    adsdir=adsdir2
                    bdsdir=bdsdir2            
                    abdir=abdirJ
                    bbdir=bbdirJ
                    selectJ=1
                    
                # -- 20190525 -- always use NHC for 9X if NHC basin
                #
                if(rcN == 1):
                    adsdir=adsdir1
                    bdsdir=bdsdir1
                    selectJ=0
                    
            # -- if NN 
            #
            else:
                if(asiz1 == -999):
                    selectJ=1
                    
                elif(asiz1 >= asiz2 or bsiz1 >= bsiz2):
                    adsdir=adsdir1
                    bdsdir=bdsdir1
                    
                # -- 20220528 -- case where NHC has no adeck and JTWC does...
                #
                    
                else:
                    adsdir=adsdir2
                    bdsdir=bdsdir2
                    abdir=abdirJ
                    bbdir=bbdirJ
                    selectJ=1
                    
                if(verb):
                    print 'FFF-NNN adsdir: ',tstmid,adsdir,asiz1,asiz2
                    print 'FFF-NNN bdsdir: ',tstmid,bdsdir,bsiz1,bsiz2
            
        if(selectJ):
                print 'III(select)JTWC -- jjjjjjjjjjjjjjjjjjjjjjjjjjjj -- tstmid: ',tstmid
        else:
            print 'III(select) NHC -- nnnnnnnnnnnnnnnnnnnnnnnnnnnn -- tstmid: ',tstmid
        print
    
    adarchdir="%s/archive"%(adsdir)
    adarchzippath="%s/%s.zip"%(adarchdir,adeckfile)
    aduniqzippath="%s/%s.uniq.zip"%(adarchdir,adeckfile)
    
    bdarchdir="%s/archive"%(bdsdir)
    bdarchzippath="%s/%s.zip"%(bdarchdir,bdeckfile)
    bduniqzippath="%s/%s.uniq.zip"%(bdarchdir,bdeckfile)
    
    adcurpath="%s/%s"%(adsdir,adeckfile)
    bdcurpath="%s/%s"%(bdsdir,bdeckfile)
    
    if(verb):
        print 'AAAcccccc ',adcurpath
        print 'BBBcccccc ',bdcurpath

    return(snum,b2id,byear,abdir,bbdir,
           adarchdir,adarchzippath,aduniqzippath,
           bdarchdir,bdarchzippath,bduniqzippath,
           adcurpath,bdcurpath)



def get9xABnew(abdir,bbdir,b2id,snum,byear,
               useNhcArchive=0,verb=1):

    
    usenrl=0
    if(int(byear) <= 2009 and IsJtwcBasin(b2id)):
        usenrl=1

    store_invest=0
    # -- not sure why 2011 for nhc from store_invest and not my uniq.zip...
    #    doesn't get to this point in w2-tc-dss-md2.py
    #
    if( (int(byear) >= 2005 and int(byear) <= 2009 or int(byear) == 2011) and IsNhcBasin(b2id) and not(useNhcArchive)):
        store_invest=1
        usenrl=0
    
    rcN=IsNhcBasin(b2id)
    
    if(usenrl):
        abdir='/w21/dat/tc/nrl'
        bbdir=abdir
        

    abcards=''
    
    if(verb): 
        print '909999999999999999999 ',abdir,bbdir,b2id,snum,byear

    amask9x=bmask9x=None
    
    if(store_invest):
        
        abdir9x="%s/store_invest"%(abdir)
        bbdir9x="%s/store_invest"%(bbdir)
        amask="%s/%s/archive/a%s%s%s.dat.%s*"%(abdir,byear,b2id,snum,byear,byear)
        bmask="%s/%s/archive/b%s%s%s.dat.%s*"%(bbdir,byear,b2id,snum,byear,byear)
        amask9x="%s/a%s%s%s.dat.%s*"%(abdir9x,b2id,snum,byear,byear)
        bmask9x="%s/b%s%s%s.dat.%s*"%(bbdir9x,b2id,snum,byear,byear)
        
    elif(useNhcArchive):
        
        from WxMAP2 import W2
        w2=W2()
        
        sbdir=w2.TcDatDirNhc
        sdir="%s/archive/%s"%(sbdir,byear)
        sdir9x="%s/invests"%(sdir)
        
        store_invest=0
        if(int(byear) >= 2005 and int(byear) <= 2012):
            store_invest=1
            sdir9x="%s/archive/store_invest"%(sbdir)
            
        amask="%s/a%s%s%s.dat"%(sdir,b2id.lower(),snum,byear)
        bmask="%s/b%s%s%s.dat"%(sdir,b2id.lower(),snum,byear)

        if(store_invest):
            amask9x="%s/aid/a%s%s%s.dat.%s*"%(sdir9x,b2id,snum,byear,byear)
            bmask9x="%s/btk/b%s%s%s.dat.%s*"%(sdir9x,b2id,snum,byear,byear)
        else:
            amask9x="%s/a%s[A-Z]%s%s.dat"%(sdir9x,b2id.lower(),snum[1],byear)
            bmask9x="%s/b%s[A-Z]%s%s.dat"%(sdir9x,b2id.lower(),snum[1],byear)
        
    elif(usenrl):
        amask="%s/%s/a%s%s%s*dat*"%(abdir,byear,b2id,snum,byear)
        bmask="%s/%s/b%s%s%s*dat*"%(bbdir,byear,b2id,snum,byear)
        
    else:
        amask="%s/%s/a%s[A-Z]%s%s.dat"%(abdir,byear,b2id.lower(),snum[1],byear)
        bmask="%s/%s/b%s[A-Z]%s%s.dat"%(bbdir,byear,b2id.lower(),snum[1],byear)
        

    if(verb):
        print 'AAAAAAAAAAAAAAAAAAAA get9xABnew: ',amask
        print 'BBBBBBBBBBBBBBBBBBBB get9xABnew: ',bmask
        print 'AAAAAAAAAAA999999999 get9xABnew: ',amask9x
        print 'BBBBBBBBBBB999999999 get9xABnew: ',bmask9x

    apaths=glob.glob(amask)
    apaths.sort()
    if(amask9x != None): apaths=apaths+glob.glob(amask9x)

    bpaths=glob.glob(bmask)
    bpaths.sort()
    if(bmask9x != None): bpaths=bpaths+glob.glob(bmask9x)

    for apath in apaths:
        if(verb): print 'aaaaaaaaaaaaaaaaaaa ',apath
        abcards=abcards+MF.ReadFile2String(apath)

    for bpath in bpaths:
        if(verb): print 'bbbbbbbbbbbbbbbbbbb ',bpath
        abcards=abcards+MF.ReadFile2String(bpath)

    return(abcards)



#uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu
# unbounded methods
#

def getAllStmopt(stmopt):
    
    curyear=mf.dtg()[0:4]
    tt=stmopt.split('.')
    if(len(tt) == 2):
        yearopt=tt[-1]
    else:
        yearopt=curyear
        
    basinopt=tt[0]  
    if(basinopt == 'all'):
        stmbasins="w,e,c,l,i,h"
    elif(mf.find(basinopt,'nh')):
        stmbasins="w,e,c,l,i"
    elif(mf.find(basinopt,'sh')):
        stmbasins="h"
        
    stmbasins=stmbasins.split(',')
        
    stmopt=''
    for n in range(0,len(stmbasins)):
        stmb=stmbasins[n]
        if(n == len(stmbasins)-1):
            stmopt=stmopt+"%s.%s"%(stmb,yearopt)
        else:
            stmopt=stmopt+"%s.%s,"%(stmb,yearopt)
            
    return(stmopt)

    

def getTstmidsAD2FromStmoptDtgopt(stmopt,dtgopt=None,do9Xonly=0,dobt=0,source=None,quiet=1):
    
    from tcCL import TcData
    
    def get9XallStmopt(stmopt):
        
        istmopts=stmopt.split(',')
        if(len(istmopts) > 1):
            allstmopt9X=''
            for istmopt in istmopts:
                stmopt9X=get9XallStmopt(istmopt)
                if(stmopt9X != None):
                    allstmopt9X=allstmopt9X+stmopt9X+','
                    
            allstmopt9X=allstmopt9X[0:-1]
            if(len(allstmopt9X) < 3): allstmopt9X=None
            return(allstmopt9X)
                
            
        stmopt9X=None
        tt2=stmopt.split('.')
        
        if(not(Is9Xstmopt(stmopt))): return(stmopt9X)
        
        if(len(tt2) == 1):

            if(len(stmopt) >= 3):
                stmopt9X='9'+stmopt[1:]
            elif(len(stmopt) == 1):
                stmopt9X='9x'+stmopt
                
        elif(len(tt2) == 2):
            if(len(tt2[0]) == 1): 
                stmopt9X='9x'+stmopt[0:]
            elif(len(tt2[0]) == 3):
                stmopt9X='9x'+stmopt[2:]
                
        return(stmopt9X)
            
    
    if(not(quiet)): MF.sTimer('gettD-tstmids')
    tstmids9Xall=[]
    tstmid9s=[]

    if(stmopt != None):
        tD=TcData(stmopt=stmopt)
        tstmids=tD.makeStmListMdeck(stmopt,dobt=dobt,doSubbasin=1,cnvSubbasin=1)
        stmopt9X=get9XallStmopt(stmopt)
        dobt9X=0
        if(stmopt9X != None):
            tstmids9Xall=tD.makeStmListMdeck(stmopt9X,dobt=dobt9X,doSubbasin=1,cnvSubbasin=1)

        tstmid9s=[]
        tstmidNs=[]
        for tstmid in tstmids:
            if(Is9X(tstmid)): 
                tstmid9=tD.makeStmListMdeck(tstmid,dobt=0,doSubbasin=1,cnvSubbasin=1)
                tstmid9s.append(tstmid9[0].upper())
            else:
                tstmidNs.append(tstmid)
    
    elif(dtgopt != None):
        dtgs=mf.dtg_dtgopt_prc(dtgopt)
        tD=TcData(dtgopt=dtgopt)

        tstmid9s=[]
        tstmidNs=[]
        
        for dtg in dtgs:
            stmidsDic=tD.getRawStm1idDtg(dtg,selectNN=0,verb=0)
            ostmids=tD.getDSsDtg(dtg,dobt=0)
            tstmidsRaw=stmidsDic.keys()
            tstmidsBT=tD.getStmidDtg(dtg,dobt=1)
            tstmidsAA=tD.getStmidDtg(dtg,dobt=0)
            for tstmidR in tstmidsRaw:
                if(Is9X(tstmidR)):
                    tstmidR=tD.get9XSubbasinFromStmid(tstmidR)
                    tstmid9s.append(tstmidR)
                    
                elif(IsNN(tstmidR)):
                    tstmidR=tD.getSubbasinStmid(tstmidR)
                    tstmidNs.append(tstmidR)
                    
            tstmid9s=mf.uniq(tstmid9s)
            tstmidNs=mf.uniq(tstmidNs)
            
        tstmids9Xall=tstmid9s
    

    tstmids=tstmid9s+tstmidNs
    if(do9Xonly):                                              tstmids=tstmid9s
    if(dobt or (source != None and mf.find(source,'ecm'))):  tstmids=tstmidNs
    
    if(not(quiet)): MF.dTimer('gettD-tstmids')
    
    # -- check if no NN storms
    #
    if(len(tstmids) == 0 and len(tstmids9Xall) > 0): tstmids=tstmids9Xall
    return(tstmids,tD,tstmids9Xall)


def stm1to2id(stmid): 
    b1id=stmid[2]
    bnum=stmid[0:2]
    b1year=stmid.split('.')[1]
    
    stm2id="%s%s.%s"%(Basin1toBasin2[b1id].lower(),bnum,b1year)
    return(stm2id)
