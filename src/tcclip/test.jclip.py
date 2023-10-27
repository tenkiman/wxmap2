#!/usr/bin/env python

import sys
import jclip23 as jclip 
import nclip23 as nclip
import TC as tc

#
#  initial position in deg N and deg E
#


case='swpac'
case='seio'
case='sio'
case='nio'
case='lant'
case='wpac'
case='epac'

idtg=89010100
vmax=60.0
dir=270.0
spd=10.0

if(case == 'wpac'):
    lat0=20.0
    lon0=140.0
elif(case == 'swpac'):
    idtg=89010100
    lat0=-15.0
    lon0=160.0
    vmax=60.0
    dir=270.0
    spd=10.0
elif(case == 'seio'):
    idtg=89010100
    lat0=-20.0
    lon0=120.0
    dir=270.0
    spd=10.0
    vmax=60.0
elif(case == 'sio'):
    idtg=89010100
    lat0=-15.0
    lon0=80.0
    dir=270.0
    spd=10.0
    vmax=60.0
elif(case == 'nio'):
    idtg=89100100
    lat0=18.0
    lon0=65.0
    dir=180.0
    spd=5.0
    vmax=35.0
elif(case == 'lant'):
    idtg=89100100
    lat0=18.0
    lon0=65.0 # W
    lon0=360-lon0
    dir=270.0
    spd=15.0
    vmax=35.0
    sid='01L'
elif(case == 'epac'):
    idtg=89100100
    lat0=18.0
    lon0=120.0 # W
    lon0=360-lon0
    dir=270.0
    spd=15.0
    vmax=105.0
    sid='01L'
    
else:
    sys.exit()

(latm12,lonm12)=tc.rumltlg(dir,spd,-12.0,lat0,lon0)
(latm24,lonm24)=tc.rumltlg(dir,spd,-24.0,lat0,lon0)

print "M12: %6.1f  %6.1f"%(latm12,lonm12)
print "M24: %6.1f  %6.1f"%(latm24,lonm24)


#nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn
#
#  check for NHC clipers first
#
#nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn

center='JTWC'
basin=tc.tcbasin(lat0,lon0)

if(basin == 'EPC' or basin == 'ATL'):

    # convert lon to deg W for input

    lon0w=360.0-lon0
    lonm12w=360.0-lonm12
    lonm24w=360.0-lonm24

    if(basin == 'EPC'):
        print "EEEEEEEEEEEEEEE"
        #nclip.epcl84(89010100,20.0,120.0,20.0,119.0,20,118.0,270.0,10.0,60.0,'01E')
        nclip.epcl84(idtg,lat0,lon0w,latm12,lonm12w,latm24,lonm24w,dir,spd,vmax,sid)

    elif(basin == 'ATL'):
        print "LLLLLLLLLLLLLLLLL"
        #nclip.atclip(89070100,20.0,80.0,270.0,10.0,270.0,10.0,60.0,'01L')
        nclip.atclip(idtg,lat0,lon0w,dir,spd,dir,spd,vmax,sid)

    
    flat=nclip.cliper.flat
    flon=nclip.cliper.flon
    for i in range(7):
        print"%5.2f  %5.2f"%(flat[i],flon[i])

    
    center='NHC'
    

#jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj
#
#  JTWC clipers
#
#jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj

#
#  calculate appropriate cliper model
#

nsind=-999


if( lat0>  3.0 and lat0< 45.0 ):
    if( lon0>=100.0 and lon0 <=180.0):
        clipermodel='wpclpr'
#
#  NIO
#
    elif(lon0>  0.0 and lon0 < 100.0):
        clipermodel='oclip'
        nsind=1

#
#  CPAC
#
    elif(lon0>180.0 and lon0 <=220.0):
        clipermodel='oclip'
        nsind=4
        
elif( lat0>-45.0 and lat0< -3.0 ):

#
#  SWPAC
#
    if( lon0>=140.0 and lon0 <=225.0 ):
        clipermodel='swpclp'
        nsind=-3
#
#  SEIO
#
    elif( lon0>=100.0 and lon0 <140.0 ):
        clipermodel='seiclp'
        nsind=-2
        
    else:
        clipermodel='oclip'
        nsind = -1 # swio
        
else:
    print "WWWW no jtwc cliper for: ",lat0,lon0
    sys.exit()




print "CCCCC ",clipermodel,nsind

if(clipermodel == 'wpclpr'):
    jclip.wpclpr (idtg,lat0,lon0,latm12,lonm12,latm24,lonm24,vmax)
    lalo=jclip.wpclpfcst.cfcst

elif(clipermodel == 'swpclp'):
    jclip.swpclp (idtg,-lat0,lon0,-latm12,lonm12,-latm24,lonm24,vmax)  # wants + lats
    lalo=jclip.swpclpfcst.cfcst
    for i in range(0,12,2): lalo[i]=-lalo[i] # convert to deg S
    
elif(clipermodel == 'seiclp'):
    jclip.seiclp (idtg,-lat0,lon0,-latm12,lonm12,-latm24,lonm24,vmax)  # wants + lats
    lalo=jclip.seiclpfcst.cfcst
    for i in range(0,12,2): lalo[i]=-lalo[i] # convert to deg S
    

elif(clipermodel == 'oclip'):

    # nsind = -3 spac (lon >= 135.0)
    # nsind = -2 seio (lon >= 100 and lon < 135)
    # nsind = -1 swio (lon < 100)
    # nsind = 4 epac (lon > 220)
    # nsind = 3 cpac (lon > 180 and lon <= 220)
    # nsind = 2 wpac (lon > 100 and lon <= 180)
    # nsind = 1 nio (lon <=100)

    print "QQQ ",nsind
    if(nsind < 0):
        jclip.oclip (nsind,idtg,-lat0,lon0,-latm12,lonm12,-latm24,lonm24)
    else:
        jclip.oclip (nsind,idtg,lat0,lon0,latm12,lonm12,latm24,lonm24)
    
    lalo=jclip.oldclpfcst.cfcst

    #
    # tau 72 in tau 60 for SIO, interpolate
    #
    
    if(nsind == -1):
        print "NNNNN"
        lalo[8]=(lalo[6]+lalo[8])*0.5
        lalo[9]=(lalo[7]+lalo[9])*0.5
    


if(clipermodel == 'wpclpr' or clipermodel == 'swpclp' or clipermodel == 'seiclp'
   or clipermodel == 'oclip' ):

    print lalo

    print "lat lon %5.1f %6.1f"%(lat0,lon0)
    for i in range(6):
        lat=lalo[2*i]
        lon=lalo[2*i+1]
        print "lat lon %5.1f %6.1f"%(lat,lon)


#
# format of output file
#
##  002   01102912
##  14L 278N 0430W  2750 110
##  02S 090S 0842E  2590 110

##  *** 14L  27.8  317.0  275.0   5.5  0  0  0
##  000 14L  26.7  317.4  275.0   5.5  1  4  8
##  012 14L  27.5  315.5  292.9   9.5  1  4  8
##  024 14L  29.5  313.5  320.3  13.5  1  4  8
##  036 14L  33.1  315.2   21.9  19.3 -1 10  0
##  048 14L  37.6  318.1   27.9  25.1 -1  8  0
##  060 14L  40.8  319.3   16.6  16.7 -1  9  0
##  072 14L  99.9  999.9  *****  ****  0  0  0
##  LOST TRACK OF CYCLONE
##  *** 02S  -9.0   84.2  259.0   5.5  0  0  0
##  000 02S  -8.4   82.6  259.0   5.5  4  4  4
##  012 02S  -7.5   82.2  340.8   4.9  1  4  8
##  024 02S  -7.5   82.0  264.3   1.0  1  4  7
##  036 02S  -6.8   80.5  294.6   8.3  1  4  8
##  048 02S  -8.4   79.4  214.2   9.6  1  4  8
##  060 02S  -8.5   79.2  234.9   1.2  1  4  8
##  072 02S  -9.5   79.4  169.6   5.1  1  4  8
##  084 02S -11.4   78.4  206.8  10.6  1  4  8
##  096 02S -12.5   76.7  238.6  10.1  1  4  8
##  108 02S -12.9   74.5  259.2  11.0  3  4  8
##  120 02S -10.4   69.7  298.2  26.8  1  4  8
##  FINISHED TRACKING CYCLONES
