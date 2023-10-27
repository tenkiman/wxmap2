import rlcompleter
import readline
readline.parse_and_bind( "tab: complete" )

import os
import sys 

import struct
import array
import time

from math import sqrt, pow, fabs

import mf
from TC import gc_dist
from TCobs import *
from const import *

from M import MFutils

from getvrvt import *

import numpy

class MtcswaObs:
    
    Undef = -999.999
    
    Vars = ['u', 'v', 'w', 'uso', 'vso', 'wso']
    
    VarDesc = {
             'u':'u comp wind',
             'v':'v comp wind',
             'w':'Wind Speed',
             'uso':'u comp superob',
             'vso':'v comp superob',
             'wso':'wind speed superob'
            }
    VarUnits = {
              'u':'[m/s]',
              'v':'[m/s]',
              'w':'[m/s]',
              'uso':'[m/s]',
              'vso':'[m/s]',
              'wso':'[m/s]'
             }
    
    DataTypes = ['IRWD']
    
    Inc = 1

    Rmin = 22.5

    Rmax = 262.5
    
    #deltaR = 60.0
    #deltaR2 = 45.0
    
    #deltaR = [45.0, 60.0, 75.0]
    
    #initTheta = 0.0
    #initTheta2 = 0.0

    MaxOB = 30.0
    
    MaxOBAn = 65.0
    
    Hours = 3.0
    
    def __init__( self, dtg, storm, inputpath, outputdir, cLat, cLon, dir, r34, vmx ):
        #__inputPath  = '%s%s/%s/%s%s.obs'%(self.Inputdir,dtg[0:4],storm,file,dtg)
        __inputPath = inputpath
        self.Basedir = outputdir
        self.Storm = storm
        self.DTG = dtg
        self.centerLat = cLat
        self.centerLon = cLon
        self.initTheta = float(dir)
        self.r34 = r34
        self.vmx = vmx
        self.outputPath = {}
        self.ctlPath = {}
        self.smpPath = {}
        self.pressureLevels = []
        
        try:
            self.oInputPath = open( __inputPath )
            openfile = True
        except:
            raise IOError( 'Unable to open: %s'( __inputPath ) )
            openfile = False
            
        self.openFile = openfile
        
        if( self.openFile ):
            for dt in self.DataTypes:
                __outputPath = '%s/tcobs.cira.%s.%s.%s.obs' % ( self.Basedir, dtg, storm, dt )
                __ctlPath = '%s/tcobs.cira.%s.%s.%s.ctl' % ( self.Basedir, dtg, storm, dt )
                __smpPath = '%s/tcobs.cira.%s.%s.%s.smp' % ( self.Basedir, dtg, storm, dt )
                
                
                try:
                    self.outputPath[dt] = open( __outputPath, 'wb' )
                except:
                    raise IOError( 'Unable to open: %s'( __outputPath ) )
                
                self.CtlFile( __ctlPath, __smpPath, __outputPath, dtg, dt )
        
        

    def CtlFile( self, ctlPath, smpPath, outPath, dtg, datatype ):
        try:
            oCtlPath = open( ctlPath, 'w' )
        except:
            raise IOError( 'Unable to open: %s'( ctlPath ) )
        
        ( dir, outFile ) = os.path.split( outPath )
        ( dir, sFile ) = os.path.split( smpPath )

        gtime = mf.dtg2gtime( dtg )
        
        vars = []
        
        for v in self.Vars:
            desc = '%s %s' % ( self.VarDesc[v], self.VarUnits[v] )
            vars.append( '%-7s 1 0 %s' % ( v, desc ) )
                
        ctl = """dset    ^%s
title   Sat Winds
dtype   station
stnmap  ^%s
undef   %07.3f
tdef    1 linear %s %dhr
vars    %d
""" % ( outFile, sFile, self.Undef, gtime, self.Hours, len( vars ) )

        for v in vars:
            ctl = ctl + "%s\n" % ( v )
        ctl = ctl + 'endvars\n'
        
        oCtlPath.writelines( ctl )
        
    def ReadCards( self ):
        cards = self.oInputPath.readlines()
        return( cards )
    
    def ParseCards( self, ncard ):
        
        iSplit = [16, 24, 44, 52, 61, 73, 82, 87, 105, 0, 34]
        eSplit = [23, 32, 50, 59, 68, 77, 86, 95, 113, 12, 42]
        
        data = []
        
        for i in range( len( iSplit ) ):
            dsplit = ncard[iSplit[i]:eSplit[i]].split()
            data = data + dsplit
        
               
        mfutils = MFutils()
        
        timei2 = mfutils.Dtg2Timei( self.DTG )
        timei1 = mfutils.Dtg2Timei( data[9][0:10] )
            
        deltaTime = mfutils.DeltaTimei( timei1, timei2 )
        
        try:
            meta = ( float( data[0] ), float( data[1] ), float( data[3] ), float( data[4] ), float( data[2] ), float( data[5] ), data[6], float( data[7] ), float( data[8] ), data[9], float( deltaTime ), float( data[10] ) )
        except:
            meta = None
        ostnid = 'sn%06d' % ( self.Inc )
        
        self.Inc += 1
        
        return( ostnid, meta )

    def LoadDataAnnulus( self ):

        ( cards ) = self.ReadCards()

        umeta = {}
        ometa = {}

        for ncard in cards:
            ( ostnid, meta ) = self.ParseCards( ncard )

            if( meta != None):
                lat = meta[0]
                lon = meta[1]
            
                pressure = meta[5]
                deltaTime = meta[10]
            
            
            
                for type in self.DataTypes:
                    #if (type == meta[6]):
                    if ( 'IRWD' == meta[6] ):
                        try:
                            self.pressureLevels.index( pressure )
                        except:
                            self.pressureLevels.append( pressure )

                        ( radius ) = gc_dist( self.centerLat, self.centerLon, lat, lon )
                        if ( radius >= self.Rmin and radius <= self.Rmax and fabs( deltaTime ) <= self.Hours ):
                            try:
                                umeta[ostnid].append( meta )
                            except:
                                umeta[ostnid] = []
                                umeta[ostnid].append( meta )
                        try:
                            ometa[ostnid].append( meta )
                        except:
                            ometa[ostnid] = []
                            ometa[ostnid].append( meta )
        
        return( umeta, ometa )
    
#
# Quality Control
#
    
    def QualityControl( self, umeta ):
                 
        qcmeta = {}
        winds = []
        
        stnid = umeta.keys()
        stnid.sort()
        
        for stn in stnid:
            if ( umeta[stn][0][4] < 150.0 * knots2ms ):
                winds.append( umeta[stn][0][4] )
                try:
                    qcmeta[stn].append( umeta[stn][0] )
                except:
                    qcmeta[stn] = []
                    qcmeta[stn].append( umeta[stn][0] ) 
            else:
                None

            #for type in self.DataTypes:
            #    if ( type == qcmeta[stn][0][6] and ( fabs( qcmeta[stn][0][4] - numpy.mean( winds ) ) > self.MaxOBAn * knots2ms ) ):
            #        print 'Wild Annulus Ob (ob/mean)', qcmeta[stn][0][4] - numpy.mean( winds ), qcmeta[stn][0][6], qcmeta[stn][0][5], qcmeta[stn][0][0], qcmeta[stn][0][1], qcmeta[stn][0][9]
        
        return qcmeta
        
                            
    def SuperObsAveraging( self, qcmeta ):
        
        someta = {}
        sostats = {}
        
        #( lats_0, lons_0 ) = getLatLonArrays( self.centerLat, self.centerLon, self.deltaR, self.Rmin, self.Rmax, self.initTheta )
        #( lats_1, lons_1 ) = getLatLonArrays( self.centerLat, self.centerLon, self.deltaR2, self.Rmin, self.Rmax, self.initTheta2 )
       
        scheme = None

        if ( self.vmx < 35 ): scheme = "weak"
        elif ( self.r34 < 60  ): scheme = "small"
        else: scheme = "medium"

        ( lats, lons, deltaR ) = getLatLonScheme ( self.centerLat, self.centerLon, scheme, self.initTheta )
        
        winds = {}
        ucomp = {}
        vcomp = {}
        temps = {}
        hgt = {}
        deltaT = {}
        
        stns = qcmeta.keys()
        stns.sort()
        for stn in stns:
            basemeta = qcmeta[stn][0]
            
            dlat = basemeta[0]
            dlon = basemeta[1]
            uwind = basemeta[2]
            vwind = basemeta[3]
            wdspd = basemeta[4]
            prslev = basemeta[5] 
            type = basemeta[6]
            temp = basemeta[7]
            height = basemeta[8]
            dtg = basemeta[9]
            dtime = basemeta[10]
            
            for inc in range( len( lats ) ):
                lat = lats[inc]
                lon = lons[inc]                    
                    
                radius = gc_dist( lat, lon, dlat, dlon )
                if ( radius <= ( deltaR * 0.5 ) ):
                    try:
                        winds[type, dtg, prslev, dtime][lat, lon].append( wdspd )
                        ucomp[type, dtg, prslev, dtime][lat, lon].append( uwind )
                        vcomp[type, dtg, prslev, dtime][lat, lon].append( vwind )
                        temps[type, dtg, prslev, dtime][lat, lon].append( temp )
                        hgt[type, dtg, prslev, dtime][lat, lon].append( height )
                        deltaT[type, dtg, prslev, dtime][lat, lon].append( dtime )
                    except:
                        try:
                            winds[type, dtg, prslev, dtime][lat, lon] = []
                            winds[type, dtg, prslev, dtime][lat, lon].append( wdspd )
                            ucomp[type, dtg, prslev, dtime][lat, lon] = []
                            ucomp[type, dtg, prslev, dtime][lat, lon].append( uwind )
                            vcomp[type, dtg, prslev, dtime][lat, lon] = []
                            vcomp[type, dtg, prslev, dtime][lat, lon].append( vwind )
                            temps[type, dtg, prslev, dtime][lat, lon] = []
                            temps[type, dtg, prslev, dtime][lat, lon].append( temp )
                            hgt[type, dtg, prslev, dtime][lat, lon] = []
                            hgt[type, dtg, prslev, dtime][lat, lon].append( height )
                            deltaT[type, dtg, prslev, dtime][lat, lon] = []
                            deltaT[type, dtg, prslev, dtime][lat, lon].append( dtime )
                        except:
                            winds[type, dtg, prslev, dtime] = {}
                            winds[type, dtg, prslev, dtime][lat, lon] = []
                            winds[type, dtg, prslev, dtime][lat, lon].append( wdspd )
                            ucomp[type, dtg, prslev, dtime] = {}
                            ucomp[type, dtg, prslev, dtime][lat, lon] = []
                            ucomp[type, dtg, prslev, dtime][lat, lon].append( uwind )
                            vcomp[type, dtg, prslev, dtime] = {}
                            vcomp[type, dtg, prslev, dtime][lat, lon] = []
                            vcomp[type, dtg, prslev, dtime][lat, lon].append( vwind )
                            temps[type, dtg, prslev, dtime] = {}
                            temps[type, dtg, prslev, dtime][lat, lon] = []
                            temps[type, dtg, prslev, dtime][lat, lon].append( temp )
                            hgt[type, dtg, prslev, dtime] = {}
                            hgt[type, dtg, prslev, dtime][lat, lon] = []
                            hgt[type, dtg, prslev, dtime][lat, lon].append( height )
                            deltaT[type, dtg, prslev, dtime] = {}
                            deltaT[type, dtg, prslev, dtime][lat, lon] = []
                            deltaT[type, dtg, prslev, dtime][lat, lon].append( dtime )
                else:
                    None
        
        typdtglev = winds.keys()
        typdtglev.sort()
        
        inc = 0
        
        for typedtgelev in typdtglev:
            ltln = winds[typedtgelev].keys()      
            ltln.sort()
            self.CreateFilesAndHeaders( typedtgelev )
            for latlon in ltln:
                avewind = numpy.mean( winds[typedtgelev][latlon] )
                aveu = numpy.mean( ucomp[typedtgelev][latlon] )
                avev = numpy.mean( vcomp[typedtgelev][latlon] )
                avet = numpy.mean( temps[typedtgelev][latlon] )
                avez = numpy.mean( hgt[typedtgelev][latlon] )
                
                for inc_i in range( len( winds[typedtgelev][latlon] ) ):
                    if ( fabs( winds[typedtgelev][latlon][inc_i] - avewind ) > ( self.MaxOB * knots2ms ) ):
                        print 'Wild Ob:', latlon[0], latlon[1], typedtgelev, 'Wind(ob/mean)', winds[typedtgelev][latlon][inc_i], avewind
                
                meta = ( latlon[0], latlon[1], typedtgelev[2], aveu, avev, avewind, avet, avez, typedtgelev[0], typedtgelev[1], deltaT[typedtgelev][latlon][0] )
                stats = ( typedtgelev, latlon[0], latlon[1],
                         len( ucomp[typedtgelev][latlon] ), aveu, numpy.std( ucomp[typedtgelev][latlon] ),
                         len( vcomp[typedtgelev][latlon] ), avev, numpy.std( vcomp[typedtgelev][latlon] ) )
                
                stnid = "sob%05d" % inc
                inc += 1
                
                try:
                    someta[stnid].append( meta )
                    sostats[stnid].append( stats )
                except:
                    try:
                        someta[stnid] = []
                        someta[stnid].append( meta )
                        sostats[stnid] = []
                        sostats[stnid].append( stats )
                    except:
                        someta[stnid] = {}
                        someta[stnid] = []
                        someta[stnid].append( meta )
                        sostats[stnid] = {}
                        sostats[stnid] = []
                        sostats[stnid].append( stats )
        
        return ( someta, sostats )
   
#
# Before super obs output
#
    
    def WriteOutput( self, basemeta, stn ):
        
        stnid = stn
        stndt = 0.0
        
        lat = basemeta[0]
        lon = basemeta[1]
        uwd = basemeta[2]
        vwd = basemeta[3]
        wsp = basemeta[4]
        psr = basemeta[5]
        typ = basemeta[6]
        tmp = basemeta[7]
        hgt = basemeta[8]
        dtime = basemeta[10]
        
        if( lon < 0.0 ):
            rlon = 360.0 + lon
        else:
            rlon = lon

        rlat = lat
        
        if ( dtime < 0 ): relTime = 1 - ( dtime / self.Hours ) * .5
        elif ( dtime > 0 ): relTime = 1 + ( dtime / self.Hours ) * .5
        else: relTime = 1
            
        stnhead = struct.pack( '8sfffii', stnid, rlat, rlon, relTime, 1, 0 )
        
        NA = 0
            
        if ( typ == self.DataTypes[0] ):
            stnrec = struct.pack( '%df' % 6, psr, uwd, vwd, wsp, tmp, hgt )
        elif ( typ == self.DataTypes[1] ):
            stnrec = struct.pack( '%df' % 4, psr, uwd, vwd, wsp )
        else:
            NA = 1
        
        if( NA != 1 ):
            self.outputPath[typ].write( stnhead )
            self.outputPath[typ].write( stnrec )
    
    def FinalizeOutput( self ):
        stnid = 'alldone '
        stnrec = struct.pack( '8sfffii', stnid, 0.0, 0.0, 0.0, 0, 0 )
        for dt in self.DataTypes:
            self.outputPath[dt].write( stnrec )
            self.outputPath[dt].close()
            
        try:
            self.oInputPath.close()
        except:
            None
            
    def GenOutput( self, qcmeta ):
        
        stns = qcmeta.keys()
        stns.sort()

        for stn in stns:
            basemeta = qcmeta[stn][0]
            self.WriteOutput( basemeta, stn )

                
        self.FinalizeOutput()
        
#
# Super Obs Output
#
        
    def WriteSuperOutput( self, basemeta, stn ):
        
        stnid = stn
        stndt = 0.0
        
        lat = basemeta[0]
        lon = basemeta[1]
        psr = basemeta[2]
        uwd = basemeta[3]
        vwd = basemeta[4]
        wsp = basemeta[5]
        tmp = basemeta[6]
        hgt = basemeta[7]
        typ = basemeta[8]
        dtime = basemeta[10]
        
        if( lon < 0.0 ):
            rlon = 360.0 + lon
        else:
            rlon = lon

        rlat = lat  
        
        if ( dtime < 0 ): relTime = 1 - ( dtime / self.Hours ) * .5
        elif ( dtime > 0 ): relTime = 1 + ( dtime / self.Hours ) * .5
        else: relTime = 1
            
        stnhead = struct.pack( '8sfffii', stnid, rlat, rlon, relTime, 1, 0 )
        #stnrec =  struct.pack('%df'%6,psr,uwd,vwd,wsp,tmp,hgt)
        
        NA = 0
            
        #if ( typ == self.DataTypes[0] ):
        #    stnrec = struct.pack( '%df' % 6, psr, uwd, vwd, wsp, tmp, hgt )
        #elif ( typ == self.DataTypes[1] or typ == self.DataTypes[2] ):
        #elif ( typ == self.DataTypes[1] ):
        stnrec = struct.pack( '%df' % 4, psr, uwd, vwd, wsp )
        #elif ( typ == self.DataTypes[3] ):
        #    stnhead = struct.pack('8sfffii',stnid,rlat,rlon,stndt,1,1)
        #    stnrec = struct.pack('%df'%3,uwd,vwd,wsp)
        #else:
        #    NA = 1
        
        if ( NA != 1 ):
            self.outputPath[typ].write( stnhead )
            self.outputPath[typ].write( stnrec )

            
    def GenSuperOutput( self, someta ):
        stns = someta.keys()
        stns.sort()
        
        for stn in stns:
            basemeta = someta[stn][0]
            self.WriteSuperOutput( basemeta, stn )
            
        self.FinalizeOutput()
        
#
# Output Everything
#

    def WriteAllOutput( self, basemeta, stn, boolean ):
        
        stnid = stn
        
        lat = basemeta[0]
        lon = basemeta[1]
        dtime = basemeta[10]
        
        if ( boolean == True ):
            uwd = self.Undef
            vwd = self.Undef
            wsp = self.Undef
            uso = basemeta[3]
            vso = basemeta[4]
            wso = basemeta[5]
            psr = basemeta[2]
            typ = basemeta[8]
            #( vr, vt, uvr, vvr, uvt, vvt ) = getvrvt( self.centerLat, self.centerLon, lat, lon, uso, vso )
            
        else:
            uwd = basemeta[2]
            vwd = basemeta[3]
            wsp = basemeta[4]
            psr = basemeta[5]
            typ = basemeta[6]
            uso = self.Undef
            vso = self.Undef
            wso = self.Undef
            #vr = vt = uvr = vvr = uvt = vvt = self.Undef
            
        
        if( lon < 0.0 ):
            rlon = 360.0 + lon
        else:
            rlon = lon

        rlat = lat  
               
        if ( dtime < 0 ): relTime = 1 - ( dtime / self.Hours ) * .5
        elif ( dtime > 0 ): relTime = 1 + ( dtime / self.Hours ) * .5
        else: relTime = 1
            
        stnhead = struct.pack( '8sfffii', stnid, rlat, rlon, relTime, 1, 0 )
        
        #NA = 0
            
        stnrec = struct.pack( '%df' % 7, psr, uwd, vwd, wsp, uso, vso, wso )
        
        #else:
        #    NA = 1
        
        self.outputPath[typ].write( stnhead )
        self.outputPath[typ].write( stnrec )
        
    def GenAllOutput( self, qcmeta, someta ):
        
        stns = qcmeta.keys()
        stns.sort()
        
        
        for stn in stns:
            baseqc = qcmeta[stn][0]
            self.WriteAllOutput( baseqc, stn, False )
            
        stns = someta.keys()
        stns.sort()
            
        for stn in stns:
            baseso = someta[stn][0]
            
            self.WriteAllOutput( baseso, stn, True )
            
        self.FinalizeOutput()
        
#
# Write Super Obs txt files
#

    def CreateFilesAndHeaders( self, typedtgelev ):
       
        for dt in self.DataTypes:
            if ( typedtgelev[0] == dt ):
                try:
                    #self.soOpen[typedtgelev] = "%s/tcobs.cira.%s.v%s.%s.%s.p%04d.txt" % ( self.Basedir, self.DTG, typedtgelev[1][6:12], self.Storm, typedtgelev[0].lower(), typedtgelev[2] )
                    self.soOpen[typedtgelev] = "%s/tcobs.cira.%s.%s.%s.Vmax%03d.%s.p%04d.txt"% ( self.Basedir, self.Storm, self.DTG[0:4], self.DTG, int(self.vmx), typedtgelev[0].lower(), typedtgelev[2] )
                except:
                    try:
                        self.soOpen[typedtgelev] = []
                        #self.soOpen[typedtgelev] = "%s/tcobs.cira.%s.v%s.%s.%s.p%04d.txt" % ( self.Basedir, self.DTG, typedtgelev[1][6:12], self.Storm, typedtgelev[0].lower(), typedtgelev[2] )
                        self.soOpen[typedtgelev] = "%s/tcobs.cira.%s.%s.%s.Vmax%03d.%s.p%04d.txt"% ( self.Basedir, self.Storm, self.DTG[0:4], self.DTG, int(self.vmx), typedtgelev[0].lower(), typedtgelev[2] )
                    except:
                        self.soOpen = {}
                        self.soOpen[typedtgelev] = []
                        #self.soOpen[typedtgelev] = "%s/tcobs.cira.%s.v%s.%s.%s.p%04d.txt" % ( self.Basedir, self.DTG, typedtgelev[1][6:12], self.Storm, typedtgelev[0].lower(), typedtgelev[2] )
                        self.soOpen[typedtgelev] = "%s/tcobs.cira.%s.%s.%s.Vmax%03d.%s.p%04d.txt"% ( self.Basedir, self.Storm, self.DTG[0:4], self.DTG, int(self.vmx), typedtgelev[0].lower(), typedtgelev[2] )

                soFile = open( self.soOpen[typedtgelev], 'w' )
                soFile.writelines( "Platform:%s DateTimeGroup:%s DeltaTime(hours):%s  PressureLev:%04d\n" % ( typedtgelev[0], self.DTG, typedtgelev[3], typedtgelev[2] ) )
    
    def WriteSuperObs( self, basestat ):
        typedtgelev = basestat[0]
        for dt in self.DataTypes:
            if ( typedtgelev[0] == dt ):
                record = "Lat: %6.2f Lon: %7.2f numobs: %3d u(m/s): mean: %5.1f std: %5.1f v(m/s): mean: %5.1f std: %5.1f  \n" % ( basestat[1], basestat[2], basestat[3], basestat[4], basestat[5], basestat[7], basestat[8] )
                soFile = open( self.soOpen[typedtgelev], 'a' )
                soFile.writelines( record )

    def GenSuperObs( self, sostats ):
        
        stnid = sostats.keys()
        stnid.sort()
        
        for stn in stnid:
            basestat = sostats[stn][0]
            self.WriteSuperObs( basestat )
            
    
            
    def RunProgram( self ):
        stime = time.time()
        ( umeta, ometa ) = self.LoadDataAnnulus()
        mf.Timer( 'Read Cards and loaded data. ', stime )
        
        stime = time.time()
        ( qcmeta ) = self.QualityControl( umeta )
        mf.Timer( 'Quality Control. ', stime )
    
        #stimer=time.time()    
        #self.GenOutput(qcmeta)
        #mf.Timer('Finished creating obs files. ', stime)
    
        stime = time.time()
        ( someta, sostats ) = self.SuperObsAveraging( qcmeta )
        mf.Timer( 'Done Averaging for super obs', stime )
    
        #self.GenSuperOutput( someta )
        #mf.Timer( 'Finished creating super obs grads files', stime )
    
        stime = time.time()    
        self.GenSuperObs( sostats )
        mf.Timer( 'Finished writing super obs files.', stime )
        
        stime = time.time()
        self.GenAllOutput( ometa, someta )
        mf.Timer( 'Finished writing all grads obs', stime )

                
        return ( self.pressureLevels )
    
if( __name__ == '__main__' ):

    satwinds = MtcswaObs( '2009082906', '13e', '/dat4/w21/dat/tc/cira/mtcswa/2010/03a/2010IO03_MPSATWD_2010060218.obs', '/dat4/w21/prc/tcobs', 18, 60.5 )
    
    satwinds.RunProgram()
    
    print 'The program has finished!'
