import os,glob
import mf

import w2
import w2env
import FM
import grads

ropt=''

fr1=FM.FieldRequest1()


class w2Env:
    
    prodcenter=w2env.W2_PROD_CENTER
    geodir=w2env.W2_GEODIR
    climosstdir=w2env.W2_CLIMOSST
    climodatdir=w2env.W2_CLIMODAT
    prcdir=w2.PrcDirFldanalW2
    cfgdir=w2.PrcCfgBdirW2
    basemapdir=w2env.W2_BASEMAP_GDIR


class w2Cfg:

    
    def __init__(self,cfgdir=None,area='tropwac',
                 proj=None,geores=None,pareabd=None,
                 lon1=None,lon2=None,lat1=None,lat2=None,
                 mplon1=None,mplon2=None,mplat1=None,mplat2=None,
                 xlint=None,ylint=None,
                 vpagebd=None):

        self.proj=proj
        self.geores=geores
        self.pareabd=pareabd
        self.lon1=lon1
        self.lon2=lon2
        self.lat1=lat1
        self.lat2=lat2
        self.mplon1=mplon1
        self.mplon2=mplon2
        self.mplat1=mplat1
        self.mplat2=mplat2
        self.xlint=xlint
        self.ylint=ylint
        self.vpagebd=vpagebd
        

        if(area != None and cfgdir != None):
            
            try:
                cards=open("%s/area.%s.cfg"%(cfgdir,area)).readlines()
            except:
                cards=[]

            def floatchk(val):
                if(val != 'default'):
                    oval=float(val)
                else:
                    oval=None
                return(oval)


            for i in range(0,len(cards)):

                print 'i ',i,cards[i][0:-1]
                card=cards[i].strip()
                if(i==0):  self.proj=card
                if(i==1):  self.geores=card
                if(i==2):  self.pareabd=card
                if(i==3):  self.lon1=float(card)
                if(i==4):  self.lon2=float(cards[i].strip())
                if(i==5):  self.lat1=float(cards[i].strip())
                if(i==6):  self.lat2=float(cards[i].strip())
                if(i==7):  self.mplon1=floatchk(card)
                if(i==8):  self.mplon2=floatchk(card)
                if(i==9):  self.mplat1=floatchk(card)
                if(i==10):  self.mplat2=floatchk(card)
                if(i==11): self.xlint=int(card)
                if(i==12): self.ylint=int(card)
                
            self.vpagebd='0.1 10.9 0.1 8.4'

    def SetGrads(self,ga):

        if(self.proj != None): ga('set mproj  ' + self.proj)
        if(self.geores != None): ga('set mpdset ' + self.geores)
        
        if(self.pareabd != None): ga('set parea ' + self.pareabd)
        if(self.vpagebd != None): ga('set vpage ' + self.vpagebd)
        
        if(self.lat1 != None and self.lat2 != None): ga("set lat %f %f"%(self.lat1,self.lat2))
        if(self.lon1 != None and self.lon2 != None): ga("set lon %f %f"%(self.lon1,self.lon2))
        
        if((self.proj == 'nps' or self.proj == 'sps' or self.proj == 'lambert') and self.mplon1 != None):
            ga("set mpvals %f %f %f %f"%(self.mplon1,self.mplon2,self.mplat1,self.mplat2))
            
        if(self.xlint != None): ga("set xlint %d"%(self.xlint))
        if(self.ylint != None): ga("set ylint %d"%(self.ylint))


class W2Plot():

    def __init__(self,ga,var=None):

        self.var=var
        self.ga=ga

        ga('set grads off')
        
        pcol='54 53 52 61 42 43 44 45 47 48 49 69 68 67 66 65 64 63 21 22 23 24 25 26'

        self.cmds="""run jaecol.gsf
q dims
q ctlinfo
q gxinfo

set rbrange -14 20
set rbcols %s
set clevs  -14 -12 -10 -8 -6 -4 -2  2   4  6  8  10  12  14  16 18 20
set ccols 54  53  52  61 42 43 44 0 47  48 49 69  68  67  66  65 64 63 21 22 23 24 25 26

set rgb 49  00 20 60
set rgb 47  00 40 100
set rgb 43  00 60 150
set rgb 61  00 120 200

set rgb 69 20  5 00
set rgb 68 50  5 00
set rgb 67 100 10 00
set rgb 66 120 10 00
set rgb 65 130 10 00
set rgb 64 150 40 0
set rgb 63 170 60 00
set rgb 21 200 100 00
set rgb 22 255 232 120
set rgb 22 255 140 100

set clevs  -14  -12  -10 -8  -6  -4  -2   2  4   6   8  10  12  14  16  18  20
set ccols 57   55  52  61  43  47   0   0   0  29  28  27  26 25  24  23  22 21 25 26
set cint 2
set gxout shaded

set lev 500
d hcurl(ua,va)*1e5
cbarc.gs

"""%(pcol)
        
        self.cmds="d psl"

        ga(self.cmds)

        


#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# main
#


#fe9=FM.FimExp()
#f9=FM.FimRun(FimExp=fe9)

fe8=FM.FimExp()
fe8.expopt='g8wrftopo'

f8=FM.FimRun(FimExp=fe8)

g8=FM.PlotMaps(f8,f8,xgrads='grads2',window=1,opt="-g 1024x760-0+0").ga

w2e=w2Env()
area='tropwpac'
w2c=w2Cfg(w2e.cfgdir,area)
w2c.SetGrads(g8)
w2p=W2Plot(g8,var='psl')

dh=g8.query('dims')

#g9=FM.PlotMaps(f8,f9,window=1,opt="-g 1024x760+0+0").ga
#f9=FM.FimRun(dtg,fimver,glvl,nlvl,npes,expopt,sroot,troot,fimtype)

#p1=FM.PrsCtl(dtg=dtg)
#h1=FM.HblCtl(dtg=dtg)
#h1.WriteCtl(F1.tDir)
#p1.WriteCtl(F1.tDir)

    

