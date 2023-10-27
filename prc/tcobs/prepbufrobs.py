from TC import *


class SatWindsObs(MFbase):
 
    
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
    
    VarsSfc = ['pso','psf','st']
    
    VarDescSfc={
             'pso':'obs ps',
             'psf':'fct ps',
             'st':'Data Subtype'
            }
    VarUnitsSfc={
              'pso':'[mb]',
              'psf':'[mb]',
              'st':'[#]'
             }

    
    Inc = 1

    R1 = 60.0

    R2 = 180.0
    
    deltaR = 60.0
    
    #subtype = []


    def __init__(self,inputdir,basedir,dtg,cLat,cLon,stmid):
        
        self.Inputdir = inputdir
        self.Basedir = basedir        
        
        
        if(cLon<0.0):
            cLon=360.0+cLon
        else:
            None

        self.centerLat = cLat
        self.centerLon = cLon
        self.dtg = dtg

        self.stmid=stmid.split('.')[0].upper()
        
        self.subtype = []
        self.ctlpaths=[]
        self.outputPath = {}

        __uInputPath = '%s/obs.u.%s.%s.txt'%(self.Inputdir,dtg,self.stmid)
        __vInputPath = '%s/obs.v.%s.%s.txt'%(self.Inputdir,dtg,self.stmid)
        __psInputPath = '%s/obs.ps.%s.%s.txt'%(self.Inputdir,dtg,self.stmid)
        
        try:
            self.uInputPath = open(__uInputPath)
            self.vInputPath = open(__vInputPath)
            self.psInputPath = open(__psInputPath)
        except:
            raise IOError('Unable to open: %s or %s'%(__uInputPath,__vInputPath))
        
        
    def CreateFiles(self,subtype):
        
        try:
            self.subtype.index(subtype)
            None
        except:
            self.subtype.append(subtype)
        
            __outputPath = '%s/obs.%s.%s.%03d.obs'%(self.Basedir,self.dtg,self.stmid,subtype)
            __ctlPath    = '%s/obs.%s.%s.%03d.ctl'%(self.Basedir,self.dtg,self.stmid,subtype)
            __smpPath    = '%s/obs.%s.%s.%03d.smp'%(self.Basedir,self.dtg,self.stmid,subtype)

            self.ctlpaths.append(__ctlPath)
                
            try:
                self.outputPath[subtype]=open(__outputPath,'wb')
                self.CtlFile(__ctlPath,__smpPath,__outputPath,self.dtg,subtype)
            except:
                raise IOError('Unable to open: %s'(__outputPath))



    def CtlFile(self,ctlPath,smpPath,outPath,dtg,subtype):
        try:
            oCtlPath = open(ctlPath,'w')
        except:
            raise IOError('Unable to open: %s'(ctlPath))
        
        (dir,outFile) = os.path.split(outPath)
        (dir,sFile) = os.path.split(smpPath)

        gtime=mf.dtg2gtime(dtg)
        
        vars=[]

        if(subtype >= 202 and subtype <= 291):
            for v in self.Vars:
                desc='%s %s'%(self.VarDesc[v],self.VarUnits[v])
                vars.append('%-7s 1 99 %s'%(v,desc))
                
        elif(subtype >= 102 and subtype <= 191):
            for v in self.VarsSfc:
                desc='%s %s'%(self.VarDescSfc[v],self.VarUnitsSfc[v])
                vars.append('%-7s 0 99 %s'%(v,desc))
            
 
                
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
        psCards=self.psInputPath.readlines()
        return(uCards,vCards,psCards)
    
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

        (uCards,vCards,psCards) = self.ReadCards()

        umeta = {}
        psmeta = {}
        

        ndata=21
        ndata=19
        if (len(uCards) == len(vCards)):
            for inc in range(ndata,len(uCards)):
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

        if (len(psCards) > 0):
            for inc in range(ndata,len(psCards)):
                (ostnid,metaPS)=self.ParseCards(psCards[inc],0)
                                            
                lat = metaPS[0]
                lon = metaPS[1]
                
                psob = metaPS[4]
                psfc = metaPS[5]
                prs = metaPS[2]
                subtype = metaPS[6]
                    
                meta = (lat,lon,prs,psob,psfc,subtype)
                try:
                    psmeta[ostnid,subtype].append(meta)
                except:
                    psmeta[ostnid,subtype]=[]
                    psmeta[ostnid,subtype].append(meta)
                    
        else:
            print 'Error: Data does not match in data file.'
        
        return(umeta,psmeta)
       
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
        
        #if ( typ == 245.0 ): print 'stnhead',typ, stnid,lat,lon,stndt
        #if ( typ == 245.0 ): print 'stnrec', prs,uob,ufc,vob,vfc,sbt
        
        self.outputPath[typ].write(stnhead)
        
        self.outputPath[typ].write(stnrec)

    
    def WriteSfcOutput(self,basemeta,stn):
        
        stnid = stn[0]
        typ = stn[1]
        stndt = 0.0
        
        lat=basemeta[0]
        lon=basemeta[1]
        prs=basemeta[2]
        psob=basemeta[3]
        psfc=basemeta[4]
        sbt=basemeta[5]
        
        if(lon<0.0):
            rlon=360.0+lon
        else:
            rlon=lon

        rlat=lat  
            
        stnhead = struct.pack('8sfffii',stnid,lat,lon,stndt,1,1)
            
        stnrec = struct.pack('%df'%3,psob,psfc,sbt)
        
        #if ( typ == 245.0 ): print 'stnhead',typ, stnid,lat,lon,stndt
        #if ( typ == 245.0 ): print 'stnrec', prs,uob,ufc,vob,vfc,sbt
        
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
            
    def GenOutput(self,qcmeta,psmeta,doua=1,dosfc=1):


        if(doua):
            stns=qcmeta.keys()
            stns.sort()

            for stn in stns:
                basemeta = qcmeta[stn][0]
                self.CreateFiles(stn[1])
                self.WriteOutput(basemeta,stn)

        if(dosfc):
            stns=psmeta.keys()
            stns.sort()

            for stn in stns:
                basemeta = psmeta[stn][0]
                self.CreateFiles(stn[1])
                self.WriteSfcOutput(basemeta,stn)
       

        self.FinalizeOutput()

    def makeStnmap(self,ropt='',verb=''):

        for ctlpath in self.ctlpaths:
            cmd="stnmap %s -i %s"%(verb,ctlpath)
            mf.runcmd(cmd,ropt)

            
        
    def RunProgram(self):
        stime=time.time()
        (umeta,psmeta) = self.LoadDataAnnulus()
        mf.Timer('Read Cards and loaded data. ', stime)

        stimer=time.time()    
        self.GenOutput(umeta,psmeta)
        mf.Timer('Finished creating obs files. ', stime)
        
        return(self.subtype)
        
        
if(__name__ == '__main__'):


    bufrdir='/lfs1/projects/fim/fiorino/w21/dat/tc/obs/gfsenkf_diag'
    bufrdir='/lfs1/projects/fim/fiorino/w21/dat/tc/obs/gfsenkf_cira_irwd_diag'
    bufrdir='/lfs1/projects/fim/fiorino/w21/dat/tc/obs/gfsenkf_control_diag'
    dtg='2010062000'
    dtg='2010062512'
    stmid='04e.2010'

    tcD=TcData()
    (stmids,btcs)=tcD.getDtg(dtg,dupchk=1)

    (lat,lon,vmax,pmin,r34)=btcs[stmid.upper()]
    
    cOB=SatWindsObs(bufrdir,bufrdir,dtg,lat,lon,stmid)
    cOB.RunProgram()
    cOB.makeStnmap()
    

    #satwinds = SatWinds('2009082906',13.0,-101.9)
    
    #stime=time.time()
    #(umeta) = satwinds.LoadDataAnnulus()
    #mf.Timer('Read Cards and loaded data. ', stime)
    
    #stime=time.time()
    #(qcmeta) = satwinds.QualityControl(umeta)
    #mf.Timer('Quality Control. ', stime)
    
    #stimer=time.time()    
    #satwinds.GenOutput(umeta)
    #mf.Timer('Finished creating obs files. ', stime)
    
    #print 'The program has finished!'
