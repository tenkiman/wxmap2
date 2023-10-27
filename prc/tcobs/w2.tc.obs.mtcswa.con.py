#!/usr/bin/env python

from TC import *

from mtcswaCurrent  import *
from prepbufrobs import *
from GA2 import *

import os

MF=MFutils()
        
#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# command line setup
#

class TcObsCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv
        
        self.argv=argv
        self.argopts={
            1:['dtgopt', 'run dtgs'],
            }

        self.defaults={
            'doupdate':0,
            }

        self.options={
            'override':['O',0,1,'override'],
            'verb':['V',0,1,'verb=1 is verbose'],
            'ropt':['N','','norun',' norun is norun'],
            'stmopt':['S:',None,'a','stmopt'],
            }

        self.purpose='''
purpose -- superob the CIRA MTCSWA (multi-platiform TC sfc wind analysis) AMSu and IRWD wind retrievals
for use in EnKF
'''
        self.examples='''
example:
%s 20090900100 -S 13e.9 # process Jimena'''


class Mtcswa(MFbase):

    sbdir=TcObsMtcswaSourceDir
    tbdir=TcObsSatWindsDir
    bufrdir='/dat4/w21/prc/tcobs'

    def lsObs(self,dtg,stm3id,lat,lon):
        #if (int(dtg) <  2009082906): stm3id = '94e'
        if ( stm3id == '04e' and int(dtg) < 2010061918 ): stm3id = '94e'
        if ( stm3id == '05e' and int(dtg) < 2010062306 ): stm3id = '95e'

        if ( lon > 180.0 ):
            lon = lon-360.0
        year=dtg[0:4]
        sdir="%s/%s/%s"%(self.sbdir,year,stm3id)
        obfiles=glob.glob("%s/*%s*obs"%(sdir,dtg))
        pressure = []
        openObFile = None
        for obfile in obfiles:
            print 'MTCSWA .obs file for dtg: ',dtg,' is: ',obfile
            print dtg,stm3id,obfile,self.tbdir,lat,lon
            satwinds = MtcswaObs(dtg,stm3id,obfile,self.tbdir,lat,lon)
            openObFile = satwinds.openFile
            if (not openObFile): break
            pressure = satwinds.RunProgram()
        self.obfiles=obfiles
        try:
            satobs = SatWindsObs(self.bufrdir,self.bufrdir,dtg,lat,lon)
            subtype = satobs.RunProgram()
            drawBufr = True
        except:
            subtype = None
            drawBufr = False
            
        return (subtype, drawBufr, pressure,openObFile)
        
        
    def draw(self,dtg,storm,lat,lon,subtype, drawBufr, pressure,vmax,mprs):
        
        #if (int(dtg) <  2009082906): storm = '94e'
        if ( storm == '04e' and int(dtg) < 2010061918 ): storm = '94e'
        if ( storm == '05e' and int(dtg) < 2010062306 ): storm = '95e'


        ga = GaGrads(lat1=(lat-30),
                     lat2=(lat+30),
                     lon1=(lon-30),
                     lon2=(lon+30),
                     quiet=1)
        
        
        #ga = GaGrads(lat1=(-1),
        #             lat2=(42),
        #             lon1=(-126),
        #             lon2=(-87),
        #             quiet=1)
        
        file2 = '%s/tcobs.cira.2009082906.13e.IRWD.grid.ctl'%(self.tbdir)
        os.system('stnmap2 -q -i %s'%(file2))              
        
        file1 = '%s/tcobs.cira.%s.%s.%s.ctl'%(self.tbdir,dtg,storm,'IRWD')
        os.system('stnmap2 -q -i %s'%(file1))              
        fh = ga.open(file1)        
        fh = ga.open(file2)
        ga.setLatLon()
        ga.setMap()
        
        cmd = ""
        
        for lev in pressure:
           
        #    cmd += """
        #    set lev %d
        #    set gxout shaded 
        #    """%lev
            
            #if ( lev == 850.0 ): cmd +="set ccolor 8\n"
            #else: cmd += "set ccolor 2\n"
            
            #cmd += "d u.1(t-0.5,t+0.5)*1.94;v.1(t-0.5,t+0.5)*1.94\n"            
            
         #   cmd += "set clevs -10 -7.5 -5 -2.5 0 2.5 5 7.5 10\n"
            #cmd += "set ccols 5 13 3 10 0 0 7 8 2 6\n"
         #   cmd += "set ccols 14 4 11 5 0 0 7 8 2 6\n"
            #cmd += "set rbrange -10 10\nset cint 2.5\n"

         #   cmd += "d hdivg(oacres(re2(u.2(t=1),0.25),u.1,10,7,4),oacres(re2(v.2(t=1),0.25),v.1,10,7,4))*1e5\nset gxout contour\nset cint 2.5\nset ccolor 1\n"

          #  cmd += "d hdivg(oacres(re2(u.2(t=1),0.25),u.1,10,7,4),oacres(re2(v.2(t=1),0.25),v.1,10,7,4))*1e5\ncbarn\n"
           # cmd += "set gxout barb\nset cthick 10\nset ccolor 0\n"
           # cmd += " d uso.1(t-0.5,t+0.5)*1.94;vso.1(t-0.5,t+0.5)*1.94\nset cthick 4\n"
            

           # if ( lev == 850.0 ): cmd +="set ccolor 14\n"
           # else: cmd += "set ccolor 4\n"
    
            #if ( lev == 850.0 ): cmd +="set ccolor 10\n"
            #else: cmd += "set ccolor 3\n"

        #    cmd += "d uso.1(t-0.5,t+0.5)*1.94;vso.1(t-0.5,t+0.5)*1.94\n"

         #   cmd += "set ccolor 2"

          #  cmd += "d uso.1(t-0.5,t+0.5)*1.94;maskout(vso.1(t-0.5,t+0.5)*1.94,mag(uso.1(t-0.5,t+0.5)*1.94,vso.1(t-0.5,t+0.5)*1.94)-65.0))\n"
            

           

             if ( drawBufr ):
   
                cmdSub = ""
                for inc_i in range(len(subtype)):
                
                    file = '/dat4/w21/prc/tcobs/obs.%s.%d.ctl'%(dtg,subtype[inc_i])
                    os.system('stnmap2 -i %s'%(file))
                    fh = ga.open(file)
                    if ( lev == 850.0 ): cmdSub +="set ccolor 14\n"
                    else: cmdSub += "set ccolor 4\n"
                    cmdSub +="d uo.%d(lev+50,lev-50)*1.94;vo.%d(lev+50,lev-50)*1.94\n"%(inc_i+3,inc_i+3)
                
                cmd += cmdSub
        
        if (lon > 180): clon = lon -360
        else: clon = lon

        cmd += """
    draw wxsym 41 5.5 4.2 0.8 1 50
    draw title %s - IRWD - %s\Conventional Observations [kts] 
    draw string 0.5 5.6 clat: %4.1f
    draw string 0.5 5.3 clon: %5.1f
    draw string 0.5 5.0 vmax: %d kts
    draw string 0.5 4.7 pmin: %d mb
    draw string 0.5 4.4 plev: %d mb
    gxyat %s.%s.con.png
    c

    """%(storm,dtg,lat,clon,vmax,mprs,pressure[0],dtg,storm)
            
        ga._cmd(cmd)
        
        
        
        
#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# main 
argstr="pyfile cur-18 "
argv=argstr.split()
argv=sys.argv
CL=TcObsCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

dtgs=mf.dtg_dtgopt_prc(dtgopt)

mT=Mtcswa()

for dtg in dtgs:

    tcD=TcData()
    (stmids,btcs)=tcD.getDtg(dtg,dupchk=1)

    for stmid in stmids:
        if ( stmopt != None):
            if ( stmid.split('.')[0].lower() == stmopt.split('.')[0].lower() ):
                lat = float(btcs[stmid][0])
                lon = float(btcs[stmid][1])
                vmax = float(btcs[stmid][2])
                mprs = float(btcs[stmid][3])
                stm3id=stmid.split('.')[0].lower()
                (subtype, drawBufr, pressure,openObFile) = mT.lsObs(dtg,stm3id,lat,lon)
                if (openObFile): mT.draw(dtg, stm3id, lat, lon, subtype, drawBufr, pressure,vmax,mprs)
            else:
               None
        else:
            lat = float(btcs[stmid][0])
            lon = float(btcs[stmid][1])
            stm3id=stmid.split('.')[0].lower()
            (subtype, drawBufr, pressure,openObFile) = mT.lsObs(dtg,stm3id,lat,lon)
            if (openObFile): mT.draw(dtg, stm3id, lat, lon, subtype, drawBufr, pressure)


    
        
