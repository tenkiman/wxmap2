from TC import *
from const import *
from math import * 


def getvrvt ( centerLat, centerLon, lat, lon, u, v):
    
    latdiff = centerLat - lat
    londiff = centerLon - lon 
    
    
    if   ( londiff == 0.0 and latdiff == 0.0 ):
        vr=0.0
        vt=0.0
        uvr=0.0
        vvr=0.0
        uvt=0.0
        vvt=0.0
        return(vr,vt,uvr,vvr,uvt,vvt)
    elif ( londiff <  0.0 and latdiff == 0.0 ): psi = 0.0
    elif ( londiff == 0.0 and latdiff <  0.0 ): psi = pi/2.0
    elif ( londiff >  0.0 and latdiff == 0.0 ): psi = pi
    elif ( londiff == 0.0 and latdiff >  0.0 ): psi = 3.0*pi/2.0
    else:
        
        (hyp_dist) = gc_dist(centerLat, centerLon, lat, lon)
        (opp_dist) = gc_dist(centerLat,centerLon,lat,centerLon)
        (adj_dist) = gc_dist(centerLat,centerLon,centerLat,lon)
        
        sin_value = opp_dist / hyp_dist
        if ( sin_value > 1.0 ): sin_value = 1.0
        sin_angle = asin(sin_value)
        
        cos_value = adj_dist / hyp_dist
        if ( cos_value > 1.0 ): cos_value = 1.0
        cos_angle = acos(cos_value)
        
        theta = 0.5 * ( cos_angle + sin_angle )        
        
        
        if   ( londiff < 0.0 and latdiff < 0.0 ): psi = theta
        elif ( londiff > 0.0 and latdiff < 0.0 ): psi = pi - theta
        elif ( londiff > 0.0 and latdiff > 0.0 ): psi = pi + theta
        elif ( londiff < 0.0 and latdiff > 0.0 ): psi = 2*pi - theta
        else:
            print "Error with getting vr and vt"
    
    (wind) = sqrt(pow(u,2)+pow(v,2))
            
    if   ( u == 0.0 and v == 0.0 ):
        vr=0.0
        vt=0.0
        uvr=0.0
        vvr=0.0
        uvt=0.0
        vvt=0.0
        return(vr,vt,uvr,vvr,uvt,vvt)
    elif ( u >  0.0 and v == 0.0 ): phi = 0.0
    elif ( u == 0.0 and v >  0.0 ): phi = pi/2.0
    elif ( u <  0.0 and v == 0.0 ): phi = pi
    elif ( u == 0.0 and v <  0.0 ): phi = 3.0*pi/2.0
    else:
        sin_value = fabs(v) / wind
        if ( sin_value > 1.0 ): sin_value = 1.0
        sin_angle = asin(sin_value)
        
        cos_value = fabs(u) / wind
        if ( cos_value > 1.0 ): cos_value = 1.0
        cos_angle = acos(cos_value)
        
        chi = 0.5 * ( cos_angle + sin_angle )        
        
        if   ( u > 0.0 and v > 0.0 ): phi = chi
        elif ( u < 0.0 and v > 0.0 ): phi = pi - chi
        elif ( u < 0.0 and v < 0.0 ): phi = pi + chi
        elif ( u > 0.0 and v < 0.0 ): phi = 2.0*pi - chi
        else:
            print "Error with getting vr and vt"
    
    vr = wind * cos ( phi - psi )
    vt = wind * sin ( phi - psi ) 
    
    uvr = vr * cos (psi)
    vvr = vr * sin (psi)
    
    uvt = vt * cos (psi+pi/2.0)
    vvt = vt * sin (psi+pi/2.0)

       
    #print "Center Lat/lon", centerLat, centerLon
    #print "Lat/Lon", lat, lon
    #print "wind", wind
    #print "psi", psi*rad2deg
    #print "phi", phi*rad2deg
    #print "vr,vt", vr,vt 
    #print "uvr,vvr",uvr,vvr
    #print "uvt,vvt",uvt,vvt
    #print "original u,v", u,v
    
    #print "uvr+uvt", uvr+uvt
    #print "vvr+vvt", vvr+vvt
    
    return (vr,vt,uvr,vvr,uvt,vvt)



def getvrvtOld (centerLon,centerLat,lon,lat,u,v,wsp,dir):
    
    (hyp_dist) = gc_dist(centerLat, centerLon, lat, lon)
    
    latdiff = fabs(centerLat - lat)
    londiff = fabs(centerLon - lon)
    
    if ( londiff == 0.0 and latdiff > 0.0 ):
        if ( centerLat > lat ): angle = 180.0
        if ( centerLat < lat ): angle = 0.0
    elif ( londiff > 0.0 and latdiff == 0.0):
        if ( centerLon > lon ): angle = 270.0
        if ( centerLon < lon ): angle = 90.0
    elif ( hyp_dist == 0.0 ):
        vr=0.0
        vt=0.0
        return (vr,vt)
    else:
        (opp_dist) = gc_dist(centerLat,centerLon,lat,centerLon)
        #opp_dist = (lat-centerLat)/360.0 * rearth    
        (adj_dist) = gc_dist(centerLat,centerLon,centerLat,lon) 
        
        #print "clat",centerLat,"clon",centerLon,"lat", lat, "lon", lon, "u/v", u, v
        print "h", hyp_dist, "o", opp_dist, "a", adj_dist
        #print "h", haversine(centerLat,centerLon, lat, lon), "o", haversine(centerLat,centerLon,lat,centerLon), "a", haversine(centerLat,centerLon,centerLat,lon)
         
         
        sin_value = opp_dist / hyp_dist
        if ( sin_value > 1.0 ): sin_value = 1.0
        sin_angle = asin(sin_value) * rad2deg
        
        cos_value = adj_dist / hyp_dist
        if ( cos_value > 1.0 ): cos_value = 1.0
        cos_angle = acos( cos_value ) * rad2deg
        
        #tan_angle = atan(opp_dist/adj_dist)
        
        #tmpangle = 1/3 * (sin_angle + cos_angle + tan_angle)
        
        tmpangle = 0.5 * (sin_angle + cos_angle)
        
        print "temp", tmpangle
        
        if ( lon < 0.0 ): lon = 360.0 + lon            
        
        if ( centerLat <= lat and centerLon <= lon ):
            print "1"
            angle0 = 270 + tmpangle
        elif ( centerLat > lat and centerLon <= lon):
            print '2'
            angle0 = tmpangle
        elif ( centerLat >= lat and centerLon >= lon ):
            print '3'
            angle0 = 90 + tmpangle
        elif ( centerLat < lat and centerLon >= lon ):
            print '4'
            angle0 = 180 + tmpangle  
            
        print angle0
            
        theta = (dir)*deg2rad
        angle = theta - angle0*deg2rad
        
        print angle*rad2deg
        #angle = gc_bearing(centerLat,centerLon, lat, lon)*deg2rad
        
    
    #uvrcomp = (-u) * sin(theta-angle)
    #vvrcomp = (-v) * cos(theta-angle)
    #vr = uvrcomp + vvrcomp
    
    #uvtcomp = (u) * cos(theta-angle)
    #vvtcomp = (-v) * sin(theta-angle)
    #vt = uvtcomp + vvtcomp
    
    #uvrcomp = (u) * sin(angle)
    #vvrcomp = (v) * cos(angle)
    #vr = uvrcomp + vvrcomp
    
    #uvtcomp = (-u) * cos(angle)
    #vvtcomp = (v) * sin(angle)
    #vt = uvtcomp + vvtcomp
    
    vr = wsp * cos (angle)
    vt = wsp * sin (angle)
    
    print "vr, vt", vr, vt
    
    uvrcomp = - vr * cos (angle0)
    vvrcomp = - vr * sin (angle0)
        
    uvtcomp = vt * cos (tmpangle)
    vvtcomp = - vt * sin (tmpangle)   
    
    
    #print "angle", angle
    #print    
    print "mag vr vt", sqrt(pow(vr,2)+pow(vt,2)), "mag u v", sqrt(pow(u,2)+pow(v,2))
    print "theta vr vt", atan((vvrcomp+vvtcomp)/(uvrcomp+uvtcomp))*rad2deg, "theta u v", atan(v/u)*rad2deg
    print "u", u, uvrcomp + uvtcomp, uvrcomp, uvtcomp
    print "v", v, vvrcomp + vvtcomp, vvrcomp, vvtcomp
    
    return(vr,vt,uvrcomp,vvrcomp,uvtcomp,vvtcomp)

def distance (centerLat,centerLon, lat, lon):
    
    centerLat = centerLat * deg2rad
    centerLon = centerLon * deg2rad
    lat = lat * deg2rad
    lon = lon * deg2rad
    
    distance = acos(sin(centerLat)*sin(lat)+cos(centerLat)*cos(lat)*cos(lon-centerLon))*rearth
    
    return distance * km2nm

def haversine (lat0,lon0, lat1, lon1):
    
    lat0 = lat0 * deg2rad
    lon0 = lon0 * deg2rad
    lat1 = lat1 * deg2rad
    lon1 = lon1 * deg2rad
    
    dlat = (lat1-lat0)
    dlon = (lon1-lon0)
    
    a = sin(dlat/2.0) * sin(dlat/2.0) + cos(lat0) * cos(lat1) * sin(dlon/2.0) * sin(dlon/2.0)
    c = 2.0 * atan2(sqrt(a),sqrt(1-a))
    
    d = rearth * c * km2nm
    
    return d

def gc_bearing(cLat,cLon, dlat, dlon):
    
    centerLat = cLat * deg2rad
    centerLon = cLon * deg2rad
    lat = dlat * deg2rad
    lon = dlon * deg2rad
    
    y = sin(lon-centerLon)*cos(lat)
    x = cos(centerLat)*sin(lat) - sin(centerLat)*cos(lat)*cos(lon-centerLon)
    bearing = atan2(y,x) * rad2deg
    
    brng = (bearing + 360) % 360 
    
    return brng
    
#def getvrvt (centerLat, centerLon, lat, lon,u,v):
#    hyp_dist

if ( __name__ == '__main__'):
    
    (vr,vt,uvrcomp,vvrcomp,uvtcomp,vvtcomp)=getvrvt (13,-102,13,-103,-10,-10) 
    #(vr,vt,uvrcomp,vvrcomp,uvtcomp,vvtcomp)=getvrvt (13.93,-102.24,14.205,-102.792,-7.446,-12.514) 
    print
    print
    #(vr,vt,uvrcomp,vvrcomp,uvtcomp,vvtcomp)=getvrvt (13.93,-102.24,17.24,-100.783,-3.939,-0.135)
    #print
    #(vr,vt,uvrcomp,vvrcomp,uvtcomp,vvtcomp)=getvrvt (13.93,-102.24,17.24,-103.601,-3.949,1.495)
    #print
    #(vr,vt,uvrcomp,vvrcomp,uvtcomp,vvtcomp)=getvrvt (13.93,-102.24,10.654,-103.595,0.131,-0.033)
    #print
    #(vr,vt,uvrcomp,vvrcomp,uvtcomp,vvtcomp)=getvrvt (13.93,-102.24,10.654,-100.789,1.487,-0.033)
    
    #,14.562,31)
    
    