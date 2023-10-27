import rlcompleter
import readline
readline.parse_and_bind("tab: complete")

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

import numpy

class MtcswaObs:
    
    Undef=-999.999
    
    Vars = ['u','v','w','t','z']
    
    VarDesc={
             'u':'u comp wind',
             'v':'v comp wind',
             'w':'Wind Speed',
             't':'Temperature',
             'z':'Height',
            }
    VarUnits={
              'u':'[knots]',
              'v':'[knots]',
              'w':'[knots]',
              't':'[K]',
              'z':'[m]',
             }
    
    DataTypes = ['AMSU','IRWD']#,'CD','ASCT']
    
    Inc = 1

    R1 = 60.0

    R2 = 180.0
    
    deltaR = 60.0


    def __init__(self,dtg,storm,inputpath,outputdir,cLat,cLon):
        #__inputPath  = '%s%s/%s/%s%s.obs'%(self.Inputdir,dtg[0:4],storm,file,dtg)
        __inputPath = inputpath
        self.Basedir = outputdir
        self.Storm = storm
        self.outputPath = {}
        self.ctlPath    = {}
        self.smpPath    = {}
        
        try:
            self.oInputPath = open(__inputPath)
        except:
            raise IOError('Unable to open: %s'(__inputPath))
        
        for dt in self.DataTypes:
            __outputPath = '%s/%s.%s.%s.obs'%(self.Basedir,dtg,storm,dt)
            __ctlPath    = '%s/%s.%s.%s.ctl'%(self.Basedir,dtg,storm,dt)
            __smpPath    = '%s/%s.%s.%s.smp'%(self.Basedir,dtg,storm,dt)
            
            try:
                self.outputPath[dt]=open(__outputPath,'wb')
            except:
                raise IOError('Unable to open: %s'(__outputPath))
            
            self.CtlFile(__ctlPath,__smpPath,__outputPath,dtg,dt)

        self.centerLat = cLat
        self.centerLon = cLon

    def CtlFile(self,ctlPath,smpPath,outPath,dtg,datatype):
        try:
            oCtlPath = open(ctlPath,'w')
        except:
            raise IOError('Unable to open: %s'(ctlPath))
        
        (dir,outFile) = os.path.split(outPath)
        (dir,sFile) = os.path.split(smpPath)

        gtime=mf.dtg2gtime(dtg)
        
        vars=[]
        
        for v in self.Vars:
            if ( datatype == self.DataTypes[0] ):
                desc='%s %s'%(self.VarDesc[v],self.VarUnits[v])
                vars.append('%-7s 1 0 %s'%(v,desc))
            #elif ( (datatype == self.DataTypes[1] or datatype == self.DataTypes[2]) and v != self.Vars[3] and v != self.Vars[4] ):
            elif ( datatype == self.DataTypes[1] and v != self.Vars[3] and v != self.Vars[4] ):
                desc='%s %s'%(self.VarDesc[v],self.VarUnits[v])
                vars.append('%-7s 1 0 %s'%(v,desc))
            #elif( datatype == self.DataTypes[3] and v != self.Vars[3] and v != self.Vars[4] ):
            #    desc='%s %s'%(self.VarDesc[v],self.VarUnits[v])
            #    vars.append('%-7s 0 0 %s'%(v,desc))
            else:
                None
                
        ctl="""dset    ^%s
title   Sat Winds
dtype   station
stnmap  ^%s
undef   %07.3f
tdef    1 linear %s 1hr
vars    %d
"""%(outFile,sFile,self.Undef,gtime,len(vars))

        for v in vars:
            ctl=ctl+"%s\n"%(v)
        ctl=ctl+'endvars\n'
        
        oCtlPath.writelines(ctl)
        
    def ReadCards(self):
        cards=self.oInputPath.readlines()
        return(cards)
    
    def ParseCards(self,ncard):
        
        iSplit=[17,26,44,52,61,73,82,87,105,0]
        eSplit=[23,32,50,59,68,77,86,95,113,12]
        
        data=[]
        
        for i in range(len(iSplit)):
            dsplit=ncard[iSplit[i]:eSplit[i]].split()
            data=data+dsplit

        meta=(float(data[0]),float(data[1]),float(data[3]),float(data[4]),float(data[2]),float(data[5]),data[6],float(data[7]),float(data[8]),data[9])
        
        ostnid='sn%06d'%(self.Inc)
        
        self.Inc+=1
        
        return(ostnid,meta)

    def LoadDataAnnulus(self):

        (cards) = self.ReadCards()

        umeta = {}

        for ncard in cards:
            (ostnid,meta)=self.ParseCards(ncard)

            lat = meta[0]
            lon = meta[1]

            (radius) = gc_dist(self.centerLat, self.centerLon, lat, lon)

            if ( radius >= self.R1 and radius <= self.R2 ):
                try:
                    umeta[ostnid].append(meta)
                except:
                    umeta[ostnid]=[]
                    umeta[ostnid].append(meta)
        
        return(umeta)
    
#
# Quality Control
#
    
    def QualityControl(self,umeta):
                 
        qcmeta={}
        
        stnid = umeta.keys()
        stnid.sort()
        
        for stn in stnid:
            if (umeta[stn][0][4] < 150.0*knots2ms):
                try:
                    qcmeta[stn].append(umeta[stn][0])
                except:
                    qcmeta[stn]=[]
                    qcmeta[stn].append(umeta[stn][0]) 
            else:
                None            
            
        return qcmeta
        
                            
    def SuperObsAveraging(self,qcmeta):
        
        someta = {}
        sostats = {}
        
        (lats_0,lons_0) = getLatLonArrays3(self.centerLat,self.centerLon,self.deltaR,self.R1, self.R2)
        
        winds = {}
        ucomp = {}
        vcomp = {}
        temps = {}
        hgt = {}
        count = {}
        
        stns=qcmeta.keys()
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

            for inc in range(len(lats_0)):
                radius = gc_dist(lats_0[inc],lons_0[inc],dlat,dlon)
                if ( radius <= (self.deltaR*0.5)):
                    try:
                        winds[type,dtg,prslev][lats_0[inc],lons_0[inc]].append(wdspd)
                        ucomp[type,dtg,prslev][lats_0[inc],lons_0[inc]].append(uwind)
                        vcomp[type,dtg,prslev][lats_0[inc],lons_0[inc]].append(vwind)
                        temps[type,dtg,prslev][lats_0[inc],lons_0[inc]].append(temp)
                        hgt[type,dtg,prslev][lats_0[inc],lons_0[inc]].append(height)
                    except:
                        try:
                            winds[type,dtg,prslev][lats_0[inc],lons_0[inc]] = []
                            winds[type,dtg,prslev][lats_0[inc],lons_0[inc]].append(wdspd)
                            ucomp[type,dtg,prslev][lats_0[inc],lons_0[inc]] = []
                            ucomp[type,dtg,prslev][lats_0[inc],lons_0[inc]].append(uwind)
                            vcomp[type,dtg,prslev][lats_0[inc],lons_0[inc]] = []
                            vcomp[type,dtg,prslev][lats_0[inc],lons_0[inc]].append(vwind)
                            temps[type,dtg,prslev][lats_0[inc],lons_0[inc]] = []
                            temps[type,dtg,prslev][lats_0[inc],lons_0[inc]].append(temp)
                            hgt[type,dtg,prslev][lats_0[inc],lons_0[inc]] = []
                            hgt[type,dtg,prslev][lats_0[inc],lons_0[inc]].append(height)
                        except:
                            winds[type,dtg,prslev] = {}
                            winds[type,dtg,prslev][lats_0[inc],lons_0[inc]] = []
                            winds[type,dtg,prslev][lats_0[inc],lons_0[inc]].append(wdspd)
                            ucomp[type,dtg,prslev] = {}
                            ucomp[type,dtg,prslev][lats_0[inc],lons_0[inc]] = []
                            ucomp[type,dtg,prslev][lats_0[inc],lons_0[inc]].append(uwind)
                            vcomp[type,dtg,prslev] = {}
                            vcomp[type,dtg,prslev][lats_0[inc],lons_0[inc]] = []
                            vcomp[type,dtg,prslev][lats_0[inc],lons_0[inc]].append(vwind)
                            temps[type,dtg,prslev] = {}
                            temps[type,dtg,prslev][lats_0[inc],lons_0[inc]] = []
                            temps[type,dtg,prslev][lats_0[inc],lons_0[inc]].append(temp)
                            hgt[type,dtg,prslev] = {}
                            hgt[type,dtg,prslev][lats_0[inc],lons_0[inc]] = []
                            hgt[type,dtg,prslev][lats_0[inc],lons_0[inc]].append(height)
                else:
                    None
        
        typdtglev = winds.keys()
        typdtglev.sort()
        
        inc = 0
        
        for typedtgelev in typdtglev:
            ltln = winds[typedtgelev].keys()      
            ltln.sort()
            self.CreateFilesAndHeaders(typedtgelev)
            for latlon in ltln:
                avewind = numpy.mean(winds[typedtgelev][latlon])
                aveu = numpy.mean(ucomp[typedtgelev][latlon])
                avev = numpy.mean(vcomp[typedtgelev][latlon])
                avet = numpy.mean(temps[typedtgelev][latlon])
                avez = numpy.mean(hgt[typedtgelev][latlon])
                
                meta = (latlon[0], latlon[1], typedtgelev[2], aveu, avev, avewind, avet, avez, typedtgelev[0],typedtgelev[1])
                stats = (typedtgelev, latlon[0], latlon[1],
                         len(ucomp[typedtgelev][latlon]), avewind, numpy.std(ucomp[typedtgelev][latlon]),
                         len(vcomp[typedtgelev][latlon]), avewind, numpy.std(vcomp[typedtgelev][latlon]))
                
                stnid = "stn%05d"%inc
                inc += 1
                
                try:
                    someta[stnid].append(meta)
                    sostats[stnid].append(stats)
                except:
                    try:
                        someta[stnid] = []
                        someta[stnid].append(meta)
                        sostats[stnid] = []
                        sostats[stnid].append(stats)
                    except:
                        someta[stnid] = {}
                        someta[stnid] = []
                        someta[stnid].append(meta)
                        sostats[stnid] = {}
                        sostats[stnid] = []
                        sostats[stnid].append(stats)
        
        return (someta,sostats)
   
#
# Before super obs output
#
    
    def WriteOutput(self,basemeta,stn):
        
        stnid = stn
        stndt = 0.0
        
        lat=basemeta[0]
        lon=basemeta[1]
        uwd=basemeta[2]
        vwd=basemeta[3]
        wsp=basemeta[4]
        psr=basemeta[5]
        typ=basemeta[6]
        tmp=basemeta[7]
        hgt=basemeta[8]
        
        if(lon<0.0):
            rlon=360.0+lon
        else:
            rlon=lon

        rlat=lat  
            
        stnhead = struct.pack('8sfffii',stnid,rlat,rlon,stndt,1,0)
        
        NA = 0
            
        if ( typ == self.DataTypes[0] ):
            stnrec = struct.pack('%df'%6,psr,uwd,vwd,wsp,tmp,hgt)
        #elif ( typ == self.DataTypes[1] or typ == self.DataTypes[2] ):
        elif ( typ == self.DataTypes[1]):
            stnrec = struct.pack('%df'%4,psr,uwd,vwd,wsp)
        #elif ( typ == self.DataTypes[3] ):
        #    stnhead = struct.pack('8sfffii',stnid,rlat,rlon,stndt,1,1)
        #    stnrec = struct.pack('%df'%3,uwd,vwd,wsp)
        else:
            NA = 1
        
        if (NA != 1):
            self.outputPath[typ].write(stnhead)
            self.outputPath[typ].write(stnrec)
    
    def FinalizeOutput(self):
        stnid='alldone '
        stnrec=struct.pack('8sfffii',stnid,0.0,0.0,0.0,0,0)
        for dt in self.DataTypes:
            self.outputPath[dt].write(stnrec)
            self.outputPath[dt].close()
            
        try:
            self.oInputPath.close()
        except:
            None
            
    def GenOutput(self,qcmeta):
        
        stns=qcmeta.keys()
        stns.sort()

        for stn in stns:
            basemeta = qcmeta[stn][0]
            self.WriteOutput(basemeta,stn)

                
        self.FinalizeOutput()
        
#
# Super Obs Output
#
        
    def WriteSuperOutput(self,basemeta,stn):
        
        stnid = stn
        stndt = 0.0
        
        lat=basemeta[0]
        lon=basemeta[1]
        psr=basemeta[2]
        uwd=basemeta[3]
        vwd=basemeta[4]
        wsp=basemeta[5]
        tmp=basemeta[6]
        hgt=basemeta[7]
        typ=basemeta[8]
        
        if(lon<0.0):
            rlon=360.0+lon
        else:
            rlon=lon

        rlat=lat  
            
        stnhead = struct.pack('8sfffii',stnid,rlat,rlon,stndt,1,0)
        stnrec =  struct.pack('%df'%6,psr,uwd,vwd,wsp,tmp,hgt)
        
        NA = 0
            
        if ( typ == self.DataTypes[0] ):
            stnrec = struct.pack('%df'%6,psr,uwd,vwd,wsp,tmp,hgt)
        elif ( typ == self.DataTypes[1] or typ == self.DataTypes[2] ):
            stnrec = struct.pack('%df'%4,psr,uwd,vwd,wsp)
        elif ( typ == self.DataTypes[3] ):
            stnhead = struct.pack('8sfffii',stnid,rlat,rlon,stndt,1,1)
            stnrec = struct.pack('%df'%3,uwd,vwd,wsp)
        else:
            NA = 1
        
        if (NA != 1):
            self.outputPath[typ].write(stnhead)
            self.outputPath[typ].write(stnrec)
            
    def GenSuperOutput(self,someta):
        stns=someta.keys()
        stns.sort()
        
        for stn in stns:
            basemeta = someta[stn][0]
            self.WriteSuperOutput(basemeta,stn)
            
        self.FinalizeOutput()
        
#
# Write Super Obs txt files
#

    def CreateFilesAndHeaders(self,typedtgelev):
       
        try:
            self.soOpen[typedtgelev] = "%s/%s.%s.%s.%04d.txt"%(self.Basedir,typedtgelev[1],self.Storm,typedtgelev[0],typedtgelev[2])
        except:
            try:
                self.soOpen[typedtgelev] = []
                self.soOpen[typedtgelev] = "%s/%s.%s.%s.%04d.txt"%(self.Basedir,typedtgelev[1],self.Storm,typedtgelev[0],typedtgelev[2])
            except:
                self.soOpen = {}
                self.soOpen[typedtgelev] = []
                self.soOpen[typedtgelev] = "%s/%s.%s.%s.%04d.txt"%(self.Basedir,typedtgelev[1],self.Storm,typedtgelev[0],typedtgelev[2])
        
        soFile = open(self.soOpen[typedtgelev],'w')
        soFile.writelines("Platform:%s DateTimeGroup:%s PressureLev:%04d\n"%(typedtgelev[0],typedtgelev[1],typedtgelev[2]))
    
    def WriteSuperObs(self,basestat):
        typedtgelev = basestat[0]
        record = "Lat: %6.2f Lon: %7.2f u(m/s): numobs: %3d mean: %5.1f std: %5.1f v(m/s): numobs: %3d mean: %5.1f std: %5.1f  \n"%(basestat[1],basestat[2],basestat[3],basestat[4],basestat[5],basestat[6],basestat[7],basestat[8])
        soFile = open(self.soOpen[typedtgelev],'a')
        soFile.writelines(record)

    def GenSuperObs(self,sostats):
        
        stnid = sostats.keys()
        stnid.sort()
        
        for stn in stnid:
            basestat = sostats[stn][0]
            self.WriteSuperObs(basestat)
            
    def RunProgram(self):
        stime=time.time()
        (umeta) = self.LoadDataAnnulus()
        mf.Timer('Read Cards and loaded data. ', stime)
    
        stime=time.time()
        (qcmeta) = self.QualityControl(umeta)
        mf.Timer('Quality Control. ', stime)
    
        stimer=time.time()    
        self.GenOutput(qcmeta)
        mf.Timer('Finished creating obs files. ', stime)
    
        stimer=time.time()
        (someta, sostats) = self.SuperObsAveraging(qcmeta)
        mf.Timer('Done Averaging for super obs', stime)
    
        #stimer=time.time()    
        #satwinds.GenSuperOutput(someta)
        #mf.Timer('Finished creating super obs grads files', stime)
    
        stimer=time.time()    
        self.GenSuperObs(sostats)
        mf.Timer('Finished writing super obs files.', stime)
    
        print 'The program has finished!'
                
if(__name__ == '__main__'):

    satwinds = Mtcswa('2009082906','13e','/home/amb/slocum/workspace/mtcswa/src/2010/03a/2010IO03_MPSATWD_2010060218.obs','/home/amb/slocum/workspace/mtcswa/src',18.0,60.5)
    
    Mtcswa.RunProgram()
    
    #stime=time.time()
    #(umeta) = satwinds.LoadDataAnnulus()
    #mf.Timer('Read Cards and loaded data. ', stime)
    
    #stime=time.time()
    #(qcmeta) = satwinds.QualityControl(umeta)
    #mf.Timer('Quality Control. ', stime)
    
    #stimer=time.time()    
    #satwinds.GenOutput(qcmeta)
    #mf.Timer('Finished creating obs files. ', stime)
    
    #stimer=time.time()
    #(someta, sostats) = satwinds.SuperObsAveraging(qcmeta)
    #mf.Timer('Done Averaging for super obs', stime)
    
    ##stimer=time.time()    
    ##satwinds.GenSuperOutput(someta)
    ##mf.Timer('Finished creating super obs grads files', stime)
    
    #stimer=time.time()    
    #satwinds.GenSuperObs(sostats)
    #mf.Timer('Finished writing super obs files.', stime)
    
    #print 'The program has finished!'
