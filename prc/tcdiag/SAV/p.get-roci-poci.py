#!/usr/bin/env python

from osgeo import ogr

ds = ogr.Open('m2.kml')

print ds
nl=0
for lyr in ds:
    nl=nl+1
    print 'LLLLLLLLLLLLLLL ',nl
    for feat in lyr:
        clev=feat.name
        geom = feat.GetGeometryRef()
        if geom != None:
            np=geom.GetPointCount()
            pb=geom.GetPoint(0)[0:2]
            pe=geom.GetPoint(np-1)[0:2]
            print 'CCCContour level: ',clev,'pb: ',pb,' pe: ',pe

            if(pb[0] == pe[0] and pb[1] == pe[1]):
                print 'CCCCCCCCCCCCCCClosed: ',clev
            else:
                print 'OOOOOOOOOOOOOOOOOpen: ',clev

                
            #for i in range(0, np):
            #    print (geom.GetPoint(i))
