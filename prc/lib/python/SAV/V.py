import os,sys,glob
import mf

import w2
import FM
import M2
from CM import ClimoFld
import GA



class DataSet():

    import cPickle as pickle

    def __init__(self,bdir='/tmp',name='test',version='0.1',type='hash'):

        self.bdir=bdir
        self.name=name
        self.curdtg=mf.dtg('dtg.phm')
        self.version=version
        self.pyppath="%s/%s.pyp"%(bdir,name)
    
    def GetPyp(self):

        if(os.path.exists(self.pyppath)):
            PS=open(self.pyppath)
            FR=pickle.load(PS)
            PS.close()
            return(FR)

        else:
            return(None)
          
        
    def PutPyp(self):

        try:
            PS=open(self.pyppath,'w')
            pickle.dump(self,PS)
            PS.close()
        except:
            print 'EEEEE unable to pickle.dump: ',self.pyppath
            sys.exit()
          

            
class DataSets(DataSet):


    def __init__(self,bdir,name,version='0.1',type='hash'):

        self.bdir=bdir
        self.name=name
        self.curdtg=mf.dtg('dtg.phm')
        self.version=version
        self.datasets={}

    def putDataSet(self,dataset):

        self.datasets.append(dataset)

        


        
    
    

class WmoStats():

    wmoversion='0.1 -- comp to ncep vsdb'

    def __init__(self,area,vdtg,var,lev,tau):

        self.ggdx=wmo.ggdx
        self.ggmethod=wmo.method
        self.ggshfilt=wmo.ggshfilt
        self.ggshfiltNwaves=wmo.ggshfiltNwaves

        self.curdtg=mf.dtg('dtg.phm')
        self.wmoversion=self.wmoversion

        self.modelAn=None
        self.modelFc=None

        self.area=area
        self.vdtg=vdtg
        self.var=var
        self.lev=lev
        self.tau=tau

        self.rmse=None
        self.meane=None
        
        self.acAnFc=None
        self.acAnFcwmo=None

        self.corrAnFc=None

        self.meanAn=None
        self.meanFc=None
        self.meanCl=None
        
        self.sigmaAn=None
        self.sigmaFc=None
        self.sigmaCl=None

        self.sigmaAnAnom=None
        self.sigmaFcAnom=None



    def makeStats(self,ga,wmo):
        """
         strictly by the wmo red book, ii.7-36 - ii.7-38
        """
        from math import sqrt
        
        wmo.getAreaLatLon(self.area)

        scg=ga.get.asumg('coslat',wmo)
        s1d=ga.get.asumg('vd*coslat',wmo)
        s2d=ga.get.asumg('vd*vd*coslat',wmo)

        s1aa=ga.get.asumg('vaa*coslat',wmo)
        s2aa=ga.get.asumg('vaa*vaa*coslat',wmo)

        s1af=ga.get.asumg('vfa*coslat',wmo)
        s2af=ga.get.asumg('vfa*vfa*coslat',wmo)

        s1a=ga.get.asumg('va*coslat',wmo)
        s2a=ga.get.asumg('va*va*coslat',wmo)

        s1f=ga.get.asumg('vf*coslat',wmo)
        s2f=ga.get.asumg('vf*vf*coslat',wmo)

        s1c=ga.get.asumg('vc*coslat',wmo)
        s2c=ga.get.asumg('vc*vc*coslat',wmo)

        maf=s1af/scg
        maa=s1aa/scg

        mf=s1f/scg
        ma=s1a/scg
        mc=s1c/scg

        try:
            sigf=sqrt(s2f/scg - mf*mf)
        except:
            sigf=None

        try:
            siga=sqrt(s2a/scg - ma*ma)
        except:
            siga=None

        try:
            sigc=sqrt(s2c/scg - mc*mc)
        except:
            sigc=None

        try:
            sigaf=sqrt(s2af/scg - maf*maf)
        except:
            sigaf=None

        try:
            sigaa=sqrt(s2aa/scg - maa*maa)
        except:
            sigaa=None

        s12ac=ga.get.asumg("(vfa-%g)*(vaa-%g)*coslat"%(maf,maa),wmo)
        s1ac=sqrt(ga.get.asumg("(vfa-%g)*(vfa-%g)*coslat"%(maf,maf),wmo))
        s2ac=sqrt(ga.get.asumg("(vaa-%g)*(vaa-%g)*coslat"%(maa,maa),wmo))

        self.corrAnFc=ga.get.scorr('va-%g'%(ma),'vf-%g'%(mf),wmo)
        self.acAnFcwmo=s12ac/(s1ac*s2ac)
        self.rmse=sqrt(s2d/scg)
        self.meane=s1d/scg
        self.acAnFc=ga.get.scorr('vaa','vfa',wmo)

        self.meanAn=ma
        self.meanFc=mf
        self.meanCl=mc

        self.sigmaAn=siga
        self.sigmaFc=sigf
        self.sigmaCl=sigc

        self.sigmaAnAnom=sigaa
        self.sigmaFcAnom=sigaf

        self.modelAn=ga.modelAn.model
        self.modelFc=ga.modelFc.model

    def ls(self):

        kk=self.__dict__.keys()
        kk.sort()

        for k in kk:
            print "%-20s: "%(k[0:20]),self.__dict__[k]

    

class WmoAreaGrid():

    ggdx=2.5
    ggdy=2.5

    globalgrid='pole'
    method='ba'
    
    globalgrid='nopole'
    method='bl'
    
    xlinear=1
    ylinear=1

    # global grid (gg) properties
    
    ggdlat=180.0
    ggdlon=360.0
    
    gglat1=-90.0
    gglat2=gglat1+ggdlat
    gglon1=0.0
    gglon2=gglon1+ggdlon

    areas={
        'nhem':[20,90,0,360],
        'shem':[-90,-20,0,360],
        'tropics':[-20,20,0,360],
        }

    ggshfilt=0
    ggshfiltNwaves=20
    
    def __init__(self,globalgrid=globalgrid,method=method):


        if(self.globalgrid == 'nopole'):
            self.ni=int(self.ggdlon/self.ggdx + 0.5)
            self.nj=int(self.ggdlat/self.ggdy + 0.5)
            self.gglat11=self.gglat1+self.ggdy*0.5
            self.gglon11=self.gglon1+self.ggdx*0.5
        else:
            self.ni=int(self.ggdlon/self.ggdx + 0.5)
            self.nj=int(self.ggdlat/self.ggdy + 0.5)+1
            self.gglat11=self.gglat1
            self.gglon11=self.gglon1

        rexopt='linear'
        reyopt='linear'

        self.method=method
        self.reargs="%d,%s,%f,%f,%d,%s,%f,%f,%s"%(self.ni,rexopt,self.gglon11,self.ggdx,self.nj,reyopt,self.gglat11,self.ggdy,self.method)

    def getAreaLatLon(self,area='nhem'):
            
        self.lat1=self.areas[area][0]
        self.lat2=self.areas[area][1]
        self.lon1=self.areas[area][2]
        self.lon2=self.areas[area][3]


def openVeriFiles(ga,modelAn,modelFc,gribver=2,dtg='2009112412'):

    if(mf.find(modelAn,'rtfim') and mf.find(modelFc,'rtfim')):

        FE=FM.setFE(dtg,modelAn)
        FEl=FM.setFE(dtg,modelAn,troot=FE.lroot)
        FRAn=FM.FimRun(FEl,gribver=gribver)
        FRAn.EnsFcCtl(chkonly=1)

        FE=FM.setFE(dtg,modelFc)
        FEl=FM.setFE(dtg,modelFc,troot=FE.lroot)
        FRFc=FM.FimRun(FEl,gribver=gribver)
        FRFc.EnsFcCtl(chkonly=1)
        
        ctlAn=FRAn.ensFcCtlpath
        ctlFc=FRFc.ensFcCtlpath
        
    else:
        
        mFc=M2.Model2(modelFc)
        mAn=M2.Model2(modelAn)
        mAn.dtg=dtg
        mFc.dtg=dtg
    
        mAn.tOutDir="/w21/dat/nwp2/w2flds/dat/%s/%s"%(modelAn,mAn.dtg)
        mAn.tbase="%s.w2flds"%(modelAn)
        mAn.tdatbase="%s/%s.%s"%(mAn.tOutDir,mAn.tbase,mAn.dtg)
        mAn.gribver=int(mAn.gribtype[-1])
        mAn.ctlpath="%s.ctl"%(mAn.tdatbase)
        mAn.EnsFcCtl(chkonly=1)
        ga.modelAn=mAn

        mFc.tOutDir="/w21/dat/nwp2/w2flds/dat/%s/%s"%(modelFc,mFc.dtg)
        mFc.tbase="%s.w2flds"%(modelFc)
        mFc.tdatbase="%s/%s.%s"%(mFc.tOutDir,mFc.tbase,mFc.dtg)
        mFc.gribver=int(mFc.gribtype[-1])
        mFc.ctlpath="%s.ctl"%(mFc.tdatbase)
        mFc.EnsFcCtl(chkonly=1)

        ctlAn=mAn.ensFcCtlpath
        ctlFc=mAn.ensFcCtlpath
        ga.modelFc=mFc

    
    C=ClimoFld()
    ctlCl=C.ctlpath
    byearc=C.byear
    ga.Climo=C

    print 'ctlAn: ',ctlAn
    print 'ctlFc: ',ctlFc
    print 'ctlCl: ',ctlCl

    ga.fhAn=ga.open(ctlAn)
    ga.fhFc=ga.open(ctlFc)
    ga.fhc=ga.open(ctlCl)

    ga.nfAn=ga.fhAn.fid
    ga.nfFc=ga.fhFc.fid
    ga.nfc=ga.fhc.fid

    return


def makeIvar(ivar,tau,fh=1):
    expr="%s.%d(ens=f%03d)"%(ivar,fh,tau)
    return(expr)
    
def makeCoslatWght(ga,ovar,wmo):
    from math import pi
    dyh=wmo.ggdx*0.5
    fh=ga.nfAn
    ggdlat=wmo.ggdlat
    expr="(cos(lat.%d(t=1)*%g/%f))"%(fh,pi,ggdlat)
    ga.dvar.regrid(ovar,expr,wmo.reargs)
    return(1)
    
def makedSinlatWght(ga,wmo):
    from math import pi
    dyh=wmo.ggdx*0.5
    ggdlat=wmo.gglat
    fh=ga.nfAn
    exprhi="(sin((lat.%d(t=1)+%g)*%g/%f))"%(fh,dyh,pi,ggdlat)
    exprlo="(sin((lat.%d(t=1)-%g)*%g/%f))"%(fh,dyh,pi,ggdlat)
    ga.dvar.regrid('sinhi',exprhi,wmo.reargs)
    ga.dvar.regrid('sinlo',exprlo,wmo.reargs)
    ga.dvar.var('dsinlat','abs(sinhi-sinlo)*%g'%(wmo.ggdy))
    return(1)
    
def makeAnfld(ga,ovar,ivar,tau,wmo,doshfilt=0):
    
    ga.dvar.regrid(ovar,makeIvar(ivar,tau,ga.nfAn),wmo.reargs)
    if(ga.get.stat(ovar).nvalid == 0):
        print 'EEE no fields found...'
        return(0)
    else:
        if(doshfilt):
            ga.set.latlon(wmo.gglat1,wmo.gglat2,wmo.gglon1,wmo.gglon2)
            ga.dvar.shfilt(ovar,makeIvar(ivar,tau,1))
            ga.dvar.regrid(ovar,ovar,wmo.reargs)
        return(1)
    
def makeFcfld(ga,ovar,ivar,tau,wmo,doshfilt=0):
    
    ga.dvar.regrid(ovar,makeIvar(ivar,tau,ga.nfFc),wmo.reargs)
    if(ga.get.stat(ovar).nvalid == 0):
        print 'EEE no fields found...'
        return(0)
    else:
        if(doshfilt):
            ga.set.latlon(wmo.gglat1,wmo.gglat2,wmo.gglon1,wmo.gglon2)
            ga.dvar.shfilt(ovar,makeIvar(ivar,tau,1))
            ga.dvar.regrid(ovar,ovar,wmo.reargs)
        return(1)
    
    
def makeCl(ga,ovar,ivar,wmo):
    byear=ga.Climo.byear
    cvdtg="%s%s"%(str(byear),ga.vdtg[4:])
    gtime=mf.dtg2gtime(cvdtg)

    expr="%s.%d(time=%s)"%(ivar,ga.nfc,gtime)
    ga.dvar.regrid(ovar,expr,wmo.reargs)
    if(ga.get.stat(ovar).nvalid == 0):
        print 'EEE no verifiying analysis...'
        return(0)
    else:
        print 'found fc for file #3'
        return(1)
    
def makeFields(ga,wmo,vdtg,var,lev,tau):

    ga.vdtg=vdtg
    ga.set.dtg(vdtg)
    ga.set.lev(lev)

    ga.set.latlon(wmo.gglat1,wmo.gglat2,wmo.gglon1,wmo.gglon2)

    rcc=makeCl(ga,'vc',var,wmo)
    rca=makeAnfld(ga,'va',var,0,wmo)
    rcf=makeFcfld(ga,'vf',var,tau,wmo)

    if(rcc and rca and rcf):
        ga.dvar.var('vaa','va-vc')
        ga.dvar.var('vfa','vf-vc')
        ga.dvar.var('vd','va-vf')
        return(1)
    else:
        return(0)

    
