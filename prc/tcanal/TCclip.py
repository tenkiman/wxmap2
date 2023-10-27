""" TC cliper forecasts """

import sys
import string

import mf

import TCw2 as TC

from tcanalsub import *

print 'qqq ',mf.PyVer()

if(mf.PyVer() >= 2.3):
    print 'qqqqqqq'
    try:
        import jclip23 as jclip
    except:
        print 'unable to import jclip23...'
    try:
        import nclip23 as nclip
    except:
        print 'unable to import nclip23...'
else:
    import jclip
    import nclip

verb=0

def NHCcliper(idtg,lat0,lon0,dir,spd,vmax,sid,basin):

    verb=0
    
    (latm12,lonm12)=TC.rumltlg(dir,spd,-12.0,lat0,lon0)
    (latm24,lonm24)=TC.rumltlg(dir,spd,-24.0,lat0,lon0)

    # convert lon to deg W for input

    lon0w=360.0-lon0
    lonm12w=360.0-lonm12
    lonm24w=360.0-lonm24

    if(basin == 'EPC'):
        if(verb): print "EEEEEEEEEEEEEEE"
        #nclip.epcl84(89010100,20.0,120.0,20.0,119.0,20,118.0,270.0,10.0,60.0,'01E')
        nclip.epcl84(idtg,lat0,lon0w,latm12,lonm12w,latm24,lonm24w,dir,spd,vmax,sid)

    elif(basin == 'ATL'):
        if(verb): print "LLLLLLLLLLLLLLLLL"
        #nclip.atclip(89070100,20.0,80.0,270.0,10.0,270.0,10.0,60.0,'01L')
        nclip.atclip(idtg,lat0,lon0w,dir,spd,dir,spd,vmax,sid)

    
    flat=nclip.cliper.flat
    flon=nclip.cliper.flon
    for i in range(0,7): flon[i]=360.0-flon[i] # convert to deg E

    if(verb):
        for i in range(7):
            print"%5.2f  %5.2f"%(flat[i],flon[i])
    
    return(flat,flon)


def JTWCcliper(idtg,lat0,lon0,dir,spd,vmax,sid,basin):

    verb=0

    # ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss
    #
    #  speed check
    #
    # ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss
    
    if(spd > 45.0):
        print "EEEEEEEEEEEE SSSSSSS speed error for: ",sid,' at: ',lat0,lon0,' on: ',idtg
        print "EEEEEEEEEEEE SSSSSSS speed= ",spd
        return([-999.0],[-999.0])

    (latm12,lonm12)=TC.rumltlg(dir,spd,-12.0,lat0,lon0)
    (latm24,lonm24)=TC.rumltlg(dir,spd,-24.0,lat0,lon0)

    #jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj
    #
    #  JTWC clipers
    #
    #jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj

    #
    #  calculate appropriate cliper model
    #

    clipermodel='NULL'
    nsind=-999

    #
    #  NHEM
    #

    if( lat0 >  3.0 ):
        if( lon0>=100.0 and lon0 <=180.0):
            if(lat0 < 45.0 ):
                clipermodel='wpclpr'
            else:
                clipermodel='oclip'
                nsind=2
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
            
    #
    #  SHEM
    #

    elif( lat0 < -3.0 ):

        #
        #  SWPAC
        #
        if( lon0>=140.0 and lon0 <=225.0):
            if( lat0 > -45.0 ):
                clipermodel='swpclp'
                nsind=-3
            else:
                clipermodel='oclip'
                nsind=-3
        #
        #  SEIO
        #
        elif( lon0>=100.0 and lon0 <140.0):
        
            if(lat0 > -45.0):
                clipermodel='seiclp'
                nsind=-2
            else:
                clipermodel='oclip'
                nsind=-2
        
        else:
            clipermodel='oclip'
            nsind = -1 # swio
    
    if(clipermodel == 'oclip'):
        print "WWWW no new jtwc cliper for: ",lat0,lon0


    if(verb): print "CCCCC ",clipermodel,nsind

    if(clipermodel == 'NULL'):
        print "EEEEEEEEEEEE problem with finding a cliper model for: ",sid,' at: ',lat0,lon0,' on: ',idtg
        return([-999.0],[-999.0])

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

        if(verb): print "QQQ ",nsind
        if(nsind < 0):
            jclip.oclip (nsind,idtg,-lat0,lon0,-latm12,lonm12,-latm24,lonm24)
        else:
            jclip.oclip (nsind,idtg,lat0,lon0,latm12,lonm12,latm24,lonm24)

        lalo=jclip.oldclpfcst.cfcst

        #
        # tau 72 in tau 60 for SIO, interpolate
        #

        if(nsind == -1):
            lalo[8]=(lalo[6]+lalo[8])*0.5
            lalo[9]=(lalo[7]+lalo[9])*0.5


    if(clipermodel == 'wpclpr' or clipermodel == 'swpclp' or clipermodel == 'seiclp'
       or clipermodel == 'oclip' ):

        if(verb): print lalo

        flat=[]
        flon=[]

        flat.append(lat0)
        flon.append(lon0)
        
        if(verb): print "lat lon %5.1f %6.1f"%(lat0,lon0)
        
        for i in range(6):
            lat=lalo[2*i]
            lon=lalo[2*i+1]
            flat.append(lat)
            flon.append(lon)
            if(verb): print "lat lon %5.1f %6.1f"%(lat,lon)

    return(flat,flon)

#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
#
# make cliper forecasts and write to file clpath
#
#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

def MakeCliperForecast(dtg,src='bt'):

    verb=0
    icards=TC.findtcs(dtg,srcopt=src)
    ntcs=len(icards)

    if(ntcs == 0):
        print "EEE no TCs for: %s "%(dtg)
        return(0,0)

    hcards=[]
    tccards=[]
    tccards.append("  ")

    #
    # convert to 8 char dtg for cliper legacy application
    #

    idtg=dtg[2:]

    #
    #  Y2K
    #
    yy=string.atoi(dtg[2:4])
    if(yy<10):
        yy=yy+10
        idtg=str(yy)+idtg[2:]

    if(verb): print "YYYY",yy,idtg

    idtg=string.atoi(idtg)

    if(verb): print "DDDDDDDDD ",dtg,idtg
    if(verb): print "NNN: ",ntcs

    hcard=" %03d   %s"%(ntcs,dtg[2:])
    print hcard
    hcards.append(hcard)

    for icard in icards:

        tt=string.split(icard)

        sid=tt[1]
        ivmax=tt[2]
        vmax=string.atof(ivmax)
        lat0=string.atof(tt[4])
        lon0=string.atof(tt[5])
        dir=string.atof(tt[8])
        spd=string.atof(tt[9])


        #
        # if vmax < 30 set to 30
        #
        if(vmax < 30.0): vmax=30.0

        rlat=lat0
        rlon=lon0

        if(lat0>0): ilat="%03d%s"%(lat0*10.0,'N')
        if(lat0<0): ilat="%03d%s"%((-lat0)*10.0,'S')
        if(lon0>=180): ilon="%04d%s"%(((360.0-lon0)*10.0),'W')
        if(lon0<180): ilon="%04d%s"%((lon0*10.0),'E')

        idir="%04d"%(dir*10.0)
        ispd="%03d"%(spd*10.0)


    ##  02S 075S 0827E  2700 030
        hcard=" %s %s %s  %s %s"%(sid,ilat,ilon,idir,ispd)
        print hcard

        hcards.append(hcard)

        print lat0,lon0,dir,spd,vmax,sid

        basin=TC.tcbasin(lat0,lon0)

        if(basin == 'EPC' or basin == 'ATL'):
            (flat,flon)=NHCcliper(idtg,lat0,lon0,dir,spd,vmax,sid,basin)

        else:
            (flat,flon)=JTWCcliper(idtg,lat0,lon0,dir,spd,vmax,sid,basin)

        if(verb): print "FFFFFFFFFFFFFFF",flat[0],flon[0]

        ocard=" *** %s %5.1f %6.1f %6.1f %5.1f  0  0  0"%(sid,lat0,lon0,dir,spd)
        if(verb): print 'aqqq ',ocard
        tccards.append(ocard)

        if(flat[0] != -999.0):
            n=0
            for tau in range(0,84,12):
                lat=flat[n]
                lon=flon[n]
                if(n>0):
                    (dir,spd,umot,vmot)=TC.rumhdsp(flat[n-1],flon[n-1],flat[n],flon[n],12)
                ocard=" %03d %s %5.1f %6.1f %6.1f %5.1f  0  0  0"%(tau,sid,lat,lon,dir,spd)
                if(verb): print ocard
                tccards.append(ocard)
                n=n+1
        else:
            tccards.append('LOST TRACK OF CYCLONE')



            

    return(hcards,tccards)




#222222222222222222222222222222222222222222222222222222222222 new version
#
# make cliper forecasts and write to file clpath
# using input from carq/bdeck parse vice ngtrp
#
#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

def MakeCliperForecast2(dtg,stmids,stmdata,stmmotion):

    verb=0

    hcards=[]
    tccards=[]
    tccards.append("  ")

    #
    # convert to 8 char dtg for cliper legacy application
    #

    idtg=dtg[2:]

    #
    #  Y2K
    #
    yy=string.atoi(dtg[2:4])
    if(yy<10):
        yy=yy+10
        idtg=str(yy)+idtg[2:]
    if(verb): print "YYYY",yy,idtg

    idtg=string.atoi(idtg)

    ntcs=len(stmids)

    if(verb): print "DDDDDDDDD ",dtg,idtg
    if(verb): print "NNN: ",ntcs

    hcard=" %03d   %s"%(ntcs,dtg[2:])
    print hcard
    hcards.append(hcard)

    for stmid in stmids:

        print 'sss ',stmid

        sid=stmid
        posit=stmdata[stmid,'posit']
        clat=posit[1]
        clon=posit[2]
        vmax=float(posit[3])
        stmyear=dtg[0:4]
        
        #
        # shem logic
        #
        if(TC.IsShemBasinStm(sid)):
            (shemoverlap,cy,cyp1)=TC.CurShemOverlap(dtg)
            if(shemoverlap): stmyear=cyp1

        osid="%s.%s"%(stmid.upper(),stmyear)
        

        motion=stmmotion[stmid,'motion']
        idir=int(motion[0])
        ispd=int(motion[1])

        dir=float(idir)
        spd=float(ispd)

        (lat0,lon0,ilat,ilon,hemns,hemew)=TC.Clatlon2Rlatlon(clat,clon)
        ilat=int(ilat)
        ilon=int(ilon)

        print sid,posit
        print ilat,ilon,clat,clon,lat0,lon0
        print vmax,idir,ispd

    ##  02S 075S 0827E  2700 030
        hcard=" %s %03d %04d  %04d %03d"%(osid,ilat,ilon,idir,ispd)
        print hcard

        hcards.append(hcard)

        basin=TC.tcbasin(lat0,lon0)
        print lat0,lon0,dir,spd,vmax,sid

        if(basin == 'EPC' or basin == 'ATL'):
            (flat,flon)=NHCcliper(idtg,lat0,lon0,dir,spd,vmax,sid,basin)

        else:
            (flat,flon)=JTWCcliper(idtg,lat0,lon0,dir,spd,vmax,sid,basin)

        if(verb): print "FFFFFFFFFFFFFFF",flat[0],flon[0]

        ocard=" *** %s %5.1f %6.1f %6.1f %5.1f  0  0  0"%(osid,lat0,lon0,dir,spd)
        if(verb): print 'aqqq ',ocard
        tccards.append(ocard)

        if(flat[0] != -999.0):
            n=0
            for tau in range(0,84,12):
                lat=flat[n]
                lon=flon[n]
                if(n>0):
                    (dir,spd,umot,vmot)=TC.rumhdsp(flat[n-1],flon[n-1],flat[n],flon[n],12)
                ocard=" %03d %s %5.1f %6.1f %6.1f %5.1f  0  0  0"%(tau,osid,lat,lon,dir,spd)
                if(verb): print ocard
                tccards.append(ocard)
                n=n+1
        else:
            tccards.append('LOST TRACK OF CYCLONE')


    return(hcards,tccards)


#333333333333333333333333333333333333333333333 even more new version
#
# make cliper forecasts and write to file clpath
# using input from btops vice carq/bdeck
#
#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

def MakeCliperForecast3(dtg,stmids,stmdata,stmmotion):

    verb=0

    hcards=[]
    tccards=[]
    tccards.append("  ")

    #
    # convert to 8 char dtg for cliper legacy application
    #
    idtg=dtg[2:]

    #
    #  Y2K
    #
    yy=string.atoi(dtg[2:4])
    if(yy<10):
        yy=yy+10
        idtg=str(yy)+idtg[2:]
    if(verb): print "YYYY",yy,idtg

    idtg=int(idtg)

    ntcs=len(stmids)

    if(verb): print "DDDDDDDDD ",dtg,idtg
    if(verb): print "NNN: ",ntcs

    hcard=" %03d   %s"%(ntcs,dtg[2:])

    hcards.append(hcard)

    for stmid in stmids:

        sid=stmid
        tt=stmdata[stmid,'posit']
        ttt=stmmotion[stmid,'motion']
        
        vmax=tt[3]
        rlat=tt[1]
        rlon=tt[2]
        
        dir=ttt[0]
        spd=ttt[1]

        lat0=rlat
        lon0=rlon

        (clat,clon,ilat,ilon,hemns,hemew)=TC.Rlatlon2Clatlon(rlat,rlon)
        
        idir=int(dir*10.0)
        ispd=int(spd*10.0)

        hcard=" %s %s %s  %04d %03d"%(sid,clat,clon,idir,ispd)

        hcards.append(hcard)

        basin=TC.tcbasin(lat0,lon0)

        if(basin == 'EPC' or basin == 'ATL'):
            (flat,flon)=NHCcliper(idtg,lat0,lon0,dir,spd,vmax,sid,basin)

        else:
            (flat,flon)=JTWCcliper(idtg,lat0,lon0,dir,spd,vmax,sid,basin)

        if(verb): print "FFFFFFFFFFFFFFF",flat[0],flon[0]

        ocard=" *** %s %5.1f %6.1f %6.1f %5.1f  0  0  0"%(sid,lat0,lon0,dir,spd)
        if(verb): print 'aqqq ',ocard
        tccards.append(ocard)

        if(flat[0] != -999.0):
            n=0
            for tau in range(0,84,12):
                lat=flat[n]
                lon=flon[n]
                if(n>0):
                    (dir,spd,umot,vmot)=TC.rumhdsp(flat[n-1],flon[n-1],flat[n],flon[n],12)
                ocard=" %03d %s %5.1f %6.1f %6.1f %5.1f  0  0  0"%(tau,sid,lat,lon,dir,spd)
                if(verb): print ocard
                tccards.append(ocard)
                n=n+1
        else:
            tccards.append('LOST TRACK OF CYCLONE')


    return(hcards,tccards)





def Cliper(dtg,clppath):
    
    verb=0
    (hcards,tccards)=MakeCliperForecast(dtg)
    o=open(clppath,'w')
    
    for card in hcards:
        if(verb): print card
        card=card+'\n'
        o.write(card)

    for card in tccards:
        if(verb): print card
        card=card+'\n'
        o.write(card)
        
    o.close()
    


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





