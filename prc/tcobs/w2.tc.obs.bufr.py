import rlcompleter
import readline
readline.parse_and_bind("tab: complete")

import os
import sys 

import struct
import array
import time

import mf

from TCobs import gc_ltlg

from TC import gc_dist

from const import *

class SatWinds:

    #Inputdir = '/w21/dat/tc/cira/mtcswa/'

    #Basedir = '/dat4/w21/prc/tcobs/'
    
    Basedir = Inputdir = '/dat4/w21/prc/tcobs/'
    
    
    Undef=1e20
    
    Vars = ['uo','uf','vo','vf','st']
    
    VarDesc={
             'uo':'obs u comp wind',
             'uf':'fct u comp wind',
             'vo':'obs v comp wind',
             'vf':'fct v comp wind',
             'st':'Data Subtype'
            }
    VarUnits={
              'uo':'[knots]',
              'uf':'[knots]',
              'vo':'[knots]',
              'vf':'[knots]',
              'st':'[#]'
             }
    
    Inc = 1

    R1 = 60.0

    R2 = 180.0
    
    deltaR = 60.0
    
    subtype = []


    def __init__(self,dtg,cLat,cLon):
        __uInputPath = '%sobs.u.%s.txt'%(self.Inputdir,dtg)
        __vInputPath = '%sobs.v.%s.txt'%(self.Inputdir,dtg)
        self.outputPath = {}
        
        try:
            self.uInputPath = open(__uInputPath)
            self.vInputPath = open(__vInputPath)
        except:
            raise IOError('Unable to open: %s or %s'%(__uInputPath,__vInputPath))
        
        if(cLon<0.0):
            cLon=360.0+cLon
        else:
            None

        self.centerLat = cLat
        self.centerLon = cLon
        self.dtg = dtg
        
    def CreateFiles(self,subtype):
        
        try:
            self.subtype.index(subtype)
            None
        except:
            self.subtype.append(subtype)
        
            __outputPath = '%sobs.%s.%03d.obs'%(self.Basedir,self.dtg,subtype)
            __ctlPath    = '%sobs.%s.%03d.ctl'%(self.Basedir,self.dtg,subtype)
            __smpPath    = '%sobs.%s.%03d.smp'%(self.Basedir,self.dtg,subtype)
                
            try:
                self.outputPath[subtype]=open(__outputPath,'wb')
                self.CtlFile(__ctlPath,__smpPath,__outputPath,self.dtg,subtype)
            except:
                raise IOError('Unable to open: %s'(__outputPath))

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
            desc='%s %s'%(self.VarDesc[v],self.VarUnits[v])
            vars.append('%-7s 1 0 %s'%(v,desc))
 
                
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
        uCards=self.uInputPath.readlines()
        vCards=self.vInputPath.readlines()
        return(uCards,vCards)
    
    def ParseCards(self,ncard,inc):
        
        iSplit=[7,17,38,46,56,77,95,0]
        eSplit=[15,25,45,55,65,78,98,5]
        
        data=[]
        
        for i in range(len(iSplit)):
            dsplit=ncard[iSplit[i]:eSplit[i]].split()
            data=data+dsplit

        meta=(float(data[3]),float(data[2]),float(data[4]),data[5],float(data[1]),float(data[0]),float(data[6]))
        
        ostnid='sn%06d'%(float(data[7]))
        
        return(ostnid,meta)

    def LoadDataAnnulus(self):

        (uCards,vCards) = self.ReadCards()

        umeta = {}

        if (len(uCards) == len(vCards)):
            for inc in range(15,len(uCards)):
                (ostnid,metaU)=self.ParseCards(uCards[inc],0)
                (ostnid,metaV)=self.ParseCards(vCards[inc],1)
                                            
                lat = metaU[0]
                lon = metaU[1]
                
                if (lat == metaV[0] and lon == metaU[1] and metaU[6] == metaV[6] and metaU[2] == metaV[2]):
        
                    (radius) = gc_dist(self.centerLat, self.centerLon, lat, lon)
        
                    #if ( radius >= self.R1 and radius <= self.R2 ):
                    uwdob = metaU[4]
                    vwdob = metaV[4]
                    uwdfc = metaU[5]
                    vwdfc = metaV[5]
                    prs = metaU[2]
                    subtype = metaU[6]
                    
                    meta = (lat,lon,prs,uwdob,uwdfc,vwdob,vwdfc,subtype)
                    try:
                        umeta[ostnid,subtype].append(meta)
                    except:
                        umeta[ostnid,subtype]=[]
                        umeta[ostnid,subtype].append(meta)
                    #else:
                    #    None
                else:
                    print 'Error: Lat and Lon do not match in the data file.'
                    
        else:
            print 'Error: Data does not match in data file.'
        
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
    
#
# Before super obs output
#
    
    def WriteOutput(self,basemeta,stn):
        
        stnid = stn[0]
        typ = stn[1]
        stndt = 0.0
        
        lat=basemeta[0]
        lon=basemeta[1]
        prs=basemeta[2]
        uob=basemeta[3]
        ufc=basemeta[4]
        vob=basemeta[5]
        vfc=basemeta[6]
        sbt=basemeta[7]
        
        if(lon<0.0):
            rlon=360.0+lon
        else:
            rlon=lon

        rlat=lat  
            
        stnhead = struct.pack('8sfffii',stnid,lat,lon,stndt,1,0)
            
        stnrec = struct.pack('%df'%6,prs,uob,ufc,vob,vfc,sbt)
        
        self.outputPath[typ].write(stnhead)
        self.outputPath[typ].write(stnrec)
    
    def FinalizeOutput(self):
        stnid='alldone '
        stnrec=struct.pack('8sfffii',stnid,0.0,0.0,0.0,0,0)
        for tp in self.subtype:
            self.outputPath[tp].write(stnrec)
            self.outputPath[tp].close()
            
        try:
            self.oInputPath.close()
        except:
            None
            
    def GenOutput(self,qcmeta):
        
        stns=qcmeta.keys()
        stns.sort()

        for stn in stns:
            basemeta = qcmeta[stn][0]
            self.CreateFiles(stn[1])
            self.WriteOutput(basemeta,stn)
       
        self.FinalizeOutput()
        
if(__name__ == '__main__'):

    satwinds = SatWinds('2009082906',13.0,-101.9)
    
    stime=time.time()
    (umeta) = satwinds.LoadDataAnnulus()
    mf.Timer('Read Cards and loaded data. ', stime)
    
    #stime=time.time()
    #(qcmeta) = satwinds.QualityControl(umeta)
    #mf.Timer('Quality Control. ', stime)
    
    stimer=time.time()    
    satwinds.GenOutput(umeta)
    mf.Timer('Finished creating obs files. ', stime)
    
    print 'The program has finished!'
