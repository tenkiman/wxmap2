import rlcompleter
import readline
readline.parse_and_bind("tab: complete")

import os
import sys 

import struct
import array
import time

from math import sqrt, pow

import mf
from TC import gc_dist

import numpy

class SatWinds:

    Inputdir = '/w21/dat/tc/cira/mtcswa/'

    Basedir = '/dat4/w21/prc/tcobs/'
    
    #Basedir = Inputdir = '/home/amb/slocum/Documents/workspace/satwindstats/src/'
    
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
    
    DataTypes = ['AMSU','IRWD','CD','ASCT'] 
    
    Inc = 1

    R1 = 60.0

    R2 = 180.0


    def __init__(self,dtg,storm,file,rad,cLat,cLon):
        __inputPath  = '%s%s/%s/%s%s.obs'%(self.Inputdir,dtg[0:4],storm,file,dtg)
        self.outputPath = {}
        self.ctlPath    = {}
        self.smpPath    = {}
        
        try:
            self.oInputPath = open(__inputPath)
        except:
            raise IOError('Unable to open: %s'(__inputPath))
        
        for dt in self.DataTypes:
            __outputPath = '%s%s%s_%s.obs'%(self.Basedir,file,dtg,dt)
            __ctlPath    = '%s%s%s_%s.ctl'%(self.Basedir,file,dtg,dt)
            __smpPath    = '%s%s%s_%s.smp'%(self.Basedir,file,dtg,dt)
            
            try:
                self.outputPath[dt]=open(__outputPath,'wb')
            except:
                raise IOError('Unable to open: %s'(__outputPath))
            
            self.CtlFile(__ctlPath,__smpPath,__outputPath,dtg,dt)

        self.radius = rad
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
            elif ( (datatype == self.DataTypes[1] or datatype == self.DataTypes[2]) and v != self.Vars[3] and v != self.Vars[4] ):
                desc='%s %s'%(self.VarDesc[v],self.VarUnits[v])
                vars.append('%-7s 1 0 %s'%(v,desc))
            elif( datatype == self.DataTypes[3] and v != self.Vars[3] and v != self.Vars[4] ):
                desc='%s %s'%(self.VarDesc[v],self.VarUnits[v])
                vars.append('%-7s 0 0 %s'%(v,desc))
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
        
        iSplit=[17,26,45,52,61,73,82,87,105]
        eSplit=[23,32,50,59,68,77,86,95,113]
        
        data=[]
        
        for i in range(len(iSplit)):
            dsplit=ncard[iSplit[i]:eSplit[i]].split()
            data=data+dsplit
                
        #meta=(lat,lon,uwd,vwd,wsp,psr,typ,tmp,hgt)
        meta=(data[0],data[1],data[3],data[4],data[2],data[5],data[6],data[7],data[8])
        
        ostnid='sn%06d'%(self.Inc)
        
        self.Inc+=1
        
        return(ostnid,meta)
    
    #def LoadDataArrays(self):
    #    
    #    (cards) = self.ReadCards()
    #    
    #    umeta = {}
    #    
    #    for ncard in cards:
    #        (ostnid,meta)=self.ParseCards(ncard)
    #        
    #        try:
    #            umeta[ostnid]={}
    #            umeta[ostnid][meta[0]]={}
    #            umeta[ostnid][meta[0]][meta[1]]=[]
    #            umeta[ostnid][meta[0]][meta[1]].append(meta)
    #        except:
    #            'Error creating dictionary.'
    #            
    #    return(umeta)

    def LoadDataAnnulus(self):

        (cards) = self.ReadCards()

        umeta = {}

        for ncard in cards:
            (ostnid,meta)=self.ParseCards(ncard)

            lat = meta[0]
            lon = meta[1]

            (radius) = gc_dist(float(lat),float(lon),self.centerLat,self.centerLon)

            if ( radius >= self.R1 and radius <= self.R2 ):
                #try:
                #    umeta[ostnid][lat][lon].append(meta)
                #except:
                #    try:
                #        umeta[ostnid][lat][lon]=[]
                #        umeta[ostnid][lat][lon].append(meta)
                #    except:
                #        try:
                #            umeta[ostnid][lat]={}
                #            umeta[ostnid][lat][lon]=[]
                #            umeta[ostnid][lat][lon].append(meta)
                #        except:
                #            umeta[ostnid]={}
                #            umeta[ostnid][lat]={}
                #            umeta[ostnid][lat][lon]=[]
                #            umeta[ostnid][lat][lon].append(meta)
        
                try:
                    umeta[ostnid].append(meta)
                except:
                    umeta[ostnid]=[]
                    umeta[ostnid].append(meta)
        
        return(umeta)
                    
#    def CheckRadius(self,lat,lon):
#        distance = sqrt(pow(lat-self.centerLat,2)+pow(lon-self.centerLon,2))
#
#        if ( distance <= self.radius ):
#            return(True)
#        else:
#            return(False)

    def QualityControl(self, umeta):
        
        stnid = []
        windspd = []
        valid = []
        
        meta ={}
        
        qcmeta={}
        
        stns=umeta.keys()
        stns.sort()
        for stn in stns:
            basemeta = umeta[stn][0]
                
            if ( basemeta[6] == 'AMSU' and basemeta[5] == '700' ):
                stnid.append(stn)
                windspd.append(float(basemeta[4]))
                
        mean = numpy.mean(windspd)
        std = numpy.std(windspd)
        
        for inc in range(len(windspd)):
            if ( windspd[inc] > -2.0*std and windspd[inc] < 2.0*std ):
                #print 'GOOD: ', stnid[inc], umeta[stnid[inc]][0]
                try:
                    qcmeta[stnid[inc]].append(umeta[stnid[inc]][0])
                except:
                    qcmeta[stnid[inc]]=[]
                    qcmeta[stnid[inc]].append(umeta[stnid[inc]][0])        
                    
            else:
                #print 'BAD: ', stnid[inc], umeta[stnid[inc]][0]
                None

        return(qcmeta)
    
    def WriteOutput(self,basemeta,stn):
        
        stnid = stn
        stndt = 0.0
        
        lat=float(basemeta[0])
        lon=float(basemeta[1])
        uwd=float(basemeta[2])
        vwd=float(basemeta[3])
        wsp=float(basemeta[4])
        psr=float(basemeta[5])
        typ=basemeta[6]
        tmp=float(basemeta[7])
        hgt=float(basemeta[8])
        
        if(lon<0.0):
            rlon=360.0+lon
        else:
            rlon=lon

        rlat=lat  
            
        stnhead = struct.pack('8sfffii',stnid,rlat,rlon,stndt,1,0)
            
        if ( typ == self.DataTypes[0] ):
            stnrec = struct.pack('%df'%6,psr,uwd,vwd,wsp,tmp,hgt)
        elif ( typ == self.DataTypes[1] or typ == self.DataTypes[2] ):
            stnrec = struct.pack('%df'%4,psr,uwd,vwd,wsp)
        elif ( typ == self.DataTypes[3] ):
            stnhead = struct.pack('8sfffii',stnid,rlat,rlon,stndt,1,1)
            stnrec = struct.pack('%df'%3,uwd,vwd,wsp)
        else:
            None
        
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
    
        #for stn in stns:
        #    lt = umeta[stn].keys()
        #    for lat in lt:
        #        lon = umeta[stn][lat].keys()
        #        
        #        basemeta = umeta[stn][lat][lon[0]][0]
        #        
        #        satwinds.WriteOutput(basemeta,stn)
    
        for stn in stns:
            basemeta = qcmeta[stn][0]
            satwinds.WriteOutput(basemeta,stn)

                
        self.FinalizeOutput()
                
if(__name__ == '__main__'):

    satwinds = SatWinds('2010060218','03a','2010IO03_MPSATWD_',4.0,18.0,59.0)
    
    stime=time.time()
    (umeta) = satwinds.LoadDataAnnulus()
    mf.Timer('Read Cards and loaded data. ', stime)
    
    stime=time.time()
    (qcmeta) = satwinds.QualityControl(umeta)
    mf.Timer('Quality Control. ', stime)
    
    
    stimer=time.time()    
    satwinds.GenOutput(qcmeta)
    mf.Timer('Finished creating obs files. ', stime)
    
    print 'The program has finished!'
