import mf
from M import MFbase,MFutils
MF=MFutils()

from WxMAP2 import W2BaseDirApp,W2BaseDirPrc

MF.sTimer(tag='load grads')
from grads import GaCore,GrADSError
#from grads import GaNum,GaLab,GaCore,GrADSError
MF.dTimer(tag='load grads')


#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# classes
#



class gXbasemap2(MFbase):

    
    def __init__(self,ga,ge):

        self._cmd=ga
        self._ge=ge
        self.set()
        

    def set(self,
            lcol=90,
            ocol=91,
            lcolrgb='set rgb 90 100 50 25',
            ocolrgb='set rgb 91 10 20 85',
            bmname='basemap2',
            bmdir='/ptmp',
            xsize=1024,
            ysize=768,
            quiet=0,
            ):

        self.lcol=lcol
        self.lcolrgb=lcolrgb
        self.ocol=ocol
        self.ocolrgb=ocolrgb

        self.gsdir="%s/grads/gslib"%(W2BaseDirApp)

        self.bmname=bmname
        self.bmdir=bmdir
        self.pngpath="%s/bm.%s.png"%(self.bmdir,self.bmname)

        self.xsize=xsize
        self.ysize=ysize
        

    def draw(self):

        if(self.ocolrgb != None):
            self._cmd(self.ocolrgb)
            
        if(self.lcolrgb != None):
            self._cmd(self.lcolrgb)
            
        self._cmd('%s/basemap.2 L %d 1 %s'%(self.gsdir,self.lcol,self.gsdir))
        self._cmd('%s/basemap.2 O %d 1 %s'%(self.gsdir,self.ocol,self.gsdir))
        self._cmd('draw map')


    def putPng(self):
        
        self._ge.makePng(self.pngpath,xsize=self.xsize,ysize=self.ysize)


            
    

class gXbasemap(gXbasemap2):


    def __init__(self,ga,ge):

        self._cmd=ga
        self._ge=ge
        self.set()


    def set(self,
            lcol=90,
            ocol=91,
            lcolrgb='set rgb 90 100 50 25',
            ocolrgb='set rgb 91 10 20 85',
            quiet=0,
            ):
        
        
        self.lcol=lcol
        self.lcolrgb=lcolrgb
        self.ocol=ocol
        self.ocolrgb=ocolrgb

        self.gsdir="%s/grads/gslib"%(W2BaseDirApp)


    def draw(self):

        if(self.ocolrgb != None):
            self._cmd(self.ocolrgb)
            
        if(self.lcolrgb != None):
            self._cmd(self.lcolrgb)
            
        self._cmd('%s/basemap L %d M'%(self.gsdir,self.lcol))
        self._cmd('%s/basemap O %d M'%(self.gsdir,self.ocol))
        self._cmd('draw map')
    

class gXplotTcBt(MFbase):

    btsizmx=0.275
    btsizmn=0.175
    btcols=[2,1,3,4]*20
    
    def __init__(self,ga,ge):

        self._cmd=ga
        self._ge=ge
        

    def set(self,
            bts,dtg0,
            nhbak=72,
            nhfor=0,
            lcol=1,
            lsty=1,
            lthk=5,
            msym=-1,
            mcol=-3,
            msiz=0.0125,
            mthk=5,
            bdtg=None,
            edtg=None,
            ddtg=6,
            ddtgbak=6,
            ddtgfor=12,
            quiet=1,
            ):
        

        ge=self._ge
        self.dtg0=dtg0
        self.nhbak=nhbak
        self.nhfor=nhfor

        # always clip the plots
        #
        ge.getGxinfo()
        self.clipplot="set clip %f %f %f %f"%(ge.plotxl,ge.plotxr,ge.plotyb,ge.plotyt)

        dtgs=bts.keys()
        dtgs.sort()

        self.dtgs=dtgs

        self.bdtg=bdtg
        self.edtg=edtg
        self.ddtg=ddtg

        if(self.bdtg != None):
            odtgs=mf.dtgrange(bdtg,edtg,ddtg)
        else:

            dtgfor=mf.dtginc(dtg0,nhfor)
            dtgbak=mf.dtginc(dtg0,-nhbak)
            pdtgsbak=mf.dtgrange(dtgbak,dtg0,ddtgbak)
            pdtgsfor=mf.dtgrange(dtg0,dtgfor,ddtgfor)
            pdtgs=mf.dtgrange(dtgbak,dtgfor,ddtg)
            
        self.platlons={}
        self.pvmax={}

        self.xys={}
        self.lineprop={}
        self.markprop={}

        odtgs=[]
        odtgsbak=[]
        odtgsfor=[]
        
        n=0
        for dtg in dtgs:

            if(not(dtg in pdtgs)):
                continue
            else:
                odtgs.append(dtg)
                if(dtg in pdtgsbak): odtgsbak.append(dtg)
                if(dtg in pdtgsfor): odtgsfor.append(dtg)
                
            plat=bts[dtg][0]
            plon=bts[dtg][1]
            btvmax=bts[dtg][2]
            
            self.platlons[dtg]=(plat,plon)
            self.pvmax[dtg]=btvmax

            self._cmd('q w2xy %f %f'%(plon,plat))
            x=float(self._cmd.rw(1,3))
            y=float(self._cmd.rw(1,6))
            self.xys[dtg]=([x,y])
            self.lineprop[dtg]=(lcol,lsty,lthk)


            if(msym < 0):
                btsiz=self.btsizmx*(btvmax/135)
                if(btsiz<self.btsizmn): btsiz=self.btsizmn
                
                mcolTD=15
                if(mcol < 0):
                    mcolTS=mcol*(-1)
                    mcolTY=2
                else:
                    mcolTS=mcol
                    mcolTY=mcol
                    
                btsym=41
                btthk=mthk
                
                btcol=mcolTY
                if(btvmax < 65):  btsym=40 ; btcol=mcolTS
                if(btvmax < 25):  btsym=1 ; btcol=mcolTD

                if(mcol < 0):
                    btcol=self.btcols[n]

            else:
                btsiz=msiz
                btsym=msym
                btcol=mcol
                btthk=mthk

            self.markprop[dtg]=(btsym,btsiz,btcol,btthk)
            n=n+1
                
        self.odtgs=odtgs
        self.otimesbak=odtgsbak
        self.otimesfor=odtgsfor
        self.otimes=odtgs





    def dline(self,times=None,
              lcol=None,
              lsty=None,
              lthk=None,
              ):

        if(times == None): times=self.otimes
        
        self._cmd(self.clipplot)

        if(len(times) < 2): return
        
        for n in range(1,len(times)):

            try:
                (x0,y0)=self.xys[times[n-1]]
            except:
                continue

            try:
                (x1,y1)=self.xys[times[n]]
            except:
                continue
            
            if(x0 == None or x1 == None): continue 

            (olcol,olsty,olthk)=self.lineprop[times[n]]
            
            # overrides
            #
            if(lcol != None): olcol=lcol
            if(lsty != None): olsty=lsty
            if(lthk != None): olthk=lthk
            
            self._cmd("set line %d %d %d"%(olcol,olsty,olthk))
            self._cmd("draw line %6.3f %6.3f %6.3f %6.3f"%(x0,y0,x1,y1))

        
    def dwxsym(self,times=None,
               wxsym=None,
               wxsiz=None,
               wxcol=None,
               wxthk=None,
               ):

        if(times == None): times=self.otimes

        self._cmd(self.clipplot)
        for n in range(0,len(times)):

            try:
                (x0,y0)=self.xys[times[n]]
                if(x0 == None): continue
            except:
                continue

            (owxsym,owxsiz,owxcol,owxthk)=self.markprop[times[n]]
            
            if(wxsym != None): owxsym=wxsym
            if(wxsiz != None): owxsiz=wxsiz
            if(wxcol != None): owxcol=wxcol
            if(wxthk != None): owxthk=wxthk
            
            cmd="draw wxsym %d %6.3f %6.3f %6.3f %d %d"%(owxsym,x0,y0,owxsiz,owxcol,owxthk)
            self._cmd(cmd)

            self.wxcol=wxcol

    def dmark(self,times=None,
              mksym=None,
              mksiz=None,
              mkcol=None,
              mkthk=None,
              ):

        if(times == None): times=self.otimes

        self._cmd(self.clipplot)
        for n in range(0,len(times)):

            try:
                (x0,y0)=self.xys[times[n]]
                if(x0 == None):  continue
            except:
                continue
            
            (omksym,omksiz,omkcol,omkthk)=self.markprop[times[n]]
            
            # overrides
            if(mksym != None): omksym=mksym
            if(mksiz != None): omksiz=mksiz
            if(mkcol != None): omkcol=mkcol
            if(mkthk != None): omkthk=mkthk
            
            cmd="set line %d 1 %d"%(omkcol,omkthk)
            self._cmd(cmd)
            cmd="draw mark %d %6.3f %6.3f %6.3f %d %d"%(omksym,x0,y0,omksiz,omkcol,omkthk)
            self._cmd(cmd)

            self.mksiz=omksiz
            self.mkcol=omkcol
            self.mkthk=omkthk

        
    def dlabel(self,times=None,
               lbsiz=0.10,
               lbcol=1,
               lbthk=5,
               yoffset=0.10,
               location='c',
               dlab=None,
               ):

        if(times == None): times=self.otimes

        self._cmd(self.clipplot)
        for n in range(0,len(times)):

            try:
                (x0,y0)=self.xys[times[n]]
                y0=y0-lbsiz*0.5-yoffset
                if(dlab == None):
                    label="%3d"%(self.pvmax[times[n]])
                else:
                    label=dlab
                if(x0 == None):  continue
            except:
                continue

            self._cmd('set string %d %s %d -30'%(lbcol,location,lbthk))
            self._cmd("set strsiz %f"%(lbsiz))
            self._cmd("draw string %f %f %s"%(x0,y0,label))


    def legend(self,ge,
               times=None,
               btcol=None,
               bttitle=None,
               btlgdcol=None,
               ystart=None,
               ):

        if(times == None): times=self.otimes

        ge=self._ge
        ge.getGxinfo()
        self._cmd("set clip 0 %6.3f 0 %6.3f"%(ge.pagex,ge.pagey))

        ssiz=0.60
        lscl=0.85
        xoffset=0.1
        x=ge.plotxr+(0.10)*(1.5/lscl)+xoffset
        xs=x+(0.15)*lscl

        if(not(hasattr(self,'finaly')) and ystart != None):
            y=ystart
        else:
            y=self.finaly
            
        dy=0.165*lscl
        yss=dy*ssiz*lscl
        sthk=6

        if(btlgdcol == None): btlgdcol=1
        
        for n in range(0,len(times)):
            if(n == 0 and bttitle != None):
                self._cmd('set string %s l %d'%(btlgdcol,sthk))
                self._cmd("set strsiz %f"%(yss))
                self._cmd("draw string %f %f %s"%(xs,y,bttitle))
                y=y-dy
                
                
            time=times[n]
            try:
                (obtsym,obtsiz,obtcol,obtthk)=self.markprop[time]
            except:
                continue
            
            if(btcol != None): obtcol=btcol
            cmd="draw wxsym %d %6.3f %6.3f %6.3f %d %d"%(obtsym,x,y,obtsiz,obtcol,obtthk)
            self._cmd(cmd)
            self._cmd('set string 1 l %d'%(sthk))
            self._cmd("set strsiz %f"%(yss))
            lgd="- %s %3d"%(time[4:10],self.pvmax[time])
            lgd="%s %3d"%(time[4:10],self.pvmax[time])
            self._cmd("draw string %f %f %s"%(xs,y,lgd))
            y=y-dy

        self.finaly=y
        self.dy=dy
            


class gXplotTcFt(gXplotTcBt):
    

    def set(self,
            fts,lcol=-1,lsty=1,lthk=7,
            msym=3,mcol=3,msiz=0.05,mthk=5,
            dovmaxflg=1,
            doland=0,
            verb=0,
            quiet=0,
            ):

        self.dovmaxflg=dovmaxflg
        self.doland=doland

        self.initLF()
        self.initVars(lcol,lsty,lthk,msym,mcol,msiz,mthk,verb)
        self.setPcutcols()
        self.initProps(fts)
        self.setLineProps()
        self.setMarkProps()


    def initLF(self):
        
        from w2 import SetLandFrac
        from w2 import GetLandFrac

        self.lf=SetLandFrac()
        self.GetLandFrac=GetLandFrac

        

    def getLF(self,lat,lon):
        landfrac=self.GetLandFrac(self.lf,lat,lon)
        return(landfrac)


    # init and set methods
    #
    def initVars(self,lcol,lsty,lthk,msym,mcol,msiz,mthk,verb):
        self.lcol=lcol
        self.lsty=lsty
        self.lthk=lthk
        self.msym=msym
        self.mcol=mcol
        self.msiz=msiz
        self.mthk=mthk
        self.verb=verb

        
    def initProps(self,fts):

        ge=self._ge
        # always clip the plots
        #
        ge.getGxinfo()
        self.clipplot="set clip %f %f %f %f"%(ge.plotxl,ge.plotxr,ge.plotyb,ge.plotyt)

        taus=fts.keys()
        taus.sort()

        self.taus=taus

        self.platlons={}
        self.pvmax={}
        self.ppmin={}
        self.pdvmax={}
        self.pvmaxflg={}

        self.xys={}
        self.lineprop={}
        self.markprop={}

        otaus=[]
        
        n=0
        for tau in taus:

            plat=fts[tau][0]
            plon=fts[tau][1]

            if(plon == None): continue

            landfrac=self.getLF(plat,plon)
            if(self.doland == 0 and landfrac > 0.5): continue

            otaus.append(tau)
            
            try:    vmax=fts[tau][2]
            except: vmax=None
            
            try:    pmin=fts[tau][3]
            except: pmin=None
            
            try:    dvmax=fts[tau][4]
            except: dvmax=None
            
            try:     vmaxflg=fts[tau][5]
            except:  vmaxflg=0

            if(not(self.dovmaxflg)): vmaxflg=0

            if(self.verb): print 'eeeeeeeeeeeeeeeeeee',tau,plat,plon,vmax,pmin,dvmax,vmaxflg
            
            self.platlons[tau]=(plat,plon)
            self.pvmax[tau]=vmax
            self.ppmin[tau]=pmin
            self.pdvmax[tau]=dvmax
            self.pvmaxflg[tau]=vmaxflg

            self._cmd('q w2xy %f %f'%(plon,plat))
            self.xys[tau]=([float(self._cmd.rw(1,3)),float(self._cmd.rw(1,6))])

            n=n+1

        self.taus=otaus
        self.otimes=otaus


    def setMarkProps(self):
        
        for tau in self.taus:
            ftsiz=self.msiz
            ftsym=self.msym
            ftcol=self.mcol
            ftthk=self.mthk

            self.markprop[tau]=(ftsym,ftsiz,ftcol,ftthk)


    def setLineProps(self):

        for tau in self.taus:
            try:
                dvmax=self.pdvmax[tau]
                vmaxflg=self.pvmaxflg[tau]
                self.setSegCol(tau,dvmax,vmaxflg)
            except:
                continue

        
    def setPcutcols(self):
        
        pcuts=[-25,-20,-15,-10,-5,0,5,  10,  15,   20, 25]
        pcols=[41,43, 45, 47, 49,15,15, 29,  27,  25,  23,  21]
        pcols=[49,47, 45, 43, 41,15,15, 21,  23,  25,  27,  29]

        pcutsvmax=[  25,  35,  50,  65,  75,  85,  95,  105,  120]
        pcolsvmax=[15,  21,  22,  23,  24,  25,  26,  27,   28,  29]

        self.pcuts=pcuts
        self.pcols=pcols
        self._ge.setShades(pcuts,pcols)

    
    def setSegCol(self,tau,dvmax,vmaxflg):

        if(self.lcol == -1 or self.lcol == -2):
            olcoldef=75
            olthkdef=4
            olsty=self.lsty
            if(dvmax != None):
                if(vmaxflg == 1): olcol=self._ge.getShadeCol(dvmax) ; olthk=6
                elif(vmaxflg == 0): olcol=olcoldef ; olthk=olthkdef
                elif(vmaxflg == -1): olcol=self._ge.getShadeCol(dvmax) ; olthk=5
            else:
                olcol=olcoldef
                olthk=olthkdef
        else:
            olcol=self.lcol
            olsty=self.lsty
            olthk=self.lthk

        self.lineprop[tau]=(olcol,olsty,olthk)


    def cbarn(self,sf=1.0,vert=1,side=None):

        self._cmd("set clip 0 %6.3f 0 %6.3f"%(self._ge.pagex,self._ge.pagey))
        cb=cbarn(self._ga,self._ge,vert=vert,side=side,sf=sf)


    
class gXplotTcFtVmax(gXplotTcFt):


    def set(self,
            fts,lcol=-1,lsty=1,lthk=7,
            msym=3,mcol=3,msiz=0.05,mthk=5,
            dovmaxflg=1,
            doland=0,
            verb=0,
            quiet=0,
            ):
        
        self.dovmaxflg=dovmaxflg
        self.doland=doland

        self.initLF()
        self.initVars(lcol,lsty,lthk,msym,mcol,msiz,mthk,verb)
        self.setPcutcols()
        self.initProps(fts)
        self.setLineProps()
        self.setMarkProps()


    def setLineProps(self):

        for tau in self.taus:
            vmax=self.pvmax[tau]
            self.setSegCol(tau,vmax)

    def setPcutcols(self):
        
        pcuts=[  25,  35,  50,  65,  90,  120]
        pcols=[15,   7,   4,  3,    2,   14,   2]

        self.pcuts=pcuts
        self.pcols=pcols
        self._ge.setShades(pcuts,pcols)

    
    def setSegCol(self,tau,vmax):

        if(vmax != None and self.lcol == -1):
            if(vmax >= 65.0): olcol=self._ge.getShadeCol(vmax) ; olthk=6
            else: olcol=self._ge.getShadeCol(vmax) ; olthk=5
            olsty=self.lsty
        else:
            olcol=self.lcol
            olsty=self.lsty
            olthk=self.lthk
            
        self.lineprop[tau]=(olcol,olsty,olthk)

    
class gXpolyCircle(MFbase):

    def __init__(self,ga,ge,cmd):

        self._ga=ga
        self._cmd=cmd
        self._ge=ge


    def set(self,clat,clon,radii,
            dtheta=10,
            dodisplay=0,
            ):
        
        from TCw2 import rumltlg

        self.clat=clat
        self.clon=clon

        self.platlons=[]
        dtau=12.0
        spdc=radii/dtau
        

        for theta in range(0,360+1,dtheta):
            (plat,plon)=rumltlg(theta,spdc,dtau,clat,clon)
            self.platlons.append([plat,plon])

        if(dodisplay):
            self._cmd('set cmax -1000')
            self._cmd('d lat')

        self.xys=[]
        for (plat,plon) in self.platlons:

            self._cmd('q w2xy %f %f'%(plon,plat))
            self.xys.append([float(self._ga.rword(1,3)),float(self._ga.rword(1,6))])



    def fill(self,lcol=1):

        self._cmd("set line %d"%(lcol))
        pcmd='draw polyf '

        for (x,y) in self.xys:
            pcmd=pcmd+"%6.3f %6.3f"%(x,y)

        print pcmd
        self._cmd(pcmd)

        
    def border(self,lcol=1,lsty=1,lthk=5):

        self._cmd("set line %d %d %d"%(lcol,lsty,lthk))
        
        for n in range(1,len(self.xys)):
            (x0,y0)=self.xys[n-1]
            (x1,y1)=self.xys[n]
            
            cmd="draw line %6.3f %6.3f %6.3f %6.3f"%(x0,y0,x1,y1)
            self._cmd(cmd)


class gXcbarn(MFbase):


    def __init__(self,cmd,ge):

        self._cmd=cmd
        self._ge=ge


    def draw(self,
                 sf=1.0,
                 vert=-1,
                 side=None,
                 xmid=None,
                 ymid=None,
                 sfstr=1.0,
                 pcuts=None,
                 pcols=None,
                 quiet=0,
                 ):

        ge=self._ge
        
        ge.getGxinfo()

        if(pcuts != None and pcols != None):
            ge.setShades(pcuts,pcols)

        # -- check if ge has colbar
        #
        elif(not(hasattr(ge,'colbar'))):
            ge.getShades()


        xsiz= ge.pagex
        ysiz= ge.pagey
        ylo=  ge.plotyb
        yhi=  ge.plotyt
        xhi=  ge.plotxr
        xlo=  ge.plotxl
        xd= xsiz-xhi

        ylolim=0.6*sf
        xdlim1=1.0*sf
        xdlim2=1.5*sf  
        barsf=0.8*sf
        yoffset=0.3*sf
        stroff=0.05*sf
        strxsiz=0.12*sf*sfstr
        strysiz=0.13*sf*sfstr

        if(ylo < ylolim and xd < xdlim1):
            print "Not enough room in plot for a colorbar"
            return
        
        #
        #  Decide if horizontal or vertical color bar
        #  and set up constants.
        #
        cnum=ge.nshades
        #
        #	logic for setting the bar orientation with user overides
        #
        if(ylo<ylolim or xd>xdlim1):
            vchk=1
        else:
            vchk=0

        if(vert >= 0): vchk=vert

        if(vchk == 1):
            
            #
            #	vertical bar
            #
            if(xmid == None): xmid=xhi+xd/2
            if(side == 'left'):
                xmid=0.0+xlo*0.35
            
            xwid=0.2*sf
            ywid=0.5*sf
            xl=xmid-xwid/2
            xr=xl+xwid

            if(ywid*cnum > ysiz*barsf): 
                ywid=ysiz*barsf/cnum
                
            if(ymid == None): ymid=ysiz/2
            yb=ymid-ywid*cnum/2
            self._cmd('set string 1 l 5 0')
            vert=1
            
        else:
            
            #
            #	horizontal bar
            #
            
            ywid=0.2*sf
            xwid=0.6*sf

            if(ymid == None): ymid=ylo/2-ywid/2
            yt=ymid+yoffset
            yb=ymid
            if(xmid == None): xmid=xsiz/2
            if(xwid*cnum > xsiz*barsf):
                xwid=xsiz*barsf/cnum
            xl=xmid-xwid*cnum/2
            self._cmd('set string 1 tc 5 0')
            vert=0

        #
        #  Plot colorbar
        #


        self._cmd("set strsiz %f %f"%(strxsiz,strysiz))

        num=0
        while (num<cnum):

            (col,minval,maxval)=ge.colbar[num]
            hi="%g"%(maxval)

            if(vert): 
                yt=yb+ywid
            else :
                xr=xl+xwid
                yt=yb+ywid

            if(num != 0 and  num != cnum-1):
                self._cmd('set line %d'%(col))
                self._cmd('draw recf %f %f %f %f'%(xl,yb,xr,yt))

                self._cmd('set line 1 1 5')
                self._cmd('draw rec %f %f %f %f'%(xl,yb,xr,yt))
                
            if(num < cnum-1):
                if(vert): 
                    xp=xr+stroff
                    self._cmd('draw string %f %f %s'%(xp,yt,hi))
                else:
                    yp=yb-stroff
                    self._cmd('draw string %f %f %s'%(xr,yp,hi))


            if(num == 0):

                if(vert):
                    xm=(xl+xr)*0.5

                    self._cmd('set line %d'%(col))
                    self._cmd('draw polyf %f %f %f %f %f %f %f %f'%(xl,yt,xm,yb,xr,yt,xl,yt))
                    
                    self._cmd('set line 1 1 5')
                    self._cmd('draw line %f %f %f %f'%(xl,yt,xm,yb))
                    self._cmd('draw line %f %f %f %f'%(xm,yb,xr,yt))
                    self._cmd('draw line %f %f %f %f'%(xr,yt,xl,yt))

                else:

                    ym=(yb+yt)*0.5
                    self._cmd('set line %d'%(col))
                    self._cmd('draw polyf %f %f %f %f %f %f %f %f'%(xl,ym,xr,yb,xr,yt,xl,ym))
                    
                    self._cmd('set line 1 1 5')
                    self._cmd('draw line %f %f %f %f'%(xl,ym,xr,yb))
                    self._cmd('draw line %f %f %f %f'%(xr,yb,xr,yt))
                    self._cmd('draw line %f %f %f %f'%(xr,yt,xl,ym))

            if(num < cnum-1):
                if(vert):
                    xp=xr+stroff 
                    self._cmd('draw string %f %f %s'%(xp,yt,hi))
                else:
                    yp=yb-stroff
                    self._cmd('draw string %f %f %s'%(xr,yp,hi))

            if(num == cnum-1 ):

                if( vert):

                    self._cmd('set line %d'%(col))
                    self._cmd('draw polyf %f %f %f %f %f %f %f %f'%(xl,yb,xm,yt,xr,yb,xl,yb))

                    self._cmd('set line 1 1 5')
                    self._cmd('draw line %f %f %f %f'%(xl,yb,xm,yt))
                    self._cmd('draw line %f %f %f %f'%(xm,yt,xr,yb))
                    self._cmd('draw line %f %f %f %f'%(xr,yb,xl,yb))

                else:

                    self._cmd('set line %d'%(col))
                    self._cmd('draw polyf %f %f %f %f %f %f %f %f'%(xr,ym,xl,yb,xl,yt,xr,ym))
                    
                    self._cmd('set line 1 1 5')
                    self._cmd('draw line %f %f %f %f'%(xr,ym,xl,yb))
                    self._cmd('draw line %f %f %f %f'%(xl,yb,xl,yt))
                    self._cmd('draw line %f %f %f %f'%(xl,yt,xr,ym))

            
            if(num<cnum-1):
                if(vert): 
                    xp=xr+stroff
                    self._cmd('draw string %f %f %s'%(xp,yt,hi))
                else:
                    yp=yb-stroff
                    self._cmd('draw string %f %f %s'%(xr,yp,hi))

            num=num+1
            if(vert):
                yb=yt
            else:
                xl=xr
        
            

class gXtitle(MFbase):


    def __init__(self,ga,ge):

        self._cmd=ga
        self._ge=ge
        self.set()


    def set(self,
            scale=1.0,
            t1col=1,
            t2col=1):
        
        self.scale=scale
        self.t1col=t1col
        self.t2col=t2col
        
    def clip(self):

        self._ge.getGxinfo()
        self._cmd("set clip 0 %6.3f 0 %6.3f"%(self._ge.pagex,self._ge.pagey))
        

    def top(self,t1,t2=None,doclip=1):

        if(doclip): self.clip()
        #
        # if scale < 0.0 then make size of t2 = t1
        #
        if(self.scale < 0.0):
            scale=scale*-1.0
            t2scale=1.05
        else:
            t2scale=0.80
            
        xr=self._ge.pagex
        xl=0
        y1=self._ge.pagey-0.15
        xs=(xr-xl)*0.5
        tsiz=0.15
        
        tsiz=tsiz*self.scale
        t2siz=tsiz*t2scale
        y2=self._ge.pagey-0.15-tsiz*1.5

        self._cmd('set strsiz %f'%(tsiz))
        self._cmd('set string %d c 6 0'%(self.t1col))
        self._cmd('draw string %f %f %s'%(xs,y1,t1))

        if(t2 != None):
            self._cmd('set string %d c 8 0'%(self.t2col))
            self._cmd('set strsiz %f'%(t2siz))
            self._cmd('draw string %f %f `0%s`0'%(xs,y2,t2))

        


    def bottom(self,t1,t2=None,sopt=None,doclip=1):

        if(doclip): self.clip()
        
        #
        # if scale < 0.0 then make size of t2 = t1
        #
        if(self.scale < 0.0):
            scale=scale*-1.0
            t2scale=1.05
        else:
            t2scale=0.80
            
        xr=self._ge.pagex
        xl=0
        y1=0.22
        y2=0.08
        
        if(sopt == 'left'):
            xs=0.2
        elif(sopt == 'right'):
            xs=0.2
            xs=xr-xs
        else:
            xs=xl+(xr-xl)*0.5

        tsiz=0.09
        
        tsiz=tsiz*self.scale
        t2siz=tsiz*t2scale

        self._cmd('set strsiz %f'%(tsiz))
        if(sopt == 'left'):
            self._cmd('set string %d l 6 0'%(self.t1col))
        elif(sopt == 'right'):
            self._cmd('set string %d r 6 0'%(self.t1col))
        else:
            self._cmd('set string %d c 6 0'%(self.t1col))
        self._cmd('draw string %f %f %s'%(xs,y1,t1))

        if(t2 != None):
            self._cmd('set strsiz %f'%(t2siz))
            if(sopt == 'left'):
                self._cmd('set string %d l 8 0'%(self.t2col))
            elif(sopt == 'right'):
                self._cmd('set string %d r 8 0'%(self.t2col))
            else:
                self._cmd('set string %d c 8 0'%(self.t2col))

            self._cmd('draw string %f %f `0%s`0'%(xs,y2,t2))



class GradsPlot(MFbase):


    def __init__(self,ga,ge):

        self.basemap=gXbasemap(ga,ge)
        self.basemap2=gXbasemap2(ga,ge)
        
        self.title=gXtitle(ga,ge)
        self.plotTcBt=gXplotTcBt(ga,ge)
        self.plotTcFt=gXplotTcFt(ga,ge)
        self.plotTcFtVmax=gXplotTcFtVmax(ga,ge)
        self.polyCircle=gXpolyCircle(ga,ge,ga)
        self.cbarn=gXcbarn(ga,ge)

    

class gxStats(MFbase):


## Data Type = grid
## Dimensions = 0 1
## I Dimension = 1 to 145 Linear 0 2.5
## J Dimension = 1 to 73 Linear -90 2.5
## Sizes = 145 73 10585
## Undef value = -9.99e+08
## Undef count = 73  Valid count = 10512
## Min, Max = 95301 103798
## Cmin, cmax, cint = 96000 103000 1000
## Stats[sum,sumsqr,root(sumsqr),n]:     1.06001e+09 1.06908e+14 1.03396e+07 10512
## Stats[(sum,sumsqr,root(sumsqr))/n]:     100838 1.01701e+10 100847
## Stats[(sum,sumsqr,root(sumsqr))/(n-1)]: 100847 1.01711e+10 100852
## Stats[(sigma,var)(n)]:     1361.58 1.85389e+06
## Stats[(sigma,var)(n-1)]:   1361.64 1.85407e+06
## Contouring: 96000 to 103000 interval 1000 



    def __init__(self,cards):

        for card in cards:

            if(mf.find(card,'Sizes')):
                tt=card.split()
                self.ni=int(tt[2])
                self.nj=int(tt[3])

            if(mf.find(card,'ndef value')):
                tt=card.split()
                self.undef=float(tt[3])

            if(mf.find(card,'ndef count')):
                tt=card.split()
                self.nundef=int(tt[3])
                self.nvalid=int(tt[7])


## Stats[(sigma,var)(n-1)]:   1361.64 1.85407e+06
            if(mf.find(card,'Stats[(sigma,var)(n)]:')):
                tt=card.split()
                self.sigma=float(tt[1])

## Min, Max = 95301 103798
            if(mf.find(card,'Min, ')):
                tt=card.split()
                self.min=float(tt[3])
                self.max=float(tt[4])
## Stats[sum,sumsqr,root(sumsqr),n]:     1.06001e+09 1.06908e+14 1.03396e+07 10512
            if(mf.find(card,',root(sumsqr),n]:')):
                tt=card.split()
                self.sum=float(tt[1])
                self.sumsqr=float(tt[2])
                self.rootsumsqr=float(tt[3])
                self.nsum=int(tt[4])


class gxGxout(MFbase):

    def __init__(self,g1s,g1v,g2s,g2v,stn):
        self.g1s=g1s
        self.g1v=g1v
        self.g2s=g2s
        self.g2v=g2v
        self.stn=stn



class GradsEnv(MFbase):


    def __init__(self,
                 lat1=-90.0,
                 lat2=90.0,
                 lon1=0.0,
                 lon2=360.0,
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
                 ):


        self.lat1=lat1
        self.lat2=lat2
        self.lon1=lon1
        self.lon2=lon2
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



    def makePng(self,
                opath,
                bmpath=None,
                bmcol=0,
                xsize=1024,
                ysize=768,
                background='black',
                ropt='',
                verb=0,
                ):

        if(self.pngmethod == 'printim'):
            if(bmpath == None):
                cmd="%s %s x%d y%d"%(self.pngmethod,opath,xsize,ysize)
            else:
                cmd="%s %s -b %s -t %d x%d y%d"%(self.pngmethod,opath,bmpath,bmcol,xsize,ysize)

        elif(self.pngmethod == 'gxyat'):
            bkopt=''
            if(background == 'black'):
                bkopt='-r'
            cmd="%s -x %d -y %d %s %s"%(self.pngmethod,xsize,ysize,bkopt,opath)

        if(verb):
            print "makePng: %s"%(opath)
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
        

    def getLevs(self,verb=0):

        if(not(hasattr(self,'fh'))):
            print """WWW in GradsEnv...need a 'fh' var to get levs..."""
        else:
            nz=self.fh.nz
            self.dimLevs=list(self._ga.coords().lev)
            self.dimNlevs=len(self.dimLevs)
            self._cmd("set z 1 %d"%(nz))
            self.Levs=list(self._ga.coords().lev)
            if(verb): print 'getLevs: nz: ',nz,'levs: ',self.Levs
            self._cmd("set z 1")
            

    def getFileMeta(self,obj=None):

        if(not(hasattr(self,'fh'))):
            print """WWW in GradsEnv...need a 'fh' var to get filemeta data..."""
        else:
            if(obj == None): obj=self
            obj.nx=self.fh.nx
            obj.ny=self.fh.ny
            obj.nz=self.fh.nz
            obj.nt=self.fh.nt

            obj.dimlevs=list(self._ga.coords().lev)
            obj.dimNlevs=len(obj.dimlevs)
            obj.lats=list(self._ga.coords().lat)
            obj.lons=list(self._ga.coords().lon)

            if(len(obj.lats) > 1):
                obj.dlat=obj.lats[1]-obj.lats[0]
            else:
                obj.dlon=0.0

            if(len(obj.lons) > 1):
                obj.dlon=obj.lons[1]-obj.lons[0]
            else:
                obj.dlon=0.0

            self._cmd("set z 1 %d"%(obj.nz))
            obj.levs=list(self._ga.coords().lev)
            obj.vars=list(self.fh.vars)
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

        if(not(hasattr(self,'lev2'))):
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
        

class W2GaBase():
    
    def getGxout(self):

        self('q gxout')
        g1s=self.rword(2,6)
        g1v=self.rword(3,6)
        g2s=self.rword(4,6)
        g2v=self.rword(5,6)
        stn=self.rword(6,4)
        gxout=gxGxout(g1s,g1v,g2s,g2v,stn)
        return(gxout)


    def getExprStats(self,expr):

        # get the current graphics and rank of display grid
        rank=len(self.coords().shape)
        cgxout=self.getGxout()

        # set gxout to stats; display expression
        self('set gxout stat')
        self('d %s'%(expr))
        cards=self.Lines

        # reset the original gxout
        if(rank == 1): self('set gxout %s'%(cgxout.g1s))
        if(rank == 2): self('set gxout %s'%(cgxout.g2s))
        exprstats=gxStats(cards)
        return(exprstats)


    def resetCurgxout(self,cgxout):

        rank=len(self.coords().shape)
        #reset the original gxout
        if(rank == 1): self('set gxout %s'%(cgxout.g1s))
        if(rank == 2): self('set gxout %s'%(cgxout.g2s))





class W2GaCore(GaCore,W2GaBase,GrADSError,MFbase):


    Quiet=1

    def __init__ (self, 
                  Bin='grads2', Echo=True, Opts='', Port=False, 
                  Strict=False, Quiet=0, RcCheck=None, Verb=0, Window=None,
                  doLogger=0):

        # --- standard gacore init
        #
        self.Bin=Bin
        self.Echo=Echo
        self.Opts=Opts
        self.Port=Port
        self.Strict=False
        self.Quiet=Quiet
        self.RcCheck=RcCheck
        self.Verb=Verb
        self.Window=Window
        self.doLogger=doLogger
        
        self.initGaCore()

        self.GrADSError=GrADSError

        self._cmd=self.__call__
        self.rl=self.rline
        self.rw=self.rword
        
        # -- instantiate a GradsEnv object, ge
        #
        self.ge=GradsEnv()
        self.ge._cmd=self.__call__

        self.ge._ga=self
        self.ge.rl=self.rline
        self.ge.rw=self.rword
        
        self.gp=GradsPlot(self,self.ge)







class W2GaNum(GaCore,W2GaBase,GrADSError,MFbase):


    Quiet=1

    def __init__ (self, 
                  Bin='grads', Echo=True, Opts='', Port=False, 
                  Strict=False, Quiet=0, RcCheck=None, Verb=0, Window=None,
                  doLogger=0):

        # --- standard gacore init
        #
        self.Bin=Bin
        self.Echo=Echo
        self.Opts=Opts
        self.Port=Port
        self.Strict=False
        self.Quiet=Quiet
        self.RcCheck=RcCheck
        self.Verb=Verb
        self.Window=Window
        self.doLogger=doLogger
        
        self.initGaCore()
        
        # -- instantiate a GradsEnv object, ge
        #
        self.ge=GradsEnv()
        self.ge._cmd=self.__call__
        
        self.gp=GradsPlot()
        
        self.gp.ge=self.ge
        self.gp.cmd=self.__call__
        self.gp._ge=self.ge
        self.gp._cmd=self.__call__

        self.GrADSError=GrADSError


def setGA(gaclass='gacore',Opts='',Bin='grads2',Quiet=1,Window=0,
          doLogger=0):


    if(gaclass == 'gacore'):
        from G2 import W2GaCore
        ga=W2GaCore(Opts=Opts,Bin=Bin,Quiet=Quiet,Window=Window,doLogger=doLogger)
    elif(gaclass == 'ganum'):
        from G2 import W2GaNum
        ga=W2GaNum(Opts=Opts,Bin=Bin,Quiet=Quiet,Window=Window,doLogger=doLogger)
        

    return(ga)

