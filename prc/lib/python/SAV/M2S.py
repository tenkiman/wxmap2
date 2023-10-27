from WxMAP2 import *
w2=W2()

from FM import FimRun
from GRIB import Grib1,Grib2


#CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
#
# classes


#CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
#
# classes

class ModelS(MFbase):

    modelrestitle=None
    modelDdtg=None
    modelgridres=None
    modelprvar=None
    modelpslvar=None
    modeltitleAck1=None
    modeltitleFullmod=None

    btau=0
    etau=168
    dtau=6

    warn=0
    
    # -- force construction of class
    #
    def __init__(self,model='mmm',center='nanimo',gribver=2,bdir2=None):

        # -- defaults
        #
        self.geodir=w2.GeogDatDirW2
        if(bdir2 == None):
            self.bdir2=w2.Nwp2DataBdir
        else:
            self.bdir2=bdir2

        self.myname="Dr. Mike Fiorino (mike@wxmap2.com) WxMAP2, Longmont, CO"
        self.modeltitleAck2=myname

        self.model=model
        self.dmodel=model
        self.dirmodel=model

        self.tautype=None
        self.nfields=999
        self.nfieldsW2flds=999
        self.dmodelType=None        

        self.gmask=None
        self.grbpaths=[]

        self.xwgrib='wgrib'
        self.location='kishou'

        self.rundtginc=6

        name2tau=None  # force these three methods to be set
        setxwgrib=None
        setgmask=None
        
        # -- set tryarch here
        if(tryarch != None): self.tryarch=tryarch


        self.center=center
        
        self.w2fldsSrcDir="%s/w2flds/dat/%s"%(self.bdir2,self.model)

        self.gribver=gribver
        self.gribtype='grb%d'%(self.gribver)
        


    def getEtau(self,dtg=None):
        if(dtg == None):
            return(self.etau)
        else:
            return(self.etau)

    def getDtau(self,dtg=None):
        if(dtg == None):
            return(self.dtau)
        else:
            return(self.dtau)

    def setDbase(self,dtg,dtype='w2flds',warn=0):
        
        cyear=dtg[0:4]
        
        if(not(hasattr(self,'lmodel'))): self.lmodel=self.dmodel

        if(dtype == 'w2flds'):
            self.dmodel=self.model
            self.lmodel=self.model

        self.bddir=self.w2fldsSrcDir
        self.dbasedir="%s/%s"%(self.bddir,dtg)
        self.dbasedirarch="%s/%s"%(self.bddirarch,dtg)
        self.dbasedirarchDat6="%s/%s"%(self.bddirarchDat6,dtg)

        self.dmodelType=dtype

        self.bddirNWP2=self.bddir
        
        if(dtype == 'w2flds'):
            self.bddir=self.w2fldsSrcDir
            self.dbasedir="%s/%s/%s"%(self.bddir,cyear,dtg)
            self.dbase="%s/%s/%s/%s.%s.%s"%(self.bddir,cyear,dtg,self.lmodel,dtype,dtg)

        self.dpath="%s.ctl"%(self.dbase)
        self.dpathexists=os.path.exists(self.dpath)
        self.tdatbase=self.dbase


    # -- set prvar method to set dependence on tau
    #
    def setprvar(self,dtg=None,tau=None):
        modelprvar=self.modelprvar
        if(tau >= 0 and tau <= 120):
            modelprvar="""_prvar='(( const(pr(t+1),0,-u)-const(pr(t-0),0,-u) )*4)'"""
        elif(tau > 120):
            modelprvar="""_prvar='(( const(pr(t+2),0,-u)-const(pr(t-0),0,-u) )*2)'"""
            
        return(modelprvar)



    def DataPath(self,dtgopt,dtype=None,getFromMss=0,dowgribinv=1,dofilecheck=1,override=0,ropt='',
                 diag=0,
                 useglob=0,
                 doDATage=0,
                 verb=1):


        if(hasattr(self,'doDATage')): doDATage=self.doDATage
        dpaths=[]
        statuss={}

        self.dtype=dtype

        dtgs=mf.dtg_dtgopt_prc(dtgopt)

        inV=None
        if(hasattr(self,'iV')): inV=self.iV.hash
        
        dataDtgs=[]

        for dtg in dtgs:
            
            # -- find tau offset
            #
            dataDtg=dtg
            if(w2.is0618Z(dtg) and self.modelDdtg == 12):
                self.tauOffset=6
                dataDtg=mf.dtginc(dtg,-6)
                
            dataDtgs.append(dataDtg)
            
            status={}

            self.setDbase(dataDtg,dtype=dtype)
            
            try:
                dthere=os.path.exists(self.dpath)
            except:
                dthere=0

            if(dthere):
                siz=MF.GetPathSiz(self.dpath)
                dpaths.append(self.dpath)

            elif(getFromMss):
                if(not(hasattr(self,'archmodelcenter'))): self.archmodelcenter=self.modelcenter
                mssdpath="%s/%s/%s.%s.tar"%(self.addir,self.archmodelcenter,self.dmodel,dataDtg)
                rc=os.popen('mssLs %s'%(mssdpath)).readlines()
                print 'getFromMss rc: ',rc

                if(len(rc) == 1):
                    tarball=rc[0]
                    mf.ChangeDir(self.bddir)
                    mf.runcmd(cmd,ropt)

                dthere=os.path.exists(self.dpath)
                if(dthere):
                    dpaths.append(self.dpath)

            # check file status...doesn't work!!!
            #
            #if(dofilecheck == 0):
            #    self.statuss=statuss
            #    return(self)

            if(dtype != None and not(hasattr(self,'dmodelType'))): self.dmodelType=dtype

            self.setxwgrib(dataDtg)
            if(hasattr(self,'setgmask')): self.setgmask(dtg)

            # -- special case for navgem from ncep
            #
            if(hasattr(self,'dsetMaskOverride') and self.dsetMaskOverride):
                
                def name2tau(ffile,dtg):
                    
                    try:
                        tau=ffile.split('.')[-2][-3:]
                        tau=int(tau)
                    except:
                        tau=None
                    return(tau)
                
                self.name2tau=name2tau
                
            
            elif(hasattr(self,'dmodelType') and self.dmodelType == 'w2flds' and self.tautype != 'alltau'):
                
                self.dmask=self.dmask.replace(self.dmodel,'%s.w2flds'%(self.dmodel))
                if(hasattr(self,'dsetmask')):
                    self.dsetmask=self.dsetmask.replace(self.dmodel,'%s.w2flds'%(self.dmodel))
                def name2tau(file,dtg):
                    try:
                        tau=file.split('.')[3][1:]
                        tau=int(tau)
                    except:
                        tau=None
                    return(tau)
                self.name2tau=name2tau


                
            self.datmask="%s/%s"%(self.dbasedir,self.dmask)

            self.datpaths=glob.glob(self.datmask)
            self.datpaths.sort()
            
            self.grbmask="%s/%s"%(self.dbasedir,self.gmask)
            self.grbpaths=glob.glob(self.grbmask)
            self.grbpaths.sort()
            
            if( len(self.datpaths) == 0 and len(self.grbpaths) > 0):
                print 'WWW(Model2.DataPath): len(self.datpaths): ',len(self.datpaths),' but grbpaths there'

                for grbpath in self.grbpaths:
                    grbsiz=MF.GetPathSiz(grbpath)
                    if(grbsiz == 0):
                        print 'WWW(Model2.DataPath): zero length source grb: ',grbpath,' delete'
                        os.unlink(grbpath)
                    else:
                        if(hasattr(self,'gname2tau')):
                            ctau="%03d"%(self.gname2tau(grbpath,dataDtg))
                            if(hasattr(self,'doLn') and self.doLn):
                                lmfile="%s.f%s.%s"%(self.tdatbase,ctau,self.gribtype)
                                cmd="ln -s -f %s %s"%(grbpath,lmfile)
                                mf.runcmd(cmd,ropt)

                self.datpaths=glob.glob(self.datmask)


            if ( len(self.datpaths) > 0):

                for datpath in self.datpaths:

                    (fdir,ffile)=os.path.split(datpath)
                    (base,ext)=os.path.splitext(datpath)
                    tau=self.name2tau(ffile,dtg)

                    gotit=0
                    if(inV != None and not(override)):
                        try:
                            (datpath,age,nf)=inV[self.model,dtg,tau]
                            status[tau]=(age,nf)
                            gotit=1
                        except:
                            None

                    if(gotit): continue


                    # -- bypass zero length files
                    #
                    if(MF.GetPathSiz(datpath) == 0):
                        if(self.warn): print 'WWW MF.GetPathSiz(datpath) == 0',MF.GetPathSiz(datpath)
                        continue


                    # old forms of the wgribpaths...
                    #
                    if(self.tautype == 'alltau' and dtype != 'w2flds'):
                        owgribpath="%s/%s.wgrib.txt"%(dir,base)
                    else:
                        owgribpath="%s/%s.%s.%03d.wgrib.txt"%(dir,self.model,dataDtg,tau)


                    #if(self.tautype == 'alltau'):
                    #    wgribpath="%s.wgrib%1d.txt"%(base,self.gribver)
                    #else:
                    (base,ext)=os.path.splitext(datpath)
                    wgribpath="%s.wgrib%1d.txt"%(base,self.gribver)

                    #if(os.path.exists(owgribpath)):
                    #    cmd="mv %s %s"%(owgribpath,wgribpath)
                    #    mf.runcmd(cmd,'')

                    if(dowgribinv):
                        try:
                            datsize=os.path.getsize(datpath)
                        except:
                            datsize=-999

                        if(not(os.path.exists(wgribpath)) or (os.path.getsize(wgribpath) == 0 and datsize > 0) or override):
                            cmd="%s %s > %s"%(self.xwgrib,datpath,wgribpath)
                            if(diag):  mf.runcmd(cmd)
                            else:      mf.runcmd(cmd,'quiet')    
                            
                    if(os.path.exists(wgribpath)):
                        if(doDATage):
                            age=MF.PathCreateTimeDtgdiff(dataDtg,datpath)
                        else:
                            age=MF.PathCreateTimeDtgdiff(dataDtg,wgribpath)
                            
                        if(age >= 1000.0): age=999.9
                        cards=open(wgribpath).readlines()
                        nf=len(cards)
                        status[tau]=(age,nf)

                        if(inV != None):
                            rc=(datpath,age,nf)
                            if(verb): print 'PPP putting rc: ',self.model,dataDtg,tau,nf
                            inV[self.model,dtg,tau]=rc


            else:
                status={}

            statuss[dtg]=status

        #
        # outside  dtg loop -- single dtg
        #

        self.ctlpath="%s.ctl"%(self.tdatbase)

        self.dpaths=dpaths
        self.ddtgs=dataDtgs
        self.statuss=statuss

        if(self.dmodelType != None and self.dmodelType == 'w2flds'):
            self.nfields=self.nfieldsW2flds
        else:
            self.nfields=self.nfields
            
        if(hasattr(self,'iV')): self.iV.put()


        return(self)


    def GetDataStatus(self,dtg,checkNF=0,mintauNF=5):

        if(hasattr(self,'bddirNWP2')):
            tdir="%s/%s"%(self.bddirNWP2,dtg)
        else:
            tdir="%s/%s"%(self.bddir,dtg)

        NFmin=self.nfields
        if(checkNF): NFmin=self.nfields-mintauNF

        lastTau=None
        latestTau=None
        latestCompleteTau=None
        earlyTau=None
        gmplastdogribmap=-999
        gmplatestTau=-999
        gmplastTau=-999

        mask="%s/gribmap.status.*.txt"%(tdir)
        gmps=glob.glob(mask)
        gmps.sort()

        gmpAge=0.0
        if(len(gmps) >= 1):
            for gmpspath in gmps:
                age=MF.PathCreateTimeDtgdiff(dtg,gmpspath)
                if(age > gmpAge):
                    gmpAge=age
                    latestgmpPath=gmpspath

            (dir,file)=os.path.split(latestgmpPath)
            tt=file.split('.')

            if(len(tt) >= 6):
                gmplastdogribmap=int(tt[3])
                gmplatestTau=int(tt[4])
                gmplastTau=int(tt[5])


        if(len(self.statuss) == 0):
            return(self)

        status=self.statuss[dtg]
        itaus=status.keys()
        itaus.sort()
        
        ages={}
        for itau in itaus:
            ages[itau]=status[itau][0]


        oldest=-1e20
        youngest=+1e20

        for itau in itaus:
            if(ages[itau] < youngest):
                youngest=ages[itau]
                earlyTau=itau

            # -- >= because for taus having the same age
            #
            if(ages[itau] >= oldest):
                oldest=ages[itau]
                latestTau=itau

        if(len(status) >= 1):
            lastTau=itaus[-1]
            latestCompleteTau=lastTau

        if(hasattr(self,'dattaus')):
            datataus=self.dattaus
        else:
            datataus=w2.Model2DataTaus(self.model,dtg)

        # -- forward search thru target data taus
        # 

        ndt=len(datataus)

        if(self.tautype == 'alltau'):
            latestCompleteTau=datataus[-1]
            
        else:
            for n in range(0,ndt):
                datatau=datataus[n]
                gotit=0
                for itau in itaus:
                    if(datatau == itau):
                        (age,nf)=self.statuss[dtg][itau]
                        if(checkNF and nf < NFmin):
                            gotit=0
                            continue
                        else:
                            gotit=1
                            latestCompleteTau=datatau
                        break
    
    
                if(gotit == 0):  break


        # -- backward search (default)
        #

        latestCompleteTauBackward=-999

        if(self.tautype == 'alltau' and self.dmodelType == None):
            None
        else:
            for n in range(ndt-1,0,-1):
                datatau=datataus[n]
                gotit=0
                for itau in itaus[-1:0:-1]:
                    if(datatau == itau):
                        (age,nf)=self.statuss[dtg][itau]
                        if(checkNF and nf < NFmin):
                            gotit=0
                            continue
                        else:
                            gotit=1
                            latestCompleteTauBackward=datatau
                        break
        
                if(gotit == 1):  break
        
        self.dstdir=tdir
        self.dsitaus=itaus
        self.dslastTau=lastTau
        self.dsgmpAge=gmpAge
        self.dsoldestTauAge=oldest
        self.dslatestTau=latestTau
        self.dsyoungest=youngest
        self.dsearlyTau=earlyTau
        self.dsgmplastdogribmap=gmplastdogribmap
        self.dsgmplatestTau=gmplatestTau
        self.dsgmplastTau=gmplastTau
        self.dslatestCompleteTau=latestCompleteTau
        self.dslatestCompleteTauBackward=latestCompleteTauBackward

        return(self)


    def makeCtl(self,dtg):

        if(not(hasattr(self,'lmodel'))): self.lmodel=self.dmodel
        if(not(hasattr(self,'dsetmask'))): self.dsetmask=self.dmask

        gmppath="%s.gmp"%(self.tdatbase)
        gmpfile="%s.%s.gmp"%(self.lmodel,dtg)

        gtime=mf.dtg2gtime(dtg)
        nt=(self.etau/self.dtau)+1

        self.ctl='''dset ^%s
index ^%s.%s.gmp
tdef % 3d linear %s %shr
%s
'''%(self.dsetmask,self.lmodel,dtg,nt,gtime,self.dtau,self.ctlgridvar)


    def doGrib(self,dtg,verb=0):

        # -- first set up the gribtype, etc
        self.setxwgrib(dtg)
        self.setctlgridvar(dtg)
        self.makeCtl(dtg)

        self.WriteCtl()  # from Model in M
        self.DoGribmap(gmpverb=verb) # from Model in M


    def setInventory(self,dtype='w2flds',override=0,unlink=0):

        dbname='nwp2Inv-%s'%(dtype)
        #tbdir=w2.Nwp2DataBdir
        #self.iV=InvHash(dbname,tbdir,override=override)

        tbdir=w2.Nwp2DataDSsBdir
        self.iV=InvHash(dbname,tbdir,override=override,unlink=unlink)


    def Model2PlotMinTau(self,dtg):
        mintauPlot=144
        return(mintauPlot)
    
    def writeCtl(self):
        MF.WriteCtl(self.ctl, self.dpath)

    def doGribmap(self,gmpverb=0):

        if(self.gribtype == 'grb1'): xgribmap='gribmap'
        if(self.gribtype == 'grb2'): xgribmap='gribmap'
        xgopt='-i'
        if(gmpverb):
            xgopt='-v -i'

        cmd="%s %s %s"%(xgribmap,xgopt,self.ctlpath)
        mf.runcmd(cmd)



class Jgsm(ModelS):

    modelrestitle='T574|N286 L64'
    modelDdtg=6
    modelgridres='1.25'
    modelres=modelgridres.replace('.','')
    modelpslvar='psl*0.01'

    btau=0
    etau=132
    dtau=6

    warn=0
    
    # -- force construction of class
    #
    
    def __init__(self,model='jgsm',center='jma',useAll=0,gribver=2,bdir2=None):

        # -- defaults
        #
        self.geodir=w2.GeogDatDirW2
        if(bdir2 == None):
            self.bdir2=w2.Nwp2DataBdir
        else:
            self.bdir2=bdir2

        self.myname="Dr. Mike Fiorino (mike@wxmap2.com) WxMAP2, Longmont, CO"
        self.modeltitleAck2=self.myname


        self.model=model
        self.dmodel=model
        self.dirmodel=model

        self.tautype=None
        self.nfields=999
        self.nfieldsW2flds=999
        self.dmodelType=None        

        self.gmask=None
        self.grbpaths=[]

        self.xwgrib='wgrib'
        self.location='kishou'

        self.rundtginc=6

        name2tau=None  # force these three methods to be set
        setxwgrib=None
        setgmask=None
        
        self.center=center
        
        self.w2fldsSrcDir="%s/w2flds/dat/%s"%(self.bdir2,self.model)

        self.gribver=gribver
        self.gribtype='grb%d'%(self.gribver)
        
        
        
    def setDbase(self,dtg,dtype='w2flds',warn=0):
        
        self.dtg=dtg
        cyear=dtg[0:4]
        if(not(hasattr(self,'lmodel'))): self.lmodel=self.dmodel

        self.dmodel=self.model
        self.lmodel=self.model
        
        if(dtype == 'w2flds'):

            self.bddir=self.w2fldsSrcDir
            self.dbasedir="%s/%s"%(self.bddir,dtg)
    
            self.dmodelType=dtype
            self.bddir=self.w2fldsSrcDir
            self.dbasedir="%s/%s/%s"%(self.bddir,cyear,dtg)
            self.dbase="%s/%s/%s/%s.%s.%s"%(self.bddir,cyear,dtg,self.lmodel,dtype,dtg)

        self.dpath="%s.ctl"%(self.dbase)
        self.dpathexists=os.path.exists(self.dpath)
        self.tdatbase=self.dbase
        
        self.xwgrib='wgrib2'
        self.dmask="%s.w2flds.%s.%s"%(self.dmodel,dtg,self.gribtype)

    def makeCtl(self):
        
        self.ctlpath=self.dpath
        self.setctlgridvar(self.dtg)
        self.lmodel=self.dmodel
        self.dsetmask=self.dmask

        gmppath="%s.gmp%s"%(self.tdatbase,self.gribver)
        (gdir,gmpfile)=os.path.split(gmppath)

        gtime=mf.dtg2gtime(dtg)
        nt=(self.etau/self.dtau)+1

        self.ctl='''dset ^%s
index ^%s
tdef % 3d linear %s %shr
%s
'''%(self.dsetmask,gmpfile,nt,gtime,self.dtau,self.ctlgridvar)


    def setGrib(self,verb=0):
        
        self.makeCtl()
        self.writeCtl()
        self.doGribmap(gmpverb=verb)
        

    def setctlgridvar(self,dtg):

        latlongrid='''xdef 288 linear   0.0 1.25
ydef 145 linear -90.0 1.25
zdef 17 levels 100000 92500 85000 70000 60000 50000 40000 30000 25000 20000 15000 10000 7000 5000 3000 2000 1000'''

        optiondtype='''options pascals
dtype grib2'''

        self.ctlgridvar='''undef 9.999E+20
title JMA GSM 1.25 deg deterministic run
*  produced by grib2ctl v0.9.12.5p16
%s
%s
vars 23
pr       0,1   0,1,8,1 ** surface Total Precipitation [kg/m^2]
zg      17,100  0,3,5 ** (1000 925 850 700 600.. 70 50 30 20 10) Geopotential Height [gpm]
psl      0,101   0,3,1 ** mean sea level Pressure Reduced to MSL [Pa]
RELD925mb   0,100,92500   0,2,13 ** 925 mb Relative Divergence [1/s]
RELD700mb   0,100,70000   0,2,13 ** 700 mb Relative Divergence [1/s]
RELD250mb   0,100,25000   0,2,13 ** 250 mb Relative Divergence [1/s]
RELV925mb   0,100,92500   0,2,12 ** 925 mb Relative Vorticity [1/s]
RELV700mb   0,100,70000   0,2,12 ** 700 mb Relative Vorticity [1/s]
RELV500mb   0,100,50000   0,2,12 ** 500 mb Relative Vorticity [1/s]
RELV250mb   0,100,25000   0,2,12 ** 250 mb Relative Vorticity [1/s]
hur      8,100  0,1,1 ** (1000 925 850 700 600 500 400 300) Relative Humidity [%%]
hurs     0,103,2   0,1,1 ** 2 m above ground Relative Humidity [%%]
STRM850mb   0,100,85000   0,2,4 ** 850 mb Stream Function [m^2/s]
STRM200mb   0,100,20000   0,2,4 ** 200 mb Stream Function [m^2/s]
ta       17,100  0,0,0 ** (1000 925 850 700 600.. 70 50 30 20 10) Temperature [K]
tas       0,103,2   0,0,0 ** 2 m above ground Temperature [K]
ua       17,100  0,2,2 ** (1000 925 850 700 600.. 70 50 30 20 10) U-Component of Wind [m/s]
uas       0,103,10   0,2,2 ** 10 m above ground U-Component of Wind [m/s]
va       17,100  0,2,3 ** (1000 925 850 700 600.. 70 50 30 20 10) V-Component of Wind [m/s]
vas       0,103,10   0,2,3 ** 10 m above ground V-Component of Wind [m/s]
VPOT850mb   0,100,85000   0,2,5 ** 850 mb Velocity Potential [m^2/s]
VPOT200mb   0,100,20000   0,2,5 ** 200 mb Velocity Potential [m^2/s]
VVELprs     8,100  0,2,8 ** (1000 925 850 700 600 500 400 300) Vertical Velocity (Pressure) [Pa/s]
endvars'''%(optiondtype,latlongrid)

    def getDataTaus(self,dtg):
        taus=range(0,self.etau+1,6)
        return(taus)

    # -- set prvar method to set dependence on tau
    #
    def setprvar(self,dtg=None,tau=None):
        modelprvar=self.modelprvar
        if(tau >= 0 and tau <= 120):
            modelprvar="""_prvar='(( const(pr(t+1),0,-u)-const(pr(t-0),0,-u) )*4)'"""
        elif(tau > 120):
            modelprvar="""_prvar='(( const(pr(t+2),0,-u)-const(pr(t-0),0,-u) )*2)'"""
            
        return(modelprvar)


    




class Model2(Model):

    addir=w2.Nwp2DataMassStore
    models=w2.Nwp2ModelsAll
    allmodels=w2.Nwp2ModelsAll
    models=w2.Nwp2ModelsActive
    modelsW2=w2.Nwp2ModelsActiveW2flds

    geodir=w2.GeogDatDirW2
    bdir2=w2.Nwp2DataBdir
    d2dir='/dat2/nwp2'
    archdir='/dat5/dat/nwp2'
    archdirDat6='/dat6/dat/nwp2'

    d2dir='/data/global/dat/nwp2'
    archdir='/data/global/dat/nwp2'
    archdirDat6='/data/global/dat/nwp2'

    modelrestitle=None
    modelDdtg=None
    modelgridres=None
    modelprvar=None
    modelpslvar=None
    modeltitleAck1=None
    modeltitleFullmod=None

    dofimlsgrib=1

    btau=0
    etau=168
    dtau=6

    warn=0

    myname="Dr. Mike Fiorino (michael.fiorino@noaa.gov) ESRL/GSD/AMB, Boulder, CO"
    modeltitleAck2=myname
    
    if(hasattr(w2,'W2doM2Tryarch')): tryarch=w2.W2doM2Tryarch
    
    def __init__(self,model='ecm2',center='ecmwf',useAll=0,gribver=1,chkm2=1,bdir2=None,
                 tryarch=tryarch):

        if(chkm2 and not(self.IsModel2(model))):
            print 'M2 -- invalid m2 model: ',model
            sys.exit()

        #
        # defaults
        #

        self.model=model
        self.dmodel=model
        self.dirmodel=model

        self.initModelCenter(center)
        self.initGribVer(gribver)

        self.tautype=None
        self.d2dir='/dat2/nwp2'
        self.nfields=999
        self.nfieldsW2flds=999
        self.dmodelType=None        

        self.gmask=None
        self.grbpaths=[]

        self.xwgrib='wgrib'
        self.location='kishou'

        self.rundtginc=6

        name2tau=None  # force these three methods to be set
        setxwgrib=None
        setgmask=None
        
        # -- set tryarch here
        if(tryarch != None): self.tryarch=tryarch
        


    def initModelCenter(self,center):
        self.center=center
        self.modelcenter="%s/%s"%(self.center,self.dirmodel)
        self.bddir="%s/%s"%(self.bdir2,self.modelcenter)
        self.bddirarch="%s/%s"%(self.archdir,self.modelcenter)
        self.bddirarchDat6="%s/%s"%(self.archdirDat6,self.modelcenter)
        self.w2fldsSrcDir="%s/w2flds/dat/%s"%(self.bdir2,self.model)
        self.w2fldsArchDir="/dat4/nwp2/w2flds/dat/%s"%(self.model)
        # -- temp location to free up the internal /dat4 drive
        self.w2fldsArchDir="/FWV1/dat2/nwp2/w2flds/dat/%s"%(self.model)
        self.w2fldsArchDir="/Volumes/FWV2/dat2/nwp2/w2flds/dat/%s"%(self.model)
        self.w2fldsArchDir="/dat5/dat/nwp2/w2flds/dat/%s"%(self.model)
        self.w2fldsArchDirDat6="/dat6/dat/nwp2/w2flds/dat/%s"%(self.model)

        self.rtfimSrcDir="%s/rtfim/dat"%(self.bdir2)
        self.rtfimArchDir="/Volumes/FWV2/dat2/nwp2/rtfim/dat"
        self.rtfimArchDir="/dat4/nwp2/rtfim/dat"
        self.rtfimArchDir2="/Volumes/FWV2/dat2/nwp2/rtfim/dat"
        self.nwp2ArchDir=w2.Nwp2DataBdirArch3

    def getRtfimModelsByDtg(self,dtg,sdir=None):

        rtmodels=[]
        if(sdir == None):   sdir=self.rtfimSrcDir

        smask="%s/*/%s"%(sdir,dtg)
        mm=glob.glob(smask)
        for m in mm:
            tt=m.split('/')
            ltt=len(tt)
            model=tt[ltt-2]
            rtmodels.append(model)
        return(rtmodels)


    def initGribVer(self,gribver):
        self.gribver=gribver
        self.gribtype='grb%d'%(self.gribver)

    def IsModel2(self,value):
        rc=0
        if(value in self.allmodels): rc=1
        return(rc)

    def IsModel1(self,value):
        rc=0
        if(value in self.models): rc=1
        return(rc)

    def getEtau(self,dtg=None):
        if(dtg == None):
            return(self.etau)
        else:
            return(self.etau)

    def getDtau(self,dtg=None):
        if(dtg == None):
            return(self.dtau)
        else:
            return(self.dtau)



    def Put2Arch(self,sbdir=None,tbdir=None,tdir=None,dtg=None,dtgs=None,rmsrc=0,ropt=''):

        rc=0
        if(tbdir == None): tbdir="%s"%(self.archdir)
        if(sbdir == None): sbdir=self.bddir
        if(dtg == None and dtgs == None): dtgs=self.ddtgs
        if(dtg != None and dtgs == None): dtgs=[dtg]

        for dtg in dtgs:
            sdir="%s/%s"%(sbdir,dtg)
            if(tdir == None):
                tdir="%s/%s"%(tbdir,self.modelcenter)

            mf.ChkDir(tdir,'mk')
            cmd="rsync -av %s %s"%(sdir,tdir)
            mf.runcmd(cmd,ropt)

            if(rmsrc):
                cmd="rm -r %s"%(sdir)
                mf.runcmd(cmd,ropt)

        print 'SSS(sbdir): ',sbdir
        print ' TTT(tdir): ',tbdir
        return(rc)


    def setDbase(self,dtg,dtype=None,warn=0):
        

        if(self.IsModel2(self.model) or self.IsModel1(self.model)):
            if(not(hasattr(self,'lmodel'))): self.lmodel=self.dmodel

            if(dtype == 'w2flds'):
                self.dmodel=self.model
                self.lmodel=self.model

            self.dbasedir="%s/%s"%(self.bddir,dtg)
            self.dbasedirarch="%s/%s"%(self.bddirarch,dtg)
            self.dbasedirarchDat6="%s/%s"%(self.bddirarchDat6,dtg)

            self.dmodelType=dtype

            self.bddirNWP2=self.bddir
            
            if(dtype != None):
                self.dbase="%s/%s.%s.%s"%(self.dbasedir,self.lmodel,dtg,dtype)
                if(dtype == 'w2flds'):
                    self.bddir=self.w2fldsSrcDir
                    self.dbasedir="%s/%s"%(self.bddir,dtg)
                    self.dbase="%s/%s/%s.%s.%s"%(self.bddir,dtg,self.lmodel,dtype,dtg)

            else:
                self.dbase="%s/%s.%s"%(self.dbasedir,self.lmodel,dtg)
                self.dmask="%s.%s.f???.%s"%(self.lmodel,dtg,self.gribtype)

            self.dpath="%s.ctl"%(self.dbase)

            self.dpathexists=os.path.exists(self.dpath)

            # -- try dat5
            #
            if(not(self.dpathexists) and self.tryarch):
                if(warn): print 'IIIIIIIIIIIIIIIIIIIIIIIIIIIIII M2.Model2.setDbase tryarch=1 -- trying the archive on: ',self.dbasedirarch,self.dtype
                self.dbasedir=self.dbasedirarch
                if(self.dtype != None):
                    self.dbase="%s/%s.%s.%s"%(self.dbasedir,self.lmodel,dtg,dtype)
                    if(self.dtype == 'w2flds'):
                        self.bddir=self.w2fldsArchDir
                        self.dbasedir="%s/%s"%(self.bddir,dtg)
                        self.dbase="%s/%s.%s.%s"%(self.dbasedir,self.lmodel,dtype,dtg)
                        self.dmask="%s.%s.%s.f???.%s"%(self.lmodel,dtype,dtg,self.gribtype)

                else:
                    self.dbase="%s/%s.%s"%(self.dbasedir,self.lmodel,dtg)
                    self.dmask="%s.%s.f???.%s"%(self.lmodel,dtg,self.gribtype)

                self.dpath="%s.ctl"%(self.dbase)
                self.dpathexists=os.path.exists(self.dpath)
            
            # -- try dat6
            #
            if(not(self.dpathexists) and self.tryarch):
                if(warn): print 'IIIIIIIIIIIIIIIIIIIIIIIIIIIIII M2.Model2.setDbase tryarch=1 -- trying the archive on: ',self.dbasedirarchDat6,self.dtype
                self.dbasedir=self.dbasedirarchDat6
                if(self.dtype != None):
                    self.dbase="%s/%s.%s.%s"%(self.dbasedir,self.lmodel,dtg,dtype)
                    if(self.dtype == 'w2flds'):
                        self.bddir=self.w2fldsArchDirDat6
                        self.dbasedir="%s/%s"%(self.bddir,dtg)
                        self.dbase="%s/%s.%s.%s"%(self.dbasedir,self.lmodel,dtype,dtg)
                        self.dmask="%s.%s.%s.f???.%s"%(self.lmodel,dtype,dtg,self.gribtype)

                else:
                    self.dbase="%s/%s.%s"%(self.dbasedir,self.lmodel,dtg)
                    self.dmask="%s.%s.f???.%s"%(self.lmodel,dtg,self.gribtype)

                self.dpath="%s.ctl"%(self.dbase)
                self.dpathexists=os.path.exists(self.dpath)

        elif(mf.find(self.model,'geo')):
            self.dbasedir=self.geodir
            if(self.model == 'geo05'):
                self.dpath="%s/lf.gfs.05deg.ctl"%(self.geodir)
            else:
                self.dpath=None

        elif(mf.find(self.model,'tctrk')):
            self.dbasedir="%s/%s"%(self.bddir,dtg)
            mask="%s/*.ctl"%(dbasedir)
            self.dpaths=glob.glob(mask)
            if(len(self.dpaths) > 0):
                self.dpaths=dpaths
            else:
                self.dpaths=[]
                self.ddtgs=[]

        else:
            print 'EEE could not set M2.setDbase.dbase  model: ',self.model,'dtg: ',dtg,' dtype: ',self.dtype,' or maybe because model not in w2localvars.py Nwp2ModelsAll...'
            sys.exit()

        self.tdatbase=self.dbase


    # -- set prvar method to set dependence on tau
    #
    def setprvar(self,dtg=None,tau=None):
        modelprvar=self.modelprvar
        if(tau == 0):
            modelprvar=modelprvar.replace('pr','pr(t+1)')
        return(modelprvar)



    def DataPath(self,dtgopt,dtype=None,getFromMss=0,dowgribinv=1,dofilecheck=1,override=0,ropt='',
                 diag=0,
                 useglob=0,
                 doDATage=0,
                 verb=1):


        if(hasattr(self,'doDATage')): doDATage=self.doDATage
        dpaths=[]
        statuss={}

        self.dtype=dtype

        dtgs=mf.dtg_dtgopt_prc(dtgopt)

        inV=None
        if(hasattr(self,'iV')): inV=self.iV.hash
        
        dataDtgs=[]

        for dtg in dtgs:
            
            # -- find tau offset
            #
            dataDtg=dtg
            if(w2.is0618Z(dtg) and self.modelDdtg == 12):
                self.tauOffset=6
                dataDtg=mf.dtginc(dtg,-6)
                
            dataDtgs.append(dataDtg)
            
            status={}

            self.setDbase(dataDtg,dtype=dtype)
            
            try:
                dthere=os.path.exists(self.dpath)
            except:
                dthere=0

            if(dthere):
                siz=MF.GetPathSiz(self.dpath)
                dpaths.append(self.dpath)

            elif(getFromMss):
                if(not(hasattr(self,'archmodelcenter'))): self.archmodelcenter=self.modelcenter
                mssdpath="%s/%s/%s.%s.tar"%(self.addir,self.archmodelcenter,self.dmodel,dataDtg)
                rc=os.popen('mssLs %s'%(mssdpath)).readlines()
                print 'getFromMss rc: ',rc

                if(len(rc) == 1):
                    tarball=rc[0]
                    mf.ChangeDir(self.bddir)
                    mf.runcmd(cmd,ropt)

                dthere=os.path.exists(self.dpath)
                if(dthere):
                    dpaths.append(self.dpath)

            # check file status...doesn't work!!!
            #
            #if(dofilecheck == 0):
            #    self.statuss=statuss
            #    return(self)

            if(dtype != None and not(hasattr(self,'dmodelType'))): self.dmodelType=dtype

            self.setxwgrib(dataDtg)
            if(hasattr(self,'setgmask')): self.setgmask(dtg)

            # -- special case for navgem from ncep
            #
            if(hasattr(self,'dsetMaskOverride') and self.dsetMaskOverride):
                
                def name2tau(ffile,dtg):
                    
                    try:
                        tau=ffile.split('.')[-2][-3:]
                        tau=int(tau)
                    except:
                        tau=None
                    return(tau)
                
                self.name2tau=name2tau
                
            
            elif(hasattr(self,'dmodelType') and self.dmodelType == 'w2flds' and self.tautype != 'alltau'):
                
                self.dmask=self.dmask.replace(self.dmodel,'%s.w2flds'%(self.dmodel))
                if(hasattr(self,'dsetmask')):
                    self.dsetmask=self.dsetmask.replace(self.dmodel,'%s.w2flds'%(self.dmodel))
                def name2tau(file,dtg):
                    try:
                        tau=file.split('.')[3][1:]
                        tau=int(tau)
                    except:
                        tau=None
                    return(tau)
                self.name2tau=name2tau


                
            self.datmask="%s/%s"%(self.dbasedir,self.dmask)

            self.datpaths=glob.glob(self.datmask)
            self.datpaths.sort()
            
            self.grbmask="%s/%s"%(self.dbasedir,self.gmask)
            self.grbpaths=glob.glob(self.grbmask)
            self.grbpaths.sort()
            
            if( len(self.datpaths) == 0 and len(self.grbpaths) > 0):
                print 'WWW(Model2.DataPath): len(self.datpaths): ',len(self.datpaths),' but grbpaths there'

                for grbpath in self.grbpaths:
                    grbsiz=MF.GetPathSiz(grbpath)
                    if(grbsiz == 0):
                        print 'WWW(Model2.DataPath): zero length source grb: ',grbpath,' delete'
                        os.unlink(grbpath)
                    else:
                        if(hasattr(self,'gname2tau')):
                            ctau="%03d"%(self.gname2tau(grbpath,dataDtg))
                            if(hasattr(self,'doLn') and self.doLn):
                                lmfile="%s.f%s.%s"%(self.tdatbase,ctau,self.gribtype)
                                cmd="ln -s -f %s %s"%(grbpath,lmfile)
                                mf.runcmd(cmd,ropt)

                self.datpaths=glob.glob(self.datmask)


            if ( len(self.datpaths) > 0):

                for datpath in self.datpaths:

                    (fdir,ffile)=os.path.split(datpath)
                    (base,ext)=os.path.splitext(datpath)
                    tau=self.name2tau(ffile,dtg)

                    gotit=0
                    if(inV != None and not(override)):
                        try:
                            (datpath,age,nf)=inV[self.model,dtg,tau]
                            status[tau]=(age,nf)
                            gotit=1
                        except:
                            None

                    if(gotit): continue


                    # -- bypass zero length files
                    #
                    if(MF.GetPathSiz(datpath) == 0):
                        if(self.warn): print 'WWW MF.GetPathSiz(datpath) == 0',MF.GetPathSiz(datpath)
                        continue


                    # old forms of the wgribpaths...
                    #
                    if(self.tautype == 'alltau' and dtype != 'w2flds'):
                        owgribpath="%s/%s.wgrib.txt"%(dir,base)
                    else:
                        owgribpath="%s/%s.%s.%03d.wgrib.txt"%(dir,self.model,dataDtg,tau)


                    #if(self.tautype == 'alltau'):
                    #    wgribpath="%s.wgrib%1d.txt"%(base,self.gribver)
                    #else:
                    (base,ext)=os.path.splitext(datpath)
                    wgribpath="%s.wgrib%1d.txt"%(base,self.gribver)

                    #if(os.path.exists(owgribpath)):
                    #    cmd="mv %s %s"%(owgribpath,wgribpath)
                    #    mf.runcmd(cmd,'')

                    if(dowgribinv):
                        try:
                            datsize=os.path.getsize(datpath)
                        except:
                            datsize=-999

                        if(not(os.path.exists(wgribpath)) or (os.path.getsize(wgribpath) == 0 and datsize > 0) or override):
                            cmd="%s %s > %s"%(self.xwgrib,datpath,wgribpath)
                            if(diag):  mf.runcmd(cmd)
                            else:      mf.runcmd(cmd,'quiet')    
                            
                    if(os.path.exists(wgribpath)):
                        if(doDATage):
                            age=MF.PathCreateTimeDtgdiff(dataDtg,datpath)
                        else:
                            age=MF.PathCreateTimeDtgdiff(dataDtg,wgribpath)
                            
                        if(age >= 1000.0): age=999.9
                        cards=open(wgribpath).readlines()
                        nf=len(cards)
                        status[tau]=(age,nf)

                        if(inV != None):
                            rc=(datpath,age,nf)
                            if(verb): print 'PPP putting rc: ',self.model,dataDtg,tau,nf
                            inV[self.model,dtg,tau]=rc


            else:
                status={}

            statuss[dtg]=status

        #
        # outside  dtg loop -- single dtg
        #

        self.ctlpath="%s.ctl"%(self.tdatbase)

        self.dpaths=dpaths
        self.ddtgs=dataDtgs
        self.statuss=statuss

        if(self.dmodelType != None and self.dmodelType == 'w2flds'):
            self.nfields=self.nfieldsW2flds
        else:
            self.nfields=self.nfields
            
        if(hasattr(self,'iV')): self.iV.put()


        return(self)


    def GetDataStatus(self,dtg,checkNF=0,mintauNF=5):

        if(hasattr(self,'bddirNWP2')):
            tdir="%s/%s"%(self.bddirNWP2,dtg)
        else:
            tdir="%s/%s"%(self.bddir,dtg)

        NFmin=self.nfields
        if(checkNF): NFmin=self.nfields-mintauNF

        lastTau=None
        latestTau=None
        latestCompleteTau=None
        earlyTau=None
        gmplastdogribmap=-999
        gmplatestTau=-999
        gmplastTau=-999

        mask="%s/gribmap.status.*.txt"%(tdir)
        gmps=glob.glob(mask)
        gmps.sort()

        gmpAge=0.0
        if(len(gmps) >= 1):
            for gmpspath in gmps:
                age=MF.PathCreateTimeDtgdiff(dtg,gmpspath)
                if(age > gmpAge):
                    gmpAge=age
                    latestgmpPath=gmpspath

            (dir,file)=os.path.split(latestgmpPath)
            tt=file.split('.')

            if(len(tt) >= 6):
                gmplastdogribmap=int(tt[3])
                gmplatestTau=int(tt[4])
                gmplastTau=int(tt[5])


        if(len(self.statuss) == 0):
            return(self)

        status=self.statuss[dtg]
        itaus=status.keys()
        itaus.sort()
        
        ages={}
        for itau in itaus:
            ages[itau]=status[itau][0]


        oldest=-1e20
        youngest=+1e20

        for itau in itaus:
            if(ages[itau] < youngest):
                youngest=ages[itau]
                earlyTau=itau

            # -- >= because for taus having the same age
            #
            if(ages[itau] >= oldest):
                oldest=ages[itau]
                latestTau=itau

        if(len(status) >= 1):
            lastTau=itaus[-1]
            latestCompleteTau=lastTau

        if(hasattr(self,'dattaus')):
            datataus=self.dattaus
        else:
            datataus=w2.Model2DataTaus(self.model,dtg)

        # -- forward search thru target data taus
        # 

        ndt=len(datataus)

        if(self.tautype == 'alltau'):
            latestCompleteTau=datataus[-1]
            
        else:
            for n in range(0,ndt):
                datatau=datataus[n]
                gotit=0
                for itau in itaus:
                    if(datatau == itau):
                        (age,nf)=self.statuss[dtg][itau]
                        if(checkNF and nf < NFmin):
                            gotit=0
                            continue
                        else:
                            gotit=1
                            latestCompleteTau=datatau
                        break
    
    
                if(gotit == 0):  break


        # -- backward search (default)
        #

        latestCompleteTauBackward=-999

        if(self.tautype == 'alltau' and self.dmodelType == None):
            None
        else:
            for n in range(ndt-1,0,-1):
                datatau=datataus[n]
                gotit=0
                for itau in itaus[-1:0:-1]:
                    if(datatau == itau):
                        (age,nf)=self.statuss[dtg][itau]
                        if(checkNF and nf < NFmin):
                            gotit=0
                            continue
                        else:
                            gotit=1
                            latestCompleteTauBackward=datatau
                        break
        
                if(gotit == 1):  break
        
        self.dstdir=tdir
        self.dsitaus=itaus
        self.dslastTau=lastTau
        self.dsgmpAge=gmpAge
        self.dsoldestTauAge=oldest
        self.dslatestTau=latestTau
        self.dsyoungest=youngest
        self.dsearlyTau=earlyTau
        self.dsgmplastdogribmap=gmplastdogribmap
        self.dsgmplatestTau=gmplatestTau
        self.dsgmplastTau=gmplastTau
        self.dslatestCompleteTau=latestCompleteTau
        self.dslatestCompleteTauBackward=latestCompleteTauBackward

        return(self)


    def makeCtl(self,dtg):

        if(not(hasattr(self,'lmodel'))): self.lmodel=self.dmodel
        if(not(hasattr(self,'dsetmask'))): self.dsetmask=self.dmask

        gmppath="%s.gmp"%(self.tdatbase)
        gmpfile="%s.%s.gmp"%(self.lmodel,dtg)

        gtime=mf.dtg2gtime(dtg)
        nt=(self.etau/self.dtau)+1

        self.ctl='''dset ^%s
index ^%s.%s.gmp
tdef % 3d linear %s %shr
%s
'''%(self.dsetmask,self.lmodel,dtg,nt,gtime,self.dtau,self.ctlgridvar)


    def doGrib(self,dtg,verb=0):

        # -- first set up the gribtype, etc
        self.setxwgrib(dtg)
        self.setctlgridvar(dtg)
        self.makeCtl(dtg)

        self.WriteCtl()  # from Model in M
        self.DoGribmap(gmpverb=verb) # from Model in M


    def setInventory(self,dtype='w2flds',override=0,unlink=0):

        dbname='nwp2Inv-%s'%(dtype)
        #tbdir=w2.Nwp2DataBdir
        #self.iV=InvHash(dbname,tbdir,override=override)

        tbdir=w2.Nwp2DataDSsBdir
        self.iV=InvHash(dbname,tbdir,override=override,unlink=unlink)


    def Model2PlotMinTau(self,dtg):
        mintauPlot=144
        return(mintauPlot)


#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# individual model classes
# gfs2


class Gfs2(Model2):

    btau=0
    # -- only goes to tau 192 on /public/data/grids/gfs/0p5deg/grib2/13JJJ
    etau=192
    dtau=6

    modelrestitle='T574|N286 L64'
    modelDdtg=6
    modelgridres='0.5'
    modelres=modelgridres.replace('.','')
    modelprvar="""_prvar='pr*4'"""
    modelpslvar='psl*0.01'

    model='gfs2'
    center='ncep'

    pltdir='plt_ncep_gfs'
    pmodel='gfs'

    modelPlotTaus=[0,6,12,18,24,30,36,42,48,60,72,84,96,108,120,132,144,156,168]
    gmodname="%s%s"%(pmodel,modelres)

    modeltitleAck1="NCEP GFS courtesy ESRL/GSD/ITS"
    modeltitleFullmod="NCEP(GFS)"

    regridTracker=0.25

    def __init__(self,bdir2=None,gribver=2):

        # three possible names for the model
        self.dmodel=self.model
        self.dirmodel=self.model
        
        if(bdir2 != None): self.bdir2=bdir2

        self.initModelCenter(self.center)
        self.initGribVer(gribver)

        self.tautype='wgrib'

        self.adecksource='ncep'
        self.adeckaid='avno'

        self.rundtginc=6

        self.nfields=344
        self.nfieldsW2flds=67


    def setprvar(self,dtg=None,tau=None,dtgGfsFv3='2019061212'):
        
        diff1=mf.dtgdiff(dtgGfsFv3,dtg)
        
        modelprvar=self.modelprvar
        if(tau == 0):
            modelprvar="""_prvar='pr(t+1)*4'"""
        if(tau >= 192):
            modelprvar="""_prvar='pr*2'"""
            
        # -- 20190614 -- like ukm2
        #
        if(diff1 >= 0):
            if(tau != None):
                if(tau <= 6):
                    modelprvar="""_prvar='pr(t+1)*4'"""
                elif(tau >= 12 and tau <= 66):
                    modelprvar="""_prvar='((pr(t-0)-pr(t-1)))*4'"""
                elif(tau >= 72 and tau <= 196):
                    #modelprvar="""_prvar='((pr(t-0)-pr(t-2)))*2'"""
                    modelprvar="""_prvar='((pr(t-0)-pr(t-1)))*4'"""

        return(modelprvar)




    def setMaxtau(self,dtg):
        hh=dtg[8:10]
        if(hh == '00' or hh == '12'):  self.maxtau=168
        else:    self.maxtau=168
        return(self.maxtau)



    def name2tau(self,file,dtg=None):
        ib=len(self.dmodel.split('.'))+1
        try:
            tau=file.split('.')[ib][1:]
            tau=int(tau)
        except:
            tau=None
        return(tau)

    def setgmask(self,dtg,dtg1='2009010100'):
        julday=int(mf.Dtg2JulianDay(dtg))
        yy=dtg[2:4]
        hh=dtg[8:10]

        diff1=mf.dtgdiff(dtg1,dtg)
        if(diff1 > 0.0 ):
            self.gmask="%2s%03d%2s*"%(yy,julday,hh)
        else:
            self.gmask="ZY0X1W2_%s*"%(dtg)


    def setxwgrib(self,dtg,dtg1='2009010100'):

        diff1=mf.dtgdiff(dtg1,dtg)
        if(diff1 > 0.0 ):
            self.nfields=331
            self.nfieldsW2flds=49

            self.gribtype='grb2'
            self.xwgrib='wgrib2'
            self.dmask="%s.%s.f???.grb2"%(self.dmodel,dtg)
            self.dsetmask="%s.%s.f%%f3.grb2"%(self.dmodel,dtg)
        else:

            self.nfields=57
            self.nfieldsW2flds=49

            self.gribtype='grb1'
            self.xwgrib='wgrib'
            self.dmask="%s.%s.f???.grb1"%(self.dmodel,dtg)
            self.dsetmask="%s.%s.f%%f3.grb1"%(self.dmodel,dtg)


    def setctlgridvar(self,dtg):

        if(self.gribtype == 'grb1'):
            optiondtype='''options template
dtype grib
zdef 10 levels 1000 925 850 700 500 300 250 200 150 100 
# profile in hPa
'''
            vars='''vars 19
prc    0  63,  1,0   ** Convective precipitation [kg/m^2]
pr     0  61,  1,0   ** Total precipitation [kg/m^2]
zg    10   7,100,0   ** Geopotential height [gpm]
psl    0   2,102,0   ** Pressure reduced to MSL [Pa]
hur   10  52,100,0   ** Relative humidity [%]
clt    0  71,211,0   ** Total cloud cover [%]
cll    0  71,214,0   ** Total cloud cover [%]
clm    0  71,224,0   ** Total cloud cover [%]
clh    0  71,234,0   ** Total cloud cover [%]
cltt   0  71,244,0   ** Total cloud cover [%]
tmx2m  0  15,105,2   ** Max. temp. [K]
tmn2m  0  16,105,2   ** Min. temp. [K]
tas    0  11,105,2   ** Temp. [K]
ua    10  33,100,0   ** u wind [m/s]
uas    0  33,105,10  ** u wind [m/s]
rlut   0 212,  8,0   ** Upward long wave flux [W/m^2]
va    10  34,100,0   ** v wind [m/s]
vas    0  34,105,10  ** v wind [m/s]
wap   10  39,100,0   ** Pressure vertical velocity [Pa/s]
endvars'''


        elif(self.gribtype == 'grb2'):
            optiondtype='''options template pascals
dtype grib2
zdef 26 levels 100000 97500 95000 92500 90000 85000 80000 75000 70000 65000 60000 55000 50000 45000 40000 35000 30000 25000 20000 15000 10000 7000 5000 3000 2000 1000
# profile in Pa'''

            vars='''vars 23
prc        0,  1,  0   0,  1, 10,  1 ** surface Convective Precipitation [kg/m^2]
pr         0,  1,  0   0,  1,  8,  1 ** surface Total Precipitation [kg/m^2]
prw        0,200,  0   0,  1,  3     ** entire atmosphere (considered as a single layer) Precipitable Water [kg/m^2]
prcr       0,  1,  0   0,  1,196,  0 ** surface Convective Precipitation Rate [kg/m^2/s]
prr        0,  1,  0   0,  1,  7,  0 ** surface Precipitation Rate [kg/m^2/s]
zg        26,100       0,  3,  5     ** (1000 975 950 925 900.. 70 50 30 20 10) Geopotential Height [gpm]
psl        0,101,  0   0,  3,  1     ** mean sea level Pressure Reduced to MSL [Pa]
hur       21,100       0,  1,  1     ** (1000 975 950 925 900.. 300 250 200 150 100) Relative Humidity [%%]
clt        0,200,  0   0,  6,  1,  0 ** entire atmosphere (considered as a single layer) Total Cloud Cover [%%]
cll        0,214,  0   0,  6,  1,  0 ** low cloud layer Total Cloud Cover [%%]
clm        0,224,  0   0,  6,  1,  0 ** middle cloud layer Total Cloud Cover [%%]
clh        0,234,  0   0,  6,  1,  0 ** high cloud layer Total Cloud Cover [%%]
cltc       0,244,  0   0,  6,  1     ** convective cloud layer Total Cloud Cover [%%]
tasmx      0,103,  2   0,  0,  4     ** 2 m above ground Maximum Temperature [K]
tasmn      0,103,  2   0,  0,  5     ** 2 m above ground Minimum Temperature [K]
tas        0,103,  2   0,  0,  0     ** 2 m above ground Temperature [K]
ua        26,100       0,  2,  2     ** (1000 975 950 925 900.. 70 50 30 20 10) U-Component of Wind [m/s]
uas        0,103, 10   0,  2,  2     ** 10 m above ground U-Component of Wind [m/s]
rlut       0,  8,  0   0,  5,193,  0 ** top of atmosphere Upward Long-Wave Rad. Flux [W/m^2]
va        26,100       0,  2,  3     ** (1000 975 950 925 900.. 70 50 30 20 10) V-Component of Wind [m/s]
ta        26,100       0,  0,  0     ** (1000 975 950 925 900.. 70 50 30 20 10) Temperature [K]
vas        0,103,10    0,  2,  3     ** 10 m above ground V-Component of Wind [m/s]
wap       21,100       0,  2,  8     ** (1000 975 950 925 900.. 300 250 200 150 100) Vertical Velocity (Pressure) [Pa/s]
endvars'''

        latlongrid='''xdef 720 linear   0.0 0.5
ydef 361 linear -90.0 0.5'''

        self.ctlgridvar='''undef 1e+20
title gfs2.2007100112.f006.grb2
%s
%s
%s'''%(optiondtype,latlongrid,vars)


class Goes(Gfs2):

    pltdir='plt_ncep_gfs'
    pmodel='gfs'

    def __init__(self,model='goes',center='ncep',bdir2=None,gribver=2,doLn=0):

        self.model=model
        # three possible names for the model
        self.dmodel='gfs'
        self.lmodel='gfs2'
        self.dirmodel=self.lmodel

        if(bdir2 != None): self.bdir2=bdir2
        
        self.initModelCenter(center)
        self.initGribVer(gribver)

        self.tautype='wgrib'
        self.dmodelType=None

        self.modelrestitle='T1534|L64'
        self.modelDdtg=6
        self.modelgridres='1.0'

        self.modeltitleAck1="NCEP GFS courtesy NCEP"
        self.modeltitleFullmod="NCEP(GFS)"

        self.btau=0
        self.etau=168
        self.dtau=6

        self.rundtginc=6

        self.doDATage=1
        self.doLn=doLn


    def setxwgrib(self,dtg):

        #gfs.t18z.goessimpgrb2.f180.1p0deg.grib2
        #gfs2.2012012118.f192.grb2

        self.nfields=4
        self.nfieldsW2flds=4
        hh=dtg[8:10]

        self.gribtype='grb2'
        self.xwgrib='wgrib2'
        #gfs.t06z.goessimpgrb2.1p00.f180
        if(self.doLn):
            self.dmask="%s.t%sz.goessimpgrb2.f???.1p00.grib2"%(self.dmodel,hh)
        else:
            self.dmask="%s.t%sz.goessimpgrb2.1p00.f???"%(self.dmodel,hh)

    def name2tau(self,file,dtg=None):

        ib=len(self.dmodel.split('.'))+1
        tt=file.split('.')
        if(self.doLn):
            taufield=tt[-3]
        else:
            taufield=tt[-1]
            
        try:
            tau=taufield[1:]
            tau=int(tau)
        except:
            tau=None

        return(tau)


    def setDbase(self,dtg,dtype=None):

        #gfs.t18z.goessimpgrb2.1p0deg.grib2.ctl

        self.modelcenter="%s/%s"%(self.center,self.dirmodel)
        self.bddir="%s/%s"%(self.bdir2,self.modelcenter)

        hh=dtg[8:10]
        self.dbasedir="%s/%s"%(self.bddir,dtg)
        self.dbase="%s/%s.t%sz.goessimpgrb2.1p0deg.grib2"%(self.dbasedir,self.lmodel,hh)
        self.dpath="%s.ctl"%(self.dbase)
        self.dpathexists=os.path.exists(self.dpath)
        self.tdatbase=self.dbase



class Fv3e(Gfs2):

    model='fv3e'
    center='esrl'

    sdir='/public/data/grids/fv3gfs_gsd/0p5deg/grib2'
    
    modeltitleAck1="FV3 GFS run at ESRL"
    modeltitleFullmod="ESRL(FV3.GFS)"

    adecksource='esrl'
    adeckaid='fv3e'
    
    def __init__(self,bdir2=None,verb=1):

        if(w2.onTheia):
            if(self.model == 'fv3e'):
                self.sdir='/scratch4/BMC/rtfim/rtruns/FV3GFS/FV3GFSrun/rt_fv3gfs_ff'
            elif(self.model == 'fv3g'):
                self.sdir='/scratch4/BMC/rtfim/rtruns/FV3GFS_GF/FV3GFSrun/rt_fv3gfs_gf'

        self.verb=verb
        self.gribver=2
        
        # three possible names for the model
        self.dmodel=self.model
        self.lmodel=self.model
        self.dirmodel=self.lmodel
        
        if(bdir2 != None): self.bdir2=bdir2
        
        self.initModelCenter(self.center)
        self.initGribVer(self.gribver)

        self.tautype='wgrib'
        self.dmodelType=None

        self.rundtginc=12

        self.doDATage=1

        self.centermodel='esrl/%s'%(self.model)
        self.mintauPlot=144
        self.mintauPlot=120
        
        self.nfields=352
        self.nfieldsW2flds=61

        self.btau=0
        self.etau=168
        self.etau=120
        self.dtau=6
        
        self.modelrestitle='C768 L64'
        
        self.modelDdtg=6
        self.modelgridres='0.25'
        self.modelCtlGrid='''xdef 720 linear   0.0 0.5
ydef 361 linear -90.0 0.5'''
        self.modelCtlGrid='''xdef 1440 linear   0.0 %s
ydef 721 linear -90.0 %s'''%(self.modelgridres,self.modelgridres)
        
        self.modelres=self.modelgridres.replace('.','')
        self.modelprvar="""_prvar='pr*4'"""
        # -- new version(?) with tipping the bucket every 6 h
        self.modelprvar="""_prvar='(( const(pr(t+0),0,-u)-const(pr(t-1),0,-u) )*4)'"""
        
        self.modelpslvar='psl*0.01'

        self.pmodel=self.model
        self.pltdir='plt_%s_%s'%(self.center,self.pmodel)
        
        self.modelPlotTaus=[0,6,12,18,24,30,36,42,48,60,72,84,96,108,120,132,144,156,168]
        self.modelPlotTaus=[0,6,12,18,24,30,36,42,48,60,72,84,96,108,120]
        self.gmodname="%s%s"%(self.pmodel,self.modelres)
        
        
    def setNwp2Fields(self,dtg,ropt='',override=0):

        tdirbase="%s/%s"%(w2.Nwp2DataBdir,self.centermodel)
        tdir="%s/%s"%(tdirbase,dtg)
        omodel=self.model
        
        yymm=dtg[0:6]
        yymmdd=dtg[0:8]
        yy=dtg[2:4]
        mmddhh=dtg[4:10]
        hh=dtg[8:10]

        julday=int(mf.Dtg2JulianDay(dtg))
        
        smask="%2s%03d%2s*"%(yy,julday,hh)
        if(w2.onTheia):
            smask="gfs.t%sz.pgrb2.0p50.f*"%(hh)
            self.sdir="%s/gfs.%s/%s"%(self.sdir,yymmdd,hh)


        nfiles=len(glob.glob("%s/%s.*.grb*"%(tdir,omodel)))

        mf.ChkDir(tdir,'mk')
        ctlpath="%s/%s.%s.ctl"%(tdir,omodel,dtg)
        gmpfile="%s.%s.gmp2"%(self.model,dtg)
        gmppath="%s/%s"%(tdir,gmpfile)
        
        source='public'

        self.tdir=tdir
        self.ctlpath=ctlpath
        self.gmpfile=gmpfile
        self.gmppath=gmppath
        self.source=source

        # -- SSSSS -- source
        
        modelmask="%s/%s"%(self.sdir,smask)
        modelfiles=glob.glob(modelmask)
        omodelfiles=[]

        modelfiles.sort()

        btau=self.btau
        etau=self.etau
        dtau=self.dtau
        taus=range(btau,etau+1,dtau)

        for mfile in modelfiles:
            (fdir,ffile)=os.path.split(mfile)
            if(w2.onTheia): mtau=int(ffile[-3:])
            else:           mtau=int(ffile[-4:])

            if(mtau in taus):
                omodelfiles.append(mfile)
                
        modelfiles=omodelfiles
        modelfiles.sort()
        
        nfiles=len(modelfiles)

        if(self.verb and nfiles > 0):
            print 'SSSSSSSSSSSSSS modelfiles modelmask: ',modelmask
            for mfile in modelfiles:
                print mfile
                
        if(nfiles == 0):
            print 'WWW no model files for dtg: ',dtg,' model: ',self.model
            self.sdir=None
            return

        localmodelfiles=[]
        
        # -- TTTTT - set up symbolic link if from public
        #
        mtaus=[]
        for modelfile in modelfiles:

            lm=len(modelfile)

            ctau=modelfile[lm-3:lm]
            (mdir,mfile)=os.path.split(modelfile)
            lmfile="%s.%s.f%s.grb%d"%(omodel,dtg,ctau,self.gribver)
            localmodelfile="%s/%s"%(tdir,lmfile)
            mtaus.append(int(ctau))

            if(not(os.path.exists(localmodelfile)) or override):
                cmd="ln -s -f %s %s"%(modelfile,localmodelfile)
                mf.runcmd(cmd,ropt)
            
            localmodelfiles.append(localmodelfile)
                
        localmodelfiles.sort()
        mtaus.sort()
        
        self.localmodelfiles=localmodelfiles
        
        if(self.verb):
            print 'LLLLL localmodel files:'
            for lmf in localmodelfiles:
                print lmf
                
        # -- make the ctlfile
        #
        gtime=mf.dtg2gtime(dtg)
        dtctl=self.dtau
        ntlast=mtaus[-1]
        nt=ntlast/dtctl + 1
        
        ctl="""dset ^%s.%s.f%%f3.grb%d
index ^%s
undef 1e+20
title based on gfs2.2007100112.f006.grb2
options template pascals
dtype grib2
%s
zdef 26 levels 100000 97500 95000 92500 90000 85000 80000 75000 70000 65000 60000 55000 50000 45000 40000 35000 30000 25000 20000 15000 10000 7000 5000 3000 2000 1000
tdef %d linear %s %dhr
vars 24
ts         0,  1  ,0   0,  0,  0     ** surface Temperature [K]
prc        0,  1,  0   0,  1, 10,  1 ** surface Convective Precipitation [kg/m^2]
pr         0,  1,  0   0,  1,  8,  1 ** surface Total Precipitation [kg/m^2]
prw        0,200,  0   0,  1,  3     ** entire atmosphere (considered as a single layer) Precipitable Water [kg/m^2]
prcr       0,  1,  0   0,  1,196,  0 ** surface Convective Precipitation Rate [kg/m^2/s]
prr        0,  1,  0   0,  1,  7,  0 ** surface Precipitation Rate [kg/m^2/s]
zg        26,100       0,  3,  5     ** (1000 975 950 925 900.. 70 50 30 20 10) Geopotential Height [gpm]
psl        0,101,  0   0,  3,192     ** mean sea level MSLP (Eta model reduction) [Pa]
hur       21,100       0,  1,  1     ** (1000 975 950 925 900.. 300 250 200 150 100) Relative Humidity [%%]
clt        0,200,  0   0,  6,  1,  0 ** entire atmosphere (considered as a single layer) Total Cloud Cover [%%]
cll        0,214,  0   0,  6,  1,  0 ** low cloud layer Total Cloud Cover [%%]
clm        0,224,  0   0,  6,  1,  0 ** middle cloud layer Total Cloud Cover [%%]
clh        0,234,  0   0,  6,  1,  0 ** high cloud layer Total Cloud Cover [%%]
cltc       0,244,  0   0,  6,  1     ** convective cloud layer Total Cloud Cover [%%]
tasmx      0,103,  2   0,  0,  4     ** 2 m above ground Maximum Temperature [K]
tasmn      0,103,  2   0,  0,  5     ** 2 m above ground Minimum Temperature [K]
tas        0,103,  2   0,  0,  0     ** 2 m above ground Temperature [K]
ua        26,100       0,  2,  2     ** (1000 975 950 925 900.. 70 50 30 20 10) U-Component of Wind [m/s]
uas        0,103, 10   0,  2,  2     ** 10 m above ground U-Component of Wind [m/s]
rlut       0,  8,  0   0,  5,193,  0 ** top of atmosphere Upward Long-Wave Rad. Flux [W/m^2]
va        26,100       0,  2,  3     ** (1000 975 950 925 900.. 70 50 30 20 10) V-Component of Wind [m/s]
ta        26,100       0,  0,  0     ** (1000 975 950 925 900.. 70 50 30 20 10) Temperature [K]
vas        0,103,10    0,  2,  3     ** 10 m above ground V-Component of Wind [m/s]
wap       21,100       0,  2,  8     ** (1000 975 950 925 900.. 300 250 200 150 100) Vertical Velocity (Pressure) [Pa/s]
endvars"""%(self.model,dtg,self.gribver,self.gmpfile,self.modelCtlGrid,
            nt,gtime,dtctl)
        
        if(MF.getPathSiz(self.ctlpath) <= 0 or override):
            MF.WriteCtl(ctl, self.ctlpath, verb=self.verb)
        
        if(MF.getPathSiz(self.gmppath) <= 0 or override):
            cmd='gribmap -v -i %s'%(self.ctlpath)
            mf.runcmd(cmd,ropt)


    def setxwgrib(self,dtg):

        self.gribtype='grb2'
        self.xwgrib='wgrib2'
        self.dmask="%s.%s.f???.grb2"%(self.dmodel,dtg)
        self.dsetmask="%s.%s.f%%f3.grb2"%(self.dmodel,dtg)


class Fv7e(Fv3e):

    model='fv7e'
    center='esrl'

    sdir='/public/data/grids/fv3gfs_gsd_c768/0p25deg/grib2'
    
    modeltitleAck1="C768 FV3 GFS run at ESRL"
    modeltitleFullmod="C768 ESRL(FV3.GFS)"

    adecksource='esrl'
    adeckaid='fv7e'
    
    def __init__(self,bdir2=None,verb=1):


        # -- if on jet --
        #
        if(w2.onWjet):
            if(self.model == 'fv7e'):
                self.sdir='/lfs3/projects/gsd-fv3-hfip/rtruns/FV3GFS_C768/FV3GFSrun/rt_fv3gfs_ff_c768/'
            elif(self.model == 'fv7g'):
                self.sdir='/lfs3/projects/gsd-fv3-hfip/rtruns/FV3GFS_GF_C768/FV3GFSrun/rt_fv3gfs_gf_c768/'
                
            
        self.verb=verb
        self.gribver=2
        
        # three possible names for the model
        self.dmodel=self.model
        self.lmodel=self.model
        self.dirmodel=self.lmodel

        if(bdir2 != None): self.bdir2=bdir2
        
        self.initModelCenter(self.center)
        self.initGribVer(self.gribver)

        self.tautype='wgrib'
        self.dmodelType=None

        self.rundtginc=12

        self.doDATage=1

        self.centermodel='esrl/%s'%(self.model)
        self.mintauPlot=144
        
        self.nfields=352
        self.nfieldsW2flds=61

        self.btau=0
        self.etau=168
        self.dtau=6
        
        self.modelrestitle='N768 L64'
        
        self.modelDdtg=6
        self.modelgridres='0.25'
        self.modelCtlGrid='''xdef 1440 linear   0.0 0.25
ydef 721 linear -90.0 0.25'''

        self.modelres=self.modelgridres.replace('.','')
        self.modelprvar="""_prvar='pr*4'"""
        # -- new version(?) with tipping the bucket every 6 h
        self.modelprvar="""_prvar='(( const(pr(t+0),0,-u)-const(pr(t-1),0,-u) )*4)'"""
        
        self.modelpslvar='psl*0.01'

        self.pmodel=self.model
        self.pltdir='plt_%s_%s'%(self.center,self.pmodel)

        self.modelPlotTaus=[0,6,12,18,24,30,36,42,48,60,72,84,96,108,120,132,144,156,168]
        self.gmodname="%s%s"%(self.pmodel,self.modelres)
        

    def setNwp2Fields(self,dtg,ropt='',override=0):

        tdirbase="%s/%s"%(w2.Nwp2DataBdir,self.centermodel)
        tdir="%s/%s"%(tdirbase,dtg)
        omodel=self.model
        
        yymm=dtg[0:6]
        yymmdd=dtg[0:8]
        yy=dtg[2:4]
        mmddhh=dtg[4:10]
        hh=dtg[8:10]

        julday=int(mf.Dtg2JulianDay(dtg))

        smask="%2s%03d%2s*"%(yy,julday,hh)
        if(w2.onWjet):
            #smask="%2s%03d%2s*.g2"%(yy,julday,hh)
            #self.sdir="%s/gfs.%s/%s/post/fim"%(self.sdir,yymmdd,hh)
            smask="gfs.t%sz.pgrb2.0p25.f*"%(hh)
            self.sdir="%s/gfs.%s/%s"%(self.sdir,yymmdd,hh)

#/lfs3/projects/gsd-fv3-hfip/rtruns/FV3GFS_C768/FV3GFSrun/rt_fv3gfs_ff_c768//gfs.20180819/00/gfs.t00z.pgrb2.0p25.f000
        nfiles=len(glob.glob("%s/%s.*.grb*"%(tdir,omodel)))

        mf.ChkDir(tdir,'mk')
        ctlpath="%s/%s.%s.ctl"%(tdir,omodel,dtg)
        gmpfile="%s.%s.gmp2"%(self.model,dtg)
        gmppath="%s/%s"%(tdir,gmpfile)
        
        source='public'

        self.tdir=tdir
        self.ctlpath=ctlpath
        self.gmpfile=gmpfile
        self.gmppath=gmppath
        self.source=source

        # -- SSSSS -- source
        
        modelmask="%s/%s"%(self.sdir,smask)
        modelfiles=glob.glob(modelmask)
        omodelfiles=[]

        modelfiles.sort()

        btau=self.btau
        etau=self.etau
        dtau=self.dtau
        taus=range(btau,etau+1,dtau)

        for mfile in modelfiles:
            (fdir,ffile)=os.path.split(mfile)
            if(w2.onWjet): mtau=int(ffile[-3:])
            else:           mtau=int(ffile[-4:])
            if(mtau in taus):
                omodelfiles.append(mfile)
                
        modelfiles=omodelfiles
        modelfiles.sort()
        
        nfiles=len(modelfiles)

        if(self.verb and nfiles > 0):
            print 'SSSSSSSSSSSSSS modelfiles modelmask: ',modelmask
            for mfile in modelfiles:
                print mfile
                
        if(nfiles == 0):
            print 'WWW no model files for dtg: ',dtg,' model: ',self.model
            self.sdir=None
            return

        localmodelfiles=[]
        
        # -- TTTTT - set up symbolic link if from public
        #
        mtaus=[]
        for modelfile in modelfiles:
            imodelfile=modelfile

            lm=len(modelfile)

            ctau=modelfile[lm-3:lm]
            (mdir,mfile)=os.path.split(modelfile)
            lmfile="%s.%s.f%s.grb%d"%(omodel,dtg,ctau,self.gribver)
            localmodelfile="%s/%s"%(tdir,lmfile)
            mtaus.append(int(ctau))

            if(not(os.path.exists(localmodelfile)) or override):
                cmd="ln -s -f %s %s"%(imodelfile,localmodelfile)
                mf.runcmd(cmd,ropt)
            
            localmodelfiles.append(localmodelfile)
                
        localmodelfiles.sort()
        mtaus.sort()
        
        self.localmodelfiles=localmodelfiles
        
        if(self.verb):
            print 'LLLLL localmodel files:'
            for lmf in localmodelfiles:
                print lmf
                
        # -- make the ctlfile
        #
        gtime=mf.dtg2gtime(dtg)
        dtctl=self.dtau
        ntlast=mtaus[-1]
        nt=ntlast/dtctl + 1
        
        ctl="""dset ^%s.%s.f%%f3.grb%d
index ^%s
undef 1e+20
title based on gfs2.2007100112.f006.grb2
options template pascals
dtype grib2
%s
zdef 26 levels 100000 97500 95000 92500 90000 85000 80000 75000 70000 65000 60000 55000 50000 45000 40000 35000 30000 25000 20000 15000 10000 7000 5000 3000 2000 1000
tdef %d linear %s %dhr
vars 24
ts         0,  1  ,0   0,  0,  0     ** surface Temperature [K]
prc        0,  1,  0   0,  1, 10,  1 ** surface Convective Precipitation [kg/m^2]
pr         0,  1,  0   0,  1,  8,  1 ** surface Total Precipitation [kg/m^2]
prw        0,200,  0   0,  1,  3     ** entire atmosphere (considered as a single layer) Precipitable Water [kg/m^2]
prcr       0,  1,  0   0,  1,196,  0 ** surface Convective Precipitation Rate [kg/m^2/s]
prr        0,  1,  0   0,  1,  7,  0 ** surface Precipitation Rate [kg/m^2/s]
zg        26,100       0,  3,  5     ** (1000 975 950 925 900.. 70 50 30 20 10) Geopotential Height [gpm]
psl        0,101,  0   0,  3,192     ** mean sea level MSLP (Eta model reduction) [Pa]
hur       21,100       0,  1,  1     ** (1000 975 950 925 900.. 300 250 200 150 100) Relative Humidity [%%]
clt        0,200,  0   0,  6,  1,  0 ** entire atmosphere (considered as a single layer) Total Cloud Cover [%%]
cll        0,214,  0   0,  6,  1,  0 ** low cloud layer Total Cloud Cover [%%]
clm        0,224,  0   0,  6,  1,  0 ** middle cloud layer Total Cloud Cover [%%]
clh        0,234,  0   0,  6,  1,  0 ** high cloud layer Total Cloud Cover [%%]
cltc       0,244,  0   0,  6,  1     ** convective cloud layer Total Cloud Cover [%%]
tasmx      0,103,  2   0,  0,  4     ** 2 m above ground Maximum Temperature [K]
tasmn      0,103,  2   0,  0,  5     ** 2 m above ground Minimum Temperature [K]
tas        0,103,  2   0,  0,  0     ** 2 m above ground Temperature [K]
ua        26,100       0,  2,  2     ** (1000 975 950 925 900.. 70 50 30 20 10) U-Component of Wind [m/s]
uas        0,103, 10   0,  2,  2     ** 10 m above ground U-Component of Wind [m/s]
rlut       0,  8,  0   0,  5,193,  0 ** top of atmosphere Upward Long-Wave Rad. Flux [W/m^2]
va        26,100       0,  2,  3     ** (1000 975 950 925 900.. 70 50 30 20 10) V-Component of Wind [m/s]
ta        26,100       0,  0,  0     ** (1000 975 950 925 900.. 70 50 30 20 10) Temperature [K]
vas        0,103,10    0,  2,  3     ** 10 m above ground V-Component of Wind [m/s]
wap       21,100       0,  2,  8     ** (1000 975 950 925 900.. 300 250 200 150 100) Vertical Velocity (Pressure) [Pa/s]
endvars"""%(self.model,dtg,self.gribver,self.gmpfile,self.modelCtlGrid,
            nt,gtime,dtctl)
        
        if(MF.getPathSiz(self.ctlpath) <= 0 or override):
            MF.WriteCtl(ctl, self.ctlpath, verb=self.verb)
        
        if(MF.getPathSiz(self.gmppath) <= 0 or override):
            cmd='gribmap -v -i %s'%(self.ctlpath)
            mf.runcmd(cmd,ropt)



class Fv7g(Fv7e):

    model='fv7g'
    center='esrl'

    sdir='/public/data/grids/fv3gfs_gf_gsd_c768/0p25deg/grib2'
    
    modeltitleAck1="C768 FV3 GFS - GF Physics run at ESRL"
    modeltitleFullmod="C768 ESRL(FV3.GF)"

    adecksource='esrl'
    adeckaid='fv7e'



class Fv3g(Fv3e):

    model='fv3g'
    center='esrl'

    sdir='/public/data/grids/fv3gfs_gf_gsd/0p5deg/grib2'
    
    modeltitleAck1="FV3 GFS - GF Physics run at ESRL"
    modeltitleFullmod="ESRL(FV3.GF)"

    adecksource='esrl'
    adeckaid='fv3g'


class Hwrf(Gfs2):
    
    btau=0
    # -- only goes to tau 192 on /public/data/grids/gfs/0p5deg/grib2/13JJJ
    etau=126
    dtau=6

    modelrestitle='T574|N286 L64'
    modelDdtg=6
    modelgridres='0.5'
    modelres=modelgridres.replace('.','')
    modelprvar="""_prvar='pr*4'"""
    modelpslvar='psl*0.01'

    model='hwrf'
    center='ncep'

    pltdir='plt_ncep_gfs'
    pmodel='hwrf'

    modelPlotTaus=[0,6,12,18,24,30,36,42,48,60,72,84,96,108,120]
    gmodname="%s%s"%(pmodel,modelres)

    modeltitleAck1="NCEP GFS courtesy ESRL/GSD/ITS"
    modeltitleFullmod="NCEP(GFS)"


    def __init__(self,bdir2=None,gribver=2):

        # three possible names for the model
        self.dmodel=self.model
        self.dirmodel=self.model

        if(bdir2 != None): self.bdir2=bdir2
        
        self.initModelCenter(self.center)
        self.initGribVer(gribver)

        self.tautype='wgrib'

        self.adecksource='ncep'
        self.adeckaid='hwrf'

        self.rundtginc=6

        self.nfields=344
        self.nfieldsW2flds=67

    def setxwgrib(self,dtg):

        self.nfields=999
        self.nfieldsW2flds=64
        
        self.gribtype='grb2'
        self.xwgrib='wgrib2'
        self.dmask="*.%s.f???.%s"%(dtg,self.gribtype)
        self.dsetmask="*.%s.f%%f3.%s"%(dtg,self.gribtype)



class GfsR(Gfs2):


    d2dir='/dat3/reforecast/2005/200508/2005082500/gaussian/c00'
    archdir=d2dir

    pltdir='plt_ncep_gfsr'
    pmodel='gfsr'

    def __init__(self,model='gfsr',center='esrl',gribver=1):

        self.model=model
        self.dmodel=self.model
        self.dirmodel=self.model

        self.initModelCenter(center)
        self.initGribVer(gribver)

        self.tautype='wgrib'

        self.modelrestitle='T382|N286 L64'
        self.modelDdtg=6
        self.modelgridres='0.5'
        self.modelprvar="""_prvar='pr*4'"""
        self.modelpslvar='psl*0.01'

        self.modeltitleAck1="ESRL GFS(EnKF) courtesy ESRL/GSD/AMB"
        self.modeltitleFullmod="ESRL(GFSR)"

        self.btau=0
        self.etau=168
        self.dtau=6

        self.rundtginc=6

        self.adecksource='esrl'
        self.adeckaid='gfsr'

        self.nfields=396
        self.nfieldsW2flds=61


    def setxwgrib(self,dtg):


        self.gribtype='grb1'
        self.xwgrib='wgrib'
        self.dmask="%s.%s.f???.grb1"%(self.dmodel,dtg)
        self.dsetmask="%s.%s.f%%f3.grb1"%(self.dmodel,dtg)



class Gfr1(GfsR):


    pltdir='plt_ncep_gfr1'
    pmodel='gfr1'

    d2dir='/dat3/reforecast/2005/200508/2005082500/latlon/c00'
    archdir=d2dir

    def __init__(self,model='gfsr',center='esrl',gribver=1):

        self.model=model
        self.dmodel=self.model
        self.dirmodel=self.model

        self.initModelCenter(center)
        self.initGribVer(gribver)

        self.tautype='wgrib'

        self.modelrestitle='T382|N286 L64'
        self.modelDdtg=6
        self.modelgridres='0.5'
        self.modelprvar="""_prvar='pr*4'"""
        self.modelpslvar='psl*0.01'

        self.modeltitleAck1="ESRL GFS(EnKF) courtesy ESRL/GSD/AMB"
        self.modeltitleFullmod="ESRL(GFSR)"

        self.btau=0
        self.etau=168
        self.dtau=6

        self.rundtginc=6

        self.adecksource='esrl'
        self.adeckaid='gfsr'

        self.nfields=396
        self.nfieldsW2flds=61


    def setxwgrib(self,dtg):


        self.gribtype='grb1'
        self.xwgrib='wgrib'
        self.dmask="%s.%s.f???.grb1"%(self.dmodel,dtg)
        self.dsetmask="%s.%s.f%%f3.grb1"%(self.dmodel,dtg)



class GfsK(Gfs2):

    pltdir='plt_ncep_gfsk'
    pmodel='gfsk'

    d2dir='/lfs2/projects/fim/fiorino/w21/dat/nwp2'
    archdir=d2dir

    def __init__(self,model='gfsk',center='esrl',gribver=1):

        self.model=model
        self.dmodel=self.model
        self.dirmodel=self.model

        self.initModelCenter(center)
        self.initGribVer(gribver)

        self.tautype='wgrib'

        self.modelrestitle='T382|N286 L64'
        self.modelDdtg=6
        self.modelgridres='0.5'
        self.modelprvar="""_prvar='pr*4'"""
        self.modelpslvar='psl*0.01'

        self.modeltitleAck1="ESRL GFS(EnKF) courtesy ESRL/GSD/AMB"
        self.modeltitleFullmod="ESRL(GFSK)"

        self.btau=0
        self.etau=168
        self.dtau=6

        self.rundtginc=6

        self.adecksource='esrl'
        self.adeckaid='gfsk'


    def setxwgrib(self,dtg):

        self.nfields=396
        self.nfieldsW2flds=61

        self.gribtype='grb1'
        self.xwgrib='wgrib'
        self.dmask="%s.%s.f???.grb1"%(self.dmodel,dtg)
        self.dsetmask="%s.%s.f%%f3.grb1"%(self.dmodel,dtg)


class Era5(Model2):

    modelrestitle='T`bl`n|N400 L91'
    modelDdtg=12
    modelgridres='0.5'
    modelres=modelgridres.replace('.','')

    modelZgVar='zg/%f'%(gravity)
    modelpslvar='psl*0.01'
    modeltitleAck1="ECMWF Data Courtesy of ERA project"
    modeltitleFullmod="ECMWF(ERA5)"

    model='era5'
    center='ecmwf'

    dmodel='era5'
    pmodel='er5'

    pltdir='plt_ecmwf_%s'%(pmodel)

    modelPlotTaus=[0,6,12,18,24,30,36,42,48,60,72,84,96,108,120,132,144,156,168]
    gmodname="%s%s"%(pmodel,modelres)
    regridTracker=0.5


    def __init__(self,bdir2=None,gribver=2):

        self.dirmodel=self.dmodel

        if(bdir2 != None): self.bdir2=bdir2
        
        self.initModelCenter(self.center)
        self.initGribVer(gribver)

        self.location='wxmap2'

        self.tautype='alltau'
        self.gribtype='grb2'

        self.nfields=94
        self.nfieldsW2flds=66

        self.tbase=self.dmodel

        self.etau=240
        self.dtau=6

        self.rundtginc=12

        self.adecksource='ecmwf'
        self.adeckaid='era5'
        self.tryarch=0
        
    def name2tau(self,ffile,dtg):
        tau=240
        return(tau)

    def setDbase(self,dtg,dtype='w2flds',warn=0):

        if(self.IsModel2(self.model) or self.IsModel1(self.model)):
            if(not(hasattr(self,'lmodel'))): self.lmodel=self.dmodel

            if(dtype == 'w2flds'):
                self.dmodel=self.model
                self.lmodel=self.model
                
            self.dbasedir="%s/%s"%(self.bddir,dtg)
            self.dbasedirarch="%s/%s"%(self.bddirarch,dtg)

            byear=dtg[0:4]
            self.bddir="%s/%s"%(self.w2fldsSrcDir,byear)
            self.useBddir=1
            self.dbasedir="%s/%s/"%(self.bddir,dtg)
            self.dbase="%s/%s/%s-%s-%s-ua"%(self.bddir,dtg,self.lmodel,dtype,dtg)
            self.dmask="%s-%s-%s-ua.%s"%(self.lmodel,dtype,dtg,self.gribtype)

            self.dpath="%s.ctl"%(self.dbase)

            self.dpathexists=os.path.exists(self.dpath)

            # -- try dat5
            #
            if(not(self.dpathexists) and self.tryarch):
                if(warn): print 'IIIIIIIIIIIIIIIIIIIIIIIIIIIIII M2.Model2.setDbase tryarch=1 -- trying the archive on: ',self.dbasedirarch,self.dtype
                self.dbasedir=self.dbasedirarch
                if(self.dtype == 'w2flds'):
                    self.bddir=self.w2fldsArchDir
                    self.dbasedir="%s/%s"%(self.bddir,dtg)
                    self.dbase="%s/%s.%s.%s"%(self.dbasedir,self.lmodel,dtype,dtg)
                    self.dmask="%s.%s.%s.f???.%s"%(self.lmodel,dtype,dtg,self.gribtype)
                    
                    self.dpath="%s.ctl"%(self.dbase)
                    self.dpathexists=os.path.exists(self.dpath)
            
        else:
            print 'EEE-M2.Era5.setDbase could not set M2.setDbase.dbase  model: ',self.model,'dtg: ',dtg,' dtype: ',self.dtype,' or maybe because model not in w2localvars.py Nwp2ModelsAll...'
            sys.exit()

        self.tdatbase=self.dbase

    def GetDataStatus(self,dtg,checkNF=0,mintauNF=5):

        if(hasattr(self,'bddirNWP2')):
            tdir="%s/%s"%(self.bddirNWP2,dtg)
        else:
            tdir="%s/%s"%(self.bddir,dtg)

        NFmin=self.nfields
        if(checkNF): NFmin=self.nfields-mintauNF

        lastTau=None
        latestTau=None
        latestCompleteTau=None
        earlyTau=None
        gmpAge=None
        gmplastdogribmap=-999
        gmplatestTau=-999
        gmplastTau=-999

        datataus=w2.Model2DataTaus(self.model,dtg)
        
        # -- for single tau in era5/ecm5 ... get the age from the single data file
        #
        stat=self.statuss[dtg]
        itaus=stat.keys()
        
        if(len(itaus) == 1):
            itau=itaus[0]
            (age,siz)=stat[itau]
        else:
            age=-999
            siz=-999
        
        for tau in datataus:
            nf=self.nfieldsW2flds
            self.statuss[dtg][tau]=(age,nf)
        
        status=self.statuss[dtg]
        itaus=status.keys()
        itaus.sort()
        
        ages={}
        for itau in itaus:
            ages[itau]=status[itau][0]


        oldest=-1e20
        youngest=+1e20

        for itau in itaus:
            if(ages[itau] < youngest):
                youngest=ages[itau]
                earlyTau=itau

            # -- >= because for taus having the same age
            #
            if(ages[itau] >= oldest):
                oldest=ages[itau]
                latestTau=itau

        if(len(status) >= 1):
            lastTau=itaus[-1]
            latestCompleteTau=lastTau


        # -- forward search thru target data taus
        # 

        ndt=len(datataus)

        if(self.tautype == 'alltau'):
            latestCompleteTau=datataus[-1]
            
        else:
            for n in range(0,ndt):
                datatau=datataus[n]
                gotit=0
                for itau in itaus:
                    if(datatau == itau):
                        (age,nf)=self.statuss[dtg][itau]
                        if(checkNF and nf < NFmin):
                            gotit=0
                            continue
                        else:
                            gotit=1
                            latestCompleteTau=datatau
                        break
    
    
                if(gotit == 0):  break


        # -- backward search (default)
        #

        latestCompleteTauBackward=-999

        if(self.tautype == 'alltau' and self.dmodelType == None):
            None
        else:
            for n in range(ndt-1,0,-1):
                datatau=datataus[n]
                gotit=0
                for itau in itaus[-1:0:-1]:
                    if(datatau == itau):
                        (age,nf)=self.statuss[dtg][itau]
                        if(checkNF and nf < NFmin):
                            gotit=0
                            continue
                        else:
                            gotit=1
                            latestCompleteTauBackward=datatau
                        break
        
                if(gotit == 1):  break
        
        self.dstdir=tdir
        self.dsitaus=itaus
        self.dslastTau=lastTau
        self.dsgmpAge=gmpAge
        self.dsoldestTauAge=oldest
        self.dslatestTau=latestTau
        self.dsyoungest=youngest
        self.dsearlyTau=earlyTau
        self.dsgmplastdogribmap=gmplastdogribmap
        self.dsgmplatestTau=gmplatestTau
        self.dsgmplastTau=gmplastTau
        self.dslatestCompleteTau=latestCompleteTau
        self.dslatestCompleteTauBackward=latestCompleteTauBackward

        return(self)

    def getDataTaus(self,dtg):
        taus=range(0,120+1,6)+range(132,240+1,12)
        return(taus)


    # -- set prvar method to set dependence on tau
    #
    def setprvar(self,dtg=None,tau=None):
        modelprvar=self.modelprvar
        if(tau >= 0 and tau <= 120):
            modelprvar="""_prvar='(( const(pr(t+1),0,-u)-const(pr(t-0),0,-u) )*4)'"""
        elif(tau > 120):
            modelprvar="""_prvar='(( const(pr(t+2),0,-u)-const(pr(t-0),0,-u) )*2)'"""
            
        return(modelprvar)


    def setMaxtau(self,dtg):
        hh=dtg[8:10]
        if(hh == '00' or hh == '12'):  self.maxtau=240
        else:    self.maxtau=-999
        return(self.maxtau)

    def setgmask(self,dtg):
        self.gmask="era5-w2flds-%s-ua*"%(dtg)


    def setxwgrib(self,dtg):

        self.xwgrib='wgrib2'
        self.dmask="%s-w2flds-%s-ua.%s"%(self.dmodel,dtg,self.gribtype)


    def setctlgridvar(self,dtg):

        latlongrid='''xdef 360 linear   0.0 1.0
ydef 181 linear -90.0 1.0'''

        if(self.gribtype == 'grb1'):
            optiondtype='''options yrev template
dtype grib
zdef 14 levels 1000 925 850 700 500 400 300 250 200 150 100 50 20 10'''

        elif(self.gribtype == 'grb2'):
            optiondtype='''options yrev template pascals
dtype grib2'''


        self.ctlgridvar='''undef 9.999E+20
title ecmo 1deg deterministic run
*  produced by grib2ctl v0.9.12.5p16
%s
%s
vars 19
sic       0  31,1,0  ** Sea-ice cover [(0-1)]
sst       0  34,1,0  ** Sea surface temperature [K]
uas       0 165,1,0  ** 10 metre u wind component m s**-1
vas       0 166,1,0  ** 10 metre v wind component m s**-1
tads      0 168,1,0  ** 2 metre dewpoint temperature K
tas       0 167,1,0  ** 2 metre temperature K
zg       14 156,100,0 ** Height (geopotential) m
psln      0 152,109,1  ** Log surface pressure -
tmin      0 202,1,0  ** Min 2m temp since previous post-processing K
psl       0 151,1,0  ** Mean sea level pressure Pa
tmax      0 201,1,0  ** Max 2m temp since previous post-processing K
hur      14 157,100,0 ** Relative humidity %%
ta       14 130,100,0 ** Temperature K
clt       0 164,1,0  ** Total cloud cover (0 - 1)
pr        0 228,1,0  ** Total precipitation m
prl       0 142,1,0  ** large-scale precipitation m
prc       0 143,1,0  ** convective precipitation m
ua       14 131,100,0 ** U-velocity m s**-1
va       14 132,100,0 ** V-velocity m s**-1
endvars'''%(optiondtype,latlongrid)


        allvarsnew='''vars 30
10FGsfc  0 49,1,0  ** Wind gust at 10 metres [m s**-1]
10Usfc  0 165,1,0  ** 10 metre U wind component [m s**-1]
10Vsfc  0 166,1,0  ** 10 metre V wind component [m s**-1]
2Dsfc  0 168,1,0  ** 2 metre dewpoint temperature [K]
2Tsfc  0 167,1,0  ** 2 metre temperature [K]
BLHsfc  0 159,1,0  ** Boundary layer height [m]
CAPEsfc  0 59,1,0  ** Convective available potential energy [J kg**-1]
CIsfc  0 31,1,0  ** Sea-ice cover [(0-1)]
CPsfc  0 143,1,0  ** Convective precipitation [m]
GHprs 14 156,100,0 ** Height [m]
LNSPhbl  0 152,109,1  ** Logarithm of surface pressure
LSPsfc  0 142,1,0  ** Stratiform precipitation [m]
MN2Tsfc  0 202,1,0  ** Minimum 2 metre temperature since previous post-processing [K]
MSLsfc  0 151,1,0  ** Mean sea-level pressure [Pa]
MX2Tsfc  0 201,1,0  ** Maximum 2 metre temperature since previous post-processing [K]
Rprs 14 157,100,0 ** Relative humidity [%]
SFsfc  0 144,1,0  ** Snowfall (convective + stratiform) [m of water equivalent]
SPhbl  0 134,109,1  ** Surface pressure [Pa]
SSTKsfc  0 34,1,0  ** Sea surface temperature [K]
Tprs 14 130,100,0 ** Temperature [K]
TCCsfc  0 164,1,0  ** Total cloud cover [(0 - 1)]
TCWsfc  0 136,1,0  ** Total column water [kg m**-2]
TPsfc  0 228,1,0  ** Total precipitation [m]
TTRsfc  0 179,1,0  ** Top thermal radiation [W m**-2 s]
Uprs 14 131,100,0 ** U velocity [m s**-1]
Vprs 14 132,100,0 ** V velocity [m s**-1]
Wprs  0 135,100,700  ** Vertical velocity [Pa s**-1]
var121sfc  0 121,1,0  ** undefined
var122sfc  0 122,1,0  ** undefined
var123sfc  0 123,1,0  ** undefined'''

        allvarsold='''vars 15
10Usfc  0 165,1,0  ** 10 metre U wind component [m s**-1]
10Vsfc  0 166,1,0  ** 10 metre V wind component [m s**-1]
2Dsfc  0 168,1,0  ** 2 metre dewpoint temperature [K]
2Tsfc  0 167,1,0  ** 2 metre temperature [K]
GHprs 14 156,100,0 ** Height [m]
LNSPhbl  0 152,109,1  ** Logarithm of surface pressure
MN2Tsfc  0 202,1,0  ** Minimum 2 metre temperature since previous post-processing [K]
MSLsfc  0 151,1,0  ** Mean sea-level pressure [Pa]
MX2Tsfc  0 201,1,0  ** Maximum 2 metre temperature since previous post-processing [K]
Rprs 14 157,100,0 ** Relative humidity [%]
Tprs 14 130,100,0 ** Temperature [K]
TCCsfc  0 164,1,0  ** Total cloud cover [(0 - 1)]
TPsfc  0 228,1,0  ** Total precipitation [m]
Uprs 14 131,100,0 ** U velocity [m s**-1]
Vprs 14 132,100,0 ** V velocity [m s**-1]'''




class Ecm5(Era5):

    modelrestitle='T`bo1n1279L137'
    modelDdtg=12
    modelgridres='0.25'
    modelres=modelgridres.replace('.','')

    modelpslvar='psl*0.01'
    modelZgVar='zg/%f'%(gravity)
    modeltitleAck1="ECMWF Data Courtesy of ERA project"
    modeltitleFullmod="ECMWF(HRES)"

    model='ecm5'
    center='ecmwf'

    dmodel='ecm5'
    pmodel='ecm'

    pltdir='plt_ecmwf_%s'%(pmodel)

    modelPlotTaus=[0,6,12,18,24,30,36,42,48,60,72,84,96,108,120,132,144,156,168]
    gmodname="%s%s"%(pmodel,modelres)

    regridTracker=0.25

    def __init__(self,bdir2=None,gribver=2):

        self.dirmodel=self.dmodel

        if(bdir2 != None): self.bdir2=bdir2
        
        self.initModelCenter(self.center)
        self.initGribVer(gribver)

        self.location='wxmap2'

        self.tautype='alltau'
        self.gribtype='grb2'

        self.nfields=94
        self.nfieldsW2flds=66

        self.tbase=self.dmodel

        self.etau=240
        self.dtau=6

        self.rundtginc=12

        self.adecksource='ecmwf'
        self.adeckaid='ecm5'
        self.tryarch=0
        
    def name2tau(self,ffile,dtg):
        tau=240
        return(tau)

    def setDbase(self,dtg,dtype='w2flds',warn=0):

        if(self.IsModel2(self.model) or self.IsModel1(self.model)):
            if(not(hasattr(self,'lmodel'))): self.lmodel=self.dmodel

            if(dtype == 'w2flds'):
                self.dmodel=self.model
                self.lmodel=self.model

            self.dbasedir="%s/%s"%(self.bddir,dtg)
            self.dbasedirarch="%s/%s"%(self.bddirarch,dtg)

            byear=dtg[0:4]
            self.bddir="%s/%s"%(self.w2fldsSrcDir,byear)
            self.useBddir=1
            self.dbasedir="%s/%s"%(self.bddir,dtg)
            self.dbase="%s/%s/%s-%s-%s-ua"%(self.bddir,dtg,self.lmodel,dtype,dtg)
            self.dmask="%s-%s-%s-ua.%s"%(self.lmodel,dtype,dtg,self.gribtype)

            self.dpath="%s.ctl"%(self.dbase)

            self.dpathexists=os.path.exists(self.dpath)

            # -- try dat5
            #
            if(not(self.dpathexists) and self.tryarch):
                if(warn): print 'IIIIIIIIIIIIIIIIIIIIIIIIIIIIII M2.Model2.setDbase tryarch=1 -- trying the archive on: ',self.dbasedirarch,self.dtype
                self.dbasedir=self.dbasedirarch
                if(self.dtype == 'w2flds'):
                    self.bddir=self.w2fldsArchDir
                    self.dbasedir="%s/%s"%(self.bddir,dtg)
                    self.dbase="%s/%s.%s.%s"%(self.dbasedir,self.lmodel,dtype,dtg)
                    self.dmask="%s.%s.%s.f???.%s"%(self.lmodel,dtype,dtg,self.gribtype)
                    
                    self.dpath="%s.ctl"%(self.dbase)
                    self.dpathexists=os.path.exists(self.dpath)
            
        else:
            print 'EEE-M2.Ecm5.setDbase could not set M2.setDbase.dbase  model: ',self.model,'dtg: ',dtg,' dtype: ',self.dtype,' or maybe because model not in w2localvars.py Nwp2ModelsAll...'
            sys.exit()

        self.tdatbase=self.dbase

    # -- set prvar method to set dependence on tau
    #
    def setprvar(self,dtg=None,tau=None):
        modelprvar=self.modelprvar
        if(tau == 0):
            modelprvar="""_prvar='(( const(pr(t+1),0,-u)-const(pr(t-0),0,-u) )*4)'"""
        elif(tau >= 6 and tau <= 120):
            modelprvar="""_prvar='(( const(pr(t-0),0,-u)-const(pr(t-1),0,-u) )*4)'"""
        elif(tau > 120):
            modelprvar="""_prvar='(( const(pr(t-0),0,-u)-const(pr(t-2),0,-u) )*2)'"""
            
        return(modelprvar)


class Ecm2(Model2,FimRun):

    modelrestitle='T`bl`n|N400 L91'
    modelDdtg=12
    modelgridres='1.0'
    modelres=modelgridres.replace('.','')

    modelprvar="""_prvar='(( const(pr(t+0),0,-u)-const(pr(t-1),0,-u) )*4*1000)'"""
    modelpslvar='psl*0.01'
    modeltitleAck1="ECMWF Data Courtesy of NCEP/NCO"
    modeltitleFullmod="ECMWF(IFS)"

    model='ecm2'
    center='ecmwf'

    dmodel='ecmo'
    pmodel='ecm'

    pltdir='plt_ecmwf_ecm'
    pmodel='ecm'

    modelPlotTaus=[0,6,12,18,24,30,36,42,48,60,72,84,96,108,120,132,144,156,168]
    gmodname="%s%s"%(pmodel,modelres)


    def __init__(self,bdir2=None,gribver=1):

        self.dirmodel=self.dmodel

        if(bdir2 != None): self.bdir2=bdir2
        
        self.initModelCenter(self.center)
        self.initGribVer(gribver)

        self.location='kishou'

        self.tautype='wgrib'

        self.nfields=94
        self.nfieldsW2flds=66

        self.tbase=self.dmodel

        self.etau=240
        self.dtau=6

        self.rundtginc=12

        self.adecksource='ecmwf'
        self.adeckaid='edet'


    # -- set prvar method to set dependence on tau
    #
    def setprvar(self,dtg=None,tau=None):
        modelprvar=self.modelprvar
        if(tau == 0):
            modelprvar="""_prvar='(( const(pr(t+1),0,-u)-const(pr(t-0),0,-u) )*4*1000)'"""
        return(modelprvar)


    def setMaxtau(self,dtg):
        hh=dtg[8:10]
        if(hh == '00' or hh == '12'):  self.maxtau=240
        else:    self.maxtau=-999
        return(self.maxtau)



    def name2tau(self,file,dtg=None):
        ib=len(self.dmodel.split('.'))+1
        try:
            tau=file.split('.')[ib][1:]
            tau=int(tau)
        except:
            tau=None
        return(tau)

    def gname2tau(self,file,dtg):

        yyyy=dtg[0:4]
        mm=dtg[4:6]

        lf=len(file)

        lfe=lf-3
        lfb=lfe-6
        vmmddhh=file[lfb:lfe]
        vmm=vmmddhh[0:2]
        if(vmm == '01' and mm == '12'):
            vdtg=str(int(yyyy+1))+vmmddhh
        else:
            vdtg=yyyy+vmmddhh
        tau=mf.dtgdiff(dtg,vdtg)
        tau=int(tau)

        return(tau)


    def setgmask(self,dtg):
        mmddhh=dtg[4:10]
        self.gmask="ecens_DCD%s*"%(mmddhh)
        self.gmask="DCD%s*"%(mmddhh)

    def setxwgrib(self,dtg):

        self.xwgrib='wgrib'
        if(hasattr(self,'dmodelType')):
            if(self.dmodelType == 'w2flds'): self.tautype='wgrib'

        if(self.tautype == 'alltau'):
            self.dmask="%s.%s.%s"%(self.dmodel,dtg,self.gribtype)
            self.dsetmask="%s.%s.%s.f%%f3.%s"%(self.dmodel,self.dmodelType,dtg,self.gribtype)
        else:
            self.dmask="%s.%s.f???.%s"%(self.dmodel,dtg,self.gribtype)
            self.dsetmask="%s.%s.f%%f3.%s"%(self.dmodel,dtg,self.gribtype)



    def setctlgridvar(self,dtg):

        latlongrid='''xdef 360 linear   0.0 1.0
ydef 181 linear -90.0 1.0'''

        if(self.gribtype == 'grb1'):
            optiondtype='''options yrev template
dtype grib
zdef 14 levels 1000 925 850 700 500 400 300 250 200 150 100 50 20 10'''

        elif(self.gribtype == 'grb2'):
            optiondtype='''options yrev template pascals
dtype grib2'''


        self.ctlgridvar='''undef 9.999E+20
title ecmo 1deg deterministic run
*  produced by grib2ctl v0.9.12.5p16
%s
%s
vars 19
sic       0  31,1,0  ** Sea-ice cover [(0-1)]
sst       0  34,1,0  ** Sea surface temperature [K]
uas       0 165,1,0  ** 10 metre u wind component m s**-1
vas       0 166,1,0  ** 10 metre v wind component m s**-1
tads      0 168,1,0  ** 2 metre dewpoint temperature K
tas       0 167,1,0  ** 2 metre temperature K
zg       14 156,100,0 ** Height (geopotential) m
psln      0 152,109,1  ** Log surface pressure -
tmin      0 202,1,0  ** Min 2m temp since previous post-processing K
psl       0 151,1,0  ** Mean sea level pressure Pa
tmax      0 201,1,0  ** Max 2m temp since previous post-processing K
hur      14 157,100,0 ** Relative humidity %%
ta       14 130,100,0 ** Temperature K
clt       0 164,1,0  ** Total cloud cover (0 - 1)
pr        0 228,1,0  ** Total precipitation m
prl       0 142,1,0  ** large-scale precipitation m
prc       0 143,1,0  ** convective precipitation m
ua       14 131,100,0 ** U-velocity m s**-1
va       14 132,100,0 ** V-velocity m s**-1
endvars'''%(optiondtype,latlongrid)


        allvarsnew='''vars 30
10FGsfc  0 49,1,0  ** Wind gust at 10 metres [m s**-1]
10Usfc  0 165,1,0  ** 10 metre U wind component [m s**-1]
10Vsfc  0 166,1,0  ** 10 metre V wind component [m s**-1]
2Dsfc  0 168,1,0  ** 2 metre dewpoint temperature [K]
2Tsfc  0 167,1,0  ** 2 metre temperature [K]
BLHsfc  0 159,1,0  ** Boundary layer height [m]
CAPEsfc  0 59,1,0  ** Convective available potential energy [J kg**-1]
CIsfc  0 31,1,0  ** Sea-ice cover [(0-1)]
CPsfc  0 143,1,0  ** Convective precipitation [m]
GHprs 14 156,100,0 ** Height [m]
LNSPhbl  0 152,109,1  ** Logarithm of surface pressure
LSPsfc  0 142,1,0  ** Stratiform precipitation [m]
MN2Tsfc  0 202,1,0  ** Minimum 2 metre temperature since previous post-processing [K]
MSLsfc  0 151,1,0  ** Mean sea-level pressure [Pa]
MX2Tsfc  0 201,1,0  ** Maximum 2 metre temperature since previous post-processing [K]
Rprs 14 157,100,0 ** Relative humidity [%]
SFsfc  0 144,1,0  ** Snowfall (convective + stratiform) [m of water equivalent]
SPhbl  0 134,109,1  ** Surface pressure [Pa]
SSTKsfc  0 34,1,0  ** Sea surface temperature [K]
Tprs 14 130,100,0 ** Temperature [K]
TCCsfc  0 164,1,0  ** Total cloud cover [(0 - 1)]
TCWsfc  0 136,1,0  ** Total column water [kg m**-2]
TPsfc  0 228,1,0  ** Total precipitation [m]
TTRsfc  0 179,1,0  ** Top thermal radiation [W m**-2 s]
Uprs 14 131,100,0 ** U velocity [m s**-1]
Vprs 14 132,100,0 ** V velocity [m s**-1]
Wprs  0 135,100,700  ** Vertical velocity [Pa s**-1]
var121sfc  0 121,1,0  ** undefined
var122sfc  0 122,1,0  ** undefined
var123sfc  0 123,1,0  ** undefined'''

        allvarsold='''vars 15
10Usfc  0 165,1,0  ** 10 metre U wind component [m s**-1]
10Vsfc  0 166,1,0  ** 10 metre V wind component [m s**-1]
2Dsfc  0 168,1,0  ** 2 metre dewpoint temperature [K]
2Tsfc  0 167,1,0  ** 2 metre temperature [K]
GHprs 14 156,100,0 ** Height [m]
LNSPhbl  0 152,109,1  ** Logarithm of surface pressure
MN2Tsfc  0 202,1,0  ** Minimum 2 metre temperature since previous post-processing [K]
MSLsfc  0 151,1,0  ** Mean sea-level pressure [Pa]
MX2Tsfc  0 201,1,0  ** Maximum 2 metre temperature since previous post-processing [K]
Rprs 14 157,100,0 ** Relative humidity [%]
Tprs 14 130,100,0 ** Temperature [K]
TCCsfc  0 164,1,0  ** Total cloud cover [(0 - 1)]
TPsfc  0 228,1,0  ** Total precipitation [m]
Uprs 14 131,100,0 ** U velocity [m s**-1]
Vprs 14 132,100,0 ** V velocity [m s**-1]'''

class Ecm4(Model2,FimRun):

    modelrestitle='To1279L137'
    modelDdtg=12
    modelgridres='0.25'
    modelres=modelgridres.replace('.','')

    modelprvar="""_prvar='(( const(pr(t+0),0,-u)-const(pr(t-1),0,-u) )*4*1000)'"""
    modelpslvar='psl*0.01'
    modeltitleAck1="ECMWF Data Courtesy of NCEP/NCO"
    modeltitleFullmod="ECMWF(HRES)"

    model='ecm4'
    center='ecmwf'

    dmodel='ecm4'
    pmodel='ecm'

    pltdir='plt_ecmwf_ecm'
    pmodel='ecm'

    modelPlotTaus=[0,6,12,18,24,30,36,42,48,60,72,84,96,108,120,132,144,156,168]
    gmodname="%s%s"%(pmodel,modelres)
    
    regridTracker=0.25


    def __init__(self,bdir2=None,gribver=1):

        self.dirmodel=self.dmodel

        if(bdir2 != None): self.bdir2=bdir2
        
        self.initModelCenter(self.center)
        self.initGribVer(gribver)

        self.location='kishou'

        self.tautype='wgrib'

        self.nfields=90
        self.nfieldsW2flds=54

        self.tbase=self.dmodel

        self.etau=240
        self.dtau=6

        self.rundtginc=12

        self.adecksource='ecmwf'
        self.adeckaid='edet'


    # -- set prvar method to set dependence on tau
    #
    def setprvar(self,dtg=None,tau=None):
        modelprvar=self.modelprvar
        if(tau == 0):
            modelprvar="""_prvar='(( const(pr(t+1),0,-u)-const(pr(t-0),0,-u) )*4*1000)'"""
        return(modelprvar)


    def setMaxtau(self,dtg):
        hh=dtg[8:10]
        if(hh == '00' or hh == '12'):  self.maxtau=240
        else:    self.maxtau=-999
        return(self.maxtau)



    def name2tau(self,file,dtg=None):
        ib=len(self.dmodel.split('.'))+1
        try:
            tau=file.split('.')[ib][1:]
            tau=int(tau)
        except:
            tau=None
        return(tau)

    def gname2tau(self,file,dtg):

        yyyy=dtg[0:4]
        mm=dtg[4:6]

        lf=len(file)

        lfe=lf-3
        lfb=lfe-6
        vmmddhh=file[lfb:lfe]
        vmm=vmmddhh[0:2]
        if(vmm == '01' and mm == '12'):
            vdtg=str(int(yyyy+1))+vmmddhh
        else:
            vdtg=yyyy+vmmddhh
        tau=mf.dtgdiff(dtg,vdtg)
        tau=int(tau)

        return(tau)


    def setgmask(self,dtg):
        mmddhh=dtg[4:10]
        self.gmask="ecens_DCD%s*"%(mmddhh)
        self.gmask="DCD%s*"%(mmddhh)

    def setxwgrib(self,dtg):

        self.xwgrib='wgrib'
        if(hasattr(self,'dmodelType')):
            if(self.dmodelType == 'w2flds'): self.tautype='wgrib'

        if(self.tautype == 'alltau'):
            self.dmask="%s.%s.%s"%(self.dmodel,dtg,self.gribtype)
            self.dsetmask="%s.%s.%s.f%%f3.%s"%(self.dmodel,self.dmodelType,dtg,self.gribtype)
        else:
            self.dmask="%s.%s.f???.%s"%(self.dmodel,dtg,self.gribtype)
            self.dsetmask="%s.%s.f%%f3.%s"%(self.dmodel,dtg,self.gribtype)



    def setctlgridvar(self,dtg):

        latlongrid='''xdef 1440 linear 0.0 0.25
ydef 721 linear -90.0 0.25'''

        if(self.gribtype == 'grb1'):
            optiondtype='''options yrev template
dtype grib
zdef 10 levels 1000 925 850 700 500 400 300 250 200'''

        elif(self.gribtype == 'grb2'):
            optiondtype='''options yrev template pascals
dtype grib2'''


        self.ctlgridvar='''undef 9.999E+20
title ecm4 0.25deg deterministic run
*  produced by grib2ctl v0.9.12.5p16
%s
%s
vars 19
sic       0  31,1,0  ** Sea-ice cover [(0-1)]
sst       0  34,1,0  ** Sea surface temperature [K]
uas       0 165,1,0  ** 10 metre u wind component m s**-1
vas       0 166,1,0  ** 10 metre v wind component m s**-1
tads      0 168,1,0  ** 2 metre dewpoint temperature K
tas       0 167,1,0  ** 2 metre temperature K
zg       10 156,100,0 ** Height (geopotential) m
psln      0 152,109,1  ** Log surface pressure -
tmin      0 202,1,0  ** Min 2m temp since previous post-processing K
psl       0 151,1,0  ** Mean sea level pressure Pa
tmax      0 201,1,0  ** Max 2m temp since previous post-processing K
hur      10 157,100,0 ** Relative humidity %%
ta       10 130,100,0 ** Temperature K
clt       0 164,1,0  ** Total cloud cover (0 - 1)
pr        0 228,1,0  ** Total precipitation m
prl       0 142,1,0  ** large-scale precipitation m
prc       0 143,1,0  ** convective precipitation m
ua       14 131,100,0 ** U-velocity m s**-1
va       14 132,100,0 ** V-velocity m s**-1
endvars'''%(optiondtype,latlongrid)


        allvarsnew='''
vars 29
10FGsfc  0 49,1,0  ** Wind gust at 10 metres [m s**-1]
10Usfc  0 165,1,0  ** 10 metre U wind component [m s**-1]
10Vsfc  0 166,1,0  ** 10 metre V wind component [m s**-1]
2Dsfc  0 168,1,0  ** 2 metre dewpoint temperature [K]
2Tsfc  0 167,1,0  ** 2 metre temperature [K]
BLHsfc  0 159,1,0  ** Boundary layer height [m]
CAPEsfc  0 59,1,0  ** Convective available potential energy [J kg**-1]
CIsfc  0 31,1,0  ** Sea-ice cover [(0-1)]
CPsfc  0 143,1,0  ** Convective precipitation [m]
GHprs 10 156,100,0 ** Height [m]
LSPsfc  0 142,1,0  ** Stratiform precipitation [m]
MSLsfc  0 151,1,0  ** Mean sea-level pressure [Pa]
PT  0 3,117,2000  ** Potential temperature [K]
Rprs 10 157,100,0 ** Relative humidity [%]
RSNsfc  0 33,1,0  ** Snow density [kg m**-3]
SDsfc  0 141,1,0  ** Snow depth [m of water equivalent]
SFsfc  0 144,1,0  ** Snowfall (convective + stratiform) [m of water equivalent]
SPsfc  0 134,1,0  ** Surface pressure [Pa]
SSTKsfc  0 34,1,0  ** Sea surface temperature [K]
Tprs 10 130,100,0 ** Temperature [K]
TCCsfc  0 164,1,0  ** Total cloud cover [(0 - 1)]
TCWsfc  0 136,1,0  ** Total column water [kg m**-2]
TPsfc  0 228,1,0  ** Total precipitation [m]
Uprs 10 131,100,0 ** U velocity [m s**-1]
Vprs 10 132,100,0 ** V velocity [m s**-1]
VOprs 10 138,100,0 ** Vorticity (relative) [s**-1]
Wprs 10 135,100,0 ** Vertical velocity [Pa s**-1]
var121sfc  0 121,1,0  ** undefined
var122sfc  0 122,1,0  ** undefined
ENDVARS
'''


#eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee ecmwf tigge
#

class Ecmh(Ecm2,FimRun):
    """ limited-area hi-res tigge pull"""

    modelrestitle='T`bl`n1279|N640 L137'
    modelDdtg=12
    modelgridres='0.5'
    modelres=modelgridres.replace('.','')

    # -- units are accumulated precip in Kg/m^2 vice m
    modelprvar="""_prvar='(( const(pr(t+0),0,-u)-const(pr(t-1),0,-u) )*4)'"""
    modelpslvar='psl*0.01'
    modeltitleAck1="ECMWF Data Courtesy of TIGGE server"
    modeltitleFullmod="ECMWF(IFS)"

    model='ecmh'
    center='ecmwf'

    dmodel='ecmh'
    pmodel='ecm'

    pltdir='plt_ecmwf_ecmh'
    pmodel='ecm'

    modelPlotTaus=[0,6,12,18,24,30,36,42,48,60,72,84,96,108,120,132,144,156,168]

    gmodname="%s%s"%(pmodel,modelres)

    modeltitleAck1="ECMWF Data Courtesy of ECMWF TIGGE Server"
    fullmod="ECMWF(IFS)"

    btau=0
    etau=240
    dtau=6
    taus=range(btau,etau+1,dtau)

    # -- grid

    gridRes=0.125
    gridRes=0.100

    latN=55.0
    latS=30.0
    lonW=240.0
    lonE=270.0
    lonW=-120.0
    lonE=-95.0

    dlonGrid=(lonE-lonW)
    dlatGrid=(latN-latS)
    ni=int(dlonGrid/gridRes + 0.5)+1
    nj=int(dlatGrid/gridRes + 0.5)+1

    ecArea='%5.1f/%5.1f/%5.1f/%5.1f'%(latN,lonW,latS,lonE)
    ecArea=ecArea.strip()

    doUA=0

    doalltaus=0

    def __init__(self,gribver=2,fctype='fc'):

        self.dirmodel=self.dmodel

        self.initModelCenter(self.center)
        self.initGribVer(gribver)

        self.location='kishou'
        self.tautype='wgrib'

        self.nfields=53
        self.nfieldsW2flds=53

        self.rundtginc=12

        self.adecksource='tmtrkN'
        self.adeckaid='ecmh'

        self.fctype=fctype
        self.dattaus=range(self.btau,self.etau+1,self.dtau)
        self.dmodelType='w2flds'


    def setDtgTdirCtl(self,dtg):

        self.dtg=dtg
        tdir="%s/%s"%(self.w2fldsSrcDir,self.dtg)
        MF.ChkDir(tdir,'mk')
        self.tdir=tdir

        if(self.doalltaus):
            self.dsetbase="%s.w2flds.%s.alltaus.grb%d"%(self.model,self.dtg,self.gribver)
        else:
            self.dsetbase="%s.w2flds.%s.f%%f3.grb%d"%(self.model,self.dtg,self.gribver)

        self.tbase="%s.w2flds.%s"%(self.model,self.dtg)
        self.ctlpath="%s/%s.ctl"%(self.tdir,self.tbase)
        self.gmpfile="%s.grib%1d.gmp"%(self.tbase,self.gribver)


    def getFieldsTigge(self,override=0,verb=0,ropt='',cleanDir=0,justSfc=0):

        def mkEcDtg(dtg):
            ecdtg="%s-%s-%s"%(dtg[0:4],dtg[4:6],dtg[6:8])
            synhour=int(dtg[8:10])
            return(ecdtg,synhour)


        if(cleanDir):
            cmd="rm %s/*"%(self.tdir)
            mf.runcmd(cmd,ropt)
            
        from ecmwfapi import ECMWFDataServer
        server = ECMWFDataServer()

        (ecdtg,synhour)=mkEcDtg(self.dtg)

        ecarea=self.ecArea
        ecgridres='%5.3f/%5.3f'%(self.gridRes,self.gridRes)

        paramsfc='136/146/147/151/165/166/167/176/177/179/228164/228228'

        paramua='129/130/131/157/156'
        paramua='all'

        taus=self.taus
        if(self.doalltaus): taus=["%d/to/%d/by/%d"%(self.btau,self.etau,self.dtau)]

        for tau in taus:

            if(self.doalltaus):
                opathsf="%s/%s.%s.alltaus.sf.grb2"%(self.tdir,self.model,self.dtg)
                opathua="%s/%s.%s.alltaus.ua.grb2"%(self.tdir,self.model,self.dtg)
                opath="%s/%s.w2flds.%s.alltaus.grb%1d"%(self.tdir,self.model,self.dtg,self.gribver)

            else:
                opathsf="%s/%s.%s.f%03d.sf.grb2"%(self.tdir,self.model,self.dtg,tau)
                opathua="%s/%s.%s.f%03d.ua.grb2"%(self.tdir,self.model,self.dtg,tau)
                opath="%s/%s.w2flds.%s.f%03d.grb%1d"%(self.tdir,self.model,self.dtg,tau,self.gribver)

            if(not(override) and MF.ChkPath(opath) and not(justSfc)): continue

            retsf={
                "dataset"   : "tigge",
                'levtype'   : "sfc",
                "date"      : "%s"%(ecdtg),
                "param"     : "%s"%(paramsfc),
                "step"      : "%s"%(str(tau)),
                "time"      : "%02d"%(synhour),
                "area"      : "%s"%(ecarea),
                "grid"      : "%s"%(ecgridres),
                "target"    : "%s"%(opathsf),
                'expver'    : "prod",
                'type'      : "%s"%(self.fctype),
            }

            retua={
                "dataset"   : "tigge",
                'levtype'   : "pl",
                'levelist'   : "all",
                "date"      : "%s"%(ecdtg),
                "param"     : "%s"%(paramua),
                "step"      : "%s"%(str(tau)),
                "time"      : "%02d"%(synhour),
                "area"      : "%s"%(ecarea),
                "grid"      : "%s"%(ecgridres),
                "target"    : "%s"%(opathua),
                'expver'    : "prod",
                'type'      : "%s"%(self.fctype),
            }

            if(verb):
                print 'retsf: ',retsf
                print 'retua: ',retua

            # -- do sfc fields first
            #
            if(ropt != 'norun'):
                
                # -- first UA fields
                #
                if(self.doUA and justSfc == 0):

                    MF.sTimer('ecmt-UA-%s'%(self.dtg))
                    server.retrieve(retua)
                    cmd="cat %s > %s"%(opathua,opath)
                    mf.runcmd(cmd)
                    try:
                        os.unlink(opathua)
                    except:
                        print 'WWW trying to kill uA path: ',opathua,' in M2.getFieldsTigge failed'
                    MF.dTimer('ecmt-UA-%s'%(self.dtg))

                # -- sfc fields 2nd
                #
                MF.sTimer('ecmt-sf-%s'%(self.dtg))
                server.retrieve(retsf)
                cmd="cat %s >> %s"%(opathsf,opath)
                mf.runcmd(cmd)
                try:
                    os.unlink(opathsf)
                except:
                    print 'WWW trying to kill SF path: ',opathsf,' in M2.getFieldsTigge failed'
                
                MF.dTimer('ecmt-sf-%s'%(self.dtg))
                    
            else:
                print 'RRR(will retrieve sfc): ',retsf
                print 'RRR(will retrieve  UA): ',retua



    def filtTaus(self,curdir,dtgChk,
                 override=0,
                 quiet=0,
                 minsiz=9000000):

        w2inv='wgrib2.inv.txt'
        MF.ChangeDir(self.tdir,verb=1)

        allfile=self.dsetbase
        self.alltaufile="%s/%s"%(self.tdir,allfile)
        
        allfile5="%s/%s/%s"%(self.w2fldsArchDir,self.dtg,allfile)
        allfile6="%s/%s/%s"%(self.w2fldsArchDirDat6,self.dtg,allfile)
        
        allfileThere=MF.ChkPath(allfile)
        allfileThere5=MF.ChkPath(allfile5)
        allfileThere6=MF.ChkPath(allfile6)
        
        print 'AAA: ',allfile,allfileThere
        print '555: ',allfile5,allfileThere5
        print '666: ',allfile6,allfileThere6
        print 'DDD: ',dtgChk
        
        if(not(allfileThere) and dtgChk == 0):
            if(allfileThere5):
                print 'WWW - cp from allfile from dat5...'
                cmd="cp %s ."%(allfile5)
                mf.runcmd(cmd)
            elif(allfileThere6):
                print 'WWW - cp from allfile from dat6...'
                cmd="cp %s ."%(allfile6)
                mf.runcmd(cmd)
                

        # -- make sure allfile there first
        #
        if(not(allfileThere) and dtgChk >= 0):
            if(dtgChk == 0):
                print 'WWW - allfile not there AND NEEDED: ',allfile,' press to the tigge retrieval...'
            elif(dtgChk == 1):
                print 'III - allfile not needed...return...'
            MF.ChangeDir(curdir,verb=0)
            return

        if( MF.getPathSiz(w2inv) <= 0 or override ):
            cmd="wgrib2 -end_ft %s > %s"%(allfile,w2inv)
            owgrib2inv=MF.runcmdLog(cmd,quiet=quiet)
            if(not(quiet)):
                for o in owgrib2inv:
                    print o

        tauinv='tau.inv.txt'
        for tau in self.taus:
            vdtg=mf.dtginc(self.dtg,tau)
            (base,ext)=os.path.splitext(allfile)
            ofile="%s.f%03d%s"%(base,tau,ext)
            ofile=ofile.replace('.alltaus','')
            if(not(quiet)):
                print 'filtTaus.tau: ',tau,vdtg,ofile

            if(MF.getPathSiz(allfile) > minsiz):
                if(MF.getPathSiz(ofile) <= 0 or override):
                    cmd="grep %s %s > %s"%(vdtg,w2inv,tauinv)
                    ogrep=MF.runcmdLog(cmd,quiet=quiet)
                    if(not(quiet)):
                        for o in ogrep:
                            print o
                            
                    cmd="wgrib2 %s -i -grib %s < %s"%(allfile,ofile,tauinv)
                    owgrib2=MF.runcmdLog(cmd,quiet=quiet)
                    if(not(quiet)):
                        for o in owgrib2:
                            print o 

        MF.ChangeDir(curdir)
        return


    def chkTauDat(self,override=0,nok=53,verb=0):

        fm=self.DataPath(self.dtg,dtype=self.dmodelType,dowgribinv=1,override=override,doDATage=1)
        fd=fm.GetDataStatus(self.dtg)
        sts=fd.statuss[self.dtg]

        taus=sts.keys()
        taus.sort()
        rc=1

        rcallfile=(hasattr(self,'alltaufile') and MF.getPathSiz(self.alltaufile) > 0)
        if(MF.getPathSiz(self.alltaufile) == 0):
            rc=-2
            print
            print "chkTauDat for model: %6s dtg:%s 0 size alltaus file return -2"%(self.model,self.dtg)
            return(rc)
            
        elif(len(taus) == 0):
            rc=0
            print
            print "chkTauDat for model: %6s dtg:%s NO taus return 0"%(self.model,self.dtg)
            return(rc)

        if(verb):
            print
            print "chkTauDat for model: %6s dtg:%s"%(self.model,self.dtg)

        for tau in taus:
            nf=sts[tau][1]
            if(nf == 41):
                rc=-1
            elif(nf == 48 or (nf >= 8 and nf <= 41) ):
                rc=-2
            elif(nf >= nok): 
                rc=1
            else:
                rc=0
            if(verb): print "chkTauDat() tau: %3d  nf: %3d"%(tau,nf)
            
        # -- blowaway alltau file
        #
        if(rc == 1 and hasattr(self,'alltaufile') and MF.getPathSiz(self.alltaufile) > 0):
            print 'III.chkTauDat() alltaufile: ',self.alltaufile,' there, blowing away...'
            os.unlink(self.alltaufile)

        return(rc)



    def makeCtl(self,ropt='',verb=0):

        gtime=mf.dtg2gtime(self.dtg)
        ntaus=len(self.taus)

        xygrid="""ydef %d linear  %4.1f %5.3f
xdef %d linear    %4.1f %5.3f"""%(self.nj,self.latS,self.gridRes,
                                  self.ni,self.lonW,self.gridRes)

        gaoptions="pascals template"
        if(self.doalltaus): gaoptions="pascals"
        ctl="""dset  ^%s
index ^%s
undef 9.999E+20
title ecmh.2012071712.f000.grb2
*  produced by g2ctl v0.0.4m
dtype grib2
%s
tdef %d linear %s %dhr
* PROFILE hPa
zdef 9 levels 100000 92500 85000 70000 50000 30000 25000 20000 5000
options %s 
vars 17
psl    0,101   0,3,0    ** mean sea level pressure [Pa]
uas    0,103,10   0,2,2 ** 10 m above ground u_velocity [m/s]
vas    0,103,10   0,2,3 ** 10 m above ground v_velocity [m/s]
pr     0,1   0,1,52,1   ** surface total_precipitation [kg/m^2]
prw    0,1,,,8   0,1,51 ** atmos col total_column_water [kg/m^2]
clt    0,1,,,8   0,6,1  ** atmos col total_cloud_cover [%%]
hfls   0,1   0,0,10,1   ** surface time_integrated_surface_latent_heat_flux [W/m^2 s]
hfss   0,1   0,0,11,1   ** surface time_integrated_surface_sensible_heat_flux [W/m^2 s]
rss    0,1   0,4,9,1    ** surface time_integrated_surface_net_solar_radiation [W/m^2 s]
tas    0,103,2   0,0,0  ** 2 m above ground temperature [K]
rls    0,1   0,5,5,1    ** surface time_integrated_outgoing_long_wave_radiation [W/m^2 s]
rlt    0,8   0,5,5,1    ** top of atmosphere time_integrated_outgoing_long_wave_radiation [W/m^2 s]
ua     8,100  0,2,2     ** (1000 925 850 700 500 300 250 200) u_velocity [m/s]
va     8,100  0,2,3     ** (1000 925 850 700 500 300 250 200) v_velocity [m/s]
ta     8,100  0,0,0     ** (1000 925 850 700 500 300 250 200) temperature [K]
hus    8,100  0,1,0     ** (1000 925 850 700 500 300 250 200) specific_humidity [kg/kg]
zg     9,100  0,3,5     ** (1000 925 850 700 500 300 250 200 50) geopotential_height [gpm]
endvars"""%(self.dsetbase,self.gmpfile,xygrid,ntaus,gtime,self.dtau,gaoptions)

        self.ctl=ctl

        MF.WriteString2File(ctl,self.ctlpath)

        gbmopt='-i'
        if(verb): gbmopt='-v -i'
        cmd="gribmap %s %s"%(gbmopt,self.ctlpath)
        mf.runcmd(cmd,ropt)


    # -- set prvar method to set dependence on tau
    #
    def setprvar(self,dtg=None,tau=None):
        modelprvar=self.modelprvar
        if(tau == 0):
            # -- units are accumulated precip in Kg/m^2 vice m
            modelprvar="""_prvar='(( const(pr(t+1),0,-u)-const(pr(t-0),0,-u) )*4)'"""
        return(modelprvar)


    def setMaxtau(self,dtg):
        hh=dtg[8:10]
        if(hh == '00' or hh == '12'):  self.maxtau=240
        else:    self.maxtau=-999
        return(self.maxtau)


    def name2tau(self,file,dtg=None):
        ib=len(self.dmodel.split('.'))+1
        try:
            tau=file.split('.')[ib][1:]
            tau=int(tau)
        except:
            tau=None
        return(tau)

    def gname2tau(self,file,dtg):

        yyyy=dtg[0:4]
        mm=dtg[4:6]

        lf=len(file)

        lfe=lf-3
        lfb=lfe-6
        vmmddhh=file[lfb:lfe]
        vmm=vmmddhh[0:2]
        if(vmm == '01' and mm == '12'):
            vdtg=str(int(yyyy+1))+vmmddhh
        else:
            vdtg=yyyy+vmmddhh
        tau=mf.dtgdiff(dtg,vdtg)
        tau=int(tau)

        return(tau)


    def setgmask(self,dtg):
        mmddhh=dtg[4:10]
        self.gmask="ecens_DCD%s*"%(mmddhh)
        self.gmask="DCD%s*"%(mmddhh)


    def setxwgrib(self,dtg):

        self.xwgrib='wgrib2'
        if(hasattr(self,'dmodelType')):
            if(self.dmodelType == 'w2flds'): self.tautype='wgrib'

        if(self.tautype == 'alltau'):
            self.dmask="%s.%s.%s"%(self.dmodel,dtg,self.gribtype)
            self.dsetmask="%s.%s.%s.f%%f3.%s"%(self.dmodel,self.dmodelType,dtg,self.gribtype)
        else:
            self.dmask="%s.%s.f???.%s"%(self.dmodel,dtg,self.gribtype)
            self.dsetmask="%s.%s.f%%f3.%s"%(self.dmodel,dtg,self.gribtype)




    def setctlgridvar(self,dtg):

        latlongrid='''xdef 720 linear   0.0 0.5
ydef 361 linear -90.0 0.5'''

        if(self.gribtype == 'grb1'):
            optiondtype='''options yrev template
dtype grib
zdef 9 levels 1000 925 850 700 500 300 250 200 50'''

        elif(self.gribtype == 'grb2'):
            optiondtype='''options template pascals
dtype grib2'''


        self.ctlgridvar='''undef 9.999E+20
title ecmo 1deg deterministic run
*  produced by grib2ctl v0.9.12.5p16
%s
%s
vars 19
sic       0  31,1,0  ** Sea-ice cover [(0-1)]
sst       0  34,1,0  ** Sea surface temperature [K]
uas       0 165,1,0  ** 10 metre u wind component m s**-1
vas       0 166,1,0  ** 10 metre v wind component m s**-1
tads      0 168,1,0  ** 2 metre dewpoint temperature K
tas       0 167,1,0  ** 2 metre temperature K
zg       14 156,100,0 ** Height (geopotential) m
psln      0 152,109,1  ** Log surface pressure -
tmin      0 202,1,0  ** Min 2m temp since previous post-processing K
psl       0 151,1,0  ** Mean sea level pressure Pa
tmax      0 201,1,0  ** Max 2m temp since previous post-processing K
hur      14 157,100,0 ** Relative humidity %%
ta       14 130,100,0 ** Temperature K
clt       0 164,1,0  ** Total cloud cover (0 - 1)
pr        0 228,1,0  ** Total precipitation m
prl       0 142,1,0  ** large-scale precipitation m
prc       0 143,1,0  ** convective precipitation m
ua       14 131,100,0 ** U-velocity m s**-1
va       14 132,100,0 ** V-velocity m s**-1
endvars'''%(optiondtype,latlongrid)


class Ecmt(Ecmh):

    modelrestitle='T`bl`n1279|N640 L137'
    modelDdtg=12
    modelgridres='0.5'
    modelres=modelgridres.replace('.','')

    # -- units are accumulated precip in Kg/m^2 vice m
    modelprvar="""_prvar='(( const(pr(t+0),0,-u)-const(pr(t-1),0,-u) )*4)'"""
    modelpslvar='psl*0.01'
    modeltitleAck1="ECMWF Data Courtesy of TIGGE server"
    modeltitleFullmod="ECMWF(IFS)"

    model='ecmt'
    center='ecmwf'

    dmodel='ecmt'
    pmodel='ecm'

    pltdir='plt_ecmwf_ecmt'
    pmodel='ecm'

    modelPlotTaus=[0,6,12,18,24,30,36,42,48,60,72,84,96,108,120,132,144,156,168]

    gmodname="%s%s"%(pmodel,modelres)

    modeltitleAck1="ECMWF Data Courtesy of ECMWF TIGGE Server"
    fullmod="ECMWF(IFS)"

    btau=0
    etau=240
    dtau=6
    taus=range(btau,etau+1,dtau)

    gridRes=0.5
    ecArea='global'
    latS=-90.0
    lonW=0.0
    ni=720
    nj=361

    doalltaus=0
    doUA=1


    def __init__(self,bdir2=None,gribver=2,fctype='fc'):

        self.dirmodel=self.dmodel
        if(bdir2 != None): self.bdir2=bdir2
                
        self.initModelCenter(self.center)
        self.initGribVer(gribver)

        self.location='kishou'
        self.tautype='wgrib'

        self.nfields=53
        self.nfieldsW2flds=53

        self.rundtginc=12

        self.adecksource='tmtrkN'
        self.adeckaid='ecmt'

        self.fctype=fctype
        self.dattaus=range(self.btau,self.etau+1,self.dtau)
        self.dmodelType='w2flds'




class Ecmg(Ecm2,FimRun):

    modelrestitle='T`bl`n|N400 L91'
    modelDdtg=12
    modelgridres='1.0'
    modelprvar="""_prvar='(( const(pr(t+0),0,-u)-const(pr(t-1),0,-u) )*4*1000)'"""
    modelpslvar='psl*0.01'
    modeltitleAck1="ECMWF Data Courtesy of ECMWF"
    modeltitleFullmod="ECMWF(IFS)"

    pltdir='plt_ecmwf_ecmg'
    pmodel='ecmg'

    def __init__(self,model='ecmg',center='ecmwf',gribver=1):

        self.model=model
        self.dmodel='ecmg'
        self.dirmodel=self.dmodel
        self.dmodelType=None

        self.initModelCenter(center)
        self.initGribVer(gribver)

        self.location='kishou'

        self.tautype='wgrib'

        self.nfields=5
        self.nfieldsW2flds=12

        self.tbase=self.dmodel

        self.etau=240
        self.dtau=12

        self.rundtginc=12

        self.adecksource='ecmwf'
        self.adeckaid='edeg'


    def setDbase(self,dtg,dtype=None):

        self.dbasedir="%s/%s"%(self.bddir,dtg)
        self.dbase="%s/%s.%s.0p5"%(self.dbasedir,self.dmodel,dtg)
        self.dpath="%s.ctl"%(self.dbase)
        self.dpathexists=os.path.exists(self.dpath)
        self.tdatbase=self.dbase


    def setxwgribNwp2(self,dtg):
        self.gribtype='grb2'
        self.xwgrib='wgrib2'
        self.dmask="%s.%s.0p5.f???.grb2"%(self.dmodel,dtg)
        self.dsetmask="%s.%s.0p5.f%%f3.grb2"%(self.dmodel,dtg)

    def name2tau(self,file,dtg=None):
        tau=file.split('.')[3][1:]
        tau=int(tau)
        return(tau)




#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# individual model classes
#  



class uKm2(Model2):

    modelrestitle='0.56x0.87|N162L50'
    modelDdtg=6
    modelgridres='0.7'
    modelres=modelgridres.replace('.','')

    pltdir='plt_ukmo_ukm'
    pmodel='ukm'
    gmodname="%s%s"%(pmodel,modelres)

    modeltitleAck1="UKMO 0.7 deg data courtesy of UKMO"
    modeltitleFullmod="UKMO"

    regridTracker=0.10


    def __init__(self,bdir2=None,
                 model='ukm2',center='ukmo',gribver=1):

        self.model=model
        self.dmodel='ukm'
        self.dirmodel=model
        self.archdirmodel='ukm'
        self.lmodel=model
        if(bdir2 != None): self.bdir2=bdir2

        self.location='kishou'

        self.initModelCenter(center)
        self.initGribVer(gribver)

        self.archmodelcenter="%s/%s"%(self.center,self.archdirmodel)

        self.tautype='alltau'

        if(mf.find(self.dmodel,'w2flds')): self.tautype='wgrib'

        self.nfields=0
        self.nfieldsW2flds=40


        # if ddtg between runs is 12 h
        #

        self.modelprvar12="""
_prvar='pr(t+0)*2'
if(_tau = 0)
  _prvar='pr(t+0)*2'
endif
if(_tau = 6)
  _prvar='((const(pr(t-1),0,-u)+pr(t+1))*0.5)*2'
endif
"""
        self.modelprvar="""
_prvar='pr(t+0)*2'
if(_tau = 0)
  _prvar='((const(pr(t-1),0,-u)+pr(t+1))*0.5)*2'
endif
if(_tau = 6)
  _prvar='((const(pr(t-1),0,-u)+pr(t+1))*0.5)*2'
endif
"""
        self.modelprvar00="""_prvar='((const(pr(t-1),0,-u)+pr(t+1))*0.5)*2'"""
        self.modelprvar06="""_prvar='((const(pr(t-1),0,-u)+pr(t+1))*0.5)*2'"""
        self.modelprvar="""_prvar='pr(t+0)*2'"""
        
        self.modelprvarNative="""
if(_tau = 0)
  _prvar='(pr(t-0))*4'
endif
        
if(_tau >= 6 & _tau <= 66)
  _prvar='((pr(t-0)-pr(t-1)))*4'
endif
      
if(_tau >= 72 & _tau <= 168)
  _prvar='((pr(t-0)-pr(t-2)))*2'
endif
"""
        

        self.modelpslvar='psl*0.01'
        self.modeltitleAck1="UKMO Data Licenced through Julian Heming, UKMO"
        self.modeltitleFullmod="UKMO(UM)"

        self.rundtginc=6

        self.adecksource='nhc,jtwc'
        self.adeckaid='egrr'


    def setprvar(self,dtg=None,tau=None,dtgNativeUkm='2017042512'):

        diff1=mf.dtgdiff(dtgNativeUkm,dtg)
        modelprvar=self.modelprvar
        if(tau == 0):
            modelprvar="""_prvar='pr(t+2)*1'"""
        if(diff1 >= 0):
            modelprvar=self.modelprvarNative
            if(tau != None):
                if(tau == 0):
                    modelprvar="""_prvar='(pr(t+1)-pr(t-0))*4'"""
                elif(tau >= 6 and tau <= 66):
                    modelprvar="""_prvar='((pr(t-0)-pr(t-1)))*4'"""
                elif(tau >= 72 and tau <= 168):
                    modelprvar="""_prvar='((pr(t-0)-pr(t-2)))*2'"""

        return(modelprvar)




    def setMaxtau(self,dtg,dtg1='2009010100'):
        hh=dtg[8:10]
        diff1=mf.dtgdiff(dtg1,dtg)
        if(diff1 > 0.0 ):
            if(hh == '00' or hh == '12'):
                self.maxtau=144
            else:
                self.maxtau=60
        else:
            if(hh == '00' or hh == '12'):
                self.maxtau=120
            else:
                self.maxtau=48

        return(self.maxtau)


    def getDataTaus(self,dtg):

        dtghh=int(dtg[8:10])

        if(dtghh == 0 or dtghh == 12):
            self.etau=168
            taus=range(0,72+1,6)+range(84,self.etau+1,12)
        elif(dtghh == 6 or dtghh == 18):
            self.etau=60
            taus=range(0,self.etau+1,6)
        else:
            taus=[]

        return(taus)


    def setModelPlotTaus(self,dtg=None):
        if(dtg == None):
            dtghh=self.dtg[8:]
        else:
            dtghh=dtg[8:]

        dtghh=int(dtghh)

        dtau=12
        etau=None
        if(dtghh == 0 or dtghh == 12):
            taus=[0,6,12,18,24,30,36,42,48,60,72,84,96,108,120,132,144,156,168]
        elif(dtghh == 6 or dtghh == 18):
            taus=[0,6,12,18,24,30,36,42,48,60]

        self.modelPlotTaus=taus
        return(taus)


    def name2tau(self,file,dtg=None,dtg1='2009010100'):

        if(hasattr(self,'dmodelType')):
            dtype=self.dmodelType
        else:
            dtype=None

        if(dtg != None):
            hh=dtg[8:10]
            diff1=mf.dtgdiff(dtg1,dtg)
        else:
            diff1=-1.0

        if(diff1 > 0.0 ):
            if(hh == '00' or hh == '12'):
                if(dtype == 'w2flds'):
                    self.nfields=40
                    ctau=file.split('.')[-2][1:]
                    tau=int(ctau)
                else:
                    tau=144
                    self.nfields=760

            else:
                if(dtype == 'w2flds'):
                    self.nfields=40
                    ctau=file.split('.')[-2][1:]
                    tau=int(ctau)
                else:
                    tau=60
                    self.nfields=440


        else:
            ctau=file.split('.')[-2][1:]
            tau=int(ctau)
        return(tau)




    def setxwgrib(self,dtg,dtg1='2009010100'):

        self.xwgrib='wgrib'
        diff1=mf.dtgdiff(dtg1,dtg)
        if(diff1 > 0.0 ):
            self.tautype='alltau'
        else:
            self.tautype='wgrib'

        if(hasattr(self,'dmodelType')):
            if(self.dmodelType == 'w2flds'): self.tautype='wgrib'

        if(self.tautype == 'alltau'):
            self.dmask="%s.%s.%s"%(self.lmodel,dtg,self.gribtype)
        else:
            self.dmask="%s.%s.f???.%s"%(self.model,dtg,self.gribtype)
            self.dsetmask="%s.%s.f%%f3.%s"%(self.model,dtg,self.gribtype)



    def gname2tau(self,file,dtg,dtg1='2009010100'):
        diff1=mf.dtgdiff(dtg1,dtg)
        if(diff1 > 0.0 ):
            tau=file.split('.')[-2][1:]
            tau=int(tau)
        else:
            tau=file.split('.')[-2][1:]
            tau=int(tau)
        return(tau)



    def setgmask(self,dtg,dtg1='2009010100'):

        diff1=mf.dtgdiff(dtg1,dtg)
        if(diff1 > 0.0 ):
            self.gmask="%s_meto.grib"%(dtg)
        else:
            self.gmask="%s.%s.t???.grb"%(self.dmodel,dtg)



    def setctlgridvar(self,dtg,dtg1='2009010100'):

        hh=dtg[8:10]
        self.btau=0

        if(self.gribtype == 'grb1'):

            diff1=mf.dtgdiff(dtg1,dtg)
            if(diff1 > 0.0 ):

                if(hh == '00' or hh == '12'):
                    self.etau=168
                    self.dtau=6
                else:
                    self.etau=60
                    self.dtau=6

                optiondtype='''dtype grib 255
zdef 7 levels 1000 925 850 700 500 300 200
# profile in hPa
'''
                latlongrid='''ydef 481 linear -90.0 0.375
xdef 640 linear 0.0 0.563'''

                vars='''vars 11
pr   0   61,  1,0  ** Total precipitation [kg/m^2]
prc  0  140,  1,0  ** Categorical rain [yes=1;no=0]
zg   7    7,100,0  ** Geopotential height [gpm]
psl  0    2,102,0  ** Pressure reduced to MSL [Pa]
hur  7   52,100,0  ** Relative humidity [%]
tas  0   11,  1,0  ** Temp. [K]
ta   7   11,100,0  ** Temp. [K]
uas  0   33,  1,0  ** u wind [m/s]
ua   7   33,100,0  ** u wind [m/s]
vas  0   34,  1,0  ** v wind [m/s]
va   7   34,100,0  ** v wind [m/s]
endvars'''

            else:

                if(hh == '00' or hh == '12'):
                    self.etau=168
                    self.dtau=6
                    self.nfields=760
                else:
                    self.etau=48
                    self.dtau=6
                    self.nfields=440

                optiondtype='''options template
dtype grib 255
zdef 12 levels 1000 950 925 850 700 500 400 300 250 200 150 100 
# profile in hPa
'''
                latlongrid='''ydef 324 linear -89.722000 0.556
xdef 432 linear -18.750000 0.833000'''

                vars='''vars 28
pr      0  61,  1,0  ** Total precipitation [kg/m^2]
bvfreq  0 138,  1,0  ** Brunt-Vaisala frequency^2 [1/s^2]
clc     0  72,  1,0  ** Convective cloud cover [%]
sno     0 143,  1,0  ** Categorical snow [yes=1;no=0]
cwork   0 146,  1,0  ** Cloud work function [J/kg]
zgmwl   0   6,  6,0  ** Geopotential [m^2/s^2]
clh     0  75,  1,0  ** High level cloud cover [%]
zg     12   7,100,0  ** Geopotential height [gpm]
zgmicao 0   5,  6,0  ** ICAO Standard Atmosphere Reference Height [M]
cll     0  73,  1,0  ** Low level cloud cover [%]
clm     0  74,  1,0  ** Mid level cloud cover [%]
prr     0  59,  1,0  ** Precipitation rate [kg/m^2/s]
pamwl   0   1,  6,0  ** Pressure [Pa]
patrop  0   1,  7,0  ** Pressure [Pa]
psl     0   2,102,0  ** Pressure reduced to MSL [Pa]
hur    12  52,100,0  ** Relative humidity [%]
msof    0 144,  1,0  ** Volumetric soil moisture [fraction]
qas     0  51,105,2  ** Specific humidity [kg/kg]
ta     12  11,100,0  ** Temp. [K]
tas     0  11,105,2  ** Temp. [K]
tatrop  0  11,  7,0  ** Temp. [K]
ugwd    0 147,  1,0  ** Zonal gravity wave stress [N/m^2]
ua     12  33,100,0  ** u wind [m/s]
uas     0  33,105,10 ** u wind [m/s]
uamwl   0  33,  6,0  ** u wind [m/s]
va     12  34,100,0  ** v wind [m/s]
vas     0  34,105,10 ** v wind [m/s]
vgwd    0  34,  6,0   ** v wind [m/s]
endvars'''


        self.ctlgridvar='''undef 1e+20
title ukm2 fields from nhc/ukmo
%s
%s
%s'''%(optiondtype,latlongrid,vars)

    def Model2PlotMinTau(self,dtg):

        dtghh=int(dtg[8:10])

        # taumin and tau forced to be the same because grib from ukmo is in one file...
        #
        if(dtghh == 0 or dtghh == 12):
            mintauPlot=144
        elif(dtghh == 6 or dtghh == 18):
            mintauPlot=60

        return(mintauPlot)





class Ngp2(Model2):


    pltdir='plt_fnmoc_ngp'
    pmodel='ngp'

    modelrestitle='T319|42km L30'
    modelDdtg=12
    modelgridres='1.0'
    modelprvar="""_prvar='pr*4'"""
    modelpslvar='psl*0.01'
    modeltitleAck1="FNMOC Data Courtesy of NCEP/NCO"
    modeltitleFullmod="FNMOC(NOGAPS)"

    etau=144
    dtau=6


    def __init__(self,model='ngp2',center='fnmoc',gribver=2):

        self.model=model
        self.dmodel=model
        self.dirmodel='nogaps'

        self.initModelCenter(center)
        self.initGribVer(gribver)

        self.tautype=None
        self.d2dir='/dat2/nwp2'

        self.location='kishou'
        self.tautype='wgrib'

        self.dmodelType=None        

        self.nfields=75
        self.nfieldsW2flds=41

        self.rundtginc=12

        self.adecksource='nhc,jtwc'
        self.adeckaid='ngps'

        self.nfields=74
        self.nfieldsW2flds=41

    def setMaxtau(self,dtg):
        hh=dtg[8:10]
        if(hh == '00' or hh == '12'):  self.maxtau=144
        else:    self.maxtau=-999
        return(self.maxtau)


    def name2tau(self,file,dtg=None):
        tau=file.split('.')[2][1:]
        tau=int(tau)
        return(tau)

    def setgmask(self,dtg,dtg1='2009010100'):
        diff1=mf.dtgdiff(dtg1,dtg)

        if(diff1 > 0.0 ):
            self.gmask="nogaps_%s*grib2"%(dtg)
        else:
            self.gmask="nogaps_%s*"%(dtg)

    def gname2tau(self,file,dtg,dtg1='2009010100'):
        diff1=mf.dtgdiff(dtg1,dtg)
        if(diff1 > 0.0 ):
            tau=file.split('.')[2][1:]
            tau=int(tau)
        else:
            tau=int(file[-3:])
        return(tau)


    def setxwgrib(self,dtg,dtg1='2009010100'):
        diff1=mf.dtgdiff(dtg1,dtg)
        if(diff1 > 0.0 ):
            self.nfields=71
            # -- min
            self.nfieldsW2flds=41
            self.xwgrib='wgrib2'
            self.dmask="*%s.%s.f???.%s"%(self.dmodel,dtg,self.gribtype)
            self.dsetmask="%s.%s.f%%f3.%s"%(self.dmodel,dtg,self.gribtype)

        else:
            # -- old form
            self.nfields=66
            self.nfieldsW2flds=68

            self.xwgrib='wgrib'
            self.dmask="*%s.%s.f???.%s"%(self.dmodel,dtg,self.gribtype)
            self.dsetmask="%s.%s.f%%f3.%s"%(self.dmodel,dtg,self.gribtype)



    def setctlgridvar(self,dtg):

        if(self.gribtype == 'grb1'):
            optiondtype='''options template
dtype grib
zdef 20 levels 1000 950 925 900 850 800 750 700 650 600 550 500 450 400 350 300 250 200 150 100 70
# profile in hPa
'''
            latlongrid='''xdef 360 linear   0.0 1.0
ydef 181 linear -90.0 1.0'''

            vars='''vars 12
vrta500   0  41,100,500  ** Absolute vorticity [/s]
prc       0  63,  1,  0  ** Convective precipitation [kg/m^2]
pr        0  61,  1,  0  ** Total precipitation [kg/m^2]
zg       20   7,100,  0 ** Geopotential height [gpm]
psl       0   2,102,  0  ** Pressure reduced to MSL [Pa]
hur      20  52,100,  0 ** Relative humidity [%]
ta       20  11,100,  0 ** Temp. [K]
ua       20  33,100,  0 ** u wind [m/s]
uas       0  33,105, 10 ** u wind [m/s]
va       20  34,100,  0 ** v wind [m/s]
vas       0  34,105, 10 ** v wind [m/s]
wap      20  39,100,  0 ** Pressure vertical velocity [Pa/s]
endvars'''


        elif(self.gribtype == 'grb2'):
            optiondtype='''options template pascals
dtype grib2
zdef 20 levels 100000 95000 92500 90000 85000 80000 75000 70000 65000 60000 55000 50000 45000 40000 35000 30000 25000 20000 15000 10000 7000
# profile in Pa'''

            latlongrid='''xdef 360 linear   0.0 1.0
ydef 181 linear -90.0 1.0'''

            vars='''vars 21
vrta500   0,100,50000   0,2,10 ** 500 mb Absolute Vorticity [1/s]
prc       0,  1,    0   0,1,10,1 ** surface Convective Precipitation [kg/m^2]
pr        0,  1,    0   0,1,8,1 ** surface Total Precipitation [kg/m^2]
zg       20,100         0,3,5 ** (1000 925 850 700 500.. 250 200 150 100 70) Geopotential Height [gpm]
zgmwl     0,  6,    0   0,3,5 ** max wind Geopotential Height [gpm]
pamwl     0,  6,    0   0,3,0 ** max wind Pressure [Pa]
parop     0,  7,    0   0,3,0 ** tropopause Pressure [Pa]
psl       0,101,    0   0,3,1 ** mean sea level Pressure Reduced to MSL [Pa]
hur      20,100         0,1,1 ** (1000 950 900 850 800.. 500 450 400 350 300) Relative Humidity [%]
ta       20,100         0,0,0 ** (1000 925 850 700 500.. 250 200 150 100 70) Temperature [K]
tas       0,103,    2   0,0,0 ** 2 m above ground Temperature [K]
tamwl     0,  6,    0   0,0,0 ** max wind Temperature [K]
tatrop    0,  7,    0   0,0,0 ** tropopause Temperature [K]
ua       20,100         0,2,2 ** (1000 925 850 700 500.. 250 200 150 100 70) U-Component of Wind [m/s]
uas       0,103,   10   0,2,2 ** 10 m above ground U-Component of Wind [m/s]
uamwl     0,  6,    0   0,2,2 ** max wind U-Component of Wind [m/s]
va       20,100         0,2,3 ** (1000 925 850 700 500.. 250 200 150 100 70) V-Component of Wind [m/s]
vas       0,103,   10   0,2,3 ** 10 m above ground V-Component of Wind [m/s]
vamwl     0,  6,    0   0,2,3 ** max wind V-Component of Wind [m/s]
wap      20,100         0,2,8 ** (1000 925 850 700 500.. 300 250 200 150 100) Vertical Velocity (Pressure) [Pa/s]
ws19      0,103,   19   0,2,1 ** 19 m above ground Wind Speed [m/s]
endvars'''

        self.ctlgridvar='''undef 1e+20
title ngp2.2007100112.f006.grb2
%s
%s
%s
###--- pr is mm/6h *4 = mm/d'''%(optiondtype,latlongrid,vars)


    def getDataTaus(self,dtg):

        dtghh=int(dtg[8:10])
        # -- ignore tau78 because it only has 17 fields
        if(dtghh == 0 or dtghh == 12):
            taus=range(0,72+1,6)+range(84,144+1,12)
        elif(dtghh == 6 or dtghh == 18):
            taus=range(0,72+1,6)+range(84,144+1,12)
        else:
            taus=[]

        return(taus)

class Ngpc(Model2):

    pltdir='plt_fnmoc_ngp'
    pmodel='ngp'

    modelrestitle='T319|42km L30'
    modelDdtg=12
    modelprvar="""_prvar='pr*4'"""
    modelpslvar='psl*0.01'

    modelgridres='0.5'
    modelres=modelgridres.replace('.','')

    model='ngpc'
    center='fnmoc'

    pltdir='plt_fnmoc_ngpc'
    pmodel='ngpc'

    modelPlotTaus=[0,6,12,18,24,30,36,42,48,60,72,84,96,108,120,132,144,156,168]
    # -- special case
    gmodname="%s%s"%('ngp',modelres)

    modeltitleAck1="FNMOC Data Courtesy GACIPS"
    modeltitleFullmod="FNMOC(NOGAPS)"



    def __init__(self,gribver=1):

        self.dmodel=self.model
        self.dirmodel='ngp05cagips'

        self.initModelCenter(self.center)
        self.initGribVer(gribver)

        self.tautype=None
        self.d2dir='/dat2/nwp2'

        self.location='kishou'
        self.tautype='wgrib'

        self.dmodelType=None        

        self.nfields=62
        self.nfieldsW2flds=54

        self.rundtginc=6

        self.adecksource='nhc,jtwc'
        self.adeckaid='ngps'


    def setMaxtau(self,dtg):
        hh=dtg[8:10]
        if(hh == '00' or hh == '12'):  self.maxtau=180
        else:    self.maxtau=-999
        return(self.maxtau)


    def name2tau(self,file,dtg=None):
        tau=file.split('.')[2][1:]
        tau=int(tau)
        return(tau)

    def setgmask(self,dtg,dtg1='2009010100'):
        diff1=mf.dtgdiff(dtg1,dtg)

        if(diff1 > 0.0 ):
            self.gmask="nogaps_%s*grib2"%(dtg)
        else:
            self.gmask="ngpc.*%s*.grb1"%(dtg)

    def gname2tau(self,file,dtg,dtg1='2009010100'):
        diff1=mf.dtgdiff(dtg1,dtg)
        if(diff1 > 0.0 ):
            tau=file.split('.')[2][1:]
            tau=int(tau)
        else:
            tau=int(file[-3:])
        return(tau)


    def setxwgrib(self,dtg,dtg1='2009010100'):
        diff1=mf.dtgdiff(dtg1,dtg)
        if(diff1 > 0.0 ):
            self.nfields=62
            # -- min
            self.nfieldsW2flds=60
            self.xwgrib='wgrib'
            self.dmask="*%s.%s.f???.%s"%(self.dmodel,dtg,self.gribtype)
            self.dsetmask="%s.%s.f%%f3.%s"%(self.dmodel,dtg,self.gribtype)

        else:
            self.nfields=66
            self.nfieldsW2flds=68

            self.xwgrib='wgrib'
            self.dmask="*%s.%s.f???.%s"%(self.dmodel,dtg,self.gribtype)
            self.dsetmask="%s.%s.f%%f3.%s"%(self.dmodel,dtg,self.gribtype)

    def setctlgridvar(self,dtg):

        if(self.gribtype == 'grb1'):
            optiondtype='''options template
dtype grib
zdef 20 levels 1000 950 925 900 850 800 750 700 650 600 550 500 450 400 350 300 250 200 150 100 70
# profile in hPa
'''
            latlongrid='''xdef 360 linear   0.0 1.0
ydef 181 linear -90.0 1.0'''

            vars='''vars 12
vrta500   0  41,100,500  ** Absolute vorticity [/s]
prc       0  63,  1,  0  ** Convective precipitation [kg/m^2]
pr        0  61,  1,  0  ** Total precipitation [kg/m^2]
zg       20   7,100,  0 ** Geopotential height [gpm]
psl       0   2,102,  0  ** Pressure reduced to MSL [Pa]
hur      20  52,100,  0 ** Relative humidity [%]
ta       20  11,100,  0 ** Temp. [K]
ua       20  33,100,  0 ** u wind [m/s]
uas       0  33,105, 10 ** u wind [m/s]
va       20  34,100,  0 ** v wind [m/s]
vas       0  34,105, 10 ** v wind [m/s]
wap      20  39,100,  0 ** Pressure vertical velocity [Pa/s]
endvars'''


        elif(self.gribtype == 'grb2'):
            optiondtype='''options template pascals
dtype grib2
zdef 20 levels 100000 95000 92500 90000 85000 80000 75000 70000 65000 60000 55000 50000 45000 40000 35000 30000 25000 20000 15000 10000 7000
# profile in Pa'''

            latlongrid='''xdef 360 linear   0.0 1.0
ydef 181 linear -90.0 1.0'''

            vars='''vars 21
vrta500   0,100,50000   0,2,10 ** 500 mb Absolute Vorticity [1/s]
prc       0,  1,    0   0,1,10,1 ** surface Convective Precipitation [kg/m^2]
pr        0,  1,    0   0,1,8,1 ** surface Total Precipitation [kg/m^2]
zg       20,100         0,3,5 ** (1000 925 850 700 500.. 250 200 150 100 70) Geopotential Height [gpm]
zgmwl     0,  6,    0   0,3,5 ** max wind Geopotential Height [gpm]
pamwl     0,  6,    0   0,3,0 ** max wind Pressure [Pa]
parop     0,  7,    0   0,3,0 ** tropopause Pressure [Pa]
psl       0,101,    0   0,3,1 ** mean sea level Pressure Reduced to MSL [Pa]
hur      20,100         0,1,1 ** (1000 950 900 850 800.. 500 450 400 350 300) Relative Humidity [%]
ta       20,100         0,0,0 ** (1000 925 850 700 500.. 250 200 150 100 70) Temperature [K]
tas       0,103,    2   0,0,0 ** 2 m above ground Temperature [K]
tamwl     0,  6,    0   0,0,0 ** max wind Temperature [K]
tatrop    0,  7,    0   0,0,0 ** tropopause Temperature [K]
ua       20,100         0,2,2 ** (1000 925 850 700 500.. 250 200 150 100 70) U-Component of Wind [m/s]
uas       0,103,   10   0,2,2 ** 10 m above ground U-Component of Wind [m/s]
uamwl     0,  6,    0   0,2,2 ** max wind U-Component of Wind [m/s]
va       20,100         0,2,3 ** (1000 925 850 700 500.. 250 200 150 100 70) V-Component of Wind [m/s]
vas       0,103,   10   0,2,3 ** 10 m above ground V-Component of Wind [m/s]
vamwl     0,  6,    0   0,2,3 ** max wind V-Component of Wind [m/s]
wap      20,100         0,2,8 ** (1000 925 850 700 500.. 300 250 200 150 100) Vertical Velocity (Pressure) [Pa/s]
ws19      0,103,   19   0,2,1 ** 19 m above ground Wind Speed [m/s]
endvars'''

        self.ctlgridvar='''undef 1e+20
title ngpc.2007100112.f006.grb2
%s
%s
%s
###--- pr is mm/6h *4 = mm/d'''%(optiondtype,latlongrid,vars)

class Navg(Ngpc):

    modelrestitle='T425|31km L60'
    modelDdtg=6
    modelgridres='0.5'
    modelprvar="""_prvar='pr*4'"""
    modelpslvar='psl*0.01'
    modeltitleAck1="FNMOC Data Courtesy NCEP"
    modeltitleFullmod="FNMOC(NAVGEM)"

    etau=180
    dtau=6

    pltdir='plt_fnmoc_navg'
    pmodel='navg'
    #gribver=1 # cagips
    gribver=2
    doLn=0
    
    model='navg'
    center='fnmoc'
    
    regridTracker=0.5

    def __init__(self,bdir2=None):

        self.dmodel='navgem'
        self.lmodel='navgem'
        self.dirmodel='nav05cagips'

        if(bdir2 != None): self.bdir2=bdir2


        self.initModelCenter(self.center)
        self.initGribVer(self.gribver)
        self.gribtype='grib2' # override standard

        self.tautype=None
        self.d2dir='/dat2/nwp2'

        self.location='kishou'
        self.tautype='wgrib'

        self.dmodelType=None        

        self.rundtginc=6

        self.adecksource='nhc,jtwc'
        self.adeckaid='navg'

        self.nfields=20
        self.nfieldsW2flds=60
        self.nfieldsW2flds=91  # when using from ncep
        self.bddir=self.w2fldsSrcDir
        

    def getDataTaus(self,dtg):

        self.dtau=6
        dtghh=int(dtg[8:10])
        if(dtghh == 0 or dtghh == 12):
            self.etau=180
            self.btau=0
        elif(dtghh == 6 or dtghh == 18):
            self.etau=144
            self.etau=180 # - ncep source
            self.btau=0

        taus=range(self.btau,self.etau+1,self.dtau)

        return(taus)

    def setxwgrib(self,dtg):
        
        if(MF.is0012Z(dtg)): 
            self.nfields=20
            self.nfieldsW2flds=60
        else:
            self.nfields=20
            self.nfieldsW2flds=60
        self.xwgrib='wgrib2'
        #self.dmask="*%s.%s.f???.%s"%(self.dmodel,dtg,self.gribtype)
        #self.dsetmask="%s.%s.f%%f3.%s"%(self.dmodel,dtg,self.gribtype)

        self.dmodel='navgem'
        self.dmask="*%s_%sf???.%s"%(self.dmodel,dtg,self.gribtype)
        #self.dsetmask="%s.%s.f%%f3.%s"%(self.dmodel,dtg,self.gribtype)
        self.dsetMaskOverride=1
        
        self.grbmask="%s_%s*.%s"%(self.dmodel,dtg,self.gribtype)
        self.gmask="%s_%s*.%s"%(self.dmodel,dtg,self.gribtype)
        self.dmask=self.gmask

    def setprvar(self,dtg=None,tau=None,source='ncep'):

        modelprvar=self.modelprvar
        if(tau == 0):
            modelprvar="""_prvar='pr(t+1)*4'"""

        return(modelprvar)
    
    def gname2tau(self,ffile,dtg):

        yyyy=dtg[0:4]
        mm=dtg[4:6]

        lf=len(ffile)
        lfe=lf-10
        lfb=lfe-6
        vmmddhh=ffile[lfb:lfe]
        vmm=vmmddhh[0:2]
        if(vmm == '01' and mm == '12'):
            vdtg=str(int(yyyy+1))+vmmddhh
        else:
            vdtg=yyyy+vmmddhh
        tau=mf.dtgdiff(dtg,vdtg)
        tau=int(tau)

        return(tau)

    


class Ngpj(Ngpc):

    modelrestitle='T239|N180 L30'
    modelDdtg=12
    modelgridres='0.5'
    modelprvar="""_prvar='pr*4'"""
    modelpslvar='psl*0.01'
    modeltitleAck1="FNMOC Data Courtesy GACIPS"
    modeltitleFullmod="FNMOC(NOGAPS)"

    etau=180
    dtau=6

    pltdir='plt_fnmoc_ngp'
    pmodel='ngp'

    def __init__(self,model='ngpj',center='fnmoc',gribver=1):

        self.model=model
        self.dmodel=model
        self.dirmodel='ngp05jtwc'

        self.initModelCenter(center)
        self.initGribVer(gribver)

        self.tautype=None
        self.d2dir='/dat2/nwp2'

        self.location='kishou'
        self.tautype='wgrib'

        self.dmodelType=None        


        self.rundtginc=6

        self.adecksource='nhc,jtwc'
        self.adeckaid='ngps'

    def setxwgrib(self,dtg):
        if(MF.is0012Z(dtg)): 
            self.nfields=20
            self.nfieldsW2flds=20
        else:
            self.nfields=20
            self.nfieldsW2flds=20
        self.xwgrib='wgrib'
        self.dmask="*%s.%s.f???.%s"%(self.dmodel,dtg,self.gribtype)
        self.dsetmask="%s.%s.f%%f3.%s"%(self.dmodel,dtg,self.gribtype)



class Gfsc(Gfs2):

    pltdir='plt_ncep_gfsc'
    pmodel='gfsc'


    def __init__(self,model='gfsc',center='ncep',gribver=1):

        self.model=model
        # three possible names for the model
        self.dmodel=self.model
        self.dirmodel=self.model

        self.initModelCenter(center)
        self.initGribVer(gribver)


        self.tautype='wgrib'

        self.modelrestitle='T382|N286 L64'
        self.modelDdtg=6
        self.modelgridres='0.5'
        self.modelprvar="""_prvar='pr*4'"""
        self.modelpslvar='psl*0.01'

        self.modeltitleAck1="NCEP GFS courtesy FNMOC/CAGIPS"
        self.modeltitleFullmod="NCEP(GFS)"

        self.btau=0
        self.etau=168
        self.dtau=6

        self.rundtginc=6

        self.adecksource='ncep'
        self.adeckaid='avno'

        self.nfields=62
        self.nfieldsW2flds=55
        
    def setxwgrib(self,dtg):

        self.xwgrib='wgrib'
        self.dmask="%s.%s.f???.%s"%(self.dmodel,dtg,self.gribtype)
        self.dsetmask="%s.%s.f%%f3.%s"%(self.dmodel,dtg,self.gribtype)


class Gfsenkf_t254(Gfs2):


    def __init__(self,model='gfsenkf_t254',center='ncep',gribver=1):

        self.model=model
        # three possible names for the model
        self.dmodel=self.model
        self.dirmodel=self.model

        self.initModelCenter(center)
        self.initGribVer(gribver)


        self.tautype='wgrib'

        self.modelrestitle='T382|N286 L64'
        self.modelDdtg=6
        self.modelgridres='0.5'
        self.modelprvar="""_prvar='pr*4'"""
        self.modelpslvar='psl*0.01'

        self.modeltitleAck1="NCEP GFS courtesy FNMOC/CAGIPS"
        self.modeltitleFullmod="NCEP(GFS)"

        self.btau=0
        self.etau=168
        self.dtau=6

        self.rundtginc=6

        self.adecksource='ncep'
        self.adeckaid='avno'

        self.nfields=62
        self.nfieldsW2flds=55

    def setxwgrib(self,dtg):

        self.nfields=57
        self.nfieldsW2flds=49

        self.xwgrib='wgrib'
        self.dmask="*.f???.grb1"%(dtg)
        self.dsetmask="%s.%s.f%%f3.grb1"%(self.dmodel,dtg)

    def setgmask(self,dtg):
        self.gmask="*%s*.grb1"%(dtg)



class Jmac(Model2):


    def __init__(self,model='jmac',center='jma',gribver=1):

        self.model=model
        self.dmodel=self.model
        self.dirmodel=self.model

        self.initModelCenter(center)
        self.initGribVer(gribver)

        self.tautype='wgrib'

        self.modelrestitle='T382|N286 L64'
        self.modelDdtg=6
        self.modelgridres='0.5'
        self.modelprvar="""_prvar='pr*4'"""
        self.modelpslvar='psl*0.01'

        self.modeltitleAck1="JMA GSM courtesy FNMOC/CAGIPS"
        self.modeltitleFullmod="JMA(GSM)"

        self.btau=0
        self.etau=168
        self.dtau=6

        self.rundtginc=6

        self.adecksource='jma'
        self.adeckaid='jgsm'


    def setMaxtau(self,dtg):
        hh=dtg[8:10]
        if(hh == '00'):  self.maxtau=84
        if(hh == '12'):  self.maxtau=168
        else:    self.maxtau=0
        return(self.maxtau)



    def name2tau(self,file,dtg):
        ib=len(self.dmodel.split('.'))+1
        try:
            tau=file.split('.')[ib][1:]
            tau=int(tau)
        except:
            tau=None
        return(tau)

    def setgmask(self,dtg,dtg1='2009010100'):
        julday=int(mf.Dtg2JulianDay(dtg))
        yy=dtg[2:4]
        hh=dtg[8:10]

        diff1=mf.dtgdiff(dtg1,dtg)
        if(diff1 > 0.0 ):
            self.gmask="%2s%03d%2s*"%(yy,julday,hh)
        else:
            self.gmask="ZY0X1W2_%s*"%(dtg)


    def setxwgrib(self,dtg):

        self.nfields=1
        self.nfieldsW2flds=1

        self.gribtype='grb1'
        self.xwgrib='wgrib'
        self.dmask="%s.%s.f???.%s"%(self.dmodel,dtg,self.gribtype)
        self.dsetmask="%s.%s.f%%f3.%s"%(self.dmodel,dtg,self.gribtype)


    def setctlgridvar(self,dtg):

        if(self.gribtype == 'grb1'):
            optiondtype='''options template
dtype grib
zdef 10 levels 1000 925 850 700 500 300 250 200 150 100 
# profile in hPa
'''
            vars='''vars 19
prc    0  63,  1,0   ** Convective precipitation [kg/m^2]
pr     0  61,  1,0   ** Total precipitation [kg/m^2]
zg    10   7,100,0   ** Geopotential height [gpm]
psl    0   2,102,0   ** Pressure reduced to MSL [Pa]
hur   10  52,100,0   ** Relative humidity [%]
clt    0  71,211,0   ** Total cloud cover [%]
cll    0  71,214,0   ** Total cloud cover [%]
clm    0  71,224,0   ** Total cloud cover [%]
clh    0  71,234,0   ** Total cloud cover [%]
cltt   0  71,244,0   ** Total cloud cover [%]
tmx2m  0  15,105,2   ** Max. temp. [K]
tmn2m  0  16,105,2   ** Min. temp. [K]
tas    0  11,105,2   ** Temp. [K]
ua    10  33,100,0   ** u wind [m/s]
uas    0  33,105,10  ** u wind [m/s]
rlut   0 212,  8,0   ** Upward long wave flux [W/m^2]
va    10  34,100,0   ** v wind [m/s]
vas    0  34,105,10  ** v wind [m/s]
wap   10  39,100,0   ** Pressure vertical velocity [Pa/s]
endvars'''


        elif(self.gribtype == 'grb2'):
            optiondtype='''options template pascals
dtype grib2
zdef 26 levels 100000 97500 95000 92500 90000 85000 80000 75000 70000 65000 60000 55000 50000 45000 40000 35000 30000 25000 20000 15000 10000 7000 5000 3000 2000 1000
# profile in Pa'''

            vars='''vars 23
prc        0,  1,  0   0,  1, 10,  1 ** surface Convective Precipitation [kg/m^2]
pr         0,  1,  0   0,  1,  8,  1 ** surface Total Precipitation [kg/m^2]
prw        0,200,  0   0,  1,  3     ** entire atmosphere (considered as a single layer) Precipitable Water [kg/m^2]
prcr       0,  1,  0   0,  1,196,  0 ** surface Convective Precipitation Rate [kg/m^2/s]
prr        0,  1,  0   0,  1,  7,  0 ** surface Precipitation Rate [kg/m^2/s]
zg        26,100       0,  3,  5     ** (1000 975 950 925 900.. 70 50 30 20 10) Geopotential Height [gpm]
psl        0,101,  0   0,  3,  1     ** mean sea level Pressure Reduced to MSL [Pa]
hur       21,100       0,  1,  1     ** (1000 975 950 925 900.. 300 250 200 150 100) Relative Humidity [%%]
clt        0,200,  0   0,  6,  1,  0 ** entire atmosphere (considered as a single layer) Total Cloud Cover [%%]
cll        0,214,  0   0,  6,  1,  0 ** low cloud layer Total Cloud Cover [%%]
clm        0,224,  0   0,  6,  1,  0 ** middle cloud layer Total Cloud Cover [%%]
clh        0,234,  0   0,  6,  1,  0 ** high cloud layer Total Cloud Cover [%%]
cltc       0,244,  0   0,  6,  1     ** convective cloud layer Total Cloud Cover [%%]
tasmx      0,103,  2   0,  0,  4     ** 2 m above ground Maximum Temperature [K]
tasmn      0,103,  2   0,  0,  5     ** 2 m above ground Minimum Temperature [K]
tas        0,103,  2   0,  0,  0     ** 2 m above ground Temperature [K]
ua        26,100       0,  2,  2     ** (1000 975 950 925 900.. 70 50 30 20 10) U-Component of Wind [m/s]
uas        0,103, 10   0,  2,  2     ** 10 m above ground U-Component of Wind [m/s]
rlut       0,  8,  0   0,  5,193,  0 ** top of atmosphere Upward Long-Wave Rad. Flux [W/m^2]
va        26,100       0,  2,  3     ** (1000 975 950 925 900.. 70 50 30 20 10) V-Component of Wind [m/s]
ta        26,100       0,  0,  0     ** (1000 975 950 925 900.. 70 50 30 20 10) Temperature [K]
vas        0,103,10    0,  2,  3     ** 10 m above ground V-Component of Wind [m/s]
wap       21,100       0,  2,  8     ** (1000 975 950 925 900.. 300 250 200 150 100) Vertical Velocity (Pressure) [Pa/s]
endvars'''

        latlongrid='''xdef 720 linear   0.0 0.5
ydef 361 linear -90.0 0.5'''

        self.ctlgridvar='''undef 1e+20
title jmac.2007100112.f006.grb2
%s
%s
%s'''%(optiondtype,latlongrid,vars)


class uKmc(uKm2):

    def __init__(self,model='ukmc',center='ukmo',gribver=1):

        self.model=model
        self.dmodel='ukm'
        self.dirmodel=model
        self.archdirmodel='ukm'
        self.lmodel=model

        self.location='kishou'

        self.initModelCenter(center)
        self.initGribVer(gribver)

        self.archmodelcenter="%s/%s"%(self.center,self.archdirmodel)

        self.tautype='alltau'

        if(mf.find(self.dmodel,'w2flds')): self.tautype='wgrib'

        self.nfields=31
        self.nfieldsW2flds=22

        self.modelrestitle='0.56x0.87|N162L50'
        self.modelDdtg=6
        self.modelgridres='0.7'

        self.xwgrib='wgrib'
        self.location='kaze'

        # if ddtg between runs is 12 h
        #

        self.modelprvar12="""
_prvar='pr(t+0)*2'
if(_tau = 0)
  _prvar='pr(t+0)*2'
endif
if(_tau = 6)
  _prvar='((const(pr(t-1),0,-u)+pr(t+1))*0.5)*2'
endif
"""
        self.modelprvar="""
_prvar='pr(t+0)*2'
if(_tau = 0)
  _prvar='((const(pr(t-1),0,-u)+pr(t+1))*0.5)*2'
endif
if(_tau = 6)
  _prvar='((const(pr(t-1),0,-u)+pr(t+1))*0.5)*2'
endif
"""
        self.modelprvar00="""_prvar='((const(pr(t-1),0,-u)+pr(t+1))*0.5)*2'"""
        self.modelprvar06="""_prvar='((const(pr(t-1),0,-u)+pr(t+1))*0.5)*2'"""
        self.modelprvar="""_prvar='pr(t+0)*2'"""

        self.modelpslvar='psl*0.01'
        self.modeltitleAck1="UKMO Data Licenced through Julian Heming, UKMO"
        self.modeltitleFullmod="UKMO(UM)"

        self.rundtginc=12

        self.adecksource='nhc,jtwc'
        self.adeckaid='egrr'
        
        self.tryarch=0



    def name2tau(self,file,dtg=None,dtg1='2009010100'):

        if(dtg != None):
            hh=dtg[8:10]
            diff1=mf.dtgdiff(dtg1,dtg)
        else:
            diff1=-1.0

        if(diff1 > 0.0 ):
            if(hh == '00' or hh == '12'):
                tau=144
                self.nfields=760
                self.nfields=22
                ctau=file.split('.')[-2][1:]
                tau=int(ctau)
            else:
                tau=60
                self.nfields=440
                self.nfields=22
                ctau=file.split('.')[-2][1:]
                tau=int(ctau)
        else:
            ctau=file.split('.')[-2][1:]
            tau=int(ctau)
        return(tau)


    def setxwgrib(self,dtg,dtg1='2009010100'):

        self.tautype='wgrib'

        if(hasattr(self,'dmodelType')):
            if(self.dmodelType == 'w2flds'): self.tautype='wgrib'

        self.dmask="%s.%s.f???.%s"%(self.lmodel,dtg,self.gribtype)
        self.dsetmask="%s.%s.f%%f3.%s"%(self.lmodel,dtg,self.gribtype)



class Ohc(Model2):

    modelrestitle='02deg'
    modelDdtg=0
    modelgridres='0.2'
    modelprvar=None
    modelpslvar=None
    modeltitleAck1="FNMOC Data Courtesy GACIPS"
    modeltitleFullmod="FNMOC(NCODA)"

    etau=0
    dtau=6

    dofimlsgrib=0


    def __init__(self,model='ohc',center='fnmoc',gribver=1):

        self.model=model
        self.dmodel=model
        self.dirmodel='ocean/ohc'

        self.initModelCenter(center)
        self.initGribVer(gribver)

        self.tautype=None
        self.d2dir='/dat2/nwp2'

        self.location='kishou'
        self.tautype='wgrib'

        self.dmodelType=None        

        self.nfields=1
        self.nfieldsW2flds=1

        self.rundtginc=12

    def setMaxtau(self,dtg):
        hh=dtg[8:10]
        if(hh == '00' or hh == '12'):  self.maxtau=0
        else:    self.maxtau=-999
        return(self.maxtau)


    def setgmask(self,dtg):
        self.gmask="ohcnogaps_%s*grib2"%(dtg)

    def gname2tau(self,file,dtg):
        tau=file.split('.')[2][1:]
        tau=int(tau)
        return(tau)

    def name2tau(self,file,dtg=None):
        tau=file.split('.')[2][1:]
        tau=int(tau)
        return(tau)

    def setxwgrib(self,dtg):
        self.nfields=2
        self.nfieldsW2flds=2
        self.xwgrib='wgrib'
        self.dmask="%s*.%s.f???.%s"%(self.dmodel,dtg,self.gribtype)
        self.dsetmask="%s.%s.f%%f3.%s"%(self.dmodel,dtg,self.gribtype)

    def setctlgridvar(self,dtg):

        if(self.gribtype == 'grb1'):
            optiondtype='''options template
dtype grib
zdef    1 levels 0
'''
            latlongrid='''ydef  350 linear -30.0 0.20
xdef 1576 linear 35.0 0.20'''

            vars='''vars 2
ohc       0 167,  1  ,0  ** OHC [kJ/cm^2]
d26c      0 242,  4, 26  ** depth of 26C ocean isotherm [m]
endvars'''


        elif(self.gribtype == 'grb2'):
            print 'EEE grib2 vars not defined for OHC'
            sys.exit()

        self.ctlgridvar='''undef 1e+20
title ohc.2007100112.f006.grb2
%s
%s
%s'''%(optiondtype,latlongrid,vars)


class Ocn(Model2):

    modelrestitle='025deg'
    modelDdtg=0
    modelgridres='0.25'
    modelprvar=None
    modelpslvar=None
    modeltitleAck1="FNMOC Data Courtesy GACIPS"
    modeltitleFullmod="FNMOC(NCODA)"

    etau=0
    dtau=6

    dofimlsgrib=0


    def __init__(self,model='ocn',center='fnmoc',gribver=1):

        self.model=model
        self.dmodel=model
        self.dirmodel='ocean/sst'

        self.initModelCenter(center)
        self.initGribVer(gribver)

        self.tautype=None
        self.d2dir='/dat2/nwp2'

        self.location='kishou'
        self.tautype='wgrib'

        self.dmodelType=None        

        self.nfields=1
        self.nfieldsW2flds=1

        self.rundtginc=24

    def setMaxtau(self,dtg):
        hh=dtg[8:10]
        if(hh == '00' or hh == '12'):  self.maxtau=0
        else:    self.maxtau=-999
        return(self.maxtau)


    def setgmask(self,dtg):
        self.gmask="ocnnogaps_%s*grib2"%(dtg)

    def gname2tau(self,file,dtg):
        tau=file.split('.')[2][1:]
        tau=int(tau)
        return(tau)

    def name2tau(self,file,dtg=None):
        tau=file.split('.')[2][1:]
        tau=int(tau)
        return(tau)


    def setxwgrib(self,dtg):
        self.nfields=2
        self.nfieldsW2flds=2
        self.xwgrib='wgrib'
        self.gribtype='grb1'
        self.dmask="*%s.%s.f???.grb1"%(self.dmodel,dtg)
        self.dsetmask="%s.%s.f%%f3.grb1"%(self.dmodel,dtg)

    def setctlgridvar(self,dtg):

        if(self.gribtype == 'grb1'):
            optiondtype='''options template
dtype grib
zdef    1 levels 0
'''
            latlongrid='''ydef  721 linear -90.0 0.25
xdef 1440 linear   0.0 0.25'''

            vars='''vars 2
sst       0 80,  1  ,0  ** SST [K]
sic       0 91,  1  ,0  ** SIC [fraction]
endvars'''


        elif(self.gribtype == 'grb2'):
            print 'EEE grib2 vars not defined for OCN'
            sys.exit()

        self.ctlgridvar='''undef 1e+20
title ocn.2007100112.f006.grb2
%s
%s
%s'''%(optiondtype,latlongrid,vars)





class Ww3(Ocn):

    modelrestitle='025deg'
    modelDdtg=0
    modelgridres='0.25'
    modelprvar=None
    modelpslvar=None
    modeltitleAck1="FNMOC Data Courtesy GACIPS"
    modeltitleFullmod="FNMOC(WW3)"

    etau=180
    dtau=6

    dofimlsgrib=0


    def __init__(self,model='ww3',center='fnmoc',gribver=1):

        self.model=model
        self.dmodel=model
        self.dirmodel='ocean/ww3'

        self.initModelCenter(center)
        self.initGribVer(gribver)

        self.tautype=None
        self.d2dir='/dat2/nwp2'

        self.location='kishou'
        self.tautype='wgrib'

        self.dmodelType=None        

        self.nfields=1
        self.nfieldsW2flds=1

        self.rundtginc=12

    def setMaxtau(self,dtg):
        hh=dtg[8:10]
        if(hh == '00' or hh == '12'):  self.maxtau=180
        else:    self.maxtau=-999
        return(self.maxtau)


    def setxwgrib(self,dtg):

        self.xwgrib='wgrib'
        self.dmask="%s*.%s.f???.%s"%(self.dmodel,dtg,self.gribtype)
        self.dsetmask="%s.%s.f%%f3.%s"%(self.dmodel,dtg,self.gribtype)

    def setctlgridvar(self,dtg):

        if(self.gribtype == 'grb1'):
            optiondtype='''options template
dtype grib
zdef    1 levels 0
'''
            latlongrid='''ydef  721 linear -90.0 0.25
xdef 1440 linear   0.0 0.25'''

            vars='''vars 1
wvzs      0 100,  1,  0  ** Sig height of wind waves and swell [m]
endvars'''


        elif(self.gribtype == 'grb2'):
            print 'EEE grib2 vars not defined for WW3'
            sys.exit()

        self.ctlgridvar='''undef 1e+20
title ww3.2007100112.f006.grb2
%s
%s
%s'''%(optiondtype,latlongrid,vars)




class Ecmn(Ecm2):

    modelrestitle='T`bl`n|N400 L91'
    modelDdtg=12
    modelgridres='1.0'
    modelres=modelgridres.replace('.','')

    modelprvar="""_prvar='(( const(pr(t+0),0,-u)-const(pr(t-1),0,-u) )*4*1000)'"""
    modelpslvar='psl*0.01'

    model='ecmn'
    center='ecmwf'

    dmodel=model
    pmodel=model

    pltdir='plt_ecmwf_ecm'
    pmodel='ecm'

    modelPlotTaus=[0,6,12,18,24,30,36,42,48,60,72,84,96,108,120,132,144,156,168]
    gmodname="%s%s"%(pmodel,modelres)

    modeltitleAck1="ECMWF Data Courtesy of NCO/NWS"
    modeltitleFullmod="ECMWF(IFS)"


    def __init__(self,gribver=2):

        self.dirmodel='ecmo_nws'

        self.initModelCenter(self.center)
        self.initGribVer(gribver)

        self.tautype=None
        self.d2dir='/dat2/nwp2'

        self.nfields=48
        self.nfieldsW2flds=47

        self.etau=240
        self.dtau=6

        self.rundtginc=12

        self.adecksource='tmtrkN'
        self.adeckaid=self.model
        self.dattaus=range(self.btau,self.etau+1,self.dtau)
        self.dattaus=range(0,48+1,6)+range(48,240+1,12)



    def setprvar(self,dtg=None,tau=None):
        modelprvar=self.modelprvar
        if(tau == 0):
            modelprvar="""_prvar='(( const(pr(t+1),0,-u)-const(pr(t-0),0,-u) )*4*1000)'"""
        elif(tau >= 48):
            modelprvar="""_prvar='(( const(pr(t+0),0,-u)-const(pr(t-2),0,-u) )*2*1000)'"""
        else:
            modelprvar="""_prvar='(( const(pr(t+0),0,-u)-const(pr(t-1),0,-u) )*4*1000)'"""

        return(modelprvar)


    def setMaxtau(self,dtg):
        hh=dtg[8:10]
        if(hh == '00' or hh == '12'):  self.maxtau=240
        else:    self.maxtau=-999
        return(self.maxtau)


    def name2tau(self,file,dtg=None):
        try:
            tau=file.split('.')[2][1:]
            tau=int(tau)
        except:
            tau=None
        return(tau)

    def gname2tau(self,file,dtg,dtg1='2009010100'):
        diff1=mf.dtgdiff(dtg1,dtg)
        if(diff1 > 0.0 ):
            tau=file.split('.')[2][1:]
            tau=int(tau)
        else:
            tau=int(file[-3:])
        return(tau)

    def setgmask(self,dtg):
        self.gmask="*.%s_%s*"%(dtg[1:8],dtg[8:10])

    def setxwgrib(self,dtg):
        self.xwgrib='wgrib2'
        self.dmask="*%s.%s.f???.%s"%(self.dmodel,dtg,self.gribtype)
        self.dsetmask="*%s.%s.f%%f3.%s"%(self.dmodel,dtg,self.gribtype)





class Cmc2(Model2):

    pltdir='plt_cmc_cmc'
    pmodel='cmc'

    def __init__(self,model='cmc2',center='cmc',gribver=1):

        self.model=model
        self.dmodel='cmc'
        self.dirmodel='cmc'
        self.lmodel=model

        self.initModelCenter(center)
        self.initGribVer(gribver)

        self.tautype='wgrib'

        self.nfields=47
        self.nfieldsW2flds=36

        self.modelrestitle='T`bl`nuuuu|Nuu Luu'
        self.modelDdtg=12
        self.modelgridres='1.0'
        #self.modelprvar="""_prvar='( const(pr(t+2),0,-u)-const(pr(t-0),0,-u) )*2'"""
        self.modelprvar="""_prvar='( const(pr(t+0),0,-u)-const(pr(t-1),0,-u) )*4'"""
        self.modelpslvar='psl*0.01'
        self.modeltitleAck1="CMC Data Courtesy of NCEP/NCO"
        self.modeltitleFullmod="CMC(GEM7)"

        self.tbase=self.dmodel

        self.adecksource='ncep'
        self.adeckaid='cmc'

        self.rundtginc=12
        
        self.etau=240
        self.dtau=6


    # -- Model2.setprvar method replaces 'pr' with 'pr(t+1)'; cmc is more complicated
    #
    def setprvar(self,dtg=None,tau=None):
        modelprvar=self.modelprvar
        if(tau == 0):
            modelprvar="""_prvar='( const(pr(t+1),0,-u)-const(pr(t-0),0,-u) )*4'"""
        return(modelprvar)

    def setMaxtau(self,dtg):
        hh=dtg[8:10]
        if(hh == '00'):  self.maxtau=240
        elif(hh == '12'):  
            # -- 20140731 -- tau 12 now out to 240
            self.maxtau=240
            #self.maxtau=144
        else:    self.maxtau=-999
        return(self.maxtau)


    def name2tau(self,file,dtg=None):
        tau=file.split('.')[2][1:]
        tau=int(tau)
        return(tau)

    def gname2tau(self,file,dtg,dtg1='2009010100'):
        diff1=mf.dtgdiff(dtg1,dtg)
        if(diff1 > 0.0 ):
            tau=int(file[-3:])
        else:
            tau=file.split('.')[2][1:]
            tau=int(tau)
            tau=int(file[-3:])
        return(tau)

    def setgmask(self,dtg,dtg1='2009010100'):
        diff1=mf.dtgdiff(dtg1,dtg)
        if(diff1 > 0.0 ):
            self.gmask="cmc_%s*"%(dtg)
        else:
            self.gmask="cmc_%s*"%(dtg)

    def setxwgrib(self,dtg):
        self.xwgrib='wgrib'
        self.dmask="%s.%s.f???.%s"%(self.lmodel,dtg,self.gribtype)
        self.dsetmask="%s.%s.f%%f3.%s"%(self.lmodel,dtg,self.gribtype)


    def setctlgridvar(self,dtg,dtg1='2009010100'):

        hh=dtg[8:10]

        latlongrid='''xdef 360 linear   0.0 1.0
ydef 181 linear -90.0 1.0'''

        self.btau=0

        if(self.gribtype == 'grb1'):

            diff1=mf.dtgdiff(dtg1,dtg)

            if(diff1 > 0.0 ):

                if(hh == '00'):
                    self.etau=240
                    self.dtau=6
                elif(hh == '12'):
                    #self.etau=144
                    # -- 20140731 -- now out to 240 at 12Z
                    self.etau=240
                    self.dtau=6

            else:

                if(hh == '00'):
                    self.etau=180
                    self.dtau=6
                elif(hh == '12'):
                    self.etau=144
                    self.dtau=6


            optiondtype='''options template
dtype grib
zdef 7 levels 1000 925 850 700 500 250 200'''

            vars='''
vars 11
vrta   7  41,100,0       ** Absolute vorticity [/s]
pr     0  61,  1,0       ** Total precipitation [kg/m^2]
zg     7   7,100,0       ** Geopotential height [gpm]
psl    0   2,102,0       ** Pressure reduced to MSL [Pa]
hur    7  52,100,0       ** Relative humidity [%]
ta     7  11,100,0       ** Temp. [K]
tas    0  11,119,10000   ** Temp. [K]
ua     7  33,100,0       ** u wind [m/s]
uas    0  33,119,10000   ** u wind [m/s]
va     7  34,100,0       ** v wind [m/s]
vas    0  34,119,10000    ** v wind [m/s]
endvars'''



            self.ctlgridvar='''undef 9.999E+20
title ecmo 1deg deterministic run
*  produced by grib2ctl v0.9.12.5p16
%s
%s
%s'''%(optiondtype,latlongrid,vars)

class Mpas(Model2):

    """ 1deg MPAS global run at esrl on zeus"""

    pltdir='plt_esrl_mpas'
    pmodel='mpas'


    def __init__(self,model='mpas',center='esrl',gribver=1):

        self.model=model
        self.dmodel=model
        self.dirmodel=model
        self.lmodel=model

        self.initModelCenter(center)
        self.initGribVer(gribver)

        self.tautype='wgrib'

        self.nfields=78
        self.nfieldsW2flds=55

        self.modelrestitle='T`bl`nuuuu|Nuu Luu'
        self.modelDdtg=12
        self.modelgridres='1.0'
        self.modelprvar="""_prvar='( const(pr(t+2),0,-u)-const(pr(t-0),0,-u) )*2'"""
        self.modelpslvar='psl*0.01'
        self.modeltitleAck1="CMC Data Courtesy of NCEP/NCO"
        self.modeltitleFullmod="CMC(GEM)"

        self.tbase=self.dmodel

        self.adecksource='esrl'
        self.adeckaid='mpas'

        self.etau=192
        self.dtau=6

        self.rundtginc=12

        self.adecksource='tmtrkN'
        self.adeckaid=self.model
        self.dattaus=range(self.btau,self.etau+1,self.dtau)


    # -- Model2.setprvar method replaces 'pr' with 'pr(t+1)'; cmc is more complicated
    #
    def setprvar(self,dtg=None,tau=None):
        modelprvar=self.modelprvar
        if(tau == 0):
            modelprvar="""_prvar='( const(pr(t+1),0,-u)-const(pr(t-0),0,-u) )*4'"""
        return(modelprvar)

    def setMaxtau(self,dtg):
        hh=dtg[8:10]
        if(hh == '00'):  self.maxtau=192
        elif(hh == '12'):  self.maxtau=192
        else:    self.maxtau=-999
        return(self.maxtau)


    def name2tau(self,file,dtg=None):
        tau=file.split('.')[2][1:]
        tau=int(tau)
        return(tau)

    def gname2tau(self,file,dtg):
        tau=file.split('.')[2][1:]
        tau=int(tau)
        return(tau)

    def setgmask(self,dtg,dtg1='2009010100'):
        self.gmask="mpas.*%s*"%(dtg)

    def setxwgrib(self,dtg):
        self.xwgrib='wgrib'
        self.dmask="*%s.%s.f???.%s"%(self.dmodel,dtg,self.gribtype)
        self.dsetmask="*%s.%s.f%%f3.%s"%(self.dmodel,dtg,self.gribtype)


    def setctlgridvar(self,dtg):

        hh=dtg[8:10]

        latlongrid='''xdef 720 linear -180.0 0.5
ydef 361 linear -90.0 0.5'''

        self.btau=0

        if(self.gribtype == 'grb1'):

            if(hh == '00'):
                self.etau=192
                self.dtau=6
            elif(hh == '12'):
                self.etau=192
                self.dtau=6


            optiondtype='''options template
dtype grib
zdef 7 levels 1000 925 850 700 500 250 200'''

            vars='''
vars 10
prl     0   62,  1,  1  ** Large-scale precipitation [kg/m^2]
prc     0   63,  1,  1  ** Convective precipitation [kg/m^2]
psl     0    2,102,  0  ** Mean sea level pressure (MAPS) [Pa]
uas     0   33,105, 10  ** u wind [m/s]
vas     0   34,105, 10  ** v wind [m/s]
zg      11   7,100,  0  ** Geopotential height [gpm]
ta      11  11,100,  0  ** Temp. [K]
hur     11  52,100,  0  ** Temp. [K]
ua      11  33,100,  0  ** u wind [m/s]
va      11  34,100,  0  ** v wind [m/s]
endvars'''



            self.ctlgridvar='''undef 9.999E+20
title ecmo 1deg deterministic run
*  produced by grib2ctl v0.9.12.5p16
%s
%s
%s'''%(optiondtype,latlongrid,vars)


class Cgd2(Model2):

    """ new hi-res real-time from .ca"""

    pltdir='plt_cmc_cgd2'
    pmodel='cgd2'

    regridTracker=0.25

    def __init__(self,model='cgd2',center='cmc',gribver=2):

        self.model=model
        self.dmodel='cmc'
        self.dirmodel='cmc'
        self.lmodel=model

        self.initModelCenter(center)
        self.initGribVer(gribver)

        self.tautype='wgrib'

        self.nfields=47
        self.nfieldsW2flds=36

        self.modelrestitle='T`bl`nuuuu|Nuu Luu'
        self.modelDdtg=12
        self.modelgridres='0.24'
        self.modelprvar="""_prvar='( const(pr(t+1),0,-u)-const(pr(t-0),0,-u) )*2'"""
        self.modelpslvar='psl*0.01'
        self.modeltitleAck1="CMC Data Courtesy of NCEP/NCO"
        self.modeltitleFullmod="CMC(GEM)"

        self.tbase=self.dmodel

        self.adecksource='ncep'
        self.adeckaid='cmc'

        self.rundtginc=12


    # -- Model2.setprvar method replaces 'pr' with 'pr(t+1)'; cmc is more complicated
    #

    def setprvar(self,dtg=None,tau=None):
        
        modelprvar=self.modelprvar
        if(tau <= 6):
            modelprvar="""_prvar='(( const(pr(t+1),0,-u)-const(pr(t-0),0,-u) )*4)'"""
        elif(tau > 6 and tau <= 144):
            modelprvar="""_prvar='(( const(pr(t-0),0,-u)-const(pr(t-1),0,-u) )*4)'"""
        elif(tau > 144):
            modelprvar="""_prvar='(( const(pr(t-0),0,-u)-const(pr(t-2),0,-u) )*2)'"""
            
        return(modelprvar)

    def setMaxtau(self,dtg):
        hh=dtg[8:10]
        if(hh == '00'):  self.maxtau=240
        elif(hh == '12'):  self.maxtau=144
        else:    self.maxtau=-999
        return(self.maxtau)


    def name2tau(self,file,dtg=None):
        tau=file.split('.')[2][1:]
        tau=int(tau)
        return(tau)

    def gname2tau(self,file,dtg,dtg1='2009010100'):
        diff1=mf.dtgdiff(dtg1,dtg)
        if(diff1 > 0.0 ):
            tau=int(file[-3:])
        else:
            tau=file.split('.')[2][1:]
            tau=int(tau)
            tau=int(file[-3:])
        return(tau)

    def setgmask(self,dtg,dtg1='2009010100'):
        diff1=mf.dtgdiff(dtg1,dtg)
        if(diff1 > 0.0 ):
            self.gmask="cmc_%s*"%(dtg)
        else:
            self.gmask="cmc_%s*"%(dtg)

    def setxwgrib(self,dtg):
        self.xwgrib='wgrib2'
        self.dmask="%s.%s.f???.%s"%(self.lmodel,dtg,self.gribtype)
        self.dsetmask="%s.%s.f%%f3.%s"%(self.lmodel,dtg,self.gribtype)


    def setctlgridvar(self,dtg,dtg1='2009010100'):

        hh=dtg[8:10]

        latlongrid='''xdef 360 linear   0.0 1.0
ydef 181 linear -90.0 1.0'''

        self.btau=0

        if(self.gribtype == 'grb1'):

            diff1=mf.dtgdiff(dtg1,dtg)

            if(diff1 > 0.0 ):

                if(hh == '00'):
                    self.etau=240
                    self.dtau=6
                elif(hh == '12'):
                    self.etau=144
                    self.dtau=6

            else:

                if(hh == '00'):
                    self.etau=180
                    self.dtau=6
                elif(hh == '12'):
                    self.etau=144
                    self.dtau=6


            optiondtype='''options template
dtype grib
zdef 7 levels 1000 925 850 700 500 250 200'''

            vars='''
vars 11
vrta   7  41,100,0       ** Absolute vorticity [/s]
pr     0  61,  1,0       ** Total precipitation [kg/m^2]
zg     7   7,100,0       ** Geopotential height [gpm]
psl    0   2,102,0       ** Pressure reduced to MSL [Pa]
hur    7  52,100,0       ** Relative humidity [%]
ta     7  11,100,0       ** Temp. [K]
tas    0  11,119,10000   ** Temp. [K]
ua     7  33,100,0       ** u wind [m/s]
uas    0  33,119,10000   ** u wind [m/s]
va     7  34,100,0       ** v wind [m/s]
vas    0  34,119,10000    ** v wind [m/s]
endvars'''



            self.ctlgridvar='''undef 9.999E+20
title ecmo 1deg deterministic run
*  produced by grib2ctl v0.9.12.5p16
%s
%s
%s'''%(optiondtype,latlongrid,vars)



class Cgd6(Cgd2,Grib1,Grib2,MFutils):

    """ lower res archive from cmc.ca"""

    pltdir='plt_cmc_cgd6'
    pmodel='cgd6'
    etau=240
    dtau=6


    def __init__(self,model='cgd6',center='cmc',gribver=2):

        self.model=model
        self.dmodel='cgd6'
        self.dirmodel='cgd6'
        self.lmodel=model

        self.initModelCenter(center)
        self.initGribVer(gribver)

        self.tautype='wgrib'

        self.nfields=47
        self.nfieldsW2flds=36

        self.dmodelType='w2flds'

        self.modelrestitle='T`bl`nuuuu|Nuu Luu'
        self.modelDdtg=12
        self.modelgridres='1.0'
        self.modelprvar="""_prvar='( const(pr(t+2),0,-u)-const(pr(t-0),0,-u) )*2'"""
        self.modelpslvar='psl*0.01'

        # -- from 1000 mb z + t
        #
        self.modelpslvar='(100000.0*exp((9.80*zg(lev=1000))/(287.04*ta(lev=1000))))*0.01'
        self.modeltitleAck1="CMC Data Courtesy of CMC"
        self.modeltitleFullmod="CMC(GDPS)"

        self.tbase=self.dmodel

        self.adecksource='tmtrkN'
        self.adeckaid='gcd6'

        self.gribtype='grb2'

        self.rundtginc=12
        
        self.tryarch=1

    # -- new method to get etau dtau w2base.Model2DataTaaus
    #
    def getEtau(self,dtg=None):
        if(dtg == None):
            return(self.etau)
        else:
            hh=dtg[8:10]
            self.etau=240
            # -- not always....
            #if(hh == '12'):  self.etau=144
            return(self.etau)

    def getDtau(self,dtg=None):
        if(dtg == None):
            return(self.dtau)
        else:
            return(self.dtau)

    def setgmask(self,dtg):
        self.gmask="%s.%s.%s.*.%s"%(self.model,self.dmodelType,dtg,self.gribtype)


    def GetTauGrib1File(self,file):
        tau=file.split('.')[-2][-3:]
        tau=int(tau)
        return(tau)


class Rtfim(Model2):

    dtg6hpr='2010010100'

    modelrestitle='T`bl`n|N400 L91'
    modelDdtg=6
    modelgridres='0.5'


    modelpslvar='psl*0.01'
    modeltitleAck1="ECMWF Data Courtesy of NCEP/NCO"
    modeltitleFullmod="ECMWF(IFS)"

    def __init__(self,model='fim8',center='esrl',gribver=1):

        self.model=model
        self.dmodel=model
        self.dirmodel='fim8'

        self.initModelCenter(center)
        self.initGribVer(gribver)

        self.tautype='wgrib'

        self.nfields=43
        self.nfieldsW2flds=29

        self.tbase=self.dmodel

        self.modelrestitle='G8(30km)L64'
        self.modelDdtg=6
        self.modelgridres='0.5'
        self.modelprvar="""_prvar='pr*4'"""
        self.modelpslvar='psl*0.01'

        self.modeltitleAck1="ESRL FIM courtesy ESRL/GSD/AMB"
        self.modeltitleFullmod="ESRL(FIM)"

        # -- confusion with dmodelType? -- main mechanism to set dmask dset
        # -- used in TCdiag
        #
        self.modeltype='rtfim'

        self.adecksource='rtfim'
        self.adeckaid='fim8'

        self.rundtginc=12


    def setMaxtau(self,dtg):
        hh=dtg[8:10]
        if(hh == '00' or hh == '12'):  self.maxtau=168
        else:    self.maxtau=-999
        return(self.maxtau)


    def name2tau(self,file,dtg=None):
        tau=file.split('.')[2][1:]
        tau=int(tau)
        return(tau)

    def gname2tau(self,file,dtg,dtg1='2009010100'):
        diff1=mf.dtgdiff(dtg1,dtg)
        if(diff1 > 0.0 ):
            tau=file.split('.')[2][1:]
            tau=int(tau)
        else:
            tau=int(file[-3:])
        return(tau)

    def setgmask(self,dtg,dtg1='2009010100'):
        diff1=mf.dtgdiff(dtg1,dtg)
        if(diff1 > 0.0 ):
            self.gmask="nogaps_%s*grib2"%(dtg)
        else:
            self.gmask="nogaps_%s*"%(dtg)

    def setxwgrib(self,dtg):
        self.xwgrib='wgrib'
        self.dmask="*%s.%s.f???.%s"%(self.dmodel,dtg,self.gribtype)
        self.dsetmask="*%s.%s.f%%f3.%s"%(self.dmodel,dtg,self.gribtype)


    def setprvar(self,dtg,tau=None):

        dtg6hpr='2010010100'

        # -- assume always 6-h buck for rtfim
        # -- 12-h bucket
        modelprvar12="""_prvar='pr*2' """
        # -- 6-h bucket
        modelprvar06="""_prvar='pr*4' """
        # -- 3-h bucket
        modelprvar03="""_prvar='pr*8' """

        # -- 20130521 -- use 12-h precip since rtfim9 does not yet output dtau=6
        modelprvar=modelprvar06
        modelprvar=modelprvar12
        if(tau == 0):
            #modelprvar=modelprvar.replace('pr','pr(t+1)')
            modelprvar=modelprvar.replace('pr','pr(t+2)')

        return(modelprvar)



    def setctlgridvar(self,dtg):

        if(self.gribtype == 'grb1'):

            optiondtype='''options yrev template
dtype grib '''

            latlongrid='''xdef 720 linear   0.0 0.5
ydef 361 linear -90.0 0.5'''


            vars='''vars 14
pr      0  61,  1,  1  ** Total precipitation [kg/m^2]
prc     0  63,  1,  1  ** Convective precipitation [kg/m^2]
prw     0  54,  1,  1  ** prw [mm]
hfls    0 121,  1,  1  ** latent heat [mm]
hfss    0 122,  1,  1  ** sensible heat [mm]
ustar   0 253,  1,  1  ** sensible heat [mm]
psl     0 129,102,  1  ** Mean sea level pressure (MAPS) [Pa]
uas     0  33,109,  1  ** u wind [m/s]
vas     0  34,109,  1  ** v wind [m/s]
zg      11   7,100,  0  ** Geopotential height [gpm]
ta      11  11,100,  0  ** Temp. [K]
hur     11  52,100,  0  ** Temp. [K]
ua      11  33,100,  0  ** u wind [m/s]
va      11  34,100,  0  ** v wind [m/s]'''



        self.ctlgridvar='''undef 1e+20
title fim8 set in M2
%s
%s
%s
###--- pr is mm/6h *4 = mm/d'''%(optiondtype,latlongrid,vars)


class Rtfim9(Model2):


    model='fim9'
    center='esrl'
    gribver=2

    modelpslvar='psl*0.01'

    modelrestitle='G9(15km)L64'
    modelDdtg=6
    modelgridres='0.5'
    modelres=modelgridres.replace('.','')

    modeltitleAck1="FIM Data Courtesy of ESRL/ITS"
    modeltitleFullmod="FIM9"

    pltdir='plt_esrl_fim9'
    pmodel='fim9'

    modelPlotTaus=[0,6,12,18,24,30,36,42,48,60,72,84,96,108,120,132,144,156,168]
    gmodname="%s%s"%(pmodel,modelres)


    # -- confusion with dmodelType? -- main mechanism to set dmask dset
    # -- used in TCdiag
    #
    dmodelType='rtfim'

    adecksource='rtfim'
    adeckaid='fim9'

    rundtginc=12

    btau=0
    etau=240
    dtau=6

    dattaus=range(btau,etau+1,dtau)

    # -- dtg for change from 12-h to 6-h accum
    #
    dtg6hpr='2013061200'

    def __init__(self):

        self.dmodel=self.model
        self.lmodel=self.model
        self.dirmodel='FIM9'

        self.bddir="%s/rtfim/dat/%s"%(self.bdir2,self.dirmodel)

        self.initGribVer(self.gribver)

        self.tautype='wgrib'

        self.nfields=43
        self.nfieldsW2flds=29

        self.tbase=self.dmodel


    def setDbase(self,dtg,dtype=None):

        print '-------- setDbase',self.model
        self.dbasedir="%s/%s"%(self.bddir,dtg)
        self.dbase="%s/%s/%s.%s.%s"%(self.bddir,dtg,self.lmodel,self.dirmodel,self.gribtype)
        self.dmask="%s.%s.f???.%s"%(self.lmodel,self.dirmodel,self.gribtype)
        self.dpath="%s.ctl"%(self.dbase)
        self.dpathexists=os.path.exists(self.dpath)
        self.tdatbase=self.dbase  
        self.dtype=None  # for rtfim set to None


    def setprvar(self,dtg,tau=None):



        # -- assume always 6-h buck for rtfim
        # -- 12-h bucket
        modelprvar12="""_prvar='pr*2' """        

        # -- 6-h bucket
        modelprvar06="""_prvar='pr*4' """

        # -- 3-h bucket
        modelprvar03="""_prvar='pr*8' """

        # -- 2013061200 now every 6-h
        if(mf.dtgdiff(dtg,self.dtg6hpr) < 0):
            modelprvar=modelprvar06
        else:
            modelprvar=modelprvar12

        if(tau == 0):
            modelprvar=modelprvar.replace('pr','pr(t+1)')

        return(modelprvar)


    def setxwgrib(self,dtg):
        self.xwgrib='wgrib2'
        self.dsetmask="%s.%s.f%%f3.%s"%(self.lmodel,self.dirmodel,self.gribtype)

    def setgmask(self,dtg,dtg1='2009010100'):
        self.gmask=self.dmask

    def name2tau(self,file,dtg):
        try:
            tau=file.split('.')[2][1:]
            tau=int(tau)
        except:
            tau=None
        return(tau)



class Fim8(Model2):

    dtg6hpr='2010010100'

    modelrestitle='T`bl`n|N400 L91'
    modelDdtg=6
    modelgridres='0.5'
    modelres=modelgridres.replace('.','')


    modelpslvar='psl*0.01'
    modeltitleAck1="FIM Data Courtesy of ESRL/ITS"
    modeltitleFullmod="FIM8"

    pltdir='plt_esrl_fim'
    pmodel='fim'

    modelPlotTaus=[0,6,12,18,24,30,36,42,48,60,72,84,96,108,120,132,144,156,168]
    gmodname="%s%s"%(pmodel,modelres)

    modeltitleAck1="ESRL FIM courtesy ESRL/GSD/AMB"
    modeltitleFullmod="FIM8"

    def __init__(self,model='fim8',center='esrl',gribver=1):

        self.model=model
        self.dmodel=model
        self.dirmodel='fim8'

        self.initModelCenter(center)
        self.initGribVer(gribver)

        self.tautype='wgrib'

        self.nfields=730
        self.nfieldsW2flds=64

        self.tbase=self.dmodel

        self.modelrestitle='G8(30km)L64'
        self.modelDdtg=6
        self.modelgridres='0.5'
        self.modelprvar="""_prvar='pr*4'"""
        self.modelpslvar='psl*0.01'

        self.modeltitleAck1="ESRL FIM courtesy ESRL/GSD/AMB"
        self.modeltitleFullmod="ESRL(FIM)"

        self.adecksource='rtfim'
        self.adeckaid='fim8'

        self.btau=0
        self.etau=240
        self.dtau=6

        self.rundtginc=12


    def setprvar(self,dtg,tau=None):

        dtg6hpr='2010010100'
        dtgAccum='2009080600'

        # -- 6-h bucket
        modelprvar06="""_prvar='pr*4' """
        # -- 3-h bucket
        modelprvar03="""_prvar='pr*8' """

        if(tau == 0):
            modelprvar06=modelprvar06.replace('pr','pr(t+1)')
            modelprvar03=modelprvar03.replace('pr','pr(t+1)')


        # -- running accum every 6 h
        modelprvarAccum="""_prvar='((pr(t-0)-pr(t-1))*4)' """
        if(tau == 0):
            modelprvarAccum="""_prvar='((pr(t-1)-pr(t-0))*4)' """

        dd=mf.dtgdiff(dtg6hpr,dtg)
        if(dd > 0.0):
            modelprvar=modelprvar06
        else:
            modelprvar=modelprvar03

        dd=mf.dtgdiff(dtgAccum,dtg)
        if(dd <= 0.0):
            modelprvar=modelprvarAccum

        return(modelprvar)

    def setMaxtau(self,dtg):
        hh=dtg[8:10]
        if(hh == '00' or hh == '12'):  self.maxtau=168
        else:    self.maxtau=-999
        return(self.maxtau)


    def name2tau(self,file,dtg=None):
        tau=file.split('.')[2][1:]
        tau=int(tau)
        return(tau)

    def gname2tau(self,file,dtg,dtg1='2009010100'):
        diff1=mf.dtgdiff(dtg1,dtg)
        if(diff1 > 0.0 ):
            tau=file.split('.')[2][1:]
            tau=int(tau)
        else:
            tau=int(file[-3:])
        return(tau)

    def setgmask(self,dtg,dtg1='2009010100'):
        diff1=mf.dtgdiff(dtg1,dtg)
        if(diff1 > 0.0 ):
            self.gmask="nogaps_%s*grib2"%(dtg)
        else:
            self.gmask="nogaps_%s*"%(dtg)

    def setxwgrib(self,dtg):
        self.xwgrib='wgrib'
        self.dmask="*%s.%s.f???.%s"%(self.dmodel,dtg,self.gribtype)
        self.dsetmask="*%s.%s.f%%f3.%s"%(self.dmodel,dtg,self.gribtype)


    def setctlgridvar(self,dtg):

        if(self.gribtype == 'grb1'):

            optiondtype='''options yrev template
dtype grib '''

            latlongrid='''xdef 720 linear   0.0 0.5
ydef 361 linear -90.0 0.5'''


            vars='''vars 14
pr      0  61,  1,  1  ** Total precipitation [kg/m^2]
prc     0  63,  1,  1  ** Convective precipitation [kg/m^2]
prw     0  54,  1,  1  ** prw [mm]
hfls    0 121,  1,  1  ** latent heat [mm]
hfss    0 122,  1,  1  ** sensible heat [mm]
ustar   0 253,  1,  1  ** sensible heat [mm]
psl     0 129,102,  1  ** Mean sea level pressure (MAPS) [Pa]
uas     0  33,109,  1  ** u wind [m/s]
vas     0  34,109,  1  ** v wind [m/s]
zg      11   7,100,  0  ** Geopotential height [gpm]
ta      11  11,100,  0  ** Temp. [K]
hur     11  52,100,  0  ** Temp. [K]
ua      11  33,100,  0  ** u wind [m/s]
va      11  34,100,  0  ** v wind [m/s]'''



        self.ctlgridvar='''undef 1e+20
title fim8 set in M2
%s
%s
%s
###--- pr is mm/6h *4 = mm/d'''%(optiondtype,latlongrid,vars)


class Fim7(Fim8):

    dtg6hpr='2010010100'

    modelrestitle='T`bl`n|N400 L91'
    modelDdtg=6
    modelgridres='0.5'
    modelres=modelgridres.replace('.','')


    modelpslvar='psl*0.01'
    modeltitleAck1="FIM Data Courtesy of ESRL/ITS"
    modeltitleFullmod="FIM7"

    pltdir='plt_esrl_fim'
    pmodel='fim'

    modelPlotTaus=[0,6,12,18,24,30,36,42,48,60,72,84,96,108,120,132,144,156,168]
    gmodname="%s%s"%(pmodel,modelres)

    modeltitleAck1="ESRL FIM courtesy ESRL/GSD/AMB"
    modeltitleFullmod="FIM7"

    def __init__(self,model='fim7',center='esrl',gribver=1):

        self.model=model
        self.dmodel=model
        self.dirmodel='fim7'

        self.initModelCenter(center)
        self.initGribVer(gribver)

        self.tautype='wgrib'

        self.nfields=730
        self.nfieldsW2flds=64

        self.tbase=self.dmodel

        self.modelrestitle='G7(60km)L64'
        self.modelDdtg=6
        self.modelgridres='0.5'
        self.modelprvar="""_prvar='pr*4'"""
        self.modelpslvar='psl*0.01'

        self.modeltitleAck1="ESRL FIM courtesy ESRL/GSD/AMB"
        self.modeltitleFullmod="ESRL(FIM)"

        self.adecksource='rtfim'
        self.adeckaid='fim7'

        self.btau=0
        self.etau=240
        self.dtau=6

        self.rundtginc=12

class Fim7X(Fim7):

    dtg6hpr='2010010100'

    modelrestitle='T`bl`n|N400 L91'
    modelDdtg=6
    modelgridres='0.5'
    modelres=modelgridres.replace('.','')


    modelpslvar='psl*0.01'
    modeltitleAck1="FIM Data Courtesy of ESRL/ITS"
    modeltitleFullmod="FIM7-X"

    pltdir='plt_esrl_fim'
    pmodel='fim'

    modelPlotTaus=[0,6,12,18,24,30,36,42,48,60,72,84,96,108,120,132,144,156,168]
    gmodname="%s%s"%(pmodel,modelres)

    modeltitleAck1="ESRL FIM courtesy ESRL/GSD/AMB"
    modeltitleFullmod="FIM8"






class Fimx(Model2,FimRun):

    def __init__(self):


        from FM import setFE
        dtg=MF.dtg()
        fmodel='rtfimx'
        FE=setFE(dtg,fmodel)
        self=FimRun(FE)


        self.adecksource='rtfimx'
        self.adeckaid='fimx'

        self.rundtginc=12




class FimModel(Model2):

    rtfimbdir='/lfs2/projects/rtfim'

    def __init__(self):

        self.bddir="%s/FIM"%(self.rtfimbdir)

        self.gnum=8
        self.version='FIM'


        def name2tau(file,dtg=None):
            tau=file.split('_')[2]
            tau=int(tau[2:len(tau)])

        def getNATfiles(dtg):

            try:
                self.natdir=glob.glob("%s/%s/FIMrun/fim_%d_*%s*"%(self.rtfimbdir,self.version,self.gnum,dtg))[0]
            except:
                self.natdir=None

            if(self.natdir != None):
                self.wsfiles=glob.glob("%s/fim_C/*ws*"%(self.natdir))
                try:
                    self.machinefile=glob.glob("%s/fim_C/MACHIN*new"%(self.natdir))[0]
                except:
                    self.machinefile=None

                self.fimtaus=[]
                self.fimages={}

                for path in self.wsfiles:

                    if(not(os.path.exists(path))):
                        continue

                    (dir,file)=os.path.split(path)
                    tau=file.split('_')[2]
                    tau=int(tau[2:len(tau)])
                    self.fimtaus.append(tau)
                    age=w2.PathCreateTimeDtgdiff(dtg,path)
                    self.fimages[tau]=age

                self.fimtaus.sort()

            else:
                return


        self.name2tau=name2tau
        self.getNATfiles=getNATfiles

#uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu
# unbounded methods
#

def setModel2(model,bdir2=None):

    def isGfsr(model):
        rc=0
        if(model == 'gfsr' or
           (model[0:2] == 'gr' and int(model[2:]) >= 0 and int(model[2:]) <= 11)): rc=1

        return(rc)
    
    model=model.lower()
    
    if(model == 'gfs2'):   return(Gfs2(bdir2=bdir2))
    elif(model == 'hwrf'):   return(Hwrf())
    elif(model == 'gfdl'):   return(Hwrf())
    elif(model == 'goes'): return(Goes(bdir2=bdir2))
    elif(model == 'gfsk'): return(GfsK())
    elif(model == 'gfr1'): return(Gfr1())
    elif(model == 'ecm2'): return(Ecm2())
    elif(model == 'ecm4'): return(Ecm4(bdir2=bdir2))
    elif(model == 'ecmt'): return(Ecmt(bdir2=bdir2))
    elif(model == 'ecmh'): return(Ecmh())
    elif(model == 'era5'): return(Era5(bdir2=bdir2))
    elif(model == 'ecm5'): return(Ecm5(bdir2=bdir2))
    
    elif(model == 'jgsm'): return(Jgsm(bdir2=bdir2))
    
    
    elif(model == 'ukm2'): return(uKm2(bdir2=bdir2))
    elif(model == 'ukm3'): return(uKm2()) # before the big change 15 jun 14
    elif(model == 'ngp2'): return(Ngp2())
    elif(model == 'ngpc'): return(Ngpc())
    elif(model == 'navg'): return(Navg(bdir2=bdir2))

    elif(model == 'gfsc'): return(Gfsc())
    # -- hfip 2011 ensemble
    elif(model == 'gfsenkf_t254'):  return(Gfsenkf_t254())
    elif(model == 'fimens_g7'):     return(Gfsenkf_t254())
    elif(model == 'ngpj'): return(Ngpj())
    elif(model == 'ukmc'): return(uKmc())
    elif(model == 'jmac'): return(Jmac())

    elif(model == 'ohc'):  return(Ohc())
    elif(model == 'ocn'):  return(Ocn())
    elif(model == 'ww3'):  return(Ww3())
    elif(model == 'ecmn'): return(Ecmn())
    elif(model == 'cmc'): return(Cmc2())
    elif(model == 'cmc2'): return(Cmc2())
    elif(model == 'fim8' or model == 'fim8h'): return(Fim8())
    elif(model == 'fim7' or model == 'fim7h'  or model == 'fimxh' or model == 'fimx'): return(Fim7())
    elif(model == 'fim7x' or model == 'fim7xh'): return(Fim7X())
    elif(model == 'fimens'): return(Fim8())
    elif(model == 'ecmg'): return(Ecmg())
    elif(model == 'mpas'): return(Mpas())
    elif(model == 'mpsg'): return(Mpas())  # gfs physics version

    elif(isGfsr(model)): return(GfsR(model='gfsr'))

    elif(mf.find(model,'rtfim') and model != 'rtfim9'): return(Rtfim())
    elif(model == 'rtfim9' or model == 'fim9' or model == 'fim9h'): return(Rtfim9())

    elif(model == 'cgd2'): return(Cgd2())
    elif(model == 'cgd6'): return(Cgd6())
    elif(model == 'fv3e'): return(Fv3e())
    elif(model == 'fv3g'): return(Fv3g())
    elif(model == 'fv7e'): return(Fv7e(bdir2=bdir2))
    elif(model == 'fv7g'): return(Fv7g(bdir2=bdir2))
    


    ####lif(model == 'fimx'): return(Fimx())
    else:
        print 'EEE(M2.setModel2) invalid model: ',model,' in setModel2...sayoonara'
        sys.exit()
        return(None)

    return(fmodel)


def setTitleAck(self):

    myname="Dr. Mike Fiorino (michael.fiorino@noaa.gov) TechDevAppUnit NHC, Miami, FL"
    myname="Dr. Mike Fiorino (michael.fiorino@noaa.gov) ESRL/GSD/AMB, Boulder, CO"

    modeltitleAck2="GrADS (http://grads.iges.org/grads) Graphics by "+myname
    modeltitleAck2="Diagnostics/graphics by "+myname
    modeltitleAck2=myname

    if(self.model == 'ifs'):
        tack1="ECMWF Data Courtesy of ERA-40 Project"
        fullmod="ECM(IFS)"

    if(self.model == 'ecm' or self.model == 'ecm2'):
        tack1="ECMWF Data Courtesy of NCEP/NCO"
        fullmod="ECMWF(IFS)"

    if(self.model == 'ecmt' or self.model == 'ecmh'):
        tack1="ECMWF Data Courtesy of TIGGE data server"
        fullmod="ECMWF(IFS)"

    if(self.model == 'gfsk'):
        tack1="ESRL GFS(EnKF) courtesy ESRL/GSD/AMB"
        fullmod="GFSK"

    if(self.model == 'ecmn'):
        tack1="ECMWF Data Courtesy of NWS/AWIPS"
        fullmod="ECMWF(IFS)"

    if(self.model == 'ngp2'):
        tack1="NOGAPS Data Courtesy of NCEP/NCO"
        fullmod="NOGAPS"

    if(self.model == 'cmc' or self.model == 'cmc2'):
        tack1="CMC Data Courtesy of NCEP/NCO"
        fullmod="CMC(CEM)"

    if(self.model == 'ngp' or self.model == 'ngp2' or self.model == 'navg'):
        tack1="NOGAPS Data Courtesy of FNMOC, Monterey, CA"
        fullmod="NOGAPS"

    if(self.model == 'ngp05'):
        tack1="NOGAPS Data Courtesy of FNMOC, Monterey, CA"
        fullmod="NOGAPS05"

    if(self.model == 'era15'):
        tack1="ECMWF ReAnalysis (ERA-15) Courtesy of ECMWF and PCMDI, LLNL"
        fullmod="ECM(ERA15)"

    if(self.model == 'gfs' or self.model == 'gfs2'):
        tack1="NCEP GFS courtesy NCEP/NCO"
        fullmod="NCEP(GFS)"

    if(mf.find(self.model,'fim')):
        tack1="ESRL FIM courtesy ESRL/GSD/AMB"
        fullmod="FIM8"

    if(self.model == 'nr1'):
        tack1="NCEP/NCAR R1 Global Reanalysis Data courtesy NOAA CDC"
        fullmod="NCEP(R1)"

    if(self.model  ==  'ukm' or self.model == 'ukm2'):
        tack1="UKMO 0.8 deg data courtesy of NCEP/NCO"
        fullmod="UKMO"

    if(self.model  ==  'ocn'):
        tack1="0 h FNMOC 0.25 deg files courtesy of FNMOC"
        fullmod="NCODA(ocn)"

    if(self.model  ==  'ohc'):
        tack1="0 h NCODA 0.2 deg files courtesy of FNMOC"
        fullmod="NCODA(ohc)"

    if(self.model  ==  'ww3'):
        tack1="0 h FNMOC 0.25 deg files courtesy of FNMOC"
        fullmod="WW3"

    if(self.model  ==  'gsm'):
        tack1="0-72 hr GSM 1.25 deg files courtesy of JMA (ftp://ddb.kishou.go.jp/pub/DATA/jp034/g02YYMMDDHH)"
        fullmod="JMA(GSM)"



if (__name__ == "__main__"):

    dtg='2020072206'
    verb=1
    m2=setModel2('jgsm')
    m2.setDbase(dtg)
    m2.setGrib(verb=verb)
    #me=setModel2('ecm5')
    #me.ls()
    sys.exit()
