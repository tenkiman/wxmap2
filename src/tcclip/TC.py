"""
config for TC processing
"""

import os
import sys
import string

BaseDirData="/dat/nwp/dat/tc"
BaseDirPrc="/home/fiorino/era/tc/prc/tctrack"

FtOpsDir=BaseDirData+"/ft_ops"
FtExpDir=BaseDirData+"/ft_exp"
VeriOpsDir=BaseDirData+"/veri_ops"
VeriExpDir=BaseDirData+"/veri_exp"

BtNeumannDir=BaseDirData+"/bt_neumann"
BtOpsDir=BaseDirData

from math import atan2
from math import atan
from math import pi
from math import cos
from math import sin
from math import log
from math import tan
from math import acos
from math import sqrt

#
# constants
#

pi4=pi/4.0
pi2=pi/2.0

deg2rad=pi/180.0
rad2deg=1.0/deg2rad
rearth=6371.0
km2nm=60.0/(2*pi*rearth/360.0)
nm2km=1.0/km2nm
knots2ms=1000/(km2nm*3600)
ms2knots=1/knots2ms
tcunits='metric'
tcunits='english'

vmaxTS=35.0
vmaxTY=65.0


MfLibrary='/home/mfiorino/lib/python'

Reanal={
    
    'era40.fc.256':('era40','stream1',(1989010100,1989123118),'e4.fc.256','era40.fc',24,'era40.256.fc'),
    'cliper.fc':('cliper','cliper',(1957080100,2002010100),'cliper.fc','cliper.fc',24,'clp'),
    
    'era40.an.012':('era40','stream1',(1986090100,1988103118),'e4.an.012','era40.an',6,'era40.012.an'),
    'era40.an.017':('era40','stream1',(1988110100,1989033118),'e4.an.017','era40.an',6,'era40.017.an'),
    'era40.an.018':('era40','stream1',(1989010100,1993083118),'e4.an.018','era40.an',6,'era40.018.an'),
    'era40.an.245':('era40','stream2',(1957080100,1958123118),'e4.an.245','era40.an',6,'era40.245.an'),
    'era40.an.251':('era40','stream3',(1972010100,1972123118),'e4.an.251','era40.an',6,'era40.251.an'),
    
    'ncepr1':('ncep','r1',(1955010100,2000123118),'ncepr1','ncepr1.an',6,'ncepr1.mrf.an'),

    }



def ReanalAttrLs(pyfile):
    
    print "Reanal Opt    Reanal  bdtg       edtg       exp       trkopt   rdt  rexptrk\n"

    for rr in Reanal.keys():
        
        (rname,rbdtg,redtg,rexp,rtrkopt,rdt,rexptrk)=ReanalAttr(rr)

        print "%12s %6s %s %s %-10s %-10s %02d %s"%(rr,rname,rbdtg,redtg,rexp,rtrkopt,rdt,rexptrk)

    print "Sample usage:\n"
    print "%s  era40.fc.246 1989010112 1989020112\n"%(pyfile)
    sys.exit()




def ReanalAttr(rr):
    
    attr=Reanal[rr]
    
    rname=attr[0]
    rbdtg=attr[2][0]
    redtg=attr[2][1]
    rexp=attr[3]
    rtrkopt=attr[4]
    rdt=attr[5]
    rexptrk=attr[6]

    return(rname,rbdtg,redtg,rexp,rtrkopt,rdt,rexptrk)

def ReanalCheck(rr):

    rc=0
    for r in Reanal.keys():
        if(rr == r): rc=1

    return(rc)


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
    tt=string.split(card)
    ttt=(tt[0],tt[1],tt[2],tt[2][0:2],tt[2][2:3],tt[3],tt[4],tt[6],tt[7],tt[9],tt[10],tt[12],tt[14],tt[16],
         tt[25],tt[26])
    return(ttt)



def gc_dist(rlat0,rlon0,rlat1,rlon1):

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

def dist_err(blat,blon,blat1,blon1,flat,flon):

    verb=0
    (xa,ya)=mercat(flat,flon)
    (xb,yb)=mercat(blat,blon)
    (xr,yr)=mercat(blat1,blon1)

    difx=xb-xr
    dify=yb-yr
    if(verb): print 'qqq ',difx,dify

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

    rr=sqrt(biasx*biasx+biasy*biasy)
    #dist_x=abs(biasx)
    #dist_y=abs(biasy)

    if(tcunits =='english'):
        rr=rr*km2nm
        biasx=biasx*km2nm
        biasx=biasx*km2nm
        

    if(verb):
#        print "mmm ",blat,blon,xa,ya,xb,yb,xr,yr,biasx,biasy
        print "mmm ",blat,blon,flat,flon,rr,biasx,biasy

    return(rr,biasx,biasy)


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
    rcourse=float(icourse)
    rspeed=float(ispeed)
    if(verb):
        print "%5.2f %4.0f %5.2f %5.2f %5.2f %5.2f\n"%\
              (distance,icourse,spdmtn,angle,umotion,vmotion)
        
##    return(icourse,ispeed,iumotion,ivmotion)
    return(rcourse,rspeed,rumotion,rvmotion)


def findtc(cdtg,source='neumann'):
    yyyy=cdtg[0:4]
    mm=cdtg[4:6]
    print 'yyyy ',yyyy
    yyyym1=string.atoi(yyyy)-1
    yyyym1=str(yyyym1)
    doprevyear=0
    
    if(source == 'neumann'):
        ddir=BtNeumannDir
        gsource=source
        if(mm == '01' or mm == '02'): doprevyear=1
            
    elif(source == 'ops'):
        ddir=BtOpsDir
        if(yyyy=='2001'):
            gsource='local.jtwc.realtime'
            gsource='local.jtwc'
        else:
            gsource='ngtrp'

    if(doprevyear):
        cmd='( grep -h %s %s/%s/bt.%s.???.* | grep -v lonbnd ; grep -h %s %s/%s/bt.%s.* | grep -v lonbnd )'%\
             (cdtg,ddir,yyyy,gsource,cdtg,ddir,yyyym1,gsource)
    else:
        cmd='grep -h %s %s/%s/bt.%s.???.* | grep -v lonbnd'%(cdtg,ddir,yyyy,gsource)

    tcs=os.popen(cmd).readlines()

    return(tcs)


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

    
def cliperinput(dtg,source='neumann'):

    verb=0
    
    tcs=findtc(dtg)
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

