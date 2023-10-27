#!/usr/bin/env python

from WxMAP2 import *
w2=W2()

from M2 import setModel2

from ga2 import setGA,GaLats,GaLatsQ

class GaLats(GaLats):

    prcdir=w2.W2BaseDirPrc
    
    def cmd2(self,gacmd,RcCheck=0):
        self._ga.cmd2(gacmd,Quiet=0,RcCheck=RcCheck)


    def __init__(self,ga,ge,dtg=None,
                 model='rtfim',
                 center='esrl',
                 comment='grib1 output for tm tracker',
#                 outconv='grads_grib',
                 outconv='grib_only',
                 calendar='standard',
                 ptable="%s/hfip/lats.hfip.table.txt"%(prcdir),
                 frequency='forecast_hourly',
                 timeoption='dim_env',
                 gridtype='linear',
                 btau=0,
                 etau=168,
                 dtau=24,
                 regrid=0,
                 remethod='re',
                 smth2d=0,
                 doyflip=0,
                 quiet=0,
                 reargs=None,
                 ):

        if(hasattr(ga,'quiet')): quiet=ga.quiet
        self.initGrads(ga,ge,quiet=quiet)

        self.ga=ga
        self.ge=ge

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

        
        self.ptable=ptable
        self.outconv=outconv
        self.calendar=outconv
        self.model=model
        self.center=center
        self.comment=comment
        self.timeoption=timeoption
        self.frequency=frequency
        self.gridtype=gridtype


    def initTaus(self,taus=None):

        if(taus == None):
            self.taus=range(self.btau,self.etau+1,self.dtau)
        else:
            self.taus=taus
            



    def initParams(self):

        self("set_lats parmtab %s"%(self.ptable))
        self("set_lats convention %s"%(self.outconv))
        self("set_lats calendar %s"%(self.calendar))
        self("set_lats model %s"%(self.model))
        self("set_lats center %s"%(self.center))
        self("set_lats comment %s"%(self.comment))
        self("set_lats timeoption %s"%(self.timeoption))
        self("set_lats frequency %s"%(self.frequency))
        
        if(self.frequency == 'forecast_hourly'):
            self("set_lats deltat %d"%(self.dtau))
        elif(self.frequency == 'forecast_minutes'):
            self("set_lats deltat %d"%(self.dtau*60))

        self("set_lats gridtype %s"%(self.gridtype))

        if(hasattr(self.ga,'fh')):
            self.fh=self.ga.fh
        else:
            print 'EEE GaLats(Q) needs a fh object (file handle) in the grads.ga object'
            sys.exit()
        
        self.ge.getFileMeta(self)



    def outvars(self,svars,uavars,verb=1):

        for tau in self.taus:
            vdtg=mf.dtginc(self.dtg,tau)
            gtime=mf.dtg2gtime(vdtg)

            self("set time %s"%(gtime))
            if(self.frequency == 'forecast_hourly'):
                self("set_lats fhour %f "%(tau))
            elif(self.frequency == 'forecast_minutes'):
                self("set_lats fminute %f "%(tau*60))

            #-- uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu ua vars
            #
            for uavar in uavars:
                (name,varexpr,type,levs)=uavar
                id=self.id_uvars[name]

                for lev in levs:
                    self("set_lats write %d %d %f"%(self.id_file,self.id_uvars[name],lev))
                    self("set lev %f"%(lev))
                    
                    self('dvar=%s'%(varexpr))
                    
                    if(lev in self.levs):
                        expr='dvar'
                    else:
                        if(verb): print 'IIII dooohhh!  ',lev,' not in: y',self.levs,' do ln(p) interp...'
                        expr=self.LogPinterp('dvar',lev)

                    if(verb): print 'IIII lev: ',lev,' varexpr: ',varexpr,' expr: ',expr
                            
                    if(self.regrid > 0):
                        
                        
                        if(self.remethod == 're2'):
                            if(hasattr(self,'reargs') and self.reargs != None):
                                expr="re2(dvar,%s)"%(self.reargs)
                            else:
                                expr="re2(dvar,%5.3f)"%(self.regrid)
                        else:
                            if(hasattr(self,'reargs') and self.reargs != None):
                                expr="re(dvar,%s)"%(self.reargs)
                            else:
                                expr="re(dvar,%d,linear,0.0,%f,%d,linear,-90.0,%f)"%(self.nxre,self.dlon,self.nyre,self.dlat)

                    if(self.smth2d > 0):
                        expr="smth2d(%s,%d)"%(expr,self.smth2d)

                    self("lats_data %s"%(expr))
                    if(verb):
                        for n in range(1,self._ga.nLines):
                            print self._ga.rline(n)

            #-- sssssssssssssssssssssssssssssssssssssss sfc vars
            #
            for svar in svars:
                
                (name,varexpr,type)=svar
                id=self.id_svars[name]

                self("set_lats write %d %d 0"%(self.id_file,self.id_svars[name]))
                self('dvar=%s'%(varexpr))
                expr='dvar'

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

    def plevdim(self,uavars,verb=1):

        plevs=[]
        for uavar in uavars:
            plevs=plevs+uavar[3]

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
            (name,expr,type,levs)=uavar
            self("set_lats var %d %s %s %d %d"%(self.id_file,name,type,self.id_grid,self.id_vdim))
            self.id_uvars[name]=int(self.rw(1,5))

    def sfcvars(self,svars):

        self.id_svars={}
        for svar in svars:
            (name,expr,type)=svar
            self("set_lats var %d %s %s %d 0"%(self.id_file,name,type,self.id_grid))
            self.id_svars[name]=int(self.rw(1,5))




class AreaGlobal(W2areas):


    def __init__(self,
                 lonW=0.0,
                 lonE=360.0,
                 latS=-90.0,
                 latN=90.0,
                 dx=0.5,
                 dy=0.5,
                 ):

        self.setLons(lonW,lonE)
        self.setLats(latS,latN)

        self.setGrid(dx,dy)


class EcmGts(MFbase):

    wgetopt=' -nv -m -nd -T 20 -t 2'
    
    model='ecmg'

    btau1=0
    etau1=168
    dtau1=24

    vars1=[
        'ua.200','ua.500','ua.700','ua.850',
        'va.200','va.500','va.700','va.850',
        'hur.700','hur.850'
        ]

    taus1=range(btau1,etau1+1,dtau1)
    res1='2p5'

    btau2=0
    etau2=240
    dtau2=24

    taus2=range(btau2,etau2+1,dtau2)
    vars2=['u','v','t','msl','gh']
    res2='0p5'

    dtauAll=24

    minsiz=1000
    
    def __init__(self,dtg,
                 tauPlot=168,
                 override=0):

        self.dtg=dtg
        self.override=override
        
        self.mE=setModel2(self.model)
        self.mE.setDbase(self.dtg)
        tdir=self.mE.dbasedir
        MF.ChkDir(tdir,'mk')
        mf.ChangeDir(tdir)

        self.tauPlot=tauPlot

        self.tdirNwp2=tdir

        tdirW2flds="%s/%s"%(self.mE.w2fldsSrcDir,self.dtg)
        self.tdirW2flds=tdirW2flds

        self.iE=InvHash(self.model,tbdir=self.mE.bddir,override=override)
        self.ctlpath2='''%s/%s.%s.%s.ctl'''%(tdir,self.model,self.dtg,self.res2)
        self.ctlpath1='''%s/%s.%s.%s.ctl'''%(tdir,self.model,self.dtg,self.res1)

        self.area=AreaGlobal()


    def getFinalTaus(self):

        mask="%s/%s.w2flds.%s.f*.grb1"%(self.tdirW2flds,self.model,self.dtg)
        finalpaths=glob.glob(mask)

        finalTaus=[]
        for path in finalpaths:
            tau=int(path.split('.')[-2][1:])
            finalTaus.append(tau)
            
        self.finalTaus=mf.uniq(finalTaus)


    def doPlot(self,override=0,ropt='',doweb=1):

        self.getFinalTaus()

        ovropt=''
        if(override): ovropt='-O'
        if(self.tauPlot in self.finalTaus):
            cmd="%s/w2-plot.py %s %s %s"%(w2.PrcDirFldanalW2,self.dtg,self.model,ovropt)
            mf.runcmd(cmd,ropt)

        (odtg,ocurfphr)=mf.dtg_phr_command_prc(self.dtg)

        curfphr=float(ocurfphr)
        if(doweb or override or curfphr <= w2.maxfphrWeb):

            webopt='-u'
            if(curfphr > w2.maxfphrWeb): webopt=''

            cmd="%s/w2.web.py %s %s"%(w2.PrcDirWebW2,self.dtg,webopt)
            mf.runcmd(cmd,ropt)

    def getMask(self,var,tau):
    
        (var,level)=var.split('.')
        if(var == 'ua'): pnum='131'
        if(var == 'va'): pnum='132'
        if(var == 'hur'): pnum='157'

        mask="%s_%02d00_%s_128_%s_%d"%(self.dtg[0:8],int(self.dtg[8:10]),pnum,level,tau)

        return(mask)

    def wgetGrib1(self):

        hurl="www.ecmwf.int/products/realtime/d/gts/file/additional/"


        lasttau=self.taus1[-1]

        try:
            nlast=self.tausGot2.index(lasttau)
        except:
            nlast=-1

        finalNlast=nlast
        if(nlast > 0): finalNlast=nlast+1

        gettaus=self.tausGot2[0:finalNlast]

        self.nfilesGrib1=0

        for tau in gettaus:
            for var in self.vars1:
                mask=self.getMask(var,tau)

                if(MF.GetPathSiz(mask) < self.minsiz and MF.GetPathSiz(mask) != None):
                    print 'WWW small file: ',mask
                    os.unlink(mask)
                    
                if(not(MF.ChkPath(mask))):
                    cmd="wget %s  \"http://%s/%s\""%(self.wgetopt,hurl,mask)
                    mf.runcmd(cmd,ropt)
                    self.nfilesGrib1=self.nfilesGrib1+1
                    
                # -- check if it was small and try again
                #
                if(MF.GetPathSiz(mask) < self.minsiz):
                    print 'WWW small file2222222222: ',mask
                    os.unlink(mask)
                    cmd="wget %s  \"http://%s/%s\""%(self.wgetopt,hurl,mask)
                    mf.runcmd(cmd,ropt)
                    self.nfilesGrib1=self.nfilesGrib1+1


    def wgetGrib2(self,nfilesTot=11):

        # -- 0.5 deg wmo essential
        #
        hurl='wmo:essential@data-portal.ecmwf.int'
        self.nfilesGrib2=0
        
        for var in self.vars2:
            files=glob.glob("*_%s_*"%(var))
            
            if(len(files) < nfilesTot):
                self.nfilesGrib2=nfilesTot-len(files)
                cmd='''wget %s "ftp://%s/%s0000/*h_%s_*"'''%(self.wgetopt,hurl,dtg,var)
                mf.runcmd(cmd,ropt)

                cmd='''wget %s "ftp://%s/%s0000/*n_%s_*"'''%(self.wgetopt,hurl,dtg,var)
                mf.runcmd(cmd,ropt)


    def prcGrib2(self,
                 ropt=1,
                 override=0):


        inv=self.iE.hash

        tausGot=[]
        taufiles={}

        for var in self.vars2:
            files=glob.glob("*_%s_*"%(var))
            for file in files:
                tt=file.split('_')
                tau=tt[5]
                var=tt[6]
                if(tau == 'an'):
                    tau=0
                elif(tau[-1] == 'h'):
                    tau=int(tau[0:-1])

                taufile="%s.%s.%s.f%03d.grb2"%(self.model,self.dtg,self.res2,tau)
                taufiles[tau]=taufile
                tausGot.append(tau)
                if(override):
                    try:
                        os.unlink(taufile)
                    except:
                        None
                


        for var in self.vars2:
            files=glob.glob("*_%s_*"%(var))
            for file in files:
                tt=file.split('_')
                tau=tt[5]
                var=tt[6]
                if(tau == 'an'):
                    tau=0
                elif(tau[-1] == 'h'):
                    tau=int(tau[0:-1])

                taufile=taufiles[tau]


                try:
                    cfiles=inv[self.dtg]
                except:
                    cfiles=[]

                cfiles=mf.uniq(cfiles)

                if(not(file in cfiles) or override):

                    cmd="cat %s >> %s"%(file,taufile)
                    mf.runcmd(cmd,ropt)
                    MF.appendDictList(inv,self.dtg,file)
                    print 'file: ',file,tau,var

        self.tausGot2=mf.uniq(tausGot)
        
        self.iE.put()

        dset='''%s.%s.%s.f%%f3.grb2'''%(self.model,self.dtg,self.res2)
        dgmp='''%s.%s.%s.gmp2'''%(self.model,self.dtg,self.res2)
        gtime=mf.dtg2gtime(self.dtg)
        nt=((self.etau2-self.btau2)/self.dtau2)+1
        nt=len(self.tausGot2)

        ctl='''dset ^%s
index ^%s
undef 9.999E+20
title ecmg.2012060312.0p5.f000.grb2
options template pascals
*  produced by g2ctl v0.0.4m
* griddef=1:0:(720 x 361):grid_template=0:winds(N/S): lat-lon grid:(720 x 361) units 1e-06 input WE:NS output WE:SN res 48 lat 90.000000 to -90.000000 by 0.500000 lon 0.000000 to 359.500000 by 0.500000 #points=259920:winds(N/S)
dtype grib2
xdef 720 linear 0.000000 0.500000
ydef 361 linear -90.000000 0.5
zdef 2 levels 85000 50000
tdef %d linear %s %dhr
vars 5
zg    2,100   0,3,5 ** 500 mb Geopotential Height [gpm]
psl   0,101   0,3,0 ** mean sea level Pressure [Pa]
ta    2,100   0,0,0 ** temperature [K]
ua    2,100   0,2,2 ** 850 mb U-Component of Wind [m/s]
va    2,100   0,2,3 ** 850 mb V-Component of Wind [m/s]
endvars'''%(dset,dgmp,nt,gtime,self.dtau2)

        MF.WriteString2File(ctl,self.ctlpath2,verb=1)

        cmd="gribmap -v -i %s"%(self.ctlpath2)
        mf.runcmd(cmd,ropt)

        
        
    
    def prcGrib1(self,
                 override=0,
                 ropt=1):

        inv=self.iE.hash

        files=glob.glob("%s*"%(dtg[0:8]))

        taufiles={}
        for file in files:
            tt=file.split('_')
            tau=int(tt[5])
            taufile="%s.%s.%s.f%03d.grb1"%(self.model,self.dtg,self.res1,tau)
            taufiles[tau]=taufile

            if(override):
                try:
                    os.unlink(taufile)
                except:
                    None
                
            

        for file in files:
            tt=file.split('_')
            tau=int(tt[5])
            taufile=taufiles[tau]

            try:
                cfiles=inv[dtg]
            except:
                cfiles=[]

            cfiles=mf.uniq(cfiles)

            if(MF.GetPathSiz(file) < self.minsiz): continue

            if(not(file in cfiles) or override):

                cmd="cat %s >> %s"%(file,taufile)
                mf.runcmd(cmd,ropt)
                MF.appendDictList(inv,dtg,file)

        dset='''%s.%s.%s.f%%f3.grb1'''%(self.model,self.dtg,self.res1)
        dgmp='''%s.%s.%s.gmp1'''%(self.model,self.dtg,self.res1)
        gtime=mf.dtg2gtime(self.dtg)
        nt=((self.etau1-self.btau1)/self.dtau1)+1

        ctl='''dset ^%s
index ^%s
undef 9.999E+20
title ecmg.2012060312.2p5.f000.grb1
options template yrev
*  produced by g2ctl v0.0.4m
* griddef=1:0:(720 x 361):grid_template=0:winds(N/S): lat-lon grid:(720 x 361) units 1e-06 input WE:NS output WE:SN res 48 lat 90.000000 to -90.000000 by 0.500000 lon 0.000000 to 359.500000 by 0.500000 #points=259920:winds(N/S)
dtype grib
xdef 144 linear   0.0 2.5
ydef  73 linear -90.0 2.5
zdef 4 levels 850 700 500 200 
tdef %d linear %s %dhr
vars 3
hur  2 157,100,0 ** Relative humidity [%%]
ua   4 131,100,0 ** U velocity [m s**-1]
va   4 132,100,0 ** V velocity [m s**-1]
endvars'''%(dset,dgmp,nt,gtime,self.dtau1)

        MF.WriteString2File(ctl,self.ctlpath1,verb=1)

        cmd="gribmap1 -E -v -i %s"%(self.ctlpath1)
        mf.runcmd(cmd,ropt)

        self.iE.put()
    

    def doGaLats(self,type,
                 odtau=12,
                 gaopt='-g 1024x768',
                 dowindow=0,
                 quiet=0,
                 override=0,
                 verb=0,
                 ):


        def setGtimes(btau,etau,tau):
        
            vdtg1=mf.dtginc(self.dtg,btau)
            gtime1=mf.dtg2gtime(vdtg1)
            vdtg2=mf.dtginc(self.dtg,etau)
            gtime2=mf.dtg2gtime(vdtg2)
            
            fact1=float(etau-tau)/lentau
            fact2=1.0-fact1

            return(gtime1,fact1,gtime2,fact2)
        

        def setVars2(btau,etau,tau):

            (gtime1,fact1,gtime2,fact2)=setGtimes(btau,etau,tau)
            
            uavars=[]
            uexpr='(ua(time=%s)*%f + ua(time=%s)*%f)'%(gtime1,fact1,gtime2,fact2)
            vexpr='(va(time=%s)*%f + va(time=%s)*%f)'%(gtime1,fact1,gtime2,fact2)
            zexpr='(zg(time=%s)*%f + zg(time=%s)*%f)'%(gtime1,fact1,gtime2,fact2)
            pexpr='(psl(time=%s)*%f + psl(time=%s)*%f)'%(gtime1,fact1,gtime2,fact2)
            uavars.append(('ua',uexpr,'instant',[850]))
            uavars.append(('va',vexpr,'instant',[850]))
            uavars.append(('zg',zexpr,'instant',[500]))
            
            svars=[]
            svars.append(('psl',pexpr,'instant'))

            topath='/%s/%s.w2flds.%s.t%03d.%s'%(self.tdir,self.model,self.dtg,tau,self.res2)
            return(uavars,svars,topath)

        def setVars1(btau,etau,tau):

            (gtime1,fact1,gtime2,fact2)=setGtimes(btau,etau,tau)
            
            uavars=[]
            uexpr='(ua(time=%s)*%f + ua(time=%s)*%f)'%(gtime1,fact1,gtime2,fact2)
            vexpr='(va(time=%s)*%f + va(time=%s)*%f)'%(gtime1,fact1,gtime2,fact2)
            hexpr='(hur(time=%s)*%f + hur(time=%s)*%f)'%(gtime1,fact1,gtime2,fact2)
            uavars.append(('ua',uexpr,'instant',[700,500,200]))
            uavars.append(('va',vexpr,'instant',[700,500,200]))
            uavars.append(('hur',hexpr,'instant',[850,700]))
            
            svars=[]

            topath='/%s/%s.w2flds.%s.t%03d.%s'%(self.tdir,self.model,self.dtg,tau,self.res1)
            return(uavars,svars,topath)



        
        tdir=self.tdirW2flds
        MF.ChkDir(tdir,'mk')

        self.tdir=tdir

        itaus=self.tausGot2

        taubands=[]
        for n in range(0,len(itaus)-1):
            taubands.append((itaus[n],itaus[n+1]))


        if(type == 'grb1'):
            ga=setGA(Opts=gaopt,Quiet=quiet,Window=dowindow,verb=self)
            ga.fh=ga.open(self.ctlpath1)
            
        elif(type == 'grb2'):
            ga=setGA(Opts=gaopt,Quiet=quiet,Window=dowindow,verb=self)
            ga.fh=ga.open(self.ctlpath2)
            
        ge=ga.ge

        self.doregrid=1
        self.remethod='bs' # use re default for change in res  'ba' for fine->coarse and 'bl' for coarse->fine
        self.rexopt='linear'
        self.reyopt='linear'

        self.setReargs()
        smth2d=0


        gl=GaLats(ga,ge,
                  dtg=self.dtg,model=self.model,
                  regrid=self.doregrid,
                  reargs=self.reargs,
                  smth2d=smth2d,
                  )

        gl.initParams()
        gl.grid(self.area)

        if(not(hasattr(self,'alltaus'))): self.alltaus=[]
        
        for tauband in taubands:

            btau=tauband[0]
            etau=tauband[1]
            lentau=etau-btau

            taus=range(btau,etau+1,odtau)
            self.alltaus=self.alltaus+taus

            for tau in taus:

                finaltaupath="%s/%s.w2flds.%s.f%03d.grb1"%(self.tdir,self.model,self.dtg,tau)

                if(type == 'grb1'):
                    (uavars,svars,topath)=setVars1(btau,etau,tau)
                elif(type == 'grb2'):
                    (uavars,svars,topath)=setVars2(btau,etau,tau)

                finalopath="%s.grb"%(topath)

                pathtest=( MF.ChkPath(finalopath,verb=0) or MF.ChkPath(finaltaupath) )
                if(pathtest and not(override)): continue

                otaus=[tau]
                gl.initTaus(otaus)
                gl.create(topath)
                gl.basetime(self.dtg)

                if(len(uavars) > 0):
                    gl.plevdim(uavars)
                    gl.plevvars(uavars)

                gl.sfcvars(svars)

                gl.outvars(svars,uavars)
                gl.close()


    def setReargs(self):
        
        aa=self.area

        if(self.remethod == ''):
            self.reargs="%d,%s,%f,%f,%d,%s,%f,%f"%(aa.ni,self.rexopt,aa.lonW,aa.dx,aa.nj,self.reyopt,aa.latS,aa.dy)
        else:
            self.reargs="%d,%s,%f,%f,%d,%s,%f,%f,%s"%(aa.ni,self.rexopt,aa.lonW,aa.dx,aa.nj,self.reyopt,aa.latS,aa.dy,self.remethod)

        if(not(self.doregrid)): self.reargs=None


    def finalGrib(self,ropt=''):


        alltaus=mf.uniq(self.alltaus)

        dset="%s.w2flds.%s.f%%f3.grb1"%(self.model,self.dtg)
        gmap="%s.w2flds.%s.gmp1"%(self.model,self.dtg)
        ctlpath="%s/%s.w2flds.%s.ctl"%(self.tdir,self.model,self.dtg)

        nt=len(alltaus)
        gtime=mf.dtg2gtime(self.dtg)
        if(len(alltaus) > 1):
            dtau=alltaus[1]-alltaus[0]
        else:
            dtau=self.dtauAll

        for tau in alltaus:

            tfiles=glob.glob("%s/*.t%03d.*"%(self.tdir,tau))

            if(len(tfiles) >= 2):
                
                finalpath='/%s/%s.w2flds.%s.f%03d.grb1'%(self.tdir,self.model,self.dtg,tau)
                # -- blow away final because of >>
                #
                try:
                    os.unlink(finalpath)
                except:
                    None

                print
                for tfile in tfiles:

                    cmd="cat %s >> %s"%(tfile,finalpath)
                    mf.runcmd(cmd,ropt)
                    cmd="rm %s"%(tfile)
                    mf.runcmd(cmd,ropt)

        ctl='''dset ^%s
index ^%s
undef 9.999E+20
title ecmg.w2flds.2012060312.f000.grb1
* produced by grib2ctl v0.9.12.5p16 defined parameter table (center 59-5 table 128), using NCEP-opn
dtype grib 255
options template 
xdef 720 linear   0.0 0.5
ydef 361 linear -90.0 0.5
zdef   4 levels 850 700 500 200
tdef  %d linear %s %dhr
vars 6
psl   0  2,102,0  ** Pressure reduced to MSL [Pa]
zg    4  7,100,0  ** Geopotential height [gpm]
hur   4 52,100,0 ** Relative humidity [%%]
ua    4 33,100,0 ** u wind [m/s]
va    4 34,100,0 ** v wind [m/s]
ta    4 11,100,0 ** temperature
ENDVARS'''%(dset,gmap,nt,gtime,dtau)
        
        MF.WriteString2File(ctl,ctlpath,verb=1)

        cmd="gribmap -v -i %s"%(ctlpath)
        mf.runcmd(cmd,ropt)



                             

        

#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
#
# command line setup
#

class MssCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv
        
        self.argv=argv
        self.argopts={
            1:['dtgopt',    'no default'],
            }

        self.defaults={
            }

        self.options={
            'verb':          ['V',0,1,'verb=1 is verbose'],
            'ropt':          ['N','','norun',' norun is norun'],
            'override':      ['O',0,1,'override'],
            'doplots':       ['P',1,0,'do NOT do plots'],
            'doplotOnly':    ['p',0,1,' norun is norun'],
            'doweb':         ['W',0,1,' do web'],
            }

        self.purpose='''
purpose -- mirror ecmwf gts fields
%s cur
'''
        self.examples='''
%s cur'''

MF.sTimer(tag='all')

CL=MssCmdLine(argv=sys.argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

dtg=mf.dtg_command_prc(dtgopt)

eG=EcmGts(dtg)

if(doplotOnly):
    eG.doPlot(override=override,doweb=doweb)
    sys.exit()


eG.wgetGrib2()
eG.prcGrib2(ropt=ropt,override=override)
eG.doGaLats(type='grb2',override=override)

eG.wgetGrib1()
eG.prcGrib1(ropt=ropt,override=override)
eG.doGaLats(type='grb1',override=override)

eG.finalGrib(ropt=ropt)

if(doplots):
    eG.doPlot(override=override,doweb=doweb)

sys.exit()


