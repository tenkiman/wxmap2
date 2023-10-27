from math import *
from const import *

def gc_ltlg ( clat, clon, radius, bearing ):
    
    #
    # Calculate the lat and lon of a destination
    # using a given distance and bearing from start point
    #
    
    radius = radius * nm2km
    bearing = bearing * deg2rad
    
    clat = clat * deg2rad
    clon = clon * deg2rad
    
    rlat0 = asin( sin( clat ) * cos( radius / rearth ) + cos( clat ) * sin( radius / rearth ) * cos( bearing ) ) 
    rlon0 = clon + atan2( sin( bearing ) * sin( radius / rearth ) * cos( clat ), cos( radius / rearth ) - sin( clat ) * sin( rlat0 ) )
    
    rlat0 = rlat0 * rad2deg
    rlon0 = rlon0 * rad2deg
    
    return( rlat0, rlon0 )


def getLatLonArrays( clat, clon, deltaR, Rmin, Rmax, initTheta ):
    
    
    lats = []
    lons = []
    
    #for inc_i in range(int(floor((R2-R1)/deltaR))):
    
    R = 0.5 * deltaR + Rmin
    inc_i = 0
    
    while ( R < Rmax ):   
        
        n = int( floor( 2.0 * pi * R / deltaR ) )
        
        deltatheta = 360.0 / ( n )
    
        #deltatheta = 2.0*asin(deltaR/(2.0*R))*rad2deg 

        initTheta += 0.5 * deltatheta * ( inc_i + 1 )
        
        if ( initTheta > 360 ): initTheta = initTheta % 360.0
    
        for inc_j in range( n ):
            course = initTheta + deltatheta * ( inc_j )            
            ( rlat, rlon ) = gc_ltlg( clat, clon, R, course )
            lats.append( rlat )
            lons.append( rlon )
            
        R += deltaR
        inc_i += 1
                    
    return ( lats, lons )

def getLatLonScheme( clat, clon, scheme, initTheta ):
    
    schemeRadii = {
                   "weak":( 90, None ),
                   "small":( 45, 90 ),
                   "medium":( 60, 120, 180 ),
                   "large":( 75, 150, 225 )
                  }

    schemeDelta = {
                   "weak": 45.0,
                   "small": 45.0,
                   "medium": 60.0,
                   "large": 75.0  
                  }


    schemeBearing = {
                     1:( 0, 120, -120 ),
                     2:( 60, 180, -60 ),
                     3:( 0, 120, -120 )
                     }
    
    
    lats = []
    lons = []
    
    if ( scheme == None ): scheme = "medium"
    
    deltaR = schemeDelta[scheme]

    ring = 1

    
    for radius in schemeRadii[scheme]:
        if ( radius != None ):
            for bearing in schemeBearing[ring]:
                course = initTheta + bearing

                if ( course > 360.0 ): course = course % 360.0
                 
                ( rlat, rlon ) = gc_ltlg( clat, clon, radius, course )
                lats.append( rlat )
                lons.append( rlon )

            ring += 1
                    
    return ( lats, lons, deltaR )
