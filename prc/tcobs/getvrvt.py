from TC import *
from const import *
from math import * 

def getvrvt(centerLat, centerLon, lat, lon, u, v):

    #hyp_dist = gc_dist(centerLat, centerLon, lat, lon)
    hyp_dist = calcdist(centerLat, centerLon, lat, lon)

    latdiff = abs(centerLat - lat)
    londiff = abs(centerLon - lon)
    
    if ( londiff == 0 and latdiff > 0 ):
        if (centerLat > lat): angle = 180
        if (centerLat < lat): angle = 0
    elif (londiff > 0 and latdiff == 0):
        if (centerLon > lon): angle = 270
        if (centerLon < lon): angle = 90
        
    elif(hyp_dist == 0):
        vr  = 0.0
        vt  = 0.0
        uvr = 0.0
        vvr = 0.0
        uvt = 0.0
        vvt = 0.0
        return(vr,vt,uvr,vvr,uvt,vvt)
    else:
        opp_dist = latdiff/360.0 * (2*pi*rearth)
        #opp_dist = gc_dist(centerLat,centerLon,lat,centerLon)
        sin_value = opp_dist / hyp_dist
        if(sin_value > 1.0): sin_value = 1.0
        sin_angle = asin(sin_value) * rad2deg
        
        #adj_dist = gc_dist(centerLat,centerLon,centerLat,lon)
        adj_dist = calcdist(centerLat,centerLon,centerLat,lon)
        cos_value = adj_dist / hyp_dist
        if(cos_value > 1.0): cos_value = 1.0
        cos_angle = acos(cos_value) * rad2deg
        
        theta = 0.5 * (sin_angle + cos_angle)
        
        if   (centerLat <= lat and centerLon <= lon): psi = 90 - theta
        elif (centerLat >  lat and centerLon <= lon): psi = 90 + theta
        elif (centerLat >= lat and centerLon >= lon): psi = 270 - theta
        elif (centerLat <  lat and centerLon >= lon): psi = 270 + theta
        
    psi = psi*deg2rad
    
    uvrcomp = u * sin(psi)
    vvrcomp = v * cos(psi)
    vr = uvrcomp + vvrcomp
    
    uvtcomp = -u * cos(psi)
    vvtcomp =  v * sin(psi)
    vt = uvtcomp + vvtcomp
    
    vvr = vr * cos(psi)
    uvr = vr * sin(psi)
    
    vvt = -vt * cos(psi + pi/2.0)
    uvt = -vt * sin(psi + pi/2.0)    
    
    return(vr,vt,uvr,vvr,uvt,vvt)
def calcdist(rlatb,rlonb,rlatc,rlonc):
    if (rlatb < 0.0 or rlatc < 0.0 ):
        pole = -90.0
    else:
        pole = 90.0

    distlatb = (pole - rlatb) * deg2rad
    distlatc = (pole - rlatc) * deg2rad
    difflon = abs ( ( rlonb - rlonc ) * deg2rad )

    cosanga =  cos(distlatb) * cos(distlatc) + sin (distlatb) * sin(distlatc) * cos(difflon)

    if (cosanga > 1.0): cosanga = 1.0


    degrees = acos(cosanga) * rad2deg
    circ_fract = degrees / 360
    xdist = circ_fract * ( 2 * pi * rearth)
    
    return(xdist)
