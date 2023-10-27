#!/usr/bin/env python

#
# intersections.py
#
# Python for finding line intersections
#   intended to be easily adaptable for line-segment intersections
#
import sys

    
def getTrackArea(pt1,pt2,pt3,pt4,verb=0):

    import math
    from area import area


    # -- local vars
    #
    # convert area units, also has error trapping
    # tested with Python24     vegaseat      01aug2005
    #create an empty dictionary
    areaD = {}
    # populate dictionary using indexing and assignment with units and conversion factors relative to sqmeter = 1.0
    # to convert x sqmeters to any of the other area units multiply by the factor
    # to convert x of any of the other area units to sqmeter divide by the factor
    # to convert x of any area unit to any of the other area units go over interim sqmeter
    # this minimizes the total number of conversion factors
    areaD['sqmeter']      = 1.0
    areaD['sqmillimeter'] = 1000000.0
    areaD['sqcentimeter'] = 10000.0
    areaD['sqkilometer']  = 0.000001
    areaD['hectare']      = 0.0001
    areaD['sqinch']       = 1550.003
    areaD['sqfoot']       = 10.76391
    areaD['sqyard']       = 1.19599
    areaD['acre']         = 0.0002471054
    areaD['sqmile']       = 0.0000003861022
    areaD['sqnm']         = areaD['sqmile']*0.868976
    
    # -- local defs
    #
    def convertArea(x, unit1, unit2):
        
        if (unit1 in areaD) and (unit2 in areaD):
            factor1 = areaD[unit1]
            factor2 = areaD[unit2]
            return factor2*x/factor1
        else:
            return False

    def intersectLines( pt1, pt2, ptA, ptB ): 
        """ this returns the intersection of Line(pt1,pt2) and Line(ptA,ptB)
            
            returns a tuple: (xi, yi, valid, r, s), where
            (xi, yi) is the intersection
            r is the scalar multiple such that (xi,yi) = pt1 + r*(pt2-pt1)
            s is the scalar multiple such that (xi,yi) = pt1 + s*(ptB-ptA)
                valid == 0 if there are 0 or inf. intersections (invalid)
                valid == 1 if it has a unique intersection ON the segment    """
    
        DET_TOLERANCE = 0.00000001
    
        # the first line is pt1 + r*(pt2-pt1)
        # in component form:
        x1, y1 = pt1;   x2, y2 = pt2
        dx1 = x2 - x1;  dy1 = y2 - y1
    
        # the second line is ptA + s*(ptB-ptA)
        x, y = ptA;   xB, yB = ptB;
        dx = xB - x;  dy = yB - y;
    
        # we need to find the (typically unique) values of r and s
        # that will satisfy
        #
        # (x1, y1) + r(dx1, dy1) = (x, y) + s(dx, dy)
        #
        # which is the same as
        #
        #    [ dx1  -dx ][ r ] = [ x-x1 ]
        #    [ dy1  -dy ][ s ] = [ y-y1 ]
        #
        # whose solution is
        #
        #    [ r ] = _1_  [  -dy   dx ] [ x-x1 ]
        #    [ s ] = DET  [ -dy1  dx1 ] [ y-y1 ]
        #
        # where DET = (-dx1 * dy + dy1 * dx)
        #
        # if DET is too small, they're parallel
        #
        DET = (-dx1 * dy + dy1 * dx)
    
        if math.fabs(DET) < DET_TOLERANCE: return (0,0,0,0,0)
    
        # now, the determinant should be OK
        DETinv = 1.0/DET
    
        # find the scalar amount along the "self" segment
        r = DETinv * (-dy  * (x-x1) +  dx * (y-y1))
    
        # find the scalar amount along the input line
        s = DETinv * (-dy1 * (x-x1) + dx1 * (y-y1))
    
        # return the average of the two descriptions
        xi = (x1 + r*dx1 + x + s*dx)/2.0
        yi = (y1 + r*dy1 + y + s*dy)/2.0
        return ( xi, yi, 1, r, s )
    
    
    def getIntersection(pt1,pt2,ptA,ptB,verb=1):
        """ prints out a test for checking by hand... """
        
        rc = intersectLines( pt1, pt2, ptA, ptB )
        if(verb):
            print "Line segment #1 runs from", pt1, "to", pt2
            print "Line segment #2 runs from", ptA, "to", ptB
            print 'RC: ',rc
    
        return(rc)



    # -- case of start/end points identical
    #
    if( (pt1[0] == pt3[0]) and (pt1[1] == pt3[1]) ): pt3[0]=pt3[0]+0.01
    if( (pt2[0] == pt4[0]) and (pt2[1] == pt4[1]) ): pt4[0]=pt4[0]+0.01

    # -- get intersection
    #
    rc=getIntersection(pt1,pt2,pt3,pt4,verb=verb)
    isIntersection=rc[2]
    
    pti=[rc[0],rc[1]]
    
    if(verb): print 'pti: ',pti
    
    if(isIntersection == 0):
        
        tpoly={
            'type': 'Polygon',
            'coordinates': [
            [
            [pt1[1],pt1[0]],
            [pt2[1],pt2[0]],
            [pt4[1],pt4[0]],
            [pt3[1],pt3[0]],
            [pt1[1],pt1[0]]
            ]
            ]
            }
        
    else:
        
        tpoly={
            'type': 'Polygon',
            'coordinates': [
            [
            pt1,
            [pt1[1],pt1[0]],
            [pti[1],pti[0]],
            [pt4[1],pt4[0]],
            [pt2[1],pt2[0]],
            [pti[1],pti[0]],
            [pt3[1],pt3[0]],
            [pt1[1],pt1[0]]
            
            ]
            ]
            }
        


    if(verb): print tpoly

    tarea2=area(tpoly)
    tarea2=convertArea(tarea2,'sqmeter','sqnm')
    tarea=math.sqrt(tarea2)
    #tarea=tarea2
    return(tarea)



if __name__ == "__main__":


    # -- no intersection - start point the same
    pt1 = [10.0,130.0] ; pt2 = [15.0,130.0]
    pt3 = [10.0,130.0] ; pt4 = [15.0,135.0]

    # -- no intersection
    pt1 = [10.0,130.0] ; pt2 = [15.0,130.0]
    pt3 = [10.0,135.0] ; pt4 = [15.0,135.0]

    # -- intersection...
    pt1 = [10.0,130.0] ; pt2 = [19.0,140.0]
    pt3 = [10.0,140.0] ; pt4 = [20.0,130.0]
    
    pt1=[8.6, 147.8] ; pt2=[9.8, 143.5]
    pt3=[8.7, 146.5] ; pt4=[10.6, 141.8]

    # -- no intersection
    #pt1 = [-5.0,130.0] ; pt2 = [5.0,130.0]
    #pt3 = [-5.0,145.0] ; pt4 = [5.0,140.0]

    #pt1 = [40.0,130.0] ; pt2 = [50.0,130.0]
    #pt3 = [40.0,135.0] ; pt4 = [50.0,135.0]

    
    tarea=getTrackArea(pt1,pt2,pt3,pt4,ve)

    print 'tarea: ',tarea

  

