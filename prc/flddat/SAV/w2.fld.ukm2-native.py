#!/usr/bin/env python

from WxMAP2 import *
w2=W2()

from GRIB import Grib1,Grib2

class ukmNative(Grib1):

    xwgrib='wgrib'
    latsCmd='w2.fld.ukm2lats.gs'
    
    model='ukm2'
    sdir='/public/data/grids/ukmet'
    prcdir=w2.PrcDirFlddatW2
    ptable="%s/../hfip/lats.hfip.table.txt"%(prcdir)

    def __init__(self,dtg,
                 ropt='',
                 override=0,
                 verb=0):

        from M2 import setModel2
        
        def makeCard(nrec,W):
            ocard="%d:%d:%03d:%s:%d:%d:%d:%f"%(nrec,W.sizrecp1,W.tau,W.var,W.lev,W.ndef,W.nundef,W.gridvalmin)
            ocard=ocard+'\n'
            return(ocard)


        m2=setModel2(self.model)

        self.dtg=dtg
        self.verb=verb
        self.fm=m2.DataPath(dtg,dtype='w2flds',dowgribinv=1,verb=verb)
        self.fstatuss=self.fm.statuss[dtg]
        
        (tdir,tbase)=os.path.split(m2.tdatbase)
        MF.ChkDir(tdir,'mk')
        
        tmpdir="%s/tmp"%(tdir)
        MF.ChkDir(tmpdir,'mk')
        
        taus=[]
        grib1s=glob.glob("%s/%s_???_meto.grib"%(self.sdir,dtg))
        grib1s.sort()

        # -- counter for tau prcoessed
        #
        self.ntauPrc=0
        
        for grbpath in grib1s:

            (ddir,dfile)=os.path.split(grbpath)
            tau=dfile.split("_")[1]
            self.tau=tau

            itau=int(tau)
            
            if(len(self.fstatuss.keys()) > 0):
                try:
                    nftau=self.fstatuss[itau][1]
                except:
                    nftau=-1
            else:
                nftau=-1

            # -- bypass if already done...
            #
            if(nftau > 0 and not(override)): 
                print 'III(%s) already processed tau: %03d ... press ...'%(CL.pyfile,itau)
                continue
            
            self.ntauPrc=self.ntauPrc+1
            
            (dbase,dext)=os.path.splitext(dfile)
            fdbpath="%s/%s.wgrib1.txt"%(tmpdir,dbase)

            ogrbpathW="%s/wind.%s.f%s.grb1"%(tmpdir,dtg,tau)
            ogrbpathM="%s/mass.%s.f%s.grb1"%(tmpdir,dtg,tau)
            octlpathW="%s/wind.%s.f%s.ctl"%(tmpdir,dtg,tau)
            octlpathM="%s/mass.%s.f%s.ctl"%(tmpdir,dtg,tau)
            ofdbpathW="%s/wind.%s.f%s.wgrib1.txt"%(tmpdir,dtg,tau)
            ofdbpathM="%s/mass.%s.f%s.wgrib1.txt"%(tmpdir,dtg,tau)
            
            ogrbpathA="%s/wind-mass.%s.f%s"%(tmpdir,dtg,tau)
            fgrbpath="%s.f%s.grb1"%(m2.tdatbase,tau)

            MF.sTimer('grib1Inv')
            print 'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWorking tau: ',tau,' grbpath: ',grbpath

            if( (override or not(MF.ChkPath(fdbpath))) and MF.ChkPath(grbpath) ):
                F=open(fdbpath,'w')
                F.writelines(grbpath+'\n')
                F.close()
                cmd="%s -V %s >> %s"%(self.xwgrib,grbpath,fdbpath)
                mf.runcmd(cmd,'')
            MF.dTimer('grib1Inv')

            if(override or not(MF.ChkPath(ogrbpathW) and MF.ChkPath(ogrbpathM))):

                (recs,recsiz,nrectot)=self.ParseFdb1(open(fdbpath).readlines())
                orecsW=[]
                orecsM=[]
                recsW={}
                recsM={}
                for nrec in range(1,nrectot+1):
                    W=recs[nrec]
                    if(W.ny == 1152): recsM[nrec]=recs[nrec]
                    else:              recsW[nrec]=recs[nrec]

                for k in recsM.keys():
                    M=recsM[k]
                    if(verb): print 'mmm:',k,M.ny,M.varcode
                    ocard=makeCard(k,M)
                    orecsM.append(ocard)

                for k in recsW.keys():
                    W=recsW[k]
                    if(verb): print 'www:',k,W.ny,W.varcode
                    ocard=makeCard(k,W)
                    orecsW.append(ocard)

                self.Wgrib1Filter(orecsW,grbpath,ogrbpathW)
                self.Wgrib1Filter(orecsM,grbpath,ogrbpathM)

            self.makeCtl(ogrbpathW,octlpathW)
            self.makeCtl(ogrbpathM,octlpathM)
            
            self.destaggerMass2Wind(octlpathM, octlpathW, ogrbpathA)
            
            # -- mv output to w2flds location
            #
            cmd="mv %s.grb %s"%(ogrbpathA,fgrbpath)
            mf.runcmd(cmd,ropt)
            
            # -- clean tmp dir
            #
            cmd="rm %s/*.grb*"%(tmpdir)
            mf.runcmd(cmd,ropt)
            
            cmd="rm %s/*.ctl*"%(tmpdir)
            mf.runcmd(cmd,ropt)
            
        self.doGribmap()
        

    def makeCtl(self,grbpath,ctlpath,
                dtau=6,
                verb=0,
                ropt=''):
        
        itau=int(self.tau)
        (gdir,gfile)=os.path.split(grbpath)
        nt=(itau/dtau) + 1
        gtime=mf.dtg2gtime(self.dtg)
        
        if(mf.find(ctlpath,'wind')):
            
            ctl="""dset ^%s
index ^%s.idx
undef 9.999E+20
title wind.2017031300_000_meto.grib
*  produced by grib2ctl v0.9.12.5p16
dtype grib 255
ydef 1153 linear -90.0 0.15625
xdef 1536 linear   0.0 0.234375 
tdef %d linear %s 6hr
zdef 7 levels
1000 925 850 700 500 300 200 
vars 4
ua   7 201,100,0 ** u wind
va   7 202,100,0 ** v wind
uas  0 225,105,9999  ** u sfc wind
vas  0 226,105,9999  ** v sfc wind
ENDVARS"""%(gfile,gfile,nt,gtime)
            
        elif(mf.find(ctlpath,'mass')):
            
            ctl="""dset ^%s
index ^%s.idx
undef 9.999E+20
title mass.2017031300_000_meto.grib
*  produced by grib2ctl v0.9.12.5p16
dtype grib 255
ydef 1152 linear -89.922 0.15625
xdef 1536 linear   0.117 0.234375
tdef %d linear %s 6hr
zdef 7 levels
1000 925 850 700 500 300 200 
vars 7
psl      0 222,102,0  ** slp
pr       0 226,1,0  ** total precip
prc      0 201,1,0  ** convective precip
tas      0 236,105,9999  ** sfc air T
zg       7 202,100,0 ** Z
ta       7 203,100,0 ** T
hur      7 234,100,0 ** RH
ENDVARS"""%(gfile,gfile,nt,gtime)         
            
        MF.WriteCtl(ctl,ctlpath)
        vopt=''
        if(self.verb): vopt='-v'
        cmd="gribmap %s -i %s"%(vopt,ctlpath)
        mf.runcmd(cmd,ropt)
        

    def makeCtl2(self,grbpath,ctlpath,
                dtau=6,
                verb=0,
                ropt=''):
        
        """ grib2 version
"""
        itau=int(self.tau)
        (gdir,gfile)=os.path.split(grbpath)
        nt=(itau/dtau) + 1
        gtime=mf.dtg2gtime(self.dtg)
        
        if(mf.find(ctlpath,'wind')):
            
            ctl="""dset ^%s
index ^%s.idx
undef 9.999E+20
title wind.2017031300_000_meto.grib2
*  produced by grib2ctl v0.9.12.5p16
dtype grib2
ydef 1153 linear -90.0 0.15625
xdef 1536 linear   0.0 0.234375 
tdef %d linear %s 6hr
zdef 7 levels
1000 925 850 700 500 300 200 
vars 4
ua    7,100      0,2,2 ** (1000 925 850 700 500 300 200) U-Component of Wind [m/s]
uas   0,103,10   0,2,2 ** 10 m above ground U-Component of Wind [m/s]
va    7,100      0,2,3 ** (1000 925 850 700 500 300 200) V-Component of Wind [m/s]
vas   0,103,10   0,2,3 ** 10 m above ground V-Component of Wind [m/s]
ENDVARS"""%(gfile,gfile,nt,gtime)
            
        elif(mf.find(ctlpath,'mass')):
            
            ctl="""dset ^%s
index ^%s.idx
undef 9.999E+20
title mass.2017031300_000_meto.grib
*  produced by grib2ctl v0.9.12.5p16
dtype grib2
ydef 1152 linear -89.922 0.15625
xdef 1536 linear   0.117 0.234375
tdef %d linear %s 6hr
zdef 7 levels
1000 925 850 700 500 300 200 
vars 7
zg    7,100           0,3,5 ** (1000 925 850 700 500 300 200) Geopotential Height [gpm]
psl   0,1,0           0,3,1 ** surface Pressure Reduced to MSL [Pa]
hur   7,100           0,1,1 ** (1000 925 850 700 500 300 200) Relative Humidity [%]
ta    7,100           0,0,0 ** (1000 925 850 700 500 300 200) Temperature [K]
tas   0,103,1         0,0,0 ** 2 m above ground Temperature [K]
pr    0,1,0        0,1,49,0 ** total presip [kg/m^2]
prc   0,1,0   255,255,255,0 ** conv precip [kg/m^2]
ENDVARS"""%(gfile,gfile,nt,gtime)         
            
        MF.WriteCtl(ctl,ctlpath)
        vopt=''
        if(self.verb): vopt='-v'
        cmd="gribmap %s -i %s"%(vopt,ctlpath)
        mf.runcmd(cmd,ropt)
        

    def destaggerMass2Wind(self,octlpathM,octlpathW,grbpathA,ropt=''):
        
        cmd='''grads -lbc "%s/%s %s %d %s %s %s %s"'''%(self.prcdir,self.latsCmd,self.dtg,int(self.tau),
                                                     octlpathW,octlpathM,grbpathA,self.ptable)
        mf.runcmd(cmd,ropt)
        
    def doGribmap(self,ropt=''):

        if(self.ntauPrc > 0):
            cmd="w2.fld.wgrib.filter.py %s %s -C -R"%(self.dtg,self.model)
            mf.runcmd(cmd,ropt)
        else:
            print '---'
            print 'III-TTT skip doing w2.fld.wgrib.filter.py because no taus actually processed for dtg: ',self.dtg
            print '---'
            return
        
        
class ukmNative2(Grib2):

    dtgHR='2017071112'
    xwgrib='wgrib2'
    latsCmd='w2.fld.ukm2lats.gs'
    
    model='ukm2'
    sdir='/public/data/grids/ukmet'
    prcdir=w2.PrcDirFlddatW2
    ptable="%s/../hfip/lats.hfip.table.txt"%(prcdir)

    def __init__(self,dtg,
                 tauopt=None,
                 doPrc=1,
                 ropt='',
                 override=0,
                 verb=0):

        from M2 import setModel2
        
        def makeCard(nrec,W):
            ocard="%d:%d:%03d:%s:%d:%d:%d:%f"%(nrec,W.sizrecp1,W.tau,W.var,W.lev,W.ndef,W.nundef,W.gridvalmin)
            ocard=ocard+'\n'
            return(ocard)



        m2=setModel2(self.model)

        self.dtg=dtg
        self.verb=verb
        # -- new version on dtgHR => 2560x1921 (0.14x0.09 deg)
        ddtg=mf.dtgdiff(self.dtgHR,dtg)
        self.ddtgHR=ddtg
        print 'QQQQQQQQQQQQQQQQQQQQQQQQQQ ddtgHR: ',self.ddtgHR

        self.fm=m2.DataPath(dtg,dtype='w2flds',dowgribinv=1,verb=verb)
        self.fstatuss=self.fm.statuss[dtg]

        if(not(doPrc)):
            print "ukmNative2 - returning because only making the self.fm object for grb1to2"
            return


        
        (tdir,tbase)=os.path.split(m2.tdatbase)
        MF.ChkDir(tdir,'mk')
        
        tmpdir="%s/tmp"%(tdir)
        MF.ChkDir(tmpdir,'mk')
        
        taus=[]
        grib2s=glob.glob("%s/%s_???_meto.grib2"%(self.sdir,dtg))
        grib2s.sort()

        # -- counter for tau prcoessed
        #
        self.ntauPrc=0
        filttaus=[]
        if(tauopt != None): filttaus=setTausTauopt(tauopt)
        
        for grbpath in grib2s:

            (ddir,dfile)=os.path.split(grbpath)
            tau=dfile.split("_")[1]
            self.tau=tau

            itau=int(tau)
            
            if(len(filttaus) > 0 and not(itau in filttaus)):
                print 'skipping tau: ',itau,' because not in filttaus: ',filttaus
                continue
            
            if(len(self.fstatuss.keys()) > 0):
                try:
                    nftau=self.fstatuss[itau][1]
                except:
                    nftau=-1
            else:
                nftau=-1

            # -- bypass if already done...
            #
            if(nftau > 0 and not(override)): 
                print 'III(%s) already processed tau: %03d ... press ...'%(CL.pyfile,itau)
                continue
            
            self.ntauPrc=self.ntauPrc+1
            
            (dbase,dext)=os.path.splitext(dfile)
            fdbpath="%s/%s.wgrib1.txt"%(tmpdir,dbase)

            ndxpathW="%s/wind.%s.f%s.idx"%(tmpdir,dtg,tau)
            ndxpathM="%s/mass.%s.f%s.idx"%(tmpdir,dtg,tau)

            octlpathW="%s/wind.%s.f%s.ctl"%(tmpdir,dtg,tau)
            octlpathM="%s/mass.%s.f%s.ctl"%(tmpdir,dtg,tau)
            
            ogrbpathA="%s/wind-mass.%s.f%s"%(tmpdir,dtg,tau)
            fgrbpath="%s.f%s.grb1"%(m2.tdatbase,tau)

            print 'WWWWWWWWWWWWWWWWWWWW22222222222222222Working tau: ',tau,' grbpath: ',grbpath

            self.makeCtl(grbpath,ndxpathW,octlpathW)
            self.makeCtl(grbpath,ndxpathM,octlpathM)
            
            self.destaggerMass2Wind(octlpathM, octlpathW, ogrbpathA)
            
            # -- mv output to w2flds location
            #
            cmd="mv %s.grb %s"%(ogrbpathA,fgrbpath)
            mf.runcmd(cmd,ropt)
            
            # -- clean tmp dir
            #
            cmd="rm %s/*.grb*"%(tmpdir)
            mf.runcmd(cmd,ropt)
            
            cmd="rm %s/*.ctl*"%(tmpdir)
            mf.runcmd(cmd,ropt)
            
        self.doGribmap()
        

    def makeCtl(self,grbpath,ndxpath,ctlpath,
                dtau=6,
                verb=0,
                ropt=''):
        
        """ grib2 version
"""
        itau=int(self.tau)
        nt=(itau/dtau) + 1
        gtime=mf.dtg2gtime(self.dtg)
        
        if(mf.find(ctlpath,'wind')):

            xydef="""ydef 1153 linear -90.0 0.15625
xdef 1536 linear   0.0 0.234375"""
            
            if(self.ddtgHR >= 0.0):
                xydef="""ydef 1921 linear -90.0 0.093750                                                                                                     |2:14753459:vt=2017071412:10 m above ground:72 hour fcst:VGRD V-Component of Wind [m/s]:
xdef 2560 linear   0.0 0.140625"""
                
            ctl="""dset %s
index %s
undef 9.999E+20
options pascals
title wind.2017031300_000_meto.grib2
*  produced by grib2ctl v0.9.12.5p16
dtype grib2
%s
tdef %d linear %s 6hr
zdef 7 levels
100000 92500 85000 70000 50000 30000 20000 
vars 4
ua    7,100      0,2,2 ** (1000 925 850 700 500 300 200) U-Component of Wind [m/s]
uas   0,103,10   0,2,2 ** 10 m above ground U-Component of Wind [m/s]
va    7,100      0,2,3 ** (1000 925 850 700 500 300 200) V-Component of Wind [m/s]
vas   0,103,10   0,2,3 ** 10 m above ground V-Component of Wind [m/s]
ENDVARS"""%(grbpath,ndxpath,xydef,nt,gtime)
            
        elif(mf.find(ctlpath,'mass')):
            
            xydef="""ydef 1152 linear -89.922 0.15625
xdef 1536 linear   0.117 0.234375"""
            
            if(self.ddtgHR >= 0.0):
                xydef="""ydef 1920 linear -89.953125 0.093750                                                                                                |2:14753459:vt=2017071412:10 m above ground:72 hour fcst:VGRD V-Component of Wind [m/s]:
xdef 2560 linear   0.070312 0.140625"""
                
            ctl="""dset %s
index %s
undef 9.999E+20
title mass.2017031300_000_meto.grib2
*  produced by grib2ctl v0.9.12.5p16
dtype grib2
options pascals
%s
tdef %d linear %s 6hr
zdef 7 levels
100000 92500 85000 70000 50000 30000 20000 
vars 7
zg    7,100           0,3,5 ** (1000 925 850 700 500 300 200) Geopotential Height [gpm]
psl   0,1,0           0,3,1 ** surface Pressure Reduced to MSL [Pa]
hur   7,100           0,1,1 ** (1000 925 850 700 500 300 200) Relative Humidity [%l%]
ta    7,100           0,0,0 ** (1000 925 850 700 500 300 200) Temperature [K]
tas   0,103,1         0,0,0 ** 2 m above ground Temperature [K]
pr    0,1,0        0,1,49,0 ** total presip [kg/m^2]
prc   0,1,0   255,255,255,0 ** conv precip [kg/m^2]
ENDVARS"""%(grbpath,ndxpath,xydef,nt,gtime)         
            
        MF.WriteCtl(ctl,ctlpath)
        vopt=''
        if(self.verb): vopt='-v'
        cmd="gribmap %s -i %s"%(vopt,ctlpath)
        mf.runcmd(cmd,ropt)
        

    def destaggerMass2Wind(self,octlpathM,octlpathW,grbpathA,ropt=''):
        
        cmd='''grads -lbc "%s/%s %s %d %s %s %s %s"'''%(self.prcdir,self.latsCmd,self.dtg,int(self.tau),
                                                     octlpathW,octlpathM,grbpathA,self.ptable)
        mf.runcmd(cmd,ropt)
        
    def doGribmap(self,ropt=''):

        if(self.ntauPrc > 0):
            cmd="w2.fld.wgrib.filter.py %s %s -C -R"%(self.dtg,self.model)
            mf.runcmd(cmd,ropt)
        else:
            print '---'
            print 'III-TTT skip doin w2.fld.wgrib.filter.py because no taus actually processed for dtg: ',self.dtg
            print '---'
            return
        
    def grb1togrb2(self,override=0,doArchive=0,ropt=''):
        """ convert grib1 from lats destaggering to grib2 using wesley's grb1to2.pl
"""

        packingType='j'
        packingType='c0'
        grib1s=self.fm.datpaths
        for grib1 in grib1s:
            ogrib2=grib1[0:-1]+'2'
            siz2=MF.getPathSiz(ogrib2)
            (fdir,ffile)=os.path.split(grib1)
            tt=ffile.split('.')
            dtg=tt[-3]
            tau=tt[-2]
            #print 'gggg',grib1,ogrib2,siz2,dtg,tau
            if(siz2 <= 0 or override):
                ttag='grb1-grb2 for: %s tau: %s'%(dtg,tau)
                MF.sTimer(ttag)
                cmd="grb1to2.pl -fast -packing %s %s -o %s"%(packingType,grib1,ogrib2)
                mf.runcmd(cmd,ropt)
                MF.dTimer(ttag)
                
                if(doArchive):
                    cmd="rm %s"%(grib1)
                    mf.runcmd(cmd,ropt)
                
        self.makeCtl2(override=override)
        self.rsync2Kishou()
            
    def makeCtl2(self,override=0):
        
        ctlpath=self.fm.ctlpath
        gmppath=ctlpath.replace('.ctl','.gmp2')
        (gmpdir,gmpfile)=os.path.split(gmppath)
        
        nt=self.fm.etau/self.fm.dtau+1
        print 'nn',nt,gmpfile,gmppath
        gtime=mf.dtg2gtime(self.dtg)
        ctl="""dset ^ukm2.w2flds.%s.f%%f3.grb2
index ^%s
undef 9.999E+20
title /data/amb/users/fiorino/w21/dat/nwp2/w2flds/dat/ukm2/2017071400/ukm2.w2flds.2017071400.f084.grb2
*  produced by g2ctl v0.0.4m
* griddef=1:0:(2560 x 1921):grid_template=0:winds(N/S): lat-lon grid:(2560 x 1921) units 1e-06 input WE:SN output WE:SN res 48 lat -90.000000 to 90.480000 by 0.094000 lon 0.000000 to 0.819000 by 0.141000 #points=4917760:winds(N/S)
dtype grib2
xdef 2560 linear   0.0 0.140625
ydef 1921 linear -90.0 0.093750
tdef   %d linear %s %dhr
* PROFILE hPa
zdef 7 levels 100000 92500 85000 70000 50000 30000 20000
options pascals template
vars 11
prc   0,1       0,1,10 surface Convective Precipitation [kg/m^2]
pr    0,1       0,1,8  surface Total Precipitation [kg/m^2]
zg    7,100     0,3,5  (1000 925 850 700 500 300 200) Geopotential Height [gpm]
psl   0,101     0,3,1  mean sea level Pressure Reduced to MSL [Pa]
hur   7,100     0,1,1  (1000 925 850 700 500 300 200) Relative Humidity [%%]
ta    7,100     0,0,0  (1000 925 850 700 500 300 200) Temperature [K]
tas   0,103,2   0,0,0   2 m above ground Temperature [K]
ua    7,100     0,2,2  (1000 925 850 700 500 300 200) U-Component of Wind [m/s]
uas   0,103,10  0,2,2  10 m above ground U-Component of Wind [m/s]
va    7,100     0,2,3  (1000 925 850 700 500 300 200) V-Component of Wind [m/s]
vas   0,103,10  0,2,3  10 m above ground V-Component of Wind [m/s]
ENDVARS"""%(self.dtg,gmpfile,nt,gtime,self.fm.dtau)
        
        MF.WriteCtl(ctl, self.fm.ctlpath)
        cmd="gribmap -v -i %s"%(self.fm.ctlpath)
        mf.runcmd(cmd,ropt)

    def rsync2Kishou(self,ropt=''):
        
        tdir=self.fm.tdatbase
        (tdir,tfile)=os.path.split(tdir)
        print 'tdir: ',tdir
        tdirKishou=tdir.replace(w2.Nwp2DataBdir,'fiorino@kishou.fsl.noaa.gov:/w21/dat/nwp2')
        print 'tdirKishou: ',tdirKishou
        
        prcdir=w2.PrcDirFlddatW2
        expath="%s/ex-kaze2kishou.txt"%(prcdir)
        
        rsyncoptDry='-alvn --delete  --protocol=29 --exclude=tmp/ --exclude-from=%s '%(expath)
        rsyncoptDo='-alv --delete --protocol=29  --exclude=tmp/ --exclude-from=%s '%(expath)
        rsyncopt=rsyncoptDo
        if(ropt == 'norun'):
            rsyncopt=rsyncoptDry
            ropt=''
            
        cmd='rsync %s %s/ %s/'%(rsyncopt,tdir,tdirKishou)
        mf.runcmd(cmd,ropt)

      
        
        
        



#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# command line setup
#

class AppCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv

        self.argv=argv
        self.argopts={
            1:['dtgopt',  'dtgs to process'],
        }

        self.options={
            'override':         ['O',0,1,'override'],
            'verb':             ['V',0,1,'verb=1 is verbose'],
            'ropt':             ['N','','norun',' norun is norun'],
            'tauopt':           ['t:',None,'a','tau option'],
            'doGrb1toGrb2':     ['C',0,1,'convert to LATS grib1 to grib2'],
            'doArchive':        ['A',0,1,'convert to LATS grib1 to grib2 and archive by rm grib1'],

        }

        self.purpose="""
working with true native grid ukm2 files"""

        self.examples='''
%s cur12 '''

#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# main
#
# -----------------------------------  default setting of max taus
#
argv=sys.argv
CL=AppCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

doPrc=1
if(doGrb1toGrb2 or doArchive): doPrc=0

overrideCA=0
if(override and (doGrb1toGrb2 or doArchive)): 
    override=0
    overrideCA=1

MF.sTimer('all-DTGs')
dtgs=mf.dtg_dtgopt_prc(dtgopt)

grib2dtg='2017042712'
for dtg in dtgs:

    MF.sTimer("ukm2-native: %s"%(dtg))
    ddtg=mf.dtgdiff(grib2dtg,dtg)
    
    if(ddtg >= 0.0):
        u2=ukmNative2(dtg,
                      doPrc=doPrc,
                      tauopt=tauopt,
                      ropt=ropt,
                      override=override,
                      verb=verb)
        
        if(doGrb1toGrb2):
            u2.grb1togrb2(override=overrideCA,doArchive=doArchive,ropt=ropt)
        
        
    else:
        u2=ukmNative(dtg,
                     ropt=ropt,
                     override=override,
                     verb=verb)
    MF.dTimer("ukm2-native: %s"%(dtg))
 
MF.dTimer('all-DTGs')
