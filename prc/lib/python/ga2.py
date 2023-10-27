from WxMAP2 import *
w2=W2()

W2BaseDirApp=w2.W2BaseDirApp
W2BaseDirPrc=w2.W2BaseDirPrc
ptmpBaseDir=w2.ptmpBaseDir

#MF.sTimer(tag='load grads')
#from grads import GaCore,GrADSError
#MF.dTimer(tag='load grads')

#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# classes
#

class gXbasemap2(MFbase):


    from mfbase import ptmpBaseDir
    
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
            bmdir=ptmpBaseDir,
            xsize=None,
            ysize=None,
            quiet=0,
            landcol=None,
            oceancol=None,
            ):

        if(xsize == None and hasattr(self._ge,'xsize')): xsize=self._ge.xsize
        if(ysize == None and hasattr(self._ge,'ysize')): ysize=self._ge.ysize

        wC=w2Colors()

        if(landcol != None):
            hex=wC.W2Colors[landcol]
            (r,g,b)=wC.hex2rgb(hex)
            lcolrgb='set rgb %d %d %d %d'%(lcol,r,g,b)
            
        if(oceancol != None):
            hex=wC.W2Colors[oceancol]
            (r,g,b)=wC.hex2rgb(hex)
            ocolrgb='set rgb %d %d %d %d'%(ocol,r,g,b)

        self.lcol=lcol
        self.lcolrgb=lcolrgb
        self.ocol=ocol
        self.ocolrgb=ocolrgb

        self.gsdir="%s/grads/gslib"%(W2BaseDirApp)

        self.bmname=bmname
        self.bmdir=bmdir
        
        # -- for grads -- must be lower case...
        #
        obmdir=self.bmdir
        obmdirl=obmdir.lower()
        if(obmdir != obmdirl): obmdirl='/tmp'
        
        self.pngpath="%s/bm.%s.png"%(obmdirl,self.bmname)
        self.pngpath=self.pngpath.lower()

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
        
        obmdir=self.bmdir
        obmdirl=obmdir.lower()
        if(obmdir != obmdirl):
            npngpath=self.pngpath.replace('/tmp',self.bmdir)
            opngpath=self.pngpath
            self.pngpath=npngpath
            cmd="mv -f -v %s %s"%(opngpath,self.pngpath)
            mf.runcmd(cmd)


            
    

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
    btsizmx=0.150
    btsizmn=0.125
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
            ddtgbak=12,
            ddtgfor=12,
            quiet=1,
            dtg0012=0,
            maxbt=50,
            mcolTD=15,
            dttimeDefault=6,
            doland=1,
            maxlandFrac=0.80,
            btMinLand=35.0,
            ):
        
        from tcbase import IsTc
                    
        self.initLF()
        
        ge=self._ge
        self.dtg0=dtg0
        self.nhbak=nhbak
        self.nhfor=nhfor

        self.doland=doland
        self.maxlandFrac=maxlandFrac

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
            pdtgs=mf.dtgrange(bdtg,edtg,ddtg)
            
            if(len(pdtgs) > maxbt):
                ddtg=12
                self.ddtg=ddtg
                if(dtg0012):
                    bdtg=mf.dtgShift0012(bdtg,round=1)
                    edtg=mf.dtgShift0012(edtg,round=0)
                pdtgs=mf.dtgrange(bdtg,edtg,ddtg)


        else:
            # -- handle ddtg = 12 and dtg0 != None
            #
            if(nhfor == None):
                dtgfor=dtgs[-1]
                if(dtg0 != None and ddtg == 12):
                    if(w2.is0012Z(dtg0) and not(w2.is0012Z(dtgfor))):
                        dtgfor=dtgs[-2]
                    elif(w2.is0618Z(dtg0) and not(w2.is0618Z(dtgfor))):
                        dtgfor=dtgs[-2]
            else:
                if(dtg0 != None): dtgfor=mf.dtginc(dtg0,nhfor)

            if(dtg0012): dtgfor=mf.dtgShift0012(dtgfor,round=0)
                
            # -- handle ddtg = 12 and dtg0 != None
            #
            if(nhbak == None):
                dtgbak=dtgs[0]
                if(dtg0 != None and ddtg == 12):
                    if(w2.is0012Z(dtg0) and not(w2.is0012Z(dtgbak))):
                        dtgbak=dtgs[1]
                    elif(w2.is0618Z(dtg0) and not(w2.is0618Z(dtgbak))):
                        dtgbak=dtgs[1]
                
            else:
                if(dtg0 != None): dtgbak=mf.dtginc(dtg0,-nhbak)

            if(dtg0012): dtgbak=mf.dtgShift0012(dtgbak,round=1)
                

            if(dtg0 != None):
                pdtgsbak=mf.dtgrange(dtgbak,dtg0,ddtgbak)
                pdtgsfor=mf.dtgrange(dtg0,dtgfor,ddtgfor)
            else:
                pdtgsbak=[]
                pdtgsfor=[]
                
            pdtgs=mf.dtgrange(dtgbak,dtgfor,ddtg)

            if(len(pdtgs) > maxbt):
                ddtg=12
                self.ddtg=ddtg
                if(dtg0012):
                    dtgbak=mf.dtgShift0012(dtgbak,round=1)
                    dtgfor=mf.dtgShift0012(dtgfor,round=0)
                pdtgs=mf.dtgrange(dtgbak,dtgfor,ddtg)


        self.platlons={}
        self.pvmax={}
        self.pvmaxflg={}

        self.xys={}
        self.lineprop={}
        self.markprop={}

        odtgs=[]
        odtgsbak=[]
        odtgsfor=[]
        
        pdt=pdtgs.sort()
        n=0
        for dtg in dtgs:
            
            if(not(dtg in pdtgs)):  continue
            
            # -- get lat/lon and check if overland
            #
            plat=bts[dtg][0]
            plon=bts[dtg][1]
            btvmax=bts[dtg][2]
            
            landfrac=self.getLF(plat,plon)
            
            #print 'BBBB ',dtg,plat,plon,landfrac,btvmax
            # -- chuck point if overland and btvmax <= 35 kt (strong tcs overland)
            #
            if(self.doland == 0 and landfrac > self.maxlandFrac and btvmax <= btMinLand): continue            

            odtgs.append(dtg)
            if(dtg in pdtgsbak): odtgsbak.append(dtg)
            if(dtg in pdtgsfor): odtgsfor.append(dtg)
            
            if(len(bts[dtg]) == 8):
                tccode=bts[dtg][-2].lower()
                wncode=bts[dtg][-1].lower()
            else:
                tccode='xx'
                wncode='xx'

            self.platlons[dtg]=(plat,plon)
            self.pvmax[dtg]=btvmax

            self._cmd('q w2xy %f %f'%(plon,plat))
            
            x=float(self._cmd.rw(1,3))
            y=float(self._cmd.rw(1,6))
            self.xys[dtg]=([x,y])

            # -- colorize line seg
            #
            lthk=9
            lcol=0
            lsty=2
            
            if(btvmax >= 100 and IsTc(tccode) == 1):                   lcol=9  ; lsty=2 ; lthk=10
            if(btvmax >= 65  and btvmax < 100 and IsTc(tccode) == 1):  lcol=2  ; lsty=1
            if(btvmax >= 35  and btvmax < 65  and IsTc(tccode) == 1):  lcol=7  ; lsty=1
            if(btvmax <  35  and IsTc(tccode) == 1):                   lcol=3  ; lsty=1
            if(btvmax >= 35  and IsTc(tccode) == 2):                   lcol=8  ; lsty=1
            if(btvmax <  35  and IsTc(tccode) == 2):                   lcol=4  ; lsty=1
            if(IsTc(tccode) == 0):                                     lcol=10 ; lsty=3
            if(tccode == 'ex' or tccode == 'pt'):                      lcol=1  ; lsty=3
            
            self.lineprop[dtg]=(lcol,lsty,lthk)


            if(msym < 0):
                btsiz=self.btsizmx*(btvmax/135)
                if(btsiz<self.btsizmn): btsiz=self.btsizmn
                
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

                if(tccode != None):
                    if(not(IsTc(tccode))):      btsym=1  ; btcol=mcolTD
                    if(tccode.lower() == 'ex'): btsym=24 ; btcol=mcolTD
                    

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

        if(dtg0 == None):
            self.otimesbak=odtgs
            self.otimesfor=odtgs
        else:
            self.otimesbak=odtgsbak
            self.otimesfor=odtgsfor

        self.otimes=odtgs
        # -- make sure there are at least two times...
        #
        if(len(self.otimes) > 1):
            self.dttime=mf.dtgdiff(self.otimes[-2],self.otimes[-1])     
        else:
            self.dttime=dttimeDefault

    def initLF(self):
         
        #from w2 import SetLandFrac
        #from w2 import GetLandFrac
        
        self.lf=w2.SetLandFrac()
        self.GetLandFrac=w2.GetLandFrac
        

    def getLF(self,lat,lon):
        landfrac=self.GetLandFrac(self.lf,lat,lon)
        return(landfrac)


    def setGradsData(self,tdtg,
                     tname='btvmax',
                     tdir='/tmp',
                     ):
    
        cpath="%s/%s.%s.ctl"%(tdir,tname,tdtg)
        opath="%s/%s.%s.dat"%(tdir,tname,tdtg)
        
        # -- make the beginning time the 1st track
        #
        bdtg=self.otimes[0]
        bgtime=mf.dtg2gtime(bdtg)
        
        if(not(hasattr(self,'dttime'))): 
            dttime=mf.dtgdiff(self.otimes[-2],self.otimes[-1])
            self.ddtime=dttime
        else:
            dttime=self.dttime
            
        tottime=mf.dtgdiff(self.otimes[0],self.otimes[-1])
        
        nt=int(tottime/dttime)+1
        
        (rlat,rlon)=self.platlons[self.otimes[0]]
        self.platlons0=(rlat,rlon)
        
        ctl="""dset %s
title %s
undef 1e20
xdef 1  levels %6.1f
ydef 1  levels %5.1f
zdef 1  levels 1013
tdef %d linear %s %dhr
vars 1
bvm 0 0 %s
endvars"""%(opath,tname,rlon,rlat,
            nt,bgtime,dttime,
            tname)
        
        MF.WriteString2Path(ctl,cpath)

        stnid='btvmax01'
        stndt=0.0
        
        oB=open(opath,'wb')
        
        # - not station data..
        #stnhead = struct.pack('8sfffii',stnid,rlat,rlon,stndt,1,0)
        #stnfoot = struct.pack('8sfffii',stnid,rlat,rlon,stndt,0,0)

        for otime in self.otimes:
            #oB.write(stnhead)
            try:
                stnrec = struct.pack('1f',self.pvmax[otime])
            except:
                continue
            oB.write(stnrec)
            #oB.write(stnfoot)
        
        oB.close()
        



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
               #yoffset=0.10,
               yoffset=0.075,
               xoffset=0.05,
               location='c',
               dlab=None,
               rotate=-30,
               #rotate=30,
               ):

        if(times == None): times=self.otimes

        self._cmd(self.clipplot)
        for n in range(0,len(times)):

            try:
                (x0,y0)=self.xys[times[n]]
                y0=y0-lbsiz*0.5-yoffset
                x0=x0-xoffset
                if(dlab == None):
                    label="%3d"%(self.pvmax[times[n]])
                else:
                    label=dlab
                if(x0 == None):  continue
            except:
                continue

            self._cmd('set string %d %s %d %d'%(lbcol,location,lbthk,rotate))
            self._cmd("set strsiz %f"%(lbsiz))
            self._cmd("draw string %f %f %s"%(x0,y0,label))


    def legend(self,ge,
               times=None,
               btcol=None,
               bttitle=None,
               btlgdcol=None,
               resetfinaly=0,
               hiTime=None,
               ystart=7.9,
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

        if((not(hasattr(self,'finaly')) and ystart != None) or resetfinaly):
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
            
            # -- hilite a dtg
            #
            if(hiTime != None and time == hiTime):
                self._cmd('set string 7 l %d'%(sthk+2))
                self._cmd("set strsiz %f"%(yss+0.001))
            else:
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
            maxlandFrac=0.80,
            verb=0,
            quiet=0,
            ):

        self.dovmaxflg=dovmaxflg
        self.doland=doland
        self.maxlandFrac=maxlandFrac

        self.initLF()
        self.initVars(lcol,lsty,lthk,msym,mcol,msiz,mthk,verb)
        self.setPcutcols()
        self.initProps(fts)
        self.setLineProps()
        self.setMarkProps()


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

            try:
                plat=fts[tau][0]
                plon=fts[tau][1]
            except:
                print 'EEE gXplotTcFt plat exception: ',tau
                continue

            if(plon == None): continue

            landfrac=self.getLF(plat,plon)
            if(self.doland == 0 and landfrac > self.maxlandFrac): continue

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


    def setLineProps(self):

        for tau in self.taus:
            try:
                dvmax=self.pdvmax[tau]
                vmaxflg=self.pvmaxflg[tau]
                self.setSegCol(tau,dvmax,vmaxflg)
            except:
                continue


    def setMarkProps(self):
        
        for tau in self.taus:
            ftsiz=self.msiz
            ftsym=self.msym
            ftcol=self.mcol
            ftthk=self.mthk

            self.markprop[tau]=(ftsym,ftsiz,ftcol,ftthk)


        
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

 
    def setGradsData(self,tdtg,
                     dttime=None,
                     tname='fcvmax',
                     platlons=None,
                     tdir='/tmp',
                     undef=1e20,
                     maxtau=None,
                     ):
    
        cpath="%s/%s.%s.ctl"%(tdir,tname,tdtg)
        opath="%s/%s.%s.dat"%(tdir,tname,tdtg)
        
        bgtime=mf.dtg2gtime(tdtg)
        if(maxtau != None):
            tottime=maxtau
        else:
            tottime=self.otimes[-1]-self.otimes[0]

        if(len(self.otimes) > 1 and dttime == None):
            dttime=self.otimes[1]-self.otimes[0]
            
        nt=int(tottime/dttime)+1
        
        if(platlons == None):
            (rlat,rlon)=self.platlons[self.otimes[0]]
        else:
            (rlat,rlon)=platlons
        
        ctl="""dset %s
title %s
undef %10.0e
xdef 1  levels %6.1f
ydef 1  levels %5.1f
zdef 1  levels 1013
tdef %d linear %s %dhr
vars 1
fvm 0 0 %s
endvars"""%(opath,tname,undef,rlon,rlat,
            nt,bgtime,dttime,
            tname)
        
        MF.WriteString2Path(ctl,cpath)

        stnid='btvmax01'
        stndt=0.0
        
        oB=open(opath,'wb')
        
        for n in range(0,int(tottime/dttime)+1):
            otime=n*dttime
            if(otime in self.otimes): ovmax=self.pvmax[otime]
            else:                     ovmax=undef
            
            # -- 20180520 - case with aid not having Vmax
            #
            if(ovmax < 0.0): ovmax=undef
            stnrec = struct.pack('1f',ovmax)
            oB.write(stnrec)
        
        oB.close()
        



    
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
            hemiDir=None,
            ):
        
        from tcbase import rumltlg

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
            if(plat == None): continue
            self._cmd('q w2xy %f %f'%(plon,plat))
            self.xys.append([float(self._ga.rword(1,3)),float(self._ga.rword(1,6))])

        if(hemiDir != None):
            self.xysh=[]
            for theta in [hemiDir,hemiDir+180]:
                (plat,plon)=rumltlg(theta,spdc,dtau,clat,clon)
                if(plat == None): continue
                self._cmd('q w2xy %f %f'%(plon,plat))
                self.xysh.append([float(self._ga.rword(1,3)),float(self._ga.rword(1,6))])



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

    def hemiline(self,hemidir,lcol=1,lsty=1,lthk=5):

        self._cmd("set line %d %d %d"%(lcol,lsty,lthk))

        for n in range(1,len(self.xysh)):
            (x0,y0)=self.xysh[n-1]
            (x1,y1)=self.xysh[n]
            
            cmd="draw line %6.3f %6.3f %6.3f %6.3f"%(x0,y0,x1,y1)
            self._cmd(cmd)

class gXarrow(MFbase):

    def __init__(self,ga,ge,cmd):

        self._ga=ga
        self._cmd=cmd
        self._ge=ge


    def set(self,latc,lonc,len,dir,
            arrang=30.0,
            arrscl=0.20,
            lab=None,labopt=None,
            dodisplay=0,
            verb=0,
            ):
        
        from tcbase import rumltlg

        self.len=len
        self.dir=dir

        self.lab=lab
        self.labopt=labopt

        self._cmd('q w2xy %f %f'%(lonc,latc))

        x=float(self._ga.rword(1,3))
        y=float(self._ga.rword(1,6))

        dd=deg2rad*dir
        arrlen=len*arrscl

        xl=sin(dd)*len
        yl=cos(dd)*len

        da1=(dir+arrang)*deg2rad
        da2=(dir-arrang)*deg2rad
        
        xa1=sin(da1)*arrlen
        ya1=cos(da1)*arrlen
        
        xa2=sin(da2)*arrlen
        ya2=cos(da2)*arrlen
        
        xa1=x+xl-xa1
        ya1=y+yl-ya1
        
        xa2=x+xl-xa2
        ya2=y+yl-ya2
        
        x1=x+xl
        y1=y+yl

        if(verb):
            print 'arrow: '
            print '            x,y: ',x,y
            print '          x1,y1: ',x1,y1
            print 'xa1,ya1,xa2,ya2: ',xa1,ya1,xa2,ya2
            
        self.x=x
        self.y=y
        self.x1=x1
        self.y1=y1
        self.xa1=xa1
        self.ya1=ya1
        self.xa2=xa2
        self.ya2=ya2

        return


    def draw(self,lcol=1,lsty=1,lthk=5,doblackout=0,doblackin=0):

        # -- set outside black
        #
        if(doblackout):
            self._cmd("set line %d %d %d"%(0,lsty,20))
            pcmd="draw line %f %f %f %f"%(self.x1,self.y1,self.xa1,self.ya1) ; self._cmd(pcmd)
            pcmd="draw line %f %f %f %f"%(self.x1,self.y1,self.xa2,self.ya2) ; self._cmd(pcmd)
            pcmd="draw line %f %f %f %f"%(self.x,self.y,self.x1,self.y1)     ; self._cmd(pcmd)

        # -- draw the arrow
        #
        self._cmd("set line %d %d %d"%(lcol,lsty,lthk))
        pcmd="draw line %f %f %f %f"%(self.x1,self.y1,self.xa1,self.ya1) ; self._cmd(pcmd)
        pcmd="draw line %f %f %f %f"%(self.x1,self.y1,self.xa2,self.ya2) ; self._cmd(pcmd)
        pcmd="draw line %f %f %f %f"%(self.x,self.y,self.x1,self.y1)     ; self._cmd(pcmd)

        # -- set inside black
        #
        if(doblackin):
            self._cmd("set line %d %d %d"%(0,lsty,3))
            pcmd="draw line %f %f %f %f"%(self.x1,self.y1,self.xa1,self.ya1) ; self._cmd(pcmd)
            pcmd="draw line %f %f %f %f"%(self.x1,self.y1,self.xa2,self.ya2) ; self._cmd(pcmd)
            pcmd="draw line %f %f %f %f"%(self.x,self.y,self.x1,self.y1)     ; self._cmd(pcmd)



class gXcbarn(MFbase):


    def __init__(self,ga,ge):

        self._cmd=ga
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

        # -- check if ge has colbar -- 20130816 -- not sure why I did this
        # -- 20150311 -- because ge.setShades adds colbar var to ge.
        #
        elif(hasattr(ge,'colbar')):
            print 'III(ga2.gXcbarn.ge.setShades: ',ge.colbar
            None    
        else:
            # -- get shades if not set above adds ge.colbar
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
            t2col=1,
            t3col=1,
            t2scale=0.80,
            t3scale=0.70,
            t1thk=5,
            t2thk=5,
            t3thk=5,
            ):
        
        self.scale=scale
        self.t1col=t1col
        self.t2col=t2col
        self.t3col=t3col
        self.t2scale=t2scale
        self.t3scale=t3scale
        self.t1thk=t1thk
        self.t2thk=t2thk
        self.t3thk=t3thk
        
    def clip(self):

        self._ge.getGxinfo()
        self._cmd("set clip 0 %6.3f 0 %6.3f"%(self._ge.pagex,self._ge.pagey))
        

    def top(self,t1,t2=None,t3=None,doclip=1):

        if(doclip): self.clip()
        #
        # if scale < 0.0 then make size of t2 = t1
        #
        if(self.scale < 0.0):
            scale=scale*-1.0
            t2scale=1.05
            t3scale=1.05
        else:
            t2scale=self.t2scale
            t3scale=self.t3scale
            
        xr=self._ge.pagex
        xl=0
        y1=self._ge.pagey-0.15
        xs=(xr-xl)*0.5
        tsiz=0.15
        
        tsiz=tsiz*self.scale
        t2siz=tsiz*t2scale
        y2=self._ge.pagey-0.15-tsiz*1.5

        t3siz=tsiz*t3scale
        y3=y2-tsiz*1.5

        self._cmd('set strsiz %f'%(tsiz))
        self._cmd('set string %d c %d 0'%(self.t1col,self.t1thk))
        self._cmd('draw string %f %f %s'%(xs,y1,t1))

        if(t2 != None):
            self._cmd('set string %d c %d 0'%(self.t2col,self.t2thk))
            self._cmd('set strsiz %f'%(t2siz))
            self._cmd('draw string %f %f `0%s`0'%(xs,y2,t2))

        if(t3 != None):
            self._cmd('set string %d c %d 0'%(self.t3col,self.t3thk))
            self._cmd('set strsiz %f'%(t3siz))
            self._cmd('draw string %f %f `0%s`0'%(xs,y3,t3))

        


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


    def plot(self,t1,t2=None,sopt=None,doclip=1):

        if(doclip): self.clip()
        
        #
        # if scale < 0.0 then make size of t2 = t1
        #
        if(self.scale < 0.0):
            scale=scale*-1.0
            t2scale=1.05
        else:
            scale=self.scale
            t2scale=0.80

        dxs=self._ge.plotxl
        dyt=self._ge.pagey-self._ge.plotyt

        tsiz=0.09
        xoff=0.75

        tsiz=tsiz*scale
        t2siz=tsiz*t2scale

        yoffscale=1.3
        yoff=tsiz*yoffscale

        xs=self._ge.plotxl-xoff-tsiz
        xm=(self._ge.plotxl+self._ge.plotxr)*0.5
        ys=(self._ge.plotyb+self._ge.plotyb)*0.5

        angle=90
        tt=tsiz+yoff

        if(tt < dyt):
            xs=xm
            ys=self._ge.plotyt+yoff+tsiz/2 
            angle=0

        y2=ys
        y1=ys
        if(t2 != None):
            y1=ys+yoff
            y2=y1-yoff*yoffscale
            
        #self._cmd('set line 0')
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
        self.arrow=gXarrow(ga,ge,ga)
        self.cbarn=gXcbarn(ga,ge)



class gxout(MFbase):

    def __init__(self,ga):
        self._cmd=ga.cmd
        
    def shaded(self):
        self._cmd('set gxout shaded')

    def contour(self):
        self._cmd('set gxout contour')



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
                 backgroundColor=0,
                 grid='on',
                 gridcol=1,
                 gridstyle=3,
                 pngmethod='printim',
                 gradslab='off',
                 timelab='off',
                 quiet=0,
                 verb=0,
                 xsize=1024,
                 ysize=768,
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

        self.backgroundColor=backgroundColor
        
        self.grid=grid
        self.gridcol=gridcol
        self.gridstyle=gridstyle

        self.pngmethod=pngmethod

        self.timelab=timelab
        self.gradslab=gradslab

        self.verb=verb

        self.xsize=xsize
        self.ysize=ysize
        



    def makePng(self,
                opath,
                bmpath=None,
                bmcol=0,
                xsize=None,
                ysize=None,
                background='black',
                ropt='',
                verb=1,
                ):

        # -- this the xsize on the _ge object = self; from the set method in gXbasemap2
        #
        if(xsize == None and hasattr(self,'xsize')): xsize=self.xsize
        if(ysize == None and hasattr(self,'ysize')): ysize=self.ysize
        
        if(self.pngmethod == 'printim'):
            bkopt=''
            if(background == 'black'):
                bkopt='black'
            if(bmpath == None):
                cmd="%s %s %s x%d y%d"%(self.pngmethod,opath,bkopt,xsize,ysize)
            else:
                cmd="%s %s %s -b %s -t %d x%d y%d"%(self.pngmethod,opath,bkopt,bmpath,bmcol,xsize,ysize)

        elif(self.pngmethod == 'gxyat'):
            bkopt=''
            if(background == 'black'):
                bkopt='-r'
            cmd="%s -x %d -y %d %s %s"%(self.pngmethod,xsize,ysize,bkopt,opath)

        if(verb):
            print "makePng: %s cmd: %s"%(opath,cmd)

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
                  

    def setFwrite(self,name,type='-sq'):

        cmd="""set fwrite %s %s"""%(type,name)
        self._cmd(cmd)



    def drawMap(self):
        self._cmd('draw map')

    def clear(self):
        self._cmd('c')
        

    def getLevs(self,obj=None,verb=0):

        if(obj != None and hasattr(obj,'fh') ):
            fh=obj.fh

        elif(hasattr(self,'fh')):
            fh=self.fh
        else:
            print """WWW in GradsLevs...need a 'fh' var to get filemeta data..."""
            sys.exit()

        if(obj == None): obj=self
        nz=fh.nz
        self.dimLevs=obj.dimLevs=list(self._ga.coords().lev)
        self.dimNlevs=obj.dimNlevs=len(self.dimLevs)
        self._cmd("set z 1 %d"%(nz))
        self.Levs=obj.Levs=list(self._ga.coords().lev)
        if(verb): print 'getLevs: nz: ',nz,'levs: ',self.Levs
        self._cmd("set z 1")
            

    def getFileMeta(self,obj=None):

        if(obj != None and hasattr(obj,'fh') ):
            fh=obj.fh

        elif(hasattr(self,'fh')):
            fh=self.fh
        else:
            print """WWW in GradsEnv...need a 'fh' var to get filemeta data..."""
            sys.exit()
            
        if(obj == None): obj=self

        self.nx=obj.nx=fh.nx
        self.ny=obj.ny=fh.ny
        self.nz=obj.nz=fh.nz
        self.nt=obj.nt=fh.nt
        self.undef=obj.undef=fh.undef

        self.dimlevs=obj.dimlevs=list(self._ga.coords().lev)
        self.dimNlevs=obj.dimNlevs=len(obj.dimlevs)
        self._cmd("set z 1 %d"%(self.nz))

        self.lats=obj.lats=list(self._ga.coords().lat)
        self.lons=obj.lons=list(self._ga.coords().lon)
        if(len(self.lons) > 1):
            self.dlon=obj.dlon=self.lons[1]-self.lons[0]
        else:
            self.dlon=0.0
        
        self.levs=obj.levs=list(self._ga.coords().lev)
        self._cmd("set lev %d"%(self.dimlevs[0]))

        self.vars=obj.vars=list(fh.vars)



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
            # -- new outout from q shades in 2.0.0.oga1
            #
            if(minval == '<' or minval == '<='):
                minval=-1e20
                maxval=float(maxval)
            elif(maxval == '>' or maxval == '>='):
                minval=float(minval)
                maxval=1e20
            else:
                minval=float(minval)
                maxval=float(maxval)

            self.colbar.append([col,minval,maxval])
            if(verb): print "III(GradsEnv.getShades):",n,col,minval,maxval,self.colbar

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

    def setXsize(self,xsize=1024,ysize=768):

        if(hasattr(self,'xsize')): xsize=self.xsize
        if(hasattr(self,'ysize')): ysize=self.ysize
        
        self._cmd("set xsize %d %d"%(xsize,ysize))

    def setPlotScale(self):
        self._cmd('set grads %s'%(self.gradslab))
        self._cmd('set timelab %s'%(self.timelab))
        self._cmd('set cmax -1e20')
        self._cmd('set grid on 3 15')
        
        # -- the lat var is displayed differently than a real data var -- use only if one not available
        # -- not really this is a red herring -- conflict with how display is calc with grids that are not 1.0 0.5 deg...
        # -- must be something in the xfrm in grads?  when setting lat/lon to NOT be a multiple of the grid res? pretty weird
        #
        dumvar='lat'
        if(hasattr(self,'vars')): dumvar=self.vars[0]
        
        # -- case of dum.ctl -- use 'lat'
        #
        if(dumvar == 'dum' or dumvar == 't'): dumvar='lat'

        # -- this doesn't work when dumvar in self.vars[0] is undef
        #exprdum="const(%s,1,-a)"%(dumvar)
        #
        # -- 20190224 -- force use of 'lat' with 2.2.1
        #
        dumvar='lat'
        exprdum=dumvar
        
        self._cmd('q dims')
        self._cmd('q ctlinfo')
        self._cmd('d abs(%s)'%(exprdum))


    def setLatLon(self):
        self._cmd("set lat %f %f"%(self.lat1,self.lat2))
        self._cmd("set lon %f %f"%(self.lon1,self.lon2))

    def setLevs(self):

        if(not(hasattr(self,'lev2'))):
            self.lev2=self.lev1
        self._cmd("set lev %f %f"%(self.lev1,self.lev2))

    def setBackgroundColor(self):
        self._cmd("set background %d"%(self.backgroundColor))
        
    def setColorTable(self,table='jaecolw2.gsf'):
        self._cmd("run %s"%(table))

    def setTimebyDtg(self,dtg,verb=0):
        gtime=mf.dtg2gtime(dtg)
        self.gtime=gtime
        if(verb): print "set time to: %s  from: %s"%(gtime,dtg)
        self.cmdQ("set time %s"%(gtime))

    def setTimebyDtgTau(self,dtg,tau,verb=0):
        vdtg=mf.dtginc(dtg,tau)
        gtime=mf.dtg2gtime(vdtg)
        self.gtime=gtime
        if(self.verb or verb): print "set time to: %s  from dtg: %s tau: %d"%(gtime,dtg,tau)
        self.cmdQ("set time %s"%(gtime))

    def reinit(self):
        self._cmd("reinit")
        



#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# w2gabase

class W2GaBase(MFbase):
    
    def c(self):
        self._cmd('clear')
        
    def d(self,var):
        rc=self._cmd('d %s'%(var))
        return(rc)
        
    def q(self,var):
        rc=self.query(var)
        return(rc)
        
        
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


    def LogPinterp(self,var,lev,texpr=None,mfact=None,verb=0):

        ge=self.ge
        
        from math import log
        for k in range(0,ge.nz-1):
            
            lev1=ge.levs[k]
            lev2=ge.levs[k+1]
            
            if(lev <= lev1 and lev >= lev2):
                lp1=log(lev1)
                lp2=log(lev2)
                lp=log(lev)
                dlp=lp1-lp2
                f2=(lp1-lp)/dlp
                f1=(lp-lp2)/dlp
                if(mfact != None):
                    f2=f2*mfact
                    f1=f1*mfact
                
                if(verb):
                    lf2=(lev1-lev)/(lev1-lev2)
                    lf1=(lev-lev2)/(lev1-lev2)
                    print 'HHHHHHHHHHHH ',lev1,lev,lev2,f1,f2,(f1+f2),lf1,lf2

                if(texpr == None):
                    expr="(%s(lev=%-6.1f)*%f + %s(lev=%-6.1f)*%f)"%(var,lev1,f1,var,lev2,f2)
                    if(f1 == 0.0 and f2 != 0.0):
                        expr="(%s(lev=%-6.1f)*%f)"%(var,lev2,f2)
                    if(f2 == 0.0 and f1 != 0.0):
                        expr="(%s(lev=%-6.1f)*%f)"%(var,lev1,f1)
                        
                else:
                    expr="(%s(%s,lev=%-6.1f)*%f + %s(%s,lev=%-6.1f)*%f)"%(var,texpr,lev1,f1,var,texpr,lev2,f2)
                    if(f1 == 0.0 and f2 != 0.0):
                        expr="(%s(%s,lev=%-6.1f)*%f)"%(var,texpr,lev2,f2)
                    if(f2 == 0.0 and f1 != 0.0):
                        expr="(%s(%s,lev=%-6.1f)*%f)"%(var,texpr,lev1,f1)
                    
                expr=expr.replace(' ','')

                return(expr)

        print 'EEE unable to interpolate to pressure level: ',lev
        print 'EEE time for plan B...in LogPinterp'
            
        return(expr)



    def LogPinterpTinterp(self,var,lev,tm1=1,tp1=1,tfm1=0.5,tfp1=0.5,verb=0):

        ge=self.ge
        
        from math import log
        for k in range(0,ge.nz-1):
            
            lev1=ge.levs[k]
            lev2=ge.levs[k+1]
            
            if(lev <= lev1 and lev >= lev2):
                lp1=log(lev1)
                lp2=log(lev2)
                lp=log(lev)
                dlp=lp1-lp2
                f2=(lp1-lp)/dlp
                f1=(lp-lp2)/dlp
                
                if(verb):
                    lf2=(lev1-lev)/(lev1-lev2)
                    lf1=(lev-lev2)/(lev1-lev2)
                    print 'HHHHHHHHHHHH ',lev1,lev,lev2,f1,f2,(f1+f2),lf1,lf2
                    
                exprm1="( (%s(t-%d,lev=%-6.1f)*%f + %s(t-%d,lev=%-6.1f)*%f)*%f )"%(var,tm1,lev1,f1,var,tm1,lev2,f2,tfm1)
                exprp1="( (%s(t+%d,lev=%-6.1f)*%f + %s(t+%d,lev=%-6.1f)*%f)*%f )"%(var,tp1,lev1,f1,var,tp1,lev2,f2,tfp1)
                expr="(%s + %s)"%(exprm1,exprp1)
                
                expr=expr.replace(' ','')
                return(expr)

        print 'EEE unable to interpolate to pressure level: ',lev
        print 'EEE time for plan B...in LogPinterp'
            
        return(expr)



class gxGxout(MFbase):

    def __init__(self,g1s,g1v,g2s,g2v,stn):
        self.g1s=g1s
        self.g1v=g1v
        self.g2s=g2s
        self.g2v=g2v
        self.stn=stn
        

class gxout(MFbase):

    def __init__(self,ga):
        self._cmd=ga.cmd
        
    def shaded(self):
        self._cmd('set gxout shaded')

    def contour(self):
        self._cmd('set gxout contour')



class gxset(MFbase):

    def __init__(self,ga):
        self._cmd=ga.cmd
        self._rl=ga.rline
        self._nL=ga.nLines
        

    def latlon(self,lat1=-90,lat2=90,lon1=0,lon2=360):
        self._cmd("set lat %f %f"%(lat1,lat2))
        self._cmd("set lon %f %f"%(lon1,lon2))
        
    def latlonA(self,area):
        self._cmd("set lat %f %f"%(area.lat1,area.lat2))
        self._cmd("set lon %f %f"%(area.lon1,area.lon2))        
        
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

                
## Stats[(sum,sumsqr,root(sumsqr))/n]:     100838 1.01701e+10 100847
            if(mf.find(card,',root(sumsqr))/n]:')):
                tt=card.split()
                self.mean=float(tt[1])

class gxGxout(MFbase):

    def __init__(self,g1s,g1v,g2s,g2v,stn):
        self.g1s=g1s
        self.g1v=g1v
        self.g2s=g2s
        self.g2v=g2v
        self.stn=stn
        
            

class gxget(MFbase):


    def __init__(self,ga,verb=0):
        self._cmd=ga.cmd
        self.ga=ga
        self.verb=verb
        

    def scorr(self,var1,var2,area):

        expr="scorr(%s,%s,lon=%s,lon=%s,lat=%s,lat=%s)"%(var1,var2,
                                                         area.lon1,area.lon2,
                                                         area.lat1,area.lat2)

        self.ga('d %s'%(expr))
        scorr=float(self.ga.rword(1,4))
        if(self.verb): print 'scorr: ',scorr

        return(scorr)

    def asum(self,var1,area):

        expr="asum(%s,lon=%s,lon=%s,lat=%s,lat=%s)"%(var1,
                                                     area.lon1,area.lon2,
                                                     area.lat1,area.lat2)
        self.ga('d %s'%(expr))
        asum=float(self.ga.rword(1,4))
        if(self.verb): print 'asum:    ',asum 
        return(asum)

    def aave(self,var1,area):

        expr="aave(%s,lon=%s,lon=%s,lat=%s,lat=%s)"%(var1,
                                                     area.lon1,area.lon2,
                                                     area.lat1,area.lat2)
        self.ga('d %s'%(expr))
        aave=float(self.ga.rword(1,4))
        if(self.verb): print 'aave:    ',aave
        return(aave)


    def asumg(self,var1,area):

        expr="asumg(%s,lon=%s,lon=%s,lat=%s,lat=%s)"%(var1,
                                                     area.lon1,area.lon2,
                                                     area.lat1,area.lat2)

        self.ga('d %s'%(expr))
        asumg=float(self.ga.rword(1,4))
        if(self.verb): print 'asumg:   ',asumg

        return(asumg)


    def stat(self,expr):

        # get the current graphics and rank of display grid
        rank=len(self.ga.coords().shape)
        cgxout=self.gxout()

        # set gxout to stats; display expression
        self.ga.cmdQ('set gxout stat')
        self.ga.cmdQ('d %s'%(expr))
        cards=self.ga.Lines
        stats=gxStats(cards)

        # reset the original gxout
        if(rank == 1): self.ga.cmdQ('set gxout %s'%(cgxout.g1s))
        if(rank == 2): self.ga.cmdQ('set gxout %s'%(cgxout.g2s))

        return(stats)


    def gxout(self):
        
        self.ga.cmdQ('q gxout')
        g1s=self.ga.rword(2,6)
        g1v=self.ga.rword(3,6)
        g2s=self.ga.rword(4,6)
        g2v=self.ga.rword(5,6)
        stn=self.ga.rword(6,4)
        gxout=gxGxout(g1s,g1v,g2s,g2v,stn)
        return(gxout)
        
        

class gxdefvar(MFbase):

    def __init__(self,ga):
        self._cmd=ga.cmd
        self._rl=ga.rline
        self._nL=ga.nLines

    def var(self,var,expr):

        cmd="""%s=%s"""%(var,expr)
        self._cmd(cmd)
        return(cmd)
        
    def re2(self,var,expr,dx=2.5,dy=2.5,method='ba'):

        cmd="""%s=re2(%s,%f,%f,%s)"""%(var,expr,dx,dy,method)
        self._cmd(cmd)
        return(cmd)
        
    def regrid(self,var,expr,reargs):

        cmd="""%s=re(%s,%s)"""%(var,expr,reargs)
        self._cmd(cmd)
        return(cmd)


    def dregrid(self,var,expr,reargs):

        cmd="""d re(%s,%s)"""%(expr,reargs)
        self._cmd(cmd)
        return(cmd)

    def dregrid0(self,var,expr,reargs,undef=0):

        cmd="""d const(re(%s,%s),%s,-u)"""%(expr,reargs,str(undef))
        self._cmd(cmd)
        return(cmd)

    def dundef0(self,expr,undef=0):

        cmd="""d const(%s,%s,-u)"""%(expr,str(undef))
        self._cmd(cmd)
        return(cmd)

        
    def writef77(self,var):
        
        cmd="""set gxout fwrite
d %s"""%(var)
        self._cmd(cmd)

        # set gxout to standard
        self._cmd('set gxout contour')
        
        
    def sh_filt(self,var,expr,nwaves=20):

        cmd="""%s=sh_filt(%s,%d)"""%(var,expr,nwaves)
        self._cmd(cmd)
        
        
        



class GaLats(W2GaBase):

    prcdir=W2BaseDirPrc
    
    def cmd2(self,gacmd,RcCheck=0):
        self._ga.cmd2(gacmd,Quiet=0,RcCheck=RcCheck)


    def initGrads(self,ga,ge,quiet=1,RcCheck=1):

        #self._cmd=ga.cmd(gacmd='',oRcCheck=RcCheck)
        if(hasattr(ga,'quiet')): quiet=ga.quiet

        if(quiet):
            self._cmd=ga.cmdQ
            ga.__call__=ga.cmdQ
        else:
            self._cmd=ga.cmd

        self._ga=ga
        self._ge=None
        if(ge != None):self._ge=ge

        self.rl=ga.rline
        self.rw=ga.rword

        self.ga=ga
        self.ge=ge

        

    def __init__(self,ga,ge,dtg=None,
                 model='rtfim',
                 center='esrl',
                 comment='grib1 output for tm tracker',
#                 outconv='grads_grib',
                 outconv='grib_only',
                 calendar='standard',
                 ptable=None,
                 frequency='forecast_hourly',
                 timeoption='dim_env',
                 gridtype='linear',
                 btau=0,
                 etau=168,
                 dtau=6,
                 taus=None,
                 regrid=0,
                 remethod='re',
                 smth2d=0,
                 doyflip=0,
                 quiet=0,
                 reargs=None,
                 ):

        if(hasattr(ga,'quiet')): quiet=ga.quiet
        self.initGrads(ga,ge,quiet=quiet)
        self.dtg=dtg
        self.model=model
        self._cmd=self.cmd2
        
        self.frequency=frequency
        
        self.regrid=regrid
        self.remethod=remethod
        self.smth2d=smth2d
        self.doyflip=doyflip
        self.reargs=reargs
                 
        self.area='global'

        self.btau=btau
        self.etau=etau
        self.dtau=dtau

        if(taus == None):
            self.taus=range(btau,etau+1,dtau)
        else:
            self.taus=taus
            #dtau=self.taus[-1]-self.taus[-2]
            # -- base on beginning vice end for models where e.g., dtau = 12 > tau48 (ukm2)
            if(len(taus) > 1):
                dtau=self.taus[1]-self.taus[0]
            else:
                if(dtau != None): dtau=dtau
                else: print 'EEE GaLats dtau == None and len of taus = 1, set dtau in __init__'; sys.exit()
        

        if(ptable == None):
            ptable="%s/hfip/lats.hfip.table.txt"%(self.prcdir),

            
        self("set_lats parmtab %s"%(ptable))
        self("set_lats convention %s"%(outconv))
        self("set_lats calendar %s"%(calendar))
        self("set_lats model %s"%(model))
        self("set_lats center %s"%(center))
        self("set_lats comment %s"%(comment))
        self("set_lats timeoption %s"%(timeoption))
        self("set_lats frequency %s"%(frequency))

        if(self.frequency == 'forecast_hourly'):
            self("set_lats deltat %d"%(dtau))
        elif(self.frequency == 'forecast_minutes'):
            self("set_lats deltat %d"%(dtau*60))

        self("set_lats gridtype %s"%(gridtype))

        if(hasattr(ga,'fh')):
            self.fh=ga.fh
        else:
            print 'EEE GaLats(Q) needs a fh object (file handle) in the grads.ga object'
            sys.exit()
        
        ge.getFileMeta(self)
        

    def q(self):
        self('query_lats')
        for n in range(1,self._ga.nLines):
            print self._ga.rline(n)

    def create(self,opath):
        self("set_lats create %s"%(opath))
        self.id_file=int(self.rw(1,5))
        

    def basetime(self,dtg):
        yyyy=int(dtg[0:4])
        mm=int(dtg[4:6])
        dd=int(dtg[6:8])
        hh=int(dtg[8:10])
        self("set_lats basetime %d %d %d %d %d 0 0"%(self.id_file,yyyy,mm,dd,hh))
        self.dtg=dtg


    def grid(self,areaObj=None):

        if(self.regrid > 0):
            if(self.remethod == 're2'):
                if(hasattr(self,'reargs') and self.reargs != None):
                    self("vargrid=re2(%s,%s)"%(self.vars[0],self.reargs))
                else:
                    self("vargrid=re2(%s,%5.3f)"%(self.vars[0],self.regrid))
            else:
                self.dlon=self.dlat=self.regrid
                self.nxre=int((360.0-self.regrid)/self.regrid+0.5)+1
                self.nyre=int(180.0/self.regrid+0.5)+1
                
                if(hasattr(self,'reargs') and self.reargs != None):
                    varexpr="vargrid=re(%s,%s)"%(self.vars[0],self.reargs)
                else:
                    varexpr="vargrid=re(%s,%d,linear,0.0,%f,%d,linear,-90.0,%f)"%(self.vars[0],self.nxre,self.dlon,self.nyre,self.dlat)

                self(varexpr)

        else:
            self("vargrid=%s"%(self.vars[0]))


        latN=latS=lonW=lonE=dLat=dLon=dx=dy=None

        if(areaObj != None):
            latN=areaObj.latN
            latS=areaObj.latS
            lonW=areaObj.lonW
            lonE=areaObj.lonE
            dLat=areaObj.dLat
            dLon=areaObj.dLon
            dx=areaObj.dx
            dy=areaObj.dy
            
        # -- old version of setting up grid
        #

        if(self.area == 'global' and latS == None):
            self("set x 1 %d"%(self.nx))
            self("set y 1 %d"%(self.ny))
            if(self.regrid > 0):
                elon=360.0-self.regrid
                self("set lon 0 %f"%(elon))
                self("set lat -90 90")
                
##         else:
##             return


        # -- new version using areaObj
        #
        if(latS != None and latN != None):
            self("set lat %f %f"%(latS,latN))

        if(lonW != None and lonE != None):

            lon1=lonW
            lon2=lonE
            if(dLon == 360): lon2=lonE-dx
            self("set lon %f %f"%(lon1,lon2))

        if(self.doyflip): self("set yflip on")

        self("lats_grid vargrid")
        self.id_grid=int(self.rw(1,5))


    def plevdim(self,uavars,verb=0):

        plevs=[]
        for uavar in uavars:
            plevs=plevs+uavar[2]

        plevs=mf.uniq(plevs)

        lexpr="set_lats vertdim plev "
        for plev in plevs:
            lexpr="%s %f"%(lexpr,plev)

        if(verb): print 'lllllllllllllll ',lexpr
        self(lexpr)
        self.id_vdim=int(self.rw(1,5))

    def plevvars(self,uavars):

        self.id_uvars={}
        for uavar in uavars:
            if(len(uavar) == 3):
                (name,levtype,levs)=uavar
            elif(len(uavar) == 4):
                (name,levtype,levs,exprs)=uavar
            elif(len(uavar) == 5):
                (name,levtype,levs,mfact,afact)=uavar

            latscmd="set_lats var %d %s %s %d %d"%(self.id_file,name,levtype,self.id_grid,self.id_vdim)
            self(latscmd)
            self.id_uvars[name]=int(self.rw(1,5))

    def sfcvars(self,svars):

        self.id_svars={}
        for svar in svars:
            
            if(len(svar) == 2):
                (name,sfctype)=svar
            elif(len(svar) == 3):
                (name,sfctype,expr)=svar
                
            self("set_lats var %d %s %s %d 0"%(self.id_file,name,sfctype,self.id_grid))
            self.id_svars[name]=int(self.rw(1,5))


    def outvars(self,svars,uavars,verb=0):

        for tau in self.taus:
            vdtg=mf.dtginc(self.dtg,tau)
            gtime=mf.dtg2gtime(vdtg)
            
            self("set time %s"%(gtime))
            if(self.frequency == 'forecast_hourly'):
                self("set_lats fhour %f "%(tau))
            elif(self.frequency == 'forecast_minutes'):
                self("set_lats fminute %f "%(tau*60))

            
            for uavar in uavars:
                
                rc=uavar
                doregular=0
                doexpr=0
                mfact=None
                afact=None
                dofact=0
                
                if(len(rc) == 3):
                    (name,uatype,levs)=rc
                    doregular=1
                    
                elif(len(rc) == 4):
                    (name,uatype,levs,exprs)=rc
                    if(not(type(exprs) is ListType)):
                        print 'simple expression exprs: ',exprs
                        doregular=1
                        doexpr=1
                        
                elif(len(rc) == 5):
                    (name,uatype,levs,mfact,afact)=rc
                    doregular=1
                    dofact=1
                        
                
                if(doregular):
                    
                    id=self.id_uvars[name]
    
                    for lev in levs:
                        self("set_lats write %d %d %f"%(self.id_file,self.id_uvars[name],lev))
                        self("set lev %f"%(lev))
                        if( (name == 'ta' or name == 'tmpp') and lev == 401):
                            expr="(vint(const(%s,500,-a),%s,300)/vint(const(%s,500,-a),const(%s,1,-a),300))"%(name,name,name,name)
                            if(verb): print 'vint expr: ',expr 
                        else:
                            if(lev in self.levs):
                                if(doexpr):
                                    expr=exprs
                                else:
                                    expr=name
                                if(dofact and mfact != None):
                                    expr="%s*%f"%(expr,mfact)
                            else:
                                if(verb): print 'IIII dooohhh!  ',lev,' not in: y',self.levs,' do ln(p) interp...for: ',name
                                if(doexpr):
                                    expr=self.LogPinterp(exprs,lev,mfact=mfact)
                                else:
                                    expr=self.LogPinterp(name,lev,mfact=mfact)
                                if(verb): print 'IIII lev: ',lev,' expr: ',expr
                                
                        if(self.regrid > 0):
                            
                            if(self.remethod == 're2'):
                                if(hasattr(self,'reargs') and self.reargs != None):
                                    expr="re2(%s,%s)"%(expr,self.reargs)
                                else:
                                    expr="re2(%s,%5.3f)"%(expr,self.regrid)
                            else:
                                if(hasattr(self,'reargs') and self.reargs != None):
                                    expr="re(%s,%s)"%(expr,self.reargs)
                                else:
                                    expr="re(%s,%d,linear,0.0,%f,%d,linear,-90.0,%f)"%(expr,self.nxre,self.dlon,self.nyre,self.dlat)
    
                        if(self.smth2d > 0):
                            expr="smth2d(%s,%d)"%(expr,self.smth2d)
    
                        self("lats_data %s"%(expr))
                        if(verb):
                            for n in range(1,self._ga.nLines):
                                print self._ga.rline(n)
                else:
                    
                    id=self.id_uvars[name]
                    
                    for lev in levs:
                        self("set_lats write %d %d %f"%(self.id_file,self.id_uvars[name],lev))
                        expr=exprs[levs.index(lev)] 
                        self("lats_data %s"%(expr))
                        if(verb):
                            for n in range(1,self._ga.nLines):
                                print self._ga.rline(n)
                    

            for svar in svars:
                
                sfcexpr=None
                if(len(svar) == 2):
                    (name,sfctype)=svar
                elif(len(svar) == 3):
                    (name,sfctype,sfcexpr)=svar
                    
                id=self.id_svars[name]

                self("set_lats write %d %d 0"%(self.id_file,self.id_svars[name]))
                
                expr=name
                if(sfcexpr != None): expr=sfcexpr

                if(self.regrid > 0):
                        
                    if(self.remethod == 're2'):
                        if(hasattr(self,'reargs') and self.reargs != None):
                            expr="re2(%s,%s)"%(expr,self.reargs)
                        else:
                            expr="re2(%s,%5.3f)"%(expr,self.regrid)
                    else:
                        if(hasattr(self,'reargs') and self.reargs != None):
                            expr="re(%s,%s)"%(expr,self.reargs)
                        else:
                            expr="re(%s,%d,linear,0.0,%f,%d,linear,-90.0,%f)"%(expr,self.nxre,self.dlon,self.nyre,self.dlat)

                if(self.smth2d > 0):
                    expr="smth2d(%s,%d)"%(expr,self.smth2d)

                self("lats_data %s"%(expr))
                if(verb):
                    for n in range(1,self._ga.nLines):
                        print self._ga.rline(n)


    def close(self):

        self("set_lats close %d"%(self.id_file))

                

    
    __call__=cmd2


class GaLatsQ(GaLats):

    def cmd2(self,gacmd,RcCheck=0):
        self._ga.cmd2(gacmd,Quiet=1,RcCheck=RcCheck)

    __call__=cmd2
        

def setGA(gaclass='gacore',Opts='',Bin='grads',Quiet=1,Window=0,verb=0,doLogger=0):

    if(gaclass == 'gacore'):

        MF.sTimer(tag='load grads gacore')
        from grads import GaCore,GrADSError
        MF.dTimer(tag='load grads gacore')
        

        class W2GaCore(GaCore,W2GaBase,GrADSError):

            Quiet=1

            def __init__ (self, 
                          Bin=Bin, Echo=True, Opts=Opts, Port=False, 
                          Strict=False, Quiet=0, RcCheck=None, Verb=0, Window=None,
                          doLogger=doLogger):

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
                self.ge.cmdQ=self.cmdQ

                self.ge._ga=self
                self.ge.rl=self.rline
                self.ge.rw=self.rword

                self.gp=GradsPlot(self,self.ge)
        

        ga=W2GaCore(Opts=Opts,Bin=Bin,Quiet=Quiet,Window=Window,doLogger=doLogger)



    if(gaclass == 'galats'):

        MF.sTimer(tag='load grads gacore - galats')
        from grads import GaCore,GrADSError
        MF.dTimer(tag='load grads gacore - galats')
        

        class W2GaLats(GaCore,GaLatsQ,GrADSError,MFbase):

            Quiet=1

            def __init__ (self, 
                          Bin='grads', Echo=True, Opts='', Port=False, 
                          Strict=False, Quiet=0, RcCheck=None, Verb=0, Window=None,
                          doLogger=doLogger):

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
                self.ge.cmdQ=self.cmdQ

                self.ge._ga=self
                self.ge.rl=self.rline
                self.ge.rw=self.rword

                self.gp=GradsPlot(self,self.ge)

                # -- lats vars
                #
                
                self.dtg=dtg
                self.model=model
                self._cmd=self.cmd2

                self.frequency=frequency

                self.regrid=regrid
                self.remethod=remethod
                self.smth2d=smth2d
                self.doyflip=doyflip
                self.reargs=reargs

                self.area='global'

                self.btau=btau
                self.etau=etau
                self.dtau=dtau

                if(taus == None):
                    self.taus=range(btau,etau+1,dtau)
                else:
                    self.taus=taus


                self("set_lats parmtab %s"%(ptable))
                self("set_lats convention %s"%(outconv))
                self("set_lats calendar %s"%(calendar))
                self("set_lats model %s"%(model))
                self("set_lats center %s"%(center))
                self("set_lats comment %s"%(comment))
                self("set_lats timeoption %s"%(timeoption))
                self("set_lats frequency %s"%(frequency))

                if(self.frequency == 'forecast_hourly'):
                    self("set_lats deltat %d"%(dtau))
                elif(self.frequency == 'forecast_minutes'):
                    self("set_lats deltat %d"%(dtau*60))

                self("set_lats gridtype %s"%(gridtype))

                if(hasattr(ga,'fh')):
                    self.fh=ga.fh
                else:
                    print 'EEE GaLats(Q) needs a fh object (file handle) in the grads.ga object'
                    sys.exit()

                ge.getFileMeta(self)


        ga=W2GaLats(Opts=Opts,Bin=Bin,Quiet=Quiet,Window=Window,doLogger=doLogger)



    elif(gaclass == 'ganum'):

        MF.sTimer(tag='load grads gacore-ganum')
        from grads import GaNum,GrADSError
        MF.dTimer(tag='load grads gacore-ganum')


        class W2GaNum(GaNum,W2GaBase,GrADSError):

            Quiet=1

            def __init__ (self, 
                          Bin='grads', Echo=True, Opts='', Port=False, 
                          Strict=False, Quiet=0, RcCheck=None, Verb=0, Window=None,
                          doLogger=doLogger):

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
                self.ge.cmdQ=self.cmdQ

                self.ge._ga=self
                self.ge.rl=self.rline
                self.ge.rw=self.rword

                self.gp=GradsPlot(self,self.ge)



        ga=W2GaNum(Opts=Opts,Bin=Bin,Quiet=Quiet,Window=Window,doLogger=doLogger)
        

    # -- decorate with verb
    ga.verb=verb
    ga.ge.verb=verb

    ga.gxout=gxout(ga)
    ga.set=gxset(ga)
    ga.dvar=gxdefvar(ga)
    ga.get=gxget(ga)
        
    return(ga)

