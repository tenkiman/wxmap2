#!/usr/bin/env python

from tcbase import *
from mtcswaNewScheme import *
from GA import *


sbdir = TcObsMtcswaSourceDir
tbdir = "/mnt/lfs1/projects/fim/slocum/w21/prj/tc/tc_mtcswa_superobs_20110606/"

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
purpose -- superob the CIRA MTCSWA (multi-platiform TC sfc wind analysis) AMSU and IRWD wind retrievals
for use in EnKF
'''
        self.examples = '''
example:
%s 20090900100 -S 13e.9 # process Jimena'''


class Mtcswa( MFbase ):

    bufrdir = '/dat4/w21/prc/tcobs'
    #Dont Use    
    def diaFile ( self, diafile, dtg, stmid ):
        spd = -999.99
        #try:
        diaInputPath = open( diafile )
        cards = diaInputPath.readlines()

        lat = float( cards[0][13:18] )
        lon = float( cards[0][18:26] )
        vmx = float( cards[0][26:31] )
        dir = float( cards[0][37:41] )
        prs = float( cards[0][40:48] )
        r34ne = float( cards[1][0:5] )
        r34se = float( cards[1][5:9] )
        r34sw = float( cards[1][9:13] )
        r34nw = float( cards[1][13:17] )
            
        r34 = ( r34ne + r34se + r34sw + r34nw ) / 4.0
            
        print '****************************'
        print dtg, stmid
        print lat, lon, vmx, dir, prs, r34
            
        #( subtype, drawBufr, pressure, openObFile ) = self.lsObs( dtg, stmid, lat, lon, dir, r34, vmx )
        #if ( openObFile ): self.draw( dtg, stmid, lat, lon, subtype, drawBufr, pressure, vmx, prs, dir, r34, spd )
        #except:
        #    None
    def md2 ( self, dtg, stmid, trk ):
        print '***************************'
        print dtg, stmid
        print trk.rlat, trk.rlon, trk.dir, trk.r34m, trk.vmax, trk.pmin

        ( subtype, drawBufr, prsLev, openObFile ) = self.lsObs( dtg, stmid, trk.rlat, trk.rlon, trk.dir, trk.r34m, trk.vmax )
        #if ( openObFile ): self.draw( dtg, stmid, trk.rlat, trk.rlon, subtype, drawBufr, prsLev[0], trk.vmax, trk.pmin, trk.dir, trk.r34, trk.spd )
        if ( openObFile ): self.draw( dtg, stmid, trk, prsLev[0] )

    def lsObs( self, dtg, stm3id, lat, lon, dir, r34, vmx ):

        #if ( stm3id == '04e' and int( dtg ) < 2010061918 ): stm3id = '94e'
        #if ( stm3id == '05e' and int( dtg ) < 2010062306 ): stm3id = '95e'

        if ( lon > 180.0 ):
            lon = lon - 360.0
        year = dtg[0:4]
        sdir = "%s/%s/%s" % ( sbdir, year, stm3id )
        obfiles = glob.glob( "%s/*%s*obs" % ( sdir, dtg ) )
        pressure = []
        openObFile = None
        for obfile in obfiles:
            print 'MTCSWA .obs file for dtg: ', dtg, ' is: ', obfile
            print dtg, stm3id, obfile, tbdir, lat, lon
            satwinds = MtcswaObs( dtg, stm3id, obfile, tbdir, lat, lon, dir, r34, vmx )
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
        
    def draw( self, dtg, stmid, trk, prsLev ):

        if ( trk.r34m != None ): r34m = trk.r34m
        else: r34m = 999
        if ( trk.r50m != None ): r50m = trk.r50m
        else: r50m = 999
        

        ga = setGA2(Quiet=1,Window=0,verb=0)

        file_grid = 'grid.ctl'
        file_ctl = '%s/tcobs.cira.%s.%s.%s.ctl' % ( tbdir, dtg, stmid, 'IRWD' )
        file_png = "%s/tcobs.cira.%s.%s.%s.Vmax%03d.%s.p%04d.png" % ( tbdir, stmid, dtg[0:4], dtg, trk.vmax, 'irwd', prsLev )

        os.system( 'stnmap -q -i %s'%file_ctl)

        cmd = ""

        cmd += """
                open %s
                open %s

                set grads off
                set timelab off
                set xlint 10
                set ylint 5
                set rgb 20 255 255 255
                set rgb 21 255 220 220
                set rgb 22 255 165 165
                set rgb 23 255 110 110
                set rgb 24 255  55  55
                set rgb 25 255   0   0
                set rgb 26 165   0   0
                

                set lev %s

                set parea 0.5 5.25 0 8
                set mpdset hired
                set digsize 0.1
                set lat %f %f
                set lon %f %f

                set gxout shaded
                set clevs 20 34 50 64 100 130
                d mag(oacres(u.2,u.1*1.94),oacres(v.2,v.1*1.94))

                set gxout barb
                set cthick 12
                set ccolor 0
                d uso.1(t-0.5,t+0.5)*1.94;vso.1(t-0.5,t+0.5)*1.94
                set cthick 4
                set ccolor 1
                d uso.1(t-0.5,t+0.5)*1.94;vso.1(t-0.5,t+0.5)*1.94

                set parea 5.75 10.5 0 8
                set mpdset hires
                set digsize 0.05
                set lat %f %f
                set lon %f %f

                set gxout shaded
                set clevs 20 34 50 64 100 130
                d mag(oacres(u.2,u.1*1.94),oacres(v.2,v.1*1.94))

                set gxout barb
                set cthick 12
                set ccolor 0
                d uso.1(t-0.5,t+0.5)*1.94;vso.1(t-0.5,t+0.5)*1.94
                set cthick 4
                set ccolor 1
                d uso.1(t-0.5,t+0.5)*1.94;vso.1(t-0.5,t+0.5)*1.94
         
                set parea 0 11 0 8.5
                set string 1 c 10 
                set strsiz 0.2
                draw string 5.5 8.2 IRWD & Superobs [kts] 
                draw string 5.5 7.8 %s - %s - %d
                draw string 5.5 0.75 knots

                set string 1 l 5
                set strsiz 0.15

                draw string 1 7.4 lat:  %4.1f
                draw string 1 7.2 lon: %5.1f
                draw string 3.5 7.4 vmax:  %3d
                draw string 3.5 7.2 pmin: %4d
                draw string 6 7.4 r34: %3d
                draw string 6 7.2 r50: %3d
                draw string 8.5 7.4 dir:  %3d
                draw string 8.5 7.2 spd: %3d

                cbarn

                gxyat -x 1024 -y 768 %s
                clear
            """%(file_ctl, file_grid, prsLev, trk.rlat-5, trk.rlat+5, trk.rlon-5, trk.rlon+5, 19.0, 43.0, -95.0, -71.0, stmid, dtg, prsLev, trk.rlat, trk.rlon, trk.vmax, trk.pmin, r34m, r50m, trk.dir, trk.spd, file_png)
        ga(cmd)       
 
    def draw_old( self, dtg, storm, lat, lon, subtype, drawBufr, pressure, vmax, mprs, dir, r34, spd ):

        #if ( storm == '04e' and int( dtg ) < 2010061918 ): storm = '94e'
        #if ( storm == '05e' and int( dtg ) < 2010062306 ): storm = '95e'


        ga = GaGrads( 
                     lat1 = ( lat - 7 ),
                     lat2 = ( lat + 7 ),
                     lon1 = ( lon - 7 ),
                     lon2 = ( lon + 7 ),
                     quiet = 0 
                     )
        
        file2 = 'grid.ctl' 
        #os.system( 'stnmap2 -q -i %s' % ( file2 ) )              
        file1 = '%s/tcobs.cira.%s.%s.%s.ctl' % ( tbdir, dtg, storm, 'IRWD' )
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
            

            #drawBufr = False

            #if ( drawBufr ):
   
            #    cmdSub = ""
            #    for inc_i in range( len( subtype ) ):
            #    
            #        file = '/dat4/w21/prc/tcobs/obs.%s.%d.ctl' % ( dtg, subtype[inc_i] )
            #        os.system( 'stnmap2 -i %s' % ( file ) )
            #        fh = ga.open( file )
            #        if ( lev == 850.0 ): cmdSub += "set ccolor 7\n"
            #        else: cmdSub += "set ccolor 3\n"
            #        cmdSub += "d uo.%d(lev+50,lev-50)*1.94;vo.%d(lev+50,lev-50)*1.94\n" % ( inc_i + 3, inc_i + 3 )
            #    
            #    cmd += cmdSub
        
        if ( lon > 180 ): clon = lon - 360
        else: clon = lon


        filename = "%s/tcobs.cira.%s.%s.%s.Vmax%03d.%s.p%04d.png" % ( tbdir, storm, dtg[0:4], dtg, int( vmax ), 'irwd', pressure[0] )

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
        
        #============================================        
        #try:
        #    fh.close()
        #    print 'fh.close() worked'
        #except:
        #    print 'fh.close didn\'t work'
        #    try:
        #        fh = ga.close()
        #        print 'fh = ga.close() worked'
        #    except:
        #        print 'fh = ga.close() didn\'t work'
        #===========================================
        
#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# main 
argstr = "pyfile cur-18 "
argv = argstr.split()
argv = sys.argv
CL = TcObsCmdLine( argv = argv )
CL.CmdLine()
exec( CL.estr )
if( verb ): print CL.estr

tD=TcData()
dtgs = mf.dtg_dtgopt_prc( dtgopt )
mT = Mtcswa()

for dtg in dtgs:
    (itrk,genstmids)=tD.getTCtrkDtg(dtg)
    otrk=tD.dupTCtrkDtg(itrk,genstmids,selectNN=0)
    
    stm1ids=otrk.keys()
    stm1ids.sort()
    stm1ids=sortStmids(stm1ids)
    
    for stm1id in stm1ids:
        if (stm1id == stmopt):
            print stm1id
            trk=otrk[stm1id]
            fstm1id=tD.getFinalStm1idFrom(stm1id,trk.rlon,trk.b1id)
            print fstm1id
            if(fstm1id in genstmids): gentrk=1
            else: gentrk=0

            stmid = stmopt.split('.')[0].lower()
            mT.md2(dtg,stmid,trk)

sys.exit()

for dtg in dtgs:
    #year = dtg[0:4]
    #Case for single storm
    if ( stmopt != None ):
        stmid = stmopt.split( '.' )[0].lower()
        diafiles = glob.glob( "%s/%s/%s/*%s*DIA" % ( sbdir, year, stmid, dtg ) )
        for diafile in diafiles:
            mT.diaFile( diafile, dtg, stmid )
    #For all storms for dtg
    else:
        stmfolders = glob.glob( "%s/%s/*/" % ( sbdir, year ) )
        for stmfolder in stmfolders:
            length = len( stmfolder )
            stmid = stmfolder[length - 4:length - 1]
            diafiles = glob.glob( "%s/*%s*DIA" % ( stmfolder, dtg ) )
            for diafile in diafiles:
                mT.diaFile( diafile, dtg, stmid )
