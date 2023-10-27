#!/usr/bin/env python

from WxMAP2 import *
w2=W2()

from M2 import setModel2

from tcbase import TcData,makePrwInventory

from adCL import TcFtBtGsf

AllAreas=w2.W2AreasPrw
ptmpBaseDir=w2.ptmpBaseDir


def getGfsGoesArea(area,bail=1):

    oarea=area
    if(not(area in w2.W2AreasPrw) and not(area in w2.W2AreasPrwOld)):
        print "EEE %s.getPrwArea() invalid area: --> %s <--"%(pyfile,area)
        print '    not in: ',w2.W2AreasPrw
        print '     or in: ',w2.W2AreasPrwOld
        if(bail): sys.exit()
        return(0,None)

    elif(area in w2.W2AreasPrw):
        return(1,area)
    
    elif(area in w2.W2AreasPrwOld):
        
        revhash={}

        kk=w2.W2AreasPrws.keys()

        for k in kk:
            val=w2.W2AreasPrws[k]
            revhash[val]=k
        
        try:
            oarea=revhash[area]
        except:
            oarea=None

        if(oarea == None):
            print "EEE %s.getGfsGoesArea() invalid area: --> %s <--"%(pyfile,area)
            print '    not in: ',w2.W2AreasPrwOld
            if(bail): sys.exit()
            return(0,None)
        else:
            return(1,oarea)
    else:
        print 'EEE big problem with area: ',area,'in getGfsGoesArea()'
        if(bail): sys.exit()
        return(-1,None)



class GfsGoes(MFbase):


    def __init__(self,model,dtg,channel,
                 dvorak=0,ortho=0,dowind=1,
                 dopinteg=0,xgrads='grads',
                 dtanl=6,ropt=''):

        self.nan=48
        self.nfc=72

        self.model=model
        self.dtg=dtg
        self.dopinteg=dopinteg
        self.dvorak=dvorak
        self.ortho=ortho
        self.dowind=dowind
        self.dtanl=dtanl
        self.channel=int(channel)
        self.ropt=ropt
        
        self.xgrads=xgrads

        self.sbdir="%s/%s"%(w2.Nwp2DataBdir,w2.Model2CenterModel(model))
        self.gfsdir="%s/w2flds/dat/gfs2"%(w2.Nwp2DataBdir)
        self.prcdir=w2.PrcDirFldanalW2
        self.odir='%s/sbt'%(w2.ptmpBaseDir)
        MF.ChkDir(self.odir,'mk')

        zoomfactX=0.90
        zoomfactY=0.950
        zoomfactY=1.0
        zoomfactX=1.0
        if(self.ortho):
            zoomfactX=0.90
            zoomfactY=0.90

        lutchannel=self.channel
        if(self.channel == 2): lutchannel=4

        lut="%s/GOES-Ch%02d.txt"%(self.prcdir,lutchannel)

        if(self.dvorak):
            self.channel=4
            lutchannel=4
            lut="%s/GOES-Ch%02d-BD.txt"%(self.prcdir,lutchannel)

        self.zoomfactX=zoomfactX
        self.zoomfactY=zoomfactY
        
        self.lut=lut
        self.zeroK=273.16
        self.gspath='%s/g.gfs.goes.gs'%(ptmpBaseDir)

        self.mapcolAN=7
        self.mapcolFC00=14
        self.mapcolFC24=13
        self.mapcolFC48=4
        self.mapcolFC72=14


    def setMapcol(self,tau):

        if(tau < 0): mapcol=self.mapcolAN
        if(tau >=0 and tau < 24): mapcol=self.mapcolFC00
        if(tau >=24 and tau < 48): mapcol=self.mapcolFC24
        if(tau >=48 and tau <= 72): mapcol=self.mapcolFC48

        return(mapcol)

    
    def cleanPng(self,ndaykeep=2,verb=1):

        mask="%s/*png"%(self.odir)
        files=glob.glob(mask)
        for ffile in files:
            if(ffile == None or not(type(ffile) == FloatType)): continue
            age=MF.PathModifyTimeCurdiff(ffile)/24.0
            dtkeep=age+ndaykeep
            if(dtkeep < 0.0):
                if(verb): print 'Klean: %5.1f'%(age),ffile
                try: os.unlink(ffile)
                except: None



    def setTauParams(self,tau,verb=0):
        
        bdtg=mf.dtginc(self.dtg,tau)
        bdtg0=bdtg[0:8]+'00'

        hh=int(bdtg[8:10])
        hplus=hh%self.dtanl
        h6=hh/self.dtanl
        h06=h6*self.dtanl
        h16=(h6+1)*self.dtanl
        dtg0=mf.dtginc(bdtg0,h06)
        dtg1=mf.dtginc(bdtg0,h16)
        if(h16 == 24): h16=0



        tau0=tau1=0

        if(tau >= 0):

            hh=int(dtg[8:10])
            hplus=tau%self.dtanl
            t6=tau/self.dtanl
            tau0=t6*self.dtanl
            tau1=(t6+1)*self.dtanl

            dtg0=dtg1=dtg
            h06=h16=hh

        self.ifact1=float(hplus)/self.dtanl
        self.ifact0=(1.0-self.ifact1)
        self.tau0=tau0
        self.tau1=tau1

        sdir0="%s/%s"%(self.sbdir,dtg0)
        self.goespath0="%s/gfs.t%02dz.goessimpgrb2.1p00.grib2.ctl"%(sdir0,h06)
        self.goespath0="%s/gfs.t%02dz.goessimpgrb2.0p25.grib2.ctl"%(sdir0,h06)

        sdir1="%s/%s"%(self.sbdir,dtg1)
        self.goespath1="%s/gfs.t%02dz.goessimpgrb2.1p00.grib2.ctl"%(sdir1,h16)
        self.goespath1="%s/gfs.t%02dz.goessimpgrb2.0p25.grib2.ctl"%(sdir1,h16)

        self.gfspath0="%s/%s/gfs2.w2flds.%s.ctl"%(self.gfsdir,dtg0,dtg0)
        self.gfspath1="%s/%s/gfs2.w2flds.%s.ctl"%(self.gfsdir,dtg1,dtg1)

        self.datathere=1
        if(tau >= 0 and
           not(MF.GetPathSiz(self.goespath0) > 0) and
           not(MF.GetPathSiz(self.gfspath0) > 0)
           ): self.datathere=0


        if(verb):
            print "     goespath0: ",self.goespath0
            print "     goespath1: ",self.goespath1
            print "      gfspath0: ",self.gfspath0
            print "      gfspath1: ",self.gfspath1
            print "     dtg0,dtg1: ",dtg0,dtg1
            print " ifact1,ifact0: ",self.ifact1,self.ifact0
            print "     tau0,tau1: ",self.tau0,self.tau1
            

    def getMainGs(self,parea):

        self.parea=parea
        AA=getW2Area(self.parea)
        
        self.loopdir=w2.W2LoopPltDir('prw')
        self.gifpath='%s/gfs.goes.chn%02d.%s.%s.loop.gif'%(self.loopdir,self.channel,self.parea,self.dtg)

        gs="""function main(args)

rc=gsfallow(on)
rc=const()

fhg0=ofile('%s')
fhg1=ofile('%s')

fhm0=ofile('%s')
fhm1=ofile('%s')

_area='%s'
'set lat %4.1f %5.1f'
'set lon %4.1f %5.1f'
#'set parea  %6.3f %6.3f %6.3f %6.3f'
_arwspace=1.0
_arwsize=0.04

"""%(self.goespath0,self.goespath1,
     self.gfspath0,self.gfspath1,
     self.parea,
     AA.latS,AA.latN,AA.lonW,AA.lonE,
     AA.pareaxl*self.zoomfactX,AA.pareaxr*self.zoomfactX,
     AA.pareayb*self.zoomfactY,AA.pareayt*self.zoomfactY)


        if(self.ortho):
            gs="""%s

'set lat -90 90'
'set lon 130 310'
'set mproj orthogr'
"""%(gs)

        # -- open the text file with the color table for chnl 3 -- h20 vapor
        #
        cards=open(self.lut).readlines()

        iskip=1
        nn=16   # start of user defined grads color 16-255
        nmax=240

        cvals='set clevs '
        rgbcols='set ccols %d'%(nn)

        for n in range(0,len(cards),iskip):
            j=len(cards)-n-1
            tt=cards[j].split()
            ndx=tt[0].split(':')[0]
            temp=float(tt[1].split(':')[1]) - self.zeroK
            red=int(tt[2].split(':')[1])
            green=int(tt[3].split(':')[1])
            blue=int(tt[4].split(':')[1])
            #print card,ndx,temp,red,green,blue
            if(nn>255 or n > nmax): continue
            cvals="%s %5.1f"%(cvals,temp)
            gscmd="""'set rgb %d %d %d %d'"""%(nn,red,green,blue)
            rgbcols="%s %d"%(rgbcols,nn)
            nn=nn+1

            gs=gs+"""%s
"""%(gscmd)


        gs=gs+"""
'%s'
"""%(cvals)

        if(self.channel == 2):  tchannel='IR2'
        if(self.channel == 3):  tchannel='W/V'
        if(self.channel == 4):  tchannel='IR4'
        if(self.channel == 4 and self.dvorak):  tchannel='IR4-BD curve'
        
        self.tchannel=tchannel
        self.rgbcols=rgbcols
        self.cvals=cvals


        return(gs)


    def getTauGs(self,tau,override=0,verb=0):


        oparea=self.parea
        if(self.ortho): oparea=self.parea

        if(tau >= 0):
            ftau=tau
            pngpath='%s/gfs.goes.chn%02d.%s.%s.f%03d.png'%(self.odir,self.channel,oparea,self.dtg,ftau)
        else:
            ftau=abs(tau)
            pngpath='%s/gfs.goes.chn%02d.%s.%s.m%03d.png'%(self.odir,self.channel,oparea,self.dtg,ftau)


        if(MF.ChkPath(pngpath)):
            print 'III pngpath: ',pngpath,' already done...'
            if(override):
                print 'OOO killing: ',pngpath,' because override = 1'
                cmd="rm %s"%(pngpath)
                mf.runcmd(cmd)
                
            else:
                return('')


        vdtg=mf.dtginc(self.dtg,tau)

        sbt0="sbtch%d.'fhg0'(time+%dhr)*%f"%(self.channel,self.tau0,self.ifact0)
        sbt1="sbtch%d.'fhg1'(time+%dhr)*%f"%(self.channel,self.tau1,self.ifact1)

        gssbt="""
'set dfile 'fhg0
'set t 1'
'sbt0=%s'

'set dfile 'fhg1
'set t 1'
'sbt1=%s'

'sbt=sbt0+sbt1 - %f'

"""%(sbt0,sbt1,self.zeroK)

        if(self.dopinteg):

            ubexpr="""  'ualevb=ua.'fhm0'(time+%dhr,lev='plev')*%f'"""%(self.tau0,1.0)
            vbexpr="""  'valevb=va.'fhm0'(time+%dhr,lev='plev')*%f'"""%(self.tau0,1.0)

            ubexprhi="""  'ualevbhi=ua.'fhm0'(time+%dhr,lev='plev2')*%f'"""%(self.tau0,1.0)
            vbexprhi="""  'valevbhi=va.'fhm0'(time+%dhr,lev='plev2')*%f'"""%(self.tau0,1.0)
            
            u0expr="""  'ualev0=ua.'fhm0'(time+%dhr,lev='plev')*%f'"""%(self.tau0,self.ifact0)
            v0expr="""  'valev0=va.'fhm0'(time+%dhr,lev='plev')*%f'"""%(self.tau0,self.ifact0)
            
            u1expr="""  'ualev1=ua.'fhm1'(time+%dhr,lev='plev')*%f'"""%(self.tau1,self.ifact1)
            v1expr="""  'valev1=va.'fhm1'(time+%dhr,lev='plev')*%f'"""%(self.tau1,self.ifact1)
            
        else:
            
            ubexpr="""  'ualevb=ua.'fhm0'(time+%dhr,lev='plev2')*%f'"""%(self.tau0,1.0)
            vbexpr="""  'valevb=va.'fhm0'(time+%dhr,lev='plev2')*%f'"""%(self.tau0,1.0)
            
            ubexprhi="""  'ualevbhi=ua.'fhm0'(time+%dhr,lev='plev2')*%f'"""%(self.tau0,1.0)
            vbexprhi="""  'valevbhi=va.'fhm0'(time+%dhr,lev='plev2')*%f'"""%(self.tau0,1.0)
            
            u0expr="""  'ualev0=ua.'fhm0'(time+%dhr,lev='plev2')*%f'"""%(self.tau0,self.ifact0)
            v0expr="""  'valev0=va.'fhm0'(time+%dhr,lev='plev2')*%f'"""%(self.tau0,self.ifact0)
            
            u1expr="""  'ualev1=ua.'fhm1'(time+%dhr,lev='plev2')*%f'"""%(self.tau1,self.ifact1)
            v1expr="""  'valev1=va.'fhm1'(time+%dhr,lev='plev2')*%f'"""%(self.tau1,self.ifact1)
            

        if(verb):
            print 'uuuuuuuuuuuuuuuuuuuuuuuuu ',ubexpr,u0expr,u1expr
            print 'vvvvvvvvvvvvvvvvvvvvvvvvv ',vbexpr,v0expr,v1expr

        mapcol=self.setMapcol(tau)
        
        gs=gssbt+"""

'c'
'%s'
'%s'
'set grads off'
#'set timelab on'
'set xlint 20'
#'set xlint 10'
'set ylint 10'

rc=plotdims()

'set mpdset mres'
'set map %d 1 6'
if(_area = 'prwEnso'); 'set map %d 1 5' ; endif
'set gxout shaded'
'set csmooth on'
'd sbt'
"""%(self.rgbcols,self.cvals,mapcol,mapcol)


        if(self.dowind):
            gs=gs+"""

nplevs=2
plev2=200
plevs='500 300'
pwghts='250 200'
pwghttot='450'
levb=600
levt=200

_prwsden=4
_cthkbb=10
_cthk=4
_cthkb=4
_bskip=8
if(_area = 'prwWpac'); _bskip=10 ; endif
if(_area = 'prwIo'); _bskip=10 ; endif
if(_area = 'prwEnso'); _bskip=16 ; endif
# -- 0p25 gfs2 
_bskip=_bskip*2
_prwbskip=8

dostrm=1
do200strm=1
dostrmbarb=0
dobarb=1
dxs=0.85
bskip=_bskip


# -- time 0 winds
#

'set dfile 'fhm0
'set t 1'

'u20=const(ua(lev='plev2'),0,-a)'
'v20=u20'
'u2b=u20'
'v2b=v20'

dopinteg=%d

if(dopinteg)

  k=1
  while(k<=nplevs)
    plev=subwrd(plevs,k)
    pwght=subwrd(pwghts,k)

    'set dfile 'fhm0
    'set t 1'
# -- get 200 wind for streams
#
    %s
    %s
    %s
    %s
    %s
    %s

    'set dfile 'fhm1
    'set t 1'
    %s
    %s

    'ualev=ualev0+ualev1'
    'valev=valev0+valev1'

    'u2b=u2b+ualevb*('pwght')'
    'v2b=v2b+valevb*('pwght')'
    'u20=u20+ualev*('pwght')'
    'v20=v20+valev*('pwght')'
    'vfact=(0.01*0.622)*'pwght

    k=k+1
  endwhile

  'u2b=(u2b*'_ms2kt') / 'pwghttot
  'v2b=(v2b*'_ms2kt') / 'pwghttot
  'u20=(u20*'_ms2kt') / 'pwghttot
  'v20=(v20*'_ms2kt') / 'pwghttot

else

  'set dfile 'fhm0
  'set t 1'
# -- get 200 wind for streams
#
  %s
  %s
  %s
  %s
  %s
  %s

  'set dfile 'fhm1
  'set t 1'
  %s
  %s

  'ualev=ualev0+ualev1'
  'valev=valev0+valev1'

  'u2b=ualevb'
  'v2b=valevb'
  'u20=ualev'
  'v20=valev'

endif


# -- streams
#
if(dostrm)

if(do200strm)
  'u20s=re2(ualevbhi,'dxs')'
  'v20s=re2(valevbhi,'dxs')'
  'm20s=(mag(ualevbhi,valevbhi)*'_ms2kt')'
else
  'u20s=re2(u2b,'dxs')'
  'v20s=re2(v2b,'dxs')'
  'm20s=mag(u20,v20)'
endif

'u2s=u20s'
'v2s=v20s'
'm2s=mag(u2s,v2s)'
'set gxout stream'
'set arrowhead 0.010'
'set strmden '_prwsden' '_arwspace' '_arwsize
'set cthick '_cthkbb
'set ccolor 0'
'd u2s;v2s'

#'set clevs 10 15 20 35 50 65 100'
#'set rbrange 0 100'

'set cthick '_cthk
'set ccolor 7'

'd u2s;v2s'


if(dostrmbarb)

'set gxout barb'
'set cthick '_cthkb
'set cthick 10'
'set ccolor 0'
'set digsiz 0.05'
if(_area = 'prwEnso'); 'set digsiz 0.035' ; endif


vmin=25
vmax=65
vmin=20
vmax=50
vminn=10

'd skip(u2s,'bskip');maskout(v2s,m2s-'vminn')'

'set cthick 5'
'set ccolor 3'
'd skip(u2s,'bskip');maskout(v2s,m2s-'vminn')'

'set cthick '_cthkbb
'set ccolor 0'
'd skip(u2s,'bskip');maskout(v2s,m2s-'vmin')'

'set cthick 5'
'set ccolor 2'
'd skip(u2s,'bskip');maskout(v2s,m2s-'vmin')'

'set cthick '_cthkbb
'set ccolor 0'
'd skip(u2s,'bskip');maskout(v2s,m2s-'vmax')'

'set cthick 6'
'set ccolor 4'
'd skip(u2s,'bskip');maskout(v2s,m2s-'vmax')'
endif

endif

# -- do barbs only
#
if(dobarb)

#'u20s=re2(u20,1.0)'
#'v20s=re2(v20,1.0)'
#'m20s=mag(u20,v20)'


'u2s=u20'
'v2s=v20'
'm2s=mag(u2s,v2s)'

'set gxout barb'
'set digsiz 0.040'
'set digsiz 0.045'
if(_area = 'prwEnso'); 'set digsiz 0.035' ; endif

'set cthick 5' ; 'set ccolor 0'
'd maskout(u2s,m2s-2.5);skip(v2s,'bskip')'

'set cthick 10' ; 'set ccolor 0'
'd maskout(u2s,m2s-25);skip(v2s,'bskip')'

'set cthick 5' ; 'set ccolor 3'
'd maskout(u2s,m2s-25);skip(v2s,'bskip')'

'set cthick 10' ; 'set ccolor 0'
'd maskout(u2s,m2s-50);skip(v2s,'bskip')'

'set cthick 5' ; 'set ccolor 2'
'd maskout(u2s,m2s-50);skip(v2s,'bskip')'

endif



"""%(self.dopinteg,
     ubexpr,vbexpr,ubexprhi,vbexprhi,u0expr,v0expr,u1expr,v1expr,
     ubexpr,vbexpr,ubexprhi,vbexprhi,u0expr,v0expr,u1expr,v1expr,
     )


        wtitle=''
        if(dowind):
            if(self.dopinteg):
                wtitle='+ GFS 0.5`3.`0 500-300 mb Winds'
            else:
                wtitle='+ GFS 0.5`3.`0 200 mb Winds'
                

        if(tau >= 0): otau="+%02d"%(tau)
        if(tau < 0): otau="-%02d"%(abs(tau))

        bttau='m000'
        if(tau <= 0):
            bttau="m%03d"%(abs(tau))
        else:
            bttau="f000"

        gs=gs+"""

'cbarn2 1.0 0 0.50'
'set map %d 1 6'
if(_area = 'prwEnso'); 'set map %d 1 5' ; endif
'draw map'
# -- draw bt

rc=plotdims()
'set clip '_xlplot' '_xrplot' '_ybplot' '_ytplot
dtau=1

rc=settcbt()

_tau=%d
_bttau=%s

_btcoltc=3
_btcol=6
_btszscl=1.0

_ftbcol=1
_ftfcol=2

if(_bttau != 'f000')
  rc=prwtcbt()
  rc=drawtcbt()
endif

if(_tau > 0) 
  rc=prwtcft()
  rc=ftposits(_tau,_tau,dtau)
  rc=drawtcft()
endif

'set clip 0 '_pagex' 0 '_pagey

t1='GFS 1.0`3.`0 GOES12 Chnl %d (%s) %s'
t2=''
rc=toptitle(t1,t2,1.0)

st1='BDTG: %s `3t`0= %s h `4VDTG: %s'
rc=stitle(st1,1.0)


#'gxyat -x 1024 -y 768 -r %s'
'printim %s x%d y%d black'
print 'PPPPP: %s'

"""%(mapcol,mapcol,tau,bttau,
     self.channel,self.tchannel,wtitle,
     self.dtg,otau,vdtg,
     pngpath,pngpath,AA.xsize,AA.ysize,pngpath)

        self.pngpath=pngpath

        return(gs)



    def runGs(self,gs):

        MF.WriteString2File(gs,gG.gspath)
        cmd='''%s -lbc "%s"'''%(self.xgrads,gG.gspath)
        MF.runcmd(cmd)



    def makeSbtAnimGifLoop(self,override=0):

        dtbeg=100
        dtend=100
        dtfc=50
        dtloop=8
        dtpause=24

        gifcmd="convert -loop 0 -delay %d "%(dtbeg)

        if(MF.ChkPath(self.gifpath) and not(override)):
            print 'LLL alldone with loop gif for dtg: ',self.dtg,' area: ',self.parea
            return


        for n in range(self.nan,0,-1):
            
            path='%s/gfs.goes.chn%02d.%s.%s.m%03d.png'%(self.odir,self.channel,self.parea,self.dtg,n)
            print 'aaaaaaaaaaaa ',path,os.path.exists(path)
            if(os.path.exists(path)):
                if(n == self.nan):
                    gifcmd="%s -delay %d %s"%(gifcmd,dtloop,path)
                elif(n == 0):
                    gifcmd="%s -delay %d %s"%(gifcmd,dtbeg,path)
                elif(n%dtpause == 0):
                    gifcmd="%s -delay %d %s"%(gifcmd,dtfc,path)
                else:
                    gifcmd="%s -delay %d %s"%(gifcmd,dtloop,path)

        for n in range(0,self.nfc+1):
            path='%s/gfs.goes.chn%02d.%s.%s.f%03d.png'%(self.odir,self.channel,self.parea,self.dtg,n)
            print 'ffffffffffffffff ',path,os.path.exists(path)
            if(os.path.exists(path)):
                if(n%dtpause == 0 and n != self.nfc):
                    gifcmd="%s -delay %d %s"%(gifcmd,dtfc,path)
                elif(n == self.nfc):
                    gifcmd="%s -delay %d %s"%(gifcmd,dtend,path)
                else:
                    gifcmd="%s -delay %d %s"%(gifcmd,dtloop,path)


        gifcmd="%s %s"%(gifcmd,self.gifpath)
        mf.runcmd(gifcmd,self.ropt)


    def getTCgs(self,dtx=1):

        tcsource='tmtrkN'
        if(tcsource == 'tmtrkN'):
            tcaids=['t'+model]
        elif(tcsource == 'mftrkN'):
            tcaids=['m'+model]

        tBG=TcFtBtGsf(tcsource,tstmids=None,tdtg=self.dtg,taids=tcaids,
                      tD=tD,
                      dtx=dtx,
                      ATtauRange='-12.0',BTtauRange='%d.0'%(-1*self.nan),ATOtauRange='0.%d'%(self.nfc),
                      verb=verb)
        tBG.getABs()

        setgsf =tBG.makeSetTcGsf()
        btgsf  =tBG.makeTcFtBtGsf('bt')
        ftgsf  =tBG.makeTcFtBtGsf('ft')
        dbtgsf =tBG.makeDrawBtGsf()
        dftgsf =tBG.makeDrawFtGsf()

        gs=setgsf+btgsf+ftgsf+dbtgsf+dftgsf

        return(gs)



    def cpTaus2Loopdir(self,tdir,ropt=''):

        taus2keep=['m048','m024','f000','f024','f048','f072']
        cpopt='-v -p -u'
        if(onKishou): cpopt='-v -p -n'
        if(override): cpopt='-v -p'

        for tau in taus2keep:
            cmd="cp %s %s/*%s*%s* %s/."%(cpopt,self.odir,self.dtg,tau,tdir)
            mf.runcmd(cmd,ropt)




#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
#
# command line setup
#

class WgetCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv
        
        self.argv=argv
        self.argopts={
            1:['dtgopt',    'no default'],
            2:['parea',    'no default'],
            }

        self.defaults={
            'model':'gfs2',
            }

        self.options={
            'override':        ['O',0,1,'override'],
            'verb':            ['V',0,1,'verb=1 is verbose'],
            'ropt':            ['N','','norun',' norun is norun'],
            'tauopt':          ['t:','all','a','tau range'],
            'channel':         ['C:',3,'i','channel to plot'],
            'dvorak':          ['D',0,1,'use channel 4 and BD curve'],
            'doregen':         ['R',0,1,'regen to wxmap2a/'],
            'ortho':           ['S',0,1,'do orthographic projection'],
            'dowind':          ['W',0,1,'plot 500-300 layer mean wind'],
            'doloop':          ['L',0,1,'make animated gif loop'],
            'doall':           ['A',0,1,'do all processes'],
            'docpOnly':        ['P',0,1,'only cp tau files over'],
            'doRsync2Wx2':     ['x',0,1,'do rsync 2 wxmap2.com'],
            'doRsync2Wx2Only': ['X',0,1,'do rsync 2 wxmap2.com Only'],
            }

        self.purpose='''
purpose -- wget mirror gfs stb (sat brightness t) goes images
for prwareas: %s
'''%(str(AllAreas))
        self.examples='''
%s cur
'''
    def err(self,type):
        if(type == 'tauopt'):
            print """EEE tauopt= 'ftaus'|btau,etau"""
            sys.exit()


    def setTausets(self,tauopt):

        tausets=[]
        tt=tauopt.split(',')

        if(tauopt == 'ftaus' or tauopt == 'all'):
            endtau=72
            tausets.append((0,endtau))

        if(tauopt == 'btaus' or tauopt == 'all'):

            begtau=-48
            dtau=6
            for btau in range(begtau,0,dtau):
                tausets.append((btau,btau+dtau-1))

        if(tauopt == 'all' or tauopt == 'ftaus' or tauopt == 'btaus'): return(tausets)

        if(len(tt) == 2):
            btau=int(tt[0])
            etau=int(tt[1])
            tausets.append((btau,etau))

        elif(len(tt) == 1):
            btau=int(tt[0])
            etau=btau
            tausets.append((btau,etau))

        else:
            tausets=None

        return(tausets)


        

#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
# main
#


MF.sTimer(tag='gfs.stb.plot')
argv=sys.argv
CL=WgetCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

dtgs=mf.dtg_dtgopt_prc(dtgopt,ddtg=6)

xgrads='grads'
xgrads=setXgrads()
pareaOpt=parea

# -- rsync to wxmap2
#
if(doRsync2Wx2Only):
    MF.sTimer('rsync2Wx2-Only')
    rc=rsync2Wxmap2('wxmap2',ropt)
    MF.dTimer('rsync2Wx2-Only')
    sys.exit()

if(doall or pareaOpt == 'all' or ( len(dtgs) > 1 ) and not(docpOnly)):

    for dtg in dtgs:

        if(pareaOpt != 'all'): AllAreas=[parea]

        for parea in AllAreas:

            (rc,parea)=getGfsGoesArea(parea)
            
            archopt=''
            overopt=''
            if(override): overopt='-O'
            if(doregen): archopt='-a'
            cmd="%s/%s %s %s -t btaus -W %s %s"%(pydir,pyfile,dtg,parea,overopt,archopt)
            mf.runcmd(cmd,ropt)

            cmd="%s/%s %s %s -t ftaus -W %s %s"%(pydir,pyfile,dtg,parea,overopt,archopt)
            mf.runcmd(cmd,ropt)

            cmd="%s/%s %s %s -L %s %s"%(pydir,pyfile,dtg,parea,overopt,archopt)
            mf.runcmd(cmd,ropt)

    # -- 20211122 - after cycling, THEN do the rsync2Wx2
    #
    cmd="%s/%s %s all -X"%(pydir,pyfile,dtg)
    mf.runcmd(cmd,ropt)

    sys.exit()


# -- dtg cycling handled above...
#

dtgs=mf.dtg_dtgopt_prc(dtgopt,ddtg=6)
dtg=dtgs[0]

# -- get parea using either prw or goes form
#
(rc,parea)=getGfsGoesArea(parea)

# -- check how old this run -- if 'tooold' force regen
#
howold=mf.dtgdiff(dtg,curdtg)/24.0
tooold=(howold > w2.W2MaxOldRegen)
if(tooold):  doregen=1

# -- doregen
#
if(doregen):
    w2.W2BaseDirWeb=w2.W2RegenBaseDirWeb
    w2.PrwGoesDir="%s/plt_prw_goes"%(w2.W2BaseDirWeb)

MF.sTimer(tag='chkifrunning')
rc=w2.ChkIfRunningNWP(dtg,pyfile,model,killjob=0,verb=1)
if(rc > w2.nMaxPidInCron and w2.dochkifrunning):
    if(ropt != 'norun'):
        print 'AAA allready running...sayounara'
        sys.exit()
MF.dTimer(tag='chkifrunning')


if(docpOnly):

    for dtg in dtgs:
        # -- make ojbect
        #
        gG=GfsGoes(model,dtg,channel,dvorak,ortho,dowind,xgrads=xgrads)

        # -- cp individual tau files to dir for owen
        #
        taupltdir="%s/%s"%(w2.PrwGoesDir,dtg)
        mf.ChkDir(taupltdir,'mk')

        gG.cpTaus2Loopdir(taupltdir,ropt='')
        
    sys.exit()


# -- get data status; make .ctl ONLY if taus >= minTauGoes
#
m=setModel2('goes')
minTauGoes=72
fm=m.DataPath(dtg,dowgribinv=1,override=override)
fd=fm.GetDataStatus(dtg)

if(not(minTauGoes in fd.dsitaus)):
    print 'WWW mintau: ',minTauGoes,' not ready...sayoonara'
    sys.exit()
else:
    print """III we're good fd.dsitaus: """,fd.dsitaus,' dtg: ',dtg


if(not(doloop)):
    tausets=CL.setTausets(tauopt)
    if(tausets == None): CL.err('tauopt')

if(channel == 3): dowind=1

# aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa -- area
#
AA=getW2Area(parea)
if(AA == None):
    print 'EEE invalid parea: ',parea
    sys.exit()


gG=GfsGoes(model,dtg,channel,dvorak,ortho,dowind,xgrads=xgrads)
# -- set TcData by first analysis dtg vice dtg (years in getMD2years shifts on 011500)
bdtgTCd=mf.dtginc(dtg,-gG.nan)
tD=TcData(dtgopt=bdtgTCd)

taupltdir="%s/%s"%(w2.PrwGoesDir,dtg)
mf.ChkDir(taupltdir,'mk')

# mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm -- make .gif loop
#
if(doloop):
    gG.setTauParams(0)
    gs=gG.getMainGs(parea)
    gG.makeSbtAnimGifLoop(override=override)
    # -- make inventory after loop gif made
    rc=makePrwInventory(gG.loopdir,verb=verb)
    sys.exit()


# mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm -- loop by sets of taus
#

gsTC=gG.getTCgs()

for tauset in tausets:
    
    (btau,etau)=tauset
    taus=range(btau,etau+1)
    tau0=taus[0]
    
    gG.setTauParams(tau0)

    doft=1
    if(taus[0] < 0): doft=0

    # bail if no data available
    if(doft and gG.datathere == 0):
        print 'EEE not tau>=0 goes data there...bail'
        sys.exit()

    gs=gG.getMainGs(parea)

    #gsffc=gG.getTcFCposits(verb=verb)
    #gsfbt=gG.getTcBTposits(verb=verb)
    #gsf=gsfbt+gsffc+gG.setDrawtcGsf()

    for tau in taus:

        #gsf=gsf+gG.setDrawtcGsf()
        gG.setTauParams(tau,verb=verb)
        gs=gs+gG.getTauGs(tau,override=override)

    gs=gs+"""'quit'
"""
    gs=gs+gsTC
    
    if(ropt != 'norun'): gG.runGs(gs)

# -- clean off files > ndaykeep old
#
rc=gG.cleanPng()
rc=gG.cpTaus2Loopdir(taupltdir,ropt='')

# -- do the prw/goes inventory for prw2.htm (will rename later)
#
### rc=makePrwInventory(loopdir,verb=verb)

MF.dTimer(tag='gfs.stb.plot')

# -- rsync to wxmap2
#
if(doRsync2Wx2):
    MF.sTimer('rsync2Wx2')
    rc=rsync2Wxmap2('wxmap2',ropt)
    MF.dTimer('rsync2Wx2')
    





