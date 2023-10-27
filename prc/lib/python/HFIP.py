import os,sys,time,copy
import getopt,glob
import cPickle as pickle

import mf
import FM
from FM import FimRun
from M2 import setModel2
from FM import onWjet

class FimRunModel2(FimRun):

    
    def __init__(self,model,dtg,override=0,verb=0):

        self.model=model
        self.dtg=dtg
        self.m2=setModel2(model)

        self.curdtg=mf.dtg()
        self.verb=verb
        self.override=override
      
        self.FE=None

        self.expopt='w2flds'
        self.fimtype=None
        self.comment='FIM g8 (30 km) with GSI'

        self.gribver=self.m2.gribver
        self.sRoot=self.m2.bddir
        self.tRoot=self.m2.bdir2
        self.lRoot=None
        
        self.fimver=None
        self.glvl=None
        self.nlvl=None
        self.npes=None

        self.fimtype=None

        self.initVars()
        self.initGribPrc()
        self.initSourceTarget()
        if(self.initDataThere() == 0):
            print 'NOT initDataThere nnnnnnnnnnnnnnnnnnnnnnn  model: %6s  dtg: %s'%(self.model,self.dtg)
            return
        if(self.initTargetDirs() == 0):
            print 'NOT initTarget    nnnnnnnnnnnnnnnnnnnnnnn  model: %6s  dtg: %s'%(self.model,self.dtg)
            return

        self.tbase="%s.%s.%s"%(self.model,self.expopt,self.dtg)
        self.tdatbase="%s/%s"%(self.tOutDir,self.tbase)
        self.ctlpath="%s.%s.ctl"%(self.tdatbase,self.gribtype)
        self.ctlpathM2="%s.ctl"%(self.tdatbase)
        self.gmppath="%s.%s.gmp"%(self.tdatbase,self.gribtype)
        self.gmpfile="%s.%s.gmp"%(self.tbase,self.gribtype)

        self.initGribs()

        # -- set maxtau
        self.m2.setMaxtau(dtg)
        self.maxtau=self.m2.maxtau
        
        #self.initTrackers()
        #self.initStdOut()
        #self.initPyp()
        

    def initVars(self):


        self.lasttau=168
        self.btau=0
        self.etau=self.lasttau
        self.dtau=6

        self.reqtaus=range(self.btau,self.etau+1,self.dtau)
        self.iokreqtaus={}
        for tau in self.reqtaus:
            self.iokreqtaus[tau]=0

        self.jday=mf.Dtg2JulianDay(self.dtg)


    def initSourceTarget(self):
        
        # set up source
        #
        if(self.sRoot != None):
            
            self.sDir="%s"%(self.sRoot)
            self.sGribDir="%s/%s"%(self.sDir,self.dtg)
            self.sTrackerDir=None
            self.sOutDir=None
            
            self.sAdeckPath=None
            self.sTrackerGribPath=None
            hh=self.dtg[8:10]

            self.gmask="%s/%s.%s.f???.%s"%(self.sGribDir,self.model,self.dtg,self.m2.gribtype)

            # for consistency with rtfim runs set tDirNotag and tDir to tDirNotag -> tOutDir
            #
            self.tDirNotag="%s/%s/dat/%s/%s"%(self.tRoot,self.expopt,self.model,self.dtg)
            self.tDir=self.tDirNotag


    def initDataThere(self):

        #eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
        # check if source and targt dir...
        #
        self.sdatathere=self.tdatathere=self.datathere=1
        if(not(mf.ChkDir(self.sDir,diropt='quiet'))): self.sdatathere=0
        if(not(mf.ChkDir(self.tDir,diropt='quiet'))): self.tdatathere=0

        # bail if source processing not there...for w2flds...
        #
        sdirchk="%s/%s"%(self.sDir,self.dtg)
        self.sdatathere=mf.ChkDir(sdirchk,diropt='quiet')
        
        if( not(self.sdatathere) and not(self.tdatathere) ):
            return(0)

        # now check if any data there
        if(len(glob.glob(self.gmask)) == 0): self.sdatathere=0


        # check if both s and t data dirs there ... always do gribver=1 if on wjet, so by the time
        # we want to do the grib, the t dir should be there...
        #
        if( self.sdatathere == 0 and self.tdatathere == 0 ):
            self.datathere=0
            if(onWjet):
                if(self.verb): print 'EEE source dir: ',self.sDir,' and tdir: ',self.tDir,' not there, sayoonara'
                return(0)


    def GetTauGrib1File(self,file):
        tau=file.split('.')[-2][1:]
        tau=int(tau)
        return(tau)


    def initGribs(self):

        self.grbtaus=None

        #gggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggg
        # grib files
        #
        if(self.sRoot != None):
            gpaths=glob.glob(self.gmask)

            taus=[]
            for gpath in gpaths:

                (dir,file)=os.path.split(gpath)
                tau=self.GetTauGrib1File(file)
                taus.append(tau)

                tpath="%s/%s.%s.f%03d.%s"%(self.tOutDir,self.model,self.dtg,tau,self.gribtype)
                if(not( os.path.exists(tpath) or os.path.islink(tpath) ) or self.override > 1 and self.override != 3):
                    cmd="ln -f -s %s %s"%(gpath,tpath)
                    mf.runcmd(cmd)

                if(tau in self.reqtaus):
                    self.iokreqtaus[tau]=1


            taus=mf.uniq(taus)
            taus.sort()

            self.gribtaus=taus




class FimRunTaccGrids(FimRun):

        
    def __init__(self,FE,gribver=2,override=0,verb=0):

        if(FE == None):
            print 'must initialize with a FimExp objec...'
            sys.exit()

        self.curdtg=mf.dtg()
        self.verb=verb
        self.override=override
        self.gribver=gribver
        
        self.initVars(FE)
        self.initGribPrc()

        self.initSourceTarget()
        if(self.initDataThere() == 0): return
        if(self.initTargetDirs() == 0): return

        self.initGribs()
        #self.initTrackers()
        #self.initStdOut()
        self.initPyp()


    def initSourceTarget(self):
        
        # set up source
        #
        if(self.sRoot != None):
            
            self.sDir="%s"%(self.sRoot)
            self.sGribDir="%s"%(self.sDir)
            self.sTrackerDir=None
            self.sOutDir=None
            
            self.sAdeckPath=None
            self.sTrackerGribPath=None
            hh=self.dtg[8:10]
            
            self.gmask="%s/%s%s/%s%s%s??????"%(self.sGribDir,self.yy,self.jday,self.yy,self.jday,hh)
            
            self.tDir="%s/dat/%s/%s"%(self.tRoot,self.expopt,self.dtg)
            self.tDirNotag=None


def setFEtacc(dtg,
              model
              ):


    sbase='/lfs2/projects/rtfim/TACC_grids'
    troot=FM.trootWjet

    if(model == 'fim9'):
        expopt='FIM9'
        taccmodel='FIM'
        sroot="%s/%s"%(sbase,taccmodel)
        comment='FIM g9 (15km) with GSI'
        
    elif(model == 'f8em'):
        expopt='F8EM'
        taccmodel='FIM_ens'
        sroot="%s/%s"%(sbase,taccmodel)
        comment='FIM g8 (30km) with t382 gfs EnKF mean'
        
    elif(model == 'f9em'):
        expopt='F9EM'
        taccmodel='FIM_EM'
        sroot="%s/%s"%(sbase,taccmodel)
        comment='FIM g9 (15km) with t382 gfs EnKF mean'
        
    elif(model == 'f0em'):
        expopt='F0EM'
        taccmodel='FIM_10km'
        sroot="%s/%s"%(sbase,taccmodel)
        comment='FIM g9.5 (10km) with t382 gfs EnKF mean'
        

    fe=FM.FimExp(
        sroot=sroot,
        troot=troot,
        model=model,
        fmodel=model,
        expopt=expopt,
        fimver=None,
        fimtype=None,
        dtg=dtg,
        comment=comment,
    )

    return(fe)
