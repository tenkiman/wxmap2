#!/usr/bin/env python

from TC import *

from mtcswaNewScheme import *
from GA2 import *

import os

MF = MFutils()
        
#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# command line setup
#

class TcObsCmdLine( CmdLine ):

    def __init__( self, argv = sys.argv ):

        if( argv == None ): argv = sys.argv
        
        self.argv = argv
        self.argopts = {
            1:['dtgopt', 'run dtgs'],
            }

        self.defaults = {
            'doupdate':0,
            }

        self.options = {
            'override':['O', 0, 1, 'override'],
            'verb':['V', 0, 1, 'verb=1 is verbose'],
            'ropt':['N', '', 'norun', ' norun is norun'],
            'stmopt':['S:', None, 'a', 'stmopt'],
            }

        self.purpose = '''
purpose -- superob the CIRA MTCSWA (multi-platiform TC sfc wind analysis) AMSu and IRWD wind retrievals
for use in EnKF
'''
        self.examples = '''
example:
%s 20090900100 -S 13e.9 # process Jimena'''


class Mtcswa( MFbase ):

    sbdir = TcObsMtcswaSourceDir
    tbdir = TcObsSatWindsDir
    bufrdir = '/dat4/w21/prc/tcobs'

    def lsObs( self, dtg, stm3id, lat, lon, dir, r34, vmx ):

        #if ( stm3id == '04e' and int( dtg ) < 2010061918 ): stm3id = '94e'
        #if ( stm3id == '05e' and int( dtg ) < 2010062306 ): stm3id = '95e'

        if ( lon > 180.0 ):
            lon = lon - 360.0
        year = dtg[0:4]
        sdir = "%s/%s/%s" % ( self.sbdir, year, stm3id )
        obfiles = glob.glob( "%s/*%s*obs" % ( sdir, dtg ) )
        pressure = []
        openObFile = None
        for obfile in obfiles:
            print 'MTCSWA .obs file for dtg: ', dtg, ' is: ', obfile
            print dtg, stm3id, obfile, self.tbdir, lat, lon
            satwinds = MtcswaObs( dtg, stm3id, obfile, self.tbdir, lat, lon, dir, r34, vmx )
            openObFile = satwinds.openFile
            if ( not openObFile ): break
            pressure = satwinds.RunProgram()
        self.obfiles = obfiles
        try:
            satobs = SatWindsObs( self.bufrdir, self.bufrdir, dtg, lat, lon, dir, r34, vmx )
            subtype = satobs.RunProgram()
            drawBufr = True
        except:
            subtype = None
            drawBufr = False
            
        return ( subtype, drawBufr, pressure, openObFile )
        
        
    def draw( self, dtg, storm, lat, lon, subtype, drawBufr, pressure, vmax, mprs, dir, r34, spd ):

        if ( storm == '04e' and int( dtg ) < 2010061918 ): storm = '94e'
        if ( storm == '05e' and int( dtg ) < 2010062306 ): storm = '95e'


        ga = GaGrads( 
                     lat1 = ( lat - 7 ),
                     lat2 = ( lat + 7 ),
                     lon1 = ( lon - 7 ),
                     lon2 = ( lon + 7 ),
                     quiet = 1 
                     )
        
        file2 = 'grid.ctl' 
        os.system( 'stnmap2 -q -i %s' % ( file2 ) )              
        
        file1 = '%s/tcobs.cira.%s.%s.%s.ctl' % ( self.tbdir, dtg, storm, 'IRWD' )
        os.system( 'stnmap2 -q -i %s' % ( file1 ) )              
        fh = ga.open( file1 )        
        fh = ga.open( file2 )
        ga.setLatLon()
        ga.setMap()
        
        cmd = ""
        
        for lev in pressure:
           
            cmd += """
            set lev %d
            set gxout shaded 
            """ % lev
            
            cmd += "set gxout shaded\nset clevs 20 30 40 50 60 70 80 90 100 110 120 130\n"
            cmd += "d mag(oacres(u.2,u.1*1.94),oacres(v.2,v.1*1.94))\nrun cbarn\n"

            cmd += "set gxout barb\nset cthick 12\nset ccolor 0\n"
            cmd += " d uso.1(t-0.5,t+0.5)*1.94;vso.1(t-0.5,t+0.5)*1.94\nset cthick 4\n"
            

            #if ( lev == 850.0 ): cmd += "set ccolor 14\n"
            #else: cmd += "set ccolor 4\n"

            cmd += "set ccolor 1\n"

            cmd += "d uso.1(t-0.5,t+0.5)*1.94;vso.1(t-0.5,t+0.5)*1.94\n"

            #cmd += "set ccolor 2"

            #cmd += "d uso.1(t-0.5,t+0.5)*1.94;maskout(vso.1(t-0.5,t+0.5)*1.94,mag(uso.1(t-0.5,t+0.5)*1.94,vso.1(t-0.5,t+0.5)*1.94)-65.0))\n"
            

            drawBufr = False

            if ( drawBufr ):
   
                cmdSub = ""
                for inc_i in range( len( subtype ) ):
                
                    file = '/dat4/w21/prc/tcobs/obs.%s.%d.ctl' % ( dtg, subtype[inc_i] )
                    os.system( 'stnmap2 -i %s' % ( file ) )
                    fh = ga.open( file )
                    if ( lev == 850.0 ): cmdSub += "set ccolor 7\n"
                    else: cmdSub += "set ccolor 3\n"
                    cmdSub += "d uo.%d(lev+50,lev-50)*1.94;vo.%d(lev+50,lev-50)*1.94\n" % ( inc_i + 3, inc_i + 3 )
                
                cmd += cmdSub
        
        if ( lon > 180 ): clon = lon - 360
        else: clon = lon


        filename = "%s/tcobs.cira.%s.%s.Vmax%03d.%s.%s.p%04d.png"% ( TcObsSatWindsDir, storm, dtg[0:4], int(vmax), dtg, 'irwd', pressure[0] )

        cmd += """
    draw title  %s - IRWD - %s\Super Obs [kts] 
    draw string 0.5 5.6 clat: %4.1f
    draw string 0.5 5.3 clon: %5.1f
    draw string 0.5 5.0 vmax: %d kts
    draw string 0.5 4.7 pmin: %d mb
    draw string 0.5 4.4 dir:  %d degree
    draw string 0.5 4.1 r34:  %d nm
    draw string 0.5 3.8 spd:  %d kts
    draw string 0.5 3.2 plev: %d mb
    gxyat %s
    c

    """ % ( storm, dtg, lat, clon, vmax, mprs, dir, r34, spd, pressure[0], filename )
            
        ga._cmd( cmd )
                
        
        
#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# main 
argstr = "pyfile cur-18 "
argv = argstr.split()
argv = sys.argv
CL = TcObsCmdLine( argv = argv )
CL.CmdLine()
exec( CL.estr )
if( verb ): print CL.estr

dtgs = mf.dtg_dtgopt_prc( dtgopt )

mT = Mtcswa()

for dtg in dtgs:

    tcD = TcData()
    
    try:
        tv=tcD.getTcvitals(dtg)

        stmids=tv.keys()
        stmids.sort()
        for stmid in stmids:
           if ( stmopt != None ):
               if ( stmid.split( '.' )[0].lower() == stmopt.split( '.' )[0].lower() ):
                   lat = float( tv[stmid][0] )
                   lon = float( tv[stmid][1] )
                   dir = float( tv[stmid][2] )
                   spd = float( tv[stmid][3] )
                   vmx = float( tv[stmid][4] )
                   prs = float( tv[stmid][6] )
                   r34 = float( tv[stmid][8] )
                   stm3id = stmid.split( '.' )[0].lower()
                   ( subtype, drawBufr, pressure, openObFile ) = mT.lsObs( dtg, stm3id, lat, lon, dir, r34, vmx )
                   if ( openObFile ): mT.draw( dtg, stm3id, lat, lon, subtype, drawBufr, pressure, vmx, prs, dir, r34, spd )
               else:
                   None
           else:
               lat = float( tv[stmid][0] )
               lon = float( tv[stmid][1] )
               dir = float( tv[stmid][2] )
               vmx = float( tv[stmid][4] )
               spd = float( tv[stmid][5] )
               prs = float( tv[stmid][6] )
               r34 = float( tv[stmid][8] )
               stm3id = stmid.split( '.' )[0].lower()
               ( subtype, drawBufr, pressure, openObFile ) = mT.lsObs( dtg, stm3id, lat, lon, dir, r34, vmx )
               if ( openObFile ): mT.draw( dtg, stm3id, lat, lon, subtype, drawBufr, pressure, vmx, prs, dir, r34, spd )
    except:
        print
        print "************************************************"
        print "Error with getTcvitals for %s."%(dtg)
        print "************************************************"
        print


                

           

#    ( stmids, btcs ) = tcD.getDtg( dtg, dupchk = 1 )
#
#    for stmid in stmids:
#        if ( stmopt != None ):
#            if ( stmid.split( '.' )[0].lower() == stmopt.split( '.' )[0].lower() ):
#                lat = float( btcs[stmid][0] )
#                lon = float( btcs[stmid][1] )
#                vmax = float( btcs[stmid][2] )
#                mprs = float( btcs[stmid][3] )
#                stm3id = stmid.split( '.' )[0].lower()
#                ( subtype, drawBufr, pressure, openObFile ) = mT.lsObs( dtg, stm3id, lat, lon )
#                if ( openObFile ): mT.draw( dtg, stm3id, lat, lon, subtype, drawBufr, pressure, vmax, mprs )
#            else:
#               None
#        else:
#            lat = float( btcs[stmid][0] )
#            lon = float( btcs[stmid][1] )
#            stm3id = stmid.split( '.' )[0].lower()
#            ( subtype, drawBufr, pressure, openObFile ) = mT.lsObs( dtg, stm3id, lat, lon )
#            if ( openObFile ): mT.draw( dtg, stm3id, lat, lon, subtype, drawBufr, pressure )  
