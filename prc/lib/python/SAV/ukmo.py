import os
import sys
import array
import copy
import glob

import mf
import w2


def CuruKmoGribFiles(sdir,dtg):
    print dtg,sdir
    paths=glob.glob("%s/G*"%(sdir))+glob.glob("%s/g*"%(sdir))
    gpaths=[]
    for path in paths:
        (dtimei,ldtg,gdtg)=mf.PathModifyTime(path)
        (dir,file)=os.path.split(path)
        ihr=int(file[3:5])
        bdtg="%s%02d"%(gdtg[0:8],ihr)
        print gdtg
        if(bdtg == dtg):
            gpaths.append(path)

    gpaths.sort()

    return(gpaths)

def kpds2varlev(k5,k6,k7):
    
    if(k5==33 and k6==100):     var='ua' ;  lev='plev'

    elif(k5==34 and k6==100):  var='va' ;  lev='plev'

    elif(k5==7 and k6==100):  var='zg' ;   lev='plev'

    elif(k5==11 and k6 == 100): var='ta' ;  lev='plev'

    elif(k5==40 and k6 == 100): var='umisc' ;  lev='plev'

    elif(k5==52 and k6==100):  var='hur' ;  lev='plev'

    elif(k5==138 and k6==1): var='bvf2' ; lev='sfc'

    elif(k5==2 and k6==102): var='psl' ; lev='sfc'

    elif(k5==51 and k6==1): var='huss' ; lev='sfc10m'

    elif(k5==33 and k6==6): var='uamxw' ; lev='maxwind'

    elif(k5==34 and k6==6): var='vamxw' ; lev='maxwind'

    elif(k5==5 and k6==6): var='uk005' ; lev='maxwind'

    elif(k5==5 and k6==7): var='uk006' ; lev='troplev'

    elif(k5==1 and k6==7): var='pstp' ; lev='troplev'

    elif(k5==11 and k6==7): var='tatp' ; lev='troplev'

    elif(k5==1 and k6==6): var='psmxw' ; lev='maxwind'

    elif(k5==11 and k6==1): var='tas' ; lev='sfc2m'

    elif(k5==143 and k6==1): var='uk143' ; lev=''

    elif(k5==144 and k6==1): var='uk144' ; lev=''

    elif(k5==146 and k6==1): var='uk146' ; lev=''

    elif(k5==147 and k6==1): var='uk147' ; lev=''

    elif(k5==111 and k6==1): var='uk111' ; lev=''

    elif(k5==20 and k6==1): var='uk20' ; lev=''

    elif(k5==59 and k6==1): var='pr' ; lev='sfc'

    elif(k5==61 and k6==1): var='pra' ; lev='sfc'

    elif(k5==33 and k6==1): var='uas' ; lev='sfc10m'

    elif(k5==34 and k6==1): var='vas' ; lev='sfc10m'

    elif(k5==75 and k6==1): var='clh' ; lev=''

    elif(k5==74 and k6==1): var='clm' ; lev=''

    elif(k5==73 and k6==1): var='cll' ; lev=''

    elif(k5==72 and k6==1): var='clc' ; lev=''
#
# 20070906 - new var -- multiple fields?  funny vert lev?
#
    elif(k5==149 and k6==1): var='uk149' ; lev=''

    else:
        print 'EEEE no var fo kpds5: ',k5,k6,k7
        sys.exit()

    return(var,lev)
            


def uKmoCtl(model,dtg,ctlpath,ropt=''):

    hh=dtg[8:10]
    gtime=mf.dtg2gtime(dtg)

    tauend=w2.Model2EtauData(model,int(hh))
    dtau=w2.Model2DtauData(model)
    ntau=(tauend/dtau)+1

    print 'DDDDDDDDDuuuuuuuu ',tauend,dtau,ntau

    ctl="""dset ^ukm.%%iy4%%im2%%id2%%ih2.t%%f3.grb
title LATS GRIB test
undef 1e+20
dtype grib
options template
index ^ukm.%s.gmp
xdef 432 linear -18.750000 0.833333
ydef 324 linear -89.722000 0.555547
zdef 12 levels
1000 950 925 850 700 500 400 300 250 200 
150 100 
tdef  %d linear %s %dhr
vars 32
zg       12    7,100 Geopotential height [m]
ta       12   11,100 Air Temperature [K]
ua       12   33,100 Eastward wind [m/s]
va       12   34,100 Northward wind [m/s]
hur      12   52,100 Relative humidity [%%]
bvf2      0  138,  1,  0,  0 UKMO 138 var [undef]
psl       0    2,102,  0,  0 Mean sea-level pressure [Pa]
huss      0   51,105,  2 Surface specific humidity (2m) [kg/kg]
uamxw     0   33,  6,  0,  0 Tropopause E-W wind [m/s]
vamxw     0   34,  6,  0,  0 Tropopause N-S wind [m/s]
uk005     0    5,  6,  0,  0 UKMO 005 var - moisture? [undef]
uk006     0    6,  6,  0,  0 UKMO 006 var - o3? [undef]
pstp      0    1,  7,  0,  0 Tropopause pressure [Pa]
tatp      0   11,  7,  0,  0 Tropopause temperature [K]
psmxw     0    1,  6,  0,  0 Tropopause pressure [Pa]
tas       0   11,105,  2 Surface (2m) air temperature [K]
uk143     0  143,  1,  0,  0 UKMO 143 var - could? [undef]
uk144     0  144,  1,  0,  0 UKMO 144 var - cloud? [undef]
uk146     0  146,  1,  0,  0 UKMO 146 var - cloud? [undef]
uk147     0  147,  1,  0,  0 UKMO 147 var - ocean? [undef]
pr        0   59,  1,  0,  0 Total precipitation rate [kg/(m^2*s)]
pra       0   61,  1,  0,  0 Total accumulated precip [kg/(m^2)]
uas       0   33,105, 10 Surface (10m) eastward wind [m/s]
vas       0   34,105, 10 Surface (10m) northward wind [m/s]
clh       0   75,  1,  0,  0 Total cloud amount high [%%]
clm       0   74,  1,  0,  0 Total cloud amount MID [%%]
cll       0   73,  1,  0,  0 Total cloud amount low [%%]
clc       0   72,  1,  0,  0 Total cloud amount CONVECTIVE [%%]
waz7     12   40,100         umisc ua var = 700 vertical velocity [m/s???]
uk20      0   20,  1,  0,  0 UKMO 20 var [undef] -- cloud
uk149     0  149,  1,  0,  0 UKMO 149 var  - waves?
uk111     0  111,  1,  0,  0 UKMO 111 var  - rsds -- insolation at sfc
endvars
###--- pr i mm/d = pr*24*3600
"""%(dtg,ntau,gtime,dtau)

    mf.WriteCtl(ctl,ctlpath)

    dogribmap=1
    if(dogribmap):
        cmd="gribmap -E -i %s"%(ctlpath)
        mf.runcmd(cmd,ropt)



def uKmo8inv(wpath,opath):
    try:
        cards=open(wpath).readlines()
    except:
        print 'EEE unable to open: ',wpath


    ocards=[]
    
    nflds=1
    ns=range(0,len(cards),8)
    taus=[]
    for n in ns:
        tt=cards[n].split(':')
        #print tt
        dtg=tt[2].split('=')[1]
        varname=tt[3]
        kpds5=int(tt[4].split('=')[1])
        kpds6=int(tt[5].split('=')[1])
        kpds7=int(tt[6].split('=')[1])
        tr=int(tt[7].split('=')[1])
        p1=int(tt[8].split('=')[1])
        p2=int(tt[9].split('=')[1])

        (ovar,olev)=kpds2varlev(kpds5,kpds6,kpds7)
        levname=tt[11]

        if(tr == 0):
            tau=p1
        elif(tr == 4):
            tau=p2
        else:
            print 'EEEEE bad tau: ',tau
            sys.exit()

        taus.append(tau)
        ocard="%03d %10s %03d %-10s %-10s %4d EE: %03d %03d %8s %-24s"%(nflds,dtg,tau,
                                                                        ovar,olev,kpds7,
                                                                        kpds5,kpds6,
                                                                        varname,levname,
                                                                        )
        print ocard
        ocards.append(ocard)
        mf.WriteList(ocards,opath)
        
        nflds=nflds+1

    taus=mf.uniq(taus)
    return(taus)

def GetExpecteduKmoGrbSiz(tau):
    if(tau <= 120):
        siz=15035868
        siz=14900000
    else:
        siz=3325500
        siz=3000000
    return(siz)

def uKmoFile2Taus(ifile,dtg):

    char2hr={

        'AAT':[0],
        'BBT':[6],
        'CCT':[12],
        'DDT':[18],
        'EET':[24],
        'FFT':[30],
        'GGT':[36],
        'HHT':[42],
        'IIT':[48],
        
        'JJT':[54,60],
        'KKT':[66,72],
        'LLT':[84],
        'MMT':[96],
        'NNT':[108],
        'OOT':[120],
        'PPA':[132,144],
        }

    taus=char2hr[ifile[5:8]]

    return(taus)

