#!/usr/bin/env python


from tcbase import *

from M2 import setModel2


class globalHwrf(MFbase):
    
    sbdir='/pub/data/nccf/com/hur/prod'
    tbdir="%s/../w21/dat/nwp2/hwrf"%(w2.HfipProducts)
    w2tbdir="%s/../w21/dat/nwp2/w2flds/dat/hwrf"%(HfipProducts)
    
    # -- every 6 h
    #
    if(w2.onKishou):
        taumax=126
        tauinc=6
        taus=range(0,taumax+1,tauinc)
    
    # -- reduced ~ ukm2
    #
    else:
        taumax6=48
        tauinc6=6
        tauinc12=12
        taumax12=120
    
        taus=range(0,taumax6+1,tauinc6) + range((taumax6+tauinc12),taumax12+1,tauinc12)

    al='ftp'
    ap="""-michael.fiorino@noaa.gov"""
    af='ftpprd.ncep.noaa.gov'

    
    def __init__(self,dtg,tD=None,
                 reqtype='w2flds',
                 getStmids=None,
                 override=0):
        
        self.dtg=dtg
        self.reqtype=reqtype
        self.override=override
        self.getStmids=getStmids
        
        self.sdir="%s/hwrf.%s"%(self.sbdir,dtg)
        self.tdir="%s/%s"%(self.tbdir,dtg)
        self.tdirStatus=1
        if(MF.ChkDir(self.tdir) == 0):
            self.tdirStatus=0
            #MF.ChkDir(tdir,'mk')
        
        self.w2tdir="%s/%s"%(self.w2tbdir,dtg)
        MF.ChkDir(self.w2tdir,'mk')
        
        if(tD == None): tD=TcData(dtgopt=dtg)
        
        self.stmids=tD.getStmidDtg(dtg, dobt=0, dupchk=0, selectNN=1, verb=0)

        self.tD=tD
        if(self.tdirStatus == 0):
            return
        else:
            self.getStmidGlobal(dofdb=1)
            self.getFullDatPaths()

    
    
    def setMask(self,tau,hstmid=None,dofdb=0):
        
        if(hstmid != None):
            hmask="*%s*hwrfprs*global*f%03d.grb2"%(hstmid,tau)
            if(dofdb): hmask="fdb*%s*hwrfprs*global*f%03d*.txt"%(hstmid,tau)
        else:
            hmask="*hwrfprs*global*f%03d.grb2"%(tau)
            if(dofdb): hmask="fdb*hwrfprs*global*f%03d*.txt"%(tau)
        return(hmask)

        
    def wgetGlobal(self,ropt=''):
        
        wgetopt=" -nv -m -nd -T 30 -t 2"
        wgetopt=" -m -nd -T 30 -t 2"
            
        if(self.tdirStatus == 0):
            if(ropt == ''): MF.ChkDir(self.tdir,diropt='mk')
            
        MF.ChangeDir(self.tdir)
    
        gstmids=None
        
        if(self.getStmids != None): 
            if(self.getStmids == 'all'): gstmids=self.stmids  ; self.getStmids=self.stmids
            else:                        gstmids=self.getStmids
    
        MF.sTimer('wget-all')
    
        if(gstmids == None):
            
            for tau in self.taus:
                MF.sTimer('wget-%03d'%(tau))
                hmask=self.setMask(tau)
                cmd="wget %s \"ftp://%s/%s/%s\""%(wgetopt,self.af,self.sdir,hmask)
                mf.runcmd(cmd,ropt)
                MF.dTimer('wget-%03d'%(tau))
            
        else:
            
            for gstmid in gstmids:
                gstm3id=gstmid.split('.')[0].lower()
                for tau in self.taus:
                    MF.sTimer('wget-%03d'%(tau))
                    hmask=self.setMask(tau,hstmid=gstm3id)
                    cmd="wget %s \"ftp://%s/%s/%s\""%(wgetopt,self.af,self.sdir,hmask)
                    mf.runcmd(cmd,ropt)
                    MF.dTimer('wget-%03d'%(tau))
                
        if(ropt == 'norun'):
            rcFull=-1
            return(rcFull)
            
        # -- process the full files that came down
        #
        self.getStmidGlobal()
        self.getFullDatPaths()
        (rcFull,rcW2)=self.invFullW2flds(dow2=0)

        MF.dTimer('wget-all')
        
        return(rcFull)
                
                
    def getStmidGlobal(self,dofdb=0):
        
        taus=[0]
        
        for tau in taus:
            hmask=self.setMask(tau,dofdb=dofdb)
            hpaths=glob.glob("%s/%s"%(self.tdir,hmask))
            
            hwrfStmids=[]
            hwrfRealStmids={}
            hwrfStmidReals={}
            
            for hpath in hpaths:
                (ddir,dfile)=os.path.split(hpath)
                tt=dfile.split('.')
                hwrfStmid=tt[0]
                if(dofdb): hwrfStmid=tt[1]
                stm3id=hwrfStmid[-3:].upper()
                hwrfStmids.append(hwrfStmid)
                
                gotit=0
                for stmid in self.stmids:
                    s3id=stmid.split('.')[0].upper()
                    syear=stmid.split('.')[1]
                    b1id=s3id[-1]
                    s3id2=s3id
                    if(b1id == 'S'): 
                        s3id2=s3id[0:2] + 'P'
                        stmid22=s3id2 + '.' + syear
                    if(b1id == 'P'): 
                        s3id2=s3id[0:2]+'S'
                        stmid22=s3id2 + '.' + syear
                    
                    if(s3id == stm3id):
                        hwrfRealStmids[hwrfStmid]=stmid
                        hwrfStmidReals[stmid]=hwrfStmid
                        gotit=1
                    elif(s3id2 == stm3id):
                        hwrfRealStmids[hwrfStmid]=stmid22
                        hwrfStmidReals[stmid22]=hwrfStmid
                        gotit=1
                        
                if(gotit != 1):
                    'WWWW----no real storm for hwrf stmid: ',stm3id
                    
        self.hwrfStmids=hwrfStmids
        self.hwrfRealStmids=hwrfRealStmids
        self.hwrfStmidReals=hwrfStmidReals
                        
    def getFullDatPaths(self,dofdb=0):
        
        datpaths={}
        for hstmid in self.hwrfStmids:
            for tau in self.taus:
                hmask=self.setMask(tau,hstmid,dofdb=dofdb)
                hmask="%s/%s"%(self.tdir,hmask)
                dpaths=glob.glob(hmask)
                
                if(len(dpaths) == 1):
                    MF.appendDictList(datpaths,hstmid, dpaths[0])
                    
        self.datpaths=datpaths

    def killFullDatPaths(self,ropt=''):
        
        for hstmid in self.hwrfStmids:
            dpaths=self.datpaths[hstmid]
            for dpath in dpaths:
                cmd="rm %s"%(dpath)
                mf.runcmd(cmd,ropt)
            
    def tarballW2fields(self,ropt=''):
        
        MF.ChangeDir(self.w2tbdir,verb=1)
        cmd="tar -czvf hwrf-%s.tgz %s"%(self.dtg,self.dtg)
        mf.runcmd(cmd,ropt)
            
            
    def invFullW2flds(self,dow2=1,verb=1):
        
        rc=1
        frc=1
        chkstmids=self.hwrfStmids
        if(self.getStmids != None): 
            chkstmids=[]
            for gstmid in self.getStmids:
                chkstmids.append(self.hwrfStmidReals[gstmid])
        
        #print self.hwrfRealStmids
        #print chkstmids
        #for gstmid in chkstmids:
        #    print 'ggg',gstmid

        for hstmid in chkstmids:
            
            grb2sByTau={}
            taus=[]

            fdb2sByTau={}
            ftaus=[]

            if(dow2):
                grb2s=glob.glob("%s/%s/%s*grb2"%(self.w2tbdir,self.dtg,hstmid))
                fdb2s=[]
            else:
                grb2s=glob.glob("%s/%s/%s*grb2"%(self.tbdir,self.dtg,hstmid))
                fdb2s=glob.glob("%s/%s/fdb*%s*txt"%(self.tbdir,self.dtg,hstmid))
                
            for fdb2 in fdb2s:
                (fdif,ffile)=os.path.split(fdb2)
                tau=ffile.split('.')[-3][-3:]
                tau=int(tau)
                siz=MF.getPathSiz(fdb2)
                #print 'qqq',tau,siz,gfile
                fdb2sByTau[tau]=(siz,ffile)
                ftaus.append(tau)
                
            for grb2 in grb2s:
                (gdif,gfile)=os.path.split(grb2)
                tau=gfile.split('.')[-2][-3:]
                tau=int(tau)
                siz=MF.getPathSiz(grb2)
                #print 'qqq',tau,siz,gfile
                grb2sByTau[tau]=(siz,gfile)
                taus.append(tau)
                
            ftaus.sort()
            taus.sort()
            
            if(ftaus == self.taus):
                fstatus='fdb - got em all!'
            else:
                fstatus='fdb....incomplete....'
                frc=0
                
            # -- check taus
            #
            rcTau=1
            rcTauF=1
            for tau in taus:
                if(not(tau in self.taus)): 
                    print 'MMMissing in Full tau: ',tau
                    rcTau=0
                    break
                
            for tau in ftaus:
                if(not(tau in self.taus)): rcTauF=0
                
            print 'RRR',rcTau,' fff',rcTauF
            if(taus == self.taus): 
                status='got em all!'
            else:
                status='....incomplete....'
                rc=0
                
            if(dow2):
                print 'GGGRRRBBB222 -- HWRF run for stmid: ',hstmid,' dtg: ',self.dtg,' W2 status: ',status
            else:
                print 'HWRF run for stmid: ',hstmid,' dtg: ',self.dtg,' FULL status: ',status
                if(len(ftaus) != 0):
                    print 'FFFDDDBBB222 -- HWRF run for stmid: ',hstmid,' dtg: ',self.dtg,' FULL status: ',fstatus
                
            if(verb):
                
                if(len(taus) > 0):
                    ocard=''
                    for tau in taus:
                        rcg=grb2sByTau[tau]
                        ocard=ocard+' %03d:%8d '%(tau,rcg[0])
                        if(tau == 72): 
                            ocard=ocard+'\n'+' %03d:%8d '%(tau,rcg[0])
                    print ocard
                print
                    
                if(len(ftaus) > 0):
                    ocard=''
                    for tau in ftaus:
                        rcg=fdb2sByTau[tau]
                        ocard=ocard+' %03d:%8d '%(tau,rcg[0])
                        if(tau == 72): 
                            ocard=ocard+'\n'+' %03d:%8d '%(tau,rcg[0])
                    print ocard
                print
                
        return(rc,frc)
                    
                            
                
    def lsGlobal(self):
        
        self.getStmidGlobal(dofdb=0)
        
        print 'HWRF runs for dtg: ',self.dtg
        print
        hkeys=self.hwrfRealStmids.keys()
        
        for hstmid in self.hwrfStmids:
            rstmid='nada'
            if( hstmid in hkeys): rstmid=self.hwrfRealStmids[hstmid]
            print 'stmid: %-15s  real stmid: %-8s '%(hstmid,rstmid)
            
        print; print 'fffffuuuullllllll'
        (rcFull,rc)=self.invFullW2flds(dow2=0)
        print; print 'wwww22222fffff'
        (rcW2,rc)=self.invFullW2flds(dow2=1)
        print 'llll rcFull: ',rcFull,' rcW2: ',rcW2
        
            
    def doFullCtl(self):
        
        hkeys=self.hwrfRealStmids.keys()
        for hstmid in self.hwrfStmids:
            rstmid=None
            if( hstmid in hkeys): rstmid=self.hwrfRealStmids[hstmid]

            if(rstmid != None):
                self.makeFullCtl(hstmid,rstmid)
            
    def makeFullCtl(self,hstmid,stmid):
        
        dset="%s.%s.hwrfprs.global.0p25.f%%f3.grb2"%(hstmid,self.dtg)
        ctlfile="%s.%s.hwrf.ctl"%(stmid,self.dtg)
        ndxfile="%s.%s.hwrf.idx"%(stmid,self.dtg)
        gtime=mf.dtg2gtime(self.dtg)
        ginc="%dhr"%(self.tauinc)
        ctlpath="%s/%s"%(self.tdir,ctlfile)
        
        ctl="""dset ^%s
index ^%s
undef 9.999E+20
title wutip02w.2019022512.hwrfprs.global.0p25.f006.grb2
* produced by g2ctl v0.1.4
* command line options: wutip02w.2019022512.hwrfprs.global.0p25.f006.grb2
* griddef=1:0:(1440 x 721):grid_template=0:winds(N/S): lat-lon grid:(1440 x 721) units 1e-06 input WE:NS output WE:SN res 48 lat 90.000000 to -90.000000 by 0.250000 lon 0.000000 to 359.750000 by 0.250000 #points=1038240:winds(N/S)
dtype grib2
ydef  721 linear -90.0 0.25
xdef 1440 linear   0.0 0.25
tdef   21 linear %s %s
* PROFILE hPa
zdef 46 levels 100000 97500 95000 92500 90000 87500 85000 82500 80000 77500 75000 72500 70000 67500 65000 62500 60000 57500 55000 52500 50000 47500 45000 42500 40000 37500 35000 32500 30000 27500 25000 22500 20000 17500 15000 12500 10000 7500 7000 5000 3000 2000 1000 700 500 200
options pascals template
vars 68
ABSVprs    46,100  0,2,10 ** (1000 975 950 925 900.. 20 10 7 5 2) Absolute Vorticity [1/s]
prc   0,1,0   0,1,10,1 ** surface Convective Precipitation [kg/m^2]
pr   0,1,0   0,1,8,1 ** surface Total Precipitation [kg/m^2]
CAPEsfc   0,1,0   0,7,6 ** surface Convective Available Potential Energy [J/kg]
CD10m   0,103,10   0,2,196 ** 10 m above ground Drag Coefficient [non-dim]
CD30m   0,103,30   0,2,196 ** 30 m above ground Drag Coefficient [non-dim]
CH10m   0,103,10   10,3,203 ** 10 m above ground Heat Exchange Coefficient [-]
CICEprs    46,100  0,6,0 ** (1000 975 950 925 900.. 20 10 7 5 2) Cloud Ice [kg/m^2]
CINsfc   0,1,0   0,7,7 ** surface Convective Inhibition [J/kg]
CLWMRprs    46,100  0,1,22 ** (1000 975 950 925 900.. 20 10 7 5 2) Cloud Mixing Ratio [kg/kg]
DLWRFavesfc  0,1,0   0,5,192,0 ** surface Downward Long-Wave Rad. Flux [W/m^2]
DLWRFsfc  0,1,0   0,5,192 ** surface Downward Long-Wave Rad. Flux [W/m^2]
DPTprs    46,100  0,0,6 ** (850 700 500 300 200 100) Dew Point Temperature [K]
DPT2m   0,103,2   0,0,6 ** 2 m above ground Dew Point Temperature [K]
DSWRFavesfc  0,1,0   0,4,192,0 ** surface Downward Short-Wave Radiation Flux [W/m^2]
DSWRFsfc  0,1,0   0,4,192 ** surface Downward Short-Wave Radiation Flux [W/m^2]
ELONsfc   0,1,0   0,191,193 ** surface East Longitude (0 to 360) [deg]
HGTsfc   0,1,0   0,3,5 ** surface Geopotential Height [gpm]
zg    46,100  0,3,5 ** (1000 975 950 925 900.. 20 10 7 5 2) Geopotential Height [gpm]
HGTtrop   0,7,0   0,3,5 ** tropopause Geopotential Height [gpm]
HLCY3000_0m  0,103,3000,0   0,7,8 ** 3000-0 m above ground Storm Relative Helicity [m^2/s^2]
HPBLsfc   0,1,0   0,3,196 ** surface Planetary Boundary Layer Height [m]
LANDsfc   0,1,0   2,0,0 ** surface Land Cover (0=sea, 1=land) [Proportion]
LHTFLsfc   0,1,0   0,0,10 ** surface Latent Heat Net Flux [W/m^2]
prl       0,1,0   0,1,9,1 ** surface Large-Scale Precipitation (non-convective) [kg/m^2]
NLATsfc   0,1,0   0,191,192 ** surface Latitude (-90 to 90) [deg]
POTtrop   0,7,0   0,0,2 ** tropopause Potential Temperature [K]
prr   0,1,0   0,1,7 ** surface Precipitation Rate [kg/m^2/s]
PRESsfc   0,1,0   0,3,0 ** surface Pressure [Pa]
PREStrop   0,7,0   0,3,0 ** tropopause Pressure [Pa]
psl   0,101,0   0,3,1 ** mean sea level Pressure Reduced to MSL [Pa]
prw   0,200,0   0,1,3 ** entire atmosphere (considered as a single layer) Precipitable Water [kg/m^2]
REFCclm   0,200,0   0,16,196 ** entire atmosphere (considered as a single layer) Composite reflectivity [dB]
REFDprs    46,100  0,16,195 ** (1000 975 950 925 900.. 20 10 7 5 2) Reflectivity [dB]
hur    46,100  0,1,1 ** (1000 975 950 925 900.. 20 10 7 5 2) Relative Humidity [%%]
RH2m   0,103,2   0,1,1 ** 2 m above ground Relative Humidity [%%]
RIMEprs    46,100  0,1,203 ** (1000 975 950 925 900.. 20 10 7 5 2) Rime Factor [non-dim]
RWMRprs    46,100  0,1,24 ** (1000 975 950 925 900.. 20 10 7 5 2) Rain Mixing Ratio [kg/kg]
SFCRsfc   0,1,0   2,0,1 ** surface Surface Roughness [m]
SHTFLsfc   0,1,0   0,0,11 ** surface Sensible Heat Net Flux [W/m^2]
SNMRprs    46,100  0,1,25 ** (1000 975 950 925 900.. 20 10 7 5 2) Snow Mixing Ratio [kg/kg]
SPFHprs    46,100  0,1,0 ** (1000 975 950 925 900.. 20 10 7 5 2) Specific Humidity [kg/kg]
SPFH2m   0,103,2   0,1,0 ** 2 m above ground Specific Humidity [kg/kg]
TCOLCclm   0,200,0   0,6,198 ** entire atmosphere (considered as a single layer) Total Column-Integrated Condensate [kg/m^2]
TCOLIclm   0,200,0   0,6,197 ** entire atmosphere (considered as a single layer) Total Column-Integrated Cloud Ice [kg/m^2]
TCOLRclm   0,200,0   0,1,204 ** entire atmosphere (considered as a single layer) Total Column Integrated Rain [kg/m^2]
TCOLSclm   0,200,0   0,1,205 ** entire atmosphere (considered as a single layer) Total Column Integrated Snow [kg/m^2]
TCOLWclm   0,200,0   0,6,196 ** entire atmosphere (considered as a single layer) Total Column-Integrated Cloud Water [kg/m^2]
TCONDprs    46,100  0,6,195 ** (1000 975 950 925 900.. 20 10 7 5 2) Total Condensate [kg/kg]
TMPsfc   0,1,0   0,0,0 ** surface Temperature [K]
ta    46,100  0,0,0 ** (1000 975 950 925 900.. 20 10 7 5 2) Temperature [K]
tas   0,103,2   0,0,0 ** 2 m above ground Temperature [K]
TMPtrop   0,7,0   0,0,0 ** tropopause Temperature [K]
UFLXsfc   0,1,0   0,2,17 ** surface Momentum Flux, U-Component [N/m^2]
ua    46,100  0,2,2 ** (1000 975 950 925 900.. 20 10 7 5 2) U-Component of Wind [m/s]
uas   0,103,10   0,2,2 ** 10 m above ground U-Component of Wind [m/s]
UGRDtrop   0,7,0   0,2,2 ** tropopause U-Component of Wind [m/s]
ULWRFavesfc  0,1,0   0,5,193,0 ** surface Upward Long-Wave Rad. Flux [W/m^2]
ULWRFsfc  0,1,0   0,5,193 ** surface Upward Long-Wave Rad. Flux [W/m^2]
USWRFavesfc  0,1,0   0,4,193,0 ** surface Upward Short-Wave Radiation Flux [W/m^2]
USWRFsfc  0,1,0   0,4,193 ** surface Upward Short-Wave Radiation Flux [W/m^2]
VFLXsfc   0,1,0   0,2,18 ** surface Momentum Flux, V-Component [N/m^2]
va    46,100  0,2,3 ** (1000 975 950 925 900.. 20 10 7 5 2) V-Component of Wind [m/s]
vas   0,103,10   0,2,3 ** 10 m above ground V-Component of Wind [m/s]
VGRDtrop   0,7,0   0,2,3 ** tropopause V-Component of Wind [m/s]
VVELprs    46,100  0,2,8 ** (1000 975 950 925 900.. 20 10 7 5 2) Vertical Velocity (Pressure) [Pa/s]
VWSHtrop   0,7,0   0,2,192 ** tropopause Vertical Speed Shear [1/s]
sst  0,1,0   10,3,0 ** surface Water Temperature [K]
ENDVARS
"""%(dset,ndxfile,gtime,ginc,
   )
                

        MF.WriteString2File(ctl,ctlpath,verb=verb)

        cmd="gribmap -v -i %s"%(ctlpath)
        mf.runcmd(cmd,ropt)

    # wwwwwwwwwwwwwww222222222222222222222 filter
    #
    def doW2flds(self):
        
        for hstmid in self.hwrfStmids:
            
            dpaths=self.datpaths[hstmid]
            dpaths.sort()
            
            for dpath in dpaths:
                
                (ddir,dfile)=os.path.split(dpath)
                tau=dfile.split('.')[-2][-3:]
                tau=int(tau)

                fdbpath='%s/fdb.%s.txt'%(ddir,dfile)
                g2path="%s/%s.%s.%s.f%03d.grb2"%(self.w2tdir,hstmid,self.reqtype,self.dtg,tau)
                
                sizfdbpath=MF.getPathSiz(fdbpath)
                if(sizfdbpath <= 0 or self.override):
                    self.MakeFdb2(dpath,fdbpath,ropt='')

                sizg2path=MF.getPathSiz(g2path)
                
                if(sizg2path <= 0 or self.override):
                    
                    cards=self.GetFdb(fdbpath) 
                    (records,recsiz,nrectot)=self.ParseFdb2(cards)
                    request=self.SetFieldRequest2(tau)
                    orecs=self.Wgrib2VarFilter(records,request,tau,verb=1)
                    self.Wgrib2Filter(orecs,dpath,g2path,override=self.override)
                    
    
    def makeW2fldsCtl(self,ropt=''):
        
        
        gtime=mf.dtg2gtime(self.dtg)
        ginc="%dhr"%(self.tauinc)
        
        for hstmid in self.hwrfStmids:
            
            ctlpath="%s/%s.%s.%s.ctl"%(self.w2tdir,hstmid,self.reqtype,self.dtg)
            gmppath="%s/%s.%s.%s.grib2.gmp"%(self.w2tdir,hstmid,self.reqtype,self.dtg)
            (gdir,gmpfile)=os.path.split(gmppath)
            
            ctl="""dset ^%s.w2flds.%s.f%%f3.grb2
index ^%s
undef 9.999E+20
title invest95p.w2flds.2019022512.f000.grb2
* produced by g2ctl v0.1.4
* command line options: invest95p.w2flds.2019022512.f000.grb2
* griddef=1:0:(1440 x 721):grid_template=0:winds(N/S): lat-lon grid:(1440 x 721) units 1e-06 input WE:NS output WE:SN res 48 lat 90.000000 to -90.000000 by 0.250000 lon 0.000000 to 359.750000 by 0.250000 #points=1038240:winds(N/S)
dtype grib2
ydef  721 linear -90.0 0.25
xdef 1440 linear   0.0 0.25
tdef   21 linear %s %s
* PROFILE hPa
zdef 11 levels 100000 92500 85000 70000 50000 40000 30000 25000 20000 15000 10000
options pascals template
vars 14
prc    0,1,0    0,1,10,1 ** surface Convective Precipitation [kg/m^2]
pr     0,1,0    0,1,8,1 ** surface Total Precipitation [kg/m^2]
zg    11,100    0,3,5 ** (1000 925 850 700 500.. 300 250 200 150 100) Geopotential Height [gpm]
prr    0,1,0    0,1,7 ** surface Precipitation Rate [kg/m^2/s]
psl    0,101,0  0,3,1 ** mean sea level Pressure Reduced to MSL [Pa]
prw    0,200,0  0,1,3 ** entire atmosphere (considered as a single layer) Precipitable Water [kg/m^2]
hur   11,100    0,1,1 ** (1000 925 850 700 500.. 300 250 200 150 100) Relative Humidity [%%]
tss    0,1,0    0,0,0 ** surface Temperature [K]
ta    11,100    0,0,0 ** (1000 925 850 700 500.. 300 250 200 150 100) Temperature [K]
tas    0,103,2  0,0,0 ** 2 m above ground Temperature [K]
ua    11,100    0,2,2 ** (1000 925 850 700 500.. 300 250 200 150 100) U-Component of Wind [m/s]
uas    0,103,10 0,2,2 ** 10 m above ground U-Component of Wind [m/s]
va    11,100    0,2,3 ** (1000 925 850 700 500.. 300 250 200 150 100) V-Component of Wind [m/s]
vas    0,103,10 0,2,3 ** 10 m above ground V-Component of Wind [m/s]
ENDVARS
"""%(hstmid,self.dtg,
     gmpfile,
     gtime,ginc)
            
            MF.WriteCtl(ctl, ctlpath)
            cmd="gribmap -v -i %s"%(ctlpath)
            mf.runcmd(cmd,ropt)
           
                
        
        

    #--------------------------------- wgrib.filter.py defs -----------------------------

    def MakeFdb2(self,datpath,fdbpath,ropt=''):
    
        F=open(fdbpath,'w')
        F.writelines(datpath+'\n')
        F.close()
    
        if(os.path.exists(datpath)):
            cmd="wgrib2 -v2 %s >> %s"%(datpath,fdbpath)
            mf.runcmd(cmd,ropt)
        else:
            print 'WWW no data for fdb2 datpath: ',datpath
        
    
    
    def GetFdb(self,fdbpath):
        F=open(fdbpath)
        cards=F.readlines()
        F.close()
        return(cards)
    
    
    
    def LevCode2Lev2(self,lc1,lv1,lc2,lv2):
        levc=None
        if(lc1== 100):
            ld='mb'
            lv=lv1
            levc="%d.%g"%(lc1,lv1)
        elif(lc1== 1):
            ld='surface'
            lv=lv1
            levc="%d.%g"%(lc1,lv1)
        elif(lc1== 4):
            ld='OC istotherm'
            lv=lv1
            levc="%d.%g"%(lc1,lv1)
        elif(lc1== 6):
            ld='max wind'
            lv=lv1
            levc="%d.%g"%(lc1,lv1)
        elif(lc1== 7):
            ld='tropopause'
            lv=lv1
            levc="%d.%g"%(lc1,lv1)
        elif(lc1== 8):
            ld='top of atmosphere'
            lv=lv1
            levc="%d.%g"%(lc1,lv1)
        elif(lc1== 10):
            ld='entire atmosphere'
            lv=lv1
            levc="%d.%g"%(lc1,lv1)
        elif(lc1== 101):
            ld='mean sea level'
            lv=lv1
            levc="%d.%g"%(lc1,lv1)
        elif(lc1== 102):
            ld='m above mean sea level'
            lv=lv1
            levc="%d.%g"%(lc1,lv1)
        elif(lc1== 103):
            ld='m above ground'
            lv=lv1
            levc="%d.%g"%(lc1,lv1)
        elif(lc1== 104):
            ld='sigma layer'
            lv=lv1
            levc="%d.%g-%g"%(lc1,lv1,lv2)
        elif(lc1== 106):
            ld='m below ground (layer)'
            lv=lv1
            levc="%d.%d-%-d"%(lc1,int(lv1*0.01),int(lv2*0.01))
        elif(lc1== 108 and lc2 == 108):
            ld='mb layer above ground (layer)'
            lv=lv1
            levc="%d.%d-%-d"%(lc1,int(lv1*0.01),int(lv2*0.01))
        elif(lc1== 109):
            ld='reserved'
            lv=lv1
            levc="%d.%g"%(lc1,lv1)
        elif(lc1== 244):
            ld='depth of atmos'
            lv=lv1
            levc="%d.%g"%(lc1,lv1)
        elif(lc1== 234):
            ld='high cloud layer'
            lv=lv1
            levc="%d.%g"%(lc1,lv1)
        elif(lc1== 224):
            ld='mid cloud layer'
            lv=lv1
            levc="%d.%g"%(lc1,lv1)
        elif(lc1== 214):
            ld='low cloud layer'
            lv=lv1
            levc="%d.%g"%(lc1,lv1)
        elif(lc1== 211):
            ld='total cloud layer'
            lv=lv1
            levc="%d.%g"%(lc1,lv1)
        elif(
            lc1 == 242 or lc1 == 243 or
            lc1 == 232 or lc1 == 233 or
            lc1 == 222 or lc1 == 223 or
            lc1 == 212 or lc1 == 213 or
            lc1 == 200 or
            lc1 == 204
            ):
            ld='NCEP level type %d'%(lc1)
            lv=float(lc1)
            levc="%d.%g"%(lc1,lv1)
        elif(
            lc1 == 220
            ):
            ld='NCEP PBL height %d'%(lc1)
            lv=float(lc1)
            levc="%d.%g"%(lc1,lv1)
        else:
            ld=None
            lv=None
            print 'WWW(LevCode2Lev2.grib2) not defined lc1: ',lc1,lv1,lc2,lv2
            
        return(lv,ld,levc)
    
    
    def ParseFdb2(self,cards,verb=0):
    
    
        def splitlevcodes(lvl):
            tt=lvl.split('=')
            lll=tt[1].split(',')
            lc=int(lll[0][1:])
            ll2=lll[1][:-1]
            if(lc == 255 or lc == 109 or lc == 104 or lc == 106  or lc == 108):
                if(ll2 == 'missing'):
                    ll=-999.
                else:
                    ll=float(ll2)
            elif(lc == 100):
                ll=float(ll2)*0.01
            #
            # new parameter from ncep for gfs when lc=103 changes on 2009121512
            #
            elif(lc == 103):
                if(ll2 == 'missing'):
                    ll=-999.
                else:
                    ll=float(ll2)
            elif(lc == 255):
                ll=-999.
            else:
                ll=float(ll2)
            return(lc,ll)
            
            
        ncards=len(cards)
    
        recsiz={}
        records={}
    
        #
        # the first card has the data path
        #
    
        nrec=0
        nc=1
        for nr in range(nc,ncards):
    
            card=cards[nr]
            tt=card.split(':')
    
            recnum=tt[0]
            sizrecp1=int(tt[1])
    
    ##        ['1', '0', '00Z07jun2007', 'HGT Geopotential Height [gpm]', 'lvl1=(100,100000) lvl2=(255,0)', '1000 mb', 'anl', '\n']
    
            var=tt[3].split()[0]
            vardesc=''
            for vt in tt[3].split()[1:]:
                vardesc="%s %s"%(vardesc,vt)
            vardesc=vardesc.lstrip()
    
            tt4=tt[4].split()
            if(len(tt4) == 4):
                lvl1=tt4[2]
                lvl2=tt4[3]
            else:
                lvl1=tt4[0]
                lvl2=tt4[1]
    
            (levcode1,lev1)=splitlevcodes(lvl1)
            (levcode2,lev2)=splitlevcodes(lvl2)
    
            (lev,levd,levc)=self.LevCode2Lev2(levcode1,lev1,levcode2,lev2)
    
            levdesc=tt[5]
            levdesc=levd
            timedesc=tt[6]
    
            rec=(
                recnum,
                sizrecp1,
                var,
                vardesc,
                lev,
                levc,
                levcode1,
                lev1,
                levcode2,
                lev2,
                levdesc,
                timedesc,
                )
    
            #print '--------- ',nrec,recnum,var,vardesc,levcode1,lev1,levcode2,lev2,levdesc,levc
            
            records[nrec]=rec
            recsiz[nrec]=sizrecp1
            nrec=nrec+1
    
        nrectot=ncards
    
        return(records,recsiz,nrectot)
    
    def SetFieldRequest2(self,tau,model='hwrf'):
    
        request={}
    
        mplevs=[1000,925,850,700,500,400,300,250,200,150,100]
        uvplevs=mplevs
        zplevs=mplevs
        tplevs=mplevs
        rhplevs=mplevs
                
            
        # sfc + ua versions
        #
        request['ugrd']=['103.10']
        request['vgrd']=['103.10']
    
        request['tmax']=['103.2']
        request['tmin']=['103.2']
        
        request['hgt']=[]
        request['tmp']=['103.2']
        request['rh']=[]
        
        
        for plev in uvplevs:
            request['ugrd']=request['ugrd']+ ['100.%d'%(plev)]
            request['vgrd']=request['vgrd']+ ['100.%d'%(plev)]
        
        for plev in zplevs:
            request['hgt']=request['hgt']+ ['100.%d'%(plev)]
    
        for plev in tplevs:
            request['tmp']=request['tmp']+ ['100.%d'%(plev)]
    
        if(len(rhplevs) > 0):
            for plev in rhplevs:
                request['rh']=request['rh']+ ['100.%d'%(plev)]
    
    
        request['ugrd']=request['ugrd']+ ['1.0']
        request['vgrd']=request['vgrd']+ ['1.0']
        request['tmax']=request['tmax']+['1.0']
        request['tmin']=request['tmin']+['1.0']
        request['tmp']=request['tmp']+['1.0']
        
        # -- 20180717 -- latest UPP from ncep only outputs MSLET - slp using eta reduction
        #
        if(model == 'fv3e' or model == 'fv3g' or model == 'fv7e' or model == 'fv7g'):
            request['mslet']=['101.0']
            request['mslet']=request['mslet']+['3.192']
        else:
            request['prmsl']=['101.0']
            request['prmsl']=request['prmsl']+['1.0']
            
        request['prate']=['1.0']
        request['cprat']=['1.0']
        request['pwat']=['200.0']
        request['apcp']=['1.0']
        request['acpcp']=['1.0']
        
        request['taus']=[tau]
    
        return(request)
    
    
    def Wgrib2VarFilter(self,records,request,tau,verb=0):
    
        nr=len(records)
    
        rtaus=request['taus']
        rtaus.sort()
        rvars=request.keys()
        rvars.sort()
    
       
        orecs=[]
    
        nrecs=records.keys()
        nrecs.sort()
        
        for nrec in nrecs:
            
    
            (
                recnum,
                sizrecp1,
                var,
                vardesc,
                lev,
                levc,
                levcode1,
                lev1,
                levcode2,
                lev2,
                levdesc,
                timedesc,
                )=records[nrec]
        
    
            var=var.lower()
    
    
            for rvar in rvars:
                if(var == rvar):
                    rlevs=request[rvar]
                    for rlev in rlevs:
                        if(levc == rlev):
                            for rtau in rtaus:
                                if(rtau == tau):
                                    if(verb): print 'MMMMMMMMMMMMM(Wgrib2VarFilter): ',	var,lev,tau,nrec,sizrecp1
                                    ocard="%s:%d"%(recnum,sizrecp1)
                                    ocard=ocard+'\n'
                                    orecs.append(ocard)
    
    
        return(orecs)
    
    
    def Wgrib2VarAnal(self,records,tau):
    
        nr=len(records)
    
        vars=[]
        taus=[]
        levs=[]
        levds={}
        
        vardescs={}
        varlevs={}
        varcodes={}
    
        for n in range(0,nr):
            
            (
                recnum,
                sizrecp1,
                var,
                vardesc,
                lev,
                levc,
                levcode1,
                lev1,
                levcode2,
                lev2,
                levdesc,
                timedesc,
                )=records[n]
        
    
            var=var.lower()
            vars.append(var)
            taus.append(tau)
            levs.append(levc)
            
            try:
                varlevs[levc,tau].append(var)
            except:
                varlevs[levc,tau]=[var]
    
            try:
                vardescs[var,tau].append(vardesc)
            except:
                vardescs[var,tau]=[vardesc]
    
            levds[levc]=levdesc
    
            try:
                varcodes[var].append(var)
            except:
                varcodes[var]=[var]
    
        vars=mf.uniq(vars)
        taus=mf.uniq(taus)
        levs=mf.uniq(levs)
        levs.sort()
    
        levsnp=[]
        levsp=[]
    
        for lev in levs:
            lc=lev.split('.')[0]
            if(lc == '100'):
                lv=lev.split('.')[1]
                levsp.append(int(lv))
            else:
                levsnp.append(lev)
    
    
        levsnp.sort()
        
        levs=[]
        for ll in levsnp:
            levs.append(ll)
    
        levsp.sort()
        for ll in levsp:
            levs.append("100.%d"%(ll))
                        
    
        print
        print "Var Inventory by Lev for Tau: ",tau
        print
        for tau in taus:
            for lev in levs:
                vcard="%-15s "%(lev)
                try:
                    lvars=varlevs[lev,tau]
                    lvars.sort()
                    nlvars=len(lvars)
                    for nlvar in range(0,nlvars):
                        lvar=lvars[nlvar]
                        vcard="%s %-6s"%(vcard,lvar)
                        if(nlvar > 0 and nlvar%12 == 0):
                            vcard=vcard+'\n '+15*' '
                except:
                    vcard=vcard
    
                if(nlvars > 12):    print 
                print vcard
                if(nlvars > 12):    print 
    
            print
            print "Var desc:"
            print
            vars.sort()
            for var in vars:
                vv=vardescs[var,tau]
                vv=mf.uniq(vv)
                vc=varcodes[var]
                print "%-6s %6s  %s"%(var,vc[0],vv[0][:-1])
    
    
            print
            print "Lev desc:"
            print
            for lev in levs:
                print "%-15s  %s"%(lev,levds[lev])
    
    
    def Wgrib2Filter(self,orecs,inpath,outpath,override=0):
    
        if(os.path.exists(outpath) and override == 0):
            return
    
        if(not(os.path.exists(inpath))):
            print 'WWW wgrib2filter inpath: ',inpath,' does not exist, returning'
            return
        
        wcmd="wgrib2 -i %s -grib %s"%(inpath,outpath)
        print wcmd
    
        w=os.popen(wcmd,'w')
        w.writelines(orecs)
        w.close()
        
    def IsGrib1(self,gribtype):
        rc=0
        if(gribtype == 'grb1'):
            rc=1
        return(rc)
    
    def IsGrib2(self,gribtype):
        rc=0
        if(gribtype == 'grb2'):
            rc=1
        return(rc)
        
    
#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# command line setup
#
class WgetCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv
        
        self.argv=argv
        self.argopts={
            1:['dtgopt',    'no default'],
            }

        self.options={
            'override':   ['O',0,1,'override'],
            'verb':       ['V',0,1,'verb=1 is verbose'],
            'ropt':       ['N','','norun',' norun is norun'],
            'dowget':     ['W',1,0,'do NOT dowget'],
            'dols':       ['l',0,1,' just list'],
            'doW2flds':   ['2',0,1,' make full ctl'],
            'doClean':    ['K',0,1,' kill full files'],
            'stmopt':     ['S:',None,'a',' select storms -- do md2a -d dtgopt to select storm...'],
            }

        self.purpose='''
purpose -- wget mirror gfs stb (sat brightness t) goes images
%s cur
'''
        self.examples='''
%s cur
'''

#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# main            hmask="*hwrfprs*global*f%03d.grb2"%(tau)
#

MF.sTimer(tag='wget.hwrf')

argv=sys.argv
CL=WgetCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

dtgs=mf.dtg_dtgopt_prc(dtgopt,ddtg=6)

if(dols): dowget=0
if(doClean): dowget=0; doW2flds=0

tD=TcData(dtgopt=dtgopt)
for dtg in dtgs:

    getStmids=None
    if(stmopt != None):
        if(mf.find(stmopt,'all')):  getStmids='all'
        else:                       getStmids=MakeStmList(stmopt)
        
    gH=globalHwrf(dtg,override=override,
                  getStmids=getStmids,
                  )
    
    if(dowget or gH.tdirStatus == 0): 
        rcFull=gH.wgetGlobal(ropt=ropt)
        if(rcFull == 1 and ropt != 'norun'):
            gH.doFullCtl()
        else:
            print 'WWW did not wget full set of taus for dtg: ',dtg,' ropt: ',ropt
            sys.exit()

    if(ropt == 'norun'):
        print 'ropt: norun continue...'
        continue
    
    gH.getStmidGlobal()
    gH.getFullDatPaths()

    # -- just ls
    #
    if(dols): 
        gH.lsGlobal()
        continue
    
    # -- make w2flds
    #
    if(doW2flds):
        (rc,frc)=gH.invFullW2flds(dow2=0)
        print 'rrrrrrrrrrrrrrrrrr',rc,frc

        if(rc == 0 and frc == 0 and not(override)):
            print 'full not yet complete...and w2flds not yet done..bail...'
            sys.exit()
        elif(rc == 0 and frc):
            print 'IIIII WW22FFLLDDSS complete!'
            sys.exit()
            
        gH.doW2flds()
        gH.makeW2fldsCtl()
    
        (rc,frc)=gH.invFullW2flds(dow2=0)
        print 'rrrr',rc,'ffff',frc
        (rcW2,frcW2)=gH.invFullW2flds(dow2=1)
        print 'rrrr',rc,'ffff',frc,' 2222 ',rcW2,frcW2
        if(rc or override):
            gH.killFullDatPaths(ropt=ropt)
        
        # -- now make the tarball
        #
        gH.tarballW2fields()
            
            

     

MF.dTimer(tag='wget.hwrf')

