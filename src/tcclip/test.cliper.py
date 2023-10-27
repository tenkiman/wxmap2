#!/usr/bin/env python

import sys
import string
import TC as tc
import TCclip as tcclip
import posix
import posixpath

#
#  initial position in deg N and deg E
#


case='wpac'
case='swpac'
case='seio'
case='sio'
case='nio'
case='lant'
case='epac'
case='nio'

idtg=89010100
vmax=60.0
dir=270.0
spd=10.0

if(case == 'wpac'):
    lat0=20.0
    lon0=140.0
    sid='01W'
elif(case == 'swpac'):
    idtg=89010100
    lat0=-15.0
    lon0=160.0
    vmax=60.0
    dir=270.0
    spd=10.0
    sid='02P'
elif(case == 'seio'):
    idtg=89010100
    lat0=-20.0
    lon0=120.0
    dir=270.0
    spd=10.0
    vmax=60.0
    sid='01S'
elif(case == 'sio'):
    idtg=89010100
    lat0=-15.0
    lon0=80.0
    dir=270.0
    spd=10.0
    vmax=60.0
    sid='01S'
elif(case == 'nio'):
    idtg=89100100
    lat0=18.0
    lon0=65.0
    dir=180.0
    spd=5.0
    vmax=35.0
    sid='01A'
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
    sid='01E'
else:
    sys.exit()


ngpath='./ngtrp.1990090700.txt'
ngpath='./ngtrp.2001103012.txt'
ngpath='./ngtrp.2001102912.txt'
#ngpath='./ngtrp.2016110312.txt'
ngpath='./ngtrp.2016102800.txt'
ngpath='./ngtrp.2016101500.txt'
ngpath='./ngtrp.2016100500.txt'



(ngdir,ngfile)=posixpath.split(ngpath)



hcards=[]
tccards=[]
tccards.append("  ")

print ngdir
print ngfile
tt=string.split(ngfile,'.')
dtg=tt[1]
idtg=dtg[2:]
yy=string.atoi(dtg[2:4])
#
#  handle Y2K
#

if(yy<10):
    yy=yy+10
    idtg=str(yy)+idtg[2:]
 
print "YYYY",yy,idtg

idtg=string.atoi(idtg)

print "DDDDDDDDD ",dtg,idtg

cards=open(ngpath).readlines()

tt=string.split(cards[0])
ncards=tt[0]
ncards=string.atoi(ncards)
print "NNN ",ncards


clppath="/tmp/tc.clp.%s.tracks.txt"%(dtg)


##  005   01103012
##  02S 075S 0827E  2700 030
##  14L 312N 0457W  3550 180
##  15L 139N 0840W  3600 000
##  95E 150N 1120W  3040 304
##  96E 115N 1200W  2850 050


hcards.append(" %03d   %s"%(ncards,dtg[2:]))

for card in cards[1:]:
    
    tt=string.split(card)
    ilat=tt[0]
    ilon=tt[1]
    ivmax=tt[2]
    isnum=tt[3]
    ibasin=tt[4]
    idir=tt[7]
    ispd=tt[8]
    nshem=ilat[-1]
    ewhem=ilon[-1]
    vmax=string.atof(ivmax)
    lat0=string.atof(ilat[0:-1])*0.1
    lon0=string.atof(ilon[0:-1])*0.1
    dir=string.atof(idir)*0.1
    spd=string.atof(ispd)*0.1

    #
    # if vmax < 30 set to 30
    #
    if(vmax < 30.0): vmax=30.0
    
    if(ewhem == 'W'): lon0=360-lon0
    if(nshem == 'S'): lat0=-lat0
    sid=isnum+ibasin
    
##  02S 075S 0827E  2700 030
    hcards.append(" %s %s %s  %s %s"%(sid,ilat,ilon,idir,ispd))

    #    print card[:-1],tt
    print ilat,nshem,ilon,ewhem,ivmax,vmax,isnum,ibasin,idir,ispd
    print lat0,lon0,dir,spd,vmax,sid

    basin=tc.tcbasin(lat0,lon0)

    if(basin == 'EPC' or basin == 'ATL'):
        (flat,flon)=tcclip.NHCcliper(idtg,lat0,lon0,dir,spd,vmax,sid,basin)
        
    else:
        (flat,flon)=tcclip.JTWCcliper(idtg,lat0,lon0,dir,spd,vmax,sid,basin)

    print "FFFFFFFFFFFFFFF"


    ocard=" *** %s %5.1f %6.1f %6.1f %5.1f  0  0  0"%(sid,lat0,lon0,dir,spd)
    tccards.append(ocard)

    print ocard

    n=0
    for tau in range(0,84,12):
        lat=flat[n]
        lon=flon[n]
        if(n>0):
            (dir,spd,umot,vmot)=tc.rumhdsp(flat[n-1],flon[n-1],flat[n],flon[n],12)
        ocard=" %03d %s %5.1f %6.1f %6.1f %5.1f  0  0  0"%(tau,sid,lat,lon,dir,spd)
        tccards.append(ocard)
        print card
        n=n+1
        
    
    #print flat
    #print flon


#
#  output
#

o=open(clppath,'w')

for card in hcards:
    print card
    card=card+'\n'
    o.write(card)

for card in tccards:
    print card
    card=card+'\n'
    o.write(card)

sys.exit()





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

