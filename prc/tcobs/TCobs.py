from math import *
from TC import rumltlg, rumhdsp
from const import *

def gc_ltlg (clat,clon,radius,bearing):
    
    #
    # Calculate the lat and lon of a destination
    # using a given distance and bearing from start point
    #
    
    radius = radius*nm2km
    bearing = bearing*deg2rad
    
    clat = clat*deg2rad
    clon = clon*deg2rad
    
    rlat0 = asin(sin(clat)*cos(radius/rearth) + cos(clat)*sin(radius/rearth)*cos(bearing)) 
    rlon0 = clon + atan2(sin(bearing)*sin(radius/rearth)*cos(clat),cos(radius/rearth)-sin(clat)*sin(rlat0))
    
    rlat0 = rlat0*rad2deg
    rlon0 = rlon0*rad2deg
    
    return(rlat0,rlon0)

def getLatLonArrays(clat,clon,deltaR,R1,R2):
    
    
    lats = []
    lons = []  
    
    print 'Center', clat, clon
    
    initTheta = 0.0
    
    for inc_i in range(int(floor((R2-R1)/deltaR))):
        
        print
    
        R = 0.5*deltaR + R1 + deltaR*inc_i
        
        deltaR = 2*R*sin(pi/4/2)
        
        #print 'Radius', R
    
        (rlat,rlon) = gc_ltlg(clat,clon,R,initTheta)
        
        print 'Start Point', rlat, rlon
   
    
        #deltatheta = deltaR*(360.0/(2.0*pi*R))
        deltatheta = (deltaR/R)*rad2deg
        
        #deltatheta = 2.0*asin(deltaR/(2.0*R))*rad2deg
        
        if ( initTheta < 270.0 ):
            theta_not = initTheta + 90.0
        else:
            theta_not = initTheta - 270.0           
        
        print 'Delta Theta ', deltatheta
        print 'Theta Not', theta_not
        
        #speed = 2.0 * pi * R / deltatheta
        speed = (R*deltatheta)*deg2rad
        #speed = deltaR
        dt = 1.0        
        
        print 'Distance', deltaR*nm2km
        print 'Num Pts', int(floor(360/deltatheta))
    
        for inc_j in range(int(floor(360.0/deltatheta))):
            print rlat, rlon
            lats.append(rlat)
            lons.append(rlon)
            course = theta_not + deltatheta*(inc_j+1)
            
            (rlat,rlon) = rumltlg(course,speed,dt,rlat,rlon)
            #(rlat,rlon) = gc_ltlg(rlat,rlon,deltaR,course)
        
    return (lats, lons)

def getLatLonArrays2(clat,clon,deltaR,R1,R2):
    
    
    lats = []
    lons = []  
    
    initTheta = 0.0
    
    for inc_i in range(int(floor((R2-R1)/deltaR))):
    
        R = 0.5*deltaR + R1 + deltaR*inc_i
    
        deltatheta = 2.0*asin(deltaR/(2.0*R))*rad2deg 

        initTheta += 0.5 * deltatheta * inc_i
    
        (rlat,rlon) = gc_ltlg(clat,clon,R,initTheta)
    
        for inc_j in range(int(floor(360.0/deltatheta))):
            lats.append(rlat)
            lons.append(rlon)
            course = initTheta + deltatheta*(inc_j+1)

            (rlat,rlon) = gc_ltlg(clat,clon,R,course)
        
    return (lats, lons)

def getLatLonArrays3(clat,clon,deltaR,R1,R2,initTheta):
    
    
    lats = []
    lons = []
    
    #for inc_i in range(int(floor((R2-R1)/deltaR))):
    
    R = 0.5*deltaR + R1
    inc_i = 0
    
    while (R < R2):   
        
        n = int(floor(2.0*pi*R/deltaR))
        
        deltatheta = 360.0/(n)
    
        #deltatheta = 2.0*asin(deltaR/(2.0*R))*rad2deg 

        initTheta += 0.5 * deltatheta * ( inc_i + 1 )
        
        if ( initTheta > 360 ): initTheta = initTheta%360.0
    
        for inc_j in range(n):
            course = initTheta + deltatheta*(inc_j)            
            (rlat,rlon) = gc_ltlg(clat,clon,R,course)
            lats.append(rlat)
            lons.append(rlon)
            
        R += deltaR
        inc_i += 1
                    
    return (lats, lons)