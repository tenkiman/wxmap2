# w2local imports:
#    1)  w2base.py
#     a) w2switches.py
#     b) w2locavars.py
#        0) w2globalvars.py
#        1) M.py MF=MFutils()
#     c) w2env W2einv
#     d) w2nwp2 W2Nwp2

from w2local import *


#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# classes -- non W2

class W2areas(MFbase):


    mapres='mres'
    pareaxl=0.4
    pareaxr=10.8
    pareayb=0.65
    pareayt=8.25
    lonW=-120.0
    lonE=0.0
    latS=-10.0
    latN=60.0
    mpval1='default'
    mpval2='default'
    mpval3='default'
    mpval4='default'
    xlint=20
    ylint=10
    xsize=W2plotXsize
    ysize=int(xsize*W2plotAspect)
    dx=1.0
    dy=1.0

    def __init__(self,
                 lonW=None,
                 lonE=None,
                 latS=None,
                 latN=None,
                 dx=None,
                 dy=None):

        if(lonW != None and lonE != None):
            self.setLons(lonW,lonE)

        if(latS != None and latN != None):
            self.setLats(latS,latN)

        self.dx=dx
        self.dy=dy
        
        if( (type(self.dx) is FloatType) and (type(self.dy) is FloatType) ):
            self.setGrid(self.dx,self.dy)

        
        

    def setLons(self,lonW,lonE):
        
        self.lonW=lonW
        self.lonE=lonE
        if(lonW < 0.0): self.lonW=lonW+360.0
        if(lonE < 0.0): self.lonE=lonE+360.0
        if(self.lonW > self.lonE): self.lonE=self.lonE+360.0

        self.dLon=self.lonE-self.lonW
        
    def setLats(self,latS,latN):
        
        self.latS=latS
        self.latN=latN
        self.dLat=self.latN-self.latS
        

    def setGrid(self,dx,dy):


        # -- E-W wrap check
        #
        wrapEW=0
        dxoffset=1.01
        if(self.lonE - self.lonW == 360.0):
            wrapEW=1
            dxoffset=0.01
        ni=(self.lonE - self.lonW)/dx + dxoffset

        dyoffset=1.01
        nj=(self.latN - self.latS)/dy + dyoffset

        self.wrapEW=wrapEW
        self.dx=dx
        self.dy=dy
        
        self.ni=int(ni)
        self.nj=int(nj)
        



class W2areaGlobal(W2areas):


    def __init__(self,
                 lonW=0.0,
                 lonE=360.0,
                 latS=-90.0,
                 latN=90.0,
                 dx=1.0,
                 dy=1.0,
                 ):

        self.setLons(lonW,lonE)
        self.setLats(latS,latN)

        self.setGrid(dx,dy)



class W2areaLant(W2areas):


    def __init__(self,
                 lonW=-120,
                 lonE=0.0,
                 latS=-10.0,
                 latN=60.0,
                 ):

        self.setLons(lonW,lonE)
        self.setLats(latS,latN)

        
class W2areaEpac(W2areas):


    def __init__(self,
                 lonW=160.0,
                 lonE=280.0,
                 latS=-10.0,
                 latN=60.0,
                 ):

        self.setLons(lonW,lonE)
        self.setLats(latS,latN)


class W2areaCpac(W2areas):


    def __init__(self,
                 lonW=120.0,
                 lonE=240.0,
                 latS=-10.0,
                 latN=60.0,
                 ):

        self.setLons(lonW,lonE)
        self.setLats(latS,latN)



class W2areaWpac(W2areas):


    def __init__(self,
                 lonW=80,
                 lonE=200.0,
                 latS=-10.0,
                 latN=60.0,
                 ):

        self.lonW=lonW
        self.lonE=lonE
        self.latS=latS
        self.latN=latN

        self.setLons(lonW,lonE)
        self.setLats(latS,latN)


class W2areaSio(W2areas):


    def __init__(self,
                 lonW=10.0,
                 lonE=130.0,
                 latS=-60.0,
                 latN=10.0,
                 ):

        self.setLons(lonW,lonE)
        self.setLats(latS,latN)

        
class W2areaNio(W2areas):


    def __init__(self,
                 lonW=20.0,
                 lonE=120.0,
                 latS=-10.0,
                 latN=50.0,
                 ):

        self.setLons(lonW,lonE)
        self.setLats(latS,latN)

        
class W2areaIo(W2areas):


    def __init__(self,
                 lonW=20.0,
                 lonE=160.0,
                 latS=-50.0,
                 latN=40.0,
                 ):

        self.setLons(lonW,lonE)
        self.setLats(latS,latN)

        
class W2areaSwpac(W2areas):

    def __init__(self,
                 lonW=120.0,
                 lonE=280.0,
                 latS=-60.0,
                 latN=20.0,
                 ):

        self.setLons(lonW,lonE)
        self.setLats(latS,latN)

        self.latS=latS
        self.latN=latN

class W2areaShem(W2areas):

    def __init__(self,
                 lonW=30.0,
                 lonE=210.0,
                 latS=-60.0,
                 latN=10.0,
                 ):

        self.setLons(lonW,lonE)
        self.setLats(latS,latN)

        
class W2areaPrwLant(W2areas):

    def __init__(self,
                 lonW=-100.0,
                 lonE=-10.0,
                 latS=-10.0,
                 latN=40.0,
                 ):

        self.setLons(lonW,lonE)
        self.setLats(latS,latN)

        
class W2areaPrwWpac(W2areas):

    def __init__(self,
                 lonW=100.0,
                 lonE=200.0,
                 latS=-10.0,
                 latN=45.0,
                 ):

        self.setLons(lonW,lonE)
        self.setLats(latS,latN)

        
class W2areaPrwEpac(W2areas):

    def __init__(self,
                 lonW=-160.0,
                 lonE=-70.0,
                 latS=-10.0,
                 latN=40.0,
                 ):

        self.setLons(lonW,lonE)
        self.setLats(latS,latN)

class W2areaPrwEnso(W2areas):

    def __init__(self,
                 lonW=-240.0,
                 lonE=0.0,
                 latS=-20.0,
                 latN=70.0,
                 ):

        self.setLons(lonW,lonE)
        self.setLats(latS,latN)

class W2areaPrwCEpac(W2areas):

    def __init__(self,
                 lonW=-190.0,
                 lonE=-70.0,
                 latS=-10.0,
                 latN=40.0,
                 ):

        self.setLons(lonW,lonE)
        self.setLats(latS,latN)

class W2areaPrwCpac(W2areas):

    def __init__(self,
                 lonW=160.0,
                 lonE=250.0,
                 latS=-10.0,
                 latN=45.0,
                 ):

        self.setLons(lonW,lonE)
        self.setLats(latS,latN)

          

class W2areaPrwIo(W2areas):

    def __init__(self,
                 lonW=20.0,
                 lonE=140.0,
                 latS=-40.0,
                 latN=30.0,
                 ):

        self.setLons(lonW,lonE)
        self.setLats(latS,latN)
        


class W2areaPrwSpac(W2areas):

    def __init__(self,
                 lonW=100.0,
                 lonE=210.0,
                 latS=-50.0,
                 latN=10.0,
                 ):

        self.setLons(lonW,lonE)
        self.setLats(latS,latN)
        

class W2areaPrwOrtho(W2areas):

    def __init__(self,
                 lonW=0.0,
                 lonE=180.0,
                 latS=-60.0,
                 latN=60.0,
                 ):

        self.setLons(lonW,lonE)
        self.setLats(latS,latN)
            
        
    
class MfTrkAreaNhem(W2areas):


    def __init__(self,
                 lonW=0.0,
                 lonE=360.0,
                 latS=-10.0,
                 latN=70.0,
                 dx=0.5,
                 dy=0.5,
                 ):

        self.setLons(lonW,lonE)
        self.setLats(latS,latN)
        self.setGrid(dx,dy)


class MfTrkAreaShem(W2areas):


    def __init__(self,
                 lonW=0.0,
                 lonE=360.0,
                 latS=-60.0,
                 latN=0.0,
                 dx=0.5,
                 dy=0.5,
                 ):

        self.setLons(lonW,lonE)
        self.setLats(latS,latN)
        self.setGrid(dx,dy)


class MfTrkAreaGlobal(W2areas):


    def __init__(self,
                 lonW=0.0,
                 lonE=360.0,
                 latS=-60.0,
                 latN=70.0,
                 dx=0.5,
                 dy=0.5,
                 ):

        self.setLons(lonW,lonE)
        self.setLats(latS,latN)
        self.setGrid(dx,dy)


class TmTrkAreaNhem(W2areas):


    def __init__(self,
                 lonW=20.0,
                 lonE=360.0,
                 latS=-10.0,
                 latN=70.0,
                 dx=0.5,
                 dy=0.5,
                 ):

        self.setLons(lonW,lonE)
        self.setLats(latS,latN)
        self.setGrid(dx,dy)

class TmTrkAreaRap(W2areas):


    def __init__(self,
                 lonW=-140.0,
                 lonE=-55.0,
                 latS=15.0,
                 latN=60.0,
                 dx=0.25,
                 dy=0.25,
                 ):

        self.setLons(lonW,lonE)
        self.setLats(latS,latN)
        self.setGrid(dx,dy)


class TmTrkAreaShem(W2areas):

    def __init__(self,
                 lonW=20.0,
                 lonE=260.0,
                 latS=-60.0,
                 latN=10.0,
                 dx=0.5,
                 dy=0.5,
                 ):

        self.setLons(lonW,lonE)
        self.setLats(latS,latN)
        self.setGrid(dx,dy)


class TmTrkAreaGlobal(W2areas):


    def __init__(self,
                 lonW=20.0,
                 lonE=360.0,
                 latS=-60.0,
                 latN=70.0,
                 dx=0.5,
                 dy=0.5,
                 ):

        self.setLons(lonW,lonE)
        self.setLats(latS,latN)
        self.setGrid(dx,dy)


class TmTrkAreaTropics(W2areas):


    def __init__(self,
                 lonW=20.0,
                 lonE=360.0,
                 latS=-40.0,
                 latN=40.0,
                 dx=1.0,
                 dy=1.0,
                 ):

        self.setLons(lonW,lonE)
        self.setLats(latS,latN)
        self.setGrid(dx,dy)

        self.searchLatS=-30.0
        self.searchLatN=30.0
        self.searchModtyp='global'
        self.searchGridtype='global'
        


class ctlProps(MFbase):


    def __init__(self,ctlpath,verb=0):

        siz=MF.GetPathSiz(ctlpath)
        if(siz == None or siz == 0):
            print 'EEE WxMAP2.ctlProps: ctlpath: ',ctlpath,' siz: ',siz
            return

        self.path=ctlpath
        
        cards=open(ctlpath).readlines()

        
        for n in range(0,len(cards)):
            
            card=cards[n].lower()
            
            if(verb): print 'cccCtlCard ',card[:-1]

            if(mf.find(card,'xdef')):
                tt=card.split()
                self.nx=tt[1]
                self.xtype=tt[2]
                self.blon=float(tt[3])
                self.dlon=float(tt[4])
            
            if(mf.find(card,'ydef')):
                tt=card.split()
                self.ny=tt[1]
                self.ytype=tt[2]
                if(self.ytype == 'linear'):
                    self.blat=float(tt[3])
                    self.dlat=float(tt[4])
                else:
                    self.lats=[]
                    n1=3
                    for nn in range(n+1,len(cards)):
                        card1=cards[nn].lower()
                        #print 'nnnnn ',nn,n1,card1[0:-1]
                        if(mf.find(card1,'def')):
                            break
                        elif(n1 == 0):
                            tt=card1.split()
                            for i in range(n1,len(tt)):
                                self.lats.append(float(tt[i]))
                            n=n+1
                            n1=0
                        elif(n1 == len(tt)):
                            n1=0
                            n=n+1
                            continue
                        else:
                            for i in range(n1,len(tt)):
                                self.lats.append(float(tt[i]))
                            n=n+1
                            n1=0
                                
                    self.blat=self.lats[0]
                    self.dlat=self.lats[-1]-self.lats[-2]
                    continue
            
            if(mf.find(card,'zdef')):
                self.levs=[]
                tt=card.split()
                self.nz=tt[1]
                self.ztype=tt[2]
                if(self.ztype == 'linear'):
                    self.blev=float(tt[3])
                    self.dlev=float(tt[4])

                else:
                    # -- assume all levels on one card
                    for i in range(3,len(tt)):
                        self.levs.append(float(tt[i]))

            
        

class f77GridOutput(W2):

    remethod='ba'
    remethod='bl'
    remethod='' # use re default for change in res  'ba' for fine->coarse and 'bl' for coarse->fine
    
    rexopt='linear'
    reyopt='linear'

    outDatType='f77'
    pcntundefMax=10.0
    diag=0  # -- diagnostic prints
    
    def __init__(self,model,dtg,
                 area=None,
                 taus=None,
                 vars=None,
                 doregrid=1,
                 tdir='mftrk',
                 doLogger=0,
                 tauoffset=0,
                 Quiet=1,
                 doByTau=1,
                 pcntundefMax=pcntundefMax,
                 prcdir='/tmp',
                 filename='Zy0x1W2',
                 ):

        self.model=model
        self.dtg=dtg
        self.area=area
        self.taus=taus
        self.tauoffset=tauoffset
        self.vars=vars
        self.doregrid=doregrid
        self.GAdoLogger=doLogger
        self.GAQuiet=Quiet
        self.doByTau=doByTau
        self.pcntundefMax=pcntundefMax
        self.prcdir=prcdir
        
        self.initVars()
        self.setCtl(tdir=tdir)
        self.setOutput(filename=filename)


    def initVars(self,undef=1e20):
        
        if(self.area == None): self.area=W2areaGlobal()

        if(self.vars == None): self.vars=['uas.uas.0.-999.-999.uas [m/s]',
                                          'vas.vas.0.-999.-999.vas [m/s]',
                                          'vrt8.(hcurl(ua,va)*1e5).850.-999.-999.rel vort 850 [*1e5 /s]',
                                          ]

        self.dpaths={}

        self.undef=undef
        
        if(self.taus == None):
            self.btau=0
            self.etau=120
            self.dtau=6
            self.tunits='hr'
            self.taus=range(self.btau,self.etau+1,self.dtau)

        else:

            self.btau=taus[0]
            self.etau=taus[-1]
            self.dtau=6
            if(len(taus) > 1): self.dtau=taus[-1]-taus[-2]
            self.tunits='hr'


        aa=self.area

        if(self.remethod == ''):
            self.reargs="%d,%s,%f,%f,%d,%s,%f,%f"%(aa.ni,self.rexopt,aa.lonW,aa.dx,aa.nj,self.reyopt,aa.latS,aa.dy)
        else:
            self.reargs="%d,%s,%f,%f,%d,%s,%f,%f,%s"%(aa.ni,self.rexopt,aa.lonW,aa.dx,aa.nj,self.reyopt,aa.latS,aa.dy,self.remethod)

        if(not(self.doregrid)): self.reargs=None

        

    def setCtl(self,ctlpath=None,tbdir=None,tdir=None,dols=0):

        self.status=1
        if(ctlpath == None):
            rc=self.getW2fldsRtfimCtlpath(self.model,self.dtg)
            isthere=rc[0]
            if(isthere):
                ctlpath=rc[1]
            else:
                print 'EEE no w2flds for model: ',self.model,' dtg: ',self.dtg
                self.status=0
                return

            (bdir,ctlfile)=os.path.split(ctlpath)
            self.ctlpath=ctlpath

        if(ctlpath != None):
            self.ctlpath=ctlpath
            
        if(hasattr(self,'tdir')):
            if(not(dols)): MF.ChkDir(self.tdir,'mk')
            return
            
                          
        if(tdir != None):
            self.tdir=tdir
            if(not(dols)): MF.ChkDir(self.tdir,'mk')

        elif(tbdir != None):
            bdir="%s/%s"%(tbdir,self.dtg)
            self.tdir="%s/%s/%s"%(tbdir,self.dtg,self.model)
            if(not(dols)): MF.ChkDir(self.tdir,'mk')
            
        return


    def setOutput(self,filename,codename='f77Output.f',f77dir='/tmp'):

        # -- output file name
        #
        self.filename=filename

        # -- output code name
        #
        if(self.outDatType == 'f77'): self.ftype='-sq'

        self.dpath="%s/%s.dat"%(self.tdir,filename)
        self.cpath="%s/%s.ctl"%(self.tdir,filename)
        self.mpath="%s/%s.meta.txt"%(self.tdir,filename)

        if(hasattr(self,'f77dir')):
            self.f77path="%s/%s"%(self.f77dir,codename)
        else:
            self.f77path="%s/%s"%(f77dir,codename)
        
        
    def makeFldMeta(self,taus=None,verb=0):

        aa=self.area

        nk=0

        if(taus == None):
            otaus=self.taus
        else:
            otaus=taus
          
        nvarsUA=0
        if(hasattr(self,'varSl')): 
            nk=len(self.varSl)
            levs=self.varSl
            nvarsUA=len(self.varSuavar)


        nvarsSfc=len(self.vars)
        if(hasattr(self,'varSsfc')):
            nvarsSfc=len(self.varSsfc)
        
##         meta="""filename: %-20s
## grid  ni: %3d  nj: %3d
## lonW: %6.2f  lonE: %6.2f
## latS: %6.2f  latN: %6.2f
## dlon: %6.3f  dlat: %6.3f
## nk: %3d"""%\
##         (self.filename,aa.ni,aa.nj,
##          aa.lonW,aa.lonE,
##          aa.latS,aa.latN,
##          aa.dx,aa.dy,
##          nk,
##          )

        # -- use q dims to get exact dims of the output grid, done in makeFldInput.setLatLonLocal()
        # -- 20170717 -- ukm2 grid > 999 points, change from %3d to %4d
        #
        meta="""filename: %-20s
grid  ni: %4d  nj: %4d
lonW: %6.2f  lonE: %6.2f
latS: %6.2f  latN: %6.2f
dlon: %6.3f  dlat: %6.3f
nk: %3d"""%\
        (self.filename,self.Gnx,self.Gny,
         self.GlonW,self.GlonE,
         self.GlatS,self.GlatN,
         self.Gdx,self.Gdy,
         nk,
         )


        if(nk > 0):
            for lev in levs:
                meta="""%s
%7.1f"""%(meta,lev)

        if(self.doByTau):
            ntaucard='ntf: %3d (N taus/file)'%(len(otaus))
        else:
            ntaucard='ntf: %3d (N taus/file)'%(1)
            
            meta="""%s
%s"""%(meta,ntaucard)

        taucard='nt: %3d (taus)'%(len(otaus))

        meta="""%s
%s"""%(meta,taucard)


        # -- 20230324 -- modify tau in meta to tau-tauoffset to handle 06/18Z ERA5 dtgs
        #
        if(self.doByTau):
            for tau in otaus:
                dtau=tau-self.tauoffset
                meta="""%s
%3d %s"""%(meta,dtau,self.dpaths[tau][-1])

        else:
            for tau in otaus:
                
                meta="""%s
%3d %s"""%(meta,tau,self.dpath)
            

        meta="""%s
nvarsSfc: %3d  nvarsUA: %3d"""%\
        (meta,
         nvarsSfc,nvarsUA,
         )


        if(hasattr(self,'varSsfc')):

            for var in self.varSsfc:
                vp=varProps(var)
                meta="""%s
%-10s %-10s %-30s"""%(meta,vp.vvar,vp.vlev,vp.vdesc)

        
        if(hasattr(self,'varSu') and hasattr(self,'varSuavar')):

            for var in self.varSuavar:
                expr=self.varSu[var][0]
                desc=self.varSu[var][1]
                meta="""%s
%-10s %-10s %-30s"""%(meta,var,'plevs',desc)
        
        else:

            for var in self.vars:
                vp=varProps(var)
                meta="""%s
%-10s %-10s %-30s"""%(meta,vp.vvar,vp.vlev,vp.vdesc)

        MF.WriteString2File(meta,self.mpath,verb=verb)

        return


    def makef77Output(self,taus=None,verb=0):

        f77='''cmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
c
      module f77Output

      use trkParams
      use f77OutputMeta
      use mfutils
      
      implicit none
'''

        if(hasattr(self,'varSsfc')):
            
            for var in self.varSsfc:
                vp=varProps(var)

        if(hasattr(self,'varSu') and hasattr(self,'varSuavar')):

            for var in self.varSuavar:
                expr=self.varSu[var][0]
                desc=self.varSu[var][1]
        
        else:

            for var in self.vars:
                vp=varProps(var)
                fldname=vp.vvar
                if(hasattr(vp,'f77name')): fldname=vp.f77name
                f77="""%s
      real*4, allocatable, dimension(:,:) :: %s"""%(f77,fldname)



        f77=f77+'''
        
      contains

      subroutine initFlds

      integer istat'''

        if(hasattr(self,'varSsfc')):
            for var in self.varSsfc:
                vp=varProps(var)

        if(hasattr(self,'varSu') and hasattr(self,'varSuavar')):
            for var in self.varSuavar:
                expr=self.varSu[var][0]
        
        else:

            for var in self.vars:
                vp=varProps(var)
                fldname=vp.vvar
                if(hasattr(vp,'f77name')): fldname=vp.f77name
                f77="""%s

      allocate(%s(ni,nj),stat=istat)
      if(istat.gt.0) go to 814"""%(f77,fldname)

        f77=f77+"""

      return

 814  continue
      print*,'error in allocate... '
      stop 814
      
      return
      end subroutine initFlds


      subroutine readFlds(ntau)

      integer ntau,iunittcf,ierr,ierrfld,itau,irecvv

      real undef

      character*24 qtitle

c--  initialize variables
c

      undef=1e10
      iunittcf=99

      if(ntf == 1) then
        open(iunittcf,file=trim(DataPaths(ntf)),
     $       form='unformatted',
     $       status='old',err=805)

      else

        open(iunittcf,file=trim(DataPaths(ntau)),
     $       form='unformatted',
     $       status='old',err=805)
      endif"""

        
        if(hasattr(self,'varSsfc')):
            for var in self.varSsfc:
                vp=varProps(var)

        if(hasattr(self,'varSu') and hasattr(self,'varSuavar')):
            for var in self.varSuavar:
                expr=self.varSu[var][0]
        
        else:

            for var in self.vars:
                vp=varProps(var)
                fldname=vp.vvar
                if(hasattr(vp,'f77name')): fldname=vp.f77name
                f77="""%s

c--       read %s
c         
      read(iunittcf,err=810,end=810) %s

      call chkfld(%s,ni,nj,undef,%f,ierrfld)
      if(ierrfld.eq.1) go to 820

      if(verbFld) then
        qtitle='%-6s input           '
        call qprntn(%s,qtitle,1,1,ni,nj,15,6)
      endif"""%(f77,fldname,fldname,fldname,self.pcntundefMax,fldname[0:6],fldname)

        f77=f77+'''
      return

 805  continue
      ierr=1
      print*,'EEEEE: error opening file in readFlds'

 810  continue
      ierr=1
      print*,'EEEEE: error reading field in readFlds'
      return

 820  continue
      ierr=1
      print*,'UUUUU: field undefined ntau: ',ntau

      return

      end subroutine readFlds


      subroutine chkfld(a,ni,nj,undef,pcntundefMax,ierr)

      real undef
      real*4 a,pcntundef,pcntundefMax
      integer i,j,ierr,nundef,ntot,ni,nj

      dimension a(ni,nj)

      ntot=ni*nj
      ierr=0
      nundef=0
      do i=1,ni
        do j=1,nj
          if(abs(a(i,j)).ge.undef) then
            nundef=nundef+1
          endif
        end do
      end do

      pcntundef=float(nundef)/float(ntot)

      
      if(pcntundef >= pcntundefMax) ierr=1
      
      return
      
      end subroutine chkfld


      end module f77Output'''

                


        MF.WriteString2File(f77,self.f77path,verb=verb)

        return



    def makeFldInputGA(self,Bin='grads'):

        # -- do grads: 1) open files; 2) get file data
        #
        from ga2 import setGA

        quiet=self.GAQuiet
        ga=setGA(Bin=Bin,doLogger=self.GAdoLogger,Quiet=quiet)
        ga.ge.fh=ga.open(self.ctlpath)
        ga.ge.getFileMeta()
        
        self.ga=ga
        self.ge=ga.ge

    def isGlobal(self,dlat=2):

        rc=0
        if(hasattr(self,'ge')):
            if(
                (180.0-(abs(self.ge.lat1)+abs(self.ge.lat2)) <= dlat) and
                (360.0-(abs(self.ge.lon1)+abs(self.ge.lon2)) <= dlat)
                ): rc=1

        return(rc)
        
        
    def getDpaths(self,useAvailTaus=0,ttaus=None,verb=0,bail=1):

        # -- meteo
        #
        nfields=len(self.vars)
        aa=self.area
        
        self.meteoTausDone=[]
        self.meteoTaus2Do=[]

        if(self.doByTau == 0 and self.filename != None):
            fullsiz=(nfields*len(self.taus))*aa.ni*aa.nj*4 + (nfields*len(self.taus))*8
            siz=MF.GetPathSiz(dpath)
            if(siz == fullsiz):
                self.meteoTausDone.append('all')
                self.meteoTaus2Do.append('all')
            else:
                self.meteoTausDone.append('all')
                self.meteoTaus2Do.append('all')
                

            print 'III single file with all taus: ',self.dpath
            return
        

        for tau in self.taus:

            if(ttaus != None and not(tau in ttaus)): continue

            self.dpaths[tau]=None

            # -- 20230324 -- modify tau in meteoDone to tau-tauoffset to handle 06/18Z ERA5 dtgs
            #
            ftau=tau
            ftau=tau-self.tauoffset
            
            if(self.filename != None):
                (dir,file)=os.path.split(self.dpath)
                file=file.replace('.dat','.f%03d.dat'%(ftau))
                dpath="%s/%s"%(dir,file)
                
                # -- why? onKishou because of the space in big fs "PROMISE PEGAuS"
                #
                #if(not(onKishou)): dpath=os.path.realpath(dpath)
                #dpath=os.path.realpath(dpath)
                # -- check if already done
                #

                sizmpath=MF.GetPathSiz(self.mpath)
                if(sizmpath == None): sizmpath=-999
                if(hasattr(self,'Gxb')):
                    Fni=self.Gnx
                    Fnj=self.Gny
                    fnij='Gxb'
                    
                elif(sizmpath > 0 ):
                    # get from metafile
                    #
                    mlist=MF.ReadFile2List(self.mpath,verb=verb)
                    for m in mlist:
                        if(mf.find(m,'grid')):
                            tt=m.split()
                            Fni=int(tt[2])
                            Fnj=int(tt[4])
                    fnij=self.mpath

                else:
                    Fni=aa.ni
                    Fnj=aa.nj
                    fnij='area'
                    

                    
                fullsiz=nfields*Fni*Fnj*4 + nfields*8
                fullsiz=nfields*Fni*Fnj*4 + nfields*8
                siz=MF.GetPathSiz(dpath)

                if(verb): print 'WxMAP2.getDpaths() Fni,Fnj: ',Fni,Fnj,' from: ',fnij,' nfields: ',nfields,' fullsiz: ',fullsiz,' siz: ',siz

                if(siz == fullsiz):
                    self.dpaths[tau]=(1,dpath)
                    self.meteoTausDone.append(ftau)
                    if(verb): print 'III(WxMAP2.getDpaths()) already made dpath: ',dpath,' override=0'
                else:
                    if(verb): print 'EEE(WxMAP2.getDpaths()) -- did not make full set of fields for model: ',self.model,' dpath: ',dpath
                    self.meteoTaus2Do.append(ftau)
                    self.dpaths[tau]=(0,dpath)

        self.meteoDone=0
        if(len(self.meteoTausDone) > 0 and useAvailTaus): self.meteoDone=1
        if(len(self.meteoTausDone) > 0 and len(self.meteoTaus2Do) == 0): self.meteoDone=1

        # -- oisst
        #
        nfields=3
        fullsiz=nfields*aa.ni*aa.nj*4 + nfields*8
        siz=MF.GetPathSiz(self.sstdpath)
        
        self.sstDone=0
        if(siz == fullsiz):
            self.sstDone=1
            
        rc=0
        if(self.meteoDone and self.sstDone):
            rc=1
            
        return(rc)
               

    def getVarExpr(self,var,tau,dologz=1,
                   tm1=1,tp1=1,tfm1=0.5,tfp1=0.5,verb=0):
        """ special variable -> expression handling"""

        ga=self.ga

        zthk900_600="(%s-%s)"%(self.zCpsexpr[600],self.zCpsexpr[900])
        zthk600_300="(%s-%s)"%(self.zCpsexpr[300],self.zCpsexpr[600])

        zthk900_600Tinterp="(%s-%s)"%(self.zCpsexprTinterp[600],self.zCpsexprTinterp[900])
        zthk600_300Tinterp="(%s-%s)"%(self.zCpsexprTinterp[300],self.zCpsexprTinterp[600])

        vp=varProps(var)
        expr=vp.vexpr
        
        try:
            doTinterp=self.doTinterp[tau]
        except:
            doTinterp=0
            
        # -- set vtexpr for var t interp expr for case of doing log z interp below...
        #
        vtexpr=None
        if(doTinterp):
            if(hasattr(vp,'vexprTinterp')):
                expr=vp.vexprTinterp
                if(expr != None):
                    expr=expr.replace('TM1',str(tm1))
                    expr=expr.replace('TP1',str(tp1))
                    expr=expr.replace('TFM1',str(tfm1))
                    expr=expr.replace('TFP1',str(tfp1))
                    vtexpr=expr
                
                    
            else:
                print 'EEE need to do Tinterp but vexprTinterp not in getVarExpr.varProps'
                sys.exit()
            
        if(vp.vvar == 'zthklo'):
            expr=zthk900_600
            if(doTinterp): expr=zthk900_600Tinterp

        elif(vp.vvar == 'zthkup'):
            expr=zthk600_300
            if(doTinterp): expr=zthk600_300Tinterp

        elif(vp.vvar[0] == 'z' and vp.vexpr == 'getexpr'):
            zlev=int(vp.vvar[1:])
            expr=self.zCpsexpr[zlev]
            if(doTinterp): expr=self.zCpsexprTinterp[zlev] 


        elif((vp.vvar == 'vrt925' or vp.vvar == 'vrt850' or vp.vvar == 'vrt700') and dologz):

            zlev=int(vp.vvar[-3:])
            uaxpr=ga.LogPinterp('ua',zlev)
            vaxpr=ga.LogPinterp('va',zlev)
            
            if(doTinterp):
                uaxprm1=ga.LogPinterp('ua',zlev,texpr='t-%d'%(tm1))
                vaxprm1=ga.LogPinterp('va',zlev,texpr='t-%d'%(tm1))
                uaxprp1=ga.LogPinterp('ua',zlev,texpr='t+%d'%(tp1))
                vaxprp1=ga.LogPinterp('va',zlev,texpr='t+%d'%(tp1))
                expr='(hcurl((%s+%s)*%f,(%s+%s)*%f)*1e5)'%(uaxprm1,uaxprp1,tfm1,vaxprm1,vaxprp1,tfp1)
            else:
                expr='(hcurl(%s,%s)*1e5)'%(uaxpr,vaxpr)
                

        elif(vp.vvar == 'pr'):

            prexpr=self.m2.setprvar(dtg=self.dtg,tau=tau)
            prexpr=prexpr.split('=')[1]
            expr="(%s)"%(prexpr.replace("""'""",''))
            
            # 20111102 -- bypass for ecmwf/ukm/cmc -- just use current tau -- problem is complicated expression for pr that include (t+0|1|2)
            #
            if(doTinterp
               and not(self.model == 'ecm2')
               and not(self.model == 'ecm4')
               and not(self.model == 'ecm5')
               and not(self.model == 'ukm2')
               and not(self.model == 'cmc2')
               and not(self.model == 'cgd2')
               ):
                expr=expr.replace('(t+0)','')
                expr=expr.replace('pr','(pr(t-%d)*%f + pr(t+%d)*%f)'%(tm1,tfm1,tp1,tfp1))

        elif(vp.vvar == 'prc'):

            prexpr=self.m2.setprvarc(dtg=self.dtg,tau=tau)
            prexpr=prexpr.split('=')[1]
            expr="(%s)"%(prexpr.replace("""'""",''))
            
            # 20111102 -- bypass for ecmwf/ukm/cmc -- just use current tau -- problem is complicated expression for pr that include (t+0|1|2)
            #
            if(doTinterp
               and not(self.model == 'ecm2')
               and not(self.model == 'ecm4')
               and not(self.model == 'ecm5')
               and not(self.model == 'ukm2')
               and not(self.model == 'cmc2')
               and not(self.model == 'cgd2')
               ):
                expr=expr.replace('(t+0)','')
                expr=expr.replace('pr','(pr(t-%d)*%f + pr(t+%d)*%f)'%(tm1,tfm1,tp1,tfp1))

        elif(vp.vvar == 'prw' or vp.vvar == 'prwup'):

            rhfact='0.01'
            # -- ngp2 going to ncep is now navgem as of 20130312
            #if(self.model == 'ngp2'): rhfact='1.0'
            vaporP='(esmrf(ta)*hur*%s)'%(rhfact)
            vaporP='(esmrf(const(ta,273.16,-u))*hur*%s)'%(rhfact)
            
            # -- special case of hi-res CMC
            #
            if(self.model == 'cgd2'):
                mixingR='hus'
            else:
                mixingR="0.622*(%s/(lev-%s))"%(vaporP,vaporP)
            prwexpr="vint(psl*0.01,%s,100)"%(mixingR)
            if(vp.vvar == 'prwup'):
                prwexpr="vint(const(psl,400,-a),%s,100)"%(mixingR)
            if(doTinterp):
                vaporP='(esmrf(const((ta(t-%d)*%f + ta(t+%d)*%f),273.16,-u))*((hur(t-%d)*%f + hur(t+%d)*%f)*%s))'%(tm1,tfm1,tp1,tfp1,
                                                                                                                   tm1,tfm1,tp1,tfp1,
                                                                                                                   rhfact)
                mixingR="(0.622*(%s/(lev-%s)))"%(vaporP,vaporP)
                prwexpr="vint( (psl(t-%d)*%f + psl(t+%d)*%f) * 0.01,%s,100)"%(tm1,tfm1,tp1,tfp1,mixingR)

            # -- special case
            #
            if(self.model == 'gfs2'): prwexpr='prw'
            if(self.model == 'ecmt'): prwexpr='prw'
            if(self.model == 'ecm5'): prwexpr='prw'
            if(self.model == 'era5'): prwexpr='prw'
            
            expr=prwexpr

        # -- inf zinterp flag set from varProps
        if(vp.zinterp):
            if(vtexpr != None):
                expr=ga.LogPinterp(vtexpr,vp.vlev)
            else:
                expr=ga.LogPinterp(vp.vexpr,vp.vlev)

        if(verb): print 'vvvvvvvvvvvvvvv ',vtexpr,vp.vvar,expr

        return(vp,expr)
    

    def getValidTaus(self,ratioMax=0.05,pThere=0.80,dofullChk=0,verb=0):
        
        """ find taus with undef """

        self.doTinterp={}
        self.stats={}
        
        ntaus=len(self.taus)
        
        for n in range(0,ntaus):

            tau0=self.taus[n]
            taum1=tau0
            taup1=tau0

            nm1=n
            np1=n
            
            if(n > 0):
                nm1=n-1
            if(n < ntaus-1):
                np1=n+1

            taum1=self.taus[nm1]
            taup1=self.taus[np1]

            nvalidMin=1e20
            nundefMax=-1e20

            pcntThere=[]
            
            fdtg=mf.dtginc(self.mdtg,tau0)
            for n in range(0,len(self.vars)):

                self.ga.ge.setTimebyDtg(fdtg,verb=0)
                if(hasattr(self,'getVarExpr') and dofullChk):
                    (vp,expr)=self.getVarExpr(self.vars[n],tau0)
                    varExpr=expr
                else:
                    vp=varProps(self.vars[n])
                    varExpr=vp.vexpr
                
                if(vp.vlev > 0):
                    self.ga('set lev %d'%(vp.vlev))
                else:
                    self.ga('set z 1')
    
                try:
                    self.stats[tau0]=self.ga.get.stat(varExpr)
                except:
                    if(dofullChk):
                        print 'WWWWWWWWWWWW bad stats',vp.vvar,varExpr,fdtg,' dofullChk'
                    continue
                
                nvalid=self.stats[tau0].nvalid
                nundef=self.stats[tau0].nundef

                # -- ratio of undef / total
                
                ratioundef2total=1.0
                if(nvalid > 0):
                    ratioundef2total=float(nundef)/(float(nvalid)+float(nundef))

                there=1
                if(ratioundef2total > ratioMax and  tau0 != 0): there=0
                pcntThere.append(there)

                if(nvalid < nvalidMin): nvalidMin=nvalid
                if(nundef > nundefMax): nundefMax=nundef
                
                if(verb):
                    print 'VVVVVVVVVVVVVVVV ',n,tau0,vp.vlev,varExpr,tau0,nvalid,nundef
                    print 'MMMMMMMMMMMMMMMM ',tau0,nvalidMin,nundefMax


            # -- final check if we should do an interp in time
            #
            
            self.doTinterp[tau0]=0

            # -- percent complete
            #
            nthere=len(pcntThere)
            there=0
            for t in pcntThere:
                there=there+t

            pcntComplete=0.0
            if(nthere > 0):
                pcntComplete=float(there)/float(nthere)

            if(pcntComplete < pThere):
                self.doTinterp[tau0]=1
                print 'PPP--doTinterp tau: ',tau0,pcntComplete,' pThere: ',pThere
            

            if(not(dofullChk)):
                # -- max/min undef/valid
                #
                nvalid=nvalidMin
                nundef=nundefMax
                ratioundef2valid=1.0
                if(nvalid > 0):
                    ratioundef2valid=float(nundef)/float(nvalid)
                if(ratioundef2valid > ratioMax and tau0 != 0):
                    self.doTinterp[tau0]=1
                    print 'SSS--doTinterp tau: ',tau0,self.stats[tau0].nundef
                
            ##self.stats[tau0].ls()


    def makeFldInput(self,
                     dogetValidTaus=1,
                     doconst0=0,
                     doglobal=0,
                     override=0,
                     verb=0,
                     taus=None,
                     ):


        def setLatlonGlobal():

            ge=self.ge
            
            cmd="""set lat %f %s
set lon %f %f"""%(ge.lat1,ge.lat2,ge.lon1,ge.lon2)
            ga(cmd)

        def setLatlonLocal(expand=1,getIgridDims=0):

            # -- expand data grid +/- 1point in x and y for vort calc
            # -- dregrid() uses re() to dump exact grid
            #
            aa=self.area

            dy=dx=0.0
            if(expand):
                dy=aa.dy
                dx=aa.dx
            
            flatS=aa.latS-dy
            flatN=aa.latN+dy

            if(flatS < -90.0): flatS=-90.0
            if(flatN >  90.0): flatN= 90.0

            # -- set the output dimension env
            #
            cmd="""set lat %f %s
set lon %f %f"""%(flatS,flatN,aa.lonW-dx,aa.lonE+dx)
            ga(cmd)

            # -- use grads dim env to get dims of input grid
            #
            if(getIgridDims):
                gh=ga.query('dims',Quiet=1)

                nx=gh.nx
                ny=gh.ny
                (xb,xe)=gh.xi
                (yb,ye)=gh.yi

                # -- assume cyclic continuity in x
                #
                if(xe > len(ge.lons)): xe=xe-len(ge.lons)

                lonb=ge.lons[xb-1]
                lone=ge.lons[xe-1]

                latb=ge.lats[yb-1]
                late=ge.lats[ye-1]

                # -- assum constant grid increment
                #
                self.Adx=ge.lons[-1]-ge.lons[-2]
                self.Ady=ge.lats[-1]-ge.lats[-2]

                self.Axb=xb
                self.Axe=xe

                self.Ayb=yb
                self.Aye=ye

                self.Anx=nx
                self.Any=ny

                self.Alatb=latb
                self.Alate=late

                self.Alonb=lonb
                self.Alone=lone

            

        self.varPs={}
        self.ovars=[]

        for var in self.vars:
            vp=varProps(var)
            self.ovars.append(vp.vvar)
            self.varPs[vp.vvar]=[vp.vexpr,vp.vlev,vp.afact,vp.mfact,vp.vdesc]

        self.getDpaths()

        if(self.meteoDone and not(override)):
            print """III self.meteoDone ... and not(override)...don't need to makeFldInput...return..."""
            return


        if(self.doByTau == 0):
            self.getDpaths()
            siz=MF.GetPathSiz(self.dpath)
            if(override == 0 and  (siz != None and siz > 0) and self.meteoDone == 0):
                print 'WWW doByTau=1 and self.dpath: ',self.dpath,' already exists...bail...'
                sys.exit()
            return
            
            
        if(not(hasattr(self,'ga'))):
            self.makeFldInputGA()
            
        ga=self.ga
        ge=self.ge


        # -- expressions for hart cps
        #
        zlevsCps=[900,850,800,750,700,650,600,550,500,450,400,350,300]

        self.zCpsexpr={}
        self.zCpsexprTinterp={}
        
        for zlev in zlevsCps:
            self.zCpsexpr[zlev]=ga.LogPinterp('zg',zlev)
            self.zCpsexprTinterp[zlev]=ga.LogPinterpTinterp('zg',zlev)


        # -- set undef
        #
        ga('set undef %g'%(self.undef))

        # -- get valid taus
        #
        if(dogetValidTaus):
            MF.sTimer('getValidTaus')
            self.getValidTaus(dofullChk=0,verb=0)
            MF.dTimer('getValidTaus')

        nfields=len(self.vars)
        
        ga.verb=verb

        if(self.doByTau == 0):
            ga.ge.setFwrite(name=self.dpath,type=self.ftype)
            ga('set gxout fwrite')
            alreadyDone=0

        mtaus=self.taus

        for tau in mtaus:
            
            otau=tau

            timerlab='fldtau: %s : %4s : %s : %s'%(self.areaname,otau,self.dtg,self.model)
            MF.sTimer(timerlab)

            if(self.doByTau):

                (rc,dpath)=self.dpaths[otau]
                #print 'ooooooooooooooooo',otau,rc,dpath
                if(rc == 0 or override):
                    ga.ge.setFwrite(name=dpath,type=self.ftype)
                    ga('set gxout fwrite')
                    alreadyDone=0
                else:
                    alreadyDone=1
                    continue

            # -- since we're setting time by dtg -- will automatically account for the tauOffset!
            #
            fdtg=mf.dtginc(self.dtg,tau)
            ga.ge.setTimebyDtg(fdtg)

            dologz=1
            for var in self.vars:
                # -- get expression to output; includes special variable handling
                #
                (vp,expr)=self.getVarExpr(var,tau,dologz=dologz)

                if(vp.testvar != None):
                    tvar=vp.testvar
                    if(not(tvar in ge.vars)):
                        expr="const(lat,%f,-a)"%(ge.undef)
                        if(self.diag): print 'III WxMAP2.varProps: setting: ',tvar,' to undef using expr: ',expr
                    
                # -- set the plev
                #
                if(vp.vlev > 0):
                    ga('set lev %d'%(vp.vlev))
                else:
                    ga('set z 1')

                # -- avoid conflict with grads var names and defined vars
                #
                varD=vp.vvar+'X'

                # -- set the lat/lon dim env to global and do define
                #
                if(doglobal and self.isGlobal()):
                    rc=setLatlonGlobal()
                    ga.dvar.var(varD,expr)

                    
                # -- set the lat/lon dim to local
                #
                # -- expand one grid point in all directions for 
                rc=setLatlonLocal(expand=1)
                ga.dvar.var(varD,expr)
                
                # -- apply mfact
                #
                if(vp.mfact != None and vp.mfact != -999):
                    mexpr='%s*%f'%(varD,vp.mfact)
                    ga.dvar.var(varD,mexpr)
                
                getIgridDims=0
                if(not(hasattr(self,'Gxb'))): getIgridDims=1
                
                rc=setLatlonLocal(expand=0,getIgridDims=getIgridDims)

                # -- get the exact grid dims of the output grid
                #
                if(not(hasattr(self,'Gxb'))):

                    if(self.doregrid == 0):
                        
                        self.Gxb=self.Axb
                        self.Gxe=self.Axe
                    
                        self.Gyb=self.Ayb
                        self.Gye=self.Aye
                        
                        self.Gdx=self.Adx
                        self.Gdy=self.Ady
                        
                        
                        self.Gnx=self.Anx
                        self.Gny=self.Any
                        
                        self.GlatS=self.Alatb
                        self.GlatN=self.Alate
                        
                        self.GlonW=self.Alonb
                        self.GlonE=self.Alone

                    else:

                        aa=self.area
                        
                        self.Gxb=aa.lonW
                        self.Gxe=aa.lonE
                    
                        self.Gyb=aa.latS
                        self.Gye=aa.latN
                        
                        self.Gdx=aa.dx
                        self.Gdy=aa.dy
                        
                        
                        self.Gnx=aa.ni
                        self.Gny=aa.nj
                        
                        self.GlatS=aa.latS
                        self.GlatN=aa.latN
                        
                        self.GlonW=aa.lonW
                        self.GlonE=aa.lonE
                        
                        
                if(self.reargs != None):
                    dore=1
                    if(doconst0):
                        #ga.dvar.dregrid0(vp.vvar,expr,self.reargs,undef=self.undef)
                        print '000000000000000000',varD,self.reargs
                        gacmd=ga.dvar.dregrid0(varD,varD,self.reargs,undef=self.undef)
                    else:
                        #ga.dvar.dregrid(vp.vvar,expr,self.reargs)
                        gacmd=ga.dvar.dregrid(varD,varD,self.reargs)

                else:
                    dore=0
                    if(doconst0):
                        gacmd=ga.dvar.dundef0(varD)
                    else:
                        ga('d %s'%(varD))
                        gacmd=varD

                if(verb):
                    print 'vvvvvv varD: %-20s'%(varD),' expr: ',gacmd
                    
                    
            if(self.doByTau):   ga('disable fwrite')

            
            MF.dTimer(timerlab)

        ga('disable fwrite')
        

        self.ga=ga
        self.ge=ga.ge

        if(override or alreadyDone == 0):
            self.makeCtlfile()
            self.makeFldMeta()
            self.makef77Output()


    def makeCtlfile(self):

        aa=self.area
        gtime=mf.dtg2gtime(self.dtg)

        (ddir,dfile)=os.path.split(self.dpath)

        if(self.doByTau):
            dfile=dfile.replace('.dat','''.f%f3.dat''')

        self.ctl="""dset ^%s
title test
undef %g
options sequential template
xdef %3d linear %7.2f %7.3f
ydef %3d linear %7.2f %7.3f"""%(dfile,self.undef,
            self.Gnx,self.GlonW,self.Gdx,
            self.Gny,self.GlatS,self.Gdy)

        #if(hasattr(self,'varSsfc')):

        self.makeCtlZdef()

        btau=self.taus[0]
        etau=self.taus[-1]
        if(self.dtau > 0):
            ntimes=(etau-btau)/self.dtau +1
        else:
            print 'EEE dtau in WxMAP2.f77GridOutput.makeCtlfile() '
            sys.exit()
            
        self.ctl=self.ctl+"""
%s
tdef %d linear %s %d%s"""%(
            self.zdef,ntimes,gtime,self.dtau,self.tunits,
            )
        
        self.makeCtlVars()

        MF.WriteString2File(self.ctl,self.cpath,verb=1)


    def makeCtlZdef(self):
        
        if(hasattr(self,'varSl')):
            self.zdef='zdef  %d levels'%(len(self.varSl))
            for lev in self.varSl:
                self.zdef=self.zdef+' %d'%(lev)

        else:
            self.zdef='zdef  1 levels 1013'




    def makeCtlVars(self):

        if(hasattr(self,'varSuavar') and hasattr(self,'varSl') and hasattr(self,'varSsfc') ):

            sfvars=self.varSsfc
            uavars=self.varSuavar

            self.ctl="""%s
vars %d"""%(self.ctl,len(sfvars)+len(uavars))

            for var in sfvars:
                vp=varProps(var)
                self.ovars.append(vp.vvar)
                card="%-12s %3d 0 %s"%(vp.vvar,0,vp.vdesc)
                self.ctl="""%s
%s"""%(self.ctl,card)


            for var in uavars:
                (vexpr,vlev,afact,mfact,vdesc)=self.varPs[var]
                #vexpr=self.varSu[var][0]
                #vdesc=self.varSu[var][-1]
                card="%-12s %3d 0 %s"%(var,len(self.varSl),vdesc)
                self.ctl="""%s
%s"""%(self.ctl,card)

        else:
            
            self.ctl=self.ctl+"""
vars %d"""%(
                len(self.vars),
                )

            for var in self.ovars:
                (vexpr,vlev,afact,mfact,vdesc)=self.varPs[var]
                card="%-12s 0 0 %s"%(var,vdesc)
                self.ctl="""%s
%s"""%(self.ctl,card)

        
        self.ctl="""%s
endvars"""%(self.ctl)



    def clean(self):

        try:
            os.unlink(self.dpath)
        except:
            print 'EEE unable to rm: ',self.dpath

        

class varProps(MFbase):

    def __init__(self,var=None,
                 vvar=None,
                 vexpr=None,
                 vexprTinterp=None,
                 vlev=None,
                 afact=None,
                 mfact=None,
                 vdesc=None,
                 f77name=None,
                 testvar=None,
                 ):

        if(var != None):
            
            tt=var.split(':')

            if(len(tt) == 6):
                (vvar,vexpr,vlev,afact,mfact,vdesc)=tt
            elif(len(tt) == 7):
                (vvar,vexpr,vexprTinterp,vlev,afact,mfact,vdesc)=tt
            elif(len(tt) == 8):
                (vvar,vexpr,vexprTinterp,vlev,afact,mfact,vdesc,f77name)=tt
            elif(len(tt) == 9):
                (vvar,vexpr,vexprTinterp,vlev,afact,mfact,vdesc,f77name,testvar)=tt
                
            if(f77name == None): f77name=vvar

            zinterp=0
            if(vlev[0] == 'Z'):
                vlev=str(vlev[1:])
                zinterp=1
                
            vlev=float(vlev)
            afact=float(afact)
            mfact=float(mfact)

        self.vvar=vvar
        self.vexpr=vexpr
        self.vexprTinterp=vexprTinterp
        self.vlev=int(vlev)
        self.zinterp=zinterp
        self.afact=afact
        self.mfact=mfact
        self.vdesc=vdesc
        self.f77name=f77name
        self.testvar=testvar







#uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu
# unbounded methods


def getW2Area(area):

    # -- tropical W2 areas
    #
    if(area == 'tropwpac'):
        AA=W2areaWpac()
    elif(area == 'tropepac'):
        AA=W2areaEpac()
    elif(area == 'tropcpac'):
        AA=W2areaCpac()
    elif(area == 'troplant'):
        AA=W2areaLant()
    elif(area == 'tropsio'):
        AA=W2areaSio()
    elif(area == 'tropnio'):
        AA=W2areaNio()
    elif(area == 'tropio'):
        AA=W2areaIo()
    elif(area == 'tropswpac'):
        AA=W2areaSwpac()
    elif(area == 'tropshem'):
        AA=W2areaShem()
        
    # - prw/goes areas
    #
    elif(area == 'prwLant'):
        AA=W2areaPrwLant()
    elif(area == 'prwEpac'):
        AA=W2areaPrwEpac()
    elif(area == 'prwEnso'):
        AA=W2areaPrwEnso()
    elif(area == 'prwCEpac'):
        AA=W2areaPrwCEpac()
    elif(area == 'prwCpac'):
        AA=W2areaPrwCpac()
    elif(area == 'prwWpac'):
        AA=W2areaPrwWpac()
    elif(area == 'prwIo'):
        AA=W2areaPrwIo()
    elif(area == 'prwSpac'):
        AA=W2areaPrwSpac()
    else:
        AA=None

    return(AA)


if (__name__ == "__main__"):

    w2=W2()
    w2.ls()

#    w2e=W2env()
#    w2e.ls()
    
    sys.exit()

        

               
    
    



                 

                 

    
