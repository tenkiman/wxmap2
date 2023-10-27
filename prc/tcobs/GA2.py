import mf

from M import MFbase

from WxMAP2 import W2BaseDirApp

from grads.ganum import GaNum

class GaGrads(GaNum,MFbase):
    
    gaxgrads='grads2'
    gaopt=None
    gawindow=0
    type='ganum'
    
    class gxset(MFbase):

        def __init__(self,ga):
            self._cmd=ga.cmd
            self._rl=ga.rline
            self._nL=ga.nLines
            
    
        def latlon(self,lat1=-90,lat2=90,lon1=0,lon2=360):
            self._cmd("set lat %f %f"%(lat1,lat2))
            self._cmd("set lon %f %f"%(lon1,lon2))
    
        def lev(self,lev1=500,lev2=None):
            if(lev2 == None): lev2=lev1
            self._cmd("set lev %f %f"%(lev1,lev2))
    
    
        def time(self,time=None):
    
            if(time == None):
                self._cmd('q time')
                card=self._rl(self._nL)
    
            self._cmd("set time %s"%(time))
    
    
        def dtg(self,dtg=None):
    
            name="%s.%s"%(self.__module__,'gxset.dtg')
            if(dtg == None):
                print 'WWW dtg must be set in: ',name
            else:
                gtime=mf.dtg2gtime(dtg)
                if(gtime != None):
                    self._cmd("set time %s"%(gtime))
                else:
                    print 'EEE invalid dtg in: ',name

    
    def __init__(self,
                 lat1=-90.0,
                 lat2=90.0,
                 lon1=0.0,
                 lon2=360.0,
                 lev1=500,
                 lev2=None,
                 pareaxl=0.5,
                 pareaxr=10.0,
                 pareayb=0.5,
                 pareayt=8.0,
                 orientation='landscape',
                 xlint=10.0,
                 ylint=5.0,
                 lintscale=1.0,
                 mapdset='hires',
                 mapcol=15,
                 mapstyle=0,
                 mapthick=6,
                 grid='on',
                 gridcol=1,
                 gridstyle=3,
                 pngmethod='printim',
                 gradslab='off',
                 timelab='off',
                 quiet=0,
                 xgrads=gaxgrads,
                 window=gawindow,
                 opt=gaopt,
                 ge=None,
                 verb=0                
                 ):

        if(opt != None):
            Opt=opt
        else:
            Opt=''
            
        self.ga=GaNum(Bin=xgrads,Opts=Opt,Verb=verb,Window=window)
        
        
        self.ga.quiet=quiet
        
        if(quiet):   self._cmd=self.ga.cmdQ
        else:        self._cmd=self.ga.cmd
        
        self._ga=self.ga
        self._ge=ge
        
        self.Verb = verb
        self.Writer = self.ga.Writer
        self.Reader = self.ga.Reader
        
        self.Echo = self.ga.Echo
        self.Strict = self.ga.Strict
        self.Version = self.ga.Version
        
        
        #self.ga.gxout=gxout(self.ga)
        self.ga.set=self.gxset(self.ga)
        #self.ga.dvar=gxdefvar(self.ga)
        #self.ga.get=gxget(self.ga)
        
        
        self.lat1=lat1
        self.lat2=lat2
        self.lon1=lon1
        self.lon2=lon2
        self.lev1=lev1
        self.lev2=lev2
        self.rl=self.ga.rline
        self.rw=self.ga.rword
        self.pareaxl=pareaxl
        self.pareaxr=pareaxr
        self.pareayb=pareayb
        self.pareayt=pareayt
        self.xlint=xlint
        self.ylint=ylint
        self.lintscale=lintscale

        self.mapdset=mapdset
        self.mapcol=mapcol
        self.mapstyle=mapstyle
        self.mapthick=mapthick

        self.grid=grid
        self.gridcol=gridcol
        self.gridstyle=gridstyle

        self.pngmethod=pngmethod

        self.timelab=timelab
        self.gradslab=gradslab


    
 #   def cmd ( self, gacmd, Quiet=False, Block=True ):
 #       """  
 #       Sends a command to GrADS. When Block=True, the output is captured 
 #       and can be retrieved by methods rline() and rword(). On input,
 #       *gacmd* can be a single GrADS command or several commands separated
 #       by a new line ('\n').
 #       """
 #       Verb = self.Verb
 #       for cmd_ in gacmd.split('\n'):
 #           cmd = cmd_ + '\n' 
 #           self.Writer.write(cmd)
 #           self.Writer.flush()
 #           if Block:
 #               rc = self._parseReader(Quiet)
 #               if rc != 0: 
 #                   if Verb==1:   print "rc = ", rc, ' for ' + cmd_ 
 #                   raise GrADSError, 'GrADS returned rc=%d for <%s>'%(rc,cmd_)
 #               else:
 #                   if Verb>1:    print "rc = ", rc, ' for ' + cmd_ 
 #       return
 #    
 #   __call__ = cmd


     
 #   def cmdQ ( self, gacmd, Quiet=True, Block=True ):
 #       """  
 #       Sends a command to GrADS. When Block=True, the output is captured 
 #       and can be retrieved by methods rline() and rword(). On input,
 #       *gacmd* can be a single GrADS command or several commands separated
 #       by a new line ('\n').
 #       """
 #       Verb = self.Verb
 #       for cmd_ in gacmd.split('\n'):
 #           cmd = cmd_ + '\n' 
 #           self.Writer.write(cmd)
 #           self.Writer.flush()
 #           if Block:
 #               rc = self._parseReader(Quiet)
 #               if rc != 0: 
 #                   if Verb==1:   print "rc = ", rc, ' for ' + cmd_ 
 #                   raise GrADSError, 'GrADS returned rc=%d for <%s>'%(rc,cmd_)
 #               else:
 #                   if Verb>1:    print "rc = ", rc, ' for ' + cmd_ 
 #       return
    
    def makePng(self,
                opath,
                xsize=1024,
                ysize=768,
                background='black',
                ropt='',
                ):

        if(self.pngmethod == 'printim'):
            cmd="%s %s x%d y%d"%(self.pngmethod,opath,xsize,ysize)
        elif(self.pngmethod == 'gxyat'):
            bkopt=''
            if(background == 'black'):
                bkopt='-r'
            cmd="%s -x %d -y %d %s %s"%(self.pngmethod,xsize,ysize,bkopt,opath)
        self._cmd(cmd)
        
        
    def makePngTransparent(self,opath,ropt=''):
        
        cmd="convert -transparent black %s %s"%(opath,opath)
        mf.runcmd(cmd)
        
        cmd="convert -transparent white %s %s"%(opath,opath)
        mf.runcmd(cmd)
        
    def makePngDissolve(self,pathfeature,pathbase,pathall,
                       disolvfrc=25,
                       ropt=''):

        cmd="composite -dissolve %f %s %s %s"%(disolvfrc,pathfeature,pathbase,pathall)
        mf.runcmd(cmd)
        
        
    def setMap(self):

        self._cmd('set mpdset %s'%(self.mapdset))
        self._cmd('set map %d %d %d'%(self.mapcol,self.mapstyle,self.mapthick))
                  
    def drawMap(self):
        self._cmd('draw map')

    def clear(self):
        self._cmd('c')
        

    def getLevs(self):

        if(not(hasattr(self._ga,'fh'))):
            print """WWW in GA.GradsEnv...need a 'fh' var to get levs..."""
        else:
            nz=self._ga.fh.nz
            self.dimLevs=list(self._ga.coords().lev)
            self.dimNlevs=len(self.dimlevs)
            self._cmd("set z 1 %d"%(nz))
            self.Levs=list(self._ga.coords().lev)
            print 'nnnnnnnnnnnnnnnnnn ',nz,self.dimlevs,self.dimNlevs,self.Levs
            

    def getFileMeta(self,obj=None):

        if(not(hasattr(self._ga,'fh'))):
            print """WWW in GA.GradsEnv...need a 'fh' var to get filemeta data..."""
        else:
            if(obj == None): obj=self
            obj.nx=self._ga.fh.nx
            obj.ny=self._ga.fh.ny
            obj.nz=self._ga.fh.nz
            obj.nt=self._ga.fh.nt

            obj.dimlevs=list(self._ga.coords().lev)
            obj.dimNlevs=len(obj.dimlevs)
            self._cmd("set z 1 %d"%(obj.nz))
            obj.levs=list(self._ga.coords().lev)
            obj.vars=list(self._ga.fh.vars)
            self._cmd("set lev %d"%(obj.dimlevs[0]))
            



    def getGxinfo(self):

        self._cmd('q gxinfo')
        
        #n  1 Last Graphic = Contour
        #n  2 Page Size = 11 by 8.5
        #n  3 X Limits = 0.5 to 10.5
        #n  4 Y Limits = 1.25 to 7.25
        #n  5 Xaxis = Lon  Yaxis = Lat
        #n  6 Mproj = 2

        self.lastgraphic=self.rw(1,4)
        self.pagex=float(self.rw(2,4))
        self.pagey=float(self.rw(2,6))
        self.plotxl=float(self.rw(3,4))
        self.plotxr=float(self.rw(3,6))
        self.plotyb=float(self.rw(4,4))
        self.plotyt=float(self.rw(4,6))
        self.xaxis=self.rw(5,3)
        self.yaxis=self.rw(5,6)

    def getGxout(self):

        self._cmd('q gxout')
        self.gxoutg1s=self.rw(2,6)
        self.gxoug1v=self.rw(3,6)
        self.gxoug2s=self.rw(4,6)
        self.gxoug2v=self.rw(5,6)
        self.gxoustn=self.rw(6,4)

    def getShades(self,verb=0):

        self._cmd('q shades')
        nl=self._ga.nLines
        
        self.nshades=int(self.rw(1,5))

        self.colbar=[]
        for n in range(2,nl+1):
            col=int(self.rw(n,1))
            minval=self.rw(n,2)
            maxval=self.rw(n,3)
            if(minval == '<'):
                minval=-1e20
                maxval=float(maxval)
            elif(maxval == '>'):
                minval=float(minval)
                maxval=1e20
            else:
                minval=float(minval)
                maxval=float(maxval)

            self.colbar.append([col,minval,maxval])
            if(verb): print n,col,minval,maxval

    def setShades(self,pcuts,pcols):

        nl=len(pcols)
        self.nshades=nl

        self.colbar=[]

        for n in range(0,nl):
            col=pcols[n]

            if(n == 0):
                minval=-1e20
                maxval=pcuts[n]
            elif(n == nl-1):
                minval=pcuts[n-1]
                maxval=1e20
            else:
                minval=pcuts[n-1]
                maxval=pcuts[n]

            minval=float(minval)
            maxval=float(maxval)
            
            self.colbar.append([col,minval,maxval])

        

    def getShadeCol(self,val):

        if(not(hasattr(self,'colbar'))):
            print 'WWW need to run getShades() before using getShadeCol()'
            return
        
        rval=float(val)
        for colb in self.colbar:
            (col,minval,maxval)=colb
            if(rval > minval and rval <= maxval):
                return(col)

        
        

    def setParea(self):

        self._cmd("set parea %6.3f %6.3f %6.3f %6.3f"%(self.pareaxl,
                                                       self.pareaxr,
                                                       self.pareayb,
                                                       self.pareayt))

    def setGrid(self):
        self._cmd('set grid %s %d %d'%(self.grid,self.gridcol,self.gridstyle))
        
        
    def setXylint(self,scale=None):

        if(scale == None):  lscale=self.lintscale
        else: lscale=scale
        xlint=self.xlint*lscale
        ylint=self.ylint*lscale
        self._cmd("set xlint %6.3f"%(xlint))
        self._cmd("set ylint %6.3f"%(ylint))

    def setPlotScale(self):
        self._cmd('set grads %s'%(self.gradslab))
        self._cmd('set timelab %s'%(self.timelab))
        self._cmd('set cmax -1000')
        self._cmd('set grid on 3 15')
        self._cmd('d lat')


    def setLatLon(self):
        self._cmd("set lat %f %f"%(self.lat1,self.lat2))
        self._cmd("set lon %f %f"%(self.lon1,self.lon2))

    def setLevs(self):

        if(not(hasattr(self._ga,'lev2')) or self.lev2 == None):
            self.lev2=self.lev1
        self._cmd("set lev %f %f"%(self.lev1,self.lev2))

        
    def setColorTable(self,table='jaecolw2.gsf'):
        self._cmd("run %s"%(table))

    def setTimebyDtg(self,dtg,verb=1):
        gtime=mf.dtg2gtime(dtg)
        if(verb): print "set time to: %s  from: %s"%(gtime,dtg)
        self._cmd("set time %s"%(gtime))

    def setTimebyDtgTau(self,dtg,tau,verb=1):
        vdtg=mf.dtginc(dtg,tau)
        gtime=mf.dtg2gtime(vdtg)
        if(verb): print "set time to: %s  from dtg: %s tau: %d"%(gtime,dtg,tau)
        self._cmd("set time %s"%(gtime))

    def reinit(self):
        self._cmd("reinit")

    
if (__name__ == '__main__'):
    
    gagrads = GaGrads()
